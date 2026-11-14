import json, re, pathlib, collections
ROOT = pathlib.Path("lean/OAI")
text = {}
for p in ROOT.rglob("*.lean"):
    text[p] = p.read_text(errors="ignore").splitlines()
mod = {p: ".".join(p.relative_to(ROOT).with_suffix("").parts) for p in text}
decls = json.load(open(".ultramath/smwfoekgk/m13/decls.json"))
# index: name -> list of (path, lineidx)
occ = collections.defaultdict(list)
pat_cache = {}
for p, lines in text.items():
    for i, l in enumerate(lines):
        for tok in re.findall(r"[A-Za-z_][\w'.]*", l):
            occ[tok].append((p, i))
attr_above = {}
for d in decls:
    p = ROOT / (d["mod"].removeprefix("OAI.").replace(".", "/") + ".lean")
    lines = text[p]
    j = d["line"] - 2
    a = ""
    while j >= 0 and (lines[j].strip().startswith("@[") or lines[j].strip().startswith("attribute") or lines[j].strip()=="") and j > d["line"]-6:
        if lines[j].strip().startswith("@"): a = lines[j].strip()
        j -= 1
    attr_above[(d["mod"], d["line"])] = a
cand = []
for d in decls:
    if d["kind"] not in ("theorem", "lemma"): continue
    if attr_above[(d["mod"], d["line"])]: continue
    p = ROOT / (d["mod"].removeprefix("OAI.").replace(".", "/") + ".lean")
    lo, hi = d["line"] - 1, d["line"] - 1 + d["len"]
    name = d["name"]
    uses = 0
    for (q, i) in occ.get(name, ()):
        if q == p and lo <= i < hi: continue          # its own declaration
        # allow the binder occurrences of its own name in its own statement? no
        uses += 1
    if uses == 0: cand.append((d, p))
tot = sum(d["len"] for d, _ in cand)
print(f"truly unreferenced theorem/lemma declarations (no name occurrence anywhere else, no attribute): {len(cand)} decls, {tot} lines")
per = collections.Counter()
for d, _ in cand: per[d["mod"].split('.')[-1]] += d["len"]
for m, s in per.most_common(15): print(f"   {s:4d} {m}")
print("\nsample:")
for d, _ in sorted(cand, key=lambda x: -x[0]["len"])[:10]:
    print(f'   {d["len"]:4d} {d["mod"].split(".")[-1]}:{d["line"]} {d["name"]}')
