# Local computation handoff

The Astra supervisor runs Lean and heavy numerical work on the user's local
computer. Main collects requests from the four Kepler sessions and maintains
this queue. Submit the source and request in a pushed Kepler-only checkpoint,
then end the research turn when results are needed to proceed. The continuous
completion watcher wakes Astra to review the request and execute it locally.
Continue independent mathematical work while an already-submitted job runs.

## Queue

`Main/` owns the queue. IDs are distinct per role from this cycle onward; the old
shared `K15-COMPUTE-001/002` names are retired and mapped at the bottom.

| ID | Owner | Purpose | State |
| --- | --- | --- | --- |
| `M-LEAN-001` | M | pinned Lean 4.35.0 build of `Lean/Kepler15/Normalisation.lean` | **COMPLETE** — exit 0, axioms `[propext, Classical.choice, Quot.sound]`, algebraic identity only |
| `M-NUM-001` | M | degree-8 grid control in `Computation/ce_laguerre.py` | **COMPLETE but INVALID as a claim** — script omitted Fourier positivity (K15-C014r); repaired variant locally re-run gives `f(0) = 0.2182024…` |
| `C-NUM-001` | C | CE control, `K = 31/41`, grids 1200/4000 | **COMPLETE, `TESTED_FINITE`** — `Δ = 0.779702445785607`, `0.779745768082807`; `min f̂ ≈ −3·10⁻⁶` |
| `C-CERT-001` | C | exact Sturm sign driver in the Laguerre family | **REQUESTED** (Q1, Q2) |
| `E-CERT-001` | E | interval certification for cluster cell volumes | **REQUESTED — driver missing** (Q3) |
| `X-R01` | X | exact optimisation over the Laguerre family (semialgebraic) | **SPECIFIED** in X's registry; not run |
| `M-NUM-002` | M | rational SOS certificate for a frozen profile | **SPECIFIED, superseded by C-CERT-001** |
| `M-CERT-002` | M | rigorous cubic-remainder bound for `C142`'s `L1` | **REQUESTED** (spec below) |

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

### C-SHELL-001c — how to propose a candidate (after K15-C022)

Do **not** propose by a dense grid LP: at degree 6 it returns a box vertex without
`p(0) >= 0`, and objective exactly `0` with it (K15-C022). Two proposers that can
work:
(a) **exact Sturm bisection**: fix a small parametric family (e.g. `p` of degree
`K` with roots pinned at `u = 13.5` and a movable double root), and bisect on the
parameter with exact sign verdicts at each step;
(b) **SOS/SDP**: minimise `p(0) + n*eta` subject to
`q = s_0 + u s_1`, `-p + eta = t_0 + (u - T_LO)(T_HI - u) t_2 + (u - T_HI) s_3` with
`s_i, t_j` sums of squares, then round the Gram data to rationals and let
`shell_check` decide. The second is the only one that scales past degree ~10.

### C-SHELL-001b — exact checker is now in the tree (use it)

`Computation/shell_check.py` (new, runnable, no heavy numerics): rational profile
`a` in the basis `u = π|x|²`, i.e. `f = e^{-π|x|²} Σ a_k u^k`, Fourier map `b = M a`
with `M` rational (verified against the Hermite–Laguerre eigen-relation for
`k ≤ 2`), then exact Sturm verdicts for `q ≥ 0` on `u ≥ 0`, `p ≤ η` on
`[12, 27/2]`, `p ≤ 0` on `[27/2, ∞)`, and a directed-`π` output interval.
Reproduce: `python3 KeplerConjecture/Computation/shell_check.py --self-test`
(1.3 s, 1 core, stdlib+sympy). C's optimiser should emit candidates in exactly
this format so that the same file certifies them; X should audit it before any
number is quoted.

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


### M-LEAN-002 — pinned build of `Lean/Kepler15/Volume.lean` (ball-volume identity)

```text
request_id = M-LEAN-002
status = REQUESTED
owner = M (Main); executed by Astra locally
reviewer = X
claim_id = K15-C024 item 1 (ball volume), K15-C039
branch = kepler15/main
source_commit = the pushed head that carries this file
input_files = KeplerConjecture/Lean/Kepler15/Volume.lean
              KeplerConjecture/Lean/Kepler15/Normalisation.lean
command = lake env lean KeplerConjecture/Lean/Kepler15/Volume.lean
          then append `#print axioms Kepler15.volume_ball_unit` and re-run
dependencies = Lean v4.35.0, Mathlib v4.35.0 (local checkout)
resources = 1 CPU, 1 GB RAM, 300 s cap (cold Mathlib read dominates)
expected_outputs = KeplerConjecture/Lean/out/volume_build.log
success_criteria = exit 0; `#print axioms` shows only
                   [propext, Classical.choice, Quot.sound]; no `sorry`
certification = Lean kernel (pinned toolchain only)
note = the two proof routes are named in the file's header. If
       `EuclideanSpace.volume_ball` or `Real.Gamma_nat_add_one_over_two` has a
       different name in v4.35.0, report the diagnostic and do not patch with
       `sorry`; Main revises the file.
```


### C-TRANSFER-001 — transfer feasibility and minimal `Φ` for a given periodic packing

```text
request_id = C-TRANSFER-001
status = REQUESTED (specification only; no code yet)
owner = C (Computation, kepler15/comp-01a1d8c0)
reviewer = X, M for the mathematics
claim_id = K15-C044 (cut condition), K15-C054 (degree bound), K15-C035 (C1)
purpose = for a given PERIODIC packing and range R, compute the cell volumes,
          b(v) = sqrt32 - vol Omega(v), and the minimal Phi for which a transfer
          exists (equivalently min over cuts of sum_U b / |delta^+_R(U)|).
inputs  = a periodic packing as (lattice basis, fractional coordinates) with all
          separations >= 2; R in {2, 2.09}
method  = (i) periodic Voronoi volumes (replicate 3x3x3, take the cell of each
          representative; volume is translation invariant);
          (ii) LP: minimise t subject to sum_w phi(v,w) - sum_w phi(w,v) >= b(v),
          |phi| <= t, for the edges of G_R (minimum image);
          (iii) report t*, the binding cut, and the implied C1 = 3 t* k_R R (R+1)^2.
checks  = fcc and hcp must return t* = 0 (their cells are exactly sqrt32);
          a locally-sparse test must return 0 as well (all b <= 0);
          a configuration with some b > 0 is the informative case and none is
          known yet (K15-C051)
cap     = 1 CPU, 1 GB, 300 s for <= 400 centres
output  = JSON: packing id, R, t*, binding cut, C1, per-vertex b
note    = this is a TOOL, not a certificate: it decides feasibility for one
          packing, while the theorem quantifies over all packings. Its value is to
          test proposed transfers and to find the obstruction K15-C051 looks for.
```


### M-LEAN-003 — narrow-import build of `CubeDiff.lean` (supersedes `M-LEAN-002`)

```text
request_id = M-LEAN-003
status = REQUESTED
owner = M; executed by Astra locally
reviewer = X
claim_id = K15-C035 (arithmetic step), K15-C040
branch = kepler15/main
input_files = KeplerConjecture/Lean/Kepler15/CubeDiff.lean
command = lake env lean KeplerConjecture/Lean/Kepler15/CubeDiff.lean
          then append `#print axioms Kepler15.cube_diff_le` and re-run
dependencies = Lean v4.35.0, Mathlib v4.35.0
resources = 1 CPU, 1 GB, 300 s
note = imports are limited to Mathlib.Tactic.Ring, Linarith, Positivity. If the
       cap is still hit, report the peak RSS and stop: the statement is
       PROPOSED and no claim depends on compiling it today.
```

`M-LEAN-002` (broad `import Mathlib`) is closed as **FAILED on resources**: 60 s
cap (~715 MB) for the broad import, and the `VolumeOfBalls + Mathlib.Tactic`
variant hit the monitored 1 GiB cap after 32.6 s with no theorem checked.
`Volume.lean` therefore now carries the ball-volume statement as `Prop`-valued
definitions (`BallVolumeClaim`, `BallVolumeScalingClaim`) with **no** `sorry` and
**no** claimed proof.

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


### M-CERT-002 — make `L1'` rigorous: the runnable handoff (supersedes the 0738 form)

> **The 0738 form of this request is withdrawn.** Four defects, all named by review 0823: it named
> `l1_remainder.py` before the file existed; it pinned no source hash; its prose said `c = 0.13` while its
> command and acceptance said `0.17` and used the non-quotiented expression; and it demanded a "strictly
> positive minimum over a ball containing `θ = 0`", which is impossible. See `C148`. Everything below is
> generated from the code, and the pilot is now in the tree.

**File and source.**

```
path      KeplerConjecture/Computation/l1_remainder.py
sha256    bd2f24c28e469f3315d046bd1d445287cf6f26b8bc056d8ba3e97f440ab2f2ac
commit    1d2db443359ad57dddb6e8ac00212044dc7777af   (first commit containing the file)
deps      python3 (stdlib), numpy, scipy.spatial   -- no Lean, no network, no GPU
runtime   ~1 s measured; budget 1 CPU / 1 GiB / 120 s
```

**What is already proved by the pilot (no local work needed).** On the ball `d(θ,Rot) ≤ 0.156743`:

- **T1** every one of the 160 triples keeps `|det| > 0` (slack `0.336265` at `θ_max`);
- **T2** the 20 active triples stay active and the 140 inactive stay slack (slack `1.095124` at `θ_max`),

so the cell has exactly 12 facets and `vol` is smooth there. `--margins` exits 0.

**What only a local run can supply: a rigorous `M₃`.** The value bound is
`vol − V_dod ≥ (ratio)d² − (M₃/6)d³`, sufficient for `c = 0.13` at `θ_max = 0.0446545` iff

```
M₃  ≤  6(ratio_min − c)/θ_max  =  9.80        (measured M₃ = 0.075; ratio_min = 0.203..0.241)
```

**Pinned command.**

```
python3 KeplerConjecture/Computation/l1_remainder.py --certify --theta 0.0446545 --c 0.13 --m3-bound X
```

where `X` is *your* rigorous third-derivative bound. Acceptance is by **exit code**, not by a printed
minimum (there is no positive minimum over a ball through `θ = 0` — the pilot certifies the ratio on
`0 < d ≤ θ_max`, and says so):

| exit | meaning | acceptable? |
| --- | --- | --- |
| `0` | T1/T2 certified **and** `X ≤ 9.80`: the value bound follows | **this is the target** |
| `1` | T1/T2 certified, value bound not certified (no bound or `X` too large) | expected if `X` is crude |
| `2` | a sound part failed (a ball beyond `0.156743`, or T1/T2 broken) | a real problem |
| `3` | the negative control was not rejected, i.e. the pilot is inert | discard the run |

**Required negative control** (the pilot must be able to fail):

```
python3 .../l1_remainder.py --certify --c 0.30 --seed 3     # must exit 3
python3 .../l1_remainder.py --certify --theta 0.30          # must exit 2 (beyond the certified ball)
```

**If `X` comes out above `9.80` but below `100`.** Do not discard the run: the pilot's ladder shows
`δ₀ ∝ M₃⁻²`, so `X = 10` still gives `δ₀ ≈ 2.8·10⁻³` and `X = 100` gives `2.8·10⁻⁵`. Report `X` and the
ladder row; the constant degrades gracefully.

**Not in scope here.** `C147`'s global-to-local entry is a *separate* obligation (it reduces to the
`≥ 13`-facet branch, `C125`) and no run of this pilot addresses it. Do not report "`δ₀` proved" from an
exit-0 run; report "the local rate is proved, entry open".
