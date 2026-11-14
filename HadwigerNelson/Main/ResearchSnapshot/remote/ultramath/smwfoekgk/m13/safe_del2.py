import json, re, pathlib, collections
ROOT = pathlib.Path("lean/OAI")
text = {p: p.read_text(errors="ignore").splitlines() for p in ROOT.rglob("*.lean")}
decls = json.load(open(".ultramath/smwfoekgk/m13/decls.json"))
blob = {p: "\n".join(ls) for p, ls in text.items()}
def attr_before(lines, idx):
    j = idx - 1
    while j >= 0 and lines[j].strip() == "": j -= 1
    return lines[j].strip().startswith("@[") or lines[j].strip().startswith("attribute ") if j >= 0 else False
cand = []
for d in decls:
    if d["kind"] not in ("theorem","lemma"): continue
    p = ROOT / (d["mod"].removeprefix("OAI.").replace(".", "/") + ".lean")
    lines = text[p]
    if attr_before(lines, d["line"]-1): continue
    name = d["name"]
    rx = re.compile(r"(?<![\w'])" + re.escape(name) + r"(?![\w'])")
    lo, hi = d["line"]-1, d["line"]-1+d["len"]
    own = lines[lo:hi]
    uses = 0
    for q, txt in blob.items():
        hits = len(rx.findall(txt))
        if q == p:
            hits -= len(rx.findall("\n".join(own)))   # subtract its own declaration block
        uses += hits
    if uses <= 0: cand.append(d)
tot = sum(d["len"] for d in cand)
print(f"safe candidates: {len(cand)} decls, {tot} lines")
per = collections.Counter()
for d in cand: per[d["mod"].split(".")[-1]] += d["len"]
for m, s in per.most_common(12): print(f"   {s:4d} {m}")
print("largest:")
for d in sorted(cand, key=lambda x:-x["len"])[:8]:
    print(f'   {d["len"]:4d} {d["mod"].split(".")[-1]}:{d["line"]} {d["name"]}')
