"""The object: a translation-invariant sector palette word at k=6.

Geometry (paper, Definition 5.1 + Lemma 5.2(3)):
  Delta = 2*pi/(6m) is the sector width of the 6m-sector field
        P_z(theta) = sigma(floor(theta/Delta) mod 6m),   z-independent;
  d_0   = pi/(9m) = Delta/3 is the centre distance allowed by the geometric lemma
        (verify_geom.py proves exactly: |arg s_+- - (arg f +- pi/3)| <= 1.5938*|z'-z|).
Hence (5.3) needs exactly the six sector displacements +-(m-1), +-m, +-(m+1) mod 6m.

Letters: the six admissible pairs of C_6 avoiding the free label 0.
Domain (k=6, C_6):  |P| in {2,3},  P not contained in a cycle edge {i,i+1}  (Lemma 6.2 / (6.2)).
"""
from itertools import combinations

K = 6
E6 = [frozenset((j, (j+1) % K)) for j in range(K)]

A = frozenset((1,3)); E = frozenset((2,5)); B = frozenset((1,4))
F = frozenset((3,5)); D = frozenset((2,4)); C = frozenset((1,5))
NAME = {A:'A', B:'B', C:'C', D:'D', E:'E', F:'F'}
BY_NAME = {v:k for k,v in NAME.items()}

def admissible(S, ell=6, sizes=(1,2,3)):
    S = frozenset(S)
    E = [frozenset((j,(j+1)%ell)) for j in range(ell)]
    return 1 <= len(S) <= 3 and len(S) in sizes and not any(S <= e for e in E)

def domain(sizes=(2,3), free=0, ell=6):
    out=[]
    for r in sizes:
        for c in combinations([x for x in range(K) if x != free], r):
            if admissible(c, ell=ell, sizes=(r,)): out.append(frozenset(c))
    return out

def offsets(m):
    """the six sector displacements forced by the exact transport (5.3)"""
    n = 6*m
    return sorted(set((m+k) % n for k in (-1,0,1)) | set((-m+k) % n for k in (-1,0,1)))

def uniform_word(m, period_pattern=None):
    """w_m: length 6m, = (A^2 B^2 D^(m-3) E^2 F^(m-3)) repeated 3 times; valid for m >= 5."""
    s = period_pattern if period_pattern is not None else 'AA'+'BB'+'D'*(m-3)+'EE'+'F'*(m-3)
    assert len(s) == 2*m
    return [BY_NAME[ch] for ch in s*3]

def as_lists(w):
    return [sorted(S) for S in w]
