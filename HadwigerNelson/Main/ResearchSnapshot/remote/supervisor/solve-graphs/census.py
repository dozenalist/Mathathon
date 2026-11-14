"""The single registered computation of the block (see PREREGISTRATION-census.md).
One process, hard 60 s cap, no variants.
"""
import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time()
CAP = 55.0
from udg.exact import Field
from udg.heule import load, load_edges

F = Field([3, 5, 11])
pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts)
adj = [set() for _ in range(n)]
for a, b in es:
    adj[a].add(b); adj[b].add(a)
print(f"[load] n={n} m={len(es)}  t={time.time()-T0:.2f}s")

def sqd(i, j):
    dx = F.sub(pts[i][0], pts[j][0]); dy = F.sub(pts[i][1], pts[j][1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))
def is3(i, j):
    return F.is_zero(F.sub(sqd(i, j), F.rat(3)))

# ---- P1: omega <= 3  (no K_4) -- for each edge {u,v} count common neighbours that
# are adjacent to both u and v; a K_4 exists iff some edge has an adjacent common neighbour.
k4 = []
for u in range(n):
    for v in adj[u]:
        if v < u:
            continue
        for w in (adj[u] & adj[v]):
            if w > v and (adj[w] & adj[u]) and (adj[w] & adj[v]):
                k4.append((u, v, w)); break
        if len(k4) > 5:
            break
print(f"[P1] K_4 witnesses found: {len(k4)}  -> omega<=3: {not k4}  t={time.time()-T0:.2f}s")

# ---- P2 + P3: common-neighbour census over non-adjacent pairs
hist = {}
two_cnt = 0
p3_fail = []
pair_checked = 0
for i in range(n):
    Ai = adj[i]
    for j in range(i + 1, n):
        if j in Ai:
            continue
        pair_checked += 1
        C = Ai & adj[j]
        c = len(C)
        hist[c] = hist.get(c, 0) + 1
        if c == 2:
            two_cnt += 1
            c1, c2 = tuple(C)
            edge12 = c2 in adj[c1]
            want3 = is3(i, j)
            if edge12 != want3:
                p3_fail.append((i, j, edge12, want3))
        if c >= 3:
            hist['>=3'] = hist.get('>=3', 0) + 1
    if time.time() - T0 > CAP:
        print("!! cap reached, results incomplete"); break

print(f"[P2] non-adjacent pairs examined: {pair_checked}")
print(f"[P2] common-neighbour count histogram: {dict(sorted(hist.items(), key=str))}")
print(f"[P2] max common neighbours: {max(c for c in hist if isinstance(c,int))} -> <=2: {not any(isinstance(c,int) and c>=3 for c in hist)}")
print(f"[P3] pairs with exactly 2 common neighbours: {two_cnt}; discriminations failed: {len(p3_fail)} {p3_fail[:3]}")
print(f"[total] {time.time()-T0:.2f}s")
json.dump({"n": n, "m": len(es), "k4_witnesses": len(k4), "pairs": pair_checked,
           "common_nb_hist": {str(a): b for a, b in hist.items()}, "two_cn_pairs": two_cnt,
           "p3_failures": p3_fail, "seconds": round(time.time()-T0, 2),
           "P1_omega_le_3": not k4,
           "P2_max_cn_le_2": not any(isinstance(c, int) and c >= 3 for c in hist),
           "P3_diamond_law": not p3_fail},
          open(os.path.join(HERE, "certs/census_heule553.json"), "w"), indent=1)
