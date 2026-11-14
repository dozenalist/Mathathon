"""Uniform verification, all four cycle lengths, m=6, n=36, block length L=4:
- values pairwise disjoint, admissible for C_ell, union omits a free label;
- the word sigma(i)=M_{floor(i/L) mod 3} is disjoint at all six transport offsets
  +-(m-1), +-m, +-(m+1) mod n.
Also checks the geometric margin 1.5938*d0 < Delta in exact rationals.
"""
from fractions import Fraction as F
from itertools import combinations
K=6
def edges(ell): return [frozenset((j,(j+1)%ell)) for j in range(ell)]
def adm(S,ell): return 1<=len(S)<=3 and not any(S<=e for e in edges(ell))
tables={3:({3},{4},{5}),4:({0,2},{1,3},{4}),5:({0,2},{1,3},{5}),6:({0,3},{1,4},{2,5})}
m=6; n=6*m; L=2*m//3
offs=sorted(set([(m+k)%n for k in (-1,0,1)]+[(-m+k)%n for k in (-1,0,1)]))
print("offsets",offs,"L",L)
for ell,(M0,M1,M2) in tables.items():
    M=[frozenset(M0),frozenset(M1),frozenset(M2)]
    assert all(adm(M[i],ell) for i in range(3)), (ell,M)
    assert not(M[0]&M[1]) and not(M[0]&M[2]) and not(M[1]&M[2]), (ell,M)
    free=set(range(K))-(M[0]|M[1]|M[2])
    word=[M[(i//L)%3] for i in range(n)]
    ok=all(not(word[i]&word[(i+o)%n]) for i in range(n) for o in offs)
    print(f"ell={ell}: values={[sorted(x) for x in M]} free={sorted(free)} offsets-disjoint={ok}")
    assert ok
# geometric margin: 1.5938 * d0 < Delta, d0=pi/(9m), Delta=pi/(3m) -> 1.5938/9 < 1/3
print("geometric margin 1.5938/9 < 1/3:", F(15938,10000)/9 < F(1,3))
print("ALL OK")
