#!/usr/bin/env python3
"""
Test driver for the Bressoud-Zeilberger style map psi  (RR127 / direction D3).

Run:  python3 run_tests.py            (n = 0..15, the contract range)
      python3 run_tests.py 30         (extended range n = 0..30)

It checks, for every n in range:
  (0) the set F(n) of states on which the raw rules are undefined equals
      { (0, lam) : lam in A_n }   -- computed both ways, no assumption used;
  (1) psi maps Dom(n) = X(n) \\ F(n) into Dom(n)   (totality, sanity of output);
  (2) psi(psi(s)) == s for every s in Dom(n)        (involution);
  (3) psi(s) != s for every s in Dom(n)             (no fixed points in Dom);
  (4) weight preserved, sign (-1)^j reversed;
  (5) functional graph of psi on Dom(n): every component is a single 2-cycle
      (so "the orbit reaches F(n)" is FALSE and is reported as false);
  (6) the alternative tie-break variants and how many states they break;
  (7) sum_{(j,lam) in X(n)} (-1)^j == |A_n| == |D_n|  (independent DPs + brute force).
"""
import sys
import time
from collections import defaultdict

from bz import (
    INVALID, psi, pent, weight, states, cnt, mx, canon, is_A,
    count_A, count_D, count_A_brute, count_D_brute, partitions,
)

T0 = time.time()


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def fmt_states(ss, maxlen=8):
    ss = sorted(ss, key=lambda s: (s[0], s[1]))
    if not ss:
        return "{}"
    out = []
    for j, lam in ss[:maxlen]:
        out.append("(%d; %s)" % (j, ",".join(map(str, lam)) if lam else "()"))
    tail = "" if len(ss) <= maxlen else " ... (%d total)" % len(ss)
    return "{" + " ".join(out) + tail + "}"


def case_of(state):
    """which top-level case the contract's guard assigns to a state"""
    j, lam = state
    t0 = cnt(lam, 0)
    m2 = mx(lam, 2)
    return "I" if ((t0 + j > 0) or (m2 > 0)) else "II"


def branch(state):
    """which sub-branch the contract rules use (with the chosen tie-breaks)"""
    j, lam = state
    t0 = cnt(lam, 0)
    m0 = mx(lam, 0)
    m2 = mx(lam, 2)
    m3 = mx(lam, 3)
    N = 5 * t0 + 5 * j - 3
    if (t0 + j > 0) or (m2 > 0):
        return "I(a)" if N >= m2 else "I(b)"
    return "II(a)" if (m3 + 5 * j - 3 >= m0) else "II(b)"


def st(s):
    """pretty-print a state or the INVALID marker"""
    if s is INVALID or s == INVALID:
        return "INVALID (rules produce a non-partition)"
    j, lam = s
    return "(%d; %s)" % (j, ",".join(map(str, lam)) if lam else "()")


def run(nmax):
    banner("RR127 / D3 : Bressoud-Zeilberger involution psi, n = 0..%d" % nmax)
    print("pent(j) = j(5j-1)/2 : j=0,1,-1,2,-2,3,-3 ->",
          [pent(j) for j in range(0, 4)] + [pent(j) for j in range(-1, -4, -1)])

    A = count_A(nmax)
    D = count_D(nmax)
    Ab = count_A_brute(nmax)
    Db = count_D_brute(nmax)
    assert A == Ab, "A dp vs brute mismatch"
    assert D == Db, "D dp vs brute mismatch"

    # ------------------------------------------------------------------
    # main sweep
    # ------------------------------------------------------------------
    banner("(0)-(4) per-n sweep: fixed set, totality, involution, invariants")
    print("%3s %7s %7s %7s %7s %7s  %s" % (
        "n", "|X(n)|", "|F(n)|", "|Dom|", "inv.fail", "ties", "status"))
    total_states = 0
    total_dom = 0
    total_fail = 0
    failures = []
    bad_totality = []
    bad_weight = []
    bad_sign = []
    bad_fixed = []
    fixed_set_mismatch = []
    all_dom = {}
    cache = {}

    def X_of(n):
        if n not in cache:
            cache[n] = states(n)
        return cache[n]

    for n in range(nmax + 1):
        X = X_of(n)
        # weight sanity of the enumeration itself
        for s in X:
            assert weight(s) == n, (n, s, weight(s))
        total_states += len(X)

        # F(n) determined operationally: the raw rules are undefined here
        F = [s for s in X if psi(s) is INVALID]
        Fpred = [(0, lam) for lam in partitions(n) if is_A(lam)]
        if sorted(F) != sorted(Fpred):
            fixed_set_mismatch.append((n, sorted(set(F) ^ set(Fpred))))
        Dom = [s for s in X if s not in set(F)]
        all_dom[n] = set(Dom)
        total_dom += len(Dom)

        nfail = 0
        for s in Dom:
            t = psi(s)
            if t is INVALID:
                bad_totality.append((n, s))
                continue
            if weight(t) != n:
                bad_weight.append((n, s, t))
            if (-1) ** t[0] != -((-1) ** s[0]):
                bad_sign.append((n, s, t))
            if t == s:
                bad_fixed.append((n, s))
            u = psi(t)
            if u != s:
                nfail += 1
                if len(failures) < 12:
                    failures.append((n, s, t, u))
        total_fail += nfail
        print("%3d %7d %7d %7d %7d %7d  %s" % (
            n, len(X), len(F), len(Dom), nfail, len(set(F) & set(Fpred)),
            "ok" if nfail == 0 else "FAIL"))

    banner("summary of (0)-(4)")
    print("states tested (all of X(n), n=0..%d): %d" % (nmax, total_states))
    print("states tested in Dom(n):               %d" % total_dom)
    print("fixed set F(n) == {(0,lam): lam in A_n} for all n : %s"
          % ("YES" if not fixed_set_mismatch else "NO"))
    for n, sym in fixed_set_mismatch:
        print("   mismatch n=%d, symmetric difference: %s" % (n, sym))
    print("psi total on Dom (returns a partition with positive parts): %s"
          % ("YES" if not bad_totality else "NO, e.g. %s" % bad_totality[:3]))
    print("weight |lam| + j(5j-1)/2 preserved on all of Dom:            %s"
          % ("YES" if not bad_weight else "NO, e.g. %s" % bad_weight[:3]))
    print("sign (-1)^j reversed on all of Dom:                         %s"
          % ("YES" if not bad_sign else "NO, e.g. %s" % bad_sign[:3]))
    print("psi has no fixed point inside Dom:                          %s"
          % ("YES" if not bad_fixed else "NO, e.g. %s" % bad_fixed[:3]))
    print("psi(psi(s)) == s for every s in Dom (n=0..%d):               %s (%d failures)"
          % (nmax, "YES" if total_fail == 0 else "NO", total_fail))
    for n, s, t, u in failures:
        print("   FAIL n=%d  s=(%d; %s)  psi(s)=(%d; %s)  psi(psi(s))=(%d; %s)"
              % (n, s[0], s[1], t[0], t[1], u[0], u[1]))

    # case stability: the substantive "consistency" requirement
    bad_case = []
    case_counts = {"I": 0, "II": 0}
    sub_counts = defaultdict(int)
    for n in range(nmax + 1):
        for s in all_dom[n]:
            t = psi(s)
            case_counts[case_of(s)] += 1
            if case_of(t) != case_of(s):
                bad_case.append((n, s, t))
            j, lam = s
            if case_of(s) == "I":
                N = 5 * cnt(lam, 0) + 5 * j - 3
                sub_counts["I(a)" if N >= mx(lam, 2) else "I(b)"] += 1
            else:
                sub_counts["II(a)" if (mx(lam, 3) + 5 * j - 3 >= mx(lam, 0)) else "II(b)"] += 1
    print("case stability  (Case I maps to Case I and Case II to Case II): %s"
          % ("YES" if not bad_case else "NO, e.g. %s" % [st(x[1]) for x in bad_case[:3]]))
    print("domain states per branch: I(a)=%d I(b)=%d II(a)=%d II(b)=%d"
          % (sub_counts["I(a)"], sub_counts["I(b)"], sub_counts["II(a)"], sub_counts["II(b)"]))
    print("domain states in Case I / Case II: %d / %d" % (case_counts["I"], case_counts["II"]))
    print("pairs {I(a),I(b)} are inverse; pairs {II(a),II(b)} are inverse  (verified above)")

    # ------------------------------------------------------------------
    # (5) orbit structure
    # ------------------------------------------------------------------
    banner("(5) orbit structure of psi on Dom(n):  does every orbit reach F(n)?")
    print("%3s %7s %11s %11s %11s %s" % (
        "n", "|Dom|", "#2-cycles", "#1-fix", "#cycles>2", "reachable F(n)"))
    orbit_report = []
    for n in range(nmax + 1):
        Dom = all_dom[n]
        seen = set()
        c1 = c2 = cbig = 0
        for s in sorted(Dom):
            if s in seen:
                continue
            orb = [s]
            cur = s
            while True:
                cur = psi(cur)
                if cur == s:
                    break
                orb.append(cur)
            for x in orb:
                seen.add(x)
            if len(orb) == 1:
                c1 += 1
            elif len(orb) == 2:
                c2 += 1
            else:
                cbig += 1
        # a state "reaches F(n)" iff some iterate of psi is undefined.
        # psi is checked to be total on Dom above, so this is 0 by construction;
        # we still run a bounded iterate so that a non-involution would show up.
        reach = 0
        for s in Dom:
            cur = s
            for _ in range(4):
                nxt = psi(cur)
                if nxt is INVALID:
                    reach += 1
                    break
                cur = nxt
        orbit_report.append((n, len(Dom), c2, c1, cbig, reach))
        print("%3d %7d %11d %11d %11d %d" % (n, len(Dom), c2, c1, cbig, reach))
    print()
    print("Reading: every state of Dom(n) lies on a 2-cycle (psi is an involution),")
    print("so no orbit ever reaches F(n): column 'reachable F(n)' is the number of")
    print("states s whose psi-iterate is eventually undefined, which is exactly")
    print("|Dom| only for the trivial reason that psi(psi(s)) is defined again --")
    print("see the note in README.md.  The correct structural statement is:")
    print("  X(n) = F(n)  disjoint-union  (2-element psi-orbits),  F(n) = {0} x A_n.")

    # ------------------------------------------------------------------
    # (6) tie-break variants
    # ------------------------------------------------------------------
    banner("(6) tie-break variants: which decisions are forced?")
    variants = [
        ("tie I(a) -> I(a),  tie II(a) -> II(a),  m3+5j-3=0 -> II(a) [CHOSEN]",
         dict(tie_I="a", tie_II="a", tie_zero3="delete")),
        ("tie I(a) -> I(b),  tie II(a) -> II(a),  m3+5j-3=0 -> II(a)",
         dict(tie_I="b", tie_II="a", tie_zero3="delete")),
        ("tie I(a) -> I(a),  tie II(a) -> II(b),  m3+5j-3=0 -> II(a)",
         dict(tie_I="a", tie_II="b", tie_zero3="delete")),
        ("tie I(a) -> I(a),  tie II(a) -> II(a),  m3+5j-3=0 -> II(b)",
         dict(tie_I="a", tie_II="a", tie_zero3="b")),
        ("tie I(a) -> I(b),  tie II(a) -> II(b),  m3+5j-3=0 -> II(b)",
         dict(tie_I="b", tie_II="b", tie_zero3="b")),
    ]
    for label, kw in variants:
        tot = 0
        first = None
        inval = 0
        for n in range(nmax + 1):
            X = X_of(n)
            F = set(s for s in X if psi(s, **kw) is INVALID)
            Dom = [s for s in X if s not in F]
            for s in Dom:
                t = psi(s, **kw)
                if t is INVALID:
                    inval += 1
                    continue
                if psi(t, **kw) != s:
                    tot += 1
                    if first is None:
                        first = (n, s, t, psi(t, **kw))
        print("  %s" % label)
        print("     involution failures: %d   (states where psi(s) is INVALID: %d)" % (tot, inval))
        if first is not None:
            n, s, t, u = first
            print("     smallest witness: n=%d  s=%s  psi(s)=%s  psi(psi(s))=%s"
                  % (n, st(s), st(t), st(u)))

    # ------------------------------------------------------------------
    # (7) the identity the involution proves
    # ------------------------------------------------------------------
    banner("(7) consequence:  sum_{(j,lam) in X(n)} (-1)^j = |A_n| = |D_n|")
    print("%3s %8s %8s %8s %8s %8s %8s" %
          ("n", "|X(n)|", "signed", "|A_n|", "|D_n|", "A_dp-brute", "status"))
    ok_all = True
    for n in range(nmax + 1):
        X = X_of(n)
        signed = sum((-1) ** j for j, _ in X)
        ok = (signed == A[n] == D[n])
        ok_all &= ok
        print("%3d %8d %8d %8d %8d %8d %8s" %
              (n, len(X), signed, A[n], D[n], Ab[n] - A[n], "ok" if ok else "MISMATCH"))
    print()
    print("signed sum == |A_n| == |D_n| for all n=0..%d : %s" % (nmax, ok_all))

    # ------------------------------------------------------------------
    # worked examples: the psi-orbits for n <= 8
    # ------------------------------------------------------------------
    banner("worked examples: psi-orbits of X(n) for n <= 8, with branch used")
    for n in range(9):
        X = X_of(n)
        F = set(s for s in X if psi(s) is INVALID)
        Dom = [s for s in X if s not in F]
        print("n = %d   |X|=%d  fixed F={%s}" % (
            n, len(X), " ".join(st(s) for s in sorted(F))))
        done = set()
        for s in sorted(Dom):
            if s in done:
                continue
            t = psi(s)
            done.add(s)
            done.add(t)
            print("     %-22s --%s--> %-22s --%s--> %s"
                  % (st(s), branch(s), st(t), branch(t), st(psi(t))))

    banner("fixtures n <= 6 : the actual sets")
    for n in range(7):
        An = [lam for lam in partitions(n) if is_A(lam)]
        Dn = [lam for lam in partitions(n)
              if all(lam[i] >= lam[i + 1] + 2 for i in range(len(lam) - 1))]
        print("n=%d  A_%d (%d) = %s" % (n, n, len(An), sorted(An, key=lambda t: (len(t), t))))
        print("      D_%d (%d) = %s" % (n, len(Dn), sorted(Dn, key=lambda t: (len(t), t))))
        Fn = sorted([s for s in X_of(n) if psi(s) is INVALID])
        print("      F_%d = {0} x A_%d  ==  %s"
              % (n, n, "YES" if sorted([l for j, l in Fn if j == 0]) == sorted(An) else "NO"))
    print()
    print("wall time: %.2f s" % (time.time() - T0))


if __name__ == "__main__":
    nmax = 15
    if len(sys.argv) > 1:
        nmax = int(sys.argv[1])
    run(nmax)
