# Gaussian normalization and solver audit

Source `87db0319217b99eafd66d96fff0e9ab75caa2127`, completion 41644. Reviewed
November 14, 2026, in the 00:08 Pacific hourly check by Astra and an independent
mathematical auditor. Original scripts are frozen in `source/` for reproduction.

For `f(x)=P(|x|^2) exp(-|x|^2)` and
`fhat(t)=pi^(3/2) Q(pi^2|t|^2) exp(-pi^2|t|^2)`, the density expression is
`4 P(0)/(3 sqrt(pi) Q(0))`. The submitted expression is too large by a factor
of pi. With positive constant terms, comparison with the Kepler value is
`32 P(0)^2 < pi^3 Q(0)^2`.

The claimed infeasibility of the fixed Gaussian family is false. The exact
example `P(s)=2-2s/3`, `Q(v)=1+2v/3` has `Q(0)=1`, `P(s)<=-2/3` for `s>=4`,
and `Q(v)>=1` for `v>=0`. It is a feasible control, not a competitive bound.

The actual degree-six model accepts this point with minimum numerical slack
about 0.6667. A local SciPy/HiGHS call returns **Model error**, not a mathematical
infeasibility certificate. The matrix has entries as large as `3.71e15`.
Scaling and solver-status handling must be repaired before drawing conclusions.

```powershell
python KeplerConjecture/Counterexamples/Reviews/41644/check_gaussian.py
```

Versions: Python 3.12.14, NumPy 2.3.5, SciPy 1.16.3, SymPy 1.14.0. Run with
one BLAS/OpenMP thread. The recorded run took less than a second and
exited 0. Exact algebra establishes feasibility; the finite numerical test
documents the submitted driver's failure mode. See [audit.json](audit.json).
