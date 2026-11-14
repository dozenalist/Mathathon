"""analyse_patch.py R model -- summary of a verified patch model."""
import sys
from itertools import combinations
K = 6; I = 5
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
R = int(sys.argv[1]); model = read_model(sys.argv[2]); pts = ball(R); N = len(pts)
def z(n, k, l): return (n * 6 + k) * 6 + l + 1
def col(n): return N * 36 + n * 6 + 1
P = {(n, k): frozenset(l for l in range(K) if model.get(z(n, k, l), False)) for n in range(N) for k in range(6)}
C = {n: next((l for l in range(K) if model.get(col(n) + l, False)), None) for n in range(N)}
print(f"R={R}: {N} nodes;  centre colour {C[0]}")
print("centre palettes:", [''.join(map(str, sorted(P[(0, k)]))) for k in range(6)])
tern = sum(1 for n in range(N) for k in range(6) if len(P[(n, k)]) == 3)
sing = sum(1 for n in range(N) for k in range(6) if len(P[(n, k)]) == 1)
print(f"ternary positions: {tern} of {6*N};  singletons: {sing}")
vals = set(P[(n, k)] for n in range(N) for k in range(6))
print(f"distinct palette values used: {len(vals)}")
print("  ", ['{' + ','.join(map(str, sorted(v))) + '}' for v in sorted(vals, key=lambda s: (len(s), sorted(s)))])
print("node colours:", [C[n] for n in range(N)])
# is the field 2-valued?  (3,2) residue?
print("2-valued field?", len(vals) == 2)
