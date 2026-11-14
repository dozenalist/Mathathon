import os,re,json,collections,sys
sys.path.insert(0,'sprint/simplify/m6')
from blocks import blocks,delete
ROOT=sys.argv[1]
files={}
for dp,dn,fn in os.walk(ROOT):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); files[p]=open(p,encoding='utf-8',errors='ignore').read()
# documented names: any identifier appearing in .md docs
docs=''
for dp,dn,fn in os.walk('.'):
    if '/.scratch' in dp or '/.ultramath' in dp or '/attachments' in dp or '/sprint' in dp: continue
    for f in fn:
        if f.endswith('.md'): docs+=open(os.path.join(dp,f),encoding='utf-8',errors='ignore').read()
toks=set(re.findall(r'[A-Za-z_][\w\u2080-\u209c\'!?]*',docs))
tokre=re.compile(r'[A-Za-z_][\w\u2080-\u209c\'!?]*')
removed=[]; rounds=0
while True:
    rounds+=1
    allconn=collections.Counter()
    for p,t in files.items(): allconn.update(tokre.findall(t))
    cand=collections.defaultdict(set)
    for p,txt in files.items():
        lines=txt.split('\n')
        for s,e,kind,name in blocks(lines):
            if kind in ('instance','class','inductive','structure'): continue
            if e-s<2: continue
            if allconn[name]>1: continue
            if name in toks: continue
            hdr='\n'.join(lines[max(0,s-5):s+3])
            if '@[' in hdr or 'deriving' in lines[s]: continue
            cand[p].add(name)
    if not cand: break
    n=0
    for p,names in cand.items():
        gone=delete(p,names); removed += [(p.replace(ROOT+'/',''),g) for g in gone]; n+=len(gone)
        files[p]=open(p,encoding='utf-8').read()
    print(f'round {rounds}: removed {n}',flush=True)
    if n==0: break
print('total removed decls',len(removed))
json.dump(removed,open(sys.argv[2],'w'),indent=0)
