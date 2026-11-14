"""Pilot block: exact controls + the spindle parity amplification probe.

Declared finite search space (exhaustive within its stated scope):
  E1 ladder -- graphs: diamond, Moser spindle, spindle triangle, and for each graph
     with a closing unit pair (p,q): (+d1) the two common unit neighbours of (p,q),
     (+d2) then the two common unit neighbours of that new pair.  For every graph
     and k in {2,3,4,5,6}: complete exhaustive count of proper k-colourings
     (no cap) plus a CDCL decision by two independent solvers.
  E2 amplification probe -- for the closing pair (p,q) of each graph, count the
     k-colourings of the CONTRACTED graph G/pq, i.e. those with c(p)=c(q).
     An equality-forcing gadget for k colours occurs in this family at k iff
     that count is 0 for every member.
"""
import json, os, sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from udg.graph import (validate, exhaustive_count, verify_colouring, sat_decision,
                       clique_number_bound, degrees)
from udg import build as B
from fractions import Fraction as Fr

OUT = os.path.join(HERE, "certs")
os.makedirs(OUT, exist_ok=True)
LOG = []


def log(s):
    print(s, flush=True)
    LOG.append(s)


def contract(adj, p, q):
    n = len(adj)
    keep = [v for v in range(n) if v != q]
    remap = {v: i for i, v in enumerate(keep)}
    remap[q] = remap[p]
    m = len(keep)
    new = [set() for _ in range(m)]
    for v in range(n):
        for u in adj[v]:
            a, b = remap[v], remap[u]
            if a != b:
                new[a].add(b)
                new[b].add(a)
    return new


def _with_edge(adj, p, q):
    a = [set(x) for x in adj]
    a[p].add(q)
    a[q].add(p)
    return a


def analyse(name, ps, info, results, merge=True):
    dups = 0
    if merge:
        ps, dups = ps.canonical()
        if dups:
            log(f"  [{name}] {dups} coincident point(s) merged (construction reuses existing vertices)")
    adj, nonedges = ps.unit_graph()
    rec = validate(ps, adj, nonedges, name, log)
    rec["coincident_points_merged"] = dups
    assert rec["all_points_distinct"], name
    tips = info["tips"]
    pairs = info["closing"]
    rec["k"] = {}
    for k in (2, 3, 4, 5, 6):
        cnt, col = exhaustive_count(adj, k)
        ok = None
        if col is not None:
            ok, msg = verify_colouring(adj, col, k)
            assert ok, msg
        sat = sat_decision(adj, k)
        verdicts = sat["verdicts"]
        consistent = all((v == "SAT") == (cnt > 0) for v in verdicts.values())
        rec["k"][str(k)] = {"n_colourings": cnt, "exhaustive_sat": cnt > 0,
                            "cdcl": verdicts, "cdcl_consistent": consistent,
                            "witness": col}
        log(f"  [{name}] k={k}: #colourings={cnt}  cdcl={verdicts} consistent={consistent}")
        assert consistent, (name, k, cnt, verdicts)
        if col is not None:
            json.dump({"graph": name, "n": rec["n"], "k": k, "colouring": col,
                       "edges_checked": rec["m"]},
                      open(os.path.join(OUT, f"{name}.k{k}.colouring.json"), "w"), indent=1)
    # E2: forced-relation census over every NON-ADJACENT pair, k = 3..6.
    # For a non-adjacent pair (p,q): n_eq = #proper k-colourings of G with c(p)=c(q)
    # (= colourings of the contraction G/pq); n_ne = total - n_eq.
    #   n_ne == 0  ->  p,q forced EQUAL at k     (equality gadget)
    #   n_eq == 0  ->  p,q forced DIFFERENT at k
    rec["forced_pairs"] = {}
    n = len(adj)
    for k in (3, 4, 5, 6):
        total = rec["k"][str(k)]["n_colourings"]
        feq, fne = [], []
        if total > 0:
            for p, q in combinations(range(n), 2):
                if q in adj[p]:
                    continue
                # n_eq == 0  <=>  G/pq not k-colourable ;  n_ne == 0  <=>  G+pq not k-colourable
                sat_eq = sat_decision(contract(adj, p, q), k, solvers=("cadical153",))["verdicts"]["cadical153"]
                if sat_eq == "UNSAT":
                    fne.append([ps.names[p], ps.names[q]])
                    cnt, _ = exhaustive_count(contract(adj, p, q), k)   # certificate, must be 0
                    assert cnt == 0
                    continue
                adj2 = [set(a) for a in adj]
                adj2[p].add(q)
                adj2[q].add(p)
                if sat_decision(adj2, k, solvers=("cadical153",))["verdicts"]["cadical153"] == "UNSAT":
                    feq.append([ps.names[p], ps.names[q]])
                    cnt, _ = exhaustive_count(adj2, k)
                    assert cnt == 0
        rec["forced_pairs"][str(k)] = {"forced_equal": feq, "forced_different": fne,
                                       "n_nonadjacent_pairs": sum(1 for p, q in combinations(range(n), 2) if q not in adj[p])}
        log(f"  [{name}] k={k} forced pairs: equal={len(feq)} different={len(fne)}"
            f" (of {rec['forced_pairs'][str(k)]['n_nonadjacent_pairs']} non-adjacent pairs)")
    results.append(rec)
    return adj, rec


def decorate(ps, info, tag):
    """Decorated variants, each on its own copy of the point set:
       +d1 = add the two common unit neighbours of the closing pair (p,q);
       +d2 = then add the two common unit neighbours of that new pair."""
    out = []
    for (p, q) in info["closing"]:
        a = ps.copy()
        i1, i2 = B.add_diamond(a, p, q, f"d1_{a.names[p]}{a.names[q]}.")
        out.append((f"{tag}+d1", a, {"tips": info["tips"], "closing": [(i1, i2)]}))
        b = ps.copy()
        j1, j2 = B.add_diamond(b, p, q, f"d1_{b.names[p]}{b.names[q]}.")
        k1, k2 = B.add_diamond(b, j1, j2, f"d2_{b.names[p]}{b.names[q]}.")
        out.append((f"{tag}+d2", b, {"tips": info["tips"], "closing": [(k1, k2)]}))
    return out


def main():
    results = []
    log("=== E1/E2 pilot: exact unit-distance graphs over Q(sqrt3,sqrt11) ===")
    ps, info = B.diamond()
    adj_d, rec_d = analyse("diamond", ps, info, results)
    t0, t1 = info["tips"]
    log("  [diamond] exact tip-relation counts (tips are NON-adjacent, sqrt(3) apart):")
    for k in (3, 4, 5, 6):
        eq, _ = exhaustive_count(contract(adj_d, t0, t1), k)
        ne, _ = exhaustive_count(_with_edge(adj_d, t0, t1), k)
        rec_d.setdefault("diamond_tip_relation", {})[str(k)] = {"equal": eq, "different": ne}
        log(f"    k={k}: #colourings with c(t0)=c(t1) is {eq}, with c(t0)!=c(t1) is {ne}")

    ps, info = B.moser()
    adj, rec = analyse("moser", ps, info, results)

    ps, info = B.spindle_triangle()
    analyse("spindle_triangle", ps, info, results)

    # decorations of the Moser spindle (its own point set, extended)
    for ctor, tag in ((B.moser, "moser"), (B.spindle_triangle, "spindle_triangle")):
        ps0, info0 = ctor()
        for nm, psx, inf in decorate(ps0, info0, tag):
            analyse(nm, psx, inf, results)

    json.dump({"log": LOG, "graphs": results}, open(os.path.join(OUT, "pilot.json"), "w"), indent=1)
    log(f"wrote {os.path.join(OUT,'pilot.json')}")
    # summary table
    lines = ["| graph | n | m | omega | k=2 | k=3 | k=4 | k=5 | k=6 | forced pairs (eq/neq) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        eqv = ",".join(f"k{k}:{len(r['forced_pairs'][str(k)]['forced_equal'])}eq/{len(r['forced_pairs'][str(k)]['forced_different'])}ne" for k in (3,4,5,6))
        lines.append(f"| {r['name']} | {r['n']} | {r['m']} | {r['clique_number']} | {r['k']['2']['n_colourings']} | "
                     f"{r['k']['3']['n_colourings']} | {r['k']['4']['n_colourings']} | "
                     f"{r['k']['5']['n_colourings']} | {r['k']['6']['n_colourings']} | {eqv} |")
    open(os.path.join(OUT, "table.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
