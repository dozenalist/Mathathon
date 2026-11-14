# m6 / d9 (R12) — measured verdicts, a verified −718-line tree, and the R1 obstruction

Three results, all measured on this machine with the pinned toolchain
(`source scripts/env4341.sh`, Lean 4.34.1 + mathlib d13f23b).

| item | result |
|---|---|
| R12 (spectral specialisation, my registered direction) | **dead**, certificate in §3 |
| mechanical trim (R7-style), built and axiom-checked | **−718 lines**, 83/83 modules, no `sorry`, statement byte-identical |
| R1 / R2 / R5 / R6 (the tower restructures) | **ceiling ≈ 900 lines net**, and R1's last step is false as stated (§4, §5) |

Files:

* `trim.patch` — unified diff `lean/OAI → E1/OAI`, deletion-only.
* `per_module.md` — before/after line counts for all 43 changed modules.
* `counts.json`, `removed.json` — the 74 removed declarations, machine-readable.
* `build.py`, `blocks.py`, `check_changed.py`, `deadfinal.py` — the harness (§6).

---

## 1. The delivered tree

`E1/OAI` is a copy of `lean/OAI` with 74 declarations removed (43 modules touched).
Removal criterion, applied to a fixed point: a declaration whose name occurs nowhere
in the tree except its own declaration line, which carries no attribute
(`@[simp]`, `@[measurability]`, … all count as uses), is not an
`instance`/`class`/`structure`/`inductive`, and whose name is not cited in
`README.md`, `docs/` or `results/*.md` (documented results untouched; the external
review bundle under `attachments/` is excluded, being an input artefact).

     31277 lines / 83 modules  ->  30559 lines / 83 modules   (−718)

Verification actually run:

```
source scripts/env4341.sh
JOBS=4 python3 sprint/simplify/m6/build.py sprint/simplify/m6/E1 sprint/simplify/m6/E1build
# 83 modules, 83 to build; built in 1814s; failures=0   (from scratch, empty build dir)
LEAN_PATH="$PWD/sprint/simplify/m6/E1build:$LEAN_PATH" lean sprint/simplify/m6/E1/Check.lean
```

`Check.lean` prints

```
'OAI.EuclideanFiveColor.no_proper_five_coloring' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Problem160.chromaticNumber_bounds' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Problem160.properColoring_seven' depends on axioms: [propext, Classical.choice, Quot.sound]
OAI.EuclideanFiveColor.no_proper_five_coloring : ¬∃ c, OAI.EuclideanFiveColor.ProperColoring 5 c
OAI.Problem160.chromaticNumber_bounds : 6 ≤ OAI.Problem160.planeChromaticNumber ∧ OAI.Problem160.planeChromaticNumber ≤ 7
```

`Geometry/PlaneColoring/Five.lean` is byte-identical to the original. No `sorry`,
`admit`, `native_decide`, `opaque` or `@[implemented_by]` anywhere (grep, 0 hits).
Not built under stock 4.33.1/`/opt/mathlib`: the port patch
`.ultramath/smwfcr56i/m8/patches2/all.patch` applies to the trimmed tree with
offsets, but ~2 hunks in 38 files collide with the trimmed regions, so that
combination needs hunk-level repair that I did not do (`patch -p1 --dry-run` log).

**This is the R7 ceiling:** trimming unmentioned material saturates at ≈720 lines.
1500 cannot be reached this way.

## 2. Where the remaining lines are

| block | lines | note |
|---|---|---|
| `Geometry/PlaneColoring/**` (60 modules) | 15083 | Part II–III (palettes, continua, cycle exclusions) |
| `Analysis/PlaneSpectrum/**` (19 modules) | 8466 | rigidity: cosets, invariant means, radial energy, number fields |
| `MeasureTheory/CompactFactors/**` (14 modules) | 7728 | factor/coding machinery + compact tower |

Import closure of `no_proper_five_coloring`: 70 modules / 30351 lines before the
trim; the 13 modules outside it (926 lines) serve the other documented results.

## 3. R12 (spectral specialisation) is dead — certificate

Direction: replace the general compact-abelian difference-law/Fourier theory by the
single concrete instance the five-colouring needs. Pre-registered falsification test:
*the concrete route needs the same general lemmas in the same generality, or the
modules it can absorb total under 800 lines.*

Measured:

* The concrete objects are already fixed, once, in `Analysis/PlaneSpectrum/Basic.lean`:
  `E = algebraicClosure ℚ ℂ` (countable), `D` its Pontryagin dual, `K` the algebraic
  unit circle, `C ⊂ D` the ordinary characters, `F = E ∩ ℝ`. There is no general
  compact-abelian-group layer over them to specialise.
* What generality remains is local and cheap: discrete abelian `G` in
  `Energy.lean`/`Amenability.lean`, a general Hilbert space `H` in
  `Representations.lean`. In Lean such generality costs *fewer* lines than the
  specialisations it serves, so replacing it adds lines.
* Absorbable (unmentioned) mass in the analytical half before the trim: 321 lines,
  now removed in `E1`.

Both horns of the falsification test fire. R12 is dead; the measured alternative was
pursued instead (§1, §4).

## 4. Certified account of R1, R2, R5, R6

All four replace `exists_terminal_factor` (Stationary.lean, 201 lines, ~75 of proof).
What the rest of the development needs from a factor `q` is exactly two things
(`Analysis/PlaneSpectrum/Ergodicity.lean`, `RadialEnergy.lean:452`):

1. the instance `ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)` — ergodicity of
   the relative square;
2. `IsWild (differenceLaw (μ.map q) (condDistrib id q μ))` — K-invariance (free:
   `relative_difference_invariant`) plus C-nullity of the relative difference law of
   the identity map.

At the **trivial** factor, (2) is immediate: `condDistrib id (const) μ = μ` and
C-nullity is `relative_singularity_base`'s content (`wild_independent_difference`).
So the whole content of the tower is (1). Ergodicity of the relative square is not
free (Haar on a compact subgroup has a non-ergodic self-product), which is the honest
statement of what `exists_terminal_factor` buys and what any replacement must buy.

| route | key step | Lean status | deletable block | net |
|---|---|---|---|---|
| R1 (join of compact extensions) | join-closure of "compact extension" | **missing**; an L²-approximation of the same shape as `ChainJoin.approximation` (Stationary.lean:144) | `Approximation` 496 + `ConditionalLimits` 701, minus what stays (`relative_singularity_base`, `UniversalGood`, `universalGood_of_factor`, base case) | ≤ 900 − new code |
| R1 successor substep | strict successor from non-ergodicity | **already there**: `CompactTower.strict_compact_successor`, Factors.lean:206 | — | 0 |
| R2 (transfinite) | countable-ordinal recursion | missing; a factor must still be coded as a *function* (`CodedMax.Model`), so `Factors` 586 + `Separability` 573 + `AlgebraModels` 664 stay | as R1 | ≤ 900 − new code |
| R5 (countable reduction) | explicit countable family | missing; each successor is produced by `Classical.choice` from a kernel, so no explicit family exists; `Separability.lean` (573) stays | as R1 | ≈ 0 |
| R6 (fixed point) | fixed point of an operator | missing; fixed-point existence is join-closure plus successor-closure again, i.e. R1's obligations | as R1 | ≤ 900 − new code |

The `2053` figure in the brief is the *whole* import cone of `Approximation.lean`, not
the propagation. `RelativeProducts` (472), `BoundedFunctions` (223), `Amenability`
(411), `Kernels` (774), `Functions` (884) are consumed by `FactorLp`, `Compact`,
`condDistrib` and by `Energy`/`InvariantMean`/`Ergodicity`; every route keeps them.
So the largest possible tower deletion is `Approximation.lean` +
`ConditionalLimits.lean` = **1197 lines**, before paying for the replacement.

## 5. R1's last step is false as stated (the decisive obstruction)

R1 ends "…so `X ×_{Y*} X` is ergodic; now apply Theorem A at `Y*`". Theorem A needs
`d` **not** `Y*`-measurable. That can fail, on the development's own space:

Take `X = D`, `μ = Haar_D`, `K` acting by `(u·d)(z) = d(uz)`.

* `μ` is `K`-invariant (automorphisms preserve Haar) and ergodic: for
  `f = Σ c_z χ_z`, `U_u χ_z = χ_{u⁻¹z}`, and `K` acts freely on `E∖{0}` because
  `((3+4i)/5 − 1)z = 0` forces `z = 0`; so every nonzero orbit is infinite and
  `c_z = 0` for `z ≠ 0`.
* `μ` is wild: `C` is a Borel subgroup of the compact group `D` and a continuous
  injective image of `ℝ²`, hence not compact, not open, hence Haar-null.
* the action is isometric, and every factor of an isometric system is a compact
  extension of the trivial factor, so `Y* = X`.

Then `X ×_{Y*} X` is a point (ergodic, vacuously) while the wild `d = id` is
`Y*`-measurable, so Theorem A is inapplicable at `Y*`: R1 cannot produce
`UniversalGood` at `Y*` here.

The same system is harmless for the architecture in the tree: `K` acts freely on
`E²∖0`, so `Haar_D × Haar_D` is ergodic diagonally, the **trivial** factor has ergodic
relative square, and `UniversalGood` holds there by `relative_singularity_base` (a
`K`-fixed character is trivial, so a wild equivariant `d` is never constant). That is
why the `UniversalGood`-maximality is the right predicate and Theorem A alone is not
a drop-in replacement.

Consequence: any route obtaining C-nullity from Theorem A must also show every needed
wild `d` is non-measurable at the chosen factor. For R1 that is false. For the
"minimal factor with ergodic square" variant it is unproved, and on `X = D × W` with
`μ = Haar_D ⊗ ν_W`, `W` mixing, the projection to `D` is a wild `d` that *is*
measurable there — so it needs a real argument, not a definition.

## 6. Harness (reusable)

* `build.py <root> <builddir>` — topological `lean -o` build, content-hash cache
  (`.hashes.json`), dependency-aware scheduling, per-module FAIL lines.
* `blocks.py` — declaration block extraction and safe deletion. It handles
  docstrings, `@[...]` on the preceding *or* the same line, and `omit … in` /
  `include … in` prefixes; each of those three broke an earlier iteration (silent
  attribute loss, dangling docstring, orphaned `omit`), so keep them.
* `deadfinal.py <tree> <out.json>` — fixed-point unmentioned-declaration finder.
* `check_changed.py <pristine> <new>` — verifies exactly the modules whose source
  changed. Adequate for deletion-only patches (a deletion cannot break a module that
  never mentioned the name); 42/42 changed modules passed it, then the full
  from-scratch build confirmed 83/83.

## 7. What −1500 needs

1. the −718 trim (done, verified); and
2. ~800 lines of tower surgery: `Approximation.lean` + `ConditionalLimits.lean` must
   go, which needs a replacement for `exists_terminal_factor` that supplies
   ergodicity of the relative square *without* the `(2.6)` propagation — and the
   replacement must survive §5.

Both are needed; neither alone reaches 1500. Any claim of 2000+ from R1 alone is
inconsistent with the measured module sizes.
