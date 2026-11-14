import re, pathlib, collections, sys
ROOT = pathlib.Path("lean")
mods, lines = {}, {}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    n = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    mods[n] = [m.group(1) for l in p.read_text(errors="ignore").splitlines()
               if (m := re.match(r"^import\s+(OAI\.[\w.]+)\s*$", l))]
    lines[n] = len(p.read_text(errors="ignore").splitlines())
ROOTS = ["OAI.Geometry.PlaneColoring.Five","OAI.Geometry.PlaneColoring.Chromatic",
         "OAI.Geometry.PlaneColoring.Seven","OAI.Geometry.PlaneColoring.Converse",
         "OAI.Geometry.PlaneColoring.NullSetRobust","OAI.Geometry.PlaneColoring.ConnectedUnitFree"]
def reach(dead):
    seen, st = set(), [r for r in ROOTS if r in mods]
    while st:
        x = st.pop()
        if x in seen or x in dead or x not in mods: continue
        seen.add(x); st.extend(mods[x])
    return seen
base = reach(set())
print(f"baseline reachable: {len(base)} modules, {sum(lines[m] for m in base)} lines")
CF = "OAI.MeasureTheory.CompactFactors."
PS = "OAI.Analysis.PlaneSpectrum."
for label, dead in [
    ("R11 (Approx+PhaseCollision+CondSpectrum+PhaseEncoding)", {CF+"Approximation", PS+"PhaseCollision", PS+"ConditionalSpectrum", PS+"PhaseEncoding"}),
    ("R11+CondSelection", {CF+"Approximation", PS+"PhaseCollision", PS+"ConditionalSpectrum", PS+"PhaseEncoding", CF+"ConditionalSelection"}),
    ("R11+CondSelection+CondLimits", {CF+"Approximation", PS+"PhaseCollision", PS+"ConditionalSpectrum", PS+"PhaseEncoding", CF+"ConditionalSelection", CF+"ConditionalLimits"}),
]:
    r = reach(dead)
    gone = sorted(base - r, key=lambda m: -lines[m])
    print(f"\n{label}: still reachable {len(r)} mods {sum(lines[m] for m in r)} lines; margin {sum(lines[m] for m in gone)} lines over {len(gone)} modules")
    for m in gone: print(f"    -{lines[m]:5d} {m}")
