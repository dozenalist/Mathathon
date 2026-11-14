"""Independent check of the coordinator's pairs-only SAT claim (handoff, 'NEW').

Domain: the six admissible PAIR values of C6 that avoid label 0,
  {1,3},{1,4},{1,5},{2,4},{2,5},{3,5}.
Constraint: on the cyclic word of length n = 6m, the values at the six transport offsets
+-（m-1), +-m, +-(m+1) mod n are disjoint at every sector.

Encoding written from scratch here (different variable order and clause generation from
sprint/k6/six_sat2.py), solved by CaDiCaL, then the model is decoded and re-checked.

usage: python3 pairs_only.py [m ...]
"""
import subprocess, sys, tempfile, os
from itertools import combinations

VALS = [frozenset(c) for c in combinations(range(1, 6), 2)
        if not any(frozenset(c) <= frozenset(e) for e in
                   [frozenset((j, (j + 1) % 6)) for j in range(6)])]
VALS.sort(key=lambda s: sorted(s))
V = len(VALS)


def solve(m, timeout=600):
    n = 6 * m
    offs = sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})
    assert len(offs) == 6, offs
    # x[i][v] : sector i carries VALS[v]
    def x(i, v):
        return i * V + v + 1
    clauses = []
    for i in range(n):
        clauses.append([x(i, v) for v in range(V)])          # at least one
        for a, b in combinations(range(V), 2):               # at most one
            clauses.append([-x(i, a), -x(i, b)])
    for o in offs:
        for i in range(n):
            j = (i + o) % n
            for a in range(V):
                for b in range(V):
                    if VALS[a] & VALS[b]:
                        clauses.append([-x(i, a), -x(j, b)])
    with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
        f.write("p cnf %d %d\n" % (n * V, len(clauses)))
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
        path = f.name
    try:
        r = subprocess.run(["/opt/lean/bin/cadical", "-q", path],
                           capture_output=True, text=True, timeout=timeout)
        out = r.stdout
        status = "SAT" if "s SATISFIABLE" in out else "UNSAT" if "s UNSATISFIABLE" in out else "?"
        if status != "SAT":
            return status, None, len(clauses), offs
        lits = set()
        for line in out.splitlines():
            if line.startswith("v "):
                lits |= {int(t) for t in line.split()[1:] if t != "0"}
        word = [None] * n
        for i in range(n):
            for v in range(V):
                if x(i, v) in lits:
                    word[i] = VALS[v]
                    break
            assert word[i] is not None
        return status, word, len(clauses), offs
    finally:
        os.unlink(path)


def check(word, m, offs):
    n = 6 * m
    assert len(word) == n
    for i in range(n):
        assert 1 <= len(word[i]) <= 3
        assert 0 not in word[i]
        assert not any(word[i] <= frozenset(e) for e in
                       [frozenset((j, (j + 1) % 6)) for j in range(6)])
        for o in offs:
            assert not (word[i] & word[(i + o) % n]), (i, o)
    return True


if __name__ == "__main__":
    ms = [int(a) for a in sys.argv[1:]] or [6, 9, 12, 15, 18]
    print("domain:", [sorted(v) for v in VALS], " |V| =", V)
    for m in ms:
        st, word, nc, offs = solve(m)
        print(f"m={m:3d} n={6*m:4d} clauses={nc:7d} offsets={offs}: {st}")
        if st == "SAT":
            print("      word[0:12] =", [sorted(v) for v in word[:12]])
            print("      constraint re-check on the decoded model:", check(word, m, offs))
            print("      distinct values:", sorted({tuple(sorted(v)) for v in word}))
