import os,re,sys,json
from collections import defaultdict
exec(open('/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m12/reach2.py').read().split("ROOTS=")[0])
REMOVE=set(sys.argv[1].split(','))
FORCE=set(sys.argv[2].split(',')) if len(sys.argv)>2 else set()
ROOTS=['OAI.Geometry.PlaneColoring.Chromatic','OAI.Geometry.PlaneColoring.ConnectedUnitFree',
 'OAI.Geometry.PlaneColoring.NullSetRobust','OAI.Geometry.PlaneColoring.Transfer']
keep=set()
for d in DECL:
    if d['name'] in REMOVE: continue
    if d['mod'] in ROOTS or d['name'] in FORCE or d['name'] is None or d['kind'] in ('instance','structure','class','inductive') or d['attr']:
        keep.add(d['idx'])
changed=True
while changed:
    changed=False
    used=set()
    for i in keep: used |= refs[i]
    for t in used:
        for j in byname.get(t,()):
            if j not in keep and DECL[j]['name'] not in REMOVE: keep.add(j); changed=True
drop=[d for d in DECL if d['idx'] not in keep]
bymod=defaultdict(int); cnt=defaultdict(int)
for d in drop: bymod[d['mod']]+=d['end']-d['start']+1; cnt[d['mod']]+=1
print('dropped %d decls, %d lines (of %d)'%(len(drop),sum(bymod.values()),sum(F[m][1] for m in F)))
for m,v in sorted(bymod.items(),key=lambda kv:-kv[1])[:26]: print('  %5d (%3d) %-58s of %d'%(v,cnt[m],m,F[m][1]))
json.dump([dict(mod=d['mod'],name=d['name'],start=d['start'],end=d['end'],kind=d['kind']) for d in drop],open('/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m12/drop2.json','w'),indent=0)
