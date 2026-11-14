"""Independent verification of the zero-survivor certificate. Data only, no solver.
Reads the raw .edge file and the saved witnesses; recomputes everything from scratch."""
import json, sys
from itertools import combinations
E = [(int(a[1])-1, int(a[2])-1) for a in ([l.split() for l in open('refs/heule_553.edge') if l.strip()][1:])]
N = 553
adj = [set() for _ in range(N)]
for u, v in E: adj[u].add(v); adj[v].add(u)
d = json.load(open('certs/adaptive_k5.json'))
W = d["witnesses"]
print("witnesses in certificate:", len(W))
# 1. every witness is a proper 5-colouring, checked straight against the .edge list
bad = 0
for t, c in enumerate(W):
    assert len(c) == N
    m = sum(1 for u, v in E if c[u] == c[v])
    if m: print("  witness", t, "has", m, "monochromatic edges"); bad += 1
    assert set(c) == {0,1,2,3,4}
print("  all proper 5-colourings (0 monochromatic of %d edges): %s" % (len(E), bad == 0))
# 2. recompute the survivor intersection from scratch
S = None
for c in W:
    same = set()
    for u, v in combinations(range(N), 2):
        if c[u] == c[v] and v not in adj[u]: same.add((u, v))
    S = same if S is None else (S & same)
print("  survivors recomputed:", len(S))
# 3. direct check: every non-adjacent pair is separated by at least one witness
unsep = []
for u, v in combinations(range(N), 2):
    if v in adj[u]: continue
    if all(c[u] == c[v] for c in W): unsep.append((u, v))
print("  non-adjacent pairs with NO separating witness:", len(unsep), unsep[:5])
print("  non-adjacent pairs total:", sum(1 for u,v in combinations(range(N),2) if v not in adj[u]))
print("\nCERTIFICATE HOLDS:", len(S) == 0 and not bad and not unsep)
