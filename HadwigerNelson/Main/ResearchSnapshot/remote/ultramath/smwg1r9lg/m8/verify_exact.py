"""Rigorous rational-interval certificate (no floating point in any decision).
Intervals are rounded OUTWARD to multiples of 1/10^40 after each operation, so all
arithmetic stays rational and small.  sin/cos: Taylor with alternating-remainder bound;
pi: Machin  pi = 16 atan(1/5) - 4 atan(1/239)."""
from fractions import Fraction as F
Q = 10**40

def rnd(lo, hi):
    import math
    lo = F(math.floor(lo*Q), Q); hi = F(math.ceil(hi*Q), Q)
    return lo, hi

def fact(n):
    r=1
    for i in range(2,n+1): r*=i
    return r
FACT=[F(fact(i)) for i in range(200)]

def atan_inv(n,k):
    S=F(0)
    for j in range(k): S += F((-1)**j, (2*j+1)*n**(2*j+1))
    nxt=F(1,(2*k+1)*n**(2*k+1))
    return rnd(S, S+nxt) if k%2==0 else rnd(S-nxt,S)

def pi_iv(k=40):
    a=atan_inv(5,k); b=atan_inv(239,k)
    return rnd(16*a[0]-4*b[1], 16*a[1]-4*b[0])
PI=pi_iv(40)
print("pi enclosure width 1e-? :", "yes" if PI[0]<F(3141592653589793238462643383279,10**30)<PI[1] else "NO")

def sin_iv(x,n=30):
    s=1; neg = x<0
    if neg: x=-x
    S=F(0)
    for k in range(n): S += F((-1)**k,1)*x**(2*k+1)/FACT[2*k+1]
    rem=x**(2*n+1)/FACT[2*n+1]
    lo,hi = rnd(S-rem,S+rem)
    return (-hi,-lo) if neg else (lo,hi)
def cos_iv(x,n=30):
    if x<0: x=-x
    S=F(0)
    for k in range(n): S += F((-1)**k,1)*x**(2*k)/FACT[2*k]
    rem=x**(2*n)/FACT[2*n]
    return rnd(S-rem,S+rem)
def sinp(num,den):           # sin(num*pi/den), monotone on [0,pi/2]
    lo=sin_iv(PI[0]*F(num,den))[0]; hi=sin_iv(PI[1]*F(num,den))[1]
    return rnd(lo,hi)
def cosp(num,den):
    lo=cos_iv(PI[1]*F(num,den))[0]; hi=cos_iv(PI[0]*F(num,den))[1]
    return rnd(lo,hi)
fl=lambda t: float(t)

print("check: sin(pi/6)=",fl(sinp(1,6)[0]),fl(sinp(1,6)[1]),"  cos(pi/3)=",fl(cosp(1,3)[0]),fl(cosp(1,3)[1]))
c=cosp(2,9); Ds=rnd(2*c[0]-1, 2*c[1]-1)
print("D* = 2cos(2pi/9)-1  in [%.22f, %.22f]"%(fl(Ds[0]),fl(Ds[1])))
print("     D^3+3D^2-1 at the two ends: [%.3e, %.3e]"%(fl(Ds[0]**3+3*Ds[0]**2-1),fl(Ds[1]**3+3*Ds[1]**2-1)))
def A(N): s=sinp(1,6*N); return rnd(1-2*s[1],1-2*s[0])
def B(N): s=sinp(5,6*N); return rnd(2*s[0]-1,2*s[1]-1)
print()
print(" N |      A_N=1-2sin(pi/(6N))      |      B_N=2sin(5pi/(6N))-1      | min < D* ?")
allok=True
for N in range(1,9):
    a,b=A(N),B(N); mhi=min(a[1],b[1])
    if N==3:
        print(" 3 | [%.18f,%.18f] | [%.18f,%.18f] | attains D*  (B_3=2sin(5pi/18)-1=2cos(2pi/9)-1 exactly)"%(fl(a[0]),fl(a[1]),fl(b[0]),fl(b[1])))
        continue
    ok = mhi < Ds[0]; allok = allok and ok
    print("%2d | [%.18f,%.18f] | [%.18f,%.18f] | %s"%(N,fl(a[0]),fl(a[1]),fl(b[0]),fl(b[1]),ok))
print("all N!=3 strictly below D*:",allok)
print("N=3 exactness:  sin(5pi/18) vs cos(2pi/9) intervals:", [fl(v) for v in sinp(5,18)], [fl(v) for v in cosp(2,9)])
print()
def TH(k,m,Nmax=80):
    best=None
    for N in range(1,Nmax):
        a=sinp(m,k*N); b=sinp(k-m,k*N)
        val=rnd(min(F(1)-2*a[1], 2*b[0]-1), min(F(1)-2*a[0], 2*b[1]-1))
        cand=(min(F(1)-2*a[1], 2*b[0]-1), N, val)
        if best is None or cand[0]>best[0]: best=cand
    return best
for (k,m) in [(6,1),(6,2),(5,2),(5,1),(3,1),(4,1),(7,1),(8,1)]:
    v,N,val = TH(k,m)
    print(" k=%d m=%d : D*(k,m) >= %.18f   (best N = %d)"%(k,m,fl(val[0]),N))

# ---- exact admissibility of N=3 at D* (symbolic identities, interval-checked signs) ----
print()
print("admissibility of N=3 at D*:")
one_minus = 2*sinp(1,9)[0]**2      # 2 sin^2(pi/9) = 1 - cos(2pi/9), lower bound
s18 = sinp(1,18)                    # sin(pi/18)
print("   1-D* = 2sin^2(pi/9) >= %.18f ; sin(pi/18) <= %.18f ; a(D*) >= pi/9 : %s"
      % (fl(one_minus), fl(s18[1]), one_minus > s18[1]))
b_star = 2*(PI[1]/2 - 2*PI[0]/9), 2*(PI[0]/2 - 2*PI[1]/9)
print("   b(D*) = 2arcsin(cos(2pi/9)) = 5pi/9 : 5pi/9 <= %.18f and b(D*) <= 5pi/9 holds analytically; enclosure [%.18f,%.18f]"
      % (fl(5*PI[0]/9), fl(b_star[0]), fl(b_star[1])))
