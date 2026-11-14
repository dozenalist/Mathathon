#!/usr/bin/env python3
"""Negative control for `verify_XC017_readable.py`: the verifier must reject what is broken.

A verifier that only ever says "valid" proves nothing.  This script writes three tampered copies
of `X_C017_small.json` and one honest copy into `.scratch/`, runs the reader-facing verifier on
each, and requires

    T1  G[0,1] shifted by 1/1000        -> REJECTED   (identity and/or PSD must fail)
    T2  A[1,1] shifted by 1e-6          -> REJECTED   (identity must fail: L p != 0)
    T3  A[0,1] = 100                    -> REJECTED   (A indefinite)
    T4  unmodified                      -> VALID

T2 is the sharp one: a 1e-6 change in a single diagonal entry is invisible to any float check of
the density (it moves the 7th digit) but breaks the exact identity, which is what the certificate
rests on.

Run: python3 Reviews/negative_control_readable.py      (exit 0 iff all four behave)
"""
import copy, json, os, subprocess, sys
import sympy as sp

base = json.load(open('X_C017_small.json'))
os.makedirs('.scratch', exist_ok=True)

def tamper(name, fn):
    c = copy.deepcopy(base); fn(c); return name, c

cases = [
    tamper("T1 G[0,1] += 1/1000", lambda c: c['G'][0].__setitem__(1, str(sp.Rational(c['G'][0][1]) + sp.Rational(1,1000)))
           or c['G'][1].__setitem__(0, c['G'][0][1])),
    tamper("T2 A[1,1] += 1e-6", lambda c: c['A'][1].__setitem__(1, str(sp.Rational(c['A'][1][1]) + sp.Rational(1,10**6)))),
    tamper("T3 A[0,1] = 100", lambda c: (c['A'][0].__setitem__(1, '100'), c['A'][1].__setitem__(0, '100'))),
    ("T4 unmodified", copy.deepcopy(base)),
]
bad = 0
for name, cert in cases:
    p = '.scratch/' + name.split()[0] + '.json'
    json.dump(cert, open(p, 'w'), indent=1)
    r = subprocess.run([sys.executable, 'verify_XC017_readable.py', p], capture_output=True, text=True)
    want = (name.startswith("T4"))
    ok = (r.returncode == 0) == want
    bad += (not ok)
    print("  [%s] %-22s exit=%d  %s" % ("PASS" if ok else "FAIL", name, r.returncode,
          "VALID" if r.returncode == 0 else "REJECTED"))
print("\nRESULT: %s" % ("verifier has teeth (3 rejections, 1 acceptance)" if not bad else "%d failures" % bad))
sys.exit(0 if not bad else 1)
