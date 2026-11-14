# A finite-to-infinite cut/flow theorem for the signed deficits

Block `K15-REVIEW-0308-M-CONTINUE`, task 2; **repaired at `K15-REVIEW-0353-M-EVIDENCE`**
after review. Four defects in the first version are corrected and named in §6; the first
version's proofs are retained there as rejected evidence, per the ledger convention.

## 0. Convention (fixed)

`G = (V,E)` is an undirected graph, **locally finite** (every vertex has finite degree).
`b : V → R` is the *deficit* — **signed**, so `b` may be negative anywhere — and demands
are imposed only on a set `F ⊆ V`. `Φ : E → [0,∞)` is the *capacity*, **non-negative**;
here `E` is a set of unordered pairs, and `Φ_e ≥ 0` for every `e`.

A **transfer** is an antisymmetric `φ : V×V → R` with `φ(v,w) = 0` unless `{v,w} ∈ E` and

```
|φ(v,w)| ≤ Φ_{vw}        for every edge {v,w},
```

together with `φ(w,v) = −φ(v,w)`. Its **divergence** is `div_φ(v) := Σ_{w ∈ N(v)} φ(v,w)`,
a finite sum by local finiteness.

The **cut** of `U ⊆ V` is `δ⁺(U) := {{v,w} ∈ E : v ∈ U, w ∉ U}` and `cap(U) :=
Σ_{e ∈ δ⁺(U)} Φ_e`, an empty sum when `δ⁺(U) = ∅`. **Note `δ⁺(U) = ∅ ⟹ cap(U) = 0`**;
that case is the source of one of the repaired defects (§6.2).

*This is the project's convention*: in `K15-C044`, `b(v) = √32 − vol Ω(v)`, `Φ` uniform,
and the demand is `div_φ(v) ≥ b(v)` — the inequality is `≥` and the deficit is signed.

## 1. Finite theorem, with a free boundary

> **Theorem 1.** Let `F ⊆ V` be finite (so `E(F)`, the set of edges with an endpoint in
> `F`, is finite by local finiteness) and let `b` be given on `F` only. Then a transfer
> with `div_φ(v) ≥ b(v)` for all `v ∈ F` exists **iff**

> for every `U ⊆ F`:  `Σ_{v∈U} b(v) ≤ cap(U)`.  **(C)**

**Proof of (⟹).** Sum `div_φ ≥ b` over `U`:

```
Σ_{v∈U} b(v) ≤ Σ_{v∈U} div_φ(v) = Σ_{v∈U} Σ_{w∈N(v)} φ(v,w) = Σ_{e={v,w} ∈ δ⁺(U)} ±φ_e ,
```

because every edge with both endpoints in `U` is counted twice with opposite signs and
cancels by antisymmetry. Each surviving term is at most `Φ_e` in absolute value, so the
sum is at most `cap(U)`. ∎

**Proof of (⟸), first proof (network flow; the reviewer's §6.1 correction applied).**
Build a directed network.

- vertices `V ∪ {s,t}`;
- **for each edge `{v,w} ∈ E`, two arcs `v→w` and `w→v`, each of capacity `Φ_{vw}`** — both
  directions, each with the *full* capacity, not a shared one;
- for `v ∈ F`: arc `s→v` of capacity `b(v)⁺ := max(b(v),0)` and arc `v→t` of capacity
  `b(v)⁻ := max(−b(v),0)`;
- for `w ∈ V∖F`: arc `w→t` of capacity `∞`.

A **cut** is `S ∋ s`, `T = V∖S ∪ {t} ∋ t`; write `U := S ∩ F` and `X := S ∖ F`.

*Which cuts can be finite?* If `X ≠ ∅` then for `w ∈ X` the arc `w→t` crosses `S → T`, and
its capacity is infinite; so **every cut of finite capacity has `X = ∅`**, i.e. all
vertices outside `F` lie on the **sink** side. (The first version of this file had this
reversed, writing "the infinite arcs make `X ⊇ N(U)∖F` optimal"; the correct statement is
`X = ∅`, forced. See §6.1.)

For `X = ∅` the capacity of the cut is

```
Σ_{v∈F∖U} b(v)⁺  +  Σ_{v∈U} b(v)⁻  +  Σ_{e ∈ δ⁺(U)} Φ_e
   =  Σ_F b⁺  −  Σ_U b  +  cap(U).
```

By max-flow/min-cut, a flow of value `Σ_F b⁺` exists iff this is `≥ Σ_F b⁺` for every
`U ⊆ F`, i.e. iff **(C)** holds.

*From the flow to the transfer.* Let `f` be such a flow. Define

```
ψ(v,w) := f(v→w) − f(w→v)        for {v,w} ∈ E,
```

i.e. the **net** of the two opposite arcs; `ψ` is antisymmetric by construction, and
`|ψ(v,w)| ≤ max(f(v→w), f(w→v)) ≤ Φ_{vw}` because both terms are non-negative, so `ψ` is a
transfer. Conversely every transfer arises this way (`f(v→w) = φ(v,w)⁺`,
`f(w→v) = φ(v,w)⁻`), so the two models have the same achievable divergence vectors.

*Divergence.* Conservation at `v ∈ F` reads `a_v − c_v = div_ψ(v)`, where `a_v ≤ b(v)⁺` is
the flow on `s→v` and `c_v ≤ b(v)⁻` that on `v→t`. Since the total flow is `Σ_F b⁺` and
`Σ_v a_v ≤ Σ_F b⁺`, every `a_v` is saturated: `a_v = b(v)⁺`. Hence

```
b(v) > 0 :  div_ψ(v) = b(v) − c_v = b(v)      (c_v ≤ b(v)⁻ = 0)
b(v) ≤ 0 :  div_ψ(v) = −c_v ≥ −b(v)⁻ = b(v)
```

so `div_ψ ≥ b` on `F` in every case. ∎

**Proof of (⟸), second proof (duality + coarea; independent of the gadget).** The system
`{Aφ ≥ b, |φ_e| ≤ Φ_e}` on `E(F)` is infeasible iff (Farkas, keeping the multipliers `z±`
of the box) there is `y ≥ 0` on `F`, extended by `0` off `F`, with

```
Σ_{v∈F} y_v b(v)  >  Σ_{e={v,w}} Φ_e |y_v − y_w|.            (∗)
```

For `t ≥ 0` put `U_t := {v ∈ F : y_v > t} ⊆ F`. Two coarea identities hold because
`y ≥ 0`:

```
Σ_{v∈F} y_v b(v) = ∫_0^∞ (Σ_{U_t} b) dt ,     Σ_e Φ_e|y_v − y_w| = ∫_0^∞ cap(U_t) dt .
```

(The second is `|y_v − y_w| = ∫_0^∞ |1[y_v>t] − 1[y_w>t]| dt`, and an edge crosses `U_t`
exactly when the two indicators differ.) So `(∗)` forces `Σ_{U_t} b > cap(U_t)` for some
`t`, contradicting **(C)**. ∎

**The two proofs are genuinely different** — the first is constructive and gives an
algorithm, the second gives the exact dual and is the one that extends to signed
capacities (where the box multipliers matter).

**Threshold formula (corrected; see §6.2).** For a **uniform** capacity `Φ ≥ 0`, putting
`|δ⁺(U)|` for the number of crossing edges,

```
t*(G,b)  =  +∞                                   if some U ⊆ F has δ⁺(U) = ∅ and Σ_U b > 0,
         =  max( 0 , sup_{U⊆F, δ⁺(U)≠∅} Σ_U b / |δ⁺(U)| )     otherwise.
```

Two things are being handled: the **empty-boundary case cannot be divided by zero** and is
an obstruction at *every* capacity — it is exactly the "closed component" condition of
`K15-C080`/`C095`, and it is capacity-free; and the `max(0, ·)` is needed because the
minimal uniform capacity is required to be non-negative even when every cut has
`Σ_U b < 0` (then `Φ = 0` works, i.e. `φ ≡ 0`).

## 2. Infinite theorem

> **Theorem 2.** Let `G` be locally finite, `{F_n}` an increasing exhaustion of `V` with each
> `F_n` finite, and suppose `(C)` holds for every finite `U ⊆ V`. Then a transfer exists
> with `|φ(v,w)| ≤ Φ_{vw}` for every edge — **with no hypothesis that the capacities are
> bounded above**.

*Proof.* For each `n`, apply Theorem 1 to the induced subgraph on `F_n ∪ N(F_n)` with
demands on `F_n`; that graph is finite (locally finite, `F_n` finite) and the hypothesis
gives its cut condition, since for `U ⊆ F_n` the set `δ⁺(U)` computed in `G` equals the one
computed in `F_n ∪ N(F_n)` — every neighbour of `U` lies in `N(F_n)`. So there is a
transfer `φ_n` with `div ≥ b` on `F_n`.

Each `φ_n` lies in `K := ∏_{e∈E} [−Φ_e, Φ_e]`. **Each factor is a compact interval, so `K`
is compact by Tychonoff — no uniform bound on `Φ` is needed** (the first version assumed
`sup_e Φ_e = Φ₀ < ∞` and used `∏[−Φ₀,Φ₀]`; see §6.3). For finite `F`, the set

```
S_F := { φ ∈ K : div_φ(v) ≥ b(v) for every v ∈ F }
```

is closed in `K`: `div_φ(v)` is a *finite* sum of coordinates of `φ` (local finiteness), so
it is continuous in the product topology, and `S_F` is an intersection of closed
conditions. `S_{F_n} ≠ ∅` for every `n`, so by the finite intersection property
`⋂_n S_{F_n} ≠ ∅`; any element of the intersection is a transfer satisfying the demand on
`⋃_n F_n = V`. ∎

**Where each hypothesis is used, exactly.**

| hypothesis | used for |
| --- | --- |
| local finiteness | `div_φ(v)` a finite sum, hence continuous — *only* here |
| `Φ_e ≥ 0` | the intervals `[−Φ_e,Φ_e]` non-degenerate, and `cap(U) = 0` for empty cuts |
| `Φ_e < ∞` per edge | the factor is compact |
| `sup_e Φ_e < ∞` | **not used** (§6.3) |
| `F_n` finite, exhaustion | Theorem 1 applies at each `n`, and `⋃F_n = V` |

Tychonoff needs no degree bound; bounded degree is *not* the mechanism (this corrects the
sentence in `K15-C067` that conflated compactness with bounded degree).

## 3. Existence versus geometry

Theorems 1–2 are **pure graph theory**: a transfer exists iff the cut inequalities hold,
and they are insensitive to where `b` came from. Everything geometric sits in *verifying*
`(C)`:

- on fcc/hcp, `b ≡ 0`, so `(C)` holds with `Φ = 0` (`K15-C078`);
- on **every** Barlow packing `b ≡ 0` too (`K15-C094`), so `(C)` holds with `Φ = 0` there —
  and every cut is *tight*, so no slack argument can prove `(C)` (`K15-C094` corollary);
- on the crack packings (`K15-C095`) `b ≤ 0` with `b < 0` at the crack faces, so `(C)`
  holds with `Φ = 0` as well: **a void never binds**;
- on a packing containing the isolated 13-cluster, `b(v₀) ≥ 0.1065632` and the singleton cut
  forces `Φ ≥ 0.008880268414417` (`K15-C081r`, `C-DECOUPLE-001`);
- for large ball cuts, `Σ_U b = (4π/3)r³(√32 c − 1) + O(r²)` while `cap(U) = O(Φ r²)`, so
  `(C)` for large balls *is* the density bound (`K15-C087`);
- and a **bounded** component with `δ⁺(C) = ∅` needs `Σ_C b ≤ 0` outright (`K15-C080`,
  `K15-C095` — *bounded* is essential; infinite closed components exist and are harmless).

## 4. The density implication is one-directional (reviewer's §6.4)

`K15-C087` proves: `(C)` for all finite `U` in a saturated `Λ`, with a uniform `Φ`,
**implies** `δ(Λ) ≤ π/√18`. It does **not** prove, and nothing available does, the
converse — a density bound carries no local cut information. So:

- `(C)` is **at least as strong as** Kepler, not a weakening of it;
- the cut form is a *reorganisation* of the proof (negligibility for free, `K15-C035`),
  whose price is that the geometric content reappears at full strength;
- there is **no equivalence** between `(C)` and the density statement, and none between
  `(C)` and `(T')` in either direction beyond `(T') ⟹ (C)`.

## 5. Worked signed examples (repaired)

**(a) Feasible, with the exact dual witness.** `G` = a centre `a` with three leaves
`l₁,l₂,l₃`; `b(a) = +1`, `b(l_i) = −1/3`; uniform `Φ = 1`. Note `Σ_F b = 0`, so the
whole-set cut is not an obstruction (`Σ_F b = 0 ≤ cap(F) = 0`). Cuts: `{a}` gives `1/3`;
`{a,l_i}` gives `(1−1/3)/2 = 1/3`; `{l_i}` and `{l_i,l_j}` are negative. So `t* = 1/3`,
attained at `{a}`. **Transfer:** `φ(a,l_i) = 1/3`, `φ = 0` elsewhere; `div_φ(a) = 1 = b(a)`
and `div_φ(l_i) = −1/3 = b(l_i)` — equality everywhere, so `{a}` is tight and is the dual
witness.

**(b) Infeasible at *every* capacity (replaces the first version's "threshold 4/3").**
Same graph, `b(a) = +4`, `b(l_i) = −1`. Then `Σ_F b = 4 − 3 = 1 > 0` while `δ⁺(F) = ∅`
(every neighbour of `F` lies in `F`), so `cap(F) = 0` and the whole-set cut fails for
**every** `Φ ≥ 0` — there is no threshold. The first version called `4/3` "the exact
threshold", which was wrong twice over: it checked only the cut `{a}` (which gives `4/3`)
and never checked `U = F`. The lesson is the general one: **`Σ_U b ≤ 0` for every
empty-boundary `U` is a necessary condition independent of the capacity**, and in a finite
graph with `F = V` it reduces to `Σ_v b(v) ≤ 0`.

**(b′) The genuine threshold example.** Same graph, `b(a) = +4`, `b(l_i) = −4/3`; now
`Σ_F b = 0`. Cuts: `{a}` gives `4/3`; `{a,l_i}` gives `(4−4/3)/2 = 4/3`;
`{a,l_i,l_j}` gives `(4−8/3)/3 = 4/9`; the rest are negative. So `t* = 4/3` and the
threshold *is* `4/3` — for this deficit vector, which is what the first version should have
written.

**(c) A signed case where the deficit and surplus must be routed two hops.** Path
`1—2—3—4`, `b = (+1,0,0,−1)`, `Φ = 1`; `Σ_F b = 0`. Cuts: `{1}` gives `1`; `{1,2}` gives
`1`; `{1,2,3}` gives `1`; so `t* = 1`. Transfer `φ(1,2) = φ(2,3) = φ(3,4) = 1`:
`div(1) = 1`, `div(2) = div(3) = 0`, `div(4) = −1` ✓. The binding cuts are the three
prefixes — the flow is unique here, which is why every prefix is tight.

## 6. The four defects in the first version (rejected text, and the repair)

**6.1 The cut orientation was reversed.** Rejected text: *"Writing a cut as `U ∪ X` with
`U ⊆ F` and `X ⊆ V∖F` and minimising over `X` (the infinite arcs make `X ⊇ N(U)∖F`
optimal) gives exactly `Σ_U b ≤ cap(U)`."* Wrong: an outside vertex `w` on the **source**
side puts the infinite arc `w→t` across the cut, so finite cuts have `X = ∅` — the outside
vertices are forced onto the **sink** side, and the minimisation over `X` is vacuous, not
an optimisation. The conclusion was right; the mechanism was inverted. Repaired in §1, with
both directed arcs written out and the netting `ψ = f(v→w) − f(w→v)` stated.

**6.2 The threshold formula divided by a zero boundary.** Rejected text: *"`t*(G,b) =
max_{U ⊆ F} Σ_U b/|δ⁺(U)|`"*, and *"the variant `b(a) = 4` is infeasible at `Φ = 1` with the
violating cut `{a}` … that is the exact threshold `4/3`."* Both wrong: the formula is
undefined when `δ⁺(U) = ∅`, and that case is an obstruction at *every* capacity, not at
some threshold; accordingly `b = (4,−1,−1,−1)` is infeasible for all `Φ`, and `4/3` is not
its threshold. Repaired in §1 (threshold formula) and §5(b)/(b′).

**6.3 The compactness argument assumed a uniform bound.** Rejected text: *"Each `φ_n` lies
in `K := ∏_{e∈E}[−Φ₀,Φ₀]`, compact by Tychonoff"*, with the hypothesis `sup_e Φ_e = Φ₀ < ∞`
and a paragraph "Where `Φ₀ < ∞` is used". The hypothesis is unnecessary: a product of
compact intervals `∏_e[−Φ_e,Φ_e]` is compact by Tychonoff whatever the `Φ_e` are. Repaired
in §2; `sup Φ < ∞` is removed from the statement.

**6.4 The density implication was presented as if it settled the strength.** Rejected
phrasing: the file left "the cut condition is the theorem" as a one-line remark, which reads
as an equivalence. Repaired in §4: the implication is one-directional, and `(C)` is at
least as strong as Kepler.
