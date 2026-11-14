"""Reproduce submitted Kepler jobs in an isolated copy, with explicit caps.

Usage: python run_checks.py PRIVATE_SNAPSHOT_PARENT
Requires the established numpy/scipy/sympy/mpmath environment. No network.
Windows: one inherited CPU affinity, one BLAS/OpenMP thread, monitored 1 GiB
private/working-set ceiling, <=300 seconds per job and <=600 seconds overall.
"""
import ctypes as ct
from ctypes import wintypes as wt
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
RUN.mkdir(parents=True, exist_ok=True)
if SNAP.exists():
    raise SystemExit('Snapshot already exists; preserve it and inspect before rerunning')
for role in ['Computation', 'Counterexamples', 'Experimental']:
    shutil.copytree(PROJECT / role, SNAP / role,
                    ignore=shutil.ignore_patterns('__pycache__'))

env = dict(os.environ)
env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
kernel = ct.WinDLL('kernel32', use_last_error=True)
kernel.GetCurrentProcess.restype = wt.HANDLE
kernel.GetProcessAffinityMask.argtypes = [wt.HANDLE, ct.POINTER(ct.c_size_t), ct.POINTER(ct.c_size_t)]
kernel.SetProcessAffinityMask.argtypes = [wt.HANDLE, ct.c_size_t]
proc_mask, sys_mask = ct.c_size_t(), ct.c_size_t()
handle = kernel.GetCurrentProcess()
assert kernel.GetProcessAffinityMask(handle, ct.byref(proc_mask), ct.byref(sys_mask))
cpu_bit = proc_mask.value & -proc_mask.value
assert kernel.SetProcessAffinityMask(handle, cpu_bit)

class Memory(ct.Structure):
    _fields_ = [('cb', wt.DWORD), ('PageFaultCount', wt.DWORD)] + [
        (name, ct.c_size_t) for name in ['PeakWorkingSetSize', 'WorkingSetSize',
        'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
        'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage', 'PrivateUsage']]

psapi = ct.WinDLL('psapi', use_last_error=True)
psapi.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ct.POINTER(Memory), wt.DWORD]

def memory_bytes(p):
    counters = Memory()
    counters.cb = ct.sizeof(counters)
    if psapi.GetProcessMemoryInfo(wt.HANDLE(int(p._handle)), ct.byref(counters), counters.cb):
        return max(counters.WorkingSetSize, counters.PrivateUsage)
    return 0

check = str(SNAP / 'Computation/shell_check.py')
jobs = [
    ('sign_helper_counterexamples', '.', [str(HERE / 'reproduce_sign_defects.py'), str(SNAP)], 30),
    ('certificate_K33b', 'Computation', ['verify_certificate.py', 'out/verified_certificate_K33b.json'], 120),
    ('certificate_K33', 'Computation', ['verify_certificate.py', 'out/verified_certificate_K33.json'], 120),
    ('checker_regressions', 'Computation', ['exactcert_tests.py'], 60),
    ('checker_exact_oracle', 'Computation', ['exactcert_oracle.py'], 60),
    ('main_checker_self_test', 'Computation', ['shell_check.py', '--self-test'], 30),
    ('main_checker_adversarial', 'Computation', ['checker_adversarial.py'], 30),
    ('main_cross_K33b', 'Computation', ['verify_comp_cert.py', 'out/verified_certificate_K33b.json'], 120),
    ('tammes_rational_enclosure', '.', ['Experimental/scripts/tammes13_enclosure.py'], 60),
    ('barlow_finite_controls', '.', ['Experimental/scripts/barlow_shell_check.py'], 30),
    ('x_K33_reconstruction', 'Counterexamples/Reviews/K33', ['audit_K33.py'], 30),
    ('x_K33_signs', 'Counterexamples/Reviews/K33', ['audit_K33_signs.py'], 120),
    ('x_tammes_enclosure', 'Counterexamples/Reviews/Tammes13', ['audit_tammes13.py'], 60),
    ('shell_propose_degree9', 'Computation', ['shell_propose.py', '--checker', check, '--degree', '9', '--out', str(RUN / 'shell_propose_degree9.json')], 120),
    ('shell_sos_degree8', 'Computation', ['shell_sos.py', '--checker', check, '--degree', '8', '--out', str(RUN / 'shell_sos_degree8.json')], 120),
]
import numpy, scipy, sympy, mpmath
meta = dict(python=sys.version, numpy=numpy.__version__, scipy=scipy.__version__,
            sympy=sympy.__version__, mpmath=mpmath.__version__, cpu_affinity_bit=cpu_bit,
            memory_cap_bytes=1024**3, total_cap_seconds=600, source_hashes={})
for p in SNAP.rglob('*.py'):
    meta['source_hashes'][p.relative_to(SNAP).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
for p in [SNAP / 'Computation/out/verified_certificate_K33.json', SNAP / 'Computation/out/verified_certificate_K33b.json']:
    meta['source_hashes'][p.relative_to(SNAP).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
(HERE / 'environment.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
start = time.monotonic()
results = []
for name, wd, args, cap in jobs:
    left = 600 - (time.monotonic() - start)
    if left <= 0:
        results.append(dict(job=name, status='not_run_total_time_cap'))
        continue
    cap = min(cap, left)
    began = time.monotonic()
    peak = 0
    status = 'completed'
    with (HERE / (name + '.log')).open('w', encoding='utf-8') as out:
        process = subprocess.Popen([sys.executable, '-u', *args], cwd=SNAP / wd,
                                   env=env, stdout=out, stderr=subprocess.STDOUT,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        while process.poll() is None:
            peak = max(peak, memory_bytes(process))
            if peak > 1024**3 or time.monotonic() - began > cap:
                status = 'memory_cap' if peak > 1024**3 else 'time_cap'
                process.kill()
                break
            time.sleep(0.25)
        code = process.wait()
    row = dict(job=name, workdir=wd, args=args, cap_seconds=cap, status=status,
               exit_code=code, elapsed_seconds=round(time.monotonic()-began, 3),
               peak_observed_bytes=peak, log=name+'.log')
    results.append(row)
    print(json.dumps(row), flush=True)
    (HERE / 'jobs.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
(HERE / 'jobs.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
