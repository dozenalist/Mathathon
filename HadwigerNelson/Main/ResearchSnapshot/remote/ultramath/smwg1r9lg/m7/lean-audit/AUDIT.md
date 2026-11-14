# Statement audit of the four cited Lean cores, and defect list

Swarm `smwg1r9lg`, member m7, direction d8.  Companion to `CERTIFICATE.md` (commands, exit
statuses, axiom listings, sharpness runs).  Every claim below was checked against the file's
own text and against a run in this session.

## 0. Verdict

* **4/4 files compile from scratch on Lean 4.34.1 + the pinned Mathlib** (`source
  scripts/env4341.sh`), exit 0, no `sorryAx`, no user axioms; the axiom sets are exactly those
  the record reports (three printed declarations in each of `repair31.lean`, `frozen_core.lean`,
  `count_lemma.lean`, seven in `check_engine.lean`).
* **Every theorem's statement matches what the file itself says it proves**, and matches the
  record's *itemised* claims about it.  The four files are honest and each is explicit about
  what it does not formalise.
* **The defects are in the record's bookkeeping, not in its mathematics**: one recorded
  command that cannot work (D1), three over-attributions of "machine-checked" (D2, D3, D8),
  two scope compressions (D4, D7), one broken file path (D5) and one documentational
  biconditional that is false (D6).  None changes a mathematical conclusion.  All are listed
  in §2 with a proof or an explicit witness and a fix.
* **New in this audit**: five sharpness theorems (`m7_sharpness.lean`,
  `m7_cover_radius.lean`) showing that none of the four cores is vacuously weak and that the
  engine's radius constant is essential, and an exact census of sector fields
  (`indep_check.py`) which exhibits the two-valued→three-valued wall of `REPORT.md` §5c as a
  finite, machine-checked fact.

## 1. Statement by statement

### 1.1 `smwfo9zkl/m9/k6_s7_engine.lean` (+ `check_engine.lean`)

| record's claim | what the file states | verdict |
|---|---|---|
| "the combinatorial core is machine-checked for an arbitrary finite label type" (`REPORT.md` §0, §2) | `graph_map_large_positive_generic : ∀ {V : Type u_1} [Fintype V] (F : C(↑(closedBall 0 5), GraphSpace ⊤)), ∃ i K, IsPreconnected K ∧ K ⊆ closedBall 0 5 ∧ (∀ z ∈ K, 0 < F z i) ∧ ∃ x ∈ K, ∃ y ∈ K, 2 < dist x y` | **match**; `V` arbitrary, only `[Fintype]` |
| `card_le_two_of_isClique_of_acyclic` is the conversion step | `{V : Type*} {G : SimpleGraph V} → G.IsAcyclic → {s : Finset V} → (∀ i ∈ s, ∀ j ∈ s, i ≠ j → G.Adj i j) → s.card ≤ 2` | **match**, and slightly stronger than claimed: no `[Fintype V]` at all |
| "`alpha < 1/6` exactly optimal for the printed argument"; "the denominator is `Σ(p_i − α)_+ ≥ 1 − 6α > 0`" | `K6.thresholdTotal_pos` assumes `hα : α < 1/6` and proves `0 < Σ_i max (p_i − α) 0` from `Σ p_i = 1` | **match** for the estimate: `1 − kα` vanishes exactly at `α = 1/k` (checked exactly, `k = 5, 6`) |
| "all seven declarations depending only on `[propext, Classical.choice, Quot.sound]`" | exactly seven `#print axioms` lines, exactly that set | **match** |
| no machine-checking is claimed for `(W)` itself | the engine contains no `(W)`, no `L`, no `L_0` | consistent: `(W)` is used in the paper-level extraction only |

### 1.2 `smwfwi7rh/m8/lean/repair31.lean`

| record's claim | what the file states | verdict |
|---|---|---|
| `no_proper_two_colouring` on `[propext, Classical.choice, Quot.sound]` | `∀ f : ℂ → Fin 2, (∀ p q, ‖p−q‖ = 1 → f p ≠ f q) → False` | **match** (it is the 3-point pigeonhole on the triangle `λ ω^j`, i.e. the *last* step of Lemma 6.4-type arguments; see D2) |
| `rigidity` on the same axioms | `normSq v = 1 → normSq (1+v) = 1/3 → v.re = -5/6` | **match** |
| `no_two_valued_sector_field` on `[propext, Quot.sound]` | `∀ n m (V : ZMod n → Bool), (∀ i, V (i+m) = !V i) → (∀ i, V (i+m+1) = !V i) → (∀ i, V (i+m−1) = !V i) → False` | **match**; the proof uses the `+1` hypothesis only, as the file says |
| `m8`'s own §8: "the sets `E, A_0, G` of R1 are **not** formalised" | true: zero occurrences of `Measure`, `volume`, `NullMeasurableSet`, `aemeasurable`, `EqOn`, `A_0`, `arcsin` in the file | **match** — but the record's ledger says otherwise, see **D2** |

### 1.3 `smwfwi7rh/m11/frozen_core.lean`

| record's claim | what the file states | verdict |
|---|---|---|
| "`union_eq_of_three_disjoint`, `not_disjoint_fourth`, `exists_card_le_one_of_free_label` on `[propext, Classical.choice, Quot.sound]`" (`STATUS.md`) | exactly these three, exactly these axioms | **match** |
| "the finite combinatorial core of the frozen-field obstruction" | three pigeonhole lemmas about three pairwise disjoint palettes of size `≥ 2` in a 6-set | **match** as a finite core; it contains no palette field, no (5.3), no measure — as its own header says |
| ledger: "frozen fields satisfy `(5.3)` at separation 1 only with `P(f) = empty`; **Lean-checked core** (`m11`)" | the file proves no such thing about separation 1 | **misattribution**, see **D3** |
| m11 `RESULTS.md` line 386: built with "stock `lean` 4.33.1 with `/opt/mathlib`" | re-run on 4.34.1: exit 0, same axioms | **upgraded**: now pinned-toolchain verified |

### 1.4 `smwfwznwk/m4/count_lemma.lean`

| record's claim | what the file states | verdict |
|---|---|---|
| "at a unit triangle `2+2+2 > 5` (`smwfwznwk` m4, Lean-checked)" (ledger), "Lean-checked `count_lemma.lean`" (§9) | `card_three_disjoint_le : (U.card = 5) → A,B,C ⊆ U → pairwise disjoint → A.card + B.card + C.card ≤ 5`; `no_free_label_triangle : (i0 : Fin 6) → A,B,C ⊆ univ.erase i0 → pairwise disjoint → 2 ≤ A.card, B.card, C.card → False`; `admissible_card_ge_two` | **match**; the three declarations are exactly the counting step |
| `FREE-LABEL.md`: "machine-checked in `work/count_lemma.lean`" | the file is at `m4/count_lemma.lean`; `m4/work/` contains only `paper.txt` | **broken pointer**, see **D5** |
| (implied by the use) the pairwise disjointness of the three palettes at a unit triangle | not formalised: it comes from the paper's (5.3)/(TE) at Remark 5.3's instance | correct as a citation, not claimed otherwise |

## 2. Defect list

**D1 (operational; the recorded command does not work).**
`REPORT.md` §2 records the engine check as `source scripts/env4341.sh; cd
.ultramath/smwfo9zkl/m9; lean check_engine.lean`.  Run verbatim, this fails:

```
check_engine.lean:1:0: error: unknown module prefix 'k6_s7_engine'
No directory 'k6_s7_engine' or file 'k6_s7_engine.olean' in the search path entries: ...
```

*Proof of the gap.*  Lean 4 resolves imports only along `LEAN_PATH`; the working directory is
not on it (`env4341.sh` does not add `.`), and `lean f.lean` writes no `.olean` at all, so the
stale `k6_s7_engine.olean` present in that directory is not rebuilt and is not found either.
Both defects are real and independent: in a clean directory I ran the recipe in three steps —
`lean -o k6_s7_engine.olean k6_s7_engine.lean` (exit 0), then the recorded
`lean check_engine.lean` (**exit 1**, same message), then
`LEAN_PATH=".:$LEAN_PATH" lean check_engine.lean` (exit 0).
*Fix*, and the recipe I actually ran:

```
lean -o k6_s7_engine.olean k6_s7_engine.lean     # exit 0, 3.21 s
LEAN_PATH=".:$LEAN_PATH" lean check_engine.lean  # exit 0, 2.45 s
```

This correct two-line recipe is already printed in
`.ultramath/smwfo9zkl/m9/s7_k6_transfer.md` §9; the report should cite it, not the one-liner.

**D2 (over-attribution, the substantive one).**
Ledger line `REPORT.md:810` says: "`m16`'s Corollary 3.1 … **not established**; repaired to the
confined form R1 (`m8`, **Lean-checked**)", and line 885 lists "confined alternation R1 … Lean-checked".
*The gap, proved by exhaustive search of the file's syntax.*  R1's statement quantifies over a
measurable set `E ⊆ S¹`, a measurable `A_0 ⊆ E` with `1_{A_0}(t+κ) = 1 − 1_{A_0}(t)` a.e. on
`E ∩ (E−κ)`, and concludes that an explicitly defined set of `t` is null.  `repair31.lean`
contains **no** occurrence of `Measure`, `volume`, `NullMeasurableSet`, `aemeasurable`, `EqOn`,
`A_0` or `arcsin` (its three quantifier-free `E`, `kappa`, `gamma_0` hits are prose in comments),
and it declares exactly 4 definitions, 15 lemmas and 4 theorems (listed by `grep -n
"^theorem\|^lemma\|^def"`), all summarised in §1.2.  A file
with no measure theory cannot imply a null-set statement; m8 says so itself in its own §8.
*Fix.*  Write: "R1 is a paper-level statement; its three finite ingredients — the forced
triangle `λ ω^j` with pairwise unit distances, the shift rigidity `Re v = −5/6`, and the
two-valued sector no-go — are Lean-checked (`no_proper_two_colouring`, `rigidity`,
`no_two_valued_sector_field`)."  Nothing else in §4c of the report needs changing: the
itemised list there is accurate.

**D3 (misattribution).**  Ledger line `REPORT.md:807` pairs the statement "frozen fields
satisfy `(5.3)` at separation 1 only with `P(f) = empty`" with "Lean-checked core (`m11`)".
*The gap.*  For a centre-independent field every instance of (TE) reads `P(f) ∩ P(f) = ∅`,
because both palettes in the statement are the same frozen value `P(f)` — the coincidence is in
the *centres*, not in the directions.  So the separation-`1` conclusion `P(f) = ∅` is immediate
and needs no combinatorial input.  What `frozen_core.lean`
actually supports is `RESULTS.md`'s Lemma C and, through it, Theorems C and D — the exclusions
at the *intermediate* distances `d ≥ 0.4609` and `d ≥ 0.3044`.
*Fix.*  Move the Lean attribution to Theorems C/D; the `d = 1` statement needs only (TE).

**D4 (scope of "the combinatorial core is machine-checked").**
`REPORT.md` §0/§2 and ledger line 772 say "the combinatorial core is machine-checked".  What
is machine-checked is: (i) clique-in-a-forest `≤ 2`, label-type arbitrary; (ii) the
multiplicity-two cover obstruction; (iii) the `α < 1/6` threshold algebra at six labels.
Not machine-checked: Lemmas 7.2 and 7.3 (the Fourier-decay and Definition 1.2 inputs) and
Lemmas 7.7 (reduced circuits) and 7.8 (annular crossing), which the record itself calls "pure
topology on a finite connected simple graph".  Also, the cover obstruction
that is formalised is the **instance** radius `5`, diameter `≤ 2` (`PlanarCovers.lean`:
`compact_open_cover_impossible` takes `Metric.ball (0:ℂ) 5 ⊆ Q`; `hit_center_subtype` uses
`Metric.ball y 4 ⊆ Q` with displacement `≤ 2`), not a scale-invariant "inradius > mesh"
statement; that sharpening is `m5`'s paper-level result, and the report correctly attributes it
to `m5`.
*Fix.*  Say "the conversion step, the cover obstruction at one instance of its constants, and
the `1 − 6α` algebra are machine-checked; Lemmas 7.2, 7.3, 7.7, 7.8 are paper-level."
Quantitatively (new, `m7_cover_radius.lean`): the instance is radius `5` with diameter bound
`2`; the radius cannot be lowered to `≤ 1` because there the mesh hypothesis is automatic
(checked: exit 0, standard axioms), while the sharp form for `(W)`'s `R > 1` is radius `> 2` in
these units.  The slack comes from `hit_center`, which hardwires radius `4` and displacement `2`
instead of being parametric; it is a formalisation gap, not a mathematical one.

**D5 (broken pointer).**  `sprint/k6/FREE-LABEL.md` line 26 cites `work/count_lemma.lean`.
The file is `.ultramath/smwfwznwk/m4/count_lemma.lean`; `.ultramath/smwfwznwk/m4/work/`
contains only `paper.txt`.  *Fix*: correct the path.

**D6 (documentational biconditional that is false).**  `k6_s7_engine.lean` comments on
`thresholdTotal_pos`: "`α < 1/6` is exactly what positivity of the denominator needs at six
labels".  Positivity is not equivalent to `α < 1/6`.  With the profile
`p = (1/6,…,1/6)` (realised by a measurable colouring constant on six equal sectors through
the centre, so that every `diskAverage` equals `1/6`) one has `Σ(p_i − α)_+ = 0` at `α = 1/6`;
with a constant colouring, `p = (1,0,…,0)` and `Σ = 5/6 > 0` at the same `α`.  The *theorem*
is unaffected and is sharp as a uniform implication (the estimate `1 − 6α` cannot be made
positive at `α = 1/6`).  *Fix*: "exactly what this estimate needs".

**D7 (adjacent, ledger compression; not one of the four files).**  Ledger line `REPORT.md:787`
says "local finiteness at `k = 5` | true (paper, machine-checked)".  I printed the machine-checked
statement (`check_exclusion.lean`, exit 0, 40.6 s):

```
EuclideanFiveColor.no_five_exclusion_continua : ∀ (c : ℂ → Fin 5), Measurable c →
  WeakColoring 5 c → ∀ {x} {K : Fin 5 → Set ℂ} {v : Fin 5 → ℂ}, (∀ i, ‖v i‖ = 1) →
  (∀ i, ApproachingContinuum x (K i) (v i)) →
  (∀ i, Disjoint (spatialSupport c i) (Straddle (K i)) ∧
        Disjoint (spatialSupport c (i+1)) (Straddle (K i))) → False
```

axioms `[propext, Classical.choice, Quot.sound]`.  This is the five-cycle endgame *given* the
§7 data; local finiteness at `k = 5` additionally needs the extraction and the `ℓ = 3, 4`
cases.  The report itself says exactly this in §4d ("it takes the §7 output as a hypothesis
and its own comment says it does not assert that the data have been extracted"), so the ledger
line is a compression, not a falsehood.

**D8 (unlocatable attribution, adjacent).**  Ledger line `REPORT.md:780` says "ternary palettes
occupy at most half the direction circle | proved, sharp (`m11`; **machine-checked**)".  m11's
directory contains exactly one Lean file, `frozen_core.lean`, whose three theorems are the
finite pigeonhole of §1.3, and m11's `RESULTS.md` attributes Lean to that file only.  No path is
given for a Lean proof of `σ{T ⊆ P_x} ≤ 1/2`, and I did not find one; as cited the claim is not
reproducible from m11's directory.  Either the citation should name the file or the word
"machine-checked" should be dropped (the statement may well be true — that is not in question
here).  For contrast, the two statements of §5b (`pair_transition_not_null`,
`exists_unit_pair_of_pair`) are locatable at `.ultramath/smwfo9zkl/m4/lean/` and I did re-run
them, from copies, on 4.34.1: `MergeSix.lean` exit 0 (83.9 s) and `MergeSixK6.lean` exit 0
(19.5 s), each printing its declarations on `[propext, Classical.choice, Quot.sound]` — so
*that* attribution in the record is sound.

## 3. What is *not* machine-checked (the honest boundary)

For anyone relying on the record, these are paper-level and must be re-audited as mathematics:

1. **§7 Lemmas 7.2, 7.3** (Definition 1.2, Lemma 4.3, Fourier decay (6.3) of circle measure).
   The analytic inputs they encode are declared label-generically in the Lean sources, which I
   checked mechanically: `diskAverage_unit_pair`, `diskAverage_support_exclusion`,
   `continuum_limit_support_exclusion` are all declared `{k : ℕ} {c : ℂ → Fin k}`
   (`DiskAverages.lean:63`, `ContinuumLimits.lean:98`, `:200`).
2. **§7 Lemmas 7.7, 7.8** (reduced circuits, annular crossing).  No Lean artefact for either.
3. **The sharpened scale-invariant cover lemma** (inradius > mesh), `m5`'s sharpening.  The
   formalised instance has one unit of slack over what its own hitting lemma needs
   (`4` vs `2 + 1`).
4. **(TE)** from (5.3) at Remark 5.3's instance; pairwise disjointness of the three palettes at
   a unit triangle; the palette bound `|P| ≤ k − 3`.  All cited, none formalised.
5. **m11's shift set** (Lemma 4.1, Lemma 4.2: `delta_min`, `M(d)` by 40-digit numerics).  The
   Lean core starts *after* this: given `δ, 2δ, 3δ ∈ Sh(d)`, the finite pigeonhole applies.
6. **R1 itself** (D2), and the fact that `P_x(e) = F(x+e)` is a *maximal* palette field.

## 4. Non-vacuity and sharpness (new results of this audit)

`m7_sharpness.lean`, exit 0, 0.71 s, all four theorems on
`[propext, Classical.choice, Quot.sound]`:

| theorem | what it refutes |
|---|---|
| `clique_le_two_sharp` | `(⊤ : SimpleGraph (Fin 3))` is not acyclic and carries a 3-clique: acyclicity in the conversion step cannot be dropped |
| `union_eq_three_disjoint_sharp` | `{0}, {1}, {2}` are pairwise disjoint in a 6-set and do not exhaust it: the size-`≥2` hypothesis in the frozen-field core is essential |
| `no_free_label_triangle_sharp` | `{0,1}, {2,3}, {4,5}` in `[6]`: the absent-label hypothesis in the free-label counting step is essential |
| `sector_two_valued_is_sharp` | at `n = 6`, `m = 1`, `V i = i mod 3` satisfies `V(i+m) ≠ V i` and `V(i+m+1) ≠ V i`: the sector no-go is *exactly* two-valued |

The last one is the finite form of the sprint's central `§5c` statement, and the exact census
in `indep_check.py` (two independent algorithms, exhaustive at `n = 6` and `n = 12`) makes it
quantitative: the number of `r`-valued sector fields on `n = 6m` positions satisfying (5.7)
and the transport is

| n | 6 | 12 | 18 | 24 | 30 | 36 |
|---|---|---|---|---|---|---|
| 2 values | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 values | 6 | 12 | 30 | 4398 | 130020 | 2793606 |

so the hypothesis class of `no_two_valued_sector_field` is empty, its three-valued analogue is
non-empty at every resolution, and the six solutions at `n = 6` are exactly the permutations of
`i mod 3` — the free-label block words of `FREE-LABEL.md`, recovered independently.

`indep_check.py` also re-derives, in exact integer arithmetic without Lean, the finite content
of the other three cores (90 exhaustiveness triples, 0 fourth-palette escapes, 0 free-label
escapes; no three pairwise disjoint 2-sets in a 5-set; no admissible singleton for `C_6`), and
the `repair31` geometry in `Q(√3, √11)` including the identity
`cos(2 arcsin(1/(2√3))) = 5/6`, `sin(...) = √11/6` and the uniqueness of `Re v = −5/6`.

**A fifth sharpness test: the engine's radius.**  `m7_cover_radius.lean` (exit 0, 8.57 s,
`M7Radius.cover_radius_le_one_vacuous` and `..._one_vacuous` on
`[propext, Classical.choice, Quot.sound]`) exhibits, for every `r ≤ 1`, a continuous
graph-valued map of the closed disk of radius `r` all of whose positive-coordinate preconnected
subsets have diameter `≤ 2`.  So the mesh hypothesis of the engine is automatic at radius `≤ 1`
and the obstruction cannot hold there: the engine's radius is essential, and the "`R > 1`" of
hypothesis `(W)` is the same constant.  This is the one place where the machine-checked layer
is *not* sharp — the formalised instance uses radius `5`, whereas the sharp form of the same
winding-number argument is radius `> 2` in these units (see D4).
