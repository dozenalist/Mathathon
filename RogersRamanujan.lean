/-
Aggregator for the Rogers--Ramanujan (SAIR Mathathon problem 127) Lean modules.

`RogersRamanujan/Lean/` sits outside the `Mathathon` module hierarchy, so without
this aggregator and the `[[lean_lib]] name = "RogersRamanujan"` entry in
`lakefile.toml` the default build compiles nothing of the project's Lean work.
Named target:  lake build RogersRamanujan

Scope note: the theorems collected here are the standard staircase reduction
(positivity bound, both inverse laws, exact weight change, nonnegativity). They
are project infrastructure, not a solution of the Rogers--Ramanujan problem.
Weak-decreasingness of the staircase coordinates is NOT yet proved here.
-/
import RogersRamanujan.Lean.Staircase
