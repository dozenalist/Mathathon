# A k = 6 palette theorem: three-label palettes occupy at most half the directions

Member m11, sprint B. Direction d6 (formalisation + verified finite certificate of the
k = 6 palette spine).

**Summary.**

1. *Theorem 2 below (proved, and machine-checked in `lean/K6Ternary.lean`).* For a weak
   measurable 6-colouring, at every centre `x` the set of directions whose maximal palette
   has three labels has angular measure at most `1/2`.
2. *Theorem 3 (proved).* For any nonempty label set `T` and any centre, the directions
   whose palette contains `T` have measure at most `1/2`; in particular no centre has an
   almost-everywhere constant palette, at any `k`. At a `k = 6` triangle centre this gives:
   the palette equals the whole triangle triple on at most half the directions, so it meets
   the outsider triple on at least half.
3. *Decided finite computation (two independent procedures).* The complete single-centre
   palette state systems at a `k = 6` cyclic centre are enumerated exactly for all four
   cycle lengths `3,4,5,6`: the maximal three-label density is `1/2` in every case (so
   Theorem 2 is sharp for the constraint list), and in every case some admissible system
   admits **no** fixed pair meeting all palettes. At `k = 5` the same computation reproduces
   the paper's triangle conclusion: all `2600` admissible triangle state systems are binary
   for the outside pair. This is the exact quantitative content of the `k = 5 -> k = 6`
   degradation of the triangle interface.
4. *Not proved, and not claimed:* the bound `|P_x(e)| <= 2` at `k = 6`. Section 6 says
   exactly why the constraint list used here cannot give it.

Everything is stated for a **weak measurable** `k`-colouring with the notation of the paper
(Definition 5.1 for palettes, Lemma 5.2 for the exclusions).

---

## 1. Setting, and what is actually available at a single centre

Labels `I`, `|I| = k`; `S = S^1` with normalised angular measure `sigma`; `R` = rotation of
directions by `kappa = pi/3`; `P_x(e)` the maximal palette of paper Definition 5.1
(a measurable set-valued function of `e`, defined up to angular null sets).

The printed facts used below, quoted with their exact hypotheses.

* **(5.2)** *(Lemma 5.2 part 1; every fixed centre `x`, every `k`)*
  for almost every independent-angle pair `(e,v) in S x S`,
  ```
      c(x + e + v)  not in  P_x(e)  union  P_x(v) .
  ```
* **(5.3)** *(Lemma 5.2 part 3)* on any arc where there is a smooth representation
  `z + f = x + s(f) + t(f)` with `s(f), t(f)` nonparallel and `s` a local diffeomorphism of
  the angular coordinate, `P_z(f) ∩ P_x(s(f)) = empty` a.e.  Remark 5.3 records the special
  case `(x+a) + f = x + f + a`, admissible for every `|a| = 1` except at `f = ±a`; this is
  the **two-centre translation exclusion**
  ```
      P_{x+a}(f) ∩ P_x(f) = empty          (a.e. f, every unit a).
  ```
* **(5.7)** *(Corollary 5.4; single centre, 60 degrees)* `P_x(f) ∩ P_x(Rf) = empty` a.e.
* **Palette bound at `k = 6`** *(Proposition 5.6's method, `results/K6-BARRIER.md` §1)*
  `1 <= |P_x(e)| <= k - 3 = 3` a.e.
* **(6.2)** *(Lemma 6.2; `ij` an edge of the transition graph `Gamma_x`)*
  `P_x(e)` is not contained in `{i,j}` for a.e. `e`.

**Warning, and a correction I had to make in my own computation.** It is tempting to add a
*120-degree* single-centre exclusion `P_x(f) ∩ P_x(R^2 f) = empty`. **No such statement
follows from (5.3).** At a single centre (`z = x`) the representation reads
`x + F = x + s(F) + t(F)`, i.e. `s(F) + t(F) = F` with `|s| = |t| = |F| = 1`; every such
triple has `s` and `t` at `120` degrees *to each other* and each at `60` degrees *to `F`*.
So (5.3) at a single centre republishes (5.7) and gives nothing at `120` degrees. The
finite model in §5 was first written with the false 120-degree constraint and it is what
made the system unsatisfiable at `k = 5` (a visible symptom: no admissible state system at
all for the `k = 5` triangle). With the constraint removed the model reproduces the paper's
`k = 5` conclusion, which is the non-vacuity check of §5.3.

Two-centre facts are used only in §6 (informally); Theorems 2 and 3 are single-centre.

---

## 2. The complementary-palette exclusion at `k = 6`

**Lemma 1.** Let `k = 6`. For every centre `x` and almost every pair `(e,v)`,
`P_x(e) union P_x(v) != I`. In particular (taking `v = Re`)
```
     |P_x(e)| = 3  and  |P_x(Re)| = 3   fail simultaneously a.e.,
```
and at most one of two palettes at 60-degree separation has three labels.

*Proof.* (5.2) produces a point `x + e + v` whose colour is outside `P_x(e) union P_x(v)`;
a colour exists at every point, so the union cannot be all of `I`. For `v = Re`, (5.7)
makes the two palettes disjoint; two disjoint subsets of a six-element set with three
elements each are complementary, so their union is `I`, contradicting the first sentence.
The pair `(e, Re)` is a null set of the (5.2)-exceptional family because `e -> (e,Re)` is a
smooth embedding. ∎

**Corollary 1a.** At `k = 6`, no centre has a complete transition graph: `Gamma_x != K_6`.

*Proof.* If all fifteen pairs are edges, (6.2) forbids every palette of size at most two
(each two-element set is an edge, and each singleton is contained in one), so `|P_x(e)| = 3`
for a.e. `e`, contradicting Lemma 1. ∎

The label count is the point: two disjoint `(k-3)`-element palettes need `2(k-3) <= k`
labels, i.e. `k <= 6`; and at `k = 6` they are *exactly* complementary, which is what (5.2)
forbids. At `k = 5` two disjoint pairs fit easily (that is why binary centres exist at
`k = 5`, Lemma 5.5), and at `k >= 7` disjoint `(k-3)`-palettes do not fit at all. The
`k = 6` case is the unique one in which (5.2) and (5.7) interact.

---

## 3. Main theorem: three-label palettes have density at most `1/2`

**Theorem 2.** Let `k >= 6` and let `c` be a weak measurable `k`-colouring. For every centre
`x`,
```
     sigma { e in S : |P_x(e)| = k - 3 }  <=  1/2 .
```
At `k = 6`: the directions carrying a three-label palette have angular measure at most `1/2`.

*Proof.* Write `E = {e : |P_x(e)| = k-3}` and `E' = R^{-1}(E) = {e : |P_x(Re)| = k-3}`.
By (5.7), `P_x(e)` and `P_x(Re)` are disjoint a.e.

*Case `k = 6`.* If `e in E ∩ E'`, both palettes have three labels and are disjoint, hence
complementary, so their union is `I`, contradicting Lemma 1. Hence `E ∩ E'` is null. Since
`E ∪ E'` is contained in the probability space `S` and `mu(E') = mu(E)` (R preserves angular
measure), `2 sigma(E) = sigma(E) + sigma(E') = sigma(E ∪ E') <= 1`.

*Case `k >= 7`.* Two disjoint sets of `k-3` elements would need `2(k-3) >= 8 > k` labels,
so `|P_x(e)| = |P_x(Re)| = k-3` already contradicts (5.7); again `E ∩ E'` is null and the
same counting applies. ∎

**Remarks.**

* Only (5.2) and (5.7) are used; no transition-graph input, no two-centre input, no
  regularity of the colouring beyond weak measurability.
* *Sharpness inside the constraint list.* §5 exhibits, for `k = 6`, admissible state systems
  (satisfying (5.2), (5.7), the palette bound, nonemptiness, and the (6.2) exclusions of a
  label cycle of any length `3,4,5,6`) in which three of the six directions of an
  `R`-orbit carry three labels. So `1/2` cannot be improved by any argument that uses only
  those constraints, and in particular it does not give `|P| <= 2`.
* *Consistency with the swarm's explicit objects.* Member m3's explicit proper measurable
  7-colouring with accumulating cyclic centres (direction d11,
  `.ultramath/smwfo9zkl/m3/w/verify.py`) has `|P_x(e)| <= 3` everywhere, so at `k = 7` the set
  `{|P_x| = k-3 = 4}` is empty there and Theorem 2 is satisfied with room to spare — the
  bound constrains only the hypothetical case in which a palette reaches the general-k bound
  `k-3`. Member m13's `k = 6` palette model with the triangle at every point (direction d5,
  `.ultramath/smwfo9zkl/m13/model_check2.py`) has `|P| = 2` everywhere, so
  `sigma{|P| = 3} = 0` there. Both are consistent with Theorem 2, and neither can test its
  sharpness; that is done by the finite models of §5.
* *Non-vacuity.* At `k = 5` the statement is `sigma{|P_x| = 2} <= 1/2`, which is **false** as
  a constraint-level statement (§5: the maximum is `6/6`) and is not asserted: the theorem
  starts at `k = 6`, exactly where `2(k-3) <= k` begins to bite. The argument therefore does
  not kill the case `k = 5`, in which binary centres provably exist (paper Lemma 5.5).

---

## 4. No almost-everywhere constant palette; the triangle interface at `k = 6`

**Theorem 3.** Let `k >= 3`, let `T` be a nonempty set of labels, and let `x` be any centre.
Then
```
     sigma { e in S : T subset P_x(e) }  <=  1/2 .
```
In particular `T` is not contained in `P_x(e)` for almost every `e`.

*Proof.* Write `F = {e : T subset P_x(e)}`. If `e in F ∩ R^{-1}F` then `T subset P_x(e)` and
`T subset P_x(Re)`, so `P_x(e) ∩ P_x(Re)` is nonempty, contradicting (5.7). Hence
`F ∩ R^{-1}F` is null and the counting of Theorem 2 applies. ∎

**Corollary 4 (triangle interface at `k = 6`).** Let `T = {i_0,i_1,i_2}` be the labels of a
triangle in `Gamma_x`, and `O = I \ T` the outsider triple. Then
```
     sigma { e : P_x(e) = T }  <=  1/2 ,       sigma { e : P_x(e) ∩ O != empty }  >=  1/2 .
```
*Proof.* By (6.2) for the three cycle edges, `P_x(e)` is contained in no pair of `T`. A
nonempty palette of at most three labels that is contained in no pair of `T` is either `T`
itself (when it misses `O`) or meets `O`. So
`{e : P_x(e) ∩ O = empty} = {e : P_x(e) = T}` up to a null set, and Theorem 3 bounds its
measure by `1/2`. ∎

**Contrast with `k = 5`.** At `k = 5` the same computation with `|P| <= 2` and a two-element
outsider set gives `P_x(e) ∩ O != empty` for **almost every** `e`, with (5.7) then making the
intersection a singleton that alternates at an `R`-step — the binary centre of paper
Theorem 6.5's triangle case, from which Lemma 5.5 gives local finiteness. At `k = 6` the
outsider set has three labels and the conclusion degrades from "a.e." to "at least half the
directions"; §5 shows that the degradation is not an artefact of the proof: in admissible
state systems the palette can equal `T` on exactly half the directions.

---

## 5. A decided finite computation: the single-centre state systems at a cyclic centre

The only `k`-dependent input of §7 is a finiteness property of the cyclic locus
(paper Theorem 6.5); member m5 (direction d4, `.ultramath/smwfo9zkl/m5/K6-CYCLIC-LOCUS.md`)
shows that what §7 actually consumes is: *some* closed square of side `> 2` meets
`L = {x : Gamma_x contains a cycle}` in finitely many points, and that nonemptiness of `L`
at every `k >= 3` is already proved. What is missing at `k = 6` is therefore the isolation
of the cyclic centres. This section decides, exactly, what the printed single-centre
constraints say about a centre whose transition graph contains a cycle of length `ell`, for
`ell = 3,4,5,6`.

### 5.1 The finite model

Directions: the six elements `t = 0,...,5` of one `R`-orbit (all exclusions below involve
only 60-degree separation, so an orbit is the natural finite quotient). Labels `I`,
`|I| = k`. A model assigns to each `t` a palette `P(t)`, a nonempty subset of `I` with
`|P(t)| <= k-3`, subject to

| constraint | paper source | imposed |
|---|---|---|
| `P(t) ∩ P(t+1) = empty` | (5.7) | for all `t` |
| `P(t) ∪ P(t') != I` | (5.2) | for all `t,t'` |
| `P(t)` not contained in any edge of the label cycle `C_ell` | (6.2) | for all `t` |

All three hold a.e. in the paper; they are imposed on all six positions and all pairs, so the
finite model is a **strengthening**. A satisfiable model therefore shows that the paper's
constraints do not refute it; an unsatisfiable one would be a genuine contradiction. The
model is *not* claimed to be realised by a colouring of the plane (no model of the joint
a.e. structure is asserted anywhere in this note).

### 5.2 Results (exact, two independent procedures)

`N` = number of admissible state systems; "heavy" = three labels at `k = 6`;
"hitting pair" = a two-element label set meeting every palette (the conclusion the paper's
triangle case needs).

| `k` | cycle length | palettes | systems `N` | max heavy per orbit | systems with no hitting pair |
|---|---|---|---|---|---|
| 5 | 3 | 9 | 2600 | 6 (i.e. all; heavy = `|P| = 2`) | **0** |
| 6 | 3 | 35 | 967464 | 3 | 587712 |
| 6 | 4 | 33 | 388796 | 3 | 192348 |
| 6 | 5 | 31 | 131790 | 3 | 54180 |
| 6 | 6 | 29 | 36228 | 3 | 9372 |
| 7 | 3 | 92 | – (MILP only) | 3 | – |

* The palette counts per cycle length (`35, 33, 31, 29` at `k = 6`, `9` at `k = 5` for the
  triangle) agree with the independent computation of member m5 (direction d4,
  `.ultramath/smwfo9zkl/m5/cycle_strata.py`), which used a different method (closed-form
  count `sum_{j=1}^{k-3} C(k,j) - 2 ell` plus brute force).
* **Sharpness of Theorem 2** at `k = 6`: the maximum of `#{t : |P(t)| = 3}` is `3` out of
  `6`, in every one of the four cycle lengths; a witness is
  `(T, {3}, T, {3}, T, {3})` with `T = {0,1,2}` for the triangle cycle (adjacent palettes
  disjoint, unions proper, `T` contained in no triangle edge). The same maximum `3` holds at
  `k = 7` (heavy = four labels), where it follows from (5.7) alone.
* **The `k = 5` control** reproduces paper Theorem 6.5's triangle step exactly: every one of
  the `2600` admissible systems is binary for the outside pair `{3,4}` (in fact every
  admissible `k = 5` palette contains `3` or `4`). This is the non-vacuity test: the model
  agrees with the known `k = 5` conclusion.
* **The `k = 6` obstruction** is exact: for every cycle length there are admissible systems
  in which no pair meets all six palettes, e.g. for the triangle
  `(T, {3}, T, {3}, T, {4})` with `T = {0,1,2}`: any pair would have to contain `3`, `4` and
  an element of `T`. So no argument from (6.2) + (5.7) + (5.2) + the palette bound alone can
  produce the `k = 5` triangle mechanism (a fixed binary pair, hence Lemma 5.5) at `k = 6`.
  Something genuinely new — a two-centre or transition-set input — is required.

### 5.3 Procedures and certificates

`verify/state_models.py` decides the questions twice, in two code paths:
**A.** a streaming depth-first enumeration with incremental pruning over the six positions,
which counts the admissible systems, the maximal number of heavy positions, the systems with
no hitting pair, and the maximal number of directions occupied by each individual palette
value. **B.** a 0/1 integer program handed to `scipy.optimize.milp` (HiGHS branch and bound),
maximising the heavy count and separately searching for a model with no hitting pair (one
witness direction per candidate pair). A and B agree on every entry of the table. For
`k = 5`, where the search space is small, a third, independent plain product enumeration
reproduces the count `2600`. Raw output: `verify/state_models_results.json`.

Run:
```
python3 verify/state_models.py        # ~70 s
```

### 5.4 The two-centre exclusion does not improve `1/2` on a seven-centre configuration

Take the seven centres `x` and `y_e = x + e^{i e kappa}`, `e = 0,...,5`, and six directions
per centre. The unit-separated pairs among the seven centres are `(x, y_e)` for all `e`, and
`(y_e, y_{e±1})`; the pairs `(y_e, y_{e±2})` and `(y_e, y_{e+3})` are at distance `sqrt 3`
and `2`. The explicit assignment (`T = {0,1,2}`)

```
  P_x(f)      = T        (f even),      {3}  (f odd)
  P_{y_e}(f) = {3} or {4} (f even, according to e mod 2),  {0} or {1} (f odd)
```

satisfies: nonemptiness and `|P| <= 3`; the 60-degree exclusion at every centre; the (5.2)
union constraint at every centre; the two-centre translation exclusion at **all twelve**
unit-separated centre pairs; and (6.2) for the triangle cycle on `T` at `x`. It has
`|P_x(f)| = 3` for three of the six directions. Hence no argument that uses only these
palette-level constraints, on this configuration, can improve the constant `1/2` of
Theorem 2, and in particular none can give `|P| <= 2`.

Certificate: `verify/joint_centres.py` (exact integer bitmasks; distances checked in exact
arithmetic, the squared distance being `2 - 2 cos((a-b)pi/3) in Z`).

```
python3 verify/joint_centres.py   # prints the twelve unit pairs, 3 of 6 heavy, ALL CONSTRAINTS PASS
```

What this certificate does **not** contain is an actual colouring function: no colour is
assigned to any point of the plane. It is a statement about palettes only, which is exactly
the level at which Theorems 1-3 live.

---

## 6. What this does not give, and why

1. `|P_x(e)| <= 2` at `k = 6` — the input `results/K6-BARRIER.md` §5 asks for — is **not**
   proved here. Theorems 2 and 3 bound how much of the direction circle can carry three
   labels (`1/2`), not whether any can.
2. §5 shows that the printed single-centre constraints plus the `(6.2)` exclusions of a label
   cycle cannot give it: at every cycle length there are admissible systems with a heavy
   palette on half the directions, and §5.4 sharpens this to a seven-centre system that also
   satisfies the two-centre translation exclusion at every unit-separated pair of the seven
   centres. So a proof of `|P| <= 2` at `k = 6` has to use an input absent from that list —
   in particular something that uses the *joint* a.e. structure over more centres than a
   single orbit's worth, since the pairwise two-centre exclusions are not enough.
   The shape such an input must have is visible from the following observation. Suppose `e`
   is a heavy direction at `x` with `P_x(e) = T`, and let `y_j = x + exp(i(theta + j kappa))`,
   `j = 0,1,2`, be the three equilateral vertices (each at distance one from `x`, and pairwise
   at distance one). The three palettes `P_{y_j}(e)` are then pairwise disjoint nonempty
   subsets of the three-element set `I minus T`, so they are its three singletons. Thus a
   heavy direction at `x` forces a *singleton palette at three centres*; and if the same
   happens on a set of directions
   of positive measure then, by the argument of §5, those singletons may vary with the
   direction, which is exactly why the `R`-alternation of (5.7) no longer produces a
   contradiction. Making that step — turning "singleton for a positive-measure set of
   directions" into a contradiction — is what a `k = 6` triangle-locus proof needs. I did not
   find it.
3. Nothing here is a statement about `chi(R^2)`. No 6-colouring is constructed and no
   contradiction is derived from the existence of one.

---

## 7. Files and exact commands

| file | content |
|---|---|
| `k6-ternary-palette.md` | this document: Theorems 2 and 3, Corollary 4, the finite classification, the gap |
| `lean/K6Ternary.lean` | machine-checked: two disjoint 3-subsets of `Fin 6` are complementary; `2 * mu {e : |P e| = 3} <= 1` from (5.2) + (5.7) + `R`-invariance; no a.e.-constant palette |
| `lean/K6Finite.lean` | machine-checked with light imports: the same finite lemma, its contrapositive, the six-cycle independent-set bound `<= 3` (by `decide`), and its attainment |
| `verify/state_models.py` | the two independent decision procedures of §5 |
| `verify/state_models_results.json` | raw output of the above |
| `verify/joint_centres.py` | exact certificate of §5.4: density `1/2` survives the two-centre exclusion on the seven-centre configuration |

```
lean lean/K6Finite.lean        # ~1 min
lean lean/K6Ternary.lean       # ~5-15 min (imports only measure theory + Finset)
python3 verify/state_models.py # ~70 s
```
All three were run in this VM: `K6Finite.lean` and `K6Ternary.lean` compile with no errors
(the only output of the second is three `Set.mem_setOf_eq` deprecation warnings), and the
Python run prints the table of §5.2 and writes the JSON.

### Hypothesis audit against the paper

| step | hypothesis used | available at `k = 6`? |
|---|---|---|
| Lemma 1 | (5.2) for a.e. pairs; (5.7); existence of a colour at each point | yes, (5.2) and (5.7) are Lemma 5.2 and Corollary 5.4, valid for every `k >= 3` |
| Theorem 2, `k = 6` | as Lemma 1, plus "two disjoint 3-subsets of a 6-set are complementary" | yes; the label count uses only `|I| = 6` |
| Theorem 2, `k >= 7` | (5.7) only | yes |
| Theorem 3 | (5.7); `T` nonempty | yes |
| Corollary 4 | (6.2) for the three triangle edges; palette bound `|P| <= 3` | yes, `results/K6-BARRIER.md` §1 |
| §5 model | (5.7), (5.2), palette bound, (6.2) | yes; all imposed as strengthenings |

No step uses Proposition 5.6 at `k = 5` (it is false at `k = 6`), none uses Theorem 6.5 or
Proposition 7.1, and none uses the two-centre exclusion.
