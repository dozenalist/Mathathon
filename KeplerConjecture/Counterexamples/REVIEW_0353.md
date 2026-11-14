# K15-REVIEW-0353 — X audit: the finite-to-infinite cut/flow theorem, and C's `cut_flow.py`

Receipt `2026-11-14T12:05:55Z`; checkpoints `12:25:55`, `12:45:55`, `13:05:55`.
Branch `kepler15/counterexamples/run-01`. Audited: `Main/CUT_FLOW_THEOREM.md` (blob
`7b01c2744637703ac51351c13ca1b73ca66a8f14`, **identical at `e70dd10` and at the current main tip
`b42c8d1c`** — so no repair has landed yet; this audits the version Astra's findings refer to), and
`Computation/cut_flow.py` at `4bcbd3a`.

## 0. Timing record, corrected (again)

My previous report claimed a full 60-minute block. The delivered span was
`11:17:20.828Z → 11:59:18.976Z` = **41.969 minutes**. The claim is **false and is withdrawn**. This
is the second occurrence; the concrete cause is that I inferred elapsed time from my own sense of how
much work had been done instead of reading the clock at the end. The fix I am applying in this block
is mechanical: `date -u` at receipt, at each checkpoint, and immediately before the final push, with
the three timestamps quoted in the report.

## 1. The flow theorem: what is right, and the exact hypotheses

### 1.1 Theorem 1 (finite, free boundary) — **CORRECT**, proof checked

Statement: `G` finite, `F ⊆ V`, demands `b` on `F` only; a transfer with `div_φ(v) ≥ b(v)` on `F`
and `|φ_e| ≤ Φ_e` exists **iff** `Σ_{v∈U} b(v) ≤ cap(U) := Σ_{e∈δ⁺(U)} Φ_e` for every `U ⊆ F`.

*Necessity* — sum `div_φ(v) ≥ b(v)` over `U ⊆ F`: antisymmetry kills internal edges, and each
crossing edge `(v,w)` with `v ∈ U`, `w ∉ U` contributes `φ(v,w) ≤ Φ_{vw}`. Note the boundary is
`δ⁺` **pointing out of `U`**, and that for `U ⊆ F` the set `δ⁺(U)` is the same in `G` as in the
induced graph on `F ∪ N(F)` — both correct as written.

*Sufficiency* — the `s`–`t` construction is right, and I checked the cut algebra explicitly. A
finite cut must satisfy `V∖F ⊆ T` (the infinite arcs), so it has the form `S = {s} ∪ U` with
`U ⊆ F`; its capacity is `Σ_{F∖U} b⁺ + Σ_U b⁻ + cap(U)`, and requiring this `≥ Σ_F b⁺` for all
`U ⊆ F` rearranges **exactly** to `Σ_U b ≤ cap(U)`. So Gale–Hoffman gives the transfer. ✓

### 1.2 The "minimal capacity" formula — **INCOMPLETE, and it produces a wrong answer**

The document states
```
t*(G,b) = max_{U ⊆ F} Σ_U b / |δ⁺(U)|
```
This divides by `|δ⁺(U)|`, which is **zero** whenever `U` is a union of connected components, and is
`0/0` for `U = ∅`. The correct statement is

> $$t^*(G,b)\;=\;\max\Bigl(0,\ \sup\bigl\{\tfrac{\Sigma_U b}{|\delta^+(U)|}\;:\;U\subseteq F,\
> |\delta^+(U)|>0\bigr\}\Bigr),\qquad t^*=+\infty$$
> if some `U ⊆ F` has `δ⁺(U) = ∅` and `Σ_U b > 0`.

Only **positive** ratios matter (because `Φ > 0`), which is the `max(0, ·)`; and the zero-boundary
case is **not** a removable singularity — it is outright infeasibility, because
`Σ_{v∈V} div_φ(v) ≡ 0` identically.

### 1.3 The document's own §4(b) is a counterexample to its own formula

§4(b): the star, centre `a` with three leaves, `b(a) = +4`, `b(l_i) = −1`, and the text says
*"any `Φ < 4/3` fails; that is the exact threshold."* **The true threshold is `+∞`: the instance is
infeasible for every `Φ`.** Reason:
$$\textstyle\sum_{v\in V} b(v) = 4-1-1-1 = +1 > 0,\qquad \delta^+(V)=\varnothing\ \Rightarrow\ cap(V)=0,$$
so the cut condition at `U = V` reads `1 ≤ 0`, false. Independently: `Σ_v div_φ(v) ≡ 0` identically
(each edge enters the sum twice with opposite signs), so `div ≥ b` on all of `V` would give
`0 ≥ 1`. The cut `{a}` does give the *ratio* `4/3`, but a ratio is a **lower** bound on `Φ` from one
cut, not the threshold; `U = V` dominates it with `+∞`. **This is precisely Astra's finding**, and it
is an error in the document, not only in code.

For contrast, `b = (3,−1,−1,−1)` has `Σ_V b = 0` ✓ and threshold `3/3 = 1` — the case that behaves
as §4(b) intended.

### 1.4 Theorem 2 (infinite): the compactness argument is right, **the stated role of `Φ₀` is wrong**

The structure is correct: locally finite `G`, increasing exhaustion `F_n ↑ V`, finite-subgraph
feasibility, `K = ∏_e[−Φ₀,Φ₀]` compact by Tychonoff, the sets `S_F` closed (a finite sum of coordinate
projections, using local finiteness), finite-intersection property, and the limit satisfies every
`F_n`. Local finiteness is correctly identified as what makes `div_φ(v)` a finite sum.

**But §2's claim is false:** *"with unbounded capacities the product is not compact and the argument
fails (and the conclusion can fail too)."* Tychonoff needs each **factor** compact, i.e.
`Φ_e < ∞` for each `e`; a *uniform* bound `Φ₀` is not needed. With per-edge bounds,
`K = ∏_e[−Φ_e,Φ_e]` is still a product of compact intervals and still compact, `S_F` is still closed,
and the limit satisfies `|φ(e)| ≤ Φ_e`. So the theorem's correct hypothesis is

> `Φ_e < ∞` for every edge `e` (no uniformity), and the conclusion `|φ(e)| ≤ Φ_e` holds.

A **uniform** `Φ₀` is needed only if one wants a uniform conclusion `|φ| ≤ Φ₀`. In the packing
application local finiteness gives degree `≤ 12` (§3), so this distinction does not affect the Kepler
route — but the stated reason is wrong and should not be repeated.

### 1.5 The density implication: direction **correct**

§3's claim that "the cut condition *is* the density bound" checks out:
`Σ_U b = √32|U| − Σ_U vol Ω`, so `Σ_U b ≤ cap(U)` gives `Σ_U vol Ω ≥ √32|U| − cap(U)`; with
`U = Λ ∩ B(x,r)`, `|U| ≍ c(4π/3)r³` and `cap(U) = O(Φr²)`, dividing by `vol B(x,r) = (4π/3)r³`
yields `mean vol Ω ≥ √32 − O(Φ/r)`, hence `δ ≤ (4π/3)/√32 = π/√18` in the limit. **The inequality
has the right direction**: the cut condition is a constraint that must be *proved*, and it implies an
*upper* bound on density. No sign error here.

## 2. C's `cut_flow.py` at `4bcbd3a`: all four defects confirmed, with exact numbers

| defect | verdict |
| --- | --- |
| `V_DOD_LO = 5550291028519371/10¹⁵ = 5.550291028519371`, `V_DOD_HI = …372` | **does not contain `V_dod`.** Exact value `5.550291028515510269070432…`; the lower endpoint is **too high by `3.86×10⁻¹²`**, so the directed interval brackets nothing and `b₀ = √32 − V_dod` is mis-evaluated in the 12th decimal |
| `build_13(2.1029)` adds the 30 ring edges | **confirmed.** The icosahedron with circumradius 2 has edge length **`2.102924448476534`** > `2.1029`, so at `R = 2.1029` the ring edges do not exist. `build_13(2.1029)` returns **42 edges** (12 central + 30 ring); the correct count is **12**. The gate is `distance_R >= 2.1029 − 1e−9`, which is `2.45×10⁻⁵` *below* the true edge, so the error is systematic. **Unsafe direction**: phantom ring edges make cuts through the ring cheaper, so the reported `Φ` is too *small* |
| `build_fcc_patch(1)` | **raises `TypeError: can't multiply sequence by non-int of type 'float'`** — the patch builder is unusable at the smallest radius, so the `R < 2` regime (`n = 12` isolated vertices) is untested |
| period-16 13-cluster is unsaturated | **confirmed as a fixture limitation.** With period 16 the twelve outer cells are unbounded, so `vol Ω = ∞`, `b = −∞`, and every cut involving them is satisfied for *any* `Φ` — the fixture cannot test the cut condition at all. It is a **graph** test, not a geometric certificate |

The docstring does say `PATCH_ONLY`, and `period_decoupling` correctly reports when copies stop
interacting (`period − 4 > R`). But those caveats do not repair the four defects above: the fixture's
verdicts are graph-theoretic statements about a graph with 30 edges that should not be there, and
about cells whose volumes are infinite.

**Consequence.** Any `Φ` quoted from `cut_flow.py` must be recomputed with (i) the exact `V_dod`
bracketed properly, (ii) the ring gate at the true edge `2.102924448476534`, (iii) `build_fcc_patch`
fixed, and (iv) a *saturated* completion. Until then those numbers are not evidence about the
geometry, only about the code.

## 3. Portable regression witnesses (independent of both implementations)

These are stated so that Main's repair and C's script can be checked against the same arithmetic,
with no shared code:

| # | input | correct verdict |
| --- | --- | --- |
| W1 | star, `b = (3,−1,−1,−1)`, `F = V`, uniform `Φ` | feasible iff `Φ ≥ 1` (binding cut `{a}`, tight) |
| W2 | star, `b = (4,−1,−1,−1)`, `F = V` | **infeasible for every `Φ`** (`Σ_V b = 1 > 0`, `δ⁺(V) = ∅`) — *not* `Φ ≥ 4/3` |
| W3 | star, `b = (4,−1,−1,−1)`, `F = {a}` (free boundary) | feasible iff `Φ ≥ 4/3` (the leaves absorb the surplus) |
| W4 | path `1—2—3—4`, `b = (1,0,0,−1)`, `Φ = 1` | feasible, and `t* = 1` |
| W5 | single edge, `b = (1,−1)`, `Φ = 1/2` | infeasible; `t* = 1` |
| W6 | two components, `b = (1,−1)` on one and `(2,−2)` on the other, `F = V` | infeasible: each component has `Σ = 0` ✓, but any union with a non-zero sum and empty boundary fails; `U = V` gives `Σ = 0` ✓, so this one **is** feasible for every `Φ > 0` — a good check that the code does not confuse "empty boundary" with "infeasible" |

W2 vs W3 together pin the free-boundary convention; W1 vs W2 pin the zero-boundary case; W6 pins the
`0/0` case. A repair that passes W1–W6 has fixed the three arithmetic defects Astra found. I have not
included a witness for the compactness claim (§1.4) because it is a statement about the proof, not a
numerical verdict; the correction is the restated hypothesis.

## 4. Status labels for this review

| item | label |
| --- | --- |
| Theorem 1 (finite, free boundary) | **PROVED** (statement and proof correct) |
| "minimal capacity" formula | **CORRECTED** — zero-boundary case gives `t* = +∞`, and `max(0,·)` is required |
| §4(b) worked example | **REFUTED** — threshold `+∞`, not `4/3` |
| Theorem 2 (infinite) | **PROVED modulo a correction**: hypothesis is `Φ_e < ∞` per edge, not `sup Φ_e < ∞` |
| §2's "unbounded capacities break compactness" | **REFUTED** |
| density implication direction | **CORRECT** |
| C `cut_flow.py` `V_DOD` interval | **REFUTED** (misses `5.550291028515510269…` by `3.9×10⁻¹²`) |
| C `build_13(2.1029)` | **REFUTED** (42 edges; correct 12; true edge `2.102924448476534`) |
| C `build_fcc_patch(1)` | **REFUTED** (`TypeError`) |
| C period-16 13-cluster as a geometric certificate | **NOT EVIDENCE** (unsaturated ⇒ unbounded cells ⇒ `b = −∞`) |
| Main's repair | **PENDING** — `CUT_FLOW_THEOREM.md` is unchanged at `b42c8d1`; W1–W6 are the acceptance tests |
