# A nonzero open interval in `a` carrying the same 6-UNSAT certificate

**Status: CANDIDATE at supervisor level.** Everything below is conditional on the independent geometry
audit accepting the 73-cell 6-UNSAT certificate (`patch19.py`, `p19.cnf`, `p19.drup`, `rup.c`). One
single-process calculation (`interval_a.py`, 0.92 s, well under the cap); no SAT search, no size sweep,
no core minimisation, no 7-UNSAT work in this block.

## 1. The interval

    a  in  ( 1/sqrt(28) , 1/sqrt(19) )  =  ( 0.188982237 , 0.229415734 )

an open interval of length `0.040433`, containing `a = 1/5 = 0.2` with margins `0.011018` below and
`0.029416` above. For **every** `a` in it, all 42 forced offsets of `F(1/5) = {v : N(v) in
{4,7,9,12,13}}` are still **strictly** forced, so:

> the 888 edges of the patch graph are unchanged, the CNF `p19.cnf` is unchanged, and the 42109-step
> refutation `p19.drup` applies verbatim: **no colouring of the plane that is constant on the
> interiors of the honeycomb cells at that `a` uses six colours.**

A modest rational closed subinterval, with strict endpoint margins in exact integer arithmetic:

    a in [19/100, 11/50] = [0.19, 0.22]  :  (19/100)^2 = 361/10000 > 1/28 (361*28 = 10108 > 10000)
                                            (11/50)^2  = 484/10000 < 1/19 (484*19 =  9196 < 10000)

Both endpoints of the open interval are genuine: at `a = 1/sqrt28` the ring-4 offsets have
`dmax = 1` exactly, and at `a = 1/sqrt19` the ring-13 offsets have `dmin = 1` exactly, so in both
cases forcing fails (see §3).

## 2. Derivation (homothety, then intersect finitely many strict inequalities)

The configuration at parameter `a` — triangular lattice of spacing `a sqrt3` together with its
Voronoi hexagons of circumradius `a` — is the image of the `a = 1` configuration under the homothety
`x |-> a x`. Hence for every lattice offset `v`

    dmin(v,a) = a * mu(v),    dmax(v,a) = a * nu(v),     mu := dmin(.,1),  nu := dmax(.,1),

so `v` is strictly forced at `a` iff `dmin < 1 < dmax` iff

    1/nu(v)  <  a  <  1/mu(v).

Intersecting over the finitely many offsets actually used by the certificate (42 of them, §2.1):

    a in ( max_v 1/nu(v) , min_v 1/mu(v) )  =  ( 1/ min_v nu(v) , 1/ max_v mu(v) ).

Exact values at `a = 1`, computed in `Q(sqrt3)` and **constant on each ring** (checked, not assumed;
`D6` acts transitively on a ring):

| ring `N` | `mu^2 = dmin^2` | `nu^2 = dmax^2` | vectors |
|---|---|---|---|
| 4 | 3 | **28** | 6 |
| 7 | 7 | 43 | 12 |
| 9 | 12 | 49 | 6 |
| 12 | 16 | 64 | 6 |
| 13 | **19** | 67 | 12 |

All five values are rational, so the endpoints are the exact radicals `1/sqrt28` and `1/sqrt19`.
`min nu^2 = 28` (ring 4) sets the lower endpoint; `max mu^2 = 19` (ring 13) sets the upper one.

### 2.1 The 42 offsets are exactly the ones the certificate uses

Recomputed from `patch19_cert.json`: the 888 recorded edges realise exactly **42 distinct offsets**,
and that set equals `F`. This matters because the edge set is the *combinatorial* condition
`{(u,w) in P^2 : w-u in F}` — it does not mention `a`. So the CNF, and therefore the refutation, is
literally the same file for every `a` in the interval.

## 3. Cross-check without homothety (the step that could be wrong)

Trusting `dmin(v,a) = a mu(v)` is where an error would hide, so the script recomputes `dmin^2` and
`dmax^2` **directly from the geometry at each `a`** (point-to-segment distances on the scaled
hexagons, exact `Q(sqrt3)`), for all 42 offsets:

| `a` | all 42 strictly forced? | note |
|---|---|---|
| 0.188 (just below) | **no** | ring-4 offsets fail: `(-2,0),(-2,2),(0,-2),(0,2)` |
| 19/100 | yes | rational endpoint |
| 1/5 | yes | |
| 11/50 | yes | rational endpoint |
| 0.230 (just above) | **no** | ring-13 offsets fail: `(-4,1),(-4,3),(-3,-1),(-3,4)` |

The failing offsets just outside the interval are exactly the rings that set the two endpoints, which
is the expected signature of a correct bound. The direct computation agrees with the homothety-derived
interval at both ends.

## 4. Why strict interior distances remove the boundary-ownership question

`dmin(v) < 1 < dmax(v)` is realised by **interior** points: interiors are dense in their closures, so
the distance function on `int C_0 x int C_v` has the same infimum and supremum, and being continuous
on a connected domain its image is an interval, hence contains every value strictly between them — in
particular `1`. Two interior points belong to their cells under **every** ownership rule, so the
violation is unconditional.

This is exactly why the interval is stated with strict inequalities and why the endpoints are
excluded: at the endpoint the unit distance is attained only at tiling **vertices**, whose owner
depends on the rule (the ring-3 tangency analysis of `CELL-A-FIFTH.md` is the same phenomenon). No
boundary rule is needed anywhere in this argument, and none is assumed.

One consequence worth stating: on the part of the interval with `a > 1/5` the forced set is strictly
**larger** than `F(1/5)` (e.g. ring 3 becomes strictly forced once `a > 1/5`, since `nu^2 = 25`).
Extra forced offsets only add edges, so `G_a[P] ⊇ G_{1/5}[P]` and the refutation still applies. On the
part below `1/5` some rings drop out, but all 42 stay, which is all the certificate needs.

## 5. Scope — two separations that must not be blurred

* **Family exclusion, not a chromatic bound.** The statement is: no colouring *constant on the
  interiors of these honeycomb cells* at such an `a` uses six colours. It says nothing about
  `chi(R^2)`. The plane's own bound `6 <= chi <= 7` is untouched, and nothing here is evidence for or
  against `chi(R^2) = 6`.
* **Six colours only.** The claim is 6-UNSAT. The earlier `chi(G[P]) = 8` figure is **uncertified and
  unnecessary**: it came from two CDCL decisions with no proof certificate, and the family exclusion
  needs only the certified 6-UNSAT. It is not used anywhere in this document.

## 6. Evidence grades

| item | grade |
|---|---|
| `dmin(v,a) = a mu(v)`, `dmax(v,a) = a nu(v)`; interval = intersection of `(1/nu(v), 1/mu(v))` | **proof** (homothety + finite intersection) |
| per-ring `mu^2, nu^2` values, ring-constancy, `max mu^2 = 19`, `min nu^2 = 28` | **exact computation** in `Q(sqrt3)`, one process, 0.92 s |
| the 42 offsets are exactly the offsets used by the 888 edges | **exact computation** from `patch19_cert.json` |
| interval `(1/sqrt28, 1/sqrt19)` and subinterval `[0.19, 0.22]` | **exact** — rationals and rational intervals; margins as exact integer inequalities |
| direct-geometry cross-check at both ends | **exact computation**, independent of the homothety step |
| "no six-colouring constant on cell interiors for `a` in that interval" | **conditional** on independent acceptance of the 73-cell 6-UNSAT certificate |
| `chi(G[P]) = 8` | **uncertified, unused** |

## 7. Reproduce

    python3 interval_a.py     # -> interval_cert.json, interval_a.out (0.92 s)
