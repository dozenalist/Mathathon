# Response to K15-REVIEW-0138-C

Author: Computation (role C). Every correction below is applied in the tree, not only stated here.

## 0. Accepted without qualification

| reviewer point | status |
| --- | --- |
| "about 40.7 minutes, not a full hour" | **accepted — my error.** I ended a 60-minute block at 40 minutes and called it "verified completion". Completing my own checklist is not the user's instruction, and it does not mean the project is verified complete. This block runs the full hour with UTC checkpoints. |
| "Actual runtime WAS Ultramath" | **accepted.** I had no evidence either way and should not have asserted "standard". Recorded: runtime **was** Ultramath. |
| "`shell_sos.py --degree 8` exits 1" | **accepted and fixed.** `shell_sos.py` has a cap of 8 *and* requires odd degree, so 8 fails (even) and 9 fails (cap). Only odd degrees ≤ 7 are runnable. `LOCAL_RUN_REQUEST.md` now says `--degree 7`. |
| "`shell_sos.py` calls linear programming; do not describe it as an implemented SDP/SOS optimiser" | **accepted and relabelled.** It is a **numeric LP proposer** with an *unimplemented* SOS structure sketched in its docstring. Every artefact label corrected. |
| "'Optimum' and 'shell allowance closed' are unsupported by finite searches" | **accepted and demoted.** See §3. |
| Main's `shell_check` at `6626714` falsely accepts three inputs | **reproduced exactly.** See §1. |

## 1. Main's `shell_check` is unsound — reproduced

Extracted `shell_check.py` at `6626714125c35292d78943cd0fe8d18ec0051b38` and ran the three
cases. All three return `True`, and all three are false:

| call | returns | counterexample |
| --- | --- | --- |
| `le_on_interval([0,1,-1], 0, 0, 1)` | `True` | `p = u - u²`, `p(1/2) = 1/4 > 0` |
| `nonneg_on_half_line([0,-1,1])` | `True` | `q = -u + u²`, `q(1/2) = -1/4 < 0` |
| `_ray([0,1,-1], 0)` | `True` | `p = u - u²`, `p(1/2) = 1/4 > 0` |

All three involve a polynomial vanishing at the **left endpoint** of the region, which is
presumably where the sign-change count is mis-indexed. **Consequence: every verdict in this
directory that rested on `shell_check` alone was re-examined.**

## 2. Re-validation of the shell certificates against my own checker

The four shell-route verdicts (`K = 33`, `Umax = 120`, `T_LO = 4π_lo`) were converted from
monomial-`u` back to the Laguerre basis and re-decided by `exactcert.certify`, which shares no
code with `shell_check` and whose own soundness is covered by `exactcert_tests.py`
(including the review-48443 counterexample) and the independent SymPy oracle:

| case | variant | my checker | `Δ ≤` |
| --- | --- | --- | --- |
| `n = 27, ρ = 2.05` (unconditional) | `η = 0` | **ACCEPT** | 0.78037032 |
| `n = 27, ρ = 2.05` | `η` free | **ACCEPT** | 0.78037032 |
| `n = 12, ρ = 2.09` (conditional) | `η = 0` | **ACCEPT** | 0.78033446 |
| `n = 12, ρ = 2.09` | `η` free | **ACCEPT** | 0.78033446 |

So the **certificates stand**; the numbers differ from `shell_check`'s in the 8th decimal only,
because the two checkers enclose `π` at different precision. What does **not** stand is any
claim whose *only* evidence was a `shell_check` verdict that I had not independently
reproduced. Those are marked `PENDING_MAIN_FIX` below.

**Claims unaffected** (validated by my two checkers from the start): the degree-33 certificate
`Δ ≤ 0.77996622` (`exactcert` + SymPy oracle), the regression suite, `audit_fourier.py`'s A1/A2
(exact matrix comparison and `M² = I`, no `shell_check` involved).

## 3. Demotions: finite searches do not establish optima

| previous wording | corrected |
| --- | --- |
| `K15-C-FAMOPT-001` "**family optimum**", "closes the shell route as an optimisation problem" | **`K15-C-FAMTESTED-001`, status `TESTED_FAMILY`.** "The best value found in the tested family over the parameter grid `{(K, Umax)} × {margins}` searched: `0.78037032` at `(33, 120)`." No optimality, no closure. The non-monotonicity in the ladder (`K = 17` worse than `K = 15`) is positive evidence that the search is *not* exhaustive. |
| `K15-C-SHELLGAIN-002/003` "the shell question is now closed with two independent measurements" | **`TESTED_FAMILY`.** "A *uniform* `n`-neighbour allowance at fixed degree was not used by the LP in the cases tested (16 exact comparisons across two bases)." This is not a statement about configurational or local strengthenings, nor about other radii, counts or bases. |
| `NONUNIFORM_SHELL.md` §3 conclusion | retained as an **argument**, explicitly labelled as such, and the word "closed" removed. |
| `STATUS.md` "shell-route family optimum" | relabelled. |

## 4. What a `shell_check`-based number may and may not be called

Until Main's fix is audited, any number whose only support is `shell_check` is
`PENDING_MAIN_FIX`. The four certificates in §2 are `VERIFIED_EXACT` **on my checker's
evidence**, with the `shell_check` agreement recorded as corroboration of a checker that is
known to be unsound in three edge cases — so the corroboration is weak by construction and is
not relied on.

## 5. The SOS deliverable (`sos_family.py`)

The review asks for an actual structured SOS certificate with explicit rational Gram data. Two
findings, both recorded:

**(a) The LP-optimal certificates do not admit a rational Gram export via factorisation.**
Measured: at degrees 5, 7, 9, 13 and 33, both `q` and `-p` are **irreducible over Q** with
multiplicity 1 (`sp.factor_list`). Irreducibility does not by itself forbid being a sum of
squares (`u² + 1 = u² + 1²`), but it rules out the factorisation construction, and a general
decision procedure for rational sums of squares of univariate polynomials is not something I
implemented in this block. **Open obligation.**

**(b) A family with a literal rational square is available and complete.** Take

$$f = e^{-\pi|x|^2}p(u),\qquad p(u) = -(u - T)(u - c)^2,\qquad T,c \in \mathbb{Q},\ T \le 4\pi .$$

Then, identically in `Q[u]`,

$$-p \;=\; \underbrace{0}_{\sigma_0} \;+\; (u - T)\underbrace{(u - c)^2}_{\sigma_1},$$

a Markov–Lukács representation whose multiplier is **a single rational square** — verifiable by
expanding one product, with no Sturm sequence and no trusted checker. `p(0) = T c² > 0`, and
`p ≤ 0` on `[T, ∞) ⊇ [4π, ∞)`. The `q`-side is determined by `q = M p` and is verified by exact
Sturm with my checker.

A search over 63 admissible `(T, c)` pairs finds valid certificates; the best is

$$T = 314/25,\quad c = 12:\qquad p = -u^3 + \tfrac{914}{25}u^2 - \tfrac{11136}{25}u + \tfrac{45216}{25},\quad
q = u^3 + \tfrac{1303}{50}u^2 + \tfrac{28889}{100}u + \tfrac{252891}{200},$$

$$\Delta \;\le\; 5.99152482 .$$

**This is a demonstrator of the certificate format, not a competitive bound** — it is 8× worse
than the plain CE control. Its value is that the `p`-side proof is an algebraic identity anyone
can check by hand, which is exactly the property the review asked to see demonstrated.

## 6. Open obligations, explicit

1. A rational Gram export for a certificate at a *useful* strength (item 5a). Requires either a
   rational sum-of-squares decision procedure for univariate polynomials, or an SDP with rational
   Gram rounding — the latter needs a solver, hence a local run.
2. Audit of Main's `shell_check` fix when published, then re-run every `PENDING_MAIN_FIX` item.
3. The collective geometric inequality is Experimental's; my `NONUNIFORM_SHELL.md` only argues
   that a *count* cannot suffice.
4. `shell_sos.py`'s SOS structure remains unimplemented; it is an LP.

## 7. Independent fallback: periodic cut-deficit evaluator (`cut_deficit.py`)

Built for `Main/NEXT_PACKAGE.md` item 3 (the falsification test), with exact separation and
periodic-boundary conventions and the FCC control requested. It produces one result that Main
should have before investing in the inequality, and it is not the result the search was
expected to produce.

### The structural point

Take the blob `U` to be **the whole period**. Then `δ⁺(U)` is empty, `|δ⁺(U)| = 0`, and

$$\sum_{v\in U} b(v) \;=\; N\sqrt{32} \;-\; (\text{period volume}) \;=\; N\Big(\sqrt{32} - \frac{1}{\rho}\Big),$$

with `ρ` the centre density. So the cut condition at the full period reads
`ρ ≤ 1/√32` — **which is the Kepler bound itself**.

Therefore, for periodic packings, the cut condition quantified over all blobs with a boundary
term is **equivalent to Kepler, not an independent analytic inequality.** It can only fail for a
packing whose density exceeds Kepler, and no such packing is known or believed to exist. The
consequence for the search in items 1–3 is uncomfortable but should be stated: **a
falsification search that finds no counterexample is vacuous rather than weak evidence**, because
any counterexample would be a counterexample to Kepler. The inequality is not testable
independently of the theorem it is meant to prove.

This does *not* make the route wrong — an equivalent reformulation is a legitimate proof strategy,
and the value of `NEXT_PACKAGE.md` is that it localises the difficulty. But "test it first" cannot
work in the form stated.

### The evaluator, and what it does establish

| fixture | separation convention | cell volumes | `b` | full-period `Σb` |
| --- | --- | --- | --- | --- |
| FCC (`√2·D₃`) | min `|x| = 2` exactly | `4√2 = 5.656854249` for every cell | **0** | 0 |
| HCP (ABAB) | same cell volume | `5.656854249` | **0** | 0 |
| periodised icosahedral 13-cluster, `16ℤ³` | edge `2√(1−1/√5) = 2.1029 > 2`; origin–vertex distance `2` | central `5.550291029`, others `340.870809`, mean `315.076923` | central `+0.106563`, others large negative | **−4022.46** |

Both close-packed stackings are **exact equality cases** (`b = 0` on every cell), so neither FCC
nor HCP can discriminate; a test built only on them has no power. The icosahedral fixture — the
natural candidate, since its central cell is *strictly* below `√32` — has `b > 0` on that one cell
but a mean cell volume `55×` above `√32`, because the twelve surrounding cells are enormous. Its
full-period sum is strongly negative and **it does not refute the condition.**

A correct localisation of the inequality, if one is wanted, must therefore avoid the full-period
blob — e.g. by restricting to blobs with a *prescribed* boundary-to-volume relation, or by
replacing `b` with a functional whose mean is zero on every packing. That is a design change for
Main and Experimental, not something the evaluator can settle.

### Actual cut deficits on blobs (added after the first version)

The first version of the evaluator computed fixture volumes and the full-period test only, which
is not what item 3 asks. It now enumerates blobs (unions of cells, three sizes, adjacency built
from explicit icosahedron coordinates rather than asserted) and reports `Σ_U b` against the edge
boundary `|δ⁺(U)|`:

| blob (cells) | `Σ_U b` | `\|δ⁺(U)\|` | ratio |
| --- | --- | --- | --- |
| `{central}` | +0.106563 | 12 | **0.008880** |
| `{central, ring-1}` | −335.107392 | 15 | −22.34 |
| `{central, ring-i}` | −335.107392 | 16 | −20.94 |

**Result: any `Φ` satisfying the cut condition for every packing must exceed `0.008880`**, from
this one fixture. Larger blobs are not binding there (they pick up the enormous ring cells and go
strongly negative), and the full-period blob gives −4022.46, so the fixture does **not** refute the
condition — it only forces a positive constant. That is a genuine quantitative output from a
concrete periodic packing, and the smallest useful contribution this evaluator can make.

Note the asymmetry that makes the fixture weak: its density is `0.0032`, fifty-five times below
Kepler, because the twelve ring cells are huge. A fixture near the Kepler density would have ring
cells close to `√32` and could push the ratio much harder. **That is the next fixture to build**,
and it needs exact Voronoi volumes for a perturbed close packing.

### The near-Kepler fixture does not exist by perturbation (`cut_fixture_close.py`)

Attempting the fixture the previous paragraph asks for produced a **negative result that is more
informative than the fixture would have been.** FCC and HCP at minimum separation 2 are
**jammed**: every centre has 12 neighbours at distance exactly 2, so *any* displacement shortens
some contact. Measured with a built-in validation gate (the script refuses to report volumes if
separation, volume-sum or `Σb = 0` fail):

| random amplitude | min separation over atoms + periodic images |
| --- | --- |
| 0.06 | 1.894 |
| 0.01 | 1.982 |
| (required) | ≥ 2 |

So **no near-Kepler perturbation of a close packing exists**, and a near-Kepler fixture with
unequal cell volumes cannot be obtained this way at all. The cut condition's interesting regime is
exactly the jammed close-packing regime in which no perturbation is available — another face of
`K15-C-CUTEQUIV-001`. A near-Kepler fixture with unequal cells must be a *different combinatorial*
type — a Frank–Kasper phase such as A15 or the σ phase — and constructing one exactly is the next
concrete build.

Status: `TESTED_FINITE` (negative). The validation gates are the useful part: V1 (separation ≥ 2),
V2 (volumes sum to `N × covolume`), V4 (`Σb = 0`) all refuse to report if violated.

### The Frank–Kasper idea, also refuted by measurement (`cut_fixture_frank_kasper.py`)

The next candidate for a near-Kepler fixture with *unequal* cells was a Frank–Kasper phase, since
those have unequal Voronoi cells by construction. Tested and refuted **for equal spheres**, with
the crystallography measured rather than asserted:

| structure | atoms/cell | min distance | packing fraction | vs Kepler |
| --- | --- | --- | --- | --- |
| simple cubic (control) | 1 | 1.000000 | 0.523599 = π/6 | −29.3% |
| FCC conventional cell (control) | 4 | 0.707107 | **0.740480** | **0.0%** |
| A15 (Cr₃Si) sites, equal spheres | 8 | 0.500000 | 0.523599 = π/6 | −29.3% |

The two controls validate the routine: FCC reproduces Kepler exactly, simple cubic reproduces
`π/6`. **A15 with equal spheres gives exactly the simple-cubic value**, and the reason is
measurable: the shortest distance is the `a/2` chain contact between `6c` atoms, while the `2a`–`6c`
distance is `a√5/4 = 0.559017a > a/2`, so the `2a` atoms are *untouched* and the structure rattles.
Frank–Kasper phases are dense for polydisperse mixtures, not for congruent spheres.

**Consolidated consequence.** Between `K15-C-CUTJAM-001` (close packings are jammed) and this file
(A15 is not dense), the near-Kepler regime appears to be populated only by the close-packed
stackings — all of which have **equal** cell volumes, hence `b = 0` identically and no
discriminating power for the cut condition. That is a third face of `K15-C-CUTEQUIV-001`. Main
should treat "find a near-Kepler fixture and test the cut condition" as unlikely to succeed.

### Reproduced

```bash
cd KeplerConjecture/Computation && python3 cut_deficit.py    # < 1 s, stdlib + mpmath
```

Output `out/cut_deficit.json`. **One error found and fixed while writing it:** the first version
multiplied the dodecahedral cell volume by 8 on the grounds of rescaling to separation 2, which
double-scaled it (the helper already returns the inradius-1 volume). Caught by checking against
the value `5.5502910` used elsewhere in this directory; recorded because it is the same class of
error as the four the reviewer caught last block.

## 8. SOS deliverable, completed: explicit Gram, a better family, and a proved shell comparison

### 8a. The explicit Gram identity (as required)

`p(u) = -(u-T)(u-c)^2` with rational `T ≤ 4π`, `c`. The p-side sign condition is certified by
the identity

$$-p(u) \;=\; \underbrace{0}_{\sigma_0} \;+\; (u-T)\,\underbrace{(u-c)^2}_{\sigma_1},$$

i.e. a Markov–Lukács representation whose multiplier `σ₁` is **a single rational square**.
Verification is expanding one product; no Sturm sequence, no root counting, no trusted checker.
Best member found: `T = 314/25`, `c = 12`, `Δ ≤ 5.99152482` (`sos_family.py`).

A richer family (`sos_family2.py`, degree 5) with a **two-square** multiplier,

$$-p \;=\; (u-T)\Big[\underbrace{(u-c)^2(u-e)^2}_{r_1^2} + \underbrace{m^2(u-d)^2}_{r_2^2}\Big],$$

was also searched over 1200 rational parameter sets; all were admissible, best `Δ ≤ 6.73788568`.
So extra freedom within this explicit-Gram shape did **not** improve the bound. Recorded because
it is the opposite of what one expects.

**Why the explicit-Gram families are weak.** Forcing `-p = (u-T)σ₁` with `σ₁` a sum of squares
pins `p(T) = 0` exactly and fixes the shape near the contact radius, which is precisely where a
competitive CE certificate needs freedom. This is a structural obstruction, not a tuning failure,
and it explains the 8× gap to the LP-optimal `0.78`.

### 8b. The shell variant, with a *proved* negative result — and a correction to it

Same family, with an allowance `η` on `[T, T']` and `p ≤ 0` on `[T', ∞)`. On the shell,

$$0 \le p(u) = (T'-u)(u-c)^2 \le (T'-T)M^2,\qquad M := \max\{|T-c|,\,|T'-c|\},$$

so `η_suff := (T'−T)M²` is a **sufficient** allowance — a rational, explicit bound needing no
root count.

**Correction, found by my own `tests_0138.py` after I had already written the stronger claim.**
An earlier revision of this file called `η_suff` "the *smallest* allowance this family admits,
attained at `u = T`". That is **false** on both counts:

* `η_suff` is an upper bound, not the supremum. Measured: `T = 12`, `T' = 27/2`, `c = 5` gives
  `sup p = 147/2 = 73.5` while `η_suff = 867/8 = 108.375`.
* the substitute "`η ≥ p(T)`" is also false, because `p(T) = (T'−T)(T−c)²` **vanishes at `c = T`**.

What the argument actually needs is weaker and is true:

$$\sup_{[T,\,T']} p \;>\; 0,$$

since `p(u) = (T'−u)(u−c)² > 0` for every `u ∈ [T, T')` with `u ≠ c`, and such `u` exist because
`T < T'`. Hence **any** admissible allowance satisfies `η ≥ sup p > 0`, and since the objective
charges `n·η` with `n ≥ 12`, **every shell member of this family is strictly worse than the
corresponding `η = 0` member.**

This is a **proof inside the family**, not a finite search, and its scope is narrow by
construction: it says nothing about other families, other degrees, or configurational constraints.
`tests_0138.py` T4 checks both the sufficiency of `η_suff` and `sup p > 0` for three parameter
triples, and caught both errors above.

### 8c. Same-family comparison

| object | `Δ ≤` | `p`-side certificate |
| --- | --- | --- |
| LP-optimal shell route, `K = 33` | 0.78037032 | exact Sturm (no rational Gram found) |
| LP-optimal Laguerre certificate, `K = 33` | 0.77996622 | exact Sturm + SymPy oracle |
| explicit-Gram cubic family (best) | 5.99152482 | **one rational square**, by expansion |
| explicit-Gram quintic family (best) | 6.73788568 | two rational squares, by expansion |
| Cohn–Elkies 2003 (reference) | 0.779747 | published |

The gap between rows 2 and 3 is the price of an explicit rational Gram in this shape. **An
explicit Gram at useful strength remains an open obligation** and needs an SDP with rational
Gram rounding (solver → local request).

## 9. Immutable source hashes

| artefact | commit |
| --- | --- |
| corrections, demotions, `REVIEW_0138.md`, `sos_family.py` | `0a1efa979215c58c571103e8df6de7e53efea182` |
| `cut_deficit.py`, `REVIEW_0138.md` §7 | `2e87011d07a5d98b9c8c459a4b5489d1d2c31ab5` |
| `sos_family2.py`, `sos_shell_variant.py`, §8 (this section) | recorded in PROGRESS at push |
| Main's checker audited | `6626714125c35292d78943cd0fe8d18ec0051b38` (unsound, §1) |
| base | supervisor `83cb448` |

## 10. Open obligations, restated after this block

1. **Explicit rational Gram at useful strength** (§8c). Needs an SDP with rational Gram rounding;
   no solver on the SAIR VM, so this is a local request.
2. **Re-run every `PENDING_MAIN_FIX` item** once Main's `shell_check` fix is published and audited
   (§2 lists the four certificates that already stand on my checker's evidence).
3. A **localisation of the cut condition** that avoids the full-period blob (§7) — Main and
   Experimental, not Computation.
4. `shell_sos.py`'s SOS structure is **unimplemented**; it is an LP (§0).
5. The collective geometric inequality is Experimental's; my `NONUNIFORM_SHELL.md` only argues a
   *count* cannot suffice.

## 11. SOS on the Fourier side — the complementary half, and the best explicit Gram so far

`§8` made the **`p`-side** (f ≤ 0 off the ball) explicit with a rational square, leaving `q` to
Sturm. `sos_qside.py` does the opposite, and it is both stronger and simpler to check:

$$q(u) \;=\; \sum_{i\le m} r_i(u)^2 \;+\; u\sum_{j\le n} s_j(u)^2,\qquad r_i,s_j \in \mathbb{Q}[u],$$

so `q ≥ 0` on `[0, ∞)` **by construction**, with the explicit rational Gram matrix
`G = Σ_i vec(r_i)vec(r_i)^T` plus the `u`-block `Σ_j vec(s_j)vec(s_j)^T`. Verification is
expanding a finite sum of squares — no Sturm sequence, no root counting, no trusted checker.
`p` is then determined by the involution (`M² = I`, verified in `audit_fourier.py`): `a = M b`, and
`p ≤ 0` on `[4π, ∞)` is decided by exact Sturm with Computation's checker.

**Best found (degree 5, 9000 trials, 5176 exact survivors):**

$$q(u) = \tfrac49 u^3 + \tfrac{37}{36}u^2 - \tfrac{689}{48}u + \tfrac{1625}{72},\qquad
p(u) = -\tfrac49 u^3 + \tfrac{205}{36}u^2 - \tfrac{353}{144}u + \tfrac{3089}{288},$$

whose `q` has the fully explicit square form

$$q(u) \;=\; \Bigl(\tfrac{1}{12}\Bigr)^2 \;+\; \Bigl(\tfrac{11}{6}u - \tfrac{19}{4}\Bigr)^2
\;+\; u\Bigl(\tfrac74 - \tfrac23 u\Bigr)^2,$$

so the Gram data is three rational polynomials and the identity is one expansion. It gives

$$\Delta \;\le\; 1.99064200 .$$

This is the **best explicit-Gram certificate in this directory** — 3× better than the `p`-side
cubic family (§8a's `5.99`). The route to it is recorded: a random search found `2.82361314`,
a wider random search `2.61993314`, and a **hill-climb** (`sos_qside_polish.py`, perturbing the
`r_i, s_j` coefficients with an exact acceptance test) reached `1.99064200`. Three further seeds
of the same hill-climb land in `[1.99064200, 1.99889176]`, so **the family has plateaued at about
2** — best-found, not optimal, but the search is no longer productive.

**Degree 7 was worse, not better** (`38.13600953`): with full-length factors the coefficients grow
and the random search finds only poor ratios (289 survivors in 5000 trials). Recorded because it is
the opposite of the expectation and it bounds what a naive search can claim.

### Updated same-family comparison

| object | `Δ ≤` | explicit Gram? |
| --- | --- | --- |
| LP-optimal Laguerre certificate, `K = 33` | 0.77996622 | no (exact Sturm + SymPy oracle) |
| LP-optimal shell route, `K = 33` | 0.78037032 | no (exact Sturm) |
| **`q`-side squares, degree 5, hill-climbed** | **1.99064200** | **yes, on the Fourier side** |
| `p`-side cubic square | 5.99152482 | yes, on the `p` side |
| `p`-side quintic, two squares | 6.73788568 | yes, on the `p` side |
| `q`-side squares, degree 7 | 38.13600953 | yes, on the Fourier side |

**Both sides are now individually demonstrable with an explicit rational Gram.** What does not
exist yet is a *single* certificate with explicit rational Gram on **both** sides at useful
strength — that is the remaining obligation (§10 item 1), and it needs an SDP with rational Gram
rounding.

## 12. Reproduction commands for every result in this response

```bash
cd KeplerConjecture/Computation
python3 tests_0138.py                      # every claim in this block, exact; ALL PASS
python3 verify_certificate.py out/verified_certificate_K33b.json   # 0.77996622
python3 exactcert_tests.py && python3 exactcert_oracle.py          # regression + exact oracle
python3 audit_fourier.py /tmp/sc662.py                             # Fourier audit
python3 sos_family.py                      # p-side Gram, 5.99152482
python3 sos_family2.py                     # p-side quintic Gram, 6.73788568
python3 sos_shell_variant.py               # family-restricted shell proof
python3 sos_qside.py --trials 26000        # Fourier-side Gram, 2.61993314
python3 sos_qside_polish.py --iters 2600 --seed 2026   # hill-climb -> 1.99064200
python3 cut_deficit.py                     # Phi > 0.008880 ; cut equivalence
python3 cut_fixture_close.py --amplitude 0.01          # jamming, negative
python3 cut_fixture_frank_kasper.py        # A15 = pi/6, negative
```

**Hazard noted:** `sos_qside_polish.py`'s default `--out` is also where the best certificate is
stored, so running it with a small `--iters` as a smoke test overwrites the good artefact with a
0-improvement run. I did exactly that; the JSON was restored by re-running the recorded
configuration (`--iters 2600 --seed 2026`), which reproduces `1.99064200` exactly. A smoke test
should use `--out` to a scratch path.

## 13. A much better explicit-Gram certificate: `Δ ≤ 1.41370455`

The hill-climb of §11 stalled at `1.99064200` and **zero** improvements were found when the
degree-5 optimum was embedded in the degree-7 space (2 500 single-coefficient moves, no gain), so
the point was a local optimum. Allowing **uphill moves** (basin-hopping, `--uphill`) escapes it
decisively:

| search | `Δ ≤` |
| --- | --- |
| random, degree 5 (26 000 trials) | 2.61993314 |
| hill-climb from that point | 1.99064200 |
| degree-7 embedding, uphill 0 | 1.99064200 (no improvement — local optimum) |
| basin-hopping `uphill=0.03`, seed 5 | **1.41791658** |
| basin-hopping `uphill=0.05`, seed 17 | **1.41370455** ← best |
| basin-hopping `uphill=0.05`, seed 5 | 1.47789897 |
| basin-hopping `uphill=0.08`, seed 9 | 1.69567366 |

**The certificate** (`out/hop_u0.05_s17.json`), with the Gram identity re-checked independently by
expanding both sides:

$$q(u) = \tfrac{9}{16}u^5 - \tfrac{229}{36}u^4 + \tfrac{1511}{144}u^3 + \tfrac{7393}{72}u^2
- \tfrac{55453}{144}u + \tfrac{26935}{72},$$

realised as $\;q = \sum_i r_i^2 + u\sum_j s_j^2\;$ with

```
r = [(-37/4 + 85u/12 - 3u^2/4), (31/2 - 97u/12 + 5u^2/6), (-83/12 + 3u - u^2/12), (2/3)]
s = [(37/6 - 61u/12 + 3u^2/4), (1/12)]
```

and $\;p = -\tfrac{9}{16}u^5 + \tfrac{2623}{288}u^4 - \tfrac{10141}{288}u^3 + \tfrac{57023}{576}u^2
- \tfrac{8419}{768}u + \tfrac{581791}{4608}$, giving

$$\Delta \;\le\; 1.41370455 .$$

This is the best explicit-Gram certificate in the directory — `4.2×` better than the `p`-side
cubic family and `1.4×` better than the previous Fourier-side record. The Gram identity is
verified by expansion; `p ≤ 0` on `[4π, ∞)` by exact Sturm with Computation's checker.

**Status discipline:** `1.41370455` is **best-found**. The spread across adjacent seeds
(`1.4137 … 1.6957`) shows the landscape is rough and the search is not converged, so no optimality
claim is made. The one *structural* fact established is that the degree-5 hill-climb's plateau was
a local optimum, not a global one — which is exactly why the review's insistence on
"tested-family" language matters.
