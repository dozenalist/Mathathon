/-
  SOURCE-ONLY CHECK FILE.  Nothing here was compiled by the swarm; all Lean runs are local on
  the parent's machine.  No existing file is edited: this file imports the module and restates
  the step ban under a fresh name, so the parent can (i) compare signatures and (ii) read the
  axiom list, before swapping the body into `FiveSupport.lean`.

  Subject: `five_support_step_ban` (lean/OAI/Geometry/PlaneColoring/FiveSupport.lean:90)
  = manuscript Lemma 6.7 (paper p.41, lines 2139-2157).  RETAINED, statement unchanged.

  Two declarations:
    1. `five_pair_meet`  -- the finite core, `by decide` over Fin 5, no residual-label witness.
    2. `five_support_step_ban_v2` -- same hypotheses / quantifiers / conclusion as `:90-93`,
       branch-free body of 15 tactic lines (old body: 21 lines, `:94-114`).

  Run (from the package root, i.e. the directory containing `OAI/`):
      lean OAI/Geometry/PlaneColoring/StepBanShort.lean
  Expected: no errors; the two `#check` lines print the same telescope up to the name;
  `#print axioms` prints [propext, Classical.choice, Quot.sound].
-/
import OAI.Geometry.PlaneColoring.FiveSupport

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor

/-- Finite core of the support-contact step ban, with no residual-label witness.

    `fiveDiag i = {i, i+2}` (`Exclusion.lean:8`), `fiveAdj i j : i+1 = j ∨ j+1 = i`
    (`Exclusion.lean:9`).  If `p` misses `fiveDiag i`, `q` misses `fiveDiag j`, and neither
    `p ⊆ fiveDiag j` nor `q ⊆ fiveDiag i` holds, then `p` and `q` cannot be disjoint.

    Why it is true: for `fiveAdj i j` the two diagonals are disjoint 2-element sets
    (`five_diag_disjoint`, `Exclusion.lean:20`), so `fiveDiag i ∪ fiveDiag j` misses a single
    label `X` (`five_adj_four`, `Exclusion.lean:23`); `p ⊆ complement (fiveDiag i) = fiveDiag j
    ∪ {X}` together with `¬ p ⊆ fiveDiag j` forces `X ∈ p`, symmetrically `X ∈ q`, and `X`
    cannot lie in two disjoint sets.  `decide` replaces the witness and both invocations of
    `five_forced_label` (`Exclusion.lean:26-28`) that the old proof needed, exactly as
    `five_diag_disjoint` (`:20`) already decides a `Disjoint`-headed statement. -/
lemma five_pair_meet : ∀i j : Fin 5, fiveAdj i j → ∀p q : Finset (Fin 5),
    Disjoint p (fiveDiag i) → Disjoint q (fiveDiag j) → ¬p⊆fiveDiag j → ¬q⊆fiveDiag i →
    ¬Disjoint p q := by decide

variable (c : ℂ → Fin 5) (hc : Measurable c)

/-- **The step ban, branch-free.**  Identical hypotheses, quantifiers and conclusion to
`five_support_step_ban` (`FiveSupport.lean:90-93`). -/
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
    exact five_pair_meet i j hij _ _ (by simpa only [het,hst] using hdt) (by simpa only [heu,hsu] using hdu) hpj hui hdis
  · rintro ⟨hst,hsu⟩
    exact five_pair_meet j i hij.symm _ _ (by simpa only [het,hst] using hdt) (by simpa only [heu,hsu] using hdu) hpi huj hdis

-- The two signatures must print identically except for the trailing name.
#check @five_support_step_ban
#check @five_support_step_ban_v2
#print axioms five_support_step_ban_v2

end EuclideanFiveColor
end
end OAI
