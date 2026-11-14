import os,re,sys
root='OAI'
mods={}
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m=p[:-5].replace('/','.')
            src=open(p).read()
            deps=set()
            for line in src.splitlines():
                line=line.strip()
                if line.startswith('import '):
                    deps.add(line[7:].strip())
            nl=src.count('\n')
            mods[m]=(deps,nl,p)
# import closure
def closure(start):
    seen=set(); st=[start]
    while st:
        m=st.pop()
        for d in mods[m][0]:
            if d in mods and d not in seen:
                seen.add(d); st.append(d)
    return seen
# who imports whom
rev={m:set() for m in mods}
for m,(deps,_,_) in mods.items():
    for d in deps:
        if d in rev: rev[d].add(m)
print('total mods',len(mods),'total lines',sum(v[1] for v in mods.values()))
# find roots: modules not imported by anyone
roots=sorted(m for m in mods if not rev[m])
print('roots:'); 
for r in roots: print('  ',r,mods[r][1])
