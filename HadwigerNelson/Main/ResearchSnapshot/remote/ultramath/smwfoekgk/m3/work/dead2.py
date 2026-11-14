import os,re,collections,json
root='../../../lean/OAI'
files={}
for dp,dn,fn in os.walk(root):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p]=open(p).read()
text='\n'.join(files.values())
tokens=collections.Counter(re.findall(r'[A-Za-z_][A-Za-z0-9_\'!?]*',text))
decl=re.compile(r'^(?:@\[[^\n]*\]\s*)?((?:private |protected |noncomputable |partial |scoped )*)(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s({:]+)')
keep_always={'no_proper_five_coloring','no_proper_five_coloring_algebraic','no_proper_five_coloring_compl_null',
 'properColoring_seven','proper_iff_weak','chromaticNumber_bounds','algebraic_colorable_iff','not_proper_five_coloring_compl_null'}
recs=[]
for p,t in files.items():
    L=t.splitlines()
    idx=[(i,m.group(1),m.group(2),m.group(3)) for i,l in enumerate(L) for m in [decl.match(l)] if m]
    for k,(i,mods,kind,name) in enumerate(idx):
        end=idx[k+1][0] if k+1<len(idx) else len(L)
        recs.append(dict(name=name,kind=kind,attrs=mods.strip(),file=p,line=i+1,n=end-i,
                         prev=L[i-1] if i else ''))
byname=collections.defaultdict(list)
for r in recs: byname[r['name']].append(r)
dead=[]
for name,rs in byname.items():
    if tokens[name]>len(rs): continue
    if len(rs)>1: continue          # duplicated names: skip (ambiguous)
    r=rs[0]
    if r['kind'] in ('instance','inductive','structure','class'): continue
    if 'simp' in r['attrs'] or 'ext' in r['attrs'] or 'norm_num' in r['attrs']: continue
    if r['attrs']: continue
    if name in keep_always: continue
    if r['prev'].strip().startswith(('variable','omit','include','@[')): continue
    dead.append(r)
dead.sort(key=lambda r:-r['n'])
print('safely-dead candidates:',len(dead),'lines',sum(r['n'] for r in dead))
per=collections.Counter()
for r in dead: per[r['file']]+=r['n']
for f,n in per.most_common(20): print(f'  {n:4d} lines {f[11:]}')
json.dump(dead,open('work/dead.json','w'),indent=0)
for r in dead[:25]: print(f"   {r['n']:4d} {r['file'][11:]}:{r['line']} {r['kind']} {r['name']}")
