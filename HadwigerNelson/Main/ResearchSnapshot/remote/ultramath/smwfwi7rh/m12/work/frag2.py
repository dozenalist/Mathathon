"""Maximally fragmented 6-cycle fields: 16 admissible palettes, 36 sectors, each palette on 2-3
sectors, (5.7) along the six R-chains.  Test (a) the gamma criterion, (b) unit triangles in
disjoint-value sum sets."""
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
def find_tri(IA,IB,step=0.05,R=2.05,D=240):
    xs=np.arange(-R,R,step); ys=np.arange(-R,R,step)
    Z=xs[:,None]+1j*ys[None,:]
    M=member(Z,np.array(IA),np.array(IB))
    def sh(M,dy,dx):
        out=np.zeros_like(M); i0=max(0,dx); i1=M.shape[0]+min(0,dx); j0=max(0,dy); j1=M.shape[1]+min(0,dy)
        out[i0:i1,j0:j1]=M[i0-dx:i1-dx, j0-dy:j1-dy]; return out
    for k in range(D):
        ang=2*np.pi*k/D; u=np.exp(1j*ang); v=u*np.exp(1j*np.pi/3)
        di=int(round(u.real/step)); dj=int(round(u.imag/step)); ei=int(round(v.real/step)); ej=int(round(v.imag/step))
        if (M & sh(M,dj,di) & sh(M,ej,ei)).any(): return True
    return False

def build(rng, counts):
    """assign palettes to the 6 chains; counts = allowed multiplicities (list per palette)"""
    order=list(ADM); rng.shuffle(order)
    limit={P:rng.choice(counts) for P in order}
    word=[None]*36; used={P:0 for P in ADM}
    for j in range(6):
        chain=[]
        for t in range(6):
            cand=[P for P in ADM if used[P]<limit[P] and (not chain or not (P & chain[-1]))
                  and not (t==5 and (P & chain[0]))]
            if not cand: return None
            P=rng.choice(cand); chain.append(P); used[P]+=1
        for t in range(6): word[j+6*t]=chain[t]
    return word

rng=random.Random(2024)
survivors=0
for trial in range(60):
    word=build(rng,[2,3])
    if word is None: continue
    vals=sorted(set(word), key=lambda s:(len(s),sorted(s)))
    gam=False
    for A,B in itertools.combinations(vals,2):
        if A&B: continue
        w1,w2=criterion([(F(a),F(b)) for a,b in arcs_of(word,A)],[(F(a),F(b)) for a,b in arcs_of(word,B)],PSI_LO,PSI_HI)
        if width(w1)>0 or width(w2)>0: gam=True; break
    if gam:
        print("trial %2d: killed by gamma (values %d, mult %d)"%(trial,len(vals),max(word.count(v) for v in vals))); continue
    bad=None
    for A,B in itertools.combinations(vals,2):
        if A&B: continue
        if find_tri(arcs_of(word,A),arcs_of(word,B)): bad=(sorted(A),sorted(B)); break
    if bad is None:
        survivors+=1
        print("trial %2d: SURVIVOR (gamma-avoiding and triangle-free). values %d, mult %d"%(
            trial,len(vals),max(word.count(v) for v in vals)))
        print("   word:", [sorted(word[i]) for i in range(36)])
        if survivors>=2: break
    else:
        print("trial %2d: gamma-silent but killed by a triangle in A=%s B=%s"%(trial,bad[0],bad[1]))
print("survivors:",survivors)
