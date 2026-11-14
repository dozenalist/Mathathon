import os,sys,subprocess,hashlib,json
from concurrent.futures import ThreadPoolExecutor
pris=sys.argv[1]; new=sys.argv[2]; jobs=int(os.environ.get('JOBS','4'))
def shas(root):
    d={}
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if f.endswith('.lean'):
                p=os.path.join(dp,f); d[os.path.relpath(p,root)]=hashlib.sha1(open(p,'rb').read()).hexdigest()
    return d
a=shas(pris); b=shas(new)
changed=[k for k in sorted(b) if a.get(k)!=b[k]]
print(f'{len(changed)} changed modules',flush=True)
env=dict(os.environ)
def run(rel):
    r=subprocess.run(['lean',os.path.join(new,rel)],capture_output=True,text=True,env=env)
    return rel,r.returncode,(r.stdout+r.stderr)[:2000]
bad=[]
with ThreadPoolExecutor(max_workers=jobs) as ex:
    for rel,rc,out in ex.map(run,changed):
        print(('OK  ' if rc==0 else 'FAIL')+' '+rel,flush=True)
        if rc!=0:
            bad.append(rel); print(out,flush=True)
print('failures:',len(bad))
