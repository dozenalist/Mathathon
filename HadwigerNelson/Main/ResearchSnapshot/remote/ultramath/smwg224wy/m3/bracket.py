#!/usr/bin/env python3
"""Bracket the freed-span figures with the attribute closure.

DECLGRAPH.log has no edges for global attribute sets, so a declaration can be
'outside the closure' and still be used by a live `simp`/instance search.  This
script (a) tags every declaration that carries an attribute or is an `instance`,
(b) recomputes a route's freed lines with all of those kept alive (lower bracket)
next to the raw figure (upper bracket).
"""
import collections
import json
import pathlib
import re
import sys

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

sp = json.loads((REPO / ".ultramath/smwg224wy/m3/SPANS_stage.json").read_text())
src = {}
for p in (ROOT / "OAI").rglob("*.lean"):
    mod = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    src[mod] = p.read_text(errors="ignore").splitlines()

INST = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)*(?:noncomputable\s+|private\s+|protected\s+)*"
                  r"(?:instance|scoped\s+instance)\b")
ATTR = re.compile(r"^\s*@\[")

globalish = set()   # declarations whose use can be implicit
for k, v in sp.items():
    lines = src[v["mod"]]
    first = lines[v["line"] - 1]
    prev = lines[v["line"] - 2] if v["line"] >= 2 else ""
    if INST.match(first) or ATTR.match(first) or (ATTR.match(prev) and first.lstrip().startswith(("theorem", "lemma", "def"))):
        globalish.add(k)
print(f"declarations with a global attribute or an instance: {len(globalish)}")


def freed(drop, keep=()):
    d, seen, st = set(drop), set(), list(ROOTS) + list(keep)
    while st:
        n = st.pop()
        if n in seen:
            continue
        seen.add(n)
        st.extend(et.get(n, ()))
        if n not in d:
            st.extend(ev.get(n, ()))
    full = seen
    d2, seen2, st = set(drop), set(), list(ROOTS) + list(keep)
    while st:
        n = st.pop()
        if n in seen2:
            continue
        seen2.add(n)
        st.extend(et.get(n, ()))
        if n not in d2:
            st.extend(ev.get(n, ()))
    return seen2


def lines_of(s):
    return sum(sp[n]["lines"] for n in s if n in sp)


base = set()
keep = []
argv = sys.argv[1:]
if "--keep" in argv:
    i = argv.index("--keep")
    keep = argv[i + 1:]
    argv = argv[:i]
base = set(argv)

full_all = freed(set(), ())
red_raw = freed(base, keep)
cand = full_all - red_raw
print(f"raw route: freed {len(cand)} decls / {lines_of(cand)} lines")
keep2 = list(keep) + sorted(cand & globalish)
red_safe = freed(base, keep2)
cand2 = full_all - red_safe
print(f"with the attribute/instance closure kept: freed {len(cand2)} decls / {lines_of(cand2)} lines")
print(f"  (kept back {len(cand & globalish)} attributed/instance decls, "
      f"{lines_of(cand & globalish)} lines)")
per = collections.Counter()
for n in cand2:
    if n in sp:
        per[sp[n]["mod"]] += sp[n]["lines"]
for m, l in per.most_common():
    print(f"{l:6d}  {m}")
json.dump(sorted(cand & globalish), open(REPO / ".ultramath/smwg224wy/m3/GLOBALISH.json", "w"), indent=0)
