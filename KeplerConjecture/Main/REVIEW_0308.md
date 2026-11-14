# Review 0308 — the `Φ` floor withdrawn, the bridge quantified, the target re-read

Block `K15-REVIEW-0308-M`. Receipt `2026-11-14T11:13:20Z`. Reviewed tip
`7c56c5ee4a2fb515a35c6f7734bfd06adf63b2f5`.

## 1. The objection is correct: `K15-C081` is withdrawn

`C081` derived `Σ_C b ≤ 13(√32 − V_dod)` — an **upper** bound on the 13-cluster's
signed deficit — and used it as a **lower** bound to force `Φ|δ⁺(C)| ≥ Σ_C b`. Invalid:
if the thirteen cells average *larger* than `√32` then `Σ_C b < 0` and the cut
condition holds with `Φ = 0`. Nothing bounds that deficit from below, and the claim
that all thirteen cells attain `V_dod` was never proved.

**Replaced by `K15-C081r`, the singleton cut**, which *is* valid and needs only
monotonicity (no Hales–McLaughlin): `Ω(v₀) ⊆` the dodecahedron determined by the
twelve neighbours, so `vol Ω(v₀) ≤ V_dod`, hence `b(v₀) ≥ √32 − V_dod = 0.1065632`
and

```
Φ ≥ (√32 − V_dod)/12 = 0.0088803…      at R = 2.09.
```

The withdrawn `0.0104949` and its "refuted outright" rule are removed from CLAIMS,
RESULTS, REVIEW_0223, ACCEPTED, TASKS and NEXT_PACKAGE; the rejected text is kept.

## 2. `K15-C079`'s boundary estimate needed a ball, not a blob

The `|U|^{2/3}` slack was justified by "`U` contains a ball of radius `r`", which does
not control an arbitrary cut's boundary (a comb-shaped `U` has `|∂U| ≍ |U|`). Corrected:
for **ball cuts** `U = B(x,r) ∩ Λ`, `|δ⁺(U)| ≤ k_R((r+R)³ − r³) ≈ 3k_RRr²` and the
`|U|^{2/3}` form holds; for general `U` the only bound is `k_R|U|`, which is **not**
`o(|U|)`. The `|U|^{2/3}` averaged inequality is therefore a *hypothesis about
ball-like cuts*, not a consequence of the cut condition.

## 3. And the cut condition is not a weaker target at all (`C087`)

For a large ball, `Σ_U b = (4π/3)r³(√32·c − 1) + O(r²)` while `Φ|δ⁺(U)| = O(r²)`, so
the cut condition reads `c ≤ 1/√32 + O(1/r)` — the Kepler bound. `C080`'s "weaker than
`(T')`" holds only for *small* components. This is the precise form of `C071`'s trade:
the transfer packaging buys negligibility (`C035`) but the geometric content returns at
full strength, so **no future block should pursue the cut condition as though it were
easier than Kepler**.

## 4. The density bridge, quantified (`C083`)

Deleting the two-unit slabs leaves the inner cube of side `S − 4`, so the kept volume
fraction is `(1 − 4/S)³ ≥ 1 − 12/S`: the bridge's `O(1/S)` is correct **with constant
12**, and the construction was checked numerically on fcc (`S = 6, R = 40` gives
`δ = 0.0194` against `0.7405`) — vacuous below `S ≈ 12`, correct as `S → ∞` with
`R/S → ∞`. So the bridge is qualitative only, which is all its use requires.

## 5. The remaining lemma against Hales and the literature (`C084`, `C085`)

`Main/REMAINING_LEMMA.md` states the cut condition exactly and compares it with Hales'
accounting: score on Delaunay stars, an exact rearrangement (his four-way
cancellation), and a pointwise inequality over a **finite** list of tame types. The
cut condition has the same shape but its quantifier is not finitised — harder to verify
mechanically, and (by §3) not weaker as a statement. No published source proves a cut
form; the pointwise chain Rogers `5.372754` → Muder `5.41848` → Hales–McLaughlin
`5.550291` cannot reach `√32` because `V_dod` is pointwise optimal.

The one cheap hope — an explicit local transfer `φ(v,w) = ψ(v−w)(b(v)−b(w))` — was
**tested and refuted** (`C085`): the requirement becomes `(s−1)b(v) ≥ (ψ*b)(v)`, which
fails on a three-line defect model at exactly the vertices that must fund the deficit
(the formula overshoots). A genuine min-cut flow has no expected closed local form.

## 6. Worker sources integrated (`C086`), and the routing plan

C `9d9ff68` (explicit-Gram states: p-side `1.3398`, Fourier `1.3713`, both-sides
`2.0017`; control only), E `9a46efc` (`E1` target, `E2` blocked on a 3-point
evaluator, `E3` obstructed), X `6535e76` (three certified CE bounds `0.8181`,
`0.7948`, `0.7807`; `X-C014` awaiting the local check). **X's 23-test audit of Main's
checker is superseded**: it audited revision `9461aae`, at which the supervisor's local
reproduction found three false accepts — the third instance of a battery passing on an
unsound revision. Generic checker soundness stays suspended; only `X-CHECK-001` at the
pushed revision, plus a soundness *argument*, can lift it.

`Main/ROUTING_0308.md` assigns: C a bounded cut/flow solver (`C-CUT-001`, with
`fcc/hcp → t* = 0` and `b > 0 → t* ≥ 0.0088803` as acceptance tests); E validated
geometric fixtures with the all-pairs separation check and the closed-component
question; X the checker audit and the two implications (`C080`, `C081r`).

## 7. State

No new bound. The geometric route is one open statement (`C044`'s cut condition), which
by `C087` is equivalent to the theorem; its only proved necessary condition is
`Φ ≥ 0.0088803`; its negligibility half is proved (`C035`); and no finite completion
can verify it (`C036`). The analytic route is frozen at degree 33.
