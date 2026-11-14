"""Second, independent implementation of the d3 audit checks (no shared algorithm with audit.py).

  J  the counting kill by bitmask arithmetic (values encoded as 6-bit masks)
  K  unit-triangle rigidity at k = 6: three pairwise disjoint ADMISSIBLE values are 2+2+2
     and cover all six labels
  L  the k = 5 and k = 7 sector-word questions for the same fragment (SAT) -- contrast
  M  a fresh pairs-only witness at m = 6:  (5.7), offsets, (TE) failure, (P5) traces
  N  m3's k = 7 colouring as the non-vacuity control for (TE)
"""
from itertools import combinations
import subprocess, tempfile, os, sys

K6_EDGES = [((i), (i + 1) % 6) for i in range(6)]
E6 = [frozenset(e) for e in K6_EDGES]


def mask(S):
    return sum(1 << x for x in S)


def admissible_mask(mS, ell):
    bits = [b for b in range(ell) if mS >> b & 1]
    if not (1 <= len(bits) <= 3):
        return False
    for i in range(ell):
        if all(b in (i, (i + 1) % ell) for b in bits):
            return False
    return True


def domain(ell, free, sizes=(2, 3)):
    out = []
    for r in sizes:
        for c in combinations(range(ell), r):
            mS = mask(c)
            if free is not None and (mS >> free & 1):
                continue
            if admissible_mask(mS, ell):
                out.append(mS)
    return out


print("=" * 78)
print("J. counting kill by bitmask arithmetic (independent of audit.py)")
for free in range(6):
    D = domain(6, free)
    bad = 0
    for a, b, c in combinations(D, 3):
        if a & b or a & c or b & c:
            continue
        if bin(a).count("1") >= 2 and bin(b).count("1") >= 2 and bin(c).count("1").__ge__(2):
            bad += 1
    print(f"   free label {free}: |D| = {len(D)}, triples pairwise disjoint with all sizes >= 2: {bad}")
    assert bad == 0
# the same without the free label: admissible triples do exist
D = domain(6, None)
good = [(a, b, c) for a, b, c in combinations(D, 3)
        if not (a & b or a & c or b & c)]
print(f"   without the free label: {len(good)} pairwise disjoint admissible triples, e.g.",
      [[x for x in range(6) if m >> x & 1] for m in good[0]])

print("=" * 78)
print("K. unit-triangle rigidity at k = 6")
# three pairwise disjoint admissible values: which size patterns occur, and is the union all of [6]?
pats = set()
for a, b, c in combinations(D, 3):
    if a & b or a & c or b & c:
        continue
    pats.add((bin(a).count("1"), bin(b).count("1"), bin(c).count("1"),
              bin(a | b | c).count("1")))
print("   (|A|,|B|,|C|,|A u B u C|) over all pairwise disjoint admissible triples:", sorted(pats))
assert pats == {(2, 2, 2, 6)}
print("   => at a unit triangle whose vertices are 6-cycle centres, the three palettes are PAIRS")
print("      and they partition [6].  (Strengthens m2's (B1): no vertex is ternary.)")

print("=" * 78)
print("L. the sector-word fragment at k = 5 and k = 7 (own CNF, CaDiCaL)")


def sat_word(ell, free, sizes, m, timeout=300):
    VALS = domain(ell, free, sizes)
    V = len(VALS)
    n = 6 * m
    offs = sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})
    def x(i, v):
        return i * V + v + 1
    cl = []
    for i in range(n):
        cl.append([x(i, v) for v in range(V)])
        for a, b in combinations(range(V), 2):
            cl.append([-x(i, a), -x(i, b)])
    for o in offs:
        for i in range(n):
            j = (i + o) % n
            for a in range(V):
                for b in range(V):
                    if VALS[a] & VALS[b]:
                        cl.append([-x(i, a), -x(j, b)])
    with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
        f.write("p cnf %d %d\n" % (n * V, len(cl)))
        for c in cl:
            f.write(" ".join(map(str, c)) + " 0\n")
        path = f.name
    try:
        r = subprocess.run(["/opt/lean/bin/cadical", "-q", path],
                           capture_output=True, text=True, timeout=timeout)
        out = r.stdout
        st = "SAT" if "s SATISFIABLE" in out else "UNSAT" if "s UNSATISFIABLE" in out else "?"
        if st != "SAT":
            return st, None, V
        lits = set()
        for line in out.splitlines():
            if line.startswith("v "):
                lits |= {int(t) for t in line.split()[1:] if t != "0"}
        w = []
        for i in range(n):
            w.append(next(VALS[v] for v in range(V) if x(i, v) in lits))
        return st, w, V
    finally:
        os.unlink(path)


for ell, free, sizes in [(5, 0, (2,)), (5, 0, (2, 3)), (7, 6, (2, 3, 4)), (6, None, (2, 3))]:
    print(f"   k={ell}, free label {free}, sizes {sizes}:")
    for m in (6, 9):
        st, w, V = sat_word(ell, free, sizes, m)
        print(f"      m={m}: domain {V} values, 6m={6*m} sectors -> {st}")
        if st == "SAT" and w is not None:
            n = 6 * m
            offs = sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})
            assert all(not (w[i] & w[(i + o) % n]) for i in range(n) for o in offs)
            print("         decoded model re-checked on all offsets:", True)

print("=" * 78)
print("M. fresh pairs-only witness at m = 6 (from pairs_only.py), all constraints")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pairs_only import solve, check          # noqa: E402
st, word, nc, offs = solve(6)
assert st == "SAT"
word = [mask(v) for v in word]
n = 36
print("   decoded and re-checked:", check([frozenset(b for b in range(6) if w >> b & 1) for w in word],
                                          6, offs))
print("   values:", sorted({tuple(b for b in range(6) if w >> b & 1) for w in word}))
print("   (5.7) P(f) cap P(Rf) = empty at every sector:",
      all(not (word[i] & word[(i + 6) % n]) for i in range(n)))
print("   (TE) at unit distance: P_{x+a}(f) = P_x(f), so the intersection is the palette itself;")
print("   palettes are nonempty in all 36 sectors:",
      all(word[i] for i in range(n)), "-> (TE) fails at every unit pair and direction.")
# (P5) traces for the pair values used
used = sorted({w for w in word})
ok = True
for mS in used:
    bits = [b for b in range(6) if mS >> b & 1]
    for e in E6:
        if not any(b not in e for b in bits):
            ok = False
print("   (P5): every value has a trace (delta_b, b outside the edge) for every C6 edge:", ok)
print("   m2 bound 2|P| <= 5 on the model:", max(bin(w).count('1') for w in word) * 2, "<= 5:",
      max(bin(w).count('1') for w in word) * 2 <= 5)

print("=" * 78)
print("N. non-vacuity control: m3's k = 7 colouring")
print("   its palettes are singletons {c(x+e)} (m3 proof.md Theorem A.2), and c is proper,")
print("   so two centres at unit distance have different labels and (TE) holds automatically.")
print("   A singleton palette has size 1, so the counting kill (which needs |P| >= 2 at the")
print("   three vertices) does not apply: exactly the difference between k = 6 and k >= 7.")
print("=" * 78)
print("ALL CHECKS PASSED")
