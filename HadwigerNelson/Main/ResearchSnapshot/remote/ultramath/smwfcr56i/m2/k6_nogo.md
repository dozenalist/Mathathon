# The k = 6 analogue of the five-label architecture: exact constants and the failing inequalities

Audit of *The Euclidean plane is not five-colorable* (OpenAI, 23 Sep 2026), sections 5–8,
with the label set generalised from `Fin 5` to `Fin k`.

Everything below is either (a) a proof, (b) an exact finite enumeration, or (c) a quotation
of the paper's own numbered statement.  Verification scripts are `check_k.py`,
`check_gadget.py`, `check_moser.py`, `check_seven.py` in this directory; their full output is
quoted in §5–§7 and the appendix.

---

## 0. Results

Throughout, `c : R^2 -> I` is a weak measurable k-colouring in the sense of the paper's
Definition 1.2 (`I` the label set, `|I| = k`), `A_i = c^{-1}(i)`, `a_i = 1_{A_i}`,
`H_i` the closed essential support of `A_i`, `P_x` the maximal palette at the centre `x`
(Definition 5.1), `R` rotation by `kappa = pi/3`, and `S` the unit circle with angular
measure `sigma`.

> **Theorem A** (general-k palette bound).  *Let `k >= 3`.  For every weak measurable
> k-colouring and every centre `x`,*
> ```text
> |P_x(e)| <= k - 3        for sigma-almost every e in S.
> ```
> *For `k = 5` this is exactly Proposition 5.6; for `k = 6` it gives `|P_x| <= 3`.*

> **Theorem B** (external state at a triangle interface).  *Let `k >= 5`, let
> `(K_0,K_1,K_2,v_0,v_1,v_2)` be the length-three interface data of Proposition 7.1 at the
> centre `x`, with cycle labels `T = {t_0,t_1,t_2}`, and put `A(e) = P_x(e) ∩ (I \ T)`
> ("the outsiders present at direction `e`").  Then for `sigma`-almost every `e`,*
> ```text
> 1 <= |A(e)| <= k - 4      and      A(e) ∩ A(Re) = empty.
> ```
> *In particular the outsider is unique exactly when `k = 5`; at `k = 6` the state takes one
> of the six values `{A ⊆ T^c : 1 <= |A| <= 2}`, and `|A(e)| = 2` forces `A(Re)` to be the
> complementary singleton.*

> **Theorem C** (the threshold is exactly `k = 5`).  *The label count enters the paper's
> sections 5–8 in exactly three forms:*
> 1. *the palette bound `|P_x| <= k-3` (Theorem A), which the paper needs in the form
>    `|P_x| <= 2` — used in §5.4, §6.3.1, §6.3.3, §8.2, §8.3;*
> 2. *the external-state bounds `1 <= |A(e)| <= k-4` at a triangle interface (Theorem B),
>    which the paper needs in the form `|A(e)| = 1` — used in §6.4 (there via the complement
>    `I \ ({X} ∪ D)`, of size `k-3`), §8.4, §8.6, §8.7;*
> 3. *the cycle-length bound `3 <= ell <= k` of Proposition 7.1.*
>
> *Forms 1 and 2 are the two inequalities* **`k-3 <= 2`** *and* **`k-4 <= 1`**, *and both are
> equivalent to* **`k <= 5`**.  *Form 3 adds one new cycle length at `k = 6` (`ell = 6`).
> Every other ingredient of §5–§8 is k-independent; in particular the final step
> §8.5–§8.6 (the region (8.4) and the seven-vertex Moser certificate) uses only the three
> cycle labels and `chi(Moser) = 4 > 3`, so it would apply verbatim to a six-label run.
> Consequently the architecture, as printed, is a `k <= 5` argument; at `k = 6` the two
> inferences in forms 1 and 2 are false as stated, with the explicit certificates of §5.*
>
> *Precisely: at `k = 5` form 2 reads `1 <= |A(e)| <= 1`, which is the paper's "there cannot
> be two outsiders"; at `k = 6` it reads `1 <= |A(e)| <= 2`, and the second value occurs
> (Corollary B2).  At `k = 4` form 2 is inconsistent (`1 <= |A| <= 0`), so a triangle
> interface cannot exist at `k = 4` at all.*

> **Theorem D** (new cycle length).  *Proposition 7.1 supplies a simple cycle of the
> complete graph on `I`; its length satisfies `3 <= ell <= k`.  At `k = 6` the extracted
> cycle has length `ell ∈ {3,4,5,6}`, and the paper contains no exclusion for `ell = 6`.
> The "planar cover" part of §7 (Lemmas 7.5, 7.6, 7.7, 7.8) does **not** use non-planarity
> of `K_5`; it uses only that a point of the one-skeleton of a simplex has at most two
> positive barycentric coordinates, so it is k-independent.*

---

## 1. The paper's inputs that are used below

All four are quoted from the paper and are k-independent as stated.

* **(P1)** *(Lemma 5.2(1))*.  At every fixed centre `x`, for `sigma ⊗ sigma`-almost every
  `(e,v) in S × S`:
  ```text
  c(x + e + v) ∉ P_x(e) ∪ P_x(v).                                    (5.2)
  ```
* **(P2)** *(Corollary 5.4)*.  At every fixed centre `x`,
  `P_x(f) ∩ P_x(Rf) = ∅` for `sigma`-almost every `f`.                   (5.7)
* **(P3)** *(Lemma 5.5)*.  There is an absolute constant `delta_* > 0` such that, for every
  fixed pair of labels and any two distinct centres that are *binary* for that pair
  (i.e. `P_x(e)` meets the pair for a.e. `e`), the two centres are at distance at least
  `delta_*`.
* **(P4)** *(§5.3, from (P2))*.  If `x` is binary for the pair `{i_+, i_-}`, then
  `P_x(e) ∩ {i_+, i_-}` is a singleton for a.e. `e`, and its selection `s_x` satisfies
  ```text
  s_x(t + kappa) = - s_x(t)      for almost every t.                      (5.8)
  ```
* **(P5)** *(Lemma 8.1, equations (8.1))*.  With the interface data of Proposition 7.1 at
  the centre `x`, the two sign-determined allowed sets `O(e), I(e)` (`O(e)` = labels left
  after deleting the endpoints of every positive edge, `I(e)` the same for the negative
  edges) satisfy, for a.e. `e` outside the finite set `B`,
  ```text
  P_x(e) ∩ O(e) ≠ ∅        and        P_x(e) ∩ I(e) ≠ ∅.                 (8.1)
  ```

Two elementary facts about `P_x` used in the proofs: `P_x` is nonempty a.e. and every trace
`b in W_x` has `supp b ⊆ P_x` a.e.; that is the content of Definition 5.1 as verified in
§5.1 of the paper.

---

## 2. Theorem A: the palette bound `k-3`

**Theorem A.** *Let `k >= 3`.  For every weak measurable k-colouring and every `x in R^2`,
`|P_x(e)| <= k-3` for `sigma`-almost every `e`.*

*Proof.*  Suppose not.  Since there are finitely many `(k-2)`-element subsets `A ⊆ I` and

```text
{ e : |P_x(e)| >= k-2 }  =  ∪_{A ⊆ I, |A| = k-2} { e : A ⊆ P_x(e) },
```

some fixed `A` with `|A| = k-2` satisfies `A ⊆ P_x(e)` for all `e` in a set `E` of positive
angular measure.

*Step 0 (the complement has two elements).*  Write `B = I \ A`.  Then

```text
|B| = k - (k-2) = 2 .
```

This is the only place where the number of labels is used: Lemma 5.5 is available for
two-element label sets and for no others.  The rest of the argument uses nothing about `B`
except `|B| = 2`.

*Step 1: for a.e. `e in E`, the exact circle sampling at the centre `x+e` avoids `A`.*  For
`sigma ⊗ sigma`-almost every `(e,v)`, (P1) gives
`c(x+e+v) ∉ P_x(e) ∪ P_x(v) ⊇ A`; Fubini gives, for `sigma`-almost every `e` (in
particular a.e. `e in E`), `a_i(x+e+v) = 0` for a.e. `v` and every `i in A`.  (The
exceptional set may depend on `e`; no uniformity is needed.)

*Step 2: for a.e. `e in E`, that sampling is a trace at `x+e`.*  The paper's §5.1 argument
applies verbatim: the map `(e,v) ↦ x+e+v` is nonsingular off the product-null set where
`e` and `v` are parallel, so the inverse image of the plane-null atypical set is
`sigma ⊗ sigma`-null, and Fubini gives: for a.e. `e`, the point `x+e+v` is typical for a.e.
`v`.  Hence for a.e. `e in E` the vector function
`v ↦ (a_i(x+e+v))_{i in I}` is the weak-* limit of a constant sequence of typical circle
samplings, i.e. a member of `W_{x+e}`.  It is supported in `B`.

*Step 3: `x+e` is binary for the pair `B`.*  The trace just constructed has nonnegative
coordinates summing to one and supported in the 2-element set `B`, so its positive
coordinates lie in `P_{x+e}` a.e.; therefore `P_{x+e}(v) ∩ B ≠ ∅` for a.e. `v`.  By
definition, `x+e` is binary for the pair `B`.

*Step 4: contradiction.*  The centres `{x+e : e in E}` are pairwise distinct (the map
`e ↦ x+e` is injective), they form an infinite set (positive measure), and they all lie in
the compact set `x + S`.  By (P3) any two of them are at least `delta_*` apart.  A
uniformly separated subset of a compact metric space is finite: cover `x + S` by finitely
many balls of radius `delta_*/3`.  Contradiction. ∎

**Remarks.**
1. The proof is the paper's proof of Proposition 5.6 with the number `3` replaced by
   `k-2`.  The only place where `k = 5` enters the paper's argument is the conclusion
   `|B| = |I \ A| = 2`; the whole of Lemma 5.5 is used only for a *pair*.  Hence the
   argument returns a bound of `2` precisely when `k-2 = 3`, i.e. `k = 5`.
2. `k = 4` gives `|P_x| <= 1`: with four labels every palette is a singleton a.e.
3. `k = 3` gives `|P_x| <= 0`, contradicting nonemptiness of the palette; so the argument
   also proves that no weak measurable 3-colouring exists.  Since the paper's Theorem 1.3
   identifies weak measurable and proper colourings, this is a special case of the known
   lower bound `chi(R^2) >= 4`, and it is a consistency check that the general form of the
   palette bound is faithful (it is not vacuous at small `k`).
4. The bound is *not* improved anywhere in the paper: the paper's `2` is `k-3` at `k=5`.

---

## 3. Theorem B: the external state at a triangle interface

**Theorem B.** *Let `k >= 5` and let `c` be a weak measurable k-colouring.  Let
`(K_0,K_1,K_2,v_0,v_1,v_2)` be the data of Proposition 7.1 at a point `x` for a simple
label cycle of length `ell = 3`; write `T = {t_0,t_1,t_2}` for its labels and
`A(e) = P_x(e) ∩ (I \ T)`.  Then for `sigma`-almost every `e in S`,*

```text
1  <=  |A(e)|  <=  k - 4 ,            A(e) ∩ A(Re) = ∅ .
```

*Proof.*  Fix `e` outside the finite set `B` of §8.1 (so `e` and `Re` are both outside `B`,
`B` being finite), and let `sigma_j in {+,-}` be the sign of `e · v_j` on edge
`e_j = {t_j, t_{j+1}}` (`j = 0,1,2`, indices mod 3).  Recall

```text
O(e) = I \ ∪_{sigma_j = +} e_j ,      I(e) = I \ ∪_{sigma_j = -} e_j ,
```

and that both contain `T^c = I \ T`, of cardinality `|T^c| = k - 3`.

*Step 1 (an outsider is always present).*  Two of the three signs agree (pigeonhole).  If two
signs are `+`, the two corresponding edges of the triangle `T` cover all three vertices of
`T`, hence `O(e) = T^c`; if two signs are `-`, then `I(e) = T^c`.  So in either case one of
`O(e)`, `I(e)` equals `T^c`, and (P5) gives `P_x(e) ∩ T^c ≠ ∅`, i.e.
```text
|A(e)| >= 1 .
```
The same computation at the direction `Re` (which is also outside `B`, and whose three signs
again have two equal ones) gives `|A(Re)| >= 1`.

*Step 2 (no palette contains every outsider).*  Suppose `A(e) = T^c`, i.e.
`T^c ⊆ P_x(e)`, i.e. `|A(e)| = k-3`.  By (P2) at the direction `e`,
```text
P_x(e) ∩ P_x(Re) = ∅ ,
```
so `T^c ∩ P_x(Re) = ∅`, i.e. `A(Re) = P_x(Re) ∩ T^c = ∅`, contradicting Step 1 at `Re`.
Hence `A(e) ≠ T^c`, and since `A(e) ⊆ T^c`,
```text
|A(e)| <= |T^c| - 1 = k - 4 .
```

*Step 3 (disjointness at the 60-degree shift).*  `A(e) ⊆ P_x(e)` and
`A(Re) ⊆ P_x(Re)`, and `P_x(e) ∩ P_x(Re) = ∅` by (P2); hence `A(e) ∩ A(Re) = ∅`. ∎

Steps 1 and 2 combined give `1 <= |A(e)| <= k-4`; the lower bound exceeds the upper bound
when `k-4 < 1`, i.e. for `k <= 4` (Corollary B3).  For `k = 5` the two bounds coincide, so
the outsider is unique; for `k = 6` both `1` and `2` are permitted by these steps, and §5
shows that `2` is not excluded by any palette-level hypothesis.

**Corollary B1 (`k = 5`).**  `|A(e)| = 1` for a.e. `e`, and `A(e) ≠ A(Re)`.  With
`T^c = {X,Y}` this is the paper's binary state `s(e) ∈ {X,Y}`, `s(Re) ≠ s(e)` of §8.4, and
the paper's sentence "There cannot be two outsiders in such a palette, since (5.7) would
leave no outsider at `Re`".

**Corollary B2 (`k = 6`).**  `|A(e)| ∈ {1,2}`, `T^c = {x_1,x_2,x_3}`, and there are six
states.  If `|A(e)| = 2` then `A(Re)` is the complementary singleton, so the state dynamics
is a walk in the disjointness graph on

```text
Sigma = { {x_1}, {x_2}, {x_3}, {x_1x_2}, {x_1x_3}, {x_2x_3} },
```

two states being adjacent when disjoint.  This graph is **not** bipartite: the three
singletons form a triangle.  For `k = 5`, `Sigma = {{X},{Y}}` and the graph is a single
edge, i.e. bipartite; hence the 60°-flip makes the state strictly alternating.

So the exact content of (5.8) and of §8.4's "alternating sectors" is: *the external state
graph is bipartite*, which holds iff `k - 4 <= 1` iff `k <= 5`.

**Corollary B3 (`k = 4`).**  `k-4 = 0 < 1`, so the two bounds are inconsistent: at `k = 4`
a length-three interface is impossible by (8.1)+(5.7) alone.  (Consistent with
`chi >= 5`: such a colouring does not exist.)

**Remark.**  Theorem B is specific to `ell = 3`.  For `ell = 4` the two agreeing edges no
longer cover `T`: with a split sign pattern `(+,+,-,-)`, one has
`O(e) = I(e) = {`one cycle label`} ∪ T^c`, so (8.1) does not force an outsider into the
palette.  This is exactly why the paper needs the separate word analysis §8.3 for
four-cycles, and it is why the table in §4 marks `ell = 4` differently from `ell = 3`.

### A part of §8.3 that does survive at `k = 6`

**Proposition B4** (four-cycle splits, general `k >= 5`).  *Let `T = {0,1,2,3}` be the labels
of a length-four interface at `x`, with edges `{0,1},{1,2},{2,3},{3,0}`, and suppose that
`P_x(e) ∩ T^c = ∅` (no outsider) and that `e` is outside the finite set `B`.  Then:*

1. *the signs form a split, i.e. exactly two positive and two negative edges, each pair
   consecutive;*
2. *the two run-middle labels `m_+, m_-` (opposite vertices of `T`) both belong to
   `P_x(e)`, so the palette determines the split and hence the diagonal
   `{m_+, m_-} ∈ {U, V}`.*

*Consequently the first half of §8.3 transfers to every `k`, and the only change is the
number of states: the admissible outsider-free palettes are*

```text
   {m_+, m_-}                       (1 palette)   at k = 5,
   {m_+, m_-}, {m_+, m_-, t}, {m_+, m_-, t'}      (3 palettes)  at k = 6,
```

*where `t, t'` are the two labels of the other diagonal.*

*Proof.*  (1) Since `P_x(e) ⊆ T`, (8.1) gives `O(e) ∩ T ≠ ∅` and `I(e) ∩ T ≠ ∅`.  `O(e) ∩ T`
is `T` minus the endpoints of the positive edges, so it is nonempty exactly when the
positive edges do not cover all of `T`; a set of edges covering all four vertices of a
4-cycle has at least two edges.  The same holds for the negative edges.  As the two sets
partition the four edges, both have exactly two edges, and a two-edge set not covering `T`
consists of two consecutive edges.  (2) For a split, `O(e) = {m_+} ∪ T^c` and
`I(e) = {m_-} ∪ T^c`; with no outsider in the palette, (8.1) forces `m_+, m_- ∈ P_x(e)`.
The middle pair determines the split, hence the diagonal.  The palette counts are
`check_k.py`, C7. ∎

At `k = 6` the extra cycle label `t` means that a diagonal no longer "fills both palette
slots"; that is exactly the sentence used in the proof of the paper's Lemma 6.6
("a diagonal already fills both palette slots"), so the continuity argument of Lemma 6.6
does not transfer even in this favourable case.

---

## 4. The k-dependence table of §5–§8

Every row is a step of the paper; "k-form" is the general-k statement and "at k=6" its
status.  `ell` is the length of the extracted interface cycle.

| # | Step | k-form / what it uses | k = 5 | k = 6 |
|---|------|----------------------|-------|-------|
| 1 | Lemma 5.2, (5.2) | any `k` | ok | ok |
| 2 | Cor. 5.4, (5.7) | any `k` | ok | ok |
| 3 | Lemma 5.5 | any `k` (pairs only) | ok | ok |
| 4 | §5.3 binary centres, (5.8) | any `k` given a binary pair | ok | ok |
| 5 | **Prop. 5.6 palette bound** | `|P_x| <= k-3` (Thm A) | `2` | **`3`** |
| 6 | Lemma 6.2, (6.2) | any `k` | ok | ok |
| 7 | Lemma 6.3 | needs two state groups whose union is `I \ {X}` | union `= 4 = 5-1` | union `4 ≠ 6-1`, **hypothesis fails** |
| 8 | **Lemma 6.4** | final step needs `chi(K_3) = 3 > k-3` | `3 > 2` ok | **`3 = 3`, no contradiction** |
| 9 | **§6.3.1 four-cycle states** | needs `|P| <= 2` | 3 states `{X},U,V` | **6 cycle-label palettes, mixed** |
| 10 | **§6.3.3 five-cycle diagonals** | needs `|P| <= 2`, `Z/5` | ok | **palettes can be triples** |
| 11 | §6.3.4 accumulation | uses 9–10 | ok | fails with 9–10 |
| 12 | Lemma 7.2–7.3 (disk averages) | any `k` | ok | ok |
| 13 | **Prop. 7.1** | simple cycle in `K_k`: `3 <= ell <= k` | `ell ∈ {3,4,5}` | **`ell ∈ {3,4,5,6}`** |
| 14 | Lemma 7.5 cover obstruction | multiplicity `<= 2`, mesh `<= 2`; any `k` | ok | ok |
| 15 | Lemmas 7.6–7.8 (non-null loop, midpoints, annulus) | any finite graph; any `k` | ok | ok |
| 16 | Lemma 8.1, (8.1) | any `k` | ok | ok |
| 17 | **§8.2 five-cycle exclusion** | "almost every palette is a pair" | ok | **fails: triples** |
| 18 | **§8.3 four-cycle words** | 3-state system, Lemma 6.3 | ok | **fails** |
| 19 | **§8.4 triangle sectors** | `|T^c| = 2` (Thm B) | `2` | **`3`** |
| 20 | **Lemma 8.6 local rigidity** | 2 colours alternate on an even unit path | ok | **no 3-colour analogue at hand** |
| 21 | **Lemma 8.7 one-orbit boundary** | 2-valued flip + Lemma 8.6 | ok | **fails** |
| 22 | Lemma 8.8 region (8.4) | uses the `ell = 3` labels only | ok | ok if 19–21 hold |
| 23 | Prop. 8.10 Moser | `chi(Moser) = 4 > 3` | ok | ok |

Rows 5 and 19 are the two instances of `k - 3 <= 2`.  Row 13 is the `ell <= k` inequality
that adds one new case at `k = 6`.  Rows 22–23 are k-independent (and are verified
independently in §6 below).

---

## 5. Certificates: the two k = 6 inferences are false

The enumerations are exact; run `python3 check_k.py`.  Quoted output is in
`check_k.out`.

**C1 (four-cycle locus, paper §6.3.1).**  Admissible palettes at a centre of the four-cycle
locus with cycle labels `0,1,2,3` are those with `1 <= |P| <= k-3` and `P` not contained in
a cycle edge (paper (6.2)).

```text
 k=5, palette bound 2: 7 admissible palettes, 2 of them cycle-label only:
   [0,2]   [1,3]
 k=6, palette bound 3: 33 admissible palettes, 6 of them cycle-label only:
   [0,2]   [1,3]   [0,1,2]   [0,1,3]   [0,2,3]   [1,2,3]
```
At `k = 5` the paper's claim "leaving precisely the two diagonals" is confirmed.  At `k = 6`
four further palettes appear, and each of them uses **both** diagonals `U = {0,2}` and
`V = {1,3}` (e.g. `{0,1,2}` contains `0,2 ∈ U` and `1 ∈ V`), so the canonical state of
§6.3.1 is not a function of the palette.

**C1b (mixed palette).**  At the `k = 6` four-cycle locus the palette `{0,2,4}` is
admissible (`|P| = 3 <= 3`, not inside an edge) and contains both the singleton group
`{X} = {4}` and the diagonal group `{0,2}`.  At `k = 5` the same palette violates the bound
`2`.  This is the concrete failure of the step "two different state groups would require at
least three palette labels, contradicting Proposition 5.6" — at `k = 6` three palette
labels are permitted.

**C2 (external alphabet, Theorem B).**  Output:

```text
 k=4: |Sigma| = 0   bipartite = True    states = []
 k=5: |Sigma| = 2   bipartite = True    states = [[3], [4]]
 k=6: |Sigma| = 6   bipartite = False   states = [[3],[4],[5],[3,4],[3,5],[4,5]]
      odd cycle: [[3], [4], [5]]
```

**C6 (the two failing inferences).**
```text
 unit equilateral triangle properly 3-coloured with labels 4,5,6: True {0:4, 1:5, 2:6}
 4-edge unit path, proper 3-colouring, endpoints differ:         True {0:4,1:5,2:6,3:4,4:5}
```
The first refutes the `k = 6` form of the last step of Lemma 6.4 ("the three forced points
lie in the `k-3` labels outside `{X} ∪ D`; a unit equilateral triangle cannot be properly
coloured"): at `k = 6` the complement has three labels and the triangle is colourable.  The
second refutes the `k = 6` form of Lemma 8.6: at `k = 5`, `s(Re) = -s(e)` makes the colours
alternate along any unit edge path, so four edges return the colour; with three labels no
such conclusion holds.

**C8 (the value `|A(e)| = 2` occurs at `k = 6`).**  Theorem B permits `|A(e)| ∈ {1,2}` at
`k = 6`; the following explicit measurable model shows that `2` is not excluded by any of
the palette-level hypotheses, i.e. that no argument using only `(5.2)`, `(5.7)`, `(8.1)` and
the bound `|P_x| <= 3` can force `|A| = 1`.  Label the labels `T = {0,1,2}` (cycle) and
`T^c = {3,4,5}` (outsiders), split the circle into the six arcs
`D_k = [k pi/3, (k+1) pi/3)`, `k = 0..5`, so that `R D_k = D_{k+1 mod 6}`, and set

```text
   A(e) = P_x(e) = {3,4}   for e in D_0 ∪ D_2 ∪ D_4 ,
   A(e) = P_x(e) = {5}     for e in D_1 ∪ D_3 ∪ D_5 .
```

Checks (`check_k.py`, C8): `1 <= |A| <= 2`; `A(e) ∩ A(Re) = ∅` everywhere (adjacent arcs
carry disjoint sets); `A ⊆ T^c`, so the palette meets `O(e)` and `I(e)` (both contain
`T^c`); `|P| <= 3`; `P` is never inside a cycle edge; and `|A| = 2` on a set of angular
measure `3 · pi/3 = pi`.  So at `k = 6` the state `A` is genuinely set-valued on a set of
positive angular measure as far as the paper's palette-level hypotheses are concerned.
This is a statement about the constraint system, not about a colouring: an actual occurrence
in a weak measurable 6-colouring would require `chi(R^2) <= 6`, which is the open problem.

**C4, C5 (the paper's own `k = 5` arithmetic, verified).**  `§8.2`: with indices in `Z/5`,
steps `±1`, six positions and antipodal positions accepting index differences `0, ±2`, an
exhaustive search over `{±1}^6` finds **no** admissible sequence (the paper's argument is
correct).  `§6.3.3`: `D_a ∩ D_b = ∅ ⟺ b - a = ±1 mod 5` holds for all ten pairs of
diagonals `D_i = {i,i+2}`.

---

## 6. The endgame is k-independent; exact verification of §8.5–8.6

Since rows 22–23 of the table carry all the chromatic content of the final contradiction, an
independent exact check of them is worth recording.  `check_moser.py` verifies, in rigorous
rational interval arithmetic (no floating-point decisions):

* **M1** all eleven edges of the seven-vertex graph (8.5) have length exactly `1`
  (`|x-y|^2 = 1` inside an interval of width `10^{-39}`);
* **M2** it has no proper 3-colouring (exhaustive over `3^7 = 2187` maps);
* **M3** with the placement `z_g = ((35+12i)/37) (g + (-290+149i)/250)`, all seven vertices
  satisfy `0 < |z_g|^2 < 4` and (8.4) `v^2 (3 xi^2 - v^2)^2 < l^3 (1-l/4)(l-1)^2`, and the
  seven coordinates agree with the paper's Table 1 to four decimals.

Note on (8.6): the shift is *inside* the bracket.  The literal reading
`((35+12i)/37) g + (-290+149i)/250` puts vertex `g = 0` at `(-1.16, 0.596)`, where (8.4)
**fails** (`P ≈ 4.81 > P' ≈ 1.39`); the reading used above reproduces Table 1 exactly.
Everything in §8.5–8.6 is therefore correct and independent of the number of labels,
because it uses only the three triangle labels and `chi(Moser) = 4 > 3`.

Consequently the `k`-threshold of the paper is *not* in the final chromatic step: a sixth
label does not call for a 5-chromatic unit-distance graph.  It is in rows 5, 13 and 19: the
two palette-counting bounds and the new cycle length.

---

## 7. What a six-label run needs: the exact obstruction

At `k = 6` the following three inputs are required, and none is available.

**(N1) A state theory for palettes of size 3 at cycle loci — or a 3-ary separation lemma.**
The paper's Proposition 5.6 pins the palette at `2` and every cycle analysis of §6.3 then
reads the *set* `P_x(e)` as a single state.  At `k = 6` the bound is `3` (Theorem A), and
C1/C1b exhibit admissible palettes that carry two state groups at once.  The only way the
paper's method can push `3` down to `2` is Lemma 5.5, and Lemma 5.5 does not extend:

> *Binary-center separation uses exactly one fact about the label set — that a nonempty
> subset of a 2-element set is a singleton.  For a 3-element set `T`, exclusion (5.2) at the
> two-angle representation `y + e^{it} = x + e^{i alpha_+(t)} + e^{i alpha_-(t)}` gives only
> `s_x(alpha_+(t)) ≠ s_y(t) ≠ s_x(alpha_-(t))`, which for `|T| = 3` carries no relation
> between `s_x(alpha_+(t))` and `s_x(alpha_-(t))`; the invariance of `s_x` under
> `H = alpha_+ ∘ alpha_-^{-1}`, and with it the entire expansion argument (5.9)–(5.11),
> is lost.*

The precise missing statement is: *for every fixed 3-element `T` there is `delta_T > 0`
such that two distinct centres that are `T`-ary are at distance `>= delta_T`*.  It is not a
consequence of (P1)–(P4): the derivation of (5.8) from (P2) uses only that the intersections
with `T` at `e` and `Re` are nonempty disjoint subsets, which for `|T| = 3` allows the pair
`({x_1},{x_2})` and the pair `({x_1},{x_2,x_3})` at successive positions — the nonsingleton
case is excluded at `k = 5` and permitted at `k = 6` (C2).

**(N2) An exclusion for interface cycles of length 6.**  By Theorem D, Proposition 7.1 at
`k = 6` returns `ell ∈ {3,4,5,6}`.  The paper has no `ell = 6` analysis.  At `k = 6` and
`ell = 6` all six labels lie on the cycle.  The run count of §8.2 ("two required runs of
length at least two plus the other two nonempty runs would occupy at least six positions",
a contradiction at `ell = 5`) is no longer a contradiction at `ell = 6`: the signs may
consist of two runs (lengths `(2,4)`, `(3,3)`, `(4,2)`) or of four runs (`2,1,2,1`).  The
allowed sets `O(e) ∩ T`, `I(e) ∩ T` are the internal vertices of the runs of length at least
two, so they have sizes between `1` and `3`; the palette bound `3` does not force the
palette to consist of one vertex from each set.  A new argument is required.  (At `k = 5`,
`ell = 5`, the paper's paragraph applies and, with palettes forced to be pairs by the bound
`2`, the `Z/5` parity argument rules the case out; I re-verified that arithmetic
exhaustively, C4.)

**(N3) A 3-valued sector theory for triangle interfaces.**  By Theorem B the external state
at `k = 6` has six admissible values with a non-bipartite disjointness graph, so the
"alternating sectors" structure of §8.4, the local rigidity of Lemma 8.6 and the one-orbit
boundary of Lemma 8.7 are all unavailable.  In particular the sector description
`sign sin(3 theta)` that produces the region (8.4) has no `k = 6` analogue from these
hypotheses: alternating two-valued data is replaced by data in which a pair-state forces the
complementary singleton at the next 60°-position (Corollary B2), a strictly weaker relation.

*Is (N3) repairable?*  A `k = 6` version of Lemma 8.6 would need, for every sufficiently
small displacement `h`, a finite unit-distance graph `G_h` with two marked vertices at
displacement `h` whose colour is the same in every proper 3-colouring of `G_h`; the paper's
gadget for two colours is the four-edge path of (8.3).  Call such a `G_h` a *3-equality
gadget at `h`*.  Two elementary facts delimit the cheap ones.

> **Lemma E.**  *(i) No graph on three vertices is a 3-equality gadget (with the convention
> that a gadget must itself be 3-colourable, so that the condition is not vacuous).
> (ii) The diamond `K_4 - e` is a unit-distance graph; its two apices are at distance
> exactly `sqrt 3`, and in every proper 3-colouring of the diamond they share a colour.*

*Proof.*  (i) Let `G` have vertices `a,b,c` and a proper 3-colouring.  If `a,b` are
adjacent they already differ; if not, recolour: give `c` its colour and `a,b` two different
remaining colours.  So no 3-vertex graph forces `a = b`.  (ii) Place
`p = 0, q = 1, c = (1 + i sqrt 3)/2, r = (1 - i sqrt 3)/2`; then `|p| = |q| = |p - q| = 1`,
`|c - p| = |c - q| = |r - p| = |r - q| = 1`, so the five unit edges form the diamond, and
`|c - r|^2 = 3`.  In a proper 3-colouring `p,q` differ, and both `c` and `r` must take the
third colour, so `c(c) = c(r)`.  ∎

(Verified by `check_gadget.py`: no 3-vertex gadget exists, the diamond has exactly six
proper 3-colourings and all give the apices one colour.)  The natural route to a small `h`
is: take `a, b` to be the two common unit neighbours of `c, c'` and force `c ≠ c'`
geometrically.  Then `a,b` are the two intersection points of the unit circles about `c,c'`,
so `|a - b| = sqrt(4 - d^2)` with `d = |c - c'|`, and one needs *forced difference* at
distance `d`.  Within this framework the cheapest forced-difference mechanism forces `c` to
take the colour of a vertex `p` of a unit triangle, which puts `|c - p| = sqrt 3`, and then
`|p - p'| = 1` requires `|2 sqrt 3 - d| <= 1`, i.e. `d >= 2 sqrt 3 - 1 > 2`, whence
`h^2 = 4 - d^2 < 0`.  That family is therefore empty, and by Lemma E the only 4-vertex
gadget gives `h = sqrt 3` only.  Whether a 3-equality gadget exists for small `h` (with
more vertices, or by another mechanism) I leave open; it is not needed for the conclusions
above, since (N1) and (N2) already block the run.

---

## 8. Summary

* The paper's architecture is a `k <= 5` argument.  Its label count enters in three forms
  (§0, Theorem C): the palette bound `|P_x| <= k-3` (Theorem A, `= 3` at `k = 6`), the
  external-state bound `1 <= |A(e)| <= k-4` at a triangle interface (Theorem B, `= 1` only
  at `k = 5`), and the cycle-length bound `ell <= k`.  The first two are the inequalities
  `k-3 <= 2` and `k-4 <= 1`, both equivalent to `k <= 5`.
* At `k = 6` the two inferences are false as stated, with explicit certificates:
  a unit equilateral triangle is properly 3-colourable; a four-edge unit path is properly
  3-colourable with distinct endpoint colours; the palette `{0,2,4}` is admissible at the
  four-cycle locus and carries two state groups; the external state alphabet has six
  elements and a non-bipartite disjointness graph.
* In addition the extracted interface cycle can have length `ell = 6` (Theorem D), a case
  the paper does not treat; and the "planar cover" obstruction is `k`-independent, not a
  `K_5` non-planarity argument.
* Everything else, in particular the final region and Moser step of §8.5–8.6, is
  `k`-independent and is verified here exactly.

## 9. The mandate's four candidate bottlenecks, answered

| Candidate | Exact k-dependence | Verdict at `k = 6` |
|---|---|---|
| palette size | `|P_x| <= k-3` (Thm A) | `3`, not `2`; genuinely set-valued states (C1, C1b) |
| diameter of the positive region (§7, mesh `<= 2`) | none: multiplicity `2` is "at most two positive barycentric coordinates" of a simplex one-skeleton, valid for every `k` | unchanged, `2` |
| cycle lengths `3,4,5` vs `3,4,5,6` | `3 <= ell <= k` (Thm D) | one new case `ell = 6`, no exclusion in the paper |
| Moser / parity exclusion | none: `chi(Moser) = 4 > 3` uses only the three cycle labels; the `Z/5` parity argument of §8.2 is internal to `ell = 5` | unchanged and verified exactly (M1–M3, C4) |

So the failure is not in the topological core (§7) and not in the chromatic endgame
(§8.5–8.6); it is in the two palette-counting steps, i.e. in the passage from "the palette is
a set of labels" to "the palette is a single state".

## 10. Reproduction

```text
 python3 check_k.py       # C1, C1b, C2, C3, C4, C5, C6, C7, C8  (exact, < 1 s)
 python3 check_gadget.py  # E1, E2, E3                            (exact, < 1 s)
 python3 check_moser.py   # M1, M2, M3                            (exact interval arithmetic)
 python3 check_seven.py   # the appendix, §1 constants            (exact)
```
Outputs are saved as `check_k.out`, `check_gadget.out`, `check_moser.out`,
`check_seven.out`.

---

## Appendix: the paper's §1 seven-colouring, verified with its actual constants

Independent of the lower bound and of the `k`-analogue, but it belongs to the same
"is the constant what the paper says" check.

The paper's §1 upper-bound paragraph reads (page 2, checked against the PDF word
coordinates):

> "Take Voronoi hexagons of a triangular lattice, each with circumradius `r = 2/5`.
> Their centers have nearest-neighbor distance `sqrt 3 r`. ... Distances inside one hexagon
> are at most `2r < 1`. Centers of distinct same-color hexagons are at least `sqrt(21) r`
> apart, so points in those hexagons are at least `(sqrt(21) - 2) r > 1` apart."

Both inequalities hold at `r = 2/5`:

```text
     2r = 4/5 < 1                      (exactly: 4 < 5)
     (sqrt 21 - 2) r = 2(sqrt21 - 2)/5 > 1
        <=>  2 sqrt 21 > 9  <=>  84 > 81          (squaring, both sides positive)
```

numerically `2r = 0.8` and `(sqrt 21 - 2) r = 1.03303 > 1`.  The scheme's two constraints
are `2r < 1` and `(sqrt 21 - 2) r > 1`, i.e. `1/(sqrt 21 - 2) < r < 1/2`, that is
`0.38721 < r < 0.5`; `r = 2/5 = 0.4` lies inside this window with the margins above.  With
the index-seven sublattice (`|2 - omega|^2 = 7` for `omega = e^{2 pi i /3}`, so same-colour
centres are at distance `sqrt 7 · sqrt 3 r = sqrt 21 r`), closed Voronoi hexagons and
boundary points assigned to any incident hexagon, the colouring is proper, including all
boundaries, and `chi(R^2) <= 7`.  Exact checks: `check_seven.py`.

**Text-extraction warning.**  The layout extraction `.scratch/paper.txt` prints the radical
of `sqrt 3 r` at the end of the preceding line, next to "triangular lattice", which makes the
line read `circumradius r = sqrt(2/5)` if one takes the extraction literally.  The PDF word
coordinates settle it: the line at `y = 627` carries "circumradius r = 2/5." (word `2/5.` at
`x = 420.8`), and the radical belongs to `sqrt 3 r` on the line at `y = 641`.  So `r = 2/5`.
No defect: with `r = 2/5` the two witness points of a "two points inside one hexagon at
unit distance" argument do not both lie inside the hexagon (the inradius is
`r sqrt 3 / 2 = 0.3464` and `2r = 0.8 < 1`).

The Lean route (`OAI.Problem160.properColoring_seven`) does not use this scheme; it uses the
triangular lattice of spacing `4/5`, whose covering radius is `(4/5)/sqrt 3 = 0.4619`, below
the `7/15 = 0.4667` that its covering lemma allows, and same-colour lattice points are at
distance `sqrt 7 · 4/5 = 2.1166 > 2`, so for same-colour `x, y`,
`dist x y >= 2 - 2(4/5)/sqrt 3 = 1.0762 > 1`.
