#!/usr/bin/env python3
"""Usage index over the OAI tree: for each declaration, how many times its short
name occurs elsewhere in the tree (crude but effective), plus its span.
Prints declarations sorted by (span desc) filtered by usage<=1 (candidate dead
or single-use leaves) and a module summary.
"""
import re, os, sys, json, argparse, collections

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")

def walk(root):
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            if f.endswith(".lean"):
                yield os.path.join(dp, f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--usagemax", type=int, default=1)
    ap.add_argument("--minlines", type=int, default=8)
    a = ap.parse_args()
    files = list(walk(a.root))
    text = {f: open(f, encoding="utf-8", errors="ignore").read() for f in files}
    lines = {f: text[f].splitlines() for f in files}
    decls = []
    for f in files:
        rel = os.path.relpath(f, a.root)
        stack, found = [], []
        for i, ln in enumerate(lines[f], 1):
            m = NS.match(ln)
            if m: stack.append(m.group(1)); continue
            if SEC.match(ln) or MUT.match(ln): stack.append(""); continue
            eo = END.match(ln)
            if eo:
                nm = eo.group(1)
                if nm and nm in stack:
                    while stack and stack.pop() != nm: pass
                elif stack: stack.pop()
                continue
            d = DECL.match(ln)
            if d:
                kind, name = d.group(1), d.group(2)
                if name in ("where", "at", "at'"): continue
                pre = ".".join(x for x in stack if x)
                found.append((kind, name, (pre + "." + name) if pre else name, i))
        for j, (kind, name, full, i) in enumerate(found):
            end = (found[j+1][3] - 1) if j + 1 < len(found) else len(lines[f])
            decls.append(dict(file=rel, kind=kind, name=name, full=full, line=i, end=end,
                              lines=end - i + 1))
    # occurrence count of the short name over the whole tree, minus its own headers
    TOK = re.compile(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?\u00a1-\uffff]*")
    cnt = collections.Counter()
    for f in files:
        for t in TOK.findall(text[f]):
            cnt[t] += 1
    hdr = collections.Counter()
    for d in decls:
        hdr[d["name"]] += 1
    for d in decls:
        d["uses"] = cnt[d["name"]] - hdr[d["name"]]
    out = [d for d in decls if d["lines"] >= a.minlines and 0 <= d["uses"] <= a.usagemax]
    out.sort(key=lambda d: -d["lines"])
    tot = sum(d["lines"] for d in out)
    print(f"{len(decls)} decls, {sum(d['lines'] for d in decls)} lines; "
          f"{len(out)} with uses<={a.usagemax} and lines>={a.minlines}, {tot} lines")
    per = collections.Counter()
    for d in out:
        per[d["file"]] += d["lines"]
    for f, n in per.most_common(25):
        print(f"  {n:5d} {f}")
    print()
    for d in out[:60]:
        print(f"{d['lines']:5d} uses={d['uses']:3d} {d['file']}:{d['line']} {d['full']}")

main()
