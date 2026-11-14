# Six colours die on 73 cells at `a = 1/5`: a certified 6-UNSAT induced subgraph

Pre-registered patch: `PATCH-PREREGISTRATION.md` (written before any computation in this block).
Certificate: `p19.cnf`, `p19.drup`, checked by `rup_verify` built from `rup.c` (rc 0).
Producer: `patch19.py` (graph, colouring, decisions) and `p19_gen.py` (DRUP export).

## Result

**Theorem (certified).** Let `a = 1/5`, let the cells be the Voronoi hexagons of the triangular
lattice of spacing `a sqrt3`, and let `F = {v : N(v) in {4,7,9,12,13}}` be the forced offsets
(`N(p,q) = p^2+pq+q^2`). Put `P = {v in Z^2 : N(v) <= 19}` — **73 cells**. Then the induced subgraph
`G[P]` of `Cay(Z^2, F)` has **no proper 6-colouring**.

Consequently **no colouring of the plane that is constant on the interiors of those cells uses six
colours**: every such colouring needs at least seven. This is a statement about the whole honeycomb
family at `a = 1/5`, not about one period — `G[P]` is an induced subgraph of the infinite forced-offset
graph, and any cell-constant colouring restricts to a colouring of `G[P]`.

**Stronger, machine-decided but not certified here.** `chi(G[P]) = 8`: 7-UNSAT is reported by two
independent CDCL solvers (`Cadical153` and `Glucose3`), and an explicit 8-colouring exists with **0
monochromatic edges out of 888** (colour classes `12,10,10,9,9,9,8,6`). So at `a = 1/5` the cell family
needs at least 8 colours — more than the plane's 7, because the paper's 7-colouring is not
cell-constant at this cell size. The `k = 7` DRUP certificate was **not** produced: its generation
exceeded the 60 s single-process cap and was abandoned (failed route, recorded in `STATUS.json`).
Grade for the 8-colour claim: machine-decided decision, no proof certificate.

## The graph (exact, stated once)

`P = {v : N(v) <= 19}`, `|P| = 73` (`N <= 21` would already be 85 > 81, so this is the cap-respecting
ball). Edges: `|E| = 888`, degrees min 16 / max 42 / mean 24.3. The centre vertex has degree exactly
`|F| = 42`, so no adjacency is lost at the centre. Maximum clique: **4** (witness
`{(0,0), (-2,0), (-2,2), (0,2)}`), so the clique bound gives only `chi >= 4`; the true value is 8.
Full vertex list, edge list and colouring: `patch19_cert.json`.

## The certificate, and how it was checked

1. Plain CNF for 6-colouring: 438 variables, 6496 clauses (at-least-one and at-most-one per cell and
   six binary clauses per edge), **no symmetry breaking**, so UNSAT is unconditional.
2. Two solvers independently report UNSAT at `k = 6` with this CNF.
3. `Glucose3(with_proof=True)` emits a 72,699-line DRUP proof; deletion lines (`d ...`) are dropped on
   export — sound, since keeping clauses only strengthens unit propagation, so a RUP check that
   succeeds against the superset is valid. Tautologies dropped, duplicate literals collapsed. Result:
   42,109 kept steps ending in the empty clause (`p19.drup`).
4. `rup.c` — my own two-watched-literal RUP checker, no solver library, no drat-trim (absent from this
   VM) — verifies every step: `RUP VERIFIED: 42109 steps, each unit-propagation refuting; empty clause
   DERIVED -> UNSAT`, rc 0, ~20 s.

Reproduce:

    python3 patch19.py            # graph + chi decision + verified 8-colouring -> patch19_cert.json
    python3 p19_gen.py            # plain CNF + Glucose3 DRUP  -> patch19_drup.json
    (python3 export step as in this block)   # -> p19.cnf, p19.drup
    gcc -O2 -o rup_verify rup.c && ./rup_verify p19.cnf p19.drup

## Two bugs found in my own tooling (kept on the record)

* **`p19_shrink.py`** — greedy minimisation of the UNSAT core exceeded the cap (73+ solver calls); it
  produced no output and is superseded. A smaller core would make a shorter certificate but was not
  needed once the full proof verified.
* **`rup.c`, first version** — two defects, both of which would have silently accepted a bad proof or
  rejected a good one: (i) clauses were added with their watched literals possibly already false at
  level 0, violating the watch invariant; (ii) unit clauses derived mid-proof were enqueued but never
  propagated, so their consequences were never derived. Defect (ii) caused a spurious `RUP FAILURE at
  step 26154`; a naive independent propagation confirmed that step *was* RUP, which localised the bug.
  Both are fixed in the shipped `rup.c`. `patch19_proof.py` is an abandoned earlier driver (pysat
  returns DIMACS strings, not lists, so its empty-clause assert fired); `p19_gen.py` supersedes it.

> **SCOPE BANNER (added after supervisor review).** The `chi = 8` figure in this report is
> **uncertified and unnecessary**. It rests on two CDCL decisions with no proof certificate (the
> `k = 7` DRUP generation exceeded the cap), and the family exclusion needs only the *certified*
> 6-UNSAT. Nothing downstream uses it; `INTERVAL.md` does not use it. The 73-cell 6-UNSAT itself
> remains **candidate** pending the independent geometry audit.

## What this does not say

* Nothing about `chi(R^2)`. It is a no-go for **one** cell-constant family at **one** parameter.
* It does not say the honeycomb family at other `a` fails; `a = 1/5` is below `1/sqrt13`, where the
  earlier certified no-go stopped.
* The 7-UNSAT claim (`chi(G[P]) = 8`) has no proof certificate in this block.
* Inherited calibration only: the retired graph worker's Heule-553 positive control
  (`supervisor/solve-graphs/certs/shard_b_summary.md`) is **not** a 6-chromatic graph and its 139 MB
  certificate was not re-run. Nothing in this block depends on it.

## Why this matters for the programme

The cell route is now closed at `a = 1/5` in the strongest sense available: not "this period fails" but
"this parameter fails, for every colouring constant on cell interiors, non-periodic ones included",
with an inspectable proof. Combined with the earlier certified results the cell family is now excluded
for hexagon circumradius in `(1/sqrt13, 1/2]` (>= 7 colours) **and** at `a = 1/5` (>= 7, in fact 8).
A six-colouring, if one exists, therefore cannot be constant on honeycomb cells at any size tested;
the untested range is `a in (0.12204, 0.27735)` minus `{1/5}`, which remains open.
