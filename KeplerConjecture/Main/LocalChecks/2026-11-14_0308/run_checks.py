"""Bounded frozen-source local jobs. Usage: python run_checks.py PRIVATE_PARENT SOLVER_DEPS"""
import ast, ctypes as ct, hashlib, json, os, shutil, subprocess, sys, time
from ctypes import wintypes as wt
from pathlib import Path
HERE=Path(__file__).resolve().parent; PROJECT=HERE.parents[2]
RUN=Path(sys.argv[1]).resolve(); SNAP=RUN/'KeplerConjecture'
if SNAP.exists(): raise SystemExit('Refusing to overwrite snapshot')
for role in ['Computation','Counterexamples','Experimental']:
    shutil.copytree(PROJECT/role,SNAP/role,ignore=shutil.ignore_patterns('__pycache__'))
tree=ast.parse((HERE.parent/'2026-11-14_0138/run_checks.py').read_text(encoding='utf-8'))
def assignment(n,key): return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==key for t in n.targets)
start=next(i for i,n in enumerate(tree.body) if assignment(n,'env'))
end=next(i for i,n in enumerate(tree.body) if assignment(n,'check'))
exec(compile(ast.Module(tree.body[start:end],type_ignores=[]),'resource_limits','exec'),globals())
check=str(SNAP/'Computation/shell_check.py'); adapter=str(HERE/'run_with_checker.py')
jobs=[('independent_exact','.',[str(HERE/'independent_checks.py'),str(SNAP)],60,False),
      ('main_regressions','Computation',['checker_adversarial.py'],60,False),
      ('x_verify_all','Counterexamples',['verify_all.py'],60,False),
      ('c_review_controls','Computation',['tests_0138.py'],60,False),
      ('c_both_sides','Computation',['sos_both_sides.py'],30,False),
      ('e_claim_controls','.', ['Experimental/scripts/verify_all_claims.py'],60,False)]
for seed in (100,101,102):
    jobs.append((f'gram_pilot_seed{seed}','Computation',[adapter,str(SNAP/'Computation/sos_qside_polish.py'),check,'--degree','7','--iters','4000','--seed',str(seed),'--uphill','0.05','--out',f'out/local_pilot_{seed}.json'],90,False))
jobs.append(('rescaled_sdp_pilot','Counterexamples',[str(HERE/'rescaled_pilot.py')],150,True))
import numpy, scipy, sympy, mpmath
meta=dict(source_workers=dict(Main='7c56c5ee4a2fb515a35c6f7734bfd06adf63b2f5',Computation='9d9ff68227362fa10e4841dbfcd82f6c12a1a8f8',Experimental='9a46efcbb771deef30c88fde761587c79eb96847',Counterexamples='6535e768657ae6cb7f44259079bd42570dc979ef'),
          python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,sympy=sympy.__version__,mpmath=mpmath.__version__,cpu_affinity_bit=cpu_bit,memory_cap_bytes=1024**3,total_cap_seconds=600,source_hashes={})
for p in [*SNAP.rglob('*.py'),SNAP/'Counterexamples/X_C014_certificate.json',SNAP/'Computation/out/sos_both_sides.json']:
    meta['source_hashes'][p.relative_to(SNAP).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/'environment.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
results=[]; began=time.monotonic()
for name,wd,args,cap,solver in jobs:
    cap=min(cap,600-(time.monotonic()-began))
    if cap<=0: results.append(dict(job=name,status='not_run_total_cap')); continue
    jobenv=dict(env)
    if solver: jobenv['PYTHONPATH']=str(Path(sys.argv[2]).resolve())+os.pathsep+env.get('PYTHONPATH','')
    status='completed'; peak=0; started=time.monotonic()
    with (HERE/(name+'.log')).open('w',encoding='utf-8') as out:
        p=subprocess.Popen([sys.executable,'-u',*args],cwd=SNAP/wd,env=jobenv,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        while p.poll() is None:
            peak=max(peak,memory_bytes(p))
            if peak>1024**3 or time.monotonic()-started>cap:
                status='memory_cap' if peak>1024**3 else 'time_cap'; p.kill(); break
            time.sleep(.25)
        code=p.wait()
    row=dict(job=name,workdir=wd,args=args,status=status,exit_code=code,cap_seconds=cap,elapsed_seconds=round(time.monotonic()-started,3),peak_observed_bytes=peak,log=name+'.log')
    results.append(row); print(json.dumps(row),flush=True)
    (HERE/'jobs.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
(HERE/'jobs.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
