#!/usr/bin/env python3
"""
run_audit.py -- deliverable harness for RR127 cycle 2, direction A.

Runs, on the FRESH implementation in bz82_audit.py:
  (i)   the phi Case-II integer domain of z: empty-set census, smallest
        selected z, and the comparison of the z >= 0 reading against the
        "all integers z <= a+2j-2" reading;
  (ii)  exhaustive phi^2 = id and psi^2 = id with domain closure, over all of
        X(n) for n <= NMAX (default 30), with coverage counters for the
        structural cases the audit must touch;
  (iii) the three printed examples of BZ82 p.315;
  (v)   raw per-weight statistics of the alternating path, plus two labelled
        traces;
  (vi)  is a written statement (see REPORT.md), not a number.
  (iv)  is compare_bz82.py, which needs the audit to be frozen first.

Usage:  python3 run_audit.py [NMAX]
Writes: results_cycle2.json, traces_cycle2.txt
Exit code 0 iff every check passed.
"""

import json
import sys
import time
from fractions import Fraction

import bz82_audit as B

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
FAILS = []          # hard failures: any entry means a check failed
NOTES = []          # observations that are not failures


def fail(where, detail):
    FAILS.append(dict(where=where, detail=str(detail)))


# ---------------------------------------------------------------------------
# (i) and (ii): the exhaustive census
# ---------------------------------------------------------------------------


def census(NMAX):
    cov = dict(
        states=0, phi_domain=0, psi_domain=0, phi_excluded=0, psi_excluded=0,
        phi_caseI=0, phi_caseII=0, psi_Ia=0, psi_Ib=0, psi_IIa=0, psi_IIb=0,
        t0_empty_lam=0, j_pos=0, j_neg=0, j_zero=0, j_even=0, j_odd=0,
        repeated_parts=0, phi_virtual_zero=0, phi_virtual_a=0, phi_virtual_mu=0,
        phi_a_eq_mu=0, psi_t0_pos=0, psi_m2_pos=0, psi_m0_zero=0,
        psi_m3_zero=0, psi_IIb_created=0, psi_IIa_deleted=0,
        psi_Ia_part_dropped=0, phi_II_part_dropped=0, phi_I_ones_pos=0,
        psi_Ib_copy_pos=0,
    )
    per_weight = {}
    # Case-II census (i): over EVERY Case-II state of X(n), n <= NMAX,
    # regardless of whether it lies in phi's domain, plus the in-domain figure.
    c2 = dict(total_caseII=0, in_domain_caseII=0, empty_admissible=0,
              empty_admissible_in_domain=0, hi_neg=0, hi_neg_in_domain=0,
              zmin0_argmax_min=None, zmin0_argmax_max=None,
              zmin0_sizes={}, domain_disagreements=0,
              domain_disagreement_examples=[], min_selected_m=None,
              max_selected_m=None, neg_created=0, setsize_min=None,
              setsize_max=None)
    for n in range(NMAX + 1):
        pw = dict(n=n, states=0, phi=0, psi=0)
        for (j, lam) in B.states_of_weight(n):
            cov["states"] += 1
            pw["states"] += 1
            t = len(lam)
            # ---- structural coverage ----
            if t == 0:
                cov["t0_empty_lam"] += 1
            if j > 0:
                cov["j_pos"] += 1
            elif j < 0:
                cov["j_neg"] += 1
            else:
                cov["j_zero"] += 1
            cov["j_even" if j % 2 == 0 else "j_odd"] += 1
            if len(set(lam)) < len(lam):
                cov["repeated_parts"] += 1

            # ---- the phi case split, evaluated on every state ----
            a = B._phi_a(j, lam)
            la = B.lam_at(lam, a)
            mu = 2 * j + a - la
            lmu = B.lam_at(lam, mu)
            tstar = t + (1 if la == 0 else 0) + (1 if lmu == 0 else 0)
            is_caseI = la + lmu >= 5 * j + tstar
            if a == mu:
                cov["phi_a_eq_mu"] += 1
                if is_caseI:
                    fail("a=mu in Case I", (j, lam, a, mu))
            if is_caseI:
                cov["phi_caseI"] += 1
                if la == 0 or lmu == 0:
                    cov["phi_virtual_zero"] += 1
                if la == 0:
                    cov["phi_virtual_a"] += 1
                if lmu == 0:
                    cov["phi_virtual_mu"] += 1
            else:
                cov["phi_caseII"] += 1
                c2["total_caseII"] += 1
                in_dom = B.phi_domain(j, lam)
                # identify the empty admissible sets exactly
                if not in_dom:
                    c2["empty_iff_offdomain_off"] = c2.get("empty_iff_offdomain_off", 0) + 1
                    if not (j == 0 and B.in_B(lam)):
                        fail("off-domain Case-II state that is not 0 x B", (j, lam))
                if in_dom:
                    c2["in_domain_caseII"] += 1
                S, ep = B.case_ii_admissible_set(j, lam, zmin=0)
                hi = ep["hi"]
                if hi < 0:
                    c2["hi_neg"] += 1
                    c2.setdefault("hi_neg_witnesses", []).append(
                        dict(j=j, lam=list(lam), hi=hi, a=ep["a"], t=t, in_phi_domain=in_dom))
                    if in_dom:
                        c2["hi_neg_in_domain"] += 1
                if not S:
                    c2["empty_admissible"] += 1
                    if len(c2.setdefault("empty_witnesses", [])) < 6:
                        c2["empty_witnesses"].append(
                            dict(j=j, lam=list(lam), n=n, in_phi_domain=in_dom,
                                 in_B=B.in_B(lam), hi=ep["hi"]))
                    if in_dom:
                        c2["empty_admissible_in_domain"] += 1
                else:
                    m = S[-1]
                    c2["zmin0_sizes"][len(S)] = c2["zmin0_sizes"].get(len(S), 0) + 1
                    if c2["setsize_min"] is None or len(S) < c2["setsize_min"]:
                        c2["setsize_min"] = len(S)
                    if c2["setsize_max"] is None or len(S) > c2["setsize_max"]:
                        c2["setsize_max"] = len(S)
                    if c2["min_selected_m"] is None or m < c2["min_selected_m"]:
                        c2["min_selected_m"] = m
                    if c2["max_selected_m"] is None or m > c2["max_selected_m"]:
                        c2["max_selected_m"] = m
                    # does the printed lower bound matter?
                    S2, _ = B.case_ii_admissible_set(j, lam, zmin=None)
                    m2 = S2[-1] if S2 else None
                    if m2 != m:
                        c2["domain_disagreements"] += 1
                        if len(c2["domain_disagreement_examples"]) < 8:
                            c2["domain_disagreement_examples"].append(
                                dict(j=j, lam=list(lam), m_zge0=m, m_allint=m2,
                                     hi=hi, lo=ep["lo"]))

            # ---- phi^2 = id, with closure, over phi's domain ----
            if B.phi_domain(j, lam):
                cov["phi_domain"] += 1
                pw["phi"] += 1
                try:
                    s2, d1 = B.phi(j, lam)
                except Exception as e:               # pragma: no cover
                    fail("phi raised", (j, lam, repr(e)))
                    continue
                if not B._is_partition(s2[1]):
                    fail("phi output not a partition", (j, lam, s2))
                if B.weight(*s2) != n:
                    fail("phi changed the weight", (j, lam, s2, B.weight(*s2), n))
                if s2[0] != j + (1 if d1["case"] == "I" else -1):
                    fail("phi j step", (j, lam, s2[0], d1["case"]))
                if (s2[0] - j) % 2 == 0:
                    fail("phi did not flip parity of j", (j, lam, s2))
                if d1["case"] == "I":
                    if d1.get("tstar_too_small"):
                        fail("phi Case I t* < max(a,mu)", (j, lam, d1["tstar_too_small"]))
                else:
                    if d1.get("negative_created_part"):
                        c2["neg_created"] += 1
                        fail("phi Case II negative created part", (j, lam, d1["created"]))
                # closure: phi must land back inside its own domain ...
                if not B.phi_domain(*s2):
                    fail("phi leaves its domain (lands in 0 x B)", (j, lam, s2, d1["case"]))
                    continue
                # ... and inside psi's domain, which the alternation needs
                if not B.psi_domain(*s2):
                    NOTES.append(dict(note="phi lands in 0 x A (psi's excluded set)",
                                      state=[j, list(lam)], image=[s2[0], list(s2[1])]))
                try:
                    s3, d2 = B.phi(*s2)
                except Exception as e:               # pragma: no cover
                    fail("phi^2 raised", (j, lam, s2, repr(e)))
                    continue
                if s3 != (j, lam):
                    fail("phi^2 != id", dict(state=[j, list(lam)], image=[s2[0], list(s2[1])],
                                             back=[s3[0], list(s3[1])],
                                             cases=[d1["case"], d2["case"]]))

            # ---- psi^2 = id, with closure, over psi's domain ----
            t0, m0, m2, m3 = B.residues(lam)
            if t0 + j > 0 or m2 > 0:
                sub = "Ia" if 5 * t0 + 5 * j - 3 >= m2 else "Ib"
            else:
                sub = "IIa" if m3 + 5 * j - 3 >= m0 else "IIb"
            cov["psi_" + sub] += 1
            if t0 > 0:
                cov["psi_t0_pos"] += 1
            if m2 > 0:
                cov["psi_m2_pos"] += 1
            if m0 == 0:
                cov["psi_m0_zero"] += 1
            if m3 == 0:
                cov["psi_m3_zero"] += 1
            if B.psi_domain(j, lam):
                cov["psi_domain"] += 1
                pw["psi"] += 1
                try:
                    s2, d1 = B.psi(j, lam)
                except Exception as e:               # pragma: no cover
                    fail("psi raised", (j, lam, repr(e)))
                    continue
                if not B._is_partition(s2[1]):
                    fail("psi output not a partition", (j, lam, s2))
                if B.weight(*s2) != n:
                    fail("psi changed the weight", (j, lam, s2, B.weight(*s2), n))
                if s2[0] != j + (1 if d1["sub"] in ("b",) else -1):
                    fail("psi j step", (j, lam, s2[0], d1["sub"]))
                if (s2[0] - j) % 2 == 0:
                    fail("psi did not flip parity of j", (j, lam, s2))
                if d1.get("negative_copy_count", 0) < 0:
                    fail("psi I(b) negative copy count", (j, lam, d1["negative_copy_count"]))
                if d1.get("nonpositive_created_part") is not None:
                    NOTES.append(dict(note="psi II(b) would create a non-positive part",
                                      state=[j, list(lam)], diag=d1["nonpositive_created_part"],
                                      in_domain=True))
                if d1.get("copies_of_5", 0) > 0:
                    cov["psi_Ib_copy_pos"] += 1
                if d1["case"] == "II" and d1["sub"] == "b" and d1.get("created"):
                    cov["psi_IIb_created"] += 1
                if d1["case"] == "II" and d1["sub"] == "a" and d1.get("nu") == 0:
                    cov["psi_IIa_deleted"] += 1
                if d1["case"] == "I" and d1["sub"] == "a" and any(
                        p % 5 == 0 and p == 5 for p in lam):
                    cov["psi_Ia_part_dropped"] += 1
                if d1["case"] == "II" and any(p == 1 for p in lam):
                    cov["phi_II_part_dropped"] += 1
                if d1["case"] == "I" and d1.get("ones_inserted", 0) > 0:
                    cov["phi_I_ones_pos"] += 1
                if not B.psi_domain(*s2):
                    fail("psi leaves its domain (lands in 0 x A)", (j, lam, s2, d1["sub"]))
                    continue
                if not B.phi_domain(*s2):
                    NOTES.append(dict(note="psi lands in 0 x B (phi's excluded set)",
                                      state=[j, list(lam)], image=[s2[0], list(s2[1])]))
                try:
                    s3, d2 = B.psi(*s2)
                except Exception as e:               # pragma: no cover
                    fail("psi^2 raised", (j, lam, s2, repr(e)))
                    continue
                if s3 != (j, lam):
                    fail("psi^2 != id", dict(state=[j, list(lam)], image=[s2[0], list(s2[1])],
                                             back=[s3[0], list(s3[1])],
                                             branches=[d1["case"] + d1["sub"],
                                                       d2["case"] + d2["sub"]]))
        per_weight[n] = pw
    c2["zmin0_sizes"] = dict(sorted(c2["zmin0_sizes"].items()))
    return cov, c2, per_weight


# ---------------------------------------------------------------------------
# (iii) the three printed examples of p.315
# ---------------------------------------------------------------------------


def printed_examples():
    out = []
    # (1) phi(2; 11,9,8,7,6,1,1,1) = (3; 10,9,7,2,2,2), a=4, mu=1, Case I
    s, d = B.phi(2, (11, 9, 8, 7, 6, 1, 1, 1))
    out.append(dict(which="(1) phi", input=[2, [11, 9, 8, 7, 6, 1, 1, 1]],
                    expected=[3, [10, 9, 7, 2, 2, 2]], got=[s[0], list(s[1])],
                    a=d["a"], mu=d["mu"], case=d["case"], printed_a=4, printed_mu=1,
                    printed_case="I", ok=(list(s) == [3, (10, 9, 7, 2, 2, 2)] and d["a"] == 4
                                          and d["mu"] == 1 and d["case"] == "I")))
    # (2) psi(-2; 15,14,9,9,8,8,8,5,5,4,3,2,1) = (-3; 14,10,9,9,8,8,8,4,3,2,2,1)
    s, d = B.psi(-2, (15, 14, 9, 9, 8, 8, 8, 5, 5, 4, 3, 2, 1))
    out.append(dict(which="(2) psi", input=[-2, [15, 14, 9, 9, 8, 8, 8, 5, 5, 4, 3, 2, 1]],
                    expected=[-3, [14, 10, 9, 9, 8, 8, 8, 4, 3, 2, 2, 1]],
                    got=[s[0], list(s[1])], t0=d["t0"], m2=d["m2"],
                    case=d["case"] + d["sub"], printed_t0=3, printed_m2=2,
                    printed_case="I(a)",
                    ok=(list(s) == [-3, (14, 10, 9, 9, 8, 8, 8, 4, 3, 2, 2, 1)]
                        and d["t0"] == 3 and d["m2"] == 2 and d["case"] == "I"
                        and d["sub"] == "a")))
    # (3) pi((4,1)) = (3,2) along the printed nine-state chain
    chain_printed = [(0, (4, 1)), (1, (1, 1, 1)), (0, (2, 1, 1, 1)), (-1, (1, 1)),
                     (0, (3, 1, 1)), (1, (2, 1)), (0, (2, 2, 1)), (1, (3,)),
                     (0, (3, 2))]
    out_state, steps, trace = B.pi_iterate((4, 1))
    got_chain = [(r["j"], r["lam"]) for r in trace]
    out.append(dict(which="(3) pi((4,1))", printed_chain=[[j, list(l)] for j, l in chain_printed],
                    got_chain=[[j, list(l)] for j, l in got_chain],
                    chain_matches=(tuple(got_chain) == tuple(chain_printed)),
                    got=[0, list(out_state)], expected=[0, [3, 2]],
                    steps=steps, Tinv=[list(B.Tinv((3, 2)))],
                    ok=(tuple(got_chain) == tuple(chain_printed) and out_state == (3, 2)
                        and B.Tinv((3, 2)) == (4, 1))))
    return out


# ---------------------------------------------------------------------------
# (v) per-weight statistics of the alternating path
# ---------------------------------------------------------------------------


def path_stats(NMAX):
    rows = []
    best = (None, None, -1)          # (n, lam, steps)
    worst_full_trace = None
    shortest_trace = None
    for n in range(NMAX + 1):
        objs = list(B.partitions(n))
        objs = [l for l in objs if B.in_A(l)]
        steps_list = []
        argmax = None
        for lam in objs:
            out, steps, trace = B.pi_iterate(lam)
            steps_list.append(steps)
            if argmax is None or steps > argmax[1]:
                argmax = (lam, steps, trace)
            if n == 2 and lam == (1, 1):
                shortest_trace = trace
        total = sum(steps_list)
        cnt = len(objs)
        rows.append(dict(
            n=n, A_count=cnt, steps_total=total,
            steps_max=(argmax[1] if argmax else 0),
            steps_mean_num=total, steps_mean_den=cnt,
            steps_mean=float(Fraction(total, cnt)) if cnt else 0.0,
            argmax_lam=list(argmax[0]) if argmax else [],
            n_argmax=sum(1 for s_ in steps_list if argmax and s_ == argmax[1]),
            states_visited_max=(argmax[1] + 1) if argmax else 1,
        ))
        if argmax and argmax[1] > best[2]:
            best = (n, argmax[0], argmax[1])
            worst_full_trace = argmax[2]
    return rows, best, worst_full_trace, shortest_trace


# ---------------------------------------------------------------------------
# shape of the Case-II admissible set, and the closed existence criterion
# ---------------------------------------------------------------------------


def admissible_shape(NMAX):
    """Tests two structural claims about the admissible z-set S.

    (S1) S is always a prefix {0,1,...,m}: no holes, so "Max" is never a maximum
         over a non-convex set and |S| = m+1.
    (S2) S is non-empty iff  a+2j-2 >= 0  and  lam(a+2j-1) <= t+5j-2.

    (S2) is the criterion that direction B of this swarm (member m1) derives
    from the monotonicity of  i |-> lam(i) - i; it is *checked* here, not
    assumed.  With (S2) the "does the maximum exist for every n" question of
    cycle 1 becomes two explicit inequalities."""
    out = dict(caseII=0, not_prefix=0, criterion_mismatch=0, size_ne_max_plus_1=0,
               witnesses=[])
    for n in range(NMAX + 1):
        for (j, lam) in B.states_of_weight(n):
            t = len(lam)
            a = B._phi_a(j, lam)
            la = B.lam_at(lam, a)
            mu = 2 * j + a - la
            lmu = B.lam_at(lam, mu)
            tstar = t + (1 if la == 0 else 0) + (1 if lmu == 0 else 0)
            if la + lmu >= 5 * j + tstar:
                continue
            out["caseII"] += 1
            S, _ep = B.case_ii_admissible_set(j, lam)
            if S != list(range(len(S))):
                out["not_prefix"] += 1
                if len(out["witnesses"]) < 5:
                    out["witnesses"].append(dict(kind="not_prefix", j=j, lam=list(lam), S=S))
            crit = (a + 2 * j - 2 >= 0) and (B.lam_at(lam, a + 2 * j - 1) <= t + 5 * j - 2)
            if bool(S) != crit:
                out["criterion_mismatch"] += 1
                if len(out["witnesses"]) < 5:
                    out["witnesses"].append(dict(kind="criterion", j=j, lam=list(lam),
                                                 S=S, crit=crit, a=a, t=t))
            if S and len(S) != S[-1] + 1:
                out["size_ne_max_plus_1"] += 1
    return out


# ---------------------------------------------------------------------------
# psi branch pairing: which branch does psi send each branch to?
# ---------------------------------------------------------------------------


def branch_pairing(NMAX):
    pair = {}
    examples = {}
    for n in range(NMAX + 1):
        for (j, lam) in B.states_of_weight(n):
            if not B.psi_domain(j, lam):
                continue
            s2, d = B.psi(j, lam)
            src = d["case"] + d["sub"]
            _n2, _l2 = s2
            t0, m0, m2, m3 = B.residues(_l2)
            if t0 + s2[0] > 0 or m2 > 0:
                dst = "Ia" if 5 * t0 + 5 * s2[0] - 3 >= m2 else "Ib"
            else:
                dst = "IIa" if m3 + 5 * s2[0] - 3 >= m0 else "IIb"
            pair[(src, dst)] = pair.get((src, dst), 0) + 1
            if (src, dst) not in examples:
                examples[(src, dst)] = dict(state=[j, list(lam)], image=[s2[0], list(s2[1])])
    return dict(counts={"%s->%s" % k: v for k, v in sorted(pair.items())},
                examples={"%s->%s" % k: v for k, v in sorted(examples.items())})


# ---------------------------------------------------------------------------
# independent counting routes (nothing here uses phi or psi)
# ---------------------------------------------------------------------------


def independent_counts(NMAX):
    """|A_n| and |D_n| by direct definitional enumeration, plus the Jacobi
    triple-product sum  sum_j (-1)^j p(n - P(j)), which uses the ordinary
    partition numbers p(m) instead of A- or D-parts.  The three agreeing is
    *not* the objective (equal counts prove nothing about naturalness); it is a
    consistency check on the sign/parity bookkeeping of the involutions."""
    p = [0] * (NMAX + 1)
    p[0] = 1
    for k in range(1, NMAX + 1):                     # p via Euler's recurrence
        tot = 0
        g = 1
        while True:
            g1 = g * (3 * g - 1) // 2
            g2 = g * (3 * g + 1) // 2
            if g1 > k and g2 > k:
                break
            sign = 1 if g % 2 == 1 else -1
            if g1 <= k:
                tot += sign * p[k - g1]
            if g2 <= k:
                tot += sign * p[k - g2]
            g += 1
        p[k] = tot
    rows = []
    for n in range(NMAX + 1):
        a = sum(1 for l in B.partitions(n) if B.in_A(l))
        d = sum(1 for l in B.partitions(n)
                if all(l[i] >= l[i + 1] + 2 for i in range(len(l) - 1)))
        jacobi = 0
        j = 0
        while B.pent(j) <= n:
            jacobi += (-1) ** j * p[n - B.pent(j)]
            j += 1
        j = -1
        while B.pent(j) <= n:
            jacobi += (-1) ** j * p[n - B.pent(j)]
            j -= 1
        rows.append(dict(n=n, A=a, D=d, jacobi=jacobi,
                         agree=(a == d == jacobi)))
    return rows


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    results = dict(nmax=NMAX, generated=time.strftime("%Y-%m-%d %H:%M:%S"))

    cov, c2, per_weight = census(NMAX)
    results["census"] = cov
    results["case_ii"] = c2
    results["per_weight_state_counts"] = per_weight
    results["exhaustive_ok"] = not FAILS

    results["examples"] = printed_examples()
    results["psi_branch_pairing"] = branch_pairing(NMAX)
    shape = admissible_shape(NMAX)
    results["admissible_shape"] = shape
    if shape["not_prefix"] or shape["criterion_mismatch"] or shape["size_ne_max_plus_1"]:
        fail("admissible-set shape", shape)
    ic = independent_counts(NMAX)
    results["independent_counts"] = ic
    bad = [r for r in ic if not r["agree"]]
    for r in bad:
        fail("counting routes disagree", r)

    rows, best, long_trace, short_trace = path_stats(NMAX)
    results["path_stats"] = rows
    results["path_extremum"] = dict(n=best[0], lam=list(best[1]), steps=best[2])

    # two complete labelled traces
    lines = []
    lines.append("# Long trace: the A_n object with the largest number of steps, n = %d" % best[0])
    lines.append("# object: %s in A_%d ; %d phi/psi applications ; %d states visited"
                 % (str(best[1]), best[0], best[2], best[2] + 1))
    lines.append("# image in B_n: %s ; T^-1 image in D_n: %s"
                 % (str(long_trace[-1]["lam"]), str(B.Tinv(long_trace[-1]["lam"]))))
    for r in long_trace:
        lines.append("  %4d  %-4s  j=%+d  lam=%-60s %s"
                     % (r["step"], r["via"], r["j"], str(r["lam"]), r.get("case", "")))
    lines.append("")
    lines.append("# Short trace: (1,1) in A_2, the smallest object needing a phi/psi step")
    for r in short_trace:
        lines.append("  %4d  %-4s  j=%+d  lam=%-60s %s"
                     % (r["step"], r["via"], r["j"], str(r["lam"]), r.get("case", "")))
    with open("traces_cycle2.txt", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    results["trace_files"] = "traces_cycle2.txt"

    results["failures"] = FAILS
    results["notes"] = NOTES
    results["elapsed_seconds"] = round(time.time() - t0, 2)

    with open("results_cycle2.json", "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True, default=str)

    # ---- console summary ----
    print("NMAX =", NMAX)
    print("states in X(n), n <= %d : %d" % (NMAX, cov["states"]))
    print("  phi domain %d  (excluded 0 x B: %d)   psi domain %d  (excluded 0 x A: %d)"
          % (cov["phi_domain"], cov["states"] - cov["phi_domain"],
             cov["psi_domain"], cov["states"] - cov["psi_domain"]))
    print("  branch coverage phi I/II = %d/%d ; psi Ia/Ib/IIa/IIb = %d/%d/%d/%d"
          % (cov["phi_caseI"], cov["phi_caseII"], cov["psi_Ia"], cov["psi_Ib"],
             cov["psi_IIa"], cov["psi_IIb"]))
    print("  j>0 %d  j<0 %d  j=0 %d ; j even %d  j odd %d"
          % (cov["j_pos"], cov["j_neg"], cov["j_zero"], cov["j_even"], cov["j_odd"]))
    print("  t=0 (empty lam) %d ; repeated parts %d ; phi virtual-zero %d (a:%d mu:%d)"
          % (cov["t0_empty_lam"], cov["repeated_parts"], cov["phi_virtual_zero"],
             cov["phi_virtual_a"], cov["phi_virtual_mu"]))
    print("  phi Case I with a=mu : %d" % cov["phi_a_eq_mu"])
    print("  psi: t0>0 %d ; m2>0 %d ; m0=0 %d ; m3=0 %d ; II(b) creating %d ; II(a) nu=0 %d"
          % (cov["psi_t0_pos"], cov["psi_m2_pos"], cov["psi_m0_zero"], cov["psi_m3_zero"],
             cov["psi_IIb_created"], cov["psi_IIa_deleted"]))
    print("  case-II states %d (in phi domain %d)"
          % (c2["total_caseII"], c2["in_domain_caseII"]))
    print("  admissible set EMPTY : %d (in domain %d)   [expected 0 / 0]"
          % (c2["empty_admissible"], c2["empty_admissible_in_domain"]))
    print("  a+2j-2 < 0          : %d (in domain %d)" % (c2["hi_neg"], c2["hi_neg_in_domain"]))
    print("  selected m range    : [%s, %s] ; |S| range [%s, %s]"
          % (c2["min_selected_m"], c2["max_selected_m"], c2["setsize_min"], c2["setsize_max"]))
    print("  z>=0 vs all-int z   : %d disagreements" % c2["domain_disagreements"])
    print("  negative created part (phi II): %d" % c2["neg_created"])
    for ex in results["examples"]:
        print("  example %-16s ok=%s" % (ex["which"], ex["ok"]))
    print("path stats (n: count, max, mean):")
    for r in rows:
        print("   n=%2d  |A_n|=%3d  max=%3d  mean=%s = %.3f  argmax=%s"
              % (r["n"], r["A_count"], r["steps_max"],
                 Fraction(r["steps_mean_num"], r["steps_mean_den"]) if r["A_count"] else "-",
                 r["steps_mean"], r["argmax_lam"]))
    sh = results["admissible_shape"]
    print("admissible z-set over all %d Case-II states: not a prefix %d ; "
          "size != max+1 %d ; criterion-mismatches %d"
          % (sh["caseII"], sh["not_prefix"], sh["size_ne_max_plus_1"],
             sh["criterion_mismatch"]))
    print("psi branch pairing:")
    for k, v in results["psi_branch_pairing"]["counts"].items():
        print("   %-9s %d" % (k, v))
    print("independent counts: A_n vs D_n vs sum_j (-1)^j p(n-P(j)) ; all agree:",
          all(r["agree"] for r in ic))
    print("   n: |A_n| ; n=24 -> %d ; n=30 -> %d"
          % (ic[24]["A"], ic[30]["A"]))
    print("OVERALL exhaustive checks passed:", not FAILS)
    if FAILS:
        print("FAILURES:", len(FAILS))
        for f in FAILS[:10]:
            print("  ", f)
    if NOTES:
        print("NOTES:", len(NOTES))
        for f in NOTES[:10]:
            print("  ", f)
    print("elapsed", results["elapsed_seconds"], "s")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
