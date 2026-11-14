#!/usr/bin/env python3
"""
d2: exact measurable palette field, take 2 -- with ALL the single-centre palette constraints
the paper actually supplies.  Constraints, and where each comes from:

  (8.1)     P(e) meets I(e) and O(e) a.e.                    Lemma 8.1
  (5.7)     P(e) cap P(Re) = empty a.e.                      Corollary 5.4
  (PAL)     |P(e)| <= 3 a.e.                                 Proposition 5.6's method at k=6
  (6.2)     P(e) not contained in any edge {i,j} of Gamma_x   Lemma 6.2
  (SUM)     P(e) cap P(v) = empty and e not parallel v  =>  |P(e)|+|P(v)| <= k-1   [(5.2) +
            the fact that x+e+v must carry a colour; note h = e+v has exactly one unordered
            representation, so this is the complete palette-only content of (5.2) at one centre]
  (M11)     sigma{T subset P} <= 1/2 for every nonempty T     m11 Theorem 3
  (L64)     not a two-valued state function {X} / fixed pair D   Lemma 6.4
  (L63)     strict state separation                          Lemma 6.3
  (abs)     P avoids a chosen label a.e.                     self-avoidance, Lemma D

A field with |P| <= 2 everywhere makes (SUM) automatic (2+2 = 4 <= 5) and makes (L63) vacuous
(no state can represent a group of 3 labels).  This script therefore searches that stratum
first, and then the general one, with (SUM) checked globally.
"""
import itertools, sys
from fractions import Fraction as F

ELL = 5

def internal(Q, sign):
    return frozenset(i for i in range(ELL)
                     if (((i - 1) % ELL) in Q) == bool(sign) and (i in Q) == bool(sign))

def allowed(Q, k=6):
    outs = frozenset(range(ELL, k))
    return internal(Q, True) | outs, internal(Q, False) | outs

def cos_pos(t, b):
    d = (F(t) - F(b)) % 360
    return d < 90 or d > 270

def pattern(t, betas):
    return frozenset(j for j in range(len(betas)) if cos_pos(t, betas[j]))

def options(Q, k=6, bmax=3, absence=frozenset(), use62=True):
    I, O = allowed(Q, k)
    out = []
    for c in range(1, bmax + 1):
        for cand in itertools.combinations(range(k), c):
            P = frozenset(cand)
            if not (P & I and P & O): continue
            if P & absence: continue
            if use62 and any(P <= frozenset({j, (j + 1) % ELL}) for j in range(ELL)): continue
            out.append(P)
    return out

def build(betas, k=6, absence=frozenset(), bmax=3, forbid_sets=(), target_vals=3):
    """forbid_sets: palette values that may not be used anywhere (to force variety)."""
    pats = [pattern(F(j) + F(1, 2), betas) for j in range(360)]
    opts = [options(p, k, bmax, absence) for p in pats]
    opts = [[P for P in o if not any(P <= F_ for F_ in forbid_sets)] for o in opts]
    if any(not o for o in opts):
        return None, pats
    field = [None] * 360
    for r in range(60):
        orb = [r + 60 * t for t in range(6)]
        sol = []; ok = [False]
        def dfs(i):
            if ok[0]: return
            if i == 6:
                ok[0] = True
                for t in range(6): field[orb[t]] = sol[t]
                return
            cands = sorted(opts[orb[i]], key=lambda P: (-len(P), sorted(P)))
            for P in cands:
                if sol and (P & sol[-1]): continue
                if i == 5 and (P & sol[0]): continue
                # (SUM) against every cell already fixed
                bad = False
                for j in range(360):
                    if field[j] is None: continue
                    if not (P & field[j]) and len(P) + len(field[j]) >= k:
                        bad = True; break
                if bad: continue
                sol.append(P); dfs(i + 1); sol.pop()
        dfs(0)
        if not ok[0]:
            return None, pats
    return field, pats

def verify(field, pats, k=6, absence=frozenset()):
    assert field is not None
    for j in range(360):
        I, O = allowed(pats[j], k); P = field[j]
        assert P & I and P & O, ("8.1", j)
        assert 1 <= len(P) <= 3, ("PAL", j)
        assert not (P & absence), ("abs", j)
        assert not any(P <= frozenset({x, (x + 1) % ELL}) for x in range(ELL)), ("6.2", j)
        assert not (P & field[(j + 60) % 360]), ("5.7", j)
    for i in range(360):
        for j in range(360):
            if not (field[i] & field[j]) and len(field[i]) + len(field[j]) >= k:
                raise AssertionError(("SUM", i, j, sorted(field[i]), sorted(field[j])))
    for t in range(1, 4):
        for T in itertools.combinations(range(k), t):
            T = frozenset(T)
            meas = sum(1 for j in range(360) if T <= field[j])
            assert meas * 2 <= 360, ("M11", sorted(T), meas)
    return True

def run(betas, name, absence=frozenset(), bmax=3):
    field, pats = build(betas, absence=absence, bmax=bmax)
    print(f"\n=== {name};  absent {sorted(absence)};  |P| <= {bmax}")
    if field is None:
        print("    no cell-constant field in this stratum")
        return None
    verify(field, pats, absence=absence)
    vals = sorted({P for P in field}, key=lambda P: (len(P), sorted(P)))
    nX = sum(1 for j in range(360) if 5 in field[j])
    print(f"    SAT.  {len(vals)} distinct values {[sorted(v) for v in vals]}")
    print(f"    (8.1),(5.7),(PAL),(6.2),(SUM),(M11) verified on all 360 cells;"
          f" max |P| = {max(len(v) for v in vals)}")
    print(f"    sigma{{X in P}} = {nX}/360 = {float(F(nX,360)):.4f}")
    print(f"    two-valued (Lemma 6.4): {'YES -- killed' if len(vals) <= 2 else 'no'}")
    print(f"    a state with a group of size >=3 (needed for Lemma 6.3): "
          f"{'yes' if max(len(v) for v in vals) >= 3 else 'no -- Lemma 6.3 vacuous'}")
    print(f"    field: " + "".join("ABCDEFGHIJ"[vals.index(field[j])] for j in range(0, 360, 6)))
    return field

if __name__ == "__main__":
    pent = [F(18 + 72 * j) for j in range(5)]
    run(pent, "pentagon lattice, nothing absent", frozenset(), bmax=2)
    run(pent, "pentagon lattice, cycle label 0 absent", frozenset({0}), bmax=2)
    run(pent, "pentagon lattice, outsider 5 absent", frozenset({5}), bmax=2)
    run(pent, "pentagon lattice, nothing absent, |P|<=3", frozenset(), bmax=3)
    run(pent, "pentagon lattice, cycle label 0 absent, |P|<=3", frozenset({0}), bmax=3)
    run(pent, "pentagon lattice, outsider 5 absent, |P|<=3", frozenset({5}), bmax=3)
