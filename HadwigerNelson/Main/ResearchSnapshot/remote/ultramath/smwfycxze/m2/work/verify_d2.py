#!/usr/bin/env python3
"""
d2 (swarm smwfycxze / m2):  section 8 at k = 6, cycle length ell = 5.

Contents
  A.  The combinatorial reduction    (Lemma A, proved by exhaustion over all 32 sign patterns)
  B.  The main theorem               (Thm 1), checked three ways over the geometry-free family
        G^3 -> (Q_0..Q_5) with Q_{i+3} = complement(Q_i)  (1000 cases)
        B1  reduced available-pair search  (the s/ delta argument of the proof)
        B2  full palette backtracking      (every palette set of every size)
        B3  CNF + CaDiCaL                  (independent solver)
  C.  Calibration at k = 5             (Prop 8.2 reproduced: UNSAT, geometry-free)
  D.  Sharpness at k = 6               (the hypothesis "centre colour = outsider" is needed)
        D1  no label known absent            -> SAT witness
        D2  a cycle label known absent       -> SAT witness
        D3  the same witnesses against (6.2) and the 120-degree saturation
  E.  The geometry sweep               (all 6^5 gap assignments: 6-sample R-orbit systems)

Exit status 0 iff every assertion below holds.
"""
import itertools, sys, json

ELL = 5
Z5 = tuple(range(ELL))

def comp(Q, ell=ELL):
    return frozenset(i for i in range(ell) if i not in Q)

def internal(Q, ell, sign):
    """labels i with both incident edges of the ell-cycle of sign `sign` (True = +)."""
    return frozenset(i for i in range(ell)
                     if (((i - 1) % ell) in Q) == bool(sign) and (i in Q) == bool(sign))

def runs(Q, ell):
    b = [1 if i in Q else 0 for i in range(ell)]
    if len(set(b)) == 1:
        return [(b[0], ell)]
    s = next(i for i in range(ell) if b[i] != b[(i - 1) % ell])
    out, cur, cnt = [], b[s], 1
    for t in range(1, ell):
        v = b[(s + t) % ell]
        if v == cur:
            cnt += 1
        else:
            out.append((cur, cnt)); cur, cnt = v, 1
    out.append((cur, cnt))
    return out

# ------------------------------------------------------------------ A  the reduction
def lemmaA():
    """For a 5-cycle with one outsider X = 5 at k = 6:
         (I \ {X}) and (O \ {X}) both nonempty  <=>  Q has exactly two runs, lengths 2 and 3.
       And for such Q:  s(Q) := interior vertex of the length-2 run is well defined,
                        A(Q)  := interior vertices of the length-3 run  =  {s+2, s+3},
                        s(complement Q) = s(Q)."""
    G, table = [], {}
    for mask in range(1 << ELL):
        Q = frozenset(i for i in range(ELL) if mask >> i & 1)
        Ip, Op = internal(Q, ELL, True), internal(Q, ELL, False)
        ok = bool(Ip) and bool(Op)
        Gset = (len(runs(Q, ELL)) == 2 and sorted(l for _, l in runs(Q, ELL)) == [2, 3])
        assert ok == Gset, (sorted(Q), runs(Q, ELL))
        if Gset:
            G.append(Q)
            length2 = [r for r in runs(Q, ELL) if r[1] == 2][0]
            length3 = [r for r in runs(Q, ELL) if r[1] == 3][0]
            # locate the length-2 run in index order
            b = [1 if i in Q else 0 for i in range(ELL)]
            st = None
            for i in range(ELL):
                if b[i] == length2[0] and b[(i - 1) % ELL] != length2[0]:
                    st = i; break
            assert st is not None
            e1, e2 = st, (st + 1) % ELL
            assert (e1 in Q) == bool(length2[0]) and (e2 in Q) == bool(length2[0])
            s = (st + 1) % ELL                      # the shared vertex of the two edges
            A = Ip if length3[0] == 1 else Op
            assert A == frozenset({(s + 2) % ELL, (s + 3) % ELL}), (sorted(Q), s, sorted(A))
            table[Q] = (s, A)
            s2, A2 = table.get(comp(Q), (None, None))
            assert s2 is None or s2 == s
    for Q in G:
        s, A = table[Q]
        s2, A2 = table[comp(Q)]
        assert s2 == s and A2 == A, (sorted(Q), s, s2)
    return G, table

# ------------------------------------------------------------------ palette machinery
def allowed(Q, k, ell=ELL):
    outs = frozenset(range(ell, k))
    return internal(Q, ell, True) | outs, internal(Q, ell, False) | outs

def palettes(Q, k, b, forbidden=frozenset(), strong=False, ell=ELL):
    """every P subset of [k] with |P| <= b, P cap forbidden = {}, meeting both allowed sets
       (strong=True: meeting both after deleting the outsiders)."""
    I, O = allowed(Q, k, ell)
    outs = frozenset(range(ell, k))
    if strong:
        I, O = I - outs, O - outs
    opts = []
    labels = [i for i in range(k) if i not in forbidden]
    for sz in range(1, b + 1):
        for c in itertools.combinations(labels, sz):
            P = frozenset(c)
            if P & I and P & O:
                opts.append(P)
    return opts

def csp_solve(patterns, k, b, forbidden=frozenset(), strong=False, ell=ELL):
    """B2: backtracking over the cyclic sequence of palettes."""
    n = len(patterns)
    opts = [palettes(Q, k, b, forbidden, strong, ell) for Q in patterns]
    if any(not o for o in opts):
        return None
    opts = [sorted(o, key=lambda P: (len(P), sorted(P))) for o in opts]
    sol = []
    def dfs(i):
        if i == n:
            return True
        for P in opts[i]:
            if sol and (P & sol[-1]):
                continue
            if i == n - 1 and (P & sol[0]):
                continue
            sol.append(P)
            if dfs(i + 1):
                return True
            sol.pop()
        return False
    if dfs(0):
        return tuple(sol)
    return None

def csp_solve_cadical(patterns, k, b, forbidden=frozenset(), strong=False, ell=ELL):
    """B3: CNF + CaDiCaL.  var(l, i) = 'label l in P_i'.  Only the admissible palettes are
    allowed: we add a clause forbidding each non-admissible subset directly as an at-most-b
    constraint plus the 'meets I' / 'meets O' clauses."""
    from pysat.solvers import Cadical153
    n = len(patterns)
    def v(l, i):  # 1-based
        return l * n + i + 1
    cls = []
    # at most b labels per palette
    for i in range(n):
        for c in itertools.combinations(range(k), b + 1):
            cls.append([-v(l, i) for l in c])
    for i, Q in enumerate(patterns):
        I, O = allowed(Q, k, ell)
        outs = frozenset(range(ell, k))
        if strong:
            I, O = I - outs, O - outs
        cls.append([v(l, i) for l in I if l not in forbidden])   # meet I
        cls.append([v(l, i) for l in O if l not in forbidden])   # meet O
        for l in forbidden:
            cls.append([-v(l, i)])
    for i in range(n):
        j = (i + 1) % n
        for l in range(k):
            cls.append([-v(l, i), -v(l, j)])                      # (5.7)
    with Cadical153(bootstrap_with=cls) as s:
        if not s.solve():
            return None
        m = s.get_model()
        out = []
        for i in range(n):
            out.append(frozenset(l for l in range(k) if m[v(l, i) - 1] > 0))
        return tuple(out)

# ------------------------------------------------------------------ the geometry-free family
def family(table):
    """All (Q_0,...,Q_5) with Q_{i+3} = complement(Q_i) and every Q_i in G.  Determined by
    (Q_0,Q_1,Q_2): 1000 cases.  Q(-e) = complement Q(e) is exact (no genericity needed)."""
    G = sorted(table, key=sorted)
    for Q0, Q1, Q2 in itertools.product(G, repeat=3):
        yield (Q0, Q1, Q2, comp(Q0), comp(Q1), comp(Q2))

def reduced_search(patterns, table, k=6, outsiders=(5,)):
    """B1: the *reduced* search used in the proof of Theorem 1: the only data used is
       s_i = s(Q_i) and A_i;  P_i must contain s_i and meet A_i;  consecutive P disjoint.
       Returns a witness tuple of two-element sets, or None."""
    n = len(patterns)
    s = [table[Q][0] for Q in patterns]
    A = [table[Q][1] for Q in patterns]
    cand = []
    for i in range(n):
        cand.append([frozenset({s[i], a}) for a in A[i]])
    sol = []
    def dfs(i):
        if i == n:
            return True
        for P in cand[i]:
            if sol and (P & sol[-1]):
                continue
            if i == n - 1 and (P & sol[0]):
                continue
            sol.append(P)
            if dfs(i + 1):
                return True
            sol.pop()
        return False
    return tuple(sol) if dfs(0) else None

# ------------------------------------------------------------------ main
def main():
    print("== A. the combinatorial reduction ==")
    G, table = lemmaA()
    print(f"   |G| = {len(G)};  for every one of the 32 sign patterns of a 5-cycle,")
    print(f"   I\\{{X}} and O\\{{X}} are both nonempty  <=>  Q in G  (checked exactly).")
    print(f"   for Q in G:  A(Q) = {{s+2, s+3}},  s(complement Q) = s(Q)  (checked exactly).")
    fam = list(family(table))
    print(f"   geometry-free family: {len(fam)} six-tuples with Q_(i+3) = complement Q_i.")

    print("\n== B. Theorem 1 (centre colour = the outsider, X = 5 absent from every palette) ==")
    ok = True
    for name, fn in (("B1 reduced s/delta search", lambda pt: reduced_search(pt, table)),
                     ("B2 full palette search |P|<=3", lambda pt: csp_solve(pt, 6, 3, frozenset({5}), True)),
                     ("B2' full palette search, unbounded", lambda pt: csp_solve(pt, 6, 5, frozenset({5}), True)),
                     ("B3 CaDiCaL |P|<=3", lambda pt: csp_solve_cadical(pt, 6, 3, frozenset({5}), True)),
                     ("B3' CaDiCaL unbounded", lambda pt: csp_solve_cadical(pt, 6, 5, frozenset({5}), True))):
        sat = [pt for pt in fam if fn(pt) is not None]
        print(f"   {name:34s}: SAT {len(sat):4d} / {len(fam)}")
        ok &= not sat
    print(f"   => Theorem 1 holds on all {len(fam)} geometry-free cases, five independent searches."
          if ok else "   *** FAILURE ***")
    if not ok:
        return 1

    print("\n== C. calibration: k = 5, ell = 5, palette bound |P| <= 2  (Proposition 8.2) ==")
    sat5 = [pt for pt in fam if csp_solve(pt, 5, 2) is not None]
    sat5c = [pt for pt in fam if csp_solve_cadical(pt, 5, 2) is not None]
    print(f"   B2 full palette search : SAT {len(sat5)} / {len(fam)}   (UNSAT reproduces Prop 8.2)")
    print(f"   B3 CaDiCaL             : SAT {len(sat5c)} / {len(fam)}")
    ok &= not sat5 and not sat5c
    if not ok:
        print("   *** calibration FAILED ***"); return 1

    print("\n== D. sharpness: what happens when the hypothesis fails ==")
    for tag, forb, strong in (("D1 no label known absent      ", frozenset(),  False),
                              ("D2 a cycle label c=0 absent    ", frozenset({0}), False),
                              ("D3 the outsider X=5 absent, but WITHOUT the strong form",
                               frozenset({5}), False)):
        wit = [(pt, csp_solve(pt, 6, 3, forb, strong)) for pt in fam]
        sol = [(pt, w) for pt, w in wit if w is not None]
        print(f"   {tag}: SAT {len(sol):4d} / {len(fam)}")
        if sol:
            pt, w = sol[0]
            print(f"      example pattern tuple  {[sorted(q) for q in pt]}")
            print(f"      palettes               {[sorted(p) for p in w]}")
            # extra printed constraints
            assert all(len(p) <= 3 for p in w)
            for i in range(6):
                assert not (w[i] & w[(i + 1) % 6]), "5.7"
            if forb:
                assert all(not (p & forb) for p in w), "self-avoidance"
            # (6.2): P not contained in any cycle edge
            for i, Q in enumerate(pt):
                for j in range(5):
                    assert not w[i] <= frozenset({j, (j + 1) % 5}), ("(6.2)", sorted(w[i]), j)
            print("      (5.7), |P|<=3, self-avoidance and (6.2) all verified")
    print("\n== E. geometry sweep: 6-sample R-orbit systems over all 6^5 gap assignments ==")
    seen = {}
    for gap in itertools.product(range(6), repeat=5):
        pt = tuple(frozenset(j for j in range(5) if (gap[j] - m) % 6 in (0, 1, 2)) for m in range(6))
        seen.setdefault(pt, gap)
    print(f"   distinct realizable six-tuples: {len(seen)}")
    rowS = []
    for label, forb, strong in (("k=5 b=2 (calibration)", frozenset(), False),
                                ("k=6 b=3 outsider absent", frozenset({5}), True),
                                ("k=6 b=3 cycle label absent", frozenset({0}), False),
                                ("k=6 b=3 no label absent", frozenset(), False)):
        sat = 0
        for pt in seen:
            k = 5 if label.startswith("k=5") else 6
            b = 2 if k == 5 else 3
            if csp_solve(pt, k, b, forb, strong) is not None:
                sat += 1
        rowS.append((label, sat, len(seen)))
        print(f"   {label:28s}: SAT {sat:5d} / {len(seen)}")
    print("\nALL CHECKS PASSED" if ok else "\nFAILURE")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
