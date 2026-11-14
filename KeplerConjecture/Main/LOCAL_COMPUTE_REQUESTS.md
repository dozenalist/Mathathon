# Local computation handoff

The Astra supervisor runs Lean and heavy numerical work on the user's local
computer. Main collects requests from the four Kepler sessions and maintains
this queue. Submit the source and request in a pushed Kepler-only checkpoint,
then continue an independent subtask where possible. The 45-minute scheduled
supervisor check collects the request and executes it locally; Sair-Watch
has been retired for this project by the latest user instruction.
Continue independent mathematical work while an already-submitted job runs.

## Queue

`Main/` owns the queue. IDs are distinct per role from this cycle onward; the old
shared `K15-COMPUTE-001/002` names are retired and mapped at the bottom.

| ID | Owner | Purpose | State |
| --- | --- | --- | --- |
| `M-LEAN-001` | M | pinned Lean 4.35.0 build of `Lean/Kepler15/Normalisation.lean` | **COMPLETE** — exit 0, axioms `[propext, Classical.choice, Quot.sound]`, algebraic identity only |
| `M-NUM-001` | M | degree-8 grid control in `Computation/ce_laguerre.py` | **COMPLETE but INVALID as a claim** — script omitted Fourier positivity (K15-C014r); repaired variant locally re-run gives `f(0) = 0.2182024…` |
| `C-NUM-001` | C | CE control, `K = 31/41`, grids 1200/4000 | **COMPLETE, `TESTED_FINITE`** — `Δ = 0.779702445785607`, `0.779745768082807`; `min f̂ ≈ −3·10⁻⁶` |
| `C-CERT-001` / `K15-C-REQ-002` | C | exact Sturm sign driver and K21 verification | **COMPLETE: REFUTED** — exact negative Fourier witness; ladder deferred until checker repaired; `Computation/Reviews/48443/` |
| `E-CERT-001` | E | interval certification for cluster cell volumes | **REQUESTED — driver missing** (Q3) |
| `X-R01` | X | rational Gaussian driver | **DIAGNOSTIC COMPLETE; NEEDS_REVISION** — exact feasible control, factor-pi error, solver Model error; `Counterexamples/Reviews/41644/` |
| `M-NUM-002` | M | rational SOS certificate for a frozen profile | **SPECIFIED, superseded by C-CERT-001** |

The 00:08 Pacific hourly review completed both actionable diagnostic jobs locally.
No job remains running. The requested degree ladder was not extended after its
certification prerequisite failed. New bounded offloads for the repaired checker,
Gaussian driver and shell-count benchmark are assigned but not yet submitted.
No new Lean source arrived in the four reviewed completions.

Publication supplement: C's repaired checker suite passed locally in 21 seconds;
full independent validation remains open. E's floating shell diagnostic and X's
one-iteration driver were run, and X's rational-truncation bug was reproduced.
See `LocalChecks/2026-11-14_0008/`. New requests `K15-C-REQ-003` and
`K15-EXP-002` explicitly refer to unwritten `shell_bench.py` and
`tammes13_enclosure.py`; their state is **NEEDS_IMPLEMENTATION**. No heavy job
is waiting on an executable handoff, and no local job remains running.

### M-NUM-002 — rational SOS certificate, revised specification (not to be run before C-CERT-001)

The rev. 2 text of the old `K15-COMPUTE-001` was not a coherent certificate
specification: with rational `P` and rational sums of squares, a factor
`(t − 8π)` carries irrational coefficients. Three coherent options; pick one and
say which:

1. **Conservative rational threshold.** Prove `−P(t) = Σ_i s_{0,i}(t)² + (t − 25)Σ_i s_{1,i}(t)²`
   with `t = 2πs`. Since `25 < 8π = 25.1327…`, this implies `f ≤ 0` for
   `t ≥ 8π`, i.e. for `|x| ≥ 2`. Purely rational, exact expansion check, no PSD
   matrix needed (a univariate sum of squares *is* the certificate).
   Cost: the threshold is stronger than needed, so the constant is slightly worse.
2. **Formal `π`.** Verify the identity in `ℚ[t, π]` treating `π` as a
   transcendental: both sides are polynomials in `(t, π)` and the identity is
   checked coefficient-wise. Requires the certifier to accept a two-variable
   coefficient ring. Do **not** write "`π² = π·π`" as if it were machinery.
3. **Rational Gaussian scaling.** Replace `e^{−πs}` by `e^{−s}` and re-derive the
   Fourier map (`φ̂(t) = π^{-3/2}·…`); then all constants become rational
   multiples of `π^{3/2}` and the certificate lives in `ℚ(√π)`. Requires the
   re-derivation to be written out and reviewed first.

Acceptance for any of the three: exact rational identity, verified by an
independent checker, with the sign regions `s ≥ 4` and `s ≥ 0` stated in `s`
(never mixed with `t`), and `f̂(0) > 0` exhibited.

### C-SHELL-001 — same-degree comparison at `η = 0` vs `η > 0` (K15-C018)

Only a request if C's Sturm driver (C-CERT-001) exists; otherwise it stays a
specification. Same degree, same grid, same normalisation on both sides, so the
two numbers differ only by the relaxation.

```text
request_id = C-SHELL-001
status = BLOCKED on C-CERT-001
owner = C (Computation, kepler15/comp-01a1d8c0)
reviewer = X, then M
claim_id = K15-C018 (benchmark; not a bound until the count 12 is certified)
purpose = measure whether a small allowance eta at rho = 2.09 buys more than the
          12 eta / fhat(0) it costs, at fixed degree and fixed basis
inputs   = a rational profile from C-CERT-001 at degree K <= 12,
           plus its eta-shifted variants f -> f - eta on [2, rho] (i.e. the
           profile whose value on the shell is capped at eta)
success  = (4 pi/3)(f(0) + 12 eta)/fhat(0) computed for eta in {0, eta_1, eta_2}
           with eta_j chosen so f stays admissible, all three verdicts exact
blocking = rho = 2.09 needs a Tammes-13 enclosure; without it the count 12 is a
           hypothesis, not an input
certification = exact (Sturm) or none
```

### M-QUEUE-001 — claims that must be re-anchored when the review lands (M)

Not a computation: `Main/HOURLY_REVIEW_2026-11-14_0008.md` and
`Computation/Reviews/48443/` were announced but are absent from the fetched
branches. When they appear, K15-C017's witness
(`q(57955199/21687900) ≈ −3.876231892749308e−5`) must be replaced by a citation of
the pushed artifact plus its hash, and the K21 source hash re-checked.

### Previously queued, unchanged

`C-CERT-001` (exact Sturm driver — the single highest-value item in the project),
`E-CERT-001` (interval certification for cluster volumes; driver still missing),
`X-R01` (exact optimisation over the Laguerre family), `M-NUM-002` (rational SOS
specification; superseded by C-CERT-001). `M-LEAN-001` and `C-NUM-001` are
complete; `M-NUM-001` is complete and invalid as a claim (K15-C014r).

### Retired IDs

`K15-COMPUTE-001` → split into `C-CERT-001` (the real work) and `M-NUM-002`
(this specification). `K15-COMPUTE-002` → `M-LEAN-001`, complete.

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


## Supervisor execution evidence at hourly transition

The local execution record is in "Computation/Reviews/27616/README.md" and "Lean/Review/27616/README.md". These record the actual sources, commands, three grid controls, remaining sign violations, and the normalization-only Lean check. New certificate claims on the Computation branch are awaiting independent local review.
