#!/usr/bin/env python3
"""Owner-based safety test for the dead-declaration set.

For every declaration span in the staged tree we know its owner.  A name occurrence
inside the span of a *live* declaration (one reachable in m10's DECLGRAPH closure) is
a real reference; an occurrence inside a *dead* declaration (or outside every span:
imports, namespace, instances, comments) is not evidence of use by the surviving
proofs.  Reports the dead set split into SAFE (no live-span occurrence) and REVIEW.
"""
import collections
import json
import pathlib
import re

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
H = REPO / "sprint/simplify/m10/harness"
ROOT = REPO / "sprint/simplify/stage/lean"
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


def closure(drop_v=()):
    d, seen, st = set(drop_v), set(), list(ROOTS)
    while st:
        n = st.pop()
        if n in seen:
            continue
        seen.add(n)
        st.extend(et.get(n, ()))
        if n not in d:
            st.extend(ev.get(n, ()))
    return seen


FULL = closure()
sp = json.loads((REPO / ".ultramath/smwg224wy/m3/SPANS_stage.json").read_text())
src = {}
for p in (ROOT / "OAI").rglob("*.lean"):
    mod = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    src[mod] = p.read_text(errors="ignore").splitlines()

bymod = collections.defaultdict(list)
for k, v in sp.items():
    bymod[v["mod"]].append((v["line"], v["end"], k, k in FULL))

live_mods = {v["mod"] for k, v in sp.items() if k in FULL}
dead = [k for k in sp if k not in FULL and sp[k]["mod"] in live_mods]
dead_short = {k: k.split(".")[-1] for k in dead}

tok = re.compile(r"[A-Za-z_][A-Za-z0-9_']*")
owner_hits = collections.defaultdict(set)
for m, rows in bymod.items():
    rows.sort()
    lines = src[m]
    starts = [r[0] for r in rows]
    import bisect
    for i, ln in enumerate(lines, 1):
        j = bisect.bisect_right(starts, i) - 1
        owner = rows[j][2] if j >= 0 and rows[j][1] >= i else None
        if owner is None or owner not in FULL:
            continue  # outside any span, or owned by a dead decl
        for t in tok.findall(ln):
            owner_hits[t].add(owner)

safe, review = [], []
for k in dead:
    hits = owner_hits.get(dead_short[k], set())
    if hits:
        review.append((k, sp[k]["lines"], sorted(hits)[:3]))
    else:
        safe.append((k, sp[k]["lines"]))
safe.sort(key=lambda x: -x[1])
review.sort(key=lambda x: -x[1])
print(f"dead decls in surviving modules: {len(dead)}  ({sum(sp[k]['lines'] for k in dead)} span lines)")
print(f"SAFE   (no occurrence inside any live declaration span): {len(safe)}, {sum(x[1] for x in safe)} lines")
print(f"REVIEW (mentioned inside a live declaration):           {len(review)}, {sum(x[1] for x in review)} lines")
print("\n-- REVIEW, largest first --")
for k, l, h in review:
    print(f"  {l:4d}  {k}   <- in {h}")
print("\n-- SAFE, largest first --")
for k, l in safe:
    print(f"  {l:4d}  {k}")
json.dump([k for k, _ in safe], open(REPO / ".ultramath/smwg224wy/m3/SAFE.json", "w"), indent=0)
json.dump([k for k, _, _ in review], open(REPO / ".ultramath/smwg224wy/m3/REVIEW.json", "w"), indent=0)
