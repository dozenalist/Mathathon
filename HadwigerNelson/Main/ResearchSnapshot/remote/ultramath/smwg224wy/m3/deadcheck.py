#!/usr/bin/env python3
"""Textual cross-check of the 'dead declaration' set.

A declaration is dead if it is not reachable in m10's DECLGRAPH.log closure AND its
short name does not occur textually anywhere in the staged tree outside its own
declaration.  Anything that fails the textual test is reported for manual review.
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


def closure(drop_v=(), keep=()):
    d, seen, st = set(drop_v), set(), list(ROOTS) + list(keep)
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

text = {}
for p in (ROOT / "OAI").rglob("*.lean"):
    mod = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    text[mod] = p.read_text(errors="ignore").splitlines()

live_mods = {sp[n]["mod"] for n in FULL if n in sp}
dead = [k for k in sp if k not in FULL and sp[k]["mod"] in live_mods]
print(f"dead decls with spans in surviving modules: {len(dead)}")

WORDFREE = re.compile(r"[A-Za-z0-9_]")
suspicious, clean, nlines = [], [], 0
for k in dead:
    s = sp[k]
    short = k.split(".")[-1]
    nlines += s["lines"]
    hits = 0
    for m, src in text.items():
        for i, ln in enumerate(src, 1):
            if not ln.lstrip().startswith(("--", "/-", "*")):
                if re.search(r"(?<![A-Za-z0-9_.'])" + re.escape(short) + r"(?![A-Za-z0-9_'])", ln):
                    hits += 1
                    # the declaration's own start line is one legitimate hit
    own = 1
    if hits > own:
        suspicious.append((k, s["lines"], hits))
    else:
        clean.append((k, s["lines"], hits))

print(f"span lines: {nlines}")
print(f"textually unreferenced (only own decl): {len(clean)}, {sum(x[1] for x in clean)} lines")
print(f"needs review: {len(suspicious)}, {sum(x[1] for x in suspicious)} lines")
for k, l, h in sorted(suspicious, key=lambda x: -x[1])[:40]:
    print(f"  {l:4d} hits={h:<3d} {k}")
