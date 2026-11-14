/-
Aggregator for the Rogers--Ramanujan (SAIR Mathathon problem 127) Lean modules.

`RogersRamanujan/Lean/` sits outside the `Mathathon` module hierarchy, so without
this aggregator and the `[[lean_lib]] name = "RogersRamanujan"` entry in
`lakefile.toml` the default build compiles nothing of the project's Lean work.
Named target:  lake build RogersRamanujan

Contents:
  * `Staircase`      -- the staircase map, its positivity bound, both inverse
                        laws, the exact weight change and nonnegativity.
  * `StaircaseOrder` -- the order statement that was missing from cycle 1
                        (`subStair_weakDec`), the converse directions
                        (`addStair_pos`, `addStair_gap`), both inverse laws as
                        maps between the correctly specified subtypes with the
                        length retained and zero padding explicit, and witnesses
                        showing the `Gap` hypothesis is needed and that padding
                        carries the length.

Together these make the staircase reduction a genuine equivalence between
positive gap partitions and weakly decreasing coordinate lists, and `ShiftT`
formalizes the same-weight shift `T`, the same-weight bijection from `D_n` onto
the `B_n` of BZ82/BP06 (with smallest part at least the length). They are project
infrastructure: they establish the D_n/B_n bridge, but do not formalize the
residue-side A_n correspondence, phi or psi, and do not solve the requested
more-natural Rogers--Ramanujan bijection problem.
-/
import RogersRamanujan.Lean.Staircase
import RogersRamanujan.Lean.StaircaseOrder
import RogersRamanujan.Lean.ShiftT
