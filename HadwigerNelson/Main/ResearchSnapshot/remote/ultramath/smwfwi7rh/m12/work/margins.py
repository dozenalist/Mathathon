"""Membership margins for the exact rational unit triangles T(t,s) = {(t,s),(t+1,s),(t+1/2,s+sqrt3/2)}
in the sum set E_A + E_B of two palette values of the gamma-avoiding fragmented field."""
import sys; sys.path.insert(0,'work')
from fractions import Fraction as F
from mpmath import mp, mpf, mpc, exp, sqrt, pi, acos, arg, fabs
mp.dps=60

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
    """x: mpf degrees -> distance to the boundary of the arc containing it (or -1)"""
    y = x % 360
    best = mpf(-1)
    for lo,hi in arcs:
        lo=mpf(lo.numerator)/mpf(lo.denominator); hi=mpf(hi.numerator)/mpf(hi.denominator)
        if lo < y < hi: best = max(best, min(y-lo, hi-y))
    return best

def vertex_margin(w, EA, EB):
    """best margin of w in EA+EB   (max over the two decompositions and the two role assignments)"""
    r = fabs(w)
    if r > 2 or r < mpf('1e-50'): return mpf(-1), None
    beta = acos(r/2); a = arg(w); best = mpf(-1); who=None
    for s in (+1,-1):
        th = (a + s*beta)*180/pi
        ph = arg(w - exp(mpc(0,1)*th*pi/180))*180/pi
        m1 = min(margin_in(th,EA), margin_in(ph,EB))
        m2 = min(margin_in(th,EB), margin_in(ph,EA))
        for m,tag in ((m1,'AB'),(m2,'BA')):
            if m > best: best, who = m, (tag, float(th), float(ph))
    return best, who

def tri_margin(t, s, EA, EB):
    t=mpf(t.numerator)/mpf(t.denominator); s=mpf(s.numerator)/mpf(s.denominator)
    s3 = sqrt(3)/2
    V=[mpc(t,s), mpc(t+1,s), mpc(t+mpf(1)/2, s+s3)]
    return [vertex_margin(v,EA,EB) for v in V]

cases = [((F(1,4),F(-7,50)), [1,4],[2,5]),
         ((F(1,4),F(-7,50)), [1,4],[3,5]),
         ((F(1,4),F(-7,50)), [2,4],[3,5]),
         ((F(1,4),F(-7,50)), [2,5],[1,3,4])]
for (t,s),A,B in cases:
    EA=arcs(frozenset(A)); EB=arcs(frozenset(B))
    print("A=%s B=%s  t=%s s=%s"%(A,B,t,s))
    print("   E_A =", [(float(a),float(b)) for a,b in EA])
    print("   E_B =", [(float(a),float(b)) for a,b in EB])
    for v,(m,who) in zip("012", tri_margin(t,s,EA,EB)):
        print("   vertex %s: margin %.4f deg  via %s"%(v,float(m),who))
    print()
