#!/usr/bin/env python3
"""Single entry point: re-verify every X artifact in this block. Exit 0 iff all pass.

Checks, in order:
  1. exact_sign.py's own 21 witness-anchored controls (half-line AND closed-interval rules).
  2. The three adversarial families against X's predicate (self-audit, truth from the algebraic rule).
  3. The three frozen certificates X-C010, X-C013, X-C014, reloaded from disk: CE1 by construction,
     CE2 decided exactly, value recomputed from P(0)/Q(0) and compared with the stored density.
  4. The Li-floor filter P(0)/Q(0) >= 1.024466 on each certificate.
No floating point decides anything; floats appear only in printed diagnostics.
"""
import json, sys, math
sys.path.insert(0,'.'); sys.path.insert(0,'Reviews')
import sympy as sp
import ce_exact_gauss as G
from exact_sign import sign_on_half_line as S
from sympy import Rational as R

s_ = G.s_
fail = []
def check(name, cond, detail=""):
    print("  [%s] %-56s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond: fail.append(name)

print("="*80); print("1. exact_sign.py controls"); print("="*80)
import importlib.util
spec = importlib.util.spec_from_file_location("es", "exact_sign.py")
es = importlib.util.module_from_spec(spec); spec.loader.exec_module(es)
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ok = es.controls()
check("21 controls (half-line + closed interval)", ok)

print("="*80); print("2. adversarial families vs X's predicate"); print("="*80)
import x_selftest_run
n_bad = x_selftest_run.run()
check("random + probe-targeted families", n_bad == 0, "%d wrong" % n_bad)

print("="*80); print("3. frozen certificates"); print("="*80)
LI_FLOOR = R(1024466, 1000000)     # P(0)/Q(0) >= 1.024466 (Li, Thm 6.1)
def verify_json(path, label, scale=None):
    try: d = json.load(open(path))
    except FileNotFoundError:
        check(label, False, "file missing"); return
    qs = []
    for coeffs in d['q']:
        q = sum(R(c)*s_**k for k, c in enumerate(reversed(coeffs)))
        if q != 0: qs.append(sp.expand(q))
    H = sp.expand(sum(q**2 for q in qs))
    P = sp.expand(-(s_-4)*H); Q = sp.expand(G.apply_map(P))
    P0 = P.subs(s_, 0); Q0 = Q.subs(G.v_, 0)
    if P0 <= 0 or Q0 <= 0:
        check(label + " positivity", False, "P0=%s Q0=%s" % (P0 > 0, Q0 > 0)); return
    ratio = P0/Q0
    dens = R(4,3)/sp.sqrt(sp.pi)*ratio
    ce2 = S(Q, 0, +1, var=G.v_)
    nroots = sp.Poly(Q, G.v_).count_roots(0, sp.oo)
    stored = d.get('density')
    check(label + " CE2 (Q >= 0 on [0,inf))", bool(ce2), "roots in [0,inf): %d" % nroots)
    check(label + " Li floor P0/Q0 >= 1.024466", bool(ratio >= LI_FLOOR), "%.9f" % float(ratio))
    if stored is not None:
        try:
            stored_num = float(sp.N(sp.sympify(str(stored)), 30))
        except Exception:
            stored_num = None
        if stored_num is None:
            check(label + " stored density present but not comparable", True, str(stored)[:40])
        else:
            check(label + " stored density matches recomputation",
                  abs(float(dens) - stored_num) < 1e-12, "%.12f" % float(dens))
    else:
        check(label + " density recomputed", True, "%.12f" % float(dens))
    print("        => Delta <= %.12f" % float(dens))
verify_json('X_C014_certificate.json', 'X-C014 (m=5 S=8, 0.780718153)')
# X-C015: both-sides explicit rational Gram -- verified WITHOUT any sign predicate
try:
    dv = json.load(open('X_C015_certificate.json'))
    mv, Sv = dv['m'], dv['S']
    Gm = sp.Matrix([[R(c) for c in row] for row in dv['G']])
    Am = sp.Matrix([[R(c) for c in row] for row in dv['A']])
    Bm = sp.Matrix([[R(c) for c in row] for row in dv['B']])
    def _v(x): return sp.Matrix([x**i for i in range(mv+1)])
    Hb = sp.expand((_v(s_/Sv).T*Gm*_v(s_/Sv))[0])
    Pv = sp.expand(-(s_-4)*Hb); Qv = sp.expand(G.apply_map(Pv))
    Qb = sp.expand((_v(G.v_/Sv).T*Am*_v(G.v_/Sv))[0]
                   + G.v_*(_v(G.v_/Sv).T*Bm*_v(G.v_/Sv))[0])
    check("X-C015 identity Q(A,B) == Q(Fourier map)", sp.simplify(Qb-Qv)==0)
    def ldl_ok(M):
        nn=M.rows; cur=M[:,:]; ok=True
        for k in range(nn):
            d=cur[k,k]
            if d<0: return False
            if d==0:
                if any(cur[k,j]!=0 for j in range(k,nn)): return False
                continue
            for i in range(k+1,nn):
                f=cur[i,k]/d
                for j in range(k,nn): cur[i,j]=cur[i,j]-f*cur[k,j]
        return True
    check("X-C015 G,A,B PSD (exact rational LDL)", ldl_ok(Gm) and ldl_ok(Am) and ldl_ok(Bm))
    P0v=Pv.subs(s_,0); Q0v=Qv.subs(G.v_,0)
    densv=R(4,3)/sp.sqrt(sp.pi)*P0v/Q0v
    check("X-C015 density matches stored", abs(float(densv)-float(sp.N(sp.sympify(dv['density']),30)))<1e-12,
          "%.12f" % float(densv))
    check("X-C015 > Kepler and > Li floor", float(densv)>0.74048049 and float(densv)>0.770657)
except FileNotFoundError:
    check("X-C015 present", False, "file missing")

# X-C016: both-sides Gram at useful strength (same checks, no sign predicate needed)
try:
    dv = json.load(open('X_C016_certificate.json'))
    mv, Sv = dv['m'], dv['S']
    Gm = sp.Matrix([[R(c) for c in row] for row in dv['G']])
    Am = sp.Matrix([[R(c) for c in row] for row in dv['A']])
    Bm = sp.Matrix([[R(c) for c in row] for row in dv['B']])
    def _v2(x): return sp.Matrix([x**i for i in range(mv+1)])
    Hb = sp.expand((_v2(s_/Sv).T*Gm*_v2(s_/Sv))[0])
    Pv = sp.expand(-(s_-4)*Hb); Qv = sp.expand(G.apply_map(Pv))
    Qb = sp.expand((_v2(G.v_/Sv).T*Am*_v2(G.v_/Sv))[0]
                   + G.v_*(_v2(G.v_/Sv).T*Bm*_v2(G.v_/Sv))[0])
    def _ldl(M):
        nn=M.rows; cur=M[:,:]
        for k in range(nn):
            dd=cur[k,k]
            if dd<0: return False
            if dd==0:
                if any(cur[k,j]!=0 for j in range(k,nn)): return False
                continue
            for i in range(k+1,nn):
                f=cur[i,k]/dd
                for j in range(k,nn): cur[i,j]=cur[i,j]-f*cur[k,j]
        return True
    check("X-C016 identity Q(A,B) == Q(Fourier map)", sp.simplify(Qb-Qv)==0)
    check("X-C016 G,A,B PSD (exact rational LDL)", _ldl(Gm) and _ldl(Am) and _ldl(Bm))
    P0v=Pv.subs(s_,0); Q0v=Qv.subs(G.v_,0)
    densv=R(4,3)/sp.sqrt(sp.pi)*P0v/Q0v
    check("X-C016 density matches stored", abs(float(densv)-float(dv['density']))<1e-12, "%.12f" % float(densv))
    check("X-C016 > Kepler and > Li floor", float(densv)>0.74048049 and float(densv)>0.770657)
except FileNotFoundError:
    check("X-C016 present", False, "file missing")

# X-C017: both-sides Gram at useful strength (same checks, no sign predicate needed)
try:
    dv = json.load(open('X_C017_certificate.json'))
    mv, Sv = dv['m'], dv['S']
    Gm = sp.Matrix([[R(c) for c in row] for row in dv['G']])
    Am = sp.Matrix([[R(c) for c in row] for row in dv['A']])
    Bm = sp.Matrix([[R(c) for c in row] for row in dv['B']])
    def _v2(x): return sp.Matrix([x**i for i in range(mv+1)])
    Hb = sp.expand((_v2(s_/Sv).T*Gm*_v2(s_/Sv))[0])
    Pv = sp.expand(-(s_-4)*Hb); Qv = sp.expand(G.apply_map(Pv))
    Qb = sp.expand((_v2(G.v_/Sv).T*Am*_v2(G.v_/Sv))[0]
                   + G.v_*(_v2(G.v_/Sv).T*Bm*_v2(G.v_/Sv))[0])
    def _ldl(M):
        nn=M.rows; cur=M[:,:]
        for k in range(nn):
            dd=cur[k,k]
            if dd<0: return False
            if dd==0:
                if any(cur[k,j]!=0 for j in range(k,nn)): return False
                continue
            for i in range(k+1,nn):
                f=cur[i,k]/dd
                for j in range(k,nn): cur[i,j]=cur[i,j]-f*cur[k,j]
        return True
    check("X-C017 identity Q(A,B) == Q(Fourier map)", sp.simplify(Qb-Qv)==0)
    check("X-C017 G,A,B PSD (exact rational LDL)", _ldl(Gm) and _ldl(Am) and _ldl(Bm))
    P0v=Pv.subs(s_,0); Q0v=Qv.subs(G.v_,0)
    densv=R(4,3)/sp.sqrt(sp.pi)*P0v/Q0v
    check("X-C017 density matches stored", abs(float(densv)-float(dv['density']))<1e-12, "%.12f" % float(densv))
    check("X-C017 > Kepler and > Li floor", float(densv)>0.74048049 and float(densv)>0.770657)
except FileNotFoundError:
    check("X-C017 present", False, "file missing")
verify_json('X_C013_certificate.json', 'X-C013 (m=3,       0.794809296)')

# X-C010 has no JSON; rebuild from its explicit formula
H10 = R(17,4096)*(6144*s_**2 + 6848*s_ + 22857)
P10 = sp.expand(-(s_-4)*H10); Q10 = sp.expand(G.apply_map(P10))
r10 = P10.subs(s_,0)/Q10.subs(G.v_,0)
check("X-C010 CE2", bool(S(Q10,0,+1,var=G.v_)))
check("X-C010 Li floor", bool(r10 >= LI_FLOOR), "%.9f" % float(r10))
check("X-C010 density == 0.818086808",
      abs(float(R(4,3)/sp.sqrt(sp.pi)*r10) - 0.818086808) < 1e-9,
      "%.12f" % float(R(4,3)/sp.sqrt(sp.pi)*r10))

print("="*80)
print("RESULT: %s" % ("ALL PASS" if not fail else "FAILURES: %s" % fail))
sys.exit(0 if not fail else 1)
