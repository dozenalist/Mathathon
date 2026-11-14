"""
Thin-shell counting: cap identity, radius-varying angular conversion, delta table.
Exact rational arithmetic (sympy).  No heavy solve; runs in <1 s.
"""
import sympy as sp

out=[]
def p(s): out.append(str(s)); print(s)

# ---- 1. Cap area identity: k caps of angular radius theta/2 have total area
# k * 2*pi*(1-cos(theta/2)); equality at k=13 with cos(theta/2)=11/13.
th=sp.symbols('theta', positive=True)
for k in (12,13,14):
    # total area / (4 pi) with 1-cos(th/2) = 2/k
    frac=sp.simplify(k*sp.Rational(1,2)*(sp.Rational(2,k)))
    p(f"k={k}: k*2pi(1-cos(th/2)) <= 4pi  <=>  theta <= 2*arccos(1-2/k) = "
      f"{sp.N(2*sp.acos(1-sp.Rational(2,k)),12)} rad")
p("cap identity check: 13*2pi*(1-11/13) = %s ; 4pi = %s ; ratio = %s"
  % (sp.simplify(13*2*sp.pi*(1-sp.Rational(11,13))), 4*sp.pi,
     sp.simplify(13*2*sp.pi*(1-sp.Rational(11,13))/(4*sp.pi))))

# ---- 2. Radius conversion. r,s in [2,2+d]; law of cosines.
r,s,d=sp.symbols('r s delta', positive=True)
cosmin=(r**2+s**2-4)/(2*r*s)
p("cos(theta_min) for radii r,s : %s" % sp.simplify(cosmin))
p("   binding case r=s=t: %s" % sp.simplify(cosmin.subs({r:sp.Symbol('t'),s:sp.Symbol('t')})))
p("   d/dr of 1-2/r^2 at r>0 : %s  (increasing => largest radius is weakest)"
  % sp.simplify(sp.diff(1-2/sp.Symbol('r')**2, sp.Symbol('r'))))

# ---- 3. delta needed so that 13 shell points force theta > Tammes_13
def delta_for(theta13):
    c=sp.cos(theta13)
    return sp.simplify(sp.sqrt(2/(1-c))-2)

p("")
p("delta(theta) = sqrt(2/(1-cos theta)) - 2")
for name,t13 in [("Tammes N=13 (57.1367 deg)", sp.N(sp.pi*57.1367/180,30)),
                 ("cap bound 2arccos(11/13)", 2*sp.acos(sp.Rational(11,13))),
                 ("kissing 60 deg", sp.pi/3)]:
    p(f"  {name:32s} theta={sp.N(t13*180/sp.pi,8)} deg  ->  delta={sp.N(delta_for(t13),8)}")

# ---- 4. crude volume count from C013(a)
p("")
p("C013(a): n <= (3+delta)^3 - 1.  n<=12  <=>  delta <= 13^(1/3)-3 = %s"
  % sp.N(13**sp.Rational(1,3)-3,10))
p("         n<=26  <=>  delta < 27^(1/3)-3 = %s" % sp.N(27**sp.Rational(1,3)-3,10))
p("         28^(1/3)-3 = %s   [(3+delta)^3 = 28]" % sp.N(28**sp.Rational(1,3)-3,12))
p("   at delta=28^(1/3)-3: (3+delta)^3 = %s" % sp.N((3+28**sp.Rational(1,3)-3)**3,12))

# ---- 5. FCC/HCP shell radii
p("")
p("FCC/HCP: 12 neighbours at |y|=2, next shell at 2*sqrt2 = %s" % sp.N(2*sp.sqrt(2),8))
p("  => 12-shell holds for delta < 2sqrt2-2 = %s" % sp.N(2*sp.sqrt(2)-2,8))

open('Experimental/evidence/shell_conversion.txt','w').write("\n".join(out)+"\n")
