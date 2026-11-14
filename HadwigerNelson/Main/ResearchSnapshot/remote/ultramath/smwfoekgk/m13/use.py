import re, pathlib, collections, sys, json
ROOT = pathlib.Path("lean/OAI")
files = {p: p.read_text(errors="ignore") for p in ROOT.rglob("*.lean")}
mod = {p: ".".join(p.relative_to(ROOT).with_suffix("").parts) for p in files}
decls = json.load(open(".ultramath/smwfoekgk/m13/decls.json"))
sys.path.insert(0,'.')
def consumers(name, home):
    out = set()
    pat = re.compile(r"(?<![\w.'])" + re.escape(name) + r"(?![\w'])")
    for p, t in files.items():
        if mod[p] == home: continue
        if pat.search(t): out.add(mod[p].split(".")[-1])
    return out
target = sys.argv[1]
ds = [x for x in decls if x["mod"].endswith("."+target)]
for x in ds:
    c = consumers(x["name"], x["mod"])
    print(f'{x["len"]:4d} {x["name"]:45s} -> {len(c):2d} ext ' + (", ".join(sorted(c))[:90]))
