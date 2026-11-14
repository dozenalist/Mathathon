import json, pathlib, collections, sys

blocks = json.load(open("ana/blocks3.json"))
dead = json.load(open("ana/dead3.json"))
texts = {}
for b in blocks:
    f = b["file"]
    if f not in texts:
        texts[f] = pathlib.Path("tree", f).read_text().splitlines()
per = collections.defaultdict(list)
for i in dead:
    per[blocks[i]["file"]].append(blocks[i])
tot = 0
for f, bs in per.items():
    L = list(texts[f])
    drop = set()
    for b in bs:
        s, e = b["start"], b["end"]
        while e + 1 < len(L) and L[e + 1].strip() == "":
            e += 1
        for j in range(s, e + 1):
            drop.add(j)
        tot += e - s + 1
    pathlib.Path("work2", f).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path("work2", f).write_text("\n".join(L[j] for j in range(len(L)) if j not in drop) + "\n")
print("dead: files %d lines %d" % (len(per), tot))

# ---- Energy.lean: replace the MovingMean cube-mean section by the InvariantMean mean
OLD_START = "variable (b : Finset G × ℕ → G)\ndef approxAt"
OLD_END = "  invariant g f := mean_shift b g f\nend\n"
p = pathlib.Path("work2/OAI/Analysis/PlaneSpectrum/Energy.lean")
t = p.read_text()
i = t.find(OLD_START)
j = t.find(OLD_END)
if i < 0 or j < 0:
    print("ENERGY PATTERN NOT FOUND (dead-decl edit may have moved it)", file=sys.stderr)
    sys.exit(1)
NEW = """/-- Both consumers (`RadialEnergy` and `Ergodicity`) use only the
`Amenable.Mean` fields, so the multiplicity-preserving cube average of this file is
not needed here: the invariant mean of `PlaneFiveColor.InvariantMean` supplies them. -/
def toMean (_ : Finset G × ℕ → G) : Amenable.Mean G where
  map := meanCLM
  map_const := mean_const
  positive := mean_nonneg
  invariant g f := mean_shift g f
end
"""
t = t[:i] + NEW + t[j + len(OLD_END):]
p.write_text(t)
print("energy dedup applied")
