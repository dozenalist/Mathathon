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
