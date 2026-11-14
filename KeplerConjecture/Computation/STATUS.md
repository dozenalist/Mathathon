# Computation — status index

Branch `kepler15/comp-01a1d8c0`. One page for Main: what is proved, what is numerical, what is
open. Full detail in `PROGRESS.md`, `CERTIFIER.md`, `SHELL_PROPOSE_RESULTS.md`, `TLO_FINDING.md`.

## Exactly verified (exact rational arithmetic; no floating point in any decision)

| claim | statement | scope |
| --- | --- | --- |
| **K15-C-VERIFIEDCERT-001** | `Δ ≤ 0.77996622` | every unit-sphere packing in `R³`; degree-33 rational certificate; accepted by two checkers sharing no code |
| **K15-C-TLOCOST-001 / XVAL-001** | the same certificate is **accepted by Main's `shell_check.py`** once `T_LO = 4·π_lo` is used | cross-session verification |
| **K15-C-SHELLPROP-002 / SHELLLADDER-001** | `Δ ≤ 0.78037031` at degree 33, `Umax = 120`, `T_LO = 4π_lo`, `n = 27`, `ρ = 2.05` | unconditional count; **0.080% above CE's 0.779747** |
| **K15-C-SHELLGAIN-002 / -003** | `TESTED_FAMILY`: the *uniform* `n`-neighbour allowance was not used by the LP in the cases tested (16 exact comparisons, two bases). **Not** a statement about local/configurational strengthenings | finite search |
| **K15-C-FOURIER-AUDIT-001** | Main's `fourier_map` verified: exact matrix agreement, `M² = I`, and quadrature to `1e-13` | A1/A2 exact, A3 float |
| **K15-C-XVAL-002** | the two exact checkers accept **each other's** certificates, in both directions, agreeing to ten digits | `CROSSVALIDATION.md` |
| **K15-C-FAMTESTED-001** | `TESTED_FAMILY`: best value found in the tested family is `0.78037032` at `(K, Umax) = (33, 120)`; **not an optimum** — the ladder is non-monotone, so the search is not exhaustive | finite search over a parameter grid |
| **K15-C-POSCERT-001** | `c = (4,1)` ⟹ `Δ ≤ 44π/15 = 9.215339` | elementary, hand-checkable, positive control |

## Actionable for Main

1. **`shell_check.py` at `6626714` is UNSOUND** — it falsely accepts `le_on_interval([0,1,-1],0,0,1)`,
   `nonneg_on_half_line([0,-1,1])`, `_ray([0,1,-1],0)`, all contradicted at `u = 1/2`
   (`REVIEW_0138.md` §1). Do not rely on it until the fix is audited.
2. **Change `shell_check.py`'s `T_LO` default from `12` to `4·π_lo`.** It costs ~6.7% of the
   bound and buys nothing: `12 < 4π` constrains `p` *inside* the ball. See `TLO_FINDING.md`.
3. `T_HI = 27/2` is valid at `ρ = 2.09` but **not** at `ρ = 2.05` (`πρ² = 13.20 < 13.5`); use
   the parameterised predicates with `T_HI(ρ) = ⌊π_lo ρ²⌋`.
4. Do not optimise in the monomial basis; propose in Laguerre and convert exactly
   (`shell_propose.py`). The monomial basis returns box vertices (reproduces `K15-C022`).
5. **Raise the constraint horizon with the degree.** A degree-29 polynomial constrained on
   `[13.2, 40]` rises to `5.4×10^46` outside it; the exact checker rejects that, correctly.
   `Umax ≈ 120` works, `250` breaks on conditioning.

## How to reproduce in one minute

```bash
cd KeplerConjecture/Computation
python3 verify_certificate.py out/verified_certificate_K33b.json   # 0.77996622, both checkers
python3 exactcert_tests.py && python3 exactcert_oracle.py          # regression + exact oracle
python3 audit_fourier.py /tmp/shell_check.py                       # Fourier audit
python3 shell_propose.py --checker /tmp/shell_check.py --degree 33 --tlo-exact --Umax 120
```

with Main's checker extracted first:
`git show omm/kepler15/main:KeplerConjecture/Computation/shell_check.py > /tmp/shell_check.py`

## Numerical only (`TESTED_FINITE`) — not certificates

`shell_bench.py` (grid LP), `ce3_baseline.py`, `ce3_constrained.py`, `search_*.py`.
The withdrawn ladder of review 48443 is retained in git history and in `out/certificate_K*.json`
as failed evidence; every one of those candidates is **rejected** by the repaired checker.

## Open

* A **local/configurational** shell statement (`NONUNIFORM_SHELL.md` §3) — the only variant that
  could still pay, and it is not a count.
* Three-point / SDP route: needs a solver, hence a local run.
* Nothing here improves on Cohn–Elkies; the exact bounds above are cross-validated artifacts.
