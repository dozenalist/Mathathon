"""CORRECTED AC-conditional enumeration (supersedes ac_filter_enum.py).

BUG FIXED (found by parent audit): the old cycle_feasible() used a complete reachability DP but
then reconstructed a witness GREEDILY, taking the first palette disjoint from the current one.
A greedy choice can dead-end at j=5 even when a valid cyclic path exists, so the old code reported
false NEGATIVES (95 instead of 174).  Fixed by DP with FULL PREDECESSOR TRACKING, and independently
cross-checked by a separately written backtracking DFS.

Declared finite space: q in {0..5}^6 with q0 = 0 (one representative per label-translation class);
six-cycle interfaces E_i = {i,(i+1) mod 6}; labels C = {0..5}.
Conditions: (AC) for every direction d, |union{E_i : q_i=d}| <= 3;
            (SIX) C1..C5 at every angle with |P_j| <= 2, cyclic adjacency.
Integer/bitmask arithmetic only. One process, one thread.
"""
import sys, time, itertools
T0 = time.time()
C = (1 << 6) - 1
E = [(1 << i) | (1 << ((i + 1) % 6)) for i in range(6)]
SIGN = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}
pc = lambda x: bin(x).count("1")

PAL = []
for a in range(6):
    P = 1 << a
    if not any(P & ~e == 0 for e in E): PAL.append(P)
for a, b in itertools.combinations(range(6), 2):
    P = (1 << a) | (1 << b)
    if not any(P & ~e == 0 for e in E): PAL.append(P)

def allowed_lists(q):
    out = []
    for u in range(6):
        up = dn = 0
        for i in range(6):
            if SIGN[(u - q[i]) % 6] == 1: up |= E[i]
            else:                         dn |= E[i]
        cp, cn = C & ~up, C & ~dn
        out.append(frozenset(P for P in PAL if (P & cp) and (P & cn)))
    return out

def ac_ok(q):
    for d in range(6):
        U = 0
        for i in range(6):
            if q[i] == d: U |= E[i]
        if pc(U) >= 4: return False
    return True

# ---------------- method 1: DP with full predecessor tracking --------------
def feasible_dp(A):
    if any(len(a) == 0 for a in A): return None
    for p0 in A[0]:
        reach = [set() for _ in range(6)]
        pred = [dict() for _ in range(6)]
        reach[0] = {p0}
        for j in range(1, 6):
            cur = {}
            for p in A[j]:
                for r in reach[j - 1]:
                    if (p & r) == 0:
                        cur[p] = r; break
            reach[j] = set(cur); pred[j] = cur
            if not reach[j]: break
        if not reach[5]: continue
        for p5 in reach[5]:
            if (p5 & p0) == 0:
                seq = [None] * 6; seq[5] = p5; c = p5
                for j in range(5, 0, -1):
                    c = pred[j][c]; seq[j - 1] = c
                if seq[0] == p0: return seq
    return None

# ---------------- method 2: independent backtracking DFS ------------------
def feasible_dfs(A):
    if any(len(a) == 0 for a in A): return None
    order = [sorted(A[j]) for j in range(6)]
    seq = [0] * 6
    def rec(j, prev):
        if j == 6:
            return (seq[5] & seq[0]) == 0
        for p in order[j]:
            if (p & prev) == 0:
                seq[j] = p
                if rec(j + 1, p): return True
        return False
    for p in order[0]:
        seq[0] = p
        if rec(1, p): return list(seq)
    return None

# ---------------- direct constraint verification of a witness -------------
def verify_witness(q, W):
    """Full independent check of C1..C5 + cyclic adjacency, at ALL six cells."""
    errs = []
    for P in W:
        if P == 0: errs.append("C1")
        if pc(P) > 2: errs.append("C2")
        for i in range(6):
            if P & ~E[i] == 0: errs.append("C4")
    for j in range(6):
        if W[j] & W[(j + 1) % 6]: errs.append("C3")
    for c in range(6):
        for j in range(6):
            up = dn = 0
            for i in range(6):
                if SIGN[((c + j) - q[i]) % 6] == 1: up |= E[i]
                else:                               dn |= E[i]
            P = W[(c + j) % 6]          # cell c uses A_{(c+j) mod 6} at angle j
            if not (P & (C & ~up)): errs.append(f"C5+ c={c} j={j}")
            if not (P & (C & ~dn)): errs.append(f"C5- c={c} j={j}")
    return errs

print(f"[0] palette candidates after C1,C2,C4: {len(PAL)}")

print("[1] enumeration")
tot = ac = 0
surv_dp = {}; surv_dfs = {}
for tail in itertools.product(range(6), repeat=5):
    q = (0,) + tail
    tot += 1
    if not ac_ok(q): continue
    ac += 1
    A = allowed_lists(q)
    w1 = feasible_dp(A)
    w2 = feasible_dfs(A)
    if (w1 is None) != (w2 is None):
        print(f"  !! METHODS DISAGREE on q={q}: dp={w1 is not None} dfs={w2 is not None}")
        sys.exit(1)
    if w1 is not None: surv_dp[q] = w1
    if w2 is not None: surv_dfs[q] = w2
print(f"      total {tot}, pass AC {ac}, survivors DP {len(surv_dp)}, survivors DFS {len(surv_dfs)}")
assert set(surv_dp) == set(surv_dfs), "DP and DFS survivor sets differ"
S = sorted(surv_dp)
print(f"      survivor sets IDENTICAL between the two methods: {len(S)}")

print("[2] verifying every witness against all constraints at all six cells")
bad = 0
for q in S:
    errs = verify_witness(q, surv_dp[q])
    if errs: bad += 1; print(f"  !! {q}: {errs[:3]}")
print(f"      witnesses failing verification: {bad}")
assert bad == 0

print("[3] spot checks")
print(f"      old count 95 -> new count {len(S)}")
for probe, note in [((0,3,3,3,0,0), "named excluded q"), ((0,0,1,2,3,4), "first omitted q"),
                    ((0,0,1,3,3,4), "old certificate")]:
    here = probe in surv_dp
    print(f"      {probe} ({note}): survivor = {here}"
          + (f"  witness {[sorted(i for i in range(6) if P>>i&1) for P in surv_dp[probe]]}" if here else ""))

print("[4] structural necessary property forced by AC")
ok = True
for q in S:
    cnt = {}
    for i in range(6): cnt[q[i]] = cnt.get(q[i], 0) + 1
    for d, s in cnt.items():
        if s >= 2:
            idx = sorted(i for i in range(6) if q[i] == d)
            U = 0
            for i in idx: U |= E[i]
            if len(idx) == 2 and pc(U) != 3: ok = False
            if len(idx) > 2: ok = False
print(f"      every direction used by <=2 positions, and 2 uses only at adjacent positions: {ok}")
multi = {}
for q in S:
    sig = tuple(sorted((lambda c: [c[k] for k in sorted(c)])({d: sum(1 for x in q if x == d) for d in set(q)}.copy()) , reverse=True))
    multi[sig] = multi.get(sig, 0) + 1
print(f"      direction-multiplicity patterns among survivors: {multi}")

import json
json.dump({"count": len(S), "total": tot, "pass_ac": ac,
           "survivors": [{"q": list(q), "witness": [sorted(i for i in range(6) if P >> i & 1)
                                                     for P in surv_dp[q]]} for q in S]},
          open("certs/ac_survivors_174.json", "w"), indent=1)
print(f"[5] saved certs/ac_survivors_174.json ; elapsed {time.time()-T0:.2f}s")

# ================= [6] dihedral / direction-reflection classification =================
print("[6] dihedral label / direction-reflection classification")

def normalize(q):
    b = q[0]
    return tuple((x - b) % 6 for x in q)

posmaps = [(f"rot{k}", (lambda i, k=k: (i + k) % 6)) for k in range(6)]
posmaps += [(f"ref{k}", (lambda i, k=k: (k - i) % 6)) for k in range(6)]

feas = {}
lists = {}
for tail in itertools.product(range(6), repeat=5):
    q = (0,) + tail
    A = allowed_lists(q)
    lists[q] = A
    feas[q] = ac_ok(q) and (feasible_dp(A) is not None)
print(f"      feasibility table over the full declared space: {sum(feas.values())} feasible of {len(feas)}")

cands = []
for nm, sig in posmaps:
    for eps in (1, -1):
        def phi(q, sig=sig, eps=eps):
            return normalize(tuple((eps * q[sig(i)]) % 6 for i in range(6)))
        cands.append((f"{nm}_eps{eps:+d}", phi))

sym = []
for nm, phi in cands:
    img = [phi(q) for q in feas]
    if len(set(img)) != len(feas) or any(x not in feas for x in img):
        print(f"      {nm}: NOT a bijection of the declared space -- discarded"); continue
    if all(feas[phi(q)] == feas[q] for q in feas):
        sym.append((nm, phi))
    else:
        bad = next(q for q in feas if feas[phi(q)] != feas[q])
        print(f"      {nm}: does NOT preserve feasibility (e.g. {bad}) -- discarded")
print(f"      verified constraint-preserving symmetries: {len(sym)}")
for nm, _ in sym: print(f"        {nm}")

Sset = set(S)
seen = set(); orbits = []
for q in S:
    if q in seen: continue
    orb = set(); frontier = [q]
    while frontier:
        x = frontier.pop()
        if x in orb: continue
        orb.add(x)
        for nm, phi in sym:
            y = phi(x)
            if y in Sset and y not in orb: frontier.append(y)
    seen |= orb
    orbits.append(sorted(orb))
orbits.sort()
print(f"      orbits of the 174 survivors under the verified group: {len(orbits)}")
print(f"      orbit sizes: {sorted((len(o) for o in orbits), reverse=True)}")

def mult_pattern(q):
    c = {}
    for x in q: c[x] = c.get(x, 0) + 1
    return tuple(sorted(c.values(), reverse=True))

print("      minimal (lexicographically least) representative of each orbit:")
for o in sorted(orbits, key=lambda o: o[0]):
    r = o[0]
    w = surv_dp[r]
    print(f"        {r}  pattern {mult_pattern(r)}  size {len(o)}  "
          f"witness {[sorted(i for i in range(6) if P>>i&1) for P in w]}")

pat = {}
for o in orbits:
    k = mult_pattern(o[0])
    pat[k] = pat.get(k, 0) + 1
print(f"      multiplicity-pattern distribution over ORBITS: {pat}")

json.dump({"count": len(S), "orbits": len(orbits),
           "symmetries": [nm for nm, _ in sym],
           "orbit_reps": [{"rep": list(o[0]), "size": len(o),
                           "pattern": list(mult_pattern(o[0])),
                           "members": [list(x) for x in o]} for o in orbits]},
          open("certs/ac_orbits_174.json", "w"), indent=1)
print(f"[7] saved certs/ac_orbits_174.json ; total elapsed {time.time()-T0:.2f}s")

