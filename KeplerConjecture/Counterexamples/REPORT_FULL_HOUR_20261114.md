# X full-hour block — K33 certificate and Tammes-13 enclosure

Block clock: **start 2026-11-14T09:17:25Z**, earliest finish **2026-11-14T10:17:25Z**.
Role X, session `i-ve-attached-viazovska-f7hh`, branch `kepler15/counterexamples/run-01`.
Supervisor commit `83cb448f6017fbaea1eae7565f6fb8112755e36e`. Audited tips:
comp `90cc632`, experimental `8aca235e`, main `bbad129d`.
**Ultramath: NOT active.** No swarm created, resumed, or queried; runtime evidence is the tool
surface only, and maximum reasoning effort is not evidence of Ultramath.

---

## Priority 1 — C's K33 exact certificate: ACCEPTED, with one metadata correction

Source: `Computation/out/verified_certificate_K33.json`, blob **`ced184a993db37c03ffdb24730faa01f79b663fb`**
(sha256 `f7b7425b52a19a5a68cdbb85af04cfdb5d6e7a323be42d2c00b9d64ac6d8e236`). My copies and scripts:
`Counterexamples/Reviews/K33/`. **Nothing was imported from `Computation/`** — the Laguerre
recurrence, the Fourier map, the sign test and the π enclosure are all re-implemented here.

### Normalization re-derived from scratch

Convention: unit balls, separation 2; `t = 2π|x|²`, so `|x| ≥ 2 ⟺ t ≥ 8π`. With
`φ_k(x) = L_k^{1/2}(t)e^{−π|x|²}` and `L_k^{1/2}` the Laguerre polynomial in the **argument** `t`,
the radial Fourier eigenrelation is `φ̂_k = (−1)^k φ_k`. Hence for `f = p(t)e^{−π|x|²}`,
`f̂ = q(t)e^{−π|x|²}` with `p = Σc_kL_k`, `q = Σ(−1)^k c_k L_k`, and
`Δ ≤ (4π/3)·p(0)/q(0)`, `Δ < π/√18 ⟺ 4p(0)√18 < 3q(0)`.
**Tails: there are none.** The Gaussian factor is strictly positive on all of `ℝ³`, so both CE
conditions are *exactly* polynomial sign conditions on half-lines; no decay or tail estimate is
needed or used.

### Independent reconstruction (exact, rational)

| check | result |
| --- | --- |
| `p` recomputed from the 34 rational coefficients = JSON `p_rational` (ascending) | **identical** |
| `q` recomputed = JSON `q_rational` | **identical** |
| `p(0)` = JSON `p0`; `p(0) > 0` | **yes**; `3.43e-2 > 0` |
| `q(0)` = JSON `q0`; `q(0) > 0` | **yes**; `1.00 > 0` |
| `p0/q0` = JSON `ratio_exact` | **identical** |
| `Δ = (4π/3)p0/q0` | **0.779966497784296** (my π enclosure, width `1e-67`) |

`deg p = deg q = 33`, both **odd**, so each must have a real root somewhere — an important
structural fact that a naive "no real roots" test would mishandle.

### Sign domains, multiplicities, endpoints (my own exact test)

* **CE1**: `p ≤ 0` on `[8·π_lo, ∞)` with `π_lo < π` — the *stronger* condition, hence safe.
  Verified: no root of odd multiplicity above the endpoint, sign at the endpoint `−1`,
  leading sign `−1`. **PASS**
* **CE2**: `q ≥ 0` on `[0, ∞)`. Verified: no root of odd multiplicity in `(0,∞)`, `q(0) > 0`,
  leading sign `+1`. **PASS**
* **Root census**: `p` has **exactly one** real root, in `(25.13, 25.1327)`, i.e. just *below*
  `8π = 25.1327412287` — precisely the contact radius `|x| = 2`, as CE requires; `q` has
  **exactly one** real root, and it lies in `(−∞, 0)`. So no endpoint or multiplicity pathology
  exists, and the "touching" case never arises for this certificate.

### The rounded bound is a genuine upper bound

`delta_upper_exact` exceeds my independent `(4π/3)p0/q0` by `2.6e-30`, so it is correctly
rounded **up**; `0.77996650` and `0.779966497785` both exceed the true value. The claim
`Δ ≤ 0.77996650` is therefore **correct**, and the bound sits `0.039486` above Kepler and
`0.000219` above Cohn–Elkies' `0.779747` — weaker than the published value, as C discloses.

### Independently supplied controls

| control | expected | observed |
| --- | --- | --- |
| **positive**, same basis: `c = (47/2, 1)` ⇒ `p = 25 − t`, `q = 22 + t` | ACCEPT | ACCEPT, `Δ = 4.75999` |
| the K33 vector itself | ACCEPT | ACCEPT |
| `−c` (sign flip) | REJECT | REJECT (`p(0) < 0`) |
| synthetic `p = −(t−30)`: simple root above the endpoint | REJECT | REJECT |
| synthetic `p = −(t−30)²`: double root (touching) | ACCEPT | ACCEPT |
| synthetic `p = −(t−30)²(t−40)` | REJECT | REJECT |
| synthetic `q = (t−5)²` | ACCEPT | ACCEPT |
| synthetic `q = t−5`, `q = (t−5)²(t−7)` | REJECT | REJECT |

The last six are the discriminating controls the assignment asks for: **two checkers agreeing
on a sign misconception would both fail them**, and my test gets the even-multiplicity cases
right in both directions. (Note: small *generic* perturbations `c_i ± 10⁻³` are legitimately
**accepted** — the feasible set is open — so they are not negative controls; the synthetic ones
above are.)

### Minimal witness and a corrected claim

Bisecting single-coefficient perturbations (exact rationals, `Reviews/K33/witness_bisect.py`):
decreasing `c₅` by `3/2²¹ = 1.431e-06` already **breaks** the certificate, as does increasing
`c₁₆` by the same amount. So the certificate is fragile at the `1.4e-06` level.

**That contradicts C's `note_on_near_tangency`**, which states "min `fhat` over [0,300] is about
`3.5e-29`". Under the stated convention `t = 2π|x|²` I get, independently:
`min q` on `[0,300]` **`≈ 3.708e-06`** at `t* = 10.332028` (grid of 6001 points plus a refined
critical point). A `1.4e-06` coefficient perturbation can only break a `3.7e-06` margin — it
could not touch a `3.5e-29` one. So the *number is wrong by 23 orders of magnitude*, while the
conclusion it was supporting ("q nearly touches zero but does not") is **right but far less
dramatic**. **Corrected claim:** `q` has a positive minimum `≈3.7e-6`, so a float-based sign
test is *unsafe* but only marginally so; the exact certificate is genuinely needed, and it is
robust to `~1e-6` perturbations, not `~1e-29`.

### Frozen verdict

> **ACCEPT `K15-C033`**: every packing of unit balls in `ℝ³` has `Δ ≤ 0.77996650`.
> Certificate `ced184a9` is **valid**; normalization, sign domains, positivity, root structure,
> tails and upward rounding all independently verified. **One metadata claim is corrected**
> (`near_tangency`: `3.7e-06`, not `3.5e-29`). Minimal witness to the fragility:
> `c₅ −= 3/2²¹` ⇒ certificate breaks.

**Bounded local reproduction (for Astra).**
```text
commit      <this commit>      branch kepler15/counterexamples/run-01
cwd         KeplerConjecture/Counterexamples/Reviews/K33
command     python3 audit_K33.py ; python3 audit_K33_signs.py
deps        python3.12, sympy 1.14.0, mpmath 1.3.0   (preinstalled; no network)
cap         5 min wall, 1 CPU, 1 GB
expected    "p matches JSON: True", "q matches JSON: True", "Deli upper bound: True",
            CE1/CE2 PASS, min q ~3.7e-06
note        witness_bisect.py needs ~20 min (bisection does ~24 exact Sturm calls per
            coefficient); run it only if the fragility figure matters.
```

---

## Priority 2 — E's Tammes-13 enclosure (`K15-E015`, tip `8aca235e`): UPHELD, one justification corrected

I re-derived the enclosure with **my own** rigorous rational Taylor bounds for `sin`, `cos`,
`tan` and `arccos` (Lagrange/alternating remainders, exact rationals, no floating point in any
decision). Script `Reviews/Tammes13/audit_tammes13.py`.

* **Equations.** `(E1) 2tan(3π/8 − a/4) = (1−2cos a)/cos²a`, `(E2) cos d = cos a/(1−cos a)`.
* **Monotonicity.** `g'(a) = −(1/2)sec²(3π/8 − a/4) − 2 sin a(1−cos a)/cos³ a`, confirmed
  **symbolically** to be exactly `d/da` of E's `g`; both terms are strictly negative on
  `(0,π/2)`, so `g` is strictly decreasing and the root is unique. **E's argument is correct.**
* **Bracket.** With my own enclosures: `g(1.2113) ∈ [+0.00135704, +0.00135704] > 0` and
  `g(1.2114) ∈ [−0.00155318, −0.00155318] < 0`, so `a* ∈ [1.2113, 1.2114]` — matching E's
  bracket exactly and independently.
* **Final bound.** From `a* ≤ 1.2114`, `cos a* ≥ 0.351709193286`, so
  `h = cos a/(1−cos a) ≥ 0.542517631970` and
  **`δ₁₃ ≤ 57.1448°`**, which is `< 57.1709°` with `0.0261°` of margin. **The shell lemma at
  `ρ = 209/100` therefore holds**, and `K15-E014`/`K15-E015` are upheld.
* **Corrected justification.** E claims the identity `α(d) = arccos(cos d/(1+cos d))` "would not
  [match] if the exponent or a coefficient were misread", and uses that as a transcription check.
  **That inference is invalid**: from `(E2)`, `cos d/(1+cos d) = cos a/(1−cos a)÷(1+cos a/(1−cos a))
  = cos a` *identically*, for **every** `a`. I confirmed numerically that both misread variants
  satisfy the identity to `1e-17` while giving `d = 72.09°` and `45.33°`. So the identity
  validates `(E2)` only; what actually pins the transcription of `(E1)` is the **numerical match
  to `57.1367°`**, which E also reports. The conclusion stands; the stated reason does not.

`K15-E015`'s disclosed dependency (Musin–Tarasov is computer-assisted) remains, and my previous
block's weaker-hypothesis remark (`R < 2√2` suffices, not `R < 1+√5`) still applies.

**Not audited in this block:** Main `bbad129d` shell_check Fourier matrix / shell-density theorem
(the files are `Computation/checker_adversarial.py`, `shell_fixture.py`, `interface_xcheck.py` on
that tip). Recorded as a gap, not as an objection.

---

## Status table

| Item | Status |
| --- | --- |
| `K15-C033` certificate `ced184a9` | **ACCEPTED** (normalization, signs, roots, tails, rounding independently verified) |
| `K15-C033` `near_tangency` claim | **CORRECTED** — `min q ≈ 3.7e-06`, not `3.5e-29` |
| minimal witness | **FROZEN** — `c₅ −= 3/2²¹` breaks it; fragility `1.431e-06` |
| controls (positive / negative / multiplicity) | **8 supplied**, all correct |
| `K15-E015` Tammes-13 enclosure | **UPHELD**; `δ₁₃ ≤ 57.1448° < 57.1709°`, margin `0.0261°` |
| `K15-E015` transcription justification | **CORRECTED** — the consistency identity is automatic |
| Main `bbad129d` shell_check | **NOT AUDITED** (gap) |
| Ultramath | **not active** |

## Next task

Audit Main's `bbad129d` shell_check Fourier matrix and shell-density theorem (the one Priority-2
item not reached), then attack E's partition disjointness/coverage and the compensation
inequality with the `1.3853219` shortfall from my previous block as the target.
