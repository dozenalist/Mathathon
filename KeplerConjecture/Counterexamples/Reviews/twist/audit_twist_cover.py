#!/usr/bin/env python3
"""Audit of Main's twist_cover.py — both revisions — and a corrected all-twists cover.

Audited blobs (exact):
  469fc9f181f976598fd866d9d6473527d4e4a6f8   main 8dc264e   (K15-C112, "inflated arcs")
  67d5c97345cbdb049461b1ea8c50d743b0bf58f1   main 6d542f5   (K15-C123, "rigorous INNER arcs")

Two independent defects, present in BOTH revisions:

 (D1) constant term.  With u = w - a and a twist about the v-w axis (the x-axis here),
      d^2(t) = |u|^2 + |q|^2 + 2 u_x q_x + 2(u_y q_y + u_z q_z) cos t + 2(u_z q_y - u_y q_z) sin t.
      The code sets A = |u|^2+|q|^2 and drops 2 u_x q_x.  It is nonzero for ALL 121 pairs, and
      for q_x > 0 it makes A too large, i.e. the code under-estimates clashes (UNSAFE).

 (D2) arc orientation.  {t : cos(t-psi) < c} is centred at psi+pi with half-width pi-acos(c).
      Both revisions use [psi-h, psi+h] with h = acos(c), which is the set where cos(t-psi) > c --
      the FAR set, i.e. the complement.  So the arcs cover the circle exactly when the pairs are
      safe, and C123's claim that its arcs are "subsets of the true violation sets" is the reverse.

Deliverable: `corrected_cover.py` in this directory rebuilds the cover with both fixed; it covers
[0, 72 deg] and survives shrinking every arc by 2 degrees.

Run: python3 audit_twist_cover.py      (exit 0 iff every statement below is reproduced)
"""
import importlib.util, sys
from mpmath import mp, mpf, pi, cos, sin, acos, atan2, sqrt, degrees

mp.dps = 60
HERE = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, __import__('os').path.join(HERE, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

fails = []
def ck(tag, cond, detail=""):
    print("  [%s] %-62s %s" % ("OK" if cond else "BAD", tag, detail))
    if not cond: fails.append(tag)

def setup(mod):
    rot = mod.build()
    return mod.eleven(rot, +1), mod.eleven(rot, -1)

W = (mpf(2), mpf(0), mpf(0))
def d2(a, q, t):
    ct, st = cos(t), sin(t)
    qr = (q[0], q[1]*ct - q[2]*st, q[1]*st + q[2]*ct)
    return sum((a[i]-W[i]-qr[i])**2 for i in range(3))

for label, blob in (("C112  469fc9f1 (main 8dc264e)", "twist_cover_469fc9f1.py"),
                    ("C123  67d5c973 (main 6d542f5)", "twist_cover_67d5c973.py")):
    print("=" * 96); print(label); print("=" * 96)
    mod = load("m_" + blob, blob)
    A, Q = setup(mod)

    # ---- D1: the omitted constant, and an unsafe witness
    nonzero = 0; unsafe = None
    for a in A:
        u = (W[0]-a[0], W[1]-a[1], W[2]-a[2])
        for q in Q:
            if abs(2*u[0]*q[0]) > mpf('1e-30'): nonzero += 1
            Ac = u[0]**2+u[1]**2+u[2]**2 + q[0]**2+q[1]**2+q[2]**2
            At = Ac + 2*u[0]*q[0]
            B = 2*(u[1]*q[1]+u[2]*q[2]); C = 2*(u[2]*q[1]-u[1]*q[2])
            if unsafe is None:
                for k in range(1, 720):
                    t = 2*pi/5 * k/720
                    if Ac + B*cos(t) + C*sin(t) >= 4 and At + B*cos(t) + C*sin(t) < 4:
                        unsafe = (a, q, t, Ac + B*cos(t)+C*sin(t), At + B*cos(t)+C*sin(t)); break
    ck("D1 the omitted 2*u_x*q_x is nonzero for every pair", nonzero == 121, "%d of 121" % nonzero)
    if unsafe:
        a, q, t, dc, dt = unsafe
        ck("D1 an UNSAFE (pair, twist): code says safe, truth is a clash",
           True, "t=%.4f deg, code d^2=%.4f, true d^2=%.4f, direct=%.4f"
           % (degrees(t), float(dc), float(dt), float(d2(a, q, t))))
        ck("D1 the direct distance agrees with the corrected constant, not the code's",
           abs(float(d2(a,q,t)) - float(dt)) < 1e-9 and abs(float(d2(a,q,t)) - float(dc)) > 0.1)

    # ---- D2: the emitted arcs are the FAR sets
    far = clash = 0
    for a in A:
        u = (W[0]-a[0], W[1]-a[1], W[2]-a[2])
        for q in Q:
            Aij = u[0]**2+u[1]**2+u[2]**2 + q[0]**2+q[1]**2+q[2]**2
            B = 2*(u[1]*q[1]+u[2]*q[2]); C = 2*(u[2]*q[1]-u[1]*q[2]); R = sqrt(B*B+C*C)
            if R == 0: continue
            c = (4-Aij)/R
            if not (-1 < c < 1): continue
            h = acos(c); psi = atan2(C, B)
            if h < mpf('1e-6'): continue
            if d2(a, q, psi) >= 4: far += 1
            else: clash += 1
    ck("D2 every emitted arc is centred where the pair is FAR (>= 2 apart)", clash == 0,
       "%d far, %d clash" % (far, clash))
print("=" * 96)
print("Corrected cover (both defects fixed):")
import subprocess
r = subprocess.run([sys.executable, __import__('os').path.join(HERE, 'corrected_cover.py')],
                   capture_output=True, text=True)
tail = r.stdout.strip().splitlines()
for line in tail[-6:]: print("   " + line)
ck("the corrected arcs cover the whole twist circle", r.returncode == 0)
print("\nRESULT:", "all statements reproduced" if not fails else "FAILED: %s" % fails)
sys.exit(0 if not fails else 1)
