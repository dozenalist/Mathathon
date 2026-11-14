# The `S_1` accumulation theorem at six colours

**Member `m4`, swarm `smwg1r9lg`, direction `d2`** — the singleton-class reformulation of the
three-valued triangle locus and the accumulation argument it enables.

*Revision 2 (after the first submission's rejection).* The first version of Theorem 3(ii) claimed
"in particular `E_O` has empty interior". That implication is **false**: a set can contain a ball
`B_r(z)` with `r <= 1` and still be nowhere conull in a ball of radius `> 1`. The clause is deleted
everywhere; Theorem 3 now states exactly what is proved (no ball of radius `> 1` is contained in
`E_O`), and the new part (iii) records why the method cannot reach smaller balls. Nothing else in
the note changed mathematically.

**Deliverable.** (i) The `S_1` dictionary, exactly (Theorem 1, both directions, with the
a.e.-statements and the failure of each direction separately). (ii) The **accumulation theorem**
(Theorem 2): what is forced at a limit point of the three-valued triangle locus, proved with no
gap, including a full proof of the state-continuity lemma that the record (`smwfycxze/m4` §10
Lemma C) carries as "sketch-quality". (iii) A new **circle-thinness theorem** (Theorem 3) obtained
from a Fubini identity: for *every* label set `O` with `|O| >= 2`, the locus `E_O` of centres whose
unit circle carries exactly the labels of `O` is not conull in any ball of radius `> 1` (hence
contains no ball of radius `> 1`; nothing is claimed about smaller balls), and at a.e. of its own
points its own unit circle is essentially disjoint from it.
(iv) The **exact finite decision** of the pointwise limit system (66 words, 60 genuinely
three-valued, and the two-valued solutions are *forced* to be the rigid alternation, so a
degenerate limit has state measures exactly `(1/2,1/2,0)`), with two independent procedures, the
`k = 5` / `k = 7` calibrations, and a machine-checked core (`orbit_core.lean`, Lean 4.34.1, axioms
`[propext, Classical.choice, Quot.sound]`).

**What is not claimed:** `(W)` at `k = 6` is not decided; no countermodel is built; and every
`k = 6` statement here is *conditional on `chi(R^2) <= 6`*, exactly as every `k = 6` statement in
the record. §6 states precisely what remains.

---

## 1. Setting, and the facts taken from the paper and the record

`c : R^2 -> I := [k] = {1,...,k}` is **weak measurable**: every class `A_i = c^{-1}(i)` is
Lebesgue measurable. `S = S^1` carries normalised angular measure `sigma`; `R` is rotation of
directions by `kappa = pi/3`; a *centre* is a point `x in R^2`; a *direction* is an element of `S`.
`P_x(e)` is the maximal palette of paper Definition 5.1 (the essential union over circle traces
`b in W_x` of `{b_i > 0}`), `Gamma_x` the transition graph of Definition 6.1 (edges `ij` with
`limsup_{h->0} |D_{ij}(B,h)|/|h| > 0` for every ball `B` about `x`), and
`L = {x : Gamma_x contains a cycle}`. A point is **typical** if it is a density-one point of its own
class; typical points are conull (paper Lemma 4.3).

**Class `S_1`** (`smwfycxze/m4`). For **every** centre `x`, `P_x(e)` is a singleton for `sigma`-a.e.
`e`. Write
```
    P_x(e) = { sigma_x(e) },      R_x = { i : sigma{e : sigma_x(e) = i} > 0 },      (1.1)
    nu_x(i) = sigma{ e : sigma_x(e) = i }   (a probability vector on I).
```
`S_1` contains every colouring constant on the cells of a locally finite Borel partition with
piecewise `C^1` boundaries, and `m3`'s `k >= 7` countermodel.

**Quoted, not re-derived.**
* **(T) endpoint trace** (`smwfwi7rh/m10` Lemma 1, from Definition 5.1): for **every** centre `x`
  and `sigma`-a.e. `e`, `c(x+e) in P_x(e)`.
* **(SA) self-avoidance** (`smwfwi7rh/m10` Lemma 2 = report Lemma D): for a.e. `x in R^2` and
  `sigma`-a.e. `e`, `c(x) notin P_x(e)`.
* **(6.2)** (paper Lemma 6.2): if `ij in Gamma_x` then `P_x(e)` is **not** contained in `{i,j}` for
  `sigma`-a.e. `e`.
* **(5.7)** (paper Corollary 5.4): `P_x(f) cap P_x(Rf) = empty` for a.e. `f`.
* **(5.2)** (paper Lemma 5.2(1)): `c(x+e+v) notin P_x(e) union P_x(v)` for a.e. `(e,v)`.
* **Closure of edge loci** (paper §6.1): for each pair `ij`, `{x : ij in Gamma_x}` is closed.
* **(5.1)** (paper, after Definition 5.1): `x_n -> x`, `b_n in W_{x_n}`, `b_n` weak-* `-> b`
  implies `b in W_x`.
* **`(W)`** is `L cap B(y,R)` finite for some `R > 1`; **`Z^3`** is the three-valued triangle locus
  of `smwfycxze/m4` §6, restated in (2.3) below.

Everything below is an a.e.-statement in the direction variable at a *fixed* centre unless the
centre itself is quantified; null sets may depend on the centre, exactly as in the paper (no joint
measurability in the centre is used anywhere).

---

## 2. Theorem 1 — the `S_1` dictionary

Fix `k = 6`, a weak measurable 6-colouring in `S_1`, a 3-element set `V ⊆ I` and `O := I \ V`
(so `|O| = 3`). Write `K_3(V)` for the triangle on `V`.

> **Theorem 1.** Let `x` be any centre.
>
> **(a) Edges avoid the essential range.** If `ij in Gamma_x` then `sigma_x(e) notin {i,j}` for
> a.e. `e`; hence `R_x cap {i,j} = empty`, and `|R_x| >= 2`.
>
> **(b) Confinement and the dichotomy.** If `Gamma_x supseteq K_3(V)` then
> ```
>     R_x <= O,        P_x(e) = {sigma_x(e)} <= O  a.e.,        |R_x| in {2,3},
> ```
> and
> ```
>     |R_x| = 3   <=>   R_x = O   ==>   Gamma_x = K_3(V) exactly.
> ```
> The last implication is not an equivalence: with `|R_x| = 2` the graph `Gamma_x` may or may not
> equal `K_3(V)` (all that is forced is that its edges avoid `R_x`, so that they live on `V` plus
> the third element of `O`). In the case `|R_x| = 3` therefore `Gamma_x = K_3(V)`, so `Gamma_x` has
> exactly one cycle, of length `3` and vertex set `V`.
>
> **(c) The dictionary map.** For every centre `x` and every label `i`,
> ```
>     sigma{ e : sigma_x(e) = i } = sigma{ e : c(x+e) = i },                        (2.1)
> ```
> so the state measure `nu_x` *is* the angular law of the colouring on the unit circle `x + S`, and
> `R_x` *is* the set of labels carried by that circle with positive angular measure.
>
> **(d) The centre's own colour.** For a.e. `x in Z^3_V` (see (2.3)): `c(x) in V`. For a.e. `x` in
> the **binary** part of the triangle locus for `V`: `c(x) notin R_x` (so the centre's colour is not
> one of the two state labels; it is the third element of `O` or an element of `V`).
>
> **(e) Both hypotheses are needed.** The circle condition in (f) below does *not* by itself give a
> cycle (witness in §5.4), and `Gamma_x supseteq K_3(V)` does *not* by itself give `|R_x| = 3`
> (the binary alternative).
>
> **(f) Resulting characterisation.** For **every** centre `x` (both directions use only (2.1) and
> (b), which hold at every centre):
> ```
>     x in Z^3_V   <=>   Gamma_x supseteq K_3(V)  and  the circle x + S carries exactly the
>                        three labels of O, each on a set of positive angular measure.        (2.2)
> ```

*Proof.* (a) is `smwfycxze/m4` Lemma A: (6.2) gives `P_x(e) notsubseteq {i,j}`; in `S_1` that is
`sigma_x(e) notin {i,j}`, and if `sigma_x = i` on a set of positive measure then `P_x(e) = {i}` is
contained in `{i,j}` there, contradiction; the same for `j`; so `R_x cap {i,j} = empty`. `|R_x| >= 2`
is Lemma B there: `R_x != empty` and `R_x = {i}` would force `sigma_x = i` a.e., contradicting
(5.7), which reads `sigma_x(e) != sigma_x(Re)` a.e.

(b) Every vertex of `K_3(V)` is an endpoint of an edge of `Gamma_x`, so (a) removes `V` from `R_x`;
`R_x != empty` and `R_x <= O` give `|R_x| in {2,3}`. If `|R_x| = 3` then `R_x = O`: then every edge
of `Gamma_x` has both endpoints outside `O` by (a), i.e. inside `V`, so
`Gamma_x <= K_3(V) <= Gamma_x`, i.e. `Gamma_x = K_3(V)`. The converse fails in the binary case:
`|R_x| = 2` forces only that `R_x` is a two-element subset of `O`, and (6.2) then excludes just
those two labels as edge endpoints, so `Gamma_x` may still be `K_3(V)` (on `V`, plus possibly edges
to the third element of `O`).

(c) (T) says `c(x+e) in P_x(e) = {sigma_x(e)}`, i.e. `c(x+e) = sigma_x(e)` a.e.; the two sets in
(2.1) are therefore equal up to a null set.

(d) Let `x in Z^3_V` be typical (a.e. point of the set is). Then `P_x(e) <= O` by (b), `R_x = O`,
and (SA) gives `c(x) notin P_x(e) = {sigma_x(e)}` for a.e. `e`, i.e. `c(x) != sigma_x(e)` a.e.;
since each element of `O` equals `sigma_x` on a set of positive measure, `c(x) notin O`, i.e.
`c(x) in V`. If `x` is a typical point of the binary part of the triangle locus, the same argument
with `R_x` in place of `O` gives `c(x) notin R_x`; and `c(x) in I = V union O` leaves the third
element of `O` and the elements of `V` as the possibilities, so nothing sharper is forced.

(e) is proved by the two witnesses collected in §5.4.

(f) is (b)+(c). `square`

**Remark 1.** (2.2) is the exact "dictionary" the direction asks for: in `S_1` a genuinely
three-valued triangle centre is a centre whose *unit circle* sees exactly the three complementary
labels — nothing more, nothing less — **provided** the transition graph already contains the
triangle. The circle data alone is provably insufficient (§5.4), and this is exactly why the
three-valued locus cannot be attacked by `(5.2)`-density arguments: at such a centre the palette is
confined to `O = [k] \ V` and no label of `V` is ever excludable at a sum point (`smwfycxze/m4`
Theorem 6).

---

## 3. Theorem 2 — the accumulation theorem

Throughout: `k = 6`, `c` weak measurable in `S_1`, `V` a 3-element set, `O = I \ V`, and
```
    Z^3_V := { x in R^2 : Gamma_x = K_3(V) and R_x = O }.                                  (2.3)
```
`Z^3 = union_V Z^3_V` over the `20` triples is the locus of `smwfycxze/m4` Theorem 5, and
`(W)` (equivalently local finiteness of `L`) is local finiteness of `Z^3` there.

> **Theorem 2 (accumulation at a three-valued triangle centre).** Let `x_n in Z^3_V` be distinct
> points with `x_n -> p in R^2`. Then:
>
> **(a) The cycle survives.** `Gamma_p supseteq K_3(V)`. In particular `p in L`, no cycle length
> and no triple is lost in the limit, and every ball about `p` meets `A_i` for every `i in V`.
>
> **(b) The palette at the limit is confined to `O`.** `P_p(e) <= O` for `sigma`-a.e. `e`; hence
> `c(p+e) in O` a.e.: the unit circle about `p` is carried by the *same* complementary triple `O`.
>
> **(c) State continuity.** `sigma_{x_n} -> sigma_p` in `L^1(S)` and `nu_{x_n} -> nu_p` in
> `l^1(O)`; both limits are unique, no subsequence is needed.
>
> **(d) The dichotomy.** Let `(m_a, m_b, m_c) = nu_p` on `O`. Then exactly one of the following
> holds.
>   * **(i) Non-degenerate:** `min(m_a,m_b,m_c) > 0`. Then `R_p = O`, `Gamma_p = K_3(V)`, i.e.
>     `p in Z^3_V`: the accumulation point of `Z^3_V` is itself in `Z^3_V`, with the *same* `V`.
>   * **(ii) Degenerate:** `nu_p = (0, 1/2, 1/2)` up to order. Then `p` is **binary** for the pair
>     of positive states, `sigma_p` is the **rigid alternation** (each class of angular measure
>     exactly `1/2`, `sigma_p(f) != sigma_p(Rf)` a.e., `R` exchanges the classes), and `p` is
>     `delta_*`-separated from every other centre binary for the same pair (paper Lemma 5.5).
>
> **(e) Self-similarity of the non-degenerate case.** In case (i), the whole structure repeats: `p`
> satisfies every hypothesis of Theorem 1 with the same `V`, `O`; in particular `c(p) in V` if `p`
> is typical, and the unit circle about `p` is `O`-carried with all three states of positive
> measure.

*Proof.* **(a)** For each edge `ij` of `K_3(V)` we have `ij in Gamma_{x_n}` for all `n`, and the
edge-presence locus is closed (paper §6.1: "for each fixed pair `ij`, its edge-presence locus is
closed"), so `ij in Gamma_p`. `p in L` is immediate. Since `ij in Gamma_p` gives `p in H_i cap H_j`
(paper, right after Definition 6.1), every ball about `p` meets every `A_i`, `i in V`.

**(c)** Fix the three edges of `K_3(V)`. For each `n` and each such edge `ij`, Lemma 6.2 gives a
trace `b^{n,ij} in W_{x_n}` with `b^{n,ij}_i = b^{n,ij}_j = 0` a.e. In `S_1` at `x_n` every trace is
supported in `P_{x_n} = {sigma_{x_n}}`, so a nonnegative trace summing to one and supported in a
singleton is that singleton's indicator:
```
    b^{n,ij} = e_{sigma_{x_n}}   a.e.                                                    (3.1)
```
in particular the three edges give the *same* trace. The `L^infty(S;R^6)`-norm of `e_{sigma_{x_n}}`
is `1`, so (bounded ball weak-* compact, `L^1(S)` separable) some subsequence converges weak-* to
some `b`. By (5.1) (closure under varying centres, with `x_n -> p`) `b in W_p`. Every trace at `p` has
its positive coordinates inside the palette (paper, after Definition 5.1), and `P_p = {sigma_p}`
a.e. (that `P_p` is a singleton a.e. is the hypothesis `S_1` *at the centre `p`*; its essential
range is used only through (b) below), so `b` is supported in `{sigma_p}`; being nonnegative with
`sum_i b_i = 1` a.e. and `sigma_p` measurable, `b = e_{sigma_p}` a.e. Hence the limit is
*independent of the subsequence*, so the whole sequence converges weak-* to `e_{sigma_p}`, and then
```
    int | e_{sigma_{x_n}} - e_{sigma_p} | dsigma
      = int e_{sigma_{x_n}} + int e_{sigma_p} - 2 int e_{sigma_{x_n}} e_{sigma_p}
      -> 1 + 1 - 2 = 0,
```
because `int e_{sigma_{x_n}} = 1`, `int e_{sigma_p} = 1`, and
`int e_{sigma_{x_n}} e_{sigma_p} = int e_{sigma_{x_n}}[sigma_p] -> int e_{sigma_p}[sigma_p] = 1`
by weak-* convergence tested against the fixed bounded function `e_{sigma_p}`. So
`sigma_{x_n} -> sigma_p` in `L^1`, and `nu_{x_n} -> nu_p` in `l^1` because
`nu_{x_n}(i) - nu_p(i) = int (e_{sigma_{x_n}} - e_{sigma_p})[i]`.

**(b)** By (a), `K_3(V) <= Gamma_p`; by (6.2) at the centre `p`, for each edge `ij` of `K_3(V)`,
`P_p(e) notsubseteq {i,j}` a.e. Since `P_p(e) = {sigma_p(e)}`, we get `sigma_p(e) notin {i,j}` a.e.
for the three edges, i.e. `sigma_p(e) notin V` a.e., i.e. `sigma_p(e) in O` a.e.; so
`P_p(e) <= O` a.e. Then (T) at `p` gives `c(p+e) in P_p(e) <= O` a.e.

**(d)** By (c), `nu_p` is a probability vector on `O` (support in `O` by (b)). `R_p = {i : nu_p(i) > 0}`
satisfies `|R_p| >= 2`: `R_p != empty` and `|R_p| = 1` would give `sigma_p = i` a.e. for a single
`i`, contradicting (5.7) at the centre `p`, which reads `sigma_p(f) != sigma_p(Rf)` a.e. So
`|R_p| in {2,3}`.

If `|R_p| = 3` then `R_p = O`, and (a) gives `Gamma_p supseteq K_3(V)` while (6.2)+(b) give
`Gamma_p <= K_3(V)` (every edge endpoint avoids `O`), so `Gamma_p = K_3(V)` and `p in Z^3_V`.

If `|R_p| = 2`, say `R_p = {a,b}`, then (5.7) at `p` reads: the two sets `{sigma_p(f)}` and
`{sigma_p(Rf)}` are disjoint subsets of `{a,b}`, hence the two *different* singletons a.e.; so
`sigma_p(Rf) != sigma_p(f)` a.e. and `R` exchanges the classes `{sigma_p = a}`, `{sigma_p = b}`.
`R` preserves `sigma`, so both classes have measure `1/2`; `nu_p = (0,1/2,1/2)` on `O` up to order.
That `p` is binary for `{a,b}` in the paper's sense (`P_p(e) cap {a,b} != empty` a.e.) is
immediate, and paper Lemma 5.5 applies verbatim.

**(e)** is Theorem 1 with `x = p`, using (a)-(d)(i) and (T) at `p`. `square`

**Remarks.**
1. Theorem 2 is exactly the "decided statement about the accumulation" the direction asks for: the
   limit of a sequence of three-valued triangle centres is either a three-valued triangle centre
   with the *same* cycle triple, or a *rigid* binary centre in which the state measures are pinned
   to `(1/2,1/2,0)` and the state function is the unique (up to rotation) alternating two-colouring
   of the circle. Nothing else can happen; in particular no cycle length other than `3` and no
   other triple can appear.
2. The degenerate case is not excluded by any printed hypothesis; it is exactly the *binary*
   locus, which is locally finite by Lemma 5.5. So the accumulation can only be invisible if it
   stays in case (i), and then it is a limit of objects of the same kind — statement (e).
3. Part (b) is where the accumulation pays: the palette at the *limit* is confined to the same
   `O`. That is a genuinely new constraint at `p`, and it is what makes Theorem 3 possible.

---

## 4. Theorem 3 — circle-thinness of the state loci (new)

Write `|.|` for plane Lebesgue measure and, for a plane set `E` and a point `y`,
```
    g_E(y) := sigma( d B(y,1) cap E )
```
for the angular measure of the part of the unit circle about `y` that lies in `E`. For `O ⊆ I` with
`|O| >= 2` put
```
    E_O := { x in R^2 : R_x = O },
```
the locus of centres whose unit circle carries *exactly* the labels of `O`, each with positive
angular measure (Theorem 1(c)). Note `Z^3_V ⊆ E_O` for `O = I \ V`, and `E_O` is defined without
any reference to `Gamma_x`: the theorem below does **not** need a cycle.

> **Theorem 3.** Let `O ⊆ I` with `|O| >= 2` and let `E ⊆ E_O` be measurable. Then
> ```
>     int_{R^2}  1{ c(y) notin O } . g_E(y)  dy  =  0 ,                                  (4.1)
> ```
> and consequently:
>
> **(i)** for a.e. `y` with `c(y) notin O`, the unit circle about `y` meets `E` in angular
> measure zero. In particular, taking `E = E_O`: for a.e. `x in E_O` the unit circle about `x` is
> essentially disjoint from `E_O`;
>
> **(ii)** `E_O` is **not conull in any ball of radius `> 1`**; consequently no ball of radius
> `> 1` is contained in `E_O`, and every ball of radius `> 1` contains a set of positive measure
> disjoint from `E`. `Z^3_V` inherits all of this.
>
> **(iii) What (ii) does *not* say, and cannot be made to say.** It does not give `int E_O = empty`:
> a set may contain a ball `B_r(z)` with `r <= 1` and still be nowhere conull in a ball of radius
> `> 1`. The proof of (ii) needs the whole ball `B(p,rho)`, `rho > 1`, to compute `g_{E_O}` on the
> inner ball `B(p, rho-1)`; against a *contained* ball `B_r(z)`, `r <= 1`, the circle `d B(y,1)`
> never lies inside `B_r(z)`, so (4.1) yields nothing. Correspondingly, (4.1) constrains
> `{c notin O}` only through the weight `g_{E_O}`: it says the two are essentially disjoint, not
> that `{c notin O}` is large anywhere.

*Proof.* For `x in E ⊆ E_O` we have `R_x = O`, hence `P_x(e) = {sigma_x(e)} ⊆ O` a.e., hence by (T)
```
    c(x+e) in P_x(e) <= O    for a.e. e in S.                                          (4.2)
```
Therefore
```
  0 = int_E int_S 1{ c(x+e) notin O } dsigma(e) dx
    = int_S int_E 1{ c(x+e) notin O } dx dsigma(e)            (Tonelli, integrand >= 0)
    = int_S int_{E - e} 1{ c(y) notin O } dy dsigma(e)        (y = x + e, translation invariance)
    = int_{R^2} 1{ c(y) notin O } . sigma{ e : y - e in E } dy     (Tonelli again)
    = int_{R^2} 1{ c(y) notin O } . g_E(y) dy ,
```
because as `e` runs over `S` the points `y - e` run over the circle of radius one about `y`, and
`y - e in E <=> y in E + e`; the angular measure of `{e : y - e in E}` equals `g_E(y)` since
`e |-> -e` preserves `sigma`. This is (4.1).

**Preliminary.** By (SA), at a.e. `x in E_O` we have `c(x) notin P_x(e) = {sigma_x(e)}` for a.e.
`e`, and `sigma_x` takes every value of `R_x = O` on a set of positive measure, so `c(x) notin O`.
Hence `{c notin O} ∩ E_O` is conull in `E_O`.

(i) By (4.1), `g_E = 0` a.e. on `{c notin O}`; applied with `E = E_O` and combined with the
preliminary, `g_{E_O}(x) = 0` for a.e. `x in E_O`.

(ii) Suppose now that `E_O` is conull in a ball `B(p,rho)` with `rho > 1`, and let
`B' := B(p, rho - 1)` (nonempty open). For `y in B'` we have `|y - p| < rho - 1`, so every point of
`d B(y,1)` is at distance `< rho` from `p`, i.e. `d B(y,1) <= B(p,rho)`; since `E_O` is conull in
`B(p,rho)` and `e |-> y + e` is an isometry of `S` onto `d B(y,1)` (a `C^1` curve), the preimage of
the null complement is `sigma`-null, so `g_{E_O}(y) = 1`. Therefore
```
    int 1{ c(y) notin O } g_{E_O}(y) dy  >=  |B' cap E_O|  =  |B'|  >  0 ,
```
contradicting (4.1). So no such ball exists: a conull subset of a ball of radius `> 1` is
impossible, hence no ball of radius `> 1` is contained in `E_O`. (Nothing here forbids a contained
ball of radius `<= 1`; see (iii).) `square`

**Remarks.**
1. *The mechanism.* (4.1) is the exact form of the intuition "the constraints are a.e.-on-circles at
   countably many centres": the map `(x,e) |-> x + e` pushes `dx (x) dsigma` to Lebesgue measure
   (`int_S int_E f(x+e) dx dsigma(e) = int_{R^2} f(y) g_E(y) dy`), so a circle-fibre hypothesis on
   `E` controls the plane only through the absolutely continuous aggregate `g_E`. The identity is
   available at *every* `O` with `|O| >= 2` and needs only `(T)` and `(SA)`.
2. *Content and sharpness.* The substance is (ii), not (4.1) (an identity). Conceptually: at every
   centre of `E_O` the *circle* is carried by `O`, while by (SA) the *centre itself* carries a label
   of `V = I \ O`; the pushforward computation says that a ball's worth of such centres would force
   the `V`-labels to be circle-averaged away, which is impossible. Quantitatively, (ii) is exactly
   the statement that this averaging cannot be beaten. The threshold `1` is *optimal for the
   method*: (4.1) sees only circles of radius exactly one (that is the radius at which the palette
   is defined), so nothing below `1` is reachable this way — and `1` is also the constant of `(W)`,
   which asks for a ball of radius `> 1`.
   What (4.1) does **not** forbid: `E_O` null, countable, sparse, Cantor-type, or dense. A
   *ball-conull* locus is the only thing excluded, which is precisely why the identity does not
   decide `(W)`.
3. *Vacua.* At `k = 5` the relevant loci are locally finite (`k - ell = 2` forces binarity) or
   empty, so the theorem is satisfied trivially — as any correct `k = 6`-specific statement must be.
   In the tame class the same. The first non-vacuous instance in the record is `m3`'s `k >= 7`
   colouring, whose accumulating triangle points have `|R_x| = 4 = k - 3`: the locus `E_O` with
   `|O| = 4` is closed and countable with one accumulation point, hence not ball-conull and
   contains no ball at all, and (4.1) holds — consistent.
4. *What it does not do.* (4.1) does not make `E_O` null, discrete or locally finite: a Cantor-type
   or a sparse positive-measure locus satisfies every conclusion. So it is a constraint on
   `Z^3_V`, not a decision of `(W)`.

## 5. The pointwise orbit system, the finite decision, and calibrations

### 5.1 The rules on one `R`-orbit, and a small correction

At a centre `x` with `Gamma_x = K_3(V)` and `R_x = O` (`|O| = 3`), Theorem 1(b) gives
`sigma_x(e) in O` a.e. Evaluated on one `R`-orbit `{e, Re, ..., R^5 e}`, the printed axioms give
```
  (P1)  sigma_x(R e) != sigma_x(e)                          -- (5.7) at x, at each orbit position
  (P2)  sigma_x(R e) notin { sigma_x(e), sigma_x(R^2 e) }   -- (5.2) at x, pair (e, R^2 e)
```
(P2) is legitimate: `e + R^2 e = R e` **exactly** (`|e| = |R^2 e| = 1`, `|Re| = 1`; checked in
`Q(sqrt 3)` in §5.3), so the sum point `x + e + R^2 e = x + Re` is the *circle* point in direction
`Re`, whose colour is `sigma_x(Re)` by Theorem 1(c).

> **Observation 5.0.** On the orbit, (P2) is *equivalent* to (P1): `sigma_x(Re) notin
> {sigma_x(e), sigma_x(R^2e)}` says exactly `sigma_x(Re) != sigma_x(e)` (which is (P1) at position
> `0`) and `sigma_x(Re) != sigma_x(R^2 e)` (which is (P1) at position `1`). So `(5.2)` at the
> `120^circ` pairs adds **nothing** to `(5.7)` on the `R`-orbit, and the whole orbit content of the
> single-centre axioms is

> ```
>     the state function is a proper colouring of the 6-cycle  C_6.                      (5.0)
> ```

This is exactly the form the record uses (`smwfycxze/m4` Block C: "the state function is a proper
colouring of the `6`-cycle"); (5.0) records *why* nothing else survives on the orbit. The verified
set equality of the two predicates over all `m^6` words, `m = 3, 4`, is check `A6` of `verify.py`.

### 5.2 Decision of the orbit system (exact, two procedures)

Counting words `w : Z/6 -> O` satisfying (5.0) (brute force over `|O|^6` and, independently,
`trace(M^6)` of the transition matrix on ordered pairs `(a,b)`, `a != b`, `(a,b) -> (b,c)`,
`c != b`):

| `|O|` | `k` | words | using all `|O|` | closed form `(m-1)^6 + (m-1)` | record |
|---|---|---|---|---|---|
| 2 | 5 | **2** | 2 | 2 | `smwfycxze/m4` Block C: 2 |
| 3 | 6 | **66** | **60** | 66 | Block C: 66 / 60 |
| 4 | 7 | **732** | 480 | 732 | Block C: 732 |

So the `k = 5` and `k = 7` rows reproduce the record exactly (calibration) and the `k = 6` row is
the one Theorem 2(d) consumes. The decisive finite statement is:

> **Lemma 5.1.** Every **two-valued** word satisfying (5.0) is `2`-periodic
> (`w(k+2) = w(k)` for all `k`). Hence in the degenerate case of Theorem 2(d)(ii) the state
> function is invariant under `R^2`, `R` exchanges the two states, and the state measures are
> exactly `(1/2,1/2,0)`.

*Proof.* With two values, `w(k+1) != w(k)` forces `w(k+1)` to be the other value, hence
`w(k+2) != w(k+1)` forces `w(k+2) = w(k)`. `square`

### 5.3 Exact certificates (`verify.py`, exit `0`, 55 checks, no floating point in a decision)

All arithmetic is `fractions.Fraction` plus an exact quadratic field `Q(sqrt 3)`; each count is
produced twice and compared.

* **A1-A10, the orbit system.** `A1` counts the words twice (brute force over `m^6`; and
  `trace(M^6)` of the transition matrix on ordered pairs) for `m = 2,3,4` and against the closed
  form `(m-1)^6 + (m-1)`; `A2-A5` are the values `2 / 66 / 732`, i.e. the `k = 5, 6, 7`
  calibrations of the record; `A6` verifies that (5.7) and (5.2)-at-`120^circ` define the **same**
  word set (Observation 5.0); `A7-A9` verify that the two-valued solutions are exactly the six
  alternating words and are `2`-periodic; `A10` verifies no three-valued solution is `2`-periodic
  (so the three-valued states are genuinely three).
* **B1-B5, the exact direction geometry.** Six exact directions
  `e_k = (cos k pi/3, sin k pi/3) in Q(sqrt 3)^2` with `|e_k| = 1`, `R e_k = e_{k+1}`,
  `|e - Re| = 1` (properness at unit distance) and `e + R^2 e = R e` (the identity that turns
  (5.2) into a statement about the circle point in direction `Re`). `B2-B5`: for `w` with
  `0 < |w| < 2` the unit decompositions `s + t = w` are exactly the two points `{s, t}` exchanged
  by `s <-> t` (the linear condition `s.w = |w|^2/2` cuts the unit circle in at most two points),
  checked exactly on the rational witness `w = (24/25, 32/25)`, `|w| = 8/5`.
* **C1-C6, the rigid alternation.** In units of `pi/3` on the circle `R/6`, the set
  `A = [0,1) u [2,3) u [4,5)` satisfies `A cap R(A) = empty`, `A u R(A) = S`, `R^2(A) = A`, and
  `sigma(A) = sigma(R A) = 1/2` exactly; the naive half-split `[0,pi)` fails both `A cap R(A) =
  empty` and `R^2`-invariance (the correction recorded in `smwfycxze/m4` Block D, reproduced).
* **D1-D2, the geometry of Theorem 3(ii).** `|y - p| < rho - 1` with `rho > 1` implies
  `sup_{z in dB(y,1)} |z - p| <= |y-p| + 1 < rho`, i.e. the unit circle about `y` lies in
  `B(p,rho)`; the threshold `rho = 1` is exact.
* **E1-E7, the hexagonal 7-colouring (`k = 7`), a genuine proper `S_1` colouring.** `E1-E4`
  certify properness in exact arithmetic: hexagons of circumradius `s = 2/5`, colour
  `(m + 3n) mod 7`, nearest same-coloured cell centres at squared distance `21 s^2 = 84/25`, hence
  every point pair between two same-coloured cells is at distance `> 1` because
  `sqrt21 > 9/2  <=>  21 > 81/4` (exact rationals). `E5-E7`: at a **hexagon centre** `x` the
  colouring is constant on `B(x, sqrt3 s/2)`, so `Gamma_x = empty`; and the unit circle about `x`
  carries the labels `{1,2,3,4,5,6}`, each on a genuine arc (every witness direction is certified
  *strictly interior* to its hexagon, so the label holds on an arc of positive length).
* **Lean core, `orbit_core.lean`** (pinned toolchain, `source scripts/env4341.sh && lean
  orbit_core.lean`, exit `0`, no `sorry`, no `native_decide`). Machine checks: `two_valued_periodic`
  (Lemma 5.1 for an arbitrary two-valued state function on `ZMod 6`, axioms `[propext,
  Quot.sound]`), and the counts `card_two = 2`, `card_three = 66`, `card_three_valued = 60`,
  `card_four = 732`, `closed_form` (axioms `[propext, Classical.choice, Quot.sound]` in each case).
* **G0-G3, a discrete model of the pushforward computation** behind (4.1), checked in exact integer
  arithmetic on the finite group `Z/7 x Z/7` with a six-element "direction" set: the identity
  `sum_{x in E} sum_{s in S} f(x+s) = sum_y f(y) #{s : y-s in E}` for twenty random integer test
  functions `f`; its consequence that the analogue of `(4.1)` vanishes identically; and the model
  counterpart of the step used in (ii) — every centre whose "circle" lies entirely in `E` is itself
  `O`-coloured.
* **F1, the exact-three witness.** The strip colouring `c(x,y) = floor(10x) mod 3` is a weak
  measurable cell colouring in `S_1` with straight boundaries; at `x = (1/20, 0)` the colouring is
  constant on the strip `(0, 1/10) x R`, so `Gamma_x = empty`, and the unit circle about `x`
  carries exactly the labels `{0,1,2}`.

### 5.4 The two witnesses that both hypotheses of Theorem 1(f) are needed

* **`Gamma_x supseteq K_3(V)` without `|R_x| = 3`:** the binary part of the triangle locus
  (Theorem 1(b)), locally finite by Lemma 5.5.
* **the circle condition without a cycle, in a *proper* colouring:** the hexagonal 7-colouring at a
  hexagon centre (checks `E5-E7`): the unit circle carries six labels on genuine arcs and
  `Gamma_x = empty`. So even a circle carrying *many* labels forces no transition.
* **the circle condition without a cycle, with *exactly* three labels:** the strip colouring at
  `x = (1/20, 0)` (check `F1`): the circle carries exactly `{0,1,2}` and `Gamma_x = empty`. That
  colouring is not proper — it is only used as a witness for the insufficiency of the circle
  condition inside `S_1`, which is a statement about the definitions (weak measurability and the
  singleton palette), not about properness.

## 6. What this does and does not decide

**Decided.**
1. The limit of three-valued triangle centres is fully classified (Theorem 2(d)): same triple and
   `Gamma = K_3` exactly, or the rigid binary alternation with measures `(1/2,1/2,0)`. In
   particular the accumulation cannot change the cycle length and cannot produce a five- or
   six-cycle, and in the non-degenerate case the locus is self-similar at its own accumulation
   points (Theorem 2(e)).
2. The palette at an accumulation point is confined to the *same* complementary triple
   (Theorem 2(b)) — a constraint that does not follow from the single-centre axioms alone.
3. `Z^3_V ⊆ E_O` is circle-thin: (4.1) holds, `E_O` is not conull in any ball of radius `> 1`, and
   hence contains no ball of radius `> 1` (Theorem 3). The proof uses only `(T)` and `(SA)` (not
   (5.2), (5.7) or (6.2)) and holds for every `k` and every `O` with `|O| >= 2`; the `k = 6`
   instance is `|O| = 3`. Nothing is claimed about balls of radius `<= 1`: Theorem 3(iii) explains
   why the method cannot reach them.
4. The state-continuity lemma of `smwfycxze/m4` §10 is proved (Theorem 2(c)), including the two
   steps that were sketched there (uniqueness of the weak-* limit and the `L^1` upgrade).

**Not decided, and why.**
1. `(W)` at `k = 6`: Theorem 3 gives `Z^3_V` thin in a specific sense, not locally finite. Nothing
   here makes `Z^3_V` null, discrete or locally finite, and by Theorem 2(d)(i) the locus is
   *closed as a locus of three-valued centres*: at its own accumulation points it reproduces
   itself. So the printed data are compatible with a self-similar `Z^3_V`.
2. **No countermodel is constructed.** At `k = 6` an `S_1` colouring is a proper 6-colouring of the
   plane, so every statement here is conditional on `chi(R^2) <= 6`; if `chi(R^2) = 7` all of it is
   vacuous. (This is the standing caveat of the whole `k = 6` record and is flagged here for the
   same reason.)
3. The degenerate alternative (Theorem 2(d)(ii)) is *not* excluded by properness; but it lands on
   the binary locus, which Lemma 5.5 already handles, so excluding it would not by itself give
   `(W)`. What remains is exactly the case `k = 6`, `ell = 3`, `|R_x| = 3` of
   `smwfycxze/m4` §9.
4. **What a proof of `(W)` in `S_1` at `k = 6` still needs**, in the light of Theorem 2: a mechanism
   that either (a) separates `T`-hitting centres for `|T| = 3` (equivalently `|P| <= 2`), or (b)
   forbids the self-similar three-valued locus. Theorem 3 blocks every argument of the following
   shape: (4.1) is the aggregate consequence of the circle-fibre axioms extracted here, and it is
   satisfied by every thin locus, so a proof that only adds up circle data cannot do (b). (This is a
   statement about the identity (4.1) and the class of loci it constrains, not a claim that no
   aggregate argument of any other form exists.) A successful argument must therefore use the
   *transition* data `Gamma_x` globally (which is `(T)`, hence equivalent to `chi(R^2) <= 6`; see
   `smwfwi7rh/m15` Theorem C), or a new kind of conclusion from (5.2).

---

## 7. Reproducing

```
cd .ultramath/smwg1r9lg/m4
python3 verify.py          # exit 0: all exact checks; two independent procedures per count
```

```
source scripts/env4341.sh      # from the repository root
lean orbit_core.lean           # exit 0, clean axioms
```

Files: `NOTE.md` (this note), `verify.py` (verifier), `verify.out` (its output),
`orbit_core.lean` (machine-checked finite core), `work/` (scratch probes, not part of the
deliverable).
