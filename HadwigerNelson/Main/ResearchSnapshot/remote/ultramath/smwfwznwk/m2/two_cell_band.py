"""Two-cell palette field with a POSITION-DEPENDENT free label, exact transport.

Setting: n = 6m sectors of width Delta = 2*pi/n.  Cell 1 carries the direction
word A (n values), cell 2 the direction word B.  Every value is an admissible
palette for C_6 (size 2 or 3, not contained in a cycle edge {i,i+1 mod 6}).

Constraints imposed (these are exactly the palette-level constraints used in
sprint/k6/Theorem C and in six_sat2.py, separately per cell and across cells):
  (i)   within cell c: word_c(k) & word_c(k + s) = {} for s in S, S = the six
        transport offsets {+-(m-1), +-m, +-(m+1)} mod n;
  (ii)  across cells: A_k & B_{k+s} = {} for s in S  (and symmetrically
        B_k & A_{k+s} = {} which is the same family since S = -S);
  (iii) free label: 0 not in range(A); 5 not in range(B); 0 in range(B)
        (so the two cells have different free labels -- a varying free label).

SAT search with CaDiCaL; the witness is then checked by verify_two_cell.py,
which re-derives every constraint independently (no SAT).
"""
import json
import os
import subprocess
import sys
import tempfile
from itertools import combinations

K = 6
E = [frozenset((j, (j + 1) % K)) for j in range(K)]
VALS = []
for r in (2, 3):
    for c in combinations(range(K), r):
        S = frozenset(c)
        if not any(S <= e for e in E):
            VALS.append(S)
V = len(VALS)


def offsets(m):
    n = 6 * m
    return n, sorted({(m + k) % n for k in (-1, 0, 1)} |
                     {(-m + k) % n for k in (-1, 0, 1)})


def solve(m, timeout=600):
    n, offs = offsets(m)
    nv = 2 * n * V

    def va(i, v):        # cell A
        return i * V + v + 1

    def vb(i, v):        # cell B
        return n * V + i * V + v + 1

    def var(f, i, v):
        return va(i, v) if f == 0 else vb(i, v)

    cl = []
    for i in range(n):
        for v in range(V):
            if 0 in VALS[v]:
                cl.append([-va(i, v)])          # (iii) A avoids 0
            if 5 in VALS[v]:
                cl.append([-vb(i, v)])          # (iii) B avoids 5
    for f in (0, 1):
        for i in range(n):
            cl.append([var(f, i, v) for v in range(V)])
            for a, b in combinations(range(V), 2):
                cl.append([-var(f, i, a), -var(f, i, b)])
    for i in range(n):
        for s in offs:
            j = (i + s) % n
            if i == j:
                continue
            for f in (0, 1):                     # (i) within a cell
                for a in range(V):
                    for b in range(V):
                        if VALS[a] & VALS[b]:
                            cl.append([-var(f, i, a), -var(f, j, b)])
            for a in range(V):                   # (ii) across the cells
                for b in range(V):
                    if VALS[a] & VALS[b]:
                        cl.append([-va(i, a), -vb(j, b)])
    cl.append([vb(i, v) for i in range(n) for v in range(V) if 0 in VALS[v]])
    with tempfile.NamedTemporaryFile('w', suffix='.cnf', delete=False) as f:
        f.write(f"p cnf {nv} {len(cl)}\n")
        for c in cl:
            f.write(" ".join(map(str, c)) + " 0\n")
        path = f.name
    try:
        r = subprocess.run(['/opt/lean/bin/cadical', '-q', path],
                           capture_output=True, text=True, timeout=timeout)
        out = r.stdout
        if 's SATISFIABLE' not in out:
            return None, len(cl), (out.strip().splitlines() or ['no output'])[-1]
        lits = set()
        for line in out.splitlines():
            if line.startswith('v '):
                lits |= {int(x) for x in line.split()[1:]}
        A, B = [], []
        for i in range(n):
            for v in range(V):
                if va(i, v) in lits:
                    A.append(sorted(VALS[v]))
                if vb(i, v) in lits:
                    B.append(sorted(VALS[v]))
        return (A, B), len(cl), 'SAT'
    finally:
        os.unlink(path)


if __name__ == "__main__":
    res = {}
    for m in (6, 9, 12):
        w, ncl, st = solve(m)
        print(f"m={m} n={6*m} clauses={ncl}: {st}")
        if w:
            A, B = w
            print("  A:", A[:12], "..." if len(A) > 12 else "")
            print("  B:", B[:12], "..." if len(B) > 12 else "")
            print("  free labels: cell1", sorted(set(range(6)) - {i for s in A for i in s}),
                  " cell2", sorted(set(range(6)) - {i for s in B for i in s}))
            res[m] = {"A": A, "B": B}
        else:
            res[m] = None
        sys.stdout.flush()
    with open('two_cell_witness.json', 'w') as f:
        json.dump(res, f)
    print("written two_cell_witness.json")
