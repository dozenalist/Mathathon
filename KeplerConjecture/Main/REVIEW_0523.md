# Block `K15-REVIEW-0523-M` — review 0523: repairs, a certified twist theorem, and the proof-status account

Received `2026-11-14T13:34:47.301Z`. Sources reconciled by full hash:

| owner | hash | what it is |
| --- | --- | --- |
| C | `ae545b9a8757f165171ab0e60dab09cf98b1abd8` | D8 / X-C034 repaired: "the vertex set comes from `b`, never from the edge list" |
| E | `93c61a8b926eeece8ea0abff10e231757d76a2cc` | transitivity of the twelve pairs checked, not assumed (group order 60, orbit 12) |
| X | `a35b71346d0f0e976b63c6da2a243fac64b75d0a` | REPORT_X040 close, ~46 min substantive |
| supervisor | `194b40cffe972aed96e14ad0445da18728c14f5f` | review 04:38 + `SUPERVISION.md`, `SYNC_…json` |
| Main, from | `c4134c26aca42379559932ba85836e75b2dc0bcb` | previous block's tip |

## 1. D8 — independently reproduced, and independently verified repaired

The review reproduced D8 on C's *pre-repair* source: an isolated `b = +1` vertex is ignored by
`verify_flow_exact`, `find_violating_cut` and `feasible_flow`; an edgeless positive input falsely
passes; the exhaustive scan crashes.

**Main re-ran the same three entry points against C's repaired revision `ae545b9`**, extracting
`cut_flow.py` and `k15radicals.py` to a scratch directory and calling them directly:

| call | instance | result | correct? |
| --- | --- | --- | --- |
| `verify_flow_exact(b=[1,0,0], edges=[(1,2)], Φ=10⁹, φ={})` | isolated `b=+1` | `(ok_cap=True, ok_div=**False**, div=[0,0,0])` | **yes** — `div[0]=0 < b[0]=1` now fails |
| `find_violating_cut(b, edges, Φ=0)` | same | ratio `10¹⁸` sentinel, cut `(0,)`, `Σb=1`, boundary `0` | **yes** — the singleton cut is named |
| `feasible_flow(b, edges, Φ=0)` | same | `None` | **yes** — infeasible |
| `verify_flow_exact(b=[1,1], edges=[], Φ=0, φ={})` | edgeless, positive `b` | `(True, **False**, [0,0])` | **yes** — no longer falsely passes |
| `feasible_flow(b=[1,1], edges=[], Φ=0)` | same | `None` | **yes** |

The structural fix is what the review asked for: `n = len(b)`, and the divergence test runs over
`range(n)` — every vertex of `b`, not the vertex set of the edge list. `validate_fixture` also
rejects malformed edge lists, negative capacities, out-of-range flow keys and non-antisymmetric
flows. **D8 is repaired; Main verified the repair on the exact witness rather than on report.**
C holds the full-hour repair/near-contact contract task; nothing here duplicates it.

## 2. The six review items — all confirmed, all repaired

Detail and rejected text in `K15-C113`; the substantive one is §2.1.

| # | review item | disposition |
| --- | --- | --- |
| 1 | `C_R` must count only **crossing** edges | **Confirmed.** `C_R` is now exactly the edges with one endpoint in `W = B∖E_B`. The old wording ("every edge not internal") wrongly included edges with *both* endpoints in `E_B`, which contribute `0` to the counting identity. |
| 2 | verify compactness **cardinality** | **Confirmed.** `vol B(0,R+1)/vol B(0,1) = (R+1)³`, not `R³`; at `R = 21.865` that is `≈11957`, not `≈10453` (`1.4%`; conclusion unchanged). |
| 3 | verify **finite truncation redundancy** | **Confirmed and now stated:** a centre at distance `> 2R_max` has its bisector outside `B(v,R_max) ⊇ Ω(v)` and cannot cut (Main's Lemma 3) — that is what makes the compactification a statement about a *finite* configuration. |
| 4 | **Barlow equality is not an iff** | **Confirmed, retracted.** Barlow `⟹` equality in `(L)`; equality `⟹` Barlow is unproved and not claimed. "Exactly the equality family" retracted in three files. |
| 5 | **an average reaching a pointwise infimum need not force every term to equal it** | **Confirmed, retracted** — see §2.2. This was a real error. |
| 6 | **exact-contact matching is an extra hypothesis** | **Confirmed.** `ρ` counts edges at distance *exactly* 2, so any **scaled** saturated packing (min separation `2+ε`) has empty contact graph and `ρ = 0`. Theorem C is silent on that whole cone. Stated explicitly. |

### 2.1 A sampled twist maximum was not a proof — and it now is (`K15-C112`)

`C108` step (4) reported `max over a twist grid of the min cross-distance = 1.12555484451`,
sampled at `t = 0°, 18°, 36°, 54°`. **The review is right: that is not an all-twists proof.**
The grid value is retained only as retraction history.

**The proof.** For a pair `(a,q)` of the two eleven-point sets, the squared distance under a
relative twist is a pure sinusoid, `d²(t) = A + B cos t + C sin t`, so the twists putting that
pair closer than 2 form a set `{cos(t−ψ) < (4−A)/R}` that is **empty, the whole circle, or a
single arc** of half-width `arccos((4−A)/R)`. A clash for *every* twist is thus the statement
that finitely many arcs **cover** the twist circle, period `2π/5` (the icosahedral stabiliser of
the shared vertex axis).

```
Computation/twist_cover.py:   121 pairs -> 125 arcs, endpoints at 50 digits,
                              each endpoint INFLATED by 1e-20 (supersets, so a cover is conservative)
                              merged: 1 interval covering [0, 2π/5], length 1.25663706 = 2π/5
                              gaps: 0   ->  CERTIFIED
```

**Why a one-pair argument is impossible, recorded so it is not retried:** `min` over pairs of
`max_t d² = 8.4223 > 4`, so *no* single pair is always too close. The arcs must be combined —
which is exactly the content the sampled maximum could not see.

Status: `PROVED` modulo 50-digit arithmetic and the `1e−20` inflation. This upgrades `C108`
step (4) from `TESTED_FINITE`. Per the review, X's audit covers `C106`–`C108`, so this is handed
to X, not self-certified.

### 2.2 The retraction that matters: "the equality case is empty"

`C108` claimed *"The equality case of the dodecahedral density bound is empty — equality would
need every cell dodecahedral, hence every centre with twelve contacts, hence `ρ > 0`."*

**The first step is invalid**, exactly as the review says: an average reaching a pointwise
infimum **in a limit** forces only that the excess has zero density, not that any term equals the
infimum. Retracted in `C108`, `RESULTS.md`, `EXPOSITION_0438.md`, `GEOMETRIC_LEMMA_0438.md` and
`REVIEW_0438.md`. What survives: *if* `ρ > 0` the bound is strict; if `ρ = 0` nothing follows.
**The emptiness is open.**

Note what is *not* affected: Theorem D's step (3), where `x, y ≥ V_dod` with `x + y = 2V_dod`
genuinely forces `x = y = V_dod`. Two terms with a fixed sum — valid. The error was extrapolating
that to a limit of averages.

Consequently the pair route's gain is now stated only in its true form: **conditional on `ρ > 0`
and non-quantitative, and not a new packing bound.**

## 3. Worker results integrated

**E's payer search — eight bounded C5 pilots** (45 s each, one CPU, 1 GiB): best
`5.898007181138247`, **none below the required `5.763417470`**. So `(L)`'s critical pair survives
all eight seeds, with the margin `+0.134590`. Two caveats that must travel with the number:
the separation was checked **numerically only**, and an upper bound on a computed cell volume is
not a lower bound on the infimum — so this is *no refutation*, not support. E's
`93c61a8` also replaces an assumption by a check: the transitivity of the twelve pairs is now
verified (group order 60, orbit 12) rather than assumed.

**X's `a35b713`** closes REPORT_X040 at ~46 min substantive and audits the repaired finite/
infinite cut theorem with an independent exact Fourier–Motzkin comparison on small graphs — a
review of the *conditional graph statement*, not of the geometric cut inequalities.

**Local verifier timings, recorded as such:** Main's exact contact-polytope verifier passed in
`1.343 s`; X's G8 sample check passed in `3.141 s`. **The latter is finite agreement, not a
general soundness proof** — generic `shell_check` soundness remains **SUSPENDED** (`G12`, `PN-4`)
and nothing in this block changes that.

## 4. Proof-status account (the concise one)

**Proved, this project.** Every Barlow cell has volume `√32` on a repaired basis (`C094`/`C104`);
the contact polytope satisfies `K ⊆ B(v,√2)` exactly, both local types, Main's own exact
derivation; `σ₀ > 2V_dod` by compactness (`C108`) with the equality-case step now certified for
**all** twists (`C112`); the cut condition ⟺ transfer existence (`C093`, repaired at `D18`); and
the monotone bridge `δ ≤ 8π/(3K)` (`C106`/`C107`).

**Conditional or open.** `(L)` sharp pair bound `≥ 2√32` — E's conjecture, unproved, equality
proved only on the Barlow family (one inclusion). An explicit `δ₀ > 0` — open (E's payer).
`ρ > 0` for every saturated packing — open, and false for scaled examples. The emptiness of the
dodecahedral equality case — **open** (§2.2). Generic `shell_check` soundness — suspended.
Novelty of the two-cell inequality — not established.

**Not a bound.** Nothing in this block improves `0.754697399337` for all packings, and nothing
here should be quoted as a new packing bound. The project's best certificate remains
`Δ ≤ 0.779966216777`, which is not an improvement on the published `0.779747`.

## 5. Next package

**PN-C (continues C's full-hour task).** The repaired cut API is accepted on the D8 witness
(§1). Next: the exhaustive scan that crashed must be replaced, and near-contact instances
(`min separation 2 + ε`) must be in the fixture set, since those are exactly where the
exact-contact hypothesis of `C106`'s matching fails. *Acceptance:* every entry point returns a
verdict on the D8 witness, the edgeless witness and a scaled (`2+ε`) instance; exit non-zero on
any internal inconsistency; `≤1 CPU`, `≤1 GiB`, `≤300 s`.

**PN-E (continues E's interval/polytope task).** The geometric content is now exactly one number:
a lower bound `vol Ω(w) ≥ 5.763417470` for the partner of a dodecahedral cell, or any explicit
`δ₀ > 0`. *Acceptance:* a proof, or an explicit legal configuration with pair sum
`< 2V_dod + 0.213126`, or a documented obstruction. **Interval arithmetic, not floating point**,
for every inequality that enters a claim.

**PN-X.** (i) `C112`: check the arc-cover argument — that each pair's "too close" set is a single
arc, that the inflation is conservative, and that the merged cover has no gap; (ii) `C108`
Theorem D's compactness (cardinality now `(R+1)³`, truncation at `2R_max`); (iii) the retraction
in §2.2, to confirm nothing downstream still assumes the emptiness.

## 6. Honest accounting

**Fixed:** six review items, one Main-found defect (the sampled twist maximum), two retractions
with rejected text preserved (`C113`), one superseded `C093` bullet struck. **Added:** `C112`, a
certified all-twists theorem. **Verified independently:** C's D8 repair on the exact witness;
C's `t*` value `= (√32 − V_dod)/12`; A15's contact pair type `16.125`. **Not achieved:** any
number, any improvement over `0.754697399337`, any progress on the sharp `2√32`, and no proof of
`ρ > 0`. **Timing** is reported in the covering message.
