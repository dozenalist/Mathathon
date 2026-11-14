# Pre-registration: `a = 1/4`, the existing 73-cell patch, six colours

Written before any computation in this block. One parameter, one patch, one `k`, one pipeline.

**Parameter.** `a = 1/4`. Honeycomb = Voronoi hexagons of the triangular lattice of spacing
`a sqrt3`; cell `(p,q) in Z^2`; forced = `dmin(v) < 1 < dmax(v)` (strict, interior-realised).

**Patch.** `P = {v : N(v) <= 19}`, the same 73 cells as the accepted certificate (supervisor's stated
preference). Not swept, not resized.

**Forced offsets at `a = 1/4`: derived analytically, before solving.** Two independent routes, both free
of computation:
* *Window.* `dmin >= |v| - 2a`, `dmax <= |v| + 2a` with `a = 1/4`, so forcedness forces
  `0.5 < |v| < 1.5`. With `|v|^2 = 3a^2 N = 3N/16` that is `4/3 < N < 12`, so `N in {3,4,7,9}`
  (the representable norms in that open range).
* *Homothety.* `dmin(v,a) = a mu(v)`, `dmax(v,a) = a nu(v)`, so forced `<=> mu(v) < 4 < nu(v)`, i.e.
  `mu^2 < 16 < nu^2`. From the exact per-ring table at `a = 1`: `N=1 (0,13)` fails `nu^2 > 16`;
  `N=3 (1,25)`, `N=4 (3,28)`, `N=7 (7,43)`, `N=9 (12,49)` all pass; `N=12` has `mu^2 = 16` exactly,
  so it fails *strictness* (a tangency, `dmin = 1`).

Both give `F(1/4) = {v : N(v) in {3,4,7,9}}`, **30 offsets** (6+6+12+6). Note this differs from
`F(1/5) = {4,7,9,12,13}`: ring 3 enters, rings 12 and 13 leave.

**Pipeline (one process for the decision).** Build `G[P]` with connection set `F(1/4)`; CNF for 6
colouring; decide. Then exactly one of:
* SAT ⟹ extract, **verify edge by edge**, report. Consequence: this patch does not exclude six colours
  at `a = 1/4`; no interval, and the upper uncovered range stays open.
* UNSAT ⟹ DRAT proof from the **`cadical` binary** (not pysat's `with_proof`, whose writer is known
  mangled per `supervisor/solve-graphs/certs/shard_b_summary.md`), checked by **`drat-trim` from
  `supervisor/solve-graphs/tools/`**, copied under this directory. `s VERIFIED` required.
* Timeout or budget exceeded ⟹ **inconclusive**, reported as such, nothing claimed.

**Interval pre-committed (conditional on UNSAT being certified).** If `G[P]` with `F(1/4)` is
6-UNSAT, then by the same homothety argument the same edge set is preserved on

    a in ( max_{v in F(1/4)} 1/nu(v) , min_{v in F(1/4)} 1/mu(v) ) = ( 1/sqrt25 , 1/sqrt12 )
      = ( 1/5 , 1/sqrt12 ) = ( 0.2 , 0.2886751... )

since `min nu^2 = 25` (ring 3) and `max mu^2 = 12` (ring 9). Overlap with the accepted interval
`(1/sqrt28, 1/sqrt19) = (0.188982, 0.229416)` is the non-empty open set `(0.2, 0.229416)`; the union is
the single open interval `(1/sqrt28, 1/sqrt12) = (0.188982, 0.288675)`. Both endpoints of the new
interval are tangencies (ring 3 at `dmax = 1` when `a = 1/5`; ring 9 at `dmin = 1` when `a = 1/sqrt12`),
so the interval is genuinely open.

**Not done in this block:** no second `k`, no other patch, no other `a`, no core minimisation, no
re-run after a result.
