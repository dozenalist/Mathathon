import re, pathlib, collections
ROOT = pathlib.Path("lean")
mods, lines = {}, {}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    n = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    mods[n] = [m.group(1) for l in p.read_text(errors="ignore").splitlines()
               if (m := re.match(r"^import\s+(OAI\.[\w.]+)\s*$", l))]
    lines[n] = len(p.read_text(errors="ignore").splitlines())
def closure(seed):
    seen, st = set(), list(seed)
    while st:
        x = st.pop()
        if x in seen or x not in mods: continue
        seen.add(x); st.extend(mods[x])
    return seen
def revclosure(seed):
    # modules that (transitively) import seed
    rev = collections.defaultdict(set)
    for n, ds in mods.items():
        for d in ds: rev[d].add(n)
    seen, st = set(), list(seed)
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x); st.extend(rev[x])
    return seen
A = "OAI.MeasureTheory.CompactFactors.Approximation"
cl = closure([A]); outer = [m for m in mods if m.startswith("OAI.Analysis.PlaneSpectrum")]
print(f"closure of Approximation.lean: {len(cl)} modules, {sum(lines[m] for m in cl)} lines")
for m in sorted(cl, key=lambda m: -lines[m]):
    print(f"   {lines[m]:5d} {m.replace('OAI.MeasureTheory.CompactFactors.','CF/')}")
print()
for name in ["OAI.Analysis.PlaneSpectrum.PhaseCollision","OAI.Analysis.PlaneSpectrum.PhaseEncoding",
             "OAI.Analysis.PlaneSpectrum.ConditionalSpectrum","OAI.Analysis.PlaneSpectrum.Selections",
             "OAI.MeasureTheory.CompactFactors.ConditionalLimits","OAI.MeasureTheory.CompactFactors.Stationary"]:
    c = closure([name]); print(f"{name.split('.')[-1]:22s} closure {len(c):3d} mods {sum(lines[m] for m in c):6d} lines, importers {len(revclosure([name]))-1}")
