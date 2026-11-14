import os,re,collections
root='../../../lean/OAI'
mods={}
for dp,dn,fn in os.walk(root):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); m='OAI.'+os.path.relpath(p,root)[:-5].replace('/','.')
            mods[m]=open(p).read()
lines={m:len(t.splitlines()) for m,t in mods.items()}
depp=re.compile(r'^import\s+(OAI\.[\w.]+)',re.M)
g={m:depp.findall(t) for m,t in mods.items()}
decl=re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |partial |scoped )*(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s({:]+)',re.M)
names=collections.defaultdict(set)
for m,t in mods.items():
    for mm in decl.finditer(t): names[mm.group(2)].add(m)
uniq={k:next(iter(v)) for k,v in names.items() if len(v)==1}
cluster=[m for m in mods if m.split('.')[-1] in
  {'Kernels','Functions','BoundedFunctions','Factors','Centers','RelativeCenters','Approximation',
   'ConditionalLimits','ConditionalSelection','ConditionalSpectrum','FourierTests','Multipliers',
   'SmallArcs','PhaseEncoding','PhaseCollision','Characters','Stationary','AlgebraModels','Separability','RelativeProducts'}]
cluster=set(cluster)
rest=[m for m in mods if m not in cluster]
print('cluster modules',len(cluster),'lines',sum(lines[m] for m in cluster))
use=collections.defaultdict(lambda: collections.Counter())
for m in rest:
    for tok in re.findall(r'[A-Za-z_][A-Za-z0-9_\'!?]*',mods[m]):
        if tok in uniq and uniq[tok] in cluster:
            use[uniq[tok]][(tok,m)]+=1
print('cluster decls referenced from outside:',sum(len(v) for v in use.values()))
for m in sorted(use,key=lambda m:-len(use[m])):
    print(f'--- {lines[m]:4d} {m[4:]}  ({len(use[m])} names used outside)')
    for (tok,frm),c in sorted(use[m].items(),key=lambda kv:-kv[1])[:14]:
        print(f'      {tok:42s} <- {frm.split(".")[-1]}')
