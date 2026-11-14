#!/usr/bin/env python3
"""RR127 cycle 3, direction C.  Machine check of each STEP of the written proof
of obligation (i) (REPORT_c3.md, Finding 2), over a (j, lambda) slab.

This does not prove anything; it fails loudly if any step of the written
argument is instantiated outside its hypotheses in a way I did not notice.

Steps checked, over every (j, lam) with |j| <= JDOM, |lam| <= MDOM that lies in
phi's domain and in Case II with the admissible set S nonempty:

  s0  S nonempty  =>  R >= 0
  s1  k >= 1
  s2  f is strictly increasing on [0, hi]                (needs BOTH indices in [1,k])
  s3  f is NOT increasing past hi (reported, not a failure: the trap)
  s4  case (a) k <= t:  f(R) >= f(0)+R and m <= R-1
  s5  case (b) k > t:   j >= 1, a <= t+1, R >= k
  s6  the sharp form:   (p2 >= 0)  <=>  (R >= k)
  s7  the lemma itself: m <= R-1

Usage: python3 proofcheck_c3.py [JDOM] [MDOM] [--json OUT].  Exit 0 iff s0-s2 and
s4-s7 hold everywhere.
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def pad(lam, x):
    return lam[x - 1] if 1 <= x <= len(lam) else 0


def plist(m):
    out = [()]

    def rec(r, cap, acc):
        for p in range(min(r, cap), 0, -1):
            acc.append(p)
            out.append(tuple(acc))
            rec(r - p, p, acc)
            acc.pop()

    if m >= 1:
        rec(m, m, [])
    return out


def main(argv):
    jdom, mdom, js = 40, 22, os.path.join(HERE, 'results_proofcheck_c3.json')
    a = list(argv[1:])
    if '--json' in a:
        i = a.index('--json')
        js = a[i + 1]
        del a[i:i + 2]
    if a:
        jdom = int(a[0])
    if len(a) > 1:
        mdom = int(a[1])

    t0 = time.time()
    c = {k: 0 for k in ('states', 's0_R_neg', 's1_k_lt1', 's2_f_not_increasing',
                        's3_f_not_increasing_past_hi', 's4a', 's4a_fail',
                        's4a_concl_fail', 's4a_R_in_range', 's4a_R_above_hi',
                        's5b', 's5b_j_lt1', 's5b_a_gt_tp1',
                        's5b_R_lt_k', 's6_equiv_fail', 's7_lemma_fail')}
    ex = []
    for j in range(-jdom, jdom + 1):
        for lam in plist(mdom):
            t = len(lam)
            x = 1
            while 2 * j + x - pad(lam, x) <= 0:
                x += 1
            aa = x
            L = pad(lam, aa)
            k = aa + 2 * j - 1
            mu = 2 * j + aa - L
            Lmu = pad(lam, mu)
            ts = t + (1 if aa > t else 0) + (1 if mu > t else 0)
            if L + Lmu >= 5 * j + ts:                       # Case I
                continue
            if j == 0 and all(v >= t for v in lam):          # outside the domain
                continue
            R = t + 5 * j - 2
            hi = k - 1

            def f(z):
                return z + pad(lam, k - z)

            S = [z for z in range(0, hi + 1) if f(z) <= R] if hi >= 0 else []
            if not S:
                continue
            c['states'] += 1
            if R < 0:
                c['s0_R_neg'] += 1
            if k < 1:
                c['s1_k_lt1'] += 1
            if any(f(z + 1) <= f(z) for z in range(0, hi)):
                c['s2_f_not_increasing'] += 1
            if hi + 1 <= max(hi, R) + 2 and f(hi + 1) <= f(hi):
                c['s3_f_not_increasing_past_hi'] += 1
            m = max(S)
            if k <= t:
                c['s4a'] += 1
                # the argument splits: f(R) >= f(0)+R is only available when
                # R lies in [0,hi] (past hi the padded index 0 is reached and f
                # steps down); when R > hi the conclusion is m <= hi <= R-1.
                if R <= hi:
                    c['s4a_R_in_range'] += 1
                    if not f(R) >= f(0) + R:
                        c['s4a_fail'] += 1
                else:
                    c['s4a_R_above_hi'] += 1
                    if not m <= hi <= R - 1:
                        c['s4a_fail'] += 1
                if m > R - 1:
                    c['s4a_concl_fail'] += 1
            else:
                c['s5b'] += 1
                if j < 1:
                    c['s5b_j_lt1'] += 1
                if aa > t + 1:
                    c['s5b_a_gt_tp1'] += 1
                if R < k:
                    c['s5b_R_lt_k'] += 1
            if (R - 1 - m >= 0) != (R >= k):
                c['s6_equiv_fail'] += 1
            if m > R - 1:
                c['s7_lemma_fail'] += 1
                if len(ex) < 5:
                    ex.append({'j': j, 'lam': list(lam), 'k': k, 'R': R, 'm': m})

    elapsed = time.time() - t0
    bad = (c['s0_R_neg'] + c['s1_k_lt1'] + c['s2_f_not_increasing']
           + c['s4a_fail'] + c['s4a_concl_fail'] + c['s5b_j_lt1']
           + c['s5b_a_gt_tp1'] + c['s5b_R_lt_k'] + c['s6_equiv_fail']
           + c['s7_lemma_fail'])
    print('proof-step check: |j| <= %d, |lam| <= %d, %d in-domain Case-II states '
          'with S nonempty' % (jdom, mdom, c['states']))
    print('s0 R >= 0 fails %d   s1 k >= 1 fails %d   s2 f not increasing on '
          '[0,hi] %d   s3 f steps down past hi (expected, not a failure) %d'
          % (c['s0_R_neg'], c['s1_k_lt1'], c['s2_f_not_increasing'],
             c['s3_f_not_increasing_past_hi']))
    print('s4 case (a) k <= t: %d states (R <= hi: %d, R > hi: %d), branch '
          'argument fails %d, m <= R-1 fails %d'
          % (c['s4a'], c['s4a_R_in_range'], c['s4a_R_above_hi'],
             c['s4a_fail'], c['s4a_concl_fail']))
    print('s5 case (b) k > t: %d states, j < 1 %d, a > t+1 %d, R < k %d'
          % (c['s5b'], c['s5b_j_lt1'], c['s5b_a_gt_tp1'], c['s5b_R_lt_k']))
    print('s6 (p2>=0) <=> (R>=k) fails %d   s7 lemma m <= R-1 fails %d'
          % (c['s6_equiv_fail'], c['s7_lemma_fail']))
    print('')
    print('TOTAL: %s  (%d step failures, %.1f s)'
          % ('PASS' if bad == 0 else 'FAIL', bad, elapsed))
    with open(js, 'w') as fh:
        json.dump(dict(script='proofcheck_c3.py', jdom=jdom, mdom=mdom,
                       verdict='PASS' if bad == 0 else 'FAIL',
                       step_failures=bad, elapsed_seconds=round(elapsed, 3),
                       counterexamples=ex, **c), fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('wrote %s' % js)
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
