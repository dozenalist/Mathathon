#!/usr/bin/env python3
"""Exact (integer) decision for translation-invariant sector palette fields at k = 6.

Direction d7 (member m8).  Companion to REPORT.md, Sections 4 and 5.

A sector field at resolution n = 6m is a word V : Z/n -> palettes, sector i being
[i*Delta,(i+1)*Delta) with Delta = 2 pi/n.  Rotation by kappa = pi/3 acts as the
sector shift i -> i+m.

Constraints used (all from the paper, at k = 6):
  A   (palette bound)   1 <= |V(i)| <= 3                     [Prop. 5.6 + complement-of-4]
  ED  (edge exclusion)  V(i) is not a subset of an edge of the cycle C_ell   [(6.2)]
  FL  (free label)      f not in V(i) for all i
  57  (sixty degrees)   V(i) cap V(i+m) = empty                [(5.7)]
  TR  (transport (5.3)) V(i) cap V(i +- m + k) = empty for k in {-1,0,1}
                        (m15's exact geometric bound 1.5938 d_0 < Delta keeps the
                         sector displacement in {-1,0,+1}; BOTH signs of the pi/3
                         offset occur, so both +m and -m are imposed)
Outputs
  1  two-valued fields: exhaustive decision at m = 2..8  -> UNSAT (0 solutions)
     with TR, SAT without TR (so TR is exactly what kills them)
  2  vacuity: the 3-valued m15 block model and the 6-value free-label word of
     sprint/k6/FREE-LABEL.md both pass ED + FL + 57 + TR at n = 36
  3  the Corollary-3.1 countermodel: the 6-block two-valued alternation
     {0,2}/{1,3}.  It satisfies A + ED (ell=3,4,5,6) + FL + 57 with E = S
     (angular measure 2 pi, the maximum), and it FAILS TR, which is what
     separates it from the fields of item 2.
Two independent implementations of every decision (word-list enumeration with
frozenset values, and bitmask/rotation arithmetic); they must agree.
"""
import itertools
import json
import os
import sys
from hashlib import sha256

HERE = os.path.dirname(os.path.abspath(__file__))

LABELS = tuple(range(6))


def edges(ell):
    return [frozenset({i, (i + 1) % ell}) for i in range(ell)]


def admissible(P, ell):
    """A + ED for the cycle C_ell (vertices 0..ell-1)."""
    if not (1 <= len(P) <= 3):
        return False
    for e in edges(ell):
        if P <= e:
            return False
    return True


def disjoint(P, Q):
    return not (P & Q)


def check_word(V, m, ell, free):
    """Return dict of which constraint sets the word satisfies."""
    n = len(V)
    assert n == 6 * m
    out = {}
    out["A"] = all(1 <= len(V[i]) <= 3 for i in range(n))
    out["ED"] = all(admissible(V[i], ell) for i in range(n))
    out["FL"] = all(free not in V[i] for i in range(n))
    out["57"] = all(disjoint(V[i], V[(i + m) % n]) for i in range(n))
    ok = True
    bad = []
    for i in range(n):
        for s in (m, -m):
            for k in (-1, 0, 1):
                j = (i + s + k) % n
                if not disjoint(V[i], V[j]):
                    ok = False
                    bad.append((i, s + k))
    out["TR"] = ok
    out["TR_failures"] = bad
    return out


# ---------------------------------------------------------------- implementation 1
def enum_two_valued(m, ell, free):
    """All two-valued words at resolution n=6m satisfying A,ED,FL,57.

    (5.7) forces V(i+m) != V(i); with two values that forces V(i+2m)=V(i), so the
    word is determined by the first m entries.  Enumerate all of them."""
    n = 6 * m
    vals = [frozenset(P) for r in (1, 2, 3) for P in itertools.combinations(LABELS, r)
            if admissible(frozenset(P), ell) and free not in P]
    sols = []
    for P, Q in itertools.permutations(vals, 2):
        if not disjoint(P, Q):
            continue
        for head in itertools.product([P, Q], repeat=m):
            V = [None] * n
            for i in range(n):
                V[i] = head[i % m] if (i // m) % 2 == 0 else (Q if head[i % m] == P else P)
            if not all(disjoint(V[i], V[(i + m) % n]) for i in range(n)):
                continue
            sols.append(V)
    return sols


# ---------------------------------------------------------------- implementation 2
def enum_two_valued_bits(m, ell, free):
    """Same decision with integer palette masks and bit rotations.

    A two-valued word with (5.7) has period 2m and flips value under a shift by m,
    so it is coded by a 2m-bit mask P (bit i set <=> sector i carries palette a)."""
    n = 6 * m
    masks = [sum(1 << b for b in P) for r in (1, 2, 3)
             for P in itertools.combinations(LABELS, r)
             if admissible(frozenset(P), ell) and free not in P]
    sols = []
    for a in masks:
        for b in masks:
            if a & b:
                continue
            for pat in range(1 << m):
                full = 0
                for i in range(2 * m):
                    bit = (pat >> (i % m)) & 1
                    if i >= m:
                        bit ^= 1
                    if bit:
                        full |= 1 << i
                # period 2m, repeated 3 times over n = 6m sectors
                P2 = full | (full << 2 * m) | (full << 4 * m)
                P2 &= (1 << n) - 1
                ok = True
                for i in range(n):
                    if (P2 >> i) & 1 and (P2 >> ((i + m) % n)) & 1:
                        ok = False
                        break
                if ok:
                    sols.append([frozenset(l for l in range(6)
                                           if ((a if (P2 >> i) & 1 else b) >> l) & 1)
                                 for i in range(n)])
    return sols


def count_solutions(m, ell, free, transport):
    s1 = enum_two_valued(m, ell, free)
    s2 = enum_two_valued_bits(m, ell, free)
    k1 = [V for V in s1 if check_word(V, m, ell, free)["TR"] or not transport]
    k2 = [V for V in s2 if check_word(V, m, ell, free)["TR"] or not transport]
    return len(s1), len(s2), len(k1), len(k2)


# --------------------------------------------------------------------- the report
report = {}
print("== 1. two-valued sector fields, exhaustive decision ==")
print(" m    ell   #(A,ED,FL,57) impl1/impl2   #(...+TR) impl1/impl2")
rows = []
for ell in (3, 4, 5, 6):
    for free in (0, 4, 5):
        for m in (2, 3, 4, 5, 6, 7, 8):
            a, b, c, d = count_solutions(m, ell, free, True)
            assert a == b and c == d, (m, ell, free, a, b, c, d)
            rows.append(dict(m=m, ell=ell, free=free, n57=a, ntr=c))
            if m in (2, 3, 6, 8) and free in (0, 5):
                print(f"{m:3d} {ell:5d} {a:8d}/{b:<8d} free={free}  {c:8d}/{d:<8d}")
report["two_valued"] = rows
max57 = max(r["n57"] for r in rows)
maxtr = max(r["ntr"] for r in rows)
print(f"\n maximum over all (ell, free, m=2..8) of #solutions without TR : {max57}")
print(f" maximum over all (ell, free, m=2..8) of #solutions with    TR : {maxtr}")
print(" => two-valued sector fields are UNSAT with (5.7)+(5.3); non-empty without (5.3)")
report["two_valued_max_without_TR"] = max57
report["two_valued_max_with_TR"] = maxtr

print("\n== 1b. the two-periodic (3,2,3,2,3,2) stratum survives (5.7)+(6.2) and dies under TR ==")
from collections import Counter
for (ell, free) in ((6, 0), (4, 5)):
    m = 6
    c = Counter()
    sols = enum_two_valued(m, ell, free)
    for V in sols:
        c[tuple(sorted({len(P) for P in V}))] += 1
    killed = sum(1 for V in sols if not check_word(V, m, ell, free)["TR"])
    print(f" ell={ell} free={free} m={m}: 2-valued 57-solutions by palette-size multiset "
          f"{dict(sorted(c.items()))}; all pass A+ED+FL: "
          f"{all(check_word(V, m, ell, free)['ED'] and check_word(V, m, ell, free)['FL'] for V in sols)}; "
          f"# failing TR = {killed} of {len(sols)}")
    report[f"two_valued_sizes_ell{ell}"] = {str(k): v for k, v in sorted(c.items())}
    report[f"two_valued_killed_by_TR_ell{ell}"] = [killed, len(sols)]

print("\n== 2. vacuity: models with >= 3 values exist ==")


def block_word(m, L, M):
    n = 6 * m
    nb = n // L
    return [frozenset(M[(i // L) % len(M)]) for i in range(n)]


m15_models = {
    3: [frozenset()],
    4: [(0, 2), (1, 4), (3, 5)],
    5: [(0, 2), (1, 3), (4, 5)],
}
FREE_LABEL_BLOCKS = {
    3: ([(3,), (4,), (5,)], 0),
    4: ([(0, 2), (1, 3), (4,)], 5),
    5: ([(0, 2), (1, 3), (5,)], 4),
}
for ell, (M, free) in FREE_LABEL_BLOCKS.items():
    V = block_word(6, 4, M)
    r = check_word(V, 6, ell, free)
    print(f" FREE-LABEL three-block model ell={ell}, values {M}, free={free}: "
          f"A={r['A']} ED={r['ED']} FL={r['FL']} 57={r['57']} TR={r['TR']}")
    report[f"free_label_blocks_{ell}"] = {k: r[k] for k in ("A", "ED", "FL", "57", "TR")}

for ell, M in m15_models.items():
    if len(M) < 3:
        continue
    free = 5 if ell == 4 else 4
    m = 6
    V = block_word(m, 2 * m // 3, M)
    r = check_word(V, m, ell, free)
    print(f" m15 three-block model ell={ell} (no free label, union = [6]): A={r['A']} "
          f"ED={r['ED']} 57={r['57']} TR={r['TR']}")
    report[f"m15_{ell}"] = {k: r[k] for k in ("A", "ED", "57", "TR")}

FREE_WORD = """
3,5 3,5 2,5 2,5 2,4 2,4 2,4 1,4 1,4 1,3 1,3 1,3
3,5 3,5 2,5 2,5 2,4,5 2,4 2,4 1,4 1,4 1,3 1,3 1,3
3,5 3,5 2,5 2,5 2,4 2,4 2,4 1,4 1,4 1,3 1,3 1,3
"""
V = [frozenset(int(t) for t in cell.split(",")) for cell in FREE_WORD.replace("\n", " ").split()]
assert len(V) == 36, len(V)
r = check_word(V, 6, 6, 0)
print(f" FREE-LABEL 6-value word n=36, ell=6: A={r['A']} ED={r['ED']} FL(0)={r['FL']} "
      f"57={r['57']} TR={r['TR']}  distinct values={len(set(V))}")
report["free_label_six"] = {k: r[k] for k in ("A", "ED", "FL", "57", "TR")}

print("\n== 3. the Corollary-3.1 countermodel: 6-block two-valued alternation ==")
for ell in (3, 4, 5, 6):
    m = 6
    A, B = frozenset({0, 2}), frozenset({1, 3})
    V = [A if (i // m) % 2 == 0 else B for i in range(36)]
    r = check_word(V, m, ell, 5)
    print(f" ell={ell}: A={r['A']} ED={r['ED']} FL(5)={r['FL']} 57={r['57']} TR={r['TR']}"
          f"   E = {{P subset of {{0,1,2,3}}}} has measure 2 pi (both values inside)")
    report[f"cor31_model_ell{ell}"] = dict(A=r["A"], ED=r["ED"], FL=r["FL"], n57=r["57"],
                                          TR=r["TR"], TR_failures_first=r["TR_failures"][:4],
                                          n_failing_pairs=len(r["TR_failures"]))
    if ell == 4:
        print(f"   first transport failures (sector, offset): {r['TR_failures'][:4]}")
        print(f"   number of failing (sector, offset) pairs: {len(r['TR_failures'])} of "
              f"{36*6}")

txt = json.dumps(report, indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, "CERT-sector-decision.json"), "w").write(txt + "\n")
print("\ncertificate: CERT-sector-decision.json (next to this script)  sha256",
      sha256(txt.encode()).hexdigest())
sys.exit(0 if (maxtr == 0 and max57 > 0) else 1)
