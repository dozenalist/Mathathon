# Paper-to-Lean fidelity audit (m14, direction d31)

Source paper: `attachments/paper.pdf` ("The Euclidean plane is not five-colorable", 62 pp.);
text copy `.scratch/paper.txt`. Target tree: `lean/OAI/**` (83 modules, 31277 lines, baseline
of `sprint/simplify/m10/harness/BASELINE.json`).

Method. Every numbered statement of the paper was located in the text with
`sprint/simplify/m14/fidelity_scan.py` (declaration-name/keyword scan over all 83 modules); the
surviving candidates were read at their signatures, and the statements that carry the headline
chain (1.1, 1.3, 1.4, 2.3-2.7, 3.1-3.5, 4.1-4.3) were read in full. This is a *statement*
audit: I did not re-verify any proof. Line numbers are 1-based into the named module.

## Verdict in one line

Every paper result that Theorem 1.1 depends on has a Lean counterpart with the same claim, with
five structural deviations, all of which are either forced (the printed Lemma 2.7 is false at
`Y = X`) or stronger/reformulated in the direction the endgame needs; one paper corollary
(1.5) is not formalised and is not used in the paper's proof.

## Table

| paper | Lean declaration (module:line) | verdict |
|---|---|---|
| Thm 1.1 no proper 5-colouring | `EuclideanFiveColor.no_proper_five_coloring` Five:135 | same |
| Def 1.2 weak measurable colouring | `WeakColoring` Coloring:27 | same |
| Thm 1.3 transfer of colorability | `proper_iff_weak` Transfer:12 | same |
| Thm 1.4 no weak measurable 5-colouring | `no_measurable_weak_five_coloring` Five:105 | same |
| Cor 1.5 positive five-colour badness | — | **not formalised** (not used in the proof) |
| Def 2.1 E, K, D, C | `E` Basic:9, `K` Basic:11, `D` Basic:47, `C` Basic:98 | same |
| Def 2.2 wild | `IsWild` Basic:297 | same |
| Thm 2.3 rigidity | `wild_fourier` Ergodicity:335, `finite_wild_fourier`:364, `residual_fourier`:403 | same |
| Lem 2.4 cosets null | `wild_coset_null` Basic:304, `wild_independent_difference`:326 | same |
| Lem 2.5 vanishing line average | `wild_line_null` Basic:696, `wild_continuous_coefficient_zero` Characters:534 | same |
| (2.6) approximation property | no separate statement; it is the `ha` hypothesis of `relative_singularity_approximation` ConditionalLimits:622, discharged at its two uses | **concretised** |
| Lem 2.7 relative singularity | `relative_singularity_base` ConditionalLimits:352, `relative_singularity_limit`:269, `relative_singularity_approximation`:622, `relative_singularity_successor` Approximation:384, plus `UniversalGood` ConditionalLimits:669 | **reformulated; printed form FALSE at Y = X** |
| Lem 3.1 compact tower | `exists_terminal_factor` Stationary:126 (`CodedMax.exists_maximal` Factors:523) | **reformulated**: maximal `UniversalGood` factor with ergodic relative product, not an explicit transfinite tower |
| Lem 3.2 conditional multiple averages | `conditional_multiple_mean_zero` AlgebraModels:566, `conditional_integer_multiple_mean_zero`:652 | same |
| Lem 3.3 radial identities | `projectedMass_radial` Energy:432, `radial_positive_near_zero` RadialEnergy:421, `massReal_vanish` RadialEnergy:452 | same |
| Lem 3.4 general position in a number field | `numberField_general_position` NumberFields:514, `General`:346, `exists_general`:351, `spanning_selection` Selections:11 | same |
| Lem 3.5 addition under a cap | `list_cap` Selections:334, `integer_cap`:402, `integer_abs_cap`:414 | same |
| Lem 4.1 continuous vectors, positivity | `ContinuousVectors.space` Representations:182, `clamp_lipschitz` Representations:317, `residual_fourier` Ergodicity:403, `fieldVector_range` BorelTransfer | same |
| Prop 4.2 proper to weak measurable | `proper_to_borel_weak_algebraic` BorelTransfer:439 | same (strictly stronger hypothesis set: a proper labelling of E suffices) |
| Lem 4.3 density-point properness | `product_zero_of_inner_zero` WeakColoring:22, `all_parameters_product_zero` WeakColoring:31, `exists_density_interval` Expansion:592, `FlatDensityZero` PaletteDensity:190 | same |
| Def 5.1 palettes | `five_palette_admissible` Accumulation:359, `palette_eq_measurable`:365, `trace_positive_le_palette` BinaryPalettes:193 | same |
| Lem 5.2 palette transfer | `palette_transfer_pair` PaletteDensity:143, `palette_neighbor_real` States:9, `palette_neighbor_disjoint` States:23 | same |
| Cor 5.4 sixty-degree exclusion | `four_support_no_sixty` FourTransport:218, `five_support_no_sixty` FiveSupport:138, `direction_sixty_unit_real` FourTransport:204 | same |
| Lem 5.5 binary-centre separation | `binary_centers_separated` BinaryPalettes:123, `binary_centers_countable`:167, `triangle_centers_separated` Accumulation:178 | same |
| Prop 5.6 palette cardinality <= 2 | `palette_cardinality` BinaryPalettes:260, `palette_triple_null`:252, `circle_complement_binary`:243 | same |
| Def 6.1 transition graph | `TransitionEdge`/`transitionSet` Transitions:9, `transitionGraph` CyclicCore:213 | same |
| Lem 6.2 an edge has an avoiding trace | `transition_abundance` Transitions:25, `state_support_avoiding_trace` BoundaryTrace:24, `avoiding_trace_palette`:53 | same |
| Lem 6.3 strict state separation | `strict_state_sequence_false` States:683, `strict_state_no_unit_support`:704, `strict_state_sequence_local_false`:547 | same |
| Lem 6.4 singleton-pair alternation impossible | `binary_alternation` BinaryPalettes:11, `binary_pair_distinct`:28, `alternating_twostep`:55 | same |
| Thm 6.5 local finiteness | `cyclicCore_compact_finite` CyclicCore:269, `fourCenter_compact_finite` Accumulation:281, `threeCenter_compact_finite`:348 | same |
| Lem 6.6 four-cycle continuity | `four_sequence_no_accumulation` Accumulation:246, `fourCenter_closed`:270, `four_support_transport` FourTransport:99 | same |
| Lem 6.7 support contact bans an angular step | `five_support_step_ban` FiveSupport:90, `five_contact_next`:175, `five_contact_prev`:185, `no_alternating_sectors` Sectors:392 | same |
| Prop 7.1 cycle of common exclusion continua | `CommonInterface` ContinuumLimits:228, `commonInterface_of_continuum`:246, `no_triangle_commonInterface`:252, `no_four_commonInterface`:270, `no_five_commonInterface`, `commonInterface_graph_acyclic`:296, `commonInterface_of_compact_sequence`:318 | **reformulated**: the Lean proves acyclicity of the interface graph at every centre and then builds full approximants; the separate "cycle of continua" object is not needed |
| Lem 7.2 disk inequalities, support detection | `diskAverage_unit_pair` DiskAverages:63, `support_of_positive_diskAverage_limit` Mesh:39 | same |
| Lem 7.3 a missing edge has small overlap | `missing_edge_overlap` DiskAverages:307, `missing_edge_uniform`:253, `missing_edge_lim` Accumulation:214 | same |
| Lem 7.4 small holes and tree fillings | `HoleApprox` HoleApproximation:280, `holeApprox_exists`:291, `HoleApprox.fill_cores` FullApproximation:186 | same |
| Lem 7.5 cover obstruction on a square | `compact_open_cover_impossible` PlanarCovers:374 (via `finite_open_cover_impossible`:348) | same |
| Lem 7.6 non-null core loops | `cyclicCore_compact_finite` CyclicCore:269 + `fullApprox_exists_of_finite_core` FullApproximation:268 + `no_large_positive_sequence` Mesh:84 | reformulated: the core-loop alternative is replaced by the compact finite core plus the mesh contradiction |
| Lem 7.7 midpoint detection | `graphCut_contractible` GraphCuts:197, `finite_fiber_separation`:269, `midpoint_threshold_labels` FullApproximation:52 | same |
| Lem 7.8 connected midpoint preimage crosses | `annulus_maps_eventually_forest` FullApproximation:64, `planeAnnulus` GraphPatches:168, `annulus_forest_extension` GraphPatches | same |
| Lem 8.1 one-sided strip restrictions | `outer_strip` AngularBoundary:244, `inner_strip`:251, `outer_strip_trace` BoundaryTrace:182, `inner_strip_trace`:210 | same |
| Prop 8.2 no length five | `five_support_no_sixty` FiveSupport:138, `five_opposite_contacts_false`:199, `five_palette_admissible` Accumulation:359, `fiveState_adj`:390 | same |
| Lem 8.3 six-position word alternatives | `sixAngle` AngularBoundary:103, `sixty_six`:92, `sixty_three`:98, `four_word_has_outsider`:28 | same |
| Lem 8.4 geometry of four split rays | `four_split_antipodes` BoundaryTrace:359, `four_word_parity` AngularBoundary:39, `four_word_opposite_parity`:47 | same |
| Prop 8.5 no length four | `four_endpoint_sequence_false` Accumulation:32, `four_normalized_sequence_false`:233, `four_gap_exists`:257, `four_support_transport` FourTransport:99 | same |
| Lem 8.6 local binary rigidity | `binary_strip_rigidity` BoundaryTrace:248, `binary_strip_palette_rigidity`:280 | same |
| Lem 8.7 the boundary is one orbit | `angleBoundary_one_orbit` AngularBoundary:448, `angleEssential_connected` Sectors:209, `one_orbit_sectors`:274 | same |
| Lem 8.8 polynomial three-label region | `polynomial_region_angles` Moser:62, `polynomial_region_density` Sectors:365 | same |
| Lem 8.9 seven-point certificate | `seven_point_boxes` Moser:268, `moser_edge_unit`:145, `placedMoser_edge_unit`:173, `moser_not_three_colorable`:159 | same |
| Prop 8.10 no length three | `no_triangle_interfaces` Sectors:428, `moser_density_impossible` Sectors:326 | same |

## The five deviations, in detail

1. **(2.6) is not a statement but a hypothesis.** The paper's approximation property appears in the
   Lean as the explicit predicate `ha` of `relative_singularity_approximation`
   (ConditionalLimits.lean:622): for every bounded `H` and every `ε` a finer factor `q` is supplied
   that is itself `UniversalGood` and approximates `H ∘ p` in `L²` within `ε`. It is discharged at
   exactly two sites, `Stationary.lean:144` (`hjoin`, via `ChainJoin.approximation`) and
   `Stationary.lean:159` (`hug`, via `relative_singularity_successor`). This is the only place in
   the development where the approximation property is consumed; nothing else uses it.

2. **Printed Lemma 2.7 is false at `Y = X`.** With `Y` the top factor, conditionally independent
   samples over `Y` coincide, so the difference law is `delta_1`, and `1 ∈ C` (the trivial
   character is continuous), so the law has `C`-mass `1`, not `0`. The paper's hypotheses do not
   exclude `Y = X`. The Lean is unaffected because it never relies on 2.7: it maximises over
   `UniversalGood` (`ConditionalLimits.lean:669`), which is a statement about *every* wild `d`,
   and `UniversalGood μ id` fails for exactly this reason, so the maximal factor cannot be the top
   factor. See my findings f15 and f9, and m16's d24.

3. **Lemma 3.1 is reformulated.** Instead of building the transfinite compact tower of the paper,
   `exists_terminal_factor` produces a maximal `UniversalGood` factor whose relative product is
   ergodic, using countable maximality inside the separable `L²` (`CodedMax.exists_maximal`).
   The two properties the rest of the proof consumes — `ErgodicVAdd Rot (D×D) (RelativeProduct.law
   μ q)` and `IsWild (differenceLaw (μ.map q) (condDistrib id q μ))` — are delivered
   (`Ergodicity.lean:29-31`, `:52-58`).

4. **Proposition 7.1 is reformulated.** The paper isolates a cycle of common-exclusion continua at
   one centre and then excludes cycles of length 3, 4, 5. The Lean proves instead that at every
   centre the interface graph is acyclic (`commonInterface_graph_acyclic`, using
   `no_triangle_interfaces`, `no_four_interfaces`, `no_five_commonInterface`), then derives the
   forest property of crossing graphs (`eventually_forest_of_bridges`), builds the full graph
   approximants (`fullApprox_exists`) and finishes by the cover obstruction applied directly to
   graph-valued maps (`graph_map_large_positive` Five:72) against
   `FullApprox.no_large_positive_sequence` Mesh:84. The §8 exclusions are still used, but through
   acyclicity rather than through the cycle object.

5. **Corollary 1.5 is not formalised.** It is a quantitative corollary about finitely additive
   isometry-invariant means and needle frequencies; the paper uses it nowhere in the proof of
   Theorem 1.1 (`grep '1\.5' .scratch/paper.txt` hits only its own statement). Not needed for the
   headline; it should not be claimed as formalised.

## Caveats

* This is a statement-level audit. Proofs were not re-verified; the build and axiom certificates
  are `sprint/simplify/m10/harness/certify.py` (d4).
* Line numbers are from the baseline tree; a patched tree shifts them.
* Rows marked "same" mean: same hypothesis class and same conclusion, up to notational
  translation (E for the algebraic plane, `Fin 5` for the five labels, `spatialSupport` for the
  essential support, `Straddle` for the annular region Δ(·)).

## Line cost per paper part (measured, all 31277 lines mapped, nothing left over)

Computed by summing the raw line counts of the modules carrying each part (multi-part files are
counted once, in the first part that claims them; the partition is exhaustive — the script found
no unmapped module and the parts sum to the tree total).

| paper part | Lean lines |
|---|---|
| §2.1-2.5 — E, K, D, C, wildness, Lemma 2.4 (cosets null), Lemma 2.5 (vanishing line average) | 2831 |
| §2.6-2.7 + §3.2 — relative singularity: `UniversalGood`, the phase/encoding machinery, the maximality, the conditional multiple averages | 8109 |
| §3.3-3.5 + spectral — radial identities, number field, addition under a cap, vector measures, invariant means, ergodic decomposition | 5301 |
| §4 — transfer (Lemmas 4.1, 4.3, Proposition 4.2) | 720 |
| §5 — palettes (5.1, 5.2, 5.4, 5.5, 5.6) | 1885 |
| §6 — transition graph (6.1-6.7) | 3898 |
| §7 — approximants, common interfaces, cover obstruction, mesh | 4371 |
| §8 — angular boundary, cycle exclusions, Moser certificate | 2817 |
| statement transfer and auxiliary results (Five, Seven, Transfer, Chromatic, NullSetRobust, proper_iff_weak support) | 1345 |
| **total** | **31277** |

Reading. The single paper part that costs the most is §2.6-2.7 + §3.2 at 8109 lines (26% of the
tree) — the relative-singularity machinery plus the conditional multiple averages. §3.3-3.5 and
its spectral support adds 5301 (the second largest), so the rigidity as a whole (§2.6-§3.5) is
13410 lines, 43% of the development. Part II (§5-§8) is 12971 lines, 41%. The transfer (§4) is
only 720 lines, so no restructuring of the transfer can reach the 1500-line target. This agrees
with the dead-route certificates of d12 (transfer) and d19 (palette pipeline), and shows why the
only blocks with enough mass to matter are §2.6-2.7/§3 (d3, d6, d8, d9, d11) and the Part II
pipeline (§5-§7: d14, d17, d19, d28).
