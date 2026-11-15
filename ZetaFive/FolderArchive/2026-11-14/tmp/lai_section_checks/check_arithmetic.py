"""Exact rational checks of Lai's Table 1 and Fauzan's limiting formulas.

Reads no external data; all formulas are transcribed from Fauzan (4.4)--(4.8),
(5.4)--(5.6), and (5.12)--(5.13). Uses only Python's standard library.
"""
from fractions import Fraction as Q
from math import floor

ALPHA = Q(3, 40)
LAMBDA = Q(37, 40)
H = Q(23, 20)


def ell(x, z):
    return floor(x - z) + floor(x + z) + 1


def intervals(x):
    cuts = {Q(0), Q(1, 2)}
    for u in (x, ALPHA * x):
        f = u - floor(u)
        for z in (f, 1 - f):
            if 0 < z < Q(1, 2):
                cuts.add(z)
    cuts = sorted(cuts)
    return [(a, b, (a + b) / 2) for a, b in zip(cuts, cuts[1:])]


def Gamma(x):
    T = floor(2 * H * x)
    s = H * x - Q(T, 2)
    q = floor(2 * x)
    nplus = x - Q(q, 2)
    integral = Q(0)
    for lo, hi, z in intervals(x):
        b = 3 * ell(ALPHA * x, z)
        integral += (hi - lo) * (T - b) * (T + b - ell(x, z) - 5)
    return integral + s * (2 * T - q - 5) + max(0, s - nplus)


def gamma_discrete(K, p, M):
    N, h, L0, m = 3 * K // 40, 37 * K // 40, 4 * M + 10, (p - 1) // 2
    T, E = divmod(h - L0 + 3 * (N - N // p), m)
    # Actual counts, computed by integer arithmetic independently of ell().
    rows = []
    for a in range(1, m + 1):
        lk = (K - a) // p + (K + a) // p + 1
        ln = (N - a) // p + (N + a) // p + 1
        rows.append((lk, 3 * ln, a))
    rows.sort(reverse=True)
    result, ordinary_halfweights_doubled = 0, []
    dimension = L0
    for i, (lk, b, a) in enumerate(rows):
        extra = int(i < E)
        La = T - b + extra
        assert La >= 0
        dimension += La
        result += La * (T + b + extra - lk - 5)
        ordinary_halfweights_doubled.append(2 * (T + extra) - lk - 4)
    assert dimension == h
    minordinary = min(ordinary_halfweights_doubled)
    for i in range(L0):
        result += min(4 * i + 12 * (N // p) - 2 * (K // p) + 1, minordinary)
    return result, T, E


def Nprofile(x):
    u = LAMBDA * x
    m = floor(2 * u)
    J = m * u - Q(m * (m + 1), 4)
    return 2 * LAMBDA * x * floor(x) - 12 * LAMBDA * x * floor(ALPHA * x) - 2 * J


def expanded_R(x):
    f = x - floor(x)
    g = ALPHA * x - floor(ALPHA * x)
    tau = 2 * H * x - floor(2 * H * x)
    sigma = 2 * x - floor(2 * x)
    eta = 2 * LAMBDA * x - floor(2 * LAMBDA * x)
    F = 4 * LAMBDA + 2 * LAMBDA * f - 12 * LAMBDA * g
    remainder = (tau * (tau - sigma) - max(0, tau - sigma) + eta * (1 - eta)) / 2
    for lo, hi, z in intervals(x):
        A = ell(x, z) - 2 * x
        B = ell(ALPHA * x, z) - 2 * ALPHA * x
        remainder += (hi - lo) * (9 * B * B - 3 * A * B)
    return x * F + remainder


if __name__ == '__main__':
    table = [
        (5, 5000, 1009, -6712, 2779),
        (5, 8000, 2003, -16845, 1183),
        (10, 20000, 2003, 43873, 70527),
        (10, 40000, 4001, 87981, 141426),
        (20, 80000, 4001, 739790, 817708),
        (20, 160000, 8009, 1477486, 1633369),
        (40, 320000, 8009, 7390051, 7661701),
        (40, 640000, 16001, 14799027, 15342855),
    ]
    print('M K p gamma correct_pGamma difference Lai_pGamma')
    for M, K, p, printed_gamma, printed_pGamma in table:
        gamma, T, E = gamma_discrete(K, p, M)
        assert gamma == printed_gamma
        pg = p * Gamma(Q(K, p))
        print(M, K, p, gamma, pg, gamma - pg, printed_pGamma)
    samples = {Q(3) + Q(j, 97) for j in range(5000)}
    samples.update(Q(j, 1) for j in range(3, 201))
    samples.update(Q(20 * j, 23) for j in range(4, 231))
    samples.update(Q(20 * j, 37) for j in range(6, 370))
    samples.update(Q(20 * j, 3) for j in range(1, 31))
    for x in samples:
        assert -Gamma(x) - Nprofile(x) == expanded_R(x), x
    print('Exact R = xF + Q identity verified at', len(samples), 'rational inputs, including floor breakpoints.')
