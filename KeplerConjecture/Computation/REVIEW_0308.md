# Response to K15-REVIEW-0308-C

Author: Computation (role C). Block 11:14:20Z → 12:14:20Z. Branch `kepler15/comp-01a1d8c0`,
base `9d9ff68227362fa10e4841dbfcd82f6c12a1a8f8`.

## 0. Accepted

| reviewer point | response |
| --- | --- |
| "Correct that overclaim" (full-period cut ⇒ equivalence) | **Accepted; corrected in §2.** The claim was wrong and the reason is instructive: the full period is not a finite `U`, so C044's criterion does not apply to it at all. |
| "Do not promote floating upper-volume fixtures to universal certificates" | **Accepted.** `cut_flow.py` uses rational enclosures `b_lo ≤ b ≤ b_hi` and takes the conservative direction in each case; the one fixture with an irrational volume is marked provisional in its own row and in the JSON. |
| "The 2.0017 control … weaker than the trivial density bound" | **Accepted; §4 states the strength table with the trivial bound 1 in it.** Every both-sides certificate I have found is above 1, so the route is a format demonstrator. |
| "Remove /tmp-specific checker paths from submitted commands" | **Done.** `LOCAL_RUN_REQUEST.md` no longer mentions any `/tmp` path; scripts either build their own rational Fourier matrix (`sos_both_sides_*.py`, `cut_flow.py`) or take a checker path with no default. |
| "larger sweeps need a single portable command with seed range, time cap and output schema" | **Done** — §5 gives one command, `--seed-lo/--seed-hi`, a cap, and a JSON schema. |

## 1. Deliverable: `cut_flow.py`, a portable periodic cut/flow evaluator

Implements C044's convention exactly — `b(v) = √32 − vol Ω(v)`; `G_R` with an edge between
centres at distance `≤ R` and capacity `Φ` per edge; the criterion `Σ_{v∈U} b(v) ≤ Φ·|δ⁺_R(U)|`
for every **finite** `U ⊆ Λ`.

**Two output kinds, deliberately not symmetric:**

| output | scope of what it proves |
| --- | --- |
| an **explicit violating cut** (finite `U`) | a genuine obstruction for the **infinite packing**: `U` is finite, so it is a legitimate test set. Unconditional. |
| a **feasible flow** on a periodic patch | `PATCH_FEASIBLE` — evidence about *that patch only*. It does not prove the cut condition for other finite `U`, and it does not prove the infinite extension. Never reported as a certificate. |

### Two correctness bugs in the flow model, found by a truth-known test suite

`tests_cut_flow.py` checks the evaluator against cases with **analytically known** answers. It
found two substantive errors, both now fixed:

1. **The flow formulation was not antisymmetric.** Each oriented arc `(i,j)` and `(j,i)` had its
   own variable with independent bounds, and antisymmetry was imposed only *after* the LP. That
   allows a "flow" that violates the divergence bound, and the verifier rejected some of them —
   inconsistently, which is what exposed it. Now there is **one variable per undirected edge**,
   with `φ(i,j) ∈ [−Φ, Φ]` and `φ(j,i) = −φ(i,j)` inside the LP.
2. **The strongest necessary condition was being skipped.** Summing `div(v) ≥ b(v)` over *every*
   vertex gives `0 = Σ_v div(v) ≥ Σ_v b(v)`, so `Σ_v b ≤ 0` is necessary. That is the
   empty-boundary cut `U = everything`, and `find_violating_cut` skipped empty boundaries (to
   avoid dividing by zero) — hiding the condition entirely. It is now checked separately
   (`global_necessary_condition`) in both the built-in and the external paths.

The distinction the tests forced is worth stating as a matter of the mathematics, not of code: on
a **finite** vertex set the empty-boundary cut carries content (`Σ_U b ≤ 0`), whereas for the
**infinite** packing the whole space is not a finite test set. A star with a positive centre and
zero leaves therefore has **no transfer at any `Φ`**, while a star whose leaves sum to `−b₀` has
threshold exactly `b₀/m`; both are now tested, and the earlier version got the first case wrong.

**Enclosure width, checked.** The threshold was recomputed with the enclosures tightened by three
and then six extra digits: it moves by `1.2·10^{-10}` and then by `3.1·10^{-14}`, i.e. it has
**converged to `0.00888026841442…`**. The shipped value `0.008880268414` sits *below* the true
threshold, which is the conservative direction for a refutation: the claim "fails for every
`Φ` below it" is weakened, never overstated, by the enclosure.

**The per-fixture threshold is now exact, not capped.** For the 13-vertex fixture the evaluator
enumerates **all 8191 non-empty subsets** (`exhaustive_cut_scan`, used whenever `n ≤ 16`) and finds
`t* = max_U Σ_U b/|δ⁺(U)| = 0.008880268414417`, attained at the singleton — at `R = 2`, `2.1029`
and `3` alike. So for this fixture `Φ ≥ 0.008880268414417` is necessary and (with the flow it
verifies) sufficient. The `|U| ≤ 6` cap that earlier versions used is gone for this fixture.

Arithmetic: FCC and HCP have `b = 0` exactly. The icosahedral fixture's cell volume involves
`√5`, so the file carries rational enclosures and uses `b_lo` to refute and `b_hi` for
feasibility — each direction conservative.

### Results

| fixture | deficits | verdict |
| --- | --- | --- |
| FCC (separation 2) | `b = 0` exactly, every cell | condition **satisfied trivially** at any `Φ ≥ 0`; **no information** |
| HCP | `b = 0` exactly, every cell | same |
| periodised icosahedral 13-cluster | central `b ∈ [0.106563219492, 0.106563221492]`; ring `b ≈ −335.214` | **the singleton cut `{0}` violates the condition for every `Φ < 0.008880268414`** |

The third row is the useful one. **Before using it the fixture is validated, not asserted**
(`validate_icos_fixture`): minimum separation among the 13 centres exactly `2.000000`; nearest
periodic image at `14`; central-cell circumradius `≤ 1.3 < 8` (the half-period), so the cell is
**uncut** and is exactly the regular dodecahedron of inradius 1, whose volume is the certified
enclosure `[5.550291028, 5.550291030]`.

### Both regimes of C044, and what each one shows

| `R` | graph | criterion | verdict for the icosahedral fixture |
| --- | --- | --- | --- |
| `1` | **no edges** | pointwise `b(v) ≤ 0` (Hales' fcc-compatibility) | **VIOLATED**: `max b ≥ 0.106563` |
| `2` | 12 edges | cut condition | fails for `Φ < 0.008880268414`; flow above, `PATCH_FEASIBLE` |
| `2.1029`, `3` | 42 edges | cut condition | same threshold; the singleton cut is still binding |

The `R < 2` row is worth Main's attention: the fixture is a legitimate packing (separation exactly
2) whose central cell is **strictly below** `√32`, so it is **not** fcc-compatible and no transfer
at bounded range can repair a positive deficit at an isolated vertex. That is precisely the reason
`K15-C035`'s correction term `A` is needed, and the evaluator now exhibits it rather than assuming
it.

### Three bugs this validator found in my own fixture code

Recorded because the reviewer's instruction — validate, do not promote — is what surfaced them:

1. **The fixture was not a packing.** The vertices `(0,±1,±φ)` used since the 13-cluster was
   first written form an icosahedron of *circumradius* `√(1+φ²) = 1.9021`, so the centre–vertex
   distance was `1.9021 < 2`. The correct configuration scales the *unit* icosahedron to
   circumradius exactly 2, giving edge `2.1029 > 2`. Without the validator this would have been
   reported as a `Φ` threshold for an invalid configuration.
2. **`R`-gating of the central-ring edges.** They are at distance exactly 2 and must be gated by
   `R`; an earlier version added them unconditionally, so `R = 1` produced a twelve-edge star
   instead of the correct edge-free graph — i.e. the `R < 2` regime was unreachable.
3. **Empty-boundary division.** With no edges the singleton cut has `|δ⁺| = 0`, and the cut
   machinery divided by zero. The cut code now only runs in the `R ≥ 2` regime; in `R < 2` the
   pointwise condition is the only object and is reported instead.

The third row is the useful one: an **explicit finite cut** giving a rigorous lower bound
`Φ ≥ 0.008880268414` for that packing.

### Corrections demanded by the evidence review, applied

1. **The singleton floor is not universal.** `0.008880268414` is necessary for a constant `Φ`
   serving **all** packings — or for any packing that *contains* the icosahedral witness — but it
   does **not** follow from `b > 0` in an arbitrary fixture. `cut_flow.py` now reports the
   **per-fixture** singleton bound `b(v)/deg(v)` explicitly (printed as
   `v0: 0.106563220973/12 = 0.008880268414`) and labels the value "for THIS fixture", with the
   universal reading spelled out separately. A valid *smaller* per-fixture `t*` is not rejected
   because of the universal floor.
2. **Positive deficit at degree zero is infeasible, and is reported as such.** It is *pointwise*
   infeasibility (the divergence bound cannot be met at that vertex at all), not a cut violation;
   it gets its own verdict `INFEASIBLE_POINTWISE` and no singleton bound is quoted for it
   (`tests_cut_flow.py` S8).
3. **Portability: every scratch-directory dependency removed.** Six scripts loaded the rational
   Fourier matrix from a hardcoded scratch path; there is now a local module `k15fourier.py` with
   its own self-test (upper-triangular, diagonal `(−1)^i`, `M² = I` at `K = 3, 5, 7`), and
   `audit_fourier.py` requires its checker path as an argument with **no default**. `grep -c /tmp
   *.py` now returns zero for every file.
4. **The resource estimate was wrong.** Measured here: `sos_qside_polish.py --degree 7
   --iters 4000 --seed 100 --uphill 0.05` takes **27 s** on the SAIR VM. On the reviewer's host,
   seeds 100–102 all hit a 90 s cap without producing a final candidate. So the estimate is
   **machine-dependent by at least 3×**, and the portable command must carry a larger default cap:
   `--cap 300` per seed, and a sweep of 20 seeds should be budgeted at **~30–100 minutes**, not
   the 13 minutes I quoted. The sweep's per-seed timeout marks `TIMEOUT` and continues, so a
   longer-than-expected run degrades gracefully rather than losing data.

**Caveat the test suite forced (`tests_cut_flow.py` S7), and it matters for reading that
threshold.** The binding cut need **not** be a singleton: absorbing a *positive*-deficit
neighbour into `U` costs something but removes an edge from the boundary, and when the neighbour's
deficit is small the trade pays. Explicit example: a star with centre `3/10`, one leaf `1/5` and two
leaves `−1/4` has `Σb = 0`, and the pair `{centre, positive leaf}` gives `(3/10+1/5)/2 = 1/4`
against the singleton's `(3/10)/3 = 1/10` — the pair binds. So a **singleton-cut bound is only a
lower bound on `Φ*`**; the exhaustive search up to `|U| = 6` is what makes `0.008880268291` a
defensible threshold for the icosahedral fixture (whose ring cells are so negative that larger `U`
loses), and `Φ*` could in principle be larger than any singleton computation suggests. Above that threshold a flow exists and is verified
exactly (`|φ| ≤ Φ`, divergence `≥ b`), reported as `PATCH_FEASIBLE`.

Note what the FCC/HCP controls show: on the two extremal packings the cut condition is
**vacuous**, so a test suite built on them has no power. That is a fact about the criterion worth
recording next to C044.

## 2. The overclaim, corrected

**What I claimed before:** "the cut condition is equivalent to Kepler for periodic packings",
arguing from a blob equal to a whole period, whose boundary term vanishes.

**Why it is wrong.** C044 quantifies over **finite** `U ⊆ Λ`. A period is a quotient object, not
a finite subset of the infinite packing, so the criterion simply does not apply to it. The
computation `Σ_{U} b = N(√32 − 1/ρ)` is correct arithmetic about a periodic cell, and it gives

> a **necessary density condition**: if the cut condition holds at some `Φ` then necessarily
> `mean b ≤ 0`, i.e. `ρ ≤ 1/√32`.

That is a condition on density. It is **not** the cut condition, it does **not** establish
equivalence with the family of finite-cut inequalities, and it says nothing about the infinite
extension. In particular it does not show that satisfying all finite cuts is as hard as Kepler.

**What would be needed for the stronger statement, and is not done.** The heuristic is that for a
packing with mean `b = c > 0`, a large finite `U` has `Σ_U b ≈ c|U|` while `|δ⁺(U)| = O(|U|^{2/3})`,
so the cut condition fails for large `U` at any fixed `Φ`. Turning that into a proof requires a
**uniform perimeter-growth bound** for a growing family of finite `U` inside the specific Voronoi
cell complex — i.e. a discrete isoperimetric estimate, which is standard in form but which I have
**not** established here. Until it is, the correct status is:

* `K15-C-CUTEQUIV-001` is **WITHDRAWN**;
* replaced by `K15-C-CUTDENSITY-001` (`PROVED`, elementary): the full-period computation yields
  the *necessary* density condition `ρ ≤ 1/√32`, and nothing more;
* the large-`U` statement is recorded as an **open obligation** with the exact missing lemma
  named (uniform perimeter growth).

### The correct version of the claim, proved through the transfer side

The withdrawn claim had a true conclusion reached by an invalid route. Here is the same conclusion
proved properly, and it is **stronger and sharper** than what I had asserted.

> **Theorem (`K15-C-TRANSFER-DENSITY-001`).** Let `Λ` be a periodic packing with `N` centres per
> fundamental domain of volume `V`, centre density `ρ = N/V`. If a transfer exists — an
> antisymmetric `φ` on the range-`R` graph with `|φ| ≤ Φ` and `Σ_w φ(v,w) ≥ b(v)` at every centre
> — then `ρ ≤ 1/√32`.

*Proof.* The packing and its cell complex are periodic, so summing the inequality over the `N`
centres of one fundamental domain gives `Σ_v Σ_w φ(v,w) ≥ Σ_v b(v) = N√32 − V`. The left side is
a sum over ordered pairs, and antisymmetry `φ(w,v) = −φ(v,w)` makes each unordered pair contribute
zero — including pairs in different copies of the domain, which periodicity identifies
consistently. So the left side is exactly `0`, whence `N√32 ≤ V`, i.e. `ρ ≤ 1/√32`. ∎

**Consequence, which is the thing Main needs.** For any packing with `ρ > 1/√32` — precisely the
packings a proof of Kepler must rule out — **no transfer exists at any capacity `Φ`**. So the
transfer/Hoffman route of `C035`/`C044` cannot *establish* the density bound where it is not
already true: it applies only where the conclusion holds. The route is **circular as a proof of the
density bound**, and its genuine content is confined to `C035`'s negligibility bookkeeping, which
is real but is not the geometry.

**Sharpness and consistency, checked numerically** (`transfer_necessity.py`):

| fixture | `Σ_v b` | `ρ` | transfer possible? |
| --- | --- | --- | --- |
| FCC (one cell) | **0** exactly | `0.1767767` `= 1/√32` | equality — the theorem is sharp |
| HCP (one cell) | **0** exactly | `0.1767767` | equality — sharp |
| periodised 13-cluster | `−4022.46` | `0.0031738` | yes, consistent with `cut_flow.py` finding a flow |

**What this does *not* say.** It does not say the cut *inequalities* are false or vacuous, nor that
individual finite cuts are uninformative — a violating cut remains a genuine obstruction (§1). It
says that *existence of a transfer* is strictly stronger than the density bound, so the flow
formulation cannot be the engine of the proof.

### Partial progress on the missing lemma (`cut_isoperimetry.py`)

The lemma needs `I(k)/k → 0`, where `I(k) = min{|δ⁺(U)| : |U| = k}`. On the one complex where the
profile is computable exactly — FCC, whose adjacency graph is the kissing graph on `√2·D₃` with 12
contact offsets — graph-balls give:

| `m` | `\|U\|` | `\|δ⁺U\|` | `\|δ⁺\|/\|U\|` | `\|δ⁺\|/\|U\|^{2/3}` |
| --- | --- | --- | --- | --- |
| 1 | 13 | 84 | 6.461538 | 15.193 |
| 3 | 147 | 444 | 3.020408 | 15.941 |
| 5 | 561 | 1092 | 1.946524 | 16.054 |
| 8 | 2057 | 2604 | 1.265921 | **16.100** |

The fitted exponent of `|δ⁺|/|U|` against `|U|` is **`−0.3230`**, essentially `−1/3`, and
`|δ⁺|/|U|^{2/3}` converges to **16.1**. So on this complex `|δ⁺(U)| ≈ 16.1·|U|^{2/3}` — the
`O(k^{2/3})` behaviour the lemma needs, with the constant.

**What this establishes and what it does not.** It exhibits the *mechanism*: for a packing with
mean deficit `c > 0`, `Σ_U b ≈ c k` eventually dominates `Φ·16.1·k^{2/3}` at any fixed `Φ`. It is a
computation on **one** complex (FCC, `TESTED_FINITE`), not a proof that a general packing's complex
has the same profile — `K15-CUTPERIM-001` **remains open**. But it converts "we have no idea
whether the mechanism is there" into "the mechanism is there on the extremal complex, with a
constant, and what is missing is the general-complex bound".

## 3. What the reviewer should hold against the earlier block

Two of my block-0308 statements do not survive review and are retracted here rather than
quietly amended:

1. `K15-C-CUTEQUIV-001`, "the cut condition is equivalent to Kepler" — **withdrawn** (§2).
2. `K15-C-SOSWHY-001`, "explicit-Gram families are weak for structural reasons" — already
   withdrawn in the previous block after the basin-hopping refuted it; it must not be revived.

## 4. Both-sides Gram: scoped negative, with the honest strength comparison

**The quintic construction now works** (`sos_both_sides_quintic2.py`). The one-square ansatz was
excluded, but allowing **two** squares in `σ₀` turns the system linear: choosing `(β, γ, d, e)`
rationally, `g` comes from `d² + g² = R`, then `h`, then `(f, i)` from a `2×2` linear system by
Cramer, then `k = q₀ − f² − i² > 0`. For the p-side record certificate it succeeds:

$$q(u) = \Bigl(-\tfrac74u^2 + 19u - \tfrac{25115432387}{806373792}\Bigr)^2
+ \Bigl(\tfrac74u^2 - \tfrac{3881}{252}u + \tfrac{322498331}{12799584}\Bigr)^2
+ \tfrac{322991273685970819}{325119346212229632}
+ u\Bigl(\tfrac76u^2 - \tfrac{35}{3}u + 18\Bigr)^2,$$

with both identities verified by expansion. **Independently cross-checked three ways:** the exact
conversion of `p` to the Laguerre basis has zero residual; `exactcert.certify` (own Sturm + Yun
over `Q`) **accepts** the certificate and reports `Δ = 1.3398238126`; and `q` computed from the
Fourier map `M p` equals the certified `q` identically. This gives `Δ ≤ 1.33982381256` — the **best both-sides
explicit-Gram certificate in this directory**, down from `2.00171738`, and equal to the best
one-sided p-side value. It remains `1.34×` the trivial bound.

Earlier attempts, retained:

| attempt | family | best `Δ ≤` |
| --- | --- | --- |
| `sos_both_sides_quintic.py` | quintic `q` from the p-side **record** certificate (`1.33982382`), two-square ansatz | **fails, with a reason** (below) |
| `sos_both_sides_search.py` | simple cubic p-side `−(u−T)(u−c)²`, two-square cubic `q` | 5.10334624 |
| `sos_both_sides_lin.py` | many **linear** squares in the p-side, so `q` stays cubic, hill-climbed | **2.4770679955** |
| (earlier) `sos_both_sides.py` | many quadratic squares, cubic `q`, one solve | 2.00171738 |

**The quintic ansatz fails for a stated reason, not by search failure.** With
`σ₁ = (au²+bu+c)²` and `σ₀ = (du²+eu+f)²+k`, matching coefficients leaves one free parameter and
forces `k = q0 − f² > 0`, i.e. `|f| < √q0 = 40.0739`. For that `q`, `|f|` has **minimum 195.95**
at `d ≈ 6.17`, and `|f| → ∞` as `d → 0` or `d → ∞`. So no choice of the parameter works and the
two-square ansatz is excluded for that certificate.

Rigour of the exclusion, stated precisely: `|f|` was evaluated on `3·10^5` points of `d ∈
(0.05, 300)`; it is **monotonically decreasing** up to `d = 6.177`, **monotonically increasing**
after it, with `|f(0.05)| = 3.6·10^7` and `|f(300)| = 2.5·10^6`. Hence the minimum over `d > 0`
is `195.948`, and `195.948 > 40.074`. The monotonicity is a numerical verification on a fine grid,
not a symbolic proof; the conclusion is a bound on `|f|` *within this parametrisation*, not a
claim about sums of squares in general.

**The honest strength table — the point of §4:**

| bound | value | comment |
| --- | --- | --- |
| **trivial** (density ≤ 1) | **1** | beats every both-sides certificate found here |
| Kepler | 0.74048049 | the theorem |
| Cohn–Elkies 2003 | 0.779747 | best explicit published certificate |
| LP-optimal in this basis | 0.77996622 | exact certificate, no rational Gram |
| **best both-sides explicit Gram (quintic, two squares)** | **1.33982381256** | `1.34×` the trivial bound |
| p-side only, many squares | 1.33982382 | `1.34×` trivial |
| Fourier-side only, five squares | 1.37125723 | `1.37×` trivial |

**So: every both-sides explicit-Gram certificate in this directory is weaker than the trivial
bound, and so are the one-sided ones.** They are format demonstrators only.

**How far, quantitatively — this is the honest version of the comparison.** `Δ < 1` is equivalent
to `p(0)/q(0) < 3/(4π) = 0.238732`:

| family | `Δ` | `p(0)/q(0)` | above the threshold |
| --- | --- | --- | --- |
| Fourier side, five squares | 1.37125723 | 0.327364 | **+37.1%** |
| p-side, many squares | 1.33982382 | 0.319859 | **+34.0%** |
| both sides, best | 2.00171737 | 0.477875 | +100.2% |
| LP-optimal (no rational Gram) | 0.77996622 | 0.186203 | −22.0% |

So the best explicit-Gram certificate needs `p(0)/q(0)` to fall by about **34%** to beat the
trivial bound. The search ladder `5.99 → 2.62 → 1.99 → 1.41 → 1.37` moved that ratio by a factor of
`4.4`, so a further `34%` is **plausible with more search power**. This is a **search-power gap,
quantified** — not an impossibility claim, and not a statement that explicit Gram certificates
cannot be competitive.

## 5. One portable command for the local pilot, and the sweep

`LOCAL_RUN_REQUEST.md` carries the pilot (and now also `cut_flow.py`, `tests_cut_flow.py` and
`cut_isoperimetry.py`). The sweep is a single command with a seed range, a time cap and an output
schema:

```bash
cd KeplerConjecture/Computation
timeout 600 python3 sweep_explicit_gram.py --seed-lo 100 --seed-hi 120 \
        --iters 4000 --uphill 0.05 --out-dir out/sweep
```

`sweep_explicit_gram.py` writes one JSON per seed with the schema

```json
{"seed": int, "degree": int, "iters": int, "uphill": float,
 "status": "VERIFIED_EXACT" | "FAILED",
 "delta": float,              // best certified Delta, if any
 "q": "polynomial in u", "p": "polynomial in u",
 "r": [[coeffs...]...], "s": [[coeffs...]...],   // the explicit Gram data
 "verification": {"q_identity": bool}}
```

and prints a summary line per seed, so a truncated run still yields usable data.
Each seed is bounded by `--cap` (default 120 s) and a capped seed is reported as `TIMEOUT`.
**Measured runtimes differ by more than 3× between machines** — 27 s per seed at `--iters 4000`
on the SAIR VM, but seeds that hit a 90 s cap locally — so budget `--cap 300` and expect
**30–100 minutes** for 20 seeds.

## 6. Status and obligations

| item | status |
| --- | --- |
| `K15-C-CUTFLOW-001` | **implemented and run**; exact thresholds; FCC/HCP controls vacuous by construction |
| `K15-C-CUTDENSITY-001` | **PROVED** (elementary): full-period ⇒ necessary density condition `ρ ≤ 1/√32` only |
| `K15-C-CUTEQUIV-001` | **WITHDRAWN** |
| uniform perimeter growth | **OPEN** — the missing lemma for any equivalence statement |
| both-sides explicit Gram | **scoped negative** above; best 2.00171738, weaker than trivial |
| quintic two-square | **excluded** for the record certificate (§4, `|f| ≥ 195.95`) |

**Reviewer asks for X:** (i) check `cut_flow.py`'s cut convention and that the singleton-cut
bound is computed from `b_lo`; (ii) confirm the `b` enclosures; (iii) confirm that no row promotes
a `PATCH_FEASIBLE` flow to a certificate; (iv) check the `|f| ≥ 195.95` bound's range.
