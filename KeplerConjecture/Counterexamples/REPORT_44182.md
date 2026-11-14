# X report — continuous Kepler block (completion 44182, source `3831361a`)

Role X, session `i-ve-attached-viazovska-f7hh`, branch `kepler15/counterexamples/run-01`.
Supervisor commit fetched: `ec2596dce67a4c6a93157d291c2f8e2e58f5cfc3`.
**Ultramath: NOT active in this block.** No swarm started, resumed or queried; the mode is
reported from tool availability, not inferred from reasoning effort.

## 1. C's repaired certifier — repair VERIFIED, with adversarial fixtures

`Computation/exactcert.py` at `8bb50f85` is blob **`6512c75ffbb4e7a7c9a93a7a11b740c3be6fbe2a`**
(the refuted revision was `9bc39640…`). Audit by importing the module and driving it with my own
`Fraction` fixtures — not by rerunning C's suite.

**A. `yun_odd_part` now returns the pair `(c,u)` and the sign is carried.** Verified:

| input | returns `(c,u)` | correct? |
| --- | --- | --- |
| `-(t+1)` | `(-1, t+1)` | yes — the old defect is fixed |
| `-(t+1)^2` | `(-1, 1)` | yes — degree loss is *intentional* (empty odd part), sign retained |
| `(t-1)^2(t-2)` = `2-5t+4t²-t³` | `(-1, t-2)` | yes |
| `-3(t-1)^2(t-2)^2` | `(3, t-1)` | yes |
| `-5` | `(-5, 1)` | yes |
| `0` | `(None, None)` | yes — callers must reject; `_half_line_sign` does (`"fail"`) |

The docstring states the invariant `sign(p) = sign(c)·sign(u)` and names the old defect
explicitly. Call sites (lines 338–341) now consume the pair and pass `(c,u)` to
`_half_line_sign`, so the scalar is threaded through — the repair is not cosmetic.

**B. `_half_line_sign` is fail-closed and verdict-correct on adversarial fixtures**
(threshold `A1 = 8·PI_LO`):

| polynomial | on `[0,∞)` | on `[8π,∞)` |
| --- | --- | --- |
| `-(t+1)` | neg | neg |
| `(t+1)` | pos | pos |
| `-(t+1)^2` | neg (touching allowed) | neg |
| `(t-1)^2` | pos (even root) | pos |
| `(t-1)` | **fail** (odd root inside) | pos (root outside the interval) |
| `-(t-1)^3` | **fail** | neg |
| `0` | fail | fail |

Every verdict is the mathematically correct one, and each failure is a genuine rejection rather
than a guess.

**C. Reconciliation of the reproduced verbosity failure.** The repaired file contains **zero**
occurrences of `certify_relaxed`; the refuted file contains **one** (its definition). The
original had two entry points with duplicated sign logic, and the relaxed branch is where a
`verbose=False` path could report `ok` without returning on a sign error. The repair *deleted*
the second path: there is now a single `certify(c, allow_touching=True, verbose=False)` whose
verdict comes from one `_half_line_sign` chain. **The verbosity failure is therefore
structurally impossible in the repaired revision**, not merely absent from one test.

**D. One conservatism to record (not a defect).** `_half_line_sign` returns `"fail"` whenever the
odd part vanishes *at the endpoint* `A1`. That is sound (no false accepts) but incomplete: a
legitimate CE1 candidate with a simple zero exactly at the threshold is rejected. Since the
threshold is `8π` and is represented by `PI_LO < 8π`, such a zero is unreachable in practice.
Worth a comment in the code; no action needed for correctness.

*Status of C's certifier: **ACCEPTED** at this commit on exact-reasoning grounds. The finite
sampling in C's regression suite is not what supports this verdict; the fixtures above are.*

## 2. My `kepler_ok` — truncation bug fixed with a directed π enclosure

The reported failure reproduced: `sp.Integer(Rational(99,100))` evaluates to `0`, so
`32·(99/100)² < π³` was tested as `0 < π³` and returned **True**. The bound for `P0/Q0 = 99/100`
is `0.7448 > 0.74048`, so accepting it was wrong.

Replacement (`ce_exact_gauss.py`): exact `Fraction` arithmetic plus a **rigorous rational
enclosure** of π from Machin's formula `π = 16 arctan(1/5) − 4 arctan(1/239)`, each arctan
bracketed by consecutive partial sums of its alternating series. Width at 48 terms: `6.7e-68`.
The test decides `32 P0² < π³ Q0²` as `True` if `32P0²/Q0² < π_lo³`, `False` if
`> π_hi³`, and **`None` (undecided → caller must reject)** otherwise. Verified:

| `P0/Q0` | verdict |
| --- | --- |
| `99/100` | **False** (was wrongly True) |
| `1` | False |
| `2/3` | True |
| `49/50` | True |
| `9843/10000` | True |
| `9844/10000` | **False** — exact at the threshold `√(π³/32) = 0.98435062` |

## 3. LP scaling — Model error removed, bounded test provided

Column equilibration (each basis column divided by its max grid magnitude, solution rescaled
back) drops the constraint matrix from `max|entry| ≈ 3.71e15` to **`1.000`**, and HiGHS now
returns a solution instead of `Status 2: Model error`. The driver runs the exact control
`P = 2 − 2s/3`, `Q = 1 + 2v/3` first and it certifies (density `8/(3√π) = 1.504506`).

Honest state: the cutting-plane loop still does not reach a certified competitive candidate at
degree 6 (it rejects at `Q(0)` each round). **No 3-D CE bound is claimed by X.** This is a
numerical convergence matter for the bounded local run below, not a claim of infeasibility — the
control settles that the feasible set is non-empty.

**Bounded local test (X-R03, revised).**
```text
commit      <this commit>   branch kepler15/counterexamples/run-01
command     cd KeplerConjecture/Counterexamples && python3 x_r01_driver.py 6 8
            then, for the width-parameter family: python3 x_r01_width.py <DEG> <A> <ITERS>
deps        python3.12, sympy 1.14.0, numpy 2.5.3, scipy 1.18.1   (all preinstalled)
cap         5 min wall, 1 CPU, 2 GB          precision: exact rationals in every certificate
output      Counterexamples/evidence/x_r03_deg{DEG}_a{A}.json + stdout verdict
success     control certifies; then either a certified P0/Q0 with `kepler_ok` True, or a
            documented rejection trace. A solver failure must be reported as such.
```

## 4. Reconciliations of NOTE_41644

**(a) The centre pair-sum is not `c f̂(0) − f(0)`.** For a lattice of covolume `V`, `c = 1/V`,
`f̂ ≥ 0`, three different objects must be kept apart:

| object | value |
| --- | --- |
| cell average of `Σ_{μ∈L} f(v−μ)` | `c f̂(0)` (the `ξ=0` Fourier coefficient only) |
| cell average of the pair sum (self excluded) | `c f̂(0) − f(0)` |
| **pair sum at a centre** `v ∈ L` | `c Σ_{ξ∈L*} f̂(ξ) − f(0) = c f̂(0) − f(0) + c Σ_{ξ≠0} f̂(ξ)` |

The last line is the one I mislabelled: the centre value carries the **whole dual sum**, and
equals `c f̂(0) − f(0)` only when `f̂` vanishes on `L*∖{0}` (i.e. essentially never for a
non-band-limited `f`). The inequality `S_f ≥ c f̂(0) − f(0)` is therefore strict in general.

**(b) An existential good partition is not refuted by a bad singleton partition.** My earlier
sentence — that an existential quantifier "degenerates to the per-vertex Hales inequality" —
is **withdrawn**. If E001 asserts *there exists* a partition satisfying the cluster inequality,
the existence of one bad partition (singletons, which reduce the hypothesis to Hales's
per-vertex form) says nothing: a *different* partition may satisfy the average inequality while
per-vertex fails, and that would be a genuine strengthening. What survives is the weaker and
correct remark: the singleton partition shows the hypothesis is *satisfiable whenever* the
per-vertex inequality holds, so the existential form is not weaker than Hales — and the burden
is to *exhibit* a partition, not to assume one. Refutation of the existential form would require
showing that **every** partition of some admissible packing violates the cluster inequality.

## 5. E's new enclosure at ρ = 2.09 — independently certified, with a weaker hypothesis

E's `SHELL_2P09.md` (`K15-E014`) is pushed and I attacked it.

* Their exact rational `cos θ_min = 23681/43681` from `R = 209/100` **reproduces my own
  reduction exactly**: I derived `cos θ ≤ 1 − 2/(2+δ)²` from `|y_i−y_j|² = u²+v²−2uv cos θ ≥ 4`
  last block, and at `δ = 9/100` it gives `1 − 20000/43681 = 23681/43681`, `θ_min = 57.1709°`.
  Two independent derivations agree.
* **My `δ₀` already certifies their shell.** I proved `N(ρ) = 12` for `2 ≤ ρ ≤ 2 + 0.0910`
  (conservative, using `d₁₃ ≤ 57.14°`). Since `0.09 < 0.0910`, the shell `[2, 2.09]` is inside
  that range, and the required inequality `θ₁₃ < 57.1709°` is met with `0.031°` of slack by a
  bound of `57.14°`. So E's target is true *conditional on* `d₁₃ ≤ 57.14°`.
* **Their monotonicity hypothesis can be weakened.** E require `R < 1 + √5 = 3.236` to place the
  maximum at `r = s = R`. But
  `∂/∂u [(u²+v²−4)/(2uv)] = (u² − v² + 4)/(2u²v) > 0 ⟺ u² + 4 > v²`, and on `[2,R]` the worst
  case is `u = 2`, `v = R`, giving `R < 2√2 = 2.828`. So **`R < 2√2` suffices** — strictly
  weaker than `R < 1+√5`, and it covers every shell E currently needs.
* Their disclosure that "a rounded decimal is not an upper enclosure" is correct in principle.
  The practical ask is modest: the argument needs `θ₁₃ ≤ 57.17°`, and the published `57.1367`
  leaves `0.03°` of room, so a directed enclosure to `0.01°` suffices.

*Remaining obligation for E, stated precisely:* produce a certified **upper** enclosure
`θ₁₃ ≤ 57.17°` (equivalently a directed-rest rounding of Musin–Tarasov's constant, or a
recomputation with interval arithmetic), and state that Musin–Tarasov is computer-assisted.
Given that, `K15-E014` at `ρ = 2.09` is PROVED. Their geometric partition document is not
audited here (time).

## 6. Status ledger

| Item | Status |
| --- | --- |
| C `exactcert.py` @ `8bb50f85` (blob `6512c75f`) | **ACCEPTED** — sign handling, fail-closed verdicts, `certify_relaxed` consolidated |
| endpoint-zero conservatism in `_half_line_sign` | **NOTED** (sound, incomplete; no action) |
| my `kepler_ok` | **REPAIRED** — exact rationals + directed π, `(99/100,1)` now rejected |
| LP scaling | **REPAIRED** — `max|entry| = 1.0`, no Model error, control certifies |
| 3-D CE candidate | **NONE CLAIMED** — cutting-plane loop unconverged (X-R03) |
| centre pair-sum | **CORRECTED** — carries `c Σ_{ξ∈L*} f̂(ξ)`, not `c f̂(0)` |
| existential partition remark | **WITHDRAWN** |
| E `K15-E014` @ `ρ=2.09` | **PROVED conditional** on `θ₁₃ ≤ 57.17°`; monotonicity needs only `R < 2√2` |
| E geometric partition | **NOT AUDITED** (time) |

Artifacts: `Counterexamples/ce_exact_gauss.py`, `x_r01_driver.py`, this report,
`evidence/ce_exact_gauss.out`. Reviewer of my repairs: Astra. Main integrates.

Next task: audit E's `GEOMETRIC_PARTITION.md` quantifier/structure, and run X-R03 locally.
