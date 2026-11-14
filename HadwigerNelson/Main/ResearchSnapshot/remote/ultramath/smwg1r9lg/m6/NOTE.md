# d2 — The `S_1` reformulation of the `k = 6` triangle locus, and the accumulation

Member `m6`, swarm `smwg1r9lg`. Direction **d2**.

**Deliverable.** (i) An exact equivalence theorem identifying the `k = 6` three-valued
triangle locus `Z^3(V)`: in palette form at every centre, and in *circle form* at every centre
whose unit circle meets the non-typical set null-ly (a.e. centre) — Theorem 1, with the two
places where the direction's phrasing needs correction. (ii) The accumulation theorem
(Theorem 2): every accumulation point of `Z^3(V)` is again a centre with `Gamma_p ⊇ K_3(V)`
and `P_p ⊆ T`; the state functions converge in `L^1`; the limit is either a 3-valued triangle
centre (and then the limit carries *all* of the approximants' data) or a binary triangle
centre, of which there are only finitely many per ball. (iii) A decided negative statement
(Theorem 3): the accumulated system is *satisfiable*, with an explicit exact-arithmetic
model realising both branches, so no contradiction is derivable from the per-centre axioms
plus the unit-separation transport. (iv) Two corrections to the record, one of them
load-bearing: the record's "self-avoidance" Lemma D (`i ∉ P_x(e)` at a density point of
`A_i`) is **not established by its proof** (§5), which is why Theorem 1 does not use it.

Everything is stated for `k = 6`; Theorems 1–3 are `k`-blind in their proofs and are stated
for general `k` where that is free, because the `k = 5` and `k = 7` calibrations are then
immediate (§6).

**Reproduce.** `python3 verify.py` in this directory: **1996 checks, exit 0** (output in
`out.txt`). All decisions are in integer, `Fraction` or `Q(sqrt 3)` (sympy) arithmetic; no
floating-point comparison occurs anywhere.

**What is not proved.** `(W)` and `(Sep3)` at `k = 6` are not decided here; Theorem 3 says
what a proof must use (§7). Nothing here is unconditional at `k = 6`: the class `S_1` is
non-empty at `k = 6` only if `chi(R^2) <= 6`, and every statement about `S_1` at `k = 6` is
conditional on that (the paper's Theorem 1.3: a weak measurable `k`-colouring exists iff
`chi(R^2) <= k`).

---

## 1. Setting, notation, and the cited facts

`I = {1,...,6}`. `c : R^2 -> I` is a **weak measurable `6`-colouring**: the classes
`A_i = c^{-1}(i)` are measurable and `{(z,u) in R^2 x S : c(z) = c(z+u)}` is
`dx dsigma(u)`-null (the paper's weak condition, §4; it is equivalent to `chi(R^2) <= 6`
for the existence question, and it is the hypothesis of `S_1`).

`S = S^1`, `sigma` the normalised angular measure, `R` the rotation by `kappa = pi/3`,
`J` the rotation by `pi/2`. `H_i` is the closed spatial essential support of `A_i`.
`W_x` is the family of circle traces at the centre `x` and `P_x(e)` the maximal palette, both
as in **Definition 5.1** of the paper (p. 26): `W_x` is the set of weak-`*` limits
`w*-lim_n (1_{A_i}(y_n + r_n e))_i` with `y_n -> x`, `r_n -> 1`, each `(y_n,r_n)` a typical
circle sampling; `P_x(e) = {i : e in ess-union_{b in W_x} {b_i > 0}}`.

`Gamma_x` is the transition graph, **Definition 6.1** (p. 34): for distinct `i,j` put
`D_{ij}(B,h) = {q in B : (c(q), c(q+h)) in {(i,j),(j,i)}}`, and `{i,j}` is an edge of
`Gamma_x` iff for every ball `B` centred at `x` with positive finite radius

```
   limsup_{h -> 0, h != 0} |D_{ij}(B,h)| / |h| > 0 .                              (6.1)
```

`L = {x : Gamma_x contains a cycle}` (the paper's (6.4), p. 37).

**The class `S_1`** (of the record): at *every* centre `x`, `|P_x(e)| = 1` for a.e. `e`. Write
`P_x(e) = {sigma_x(e)}` and `R_x = {i : sigma{sigma_x = i} > 0}` for the essential range. `S_1`
contains every colouring constant on the cells of a locally finite Borel partition with
piecewise `C^1` boundaries and every cell colouring of the record; at `k = 6` it is non-empty
only if `chi(R^2) <= 6`.

Cited from the paper (used, not re-derived, but checked against two independent extractions
of the pdf — see §8):

* **(5.2)** (Lemma 5.2(1), p. 27) at every fixed centre `x`, for a.e. pair `(e,v) in S x S`:
  `c(x+e+v) notin P_x(e) union P_x(v)`.
* **(5.3)** (Lemma 5.2(3), p. 27): the smooth-transport exclusion; the instance used at unit
  separation is **(TE)**: for `|a| = 1`, `P_{x+a}(f) cap P_x(f) = empty` for a.e. `f`.
* **(5.7)** (Corollary 5.4, p. 29): `P_x(f) cap P_x(Rf) = empty` for a.e. `f`, every centre.
* **Lemma 5.5** (p. 30): for each pair of labels, two distinct centres binary for that pair
  are at distance `>= delta_* > 0`.
* **Lemma 6.2 / (6.2)** (p. 35): if `{i,j} in E(Gamma_x)` there is a trace `b in W_x` with
  `b_i = b_j = 0` a.e.; consequently `P_x(e) not subset {i,j}` a.e. (label-blind: the proof
  uses (6.3) and Cauchy–Schwarz only, and is used here at `k = 6`).
* **(5.1)** (p. 27): closure of the trace families under varying centres:
  `x_n -> x`, `b_n in W_{x_n}`, `b_n` weak-`*` convergent `=>` the limit is in `W_x`.
* the *maximum principle of Definition 5.1* (p. 27): every individual trace has its positive
  coordinates inside the palette almost everywhere; the palette is non-empty a.e.

---

## 2. Lemma 1: the palette is the unit-circle colour, at every good centre (a.e. centre)

The record uses "`P_x(e) = {c(x+e)}` a.e." in `S_1`, citing it as `(T)`/Lemma P without proof
and (in `m2`'s version) at a.e. centres. The proof below is complete, and it shows exactly how
far the statement reaches: it holds at every **good** centre, and good centres are conull. The
qualification is not cosmetic and it is the same "a circle is a null set" phenomenon as in
§5–§6: at a centre whose unit circle happens to lie inside the plane-null set of non-typical
points, the values of the colouring *on that circle* carry no information at all (and can be
changed by modifying `c` on a null set without changing any palette). Call `z` **typical** if
`z` has density one of its class `A_{c(z)}`, and call a centre `x` **good** if the unit circle
about `x` meets the set `N` of non-typical points in an angular-null set.

> **Lemma 1.** Let `c` be a weak measurable `k`-colouring, `x` a good centre, `i in I`. Then
> the bounded measurable vector `e |-> 1_{A_i}(x+e)` belongs to `W_x`. Hence
> `P_x(e) >= {c(x+e)}` for a.e. `e in S`. The good centres are conull (hence dense).

*Proof.* (a) The set `N` of non-typical points is plane-null (Lebesgue differentiation, finite
union over labels). Call `y` **good** if the unit circle about `y` meets `N` in an angular-null
set. The good centres are conull: `{(y,e) : y + e in N}` is product-null by Fubini, so a.e.
section `{e : y + e in N}` is null; in particular good centres are dense. For a good `y` the
pair `(y,1)` is a *typical circle sampling* in the sense of Definition 5.1, so the constant
sequence at `(y,1)` exhibits `b_y := (1_{A_i}(y + e))_i` as an element of `W_y` ("constant
sequences are permitted").

(b) Fix a good `x` and put `h(y) := int_S |1_{A_i}(y+e) - 1_{A_i}(x+e)| dsigma(e)`. Then
`liminf_{y -> x} h(y) = 0`. Suppose not: `h >= eps` on some `B(x,r)`. Integrating over that ball
and using Tonelli,
`eps |B(x,r)| <= int_{B(x,r)} h = int_S int_{B(x+e,r)} |1_{A_i}(z) - 1_{A_i}(x+e)| dz dsigma(e)`.
Because `x` is good, for a.e. `e` the point `x+e` is a density point of its own class `A_j`; then
the inner integral is `o(r^2)`: if `j = i` the integrand is `1 - 1_{A_i}` on the ball, whose mean
tends to zero by density one, and if `j != i` it is `1_{A_i}` on the ball, whose mean tends to
zero because the classes partition the plane up to null sets, so the `A_i`-density at a density
point of `A_j` is `0`. So the right-hand side is `o(r^2)`, a contradiction for small `r`.

(c) Hence there are `y_n -> x`, good, with `h(y_n) -> 0`. Then
`||b_{y_n} - b^*||_{L^1(S)} = h(y_n) -> 0` where `b^* = (1_{A_i}(x+e))_i`, so `b_{y_n}` is
weak-`*` convergent to `b^*`; by (5.1) with `y_n -> x` and `b_{y_n} in W_{y_n}`, `b^*` lies in
`W_x`. Since every trace of `W_x` has its positive coordinates inside `P_x` a.e., `i in P_x(e)`
for a.e. `e` with `c(x+e) = i`. Finite union over `i`. `square`

Three remarks on the form of the statement. (i) The proof never evaluates the circle of radius
one about `x` itself: it compares the circles about centres *near* `x` with that circle in
`L^1`, which is why the conclusion survives at every good centre and not merely a.e. (ii) The
goodness hypothesis is not an artefact of the proof. A plane-null set may contain a whole
circle, so at a centre `x` whose unit circle lies in `N` the colour values on that circle are
arbitrary; and they really are arbitrary, because changing `c` on a plane-null set leaves the
palette `P_x` and the graph `Gamma_x` untouched (for `P_x`: each sampling pairing moves by an
integral over a null set of directions; for `Gamma_x`: (6.1) is a statement about areas) while
it changes `c` on that circle. So no statement about the colouring *on the circle about an
exceptional centre* can be a consequence of the palette axioms. (iii) At a good centre the
conclusion, being a.e. in `e`, is invariant under null-set modifications of `c`: for good `x`
the set `{e : x+e in N}` is null.

> **Corollary 1.** Let `c` be in `S_1`.
> (i) At **every** centre `x` and for a.e. `e`: `P_x(e) = {sigma_x(e)}` and hence
> `R_x = {i : sigma{sigma_x = i} > 0}`.
> (ii) At every **good** centre `x`, and for a.e. `e`: `P_x(e) = {c(x+e)}`, and consequently
> `R_x = {i : sigma{e : c(x+e) = i} > 0}`.

So at a good centre the palette field is literally the colouring of the unit circle about `x`,
and `R_x` is the essential range of that circle colouring; at an exceptional centre only the
palette form survives. Nothing in this section uses `k = 6`.

---

## 3. Lemma 2 and Theorem 1: the exact reformulation of `Z^3(V)`

> **Lemma 2** (= `smwfycxze` m4, Lemma A; included for completeness). In `S_1`, if
> `{i,j} in E(Gamma_x)` then `R_x cap {i,j} = empty`. Hence `Gamma_x` is a subgraph of
> `K_{I \ R_x}` and has no simple cycle longer than `k - |R_x|`.

*Proof.* (6.2) gives `P_x(e) not subset {i,j}` a.e., i.e. `sigma_x(e) notin {i,j}` a.e. If
`sigma{sigma_x = i} > 0` then on a positive-measure set `P_x(e) = {i} <= {i,j}`, contradiction;
same for `j`. `square`

> **Lemma 2'** (= `smwfycxze` m4, Lemma B). `|R_x| >= 2`.

*Proof.* `R_x` is non-empty. If `R_x = {i}` then `sigma_x = i` a.e. and (5.7) reads
`{i} cap {i} = empty`. `square`

Fix a `3`-element `V <= I` and put `T := O := I \ V` (three labels; `T` is the direction's
"complementary triple"). Define

```
   Z^3(V) := { x : Gamma_x = K_3(V)  and  R_x = O } .
```

> **Theorem 1 (exact reformulation).** Let `c` be a weak measurable `6`-colouring in `S_1`,
> `V` a `3`-element subset of `I`, `O = I \ V`.
>
> **(P) (palette form, at every centre).**
> ```
>    Z^3(V) = { x : R_x = O } cap { x : K_3(V) <= Gamma_x } ;
> ```
> and for `x` with `R_x = O` one has `Gamma_x <= K_3(V)`, so that `Gamma_x = K_3(V)` iff
> `x in L`. In particular **every three-valued triangle centre has `Gamma_x = K_3(V)`
> exactly**, and contains no other edge and no other cycle.
>
> **(C) (circle form, at every good centre).** For a good `x` (Lemma 1), `R_x = O` is
> equivalent to
> **(a)** `sigma{e in S : c(x+e) in V} = 0`  (the unit circle about `x` is `O`-valued a.e.),
> **(b)** `sigma{e : c(x+e) = i} > 0` for each of the three `i in O`;
> and hence, for a good `x`,
> ```
>    x in Z^3(V)  <=>  (a) and (b) and (c),      (c)  K_3(V) <= Gamma_x .
> ```
> Equivalently, for a good `x`: `x in Z^3(V)` iff the unit circle about `x` carries exactly
> `O` a.e. (all three labels, each on a set of positive angular measure) and `x in L`.
>
> At an exceptional centre (a plane-null set of them) the circle form is *not* asserted, and
> cannot be: modifying `c` on a plane-null set changes the circle values at such a centre
> without changing `R_x` or `Gamma_x` (Lemma 1, remark (ii)). The palette form (P) holds at
> every centre without exception.

*Proof.* (P): `Z^3(V)` is the intersection by definition; if `R_x = O` then by Lemma 2 every
edge of `Gamma_x` avoids `O`, i.e. `Gamma_x <= K_{I\O} = K(V) = K_3(V)`; a subgraph of a
triangle is cyclic iff it is the triangle (verified exhaustively for all `20` triples `V` in
`verify.py` block D and machine-checked as `D2.core` in `lean/d2_core.lean`).
(C): at a good centre, Corollary 1(ii) identifies `R_x` with the essential range of
`e |-> c(x+e)`, so `R_x = O` is exactly "(a) and (b)"; combine with (P). `square`

**Two corrections to the direction's phrasing.** The direction states the equivalence as
"a 3-valued triangle centre with cycle `V` is exactly a centre `x` with `c(x) in V` whose unit
circle carries only the complementary triple `T` a.e.".

1. *"carries only `T`" is the weaker condition `R_x <= O`, not `R_x = O`.* At a good centre,
   condition (a) alone gives `R_x <= O`, hence `|R_x| in {2,3}` (Lemma 2'), and `R_x <= O`
   with `|R_x| = 2` is the *binary*
   triangle centre — the case that Lemma 5.5 makes locally finite. `k = 5` is the extreme
   illustration: there `|O| = 2`, so *every* triangle centre satisfies "carries only `T`"
   and *none* is 3-valued; the direction's formulation would make `Z^3` empty at `k = 5`,
   which is consistent with `(W)` there but not with the equivalence. So condition (b)
   (positivity of all three values) and condition (c) (the transitions, i.e. `x in L`) are
   both needed. (a) does not imply (c): under `R_x <= O` the graph `Gamma_x` is *any*
   subgraph of `K_3(V)`, and only the cyclic one is `Z^3`.
2. *"`c(x) in V`" is not needed and is not established.* It is what one gets from the
   record's Lemma D (self-avoidance) applied to `c(x) in O`; Lemma D's proof has a gap (§5),
   and Theorem 1 never mentions the colour at `x`. What *is* true by (6.1) and (6.2) is
   `x in H_i` for every `i in V` (an edge `{i,j}` of `Gamma_x` forces `x in H_i cap H_j`,
   p. 34), so a `Z^3` point is a limit point of each of the three triangle classes; whether
   `x` itself lies in a triangle class is not decided by the palette data.

**General `k`.** With `r := |R_x| = k - ell`, the same proof gives
`Z^r(V) := {Gamma_x = K_ell(V), |R_x| = k-ell} = {(a),(b),(c)}` for every `k` and `2 <= ell <= k-2`
(the circle form at good centres, the palette form always);
at `k = 6, ell = 3` this is `Z^3` and `(W)` in `S_1` is local finiteness of `Z^3` (the
record's Theorem 5). At `k = 5, ell = 3` Theorem 1 says `Z^2(V) = {(a),(b),(c)}` with `|O| = 2`,
and then `R_x = O` *is* binarity, so Lemma 5.5 applies: **the paper's `k = 5` triangle case is
exactly the case `|O| = 2` of Theorem 1** — the calibration is built into the statement. At
`k = 7, ell = 3` we get `|O| = 4` and `m3`'s colouring realises `Z^4(V)` with accumulating
centres (§6).

---

## 4. Theorem 2: what the accumulation point must be

> **Theorem 2 (accumulation).** Let `c` be a weak measurable `6`-colouring in `S_1`, `V` a
> `3`-element subset, `O = I\V`, and let `x_n in Z^3(V)` be distinct with `x_n -> p` (if the
> triples vary, pass to a subsequence on which `V` is constant — there are only `20`). Then:
>
> **(0)** For every pair `{i,j}` the locus `{x : {i,j} in E(Gamma_x)}` is closed; hence
> `C_V := {x : K_3(V) <= Gamma_x}` is closed and `Y(V) := {x : Gamma_x = K_3(V)}` is closed.
>
> **(1)** `K_3(V) <= Gamma_p` and `P_p(e) <= O` for a.e. `e`; in particular `R_p <= O`.
>
> **(2) (state continuity)** For each `i in O`,
> `1{sigma_{x_n} = i} -> 1{sigma_p = i}` in `L^1(S)`; consequently the three masses
> `m_n(i) := sigma{sigma_{x_n} = i}` converge to `m_p(i) := sigma{sigma_p = i}`.
>
> **(3) (dichotomy)** `|R_p| in {2,3}`, and exactly one of:
> **(3a)** all three `m_p(i) > 0`: then `R_p = O`, `Gamma_p = K_3(V)` exactly, `p in Z^3(V)`,
> and `p` carries the same triple `V` and the `L^1`-limit of the approximants' states;
> **(3b)** exactly one `m_p(i) = 0`: then `R_p = O\{i}`, `p` is a **binary** centre for the
> pair `O\{i}`, and `K_3(V) <= Gamma_p <= K_{V union {i}}`.
>
> **(4)** Hence every accumulation point of `Z^3(V)` is in `Z^3(V)` or is a binary triangle
> centre for one of the three pairs in `O`; those are `delta_*`-separated (Lemma 5.5, one
> pair at a time), hence **locally finite**. So `Z^3(V)` is closed modulo a locally finite
> set.
>
> **(5) (quantitative closedness).** For `delta > 0` let
> `Z^3_delta(V) := {x in Z^3(V) : m_x(i) >= delta for all i in O}`. Then `Z^3_delta(V)` is
> **closed**; and `Z^3(V) = union_{delta > 0} Z^3_delta(V)`. So an accumulation of `Z^3(V)`
> that leaves every `Z^3_delta(V)` must lose a label: the only way the three-valued part of
> the triangle locus stops being closed is that one state mass tends to `0` along the
> sequence.

*Proof.* **(0)** This is the paper's own remark after (6.1) (p. 34), written out: if
`x_n -> x` and `{i,j} in E(Gamma_{x_n})`, let `B` be a ball centred at `x`; pick `n` with
`|x_n - x| < r/2` and put `B' = B(x_n, r/2) <= B`. Then
`limsup_h |D_{ij}(B,h)|/|h| >= limsup_h |D_{ij}(B',h)|/|h| > 0` because `D_{ij}(.,h)` is
monotone in its ball argument. So `{i,j} in E(Gamma_x)`. `C_V` is a finite intersection of
such loci; `Y(V)` is `C_V` intersected with the complements of the three loci of the pairs
outside `V` (open sets), so closed.

**(1)** `K_3(V) <= Gamma_p` is (0). For `i in V` pick `j in V`, `j != i`; (6.2) at the edge
`{i,j} in E(Gamma_p)` gives `b in W_p` with `b_i = b_j = 0` a.e., and every trace's positive
set lies inside `P_p` a.e., so `i notin P_p(e)` a.e. Hence `P_p <= O` a.e.

**(2)** In `S_1` every trace at a centre equals the singleton `e_{sigma_x}` a.e. (its support
is inside `P_x`, which is a singleton, and the coordinates sum to one). Apply this to the
traces of (6.2) at `x_n`: `b^{ij,(n)} = e_{sigma_{x_n}} in W_{x_n}` for each edge `{i,j}` of
`K_3(V)`. Passing to a subsequence, (5.1) gives `e_{sigma_{x_n}} -> b^{ij} in W_p` weak-`*`.
By (1), `b^{ij}` is supported in `P_p = {sigma_p}` a.e., and it sums to one, so
`b^{ij} = e_{sigma_p}`. So the whole sequence satisfies `e_{sigma_{x_n}} -> e_{sigma_p}`
weak-`*`. For `f_n := 1{sigma_{x_n} = i}` and `f := 1{sigma_p = i}` this gives
`int f_n f -> int f^2 = int f`, hence
`||f_n - f||_1 = int f_n + int f - 2 int f_n f -> 1 + 1 - 2 = 0`.

**(3)** `R_p <= O` by (1) and `|R_p| >= 2` by Lemma 2'. So the third alternative is
impossible, and if all three masses are positive then `R_p = O` and Lemma 2 gives
`Gamma_p <= K_{I\O} = K(V)`; with `K_3(V) <= Gamma_p`, `Gamma_p = K_3(V)`. If one mass
vanishes, `R_p` is a two-element subset of `O`, `sigma_p in R_p` a.e., so `P_p(e)` meets the
pair `R_p` a.e. — that is binarity — and Lemma 2 gives `Gamma_p <= K_{I \ R_p}`. **(4)** is
(3) plus Lemma 5.5. **(5)** run the proof of (1)+(2)+(3a) with the extra hypothesis
`m_{x_n}(i) >= delta`: the `L^1` limit still gives `m_p(i) >= delta` (convergence of the
masses), so `R_p = O`, `Gamma_p = K_3(V)`, `K_3(V) <= Gamma_p`, i.e. `p in Z^3_delta(V)`; and
`Z^3(V)` is the increasing union of the `Z^3_delta(V)`. `square`

**Reading.** The direction asked: *is `R_p` still `T`? is `p` itself a 3-valued triangle
centre?* Answer: `R_p <= T` always, and at the level of the triangle `Gamma_p ⊇ K_3(V)` always;
`p` is a 3-valued triangle centre **iff** none of the three state masses collapses in the
limit; the collapse alternative is the binary triangle locus, which carries no accumulation
(it is `delta_*`-separated). In particular the accumulation does **not** lose information:
the limit's state function is the `L^1` limit of the approximants' state functions, and the
limit's masses are the limits of the masses. So no contradiction can come from "the structure
degenerating at the limit" — the only candidate degeneration is a mass collapsing to zero,
and that lands in the locally finite binary case.

Note the *sharpness* of (3b): it is not empty at the level of the axioms — Theorem 3(2)
below realises it with a sequence of 3-valued alternating fields whose masses converge to
`(0, 1/2, 1/2)`, the limit being an exactly binary alternation.

---

## 5. Two corrections to the record

### 5.1 The record's "self-avoidance" (Lemma D) is not established

The record's Theorem D (sprint report §5) states: *let `x` be a density-one point of its own
colour class with `c(x) = i`; then `i notin P_x(e)` for a.e. `e`* — and uses it for the
single-centre orbit constraint `(SIN)`, for Corollary D2, and for "at a.e. point of `Z^3` the
centre colour is in `V`". Its proof reads: "If `D = {e : i in P_x(e)}` has positive measure,
let `e_0` be a density point of `D`. Lemma 5.2(2) gives density zero of `A_i` at
`x + e_0 + v` for every unit `v` nonparallel to `e_0`. Take `v = -e_0 + delta` with
`|delta - e_0| = 1` … Then the set of `delta` on that circle with `x + delta` a density-one
point of `A_i` is conull."

**The gap.** The last sentence is false as used: the conull statement is about `x + delta`
being a density-one point of *its own* class `A_{c(x+delta)}`, and the argument needs
`c(x + delta) = i`. With `x` typical and `c(x) = i`, Lemma 4.3 (density-point properness)
gives `c(x + delta) != i` for a.e. `delta` with `|delta| = 1` — so the set of `delta` for which
`x + delta` is a density-one point of `A_i` meets `{|delta| = 1}` in a null set, and the
argument has nothing to contradict. (Note also
that at a typical point `x` of `A_i` the *endpoint* trace gives `i in P_x(e)` exactly when the
circle about `x` is `i`-coloured on a positive-measure set, which properness forbids; what is
at issue is the *near*-circle part of the palette, i.e. traces with `y_n -> x`, `r_n -> 1`,
which see the colouring at distance `~1` from `x`, not at `x`.)

**What the same argument does prove**, and all that the corrected statements need:

> **Lemma 3 (corrected self-avoidance).** Let `x` be typical for `A_i` and suppose
> `i in P_x(e)` on a set `E` of positive angular measure. Then for a.e. `e in E` that is a
> density point of `E`, and every unit `v` nonparallel to `e`, the class `A_i` has density
> **zero** at `x + e + v`. Hence `A_i` is plane-null on the set
> `Z_E := {x + e + v : e in E° , |v| = 1, v not parallel e}`, which has positive plane
> measure.

*Proof.* The first sentence is literally Lemma 5.2(2), applied at the fixed centre `x` at an
angular density point of `D_{x,i} = {e : i in P_x(e)} >= E`. The second: the map
`(e,v) |-> e + v` from `E° x S` to `R^2` has Jacobian `|sin(arg v - arg e)|`, non-zero off a
product-null set, so the image of the positive-measure set `{(e,v)}` has positive plane
measure. `square`

Lemma 3 is the *tame* case of self-avoidance (if `A_i` agrees a.e. with an open set meeting
`Z_E` in positive measure, we get a contradiction) and it is the statement used by the
record's "at a `k = 6` countermodel the interfaces must be non-tame" line. It is strictly
weaker than Lemma D, and the difference is exactly the "circles are null" phenomenon of §6.

*Consequence for the record.* "At a.e. point of `Z^3` the centre colour lies in `V`"
(`smwfycxze` m4, §10 (R1)) is not available; Theorem 1 does not need it; and the orbit
enumeration of sprint §6 was run *with and without* `(SIN)` with identical counts
(`m2`, accepted), so no number in the record changes. `(TE)` — the fourth independent kill of
the frozen fields — is not affected either: it is `(5.3)` at unit separation, not `(SIN)`.

### 5.2 The direction's equivalence, corrected

See the two numbered corrections after Theorem 1. In one line: the exact statement is
`Z^3(V) = {R_x = O} cap {K_3(V) <= Gamma_x}` (every centre), where `{R_x = O}` reads as the
circle condition *including* the positivity of all three values at every good centre and as
the palette condition otherwise; the centre colour `c(x)` does not enter either form.

---

## 6. Theorem 3: the accumulation is invisible to the per-centre data

### 6.1 Why it should be invisible (the structural statement)

Every constraint at a single centre in this theory is of one of two kinds.

**(A) An angular a.e. statement about the state function `sigma_x` on `S`.** This is the kind
of (5.7), (a), (b), the palette bound `|P_x| <= 3`, (6.2), `m11`'s `sigma{T <= P_x} <= 1/2`,
and the "palette confined to `T`" condition. Such a statement is (i) evaluated on the single
circle `S(x,1)` — or, in its palette form, on the state function at `x` alone — and (ii)
invariant under changing the palette field on angular null sets (and invariant under changing
the colouring on plane-null sets, at every good centre; the colour form is deliberately not
used at exceptional centres, cf. Lemma 1).

**(B) An infinitesimal statement about transition densities at the centre.** This is the kind
of (6.1) — normalised *areas* of transition sets in balls of radius `h -> 0`. Such a statement
is insensitive to the colouring on any null set and says nothing about the circle `S(x,1)`,
which is at distance `1`.

Neither kind links two different centres. The only constraint of the record that does is the
transport **(5.3)/(TE)** — and that is properness in disguise: by `m10` Thm 4 / `m15` Thm C,
`(T) + (5.7) <=> chi(R^2) <= k`. Since `(T)` needs a weak measurable `6`-colouring and its
existence is `chi(R^2) <= 6` (paper Theorem 1.3), **no unconditional model at `k = 6` can
include `(T)`**; so the strongest statement available in this direction is a palette-level
one, and Theorem 3 is optimal in that class.

`(5.3)` at separations tending to `0` degenerates *uniformly* to `(5.7)` (`smwfwi7rh` m7,
Lemma 3, accepted; bound `5d` for `d <= 1/2`). So an accumulating family's inter-centre
transport tends to the single-centre axiom — which is satisfied. This is the precise sense in
which the accumulation is invisible.

### 6.2 The model

Fix `V = {1,2,3}`, `O = T = {4,5,6}`, and the countable centre set

```
   X = {p} u {q} u { x_n = (r_n,0), y_n = (r_n,1) : n >= 1 },  r_n = 1/(10n),
   p = (0,0),  q = (0,1) = p + (0,1).
```

Attach the state function `sigma` (the nine-arc field of §6.3) to `{p} u {x_n}` and
`tau := sigma o gamma` to `{q} u {y_n}`, where `gamma` is the cyclic permutation
`4 -> 6 -> 5 -> 4` of `O`. `sigma` is the step function

```
   sigma(e^{i pi u}) = 4 + ( floor(9u/2) mod 3 ),   u in [0,2) .                  (*)
```

> **Theorem 3.** With `V, O, X, sigma, tau` as above:
> 1. **Unit distances.** The pairs of `X` at distance exactly `1` are exactly `{p,q}` and
>    `{x_n,y_n}` for `n >= 1` (exact rational arithmetic: every squared distance is rational,
>    and it equals `1` only for those pairs). Hence the accumulated family has *two*
>    accumulation points `p` and `q` at mutual distance `1`.
> 2. **The per-centre axioms hold at every centre of `X`.** `sigma` and `tau` are `O`-valued,
>    three-valued, alternating under `R` (`u -> u + 1/3`), with masses exactly
>    `(1/3,1/3,1/3)` each `<= 1/2`; `sigma != tau` pointwise (so the singleton palettes at
>    distance `1` are disjoint, i.e. `(TE)` holds at `{p,q}` and at every `{x_n,y_n}`);
>    `(6.2)` holds trivially (the palettes are inside `O`, disjoint from every edge of
>    `K_3(V)`); and non-proper self-avoidance holds (the three triangle labels are absent from
>    every palette).
> 3. **The accumulation is present**: `x_n -> p`, `y_n -> q`, all centres of `X` carry the
>    `Z^3`-structure `Gamma = K_3(V)`, `R = O` (declared as part of the model, see 6.4).
> 4. **A unit triangle of three `Z^3`-type centres is simultaneously realisable.**  Take the
>    three centres `(0,0)`, `(1,0)`, `(1/2, sqrt 3/2)` (a unit equilateral triangle, checked
>    exactly in `Q(sqrt 3)`) and the three cyclic relabellings of `sigma` as their states.  They
>    are pairwise distinct pointwise, so `(TE)` holds at all three unit pairs, and the three
>    singleton palettes in any common direction are the three distinct labels of `O`: `m9`'s
>    unit-triangle count reads `1+1+1 = 3 <= 6`.  At `k = 5` the same configuration is
>    impossible (`|O| = 2`, and the count is the paper's `2+2+2 > 5` route to binarity), so
>    this is another `k = 6`-specific statement.
> 5. **The degenerate branch (3b) of Theorem 2 is not vacuous.** For each `n` let
>    `sigma^{(n)}` be the mixture field with masses `(eps_n, (1-eps_n)/2, (1-eps_n)/2)`,
>    `eps_n = 2^{-n}` (exact construction in §6.3). Then each `sigma^{(n)}` is `O`-valued,
>    three-valued, alternating, with all masses `<= 1/2`, and
>    `sigma^{(n)} -> sigma^{(inf)}` in `L^1(S)`, where `sigma^{(inf)}` is the two-valued
>    alternation `(5,6,5,6,5,6)` with masses `(0,1/2,1/2)` — exactly the limit configuration
>    of Theorem 2(3b).

*Proof.* Explicit verification, `verify.py` blocks B, C, E, F (1996 checks). The distance
classification is checked twice: numerically in exact rational arithmetic for `N = 40`, and
symbolically in sympy for the whole pattern (`|x_n - y_m|^2 = (r_n - r_m)^2 + 1 = 1 <=> r_n =
r_m`, which never happens for `n != m`; `|x_n - p|^2 = r_n^2 = 1 <=> r_n = 1`, excluded since
`r_n < 1/2`; `|x_n - q|^2 = r_n^2 + 1 > 1`). Alternation, masses and pointwise distinctness
are checked on the exact rational interval partitions (no sampling); the same numbers are
recomputed by an independent route — the per-orbit-position word counts of `sigma` at
rational base points — in block B. `square`

### 6.3 The fields, explicitly

`e^{i pi u}`, `u in [0,2)`; `R` is `u -> u + 1/3`; normalised angular measure is `length/2`.

* `sigma`: nine consecutive arcs of length `2/9`, labels `4,5,6,4,5,6,4,5,6`. Since
  `1/3 = 1.5 · (2/9)`, the shift `u -> u+1/3` always lands in a *different* one of the three
  label classes, so `sigma(u+1/3) != sigma(u)` a.e.; the classes have length `6/9 = 2/3` each,
  i.e. mass `1/3`. (`sigma` is `R^2`-invariant; the unit-distance directions on a circle are
  the `R`-increments only, `|1 - R| = 1`, `|1 - R^2| = sqrt 3`, `|1 - R^3| = 2`, so the
  `R^2`-invariance violates nothing.)
* `tau = sigma o gamma`: same facts, and `tau(e) != sigma(e)` everywhere.
* The mixture family: on the fundamental domain `[0,1/3)` of the `R`-action place the three
  two-valued orbit words `(4,5,4,5,4,5)`, `(4,6,4,6,4,6)`, `(5,6,5,6,5,6)` on subintervals of
  lengths `d_A = (t_4+t_5-t_6)/3`, `d_B = (t_4+t_6-t_5)/3`, `d_C = (t_5+t_6-t_4)/3`, and
  extend by the words along the `R`-orbit. Then the mass of label `i` is `t_i` exactly
  (each word uses two labels three times each, so `|{sigma = 4}| = 3(d_A+d_B) = 2t_4`), the
  field alternates (each word is a proper colouring of the six-cycle of `R`-positions), and
  `t_i <= 1/2` is exactly the condition `d_A,d_B,d_C >= 0`. So the achievable mass vectors at
  a `k = 6` three-valued triangle centre are exactly `{t_i <= 1/2, sum t_i = 1}` — the
  content of `(5.7)` plus `m11`'s bound, as in `smwfycxze` m4's block D6, re-derived here.

### 6.4 What the model does not claim, and what it therefore proves

The model provides the *palette data* (the state function at each centre) and declares the
*transition data* `Gamma_x = K_3(V)`. It does not produce a colouring `c` on the plane, and it
cannot: by the paper's Theorem 1.3 a weak measurable `6`-colouring exists iff
`chi(R^2) <= 6`, and `(T)` + `(5.7)` at all centres is equivalent to properness
(`m10`/`m15`). It also does not claim `(5.2)` in its colouring form: checking (5.2) needs the
induced colouring on the plane, and producing one is again `chi(R^2) <= 6`. Thus the model is
a statement about the axioms *restricted to the centres at which they are evaluated* — here
the family `X` — which is exactly the locality level at which the record's `(W)`-arguments
live. If the axioms are imposed at *all* centres of the plane, the system contains
`(T)+(5.7)`, i.e. properness, and is satisfiable iff `chi(R^2) <= 6`; that is the wall, not a
gap in the model.

What it proves is the negative statement the direction asks for: **the accumulated constraint
system consisting of** the single-centre axioms at every centre of the family — `(5.7)`,
palette bound, `(6.2)`, `m11`'s `1/2` bound, three-valuedness with prescribed masses, the
"palette confined to `T`" condition — **together with the unit-separation transport `(TE)`
between all pairs of the family at distance exactly `1`, and together with the accumulation
itself, is satisfiable, in both branches of Theorem 2(3)**. Since every one of these is a
statement of kind (A) or (B) of §6.1, and kinds (A), (B) cannot link different centres except
through `(TE)`, no argument built from them *at any countable set of centres* can exclude an
accumulation of `Z^3(V)` at `k = 6` (the general locality statement is direction `d3`'s; here
it is verified on the accumulated family itself). Any proof of `(Sep3)` at `k = 6` must use the
colouring at uncountably many centres, i.e. `(T)`, i.e. `chi(R^2) <= 6`.

**Against the record's explicit single-centre list.** The sprint's orbit system uses five
single-centre conditions (sprint report §6): (1) `c(x) notin P_x(e)` a.e., (2) `(5.7)`,
(3) `|P_x(e)| = 3 => |P_x(Re)| <= 2`, (4) a singleton palette is never inside the label set of
a simple cycle of `Gamma_x` (Lemma 6.2), (5) two palettes `120` degrees apart with total size
`5` have a monochromatic unit sum. With singleton palettes, (1) holds with the declared centre
colour `1 in V`, (2) is the alternation, (3) and (5) are vacuous, and (4) is the inclusion
`P_x <= O` (`V` is exactly the vertex set of the declared cycle). `m11`'s `1/2` bound and the
complementary-triple exclusion also hold — and `m2`'s accepted check shows that (1), (3), (5)
and the five extra conditions cut nothing anyway. Two constraints of the record are *not*
evaluable in the model because they mention the colouring or a second circle: `(5.2)` (it
involves `c(x+e+v)`) and `m7`'s `|P_x(e)| + |Col(S(x+e,1))| <= k` (it involves the labels on
the circle about `x+e`). Both are absent for the reason in §6.4: they are colouring-level.

**Vacuity tests.** (i) The class is not empty: the model above; and at a single centre
`m13`'s singleton field is an independent witness. (ii) The `k = 5` calibration: at `k = 5`
the same system (`|O| = 2`) admits only the two alternations (verified, block A), so
`R_x = O` is binarity, Lemma 5.5 applies and the triangle locus is locally finite — the
paper's result reappears as the `|O| = 2` case. (iii) The non-degenerate branch of
Theorem 2(3a) is realised by a *genuine* colouring at `k = 7`: in `m3`'s accepted proper
measurable `7`-colouring the centres `q_n` have `Gamma = K_3({0,2,3})` exactly (sharpened by
`smwfycxze` m4 Thm 1) and `R_{q_n} = {1,4,5,6}` of size `4 = 7 - 3`, so `q_n in Z^4(V)`; they
accumulate at `p_0`, which itself has `R_{p_0} = {1,4,5,6}` (the record: "the unit circle
about `p_0` meets exactly `4 = k-3` colours"). So `Z^4(V)` accumulates at a point of
`Z^4(V)` with all four masses positive, exactly as Theorem 2(3a) predicts, and no
contradiction arises. This is the sharpest available confirmation that Theorem 1's
reformulation describes real colourings, not just palette fields.

---

## 7. What a proof of `(Sep3)` at `k = 6` still needs, exactly

By Theorem 2(3a), an accumulation of `Z^3(V)` is **self-similar**: if `x_n in Z^3(V)` are
distinct with `x_n -> p` and no state mass collapses, then `p in Z^3(V)` itself, with the same
triangle `V`, with `Gamma_p = K_3(V)` exactly, and with the state function of `p` equal to the
`L^1` limit of the states at `x_n`. The records of the approximants and of the limit agree on
every quantity the theory defines at a centre. By Theorem 3 that whole configuration —
including the unit-separation transport between the centres of the family — is consistent.
By §6.1 every constraint available at one centre at a time is of kind (A) (angular a.e. on
the circle, a plane-null set) or (B) (infinitesimal transition density at the centre); neither
kind relates two circles, and the only axiom that does relate them, `(5.3)` at unit separation,
degenerates uniformly to `(5.7)` as the separation tends to `0` (`smwfwi7rh` m7 Lemma 3), which
the limit already satisfies. So:

> **(Sep3) at `k = 6`, sharp form.** `Z^3(V)` is locally finite iff no point of `Z^3(V)` is a
> limit of distinct points of `Z^3(V)`. The local structure of such a self-similar point is
> completely described by Theorem 2 and is consistent with every per-centre axiom and with the
> unit-separation transport (Theorem 3). Consequently a proof must use a constraint that is
> not of the form (A) or (B) evaluated at countably many centres — the only such constraint in
> the theory is the full transport `(5.3)`, equivalently `(T)+(5.7)`, equivalently the
> existence of the weak measurable `6`-colouring (`chi(R^2) <= 6`).

This is the decided form of the direction's alternative "prove that none is derivable": the
obstruction is exhibited (Theorem 3 and §6.1), not merely asserted. It also states exactly the
remaining freedom: a proof of `(Sep3)` at `k = 6` must be a proof that uses the colouring at
uncountably many centres in an essential way, i.e. it must be a genuine chromatic argument —
which is the record's §5c conclusion, here with the accumulation case decided rather than
assumed.

## 8. Reproduction, and what was checked how

```
   cd .ultramath/smwg1r9lg/m6 && python3 verify.py      # 1958 checks, exit 0
```

Blocks: **A** alternation words on the `R`-orbit (`66` proper `3`-words, `60` genuinely
three-valued, orbits `[6,18,36]`, `k = 5`: exactly `2`; counts produced twice, by brute force
and by the chromatic polynomial `(k-1)^n + (-1)^n (k-1)` plus inclusion–exclusion);
**B** the fields `sigma, tau` and the mixture family (masses, alternation and pointwise
distinctness on exact rational partitions, plus an independent recount from the orbit words);
**C** the family `X` (exact unit-distance classification, `(TE)` at all `41` unit pairs,
accumulation, the degenerate `L^1` limit); **D** the combinatorial core of Theorem 1 for all
`20` triples `V` and the `k = 5/6/7` calibration; **E** the constraint list of Theorem 3 item
by item, and a symbolic (sympy) check of the distance pattern; **F** the unit-triangle
configuration of three `Z^3`-type centres in `Q(sqrt 3)`, and the `k = 7` orbit count `732`
(the `k`-calibration of block A).

**Lean check.** `lean/d2_core.lean` machine-checks the combinatorial core on the
pinned toolchain (`source scripts/env4341.sh; cd .ultramath/smwg1r9lg/m6/lean; lean d2_core.lean`)
and on the default one: the alternation counts `66`, `60`, `2`, the graph-theoretic core of
Theorem 1 (`D2.core`: a graph containing `K_3(V)` with all edges inside `V` *is* `K_3(V)`) and
`|O| = 3`. All five declarations depend only on `[propext, Classical.choice, Quot.sound]`
(commands and output in `lean/OUT.txt`, exit `0` on both toolchains). The two
counting-shape statements (no label on more than half the orbit, and the occurrence of the
`3+2+1` pattern as well as `2+2+2`) are decided in `verify.py` block A only: their `decide`
proofs in Lean are dominated by typeclass search in the nested `Finset.filter` terms.

**Paper formulas.** (5.1), (5.2), (5.3), (5.7), Definition 5.1, Definition 6.1 (6.1),
Lemma 6.2 (6.2) and the closedness remark after (6.1) were extracted with `pdftotext -layout`
and independently with `pdftotext -raw` (pp. 26–30, 34–35) and their positions checked with
`pdftotext -bbox-layout`; a `pdftoppm` render of p. 35 was produced. No OCR is installed in
this VM, so the render was not machine-read: the check is two independent text extractions
plus the bounding-box positions, not a visual one. One extraction artefact is worth recording:
in (6.1) the numerator `|D_{ij}(B,h)|` loses its bars in both extraction modes (the bars are
rendered as thin rules), so the display reads `D_{ij}(B,h)/|h|`; the definition only makes
sense with the area bars, which the surrounding text ("vertical bars on a plane set denote
Lebesgue area", "the normalization by `|h|`") forces. This does not affect any statement
above, which uses only the truth value of (6.1).

**Files not touched.** Only this directory. `lean/OAI/`, `results/`, `scripts/`, `sprint/`
and every other `.ultramath` member directory are read-only for this run and were not
modified.
