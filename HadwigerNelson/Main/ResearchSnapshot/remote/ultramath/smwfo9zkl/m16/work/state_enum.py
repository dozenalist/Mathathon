"""k-colour cyclic-centre palette-state accounting.

At a cyclic centre x whose transition graph Gamma_x contains a simple cycle Q of
length ell (vertex set T, edge set Ec), the palette function P_x: S -> 2^I satisfies,
for almost every direction t:

  (P1)  1 <= |P(t)| <= k-3                       [palette bound]
  (P2)  P(t) not a subset of {i,j}  for every {i,j} in Ec   [paper (6.2)]
  (P3)  P(t) cap P(t+kappa) = empty, kappa = pi/3           [paper (5.7)]

Since 6*kappa = 2*pi, (P3) says: along each R-orbit of directions, which is a
6-cycle in direction space, the palette values w_0..w_5 satisfy w_j cap w_{j+1}
= empty (indices mod 6).  We call such a 6-tuple an *orbit datum*.

Every measurable palette function realises one orbit datum per orbit; and for any
admissible orbit datum (w_0..w_5) the piecewise-constant function
P(t) = w_j for t in [j*kappa,(j+1)*kappa) is measurable and satisfies (P1)-(P3).
So the set of *attainable support families* is exactly the set of unions of value
sets of admissible orbit data.

Engines available to a paper-style argument:

  E1 (Lemma 5.5, binary centre): exists a fixed label pair {i,j} with
      |v cap {i,j}| = 1 for EVERY value v in the support.  Then P alternates on
      the pair and the locus is delta*-separated (Lemma 5.5 is k-independent).

  E2 (Theorem A of this work = paper Lemma 6.4 generalised): a 2-state
      quotent: the support is covered by two classes A_0,A_1 of a proper
      2-colouring of the disjointness graph, with disjoint represented groups
      G_a <= cap{v : v in class a} and |G_0| + |G_1| = k-2.  Then contradiction.

  E3 (paper Lemma 6.3): same with |G_0| + |G_1| = k-1 (singleton complement);
      gives support separation (not a contradiction by itself).

This program computes, for each k and ell, the disjointness graph, whether it is
bipartite (with a certificate either way), the largest group pair, and which
engines apply.  Entry-wise, the answer is checked a second time by
state_enum2.py, written independently.
"""
import itertools, json, sys

def palette_values(k, cycle_vertices, cycle_edges):
    I = list(range(k))
    allowed = []
    for r in range(1, k-2):          # r = |v|;  palette bound 1 <= |v| <= k-3
        for v in itertools.combinations(I, r):
            s = set(v)
            if any(s <= set(e) for e in cycle_edges):
                continue
            allowed.append(frozenset(s))
    return sorted(allowed, key=lambda z: (len(z), sorted(z)))

def disjoint_graph(vals):
    n = len(vals)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if not (vals[i] & vals[j]):
                adj[i].append(j); adj[j].append(i)
    return adj

def two_colour(adj):
    """BFS 2-colouring.  Returns (colours, None) or (None, odd_cycle)."""
    n = len(adj); col = [-1]*n
    for s in range(n):
        if col[s] >= 0: continue
        col[s] = 0; par = {s: None}; queue=[s]
        while queue:
            u = queue.pop()
            for v in adj[u]:
                if col[v] < 0:
                    col[v] = 1-col[u]; par[v]=u; queue.append(v)
                elif col[v] == col[u]:
                    # reconstruct the odd cycle u -> (tree path) -> v -> u
                    anc = {}
                    x = u; d = 0
                    while x is not None:
                        anc[x] = d; x = par[x]; d += 1
                    y = v; back = []
                    while y not in anc:
                        back.append(y); y = par[y]
                    a = anc[y]
                    pathu = []
                    x = u
                    while x != y:
                        pathu.append(x); x = par[x]
                    cyc = pathu + [y] + list(reversed(back)) + [u]
                    return None, cyc
    return col, None

def count_orbit_data(adj):
    """number of 6-tuples (w_0..w_5) with cyclic disjointness = #closed walks of length 6"""
    import numpy as np
    n = len(adj)
    A = np.zeros((n,n), dtype=object)
    for i in range(n):
        for j in adj[i]:
            A[i][j] = 1
    M = A.copy()
    for _ in range(5):
        M = M.dot(A)
    return int(sum(M[i][i] for i in range(n)))

def core_groups(vals, colours, cls):
    vs = [vals[i] for i in range(len(vals)) if colours[i] == cls]
    if not vs: return frozenset()
    core = vs[0]
    for v in vs[1:]:
        core = core & v
    return frozenset(core)

def engines(k, vals, adj, colours):
    res = {}
    # E1
    e1 = []
    for i, j in itertools.combinations(range(k), 2):
        pr = {i, j}
        if all(len(v & pr) == 1 for v in vals):
            e1.append(sorted(pr))
    res["E1_pairs"] = e1
    # E2 / E3 from the bipartition (if it exists)
    res["E2"] = res["E3"] = None
    if colours is not None:
        g0 = core_groups(vals, colours, 0); g1 = core_groups(vals, colours, 1)
        res["groups"] = [sorted(g0), sorted(g1)]
        res["E2"] = (len(g0)+len(g1) == k-2 and len(g0) > 0 and len(g1) > 0)
        res["E3"] = (len(g0)+len(g1) == k-1 and len(g0) > 0 and len(g1) > 0)
    return res

def main():
    report = {}
    for k in (5, 6):
        for ell in range(3, k+1):
            T = list(range(ell))
            Ec = [frozenset({T[i], T[(i+1) % ell]}) for i in range(ell)]
            vals = palette_values(k, T, Ec)
            adj = disjoint_graph(vals)
            # values that actually occur in an admissible orbit datum
            occ = [i for i in range(len(vals)) if adj[i]]
            valso = [vals[i] for i in occ]
            adjo = [[occ.index(j) for j in adj[occ[i]]] for i in range(len(occ))]
            colours, odd = two_colour(adjo)
            nod = count_orbit_data(adjo)
            ent = {
              "k": k, "ell": ell,
              "n_allowed": len(vals),
              "allowed": [sorted(v) for v in vals],
              "n_occurring": len(valso),
              "occurring": [sorted(v) for v in valso],
              "bipartite": colours is not None,
              "odd_cycle_witness": None if odd is None else [sorted(valso[i]) for i in odd],
              "two_colouring": None if colours is None else
                  {str(sorted(valso[i])): colours[i] for i in range(len(valso))},
              "n_orbit_data": nod,
              "engines": engines(k, valso, adjo, colours),
            }
            report[f"k{k}_ell{ell}"] = ent
    txt = json.dumps(report, sort_keys=True, indent=1)
    open("states_k5_k6.json","w").write(txt)
    print(f"{'key':10s} {'#occ':>4s} {'bip':>5s} {'#orbits':>8s}  E1_pairs        E2    E3   groups / odd-cycle-witness")
    for key in sorted(report):
        e = report[key]
        eng = e["engines"]
        extra = ("groups="+str(eng.get("groups"))) if e["bipartite"] else ("odd cycle: "+ " - ".join(str(v) for v in (e["odd_cycle_witness"] or [])))
        print(f"{key:10s} {e['n_occurring']:4d} {str(e['bipartite']):>5s} {e['n_orbit_data']:8d}  {str(eng['E1_pairs']):15s} {str(eng['E2']):5s} {str(eng['E3']):5s} {extra}")
    import hashlib
    print("SHA256 of canonical json:", hashlib.sha256(txt.encode()).hexdigest())

main()
