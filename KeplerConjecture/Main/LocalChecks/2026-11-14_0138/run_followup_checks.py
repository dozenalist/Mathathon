"""Bounded local checks of the second immutable 01:38 review snapshot.

Usage: python run_followup_checks.py PRIVATE_PARENT LEAN_PATH_FILE LEAN_BINARY
Reuses matching caches read-only; writes no shared build products. On Windows,
one inherited CPU, one BLAS thread, monitored 1 GiB process memory, 600s total.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
RUN = Path(sys.argv[1]).resolve()
SNAP = RUN / 'KeplerConjecture'
if SNAP.exists():
    raise SystemExit('Refusing to overwrite the frozen snapshot')
for role in ['Computation', 'Experimental', 'Counterexamples', 'Lean']:
    shutil.copytree(PROJECT / role, SNAP / role,
                    ignore=shutil.ignore_patterns('__pycache__'))

# Reuse only the reviewed resource-accounting definitions, not its run body.
tree = ast.parse((HERE / 'run_checks.py').read_text(encoding='utf-8'))
start = next(i for i, n in enumerate(tree.body)
             if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'env' for t in n.targets))
end = next(i for i, n in enumerate(tree.body)
           if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'check' for t in n.targets))
import ctypes as ct
from ctypes import wintypes as wt
exec(compile(ast.Module(tree.body[start:end], type_ignores=[]), 'resource_limits', 'exec'), globals())
env['LEAN_PATH'] = Path(sys.argv[2]).read_text(encoding='utf-8-sig').strip()
lean = sys.argv[3]

original = SNAP / 'Lean/Kepler15/Volume.lean'
targeted = HERE / 'VolumeTargeted.lean'
targeted.write_text(original.read_text(encoding='utf-8').replace(
    'import Mathlib\n',
    'import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls\n'
    'import Mathlib.Tactic\n') +
    '\n#print axioms Kepler15.volume_ball_unit\n'
    '#print axioms Kepler15.volume_ball_three\n'
    '#print axioms Kepler15.cube_diff_le\n', encoding='utf-8')

jobs = [
    ('volume_original', '.', [lean, '-j1', '-M1024', str(original)], 60),
    ('volume_targeted', '.', [lean, '-j1', '-M1024', str(targeted)], 240),
    ('shell_sos_degree9', 'Computation', [sys.executable, 'shell_sos.py',
        '--checker', str(SNAP / 'Computation/shell_check.py'), '--degree', '9',
        '--out', str(RUN / 'shell_sos_degree9.json')], 120),
    ('transfer_fcc_fixture', 'Computation', [sys.executable, 'transfer_check.py'], 60),
    ('cluster_monotonicity_fixture', 'Computation', [sys.executable, 'cluster_fixture.py'], 60),
    ('experimental_constants', '.', [sys.executable, 'Experimental/scripts/verify_all_claims.py'], 30),
]
meta = {'source_commit': '6c12d57', 'source_workers': {
    'Main': '96419eaa2067ea7baedc4608215fa6b6d7c7b6a7',
    'Computation': 'a13efc877eb3d22fc0a59176b1cdef4a74396557',
    'Experimental': '4ea4e8b96eea76b9f045325f9d18229a2157aeb5',
    'Counterexamples': '993019475dc813b2114edb1d3160fcb6ba572967'},
    'cpu_affinity_bit': cpu_bit, 'memory_cap_bytes': 1024**3,
    'memory_limit': 'Lean -M1024 plus monitored private/working set; other jobs monitored',
    'total_cap_seconds': 600, 'mathlib_commit': '56a005855ea17e0b0958f73ec801ae140b0a1679',
    'lean_binary': lean, 'source_hashes': {}}
for p in [*SNAP.rglob('*.py'), original, targeted]:
    key = p.relative_to(SNAP).as_posix() if p.is_relative_to(SNAP) else p.name
    meta['source_hashes'][key] = hashlib.sha256(p.read_bytes()).hexdigest()
(HERE / 'followup_environment.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
results = []
begin = time.monotonic()
for name, wd, argv, limit in jobs:
    limit = min(limit, 600 - (time.monotonic() - begin))
    if limit <= 0:
        results.append({'job': name, 'status': 'not_run_total_time_cap'})
        continue
    status, peak, start_time = 'completed', 0, time.monotonic()
    with (HERE / (name + '.log')).open('w', encoding='utf-8') as out:
        proc = subprocess.Popen(argv, cwd=SNAP / wd, env=env, stdout=out,
                                stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        while proc.poll() is None:
            peak = max(peak, memory_bytes(proc))
            if peak > 1024**3 or time.monotonic() - start_time > limit:
                status = 'memory_cap' if peak > 1024**3 else 'time_cap'
                proc.kill()
                break
            time.sleep(0.25)
        code = proc.wait()
    row = dict(job=name, args=argv, workdir=wd, cap_seconds=limit, status=status,
               exit_code=code, elapsed_seconds=round(time.monotonic()-start_time, 3),
               peak_observed_bytes=peak, log=name+'.log')
    results.append(row)
    print(json.dumps(row), flush=True)
    (HERE / 'followup_jobs.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
