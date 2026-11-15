import OAI.Geometry.PlaneColoring.FiveSupport
/-
  REVISION r2 of the branch-free step ban (source only; not compiled here).
  Supersedes `.ultramath/smwguim4i/m1/StepBanShort.lean` (m1's file is left untouched).

  WHY r2. The local run failed at `five_pair_meet` with
    failed to synthesize Decidable (∀ i j : Fin 5, fiveAdj i j → ∀ p q : Finset (Fin 5), …)
  because `fiveAdj` is a plain `def` (`Exclusion.lean:9`), so instance search does not see the
  `Or` of `Fin` equalities underneath it. A kernel `decide` over `25 x 32 x 32` Finset pairs
  (via `Finset.univ` on `Finset (Fin 5)`) would also be expensive.

  THE FIX. Split the finite core into
    (1) a LABEL-level lemma `five_outsider_unique`, whose `decide` runs over 5^4 = 625 label
        cases and spells the adjacency out as `(i + 1 = j ∨ j + 1 = i)` so the `Or` gets its
        `Decidable` instance from `DecidableEq (Fin 5)` without unfolding any definition;
    (2) a STRUCTURED proof of `five_pair_meet` from that lemma, using
        `Finset.not_subset` (Data/Finset/Defs.lean:243, present at the same line in the pinned
        .scratch/mathlib4) and `Finset.disjoint_left` (Data/Finset/Disjoint.lean:47, likewise).
  No `problem` witness label and no `decide` over Finsets; still branch-free.

  The rest is m1's file unchanged: `five_support_step_ban_v2` has the same hypotheses,
  quantifiers and conclusion as `five_support_step_ban` (`FiveSupport.lean:90-93`), with the two
  call sites adjusted for the new argument order (see below).

  Contract checks kept: the two `#check` lines and the `#print axioms` line.
  This file contains no `sorry`.

  Run (from the package root, i.e. the directory containing `OAI/`):
      lean OAI/Geometry/PlaneColoring/StepBanShort.lean     -- adapted path of this file
-/

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor

/-- **Label-level finite core.** For adjacent `i j` (`i + 1 = j ∨ j + 1 = i`), any two labels
outside both diagonals coincide: `fiveDiag i ∪ fiveDiag j` has four elements, so it misses exactly
one label (`five_adj_four`, `Exclusion.lean:23`), and both `y` and `z` must be it.

`decide` here covers `5^4 = 625` label quadruples; the adjacency is written out as the bare
disjunction so that its `Decidable` instance comes from `DecidableEq (Fin 5)` and does **not**
require unfolding `fiveAdj`. -/
lemma five_outsider_unique : ∀ i j y z : Fin 5, (i + 1 = j ∨ j + 1 = i) →
    y ∉ fiveDiag i → y ∉ fiveDiag j → z ∉ fiveDiag i → z ∉ fiveDiag j → y = z := by
  decide

/-- **Finite core of the support-contact step ban, structured.**

`fiveDiag i = {i, i+2}` (`Exclusion.lean:8`), `fiveAdj i j : i+1 = j ∨ j+1 = i`
(`Exclusion.lean:9`). If `p` misses `fiveDiag i`, `q` misses `fiveDiag j`, and neither
`p ⊆ fiveDiag j` nor `q ⊆ fiveDiag i` holds, then `p` and `q` cannot be disjoint.

Argument: `¬ p ⊆ fiveDiag j` supplies `y ∈ p` with `y ∉ fiveDiag j`; disjointness gives `y ∉ fiveDiag i`.
Symmetrically `z ∈ q` with `z ∉ fiveDiag i` and `z ∉ fiveDiag j`. The label-level lemma gives `y = z`,
so `y` would lie in both `p` and `q`. -/
lemma five_pair_meet {i j : Fin 5} (hij : fiveAdj i j) {p q : Finset (Fin 5)}
    (hp : Disjoint p (fiveDiag i)) (hq : Disjoint q (fiveDiag j))
    (hpj : ¬ p ⊆ fiveDiag j) (hqi : ¬ q ⊆ fiveDiag i) : ¬ Disjoint p q := by
  intro hpq
  obtain ⟨y, hyp, hyj⟩ := Finset.not_subset.mp hpj
  obtain ⟨z, hzq, hzi⟩ := Finset.not_subset.mp hqi
  have hyi : y ∉ fiveDiag i := Finset.disjoint_left.mp hp hyp
  have hzj : z ∉ fiveDiag j := Finset.disjoint_left.mp hq hzq
  -- `fiveAdj` is a plain `def`, so `hij` is definitionally the bare disjunction:
  have hyz : y = z := five_outsider_unique i j y z hij hyi hyj hzi hzj
  exact Finset.disjoint_left.mp hpq hyp (hyz.symm ▸ hzq)

variable (c : ℂ → Fin 5) (hc : Measurable c)

/-- **The step ban, branch-free.** Identical hypotheses, quantifiers and conclusion to
`five_support_step_ban` (`FiveSupport.lean:90-93`). The two call sites below drop the former
placeholder arguments because `p` and `q` are now implicit in `five_pair_meet`; they are inferred
from the `Disjoint` hypotheses. -/
lemma five_support_step_ban_v2 (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i j : Fin 5}
    (hi : a∈fiveSupport c hc x i) (hj : a∈fiveSupport c hc x j) (hij : fiveAdj i j) :
    ∀ᵐt∂angularMeasure,¬(fiveState c hc x t=i ∧ fiveState c hc x (t+(sixty : Angles))=j) ∧
      ¬(fiveState c hc x t=j ∧ fiveState c hc x (t+(sixty : Angles))=i) := by
  obtain ⟨bi,hbi,hzi⟩ := five_support_trace c hc hw hx hi
  obtain ⟨bj,hbj,hzj⟩ := five_support_trace c hc hw hx hj
  have hq := (measurePreserving_add_right angularMeasure (sixty : Angles)).quasiMeasurePreserving
  have hni := avoiding_trace_palette c hc hbi hzi
  have hnj := avoiding_trace_palette c hc hbj hzj
  have hnd := palette_neighbor_disjoint c hc hw x a
  have hdg := fiveState_diag c hc hw hx
  filter_upwards [hni,hnj,hnd,hdg,hq.ae hni,hq.ae hnj,hq.ae hnd,hq.ae hdg,
    palette_sixty_disjoint c hc hw (x+direction (a : Angles))]
    with t hpi hpj hdt het hui huj hdu heu hdis
  refine ⟨?_,?_⟩
  · rintro ⟨hst,hsu⟩
    exact five_pair_meet hij (by simpa only [het,hst] using hdt) (by simpa only [heu,hsu] using hdu)
      hpj hui hdis
  · rintro ⟨hst,hsu⟩
    exact five_pair_meet hij.symm (by simpa only [het,hst] using hdt) (by simpa only [heu,hsu] using hdu)
      hpi huj hdis

-- The two signatures must print identically except for the trailing name.
#check @five_support_step_ban
#check @five_support_step_ban_v2
#print axioms five_support_step_ban_v2

end EuclideanFiveColor
end
end OAI
/-
  CONSUMER `five_opposite_contacts_false` RESTATED AND PROVED FROM `five_support_step_ban_v2`.
  Owned standalone file, swarm smwgzbcnp, member m1.  SOURCE ONLY: nothing in this file was
  compiled remotely; the only execution in this run was sub-second text processing.

  ============================================================================
  1. WHAT THIS FILE IS
  ============================================================================
  `five_opposite_contacts_false_from_v2` below is the real downstream consumer
  `five_opposite_contacts_false` of `lean/OAI/Geometry/PlaneColoring/FiveSupport.lean:199-233`,
  copied out of that source with `sed -n '199,233p'` (35 lines) and changed on exactly three
  lines:

      line  1  the lemma name    five_opposite_contacts_false -> five_opposite_contacts_false_from_v2
      line 22  the callee name   five_support_step_ban -> five_support_step_ban_v2   (source :220)
      line 23  the callee name   five_support_step_ban -> five_support_step_ban_v2   (source :221)

  Everything else -- every binder name, binder order, binder flag (implicit vs explicit), the four
  hypotheses `hi hi' hj hj'`, the hypothesis `hab : b=a+3*sixty`, the implicits `{x} {a b} {i j}`,
  and the conclusion `False` -- are the source bytes, not a transcription: the body was produced by
  `sed` and `diff -u` of the two blocks shows only lines 1, 22, 23 (see `work/diff-body.txt`, which
  is the verbatim output).  The lemma name has to differ because
  `OAI.EuclideanFiveColor.five_opposite_contacts_false` already exists in the imported olean, so
  re-declaring it would be a duplicate declaration; the `#check` pair at the end of this file is
  the contract that the two statements print identically except for that name.

  The section context is also the source's, byte for byte: `namespace OAI`, `noncomputable
  section`, `open Set Filter Topology MeasureTheory`, `namespace EuclideanFiveColor`,
  `variable (c : ℂ → Fin 5) (hc : Measurable c)` -- the same five lines as
  FiveSupport.lean:166-169.

  ============================================================================
  2. HOW `_v2` IS BROUGHT INTO SCOPE FOR A LOCAL RUN (no invented import path)
  ============================================================================
  `five_support_step_ban_v2` is declared at
  `supervisor/simplify-architecture/step-ban/StepBanShort-r2.lean:76` (sha256
  19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655), inside `namespace OAI`.
  That file sits outside the `OAI/` module tree and carries no module path, so there is NO `import`
  that reaches it, and this file does not invent one.  The single import below,
  `OAI.Geometry.PlaneColoring.FiveSupport`, does exist: its olean is at
  `lean/build/lib/OAI/Geometry/PlaneColoring/FiveSupport.olean`, which is on `LEAN_PATH` after
  `source scripts/env4341.sh` (that script prepends `$R/lean/build/lib`).

  The parent therefore brings `_v2` into scope by CONCATENATION -- one module, r2's body first,
  then this file's body.  Exact commands, from the repo root:

      cd <repo>
      { echo 'import OAI.Geometry.PlaneColoring.FiveSupport'
        grep -v '^import ' supervisor/simplify-architecture/step-ban/StepBanShort-r2.lean
        grep -v '^import ' .ultramath/smwgzbcnp/m1/ConsumerFromV2.lean
      } > lean/OAI/Geometry/PlaneColoring/StepBanConsumer.lean
      source scripts/env4341.sh
      ( cd lean && lean OAI/Geometry/PlaneColoring/StepBanConsumer.lean )

  The concatenation is idempotent and already materialised: `StepBanConsumer.lean` in this same
  directory is exactly that concatenation (same command, same inputs), so the parent may equally
  just copy it to `lean/OAI/Geometry/PlaneColoring/` and skip the `{ ... }` line.  Each of the two
  inputs opens `namespace OAI ... end OAI` and `noncomputable section ... end` on its own, so
  appending one to the other is scope-clean; the only command that must not be duplicated is
  `import`, which is why the two `grep -v '^import '` filters are there (line 1 of this file,
  line 30 of r2).

  ============================================================================
  3. PREMISE CITATIONS -- every name used by the proof, with the line that declares it
  ============================================================================
  Paths are relative to the repo root; all were checked by reading the line.

  used as                              declaration                                   file:line
  ------------------------------------------------------------------------------------------------
  `five_contact_next`                  lemma five_contact_next                       FiveSupport.lean:175
  `five_contact_prev`                  lemma five_contact_prev                       FiveSupport.lean:185
  `FiveComb.opposite_contacts`         lemma opposite_contacts                       FiveSupport.lean:156
  `FiveComb.two_bans`                  lemma two_bans                                FiveSupport.lean:160
  `FiveComb.contact_neighbors`         lemma contact_neighbors (used inside :175/:185)  FiveSupport.lean:154
  `mem_fiveSupportList`                @[simp] lemma mem_fiveSupportList             FiveSupport.lean:173
  `five_support_no_sixty`              lemma five_support_no_sixty                   FiveSupport.lean:138
  `fiveRealState`                      def fiveRealState                             FiveSupport.lean:82
  `fiveSupport`                        def fiveSupport                               FiveSupport.lean:83
  `stateSupport_nonempty_measure`      lemma stateSupport_nonempty_measure           FiveSupport.lean:71
  `fiveState_adj`                      lemma fiveState_adj                           Accumulation.lean:390
  `angleMk_quasiMeasurePreserving`     lemma angleMk_quasiMeasurePreserving          PaletteDensity.lean:158
  `measure_eq_zero_iff_ae_notMem`      theorem measure_eq_zero_iff_ae_notMem         pinned mathlib4:
                                       Mathlib/MeasureTheory/OuterMeasure/AE.lean:146
  `sixty`                              def sixty : ℝ := Real.pi/3                    PaletteTransport.lean:390
  `fiveDiag`                           def fiveDiag                                  Exclusion.lean:8
  `fiveAdj`                            def fiveAdj                                   Exclusion.lean:9
  `FiveComb.Adj`                       def Adj (in the statements of :156/:160 only)  FiveSupport.lean:152
  `Angles`                             abbrev Angles := AddCircle (2*Real.pi)         Coloring.lean:16
  `angularMeasure`                     def angularMeasure : Measure Angles            Coloring.lean:17
  `five_support_step_ban`              lemma five_support_step_ban (RETAINED)        FiveSupport.lean:90
                                       called by the source at :220 and :221; not called here
  `five_support_step_ban_v2`           lemma five_support_step_ban_v2                StepBanShort-r2.lean:76
  `five_pair_meet`                     lemma five_pair_meet (used inside _v2)        StepBanShort-r2.lean:58
  `five_outsider_unique`               lemma five_outsider_unique (inside _v2)       StepBanShort-r2.lean:45

  ============================================================================
  4. WHAT THE SUBSTITUTION COSTS AND SAVES
  ============================================================================
  Nothing in the consumer changes except the two callee names: `_v2`'s conclusion is the same
  conjunction, so `hbanI.1`, `hbanI.2`, `hbanJ.1`, `hbanJ.2` at source :227, :228, :230, :231 and
  the whole `hnot` block :222-231 are untouched.  The case split that disappears is inside the
  callee's old body (`rcases hs with hi|hj`, source :103), together with the `five_forced_label`
  invocations at :105/:107 and the `hji`/`union_comm` scaffolding at :97/:107 -- not any split in
  the consumer.  Full report with quotations: `CASE-SPLIT.md` in this directory.

  ============================================================================
  5. STATUS
  ============================================================================
  No `sorry`, no `admit`, no new axioms, no `axiom` declarations.  The proof below is the source's
  proof with the callee renamed, so its obligations are the source's obligations; the one thing not
  yet done is the parent's local `lean` run of the concatenated module.
-/

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)

lemma five_opposite_contacts_false_from_v2 (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x)
    {a b : ℝ} (hab : b=a+3*sixty) {i j : Fin 5}
    (hi : a∈fiveSupport c hc x i) (hi' : a∈fiveSupport c hc x (i+1))
    (hj : b∈fiveSupport c hc x j) (hj' : b∈fiveSupport c hc x (j+1)) : False := by
  have hn := five_contact_next c hc hw hx hi hi'
  have hp := five_contact_prev c hc hw hx hj hj'
  have hdis : Disjoint ({i-1,i+2} : Finset (Fin 5)) {j-1,j+2} := by
    apply Finset.disjoint_left.mpr
    intro k hk hl
    have hiK : a+sixty∈fiveSupport c hc x k := by
      apply (mem_fiveSupportList _ _ _ _ _).mp
      simp only [Finset.mem_insert,Finset.mem_singleton] at hk
      rcases hk with rfl|rfl <;> tauto
    have hjK : b-sixty∈fiveSupport c hc x k := by
      apply (mem_fiveSupportList _ _ _ _ _).mp
      simp only [Finset.mem_insert,Finset.mem_singleton] at hl
      rcases hl with rfl|rfl <;> tauto
    exact five_support_no_sixty c hc hw hx hiK (by convert hjK using 1; rw [hab]; ring)
  have hji := FiveComb.opposite_contacts i j hdis
  obtain ⟨s,hs,_hst,hban⟩ := FiveComb.two_bans i j hji
  have hss : a∈fiveSupport c hc x s := by rcases hs with rfl|rfl <;> assumption
  have hbanI := five_support_step_ban_v2 c hc hw hx hi hi' (Or.inl rfl)
  have hbanJ := five_support_step_ban_v2 c hc hw hx hj hj' (Or.inl rfl)
  have hnot : ∀ᵐt∂angularMeasure,fiveState c hc x t≠s := by
    filter_upwards [hbanI,hbanJ,fiveState_adj c hc hw hx] with t hbI hbJ ha he
    rw [he] at ha
    rcases hban _ ha with h|h
    · rcases h with ⟨rfl,ht⟩|⟨rfl,ht⟩
      · exact hbI.1 ⟨he,ht⟩
      · exact hbI.2 ⟨he,ht⟩
    · rcases h with ⟨rfl,ht⟩|⟨rfl,ht⟩
      · exact hbJ.1 ⟨he,ht⟩
      · exact hbJ.2 ⟨he,ht⟩
  have hz : volume (fiveRealState c hc x s)=0 := measure_eq_zero_iff_ae_notMem.mpr (angleMk_quasiMeasurePreserving.ae hnot)
  exact (stateSupport_nonempty_measure hss).ne' hz

-- Contract checks: the two signatures must print identically except for the trailing name,
-- and the new proof must rest on the standard axioms only.
#check @five_opposite_contacts_false
#check @five_opposite_contacts_false_from_v2
#print axioms five_opposite_contacts_false_from_v2

end EuclideanFiveColor
end
end OAI
