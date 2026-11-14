import json, pathlib, collections, shutil, sys

M9 = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m9")
blocks = json.load(open(M9 / "ana/blocks3.json"))
info = {(b["mod"], b["start"]): b for b in blocks}
union = set(tuple(x) for x in json.load(open(M9 / "ana/union_drop.json")))
rest = M9 / "ana/restore5.json"
restored = set(tuple(x) for x in json.load(open(rest))) if rest.exists() else set()
PROT = {"no_proper_five_coloring", "no_proper_five_coloring_algebraic", "properColoring_seven",
        "chromaticNumber_bounds", "proper_iff_weak", "algebraic_colorable_iff",
        "not_proper_five_coloring_compl_null", "six_le_planeChromaticNumber",
        "planeChromaticNumber_le_seven", "not_properColoring_five", "not_properColoring_of_le",
        "planeProperColoring_iff", "properColoring_of_plane", "plane_of_properColoring",
        "properColoring_mono", "toPlane", "ofPlane", "finite_config_proper",
        "exists_properColoring_of_finset", "properColoring_of_weak",
        "diam_le_one_of_preconnected_unitFree", "not_straddle_of_isPreconnected",
        "proper_to_borel_weak_algebraic"}
final = [info[k] for k in union
         if k not in restored and info[k]["short"] not in PROT and info[k]["kind"] != "instance"]
print("delete %d decls, %d precise lines" % (len(final), sum(b["end"] - b["start"] + 1 for b in final)))
work = M9 / "work5"
if work.exists():
    shutil.rmtree(work)
shutil.copytree(M9 / "tree", work)
per = collections.defaultdict(list)
for b in final:
    per[b["file"]].append(b)
tot = 0
for f, bs in per.items():
    L = pathlib.Path(M9 / "tree", f).read_text().splitlines()
    di = set()
    for b in bs:
        s, e = b["start"], b["end"]
        while e + 1 < len(L) and L[e + 1].strip() == "":
            e += 1
        for j in range(s, e + 1):
            di.add(j)
        tot += e - s + 1
    pathlib.Path(work, f).write_text("\n".join(L[j] for j in range(len(L)) if j not in di) + "\n")
mods = sorted(set(b["mod"] for b in final))
(M9 / "touched5.txt").write_text("\n".join(mods) + "\n")
print("modules", len(mods), "raw removed", tot)
