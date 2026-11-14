# Direction d3 — null-set (representative) robustness of the palette, and sharpness of eps > 0 in (D)

Member m3, swarm smwfyhztv. Scope: **only** the palette object as formalised in
`lean/OAI/Geometry/PlaneColoring/`. Nothing here says anything about chi(R^2).

Definitions, verbatim from the repo (so every statement can be checked against the formalisation):

* `Compactness.lean`: `Typical c z := DensityOne {w | c w = c z} z`;
  `DensityOne A x := Tendsto (fun r => volume (A ∩ closedBall x r) / volume (closedBall x r)) (𝓝[>] 0) (𝓝 1)` (`WeakColoring.lean:119`).
* `Compactness.lean`: `TypicalSampling c y r := 0 < r ∧ ∀ᵐ t ∂angularMeasure, Typical c (y + r*direction t)`.
* `sampleFn c y r i t = if c (y + r*direction t) = i then 1 else 0`; `sample = toLp` (its L2 class).
* `Compactness.lean:261`: `IsTrace c hc x b := (x,1,b) ∈ closure (sampleSet c hc)`,
  `sampleSet = {(y,r,sampleCode c hc y r) | TypicalSampling c y r}`;
  `trace_realization`: every trace is realised by `y n → x`, `r n → 1`, all `TypicalSampling c (y n) (r n)`.
* `Palettes.lean`: `tracePositive x i b = {t | 0 < traceValue b i t}`,
  `paletteSet x i = ⋃ b ∈ paletteGenerators, tracePositive x i b`, `paletteGenerators` any countable
  essential cover (`tracePositive_le_palette`, `paletteSet_minimal`).

**What (D) can even mean.** `paletteSet`, exactly as defined, depends on the chosen representatives of the
L2 classes `traceValue b i`; only its class modulo `angularMeasure` is canonical. So an equality of palettes is
only assertable a.e. in the direction — which is what (D) says. Below I prove the *trace-set* and
*generator-set* equalities exactly (no a.e. at all), and the palette statement a fortiori.

--------------------------------------------------------------------------------

## Theorem 1 (dichotomy of typicality at a recoloured point)

Let `Z` be Lebesgue-null, `c' = c` off `Z`, `Z' = {z | c' z ≠ c z} ⊆ Z`. Then

* (i) `z ∉ Z'` => (`Typical c z ↔ Typical c' z`);
* (ii) `z ∈ Z'` => **not both** `Typical c z` and `Typical c' z`.

*Proof.* (i) `c' z = c z =: i`, and off `Z` the classes `{c = i}` and `{c' = i}` coincide; they differ
inside the null set `Z`, and `DensityOne` is unchanged when the set is changed on a null set (the numerator
`volume (A ∩ closedBall x r)` is unchanged). (ii) Put `i = c z`, `i' = c' z`, `i ≠ i'`. Off `Z`,
`{c = i'} = {c' = i'}` and `{c = i} = {c' = i}`, so `{c' = i'} ⊆ {c = i'} ∪ Z`, whence
`dens({c' = i'}, z) ≤ dens({c = i'}, z) =: d'` (null sets have density 0 at each point), and symmetrically
`dens({c = i}, z) ≤ dens({c' = i}, z)`. The sets `{c = i}`, `{c = i'}` are disjoint, so `d + d' ≤ 1` with
`d = dens({c = i}, z)`. If `Typical c z` then `d = 1`, so `d' = 0`, so `dens({c' = i'}, z) = 0 < 1`, i.e.
`¬ Typical c' z`. Symmetric in `c, c'`. ∎

*Remark.* (ii) is why a null-set recolouring is hard to see: a point is a density point of the colour it is
*given* only if that colour already fills its neighbourhoods (up to a null set).

## Theorem 2 (KEY: two typical centre-circles see the same colours)

If `TypicalSampling c y r` **and** `TypicalSampling c' y r`, then for every `i`

    sampleFn c y r i =ᵐ[angularMeasure] sampleFn c' y r i,

hence the two `sample` elements of `L2(angularMeasure)` are equal.

*Proof.* Write `z t = y + r * direction t`, `A = {t | Typical c (z t)}`, `A' = {t | Typical c' (z t)}`; both
are conull by hypothesis (`0 < r` holds in both hypotheses). Let `D = {t | c' (z t) ≠ c (z t)} ⊆ {t | z t ∈ Z}`.
For `t ∈ D` we have `z t ∈ Z'`, so by Theorem 1(ii) the two properties `Typical c (z t)` and
`Typical c' (z t)` are mutually exclusive; hence `D ∩ A ∩ A' = ∅`, while `A ∩ A'` is conull, so `D` is
`angularMeasure`-null. Off `D`, `c (z t) = c' (z t)`, so both `sampleFn`s agree at `t`. ∎

Theorem 2 needs nothing beyond `volume Z' = 0`: no geometry, no hypothesis on how circles meet `Z`. The
density-point predicate — not the shape of the sampling circle — is what makes null-set changes invisible.

## Theorem 3 (generator sets agree wherever both predicates hold)

With `S_c := sampleSet c hc` (viewed in `ℂ × ℝ × (Fin k → L2)`):
`S_c ∩ {TypicalSampling c'} = S_{c'} ∩ {TypicalSampling c}`, and on
`{TypicalSampling c} ∩ {TypicalSampling c'}` the two generator sets are literally **equal**.
Immediate from Theorem 2.

## Theorem 4 (clean unconditional equal-palette criterion)

Assume `Z' = {z | c' z ≠ c z}` is null **and no point of `Z'` is `Typical` for `c`, and no point of `Z'` is
`Typical` for `c'`** — the situation of every "recolour a null set with a label whose class is thin there"
gadget (recolour a curve, an annulus boundary, a finite union of circles, a Cantor set...). Then

    TypicalSampling c y r ↔ TypicalSampling c' y r        (all y, r)
    S_c = S_{c'}                                          (all y, r, s)
    IsTrace c hc x b ↔ IsTrace c' hc x b                  (all x, b)
    paletteSet c hc x i = paletteSet c' hc x i             (all x, i; as sets)

so `P^c_x(e) = P^{c'}_x(e)` for **every** direction `e`, not merely a.e.

*Proof.* (`⇒` direction of the first line; the other is symmetric.) Let `T' = {t | z t ∈ Z'}`. If
`angularMeasure T' > 0`, then for a.e. `t ∈ T'` the point `z t` is `Typical` for `c` (hypothesis
`TypicalSampling c y r`), contradicting the standing assumption on `Z'`. So `T'` is null, and for a.e. `t`
we have `z t ∉ Z`, where `Typical c (z t) ↔ Typical c' (z t)` by Theorem 1(i) and `c (z t) = c' (z t)`. Hence
`TypicalSampling c' y r`; the samples agree by Theorem 2. Trace sets are the closures at `(x,1)` of literally
equal generator sets, so they are equal, and `paletteGenerators` depends only on the family
`{tracePositive x i b}` (the same family for both colourings), so `paletteSet` is literally the same set. ∎

*What Theorem 4 does NOT cover, stated exactly.* Only a recolouring that **creates** density points: some
`z ∈ Z'` with `c' z = i'` and `dens({c = i'}, z) = 1` while `c z = i ≠ i'`, so `z` is `Typical` for `c'` but not
for `c`. Then a pair with `TypicalSampling c' y r` can have `angularMeasure{t | z t ∈ Z'} > 0`, and by Theorem
1(ii) `TypicalSampling c` fails there, so Theorem 3 says nothing. Whether a `c`-trace realised only by such
pairs can carry a colour outside the `c'`-palette is **not settled here**; a counterexample would have to live
exactly there. I did not find one. Theorem 2 shows the mechanism is not "the circle meets the null set" (that
is irrelevant) but "the null set carries a point of full density of its new colour".

--------------------------------------------------------------------------------

## Theorem 5 (the eps > 0 in (D) is necessary: sharpness at R = 1)

There are `x_0`, `k = 8` and measurable `c, c' : ℂ → Fin 8` with `c = c'` on `{|z - x_0| ≥ 1}`
(agreement off the open unit ball, i.e. the `eps = 0`, `R = 1` case) such that `P^c_{x_0}(e) ≠ P^{c'}_{x_0}(e)`
for a.e. direction `e` (in fact the difference set is conull; see the proof).

*Construction* (`x_0 = 0`). Let `c` be the hexagonal 7-colouring with colours `0,…,6` (colour classes unions of
open hexagons with a fixed measurable choice on the boundaries, so every interior point of its class is a
density point of that class); colour `7` is never used. Let `A = {z | 9/10 < |z| < 1}` (open annulus,
`A ⊆ B(0,1)`), and `c' = 7` on `A`, `c' = c` off `A`. Then `c = c'` on `{|z| ≥ 1}`, both measurable.

* `7 ∉ P^c_0(e)` for every `e`: `c` never takes the value 7, so `sampleFn c y r 7 ≡ 0`, hence
  `traceValue b 7 = 0` and `tracePositive 0 7 b = ∅` for every trace `b`.
* `7 ∈ P^{c'}_0(e)` for every `e`: take `y_n = 0`, `r_n = 1 - 1/n` (so `y_n → 0`, `r_n → 1`). For `n ≥ 11`
  the circle `{|z| = r_n}` lies in `A`, whose points are interior to the open class `{c' = 7}`, hence
  `Typical c'` there; so `TypicalSampling c' 0 r_n` holds (indeed the a.e.-condition holds everywhere) and
  `sampleFn c' 0 r_n 7 ≡ 1`. The samples are the constant function 1, so by `sampling_weak_compact` /
  `trace_realization` the limit `b` of this sequence is a trace at `0` with `traceValue b 7 =ᵐ 1`, giving
  `tracePositive 0 7 b =` all directions and `paletteSet 0 7` conull. Hence `7 ∈ P^{c'}_0(e)` a.e. `e`.

So `P^c_0(e) ⊆ {0,…,6}` while `7 ∈ P^{c'}_0(e)`: the palettes differ a.e. in the direction. (The reason the
statement is a.e. and not "for every e" is the one noted at the top: `paletteSet` is defined through chosen
representatives of the L² classes `traceValue b i`, so only its class modulo `angularMeasure` is canonical; here
`tracePositive 0 7 b` is a representative of the whole direction circle.) ∎

Note it is the *open* annulus of positive area that is visible: `{|z| = 1}` itself is null, and recolouring
exactly the unit circle would be invisible by Theorem 4.

*The positive side of the threshold (for comparison).* For `R = 1 - eps < 1` the argument needs no density input:
if `|y - x_0| < eps/2` and `r > 1 - eps/2`, then for every unit `u`,
`|y + r u - x_0| ≥ r - |y - x_0| > 1 - eps`, so `c` and `c'` agree at every sampled point and, moreover,
agree on a whole *neighbourhood* of it (`|z - x_0| > 1 - eps` leaves room
`|z - x_0| - (1 - eps) > 0`), whence `Typical c (y + r u) ↔ Typical c' (y + r u)`; so
`sampleFn c y r = sampleFn c' y r` identically in `t`. The window `{|y - x_0| < eps/2, r > 1 - eps/2}` is an
**open** neighbourhood of the target point `(x_0,1)` in `(y,r)`-space, so the closures of the two generator sets
at `(x_0,1)` coincide, the trace sets are literally equal, `paletteSet` needs no a.e. repair, `eps` is
independent of `k`, and `P^c_{x_0}(e) = P^{c'}_{x_0}(e)` for every direction `e`. That is (D); the full write-up
belongs to d1 (m2), which owns that direction — recorded here only to locate the threshold that Theorem 5 shows
is sharp.

--------------------------------------------------------------------------------

## Status, honest summary

* Proved here: Theorem 1, 2, 3 (null-set robustness at the level of generator sets, hypothesis
  `volume Z' = 0` only), Theorem 4 (palettes equal for *every* direction when the recolouring creates no density
  points), Theorem 5 (`eps > 0` in (D) is necessary; the boundary is `R = 1`).
* Not settled here: palettes under a recolouring that *creates* density points (residual case isolated above),
  and the full (D) statement itself (d1's direction; the ingredient it needs is the open-neighbourhood argument,
  not Theorem 2).
* No claim about chi(R^2) is made or implied.
* **No numerics were run under this direction**: the claims are proved, not estimated. The only computational
  object, the hexagonal 7-colouring, enters solely via "its colour classes are unions of open hexagons, hence
  their interior points are density points of their class", which is exact. The disk-recolouring experiments of
  task (2) and the PHASE-TRANSITION arithmetic of task (4) are d1's; kept disjoint on purpose.
