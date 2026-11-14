#!/usr/bin/env python3
"""
================================================================================
The Section 8 strip layer at k colours: exact decision, certificate, and the
six-colour verdict.
================================================================================

Run:   python3 verify.py            (prints every table below; ~2 s)

CONTENTS
  S1  the model (constraint system STRIP(k,ell)) and a from-scratch checker
  S2  decision procedure 1: exhaustive over phase vectors + product-graph cycle
  S3  decision procedure 2: propositional CNF + DPLL (independent formulation)
  S4  closed-form satisfying word for every k >= 6 (the theorem of RESULTS.md)
  S5  exact rational certificate for the six-colour six-cycle case
  S6  main: full table for 4 <= k <= 7, the two-procedure cross-check, the
      construction for 4 <= k <= 40, and the exact certificate

MODELLING NOTE (see RESULTS.md for the derivation from the paper)
  x is a cyclic centre; K_j, v_j (j = 0..ell-1) are the exclusion continua and
  limiting directions of Proposition 7.1 for a simple label cycle of length ell
  on labels 0..ell-1; edge i joins i and i+1 mod ell.  R = rotation by pi/3,
  theta_j = j*pi/3, e a unit direction with R^j e not perpendicular to any v_i.
      sigma(i,j) = sign(cos(theta_j - arg v_i))        (sign of edge i at R^j e)
  The open semicircle {u : u.v_i > 0} contains exactly three of the six
  directions R^j e, and they are consecutive, so sigma(i,.) is a run of three
  consecutive positions: sigma(i,j)=+1 iff j in {delta_i, delta_i+1, delta_i+2}.
      O_j = labels that are not an endpoint of a POSITIVE edge at R^j e
      I_j = labels that are not an endpoint of a NEGATIVE edge at R^j e
      (labels outside the cycle are endpoints of no edge, so lie in both)
  Constraints used by the paper in this range (Lemma 8.1, Corollary 5.4,
  general-k palette bound, optionally Lemma 6.2):
      S0  O_j != empty and I_j != empty
      S1  1 <= |P_j| <= k-3
      S2  P_j meets O_j and P_j meets I_j
      S3  P_j and P_{j+1} are disjoint (indices mod 6)
      S4  (optional) P_j is not contained in a cycle edge
"""
import itertools
from fractions import Fraction

# =============================================================================
# S1  MODEL + CHECKER
# =============================================================================
def runs_of(delta, ell):
    return [frozenset({(delta[i] + t) % 6 for t in range(3)}) for i in range(ell)]

def allowed(k, ell, delta):
    R = runs_of(delta, ell)
    out = []
    for j in range(6):
        pos, neg = set(), set()
        for i in range(ell):
            ends = {i, (i + 1) % ell}
            if j in R[i]:
                pos |= ends
            else:
                neg |= ends
        out.append((frozenset(set(range(k)) - pos), frozenset(set(range(k)) - neg)))
    return out

def cycle_edges(ell):
    return [frozenset({i, (i + 1) % ell}) for i in range(ell)]

def check(k, ell, delta, word, strong=False):
    """Verify a certificate from scratch; return the list of violations."""
    bad = []
    if len(delta) != ell or len(word) != 6:
        return ["arity"]
    if any(not (0 <= d < 6) for d in delta):
        return ["delta out of range"]
    AI = allowed(k, ell, delta)
    for j, (O, I) in enumerate(AI):
        if not O or not I:
            bad.append("S0 at j=%d" % j)
        P = frozenset(word[j])
        if not (1 <= len(P) <= k - 3):
            bad.append("S1 at j=%d (|P|=%d)" % (j, len(P)))
        if not (P & O):
            bad.append("S2/O at j=%d" % j)
        if not (P & I):
            bad.append("S2/I at j=%d" % j)
    for j in range(6):
        if frozenset(word[j]) & frozenset(word[(j + 1) % 6]):
            bad.append("S3 between j=%d and j=%d" % (j, (j + 1) % 6))
    if strong:
        CE = cycle_edges(ell)
        for j in range(6):
            P = frozenset(word[j])
            for ed in CE:
                if P <= ed:
                    bad.append("S4 at j=%d (palette inside edge %s)" % (j, sorted(ed)))
    return bad

# =============================================================================
# S2  PROCEDURE 1: exhaustive over delta, product-graph search for a word
# =============================================================================
def p1_options(k, ell, O, I, strong):
    cap = k - 3
    CE = cycle_edges(ell) if strong else []
    res = []
    for size in range(1, cap + 1):
        for P in itertools.combinations(range(k), size):
            Ps = frozenset(P)
            if (Ps & O) and (Ps & I) and not any(Ps <= ed for ed in CE):
                res.append(Ps)
    return res

def p1_decide(k, ell, strong=False):
    for delta in itertools.product(range(6), repeat=ell):
        AI = allowed(k, ell, delta)
        if any(not O or not I for O, I in AI):
            continue                                  # S0 kills this delta
        opts = [p1_options(k, ell, O, I, strong) for O, I in AI]
        if any(not o for o in opts):
            continue
        word = [None] * 6
        def bt(j):
            if j == 6:
                return not (frozenset(word[5]) & frozenset(word[0]))
            for P in opts[j]:
                if j and (P & word[j - 1]):
                    continue
                word[j] = P
                if bt(j + 1):
                    return True
                word[j] = None
            return False
        for P0 in opts[0]:
            word[0] = P0
            if bt(1):
                return ("SAT", {"delta": list(delta), "word": [sorted(w) for w in word]})
        word[0] = None
    return ("UNSAT", None)

# =============================================================================
# S3  PROCEDURE 2: CNF + DPLL (decides label membership, not palettes)
# =============================================================================
def p2_cnf(k, ell, delta, strong=False):
    idx = lambda j, i: j * k + i + 1                 # DIMACS literals 1..6k
    cl = []
    for j, (O, I) in enumerate(allowed(k, ell, delta)):
        cl.append([idx(j, i) for i in range(k)])                       # nonempty
        for S in itertools.combinations(range(k), k - 2):              # |P|<=k-3
            cl.append([-idx(j, i) for i in S])
        if not O or not I:
            cl.append([])
            continue
        cl.append([idx(j, i) for i in sorted(O)])                      # S2 outer
        cl.append([idx(j, i) for i in sorted(I)])                      # S2 inner
    for j in range(6):
        for i in range(k):
            cl.append([-idx(j, i), -idx((j + 1) % 6, i)])              # S3
    if strong:
        for j in range(6):
            for a in range(ell):
                cl.append([-idx(j, a), -idx(j, (a + 1) % ell)])        # S4
    return 6 * k, cl

def p2_simplify(clauses, assign):
    out = []
    for c in clauses:
        sat = False
        rem = []
        for lit in c:
            v = abs(lit) - 1
            if v in assign:
                if assign[v] == (lit > 0):
                    sat = True
                    break
            else:
                rem.append(lit)
        if sat:
            continue
        if not rem:
            return None
        out.append(rem)
    return out

def p2_dpll(nv, clauses, order):
    def rec(assign, cls):
        while True:
            units = [c[0] for c in cls if len(c) == 1]
            if not units:
                break
            for u in units:
                v, val = abs(u) - 1, u > 0
                if v in assign and assign[v] != val:
                    return None
                assign = assign | {v: val}
                cls = p2_simplify(cls, {v: val})
                if cls is None:
                    return None
            if not cls:
                return assign
        if not cls:
            return assign
        shortest = min(cls, key=len)
        lit = min(shortest, key=lambda l: order[abs(l) - 1])
        v = abs(lit) - 1
        for val in (True, False):
            c2 = p2_simplify(cls, {v: val})
            if c2 is None:
                continue
            r = rec(assign | {v: val}, c2)
            if r is not None:
                return r
        return None
    return rec({}, clauses)

def p2_decide(k, ell, strong=False):
    for delta in itertools.product(range(6), repeat=ell):
        AI = allowed(k, ell, delta)
        if any(not O or not I for O, I in AI):
            continue
        nv, cl = p2_cnf(k, ell, delta, strong)
        m1 = p2_dpll(nv, cl, list(range(nv)))
        m2 = p2_dpll(nv, cl, list(range(nv - 1, -1, -1)))
        if (m1 is None) != (m2 is None):
            raise RuntimeError("branching-order-dependent verdict at %s" % ((k, ell, delta),))
        if m1 is not None:
            word = [sorted(i for i in range(k) if m1.get(j * k + i, False)) for j in range(6)]
            errs = check(k, ell, delta, word, strong=strong)
            if errs:
                raise RuntimeError("CNF model fails the checker: %s" % errs)
            return ("SAT", {"delta": list(delta), "word": word})
    return ("UNSAT", None)

# =============================================================================
# S4  CLOSED FORM: a satisfying word for every k >= 6 (and for (5,3),(5,4))
# =============================================================================
def closed_form(k, ell):
    """p = floor(ell/2); delta_i = 0 for i < p, 3 for i >= p; word P,Q,P,Q,P,Q."""
    p = ell // 2
    if k - ell >= 2:                       # at least two outsiders
        P, Q = [k - 2], [k - 1]
    elif k - ell == 1:                     # exactly one outsider
        P, Q = [k - 1], [1, p + 1]
    else:                                  # ell == k, no outsider
        P, Q = [1, p + 1], [2, p + 2]
    delta = [0] * p + [3] * (ell - p)
    return delta, [P if j % 2 == 0 else Q for j in range(6)]

# =============================================================================
# S5  EXACT CERTIFICATE, k = ell = 6
# =============================================================================
def certificate_k6():
    """Unit vectors at multiples of pi/3 stored as (cx, sy) meaning
    (cx, sy*sqrt3/2); dot products are then rational and every sign exact."""
    COS = [Fraction(1), Fraction(1, 2), Fraction(-1, 2), Fraction(-1), Fraction(-1, 2), Fraction(1, 2)]
    SIN = [Fraction(0), Fraction(1), Fraction(1), Fraction(0), Fraction(-1), Fraction(-1)]
    dot = lambda u, v: u[0] * v[0] + Fraction(3, 4) * u[1] * v[1]
    sgn = lambda q: (q > 0) - (q < 0)
    k, ell = 6, 6
    E = list(zip(COS, SIN))                                  # R^j e, e = 1
    V = [(Fraction(1, 2), Fraction(1))] * 3 + [(Fraction(-1, 2), Fraction(-1))] * 3
    sigma = [[sgn(dot(E[j], V[i])) for j in range(6)] for i in range(ell)]
    assert all(s != 0 for row in sigma for s in row)
    for row in sigma:                                        # three consecutive +
        plus = [j for j in range(6) if row[j] > 0]
        assert len(plus) == 3 and (plus[1] - plus[0]) % 6 == 1 and (plus[2] - plus[1]) % 6 == 1
    delta = [next(j for j in range(6) if row[j] > 0) for row in sigma]
    word = [[1, 4] if j % 2 == 0 else [2, 5] for j in range(6)]
    return sigma, delta, word, check(k, ell, delta, word, strong=True)

# =============================================================================
# S5b  GLOBAL WITNESS: one palette field on the WHOLE circle of directions
# =============================================================================
def cosign(t, phi):
    """sign of cos(pi*(t-phi)) for t, phi rational multiples of pi (mod 2)."""
    d = (t - phi) % 2
    if d == Fraction(1, 2) or d == Fraction(3, 2):
        raise ValueError("direction perpendicular to some v_i")
    return 1 if (d < Fraction(1, 2) or d > Fraction(3, 2)) else -1

def global_field(k, ell):
    """Phi(u) = P on the even arcs (r*pi/3,(r+1)*pi/3), Q on the odd arcs."""
    p = ell // 2
    if k - ell >= 2:
        P, Q = frozenset({k - 2}), frozenset({k - 1})
    elif k - ell == 1:
        P, Q = frozenset({k - 1}), frozenset({1, p + 1})
    else:
        P, Q = frozenset({1, p + 1}), frozenset({2, p + 2})
    phi = [Fraction(1, 3)] * p + [Fraction(4, 3)] * (ell - p)
    return (lambda t: P if int((3 * t) % 6) % 2 == 0 else Q), phi

def check_global(k, ell, N=31):
    """Check S0-S4 at every non-boundary direction of a mesh of 6N directions."""
    Phi, phi = global_field(k, ell)
    n_ok, fails = 0, []
    for m in range(6 * N):
        t = Fraction(m, 3 * N)
        if (3 * t) % 1 == 0:
            continue                                  # arc boundary: measure zero
        pos, neg = set(), set()
        for i in range(ell):
            ends = {i, (i + 1) % ell}
            if cosign(t, phi[i]) > 0:
                pos |= ends
            else:
                neg |= ends
        O = frozenset(set(range(k)) - pos)
        I = frozenset(set(range(k)) - neg)
        Pu, Pv = Phi(t), Phi(t + Fraction(1, 3))
        bad = []
        if not O or not I:
            bad.append("S0")
        if not 1 <= len(Pu) <= k - 3:
            bad.append("S1")
        if not Pu & O:
            bad.append("S2/O")
        if not Pu & I:
            bad.append("S2/I")
        if Pu & Pv:
            bad.append("S3")
        for a in range(ell):
            if Pu <= {a, (a + 1) % ell}:
                bad.append("S4")
        if bad:
            fails.append((str(t), bad))
        else:
            n_ok += 1
    return n_ok, n_ok + len(fails), fails

# =============================================================================
# S6  MAIN
# =============================================================================
if __name__ == "__main__":
    print("=" * 78)
    print("TABLE: STRIP(k,ell) for 4 <= k <= 7, 3 <= ell <= k")
    print("       (without and with the Lemma 6.2 constraint S4)")
    print("=" * 78)
    disagreements = []
    for strong in (False, True):
        for k in range(4, 8):
            for ell in range(3, k + 1):
                v1, c1 = p1_decide(k, ell, strong)
                v2, c2 = p2_decide(k, ell, strong)
                if v1 != v2:
                    disagreements.append((k, ell, strong, v1, v2))
                tag = "[+S4]" if strong else "     "
                print(f"  k={k} ell={ell} {tag}  procedure1={v1:5s} procedure2={v2:5s}"
                      + ("" if c1 is None else f"   witness delta={c1['delta']} word={c1['word']}"))
    print("\n  disagreements between the two procedures:",
          disagreements if disagreements else "NONE")

    print()
    print("=" * 78)
    print("CLOSED FORM: word P,Q,P,Q,P,Q with p = floor(ell/2), delta_i = 0 (i<p), 3 (i>=p)")
    print("checked with S1-S4 for 4 <= k <= 40, 3 <= ell <= k")
    print("=" * 78)
    fails, nok = [], 0
    for k in range(4, 41):
        for ell in range(3, k + 1):
            d, w = closed_form(k, ell)
            errs = check(k, ell, d, w, strong=True)
            if errs:
                fails.append((k, ell))
            else:
                nok += 1
    print("  verified:", nok, "pairs;  fails exactly at:", sorted(fails))
    for k in (6,):
        for ell in range(3, k + 1):
            d, w = closed_form(k, ell)
            print(f"    k=6 ell={ell}: delta={d} word={w}")

    print()
    print("=" * 78)
    print("EXACT CERTIFICATE k=6, ell=6 (rational coordinates, exact dot products)")
    print("=" * 78)
    sigma, delta, word, errs = certificate_k6()
    print("  x = (0,0), e = (1,0), v_0=v_1=v_2 = e^{i pi/3}, v_3=v_4=v_5 = e^{i 4 pi/3}")
    print("  sign matrix (edge i at direction R^j e):")
    for i, row in enumerate(sigma):
        print("    edge", i, "->", row)
    print("  strip sets O_j / I_j:")
    for j, (O, I) in enumerate(allowed(6, 6, delta)):
        print(f"    j={j}: O={sorted(O)} I={sorted(I)}")
    print("  palette word:", word)
    print("  checker (S0,S1,S2,S3,S4):", "ALL HOLD" if not errs else errs)

    print()
    print("=" * 78)
    print("VALIDATION: at k=5, ell=5 the same system is UNSAT, which is exactly")
    print("Proposition 8.2 of the paper (the strip layer IS the five-cycle argument).")
    print("=" * 78)
    v1, _ = p1_decide(5, 5)
    v2, _ = p2_decide(5, 5)
    print("  STRIP(5,5):", v1, "/", v2, "  (paper: no five-cycle)")
    print("  STRIP(6,6):", p1_decide(6, 6)[0], "/", p2_decide(6, 6)[0],
          "  (so Section 8 has no six-colour six-cycle exclusion)")

    print()
    print("=" * 78)
    print("GLOBAL WITNESS: a single piecewise-constant palette field on the whole")
    print("circle of directions, alternating P/Q on the arcs (r*pi/3,(r+1)*pi/3)")
    print("=" * 78)
    for k in (5, 6):
        for ell in range(3, k + 1):
            n_ok, tot, fails = check_global(k, ell)
            print(f"  k={k} ell={ell}: {n_ok}/{tot} sampled directions satisfy S0-S4"
                  + ("" if not fails else f"   failures e.g. {fails[:2]}"))
    print("  (k=5, ell=5 must fail: STRIP(5,5) is unsatisfiable, Proposition 8.2.)")

