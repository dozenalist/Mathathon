# simplify-verification, block 1: the §7 connected-set exclusion, and the m6 trim

Scope: one block.  I read `README.md`, `results/VERIFICATION.md`, `results/K6-BARRIER.md` (§7 part),
`sprint/simplify/REPORT.md`, `sprint/simplify/m6/*` and `sprint/simplify/m14/CUT-PREREQ.md`, then
did two independent checks.  Nothing outside `supervisor/simplify-verification/` was modified.

Grades used below: **[MC]** machine-checked here in this block, in the pinned environment
(Lean 4.34.1 + mathlib `d13f23b`, `scripts/env4341.sh`); **[TXT]** exact textual/mechanical
analysis, reproducible by script, no proof assistant; **[PAPER]** paper-level argument only.

---

## 1. What I verified first-hand, and what I only read

`results/VERIFICATION.md` makes four kinds of claim.  I did not re-run the 78-module build
(expensive, and `scripts/build4341.log` already records it); I checked the parts that a small
targeted computation settles.

| claim in VERIFICATION.md | my status |
|---|---|
| 78/78 modules compile under 4.34.1; axiom certificate on six roots | prior report, not re-run here |
| `ProperColoring k c := ∀ x y, ‖x−y‖ = 1 → c x ≠ c y` — the paper's Definition, no regularity | read in `lean/OAI/.../Basic.lean`; consistent [TXT] |
| "The connected-set exclusion of §7 is pure connectedness … Machine-checked (`ConnectedUnitFree.lean`)" | **true as stated, but weaker than it reads**: the module is *standalone* — its three theorems have **no consumer anywhere in the tree** (`rg` over `lean/` finds only the module itself and `results/lean/Check4.lean`, an axiom-printing certificate).  So "§7 exclusion formalised" means "a faithful lemma exists", not "the paper's §7 is wired into the lower-bound proof". [TXT] |
| seven-colouring constants, Moser certificate | prior report, not re-run |

Two statement-level points about `ConnectedUnitFree.lean` that the file's own docstring half-admits:

* its `diam_le_one_of_preconnected_unitFree` concludes `‖x − y‖ ≤ 1`, but under its own hypothesis
  (`‖x − y‖ ≠ 1` on `C × C`) the value `1` is **never attained**, and the intermediate value theorem
  gives the strictly stronger `‖x − y‖ < 1`.  As written the `≤` invites a reader to think the
  equality case is live.
* the proof routes through the product set `C × C` (`hC.prod hC`, `Icc_subset`); that is not needed.

## 2. The paper's use, checked against the rendered page

`attachments/here-are-three-files-ni5n/paper.pdf`, p. 42, eq. (7.1) (checked on a `pdftoppm`
render, not `pdftotext`):

  Δ(K) = { z ∈ R² : min_{q∈K} |z − q| < 1 < max_{q∈K} |z − q| }   for nonempty compact K,
  "Connectedness of K implies that every point of Δ(K) is at unit distance from a point of K."

The Lean lemma `not_straddle_of_isPreconnected` is exactly that sentence, in the form
`¬ (∃ q ∈ C, ‖z − q‖ < 1) ∧ (∃ q ∈ C, 1 < ‖z − q‖)` — i.e. `z ∉ Δ(C)`.  It is *stronger* than the
paper's use in three inessential ways (no compactness, no nonemptiness, any normed space), and the
`min`/`max` in (7.1) are not needed: only the two existential comparisons are used.  So a paper
simplification is available at no cost: (7.1) may be stated for an arbitrary `K` as
`{z : ∃q∈K, |z−q| < 1} ∩ {z : ∃q∈K, |z−q| > 1}`, and compactness of `K` becomes a property needed
only later, not for the straddling mechanism. [PAPER + TXT]

## 3. Deliverable: one principle instead of two proofs

`lean/ConnectedSetExclusion.lean` (Mathlib only, nothing imported from the development):

* `preconnected_forall_lt_or_forall_gt` — **[MC]** *the* principle: for preconnected `C` and
  `ContinuousOn f C`, if `f` never takes the value `c` on `C` then `f < c` everywhere on `C` or
  `f > c` everywhere on `C`.  Axioms `[propext, Classical.choice, Quot.sound]`.
* `unitFree_not_straddle` — **[MC]** the paper's sentence, 8 lines from the principle.  Same
  statement as the tree's `not_straddle_of_isPreconnected`.  Axioms as above.
* `unitFree_pairwise_lt` — **[MC]** the tree's `diam_le_one_of_preconnected_unitFree` with the
  conclusion `< 1` (which implies it); proof avoids `C × C` entirely by applying the principle to
  the single function `y ↦ ‖x − y‖` and using `‖x − x‖ = 0 < 1`.  Axioms as above.
* `diam_le_one_of_preconnected_unitFree'` — **[MC]** the development's exact conclusion, one line.
* `unitFree_sharp` — **[MC]** *the bound cannot be improved*: for every `ε ∈ (0,1)` there is a
  preconnected unit-free set in `ℝ` with two points at distance exactly `1 − ε`
  (`C = (−1/2, 1/2)`, witnesses `±(1−ε)/2`).  Consequence: `diam ≤ 1` is sharp, and no future
  counting argument (including any §7 or k = 6 argument) may replace it by `diam ≤ 1 − ε`.
  This is the lemma I would most want on record, because it is exactly the kind of "make it
  strict and count" step a simplification would be tempted to take.

Net effect on the module: two separate IVT arguments (`C×C` + `Icc_subset`, and a second
single-variable one) become one principle plus two short corollaries; the sharper conclusion is
recovered; the sharpness limit is recorded.

## 4. m6's `trim.patch` (the current simplification worker's main artifact): fidelity audit

`sprint/simplify/m6/trim.patch`, 42 modules, 31277 → 30559 lines.  My checks [TXT], all
reproducible from the patch alone:

1. **It is deletion-only.**  718 deleted lines, **0 added lines**, 61 hunks.  Hence every surviving
   declaration in the tree keeps a *byte-identical* statement and proof: the trim **cannot** change
   a root statement, a hypothesis, or an axiom dependency.  (This is a stronger and cheaper
   guarantee than a rebuild gives.)
2. **What is deleted:** 74 declaration blocks — 58 `lemma`, 13 `theorem`, 3 `def`; no `instance`,
   `structure`, `class` or `inductive`, and no deleted line is an attribute line (`@[` count 0), so
   no `simp`/instance search can silently lose a rule.
3. **No dangling references.**  All 74 deleted names occur **0** times in the trimmed tree
   `sprint/simplify/m6/E1` (they occurred once, or in later rounds once their only consumer was
   itself removed).  The trimmed tree has the same 83-module set as `lean/OAI`, and none of the
   deleted names appears in `results/lean/Check{3,4,5}.lean`.
4. **Residual risk (theirs, not mine to close):** `sprint/simplify/m6/fullbuild.log` contains only
   the line `83 modules, 83 to build` — the full rebuild was started and not finished, so the
   evidence is the per-module `chk4.log` on the 42 changed modules.  Given (1)–(3) the only failure
   mode is a compile error, not a semantic change; but "the patched tree builds" is still unproved.
   **Cheapest way to close it:** one `JOBS=2 python3 sprint/simplify/m6/build.py
   sprint/simplify/m6/E1 <fresh build dir>` run on an unsaturated box (~2–4 min/module under
   contention).

Savings of 718 lines are real but must be reported as *dead-code* savings: it does not touch the
`UniversalGood`/approximation architecture, so it neither overlaps nor competes with the
architecture worker's relative-singularity replacement.

## 5. m14's `cut-prereq-differenceLaw.patch` (the other simplification artifact): fidelity audit

`sprint/simplify/m14/CUT-PREREQ.md` relocates three blocks so that a later deletion zone can be cut:
`EuclideanFiveColor.DifferenceFourier` (→ new `DifferenceLaw.lean`), and
`EuclideanFiveColor.DifferenceInvariant` + `KernelSupport.factor_smul_preserving` +
`PlaneFiveColor.Spectral.relative_difference_invariant` (→ new `DifferenceInvariant.lean`).
`move_audit.py` on the patch [TXT]: 174 added vs 133 deleted content lines; **every deleted line
reappears verbatim among the added lines (0 lost)**, and the 17 added lines with no deleted
counterpart are exactly `import`s, `namespace`/`open`/`noncomputable section`/`variable`/`end`
boilerplate.  So the relocation is textually verbatim and no statement line is invented.

Caveat I cannot close without a build: verbatim *source* does not by itself guarantee the same
*elaborated* signature — a block re-elaborated under a different `variable`/`open` context can pick
up different implicit binder lists or extra instance arguments, which is invisible in text.  The
report's individual `lean -o` runs (rc 0 for the five touched modules) plus unmodified downstream
namespaces is the evidence for that step; a full 83-module rebuild of the patched tree is still
outstanding there too.

## 6. One root-level fidelity remark (cheap, worth fixing in VERIFICATION.md's wording)

There are **two** `ProperColoring` definitions in the tree:

* `OAI.Problem160.ProperColoring k := ∃ c : Plane → Fin k, ∀ x y, dist x y = 1 → c x ≠ c y`
  with `Plane := EuclideanSpace ℝ (Fin 2)` (`Geometry/PlaneColoring/Basic.lean:26`) — this is the
  one `planeChromaticNumber := sInf {k | ProperColoring k}` uses, hence the one the paper's
  χ(R²) means;
* `OAI.EuclideanFiveColor.ProperColoring k (c : ℂ → Fin k)` on `ℂ`
  (`Geometry/PlaneColoring/Coloring.lean:7`) — this is the one quoted in `results/VERIFICATION.md`'s
  "Statement fidelity" section and in the axiom certificate line
  `no_proper_five_coloring : ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c`.

The quote is accurate for the second, and `Chromatic.lean` bridges the two through the explicit
isometry `toPlane`/`ofPlane` (`dist_toPlane`), which is what makes `chromaticNumber_bounds`
(`6 ≤ planeChromaticNumber ∧ planeChromaticNumber ≤ 7`) a statement about the paper's χ(R²) rather
than about a bridge-less ℂ-vocabulary.  Nothing is wrong; the phrase "the paper's Definition" in
VERIFICATION.md should say *which* definition it quotes, because the two are not interchangeable
without that isometry lemma.  Similarly `WeakColoring` is stated over `ℂ`
(`Coloring.lean:27`) while `WeakMeasurableColoring` is stated over `Plane` (`Basic.lean:31`) —
`proper_iff_weak` lives in the `ℂ` vocabulary.

---

## 7. Corrections to this file (block 2), after review

**(a) Section 4 over-claimed.** It said deletion-only "means the trim cannot change a root statement,
a hypothesis, or an axiom dependency". What deletion-only proves is narrower and must be stated so:
every **surviving declaration's source text is byte-identical**, so no statement or hypothesis is
*rewritten*. It does **not** prove

* identical **elaborated** types — a declaration re-elaborated in a module where a section variable,
  `open`, or instance is no longer available can gain implicit binders or instance arguments while
  its text is untouched;
* identical **axiom dependencies** — an axiom dependency is a property of the *proof term*, and a
  deleted lemma that nothing mentioned textually could still have participated (e.g. as an unnamed
  instance or via a `simp` attribute installed elsewhere). The 74-name / 0-occurrence check plus
  "no deleted attribute line / no deleted `instance`" makes this unlikely, not impossible.

So the trim still needs the rebuild **and** a `#check`/`#print axioms` comparison against the
pristine build (`LOCAL-CHECK-QUEUE.json` item 4). The same applies to section 5's "verbatim" verdict
on m14: verbatim source does not establish an identical signature.

**(b) Section 3 conflated two different "equality at 1"s.** Keep them apart:

* **attained pair distance**: with the unit-free hypothesis, `‖x - y‖ = 1` never occurs on `C`;
  `unitFree_pairwise_lt` says every pair distance is `< 1` strictly. This is the statement that is
  equivalent to the tree's `≤ 1` *given* the hypothesis, and strictly stronger as a conclusion.
* **the supremum**: `diam C = sup{‖x-y‖}` **can** equal `1` while every pair distance is `< 1` — my
  own `unitFree_sharp` set `C = (-1/2, 1/2)` is exactly that case (pairs up to `1 - ε`, sup `1`).

Hence: "diam ≤ 1 is sharp" is a statement about the supremum, and it does not conflict with the
pairwise strictness. The tree's `≤ 1` in the *pairwise* form is the unnecessary weakening; a
`Metric.diam`-form bound is where `1` is genuinely attained as a limit, and no `1 - ε` improvement is
possible there (that is what `unitFree_sharp` machine-checks).

**(c) The diamond check in `supervisor/simplify-angular` is not integration evidence.** Its local
result used native Lean 4.35.0 with only `import Lean.Elab.Tactic.Omega` — a different toolchain and a
different import graph from the pinned 4.34.1 + mathlib `d13f23b` development. Recorded as queue
item 5 with that caveat, not as a compiled-in-development result.

---

## 8. Discipline note on the withheld candidate (blocks 2-5, unchanged)

`supervisor/simplify-angular/FIVE-CYCLE-CORE.md` is **withheld from the Lean queue and from the
paper replacement list**, and stays withheld although its finite theorem compiles and its
`moser_recheck.log` shows `rc=0` with `[propext, Classical.choice, Quot.sound]` for
`moser_edge_unit` and `moser_not_three_colorable`.

Two distinct things must not be conflated:

* **the finite theorem** ((V) at all six positions + (D) + (N) + (R) unsat) — *true*, machine-checked
  twice (their `five_cycle_full.py`, my `checks/five_cycle_licence.py`), 21 valid lists, 0 solutions;
* **the inherited application** (that this discharges §6.3.4 without Lemma 6.7) — *not established*,
  because it uses (V) at positions 1, 2, 4, 5 while the paper proves no-common-label only at 0 and 3.
  Eight configurations satisfy the licensed hypotheses (`AUDIT-FIVE-CYCLE.md` §3), and the angular
  worker's newer "two positions suffice" result is precisely an (NC-1)-shaped assumption, not a
  supply of it (§4c).

A compiled stronger theorem plus a passing Moser recheck is evidence about those two artefacts only.
It is **remote evidence** (`moser_recheck.log` was produced elsewhere); I have not re-run it, and I
did not compile anything.
