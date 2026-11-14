# Proof-to-certificate interface (normative)

Every number this project reports as a bound must arrive as an object in one of
the three conventions below, with the dictionary and the checker named. This file
is the contract between the proposer (C), the prover (M) and the reviewer (X).
Author: M. Reviewer: X. First cross-checked 2026-11-14.

## 0. The two mathematical objects, never conflated

For a radial `f` and a radial `f̂`:

* the **polynomials** `p, q` (rational coefficients, a finite list), and
* the **functions** `f(x) = p(τ(x))·G(x)`, `f̂(t) = q(τ'(t))·G'(t)`.

All sign conditions are conditions on the **functions**, decided through the
**polynomials**. Because the Gaussian factor is strictly positive everywhere, a
sign condition on the function is equivalent to the same sign condition on the
polynomial *in that variable* — but the two are different objects and a value of
`p` is never a value of `f`. (This distinction is where checkpoint `a08f378`'s
`audit_min_fhat` field went wrong: it printed `q`, and its huge magnitudes were
meaningless as values of `f̂`.)

## 1. The three conventions in use

| | radius / separation | variable | Gaussian | bound |
| --- | --- | --- | --- | --- |
| **C** (`Computation/exactcert.py`) | 1 / 2 | `t = 2π\`x\`²` | `e^{−t/2}` | `Δ ≤ (4π/3)·p(0)/q(0)` |
| **M** (`Computation/shell_check.py`) | 1 / 2 | `u = π\`x\`² = t/2` | `e^{−π\`x\`²}` | `Δ ≤ (4π/3)·P(0)/Q(0)` |
| **X** (`Counterexamples/ce_exact_gauss.py`) | 1 / 2 | `s = \`x\`²` | `e^{−s}` | `Δ ≤ (4/(3√π))·P(0)/Q(0)` |

All three use the **unnormalised** transform
`f̂(t) = ∫ f(x) e^{−2πi⟨x,t⟩} dx`, unit-radius balls, minimum separation 2, and
`Δ` = occupied-volume density. The Fourier map is the same operator in each; only
the variable and the Gaussian width differ.

## 2. The dictionaries (exact, coefficient-wise)

* **C ↔ M.** `u = t/2`, so `p(t) = P(t/2)`, i.e. `p_k = P_k / 2^k`, and the same
  for `q`. Thresholds: `u ≥ 12 ⟺ t ≥ 24`; `4π ⟺ 8π`. A rational `P` gives a
  rational `p` and conversely.
* **C ↔ X.** `f = P(s)e^{−s} = P(s)e^{−π s/π}` is the C-family at Gaussian width
  `1/π` in the `s`-variable; it is **not** the same function space as C's
  `p(t)e^{−t/2}` (different width). Their optima need not coincide numerically,
  and a certificate from one is *not* a certificate in the other. Both are sound;
  choose one per certificate.
* **Why X's choice is attractive:** both thresholds are rational (`s ≥ 4`,
  `w ≥ 0`), so no directed-π interval is needed for the *sign* conditions; the
  cost is a `π^{−1/2}` in the final constant. C's and M's choices keep the
  constant rational but force a conservative rational threshold, which loses a
  little (see §4).

## 3. The certificate schema (what a proposer must emit)

```
object      : "K15 CE certificate"
convention  : "C" | "M" | "X"
degree      : K
coefficients: [rational strings]        # in the stated basis
pi_enclosure: [PI_LO, PI_HI]            # rational strings, PI_LO < pi < PI_HI
signs       : { "A1": "...", "A2": "..." }   # the regions actually verified
claim       : "Delta <= <rational> (delta_upper)"
checker     : path + sha256 of the exact checker used, and its verdict
does_not_improve_on : e.g. "Cohn-Elkies 2003 (0.779747)"
```

Non-negotiable: the checker's verdict must be **unconditional** (no failure path
behind a verbosity flag — review 48443), the coefficients must be **rational**,
and the printed bound must be a rational interval, never a float.

## 4. The rational threshold, and why there is no loss

`π` is carried as a rational interval `[PI_LO, PI_HI]` with 29 digits (the same
pair Computation uses). Because `PI_LO < π`, the thresholds
`T_LO = 4·PI_LO` and `T_HI = PI_LO·ρ²` are **rational and ≤ the true ones**, so
proving a sign on them proves it on the true regions — with *no* rounding loss.
(The earlier revision used integer stand-ins such as `T_HI = 25`, which is
strictly stronger than needed and therefore lossy; that is superseded.)

Direction of the inequalities, once and for all: a *smaller* start point for a
`≤ 0` region makes the requirement **stronger**, and a smaller `T_HI` for the
"beyond ρ" region makes it stronger too — so using `PI_LO` everywhere is safe in
both places. The containment is recomputed and printed on every run, so a change
of `ρ` cannot silently invalidate a certificate.

## 5. The cross-check performed (evidence)

`Computation/interface_xcheck.py` takes a rational Main-basis vector, converts it
to C's basis, and verifies **identically** that `p(t) = P(t/2)` and
`q(t) = Q(t/2)`. For `a = (7/2, −3, 1/5, −1/7)`:

| quantity | Main (`shell_check.fourier_map`) | Computation (`exactcert.build_pq`) |
| --- | --- | --- |
| `c` | — | `(77/64, 55/32, −11/40, 3/28)` |
| `p(0)` | `7/2` | `7/2` |
| `q(0)` | `−17/8` | `−17/8` |
| verdict | FAIL (`q(0) < 0`) | REJECT (`A2`: root of the odd part on `[0,∞)`) |

The two implementations were written independently, in different variables, and
agree on the object and on the verdict. That is the reconciliation evidence; it
does **not** certify any bound, since this test vector is not admissible.

## 6. What a certificate does and does not establish

A passing certificate establishes one inequality: `Δ(Λ) ≤ X` for **every**
packing of unit balls in `R³`, conditional on (i) the checker being correct, and
(ii) the count or geometric input quoted with it (e.g. `n = 12` on the shell,
which is conditional on the Tammes-13 enclosure). It establishes nothing about
sharpness, nothing about equality cases, and nothing about optimality of the
family. A finite-grid search that produces no certificate establishes only that
*that search* failed (review 27616); it is never an impossibility proof.
