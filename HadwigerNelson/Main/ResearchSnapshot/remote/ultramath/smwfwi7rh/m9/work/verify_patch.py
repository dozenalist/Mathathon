"""verify_patch.py R  -- decode a cadical model for s3_patch.py R and check EVERY
constraint of the paper's palette calculus directly (independent of the CNF encoding).
Also checks the induced sub-configuration on every smaller ball, which must also be
admissible (monotonicity).  Prints violations with names.
"""
import sys
from itertools import combinations

K = 6
I = 5
ELL = 5

def ball(R):
    out = [(0, 0)]
    for i in range(-R, R + 1):
        for j in range(-R, R + 1):
            if (i, j) != (0, 0) and abs(i) <= R and abs(j) <= R and abs(i + j) <= R:
                out.append((i, j))
    return out

DIRS = {(1, 0): 0, (1, -1): 5, (0, -1): 4, (-1, 0): 3, (-1, 1): 2, (0, 1): 1}

def read_model(path):
    vals = {}
    for line in open(path):
        if line.startswith('v'):
            for tok in line[1:].split():
                x = int(tok)
                if x == 0: continue
                vals[abs(x)] = x > 0
    return vals

def check(R, pts, model, unitchk=True, colourchk=True, verbose=True, N0=None):
    # N0 = number of points in the encoded instance (node 0 is its centre)
    if N0 is None: N0 = len(pts)
    big = ball(R) if N0 != len(pts) else pts
    bigidx = {p: n for n, p in enumerate(big)}
    idx = {p: bigidx[p] for p in pts}
    def z(n, k, l): return (n * 6 + k) * 6 + l + 1
    def col(n): return N0 * 36 + n * 6 + 1
    N = N0
    P = {(n, k): frozenset(l for l in range(K) if model.get(z(n, k, l), False)) for n in range(N) for k in range(6)}
    C = {n: next((l for l in range(K) if model.get(col(n) + l, False)), None) for n in range(N)}
    bad = []
    def bad_add(msg): bad.append(msg)
    for n in range(N):
        for k in range(6):
            Pk = P[(n, k)]
            if not (1 <= len(Pk) <= 3): bad_add(f"size at node {n} dir {k}: {sorted(Pk)}")
            if n == 0 and I in Pk: bad_add(f"centre palette contains i at k={k}")
            if Pk & P[(n, (k + 1) % 6)]: bad_add(f"(5.7) at node {n} k={k}")
            Q = P[(n, (k + 2) % 6)]
            if len(Pk) + len(Q) == 5 and not (Pk & Q): bad_add(f"MON at node {n} k={k}")
        for k1 in range(6):
            for k2 in range(k1 + 1, 6):
                a, b = P[(n, k1)], P[(n, k2)]
                if len(a) == 3 and len(b) == 3 and not (a & b): bad_add(f"C1 at node {n} {k1},{k2}")
    # centre: not inside an edge of C5, no singleton, Lemma A
    for k in range(6):
        Pk = P[(0, k)]
        for e in [(j, (j + 1) % ELL) for j in range(ELL)]:
            if Pk <= frozenset(e): bad_add(f"centre palette inside edge {e} at k={k}")
        if len(Pk) < 2: bad_add(f"centre singleton at k={k}")
        if len(Pk) == 3:
            want = frozenset(range(K)) - Pk - {I}
            if P[(0, (k + 1) % 6)] != want: bad_add(f"Lemma A at k={k}: {sorted(Pk)} -> {sorted(P[(0,(k+1)%6)])} want {sorted(want)}")
    # (UNIT)
    if unitchk:
        for (p, n) in idx.items():
            for (d, di) in DIRS.items():
                q = (p[0] + d[0], p[1] + d[1])
                if q not in idx: continue
                m = idx[q]
                for k in range(6):
                    if k in (di, (di + 3) % 6): continue
                    if P[(n, k)] & P[(m, k)]: bad_add(f"(UNIT) pair {p}-{q} dir {k}")
    if colourchk:
        for n in range(N):
            if C[n] is None: bad_add(f"no colour at node {n}")
            else:
                for k in range(6):
                    if C[n] in P[(n, k)]: bad_add(f"self-avoidance node {n}")
        for (p, n) in idx.items():
            for (d, di) in DIRS.items():
                q = (p[0] + d[0], p[1] + d[1])
                if q not in idx: continue
                m = idx[q]
                if C[n] is not None and C[n] == C[m]: bad_add(f"same colour on unit pair {p}-{q}")
        for (d, di) in DIRS.items():
            if d in idx:
                m = idx[d]
                if C[m] is not None and C[m] not in P[(0, di)]: bad_add(f"trace: colour of {d} not in P_x(dir {di})")
    return bad, P, C

if __name__ == "__main__":
    R = int(sys.argv[1]); mp = sys.argv[2]
    model = read_model(mp)
    pts = ball(R)
    bad, P, C = check(R, pts, model, N0=len(pts))
    print(f"R={R}: {len(bad)} violation(s) on the full ball")
    for b in bad[:20]: print("   ", b)
    # monotonicity: every smaller ball must also be admissible
    for r in range(1, R + 1):
        sub = ball(r)
        bad2, _, _ = check(R, sub, model, N0=len(pts))
        print(f"  sub-ball r={r}: {len(bad2)} violation(s)")
        for b in bad2[:6]: print("     ", b)
