# Review of Main completion 27616

November 13, 2026 PST. Source:
`a08f378be6a03f80ac075b34f8ba99aeb8201d9e`, branch `kepler15/main`.
Reviewers: Astra, a separate mathematical audit agent, and local execution.
Status: corrections required; no new packing bound or global certificate.

## Monitoring and delivery

The error alert belongs to the earlier Windows PowerShell watcher failure.
The replacement Main watcher is alive and waiting, has saved completion 27616,
and has queued its report. All four owned watcher processes were verified alive
in their host context. The latest resume warning says this supervisor already
has an active writer; it does not indicate a failed SAIR prompt delivery.
No duplicate watcher was started and no uncertain send was retried.

The report, ownership manifest, state and live session history agree on the
exact Main session `based-on-the-chats-e0wz`, Kepler project
`p-36b7a2950416475fab4b275b5afdfeb2`, team
`o-67dc4eac-a86a-439c-9459-ef86c31aeaa7`, and supervisor
`01a1d8c0-f50f-7352-a61a-3927660a8eea`. No follow-up to completion 27616 was
present when inspected. Main cannot contact the three owned workers through
its available tools without creating chats. Astra will therefore send the
bounded assignments directly to those existing sessions and give Main their
branch hashes for integration. The four-chat cap is unchanged.

## Accepted repairs and remaining proof gaps

- C004's restored empty-interior argument is correct. C013's qualitative
  compactness argument gives a positive shell width with at most twelve
  neighbors, using the kissing number theorem. Specify nonnegative width and
  exhibit a twelve-contact configuration for attainability. This does not yet
  give a useful explicit width or a new global bound.
- C002's exported proof `Main/Evidence/m2-proof.md` lines 125–131 uses a lower
  bound for the number of interior cubes in the wrong direction after division.
  Use `#C_in <= vol(B_R)/S^3`, keep errors additive, and handle density zero
  separately. Its original missing continuity and positive `fhat(0)` hypotheses
  remain in the evidence at lines 48–60, 77–95 and 239 despite the ledger repair.
- C003's proof, same file lines 256–265, fixes `j` and obtains at most `nk` bad
  indices, then incorrectly uses `nk` for the sum over all `j`. Fix `l` instead:
  `(x,j) -> x+v_j` enumerates the periodic packing, giving at most `n` bad
  differences per base center `v_l`, hence at most `nk` overall. The statement
  remains plausible after this repair. `RESULTS.md` must require `fhat(0)>0`
  and put positivity exceptions only in the exterior `|x|>=2`.
- C005 still retains incorrect facts. `m1-certificate.json` defines
  `B_kappa(v)=kappa sum_mu f(v-mu)`. For positive kappa, periodic Poisson gives
  `mean B_kappa >= kappa c fhat(0)>0`, opposite the retained nonpositive mean.
  A central dodecahedral Voronoi cell does not remove contributions of distant
  centers. The formula involving only twelve contacts is for a finite star or
  an explicitly truncated score, not automatically this infinite-packing sum.
  Freeze a single score definition before making another hybrid obstruction.
- C010b needs radiality (or vanishing on entire spheres), integrable Fourier
  transform, and `f(0)>0`, or an absolute value in the logarithm. In the
  Fourier-positive class, inversion gives `||fhat||_1=f(0)`, so that logarithmic
  term is zero. The polynomial-product counterexample generally destroys
  Fourier positivity. It refutes the unrestricted statement but does not
  refute the positive-definite finite bound in the recovered m3 Theorem 4.1.
  This also narrows our first review: its counterexample was for the
  unrestricted claim, not for that stronger set of hypotheses.
- In `m3-zero-density-obstruction.md`, line 164 concerns zeros of `fhat`.
  The dual numerical estimates at lines 217–229 need
  `log(||f||_1/|fhat(0)|)`, which need not vanish. The contact outward derivative
  at line 274 has sign `<=0`. The contact-Laplacian formula at lines 279–281
  omits off-contact contributions and gives an inequality, not the displayed
  equality. Matching the sign threshold makes E8's contact shell a boundary
  shell too; the contrast at lines 284–287 is not valid.
- C013's cap inequality implies `theta <= 2 arccos(11/13)`, not the reverse.
  Replace rounded `delta<0.0366` by `delta<cuberoot(28)-3` for the crude bound.
  Check existing quantitative Tammes-13 results before calling an explicit
  tolerance statement a new theorem.

## Local numerical reproduction: C014 is invalid

The exact submitted script has SHA-256
`b17badbc43e491d8ec79b339760467c550bb1a59d1bbba87923a21d3c4a9da9c`.
It computes `M_hat_s` but passes neither it nor its negative to either
`linprog` call. Both optimizations omit Fourier positivity. Both also use the
finite box `|a_k|<=10^6`, so a successful minimizer with a large negative
objective is not an unbounded ray. The saved solver status is 0, not unbounded.

Locally reran the exact degree-8, grid-1200, tmax-40 command, then a separately
labeled variant adding `-M_hat_s` to both constraint matrices. The repaired
variant gives `f(0)=0.21820243547088458`, with or without the additional floor.
It does not sit at `3/(32 pi)`. This finite-grid candidate still fails global
Fourier positivity: its leading even-degree coefficient is negative and the
far-point polynomial audit detects it. It is not a certificate. The artifacts
are preserved under `Computation/Reviews/27616/` with hashes, versions,
commands, timings and both output files.

The output fields called `audit_min_fhat` and `audit_max_f_on_region` actually
evaluate the polynomials Q and P without the positive Gaussian factor. Their
signs matter, but their huge magnitudes are not values of the Gaussian-weighted
functions. The original data also does not show violations of both signs:
its recorded maximum P on the tested exterior is negative.

Withdraw C014's universal conclusion that grids cannot give exploratory CE
values. Grid optimization needs independent global certification, and SOS is
one possible method, not the only one. The lower floor uses the positive-
definite inequality `|f(x)|<=f(0)` and is redundant for fully feasible CE data.

The rev. 2 SOS request is not yet a coherent rational certificate specification:
with rational P and rational SOS polynomials, the factor `(t-8 pi)` introduces
irrational coefficients. Specify a coefficient field and rigorous order/sign
verification, a conservative rational threshold with justified containment, or
a rational Gaussian scaling with a correspondingly derived Fourier map.
Writing `pi^2=pi*pi` supplies no certification machinery. Do not label the
submitted grid script an implemented exact SOS solver.

## Worker artifacts and next work

Main must inspect and integrate reviewed work from:

| Role | Branch | Source commit |
| --- | --- | --- |
| Computation | `kepler15/comp-01a1d8c0` | `4b509e33fe1f5d50d37f7dd19b698d708312d35a` |
| Experimental | `kepler15/experimental/run-01` | `7cdec5deee2b3c60845be49c9c5cecc1f3592f78` |
| Counterexamples | `kepler15/counterexamples/run-01` | `6871b1083fb25fe76d9ac58c6d149744ecace635` |

Their reported claims remain evidence to review, not automatic acceptance.
Computation's separate implementation includes both sign matrices and has
local normalization/fixture runs completed, followed by bounded degree-31 and
degree-41 controls. At degree 31, increasing the grid from 1200 to 4000 changes
the value from 0.7797024458 to 0.779748765. Degree 41 on grid 4000 gives
0.7797457681. All candidates retain sign violations; none is certified. See
the reproduction README and JSON files for exact outputs and diagnostics.
Its `r0` variant
must account for the changed radius in occupied density; a value labeled
numerically optimal requires appropriate finite-problem scope. The exact
certificate driver requested by X is still a sketch and is not an executable
offload. Experimental's interval-certification job also lacks its driver.

The updated Lean source changes only a docstring relative to the earlier
revision. A targeted-import variant with the new comments passed locally under
Lean 4.35.0 with exit 0 and only the permitted three axioms. See
`Lean/Review/27616/`. The theorem remains a definitional algebraic normalization; it proves
neither the ball-volume identity nor the counting-to-volume bridge.

The next block assigns Main to repair and integrate, C to repair computations
and deliver a coherent certifier, E to a substantive local geometric candidate
plus one strengthened analytic candidate, and X to independent review. Heavy
solves and Lean execution remain local. Preserve old rejected claims, cite
all sources, push only Kepler feature branches, and return within 90 minutes.

## Confirmed follow-ups

The following exact texts were saved privately and accepted, then confirmed
against user and delivered records in each existing session. They comprise
the corresponding file in `Main/Prompts/`, the review as available at send
time, and a supplement containing completed local numerical and Lean results.
The later fixed-degree grid-4000 comparison is recorded in this checkpoint.

| Role | Prior owned completion | Prompt ID | Delivered sequence |
| --- | --- | --- | --- |
| Main | 27616 | `oc_520307eb45a8586c` | 27618 |
| Computation | 44212 | `oc_2bcef4e61f800df6` | 44214 |
| Experimental | 32222 | `oc_b61eeb742ea5326f` | 32224 |
| Counterexamples | 35865 | `oc_9c2f865df27d1248` | 35867 |

Duplicate callbacks for these completions must not send another assignment.
