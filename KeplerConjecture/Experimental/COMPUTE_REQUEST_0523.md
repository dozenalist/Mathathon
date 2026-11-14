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

**Already measured locally, so this request is now smaller than first drafted.** The scaling is
linear in the box width, and the lower end is useful even at a coarse box:

```
width 0.1 deg      -> certified [5.871272, 5.924619]     (lower end is 0.108 ABOVE the threshold 5.763417)
width 0.025 deg    -> certified [5.891298, 5.904634]
width 0.003125 deg -> certified [5.897134, 5.898801]
```

**Task (what remains).** Certify the whole legal `(θ, φ)` window — `θ ∈ [106°, 120°]`,
`φ ∈ [22°, 36°]` — with `0.1°` boxes: `(14/0.1)² ≈ 2×10⁴` boxes, each asking only
"is the certified lower end above `5.763417470`?"  Report the number of boxes that fail.

**Before spending that, read this.** The sandwich is dependency-dominated: on a `1°×1°` box it
certifies width `0.53` when the true variation is `9e-7` (ratio `6e5`), and a parameter
Lipschitz bound would give about `4e-3` per degree — ~130× better over the legal window. If
Astra can differentiate `V` in `(θ, φ)` with interval arithmetic, the `2e4`-box count collapses
by two orders of magnitude and this request should be re-scoped before it is run.

That is the complete certification of the C5 family, and it is cheap. What it is **not** is a
bound over completions: the domain of `REVIEW_0523` §3 has up to 200 coordinates, and the
atom's cost per box (≈10 s in pure Python) is irrelevant next to the box count at that
dimension. The dimension, not the atom, is the obstruction, and this request deliberately does
not pretend otherwise.

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
