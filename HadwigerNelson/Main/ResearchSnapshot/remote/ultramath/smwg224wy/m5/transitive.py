#!/usr/bin/env python3
"""Transitive dead-declaration cut.

Reachability is computed textually from the 7 headline declarations: a declaration
is live if it is named inside the text of a live declaration.  Two safety rules:
  * any declaration carrying an `@[...]` attribute is *always* live (it may be used
    by `simp`/`instance` search without being named), and it propagates liveness;
  * only theorem/lemma/abbrev declarations are ever cut (never def/instance/
    structure/inductive/opaque), so the environment's interfaces are untouched.
Then cut, recompute, repeat.

  python3 transitive.py --work PRISTINE --dst OUT [--max N]
"""
import re, os, argparse, pathlib, shutil, collections

DECL = re.compile(r"^(?P<attr>@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(?P<kind>theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+(?P<name>[^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
ENDL = re.compile(r"^\s*end(?:\s+[\w.]+)?\s*$")
STRUCT = re.compile(r"^\s*(variable|open|section|omit|attribute|set_option|universe|local\b|private\b|scoped\b|noncomputable\b|include\b)\b")
TOK = re.compile(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?\u00a1-\uffff]*")
ROOTS = ["no_proper_five_coloring", "no_proper_five_coloring_algebraic",
         "properColoring_seven", "proper_iff_weak", "chromaticNumber_bounds",
         "not_proper_five_coloring_compl_null", "algebraic_colorable_iff"]
SAFE = {"theorem", "lemma", "abbrev"}

def deletable_region(lines, start, end):
    j = end
    while j > start and lines[j-1].strip() == '': j -= 1
    while j > start and (ENDL.match(lines[j-1]) or STRUCT.match(lines[j-1])
                         or lines[j-1].lstrip().startswith('--')): j -= 1
    if j > start and lines[j-1].strip().endswith('-/'):
        k = j - 1
        while k > start and not lines[k-1].strip().startswith('/--'): k -= 1
        j = k
    while j > start and lines[j-1].strip() == '': j -= 1
    return j

def scan(root):
    out = []
    files = {}
    for f in sorted((root / "lean" / "OAI").rglob("*.lean")):
        text = f.read_text(errors="ignore")
        files[str(f)] = text
        lines = text.splitlines()
        stack, found = [], []
        for i, ln in enumerate(lines, 1):
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
                kind, name = d.group("kind"), d.group("name")
                if name in ("where", "at", "at'"): continue
                pre = ".".join(x for x in stack if x)
                found.append((kind, bool(d.group("attr")), name,
                              (pre + "." + name) if pre else name, i))
        for j, (kind, attr, name, full, i) in enumerate(found):
            end = (found[j+1][4] - 1) if j + 1 < len(found) else len(lines)
            out.append(dict(kind=kind, attr=attr, name=name, full=full, line=i,
                            end=end, lines=end - i + 1, path=str(f),
                            text="\n".join(lines[i-1:end])))
    return out, files

def liveness(decls):
    byname = collections.defaultdict(list)
    for d in decls: byname[d["name"]].append(d)
    live = set()
    dq = []
    for d in decls:
        if d["name"] in ROOTS: live.add(d["full"]); dq.append(d)
        elif d["attr"] and d["kind"] in SAFE | {"def", "instance"}: live.add(d["full"]); dq.append(d)
    while dq:
        d = dq.pop()
        for t in set(TOK.findall(d["text"])):
            if t == d["name"]: continue
            for e in byname.get(t, ()):
                if e["full"] not in live:
                    live.add(e["full"]); dq.append(e)
    return live

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--max", type=int, default=15)
    a = ap.parse_args()
    dst = pathlib.Path(a.dst)
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(pathlib.Path(a.work) / "lean", dst / "lean")
    total = 0
    for it in range(1, a.max + 1):
        decls, _ = scan(dst)
        live = liveness(decls)
        dead = [d for d in decls if d["full"] not in live and d["kind"] in SAFE]
        if not dead:
            print(f"iter {it}: fixpoint, {len(live)} live decls"); break
        per = collections.defaultdict(list)
        for d in dead: per[d["path"]].append(d)
        removed = 0
        for path, ds in per.items():
            p = pathlib.Path(path)
            lines = p.read_text(errors="ignore").splitlines()
            for d in sorted(ds, key=lambda d: -d["line"]):
                j = deletable_region(lines, d["line"], min(d["end"], len(lines)))
                del lines[d["line"]-1:j]
                removed += j - (d["line"] - 1)
            p.write_text("\n".join(lines) + "\n")
        total += removed
        print(f"iter {it}: {len(dead)} dead decls, {removed} raw lines removed "
              f"({sum(d['lines'] for d in dead)} span-lines), from {len(per)} files")
    n = sum(1 for f in (dst / "lean" / "OAI").rglob("*.lean") for _ in open(f, errors="ignore"))
    print(f"total removed {total}; final tree {n} raw lines, "
          f"{len(list((dst / 'lean' / 'OAI').rglob('*.lean')))} modules")

main()
