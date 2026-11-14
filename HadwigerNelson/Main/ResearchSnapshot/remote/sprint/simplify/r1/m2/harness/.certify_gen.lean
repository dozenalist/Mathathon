import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven
import OAI.Geometry.PlaneColoring.Transfer
import OAI.Geometry.PlaneColoring.Chromatic
import OAI.Geometry.PlaneColoring.NullSetRobust

-- @@STATEMENTS
set_option pp.universes true in #check @OAI.EuclideanFiveColor.no_proper_five_coloring
#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring
-- @@END OAI.EuclideanFiveColor.no_proper_five_coloring
set_option pp.universes true in #check @OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic
#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic
-- @@END OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic
set_option pp.universes true in #check @OAI.Problem160.properColoring_seven
#print axioms OAI.Problem160.properColoring_seven
-- @@END OAI.Problem160.properColoring_seven
set_option pp.universes true in #check @OAI.EuclideanFiveColor.proper_iff_weak
#print axioms OAI.EuclideanFiveColor.proper_iff_weak
-- @@END OAI.EuclideanFiveColor.proper_iff_weak
set_option pp.universes true in #check @OAI.Problem160.chromaticNumber_bounds
#print axioms OAI.Problem160.chromaticNumber_bounds
-- @@END OAI.Problem160.chromaticNumber_bounds
set_option pp.universes true in #check @OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null
#print axioms OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null
-- @@END OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null
set_option pp.universes true in #check @OAI.EuclideanFiveColor.algebraic_colorable_iff
#print axioms OAI.EuclideanFiveColor.algebraic_colorable_iff
-- @@END OAI.EuclideanFiveColor.algebraic_colorable_iff
