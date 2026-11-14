"""How far can a FROZEN palette field with a free label and palettes of size >= 2 go?

A word  word : Z/n -> 2^[6]  with
  (a) 2 <= |word[i]| <= 3            (size bound at a six-cycle centre),
  (b) word[i] contains a non-adjacent pair of C_6  (Lemma 6.2 / (6.2) at an ell=6 centre),
  (c) 0 not in word[i]               (free label = non-proper self-avoidance),
  (d) word[i] cap word[i+k] = empty for every k in +-K(d)   (Lemma 5.2(3)),
where K(d) = [floor(delta_min(d)/Delta), ceil(M(d)/Delta)], is exactly the frozen
countermodel with transport radius >= d.  Decided by CaDiCaL on an explicit CNF.
"""
import math, subprocess, os, tempfile, itertools, sys
from frozen import shift, deriv
CADICAL = "/opt/lean/bin/cadical"

def palettes_valid_for_C6():
    """pairs/triples of [5], size 2..3, containing a pair non-adjacent in C6."""
    out=[]
    for r in (2,3):
        for S in itertools.combinations(range(1,6), r):
            S=set(S)
            if any((j-i)%6 not in (1,5) for i in S for j in S if i<j and (j-i)%6!=0 and (i-j)%6 not in (1,5) for _ in [0]):
                pass
            # contains a non-adjacent pair of C6
            ok=any((b-a)%6 not in (1,5) for a in S for b in S if a<b)
            if ok: out.append(frozenset(S))
    return out

def sh_interval(d, N=30000):
    lo=hi=None
    for i in range(N):
        psi=-math.pi+2*math.pi*i/N
        for sgn in (+1,-1):
            s=shift(d,psi,sgn); dv=deriv(d,psi,sgn)
            if s is None or dv is None or s<=0 or abs(1+dv)<1e-6: continue
            lo=s if lo is None else min(lo,s); hi=s if hi is None else max(hi,s)
    return lo,hi

def Kset_from(d, n, iv):
    lo,hi=iv; D=2*math.pi/n
    klo=math.floor(lo/D); khi=math.ceil(hi/D)
    ks=set()
    for k in range(klo,khi+1):
        ks.add(k%n); ks.add((-k)%n)
    return ks

def word_exists(n, d, alph, iv=None):
    K=Kset_from(d,n,iv if iv is not None else sh_interval(d))
    var={}
    cnt=0
    for i in range(n):
        for P in alph:
            cnt+=1; var[(i,P)]=cnt
    cl=[]
    for i in range(n):
        cl.append([var[(i,P)] for P in alph])
        for P,Q in itertools.combinations(alph,2):
            cl.append([-var[(i,P)],-var[(i,Q)]])
    for k in sorted(K):
        for i in range(n):
            j=(i+k)%n
            for P in alph:
                for Q in alph:
                    if not P.isdisjoint(Q):
                        cl.append([-var[(i,P)],-var[(j,Q)]])
    fd,path=tempfile.mkstemp(suffix=".cnf"); os.close(fd)
    try:
        with open(path,"w") as f:
            f.write(f"p cnf {cnt} {len(cl)}\n")
            for c in cl: f.write(" ".join(map(str,c))+" 0\n")
        r=subprocess.run([CADICAL,"-q",path],capture_output=True,text=True)
        return "s SATISFIABLE" in r.stdout, K
    finally: os.unlink(path)

if __name__=="__main__":
    alph = palettes_valid_for_C6()
    print(f"{len(alph)} admissible palettes over labels 1..5:", sorted(sorted(p) for p in alph))
    for d in [0.10,0.15,0.20,0.25,0.28,0.30]:
        iv = sh_interval(d, 6000)
        row=[]
        for n in [24,36,48,60,72,96,120]:
            sat,_ = word_exists(n,d,alph,iv)
            row.append(f"n={n}:{'SAT' if sat else 'UNSAT'}")
        print(f" d={d:.3f}  " + "  ".join(row), flush=True)
