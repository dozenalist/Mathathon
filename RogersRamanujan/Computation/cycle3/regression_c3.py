#!/usr/bin/env python3
"""RR127 cycle 3, direction C.  Fast regression against Computation/bz82.py.

One self-contained script.  It imports the COMMITTED reference map
(../bz82.py, i.e. RogersRamanujan/Computation/bz82.py) and re-checks the
highest-value invariants.  Nothing is re-implemented here except the small
bookkeeping functions needed to read the branch parameters of a step, so a PASS
means "the committed module still does what the claim ledger says".

Checks, one PASS/FAIL line each:

  EX-1  BZ82 p.315 example (1): phi(2; 11,9,8,7,6,1,1,1) = (3; 10,9,7,2,2,2),
        with the printed parameters a = 4, mu = 1 and Case I.
  EX-2  BZ82 p.315 example (2): psi(-2; 15,14,9,9,8,8,8,5,5,4,3,2,1)
        = (-3; 14,10,9,9,8,8,8,4,3,2,2,1), with t0 = 3, m2 = 2, Case I(a).
  EX-3  BZ82 p.315 example (3): forward((4,1)) = (3,2), reached along the
        printed nine-state chain exactly.
  PHI   phi(phi(s)) = s AND phi(s) stays in phi's domain, for every in-domain
        state of weight <= 18.
  PSI   psi(psi(s)) = s AND psi(s) stays in psi's domain, for every in-domain
        state of weight <= 18.
  BIJ   on 0 <= n <= 18: forward maps A_n INTO D_n, injectively, preserving
        weight; inverse maps D_n INTO A_n; inverse(forward(x)) = x for every
        x in A_n and forward(inverse(y)) = y for every y in D_n; and
        |A_n| = |D_n|.
  C2MAX the Case-II maximum-existence criterion, over EVERY Case-II state of
        weight <= 30: the admissible z-set is the down-set {0,..,m}, and it is
        nonempty exactly when k >= 1 and lam(k) <= t+5j-2, and it is empty
        exactly on {0} x B(n) (B = smallest part >= length).
  C2BOX the two created parts in Case II are nonnegative (m >= 0 and
        t+5j-3-m >= 0), and Case I inserts r = L+lam(mu)-5j-t* >= 0 ones.

Machine-readable output goes to a JSON file, not YAML, and only aggregate rows
are written -- no per-state rows.

Usage:  python3 regression_c3.py [--json OUT] [--bound-BIJ N]
Defaults: bound 18 for PHI/PSI/BIJ, bound 30 for C2MAX/C2BOX.
Exit code 0 iff every check passed.  The whole run is intended to be < 20 s.
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import bz82 as B                                       # noqa: E402  committed map
from rr_core import enumerate_residue, enumerate_gap, is_residue, is_gap, weight, T, Tinv  # noqa: E402


# ---------------------------------------------------------------------------
# bookkeeping helpers: read the branch parameters of one phi / psi step
# ---------------------------------------------------------------------------
def pad(lam, x):
    return lam[x - 1] if 1 <= x <= len(lam) else 0


def phi_params(j, lam):
    """(a, L, mu, lam_mu, t*, r, hi, R, admissible, m, case) for one phi step."""
    t = len(lam)
    a = 1
    while 2 * j + a - pad(lam, a) <= 0:
        a += 1
    L = pad(lam, a)
    mu = 2 * j + a - L
    Lmu = pad(lam, mu)
    tstar = t + (1 if a > t else 0) + (1 if mu > t else 0)
    r = L + Lmu - 5 * j - tstar
    hi, R = a + 2 * j - 2, t + 5 * j - 2
    adm = [z for z in range(0, hi + 1) if z + pad(lam, a + 2 * j - 1 - z) <= R]
    case = 'I' if L + Lmu >= 5 * j + tstar else 'II'
    m = max(adm) if adm else None
    return dict(a=a, L=L, mu=mu, lam_mu=Lmu, tstar=tstar, r=r, hi=hi, R=R,
                admissible=adm, m=m, case=case, t=t)


def largest_mod(lam, rr):
    return max([0] + [x for x in lam if x % 5 == rr])


def constituents(n):
    """Every signed state (j, lam) in X(n)."""
    out = []
    j = 0
    while B.f(j) <= n or B.f(-j) <= n:
        for jj in ({j, -j} if j else {0}):
            if B.f(jj) <= n:
                out.extend((jj, lam) for lam in _parts(n - B.f(jj)))
        j += 1
    return out


def _parts(n, cap=None):
    if cap is None:
        cap = n if n > 0 else 1
    if n == 0:
        return [()]
    out = []
    for p in range(min(n, cap), 0, -1):
        out.extend((p,) + rest for rest in _parts(n - p, p))
    return out


def in_B(lam):
    k = len(lam)
    return all(x >= k for x in lam)


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------
def check_ex1():
    st = (2, (11, 9, 8, 7, 6, 1, 1, 1))
    got = B.phi(st)
    want = (3, (10, 9, 7, 2, 2, 2))
    p = phi_params(*st)
    ok = (got == want and p['a'] == 4 and p['mu'] == 1 and p['case'] == 'I'
          and p['r'] == 0)
    return dict(ok=ok, input=[2, list(st[1])], got=[got[0], list(got[1])],
                want=[3, [10, 9, 7, 2, 2, 2]],
                printed_a=4, printed_mu=1, printed_case='I',
                a=p['a'], mu=p['mu'], case=p['case'], ones_inserted=p['r'])


def check_ex2():
    st = (-2, (15, 14, 9, 9, 8, 8, 8, 5, 5, 4, 3, 2, 1))
    got = B.psi(st)
    want = (-3, (14, 10, 9, 9, 8, 8, 8, 4, 3, 2, 2, 1))
    lam = st[1]
    t0 = sum(1 for x in lam if x % 5 == 0)
    m2, m3, m0 = largest_mod(lam, 2), largest_mod(lam, 3), largest_mod(lam, 0)
    sub = 'a' if 5 * t0 + 5 * st[0] - 3 >= m2 else 'b'
    ok = (got == want and t0 == 3 and m2 == 2 and sub == 'a' and m3 == 8)
    return dict(ok=ok, input=[-2, list(lam)], got=[got[0], list(got[1])],
                want=[-3, [14, 10, 9, 9, 8, 8, 8, 4, 3, 2, 2, 1]],
                printed_t0=3, printed_m2=2, printed_case='I(a)',
                t0=t0, m2=m2, sub=sub, m0=m0, m3=m3)


CHAIN = [(0, (4, 1)), (1, (1, 1, 1)), (0, (2, 1, 1, 1)), (-1, (1, 1)),
         (0, (3, 1, 1)), (1, (2, 1)), (0, (2, 2, 1)), (1, (3,)), (0, (3, 2))]


def check_ex3():
    st, trace = (0, (4, 1)), [(0, (4, 1))]
    for step in range(200):
        st = B.phi(st) if step % 2 == 0 else B.psi(st)
        trace.append(st)
        if st[0] == 0 and in_B(st[1]):
            break
    ok = (tuple(trace) == tuple(CHAIN) and st == (0, (3, 2))
          and Tinv((3, 2)) == (4, 1) and B.forward((4, 1)) == (4, 1))
    return dict(ok=ok, chain_matches=(tuple(trace) == tuple(CHAIN)),
                steps=len(trace) - 1, got_chain=[[j, list(l)] for j, l in trace],
                printed_chain=[[j, list(l)] for j, l in CHAIN],
                endpoint=[0, [3, 2]], Tinv_of_endpoint=list(Tinv((3, 2))),
                forward_of_41=list(B.forward((4, 1))))


def _domain_states(bound, which):
    dom = B.phi_domain if which == 'phi' else B.psi_domain
    inv = B.phi if which == 'phi' else B.psi
    n_states = 0
    for n in range(bound + 1):
        for st in constituents(n):
            if not dom(st, n):
                continue
            n_states += 1
            img = inv(st)
            if img == st:
                return dict(ok=False, checked=n_states,
                            detail='involution fixed point', state=[st[0], list(st[1])])
            if not dom(img, n):
                return dict(ok=False, checked=n_states,
                            detail='image left the domain',
                            state=[st[0], list(st[1])], image=[img[0], list(img[1])])
            if B.state_weight(img) != n:
                return dict(ok=False, checked=n_states, detail='weight broken',
                            state=[st[0], list(st[1])])
            if inv(img) != st:
                return dict(ok=False, checked=n_states, detail='involution broken',
                            state=[st[0], list(st[1])], image=[img[0], list(img[1])],
                            back=[inv(img)[0], list(inv(img)[1])])
    return dict(ok=True, checked=n_states)


def check_phi(bound):
    r = _domain_states(bound, 'phi')
    r['bound'] = bound
    return r


def check_psi(bound):
    r = _domain_states(bound, 'psi')
    r['bound'] = bound
    return r


def check_bij(bound):
    rows = []
    total = 0
    for n in range(bound + 1):
        A, D = enumerate_residue(n), enumerate_gap(n)
        if len(A) != len(D):
            return dict(ok=False, detail='|A_n| != |D_n| at n=%d (%d vs %d)'
                        % (n, len(A), len(D)))
        seen = set()
        for x in A:
            y = B.forward(x)
            if not is_gap(y):
                return dict(ok=False, detail='forward landed outside D_n',
                            n=n, arg=list(x), image=list(y))
            if weight(y) != n:
                return dict(ok=False, detail='forward broke the weight', n=n,
                            arg=list(x), image=list(y))
            if y in seen:
                return dict(ok=False, detail='forward not injective', n=n,
                            arg=list(x), image=list(y))
            seen.add(y)
            if B.inverse(y) != x:
                return dict(ok=False, detail='inverse . forward != id', n=n,
                            arg=list(x), image=list(y),
                            back=list(B.inverse(y)))
        if seen != set(D):
            return dict(ok=False, detail='forward image != D_n', n=n,
                        missing=len(set(D) - seen))
        for y in D:
            x = B.inverse(y)
            if not is_residue(x):
                return dict(ok=False, detail='inverse landed outside A_n', n=n,
                            arg=list(y), image=list(x))
            if weight(x) != n:
                return dict(ok=False, detail='inverse broke the weight', n=n,
                            arg=list(y), image=list(x))
            if B.forward(x) != y:
                return dict(ok=False, detail='forward . inverse != id', n=n,
                            arg=list(y), image=list(x))
        rows.append({'n': n, 'A': len(A), 'D': len(D)})
        total += len(A)
    return dict(ok=True, bound=bound, objects=total, per_weight=rows)


def check_c2max(bound):
    stats = dict(checked=0, nonempty=0, empty=0, empty_in_domain=0,
                 empty_out_of_domain=0, downset_violations=0,
                 criterion_violations=0, domain_mismatch=0)
    for n in range(bound + 1):
        for st in constituents(n):
            p = phi_params(*st)
            if p['case'] != 'II':
                continue
            stats['checked'] += 1
            adm = p['admissible']
            # the admissible set is an initial segment of z
            if adm != list(range(0, len(adm))):
                stats['downset_violations'] += 1
            # the sharp criterion: nonempty <=> k >= 1 and lam(k) <= R
            crit = (p['t'] + 2 * st[0] >= 1 and pad(st[1], p['t'] + 2 * st[0]) <= p['R'])
            if crit != bool(adm):
                stats['criterion_violations'] += 1
            if adm:
                stats['nonempty'] += 1
                if p['m'] != max(adm):
                    stats['downset_violations'] += 1
            else:
                stats['empty'] += 1
                excluded = (st[0] == 0 and in_B(st[1]))
                if excluded:
                    stats['empty_out_of_domain'] += 1
                else:
                    stats['empty_in_domain'] += 1
            # the domain claim: empty exactly on {0} x B(n)
            if bool(adm) == (st[0] == 0 and in_B(st[1])):
                stats['domain_mismatch'] += 1
    ok = (stats['downset_violations'] == 0 and stats['criterion_violations'] == 0
          and stats['empty_in_domain'] == 0 and stats['domain_mismatch'] == 0)
    stats['ok'] = ok
    stats['bound'] = bound
    return stats


def check_c2box(bound):
    stats = dict(case_II=0, case_I=0, p2_zero=0, m_zero=0, r_zero=0,
                 negative_part=0, negative_ones=0)
    for n in range(bound + 1):
        for st in constituents(n):
            p = phi_params(*st)
            if p['case'] == 'I':
                stats['case_I'] += 1
                if p['r'] < 0:
                    stats['negative_ones'] += 1
                if p['r'] == 0:
                    stats['r_zero'] += 1
            else:
                if p['admissible']:
                    stats['case_II'] += 1
                    m = p['m']
                    p1, p2 = m, p['t'] + 5 * st[0] - 3 - m
                    if p1 < 0 or p2 < 0:
                        stats['negative_part'] += 1
                    if p2 == 0:
                        stats['p2_zero'] += 1
                    if m == 0:
                        stats['m_zero'] += 1
    stats['ok'] = (stats['negative_part'] == 0 and stats['negative_ones'] == 0)
    stats['bound'] = bound
    return stats


# ---------------------------------------------------------------------------
def main(argv):
    json_out = os.path.join(HERE, 'results_regression_c3.json')
    small = 18
    big = 30
    args = list(argv[1:])
    if '--json' in args:
        json_out = args[args.index('--json') + 1]
    if '--bound-BIJ' in args:
        small = int(args[args.index('--bound-BIJ') + 1])

    t0 = time.time()
    plan = [
        ('EX-1', 'BZ82 p.315 example (1), phi: a=4 mu=1 Case I', lambda: check_ex1()),
        ('EX-2', 'BZ82 p.315 example (2), psi: t0=3 m2=2 Case I(a)', lambda: check_ex2()),
        ('EX-3', 'BZ82 p.315 example (3), nine-state chain, pi((4,1))=(3,2)', lambda: check_ex3()),
        ('PHI', 'phi^2 = id and closure on X(n)\\{0}xB(n), n <= %d' % small,
         lambda: check_phi(small)),
        ('PSI', 'psi^2 = id and closure on X(n)\\{0}xA(n), n <= %d' % small,
         lambda: check_psi(small)),
        ('BIJ', 'forward/inverse are mutually inverse bijections A_n <-> D_n, n <= %d' % small,
         lambda: check_bij(small)),
        ('C2MAX', 'Case-II maximum exists iff k>=1 and lam(k)<=R, n <= %d' % big,
         lambda: check_c2max(big)),
        ('C2BOX', 'created parts/inserted ones are nonnegative, n <= %d' % big,
         lambda: check_c2box(big)),
    ]
    results = {}
    lines = []
    nfail = 0
    for name, desc, fn in plan:
        t1 = time.time()
        try:
            res = fn()
        except Exception as exc:                  # a raised error is a FAIL
            res = dict(ok=False, error=repr(exc))
        res['seconds'] = round(time.time() - t1, 3)
        res['description'] = desc
        results[name] = res
        if not res.get('ok'):
            nfail += 1
            detail = res.get('detail') or res.get('error') or ''
            lines.append('%-6s FAIL  %s  %s' % (name, desc, detail))
        else:
            extra = []
            for k in ('checked', 'objects', 'case_II', 'case_I', 'steps', 'a', 'mu'):
                if k in res:
                    extra.append('%s=%s' % (k, res[k]))
            lines.append('%-6s PASS  %s  (%s, %.2fs)'
                         % (name, desc, ' '.join(extra), res['seconds']))

    elapsed = time.time() - t0
    print('RR127 cycle 3 fast regression against RogersRamanujan/Computation/bz82.py')
    print('')
    for ln in lines:
        print(ln)
    print('')
    verdict = 'PASS' if nfail == 0 else 'FAIL'
    print('TOTAL: %s  %d/%d checks passed in %.2f s'
          % (verdict, len(plan) - nfail, len(plan), elapsed))
    payload = dict(script='regression_c3.py', verdict=verdict, checks=nfail,
                   checks_passed=len(plan) - nfail, elapsed_seconds=round(elapsed, 3),
                   bounds=dict(involutions=small, case_II=big),
                   results=results)
    with open(json_out, 'w') as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('wrote %s' % json_out)
    return 0 if nfail == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
