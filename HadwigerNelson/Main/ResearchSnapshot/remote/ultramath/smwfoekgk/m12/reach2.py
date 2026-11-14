import os,re,sys,json
from collections import defaultdict
root='OAI'
files={}
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p[:-5].replace('/','.')]=p
KW='theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque'
head=re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|scoped\s+)*('+KW+r')\b\s*(?:\(([^)]*)\))?\s*([A-Za-z_\u00a1-\uffff][\w\u00a1-\uffff\'.]*)?')
tok=re.compile(r'[A-Za-z_\u00a1-\uffff][\w\u00a1-\uffff\'.]*')
DECL=[];F={}
for m,p in sorted(files.items()):
    text=open(p).read(); lines=text.split('\n'); nlines=text.count('\n')
    ds=[]
    for i,l in enumerate(lines):
        mm=head.match(l)
        if mm:
            name=mm.group(3)
            if name in (None,'') or (mm.group(1) in ('instance','def') and name is None):
                name=None
            ds.append((i,mm.group(1),name))
    F[m]=(lines,nlines,p)
    for j,(i,k,nm) in enumerate(ds):
        end = ds[j+1][0] if j+1<len(ds) else len(lines)
        DECL.append(dict(mod=m,name=nm,kind=k,start=i+1,end=end,idx=len(DECL),
                         attr='@[' in lines[i]))
byname=defaultdict(list)
for d in DECL:
    if d['name']: byname[d['name']].append(d['idx'])
refs=[set() for _ in DECL]
for d in DECL:
    lines,_,_=F[d['mod']]
    body='\n'.join(lines[d['start']-1:d['end']])
    ts=set()
    for t in tok.findall(body):
        parts=t.split('.')
        for q in range(len(parts)):
            ts.add('.'.join(parts[q:]))
    if d['name']: ts.discard(d['name'])
    refs[d['idx']]=ts
ROOTS=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1] else [
 'OAI.Geometry.PlaneColoring.Chromatic','OAI.Geometry.PlaneColoring.ConnectedUnitFree',
 'OAI.Geometry.PlaneColoring.NullSetRobust','OAI.Geometry.PlaneColoring.Transfer']
keep=set(); forced=set()
for d in DECL:
    if d['mod'] in ROOTS or d['name'] is None or d['kind'] in ('instance','structure','class','inductive') or d['attr']:
        keep.add(d['idx']); forced.add(d['idx'])
changed=True
while changed:
    changed=False
    used=set()
    for i in keep: used |= refs[i]
    for t in used:
        for j in byname.get(t,()):
            if j not in keep: keep.add(j); changed=True
drop=[d for d in DECL if d['idx'] not in keep]
bymod=defaultdict(int); cnt=defaultdict(int)
for d in drop: bymod[d['mod']]+=d['end']-d['start']+1; cnt[d['mod']]+=1
print('TOTAL lines %d decls %d forced %d'%(sum(F[m][1] for m in F),len(DECL),len(forced)))
print('dropped decls %d, approx lines %d'%(len(drop),sum(bymod.values())))
for m,v in sorted(bymod.items(),key=lambda kv:-kv[1]): print('  %5d (%3d) %-60s of %d'%(v,cnt[m],m,F[m][1]))
json.dump([dict(mod=d['mod'],name=d['name'],start=d['start'],end=d['end'],kind=d['kind']) for d in drop],open(os.path.dirname(os.path.abspath(__file__))+'/drop.json','w'),indent=0)
