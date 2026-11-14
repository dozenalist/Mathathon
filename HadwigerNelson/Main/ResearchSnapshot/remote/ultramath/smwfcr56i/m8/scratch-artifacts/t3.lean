import Mathlib
open Finset
#check @Finset.prod_le_prod
#check @Finset.prod_le_prod'
#check @measurable_pi_lambda
#check @measurable_pi_iff
#check @Measurable.of_eval
#check @ErgodicVAdd.aeconst_of_forall_preimage_vadd_ae_eq
example {ι : Type*} (s : Finset ι) (f g : ι → ℝ) (h0 : ∀ i ∈ s, 0 ≤ f i) (h : ∀ i ∈ s, f i ≤ g i) :
    ∏ i ∈ s, f i ≤ ∏ i ∈ s, g i := Finset.prod_le_prod h0 h
