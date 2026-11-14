import os
root='OAI'
mods={}
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); m=p[:-5].replace('/','.')
            src=open(p).read()
            deps={l.strip()[7:].strip() for l in src.splitlines() if l.strip().startswith('import ')}
            mods[m]=(deps,src.count('\n'),p)
rev={m:set() for m in mods}
for m,(deps,_,_) in mods.items():
    for d in deps:
        if d in rev: rev[d].add(m)
print("module | lines | importers")
for m in sorted(mods, key=lambda m:-mods[m][1]):
    print(f"{mods[m][1]:5d} {m}  <- {sorted(x.split('.')[-1] for x in rev[m])}")
