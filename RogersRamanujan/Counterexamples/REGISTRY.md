# RR127 counterexample registry

Owner X. Adversarial review of candidates. Each entry names the exact candidate
version, a reproducible witness, and the scope of what the failure refutes.
Minimization order where a set is searched: smallest weight first, then the
fixed documented order = descending lexicographic on the descending tuple.

The executable form of this registry is `checker.py` (shares no code with
`Computation/`; re-derives every enumerator and every reduction, and imports the
candidate map only as the object under test).

    python3 RogersRamanujan/Counterexamples/checker.py 30     # -> PASS, 0 fails

## REFUTED / closed design requirements

### RR-X001 — length preservation. REFUTED (all n >= 2 conceptually; witness n=2).
Witness: `n = 2`, `A_2 = {(1,1)}`, `D_2 = {(2)}`. No weight-preserving bijection
can match lengths. Do not add "preserves the number of parts" to any spec.

### RR-X002 — largest-part preservation. REFUTED for every n >= 2.
Witness family: `(1^n) in A_n`; `D_n` has no partition with largest part 1 for
`n >= 2`. Minimal witnesses by weight, then lexicographic:
`n=2:(1,1)`, `n=3:(1,1,1)`, `n=4:(1,1,1,1)`, `n=5:(1,1,1,1,1)`,
`n=6:(1,1,1,1,1,1)`, `n=7:(4,1,1,1)`, `n=8:(4,4)`, `n=9:(4,4,1)`,
`n=10:(4,4,1,1)`, `n=11:(4,4,1,1,1)`, `n=12:(4,4,4)`, `n=13:(6,6,1)`,
`n=14:(6,6,1,1)`.
Counts of forced objects for `n = 2..14`: 1,1,1,1,1,2,3,3,3,3,4,7,8.
Confirmed independently by worker m2 (`.ultramath/smwfxwsqf/m2/obstruction.txt`)
and re-derived from scratch by M.

### RR-X003 — "equal largest-part cutoff" refinement. REFUTED at n=5, m=4.
`{|lambda in A_5 : lambda_1 <= 4|} = 2` (`(4,1)`, `(1,1,1,1,1)`);
`{|lambda in D_5 : lambda_1 <= 4|} = 1` (`(4,1)`). Any finitized identity of this
shape needs its own boundary conditions and proof.

### RR-X004 — "fix the intersection" as a *characterizing* requirement. BLOCKED as a design principle.
`A_n cap D_n` has size 0 at `n = 2, 3, 8`, and 1 at `n = 0,1,4,5,6,7,9,12,13`.
So an intersection-fixing rule is vacuous at those weights and cannot be the
structural content of a uniform bijection. Retained only as an optional
convention; it must be justified, never assumed.

## Source-level defects found (not failures of our code)

### RR-X005 — the literal printed `phi` Case II rule is inconsistent. See DECISIONS D-3.
Under a verbatim transcription of BZ82 p.314, `phi` has **2692 defects** among
the 3198 in-domain states of weight <= 18 (not an involution), and the inverse
iteration enters a 2-cycle at `(0;(2)) <-> (1;())` already at `n = 2`, so the
reference map is not even total. With the reconstructed tie-break of D-3 the
defect count is **0** for weight <= 25 and all three printed examples reproduce.
Scope of the refutation: the *printed formula*, not BZ82's theorem, which is not
in question.

## Attacks that were run and found nothing

Candidate version reviewed: `Computation/bz82.py` as committed in this
checkpoint. All of the following passed for `n <= 30` (`n <= 50` for the
bijection laws):

* membership and codomain: every image is a valid partition in `D_n`;
* exact weight preserved for every object;
* determinism: repeated calls agree;
* no collisions; forward is onto `D_n`; inverse is onto `A_n`;
* both inverse laws `inverse(forward(a)) = a` and `forward(inverse(d)) = d`;
* claimed termination: replaced a step cap with a repeated-state detector, so a
  cycle is reported rather than silently timing out;
* degenerate inputs: `()`, `(1)`, `(1,1)`, `(1^12)`, `(4)`, `(6)`, `(4,4,4)`,
  `(2)`, `(13)`, `(5,3)`, `(7,3,1)`, `(9,6,4,1)`;
* invalid inputs are rejected, not silently repaired: a partition outside both
  families raises `ValueError` from `forward`/`inverse` rather than being
  sorted or truncated.

## Standing objections

* No all-n proof of BZ82 termination has been produced here. A bounded search is
  not an impossibility result for any other candidate.
* The staircase group order (weak decreasing) is verified computationally and
  partly in Lean; Lean currently proves nonnegativity but not the order.
* `psi` is a clean involution on the tested range; `phi` depends on D-3, so any
  claim resting on `phi` inherits that reconstruction.
