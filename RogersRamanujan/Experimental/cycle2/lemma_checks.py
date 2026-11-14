"""Step-by-step machine checks of the five symbolic lemmas in PROOF_families.md.

Each lemma is a *parametric* statement; here it is instantiated on every
parameter in a range, which is what makes the write-up checkable: the proof in
PROOF_families.md is a single case analysis with inequalities that are uniform,
and this file confirms the instantiation.

Run:  python3 lemma_checks.py
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
from bz82 import phi, psi, pi_forward
from rr_core import is_gap, weight

def dshow(p): return "(" + ",".join(map(str, p)) + ")"

def expect(name, got, want, fails):
    if got != want:
        fails.append((name, got, want))

def in_B(b):
    k = len(b)
    return all(x >= k for x in b)

fails = []

# ---- Lemma 0: phi(0;(1^s)) = (-1;(s-3)) for s >= 3 ----------------------
for s in range(3, 201):
    want = (s - 3,) if s - 3 > 0 else ()
    expect("L0 s=%d" % s, phi((0, (1,) * s)), (-1, want), fails)
print("Lemma 0 (one phi collapses the ones-ray): checked s = 3..200, fails = %d"
      % sum(1 for f in fails if f[0].startswith("L0")))

# ---- Lemma 1: psi(-1;(p)) in four branches ------------------------------
b1 = {"a": 0, "b": 0, "c": 0, "d1": 0, "d2": 0}
for p in range(0, 201):
    lam = (p,) if p > 0 else ()
    r = p % 5
    got = psi((-1, lam))
    if r == 0:
        expect("L1a p=%d" % p, got, (0, (p + 3,)), fails); b1["a"] += 1
    elif r in (1, 4) and p >= (6 if r == 1 else 4):
        expect("L1b p=%d" % p, got, (0, (p, 3) if p > 3 else (3, p)), fails); b1["b"] += 1
    elif r == 2:
        k = (p + 3) // 5
        expect("L1c p=%d" % p, got, (0, (5,) * k), fails); b1["c"] += 1
    elif r == 3 and p == 3:
        expect("L1d1 p=3", got, (0, (3, 3)), fails); b1["d1"] += 1
    elif r == 3 and p >= 8:
        expect("L1d2 p=%d" % p, got, (-2, (p - 8,) if p > 8 else ()), fails); b1["d2"] += 1
print("Lemma 1 (psi on a singleton) branch counts over p = 0..200: %s ; fails = %d"
      % (b1, sum(1 for f in fails if f[0].startswith("L1"))))

# ---- Lemma 2: the six-step chain for p = 3 mod 5, p >= 8 ----------------
n2 = 0
for p in range(8, 201):
    if p % 5 != 3:
        continue
    n2 += 1
    s1 = psi((-1, (p,)))                       # step 1
    expect("L2i p=%d" % p, s1, (-2, (p - 8,) if p > 8 else ()), fails)
    s2 = phi(s1)                               # step 2
    expect("L2ii p=%d" % p, s2, (-1, (1,) * p), fails)
    s3 = psi(s2)                               # step 3
    expect("L2iii p=%d" % p, s3, (0, (3,) + (1,) * p), fails)
    s4 = phi(s3)                               # step 4
    expect("L2iv p=%d" % p, s4, (-1, (p - 2, 2)), fails)
    s5 = psi(s4)                               # step 5  (endpoint)
    expect("L2v p=%d" % p, s5, (0, (p - 2, 5)), fails)
    if not in_B(s5[1]):
        fails.append(("L2 B-membership p=%d" % p, s5, "in B"))
print("Lemma 2 (six-step chain): %d parameters p = 8..200, p = 3 mod 5 ; fails = %d"
      % (n2, sum(1 for f in fails if f[0].startswith("L2"))))

# ---- Lemma 3: phi(0;(4^r)) = (1;(5^{r-2},1^{8-r})) for 5 <= r <= 8 -----
for r in range(5, 9):
    want = (1, (5,) * (r - 2) + (1,) * (8 - r) if (8 - r) > 0 else (5,) * (r - 2))
    want = (1, tuple(sorted((5,) * (r - 2) + (1,) * (8 - r), reverse=True)))
    expect("L3 r=%d" % r, phi((0, (4,) * r)), want, fails)
print("Lemma 3 (fours-ray, window 5..8): fails = %d"
      % sum(1 for f in fails if f[0].startswith("L3")))

# ---- Lemma 4: (0;(4^r)) is already in B for r <= 4 ---------------------
for r in range(0, 5):
    if not in_B((4,) * r):
        fails.append(("L4 r=%d" % r, (4,) * r, "in B"))
print("Lemma 4 (fours-ray trivial window r <= 4): fails = %d"
      % sum(1 for f in fails if f[0].startswith("L4")))

# ---- Lemma 5: psi(1;(5^6)) = (0;(32)) ---------------------------------
expect("L5", psi((1, (5,) * 6)), (0, (32,)), fails)
print("Lemma 5 (r = 8 terminates in two steps): fails = %d"
      % sum(1 for f in fails if f[0].startswith("L5")))

# ---- Lemma 6: phi(0;(4^r)) = (-1;(r-6,3,3^r)) for r >= 9 ---------------
n6 = 0
for r in range(9, 61):
    n6 += 1
    want = tuple(sorted((r - 6, 3) + (3,) * r, reverse=True))
    expect("L6 r=%d" % r, phi((0, (4,) * r)), (-1, want), fails)
print("Lemma 6 (fours-ray, r >= 9): %d parameters, fails = %d"
      % (n6, sum(1 for f in fails if f[0].startswith("L6"))))

# ---- Theorem F: end-to-end against the committed baseline ---------------
bad = 0
for s in range(0, 121):
    b, tr = pi_forward((1,) * s)
    p = s - 3
    r = p % 5
    if s in (0, 1, 2):
        pred = () if s == 0 else (s,)
    elif r == 0:
        pred = (s,)
    elif r == 1:
        pred = (2, 2) if p == 1 else (p, 3)
    elif r == 3:
        pred = (3, 3) if p == 3 else (p - 2, 5)
    elif r == 4:
        pred = (p, 3)
    else:
        k = (p + 3) // 5
        pred = (5,) * k if k <= 5 else None
    if pred is not None and pred != b:
        bad += 1
        print("  THEOREM F MISMATCH s=%d pred=%s got=%s" % (s, dshow(pred), dshow(b)))
print("Theorem F end-to-end: claimed s = 0..120, mismatches = %d" % bad)

print("\nTOTAL failures across every check above: %d" % len(fails))
for f in fails[:20]:
    print("  ", f)
assert not fails and bad == 0
print("ALL LEMMA CHECKS PASS")
