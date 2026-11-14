/-
Fifth axiom line for `ConnectedSetExclusion.lean`.

The shipped file `ConnectedSetExclusion.lean` ends with four `#print axioms` lines: the four lemmas
`preconnected_forall_lt_or_forall_gt`, `unitFree_not_straddle`, `unitFree_pairwise_lt`,
`unitFree_sharp`.  The fifth theorem of that file, `diam_le_one_of_preconnected_unitFree'`, is a
one-line corollary and was not printed.  This file prints it, so the axiom set of the *whole* file is
covered by five commands, not four.

Run in this directory (needs `ConnectedSetExclusion.olean`, i.e. the previous command must have run):
    source scripts/env4341.sh && cd supervisor/simplify-verification/lean
    lean ConnectedSetExclusion.lean && lean CheckFifth.lean
-/
import ConnectedSetExclusion

#print axioms SupervisorVerify.diam_le_one_of_preconnected_unitFree'
