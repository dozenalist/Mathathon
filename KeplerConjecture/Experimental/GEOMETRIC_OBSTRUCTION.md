# The icosahedral compensation inequality: quantitative obstruction

Role E. `K15-E040`. Status **OBSTRUCTED (quantitative)**. The inequality is neither
proved nor refuted; the obstruction is stated exactly, with the certified brackets.
Scripts: `scripts/icosa_compensation_search.py`, `scripts/icosa_targeted_completion.py`.
Evidence: `evidence/icosa_compensation_search.txt`, `evidence/icosa_targeted_completion.txt`.

## The inequality

For `C = {v}` the dodecahedral centre, `Block(C) = C union N(C)` is the 13-cluster and
`(T')` reads `sum_{i=1..12} vol Omega(w_i) >= 13 sqrt(32) - 5.5502910285155`, i.e.

```
sum  >=  67.9888142149 ,        mean  >=  5.665734518 .
```

## What is provable from the certified local data — and it is not enough

`Omega(w) = { x : |x-w| <= |x-z| for all z }` and, for `x = w + t u`,

```
x in Omega(w)  <=>  t <= d_z / (2 cos phi_z)   for every other centre z with cos phi_z > 0,
```

where `d_z = |z-w|` and `phi_z` is the angle between `u` and `z-w`. Since every centre has
`d_z >= 2`, the bound `d_z/(2 cos phi_z) >= 1` holds whenever `cos phi_z > 0`, and the
directions with `cos phi_z <= 0` are unconstrained by any *known* centre. Hence

```
t(u) >= 1 for every u in S^2 ,        so        vol Omega(w) >= 4 pi / 3 = 4.188790205 .
```

**This is exactly what local distance data can give, and no more.** The six known
neighbours of an outer centre cannot improve it, because in every direction either a
neighbour constrains `t` to `>= 1` or no known neighbour constrains it at all. So the
inscribed-ball bound is *optimal for the information available from the 13-cluster alone*,
and it falls short by

```
13 sqrt(32) - 5.5502910285 - 13 (4 pi / 3) = 19.08483258 .
```

Certified bodies disjoint inside the outer cells therefore cannot close `(T')`: the largest
body certifiable from the cluster is the unit ball, and any refinement must use information
about the *completion*, not about the cluster. Recorded as the first half of the
obstruction.

## The bracket, with both directions

| quantity | value | status |
| --- | --- | --- |
| absolute floor on any mean cell volume (dodecahedral theorem) | `5.550291029` | proved elsewhere, imported |
| `(T')` threshold mean | `5.665734518` | required |
| best certified **lower** bound from local data | `4.188790205` | proved here |
| best computed **upper** bound (targeted completion) | `8.321262` | `TESTED_FINITE` |
| best computed upper bound (random completions) | `8.167277` | `TESTED_FINITE` |

So the true value of the infimum over completions lies in `[4.18879, 8.16728]` per cell —
a window of factor `1.987` — and the threshold `5.665735` sits inside it. **The inequality
is not decidable from the information currently certified.** That is the quantitative
obstruction.

## Why the completions are far above the threshold, and why that is suspicious

The threshold mean is only

```
5.665734518 / 5.550291029 = 1.0207995  ,   i.e. 2.080 % above the global minimum cell volume.
```

`(T')` therefore demands that **every one of the twelve outer cells be within 2.08 % of the
smallest Voronoi cell that any packing admits**. That is a near-extremal requirement on
twelve specific, non-generic cells. Two consequences:

1. It is *implausible*, and I expect `(T')` to be **false**; but the computed upper bounds
   (`8.17`–`8.32`, i.e. `47 %` above threshold) are nowhere near a refutation, because a
   finite completion only gives an upper bound and ours are undersaturated (density `0.10`
   against `0.177` for fcc).
2. It explains why the icosahedral block is the wrong block. A 13-member block asks twelve
   cells to be near-extremal *simultaneously*, while the deficit being repaid is only
   `0.1066`. The compensation is real but diffuse, and a one-step block cannot see it.

## Corrected condition (derived from the obstruction, not guessed)

Enlarge the block to two steps and let the deficit be repaid by the **second** shell:

```
Block2(C) = C  union  N(C)  union  N(N(C)) ,
D(C) = sum_{v in C} (sqrt(32) - vol Omega(v))                       (unchanged)
S2(C) = sum_{w in Block2(C) \\ C} ( vol Omega(w) - sqrt(32) )       (two shells of surplus)
(T'-2)   S2(C) >= D(C) .
```

Since `S2 >= S` termwise, `(T'-2)` is **strictly weaker** than `(T')`, and the price is a
larger block: `diam Block2(C) <= diam(C) + 4 (2.09)`, which raises the boundary constant in
`K15-E001` Step 2 but does not affect any certified count. This is the corrected condition
the fallback asks for, and it is derived from the measured gap rather than assumed.

## Fixtures recorded

- `centre = 5.5502910285155` reproduced in **every** run, matching `K15-E002` to `1e-15`.
  This is the control that the completion construction did not disturb the core.
- `minsep = 2.0` verified in every accepted configuration.
- Targeted rings at polar angle `62 deg` and `70 deg`, `5`–`7` points per outer centre,
  azimuthal offsets `0`, `pi/6`, `pi/3`: all accepted, none reduced the sum below `99.8`.
  Placing neighbours at distance `2` in the free outward hemisphere is therefore **not**
  the lever that controls these cells.

## What would settle it

A certified lower bound of the form `vol Omega(w) >= Phi(neighbour data)` with
`Phi > 5.665735` on the outer configuration, where `Phi` uses the *count* of neighbours
within `2.09` (at most `12`, from `K15-E014`) plus the angular data. That is a
kissing-with-tolerance estimate with an angular constraint, and it is the next missing
inequality. Offloaded as `LOCAL_ICOSA_SEARCH.md`.
