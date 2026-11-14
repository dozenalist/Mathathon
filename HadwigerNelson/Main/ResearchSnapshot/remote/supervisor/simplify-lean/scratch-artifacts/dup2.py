import json,re,collections,os
D=json.load(open('supervisor/simplify-lean/.scratch/decls.json'))
# usage counts: how many times the short name occurs in other files
files={}
for dp,_,fs in os.walk('lean/OAI'):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p]=open(p).read()
use=collections.Counter()
for d in D:
    nm=d['name'].split('.')[-1]
    if len(nm)<4: continue
    pat=re.compile(r'(?<![A-Za-z0-9_.])'+re.escape(nm)+r'(?![A-Za-z0-9_])')
    c=0
    for p,t in files.items():
        n=len(pat.findall(t))
        if p==d['file']: n-=1   # subtract its own definition
        c+=max(n,0)
    use[d['name']+"@"+d['file']+":"+str(d['line'])]=c
by=collections.defaultdict(list)
for d in D:
    c=re.sub(r'\s+','',d['concl'])
    if len(c)<12: continue
    by[c].append(d)
rows=[]
for c,ds in by.items():
    fs={d['file'] for d in ds}
    if len(fs)<2: continue
    tot=sum(d['nbody'] for d in ds)
    rows.append((tot,len(ds),c,ds))
rows.sort(reverse=True)
print("== top cross-file duplicate-conclusion clusters by total body lines (restricted to rigidity half)")
for tot,n,c,ds in rows[:10]:
    if 'Analysis' not in c and 'MeasureTheory' not in str([d['file'] for d in ds]): continue
    print(f'--- total {tot} body-lines, {n} decls: {c[:90]}')
    for d in ds:
        k=d['name']+"@"+d['file']+":"+str(d['line'])
        print(f'    body={d["nbody"]:>3}  uses={use.get(k,0):>2}  {d["file"]}:{d["line"]}  {d["name"]}')
