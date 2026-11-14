"""Check of the ternary-successor lemma's arithmetic and of the known models.

Lemma.  k=6, x a 6-cycle centre (all palettes have >= 2 labels).  Let T be a palette value with
|T| = 3 on a positive-measure direction set E_T, and let V be a pair value with V subset [6]\\T.
Put E = {a in E_T : P_x(Ra) = V}.  Then E contains no arc of length >= gamma = 2 arcsin(1/(2 sqrt3)).

Proof chain:  (5.7) gives P(Ra) cap T = empty; |P| >= 2 so P(Ra) is a pair or triple inside T^c;
a complementary triple is excluded by (5.2); hence P(Ra) is a pair.  For a in E, Ra in E_V, so
z(a) = e^{ia}+e^{iRa} = sqrt3 e^{i(a+30deg)} lies in E_T + E_V.  Two such points with angle gamma
are at distance 2 sqrt3 sin(gamma/2) = 1.  |T u V| = 5 so |T'| = 1 < chi(unit edge) = 2.
"""
from fractions import Fraction as F
import sys
sys.path.insert(0,'work')
from gamma_crit import G_LO, G_HI
from fractions import Fraction

# 1. the distance identity: 2*sqrt3*sin(gamma/2) = 1, i.e. sin(gamma/2) = 1/(2 sqrt3)
#    gamma/2 = arcsin(1/(2 sqrt3)) by definition of gamma -> exact
print("gamma/2 = arcsin(1/(2 sqrt3)) so 2 sqrt3 sin(gamma/2) = 2 sqrt3 * 1/(2 sqrt3) = 1  (exact)")
print("gamma in degrees = (%.9f, %.9f)" % (float(G_LO), float(G_HI)))
print("|1+e^{i60deg}| = sqrt3 : 1 + e^{i60} = 1.5 + i sqrt3/2, modulus^2 = 2.25+0.75 = 3 (exact)")

# 2. free_l6: the only ternary value sits on one 10-degree sector -> 10 < gamma, consistent
word = [[(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
        [(3,5),(3,5),(2,5),(2,5),(2,4,5),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
        [(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)]]
w=[frozenset(t) for r in word for t in r]
tri=[i for i in range(36) if len(w[i])==3]
print("free_l6 ternary sectors:", tri, "-> arc length", 10*len(tri), "deg  (< gamma:", 10*len(tri) < float(G_LO), ")")
print("free_l6: R-successor of a ternary sector:", [sorted(w[(i+6)%36]) for i in tri])
# the 16 admissible palettes at a 6-cycle centre with centre colour 0, and their complement types
import itertools
ADM=[frozenset(s) for r in (2,3) for s in itertools.combinations(range(1,6),r)
     if not any(frozenset(s) <= frozenset({i,(i+1)%6}) for i in range(6))]
print("admissible palettes: %d pairs + %d triples = %d"%(sum(1 for P in ADM if len(P)==2),
      sum(1 for P in ADM if len(P)==3), len(ADM)))
# for each triple, the pairs inside its complement (these are the possible R-successors)
for T in [P for P in ADM if len(P)==3][:4]:
    comp=frozenset(range(6))-T
    print("  T=%-10s complement=%-9s pairs inside complement: %s"%(sorted(T),sorted(comp),
          [sorted(V) for V in ADM if len(V)==2 and V<=comp]))
