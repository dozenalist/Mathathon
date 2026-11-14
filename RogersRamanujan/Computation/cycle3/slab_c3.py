#!/usr/bin/env python3
"""RR127 cycle 3, direction C.  A (j, lambda) slab that is NOT a weight slice.

Every census in the project so far fixes a weight n and enumerates
X(n) = {(j;lam) : |lam| + P(j) = n}.  That couples j to |lam|, so a state with
j = -12 can only appear next to a partition of weight P(12) = 342 or more and is
never seen at small bounds.  This script sweeps the rectangle

    |j| <= JDOM,  lam a partition of |lam| <= MDOM,

and reports, for every state, its phi branch and the two quantities the
obligations (i) and (iii) of the cycle-3 brief turn on:

  (iii)  does a == mu ever co-occur with Case I?   (a fallback would be needed)
  (i)    is the second created Case-II part t+5j-3-m >= 0, and does the
         sufficient certificate C-a (t+5j-2 >= m+1) always hold?

Nothing here is a proof; it is a much wider finite screen than a weight slice,
deliberately chosen to break the j/lambda coupling.

Usage:  python3 slab_c3.py [JDOM] [MDOM] [--json OUT]
Defaults JDOM = 24, MDOM = 24.  Exit code 0 iff no violation was found.
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def pad(lam, x):
    return lam[x - 1] if 1 <= x <= len(lam) else 0


def parts_upto(m):
    """Every partition with weight <= m, as tuples in descending order."""
    out = [()]

    def rec(remaining, cap, acc):
        for p in range(min(remaining, cap), 0, -1):
            acc.append(p)
            out.append(tuple(acc))
            rec(remaining - p, p, acc)
            acc.pop()

    rec(m, m, [])
    out.sort(key=lambda q: (len(q), q), reverse=True)
    return out


def main(argv):
    jdom, mdom, json_out = 24, 24, os.path.join(HERE, 'results_slab_c3.json')
    a = list(argv[1:])
    if '--json' in a:
        i = a.index('--json')
        json_out = a[i + 1]
        del a[i:i + 2]
    if a:
        jdom = int(a[0])
    if len(a) > 1:
        mdom = int(a[1])

    t0 = time.time()
    lams = parts_upto(mdom)
    st = dict(states=0, case_I=0, case_II=0, case_II_empty_adm=0,
              a_eq_mu=0, a_eq_mu_case_I=0, a_eq_mu_real_slot=0,
              negative_p2=0, cert_Ca_fail=0, r_negative=0,
              case_II_hi_negative_in_domain=0, empty_adm_in_domain=0,
              empty_adm_out_of_domain=0, criterion_violations=0,
              excluded_states=0, min_p2=None, min_p2_state=None,
              min_r=None, min_r_state=None)
    viol = []

    for j in range(-jdom, jdom + 1):
        for lam in lams:
            st['states'] += 1
            t = len(lam)
            x = 1
            while 2 * j + x - pad(lam, x) <= 0:
                x += 1
            aa = x
            L = pad(lam, aa)
            k = aa + 2 * j - 1
            mu = 2 * j + aa - L
            Lmu = pad(lam, mu)
            tstar = t + (1 if aa > t else 0) + (1 if mu > t else 0)
            case1 = (L + Lmu >= 5 * j + tstar)
            kk = len(lam)
            in_dom = not (j == 0 and all(v >= kk for v in lam))
            if not in_dom:
                st['excluded_states'] += 1
            if aa == mu:
                st['a_eq_mu'] += 1
                if aa <= t:
                    st['a_eq_mu_real_slot'] += 1
                if case1:
                    st['a_eq_mu_case_I'] += 1
                    if len(viol) < 10:
                        viol.append({'kind': 'a==mu with Case I', 'j': j,
                                     'lam': list(lam), 'a': aa, 'mu': mu, 'L': L})
            if case1:
                st['case_I'] += 1
                r = L + Lmu - 5 * j - tstar
                if r < 0:
                    st['r_negative'] += 1
                    if len(viol) < 10:
                        viol.append({'kind': 'r < 0', 'j': j, 'lam': list(lam),
                                     'r': r})
                if st['min_r'] is None or r < st['min_r']:
                    st['min_r'] = r
                    st['min_r_state'] = {'j': j, 'lam': list(lam), 'r': r}
                continue
            st['case_II'] += 1
            hi, R = aa + 2 * j - 2, t + 5 * j - 2
            adm = [z for z in range(0, hi + 1)
                   if z + pad(lam, aa + 2 * j - 1 - z) <= R] if hi >= 0 else []
            # the sharp criterion: nonempty <=> k >= 1 and lam(k) <= R
            crit = (k >= 1 and pad(lam, k) <= R)
            if crit != bool(adm):
                st['criterion_violations'] += 1
                if len(viol) < 10:
                    viol.append({'kind': 'maximum-existence criterion fails',
                                 'j': j, 'lam': list(lam), 'k': k, 'R': R,
                                 'criterion': crit, 'nonempty': bool(adm)})
            if hi < 0:
                if in_dom:
                    st['case_II_hi_negative_in_domain'] += 1
                    if len(viol) < 10:
                        viol.append({'kind': 'Case II with hi < 0, IN DOMAIN',
                                     'j': j, 'lam': list(lam), 'hi': hi})
                continue
            if not adm:
                if in_dom:
                    st['empty_adm_in_domain'] += 1
                    if len(viol) < 10:
                        viol.append({'kind': 'Case II empty admissible set, IN DOMAIN',
                                     'j': j, 'lam': list(lam), 'hi': hi, 'R': R})
                else:
                    st['empty_adm_out_of_domain'] += 1
                continue
            m = max(adm)
            p2 = t + 5 * j - 3 - m
            if p2 < 0:
                st['negative_p2'] += 1
                if len(viol) < 10:
                    viol.append({'kind': 'p2 < 0', 'j': j, 'lam': list(lam),
                                 'm': m, 'hi': hi, 'R': R, 'p2': p2})
            if R < m + 1:
                st['cert_Ca_fail'] += 1
                if len(viol) < 10:
                    viol.append({'kind': 'C-a fails (R < m+1)', 'j': j,
                                 'lam': list(lam), 'm': m, 'R': R})
            if st['min_p2'] is None or p2 < st['min_p2']:
                st['min_p2'] = p2
                st['min_p2_state'] = {'j': j, 'lam': list(lam), 'm': m,
                                      'p2': p2, 'weight': sum(lam) + j * (5 * j - 1) // 2}

    elapsed = time.time() - t0
    bad = (st['a_eq_mu_case_I'] + st['negative_p2'] + st['cert_Ca_fail']
           + st['r_negative'] + st['case_II_hi_negative_in_domain']
           + st['empty_adm_in_domain'] + st['criterion_violations'])
    print('slab sweep:  |j| <= %d, |lam| <= %d   (%d partitions)'
          % (jdom, mdom, len(lams)))
    print('states %d  Case I %d  Case II %d'
          % (st['states'], st['case_I'], st['case_II']))
    print('a == mu: %d (with a <= t: %d)   a == mu AND Case I: %d'
          % (st['a_eq_mu'], st['a_eq_mu_real_slot'], st['a_eq_mu_case_I']))
    print('states outside phi\'s domain ({0}xB(n)): %d'
          % st['excluded_states'])
    print('Case II: p2 < 0 %d, C-a fails %d, criterion violations %d'
          % (st['negative_p2'], st['cert_Ca_fail'],
             st['criterion_violations']))
    print('Case II outside phi\'s domain: hi < 0 %d, admissible empty %d '
          '(these ARE the excluded states)'
          % (st['case_II_hi_negative_in_domain'],
             st['empty_adm_out_of_domain']))
    print('Case II INSIDE phi\'s domain: hi < 0 %d, admissible empty %d'
          % (st['case_II_hi_negative_in_domain'], st['empty_adm_in_domain']))
    print('Case I: r < 0 %d;  min r = %s at %s'
          % (st['r_negative'], st['min_r'], st['min_r_state']))
    print('min p2 = %s at %s' % (st['min_p2'], st['min_p2_state']))
    print('')
    print('TOTAL: %s  (%d violations, %.1f s)'
          % ('PASS' if bad == 0 else 'FAIL', bad, elapsed))
    payload = dict(script='slab_c3.py', jdom=jdom, mdom=mdom,
                   verdict='PASS' if bad == 0 else 'FAIL',
                   violations=viol, elapsed_seconds=round(elapsed, 3), **st)
    with open(json_out, 'w') as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('wrote %s' % json_out)
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
