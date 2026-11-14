import re, pathlib, collections
ROOT = pathlib.Path("lean")
mods = {}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    deps = [m.group(1) for line in p.read_text(errors="ignore").splitlines()
            if (m := re.match(r"^import\s+(OAI\.[\w.]+)\s*$", line))]
    mods[name] = (p, [d for d in deps if d in mods or (ROOT / (d.replace(".", "/") + ".lean")).exists()])
lines = {n: len(p.read_text(errors="ignore").splitlines()) for n, (p, d) in mods.items()}
rev = collections.defaultdict(set)
for n, (p, ds) in mods.items():
    for d in ds: rev[d].add(n)
def reach(start):
    seen, st = set(), [start]
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x)
        st.extend(mods.get(x, (None, []))[1])
    return seen
import sys
target = sys.argv[1] if len(sys.argv) > 1 else "OAI.Geometry.PlaneColoring.Five"
R = reach(target)
print(f"modules: {len(mods)}  total lines: {sum(lines.values())}")
print(f"closure of {target}: {len(R)} modules, {sum(lines[m] for m in R)} lines")
un = [m for m in mods if m not in R]
print(f"NOT in closure: {len(un)} modules, {sum(lines[m] for m in un)} lines")
for m in sorted(un, key=lambda x: -lines[x])[:15]: print("   ", lines[m], m)
# roots (no importers)
roots = [m for m in mods if not rev[m]]
print("roots:", [(lines[m], m) for m in sorted(roots, key=lambda x: -lines[x])])
