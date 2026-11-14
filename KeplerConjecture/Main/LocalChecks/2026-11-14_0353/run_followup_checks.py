"""Frozen negative-eta witness, targeted repair regression and numeric C5 fixture."""
import ast, ctypes as ct, hashlib, json, os, subprocess, sys, time
from ctypes import wintypes as wt
from pathlib import Path
HERE=Path(__file__).resolve().parent; PROJECT=HERE.parents[2]; WT=PROJECT.parent
RUN=Path(sys.argv[1]).resolve(); SNAP=RUN/'KeplerConjecture'
if SNAP.exists(): raise SystemExit('Refusing to overwrite')
inputs={
 '33df893ec435bf383154b075f19a6d2c85fe5880':['Counterexamples/Reviews/X_eta_negative_witness.py','Counterexamples/Reviews/C_shell_propose.json','Counterexamples/Reviews/shell_check_7c56c5ee.py'],
 '9d6414d2495ebfd1abb02f6144b3882e57078089':['Computation/shell_check.py','Computation/checker_adversarial.py'],
 '212d13292b2f86d6c9114b7160642228644942a3':['Experimental/scripts/c5_completion.py']}
for sha,paths in inputs.items():
 for rel in paths:
    p=SNAP/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(subprocess.check_output(['git','show',f'{sha}:KeplerConjecture/{rel}'],cwd=WT))
tree=ast.parse((HERE.parent/'2026-11-14_0138/run_checks.py').read_text())
def assignment(n,key): return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==key for t in n.targets)
start=next(i for i,n in enumerate(tree.body) if assignment(n,'env')); end=next(i for i,n in enumerate(tree.body) if assignment(n,'check'))
exec(compile(ast.Module(tree.body[start:end],type_ignores=[]),'resource_limits','exec'),globals())
jobs=[('eta_negative_witness','Counterexamples/Reviews',['X_eta_negative_witness.py'],45),
      ('eta_repaired_regressions','Computation',['checker_adversarial.py'],45),
      ('e_c5_numeric','.', ['Experimental/scripts/c5_completion.py'],60)]
(HERE/'followup_environment.json').write_text(json.dumps(dict(inputs=inputs,cpu_affinity_bit=cpu_bit,memory_cap_bytes=1024**3,total_seconds=150,hashes={p.relative_to(SNAP).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in SNAP.rglob('*') if p.is_file()}),indent=2)+'\n')
results=[]; began=time.monotonic()
for name,wd,args,cap in jobs:
 cap=min(cap,150-(time.monotonic()-began)); status='completed'; peak=0; started=time.monotonic()
 if cap<=0: results.append(dict(job=name,status='not_run_total_cap')); continue
 with (HERE/(name+'.log')).open('w',encoding='utf-8') as out:
    p=subprocess.Popen([sys.executable,'-u',*args],cwd=SNAP/wd,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    while p.poll() is None:
        peak=max(peak,memory_bytes(p))
        if peak>1024**3 or time.monotonic()-started>cap:
            status='memory_cap' if peak>1024**3 else 'time_cap';p.kill();break
        time.sleep(.25)
    code=p.wait()
 row=dict(job=name,workdir=wd,args=args,status=status,exit_code=code,cap_seconds=cap,elapsed_seconds=round(time.monotonic()-started,3),peak_observed_bytes=peak,log=name+'.log');results.append(row);print(json.dumps(row),flush=True)
 (HERE/'followup_jobs.json').write_text(json.dumps(results,indent=2)+'\n')
