# Shard B: positive control at the 5-chromatic level (COMPLETE)

Benchmark: Heule's published 553-vertex 5-chromatic unit-distance graph
(arXiv:1805.12181; data `vtx/553.vtx` + `edge/553.edge` from github.com/marijnheule/CNP-SAT).

## What was done independently
* Coordinates re-parsed from Mathematica syntax into **our own** exact field
  `Q(sqrt3, sqrt5, sqrt11)` (8 basis elements). Heule's checker instead rewrites them into
  Singular input modulo `(r3*Sqrt3-1, s11^2-11, s5^2-5, s3^2-3)`; **we did not run Singular**
  (it is not installed) and did not reuse his checker.
* Every one of the **2722** published edges satisfies `d^2 = 1` as an exact field identity: **0 failures**.
* All **553** vertices are distinct.
* **Completeness check:** of the 553*552/2 - 2722 = 149,706 non-edges, **none** is at unit
  distance (0 hidden unit pairs), so the `.edge` file is the complete unit-distance graph of these points.
  (0 hidden unit pairs), so the `.edge` file is the complete unit-distance graph of these points.
* Degree range 4..38.

## Decision
`k = 4` CNF: 2212 variables, 11441 clauses.
* `cadical153` and `minisat22`: **UNSAT** (agreement).
* `cadical195` DRAT proof: 1,318,521 lines, 139 MB, verified by `drat-trim -f`:
  **`s VERIFIED`**, 563,423 of 665,255 lemmas in core, 43,903,463 resolution steps, 47 s.
  (11438 of 11441 input clauses in the core.)

## Caution recorded
The first attempt used pysat's `cadical153` binding with `with_proof=True`. Its proof came out
with cadical's internal clause-offset format mangled by `_proof_bin2text`, and `drat-trim`
rejected it at line 1. That was a **tooling defect, not a mathematical failure**; the rejection
was not suppressed, the writer was replaced, and the re-run verifies.

## Reproduction
```
cd supervisor/solve-graphs
python3 shard_b.py                     # exact validation + 4-UNSAT by two solvers
python3 shard_b_proof.py               # CNF + DRAT proof (cadical195)
./tools/drat-trim certs/heule553_k4.cnf certs/heule553_k4.drat -f    # -> s VERIFIED
```
