# Cycle 3 / m4 / direction A' — report for Main (short)

Full argument: `PROOF_PHI_OBLIGATIONS.md` (this directory).
Proposed destination: `RogersRamanujan/Counterexamples/cycle3/`.

## Status of the five phi obligations

| obligation | status |
|---|---|
| (i) `m >= 0`, `t+5j-3-m >= 0` | PROVED (Lemmas 3, 4) |
| (ii) `N = L+lam(mu)-5j-t* >= 0`, integer | PROVED (Lemma 2; it *is* Case I's inequality) |
| (iii) deletions at `a`, `mu` valid incl. `a != mu` | PROVED (Lemmas 0, 1) |
| (iv) case stability `I <-> II` | not proved; reduced to R1 (two explicit inequalities) |
| (v) `phi^2 = id` | not proved; reduced to R2 (slot-level inverse recipe) |

Lemma 4 is the substantive one: for every in-domain Case-II state,
`p2 = t+5j-3-m >= 0`.  Proof (5 sections of `PROOF...md`): `m <= R` is
immediate, the bad case `m = R` is excluded in each branch of the *established*
Case-II dichotomy (`a <= t` with `j>=1` / `j=0` / `j<=-1`, or `a = t+1, j>=1`),
using `lam(k) <= R` (E1) and the minimality of `a`.  It uses Main's E1 and E2 as
black boxes; nothing else.

## Proposed changes to Main (I do not edit outside my directory)

1. `Computation/bz82.py` Case I: the `if drop:` fallback that removes a second
   copy of the value at `a` is **dead code on the domain** by Lemma 1
   (`a = mu` is impossible in Case I).  Replace it with an assertion.  It is the
   only "second-removal" convention left in `phi`, so removing it removes the
   only remaining place where `phi` could differ from BZ82 by convention.
2. `Main/CLAIMS.md` RR-C009: the obligation list can shrink from five items to
   two.  Suggested text: "(i),(ii),(iii) PROVED (cycle 3, direction A');
   remaining: R1 case stability, R2 branch inverseness — statements in
   `Counterexamples/cycle3/PROOF_PHI_OBLIGATIONS.md` §8."
3. Record the sharp witness `(0; (1,1,1)) -> (-1; ())`: weight 3, Case II,
   `m = 0` **and** `p2 = 0`, so *both* created parts are zero and both are
   carried by virtual slots.  This is the smallest state where the
   "created part 0 is discarded" convention is load-bearing.  (The other two
   under weight 30: `(-1;(1^8))`, `(-2;(1^13))`.)
4. Record the positional slot identity (R2.1''), which is the sharpest finite
   statement we have about the inverse branches: in the Case II -> I direction
   `lam'(a') = m` and `lam'(mu') = p2` with **no swap**, and dually `m' = L`,
   `p2' = lam(mu)`.  0 exceptions to weight 40 and on random states to
   weight 9624.  This is the target a proof of (v) should aim at.
5. No *new* defect is claimed anywhere in BZ82; no printed rule was re-read or
   reconstructed here.

## Exact commands (from the project root)

    python3 .ultramath/smwg1kdjq/m4/cycle3/phi_obligations.py 30 --compare
    python3 .ultramath/smwg1kdjq/m4/cycle3/phi_obligations.py 40 --compare
    python3 .ultramath/smwg1kdjq/m4/cycle3/stress.py
    python3 .ultramath/smwg1kdjq/m4/cycle3/probe.py 30
    python3 .ultramath/smwg1kdjq/m4/cycle3/probe_slots.py 30

(The scripts `sys.path`-insert the committed `Computation/` directory for the
`--compare` mode and otherwise use only the standard library; they can be run
from any directory.)
