# Audit and repair: the trace-limit route to `(W3)` at `k = 6`, in `S_1`

Supersedes the previous version of this file. Grades: **[P]** paper-level argument written here with
explicit hypotheses; **[A]** arithmetic, machine-checked (`checks/onehot_limit.py`, output appended
to `supervisor_checks.out`); **[S]** source-checked at cited Lean lines; **[C]** cited, not re-verified.

## 0. RETRACTIONS (banner — read before anything below)

| # | retracted claim | why it is wrong |
|---|---|---|
| R1 | "the set of a.e.-defined measurable maps into a finite set is compact for convergence in measure" | **False.** On a nonatomic probability space, independent Rademacher-type one-hot fields are pairwise at a fixed positive distance (L² distance `1`, L⁰ distance `1/2`) and have no Cauchy subsequence [A, §3]. Closed and bounded in `L⁰` is not compact. |
| R2 | **Proposition 4** and its conclusion "`[6] \ (V ∪ V') != empty` at an accumulation point; 20 of 400 ordered label pairs excluded" | Rested entirely on R1. **Withdrawn**, with the label counts. No excluded-pair statement survives. |
| R3 | "a limit of one-hot fields need not be one-hot, so singleton palettes do not pass to the limit" | **False for strong `L²` limits**: coordinates of a one-hot field are indicator functions, and a strong `L²` limit of indicators is an indicator. See §4, which also shows this makes the route *impossible*, not merely blocked. |
| R4 | the 12-sector countermodel "`b_n(s) = 3 + ((s+n) mod 3)`" as a weak limit / as a witness of non-compactness | Its Cesàro average is uniform but the sequence itself has no weak limit (period 3), and it has 3 distinct members so a constant subsequence exists. It witnesses only that the *convex hull* of the one-hot fields contains non-one-hot elements. Replaced by the Rademacher example [A]. |
| R5 | "force `b_inf` to take three values on positive-measure sets ⟹ `|P_p| >= 3`" | **Category error**: `P_p(e)` is the support of the traces *at the single direction `e`*. A field taking three labels on different direction sets is still, at each `e`, one label, so the palette there has cardinality `1`. |
| R6 | "`(A1)` must be weakened to a.e. centre, because Lean's `ae_typicalSampling` is a.e.-in-`y`" | Half right, half wrong, and the correction matters. The per-centre endpoint trace is **available at every centre**, but by an argument that is *not* the Lean a.e. statement: the non-typical set is plane-null and the circle is an isometry of angular measure. Grade **[P]**, not [S]. See §2. |

Nothing below claims that "a whole family of methods is exhausted". §5 states one narrow closure and
says exactly what it closes.

## 1. Source-level audit of the objects (new in this version)

Read from `lean/OAI/Geometry/PlaneColoring/{Compactness,Palettes}.lean`:

* **[S]** `Typical z := DensityOne {w | c w = c z} z`;
  `TypicalSampling c y r := 0 < r ∧ ∀ᵐ t ∂angularMeasure, Typical c (y + (r:ℂ)*direction t)`
  (Compactness.lean:83-86).
* **[S]** `ae_typicalSampling c hc (hr : 0 < r) : ∀ᵐ y ∂volume, TypicalSampling c y r`
  (Compactness.lean:87-96) — an **a.e.-in-centre** statement at fixed radius. This is *not* the form
  the accumulation argument needs, and it is not what licenses a prescribed centre.
* **[S]** `sampleCode c hc y r` is the `TraceVector k` of `L²` classes `t ↦ [c(y + r·direction t) = i]`
  (Compactness.lean:255); `sampleSet := {(y,r,b) | TypicalSampling c y r ∧ b = sampleCode c hc y r}`
  (l.259); **`IsTrace c hc x b := (x,1,b) ∈ closure (sampleSet)`** (l.261). So the trace relation is
  closure at **radius exactly 1**, in the *norm* topology of `TraceVector k`.
* **[S]** `trace_realization` (l.262): `IsTrace x b` gives centres `y n → x`, radii `r n → 1`, all
  `TypicalSampling c (y n) (r n)`, with `sampleCode (y n) (r n) → b` in norm.
* **[S]** `trace_limit` (l.289): traces pass to limits jointly in centre and trace — if
  `IsTrace (x n) (b n)`, `x n → y`, `b n → a` in norm, then `IsTrace y a`. `isCompact_traces` (l.286)
  is trivial (fixed centre, bounded finite-dimensional trace vector).
* **[S]** `trace_bounds` (l.297) is proved from **weak** limits only (`traceCode_tendsto_iff`,
  `weak_limit_nonneg`, `weak_limit_le_one`, `weak_limit_sum`): the containment of a trace's positive
  coordinates in the palette is a weak-limit statement. Consequence: the *palette* is a weak object,
  while `IsTrace` membership is a strong one. Both facts are used below.
* **[S]** `paletteSet x i := ⋃_{b ∈ paletteGenerators x i} tracePositive x i b`, `palette x t` its
  finset; `tracePositive_le_palette` gives `{t | 0 < traceValue b i t} ⊆ paletteSet x i` a.e.

## 2. What is licensed at a prescribed centre (repairs R6)

**Prop. 0 [P].** For **every** `x` and a.e. `e ∈ S`, `c(x+e) ∈ P_x(e)`.

*Proof.* Let `N = {z : z not Typical}`. By Lemma 4.3 of the paper, `N` is plane-null. The map
`e ↦ x + e` is an isometry from `S` with angular measure onto the circle `x + S`, so
`{e : x + e ∈ N}` is angular-null; hence `x + e` is typical for a.e. `e`, i.e.
`TypicalSampling c x 1` holds, so `(x,1,sampleCode c x 1) ∈ sampleSet` and its code is a trace at
`x`. The code at direction `e` is one-hot with the label `c(x+e)`, so
`traceValue b i e > 0` exactly when `c(x+e) = i`, and by `tracePositive_le_palette`
`i ∈ P_x(e)` for a.e. `e` on that set. Union over the finitely many `i`. `square`

**Grade discipline.** This is the same argument as `m10`'s Lemma 1 (`[C]`), and it is **[P]**: the
Lean development has `ae_typicalSampling` (a.e. *centre*), **not** the per-centre statement, which
needs the paper's "`N` is plane-null" plus absolute continuity of the circle map. So the endpoint
trace at a *prescribed* centre is available; the a.e.-typicity in Lean is a different statement and
must not be cited for it.

## 3. The obstruction: no compactness, and none can be manufactured (repairs R1, R4)

**Prop. 1 [A].** The set of one-hot `T`-valued fields on `(S, sigma)` is **not** compact for
convergence in `L²` nor in measure. Witness: on `Ω = {0,1}^ℕ` with product measure, let
`u_k = e_1` on `{ω_k = 0}` and `e_2` otherwise. Then `‖u_k - u_l‖²_{L²} = 2·P(ω_k != ω_l) = 1` for
all `k != l`, and `P(‖u_k - u_l‖ >= 1) = 1/2`; no Cauchy subsequence exists.

*Checked exactly on the finite model `{0,1}³` (all three pairs, `P = 1/2`, `‖·‖² = 1`), and stated
for the infinite product.* The same construction with `T` replaced by any finite set of size `>= 2`
applies verbatim; it is the standard example that `L⁰`-bounded does not imply `L⁰`-compact on a
nonatomic space.

**Consequence.** The step "pass to a strongly convergent subsequence of the singleton fields
`b_{x_n}`" is not available, and no theorem in the record supplies it. This is the *one* source-level
gap: an **admissibility-and-compactness lemma for the prescribed sequence `(x_n, 1)`**, which would
have to say that the codes `sampleCode c x_n 1` have a norm-convergent subsequence. Prop. 0 gives the
admissibility half; Prop. 1 shows the compactness half is false as an abstract statement about
one-hot fields, so such a lemma, if true for trace codes, must use the *specific* geometry of the
`x_n` (they are triangle centres with a common label set) and cannot be deduced from measurability.

## 4. Second, independent obstruction: even granted compactness, the route yields nothing (repairs R3, R5)

**Prop. 2 [P].** In `S_1`, at every centre `x`, every trace `b ∈ W_x` is one-hot a.e.; and any norm
limit of one-hot fields is one-hot.

*Proof.* If `b_i(e) > 0` and `b_j(e) > 0` with `i != j` on a set of positive angular measure, then both
`i, j ∈ P_x(e)` there (`tracePositive_le_palette`), contradicting `|P_x(e)| = 1` a.e. With
`sum_i b_i = 1` a.e. (`trace_bounds`) `b` is one-hot a.e. For the second part, coordinates of a one-hot
field are indicator functions; a strongly `L²`-convergent sequence of indicators converges a.e. along
a subsequence, and `{0,1}` is closed, so the limit is an indicator; coordinatewise limits of a
partition form a partition. `square`

**Corollary (the narrow closure of §5).** In `S_1` the conclusion "`|P_p(e)| >= 3` at the
accumulation point" **cannot** be obtained from trace limits: the limit object is again one-hot, and
one-hot means `|P_p(e)| = 1`, which is what `S_1` already assumes. So the accumulation-limit argument
is not merely blocked by a missing compactness lemma — it is incapable of producing the needed value
count. This closes **the trace-limit route to `(W3)`**, and nothing else.

## 5. What survives, with its own hypothesis checked

**Prop. A [P] (kept; conditional complement-triple claim).** Let `c` be a weak measurable 6-colouring
in `S_1`. Let `x` be a centre whose `Γ_x` contains a triangle with label set `V`, `|V| = 3`, and put
`T = [6] \ V`. Then `c(x+e) ∈ T` for a.e. `e ∈ S`, and `P_x(e) = {c(x+e)}` a.e.

*Proof.* `S_1` gives `P_x(e) = {b_x(e)}` a.e.; Lemma 6.2 on the three edges of the triangle forbids a
singleton inside an edge, so `b_x(e) ∉ V` a.e.; Prop. 0 (endpoint trace at the *prescribed* centre,
which is what makes this legal at every triangle centre, not just a.e. one) gives
`c(x+e) ∈ P_x(e) = {b_x(e)}`. `square`

Sharpness [C]+[A]: `m3`'s proper measurable `k >= 7` colouring has `V = {0,2,3}`,
`T = {1,4,5,6}`, `|T| = k - 3 = 4`, and its gadget lies within `~0.0071` of `p_0` while the unit
circle about `q_n` stays `>= 0.993` from `p_0`, so the circle carries exactly `T`. Prop. A holds there
with equality.

**What Prop. A does not give.** No finiteness, no separation, no excluded label pair. `V = V'` at an
accumulation point is untouched by it, and no attack on `(W3)` follows from it alone.

## 6. G1 and G2, still separate

**(G1)** `(W)`/`(W3)`: finitely many cyclic (triangle) centres in one ball of radius `> 1` — open; this
block reduces the reachable machinery, it does not advance the truth of `(W3)`.
**(G2)** §8 at `k = 6`: with `(W)` granted, Prop. 7.1 yields `ell ∈ {3,4,5,6}` and the printed §8
excludes `ell ∈ {3,4,5}` only at `k = 5`; the strip layer is SAT for every `k >= 6` and `ell`. Open,
untouched here. Neither gap alone bounds `chi(R^2)`; `6 <= chi(R^2) <= 7` unchanged.

## 7. Files

| file | content |
|---|---|
| this file | retraction banner, source audit, Prop. 0, Prop. 1 (Rademacher), Prop. 2, Prop. A |
| `checks/onehot_limit.py` | [A] sections [13]-[14]: Rademacher distances, admissibility bookkeeping |
| `CORRECTED-DEPENDENCY-MAP.md`, `LEMMA-isolation-window.md` | unchanged; their W/W2 material is independent of this file |
