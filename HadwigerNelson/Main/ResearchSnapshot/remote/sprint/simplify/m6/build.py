#!/usr/bin/env python3
"""Build a copy of the OAI tree with `lean -o`, topologically, into <root>/build/lib.
Usage: python3 build.py <srcroot> <builddir> [--jobs N] [--only MOD] [--list]
Prints per-module status and total lines."""
import os,re,subprocess,sys,time,json
from concurrent.futures import ThreadPoolExecutor
src=os.path.abspath(sys.argv[1]); build=os.path.abspath(sys.argv[2])
jobs=int(os.environ.get('JOBS','3'))
mods={}; deps={}
for dp,dn,fn in os.walk(src):
    for f in fn:
        if not f.endswith('.lean'): continue
        p=os.path.join(dp,f); rel=os.path.relpath(p,src)
        if not rel.startswith('OAI/'): continue
        m=rel[:-5].replace('/','.')
        mods[m]=p; d=[]
        for line in open(p,errors='ignore'):
            mm=re.match(r'^import\s+([\w.]+)',line.strip())
            if mm: d.append(mm.group(1))
        deps[m]=[x for x in d if x.startswith('OAI.')]
order=[];state={}
def visit(n,stack=()):
    if state.get(n)==2: return
    if state.get(n)==1: raise SystemExit('cycle '+n)
    state[n]=1
    for x in deps[n]:
        if x in mods: visit(x)
    state[n]=2; order.append(n)
for n in sorted(mods): visit(n)
os.makedirs(build,exist_ok=True)
leanpath=os.environ['LEAN_PATH']
env=dict(os.environ); env['LEAN_PATH']=build+':'+leanpath
import hashlib
hfile=os.path.join(build,'.hashes.json')
old=json.load(open(hfile)) if os.path.exists(hfile) else {}
def sha(p): return hashlib.sha1(open(p,'rb').read()).hexdigest()
cur={n:sha(mods[n]) for n in mods}
failed=[]
def need(n,seen=None):
    seen=seen or set()
    if n in seen: return False
    seen.add(n)
    o=os.path.join(build,n.replace('.','/')+'.olean')
    if not os.path.exists(o): return True
    if old.get(n)!=cur[n]: return True
    return any(need(d,seen) for d in deps[n] if d in mods)
todo=[n for n in order if need(n)]
print(f'{len(mods)} modules, {len(todo)} to build',flush=True)
t0=time.time()
def run(n):
    o=os.path.join(build,n.replace('.','/')+'.olean')
    os.makedirs(os.path.dirname(o),exist_ok=True)
    r=subprocess.run(['lean','-o',o,mods[n]],capture_output=True,text=True,env=env)
    return n,r.returncode,r.stdout+r.stderr
from concurrent.futures import FIRST_COMPLETED, wait, ThreadPoolExecutor
ex=ThreadPoolExecutor(max_workers=jobs)
done=set(); pending=list(todo); running={}
while pending or running:
    ready=[n for n in pending if all(d in done or d not in mods for d in deps[n])]
    while ready and len(running)<jobs:
        n=ready.pop(0); pending.remove(n)
        running[ex.submit(run,n)]=n
    if not running:
        print('STUCK: no progress; remaining', pending[:5], flush=True); break
    fin,_=wait(list(running),return_when=FIRST_COMPLETED)
    for f in fin:
        n=f.result()[0]; rc=f.result()[1]; out=f.result()[2]
        del running[f]
        done.add(n)
        if rc!=0:
            failed.append(n); print('FAIL',n,flush=True); print(out[:3000],flush=True)
for n in order:
    if n not in failed: old[n]=cur[n]
json.dump(old,open(hfile,'w'))
print(f'built in {time.time()-t0:.0f}s; failures={len(failed)}')
if failed: print('failed:',failed)
tot=sum(sum(1 for _ in open(p,errors='ignore')) for p in mods.values())
print('total lines',tot)
