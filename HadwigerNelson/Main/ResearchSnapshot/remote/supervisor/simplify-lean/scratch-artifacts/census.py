import re, os, sys, json, collections
ROOT='lean/OAI'
decl=re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |partial )*(theorem|lemma)\s+([A-Za-z0-9_.\'!?]+)')
cmd=re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |partial |scoped |local )*(theorem|lemma|def|abbrev|instance|structure|inductive|class|namespace|end|section|open|variable|universe|#)')
out=[]
for dp,_,fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.lean'): continue
        p=os.path.join(dp,f); L=open(p).read().split('\n')
        i=0
        while i<len(L):
            m=decl.match(L[i])
            if not m: i+=1; continue
            j=i+1
            while j<len(L) and not cmd.match(L[j]) and not L[j].startswith('end '):
                j+=1
            blk=L[i:j]
            out.append(dict(file=p,name=m.group(2),line=i+1,blk=blk))
            i=j
print('decls',len(out))
# statement/conclusion extraction: text between ':' after binders and ':=' ; conclusion = last non-empty line of statement
def split_stmt(blk):
    txt=blk[0]
    # find top-level ':=' or ' where ' etc; crude: first ':='
    stmt=[];body=[]
    inseg=False
    joined='\n'.join(blk)
    idx=joined.find(':=')
    if idx<0: return joined,''
    return joined[:idx],joined[idx:]
for d in out:
    s,b=split_stmt(d['blk'])
    d['stmt']=s; d['body']=b
    lines=[x.strip() for x in s.split('\n') if x.strip()]
    d['concl']=lines[-1] if lines else ''
    d['nlines']=len(d['blk'])
    d['nbody']=len([x for x in b.split('\n') if x.strip()])
json.dump([{k:v for k,v in d.items() if k!='blk'} for d in out],open('supervisor/simplify-lean/.scratch/decls.json','w'))
# duplicate conclusions across files
by=collections.defaultdict(list)
for d in out:
    c=re.sub(r'\s+','',d['concl'])
    if len(c)<12: continue
    by[c].append(d)
n=0
for c,ds in sorted(by.items(),key=lambda kv:-len(kv[1])):
    if len(ds)<2: continue
    files={d['file'] for d in ds}
    if len(files)<2: continue
    n+=1
    print(f'--- {len(ds)} decls, {len(files)} files :: {c[:110]}')
    for d in ds: print(f'    {d["file"]}:{d["line"]} {d["name"]}  body={d["nbody"]}L')
    if n>=18: break
