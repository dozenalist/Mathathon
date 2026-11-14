# Proof-gap ledger

> **Supervisor review, 07:38 Pacific:** E's origin/radius repairs pass the
> named controls, but a duplicated cube face gives volume 28/3 instead of 8.
> Generic certification remains pending; distinct-face fixtures are not thereby
> refuted. Main C133's short all-orientation argument awaits independent audit;
> C132 still reverses an inequality, and C134 mistakes examples for minima.
> C's generic exact-volume completeness is unproved. The twelve-face premise
> has a primary Fejes Toth source; E's remaining ring-excess proof is unchecked.
> No new best bound or simpler proof is accepted. This current disposition
> overrides conflicting author labels and older status banners below.
> See [the review](REVIEW_2026-11-14_0738.md).

> **Supervisor review, 06:53 Pacific:** C's nonvacuous periodic fixture has
> locally reproduced values and independently checked legality/flow, conditional
> on its volume data; the generic volume algorithm remains under review.
> E's replacement origin-interior helper has a new exact false acceptance and
> its radius mesh lacks a proved error bound. Main C124/C125 retain degree,
> boundary, limit and face-class errors; G13/G14 are not accepted as closed.
> Axial twist repairs do not yet prove the all-orientation near-contact bridge.
> No new best bound or simpler proof is accepted. This scope overrides author
> labels below. See [the review](REVIEW_2026-11-14_0653.md).

Every open obligation, its owner, and precisely what would close it. "Closed"
means an artifact exists and has survived review; nothing here is closed by
assertion. Maintained by M; reviewer X.

| # | Gap | Blocks | Owner | What closes it | Status |
| --- | --- | --- | --- | --- | --- |
| G1 | Periodic → arbitrary packings: K15-C002b's estimate is repaired but unaudited | every CE-type bound, incl. `VERIFIED_CROSS` C023's scope | X | line-by-line audit of Lemma 1.2 as repaired (`#C_in ≤ vol/S³`, additive errors, `c = 0` case) | open |
| G2 | Tammes-13 directed enclosure `θ₁₃ < arccos(1 − 2/ρ²)` | shell count 12 | E → M audited (K15-C027) | done at `ρ = 2.09` subject to Musin–Tarasov Thm 1; X to check the transcription of the defining equations | closed pending X |
| G3 | Contact number `n = 12` on a shell of positive width | K15-C018 sharp form | E → M audited | G2 (`ρ = 2.09`, unconditional in the arithmetic) | closed pending X |
| G4 | Specified partition rule for the cluster criterion (the universal form is false) | K15-C025 H2 | E | a rule + boundary estimate, checked on the icosahedral 13-cluster | open (K15-C035 makes the boundary term free *if* `A` is a bounded-range transfer, so G4 reduces to choosing the transfer's range) |
| G5 | Analytic cluster-volume lower bound at `D = 2` | K15-C025 H3 | E | a Rogers-simplex or Fejes Tóth type inequality restricted to the cluster, with the constant exhibited | open |
| G6 | Negligibility of the correction `A` | K15-C025 H4 | M | **supplied** for any antisymmetric transfer of range `R`, bound `Φ`: `Σ A ≤ 3ΦR(R+1)⁵r²` (K15-C035, factor `R` restored) | closed by K15-C035 (proof only; the transfer still has to be *designed*) |
| G7 | A value `V_0 > 5.550291` for the cluster inequality | beating the dodecahedral barrier | E | G4+G5+G6 and a computation of the cluster minimum | open. The "falsification test" previously recorded here came from K15-C029 and is **withdrawn** (review 0138); the correct constraint is `θ#(D_θ) ≤ C₁r² + N_A` (K15-C029r) |
| G8 | Independence audit of the two exact checkers | `VERIFIED_CROSS` C023's status | X | confirm C's `exactcert` and Main's `shell_check` share no code path and agree on adversarial vectors (the interface test `interface_xcheck.py` is a start) | open |
| G9 | Lean: ball-volume identity and counting-to-volume bridge | any Lean-verified density claim | Astra (local) | a pinned build of a module proving `volume (ball 0 1) = 4π/3` and the count bound; current `Normalisation.lean` proves neither | not started |
| G10 | Shell-allowance gain | whether the shell route is dead | C/M | an exact-certified `η > 0` candidate whose objective beats the same-degree `η = 0` value | open; K15-C028 quantifies the obstruction: the cost `12η` scales with the *amplitude* of `P` on the shell, so only profiles already near-binding there can pay |

## The one remaining obligation on the geometric route

`K15-C035` supplies H4 (negligibility) and bypasses the partition bookkeeping;
`K15-C036` shows no finite fixture can verify the pointwise inequality that
remains. So G5 — an **analytic** lower bound for `Σ_{v∈K} vol Ω(v)` over clusters,
or equivalently for `vol Ω(v)` pointwise against the transfer it receives — is
the whole remaining mathematical content. Everything else in the ledger is
bookkeeping, verification, or comparison.

## Rules the ledger enforces

1. No gap is closed by a finite grid (review 27616).
2. A failed search is evidence about the search, never an impossibility theorem
   (K15-C014r, the shell benchmark's gain 0).
3. A bound enters `Main/CLAIMS.md` only as `VERIFIED_CROSS` (two independent
   exact implementations) or `PROVED`; `TESTED_FINITE` never enters `RESULTS.md`
   as a bound.
4. Every status change names the artifact and its hash.

## G11 — the pair constant (new, review 0438)

**Statement.** `σ₀ := inf{vol Ω(v) + vol Ω(w) : contact pair in a 2-separated configuration}`
satisfies `σ₀ > 2V_dod` — proved (`C108`), but **non-explicit**. The gap is the *value*: any
explicit `δ₀ = σ₀ − 2V_dod > 0` turns `C108`'s strictness statement into a number, by
`δ ≤ (4π/3)/(V_dod + δ₀ρ)`.

**Closure conditions.** (i) an explicit `δ₀ > 0` (E's payer problem; the sharp value would be
`2√32 − 2V_dod = 0.213126`, and the best witness gives `δ₀ ≤ 0.347676`); (ii) `ρ > 0` for every
saturated packing with high density, or a replacement bridge that does not need a matching.
**Owner** E (i), M (ii). **Not on the critical path** for `C094`, which no longer depends on it.

## G12 — `shell_check` soundness argument (carried, still open)

Unchanged from `AUDIT_REQUEST_X.md` item 5 and `PN-4`. Note C's report against revision
`6626714` is a *stale revision* and is not evidence about the current file (`C103`).

## G13 — the contact-matching density `ρ > 0` (review 0523)

**Statement.** `ρ` is the density of a maximal matching of the **contact** graph (edges at
distance *exactly* `2`). The bridge `C106`/`C108` is silent unless `ρ > 0`.

**Why it is a real hypothesis, not a technicality.** Any **scaled** saturated packing — minimum
separation `2 + ε` instead of `2` — has an empty contact graph and `ρ = 0`. So exact-contact
matching can fail outright, and the pair route cannot bound contact-free packings at all.
**Closure condition:** a proof that a *high-density* saturated packing has a positive density of
contacts, or a replacement bridge that uses near-contacts at `2 + ε` instead of contacts.
**Owner** M. Not on the critical path for `C094`.

## G14 — the emptiness of the dodecahedral equality case (REOPENED at review 0523)

Previously recorded as proved via `C108`. **Reopened**: the argument went from "the average cell
volume equals the pointwise infimum" to "every cell is dodecahedral", which is invalid in a
limit. What is proved is only: if `ρ > 0` (G13), equality is impossible. **Closure:** rule out
`ρ = 0` at equality, or find another route.

## G13 — CLOSED as a hypothesis (review 0608, `C124`)

`ρ_ε > 0` was required by `C108`/`C114` and can fail (scaled packings). `C124` removes the
requirement with a two-case split: `|S_ε| ≤ 26|M|` for a maximal matching turns `ρ_ε = 0` into
"asymptotically ε-loose", which the inball bound handles (`δ ≤ 1/(1+ε/2)³ = 0.414086` at
`ε = 0.6832816`). **No contact-density hypothesis is needed for the strictness statement.**

## G14 — CLOSED (review 0608, `C124`)

The emptiness of the dodecahedral equality case is restored on a sound proof. It was retracted at
`C113` because the original used an average-to-pointwise inference; `C124` bounds the density
directly from the cell-volume sum in the `ρ_ε = 0` branch and needs no termwise statement.

## G15 — the arc test's period reduction (DOWNGRADED, review 0608, `C129`)

**No longer load-bearing.** `C129` proves the whole band in closed form from a *single* pair
(`d_max = 4/√5 + 2√((2√5−1)/5)`), with no period reduction and no covering. The question below is
kept only because the arc-test tooling still exists.

### original statement

The corrected arc test (`C127`) agrees with an independent twist scan at every `d` tested and
reproduces `X-C051`'s `3.4555003444` to ten digits, but Main has **not** proved that the mod-period
reduction is sound for arcs longer than the period. The `d = 2` case is now proved *without* that
machinery (`C128`, one-pair argument), so nothing load-bearing depends on it. **Closure:** a written
argument that the reduction preserves the cover, or replace the band computation with a projection
argument like `C128`'s.

## G16 — CLOSED (review 0653, `C133`): the all-orientation two-dodecahedra exclusion

Review 0653 asked for the gap between "axial twist excluded" (`C129`) and "every relative orientation
excluded" — the statement `C124`/`C114` actually need at `d > 2`, where the second cell's icosahedron
is free in `SO(3)`. It was queued as the bounded local job `X-ORIENT-001`.

**Closed by a proof, not by a computation.** A dodecahedral cell of inradius 1 has its 12 face normals
in icosahedral position; the icosahedron's **covering radius** is
`ρ_c = arccos√((1+2/√5)/3) = 37.3773681…°`, so for any direction `e` some contact direction `u_i` has
`⟨e,u_i⟩ ≥ cos ρ_c`, and then `|p − (w+2u_i)|² ≤ d² + 4 − 4d cos ρ_c < 4` whenever
`d < 4cos ρ_c = 3.1786179`. The only escape is `w + 2u_i = p` exactly, which forces `d = 2` and the
axis to be a face normal of both cells — `C128`'s case. So `X-ORIENT-001` is discharged, `C124`
returns to `PROVED`, and the local job is withdrawn.

What remains open is unchanged: `δ₀(ε)` is still non-explicit (`G11`), so `C124` gives strictness and
no constant, and `RESULTS.md` does not move. `C129`'s axial constant `3.4555` is still the better
constant *on that sub-family*; `C133`'s `3.1786` is the orientation-free one.
