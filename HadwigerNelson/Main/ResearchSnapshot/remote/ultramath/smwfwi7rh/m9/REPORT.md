# Six colours at a cyclic centre: the unit-triangle count is exactly tight, and the (3, 2) residue is the exact obstruction

**Swarm direction d11 (member m9).** Cycle length `ell = 5` at `k = 6`, the one case of
`ell in {3,4,5,6}` that no other member of this swarm took. Main new results: **the unit-triangle
count `3 x 2 = 6 = k` is exactly tight at six colours** (Theorem 1), which gives a sharp
singleton/ternary dichotomy at every unit triangle, explains the `k`-phase transition
quantitatively, and yields the exact structure of the surviving `(3, 2)` residue (Theorems 3 and 4).
Everything is either proved from the paper's hypotheses or decided by an exact finite computation
whose certificate is in this directory. Section 9 is the status ledger, Section 10 the audit of the
record.

---

## 0. Summary

1. **Theorem 1 (the unit-triangle count; tight at `k = 6`).** For every weak measurable
   `k`-colouring and every unit equilateral triangle with vertices `p, q, r`,
   $$\sum_{i \in \{p,q,r\}} \int_S |P_i(f)|\, d\sigma(f) \;\le\; k .$$
   *(Proof: the three palettes in a common direction are pairwise disjoint a.e.)*
   At `k = 6` the bound is exactly tight, and hence: **if none of the three vertices has a singleton
   palette on a positive-measure set, then all three palettes are pairs a.e.** Equivalently, at a
   unit triangle, ternarity at one vertex forces a positive-measure singleton set at some vertex.
   Calibration: at `k = 5` the same count reads `3 x 2 = 6 > 5 = k`, so a unit triangle can never
   carry three pairs — which is the quantitative content behind the necessity of singletons in the
   five-colour theory; at `k >= 7` there is slack `k - 6`, which is exactly the room the `m3`
   construction uses.
2. **Theorem 3 (the residue).** At a typical centre at `k = 6` the palette map is either pair-valued
   or 2-valued with sizes `(3, 2)`; in the second case its ternary class is `R^2`-invariant, so the
   field is 3-fold symmetric (`P(t + 2pi/3) = P(t)`). This `(3,2)` residue is exactly the case that
   all three alternation/sum tools of the record miss (`m16`'s Theorem A needs `|A|+|B| = 4`,
   `m7`'s Lemma 6.4 needs `<= 3`, and the monochromatic-unit-sum lemma needs a `120`-degree
   crossing pair, which `R^2`-invariance forbids). **Corollary 2: the `(3,2)` residue cannot occupy
   the three vertices of a unit triangle** — decided exactly twice (exhaustive enumeration of all
   `120^3` configurations; and a CNF instance), and immediate from Theorem 1.
3. **Lemma 5 (ternary rigidity).** A ternary palette determines its `R`-successor exactly:
   `P_x(Re) = [6] \ (P_x(e) union {c(x)})`, a pair, and `P_x(R^2 e) subseteq P_x(e)`.
4. **Lemma 6 (unit-step transport; the paper's Remark 5.3).** For `|u| = 1` and a.e. `f` not
   parallel to `u`, `P_{x+u}(f) cap P_x(f) = empty`. It implies the record's two-centre bound
   `|P_x| + |P_y| <= 5` (`m2`) in the stronger pairwise-disjointness form, and **no
   translation-invariant palette field satisfies it** — so every palette-level countermodel of the
   previous sprint (`m13`, `m15`, `FREE-LABEL.md`) satisfies (5.3) only for `|z - z'| <= d_0`, not at
   the unit separations the paper's Lemma 6.7 uses (Section 10).
5. **Lemma 8 (the split).** The exact `k = 6` fate of the paper's five-cycle step ban (Lemma 6.7):
   at a five-cycle centre with diagonal palettes, a state contact at direction `a` forces, at
   `z = x + a`, `P_z(f) cap {i+4, X} != empty` for a.e. `f` in state `i` or `i+1`, with the two
   members of `{i+4, X}` split between `f` and `Rf` — a pair where `k = 5` had the single label `X`.
6. **Decided computation.** The palette calculus at a five-cycle centre at `k = 6` **including the
   unit-step transport** is satisfiable: an explicit 6-sector field on a hexagonal patch of radius 7
   (169 centres, 1014 palette positions, ternary palettes and 441 singleton positions included) is
   exhibited and independently re-verified with zero violations. Hence no local palette argument
   excludes the five-cycle at six colours, and the `(3,2)` residue at the centre itself is
   compatible with the whole one-ring neighbourhood (it is *not* compatible with the residue holding
   at every point, by Corollary 2).

**Not decided here:** whether `(W)` holds at `k = 6`. The `(3,2)` residue is the exact obstruction;
Section 9 lists what a proof must add.

---

## 1. Setting, and exactly what is used

Notation is the paper's (`attachments/here-are-three-files-ni5n/paper.pdf`): `c` a weak measurable
`k`-colouring, `A_i` the colour classes, `H_i` their closed essential supports, `S = S^1` with
angular measure `sigma` (total mass `2pi`; below, `d sigma / 2 pi` is used where a probability is
meant), `kappa = pi/3`, `R` rotation of directions by `kappa`, `P_x` the maximal palette
(Definition 5.1), `D_{x,i} = {e : i in P_x(e)}`, `W_x` the trace family, `Gamma_x` the transition
graph (Definition 6.1), `L = {x : Gamma_x` contains a cycle`}`, and "typical" = a spatial
density-one point of its own colour class (conull, Lemma 4.3).

Quoted from the paper (checked against the extracted text of each displayed formula):

* **(5.2)** (Lemma 5.2(1)): for a.e. independent-angle pair `(e, v)`,
  `c(x + e + v) notin P_x(e) union P_x(v)`.
* **Lemma 5.2(2)**: if `e` is an angular density-one point of `D_{x,i}` then for every `v`
  nonparallel to `e` the spatial density of `A_i` at `x + e + v` is zero.
* **(5.3)** (Lemma 5.2(3)): if `z + f = x + s(f) + t(f)` is a smooth representation with `s, t`
  nonparallel unit vectors and `s` a local diffeomorphism in the angular coordinate, then
  `P_z(f) cap P_x(s(f)) = empty` a.e.
* **Remark 5.3**: for any fixed unit direction `a` the representation `(x + a) + f = x + f + a` is
  admissible off `f = +-a`.
* **(5.7)** (Corollary 5.4): `P_x(f) cap P_x(Rf) = empty` a.e.
* **Lemma 4.3**: two density-one points of the same class are never at distance exactly one.
* **Lemma 6.2 / (6.2)**: `ij in Gamma_x` implies `P_x(e)` is not contained in `{i, j}` a.e., and
  there is a trace `b^{ij} in W_x` with `b^{ij}_i = b^{ij}_j = 0` a.e.
* **Definition 5.1**: palettes are nonempty a.e.; every trace is supported in the palette; `W` is
  closed under varying centres, (5.1).

Further inputs, established in the previous sprint and cited rather than re-derived:

* **(SA)** self-avoidance: `c(x) notin P_x(e)` for a.e. `e` at a typical `x` (`STRUCTURE.md`, L. 1).
* **(P)** `1 <= |P_x(e)| <= 3` at `k = 6` (`m16`'s transfer table).
* **(DENS)** `sigma{T subseteq P_x} <= 1/2` (probability) for every nonempty `T` (`m11`, sharp):
  `T subseteq P_x(e)` and `T subseteq P_x(Re)` are incompatible by (5.7).
* **(SUM)** the monochromatic-unit-sum lemma (`STRUCTURE.md`, Lemma 6): at a typical `x` with
  `c(x) = i` there are no density-one directions `u, v` of exact palette levels `A = P_x(u)`,
  `B = P_x(v)` with `A cap B = empty`, `|A| + |B| = k - 1`, `i notin A union B` and `|u + v| = 1`.

**Geometric identities used** (elementary; re-checked to `1e-15` in `work/s5_trig.py`):
`1 + e^{2 pi i/3} = e^{i pi/3}`; `|1 + e^{2 pi i/3}| = 1`; `|1 + e^{i pi/3}| = sqrt 3`;
`e^{i pi/3} - 1 = e^{2 pi i/3}`; `u + R^2 u = Ru` for `|u| = 1`; the side directions of a unit
equilateral triangle are `{w, Rw, R^2 w}`; and the unit decomposition `s + t = u + f` with all four
vectors of unit length has `{s, t} = {u, f}` uniquely.

---

## 2. Lemma 6 (unit-step transport) and the sharp form of `m2`

> **Lemma 6.** Let `x` be any centre and `u` a unit vector. Then for a.e. unit direction `f` not
> parallel to `u`,
> $$P_{x+u}(f) \cap P_x(f) = \emptyset .$$

*Proof.* Take `z = x + u` and the representation `z + f = x + f + u`, i.e. `s(f) = f`, `t(f) = u`,
in (5.3). The first endpoint map is the identity (a local diffeomorphism in the angular
coordinate); the second is the constant unit vector `u`, which Remark 5.3 permits; `s` and `t` are
nonparallel exactly off `f = +-u`. A countable cover of the circle by arcs avoiding `+-u` gives the
statement. `square`

As an identity this is Remark 5.3's stated consequence of (5.3) — the paper's Lemma 6.7 uses
exactly it ("(5.3) applied to `z + f = x + f + a` gives `P_z(f) cap P_x(f) = empty`"). Consequences:

> **Corollary 7.**
> (i) For a unit triangle `p, q, r` and a.e. direction `f` not parallel to its three sides, the
> palettes `P_p(f), P_q(f), P_r(f)` are pairwise disjoint; hence
> `|P_p(f)| + |P_q(f)| + |P_r(f)| <= k`, and `|P_x(f)| + |P_y(f)| <= k - 1 = 5` for every unit pair.
> The record's bound `m2` is the `k = 6` case, in the weaker "sum" form.
> (ii) No translation-invariant palette field satisfies (5.3) at separation 1: if `P_{x+u} = P_x`
> for all unit `u`, Lemma 6 gives `P(f) = empty`, contradicting nonemptiness.

---

## 3. Theorem 1 (the unit-triangle count is exactly tight at six colours)

> **Theorem 1.** Let `c` be a weak measurable `k`-colouring and `p, q, r` the vertices of a unit
> equilateral triangle (any three centres, pairwise at distance exactly one). Then
> $$\sum_{i \in \{p,q,r\}} \int_S |P_i(f)|\, \frac{d\sigma(f)}{2\pi} \;\le\; k .$$
> Consequently, at `k = 6`: if at each of the three vertices `|P_i| >= 2` a.e., then at each of the
> three `|P_i| = 2` a.e. In particular, if some vertex has a palette of size `3` on a set of positive
> angular measure, then some vertex has a palette of size `1` on a set of positive angular measure.

*Proof.* By Corollary 7(i), for a.e. `f` the three palettes are pairwise disjoint subsets of the
`k` labels, so `|P_p(f)| + |P_q(f)| + |P_r(f)| <= k` a.e.; integrate. The exceptional directions
(the three side directions and their opposites, a null set) do not matter.
At `k = 6`: `|P_i| >= 2` a.e. gives `int |P_i| >= 2`, so `6 = 2+2+2 <= sum int |P_i| <= 6`, and
equality forces `int|P_i| = 2`, i.e. `|P_i| = 2` a.e., at each vertex. `square`

**Provenance.** The *inequality* is an immediate integration of the pairwise-disjointness form of
`m2` (Corollary 7(i)) and is not claimed as new; its content here is the *equality case* at `k = 6`
and the singleton/ternary dichotomy that follows, together with the `k`-calibration below.

**Calibration (`k = 5`, `k >= 7`).** At `k = 5` the same count reads `3 x 2 = 6 > 5 = k`: no unit
triangle can carry three pairs a.e., so *every* unit triangle at five colours has a vertex which is
not a pair a.e. — the quantitative content behind the five-colour scheme's forced singletons. At
`k >= 7` the count leaves slack `k - 6 >= 1`, which is exactly the room used by `m3`'s construction
(four outsider labels against a three-label cycle, with singleton palettes everywhere). So the
`k`-phase transition has a second, independent explanation: `k = 6` is the balance point of the unit
triangle count `3 x 2 = k`.

**Consequence at a cyclic centre.** A typical centre `x` at `k = 6` whose palette is ternary on a
positive-measure set, and the six points `x + R^j u` of a unit hexagon about it, give six unit
triangles `(x, x+R^j u, x+R^{j+1}u)`. Theorem 1 says each of them has a vertex with a
positive-measure singleton set; the vertex cannot be `x` (its ternary set is positive), so at least
three of the six rim points carry a positive-measure singleton set. Inside the `(3,2)` residue those
singletons are forced to be exactly `{c(x)}` (Section 5, after the residue structure).

---

## 4. Lemma 5 (ternary rigidity at six colours)

> **Lemma 5.** Let `x` be typical, `c(x) = i`, and suppose no palette on the `R`-orbit of `e` is a
> singleton. If `|P_x(e)| = 3` then
> (a) `P_x(Re) = [6] \ (P_x(e) union {i})`, a two-element set;
> (b) `P_x(R^2 e) subseteq P_x(e)`.

*Proof.* (a) (5.7) gives `P_x(Re) cap P_x(e) = empty` and (SA) gives `i notin P_x(Re)`, so
`P_x(Re) subseteq [6] \ (P_x(e) union {i})`, a set of `6 - 3 - 1 = 2` elements; nonemptiness plus the
no-singleton hypothesis forces equality.
(b) Apply (5.7) to `Re`, then (SA):
`P_x(R^2e) subseteq [6] \ (P_x(Re) union {i}) = [6] \ (([6] \ (P_x(e) union {i})) union {i}) =
P_x(e)`. `square`

The no-singleton hypothesis holds at a six-cycle centre (`V(C) = [6]`, and `STRUCTURE.md`'s Lemma 3
forbids singletons there) and at a five-cycle centre whose colour is the outsider (`V(C) = Z/5Z`, so
a singleton would be the outsider label, which (SA) forbids). Consistently, all 380 admissible
five-cycle orbit words at `k = 6` have sizes in `{2, 3}` and all satisfy Lemma 5, so there it cuts
nothing further; its content is that ternarity propagates rigidly along the `R`-orbit.

---

## 5. Theorem 3 (the `(3,2)` residue is the exact obstruction) and Corollary 2

> **Theorem 3.** Let `x` be a typical centre of a weak measurable 6-colouring.
> (a) Either `|P_x| <= 2` a.e., or there is a positive-measure set on which `|P_x| = 3`; then Lemma 5
> applies there and on its `R^2`-image.
> (b) If the palette map is 2-valued with values `A` (three labels) and `B` (two),
> `A cap B = empty`, `A union B = [6] \ {c(x)}`, then the `A`-class `U` satisfies `R^2 U = U`; hence
> `P(t + 2pi/3) = P(t)` (3-fold symmetry), `sigma(U) <= pi` (as a measure), with equality iff
> `R U = [6]\U`.
> (c) None of the three exclusions of the record applies in case (b): `m16`'s Theorem A needs
> `|A|+|B| = k-2 = 4`; `m7`'s Lemma 6.4 needs `|A|+|B| <= k-3 = 3`; and (SUM) needs two disjoint
> palettes at directions `u, v` with `|u+v| = 1`, i.e. `120` degrees apart — but by (b) those
> directions lie in the same class, where the palette has one and the same value. (DENS) gives
> `sigma(U) <= pi` and the models of §8.2 attain it; Corollary 7(i) is satisfied, the two values
> being disjoint.

*Proof.* (a) is (P). (b) Let `u` be a density direction of `U`. If `P_x(R^2u) = B` then
`|u + R^2 u| = 1` and (SUM) applies to the disjoint pair `(A, B)` with `|A| + |B| = 5 = k-1` and
`c(x) notin A union B`, at density points — which exist because `sigma(R^2U cap ([6]\U)) > 0` would
produce one. So `R^2U subseteq U` modulo null, and since `R^2` has order three, `R^2U = U`. (DENS)
with `T = A` gives `sigma(U) <= pi`, and `RU subseteq [6]\U` by (5.7), with equality of measures iff
`sigma(U) = pi`. (c) is a check of the three hypotheses using (b). `square`

> **Corollary 2.** The `(3,2)` residue cannot hold at the three vertices of a unit equilateral
> triangle.

*First proof (from Theorem 1).* At each of the three vertices the residue has a positive-measure
ternary set and no singleton value, so Theorem 1 forces all three palettes to be pairs a.e. —
contradiction.
*Second proof (exhaustive, exact).* `work/s7_triangle.py` enumerates all `120` residue fields per
vertex, i.e. all `120^3 = 1 728 000` configurations of the unit triangle, and checks every
constraint of the calculus exactly: `0` solutions. For non-vacuity the same script finds `120`
single-node fields and `1080` two-node (unit pair) configurations.
*Third proof (CNF, independent code path).* `work/s6_residue_patch.py 1 all` — the residue demanded
at all seven centres of the unit wheel — is UNSAT (CaDiCaL), whereas the same instance with the
residue only at the centre is SAT and with no residue condition is SAT.

The residue is therefore *local but not spreadable*: it may sit at an isolated centre, but not at
three mutually adjacent ones.

**The exact catalogue** (`work/s1_residue.py`; centre colour in the cycle / the outsider):
`ell = 3`: 9 / 7; `ell = 4`: 8 / 6; `ell = 5`: 7 / 5; `ell = 6`: 6 (no outsider). Every one is
3-fold symmetric along the `R`-orbit, as Theorem 3(b) requires. For `ell = 5` with the outsider
colour there are exactly five, one per diagonal of `C_5`:

```
(A, B) = ({0,1,3},{2,4}), ({0,2,3},{1,4}), ({0,2,4},{1,3}), ({1,2,4},{0,3}), ({1,3,4},{0,2})
```

Beyond the catalogue, inside the residue the singleton forced by Theorem 1 at a rim point of a
ternary centre is exactly `{c(x)}`: at the pair `(x, y)` the four *constrained* directions carry
both values of `x`, whose union is `[6]\{c(x)}`, so a singleton at `y` in a constrained direction
must be `{c(x)}`. (In the two unconstrained directions no such conclusion is available.)

---

## 6. Lemma 4 (the twist)

> **Lemma 4.** Suppose that at every point of a plane set the palette map is 2-valued with sizes
> `(3, 2)`. Then for every unit vector `w` in the ternary class `U_y` of a point `y`:
> (a) `P_{y+w}(f) subseteq [6] \ P_y(f)` for a.e. `f in U_y` not parallel to `w`;
> (b) `sigma(U_{y+w} cap U_y) = 0`; if `sigma(U_y) = pi` (equivalently `R U_y = [6]\U_y`) then
> `U_{y+w} = R U_y`.

*Proof.* (a) is Lemma 6 at the unit pair `(y, y+w)`. (b) The points `y`, `y+w`, `y+Rw` form a unit
triangle with side directions `w, Rw, R^2w`; for a.e. `f in U_y` outside those directions the three
palettes are pairwise disjoint (Corollary 7(i)), so `|P_{y+w}(f)| + |P_{y+Rw}(f)| <= 6 - 3 = 3` and
`|P_{y+w}(f)| <= 2`. So the ternary class of `y+w` meets `U_y` in a null set; if `sigma(U_y) = pi`
then `[6]\U_y = R U_y` and equality of measures forces `U_{y+w} = R U_y`. `square`

Note that (b)'s first part does **not** need the residue at `y+w`, only at `y`. The twist is
compatible with the geometry around every unit triangle (side directions `120` degrees apart, hence
`R^2`-related, and `R^2` preserves every class by Theorem 3(b)), which is why the residue is not
killed by pairwise constraints; Corollary 2 is what does kill its *spread*.

---

## 7. Lemma 8 (the leftover-pair split: the exact `k = 6` fate of Lemma 6.7)

At a five-cycle centre at `k = 5` the paper's §6.3.3 shows every palette is a diagonal
`D_j = {j, j+2}` of `C_5`, writes `w_x(e) = j`, and proves `w_x(Re) = w_x(e) +- 1`. Lemma 6.7 then
shows that a *state contact* (a direction `a` in the closed essential supports of two adjacent states
`i, i+1`) bans both steps from the shared state, because the trace argument puts the *single*
remaining label into both `P_z(f)` and `P_z(Rf)` at `z = x + a`. At `k = 6`,
`[6] = Z/5Z union {X}` and the same computation produces a pair.

> **Lemma 8.** Let `x` be typical with `c(x) = X` (the outsider of the five-cycle `C_5` on `Z/5Z`),
> suppose `Gamma_x` contains `C_5`, and let `a` lie in the closed essential supports of the states
> `i` and `i+1`, where state `j` means `P_x = D_j = {j, j+2}`. Put `z = x + a`. Then for a.e. `f`
> with `w_x(f) in {i, i+1}` and `f` not parallel to `a`,
> $$P_z(f) \cap \{i+4, X\} \neq \emptyset ,$$
> and if `w_x(f) = i` and `w_x(Rf) = i+1` (a step), then `P_z(f)` and `P_z(Rf)` meet `{i+4, X}` in
> *different* members.

*Proof.* As in Lemma 6.7, the two cycle edges at `i` and at `i+1` together with the contact
hypothesis give traces `b, b' in W_z` with `P_z(f) \ subsetneq D_i` and `P_z(f) \ subsetneq D_{i+1}`
a.e. (the centres `x + f` for `f` in state `i` tend to `z`, and (5.1) closes `W` under varying
centres). Lemma 6 at the unit pair `(x, z)` gives `P_z(f) cap D_i = empty` whenever `w_x(f) = i`;
since `[6] \ D_i = D_{i+1} union {i+4, X}` and `P_z(f)` is not inside `D_{i+1}`, it meets
`{i+4, X}`. Symmetry in `i, i+1` covers the other case; and (5.7) at `z` gives the split. `square`

So the `k = 5` "global step ban" is exactly the statement that the leftover has one element, which
holds iff `k = 5`. At `k = 6` it is a pair, and a split is consistent (§8.3 exhibits fields
satisfying all of it).

---

## 8. Decided finite computations (certificates in `work/`)

### 8.1 Single-centre orbit words: independent re-derivation

`work/s4_orbit_indep.py` (vectorised brute force over all `|A|^6` tuples — no recursion, no transfer
matrix) reproduces the seven counts of `sprint/k6/STRUCTURE.md` **exactly**:

| `ell` | centre colour | admissible palettes | orbit words |
|---|---|---|---|
| 3 | in the cycle | 22 | 70194 |
| 3 | outsider | 19 | 11888 |
| 4 | in the cycle | 20 | 18746 |
| 4 | outsider | 17 | 2164 |
| 5 | in the cycle | 18 | 3720 |
| 5 | outsider | 15 | 380 |
| 6 | in the cycle | 16 | 510 |

### 8.2 The `(3,2)` residue catalogue

`work/s1_residue.py`, counts as in Section 5, all 3-fold symmetric.

### 8.3 The palette calculus **with** the unit-step transport: satisfiable to radius 7

`work/s3_patch.py` builds, for the hexagonal lattice ball of radius `R` (unit-distance graph = the
triangular lattice; palette indices = the six absolute lattice directions), the CNF for: sizes
`1..3` at every centre; at the centre `x = (0,0)` in addition `i = 5 notin P`, `P` not inside an edge
of `C_5`, no singleton, Lemma 5; (5.7), (MON), (C1) at every centre; **Lemma 6 at every unit pair
and every non-parallel direction**; and a colour at every centre with self-avoidance, distinct
colours on unit pairs, and the constant-sequence trace `c(y) in P_x(dir y)` for the six neighbours
of `x`.

CaDiCaL returns **SAT** for `R = 1, ..., 7` (169 centres, 1014 palette positions at `R = 7`; the
model has 267 ternary positions and 441 singleton positions, and its centre palettes are
`{2,4},{0,1,3},{2,4},{1,3},{2,4},{0,1,3}`). Every model is decoded and re-checked by the
independent checker `work/verify_patch.py`, which reports **0 violations** on the full ball and on
every sub-ball. Models: `work/cert/patch_R*.model`.

Two related decisions of the same instance family, at `R = 1` (`work/s6_residue_patch.py`):

| extra condition | result |
|---|---|
| none | SAT |
| the `(3,2)` residue at the centre `x` only | SAT |
| the `(3,2)` residue at all 7 centres | **UNSAT** (Corollary 2) |

**Consequence.** The five-cycle case at `k = 6` is not excluded by the palette calculus, even with
the unit-step transport added. Since the `k = 5` proof of §6.3.3-6.3.4 is precisely "diagonal
structure plus step ban", and Lemma 8 shows that at `k = 6` the step ban is the leftover-pair split,
the printed three-step scheme has no six-colour analogue for `ell = 5`: the obstruction is the split,
not any pairwise palette constraint. What *is* excluded is the spread of the residue across a unit
triangle (Corollary 2).

---

## 9. Status ledger

| statement | status |
|---|---|
| `sum_i int_S |P_i| dsigma/2pi <= k` at a unit triangle (any `k`) | **proved** (Theorem 1) |
| at `k = 6`, a unit triangle without positive-measure singletons has three pairs a.e. | **proved** (Theorem 1) |
| at `k = 5`, no unit triangle carries three pairs a.e. (count `6 > 5`) | **proved** (Theorem 1, calibration) |
| ternary palette determines its `R`-successor and forces `P(R^2 e) subseteq P(e)` | **proved** (Lemma 5) |
| `P_{x+u}(f) cap P_x(f) = empty` at unit separation (sharp `m2`) | **proved** (Lemma 6; the paper's Remark 5.3) |
| the `(3,2)` residue is forced 3-fold symmetric | **proved** (Theorem 3(b)) |
| the `(3,2)` residue misses `m16`-A, `m7`-6.4 and (SUM) | **proved** (Theorem 3(c)) |
| the `(3,2)` residue is impossible at the vertices of a unit triangle | **proved** (Corollary 2, three ways) |
| inside the residue, the forced rim singleton is `{c(x)}` | **proved** (Section 5) |
| the residue locus has no unit triangle, so it cannot be conull in any open set | **corollary** |
| the five-cycle step ban at `k = 6` is the leftover-pair split | **proved** (Lemma 8) |
| palette calculus + Lemma 6 satisfiable at a five-cycle centre, radius `<= 7` | **decided** (§8.3) |
| the seven orbit-word counts | **decided twice** (§8.1) |
| `(W)`: `L cap B(y,R)` finite for some `R > 1` | **open** |
| the `(3,2)` residue realisable by a proper 6-colouring | **open** |

**What a proof of `(W)` at `k = 6` must now add.** By Theorem 3 every cyclic centre is either
pair-valued or a residue point. By Corollary 2 the residue points form a set containing no unit
triangle, and by Lemma 4 the residue cannot survive a unit step in a ternary direction. So the
remaining possibilities are:

* exclude the pair-valued case at a five-cycle centre by proving that the leftover-pair split of
  Lemma 8 cannot occur at two opposite contacts `a`, `-a` — the only step of §6.3.3-6.3.4 that fails;
* prove that the residue locus (a set with no unit triangle, and with the twist of Lemma 4) cannot
  be locally finite — i.e. that `L` accumulates there;
* or prove that the residue cannot be the maximal palette field of a proper 6-colouring, which is
  the trace-consistency frontier.

---

## 10. Audit of the record

1. **`m2` is a corollary of Lemma 6, and the pairwise form is stronger.** `STRUCTURE.md` derives
   `|P_x| + |P_y| <= 5` from the unit triangle; the triangle argument gives pairwise disjointness of
   the three palettes, which is what Theorem 1, Theorem 3 and Lemma 4 use. Integrating it gives the
   new tightness statement at `k = 6`.
2. **The record's palette-level no-go is stated for a strictly smaller constraint set than it
   appears to be.** `sprint/k6/FREE-LABEL.md`'s conclusion is correct for the constraints it
   verifies, which include (5.3) only for `|z - z'| <= d_0`. But the paper's five-cycle step ban uses
   (5.3) at separation **1** (Lemma 6.7), and by Corollary 7(ii) *no* translation-invariant field —
   so none of the four countermodels (`m13`, `m15`, `FREE-LABEL`) — satisfies that. The honest
   statement is: the small-distance transport is satisfiable; whether the full transport is
   satisfiable was open, and §8.3 answers it affirmatively on patches up to radius 7 with an explicit
   certificate. The countermodels should be cited as small-distance models.
3. **The `(3,2)` gap between the two alternation theorems is real.** `m16`'s Theorem A excludes
   disjoint groups with `|A|+|B| = 4`; `m7`'s lemma excludes `<= 3`. Disjoint nonempty groups at
   `k = 6` always have `|A|+|B| <= 5`, so sizes `(3,2)` — complement `{c(x)}` — are covered by
   neither. Theorem 3 shows this is exactly the residue on which (DENS) is attained with equality
   and which (SUM) cannot see; Corollary 2 shows where it does break.
4. **`m16`'s Corollary 3.1 gap** is correctly withdrawn in `REPORT.md` §4c; nothing here uses it.
5. **One bug found and fixed in my own work**, recorded for honesty: an earlier version of
   `work/s3_patch.py` encoded (6.2) as "the palette contains at most one endpoint of each cycle edge"
   instead of "the palette is not contained in an edge", which silently removed all ternary palettes
   at the centre. All numbers quoted here are from the corrected encoders, and every model is
   re-checked by `work/verify_patch.py`, which tests the correct (6.2).

---

## 11. Files and the exact commands

| file | content |
|---|---|
| `REPORT.md` | this document |
| `work/s1_residue.py` | `(3,2)` residue catalogue per cycle length and centre colour |
| `work/s2_ring.py` | CNF for the unit wheel `W_6` (7 centres) |
| `work/s3_patch.py` | CNF for the hexagonal patch of radius `R`, with Lemma 6 |
| `work/s6_residue_patch.py` | same, with the `(3,2)` residue demanded at the centre / at all nodes |
| `work/s7_triangle.py` | exhaustive decision of the residue on 1, 2 and 3 unit-separated vertices |
| `work/verify_patch.py` | independent checker of a patch model against every constraint |
| `work/analyse_patch.py` | summary of a patch model |
| `work/s4_orbit_indep.py` | independent (vectorised brute-force) orbit-word counts |
| `work/s5_trig.py` | re-check of the elementary geometric identities |
| `work/cert/patch_R*.model` | CaDiCaL models for `R = 1,...,7`, all verified with 0 violations |
| `work/ref_orbit.py` | copy of `sprint/k6/orbit_correct.py`, for the calibration only |

Commands (from this directory):

```bash
python3 work/s7_triangle.py          # 120 / 1080 / 0  (single node / unit pair / unit triangle)
python3 work/s1_residue.py           # residue catalogue, exact counts
python3 work/s4_orbit_indep.py       # all seven orbit counts (~12 min)
cd work && python3 s3_patch.py 7 > p.cnf \
  && /opt/lean/bin/cadical p.cnf > cert/patch_R7.model \
  && python3 verify_patch.py 7 cert/patch_R7.model      # SAT, "0 violation(s)"
cd work && python3 s6_residue_patch.py 1 all > r.cnf && /opt/lean/bin/cadical -q r.cnf   # UNSAT (rc 20)
```
