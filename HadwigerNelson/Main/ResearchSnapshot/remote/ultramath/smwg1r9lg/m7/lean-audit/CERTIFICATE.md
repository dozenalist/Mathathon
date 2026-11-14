# Certificate: from-scratch recomputation of the four cited Lean cores

Swarm `smwg1r9lg`, member m7, direction d8.  Everything below was produced in this session,
in `.ultramath/smwg1r9lg/m7/lean-audit/`, from **copies** of the four files.  No file outside
this directory was modified; the copies are byte-identical to the originals (md5 table below),
so the audit is of the real artefacts.

## Toolchain

```
source scripts/env4341.sh
lean --version
Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)
```

`scripts/env4341.sh` sets `PATH` to `<repo>/.scratch/toolchain/bin` and

```
LEAN_PATH = <repo>/lean/build/lib          (OAI development, prebuilt)
          : <repo>/.scratch/toolchain/lib/lean
          : <repo>/.scratch/mathlib4/.lake/build/lib/lean  (+ every vendored package)
```

For comparison the *default* `lean` on `PATH` is 4.33.1; every number below is 4.34.1.

## Copies audited (byte-identical to the originals)

| file | md5 (copy = original) |
|---|---|
| `k6_s7_engine.lean` (smwfo9zkl/m9) | `9119c13fb808fd4e8ca01b8700c70059` |
| `check_engine.lean`   (smwfo9zkl/m9) | `eac3821102697a983bfa9ba4b4297d9b` |
| `repair31.lean`    (smwfwi7rh/m8) | `2a3779f5130d4dbc99e8458b6ab69f54` |
| `frozen_core.lean` (smwfwi7rh/m11) | `d66c4ece018cc73ae197aebe2c5b1653` |
| `count_lemma.lean` (smwfwznwk/m4) | `e75ba1217ba8e49145f66cb41b919d09` |

## Runs

### 1. The §7 engine (two commands are needed)

```
lean -o k6_s7_engine.olean k6_s7_engine.lean        # exit 0, 3.21 s
LEAN_PATH=".:$LEAN_PATH" lean check_engine.lean     # exit 0, 2.45 s
```

Seven declarations, all on `[propext, Classical.choice, Quot.sound]` (output reflowed to one
line each; the original wraps the second declaration across three lines):

```
'OAI.EuclideanFiveColor.k6_graph_map_large_positive' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.k6_card_le_two_of_isClique_of_acyclic' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.graphRealization_positive_two' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.graph_map_large_positive_generic' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.K6.thresholdTotal_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.K6.thresholdMap_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.K6.threshold_support_card_le_two' depends on axioms: [propext, Classical.choice, Quot.sound]
```

and the two `#check`ed types, printed verbatim, which are the statement audit:

```
@graph_map_large_positive_generic : ∀ {V : Type u_1} [Fintype V] (F : C(↑(Metric.closedBall 0 5), GraphSpace ⊤)),
  ∃ i K, IsPreconnected K ∧ K ⊆ Metric.closedBall 0 5 ∧
      (∀ (z : ↑(Metric.closedBall 0 5)), ↑z ∈ K → 0 < ↑(F z) i) ∧ ∃ x ∈ K, ∃ y ∈ K, 2 < dist x y
@K6.threshold_support_card_le_two : ∀ {c : ℂ → Fin 6} {ε α : ℝ} {G : SimpleGraph (Fin 6)},
  G.IsAcyclic → ∀ (q : ℂ),
      (∀ (i : Fin 6), α < diskAverage c ε i q → ∀ (j : Fin 6), α < diskAverage c ε j q → i ≠ j → G.Adj i j) →
        {i | α < diskAverage c ε i q}.card ≤ 2
```

**The command recorded in `sprint/k6/REPORT.md` §2 does not work.**  Running exactly
`cd .ultramath/smwfo9zkl/m9; lean check_engine.lean` gives

```
check_engine.lean:1:0: error: unknown module prefix 'k6_s7_engine'
No directory 'k6_s7_engine' or file 'k6_s7_engine.olean' in the search path entries: ...
```

because Lean 4 never searches the working directory for imports, and `lean f.lean` writes no
`.olean` (so the stale `k6_s7_engine.olean` in that directory is required unless one passes
`-o`).  Both halves of that sentence are needed: in a clean directory, after `lean -o
k6_s7_engine.olean k6_s7_engine.lean` has succeeded, the recorded one-liner still exits 1 with
the same message, and only `LEAN_PATH=".:$LEAN_PATH"` makes it exit 0.  The two-command recipe
above is the one printed correctly in
`.ultramath/smwfo9zkl/m9/s7_k6_transfer.md` §9, and it reproduces: my rebuilt olean is
430264 bytes, the same size as the one on disk.

### 2. `repair31.lean`

```
lean repair31.lean        # exit 0, 1.16 s
'Repair31.no_proper_two_colouring' depends on axioms: [propext, Classical.choice, Quot.sound]
'Repair31.rigidity' depends on axioms: [propext, Classical.choice, Quot.sound]
'Repair31.no_two_valued_sector_field' depends on axioms: [propext, Quot.sound]
```

Exactly the three statements and exactly the axiom sets in `REPORT.md` §4c and in
`.ultramath/smwfwi7rh/m8/REPORT.md` §8.

### 3. `frozen_core.lean`

```
lean frozen_core.lean     # exit 0, 0.70 s
'union_eq_of_three_disjoint' depends on axioms: [propext, Classical.choice, Quot.sound]
'not_disjoint_fourth' depends on axioms: [propext, Classical.choice, Quot.sound]
'exists_card_le_one_of_free_label' depends on axioms: [propext, Classical.choice, Quot.sound]
```

(one deprecation *warning* on `push_neg`, not an error).  Matches `STATUS.md`.  Note that
m11's own `RESULTS.md` line 386 says this file was built with "stock `lean` 4.33.1 with
`/opt/mathlib`"; the run above puts it on the pinned 4.34.1 toolchain for the first time.

### 4. `count_lemma.lean`

```
lean count_lemma.lean     # exit 0, 0.55 s
'card_three_disjoint_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'no_free_label_triangle' depends on axioms: [propext, Classical.choice, Quot.sound]
'admissible_card_ge_two' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### 5. New: sharpness certificates (`m7_sharpness.lean`, written for this audit)

```
lean m7_sharpness.lean    # exit 0, 0.71 s
'clique_le_two_sharp' depends on axioms: [propext, Classical.choice, Quot.sound]
'union_eq_three_disjoint_sharp' depends on axioms: [propext, Classical.choice, Quot.sound]
'no_free_label_triangle_sharp' depends on axioms: [propext, Classical.choice, Quot.sound]
'sector_two_valued_is_sharp' depends on axioms: [propext, Classical.choice, Quot.sound]
```

What they say (each is the *failure* of the audited core when its load-bearing hypothesis is
dropped, i.e. the core is not vacuously weak):

| theorem | content |
|---|---|
| `clique_le_two_sharp` | the complete graph on three labels has a 3-clique and is not acyclic, so acyclicity in `card_le_two_of_isClique_of_acyclic` cannot be dropped |
| `union_eq_three_disjoint_sharp` | three *singleton* palettes in `[6]` are pairwise disjoint and do not exhaust it, so the hypothesis `A.card ≥ 2` in `union_eq_of_three_disjoint` is doing the work |
| `no_free_label_triangle_sharp` | in `[6]` (no free label) three pairwise disjoint 2-palettes exist, so the absent label is what makes `no_free_label_triangle` true |
| `sector_two_valued_is_sharp` | at `n = 6`, `m = 1`, the **three-valued** field `V i = i mod 3` satisfies `V (i+m) ≠ V i` and `V (i+m+1) ≠ V i`: `no_two_valued_sector_field` is exactly a two-valued statement |

### 5b. New: the radius constant of the cover obstruction is essential (`m7_cover_radius.lean`)

```
lean m7_cover_radius.lean   # exit 0, 8.57 s
'M7Radius.cover_radius_le_one_vacuous' depends on axioms: [propext, Classical.choice, Quot.sound]
'M7Radius.cover_radius_one_vacuous' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`cover_radius_le_one_vacuous (r : ℝ) (hr1 : r ≤ 1)` produces an explicit continuous
graph-valued map of the closed disk of radius `r` — every positive-coordinate preconnected
subset of which has diameter `≤ 2` — i.e. a point satisfying the mesh hypothesis of
`graph_map_small_mesh_impossible_generic`.  Hence the obstruction genuinely needs a disk of
radius `> 1` in the normalisation where the diameter bound is `2`: the mesh hypothesis is
*automatic* for every graph-valued map on such a disk, so the theorem's radius cannot be
lowered.  (The proof needs nothing about the map: the whole disk has diameter `2r ≤ 2`.)

This is the audit answer to "is the engine's radius vacuous?": no, and it fails below 1.  It
also locates the formalisation gap precisely.  `PlanarCovers.hit_center` is stated with the
numbers `4` (radius of the ball around the target) and `2` (displacement) hardwired, which is
what forces `ball(0,5) ⊆ Q` at the level of the engine; the sharp form of the same winding-number
argument would be parametric, giving *inradius > diameter bound*, i.e. radius `> 2` in these
units — exactly the normalised form of `(W)`'s `R > 1`.  The formalised instance therefore
holds with slack, and re-running it at the sharp constant would require re-proving `hit_center`
with parameters.

### 5c. Adjacent: the two §5b label-merging statements (outside the four cores)

`REPORT.md` §5b also claims `pair_transition_not_null` and `exists_unit_pair_of_pair` are
machine-checked.  They are locatable at `.ultramath/smwfo9zkl/m4/lean/`, and I re-ran both from
copies on 4.34.1:

```
lean MergeSix.lean        # exit 0, 83.92 s
  'OAI.EuclideanFiveColor.exists_unit_pair_of_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
lean MergeSixK6.lean      # exit 0, 19.53 s
  'OAI.EuclideanFiveColor.exists_unit_pair_of_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
  'OAI.EuclideanFiveColor.pair_transition_not_null' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### 6. Independent non-Lean check (`indep_check.py`, exact arithmetic, no floats)

```
python3 indep_check.py    # exit 0, 34.57 s, "ALL ASSERTIONS HOLD"
```

* `frozen_core`: all 90 ordered triples of pairwise disjoint subsets of `[6]` with all sizes
  `≥ 2` exhaust `[6]`; no nonempty fourth palette is disjoint from all three; the free-label
  form has no counterexample; and the singleton triple `{0},{1},{2}` fails to exhaust.
* `count_lemma`: no three pairwise disjoint 2-subsets of a 5-set; no subset of `[6]` contained
  in no edge `{i,i+1}` of `C_6` has size `< 2`; the three 2-sets `{0,1},{2,3},{4,5}` are a
  sharpness witness.
* `repair31` geometry in `Q(√3,√11)` (sympy, symbolic): `|u| = |ω| = |1+ω| = 1`,
  `|1-u|² = 1/3`, `|1-ω|² = 3`, `ω³ = 1`, the three points `λ ω^j` are pairwise at distance
  exactly 1 with `|λ ω^j|² = 1/3`, and `2 arcsin(1/(2√3))` has `cos = 5/6`, `sin = √11/6`.
  The rigidity equation `|v| = 1 ∧ |1+v|² = 1/3` has the unique solution `Re v = -5/6`.
* sector fields, two independent algorithms (exhaustive enumeration and backtracking
  colouring count), `n = 6m`, `m = 1..6`:

  | n | 6 | 12 | 18 | 24 | 30 | 36 |
  |---|---|---|---|---|---|---|
  | 2-valued solutions of (5.7)+transport | 0 | 0 | 0 | 0 | 0 | 0 |
  | 3-valued solutions | 6 | 12 | 30 | 4398 | 130020 | 2793606 |

  At `n = 6` the exhaustive and the backtracking counts agree (6 and 0) and the six solutions
  are exactly the permutations of `V i = i mod 3` — so the sector obstruction is precisely the
  two-valued wall of `REPORT.md` §5c, with the first non-empty stratum at three values.
* engine arithmetic: the printed estimate `Σ(p_i - α)_+ ≥ 1 - kα` has its zero exactly at
  `α = 1/k` (`1/5` at five labels, `1/6` at six), so `α < 1/6` is the sharp hypothesis for that
  estimate; and the cover obstruction's numbers are `ball radius 5`, `diameter ≤ 2`,
  hitting radius `1`, i.e. `5 > 2 + 1`.

## What this certificate does not claim

It certifies compilation, statements and axioms; it does not certify that the surrounding
mathematical arguments are complete.  See `AUDIT.md` for the exact scope of every claim and
the defect list.
