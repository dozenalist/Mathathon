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
                              each endpoint **shrunk inward** by 1e-30, so the arcs are SUBSETS of the true violation sets (K15-C123)
                              merged: 1 interval covering [0, 2π/5], length 1.25663706 = 2π/5
                              gaps: 0   ->  CERTIFIED
```

**Why a one-pair argument is impossible, recorded so it is not retried:** `min` over pairs of
`max_t d² = 8.4223 > 4`, so *no* single pair is always too close. The arcs must be combined —
which is exactly the content the sampled maximum could not see.

Status: `PROVED` modulo 60-digit arithmetic and the inward `1e−30` margin (`C123` corrected the
rounding direction — the original `1e−20` inflation was outward and unsound, review 0608). This
upgrades `C108`
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

## 2.3 The primary-source equality case — verified, not assumed (`K15-C115`)

The review asked for "the **actual primary-source** equality case". Every earlier block cited
Hales–McLaughlin's equality case from memory, and `REVIEW_0438` itself flagged it as "the softest
link in the chain". It is now read.

**Source:** Hales & McLaughlin, *The Dodecahedral Conjecture*, 6 pp.,
`sha256 beab1f4a…ef6960`, retrieved this block, `pdftotext -layout` (139 128 bytes of text),
spot-checked against the p. 2 page image.

> *"The assertion can then be stated as the inequality `vol(Ω(Λ,v)) ≥ vol(Ω(Λ_dod,0))` for every
> `v ∈ Λ`, and for every set of points `Λ ⊂ R³` whose pairwise distances are at least the diameter
> 2. **The case of equality occurs exactly when `Ω(Λ,v)` is congruent to a regular dodecahedron of
> inradius 1.**"*

Three things this pins down, all of which the ledger had been assuming:

1. **"Exactly"** — the equality case is a characterisation, not just attainment. That is precisely
   what Theorem D's step (3) needs, so **Theorem D's dependency is now a citation** and
   `REVIEW_0438`'s "softest link" is closed.
2. **The quantification is over arbitrary 2-separated point sets**, not over packings with a
   density. Theorem D minimises over 2-separated *configurations*, so no bounded-density or
   saturation hypothesis is smuggled in — this was worth checking and it checks out.
3. **A second, independent equality source:** §4 quotes Fejes Tóth's Theorem 4.1 — *"Let `P` be
   any polyhedron with at most 12 faces that contains a unit sphere `S²` … volume … at least
   `ω_dod`. Equality holds exactly [when] `P` is congruent to the regular dodecahedron."* That is
   a statement about **all** polyhedra containing a unit sphere, not about Voronoi cells, and it
   covers the `≤ 12`-face case on its own.

**What it still does not give.** No quantitative stability: neither the introduction nor Theorem
4.1 bounds how far from a dodecahedron a cell may be while remaining within `V_dod + ε`. So `δ₀`
remains non-explicit and `G11`/`G14` are unaffected. The verification removes an assumption; it
adds no number.

## 2.4 Honest comparison with known work: the dodecahedral bound is Kepler-scale

Reading the primary source (§2.3) also corrected a cost claim of my own, and this belongs in the
review record because the review's success criterion is "an honest comparison with known work".

`K15-C100`'s table put Hales–McLaughlin's cost down as *"one cell inequality (dodecahedron)"*, a
row that reads as a short proof and invites the inference that a **two**-cell inequality would
also be short. The source says otherwise: three programs (graph generation, a linear-programming
package, an interval-arithmetic inequality prover), *"several hundred linear programs"*, a
hypermap classification with LP infeasibility per hypermap system, and a local-deformation
argument for the `n ≥ 13` case. And on the comparison with the other proof: *"the two solutions
follow a similar outline and share a significant number of methods. Both are based on long
computer calculations."*

**So `0.754697399337` is Kepler-scale, not cheap**, and the pair route must not be advertised as
"a shorter proof than Hales" on the strength of that precedent. Withdrawn in `COMPLEXITY.md`; what
stands is narrower and still worth having: *if* `(L)` were proved, the remaining step to
`π/√18` is the elementary bridge of `C106`, so the proof's cost would be the cost of `(L)` alone.

The source also independently confirms `D19`: *"With the Dodecahedral problem, there is no such
flexibility. The problem about finite clusters of balls is fixed from the outset."* The per-cell
family is rigid — from the primary source, not from this project's inference.

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

## 3a. E's payer value, reproduced independently (`K15-C118`)

The eight bounded C5 pilots the review reports (best `5.898007181138247`, none below
`5.763417470`) all ran **E's own code**. The number is the most load-bearing in the whole route,
so Main rebuilt the configuration from E's written description and recomputed it with Main's code:

| quantity | Main | E | difference |
| --- | --- | --- | --- |
| `vol Ω(w1)`, frozen fixture | `5.89801737180372` | `5.898017371803720` | `1e−15` |
| min separation, all 78 pairs | exactly `2` | `≥ 2` | — |
| margin over the required `5.763417470` | `0.134599902` (frozen) / `0.134549652` (family optimum) | `0.134590` / `0.134549` | last digit |

So the pilot result is **independently confirmed**, and the two margins quoted across worker
documents are resolved: they are the *frozen fixture* and the *family optimum*, two different
objects, both positive. Two bugs in Main's own first attempt are recorded in `C118` (a fan
triangulation that does not tile a polytope, overcounting `11×`; and a legality test with zero
tolerance that reports a false failure).

**Still not support for `(P′)`.** E's own `K15-E090` is right that the fixture is a *local*
witness — its five pentagons would clash if repeated at all twelve outer centres — so it tests
the inequality at the sharpest pair and says nothing about simultaneous compensation.

## 3b. The pair route's scope checked against the trivial bound (`K15-C119`)

One thing had not been checked and should have been: is the pair route even *needed* over the
range it works on? Three elementary inequalities answer it.

1. Every cell contains the inball `B(v,d/2)`, so `δ ≤ 8/d³` for minimum separation `d`.
2. `8/d³ ≤ 0.754697399337` iff `d ≥ 2.1967082`, so **for `d ≥ 2.1967082` the dodecahedral bound
   is implied by the trivial inball bound** and ML does no work.
3. The near-contact band of `C116` reaches `6/√5 = 2.6832816`, strictly containing `2.1967082`.

So the only packings where a two-cell argument has to do anything are those with
`2 ≤ d < 2.1967082`, and on that whole range the near-contact pair bound is available with a
margin of `0.49` in `d`. **The route's scope is therefore fine; what remains is `ρ_ε > 0` — the
*density* of close pairs, not their existence.** That is `G13` and nothing else.

This is not new mathematics — `δ ≤ 8/d³` is the oldest bound in the subject — but the
comparison had not been made, and it says the route is aimed at the right regime.

## 3c. Fallback work: the first **explicit** stability bound, and the target it opens

The brief's fallback was "strengthen a concrete missing geometric lemma". Reading the primary
source made one available, and it is three lines.

**`C121` (proved, elementary).** Let `Ω(v)` have **at most 12 faces** and let every neighbour be at
distance `≥ 2ρ` (`ρ ≥ 1`). Then `vol Ω(v) ≥ V_dod·ρ³`. *Proof:* scale by `1/ρ`; the result is
convex, contains `B(0,1)`, has `≤ 12` faces all at distance `≥ 1`, so Fejes Tóth's Theorem 4.1
(quoted at `C115`) gives volume `≥ V_dod`.

This is exactly what `CLOSED_COMPONENT.md` A2 recorded as **needed and unavailable**: *"cells with
inradius `≥ 1.045` have volume `≥ V_dod·(1.045)³` — neither is available."* It is available. At the
isolated-vertex value `ρ = 1.045`:

```
vol Ω(v) ≥ V_dod·(1.045)³ = 6.333804 = 1.1197·√32 > √32 ,
```

so **`b(v) < 0` with a `12%` margin, with no compactness and no unspecified constant**, and the
singleton closed-component question is **settled in the `≤ 12`-face case**.

**Where it stops, exactly.** The hypothesis is a face count and it is *not* automatic: an isolated
vertex has all bisectors at `≥ 1.045`, so every neighbour within `2R_cell` cuts, and `R_cell` is not
bounded *a priori* without a volume bound. So the residual gap is precisely: *can an isolated
vertex's cell have more than 12 faces?*

**`C122` (proposed) — what would close it.** Repeat the three lines with any "`F`-face circumscribed"
constant `c_F`. The isolated-vertex requirement is `c_F·1.045³ > √32`, i.e.

```
c_F  >  4.95708216846 .
```

| `c_F` | source | `c_F·1.045³` | verdict |
| --- | --- | --- | --- |
| `V_dod = 5.550291` | Fejes Tóth, `≤ 12` faces | `6.333804` | `+11.97%` ✓ |
| `V_ico = 5.054056` | regular icosahedron, inradius 1 | `5.767518` | `+1.96%` ✓ |
| `4π/3` | inscribed ball only | `4.780105` | `−15.5%` ✗ |

So a bound for **circumscribed polyhedra with `≤ 20` faces** at `c ≥ 4.958` would close the
`≤ 20`-face case. Two gaps remain and both are stated: the face count is not free, and the `13–20`
face constants are a classical question Main has **not** resolved (whether the regular icosahedron
minimises among `20`-face circumscribed polyhedra is not established here — no source in the
repository, and it was not searched).

**Consequence for the ledger.** `G11` and `G14` are unchanged, but `C121` is the first *explicit*
stability statement the project has produced, and `C122` turns "settle the singleton question" into
two finite-dimensional sub-problems with numbers (`4.958`, and a face count).

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

**Fixed:** six review items, one Main-found defect (the sampled twist maximum), three retractions
with rejected text preserved (`C113`), one superseded `C093` bullet struck, and one cost claim of
my own withdrawn (`C117`).

**Added:** `C112` (certified all-twists theorem), `C114` (near-contact widening), `C116` (the band
`6/√5`, sharp), `C115` (primary-source equality case, audited), `C119` (where the dodecahedral
bound does work), and `Main/PROOF_STATUS.md`.

**Verified independently of worker code:** C's D8 repair on the exact witness (§1); E's payer
fixture to `1e−15` and its whole `14°` family (`C118`, `C120`); C's `t*` value
`= (√32 − V_dod)/12`; A15's contact-pair type `16.125`.

**Not achieved:** any number, any improvement over `0.754697399337`, any progress on the sharp
`2√32`, and no proof of `ρ > 0`.

**Artifacts pushed** (all on `kepler15/main`): this file, `Main/PROOF_STATUS.md`, and
`Computation/{twist_cover, twist_all_t, near_contact_band, payer_reproduce, payer_family}.py`;
reconciled `CLAIMS.md` (`C112`–`C122`, `C093` bullet struck), `ACCEPTED.md`, `RESULTS.md`,
`PROOF_GAPS.md` (`G13` new, `G14` reopened), `COMPLEXITY.md` (§1b and the §2a correction),
`EXPOSITION_0438.md`, `SOURCE_MANIFEST.md`. The check suite grew from 12 to 16 checks, all green in
`6.3 s`; the ledger linter passes.

**Timing** is stated in the covering message as measured — actual elapsed, not assigned.
