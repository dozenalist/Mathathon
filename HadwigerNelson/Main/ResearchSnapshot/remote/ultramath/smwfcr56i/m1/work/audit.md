# Statement-fidelity audit of the Hadwiger–Nelson Lean bundle

Member m1, direction d5. Question asked: **is the Lean theorem the paper's theorem?**
All verdicts below are from reading the bundle's source in `lean/OAI/**` and from
machine checks run in this VM; nothing is taken from the review bundle's prose.

Files produced by me (all under `.ultramath/smwfcr56i/m1/`):

| file | what it is |
|---|---|
| `Axioms.lean`, `work/axioms.txt` | `#print axioms` driver + log, 27 declarations |
| `Def12.lean` | machine-checked: the bundle's `WeakColoring` **is** paper Definition 1.2 |
| `ChromaticNumber.lean` | machine-checked: the paper's displayed `6 ≤ χ(ℝ²) ≤ 7`, which the bundle never states |
| `verify_seven.py` | exact (integer) verification of every constant in both seven-colourings |

---

## 0. The "port" premise is false

The bundle targets Lean 4.34.1 + mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`.
`fetch_exact_env.sh` has already put exactly that toolchain and that fully cached mathlib
in `repo/.scratch/`.  All 78 modules compile **with no patch at all**:

```
$ (cd repo/lean && source ../scripts/env4341.sh && lean OAI/Analysis/PlaneSpectrum/Basic.lean)
$ echo $?
0
```

`scripts/build4341.log` records the full run: 78 modules, `OK` each, 2–14 s, final line
`done`.  The 47 failures in `scripts/build_status.json` are 4.33.1-vs-4.34 API gaps
(`And.fun_mul`, `MemLp.coeFn_toLp`, `isometry_add_right`, …), i.e. artifacts of using the
wrong toolchain, not defects of the bundle.  A 4.33.1 port would be work spent undoing
Mathlib API changes.

## 1. Axiom certificate

Command (from `repo/lean`):

```
source ../scripts/env4341.sh
LEAN_PATH="build/lib:$LEAN_PATH" lean ../.ultramath/smwfcr56i/m1/Axioms.lean
```

Result — **every** declaration listed depends only on `[propext, Classical.choice,
Quot.sound]`:

```
'OAI.EuclideanFiveColor.no_proper_five_coloring'            [propext, Classical.choice, Quot.sound]
'OAI.Problem160.properColoring_seven'                       [propext, Classical.choice, Quot.sound]
'OAI.Problem160.exists_unit_distance_coloring_of_center_cover'
'OAI.Problem160.triangular_lattice_cover'
'OAI.Problem160.triangularLattice_dist_gt_two'
'OAI.Problem160.SevenLattice.same_color_separation'
'OAI.EuclideanFiveColor.no_measurable_weak_five_coloring'
'OAI.EuclideanFiveColor.proper_to_borel_weak'
'OAI.EuclideanFiveColor.fullApprox_exists'
'OAI.EuclideanFiveColor.FullApprox.no_large_positive_sequence'
'OAI.EuclideanFiveColor.graph_map_large_positive'
'OAI.PlanarCover.compact_open_cover_impossible'
'OAI.EuclideanFiveColor.graphRealization_positive_three'
'OAI.EuclideanFiveColor.thresholdMap_mem_forest'
'OAI.EuclideanFiveColor.compact_forest_charts'
'OAI.PlaneFiveColor.Spectral.wild_coset_null'
'OAI.PlaneFiveColor.Spectral.wild_independent_difference'
'OAI.PlaneFiveColor.Spectral.wild_line_average_zero'
'OAI.EuclideanFiveColor.palette_cardinality'
'OAI.EuclideanFiveColor.binary_centers_separated'
'OAI.EuclideanFiveColor.cyclicCore_compact_finite'
'OAI.EuclideanFiveColor.no_five_exclusion_continua'
'OAI.EuclideanFiveColor.no_five_commonInterface'
'OAI.EuclideanFiveColor.no_triangle_commonInterface'
'OAI.EuclideanFiveColor.five_opposite_contacts_false'
'OAI.EuclideanFiveColor.straddle_connected_unit'
'OAI.EuclideanFiveColor.four_words_no_mixed'
```

No `sorryAx`, no `Lean.ofReduceBool`, no user axiom.  Textual scan over all 78 modules
also finds **zero** occurrences of `sorry`, `axiom`, `native_decide`, `@[implemented_by]`,
`opaque` and `admit`.

Consequence: `6 ≤ χ(ℝ²)` is machine-checked in ZFC + the three standard Lean axioms, which
is the paper's own standard.

## 2. Definition-by-definition verdicts

| paper | Lean | verdict |
|---|---|---|
| Def 1.1 proper *k*-colouring: `c : ℝ² → {1..k}`, `‖x−y‖ = 1 ⇒ c x ≠ c y` | `OAI.EuclideanFiveColor.ProperColoring k c := ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y` (`Coloring.lean:7`) and `OAI.Problem160.ProperColoring k := ∃ c : Plane → Fin k, ∀ x y, dist x y = 1 → c x ≠ c y` (`Basic.lean:26`) | **exact.** No measurability, no boundedness, no periodicity, no metric restriction. `Plane = EuclideanSpace ℝ (Fin 2)`; `Fin k` is exactly `{1..k}`. |
| Def 1.2 weak measurable *k*-colouring | `OAI.EuclideanFiveColor.WeakColoring k c := AEMeasurable c volume ∧ ∀ᵐ p ∂(volume.prod angularMeasure), c p.1 ≠ c (p.1 + direction p.2)` (`Coloring.lean`) | **equivalent**, and now machine-checked (`Def12.lean`): the paper's literal form, `∀ R>0, ∑_i ∫_{B(0,R)}∫_{S¹} 1_{A_i}(x)1_{A_i}(x+u) dσ dx = 0`, is `↔` the Lean form for *every* `c : ℂ → Fin k`, no hypothesis. `angularMeasure = AddCircle.haarAddCircle`, a probability Haar measure; `direction t = e^{it}`, `‖direction t‖ = 1`. `AEMeasurable` vs the paper's "Lebesgue measurable" is exactly the null-set invariance the paper states in the sentence after Def 1.2. |
| "the `Fin 5` weights" ∑_i 1_{A_i}(x)1_{A_i}(x+u) | `Def12.sum_class_indicators` | **checked**: `∑ i : Fin k, 1_{c x = i}·1_{c y = i} = [c x = c y]`. The five colour-class indicators sum to the equality indicator, so nothing is lost by working with `c` instead of the `A_i`. |
| `graphRealization`, §7's metric graph on 5 labels | `graphRealization G := {p | ∃ i j, (i = j ∨ G.Adj i j) ∧ ∃ t ∈ [0,1], p = (1-t)e_i + t e_j}` inside `(V → ℝ)`; `GraphSpace G := ↥(graphRealization G)` | **exact** topological realization of the finite simple graph (edge interiors = two positive barycentric coordinates, vertices = one). `graphRealization_positive_three` is the paper's "every point of G has at most two positive coordinates" and is checked ("at most two of three labels agree"). Used with `G = ⊤ : SimpleGraph (Fin 5)` = K₅. |
| §7.1 eq. (22), thresholded/renormalized disk average | `thresholdWeight = max (diskAverage c ε i q - α) 0`, `thresholdTotal = ∑`, `thresholdMap = weight/total` (`GraphRealization.lean:243`) | **exact**, including the `α < 1/5` side condition that makes `thresholdTotal > 0` (so no division by zero is hidden). |
| §7/§8 "global graph approximant with small exceptional disks" | `structure FullApprox c α t`: `ε ∈ (0,t)`; finite `disks` of positive radius, pairwise disjoint closed balls, total radius `< t`; `map : C(closedBall 0 5, GraphSpace ⊤)` with `map z = thresholdMap c ε α z` off the holes | **exact** and *inhabited by construction*: `fullApprox_exists` produces it from `Measurable c` + `WeakColoring 5 c`; it is not an extra hypothesis smuggled in. |

## 3. Theorem-by-theorem verdicts

| paper | Lean | verdict |
|---|---|---|
| **Thm 1.1** no proper five-colouring, arbitrary colour classes | `OAI.EuclideanFiveColor.no_proper_five_coloring : ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c` (`Five.lean:133`) | **exact.** Note the task prompt's pointer is wrong: this declaration is in `Five.lean`, not `Compactness.lean`. |
| **Thm 1.1**, 2nd sentence: `6 ≤ χ(ℝ²) ≤ 7` | — | **not formalized.** `OAI.Problem160.planeChromaticNumber := sInf {k | ProperColoring k}` occurs *only* in its definition. **Closed by me**: `ChromaticNumber.lean` proves `OAI.Problem160.chromaticNumber_bounds : 6 ≤ planeChromaticNumber ∧ planeChromaticNumber ≤ 7`, axiom-clean. |
| **Thm 1.3**, forward: proper ⟹ weak measurable, every *k* | `OAI.EuclideanFiveColor.proper_to_borel_weak : ProperColoring k c → ∃ d, Measurable d ∧ WeakColoring k d`, `{k : ℕ} [NeZero k]` | **exact** for the direction used. |
| **Thm 1.3**, converse: weak measurable ⟹ proper | — | **not formalized.** Not needed for Thm 1.1. I checked the paper's proof by hand (Lemma 4.3 density-point sets are strictly unit-independent, a translate of any finite configuration lands in the conull set, then Tychonoff/FIP) — valid. So the bundle proves *less* than the paper here, but nothing that Thm 1.1 uses. |
| **Thm 1.4** no weak measurable five-colouring | `no_measurable_weak_five_coloring (hc : Measurable c) (hw : WeakColoring 5 c) : False` | **equivalent**: `Measurable` in place of `AEMeasurable` is WLOG because `BadPair(c)` and `BadPair(c')` differ by a product-null set when `c = c'` a.e. Not a weakening. |
| **Cor 1.5** positive five-colour badness | — | **not formalized.** Its δ is existential and comes from de Bruijn–Erdős compactness applied to Thm 1.1, so nothing here is quantitative. |
| §1 upper bound, hexagonal 7-colouring | `OAI.Problem160.properColoring_seven : ProperColoring 7` | **exact** (see §5). |
| **Lemma 2.4** coset/difference rigidity | `PlaneFiveColor.Spectral.wild_coset_null`, `wild_independent_difference` | counterpart present. |
| **Lemma 2.5** vanishing line average | `PlaneFiveColor.Spectral.wild_line_average_zero`, `wild_line_null` | counterpart present. |
| **Lemma 3.1** compact tower | `OAI...exists_terminal_factor` (`CompactFactors/Stationary.lean:126`) | counterpart present. |
| **Prop 5.6** palette cardinality `1 ≤ |P_x(e)| ≤ 2` a.e. | `OAI.EuclideanFiveColor.palette_cardinality : ∀ᵐ t, 1 ≤ (palette c hc x t).card ∧ (palette c hc x t).card ≤ 2` | **exact**, including the lower bound and the "exceptional set may depend on x". |
| **Lemma 5.5** binary-centre separation | `OAI.EuclideanFiveColor.binary_centers_separated : ∃ δ > 0, …` | counterpart present, same shape. |
| **Thm 6.5** local finiteness of cyclic centres | `OAI.EuclideanFiveColor.cyclicCore_compact_finite : (K ∩ CyclicCore c).Finite` | counterpart present, same shape. |
| **Lemma 7.5** cover obstruction on a square of side ten | `OAI.PlanarCover.compact_open_cover_impossible` | **proved in a stronger form**: any compact `Q ⊇ ball(0,5)`, not only a square. The proof is the Brouwer/degree argument of the paper's Lemma 7.5, carried out on the ball `ball(y,4) ⊆ Q` rather than on `Q` itself, so the generalization is genuine. Requires `1 + 2r`-style separation only through `diam ≤ 2`; matches. |
| **Prop 7.1** cycle of common exclusion continua | `OAI.EuclideanFiveColor.no_five_exclusion_continua` (`Exclusion.lean:1365`) | counterpart present. |
| **Lemma 7.8** connected midpoint preimage crosses the annulus | `straddle_connected_unit`, `straddle_eventually_of_compact_limit` | counterpart present. |
| §8.2 five-cycle exclusion | `no_five_commonInterface : (∀ i, CommonInterface c x i (i+1)) → False` | counterpart present; `i+1` on `Fin 5` is the cyclic successor, so this is the 5-cycle `0-1-2-3-4-0`. |
| §8.4–8.5 triangle exclusion | `no_triangle_commonInterface`, `five_opposite_contacts_false`, `four_words_no_mixed` | counterpart present. |

## 4. Defects

I found **no** declaration whose Lean statement is false as stated, and no declaration
weaker than the paper's statement in a way that affects Theorem 1.1.  Two fidelity gaps
were found (§3, Thm 1.1 second sentence; Thm 1.3 converse); the first is closed here, the
second is irrelevant to the result and its paper proof is correct.

## 5. The upper-bound constants, exactly

`verify_seven.py` (integer arithmetic only; `python3 verify_seven.py`, all checks pass):

* triangular lattice `Z + Zω` with `ω = e^{2πi/3}`, sites `(a + b/2, √3 b/2)`;
  covering radius squared is exactly `1/3`, attained at the centroid `(1/2, √3/6)`
  (`|(1/2, √3/6)|² = 1/4 + 1/12 = 1/3`);
* paper route, `r = 2/5`: `2r = 4/5 < 1` and `(√21 − 2)·r > 1 ⟺ √21 > 9/2 ⟺ 21 > 81/4`;
* Lean route, spacing `4/5`, colour `a + 3b mod 7`:
  covering radius `≤ (4/5)/√3`, and `2r = 14/15 < 1`;
  `4/(5√3) ≤ 7/15 ⟺ 144 ≤ 147`;
  same-colour centres `≥ (4/5)√7`, and `(4/5)√7 > 1 + 2r = 29/15 ⟺ 1008 > 841`;
* index-6 fails exactly where 7 succeeds: cover radius `d/√3` and min same-colour
  spacing `2d` would need `2d > 1 + 2d/√3`, i.e. `d > 1.1830`, while `2r < 1` needs
  `d < √3/2 = 0.8660`.

So `OAI.Problem160.properColoring_seven` is the paper's claim, and its numeric chain is
correct; it is the same construction with `r_eff = 4/(5√3)` in place of `2/5`.

## 6. What I did not do

* No statement-by-statement map of §2–§3's analytic lemmas (Lemma 2.6, 2.7, 3.2–3.5):
  that is direction d3's remit. I only confirmed that counterparts for 2.4, 2.5, 3.1 exist.
* I did not attempt to prove or refute any of the paper's analytic or topological steps;
  I only checked that the Lean statements are the paper's statements.
* I did not modify anything outside `.ultramath/smwfcr56i/m1/`.
