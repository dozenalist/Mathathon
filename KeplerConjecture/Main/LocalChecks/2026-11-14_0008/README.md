# Checks of repairs received during publication

The four workers completed their assigned block while the 00:08 Pacific review
was being published. Their pushed commits were merged with authorship retained.
These small checks do not start another prompt cycle. Full reconciliation by
Main and independent proof review remain for the next hourly check.

| Job | Result | Scope |
| --- | --- | --- |
| C repaired checker regression suite | Exit 0, all tests pass, 21.2 seconds | Includes 24 random candidates checked on finite sample points; **not** a proof of verifier correctness or a new certificate |
| E shell diagnostic | Exit 0, 0.2 seconds | Exact endpoint `23681/43681` and floating angle about 57.170902 degrees; **no directed enclosure** of the Tammes constant |
| X degree-six driver, one iteration | Exit 0, 2.3 seconds | Feasible control accepted; optimization still reports a HiGHS Model error; no new candidate |
| X comparison helper regression | Exit 0, 2.0 seconds | Reproduces another bug: positive rationals are truncated to integers before comparison |

For the last test, `P(0)=99/100`, `Q(0)=1` gives exact left side
`32 P(0)^2=19602/625 > pi^3`, but `kepler_ok` returns true after applying
`sympy.Integer`. This is a counterexample to the comparison helper, not a
claimed feasible sphere-packing certificate. Replace the truncation with exact
rationals and use a directed pi comparison before relying on the helper.

The E script's name and prose suggest interval arithmetic, but it uses ordinary
high-precision `mpmath` floats and the rounded value 57.1367. Its rational endpoint
check is exact; its angle comparison is illustrative. The requested
`tammes13_enclosure.py` is explicitly unwritten. Likewise, C's proposed
`shell_bench.py` is explicitly unwritten. Those are **NEEDS_IMPLEMENTATION**,
not runnable heavy jobs and not results.

Source hashes, exact commands, exit codes and time caps are in [jobs.json](jobs.json).
Python 3.12.14, NumPy 2.3.5, SciPy 1.16.3, SymPy 1.14.0, mpmath 1.3.0;
one OpenMP/BLAS thread. All subprocesses finished and none remains running.
The raw logs retain worker wording without endorsing every status label.

Reproduce from the project worktree using:

```powershell
python KeplerConjecture/Main/LocalChecks/2026-11-14_0008/run_checks.py
```

The runner refers to current canonical files and must be used at this integration
revision or with the exact worker sources recorded in `jobs.json`. Earlier
rejected inputs remain frozen in the separate completion review directories.
