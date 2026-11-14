# Compute request — global completion search around the frozen payer

Filed by role E, `K15-REVIEW-0353-E`. Routed by Astra; runs off-box.

## Why it is small

`REVIEW_0353.md` §2 proves that any centre able to cut `Ω(w1)` must satisfy
`|z − w1| < 2.603447`, and that the twelve fixture centres already block that shell almost
completely (certified covering radius `41.85°` against the `48.88°` needed). The search
space is a shell of width `0.6`, not a neighbourhood of space.

## Exact inputs (pushed)

```
code    KeplerConjecture/Experimental/scripts/c5_fixture.py
data    KeplerConjecture/Experimental/evidence/c5_fixture.json
commit  c76194f9abb914d9519ec86e0cb67a6cb55f85bb
fixture c=(0,0,0), w1=(0,0,2), 5 ring at (4/sqrt5 cos 72k, 4/sqrt5 sin 72k, 2/sqrt5),
        5 pentagon at w1 + 2(s cos(36+72k), s sin(36+72k), 3/8), s = sqrt55/8,
        south=(0,0,4)
```

## Task

Minimise `vol Ω(w1)` over 2-separated supersets of those twelve centres, i.e. over legal
`z` with `2 ≤ |z − w1| ≤ 2.7`.

Accept criterion: **a legal configuration with `vol Ω(w1) < 5.763417471` refutes `(P')` at
the icosahedral pair.** Anything at or above that value changes nothing.

## Caps

```
CPU     <= 1 core
memory  <= 1 GiB
time    <= 10 minutes per seed, 8 seeds, hard kill
output  best legal value, its configuration, min separation incl. pairs against w1,
        max|vertex| (must be < 2, or the ball is binding and the value is not a cell)
```

Every returned configuration must pass `c5_fixture.py`'s legality block before being
believed; a value below `V_dodeca = 5.550291029` is a bug, not a discovery.
