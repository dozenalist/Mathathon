import re,pathlib,collections,json
ROOT=pathlib.Path("tree")
mods={}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    n=".".join(p.relative_to(ROOT).with_suffix("").parts)
    t=p.read_text(errors="ignore")
    deps=[m.group(1) for m in re.finditer(r"^import\s+(OAI\.[\w.]+)\s*$",t,re.M)]
    mods[n]=(p,deps,len(t.splitlines()))
# roots: headline theorems
roots=["OAI.Geometry.PlaneColoring.Five","OAI.Geometry.PlaneColoring.Chromatic","OAI.Geometry.PlaneColoring.NullSetRobust"]
seen=set()
def go(n):
    if n in seen: return
    seen.add(n)
    for d in mods[n][1]: go(d)
for r in roots: go(r)
unreach=[n for n in mods if n not in seen]
print("modules",len(mods),"reachable",len(seen),"unreachable",len(unreach))
print("unreachable lines",sum(mods[n][2] for n in unreach))
for n in sorted(unreach): print(" ",n,mods[n][2])
# who imports whom: print modules whose only importers are in set
imp=collections.defaultdict(list)
for n,(p,ds,l) in mods.items():
    for d in ds: imp[d].append(n)
print("\nleaf-only modules (imported by <=2):")
for n in sorted(mods):
    if len(imp[n])<=2: print(f"  {n} lines={mods[n][2]} importers={imp[n]}")
