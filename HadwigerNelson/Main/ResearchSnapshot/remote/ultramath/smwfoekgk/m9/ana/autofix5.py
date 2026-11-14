import json, re, pathlib, collections, sys
M9 = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m9")
blocks = json.load(open(M9/"ana/blocks3.json"))
info = {(b["mod"], b["start"]): b for b in blocks}
union = set(tuple(x) for x in json.load(open(M9/"ana/union_drop.json")))
rest = M9/"ana/restore5.json"
restored = set(tuple(x) for x in json.load(open(rest))) if rest.exists() else set()
cand = [info[k] for k in union if k not in restored]
bymod = collections.defaultdict(list)
for b in cand: bymod[b["mod"]].append(b)
NAMEPAT=[r"Unknown identifier `([^`]+)`", r"Unknown constant `([^`]+)`",
         r"does not contain `([^`]+)`", r"project the field `([^`]+)`",
         r"failed to synthesize instance of type class\s*\n\s*([^\n]+)"]
added=[]
for lg in sorted(pathlib.Path("/tmp").glob("w_OAI*.log")):
    mod = lg.stem[2:].replace("_",".")
    t = lg.read_text(errors="ignore")
    errs=[l for l in t.splitlines() if "error" in l]
    if not errs: continue
    if all("object file" in l for l in errs): continue
    names=set()
    for p in NAMEPAT:
        for m in re.finditer(p,t): names.add(m.group(1).strip().split(".")[-1])
    fixed=False
    for b in bymod.get(mod,[]):
        if b["short"] in names:
            restored.add((b["mod"],b["start"])); added.append(b["full"]); fixed=True
    if not fixed:
        hard=[b for b in bymod.get(mod,[]) if b["attr"] or b["kind"]=="def"]
        for b in hard:
            restored.add((b["mod"],b["start"])); added.append("SOFT "+b["full"])
json.dump(sorted(restored),open(rest,"w"))
print("restored now:",len(restored),"added this round:",len(added))
for a in added[:40]: print("   +",a)
