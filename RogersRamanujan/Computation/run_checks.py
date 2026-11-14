#!/usr/bin/env python3
"""RR127 computation checkpoint driver.

Usage:  python3 run_checks.py [NMAX]     (default 30)

Emits results.json next to this file, containing
  * the canonical fixtures for n <= 6,
  * |A_n| and |D_n| by four independent methods for n <= NMAX,
  * the staircase and T inverse-law checks,
  * exhaustive verification of the BZ82 reference bijection for n <= NMAX,
  * orbit-length statistics for the BZ82 iteration,
  * environment and timing identity.

Nothing here is a proof of an all-n statement: the bijection results are
TESTED_FINITE over the stated range.
"""

import json
import os
import platform
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import rr_core
import bz82
from rr_core import (enumerate_residue, enumerate_gap, count_residue_dp,
                     count_gap_dp, staircase, unstaircase, T, Tinv, is_residue,
                     is_gap, weight)


def all_partitions(n):
    """Generic enumeration of every partition of n (method 5, deliberately naive)."""
    out = []

    def rec(rem, cap, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        for x in range(min(cap, rem), 0, -1):
            acc.append(x)
            rec(rem - x, x, acc)
            acc.pop()

    rec(n, n, [])
    return out


def power_product(N):
    """coeffs of prod_{k>=0} 1/((1-x^{5k+1})(1-x^{5k+4})) up to x^N."""
    t = [0] * (N + 1)
    t[0] = 1
    for part in [x for x in range(1, N + 1) if x % 5 in (1, 4)]:
        for s in range(part, N + 1):
            t[s] += t[s - part]
    return t


def q_series(N):
    """coeffs of sum_{t>=0} x^{t^2}/(x;x)_t  (the B(n) side) up to x^N."""
    t = [0] * (N + 1)
    for k in range(0, N + 1):
        if k * k > N:
            break
        m = N - k * k
        atmost = [0] * (m + 1)
        atmost[0] = 1
        for p in range(1, k + 1):
            for s in range(p, m + 1):
                atmost[s] += atmost[s - p]
        for w in range(m + 1):
            t[w + k * k] += atmost[w]
    return t


def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    R = {}
    R['environment'] = {
        'python': sys.version.split()[0],
        'platform': platform.platform(),
        'nmax': NMAX,
    }
    t0 = time.time()

    # ---- fixtures -------------------------------------------------------
    R['fixtures'] = {n: {'A': [list(p) for p in enumerate_residue(n)],
                         'D': [list(p) for p in enumerate_gap(n)]}
                     for n in range(0, 7)}

    # ---- counts, four methods -------------------------------------------
    prod = power_product(NMAX)
    qs = q_series(NMAX)
    counts = []
    for n in range(0, NMAX + 1):
        generic = all_partitions(n) if n <= 20 else None
        ga = gd = None
        if generic is not None:
            ga = sum(1 for p in generic if all(x % 5 in (1, 4) for x in p))
            gd = sum(1 for p in generic
                     if all(p[i] >= p[i + 1] + 2 for i in range(len(p) - 1)))
        row = {
            'n': n,
            'direct_residue': len(enumerate_residue(n)),
            'direct_gap': len(enumerate_gap(n)),
            'dp_residue': count_residue_dp(n),
            'dp_gap': count_gap_dp(n),
            'product_series': prod[n],
            'q_series': qs[n],
            'generic_filter_residue': ga,
            'generic_filter_gap': gd,
        }
        vals = [row[k] for k in ('direct_residue', 'direct_gap', 'dp_residue',
                                 'dp_gap', 'product_series', 'q_series') if row[k] is not None]
        row['agree'] = len(set(vals)) == 1 and (ga is None or ga == row['dp_residue'])
        counts.append(row)
    R['counts'] = counts
    R['counts_all_agree'] = all(r['agree'] for r in counts)

    # ---- staircase and T inverse laws -----------------------------------
    st_ok = True
    st_detail = []
    for n in range(0, NMAX + 1):
        for lam in enumerate_gap(n):
            k, mu = staircase(lam)
            if len(mu) != k or sum(mu) != n - k * k:
                st_ok = False
                st_detail.append(('weight', n, lam))
            if any(mu[i] < mu[i + 1] for i in range(k - 1)) or any(x < 0 for x in mu):
                st_ok = False
                st_detail.append(('order', n, lam))
            if unstaircase(k, mu) != lam:
                st_ok = False
                st_detail.append(('inverse', n, lam))
            b = T(lam)
            if sum(b) != n or any(x < k for x in b):
                st_ok = False
                st_detail.append(('T-member', n, lam))
            if Tinv(b) != lam:
                st_ok = False
                st_detail.append(('T-inverse', n, lam))
            if any(b[i] != mu[i] + k for i in range(k)):
                st_ok = False
                st_detail.append(('T-mu-bridge', n, lam))
    R['staircase_and_T'] = {'ok': st_ok, 'failures': st_detail[:20]}

    # ---- exhaustive verification of the BZ82 reference map --------------
    bij = []
    bij_ok = True
    for n in range(0, NMAX + 1):
        A = enumerate_residue(n)
        D = enumerate_gap(n)
        fa = {a: bz82.forward(a) for a in A}
        ga = {d: bz82.inverse(d) for d in D}
        steps = [len(bz82.pi_forward(a)[1]) - 1 for a in A]
        checks = {
            'n': n,
            'count': len(A),
            'forward_in_A': all(a in A for a in A),
            'forward_values_in_D': all(d in D for d in fa.values()),
            'forward_injective': len(set(fa.values())) == len(fa),
            'forward_surjective': set(fa.values()) == set(D),
            'inverse_values_in_A': set(ga.values()) == set(A),
            'inverse_left': all(ga[fa[a]] == a for a in A),
            'inverse_right': all(fa[ga[d]] == d for d in D),
            'deterministic': all(bz82.forward(a) == fa[a] for a in A),
            'weight_preserved': all(weight(fa[a]) == n for a in A),
            'max_iteration_steps': max(steps) if steps else 0,
            'total_iteration_steps': sum(steps),
        }
        checks['ok'] = all(v for k, v in checks.items()
                           if k not in ('n', 'count', 'max_iteration_steps',
                                        'total_iteration_steps'))
        bij_ok &= checks['ok']
        bij.append(checks)
        if not checks['ok']:
            break
    R['bz82_bijection'] = {'ok': bij_ok, 'per_weight': bij,
                           'verified_through': bij[-1]['n'] if bij else -1}

    # ---- involution structure -------------------------------------------
    def states(n):
        lo = -1
        while bz82.f(lo) <= n:
            lo -= 1
        out = []
        j = lo
        while True:
            m = bz82.f(j)
            if 0 <= m <= n:
                rem = n - m

                def rec(r, cap, acc):
                    if r == 0:
                        out.append((j, tuple(acc)))
                        return
                    for x in range(min(cap, r), 0, -1):
                        acc.append(x)
                        rec(r - x, x, acc)
                        acc.pop()

                rec(rem, rem, [])
            j += 1
            if j > 0 and bz82.f(j) > n:
                break
        return out

    inv_ok = True
    inv_stats = []
    for n in range(0, min(NMAX, 25) + 1):
        stt = states(n)
        pd = [s for s in stt if bz82.phi_domain(s, n)]
        sd = [s for s in stt if bz82.psi_domain(s, n)]
        ph = all(bz82.phi(bz82.phi(s)) == s for s in pd)
        ps = all(bz82.psi(bz82.psi(s)) == s for s in sd)
        inv_ok &= ph and ps
        inv_stats.append({'n': n, 'states': len(stt), 'phi_domain': len(pd),
                          'psi_domain': len(sd), 'phi_involutive': ph,
                          'psi_involutive': ps})
    R['involution_structure'] = {'ok': inv_ok, 'per_weight': inv_stats}

    R['elapsed_seconds'] = round(time.time() - t0, 3)
    out = os.path.join(HERE, 'results.json')
    with open(out, 'w') as fh:
        json.dump(R, fh, indent=1)
    print('wrote', out, 'in', R['elapsed_seconds'], 's')
    print('counts_all_agree      =', R['counts_all_agree'])
    print('staircase_and_T.ok    =', R['staircase_and_T']['ok'])
    print('bz82_bijection.ok     =', R['bz82_bijection']['ok'],
          'through n =', R['bz82_bijection']['verified_through'])
    print('involution_structure  =', R['involution_structure']['ok'])


if __name__ == '__main__':
    main()
