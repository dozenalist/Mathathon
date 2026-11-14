-- Statement + axiom certificate for the sprint deliverables.
-- Built with `lean Check.lean` under either toolchain, against the tree's oleans
-- (LEAN_PATH must contain the tree's build/lib first).
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Chromatic
import OAI.Geometry.PlaneColoring.Transfer
import OAI.Geometry.PlaneColoring.NullSetRobust

open OAI

-- The headline. `#check` prints the type (compare byte for byte with the baseline
-- printout); `#print axioms` must print exactly [propext, Classical.choice, Quot.sound].
#check @OAI.EuclideanFiveColor.no_proper_five_coloring
#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring

-- The other kept results.
#check @OAI.Problem160.properColoring_seven
#print axioms OAI.Problem160.properColoring_seven
#check @OAI.EuclideanFiveColor.proper_iff_weak
#print axioms OAI.EuclideanFiveColor.proper_iff_weak
#check @OAI.EuclideanFiveColor.chromaticNumber_bounds
#print axioms OAI.EuclideanFiveColor.chromaticNumber_bounds

-- The main theorem of the paper restated against the tree's own definitions.
#check @OAI.PlaneFiveColor.Spectral.ergodic_wild_fourier
#print axioms OAI.PlaneFiveColor.Spectral.ergodic_wild_fourier
