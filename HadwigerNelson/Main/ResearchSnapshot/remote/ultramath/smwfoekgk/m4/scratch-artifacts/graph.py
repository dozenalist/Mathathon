import os,re,sys,collections
root='/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean'
mods={}
for dp,dn,fn in os.walk(os.path.join(root,'OAI')):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f)
            m='OAI.'+os.path.relpath(p,os.path.join(root,'OAI'))[:-5].replace('/','.')
            src=open(p).read()
            imps=re.findall(r'^import\s+(\S+)',src,re.M)
            mods[m]=(len(src.splitlines()),imps,p)
def clos(m,seen=None):
    if seen is None: seen=set()
    if m in seen or m not in mods: return seen
    seen.add(m)
    for i in mods[m][1]:
        clos(i,seen)
    return seen
if __name__=='__main__':
    for m in sys.argv[1:]:
        c=clos(m)
        print(m,'closure:',len(c),'modules',sum(mods[x][0] for x in c),'lines')
