#!/usr/bin/env python3
"""
negative_control.py -- sensitivity tests for the audit of direction A.

`run_audit.py` reports zero defects over all 66 658 in-domain states of weight
<= 30.  A zero is only meaningful if the harness would have reported a
non-zero, so this program reruns the same machinery against deliberately
wrong readings of the printed rules and records the damage.

Variants (all on the SAME states, same code path, only the disputed line
changed):

  PHI-1  phi Case I deletes *positions* in the sequence padded at the END to
         length t*, instead of deleting the parts lam(a), lam(mu).  This is the
         reading the phrase "delete the slots at a and mu (a slot beyond t
         holds a virtual 0)" invites if "a slot beyond t" is read as "appended".
  PHI-2  phi Case II with the lower bound z >= 1 and a fallback of m = 0 when
         that set is empty  [the cycle-1 rule of DECISIONS.md D-3, which
         supervisor correction C2 says is behaviourally identical to z >= 0].
  PHI-3  phi Case II with the lower bound z >= 1 and no fallback.
  PSI-1  the I(a) tie broken the other way (equality 5t0+5j-3 = m2 -> I(b)).
  PSI-2  the II(a) tie broken the other way (equality m3+5j-3 = m0 -> II(b)).
  PSI-3  II(a) with nu = m3+5j-3 = 0 keeping a created part of 0.

Usage: python3 negative_control.py [NMAX]   (default 18, the range D-3a used)
Writes ctrl_cycle2.json.  Exit code 0 always: the point is the counts.
"""

import json
import sys

import bz82_audit as B

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18


# ---------------------------------------------------------------------------
# phi variants
# ---------------------------------------------------------------------------


def phi_ph1(j, lam):
    """PHI-1: Case I by padded-at-the-end positions."""
    t = len(lam)
    a = B._phi_a(j, lam)
    la = B.lam_at(lam, a)
    mu = 2 * j + a - la
    lmu = B.lam_at(lam, mu)
    tstar = t + (1 if la == 0 else 0) + (1 if lmu == 0 else 0)
    if la + lmu >= 5 * j + tstar:                       # Case I
        ones = la + lmu - 5 * j - tstar
        vals = [B.lam_at(lam, y) + 1 for y in range(1, tstar + 1) if y not in (a, mu)]
        return (j + 1, tuple(sorted(vals + [1] * ones, reverse=True))), "I"
    # Case II is unaffected by the PHI-1 dispute: delegate to the correct rule.
    return B.phi(j, lam)[0], "II"


def phi_ph2(j, lam):
    """PHI-2: z >= 1 with fallback m = 0 (the cycle-1 rule of D-3)."""
    t = len(lam)
    a = B._phi_a(j, lam)
    la = B.lam_at(lam, a)
    mu = 2 * j + a - la
    lmu = B.lam_at(lam, mu)
    tstar = t + (1 if la == 0 else 0) + (1 if lmu == 0 else 0)
    if la + lmu >= 5 * j + tstar:
        return B.phi(j, lam)[0], "I"
    hi = a + 2 * j - 2
    S1 = [z for z in range(1, hi + 1) if z + B.lam_at(lam, a + 2 * j - 1 - z) <= t + 5 * j - 2]
    m = max(S1) if S1 else 0
    return _phi_case2_assemble(j, lam, m), "II"


def phi_ph3(j, lam):
    """PHI-3: z >= 1, no fallback (raises when empty)."""
    t = len(lam)
    a = B._phi_a(j, lam)
    la = B.lam_at(lam, a)
    mu = 2 * j + a - la
    lmu = B.lam_at(lam, mu)
    tstar = t + (1 if la == 0 else 0) + (1 if lmu == 0 else 0)
    if la + lmu >= 5 * j + tstar:
        return B.phi(j, lam)[0], "I"
    hi = a + 2 * j - 2
    S1 = [z for z in range(1, hi + 1) if z + B.lam_at(lam, a + 2 * j - 1 - z) <= t + 5 * j - 2]
    if not S1:
        raise ValueError("empty (z>=1)")
    return _phi_case2_assemble(j, lam, max(S1)), "II"


def _phi_case2_assemble(j, lam, m):
    t = len(lam)
    p2 = t + 5 * j - 3 - m
    parts = [p - 1 for p in lam if p - 1 > 0]
    parts += [p for p in (m, p2) if p > 0]
    return (j - 1, tuple(sorted(parts, reverse=True)))


# ---------------------------------------------------------------------------
# psi variants
# ---------------------------------------------------------------------------


def psi_variant(j, lam, ia_tie="ge", iia_tie="ge", iia_keep_zero=False):
    t0, m0, m2, m3 = B.residues(lam)
    if t0 + j > 0 or m2 > 0:
        take_a = (5 * t0 + 5 * j - 3 >= m2) if ia_tie == "ge" else (5 * t0 + 5 * j - 3 > m2)
        if take_a:                                        # I(a)
            nu = 5 * t0 + 5 * j - 3
            parts = [p - 5 for p in lam if p % 5 == 0 and p - 5 > 0]
            parts += [p for p in lam if p % 5 != 0]
            if nu > 0:
                parts.append(nu)
            return (j - 1, tuple(sorted(parts, reverse=True)))
        num = m2 - 5 * j - 2 - 5 * t0                        # I(b)
        k = num // 5
        if k < 0:
            raise ValueError("I(b) with negative copy count")
        parts, dropped = [], False
        for p in lam:
            if not dropped and p == m2:
                dropped = True
                continue
            parts.append(p + 5 if p % 5 == 0 else p)
        parts += [5] * k
        return (j + 1, tuple(sorted(parts, reverse=True)))
    # Case II
    take_a = (m3 + 5 * j - 3 >= m0) if iia_tie == "ge" else (m3 + 5 * j - 3 > m0)
    if take_a:                                               # II(a)
        nu = m3 + 5 * j - 3
        parts, replaced = [], False
        for p in lam:
            if not replaced and p == m3:
                replaced = True
                if nu > 0 or (nu == 0 and iia_keep_zero):
                    parts.append(nu)
                continue
            parts.append(p)
        return (j - 1, tuple(sorted(parts, reverse=True)))
    nu = m0 - 5 * j - 2                                       # II(b)
    if m0 == 0:
        return (j + 1, tuple(sorted(list(lam) + ([nu] if nu > 0 else []), reverse=True)))
    parts, replaced = [], False
    for p in lam:
        if not replaced and p == m0:
            replaced = True
            if nu > 0:
                parts.append(nu)
            continue
        parts.append(p)
    return (j + 1, tuple(sorted(parts, reverse=True)))


# ---------------------------------------------------------------------------
# drivers
# ---------------------------------------------------------------------------


def phi_defects(fn, NMAX, weight_check=True):
    """Count in-domain states of weight <= NMAX where fn fails to be an
    involution with closure (and, if asked, the weight identity)."""
    bad = dict(weight=0, not_partition=0, raised=0, closure=0, square=0, total=0)
    first = {}
    for n in range(NMAX + 1):
        for (j, lam) in B.states_of_weight(n):
            if not B.phi_domain(j, lam):
                continue
            bad["total"] += 1
            try:
                s2, case = fn(j, lam)
            except Exception as e:
                bad["raised"] += 1
                first.setdefault("raised", [j, list(lam), repr(e)[:80]])
                continue
            if not B._is_partition(s2[1]):
                bad["not_partition"] += 1
                first.setdefault("not_partition", [j, list(lam), [s2[0], list(s2[1])]])
                continue
            if weight_check and B.weight(*s2) != n:
                bad["weight"] += 1
                first.setdefault("weight", [j, list(lam), [s2[0], list(s2[1])],
                                            B.weight(*s2), n])
            if not B.phi_domain(*s2):
                bad["closure"] += 1
                first.setdefault("closure", [j, list(lam), [s2[0], list(s2[1])]])
                continue
            try:
                s3, _ = fn(*s2)
            except Exception as e:
                bad["square"] += 1
                first.setdefault("square", [j, list(lam), [s2[0], list(s2[1])], "raised"])
                continue
            if s3 != (j, lam):
                bad["square"] += 1
                first.setdefault("square", [j, list(lam), [s2[0], list(s2[1])],
                                            [s3[0], list(s3[1])]])
    return bad, first


def psi_defects(kw, NMAX):
    bad = dict(weight=0, not_partition=0, raised=0, closure=0, square=0, total=0)
    first = {}
    for n in range(NMAX + 1):
        for (j, lam) in B.states_of_weight(n):
            if not B.psi_domain(j, lam):
                continue
            bad["total"] += 1
            try:
                s2 = psi_variant(j, lam, **kw)
            except Exception as e:
                bad["raised"] += 1
                first.setdefault("raised", [j, list(lam), repr(e)[:80]])
                continue
            if not B._is_partition(s2[1]):
                bad["not_partition"] += 1
                first.setdefault("not_partition", [j, list(lam), [s2[0], list(s2[1])]])
                continue
            if B.weight(*s2) != n:
                bad["weight"] += 1
                first.setdefault("weight", [j, list(lam), [s2[0], list(s2[1])],
                                            B.weight(*s2), n])
            if not B.psi_domain(*s2):
                bad["closure"] += 1
                first.setdefault("closure", [j, list(lam), [s2[0], list(s2[1])]])
                continue
            try:
                s3 = psi_variant(s2[0], s2[1], **kw)
            except Exception:
                bad["square"] += 1
                first.setdefault("square", [j, list(lam), [s2[0], list(s2[1])], "raised"])
                continue
            if s3 != (j, lam):
                bad["square"] += 1
                first.setdefault("square", [j, list(lam), [s2[0], list(s2[1])],
                                            [s3[0], list(s3[1])]])
    return bad, first


def z_domain_census(NMAX):
    """PHI-2 / PHI-3 against PHI (z >= 0): on which Case-II states do the
    readings differ, and how often is the z >= 1 admissible set empty?"""
    out = dict(caseII=0, zge1_empty=0, zge1_empty_in_domain=0,
               zge1_fallback_differs_from_z0=0, witnesses=[])
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
            in_dom = B.phi_domain(j, lam)
            hi = a + 2 * j - 2
            S0 = [z for z in range(0, hi + 1)
                  if z + B.lam_at(lam, a + 2 * j - 1 - z) <= t + 5 * j - 2]
            S1 = [z for z in range(1, hi + 1)
                  if z + B.lam_at(lam, a + 2 * j - 1 - z) <= t + 5 * j - 2]
            if not S1:
                out["zge1_empty"] += 1
                if in_dom:
                    out["zge1_empty_in_domain"] += 1
                m1 = 0
            else:
                m1 = max(S1)
            m0 = max(S0) if S0 else None
            if m1 != m0:
                out["zge1_fallback_differs_from_z0"] += 1
                if len(out["witnesses"]) < 8:
                    out["witnesses"].append(dict(j=j, lam=list(lam), n=n,
                                                 m_zge1_fallback=m1, m_zge0=m0,
                                                 in_phi_domain=in_dom))
    return out


def main():
    res = dict(nmax=NMAX, generated=__import__("time").strftime("%Y-%m-%d %H:%M:%S"))
    # ---- the correct reading, as a baseline (must be all zeros) ----
    b, f = phi_defects(lambda j, l: (B.phi(j, l)[0], B.phi(j, l)[1]["case"]), NMAX)
    res["baseline_phi"] = dict(defects=b, first=f)
    b2, f2 = psi_defects({}, NMAX)
    res["baseline_psi"] = dict(defects=b2, first=f2)

    # ---- PHI-1 ----
    b, f = phi_defects(phi_ph1, NMAX)
    res["PHI-1_position_deletion"] = dict(defects=b, first=f)
    # ---- PHI-2 / PHI-3 ----
    b, f = phi_defects(phi_ph2, NMAX)
    res["PHI-2_zge1_with_fallback"] = dict(defects=b, first=f)
    b, f = phi_defects(phi_ph3, NMAX)
    res["PHI-3_zge1_no_fallback"] = dict(defects=b, first=f)
    res["z_domain_census"] = z_domain_census(NMAX)
    # ---- PSI-1/2/3 ----
    for name, kw in [("PSI-1_flip_Ia_tie", dict(ia_tie="gt")),
                     ("PSI-2_flip_IIa_tie", dict(iia_tie="gt")),
                     ("PSI-3_IIa_keep_zero", dict(iia_keep_zero=True))]:
        b, f = psi_defects(kw, NMAX)
        res[name] = dict(defects=b, first=f)

    with open("ctrl_cycle2.json", "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=str)

    def show(k):
        d = res[k]["defects"]
        tot = d["weight"] + d["not_partition"] + d["raised"] + d["closure"] + d["square"]
        print("  %-26s in-domain %6d  DEFECTIVE %5d   (weight %d, raise %d, "
              "closure %d, square %d)  first=%s"
              % (k, d["total"], tot, d["weight"], d["raised"], d["closure"],
                 d["square"], res[k]["first"].get("square")
                 or res[k]["first"].get("weight") or res[k]["first"].get("raised")))
    print("NMAX =", NMAX)
    for k in ["baseline_phi", "PHI-1_position_deletion", "PHI-2_zge1_with_fallback",
              "PHI-3_zge1_no_fallback", "baseline_psi", "PSI-1_flip_Ia_tie",
              "PSI-2_flip_IIa_tie", "PSI-3_IIa_keep_zero"]:
        show(k)
    z = res["z_domain_census"]
    print("phi Case-II states:", z["caseII"], "| z>=1 set empty:", z["zge1_empty"],
          "(in phi's domain:", z["zge1_empty_in_domain"], ")")
    print("z>=1-with-fallback-0 vs printed z>=0, differing m:",
          z["zge1_fallback_differs_from_z0"])
    print("witnesses:", z["witnesses"][:3])


if __name__ == "__main__":
    main()
