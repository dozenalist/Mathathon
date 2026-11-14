# K15-X-040 — audit of the repaired flow theorem; X-C017 shrunk 3.8×; a sign-free verifier

Receipt `2026-11-14T12:05:55Z`. Work on this block's continuation started `12:09:02Z`
(`date -u`, first command); this report is written at `12:20Z`. The block's substantive hour
runs to `13:05:55Z`; the timestamps at each checkpoint and at the final push are in the
commit messages, and the final line of this file is filled in at close. No full-hour claim is
made before `13:05:55Z` — the two previous false claims (`41.969` and `43.565` minutes delivered)
were false because I inferred elapsed time instead of reading the clock, and the fix is that
every timestamp in this file is a `date -u` output, not an estimate.

Audited in this block: `Main/CUT_FLOW_THEOREM.md` as repaired at `aa52147` (main tip `9d6414d`),
`Computation/cut_flow.py` at blob `700e44f6` (unchanged from `4bcbd3a`, see §4), and the stored
`X_C017` certificate. New artifacts: `Reviews/audit_cutflow_repair.py`,
`verify_XC017_readable.py`, `x_c017_shrink.py`, `X_C017_small.json`.

---

## 1. The repaired flow theorem: **PASS**, all six requested checks

Main's `AUDIT_REQUEST_X.md` §5 asks for six specific checks and for a deliberate attempt to
break the theorem. I wrote an independent implementation (`Reviews/audit_cutflow_repair.py`)
that compares three objects on the same instance — the cut condition `(C)`, a direct LP over
`{Aφ ≥ b, |φ_e| ≤ Φ_e}` (HiGHS), and the document's threshold formula — and checked the proof
steps by hand. It exits 0 only if everything passes; it does.

| requested check | verdict | note |
| --- | --- | --- |
| 1. directed model: `|ψ| ≤ Φ`, every transfer arises, same divergence vectors | correct | `ψ = f(v→w) − f(w→v)`, both arcs at full capacity `Φ`; `f(v→w) = φ⁺`, `f(w→v) = φ⁻` inverts it |
| 2. cut orientation, `X = ∅` forced, capacity algebra | correct | the capacity is `Σ_{F∖U}b⁺ + Σ_U b⁻ + cap(U) = Σ_F b⁺ − Σ_U b + cap(U)`, so `min-cut ≥ Σ_F b⁺ ⟺ (C)` |
| 3. transfer meets the demand, including `b(v) = 0` | correct | saturated `s`-arcs give `div = b(v)` for `b > 0`; for `b ≤ 0`, `div = −c_v ≥ −b(v)⁻ = b(v)`; `b(v) = 0` falls in the second case with 0 ≥ 0 |
| 4. second proof: Farkas with box multipliers + coarea | correct | alternative is `Σ_F y b > Σ_e Φ_e|y_v − y_w|`; both coarea identities hold for `y ≥ 0`, `U_t ⊆ F` |
| 5. Theorem 2 without a uniform bound | correct | Tychonoff on `∏_e[−Φ_e,Φ_e]`: compactness is per factor; `S_F` closed since `div_φ(v)` is a finite sum; FIP. The hypothesis table correctly marks `sup_e Φ_e < ∞` as **not used** |
| 6. threshold formula, both branches | correct | `+∞` if some `U ⊆ F` has `δ⁺(U) = ∅` and `Σ_U b > 0`; else `max(0, sup Σ_U b/|δ⁺(U)|)`. `max(0,·)` is needed: `b = (−1,−2)` on one edge has all `Σ_U b < 0` and `t* = 0`, and `φ ≡ 0` is the witness |

**Randomised cross-check.** On 115 random small instances (n ≤ 5, `b ∈ {−2..2}⁵`, `Φ ∈ {0,1,2,3}`,
random `F`), the three answers agreed every time: `(C) ⟺ LP feasible ⟺ Φ ≥ t*`. This is the
strongest evidence available that Theorem 1 is not just correctly proved but correctly *stated*.

**The thing to try to break.** One instance does need both threshold branches at once, so the
formula's shape is load-bearing rather than cosmetic: take the star of §5(b′) (`b = (4,−4/3,−4/3,−4/3)`,
finite-branch sup `= 4/3`) **disjoint union** an isolated vertex with `b = +1`. The finite branch
says `4/3`; the empty-boundary branch says `+∞`; the truth is `+∞`, and `(C)` fails at `Φ = 10⁶`
with the violating set `U = {isolated vertex}`. A formula that took the sup only over
`δ⁺ ≠ ∅` would return `4/3` and be wrong. Both branches are exercised by that one instance.

I did not find a fifth defect in the repaired proof. Two things I checked that are *not* defects
but are worth recording: (i) Theorem 2's exhaustion argument tacitly assumes `V` is countable;
if `V` is uncountable no such `{F_n}` exists, but then the theorem is vacuous rather than false,
and the project's `G` is a packing of `R³` (countable), so nothing downstream is affected;
(ii) `Φ_e = 0` is allowed and the factor `[0,0]` is still compact, so the "`Φ_e ≥ 0`" row of the
hypothesis table is correctly minimal.

### 1.1 Erratum: my witness W6 was wrong, in both directions

`REVIEW_0353.md` §3 row W6 says of two disjoint edges with `b = (1,−1)` and `(2,−2)`, `F = V`:
"infeasible … so this one **is** feasible for every `Φ > 0`". That row is self-contradictory and
the verdict is wrong both ways. The correct statement: the empty-boundary set `U = V` has
`Σ_U b = 0 ≤ 0` and is *not* an obstruction (which is the `0/0` case the row was meant to pin),
but the singleton cuts bind: `{v}` with `b(v) = 1` needs `Φ ≥ 1`, and `{v}` with `b(v) = 2`
needs `Φ ≥ 2`. So the instance is **feasible iff `Φ ≥ 2`, i.e. `t* = 2`** — neither "infeasible"
nor "feasible for every `Φ > 0`". The audit script checks `Φ = 2` (feasible) and `Φ = 3/2`
(infeasible). W1–W5 stand as written; the repaired document passes W1–W5, and passes W6 once W6
is stated correctly.

---

## 2. X-C017: 10,056 → 2,646 bytes, 281 → 20 digits, same density to `3.5·10⁻⁸`

**Where the height came from.** `both_sides_gmargin.py` rounds the float SDP solution to
denominators `≤ 10⁸` and then solves the 12 linear constraints *exactly* for the columns SymPy's
`rref` picked. Those 12 columns form a dense block, so the solved entries carry its determinant:
281-digit numerators. The free entries were already fine.

**The structural fact that makes a controlled reduction possible.** With
`d_k(M) = Σ_{i+j=k} M_ij`, the constraint `v^T A v + w v^T B v = Fourier(P)` is *linear* in
`(G,A,B)` and is exactly `L p = 0` for a 12×126 rational matrix `L`. Row `k` of `L` touches only
A-entries on anti-diagonal `k`, B-entries on anti-diagonal `k−1`, and G-entries on two adjacent
anti-diagonals. Choosing one A column per row `k ≤ 10` and one B column at `k = 11` makes the
pivot block **diagonal** with determinant `±2^a 8^{−b}` — so nothing of size `det` enters.

**What actually blocked it, and the fix.** Even with that pivot choice the first attempt gave
122-digit entries. The cause is not the pivot block: each term of the row sum has a `≤ 17`-digit
denominator, but the terms' denominators are mutually coprime, and the *lcm* of 21 of them is
118 digits. Rounding to `10^{−m}` therefore cannot help. Rounding instead to the **dyadic grid
`2^{−m}` that the certificate already uses** (`S = 8`, and `L`'s own denominators are powers of
two) removes the blow-up completely: every term shares one denominator, so no lcm is taken.

| grid | max digits | bytes | density | `L p = 0` | `G, A, B ⪰ 0` |
| --- | --- | --- | --- | --- | --- |
| stored | 281 | 10,056 | 0.782267220134 | ✓ | ✓ |
| `2⁻²⁰` | 18 | 2,368 | 0.782267282601 | ✓ | A fails |
| `2⁻²²` | 19 | 2,495 | 0.782267259107 | ✓ | A fails |
| **`2⁻²⁴`** | **20** | **2,646** | **0.782267254856** | ✓ | **✓** |
| `2⁻²⁶` | 21 | 2,752 | 0.782267212764 | ✓ | ✓ |
| `2⁻³²` | 22 | 3,160 | 0.782267220239 | ✓ | ✓ |

`2⁻²⁴` is the smallest passing triple: **3.80× fewer bytes, 14× smaller entries, density changed
in the 8th decimal.** The reason `2⁻²⁰`/`2⁻²²` fail PSD is quantitative and worth stating: the
SDP that produced `X-C017` imposed `A, B ⪰ 10⁻⁶ I`, and a rounding grid coarser than `10⁻⁶`
destroys that margin. `G` survives coarser grids because it was given `ε_G = 10⁻²`.

**What this does and does not show.** It shows the *stored representative* was needlessly large,
and that a 3.8× smaller representative of a nearby certificate exists and verifies exactly. It
does **not** show that a small-denominator triple exists at exactly `0.782267220134`: the
constraint rows carry `S^{−k}`, so pinning the density to 12 digits pins the denominators to
roughly `8^{11} ≈ 10^{10}` times whatever the free entries carry. The honest statement of the
reduction's status is: *same construction, same structural properties, `3.5·10⁻⁸` weaker,
3.8× smaller.*

**Comparison with the other certified objects** (the comparison the block asked for):
`C`'s `SOSQSIDE-005` carries a single explicit rational Gram (`Reviews/C_SOSQSIDE005.json`:
22 numeric entries, median 2 digits, max 19) at `1.413704545` — smaller entries, useless bound. `C`'s K33 certificates are `29`-digit
rationals at `0.779966500`, i.e. better bound and about 1.5× the entry size of `X_C017_small`;
but K33 needs a **sign predicate on neither side only because it has one side**, whereas `X_C017`
and `X_C017_small` are the only objects in the project with **both** sides witnessed by rational
PSD matrices — which is the property that removes the predicate obligation entirely (§3). The
`10`-digit `B` block of the stored certificate shows that the `B` side was always cheap; the size
was entirely a `G`/`A` artefact of the pivot solve.

---

## 3. A reader-facing verifier, and why no sign predicate is needed

`verify_XC017_readable.py` reloads a certificate from disk and prints, step by step, (1) symmetry,
(2) rational `LDL^T` with every pivot printed, (3) the identity `v^TAv + w v^TBv = Fourier(P)`
by expansion, (4) `P(0)`, `Q(0)`, the exact ratio and the density, (5) what is and is not claimed.
It runs on both `X_C017_certificate.json` and `X_C017_small.json` and exits 0 on both.

The exposition the block asked for is short: **CE1 and CE2 are not sign conditions here.** For
`H = v(s/S)^T G v(s/S)` with `G ⪰ 0`, `H ≥ 0` identically; `P = −(s−4)H` is then `≥ 0` on `[0,4]`
and `< 0` beyond `4` *because of the factor*, with no root isolation. For
`Q = v(w/S)^T A v(w/S) + w·v(w/S)^T B v(w/S)` with `A, B ⪰ 0`, `Q ≥ 0` on `[0,∞)` because both
summands are. The only remaining obligation is a polynomial **identity**, decided by expansion in
exact arithmetic. So the entire certificate is: three rational PSD tests (`LDL^T`) plus one
expansion. That is the whole reason the both-sides Gram form was worth the strength it costs —
and it is why `X_C017` is quoted as an *auditability* result, not as a bound. It is not a Kepler
proof and beats nothing: `0.782267 > 0.740480`.

The script prints that last sentence itself, because a verifier that returned "valid" for a
`0.782` density without saying so would invite exactly the misreading the block has twice had to
correct.

---

## 4. C's `cut_flow.py`: unchanged, so all four defects stand

`Computation/cut_flow.py` is blob `700e44f6c92563b66b4146106cfe8e00cd5a3455` at `4bcbd3a` **and**
at the current `comp` tip `790efa73` — Main's repair touched only the theorem, not the script. So
the four findings of `REVIEW_0353.md` §2 remain open on C's side, with the same exact numbers:
the `V_DOD` interval's lower endpoint is `3.86·10⁻¹²` too high; `build_13(2.1029)` returns 42 edges
instead of 12 (the true icosahedral edge at circumradius 2 is `2.102924448476534`, and phantom ring
edges make cuts cheaper in the unsafe direction); `build_fcc_patch(1)` raises `TypeError`; and the
period-16 13-cluster is unsaturated, so `b = −∞` and every cut is satisfied for every `Φ` — no
geometric content. W1–W6 in `REVIEW_0353.md` §3 remain the acceptance tests, with W6 restated as
in §1.1 above.

---

## 5. Ledger

| id | claim | status |
| --- | --- | --- |
| `X-C018` | The repaired `CUT_FLOW_THEOREM.md` (`aa52147`) is correct at all six points Main listed (directed model, cut orientation, demand satisfaction, Farkas+coarea, Theorem 2 without a uniform bound, threshold formula with both branches); no fifth defect found; 115 random instances agree across cut condition, LP and threshold formula. | **VERIFIED**, `Reviews/audit_cutflow_repair.py` exits 0 |
| `X-C019` | `X_C017_small.json` is a valid CE certificate at density `0.782267254856` (`2⁻²⁴` grid, ≤ 20-digit entries, 2,646 bytes), `3.5·10⁻⁸` below `X-C017` and 3.80× smaller; `L p = 0` exactly, `G, A, B ⪰ 0` by rational `LDL^T`. | **VERIFIED**, `verify_XC017_readable.py X_C017_small.json` exits 0 |
| `X-C020` | Erratum: `REVIEW_0353.md` §3 row W6 is wrong in both directions; correct verdict `t* = 2`, feasible iff `Φ ≥ 2`. The empty-boundary `0/0` case is *not* an obstruction when `Σ_U b = 0`. | **CORRECTION**, supersedes that row |
| `X-C021` | The height of `X_C017` is lcm blow-up of mutually coprime term denominators (each `≤ 17` digits, lcm `118` digits), not the pivot block; dyadic rounding at `S = 8` removes it. Coarser than `10⁻⁶` breaks `A`'s forced margin. | **VERIFIED** by the table in §2 |

## 6. Limits of this block

- The audit of Theorem 2 is a proof reading plus the hypothesis table; it is not machine-checked
  (there is no finite instance of an infinite theorem). What *is* machine-checked is Theorem 1
  and the threshold formula, on 115 randomised instances against an LP.
- The reduction is bounded, not optimal. I did not search for a different certificate at the same
  density with smaller height, because that is the "blind high-degree optimisation" the block was
  told not to spend its fallback on; and I did not run `m ≥ 6`, for the same reason.
- `X_C017_small` is a *different* certificate from `X_C017` (density `0.782267254856` vs
  `0.782267220134`). Both are in the tree; `verify_all.py` still checks the original, and the
  readable verifier checks either.

*Close timestamp (`date -u`, quoted from the shell immediately before the final push): filled in
below.*
