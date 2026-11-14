"""Bounded smoke checks for worker repairs arriving during hourly publication.

These executions do not certify the repaired verifier or the shell theorem.
Run with NumPy, SciPy, SymPy and mpmath available; one BLAS/OpenMP thread.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
env = dict(os.environ)
env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
jobs = [
    ('checker_regressions', 'Computation', ['exactcert_tests.py'],
     '8bb50f857916ba986f42690b0ec081edebc4efdc', 120),
    ('shell_float_diagnostic', 'Experimental', ['scripts/shell_2p09_interval.py'],
     '96fbf9bbcb6eef18b9f56ec926f226a6473fc22d', 20),
    ('gaussian_one_iteration', 'Counterexamples', ['x_r01_driver.py', '6', '1'],
     '3831361a0b4d9366597c82191e78327eee96e404', 60),
    ('gaussian_comparison_regression', 'Counterexamples', ['-c',
     'import sympy as s; import x_r01_driver as D; '
     'p=s.Rational(99,100); q=s.Integer(1); '
     'print("input:",p,q); print("submitted helper:",D.kepler_ok(p,q)); '
     'print("exact lhs:",32*p*p); print("pi cubed:",s.N(s.pi**3,30)); '
     'print("correct comparison:",bool(32*p*p < s.pi**3)); '
     'assert D.kepler_ok(p,q) != bool(32*p*p < s.pi**3)'],
     '3831361a0b4d9366597c82191e78327eee96e404', 20),
]
results = []
for name, wd, args, source, cap in jobs:
    started = time.monotonic()
    log = HERE / (name + '.log')
    with log.open('w', encoding='utf-8') as out:
        try:
            p = subprocess.run([sys.executable, *args], cwd=PROJECT / wd,
                               env=env, stdout=out, stderr=subprocess.STDOUT,
                               timeout=cap, check=False)
            code, status = p.returncode, 'completed'
        except subprocess.TimeoutExpired:
            code, status = None, 'timed_out'
            out.write('\nLOCAL TIME CAP REACHED\n')
    item = dict(job=name, source_commit=source, args=args,
                workdir='KeplerConjecture/' + wd, cap_seconds=cap,
                exit_code=code, status=status,
                elapsed_seconds=round(time.monotonic()-started, 3),
                log=log.name)
    results.append(item)
    print(json.dumps(item), flush=True)
    (HERE / 'jobs.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
