"""Run the 02:23 snapshot with one CPU, monitored 1 GiB and explicit time caps.
Usage: python run_checks.py PRIVATE_PARENT LEAN_PATH_FILE SOLVER_DEPS
No shared caches/build outputs are modified. Source snapshot is never overwritten.
"""
import ast, hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
import ctypes as ct
from ctypes import wintypes as wt
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
RUN=Path(sys.argv[1]).resolve(); SNAP=RUN/'KeplerConjecture'
if SNAP.exists(): raise SystemExit('Refusing to overwrite snapshot')
for role in ['Computation','Counterexamples','Experimental','Lean']:
    shutil.copytree(PROJECT/role,SNAP/role,ignore=shutil.ignore_patterns('__pycache__'))
tree=ast.parse((HERE.parent/'2026-11-14_0138/run_checks.py').read_text(encoding='utf-8'))
def assigns(n,key):
    return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==key for t in n.targets)
start=next(i for i,n in enumerate(tree.body) if assigns(n,'env'))
end=next(i for i,n in enumerate(tree.body) if assigns(n,'check'))
exec(compile(ast.Module(tree.body[start:end],type_ignores=[]),'resource_limits','exec'),globals())
env['LEAN_PATH']=Path(sys.argv[2]).read_text(encoding='utf-8-sig').strip()
lean='C:/Users/carte/.elan/toolchains/leanprover--lean4---v4.35.0/bin/lean.exe'
cube=HERE/'CubeDiffAudit.lean'
cube.write_text((SNAP/'Lean/Kepler15/CubeDiff.lean').read_text(encoding='utf-8')+'\n#print axioms Kepler15.cube_diff_le\n',encoding='utf-8')
check=str(SNAP/'Computation/shell_check.py')
jobs=[
 ('independent_exact','.',[sys.executable,str(HERE/'independent_checks.py'),str(SNAP)],45,False),
 ('cube_diff_lean','.',[lean,'-j1','-M1024',str(cube)],300,False),
 ('main_regressions','Computation',[sys.executable,'checker_adversarial.py'],45,False),
 ('sos_family','Computation',[sys.executable,'sos_family.py','--checker',check],45,False),
 ('shell_variant','Computation',[sys.executable,'sos_shell_variant.py'],30,False),
 ('periodic_cut_controls','Computation',[sys.executable,'cut_deficit.py'],30,False),
 ('block_fixtures','.',[sys.executable,'Experimental/scripts/block_evaluator.py'],60,False),
 ('transfer_fixtures','.',[sys.executable,'Experimental/scripts/transfer_evaluator.py'],45,False),
 ('factor_rounded_sdp','Counterexamples',[sys.executable,'x_r03b_sos_from_sdp.py'],300,True),
 ('dense_completion_search','.',[sys.executable,'Experimental/scripts/dense_completion_search.py','--seconds','300','--seeds','4'],320,False),
]
import numpy,scipy,sympy,mpmath
meta=dict(source_workers={
 'Main':'e76a15709c5907f76bbbf482755e916c71be76d4',
 'Computation':'dbeb320fb80be64799fc722174367ac61c387480',
 'Experimental':'e077495a70c9bad3128223ae25aa30828326f42d',
 'Counterexamples':'f7c9035c98497794806af352b36fe48a4b8ac821'},
 python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,sympy=sympy.__version__,
 mpmath=mpmath.__version__,cpu_affinity_bit=cpu_bit,memory_cap_bytes=1024**3,total_cap_seconds=900,
 solver_dependencies=str(Path(sys.argv[3]).resolve()),
 mathlib_commit='56a005855ea17e0b0958f73ec801ae140b0a1679',source_hashes={})
for p in [*SNAP.rglob('*.py'),*SNAP.rglob('*.lean'),SNAP/'Counterexamples/X_C013_certificate.json']:
    meta['source_hashes'][p.relative_to(SNAP).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/'environment.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
results=[]; began=time.monotonic()
for name,wd,argv,cap,solver in jobs:
    cap=min(cap,900-(time.monotonic()-began))
    if cap<=0:
        results.append(dict(job=name,status='not_run_total_cap')); continue
    jobenv=dict(env)
    if solver: jobenv['PYTHONPATH']=str(Path(sys.argv[3]).resolve())+os.pathsep+env.get('PYTHONPATH','')
    status='completed'; peak=0; started=time.monotonic()
    with (HERE/(name+'.log')).open('w',encoding='utf-8') as out:
        p=subprocess.Popen(argv,cwd=SNAP/wd,env=jobenv,stdout=out,stderr=subprocess.STDOUT,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        while p.poll() is None:
            peak=max(peak,memory_bytes(p))
            if peak>1024**3 or time.monotonic()-started>cap:
                status='memory_cap' if peak>1024**3 else 'time_cap'; p.kill(); break
            time.sleep(.25)
        code=p.wait()
    row=dict(job=name,args=argv,workdir=wd,status=status,exit_code=code,cap_seconds=cap,
        elapsed_seconds=round(time.monotonic()-started,3),peak_observed_bytes=peak,log=name+'.log')
    results.append(row); print(json.dumps(row),flush=True)
    (HERE/'jobs.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
(HERE/'jobs.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
