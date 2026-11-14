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
density bound. So the transfer route is a reorganisation whose price is the full geometric
content. Three further costs, all established this block:

- **no slack** (`K15-C094`): on every Barlow packing `b ≡ 0`, so *every* cut is tight;
  a proof by a positive margin on a compact class cannot work;
- **the equality case is not classified** (`K15-C095`): continuum many extremal packings,
  so any argument that rests on "the extremiser is fcc/hcp" is unsound;
- **step 0 is open** (`K15-C096`): bounded closed components are not excluded, though the
  singleton case is reduced to `V(2.09) ≥ √32` with a `12%` margin.

None of these says the route is closed — `K15-C036` already says no finite computation can
decide its remaining inequality (`G5`), and that assessment is unchanged.

## 4. What this means for "simpler", in one paragraph

A simpler proof of `δ ≤ π/√18` is not available in this project and no route explored here
is a shortcut. The honest statement of the frontier: the only bound within `0.14%` of the
truth is the **lattice** three-point bound, the plain LP is *proved* not sharp, and the
transfer route is at least as strong as the theorem. So the realistic outcomes, in
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
