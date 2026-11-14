# K15-COMPUTE-002 — three-point (truncated) evaluator, specification frozen

```text
request_id          = K15-COMPUTE-002
status              = SPECIFIED_NOT_IMPLEMENTED
owner               = Computation session (SAIR chat, role C)
reviewer            = Counterexamples session (role X); mathematics by Experimental (E)
claim_id            = K15-C-3PT-SPEC-001
source_commit       = f33e814e46b4b6f6ca6b9e84b3d84ba7d841d549
branch              = kepler15/comp-01a1d8c0
working_directory   = KeplerConjecture/Computation
```

## Why this is the right second evaluator

`K15-C-INVERSE-001` (in `RESULTS_baseline.md` §2) shows that prescribing the equality-case
zero sets *raises* the bound. So a two-point family, however constrained, cannot reach
`pi/sqrt(18)`. The only published mechanism that provably beats the ordinary two-point
optimum in `d = 3` on this contract is the **truncated three-point bound** of Cohn, de Laat
and Salmon, arXiv:2206.15373, Theorem 1.1, whose `d = 3` value is `Delta <= 0.770271`
(occupied-volume density) versus `0.779747` for ordinary CE. Reproducing `0.770271` and
then perturbing it is the cheapest path to a genuinely stronger evaluated bound.

## The exact statement to implement (verbatim hypotheses, unit-radius contract)

Fix `0 < r < R`, `r = 2` (unit spheres, minimum separation 2). Let `f2 : R^3 -> R` be
continuous and integrable with `f2hat(0) = 1` and `f2hat >= 0` everywhere, and let
`f3 : R^3 x R^3 -> R` be a positive definite kernel. If

```
f2(x) + f3(x,0) + f3(0,x) + f3(x,x) <= 0        for r <= |x| <= R,
f2(x) <= 0                                      for |x| >= R,
f3(x,y) <= 0                                    for r <= |x|,|y| <= R and |x-y| >= r,
```

then the packing density is at most `vol(B^n_{r/2}) (f2(0) + f3(0,0))`.
Source: CDS22 Theorem 1.1, checked in the paper text; the density factor here is
`vol(B_1) = 4pi/3` because `r = 2`.

Two structural facts that constrain any implementation:

1. **The diagonal is where the gain lives.** If `f3(0,0) = 0` then positive definiteness on
   `{0,x}` gives `f3(0,x) = 0` identically, and `f2` alone is a sharp two-point certificate —
   excluded by Li. So a competitive `f3` must have `f3(0,0) > 0`. (Recovered note r1, Thm 3.1;
   independently consistent with the swarm's accepted three-point direction.)
2. **Truncation is essential.** CDS Lemma 1.2: a Gaussian-times-polynomial kernel on
   `R^3 x R^3` satisfying the hypotheses with `R = infinity` must vanish identically. So the
   finite `R` (their `d = 3` optimum uses `R = 1.886835` in their normalisation) is not a
   technical convenience; the problem has no untruncated polynomial-times-Gaussian answer.

## Implementation plan (SDP)

* `f3` as a positive definite kernel from a finite feature map: `f3(x,y) = sum_{i<=k} phi_i(x) phi_i(y)`,
  with `phi_i` in a radial-times-harmonic basis truncated by degree, so that positive
  definiteness is automatic and only the three inequality regions need checking.
* The two inequality regions are semialgebraic once `phi_i` are polynomial times a Gaussian;
  enforce them by sum-of-squares with the region description
  `{r <= |x| <= R}`, `{|x-y| >= r}` on the truncated ball. Use `sympy`-generated Gram matrices,
  or a discretisation for a first pass.
* Normalise `f2hat(0) = 1`; the objective is `f2(0) + f3(0,0)`.

Resource-bounded first instance (this is what the request is for): feature dimension `k = 1`
(a single radial `phi`), angular degree `<= 2`, `R = 1.886835 * r/2` rescaled to our contract,
collocation grid of `2e4` points in the two regions. If that returns a value above
`0.779747`, the implementation is weaker than ordinary CE and is a bug, not a finding: the
two-point case must be recovered exactly when `phi = 0`, and that is the first test.

## Acceptance tests (must pass before any number is reported)

1. **Degeneracy test.** With all `phi_i = 0` the SDP must reproduce the two-point optimum,
   i.e. `Delta <= 0.779747` (CE03) to within solver tolerance. This is the single most
   important test: it verifies the objective, the normalisation, and the density factor.
2. **Sign check.** `f3(0,0) > 0` at any value below `0.779747`, else by fact 1 above the
   "improvement" is a two-point certificate and contradicts Li — which would mean a bug.
3. **Region check.** Every reported solution has its inequality violations reported with
   locations; status stays `TESTED_FINITE` until an SOS certificate covers both regions.

## Resources

| stage | wall time | RAM | notes |
| --- | --- | --- | --- |
| degeneracy test | ~1 min | < 1 GB | LP only |
| `k = 1`, degree 2 collocation | ~5 min | < 4 GB | numpy only |
| full SOS check | ~30-60 min | < 16 GB | needs an SDP solver (`cvxpy`/`SCS` or `MOSEK`) |

Dependencies to pin locally: `numpy`, `scipy`, and for the SOS stage an SDP solver. The VM has
no SDP solver installed; this stage is genuinely local-only.

## Certification status and remaining obligations

Even a successful run is `TESTED_FINITE` unless the two regions are covered by an SOS
certificate with exact or interval arithmetic. Remaining obligations after a positive
result: (i) SOS certificate for both regions; (ii) proof that the truncated bound applies to
*arbitrary* (non-periodic) packings — CDS give this in their §2.1 by mollification, so it is
a citation, not new work; (iii) an honest comparison against `0.770271`, since matching a
published value is reproduction, not improvement.

## While this is pending

Computation freezes this specification and does not implement it ahead of the local
degeneracy test; the mathematical next step is Experimental's, which needs to say whether
its hybrid candidate is expressible as a CDS triple `(f2, f3)` at all.
