# A finite-to-infinite cut/flow theorem for the signed deficits

Block `K15-REVIEW-0308-M-CONTINUE`, task 2. Written to be self-contained: the
inequality convention is fixed once, every finite subsystem is justified, and the
geometric input is separated from the graph-theoretic existence question.

## 0. Convention (fixed)

`G = (V,E)` is an undirected graph, possibly infinite, **locally finite** (every
vertex has finite degree). `b : V → R` is the *deficit*, `Φ : E → (0,∞)` the
*capacity*. A **transfer** is an antisymmetric `φ : V×V → R` with `φ(v,w) = 0` unless
`{v,w} ∈ E` and `|φ(v,w)| ≤ Φ_{vw}`. Its **divergence** is
`div_φ(v) := Σ_{w ∈ N(v)} φ(v,w)` (a finite sum by local finiteness).
The **cut** of `U ⊆ V` is `δ⁺(U) := {{v,w} ∈ E : v ∈ U, w ∉ U}`, and we write
`cap(U) := Σ_{e ∈ δ⁺(U)} Φ_e`.

*This is the convention used throughout the project*: in `K15-C044`, `b(v) = √32 − vol Ω(v)`,
`Φ` uniform, and the demand is `div_φ(v) ≥ b(v)` — the inequality is `≥` and the
deficit is signed, so `b` may be negative anywhere.

## 1. Finite theorem (with a free boundary)

> **Theorem 1.** Let `G` be finite, `F ⊆ V`, and demands `b` given only on `F`
> (no constraint elsewhere). Then a transfer with `div_φ(v) ≥ b(v)` for `v ∈ F`
> exists **iff** for every `U ⊆ F`: `Σ_{v∈U} b(v) ≤ cap(U)`.

*Proof.* (⟹) Sum `div_φ ≥ b` over `U ⊆ F`: internal edges cancel by antisymmetry,
crossing edges contribute at most their capacities. Note `δ⁺(U)` in `G` is the same
as in the graph induced by `F ∪ N(F)` when `U ⊆ F`, since every neighbour of `U` lies
in `N(F)`.
(⟸) Add a sink `t` and, for each `w ∉ F`, an arc `w → t` of infinite capacity; add a
source `s` with arcs `s → v` of capacity `b(v)⁺` and arcs `v → t` of capacity
`b(v)⁻` for `v ∈ F`. Gale–Hoffman (equivalently max-flow/min-cut) says a flow of value
`Σ_{v∈F} b(v)⁺` exists iff every cut separating `s` from `t` has capacity at least
that value. Writing a cut as `U ∪ X` with `U ⊆ F` and `X ⊆ V∖F` and minimising over
`X` (the infinite arcs make `X ⊇ N(U)∖F` optimal) gives exactly
`Σ_U b ≤ cap(U)`. The resulting flow's restriction to `E` is the transfer. ∎

**Consequence (uniform capacity).** If `Φ_e ≡ Φ` then
`t*(G,b) = max_{U ⊆ F} Σ_U b / |δ⁺(U)|`
(with `|δ⁺(U)|` the number of crossing edges) is the minimal capacity, and it is
attained at some cut (finitely many cuts when `G` is finite).

## 2. Infinite theorem (compactness, with the finite subsystems justified)

> **Theorem 2.** Let `G` be locally finite and `{F_n}` an increasing exhaustion of `V`
> with each `F_n` finite. Suppose that for every finite `U ⊆ V`,
> `Σ_{v∈U} b(v) ≤ cap(U)`, and that `sup_e Φ_e = Φ₀ < ∞`. Then a transfer exists with
> `|φ| ≤ Φ₀`.

*Proof.* For each `n`, apply Theorem 1 on the finite graph induced by `F_n ∪ N(F_n)`
with demands on `F_n`; the hypothesis gives its cut condition, so there is a transfer
`φ_n` with `|φ_n| ≤ Φ₀` satisfying the divergence on `F_n`. Each `φ_n` lies in
`K := ∏_{e∈E} [−Φ₀, Φ₀]`, compact by Tychonoff. The sets
`S_F := {φ ∈ K : div_φ(v) ≥ b(v) for all v ∈ F}` are closed, and `S_{F_n} ≠ ∅` for
every `n`, so by the finite intersection property `⋂_n S_{F_n} ≠ ∅`. Any element of
the intersection is a transfer. ∎

**Where local finiteness is used.** Tychonoff needs no degree bound; the *passage of
the divergence inequality to the limit* does, because `div_φ(v)` is an infinite sum
when `deg(v) = ∞`. So: **compactness alone gives a "transfer" whose divergence is only
defined where degrees are finite**; the packing application has degree `≤ 12`
(`K15-C054`), so the theorem applies as stated.

**Where `Φ₀ < ∞` is used.** `K` must be compact; with unbounded capacities the product
is not compact and the argument fails (and the conclusion can fail too).

## 3. Existence versus geometry (the point of the separation)

Theorems 1–2 are **pure graph theory**: they say a transfer exists iff the cut
inequalities hold, and they are insensitive to where `b` came from. Everything
geometric sits in *verifying* `Σ_U b ≤ cap(U)`:

- on fcc/hcp, `b ≡ 0`, so the condition holds with `Φ = 0` (`K15-C078`);
- on a packing containing the isolated 13-cluster, `b(v₀) ≥ 0.1065632` and the
  singleton cut forces `Φ ≥ 0.0088803` (`K15-C081r`) — a *witness-specific* floor, not
  a universal one: the per-packing bound is `Φ ≥ max_v b(v)/deg(v)`;
- for large ball cuts, `Σ_U b = (4π/3)r³(√32 c − 1) + O(r²)` while `cap(U) = O(Φ r²)`,
  so the cut condition *is* the density bound (`K15-C087`);
- and a **closed** component (`δ⁺(C) = ∅`) needs `Σ_C b ≤ 0` outright (`K15-C080`).

So the graph theory contributes existence-from-cuts; the geometry contributes cuts.

## 4. Worked signed examples

**(a) Feasible, with the exact dual witness.** `G` = a centre `a` with three leaves
`l₁,l₂,l₃`; `b(a) = +1`, `b(l_i) = −1/3`; uniform `Φ = 1`.
Cuts: `{a}` gives `1/3`; any `{l_i}` gives `−1/3 ÷ 1 < 0`; `{a,l_i}` gives
`(1 − 1/3)/2 = 1/3`; `{l_i,l_j}` gives `−2/3 ÷ 2 < 0`; all others are ≤ `1/3`. So
`t* = 1/3`, attained at `{a}`. **Transfer**: `φ(a,l_i) = 1/3` for each `i`, `φ = 0`
elsewhere. Then `div_φ(a) = 1 = b(a)` ✓ and `div_φ(l_i) = −1/3 = b(l_i)` ✓ — equality
everywhere, so the cut `{a}` is *tight* and is the dual witness (the LP dual of the
max-flow is a cut, and here it is a singleton).

**(b) Infeasible, with the violating cut.** Same graph, `b(a) = +4`, `b(l_i) = −1`.
The cut `{a}` gives `4/3 > 1`, so no transfer with `Φ = 1` exists. (Any `Φ < 4/3`
fails; that is the exact threshold.)

**(c) A signed case where the deficit and surplus must be routed two hops.** Path
`1—2—3—4`, `b = (+1, 0, 0, −1)`, `Φ = 1`: cuts `{1}` give `1`; `{1,2}` give `1/1 = 1`;
`{1,2,3}` give `1/1 = 1`; so `t* = 1`. Transfer: `φ(1,2) = φ(2,3) = φ(3,4) = 1`
(`div(1) = 1`, `div(2) = 0`, `div(3) = 0`, `div(4) = −1` ✓). The binding cuts are the
three prefixes — the flow is unique here, which is why every prefix is tight.
