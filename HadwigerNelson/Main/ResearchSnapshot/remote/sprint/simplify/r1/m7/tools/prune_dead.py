#!/usr/bin/env python3
"""Conservative dead-declaration pruner for the OAI tree.

A declaration is a *candidate* iff it is not a node of the m10 sound proof-term
closure of the 7 headline declarations AND carries no attribute AND is not an
instance (attributes/instances are used implicitly by `simp`/typeclass search,
so they are never touched).  Candidates are then thinned to a fixed point: a
candidate survives only if no *kept* declaration mentions its unqualified name
in its (comment-stripped) body.

Deletion is by trimmed block: the block runs from the declaration keyword to the
last line of its body (stop at the first top-level structural command or next
declaration keyword; track (), [], {}, comment nesting) and is extended upwards
over modifiers that would otherwise dangle (`omit ... in`, `include ... in`,
`@[...]`, `noncomputable`, `private`, `protected`) plus blank/comment lines.

  python3 prune_dead.py --root DIR --spans S.json --log L.log [--apply] [--out P]
"""
import argparse, json, pathlib, re, collections

BREAK = re.compile(r"^\s*(end|section|noncomputable\s+section|open|variable|namespace|attribute|"
                   r"set_option|local|include|omit|universe|export|#|@\[|/--|/-!)")
KW = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+")
MODIF = re.compile(r"^\s*(omit\b.*\bin\s*$|include\b.*\bin\s*$|noncomputable\s*$|private\s*$|"
                   r"protected\s*$|scoped\s*$|@\[[^\]]*\]\s*$)")
OPEN = {"(": ")", "[": "]", "{": "}", "\u27e8": "\u27e9"}
CLOSE = {v: k for k, v in OPEN.items()}


def depth_profile(lines):
    out, d, com = [], 0, 0
    for ln in lines:
        i, n = 0, len(ln)
        while i < n:
            if com:
                if ln.startswith("-/", i):
                    com -= 1; i += 2
                else:
                    i += 1
            elif ln.startswith("/-", i):
                com += 1; i += 2
            elif ln.startswith("--", i):
                break
            elif ln[i] in OPEN:
                d += 1; i += 1
            elif ln[i] in CLOSE:
                d -= 1; i += 1
            else:
                i += 1
        out.append((d, com))
    return out


def strip_comments(t):
    out, com = [], 0
    for ln in t.splitlines():
        o, i, n = [], 0, len(ln)
        while i < n:
            if com:
                if ln.startswith("-/", i):
                    com -= 1; i += 2
                else:
                    i += 1
            elif ln.startswith("/-", i):
                com += 1; i += 2
            elif ln.startswith("--", i):
                break
            else:
                o.append(ln[i]); i += 1
        out.append("".join(o))
    return "\n".join(out)


def body_end(lines, start, stop0, bound):
    """0-based exclusive end index of the declaration whose keyword is at `start`.

    `stop0`/`bound` bound the search (exclusive 0-based).
    """
    seg = lines[start:bound]
    prof = depth_profile(seg)
    stop = len(seg)
    for i in range(1, len(seg)):
        d, com = prof[i - 1]
        if d == 0 and com == 0 and (BREAK.match(seg[i]) or KW.match(seg[i])):
            stop = i
            break
    last = None
    for i in range(stop):
        if seg[i].strip():
            last = i
    if last is None:
        return None
    return start + last + 1


def extend_up(lines, start):
    """Eat dangling modifiers / comments / blank lines directly above `start`."""
    i = start
    while i > 0:
        j = i - 1
        st = lines[j].strip()
        if not st or st.startswith("--") or MODIF.match(lines[j]):
            i = j; continue
        if st.endswith("-/"):
            k = j
            while k > 0 and "/-" not in lines[k]:
                k -= 1
            i = k; continue
        break
    return i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--spans", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--allow-attr", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    sp = json.loads(pathlib.Path(a.spans).read_text())
    nodes = set()
    for ln in pathlib.Path(a.log).read_text().splitlines():
        if ln.startswith("NODE "):
            nodes.add(ln.split(" ", 2)[2].strip())

    mods = sorted({v["mod"] for v in sp.values()})
    src = {m: (root / "lean" / (m.replace(".", "/") + ".lean")).read_text(errors="ignore").splitlines()
           for m in mods}
    bymod = collections.defaultdict(list)
    for name, d in sp.items():
        bymod[d["mod"]].append((d["line"], name, d))
    for m in bymod:
        bymod[m].sort()

    def attr_or_instance(m, name, d):
        ls = src[m]
        i = d["line"] - 1
        if d["kind"] == "instance":
            return True
        if a.allow_attr:
            return False
        return any(ls[k].lstrip().startswith("@[") for k in range(max(0, i - 3), min(len(ls), i + 1)))

    cand = {}
    for m, ds in bymod.items():
        for idx, (line, name, d) in enumerate(ds):
            if name in nodes or attr_or_instance(m, name, d):
                continue
            bound = (ds[idx + 1][0] - 1) if idx + 1 < len(ds) else len(src[m])
            if bound <= line:
                continue
            end = body_end(src[m], line - 1, None, bound)
            if end is None or end <= line - 1:
                continue
            s0 = extend_up(src[m], line - 1)
            cand[name] = dict(mod=m, line=s0 + 1, end=end, lines=end - s0, kind=d["kind"])

    body_text, pat = {}, {}
    for m, ds in bymod.items():
        ls = src[m]
        for idx, (line, name, d) in enumerate(ds):
            nxt = (ds[idx + 1][0] - 1) if idx + 1 < len(ds) else len(ls)
            body_text[name] = strip_comments("\n".join(ls[line - 1:nxt]))
    for name in sp:
        sh = name.split(".")[-1]
        pat[name] = re.compile(r"(?<![A-Za-z0-9_'!?])" + re.escape(sh) + r"(?![A-Za-z0-9_'!?])")

    kept = set(sp) - set(cand)
    changed = True
    while changed:
        changed = False
        for name in list(cand):
            for k in kept:
                if k != name and pat[name].search(body_text[k]):
                    kept.add(name); cand.pop(name); changed = True
                    break
    total = sum(v["lines"] for v in cand.values())
    per = collections.Counter()
    for v in cand.values():
        per[v["mod"]] += v["lines"]
    print(f"candidates after thinning: {len(cand)} declarations, {total} lines")
    for m, l in per.most_common():
        print(f"  {l:5d} {m}")
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(cand, indent=1))
    if not a.apply:
        for name, v in sorted(cand.items(), key=lambda kv: -kv[1]["lines"])[:15]:
            print(f"  {v['lines']:4d} {v['mod']}:{v['line']}-{v['end']} {name}")
        return
    written = []
    for m, ds in bymod.items():
        blocks = sorted({(v["line"], v["end"]) for n, v in cand.items() if v["mod"] == m}, reverse=True)
        ls = list(src[m])
        for s, e in blocks:
            del ls[s - 1:e]
        new = "\n".join(ls) + "\n"
        p = root / "lean" / (m.replace(".", "/") + ".lean")
        if new != p.read_text():
            p.write_text(new)
            written.append(m)
    print(f"applied; {len(written)} files rewritten")
    for m in written:
        print("  wrote", m)


main()
