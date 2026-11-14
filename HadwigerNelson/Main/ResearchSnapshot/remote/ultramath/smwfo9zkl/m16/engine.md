# The separation engine at six colours

**Swarm direction d8 (member m16).** The paper's geometric obstruction (§5.4, §6, §7, §8) is
driven by one engine: a *separation lemma*. At five colours the engine consumes a **complement of
size two**. This document

1. proves the engine in the exact generality the argument needs (**Theorem A**: any two disjoint
   label groups whose union misses exactly two labels cannot alternate around a centre) — new at
   `k = 6`, and it gives genuine six-colour statements (Corollaries 3.1–3.3);
2. records precisely where `|P| <= 2` is used at each step of §6–§7, and certifies by a decided
   finite computation that **no** cycle stratum at `k = 6` is forced into the engine's format
   (§4, two independent programs, certificates in `work/`);
3. proves that the sum construction powering the engine has a hard ceiling at complement size two:
   with a single state shift it forces a configuration of chromatic number at most three
   (**Theorem E** and the certified computation of §5), so it cannot decide the complement-three
   case — in particular it cannot give `|P_x(e)| <= 2` at `k = 6`. §5.5 states the exact geometric
   property a six-colour engine would need.

Everything the paper supplies is cited, not re-derived; every constant taken from a *displayed*
formula was checked numerically (`work/verify_formulas.py`, output quoted in §1.2).

---

## 1. Setting, and exactly what is taken from the paper

### 1.1 Notation and the paper's statements used

`k` labels `I = {1,...,k}`; a weak measurable colouring `c : R^2 -> I` with colour classes `A_i`;
`kappa = pi/3`; `R` = rotation of the angular circle by `kappa`; `S = S^1` with angular measure
`sigma`; `P_x(e)` the maximal palette at centre `x` in direction `e` (Definition 5.1);
`D_{x,i} = {e : i in P_x(e)}`; `Gamma_x` the transition graph on `I` (Definition 6.1);
`L = {x : Gamma_x contains a cycle}`.

Quoted from the paper (`attachments/here-are-three-files-ni5n/paper.pdf`):

* **(5.2)** (Lemma 5.2.1): for a.e. independent-angle pair `(e,v)` in `S x S`,
  `c(x+e+v) not in P_x(e) union P_x(v)`.
* **Lemma 5.2.2**: if `e` is an angular density-one point of `D_{x,i}`, then for every `v`
  nonparallel to `e` the *spatial* density of `A_i` at `x+e+v` is zero.
* **Lemma 5.2.3 / (5.3)**: for a smooth representation `z+f = x+s(f)+t(f)` with `s,t` nonparallel,
  `P_z(f) cap P_x(s(f)) = empty` a.e. (the two-centre constraint).
* **(5.7)** (Corollary 5.4): `P_x(f) cap P_x(Rf) = empty` a.e.
* **Lemma 5.5** (binary-centre separation): for every fixed pair of labels, any two distinct
  centres *binary* for that pair are at distance at least an absolute `delta_* > 0`.
  (Binary for `{i+,i-}`: `P_x(e) cap {i+,i-}` is a nonempty singleton a.e.)
* **Lemma 6.2 / (6.2)**: `ij in Gamma_x` implies `P_x(e)` is not a subset of `{i,j}` for a.e. `e`.
* **Lemma 6.3** (strict state separation): states `A,B` at `x` representing disjoint label groups
  whose union is `I \ {X}`; at nonparallel density-one directions the sum has density one of the
  single label `X`, so the closed essential support of `B` contains no pair at chordal distance one.
* **Lemma 6.4** (singleton–pair alternation is impossible): at a fixed centre, no measurable state
  function with only the two values `{X}` (singleton) and `D` (a fixed disjoint pair), changing
  state under `R` a.e.
* **Proposition 5.6**: `1 <= |P_x(e)| <= 2` a.e. at `k = 5`; general `k`: `|P_x(e)| <= k-3`
  (`results/K6-BARRIER.md` §1 for the paper's method at general `k`).
* **Theorem 6.5**: `L` is closed and locally finite (`k = 5`).

**Convention.** A *state function with values in a family `G` of label groups* is a measurable
`sigma : S -> G` such that `sigma(e) <= P_x(e)` for a.e. `e`. It *changes state under `R`* if
`sigma(t+kappa) != sigma(t)` a.e.; writing `A_0 = {sigma = A}` this is
`1_{A_0}(t+kappa) = 1 - 1_{A_0}(t)` a.e.

### 1.2 Numerical check of the displayed formulas the engine uses

`python3 work/verify_formulas.py`:

```
gamma             = 0.5856855434571511
cos(gamma)        = 0.8333333333333333     (paper, Lemma 6.4: 5/6)            OK
2cos(gamma)       = 1.6666666666666665     (= 5/3: rational algebraic integer, not an integer)
|1-e^{i gamma}|   = 0.5773502691896258     (1/sqrt 3 = 0.5773502691896258)     OK
z_j = x + e^{i(t+2j kappa)}(1-e^{i gamma}), j = 0,1,2:
   distances to x     = [0.5774, 0.5774, 0.5774]
   pairwise distances = [1.0, 1.0, 1.0]                                        OK
diadic identity y + e^{it} = x + e^{i alpha+} + e^{i alpha-}: residual ~ 5e-16  OK
alpha+-(t) = t +- kappa - d sin t -+ d cos t / sqrt 3 + O(d^2): confirmed to O(d^2)
```

Hence `gamma = 2 arcsin(1/(2 sqrt 3))`, `cos gamma = 5/6`, `gamma/pi` irrational (as `2 cos gamma
= 5/3` is a rational algebraic integer that is not an integer), and `z_0,z_1,z_2` form a unit
equilateral triangle at distance `1/sqrt 3` from `x`.

### 1.3 Where `|P| <= 2` actually enters (audit)

| step | the line that needs the bound | at `k = 6` |
|---|---|---|
| Prop. 5.6, upper bound | complement of a `(k-2)`-set is a **pair** | transfers, gives `\|P\| <= 3` |
| Thm 6.5, triangle | "a nonempty subset of the three triangle labels of size at most two lies in some triangle edge, which is forbidden" — valid because `\|P\| <= 2` then forces `P` into `T` | **fails**: a palette can be `T` itself, or one triangle label plus an outsider (`{p,s}`), neither of which is a subset of a triangle edge |
| Lemma 6.6 (four-cycle continuity) | "Two different state groups would require at least three palette labels, contradicting Proposition 5.6" | **fails**: three labels are allowed |
| §6.3.3 (five-cycle) | "almost every palette is exactly one of its diagonals `D_i`" | **fails**: triples are palettes |
| §7 (one-skeleton) | palette is a pair, so the smoothed vector has two positive coordinates | **fails** (direction d1's problem) |
| §8 (cycle exclusions) | triangle interface: the outsider set is one label (`k-4 = 1`) | **fails**: `k-4 = 2` |

Theorem A below is what survives of the engine at `k = 6`: the bound `|P| <= 2` is *not* what the
alternation exclusion needs — what it needs is that the two state groups **miss exactly two
labels**.

---

## 2. Theorem A: the alternation engine in its natural generality

> **Theorem A.** Let `k >= 4`, `x` a centre of a weak measurable `k`-colouring, and `A`, `B`
> **disjoint nonempty** label groups with `|A| + |B| = k - 2`. Then there is no measurable state
> function at `x` with values `A`, `B` that changes state under `R`.

Spelled out with `A_0 = {e : A <= P_x(e)}`: there is no measurable `A_0` with
`1_{A_0}(t+kappa) = 1 - 1_{A_0}(t)` a.e., `A <= P_x(e)` a.e. on `A_0`, and `B <= P_x(e)` a.e. on
`S \ A_0`. The paper's Lemma 6.4 is the case `k = 5`, `|A| = 1`, `|B| = 2`: its complement `C` has
two elements. The theorem says **nothing in that argument uses `|A| = 1` and `|B| = 2`**; only
`|C| = 2` matters.

### 2.1 Proof

Put `C = I \ (A union B)`, so `|C| = 2`, and `gamma = 2 arcsin(1/(2 sqrt 3))`.

**Step 1 (the same-state set is not null).** Let `E = {t in S : 1_{A_0}(t) = 1_{A_0}(t+gamma)}`.
Then `sigma(E) > 0`.

*Proof.* If `sigma(E) = 0` then `1_{A_0}(t+gamma) = 1 - 1_{A_0}(t)` a.e., hence
`1_{A_0}(t+2gamma) = 1_{A_0}(t)` a.e.: `A_0` is invariant under rotation by `2gamma`, which is
ergodic since `gamma/pi` is irrational (§1.2). A measurable invariant set is null or conull, but
the alternation gives `sigma(A_0) = pi`. Contradiction. ∎

**Step 2 (a positive-measure set of admissible parameters).** For every fixed integer `m` the
identity `1_{A_0}(t+m kappa) = 1_{A_0}(t)` (`m` even) or `= 1 - 1_{A_0}(t)` (`m` odd) holds a.e.;
almost every point of `D_{x,i}` is a density-one point of `D_{x,i}` (Lebesgue); and the finitely
many directions occurring below are never parallel (a property of `gamma`, checked in Step 3).
Hence there is `Y <= E` with `sigma(Y) > 0` such that for every `t in Y`:

* `t + 2j kappa in A_0` and `t + pi + gamma + 2j kappa not in A_0` for `j = 0,1,2`
  (using `pi = 3kappa`, `1_{A_0}(t+gamma) = 1_{A_0}(t)` and the `2kappa`-invariance of `A_0`);
* each of those six directions is a density-one point of `D_{x,i}` for every `i in A`,
  respectively `i in B`.

**Step 3 (three forced sums).** For `t in Y` and `j = 0,1,2` put

```
z_j = x + e^{i(t+2j kappa)} + e^{i(t + pi + gamma + 2j kappa)}
    = x + e^{i(t+2j kappa)} (1 - e^{i gamma}).
```

The two unit summand directions differ by `pi + gamma`, neither `0` nor `pi` mod `2pi`, so they are
nonparallel; by Step 2 the first is in `A_0` (palette contains `A`) and the second outside (`B`).
Lemma 5.2.2, applied once for each `i in A` at the first direction and once for each `i in B` at
the second, gives: **the spatial density of `A_i` at `z_j` is zero for every `i in A union B`.**
Since `sum_i 1_{A_i} = 1` a.e., the union of the two colour classes of `C` has **spatial density
one** at each `z_j`.

**Step 4 (pairwise unit distance).** `|1 - e^{i gamma}| = 1/sqrt 3` and
`|1 - e^{2i kappa}| = |1 - e^{4i kappa}| = sqrt 3`, so for `j != j'`
`|z_j - z_{j'}| = |1-e^{i gamma}| |e^{2ij kappa} - e^{2ij' kappa}| = 1`. Also `|z_j - x| = 1/sqrt 3`.

**Step 5 (contradiction).** Put `C = {c_1,c_2}` and `U = A_{c_1} union A_{c_2}`; `U` has density
one at each `z_j`. Choose `r > 0` with `|U cap B(z_j,r)|/(pi r^2) > 3/4` for `j = 0,1,2`. For a
vector `v`, `|v| < r`, let `B_j = {v' : |v'| < r, z_j + v' not in U}`; then
`sigma(B_j) < (1/4) pi r^2`, so `sigma(B_0 union B_1 union B_2) < (3/4) pi r^2 < pi r^2`, and some
`v` satisfies `z_j + v in U` for `j = 0,1,2`. The points `z_0+v, z_1+v, z_2+v` are pairwise at
distance one yet carry only the two colours `c_1,c_2`; two of them share a colour and are at
distance one. This contradicts properness. ∎

### 2.2 Remarks

1. **Local form.** The proof uses the hypotheses only at the six directions attached to `t`. So the
   conclusion holds under the weaker hypothesis
   `sigma( Y_A cap (Y_A - 2kappa) cap (Y_A - 4kappa) cap (Y_B - pi - gamma) cap (Y_B - pi - gamma - 2kappa) cap (Y_B - pi - gamma - 4kappa) ) > 0`,
   where `Y_A = {e : A <= P_x(e)}`, `Y_B = {e : B <= P_x(e)}` and `Y - u = {t : t+u in Y}`,
   together with the density-one conditions of Step 2. The global form is the case
   `Y_A = A_0`, `Y_B = S \ A_0`.
2. **The complement size is what matters.** `|C| = 2` is used twice: to conclude that the sum has
   density one of `U` (four labels excluded) and, decisively, in Step 5, where three pairwise unit
   points must be coloured with `|C| = 2` colours. With `|C| = 3` — the six-colour case — three
   unit points *can* be properly coloured and the argument stops. §5 shows that this is a ceiling
   of the construction, not a defect of this proof.
3. The theorem is `k`-uniform.

### 2.3 What it specialises to, and the vacuity test

* `k = 5`, `|A| = 1`, `|B| = 2`: the paper's Lemma 6.4 verbatim.
* `k = 5`, `|A| = 2`, `|B| = 1`: the same with the two states exchanged.
* `k = 6`: the excluded alternations are exactly the shapes `(1,3)`, `(2,2)`, `(3,1)`.

Vacuity: the theorem cannot be tested against a known colouring (no colouring with `k >= 4` is
known to have a cyclic centre, and the hypotheses are about a single centre). The test that it does
not kill a known case is the `k = 5` one: there it *is* the paper's engine, used in the
machine-checked proof of `chi >= 6`. It is not applied at `k = 7` (there `|A|+|B| = 5` would need a
state of size `>= 4`, and `|P| <= 4` leaves the argument true but unused).

---

## 3. Six-colour consequences

Throughout `k = 6`, `x in L`, the cycle `Q <= Gamma_x` has length `ell`, vertex set `T` and edge set
`E(Q)`; (6.2) reads: `P_x(e)` is not a subset of `{i,j}` for `{i,j} in E(Q)`; (5.7) reads
`P_x(e) cap P_x(Re) = empty`; the palette bound is `1 <= |P_x(e)| <= 3`.

> **Corollary 3.1 (four-cycle, `k = 6`).** Let `Q` be a four-cycle with labels `0,1,2,3` in cyclic
> order and outsiders `X,Y`. Then `{e : P_x(e) <= {0,1,2,3}}` is angular null. Equivalently: at a
> six-colour four-cycle cyclic centre the palette contains an outsider for almost every direction.

*Proof.* Suppose `P_x(e) <= {0,1,2,3}` a.e. Singletons inside `{0,1,2,3}` and adjacent pairs are
excluded by (6.2) (each label of the four-cycle lies in a cycle edge); so the only pairs left are
the diagonals `{0,2}`, `{1,3}`. A triple `D` has complement inside `{0,1,2,3}` a single label,
excluded by (6.2); moreover a triple has no disjoint partner among the palettes (which all lie in
`{0,1,2,3}`), so (5.7) forbids triples. Hence `P_x(e) in {{0,2},{1,3}}` a.e., and (5.7) forces
consecutive values to differ, so the state function with values `A = {0,2}`, `B = {1,3}` changes
state under `R`. Since `|A|+|B| = 4 = k-2`, Theorem A contradicts it. ∎

> **Corollary 3.2 (triangle, `k = 6`).** Let `T = {p,q,r}` be a triangle in `Gamma_x` at `k = 6`
> and `O = {s,t,u}` the outsider triple. Then
> (a) every two-valued palette system `{A,B}` with `A,B` disjoint and `|A| + |B| = 4` is
> impossible; the instances include `{T}` with `{w}` (`w in O` fixed), `{p,s}` with `{q,t}`,
> `{s,t}` with `{p,u}`, and the full list is in `work/states_k5_k6_b.json`;
> (b) what survives is exactly the class allowed by (6.2) and (5.7): palettes are the singletons of
> `O`, the pairs meeting `O`, and the triples (35 values, of which `T` and `O` are disjoint and
> alternate with each other), subject only to consecutive disjointness.

*Proof.* (a) Theorem A, since (5.7) forces the state change. (b) A palette is excluded by (6.2)
exactly when it is a subset of a triangle edge, i.e. exactly the empty set, the three singletons of
`T` and the three edges; all other values with `1 <= |v| <= 3` occur, and the disjointness structure
is the one recorded in the table of §4.2 (`#occ = 35`). ∎

**Remark.** At `k = 5` the corresponding list has 8 values and *all* of them meet the outsider pair
in exactly one element, which is the paper's triangle argument; at `k = 6` the panel is
(i) singletons of `T` and triangle edges excluded, (ii) everything else present, in particular the
palette may be `T` itself or `O` itself or a mixed pair. The paper's conclusion "the palette
intersects the outsider pair in one label, alternating" is therefore **false** at `k = 6`, and the
class that Theorem A does remove is precisely the two-valued one.

> **Corollary 3.3 (kill list at `k = 6`).** Let `x` be a six-colour cyclic centre and
> `ell in {3,4,5,6}` the length of `Q`. Then no palette system at `x` takes exactly two values
> `A, B` that are disjoint with `|A| + |B| = 4`. The complete list of admissible pairs is machine-generated in
> `work/states_k5_k6_b.json` (key `thmA_targets`); e.g. for `ell = 4` it contains `{0,2}+{1,3}`
> (the two diagonals), `{0,2}+{4,5}` (a diagonal plus both outsiders), `{0,1,4}+{5}`; for
> `ell = 3` it contains `{0,1,2}+{3}` (the triangle plus a single outsider) and `{0,3}+{1,4}`.

*Proof.* Theorem A applied to the two values: disjoint groups of total size `k-2`, changing state
under `R` by (5.7). ∎

---

## 4. No six-colour cycle stratum is forced into the engine's format (certified computation)

### 4.1 The finite object

Fix `k` and a simple cycle `Q <= Gamma_x` of length `ell`. At a.e. direction the palette obeys
(P1) `1 <= |P| <= k-3`, (P2) `P` is not a subset of an edge of `Q`, (P3) `P(t) cap P(t+kappa) =
empty`. Since `6 kappa = 2 pi`, the orbit `t, t+kappa, ..., t+5kappa` is a 6-cycle in direction
space, so (P3) says exactly: **the six palette values on an orbit form a closed walk of length six
in the graph `G(k,ell)`** whose vertices are the values allowed by (P1)–(P2) that have at least one
disjoint allowed partner, edges joining disjoint values. Conversely every such closed walk occurs
(take `P` piecewise constant on `[j kappa, (j+1)kappa)`).

A paper-style engine is a quotient of palette values into few states; a two-state engine is a
**proper 2-colouring of `G(k,ell)`**, and it covers *every* palette system at that stratum exactly
when `G(k,ell)` is bipartite with the right group sizes (`G_a <= cap` of the values in class `a`,
`|G_0| + |G_1| = k-2` for Theorem A, `= k-1` for Lemma 6.3). This is a finite decision problem; it
is decided twice, by independent programs.

### 4.2 Result

`work/state_enum.py` (frozensets, BFS) and `work/state_enum2.py` (bitmasks, boolean-matrix
odd-walk detection in exact integer arithmetic) agree on every entry; `work/crosscheck.py`
re-verifies each certificate edge by edge in a third code path.

```
key        #occ  bip   #orbit_data  E1_pairs   E2    E3   certificate
k5_ell3       8  True     2600      [[3, 4]]   False False groups=[[3], [4]]
k5_ell4       7  False     362      []         -     -    odd cycle 3: [1,3]-[4]-[0,2]-[1,3]
k5_ell5       5  False     100      []         -     -    odd cycle 5: [2,4]-[0,3]-[1,4]-[0,2]-[1,3]-[2,4]
k6_ell3      35  False  1118252     []         -     -    odd cycle 3: [1,2,5]-[3]-[4]-[1,2,5]
k6_ell4      33  False   463840     []         -     -    odd cycle 3: [1,3,5]-[4]-[0,2]-[1,3,5]
k6_ell5      31  False   164630     []         -     -    odd cycle 3: [1,3,4]-[5]-[0,2]-[1,3,4]
k6_ell6      29  False    50792     []         -     -    odd cycle 5: [2,4,5]-[0,3]-[1,4,5]-[0,2]-[1,3]-[2,4,5]
```

(`#occ` = palette values occurring in some admissible orbit datum; `bip` = bipartite; `E1_pairs` =
label pairs met in exactly one element by every occurring value, i.e. the Lemma 5.5 format; `E2` /
`E3` = the group-size tests `|G_0|+|G_1| = k-2` resp. `k-1`.)

Reading.

* **`k = 5`, `ell = 3` (triangle).** There are 8 occurring values and **every one of them meets the
  outsider pair `{X,Y}` in exactly one element** (`E1` holds with the pair `{3,4}`; the pair `{X,Y}`
  itself never occurs, having no disjoint partner). That is precisely the paper's three-colour
  argument: the palette is binary for `{X,Y}` a.e., alternates, and Lemma 5.5 makes the locus
  locally finite. The program reproduces the paper's chain from the constraints alone — the
  non-vacuity test.
* **`k = 5`, `ell = 4, 5`.** Not bipartite: the paper's four- and five-cycle arguments are not
  two-state arguments; they use the canonical-state / continuity / transport mechanism of §6.3,
  whose essential step is *"two different state groups would require at least three palette
  labels, contradicting Proposition 5.6"* — exactly the sentence that fails at `k = 6`.
* **`k = 6`, all `ell`.** Every disjointness graph is non-bipartite, with an explicit odd cycle (for
  `ell = 3,4,5` a triangle of pairwise disjoint allowed palettes). Hence **no six-colour cycle
  stratum is forced into any two-state alternation format**: the palette system may use three
  states, and no two-state quotient alternates along every orbit. A six-colour engine must handle a
  complement of size three.

Certificate: `work/CERT-state-accounting.txt`, sha256
`ed3f7724d1e73b58c2e88913af0ed22499760d73557312b0f436091fd95cebc7`.

### 4.3 The palette systems that survive at `k = 6`

Explicitly: at a triangle centre the residual class is the 35 values listed in Corollary 3.2(b)
(i.e. everything except the singletons of `T` and the three triangle edges), with only consecutive
disjointness imposed; at a four-cycle centre the palette must contain an outsider for a.e.
direction (Corollary 3.1); at a five- or six-cycle centre the residual class is the value family
recorded in `work/states_k5_k6.json`. That is the exact class a six-colour engine must rule out,
and by §4.2 none of it is reachable by a two-state alternation.

---

## 5. Ceiling of the sum construction: complement three is out of reach for one shift

### 5.1 The construction in the form the engine uses it

Let `sigma : S -> {A,B}` be a state function at `x` changing state under `R`, `A_0` its `A`-set
(so `sigma(A_0) = pi`), `C = I \ (A union B)`, `c = |C|`, and `Y_gamma = {t : sigma(t+gamma) =
sigma(t)}` the *same-state* set of the shift `gamma`. For `t in Y_gamma` and `m in Z`,

```
z = x + e^{it} + e^{i(t + (2m+1)kappa + gamma)}
```

is a sum of two unit vectors whose directions carry opposite states, since
`sigma(t + (2m+1)kappa + gamma) = flip sigma(t+gamma) = flip sigma(t)`. So by Lemma 5.2.2 **the
colour of `z` lies in `C` with density one.** The engine of Theorem A and of the paper's Lemma 6.4
is this forcing followed by a unit-distance configuration built from such points.

### 5.2 Which shifts are available

> **Lemma 5.1 (good shifts are abundant, for every `sigma`).** Let `sigma : S -> {A,B}` be
> measurable with `sigma(t+kappa) != sigma(t)` a.e. Then
> `int int 1{sigma(t+gamma) = sigma(t)} dt dgamma = |A_0|^2 + |B_0|^2 > 0`; hence the set of
> `gamma` with `sigma(Y_gamma) > 0` has positive measure. Likewise the set of pairs
> `(gamma_1,gamma_2)` with `sigma{t : sigma(t+gamma_1) = sigma(t) = sigma(t+gamma_2)} > 0` has
> positive measure.

*Proof.* Fubini twice, using `sigma{u : sigma(u) = sigma(t)} = |A_0|` or `|B_0|` according to
`sigma(t)` (third power for pairs). Both are `pi > 0` by the alternation. ∎

> **Lemma 5.2 (conull-agreement shifts form a null subgroup).** `G_sigma = {delta : sigma(t+delta)
> = sigma(t) a.e.}` is a measurable subgroup of `S`, and it is null; the flip shifts are the coset
> `kappa + G_sigma`.

*Proof.* `G_sigma` is the zero set of the measurable function `delta |-> int |sigma(t+delta) -
sigma(t)| dt`, hence measurable, and it is a subgroup. A measurable subgroup of positive measure
contains an interval (Steinhaus), hence is open, hence all of `S`, which would make `sigma` constant
and contradict the `kappa`-flip. So `G_sigma` is null, and `sigma` flips under `delta` iff
`delta - kappa in G_sigma`. ∎

The paper's constant `gamma_0` is good *for every* `sigma`: if `gamma_0 - kappa in G_sigma`, then
`G_sigma` contains `2kappa` and `gamma_0 - kappa`, whose ratio `(3gamma_0/pi - 1)/2` is irrational,
so `G_sigma` is dense and hence (Lemma 5.2) all of `S`, contradiction. This is what lets Lemma 6.4
use a **single fixed** shift.

### 5.3 One shift forces all points onto three concentric circles

For a fixed good shift `gamma` the forced points are

```
z(m,j) = x + e^{i(t+2j kappa)} (1 + e^{i((2m+1)kappa + gamma)}),   m,j in {0,1,2}, t in Y_gamma,
```

using the `2kappa`-periodicity of `sigma`. For fixed `t` these nine points all lie on the **three
concentric circles** of radii `r_m(gamma) = 2|cos(((2m+1)pi/3 + gamma)/2)|`, `m = 0,1,2`.

> **Theorem E (one circle is never enough).** Let `G` be a unit-distance graph whose vertices all
> lie on one circle. Then `chi(G) <= 3`.

*Proof.* Two points of a circle of radius `r` are at distance one iff their angular difference is
`+-theta` with `2 r sin(theta/2) = 1` (no edges if `r < 1/2`; `theta = pi` if `r = 1/2`). So every
component of `G` lies in an orbit of the rotation by `theta`: a bi-infinite path (2-colourable) if
`theta/(2pi)` is irrational, a `q`-cycle (at most 3-colourable) if `theta/(2pi) = p/q`. ∎

At `k = 5` (`c = 2`) the engine uses `gamma_0`, where `r_1 = 1/sqrt 3` and `z_0,z_1,z_2` form a
**triangle** on that circle: `3 = c + 1 > c = 2`, so the contradiction goes through. At `c = 3` a
single circle cannot work, by Theorem E.

### 5.4 The certified computation for the nine-point configuration

`work/circles_ceiling.py` decides the chromatic number of `{z(m,j)}` for every `gamma`. The 36
unit-distance conditions are real-analytic equations in `gamma`; every zero is located (sign changes
plus tangential minima, bisection to 60 digits), and on each stratum the graph is computed and its
chromatic number certified by exhaustive search.

```
distinct critical gamma values: 12        (they are +-gamma_0 + k pi/3, k = 0..5)
chromatic numbers attained: [1, 2, 3]     max chromatic number: 3
all strata with chi >= 2 have exactly 3 edges, e.g.
  gamma = 0.585685543457 (= gamma_0)  chi = 3  radii = [1.369637, 0.577350, 1.946988]  unit-chord circle m = 1
  gamma = 1.508709558936              chi = 3  radii = [0.577350, 1.369637, 1.946988]  unit-chord circle m = 0
at gamma_0 the 3 edges are exactly the three unit triangles on the circle r = 1/sqrt 3.
```

So **for every shift the nine forced points span a unit-distance graph of chromatic number at most
3**, edges occurring only for `gamma = +-gamma_0 mod pi/3`, and then only the three triangles on the
circle of radius `1/sqrt 3`. Certificate `work/CERT-circles-ceiling.json`, sha256 `53d0c91c...`.

**Remark (the smallest four-chromatic unit-distance graph is incompatible).** The Moser spindle (7
vertices, 11 unit edges) has chromatic number 4 — verified exactly in `work/spindle.py` (exact
coordinates in `Q(sqrt 3, sqrt 11)`, all 11 edges of squared length 1, exhaustive colouring
search). It does sit on three concentric circles — at its shared vertex `a`, with radii
`{0, 1, sqrt 3}` — but the single-shift radii never have that shape: `r_m(gamma) = 0` forces
`gamma in {0, 2pi/3, 4pi/3}`, and for those three values the radii are `{0, sqrt 3, sqrt 3}`. (The
radius computation is exact; the claim that no other centre of the spindle has at most three
distinct radii is numerical, from `work/spindle.py`, not proved.)

### 5.5 The exact remaining question

By §5.3–5.4 a complement-three engine needs **at least two simultaneously good shifts** (Lemma 5.1
shows good tuples are abundant, so that is not the obstruction), i.e. a four-chromatic
unit-distance configuration whose vertices can be placed, one by one, at points
`x + e^{it} + e^{i(t + (2m+1)kappa + gamma_i)}` with `t` in the *given* same-state sets
`Y_{gamma_i}`. Those sets are adversarially placed measurable sets of positive measure, and each
vertex needs only one representation, so the requirement is:

> **(Q)** Find a four-chromatic unit-distance graph `G` with `n >= 7` vertices and shifts
> `gamma_1,...,gamma_s` such that for **every** measurable `sigma` (with the `kappa`-flip) a
> congruent copy of `G` has its vertices in
> `{x + e^{it}(1 + e^{i((2m+1)kappa + gamma_i)}) : t in Y_{gamma_i}, m in Z}`.

For `s = 1` the set is three concentric circles with the radii `r_m(gamma)`, and (Q) is refuted:
Theorem E and §5.4. For `s >= 2`, (Q) is open; it is the exact statement a six-colour version of
Proposition 5.6 must settle. The `k = 5` case is `s = 1` with a *triangle*, which works because
`3 = c+1 > c = 2`; at `c = 3`, `s = 1` provably cannot work.

---

## 6. Summary, and what is not proved

**Proved here.**

* **Theorem A**: for every `k >= 4` two disjoint nonempty label groups with `|A|+|B| = k-2` cannot
  alternate around a centre. New at `k = 6`; it is the paper's Lemma 6.4 with the sizes `(1,2)`
  replaced by the complement size `2`.
* **Corollaries 3.1–3.3 (`k = 6`)**: at a six-colour four-cycle cyclic centre an outsider is in the
  palette a.e.; at a six-colour triangle centre every two-valued system `{A,B}` with `|A|+|B| = 4`
  is impossible while the residual class is the 35 values of Corollary 3.2(b); and the complete
  kill list `|A|+|B| = 4` for every cycle length.
* **Theorem E**: a unit-distance graph on one circle is 3-colourable.
* **Certified computations** (`work/`, two independent decision procedures plus a third
  cross-check): (i) every six-colour cycle stratum is non-bipartite in the palette-disjointness
  graph, with explicit odd cycles, so none is forced into a two-state alternation — while at
  `k = 5, ell = 3` the same program reproduces the paper's chain exactly; (ii) the nine-point
  configuration forced by one state shift has chromatic number at most 3 for every shift.
* **Lemmas 5.1–5.2**: good shifts are abundant for every state function, and the conull-agreement
  shifts form a null subgroup — which is why one fixed shift is good for every `sigma` at `k = 5`.

**Not proved, not claimed.** Local finiteness at `k = 6` is not established here; neither is
`|P_x(e)| <= 2` at `k = 6`, nor anything about `chi(R^2)`. §4.3 lists the palette systems that
survive at `k = 6`; §5.5 states the single geometric property a six-colour engine needs. The
Moser-spindle remark in §5.4 is numerical, not proved.

---

## 7. Files and how to check them

| file | content | command |
|---|---|---|
| `work/verify_formulas.py` | numerical verification of the paper's constants and of the unit triangle | `python3 work/verify_formulas.py` |
| `work/state_enum.py` | palette-state accounting, implementation 1 (frozensets, BFS) | `python3 work/state_enum.py` |
| `work/state_enum2.py` | same decision, implementation 2 (bitmasks, boolean-matrix odd-walk test) | `python3 work/state_enum2.py` |
| `work/crosscheck.py` | agreement check + edge-by-edge verification of every odd-cycle certificate | `python3 work/crosscheck.py` |
| `work/CERT-state-accounting.txt` | certificate text (sha256 `ed3f7724...`) | written by `crosscheck.py` |
| `work/circles_ceiling.py` | chromatic number of the single-shift forced configuration, all shifts | `python3 work/circles_ceiling.py` |
| `work/CERT-circles-ceiling.json` | its certificate (sha256 `53d0c91c...`) | written above |
| `work/spindle.py` | exact verification of the Moser spindle (11 unit edges, `chi = 4`) | `python3 work/spindle.py` |
| `work/states_k5_k6.json`, `work/states_k5_k6_b.json` | full machine output of both implementations | — |
