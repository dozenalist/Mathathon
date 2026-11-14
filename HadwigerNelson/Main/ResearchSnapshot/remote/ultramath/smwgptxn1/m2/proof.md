# MC120: exact form, exact sharpening, and what fails in the sketch

Member m2, swarm `smwgptxn1`, direction d1 (attack MC120 / multi-centre producer).
Everything below is at paper level, in the project's own hypotheses; the only computation is
`check.py` (exact/symbolic, ~6 s, no SAT, no Lean build).

---

## 0. Verdict, in one paragraph

**MC120 is TRUE as stated, but its printed sketch contains a genuine gap and its printed
consequence is not a contradiction.** The gap: the sketch's operative inequality is not
`2·asin(1/(2r)) < 60°`; the real criterion is the **diameter criterion** of Lemma 1,
`max{2(1+δ)sin(w/2), √(δ²+4(1+δ)sin²(w/2))} > 1`, where `δ` is the *uniform outer strip width
over a closed subarc*,
and `r` is not free — one needs `r ∈ (1, 1+δ_J)`. Because of this the true threshold is
**strictly better than 120° for every datum** (Theorem 2) and MC120 is the limiting
`δ → 0` form. The printed consequence is moreover **stronger than what follows**: Theorem 1
gives only *spread* `≥ 120°` (largest gap `≤ 240°`), **not** pairwise distance `≥ 120°`, and
therefore **not** "equilateral" (countermodel `{0°, 60°, 200°}`). §7c is stated in that corrected
weak form; the regular triple is a boundary case consistent with MC120, not a forced one. §7
supplies a genuinely different, multi-centre producer that removes the aperture bound
altogether but needs fat windows.

---

## 1. Exact hypotheses used (quoted from the tree, not re-derived)

* `WeakColoring k c` (`PlaneColoring/Coloring.lean:27`):
  `AEMeasurable c volume ∧ ∀ᵐ p ∂(volume.prod angularMeasure), c p.1 ≠ c (p.1 + direction p.2)`.
  So the bad unit-pair set is null in the **3-dimensional** space `ℂ × S¹`. (This is
  important: a 2-parameter family of monochromatic unit pairs does *not* contradict it;
  an **open** family does. Lemma 2 uses exactly this.)
* `Straddle K = {z | ∃p∈K, ∃q∈K, dist z p < 1 ∧ 1 < dist z q}` (`AngularBoundary.lean:147`), open.
* `ApproachingContinuum x K v` (`AngularBoundary.lean:235`): `x∈K`, `r : ℕ→ℝ` with `r n > 0`,
  `r n → 0`, unit `w n → v`, and `x + r n • w n ∈ K`.
* `ApproachingContinuum.outer_strip` (`AngularBoundary.lean:244`): if `‖e‖=1`, `0 < ⟪e,v⟫`
  then `∃δ>0`, `∀e', ‖e'‖=1 → dist e' e < δ → ∀r, 1<r → r<1+δ → x + r•e' ∈ Straddle K`.
* `finite_support_exclusion_ae` (`AngularBoundary.lean:317`): for measurable `c`,
  `(∀i ∀j∈F i, Disjoint (spatialSupport c j) (Straddle (K i)))` ⟹
  `∀ᵐ z, ∀i, z ∈ Straddle (K i) → c z ∉ F i`.
* `Acute`: `direction : Angles → ℂ`, `Angles = AddCircle (2π)`; `direction (t)` is the unit
  vector of angle `t`. Aperture/cones are measured on `Angles` (oriented, mod 2π).

Fix reference: residual `R := Fin k \ ⋃_{i∈E} F i`, and the window `W := ⋂_{i∈E} Straddle (K i)`.

---

## 2. Lemma 1 (exact diameter criterion for an annular sector)

For `x ∈ ℂ`, `w ∈ (0, π]`, `δ > 0` put
`S(x; w, δ) := { x + r·direction(t) : 1 < r < 1+δ, |t − t₀| < w/2 }` (an open annular sector).

* `S` is connected (image of the connected open rectangle `(t₀−w/2, t₀+w/2) × (1, 1+δ)`).
* `inf{‖p−q‖} = 0`, and the diameter is exactly the sector-annulus diameter

  `diam S = max{ d₁ , d₂ }`,  `d₁ := 2(1+δ)·sin(w/2)`,  `d₂ := √(δ² + 4(1+δ)·sin²(w/2))`

  (the two competing farthest pairs are the two **outer** corner points, giving `d₁`, and an
  **inner** corner with the **opposite outer** corner, giving `d₂`; because `0 < w ≤ π` no other
  pair is farther). Note `d₂ ≥ δ`, so the *radial* width is covered by `d₂`.

Consequently, since the distance function is continuous on a connected set, its image is an
interval with endpoints `0` and `diam S`, so (`diam S` need not be attained: `S` is open and
the interval may be half-open — irrelevant)

> **`S` contains a pair at distance exactly 1  ⟺  max{d₁, d₂} > 1.`**

Two exact evaluations used below: `max{d₁,d₂} = 1 ⟺ d₁ = d₂ = 1`, and
`d₁ > d₂ ⟺ sin(w/2) > ½√(δ/(1+δ))`. Hence (solving `d₁ = 1` and `d₂ = 1` exactly)

* if `0 < δ < (√5−1)/2` then the two thresholds satisfy `2asin(1/(2+2δ)) < 2asin(√(1−δ)/2)`,
  so **the criterion is `w > 2·asin(1/(2+2δ))`**;
* if `δ ≥ 1` then `d₂ ≥ δ ≥ 1`, so the criterion holds for **every** `w > 0`;
* at `δ = 0` both thresholds equal `π/3`.

*Exact values* (`check.py` (a),(b)): `2·sin(π/6) = 1` exactly; and a cone of aperture `a`
gives the common-positive arc width `w = π − a`, so `a = 2π/3` gives `w = π/3` exactly. Hence
**`w > π/3` (i.e. `a < 120°`) implies `d₁ = 2(1+δ)sin(w/2) > 2·1·sin(π/6) = 1` for every `δ > 0`**,
and at `w = π/3` with `δ = 0` (the open arc of width exactly 60° at radius exactly 1) the
diameter is exactly `1`, so there is **no** unit pair: for `0 < θ < π/3` the chord is
`2 sin(θ/2) < 2 sin(π/6) = 1`. That is the exact sense in which `120°` is the boundary.

## 3. Lemma 2 (an open set with a unit pair is not a.e. monochromatic)

Let `c` be measurable, `WeakColoring k c`, `U ⊆ ℂ` open, `z₁,z₂ ∈ U`, `‖z₁−z₂‖ = 1`, and
`ρ : Fin k`. Then `¬ (∀ᵐ z, z ∈ U → c z = ρ)`.

*Proof.* `V := {(z,u) ∈ ℂ × S¹ : z ∈ U ∧ z+u ∈ U}` is **open** in `ℂ × S¹` and contains
`(z₁, z₂−z₁)`, so `(volume × angularMeasure)(V) > 0`. Under the assumption, `c z = ρ` for a.e.
`(z,u) ∈ V`, and `c(z+u) = ρ` for a.e. `(z,u) ∈ V` (the set of `u` with `z+u` in a plane-null
set is null on `S¹`; Fubini). So `c z = c(z+u)` on a positive-measure subset of `ℂ × S¹`,
contradicting `WeakColoring`. ∎

*This is the step the sketch calls "violating a.e. monochromaticity … via a common
translation". It must be run on the open pair set `V`, not on a single chord: a single chord
(or a 2-parameter family) is null in `ℂ × S¹` and contradicts nothing.*

## 4. Lemma 3 (uniform outer width — the mechanism the sketch asserts without proof)

Let `x ∈ ℂ`, `K ⊆ ℂ`, `ApproachingContinuum x K v`, and let `J` be a **closed** arc of
directions such that `c_J := min_{direction(t) ∈ J} ⟪direction(t), v⟫ > 0`. Then
`∃ δ_J > 0` such that **for every** `e' ∈ J` and every `r ∈ (1, 1+δ_J)`: `x + r•e' ∈ Straddle K`.

*Proof (explicit constant).* Take `n` with `r n ≤ c_J/2` and
`|⟪direction(t), w n⟫ − ⟪direction(t), v⟫| ≤ c_J/4` for all `direction(t) ∈ J` (uniform in `t`
by compactness of `J` and `w n → v`). Put `q := x + r n • w n ∈ K`, `m_J := r n·c_J/2 > 0`.
For `e' ∈ J`:
`‖e' − r n·w n‖² = 1 − 2 r n ⟪e',w n⟫ + (r n)² ≤ 1 − 2 r n·(3c_J/4) + r n·c_J/2 = 1 − r n c_J
< (1 − m_J)²`-form, so `‖e' − r n w n‖ ≤ 1 − m_J`. Hence
`dist(x + r e', q) ≤ (r−1) + (1 − m_J) < 1` when `r < 1 + m_J`, while
`dist(x + r e', x) = r > 1`. So `x + r e' ∈ Straddle K` by definition. ∎

Take `δ_J := m_J`. **Note `δ_J` is produced by compactness-plus-uniformity in `n`, hence is
strictly positive on every closed subarc, but is not bounded below as `J` grows** (as `r n → 0`,
`m_J = r n c_J/2 → 0` for the tangent-most `c_J`). This is precisely the loose end in the sketch.

---

## 5. Theorem 1 (= MC120, exact and proved)

**Hypotheses.** `k ≥ 1`; `c : ℂ → Fin k` measurable, `WeakColoring k c`; `x ∈ ℂ`; `E` finite;
`K : E → Set ℂ`, `v : E → ℂ` with `Nonempty (ApproachingContinuum x (K i) (v i))` for all `i`;
label sets `F : E → Finset (Fin k)` with `∀i ∀j∈F i, Disjoint (spatialSupport c j) (Straddle (K i))`;
`R := Fin k \ ⋃_i F i` with `|R| ≤ 1`; and the directions `v i` all lying in a **closed cone of
aperture `a < 2π/3`**.

**Conclusion.** `False`.

*Proof.* (1) `I := {t : ∀i, 0 < ⟪direction t, v i⟫}` is an open arc of width `π − a > π/3`.
(2) Pick a closed subarc `J ⊂ I` with `π/3 < w_J < π − a`. By Lemma 3 (applied for each `i`
and intersected) there is `δ_J > 0` with `S(x; w_J, δ_J) ⊆ W := ⋂_i Straddle (K i)`.
(3) `finite_support_exclusion_ae` gives `∀ᵐ z ∀i, z ∈ Straddle (K i) → c z ∉ F i`; hence
`∀ᵐ z, z ∈ W → c z ∈ R`, and `|R| ≤ 1` so a.e. `z ∈ W` has one label `ρ`.
(4) `S := S(x; w_J, δ_J)` is open, `S ⊆ W`, and by Lemma 1 `S` contains a unit pair because
`2(1+δ_J) sin(w_J/2) > 2·1·sin(π/6) = 1`. Lemma 2 gives `False`. ∎

(If `R = ∅`, step (4) is unnecessary: `W` is nonempty open and plane-null — the
"empty-residual / strict < 180°" rule; `a < π` gives `w > 0`.)

## 6. Theorem 2 (sharpening: the true threshold; MC120 is the `δ → 0` limit)

Same hypotheses, but replace the aperture hypothesis by

> there is a closed subarc `J ⊂ I` with `max{2(1+δ_J)sin(w_J/2), √(δ_J² + 4(1+δ_J)sin²(w_J/2))} > 1`,

i.e. equivalently (Lemma 1, and for `0 < δ_J < (√5−1)/2 ≈ 0.618`) `w_J > 2·asin(1/(2+2δ_J))`,
i.e. **`a < π − 2·asin(1/(2+2δ_J))`** for that datum. Then `False` — by the same proof, with
step (4) read off directly.

Strictness: for every `δ_J > 0`, `2 asin(1/(2+2δ_J)) < π/3`, so the admissible aperture is
**strictly larger than 120° for every datum**, with slack `π/3 − 2asin(1/(2+2δ_J))`
(exactly `125.93°` at `δ_J = 0.1`, `120.65°` at `δ_J = 0.01`; `check.py`).
Since `inf_{δ>0} (π − 2 asin(1/(2+2δ))) = π − π/3 = 2π/3`, **MC120's constant 120° is exactly
the uniform (`δ ↓ 0`) limit and cannot be improved by any aperture-only rule of this shape.**
MC120 is thus correct and optimal *as an aperture-only rule*, but not sharp for a given colouring.

**Endpoint.** At `a = 2π/3` exactly, `w = π/3` and the argument needs
`2(1+δ_J) sin(w_J/2) > 1` with `w_J < π/3`, i.e. `w_J > 2asin(1/(2+2δ_J))`; both sides tend to
`π/3` as the subarc grows to the open arc, so the endpoint holds **iff** the datum's strip
width dominates the angular margin. This is exactly the open obligation of §8.

## 7. What is FALSE in the printed sketch and in its printed consequence

**(7a) The inequality `2·asin(1/(2r)) < 60°` is not the operative one.** It is neither
necessary nor sufficient. The exact statement is Lemma 1 with `δ = δ_J`:
`r` is not free, it must satisfy `r < 1 + δ_J`, and the correct test is Lemma 1's
`max{d₁,d₂} > 1` (with `d₁ = 2(1+δ_J)sin(w_J/2)`); the sketch's chord form is the sub-case
`r = r' = 1+δ_J`, which needs `r ≥ 1/(2 sin(w_J/2))` **and** `r < 1+δ_J` simultaneously.
Keeping the sketch's chord formula gives the same condition only when one *also* keeps
`r ∈ (1, 1+δ_J)`; the sketch states "a fixed radius `r > 1`", which is false as a uniform claim.

**(7b) "any two blocks cover 5 labels" is FALSE.** Two adjacent-edge pairs
`E_i = {i,i+1}`, `E_j = {j,j+1}` have `|E_i ∪ E_j| ≤ 4`; the exact maximum over the 36 ordered
pairs is **4** (`check.py` (b)). The correct label count is: no two edge-pair blocks can leave
`≤ 1` label, so a third block is genuinely needed, and `|⋃_{i∈I} E_i| ≥ 5` for exactly
**14 of the 20** three-element index sets `I ⊆ {0,…,5}` (`check.py` (b) lists them, e.g.
`{0,2,4} → [0..5]`, `{0,2,5} → [0,1,2,3,5]`).

**(7c) CORRECTED — the consequence is WEAKER than "equilateral", and it is a reduction, not a
contradiction.** *(This replaces an earlier, wrong version of 7c that read Theorem 1 as giving
"pairwise circular distance ≥ 120°"; the judge's countermodel is `{0°, 60°, 200°}`, whose
spread is `200° ≥ 120°` while `0°` and `60°` are only `60°` apart. That inference is invalid and
is withdrawn.)* Theorem 1 gives exactly:

> the three directions are **not contained in an open cone of aperture `< 120°`**, i.e. their
> **spread** is `≥ 120°`, i.e. the **largest gap** between consecutive directions is `≤ 240°`.

Equivalently, in "arc" form: the least closed arc containing the three directions has length
`≥ 120°`. This is *not* a pairwise condition. The correct dictionary (and the only thing
`check.py` (c) certifies) is:

* **pairwise `≥ 120°` ⟺ the regular triple** `{θ, θ+120°, θ+240°}` — a bound on the three cyclic
  gaps, which sum to `360°`. (`check.py` (c): on a 0.5° grid with tolerance `1e-12` the only such
  set is `{0°,120°,240°}`.) So "equilateral" is exactly the *pairwise* boundary statement, which
  we do **not** have; and it is not **necessary** for Theorem 1 — e.g. `{0°, 130°, 250°}` has
  spread `130°` (so is MC120-compatible) with `circ-dist(250°, 0°) = 110° < 120°`.
* The pairwise bound that *is* available at six colours is the two-block one: with only two
  edge-pair blocks the residual has `≥ 2` labels (`|E_i ∪ E_j| ≤ 4`), so only CC60 applies and
  the conclusion is the much weaker "**not** in a closed cone of aperture `≤ 60°`", i.e.
  separation `> 60°`. Three blocks are genuinely needed to reach `spread ≥ 120°`.
* "Must be exactly equilateral" is therefore **not proved**, and the regular triple is a
  **boundary case consistent with** MC120, not a forced one.

*Why pairwise `≥ 120°` cannot be recovered from Theorem 1 at all.* To force it one would have to
apply MC120 to a **pair** of blocks, and a pair always leaves `≥ 2` labels. In the orbit-A pattern
(pairs `{0,1}, {1,2}` at one direction, `{2,3}, {3,4}` at `120°`, `{4,5}, {5,0}` at `240°`) the
two 4-interface sub-families `{0,1,2,3}` and `{0,1,4,5}` already cover 5 labels at spread exactly
`120°`, and the full six-interface family covers all 6 labels — so there `R = ∅`, and **the
co-size-0 case applies, which needs no aperture at all**, only `⋂_i Straddle (K_i) ≠ ∅`
(the "empty-residual / strict `< 180°`" rule: if `R = ∅` then `W := ⋂_i Straddle (K_i)` is
plane-null, hence empty, so `W ≠ ∅` is already a contradiction and Lemma 2 is not needed).
Note that at spread `120°` the common-positive arc is **empty**, so Lemma 3 gives `W ≠ ∅`
*nowhere* here: this co-size-0 route is a **far-field / reach** condition on the continua, with
no angular content, and it is the honest frontier.

*And the boundary is consistent:* at spread exactly `120°` the three unit points
`y_j = x + direction(q_j)` are at pairwise distance `|1 − e^{2πi/3}| = √3` exactly
(`check.py` (d)), so they form no unit triangle and no further unit-distance constraint fires.
MC120 *reduces* the six-colour edge-pair problem to the spread-`120°`-boundary stratum; it does
not kill it, and "equilateral" was an overclaim.

**(7d) The open question I can state but not settle.** At spread exactly `120°` with strand-like
continua (e.g. `x = 0`, `K_i` a short radial segment in direction `v_i`, all inside the unit
disc), the common-positive arc is empty, so Lemma 3 gives nothing; whether
`⋂_i Straddle (K_i)` nevertheless contains a **unit pair** is a question about the *reach* of the
continua, not about the angular data, and it must be decided per family. Exact model computation
(`K_i = [0, ½ v_i]`, `v_i = e(0), e(2π/3), e(4π/3)`, `v₁+v₂+v₃ = 0`): I claim
`⋂_i Straddle (K_i) ∩ B(0,1) = ∅`. Indeed, if `z ∈ ⋂_i Straddle (K_i)` then for each `i` there
is `q ∈ K_i` with `‖z−q‖ > 1`. Writing `q = s v_i`, `0 ≤ s ≤ ½`, and using `‖z‖ < 1`:
`‖z−q‖² = ‖z‖² + s² − 2s⟪z,v_i⟫ > 1` forces `2s⟪z,v_i⟫ < ‖z‖² + s² − 1 ≤ ‖z‖² − 3/4 < 0`, so
`s > 0` and `⟪z,v_i⟫ < 0` — for **all three** `i`. But `Σ_i ⟪z,v_i⟫ = ⟪z, v₁+v₂+v₃⟫ = 0`, so the
three inner products cannot all be negative. Hence `⋂_i Straddle (K_i) ∩ B(0,1) = ∅` inside the
unit disc; in that model the window is empty there and the exclusions are vacuous.
**The endpoint is therefore genuinely undecided by the geometry used here, which is exactly why
MC120 declines it.**

---

## 8. A different producer: the two-centre overlap rule (no aperture bound)

**Theorem 3 (exact).** Let `c` be measurable with `WeakColoring k c`. Let `x, y ∈ ℂ`, let
`W_x, W_y` be open sets with a.e. label bounds `∀ᵐ z, z ∈ W_x → c z ∈ R_x` and
`∀ᵐ z, z ∈ W_y → c z ∈ R_y` (these follow from `finite_support_exclusion_ae` with
`W_x = ⋂_i Straddle (K_x i)`, `R_x = Fin k \ ⋃ F_x i`, and likewise at `y`). Put
`D := W_x ∩ W_y`. If `D` contains a pair at distance `1` and `|R_x ∩ R_y| ≤ 1`, then `False`.

*Proof.* A.e. `z ∈ D` has `c z ∈ R_x ∩ R_y`, a set of at most one element; `D` is open and
contains a unit pair; Lemma 2. ∎

This is **not a same-centre exclusion**: it uses two centres and needs no cone, no aperture and
no `BinaryCenter` hit. It strictly extends CC60 on the residual-size-2 stratum: CC60 needs
aperture `≤ 60°` at one centre, Theorem 3 needs only `|R_x| = |R_y| = 2`, `|R_x ∩ R_y| = 1`,
and `D` fat enough.

**Exact geometric certificate (two centres at unit distance, full annular windows).** Let
`‖x − y‖ = 1`, `W_z^ann := {p : ‖p − z‖ ∈ (1, 1+δ)}` for `z = x, y`, and
`D = W_x^ann ∩ W_y^ann`. Take the perpendicular bisector line of `xy`; on it,
`‖p − x‖ = √(1/4 + h²)`, so the points of `D` on that line are those with
`h ∈ (√3/2, √((1+δ)² − 1/4))`. Hence the *segment* `{h ∈ (√3/2, √((1+δ)²−1/4))}` lies in `D`
and contains a unit pair **iff**

> `√((1+δ)² − 1/4) − √3/2 > 1  ⟺  1 + δ > √(2+√3) = (√6+√2)/2  ⟺  δ > (√6+√2)/2 − 1 ≈ 0.93185…`

(`check.py` (e), exact: `√(2+√3) − (√6+√2)/2 = 0`). So Theorem 3 applies in this geometry iff
`δ > (√6+√2)/2 − 1`, and then **no aperture restriction at all** is imposed on the directions.

*Honest scope.* The programme's actual windows are *sectors*, not full annuli, so this
certificate is a criterion, not an application: Theorem 3 fires on the residual-size-2 stratum
as soon as the two windows meet in a set with a genuine (same-component) unit pair, which
needs either fat `δ` or very wide direction arcs. In the programme's thin-strip regime
(`δ ∼ r_n → 0`) it does not currently fire.

---

## 9. The exact unresolved obligation

> **(O1) Endpoint / uniform optimality.** Decide whether there is an absolute `A < 120°` such
> that "same-centre exclusions with `|R| ≤ 1` and all approach directions in a closed cone of
> aperture `≤ A`" is contradictory. By Theorem 2 this is *equivalent* to: is
> `sup over admissible data of 2·asin(1/(2+2δ_J))` strictly below `π/3`, i.e. is the uniform
> strip width `δ_J` bounded below by a positive constant in terms of the angular margin
> `π/3 − w_J` alone (independent of the approach sequence)? Lemma 3 gives only
> `δ_J = r_n c_J/2`, which tends to `0` as the approach sequence is taken deeper; no lower
> bound is known. MC120 correctly declines to claim the endpoint.
>
> **(O2) The spread-`120°` boundary stratum.** By §7c (corrected) MC120 reduces the six-colour
> edge-pair case only to "spread `≥ 120°`", i.e. largest gap `≤ 240°` — *not* to the regular
> triple. The regular triple is the boundary case of that stratum and is *not* excluded by any
> argument above. Two ways forward, both open: (a) a multi-centre argument (Theorem 3 is the
> natural candidate and needs a window-intersection fatness not presently available);
> (b) the residual-`∅` far-field route of §7c: two 4-interface sub-families already cover 5
> labels at spread exactly `120°` (orbit-A), so the co-size-`0` case applies there and needs
> only `⋂_i Straddle (K_i) ≠ ∅` — a *reach* condition on the continua, with no angular
> hypothesis at all.
>
> **(O3) The endpoint, cadastrally.** §7d: at spread exactly `120°` with strand-like continua
> the common-positive arc is empty and a model computation gives `⋂_i Straddle (K_i) ∩ B(0,1) = ∅`
> (in that model), so the window is empty and the exclusions are vacuous. Whether *some*
> strand-like family makes the window nonempty with a unit pair at spread exactly `120°` is not
> settled here.

## 10. How a referee checks this in under a minute

1. `python3 check.py` (exact/symbolic, prints `2*sin(pi/6) = 1`; `w(2π/3) = π/3`; the 14/20
   and max-union-4 counts; the only regular triple; `|1−e^{2πi/3}| = √3`; and
   `√(2+√3) = (√6+√2)/2`). Under 7 s (measured 5.7 s).
2. Lemma 1 and Lemma 2 are three-line proofs; Lemma 2's only subtlety (open pair set, not a
   chord family) is the exact point where the sketch is imprecise.
3. Lemma 3 carries its constants; Theorem 1 then follows verbatim.
4. §7b is a two-line label count. §7c is now the *weak* correct form: spread >= 120 deg
   (largest gap <= 240 deg), NOT pairwise >= 120 deg; `check.py` (c) certifies only the
   sufficient boundary condition "spread 120 deg AND pairwise 120 deg => regular triple".

## 11. Grading of my own claims

| claim | grade |
|---|---|
| Lemma 1 (diameter criterion, exact threshold) | proved, exact, machine-checked constants |
| Lemma 2 (open pair set vs `WeakColoring`) | proved at paper level |
| Lemma 3 (uniform strip, explicit `δ_J`) | proved at paper level, explicit constants |
| Theorem 1 (= MC120, strict `< 120°`) | **TRUE**, proved; sketch repaired |
| Theorem 2 (sharp data-dependent threshold; 120° = uniform limit) | proved |
| §7a/§7b (sketch's inequality; "two blocks cover 5 labels") | **FALSE as printed**, exact countervalues |
| §7c (spread >= 120 deg only; "pairwise >= 120 deg" and "equilateral" WITHDRAWN) | corrected; exact `√3` and countermodel `{0,60,200}` |
| §7d (endpoint at spread exactly 120 deg, strand-like continua) | model computation only; **open** |
| Theorem 3 (two-centre overlap rule) | proved; exact `δ > (√6+√2)/2 − 1` certificate |
| endpoint `120°`, spread-`120°` stratum | **open** (O1), (O2), (O3) |
