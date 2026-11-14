#!/usr/bin/env python3
"""Self-audit runner: drive X's exact_sign via the Adapter through the SAME families
(random + probe-targeted) that x_family_check.py uses against other checkers."""
import sys, random
sys.path.insert(0,'.'); sys.path.insert(0,'..')
import sympy as sp
from fractions import Fraction as Fr
import x_family_check as F
from x_selftest_exact_sign import Adapter as sc

u = sp.Symbol('u')
def run(n=60, seed=1):
    rng = random.Random(seed)
    pool = [Fr(k,2) for k in range(0,5)] + [Fr(1,4),Fr(3,4),Fr(5,4),Fr(7,3)]
    bad = 0
    for _ in range(n):
        k = rng.choice([1,2,3,4]); rs=[rng.choice(pool) for _ in range(k)]
        es = [rng.choice([1,2]) for _ in range(k)]; c = rng.choice([1,-1])
        p = sp.Integer(c)
        for r,e in zip(rs,es): p = sp.expand(p*(u-sp.Rational(r.numerator,r.denominator))**e)
        cs = F.to_coeffs(p,u)
        for name, truth, call in [
            ("le", F.truth_le_interval(p,0,1,u), lambda: sc.le_on_interval(cs,sp.Integer(0),sp.Integer(0),sp.Integer(1))),
            ("nn", F.truth_ge_half_line(p,u),    lambda: sc.nonneg_on_half_line(cs)),
            ("ray",F.truth_le_ray(p,0,u),        lambda: sc._ray(cs,sp.Integer(0)))]:
            try: got = call()
            except Exception as ex: got = "EXC:%s"%type(ex).__name__
            if got != truth:
                bad += 1
                if bad <= 4: print("   MISMATCH %-4s p=%-40s truth=%-5s got=%s" % (name,str(sp.factor(p))[:40],truth,got))
    print("  random family: %d queries, %d wrong" % (3*n,bad))
    tgt=0
    for probes in [(0,sp.Rational(1,2),1),(0,1,2)]:
        for c in (1,-1):
            for es in ([2,2,2],[2,2,1],[1,2,2]):
                p=sp.Integer(c)
                for r,e in zip(probes,es): p=sp.expand(p*(u-sp.Rational(r))**e)
                cs=F.to_coeffs(p,u)
                if probes[1]==sp.Rational(1,2):
                    truth=F.truth_le_interval(p,0,1,u)
                    try: got=sc.le_on_interval(cs,sp.Integer(0),sp.Integer(0),sp.Integer(1))
                    except Exception as ex: got="EXC"
                else:
                    truth=F.truth_le_ray(p,0,u)
                    try: got=sc._ray(cs,sp.Integer(0))
                    except Exception as ex: got="EXC"
                if got!=truth:
                    tgt+=1; print("   MISMATCH targeted p=%-40s truth=%-5s got=%s"%(str(sp.factor(p))[:40],truth,got))
    print("  probe-targeted family: 12 queries, %d wrong" % tgt)
    return bad+tgt
if __name__=="__main__":
    print("X exact_sign.py self-audit on the families that break probe-based checkers:")
    sys.exit(0 if run()==0 else 1)
