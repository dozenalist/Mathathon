import re, pathlib, collections
ROOT = pathlib.Path("lean")
mods, lines = {}, {}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    n = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    mods[n] = [m.group(1) for l in p.read_text(errors="ignore").splitlines()
               if (m := re.match(r"^import\s+(OAI\.[\w.]+)\s*$", l))]
    lines[n] = len(p.read_text(errors="ignore").splitlines())
rev = collections.defaultdict(set)
for n, ds in mods.items():
    for d in ds: rev[d].add(n)
sh = lambda m: m.replace("OAI.MeasureTheory.CompactFactors.","CF/").replace("OAI.Analysis.PlaneSpectrum.","PS/").replace("OAI.Geometry.PlaneColoring.","PC/")
print("module: lines, direct importers")
for m in sorted(mods, key=lambda x: -lines[x]):
    if lines[m] < 150: continue
    print(f"{lines[m]:5d} {sh(m):32s} <- {', '.join(sorted(sh(x) for x in rev[m]))}")
