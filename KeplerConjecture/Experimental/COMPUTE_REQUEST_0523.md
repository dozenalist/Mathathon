# Compute request — certify the B&B atom at the box sizes it actually needs

Filed by role E, `K15-REVIEW-0523-E`. Routed by Astra. Initial local cap 120 s; the runs
below are quoted for 1 CPU and ≤ 2 GiB.

## Pushed inputs

```
repo    https://github.com/dozenalist/Mathathon
branch  kepler15/experimental/run-01
commit  see REVIEW_0523.md §8 for the exact hash of this block
code    KeplerConjecture/Experimental/scripts/rational_interval.py
        KeplerConjecture/Experimental/scripts/rigorous_cell_volume.py
deps    python3 only: fractions, itertools, functools.  No numpy, no sympy, no mpmath.
        (mpmath is used ONLY in the self-tests of rational_interval.py as a reference value,
        never in a decision.)
```

## What is already validated (local, 6.6 s)

| control | enclosure | width |
| --- | --- | --- |
| cube `[-1,1]³` | `8` exact | 0 |
| fcc contact cell | `4√2` | `1e-18` |
| hcp contact cell | `4√2` | `1e-18` |
| C5 payer fixture | `5.898017371803720` | `9e-19` |

## What the run must decide

The box evaluation is **correct but too wide at the box size tried**: a `0.2° × 1°` box in
`(θ, φ)` returns `[5.7281, 6.0663]`, width `0.338`, because the interval centres' own error is
multiplied by `R` and summed over the twelve constraints. The true variation of the volume over
that box is of order `1e-4`, so the enclosure is dominated by dependency, not by geometry.

**Task.** For a geometric sequence of box widths `w = 2^-k`, `k = 0..16`, centred on
`(θ, φ) = (111.7975°, 36°)`, record the certified enclosure width. Report the smallest `w`
whose enclosure width is below `1e-3` (the scale a B&B needs) and the number of boxes of that
width needed to cover the legal family (the legal window is `θ ∈ [106°, 120°]`, `φ ∈ [22°, 36°]`).

That single curve converts "the atom works" into "the B&B needs N boxes", which is the number
the next block has to know.

```
CPU      <= 1 core
memory   <= 2 GiB
time     <= 120 s per box width, hard kill
output   per k: box width in degrees, certified [lo, hi], width of the enclosure
failure  a run that exceeds 120 s at some k reports the k it reached and stops; that is a
         useful answer, not a failure
```

## Not this request

Not a search for better completions, and not a proof of `(P')`. The volume of §2 is a
two-sided **enclosure**; only an enclosure can ever be part of a lower bound, and the searches
of the previous block (all upper bounds) cannot.
