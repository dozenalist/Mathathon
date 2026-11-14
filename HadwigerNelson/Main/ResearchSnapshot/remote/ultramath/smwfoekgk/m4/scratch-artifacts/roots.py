import os,re,collections
root='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean'
mods={}
for dp,dn,fn in os.walk(os.path.join(root,'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m='OAI.'+os.path.relpath(p,os.path.join(root,'OAI'))[:-5].replace('/','.')
            src=open(p).read()
            mods[m]=dict(lines=len(src.splitlines()),imports=re.findall(r'^import\s+(\S+)',src,re.M),path=p)
short=lambda m:m.replace('OAI.','')
# every module is potentially a root; compute, for each module, which *leaves-ward* path
# Better: for each module, the set of modules that depend on it (transitively) = users*
def dependents(m):
    out=set(); 
    # reverse closure: modules importing m directly
    users=collections.defaultdict(set)
    for x,d in mods.items():
        for i in d['imports']: users[i].add(x)
    stack=[m]
    while stack:
        y=stack.pop()
        for u in users[y]:
            if u not in out: out.add(u); stack.append(u)
    return out
# key question: for each module, is it reachable from Stationary? from Ergodicity without Stationary?
def clos(m,exclude=frozenset()):
    seen=set(); stack=[m]
    while stack:
        y=stack.pop()
        if y in seen or y in exclude or y not in mods: continue
        seen.add(y); stack.extend(mods[y]['imports'])
    return seen
stat=clos('OAI.MeasureTheory.CompactFactors.Stationary')
# modules reachable from Ergodicity but not through Stationary
ergo=clos('OAI.Analysis.PlaneSpectrum.Ergodicity')
print('Stationary closure', len(stat), sum(mods[x]['lines'] for x in stat))
print('Ergodicity closure', len(ergo), sum(mods[x]['lines'] for x in ergo))
onlystat=sorted(stat, key=lambda m:mods[m]['path'])
print('\n-- modules in Stationary closure (the terminal-factor branch):')
for m in onlystat: print(f"  {mods[m]['lines']:5d} {short(m)}")
