#!/usr/bin/env python3
"""Emit the concrete deletion list for a route: every declaration the route frees,
as module:line-end name, with the attribute closure kept (fixpoint).

  python3 candidates.py OUT.txt NAME... [--keep NAME...]
"""
import collections
import json
import pathlib
import sys

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
H = REPO / "sprint/simplify/m10/harness"
ROOTS = ["OAI.EuclideanFiveColor.no_proper_five_coloring",
         "OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic",
         "OAI.Problem160.properColoring_seven",
         "OAI.EuclideanFiveColor.proper_iff_weak",
         "OAI.Problem160.chromaticNumber_bounds",
         "OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null",
         "OAI.EuclideanFiveColor.algebraic_colorable_iff"]

nodes, et, ev = {}, collections.defaultdict(set), collections.defaultdict(set)
for ln in (H / "DECLGRAPH.log").read_text().splitlines():
    ln = ln.strip()
    if ln.startswith("NODE "):
        _, m, n = ln.split(" ", 2)
        nodes[n] = m
    elif ln.startswith("EDGET "):
        _, a, b = ln.split(" ", 2)
        et[a].add(b)
    elif ln.startswith("EDGEV "):
        _, a, b = ln.split(" ", 2)
        ev[a].add(b)
sp = json.loads((REPO / ".ultramath/smwg224wy/m3/SPANS_stage.json").read_text())
allgl = set(json.loads((REPO / ".ultramath/smwg224wy/m3/GLOBALISH_ALL.json").read_text()))


def closure(drop, keep):
    d, seen, st = set(drop), set(), list(ROOTS) + list(keep)
    while st:
        n = st.pop()
        if n in seen:
            continue
        seen.add(n)
        st.extend(et.get(n, ()))
        if n not in d:
            st.extend(ev.get(n, ()))
    return seen


out = sys.argv[1]
argv = sys.argv[2:]
keep = []
if "--keep" in argv:
    i = argv.index("--keep")
    keep = [x for x in argv[i + 1:] if x]
    argv = argv[:i]
drop = set(argv)
full = closure((), ())
while True:
    extra = sorted(((full - closure(drop, keep)) & allgl) - set(keep))
    if not extra:
        break
    keep += extra
freed = full - closure(drop, keep)
rows = sorted((sp[n]["mod"], sp[n]["line"], sp[n]["end"], n) for n in freed if n in sp)
per = collections.Counter()
for m, a, b, n in rows:
    per[m] += b - a + 1
lines = [f"# route: drop {sorted(drop)}; keep {sorted(keep)}",
         f"# freed: {len(rows)} declarations, {sum(per.values())} span lines",
         "# module | line-end | name",
         ""]
cur = None
for m, a, b, n in rows:
    if m != cur:
        lines.append(f"## {m}  ({per[m]} lines)")
        cur = m
    lines.append(f"{a:5d}-{b:<5d} {n}")
pathlib.Path(out).write_text("\n".join(lines) + "\n")
print(f"wrote {out}: {len(rows)} declarations, {sum(per.values())} lines, {len(per)} modules")
