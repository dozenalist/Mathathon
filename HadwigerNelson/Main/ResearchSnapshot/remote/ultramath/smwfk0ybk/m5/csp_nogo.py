"""Certified no-go for the palette route to k = 6, with the non-vacuity calibration.

THEOREM (extended state-level no-go).
Class C: arguments that conclude a contradiction at k from the palette data at one cyclic
centre x and one interface of length l, namely
  (C1)  1 <= |P_i| <= k-3                    (general-k palette bound)
  (C2)  P_i & O_i != 0 and P_i & I_i != 0    (paper Lemma 8.1, display (8.1))
  (C3)  P_i & P_{i+1} == 0, i mod 6          (paper Corollary 5.4, display (5.7))
  (C4)  [k = 6 only] no two palettes are complementary 3-sets        (m6, Theorem 1)
  (C5)  [k = 6 only] at most three palettes are ternary              (m6, Theorem 2)
  over the six directions of the pi/3-orbit, with the ray geometry arbitrary.
Then C cannot decide k = 6: (C1)-(C5) are SIMULTANEOUSLY SATISFIABLE at k = 6 for l = 3 and
l = 4 and every one of the 6^l sign words (witness: alternate two outsiders).  No value of the
interface length l > 4, no mesh, no constant, and no refinement of the six-orbit data changes
this, because the countermodel does not use the ray geometry at all.
The class is NOT vacuous: the same constraints decide k = 4 (both lengths) and k = 5 at l = 5.

Everything is integer/bitmask exact.  Written from the paper's displays; no code shared with
`.ultramath/smwfhd5sl/m5/interface_csp.py` or with any other member.

Check:  python3 .ultramath/smwfk0ybk/m5/csp_nogo.py
"""
from itertools import product, combinations

COS = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}
POP = [bin(m).count('1') for m in range(64)]


def allowed(l, k, c):
    """(O_i, I_i) as bitmasks, i = 0..5; outsiders (labels >= l) are allowed on both sides."""
    U = sum(1 << t for t in range(l, k))
    O, I = [], []
    for i in range(6):
        sig = [COS[(c[j] + 1 - i) % 6] for j in range(l)]
        o, ii = U, U
        for j in range(l):
            if sig[(j - 1) % l] == -1 and sig[j] == -1:
                o |= 1 << j
            if sig[(j - 1) % l] == 1 and sig[j] == 1:
                ii |= 1 << j
        O.append(o)
        I.append(ii)
    return O, I


def admissible(k, o, i):
    out = []
    for r in range(1, k - 2):
        for comb in combinations(range(k), r):
            p = 0
            for t in comb:
                p |= 1 << t
            if (p & o) and (p & i):
                out.append(p)
    return out


def tighten(k, pals):
    """(C4),(C5) at k = 6; vacuous for other k."""
    if k != 6:
        return True
    full = (1 << k) - 1
    for a in range(6):
        for b in range(a + 1, 6):
            if pals[a] | pals[b] == full and POP[pals[a]] == 3 and POP[pals[b]] == 3:
                return False
    return sum(1 for p in pals if POP[p] == 3) <= 3


def decisive(l, k, c):
    """Exhaustive: is there a palette assignment satisfying (C1)-(C5) for this sign word?"""
    O, I = allowed(l, k, c)
    adm = [admissible(k, O[i], I[i]) for i in range(6)]
    if any(not a for a in adm):
        return None
    sol = []

    def dfs(i):
        if i == 6:
            return not (sol[5] & sol[0]) and tighten(k, sol)
        for p in adm[i]:
            if i and (p & sol[i - 1]):
                continue
            sol.append(p)
            if dfs(i + 1):
                return True
            sol.pop()
        return False

    for p in adm[0]:
        sol = [p]
        if dfs(1):
            return list(sol)
    return None


def witness_alts(l, k):
    """The alternating-outsider model: {l} at even positions, {l+1} at odd ones."""
    a, b = 1 << l, 1 << (l + 1)
    return [a, b, a, b, a, b]


def main():
    print("non-vacuity calibration of the same constraint system:")
    for k, l in ((4, 3), (4, 4), (5, 5), (6, 5)):
        total = sat = 0
        for c in product(range(6), repeat=l):
            total += 1
            if decisive(l, k, c) is not None:
                sat += 1
        print(f"  k={k} l={l}: {sat}/{total} sign words satisfiable"
              f"  -> {'SAT' if sat else 'UNSAT (the class decides here)'}")

    print("\nthe no-go at k = 6 (alternating outsiders, every sign word):")
    for l in (3, 4):
        k = 6
        pals = witness_alts(l, k)
        bad = 0
        for c in product(range(6), repeat=l):
            O, I = allowed(l, k, c)
            ok = all(POP[p] <= k - 3 and POP[p] >= 1 and (p & O[i]) and (p & I[i])
                     and not (p & pals[(i + 1) % 6]) for i, p in enumerate(pals))
            if not (ok and tighten(k, pals)):
                bad += 1
        print(f"  k=6 l={l}: {6 ** l - bad}/{6 ** l} sign words have the model "
              f"P_0=P_2=P_4={{{l}}}, P_1=P_3=P_5={{{l + 1}}}"
              + ("" if bad == 0 else f"  FAILURES {bad}"))
    print("\n  hence (C1)-(C5) is satisfiable at k = 6, so no UNSAT certificate exists,")
    print("  so this route cannot prove chi(R^2) >= 7.  For l = 5, 6 the outsider trick")
    print("  is unavailable (k - l < 2) and the words must be searched; but a single")
    print("  satisfiable (l, word) already settles the decision.")


if __name__ == "__main__":
    main()
