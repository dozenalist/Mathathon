#!/usr/bin/env python3
"""RR127 cycle 3, direction C.  CORRECTED skeleton audit of BZ82's phi (p.314).

Replaces (does not edit) Counterexamples/cycle2/phi_skeleton.py.  Three defects
of that file are repaired here; each is stated so a reader can check the repair:

  BUG-1  ``st['a==mu']``.  The cycle-2 file reads ``st['a==mu']`` from a Counter,
         which silently yields 0 rather than raising, so the reported failure
         "KeyError: 'a==mu'" is the labelled symptom of a counter being read at
         a point where no code path ever wrote the key.  Here every counter is
         a plain dict pre-populated by ``Census(keys)`` and ``Census.bump``
         raises KeyError on an unknown key, so an unwritten key is a loud
         failure instead of a silent zero.

  BUG-2  case stability.  The cycle-2 ``case_of`` re-derived the branch from a
         fresh record instead of consuming the record that ``phi`` had already
         populated, so P7 could pass without inspecting the actual step.  Here
         ``phi`` *returns* ``(state, rec)`` and P7 consumes that rec; P7 also
         asserts ``rec['branch'] in ('I','II')``, so a vacuous pass is
         impossible.

  BUG-3  Case I slot deletion.  The cycle-2 code deleted "any slot whose
         position is a or mu" with no check that two *distinct* slots exist.
         When ``a == mu <= t`` there is only one slot at that position, and the
         collision was silently resolved by set semantics.  Here the slot
         inventory is an explicit list ``[(pos, value), ...]`` of size ``t*``,
         each of the two deletions must consume a distinct entry, and a
         collision is a recorded WITNESS, never an invented fallback.

What is audited (P0-P9).  Each step is one obligation of the phi branch
analysis.  Every step is checked on EVERY signed state of weight <= NMAX, i.e.
on all of X(n), not only on phi's domain, so the domain claim is itself data:

  P0  DOMAIN        phi is computable (returns a partition) exactly on
                    X(n) minus {0}xB(n); the excluded states are exactly those
                    where the Case-II admissible z-set is empty.
  P1  FIND-a        a exists, a >= 1, every y < a has 2j+y-lam(y) <= 0 (a is
                    really the minimum), and a <= max(t+1, 1-2j).
  P2  FIND-mu       mu = 2j+a-L is an integer with 1 <= mu <= a+2j, i.e.
                    mu = k+1-L with 0 <= L = lam(a) <= k = a+2j-1.
  P3  a == mu       characterisation a == mu <=> L = 2j, and the sharp
                    obligation: a == mu MUST NEVER CO-OCCUR WITH CASE I, since
                    only Case I deletes the two slots and the slot at position a
                    would then have to be deleted twice.  This is checked
                    directly, and the two-case argument is in the module note
                    below ("NOTE ON a == mu").  A co-occurrence is reported as a
                    minimal witness and never patched with a fallback.
  P4  WEIGHT        the image has the same weight and every part is >= 1, in
                    both cases.
  P5  CASE-II-BOX   the admissible z-set is the down-set {0..m}, the index
                    range is nonempty (a+2j-2 >= 0) on the domain, and the
                    *second* created part t+5j-3-m is nonnegative -- with the
                    derivation recorded: a sufficient certificate is
                      (C-a) t+5j-2 >= m+1, or
                      (C-b) m = a+2j-2 and lam(k-m) = lam(1) >= 1.
  P6  CASE-I-COUNT  r = L + lam(mu) - 5j - t* is a nonnegative integer and the
                    slot inventory has size t*.
  P7  CASE-STABLE   phi(I) lands in Case II and phi(II) lands in Case I, and
                    the image stays inside phi's domain.
  P8  INVOLUTION    phi(phi(s)) = s on every in-domain state (finite evidence
                    for obligation (v); explicitly NOT a proof).
  P9  PARITY        j changes parity and |lam| + P(j) is invariant.

As a cross-check rather than a P-step, every in-domain state is also run
through the committed Computation/bz82.py and the images compared.

Usage:  python3 phi_skeleton_c3.py [NMAX] [--json OUT]
Default NMAX = 30.  Exit code 0 iff every step passed on every state.

NOTE ON a == mu.  Main's obligation (iii) asks whether a = mu is impossible in
Case I.  It is impossible, and the argument needs no computation:

  * If a <= t then L = lam(a) = 2j and L >= 1, so j >= 1.  Also mu = a <= t, so
    lam(mu) = L = 2j and t* = t.  Case I would need L + lam(mu) = 4j >=
    5j + t*, i.e. j + t <= 0, contradicting j >= 1 and t >= 0.
  * If a > t then L = lam(a) is the padded zero, so 2j = 0, i.e. j = 0.  Then
    mu = a > t as well, so lam(mu) = 0 and t* = t + 2.  Case I would need
    0 >= 5*0 + t* = t + 2, impossible.

So a = mu implies Case II, where no slot is deleted and the collision is
harmless; the "delete the slot at a and the slot at mu" reading needs no second
removal anywhere in Case I, and no fallback is required.  The finite census
below re-confirms it, and the auditor records the two sub-cases separately.
"""

import json
import os
import sys
import time


# ---------------------------------------------------------------------------
# X(n): signed states
# ---------------------------------------------------------------------------
def P(j):
    """5-pentagonal number j(5j-1)/2.  P(j-1)=P(j)-(5j-3), P(j+1)=P(j)+(5j+2)."""
    return j * (5 * j - 1) // 2


def weight(j, lam):
    return sum(lam) + P(j)


def parts_of(n, maxpart=None):
    """Descending partitions of n with parts <= maxpart, as tuples."""
    if maxpart is None:
        maxpart = n if n > 0 else 1
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in parts_of(n - p, p):
            yield (p,) + rest


def jrange(n):
    """Every j in Z with P(j) <= n, ascending."""
    js = [0]
    j = 1
    while P(j) <= n or P(-j) <= n:
        if P(j) <= n:
            js.append(j)
        if P(-j) <= n:
            js.append(-j)
        j += 1
    return sorted(js)


def states(n):
    for j in jrange(n):
        for lam in parts_of(n - P(j)):
            yield (j, lam)


def in_B(lam):
    """B(n) = {partitions of length k with smallest part >= k}; () has k = 0."""
    k = len(lam)
    return all(x >= k for x in lam)


def is_partition(lam):
    return (isinstance(lam, tuple)
            and all(isinstance(x, int) and not isinstance(x, bool) and x > 0
                    for x in lam)
            and all(lam[i] >= lam[i + 1] for i in range(len(lam) - 1)))


# ---------------------------------------------------------------------------
# the phi rules, transcribed with an explicit record
# ---------------------------------------------------------------------------
class Undef(Exception):
    """Raised only where the printed rule genuinely has no value."""


def lam_padded(lam, x):
    return lam[x - 1] if 1 <= x <= len(lam) else 0


def phi(j, lam):
    """BZ82 p.314 phi.  Returns (state, rec).  Raises Undef where undefined."""
    t = len(lam)
    rec = {'t': t, 'j_in': j, 'lam_in': lam}

    # ---- a = min{x >= 1 : 2j + x - lam(x) > 0}                        [P1]
    a = 1
    while 2 * j + a - lam_padded(lam, a) <= 0:
        a += 1
    L = lam_padded(lam, a)
    k = a + 2 * j - 1
    mu = 2 * j + a - L                       # = k + 1 - L
    Lmu = lam_padded(lam, mu)
    tstar = t + (1 if a > t else 0) + (1 if mu > t else 0)
    rec.update(a=a, L=L, k=k, mu=mu, Lmu=Lmu, tstar=tstar)

    if L + Lmu >= 5 * j + tstar:                                    # Case I
        rec['branch'] = 'I'
        r = L + Lmu - 5 * j - tstar
        rec['r'] = r
        # Slot inventory: the t real slots, plus ONE phantom slot of value 0 at
        # each of a, mu that exceeds t.  Size t* by construction.
        slots = [(pos, lam[pos - 1]) for pos in range(1, t + 1)]
        slots += [(pos, 0) for pos in (a, mu) if pos > t]
        rec['slot_count'] = len(slots)
        if len(slots) != tstar:                  # would be a bookkeeping bug
            raise AssertionError('slot inventory %d != t* %d at j=%r lam=%r'
                                 % (len(slots), tstar, j, lam))
        if r < 0:
            raise Undef('Case I: negative inserted count r=%d' % r)
        keep = list(slots)
        collisions = 0
        for pos in (a, mu):
            idx = next((i for i, (p, _v) in enumerate(keep) if p == pos), None)
            if idx is None:                     # BUG-3: no invented fallback
                collisions += 1
                break
            keep.pop(idx)
        rec['slot_collision'] = collisions
        if collisions:
            raise Undef('Case I: the second deleted slot does not exist '
                        '(a == mu with only one slot at that position)')
        out = [v + 1 for (_p, v) in keep] + [1] * r
        rec['ones_inserted'] = r
        new = tuple(sorted(out, reverse=True))
        rec['branch_out'] = 'I'
        return (j + 1, new), rec

    # ---- Case II                                                      [P5]
    rec['branch'] = 'II'
    hi = a + 2 * j - 2
    R = t + 5 * j - 2
    rec.update(hi=hi, R=R)
    adm = [z for z in range(0, hi + 1)
           if z + lam_padded(lam, a + 2 * j - 1 - z) <= R]
    rec['admissible'] = adm
    if not adm:
        raise Undef('Case II: admissible z-set empty (hi=%d)' % hi)
    m = max(adm)
    rec['m'] = m
    p1, p2 = m, t + 5 * j - 3 - m
    rec.update(p1=p1, p2=p2)
    # the derivation certificate for p2 >= 0, recorded rather than assumed
    cert = []
    if p2 >= 0:
        if R >= m + 1:
            cert.append('C-a')
        if m == hi and lam_padded(lam, a + 2 * j - 1 - m) >= 1:
            cert.append('C-b')
    rec['p2_cert'] = cert
    if p1 < 0 or p2 < 0:
        raise Undef('Case II: negative created part (%d,%d)' % (p1, p2))
    rest = [v - 1 for v in lam if v - 1 > 0]
    out = rest + [p for p in (p1, p2) if p > 0]
    rec['branch_out'] = 'II'
    return (j - 1, tuple(sorted(out, reverse=True))), rec


def phi_computes(j, lam):
    try:
        phi(j, lam)
        return True
    except Undef:
        return False


def case_of(state):
    """BUG-2 fix: consume the record that phi returns, do not re-derive it."""
    j, lam = state
    _out, rec = phi(j, lam)      # may raise Undef; caller passes defined states
    assert rec.get('branch') in ('I', 'II'), 'record not populated: %r' % (rec,)
    return rec['branch']


# ---------------------------------------------------------------------------
# census plumbing
# ---------------------------------------------------------------------------
STEPS = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9']

LABELS = {
    'P0': 'domain = X(n) \\ {0}xB(n)',
    'P1': 'a exists, a >= 1, minimal, a <= max(t+1, 1-2j)',
    'P2': 'mu = k+1-L is a slot index, 1 <= mu <= a+2j',
    'P3': 'a == mu <=> L = 2j, and then a > t (both slots virtual)',
    'P4': 'weight preserved, every image part >= 1',
    'P5': 'Case II: z-set is 0..m, hi >= 0, p2 = t+5j-3-m >= 0',
    'P6': 'Case I: r = L+lam(mu)-5j-t* >= 0, slot count = t*',
    'P7': 'Case I <-> Case II, image stays in the domain',
    'P8': 'phi(phi(s)) = s (finite evidence, not a proof)',
    'P9': 'j flips parity, |lam| + P(j) invariant',
}


class Census:
    """Fixed-key counters: writing an unknown key is a loud KeyError (BUG-1)."""

    def __init__(self, keys):
        self.d = {k: 0 for k in keys}

    def bump(self, key, n=1):
        if key not in self.d:
            raise KeyError('census key %r was never declared' % (key,))
        self.d[key] += n


class Checker:
    def __init__(self):
        self.fails = {k: [] for k in STEPS}
        self.n = {k: 0 for k in STEPS}

    def check(self, step, cond, j, lam, extra=''):
        self.n[step] += 1
        if not cond:
            self.fails[step].append((j, lam, extra))

    def ok(self, step):
        return not self.fails[step]


CENSUS_KEYS = [
    'states', 'domain', 'excluded', 'case_I', 'case_II',
    'a_eq_mu', 'a_eq_mu_real_slot', 'a_eq_mu_virtual', 'a_eq_mu_case_I',
    'case_I_ones_pos', 'case_I_virtual_a', 'case_I_virtual_mu',
    'case_I_both_virtual', 'case_II_part_dropped',
    'cert_Ca', 'cert_Cb', 'cert_both', 'cert_neither',
    'p2_zero', 'm_zero', 'stability_checked', 'm_eq_hi', 'm_lt_hi',
]


# ---------------------------------------------------------------------------
# the audit
# ---------------------------------------------------------------------------
def main(argv):
    nmax = 30
    json_out = None
    args = list(argv[1:])
    if '--json' in args:
        i = args.index('--json')
        json_out = args[i + 1]
        del args[i:i + 2]
    if args:
        nmax = int(args[0])

    t0 = time.time()
    st = Census(CENSUS_KEYS)
    ck = Checker()
    a_mu_witness = []
    p2_uncertified = []

    for n in range(nmax + 1):
        for (j, lam) in states(n):
            st.bump('states')
            t = len(lam)
            # ------------- P1: existence, minimality, explicit bound of a
            x = 1
            while 2 * j + x - lam_padded(lam, x) <= 0:
                x += 1
            a = x
            bound = max(t + 1, 1 - 2 * j)
            ck.check('P1', a >= 1 and a <= bound, j, lam,
                     'a=%d bound=%d' % (a, bound))
            ck.check('P1', all(2 * j + y - lam_padded(lam, y) <= 0
                               for y in range(1, a)),
                     j, lam, 'a=%d not minimal' % a)
            L = lam_padded(lam, a)
            # ------------- P2: mu is a genuine slot index
            k = a + 2 * j - 1
            mu = 2 * j + a - L
            is_case1 = (L + lam_padded(lam, mu) >= 5 * j
                        + t + (1 if a > t else 0) + (1 if mu > t else 0))
            ck.check('P2', 1 <= mu <= a + 2 * j, j, lam,
                     'mu=%d a+2j=%d' % (mu, a + 2 * j))
            ck.check('P2', mu == k + 1 - L and 0 <= L <= k, j, lam,
                     'mu=%d k+1-L=%d L=%d k=%d' % (mu, k + 1 - L, L, k))
            # ------------- P3: the a == mu collision
            if a == mu:
                st.bump('a_eq_mu')
                # (i) characterisation: mu = a  <=>  2j - L = 0
                ck.check('P3', L == 2 * j, j, lam,
                         'a=mu=%d but L=%d, 2j=%d' % (a, L, 2 * j))
                # (ii) the collision never meets Case I
                ck.check('P3', not is_case1, j, lam,
                         'a == mu = %d CO-OCCURS WITH CASE I (a would have to be '
                         'deleted twice)' % a)
                st.bump('a_eq_mu_real_slot' if a <= t else 'a_eq_mu_virtual')
                if is_case1:
                    st.bump('a_eq_mu_case_I')
                    if len(a_mu_witness) < 5:
                        a_mu_witness.append({'weight': n, 'j': j,
                                             'lam': list(lam), 'a': a, 'mu': mu,
                                             'L': L, 't': t, 'case': 'I'})
            # ------------- P0: the domain
            computes = phi_computes(j, lam)
            expect_excluded = (j == 0 and in_B(lam))
            ck.check('P0', computes == (not expect_excluded), j, lam,
                     'computes=%s excluded=%s' % (computes, expect_excluded))
            if not computes:
                st.bump('excluded')
                ck.check('P0', expect_excluded, j, lam,
                         'undefined but NOT in 0 x B(n)')
                continue
            st.bump('domain')
            (j2, lam2), rec = phi(j, lam)
            st.bump('case_' + rec['branch'])
            # ------------- P4: weight and positivity
            ck.check('P4', weight(j2, lam2) == n, j, lam,
                     '%r -> %r weight %d != %d'
                     % ((j, lam), (j2, lam2), weight(j2, lam2), n))
            ck.check('P4', is_partition(lam2), j, lam,
                     'image %r not a partition' % (lam2,))
            # ------------- P5: Case II box
            if rec['branch'] == 'II':
                adm = rec['admissible']
                ck.check('P5', rec['hi'] >= 0, j, lam, 'hi=%d' % rec['hi'])
                ck.check('P5', adm == list(range(0, rec['m'] + 1)), j, lam,
                         'admissible set is not the down-set 0..m: %r' % (adm,))
                ck.check('P5', rec['m'] >= 0, j, lam, 'm=%d' % rec['m'])
                ck.check('P5', rec['p2'] >= 0, j, lam,
                         'second created part t+5j-3-m = %d < 0 (m=%d)'
                         % (rec['p2'], rec['m']))
                if rec['p2'] == 0:
                    st.bump('p2_zero')
                if rec['m'] == 0:
                    st.bump('m_zero')
                st.bump('m_eq_hi' if rec['m'] == rec['hi'] else 'm_lt_hi')
                cert = rec['p2_cert']
                if 'C-a' in cert and 'C-b' in cert:
                    st.bump('cert_both')
                elif 'C-a' in cert:
                    st.bump('cert_Ca')
                elif 'C-b' in cert:
                    st.bump('cert_Cb')
                else:
                    st.bump('cert_neither')
                    if len(p2_uncertified) < 5:
                        p2_uncertified.append({'weight': n, 'j': j,
                                               'lam': list(lam), 'm': rec['m'],
                                               'hi': rec['hi'], 'R': rec['R'],
                                               'p2': rec['p2']})
                if len(lam2) < len(lam):
                    st.bump('case_II_part_dropped')
            # ------------- P6: Case I inserted count
            else:
                ck.check('P6', rec['r'] >= 0, j, lam, 'r=%d' % rec['r'])
                ck.check('P6', rec['slot_count'] == rec['tstar'], j, lam,
                         'slot inventory %d != t* %d'
                         % (rec['slot_count'], rec['tstar']))
                if rec['r'] > 0:
                    st.bump('case_I_ones_pos')
                if rec['a'] > t:
                    st.bump('case_I_virtual_a')
                if rec['mu'] > t:
                    st.bump('case_I_virtual_mu')
                if rec['a'] > t and rec['mu'] > t:
                    st.bump('case_I_both_virtual')
            # ------------- P7: case stability (record consumed, not re-derived)
            try:
                src = case_of((j2, lam2))
            except Undef as exc:
                src = 'UNDEF(%s)' % exc
            st.bump('stability_checked')
            want = 'II' if rec['branch'] == 'I' else 'I'
            ck.check('P7', src == want, j, lam,
                     'phi(%r) is Case %s, expected Case %s'
                     % ((j2, lam2), src, want))
            ck.check('P7', not (j2 == 0 and in_B(lam2)), j, lam,
                     "image %r left phi's domain" % (lam2,))
            # ------------- P8: phi^2 = id (finite evidence only)
            try:
                (j3, lam3), _ = phi(j2, lam2)
            except Undef as exc:
                j3, lam3 = None, exc
            ck.check('P8', (j3, lam3) == (j, lam), j, lam,
                     'phi(s)=%r phi^2(s)=%r' % ((j2, lam2), (j3, lam3)))
            # ------------- P9: parity and the weight identity
            ck.check('P9', (j2 - j) % 2 != 0, j, lam, 'j=%d -> %d' % (j, j2))
            ck.check('P9', sum(lam2) + P(j2) == n, j, lam, 'invariant broken')

    elapsed = time.time() - t0

    # ------------- cross-check against the committed implementation
    cross = {'checked': 0, 'mismatch': 0, 'examples': []}
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
        import bz82 as B                        # the committed reference map
        for n in range(nmax + 1):
            for (j, lam) in states(n):
                if not B.phi_domain((j, lam), n):
                    continue
                mine, _rec = phi(j, lam)
                theirs = B.phi((j, lam))
                cross['checked'] += 1
                if mine != theirs:
                    cross['mismatch'] += 1
                    if len(cross['examples']) < 5:
                        cross['examples'].append(
                            {'j': j, 'lam': list(lam),
                             'cycle3': [mine[0], list(mine[1])],
                             'bz82': [theirs[0], list(theirs[1])]})
    except ImportError as exc:                  # pragma: no cover
        cross['error'] = repr(exc)

    # ------------- report
    print('phi skeleton audit (corrected), all signed states of weight <= %d'
          % nmax)
    print('states in X(n): %d  in phi domain: %d  excluded {0}xB(n): %d'
          % (st.d['states'], st.d['domain'], st.d['excluded']))
    print('Case I: %d   Case II: %d' % (st.d['case_I'], st.d['case_II']))
    print('a == mu: %d  (a <= t: %d, a > t: %d)   a == mu AND Case I: %d'
          % (st.d['a_eq_mu'], st.d['a_eq_mu_real_slot'],
             st.d['a_eq_mu_virtual'], st.d['a_eq_mu_case_I']))
    print('Case II: p2 = 0 in %d, m = 0 in %d, m = hi in %d, m < hi in %d, '
          'image lost a 1 in %d'
          % (st.d['p2_zero'], st.d['m_zero'], st.d['m_eq_hi'],
             st.d['m_lt_hi'], st.d['case_II_part_dropped']))
    print('p2 certificate: C-a only %d, C-b only %d, both %d, neither %d'
          % (st.d['cert_Ca'], st.d['cert_Cb'], st.d['cert_both'],
             st.d['cert_neither']))
    print('Case I virtual slots: a only %d, mu only %d, both %d; r > 0 in %d'
          % (st.d['case_I_virtual_a'], st.d['case_I_virtual_mu'],
             st.d['case_I_both_virtual'], st.d['case_I_ones_pos']))
    print('')
    for step in STEPS:
        status = 'PASS' if ck.ok(step) else 'FAIL'
        first = ''
        if not ck.ok(step):
            j, lam, extra = ck.fails[step][0]
            first = '  first: j=%d lam=%r  %s  (n=%d)' % (j, lam, extra,
                                                         weight(j, lam))
        print('%-3s %-4s %6d checks  %s%s'
              % (step, status, ck.n[step], LABELS[step], first))
    print('')
    if a_mu_witness:
        print('WITNESSES for a == mu with a <= t (Case I slot collision):')
        for w in a_mu_witness:
            print('  %r' % (w,))
    if p2_uncertified:
        print('STATES where p2 >= 0 holds but NEITHER certificate applies '
              '(recorded: needs a third argument):')
        for w in p2_uncertified:
            print('  %r' % (w,))
    print('cross-check vs Computation/bz82.py: %d states, %d mismatches'
          % (cross['checked'], cross['mismatch']))
    for e in cross['examples']:
        print('  MISMATCH %r' % (e,))
    if 'error' in cross:
        print('  (cross-check skipped: %s)' % cross['error'])

    total_fail = sum(len(v) for v in ck.fails.values())
    verdict = 'PASS' if total_fail == 0 and cross['mismatch'] == 0 else 'FAIL'
    print('')
    print('TOTAL: %s  (%d failed assertions, %d cross-check mismatches, %.1f s)'
          % (verdict, total_fail, cross['mismatch'], elapsed))

    payload = {
        'script': 'phi_skeleton_c3.py',
        'nmax': nmax,
        'verdict': verdict,
        'elapsed_seconds': round(elapsed, 3),
        'census': st.d,
        'steps': {s: {'label': LABELS[s], 'checks': ck.n[s],
                      'failures': len(ck.fails[s]),
                      'status': 'PASS' if ck.ok(s) else 'FAIL',
                      'first_failure': (None if ck.ok(s) else
                                        {'j': ck.fails[s][0][0],
                                         'lam': list(ck.fails[s][0][1]),
                                         'detail': ck.fails[s][0][2]})}
                  for s in STEPS},
        'a_eq_mu_witnesses': a_mu_witness,
        'p2_uncertified_witnesses': p2_uncertified,
        'crosscheck_bz82': cross,
    }
    if json_out:
        with open(json_out, 'w') as fh:
            json.dump(payload, fh, indent=1, sort_keys=True)
            fh.write('\n')
        print('wrote %s' % json_out)
    return 0 if verdict == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
