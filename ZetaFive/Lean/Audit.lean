module

meta import Lean.Elab.Command
meta import Lean.Util.CollectAxioms
import ZetaFive

/-! # Kernel dependency audit

Run `lake env lean ZetaFive/Lean/Audit.lean` after building `ZetaFive`.
The last declarations are explicitly conditional: a standard-axiom report for
them does not construct `PaperEstimates k` or prove unconditional irrationality.
-/

#print axioms ZetaFive.Common.irrational_of_eventually_exists_int_poly_exp
#print axioms ZetaFive.Common.irrational_of_normalized_estimates
#print axioms ZetaFive.Common.coeff_det_of_natDegree_le_one
#print axioms ZetaFive.Common.det_power_sum_matrix_ne_zero
#print axioms ZetaFive.Common.partial_fractions
#print axioms ZetaFive.Common.integralHankel_det_pos
#print axioms ZetaFive.Common.andreief
#print axioms ZetaFive.Common.Arithmetic.det_GV
#print axioms ZetaFive.moment_factorial
#print axioms ZetaFive.riemannZeta_eq
#print axioms ZetaFive.lai_degree
#print axioms ZetaFive.calegari_degree
#print axioms ZetaFive.weight_pos
#print axioms ZetaFive.hasDerivAt_weight
#print axioms ZetaFive.weight_le_uniform_exp_bound
#print axioms ZetaFive.mono_moment
#print axioms ZetaFive.moment_integral_two_through_five
#print axioms ZetaFive.poleValue_valuation_mul
#print axioms ZetaFive.moment_rep
#print axioms ZetaFive.delta_pos
#print axioms ZetaFive.delta_eq_integral
#print axioms ZetaFive.determinantIntegrand_le_uniform_bound
#print axioms ZetaFive.irrational_two_through_five_of_estimates
#check ZetaFive.PaperEstimates
#check ZetaFive.irrational_two_through_five_of_estimates

/- Fail the audit, rather than merely print a warning, if any public declaration
in this development transitively uses a proof hole or a nonstandard axiom. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut checked : Nat := 0
  for (name, _) in env.constants.toList do
    if (`ZetaFive).isPrefixOf name then
      let axioms ← Lean.collectAxioms name
      for ax in axioms do
        unless #[``propext, ``Classical.choice, ``Quot.sound].contains ax do
          throwError "Unexpected axiom {ax} in {name}"
      checked := checked + 1
  if checked == 0 then
    throwError "No ZetaFive declarations were audited"
  logInfo m!"Checked {checked} ZetaFive declarations: only standard Lean axioms."
