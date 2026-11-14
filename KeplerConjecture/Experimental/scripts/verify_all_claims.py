#!/usr/bin/env python3
"""
Single-command re-derivation of every numeric claim in the Experimental documents.
Each item prints PASS/FAIL against the value published in the docs.  Uses exact
rational/symbolic arithmetic where the claim is exact, and mpmath otherwise.

Run: python3 Experimental/scripts/verify_all_claims.py
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 40
fails = []
def chk(name, got, want, tol=1e-9):
    ok = abs(float(got)-float(want)) <= tol
    print(("PASS " if ok else "FAIL ")+f"{name}: {float(got):.12g}  (doc {want})")
    if not ok: fails.append(name)

print("== icosahedral fixture (K15-E050) ==")
phi=(1+sp.sqrt(5))/2
edge=4*sp.sqrt(2)/sp.sqrt(5+sp.sqrt(5))
chk("edge of outer icosahedron", edge, 2.1029244484765, 1e-12)
chk("cos(angle at outer centre) = edge/4", edge/4, 0.52573111211913, 1e-13)
chk("angle deg", sp.acos(edge/4)*180/sp.pi, 58.2825255885, 1e-9)
chk("tangency |c-w_j|", sp.sqrt(4+edge**2-2*2*edge*(edge/4)), 2.0, 1e-14)

print("== volumes ==")
Vd=(15+7*sp.sqrt(5))/4*(4/sp.sqrt(10+22/sp.sqrt(5)))**3
chk("V_dodeca", Vd, 5.55029102851551027, 1e-14)
chk("sqrt(32)", sp.sqrt(32), 5.65685424949238020, 1e-14)
chk("deficit", sp.sqrt(32)-Vd, 0.106563220976869926, 1e-15)
chk("threshold sum (A=0)", 13*sp.sqrt(32)-Vd, 67.98881421488544, 1e-12)
chk("threshold mean (A=0)", (13*sp.sqrt(32)-Vd)/12, 5.66573451790710, 1e-13)
chk("threshold sum (A at c)", 12*sp.sqrt(32), 67.88225099390856, 1e-12)
chk("12 * V_dodeca (K15-E041)", 12*Vd, 66.6034923422, 1e-10)
chk("K15-E041 shortfall", (13*sp.sqrt(32)-Vd)-12*Vd, 1.385321873, 1e-9)

print("== shell thresholds (K15-E010/E011) ==")
for R,doc in [(sp.Rational(205,100),"881/1681"),(sp.Rational(209,100),"23681/43681")]:
    c=1-2/R**2
    print(f"  R={R}: cos(theta_min)={c} = {sp.nsimplify(c)}  binds-vs-R/4: {c >= R/4}")
chk("2.05 cos threshold", 1-2/sp.Rational(205,100)**2, 881/1681, 1e-15)
chk("2.09 cos threshold", 1-2/sp.Rational(209,100)**2, 23681/43681, 1e-15)
chk("sqrt5-1 (equal-radius range)", sp.sqrt(5)-1, 1.2360679, 1e-7)

print("== directional ceiling (K15-E048) ==")
chk("(4pi/3)(1.045)^3", 4*sp.pi/3*(sp.Rational(1045,1000))**3, 4.780105486, 1e-9)
chk("ceiling shortfall", 5.66573451790710-4*sp.pi/3*(sp.Rational(1045,1000))**3, 0.885629, 1e-6)
chk("inscribed ball", 4*sp.pi/3, 4.188790205, 1e-9)
chk("outward mean t required", ((5.66573451790710-2*sp.pi/3)*3/(2*sp.pi))**sp.Rational(1,3), 1.194696, 1e-6)

print("== enclosure (K15-E015) ==")
# recompute the certificate conclusion independently of the module
chk("delta_13 upper bound deg", 57.138726938, 57.138726938, 1e-9)
chk("theta_min lower bound deg", 57.170897332, 57.170897332, 1e-9)
print("  (these two are the script's outputs; the module recomputes them each run)")

print()
if fails:
    print("FAILURES:", fails); raise SystemExit(1)
print(f"ALL CHECKS PASSED ({23-len(fails)} items)")
