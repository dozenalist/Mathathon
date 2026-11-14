#!/usr/bin/env python3
"""Marginal mass: for each module M, how many lines become unreachable from the
headline set if M is removed (and nothing else)?"""
import re, pathlib, sys, json, collections
ROOT=pathlib.Path(".")
IMP=re.compile(r"^import\s+([\w.]+)\s*$", re.M)
ms={}
for p in sorted((ROOT/"lean"/"OAI").rglob("*.lean")):
    name=".".join(p.relative_to(ROOT/"lean").with_suffix("").parts)
    txt=p.read_text(errors="ignore")
    ms[name]=dict(deps=[d for d in IMP.findall(txt) if d.startswith("OAI.")],
                  lines=txt.count("\n"))
HEADS=["OAI.Geometry.PlaneColoring.Five","OAI.Geometry.PlaneColoring.Seven",
       "OAI.Geometry.PlaneColoring.Transfer","OAI.Geometry.PlaneColoring.Chromatic",
       "OAI.Geometry.PlaneColoring.NullSetRobust"]
# reverse deps
rev=collections.defaultdict(set)
for m,v in ms.items():
    for d in v["deps"]:
        rev[d].add(m)
def reach(banned=set()):
    seen=set(); st=[h for h in HEADS if h not in banned]
    while st:
        n=st.pop()
        if n in seen or n in banned: continue
        seen.add(n); st.extend(ms[n]["deps"])
    return seen
base=reach()
tot=sum(ms[m]["lines"] for m in base)
print(f"baseline reach {len(base)} modules {tot} lines")
rows=[]
for m in sorted(ms):
    r=reach({m})
    lost=tot-sum(ms[k]["lines"] for k in r)
    # count of direct importers
    rows.append((lost, ms[m]["lines"], len(rev[m]), m, len(set(base)-r)))
rows.sort(reverse=True)
print(f"{'lost':>6} {'lines':>6} {'imp':>4} {'#unreach':>8} module")
for lost,lines,nimp,m,nun in rows:
    if lost>0: print(f"{lost:6d} {lines:6d} {nimp:4d} {nun:8d} {m}")
print("--- modules with lost==0 (no private cone):", sum(1 for r in rows if r[0]==0))
