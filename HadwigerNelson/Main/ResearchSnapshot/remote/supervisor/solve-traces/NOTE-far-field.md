# The palette is a radius-one trace: far-field decoupling, and what it costs at k = 6

Owner: `supervisor/solve-traces` (coordinator: trace and measure constraints). 2026-11-14 UTC.
Read from source in this repo; nothing outside this directory was modified.

## 0. Grade of claims
* **[S]** source-checked at the cited Lean lines. **[P]** paper-level proof written here, every
almost-everywhere quantifier retained. **[A]** exact arithmetic, script in `checks/`, output saved.

## 1. [S] The palette object is a *radius-one cluster trace*, not a small-scale self-correlation

`lean/OAI/Geometry/PlaneColoring/Compactness.lean`:
* l.97 `sampleFn c y r i t := if c (y + (r:C) * direction t) = i then 1 else 0` - the colour at
  distance `r` from centre `y` in direction `t`;
* l.111 `sample := (sampleFn_memLp ...).toLp _` - its L2 class on the direction circle;
* l.255-262 `sampleCode c y r : TraceVector k`, `IsTrace c x b := (x,1,b) in closure (sampleSet c hc)`,
  `sampleSet := {(y,r,b) : TypicalSampling c y r and b = sampleCode c y r}`;
* l.262-272 `trace_realization`/`trace_of_realization`: `IsTrace c x b` iff there are `y n -> x`,
  `r n -> 1` with `sampleCode c (y n) (r n) -> b`.

`Palettes.lean` l.9-45: `tracePositive`, `paletteGenerators` (countable essential union), `paletteSet`,
`palette x t = {i : t in paletteSet x i}`.

**Consequence (the reading used below).** For label `i`, unit direction `e`, centre `x`:

> **[S]** `i in P_x(e)` iff there are `y_n -> x`, `r_n -> 1`, an angle `t` representing `e`, and a set `T`
> of directions of positive angular measure near `t`, with `c(y_n + r_n u) = i` for all large `n`, `u in T`.

So `P` is a **far-field** object (distance about 1) and `Gamma_x` (`Transitions.lean` l.6-25,
`transitionSet` at separation `h -> 0`, `transitionRatio = volume/|h|`) is a **near-field** object: they are
computed from disjoint families of colour samples, and no palette axiom ties the radius 1 to the scale `h`.
Consistency check against the two colourings the project owns:

| colouring | palette at a.e. centre | Gamma |
|---|---|---|
| hexagonal 7-colouring `c_0` | `P_x(e) = {c_0(x+e)}` (singleton) | locally constant, no cycle in `Gamma_x` |
| `m3` seven-colouring at `q_n` | `{1,4,5,6}` - the four *outsider* labels | contains the triangle `{0,2,3}` |

Section 3 explains *why* the palette at `q_n` cannot contain `0,2,3`: the gadget is smaller than the radius.

## 2. [P] Lemma D (far-field decoupling)

> **Lemma D.** Let `c, c' : C -> Fin k` be measurable. Let `x_0 in C`, `0 < eps <= 1`, and suppose `c = c'`
> off the open ball `B(x_0, 1-eps)`. Then for a.e. direction `e`: `P^c_{x_0}(e) = P^{c'}_{x_0}(e)`.

*Proof.* By `trace_realization` it suffices to show every trace of `c` at `x_0` is a trace of `c'` at
`x_0` (the relation is symmetric). Let `b` be a trace of `c` at `x_0`, realised by `y_n -> x_0`,
`r_n -> 1`, `sampleCode c (y_n) (r_n) -> b`. For `n` large, `|y_n - x_0| < eps/2` and `|r_n - 1| < eps/2`,
hence for every direction `u`, `|(y_n + r_n u) - x_0| >= r_n - |y_n - x_0| > 1 - eps`: the sampled point
lies outside `B(x_0,1-eps)`, where `c = c'`. Hence `sampleFn c (y_n) (r_n) i t = sampleFn c' (y_n) (r_n) i t`
for **every** `t` and all large `n`, i.e. `sampleCode c' (y_n) (r_n) = sampleCode c (y_n) (r_n) -> b`, and
`b` is a trace of `c'` at `x_0` by `trace_of_realization`. No a.e. quantifier is spent: the exceptional set
is empty. `square`

**Remarks.** (1) `eps` is free and `k`-independent; agreement off `B(x_0,R)` with `R < 1` suffices, `R = 1`
does not, since circles of radius 1 about `y != x_0` cross the sphere. (2) `TypicalSampling` costs nothing:
it constrains only the sample points, where `c = c'`. (3) Properness is not used.

**Corollary D1 (accumulation of cyclic centres is invisible to the palette).** If `L` contains `q_n -> p`
and `c` near `q_n` differs from a *fixed* measurable background `c'` only inside `B(q_n, 1-eps_n)` with
`eps_n -> eps > 0`, then every label of every `P_{q_n}` is a background label on the unit annulus about `p`.
The accumulation is a statement about `Gamma`; the palette cannot see it. This is the shape of the k >= 7
counterexample and the reason no palette-level axiom separates one cyclic centre from infinitely many
accumulating ones (`sprint/k6/FREE-LABEL.md`).

## 3. [A] The k >= 7 counterexample verified against Lemma D

`m3`: `p_0 = (1/55, 18/55)`, `ell = 1/100`, `W = p_0 + [-ell/2, ell/2]^2`, `q_n = p_0 + (ell 2^(-n-3), 0)`;
`c` equals the background `c_0` off `W`. `checks/decouple_arith.py` (Fractions) computes

```
max_{z in W} |z - q_n| <= 0.008004   (n = 0, worst case; -> 0.007078 by n = 7)
```

so `W` lies in `B(q_n, 1/2)`: Lemma D applies with `eps = 1/2`, hence `P^c_{q_n}(e) = P^{c_0}_{q_n}(e)` a.e.
`e`. Every trace circle satisfies `|y + r u - p_0| in (1-eps-|q_n-p_0|, 1+eps+|q_n-p_0|)` contained in
`(0.498, 1.502)`, which contains `m3`'s certified annulus `A = {1-71/10000 <= |q-p_0| <= 1+71/10000}`; on
`A` the background meets no hexagon of colour `0,2,3`. Hence `P_{q_n}(e)` is contained in `{1,4,5,6}` while
`c(q_n) in {0,2,3}`. This is a *verification* of the recorded example, and the first derivation of both
halves from one lemma about the trace rather than from the gadget's geometry.

## 4. What this says about the frontier at k = 6, and what it does not

The genuine-colouring constraints on `P`, with exact quantifiers:

* **(A1) trace** [recorded, `m10`]: for a.e. `x`, a.e. `e`, `c(x+e) in P_x(e)`.
* **(A2) two-centre disjointness** [recorded, `m4`]: for a.e. `e`, a.e. `x`, every unit `a`,
  `P_x(e) cap P_{x+a}(e) = empty`.
* **(A3) far-field decoupling** [Lemma D]: `P_x` is determined by the annulus `{1-eps <= |z-x| <= 1+eps}`,
  uniformly in the colouring behind it.
* **(A4) sum rule** [`trace_bounds`, Compactness.lean l.297]: `sum_i traceValue b i = 1`, so the direction
  `e` density is a probability measure supported in `P_x(e)`.

1. (A1)+(A2) already give properness (`m10` Thm 4; `m4` Cor. 2), and (A3) says `P` cannot distinguish a
   colouring from a recolouring of a ball of radius < 1. Hence **no axiom system on `P` alone decides (W)**:
   the countermodels fail the trace, and imposing the trace returns `chi(R^2) <= 6` (`m10` Thm 3).
2. A k = 6 accumulating colouring modelled on `m3` therefore costs exactly: **a proper 6-colouring of the
   plane minus a small disk whose unit-annulus colours avoid the gadget's cycle labels.** By (A3) that
   annulus condition decouples from the gadget, so the cost is a colouring, not a palette count - the
   "purely chromatic wall" sentence of `sprint/k6/REPORT.md` section 3b, here derived rather than observed.
3. Not claimed: nothing here decides (W), bounds `chi(R^2)`, or produces a 6-colouring.

## 5. Files

| file | content |
|---|---|
| `checks/decouple_arith.py`, `checks/decouple_arith.out` | [A] the k >= 7 decoupling arithmetic |
| `.ultramath/smwfyhztv/` | three independent checks of Lemma D (owned swarm) |

## 4b. [P] Corollary D2 (a no-go for a whole style of argument)

> **Corollary D2.** Let `c` be weak measurable, `x in C`, `0 < eps <= 1`, and let `c'` be any
> measurable colouring with `c' = c` off `B(x, 1-eps)`. Then `P^{c'}_x = P^c_x` (a.e. direction), while
> the near-field data of `c'` at `x` - the sets `transitionSet c' i j x R h` for `h -> 0`, hence
> `Gamma_x`, hence membership of `x` in the cyclic locus `L` - are unconstrained by `P^c_x`.

Consequently: **no argument can derive a property of the near-field germ at `x` (in particular
`x in L`, `x notin L`, or any cycle in `Gamma_x`) from the palette at `x` alone.** Information about
`P_x` is information about the annulus `{1-eps <= |z-x| <= 1+eps}`, at distance one. This is exactly
why the `k >= 7` construction works, and it fixes the form any `k = 6` argument must have: the palette
constraints must be applied at centres *away* from the cyclic centres (at distance about 1), never at
them. It also explains why the record's `Gamma`-side and `P`-side computations never interact: they are
computations about disjoint regions.

The `k = 6` question in this language: is there a weak measurable 6-colouring `c` such that the family
of "far-field palettes" `{P_{q_n}}` is consistent with `c`'s properness on all the unit annuli while
`Gamma_{q_n}` carries a cycle for `q_n -> p`? Corollary D2 says the two halves can be *specified*
independently; they cannot be *realised* independently only because a single colouring must produce
both, which is the chromatic wall.

## 4c. [P] Sharpness of Lemma D: the radius 1 is not attained

Independent member `m1` of the owned swarm `smwfyhztv` produced, and I checked, the following. Take
`x_0 = 0`, `k = 2`, `c_1(z) = 0` for `|z| < 1` and `c_1(z) = 1` for `|z| >= 1`; `c'_1 ≡ 1`. Then
`c_1 = c'_1` on the closed set `{|z| >= 1}`, i.e. they agree off the OPEN unit ball, and yet

* `c_1`: `y_n = 0`, `r_n = 1 - 1/(n+2) < 1` puts the whole sampling circle inside the open unit disc, at
  interior points of the colour-`0` class, so `TypicalSampling` holds and `sampleCode` is constantly
  `(1,0)`; hence `0 in P^{c_1}_0(e)` for a.e. `e`. Likewise `r_n = 1 + 1/(n+1)` gives `1 in P^{c_1}_0(e)`.
  So `P^{c_1}_0 = {0,1}` a.e.
* `c'_1` is constant, so every sample code is `(0,1)`, every trace is `(0,1)`, and `P^{c'_1}_0 = {1}`.

Hence `P^c_0 != P^{c'}_0` on a set of directions of FULL angular measure. So Lemma D's hypothesis
`R < 1` cannot be relaxed to `R = 1`: **the constant 1 is a genuine threshold, and it is not attained**.
The same member's sharper form: if `c = c'` on `{|z - x_0| >= 1}` and the palettes at `x_0` differ, then
the disagreement set must accumulate on the sphere `S(x_0,1)` (contrapositive of Lemma D with
`R = 1 - delta`). Files: `.ultramath/smwfyhztv/m1/sharpness.md` (sections 4.1-4.3).

*Consequence for section 4b.* Corollary D2 must be read with `eps > 0`: a recolouring supported in a ball
of radius exactly 1 CAN move the palette, but only by reaching the sphere. The gadget hypothesis of
section 3 (diameter `< 1`, hence contained in `B(q_n, 1/2)`) is therefore exactly what is needed, and it
cannot be weakened to "supported in `B(q_n,1)`".

A companion member (`m3`) proves the palette is a measure-class invariant: if `c' = c` off a
Lebesgue-null set then the trace sets agree (their Theorem 1: at a point where the two colourings differ,
at most one of them is typical, so no trace is lost), hence `P^{c'}_x = P^c_x` a.e. direction for every
`x`. This is the right robustness statement for a palette-based argument and it makes precise that
palettes cannot see exceptional sets. File: `.ultramath/smwfyhztv/m3/report.md`.
