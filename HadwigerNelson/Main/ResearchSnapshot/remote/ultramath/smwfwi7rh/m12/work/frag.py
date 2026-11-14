"""most fragmented 6-cycle sector field: 16 admissible palettes on 36 sectors,
each palette on 2-3 sectors; test whether every disjoint-value sum is unit-triangle-free."""
import numpy as np, sys, itertools, random
sys.path.insert(0,'work')
from sumtest import member
from fractions import Fraction as F
from orbit_crit import criterion, width
from gamma_crit import PSI_LO, PSI_HI
ADM=[frozenset(s) for r in (2,3) for s in itertools.combinations(range(1,6),r)
     if not any(frozenset(s) <= frozenset({i,(i+1)%6}) for i in range(6))]
def arcs_of(word,val):
    out=[];i=0
    while i<36:
        if word[i]==val:
            j=i
            while j+1<36 and word[j+1]==val: j+=1
            out.append((10.0*i,10.0*(j+1))); i=j+1
        else: i+=1
    return out
def find_tri(IA,IB,step=0.04,R=2.04,D=360):
    xs=np.arange(-R,R,step); ys=np.arange(-R,R,step)
    Z=xs[:,None]+1j*ys[None,:]
    M=member(Z,np.array(IA),np.array(IB))
    def sh(M,dy,dx):
        out=np.zeros_like(M); i0=max(0,dx); i1=M.shape[0]+min(0,dx); j0=max(0,dy); j1=M.shape[1]+min(0,dy)
        out[i0:i1,j0:j1]=M[i0-dx:i1-dx, j0-dy:j1-dy]; return out
    for k in range(D):
        ang=2*np.pi*k/D; u=np.exp(1j*ang); v=u*np.exp(1j*np.pi/3)
        di=int(round(u.real/step)); dj=int(round(u.imag/step)); ei=int(round(v.real/step)); ej=int(round(v.imag/step))
        T=M & sh(M,dj,di) & sh(M,ej,dj*0+ej) if False else M & sh(M,dj,di) & sh(M,ej,ei)
        if T.any(): return True
    return False
random.seed(11)
def build():
    # each palette used at most 3 times; chains {(j+6t)}_{t=0..5} must alternate-disjoint
    for _ in range(4000):
        word=[None]*36; cnt={}
        ok=True
        for j in range(6):
            chain=[]
            for t in range(6):
                cand=[P for P in ADM if cnt.get(P,0)<3 and (not chain or not (P & chain[-1]))]
                if not cand: ok=False; break
                P=random.choice(cand); chain.append(P); cnt[P]=cnt.get(P,0)+1
            if not ok: break
            if chain[0] & chain[-1]: ok=False; break
            for t in range(6): word[j+6*t]=chain[t]
        if ok and max(cnt.values())<=3: return word
    return None
for trial in range(40):
    word=build()
    if word is None: break
    vals=sorted(set(word), key=lambda s:(len(s),sorted(s)))
    gam=[]
    for A,B in itertools.combinations(vals,2):
        if A&B: continue
        w1,w2=criterion([(F(a),F(b)) for a,b in arcs_of(word,A)],[(F(a),F(b)) for a,b in arcs_of(word,B)],PSI_LO,PSI_HI)
        if width(w1)>0 or width(w2)>0: gam.append((sorted(A),sorted(B)))
    if gam: continue          # want a gamma-avoiding one
    bad=None
    for A,B in itertools.combinations(vals,2):
        if A&B: continue
        if find_tri(arcs_of(word,A),arcs_of(word,B)): bad=(sorted(A),sorted(B)); break
    print("trial",trial,"distinct values",len(vals),"max multiplicity",max(word.count(v) for v in vals),
          "gamma-avoiding", not gam, "triangle found for", bad)
    if bad is None:
        print("  SURVIVOR (evades gamma and the general form):", [(i,sorted(word[i])) for i in range(36)])
        break
