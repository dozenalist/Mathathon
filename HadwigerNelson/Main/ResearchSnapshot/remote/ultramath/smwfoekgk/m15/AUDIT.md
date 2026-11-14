# R11 audit: the approximation/phase-collision chain, measured

Member m15, direction d6.  Two deliverables:

* **machine-checked**: `sprint/simplify/m15/work/TowerMax.lean` (139 lines, axiom-clean,
  `[propext, Classical.choice, Quot.sound]`) proves that the supremum of the compact
  tower has ergodic relative product, with **no approximation property and no
  `UniversalGood`**, plus a drop-in replacement for `exists_terminal_factor` that
  isolates the single remaining obligation;
* **measured**: the exact size of the material an architecture change would delete
  (5 161 declaration lines, 276 declarations, 13 modules, 3 modules whole), and the
  exact reason it cannot be cashed today.

Reproduce the measurements with

```
cd sprint/simplify/m15 && python3 reach2.py
```

`reach2.py` parses every `theorem/lemma/def/structure/inductive/instance` in the 83
modules of `lean/OAI`, takes its line span as its body, records which *other* declared
names the body mentions (dot-suffix aware), and computes forward reachability from
`no_proper_five_coloring`, `properColoring_seven`, `chromaticNumber_bounds`,
`no_proper_five_coloring_algebraic`, `not_proper_five_coloring_compl_null`,
`proper_iff_weak`, `algebraic_colorable_iff`.  The result is mention-based, hence
approximate in both directions (an unused `open`ed name counts as a mention; a name
reached only through a `simp` lemma set does not).

## 0. Baseline

83 modules, 31 360 lines, 2 511 declarations; 2 319 declarations reachable from the
headline theorems.  The whole `MeasureTheory/CompactFactors` directory (14 modules,
7 729 lines) is reachable only through `exists_terminal_factor`.

## 1. The prize, measured

Make `exists_terminal_factor` a leaf (keep the statement, drop the proof) and recount:

| | |
|---|---|
| declarations lost | **276** |
| declaration lines lost | **5 161** |
| modules affected | 13 |
| modules that die whole | 3 (`PhaseCollision`, `SmallArcs`, `PhaseEncoding`, 1 117 file lines) |

Per module — file lines / dead declaration lines / surviving declaration lines:

```
Functions              885   810     10        Kernels                775   585    141
PhaseCollision         538   446      0        ConditionalSpectrum    498   423     28
Centers                704   413    249        ConditionalLimits      702   401    144
RelativeCenters        599   389     81        Approximation          497   367     87
ConditionalSelection   443   351     65        SmallArcs              323   291      0
Factors                587   274    255        PhaseEncoding          256   234      0
Basic (PlaneSpectrum)  736   177    494        Stationary             202     0    173
```

Ten of the thirteen modules keep under 40 % of their body.  The per-declaration list,
ready to delete, is `sprint/simplify/m15/DEAD-IF-THEOREMA.txt` (307 lines, `file:line
name (lines)`).

## 2. It cannot be cashed in halves

The three propagation theorems are `relative_singularity_base`
(ConditionalLimits:352), `relative_singularity_approximation` (ConditionalLimits:622),
`relative_singularity_successor` (end of Approximation.lean).  Reachable declaration
sets: base 248, approximation **681**, successor **680**, both 682.

`relative_singularity_successor` does *not* reach `relative_singularity_approximation` —
the successor step never uses (2.6) or the phase-collision induction — yet the two share
679 of 681 declarations (`exact_finite_center_reduction`, `kernelEncoding`,
`exists_small_arc_constants`, `finite_uniform_(successor|precision)_contradiction`, ...).
Deleting the join propagation alone saves **1** declaration, the successor alone **6**.
Both must go or neither does.

## 3. What is now machine-checked (new)

`work/TowerMax.lean`, checked under Lean 4.34.1 + pinned mathlib against the existing
83 oleans:

```
source scripts/env4341.sh && cd sprint/simplify/m15/work && lean TowerCheck.lean
```

* `Tower μ` — inductive: the base factor, the strict compact successor
  (`CompactTower.strict_compact_successor` applied to `encode ∘ extend`), and countable
  chain joins (`ChainJoin.code`).  Closure under successors and joins is therefore
  *free by construction* — no hypothesis, no (2.6).
* `exists_tower_maximal` — `CodedMax.exists_maximal` with `Good := Tower`.
* `exists_ergodic_factor` — the maximal `Tower` member has **ergodic relative product**.
  Proof: if not, `strict_compact_successor` (which is unconditional in the
  non-ergodicity of the relative product) produces `H` not factorisable through the
  factor, hence a strictly larger `Tower` member, contradicting maximality.  This is the
  whole of what `exists_terminal_factor` needs from maximality.
* `exists_terminal_factor_of_tower_good` — the drop-in replacement: given `UniversalGood`
  at the tower supremum, it produces exactly the conclusion of `exists_terminal_factor`.

All three axioms: `[propext, Classical.choice, Quot.sound]`; no `sorry`, no new axiom.
So **R1/R2/R6's positive half is discharged and costs 139 lines.**  What they cannot do
is the second half, below.

## 4. The one remaining obligation, in its sharpest form

`UniversalGood` is *antitone*: coarsening preserves it (`universalGood_of_factor`), it
holds at the trivial factor (`relative_singularity_base`), and it fails at the top factor
(relative law `= delta_1`, and `1 in C = jHom.range`).  Also, ergodicity of the relative
product is *monotone upward* in the factor, so the tower supremum is the **coarsest**
factor that can possibly have ergodic relative product — no coarser choice exists.  It
is therefore the optimal, and the only, candidate.

Theorem A's hypothesis is used in exactly one place (`r = 0` forces `d` to be
`Y`-measurable), so it is equivalent to

> **Theorem A'.** `d` wild and `X x_Y X` ergodic implies: the relative difference law
> over `Y` is `C`-null, **or** `d` is `Y`-measurable.

And `UniversalGood` is consumed in the whole development at exactly one point,
`Ergodicity.lean:57`:

```lean
exact hgood id measurable_id (fun k => Eventually.of_forall (fun d => rfl)) (by simpa using hw)
```

— that is, only at `d = id`.  Hence the entire obligation is:

> **(O)** For `μ` a probability on `D`, `ErgodicSMul K D μ`, `IsWild μ`: the tower
> supremum factor of `(D, μ)` is **proper**, `sigma(p) != top`.  (Equivalently: `(D, μ)`
> is not a compact extension of the trivial factor; equivalently some bounded measurable
> `f` has non-precompact `K`-orbit in `L²(D, μ)`.)

(O) plus Theorem A for the single map `d = id` gives `exists_terminal_factor`, and
section 1's 5 161 lines go.  (O) is not a formal consequence of `IsWild` (which is only
`K`-invariance plus `μ C = 0`) — no existing lemma connects `C`-nullness to the Koopman
spectrum.

No join-closed maximality predicate supplies properness, which is why nothing cheaper
works:

| candidate `Good` | base | chain joins | compact successor | excludes top |
|---|---|---|---|---|
| `UniversalGood` (paper) | 248 decls | **681 decls** | free (`relative_singularity_successor`) | yes, by antitonicity |
| "`Tower` member" (R1/R2/R6) | free | free | free | **no** — contains top iff `X` is compact over the trivial factor |
| `d` not `p`-measurable | free | **no** — a join of proper factors can be top | **no** — `extend p H` can be top | yes |

Note that `Functions.lean` already has `compact_add`, `compact_mul`,
`compact_of_l2_approximation`, `compact_of_bounded_pointwise_limit`, `compact_iUnion` —
so the closed-subalgebra part of the compact structure theory is available.  Composition
of compact extensions is therefore *not* the obstacle; properness is.

## 5. Two dead ends, with reasons (do not repeat)

1. **Martingale/Levy shortcut for the chain join.**  `UniversalGood p` is *not* the
   conditional expectation of `1_{d(x)/d(x') in C}` on `sigma(p) (x) sigma(p)`; it asks
   for two conditionally independent draws with the **same** `p`-value, i.e. the
   restriction of that conditional expectation to the **diagonal** `y = y'`.  Diagonal
   restriction is not continuous in `L²`, so goodness does not transfer along a chain by
   Levy.
2. **Portmanteau / weak-convergence shortcut.**  `C` is deliberately only Borel
   (`Basic.lean:99`: *"The subgroup C is not replaced by its closure"*).  `C = j(R^2)` is
   `F_sigma`, not closed; for closed `F`, Portmanteau gives `μ(F) >= limsup μ_n(F)`, the
   useless direction, and `C` is not open.  This is why the finite-list/phase-collision
   induction is load-bearing.

## 6. Verdict per route

* **R1** (maximal compact extension): positive half **proved here, 145 lines, axiom
  clean**.  Negative half blocked on (O).  Total cost if (O) is supplied: +139, prize
  5 161.
* **R2** (transfinite/ordinal recursion): *strictly worse than R1*.  `SeparableZorn`
  already reduces arbitrary chains to countable ones and `ChainJoin` already codes
  countable joins, so ordinal machinery replaces ~90 lines of `CodedMax`/`SeparableZorn`
  and adds ordinal recursion; it inherits the same (O) blocker.
* **R5** (countable reduction): **already in the tree.**  `SeparableZorn.countable_cover`
  (Factors.lean:501) is exactly the countable reduction; there is nothing left to do.
  Empty route.
* **R6** (fixed point): identical to R1 — `Tower` *is* the least fixed point of
  "base / compact successor / countable join" and the maximality argument is Zorn on it.
  Same verdict, same blocker, no line difference.
* **R3** (hybrid): the only soft piece is `universalGood_of_factor` (coarsening), a
  mixture-of-`C`-null-measures argument provable directly — but it is 1 declaration out
  of 681, so it buys nothing alone.
* **R7** (fat trim): the 5 161 lines are *not* trimmable today — both propagation
  theorems reach them.  Independent trimming is the only route that does not need (O).
  Available mechanical fat for a quick win: 538 duplicate `open`/`open scoped` lines
  (971 exist; only the first occurrence per file is load-bearing).

## 7. Independent measurement of the fallback (R7 dead weight): 1 312, not 1 771

`sprint/simplify/m15/reach3.py` is a second, independent tool: it strips comments and
docstrings *before* extracting mentions (a comment naming a lemma otherwise fakes
reachability) and expands qualified names on dot suffixes.

```
dead:                               184 decls / 1 312 declaration lines
  instance or @[...]-attributed:     52 decls /   191 lines   (UNSAFE: simp/instance
                                                              use is invisible to a
                                                              name-based scan)
  plain:                            132 decls / 1 121 lines
```

Largest plain items: `PhaseCollision.collision_from_close_encodings` 67,
`ConditionalLimits.relative_singularity_limit` 62, `ConditionalLimits.
finite_encoding_at_of_approximation` 51, `MeasurableAssembly.
exists_measurable_unit_distance_coloring_of_center_cover` 48, `FourContinuity.
strict_state_uniform_on_compact` 46, `BoundaryTrace.unit_antipodes_of_no_positive` 40,
`Compactness.sampling_weak_compact` 29, `ConnectedUnitFree.
diam_le_one_of_preconnected_unitFree` 27.

So R7 alone reaches ~1 121 lines on this count, not 1 500; the floor is cleared only by
R7 together with the R1-specific 3 453 (gated on (O)).  The 460-line gap with m12's
budget needs a build to settle.
