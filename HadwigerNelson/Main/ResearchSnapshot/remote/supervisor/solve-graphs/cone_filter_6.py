"""CONDITIONAL cone filter on the audited 174 + complete witness enumeration for the survivors.

CONE FILTER (conditional, NOT proved - referee pending): for every cyclic adjacent direction pair
{d,(d+1) mod 6}, the union of E_i over the positions with q_i in that pair must cover <= 3 labels.

Also enumerates ALL cyclic witnesses (C1..C5 + cyclic adjacency, |P_j|<=2) for each surviving q,
to decide FORCES vs ADMITS a three-disjoint-pair word.
Integer/bitmask arithmetic. One process, one thread.
"""
import sys, time, itertools, json
T0 = time.time()
C = (1 << 6) - 1
E = [(1 << i) | (1 << ((i + 1) % 6)) for i in range(6)]
SIGN = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}
pc = lambda x: bin(x).count("1")
name = lambda P: sorted(i for i in range(6) if P >> i & 1)

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

def cone_ok(q):
    for d in range(6):
        grp = {d, (d + 1) % 6}
        U = 0
        for i in range(6):
            if q[i] in grp: U |= E[i]
        if pc(U) >= 4: return False
    return True

def feasible_dp(A):
    if any(len(a) == 0 for a in A): return None
    for p0 in A[0]:
        reach = [set() for _ in range(6)]; pred = [dict() for _ in range(6)]
        reach[0] = {p0}
        for j in range(1, 6):
            cur = {}
            for p in A[j]:
                for r in reach[j - 1]:
                    if (p & r) == 0: cur[p] = r; break
            reach[j] = set(cur); pred[j] = cur
            if not reach[j]: break
        if not reach[5]: continue
        for p5 in reach[5]:
            if (p5 & p0) == 0:
                seq = [None] * 6; seq[5] = p5; c = p5
                for j in range(5, 0, -1): c = pred[j][c]; seq[j - 1] = c
                if seq[0] == p0: return seq
    return None

def all_witnesses(A):
    """Complete enumeration of cyclic witnesses (P_0..P_5)."""
    out = []
    seq = [0] * 6
    def rec(j, prev):
        if j == 6:
            if (seq[5] & seq[0]) == 0: out.append(tuple(seq))
            return
        for p in sorted(A[j]):
            if (p & prev) == 0:
                seq[j] = p; rec(j + 1, p)
    for p0 in sorted(A[0]):
        seq[0] = p0; rec(1, p0)
    return out

def is_three_disjoint_pair_word(w):
    """True iff the distinct palettes in w are three pairwise-disjoint 2-sets (a partition of C)."""
    D = list(set(w))
    if len(D) != 3: return False
    if any(pc(P) != 2 for P in D): return False
    u = 0
    for P in D:
        if u & P: return False
        u |= P
    return u == C

print("=" * 78); print("CONDITIONAL CONE FILTER AND COMPLETE WITNESS ENUMERATION"); print("=" * 78)

# ---- stage 1: rebuild the 174, then apply the cone filter ----
feas = {}; lists = {}
for tail in itertools.product(range(6), repeat=5):
    q = (0,) + tail
    A = allowed_lists(q); lists[q] = A
    feas[q] = ac_ok(q) and (feasible_dp(A) is not None)
S174 = [q for q in feas if feas[q]]
print(f"[1] audited base: {len(S174)} AC-survivors of 7776  (matches the corrected count 174: {len(S174)==174})")

cone = [q for q in S174 if cone_ok(q)]
print(f"[1] after the CONDITIONAL cone filter: {len(cone)} survivors")
print(f"    {sorted(cone)}")
parent = [[0,0,2,2,4,4],[0,0,4,4,2,2],[0,1,2,3,4,5],[0,2,2,4,4,0],[0,4,4,2,2,0],[0,5,4,3,2,1]]
pset = {tuple(x) for x in parent}
print(f"[1] agree with the parent's list of six: {set(cone) == pset}")
print(f"    cone filter applied to ALL 7776: {sum(1 for q in feas if cone_ok(q))} (same set: "
      f"{set(q for q in feas if cone_ok(q)) == pset})")

# ---- stage 2: classify the six under the 24 certified symmetries ----
def normalize(q):
    b = q[0]; return tuple((x - b) % 6 for x in q)
posmaps = [(f"rot{k}", (lambda i, k=k: (i + k) % 6)) for k in range(6)]
posmaps += [(f"ref{k}", (lambda i, k=k: (k - i) % 6)) for k in range(6)]
sym = []
for nm, sig in posmaps:
    for eps in (1, -1):
        phi = (lambda q, sig=sig, eps=eps: normalize(tuple((eps * q[sig(i)]) % 6 for i in range(6))))
        if all(cone_ok(phi(q)) == cone_ok(q) and feas[phi(q)] == feas[q] for q in feas):
            sym.append((nm, eps, phi))
print(f"\n[2] symmetries that preserve the CONE-FILTERED feasibility table: {len(sym)}")
S6 = set(cone); seen = set(); orbits = []
for q in sorted(S6):
    if q in seen: continue
    orb = set(); fr = [q]
    while fr:
        x = fr.pop()
        if x in orb: continue
        orb.add(x)
        for nm, eps, phi in sym:
            y = phi(x)
            if y in S6 and y not in orb: fr.append(y)
    seen |= orb; orbits.append(sorted(orb))
orbits.sort()
print(f"    the six form {len(orbits)} orbits under the certified symmetries")
for o in orbits:
    print(f"      orbit size {len(o)}: {o}")

# ---- stage 3: complete witness enumeration ----
print("\n[3] COMPLETE cycle-witness enumeration for each of the six")
report = []
for q in sorted(S6):
    W = all_witnesses(lists[q])
    pal_used = sorted({tuple(name(P)) for w in W for P in w})
    tdp = [w for w in W if is_three_disjoint_pair_word(w)]
    print(f"\n    q={q}   witnesses: {len(W)}")
    print(f"      distinct palettes over ALL witnesses: {pal_used}")
    print(f"      three-disjoint-pair words: {len(tdp)} of {len(W)}"
          f"   -> {'FORCES' if len(tdp)==len(W) else ('ADMITS' if tdp else 'NEITHER')}")
    for w in W[:6]:
        print(f"        {[name(P) for P in w]}")
    if len(W) > 6: print(f"        ... ({len(W)-6} more)")
    report.append({"q": list(q), "n_witnesses": len(W),
                   "palettes_used": pal_used, "n_three_disjoint_pair_words": len(tdp),
                   "verdict": "FORCES" if len(tdp) == len(W) else ("ADMITS" if tdp else "NEITHER"),
                   "witnesses": [[name(P) for P in w] for w in W]})

# ---- stage 4: explicit full-circle step palettes ----
print("\n[4] explicit full-circle step palettes (one per q, from a chosen witness W)")
for r in report:
    q = tuple(r["q"]); W = [sum(1 << i for i in P) for P in r["witnesses"][0]]
    print(f"    q={q}: base-direction step palette by open sign cell c=0..5: "
          f"{[name(W[c]) for c in range(6)]}")
    print(f"        angle j in cell c uses W[(c+j) mod 6]; boundary t = (2k+1)pi/6 carries NO palette (null)")

json.dump({"cone_survivors": [list(q) for q in sorted(S6)],
           "cone_orbits": [[list(q) for q in o] for o in orbits],
           "n_symmetries_preserving_cone": len(sym),
           "per_q": report},
          open("certs/cone_six.json", "w"), indent=1)
print(f"\n[done] saved certs/cone_six.json ; {time.time()-T0:.2f}s")
