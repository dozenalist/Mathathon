# Exact fixture: the icosahedral 13-cluster

Role E. `K15-E050`. Status **PROVED (exact arithmetic)**. For X and C to reuse.

Everything here is exact; the decimals are for reading only. Verified symbolically with
`sympy` in this block.

## Coordinates

Let `phi = (1 + sqrt5)/2`. The unscaled icosahedron with vertices

```
(0, +-1, +-phi) ,   (+-1, +-phi, 0) ,   (+-phi, 0, +-1)
```

has edge `2` and circumradius

```
R0 = sqrt(1 + phi^2) = sqrt(2 + phi) = sqrt( (5 + sqrt5)/2 ) = 1.90211303259031...
```

Scale by `2/R0 = 2 sqrt2 / sqrt(5 + sqrt5) = 1.05146222423827...` to put the twelve vertices
at circumradius exactly `2`. The centre `c = 0` completes the cluster.

## The two numbers that matter

```
edge (mutual distance of adjacent outer centres)  =  4 sqrt2 / sqrt(5 + sqrt5)  =  2.1029244484765...
```

so the twelve outer balls are **not** mutually tangent — they are separated by
`2.102924... > 2`, while each is tangent to the central ball (`|w_i| = 2`). This is the
geometric reason the cluster is a legal packing but a frustrated one: the icosahedron cannot
be closed up, and the 12-neighbour shell is `0.1029` too wide to be an fcc/hcp contact
configuration.

The angle at an outer centre `w` between the directions to `c` and to an adjacent outer
centre satisfies, by the law of cosines on the `(2, 2, edge)` triangle,

```
cos(angle) = edge/4 = 0.52573111211913... ,      angle = 58.2825255885... deg ,
```

and the tangency check `|c - w_j| = sqrt(4 + edge^2 - 2*2*edge*cos(angle)) = sqrt(4) = 2`
holds **exactly** (verified symbolically). Note `cos(58.2825 deg) = edge/4`, so the angle is
determined by the edge alone — a useful simplification for any angular computation.

## Volumes, exact

```
V_dodeca   = (15 + 7 sqrt5)/4 * (4/sqrt(10 + 22/sqrt5))^3  =  5.55029102851551027...
sqrt(32)   =                                                5.65685424949238020...
deficit    = sqrt(32) - V_dodeca                           =  0.106563220976869926...
```

The centre's cell is the regular dodecahedron of inradius `1`, and by `K15-E045` it is
**exactly** `V_dodeca` in every saturated completion, so the deficit is exact and unavoidable.

## Thresholds derived from the fixture

```
cluster FCC-compatibility with A = 0 :   sum over 12 outer  >=  13 sqrt(32) - V_dodeca
                                                          =  67.98881421488544...
                                      mean over 12 outer  >=  5.66573451790710...
with A = sqrt(32) - vol Omega on c    :   sum over 12 outer  >=  12 sqrt(32)
                                                          =  67.88225099390856...
                                      mean over 12 outer  >=  sqrt(32) = 5.6568542495
```

The second row is worth recording: allowing the *smallest possible* positive correction at the
centre (which is exactly `A(c) = sqrt(32) - V_dodeca = 0.10656`) lowers the requirement only
from `67.9888` to `67.8823`, i.e. from mean `5.665735` to `5.656854 = sqrt(32)` exactly. It
does **not** remove the difficulty, because `sqrt(32)` is still above the dodecahedral floor
`5.550291`. So no choice of `A` at the defect avoids the `2 %` problem of `K15-E041`.

## Sanity values reproduced independently

| quantity | value | check |
| --- | --- | --- |
| centre cell in 12 completions | `5.550291028515513` | matches `V_dodeca` to `1e-15` |
| mutual distance of outer centres | `2.1029244484765` | `> 2`, legal |
| `|c - w_j|` | exactly `2` | tangent, as required |
| minimal separation in all fixtures | `2.0` | verified each run |
