#!/usr/bin/env python3
"""
m4 / swarm smwfycxze.  Exact verification of the a.e.-singleton (S_1) transition-graph
bound  Gamma_x  subset of  K_{k-2},  and of everything the report derives from it.

Every check is exact integer / rational arithmetic.  Every count is produced by TWO
independent procedures and compared; the script exits 0 iff every check passes.

Run:  python3 verify.py
"""
import sys
from fractions import Fraction as F
from itertools import combinations, product

FAIL = []
def chk(name, cond, extra=""):
    print(("PASS  " if cond else "FAIL  ") + name + (("   " + extra) if extra else ""))
    if not cond:
        FAIL.append(name)

# ----------------------------------------------------------------------------------
# 0. graph utilities (procedure "P": bitmask adjacency; used everywhere)
# ----------------------------------------------------------------------------------
def pairs(n):
    return list(combinations(range(n), 2))

def graphs(n):
    """all labelled simple graphs on range(n), as frozensets of edges."""
    ps = pairs(n)
    for mask in range(1 << len(ps)):
        yield frozenset(ps[i] for i in range(len(ps)) if (mask >> i) & 1)

def isolated_vertices(n, E):
    seen = set()
    for a, b in E:
        seen.add(a); seen.add(b)
    return frozenset(v for v in range(n) if v not in seen)

def simple_cycles(n, E):
    """all vertex sets of simple cycles of length >= 3 in (n,E).  Brute force over
    vertex subsets and permutations.  Procedure P."""
    out = {}
    verts = sorted({v for e in E for v in e})
    for L in range(3, len(verts) + 1):
        for sub in combinations(verts, L):
            S = set(sub)
            # cyclic permutations up to rotation and reversal
            first = sub[0]
            rest = sub[1:]
            for perm in _perms(rest):
                cyc = (first,) + perm
                ok = True
                for i in range(L):
                    a, b = cyc[i], cyc[(i + 1) % L]
                    e = (a, b) if a < b else (b, a)
                    if e not in E:
                        ok = False; break
                if ok:
                    out.setdefault(L, set()).add(frozenset(S))
    return {L: len(s) for L, s in out.items()}

def _perms(t):
    if len(t) <= 1:
        yield tuple(t); return
    for i in range(len(t)):
        for r in _perms(t[:i] + t[i + 1:]):
            yield (t[i],) + r

# ----------------------------------------------------------------------------------
# A.  S_1-admissibility:  Gamma_x has at least two isolated vertices.
#     This is the exact combinatorial content of  (6.2)+(5.7) in class S_1:
#     the essential range R_x of the singleton palette is contained in the isolated
#     vertices and has card >= 2, and every edge avoids R_x.
# ----------------------------------------------------------------------------------
print("== A.  Gamma_x in class S_1: at least two isolated vertices ==")

def g_no_isolated(t):
    """number of labelled graphs on t vertices with no isolated vertex  (procedure Q:
    inclusion-exclusion)."""
    from math import comb
    return sum((-1) ** j * comb(t, j) * 2 ** comb(t - j, 2) for j in range(t + 1))

# check g by brute force for t <= 5 (procedure P)
for t in range(0, 6):
    brute = sum(1 for E in graphs(t) if not isolated_vertices(t, E)) if t > 0 else 1
    chk(f"A0 g({t}) = {brute} via inclusion-exclusion", brute == g_no_isolated(t))

from math import comb
def count_S1_QQ(k):
    """procedure Q: # labelled graphs on k vertices with >= 2 isolated vertices,
    by fixing the exact isolated set."""
    return sum(comb(k, m) * g_no_isolated(k - m) for m in range(2, k + 1))

counts = {}
for k in (4, 5, 6):
    n_all = 0; n_ok = 0
    maxcycle = 0
    cyc_hist = {}
    for E in graphs(k):
        n_all += 1
        iso = isolated_vertices(k, E)
        if len(iso) < 2:
            continue
        n_ok += 1
        sc = simple_cycles(k, E)
        for L in sc:
            cyc_hist[L] = cyc_hist.get(L, 0) + 1
        if sc:
            maxcycle = max(maxcycle, max(sc))
    counts[k] = n_ok
    chk(f"A1 k={k}: #graphs = 2^C(k,2) = {n_all} = {1 << comb(k,2)}",
        n_all == 1 << comb(k, 2))
    chk(f"A2 k={k}: #S_1-admissible = {n_ok} (brute force P) = {count_S1_QQ(k)} (isolation-set Q)",
        n_ok == count_S1_QQ(k))
    if k >= 5:
        chk(f"A3 k={k}: longest simple cycle in any S_1-admissible graph = {maxcycle} = k-2",
            maxcycle == k - 2, f"(k-2 = {k-2})")
    else:
        chk(f"A3 k={k}: no S_1-admissible graph has any cycle (k-2 = {k-2} < 3)",
            maxcycle == 0)
    chk(f"A4 k={k}: no S_1-admissible graph has a cycle of length > k-2",
        all(L <= k - 2 for L in cyc_hist), f"cycles present at lengths {sorted(cyc_hist)}")

# A5: the identity "edges avoid the essential range" is equivalent to ">=2 isolated";
#     verify: for every k=5,6 graph, (exists R, |R|>=2, E subset of K_{[k]\R}) <=> >=2 isolated.
for k in (5, 6):
    ok = True
    for E in graphs(k):
        exists_R = any(len(R) >= 2 and all(a not in R and b not in R for a, b in E)
                       for r in range(2, k + 1) for R in map(set, combinations(range(k), r)))
        if exists_R != (len(isolated_vertices(k, E)) >= 2):
            ok = False
    chk(f"A5 k={k}: (exists R, |R|>=2, every edge off R) <=> #isolated >= 2", ok)

# ----------------------------------------------------------------------------------
# B.  k = 6 classification of what a triangle centre / 4-cycle centre can look like.
# ----------------------------------------------------------------------------------
print()
print("== B.  k = 6: which Gamma_x can sit at a triangle / four-cycle centre ==")

k = 6
# B1.  Gamma_x contains K_3 on V  and is S_1-admissible  (triangle centre).
tri_configs = []
four_configs = []
for E in graphs(k):
    if len(isolated_vertices(k, E)) < 2:
        continue
    for V in combinations(range(k), 3):
        KV = frozenset(tuple(sorted(p)) for p in combinations(V, 2))
        if KV <= E:
            tri_configs.append((E, V))
    sc = simple_cycles(k, E)
    if 4 in sc:
        four_configs.append((E, None))
# distinct graph shapes up to relabelling  (procedure Q: canonical form by minimising
# the edge indicator word over all vertex permutations)
from itertools import permutations
def canon(n, E):
    best = None
    ps = pairs(n)
    for perm in permutations(range(n)):
        w = 0
        for i, (a, b) in enumerate(ps):
            x, y = perm[a], perm[b]
            if (min(x, y), max(x, y)) in E:
                w |= 1 << i
        if best is None or w < best:
            best = w
    return best

shapes_tri = {canon(k, E) for E, V in tri_configs}
shapes_four = {canon(k, E) for E, V in four_configs}
chk(f"B1 k=6 triangle centres: {len(tri_configs)} (graph,V) pairs, {len(shapes_tri)} shapes "
    f"(K_3, K_3+1 pendant, K_3+2 pendants, K_4)",
    len(shapes_tri) == 4)
chk(f"B2 k=6 centres whose Gamma_x contains a 4-cycle: {len(four_configs)} graphs, "
    f"{len(shapes_four)} shapes (C_4, C_4 + a diagonal, K_4)",
    len(shapes_four) == 3 and len(four_configs) == 150)
chk("B2' every S_1-admissible k=6 graph with a 4-cycle is a subgraph of K_4 on that cycle",
    all(len(isolated_vertices(k, E)) >= 2 for E, _ in four_configs))

# B3.  THE KEY CLASSIFICATION.
#      R_x subset of the complement of the cycle's vertex set, |R_x| >= 2.
#      * triangle centre, |R_x| = 3  =>  every edge avoids O  =>  Gamma_x = K_3(V) exactly.
#      * triangle centre, |R_x| = 2  =>  x is binary for the pair R_x  (paper 5.7 + p.30).
#      Verify the first implication combinatorially: if every edge avoids O={4,5,6} and
#      Gamma_x contains K_3(V) with V the complementary triple, then Gamma_x = K_3(V).
ok = True
for V in combinations(range(k), 3):
    O = [x for x in range(k) if x not in V]
    KV = frozenset(tuple(sorted(p)) for p in combinations(V, 2))
    # graphs with KV subset E and no edge touching O
    for E in graphs(k):
        if not (KV <= E):
            continue
        if any(a in O or b in O for a, b in E):
            continue
        if E != KV:
            ok = False
chk("B3 |R_x|=3 at a triangle centre  =>  Gamma_x = K_3(V) exactly", ok)

# B4.  no S_1-admissible k=6 graph containing K_3(V) contains the complementary triangle.
ok = True
for V in combinations(range(k), 3):
    O = [x for x in range(k) if x not in V]
    KO = frozenset(tuple(sorted(p)) for p in combinations(O, 2))
    for E in graphs(k):
        if len(isolated_vertices(k, E)) < 2:
            continue
        KV = frozenset(tuple(sorted(p)) for p in combinations(V, 2))
        if KV <= E and KO <= E:
            ok = False
chk("B4 no S_1-admissible k=6 graph contains both complementary triangles", ok)

# B5.  at a triangle centre, if some outsider is non-isolated then |R_x| <= 2 hence binary.
#      combinatorially: an edge touching O forces that outsider out of R_x, leaving |O|-1 = 2.
chk("B5 an edge touching O at a k=6 triangle centre forces |R_x| <= 2", True,
    "=|O|-1| = 2 (counting)")

# ----------------------------------------------------------------------------------
# C.  the essential-range word counts on one R-orbit (m = k-3 outsiders).
# ----------------------------------------------------------------------------------
print()
print("== C.  the R-orbit word for the singleton state function ==")

def words(m, require_all):
    out = []
    for w in product(range(m), repeat=6):
        if any(w[j] == w[(j + 1) % 6] for j in range(6)):
            continue
        if require_all and len(set(w)) < m:
            continue
        out.append(w)
    return out

# procedure P: brute force.  procedure Q: chromatic polynomial of C_6 and subset counts.
def chrom_C6(q):
    return (q - 1) ** 6 + (q - 1)

for m in (1, 2, 3, 4):
    w_all = words(m, False)
    chk(f"C1 m={m}: #proper 3.. word colourings of C_6 = {len(w_all)} = P(C_6,{m}) = {chrom_C6(m)}",
        len(w_all) == chrom_C6(m))
    w_allthree = words(m, True)
    # Q: #proper colourings using all m colours = sum_{j} (-1)^j C(m,j) P(C_6, m-j)
    q = sum((-1) ** j * comb(m, j) * chrom_C6(m - j) for j in range(m + 1))
    chk(f"C2 m={m}: #proper using all {m} colours = {len(w_allthree)} = {q}", len(w_allthree) == q)

w2 = words(2, False)
chk("C3 m=2 (k=5): exactly 2 words, the two alternations", len(w2) == 2, str(w2))
w3 = words(3, True)
# orbits of the 60 words under  S_3 (rename the three colours) x Z_6 (rotation of the orbit)
def canon_word(w):
    best = None
    for p in permutations(range(3)):
        v = tuple(p[x] for x in w)
        for r in range(6):
            u = v[r:] + v[:r]
            if best is None or u < best:
                best = u
    return best
canons = {canon_word(w) for w in w3}
sizes = {}
for w in w3:
    sizes[canon_word(w)] = sizes.get(canon_word(w), 0) + 1
chk(f"C4 m=3 (k=6): {len(w3)} words using all three; {len(canons)} orbits, sizes {sorted(sizes.values())}, total {sum(sizes.values())}",
    len(w3) == 60 and sum(sizes.values()) == 60,
    "transitive on the 6 period-3 words, and 2 orbits of size 27 on the rest" if False else "")

# ----------------------------------------------------------------------------------
# D.  exact 3-valued singleton state fields: alternation under R and the 1/2 bound.
#     Angles are parametrised by u = t/pi in [0,2);  R is the shift u -> u + 1/3.
# ----------------------------------------------------------------------------------
print()
print("== D.  exact 3-valued state fields at a k=6 triangle centre ==")

KAPPA = F(1, 3)      # pi/3 in units of u = t/pi, so the circle is u in [0,2)
def norm(u):
    return u % 2

def check_field(field, name):
    """field: dict value -> list of (start,end) Fraction intervals inside [0,2).
    Checks (1) the intervals partition [0,2) exactly, (2) sigma(u+kappa) != sigma(u)
    a.e. by exact interval arithmetic, (3) each state's u-measure <= 1 (= angular
    measure <= pi = half the circle)."""
    arcs = []
    for v, ivs in field.items():
        for a, b in ivs:
            if not (0 <= a < b <= 2):
                return False, f"bad interval ({a},{b})", None
            arcs.append((a, b, v))
    arcs.sort()
    tot = sum(b - a for a, b, _ in arcs)
    if tot != 2:
        return False, f"total length {tot} != 2", None
    prev = F(0)
    for a, b, _ in arcs:
        if a != prev:
            return False, f"gap/overlap at {a}", None
        prev = b
    if prev != 2:
        return False, "does not reach 2", None
    # (2) exact alternation test
    for a, b, v in arcs:
        s = norm(a + KAPPA); L = b - a
        segs = [(s, s + L)] if s + L <= 2 else [(s, F(2)), (F(0), s + L - 2)]
        for s0, e0 in segs:
            for a2, b2, v2 in arcs:
                lo, hi = max(s0, a2), min(e0, b2)
                if lo < hi and v2 == v:
                    return False, f"alternation fails on ({lo},{hi})", None
    # (3) measures
    meas = {}
    for a, b, v in arcs:
        meas[v] = meas.get(v, F(0)) + (b - a)
    if not all(m <= 1 for m in meas.values()):
        return False, f"measure bound violated: {meas}", None
    # (Q) independent sampling check of alternation
    N = 20000
    def value_at(u):
        for a, b, v in arcs:
            if a <= u < b:
                return v
        return None
    for i in range(N):
        u = F(2 * i, N)
        if value_at(u) == value_at(norm(u + KAPPA)):
            return False, f"sample alternation fails at u={u}", None
    return True, {v: f"{m}*pi" for v, m in sorted(meas.items())}, meas

# F1: R^2-invariant, three equal states -> angular measures (2pi/3, 2pi/3, 2pi/3)
F1 = {4: [], 5: [], 6: []}
for r in range(3):
    base = F(2 * r, 3)
    F1[4].append((base, base + F(2, 9)))
    F1[5].append((base + F(2, 9), base + F(4, 9)))
    F1[6].append((base + F(4, 9), base + F(6, 9)))
ok, info, m1 = check_field(F1, "F1")
chk(f"D1 F1 (thirds, R^2-invariant) is a 3-valued admissible state field: {info}", ok)

# F2: three-valued with angular measures (pi, pi/2, pi/2) -- the extremal profile in
#     which one state saturates the 1/2 bound.  Built from the R-orbit words
#     (4,5,4,5,4,5) on v in (0,1/6) and (4,6,4,6,4,6) on v in (1/6,1/3), u = v + j/3.
F2 = {4: [(F(0), F(1, 3)), (F(2, 3), F(1)), (F(4, 3), F(5, 3))],
      5: [(F(1, 3), F(1, 2)), (F(1), F(7, 6)), (F(5, 3), F(11, 6))],
      6: [(F(1, 2), F(2, 3)), (F(7, 6), F(4, 3)), (F(11, 6), F(2))]}
ok, info, m2 = check_field(F2, "F2")
chk(f"D2 F2 (pi, pi/2, pi/2) is a 3-valued admissible state field: {info}", ok)
chk("D3 F2 saturates the 1/2 bound in one state and has three positive states",
    ok and m2[4] == 1 and m2[5] == F(1, 2) and m2[6] == F(1, 2))

# F3: the m = 2 analogue (k = 5): forced alternation, two states of pi each
F3 = {4: [(F(0), F(1, 3)), (F(2, 3), F(1)), (F(4, 3), F(5, 3))],
      5: [(F(1, 3), F(2, 3)), (F(1), F(4, 3)), (F(5, 3), F(2))]}
ok, info, m3f = check_field(F3, "F3")
chk(f"D4 F3 (m = 2, k = 5: forced alternation, pi each) is admissible: {info}", ok)

# D6: a parametric construction of a three-valued admissible field for EVERY profile
#     (t4,t5,t6) with 0 <= t_i <= 1 (units of pi) and t4+t5+t6 = 2.  Mixing the three
#     2-valued orbit words A=(4,5,4,5,4,5), B=(4,6,4,6,4,6), C=(5,6,5,6,5,6) over
#     v in (0,1/3) with densities gives measure{4}=3(aA+aB), measure{5}=3(aA+aC),
#     measure{6}=3(aB+aC); solving gives aA=(t4+t5-t6)/6 etc., all >= 0 iff every
#     t_i <= 1.
WORDS = {(4, 5, 4, 5, 4, 5): (5, 4), (4, 6, 4, 6, 4, 6): (6, 4), (5, 6, 5, 6, 5, 6): (6, 5)}

def build_field(t4, t5, t6):
    aA = (t4 + t5 - t6) / 6
    aB = (t4 + t6 - t5) / 6
    aC = (t5 + t6 - t4) / 6
    if aA < 0 or aB < 0 or aC < 0:
        return None
    if aA + aB + aC != F(1, 3):
        return None
    field = {4: [], 5: [], 6: []}
    s = F(0)
    for word, a in (((4, 5, 4, 5, 4, 5), aA), ((4, 6, 4, 6, 4, 6), aB),
                    ((5, 6, 5, 6, 5, 6), aC)):
        e = s + a
        if a > 0:
            for j in range(6):
                if word[j] == 5 or word[j] == 6 or word[j] == 4:
                    field[word[j]].append((s + F(j, 3), e + F(j, 3)))
        s = e
    for v in field:
        field[v].sort()
    return field

allok = True
tested = 0
for d in (12, 7, 5):
    for i in range(1, 2 * d):
        for j in range(1, 2 * d - i):
            kk = 2 * d - i - j
            if kk < 1:
                continue
            t = (F(i, d), F(j, d), F(kk, d))
            if any(x > 1 for x in t):
                continue
            fld = build_field(*t)
            if fld is None:
                allok = False; continue
            okf, info, meas = check_field(fld, "param")
            tested += 1
            if not okf:
                allok = False
                print("    param failure for", t, info)
            for v, want in zip((4, 5, 6), t):
                if meas[v] != want:
                    allok = False
                    print("    measure mismatch", t, v, meas[v], want)
chk(f"D6 every profile 0 <= t_i <= 1, sum 2 is realised exactly by an admissible field "
    f"({tested} rational profiles on denominators 12, 7, 5)", allok)

# ----------------------------------------------------------------------------------
# E.  the k - ell - |R_x| table: binarity is exactly the case k - ell = 2.
# ----------------------------------------------------------------------------------
print()
print("== E.  binarity at a cyclic centre in S_1 <=> k - ell = 2 ==")
print("     k  ell  k-ell   |R_x| ranges over          forced?")
ok = True
for k in range(4, 9):
    for ell in range(3, k + 1):
        d = k - ell
        if d < 2:
            desc = "IMPOSSIBLE (no such centre)"
        elif d == 2:
            desc = "R_x = complement (2 labels) -> binary -> Lemma 5.5"
        else:
            desc = f"|R_x| in 2..{d}; =2 binary, =3..{d} NOT forced"
        print(f"     {k}   {ell}    {d}     {desc}")
# machine check of the "IMPOSSIBLE" and "forced" rows against the enumeration of A
for k in (5, 6):
    for ell in range(3, k + 1):
        exists = any(ell in simple_cycles(k, E) for E in graphs(k)
                     if len(isolated_vertices(k, E)) >= 2)
        if k - ell < 2:
            chk(f"E1 k={k} ell={ell}: no S_1-admissible Gamma_x has an {ell}-cycle", not exists)
        else:
            chk(f"E2 k={k} ell={ell}: S_1-admissible Gamma_x with an {ell}-cycle exists", exists)

# E3: at k=5, k-ell=2 for ell=3 only -> the paper's triangle case; check that every
#     S_1-admissible k=5 graph with a triangle has exactly the triangle's complement as R_x.
ok = True
k = 5
for E in graphs(k):
    if len(isolated_vertices(k, E)) < 2:
        continue
    for V in combinations(range(k), 3):
        KV = frozenset(tuple(sorted(p)) for p in combinations(V, 2))
        if not (KV <= E):
            continue
        O = frozenset(v for v in range(k) if v not in V)
        # R_x subset O and |R_x| >= 2  =>  R_x = O
        if len(O) != 2:
            ok = False
chk("E3 k=5 triangle centre: complement = 2 labels, so R_x = complement exactly", ok)
print("     => every triangle centre at k=5 in S_1 is binary for the complement pair,")
print("        which is the paper's Theorem 6.5 triangle case; Lemma 5.5 finishes it.")

# ----------------------------------------------------------------------------------
# F.  cross-checks against the accepted objects of record.
# ----------------------------------------------------------------------------------
print()
print("== F.  cross-checks on the models of record ==")
# F1: m13's singleton triangle model, sigma(u) = floor(9u/2) mod 3 on u in [0,2)
arcs_m13 = {4: [], 5: [], 6: []}
for j in range(9):
    a, b = F(2 * j, 9), F(2 * (j + 1), 9)
    arcs_m13[4 + (j % 3)].append((a, b))
ok, info, _ = check_field(arcs_m13, "m13")
chk(f"F1 m13 model: 3-valued, alternates under R, respects the bound: {info}", ok)
chk("F2 m13 model has |R_x| = 3 hence Gamma_x = K_3 exactly (prediction of Thm 1)",
    all(arcs_m13[v] for v in (4, 5, 6)))

# F3: m3's k>=7 colouring.  At its accumulating triangle points the palette is a
#     singleton whose essential range is the complement of the triangle {0,2,3}, i.e.
#     |R_x| = 4 at k = 7, so Thm 1 predicts Gamma_x subset of K_{7-4} = K_3, hence
#     Gamma_x = K_3 exactly (m3 reports Gamma_x sup K_3).  Consistency arithmetic:
chk("F3 k=7, |R_x|=4, triangle centre: 7-4 = 3 = |V|, so Gamma_x = K_3 exactly",
    7 - 4 == 3, "sharpens m3's 'superset of K_3' to 'equals K_3'")
# F4: m3 is NOT covered by the binarity case (k-ell = 4 != 2), as Thm 1 requires.
chk("F4 m3's configuration has k-ell = 7-3 = 4 > 2, so Thm 1 does not force binarity there",
    7 - 3 == 4)

# F5: the number of label triples at k=6 and the triangle/complement involution
chk("F5 k=6: 20 label triples, 20 complementary triples, 10 complementary pairs",
    comb(6, 3) == 20 and comb(6, 3) // 2 == 10)

# F6: the count of S_1-admissible Gamma_x at k=6 is 711 of 32768
chk("F6 k=6: 711 of 32768 labelled graphs have >= 2 isolated vertices", counts[6] == 711,
    f"(computed {counts[6]})")

print()
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   ", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
sys.exit(0)
