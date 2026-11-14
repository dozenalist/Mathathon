import re, pathlib, collections
ROOT = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean")
mods={}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name=".".join(p.relative_to(ROOT).with_suffix("").parts)
    deps=[m.group(1) for m in re.finditer(r"^import\s+(OAI\.[\w.]+)\s*$",p.read_text(errors="ignore"),re.M)]
    mods[name]=(p,deps)
CF={n for n in mods if ".CompactFactors." in n or n.endswith("CompactFactors")}
PS={n for n in mods if ".PlaneSpectrum." in n}
for fam,label in ((CF,"CompactFactors"),(PS,"PlaneSpectrum")):
    print("==",label)
    for n in sorted(fam):
        users=[m for m,(p,d) in mods.items() if n in d]
        print(f"  {n.split('.',1)[1]:55s} <- {[u.split('.')[-1] for u in users]}")
