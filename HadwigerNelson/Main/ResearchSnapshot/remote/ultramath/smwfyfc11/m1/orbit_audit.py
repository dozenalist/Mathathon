"""C3 audit: damage assessment on REPORT.md sec.6 orbit-word counts.

Independent re-implementation (bitmask DFS + counting only, no word storage).
Constraints, exactly as listed in sprint/k6/REPORT.md sec.6:
  1. (SA)  i notin P_x(e) a.e.                 -> encoded by the ALPHABET
  2. (5.7) P_x(e) cap P_x(Re) = empty          -> ok_adj: a & b == 0
  3. (SA2) |P_x(e)|=3 -> |P_x(Re)|<=2          -> ok_adj: not(pc(a)==3 and pc(b)==3)
  4. (SING) |P|={b} -> b notin V               -> ok_adj
  5. (MON) |P_j|+|P_{j+2}|=5, disjoint -> no   -> ok_mon
  plus (C1) no two complementary triples, and (C2) at most 3 ternary palettes.

modes:
  'full'    : published. alphabet = nonempty subsets of [6]\\{i}, size<=3, not a subset
              of any cycle edge; all five constraints + C1 + C2.
  'noSA'    : constraint 1 deleted  (i may appear in palettes).
  'weakSA'  : constraint 1 weakened to "P_x(e) != {i}".
options (sensitivity, reported separately):
  sa2       : keep constraint 3 as an independent axiom (True) or not (False)
  mon       : 'published'  -> forbid any disjoint distance-2 pair with total size 5
              'icompl'     -> forbid only when the complement of the pair is exactly {i}
                              (the form justified by (5.2)+properness alone)
"""
import sys
from itertools import combinations

K = 6
PC = [bin(m).count('1') for m in range(1 << K)]
TRIPLES = [sum(1 << x for x in c) for c in combinations(range(K), 3)]
# pair-class of a triple = its complementary pair {T, T^c} within the 20 triples
TPAIR = {}
for t in TRIPLES:
    comp = t ^ ((1 << K) - 1)
    TPAIR[t] = min(t, comp)


def alphabet(ell, i, mode):
    V = set(range(ell))
    avail = [x for x in range(K)] if mode in ('noSA', 'weakSA') else [x for x in range(K) if x != i]
    out = []
    for r in range(1, 4):
        for c in combinations(avail, r):
            P = sum(1 << x for x in c)
            if mode == 'weakSA' and P == (1 << i):
                continue
            if all(P & ~((1 << j) | (1 << ((j + 1) % ell))) for j in range(ell)):
                out.append(P)
    return out


def count(ell, i, mode='full', sa2=True, mon='published'):
    A = alphabet(ell, i, mode)
    n = len(A)
    if mon == 'icompl':
        target = ((1 << K) - 1) ^ (1 << i)      # complement must be exactly {i}
        def mon_ok(a, b):
            return not (PC[a] + PC[b] == 5 and (a & b) == 0 and (a | b) == target)
    elif mon == 'none':
        def mon_ok(a, b):
            return True
    else:
        def mon_ok(a, b):
            return not (PC[a] + PC[b] == 5 and (a & b) == 0)
    adj = [[False] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            a, b = A[x], A[y]
            if a & b:
                continue
            if sa2 and PC[a] == 3 and PC[b] > 2:
                continue
            if PC[b] == 1 and ((b & -b).bit_length() - 1) in set(range(ell)):
                continue
            adj[x][y] = True
    # pair-class index for C1
    cls = [TPAIR.get(A[x], -1) for x in range(n)]
    tern = [PC[A[x]] == 3 for x in range(n)]
    cnt = 0
    # iterative-free recursion of depth 6 over indices
    def rec(pos, w, used, ntern):
        nonlocal cnt
        if pos == 6:
            if not adj[w[5]][w[0]]:
                return
            if not mon_ok(A[w[4]], A[w[0]]):
                return
            if not mon_ok(A[w[5]], A[w[1]]):
                return
            cnt += 1
            return
        prev = w[pos - 1]
        for b in range(n):
            if not adj[prev][b]:
                continue
            if pos >= 2 and not mon_ok(A[w[pos - 2]], A[b]):
                continue
            if tern[b]:
                if ntern == 3:
                    continue
                # (C1) no two COMPLEMENTARY triples anywhere (identical repeats are fine)
                if any((A[b] & A[t]) == 0 for t in used):
                    continue
                used.append(b)
                w.append(b)
                rec(pos + 1, w, used, ntern + 1)
                w.pop()
                used.pop()
            else:
                w.append(b)
                rec(pos + 1, w, used, ntern)
                w.pop()
    for a0 in range(n):
        u = [a0] if tern[a0] else []
        rec(1, [a0], u, 1 if tern[a0] else 0)
    return n, cnt


ROWS = [(3, 0, 'in'), (3, 3, 'out'), (4, 0, 'in'), (4, 4, 'out'),
        (5, 0, 'in'), (5, 5, 'out'), (6, 0, 'in')]

if __name__ == '__main__':
    print("== published (mode=full, sa2=True, mon='published') ==")
    pub = {}
    for ell, i, lab in ROWS:
        nA, c = count(ell, i, 'full')
        pub[(ell, lab)] = c
        print(f"ell={ell} centre={lab:3s} |A|={nA:2d} words={c}")
    print("published table:", [pub[(e, l)] for e, _, l in ROWS])


def variants():
    import time
    print("\n== (i) constraint 1 DELETED (i may appear in palettes) ==")
    for ell in (3, 4, 5, 6):
        vals = []
        for i in (0, ell if ell < 6 else 0):
            t = time.time()
            nA, c = count(ell, i, 'noSA', sa2=True, mon='published')
            vals.append((i, nA, c, round(time.time() - t, 1)))
        print(f"ell={ell}: " + "  ".join(f"i={i} |A|={nA} words={c} ({dt}s)" for i, nA, c, dt in vals))
    print("\n== (ii) constraint 1 WEAKENED to P_x(e) != {i} ==")
    for ell in (3, 4, 5, 6):
        vals = []
        for i in (0, ell if ell < 6 else 0):
            t = time.time()
            nA, c = count(ell, i, 'weakSA', sa2=True, mon='published')
            vals.append((i, nA, c, round(time.time() - t, 1)))
        print(f"ell={ell}: " + "  ".join(f"i={i} |A|={nA} words={c} ({dt}s)" for i, nA, c, dt in vals))
    print("\n== refinement: constraint 1 AND its consequence constraint 3 (SA2) deleted,")
    print("   MON in the (5.2)+properness form (complement of the pair must be exactly {i}) ==")
    for ell in (3, 4, 5, 6):
        vals = []
        for i in (0, ell if ell < 6 else 0):
            t = time.time()
            nA, c = count(ell, i, 'noSA', sa2=False, mon='icompl')
            vals.append((i, nA, c, round(time.time() - t, 1)))
        print(f"ell={ell}: " + "  ".join(f"i={i} |A|={nA} words={c} ({dt}s)" for i, nA, c, dt in vals))

    print("\n== (5.7) ALONE: drop 1,3,5 (only disjointness of adjacent palettes, SING, C1, C2) ==")
    for ell in (3, 4, 5, 6):
        nA, c = count(ell, 0, 'noSA', sa2=False, mon='none')
        print(f"ell={ell}: |A|={nA} words={c}")


if __name__ == '__main__':
    variants()
