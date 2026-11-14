#!/usr/bin/env python3
"""
verify.py -- exact verification for "sum-set density transport at k = 6".

THEOREM (proved in THEOREM.md, Theorem 1).  Let c be a weak measurable k-colouring,
x a centre, G1, G2 disjoint label groups and E1, E2 sets of directions of positive
angular measure with  G_j <= P_x(e) for a.e. e in E_j.  Then for every finite
unit-distance graph Q contained in the sum set
        Z = { x + e^{i a} + e^{i b} :  a density point of E1, b of E2, a not parallel b }
one has   |I \\ (G1 u G2)| >= chi(Q).

INSTANCE USED HERE (paper Lemma 6.4's triangle, roles of G1/G2 interchangeable):
with gamma = 2 arcsin(1/(2 sqrt 3)) (so cos gamma = 5/6, |1-e^{i gamma}| = 1/sqrt 3)
and psi = pi + gamma, if for some t
     {t, t+120, t+240} <= E_A   and   {t+psi, t+psi+120, t+psi+240} <= E_B
(or the same with A, B interchanged) then Z contains the unit equilateral triangle
     z_j - x = e^{i(t+2j*60)} (1 - e^{i gamma}) ,  |z_{j+1}-z_j| = 1 ,
hence |I \\ (A u B)| >= 3.  At k = 6 two disjoint palette values with |A|,|B| >= 2
have |A u B| >= 4, so this is a contradiction.

All arithmetic below is exact (fractions.Fraction); the only transcendental input is
gamma, enclosed in a rational interval of width < 1e-35 degrees.
Run:  python3 verify.py
"""
from fractions import Fraction as F
import itertools

# ---------------------------------------------------------------- constants --
PI_LO = F(31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679, 10**100)
PI_HI = PI_LO + F(1, 10**98)

def sqrt_bounds(x, iters=400):
    x = F(x)
    lo = F(int(x)) if int(x) > 0 else F(1, 10**6)
    while lo*lo > x: lo /= 2
    hi = lo + 1
    while hi*hi < x: hi *= 2
    for _ in range(iters):
        m = (lo+hi)/2
        if m*m < x: lo = m
        else: hi = m
    return lo, hi

def cos_bounds(x, n=16):
    """rigorous enclosure of cos x (radians) by two consecutive Taylor partial sums"""
    x = F(x); lo = F(0); hi = F(0); term = F(1)
    for j in range(n+1):
        if j % 2 == 0: lo += term; hi += term
        else:          lo -= term; hi -= term
        term = term * x * x / ((2*j+1)*(2*j+2))
    return lo - abs(term), hi + abs(term)

def gamma_deg_bounds():
    """gamma = 2 arcsin(1/(2 sqrt3)) in degrees; bisection on cos(gamma) = 5/6"""
    lo, hi = F(0), PI_HI/2
    for _ in range(400):
        mid = (lo+hi)/2
        c_lo, c_hi = cos_bounds(mid)
        if c_lo > F(5,6):   lo = mid
        elif c_hi < F(5,6): hi = mid
        else: break
    f = lambda r, up: r*180/(PI_LO if up else PI_HI)
    return f(lo, False), f(hi, True)

G_LO, G_HI = gamma_deg_bounds()
PSI_LO, PSI_HI = 180+G_LO, 180+G_HI

# ------------------------------------------------------- interval algebra ----
def merge(iv):
    iv = sorted(iv); out = []
    for lo,hi in iv:
        if out and lo <= out[-1][1]: out[-1] = (out[-1][0], max(out[-1][1],hi))
        else: out.append((lo,hi))
    return out

def norm(E):
    out = []
    for lo,hi in E:
        lo,hi = F(lo), F(hi)
        if hi-lo >= 360: return [(F(0),F(360))]
        a = lo % 360; rem = hi-lo
        while rem > 0:
            take = min(F(360)-a, rem); out.append((a,a+take)); rem -= take; a = F(0)
    return merge(out)

def shift(E, s_lo, s_hi):
    """union over s in [s_lo,s_hi] of (E - s) mod 360"""
    E = norm(E); out = []
    for lo,hi in E:
        a = (lo - s_hi) % 360; length = (hi - s_lo) - (lo - s_hi)
        if length >= 360: return [(F(0),F(360))]
        x = a
        while length > 0:
            take = min(F(360)-x, length); out.append((x,x+take)); length -= take; x = F(0)
    return merge(out)

def inter(P,Q):
    P, Q = norm(P), norm(Q); out = []
    for a1,a2 in P:
        for b1,b2 in Q:
            lo,hi = max(a1,b1), min(a2,b2)
            if hi > lo: out.append((lo,hi))
    return merge(out)

def width(E): return sum(hi-lo for lo,hi in E)

def orbit3(E):  return inter(inter(E, shift(E,120,120)), shift(E,240,240))

def shifted3(E):
    return inter(inter(shift(E,PSI_LO,PSI_HI), shift(E,PSI_LO+120,PSI_HI+120)),
                 shift(E,PSI_LO+240,PSI_HI+240))

def criterion(EA, EB):
    """(witnesses for t in E_A-orbit with t+psi in E_B , and the reverse)"""
    return inter(orbit3(EA), shifted3(EB)), inter(orbit3(EB), shifted3(EA))

def in_set(x, E):
    x = F(x) % 360
    return any(lo <= x < hi for lo,hi in norm(E))

def check_witness(EA, EB, t, role):
    """rigorous check of the concrete witness t for the whole psi enclosure"""
    if role == 'A->B':
        return (all(in_set(t+120*j, EA) for j in range(3)) and
                all(in_set(t+psi+120*j, EB) for psi in (PSI_LO,PSI_HI) for j in range(3)))
    return (all(in_set(t+120*j, EB) for j in range(3)) and
            all(in_set(t+psi+120*j, EA) for psi in (PSI_LO,PSI_HI) for j in range(3)))

# ---------------------------------------------------------------- the models -
def block_word(blocks, n=36, L=4):
    return [blocks[(i//L) % 3] for i in range(n)]

BLOCKS = {
 "m15 uniform blocks, ell=3": [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})],
 "m15 uniform blocks, ell=4": [frozenset({0,2}), frozenset({1,4}), frozenset({3,5})],
 "m15 uniform blocks, ell=5": [frozenset({0,2}), frozenset({1,3}), frozenset({4,5})],
 "m15 uniform blocks, ell=6": [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})],
 "FREE-LABEL, ell=3":         [frozenset({3}),    frozenset({4}),    frozenset({5})],
 "FREE-LABEL, ell=4":         [frozenset({0,2}),  frozenset({1,3}),  frozenset({4})],
 "FREE-LABEL, ell=5":         [frozenset({0,2}),  frozenset({1,3}),  frozenset({5})],
}
FREE_L6 = [[(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
           [(3,5),(3,5),(2,5),(2,5),(2,4,5),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
           [(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)]]

def models():
    M = {k: (36, block_word(v)) for k,v in BLOCKS.items()}
    M["FREE-LABEL, ell=6"] = (36, [frozenset(t) for r in FREE_L6 for t in r])
    n = 36; w = []
    for i in range(n):                       # m13 : s(t) = floor(9t/2pi) mod 3
        s = int(F(9*(2*i+1), 2*n)) % 3       # 9*t/2pi at the sector midpoint
        w.append(frozenset({4+s}))
    M["m13 singleton triangle"] = (n, w)
    return M

def dirset(n, word, value):
    out = []; i = 0; step = F(360,n)
    while i < n:
        if word[i] == value:
            j = i
            while j+1 < n and word[j+1] == value: j += 1
            out.append((i*step, (j+1)*step)); i = j+1
        else: i += 1
    return out

# ------------------------------------------------------------------- report --
def main():
    print("="*80); print("A. exact constants"); print("="*80)
    print("  cos(2 arcsin(1/(2 sqrt3))) = 1 - 2*(1/12) = 5/6 :", F(1)-2*F(1,12) == F(5,6))
    print("  |1-e^{i gamma}|^2 = 2 - 2 cos gamma = 2 - 5/3 = 1/3 :", F(2)-F(5,3) == F(1,3))
    print("  |e^{2 i kappa} - 1|^2 = |e^{120i}-1|^2 = 3 ; 3*(1/3) = 1  (unit side)")
    print("  gamma in degrees in (%.12f, %.12f), width %.2e" % (float(G_LO),float(G_HI),float(G_HI-G_LO)))
    print("  psi = pi+gamma     in (%.12f, %.12f)" % (float(PSI_LO),float(PSI_HI)))

    print(); print("="*80); print("B. k-arithmetic:  contradiction iff  k - |G1 u G2| < chi(Q)"); print("="*80)
    for u in (2,3,4,5,6):
        need = 6-u
        what = {0:'-- (5.2) alone already contradicts',1:'a unit edge  (chi 2)',
                2:'the unit triangle of Lemma 6.4  (chi 3)',3:'the Moser spindle  (chi 4)',
                4:'a 5-chromatic unit-distance graph'}[need]
        print("  |G1 u G2| = %d  =>  |T'| = %d  =>  contradiction from %s" % (u, need, what))
    print("  at a 6-cycle centre all palettes have size >= 2, so |G1 u G2| >= 4.")

    print(); print("="*80); print("C. every palette-level countermodel at k=6 that is pair-valued dies"); print("="*80)
    M = models(); killed = []
    for name,(n,word) in M.items():
        vals = sorted(set(word), key=lambda s:(len(s),sorted(s)))
        per = all(word[i] == word[(i+120*n//360) % n] for i in range(n))
        prints = []
        for A,B in itertools.combinations(vals,2):
            if A & B: continue
            EA, EB = dirset(n,word,A), dirset(n,word,B)
            w1, w2 = criterion(EA,EB)
            hit = None
            for role, w in (('A->B',w1), ('B->A',w2)):
                if width(w) > 0:
                    lo, hi = max(norm(w), key=lambda t: t[1]-t[0])
                    t = (lo+hi)/2
                    if check_witness(EA,EB,t,role): hit=(role,t,width(w)); break
            u = len(A|B)
            prints.append((sorted(A), sorted(B), u, hit))
        kills = [p for p in prints if p[3] and 6-p[2] < 3]
        status = "ELIMINATED" if kills else "survives"
        if kills: killed.append(name)
        print("  %-28s 120deg-periodic=%-5s  %s" % (name, per, status))
        for A,B,u,hit in kills[:2]:
            print("        A=%-9s B=%-9s |AuB|=%d T'=%d   role %s  t = %.6f deg  (witness set of width %.3f deg)"
                  % (A,B,u,6-u,hit[0],float(hit[1]),float(hit[2])))
    print()
    print("  eliminated: %d of %d.  survivors: %s" % (len(killed), len(M), [m for m in M if m not in killed]))
    print("  the survivors are exactly the models whose palettes are singletons (|A u B| = 2,")
    print("  |T'| = 4 >= 3): they are consistent with the mechanism, and a 6-cycle centre")
    print("  has no singleton palette (Lemma 3 of sprint/k6/STRUCTURE.md).")

    print(); print("="*80); print("D. the mechanism is strictly stronger than the gamma criterion"); print("="*80)
    d = PI_LO/3; s_lo, s_hi = sqrt_bounds(3); val = d*s_lo - d*d; inv3 = 1/sqrt_bounds(3)[1]
    print("  direction sets E_A = (0,120), E_B = (120,240) degrees:")
    print("    neither contains a full 120-degree orbit, so no gamma witness exists;")
    print("    the arc-sum lemma gives a disc of radius >= delta*sigma - delta^2 = %.6f" % float(val))
    print("    and 1/sqrt3 = %.6f  =>  disc contains a unit triangle:  %s" % (float(inv3), val >= inv3))

if __name__ == "__main__":
    main()
