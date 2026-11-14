# Local pilot request — minimise vol D' over the admissible six-direction sets

Filed by role E, `K15-REVIEW-0653-E`. All heavy scans go through Astra from now on.

## Immutable inputs

```
repo      https://github.com/dozenalist/Mathathon
branch    kepler15/experimental/run-01
commit    549660ab99e8d1879f3cba526d5aa0c5f1a0ecb4
code      KeplerConjecture/Experimental/scripts/premise_audit.py
          KeplerConjecture/Experimental/scripts/cell_certificate.py
          KeplerConjecture/Experimental/scripts/rational_interval.py
deps      python3 with numpy and scipy only (ConvexHull); no Lean, no network.
```

## Exact command

```
python3 Experimental/scripts/premise_audit.py 600
```

## Caps

```
CPU      <= 1 core
memory   <= 1 GiB
time     <= 120 s per start,  600 s total, hard kill
```

## What is already known locally (25 s, 1 CPU)

```
C5 configuration                5.572649
local search from C5            5.567413
six random legal restarts       5.567434 ... 5.567420   (all within 2e-5)
premise needed                  5.540000      slack +0.0274
V_dod                           5.550291
```

## Expected output

The minimum `vol D'` found, the configuration attaining it, and whether any start falls below
`5.5400`. A run that reports a value below `5.5400` **refutes the premise** and with it the
conditional twelve-face theorem; a run that stays above it strengthens the evidence but does not
prove it. Both outcomes are useful; neither is a proof.

## Not this request

Not a Lean build, and not a certification: `premise_audit.py` maximises over configurations with
floating point and by descent, so its output bounds the minimum from **above** only.
