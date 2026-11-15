"""BOUNDED-MEMORY ALL-PHASE CENSUS  (member m2, swarm smwgui92e, direction d2)

Object.  A staircase is (initial class tau, ordered partition of the six interface indices)
= (tau, chain of subsets 0 = A_0 < A_1 < ... < A_k = [6]); the class at step j is
[tau - 1_{A_j}].  The staircase survives iff every class on it is SAT in the parent's
fixed-phase table (177 SAT / 7599 UNSAT of 7776 classes).

KEY REDUCTION (this file).  The class sequence depends on the ordered partition ONLY through
its chain of partial unions, so the census is a DP on the 64-element Boolean lattice B_6 per
class, i.e. 7776 x 64 states, NOT 7776 x 4683 staircases.  Memory: one 7776 x 64 boolean
table + one 7776 x 64 integer DP array (+ 7776 x 64 x 7 for the per-block-count split).

Usage:
  python3 census.py --smoke 300     recompute SAT on 300 classes, census restricted to them
  python3 census.py --full          recompute the whole 7776-class table, full census
  python3 census.py --table T.txt --full   use the parent's table file (one SAT class per
                                    line, six integers 0..5, e.g. "0 0 1 2 3 4"), full census
"""
import sys, time, json, math
from itertools import product

PAT = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}      # (+,+,-,-,-,+)
FULL = (1 << 6) - 1

def canon(t):
    b = t[0]
    return tuple((x - b) % 6 for x in t)

# ---------- the six column types (a column = sign vector of the six cosines at one phase) ----------
def column(tau, j):
    return tuple(PAT[(j - tau[i]) % 6] for i in range(6))

def sides(col):
    """R+ = uncovered vertices of the positive edge set; R- likewise (verified in verify1.py)"""
    Rp = {v for v in range(6) if col[(v-1) % 6] <= 0 and col[v] <= 0}
    Rn = {v for v in range(6) if col[(v-1) % 6] >= 0 and col[v] >= 0}
    return tuple(sorted(Rp)), tuple(sorted(Rn))

def allowed(col):
    """minimal palettes that HIT R+ and R-: all {x,y}, x in R+, y in R-  (lemma: minimal hitting
    sets suffice, so this is equivalent to the unrestricted 64-palette rule)"""
    Rp, Rn = sides(col)
    return tuple(sorted({(1 << x) | (1 << y) for x in Rp for y in Rn}))

CTYPES = [c for c in product((1, -1), repeat=6)]                    # 64 sign vectors
ALLOWED = {c: allowed(c) for c in CTYPES}
DISJ = [[q for q in range(64) if not (p & q)] for p in range(64)]    # palette masks 0..63

def sat(tau):
    """parent's fixed-phase CSP: a cyclic sequence of palettes P_0..P_5, P_j hitting R+(col j)
    and R-(col j), with P_j & P_{j+1} = 0 including the wrap."""
    A = [ALLOWED[column(tau, j)] for j in range(6)]
    if any(len(a) == 0 for a in A):
        return False, True          # an empty side: UNSAT from clause (2)/(3) alone
    for p0 in A[0]:
        reach = {p0}
        for j in range(1, 6):
            reach = {q for q in A[j] if any(not (q & p) for p in reach)}
            if not reach: break
        if reach and any(not (q & p0) for q in reach):
            return True, False
    return False, False

def sat_dfs(tau):
    """independent implementation: backtracking DFS, no shared state with sat()"""
    A = [ALLOWED[column(tau, j)] for j in range(6)]
    seq = [0]*6
    def rec(j, prev):
        if j == 6:
            return not (seq[5] & seq[0])
        for p in A[j]:
            if not (p & prev):
                seq[j] = p
                if rec(j+1, p): return True
        return False
    for p0 in A[0]:
        seq[0] = p0
        if rec(1, p0): return True
    return False

def sat_masks(tau):
    """independent implementation over the UNRESTRICTED 64 palettes (all subsets of C):
    checks the 'reduced == unrestricted' claim on a sample."""
    A = []
    for j in range(6):
        col = column(tau, j); Rp, Rn = sides(col)
        A.append([P for P in range(1, 64) if (P & sum(1 << x for x in Rp)) and (P & sum(1 << x for x in Rn))])
    if any(not a for a in A): return False
    # reachability over 64 palettes, forward DP from every start
    for p0 in A[0]:
        reach = {p0}
        for j in range(1, 6):
            reach = {q for q in A[j] if any(not (q & p) for p in reach)}
            if not reach: break
        if reach and any(not (q & p0) for q in reach): return True
    return False

# ---------- the class space ----------
CLASSES = [canon((0,) + tail) for tail in product(range(6), repeat=5)]
IDX = {c: i for i, c in enumerate(CLASSES)}
NCL = len(CLASSES)
assert NCL == 7776 and len(set(CLASSES)) == 7776

def build_table(recompute=True, n=None, tablefile=None):
    T = [False]*NCL
    if tablefile:
        with open(tablefile) as f:
            for line in f:
                p = [int(x) for x in line.split()]
                if len(p) == 6: T[IDX[canon(tuple(p))]] = True
        return T, "parent table file " + tablefile
    n = NCL if n is None else n
    for c in range(n):
        T[c] = sat(CLASSES[c])[0]
    return T, f"recomputed {n} classes"

# ---------- subset bookkeeping ----------
SUBS = [[] for _ in range(64)]
for A in range(64):
    B = A
    while B:
        SUBS[A].append(B)
        B = (B - 1) & A
ORDER = sorted(range(64), key=lambda A: bin(A).count("1"))

def decremented_code(C, A):
    """index of the class [C - 1_A]"""
    return IDX[canon(tuple((C[i] - (1 if (A >> i) & 1 else 0)) % 6 for i in range(6)))]

def census(T):
    """dp[k][c][A] = number of alive chains 0 < ... < A with k blocks, for class c"""
    import numpy as np
    alive = np.zeros((NCL, 64), dtype=np.int64)
    for A in range(64):
        for c in range(NCL):
            alive[c, A] = 1 if T[decremented_code(CLASSES[c], A)] else 0
    dp = np.zeros((7, NCL, 64), dtype=np.int64)
    dp[0][:, 0] = 1
    for A in ORDER:
        for k in range(1, 7):
            s = np.zeros(NCL, dtype=np.int64)
            for B in SUBS[A]:
                s += dp[k-1][:, A ^ B]
        # note: each nonempty B is one block, so dp[k][A] gets sum over the last block B
            dp[k][:, A] = s * alive[:, A]
    return alive, dp

def run(argv):
    t0 = time.time()
    mode = "smoke"; n = 300; tablefile = None
    if "--full" in argv: mode = "full"
    if "--smoke" in argv: n = int(argv[argv.index("--smoke")+1])
    if "--table" in argv: tablefile = argv[argv.index("--table")+1]
    T, how = build_table(recompute=(tablefile is None), n=(n if mode == "smoke" else None), tablefile=tablefile)
    nsat = sum(T)
    print(f"[table] {how}: SAT={nsat}  UNSAT={NCL-nsat if not tablefile and (mode=='full') else '-'}")
    # independent spot checks
    smp = [0, 1, 2, 3, 4, 5, 100, 777, 1234, 4321, 7775]
    for c in smp:
        a = sat(CLASSES[c])[0]; b = sat_dfs(CLASSES[c]); m = sat_masks(CLASSES[c])
        assert a == b == m, (CLASSES[c], a, b, m)
    print(f"[spot] DP, backtracking DFS and unrestricted-64-mask rule agree on {len(smp)} sampled classes")
    alive, dp = census(T)
    tot_by_k = [int(dp[k][:, 63].sum()) for k in range(7)]
    allk = [int(dp[k][:, 63].sum()) for k in range(7)]
    print(f"[census] surviving staircases by number of blocks k=1..6: {allk[1:]}")
    print(f"[census] total surviving = {sum(allk[1:])}  of  7776*4683 = {7776*4683}")
    print(f"[time] {time.time()-t0:.2f}s")
    return T, dp, tot_by_k

if __name__ == "__main__":
    run(sys.argv[1:])
