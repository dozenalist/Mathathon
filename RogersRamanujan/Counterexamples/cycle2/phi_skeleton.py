#!/usr/bin/env python3
"""RR127 cycle 2, direction B.  Skeleton audit of BZ82's phi (p.314).

Companion to psi_audit.py.  This file does NOT re-do direction A's exhaustive
phi^2 = id census; it audits the *proof skeleton* asked for in the brief:
existence of a and mu, the Case I removal multiplicities when a = mu, both
inverse directions, and n = 0.

The one structural result derived here and not in the repo:

  MONOTONICITY LEMMA.  i |-> lambda_i - i is non-increasing on i >= 1
  (lambda_i is weakly decreasing, -i strictly decreasing).  Hence the Case II
  admissible condition  lambda_i - i <= t+3j-a-1  is an UP-SET in i, i.e. the
  admissible z-set  {z : ...}  is  DOWNWARD CLOSED in z.  So it is exactly
  {0,1,...,m} (or empty), the maximum m -- if it exists -- is the largest
  element of an initial segment, and

      max exists  <=>  z = 0 is admissible  <=>  lambda_{a+2j-1} <= t+5j-2
                       (and a+2j-2 >= 0).

Run: python3 phi_skeleton.py 24
"""

import sys
from collections import Counter

def parts_of(n, maxpart=None):
    if maxpart is None:
        maxpart = n if n > 0 else 1
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in parts_of(n - p, p):
            yield (p,) + rest

def P(j):
    return j * (5 * j - 1) // 2

def weight(j, lam):
    return sum(lam) + P(j)

def jrange(n):
    js = [0]; j = 1
    while P(j) <= n:
        js.append(j); js.append(-j); j += 1
    return sorted(js)

def states(n):
    for j in jrange(n):
        for lam in parts_of(n - P(j)):
            yield (j, lam)

def B_set(n):
    """B(n) = {lambda : length k, smallest part >= k}; () has k = 0."""
    out = set()
    for lam in parts_of(n):
        k = len(lam)
        if k == 0 or min(lam) >= k:
            out.add(lam)
    return out

def lam_padded(lam, x):
    return lam[x - 1] if 1 <= x <= len(lam) else 0

class Undef(Exception):
    pass

def phi(j, lam, rec=None):
    """BZ82 p.314 phi, transcribed from Main/CLAIMS.md / the RR127 brief."""
    t = len(lam)
    r = {} if rec is None else rec
    r['t'] = t
    # a = min{x >= 1 : 2j + x - lam(x) > 0}
    x = 1
    while 2 * j + x - lam_padded(lam, x) <= 0:
        x += 1
    a = x
    la = lam_padded(lam, a)
    mu = 2 * j + a - la
    lmu = lam_padded(lam, mu)
    tstar = t + (1 if a > t else 0) + (1 if mu > t else 0)
    r.update(a=a, lam_a=la, mu=mu, lam_mu=lmu, tstar=tstar)
    if la + lmu >= 5 * j + tstar:                        # ---- Case I
        r['branch'] = 'I'
        cnt = la + lmu - 5 * j - tstar
        r['r'] = cnt
        if cnt < 0:
            raise Undef('Case I: negative number of 1s')
        word = [lam_padded(lam, y) for y in range(1, tstar + 1)]
        remaining = [word[y - 1] for y in range(1, tstar + 1) if y not in (a, mu)]
        out = [v + 1 for v in remaining] + [1] * cnt
        if any(v <= 0 for v in out):
            raise Undef('Case I: non-positive part')
        return (j + 1, tuple(sorted(out, reverse=True)))
    # ---- Case II
    r['branch'] = 'II'
    D = a + 2 * j - 2
    r['D'] = D
    admissible = []
    for z in range(0, D + 1):
        if z + lam_padded(lam, a + 2 * j - 1 - z) <= t + 5 * j - 2:
            admissible.append(z)
    r['admissible'] = admissible
    if not admissible:
        raise Undef('Case II: admissible z-set empty')
    m = max(admissible)
    r['m'] = m
    p1, p2 = m, t + 5 * j - 3 - m
    r['parts_created'] = (p1, p2)
    if p2 < 0 or p1 < 0:
        raise Undef('Case II: negative created part %d' % min(p1, p2))
    out = [v - 1 for v in lam if v - 1 > 0] + [p for p in (p1, p2) if p > 0]
    return (j - 1, tuple(sorted(out, reverse=True)))

def phi_defined(j, lam):
    try:
        phi(j, lam); return True
    except Undef:
        return False

FAIL = []
def check(cond, tag, j, lam, extra=''):
    if not cond:
        FAIL.append((tag, j, lam, extra))

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    st = Counter()
    first = {}
    def note(tag):
        st[tag] += 1
        first.setdefault(tag, None)

    for n in range(N + 1):
        Bn = B_set(n)
        for (j, lam) in states(n):
            t = len(lam)
            # ---------- P1 existence / minimality of a
            x = 1
            while 2 * j + x - lam_padded(lam, x) <= 0:
                x += 1
            a = x
            check(a <= max(t + 1, 1 - 2 * j), 'P1 a <= max(t+1,1-2j)', j, lam, a)
            check(all(2 * j + y - lam_padded(lam, y) <= 0 for y in range(1, a)),
                  'P1 a is the minimum', j, lam, a)
            la, mu = lam_padded(lam, a), 2 * j + a - lam_padded(lam, a)
            # ---------- P2 mu >= 1, mu is a slot index >= 1
            check(mu >= 1, 'P2 mu >= 1', j, lam, mu)
            check(mu <= max(t + 1, 1 - 2 * j) + 2 * j, 'P2 mu bounded', j, lam, mu)
            tstar = t + (a > t) + (mu > t)
            case1 = (la + lam_padded(lam, mu) >= 5 * j + tstar)
            # ---------- P3 a = mu never happens in Case I
            if a == mu:
                st['a==mu'] += 1; first['a==mu'] = first['a==mu'] or (j, lam)
                check(not case1, 'P3 a=mu => Case II', j, lam, 'a=mu=%d' % a)
                check(la == 2 * j, 'P3 a=mu <=> lam_a = 2j', j, lam)
            defined = phi_defined(j, lam)
            # ---------- domain claim for phi: undefined exactly on {0} x B(n)
            expect_undef = (j == 0 and lam in Bn)
            check(defined != expect_undef, 'P0 domain = X(n) \\ {0}xB(n)', j, lam,
                  'defined=%s expect_undef=%s' % (defined, expect_undef))
            if not defined:
                st['F'] += 1
                continue
            st['Dom'] += 1
            rec = {}
            j2, lam2 = phi(j, lam, rec)
            st['case' + rec['branch']] += 1
            # ---------- P4 weight
            check(weight(j2, lam2) == n, 'P4 weight', j, lam, rec['branch'])
            check(all(p > 0 for p in lam2), 'P4 positivity', j, lam, rec['branch'])
            # ---------- P5 Case II structure: down-set + z=0 admissible
            if rec['branch'] == 'II':
                ad = rec['admissible']
                check(rec['D'] >= 0, 'P5 D = a+2j-2 >= 0', j, lam, 'D=%d' % rec['D'])
                check(ad == list(range(0, max(ad) + 1)),
                      'P5 admissible z-set is a DOWN-SET', j, lam, ad)
                check(0 in ad, 'P5 z = 0 admissible', j, lam,
                      'lam_%d = %d vs t+5j-2 = %d'
                      % (a + 2 * j - 1, lam_padded(lam, a + 2 * j - 1), t + 5 * j - 2))
                check(rec['m'] == max(ad), 'P5 m = max', j, lam)
            # ---------- P6 Case I: the number of new 1s is a nonneg integer
            if rec['branch'] == 'I':
                check(rec['r'] >= 0, 'P6 r >= 0', j, lam, rec['r'])
                check(rec['r'] == rec['lam_a'] + rec['lam_mu'] - 5 * j - rec['tstar'],
                      'P6 r formula', j, lam)
            # ---------- P7 case stability
            j3, lam3 = phi(j2, lam2)
            def case_of(jj, ll):
                return phi(jj, ll, {}).get('branch')
            check(case_of(j2, lam2) != rec['branch'],
                  'P7 Case I <-> Case II (phi changes the case)', j, lam, rec['branch'])
            # ---------- P8 finite involution check (evidence, not a proof)
            check((j3, lam3) == (j, lam), 'P8 phi^2 = id (finite check)', j, lam,
                  'phi(s)=%s phi^2(s)=%s' % ((j2, lam2), (j3, lam3)))
            # ---------- indices: phi must flip the sign parity
            check((j2 - j) % 2 != 0, 'P9 j parity flips', j, lam)

    print('phi skeleton audit, n = 0..%d, all %d states of X(n)' % (N, st['X'] if 'X' in st else 0))
    print('domain states %d, excluded {0}xB(n) %d' % (st['Dom'], st['F']))
    print('Case I %d, Case II %d' % (st['caseI'], st['caseII']))
    print('states with a = mu: %d  (all Case II: %s)' %
          (st['a==mu'], all(f[0] != 'P3 a=mu => Case II' for f in FAIL)))
    print('')
    if FAIL:
        print('FAILURES %d' % len(FAIL))
        c = Counter(f[0] for f in FAIL)
        for tag, k in c.most_common():
            w = next(f for f in FAIL if f[0] == tag)
            print('  %-48s x%-5d first j=%s lam=%s  %s' % (tag, k, w[1], w[2], w[3]))
        return 1
    print('0 failures on every skeleton step P0-P9 over the whole range.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
