# K15-REVIEW-0138 — X independent review (block 2)

Receipt `2026-11-14T10:04:35Z`; earliest finish `11:04:35Z`. Runtime: Ultramath (supervisor
verified). Branch `kepler15/counterexamples/run-01`. Audited tips: main `9461aae`, setup
`3c8ea4b`, experimental `ec66012`, comp `447da32`; target commits `96419eaa`, `4ea4e8b9`,
`6626714`.

## 1. Main's repaired `shell_check` — ACCEPTED on an independent 23-test battery

`Computation/shell_check.py` at `9461aae` is blob **`5619c1defd998d175d4ae2bea3ecb64b69c08f9a`**
(the defective revision at `6626714` was `a8526a8c322fc350c27557656d655e28a371a62b`). The repair
**is** pushed, and it rejects all three reported witnesses:
`le_on_interval([0,1,−1],0,0,1)`, `nonneg_on_half_line([0,−1,1])`, `_ray([0,1,−1],0)` all return
`False`, correct since `u−u² = +1/4` and `u²−u = −1/4` at `u = 1/2`.

**Mechanism, verified against the symptom.** Their `_count_roots_open` docstring says the old code
subtracted a root at `lo` instead of at `hi` when converting Sturm's `(a,b]` count to `(a,b)`.
That is exactly the reported failure: `u²−u = u(u−1)` has its root at `lo = 0`, so the erroneous
subtraction removed the *only* interior root and left the count at 0. The repaired version
additionally decides the sign with `P.intervals(eps=1e-8)` isolating intervals plus one rational
point in each gap between consecutive intervals — complete, because the sign is constant on each
gap and the interval endpoints are exact rationals.

**My battery** (`Reviews/x_adversarial_shellcheck.py`, reproduction below) — 23 tests, **0
mismatches**:

| family | cases | result |
| --- | --- | --- |
| the three reported witnesses | `u−u²`, `u²−u` on `[0,1]` / `[0,∞)` | correct (reject) |
| same shapes, true statements (over-rejection check) | `u²−u ≤ 0` on `[0,1]`; `−(u−1)² ≤ 0`; `−(u−5)² ≤ 0` on `[5,∞)` | correct (accept) |
| touching from **above** (must reject) | `(u−1)² ≤ 0` on `[0,2]`; `(u−5)² ≤ 0` on `[5,∞)` | correct (reject) |
| **irrational roots** | `u²−2` on `[0,1]` (accept) / `[0,2]` (reject) / `[3/2,2]` (reject); `2−u²` on `[0,∞)`; `u²−2` on `[2,∞)`; `(u²−2)²` (accept) | all correct |
| repeated roots | `(u−1)³`, `−(u−1)³` on `[0,2]` | correct |
| zero polynomial / constants | `0 ≤ 0` (accept), `−1 ≥ 0` (reject), `0 ≤ 0` on a ray | correct |

**A methodological point that cost me four wrong expectations.** While writing the battery I
mis-predicted four cases, all by confusing *"has a double root"* with *"satisfies ≤ 0"*: `(u−1)²`
touches zero from **above**, so it is `1` at `u = 0` and is **not** `≤ 0` on `[0,2]`; likewise
`−(u−1)³ = +1` at `u = 0`; and `u²−2 > 0` on `[3/2,2]` because `√2 < 3/2`. Every one of those was
my error and Main's code was right. The battery therefore now **verifies every "False"
expectation against an explicit witness value** before trusting it (see the automatic witness
block in the script). This is the same class of mistake that produced my earlier unsound
predicate and Main's earlier endpoint defect: the failure mode is human, and the mitigation is
witness-anchored expectations rather than intuition.

**Scope statement, which the review rightly insisted on.** Accepting `5619c1d` certifies *the
predicate implementations* on the families above. It does **not** make the K33 bound rest on
checker agreement: `K33`/`K33b` are valid because Computation's strict and independent SymPy
checks passed locally **and** because their sign structure is decidable by hand
(`p` has one real root below `8π`, `q` has one real root, negative). **Particular valid K33
coefficients are one thing; generic checker soundness is another, and I keep them separate.**

Reproduction: `cd KeplerConjecture/Counterexamples/Reviews && python3 x_adversarial_shellcheck.py
shell_check_9461aae.py` (exit 0 iff 0 mismatches).

---

## 2. Main's transfer package (`96419eaa`): `C035`, `C044`, `NEXT_PACKAGE`

### 2.1 `K15-C035` (transfer ⟹ negligibility): conclusion ACCEPTED, **constant missing a factor `R`**

The mechanism is sound and elegant: an antisymmetric `φ` with `φ(v,w)=0` for `|v−w|>R` and
`|φ|≤Φ` gives `A(v) = Σ_w φ(v,w)` whose sum over a ball cancels pairwise in the interior, leaving
only pairs straddling the boundary. Step (a) `k_R ≤ (R+1)³−1` is correct (the balls `B(w,1)` for
`|w−v| ≤ R` are disjoint and lie inside `B(v,R+1)`, and miss `B(v,1)`).

**The arithmetic step in (b) is invalid for `R ≥ 2`.** They write
```
3Φ k_R · R r²(R+1)²  ≤  3Φ (R+1)³ · r²(R+1)²
```
which requires `k_R·R ≤ (R+1)³`. But `k_R ≤ (R+1)³−1`, so `k_R·R ≤ R((R+1)³−1)`, and for `R = 2`
that is `52 > 27 = (R+1)³`. **A factor `R` is dropped.** The argument as written gives
$$\sum_{v\in\Lambda\cap B(x,r)} A(v) \;\le\; 3\Phi\,R\,(R+1)^5 r^2 ,$$
so the correct explicit constant is `C₁ = 3ΦR(R+1)⁵`, not `3Φ(R+1)⁵`. `C035` is still true and
still negligible (an `R`-dependent constant is harmless: `R` and `Φ` are fixed parameters), so
**nothing downstream breaks**; but the stated constant is not established, and a Lean lemma
`cube_diff_le` that encodes the displayed chain would be encoding a false step. Fix: replace
`3Φ(R+1)⁵` by `3ΦR(R+1)⁵` (or absorb `R` into `Φ` by redefining `Φ' = ΦR`).
*Also:* the prose says the balls lie in `B(v,R+2)∖B(v,1)`, which would give `(R+2)³−1`; the
*stated* `(R+1)³−1` is the correct one, so the prose and the formula are inconsistent (the formula
is right).

### 2.2 `K15-C044` (cut criterion): lemma ACCEPTED, **isoperimetric consequence over-stated**

The criterion is the Hoffman/Gale circulation condition for the transfer polytope; the reduction
via supersource/supersink is standard and the correction history (replacing "`Σ_U b ≤ 0` for every
union of components" by the cut condition) is right — the component formulation is indeed vacuous
on a connected `G_R`.

Two gaps:

1. **Finite-to-infinite extension is not supplied.** For infinite `Λ` the criterion quantifies over
   finite `U`, but each cut `δ⁺_R(U)` is computed in the *whole* graph, so one cannot simply apply
   finite max-flow to finite induced subgraphs (whose cut sets are smaller). The standard repair is
   a compactness argument on `∏_{e}[−Φ,Φ]` (Tychonoff) applied to the *finite constraint systems
   restricted to all edges incident to a finite vertex set* — each is feasible by the cut
   condition, so the whole system is. That step should be written out; it is not automatic.
2. **`|δ⁺(U)| = O(|U|^{2/3})` is asserted for every finite `U` and is false in that generality.**
   It is a *ball-like* estimate. For a long thin set — e.g. `U` a chain of `n` centres along a
   line, each with `O(1)` neighbours outside — `|δ⁺| = Θ(n)`, not `O(n^{2/3})`. The repair is to
   restrict the consequence to `U = Λ ∩ B(x,r)`, for which it does hold: saturation gives
   `Ω(v) ⊆ B(v,2)`, hence `U ⊆ B(x,r+2)` and `|δ⁺_R(U)| ≤ k_R·((r+2)³−r³) = O(r²) = O(|U|^{2/3})`
   with `|U| ≍ r³`. Then `Σ_U b ≤ Φ|δ⁺| = O(Φr²)` is exactly the averaged inequality wanted.
   **Statement as published is stronger than what is proved.**

### 2.3 `NEXT_PACKAGE`: the `V = 5.40` step is **already implied** by the dodecahedral theorem

The package proposes "`Σ_{v∈K} vol Ω(v) ≥ 13V` for some `V > 5.372754` — even `V = 5.40` would be a
new cluster inequality". **It would not.** Hales–McLaughlin give
`vol Ω(v) ≥ V_dod = 5.550291` for *every* cell of a saturated packing, hence for every cluster
`Σ_{v∈K} vol Ω(v) ≥ 13·V_dod = 72.153783 > 13·5.40 = 70.2`. So a cluster inequality at `V = 5.40`
is a **strictly weaker consequence of a published theorem**, not a new step; the ladder in the
same file (`5.372754 → 5.550291 → 5.656854`) already says the only interesting target is
`V > 5.550291`. **Novelty claim withdrawn; the genuinely open target is beating the dodecahedral
constant *on average over a cluster*.** (Proof-complexity is a separate axis: if a *simpler* proof
of `V = 5.40` existed it would have value as a stepping stone, but it would not be a new
inequality and the file does not claim that.)

The constants in their table are arithmetically right: `(4π/3)/5.372754 = 0.779636` (Rogers
`0.7796356`), `(4π/3)/5.550291 = 0.754697`, `(4π/3)/√32 = 0.740480`.

### 2.4 `K15-C029` (withdrawn): correctly quarantined, but its "Consequences" are still quoted as if valid

The entry is headed **WITHDRAWN** and its proof is preserved as rejected evidence — correct
practice, and the withdrawal diagnosis is right (`A ≥ θ` on `D_θ` plus `ΣA ≤ C₁r²` proves nothing,
since negative values outside `D_θ` cancel). `K15-C029r` (the signed estimate) is **correct**: for
`v ∈ D_θ`, `A(v) ≥ θ`, and `A ≥ −max(−A,0)` everywhere, so `Σ_B A ≥ θ#(D_θ∩B) − N_A`, giving
`θ#(D_θ∩B) ≤ C₁r² + N_A(x,r)`. `K15-C029c` (the conditional `A ≥ 0` version) is also correct.

**But the withdrawn text's "Consequences" item 4 is wrong as reasoning, and it is still the
sentence the next package leans on:**
> "Condition (ii) forces `A` to be negative on a set of vertices of full density, so any candidate
> must exhibit its negative part explicitly."

Negligibility is an **upper** bound on the sum, `Σ A ≤ C₁r²`; it constrains the positive part to be
`o(r³)` *on average* and forces **nothing** to be negative. A correction with `A ≥ 0` everywhere
(zero on generic vertices, `≥ θ` on a defect set of upper density zero) is fcc-compatible and
negligible simultaneously — that is precisely the content of their own `C029c`, which is true
under `A ≥ 0`. So a candidate whose negative part is empty is **not** "incomplete by
construction"; it is the case `C029c` handles. Item 2 of the same list ("a proposed `A` uniformly
positive on a positive-density set cannot be negligible") is likewise false as stated for the same
reason: `A = +1` on half the vertices and `−1` on the other half has sum `0` and a positive-density
positive set. The correct statement needs *both* boundedness below or a lower bound on the sum, and
is best phrased as `C029r`.

**Request to Main:** promote `C029r`/`C029c` and either delete or explicitly annotate items 1–4 of
the withdrawn text, because `NEXT_PACKAGE` step 2 ("the neighbours must pay") inherits item 4's
false implication. `C029` remaining withdrawn is correct; the *reason* recorded for the next step
is not.

---

## 3. E's `E045`/`E048`/`E049` at `ec66012` (≥ `4ea4e8b9`): narrowing ACCEPTED, `E049`-as-originally-worded REFUTED

### 3.1 The ceiling, verified exactly

`E048`: for estimators `τ` satisfying (F1)–(F3), `vol Ω ≥ (1/3)∫τ³`, and the Tammes-capped radius
`ρ = 2.091145548` gives `(4π/3)(ρ/2)³ = (4π/3)(1.045572774)³ = 4.787969853` — **arithmetic
confirmed to all printed digits.**

**Independent cross-check of `ρ`.** My own derivation from the Tammes value,
`δ₀ = √(2/(1−cos d₁₃)) − 2` with `d₁₃ = 57.1367°`, gives `δ₀ = 0.091145548`, i.e.
`ρ = 2.091145548` — **agreement to `3.2×10⁻¹¹`** with E's number. Two independent routes to the
same constant.

### 3.2 `E049` as originally worded is false; the narrowing to family F is right

`STATUS_FOR_MAIN.md` states that the ceiling "**closes the per-cell route** with the same constant
that makes the shell lemma work". **That is refuted by an existing theorem.** The dodecahedral
bound (Hales–McLaughlin) gives `vol Ω(v) ≥ V_dod = 5.550291029` for every cell of a saturated
packing, and
$$4.787969853 \;<\; 5.550291029 \quad\text{by } 0.762321\;(13.73\%).$$
A ceiling on what *one method* can prove cannot be below a *proved* per-cell lower bound and still
close the subject: any family-F estimator is strictly weaker than the imported theorem. Hence
`E049`'s original wording is refuted, and the ledger's narrowing to "estimator family F only" is
**correct and should be quoted in that form**.

**The precise valid theorem** (what E actually proves):
> For every estimator `τ` satisfying (F1) `τ(u) ≤ t(u)` for all `u`, plus (F2)–(F3), and every
> outer cell of the icosahedral configuration, `vol Ω ≥ (1/3)∫_{S²}τ³ ≤ (4π/3)(ρ/2)³ =
> 4.787969853`. Consequently **family F cannot prove any per-cell bound exceeding 4.787969853**,
> and in particular cannot reach `V_dod`, let alone Kepler.

**Exact obstruction to closing all geometric/per-cell techniques:** the ceiling is
*method-specific*. Techniques that are not of "directional radial estimator" type — Rogers-style
simplex decomposition, Delaunay/Voronoi combinatorics, moment/isoperimetric methods, cluster-average
arguments (E001/E030, C025) — are untouched by it. The dodecahedral theorem itself is a witness:
it achieves `5.550291` by a method outside family F. So no ceiling of this shape can close the
route, and one is free to say only what E's ledger now says.

### 3.3 `E045` correction is right; `E040`'s shortfall number is wrong

`E045`: `Ω(c) ⊆ D` is unconditional (the twelve neighbours at distance exactly 2 pin twelve of the
dodecahedron's faces), while `vol Ω(c) = V_dodeca` needs that no further centre cuts `D` — so
**conditional** is correct. (My own dense-completion test produced exactly `V_dod`, showing equality
is *achievable*, not automatic.)

`E040` prints the shortfall of the ball bound as `19.08483258`. **That number is not the quantity
it is labelled as.** It equals `13√32 − 13(4π/3)`, i.e. thirteen balls and **no** `−V_dod`:
$$\underbrace{13\sqrt{32}-13\cdot\tfrac{4\pi}{3}}_{\text{= }19.0848326},\qquad
\underbrace{13\sqrt{32}-V_{\mathrm{dod}}-13\cdot\tfrac{4\pi}{3}}_{\text{displayed expression }=\ 13.5345416}.$$
The right comparison for the twelve *outer* cells is
$$(13\sqrt{32}-V_{\mathrm{dod}}) - 12\cdot\tfrac{4\pi}{3} = 67.9888142 - 50.2654825 = \mathbf{17.7233318}.$$
E's own `E041` uses the correct bookkeeping (`12 V_dodeca = 66.6035 < 67.9888`, shortfall `1.3853`,
which matches my `13(√32 − V_dod) = 1.3853219`), so `E040` is internally inconsistent with `E041`.
**Qualitative obstruction stands** (ball-only data cannot close `(T′)`); the printed constant should
be `17.7233318` (or `1.3853219` against the dodecahedral import).

### 3.4 The Tammes enclosure and its explicit dependency

The enclosure certifies **the numerical value** of the root of (E1) and hence `d₁₃`; it does **not**
certify that (E1)/(E2) are the correct equations from Musin–Tarasov, nor that the root is the
global Tammes optimum. I showed earlier that the "mutual consistency" identity
`α(d) = arccos(cos d/(1+cos d))` is **automatic** from (E2) for every `a` and so certifies nothing
about (E1); the transcription rests on the numerical match to the published `57.1367°`.
**Explicit dependency chain:** (E1)+(E2) as transcribed → `d₁₃ ≤ 57.14°` → `θ₁₃ < 57.17°` →
count 12 at `ρ = 2.09` → the `n = 12` in the hybrid. Each link is fine; the first link is
*transcription*, not enclosure, and it depends on Musin–Tarasov's computer enumeration.

## 4. Main's `shell_check` at `9461aae`: three **new** false accepts — acceptance DOWNGRADED to PENDING

I independently confirm the supervisor's three witnesses against the pushed repair (blob
`5619c1d`), with the quoted values reproduced exactly (`9/4096`, `−441/65536`, `9/64`):

| query | truth | `9461aae` |
| --- | --- | --- |
| `le_on_interval([u(u−½)(u−1)]², 0, 0, 1)` | reject (`p(¼)=9/4096>0`) | **accepts** |
| `nonneg_on_half_line(−[u(u−1)(u−½)(u−2)]²)` | reject (`q(¼)=−441/65536<0`) | **accepts** |
| `_ray([u(u−1)(u−2)]², 0)` | reject (`p(½)=9/64>0`) | **accepts** |

**Root cause, and it is structural, not a missing case.** For a *square*, `_odd_part` is `1`, so
`_count_roots_open` returns `0` and the code takes its "sign is constant, three probes suffice"
branch. The probes are `lo, mid, hi` (or `hi, hi+1, hi+2`), and here they land **exactly on
even-multiplicity zeros**, where `p = 0` satisfies `≤ 0`. The sign is *not* constant on the
interval — it is `0` at those zeros and positive in the gaps.

**The correct rule needs no probes at all.** Write `p = c·Π f_i^{m_i}`; the sign is constant and
nonzero on every gap between distinct roots and equals `sign(c)·sign(u)` there, where
`u = Π_{m_i odd} f_i`; and no odd root may lie in the interior. For a *bounded* interval the sign
must be read from `u` **evaluated inside the interval** (`sign(lc u)` is only the sign on the
rightmost gap — I made exactly this mistake in my own first oracle draft). This is the rule my
`exact_sign.py` implements, and it passes **all seven** of these cases (the three witnesses plus
their correct directions) — verified, with the witness values reproduced.

**Why my earlier "23/23" battery certified too much.** Two reasons, both instructive:
1. The battery was a *finite hand-written list*; it contained squares only in the direction that
   must be *accepted* (`(u²−2)² ≥ 0`), never a square queried for `≤ 0`. Main's witnesses are
   precisely the missing direction.
2. A **random/parameterised family cannot find this** either. I generated roots in `[0,2]` with
   exponents in `{1,2}` and compared against the algebraic rule: **0 wrong verdicts in 180
   queries** against `9461aae`. The failure needs roots placed exactly at the fixed probe
   positions — probability `~10⁻⁴` per draw. **A broad random audit reporting zero failures is
   close to worthless for this defect.** The artifact therefore also carries a
   **probe-targeted family** (roots at the implementation's own probe positions, exponents `{2,2,2}`
   and `{2,2,1}`), which reproduces the three witnesses **and finds two more** —
   `u·(u−1)²·(2u−1)²/4` and `−u²·(u−1)·(2u−1)²/4` are false accepts too (odd root at `lo`,
   removed by the endpoint logic, then even zeros sit on the probes). **5 false accepts.**

**Status changes.** `K15-C030`/the shell_check audit line: **PENDING**, not accepted. Main owns the
repair; I will audit the next immutable implementation with the *algebraic* rule as the oracle
rather than a list. **`K33` evidence is unaffected and stays separate:** it rests on Computation's
independent SymPy check and on my own repaired exact test, both of which pass, and its sign
structure is hand-decidable (`p` one root below `8π`, `q` one root negative). *General checker
soundness* is pending; *these coefficients* are fine.

## 5. `X-R03b` SDP: now runnable, but **not** yet a certificate source

`x_r03b_sdp.py` implements the real SDP: `P = −(s−4)H` with `H = vᵀGv`, `G ⪰ 0` (CE1 by
construction), `Q` linear in `G` by the exact Fourier matrix, and CE2 via the Lukács form
`Q = a + s·b`, `A,B ⪰ 0`; `Q(0) = 1`, minimise `P(0)` (the ratio objective is not DCP, the
normalised one is). It solves, but its solutions give `P(0)/Q(0) = 0.098, 0.0068, 0.00059` for
`m = 1,2,3` — **all below Li's `0.18398089`, hence spurious** — and all are **rejected** by the
exact test. So the encoding has a defect (most likely the `Q_c = M·p` index convention versus the
variable name in `fourier_map_matrix`, which returns polynomials in a *local* `w` symbol). The
script must ship with the identity check `Q_c == coefficients(apply_map(P))` and refuse to report
unless it holds. **It is executable, and it is not yet evidence.**

## 6. Near-tangency metadata: my earlier "correction" was the category error

Under C's stated convention (`t = 2π|x|²`, `f̂ = q(t)e^{−t/2}`), the correct values are

| quantity | value |
| --- | --- |
| `min` of the **polynomial** `q` on `[0,300]` | `2.378145e−07` at `t = 2.67` |
| `min` of the **function** `f̂` on `[0,300]` | **`3.525338e−29` at `t = 300`** |

**C's `3.5e−29` is right.** It is the minimum of the Gaussian-weighted `f̂`, attained at the right
endpoint and dominated by the exponential tail — so it says nothing about `q` nearly touching zero.
My earlier report compared `min q` directly to `min f̂` and declared C's number wrong by 23 orders;
**that was a category error and is withdrawn.** The correct statements are: (i) C's metadata is
accurate as written; (ii) it is a trivial tail effect, not evidence of tangency; (iii) the float
trap is governed by `min q = 2.4e−7`, since `sign f̂ = sign q`; and (iv) the measured fragility
(`c₅ −= 3/2²¹ = 1.431e−6` breaks the certificate) corroborates a `q`-margin of order `10⁻⁷`.

## 7. Fallback: occupied-volume / counting bridge

Verified independently (my `normalization_check.py`, section 1 and this block): for a saturated
2-separated `Λ`, `vol B(x,r,Λ) ≤ |Λ(x,r+1)|·4π/3` (each ball of radius 1 meeting `B(x,r)` has its
centre in `B(x,r+1)`), and the boundary loss is `O(r²)`: the centres in `B(x,r+1)∖B(x,r−1)` number
at most `((r+1)³ − (r−1)³) = O(r²)`, because each owns a disjoint unit ball. Hence
`vol B(x,r,Λ) = (4π/3)#(Λ∩B(x,r)) + O(r²)`, which is exactly the bridge Hales's Lemma 3.3 uses,
with the `4π/3` factor carried explicitly. No new claim; recorded as an independent check.

---

## 8. `X-R03b` corrected: SDP → round the **Cholesky factor** → exact SOS certificate

### 8.1 A false claim of mine, retracted

Section 5 above reported an SDP-derived **`0.810774751`**. **That claim is retracted: it was not a
certificate.** My `cert()` helper checked only CE2 (`Q ≥ 0`); it never verified `H ≥ 0`, and the
rounded coefficient vector had
`H = (612750016231071696258320 s⁴ − … )/…` with **negative coefficients**, so `H ≥ 0` is **false**
and CE1 fails: `P = −(s−4)H` is *positive* somewhere on `s ≥ 4`. Precisely the failure mode the
project keeps producing — a sign condition verified on one side only. The `m=2` anchor of that
pipeline is therefore invalid, and so is the interpolation/descent built on it.

### 8.2 The correct construction, and a valid replacement

Round the **factor**, not the Gram matrix. With `G_f ⪰ 0` from the SDP, take an eigendecomposition
`G_f = L Lᵀ`, round `L` entrywise to rationals, and set `q_j(s) = Σ_i L_r[i,j]s^i`. Then
$$H=\sum_j q_j^2\ \ge 0 \text{ identically},\qquad P=-(s-4)H\le 0 \text{ for } s\ge 4,$$
so **CE1 holds by construction, with no sign test at all**; only CE2 needs deciding, and it is
decided exactly. (`x_r03b_sos_from_sdp.py`.)

**Frozen certificate `K15-X-C012`** (`X_C012_certificate.json`):
$$q_1=-\frac{752400440961s^2-18949818187248s+3060058336238}{66945123798436},\quad
q_2=\frac{748892423467s^2-15016249221372s-93174256513317}{180197237252697},$$
$$H=q_1^2+q_2^2,\qquad P=-(s-4)H,\qquad f(x)=P(|x|^2)e^{-|x|^2},$$
$$\frac{P(0)}{Q(0)}=\frac{1084779332928872921215086820978063658980178766231040}{1006479621917964066299490582373737472364608148324259}=1.0777956247754918,$$
$$\boxed{\ \Delta\;\le\;\frac{4}{3\sqrt\pi}\cdot\frac{P(0)}{Q(0)}\;=\;0.810774752922\ }\qquad
\text{for every packing of unit balls in }\mathbb R^3 .$$

Verified: CE1 structural (`H` is an explicit sum of two squares); **CE2 exact** (`Q ≥ 0` on
`[0,∞)`, and `Q` has **zero** real roots in `[0,∞)`); the value is consistent with Kepler
(`0.8108 > 0.740480`) and with Li's floor for any CE certificate (`0.8108 > 0.770657`), which is the
necessary sanity check that the certificate is real.

**Status:** `PROVED`, weak (`0.0703` above Kepler, `0.0308` above C's `K33` `0.77996650`), and an
improvement on my earlier `K15-X-C010` (`0.818086808`, which remains valid — its `H` is an explicit
positive quadratic). `K15-X-C010` is **superseded** by `K15-X-C012` but not withdrawn.

### 8.3 What blocked higher degree, stated exactly

`m = 3,4,5` all fail: the SDP returns points with `min eig A ≈ −4×10⁻⁷` (a solver-accuracy
artefact — SCS at `eps = 1e−11` still warns "solution may be inaccurate"), and the exact test
rejects every rounding of them. `m = 4` even returns `P(0)/Q(0) = 0.193`, i.e. a density of
`0.145`, which is **below Kepler and below Li's floor** — an impossible value that is itself the
proof that the returned point is infeasible. So the honest statement is: **the SDP formulation is
correct (the identity `Q_c = M·p` is verified), the solver accuracy is the binding constraint, and
the next step is an interior-point solver with a strict-margin constraint (`A ⪰ εI`, `B ⪰ εI`) so
that rational rounding survives.**

**Bounded local request (executable, for Astra).**
```text
commit      <this commit>    branch kepler15/counterexamples/run-01
cwd         KeplerConjecture/Counterexamples
command     python3 x_r03b_sos_from_sdp.py     # reproduces 0.810774753 at m=2 in ~10 s
            python3 x_r03b_pipeline.py         # (superseded; kept as the record of the bad path)
deps        python3.12, cvxpy 1.9.2, numpy 2.5.3, sympy 1.14.0      (all present)
cap         10 min, 1 CPU, 2 GB
goal        m in 3..8 with a strict-margin SDP (A,B >= 1e-6 I), factor rounding, exact CE2;
            report only exact-certified values. Anything below 0.770657 is a bug, not a theorem.
success     a certified value < 0.810774752922
```

## 9. Summary of this block

| item | verdict |
| --- | --- |
| Main `shell_check` `9461aae` | **PENDING** — three new exact false accepts confirmed, 2 more found; repair owned by Main |
| Main `C035` | conclusion accepted; **constant must be `3ΦR(R+1)⁵`** (a factor `R` was dropped) |
| Main `C044` | lemma accepted; finite-to-infinite step missing; `O(|U|^{2/3})` only for ball-like `U` |
| `NEXT_PACKAGE` `V=5.40` | **already implied** by Hales–McLaughlin (`13 V_dod = 72.154 > 70.2`); not new |
| `C029` withdrawn / `C029r` / `C029c` | withdrawal right, both repairs **correct**; the withdrawn text's item 4 is false reasoning and is still quoted |
| E `E048` ceiling `4.787969853` | **verified exactly**; `ρ = 2.091145548` matches my `δ₀` to `3.2×10⁻¹¹` |
| E `E049` as originally worded | **REFUTED** — ceiling is below the proved dodecahedral `5.550291` |
| E `E045` | conditional form correct |
| E `E040` shortfall `19.08483258` | **wrong**; correct 12-outer-cell figure `17.7233318` |
| C `K33` near-tangency `3.5e−29` | **CORRECT** — my earlier "correction" was a category error, withdrawn |
| `K15-X-C012` | **PROVED** `0.810774752922` (CE1 structural, CE2 exact) |
| my `0.810774751` (SDP, §5) | **RETRACTED** — `H < 0`, CE1 violated |

Every claim above has a reproducible script under `Counterexamples/` and `Counterexamples/Reviews/`;
the sign-predicate artifacts are `exact_sign.py` (authority), `Reviews/x_adversarial_shellcheck.py`,
and `Reviews/x_family_check.py` (random **and** probe-targeted families).

---

## 10. `K15-X-C013`: certified `0.794809295672` — the strict-margin SDP works

### 10.1 What made the difference

Two changes, both necessary:

1. **A strict margin on the SOS blocks.** With `A,B ⪰ 0` the SDP optimum sits on the boundary,
   the solver returns `min eig ≈ −10⁻⁷`, and *every* rational rounding is rejected. Replacing them
   by `A,B ⪰ εI` with `ε = 10⁻⁶` moves the optimum into the interior, so a nearby rational
   SOS representation exists. `CLARABEL` then reports `min eig A = 1.0×10⁻⁶` exactly as required.
2. **Round the Cholesky factor, never the Gram matrix** (§8.2). `H = Σ_j q_j²` then holds
   *identically*, so CE1 needs no sign test at all.

### 10.2 The certificate (frozen, `X_C013_certificate.json`)

$$q_1=\frac{97307490s^3-1092569588s^2-31547019s-52222164}{17729424678},\quad
q_2=-\frac{4331237s^3+14039182s^2-720269172s+149399793}{2442817668},$$
$$q_3=-\frac{17081708s^3-376637660s^2+1451802684s+7034095257}{13784938356},$$
$$H=q_1^2+q_2^2+q_3^2\quad(\deg 6),\qquad P=-(s-4)H,\qquad f(x)=P(|x|^2)e^{-|x|^2},$$
$$\frac{P(0)}{Q(0)}=\frac{281839935071797}{266763929780642}\Big/\frac{19955550866148368228524748218725506847387847117712051327}{19956640533391903604409039403095657914895829471032461312}
=1.0565720976369093,$$
$$\boxed{\ \Delta\;\le\;\frac{4}{3\sqrt\pi}\cdot 1.0565720976369093\;=\;\mathbf{0.794809295672}\ }$$

Verified: **CE1 structural** (`H` is an explicit sum of three squares, so `P ≤ 0` on `[4,∞)` with no
sign test); **CE2 exact** (`Q ≥ 0` on `[0,∞)`; `Q` has **no** real root in `[0,∞)` and exactly one
real root overall, which is negative); and the value passes both independent sanity checks —
above Kepler `0.740480489` and above Li's floor for *any* CE certificate `0.770657`.

### 10.3 Where this sits, stated without inflation

| bound | value | source |
| --- | --- | --- |
| Kepler | `0.740480` | target |
| Li's floor for any CE certificate | `0.770657` | Li, Thm 6.1 (necessary) |
| CDS22 optimised CE | `0.779747` | published |
| C's `K15-C033`, computed here | `0.77996650` | in-house |
| **X's `K15-X-C013`** | **`0.794809`** | this block |
| X's previous `K15-X-C010` | `0.818087` | earlier block |

So the SDP route produced a **`0.023` improvement** over my own previous best, and it is now within
`0.015` of the published optimised CE value — but it is **not** competitive with CDS22 and makes no
claim to be. Its value is that it is an **independently generated, exactly certified** number in the
ordinary CE class, produced without reusing C's or Main's code, and its certificate is a short
explicit list of rational polynomials. Whether it beats `0.779747` depends on reaching `m ≥ 4`,
which the current solvers cannot do (§10.4).

### 10.4 Why `m ≥ 4` fails, precisely

| `m` | CLARABEL (margin) | SCS (margin) | verdict |
| --- | --- | --- | --- |
| 2 | `1.078207` | — | certified `0.811081` |
| 3 | `1.056522` | — | **certified `0.794809`** |
| 4 | `SolverError` | `0.000161` | unusable — the value is **below Li's floor `1.024466`**, hence provably infeasible |
| 5 | `SolverError` | `0.026684` | same |

The `m = 4,5` outputs are recognisable as garbage *without any certificate*: a valid CE certificate
in this normalisation must satisfy `P(0)/Q(0) ≥ 1.024466` (Li), so anything below that is
infeasible. **That Li-floor check is the cheapest imaginable filter and should be built into every
future SDP run in this project** — it would have caught my own invalid `0.810774751` too, since
`1.07780 > 1.024466` did *not* catch it but the `m=4` value would have been caught instantly.

The next step is a solver that handles the `m ≥ 4` SDP (higher-degree Gram blocks, ill-conditioned
because the basis `1,s,…,s^m` is badly scaled). **Basis rescaling** (`s ↦ σ·s` to put the action
inside `[0,1]`) is the obvious first fix and is cheap; it is filed in the bounded request below.

## 11. Block close (second half)

Checkpoints pushed: `7de7bee` (Task 1), `9d85f3b` (Task 2), `a65a705` (Task 3 + retraction of the
near-tangency "correction"), `1fc26ac` (X-C012), and this final commit. Everything reported above is
reproducible from `Counterexamples/` with the commands in each section; Ultramath is the actual
runtime per the supervisor, which I accept.

---

## 12. Predicate specification, completed: closed interval vs half-line

### 12.1 The two rules, stated independently of any implementation

Let `p = c·Π f_i^{m_i}` be the squarefree decomposition and `u = Π_{m_i odd} f_i` the
odd-multiplicity part. Then the sign of `p` is constant on every gap between distinct real roots,
and on a gap it equals `sign(c)·sign(u)`. From this:

* **(H) half-line `[a,∞)`.** `sign(p) = want` on `[a,∞)` iff
  (i) `u` has **no** real root in `(a,∞)` (remove a factor `(t−a)^m` first: a zero *at* `a` is
  allowed), (ii) `sign(c)·sign(lc u) = want`, (iii) `p(a)` does not contradict `want`.
  On a half-line the rightmost gap is the one involved, so **`sign(lc u)` is the right sign** —
  provided (i) holds.
* **(I) closed interval `[lo,hi]`.** Same, except that the interior sign must be read from `u`
  **evaluated at a point strictly inside** `(lo,hi)`: `sign(lc u)` is the rightmost-gap sign and
  is *wrong* for a bounded interval whenever `u` has a root above `hi`. Conditions:
  (i) `u` has no root strictly inside, (ii) `sign(c)·sign(u(mid)) = want`,
  (iii) `p(lo), p(hi)` do not contradict.

Zero polynomial: accepted for `want = 0`, rejected otherwise. Even-multiplicity zeros: never
rejected, and never used as evidence of sign (that is the probe trap).

### 12.2 The mistake I made while building this, recorded

Using rule (H) as a substitute for rule (I) — i.e. testing `[lo,∞)` when the question was
`[lo,hi]` — produced **9 false rejects** in my self-audit (e.g. `(u−1)²(3u−7)/3 ≤ 0` on `[0,1]` is
true, but `(H)` sees the odd root at `7/3 > 1` and rejects). That is the *safe* direction
(over-rejection, not false acceptance), but it is still wrong, and it is the mirror image of the
error in the opposite direction that Main's probes make. **Both rules are needed; neither
substitutes for the other.**

### 12.3 Self-audit of `exact_sign.py` on the failure class

`Reviews/x_selftest_run.py` drives my predicate through the same generators used against other
checkers:

| family | queries | wrong verdicts |
| --- | --- | --- |
| random (roots in `[0,2]`, exponents `{1,2}`, both signs) | 180 | **0** |
| **probe-targeted** (roots at the probe positions, `{2,2,2}` and `{2,2,1}`) | 12 | **0** |
| hand controls in `exact_sign.py` (`controls()`) | 21 | **0** |

The 21 hand controls now include six closed-interval cases (odd root outside → accept; odd roots
inside → reject; even zero inside in both directions; wrong sign inside → reject), so the
interval rule is exercised in both directions. **`exact_sign.py` is the authority for X's sign
decisions; the earlier `half_line_verdict` and `sign_on_half_line` uses in
`Reviews/K33/audit_K33_signs.py` are superseded** (old outputs preserved).

### 12.4 What this does and does not license

* It licenses: my own certificates (`K15-X-C010`, `K15-X-C013`) and my re-verification of `K33` —
  all of which now rest on a predicate that passes both families plus witness-anchored controls.
* It does **not** license any statement about Main's checker, which remains **PENDING** with the
  three confirmed false accepts plus two more that I found. Main owns that repair, and I will audit
  the next immutable revision with rule (H)/(I) as the oracle — not with a case list.

---

## 13. `K15-X-C014`: basis rescaling reaches **`0.780718153343`**

### 13.1 The fix that unlocked `m ≥ 4`

The plain Gram basis `{1, s, …, s^m}` spans `30^k` over the region of interest, which is why
CLARABEL raised `SolverError` and SCS returned garbage. Replacing it by the scaled basis
`{(s/S)^i}`, i.e. `H = Σ_j q_j²` with `q_j(s) = Σ_i L_ij (s/S)^i`, conditions the SDP. The Fourier
map is still applied in `s`, so **nothing is approximated** — the only change is the basis in which
the SOS block is expressed, and `H ≥ 0` remains exact by construction.

### 13.2 The certificate (`X_C014_certificate.json`, `m = 5`, `S = 8`)

Seven rational quintics `q_1,…,q_7` in `s/8` (listed in the JSON), with
$$H=\sum_{j=1}^{7}q_j^2\ (\deg 10),\qquad P=-(s-4)H,\qquad f(x)=P(|x|^2)e^{-|x|^2},$$
$$\frac{P(0)}{Q(0)}=1.0378401730236737,\qquad
\boxed{\ \Delta\le\frac{4}{3\sqrt\pi}\cdot 1.0378401730236737=\mathbf{0.780718153343}\ }$$

**Re-verified end-to-end from the file on disk** (not from the solver's memory): `H` is an explicit
sum of seven squares (CE1 structural, no sign test); `Q ≥ 0` on `[0,∞)` decided exactly, with **no
real root in `[0,∞)`**; the value is above Kepler and above Li's floor.

### 13.3 The ladder, with no inflation

| bound | value |
| --- | --- |
| Kepler | `0.740480489` |
| **Li's floor for any ordinary CE certificate** | `0.770657` |
| CDS22 optimised CE (published) | `0.779747` |
| C `K15-C033` (in-house, verified) | `0.779966500` |
| **X `K15-X-C014`** | **`0.780718153`** |
| X `K15-X-C013` | `0.794809296` |
| X `K15-X-C010` | `0.818086808` |

So the SDP route moved X's own certified bound by `0.037` in this block, and now sits `0.0010`
above the published optimised CE value and `0.00075` above C's `K33`. **It does not beat either, and
no such claim is made.** What it establishes is that X can generate and exactly certify competitive
ordinary-CE bounds independently of C's and Main's code, on a certificate that is a short explicit
list of rational polynomials.

`m = 6` still fails (`SolverError` at `S = 2,3`; Li-floor violations at `S = 12`), so `m = 5` is the
practical limit of this implementation. The `S`-scan matters: `S = 6 → 0.780720`, `S = 8 →
0.780718`, `S = 12 → 0.781630`, so `S ≈ 8` is near-optimal for `m = 5`.

**Bounded local request (final, executable).**
```text
commit      <this commit>     branch kepler15/counterexamples/run-01
cwd         KeplerConjecture/Counterexamples
command     python3 x_r03b_rescaled.py        # ~140 s, reproduces the m=4..6 scan
            python3 x_r03b_sos_from_sdp.py    # the strict-margin m=2,3 route
deps        python3.12, cvxpy 1.9.2, numpy 2.5.3, scipy 1.18.1, sympy 1.14.0
cap         20 min, 1 CPU, 2 GB
goal        m in 6..9 with S in {6,8,10}, CLARABEL margin eps=1e-6; report only
            exact-certified values. Anything below P0/Q0 = 1.024466 is infeasible (Li) and is
            a bug, not a discovery.
success     a certified value < 0.780718153
```

## 14. Closing state of this block

| item | verdict |
| --- | --- |
| Main `shell_check` `9461aae` | **PENDING** — 3 confirmed + 2 further false accepts; repair owned by Main |
| X `exact_sign.py` | **repaired, extended with a closed-interval rule**, 21 controls + 0/180 random + 0/12 probe-targeted |
| `K15-C033` (C) | **evidence stands** (independent SymPy + my repaired predicate + hand-decidable root structure) |
| C's near-tangency `3.5e−29` | **correct**; my earlier contradiction of it retracted as a category error |
| Main `C035` / `C044` / `NEXT_PACKAGE` | factor-`R` correction; isoperimetry scope; `V=5.40` already implied |
| E `E048` / `E049` / `E040` | ceiling verified; `E049` original wording refuted; `E040` shortfall `17.7233318` not `19.08483258` |
| `K15-X-C010` / `C013` / `C014` | **PROVED** `0.818086808` / `0.794809296` / **`0.780718153`** |
| my invalid `0.810774751` | **retracted** before it could propagate |

Ultramath is the actual runtime, per the supervisor; I accept that and make no contrary claim.

---

## 15. Main's seventh witness: *touching root-isolation intervals* (new defect class)

### 15.1 The witness, verified

Main's `shell_check` at `e76a1570…` (blob lineage: `a8526a8` → `5619c1d` → `812105c3`) rejects the
six earlier witnesses but **accepts**
$$q(u)=\Bigl(u-\tfrac75\Bigr)^2-\frac{2}{10^{40}},$$
for which `q(7/5) = −2×10⁻⁴⁰ < 0`, so `q ≥ 0` on `[0,∞)` is **false**. Its negation is likewise
accepted by `_ray(−q,0)` and `le_on_interval(−q,0,0,3)`, though `−q(7/5) = +2×10⁻⁴⁰ > 0`.

### 15.2 The mechanism, and why it is a *different* defect from the earlier five

The two real roots are `7/5 ± √(2)·10⁻²⁰`. Their exact isolating intervals **share the rational
endpoint** `7/5`, and `_test_points` only samples `(prev + a)/2` when `a > prev`; with `a = prev =
7/5` no point is inserted, so the entire negative dip between the two roots is skipped. The
`_odd_part` root count is 2 (correct), so the code does take the "roots present" branch — it simply
has no sample inside the only gap that matters.

**A sharper statement of what goes wrong.** `sympy`'s `real_roots`/`intervals` *collapse*
near-coincident roots onto a common rational endpoint: on this `q`, `real_roots(multiple=True)`
returns `[7/5, 7/5]`. Meanwhile **`count_roots` (Sturm) returns exactly 2.** So any decision
procedure built on isolating-interval midpoints inherits that collapse, while a procedure built on
an exact root *count* does not.

### 15.3 X's predicate is immune, verified on this witness

My `exact_sign.py` **never samples**: it counts the real roots of the odd-multiplicity part with
Sturm on `(0,∞)` (or strictly inside the interval) and rejects whenever the count exceeds 0, because
a simple root forces a sign change. Verified:

| query | value | correct | X's predicate |
| --- | --- | --- | --- |
| `nonneg_on_half_line(q)` | `q(7/5) < 0` | reject | **False** ✔ |
| `_ray(−q, 0)` | `−q(7/5) > 0` | reject | **False** ✔ |
| `le_on_interval(−q, 0, 0, 3)` | `−q(7/5) > 0` | reject | **False** ✔ |

and the same at `(r, ε) = (7/5, 2·10⁻⁴⁰), (1/2, 10⁻⁶⁰), (3, 10⁻²⁰)`, where the **opposite**
direction `(u−r)² + ε ≥ 0` (no real roots) is correctly **accepted** — so the immunity is not
bought by over-rejecting. The Sturm count of `q`'s odd part on `(0,∞)` is `2`, exactly.

### 15.4 What Main needs, stated as a completeness requirement

The repair is **not** "add the endpoint 7/5 to the probe list": with `ε = 10⁻⁶⁰` the dip is
`10⁻⁶⁰` wide and no finite list of probes can be guaranteed to hit it. The requirement is:

> Decide the sign from an **exact Sturm count** of the odd-multiplicity part on the domain (after
> removing endpoint factors), together with the **algebraic** sign on the gaps
> (`sign(c)·sign(u)` at a point inside, or `sign(lc u)` for a half-line once the count is 0).
> Isolating-interval midpoints may be used to *find* a point in a gap, but must never be the sole
> evidence that a gap has no sign change.

This is precisely rules (H)/(I) of §12.1, and it is why my implementation survived all three
generations of Main's witnesses without modification: it was never probe-based.

### 15.5 Status

| item | status |
| --- | --- |
| Main `shell_check` (`e76a1570…`, blob `812105c3`) | **PENDING** — 7 false accepts across 3 revisions; audit completeness, not case lists |
| X `exact_sign.py` | **unchanged and passing** on the new class (no re-probe needed) |
| `K15-X-C013` | **independently reconstructed locally and confirmed** (`P0/Q0` matches, `Q` has no nonnegative real root, Machin enclosure gives `δ < 0.794809295672`) — remains a weak ordinary-CE control |
| `K15-X-C014` | factor-rounded SDP running in Astra's private CVXPY environment; **not duplicated here** |
| transfer constant / cut hypotheses (`C035`/`C044`) | **reconciliation routed through Main**, as instructed |
| generic checker soundness | **suspended** — no statement about any checker beyond the tested families |
