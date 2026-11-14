import os,re,collections
root='../../../lean/OAI'
mods={}
for dp,dn,fn in os.walk(root):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); m='OAI.'+os.path.relpath(p,root)[:-5].replace('/','.')
            mods[m]=(p,open(p).read())
depp=re.compile(r'^import\s+(OAI\.[\w.]+)',re.M)
g={m:[d for d in depp.findall(t)] for m,(p,t) in mods.items()}
lines={m:len(t.splitlines()) for m,(p,t) in mods.items()}
def cl(starts,skip=frozenset()):
    seen=set(); stack=list(starts)
    while stack:
        m=stack.pop()
        if m in seen or m in skip: continue
        seen.add(m); stack.extend(g.get(m,[]))
    return seen
head=['OAI.Geometry.PlaneColoring.Five']
D={'OAI.MeasureTheory.CompactFactors.'+x for x in ['Stationary','Approximation','ConditionalLimits','RelativeCenters']}
base=cl(head); after=cl(head,skip=D)
gone=base-after
print('D total lines',sum(lines[m] for m in D))
print('unreachable after deleting D:',len(gone),'modules,',sum(lines[m] for m in gone),'lines')
for m in sorted(gone,key=lambda m:-lines[m]): print(f'   {lines[m]:5d} {m[4:]}')
