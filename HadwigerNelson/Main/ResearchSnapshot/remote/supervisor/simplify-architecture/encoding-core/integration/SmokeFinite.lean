/-  Smoke root A: depends on the REPLACEMENT proof in ConditionalSpectrum.lean.
    Run from the repo root after `source scripts/env4341.sh` and a tree build:
      LEAN_PATH="$PWD/supervisor/simplify-architecture/encoding-core:$LEAN_PATH" \
        lean supervisor/simplify-architecture/encoding-core/integration/SmokeFinite.lean
    Expected: no errors; all `#print axioms` lines print
      [propext, Classical.choice, Quot.sound]
    A leaked `sorryAx` here means the transplanted body was not substituted. -/
import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum

open OAI.PlaneFiveColor.Spectral

-- the shared theorem carrying the transplanted 151-line body
#print axioms uniform_precision_contradiction
#check @uniform_precision_contradiction

-- the public root, now proved by a one-line call into it
#print axioms finite_uniform_precision_contradiction
#check @finite_uniform_precision_contradiction

-- a consumer that actually depends on the replacement (ConditionalSpectrum:479)
#print axioms finite_uniform_successor_contradiction
#check @finite_uniform_successor_contradiction

-- the definition is an alias; this must elaborate with the same binders
#check @FiniteEncodingApproximationAt
