"""Exact arithmetic in Q(sqrt(d1),...,sqrt(dm)), d_i pairwise coprime squarefree.

Representation: a field element is a tuple of Fractions, one per element of the
multiplicative basis  {prod_{i in S} d_i : S subset of radicands}.  The basis is
closed under multiplication (sqrt(a)*sqrt(b) = k*sqrt(s) with ab = k^2 s and s in
the basis), so no division is ever needed: we only compare squared distances to 1.
"""
from fractions import Fraction
from itertools import combinations


def squarefree_split(n):
    """n > 0 -> (k, s) with n = k*k*s and s squarefree."""
    n = abs(int(n))
    k, s, m, p = 1, 1, n, 2
    while p * p <= m:
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        if e:
            k *= p ** (e // 2)
            if e % 2:
                s *= p
        p += 1 if p == 2 else 2
    if m > 1:
        s *= m
    return k, s


class Field:
    """Q(sqrt(d) : d in radicands). radicands must be pairwise coprime, squarefree, > 1."""

    def __init__(self, radicands):
        rs = sorted(set(int(r) for r in radicands))
        for r in rs:
            assert r > 1 and squarefree_split(r) == (1, r), f"{r} not squarefree"
        for a, b in combinations(rs, 2):
            assert squarefree_split(a * b)[1] == a * b, f"{a},{b} not coprime"
        self.rs = rs
        basis = [1]
        for r in range(1, len(rs) + 1):
            for comb in combinations(rs, r):
                v = 1
                for c in comb:
                    v *= c
                basis.append(v)
        self.basis = sorted(set(basis))
        self.idx = {b: i for i, b in enumerate(self.basis)}
        # closure table: basis[i]*basis[j] = qty * basis[k]
        self.table = {}
        for i, a in enumerate(self.basis):
            for j, b in enumerate(self.basis):
                k, s = squarefree_split(a * b)
                assert s in self.idx, f"basis not closed: sqrt({a*b})"
                self.table[(i, j)] = (k, self.idx[s])
        self.zero = tuple(Fraction(0) for _ in self.basis)
        self.one = tuple(Fraction(1) if b == 1 else Fraction(0) for b in self.basis)

    # --- constructors -------------------------------------------------
    def rat(self, q):
        q = Fraction(q)
        return tuple(q if b == 1 else Fraction(0) for b in self.basis)

    def sqrt(self, d):
        """sqrt(d) for a squarefree d already in the basis."""
        d = int(d)
        assert d in self.idx, f"sqrt({d}) outside the field"
        return tuple(Fraction(1) if b == d else Fraction(0) for b in self.basis)

    # --- ring operations ----------------------------------------------
    def add(self, x, y):
        return tuple(a + b for a, b in zip(x, y))

    def sub(self, x, y):
        return tuple(a - b for a, b in zip(x, y))

    def neg(self, x):
        return tuple(-a for a in x)

    def mul(self, x, y):
        n = len(self.basis)
        out = [Fraction(0)] * n
        for i, a in enumerate(x):
            if not a:
                continue
            for j, b in enumerate(y):
                if not b:
                    continue
                k, m = self.table[(i, j)]
                out[m] += a * b * k
        return tuple(out)

    def is_zero(self, x):
        return all(a == 0 for a in x)

    def eq(self, x, y):
        return all(a == b for a, b in zip(x, y))

    def __repr__(self):
        return f"Field({self.rs})"


def parse(field, expr):
    """Parse a small exact expression into a field element.

    expr is a pair (coeff_list, ) design: we accept a dict {basis_value: Fraction}
    plus a helper for numbers of the shape a + b*sqrt(d)."""
    out = list(field.zero)
    for b, c in expr.items():
        out[field.idx[int(b)]] += Fraction(c)
    return tuple(out)
