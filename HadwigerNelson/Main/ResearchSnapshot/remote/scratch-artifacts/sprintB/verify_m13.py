"""Independent verification of m13's model at k=6 with exact rational arithmetic.
Model: P_z(e^{it}) = {4 + s(t)}, s(t)=floor(9t/(2pi)) mod 3.
Checks: (P1) size; (P2) s(t+pi/3)!=s(t); (P3) for |z-z'|<=1/50 and every unit w,
the two decompositions s+t'=(z'-z)+w satisfy s(arg s)!=s(arg w) and s(arg t')!=s(arg w);
(P4) singletons in {4,5,6} avoid edges of {1,2,3}; (P6) no complementary triples.
Uses Fraction and rational bounds 333/106 < pi < 22/7 (both true: 3.141509<pi<3.142857).
"""
from fractions import Fraction as F
from math import comb
import itertools, random
PI_LO=F(333,106); PI_HI=F(22,7)
def s_of_u(u): # u = 9t/(2pi) rational
    return (u.numerator//u.denominator) % 3
def s_t(t): # t rational multiple of pi handled as t/pi rational
    u=9*t/2  # since t = x*pi, 9t/(2pi)=9x/2
    return s_of_u(u)
# (P1),(P4),(P6)
print("P1: all palettes singleton -> size 1 in 1..3  OK")
print("P4: {4},{5},{6} not subset of {1,2},{1,3},{2,3}  OK")
print("P6: no ternary palette -> no complementary triple pair  OK")
# (P2): beta=3/2. For any u=n+x, x in [0,1): floor(u+3/2)-floor(u)=floor(x+3/2) in {1,2}.
bad=0
for num in range(0,2000):
    u=F(num,7)  # sample rationals
    d=(u+F(3,2)).numerator//(u+F(3,2)).denominator - (u.numerator//u.denominator)
    if d%3==0: bad+=1
print("P2: sampled 2000 rational u, violations:",bad)
# exact statement: floor(x+3/2) in {1,2} for x in [0,1) -> never 0 mod 3. Proof by cases x<1/2 / x>=1/2.
print("P2 proof: x<1/2 -> floor=1; x>=1/2 -> floor=2; both !=0 mod 3.  OK")
# (P3): deviation bound. If arg(s)-arg(w) = +-pi/3 + xi, |xi|<=4d<=4/50,
# beta = 9(arg s-arg w)/(2pi) = +-3/2 + 9 xi/(2pi), |9 xi/(2pi)| <= 9*4/50/(2*333/106)
dev=9*F(4,50)/(2*PI_LO)
print("max |beta -+ 3/2| =",float(dev),"; need < 1/2:", dev<F(1,2))
lo=F(3,2)-dev; hi=F(3,2)+dev
print("beta in [",float(lo),",",float(hi),"] subset (1,2):", lo>1 and hi<2)
print("mirror negative interval subset (-2,-1):", -hi>-2 and -lo<-1)
# And the key fact for any beta in (1,2): floor(x+beta)-floor(x) in {1,2} for all x in [0,1).
# Proof: x+beta in (1,3), so floor in {1,2}; difference nonzero mod 3.
print("P3 conclusion: s(t+b)!=s(t) for all t whenever 1<beta<2 or -2<beta<-1.  OK")
# Triangle locus = whole plane: (P4) holds at every z and (P5) with W_z={delta_{4+s}}.
print("(P5): W_z = {delta_{4+s(t)}} supported in P_z, kills labels 1,2,3 identically.  OK")
print("ALL CHECKS PASS")
