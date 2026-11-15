import ZetaFive
-- Full axiom audit: EVERY theorem/lemma exported by the correspondence library.
-- Regenerate with: python3 tools/gen_audit.py (kept in ZetaFive/Main).

-- ===== Basic.lean (namespace ZetaFive.Correspondences)
#print axioms ZetaFive.Correspondences.H5_zero
#print axioms ZetaFive.Correspondences.H5_succ
#print axioms ZetaFive.Correspondences.H5_increment
#print axioms ZetaFive.Correspondences.L_zero
#print axioms ZetaFive.Correspondences.L_monomial
#print axioms ZetaFive.Correspondences.L_C_mul_X_pow
#print axioms ZetaFive.Correspondences.L_add
#print axioms ZetaFive.Correspondences.L_C_mul
#print axioms ZetaFive.Correspondences.τ_add
#print axioms ZetaFive.Correspondences.τ_C_mul
#print axioms ZetaFive.Correspondences.derivative_C_mul_X_pow_succ
#print axioms ZetaFive.Correspondences.μpoly_monomial
#print axioms ZetaFive.Correspondences.μpoly_add
#print axioms ZetaFive.Correspondences.pull_neg_X_sq_pow
#print axioms ZetaFive.Correspondences.pull_monomial

-- ===== Transport.lean (namespace ZetaFive.Correspondences)
#print axioms ZetaFive.Correspondences.τ_C_mul_X_pow
#print axioms ZetaFive.Correspondences.τ_X
#print axioms ZetaFive.Correspondences.μpoly_eq_τ_pull
#print axioms ZetaFive.Correspondences.τ_X_pow_three
#print axioms ZetaFive.Correspondences.τ_X_pow_four
#print axioms ZetaFive.Correspondences.μpoly_one
#print axioms ZetaFive.Correspondences.rat_pole_identity
#print axioms ZetaFive.Correspondences.d_natCast
#print axioms ZetaFive.Correspondences.d_neg_natCast
#print axioms ZetaFive.Correspondences.τX_single_pole_transport

-- ===== AffineParameter.lean (namespace ZetaFive.Correspondences)
#print axioms ZetaFive.Correspondences.list_pole_affine
#print axioms ZetaFive.Correspondences.mu_affine
#print axioms ZetaFive.Correspondences.mu_sub_eq
#print axioms ZetaFive.Correspondences.laurent_pole_expansion
#print axioms ZetaFive.Correspondences.laurent_pole_coeff

-- ===== Matrix.lean (namespace ZetaFive.Correspondences)
#print axioms ZetaFive.Correspondences.weight_cancellation
#print axioms ZetaFive.Correspondences.weight_denom_ne_zero
#print axioms ZetaFive.Correspondences.gramMatrix_affine
#print axioms ZetaFive.Correspondences.det_congruence
#print axioms ZetaFive.Correspondences.det_add_smul_eq_det_mul

-- ===== Candm1.lean (namespace ZetaFive.Correspondences.M1)
#print axioms ZetaFive.Correspondences.M1.L_finset_sum
#print axioms ZetaFive.Correspondences.M1.L_neg
#print axioms ZetaFive.Correspondences.M1.L_sub
#print axioms ZetaFive.Correspondences.M1.L_X_pow
#print axioms ZetaFive.Correspondences.M1.L_eq_sum_range
#print axioms ZetaFive.Correspondences.M1.L_X_add_one_pow
#print axioms ZetaFive.Correspondences.M1.sum_range_choose_bernoulli_sub
#print axioms ZetaFive.Correspondences.M1.L_comp_X_add_one_sub
#print axioms ZetaFive.Correspondences.M1.derivative_comp_X_add_one
#print axioms ZetaFive.Correspondences.M1.iterate_derivative_comp_X_add_one
#print axioms ZetaFive.Correspondences.M1.iterate_derivative_sub
#print axioms ZetaFive.Correspondences.M1.iterate_derivative_three
#print axioms ZetaFive.Correspondences.M1.τ_eq_L_iterate_derivative
#print axioms ZetaFive.Correspondences.M1.τ_comp_X_add_one_sub
#print axioms ZetaFive.Correspondences.M1.L_comp_X_add_one_sub_X

-- ===== Candm2.lean (namespace ZetaFive.Correspondences.M2)
#print axioms ZetaFive.Correspondences.M2.mu_coeff_eq_factor
#print axioms ZetaFive.Correspondences.M2.mu_factor_ne_zero
#print axioms ZetaFive.Correspondences.M2.mu_coeff_ne_zero_iff
#print axioms ZetaFive.Correspondences.M2.mu_coeff_ne_zero
#print axioms ZetaFive.Correspondences.M2.mu_poly_monomial_ne_zero
#print axioms ZetaFive.Correspondences.M2.mu_coeff_zero
#print axioms ZetaFive.Correspondences.M2.L_one
#print axioms ZetaFive.Correspondences.M2.L_X_pow_eq_zero_of_odd
#print axioms ZetaFive.Correspondences.M2.tau_one
#print axioms ZetaFive.Correspondences.M2.tau_X_pow_two
#print axioms ZetaFive.Correspondences.M2.tau_X'
#print axioms ZetaFive.Correspondences.M2.tau_X_pow_eq_zero_of_even
#print axioms ZetaFive.Correspondences.M2.L_ne_zero
#print axioms ZetaFive.Correspondences.M2.tau_ne_zero
#print axioms ZetaFive.Correspondences.M2.mu_poly_ne_zero

-- ===== Candm3.lean (namespace ZetaFive.Correspondences.M3)
#print axioms ZetaFive.Correspondences.M3.natCast_polyX
#print axioms ZetaFive.Correspondences.M3.L_sum
#print axioms ZetaFive.Correspondences.M3.L_neg
#print axioms ZetaFive.Correspondences.M3.L_X_add_one_pow
#print axioms ZetaFive.Correspondences.M3.L_neg_one_sub_X_pow
#print axioms ZetaFive.Correspondences.M3.reflect_add
#print axioms ZetaFive.Correspondences.M3.reflect_neg
#print axioms ZetaFive.Correspondences.M3.reflect_monomial
#print axioms ZetaFive.Correspondences.M3.L_reflect
#print axioms ZetaFive.Correspondences.M3.L_eq_zero_of_reflect_eq_neg
#print axioms ZetaFive.Correspondences.M3.derivative_reflect
#print axioms ZetaFive.Correspondences.M3.derivative3_reflect
#print axioms ZetaFive.Correspondences.M3.τ_reflect
#print axioms ZetaFive.Correspondences.M3.d_neg_one_sub
#print axioms ZetaFive.Correspondences.M3.list_sum_neg_map
#print axioms ZetaFive.Correspondences.M3.poleSum_reflect
#print axioms ZetaFive.Correspondences.M3.tauX_reflect

-- ===== Candm4.lean (namespace ZetaFive.Correspondences.M4)
#print axioms ZetaFive.Correspondences.M4.H5_one
#print axioms ZetaFive.Correspondences.M4.H5_two
#print axioms ZetaFive.Correspondences.M4.H5_nonneg
#print axioms ZetaFive.Correspondences.M4.H5_lt_succ
#print axioms ZetaFive.Correspondences.M4.H5_le_succ
#print axioms ZetaFive.Correspondences.M4.H5_mono
#print axioms ZetaFive.Correspondences.M4.H5_strictMono
#print axioms ZetaFive.Correspondences.M4.H5_pos
#print axioms ZetaFive.Correspondences.M4.H5_ge_one
#print axioms ZetaFive.Correspondences.M4.inv_pow_five_le_sub_inv
#print axioms ZetaFive.Correspondences.M4.inv_five_le_telescope
#print axioms ZetaFive.Correspondences.M4.H5_succ_le_two_sub_inv
#print axioms ZetaFive.Correspondences.M4.H5_lt_two
#print axioms ZetaFive.Correspondences.M4.H5_le_two
#print axioms ZetaFive.Correspondences.M4.H5_add
#print axioms ZetaFive.Correspondences.M4.H5_tail_le
#print axioms ZetaFive.Correspondences.M4.H5_tail_le_inv
#print axioms ZetaFive.Correspondences.M4.H5_cauchy
#print axioms ZetaFive.Correspondences.M4.eq_sub_H5_of_nat
#print axioms ZetaFive.Correspondences.M4.d_reflect
#print axioms ZetaFive.Correspondences.M4.H5Z_zero
#print axioms ZetaFive.Correspondences.M4.H5Z_natCast
#print axioms ZetaFive.Correspondences.M4.H5Z_reflect
#print axioms ZetaFive.Correspondences.M4.H5Z_diff_pos
#print axioms ZetaFive.Correspondences.M4.H5Z_diff
#print axioms ZetaFive.Correspondences.M4.eq_sub_H5Z
#print axioms ZetaFive.Correspondences.M4.H5Z_satisfies_diff
#print axioms ZetaFive.Correspondences.M4.H5Z_satisfies_refl
#print axioms ZetaFive.Correspondences.M4.pole_values_unique

