"""Direct DFS decision procedure for the six-cycle free-label sector word.

No SAT solver: complete backtracking search over the palette alphabet with
forward checking, on the sector cycle Z_{6m}.

The pair-only alphabet has a useful exact structure, verified here:
    P = {13,14,15,24,25,35} (admissible pairs avoiding label 0)
    disjointness on P is exactly adjacency in the graph
        15 -- 24 -- 13 -- 25 -- 14 -- 35 -- 24      (a 5-cycle 24-13-25-14-35-24
                                                     with a pendant vertex 15 on 24)
so a pair-only word is a graph homomorphism Z_{6m}(+-(m-1),+-m,+-(m+1)) -> G_P.
"""
from itertools import combinations
import sys
sys.setrecursionlimit(10000)

K = 6
EDGES = [frozenset((j, (j + 1) % 6)) for j in range(6)]


def admissible(S):
    S = frozenset(S)
    return 1 <= len(S) <= 3 and not any(S <= e for e in EDGES)


def domain(pairs_only=True, avoid0=True):
    out = []
    for r in (2, 3):
        for c in combinations(range(K), r):
            S = frozenset(c)
            if avoid0 and 0 in S:
                continue
            if admissible(S):
                out.append(S)
    return [v for v in out if len(v) == 2] if pairs_only else out


def offsets(m):
    n = 6 * m
    return sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})


def solve(m, vals, want_all=False, cap=None):
    """Complete DFS. Returns (status, first solution or None, count)."""
    n = 6 * m
    offs = offsets(m)
    nb = {i: sorted({(i + j) % n for j in offs} - {i}) for i in range(n)}
    V = len(vals)
    dom = [[v for v in range(V) if not (vals[v] & vals[u])] for u in range(V)]
    comp = [[w for w in range(V) if not (vals[v] & vals[w])] for v in range(V)]
    assign = [-1] * n
    avail = [set(range(V)) for _ in range(n)]
    sols = []
    nodes = [0]

    def propagate(i, v):
        """remove inconsistencies after assign[i]=v; return list of (j, removed) to undo."""
        undo = []
        for j in nb[i]:
            if assign[j] == -1:
                allowed = set(comp[v])
                rem = avail[j] - allowed
                if rem:
                    if not (allowed & avail[j]):
                        for (jj, rr) in undo:
                            avail[jj] |= rr
                        return None
                    avail[j] -= rem
                    undo.append((j, rem))
        return undo

    def dfs(i):
        nodes[0] += 1
        if cap is not None and nodes[0] > cap:
            raise TimeoutError
        if i == n:
            # close the cycle
            for j in range(n):
                for o in offs:
                    q = (j + o) % n
                    if vals[assign[j]] & vals[assign[q]]:
                        return
            sols.append(list(assign))
            if not want_all:
                raise StopIteration
            return
        for v in sorted(avail[i]):
            assign[i] = v
            undo = propagate(i, v)
            if undo is not None:
                dfs(i + 1)
                for (j, rem) in undo:
                    avail[j] |= rem
            assign[i] = -1
            if sols and not want_all:
                return

    try:
        dfs(0)
    except StopIteration:
        pass
    except TimeoutError:
        return ("timeout", None, 0)
    return ("SAT" if sols else "UNSAT", sols[0], len(sols))


if __name__ == "__main__":
    pairs = domain(True)
    print("pair alphabet:", [sorted(v) for v in pairs])
    # disjointness graph on the pair alphabet
    print("disjointness adjacency:")
    for v in pairs:
        print("   ", sorted(v), "->", [sorted(w) for w in pairs if not (v & w)])
    print()
    whole = domain(False)
    for m in [int(a) for a in sys.argv[1:]] or [6, 9, 12]:
        st, sol, cnt = solve(m, pairs, want_all=False)
        print(f"pairs-only  m={m} n={6*m}: {st}", "".join(
            "[%s]" % ",".join(map(str, sorted(pairs[v]))) for v in sol) if sol else "")
        st2, sol2, cnt2 = solve(m, whole, want_all=False)
        print(f"pairs+tripl m={m} n={6*m}: {st2}", "".join(
            "[%s]" % ",".join(map(str, sorted(whole[v]))) for v in sol2) if sol2 else "")
