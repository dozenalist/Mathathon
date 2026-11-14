"""The record's flagged-unchecked item: is m6's STRIP(6,5) witness killed by Lemma 6.4?

m6's witness (smwfo9zkl/m6 RESULTS.md, Theorem 2, ell=5 row):
    P(u) = {5}    on the open arcs (r*60, (r+1)*60) deg with r even,
    P(u) = {1,3}  on the odd arcs.
Two palette values A = {5}, B = {1,3}, |A u B| = 3 = k-3 at k = 6.

m12's/m7's mechanism (Theorem 1 of m12 = the k-general Lemma 6.4) says: two disjoint palette
groups on positive-measure direction sets force |[k] \ (G_1 u G_2)| >= chi(Q) for every finite
unit-distance graph Q in the direction-sum set.  Here |T'| = 6 - 3 = 3, so a contradiction
needs chi(Q) >= 4, i.e. a 4-chromatic unit-distance graph in Z(E_A, E_B); a unit triangle
(chi = 3) gives only the true inequality 3 >= 3.
"""
from fractions import Fraction as F
from ival import norm, inter, rotate, diff, member
import consts

EA = norm([(0, 60), (120, 180), (240, 300)])          # {5}
EB = norm([(60, 120), (180, 240), (300, 360)])        # {1,3}

def orbit3(E):
    return inter(inter(E, rotate(E, 120)), rotate(E, 240))

UA, UB = orbit3(EA), orbit3(EB)
print("A = {5} on", EA)
print("B = {1,3} on", EB)
print("orbit3(E_A) = E_A ?", UA == norm(EA), "  orbit3(E_B) = E_B ?", UB == norm(EB))
D = diff(UA, UB)          # psi must lie here for the role B->A (t in E_B, t+psi in E_A)
Db = diff(UB, UA)
inside = lambda S: any(a <= consts.PSI_LO and consts.PSI_HI < b for a, b in S)
print("psi in U_A - U_B ?", inside(Db), "   psi in U_B - U_A ?", inside(D))
print("=> the sum set contains a unit equilateral triangle (m12 Theorem 2):", inside(Db) or inside(D))
print()
print("k-arithmetic at k = 6:")
print("   |A u B| = ", len({5} | {1,3}), "   |T'| = ", 6 - len({5} | {1,3}))
print("   chi(unit triangle) = 3 <= |T'| = 3  ->  NO contradiction")
print("   a contradiction would need chi(Q) >= 4, i.e. a 4-chromatic unit-distance")
print("   graph inside Z(E_A,E_B); none is exhibited anywhere in the record.")
