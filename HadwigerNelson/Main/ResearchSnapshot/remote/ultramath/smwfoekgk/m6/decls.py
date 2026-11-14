import os,re,sys,json,collections
ROOT='lean/OAI'
files={}
for dp,dn,fn in os.walk(ROOT):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p]=open(p,encoding='utf-8',errors='ignore').read()
decl_re=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe|scoped)\s+)*(theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\s+([A-Za-z_][\w\u2080-\u209c\'!?]*)',re.M)
decls={}
for p,txt in files.items():
    for m in decl_re.finditer(txt):
        kind,name=m.group(1),m.group(2)
        ln=txt.count('\n',0,m.start())+1
        decls.setdefault(name,[]).append((kind,p,ln))
# identifier counts per file
tok=re.compile(r'[A-Za-z_][\w\u2080-\u209c\'!?]*')
tokcounts={p:collections.Counter(tok.findall(t)) for p,t in files.items()}
res={}
for n,locs in decls.items():
    ownerfiles={l[1] for l in locs}
    ext={}
    for p,c in tokcounts.items():
        k=c.get(n,0)
        if k:
            if p in ownerfiles:
                ext[p]=k  # inside own file
            else:
                ext[p]=k
    outside={p:k for p,k in ext.items() if p not in ownerfiles}
    res[n]=(locs,outside)
json.dump({n:{'locs':v[0],'outside':v[1]} for n,v in res.items()},open('.ultramath/smwfoekgk/m6/decls.json','w'))
tot=sum(t.count('\n')+1 for t in files.values())
print('files',len(files),'lines',tot,'named decls',len(decls))
byk=collections.Counter(len(v[1]) for v in res.values())
print('decls by #other-files mentioning them:',dict(sorted(byk.items())))
zero=sorted(n for n,v in res.items() if not v[1])
print('=== decls mentioned in NO other file:',len(zero))
for n in zero:
    locs,_=res[n]
    print('   ',locs[0][0],n,locs[0][1],locs[0][2])
