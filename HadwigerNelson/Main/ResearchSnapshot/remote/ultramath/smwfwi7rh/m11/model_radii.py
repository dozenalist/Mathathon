"""Exact transport radius of the report's frozen countermodels.

Their fields are functions of the DIRECTION only: P_z(theta) = sigma(floor(theta/Delta)),
n = 36 sectors, Delta = 2 pi/36, and the sector word is given explicitly.
Because the field does not depend on the centre, Lemma 5.2(3) at distance d reads

    P(f) cap P(f + delta) = empty      for a.e. f and every delta in Sh(d),

and since Delta-quantised, this is equivalent to:  every integer k that occurs as
floor((theta+delta)/Delta) - floor(theta/Delta) for some delta in Sh(d) lies in

    Safe = { k mod n : word[i] cap word[i+k] = empty  for all i }.

Sh(d) contains the interval [delta_min(d), M(d)] (the branch s_+ is continuous, and
the two branches give +- the interval).  Hence  K(d) := [floor(delta_min/Delta),
ceil(M/Delta)]  must be contained in Safe (mod n), and so must -K(d).
"""
import math, json
from frozen import shift, deriv

n = 36
DELTA = 2*math.pi/n

def blockword(M0,M1,M2,L=4):
    return [M0 if (i//L)%3==0 else (M1 if (i//L)%3==1 else M2) for i in range(n)]

MODELS = {
 "ell=3 three-block {3},{4},{5}":      blockword(frozenset({3}),frozenset({4}),frozenset({5})),
 "ell=4 three-block {0,2},{1,3},{4}":  blockword(frozenset({0,2}),frozenset({1,3}),frozenset({4})),
 "ell=5 three-block {0,2},{1,3},{5}":  blockword(frozenset({0,2}),frozenset({1,3}),frozenset({5})),
}
# the 36-sector free-label word of FREE-LABEL.md, copied verbatim
W6 = [[3,5],[3,5],[2,5],[2,5],[2,4],[2,4],[2,4],[1,4],[1,4],[1,3],[1,3],[1,3],
      [3,5],[3,5],[2,5],[2,5],[2,4,5],[2,4],[2,4],[1,4],[1,4],[1,3],[1,3],[1,3],
      [3,5],[3,5],[2,5],[2,5],[2,4],[2,4],[2,4],[1,4],[1,4],[1,3],[1,3],[1,3]]
MODELS["ell=6 free-label 36-sector word"] = [frozenset(w) for w in W6]

def safe_set(word):
    return sorted({k for k in range(1,n) if all(word[i].isdisjoint(word[(i+k)%n]) for i in range(n))})

def sh_interval(d, N=20000):
    lo=hi=None
    for i in range(N):
        psi=-math.pi+2*math.pi*i/N
        for sgn in (+1,-1):
            s=shift(d,psi,sgn); dv=deriv(d,psi,sgn)
            if s is None or dv is None or s<=0 or abs(1+dv)<1e-6: continue
            lo=s if lo is None else min(lo,s); hi=s if hi is None else max(hi,s)
    return lo,hi

def ok(d, S, N=20000):
    lo,hi = sh_interval(d,N)
    klo=math.floor(lo/DELTA); khi=math.ceil(hi/DELTA)
    ks=set(range(klo,khi+1))
    need=set()
    for k in ks: need.add(k%n); need.add((-k)%n)
    return need <= S, klo, khi, sorted(need - S)

if __name__=="__main__":
    out={}
    for name,word in MODELS.items():
        S = set(safe_set(word))
        # verify each palette is admissible for its cycle and nonempty, size<=3
        # search the largest d (bisection)
        a,b = 0.0, 0.9
        okb,_,_,_ = ok(b,S)
        if okb:
            print(name, "satisfies transport at d=0.9 -- unexpected"); continue
        for _ in range(28):
            m=(a+b)/2
            if ok(m,S)[0]: a=m
            else: b=m
        lo,hi = sh_interval(a,4000)
        print(f"{name:42s}  Safe={sorted(S)}")
        print(f"{'':42s}  transport radius = {a:.5f}   (report claims d0 = pi/54 = {math.pi/54:.5f})")
        out[name]=dict(safe=sorted(S), radius=a)
    json.dump(out, open("model_radii.json","w"), indent=1)
