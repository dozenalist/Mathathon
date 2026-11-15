"""Exact, reproducible finite checks for the zeta(5) to zeta(7) exploration.

Source: A. Fauzan, ZETA5_IS_IRRATIONAL.pdf (2026-09-17), equations
(2.2)--(2.5), (5.19)--(5.20), (6.4). The s=7 formulas are independently
derived in this exploration. Small K below are illustrative examples, NOT
instances of the paper's asymptotic theorem (which requires K divisible by 40
and a much larger cutoff). No third-party Python packages are required.
"""
from fractions import Fraction as Q
from math import comb, factorial, gcd, lcm
from pathlib import Path
import json
from functools import lru_cache


@lru_cache(None)
def bernoulli(n):
    b = [Q(1)]
    for m in range(1, n + 1):
        b.append(-sum(Q(comb(m + 1, k)) * b[k] for k in range(m)) / (m + 1))
    return b[n]


def mu_monomial(s, e):
    return Q((-1) ** e * factorial(2 * e + s),
             factorial(2 * e + 2) * factorial(s - 1)) * bernoulli(2 * e + 2)


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def mul(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def evaluate(p, x):
    z = Q(0)
    for a in reversed(p):
        z = z * x + a
    return z


def divmod_poly(a, b):
    a = a[:]
    if len(a) < len(b):
        return [Q(0)], a
    out = [Q(0)] * (len(a) - len(b) + 1)
    while len(a) >= len(b) and any(a):
        d = len(a) - len(b)
        c = a[-1] / b[-1]
        out[d] = c
        for i, v in enumerate(b):
            a[i + d] -= c * v
        trim(a)
    return trim(out), a


def D(n):
    p = [Q(1)]
    for j in range(1, n + 1):
        p = mul(p, [Q(j*j), Q(1)])
    return p


def matrix_affine(s, K, N):
    h = K - N
    denominator = D(K)
    numerator = [Q(1)]
    for _ in range(6):
        numerator = mul(numerator, D(N))
    dprime = [i * denominator[i] for i in range(1, len(denominator))]
    entries = []
    for e in range(2*h - 1):
        num = [Q(0)] * e + numerator
        quotient, _ = divmod_poly(num, denominator)
        c = sum(a * mu_monomial(s, i) for i, a in enumerate(quotient))
        xcoef = Q(0)
        for j in range(1, K + 1):
            residue = evaluate(num, -j*j) / evaluate(dprime, -j*j)
            harmonic = sum(Q(1, v**s) for v in range(1, j + 1))
            c += residue * (-j**(s - 1) * harmonic - Q(1, s - 1) + Q(1, 2*j))
            xcoef += residue * j**(s - 1)
        entries.append([c, xcoef])
    return [[entries[i+j] for j in range(h)] for i in range(h)]


def det(a):
    a = [r[:] for r in a]
    d = Q(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            d = -d
        v = a[k][k]
        d *= v
        for i in range(k+1, len(a)):
            r = a[i][k] / v
            for j in range(k+1, len(a)):
                a[i][j] -= r * a[k][j]
    return d


def determinant_polynomial(a):
    h = len(a)
    values = [det([[c + j*x for c, x in row] for row in a]) for j in range(h+1)]
    # Newton forward-difference interpolation in the binomial basis.
    result = [Q(0)] * (h+1)
    basis = [Q(1)]
    differences = values[:]
    for k in range(h+1):
        coefficient = differences[0] / factorial(k)
        for i, b in enumerate(basis):
            result[i] += coefficient * b
        differences = [b-a for a,b in zip(differences, differences[1:])]
        basis = mul(basis, [Q(-k), Q(1)])
    assert all(evaluate(result, j) == values[j] for j in range(h+1))
    return trim(result)


def scalar(K, N):
    h = K-N
    num = factorial(K)**(2*h) * 4**(h-1)
    den = factorial(N)**(12*h)
    for i in range(1, h):
        den *= factorial(2*i)**2
    return Q(num, den)


def valuation(q, p):
    if not q:
        return None
    a, b = q.numerator, q.denominator
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    while b % p == 0:
        b //= p
        v -= 1
    return v


def polynomial_record(p):
    denominator = lcm(*(x.denominator for x in p))
    numerators = [int(x * denominator) for x in p]
    numerator_gcd = gcd(*numerators)
    return {
        "coefficients_low_to_high": [str(x) for x in p],
        "content": str(Q(numerator_gcd, denominator)),
        "primitive_integer_normalization": str(Q(denominator, numerator_gcd)),
        "gauss_valuations": {str(q): min(valuation(x, q) for x in p if x)
                             for q in [2,3,5,7,11,13,17,19]},
    }


def determinant_valuation_modular(a, p, precision=400):
    """Exact v_p(det(a)) when enough p-adic precision remains.

    Coefficients are exact Fractions. After clearing a common p power,
    row extraction and unit-pivot elimination are performed modulo p^precision.
    Each p-power row extraction reduces precision explicitly. A finite answer
    with remaining precision > 0 certifies the valuation; no floating point.
    """
    n = len(a)
    initial_precision = precision
    shift = max(0, -min(valuation(x,p) for row in a for x in row if x))
    modulus = p**precision
    b = [[int((x*p**shift).numerator) * pow(int((x*p**shift).denominator), -1, modulus) % modulus
          for x in row] for row in a]
    accumulated = 0
    for k in range(n):
        candidates = [(valuation(Q(b[i][j]),p), i, j)
                      for i in range(k,n) for j in range(k,n) if b[i][j]]
        if not candidates:
            raise ArithmeticError('Insufficient p-adic precision')
        v,i,j = min(candidates)
        b[k],b[i] = b[i],b[k]
        if j != k:
            for row in b:
                row[k],row[j] = row[j],row[k]
        accumulated += v
        precision -= v
        assert precision > 0
        modulus = p**precision
        power = p**v
        for j in range(k,n):
            assert b[k][j] % power == 0
            b[k][j] = (b[k][j] // power) % modulus
        inv = pow(b[k][k], -1, modulus)
        for i in range(k+1,n):
            factor = b[i][k] * inv % modulus
            for j in range(k+1,n):
                b[i][j] = (b[i][j] - factor*b[k][j]) % modulus
    return {"valuation":accumulated-shift*n,"remaining_precision":precision,
            "initial_precision":initial_precision,"entry_scaling_power":shift}


def old_outer_bound(K,N,p):
    v = K-p*(K//p)
    u = max(0,N+v-p+1)
    t = min(N,v)+u
    r = max(0,K+4*N-2*p+2)
    if K<2*p:
        return -7*(K-p)+6*t-1-min(r,p-1-N+u)
    return -7*(K-p)+3+12*N+5*t-min(r,p+u)


def main():
    astar = Q(9928298118277006344769, 7535670527041937280000)
    lam = Q(37,40)
    u = -Q(2733991,2000000)
    a200 = astar + 7*lam/200 - (Q(2923,240)-Q(1,4))/200**2 + Q(32,200**3)
    out = {
        "source": "https://zenodo.org/records/22826419",
        "scope": "Exact finite examples and arithmetic constants, no asymptotic inference from small K.",
        "moments": {str(s): [str(mu_monomial(s,e)) for e in range(6)] for s in [5,7]},
        "constants": {name: {"exact":str(v), "decimal":float(v)} for name,v in {
            "Astar":astar, "U":u, "A200":a200, "A200_plus_U":a200+u,
            "inner_extra_cost_M200":2*lam*(Q(1,3)-Q(1,200)),
            "A200_plus_U_plus_inner_extra":a200+u+2*lam*(Q(1,3)-Q(1,200)),
        }.items()},
        "examples": [],
        "moment_valuation_first_negative": {},
    }
    for p in [7,11,13]:
        out["moment_valuation_first_negative"][str(p)] = {
            str(s): next(e for e in range(5*p) if valuation(mu_monomial(s,e),p)<0)
            for s in [5,7]
        }
    for K,N in [(1,0),(2,0),(3,0),(4,0),(4,1),(5,1),(6,1),(8,1)]:
        record = {"K":K, "N":N, "h":K-N, "S":str(scalar(K,N)), "s":{}}
        for s in [5,7]:
            a = matrix_affine(s,K,N)
            delta = determinant_polynomial(a)
            f = [v * scalar(K,N) for v in delta]
            record["s"][str(s)] = {"Delta":polynomial_record(delta), "F":polynomial_record(f)}
            if K<=2:
                record["s"][str(s)]["matrix_entries_constant_X"] = [[[str(x) for x in e] for e in row] for row in a]
        out["examples"].append(record)
    # Verify modular determinant valuation against exact determinants above.
    for K,N in [(2,0),(4,1),(6,1)]:
        for s in [5,7]:
            a = [[x[0] for x in row] for row in matrix_affine(s,K,N)]
            d = det(a)
            for p in [7,23,29]:
                assert determinant_valuation_modular(a,p)["valuation"] == valuation(d,p)
    out["K40_local_checks"] = {}
    for p in [17,19,23,29,31,37]:
        assert p >= 7 and p <= 40 < 3*p and p*p > 2*40
        assert 2*3 < p and 5*3 <= 2*p-2  # All conditions in (4.9).
    for s in [5,7]:
        a = [[x[0] for x in row] for row in matrix_affine(s,40,3)]
        exact_d = det(a)
        out["K40_local_checks"][str(s)] = {
            str(p): {"Delta_at_X0":determinant_valuation_modular(a,p),
                     "independent_exact_rational_determinant_valuation":valuation(exact_d,p),
                     "paper_zeta5_outer_lower_bound":old_outer_bound(40,3,p)}
            for p in [17,19,23,29,31,37]
        }
        for rec in out["K40_local_checks"][str(s)].values():
            assert rec["Delta_at_X0"]["valuation"] == rec["independent_exact_rational_determinant_valuation"]
        out["K40_local_checks"][str(s)]["exact_determinant_size"] = {
            "numerator_bits":exact_d.numerator.bit_length(),
            "denominator_bits":exact_d.denominator.bit_length(),
        }
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({"moments":out["moments"],"constants":out["constants"],
                      "moment_valuation_first_negative":out["moment_valuation_first_negative"],
                      "K40_local_checks":out["K40_local_checks"],
                      "example_contents":[{"K":r["K"],"N":r["N"],"contents":{s:d["F"]["content"] for s,d in r["s"].items()}} for r in out["examples"]]},indent=2))


if __name__ == '__main__':
    main()
