#!/usr/bin/env python3
"""Read X-C017 from disk and check it out loud, with no sign predicate anywhere.

Usage:  python3 verify_XC017_readable.py [certificate.json]

Works on any both-sides Gram certificate in this directory (X_C015, X_C016, X_C017,
X_C017_small); the stored `density` may be a string or a number.

Why this script exists.  Every other X certificate needs a decision about the sign of a
polynomial on an interval, and every sign tester in this project has been unsound at least
once (shell_check.py: a8526a8 -> 5619c1d -> 812105c3 -> 909a50a).  X-C017 needs none: the
two conditions that make it a certificate are

  (CE1)  P = -(s-4)H  with  H = sum of squares          (so P >= 0 on [0,4] and P < 0 after 4)
  (CE2)  Q >= 0 on [0,inf)

and both are *witnessed by positive semidefinite Gram matrices*, so they are decided by
rational LDL^T factorisation -- finite arithmetic on exact rationals, no root isolation, no
sampling, no probes.  That is the whole point of the both-sides Gram form:

    H(s) = v(s/S)^T G v(s/S) >= 0                       for every real s, if G >= 0
    Q(w) = v(w/S)^T A v(w/S) + w v(w/S)^T B v(w/S) >= 0 for every w >= 0, if A,B >= 0

where v(x) = (1,x,...,x^m).  The remaining obligation is an *identity*, checked by expansion:

    Q  ==  Fourier map of P            (P(s) -> Q(w),  f = P(s)e^{-s},  f^ = pi^{3/2}Q(w)e^{-w})

Nothing else is assumed.  The density follows from  (4/(3 sqrt pi)) P(0)/Q(0)  and the
comparison with pi/sqrt18 is the exact directed test in ce_exact_gauss.kepler_ok.
"""
import json, sys
import sympy as sp
from sympy import Rational as R
import ce_exact_gauss as G

path = sys.argv[1] if len(sys.argv) > 1 else 'X_C017_certificate.json'
d = json.load(open(path))
m, S = d['m'], d['S']
stored = sp.N(sp.sympify(d['density']), 20)     # some files store a formula, e.g. over sqrt(pi)
print("certificate: %s   (m=%d, S=%d, stored density %s)" % (path, m, S, sp.N(stored, 12)))
v = lambda x: sp.Matrix([x**i for i in range(m+1)])
M = {k: sp.Matrix([[R(c) for c in row] for row in d[k]]) for k in ('G','A','B')}

print("\n[1] symmetric?  G %s  A %s  B %s" % tuple(
    "yes" if Mk == Mk.T else "NO" for Mk in (M['G'], M['A'], M['B'])))

print("\n[2] positive semidefinite, by rational LDL^T (printed pivot by pivot)")
def ldl(Mx, name):
    cur = Mx[:,:]; nn = Mx.rows; ok = True
    piv = []
    for k in range(nn):
        dd = cur[k,k]; piv.append(dd)
        if dd < 0: ok = False
        if dd == 0:
            if any(cur[k,j] != 0 for j in range(k,nn)): ok = False
            continue
        for i in range(k+1,nn):
            f = cur[i,k]/dd
            for j in range(k,nn): cur[i,j] -= f*cur[k,j]
    print("    %s: pivots %s  -> %s" % (name, [str(p) for p in piv], "PSD" if ok else "NOT PSD"))
    return ok
psd = all(ldl(M[k], k) for k in ('G','A','B'))

print("\n[3] the identity  v^T A v + w v^T B v  ==  Fourier(P),  P = -(s-4) v(s/S)^T G v(s/S)")
H = sp.expand((v(G.s_/S).T*M['G']*v(G.s_/S))[0])
P = sp.expand(-(G.s_-4)*H)
Q = sp.expand(G.apply_map(P))
Qab = sp.expand((v(G.v_/S).T*M['A']*v(G.v_/S))[0] + G.v_*(v(G.v_/S).T*M['B']*v(G.v_/S))[0])
ident = sp.expand(Qab - Q) == 0
print("    deg H = %d, deg P = %d, deg Q = %d;  difference is %s"
      % (sp.Poly(H, G.s_).degree(), sp.Poly(P, G.s_).degree(), sp.Poly(Q, G.v_).degree(),
         "identically zero" if ident else str(sp.expand(Qab-Q))))

print("\n[4] the density")
P0, Q0 = P.subs(G.s_, 0), Q.subs(G.v_, 0)
print("    P(0) = %s" % P0); print("    Q(0) = %s" % Q0)
print("    P(0)/Q(0) = %s" % (R(P0)/R(Q0)))
dens = float(R(4,3)/sp.sqrt(sp.pi)*R(P0)/R(Q0))
print("    density = (4/(3 sqrt pi)) P(0)/Q(0) = %.12f" % dens)

print("\n[5] what this does and does not claim")
kok = G.kepler_ok(R(P0), R(Q0))
print("    density < pi/sqrt18 (i.e. would this prove Kepler)?  %s   [Kepler = 0.740480490]" % ("yes" if kok else "NO"))
print("    density > Li's floor 0.770657 (a CE certificate below it would be a bug)?  %s"
      % ("yes" if dens > 0.770657 else "NO"))
print("    => this is a bound  delta <= %.6f, WEAKER than Kepler; it is NOT a Kepler proof." % dens)

valid = psd and ident and P0 > 0 and Q0 > 0 and (dens > 0.770657)
print("\nVERDICT: %s" % ("VALID CE CERTIFICATE" if valid else "REJECTED"))
sys.exit(0 if valid else 1)
