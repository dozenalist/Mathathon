"""Rational point witness for the fixed D_N^6, zeta(7) transfer.

This bounds the coefficient produced by the original comparison measure,
even if its potential supremum were bounded perfectly. It compares both
the source-derived arithmetic bound and a sharper exact finite-integral
version of the same local valuation certificate at M=200.

It is not a lower bound on actual determinant values or optimal content.
Other comparison measures and better local valuation estimates remain open.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from arithmetic_exact_inner import integral
from single_point_certificate import I, J, PI, ROWS


def main():
    # The nested order is essential for the energy formula below.
    assert sum(ci for _, _, ci in ROWS) == 925000000000
    assert all(ai < bi and ci > 0 for ai, bi, ci in ROWS)
    assert all(a2 < a1 < b1 < b2
               for (a1,b1,_),(a2,b2,_) in zip(ROWS, ROWS[1:]))
    t = I(F(3,4))
    alpha = I(F(3,40))
    lamq = F(37,40)
    lam = I(lamq)
    potential = I(0)
    energy = I(0)
    cumulative = I(0)
    for ai, bi, ci in ROWS:
        a, b, c = I(F(ai,10**12)), I(F(bi,10**12)), I(F(ci,10**12))
        assert t.lo > b.hi
        potential += c * ((t-(a+b)/2+((t-a)*(t-b)).sqrt())/2).log()
        energy += ((cumulative+c)*(cumulative+c)-cumulative*cumulative) * ((b-a)/4).log()
        cumulative += c

    field6 = 2*PI*t.sqrt()+J(t,I(1))-6*J(t,alpha)
    phi6 = 2*potential-field6
    C6 = -2*lam+12*alpha*lam*(1-alpha.log())+3*lam*lam-2*lam*lam*(2*lam).log()
    real_floor = lam*phi6-energy+C6

    M = 200
    exact_inner, logterms, intervals, quadratic = integral(3,7,M)
    assert not logterms and quadratic == 0
    refined_A = F(27071,16000) + 8*lamq/M + exact_inner
    Astar = F(9928298118277006344769,7535670527041937280000)
    original_A = (Astar+7*lamq/M-(F(2923,240)-F(1,4))/M**2+F(32,M**3)
                  +F(751,768))
    assert refined_A < original_A
    refined_budget = I(refined_A)+real_floor
    original_budget = I(original_A)+real_floor
    assert refined_budget.lo > F(9,10)
    assert original_budget.lo > F(9,10)

    result = {
        't':'3/4', 'M':M, 'inner_intervals':intervals,
        'refined_inner_integral_exact':str(exact_inner),
        'refined_arithmetic_coefficient_exact':str(refined_A),
        'original_arithmetic_coefficient_exact':str(original_A),
        'refined_arithmetic_coefficient':I(refined_A).encode(),
        'original_arithmetic_coefficient':I(original_A).encode(),
        'phi6_at_three_quarters':phi6.encode(),
        'real_certificate_coefficient_lower_witness':real_floor.encode(),
        'refined_combined_coefficient_lower_witness':refined_budget.encode(),
        'original_combined_coefficient_lower_witness':original_budget.encode(),
        'proved':(
            'For D_N^6 at zeta(7), M=200, and the original comparison measure, '
            'every valid potential upper constant yields total coefficient >9/10 '
            'even with exact finite integration of the proposed local valuation bounds. '
            'This rules out rescuing this certificate merely by sharpening its '
            'finite-integral and potential enclosures. Better local estimates, '
            'other measures and actual determinant behavior are not excluded.'),
        'method':'Rational interval arithmetic, with exact rational piecewise integration.'
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('_exact')},indent=2))


if __name__ == '__main__':
    main()
