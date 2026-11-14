import os,re,sys,collections
root='lean'
mods={}
for dp,dn,fn in os.walk(root):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m=p[len('lean/'):-5].replace('/','.')
            mods[m]=(p,open(p).read())
lines={m:len(t.splitlines()) for m,(p,t) in mods.items()}
depp=re.compile(r'^import\s+(\S+)',re.M)
g={m:depp.findall(t) for m,(p,t) in mods.items()}
def cl(m,seen=None):
    if seen is None: seen=set()
    if m in seen: return seen
    seen.add(m)
    for d in g.get(m,[]):
        if d.startswith('OAI'): cl(d,seen)
    return seen
for m in sys.argv[1:]:
    c=cl(m)
    tot=sum(lines[x] for x in c)
    print(m,'closure',len(c),'modules',tot,'lines')
    bydir=collections.Counter()
    for x in c: bydir[x.split('.')[1]]+=lines[x]
    print('  ',dict(bydir))
