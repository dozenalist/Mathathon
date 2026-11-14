# Trace-consistency at six colours is the six-colouring problem

**m15, swarm smwfwi7rh, direction d14.** A theorem package with exact certificates.

The headline is a five-line theorem (§4): **the paper's own trace relation, together with its
sixty-degree exclusion (5.7), already forces a proper colouring.** Everything the sprint calls
"trace-consistency" is therefore not a technical gap that one more estimate could close — it is
Hadwiger–Nelson's upper bound. §5 turns that into a one-line obstruction that kills every palette
countermodel in the sprint, certified exactly in `verify.py`.

---

## 0. Results

1. **Theorem A (support inequality).** For a weak measurable `k`-colouring, the palette is contained
   in the support field: `P_x(e) ⊆ F(x + e)` for a.e. `e`, where `F(q) = {i : q ∈ H_i}` and `H_i` is
   the closed spatial essential support of `A_i`. This is the only relation between palettes and
   supports that the paper uses, and the reverse inclusion is *not* available without a density
   hypothesis (Remark A.2).
2. **Theorem B (hitting condition).** The trace relation `(T)  c(x+e) ∈ P_x(e)` — printed in §5.1 of
   the paper — implies that for a.e. `y` the palettes at the unit circle around `y`, pointing at
   `y`, have nonempty intersection: `∩_{x ∈ S¹(y)} P_x(y − x) ∋ c(y)`.
3. **Theorem C (the wall).** `(T)` plus `(5.7)` already force `c` to be a.e. proper, hence
   `χ(R²) ≤ k`. Conversely every weak measurable `k`-colouring satisfies both. So
   **trace-consistency + (5.7) ⟺ `χ(R²) ≤ k`**, and at `k = 6` the frontier is exactly the
   six-colouring problem. The proof is the rotation identity `|1 − R| = 1`: every unit pair `(y,y')`
   is `(x+Re, x+e)` for a suitable centre `x`, so the two palettes `P_x(Re)` and `P_x(e)` — which
   (5.7) makes disjoint — both contain `c(y)` resp. `c(y')`.
4. **Corollary C1.** Any palette field whose unit-circle intersections are empty somewhere (in
   particular *any centre-independent field*, and any field graded by a scale that does not change
   at unit distance) is **not** the palette field of any colouring — one line, and certified for all
   five countermodel families of the sprint in `verify.py` section B.
5. **Corollary C2 (selection form).** If `F : R² → 2^{[k]}` is measurable, nonempty-valued and
   `F(u) ∩ F(v) = ∅` for a.e. unit pair, then every measurable selection `c(q) ∈ F(q)` is a weak
   measurable `k`-colouring. So **such an `F` exists ⟺ `χ(R²) ≤ k`** — the "point-field" special
   case of Theorem C, stated because it is the cleanest finite object to search over.
6. **Theorem D (homogeneity obstruction).** No centre-independent field satisfies
   `(5.7)` + nonemptiness + the hitting condition; and no centre-independent field satisfies
   `(5.7)` + nonemptiness + the point-field identity. Explicit witnesses for the sprint's five
   countermodel families (§5).
7. **Theorem E (redundancy).** Given the point-field identity, the paper's transport axioms (5.2)
   and (5.3) are consequences of (5.7). So the palette axiom system has exactly one non-redundant
   structural axiom, and it is the one equivalent to colouring existence.
8. **Theorem F (support form at k = 6, conditional on non-degeneracy).** At `k = 6` at most three
   supports contain any given point and no support contains a unit pair, so a 6-colouring is a cover
   of the plane by six closed unit-pair-free sets with concurrency at most three.
9. Two corrections: a gap in the "heavy direction" hint of m11 (§8.1) and the rigorous death of my
   own direction d14, scale gluing (§8.2).

---

## 1. Conventions (the paper's, unchanged)

`k ≥ 3`; `c : R² → [k]` is a weak measurable `k`-colouring (paper, Definition 1.2) with Borel
representatives `A_i = c^{-1}(i)` forming a partition, `a_i = 1_{A_i}`. `S = S¹` with normalised
arc length `σ`; `R` = rotation of directions by `κ = π/3`.

* `P_x(e)` is the maximal palette of Definition 5.1: the weak-* limits of angular samples
  `e ↦ (a_i(y_n + r_n e))` with `y_n → x`, `r_n → 1` through typical circle samplings, and the
  essential union over those traces.
* `H_i = {q : |A_i ∩ B(q,r)| > 0 for every r > 0}` is the closed spatial essential support (§5.1).
* `Γ_x` is the transition graph (Definition 6.1); `L = {x : Γ_x contains a cycle}` (6.4).

Printed facts used, with their exact hypotheses:

* **(5.7)** (Corollary 5.4): at every centre `x`, `P_x(e) ∩ P_x(Re) = ∅` for `σ`-a.e. `e`.
* **(T)** (Definition 5.1 with constant sequences, plus the countability paragraph of §5.1, which
  states that every individual trace has its positive coordinates in the palette almost everywhere):
  `c(x + e) ∈ P_x(e)` for `dx ⊗ σ`-a.e. `(x,e)`. Explicitly: for a.e. `x` the constant sampling
  `(y_n, r_n) = (x, 1)` is a typical circle sampling, hence a trace in `W_x`, whose positive
  coordinates lie in the palette a.e. This is the same step the paper uses in the proof of
  Proposition 5.6 ("the actual sampling at center `x + e`, radius exactly one, is itself a trace").
* **Palette bound** (`results/K6-BARRIER.md` §1, Proposition): `1 ≤ |P_x(e)| ≤ k − 3` a.e.; at
  `k = 6`, `|P_x(e)| ≤ 3`.

Nothing below uses Proposition 5.6, Theorem 6.5 or Proposition 7.1. The only geometry used is
`R − 1 = exp(2πi/3)`, `|R − 1| = |1 − R| = 1`, and that `e ↦ (R−1)e`, `e ↦ (1−R)e` are rotations of
`S`; all three are checked in exact arithmetic in `verify.py` section A.

---

## 2. Theorem A — palettes are contained in the support field

> **Theorem A.** Let `c` be a weak measurable `k`-colouring. Then for every centre `x` and `σ`-a.e.
> `e`, `P_x(e) ⊆ F(x + e)`, where `F(q) := {i : q ∈ H_i}`.

*Proof.* Let `i ∈ P_x(e)`. By Definition 5.1, `e` lies in the essential union of the sets
`{b_i > 0}` over the traces `b ∈ W_x`, and by the countability paragraph of §5.1 that union may be
taken over countably many traces; so for a.e. such `e` there is `b ∈ W_x` with `b_i(e) > 0`. Fix an
arc `J ∋ e`. If `liminf_n ∫_J a_i(y_n + r_n e') dσ(e') = 0` along the samplings realizing `b`, then
along a subsequence the integrals tend to `0`, hence `∫_J b_i dσ = 0`, contradicting `b_i(e) > 0` for
`J` small. So for infinitely many `n` the arc `{y_n + r_n e' : e' ∈ J}` meets `A_i` in positive
angular measure, hence in positive length; those points tend to `x+e` as `n → ∞` and `J ↓ {e}`. As
`J` was arbitrary, `A_i` has positive Lebesgue measure in every ball around `x + e`: `x + e ∈ H_i`.
∎

*Remark A.1 (why the paper needs no more).* The paper uses exactly this direction: in the proof of
Proposition 5.6 the exact circle sample at `x+e` is a trace at the centre `x+e`, whose positive
coordinates lie in the palette; in Definition 6.1's remark, `ij ∈ Γ_x ⟹ x ∈ H_i ∩ H_j`.

*Remark A.2 (the reverse inclusion needs a density hypothesis, and we never use it).* The reverse
implication "`q ∈ H_i` ⟹ `i ∈ P_x(q−x)`" is a statement about arcs of radius one through `q`, and
it holds when the class does not become degenerate at `q`, e.g. under
`limsup_{ρ→0} |A_i ∩ B(q,ρ)|/ρ² > 0` (average the arc fraction over the placements
`(y,r) ∈ B(x,ρ) × (1−ρ,1+ρ)`: its mean is comparable to that density, and `ρ` can be matched to the
arc width). It can fail at a Lebesgue-theoretic cusp of `H_i`, and nothing in this note depends on
it. In particular Theorem A is an inclusion, not an identity, and I flag that the "point field"
statements below are stated for fields satisfying the identity as an *axiom*.

---

## 3. Theorem B — the hitting condition

> **Theorem B.** For `dx ⊗ σ`-a.e. `(x,e)`, `c(x+e) ∈ P_x(e)`. Consequently, for a.e. `y`,
> ```
>      c(y) ∈ ∩_{x ∈ S¹(y)} P_x(y − x)      (intersection over arclength-a.e. x),
> ```
> so in particular that intersection is nonempty. Call this **(HIT)**.

*Proof.* The first sentence is (T). For the second: fix `y`. The pairs `(x, y−x)` with
`x ∈ S¹(y)` form a smooth embedded circle in `R² × S`; the exceptional set of (T) is null in the
product, so by Fubini it meets that circle in an arclength-null set. Hence `c(y) ∈ P_x(y−x)` for a.e.
`x ∈ S¹(y)`. ∎

`(HIT)` is a *necessary* condition on the palette field of a colouring, and it is the exact place
where every countermodel in this sprint fails (§5, Theorem D and `verify.py` section B).

---

## 4. Theorem C — the wall

> **Theorem C.** Let `c : R² → [k]` be measurable and let `P` be any field satisfying (T) and (5.7).
> Then `c(u) ≠ c(v)` for a.e. unit pair `(u,v)`; hence `c` is a weak measurable `k`-colouring and
> `χ(R²) ≤ k`.

*Proof.* Let `(y, y')` be a unit pair and `w = y' − y`. Because `|1 − R| = 1`, the vector
`e := w/(1 − R)` is a unit vector, and `x := y − Re` is a centre with
```
     y = x + Re,        y' = y + w = x + Re + (1−R)e = x + e.
```
By (T) at the centre `x` in the directions `Re` and `e`,
```
     c(y) = c(x + Re) ∈ P_x(Re),        c(y') = c(x + e) ∈ P_x(e),
```
and by (5.7) the two palettes are disjoint. Hence `c(y) ≠ c(y')`. The map
`(x,e) ↦ (x + Re, x + e)` is a measure-preserving bijection of `R² × S` onto the unit-pair manifold
(`e ↦ Re − e = (R−1)e` is a rotation of `S`, and `du = dx`), and the (T)-exceptional set is a null
set, so the exclusion holds for a.e. unit pair. ∎

> **Corollary C0.** `(T)` + `(5.7)` for some palette field ⟺ there is a weak measurable
> `k`-colouring ⟺ (paper, Theorem 1.3) `χ(R²) ≤ k`.

The `⟸` direction is the paper: every weak measurable colouring satisfies (5.7) (Corollary 5.4) and
(T) (§5.1).

> **Corollary C1.** A field `P` satisfying (5.7) and *failing* (HIT) on a set of `y` of positive
> measure is not the palette field of any weak measurable `k`-colouring.

*Proof.* Immediate from Theorem B. ∎

> **Corollary C2 (selection form).** Let `F : R² → 2^{[k]}` be measurable with `F(q) ≠ ∅` a.e. and
> `F(u) ∩ F(v) = ∅` for a.e. unit pair. Then every measurable selection `c(q) ∈ F(q)` is a weak
> measurable `k`-colouring, so `χ(R²) ≤ k`. Conversely a `k`-colouring gives `F(q) = {c(q)}`. Hence
> ```
>     a nonempty-valued measurable unit-disjoint F : R² → 2^{[k]} exists  ⟺  χ(R²) ≤ k.
> ```

*Proof.* For each `i`, the set of unit pairs with both endpoints of colour `i` is contained in
`{(u,v) : i ∈ F(u) ∩ F(v)}`, which is null. ∎

**What Theorem C settles.** "Trace-consistency with a proper colouring" — the condition the sprint
identifies as the frontier — is *not* an extra technical hypothesis sitting between the palette
axioms and the truth. Together with the paper's own (5.7) it is equivalent to the existence of a
6-colouring. Consequently:

* no argument using palette axioms (5.2), (5.3), (5.7), (6.2), the palette bound, self-avoidance,
  the two-centre bound or the density bound, *plus trace-consistency*, can prove (W) at `k = 6`
  without proving `χ(R²) ≥ 7`;
* conversely, a `k = 6` countermodel must be a genuine 6-colouring with non-locally-finite `L`, and
  no palette-level object can be it;
* the boundary is sharp in both directions, because the countermodels of Theorem C / FREE-LABEL
  satisfy every palette axiom and fail exactly (HIT) — see §5 and `verify.py` section B.

---

## 5. Theorem D — the homogeneity obstruction, with exact certificates

> **Theorem D.** Let `P_x(e) = Q(e)` be a centre-independent field (in particular any
> translation-invariant one) with nonempty values. Then for every `y`,
> `∩_{x ∈ S¹(y)} P_x(y−x) = ∩_{e ∈ S} Q(e) = ∅` as soon as `Q(e) ∩ Q(Re) = ∅` for a.e. `e`. Hence no
> centre-independent field satisfies (5.7) + nonemptiness + (HIT), and none is the palette field of
> any colouring.
>
> More generally, let `P_x(e) = Q(σ(x), e)` and suppose that on a set `G` of centres of positive
> measure the type `σ` is the same for a.e. point of every unit circle `S¹(y)`, `y ∈ G`. Then (5.7)
> + nonemptiness + (HIT) fail on `G`.

*Proof.* For a centre-independent field, `P_x(y−x) = Q(y−x)` and `y−x` runs over all of `S` as `x`
does, so the intersection is `∩_e Q(e)`, which is empty because `Q(e)` and `Q(Re)` are disjoint and
nonempty. For the general case, on `S¹(y)` with `y ∈ G` the type is the single value `s(y)`, so the
intersection is `∩_e Q(s(y), e) = ∅` by the same argument. ∎

Theorem D is verified exactly, model by model, in `verify.py` section B: for each of

| model | sectors | values | witness that the intersection is empty |
|---|---|---|---|
| m15 three-block, `ℓ = 3` | 36 | `{3},{4},{5}` | `{3} ∩ {4} = ∅` |
| m15 three-block, `ℓ = 4` | 36 | `{0,2},{1,3},{4}` | `{0,2} ∩ {1,3} = ∅` |
| m15 three-block, `ℓ = 5` | 36 | `{0,2},{1,3},{5}` | `{0,2} ∩ {1,3} = ∅` |
| free-label word, `ℓ = 6` | 36 | six values | total intersection `∅` |
| m13 singleton | 9 | `{4},{5},{6}` | `{4} ∩ {5} = ∅` |

the script re-checks that the field satisfies the palette axioms it is claimed to satisfy — (5.7) at
every direction, the palette bound, `C_ℓ`-admissibility, the free label, and for `ℓ = 6` disjointness
at all six transport offsets `±5, ±6, ±7` — and that the total intersection of its values is empty,
which is exactly the failure of (HIT) at every centre.

**Consequence.** No centre-independent, sector-valued, or "graded by a quantity that does not change
at unit distance" field can be a colouring's palette field, independently of any colouring question.
This is a stronger statement than the sprint's "the countermodels fail self-avoidance": the
free-label models *do* satisfy non-proper self-avoidance, and they still die here.

---

## 6. Theorem E (redundancy) and Theorem F (support form)

> **Theorem E.** Let `P` be a *point field*, `P_x(e) = F(x+e)`, with nonempty values, satisfying
> (5.7). Then the paper's palette transfer (5.2) and smooth transport (5.3) hold.

*Proof.* (5.2) asks for `c(x+e+v) ∉ P_x(e) ∪ P_x(v)`. With the point field, `P_x(e) = F(x+e)`,
`P_x(v) = F(x+v)`, and `c(x+e+v) ∈ F(x+e+v)` by (T)+Theorem A; and
`|(x+e+v)−(x+e)| = |v| = 1`, `|(x+e+v)−(x+v)| = |e| = 1`. Since (5.7) becomes
`F(u) ∩ F(v) = ∅` for a.e. unit pair (the change of variables `(x,e) ↦ (x+e, x+Re)` of Theorem C is
measure preserving), the two exclusions follow. (5.3) asks for `P_z(f) ∩ P_x(s(f)) = ∅` whenever
`z + f = x + s(f) + t(f)` with `|s| = |t| = 1`; with the point field this is
`F(z+f) ∩ F(x+s) = ∅`, and `|(z+f) − (x+s)| = |t| = 1`. ∎

So of `(5.7)`, `(5.2)`, `(5.3)`, the palette bound and `(6.2)`, the first three collapse to **one**
once the point-field identity is imposed. The countermodels are not countermodels to the axiom
system; they are countermodels to the missing structural identity (or, equivalently by §4, to (T)).

> **Theorem F** (needs the reverse inclusion of Remark A.2, i.e. non-degeneracy of the relevant
> class densities; it is not used anywhere else in this note). For a weak measurable 6-colouring with
> non-degenerate classes, `|F(q)| ≤ 3` for a.e. `q`, and no `H_i` contains a unit pair. Hence the six
> supports form a cover of the plane by closed unit-pair-free sets of concurrency at most three.

*Sketch.* `|F(q)| = |P_x(q−x)| ≤ 3` by Remark A.2 and the palette bound; the second statement is
`P_x(e) ∩ P_x(Re) = ∅` read through the identity. ∎

---

## 7. What remains at `k = 6`, and non-vacuity

```
  palette axioms alone                : satisfiable, accumulating, every ℓ   (sprint Thm C, FREE-LABEL)
  palette axioms + (T) (trace)        : equivalent to χ(R²) ≤ 6             (Theorem C)
  (W) at k = 6 fails                  : ⟸ a 6-colouring with non-locally-finite L exists [trivial]
                                        ⟹ any countermodel is a weak measurable 6-colouring whose
                                          palette field satisfies (T)+(5.7), hence χ(R²) ≤ 6
                                          [Theorem C]
```

So a proof of (W) at `k = 6` must be an argument about 6-colourings (Theorem A, the palette bound,
the paper's §5 machinery, Theorem D's (HIT) are all available); it cannot come from any further
palette axiom, and a `k = 6` countermodel must be a genuine 6-colouring.

**Non-vacuity.**

* `k ≥ 7`: the hexagonal 7-colouring (paper §1) gives `F(q) = {c(q)}` nonempty and unit-disjoint
  (Corollary C2's hypothesis), and m3's alteration `.ultramath/smwfo9zkl/m3/` keeps it proper with
  accumulating `L`. So the criterion is satisfiable at the first `k` where it can be.
* `k = 6`, finite: `verify.py` section C decides the Corollary C2 system on the Moser spindle in
  exact coordinates `Q(√3,√11)`: **UNSAT at `k = 3`** (this is 4-chromaticity) and **SAT at `k = 6`**
  with an explicit witness. So the point-field system is locally consistent at `k = 6`, as it must be
  if `χ(R²) ∈ {6,7}`.
* `k = 6`, cyclic structure: `verify.py` section D decides the wheel `W₆` (a centre and its six unit
  neighbours): the six-cycle palette structure at the hub is consistent with the point field + (5.7)
  + (6.2) at `k = 6`, with witness `rim = {0,2},{1,3},{0,2},{1,3},{0,2},{1,3}`, `hub = {4}`. The
  six-cycle obstruction is global, not local.

---

## 8. Two corrections, and one dead end of my own

### 8.1 A gap in the "heavy direction" hint of m11

`.ultramath/smwfo9zkl/m11/k6-ternary-palette.md` §6 item 2 offers a step towards `|P_x(e)| ≤ 2` at
`k = 6`: if the palette at some direction is the full triangle triple `T`, then "the three palettes
`P_{y_j}(e)` are pairwise disjoint nonempty subsets of `I ∖ T`, so they are its three singletons",
for `y_j = x + exp(i(θ + jκ))`, `j = 0,1,2`, described as "the three equilateral vertices, each at
distance one from `x`, and pairwise at distance one".

The three points are **not** pairwise at unit distance: their mutual distances are `1, 1, √3`
(`|1 − e^{2πi/3}| = √3`). Three points on a unit circle can never be pairwise at unit distance — the
unit-distance graph on a circle is a disjoint union of hexagons, so only *consecutive* directions are
at distance one. What the two-centre exclusion (Remark 5.3) gives at a heavy direction with
`P_x(e) = T` is only: `P_{y_j}(f) ⊆ I ∖ T` for all three `j`, and
`P_{y_0}(f) ∩ P_{y_1}(f) = ∅`, `P_{y_1}(f) ∩ P_{y_2}(f) = ∅` — while `P_{y_0}(f)` and `P_{y_2}(f)`
**may be equal**. So `P_{y_1}` is not forced to be a singleton and the suggested step to three
singleton palettes does not follow.

Nothing load-bearing in m11's note depends on this: its Theorems 1–3, Corollary 4, the finite
classification and the seven-centre certificate of its §5.4 are unaffected, and I re-checked the
models independently in `verify.py` section B. Use the corrected geometry if you build on the hint.

### 8.2 A dead end: my own direction d14 (scale gluing)

d14 proposed to build a `k = 6` countermodel by gluing a 6-colourable pattern across a geometric
sequence of scales, so that the palette depends on `z` only through a scale band such as
`⌊log₂ |z|⌋ mod 3`, with a finite transition gadget at each boundary, and to decide the gadget
exactly. This is refuted before any gadget is reached:

* for every `y` whose unit circle `S¹(y)` stays inside one scale band, the type is constant on that
  circle, so by Theorem D the hitting condition (HIT) fails at `y`;
* the set of such `y` has infinite measure — it contains the annuli `2^k + 1 < |y| < 2^{k+1} − 1`,
  whose total measure is `Σ_k 2π(2^{k+1} − 1 + 2^k + 1)(2^k − 2)`, which diverges;
* by Corollary C1 a field that fails (HIT) on a positive-measure set is not the palette field of any
  colouring.

The same argument kills every graded, hierarchical, self-similar or lacunary ansatz, and every
centre-independent sector model: "more clever grading" cannot work. Independently, no proper
6-colouring of the plane is known (`6 ≤ χ(R²) ≤ 7` after the paper's Theorem 1.1), so any `k = 6`
construction has Hadwiger–Nelson's upper bound as a subproblem — which is the content of Theorem C.

---

## 9. Files and exact commands

| file | content |
|---|---|
| `POINT-FIELD.md` | this note: Theorems A–F, Corollaries C0–C2, the m11 correction, the d14 dead end |
| `verify.py` | exact checks A–D below; exits `0` iff all 34 checks pass |
| `verify.out` | recorded output of the run |

```
python3 verify.py          # ~2 s, exact arithmetic in Q(sqrt3, sqrt11)
```

* **A** geometry: `R − 1 = exp(2πi/3)`, `|R−1| = |1−R| = 1`; for every exact unit `w` there is a unit
  `e` with `(R−1)e = w` and a unit `e` with `(1−R)e = w`; `(x,e) ↦ (x+e, x+Re)` is injective into
  unit pairs with `v − u = (R−1)e`; `e ↦ (R−1)e` is the rotation by `2π/3`; every sampled unit pair
  is `(x+e, x+Re)`, and also `(x+Re, x+e)` for the trace form (A1–A7, the last recording that m11's three points are at squared distances 1, 1, 3).
* **B** the five countermodel families: palette axioms hold, total intersection of values is empty
  (failure of (HIT)), with an explicit witness pair of directions and centres.
* **C** the Moser spindle in exact coordinates (7 vertices, 11 unit edges, not 3-colourable, 4-
  colourable); the point-field system is UNSAT at `k = 3` (exhaustive over nonempty subsets) and SAT
  at `k = 6` with a witness.
* **D** the wheel `W₆`: six-cycle structure at the hub consistent at `k = 6`, explicit witness.

All arithmetic is exact (`fractions.Fraction` on the basis `1, √3, √11, √33`); no floating point is
used in any decision.
