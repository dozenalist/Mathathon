"""Exact finite check of a denominator in the general zeta Hankel family.

Optional dependency: python-flint (tested with version 0.9.0).
Install: python -m pip install python-flint
Run from the repository root:
    python ZetaFive/Computation/check_general_k_denominators.py

The input is fixed at k=2, K=40, N=3, numerator power r=6, and h=37.
We construct the rational matrix G_k(0), then compute

    F_k(0) = scale(K,N,r,h) * det(G_k(0))

using the same functional and scalar as ZetaFive/Lean/Family/Construction.lean
and ZetaFive/Lean/Family/Parameters.lean. The selected prime is p=83.

The assertion v_83(F_2(0)) = -11 is exact rational arithmetic evidence.
Consequently no nonzero rational normalizer whose prime factorization is
supported on primes <= 2h = 74 can make this particular F_2 an integer
polynomial: its constant coefficient would still have valuation -11.

This is NOT a Lean theorem or an asymptotic estimate. A failure at n=1
does not, by itself, disprove an assertion restricted to sufficiently large n.
It does rule out copying an all-n integrality theorem unchanged from k=5.
"""

from __future__ import annotations

import json
from math import factorial, prod

try:
    from flint import fmpq, fmpq_mat, fmpq_poly, fmpz_poly
except ImportError as exc:
    raise SystemExit("Install the optional dependency: python -m pip install python-flint") from exc


def valuation(q: fmpq, p: int) -> int:
    """The exact p-adic valuation of a nonzero rational number."""
    if not q:
        raise ValueError("This check only assigns valuations to nonzero rationals")
    numerator, denominator = q.numerator, q.denominator
    answer = 0
    while numerator % p == 0:
        numerator //= p
        answer += 1
    while denominator % p == 0:
        denominator //= p
        answer -= 1
    return answer


def scalar_normalization(K: int, N: int, r: int, h: int) -> fmpq:
    """Exactly Parameters.scale, including natural subtraction in h-1.

    (K!)^(2h) * 4^(h-1) /
      ((N!)^(2*r*h) * product_{1<=i<=h-1} ((2i)!)^2).
    """
    return fmpq(
        factorial(K) ** (2 * h) * 4 ** max(h - 1, 0),
        factorial(N) ** (2 * r * h)
        * prod(factorial(2 * i) ** 2 for i in range(1, h)),
    )


def constant_hankel_entries(k: int, K: int, N: int, r: int, h: int) -> list[fmpq]:
    """The values mu_{k,0}(D_N(t)^r t^s / D_K(t)), for 0<=s<=2h-2."""
    assert k >= 2 and 0 <= N < K and r >= 1 and h >= 1
    D_N, D_K = fmpz_poly([1]), fmpz_poly([1])
    for j in range(1, K + 1):
        factor = fmpz_poly([j * j, 1])
        D_K *= factor
        if j <= N:
            D_N *= factor

    numerator = fmpq_poly(D_N**r)
    denominator = fmpq_poly(D_K)
    derivative = D_K.derivative()
    harmonic = fmpq(0)
    poles = []
    for j in range(1, K + 1):
        harmonic += fmpq(1, j**k)
        if j > N:
            node = -j * j
            residue = fmpq(D_N(node) ** r, derivative(node))
            pole_constant = -j ** (k - 1) * harmonic - fmpq(1, k - 1) + fmpq(1, 2 * j)
            poles.append([node, residue, pole_constant])

    max_degree = max(0, r * N + 2 * h - 2 - K)
    moments = [
        (-1) ** e
        * fmpq.bernoulli(2 * e + 2)
        * fmpq(factorial(2 * e + k), factorial(k - 1) * factorial(2 * e + 2))
        for e in range(max_degree + 1)
    ]
    entries = []
    for _ in range(2 * h - 1):
        quotient, _remainder = divmod(numerator, denominator)
        value = sum((quotient[e] * moments[e] for e in range(len(quotient))), fmpq(0))
        for pole in poles:
            node, residue, pole_constant = pole
            value += residue * pole_constant
            pole[1] *= node
        entries.append(value)
        numerator = numerator.left_shift(1)
    return entries


def main() -> None:
    k, K, N, r, h, p = 2, 40, 3, 6, 37, 83
    assert h == K - N
    assert p > 2 * h
    entries = constant_hankel_entries(k, K, N, r, h)
    delta_at_zero = fmpq_mat([[entries[i + j] for j in range(h)] for i in range(h)]).det()
    scale = scalar_normalization(K, N, r, h)
    normalized_at_zero = scale * delta_at_zero

    # All factorial arguments in scale are below p, so its valuation is zero.
    assert max(K, N, 2 * (h - 1)) < p
    assert valuation(scale, p) == 0
    assert valuation(delta_at_zero, p) == -11
    assert valuation(normalized_at_zero, p) == -11

    print(json.dumps({
        "status": "EXACT_FINITE_CHECK_NOT_LEAN_VERIFIED",
        "k": k, "K": K, "N": N, "numerator_power": r, "h": h,
        "prime": p,
        "upstream_k5_normalizer_support_bound": 2 * h,
        "valuation_of_scale": valuation(scale, p),
        "valuation_of_delta_at_zero": valuation(delta_at_zero, p),
        "valuation_of_normalized_at_zero": valuation(normalized_at_zero, p),
    }, indent=2))


if __name__ == "__main__":
    main()
