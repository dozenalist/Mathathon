import os,re,collections
decl=re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |partial )*(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s({:]+)')
files={}
for dp,dn,fn in os.walk('../../../lean/OAI'):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p]=open(p).read()
text='\n'.join(files.values())
tokens=collections.Counter(re.findall(r'[A-Za-z_][A-Za-z0-9_\'!?]*',text))
recs=[]
for p,t in files.items():
    L=t.splitlines()
    idx=[(i,m.group(1),m.group(2)) for i,l in enumerate(L) for m in [decl.match(l)] if m]
    for k,(i,kind,name) in enumerate(idx):
        end=idx[k+1][0] if k+1<len(idx) else len(L)
        recs.append((name,kind,p,i+1,end-i))
# a declaration's name appears once at its def + once per use (roughly); names may clash across files
byname=collections.defaultdict(list)
for r in recs: byname[r[0]].append(r)
dead=[]
for name,rs in byname.items():
    n=tokens[name]
    if n<=len(rs):   # only the definitions themselves
        for r in rs: dead.append(r)
dead.sort(key=lambda r:-r[4])
print('declarations:',len(recs),'never-referenced (name occurs only at its own defs):',len(dead),'lines',sum(r[4] for r in dead))
for name,kind,p,i,n in dead[:40]: print(f'{n:4d} {p[11:]:55s}:{i:4d} {kind} {name}')
