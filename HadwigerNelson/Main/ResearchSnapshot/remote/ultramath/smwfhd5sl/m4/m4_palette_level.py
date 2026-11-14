"""Is the palette level of Section 8 satisfiable?  Table over k = 3..6 and 3 <= l <= k.

The palette level is the list
  (P) 1 <= |P_j| <= k-3
  (S) P_j meets O(R^j e) and I(R^j e)
  (R) P_j cap P_{j+1} = empty
  (B) P_j = P_{j+3} whenever both avoid the labels outside the cycle      [state determinism]
  (Z) six positions
  (A) (only for l = k = 5, where the palette is forced to be a pair) both P_j, P_{j+3}
      lie in the option set Opt(R^j e), which is Opt(-e) = Opt(e)

For UNSAT it is enough to refute the relaxation in which the six sign patterns are free
subject to s_{j+3} = -s_j (every geometric datum satisfies that).  For SAT an explicit
model is printed.
"""
import itertools

SECT = "=" * 78


def show(P):
    return "{" + ",".join(str(i) for i in sorted(P)) + "}"


def allowed(s, cyc, k):
    L = len(cyc)
    outside = set(range(k)) - set(cyc)
    O, I = set(), set()
    for j in range(L):
        if s[(j - 1) % L] < 0 and s[j] < 0:
            O.add(cyc[j])
        if s[(j - 1) % L] > 0 and s[j] > 0:
            I.add(cyc[j])
    return O | outside, I | outside


def options(s, cyc, k):
    O, I = allowed(s, cyc, k)
    if not O or not I:
        return O, I, []
    out = []
    for r in range(1, k - 2):
        for P in itertools.combinations(sorted(O | I), r):
            P = frozenset(P)
            if P & O and P & I:
                out.append(P)
    return O, I, out


def solve(k, L, impose_A=False):
    """return one model (sign patterns + palettes) or None"""
    cyc = tuple(range(L))
    outside = frozenset(range(L, k))
    sg = [tuple(s) for s in itertools.product((-1, 1), repeat=L)]
    opt = {s: options(s, cyc, k) for s in sg}
    ok_s = [s for s in sg if opt[s][2]]
    # 3 free sign patterns, the last three are the negations
    for s0 in ok_s:
        for s1 in ok_s:
            for s2 in ok_s:
                S = [s0, s1, s2, tuple(-x for x in s0), tuple(-x for x in s1), tuple(-x for x in s2)]
                cand = []
                if impose_A:
                    for j in range(6):
                        cand.append(opt[S[j]][2])
                else:
                    for j in range(6):
                        O, I = allowed(S[j], cyc, k)
                        lst = [P for P in opt[S[j]][2]
                               if not (not (P & outside) and P and False)]
                        cand.append(lst)
                # backtracking
                res = []

                def rec(j):
                    if j == 6:
                        # (B): P_j = P_{j+3} when both avoid `outside`.  Vacuous when
                        # there are no outsiders at all (l = k), NOT "P_j = P_{j+3}".
                        if outside:
                            for a in range(3):
                                Pa, Pb = res[a], res[a + 3]
                                if not (Pa & outside) and not (Pb & outside) and Pa != Pb:
                                    return False
                        return not (res[0] & res[5])
                    for P in cand[j]:
                        if j and (P & res[-1]):
                            continue
                        res.append(P)
                        if rec(j + 1):
                            return True
                        res.pop()
                    return False

                if rec(0):
                    return S, list(res), cyc
    return None


print(SECT)
print("palette level of Section 8: satisfiable?   (UNSAT by relaxation, SAT by model)")
print(SECT)
print("\n k  l   (P),(S),(R),(B),(Z)              + (A) at l=k=5")
for k in range(3, 7):
    for L in range(3, k + 1):
        r = solve(k, L)
        rA = solve(k, L, impose_A=True) if (L == k == 5) else None
        tag = "SAT" if r else "UNSAT"
        tagA = "" if rA is None else ("SAT" if rA else "UNSAT")
        print(f" {k}  {L}   {tag:5s}                          {tagA}")
        if r:
            S, P, cyc = r
            print("        model:  s =", ["".join('+' if x > 0 else '-' for x in s) for s in S])
            print("                P =", [show(x) for x in P])

print("""
Read-off.
 * k = 3: (P) is 1 <= |P| <= 0, unsatisfiable outright.
 * k = 4: the palette level is unsatisfiable at both lengths -- with |P| = 1 the
   outsider (there is exactly one for l = 3) has to serve every position, and (R) kills it.
 * k = 5, l = 5: unsatisfiable at the palette level, and the paper's Prop 8.2 is exactly
   this (Section 3.1 of CORE.md).
 * k = 5, l = 4 and l = 3: SATISFIABLE at the palette level.  So Propositions 8.5 and 8.10
   need their geometric layers (the four-ray diagonal geometry; the sector structure and
   the polynomial three-label region).  Those layers are k-blind, but the state spaces they
   act on are not: at k = 6 they are the six-state systems of W6.
 * k = 6: satisfiable at every length.  This is the sharpness statement of CORE.md Sec. 4.
""")

# ---------------------------------------------------------------- refinement
print(SECT)
print("k = 5, l = 4: which state words survive the palette level?")
print(SECT)


def state_of(P, k):
    outside = set(range(4, k))
    if P & outside:
        return 'X'
    return 'U' if P == frozenset({0, 2}) else ('V' if P == frozenset({1, 3}) else '?')


cyc, k = (0, 1, 2, 3), 5
outside = frozenset({4})
sg = [tuple(s) for s in itertools.product((-1, 1), repeat=4)]
opt = {s: options(s, cyc, k) for s in sg}
ok_s = [s for s in sg if opt[s][2]]
seen = {}
count = 0
for s0 in ok_s:
    for s1 in ok_s:
        for s2 in ok_s:
            S = [s0, s1, s2, tuple(-x for x in s0), tuple(-x for x in s1), tuple(-x for x in s2)]
            cand = [opt[S[j]][2] for j in range(6)]
            res = []

            def rec(j):
                global count
                if j == 6:
                    for a in range(3):
                        Pa, Pb = res[a], res[a + 3]
                        if not (Pa & outside) and not (Pb & outside) and Pa != Pb:
                            return
                    if res[0] & res[5]:
                        return
                    w = ''.join(state_of(P, k) for P in res)
                    seen[w] = seen.get(w, 0) + 1
                    count += 1
                    return
                for P in cand[j]:
                    if j and (P & res[-1]):
                        continue
                    res.append(P)
                    rec(j + 1)
                    res.pop()

            rec(0)
print(f"\n  palette-level solutions at k = 5, l = 4: {count}")
print("  distribution of state words p_0..p_5 (X = outsider 4 present, U = {0,2}, V = {1,3}):")
for w in sorted(seen):
    per = all(w[j] == w[(j + 3) % 6] for j in range(3))
    print(f"    {w}   {seen[w]:5d} palette data   three-periodic: {per}")
print(f"""
  {count} palette-level solutions, {len(seen)} distinct state words.  All of them satisfy
  (8.2a)+(8.2b), so they are among the 34 words of m4_s8_core.py 2.1: the 6 three-periodic
  permutations and the 28 words with a well-defined parity h.  So the palette level of
  Proposition 8.5 is satisfiable and excludes nothing on its own at k = 5.  The exclusion is
  two-staged and both stages are needed: Lemma 8.3's cross-word restriction removes the six
  three-periodic words, and the cross-word plus complementary-arc count removes the 28
  parity words.  (A single word may mix U and V on its non-X parity; the "all three selected
  entries agree" step of 8.5 is a statement about a *pair* of nearby words.)""")
