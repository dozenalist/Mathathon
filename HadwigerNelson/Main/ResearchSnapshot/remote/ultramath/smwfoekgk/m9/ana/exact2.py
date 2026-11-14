import json, collections, pathlib

M9 = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m9")
decls = json.load(open(M9 / "ana/decls_ns.json"))
blocks = json.load(open(M9 / "ana/blocks3.json"))
deps = {}
for line in open(M9 / "ana/deps.txt"):
    line = line.rstrip("\n")
    if not line:
        continue
    n, _, rest = line.partition("\t")
    deps[n] = set(rest.split()) if rest else set()

byfull = {}
for d in decls:
    if d["full"]:
        byfull.setdefault(d["full"], d)

DELIV = {"OAI.Geometry.PlaneColoring.Chromatic", "OAI.Geometry.PlaneColoring.Seven",
         "OAI.Geometry.PlaneColoring.NullSetRobust", "OAI.Geometry.PlaneColoring.Transfer",
         "OAI.Geometry.PlaneColoring.Converse", "OAI.Geometry.PlaneColoring.ConnectedUnitFree",
         "OAI.Geometry.PlaneColoring.MeasurableProper", "OAI.Geometry.PlaneColoring.MeasurableAssembly",
         "OAI.Geometry.PlaneColoring.Metric", "OAI.Geometry.PlaneColoring.Lattice",
         "OAI.Geometry.PlaneColoring.Assembly", "OAI.Geometry.PlaneColoring.Basic",
         "OAI.Geometry.PlaneColoring.Covering"}
NAMED = {"no_proper_five_coloring", "no_proper_five_coloring_algebraic", "properColoring_seven",
         "chromaticNumber_bounds", "proper_iff_weak", "algebraic_colorable_iff",
         "not_proper_five_coloring_compl_null", "six_le_planeChromaticNumber",
         "planeChromaticNumber_le_seven", "not_properColoring_five", "not_properColoring_of_le",
         "planeProperColoring_iff", "properColoring_of_plane", "plane_of_properColoring",
         "properColoring_mono", "toPlane", "ofPlane", "finite_config_proper",
         "exists_existing", "exists_properColoring_of_finset", "properColoring_of_weak",
         "diam_le_one_of_preconnected_unitFree", "not_straddle_of_isPreconnected",
         "proper_to_borel_weak_algebraic", "planeProperColoring_iff"}

roots = set()
for d in decls:
    if d["mod"] in DELIV:
        if d["full"]:
            roots.add(d["full"])
    elif d["name"] in NAMED and d["full"]:
        roots.add(d["full"])
print("roots", len(roots))

keep = set(roots)
# force-keep all constants of these kinds / attributes
forced = set()
for d in decls:
    if d["full"] and (d["kind"] in ("instance", "structure", "class", "inductive", "abbrev")
                      or d["private"] or d["name"] is None):
        forced.add(d["full"])
keep |= forced
changed = True
while changed:
    changed = False
    for n in list(keep):
        for m in deps.get(n, ()):
            if m in byfull and m not in keep:
                keep.add(m)
                changed = True
dead = [d for d in decls if d["full"] and d["full"] in byfull and d["full"] not in keep]

# map to precise blocks
bymod = collections.defaultdict(list)
for b in blocks:
    bymod[b["mod"]].append(b)
tot = 0
chosen = []
for d in dead:
    cands = [b for b in bymod[d["mod"]] if b["short"] == d["full"].split(".")[-1]]
    if not cands:
        cands = [b for b in bymod[d["mod"]] if b["full"] == d["full"]]
    if not cands:
        continue
    b = min(cands, key=lambda b: abs(b["start"] + 1 - d["line"]))
    chosen.append(b)
    tot += b["end"] - b["start"] + 1
print("EXACT-GRAPH dead: %d decls, %d precise lines" % (len(chosen), tot))
print("kinds:", collections.Counter(b["kind"] for b in chosen))
per = collections.Counter()
for b in chosen:
    per[b["mod"].split(".")[-1]] += b["end"] - b["start"] + 1
print(per.most_common(20))
json.dump(sorted([[b["mod"], b["start"]] for b in chosen]), open(M9 / "ana/exact_drop.json", "w"))
