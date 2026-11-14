"""Exact verification of paper section 8.5/8.6:
   (a) the seven-vertex Moser unit-distance graph of (8.5),
   (b) its non-3-colourability,
   (c) the placement (8.6) and the strict membership certificate of Lemma 8.9 / eq (8.4),
       together with the paper's Table 1 / Table 2 rational certificates.
All arithmetic in K = Q(sqrt3,sqrt11) exactly, or in rigorous rational intervals.
"""
from fractions import Fraction as F
from kk import *
import itertools, sys

log = []
def say(*a):
    s = " ".join(str(x) for x in a)
    log.append(s)
    print(s)

# ---------------- (a) the graph of (8.5) ----------------
# points as pairs (xi,upsilon) of elements of K, identifying C with R^2
P = {}
P['0']  = (K(0), K(0))
P['A']  = (kscale(F(1,2), R3), K(F(1,2)))
P['B']  = (kscale(F(1,2), R3), K(F(-1,2)))
P['T']  = (R3, K(0))
u = (K(F(5,6)), kscale(F(1,6), R11))
for nm, g in (('A',P['A']),('B',P['B']),('T',P['T'])):
    P['u'+nm] = (sub(mul(u[0],g[0]), mul(u[1],g[1])),
                 add(mul(u[0],g[1]), mul(u[1],g[0])))
names = ['0','A','B','T','uA','uB','uT']

def sqdist(p,q):
    dx = sub(p[0],q[0]); dy = sub(p[1],q[1])
    return add(mul(dx,dx), mul(dy,dy))

say("== (a) unit distances among the seven points of (8.5) ==")
edges = []
nonedges = []
for i,j in itertools.combinations(range(7),2):
    d2 = sqdist(P[names[i]], P[names[j]])
    if eq(d2, ONE):
        edges.append((names[i],names[j]))
    else:
        nonedges.append((names[i],names[j],d2))
say("  #unit pairs =", len(edges))
for e in edges: say("    ", e[0], "-", e[1])
say("  #non-unit pairs =", len(nonedges))
for nm,nm2,d2 in nonedges:
    say("    non-unit:", nm, nm2, "  sqdist =", kshow(d2,""))
# the paper's specific claims
say("  |u|^2 = 1 :", eq(add(mul(u[0],u[0]),mul(u[1],u[1])), ONE))
# |T - uT|^2 = 3|1-u|^2 = 3*(1+11)/36 = 1
d = sqdist(P['T'],P['uT'])
say("  |T-uT|^2 =", kshow(d,""), " is 1 :", eq(d,ONE))
# 35^2+12^2 = 37^2
say("  multiplier norm: 35^2+12^2 =", 35*35+12*12, "= 37^2 :", 35*35+12*12==37*37)

# ---------------- (b) non-3-colourability ----------------
say("")
say("== (b) non-3-colourability ==")
E = [(names.index(a),names.index(b)) for a,b in edges]
bad = 0; total = 0
sol = None
for col in itertools.product(range(3), repeat=7):
    total += 1
    if all(col[a]!=col[b] for a,b in E):
        bad += 1; sol = col
say("  colourings tried (3^7) =", total, " proper =", bad)
if bad:
    say("  COUNTEREXAMPLE (proper 3-colouring):", sol)
else:
    say("  => the graph is NOT 3-colourable (exhaustive check)")
# also verify the stated forcing argument
say("  forcing argument check: triangles (0,A,B),(T,A,B) share edge AB;")
say("     triangles (0,uA,uB),(uT,uA,uB) share edge uA-uB;")
tryas = [set([0,1,2]), set([3,1,2]), set([0,5,4]), set([6,5,4])]
tris = [(names.index(a),names.index(b),names.index(c)) for a,b,c in
        [('0','A','B'),('T','A','B'),('0','uA','uB'),('uT','uA','uB')]]
say("     all four are triangles:", all(
    eq(sqdist(P[names[i]],P[names[j]]),ONE) for (i,j,k) in tris for (i2,j2) in [(i,j),(i,k),(j,k)]
    for i,j in [(i2,j2)]))
say("     |T - uT| = 1 (contradiction edge):", eq(sqdist(P['T'],P['uT']),ONE))

# ---------------- (c) placement (8.6) and certificate ----------------
say("")
say("== (c) placement (8.6), Lemma 8.9 certificate ==")
# z_g = ((35+12i)/37) (g + (-290+149i)/250)
# (the typeset formula is z_g = (35+12i)/37 * (g + (-290+149i)/250); the flat-text
#  extraction lost the parentheses.  Verified below against the paper's residual table.)
ar, ai = F(35,37), F(12,37)
br_, bi = F(-290,250), F(149,250)
Z = {}
for nm in names:
    gx, gy = P[nm]
    hx, hy = add(gx, K(br_)), add(gy, K(bi))
    Z[nm] = (sub(mul(K(ar),hx), mul(K(ai),hy)),
             add(mul(K(ai),hx), mul(K(ar),hy)))
brs = encl(40)
say("  brackets: r3 in [%s, %s]" % (float(brs[0][0]), float(brs[0][1])))
say("            r11 in [%s, %s]" % (float(brs[1][0]), float(brs[1][1])))

def iv(x): return kint(x, brs)
def fv(x, d=12):  # display only
    I = iv(x)
    return (float(I[0])+float(I[1]))/2

ok_all = True
say("")
say("  g     xi (approx)   ups (approx)   |z|^2 in            P < P'  ")
rowdata = {}
for nm in names:
    xi, up = Z[nm]
    l  = add(mul(xi,xi), mul(up,up))
    expr3xi2_minus_up2 = sub(kscale(3, mul(xi,xi)), mul(up,up))
    Ppoly = mul(mul(up,up), mul(expr3xi2_minus_up2, expr3xi2_minus_up2))
    l3 = mul(mul(l,l), l)
    oneminus = sub(ONE, kscale(F(1,4), l))
    lm1 = sub(l, ONE)
    Pprime = mul(mul(l3, oneminus), mul(lm1,lm1))
    Il = iv(l); IP = iv(Ppoly); IPp = iv(Pprime)
    rowdata[nm] = (l, Ppoly, Pprime, Il, IP, IPp)
    inopen = ipos(Il) and izerosafe(isub(Il,(F(4),F(4)))) and not izerosafe(isub(Il,(F(1),F(1))))
    # l<4 : (l-(4,4)) strictly negative
    llt4 = ineg(isub(Il,(F(4),F(4))))
    lpos = ipos(Il)
    PltPp = ineg(isub(IP,IPp))
    say("  %-3s  %11.6f  %11.6f   [%.9f,%.9f]   P<0? %s  l<4? %s  0<l? %s"
        % (nm, fv(xi), fv(up), float(Il[0]), float(Il[1]), PltPp, llt4, lpos))
    ok_all = ok_all and lpos and llt4 and PltPp

say("")
say("  ALL SEVEN VERTICES SATISFY 0 < |z|^2 < 4 AND P < P' :", ok_all)

say("")
say("== paper's Table 1/2 rational certificate, re-checked ==")
ta = {  # g: (xi0, ups0, Pplus, Pminusprime)
 '0':('-1.2906','0.1876','0.90','1.35'),
 'A':('-0.6335','0.9414','0.095','0.110'),
 'B':('-0.3092','-0.0045','0.000002','0.00065'),
 'T':('0.3478','0.7493','0.023','0.026'),
 'uA':('-1.1598','1.1790','9.8','19.0'),
 'uB':('-0.3666','0.5700','0.0022','0.024'),
 'uT':('-0.2358','1.5614','12.65','12.9'),
}
tb = {  # g: (by, bH, a, b)
 '0':('0.0353','4.963','1.70','1.71'),
 'A':('0.887','0.319','1.28','1.29'),
 'B':('0.000022','0.287','0.095','0.096'),
 'T':('0.562','0.199','0.682','0.683'),
 'uA':('1.391','2.647','2.73','2.74'),
 'uB':('0.326','0.079','0.459','0.46'),
 'uT':('2.44','2.273','2.493','2.495'),
}
h = F('0.00011')
allok = True
for nm in names:
    xi0 = F(ta[nm][0]); up0 = F(ta[nm][1])
    Pp = F(ta[nm][2]); Pm = F(ta[nm][3])
    by = F(tb[nm][0]); bH = F(tb[nm][1]); a = F(tb[nm][2]); b = F(tb[nm][3])
    xl = (abs(xi0)-h)**2; xu = (abs(xi0)+h)**2
    yl = (abs(up0)-h)**2; yu = (abs(up0)+h)**2
    ll = xl+yl; lu = xu+yu
    H = max(abs(3*xl-yu), abs(3*xu-yl))
    c1 = yu < by
    c2 = H  < bH
    c3 = a  < ll
    c4 = lu < b
    # P <= yu*H^2 < by*bH^2 < P+
    c5 = yu*H*H < Pp
    c6 = by*bH*bH < Pp
    # P' >= ll^3 (1-lu/4) min(|ll-1|,|lu-1|)^2 > a^3(1-b/4)min(|a-1|,|b-1|)^2 > P-'
    d1 = a**3*(1-b/4)*min(abs(a-1),abs(b-1))**2
    c7 = d1 > Pm
    c8 = (0 < a) and (b < 4)
    # interval avoids 1
    c9 = not (ll < 1 < lu)
    # and does the true value lie in the box? recompute exact l and compare
    Il = rowdata[nm][3]
    c10 = (ll <= Il[0]) and (Il[1] <= lu)
    rowok = c1 and c2 and c3 and c4 and c5 and c6 and c7 and c8 and c9 and c10
    allok = allok and rowok
    say("  %-3s yu<by:%d H<bH:%d a<ll:%d lu<b:%d yuH2<P+:%d Pr>P-'_:%d (a,b) in (0,4), 1 excluded:%d box contains true l:%d  -> %s"
        % (nm, c1,c2,c3,c4,c5,c7,c8 and c9,c10, "OK" if rowok else "FAIL"))
say("  Table 1/2 certificate valid for all seven rows:", allok)
say("  P+ < P-' in every row of Table 1:",
    all(F(ta[nm][2]) < F(ta[nm][3]) for nm in names))

say("")
say("== residuals of (8.5)->rounding (paper's displayed dx,dy divided by 710400000000) ==")
res = {'0':(3840000,-23040000),'A':(-29520000,10176000),'B':(-12240000,-22464000),
       'T':(25440000,10752000),'uA':(32043244,-19212795),'uB':(4763244,-27212795),
       'uT':(32966488,-23385590)}
# a* = 1.732055, b* = 3.316625 exact midpoints
astar = F('1.732055'); bstar = F('3.316625')
def mid(nm):
    """z_g with r3->astar, r11->bstar (paper's midpoint substitution)"""
    gx, gy = P[nm]
    def ev(x):
        a0,a1,a2,a3 = x
        return a0 + a1*astar + a2*bstar + a3*astar*bstar
    x0, y0 = ev(gx) + br_, ev(gy) + bi
    return (ar*x0 - ai*y0, ai*x0 + ar*y0)
allok2 = True
for nm in names:
    zx, zy = mid(nm)
    dx = zx - F(ta[nm][0]); dy = zy - F(ta[nm][1])
    pred = (F(res[nm][0], 710400000000), F(res[nm][1],710400000000))
    ok = (dx==pred[0] and dy==pred[1])
    allok2 = allok2 and ok
    say("  %-3s residual match: %s   (dx,dy)=(%s, %s)" % (nm, ok, dx, dy))
say("  all displayed residuals reproduced exactly:", allok2)
zT  = mid('T'); zuT = mid('uT')
dT  = ((zT[0]-zuT[0])**2 + (zT[1]-zuT[1])**2)
say("  |T-uT|^2 with midpoint substitution =", float(dT), " (exact value 1; midpoint error only)")

say("")
say("== summary of assertions ==")
assert len(edges) == 11
assert len(nonedges) == 10
assert all(not eq(d2, ONE) for (_,_,d2) in nonedges)
assert all(not iszero(d2) for (_,_,d2) in nonedges)          # pairwise distinct points
assert bad == 0                                               # not 3-colourable
assert ok_all                                                 # all 7 in the region (8.4), 0<|z|^2<4
assert allok                                                  # Table 1/2 certificate for all 7 rows
assert allok2                                                 # residual table reproduced exactly
assert all(F(ta[nm][2]) < F(ta[nm][3]) for nm in names)       # P+ < P-' every row
say("  ALL ASSERTIONS PASSED")
open("verify_sec8.log","w").write("\n".join(log)+"\n")
