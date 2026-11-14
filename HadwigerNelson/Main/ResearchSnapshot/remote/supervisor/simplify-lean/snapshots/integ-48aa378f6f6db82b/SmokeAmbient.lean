/-  Smoke root B: depends on the REPLACEMENT proof in ConditionalLimits.lean, and on the
    cross-module consumer of the finite theorem at ConditionalLimits:322. -/
import OAI.MeasureTheory.CompactFactors.ConditionalLimits

open OAI.PlaneFiveColor.Spectral

-- the ambient root, now a one-line call to the shared theorem
#print axioms ambient_uniform_precision_contradiction
#check @ambient_uniform_precision_contradiction

-- cross-module consumer of the FINITE theorem (ConditionalLimits:322): proves the finite
-- statement survived the patch, since this call is positional
#print axioms uniform_precision_contradiction
#check @FiniteEncodingApproximationAt
#check @AmbientEncodingAt

-- the deep consumer in Approximation.lean:414
#print axioms finite_uniform_successor_contradiction
