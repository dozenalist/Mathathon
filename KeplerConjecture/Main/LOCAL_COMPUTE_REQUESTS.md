# Local computation handoff

The Astra supervisor runs Lean and heavy numerical work on the user's local
computer. Main collects requests from the four Kepler sessions and maintains
this queue. Submit the source and request in a pushed Kepler-only checkpoint,
then end the research turn when results are needed to proceed. The continuous
completion watcher wakes Astra to review the request and execute it locally.
Continue independent mathematical work while an already-submitted job runs.

## Queue

Two requests submitted 2026-11-14 from branch `kepler15/main`. Both are
**independent**: 001 is the numerical baseline, 002 is the Lean build. Neither
has been executed; nothing in `Main/CLAIMS.md` depends on them yet.

### K15-COMPUTE-001 — certified two-point LP in the Laguerre basis, d = 3

```text
request_id = K15-COMPUTE-001
status = REQUESTED
owner = C (Computation, session using-the-chats-in-mcl6) — script authored there;
        Main supplies the specification below
reviewer = X (Counterexamples, i-ve-attached-viazovska-f7hh)
claim_id = K15-C002 (control), and the Tier-1 question of Main/CLAIMS.md
source_commit = the pushed head of kepler15/main that carries this file
branch = kepler15/main (Main) or Computation/'s own branch, whichever C pushes
purpose = (a) reproduce the published d = 3 two-point value 0.779746762
          (occupied-volume units) with an independently written evaluator;
          (b) report the degree-versus-constant curve for the univariate
          reduction, and (c) state whether the optimum is *certified* (SOS,
          rational coefficients) or only sampled.
working_directory = repository root
input_files = KeplerConjecture/Computation/ce_laguerre.py (C to add),
              KeplerConjecture/Computation/README.md (conventions),
              KeplerConjecture/Main/CLAIMS.md (normalisation, K15-C007)
command = python3 KeplerConjecture/Computation/ce_laguerre.py --degree 40             --precision 60 --grid 2001 --out KeplerConjecture/Computation/out/
dependencies = python3 3.11+, numpy, scipy, mpmath, sympy; optional cvxpy or
               scs/mosek for the SDP; pin exact versions in the log
resources = 1 core, < 4 GB RAM, expect < 10 min at degree 40; abort above 30 min
parameters = dimension 3; basis phi_k(x) = exp(-pi r^2) L_k^{1/2}(2 pi r^2),
             k = 0..n, n in {12, 16, 20, 24, 30, 40}; t = 2 pi r^2;
             f = sum a_k phi_k, fhat = sum (-1)^k a_k phi_k;
             sign conditions f <= 0 on [4, inf) and fhat >= 0 on [0, inf)
             reduced to SOS on the half-line; degrees of the SOS multipliers
             n/2; precision 60 decimal digits; no random seed (deterministic)
expected_outputs = KeplerConjecture/Computation/out/ce_laguerre.json
             (coefficients, f(0), fhat(0), ratio, degree, solver status,
             residuals), out/ce_laguerre.txt (human table)
success_criteria = (1) the ratio 4 pi/3 * f(0)/fhat(0) at some n is <= 0.7798
             and decreases monotonically in n; (2) at least one n with the SOS
             certificate verified symbolically by sympy (exact rational
             coefficients, residual < 1e-40); (3) the run prints BOTH
             occupied-volume and centre-density values; (4) explicit statement
             of whether Li's 0.18398089 lower bound is approached from above
certification = whichever of: exploratory float, interval, exact SOS.
             A float optimum alone is `TESTED_FINITE` and cannot be promoted
remaining_obligations = global signs (the SOS identity is the certificate),
             tail (none in this reduction: the half-line SOS covers [4, inf)),
             and the passage from the univariate reduction to the multivariate
             admissible class, which must be stated as an inclusion, not asserted
```

Why this is worth a local run: it is the only way to turn `Main/DECISIONS.md`
D2/D4 from assertions into measurements, it is small (a univariate SDP), and it
either produces the first locally reproduced 3D number in this project or
explains exactly why not.

### K15-COMPUTE-002 — build the frozen definitions under the pinned toolchain

```text
request_id = K15-COMPUTE-002
status = REQUESTED
owner = M (Main), executed by Astra locally
reviewer = X
claim_id = K15-C001 (definitions), K15-C012 (constant, later)
source_commit = the pushed head of kepler15/main that carries this file
branch = kepler15/main
purpose = kernel-check the frozen scale definitions and the identity
          centreDensity = 3 * upperDensity / (4 pi) under Lean v4.35.0
working_directory = repository root
input_files = KeplerConjecture/Lean/Kepler15/Normalisation.lean
command = lake env lean KeplerConjecture/Lean/Kepler15/Normalisation.lean
          then, in a scratch copy of the file, append
          #print axioms Kepler15.centreDensity_eq
dependencies = Lean v4.35.0, Mathlib v4.35.0 (source checkout already present)
resources = 1 core, ~2 GB RAM, < 5 min after the Mathlib cache is warm
parameters = none
expected_outputs = KeplerConjecture/Lean/out/normalisation_build.log
success_criteria = exit status 0, no `sorry`, no warnings promoted to errors,
             and `#print axioms` output exactly
             [propext, Classical.choice, Quot.sound]
certification = Lean kernel (pinned toolchain only)
remaining_obligations = the module contains no analysis; it fixes notation.
             The Fourier transform and the Cohn-Elkies admissibility class are
             deliberately deferred to a second module.
```

**Pre-check already done (not a substitute).** The same file was elaborated on
the VM with Lean 4.33.1 and the VM's Mathlib: exit status 0, no diagnostics, and
`#print axioms Kepler15.centreDensity_eq` gives
`[propext, Classical.choice, Quot.sound]`. That is evidence of well-typedness,
**not** of the pinned build, and it is recorded as `LEAN_CONDITIONAL` evidence
only. Expect possible renaming in `Filter.limsup` / `MeasureTheory.volume`
between 4.33.1 and 4.35.0; the proof is one `unfold` + `field_simp`.

## Required request record

```text
request_id = K15-COMPUTE-001
status = REQUESTED | RUNNING | COMPLETE | FAILED | NEEDS_REVISION
owner = SAIR session ID and role
reviewer = independent session ID and role
claim_id = precise claim or baseline tested
source_commit = full pushed Git commit
branch = exact branch
working_directory = repository-relative path
input_files = explicit KeplerConjecture paths and checksums where useful
command = complete reproducible command with arguments
dependencies = pinned Lean/mathlib or numerical package versions
resources = requested wall time, threads, peak RAM, disk estimate
parameters = dimension, scale, degree, grid, precision, seed, tolerances
expected_outputs = explicit KeplerConjecture paths
success_criteria = expected assertions, residuals, signs, or theorem names
certification = exploratory floating point, interval, exact, or Lean kernel
remaining_obligations = global signs, tails, realization, proof gaps
```

For Lean, identify the actual `.lean` module, imports, exact target statements,
and declarations for `#print axioms`. The pinned project toolchain is Lean
v4.35.0 with Mathlib v4.35.0. Build/cache preparation is a local supervisor task.
Record compile exit status, complete relevant diagnostics, toolchain, source
hash, and axiom output. A successful unrelated root build gives no evidence
about an unimported Kepler file.

For numerical work, save compact coefficients and solver output along with
the generator. Report density normalization, objective, primal and dual
residuals, global-sign/tail certification status, and independent validation.
Request an initial small instance with a measured resource budget before
expanding a large solve. The supervisor will run feasible requests and return
logs or a concrete local limitation. Unexecuted jobs remain pending.

Main owns integration of this queue. Workers can put standalone requests in
their own role directories and identify them in the final response for Main
or Astra to collect.
