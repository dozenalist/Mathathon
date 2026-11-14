#!/usr/bin/env python3
"""X's independent adversarial battery for Main's shell_check predicates.

Usage: python3 x_adversarial_shellcheck.py <path-to-shell_check.py>
Every expectation is derived independently (value at a witness point / known maths).
Note the trap that caught ME while writing it: "has a double root" is NOT "satisfies <= 0".
(u-1)^2 touches zero from ABOVE, so it is NOT <= 0 on [0,2]; the touching-from-below case is
-(u-1)^2.  Both directions are tested below.
"""
import importlib.util, sys, sympy as sp
path = sys.argv[1] if len(sys.argv)>1 else 'shell_check_9461aae.py'
spec=importlib.util.spec_from_file_location("sc",path); sc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)
u=sp.Symbol('u')
def C(*cs): return [sp.Integer(c) for c in cs]
bad=0; n=0
def T(label, exp, fn):
    global bad,n
    n+=1
    try: got=fn()
    except Exception as e: got="EXC:%s"%type(e).__name__
    ok=(got==exp); bad += (0 if ok else 1)
    print("%-52s exp=%-5s got=%-5s %s" % (label, exp, got, "OK" if ok else "*** MISMATCH ***"))
print("=== reported regression witnesses (must all be False) ===")
T("le_on_interval u-u^2 <=0 on [0,1]  (value +1/4 at 1/2)", False, lambda: sc.le_on_interval(C(0,1,-1),0,0,1))
T("nonneg_on_half_line u^2-u          (value -1/4 at 1/2)", False, lambda: sc.nonneg_on_half_line(C(0,-1,1)))
T("_ray u-u^2 <=0 on [0,inf)          (value +1/4 at 1/2)", False, lambda: sc._ray(C(0,1,-1),0))
print("=== true statements of the same shapes (no over-rejection) ===")
T("le_on_interval u^2-u <=0 on [0,1]", True, lambda: sc.le_on_interval(C(0,-1,1),0,0,1))
T("le_on_interval -(u-1)^2 <=0 on [0,2] (touch from BELOW)", True, lambda: sc.le_on_interval(C(-1,2,-1),0,0,2))
T("le_on_interval (u-1)^2 <=0 on [0,2]  (touch from ABOVE -> FALSE)", False, lambda: sc.le_on_interval(C(1,-2,1),0,0,2))
T("_ray -(u-5)^2 <=0 on [5,inf)", True, lambda: sc._ray(C(-25,10,-1),5))
T("_ray (u-5)^2 <=0 on [5,inf)   (FALSE)", False, lambda: sc._ray(C(25,-10,1),5))
print("=== IRRATIONAL roots (the class that broke X's old predicate) ===")
T("nonneg_on_half_line u^2-2            (value -2 at 0)", False, lambda: sc.nonneg_on_half_line(C(-2,0,1)))
T("nonneg_on_half_line (u^2-2)^2        (true)", True, lambda: sc.nonneg_on_half_line(C(4,0,-4,0,1)))
T("_ray 2-u^2 <=0 on [0,inf)            (false near 0)", False, lambda: sc._ray(C(2,0,-1),0))
T("_ray u^2-2 <=0 on [2,inf)            (false at u=2)", False, lambda: sc._ray(C(-2,0,1),2))
T("le_on_interval u^2-2 <=0 on [0,1]    (true)", True, lambda: sc.le_on_interval(C(-2,0,1),0,0,1))
T("le_on_interval u^2-2 <=0 on [0,2]    (false; root sqrt2)", False, lambda: sc.le_on_interval(C(-2,0,1),0,0,2))
T("le_on_interval u^2-2 <=0 on [0,3/2]  (false; sqrt2<3/2)", False, lambda: sc.le_on_interval(C(-2,0,1),0,0,sp.Rational(3,2)))
T("le_on_interval u^2-2 <=0 on [3/2,2]  (FALSE: +1/4 at 3/2)", False, lambda: sc.le_on_interval(C(-2,0,1),sp.Rational(3,2),sp.Rational(3,2),2))
print("=== repeated roots, endpoints, zero polynomial, constants ===")
T("le_on_interval (u-1)^3 <=0 on [0,2]  (false: >0 on (1,2])", False, lambda: sc.le_on_interval(C(-1,3,-3,1),0,0,2))
T("le_on_interval -(u-1)^3 <=0 on [0,2] (FALSE: +1 at u=0)", False, lambda: sc.le_on_interval(C(1,-3,3,-1),0,0,2))
T("nonneg_on_half_line zero poly (true)", True, lambda: sc.nonneg_on_half_line(C(0)))
T("_ray zero poly (true)", True, lambda: sc._ray(C(0),0))
T("le_on_interval zero <=0 (true)", True, lambda: sc.le_on_interval(C(0),0,0,1))
T("nonneg_on_half_line constant -1 (false)", False, lambda: sc.nonneg_on_half_line(C(-1)))
T("_ray constant 0 <=0 (true)", True, lambda: sc._ray(C(0),5))
print("\n=== automatic witness check for every expectation labelled FALSE ===")
W=[("u-u^2",lambda x: x-x*x,sp.Rational(1,2)),("u^2-u",lambda x: x*x-x,sp.Rational(1,2)),
   ("u^2-2",lambda x: x*x-2,sp.Rational(1,2)),("(u^2-2)^2 negated n/a",lambda x: 0,0),
   ("2-u^2",lambda x: 2-x*x,sp.Rational(1,2)),("-(u-1)^3",lambda x: -(x-1)**3,sp.Integer(0)),
   ("u^2-2 on[3/2,2]",lambda x: x*x-2,sp.Rational(3,2)),("(u-1)^3",lambda x: (x-1)**3,sp.Rational(3,2)),
   ("(u-1)^2",lambda x: (x-1)**2,sp.Integer(0)),("(u-5)^2",lambda x: (x-5)**2,sp.Integer(6)),
   ("u-5",lambda x: x-5,sp.Integer(6))]
for nm,f,x in W:
    v=f(x)
    print("   %-22s at u=%-5s -> %-8s  %s" % (nm,x,sp.nsimplify(v),
          "wrong sign as claimed" if v!=0 else "(zero: not a witness)"))
print("\n%d tests, %d mismatches" % (n,bad))
sys.exit(0 if bad==0 else 1)
