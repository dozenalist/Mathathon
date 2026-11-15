#!/usr/bin/env python3
"""indep_ln3.py -- independent checker for the LN3 claims (T1: A6 paired palettes; T3: J-depth).

Written from scratch from the TEXT of LN3-FINDINGS.md, A6-FINITE-CHECK.md, STATUS.json and the
lane scripts (read as text only; nothing of theirs is imported or executed). stdlib only, reads no
file except itself (for its own sha256).

Algorithms deliberately differ from the lane's:
  T1  lane: label-wise independent-set reduction.  Here: position-wise enumeration over the 28
      per-position (H1)&(H2) options -- (a) exhaustive backtracking that lists every model and
      (b) an exact transfer-matrix count (trace / entry sum of 28x28 integer matrix products).
  T3  lane: DFS feasibility + DFS chains.  Here: layered forward-reachability feasibility test,
      permutation chains by BFS over subsets of decremented slots, simple paths via SCC
      (Tarjan) analysis + longest-path DP on the condensation, with exhaustive DFS only inside
      non-trivial SCCs if any exist.
"""
import sys, time, hashlib
from itertools import product
from collections import Counter

T_START = time.perf_counter()
SELF_SHA = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
VERDICTS = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def verdict(name, ok, detail):
    VERDICTS.append((name, ok, detail))
    say(f"  => {name}: {'CONFIRMED' if ok else 'DISAGREES'}  [{detail}]")


def bits(S):
    return sum(1 << x for x in S)


def members(m, n):
    return tuple(x for x in range(n) if (m >> x) & 1)


def popcount(m):
    return bin(m).count("1")


say(f"indep_ln3.py sha256 = {SELF_SHA}")
say(f"python {sys.version.split()[0]}")

# =====================================================================================
# T1 -- A6 setting.  Labels Fin 6, positions j in Fin 6 (indices mod 6).
#   f = (1,5,3,1,5,3)   (H1)  f_j in P_j
#   T = ({3,4,5},{1,2,3},{0,1,5},{3,4,5},{1,2,3},{0,1,5})   (H2)  P_j meets T_j
#   (H3) P_j disjoint P_{j+1}, cyclic (palette_sixty_disjoint); "path-only" drops pair (5,0).
#   g = (4,2,0,4,2,0) = f + 3 (mod 6)  (the forced partner label).
# =====================================================================================
say("\n=== T1: A6 paired-palette claims ===")
L = 6
f = (1, 5, 3, 1, 5, 3)
g = (4, 2, 0, 4, 2, 0)
h = (3, 1, 5, 3, 1, 5)
T = ({3, 4, 5}, {1, 2, 3}, {0, 1, 5}, {3, 4, 5}, {1, 2, 3}, {0, 1, 5})
Tm = [bits(t) for t in T]
say(f"f = {f}\ng = {g}  (g == f+3 mod 6: {all(g[j] == (f[j] + 3) % 6 for j in range(L))})")
say(f"T = {[sorted(t) for t in T]}\nh = {h}  (h == f+2 mod 6: {all(h[j] == (f[j] + 2) % 6 for j in range(L))})")


def H1(P, j):
    return (P >> f[j]) & 1 == 1


def H2(P, j):
    return (P & Tm[j]) != 0


def H3cyc(fam):
    return all((fam[j] & fam[(j + 1) % L]) == 0 for j in range(L))


def H3path(fam):
    return all((fam[j] & fam[j + 1]) == 0 for j in range(L - 1))


# ---- claim 1: per-position options, literal scan of all 64 subsets of Fin 6
OPT = [[P for P in range(1 << L) if H1(P, j) and H2(P, j)] for j in range(L)]
per = [len(o) for o in OPT]
size = 1
for c in per:
    size *= c
say(f"\n[1] per-position #(P subset Fin6 : H1 & H2) = {per}; product = {size:,}")
say(f"    closed-form check 2^5 - 2^2 = {2**5 - 2**2} (valid since f_j not in T_j: "
    f"{all(f[j] not in T[j] for j in range(L))})")
verdict("T1.1 (28 each, 28^6 = 481,890,304)", per == [28] * 6 and size == 481890304, f"{per}, {size}")

# ---- claim 2: W1 = {f_j, h_j}
W1 = [bits({f[j], h[j]}) for j in range(L)]
c2_h1 = all(H1(W1[j], j) for j in range(L))
c2_h2 = all(H2(W1[j], j) for j in range(L))
c2_miss = all(not (W1[j] >> g[j]) & 1 for j in range(L))
c2_h3 = H3cyc(W1)
bad_pairs = [(j, (j + 1) % L, members(W1[j] & W1[(j + 1) % L], L)) for j in range(L)
             if W1[j] & W1[(j + 1) % L]]
say(f"\n[2] W1 = {[members(P, L) for P in W1]}")
say(f"    H1 {c2_h1}  H2 {c2_h2}  misses g at all 6 positions {c2_miss}  H3(cyclic) {c2_h3}"
    f"  H3 failures {bad_pairs}")
verdict("T1.2 (W1 meets H1&H2 and misses g)", c2_h1 and c2_h2 and c2_miss,
        f"H1={c2_h1} H2={c2_h2} misses-g={c2_miss}; note W1 violates H3 at {len(bad_pairs)} pairs")

# ---- claim 3: two-label families
# Reading R1 (lane): P_j = {f_j, v_j}, v_j in T_j  -> 3^6 = 729 families, enumerated literally.
R1 = [tuple(bits({f[j], v[j]}) for j in range(L))
      for v in product(*[sorted(T[j]) for j in range(L)])]
r1_ok = [fam for fam in R1 if all(H1(fam[j], j) and H2(fam[j], j) for j in range(L))]
# Reading R2: P_j = {f_j, v_j}, v_j any label != f_j -> 5^6 = 15625, enumerated literally.
R2 = [tuple(bits({f[j], v[j]}) for j in range(L))
      for v in product(*[[x for x in range(L) if x != f[j]] for j in range(L)])]
r2_ok = [fam for fam in R2 if all(H1(fam[j], j) and H2(fam[j], j) for j in range(L))]
# Reading R3: P_j any 2-element subset (15^6); H1,H2 are per-position so the count is the product
two_ok = [[P for P in range(1 << L) if popcount(P) == 2 and H1(P, j) and H2(P, j)] for j in range(L)]
r3 = 1
for o in two_ok:
    r3 *= len(o)
two_ok_is_fT = all(sorted(two_ok[j]) == sorted(bits({f[j], t}) for t in T[j]) for j in range(L))
say(f"\n[3] R1 {{f_j,v_j}}, v_j in T_j: {len(r1_ok)} of {len(R1)} satisfy H1&H2")
say(f"    R2 {{f_j,v_j}}, v_j != f_j : {len(r2_ok)} of {len(R2)} satisfy H1&H2;"
    f" set equals R1: {set(r2_ok) == set(R1)}")
say(f"    R3 any 2-subsets (15^6)    : {r3} satisfy H1&H2; per-position they are exactly"
    f" {{f_j,t}}, t in T_j: {two_ok_is_fT}")
verdict("T1.3 (all 729 two-label families satisfy H1&H2)",
        len(R1) == 729 and len(r1_ok) == 729 and len(r2_ok) == 729 and r3 == 729,
        "729/729 (R1), 729/15625 (R2), 729 (R3) -- same set under every reading")

# ---- claim 4: adding (H3) cyclic
r1_h3 = [fam for fam in r1_ok if H3cyc(fam)]
target = tuple(bits({f[j], g[j]}) for j in range(L))


def backtrack(cyclic):
    """Exhaustive over OPT[0] x ... x OPT[5] (28^6); prunes only on violated path edges."""
    models = []
    fam = []

    def rec(j):
        if j == L:
            if (not cyclic) or (fam[-1] & fam[0]) == 0:
                models.append(tuple(fam))
            return
        for P in OPT[j]:
            if j and (P & fam[-1]):
                continue
            fam.append(P)
            rec(j + 1)
            fam.pop()

    rec(0)
    return models


def matmul(X, Y):
    n, m, p = len(X), len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][c] for k in range(m)) for c in range(p)] for i in range(n)]


def transfer(j, k):
    return [[1 if (a & b) == 0 else 0 for b in OPT[k]] for a in OPT[j]]


M = transfer(0, 1)
for j in range(1, L - 1):
    M = matmul(M, transfer(j, j + 1))          # positions 0 -> 5 along the path
path_count_tm = sum(sum(r) for r in M)
Mc = matmul(M, transfer(L - 1, 0))             # close the cycle 5 -> 0
cyc_count_tm = sum(Mc[i][i] for i in range(len(Mc)))

cyc_models = backtrack(True)
path_models = backtrack(False)
say(f"\n[4] R1 two-label families with H1&H2&H3(cyclic): {len(r1_h3)} -> "
    f"{[[members(P, L) for P in fam] for fam in r1_h3]}")
say(f"    all families (28^6 space) with H1&H2&H3(cyclic): backtracking {len(cyc_models)}, "
    f"transfer-matrix trace {cyc_count_tm}")
say(f"    unique model = {{f_j,g_j}}: {cyc_models == [target]} ; model = "
    f"{[members(P, L) for P in cyc_models[0]] if cyc_models else None}")
verdict("T1.4 (adding H3 leaves exactly 1)",
        len(r1_h3) == 1 and r1_h3[0] == target and len(cyc_models) == 1 and cyc_count_tm == 1
        and cyc_models[0] == target,
        "1 in the 729 two-label space and 1 in the full 28^6 space, = {f_j,g_j}")

# ---- claim 5: path-only (no 5-0 wrap)
r1_path = [fam for fam in r1_ok if H3path(fam)]
say(f"\n[5] all families (28^6 space) with H1&H2&H3(path only): backtracking {len(path_models)}, "
    f"transfer-matrix sum {path_count_tm}")
say(f"    (for reference: inside the 729 two-label space the path-only count is {len(r1_path)})")
labelset_sizes = Counter(tuple(popcount(P) for P in fam) for fam in path_models)
say(f"    palette-size profiles among the path-only models: {dict(sorted(labelset_sizes.items()))}")
verdict("T1.5 (path-only gives exactly 64)", len(path_models) == 64 and path_count_tm == 64,
        f"full-family space: {len(path_models)} (two-label space: {len(r1_path)})")
say(f"T1 runtime {time.perf_counter() - T_START:.2f} s")

# =====================================================================================
# T3 -- J-depth.  Definitions (LN3-FINDINGS, STATUS.json block jdepth, m6 Lemma 1):
#   slots/rows i, columns k, labels x all in Z_N; sigma in Z_N^N; window w.
#   F_k = {i : (k - sigma_i) mod N in {0..w-1}}        (M_{i,k} = 1)
#   A_k = J(F_k) = {x : x not in F_k and x-1 not in F_k}
#   B_k = J(F_k^c) = {x : x in F_k and x-1 in F_k}
#   sigma in W  iff  exist Q_0..Q_{N-1} subset Z_N, Q_k meets A_k and B_k, Q_k disj Q_{k+1} (cyclic)
#   Ap = {sigma in W : residues (sigma_i - i) mod N lie in {c, c+1} for some c};  Am with +i
#   J = W \ (Ap u Am)
#   permutation chain: sigma, sigma - e_{p1}, sigma - e_{p1} - e_{p2}, ... (each slot at most once);
#     depth = longest initial run of states inside W (counted in states, max N+1)
#   simple path: any sequence of single-slot decrements, states pairwise distinct, all in W.
# Reduction used in the W test: if (Q_k) works, choosing a_k in Q_k&A_k, b_k in Q_k&B_k and
# Q'_k = {a_k, b_k} also works (subsets keep disjointness) -- so Q_k ranges over {a,b}, a in A, b in B.
# This reduction is cross-checked against the unreduced test (all 2^N subsets) on N=6.
# =====================================================================================


def make_T3(N, w):
    FULL = (1 << N) - 1

    def shift_up(F):  # {x : x-1 in F}
        return ((F << 1) | (F >> (N - 1))) & FULL

    AB = []
    ALLOW = []
    for F in range(1 << N):
        A = FULL & ~F & ~shift_up(F)
        B = F & shift_up(F)
        AB.append((A, B))
        ALLOW.append(tuple(sorted({(1 << a) | (1 << b) for a in members(A, N) for b in members(B, N)})))
    # packed F-tuple contribution of row i holding value v: bit i in each column k of v's window
    CONTRIB = [[sum((1 << i) << (N * ((v + t) % N)) for t in range(w)) for v in range(N)]
               for i in range(N)]

    def columns(s):
        P = 0
        for i in range(N):
            P += CONTRIB[i][s[i]]
        return [(P >> (N * k)) & FULL for k in range(N)]

    def feasible(S):
        """layered forward reachability around the cycle of columns, from the thinnest column."""
        if not all(S):
            return False
        k0 = min(range(N), key=lambda k: len(S[k]))
        order = [(k0 + t) % N for t in range(1, N)]
        for q0 in S[k0]:
            cur = (q0,)
            for k in order:
                cur = tuple(q for q in S[k] if any(not (q & r) for r in cur))
                if not cur:
                    break
            else:
                if any(not (r & q0) for r in cur):
                    return True
        return False

    def inW(s):
        return feasible([ALLOW[F] for F in columns(s)])

    def inW_unreduced(s):
        """No two-element reduction: Q_k ranges over ALL subsets meeting A_k and B_k."""
        S = []
        for F in columns(s):
            A, B = AB[F]
            S.append(tuple(q for q in range(1, 1 << N) if (q & A) and (q & B)))
        return feasible(S)

    return inW, inW_unreduced, columns, AB


def twoc(vals, N):
    S = set(vals)
    return any(S <= {c, (c + 1) % N} for c in range(N))


def dec(s, i, N):
    t = list(s)
    t[i] = (t[i] - 1) % N
    return tuple(t)


def perm_depth(s, N, W):
    """BFS over subsets X of slots: X reachable iff sigma - chi_X in W and X minus some slot reachable."""
    layer = {0}
    best = 1
    for t in range(1, N + 1):
        nxt = set()
        for X in layer:
            for i in range(N):
                if (X >> i) & 1:
                    continue
                Y = X | (1 << i)
                if Y in nxt:
                    continue
                st = tuple((s[j] - ((Y >> j) & 1)) % N for j in range(N))
                if st in W:
                    nxt.add(Y)
        if not nxt:
            break
        layer = nxt
        best = t + 1
    return best


def tarjan(nodes, succ):
    """iterative Tarjan SCC; returns list of SCCs (each a list), in reverse topological order."""
    index = {}
    low = {}
    onstack = set()
    stack = []
    sccs = []
    counter = 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, 0)]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        onstack.add(root)
        while work:
            v, pi = work[-1]
            nb = succ[v]
            if pi < len(nb):
                work[-1] = (v, pi + 1)
                u = nb[pi]
                if u not in index:
                    index[u] = low[u] = counter
                    counter += 1
                    stack.append(u)
                    onstack.add(u)
                    work.append((u, 0))
                elif u in onstack:
                    low[v] = min(low[v], index[u])
            else:
                work.pop()
                if work:
                    p = work[-1][0]
                    low[p] = min(low[p], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        x = stack.pop()
                        onstack.discard(x)
                        comp.append(x)
                        if x == v:
                            break
                    sccs.append(comp)
    return sccs


def run_T3(N, w, cross_check_unreduced=False):
    t0 = time.perf_counter()
    inW, inW_unreduced, columns, AB = make_T3(N, w)
    W = set()
    for s in product(range(N), repeat=N):
        if inW(s):
            W.add(s)
    tW = time.perf_counter() - t0
    # sanity: invariance of W under sigma -> sigma + c (all entries), checked exhaustively
    shift_inv = all(tuple((x + 1) % N for x in s) in W for s in W)
    Ap = {s for s in W if twoc([(s[i] - i) % N for i in range(N)], N)}
    Am = {s for s in W if twoc([(s[i] + i) % N for i in range(N)], N)}
    J = W - Ap - Am
    say(f"\n[N={N}, w={w}] |W| = {len(W)}  |Ap| = {len(Ap)}  |Am| = {len(Am)}  |Ap&Am| = {len(Ap & Am)}"
        f"  |J| = {len(J)}   (W built in {tW:.1f} s; W invariant under +1 shift: {shift_inv})")
    if cross_check_unreduced:
        t1 = time.perf_counter()
        mism = [s for s in product(range(N), repeat=N) if inW_unreduced(s) != (s in W)]
        say(f"    unreduced (all-subsets) W test over all {N**N} sigma: mismatches = {len(mism)}"
            f"  ({time.perf_counter() - t1:.1f} s)")
    # permutation chains
    pd = {s: perm_depth(s, N, W) for s in J}
    dist = Counter(pd.values())
    pmax = max(pd.values()) if pd else 0
    attain = sorted(s for s in J if pd[s] == pmax)
    say(f"    permutation-chain depth from J: max = {pmax}; distribution {dict(sorted(dist.items()))};"
        f" attaining states {len(attain)}, e.g. {attain[0] if attain else None}")
    # simple paths: decrement graph restricted to W, part reachable from J
    succ = {}
    frontier = list(J)
    seen = set(J)
    while frontier:
        v = frontier.pop()
        nb = [u for u in (dec(v, i, N) for i in range(N)) if u in W]
        succ[v] = nb
        for u in nb:
            if u not in seen:
                seen.add(u)
                frontier.append(u)
    nodes = sorted(seen)
    nedges = sum(len(succ[v]) for v in nodes)
    sccs = tarjan(nodes, succ)
    big = [c for c in sccs if len(c) > 1]
    selfloops = [v for v in nodes if v in succ[v]]
    reach_types = Counter('Ap' if v in Ap else 'Am' if v in Am else 'J' for v in nodes)
    say(f"    decrement subgraph of W reachable from J: {len(nodes)} states {dict(reach_types)},"
        f" {nedges} edges, SCCs {len(sccs)}, non-trivial SCCs {len(big)}"
        f" (sizes {sorted(len(c) for c in big)[-5:]}), self-loops {len(selfloops)}")
    res = {"W": len(W), "Ap": len(Ap), "Am": len(Am), "J": len(J), "perm_max": pmax,
           "perm_dist": dict(dist), "W_set": W, "Jset": J, "Ap_set": Ap, "Am_set": Am}
    if not big and not selfloops:
        # DAG: longest path (in states) via DP in reverse topological order (Tarjan output order)
        longest = {}
        nxt = {}
        for comp in sccs:
            v = comp[0]
            best, arg = 1, None
            for u in succ[v]:
                if longest[u] + 1 > best:
                    best, arg = longest[u] + 1, u
            longest[v] = best
            nxt[v] = arg
        smax = max(longest[s] for s in J)
        sdist = Counter(longest[s] for s in J)
        start = min(s for s in J if longest[s] == smax)
        path = [start]
        while nxt[path[-1]] is not None:
            path.append(nxt[path[-1]])
        say(f"    graph is acyclic -> exact longest simple path from J (states): {smax};"
            f" distribution {dict(sorted(sdist.items()))}")
        say(f"    a longest path: {' -> '.join(''.join(map(str, p)) for p in path)}")
        res["simple_max"] = smax
        res["simple_exact"] = True
    else:
        res["simple_max"] = None
        res["simple_exact"] = False
        say("    graph has cycles: no DAG longest-path DP; rigorous bounds computed below")
    res["succ"] = succ
    res["sccs"] = big
    say(f"    [N={N}] T3 runtime {time.perf_counter() - t0:.1f} s")
    return res


say("\n=== T3: J-depth (calibration at N=6, then claim at (m,w)=(7,3)) ===")
r6 = run_T3(6, 3, cross_check_unreduced=True)
calib = (r6["W"], r6["Ap"], r6["Am"], r6["J"], r6["perm_max"], r6["perm_dist"])
calib_ok = calib == (1062, 378, 378, 306, 3, {1: 90, 2: 144, 3: 72})
say(f"    calibration vs record (1062, 378, 378, 306, depth 3, {{1:90,2:144,3:72}}): "
    f"{'MATCH' if calib_ok else 'MISMATCH ' + str(calib)}")

r7 = run_T3(7, 3)
verdict("T3a (7,3) permutation-chain J-depth = 8", r7["perm_max"] == 8, f"computed {r7['perm_max']}")

# the FINDINGS witness path of 13 states
wit = ["1153450", "1143450", "1133450", "1133456", "1123456", "0123456", "6123456",
       "6123356", "6123355", "6122355", "6122345", "6112345", "5112345"]
wit = [tuple(int(c) for c in x) for x in wit]
steps_ok = all(sum(1 for i in range(7) if wit[t][i] != wit[t + 1][i]) == 1 and
               any(dec(wit[t], i, 7) == wit[t + 1] for i in range(7)) for t in range(len(wit) - 1))
say(f"\n    FINDINGS 13-state witness: start in J {wit[0] in r7['Jset']}, all in W "
    f"{all(x in r7['W_set'] for x in wit)}, single decrements {steps_ok}, distinct {len(set(wit)) == 13};"
    f" types {''.join('P' if x in r7['Ap_set'] else 'M' if x in r7['Am_set'] else 'J' for x in wit)}")

if r7["simple_exact"]:
    verdict("T3b (7,3) simple-path J-depth = 13", r7["simple_max"] == 13, f"computed exact {r7['simple_max']}")
else:
    # The reachable decrement graph has non-trivial SCCs, so an exhaustive longest-simple-path search
    # is not feasible (longest path in a 1918-node strongly connected digraph). Instead:
    #  (UB) rigorous upper bound: a simple path meets SCCs in topological order and visits each SCC's
    #       states at most once -> longest |SCC|-weighted path in the condensation from a J-containing SCC;
    #  (LB) constructive lower bound: explicit simple paths found by a deterministic Warnsdorff-type
    #       greedy walk, each one re-verified state by state below.
    succ = r7["succ"]
    W7, J7 = r7["W_set"], r7["Jset"]
    allsccs = tarjan(sorted(succ), succ)          # reverse topological order
    comp_of = {}
    for ci, comp in enumerate(allsccs):
        for v in comp:
            comp_of[v] = ci
    wbest = {}
    for ci, comp in enumerate(allsccs):           # successors' SCCs come earlier in this order
        outs = {comp_of[u] for v in comp for u in succ[v]} - {ci}
        wbest[ci] = len(comp) + max((wbest[d] for d in outs), default=0)
    UB = max(wbest[comp_of[s]] for s in J7)
    big_ids = sorted({comp_of[v] for c in r7["sccs"] for v in c})
    for ci in big_ids:
        comp = allsccs[ci]
        say(f"    non-trivial SCC #{ci}: {len(comp)} states, types "
            f"{dict(Counter('Ap' if v in r7['Ap_set'] else 'Am' if v in r7['Am_set'] else 'J' for v in comp))}")
    say(f"    rigorous upper bound on a simple in-W path from J (|SCC|-weighted condensation path): {UB}")

    def greedy(start):
        path, on, v = [start], {start}, start
        while True:
            cands = [u for u in succ[v] if u not in on]
            if not cands:
                return path
            v = min(cands, key=lambda u: (sum(1 for x in succ[u] if x not in on), u))
            path.append(v)
            on.add(v)

    starts = sorted(s for s in J7 if comp_of[s] in big_ids)
    starts = starts[::max(1, len(starts) // 120)]  # deterministic sample of ~120 J starts inside the SCCs
    best_path = max((greedy(s) for s in starts), key=len)
    ok_path = (best_path[0] in J7 and all(x in W7 for x in best_path) and len(set(best_path)) == len(best_path)
               and all(any(dec(best_path[t], i, 7) == best_path[t + 1] for i in range(7))
                       for t in range(len(best_path) - 1)))
    LB = len(best_path) if ok_path else 13
    say(f"    constructive lower bound (greedy over {len(starts)} J starts): explicit simple in-W path of "
        f"{len(best_path)} states from J; re-verified (start in J, all in W, distinct, unit decrements): {ok_path}")
    say(f"    first 20 states: {' -> '.join(''.join(map(str, p)) for p in best_path[:20])} ...")
    say(f"    => longest simple in-W path from a J state at (7,3) lies in [{LB}, {UB}]")
    VERDICTS.append(("T3b (7,3) simple-path J-depth = 13", False if LB > 13 else None,
                     f"13 is only a lower bound (FINDINGS' witness re-verified); exact value UNDETERMINED, "
                     f"in [{LB}, {UB}]"))
    say(f"  => T3b (7,3) simple-path J-depth = 13: {'DISAGREES' if LB > 13 else 'UNDETERMINED'}"
        f"  [as an exact maximum; value in [{LB}, {UB}]]")

say("\n=== SUMMARY ===")
for name, ok, detail in VERDICTS:
    tag = "CONFIRMED" if ok is True else ("DISAGREES" if ok is False else "UNDETERMINED")
    say(f"{tag:12s} {name}  [{detail}]")
say(f"T3 calibration at N=6: {'MATCH' if calib_ok else 'MISMATCH'}")
say(f"total runtime {time.perf_counter() - T_START:.1f} s")
