"""Bounded local review; frozen integrated sources, one core and one GiB."""
import ast,ctypes as ct,hashlib,json,os,shutil,subprocess,sys,time
from ctypes import wintypes as wt
from pathlib import Path
HERE=Path(__file__).resolve().parent;PROJECT=HERE.parents[2];WT=PROJECT.parent
RUN=Path(sys.argv[1]).resolve();SNAP=RUN/'KeplerConjecture'
if SNAP.exists():raise SystemExit('Refusing overwrite')
for role in ['Computation','Counterexamples','Experimental']:
 shutil.copytree(PROJECT/role,SNAP/role,ignore=shutil.ignore_patterns('__pycache__'))
tree=ast.parse((HERE.parent/'2026-11-14_0138/run_checks.py').read_text(encoding='utf-8'))
def assignment(n,key):return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==key for t in n.targets)
start=next(i for i,n in enumerate(tree.body) if assignment(n,'env'));end=next(i for i,n in enumerate(tree.body) if assignment(n,'check'))
exec(compile(ast.Module(tree.body[start:end],type_ignores=[]),'resource_limits','exec'),globals())
jobs=[('independent_repairs','.',[str(HERE/'probe_repairs.py'),str(SNAP)],30),
 ('c_cut_tests','Computation',['tests_cut_flow.py'],30),
 ('e_exact_fixture','.', ['Experimental/scripts/c5_fixture.py'],30),
 ('e_barlow_contact','.', ['Experimental/scripts/barlow_contact_cell.py'],30),
 ('e_global_pilot_seed0','.', ['Experimental/scripts/c5_global_search.py','--seconds','45','--seed','0'],60)]
meta=dict(integrated_source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=WT,text=True).strip(),sources=dict(Main='7ba71464259d9965e7e060c8a61ed981d0e2b0bc',Computation='6fbd0a1bf214a92b625cee84e8ee95ac5da4b8d9',Experimental='498cfc3c0ce8d023fbf29b5810d06be115ac256b',Counterexamples='d64de362da7b6f52bd494d15364e67783a3b184b'),cpu_affinity_bit=cpu_bit,memory_cap_bytes=1024**3,total_cap_seconds=180,source_hashes={p.relative_to(SNAP).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in SNAP.rglob('*') if p.is_file()})
(HERE/'environment.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
results=[];began=time.monotonic()
for name,wd,args,cap in jobs:
 cap=min(cap,180-(time.monotonic()-began));status='completed';peak=0;started=time.monotonic()
 if cap<=0:results.append(dict(job=name,status='not_run_total_cap'));continue
 with (HERE/(name+'.log')).open('w',encoding='utf-8') as out:
  p=subprocess.Popen([sys.executable,'-u',*args],cwd=SNAP/wd,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
  while p.poll() is None:
   peak=max(peak,memory_bytes(p))
   if peak>1024**3 or time.monotonic()-started>cap:
    status='memory_cap' if peak>1024**3 else 'time_cap';p.kill();break
   time.sleep(.25)
  code=p.wait()
 row=dict(job=name,workdir=wd,args=args,status=status,exit_code=code,cap_seconds=cap,elapsed_seconds=round(time.monotonic()-started,3),peak_observed_bytes=peak,log=name+'.log');results.append(row);print(json.dumps(row),flush=True)
 (HERE/'jobs.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
