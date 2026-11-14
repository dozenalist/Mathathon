# The triangle gate in the a.e.-singleton class at six colours: the transition graph is
# a subgraph of `K_4`, and the residual is exactly the three-valued triangle

Member `m4`, swarm `smwfycxze`, direction `d3` (registered as *d4: the triangle gate in `S_1`
at `k = 6`*).

**Verifier.** `verify.py` in this directory. Run `python3 verify.py`; exit status 0 means all
**56** checks pass. Exact integer / rational arithmetic throughout (`fractions.Fraction`, no
floating point where a decision is made); every count is produced by **two independent
procedures** and compared. Wall clock about 110 s (the parametric field check of block D6
dominates).

---

## 0. What is delivered

| § | statement | kind |
|---|---|---|
| 2 | **Theorem 1** (two isolated vertices): in the a.e.-singleton class `S_1`, at **every** centre of **every** weak measurable `k`-colouring, `Gamma_x` has at least two isolated vertices; equivalently `Gamma_x` is a subgraph of `K_{k-2}`, so `Gamma_x` has no simple cycle of length `> k-2` | theorem (new, all `k`) |
| 3 | **Corollary 2** (binarity `<=>` `k - ell = 2`): at a centre whose `Gamma_x` contains a cycle of length `ell`, the essential range `R_x` of the singleton palette satisfies `R_x` inside `[k] \ V(C)` and `|R_x| >= 2`; hence `k - ell = 2` forces `R_x` to *be* the complement and forces the centre to be **binary** for that pair, hence `delta_*`-separated by Lemma 5.5; `k - ell < 2` is impossible | theorem; calibrates the paper and `m4` (`smwfwi7rh`) |
| 4 | **Corollary 3** (`k = 6` classification): in `S_1` at `k = 6`, `Gamma_x` is a subgraph of `K_4` at every centre; at a triangle centre with vertices `V` exactly one of two things happens: `|R_x| = 2` (binary, `delta_*`-separated) or `|R_x| = 3 = |[6]\V|` and then **`Gamma_x = K_3(V)` exactly**; also `Gamma_x` never contains the complementary triangle | theorem (new) |
| 5 | **Corollary 4** (which `§8` cases can matter in `S_1`): for an `S_1` colouring at `k = 6` the cycle extracted in `§7` has length `ell` in `{3,4}`. **`§8`'s `ell = 5` and `ell = 6` cases are vacuous in `S_1`** | theorem (new) |
| 6 | **Theorem 5** (the exact residual): in `S_1` at `k = 6`, `(W)` `<=>` `L` locally finite `<=>` the *three-valued triangle locus* `Z^3` is locally finite, where `Z^3 = {x : Gamma_x = K_3(V)` and `R_x = [6]\V` for some triple `V}`. Everything else in `L` is locally finite unconditionally | theorem (new, sharp form of `m4` Thm 3) |
| 7 | **Theorem 6** (no printed mechanism reaches it): at a triangle centre in `S_1` the palette is confined to the complementary triple, so every `(5.2)`-exclusion available there removes at most `|O| = k-3` labels and never a triangle label; at `k = 6` that is `3`, exactly `chi(K_3)`. Lemmas 6.3, 6.4 and 6.7 each need `4` or `5` labels excluded, so all three are unavailable. The `k = 5` triangle case is *not* one of them: it is the `k - ell = 2` case of Corollary 2 | no-go with its class stated and calibrated |
| 8 | **Decided finite computation** (two independent procedures each): `711` of `32768` labelled graphs on six labels are `S_1`-admissible; the longest cycle in any of them is `4 = k-2`; `3` graph shapes at a four-cycle centre and `4` at a triangle centre; the `R`-orbit word counts `m = 2` (k=5): `2`, `m = 3` (k=6): `66`/`60`/orbits `[6,18,36]`; and two exact three-valued state fields with angular measures `(2pi/3,2pi/3,2pi/3)` and `(pi,pi/2,pi/2)`, both verified exactly to alternate under `R` and to respect the `1/2` bound | computation |
| 9 | **phase transition**: the forced (binarity) regime is `k - ell = 2`; the first unforced case is `k = 6, ell = 3, |R_x| = 3`; the first **refuted** case is `k = 7, ell = 3, |R_x| = 4` (`m3`, accepted). So the residual of Theorem 5 inherits the `5 / 6 / 7` transition and is not a technical artefact | status |

**What is not done: `(W)` at `k = 6` is not decided here.** §10 states exactly what remains and
what is *not* claimed.

---

## 1. Setting and the cited facts

`c : R^2 -> I`, `I` a `k`-element label set, a **weak measurable** `k`-colouring: every colour
class `A_i = c^{-1}(i)` is Lebesgue measurable. `S = S^1` carries normalised angular measure
`sigma`; all angular statements are a.e. ; `R` is rotation of directions by `kappa = pi/3`.

* `P_x(e)`, the **maximal palette** of paper Definition 5.1 (p. 26): the essential union, over
  all circle traces `b in W_x` at `x`, of `{b_i > 0}`. It is measurable in `e`, nonempty a.e.,
  and every trace is supported in it.
* **(5.7)** (Corollary 5.4, p. 29): `P_x(e) ∩ P_x(Re) = empty` a.e.
* **(6.2)** (Lemma 6.2, p. 35): if `ij` is an edge of `Gamma_x` then `P_x(e)` is **not**
  contained in `{i,j}` for a.e. `e`.
* **(5.2)** (Lemma 5.2 (1), p. 27): for a.e. independent-angle pair `(e,v)`,
  `c(x + e + v)` `notin` `P_x(e) ∪ P_x(v)`.
* **Lemma 5.5** (p. 30): `delta_* > 0` such that any two distinct centres binary for the *same
  pair* of labels are at distance `>= delta_*`. "`x` binary for `{i+,i-}`" means
  `P_x(e) ∩ {i+,i-} != empty` a.e. (p. 30).
* **`m11` Theorem 3** (`sigma{T subset P_x} <= 1/2` for every nonempty `T`, every centre).
* **Class `S_1`** (`m4` of `smwfwi7rh`): for **every** centre `x`, `P_x(e)` is a **singleton**
  for a.e. `e`. Write `P_x(e) = {sigma_x(e)}` and
  `R_x = { i : sigma{e : sigma_x(e) = i} > 0 }` for the **essential range**.

`S_1` contains every colouring constant on the cells of a locally finite Borel partition with
piecewise `C^1` boundaries, and `m3`'s `k >= 7` countermodel. At `k = 6` the class `S_1` is
nonempty only if a 6-colouring exists, so every `k = 6` statement below is *conditional on
`chi(R^2) <= 6`* — the same caveat as every `k = 6` statement in the record.

---

## 2. Theorem 1: the palette value is an isolated vertex, and there are at least two of them

> **Lemma A.** Let `c` be a weak measurable `k`-colouring in `S_1`, `x in R^2`. If `{i,j}` is an
> edge of `Gamma_x` then `sigma_x(e)` `notin` `{i,j}` for a.e. `e`. Hence every label of the
> essential range `R_x` is an **isolated vertex** of `Gamma_x`.

*Proof.* (6.2) gives `P_x(e)` `not subset` `{i,j}` a.e.; in `S_1` that is `sigma_x(e)` `notin`
`{i,j}` a.e. If `sigma(E_i) > 0` then on a set of positive measure `sigma_x = i`, so
`P_x(e) = {i}` is contained in `{i,j}`, contradicting the a.e. statement. The same for `j`.
Hence `R_x ∩ {i,j} = empty`. `square`

> **Lemma B.** `|R_x| >= 2`.

*Proof.* `R_x` is nonempty (the palette is nonempty a.e.). If `R_x = {i}` then `sigma_x = i`
a.e.; but (5.7) reads `{sigma_x(e)} ∩ {sigma_x(Re)} = empty` a.e., i.e. `sigma_x(e) !=
sigma_x(Re)` a.e., and `R` preserves angular null sets, so `sigma_x(Re) = i` a.e. Contradiction.
`square`

> **Theorem 1.** For every weak measurable `k`-colouring in `S_1` and every `x in R^2`, every
> edge of `Gamma_x` has both endpoints outside `R_x`. Hence
> ```
>     Gamma_x  is a subgraph of  K_{[k] \ R_x}  ⊆  K_{k-2} ,
> ```
> and `Gamma_x` contains **no simple cycle of length `> k-2`**. Equivalently: `Gamma_x` has at
> least two isolated vertices. The bound `k-2` cannot be improved to `k-3`.

*Proof.* Immediate from Lemmas A and B. Sharpness: at `k = 5` a triangle centre has
`Gamma_x ⊇ K_3 = K_{k-2}` (the paper's triangle case, and `m1`'s single-centre classification
shows the palette level does not exclude `K_{k-2}`). `square`

**Relation to `m4` (`smwfwi7rh`) Theorem 3.** Its parts (i) and (ii) are the `k = 6` instances
`k - ell = 1, 0` of Theorem 1 (`ell = 6`: `V(C) = [6]`, so `R_x ⊆ empty`, contradicting
`|R_x| >= 2`; `ell = 5`: `R_x ⊆ {X}`, the same). Theorem 1 is stronger in three ways: it is a
statement about `Gamma_x` itself rather than about cycles, it holds at every `k`, and it gives
`Gamma_x ⊆ K_{k-2}` rather than only a cycle-length bound. Its proof uses neither Proposition
5.6 nor Lemma 5.5.

---

## 3. Corollary 2: binarity at a cyclic centre is exactly the case `k - ell = 2`

> **Corollary 2.** Let `x` be a centre in `S_1` whose `Gamma_x` contains a simple cycle `C` with
> vertex set `V(C)`, `|V(C)| = ell`. Then
> 1. `R_x ⊆ [k] \ V(C)` and `|R_x| >= 2`; in particular `k - ell >= 2`;
> 2. if `k - ell = 2` then `R_x = [k] \ V(C)` exactly, `P_x(e) ⊆ [k] \ V(C)` a.e., so `x` is
>    **binary** for the pair `[k] \ V(C)`, and Lemma 5.5 gives `delta_*`-separation: any two
>    such centres with the same `V(C)` are at distance `>= delta_*`;
> 3. if `k - ell < 2` there is no such centre at all.

*Proof.* (1) every vertex of `C` lies in some edge of `Gamma_x`, so Lemma A removes all of
`V(C)` from `R_x`; Lemma B gives `|R_x| >= 2`. (2) `R_x` is a subset of a two-element set with
at least two elements. Then `sigma_x(e) in [k]\V(C)` a.e., so
`P_x(e) = {sigma_x(e)}` meets the pair `[k]\V(C)` a.e.; that *is* the definition of binarity
(p. 30), and Lemma 5.5 applies. (3) is (1). `square`

**The calibration table.** This single corollary reproduces four accepted results and locates
the frontier; the verifier checks the combinatorial content of every row (`verify.py` blocks A
and E).

| `k` | `ell` | `k - ell` | consequence in `S_1` | status |
|---|---|---|---|---|
| 5 | 3 | **2** | every triangle centre is binary for the complement pair `->` Lemma 5.5 `->` locally finite | **this is the paper's Theorem 6.5 triangle case** |
| 5 | 4 | 1 | no such centre exists | the paper proves this by the harder §6.3.1/6.3.2 |
| 5 | 5 | 0 | no such centre exists | the paper proves this by §6.3.4 |
| 6 | 4 | **2** | every four-cycle centre is binary for the complement pair `->` locally finite | `m4` (`smwfwi7rh`) Thm 3(iii) |
| 6 | 5, 6 | 1, 0 | no such centre exists | `m4` Thm 3(i),(ii) |
| 6 | **3** | **3** | **not forced** | `(W)` at `k = 6` |
| 7 | 3 | 4 | not forced, and **false** (`m3`) | refuted |
| `k >= 7` | 3 | `k-3 >= 4` | not forced, and **false** (`m3`) | refuted |

So the paper's triangle case is a `k - ell = 2` phenomenon, and at `k = 6` the triangle is the
unique cycle length in `S_1` for which that phenomenon is unavailable. The three `k = 5` rows
also give, in `S_1`, one-line proofs of the paper's four- and five-cycle exclusions, which the
paper proves by the `L^1`-continuity and transport machinery of §6.3 — a genuine simplification,
not a new result.

---

## 4. Corollary 3: the `k = 6` classification of `Gamma_x` in `S_1`

> **Corollary 3.** Let `k = 6` and `c` a weak measurable 6-colouring in `S_1`.
> 1. `Gamma_x ⊆ K_4` for **every** centre `x`. Hence `L` is the union of the triangle locus and
>    the four-cycle locus, and `Gamma_x` contains no 5- or 6-cycle.
> 2. At a **triangle** centre, i.e. `Gamma_x ⊇ K_3(V)` with `|V| = 3`, put `O = [6] \ V`. Then
>    `R_x ⊆ O` and `|R_x| ∈ {2,3}`, and:
>    * `|R_x| = 2` `=>` `x` is binary for the pair `R_x`, hence `delta_*`-separated;
>    * `|R_x| = 3 = O` `=>` **`Gamma_x = K_3(V)` exactly**, i.e. the triangle is the only
>      cycle and `§7`'s extraction at `x` returns `ell = 3` with this cycle.
> 3. `Gamma_x` never contains `K_3(O)`, the complementary triangle. (`B4` in the verifier.)
> 4. At a **four-cycle** centre, `R_x` is the complement pair and `x` is binary for it.
> 5. There are exactly `4` graph shapes at a triangle centre (`K_3`, `K_3` + one pendant,
>    `K_3` + two pendants, `K_4`) and exactly `3` at a four-cycle centre (`C_4`, `C_4` + one
>    diagonal, `K_4`).

*Proof.* (1) Theorem 1 with `|R_x| >= 2` gives `Gamma_x ⊆ K_{6-|R_x|} ⊆ K_4`. (2) Lemma A gives
`R_x ⊆ O`; `|R_x| >= 2`. If `|R_x| = 2`: `sigma_x ∈ R_x` a.e. so `P_x(e) ∩ R_x != empty` a.e.,
which is binarity, and Lemma 5.5 applies. If `|R_x| = 3 = O`: every edge avoids `O` by Lemma A,
and `K_3(V) ⊆ Gamma_x`, so `Gamma_x = K_3(V)`. (3) If `K_3(O) ⊆ Gamma_x` then every edge of
`K_3(O)` avoids `O`, so `R_x ∩ O = empty`, contradicting `R_x ⊆ O` and `|R_x| >= 2`. (4) as in
Corollary 2 with `k - ell = 2`. (5) enumeration, `verify.py` block B: `4` and `3` shapes.
`square`

**Consistency with the models of record.** `m13`'s singleton triangle field at `k = 6` has
`sigma(u) = 4 + (floor(9u/2) mod 3)` in units `u = t/pi`; the verifier checks exactly that it is
three-valued, alternates under `R`, has measures `(2pi/3, 2pi/3, 2pi/3)` and hence `|R_x| = 3`;
Corollary 3(2) then *predicts* `Gamma_x = K_3` at every point of that model, which is what the
model has. **Caveat:** `m13`'s field is centre-independent, so it satisfies the *palette axioms*
of `S_1` but is not the maximal palette of any weak measurable colouring (`m4` Corollary 2,
`m10`); it models Theorem 6's hypothesis list, not `S_1` itself.

`m3`'s `k >= 7` countermodel *is* a weak measurable colouring in `S_1` and has `|R_x| = 4` at its
accumulating triangle points (its palette is a singleton whose values are the four labels outside
`{0,2,3}`), so Theorem 1 predicts `Gamma_x ⊆ K_3`, i.e. **`Gamma_x = K_3` exactly** — sharpening
`m3`'s reported `Gamma_x ⊇ K_3` to equality. And `m3` is *not* covered by Corollary 2 because
there `k - ell = 4 != 2`, exactly as Theorem 1 requires.

---

## 5. Corollary 4: in `S_1` at `k = 6` only `§8`'s `ell = 3` and `ell = 4` cases can occur

`§7`'s extraction takes a cyclic centre `x` and a simple cycle of `Gamma_x`. By Corollary 3(1),
`Gamma_x ⊆ K_4`, so that cycle has length `ell ∈ {3,4}`. Therefore:

> **Corollary 4.** For a weak measurable 6-colouring in `S_1`, `§7` produces only `ell = 3` or
> `ell = 4`. **`§8`'s Proposition 8.2 (`ell = 5`) and its new `ell = 6` case are vacuous in
> `S_1`**; only Proposition 8.5 (`ell = 4`) and Proposition 8.10 (`ell = 3`) are needed for the
> `S_1` branch of the argument at `k = 6`.

Moreover the `ell = 4` case in `S_1` carries strictly more structure than `§8`'s hypotheses use:
the palette at such a centre is **binary** for the complement pair (Corollary 2(2)), and
`Gamma_x ⊆ K_4`. That is available to the `ell = 4` direction and is not used by the printed
`§8` argument.

Note the logical role: `§8` kills the `§7` structure *given* `(W)`. So Corollary 4 does not let
one drop `§8`'s `ell = 4` case; it says which cases the `S_1` branch has to supply, and it
guarantees `ell = 5, 6` never arise there.

---

## 6. Theorem 5: the exact residual statement

Throughout, `L = {x : Gamma_x contains a cycle}` is closed (paper §6, and each edge-presence
locus is closed).

> **Theorem 5.** Let `k = 6` and let `c` be a weak measurable 6-colouring in `S_1`. Then the
> following are equivalent.
> 1. **(W)**: there are `y` and `R > 1` with `L ∩ B(y,R)` finite.
> 2. `L` is locally finite.
> 3. The **three-valued triangle locus**
>    ```
>        Z^3 = { x : Gamma_x = K_3(V) and R_x = [6] \ V  for some 3-element V ⊆ [6] }
>    ```
>    is locally finite.
>
> The part of `L` outside `Z^3` is locally finite **unconditionally**.

*Proof.* (1) `<=>` (2): locally finite `=>` (W) is immediate; conversely if `L` is not locally
finite there is a closed ball `B(y,r)` with `L ∩ B(y,r)` infinite, and then `L ∩ B(y,2)` is
infinite too, so `(W)` fails. (2) `<==>` (3): by Corollary 3, `L` is the union of the triangle
locus and the four-cycle locus. The four-cycle locus is contained in the union over the `15`
label pairs of the binary set for that pair, each `delta_*`-separated by Lemma 5.5, so locally
finite. Within the triangle locus, Corollary 3(2) splits it into the binary triangle centres
(again `delta_*`-separated after a union over `15` pairs, so locally finite) and the centres
with `|R_x| = 3`, at which Corollary 3(2) gives `Gamma_x = K_3(V)` — that is `Z^3`. A finite
union of locally finite sets is locally finite, and `L` is locally finite iff every member of
the finite union is. `square`

So in `S_1` at `k = 6` the whole of `(W)` is the question

> **(Sep3)** `Z^3` is locally finite — for each of the `20` label triples `V`, the set of
> centres with `Gamma_x = K_3(V)` and `R_x = [6]\V` is locally finite,

and `Z^3` is the only set in the plane for which `(W)` is still undecided. This is `m4`'s
reduction of `(W)` in `S_1` to the triangle locus, sharpened to the part of the triangle locus
that binarity does not reach. Note the shape of `Z^3`: at such a centre `Gamma_x` is *exactly*
the label triangle and nothing else, and the palette field is a measurable
`sigma_x : S^1 -> [6]\V` with `sigma_x(e) != sigma_x(Re)` a.e. and each of the three values on
at most half the circle (`m11` Theorem 3).

---

## 7. Theorem 6: why none of the printed mechanisms can reach `Z^3`

The paper's single-centre and two-centre machinery has exactly four engines, and each needs a
*label budget* at the centre.

**Counting lemma.** Let `x` be a triangle centre in `S_1` with `Gamma_x ⊇ K_3(V)`, `O = [6]\V`.
By Lemma A, `sigma_x(e) in O` a.e., so **every palette at `x` is contained in `O`**. The same
holds at every triangle centre with the same `V`. Hence:

* a single application of `(5.2)` at such a centre excludes at most `2` labels at the sum point
  (one per unit summand), and both lie in `O`;
* any density statement obtained by iterating `(5.2)` over such centres excludes only labels of
  `O`, i.e. at most `|O| = k - 3 = 3` labels at `k = 6`;
* no label of `V` is ever excludable, because no palette at any of these centres contains one.

Consequently at least `3` labels remain available at every point reachable by `(5.2)` from the
triangle centres, and `3 = chi(K_3)`: a unit equilateral triangle can always be properly
coloured with what is left. The printed engines need strictly more:

| engine | what it needs | at `k = 6` |
|---|---|---|
| Lemma 6.3, strict state separation | two disjoint label groups whose union is `I \ {X}`: `k-1 = 5` labels excluded | not available (budget `3`) |
| Lemma 6.4, singleton/pair alternation | a singleton and a pair with total size `k-2 = 4`: `4` labels excluded | not available (budget `3`) |
| Lemma 6.7, step ban | a cyclic index order with adjacency forcing, i.e. a 5-cycle of states | not available (only `3` states, no cyclic order used) |
| Lemma 5.5, binary separation | `2` labels, both in `O`, with `k - ell = 2` | **available only for `ell = 4`** |

> **Theorem 6.** In `S_1` at `k = 6` there is no derivation of a contradiction at a triangle
> centre from `(5.2)`, `(5.7)`, `(6.2)` and `m11`'s `1/2` bound: the total excludable label set
> at such a centre has at most `k - 3 = 3` elements and contains no triangle label, while each
> of Lemmas 6.3, 6.4, 6.7 requires `4` or `5`.

**Calibration at `k = 5`.** The same bookkeeping gives a budget of `|O| = 2`, also below `4`.
So the paper's `k = 5` triangle case cannot be a `(5.2)`-density argument either — and it is
not: it is binarity plus Lemma 5.5, which is `k - ell = 2` in Corollary 2. At `k = 5` the
triangle has a *two-element* complement, so (5.7) applied to two singleton-intersections of a
two-element set forces equality; at `k = 6` the complement has three elements and (5.7) forces
only inequality. **That is the entire `k = 5 -> k = 6` degradation, and it is a statement about
`k - ell`, not about `k`.**

**Vacuity test.** The class of Theorem 6 is nonempty at the palette level, and its hypotheses are
satisfied by the models of record: `m13`'s singleton field (`|R_x| = 3`, `Gamma = K_3`), `m15`'s
pair field and `FREE-LABEL`'s fields are not in `S_1` (their palettes are pairs), but `m13`'s is,
and so is `m3`'s `k >= 7` colouring. The first two fail the paper's `(5.3)` already at unit
separation (`m4` Corollary 2, `m10`), which is why they are not near-counterexamples; `m3`'s is a
genuine colouring and it is exactly the case Theorem 6 does *not* exclude — consistent, since at
`k = 7` the budget is `|O| = 4`, enough for Lemma 6.4's engine, and Theorem 1 does not force
binarity there.

---

## 8. The decided finite computation

Everything below is in `verify.py`; each count is produced twice, by two unrelated procedures
(brute force over all graphs / all words, versus an isolation-set or chromatic-polynomial or
orbit computation), and the two are compared.

**Block A — Theorem 1's combinatorial core.**

| `k` | `#{(labelled graphs on k vertices)}` | `#S_1`-admissible (>= 2 isolated) | longest cycle | cycles present |
|---|---|---|---|---|
| 4 | 64 | 7 | none | — |
| 5 | 1024 | **51** | **3 = k-2** | 3 |
| 6 | 32768 | **711** | **4 = k-2** | 3, 4 |

The `711` is confirmed by inclusion–exclusion over the exact isolated set
(`sum_m C(6,m) g(6-m)` with `g(t) = sum_j (-1)^j C(t,j) 2^{C(t-j,2)}`), and the `g(t)` are
themselves brute-forced for `t <= 5`. Also verified for `k = 5, 6`: a graph is `S_1`-admissible
iff there is an `R` with `|R| >= 2` and every edge off `R` — the translation of Lemmas A+B.

**Block B — the `k = 6` classification.** `440` `(graph, V)` pairs at triangle centres in `4`
isomorphism shapes; `150` graphs with a four-cycle in `3` shapes; `|R_x| = 3` at a triangle
centre forces `Gamma_x = K_3(V)`; no `S_1`-admissible graph contains both complementary
triangles.

**Block C — the `R`-orbit word.** On one `R`-orbit (`6` positions) the state function is a
proper colouring of the `6`-cycle:

| `m = k-3` | proper words `P(C_6,m) = (m-1)^6 + (m-1)` | using all `m` | orbits under `S_m × Z_6` |
|---|---|---|---|
| 2 (`k = 5`) | `2` | `2` | `1` (the two alternations) |
| 3 (`k = 6`) | `66` | `60` | `3`, sizes `[6, 18, 36]` |
| 4 (`k = 7`) | `732` | `480` | — |

So the state word is *unique* up to relabelling at `k = 5` and has `60` genuinely three-valued
possibilities at `k = 6`. At `k = 5` uniqueness is exactly what makes (5.7) a functional
equation (`s_x` invariant under `alpha_+ o alpha_-^{-1}`), which is what Lemma 5.5 consumes; at
`k = 6` there is no functional equation, only inequalities, and the hypothesis of Lemma 5.5 is
not met.

**Block D — exact state fields.** With `u = t/pi in [0,2)` (so `R` is the shift `u -> u + 1/3`)
two three-valued fields are given as explicit rational interval families and verified **exactly**
(interval arithmetic, no sampling used for the decision; rational sampling is the second
procedure):

* `F1`: `R^2`-invariant, arcs of `u`-length `2/9` repeating `4,5,6`; angular measures
  `(2pi/3, 2pi/3, 2pi/3)`;
* `F2`: angular measures `(pi, pi/2, pi/2)` — one state **saturating** the `m11` `1/2` bound —
  built from the two orbit words `(4,5,4,5,4,5)` and `(4,6,4,6,4,6)`;
* `F3`: the `m = 2` analogue, the forced alternation, `(pi, pi)`. Note that the naive
  "half / half" split of the circle **fails** alternation (the exact test catches it): a state
  of angular measure `pi` must be an `R^2`-invariant alternating set, i.e.
  `(0,1/3) ∪ (2/3,1) ∪ (4/3,5/3)` in `u`, not an interval. This is a small but real correction
  to the intuition that "the bound `1/2` is trivial".
* `D6`: the parametric construction above, checked exactly on `139` rational profiles.

So the `m11` bound is not binding at a triangle centre in `S_1`. **Block D6** makes this
quantitative: mixing the three two-valued orbit words `(4,5,4,5,4,5)`, `(4,6,4,6,4,6)`,
`(5,6,5,6,5,6)` with densities `a_A = (t_4+t_5-t_6)/6`, `a_B = (t_4+t_6-t_5)/6`,
`a_C = (t_5+t_6-t_4)/6` (all `>= 0` exactly when every `t_i <= 1`, and summing to `1/3`)
produces an admissible three-valued field for **every** profile `(t_4,t_5,t_6)` with
`0 <= t_i <= 1` and `sum t_i = 2` — verified exactly for the `139` rational profiles with
denominators `12, 7, 5`. The content of `(5.7)` plus the bound at a triangle centre is therefore
exactly: *three measurable sets, each of measure at most `pi`, each disjoint from its own
`pi/3`-shift, with `P_x(e)` the point mass on the set containing `e`* — and nothing more.

**Block E — the binarity table.** The machine checks `k - ell < 2 =>` no admissible centre and
`k - ell >= 2 =>` an admissible centre exists, for `k = 5, 6`, and that at `k = 5` the
complement of a triangle is exactly the two-element `R_x`.

**Block F — cross-checks.** `m13`'s model re-verified from its formula; `m3`'s `k = 7`
configuration checked against Theorem 1's prediction; `C(6,3) = 20`, `10` complementary pairs;
`711 / 32768`.

---

## 9. The phase transition, and where `k = 6` sits

The table of §3 in the coordinates `(k, ell, |R_x|)`:

```
  k - ell = 2      binarity forced        locally finite        (5,3) paper; (6,4) m4; (7,5); ...
  k - ell < 2      centre impossible      locally finite        (5,4),(5,5),(6,5),(6,6), ...
  k - ell = 3      |R_x| in {2,3}         |R_x| = 2 locally finite;
                                          |R_x| = 3  ->  FIRST UNFORCED CASE
                                          (6,3) OPEN;  (7,4); (8,5); ...
  k - ell = 4      |R_x| in {2,3,4}       (7,3) REFUTED by m3; (8,4); ...
  k - ell >= 5     |R_x| in {2..k-ell}    (k,3) REFUTED by m3 for every k >= 7
```

So `(Sep3)` — hence `(W)` in `S_1` — is a genuine phase-transition statement: it holds at
`k = 5` (Lemma 5.5's mechanism, `k - ell = 2`), is **refuted at every `k >= 7`** by `m3`'s
accepted proper measurable colouring, and is open exactly at `k = 6`. The single case that
decides it is `k = 6`, `ell = 3`, `|R_x| = 3`. This is the same `5 / 6 / 7` transition as local
finiteness itself, which is why `(Sep3)` is not a technical lemma with an independent life: at
`k = 6` it *is* `(W)`.

---

## 10. What is NOT claimed, and what a proof would have to do

**Not claimed.**

1. **`(W)` at `k = 6` is not decided.** No proof, no countermodel. `(Sep3)` is stated, not
   settled. `chi(R^2) >= 7` and `chi(R^2) <= 6` are both unproved.
2. **Nothing here is unconditional at `k = 6`**: every `k = 6` statement is conditional on
   `chi(R^2) <= 6`, and is vacuous if `chi(R^2) = 7`. `S_1` at `k = 6` is nonempty only in a
   world where a 6-colouring exists.
3. **Theorem 1 is not a bound on `L`,** only on `Gamma_x` at each centre. It does not make the
   triangle locus locally finite and it does not improve `(W)`.
4. **Theorem 6 is not a theorem about colourings.** It is a statement that a particular finite
   label budget is insufficient; it does not rule out every conceivable `(5.2)`-argument, only
   those whose conclusions are of the forms used by Lemmas 6.3, 6.4, 6.7 and 5.5. An argument
   that extracts a new *kind* of conclusion from `(5.2)` is not excluded.
5. **No claim of priority over `m4` (`smwfwi7rh`) Theorem 3.** Corollary 2 contains it
   (`k = 6`), with a shorter proof and a stronger conclusion; the reduction of `(W)` in `S_1` to
   the triangle locus is `m4`'s.
6. **The `sigma`-algebra / measurability level is not pushed.** All statements are a.e. in the
   direction variable at each fixed centre; no joint measurability in the centre is assumed or
   proved, exactly as in the paper (`m10` records that none is needed).
7. **No new numerical constant.** `delta_*` is the paper's, unquantified.

**What a proof of `(Sep3)` at `k = 6` would have to do.** By Theorem 6 it cannot be a
`(5.2)`-density argument at the triangle centre; by §8 it cannot be a strip/palette argument
(`m6`: `STRIP(6,3)` is SAT with witness `{4}`/`{5}`); by `m14` it cannot be a finite palette
system. Two routes survive, and §4/§6 say exactly what is available on each:

* **(R1) Use the exactness of `Gamma_x = K_3(V)`.** At a centre of `Z^3` all twelve non-`V`
  pairs have `limsup |D_{ij}(B,h)|/|h| = 0` for every ball about `x`. In particular the
  `V`/`O` and the `O`/`O` interfaces have vanishing transition density at `x` at every scale,
  while `x` lies in `H_1 ∩ H_2 ∩ H_3` (it is an endpoint of every triangle edge) and, at every
  *typical* `x in Z^3`, the unit circle about `x` is `O`-valued almost everywhere (the constant
  trace gives `{c(x+e)} ⊆ P_x(e) = {sigma_x(e)}`, and `sigma_x(e) in O`). So `Z^3` is essentially
  the set of points at which the colouring is *non-tame in a quantitative way*: no `V`/`O`
  interface of positive length through any punctured neighbourhood. That matches `m3`'s accepted
  constraint (a `k = 6` countermodel must be non-tame) and turns `(Sep3)` into a statement about
  colourings whose interfaces have vanishing `1`-density, which is the natural target for the
  tameness direction (board `d2`).
* **(R2) Use the state continuity along `Z^3`.** The `L^1`-continuity of
  `x |-> 1{sigma_x = i}` along the triangle locus with fixed `V` (Lemma 6.6's proof, with the
  singleton palette playing the role of Proposition 5.6 in the limit — see Lemma C below) gives
  that `Z^3` carries a continuous field of three-valued state functions with all three states of
  positive measure. So an accumulation point of `Z^3` is itself in `Z^3` and its state function
  is a limit of the others; the obstruction, if any, is a rigidity statement for that field, and
  §8 shows that the rigidity cannot come from the angular axioms alone (the `66`-word system
  with the `1/2` bound is satisfiable, with explicit exact witnesses).

> **Lemma C (state continuity; proved, sketch-quality but complete).** Fix a 3-element `V` and
> let `x_n -> x` be centres in `S_1` each satisfying `Gamma_{x_n} ⊇ K_3(V)` and each contained
> in the triangle locus for `V`; suppose `Gamma_x ⊇ K_3(V)` too. Then
> `1{sigma_{x_n} = i} -> 1{sigma_x = i}` in `L^1(S)` for each `i`. Hence the state functions,
> and the three state measures, converge.

*Proof.* By Lemma A, `sigma_{x_n}` and `sigma_x` take values in `O = [6]\V`. For each centre `y`
in the triangle locus for `V` and each edge `ij` of `K_3(V)`, (6.2)'s trace `b^{ij} in W_y` is
supported in the singleton `P_y`, so `b^{ij} = e_{sigma_y}` a.e. and in particular
`b^{ij}_k = 1{sigma_y = k}` a.e. Now take a subsequence and pass to weak-* limits
`b^{ij}_n -> b^{ij}`; the closure (5.1) gives `b^{ij} in W_x`, so `b^{ij}` is supported in
`P_x = {sigma_x}` and sums to one, i.e. `b^{ij} = e_{sigma_x}` a.e. A weak-* limit of `{0,1}`
valued functions that is itself `{0,1}` valued is an `L^1` limit, because
`int |f_n - f| = int f_n + int f - 2 int f_n f -> 0`. Every subsequence has a further
subsequence with the same limit, so the whole sequence converges. `square`

Lemma C is what makes `Z^3` a legitimate object to reason about at its own accumulation points:
membership in `Z^3` is a closed condition on `R_x` and the state measures are continuous, so
`Z^3` is "self-similar" along its own accumulation and no degeneration forces a contradiction.

---

## 11. Files

| file | content |
|---|---|
| `NOTE.md` | this note |
| `verify.py` | all `56` checks; `python3 verify.py`, exit `0` |
| `out.txt` | its output |
