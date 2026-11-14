import os,re,sys
decl=re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |partial )*(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s({:]+)')
out=[]
for dp,dn,fn in os.walk('lean/OAI'):
    for f in fn:
        if not f.endswith('.lean'): continue
        p=os.path.join(dp,f); L=open(p).read().splitlines()
        starts=[]
        for i,l in enumerate(L):
            m=decl.match(l)
            if m: starts.append((i,m.group(1),m.group(2)))
        for k,(i,kind,name) in enumerate(starts):
            end=starts[k+1][0] if k+1<len(starts) else len(L)
            out.append((end-i,p,kind,name,i+1))
out.sort(reverse=True)
tot=sum(x[0] for x in out)
print('decls',len(out),'lines in decls',tot)
for n,p,kind,name,i in out[:45]:
    print(f'{n:5d} {p[8:]:55s}:{i:4d} {kind} {name}')
