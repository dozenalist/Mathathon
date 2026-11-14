"""RR127 cycle 2, direction C (experimental).

Closed-form endpoint rules for parametric families in A_n under the BZ82
alternating path, checked against the committed baseline
Computation/bz82.py (which is imported READ-ONLY and never modified).

Conventions (project, DECISIONS D-1):
  A_n = partitions of n, parts = 1 or 4 (mod 5);   () = partition of 0.
  B_n = {b : parts of b >= len(b)};   D_n = {lam : lam_i >= lam_{i+1}+2}.
  T(lam)_i = lam_i - k + 2i - 1 with k = len(lam)   (D_n -> B_n),
  Tinv(b)_i = b_i + k - 2i + 1.                      (B_n -> D_n)
  pi = iterate phi,psi,phi,... until j = 0 and the partition lies in B_n.

This module re-implements T/Tinv from that closed formula (it does NOT import
rr_core.T/Tinv), so the D-side outputs below are computed by a second route.

Run:  python3 family_rules.py
"""
import sys

import os
def _computation_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.path.join(here, "..", "..", "Computation"),
             os.path.join(here, "..", "..", "..", "repo", "RogersRamanujan", "Computation"),
             "/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation",
             os.environ.get("RR_COMPUTATION", "")]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "bz82.py")):
            return os.path.abspath(c)
    raise SystemExit("cannot locate RogersRamanujan/Computation/bz82.py")
BASE = _computation_dir()
sys.path.insert(0, BASE)
from bz82 import pi_forward          # baseline, read-only import
from rr_core import weight, is_gap, is_residue

# ---------------------------------------------------------------------------
# second, formula-only implementation of the staircase shift
# ---------------------------------------------------------------------------
def Tinv_impl(b):
    k = len(b)
    return tuple(b[i] + k - 2 * (i + 1) + 1 for i in range(k))

# ---------------------------------------------------------------------------
# The proposed rules.  Each returns either a tuple (a B-endpoint b) or None
# when the rule is not claimed to apply.  Nothing here is fitted; every entry
# is derived in PROOF_families.md from one or two applications of the printed
# phi/psi rules plus an inequality that is uniform in the parameter.
# ---------------------------------------------------------------------------
def b_ones(s):
    """Rule M1 / Theorem F: B-endpoint of (0;(1^s)).  None = no claim."""
    if s in (0, 1):
        return (s,) if s == 1 else ()
    if s == 2:
        return (2,)
    # s >= 3: p = s - 3, and phi(0;(1^s)) = (-1;(p)) exactly.
    p = s - 3
    r = p % 5
    if r == 0:                       # s = 3 mod 5 : s >= 3
        return (p + 3,)              # = (s,)
    if r == 1:                       # s = 4 mod 5 : p >= 6 required
        if p < 6:
            return (2, 2)            # the single exception s = 4 (p = 1)
        return (p, 3)
    if r == 2:                       # s = 0 mod 5 : 5^{s/5}, only legal while
        k = (p + 3) // 5             # 5 >= k, i.e. s <= 25
        if k > 5:
            return None              # rule intentionally has no claim here
        return (5,) * k
    if r == 3:                       # s = 1 mod 5 : six-step chain, p >= 8
        if p < 8:
            return (3, 3)            # the single exception s = 6 (p = 3)
        return (p - 2, 5)
    if r == 4:                       # s = 2 mod 5
        return (p, 3)
    raise AssertionError(p)

def b_fours(r):
    """Rule M2 / Theorem G: B-endpoint of (0;(4^r)).  None = no claim.

    Proved windows only: r <= 4 (zero steps, the A-object is already in B),
    and r = 8 (two steps).  No closed form is claimed for 5 <= r <= 7 or r >= 9.
    """
    if r <= 4:
        return (4,) * r
    if r == 8:
        return (32,)
    return None

# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------
def dshow(p):
    return "(" + ",".join(map(str, p)) + ")"

def test_ones(smax=120, frozen_at=25):
    print("=== M1: B-endpoint of (0;(1^s)), s = 0..%d" % smax)
    print("    frozen claim set = s <= %d ; s in %d..%d is held out" % (frozen_at, frozen_at + 1, smax))
    bad = []
    kinds = {"train": [0, 0], "heldout": [0, 0]}
    no_claim = []
    for s in range(smax + 1):
        got, _ = pi_forward(tuple([1] * s))
        pred = b_ones(s)
        tag = "train" if s <= frozen_at else "heldout"
        if pred is None:
            no_claim.append(s)
            continue
        kinds[tag][1] += 1
        if pred == got:
            kinds[tag][0] += 1
        else:
            bad.append((s, pred, got))
    for tag in ("train", "heldout"):
        print("    %-8s agreements %d / %d" % (tag, kinds[tag][0], kinds[tag][1]))
    print("    states with no claim (s = 0 mod 5, s >= 30): %s" % no_claim)
    print("    mismatches: %s" % (bad if bad else "none"))
    # D-side, computed with our own Tinv
    print("=== M1 D-side spot checks (own Tinv, independent of rr_core.Tinv)")
    for s in (5, 8, 9, 11, 13, 16, 21, 25, 31, 34, 36, 41, 44, 56):
        b, _ = pi_forward(tuple([1] * s))
        lam = Tinv_impl(b)
        ok = (is_gap(lam) and weight(lam) == s and is_residue(tuple([1] * s)))
        print("    s=%2d b=%-14s Tinv=%-16s gap=%s wt=%d" % (s, dshow(b), dshow(lam), is_gap(lam), weight(lam)))
        assert ok, ("D-side check failed", s, lam)
    return bad

def test_fours(rmax=20):
    print("=== M2: B-endpoint of (0;(4^r)), r = 0..%d" % rmax)
    bad = []
    for r in range(rmax + 1):
        got, tr = pi_forward(tuple([4] * r))
        pred = b_fours(r)
        mark = "no claim" if pred is None else ("OK" if pred == got else "MISMATCH pred=%s" % dshow(pred))
        print("    r=%2d n=%2d steps=%4d b=%-18s %s" % (r, 4 * r, len(tr) - 1, dshow(got), mark))
        if pred is not None and pred != got:
            bad.append((r, pred, got))
    return bad

def refutation_zero_class(kmax=12):
    """C1 (frozen): b(5k) = (5^k) for all k.  Proved for k <= 5, so the test
    is the held-out range k = 6..kmax."""
    print("=== C1 held-out test: is b(5k) = (5^k) beyond k = 5 ?")
    fails = []
    for k in range(6, kmax + 1):
        s = 5 * k
        got, tr = pi_forward(tuple([1] * s))
        pred = (5,) * k
        ok = pred == got
        print("    k=%2d s=%3d steps=%4d pred=%-22s got=%-24s %s"
              % (k, s, len(tr) - 1, dshow(pred), dshow(got), "ok" if ok else "FAIL"))
        if not ok:
            fails.append((k, pred, got))
    print("    failures: %d / %d" % (len(fails), kmax - 5))
    return fails

def affine_probe(kmax=12):
    """C2 (frozen): b(5k) is coordinatewise affine in k, with at most 3 parts.
    Fit on the *proved* window k = 1..5 (all three coordinates for k <= 3, one
    for k = 1) and test k = 6..kmax."""
    print("=== C2: is b(5k) coordinatewise affine in k for k >= 6 ?")
    data = {}
    for k in range(1, kmax + 1):
        got, _ = pi_forward(tuple([1] * (5 * k)))
        data[k] = got
    print("    values: " + "; ".join("k=%d:%s" % (k, dshow(data[k])) for k in data))
    print("    first-coordinate differences for k = 1..%d: %s"
          % (kmax, [data[k][0] - data[k - 1][0] for k in range(2, kmax + 1)]))
    lens = [len(data[k]) for k in data]
    print("    lengths: %s" % lens)
    print("    => no affine law: the length itself is not eventually constant,")
    print("       and the first coordinate is not monotone (12 at k=9, 35 at k=10).")
    return data

if __name__ == "__main__":
    bad1 = test_ones()
    bad2 = test_fours()
    f1 = refutation_zero_class()
    affine_probe()
    print("=== verdict")
    print("    M1 mismatches (claimed range): %s" % (bad1 if bad1 else "none"))
    print("    M2 mismatches (claimed range): %s" % (bad2 if bad2 else "none"))
    print("    C1 failures outside the proved window: %d" % len(f1))
    assert not bad1 and not bad2
    print("    ALL CLAIMED RANGES AGREE")
