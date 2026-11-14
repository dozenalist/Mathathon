#!/usr/bin/env python3
"""RR127 cycle 2, direction B (proof audit), member m1.

Audit harness for the amended all-n proof that psi is an involution on
X(n) \\ {0} x A(n)  (Bressoud-Zeilberger 1982, p.314).

`psi` below is transcribed from the problem statement laid out in
RogersRamanujan/Main/CLAIMS.md (RR-C008) -- NOT from Experimental/swarm_smwfxwsqf/m3/bz.py.
The point of the audit is that the *proof steps* -- not only the final
involution property -- are asserted state by state and can fail individually.

Files: AMENDED_PROOF.md (the written proof), this file (executable test).
Run:   python3 psi_audit.py 30
"""

import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------- partitions

def parts_of(n, maxpart=None):
    """All partitions of n as descending tuples of positive ints."""
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
    js = [0]
    j = 1
    while P(j) <= n:
        js.append(j)
        js.append(-j)
        j += 1
    return sorted(js)

def states(n):
    """X(n) = {(j, lam) : |lam| + P(j) = n}."""
    for j in jrange(n):
        for lam in parts_of(n - P(j)):
            yield (j, lam)

def in_A(lam):
    return all(p % 5 in (1, 4) for p in lam)

def A_set(n):
    return set(lam for lam in parts_of(n) if in_A(lam))

def cls(lam):
    """(t, t0, m0, m2, m3)."""
    t = len(lam)
    t0 = sum(1 for p in lam if p % 5 == 0)
    def mx(r):
        v = [p for p in lam if p % 5 == r]
        return max(v) if v else 0
    return t, t0, mx(0), mx(2), mx(3)

# ---------------------------------------------------------------- psi

class Undef(Exception):
    pass

def psi(j, lam, record=None):
    """BZ82 p.314, psi, transcribed from the statement in CLAIMS.md RR-C008.

    Returns (j', lam').  Raises Undef when the rule produces no partition
    (exactly the states {0} x A(n)) -- audit item (b) of the proof.
    `record`, if a dict, receives the branch and all intermediates.
    """
    t, t0, m0, m2, m3 = cls(lam)
    rec = {} if record is None else record
    rec.update(t=t, t0=t0, m0=m0, m2=m2, m3=m3)

    if t0 + j > 0 or m2 > 0:                                  # ---- Case I
        N = 5 * t0 + 5 * j - 3
        rec['N'] = N
        if N >= m2:                                           # ---- I(a)
            rec['branch'] = 'I(a)'
            rest = [p for p in lam if p % 5 != 0]
            rest += [p - 5 for p in lam if p % 5 == 0 and p - 5 > 0]
            rec['dropped_5s'] = sum(1 for p in lam if p == 5)
            if N <= 0:
                raise Undef('I(a) created a non-positive part')
            rest.append(N)
            return (j - 1, tuple(sorted(rest, reverse=True)))
        else:                                                 # ---- I(b)
            rec['branch'] = 'I(b)'
            k = (m2 - 5 * j - 2 - 5 * t0)
            if k < 0 or k % 5 != 0:
                raise Undef('I(b) needs a non-integral/negative number of 5s')
            k //= 5
            rec['k'] = k
            rest = list(lam)
            rest.remove(m2)
            rest = [p + 5 if p % 5 == 0 else p for p in rest]
            rest += [5] * k
            return (j + 1, tuple(sorted(rest, reverse=True)))

    # ---- Case II : t0 + j <= 0 and m2 = 0
    assert t0 + j <= 0 and m2 == 0
    rec['branch'] = None
    nu = m3 + 5 * j - 3
    rec['nu'] = nu
    if nu >= m0:                                              # ---- II(a)
        rec['branch'] = 'II(a)'
        rest = list(lam)
        if m3 > 0:
            rest.remove(m3)
        if nu > 0:
            rest.append(nu)
        return (j - 1, tuple(sorted(rest, reverse=True)))
    else:                                                     # ---- II(b)
        rec['branch'] = 'II(b)'
        mu = m0 - 5 * j - 2
        rec['mu'] = mu
        if mu <= 0:
            raise Undef('II(b) created the non-positive part %d' % mu)
        rest = list(lam)
        if m0 > 0:
            rest.remove(m0)
        rest.append(mu)
        return (j + 1, tuple(sorted(rest, reverse=True)))

def psi_defined(j, lam):
    try:
        psi(j, lam)
        return True
    except Undef:
        return False

# ---------------------------------------------------------------- audit core

FAIL = []

def check(cond, tag, j=None, lam=None, extra=''):
    if not cond:
        FAIL.append((tag, j, lam, extra))
    return cond

def audit(N, verbose=True):
    stats = Counter()
    IIa_nu0_rep = []        # Repair 2 witnesses: nu = 0 with m3 repeated
    IIa_nu0_notrep = []
    IIb_m0zero = []         # Repair 1 witnesses: m0 = 0
    per_n = defaultdict(lambda: Counter())

    for n in range(N + 1):
        An = A_set(n)
        X = list(states(n))
        stats['X'] += len(X)
        # --- the domain claim: psi undefined exactly on {0} x A(n)
        for (j, lam) in X:
            assert weight(j, lam) == n
            defined = psi_defined(j, lam)
            expect_undef = (j == 0 and lam in An)
            check(defined != expect_undef, 'domain', j, lam,
                  'defined=%s, j=0 and lam in A = %s' % (defined, expect_undef))
            if not defined:
                stats['F'] += 1
                continue
            stats['Dom'] += 1
            per_n[n]['Dom'] += 1
            t, t0, m0, m2, m3 = cls(lam)

            rec = {}
            j2, lam2 = psi(j, lam, rec)
            br = rec['branch']
            stats['branch_' + br] += 1
            per_n[n][br] += 1

            # ---- (a) weight, positivity, sign
            check(weight(j2, lam2) == n, '(a) weight', j, lam, br)
            check(all(p > 0 for p in lam2), '(a) positivity', j, lam, br)
            check((j2 - j) % 2 != 0, '(a) parity flips', j, lam, br)

            t2, t02, m02, m22, m32 = cls(lam2)
            # ---- (c) case stability of the top-level case
            case1_in = (t0 + j > 0 or m2 > 0)
            case1_out = (t02 + j2 > 0 or m22 > 0)
            check(case1_in == case1_out, '(c) top-level case stability', j, lam, br)

            # ---- branch-specific structural claims of the proof
            if br == 'I(a)':
                Nv = rec['N']
                s5 = rec['dropped_5s']
                check(Nv >= 2, '(c-Ia) N >= 2', j, lam)
                check(t02 == t0 - s5, '(c-Ia) t0\' = t0 - #(parts=5)', j, lam,
                      'got %d want %d' % (t02, t0 - s5))
                check(m22 == Nv, '(d-Ia) m2\' = N', j, lam, 'got %d want %d' % (m22, Nv))
                check(lam2.count(Nv) >= 1, '(d-Ia) N present', j, lam)
            elif br == 'I(b)':
                check(m2 >= 2, '(c-Ib) m2 != 0 (virtual zero impossible)', j, lam,
                      'm2 = %d' % m2)
                k = rec['k']
                check(k >= 0, '(a-Ib) k >= 0', j, lam, 'k=%d' % k)
                check(t02 == t0 + k, '(c-Ib) t0\' = t0 + k', j, lam,
                      'got %d want %d' % (t02, t0 + k))
                check(5 * (t02 + j2) == m2 + 3, '(c-Ib) 5(t0\'+j\') = m2+3', j, lam,
                      'got %d want %d' % (5 * (t02 + j2), m2 + 3))
                check(m22 <= m2, '(d-Ib) m2\' <= m2', j, lam)
            elif br == 'II(a)':
                nu = rec['nu']
                check(m3 >= 1, '(c-IIa) m3 != 0 (virtual zero impossible)', j, lam,
                      'm3 = %d, j = %d' % (m3, j))
                check(nu >= m0, '(IIa) guard', j, lam)
                check(t02 in (t0, t0 + 1), '(c-IIa) t0\' in {t0, t0+1}', j, lam,
                      't0=%d t0\'=%d' % (t0, t02))
                check((t02 == t0 + 1) == (nu > 0), '(c-IIa) t0\' = t0+1 iff nu>0', j, lam)
                check(t02 + j2 <= 0, '(c-IIa) t0\'+j\' <= 0', j, lam)
                check(m22 == 0, '(c-IIa) m2\' = 0', j, lam, 'm2\'=%d' % m22)
                if nu > 0:
                    check(nu % 5 == 0, '(IIa) nu = 0 mod 5', j, lam)
                    check(m02 == nu, '(d-IIa) m0\' = nu', j, lam,
                          'got %d want %d' % (m02, nu))
                else:
                    check(m02 == m0, '(d-IIa) nu=0: m0\' = m0 = 0', j, lam)
                check(m32 <= m3, '(d-IIa) NEW bound m3\' <= m3', j, lam,
                      'm3=%d m3\'=%d' % (m3, m32))
                # the *false* bound used by the committed proof
                repeated = (lam.count(m3) >= 2)
                check((m32 == m3) == repeated, '(d-IIa) m3\'=m3 iff m3 repeated',
                      j, lam, 'm3=%d m3\'=%d repeated=%s' % (m3, m32, repeated))
                stats['old_bound_broken'] += (m32 > m3 - 5)
                if m32 > m3 - 5:
                    stats['old_bound_broken_repeated'] += repeated
                if nu == 0:
                    (IIa_nu0_rep if repeated else IIa_nu0_notrep).append((j, lam))
                    check(m02 == 0, '(d-IIa) nu=0 => m0 = 0', j, lam)
                # the inequality that drives the inverse branch at s'
                check(m32 + 5 * (j2) - 3 < m02, '(d-IIa) II(b) selected at s\'', j, lam,
                      'got %d vs m0\'=%d' % (m32 + 5 * j2 - 3, m02))
            else:  # II(b)
                nu = rec['nu']
                mu = rec['mu']
                check(nu < m0, '(IIb) guard', j, lam)
                if m0 > 0:
                    check(t02 == t0 - 1, '(c-IIb) m0>0: t0\' = t0-1', j, lam,
                          't0=%d t0\'=%d' % (t0, t02))
                    check(mu >= 3, '(a-IIb) mu >= 3', j, lam, 'mu=%d' % mu)
                else:
                    IIb_m0zero.append((j, lam))
                    check(t0 == 0 and t02 == t0, '(c-IIb) REPAIR 1: m0=0 => t0\'=t0=0',
                          j, lam, 't0=%d t0\'=%d' % (t0, t02))
                    check(j <= -1, '(c-IIb) REPAIR 1: m0=0 => j <= -1', j, lam, 'j=%d' % j)
                    check(mu >= 3, '(a-IIb) m0=0 => mu >= 3', j, lam, 'mu=%d' % mu)
                check(mu % 5 == 3, '(a-IIb) mu = 3 mod 5', j, lam)
                check(m32 == mu, '(d-IIb) m3\' = mu (= max(m3,mu))', j, lam,
                      'm3=%d mu=%d m3\'=%d' % (m3, mu, m32))
                check(m02 <= m0, '(d-IIb) m0\' <= m0', j, lam)
                check(m22 == 0, '(c-IIb) m2\' = 0', j, lam)
                check(m32 + 5 * j2 - 3 >= m02, '(d-IIb) II(a) selected at s\'', j, lam,
                      'got %d vs m0\'=%d' % (m32 + 5 * j2 - 3, m02))
                check(m32 + 5 * j2 - 3 == m0, '(d-IIb) II(a) at s\' restores m0', j, lam)

            # ---- (d) doing it again gives s back
            check(psi(j2, lam2) == (j, lam), '(d) psi^2 = id', j, lam,
                  'psi(s)=%s psi^2(s)=%s' % ((j2, lam2), psi(j2, lam2)))
    return stats, per_n, IIa_nu0_rep, IIa_nu0_notrep, IIb_m0zero

# ---------------------------------------------------------------- repairs

def repairs_report(N):
    print('\n=== targeted witnesses for the two repairs in the committed proof ===')

    print('\nRepair 1  (II(b) case-stability, m0 = 0): t0\' = t0, NOT t0 - 1')
    w = [(-1, ()), (-1, (1,)), (-1, (3,)), (-1, (2, 3)), (-1, (3, 3, 3))]
    for s in w:
        j, lam = s
        rec = {}
        j2, lam2 = psi(j, lam, rec)
        if rec['branch'] != 'II(b)' or rec['m0'] != 0:
            print('    (-1;%s) is not an m0=0 II(b) state -- skipped (branch %s)'
                  % (','.join(map(str, lam)), rec['branch']))
            continue
        t02 = cls(lam2)[1]
        print('    (-1;%-7s) --II(b)--> (%d;%-7s)   t0 = %d, t0\' = %d, j\' = %d, so t0\'+j\' = %d'
              % (','.join(map(str, lam)) or '', j2, ','.join(map(str, lam2)) or '',
                 rec['t0'], t02, j2, t02 + j2))
        assert t02 == rec['t0'] == 0 and j2 <= 0
    print('    The claim "t0\' = t0 - 1" would give t0\' = -1 in every row above.')

    print('\nRepair 2  (II(a) branch-inverse, nu = m3 + 5j - 3 = 0)')
    for lam in [(3, 3), (3, 3, 3), (3, 3, 1), (3, 3, 1, 1), (3, 3, 4), (3, 3, 3, 2),
                (3,), (3, 1), (3, 1, 1), (8, 3), (2,), (1,), ()]:
        j = 0
        rec = {}
        try:
            j2, lam2 = psi(j, lam, rec)
        except Undef as e:
            print('    (0;%-9s) undefined: %s' % (','.join(map(str, lam)), e))
            continue
        if rec['branch'] != 'II(a)' or rec['nu'] != 0:
            print('    (0;%-9s) branch %s nu %s -- not the witness shape'
                  % (','.join(map(str, lam)), rec['branch'], rec.get('nu')))
            continue
        m3 = rec['m3']
        m32 = cls(lam2)[4]
        m02 = cls(lam2)[2]
        rep = lam.count(m3) >= 2
        print('    (0;%-9s) --II(a)--> (%d;%-9s)  m3 = %d, m3\' = %d, %s  '
              'm3\'+5(j-1)-3 = %d, m0\' = %d'
              % (','.join(map(str, lam)), j2, ','.join(map(str, lam2)) or '',
                 m3, m32, 'REPEATED' if rep else 'not repeated',
                 m32 + 5 * (j2) - 3, m02))
        print('        false bound m3\' <= m3-5 = %d holds? %s ; correct bound m3\' <= m3 = %d holds? %s'
              % (m3 - 5, m32 <= m3 - 5, m3, m32 <= m3))
        assert m32 <= m3

    print('\nEvery state of weight <= %d with II(a) and nu = 0:' % N)
    return None

# ---------------------------------------------------------------- main

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print('psi audit, all n = 0..%d, every state of X(n), every proof step asserted' % N)
    stats, per_n, rep, notrep, m0zero = audit(N)

    print('\n--- proof-step assertion failures ---')
    if FAIL:
        print('FAILURES: %d' % len(FAIL))
        seen = Counter(f[0] for f in FAIL)
        for tag, c in sorted(seen.items()):
            w = next(f for f in FAIL if f[0] == tag)
            print('  %-45s x%-5d first witness j=%s lam=%s | %s'
                  % (tag, c, w[1], w[2], w[3] if len(w) > 3 else ''))
        return 1
    print('0 failures: every step of the amended proof (a)-(d), every branch,')
    print('every virtual-zero case and every multiplicity case, holds on every state.')

    print('\nstates in X(n):   %d' % stats['X'])
    print('states in Dom(n): %d   (F(n) = {0}xA(n): %d)' % (stats['Dom'], stats['F']))
    print('branch counts:    I(a)=%d I(b)=%d II(a)=%d II(b)=%d'
          % (stats['branch_I(a)'], stats['branch_I(b)'],
             stats['branch_II(a)'], stats['branch_II(b)']))
    print('I(a) = I(b) and II(a) = II(b) (forced by psi^2 = id): %s'
          % (stats['branch_I(a)'] == stats['branch_I(b)']
             and stats['branch_II(a)'] == stats['branch_II(b)']))

    print('\nvirtual zeros, measured over the whole range:')
    print('  I(b) selected with m2 = 0          : 0 occurrences (proved impossible: N<m2=0 => N<0')
    print('                                       => t0+j <= 0 => Case II, contradiction)')
    print('  II(a) selected with m3 = 0         : 0 occurrences (proved impossible: nu=5j-3>=m0>=0')
    print('                                       => j>=1, but Case II gives j <= -t0 <= 0)')
    print('  II(a) selected with nu = 0, m3 repeated     : %d states' % len(rep))
    print('  II(a) selected with nu = 0, m3 not repeated : %d states' % len(notrep))
    print('  II(b) selected with m0 = 0                  : %d states' % len(m0zero))
    print('     (in all of them t0 = t0\' = 0 and j <= -1 -- Repair 1), e.g. (-1;()) -> (0;(3))')
    print('  states where the committed bound m3\' <= m3-5 is FALSE : %d'
          % stats['old_bound_broken'])
    print('     of which m3 is repeated                              : %d'
          % stats['old_bound_broken_repeated'])
    print('  n = 0: X(0) = {(0;())}, () in A_0, so Dom(0) = {} -- theorem vacuous.')
    if notrep:
        print('  smallest II(a)/nu=0/m3-not-repeated witness: j=%d lam=%s'
              % (notrep[0][0], notrep[0][1] or '()'))
    if rep:
        print('  smallest II(a)/nu=0/m3-REPEATED witness:     j=%d lam=%s'
              % (rep[0][0], rep[0][1]))

    repairs_report(N)
    return 0

if __name__ == '__main__':
    sys.exit(main())
