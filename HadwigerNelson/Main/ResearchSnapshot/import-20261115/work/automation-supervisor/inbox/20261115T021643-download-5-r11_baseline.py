#!/usr/bin/env python3
"""Judge-side baseline for owner spec R1-1 (L-R1). NOT a swarm submission.

Written from the R1-1 model statement only; no other lane's script is imported or
read. Purpose: give the parent an independent set of numbers to adjudicate the
swarm's reports against.

MODEL (R1-1, verbatim encoding).
  C = {0..5}; E_i = {i, i+1 mod 6}; alpha_i in degrees mod 360.
  Ppos(x) = {i : cos(x - alpha_i) > 0};  Pneg likewise with < 0.
  Rp = C \\ union{E_i : i in Ppos};  Rn likewise.
  t_j = t + 60 j.  R(t,alpha) asks for P_0..P_5 subset C with
     P_j meets Rp(t_j) and Rn(t_j),  P_j disjoint P_{j+1} cyclically.
  Sign class tau in (Z/6)^6, tau_0 = 0, with
     cos(t+60j-alpha_i) > 0  iff  (j - tau_i) mod 6 in {0,1,5}.
  Staircase: ordered set partition (B_1..B_k) of {0..5} gives the chain
     tau - 1_{B_1 u ... u B_m}, m = 1..k; survives iff every class SAT.

No floats anywhere: angles are Fractions of degrees, and every sign test is a
rational comparison against +-90.
"""
from fractions import Fraction as F
from itertools import permutations
import json, time, hashlib, sys

C = tuple(range(6))
E = [frozenset({i, (i + 1) % 6}) for i in range(6)]

# ---------------------------------------------------------------- exact cos sign
def sgn_cos(d):
    """sign of cos(d) for a Fraction d in degrees: +1, -1, or 0. Exact."""
    r = d % 360
    if r < 90 or r > 270: return 1
    if r == 90 or r == 270: return 0
    return -1

# ---------------------------------------------------------------- classes
def tau_digits(t):
    """tau as a 5-tuple (tau_1..tau_5) given a 6-tuple with tau_0 = 0."""
    return tuple(t[i] % 6 for i in range(1, 6))
def id_of(d):
    v = 0
    for x in reversed(d): v = v * 6 + x
    return v
def digits_of(v):
    out = []
    for _ in range(5): out.append(v % 6); v //= 6
    return tuple(reversed(out))

ALL_IDS = [id_of(d) for d in ((a,b,c,e,f) for a in range(6) for b in range(6)
                              for c in range(6) for e in range(6) for f in range(6))]
DIG = {v: digits_of(v) for v in ALL_IDS}

def rows(tau):
    """(Rp(j), Rn(j)) for j=0..5, from the class rule (j - tau_i) mod 6 in {0,1,5}."""
    out = []
    for j in range(6):
        pos = [i for i in range(6) if (j - tau[i]) % 6 in (0, 1, 5)]
        neg = [i for i in range(6) if (j - tau[i]) % 6 in (2, 3, 4)]
        Rp = set(C).difference(*[E[i] for i in pos]) if pos else set(C)
        Rn = set(C).difference(*[E[i] for i in neg]) if neg else set(C)
        out.append((frozenset(Rp), frozenset(Rn)))
    return out

def class_from_tau(tau6):
    return tau_digits(tuple(x % 6 for x in tau6))

# ---------------------------------------------------------------- solvers
def pals_min(Rp, Rn):
    """minimal hitting sets of both Rp and Rn: {x,y}, x in Rp, y in Rn."""
    s = set()
    for x in Rp:
        for y in Rn:
            s.add(frozenset((x, y)))
    return sorted(s, key=lambda p: (len(p), tuple(sorted(p))))

def solve_dfs(R):
    """impl A: recursive DFS over minimal palettes, wrap constraint checked at the end."""
    D = [pals_min(Rp, Rn) for Rp, Rn in R]
    if any(not d for d in D): return False
    seq = [None] * 6
    def rec(j, prev):
        if j == 6: return not (seq[5] & seq[0])
        for p in D[j]:
            if not (p & prev):
                seq[j] = p
                if rec(j + 1, p): return True
        seq[j] = None
        return False
    for p in D[0]:
        seq[0] = p
        if rec(1, p): return True
    return False

def solve_dp(R):
    """impl B: reachable-set DP per starting palette, no recursion."""
    D = [pals_min(Rp, Rn) for Rp, Rn in R]
    if any(not d for d in D): return False
    for start in D[0]:
        S = [start]
        for j in range(1, 6):
            S = [m for m in D[j] if any(not (m & q) for q in S)]
            if not S: break
        else:
            if any(not (m & start) for m in S): return True
    return False

def solve_full(R):
    """impl C: unrestricted, all nonempty masks per column (minimality NOT used)."""
    from itertools import combinations as _comb
    allm = [frozenset(T) for r in range(1, 7) for T in _comb(C, r)]
    D = []
    for Rp, Rn in R:
        D.append([m for m in allm if (m & Rp) and (m & Rn)])
    if any(not d for d in D): return False
    for m0 in D[0]:
        S = [m0]
        for j in range(1, 6):
            S = [m for m in D[j] if any(not (m & q) for q in S)]
            if not S: break
        else:
            if any(not (m & m0) for m in S): return True
    return False

def propagate(R):
    """label-level unit propagation. vars x[i][j]. Returns (refuted, rounds)."""
    Rp = [R[j][0] for j in range(6)]
    Rn = [R[j][1] for j in range(6)]
    val = {}                      # (i,j) -> True/False
    def get(i, j): return val.get((i, j))
    changed = True; rounds = 0
    while changed:
        changed = False; rounds += 1
        for j in range(6):        # clause: some i in Rp(j) true
            for S in (Rp[j], Rn[j]):
                lits = [i for i in S if get(i, j) is not False]
                if any(get(i, j) is True for i in S):
                    continue
                if not lits: return True, rounds
                if len(lits) == 1:
                    if get(lits[0], j) is not True:
                        val[(lits[0], j)] = True; changed = True
        for (i, j), v in list(val.items()):
            if v is True:
                for k in ((j - 1) % 6, (j + 1) % 6):
                    if get(i, k) is not False:
                        val[(i, k)] = False; changed = True
    return False, rounds

def propagate_palette(R):
    """palette-level unit propagation over the 6 positions."""
    D = [pals_min(Rp, Rn) for Rp, Rn in R]
    if any(not d for d in D): return True
    changed = True
    while changed:
        changed = False
        forced = set()
        for j in range(6):
            if not D[j]: return True
            inter = set(C)
            for p in D[j]: inter &= set(p)
            if inter: forced.add((j, min(inter)))
        for (j, x) in forced:
            for k in ((j - 1) % 6, (j + 1) % 6):
                keep = [p for p in D[k] if x not in p]
                if len(keep) != len(D[k]):
                    D[k] = keep; changed = True
                    if not D[k]: return True
    return False

# ---------------------------------------------------------------- (a) fixed phase
t0 = time.time()
SAT, EMPTY, NONEMPTY_UNSAT = set(), set(), set()
PROP_INC_LAB, PROP_INC_PAL, MISMATCH = [], [], []
for v in ALL_IDS:
    tau = (0,) + DIG[v]
    R = rows(tau)
    empty = any((not Rp) or (not Rn) for Rp, Rn in R)
    if empty:
        EMPTY.add(v); continue
    a = solve_dfs(R); b = solve_dp(R)
    if a != b: MISMATCH.append(v)
    if a:
        SAT.add(v)
    else:
        NONEMPTY_UNSAT.add(v)
        if not propagate(R)[0]: PROP_INC_LAB.append(v)
        if not propagate_palette(R): PROP_INC_PAL.append(v)
t_fixed = time.time() - t0
# unrestricted cross-check on all classes (impl C)
t0 = time.time()
MISMATCH_FULL = []
for v in ALL_IDS:
    R = rows((0,) + DIG[v])
    if solve_dfs(R) != solve_full(R): MISMATCH_FULL.append(v)
t_full = time.time() - t0
FIXED = {"sat": len(SAT), "unsat": 7776 - len(SAT), "nonempty_unsat": len(NONEMPTY_UNSAT),
         "empty_side_classes": len(EMPTY), "propagation_incomplete": len(PROP_INC_LAB),
         "propagation_incomplete_palette_level": len(PROP_INC_PAL),
         "dfs_vs_dp_mismatch": len(MISMATCH), "minimal_vs_unrestricted_mismatch": len(MISMATCH_FULL),
         "seconds": round(t_fixed + t_full, 2)}

# ---------------------------------------------------------------- (b) staircases
import numpy as np
t0 = time.time()
SUBS = [()] + [(x,) for x in range(6)]
from itertools import combinations
SUBS = [A for r in range(7) for A in combinations(range(6), r)]
SUBI = {A: i for i, A in enumerate(SUBS)}
FULL = tuple(range(6))
# f[iA][v] = SAT(canon(tau - 1_A)) ; canon subtracts coordinate 0
f = np.zeros((64, 7776), dtype=np.int64)
idpos = {v: i for i, v in enumerate(ALL_IDS)}
for A in SUBS:
    sub = set(A)
    for v in ALL_IDS:
        d = DIG[v]
        full6 = (0,) + d
        shifted = tuple((full6[i] - (1 if i in sub else 0)) % 6 for i in range(6))
        c = tuple((shifted[i] - shifted[0]) % 6 for i in range(1, 6))
        f[SUBI[A], idpos[v]] = 1 if id_of(c) in SAT else 0
zero = SUBI[()]
dp = np.zeros((64, 8, 7776), dtype=np.int64)
dp[zero, 0, :] = f[zero, :]
for b in range(0, 7):
    S = dp[:, b, :].copy()
    for i in range(6):                       # subset zeta transform
        for A in SUBS:
            if i in A:
                B = tuple(x for x in A if x != i)
                S[SUBI[A], :] += S[SUBI[B], :]
    for A in SUBS:
        if A == (): continue
        proper = S[SUBI[A], :] - dp[SUBI[A], b, :]
        dp[SUBI[A], b + 1, :] = np.where(f[SUBI[A], :] == 1, proper, 0)
by_k = [int(dp[SUBI[FULL], k, :].sum()) for k in range(1, 7)]
t_stair = time.time() - t0
# Fubini(6) = 4683 from k! S(6,k)
S2 = [[0]*7 for _ in range(7)]
S2[0][0] = 1
for n in range(1, 7):
    for k in range(1, n+1):
        S2[n][k] = k*S2[n-1][k] + S2[n-1][k-1]
import math
fub = [(k, math.factorial(k)*S2[6][k]) for k in range(1, 7)]
STAIR = {"by_k": by_k, "total": sum(by_k), "space": 7776*sum(v for _, v in fub),
         "fubini_slices": fub, "fubini": sum(v for _, v in fub), "seconds": round(t_stair, 2)}

# ---------------------------------------------------------------- (c) all phases
t0 = time.time()
SATL = sorted(SAT)
EMPTYL = sorted(EMPTY)
def translate(ids, d):
    out = set()
    for v in ids:
        g = DIG[v]
        out.add(id_of(tuple(((g[i] + d[i]) % 6) for i in range(5))))
    return out
# class at phase t for alpha_i = 60(n_i + f_i): tau_i = round(-(alpha_i - t)/60) mod 6
def cls_digits(n, f, t):
    n = (0,) + tuple(n)          # n is the 5-tuple (n_1..n_5); alpha_0 = 0 fixes n_0 = 0
    tau = []
    for i in range(6):
        u = F(60)*(F(n[i]) + f[i]) - F(t)
        u = u / 60
        tau.append(int((-u + F(1, 2)).__floor__()) % 6)
    return tuple((tau[i] - tau[0]) % 6 for i in range(1, 6))
ORD = list(permutations(range(5)))    # orderings of f_1..f_5
field = empty_fail = c2_fail = 0
nvals = [digits_of(v) for v in ALL_IDS]        # all n in (Z/6)^5
for order in ORD:
    f = [F(0)] + [F(order.index(i-1) + 1, 6) for i in range(1, 6)]   # f_0 = 0, ranks 1..5 over 6
    # six arcs of R/60Z: boundaries at 60 f_i + 30 mod 60 -> midpoints
    bnd = sorted({(F(60)*f[i] + 30) % 60 for i in range(6)})
    mids = [ (bnd[k] + (bnd[(k+1) % len(bnd)] + (60 if k+1 == len(bnd) else 0)))/2 % 60
             for k in range(len(bnd)) ]
    # simpler and exact: direct count per cell over n (7776) once per ordering
    chain_ok = 0; chain_empty = 0; chain_c2 = 0
    for n in nvals:
        cs = [id_of(cls_digits(n, f, t)) for t in mids]
        if any(c in EMPTY for c in cs): chain_empty += 1
        elif all(c in SAT for c in cs): chain_ok += 1
        else: chain_c2 += 1
    field += chain_ok; empty_fail += chain_empty; c2_fail += chain_c2
t_all = time.time() - t0
ALLPH = {"cells": len(ORD)*7776, "field": field, "empty_side": empty_fail, "c2_only": c2_fail,
         "sum_check": field + empty_fail + c2_fail, "seconds": round(t_all, 2)}

# ---------------------------------------------------------------- (d) sign cells
signcells = set(); basechambers = set()
for order in ORD:
    f = [F(0)] + [F(order.index(i-1) + 1, 6) for i in range(1, 6)]
    bnd = sorted({(F(60)*f[i] + 30) % 60 for i in range(6)})
    mids = [ (bnd[k] + (bnd[(k+1) % len(bnd)] + (60 if k+1 == len(bnd) else 0)))/2 % 60
             for k in range(len(bnd)) ]
    for n in nvals:
        cs = [id_of(cls_digits(n, f, t)) for t in mids]
        if all(c in SAT for c in cs):
            basechambers.add(order)
            signcells.add((order, tuple(x % 2 for x in n)))
SIGN = {"signcells_total": len(ORD)*2**5, "signcells_meeting": len(signcells),
        "basechambers_total": len(ORD), "basechambers_meeting": len(basechambers)}

# ---------------------------------------------------------------- (e) two vectors
def vector_check(degs):
    al = [F(d) for d in degs]
    bnd = sorted({(al[i] + 30) % 60 for i in range(6)})
    mids = [ (bnd[k] + (bnd[(k+1) % len(bnd)] + (60 if k+1 == len(bnd) else 0)))/2 % 60
             for k in range(len(bnd)) ]
    per = []
    for t in mids:
        tau = []
        for i in range(6):
            u = (al[i] - t) / 60
            tau.append(int((-u + F(1, 2)).__floor__()) % 6)
        c = tuple((tau[i] - tau[0]) % 6 for i in range(1, 6))
        v = id_of(c)
        per.append({"t": str(t), "class": c, "sat": v in SAT,
                    "empty_side": v in EMPTY, "c2": (v not in SAT and v not in EMPTY)})
    f = [ (al[i]/60) % 1 for i in range(6) ]
    return {"alpha": [str(a) for a in al], "arcs": len(mids), "per_arc": per,
            "field": all(p["sat"] for p in per),
            "frac_parts": [str(x) for x in f],
            "frac_distinct": len(set(f)) == 6}

VEC = {"v1": vector_check([0, 30, 90, 150, 240, 300]),
       "v2": vector_check([0, F(435, 4), F(495, 4), F(285, 2), F(585, 2), F(315)])}

EQUAL = {"cells": 120*6**5, "cell_measure_of_total": str(F(1, 120*6**5)),
         "sat_measure": str(F(1440, 120*6**5)),
         "why": "alpha_0 = 0; each cell = (open ordering simplex of f_1..f_5, volume 1/5! by coordinate-permutation symmetry) x (n_1..n_5 in Z/6, each a translate slab of length 1/6), so all 120*6^5 cells have equal measure; field count 1440 gives 1440/933120 = 1/648"}
OUT = {"equal_measure": EQUAL, "fixed": FIXED, "staircase": STAIR, "allphase": ALLPH, "signcells": SIGN,
       "basechambers": {"total": SIGN["basechambers_total"], "meeting": SIGN["basechambers_meeting"]},
       "vectors": VEC,
       "measure": str(F(field, len(ORD)*7776)) if field else None}
print(json.dumps(OUT, indent=1, default=str))
