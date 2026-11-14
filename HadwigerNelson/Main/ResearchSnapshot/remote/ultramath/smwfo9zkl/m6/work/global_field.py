#!/usr/bin/env python3
"""
GLOBAL witness: a measurable (piecewise constant) palette field on the whole
circle of directions that satisfies the strip layer at EVERY direction.

Construction (k >= 6, any ell, and (5,3), (5,4)):
   p = floor(ell/2);   v_i = e^{i pi/3} for i < p,   v_i = e^{i 4 pi/3} for i >= p
   arcs A_r = (r*pi/3, (r+1)*pi/3),  r = 0..5
   Phi(u) = P  if u in A_r with r even,   Q  if r odd
with (P,Q) as in the closed form of verify.py:
   (A) k-ell >= 2 :  P = {k-2},      Q = {k-1}
   (B) k-ell == 1 :  P = {k-1},      Q = {1,p+1}
   (C) ell == k   :  P = {1,p+1},    Q = {2,p+2}

Why it works: u . v_i > 0 iff u lies in the open semicircle centred at arg v_i,
so for u in either of the two semicircles determined by the v_i the positive
edges are {i < p} or {i >= p}; the strip sets O(u), I(u) are then
{p+1,...,k-1} and {1,...,p-1} u {ell,...,k-1} in one order or the other, and
condition S2 ("meet O and meet I") is the same condition in both cases.  R
shifts the arc index by exactly one, so Phi(Ru) is the *other* member of the
disjoint pair (P,Q), which gives S3.

Angles are Fractions of pi, so every sign decision is exact.
"""
from fractions import Fraction as F
import sys

def cosign(t, phi):
    """sign of cos(pi*(t - phi)), t, phi rational multiples of pi (mod 2)."""
    d = (t - phi) % 2
    if d == F(1, 2) or d == F(3, 2):
        raise ValueError("direction perpendicular to some v_i")
    return 1 if (d < F(1, 2) or d > F(3, 2)) else -1

def global_field(k, ell):
    p = ell // 2
    if k - ell >= 2:
        P, Q = frozenset({k - 2}), frozenset({k - 1})
    elif k - ell == 1:
        P, Q = frozenset({k - 1}), frozenset({1, p + 1})
    else:
        P, Q = frozenset({1, p + 1}), frozenset({2, p + 2})
    phi = [F(1, 3)] * p + [F(4, 3)] * (ell - p)
    def Phi(t):
        r = int((3 * t) % 6)              # arc index of u
        return P if r % 2 == 0 else Q
    return Phi, phi, P, Q, p

def strip_sets(k, ell, phi, t):
    pos, neg = set(), set()
    for i in range(ell):
        ends = {i, (i + 1) % ell}
        if cosign(t, phi[i]) > 0:
            pos |= ends
        else:
            neg |= ends
    return frozenset(set(range(k)) - pos), frozenset(set(range(k)) - neg)

def check_global(k, ell, N=13, verbose=False):
    """Check at all t = m/(3N) for m = 0..6N-1 that are not arc boundaries."""
    Phi, phi, P, Q, p = global_field(k, ell)
    n_ok = 0
    fails = []
    for m in range(6 * N):
        t = F(m, 3 * N)
        if (3 * t) % 1 == 0:               # arc boundary: measure zero, skip
            continue
        O, I = strip_sets(k, ell, phi, t)
        Pu, Pv = Phi(t), Phi(t + F(1, 3))
        bad = []
        if not O or not I:
            bad.append("S0")
        if not 1 <= len(Pu) <= k - 3:
            bad.append("S1")
        if not Pu & O:
            bad.append("S2/O")
        if not Pu & I:
            bad.append("S2/I")
        if Pu & Pv:
            bad.append("S3")
        for a in range(ell):
            if Pu <= {a, (a + 1) % ell}:
                bad.append("S4")
        if bad:
            fails.append((str(t), bad))
        else:
            n_ok += 1
    return n_ok, fails

if __name__ == "__main__":
    print("GLOBAL palette field: constraints checked at every non-boundary direction")
    print("of a mesh of 6N equally spaced directions (exact rational angles).\n")
    N = 61
    for k in (5, 6):
        for ell in range(3, k + 1):
            n_ok, fails = check_global(k, ell, N=N)
            tot = n_ok + len(fails)
            print(f"  k={k} ell={ell}: {n_ok}/{tot} directions satisfy S0-S4"
                  + ("" if not fails else f"   FAILURES at {fails[:3]}"))
    print("\n  (k=5 ell=5 must fail: STRIP(5,5) is unsatisfiable -- Proposition 8.2.)")
    print("  (everything else, in particular every ell at k=6, holds at every sampled direction.)")
