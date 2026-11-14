import math, random
from mpmath import mp, mpf, asin, sin, pi, cos
mp.dps=30

# --- 1. verify Sh(d)=[2asin((1-d)/2),2asin((1+d)/2)] by direct optimisation of the shift map
def shift_extremes(d, N=400000):
    lo, hi = 1e9, -1e9
    for k in range(N):
        psi = -math.pi + 2*math.pi*k/N
        w = complex(d,0)+complex(math.cos(psi),math.sin(psi)); r=abs(w)
        if r<1e-9 or r>2-1e-12: continue
        th = math.atan2(w.imag,w.real)
        for sgn in (1,-1):
            v = th + sgn*math.acos(r/2) - psi
            v = math.remainder(v, 2*math.pi)
            if v>hi: hi=v
            if v<lo: lo=v
    return lo,hi
for d in [0.2,0.5,0.53]:
    lo,hi = shift_extremes(d, 200000)
    print("d=%.2f empirical shift range [%.7f, %.7f]  closed form [%.7f, %.7f]"%(
        d, lo, hi, float(2*asin((1-d)/2)), float(2*asin((1+d)/2))))

# --- 2. the 18-sector frozen field, verify (5.3) directly against the paper's formula
def P(theta):
    return (math.floor(9*theta/math.pi))%6
random.seed(1)
for D in [0.3, 0.5, 0.5320888]:
    worst=None; viol=0; tot=0
    for _ in range(60000):
        d = D*random.random()
        alpha = random.uniform(-math.pi, math.pi)
        f = random.uniform(-math.pi, math.pi)
        a = complex(d*math.cos(alpha), d*math.sin(alpha)); ff=complex(math.cos(f),math.sin(f))
        w = a+ff; r=abs(w)
        if r<1e-9 or r>2-1e-12: continue
        th=math.atan2(w.imag,w.real)
        for sgn in (1,-1):
            s = th+sgn*math.acos(r/2)   # arg of s
            tot+=1
            if P(f)==P(s):
                # careful: P returns a label; palettes here are singletons
                viol+=1
    print("D=%.7f: checked %d (d,alpha,f,branch) triples of Lemma 5.2(3) on the 18-sector field, violations=%d"%(D,tot,viol))

# --- 3. same for the exact shift using complex arithmetic (independent recomputation of s)
def s_of(d,alpha,f):
    a=complex(d*math.cos(alpha),d*math.sin(alpha)); ff=complex(math.cos(f),math.sin(f))
    w=a+ff; r=abs(w)
    if r<1e-9 or r>2-1e-12: return []
    c=min(r/2,1.0); q=math.sqrt(max(0.0,1-c*c)); what=w/r
    return [w/2+sg*1j*what*q for sg in (1,-1)]
def Plab(z):
    return math.floor(9*math.atan2(z.imag,z.real)/math.pi)%6
viol=0; tot=0
for _ in range(300000):
    d=0.53*random.random(); alpha=random.uniform(-math.pi,math.pi); f=random.uniform(-math.pi,math.pi)
    fu=complex(math.cos(f),math.sin(f))
    for s in s_of(d,alpha,f):
        tot+=1
        if Plab(fu)==Plab(s): viol+=1
print("D=0.53 complex-arithmetic recomputation: %d checks, %d violations"%(tot,viol))
