"""Step A (no solver calls): build the baseline survivor set from ALL previously saved
separating witnesses -- the 8 ensembled partitions, the (0,39) witness and the (0,50)
witness -- then rank survivors deterministically and pre-register the top 8."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from udg.exact import Field
from udg.heule import load, load_edges

F = Field([3, 5, 11]); pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts); adj = [set() for _ in range(n)]
for a, b in es: adj[a].add(b); adj[b].add(a)
E = [(a, b) for a, b in es]

def same_pairs(c):
    byc = {}
    for v, x in enumerate(c): byc.setdefault(x, []).append(v)
    S = set()
    for grp in byc.values():
        for a in range(len(grp)):
            for b in range(a+1, len(grp)):
                i, j = grp[a], grp[b]
                if j not in adj[i]: S.add((i, j))
    return S

def check(c):
    return sum(1 for u, v in E if c[u] == c[v])

ens = json.load(open(os.path.join(HERE, "certs/ensemble_k5.json")))
dis = json.load(open(os.path.join(HERE, "certs/experiment_diseq.json")))
W = [w["canonical"] for w in ens["witnesses"]]          # 8 partitions
W.append(ens["tested_witness"])                          # separates (0,50)
W.append(dis["colouring_Gpq"])                           # separates (0,39)
labels = [f"ensemble_{i}" for i in range(8)] + ["witness_(0,50)", "witness_(0,39)"]
print("saved witnesses reused:", len(W))
for lab, c in zip(labels, W):
    assert check(c) == 0, f"{lab} invalid"
    print(f"  {lab}: verified 0 monochromatic of {len(E)} edges, same-colour nonedges {len(same_pairs(c))}")

S = same_pairs(W[0])
for c in W[1:]: S &= same_pairs(c)
print(f"\nbaseline survivors: {len(S)}  (from 8-partition set 30395, plus the two extra witnesses)")
print(f"(0,39) in baseline:", (0, 39) in S, " (0,50) in baseline:", (0, 50) in S)

ranked = sorted(S, key=lambda p: (-len(adj[p[0]] & adj[p[1]]), p[0], p[1]))
sel = ranked[:8]

def sd(i, j):
    dx = F.sub(pts[i][0], pts[j][0]); dy = F.sub(pts[i][1], pts[j][1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))
rows = []
for t, (i, j) in enumerate(sel, 1):
    d2 = sd(i, j)
    rows.append({"t": t, "i": i, "j": j, "common": len(adj[i] & adj[j]),
                 "d2": [str(x) for x in d2], "d2_is_1": F.is_zero(F.sub(d2, F.one))})
    print(f"  #{t}: ({i},{j}) common-nb={len(adj[i] & adj[j])} d^2 coeffs={[str(x) for x in d2 if x]}")
json.dump({"baseline_survivors": len(S), "selected": rows,
           "rank_rule": "decreasing |N(i) cap N(j)|, then increasing i, then increasing j",
           "n_witnesses_used": len(W)},
          open(os.path.join(HERE, "certs/prereg_chase_pairs.json"), "w"), indent=1)
print("\nwrote certs/prereg_chase_pairs.json")
