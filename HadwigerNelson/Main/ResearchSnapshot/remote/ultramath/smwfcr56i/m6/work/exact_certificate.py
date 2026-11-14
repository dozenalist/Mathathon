"""A decimal-free certificate for Lemma 8.9: for each of the seven placed points
z_g, the exact value P' - P is an element of K = Q(sqrt3, sqrt11); we print its
four rational coordinates together with a strictly positive rational lower bound
obtained from the rational brackets 1732051/1000000 < sqrt3 < 1732051/1000000+1e-6
(verified by exact squaring) and the analogous bracket for sqrt11.
Likewise for 4 - |z_g|^2 and |z_g|^2.
"""
from fractions import Fraction as F
from kk import *
import itertools

names = ['0','A','B','T','uA','uB','uT']
P = {'0': (K(0),K(0)),
     'A': (kscale(F(1,2),R3), K(F(1,2))),
     'B': (kscale(F(1,2),R3), K(F(-1,2))),
     'T': (R3, K(0))}
u = (K(F(5,6)), kscale(F(1,6),R11))
for nm,g in (('A',P['A']),('B',P['B']),('T',P['T'])):
    P['u'+nm] = (sub(mul(u[0],g[0]),mul(u[1],g[1])), add(mul(u[0],g[1]),mul(u[1],g[0])))
ar,ai = F(35,37), F(12,37); tx,ty = F(-290,250), F(149,250)
Z = {}
for nm in names:
    gx,gy = P[nm]
    hx,hy = add(gx,K(tx)), add(gy,K(ty))
    Z[nm] = (sub(mul(K(ar),hx), mul(K(ai),hy)), add(mul(K(ai),hx), mul(K(ar),hy)))

def coords(x):
    a0,a1,a2,a3 = x
    return (a0,a1,a2,a3)

print("Exact rational certificate for Lemma 8.9 (no decimals anywhere).")
print("K = Q(sqrt3,sqrt11), a0 + a1*sqrt3 + a2*sqrt11 + a3*sqrt33.")
print()
rows = []
for nm in names:
    xi, up = Z[nm]
    l  = add(mul(xi,xi), mul(up,up))
    e  = sub(kscale(3,mul(xi,xi)), mul(up,up))
    Pp = mul(mul(up,up), mul(e,e))
    Pq = mul(mul(mul(l,l),l), mul(sub(ONE,kscale(F(1,4),l)), mul(sub(l,ONE),sub(l,ONE))))
    diff = sub(Pq,Pp)
    four_l = sub(K(4), l)
    rows.append((nm,l,diff,four_l))

# --- positivity by rational brackets whose validity is checked by squaring integers ---
def bracket(val, den=10**12):
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    s = Decimal(val.numerator)/Decimal(val.denominator)
    s = s.sqrt()
    lo = F(int(s*den), den)
    hi = lo + F(1,den)
    assert lo*lo <= val <= hi*hi, "bracket invalid"
    assert lo > 0
    return (lo,hi)
I3, I11 = bracket(F(3)), bracket(F(11))
print("brackets (verified by exact squaring):")
print("   %s < sqrt3  < %s   (lo^2 <= 3 <= hi^2 exactly)" % (I3[0], I3[1]))
print("   %s < sqrt11 < %s   (lo^2 <= 11 <= hi^2 exactly)" % (I11[0], I11[1]))
print()
def kint(x):
    a0,a1,a2,a3 = x
    t = (F(a0),F(a0))
    t = iadd(t, imul((F(a1),F(a1)), I3))
    t = iadd(t, imul((F(a2),F(a2)), I11))
    t = iadd(t, imul((F(a3),F(a3)), imul(I3,I11)))
    return t

print("%-4s %-56s %-22s" % ("g","P' - P  as (a0,a1,a2,a3)","lower bound > 0"))
allpos = True
for nm,l,diff,four_l in rows:
    I = kint(diff)
    assert I[0] > 0, (nm, I)
    allpos = allpos and I[0] > 0
    a0,a1,a2,a3 = coords(diff)
    print("%-4s  P'-P > %-50s  (= %.10f)" % (nm, I[0], float(I[0])))
print()
print("P' - P > 0 for all seven vertices (and the lower bounds above are exact")
print("rationals):", allpos)
print()
print("%-4s %-30s %-14s %-14s" % ("g","|z|^2 (a0,a1,a2,a3)","lo(|z|^2)","hi(|z|^2)"))
allbox = True
for nm,l,diff,four_l in rows:
    I = kint(l); F4 = kint(four_l)
    assert I[0] > 0 and F4[0] > 0, (nm, I, F4)
    allbox = allbox and I[0] > 0 and F4[0] > 0
    a0,a1,a2,a3 = coords(l)
    print("%-4s  |z|^2 > %-52s (= %.10f)   and  4-|z|^2 > %s" %
          (nm, I[0], float(I[0]), F4[0]))
print()
print("0 < |z|^2 and |z|^2 < 4 for all seven vertices:", allbox)
