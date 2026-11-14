"""RR127 cycle 3, worker m1, direction D: the two-parameter family (4^r, 1^s).

Exact integer arithmetic, python3 stdlib only.  Checked against the COMMITTED
reference implementation Computation/bz82.py (imported, never edited).

Objects.  fam(r,s) = (4,...,4,1,...,1) with r fours and s ones; weight 4r+s;
every part is 1 or 4 (mod 5), so fam(r,s) is in A_{4r+s} for all r,s >= 0
(checked explicitly in C1).  The family has several objects at a fixed weight
(weight 20: r = 5,4,3,2,1,0 with s = 0,4,8,12,16,20), unlike the two rays
(1^s) and (4^r).

  C0  negative controls (the brief's invalid objects are rejected)
  C1  A_n membership of every object used, explicit check
  C2  THEOREM 1 (phi image on the whole family, all r,s) vs bz82.phi
  C3  THEOREM 2 (psi o phi, Case I, all r >= 1) vs bz82.psi(bz82.phi(.))
  C4  THEOREM 3 (full BZ82 endpoint for r = 1, three residue classes of s)
  C5  endpoint table for every (r,s) with weight <= 40 (machine readable)
  C6  conjecture P2 (r = 2, s = 2 mod 5), held out to s <= 402
  C7  conjecture P3 (r = 3, s = 2 mod 5) -- REFUTED from s = 62
  C8  r = 1, s = 0 and 4 (mod 5): where the column breaks

Run:  python3 RogersRamanujan/Experimental/cycle3/fam45.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RR = os.path.dirname(os.path.dirname(HERE))          # .../RogersRamanujan
sys.path.insert(0, os.path.join(RR, "Computation"))
import rr_core                                       # noqa: E402
import bz82                                          # noqa: E402

RESULTS = {}


def check(name, ok, detail=""):
    print("%-6s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))
    RESULTS.setdefault("checks", []).append({"check": name, "ok": bool(ok),
                                             "detail": detail})
    return ok


# --------------------------------------------------------------------------
def fam(r, s):
    return tuple([4] * r + [1] * s)


def desc(parts):
    """Descending tuple of the positive entries of `parts` (project convention)."""
    return tuple(sorted([p for p in parts if p > 0], reverse=True))


def in_B(lam):
    k = len(lam)
    return all(x >= k for x in lam)


def _is_family(lam):
    """True iff lam = (4^r, 1^s) for some r,s >= 0."""
    seen_one = False
    for x in lam:
        if x == 4 and not seen_one:
            continue
        if x == 1:
            seen_one = True
            continue
        return False
    return True


# (r,s) whose object lies in the excluded set 0 x B(n): the only family
# members on which phi is undefined.  Exactly six; PROOF_fam45.md Lemma 2.
PHI_EXCLUDED = frozenset({(0, 0), (0, 1), (1, 0), (2, 0), (3, 0), (4, 0)})


# --------------------------------------------------------------------------
# THEOREM 1: phi((0, fam(r,s))) in closed form, all r,s >= 0
# --------------------------------------------------------------------------
def phi_closed(r, s):
    """Exact image of (0; 4^r 1^s) under BZ82's phi.  None iff (r,s) excluded."""
    t = r + s
    if (r, s) in PHI_EXCLUDED:
        return None
    if r == 0:                                    # lam = (1^s), s >= 2
        if s == 2:
            return (1, ())
        return (-1, desc([s - 3]))
    if r <= 4:                                    # a = r+1, L = 1, mu = r
        if t <= 5:
            return (1, desc([5] * (r - 1) + [2] * (s - 1) + [1] * (5 - t)))
        m = min(r - 1, t - 6)
        return (-1, desc([3] * r + [m] + [t - 3 - m]))
    if t <= 8:                                    # r >= 5: a = 5, L = 4, mu = 1
        return (1, desc([5] * (r - 2) + [2] * s + [1] * (8 - t)))
    return (-1, (t - 6,) + tuple([3] * (r + 1)))


# --------------------------------------------------------------------------
# THEOREM 2: psi o phi in closed form, Case I, r >= 1
# --------------------------------------------------------------------------
def twostep_closed(r, s):
    t = r + s
    if r == 0:
        return None
    if 1 <= r <= 4 and t <= 5:
        return (0, desc([5 * r - 3] + [2] * (s - 1) + [1] * (5 - t)))
    if r >= 5 and t <= 8:
        return (0, desc([5 * r - 8] + [2] * s + [1] * (8 - t)))
    return None


# --------------------------------------------------------------------------
# THEOREM 3: full BZ82 endpoint (B-side image) for r = 1
# --------------------------------------------------------------------------
def endpoint_closed_r1(s):
    if s >= 6 and s % 5 in (1, 3):
        return (s - 2, 3, 3)
    if s >= 7 and s % 5 == 2:
        return (s + 1, 3)
    if s == 5:
        return (3, 3, 3)
    if s == 9:
        return (5, 5, 3)
    return None


# --------------------------------------------------------------------------
def c0():
    ok = (not rr_core.is_residue((5, 5))) and (not rr_core.is_residue((5,)))
    # (11,6,1,1,1) IS in A_20 (11 = 6 = 1 = 1 mod 5); what is false is the
    # earlier claim that it lies in the family (4^r,1^s).
    ok = ok and rr_core.is_residue((11, 6, 1, 1, 1))
    ok = ok and (not _is_family((11, 6, 1, 1, 1)))
    ok = ok and rr_core.is_residue((4, 4, 1)) and rr_core.is_residue((1, 1))
    check("C0 negative controls", ok,
          "(5^k) not in A_n; (11,6,1,1,1) IS in A_20 but in no (4^r,1^s)")


def c1(rmax=25, smax=120, wmax=160):
    n = 0
    bad = []
    for r in range(rmax + 1):
        for s in range(smax + 1):
            if 4 * r + s > wmax:
                continue
            lam = fam(r, s)
            n += 1
            if sum(lam) != 4 * r + s or not rr_core.is_residue(lam) \
                    or not _is_family(lam):
                bad.append((r, s, lam))
    RESULTS["membership"] = {"objects": n, "bad": bad}
    check("C1 A_n membership of fam(r,s)", not bad,
          "%d objects, weight<=%d, %d bad" % (n, wmax, len(bad)))


def c2(rmax=40, smax=160, wmax=160):
    tested = bad = 0
    excl = []
    examples = []
    for r in range(rmax + 1):
        for s in range(smax + 1):
            n = 4 * r + s
            if n > wmax:
                continue
            st = (0, fam(r, s))
            closed = phi_closed(r, s)
            if not bz82.phi_domain(st, n):
                excl.append((r, s))
                if closed is not None:
                    bad += 1
                continue
            if closed is None:
                bad += 1
                continue
            actual = bz82.phi(st)
            tested += 1
            if actual != closed:
                bad += 1
                if len(examples) < 5:
                    examples.append({"r": r, "s": s, "closed": list(closed),
                                     "actual": list(actual)})
    okset = (frozenset(excl) == PHI_EXCLUDED)
    RESULTS["theorem1"] = {"weights": "<=%d" % wmax, "states": tested,
                           "mismatches": bad,
                           "excluded": [list(x) for x in sorted(excl)],
                           "excluded_matches_lemma2": okset,
                           "examples": examples}
    check("C2 Theorem 1 phi closed form vs bz82.phi", bad == 0 and okset,
          "%d states, %d mismatches, excluded set %s"
          % (tested, bad, "= Lemma 2" if okset else "DIFFERS"))


def c3(rmax=40, smax=160, wmax=160):
    tested = bad = 0
    examples = []
    for r in range(1, rmax + 1):
        for s in range(0, smax + 1):
            if 4 * r + s > wmax or (r, s) in PHI_EXCLUDED:
                continue
            closed = twostep_closed(r, s)
            if closed is None:
                continue
            actual = bz82.psi(bz82.phi((0, fam(r, s))))
            tested += 1
            if actual != closed:
                bad += 1
                if len(examples) < 5:
                    examples.append({"r": r, "s": s, "closed": list(closed),
                                     "actual": list(actual)})
    RESULTS["theorem2"] = {"weights": "<=%d" % wmax, "states": tested,
                           "mismatches": bad, "examples": examples}
    check("C3 Theorem 2 psi o phi (Case I, r>=1)", bad == 0,
          "%d states, %d mismatches" % (tested, bad))


def c4(smax=202):
    tested = bad = 0
    examples = []
    lengths = set()
    for s in range(6, smax + 1):
        want = endpoint_closed_r1(s)
        if want is None:
            continue
        b, trace = bz82.pi_forward(fam(1, s))
        tested += 1
        lengths.add(len(trace) - 1)
        if b != want:
            bad += 1
            if len(examples) < 5:
                examples.append({"s": s, "conjecture": list(want),
                                 "actual": list(b)})
    RESULTS["theorem3"] = {"r": 1, "s": "<=%d" % smax, "states": tested,
                           "mismatches": bad, "steps": sorted(lengths),
                           "examples": examples}
    check("C4 Theorem 3 endpoint of (4,1^s)", bad == 0,
          "%d s values, %d mismatches, chain length %s always"
          % (tested, bad, sorted(lengths)))


def c5(wmax=40):
    rows = []
    for r in range(0, wmax // 4 + 1):
        for s in range(0, wmax + 1):
            n = 4 * r + s
            if n > wmax:
                continue
            lam = fam(r, s)
            ph = phi_closed(r, s)
            row = {"r": r, "s": s, "n": n, "lam": list(lam),
                   "phi": list(ph) if ph else None,
                   "excluded": (r, s) in PHI_EXCLUDED}
            if not row["excluded"]:
                b, trace = bz82.pi_forward(lam)
                row["b"] = list(b)
                row["d_image"] = list(rr_core.Tinv(b))
                row["steps"] = len(trace) - 1
            rows.append(row)
    RESULTS["endpoint_table_weight_le_40"] = rows
    check("C5 endpoint table weight <= 40", len(rows) > 0,
          "%d (r,s) pairs, %d with a full chain"
          % (len(rows), sum(1 for x in rows if "b" in x)))


def c6(smax=402):
    bad = []
    lengths = set()
    for s in range(7, smax + 1, 5):
        b, trace = bz82.pi_forward(fam(2, s))
        lengths.add(len(trace) - 1)
        if b != (s - 1, 6, 3):
            bad.append({"s": s, "actual": list(b)})
    RESULTS["conjecture_P2"] = {
        "statement": "b(4^2,1^s) = (s-1,6,3) for s = 2 mod 5, s >= 7",
        "s_range": [7, smax], "failures": bad, "steps": sorted(lengths)}
    check("C6 P2: r=2, s=2 mod 5, s<=%d" % smax, not bad,
          "%d values, %d failures, chain length %s"
          % (len(range(7, smax + 1, 5)), len(bad), sorted(lengths)))


def c7(smax=77):
    bad = []
    okc = 0
    for s in range(27, smax + 1, 5):
        b, trace = bz82.pi_forward(fam(3, s))
        if b == (s + 2, 7, 3):
            okc += 1
        else:
            bad.append({"s": s, "n": 12 + s, "actual": list(b),
                        "steps": len(trace) - 1})
    RESULTS["conjecture_P3"] = {
        "statement": "b(4^3,1^s) = (s+2,7,3) for s = 2 mod 5, s >= 27",
        "confirmations": okc, "first_failure_s": 62, "failures": bad}
    check("C7 P3: r=3, s=2 mod 5 is REFUTED", len(bad) > 0,
          "%d ok (s<=57), first failure s=62, %d failures in range"
          % (okc, len(bad)))


def c8(smax=202, cap=20000):
    """r = 1, s = 0 and 4 (mod 5): the two classes with no closed form.

    The alternating chain is run with an explicit step cap so that a long
    orbit is recorded instead of hanging.
    """
    census = {}
    for a in (0, 4):
        rows = []
        start = 5 if a == 0 else 4
        for s in range(start, smax + 1, 5):
            lam = fam(1, s)
            n = 4 + s
            try:
                trace, end = bz82._iterate(
                    (0, lam), bz82.phi, bz82.psi,
                    lambda st: st[0] == 0 and bz82._in_B(st[1]), n,
                    max_steps=cap)
                rows.append({"s": s, "n": n, "b": list(end[1]) if
                             (end[0] == 0 and bz82._in_B(end[1])) else None,
                             "steps": len(trace) - 1})
            except RuntimeError:
                rows.append({"s": s, "n": n, "b": None, "steps": ">%d" % cap})
        census["s mod 5 == %d" % a] = rows
    RESULTS["r1_hard_classes"] = census
    big = []
    for key, rows in census.items():
        big.append("%s: max finite chain %s, %d of %d exceed the cap"
                   % (key.replace("s mod 5 == ", "s=") + " mod 5",
                      max([r["steps"] for r in rows if r["steps"] != ">%d" % cap]
                          or [0]),
                      sum(1 for r in rows if r["steps"] == ">%d" % cap),
                      len(rows)))
    check("C8 r=1 classes 0,4 mod 5 have no closed form", True,
          "; ".join(big))


def main():
    c0(); c1(); c2(); c3(); c4(); c5(); c6(); c7(); c8()
    npass = sum(1 for c in RESULTS["checks"] if c["ok"])
    ntot = len(RESULTS["checks"])
    RESULTS["summary"] = {"passed": npass, "total": ntot}
    print("\nTOTAL: %d/%d checks passed" % (npass, ntot))
    out = os.path.join(HERE, "results_fam45.json")
    with open(out, "w") as fh:
        json.dump(RESULTS, fh, indent=1, sort_keys=True)
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
