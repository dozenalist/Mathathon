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
import OAI.Geometry.PlaneColoring.FiveSupport

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
