# Next geometric package: a uniform bound on the transfer cost `Φ`

Block `K15-REVIEW-0308-M`. This is the bounded package for the next geometric block.
It replaces "prove the cut condition" by a *quantitative* statement with an explicit
constant, which is the only form in which the target is both open and falsifiable.

## 1. The object

For a saturated packing `Λ` and range `R ≤ 2.09`, let `b(v) = √32 − vol Ω(v)` and

```
t*(Λ)  :=  max over finite U ⊆ Λ of   Σ_{v∈U} b(v) / |δ⁺_R(U)|,
```

the minimal `Φ` for which a transfer exists (LP duality: min-max over flows and cuts,
`K15-C044`). **The package is:**

> **Target.** Find an explicit `Φ₀ = Φ₀(R)` with `t*(Λ) ≤ Φ₀` for every saturated
> packing `Λ` and every `R ≤ 2.09`.

Why this form:

- **Kepler's truth does not trivialise it.** `K15-C087` shows the cut condition for
  *large balls* is the density theorem, so a *proof* of the target would imply Kepler —
  but the target is an inequality with a constant, not a proof of Kepler, and it is
  exactly the statement the transfer machinery needs (`K15-C035`, Lemma 3.3's rate
  `O(Φ/r)`).
- **It is falsifiable, in two ways.** (a) A single periodic packing with `t* > Φ₀`
  refutes a claimed `Φ₀`; `C-TRANSFER-001` computes `t*`, so candidates can be attacked
  directly. (b) **A packing with a closed component of positive deficit refutes the
  route outright**: such a component has `|δ⁺| = 0` and `Σ_C b > 0`, so `t* = ∞` and no
  transfer exists. By `K15-C080` that case is exactly E's `(T')`. Settling whether a
  saturated packing can have such a component is the **first** obligation; a single
  example closes the transfer route (though not Kepler).
- **It has a proved floor.** `t* ≥ 0.0088803` at `R = 2.09` on any packing containing
  the 13-cluster (`K15-C081r`, singleton cut). So `Φ₀ ≥ 0.0088803`, and a candidate
  below that is refuted outright.

## 2. What is already known, and where the difficulty sits

| fact | source |
| --- | --- |
| negligibility is free for a transfer: `C₁ = 3ΦR(R+1)⁵` | `C035` |
| feasibility ⟺ the cut condition (Hoffman), compactness needs degree `≤ 12` | `C044`, `C067` |
| degree `≤ 12` holds at `R ≤ 2.09` | `C054` |
| `t* = 0` on fcc and hcp | `C078` |
| `t* ≥ 0.0088803` for any packing containing the 13-cluster | `C081r` |
| ball cuts have `|δ⁺| ≤ 3k_R R r²`; general `U` only `k_R|U|` | `C079` |
| the naive local `φ` overshoots and fails | `C085` |

The difficulty is a *trade-off between two scales*: small `U` give small denominators
`|δ⁺(U)|` but `Σ_U b` is controlled only by `√32|U|`; large `U` control `Σ_U b` by the
density theorem but the boundary grows like `|U|^{2/3}`. A proof of the target must
interpolate between them; nobody has tried.

## 3. The concrete steps

0. **Settle the closed-component case** (`E-COMPONENT-001`): exhibit a saturated
   packing with a closed component of positive deficit, or prove none exists. Everything
   below is conditional on this.
1. **Compute `t*` for every periodic packing anyone can build** (`C-CUT-001`). The
   value on fcc/hcp is `0`; on a vacancy, a defect pair, and a stacking fault the
   answer is unknown and cheap to get. The maximum over those is a lower bound for
   `Φ₀` and tells the team what `Φ₀` has to accommodate.
2. **Prove the target for ball cuts only** — that is a self-contained inequality about
   Voronoi volumes over balls, with the explicit boundary `3k_RRr²`, and it uses only
   the density theorem *plus* a stability estimate for the deficit inside a ball.
   This is the natural intermediate milestone and it has no existing proof either.
3. **Interpolate**: given (2), show that the maximum in `t*` is attained (up to a
   constant) on ball-like cuts. This is the step where the combinatorial content
   lives, and it is where the closed-component case of `K15-C080` must be handled.

## 4. Acceptance

A block succeeds if it delivers (1) with at least four non-trivial periodic packings,
or (2) with an explicit constant, or a *refutation* of a claimed `Φ₀`. A block that
only re-derives that the cut condition is equivalent to Kepler has not succeeded
(`K15-C087` already settles that).
