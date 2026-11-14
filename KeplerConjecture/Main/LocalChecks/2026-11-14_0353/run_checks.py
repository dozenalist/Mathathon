"""Run reviewed frozen inputs with one CPU, one GiB and a five-minute total cap."""
import ast, ctypes as ct, hashlib, json, os, subprocess, sys, time
from ctypes import wintypes as wt
from pathlib import Path
HERE=Path(__file__).resolve().parent; PROJECT=HERE.parents[2]; WT=PROJECT.parent
RUN=Path(sys.argv[1]).resolve(); SNAP=RUN/'KeplerConjecture'
sources={'Main':'e70dd10c64a305f0c6bba3401fc20c8b3d7eb7cd','Computation':'4bcbd3a0ee94bd29d2f1fdcc5e69aaf1f0ed0a62','Experimental':'82689ba1999a1ca240e480f9bc90121101f9e801','Counterexamples':'118ecd1601bb500f7d305ce299dcb00f73a66772'}
if SNAP.exists(): raise SystemExit('Refusing to overwrite frozen snapshot')
for role,sha in sources.items():
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',sha,'--',f'KeplerConjecture/{role}'],cwd=WT,text=True).splitlines()
    for name in paths:
        dest=RUN/name; dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(subprocess.check_output(['git','show',f'{sha}:{name}'],cwd=WT))
tree=ast.parse((HERE.parent/'2026-11-14_0138/run_checks.py').read_text(encoding='utf-8'))
def assignment(n,key): return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==key for t in n.targets)
start=next(i for i,n in enumerate(tree.body) if assignment(n,'env'))
end=next(i for i,n in enumerate(tree.body) if assignment(n,'check'))
exec(compile(ast.Module(tree.body[start:end],type_ignores=[]),'resource_limits','exec'),globals())
jobs=[('independent_exact','.',[str(HERE/'independent_checks.py'),str(SNAP)],90),
      ('c_cut_tests','Computation',['tests_cut_flow.py'],30),
      ('c_cut_flow','Computation',['cut_flow.py','--fixture','out/fixture_example.json'],45),
      ('c_quintic2','Computation',['sos_both_sides_quintic2.py'],45),
      ('e_icosa_constants','.', ['Experimental/scripts/icosa_cut_check.py'],30)]
import numpy, scipy, sympy, mpmath
meta=dict(sources=sources,python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,sympy=sympy.__version__,mpmath=mpmath.__version__,cpu_affinity_bit=cpu_bit,memory_cap_bytes=1024**3,total_cap_seconds=300,
          hashes={p.relative_to(SNAP).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in SNAP.rglob('*') if p.is_file()})
(HERE/'environment.json').write_text(json.dumps(meta,indent=2)+'\n')
results=[]; began=time.monotonic()
for name,wd,args,cap in jobs:
    cap=min(cap,300-(time.monotonic()-began)); status='completed'; peak=0; started=time.monotonic()
    if cap<=0: results.append(dict(job=name,status='not_run_total_cap')); continue
    with (HERE/(name+'.log')).open('w',encoding='utf-8') as out:
        p=subprocess.Popen([sys.executable,'-u',*args],cwd=SNAP/wd,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        while p.poll() is None:
            peak=max(peak,memory_bytes(p))
            if peak>1024**3 or time.monotonic()-started>cap:
                status='memory_cap' if peak>1024**3 else 'time_cap'; p.kill(); break
            time.sleep(.25)
        code=p.wait()
    row=dict(job=name,workdir=wd,args=args,status=status,exit_code=code,cap_seconds=cap,elapsed_seconds=round(time.monotonic()-started,3),peak_observed_bytes=peak,log=name+'.log')
    results.append(row); print(json.dumps(row),flush=True)
    (HERE/'jobs.json').write_text(json.dumps(results,indent=2)+'\n')
