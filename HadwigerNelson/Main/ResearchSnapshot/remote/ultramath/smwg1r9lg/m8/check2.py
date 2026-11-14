from mpmath import mp, mpf, asin, sin, cos, pi, findroot
mp.dps = 40
def a(D): return 2*asin((1-D)/2)
def b(D): return 2*asin((1+D)/2)
def Da(y): return 1 - 2*sin(y/2)       # a(D)>=y  <=> D<=Da(y)
def Db(y): return 2*sin(y/2) - 1       # b(D)<=y  <=> D<=Db(y)
L = 2*pi
def Dstar(k,m,N):   # condition: N*k*a >= m*L  and  N*k*b <= (k-m)*L
    return min(Da(m*L/(k*N)), Db((k-m)*L/(k*N)))
print("thresholds: D*(k,m) = max_N min( a^{-1}(mL/(kN)), b^{-1}((k-m)L/(kN)) )")
for k in range(3,11):
    row=[]
    for m in range(1,k):
        vals=[(Dstar(k,m,N),N) for N in range(1,400)]
        v,Nb=max(vals); row.append("m=%d:%.10f(N=%d)"%(m,v,Nb))
    print(" k=%2d  "%k + "  ".join(row))
print()
print("continuum versions (b <= (k/m-1)a):")
for k in range(3,10):
    for m in range(1,k):
        if k-m<=0: continue
        r = mpf(k)/m - 1
        try:
            v = findroot(lambda D: b(D)-r*a(D), mpf("0.3"))
        except Exception as e:
            v = float('nan')
        print("   k=%d m=%d  r=k/m-1=%.4f  D=%.10f"%(k,m,r,v))
