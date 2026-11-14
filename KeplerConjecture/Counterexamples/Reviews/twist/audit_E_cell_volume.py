#!/usr/bin/env python3
"""Audit of E's rigorous_cell_volume.py at experimental d289bef (blob d015a2e1e322853286322ff2c6ec4a5a88f03550).

Two defects, both reproduced here on E's own code:

 (V1) NORM.  The slack for the unit-normal perturbation is computed as
          e = max((x.hi - x.lo)/2 for x in n)      # componentwise
          slack = R*e + f
      but the inclusion {y.n' <= b' - slack} subset Omega needs |y.(n-n')| <= R*||n-n'||_2,
      and ||.||_2 can exceed ||.||_inf by up to sqrt 3.  Exact witness: n0=(1,0,0),
      n=(3/5,4/5,0), y=(-4/9,8/9,0), R=1: ||n-n0||_inf = 4/5 but y.(n-n0) = 8/9 > 4/5, with
      |y| = 0.9938 < 1.  So the allowance is smaller than the perturbation it must absorb.

 (V2) BOUNDEDNESS.  polytope_volume accepts any body with >= 4 feasible triple-plane vertices
      and never checks that the body is bounded; sandwich's R-check inspects only the vertices it
      found, so an unbounded body passes vacuously.  Exact witness: centres
      (+-2,0,0), (0,+-2,0), (0,0,-2) give the cell {|x|<=1, |y|<=1, z>=-1}, which has the
      recession ray (0,0,1) and INFINITE volume; E's sandwich(R=2) returns {4/3} as both the
      lower and the upper bound.

Also checks the two controls that do pass (fcc/hcp 4sqrt2), so the audit separates "the machinery
is exact" from "the enclosure is valid".

Run: python3 audit_E_cell_volume.py     (exit 0 iff every statement is reproduced)
"""
import importlib.util, math, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

m = load("ecv", "E_rigorous_cell_volume_d015a2e.py")
Iv = m.Iv
fails = []
def ck(tag, cond, detail=""):
    print("  [%s] %-60s %s" % ("OK" if cond else "BAD", tag, detail))
    if not cond: fails.append(tag)

print("=" * 96); print("V1  componentwise error used where the Euclidean norm is needed"); print("=" * 96)
n0 = [F(1), F(0), F(0)]
n  = [F(3, 5), F(4, 5), F(0)]
d  = [n[i]-n0[i] for i in range(3)]
y  = [F(-4, 9), F(8, 9), F(0)]
e_inf = max(abs(x) for x in d)
e_2 = math.sqrt(sum(float(x)**2 for x in d))
y_dot = sum(y[i]*d[i] for i in range(3))
y_norm = math.sqrt(sum(float(x)**2 for x in y))
print("  n - n0 = %s ; ||.||_inf = %s ; ||.||_2 = %.6f" % ([str(x) for x in d], e_inf, e_2))
print("  y = %s ; |y| = %.6f (R = 1 covers it)" % ([str(x) for x in y], y_norm))
print("  y.(n - n0) = %s = %.6f  >  R*||.||_inf = %.6f" % (y_dot, float(y_dot), float(e_inf)))
ck("V1 a legal y moves the half-space further than the code's slack",
   y_dot > e_inf and y_norm < 1)
print("  (the code sums R*e with e componentwise: `slacks.append(R * eq + fq)`)")

print("=" * 96); print("V2  an unbounded cell gets a finite 'certified' enclosure"); print("=" * 96)
centres = [(Iv(2), Iv(0), Iv(0)), (Iv(-2), Iv(0), Iv(0)),
           (Iv(0), Iv(2), Iv(0)), (Iv(0), Iv(-2), Iv(0)),
           (Iv(0), Iv(0), Iv(-2))]
out = m.sandwich(centres, F(2))
lo, hi = out[0], out[1]
print("  sandwich returned [%s, %s] with %d/%d vertices" % (float(lo), float(hi), out[2], out[3]))
print("  the true cell is {|x| <= 1, |y| <= 1, z >= -1}: recession ray (0,0,1), volume = +infinity")
ck("V2 a finite upper bound is returned for an infinite-volume cell", hi < 10**6,
   "upper bound %s" % float(hi))
ck("V2 and the returned value is the pyramid volume 4/3, not an error", abs(float(hi) - 4/3) < 1e-9)
print("  (polytope_volume never tests boundedness; sandwich's R-check looks only at the vertices")
print("   it found, so an unbounded body passes it vacuously)")

print("=" * 96); print("the exactness that does work: the fcc control"); print("=" * 96)
P = m.barlow_contact_cell("fcc")
vi, vo, ni, no = m.sandwich(P, F(2))
ref = 4*math.sqrt(2)
ck("fcc cell enclosed and contains 4 sqrt2", float(vi) <= ref <= float(vo),
   "[%.12f, %.12f]" % (float(vi), float(vo)))

print("=" * 96); print("what a repair must satisfy (the five requirements)"); print("=" * 96)
reqs = [
 ("boundedness", "polytope_volume must PROVE the body is bounded (e.g. a positive combination of "
                 "the normals equal to 0, or accept a ball constraint |y| <= R and check it), not "
                 "merely find 4 vertices"),
 ("norm choice", "the perturbation slack must be R*||n - n'||_2 <= R*sqrt(3)*max_component, or the "
                 "normal must be renormalised so that the two agree"),
 ("radius bootstrap", "R must be an a-priori bound on the cell that does not depend on the vertex "
                      "enumeration; with the B(w,2) constraint available, R = 2 is provable "
                      "independently, and the outer polytope must include it"),
 ("inner inclusion", "the inner polytope's half-spaces must use the Euclidean slack; and the "
                     "lower bound must be 0 when the inner polytope is empty"),
 ("exact domain coverage", "a bound on ONE cell for ONE configuration is not a bound over "
                           "completions; the branch-and-bound must cover the parameter domain "
                           "exactly, including its boundary"),
]
for name, text in reqs:
    print("  - %-22s %s" % (name, text))
print("\nRESULT:", "both defects reproduced on E's code" if not fails else "FAILED: %s" % fails)
sys.exit(0 if not fails else 1)
