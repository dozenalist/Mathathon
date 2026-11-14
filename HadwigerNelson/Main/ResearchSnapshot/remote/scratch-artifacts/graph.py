import os,collections,sys
R='lean/OAI'
mods={}
for dp,dn,fn in os.walk(R):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            name=os.path.relpath(p,R)[:-5].replace('/','.')
            imp=[]
            for line in open(p):
                line=line.strip()
                if line.startswith('import '):
                    for t in line[7:].split():
                        if t.startswith('OAI.'): imp.append(t[4:])
            mods[name]=(p,imp,sum(1 for _ in open(p)))
deps={m:set(i) for m,(p,i,n) in mods.items()}
rev=collections.defaultdict(set)
for m,i in deps.items():
    for x in i: rev[x].add(m)
def reach(start, banned=frozenset()):
    seen=set(); st=[s for s in start]
    while st:
        x=st.pop()
        if x in seen or x in banned: continue
        seen.add(x); st.extend(deps.get(x,()))
    return seen
TOPMOD='Geometry.PlaneColoring.Five'
topdep=reach([TOPMOD])
print("modules reachable from Five:",len(topdep),"lines:",sum(mods[m][2] for m in topdep))
print("modules NOT reachable from Five:")
for m in sorted(set(mods)-topdep): print("   ",m,mods[m][2])
for target in sys.argv[1:]:
    rest=reach([TOPMOD],banned={target})
    excl=sorted(topdep-rest)
    print(f"\n== removing {target}: {len(excl)} modules become unreachable, {sum(mods[m][2] for m in excl)} lines")
    for m in excl: print("   ",m,mods[m][2])
