"""Bug fix, not a new variant: the P1 test in census.py counted TRIANGLES as K_4.
A K_4 needs a 4th vertex adjacent to all three triangle vertices.  P2 and P3 are
unaffected and are not recomputed here (they passed on the registered run)."""
import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from udg.exact import Field
from udg.heule import load, load_edges
F = Field([3, 5, 11])
pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts); adj = [set() for _ in range(n)]
for a, b in es:
    adj[a].add(b); adj[b].add(a)
t0 = time.time()
tri = 0; k4 = []
for u in range(n):
    for v in adj[u]:
        if v < u: continue
        for w in (adj[u] & adj[v]):
            if w > v:
                tri += 1
                common = adj[u] & adj[v] & adj[w]
                if common:
                    k4.append((u, v, w, min(common)))
print(f"[P1] triangles: {tri}")
print(f"[P1] K_4 witnesses: {len(k4)} {k4[:5]} -> omega<=3: {not k4}")
print(f"[P1] max clique size (by exhaustive check that no triangle has a common neighbour): "
      f"{3 if not k4 else 4}")
print(f"t={time.time()-t0:.2f}s")
d = json.load(open(os.path.join(HERE, "certs/census_heule553.json")))
d["P1_note"] = ("first run's P1 test counted triangles (bug in my code); corrected test below. "
                "P2/P3 unchanged.")
d["triangles"] = tri; d["k4_witnesses"] = len(k4); d["P1_omega_le_3"] = not k4
d["P1_corrected_seconds"] = round(time.time() - t0, 2)
json.dump(d, open(os.path.join(HERE, "certs/census_heule553.json"), "w"), indent=1)
print("updated certs/census_heule553.json")
