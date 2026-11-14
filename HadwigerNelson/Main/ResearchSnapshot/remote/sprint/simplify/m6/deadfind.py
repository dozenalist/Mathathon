import os,re,json,collections,sys
sys.path.insert(0,'sprint/simplify/m6')
from blocks import blocks,DECL
ROOT=os.environ.get('ROOT','lean/OAI')
files={}
for dp,dn,fn in os.walk(ROOT):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p]=open(p,encoding='utf-8',errors='ignore').read()
tok=re.compile(r'[A-Za-z_][\w\u2080-\u209c\'!?]*')
allconn=collections.Counter()
for p,t in files.items(): allconn.update(tok.findall(t))
dead=[]
for p,txt in files.items():
    lines=txt.split('\n')
    for s,e,kind,name in blocks(lines):
        if kind in ('instance','class','inductive','structure'): continue
        if e-s<2: continue
        if allconn[name]>1: continue
        # attribute in the 5 lines above or on any line of the header
        hdr='\n'.join(lines[max(0,s-5):s+1])
        if '@[' in hdr: continue
        if 'deriving' in lines[s]: continue
        dead.append(dict(file=p.replace('lean/OAI/',''),name=name,kind=kind,lines=e-s))
json.dump(dead,open(os.environ.get('OUT','.ultramath/smwfoekgk/m6/dead2.json'),'w'),indent=0)
print('candidates',len(dead),'lines',sum(d['lines'] for d in dead))
byfile=collections.Counter()
for d in dead: byfile[d['file']]+=d['lines']
for f,n in byfile.most_common(): print(f'{n:5d} {f}')
