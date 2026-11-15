"""Exact core for the licensed relaxation R on six directions.

Everything here is exact rational arithmetic; no floats anywhere.
Clauses (1)-(4) are used verbatim:
  (1) palette(t) nonempty
  (2) palette(t) meets R+(t), R-(t) = C \\ union{E_i : i in Ppos(t) / Pneg(t)}
  (3) same for R-   [the task numbers them (2)(3) jointly; we keep (1),(2),(3)=(R+),(R-)]
  (4) palette(t+60j) meets-disjoint palette(t+60(j+1)), all j incl. 5->0.
Reduction (equivalence, both directions, proved in REPORT.md):
  R is SAT at t  <=>  exists P_0..P_5, each a set of size <=2 hitting R+ and R-,
  with P_j disjoint P_{j+1} for every j (cyclic).
"""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache

C = tuple(range(6))
E = {i: frozenset({i, (i + 1) % 6}) for i in range(6)}
# base sign pattern index m=0..5 : sign cos(phi + 60 m) with phi in (0,30)
PAT = (1, 1, -1, -1, -1, 1)


def sign_cos(x):
    """Exact sign of cos(x degrees) for x a Fraction/int."""
    d = F(x) % 360
    if d == 90 or d == 270:
        return 0
    return 1 if (d < 90 or d > 270) else -1


def smat(alpha, t):
    """S[j][i] = sign cos(t+60j-alpha_i), six phases x six bonds."""
    t = F(t)
    al = [F(a) for a in alpha]
    return [[sign_cos(t + 60 * j - al[i]) for i in range(6)] for j in range(6)]


def Rsets(alpha, t):
    """[(R+(t+60j), R-(t+60j))] for j=0..5, computed from first principles."""
    out = []
    t = F(t)
    al = [F(a) for a in alpha]
    for j in range(6):
        Pp = [i for i in range(6) if sign_cos(t + 60 * j - al[i]) > 0]
        Pn = [i for i in range(6) if sign_cos(t + 60 * j - al[i]) < 0]
        Rp, Rm = set(C), set(C)
        for i in Pp:
            Rp -= E[i]
        for i in Pn:
            Rm -= E[i]
        out.append((frozenset(Rp), frozenset(Rm)))
    return out


def Rsets_from_tau(tau):
    """Same but from the finite class tau (avoids all trigonometry)."""
    out = []
    for j in range(6):
        Pp = [i for i in range(6) if PAT[(j - tau[i]) % 6] > 0]
        Pn = [i for i in range(6) if PAT[(j - tau[i]) % 6] < 0]
        Rp, Rm = set(C), set(C)
        for i in Pp:
            Rp -= E[i]
        for i in Pn:
            Rm -= E[i]
        out.append((frozenset(Rp), frozenset(Rm)))
    return out


def cands(Rp, Rm):
    """All sets of size 1 or 2 hitting both R+ and R- (the reduced witness alphabet)."""
    res = []
    for k in (1, 2):
        for S in combinations(C, k):
            S = frozenset(S)
            if (S & Rp) and (S & Rm):
                res.append(S)
    return res


def cand_table(tau):
    return [cands(Rp, Rm) for (Rp, Rm) in Rsets_from_tau(tau)]


def tau_of(alpha, t):
    """Finite class of (alpha,t): tau_i = n_i - sgn(x_i)*[|x_i|>30], x_i = s - r_i,
    s = t mod 60, alpha_i = 60 n_i + r_i, r_i in [0,60). Returns None-entry on a zero
    (i.e. some |x_i| == 30: the phase meets a breakpoint and the class is undefined)."""
    s = F(t) % 60
    out, degen = [], []
    for i in range(6):
        a = F(alpha[i]) % 360
        n = int(a // 60)
        r = a - 60 * n
        x = s - r
        if abs(x) == 30:
            degen.append(i)
        ti = n
        if x > 30:
            ti = n - 1
        elif x < -30:
            ti = n + 1
        out.append(ti % 6)
    return out, degen


def canon(tau):
    """Class representative: subtract tau_0 (global j-relabel is a CSP symmetry)."""
    return tuple((x - tau[0]) % 6 for x in tau)


# ---------------- solver A: DFS with fixed first element --------------
def solve_dp(table):
    """SAT?  returns (True, [P_0..P_5]) or (False, None).  Plain DFS, no memo."""
    n = 6
    for start in range(len(table[0])):
        acc = [table[0][start]]
        ok = True

        def rec(j, prev):
            if j == n:
                return not (acc[0] & acc[n - 1])
            for x in table[j]:
                if prev & x:
                    continue
                acc.append(x)
                if rec(j + 1, x):
                    return True
                acc.pop()
            return False

        if rec(1, acc[0]):
            return True, list(acc)
    return False, None


# ---------------- solver B: half-enumeration (independent verifier) -----------
def solve_half(table):
    """Independent decision: split the 6-cycle at two cut edges (5-0 and 2-3).
    Enumerate every compatible path of length 3 on {0,1,2} and on {3,4,5}, then join."""
    n = 6
    left = []   # (P0,P1,P2) with P0^P1 empty, P1^P2 empty
    for a in table[0]:
        for b in table[1]:
            if a & b:
                continue
            for c in table[2]:
                if b & c:
                    continue
                left.append((a, b, c))
    right = []
    for d in table[3]:
        for e in table[4]:
            if d & e:
                continue
            for f in table[5]:
                if e & f:
                    continue
                right.append((d, e, f))
    for (a, b, c) in left:
        for (d, e, f) in right:
            if (c & d) or (f & a):
                continue
            return True, [a, b, c, d, e, f]
    return False, None


def solve_chain(table):
    """Chain version of R: clauses (1)-(3) at j=0..5 and clause (4) for j=0..4 ONLY.
    The wrap edge 5->0 is dropped; every other edge is kept.  (An earlier version
    here stopped at j=5, which silently dropped the 4->5 edge as well; that variant
    is not the chain relaxation and its results are void.)"""
    n = 6
    acc = []

    def rec(j, prev):
        if j == n:
            return True                     # no check against acc[0]: wrap dropped
        for x in table[j]:
            if prev & x:
                continue
            acc.append(x)
            if rec(j + 1, x):
                return True
            acc.pop()
        return False

    for start in table[0]:
        acc[:] = [start]
        if rec(1, start):
            return True, list(acc)
    return False, None


def count_chain(table):
    """Number of chain (wrap-dropped) solutions."""
    tot = 0
    cur = [None]
    states = {None: 1}
    for j in range(6):
        nxt = {}
        for x in table[j]:
            s = 0
            for prev, c in states.items():
                if prev is None or not (prev & x):
                    s += c
            if s:
                nxt[x] = s
        states = nxt
    return sum(states.values())


def count_solutions(table):
    """Number of cyclic-disjoint selections, by DP over the 6-cycle fixing P_0."""
    n = 6
    tot = 0
    for a in table[0]:
        cur = {a: 1}
        for j in range(1, n):
            nxt = {}
            for x, c in cur.items():
                for y in table[j]:
                    if x & y:
                        continue
                    nxt[y] = nxt.get(y, 0) + c
            cur = nxt
        for x, c in cur.items():
            if not (x & a):
                tot += c
    return tot


def verify_witness(alpha, t, P):
    """Independent check of a witness against clauses (1)-(4) from first principles."""
    errs = []
    R = Rsets(alpha, t)
    for j in range(6):
        Rp, Rm = R[j]
        if not P[j]:
            errs.append(f"j={j}: empty palette (clause 1)")
        if not (set(P[j]) & Rp):
            errs.append(f"j={j}: misses R+={sorted(Rp)} (clause 2)")
        if not (set(P[j]) & Rm):
            errs.append(f"j={j}: misses R-={sorted(Rm)} (clause 3)")
    for j in range(6):
        inter = set(P[j]) & set(P[(j + 1) % 6])
        if inter:
            errs.append(f"j={j}->{(j+1)%6}: palettes meet at {sorted(inter)} (clause 4)")
    return (len(errs) == 0), errs


def full_palette_alphabet(Rlist):
    """Every set of ANY size hitting both R+ and R- (the unreduced alphabet)."""
    out = []
    for (Rp, Rm) in Rlist:
        s = []
        for mask in range(64):
            S = frozenset(i for i in range(6) if mask >> i & 1)
            if S and (S & Rp) and (S & Rm):
                s.append(S)
        out.append(s)
    return out


def solve_full_palette(Rlist):
    """Decision for R with NO reduction: palettes of any size.
    Exact, independent of tau and of the 2-witness reduction. Bitmask DP."""
    n = 6
    pal = full_palette_alphabet(Rlist)
    adj = []
    for j in range(n):
        row = []
        for x in pal[j]:
            m = 0
            for k, y in enumerate(pal[(j + 1) % n]):
                if not (x & y):
                    m |= 1 << k
            row.append(m)
        adj.append(row)
    for s in range(len(pal[0])):
        reach = 1 << s                      # bitmask over pal[0]
        for step in range(1, n):            # reach -> palettes of phase `step`
            new = 0
            r = reach
            k = 0
            while r:
                if r & 1:
                    new |= adj[step - 1][k]
                r >>= 1
                k += 1
            reach = new
            if not reach:
                break
        r = reach
        k = 0
        while r:
            if r & 1 and (adj[n - 1][k] >> s) & 1:
                return True
            r >>= 1
            k += 1
    return False
