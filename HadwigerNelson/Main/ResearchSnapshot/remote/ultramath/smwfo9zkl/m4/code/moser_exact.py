"""Exact verification of the two finite obstructions used in Theorem B.

Run:  python3 moser_exact.py
Output: prints the eleven unit pairs among the seven spindle vertices, decides
2-, 3- and 4-colourability by SAT, and writes moser_spindle_exact.json.

All arithmetic is exact, in K[i] with K = Q(sqrt3, sqrt11) (see field.py).
Coordinates (Moser spindle, scaled/rotated into K[i]):
    A  = 0
    B  = sqrt3
    B' = sqrt3 * (5/6 + i sqrt11/6)          (so |B - B'| = 1)
    C+ = sqrt3/2 + i/2,  C- = sqrt3/2 - i/2  (the two points at distance 1 from A and B)
    D+ = B'/2 + (1/2) i B'/sqrt3,  D- = B'/2 - (1/2) i B'/sqrt3
        (the two points at distance 1 from A and B')
The graph is the Moser spindle: two 5-edge "diamonds" sharing A, plus the edge B B'.
It is not 3-colourable, hence gives the constant 1/11 in Lemma 3.1.
"""
import sys, json
sys.path.insert(0, '.')
from field import *
from colour import colourable, check_colouring

F0 = F(0)


def addz(z, w):
    return (Kadd(z[0], w[0]), Kadd(z[1], w[1]))


def subz(z, w):
    return (Ksub(z[0], w[0]), Ksub(z[1], w[1]))


def scalez(z, s):
    return (Kscale(z[0], s), Kscale(z[1], s))


def main():
    Z = (F0,) * 4
    r3 = (F0, F(1), F0, F0)
    A = (Z, Z)
    B = (r3, Z)
    Bp = ((F0, F(5, 6), F0, F0), (F0, F0, F0, F(1, 6)))
    C1 = ((F0, F(1, 2), F0, F0), (F(1, 2), F0, F0, F0))
    C2 = ((F0, F(1, 2), F0, F0), (F(-1, 2), F0, F0, F0))
    M = scalez(Bp, F(1, 2))
    Ju = ((F0, F0, F(-1, 6), F0), (F(5, 6), F0, F0, F0))   # i * (B'/sqrt3)
    D1 = addz(M, scalez(Ju, F(1, 2)))
    D2 = subz(M, scalez(Ju, F(1, 2)))
    pts = [A, B, Bp, C1, C2, D1, D2]
    names = ["A", "B", "B'", "C1", "C2", "D1", "D2"]
    edges = [(i, j) for i in range(7) for j in range(i + 1, 7)
             if is_unit(subz(pts[j], pts[i]))]
    print("unit pairs:", [(names[i], names[j]) for i, j in edges])
    print("vertices:", len(pts), " unit edges:", len(edges))
    assert len(edges) == 11, "Moser spindle must have 11 unit edges"
    adj = [set() for _ in range(7)]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    res = {}
    for k in (2, 3, 4):
        sat, col, nclauses = colourable(7, adj, k)
        res[k] = {"satisfiable": sat, "colouring": col, "clauses": nclauses}
        if sat:
            assert check_colouring(7, adj, col, k)
            print(f"{k} colours: SAT, colouring {col} (checked edge by edge)")
        else:
            print(f"{k} colours: UNSAT ({nclauses} clauses) -> not {k}-colourable")
    print()
    print("Constant from Lemma 3.1 with H = Moser spindle: 1/|E(H)| = 1/11.")
    print("Constant from Lemma 3.1 with H = unit triangle: 1/|E(K3)| = 1/3.")
    json.dump({"names": names,
               "coords_num_den_K": [[[str(x) for x in p[0]], [str(x) for x in p[1]]] for p in pts],
               "edges": edges,
               "colourings": {str(k): v for k, v in res.items()}},
              open("moser_spindle_exact.json", "w"), indent=1)
    print("written: moser_spindle_exact.json")


if __name__ == "__main__":
    main()
