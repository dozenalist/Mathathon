import json, pathlib, collections, sys

M12 = "/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m12/drop.json"
drop = json.load(open(M12))
blocks = json.load(open("ana/blocks3.json"))
idx = collections.defaultdict(list)
for b in blocks:
    idx[(b["mod"], b["short"])].append(b)
    idx[(b["mod"], b["full"])].append(b)

chosen = {}
unmatched = []
for d in drop:
    key = (d["mod"], d["name"])
    cands = idx.get(key)
    if not cands:
        tail = d["name"].split(".")[-1]
        cands = [b for b in blocks if b["mod"] == d["mod"] and b["short"] == tail]
    if not cands:
        unmatched.append(d)
        continue
    b = min(cands, key=lambda b: abs(b["start"] - (d["start"] - 1)))
    chosen[b["start"], b["mod"]] = b
print("matched %d unmatched %d" % (len(chosen), len(unmatched)))
for d in unmatched:
    print("  UNMATCHED", d["mod"], d["name"], d["kind"])
lines = sum(b["end"] - b["start"] + 1 for b in chosen.values())
print("precise extent lines", lines)

per = collections.defaultdict(list)
for b in chosen.values():
    per[b["file"]].append(b)
tot = 0
for f, bs in per.items():
    L = pathlib.Path("tree", f).read_text().splitlines()
    dropi = set()
    for b in bs:
        s, e = b["start"], b["end"]
        while e + 1 < len(L) and L[e + 1].strip() == "":
            e += 1
        for j in range(s, e + 1):
            dropi.add(j)
        tot += e - s + 1
    pathlib.Path("work3", f).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path("work3", f).write_text("\n".join(L[j] for j in range(len(L)) if j not in dropi) + "\n")
print("files %d lines removed %d" % (len(per), tot))
mods = sorted(set(b["mod"] for b in chosen.values()))
open("touched3.txt", "w").write("\n".join(mods) + "\n")
print("modules touched", len(mods))
json.dump(sorted(set(b["short"] for b in chosen.values())), open("ana/drop3_names.json", "w"))
