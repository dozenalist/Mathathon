"""find an exact unit triangle (rational centre c, direction u = e^{i phi}, phi a multiple of 1/2 deg)
inside the sum set of the two values, with large membership margins."""
import sys; sys.path.insert(0,'work')
from fractions import Fraction as F
from mpmath import mp, mpf, mpc, exp, sqrt, pi, acos, arg, fabs
mp.dps=50
WORD = [(0,[1,4]),(1,[1,2,4]),(2,[2,4]),(3,[1,4]),(4,[1,3,4]),(5,[1,3,5]),(6,[2,3,5]),(7,[3,5]),
        (8,[3,5]),(9,[2,5]),(10,[2,5]),(11,[2,4]),(12,[1,4]),(13,[2,4]),(14,[1,4]),(15,[1,3,4]),
        (16,[1,3,4]),(17,[1,3,5]),(18,[2,5]),(19,[3,5]),(20,[2,3,5]),(21,[2,5]),(22,[2,5]),(23,[2,4]),
        (24,[1,3]),(25,[1,4]),(26,[1,4]),(27,[1,3,4]),(28,[1,4]),(29,[1,5]),(30,[2,5]),(31,[3,5]),
        (32,[3,5]),(33,[2,5]),(34,[2,5]),(35,[2,4])]
word=[frozenset(t) for i,t in WORD]
def arcs(val):
    out=[];i=0
    while i<36:
        if word[i]==val:
            j=i
            while j+1<36 and word[j+1]==val: j+=1
            out.append((F(10*i),F(10*(j+1)))); i=j+1
        else: i+=1
    return out
def margin_in(x, arcs):
    y = x % 360; best = mpf(-1)
    for lo,hi in arcs:
        lo=mpf(lo.numerator)/lo.denominator; hi=mpf(hi.numerator)/hi.denominator
        if lo < y < hi: best=max(best, min(y-lo, hi-y))
    return best
def vertex_margin(w, EA, EB):
    r = fabs(w)
    if r > 2 or r < mpf('1e-40'): return mpf(-1)
    beta = degrees = acos(r/2)*180/pi; a = arg(w)*180/pi
    best = mpf(-1)
    for s in (+1,-1):
        th = a + s*beta
        ph = arg(w - exp(mpc(0,1)*th*pi/180))*180/pi
        best = max(best, min(margin_in(th,EA), margin_in(ph,EB)), min(margin_in(th,EB), margin_in(ph,EA)))
    return best
def tri_margin(c, phi_deg, EA, EB):
    u = exp(mpc(0,1)*mpf(phi_deg)*pi/180)
    V=[mpc(c[0],c[1]), mpc(c[0],c[1])+u, mpc(c[0],c[1])+u*exp(mpc(0,1)*pi/3)]
    return [vertex_margin(v,EA,EB) for v in V]
A=frozenset({1,4}); B=frozenset({2,5})
EA=arcs(A); EB=arcs(B)
print("E_A =", [(float(a),float(b)) for a,b in EA])
print("E_B =", [(float(a),float(b)) for a,b in EB])
best=None
for cx in [F(-53,100)+F(k,100) for k in range(0,4)]:
    pass
import itertools
for cx in [F(-52+k,100) for k in range(-2,3)]:
    for cy in [F(-4+k,100) for k in range(-3,3)]:
        for k in range(0,360,2):                      # phi in 0..360 step 2 deg
            ms = tri_margin((mpf(cx.numerator)/cx.denominator, mpf(cy.numerator)/cy.denominator), k, EA, EB)
            m = min(ms)
            if m>0 and (best is None or m>best[0]):
                best=(m,cx,cy,k,ms)
print("best:", None if best is None else (float(best[0]), str(best[1]), str(best[2]), best[3], [float(x) for x in best[4]]))
