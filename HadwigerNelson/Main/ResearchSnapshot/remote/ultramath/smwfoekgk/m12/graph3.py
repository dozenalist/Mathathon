import os
root='OAI'
mods={}
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); m=p[:-5].replace('/','.')
            src=open(p).read()
            deps={l.strip()[7:].strip() for l in src.splitlines() if l.strip().startswith('import ')}
            mods[m]=(deps,src.count('\n'),p)
def closure(starts, banned=()):
    seen=set(starts); st=list(starts)
    while st:
        m=st.pop()
        for d in mods[m][0]:
            if d in mods and d not in seen and d not in banned:
                seen.add(d); st.append(d)
    return seen
roots=['OAI.Geometry.PlaneColoring.Chromatic','OAI.Geometry.PlaneColoring.ConnectedUnitFree','OAI.Geometry.PlaneColoring.NullSetRobust','OAI.Geometry.PlaneColoring.Transfer']
allr=closure(roots)
print('all reachable',len(allr),sum(mods[m][1] for m in allr))
banned={'OAI.MeasureTheory.CompactFactors.Approximation'}
# also need to ban Stationary (which imports Approximation) - simulate deleting the chain: remove modules that use it
import functools
def closure2(starts):
    seen=set(starts); st=list(starts); dead=set()
    changed=True
    # iterative: a module that imports a dead module cannot be built; mark it dead
    while changed:
        changed=False
        for m in mods:
            if m in seen or m in dead: continue
            # reachable if some importer gives... simpler: compute reachability from starts allowing only deps that are not dead
            pass
    return seen
# simpler: iteratively compute: dead = modules whose import requires a banned module
dead=set()
changed=True
while changed:
    changed=False
    for m,(deps,_,_) in mods.items():
        if m in dead: continue
        if any(d in banned or d in dead for d in deps if d in mods):
            dead.add(m); changed=True
live=set(mods)-dead
reach=closure(roots,banned=dead)
print('dead if Approximation removed:',len(dead),'lines',sum(mods[m][1] for m in dead))
for m in sorted(dead,key=lambda m:-mods[m][1]): print('   ',mods[m][1],m)
