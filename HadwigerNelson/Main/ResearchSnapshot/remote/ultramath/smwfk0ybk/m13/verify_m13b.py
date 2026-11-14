"""m13 verifier.  Independent decision procedures for the k=6 interface CSP and the
agreement checks behind the sliver-profile report.

CHECK 0  m5's sliver formula == the paper's set definition (labels left after deleting
         endpoints of positive edges), i.e. m5's encoding of (C2) is m2 Lemma 1.1.
CHECK 1  rotation symmetry: sat(l,c) = sat(l,c+s) for every shift s (so 6^l vs 6^(l-1)).
CHECK 2  agreement of my recursive DFS with m5's bitmask DP on EVERY (l, geometry), k=6.
CHECK 3  the two-outsider theorem, verified instance by instance for l = 3,4: the
         alternating singleton model satisfies (C1)-(C5).
CHECK 4  KEY: every C1-C3 satisfiable instance has a model with ALL palettes of size <= 2
         (found by a reachability DP, a different algorithm from my DFS).  Such a model
         automatically satisfies (C4) and (C5), so the tightened (C1)-(C5) decision equals
         the C1-C3 decision, instance by instance.
CHECK 5  the same statement by the recursive DFS (second algorithm) + a no-pruning
         product enumeration on a random sample of instances.
"""
from itertools import product, combinations
import sys, random

sys.path.insert(0, "../../smwfhd5sl/m5")
import interface_csp as m5
from profile2 import first_model, sign_word, slivers

K = 6

def paper_slivers(ell, k, c):
    U = set(range(ell, k)); T = set(range(ell))
    rows = m5.sign_matrix(ell, c)
    out = []
    for i in range(6):
        row = rows[i]
        pos = set(); neg = set()
        for j in range(ell):                       # edge j joins labels j and j+1
            s = pos if row[j] == 1 else neg
            s.add(j); s.add((j + 1) % ell)
        out.append(((T - pos) | U, (T - neg) | U))
    return out

def admissible(ell, k, O, I, maxsize):
    return [frozenset(s) for r in range(1, maxsize + 1) for s in combinations(range(k), r)
            if set(s) & O and set(s) & I]

def sat_small_DP(ell, k, c, maxsize):
    """m5-style forward reachability DP restricted to palettes of size <= maxsize."""
    adm = [admissible(ell, k, O, I, maxsize) for (O, I) in slivers(ell, k, sign_word(ell, c))]
    if any(not a for a in adm):
        return False
    pos = {p: n for n, p in enumerate(adm[0])}
    reach = {p: 1 << n for p, n in pos.items()}
    for i in range(1, 6):
        nxt = {}
        for q in adm[i]:
            acc = 0
            for p, v in reach.items():
                if not (p & q):
                    acc |= v
            if acc:
                nxt[q] = acc
        reach = nxt
        if not reach:
            return False
    for q, v in reach.items():
        for p, n in pos.items():
            if not (p & q) and (v >> n) & 1:
                return True
    return False

def sat_small_DFS(ell, k, c, maxsize):
    sl = slivers(ell, k, sign_word(ell, c))
    adm = [admissible(ell, k, O, I, maxsize) for (O, I) in sl]
    if any(not a for a in adm):
        return False
    cur = []
    def rec(i):
        if i == 6:
            return not (cur[5] & cur[0])
        for q in adm[i]:
            if i and (q & cur[i - 1]):
                continue
            cur.append(q)
            if rec(i + 1):
                return True
            cur.pop()
        return False
    return rec(0)

def enumerate_small(ell, k, c, maxsize, limit=1):
    """No pruning: full product over admissible palettes, filtered at the end."""
    sl = slivers(ell, k, sign_word(ell, c))
    adm = [admissible(ell, k, O, I, maxsize) for (O, I) in sl]
    if any(not a for a in adm):
        return []
    full = frozenset(range(k))
    out = []
    for tup in product(*adm):
        if any(tup[i] & tup[(i + 1) % 6] for i in range(6)):
            continue
        if any((tup[a] | tup[b]) == full for a in range(6) for b in range(a + 1, 6)):
            continue
        if sum(1 for p in tup if len(p) == 3) > 3:
            continue
        out.append(tup)
        if len(out) >= limit:
            break
    return out

def main():
    log = []
    def say(s):
        print(s, flush=True); log.append(s)

    # CHECK 0
    from profile2 import slivers as f2
    bad = sum(1 for ell in range(3, K + 1) for c in product(range(6), repeat=ell)
              if tuple(map(lambda t: (frozenset(t[0]), frozenset(t[1])),
                           paper_slivers(ell, K, c))) !=
                 tuple((O, I) for (O, I) in f2(ell, K, sign_word(ell, c))))
    say(f"CHECK 0  paper definition of O,I vs m5/m2 formula: mismatches over all instances = {bad}")

    # CHECK 1
    rot_bad = 0
    for ell in range(3, K + 1):
        base = {c: m5.sat_geometry(ell, K, c) for c in product(range(6), repeat=ell)}
        for c, v in base.items():
            for s in range(1, 6):
                if base[tuple((x + s) % 6 for x in c)] != v:
                    rot_bad += 1
    say(f"CHECK 1  rotation invariance of the C1-C3 decision: violations = {rot_bad}")

    # CHECK 2 and CHECK 4
    tot = {ell: [0, 0] for ell in range(3, K + 1)}
    dis = 0; n = 0
    for ell in range(3, K + 1):
        for c in product(range(6), repeat=ell):
            n += 1
            a = m5.sat_geometry(ell, K, c)              # m5 bitmask DP, sizes <= k-3
            b = first_model(ell, K, c, False) is not None   # my DFS, sizes <= k-3
            d = sat_small_DP(ell, K, c, 2)              # DP, sizes <= 2 only
            if a != b or a != d:
                dis += 1
            tot[ell][0] += a; tot[ell][1] += d
    say(f"CHECK 2  instances compared = {n}; disagreements (m5 DP vs my DFS vs size<=2 DP) = {dis}")
    for ell in range(3, K + 1):
        say(f"CHECK 4  l={ell}: C1-C3 SAT = {tot[ell][0]}/{6**ell}; "
            f"models with all |P_i| <= 2 = {tot[ell][1]}/{6**ell}")

    # CHECK 3
    th_bad = 0
    for ell in (3, 4):
        for c in product(range(6), repeat=ell):
            P = [frozenset([ell]) if i % 2 == 0 else frozenset([ell + 1]) for i in range(6)]
            sl = slivers(ell, K, sign_word(ell, c))
            sl = [(frozenset(O), frozenset(I)) for (O, I) in sl]
            ok = all(1 <= len(P[i]) <= K - 3 and (P[i] & sl[i][0]) and (P[i] & sl[i][1])
                     for i in range(6))
            ok &= all(not (P[i] & P[(i + 1) % 6]) for i in range(6))
            ok &= not any((P[a] | P[b]) == frozenset(range(K))
                          for a in range(6) for b in range(a + 1, 6))
            ok &= sum(1 for p in P if len(p) == 3) <= 3
            if not ok:
                th_bad += 1
    say(f"CHECK 3  two-outsider alternating singleton model, l=3,4, all geometries: failures = {th_bad}")

    # CHECK 5: DFS with maxsize 2 on every instance + no-pruning product on a sample
    d2 = {ell: 0 for ell in range(3, K + 1)}
    for ell in range(3, K + 1):
        for c in product(range(6), repeat=ell):
            if sat_small_DFS(ell, K, c, 2):
                d2[ell] += 1
    agree = all(d2[ell] == tot[ell][1] for ell in range(3, K + 1))
    say(f"CHECK 5  DFS(size<=2) counts {[d2[e] for e in range(3, K+1)]} agree with DP: {agree}")

    random.seed(7)
    sample = []
    for ell in range(3, K + 1):
        inst = [c for c in product(range(6), repeat=ell) if sat_small_DP(ell, K, c, 2)]
        sample += [(ell, random.choice(inst)) for _ in range(30)]
    sbad = 0
    for ell, c in sample:
        if not enumerate_small(ell, K, c, 2, limit=1):
            sbad += 1
    say(f"CHECK 5  no-pruning product enumeration on {len(sample)} random satisfiable "
        f"instances: failures = {sbad}")

    open("verify_m13.log", "w").write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
