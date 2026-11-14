# Proof complexity of the routes to `δ ≤ π/√18` — where a *simpler* proof could come from

Block `K15-REVIEW-0308-M-CONTINUE`, continuing `K15-C071` after the repairs. This is not a
survey: it lists only objects whose numbers the ledger has re-derived, and it is written
because the person's goal is a **simpler** proof, so the cost of each route is the object of
study, not an afterthought.

## 1. The ladder, with the gap to the truth

Truth: `π/√18 = 0.740480489693`.

| object | value | gap to truth | what it costs | type |
| --- | --- | --- | --- | --- |
| three-point, **lattices only** (CDS22) | `0.741506` | **`+0.00103`** (`0.14%`) | a finite LP + a positive-definite kernel check | general-position-free but lattice-restricted |
| Hales | `0.740480489693` | 0 | interval arithmetic on `R⁵/R⁶` cells, `≈5×10³` planar maps, `≈10⁵` LPs of `10²`–`2×10³` constraints; equality case **not** computational | complete |
| Hales–McLaughlin | `0.754697399337` | `+0.01422` | one cell inequality (dodecahedron) | pointwise |
| three-point, general (CDS22) | `0.770271` | `+0.02979` | the same LP without the lattice restriction | complete |
| Muder | `0.773055` | `+0.03257` | Barlow/stacked-specific | restricted |
| Rogers simplex | `0.779635570044` | `+0.03916` | a simplex volume | pointwise |
| Cohn–Elkies two-point | `0.779747` | `+0.03927` | one admissible `f` | complete |
| **this project's best certificate** (`K33b`) | `0.779966216777` | `+0.03949` | exact Sturm + rational Gram | complete but **not an improvement** |

Two numbers carry all the information:

1. **The lattice-restricted three-point bound is `0.14%` from the truth.** Nothing else
   non-computational is anywhere near it. So the *only* structural idea currently within
   reach of a short proof is the three-point (pair-correlation) family, and the entire
   remaining gap is the difference between "lattices" and "all packings".
2. **The general three-point bound is `4.0%` from the truth**, i.e. the lattice restriction
   is worth `0.029` of density — more than any improvement this project has produced.

## 1a. The pair route as a cost object (added at review 0438)

`GEOMETRIC_LEMMA_0438.md` introduces a route not in the ladder above, so it is placed here for
comparison. Its content is a **two-cell** inequality, and its payoff is exact:

| route | object | gives | status of the object |
| --- | --- | --- | --- |
| pointwise | `vol Ω(v) ≥ V_dod` | `0.754697399337` | **proved**, and **sharp** (attained), so closed |
| pair, trivial constant | `vol Ω(v)+vol Ω(w) ≥ 2V_dod` | `0.754697399337` | proved (ML twice) — reproduces ML exactly |
| pair, `(L_δ)` | `≥ 2V_dod + δ`, any `δ > 0` | `< 0.754697399337` | **proved non-explicit** (`C108`) |
| pair, sharp `(L)` | `≥ 2√32` | `0.740480489693` | **open** (E's `E074`) |
| three-point, general | an LP optimum | `0.770271` | proved (CDS22) — weaker than ML |
| two-point | one `f` | `0.779747` | proved — and *provably* not sharp (Li) |

Three cost observations that matter more than the numbers.

1. **No sharpness barrier.** The pointwise route is not merely stuck: `V_dod` is *attained*, so
   no pointwise improvement exists. The pair route's floor `2V_dod` is *unattainable* for a
   contact pair, so the interval `[2V_dod, 2√32]` — a `1.92%` window — is entirely usable, and
   every point in it yields a real improvement. This is the only route in the table with that
   property.
2. **The computational content is of a different kind.** Hales needs interval arithmetic on
   `R⁵/R⁶` cells, `≈5×10³` planar maps and `≈10⁵` LPs. The pair route needs (i) one exact finite
   polytope computation per local type (two types, 14 vertices each — `C104` does it in
   ~0.3 s), and (ii) a combinatorial matching statement. **No large computation is in
   prospect**: the local object is two cells, not a decomposition star.
3. **The bridge is where the risk is, not the geometry.** `C106`/`C108` show the local bound is
   converted to a density bound by a counting argument whose failure mode is `ρ = 0` (no
   contacts at all), not a numerical threshold. So the pair route's risk profile is inverted
   relative to the analytic route: its *inequality* is hard and its *bookkeeping* is easy, while
   the two-point LP's inequality is easy and its sharpness impossible.

**The honest comparison to Hales.** The pair route, if `(L)` were proved, would be a genuinely
shorter proof of `δ ≤ π/√18` than Hales' — but it would still rest on a two-cell isoperimetric
inequality that nobody has proved, and E's own best witness (`5.897967` against a required
`5.763417`) shows the margin at the critical pair is only `1.19%`. So it is *promising*, not
*short*.

## 2. The obstruction that decides the analytic route

`K15-C094` (R. Li, Adv. Math. 460 (2024), Thm 6.1): the **plain** Cohn–Elkies LP is **not
sharp in `d = 3`**. So no amount of care with the two-point certificate reaches
`0.740480489693`; the level-2 class is provably insufficient. `K15-C094`'s companion
observation in this project (non-uniqueness, now made concrete by `K15-C095`: *any planar
fault is an equality case*) explains the mechanism — complementary slackness for a sharp `f`
would need `f` to vanish on the shell radii of a **continuum** of extremal packings.

**Consequence for the goal.** The analytic route can only produce a *simpler* proof by
leaving the level-2 class. The three-point class is the next step and its general bound is
`0.770271`, so three-point alone does not close it either; what would is a level-3 object
that is sharp — a well-known open problem, not a computation.

## 3. The geometric route's cost, after this block

`K15-C087`: the cut condition **implies** `δ ≤ π/√18`, and nothing implies it from the
density bound.

> **Correction (`K15-REVIEW-0438-M`).** An earlier version of this section concluded "so the
> transfer route is a reorganisation whose price is the full geometric content", treating the
> implication as a verdict on the route. **That inference is invalid and is withdrawn.** A
> sufficient condition implies its target by definition; that is not circularity and it is not
> a defect. Circularity would require assuming the target — which is what `C094`'s Lemma 1
> actually did, and what `C104` repaired. The correct content of the one-way arrow is narrow:
> the cut form cannot be sold as a **weaker** target than Kepler. Its **cost** relative to
> Hales' proof — how hard it is to verify the cuts — is an open comparison (`C071`, `C100`),
> not something the implication decides.

Three further costs, all established this block:

- **no slack** (`K15-C094`): on every Barlow packing `b ≡ 0`, so *every* cut is tight;
  a proof by a positive margin on a compact class cannot work;
- **the equality case is not classified** (`K15-C095`): continuum many extremal packings,
  so any argument that rests on "the extremiser is fcc/hcp" is unsound;
- **step 0 is open** (`K15-C096`): bounded closed components are not excluded, though the
  singleton case is reduced to `V(2.09) ≥ √32` with a `12%` margin.

None of these says the route is closed — `K15-C036` already says no finite computation can
decide its remaining inequality (`G5`), and that assessment is unchanged.

## 4. What this means for "simpler", in one paragraph

A simpler proof of `δ ≤ π/√18` is not available in this project, and none of the routes
explored here is *known* to be cheaper. The honest statement of the frontier: the only bound
within `0.14%` of the truth is the **lattice** three-point bound, and the plain LP is *proved*
not sharp. The transfer route is at least as strong as the theorem — which, per the
correction in §3, is a statement about its logical strength and not a verdict on its cost. So the realistic outcomes, in
increasing order of difficulty, are (i) a certified improvement over `0.754697399337`
(pointwise cell inequalities — Hales–McLaughlin plus a stability term, `K15-C096`'s `(S)` is
exactly such a term); (ii) a general three-point bound strictly better than `0.770271`;
(iii) a sharp level-3 object. Only (i) is currently well-posed enough to attack with this
project's tools, and `(S)` is the concrete instance of it.

## 5. Not claimed

- No new bound. `0.754697399337` remains the record to beat analytically.
- The `0.741506` and `0.770271` figures are quoted from the retained CDS22 material and are
  **not** re-derived here beyond `constants_check.py`'s coverage; they are used only for
  their *order of magnitude* in the comparison, never in an argument.
- The Hales cost figures are read from his own §25.14 accounting (see `C088`), not measured.

---

# Addendum: `(S)` reduces to "mixed radii do not help"

Follow-up to `K15-C096` in the remaining time of the block. The target `V(2.09) ≥ √32` can
be split at the Tammes threshold, and the split is sharp because **`2.09` is exactly the
radius just below which 13 points stop fitting on a sphere**.

## 1. The split

`13` points on the sphere of radius `ρ` with mutual distance `≥ 2` exist iff
`2 arcsin(1/ρ) ≥ θ₁₃`, where `θ₁₃ = 57.1367°` is the Tammes-13 optimal separation
(Musin–Tarasov; the enclosure this project already relies on for `n(ρ) ≤ 12`, `C027`/`C060`).
Numerically the threshold is

```
ρ ≥ 2.091145548…        (and at ρ = 2.09 the required separation is 57.1709° > 57.1367°)
```

so:

> **At radius exactly `2.09`, every admissible configuration has at most 12 points** — and
> `2.09` is `0.05%` below the radius at which a 13th point would fit. Hales' constant is
> therefore not arbitrary: it is the Tammes-13 threshold, rounded down.

Hence the minimum `V(2.09)` splits into two cases:

- **(A) all points at radius exactly `ρ`, at most 12 of them.** Scaling `x ↦ 2x/ρ` maps the
  cell cut by `{⟨u_i,x⟩ ≤ ρ/2}` to the cell cut by `{⟨u_i,x⟩ ≤ 1}`, i.e. to the `ρ = 2`
  problem for the same directions. By Fejes Tóth's 12-point optimality the icosahedral
  directions maximise the spread, and spread can only *shrink* the cell, so the minimum in
  case (A) is the icosahedral one: `V_dod(ρ/2)³ = 6.333804106` at `ρ = 2.09`, which is
  `1.1197·√32`. **Case (A) is settled in favour of `V(2.09) ≥ √32` by `12%`**, modulo the
  two cited theorems (Tammes-12, and the spread-monotonicity lemma, neither of which this
  project proves).
- **(B) some point at radius `> ρ`.** More than 12 points become available (the shell
  `[2.09, 2.956]` — the part of space that can still cut a cell of circumradius `≤ 1.478` —
  has volume `70.0` and can hold at most `16` two-separated points). Then `(S)` is the
  statement **"mixed radii do not help"**: a point pushed out has a looser half-space
  (`⟨u,x⟩ ≤ r/2` with `r/2 > ρ/2`), so extra points must gain more by their number than
  they lose by their distance.

So `(S)` is *equivalent* to `(B)`, and `(B)` is exactly the case the numerical probe
(`Computation/rho_probe.py`) addresses: from the icosahedral twelve at `ρ`, an extra point
is admissible in one of the 20 hole directions only for radius `≳ 3.2`, where its bisector
at `1.6` lies **outside** the cell's circumradius `1.478`, so it cannot cut. Verified at
`ρ = 2.0127, 2.09, 2.2` for every radius in `[ρ,4]`. Case (B) with *two or more* extra
points, or with a point placed off the hole directions, is **not** searched.

## 2. Two cheap consistency checks this gives

1. **`2.09` is the right constant to attack.** `ρ* = 2.0127` (where the scaled dodecahedron
   reaches `√32`) is *below* `2.09`, and `2.09` is *below* the Tammes-13 threshold `2.0911`.
   So `√32` is crossed in the interior of the admissible window and the window is bounded
   above by a clean geometric quantity — not by an arbitrary decimal. If a 13th point
   *were* allowed, `(B)` would be the whole problem; as it is, `(A)` is already settled at
   `12%` margin.
2. **The trivial bound is nowhere near.** `vol B(0,ρ/2) = 4.78011` at `ρ = 2.09`, and it
   beats `V_dod` only for `ρ > 2.1967`. So for `ρ ∈ [2, 2.1967]` the binding information is
   Hales–McLaughlin and its stability, not the inball — which is why `(S)` has to be a
   stability statement and cannot be replaced by a ball estimate.

## 3. What this changes for `PN-1`

The request to Astra narrows from "decide `V(2.09) ≥ √32`" to **"decide case (B)"**: show
that a 2-separated configuration with all `|c| ≥ 2.09`, at least one `|c| > 2.09`, and at
most 16 points in the relevant shell, has `vol Ω(0) ≥ √32`. That is a bounded,
finite-dimensional optimisation with an explicit admissible set, an explicit target, and an
existing negative probe on its natural configurations — much better posed than the original.
*Acceptance unchanged*: a proof, a certified enclosure, or an explicit counterexample (which
would refute the transfer route and must be reported at once).
