"""Exact Fourier algebra for Gaussian polynomials on R^n x R^n.

No third-party packages are required.  A polynomial is a dictionary from
(a,b,c) to a Fraction, denoting U^a V^b W^c, where
U=pi*|x|^2, V=pi*|y|^2, W=pi*<x,y>.

If f(x,y)=P(U,V,W)*exp(-pi*(|x|^2+|y|^2)), then
fourier(P,n) is the polynomial multiplying the same Gaussian in f-hat,
for the Fourier convention exp(-2*pi*i*<z,xi>).
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial
from typing import Iterable

Exponent = tuple[int, int, int]
Polynomial = dict[Exponent, Fraction]


def clean(p: Polynomial) -> Polynomial:
    return {m: Fraction(c) for m, c in p.items() if c}


def add(p: Polynomial, q: Polynomial, scale: Fraction = Fraction(1)) -> Polynomial:
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, Fraction(0)) + scale * c
    return clean(out)


def multiply(p: Polynomial, q: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for a, ca in p.items():
        for b, cb in q.items():
            m = tuple(x + y for x, y in zip(a, b))
            out[m] = out.get(m, Fraction(0)) + ca * cb
    return clean(out)


def derivative(p: Polynomial, variable: int) -> Polynomial:
    out: Polynomial = {}
    for m, coeff in p.items():
        if m[variable]:
            powers = list(m)
            powers[variable] -= 1
            out[tuple(powers)] = coeff * m[variable]
    return clean(out)


def evaluate(p: Polynomial, u, v, w):
    return sum(c * u**a * v**b * w**d for (a, b, d), c in p.items())


def laplacian(p: Polynomial, n: int = 4) -> Polynomial:
    """Apply the Cartesian Laplacian in scaled coordinates sqrt(pi)*(x,y).

    On Gram polynomials this is
      D=4U*dUU+4V*dVV+(U+V)*dWW+4W*(dUW+dVW)+2n*(dU+dV).
    Every application lowers the Gram degree by one.
    """
    out: Polynomial = {}

    def insert(m: Exponent, c: Fraction):
        out[m] = out.get(m, Fraction(0)) + c

    for (a, b, c), coeff in p.items():
        if a:
            insert((a - 1, b, c), coeff * 2 * a * (2 * a + n - 2 + 2 * c))
        if b:
            insert((a, b - 1, c), coeff * 2 * b * (2 * b + n - 2 + 2 * c))
        if c >= 2:
            insert((a + 1, b, c - 2), coeff * c * (c - 1))
            insert((a, b + 1, c - 2), coeff * c * (c - 1))
    return clean(out)


def fourier(p: Polynomial, n: int = 4) -> Polynomial:
    """Return the exact Fourier polynomial; works for mixed Gram degrees.

    On a homogeneous Gram polynomial P_k of degree k, the action is
       (-1)^k * exp(-D/4) P_k.
    The exponential terminates after k+1 terms.
    """
    out: Polynomial = {}
    by_degree: dict[int, Polynomial] = {}
    for m, c in p.items():
        by_degree.setdefault(sum(m), {})[m] = c
    for degree, component in by_degree.items():
        current = component
        for j in range(degree + 1):
            out = add(out, current, Fraction((-1) ** (degree + j), 4**j * factorial(j)))
            current = laplacian(current, n)
    return clean(out)


def monomials(max_degree: int) -> Iterable[Exponent]:
    for degree in range(max_degree + 1):
        for a in range(degree + 1):
            for b in range(degree - a + 1):
                yield a, b, degree - a - b


def symmetric_basis(max_degree: int) -> list[tuple[str, Polynomial]]:
    """Swap-invariant, W-even polynomials of Gram degree <= max_degree.

    This degree is half the Cartesian degree.  In Cohn--de Laat--Salmon
    Section 5.2, the parameter d allows max_degree=2*d here.
    """
    result = []
    for a, b, c in monomials(max_degree):
        if c % 2 or a < b:
            continue
        p = {(a, b, c): Fraction(1)}
        if a != b:
            p[(b, a, c)] = Fraction(1)
        result.append((f"sym({a},{b},{c})", p))
    return result


def format_polynomial(p: Polynomial) -> str:
    if not p:
        return "0"
    pieces = []
    for powers in sorted(p, key=lambda m: (sum(m), m)):
        coefficient = p[powers]
        factors = [str(coefficient)]
        for name, power in zip(("U", "V", "W"), powers):
            if power:
                factors.append(name if power == 1 else f"{name}^{power}")
        pieces.append("*".join(factors))
    return " + ".join(pieces).replace("+ -", "- ")


def rational_rank(rows: list[list[int | Fraction]]) -> int:
    """Exact row rank by Gaussian elimination over Q, for small diagnostics."""
    if not rows:
        return 0
    a = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((j for j in range(rank, len(a)) if a[j][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        denominator = a[rank][column]
        a[rank] = [x / denominator for x in a[rank]]
        for j in range(rank + 1, len(a)):
            multiplier = a[j][column]
            if multiplier:
                a[j] = [x - multiplier * y for x, y in zip(a[j], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank
