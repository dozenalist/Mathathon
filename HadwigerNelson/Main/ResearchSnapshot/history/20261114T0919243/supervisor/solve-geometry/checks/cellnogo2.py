"""Audit of CELL-NOGO-v2 Theorem 2: the K_7 obstruction and its windows. Exact, no search."""
import os
from fractions import Fraction as F
from itertools import combinations

out=[]
def say(*a):
    s=" ".join(str(x) for x in a); out.append(s); print(s)
Norm=lambda p,q: p*p+p*q+q*q
say("[18] CELL-NOGO-v2 Theorem 2: the 7-clique in the N in {1,3,4} Cayley graph")
S=[(0,0),(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
say(f"     S = centre + six ring-1 neighbours: {S}")
norms=[]
for a,b in combinations(S,2):
    d=(b[0]-a[0], b[1]-a[1]); norms.append(Norm(*d))
say(f"     all {len(norms)} pairwise differences have Eisenstein norm in "
    f"{sorted(set(norms))}  (subset of {{1,3,4}}: {set(norms)<= {1,3,4}})")
say(f"     => S is a K_7 in Cay(Z^2, {{N in {{1,3,4}}}}), so chi >= 7")
vec=[(p,q) for p in range(-3,4) for q in range(-3,4) if 0 < Norm(p,q) <= 4]
say(f"     the {len(vec)} vectors with 0 < N <= 4 (18 expected): {len(vec)==18}, "
    f"norms {sorted(set(Norm(*v) for v in vec))}")
bad=[v for v in vec if (v[0]+3*v[1]) % 7 == 0]
say(f"     colouring (p,q) -> p+3q mod 7: vectors hit by 0 = {len(bad)} (need 0) -> chi <= 7")
say(f"     combined: chi(Cay(Z^2, N in {{1,3,4}})) = 7")

# windows: mu^2, nu^2 at a=1 (exact polygon values, from the accepted per-offset table)
tab={1:(0,13), 3:(1,25), 4:(3,28), 7:(7,43), 9:(12,49), 12:(16,64), 13:(19,67)}
say("[19] per-ring windows (1/nu, 1/mu), exact endpoints")
import math
for N,(mu2,nu2) in sorted(tab.items()):
    lo = '0' if nu2==0 else f'1/sqrt{nu2} = {math.sqrt(1/nu2):.6f}'
    hi = 'inf' if mu2==0 else (f'1/{math.sqrt(mu2):.6f}' if int(math.isqrt(mu2))**2!=mu2 else f'1/{math.isqrt(mu2)}')
    say(f"     N={N:2d}: mu^2={mu2:2d}, nu^2={nu2:2d} -> forced on ({lo}, {hi})")

# endpoint questions at a = 1/2 and a = 1/sqrt13, via exact squared comparisons
say("[20] endpoints, decided by exact integer comparisons")
for N in (1,3,4):
    mu2,nu2 = tab[N]
    forced_half = (mu2 < 4) and (nu2 > 4)          # 1/nu < 1/2 < 1/mu  <=>  mu<2<nu  <=> mu^2<4<nu^2
    say(f"     a = 1/2, ring {N}: forced = {forced_half}  (mu^2<4<nu^2: {mu2}<4<{nu2})")
say(f"     a = 1/sqrt13, ring 1: 1/nu = 1/sqrt13 exactly (nu^2 = 13) -> NOT strictly forced:"
    f" {13 > 13 is False}")
say(f"     a = 1/sqrt13, rings 3 and 4 still forced: "
    f"{tab[3][0]<13 and tab[3][1]>13}, {tab[4][0]<13 and tab[4][1]>13}"
    f"  (mu^2 < 13 < nu^2 with a^2 = 1/13)")
say("     => at a = 1/2 the K_7 argument applies (not merely vacuity);")
say("        at a = 1/sqrt13 ring 1 is a tangency, so the K_7 fails there: the endpoint is open")
# window sufficiency: a ring forced at a >= 1/sqrt13 has mu^2 <= 13
say("[21] window sufficiency: a ring forced at a >= 1/sqrt13 has mu^2(a=1) <= 13")
ok=[N for N,(m,n) in tab.items() for _ in [0] if m <= 13]
say(f"     rings with mu^2 <= 13: {sorted(ok)} (N=12 has mu^2=16, so excluded);"
    f" matches the producer's {{1,3,4,7,9}}: {sorted(ok)==[1,3,4,7,9]}")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","supervisor_checks.out"),"a").write("\n".join(out)+"\n")
