from fractions import Fraction as F
from kk import *
import itertools
exec(open('verify_sec8.py').read().split("# ---------------- (a)")[0])  # reuse kk helpers only
names = ['0','A','B','T','uA','uB','uT']
P = {}
P['0']  = (K(0), K(0))
P['A']  = (kscale(F(1,2), R3), K(F(1,2)))
P['B']  = (kscale(F(1,2), R3), K(F(-1,2)))
P['T']  = (R3, K(0))
u = (K(F(5,6)), kscale(F(1,6), R11))
for nm,g in (('A',P['A']),('B',P['B']),('T',P['T'])):
    P['u'+nm] = (sub(mul(u[0],g[0]),mul(u[1],g[1])), add(mul(u[0],g[1]),mul(u[1],g[0])))
ar,ai = F(35,37), F(12,37); tx,ty = F(-290,250), F(149,250)
brs = encl(40)
def show(x):
    I = kint(x, brs); return "%.10f" % ((float(I[0])+float(I[1]))/2)
print("%-4s %-24s %-24s %-12s %-12s %-14s" % ("g","xi","ups","|z|^2","P","P'"))
for nm in names:
    gx,gy = P[nm]
    hx,hy = add(gx,K(tx)), add(gy,K(ty))
    xi = sub(mul(K(ar),hx), mul(K(ai),hy))
    up = add(mul(K(ai),hx), mul(K(ar),hy))
    l  = add(mul(xi,xi), mul(up,up))
    e3 = sub(kscale(3,mul(xi,xi)), mul(up,up))
    Pp = mul(mul(up,up), mul(e3,e3))
    Pq = mul(mul(mul(l,l),l), mul(sub(ONE,kscale(F(1,4),l)), mul(sub(l,ONE),sub(l,ONE))))
    print("%-4s %-24s %-24s %-12s %-12s %-14s" % (nm, show(xi), show(up), show(l), show(Pp), show(Pq)))
# exact l as a K element
print()
for nm in names:
    gx,gy = P[nm]
    hx,hy = add(gx,K(tx)), add(gy,K(ty))
    xi = sub(mul(K(ar),hx), mul(K(ai),hy)); up = add(mul(K(ai),hx), mul(K(ar),hy))
    l  = add(mul(xi,xi), mul(up,up))
    a0,a1,a2,a3 = l
    print("|z_%-2s|^2 = %s + %s*sqrt3 + %s*sqrt11 + %s*sqrt33" % (nm,a0,a1,a2,a3))
