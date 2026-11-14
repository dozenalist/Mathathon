import json, re, sys, pathlib, collections

M9 = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m9")
blocks = json.load(open(M9 / "ana/blocks3.json"))
final = json.load(open(M9 / "ana/final_drop.json"))
info = {(b["mod"], b["start"]): b for b in blocks}
dropped = [info[(m, s)] for m, s in final]
bymod = collections.defaultdict(list)
for b in dropped:
    bymod[b["mod"]].append(b)
restore = set(tuple(x) for x in json.load(open(M9 / "ana/restore.json")))

NAMEPAT = [r"Unknown identifier `([^`]+)`", r"Unknown constant `([^`]+)`",
           r"does not contain `([^`]+)`", r"project the field `([^`]+)`"]
logs = sorted(pathlib.Path("/tmp").glob("w_OAI*.log"))
added = collections.Counter()
for lg in logs:
    mod = lg.stem[2:].replace("_", ".")
    t = lg.read_text(errors="ignore")
    errs = [l for l in t.splitlines() if "error" in l]
    if not errs:
        continue
    if all("object file" in l for l in errs):
        continue
    names = set()
    for p in NAMEPAT:
        for m in re.finditer(p, t):
            names.add(m.group(1).split(".")[-1])
    fixed = False
    for b in bymod.get(mod, []):
        if b["short"] in names:
            restore.add((b["mod"], b["start"]))
            added[b["short"]] += 1
            fixed = True
    if not fixed:
        # unsolved goals / synthInstance: restore attributed or def decls in this module
        soft = [b for b in bymod.get(mod, []) if b["attr"] or b["kind"] == "def"]
        for b in soft:
            restore.add((b["mod"], b["start"]))
            added["SOFT:" + mod.split(".")[-1] + ":" + b["short"]] += 1
json.dump(sorted(restore), open(M9 / "ana/restore.json", "w"))
print("total restores", len(restore))
for k, v in added.items():
    print("  +", k)
# rebuild work4
import subprocess
subprocess.run([sys.executable, str(M9 / "ana/repair.py")], cwd=str(M9), check=True)
