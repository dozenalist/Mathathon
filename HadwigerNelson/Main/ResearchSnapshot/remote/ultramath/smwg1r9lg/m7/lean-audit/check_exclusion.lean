/-
  Adjacent check (not one of the four cores): the record's ledger says
  "local finiteness at k = 5 | true (paper, machine-checked)" and, in the text,
  that the k=5 endgame is machine-checked at Exclusion.lean:144 while the file's own
  comment "does not assert that the data have been extracted".  Print the statement
  so the claim can be read exactly.
-/
import OAI.Geometry.PlaneColoring.Exclusion

open OAI

#check @OAI.EuclideanFiveColor.no_five_exclusion_continua
#print axioms OAI.EuclideanFiveColor.no_five_exclusion_continua
