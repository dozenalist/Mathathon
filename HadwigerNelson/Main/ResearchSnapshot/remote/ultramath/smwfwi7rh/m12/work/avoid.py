"""Search for a gamma-avoiding sector palette field at a 6-cycle centre at k=6.
Constraints: 36 sectors of 10 deg; every palette admissible for C_6 (no edge containment),
no singleton (every label lies on a cycle edge), centre colour i0=0 excluded from every palette
(self-avoidance at a typical point), and (5.7):  sigma(i) & sigma(i+6) == {}.
Then test the gamma criterion for every pair of disjoint values."""
import random, itertools, sys
sys.path.insert(0,'work')
from fractions import Fraction as F
from orbit_crit import criterion, width, norm, verify

# admissible palettes at a 6-cycle centre with centre colour 0:  subsets of {1..5},
# not contained in an edge of the 6-cycle 0-1-2-3-4-5-0, of size 2 or 3.
EDGES = [frozenset({i,(i+1)%6}) for i in range(6)]
def admissible():
    out=[]
    for r in (2,3):
        for S in itertools.combinations(range(1,6), r):
            s=frozenset(S)
            if not any(s <= e for e in EDGES): out.append(s)
    return out
ADM = admissible()
print("admissible palettes at a 6-cycle centre (centre colour 0):", len(ADM), [sorted(s) for s in ADM])

def arcs_of(word, val):
    out=[]; i=0; n=len(word)
    while i<n:
        if word[i]==val:
            j=i
            while j+1<n and word[j+1]==val: j+=1
            out.append((F(10*i),F(10*(j+1)))); i=j+1
        else: i+=1
    return out

def gamma_avoiding(word):
    vals=set(word)
    for A,B in itertools.combinations(vals,2):
        if A & B: continue
        EA, EB = arcs_of(word,A), arcs_of(word,B)
        w1,w2 = criterion(EA,EB, F(0), F(0))  # dummy psi; use real below
    return None

from gamma_crit import PSI_LO, PSI_HI
def killed_pairs(word):
    vals=sorted(set(word), key=lambda s:(len(s),sorted(s)))
    out=[]
    for A,B in itertools.combinations(vals,2):
        if A & B: continue
        EA, EB = arcs_of(word,A), arcs_of(word,B)
        w1,w2 = criterion(EA,EB,PSI_LO,PSI_HI)
        if width(w1)>0 or width(w2)>0:
            out.append((sorted(A),sorted(B),len(A|B)))
    return out

random.seed(7)
best=None
for trial in range(20000):
    word=[None]*36
    ok=True
    for j in range(6):                       # R-orbit chains {j, j+6, ..., j+30}
        chain=[]
        for t in range(6):
            for _ in range(200):
                P=random.choice(ADM)
                if not chain or not (P & chain[-1]): break
            else: ok=False; break
            chain.append(P)
        if not ok: break
        if chain[0] & chain[-1]:             # close the cycle
            for _ in range(200):
                P=random.choice(ADM)
                if not (P & chain[-2]) and not (P & chain[0]): break
            else: ok=False; break
            chain[-1]=P
        for t in range(6): word[j+6*t]=chain[t]
    if not ok: continue
    kp = killed_pairs(word)
    if not kp:
        print("gamma-avoiding 6-cycle field found at trial", trial)
        print(" ", [(i,sorted(word[i])) for i in range(36)])
        assert all(word[i] in ADM for i in range(36))
        assert all(not (word[i] & word[(i+6)%36]) for i in range(36))
        print("  (5.7) and admissibility verified; distinct values:", len(set(word)))
        best=word; break
if best is None: print("no gamma-avoiding field found")
