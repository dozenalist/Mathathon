# Exact certificate checker and candidate generator

> ## WITHDRAWN — review 48443
>
> **The certified bounds previously claimed in this file are REFUTED and withdrawn.**
> Review 48443 reconstructed the `K = 21` certificate independently with exact SymPy
> Laguerre polynomials, matched the stored `p` and `q`, and found **ten simple positive
> roots of `q`**, with `q(57955199/21687900) ≈ -3.8762318927e-05 < 0`. The witness is
> reproduced exactly by `exactcert_tests.py` T5.
>
> Root cause, now fixed: in `certify_relaxed` the line
> `if verbose: print(...); return rec` puts **both** statements inside the `if`, so a
> failing candidate returned normally when `verbose=False` and fell through to the success
> path. Additionally `yun_odd_part` returned a monic odd part and **discarded the leading
> sign**, so `-t-1` and `t+1` were treated alike.
>
> Consequences recorded here rather than removed:
> * every JSON in `out/certificate_K*.json` is a **failed candidate**, retained as evidence;
> * re-running them through the repaired checker **rejects all seven** (A1 or A2);
> * no bound in this directory is currently proved. `K15-C-EXACTCERT-001` is `REFUTED`.
>
> The design discussion below (§2 coefficient field, Fourier map, endpoints; §3 multiplicity)
> is retained because it is still the right design; the *numbers* were not valid.

Owner: Computation. Branch `kepler15/comp-01a1d8c0`. Files: `exactcert.py` (checker),
`gen_candidate.py` (generator). Both are runnable; execution is offloaded to Astra
(`REQUESTS/K15-C-REQ-002.md`).

## 1. What is certified

For every packing of unit spheres in `R^3` (centre separation at least 2), the
occupied-volume upper density satisfies

\[
\Delta \le 0.78010544 \qquad\text{(WITHDRAWN — not proved)}
\]

This is **+5.351% above the Kepler value** `pi/sqrt(18) = 0.74048049`, so it is a loose
bound, not a competitive one. It is, however, obtained without any discretisation
assumption: the two sign conditions are decided in exact rational arithmetic.

**Status: `REFUTED` (review 48443).** No valid certificate in this family has yet been
exhibited. The repaired checker rejects every stored candidate.

## 2. Coefficient field, scale, Fourier map, endpoints

| item | specification |
| --- | --- |
| variable | `t = 2*pi*|x|^2 >= 0` |
| basis | `phi_k(x) = L_k^(1/2)(t) exp(-t/2)`, `k <= K`, `K` **odd** |
| coefficient domain | `c in Q^(K+1)`, stored exactly as fractions |
| polynomials | `p(t) = sum c_k L_k^(1/2)(t)`, `q(t) = sum (-1)^k c_k L_k^(1/2)(t)`, both in `Q[t]` |
| functions | `f = p * exp(-t/2)`, `fhat = q * exp(-t/2)` — always distinguished from `p,q` |
| Fourier map | diagonal in this basis with eigenvalue `(-1)^k`, hence exact and rational |
| (A1) | `p(t) < 0` for `t >= 8*pi`  (i.e. `|x| >= 2`) |
| (A2) | `q(t) > 0` for `t >= 0` |
| bound | `Delta <= (4*pi/3) * p(0)/q(0)`, with `p(0), q(0) in Q` |

**Why `K` must be odd.** The leading coefficient of `L_k^(1/2)` is `(-1)^k/k!`, so
`lc(p) = (-1)^K c_K/K!` and `lc(q) = c_K/K!`. Signs at both ends need `(-1)^K c_K < 0`
and `c_K > 0`, which are consistent **only for odd `K`**. An even-degree strict-sign
certificate in this basis does not exist; the generator raises rather than silently
returning a bad number.

**The irrational endpoint `8*pi`.** `pi` is enclosed by rationals
`PI_LO < pi < PI_HI` (decimal truncations of rigorously known digits). Since
`8*PI_LO < 8*pi`, verifying `p < 0` on `[8*PI_LO, inf)` gives `p < 0` on `[8*pi, inf)`
a fortiori. The direction is safe: the check is slightly *stronger* than required, so it
can only ever certify a smaller bound, never an invalid one. No symbolic `pi` and no
interval coefficients are needed.

## 3. The exact-order design

`sign(p)` is constant between consecutive real roots, so a sign on a half-line is decided
by (i) the number of real roots there and (ii) the sign at one point. Root counting is
Sturm's theorem over `Q`, which counts **distinct** real roots and so is blind to
multiplicity. That matters, because at an optimum `p` and `q` *touch* zero: the equality
case forces double zeros, and a strict "no roots" test rejects exactly the good
candidates.

The design therefore uses **Yun's squarefree decomposition**: write
`p = prod_i f_i^i`; then `sign(p) = prod_{i odd} sign(f_i)` away from roots, so
`u := prod_{i odd} f_i` is squarefree and carries the sign of `p`. Certifying
`u > 0` on the half-line (no root + one positive value) certifies `p >= 0`, allowing
even-multiplicity touching and still rejecting any odd-multiplicity crossing.

Effect, measured at `K = 9`: strict-sign certification gives `Delta <= 2.50596`; the
squarefree route gives `0.82276`. The strict test is not merely conservative, it is
useless in practice.

## 4. Results — WITHDRAWN (see banner)

The table below records what the **buggy** checker reported. None of it is valid; all seven
candidates are rejected by the repaired checker. It is retained only to document the
failure:

`gen_candidate.py`, grid of 300–320 points on each region, `Tmax = 70–80`, coefficients
rounded to denominator `10^6`, then verified exactly.

| `K` | certified `Delta <=` | gap to Kepler | float LP value | rounding loss |
| --- | --- | --- | --- | --- |
| 9 | 0.82276051 | +11.112% | 0.82287862* | — |
| 11 | 0.79724095 | +7.665% | | |
| 13 | 0.78487203 | +5.995% | | |
| 15 | 0.78250880 | +5.676% | | |
| 17 | 0.78229459 | +5.647% | | |
| 19 | 0.78095347 | +5.466% | | |
| **21** | **0.78010544** | **+5.351%** | | |

\* the K=9 entry at grid 400; the tabulated 0.82276051 uses grid 300. Certified values are
monotone decreasing in `K` and approach the CE LP optimum `0.779747` from above, as they
must: certifying a looser constraint set can only give a looser bound.

The certified value differs from the float LP objective by `~1.3e-5`
(e.g. `0.82289543` vs `0.82287862` at K=9, grid 400), so the rational rounding is
negligible. **The reported number is always the one produced by the exact checker applied
to the rounded coefficients, never the float objective.**

## 5. What this is not

* Not an SOS certificate. No float residual is called exact; the sign test contains no
  floating point at all.
* Not a claim of optimality, of sharpness, or of any improvement over `0.779747`.
* Not a certificate that the family is rich: it says nothing about degrees above 21.
* The `Tmax` grid used to *find* candidates is heuristic. It plays no role in
  verification — a candidate that fails the exact test is discarded, whatever the grid.
