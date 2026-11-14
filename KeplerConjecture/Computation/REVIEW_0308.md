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

Arithmetic: FCC and HCP have `b = 0` exactly. The icosahedral fixture's cell volume involves
`√5`, so the file carries rational enclosures and uses `b_lo` to refute and `b_hi` for
feasibility — each direction conservative.

### Results

| fixture | deficits | verdict |
| --- | --- | --- |
| FCC (separation 2) | `b = 0` exactly, every cell | condition **satisfied trivially** at any `Φ ≥ 0`; **no information** |
| HCP | `b = 0` exactly, every cell | same |
| periodised icosahedral 13-cluster | central `b ∈ [0.106563219492, 0.106563221492]`; ring `b ≈ −335.214` | **the singleton cut `{0}` violates the condition for every `Φ < 0.008880268291`** |

The third row is the useful one: an **explicit finite cut** giving a rigorous lower bound
`Φ ≥ 0.008880268291` for that packing. Above that threshold a flow exists and is verified
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

## 3. What the reviewer should hold against the earlier block

Two of my block-0308 statements do not survive review and are retracted here rather than
quietly amended:

1. `K15-C-CUTEQUIV-001`, "the cut condition is equivalent to Kepler" — **withdrawn** (§2).
2. `K15-C-SOSWHY-001`, "explicit-Gram families are weak for structural reasons" — already
   withdrawn in the previous block after the basin-hopping refuted it; it must not be revived.

## 4. Both-sides Gram: scoped negative, with the honest strength comparison

The task asked to derive the quintic construction and to seek simpler structure with an honest
3D strength comparison. Three attempts, all with exact identities:

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
two-square ansatz is excluded for that certificate. (This is a bound on `|f|` over the
parametrisation, not a finite search claim.)

**The honest strength table — the point of §4:**

| bound | value | comment |
| --- | --- | --- |
| **trivial** (density ≤ 1) | **1** | beats every both-sides certificate found here |
| Kepler | 0.74048049 | the theorem |
| Cohn–Elkies 2003 | 0.779747 | best explicit published certificate |
| LP-optimal in this basis | 0.77996622 | exact certificate, no rational Gram |
| **best both-sides explicit Gram** | **2.00171738** | `2.0×` the trivial bound |
| p-side only, many squares | 1.33982382 | `1.34×` trivial |
| Fourier-side only, five squares | 1.37125723 | `1.37×` trivial |

**So: every both-sides explicit-Gram certificate in this directory is weaker than the trivial
bound, and so are the one-sided ones.** They are format demonstrators only. That is the honest
statement, and it is scoped to the families searched and to the constructions implemented — the
evidence does not support "explicit Gram certificates cannot be competitive", only that these
small-square families do not reach 1.

## 5. One portable command for the local pilot, and the sweep

`LOCAL_RUN_REQUEST.md` carries the pilot. The sweep is a single command with a seed range, a time
cap and an output schema:

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
`timeout 600` bounds each seed; the whole sweep is `20 × ~40 s ≈ 13 min` on one core.

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
