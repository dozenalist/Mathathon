# Computation interfaces for X (Counterexamples) and E (Experimental)

Owner: Computation session. Branch `kepler15/comp-01a1d8c0`, source commit
`69f3213aa6f2b636ec1b0e25a7394acfecae986b`.
Every number produced by this directory is **TESTED_FINITE** unless stated otherwise:
sign conditions are checked on finite grids. No output here is a certificate.

## 0. Files

| file | purpose |
| --- | --- |
| `k15conv.py` | the two normalisations, exact conversions, published-reference reconciliation with assertions |
| `fixtures.py` | five elementary fixtures (F1–F5); no solver involved |
| `ce3_baseline.py` | the CE control: radial Gaussian–Laguerre LP in `d = 3` |
| `ce3_constrained.py` | strengthened-candidate evaluator 1 (equality-case-constrained inverse problem) |
| `evaluator.py` | callable objective/evaluator for E; self-tests on stored coefficients |
| `out/` | JSON outputs with coefficients, parameters and diagnostics |
| `RESULTS_baseline.md` | the measured values and their status |
| `REQUESTS/` | local execution requests for Astra |

Reproduce everything in this block (VM, ~40 s total):

```
cd KeplerConjecture/Computation
python3 k15conv.py
python3 fixtures.py
python3 ce3_baseline.py --degree 31 --grid 1200 --out out/ce3_K31_g1200.json
python3 ce3_constrained.py --degree 25 --grid 900 --out out/constrained_K25.json
python3 evaluator.py
```

## 1. Normalisation contract (do not mix silently)

Native `A`: minimum separation 1, balls of radius 1/2, `rho_A` = centres per unit volume,
transform `fhat(t) = int f(x) e^{-2 pi i <x,t>} dx`, CE bound `rho_A <= f(0)/fhat(0)`.

Project `B`: unit radius, minimum separation 2, `Delta` = occupied-volume density,
CE bound `Delta <= (4 pi/3) f(0)/fhat(0)`.

Exact bridges: `rho_B = rho_A/8`, `Delta = (4 pi/3) rho_B = (pi/6) rho_A`, and a certificate
`f` in `A` becomes `g(x) = f(x/2)` in `B` with `ghat(t) = 8 fhat(2t)`.

`k15conv.py` asserts all four consistency checks:
Kepler `pi/sqrt(18)`; FCC `rho_A = sqrt2` and `rho_B = 2^(-5/2)`;
Li's CE lower bound `0.18398089` (unit-sphere centre density) `=` `rho_A > 1.47184712`;
Li-quoted best non-Hales bound `0.183889` `=` CDS22 general three-point `0.770271`.

**One rounding discrepancy is recorded, not hidden.** Cohn–Elkies' Table 3 entry `0.18616`
converts to `Delta = 0.779785`, while CDS22's Table 1.1 quotes `0.779747` for the same
quantity: a relative difference `4.9e-05`. CE03 print a rigorous upper bound rounded up at
five decimals; CDS22 quote a more precise value. Both are legitimate; do not treat them as
the same number to five decimals.

## 2. For E — the callable evaluator

Give me a candidate as either a pair of Python callables of the radius, or as coefficients
in the Gaussian–Laguerre basis.

```python
import sys; sys.path.insert(0, "KeplerConjecture/Computation")
from evaluator import bound_from_callable, bound_from_coefficients

# (a) arbitrary radial candidate
res = bound_from_callable(f=lambda r: ..., fhat=lambda s: ..., r0=1.0, R=6.0, S=6.0)
#     or let it integrate the transform for you (slower):
res = bound_from_callable(f=lambda r: ..., compute_fhat=True)

# (b) Gaussian-Laguerre coefficients, phi_k(r) = L_k^{1/2}(2 pi r^2) e^{-pi r^2}
res = bound_from_coefficients(c)
```

Returned dict (all keys always present):

```
rho_A_bound, Delta_bound, Kepler, gap_absolute, gap_relative, rho_B,
max_f_outside, argmax_f, min_fhat, argmin_fhat,
f_nonpositive_off_r0, fhat_nonnegative,
status="TESTED_FINITE", certified=False, remaining_obligations=[...]
```

Report `Delta_bound` and `gap_relative`; quote `certified=False` with every such number.
If your candidate only satisfies the sign conditions on part of the domain, say which part
and keep the status `TESTED_FINITE`.

For a candidate whose theory predicts *equality* (`Delta = pi/sqrt(18)`), also send the
contact-shell data: the values of `f` and `fhat` at the first few FCC and dual BCC shell
radii, from `ce3_constrained.fcc_shells()` / `dual_shells()`. Exact zero versus `1e-6`
matters for the diagnosis.

## 3. For X — the checker inputs

X should independently verify, in this order of importance:

1. **The conversion.** Re-derive `Delta = (pi/6) rho_A` from the two definitions and check
   `k15conv.py`'s four assertions by hand. Then check `fixtures.py` F4, which obtains
   `rho_A = 1.414213562373` and `rho_B = 0.176776695297` by *counting* lattice points in an
   aligned half-open box (exact, no boundary error), not by algebra.
2. **The transform convention.** `fixtures.py` F1 (Gaussian duality) and F2 (the 1D sinc
   control, `max |fhat(k)| = 2.9e-63` at integers) fix the convention independently of any
   optimisation.
3. **The Poisson identity on FCC.** `fixtures.py` F5 checks
   `sum_L F = det(L)^{-1} sum_{L*} Fhat` for a Gaussian and agrees to `2.0e-29`.
   This is the check that caught the 2026-11-14 dual-shell enumeration bug: a hand-built
   half-integer shell list was wrong and only brute-force enumeration over
   `Z^3 u (Z+1/2)^3` settled it. **Any replacement shell enumerator must pass F5.**
4. **The control values.** `out/ce3_K31_g1200.json` contains the coefficients, so X can
   recompute `f(0)`, `fhat(0)` and `Delta` without the solver, and can check that the
   published CE03 value `0.779747` is reproduced to `0.006%` by our non-rigorous optimum.
   Our value is *below* CE03's, which is the correct direction: CE03's is rigorous but not
   LP-optimal, ours is numerically optimal but not certified.
5. **The sign violations.** The stored optimum has `max f = +2.5e-11` on `[1, 12]` and
   `min fhat = -1.4e-08` on `[0, 12]`. These are genuine finite-grid violations and are the
   reason the status is `TESTED_FINITE`. X should confirm they are confined to near-tangency
   points (`argmin fhat = 1.304`, `argmax f = 1.640`) and are grid artefacts of a
   boundary-touching LP solution, not a coding error — by refining the grid and checking
   that they shrink.

## 4. What is deliberately *not* claimed

* No claim that `0.77970` is a rigorous bound. It is a numerical LP value on a grid.
* No claim that the Gaussian–Laguerre family is optimal for the CE LP; only that it is
  converged in degree to five digits (`k15conv.py`'s reference table gives the ordering).
* No claim of any improvement over Li's obstruction. The evaluator in §2 will honestly
  report a bound larger than `0.7707` (Li's floor) if a candidate is worse than three-point
  methods; that is a real result about the candidate.
