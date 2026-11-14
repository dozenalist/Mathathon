#!/usr/bin/env python3
"""Conservative drop set: a declaration survives if it is in the proof-term closure of
the advertised surface OR is *mentioned by name* inside the source span of a surviving
declaration.  The second condition is what makes `simp [foo]`-style syntactic uses safe:
such a name is elaborated but may never appear in the proof term."""
import json, pathlib, collections, re, sys

H = pathlib.Path(__file__).resolve().parent
REPO = H.parent.parent.parent
sp = json.loads((H / "SPANS.json").read_text())
nodes, et, ev = {}, collections.defaultdict(set), collections.defaultdict(set)
for ln in (H / "DECLGRAPH.log").read_text().splitlines():
    ln = ln.strip()
    if ln.startswith("NODE "): _, m, n = ln.split(" ", 2); nodes[n] = m
    elif ln.startswith("EDGET "): _, x, y = ln.split(" ", 2); et[x].add(y)
    elif ln.startswith("EDGEV "): _, x, y = ln.split(" ", 2); ev[x].add(y)
ROOTS = ["OAI.EuclideanFiveColor.no_proper_five_coloring",
         "OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic",
         "OAI.Problem160.properColoring_seven",
         "OAI.EuclideanFiveColor.proper_iff_weak",
         "OAI.Problem160.chromaticNumber_bounds",
         "OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null",
         "OAI.EuclideanFiveColor.algebraic_colorable_iff"]
force = []
fp = H / "FORCE.txt"
if fp.exists():
    force = [l.strip() for l in fp.read_text().splitlines() if l.strip()]
by_short = collections.defaultdict(list)
for k in sp: by_short[k.split(".")[-1]].append(k)
extra = []
for w in force:
    e = [k for k in sp if k == w] or by_short.get(w.split(".")[-1], [])
    extra += [k for k in e if k not in ROOTS]
# span text of each declaration
text = {}
for p in sorted((REPO / "lean" / "OAI").rglob("*.lean")):
    mod = ".".join(p.relative_to(REPO / "lean").with_suffix("").parts)
    lines = p.read_text(errors="ignore").splitlines()
    for k, v in sp.items():
        if v["mod"] == mod:
            text[k] = "\n".join(lines[v["line"]-1:v["end"]])
        else: pass
kept = set(ROOTS) | set(extra)
for it in range(40):
    # semantic closure
    st, sem = list(kept), set()
    while st:
        n = st.pop()
        if n in sem: continue
        sem.add(n)
        st.extend(et.get(n, ())); st.extend(ev.get(n, ()))
    # textual mentions inside surviving spans
    add = set()
    for k in list(sem):
        if k not in text: continue
        words = set(re.findall(r"[A-Za-z_][A-Za-z0-9_']*", text[k]))
        for w in words:
            for cand in by_short.get(w, ()):
                if cand not in sem: add.add(cand)
    if not add: kept = sem; break
    kept = sem | add
    print(f"iter {it}: kept {len(kept)} (+{len(add)} textual)", file=sys.stderr)
drop = {k: v for k, v in sp.items() if k not in kept}
per = collections.Counter()
for k, v in drop.items(): per[v["mod"]] += v["lines"]
print(f"DECLARATIONS to drop: {len(drop)}  span lines {sum(v['lines'] for v in drop.values())}")
print(f"modules affected: {len(per)}")
for m, l in per.most_common(20): print(f"{l:5d} {m}")
json.dump(drop, open(H / "TEXDROP.json", "w"), indent=0)
