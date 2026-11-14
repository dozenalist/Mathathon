# Referee report v2 — MC120 (strict <120°), the endpoint, and the equilateral collapse

Swarm `smwgpu16s` (unchanged, still running; members `m1`, `m2`; model `deepseek/deepseek-v4.1-flash`;
`reasoning_effort=max`; `member_steps=60`; `minutes=60`; dir `.ultramath/smwgpu16s`). Grades **[P]** hand proof,
**[S]** source-read / parent-compiled, **[C]** cited, **[X]** open.

## 0. Retractions of MY v1 corrections — all three were wrong

| # | my v1 claim | why it is wrong |
|---|---|---|
| **R1** | "uniform strip width over a compact subarc is not established; the source gives `δ` pointwise with no continuity" | **Wrong.** Nesting gives it elementary: if the strip at base direction `e` of width `δ` lies in the open set `S`, then for `dist(e′,e) < δ/2` the strip at `e′` of width `δ/2` is contained in the strip at `e` (angular and radial ranges nest), hence in `S`. So the condition "a strip of width `δ` at `e′` lies in `S`" holds on a neighbourhood of every `e` where it holds at all, i.e. `e ↦ sup δ` is positive and lower semicontinuous, and on a **compact** subarc it has a **positive minimum**. The parent has now compiled this as `outerAngularStrips_compact_radius` in `ConeGeometry` (standard axioms), together with OA120/CC60 and a concrete consumer [S]. My objection was to the *source's* lemma statement, and it does not transfer to the compiled angular-neighbourhood version. |
| **R2** | "the endpoint `a = 120°` is also covered, since `γ(r) < 60°` strictly" | **Circular, and false.** Choosing the pair at angular gap `γ(r)` *after* `r`, and needing the strip widths at those two directions to exceed `r − 1`, gives no `r` satisfying both. Worse, the supervisor's **Reuleaux counterexample** refutes the conclusion: see §1. My extension is **withdrawn**; MC120 keeps **strict `< 120°`**. |
| **R3** | "the equilateral arithmetic fails for 2-element blocks (union ≤ 4)" | **Misreading of the transmitted statement.** A *paired block* is **two adjacent edge exclusions combined**, `E_{2k} ∪ E_{2k+1}`, e.g. `{0,1} ∪ {1,2} = {0,1,2}` — three labels. Two blocks are therefore **four continua** and cover `≥ 5` labels. My "vertex block" reformulation happens to coincide, but the transmitted arithmetic was already correct and needed no repair. See §2. |

## 1. The Reuleaux counterexample, audited [P]

`A = (√3/2, −1/2)`, `B = (√3/2, 1/2)`, `C = (√3, 0)`: all three are unit vectors (angles `−30°, +30°, 0°`) and
pairwise at distance `1`, so they are an equilateral triangle of side `1`. Let
`W := (B(A,1) ∩ B(B,1) ∩ B(C,1)) ∩ {|z| > 1}` with **open** balls.

*`W` is the intersection of three open unit disks, i.e. the interior of the Reuleaux triangle of width `1`, cut by
`|z| > 1`. The Reuleaux triangle has diameter `1` and its interior has all pairwise distances `< 1`; hence
**`W` contains no unit pair** ✓ — so "`c` is a.e. constant on `W`" is *not* contradictory there.

*For every `θ ∈ (−π/6, π/6)` the direction `e(θ)` lies in all three open disks (at `θ = 0` the distance to `A` is
`0.517… < 1`; at `θ → ±30°` the distance to `C` stays `≤ 0.518`), and by strictness the same holds on a
**radial range** `|z| ∈ (1, 1+δ(θ))`. So there is a genuine **outer** angular/radial strip of full width `60°`
inside `W` — an open `60°` outer arc that is monochromatic and contains no unit pair.

*Exactly why my endpoint argument dies here.* At radius `r`, the maximal half-angle of a point still inside the
disk about `A` is `θ_max(r) = arccos(r/2) − 30°`, attained **on** the Reuleaux arc; and the half-angle needed for
a unit pair at radius `r` is `arcsin(1/(2r))`. These two are **identically equal**:
`sin(arccos(r/2) − 30°) = (√3/2)√(1−r²/4) − r/4 = 1/(2r)`. So the pair sits exactly on the boundary of `W`, never
inside: at `60°` there is **no slack**, and an open `60°` arc can never contain a unit pair. This is the sharp
form of "the endpoint is not claimed", and it validates keeping MC120 **strict**.

*What the example does and does not refute.* It refutes any argument that derives a contradiction from
"outer strip + residual ≤ 1" alone at aperture `120°` (i.e. arc width `60°`). It does **not** refute the actual
MC120 theorem at `< 120°`, nor any stronger separately-proved actual-continuum statement — consistent with the
supervisor's scoping.

## 2. MC120 and the equilateral collapse, final form

> **MC120 (strict, as banked) [P]+[S].** `c` measurable weak, centre `x`, finite family `K_i` with
> `ApproachingContinuum x (K i) v i`, directions in a closed cone of aperture `a < 120°`, `H_i` excluded on
> `Straddle(K_i)`, `J = [k] ∖ ⋃ H_i`. If `|J| ≤ 1` and `W ≠ ∅` then `False`.
>
> Proof unchanged from v1: `I` has width `180° − a > 60°`; take a compact subarc of width `> 60°`; by
> `outerAngularStrips_compact_radius` (R1) it carries a **uniform** positive width, so `W` contains a band of
> angular width `> 60°` and radial range `(1, 1+δ₀)`; inside it, at any `r ∈ (1, 1+δ₀)`, two points at angular
> separation `γ(r) = 2arcsin(1/(2r)) < 60°` are at distance exactly `1` and both lie in `W`; a.e. `W`-points have
> colour `j`, while weak properness separates a.e. unit pair on a circle meeting `W` in a positive angular arc —
> contradiction. **The strictness `< 120°` is what produces the slack `width(I) − γ(r) > 0`; at `120°` the slack
> vanishes (Reuleaux, §1).**
>
> **EC (equilateral collapse, as transmitted, corrected reading) [P].** Let `c` be a measurable weak `6`-colouring
> and let three continua at a common centre carry **paired blocks** `B_k = E_{i_k} ∪ E_{i_k+1}` (two adjacent edge
> exclusions, three labels each), with the three block-vertices pairwise at distance `≥ 2` on the 6-cycle (so, up
> to relabelling, `{0,1,2}, {2,3,4}, {4,5,0}` — the only such families). Then every pair of blocks leaves exactly
> one label, MC120 gives pairwise separation `≥ 120°`, and three gaps summing to `360°` with each `≥ 120°` are all
> `= 120°`: **the three directions are exactly equilateral.**
>
> *If two block-vertices are adjacent* (`{0,1,2}` vs `{1,2,3}`) the union leaves **two** labels, only CC60's
> `> 60°` applies, and a **continuous family** survives — which is why the collapse must not be stated for
> arbitrary triples.
>
> **A note on a member's counter-proposal [X].** `m1` offers `0°/120°/250°` as a refutation of the
> "120° span" step. Its **circular** separations are `120°, 130°, 110°` — the last is `< 120°`, so it fails the
> hypothesis; with circular (shorter-arc) separations the three-gap argument is valid (a gap `> 180°` forces one
> of the others `< 90° < 120°`). So the triple is not a counterexample to EC, but it does correctly warn that
> *linear* differences along a fixed coordinate are the wrong reading.

## 3. Relay status, stated exactly

`ultramath_status` (this block) shows `waiting_for_verdict: []`, `accepted: 0`, both members **running** —
`m2` on `d1` (the three quantitative hinges of MC120), `m1` on `d2` (a direction-packing theorem). **There is no
message channel to a running member**: the only relay path is the reason field of `ultramath_verdict`, which is
available only when a member submits. So these corrections are **not yet relayed**; they will be attached to the
first verdict, and I will not claim they have been delivered until then. In the meantime R1–R3 above are recorded
here so that no downstream artifact inherits the wrong versions.

## 4. Accepted vs speculation

**Accepted:** MC120 with strict `< 120°` (with the compiled uniform-width lemma), including the empty-residual
case `J = ∅ ⇒ W = ∅`; the Reuleaux counterexample as a *sharp negative* for the endpoint; EC for the three-block
family `{0,1,2},{2,3,4},{4,5,0}`.

**Withdrawn:** my R1, R2, R3.

**Open [X]:** whether the equilateral configuration admits a six-colour-specific obstruction (the assignment for
`m2`); whether blocks at adjacent vertices (two labels left) can be excluded at all; anything global about
`χ(ℝ²)`; the 57/60 + continuous-family count is taken as the bank's, not re-derived here.

**Exact unresolved obligation.** For the equilateral three-block family: produce a source-licensed statement —
consuming only actual continua, `WeakColoring 6`, and the compiled cone lemmas — that contradicts it, or prove
that it is consistent with all of them. Absent that, the six-colour common-interface stage reads: aperture
`< 120°` with `≤ 1` residual impossible; equilateral triples rigid but not excluded; adjacent-block triples have
continuous families.
