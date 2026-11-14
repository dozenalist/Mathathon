"""CSP for a translation-invariant sector palette word (k=6, cycle C_ell, ell=6).

n = 6m sectors, sector width Delta = 2 pi/n = pi/(3m); d_0 = pi/(9m) = Delta/3.
Constraints: for every sector i and every transport offset o in
  {+-(m-1), +-m, +-(m+1)} mod n      (m >= 2)
the values at i and i+o are disjoint.  Value domain: admissible palettes for C_6
avoiding a fixed free label 0.
"""
from itertools import combinations

K = 6
E6 = [frozenset((j, (j+1) % K)) for j in range(K)]

def domain(ell=6, free=0, sizes=(2,3)):
    out=[]
    for r in sizes:
        for c in combinations([x for x in range(K) if x!=free], r):
            S=frozenset(c)
            if not any(S<=e for e in E6): out.append(S)
    return out

def offsets(m):
    n=6*m
    return sorted(set((m+k)%n for k in (-1,0,1))|set((-m+k)%n for k in (-1,0,1)))

def check_word(word, m, verbose=True):
    """Independent direct check of every constraint on a word of length 6m."""
    n=6*m
    assert len(word)==n, (len(word), n)
    V=domain()
    ok=True
    for i,S in enumerate(word):
        S=frozenset(S)
        if not any(S==T for T in V):
            print("BAD value at",i,sorted(S)); ok=False
    offs=offsets(m)
    for i in range(n):
        for o in offs:
            j=(i+o)%n
            if i==j: continue
            if word[i]&word[j]:
                if verbose: print("BAD disjointness",i,j,sorted(word[i]),sorted(word[j]),"offset",o)
                ok=False
    # (5.7): P(e) cap P(Re) = empty, R = +pi/3 = shift by m sectors -- implied by offset m
    for i in range(n):
        if word[i]&word[(i+m)%n]:
            print("BAD (5.7) at",i); ok=False
    return ok
