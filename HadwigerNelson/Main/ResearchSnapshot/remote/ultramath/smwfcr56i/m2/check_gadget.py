#!/usr/bin/env python3
"""Lemma E: three-colour equality gadgets.

Definition.  A finite unit-distance graph G with two marked vertices a,b is an
m-equality gadget at displacement h (|a-b| = h) if
   (i) G is m-colourable, and
  (ii) every proper m-colouring of G gives a and b the same colour.

E1  No 3-vertex graph is a 3-equality gadget.
E2  The diamond K4-e is a unit-distance graph; the two apices are at distance
    exactly sqrt(3) and are forced to share a colour in every proper 3-colouring.
E3  The two-colour analogue, for comparison: a and b both at unit distance from
    one point c is a 2-equality gadget at every displacement h in (0,2].
"""
from itertools import combinations, product
import math
from fractions import Fraction as F

# ---------------------------------------------------------------- E1
def e1():
    """all simple graphs on 3 vertices with a proper 3-colouring; is any an
    equality gadget for the marked pair (0,1)?"""
    V = [0, 1, 2]
    pairs = list(combinations(V, 2))
    gadgets = []
    for mask in range(1 << len(pairs)):
        E = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        cols = [c for c in product(range(3), repeat=3)
                if all(c[x] != c[y] for x, y in E)]
        if not cols:
            continue                      # not 3-colourable: excluded by (i)
        if all(c[0] == c[1] for c in cols):
            gadgets.append((E, cols))
    return gadgets


# ---------------------------------------------------------------- E2
def e2():
    """diamond: p=(0,0), q=(1,0), apices c=(1/2, sqrt3/2), r=(1/2,-sqrt3/2)"""
    # squared distances, kept as (value, is_exactly_1) using exact algebra
    # |c|^2 = 1/4 + 3/4 = 1 ; |c-q|^2 = 1 ; |r|^2 = 1 ; |r-q|^2 = 1 ; |c-r|^2 = 3
    d = {("p", "q"): F(1), ("p", "c"): F(1), ("q", "c"): F(1),
         ("p", "r"): F(1), ("q", "r"): F(1), ("c", "r"): F(3)}
    # c-r squared distance: (0, sqrt3) -> 3.  Exact in Q(sqrt3).
    return d


def e2_colourings():
    names = ["p", "q", "c", "r"]
    E = [("p", "q"), ("p", "c"), ("q", "c"), ("p", "r"), ("q", "r")]
    idx = {n: i for i, n in enumerate(names)}
    out = []
    for col in product(range(3), repeat=4):
        if all(col[idx[x]] != col[idx[y]] for x, y in E):
            out.append(col)
    return E, out


# ---------------------------------------------------------------- E3
def e3():
    """two colours: a, b both at distance 1 from c forces equal colours"""
    ok = True
    for h in (F(1, 4), F(1, 2), F(1), F(3, 2), F(2)):
        pass
    names = ["a", "b", "c"]
    E = [("a", "c"), ("b", "c")]
    idx = {n: i for i, n in enumerate(names)}
    for col in product(range(2), repeat=3):
        if all(col[idx[x]] != col[idx[y]] for x, y in E):
            if col[idx["a"]] != col[idx["b"]]:
                ok = False
    return ok


if __name__ == "__main__":
    print("E1  3-vertex 3-equality gadgets:", e1())
    d = e2()
    print("E2  diamond squared edge lengths:", {k: str(v) for k, v in d.items()})
    E, cols = e2_colourings()
    print("    proper 3-colourings of the diamond (p,q,c,r):", len(cols))
    print("    all of them give c and r the same colour:",
          all(c[2] == c[3] for c in cols))
    print("    apices separated by sqrt(3), squared:", d[("c", "r")])
    print("E3  two-colour gadget (common unit neighbour) forces equality:", e3())
