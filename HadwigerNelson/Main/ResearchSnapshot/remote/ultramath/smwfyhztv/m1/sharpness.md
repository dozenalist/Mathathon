# Far-field decoupling for the palette object: the threshold is exactly 1

**Swarm `smwfyhztv`, member m1, direction d2 (sharpness / refutation).**
Repo read: `lean/OAI/Geometry/PlaneColoring/{Compactness,Palettes,Transitions}.lean`.

**Verdict.** The lemma (D) *as stated* (hypothesis `eps > 0`, i.e. agreement off the
open ball `B(x_0, 1-eps)`) is **true**, with no dependence on `k`, no properness,
and no dependence on the rest of the colouring. The constant `1` in it is
**exactly optimal and not attained**: at `eps = 0` (agreement only on
`{z : |z - x_0| >= 1}`) the conclusion **fails**, and it fails on a set of
directions of *full* angular measure (§4, two explicit colourings). The exact
determinant of the palette at `x_0` is the **germ of `c` at the sphere
`S(x_0,1)`** (§3, Theorem 4), not `c` off any sphere of radius `< 1`.

Nothing below says anything about `chi(R^2)`.

---

## 1. The objects, in the repo's own notation

(`Compactness.lean`, `Palettes.lean`; `μ` = `angularMeasure` on `Angles`, finite.)

* `Typical c z  :=  DensityOne {w | c w = c z} z`  — `z` is a Lebesgue density
  point of its own colour class.
* `TypicalSampling c y r  :=  0 < r ∧ ∀ᵐ t, Typical c (y + r·direction t)`.
  Note `direction t` is a unit complex number, so `y + r·direction t` runs over
  the **circle** `C(y,r) = {y + r u : |u| = 1}`.
* `sampleFn c y r i t = if c (y + r·direction t) = i then 1 else 0`,
  `sample c hc y r i` = its `Lp ℝ 2 angularMeasure` class,
  `sampleCode c hc y r` = the `TraceVector k = Fin k → WeakBall.Space (RealL2 …)`.
* `IsTrace c hc x b  :=  (x,1,b) ∈ closure (sampleSet c hc)`, and
  `trace_realization` / `trace_of_realization` say precisely:

  > `IsTrace c hc x b` iff there are `y : ℕ → ℂ`, `r : ℕ → ℝ` with
  > `TypicalSampling c (y n) (r n)` for all `n`, `y n → x`, `r n → 1`, and
  > `sampleCode c hc (y n) (r n) → b`.

  So a trace at `x` is a **radius-one cluster** of the colouring, sampled on
  circles whose centres tend to `x` and whose radii tend to `1`. This is the
  only structural input of everything below.
* `tracePositive c hc x i b = {t | 0 < traceValue b i t}` (a genuine subset of
  `Angles`, measurable). It depends on `c` **only through the subtype**
  `Traces c hc x`: the set is defined from the `Lp` element `b.1 i` alone.
* `paletteSet c hc x i = ⋃ b ∈ paletteGenerators c hc x i, tracePositive c hc x i b`,
  where the generator set is produced by `Classical.choose` from
  `exists_countable_essential_union`. **Its two universal properties** are what a
  proof must use (the chosen generators are meaningless otherwise):

  * (P1) `tracePositive c hc x i b ≤ᵐ paletteSet c hc x i` for every `b`
    (`tracePositive_le_palette`);
  * (P2) if `A` is measurable and `tracePositive c hc x i b ≤ᵐ A` for **all** `b`,
    then `paletteSet c hc x i ≤ᵐ A` (`paletteSet_minimal`).
* `palette c hc x t = Finset.univ.filter (fun i => t ∈ paletteSet c hc x i)`,
  `mem_palette : i ∈ palette c hc x t ↔ t ∈ paletteSet c hc x i`.
  "For a.e. direction `e`: `P_x(e) = P'_x(e)`" is the statement
  `palette c hc x =ᵐ[angularMeasure] palette c' hc' x`.

Throughout, `c, c' : ℂ → Fin k` are **measurable only** (§2–§4 use nothing else).

---

## 2. The engine: a locality principle for the radius-one palette

**Theorem 1 (locality).** Let `c, c' : ℂ → Fin k` be measurable, `Z ⊆ ℂ` **open**
with `c = c'` on `Z`, and `x ∈ ℂ`. Suppose

> (★) for every `y n → x`, `r n → 1` there is `N` with, for all `n ≥ N`,
> `{y n + r n · direction t : t ∈ Angles} ⊆ Z`.

Then for every `b : TraceVector k`, `IsTrace c hc x b ↔ IsTrace c' hc' x b`.

*Proof.* (`⇒`; `⇐` is the same with `c, c'` exchanged.)

1. Choose `y, r, b` with `TypicalSampling c (y n) (r n)`, `y n → x`, `r n → 1`,
   `sampleCode c hc (y n) (r n) → b` (`trace_realization`).
2. **Sample equality.** Fix `n ≥ N`. For every `t`, the point
   `z := y n + r n · direction t` lies in `Z` (★), so `c z = c' z`; hence
   `sampleFn c (y n) (r n) i t = sampleFn c' (y n) (r n) i t` for **all** `t` —
   a pointwise identity, not just a.e. Therefore
   `sample c hc (y n) (r n) i = sample c' hc' (y n) (r n) i` as `Lp` elements
   (`Lp.ext`), and `sampleCode c hc (y n) (r n) = sampleCode c' hc' (y n) (r n)`.
   In particular the `c'`-sample codes still converge to `b`.
3. **Typical-sampling transfer.** Fix `n ≥ N`. For *every* `t` the point
   `z := y n + r n · direction t` lies in the open set `Z`, so choose `ρ = ρ(t) > 0`
   with `B(z,ρ) ⊆ Z` (no uniformity in `t` is needed). Then `c = c'` on `B(z,ρ)`
   and `c' z = c z`, so the two colour classes agree on `B(z,ρ)`:
   `{w | c w = c z} ∩ B(z,ρ) = {w | c' w = c' z} ∩ B(z,ρ)`. `DensityOne` at `z`
   is a limit of ball ratios as the radius tends to `0`, hence only sees an
   arbitrarily small ball around `z`, so `Typical c z ↔ Typical c' z`. As this
   equivalence holds **for every `t`** (not merely a.e.), the two a.e. statements
   have the same exceptional set: `∀ᵐ t, Typical c' (y n + r n · direction t)`
   follows from the `c`-version. Together with `0 < r n`:
   `TypicalSampling c' (y n) (r n)`.
4. By `trace_of_realization` with the tail `n ≥ N`: `IsTrace c' hc' x b`. ∎

Two features of the proof matter for §5: (i) step 2 needs the circle **inside**
the region of agreement; (ii) step 3 needs **uniform positive distance** from the
boundary of `Z` along the whole circle, which is what openness plus (★) supply.

**Theorem 2 (palette equality from trace equality).** Let `c, c', x` satisfy the
hypothesis of Theorem 1 with `IsTrace c hc x b ↔ IsTrace c' hc' x b` for all `b`.
Then for every `i : Fin k`, `paletteSet c hc x i =ᵐ paletteSet c' hc' x i`, and
hence `palette c hc x =ᵐ palette c' hc' x`.

*Proof.* `tracePositive c hc x i b = {t | 0 < traceValue b i t} = tracePositive c' hc' x i ⟨b, ·⟩`
(strictly equal sets: same `Lp` element, and `IsTrace c' x b` is available).
So `{tracePositive c hc x i b} = {tracePositive c' hc' x i b'}` as families.
By (P1) for `c'` and (P2) for `c`, `paletteSet c hc x i ≤ᵐ paletteSet c' hc' x i`;
symmetrically the reverse. `angularMeasure` is finite, so `≤ᵐ` both ways gives
`=ᵐ`. Finally `palette` is a `Finset.filter` over the finite index type `Fin k`,
so `ae_all_iff` over `Fin k` turns the `k`-fold a.e. equality into an a.e.
equality of the palettes (`mem_palette` rewrites membership). ∎

> Note the shape of the argument: the palette is determined by the *family*
> `{tracePositive b}`, not by the choice-produced generators; that is why (P1)+(P2)
> both appear. A proof that only unfolds `paletteSet` as a union of one chosen
> generating set cannot conclude anything about `c'`.

---

## 3. Corollaries: what is true, and with what constant

**Corollary 3 (one-sided; this is lemma (D)).** Let `x_0 ∈ ℂ`, `R < 1`, and
suppose `c = c'` on `{z : |z - x_0| > R}` (the closed annulus complement
`{|z - x_0| ≥ R}` is more than enough; `R = 1 - eps` recovers (D) verbatim).
Then for every `x` with `|x - x_0| < 1 - R`, `IsTrace c x · = IsTrace c' x ·`
and `palette c hc x =ᵐ palette c' hc' x`.

*Proof.* `Z := {|z - x_0| > R}` is open and `c = c'` on it. For any `y n → x`,
`r n → 1` and any `u` with `|u| = 1`:
`|y n + r n u - x_0| ≥ r n - |y n - x_0| ≥ r n - |y n - x| - |x - x_0| → 1 - |x - x_0| > R`,
so `y n + r n u ∈ Z` for all `n` large, uniformly in `u`. Apply Theorems 1, 2. ∎

In the special case `x = x_0` this is exactly the task's suggested proof, and it
is correct as it stands **provided** one also (a) transfers `Typical`/density
points, (b) goes through (P1)+(P2) for the essential union. Slack: `eps = 1 - R`
works for every `eps > 0`; **no dependence on `k`**, no properness, no
hypothesis on `c` inside `B(x_0,1-eps)` at all, and the agreement may be assumed
on the *open* set `{|z-x_0| > R}` (so a difference exactly on the sphere
`{|z - x_0| = R}` is invisible — those circles are disjoint from the trace
circles, which have radius `> R` eventually).

**Corollary 4 (two-sided, the exact "germ at the sphere" form).** Let `δ > 0`
and suppose `c = c'` on the open annulus `{z : 1-δ < |z - x_0| < 1+δ}`. Then for
every `x` with `|x - x_0| < δ/2`, `IsTrace c x · = IsTrace c' x ·` and the
palettes at `x` agree a.e. In particular the palette at `x_0` is a function of
the **germ of `c` at the sphere `S(x_0,1) = {|z - x_0| = 1}`** only: colourings
that agree on some annulus around that sphere, however thin, have the same
palette at `x_0`, and colourings may differ freely both deep inside and far
outside.

*Proof.* Same as Corollary 3 with `Z` the annulus: for `n` large
`|y n + r n u - x_0| ≤ r n + |y n - x| + |x - x_0| < 1+δ` and
`≥ r n - |y n - x| - |x - x_0| > 1-δ`, uniformly in `u`. ∎

So (D) is a special case of a *sphere-germ* statement; the "far-field" name is
about the radius `1`, and the object it decouples from is everything at distance
`≥ 1` from `x_0` — the near field at `x_0` is *not* decoupled (see §5.3).

---

## 4. REFUTATION at `eps = 0` (i.e. at `R = 1`): the threshold is not attained

Two counterexamples. Both have `k = 2`, colours `0` and `1`, `x_0 = 0`,
measurable colourings (open discs/annuli are measurable), and both agree with
the comparison colouring on the **closed** set `{|z| ≥ 1}`, yet the palettes at
`0` differ on a set of directions of **full** angular measure.

### 4.1 Counterexample 1 (`R = 1`, difference = the whole open disc)

`c_1(z) := 0` if `|z| < 1`, `c_1(z) := 1` if `|z| ≥ 1`;  `c'_1 ≡ 1`.
Then `c_1 = c'_1` exactly on `{|z| ≥ 1}` — the hypothesis of (D) with `eps = 0`.
Claim: for `μ`-a.e. `t`, `palette c_1 h 0 t = {0,1}` while `palette c'_1 h' 0 t = {1}`.

*(i) Colour `0` is in `P^{c_1}_0`.* Let `r n := 1 - 1/(n+2) ∈ (0,1)`, `y n := 0`.
For every `t`, `|0 + r n · direction t| = r n < 1`, so `c_1(…) = 0` and
`sampleFn c_1 0 r n 0 ≡ 1`, `sampleFn c_1 0 r n 1 ≡ 0`. Also
`TypicalSampling c_1 0 r n`: `0 < r n`, and for every `t` the point
`r n · direction t` is an **interior** point of the open disc `{|w| < 1}`, hence a
density point of `{w | c_1 w = 0}` (density `= 1` on a neighbourhood).
The sample code is then *constant* in `n`, so it converges, and
`trace_of_realization` gives a trace `b` with `traceValue b ⟨0,_⟩ = oneL2`.
Hence `{t | 0 < traceValue b ⟨0,_⟩ t} =ᵐ Set.univ`, and by (P1)
`paletteSet c_1 h 0 0 =ᵐ Set.univ`.

*(ii) Colour `1` is in `P^{c_1}_0`.* Same with `r n := 1 + 1/(n+1) > 1`; the circle
`{|z| = r n}` lies in the interior of `{|z| ≥ 1}`, giving a trace `b'` with
`traceValue b' ⟨1,_⟩ = oneL2`, so `paletteSet c_1 h 0 1 =ᵐ Set.univ`.

Since `palette` is a `Finset` of `Fin 2`, (i)+(ii) give `palette c_1 h 0 t = {0,1}`
for a.e. `t`.

*(iii) `P^{c'_1}_0 = {1}`.* For `c'_1 ≡ 1` we have `sampleFn c'_1 y r ⟨1,_⟩ ≡ 1`,
`sampleFn c'_1 y r ⟨0,_⟩ ≡ 0` for **every** `y` and every `r`. So every sample
code equals `b* := (0, oneL2)`, every `IsTrace` vector at `0` is `b*`
(`trace_realization` + uniqueness of limits), `traceValue b* ⟨0,_⟩ = 0`, hence
`tracePositive c'_1 h' 0 0 b = ∅` for all `b` and, by (P2) with `A = ∅`,
`paletteSet c'_1 h' 0 0 =ᵐ ∅`. (Similarly `paletteSet c'_1 h' 0 1 =ᵐ Set.univ`, so
`palette c'_1 h' 0 t = {1}` a.e.)

Hence `palette c_1 h 0 ≠ᵐ palette c'_1 h' 0`: `0 ∈ P^{c_1}_0(e)` and
`0 ∉ P^{c'_1}_0(e)` for a.e. `e`. **Lemma (D) with `eps = 0` is false, and
maximally so** (full-measure direction set), with `k = 2`.

### 4.2 Counterexample 2: an arbitrarily thin annulus inside the unit disc

Fix any `δ ∈ (0,1)`. Put
`c_δ(z) := 0` if `1-δ < |z| < 1`, `c_δ(z) := 1` otherwise;  `c'_δ ≡ 1`.
Then `c_δ = c'_δ` on `{|z| ≥ 1}` **and** on `{|z| ≤ 1-δ}`; they differ only in the
open annulus `{1-δ < |z| < 1}`, which is at distance `δ` from the sphere and lies
strictly inside the open unit ball. Yet the palettes at `0` differ:

* with `y n = 0`, `r n = 1 - 1/(n+2)` (any `n` with `r n > 1-δ`), the whole circle
  `{|z| = r n}` lies in the open annulus, is thus coloured `0` pointwise, and
  consists of interior points of the colour-`0` set, so `TypicalSampling c_δ 0 r n`
  holds and the constant trace has colour-`0` value `oneL2`: `0 ∈ P^{c_δ}_0(e)`
  for a.e. `e`;
* with `r n = 1 + 1/(n+1)` the circle lies in `{|z| > 1}`, giving `1 ∈ P^{c_δ}_0(e)`;
* `P^{c'_δ}_0 = {1}` as in 4.1(iii), so `0 ∉ P^{c'_δ}_0(e)` for every `e`.

So for **every** `δ > 0` there are colourings agreeing off `B(0,1)` and off
`B(0,1-δ)` whose palettes at `0` differ on a full-measure direction set.

Consequently the number `1` is a genuine **threshold**: every `R < 1` works
(Corollary 3) and `R = 1` fails (4.1), for all `k ≥ 2` (no `k`-dependence),
with the *smallest possible* colour set.

### 4.3 What the counterexamples force (necessary condition)

**Corollary 5.** Suppose `c = c'` on `{|z - x_0| ≥ 1}`, `D := {c ≠ c'} ⊆ B(x_0,1)`,
and `palette c h x_0 ≠ᵐ palette c' h' x_0`. Then for **every** `δ > 0` there is
`z ∈ D` with `|z - x_0| > 1 - δ`; i.e. `D` accumulates on the sphere
`S(x_0,1)`. So a recolouring confined to a ball of radius `ρ` about `x_0` can move
the palette at `x_0` only if `ρ > 1` (for `ρ < 1` Corollary 3 forbids it), and for
`ρ = 1` only if the recoloured set still reaches the sphere.

*Proof.* Contrapositive of Corollary 3 with `R = 1-δ`: if `D ⊆ B(x_0,1-δ)` then
`c = c'` on `{|z-x_0| > 1-δ}`, so the palettes at `x_0` agree, contradicting the
hypothesis. Hence for every `δ > 0`, `D ⊄ B(x_0,1-δ)`. ∎

(Compare task (4): a gadget of diameter `< 1` — i.e. contained in a ball of radius
`< 1` — leaves the palette at its centre equal to the background palette. That is
Corollary 3, and it is exactly the mechanism the `k ≥ 7` construction needs. The
exact `Fraction` audit of `W = p_0 + [-1/200,1/200]^2` is carried out separately
in direction d1; my Corollary 3 is the statement it applies.)

---

## 5. Exact scope of the negative result

### 5.1 Proved here (no gaps claimed)

1. Theorem 1 (locality), Theorem 2 (essential-union stage), Corollary 3
   (= (D), `R < 1`, sharp statement), Corollary 4 (sphere-germ form),
   Corollary 5 (necessity of accumulation at the sphere).
2. Refutation of (D) at `eps = 0`: two explicit measurable colourings, `k = 2`,
   palettes differing on a full-measure set of directions (§4).
3. The quantitative arc computations of §6 (exact closed form, plus sampler).

These are proofs at the level of the repo's definitions; the Lean formalisation
itself is **not** carried out here (the necessary lemmas are named at each step:
`trace_realization`, `trace_of_realization`, `Lp.ext`, `tracePositive_le_palette`,
`paletteSet_minimal`, `ae_all_iff`, `mem_palette`). Where the proof uses "an
interior point of an open set is a density point of it", the Lean step needed is
`DensityOne` of an open set at its own point (immediate from the ball ratio `≡ 1`
near an interior point).

### 5.2 NOT claimed (open, and honestly open)

* **`eps = 0` for *proper* colourings.** Both counterexamples are non-proper
  (`c_1` and `c_δ` are not proper colourings of the plane; triviality of the
  palette of `c'_1 ≡ 1` also uses a constant colouring). Whether two **proper**
  colourings agreeing off `B(x_0,1)` can have different palettes at `x_0` is
  *not* settled here. What is settled is that the obvious attempts fail: by
  Corollary 5 any such pair must differ in a set accumulating on `S(x_0,1)`, and
  recolouring an open region reaching the sphere with a single colour destroys
  properness on the chords of length `1` inside the region (the centre `x_0` and
  every point of `S(x_0,1)` are at distance exactly `1`, and so are many pairs
  inside any open region touching the sphere), so the recolouring must be a
  genuinely proper colouring of a region that touches the sphere. This looks like
  the same rigidity that the paper's transition theory is about; it is not
  disposed of by the argument in §4.
* Nothing about `chi(ℝ^2)`, nothing about the truth of the paper's main theorem.
* Nothing about `Γ_x`/`TransitionEdge` beyond the contrast in §5.3.

### 5.3 What a correct proof of (D) **must** use (and what the failure at `R = 1` shows)

1. **The radius-one cluster structure.** `IsTrace x b` forces `y n → x` **and**
   `r n → 1` (`trace_realization`). This is the whole game: the sample points
   satisfy `||y n + r n u - x_0| - 1| ≤ |y n - x_0| + |r n - 1| → 0`, i.e. they
   lie in a shrinking annulus around `S(x_0,1)`. A near-field object
   (`TransitionEdge c i j x`, `Transitions.lean`: volume ratio in `ball(x,R)` for
   **all** `R > 0` and `h → 0`) has no such shrinking annulus and therefore
   **does not** decouple: modifying `c` anywhere in a ball `B(x_0,ρ)` around
   `x_0`, `ρ > 0`, changes the volume ratio for `R > ρ`, so no analogue of (D)
   with a positive threshold can hold for `Γ_x`. The far-field decoupling is a
   property of the *radius-one* cluster trace, not of the colouring's local
   structure.
2. **A uniform-in-`n`, uniform-in-`u` margin.** One needs
   `inf_n inf_{|u|=1} dist(y n + r n u, Z^c) > 0`; this is the strict inequality
   `r n - |y n - x_0| > R`, which is exactly `R < 1`. At `R = 1` the margin tends
   to `0` and §4 exhibits colourings that exploit precisely that.
3. **Openness of the agreement set around the sample points**, used *twice*:
   for the pointwise identity of `sampleFn` (§2 step 2) and — this is the step
   that is easy to miss — for the **`Typical`/density-point transfer**
   (§2 step 3). `Typical` is not a point-measurable property: it asks for a
   density-one statement in a *neighbourhood*, so equality of `c` and `c'` at the
   sample point is not enough; one needs `c = c'` on a ball around it, which is
   why the hypothesis must be "agreement on a set containing a neighbourhood of
   the *entire* trace circles", and why agreement on `{|z - x_0| ≥ 1-eps}` works
   with `eps>0` (the sample points are at distance `> 1-eps`, strictly) but
   agreement on `{|z - x_0| ≥ 1}` does not (the sample points approach the
   sphere from inside).
4. **The two-sided universal property of the essential union** (P1)+(P2): the
   generators are `Classical.choose`d, so `paletteSet` must be shown to be a
   function of the *family* `{tracePositive b}`; and the family is preserved
   because `tracePositive` depends on `c` only through the subtype
   `Traces c hc x`, i.e. only through `IsTrace`. A proof that ignores this and
   compares unions generator-by-generator proves nothing (the generator sets may
   be different countable subsets of the same family).
5. **Measurability only.** No properness, no weak-colouring hypothesis, no bound
   on `k`, and no interaction with the paper's transition theory. `eps` does not
   depend on `k`.

---

## 6. Numeric / exact-arc audit

Files: `farfield_check.py` (script), `farfield_check.out` (its full output).

Method. For a centre `y` with `|y| = ρ` and radius `r`, the colour-`0` angular
fraction on the circle `C(y,r)` is computed **in closed form**: with
`z = y + r e^{it}`, `|z|² = ρ² + r² + 2ρr cos(t - arg y)`, so
`{t : |z| < a}` has angular measure `0`, full, or `2(π - arccos κ)` where
`κ = (a² - ρ² - r²)/(2ρr)` — with the branch decision made in `Fraction`
arithmetic and only `arccos` evaluated in `double`. The closed form is
cross-checked against brute-force sampling at `N = 2^19` angles (agreement
`≤ 1.9e-6 = O(1/N)`, rows in §5 of the output).

Results (all from `farfield_check.out`):

* **§0 circle geometry**: `ρ < eps/2`, `r > 1 - eps/2` give
  `r - ρ > 1 - eps` (checked exactly for `eps = 1/10, 1/100, 1/1000`). This is the
  uniform margin of §5.3(2).
* **§1–§2 Counterexample 1**: colour-`0` fraction is `1.000000` on every circle of
  radius `r < 1` about the origin, `0` for `r > 1` (so `c_1`'s palette is `{0,1}`
  and `c'_1`'s is `{1}`); the grid over `ρ ∈ {0, 1e-6, 1e-3}` × `r ∈ [1-1e-3, 1+1e-3]`
  shows the same, plus the genuine `≈ 1/2` mixing when the circle straddles `|z| = 1`
  (e.g. `ρ = 1e-3`, `r = 1` → `0.499841`).
* **§3 Counterexample 2** (`δ = 1/100`): colour-`0` fraction `1.000000` for
  `r ∈ (1-δ, 1)` with `ρ` small, and `0` outside, confirming that the thin
  annulus is fully visible to the trace but invisible to every ball of radius `< 1`.
* **§4 Control (positive side)**: for the pair `c_δ = 0` on `{|z| < 1-eps}` vs
  `c'_δ ≡ 1`, which agree exactly on `{|z| ≥ 1-eps}`, the window
  `ρ < eps/2`, `r > 1-eps/2` gives `min |z| = r-ρ > 1-eps` and colour-`0`
  fraction identically `0`: both window-palettes are `{1}`. The theorem's window
  is exactly the window in which the trace circles cannot see the difference.

Caveat on the numbers: the closed form is exact in exact real arithmetic; the
printed decimals are `double` (`~1e-16` relative) and the sampler agrees to
`O(1/N)`. Two rows where `ρ ~ 1e-6` and `r` is `1 ± 1e-6` are decided by `κ`
computed in `double`; the exact branch decision there is `full`/`empty` and was
verified with `Fraction` arithmetic in §0. (During the audit the sign of the
`κ ≥ 1` branch was initially wrong — `κ ≥ 1` means *full*, not *empty*; fixed,
and the fixed version is what §1–§4 report. The brute-force sampler is what
caught it, which is why it is kept in the script.)

---

## 7. Files

| file | content |
|---|---|
| `sharpness.md` | this document: statements, proofs, refutation, scope |
| `farfield_check.py` | exact-arc + sampler audit of the counterexamples and of the control window |
| `farfield_check.out` | its complete output (reproduce with `python3 farfield_check.py`) |
