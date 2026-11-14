import json, re, pathlib, collections
ROOT = pathlib.Path("lean/OAI")
tok = re.compile(r"[A-Za-z_][\w']*(?:\.[A-Za-z_][\w']*)*")
decls = json.load(open(".ultramath/smwfoekgk/m13/decls.json"))
per_file = {}          # path -> {name: count} for every dot-component
per_block = {}         # (mod,line) -> {name: count}
for p in ROOT.rglob("*.lean"):
    lines = p.read_text(errors="ignore").splitlines()
    c = collections.Counter()
    for l in lines:
        for m in tok.finditer(l):
            for comp in m.group(0).split("."): c[comp] += 1
    per_file[p] = c
cand = []
for d in decls:
    if d["kind"] not in ("theorem", "lemma"): continue
    p = ROOT / (d["mod"].removeprefix("OAI.").replace(".", "/") + ".lean")
    lines = p.read_text(errors="ignore").splitlines()
    j = d["line"] - 2
    while j >= 0 and lines[j].strip() == "": j -= 1
    if j >= 0 and (lines[j].strip().startswith("@[") or lines[j].strip().startswith("attribute ")): continue
    own = collections.Counter()
    for l in lines[d["line"]-1 : d["line"]-1+d["len"]]:
        for m in tok.finditer(l):
            for comp in m.group(0).split("."): own[comp] += 1
    total = 0
    for q, c in per_file.items():
        total += c.get(d["name"], 0)
    total -= own.get(d["name"], 0)
    if total <= 0: cand.append(d)
tot = sum(d["len"] for d in cand)
print(f"safe candidates: {len(cand)} decls, {tot} lines")
per = collections.Counter()
for d in cand: per[d["mod"].split(".")[-1]] += d["len"]
for m, s in per.most_common(12): print(f"   {s:4d} {m}")
print("largest:")
for d in sorted(cand, key=lambda x: -x["len"])[:8]:
    print(f'   {d["len"]:4d} {d["mod"].split(".")[-1]}:{d["line"]} {d["name"]}')
