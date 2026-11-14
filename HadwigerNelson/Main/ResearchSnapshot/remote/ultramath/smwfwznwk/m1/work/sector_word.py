"""Uniform pair-only free-label sector word for the 6-cycle at k=6.

Letters are the six admissible pairs avoiding the free label 0:
  A={1,3} E={2,5} B={1,4} F={3,5} D={2,4} C={1,5}
Disjointness graph H (letter x -- letter y iff x & y = empty):
  A-E, A-D, B-E, B-F, D-F, C-D     i.e. 5-cycle A-E-B-F-D-A  plus the pendant C-D.

THE WORD.  For m >= 5 let
      u_m = A^2 B^2 D^(m-3) E^2 F^(m-3)        (a cyclic word of length 2m)
and let w_m be u_m repeated three times (length 6m).
Claim: w_m(i) & w_m(i+o) = empty for every i and every o in {+-(m-1),+-m,+-(m+1)} mod 6m.

Reason (exact, all m >= 5): 2m | 6m, and modulo 2m the six offsets reduce to
{m-1, m, m+1}; so it suffices that u_m(i) & u_m(i+m+d) = empty for d in {-1,0,1} and all
i in Z_2m.  Position ranges of u_m:  {0,1}=A  {2,3}=B  [4,m]=D  {m+1,m+2}=E  [m+3,2m-1]=F.
For i in {0,1} the three partners lie in {m-1,m,m+1,m+2}, i.e. in D and E;
for i in {2,3} in {m+1,...,m+4}, i.e. in E and F;
for i in [4,m] in [m+3,2m] = F, with 2m read as 0, i.e. in F and A;
for i in {m+1,m+2} in {0,1,2,3}, i.e. in A and B;
for i in [m+3,2m-1] in [2,m], i.e. in B and D.
The six pairs {A,D},{A,E},{B,E},{B,F},{D,F},{A,B} are exactly the edges of H, so every
constraint holds.  (This is what verify.py checks, twice, and what verify_geom.py reduces
to the exact transport statement.)
"""
from itertools import combinations

A,E,B,F,D,C = (frozenset(x) for x in [(1,3),(2,5),(1,4),(3,5),(2,4),(1,5)])
LETTERS = {'A':A,'B':B,'C':C,'D':D,'E':E,'F':F}

def word_from_string(m, s=None):
    if s is None:
        s = 'AA'+'BB'+'D'*(m-3)+'EE'+'F'*(m-3)
    assert len(s) == 2*m, (len(s), 2*m)
    return [LETTERS[ch] for ch in (s*3)]

def offsets(m):
    n = 6*m
    return sorted(set((m+k) % n for k in (-1,0,1)) | set((-m+k) % n for k in (-1,0,1)))
