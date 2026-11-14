import os,re,collections
root='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean'
mods={}
for dp,dn,fn in os.walk(os.path.join(root,'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m='OAI.'+os.path.relpath(p,os.path.join(root,'OAI'))[:-5].replace('/','.')
            src=open(p).read()
            mods[m]=dict(lines=len(src.splitlines()),imports=re.findall(r'^import\s+(\S+)',src,re.M),path=p)
users=collections.defaultdict(set)
for m,d in mods.items():
    for i in d['imports']:
        users[i].add(m)
short=lambda m:m.replace('OAI.','')
for m in sorted(mods):
    d=mods[m]
    print(f"{d['lines']:5d} {short(m):55s} users={len(users[m]):2d}  imports={[short(i) for i in d['imports']]}")
