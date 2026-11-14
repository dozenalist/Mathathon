#!/usr/bin/env python3
"""Cut every declaration of the tree that m10's DECLGRAPH.log never reached.

Dead = the declaration's full name is absent from the NODE lines AND no declaration
of the same (module, short name) was reached.

  python3 cut.py --tree sprint/simplify/r1/m5/stage --spans MYSPANS.json \
                 [--log sprint/simplify/m10/harness/DECLGRAPH.log] [--apply] \
                 [--revert-module MOD ...] [--report OUT.json]
"""
import json, re, os, sys, argparse, pathlib, collections

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
ENDL = re.compile(r"^\s*end(?:\s+[\w.]+)?\s*$")

def scan(root):
    root = pathlib.Path(root)
    out = {}
    for p in sorted((root / "lean" / "OAI").rglob("*.lean")):
        mod = ".".join(p.relative_to(root / "lean").with_suffix("").parts)
        lines = p.read_text(errors="ignore").splitlines()
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
                kind, name = d.group(1), d.group(2)
                if name in ("where", "at", "at'"): continue
                pre = ".".join(x for x in stack if x)
                found.append((kind, name, (pre + "." + name) if pre else name, i))
        for j, (kind, name, full, i) in enumerate(found):
            end = (found[j+1][3] - 1) if j + 1 < len(found) else len(lines)
            out.setdefault(mod, []).append(dict(name=name, full=full, line=i, end=end,
                                                lines=end - i + 1))
    return out, root

def deletable_region(lines, start, end):
    """1-based inclusive [start,end] -> exclusive slice end, keeping trailing
    structural `end` lines, trailing doc comments (they belong to the next decl)
    and dropping blanks."""
    j = end
    while j > start and lines[j-1].strip() == '': j -= 1
    while j > start and ENDL.match(lines[j-1]): j -= 1
    if j > start and lines[j-1].strip().endswith('-/'):
        k = j - 1
        while k > start and not lines[k-1].strip().startswith('/--'): k -= 1
        j = k
    while j > start and lines[j-1].strip() == '': j -= 1
    return j

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--log", default="sprint/simplify/m10/harness/DECLGRAPH.log")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", default=None)
    ap.add_argument("--revert", nargs="*", default=[])
    a = ap.parse_args()
    reached = set()
    reachedpairs = set()
    for line in open(a.log, encoding="utf-8", errors="ignore"):
        p = line.split()
        if p and p[0] == "NODE":
            reached.add(p[2])
            reachedpairs.add((p[1], p[2].split(".")[-1]))
    decls, root = scan(a.tree)
    dead = []
    for mod, ds in decls.items():
        for d in ds:
            if d["full"] in reached: continue
            if (mod, d["name"]) in reachedpairs: continue
            dead.append(dict(mod=mod, **d))
    tot = sum(d["lines"] for d in dead)
    print(f"dead: {len(dead)} declarations, {tot} span-lines")
    per = collections.Counter()
    for d in dead: per[d["mod"]] += d["lines"]
    for m, L in per.most_common(50): print(f"  {L:5d} {m}")
    if a.report:
        json.dump(dead, open(a.report, "w"), indent=0)
    if not a.apply:
        return
    bymod = collections.defaultdict(list)
    for d in dead: bymod[d["mod"]].append(d)
    killed = 0
    for mod, ds in bymod.items():
        if mod in a.revert: continue
        p = root / "lean" / (mod.replace(".", "/") + ".lean")
        lines = p.read_text(errors="ignore").splitlines()
        for d in sorted(ds, key=lambda d: -d["line"]):
            j = deletable_region(lines, d["line"], min(d["end"], len(lines)))
            del lines[d["line"]-1:j]
            killed += j - (d["line"] - 1)
        p.write_text("\n".join(lines) + "\n")
    print(f"applied: removed {killed} raw lines from {len(bymod) - len(a.revert)} modules")

main()
