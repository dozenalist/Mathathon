import os,re,collections
root='lean'
mods={}
for dp,dn,fn in os.walk(root):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); m=p[len('lean/'):-5].replace('/','.')
            mods[m]=(p,open(p).read())
lines={m:len(t.splitlines()) for m,(p,t) in mods.items()}
depp=re.compile(r'^import\s+(\S+)',re.M)
g={m:[d for d in depp.findall(t)] for m,(p,t) in mods.items()}
rev=collections.defaultdict(set)
for m,ds in g.items():
    for d in ds: rev[d].add(m)
def cl(m,seen=None):
    seen=set() if seen is None else seen
    if m in seen: return seen
    seen.add(m)
    for d in g.get(m,[]):
        if d.startswith('OAI'): cl(d,seen)
    return seen
head='OAI.Geometry.PlaneColoring.Five'
C=cl(head)
print('closure of Five:',len(C),sum(lines[x] for x in C))
for m in sorted(C,key=lambda m:-lines[m]):
    consumers=sorted(rev[m])
    print(f'{lines[m]:5d} {m[4:]:58s} consumers={len(consumers)} {[c.split(".")[-1] for c in consumers][:6]}')
print()
print('NOT in closure:')
for m in sorted(set(mods)-C,key=lambda m:-lines[m]):
    print(f'{lines[m]:5d} {m[4:]:58s} consumers={sorted(rev[m])}')
