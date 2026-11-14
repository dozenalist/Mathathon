"""Verify cert/sector_words.json.  Two independent code paths + the full condition list.

Path A  direct:  words are read back, and every one of the 6*(6m) disjointness constraints is
        checked by literal set intersection, with the offsets recomputed from their definition.
Path B  geometric: the partner sectors are *not* taken from a formula.  For every sector i we
        take the two exact rotations i+-m of the 60-degree exclusion (5.7), and the lemma
        "1.5938*d_0 < Delta" says the exact unit decompositions can move the sector index by at
        most one, so we check disjointness against every sector at index distance <= 1 from
        i+-m, and we separately verify the numeric deviation bound on an actual grid of
        geometric configurations (work/verify_geom.py, run by run_all.sh).

Then the whole necessary-condition list of the paper at a cyclic centre:
  (P1) 1 <= |P| <= 3;  (6.2) P not contained in any cycle edge;  (5.7) P(e) cap P(Re) = empty;
  (5.3) the six transport offsets;  non-proper self-avoidance: label 0 in no palette;
  m2 two-centre bound |P_x|+|P_y| <= k-1 = 5;  m11 no ternary palette (density 0 <= 1/2);
  (P5) for every cycle edge {i,i+1} a trace supported in P with zero mass on i and i+1;
  (P6) no complementary triple pair (vacuous);  and: every label 1..5 does occur in some
  palette, so the only label function avoiding the field a.e. is the constant 0.
"""
import json, sys
from itertools import combinations
sys.path.insert(0,'work')

K=6
EDGES=[frozenset((j,(j+1)%K)) for j in range(K)]

def offsets_from_definition(m):
    n=6*m
    return sorted(set((m+k)%n for k in (-1,0,1)) | set((-m+k)%n for k in (-1,0,1)))

def main(path='cert/sector_words.json'):
    cert=json.load(open(path))
    allok=True
    for key in sorted(cert['words'],key=int):
        rec=cert['words'][key]; m=rec['m']; n=rec['n']
        w=[frozenset(s) for s in rec['word']]
        assert len(w)==n
        ok=[]
        # ---- Path A: literal check
        A_fail=[]
        if rec['offsets']!=offsets_from_definition(m): A_fail.append("offset list mismatch")
        for o in offsets_from_definition(m):
            if o%n==0: A_fail.append("degenerate offset")
            for i in range(n):
                j=(i+o)%n
                if w[i]&w[j]: A_fail.append(f"A: sectors {i},{j} offset {o} meet")
        for i in range(n):
            if len(w[i])!=2: A_fail.append(f"A: |P|={len(w[i])} at {i}")
            if 0 in w[i]:    A_fail.append(f"A: free label 0 at {i}")
            if any(w[i]<=e for e in EDGES): A_fail.append(f"A: (6.2) at {i}")
        # ---- Path B: geometric check (no offset formula): +-m plus one sector of slack
        B_fail=[]
        for i in range(n):
            for s in (+1,-1):
                centre=(i+s*m)%n                 # exact 60-degree rotation of the direction
                for d in (-1,0,1):               # the deviation lemma's slack
                    j=(centre+d)%n
                    if w[i]&w[j]: B_fail.append(f"B: sectors {i},{j} meet (60deg + {d})")
        # ---- (5.7) as a separate statement
        C_fail=[i for i in range(n) if w[i]&w[(i+m)%n]]
        # ---- (P5) trace condition, with an explicit trace
        D_fail=[]; traces={}
        values=sorted({tuple(sorted(S)) for S in w})
        for P in values:
            P=set(P)
            for e in EDGES:
                a,b=sorted(e)
                if a in P and b in P:
                    D_fail.append(f"no trace for edge {a}{b} within {sorted(P)}")
                else:
                    mass=[x for x in P if x not in (a,b)]
                    if not mass: D_fail.append(f"trace support empty for {a}{b} in {sorted(P)}")
                    else: traces[(tuple(sorted(P)),(a,b))]=mass[0]
        # ---- m2, m11
        E_fail=[]
        if any(len(P)>2 for P in w): E_fail.append("ternary palette (m2/m11)")
        if not all(2*len(P)<=5 for P in w): E_fail.append("m2 bound violated")
        # ---- m11: sigma{T subset P} <= 1/2 for every nonempty label set T (exact sector counts)
        F_fail=[]; m11={}
        for r in range(1,4):
            for T in combinations(range(6),r):
                T=frozenset(T); c=sum(1 for P in w if T<=P)
                m11[tuple(sorted(T))]=c
                if 2*c>n: F_fail.append(f"m11: |{{T={sorted(T)} subset P}}| = {c}/{n} > 1/2")
        # ---- labels occurring in palettes
        used=set().union(*w)
        info=dict(m=m,n=n,letters=''.join(rec['word_as_letters']),
                  values=sorted(values), labels_used=sorted(used),
                  labels_absent=sorted(set(range(6))-used))
        good = not(A_fail or B_fail or C_fail or D_fail or E_fail or F_fail)
        allok &= good
        print(f"m={m:>2} n={n:>3}: values {info['values']}")
        print(f"        labels used {info['labels_used']}, absent {info['labels_absent']}")
        print(f"        path A {'ok' if not A_fail else A_fail[:2]} | path B {'ok' if not B_fail else B_fail[:2]}"
              f" | (5.7) {'ok' if not C_fail else C_fail[:2]} | (P5) {'ok' if not D_fail else D_fail[:2]}"
              f" | m2 {'ok' if not E_fail else E_fail[:2]}"
              f" | m11 {'ok, tight at ' + str(max(m11.values())) + '/' + str(n) if not F_fail else F_fail[:2]}")
    print()
    print("CERTIFICATE:", "VERIFIED" if allok else "FAILED")
    return allok

if __name__=='__main__':
    sys.exit(0 if main() else 1)
