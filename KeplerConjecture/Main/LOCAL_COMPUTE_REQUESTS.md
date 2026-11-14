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

### K15-COMPUTE-001 (rev. 2) — exact SOS certificate for a two-point profile, d = 3

Revision 2 after review objections 4, 7 and 8. The rev. 1 specification had the
variable mismatch `t = 2πr²` against a sign interval starting at 4; it also asked
for a sympy check of a floating-point optimum, which is not a certificate, and it
used language that could be read as expecting convergence to Li's lower bound.

```text
request_id = K15-COMPUTE-001
status = REQUESTED (rev. 2)
owner = C (Computation, using-the-chats-in-mcl6)
reviewer = X (Counterexamples, i-ve-attached-viazovska-f7hh)
claim_id = K15-C002 control; no new bound is claimed
source_commit = the pushed head of kepler15/main that carries this revision
working_directory = repository root
input_files = KeplerConjecture/Computation/ce_laguerre.py  (runnable; sha256 in
              Computation/out/MANIFEST.txt), KeplerConjecture/Main/CLAIMS.md
command = python3 KeplerConjecture/Computation/ce_laguerre.py --degree 8             --grid 1200 --tmax 40 --out KeplerConjecture/Computation/out/ce_d8.json
dependencies = python3 >= 3.11, numpy, scipy (scipy.sparse.linalg), sympy;
              record exact versions with `pip freeze`
resources = 1 core, < 2 GB RAM; the submitted instance runs in 1.1 s. The
              SDP/SOS instance at degree n <= 24 should be capped at 15 min and
              is expected to need < 4 GB.
parameters = s = |x|^2 >= 0; Laguerre argument t = 2*pi*s.
              (A1) f <= 0 for |x| >= 2  <=>  P(t) <= 0 for t >= 8*pi  [NOT 4]
              (A2) fhat >= 0           <=>  Q(t) >= 0 for t >= 0
              f = sum_{k<=n} a_k exp(-pi s) L_k^(1/2)(t),
              fhat = sum_k (-1)^k a_k exp(-pi s) L_k^(1/2)(t),
              c_k = L_k^(1/2)(0) = (2k+1) C(2k,k)/4^k, fhat(0) > 0 required.
expected_outputs = Computation/out/ce_<n>.json (coefficients, f(0), fhat(0),
              ratio, both normalisations, solver status, residuals) and
              Computation/out/ce_<n>.txt
success_criteria = ONE of:
              (a) an exact rational identity -P(t) = s0(t) + (t - 8*pi) s1(t) and
                  Q(t) = u0(t) + t u1(t) with s_i, u_i sums of squares of
                  polynomials with rational coefficients (pi treated as a formal
                  transcendental; any pi^2 appearing is reduced via pi^2 = pi*pi
                  and the identity checked coefficient-wise), verified by exact
                  arithmetic; or
              (b) a rigorous residual bound on the whole half-line.
              A floating-point optimum is EXPLORATORY and must be labelled so.
certification = exact or none. `TESTED_FINITE` at best for a float optimum.
remaining_obligations = the reduction from the univariate family to the full
              admissible class must be stated as an inclusion and proved;
              Li's theorem bounds the optimum of ordinary CE and says nothing
              about convergence of this particular sequence - do not compare
              a finite-degree value with 0.18398089 as if it were a limit.
```

**Already run on the VM (exploratory, negative result).** The submitted script
implements the *grid* version of the two sign conditions and demonstrates that
this approach cannot work: the LP is unbounded below, and with the rigorous floor
`f(0) >= 3/(32 pi)` forced it attains the floor with fine-grid violations of
order `10^10`. See K15-C014 and `Computation/out/ce_d8.json`. The lesson is
carried by rev. 2 above: the identity, not the grid.

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
