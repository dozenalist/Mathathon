from mpmath import mp, mpf, asin, sin, cos, pi, findroot
mp.dps = 40

def a(D): return 2*asin((1-D)/2)
def b(D): return 2*asin((1+D)/2)

def D_from_a(y):   # smallest D>0 with a(D)>=y  (a increasing)
    return 1 - 2*sin(y/2)
def D_from_b(y):   # largest D with b(D)<=y
    return 2*sin(y/2) - 1

print("Sh(d) check vs m11 table:")
for d in ["0.175","0.3044","0.5","0.4609"]:
    D = mpf(d); print("  d=%s  a=%.9f b=%.9f"%(d, a(D), b(D)))

print()
print("max over N of min(1-2sin(pi/(6N)), 2sin(5pi/(6N))-1), k=6,m=1:")
best=None
for N in range(1,20):
    v1 = 1-2*sin(pi/(6*N)); v2 = 2*sin(5*pi/(6*N))-1
    v = min(v1,v2)
    if v2 < 0: v = v2
    print("  N=%2d  A=%.12f  B=%.12f  min=%.12f"%(N, v1, v2, min(v1,v2)))
Dstar = 2*cos(2*pi/9)-1
print("  2cos(2pi/9)-1 =", Dstar)
print("  root of D^3+3D^2-1:", findroot(lambda D: D**3+3*D**2-1, mpf("0.53")))
print("  a(D*)=%.15f 2pi/18=%.15f   b(D*)=%.15f 5pi/9=%.15f"%(a(Dstar), 2*pi/18, b(Dstar), 5*pi/9))

print()
print("thresholds D*(k,m): max over N of min(D_from_a(2pi/(kN)), D_from_b((k-m)2pi/(kN)))")
for k in range(4,11):
    for m in range(1,4):
        if m>=k: continue
        best = max(min(D_from_a(2*pi/(k*N)), D_from_b((k-m)*2*pi/(k*N))) for N in range(1,200))
        # refine: scan more N
        vals = [(min(D_from_a(2*pi/(k*N)), D_from_b((k-m)*2*pi/(k*N))),N) for N in range(1,2000)]
        best,Nb = max(vals)
        print("  k=%2d m=%d  D*=%.12f  (N=%d)"%(k,m,best,Nb))
print()
print("m11 Theorem D calibration: b=2a at k=6")
print("  solve 2asin((1+D)/2)=4asin((1-D)/2):", findroot(lambda D: b(D)-2*a(D), mpf("0.3044")))
print("m11 Theorem C calibration: b=3a at k=6:", findroot(lambda D: b(D)-3*a(D), mpf("0.4608")))
