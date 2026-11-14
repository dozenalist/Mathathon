# Rogers–Ramanujan: achieved results and remaining gaps

Reviewed November 13, 2026, America/Los_Angeles. This is the current results
summary; older dated reports and the claim ledger retain the research history.
The latest imported SAIR checkpoint is
`d8684a9384edc52e5960733a4f92bf8c207083db` (cycle 4), incorporating the supervisor
review `c8eeb4aa9c1d584f8c6028e813334e2b0edcf98f`.

**The Mathathon objective remains open.** We have formalized standard bridges,
implemented and tested a classical reference bijection, proved useful local
facts and obstructions, and identified precise proof gaps. We have not produced
a new, more natural bijection with a complete proof and inverse.

## The mathematical target

For weight n, A_n consists of descending positive partitions with parts 1 or 4
modulo 5. D_n consists of descending positive partitions with adjacent gaps at
least 2. B_n is the intermediate family whose smallest part is at least its
length. The empty partition is included at weight zero. B and D have different
membership conditions and must remain distinct.

The target is an explicit, uniform, weight-preserving A_n/D_n bijection with an
independently recoverable inverse and a convincing structural improvement over
known constructions. See the [problem specification](../Literature/PROBLEM_SPEC.md).

## Achievements and evidence

| Result | What has been established | Evidence and limits |
| --- | --- | --- |
| Staircase equivalence | Subtracting the odd staircase from a length-k gap partition produces a weakly decreasing nonnegative coordinate list of weight n-k², with k and zero padding retained; both inverse laws hold. | [Staircase.lean](../Lean/Staircase.lean), [StaircaseOrder.lean](../Lean/StaircaseOrder.lean); verified on Lean 4.35.0. This is a standard reduction, now formalized. |
| Same-weight D/B shift | T(lambda)_i = lambda_i-k+2i-1 and its inverse define a bijection between the stated list subtypes, preserving weight and satisfying order and positivity conditions. | [ShiftT.lean](../Lean/ShiftT.lean): `toD_toB`, `toB_toD`, `weight_toB` and supporting lemmas. The named target builds on Lean 4.35.0 with permitted printed axioms. This does not formalize the A/D correspondence. |
| Executable classical baseline | Forward and inverse implementations of Bressoud–Zeilberger's 1982 construction, with signed states, local involutions and complete traces. | [bz82.py](../Computation/bz82.py), [saved n<=50 run](../Computation/results_n50.json). Every weight 0–50 has successful bijection checks. The saved run has **1,065 objects at n=50**, correcting an older prose figure of 374. These are finite checks, not an all-input proof. |
| Counting checks | The two partition families agree through weight 50 under the recorded enumeration, recurrence and series checks. | The same saved dataset. Product expansion and residue coin-change are the same recurrence; they are not two independent mathematical methods. |
| Obstructions | A universal weight-preserving map cannot also preserve length or largest part. Equal largest-part cutoffs do not give the proposed refinement. | At n=2, `(1,1)` must map to `(2)`. For any n>=2, `(1^n)` has no D_n image with largest part 1. At n=5, cutoff 4 gives counts 2 versus 1. These are elementary proofs, not claims of novelty. |
| Local phi lemmas | Nonnegative Case-II admissibility on its domain; distinct Case-I deletion slots; nonnegative inserted counts and split parts; signed-weight identities. | [Maximum-existence argument](LEMMA_MAXEXIST.md) and [worker obligation proof](../Counterexamples/cycle4/PROOF_PHI_OBLIGATIONS.md). These establish local facts; branch stability and both compositions remain open in the project's proof. |
| Partial family analysis | Explicit local formulas and selected short endpoint classes for inputs `(4^r,1^s)`; tested conjectures and counterexamples. | [Family analysis](../Experimental/cycle3/PROOF_fam45.md). These are partial results with boundary corrections. A uniform full-family endpoint rule and independent inverse characterization have not been established. |

An amended written proof for the residue involution psi is committed in
[AMENDED_PROOF.md](../Counterexamples/cycle2/AMENDED_PROOF.md) and was reported
reviewed by SAIR. It is not Lean-verified. We distinguish that paper argument
from finite checks and from the unresolved phi proof.

## Verification of the latest checkpoint

On the integrated cycle-4 sources the supervisor ran:

- `python RogersRamanujan/Computation/cycle3_fast_regression.py`: **13 checks,
  zero failures**. Both local involutions pass on all **3,198** tested domain
  states each through signed weight 18. Two intentionally corrupted maps are
  rejected on **224/224** control states each.
- `python RogersRamanujan/Counterexamples/checker.py 20`: **PASS**, zero failures.
- `lake build RogersRamanujan` using **Lean 4.35.0**: success, six jobs. The
  imported modules print only permitted axioms; the formalized bridge has no
  `sorry` dependency. [Earlier full build log](verification/2026-11-13_2308_PST/lean435-build.txt).

The historical n<=50 dataset has 51 rows of endpoint-bijection checks. Its
separate exhaustive signed-state involution census stops at weight **25**;
its `nmax=50` header does not extend every sub-check to 50. Other reports have
separate larger bounds. Bounds belong to individual tests, not filenames.

## Corrections that materially improved the project

For `(4^3,1^62)`, the correct B endpoint is `(25,17,8,8,8,8)` and its D image
is `(30,20,9,7,5,3)`. The trace has **1,910 involution edges / 1,911 states**,
and the inverse recovers the input. Main's earlier rejection of the B endpoint
used D's gap condition on the wrong family; its five-step count measured a
partition's length instead of the trace. Both errors are retracted.

The old psi regression accepted merely one successful state. It now compares
successes with the whole tested domain and includes negative controls. The
Case-II maximum proof now uses monotonicity only on its allowed index range.
A claimed all-input slot theorem, RR-C021, was downgraded to **TESTED_FINITE**:
its worker artifact explicitly leaves that proof open. Family boundary values,
endpoint scope and edge/state conventions have also been corrected.

Finite path measurements and capped runs establish neither an asymptotic
complexity law nor failure of termination. The old linear-growth descriptions
are withdrawn. A counterexample to a proposed inequality does not by itself
establish a typographical error in a published source.

## Remaining work

1. Prove phi's branch stability and both compositions, including repeated parts,
   virtual zeros, vanished ones and both orders of the deleted slots. R1/R2 are
   explicit remaining obligations, not accepted all-input theorems.
2. Complete the finite alternating-path endpoint and inverse argument for the
   implementation, conditional on both involution proofs.
3. Turn partial family formulas into a structurally useful correspondence with
   an independently specified inverse. P2 remains a conjecture; finite
   confirmations do not supply its missing proof.
4. Produce and justify the requested more natural A/D bijection, with accurate
   attribution and comparison to known maps. Full-text access gaps for the
   Garsia–Milne references still limit that comparison.

Bressoud–Zeilberger's published bijection is established prior work. The open
proof obligations above concern this project's reconstruction and its intended
new contribution, not the validity of the classical Rogers–Ramanujan identity.
See [literature notes](../Literature/README.md), [claims](CLAIMS.md),
[decisions](DECISIONS.md), and [progress history](../PROGRESS.md).

## Repository and SAIR handoff

Canonical repository: https://github.com/dozenalist/Mathathon.
The public results are published on `main`; `rr127/main` is the project research
branch. Use `git fetch origin` and actual remote refs to obtain the current
commit, rather than copying an old hash from a transcript. The assigned SAIR
project is `p-9021becf3f0d47a89b3f3c794c1e872b`, coordinator
`chat-c03d79e54b`. Keep all project work and synchronization within that binding.
