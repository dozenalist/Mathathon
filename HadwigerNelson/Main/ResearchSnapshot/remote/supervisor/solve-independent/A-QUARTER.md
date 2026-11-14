# `a = 1/4`: certified 6-UNSAT on the same 73 cells, and the interval `(1/5, 1/sqrt12)`

Pre-registered in `PREREG-A-QUARTER.md` before any computation. One parameter, one patch, one `k`,
one pipeline, 3.02 s total (cap 60 s). No second search, no sweep, no core minimisation.

## 1. Forced offsets at `a = 1/4` — two independent derivations, then checked exactly

*From the window.* `dmin >= |v| - 2a`, `dmax <= |v| + 2a` with `a = 1/4` force `0.5 < |v| < 1.5`; and
`|v|^2 = 3a^2 N = 3N/16`, so `4/3 < N < 12`, i.e. `N in {3,4,7,9}`.

*From homothety and the `a = 1` ring table.* Forced `<=> mu(v) < 4 < nu(v) <=> mu^2 < 16 < nu^2`.
`N=1 (0,13)` fails; `N=3 (1,25)`, `N=4 (3,28)`, `N=7 (7,43)`, `N=9 (12,49)` pass; `N=12` has
`mu^2 = 16` **exactly**, so it fails strictness — a tangency.

Both give `F(1/4) = {v : N(v) in {3,4,7,9}}`, **30 offsets** (6+6+12+6), confirmed by direct exact
computation in `Q(sqrt3)` at the start of the pipeline. Ring 3 enters relative to `a = 1/5`; rings 12
and 13 leave.

## 2. The experiment

Patch `P = {v : N(v) <= 19}`, the same 73 cells as the accepted certificate.
`G[P]`: **723 edges**, degrees 12..30 (centre degree 30 = `|F|`), **max clique 4** — so the clique
bound is worthless here and the UNSAT is genuinely global.

Plain CNF for 6 colouring, no symmetry breaking: 438 variables, 5506 clauses. `cadical` (binary, DRAT
output) reports **UNSAT**; `drat-trim` from `supervisor/solve-graphs/tools/` (copied under `tools/`,
sha256 identical to the accepted original) reports

    c 32677 of 41772 lemmas in core using 842488 resolution steps
    c 0 RAT lemmas in core; 7111 redundant literals in core lemmas
    s VERIFIED

So **no colouring of the plane that is constant on the interiors of these honeycomb cells at
`a = 1/4` uses six colours.** That is a restricted family exclusion, not a statement about `chi(R^2)`.

## 3. The interval, derived analytically after the certification

`dmin(v,a) = a mu(v)`, `dmax(v,a) = a nu(v)`, so all 30 offsets stay strictly forced exactly on

    a  in  ( max_v 1/nu(v) , min_v 1/mu(v) )  =  ( 1/min nu , 1/max mu )
         =  ( 1/sqrt25 , 1/sqrt12 )  =  ( 1/5 , 0.2886751... )

since `min nu^2 = 25` (ring 3) and `max mu^2 = 12` (ring 9). Length `0.088675`. `a = 1/4 = 0.25` sits
inside with margins `0.05` below and `0.038675` above. **Both endpoints are tangencies and are
therefore genuinely excluded**: at `a = 1/5` ring 3 has `dmax = 5a = 1` exactly, at `a = 1/sqrt12` ring
9 has `dmin = a sqrt12 = 1` exactly. Neither is a numerical artefact.

## 4. Overlap with the accepted interval, and the resulting closure

| interval | justification | status |
|---|---|---|
| `(1/sqrt28, 1/sqrt19) = (0.188982, 0.229416)` | 73-cell certificate at `a = 1/5` | **accepted** (geometry audit: drat-trim `s VERIFIED` on matching hashes; independent CNF/edge/interval recheck) |
| `(1/5, 1/sqrt12) = (0.2, 0.288675)` | 73-cell certificate at `a = 1/4` | this block: drat-trim `s VERIFIED`; **pending** the same independent audit |
| `(1/sqrt13, 1/2] = (0.277350, 0.5]` | forced set contains `T^2 = {N in {1,3,4}}`, so `>= 7` colours (`CELL-NOGO-v2.md` Thm 2) | earlier exact computation + proof |

Overlap of the first two: `(0.2, 0.229416)`, non-empty. Their union is the single open interval
`(1/sqrt28, 1/sqrt12) = (0.188982, 0.288675)`. Union with the third (which starts at `0.277350 <
0.288675`, so there is no gap):

> **For every `a` in `(1/sqrt28, 1/2]` — every hexagon circumradius from `0.188982` to `0.5` — no
> colouring of the plane that is constant on the interiors of the honeycomb cells uses six colours.**
> Above `1/2` the family is vacuous (a cell's interior then contains a unit pair); below `1/sqrt28`
> nothing is known.

This is the whole non-vacuous range apart from the bottom sliver `(0, 1/sqrt28]`. Note the three
ingredients are independent results with different methods (two separate machine certificates plus the
`T^2` argument), and the second is not yet independently audited.

## 5. Why the strict criterion removes boundary-ownership questions here too

Every offset in `F` satisfies `dmin < 1 < dmax` **strictly**, so the unit pair is realised by interior
points of both cells (dense interiors, connected domain, interval image). Interior points belong to
their cell under any ownership rule, so no rule is assumed. The parameter `a = 1/4` was chosen so that
`N = 12` fails strictness exactly (`dmin = 1`), which keeps every excluded case a tangency and every
included case interior-realised.

## 6. Evidence grades

| item | grade |
|---|---|
| `F(1/4) = {N in {3,4,7,9}}`, 30 offsets | **proof** (window argument) + **exact computation** (direct `Q(sqrt3)`, agrees) |
| 723 edges, degrees 12..30, max clique 4 | exact computation |
| `G[P]` not 6-colourable at `a = 1/4` | **machine certificate**: cadical UNSAT + drat-trim `s VERIFIED` with the accepted checker; **pending independent audit** |
| interval `(1/5, 1/sqrt12)` and its endpoint tangencies | **proof** from homothety + exact per-ring values; **conditional** on the `a = 1/4` certificate |
| union `(1/sqrt28, 1/2]` | **conditional**: needs both machine certificates accepted and the earlier `T^2` result |
| whole-plane chromatic consequences | **none** — nothing here bounds `chi(R^2)` in either direction |

## 7. Artefacts and reproduction

    python3 a_quarter.py     # 3.02 s total

| file | sha256 |
|---|---|
| `p25.cnf` | `4d5d07d62ddfb89db4706ad46ab7e68fac210f94c8399586f32e146d608e59ca` |
| `p25.drat` (3,425,541 bytes) | `12a72a7ae61e50f40a0d9948b0d96fd906d25b1c04ec7a15294bfc7fc7b6549d` |
| `tools/drat-trim` (identical to the accepted binary) | `a9571deb08430a3d7f7a72074440f53e2ad48196dced50b146835052a18e9066` |

Also: `a_quarter_cert.json` (graph parameters, forced offsets, decision, drat tail, hashes),
`a_quarter.out` (full log), `a_quarter_hashes.txt`, `PREREG-A-QUARTER.md`.

**Not done, by instruction:** no second `k`, no other patch, no other `a`, no core minimisation, no
re-run after the result. `rup.c` was not used; the accepted `drat-trim` was.
