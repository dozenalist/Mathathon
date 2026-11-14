# The k = 6 ternary separation engine

Swarm `smwfwi7rh`, member m1, direction d18.

**What this note contains.** (i) The exact `k = 6` replacement of the paper's
Proposition 5.6 by a separation hypothesis about *3-hitting* centres
(Theorem 2) — the precise analogue of the way the paper derives `|P| ≤ 2` at
`k = 5` from Lemma 5.5. (ii) A proof that separation is free whenever the
centre's palette meets one fixed pair of the triple almost everywhere
(Theorem 3), so that the residue is an explicit "spread" class. (iii) A
sharpness proposition: no separation statement of this kind follows from the
palette data of the record, and the countermodel is excluded only by the
transport `(T)` of the paper's Remark 5.3. (iv) An exact accounting (§5) of what
even `|P| <= 2` would still not give at `k = 6`: three independent defects, with
certified enumerations. Nothing here decides (W), and no claim is made about
local finiteness of the full locus.

---

## 1. Setting, and the paper inputs used

`c` is a weak measurable 6-colouring (Definition 1.2), labels
`I = {0,1,2,3,4,5}`, `S = S1` carries the angular probability `sigma`, `R` is
the rotation by `kappa = pi/3`, `Gamma_x` is the transition graph
(Definition 6.1), and `P_x : S -> 2^I` is the maximal palette at the centre `x`
(Definition 5.1), defined up to an angular null set that may depend on `x`, with
`P_x(f)` nonempty for a.e. `f`.

Four paper facts are used, with their hypotheses:

* **(5.2)** [Lemma 5.2(1)] for a.e. `(e,v)` in `S x S`,
  `c(x+e+v) not in P_x(e) union P_x(v)`.
* **(5.3)** [Lemma 5.2(3)] if `z + f = x + s(f) + t(f)` on an angular arc, with
  `s,t` unit and nonparallel and `s` a local angular diffeomorphism, then
  `P_z(f) cap P_x(s(f)) = empty` a.e. on the arc.
* **(5.7)** [Corollary 5.4] `P_x(f) cap P_x(Rf) = empty` for a.e. `f`.
* **(6.2)** [Lemma 6.2] `ij in Gamma_x` implies `P_x(e)` is not contained in
  `{i,j}`, for a.e. `e`.

Their proofs (Lemma 4.3; Lemma 5.2(2); the instantiation
`x + f = x + Rf + R^{-1}f`; Definition 6.1 with the Fourier decay (6.3)) never
use the number of labels beyond `I` being finite. They are available verbatim at
`k = 6`.

**Lemma 0 (Lemma 5.5 is k-general).** *There is an absolute `delta_* > 0` with:
for every `k >= 3`, every weak measurable k-colouring, every pair of labels, and
every two distinct centres binary for that pair, the centres are at distance
`>= delta_*`.*

"Binary for `{i+,i-}`" means `P_x(e) cap {i+,i-}` nonempty a.e. (paper, §5.3).
*Audit of the printed proof* (pp. 29-33): it uses only (i) binarity for one fixed
pair, which makes the intersection a singleton a.e. and gives the sign selection
`s_x` with `s_x(t+kappa) = -s_x(t)`, i.e. (5.8) from (5.7); (ii) the exact
two-circle representation `y + e^{it} = x + e^{i alpha+(t)} + e^{i alpha-(t)}`
and (5.3) applied twice, giving `s_x(alpha+(t)) = s_x(alpha-(t)) = -s_y(t)`;
(iii) the six maps `F_j`, the uniform expansions (5.9)-(5.10), and the
bounded-distortion argument forcing `A = {s_x = 1}` (angular measure `pi` per
period) to be conull on a full period. No other label, no palette-size bound,
nothing about `|I| = 5`. Hence the lemma holds for every `k`. QED

---

## 2. The extraction lemma and the reduction

**Definition 1.** For `T` a subset of `I`, a centre `x` is **T-hitting** if
`sigma{f : P_x(f) cap T nonempty} = 1`. "Binary for `{u,v}`" is the case
`T = {u,v}`.

**Theorem 1 (extraction, `k = 6`).** *Let `A` be a subset of `I` with
`|A| = 3`, put `T = I minus A`, and let `x` be a centre with
`sigma{e : A contained in P_x(e)} > 0`. Then every point of
`{x + e : A contained in P_x(e)}` is a T-hitting centre; that set is a subset of
the circle `x + S` of positive angular measure, so for every `delta > 0` there
are two distinct T-hitting centres at distance `< delta`.*

*Proof.* Put `B = {e : A contained in P_x(e)}`, `sigma(B) > 0`.

*(1) The circle samplings avoid `A`.* By (5.2) and Fubini, for a.e. `e` in `B`
we have `c(x+e+v)` outside `A` for a.e. `v`: for a.e. `(e,v)` the point
`c(x+e+v)` avoids `P_x(e) union P_x(v)`, which contains `A`.

*(2) The slices are typical.* The map `(e,v) -> x+e+v` has Jacobian
`|sin(arg v - arg e)|`, nonsingular off the product-null set `{e = ±v}`; the
atypical points of the plane form a null set, so its inverse image is
product-null, and by Fubini, for a.e. `e` in `B`, the exact radius-one sampling
`v -> x+e+v` at the centre `x+e` is typical for a.e. `v`. (This is the paragraph
"For almost every such `e`, this exact radius-one circle sampling is also
typical" in the proof of Proposition 5.6.)

*(3) The constant-sequence trace.* Definition 5.1 permits `(y_n,r_n) = (x+e,1)`,
so `b(v) = (1_{A_i}(x+e+v))_{i in I}` belongs to `W_{x+e}`. By (1) its support
lies in `T`, and the sum of its coordinates is `1` a.e., so `b` is nonzero; every
individual trace has its positive coordinates inside the maximal palette a.e.,
hence `P_{x+e}(v) cap T` is nonempty for a.e. `v`. So `x+e` is T-hitting.

*(4) Positive measure on a compact circle.* `B` has positive angular measure, so
`{x+e : e in B}` has positive angular measure in the compact metric circle `x+S`,
is infinite, and no `delta`-separated subset of a compact metric space is
infinite. QED

**Theorem 2 (the reduction).** *Suppose that for every 3-element `T` contained in
`I` there is `delta_T > 0` such that any two distinct T-hitting centres are at
distance `>= delta_T`. Then `|P_x(f)| <= 2` for every centre `x` and a.e. `f`.*

*Proof.* If `sigma{f : |P_x(f)| >= 3} > 0` then, `I` being finite, some fixed
3-element `A` contained in `I` satisfies `A` contained in `P_x(f)` on a set of
positive angular measure. Theorem 1 with `T = I minus A` produces distinct
T-hitting centres at distance `< delta_T`. QED

**Why this is the right statement.** At `k = 5` the identical scheme is the
paper's own proof of Proposition 5.6: there `|A| = k-2 = 3` leaves a **pair**
`T`, and Lemma 5.5 supplies the separation. At `k = 6`, `|A| = 3` leaves a
**triple**, and no separation lemma for triples is known. Theorem 2 says that
such a lemma is *exactly* what stands between the paper's method and the bound
`1 <= |P| <= 2` at six colours — neither more nor less.

---

## 3. Where the separation is free

For a T-hitting centre `x` with `|T| = 3`, let
`H(x) = {{u,v} subset T : P_x(f) cap {u,v} nonempty for a.e. f}` be the set of
pairs hit almost everywhere. Call `x` **T-spread** if `H(x)` is empty, i.e. if
for each pair the third label `w` satisfies
`sigma{f : P_x(f) cap T = {w}} = 1`.

**Theorem 3.** *Let `|T| = 3` and let `x, y` be T-hitting with
`|x - y| < delta_*`. Then `H(x) cap H(y)` is empty. In particular
`|H(x)| + |H(y)| <= 3`; and a T-hitting centre whose `H(x)` has three elements
forces every T-hitting centre within `delta_*` to be T-spread.*

*Proof.* If `{u,v}` lies in `H(x) cap H(y)` then both centres are binary for
`{u,v}` and Lemma 0 gives `|x - y| >= delta_*`. QED

**Corollary 3.1.** *For each pair `{u,v}` inside `T`, the set of T-hitting
centres with `{u,v}` in `H(x)` is uniformly `delta_*`-separated, hence locally
finite. Therefore the T-hitting locus is locally finite off its T-spread part.*

The T-spread part is exactly the class in which the `k = 5` style argument has no
purchase: a T-spread T-hitting centre has all three outsider labels occurring as
the whole palette-intersection on positive-measure sets, so no fixed pair is
available and the sign selection of Lemma 5.5 does not exist.

**Corollary 4 (conditional local finiteness of the triangle locus at `k = 6`).**
*Grant `|P_x(f)| <= 2` for every centre and a.e. `f` — which holds if the
separation hypothesis of Theorem 2 does. (At `k = 5` it holds unconditionally, by
Proposition 5.6.) Let `{0,1,2}` be a triangle and `T = {3,4,5}`.*

*(a)* Every palette of size `<= 2` at such a centre meets `T` a.e.: a palette
contained in `{0,1,2}` of size `<= 2` lies inside a triangle edge and is excluded
by (6.2). (Exact: all 15 admissible palettes of size `<= 2` meet `T`; see §7.)

*(b)* For each of the three pairs `{u,v}` inside `T`, the triangle centres binary
for `{u,v}` are `delta_*`-separated, by Lemma 0.

*(c)* Hence the triangle locus at `k = 6` is locally finite off the T-spread
triangle centres.

This is a genuine conditional local-finiteness statement at six colours: it
covers every triangle centre whose palette meets one fixed pair of outsiders
almost everywhere. It is honestly conditional, `|P| <= 2` at `k = 6` being open,
and §5 shows that even granting it the four- and five-cycle cases need more.

---

## 4. Sharpness: separation is not a palette-level statement

**Proposition 5.** *There is a palette field on `S` at `k = 6` with: singleton
values (hence `1 <= |P| <= 3`); `P(f) cap P(Rf)` empty for every `f` [(5.7)]; no
value contained in an edge of the triangle `{3,4,5}` [(6.2)]; independent of the
centre; and T-hitting and T-spread for `T = {0,1,2}` at every centre. Hence no
two distinct centres can be separated by palette data alone.*

*Construction and proof.* Six sectors of `60` degrees, sector word
`W = (0,1,2,0,1,2)`, `P(f) = {W(sector of f)}`. Cyclically neighbouring entries
differ, which is exactly (5.7) on one `R`-orbit; a singleton is never contained
in a triangle edge; the three labels `0,1,2` all occur, so every centre is
T-hitting and T-spread. Exact check in §7. QED

**Remark 5.1 (the model is not any colouring's palette field).** The paper's
Remark 5.3 records that the representation `(x+a) + f = x + f + a` is admissible
in Lemma 5.2(3) for every unit vector `a`, off `f = ±a` (`s(f) = f` is a local
angular diffeomorphism; `t(f) = a` is constant and nonparallel to `s(f)`). Hence
the palette field of any weak measurable colouring satisfies

> **(T)** `P_{x+a}(f) cap P_x(f)` is empty for every unit vector `a` and a.e. `f`.

The field of Proposition 5 does not depend on the centre, so its `(T)`-instance
reads: `P(f) cap P(f)` is empty. It therefore violates `(T)` at every direction
and is not the palette field of any weak measurable 6-colouring. The same applies
to every space-translation-invariant palette model in the record — the singleton
model of m13, the four uniform block fields of m15, and the free-label words of
`sprint/k6/FREE-LABEL.md`. So the earlier conclusion "the palette-level route is
dead at `k = 6`" was established for a strictly *weaker* system than a
colouring's palette field: `(T)` is a colouring-level constraint at a single pair
of centres at distance one, not the global properness of a label function.

---

## 5. What `|P| <= 2` would still not give at `k = 6`

Assume `|P_x(f)| <= 2` for every centre and a.e. `f`. The paper's §6.3 analyses
were built for `k = 5`, where `|P| <= 2` (Proposition 5.6) and where there is a
*single* label outside the cycle. At `k = 6` there are `k - ell` outsiders, and
the exact enumerations of §7 exhibit three independent defects.

**(i) Four-cycle `{0,1,2,3}`, outsiders `X = 4`, `Y = 5`.** Admissible palettes of
size `<= 2`: **13**. The paper's canonical state (`X` if `X` is in `P`, else
`U = {0,2}`, else `V = {1,3}`) is **undefined** for the five palettes `{5}`,
`{0,5}`, `{1,5}`, `{2,5}`, `{3,5}`, so §6.3.1's "This is exhaustive almost
everywhere" fails at `k = 6` even with `|P| <= 2`. Moreover the repair by
declaring a `Y`-state does not restore Lemma 6.6's key step, and this is not a
matter of taste: that step needs two distinct represented groups whose union has
size `>= 3`, so that `|P| <= 2` is contradicted, and at `k = 6` no assignment of
groups to the 13 palettes satisfies that requirement.

**Theorem 5.1 (certified).** *At a `k = 6` four-cycle centre with `|P| <= 2`, an
assignment `P -> G(P)` with `empty != G(P) subset P` for every admissible
palette `P`, such that any two distinct assigned groups have union of size
`>= 3`, exists **iff** the two outsider singletons `{4}` and `{5}` do not both
occur as palette values.* *The minimal obstruction is exactly the two-element
family* `{{4},{5}}`: each singleton palette forces its own one-element group,
and those two groups have union of size `2`, while every sub-family avoiding
both singletons is satisfiable.*

*Proof.* If both `{4}` and `{5}` occur, the palettes `{4}` and `{5}` admit only
the groups `{4}` and `{5}` respectively, and `|{4} union {5}| = 2 < 3`. For the
converse, satisfiability is inherited by sub-families, so it suffices to test the
maximal sub-families avoiding the pair: `cert3.py` finds, by two independent
searches, an assignment for the 11 palettes other than `{4}`, `{5}` (e.g.
`{0,2},{0,4},{0,5} -> {0}`; `{1,3} -> {1,3}`; `{1,4} -> {1,4}`; `{1,5} -> {1,5}`;
`{2,4} -> {2,4}`; `{2,5} -> {2,5}`; `{3,4} -> {3,4}`; `{3,5} -> {3,5}`;
`{4,5} -> {4,5}`), and likewise for the twelve palettes omitting just one of the
two singletons, while the full family of 13 has none. QED

Hence the exact extra input for the four-cycle continuity step at `k = 6` is a
treatment of the *outsider singleton* palettes: either a proof that at most one
outsider occurs as a singleton palette value at a four-cycle centre, or a
modified continuity argument on the directions where one does.

**(ii) Five-cycle `{0,1,2,3,4}`, outsider `5`.** Admissible palettes of size
`<= 2`: **11** — the five diagonals `{i,i+2}` and the six outsider palettes
`{5}`, `{0,5}`, `{1,5}`, `{2,5}`, `{3,5}`, `{4,5}`. So §6.3.3's reduction
"almost every palette is exactly one of its diagonals" fails at `k = 6` — again
because of the outsider, not because of a ternary palette.

**(iii) Triangle `{0,1,2}`, outsider triple `T = {3,4,5}`.** Admissible palettes
of size `<= 2`: **15**, and all fifteen meet `T`. The paper's conclusion that the
palette meets `{3,4,5}` survives, but a triple supports no binary selection:
Corollary 4 covers the centres meeting a fixed pair of outsiders, and the spread
residue is open.

**Conclusion.** Ternary separation is *necessary* for `|P| <= 2` at `k = 6` and
would replace Proposition 5.6 exactly; it is *not sufficient* to transfer §6.3,
because at `k = 6` the outsider count and Lemma 6.3's label count add two further
defects that `k = 5` never had. The four-cycle input at `k = 6` therefore splits
into three explicit statements: (TS) of §2, the outsider-singleton treatment of
(i), and a Lemma 6.3 analogue whose two represented groups leave a complement of
size `2` rather than `1` — the last being the defect identified by m7.

---

## 6. Vacuity tests

1. **The mechanism is the paper's own.** With `|A| = k-2` and `|T| = 2` the scheme
   of §2 is literally the proof of Proposition 5.6 at `k = 5`. Theorem 2 is the
   honest `k = 6` instance, and it names the missing separation statement instead
   of assuming it.
2. **(TS) is not implied by palette data** (Proposition 5) and **not implied by
   binarity** (Theorem 3): a T-hitting centre with `H(x)` empty is exactly the
   uncovered case.
3. **Theorem 1 is not vacuous:** a palette containing a fixed triple on a set of
   positive angular measure produces an *uncountable* set of 3-hitting centres on
   a compact circle, which is why (TS) would be strong.
4. **Corollary 4 is conditional** and is labelled so: `|P| <= 2` at `k = 6` is
   open, and §5 lists what it would still not give.
5. **No claim about (W).** The note does not address local finiteness of `L`.

---

## 7. Files, reproduction, and source checks

| file | content |
|---|---|
| `.ultramath/smwfwi7rh/m1/note.md` | this note |
| `.ultramath/smwfwi7rh/m1/cert.py` | implementation A: palette states at `k = 6` for the four-cycle, five-cycle, triangle, and the Proposition 5 model |
| `.ultramath/smwfwi7rh/m1/cert2.py` | implementation B: bitmask recomputation of the same enumerations, sharing no code with A |
| `.ultramath/smwfwi7rh/m1/cert3.py` | Theorem 5.1: two independent searches for the group assignment and the minimal obstruction |

Commands:

```
cd .ultramath/smwfwi7rh/m1
python3 cert.py
python3 cert2.py
python3 cert3.py
```

`cert.py` and `cert2.py` both print `13` admissible palettes for the four-cycle,
with the five outside the `X/U/V` trichotomy (`{5}`, `{0,5}`, `{1,5}`, `{2,5}`,
`{3,5}`) and the ambiguous palette `{4,5}`; `11` for the five-cycle (5 diagonals,
6 outsider palettes); `15 / 15` for the triangle; and, for the Proposition 5
field, `(5.7) True, sizes [1], T-hitting True, T-spread True,
admissible(triangle) True`. `cert3.py` prints `PATH A assignment exists: None`,
`PATH B assignment exists: None`, `minimal obstruction family: [(4,), (5,)]`,
and `satisfiable: True / True` for each of the three maximal sub-families
omitting the obstruction pair.

**Source checks.** (5.2), (5.3) and Remark 5.3 on pp. 27-29; (5.7) on p. 29;
Lemma 5.5 on pp. 29-33; Proposition 5.6 on pp. 33-34; Definition 6.1 and
Lemma 6.2 on p. 35. Text extracted twice, once with `pdftotext -layout` and once
with `pdftotext -raw` (pp. 27 and 28-29); both extractions give the two
formulas this note rests on, `Pz(f) ∩ Px(s(f)) = ∅` (5.3) and
`(x + a) + f = x + f + a` (Remark 5.3). Page 29 was additionally rendered with
`pdftoppm -r 150 -png` (file `work/png/p-29.png`); this agent cannot inspect
images, so the render is recorded for a human check but is **not** part of the
verification claim above: the verification of the two formulas rests on the two
independent text extractions.
