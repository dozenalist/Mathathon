import json, pathlib, collections, sys, re

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
drop = json.load(open(REPO / ".ultramath/smwfoekgk/m12/drop.json"))
blocks = json.load(open("ana/blocks3.json"))
mine = json.load(open("ana/dead3.json"))

idx = collections.defaultdict(list)
for b in blocks:
    idx[(b["mod"], b["short"])].append(b)
    idx[(b["mod"], b["full"])].append(b)

# ---- map m12 decls to my precise blocks
chosen = {}
for d in drop:
    cands = idx.get((d["mod"], d["name"]))
    if not cands:
        tail = d["name"].split(".")[-1]
        cands = [b for b in blocks if b["mod"] == d["mod"] and b["short"] == tail]
    if not cands:
        print("UNMATCHED", d["mod"], d["name"])
        continue
    b = min(cands, key=lambda b: abs(b["start"] - (d["start"] - 1)))
    chosen[(b["mod"], b["start"])] = b
for i in mine:
    b = blocks[i]
    chosen.setdefault((b["mod"], b["start"]), b)

allb = list(chosen.values())
# restore set: list of [mod, start]
restore = []
rp = pathlib.Path("ana/restore.json")
if rp.exists():
    restore = json.load(open(rp))
# pre-restore the dotted-name decls (m12's byname keying bug: unqualified sibling refs missed)
for d in drop:
    if "." in d["name"]:
        for b in allb:
            if b["mod"] == d["mod"] and b["short"] == d["name"].split(".")[-1]:
                restore.append([b["mod"], b["start"]])
# force-restore anything named on the command line, as mod:short
for a in sys.argv[1:]:
    m, s = a.rsplit(":", 1)
    for b in allb:
        if b["mod"] == m and (s == "__ALL__" or b["short"] == s):
            restore.append([b["mod"], b["start"]])
rest = set(map(tuple, restore))
# also always keep my protected API
PROT = {"no_proper_five_coloring", "no_proper_five_coloring_algebraic", "properColoring_seven",
        "chromaticNumber_bounds", "proper_iff_weak", "algebraic_colorable_iff",
        "not_proper_five_coloring_compl_null", "six_le_planeChromaticNumber",
        "planeChromaticNumber_le_seven", "not_properColoring_five", "not_properColoring_of_le",
        "planeProperColoring_iff", "properColoring_of_plane", "plane_of_properColoring",
        "properColoring_mono", "toPlane", "ofPlane", "finite_config_proper",
        "exists_properColoring_of_finset", "properColoring_of_weak",
        "diam_le_one_of_preconnected_unitFree", "not_straddle_of_isPreconnected",
        "proper_to_borel_weak_algebraic"}
final = [b for b in allb if (b["mod"], b["start"]) not in rest and b["short"] not in PROT]
print("delete %d decls, precise lines %d ; restored %d" % (
    len(final), sum(b["end"] - b["start"] + 1 for b in final), len(rest)))
json.dump(sorted([b["mod"], b["start"]] for b in final), open("ana/final_drop.json", "w"))
json.dump(sorted(rest), open("ana/restore.json", "w"))

work = pathlib.Path("work4")
import shutil
if work.exists():
    shutil.rmtree(work)
shutil.copytree("tree", work)
per = collections.defaultdict(list)
for b in final:
    per[b["file"]].append(b)
tot = 0
for f, bs in per.items():
    L = pathlib.Path("tree", f).read_text().splitlines()
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
open("touched4.txt", "w").write("\n".join(mods) + "\n")
print("modules", len(mods), "raw lines removed", tot)
