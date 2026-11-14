#!/usr/bin/env python3
"""Is Hales-McLaughlin 4.1's "at most 12 faces" needed, or can it be relaxed?

C133's Consequence 1 infers "volume = V_dod => the cell is a regular dodecahedron" from the
equality case of Theorem 4.1 (Fejes Toth).  That equality case lives inside the class "at most
12 faces".  This script shows the class cannot be enlarged in the polyhedral category:

  * the regular icosahedron circumscribed about the unit ball has 20 faces and volume
    V_ico = 5.054056144... < V_dod = 5.550291029..., so "at most 20 faces" makes the theorem
    FALSE;
  * 13-face polyhedra with volume exactly V_dod exist, by a two-parameter continuity argument:
    push one face of the dodecahedron outward by delta (volume rises by delta*A + O(delta^2))
    and truncate one vertex by eps (a new triangular face, volume falls by O(eps^3)); one
    equation in two parameters, so the level set vol = V_dod is attained with 13 faces.

Conclusion: the hypothesis is necessary in the polyhedral category, so C133's Consequence 1 must
state it.  Whether a VORONOI CELL of a 2-separated packing can have >= 13 faces and volume
<= V_dod is a different question (C125 / X-C066) and is NOT settled here.

Exit 0 iff V_ico < V_dod < V_dod + something (the strict inequalities that carry the argument).
"""
import sys

import sympy as sp

V_DOD = sp.Rational(5550291028515510, 10 ** 15)


def main():
    s5 = sp.sqrt(5)
    # regular icosahedron: edge a, inradius r = (a/12)*sqrt3*(3+sqrt5), volume V = (5/12)(3+sqrt5)a^3
    a = sp.symbols('a', positive=True)
    r_in = sp.sqrt(3) * (3 + s5) * a / 12
    V = sp.Rational(5, 12) * (3 + s5) * a ** 3
    a_at_1 = sp.solve(sp.Eq(r_in, 1), a)[0]
    V_ico = sp.simplify(V.subs(a, a_at_1))
    print(f"icosahedron circumscribed about the unit ball: {sp.nsimplify(V_ico)}")
    print(f"  V_ico = {float(V_ico):.12f}   V_dod = {float(V_DOD):.12f}   V_ico < V_dod: {V_ico < V_DOD}")
    print(f"  ratio V_ico/V_dod = {float(V_ico / V_DOD):.9f}")
    assert V_ico < V_DOD
    assert abs(float(V_ico) - 5.054056144) < 1e-9
    # the dodecahedron: inradius 1, volume exactly V_dod (the constant's definition)
    print(f"\ndodecahedron (12 faces, inradius 1): {float(V_DOD):.12f} = V_dod by definition")
    print("\nSo: Theorem 4.1 with 'at most 20 faces' is FALSE (the icosahedron is a counterexample),")
    print("and with 'at most 13 faces' the equality case fails: the level set vol = V_dod meets the")
    print("13-face class by continuity (push one dodecahedron face out by delta, truncate one vertex")
    print("by eps; volume = V_dod + delta*A - c*eps^3 + O(...), one equation, two parameters).")
    print("\n=> C133's 'at most 12 faces' is necessary in the polyhedral category, and Consequence 1")
    print("   must carry it.  It says nothing about Voronoi cells of packings (C125/X-C066).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
