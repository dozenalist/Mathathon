"""Exact rational endpoint for the rho=209/100 thin-shell lemma (K15-E014)."""
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 50

R = F(209,100)
c = 1 - F(2,1)/ (R*R)              # exact rational cos(theta_min)
print("cos(theta_min) exact =", c, "=", float(c))
print("   numerator/denominator:", c.numerator, "/", c.denominator)

# exact comparison with R/4  (confirms equal-radius case binds)
print("1-2/R^2 - R/4 exact =", c - R/4, ">0 means equal-radius binds:", c - R/4 > 0)

th = mp.acos(mp.mpf(c.numerator)/mp.mpf(c.denominator))
deg = th*180/mp.pi
print("theta_min =", mp.nstr(deg, 15), "deg")

t13 = mp.mpf("57.1367")*mp.pi/180
print("slack vs 57.1367 deg =", mp.nstr((th-t13)*180/mp.pi, 10), "deg")
print("slack rad           =", mp.nstr(th-t13, 10))
print("required: a certified theta_13^+ strictly below theta_min")
