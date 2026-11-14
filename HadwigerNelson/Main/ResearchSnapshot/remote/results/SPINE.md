# The proof of `chi(R^2) >= 6` in twelve steps

This is a reader's spine of the OpenAI paper *The Euclidean plane is not five-colorable*
(23 Sep 2026, 62 pp.), checked line by line against the Lean development in `lean/OAI`.
It is not a replacement for the paper: each step names the paper's own numbered statement and
the Lean module that machine-checks it. Its purpose is to show where the weight of the proof
actually sits, and that the architecture is forced.

**Notation.** `E = algebraicClosure(Q, C)` is the algebraic plane, `F = E ∩ R`, `K = {u ∈ E :
|u| = 1}` the algebraic unit circle (a divisible group), `D` the Pontryagin dual of the discrete
additive group `E`, and `C ⊂ D` the subgroup of ordinary continuous characters `j(xi)(z) =
exp(i xi·z)`, `xi ∈ R^2`. `K` acts on `D` by `(u d)(z) = d(u z)`.

---

## Part I. From an arbitrary colouring to a measurable one

### Step 1 (Section 2.1). The rigidity theorem.
**Theorem 2.3.** Every `K`-invariant Borel probability `nu` on `D` with `nu(C) = 0` is Haar
measure.

This is the only genuinely new *analytical* input of the whole paper; everything else in Part I
is soft. Its proof occupies Sections 2.2–2.4 and 3 and has five ingredients:

* **1a. Cosets are null (Lemma 2.4).** If `nu(d + C) > 0`, the `K`-orbit of the coset `d + C` is
  finite, because `K` is divisible and a finite image of a divisible group is trivial; so every
  `u ∈ K` fixes the coset, giving `(u − 1)d ∈ C`, hence `d ∈ C`. Contradiction.
  `[Lean: PlaneSpectrum/Basic.lean, wild_coset_null, wild_independent_difference]`

* **1b. Line averages vanish (Lemma 2.5).** For `a ≠ 0`, the set of characters whose restriction
  to the line `aF` is continuous is `nu`-null, and the invariant mean `I` over `F/Z` annihilates
  `phi(t) f_nu(a t)`. The point of using an invariant mean rather than a Følner average is that
  `f_nu` restricted to `F` is *not assumed measurable*; `I` is defined on all bounded functions
  because `F/Z` is discrete.
  `[Lean: PlaneSpectrum/InvariantMean.lean; MeasureTheory/CompactFactors/Amenability.lean]`

* **1c. Relative singularity (Lemma 2.7).** For an ergodic `K`-system `X → D` with wild law,
  and any factor `Y` in a compact (Furstenberg–Zimmer) tower, the law of `d(x) − d(x')` for two
  conditionally independent samples over `Y` is still wild. The proof is a transfinite induction
  along the tower with a finite-list/phase-collision argument; the tower is countable because
  `L^2` is separable.
  `[Lean: MeasureTheory/CompactFactors/* (19 modules) and PlaneSpectrum/ConditionalSpectrum,
  PhaseEncoding, PhaseCollision]`

* **1d. The radial inequality (Lemma 3.3).** With `P = E[· | Y]`, `g_z = P psi_z` and
  `m(z) = ||g_z||^2`, the function `m` is radial, `w = −log m` satisfies
  `w(|A − B|) <= w(A) + w(B)`, and every Følner average of `m(2r|Re u|)` tends to `m(r)^2`.
  This is where the conditional multiple average theorem (Lemma 3.2) is used: the algebraic
  identity `|A − B u^2|^2 = |−L + (A−B)u + L u^2|^2` turns a two-term correlation into a
  three-term one, and the two projections give `m(A)m(B) <= m(|A−B|)`.
  `[Lean: PlaneSpectrum/RadialEnergy.lean, Energy.lean, Representations.lean]`

* **1e. The number-field argument (Lemmas 3.4, 3.5).** If `m(r) > 0` at one positive `r ∈ F`,
  the difference inequality propagates it: general-position rotations `u(t) = (1+it)/(1−it)` give
  `Q`-bases of a number field among the rotations, and addition under a cap turns an integer
  relation `D_0 = sum a_k k` into `m(s) >= e^{−4 M_0 H} > 0` on a whole interval `(0, 2 r c_0)`.
  That contradicts 1b. So `m` vanishes off `0`, all Fourier coefficients vanish, and `nu` is Haar.
  `[Lean: PlaneSpectrum/NumberFields.lean; MeasureTheory/CompactFactors/Approximation.lean]`

The ergodic decomposition at the end of Section 3 is the standard reduction from a `K`-invariant
to an ergodic `K`-invariant measure; `C` is invariant, so wildness passes to almost every
component. `[Lean: PlaneSpectrum/Ergodicity.lean]`

### Step 2 (Proposition 4.2). A proper colouring of `E` produces a measurable one of the plane.
Given a proper `k`-colouring of `E`:

* `Omega = {proper k-labellings of E}` is closed in the compact space `{1..k}^E`, and the
  countable amenable group `E ⋊ K` acts on it; averaging a point mass along a Følner sequence
  gives an invariant probability `mu` (Proposition 4.2, first paragraph).
* `f_i` = indicator that the origin has label `i`; properness gives `∫ f_i T_u f_i dmu = 0` for
  every `u ∈ K`.
* Split `f_i = p_i + b_i` with `p_i = E[f_i | F_c]`, the conditional expectation onto the
  "continuous factor" of Lemma 4.1. Then `0 ≤ p_i`, `sum p_i = 1`, and `p_i` is rotation-fixed.
  Lemma 4.1 identifies `F_c` as the spectral subspace on `C`; the spectral measure of `b_i` is
  `K`-invariant and gives `C` measure zero, so Step 1 makes it Haar, hence
  `⟨b_i, T_z b_i⟩ = 0` for all `z ≠ 0`.
* Therefore `∫ p_i T_u p_i dmu = 0` for every unit `u`, hence for every `x ∈ R^2`,
  `⟨T_x p_i, T_{x+u} p_i⟩ = 0`.
* The map `x ↦ T_x p_i` is continuous into `L^2(mu)`; choosing finitely-valued approximations
  with summable squared errors gives *jointly measurable* fields `H_i(x, omega)`, non-negative,
  summing to one, with `H_i(x,omega) H_i(x+u,omega) = 0` for almost every `(x,u)`. Fubini then
  gives one sample `omega` for which the colouring `x ↦` least `i` with `H_i(x,omega) > 0` is
  measurable and weak (Definition 1.2).
  `[Lean: PlaneColoring/BorelTransfer.lean, proper_to_borel_weak_algebraic]`

**This step is where the theorem is stronger than the paper states it:** the hypothesis is a
proper colouring of `E`, not of `C`. See `results/T1-algebraic-plane.md`.

### Step 3 (Lemma 4.3 and the end of Section 4). The converse.
In a weak measurable colouring, the full-density-point set of each colour class contains no unit
pair (density points of a class, hit by a small random translate of the unit circle, would give a
monochromatic unit pair of positive product measure). These sets are conull, disjoint and
partition the plane off a null set. Every finite configuration can be translated into a conull set
(intersection of finitely many conull sets), so every finite unit-distance graph is `k`-colourable;
Tychonoff compactness in `{1..k}^{R^2}` then gives a proper colouring of the plane.
`[Lean: PlaneColoring/WeakColoring.lean, weak_density_proper, ae_density_actual]`

**Step 4.** Theorem 1.3: for every `k`, *E is k-colourable ⇔ C is k-colourable ⇔ C has a weak
measurable k-colouring*. In particular `chi(E) = chi(C)`.

---

## Part II. No weak measurable five-colouring (Sections 5–8)

Now fix a weak measurable 5-colouring, with Borel representatives `A_i`, `a_i = 1_{A_i}`, and
essential supports `H_i`. Write `R` for rotation by `pi/3`, `J` for rotation by `pi/2`.

### Step 5 (Section 5.1–5.2). Palettes.
For a centre `x` and direction `e`, the *maximal palette* `P_x(e) ⊂ {1..5}` is the set of labels
that occur with positive angular weight in weak-* limits of circle samples at centres tending to
`x` and radii tending to `1` (Definition 5.1). The key transfer lemma (5.2) says that for
`sigma ⊗ sigma`-almost every `(e,v)`, the point `x + e + v` has a colour outside
`P_x(e) ∪ P_x(v)`; Corollary 5.4 specialises this to `P_x(f) ∩ P_x(Rf) = ∅`.
`[Lean: PlaneColoring/Palettes.lean, PaletteTransport.lean]`

### Step 6 (Proposition 5.6). Palettes have at most two labels.
If a triple `A` lay in `P_x(e)` on a set of positive angular measure, the exact circle at `x + e`
would be coloured by the complementary pair `{1..5} \\ A`; those centres would be "binary", and
Lemma 5.5 (binary-centre separation: a uniform `delta_* > 0` between centres whose palettes meet a
fixed pair) would make a uniformly separated subset of a compact circle infinite — impossible.
`[Lean: PlaneColoring/PaletteDensity.lean, PaletteTransport.lean, Rigidity.lean]`

### Step 7 (Section 6). Transition graphs and local finiteness.
The transition graph `Gamma_x` on the five labels has an edge `ij` when some palette at `x`
contains both `i` and `j`. Lemma 6.2 produces, at every transition, a circle trace avoiding both
labels; Lemmas 6.3, 6.4 and 6.7 convert this into strict state separation and ban angular steps.
Theorem 6.5: the set of centres whose transition graph contains a cycle is closed and locally
finite.
`[Lean: PlaneColoring/Transitions.lean, States.lean, BinaryPalettes.lean, CyclicCore.lean]`

### Step 8 (Section 7.1–7.2, Proposition 7.1). Common exclusion continua.
Disk averages of the colour indicators, thresholded and renormalised, give continuous
graph-valued maps into the geometric realisation of `K_5`. At a cyclic centre, a non-null core
loop (Lemmas 7.3–7.6) produces a simple cycle `j ↦ (j, j+1)` of labels and compact connected sets
`K_j` through a common point `x` such that both endpoint labels of edge `j` are absent almost
everywhere from the open region `Delta(K_j) = {z : min_{q ∈ K_j} |z−q| < 1 < max_{q ∈ K_j} |z−q|}`.
The topological input is Lemma 7.5: a closed square of side ten has no relatively open cover of
multiplicity at most two and mesh at most two (proved by a partition of unity, a Brouwer fixed
point, and the fact that a finite union of segments has empty interior in the plane), together
with Lemma 7.7 (every nontrivial free homotopy class in a graph meets the midpoint of some edge of
its reduced word).
`[Lean: PlaneColoring/PlanarCovers.lean, DiskAverages.lean, Mesh.lean, GraphCuts.lean,
HoleApproximation.lean, ContinuumLimits.lean, FullApproximation.lean]`

### Step 9 (Section 8.1). One-sided strip restrictions.
For `e` not perpendicular to any limiting direction `v_j`, give edge `j` the sign of `e · v_j`.
Then an outer strip just outside radius one uses only labels in `O(e)`, the set left after deleting
the endpoints of all positive edges, and an inner strip only labels in `I(e)` from the negative
edges. Both are non-empty, and the palette at `e` meets both (Lemma 8.1).
`[Lean: PlaneColoring/AngularBoundary.lean, BoundaryTrace.lean]`

### Step 10 (Section 8.2–8.6). No cycle of length 3, 4 or 5.
* **Length 5** (Proposition 8.2): the five signs must split into one positive and one negative run,
  of lengths two and three; the allowed sets are the internal vertices, of sizes one and two; the
  palette bound forces every palette to be a pair meeting both, and the six positions of the
  `R`-orbit force six equal sign steps, which do not close modulo five.
* **Length 4** (Proposition 8.5, Lemmas 8.3, 8.6): a six-position word on four labels plus an
  outsider is impossible; the two diagonals `{0,2}`, `{1,3}` give a parity rule that antipodal
  directions violate.
* **Length 3** (Proposition 8.10, Lemma 8.8): the two outside labels alternate through six sectors;
  the open three-label region (8.4) then contains a placed copy of the seven-vertex Moser spindle,
  which is not 3-colourable.
  `[Lean: PlaneColoring/Exclusion.lean, FourContinuity.lean, FourTransport.lean, Accumulation.lean,
  FiveSupport.lean, Sectors.lean, Moser.lean]`

### Step 11. Contradiction.
Proposition 7.1 supplies a simple cycle of length between 3 and 5; Steps 10 exclude all three
lengths. Hence no weak measurable 5-colouring exists (Theorem 1.4), and by Step 4 no proper
5-colouring exists (Theorem 1.1).

---

## Where the weight sits

| Part | Paper | Lean modules | What it costs |
|---|---|---|---|
| Rigidity (Step 1) | §2.2–§3.5, ~22 pp. | `PlaneSpectrum/*` (18), `CompactFactors/*` (19) | Furstenberg–Zimmer tower, conditional multiple averages, number-field addition |
| Transfer (Steps 2–4) | §4, ~6 pp. | `BorelTransfer`, `WeakColoring` | spectral projection onto the continuous factor; measurable selection |
| Palette geometry (Steps 5–7) | §5–§6, ~16 pp. | `Palettes`–`States`–`CyclicCore` (14) | density-point estimates on circles, transition states |
| Continua and cover (Step 8) | §7, ~13 pp. | `PlanarCovers`–`FullApproximation` (10) | disk averaging, planar cover obstruction, homotopy of graph words |
| Cycle exclusions (Steps 9–11) | §8, ~11 pp. | `Exclusion`–`Sectors` (8) | finite angular word combinatorics, Moser certificate |

Reading order for a referee: Step 1e (the number-field argument) and Step 8 (the cover
obstruction) are the two places where a mistake would most easily hide, because both compress a
large amount of geometry into a short inequality. Step 6 is the first place where the number of
labels is used, and it is exactly where any attempt at six colours must fail or be replaced —
see `results/K6-BARRIER.md`.
