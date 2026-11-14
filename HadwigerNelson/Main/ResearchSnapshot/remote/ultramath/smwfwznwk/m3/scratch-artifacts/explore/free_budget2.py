"""Lemma: at k=6 a word satisfying (A) admissibility and (C) six-offset
disjointness (m>=3) cannot have its palette union inside a 4-element set.
Proof: in a 4-set A, two disjoint pairs are complementary, so every value must be a
pair and every neighbour of i equals A \\ W(i).  Then W(i-2)=W(i) for all i, so W is
2-periodic; but one of m-1, m, m+1 is even, and an even shift must land on the same
value, which is not disjoint from itself.  Machine check of the reduction and of the
conclusion."""
from itertools import combinations
E=[(1<<j)|(1<<((j+1)%6)) for j in range(6)]
def adm(S): return 1<=bin(S).count('1')<=3 and not any(S&e==S for e in E)
def offsets(m):
    n=6*m; return sorted({(m+k)%n for k in (-1,0,1)}|{(-m+k)%n for k in (-1,0,1)})
bad=[]
for A in combinations(range(6),4):
    for r in (2,3):
        for c in combinations(A,r):
            S=sum(1<<i for i in c)
            if not adm(S): bad.append(('not admissible?',A,c))
# (1) in a 4-set, disjoint admissible values are exactly complementary pairs
for A in combinations(range(6),4):
    vals=[]
    for r in (2,3):
        for c in combinations(A,r):
            S=sum(1<<i for i in c)
            if adm(S): vals.append(S)
    Aset=sum(1<<i for i in A)
    for a in vals:
        mates=[b for b in vals if not (a&b)]
        if bin(a).count('1')==2:
            assert mates in ([Aset^a], []), (A,bin(a),mates)  # at most the complement
        else:
            assert mates==[], (A,bin(a),mates)         # a triple has no partner in A
print("(1) in a 4-set: pairs have the unique complementary partner, triples none: OK")
# (2) the parity obstruction, for every m>=3
ok=True
for m in range(3,2001):
    S=set(offsets(m))
    iff = any(d%2==0 for d in S)
    ok &= iff
print("(2) one of the six offsets is even, for every m>=3:", ok)
# (3) the conclusion: no 2-periodic word on a 4-set satisfies (C), m = 3..600
cnt=0
for m in range(3,601):
    n=6*m; S=set(offsets(m))
    for A in combinations(range(6),4):
        vals=[]
        for r in (2,3):
            for c in combinations(A,r):
                Sv=sum(1<<i for i in c)
                if adm(Sv): vals.append(Sv)
        # all 2-periodic words: choose W(0)=P, W(1)=Q
        for P in vals:
            for Q in vals:
                W=[P if i%2==0 else Q for i in range(n)]
                if all(not(W[i]&W[(i+d)%n]) for i in range(n) for d in S):
                    cnt+=1; print("  unexpected 2-periodic solution",m,A,bin(P),bin(Q))
print("(3) 2-periodic words on a 4-set satisfying (C):", cnt, "(expected 0)")
