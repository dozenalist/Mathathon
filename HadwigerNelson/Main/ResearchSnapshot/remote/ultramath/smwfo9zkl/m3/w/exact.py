from fractions import Fraction as F
import itertools, math
# exact Eisenstein/triangular lattice data from the paper's 7-colouring
# r = 2/5 circumradius, nearest-neighbour distance d = sqrt(3)*r = 2*sqrt(3)/5
# lattice point (m,n): z = d*(m + n*omega), omega = -1/2 + i sqrt3/2
#   X = sqrt3*(2m-n)/5 ,  Y = 3n/5
# colour(m,n) = (m+2n) mod 7
def zXY(m,n): return (F(0), F(2*m-n,5), F(3*n,5))   # (rational part, coeff of sqrt3, rational)
def dist2(p0,m,n):
    # |p0 - z|^2 = A + B sqrt3
    x0,y0 = p0
    xs, xr, yr = zXY(m,n)   # z = xs*sqrt3 + xr + i*yr   (xs = (2m-n)/5)
    # (x0 - xs*sqrt3 - xr)^2 + (y0-yr)^2
    a = (x0-xr); b = -xs
    A = a*a + 3*b*b + (y0-yr)**2
    B = 2*a*b
    return A,B
def sgn(p,q):
    # sign of p + q*sqrt3
    if p==0 and q==0: return 0
    if q==0: return 1 if p>0 else -1
    if p==0: return 1 if q>0 else -1
    if p>0 and q>0: return 1
    if p<0 and q<0: return -1
    v=p*p-3*q*q
    if p>0: return 1 if v>0 else -1
    else:   return 1 if v<0 else -1   # p<0,q>0 : p+q sqrt3 >0 iff 3q^2>p^2 iff v<0
def below(A,B,lam):   # decide A+B sqrt3 < lam^2   (lam^2 rational)
    return sgn(A-lam*lam, B) < 0
def colour(m,n): return (m+2*n)%7
def check(p0, eps, verbose=True):
    r=F(2,5)
    lo = 1-eps-r; hi = 1+eps+r
    assert lo>0
    lo2=lo*lo; hi2=hi*hi
    present={}
    for m in range(-6,7):
        for n in range(-6,7):
            A,B=dist2(p0,m,n)
            inside = (not below(A,B,lo2)) and below(A,B,hi2)   # lo^2 <= d^2 < hi^2
            if inside: present.setdefault(colour(m,n),[]).append((m,n))
    return present
def run(p0, eps):
    pres=check(p0,eps)
    missing=sorted(set(range(7))-set(pres))
    return missing, pres
if __name__=="__main__":
    p0=(F(2,55),F(16,55))
    print("p0 =",p0, " |p0|^2 =", sum(x*x for x in p0))
    print("inside Voronoi cell of origin? (need |p0| < r = 2/5):", sum(x*x for x in p0) < F(4,25))
    for L in [F(1,100), F(1,90), F(1,80), F(1,70), F(1,60)]:
        eps=L/F(1)/F(2)**F(1)  # placeholder
        eps=float(L)/math.sqrt(2)
        # exact eps as a real: use rational bound eps_r >= L/sqrt2  (take a rational upper bound)
        epsq=F(math.ceil(float(L)/math.sqrt(2)*10**9),10**9)
        miss,pres=run(p0,epsq)
        print("L=%s  eps<=%s  missing=%s  colours present=%s"%(L,epsq,miss,sorted(pres)))
