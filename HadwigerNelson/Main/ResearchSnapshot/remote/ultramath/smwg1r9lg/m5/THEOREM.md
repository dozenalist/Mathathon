# The countable/uncountable barrier in the palette axioms

**What a palette-level proof of (W) at six colours can and cannot see.**

m5, swarm `smwg1r9lg`, direction d3. Files: `THEOREM.md` (this document), `QUOTES.md`
(the exact quotations and the two-extractor check), `verify.py` (exact certificates, two
independent methods per numerical claim), `verify.out` (its transcript).

---

## 0. Results

The paper's palette system (§5) consists of **six** axioms/properties, listed with their exact
quantifier structure in §1. The deliverable is a classification of them into exactly four
types, and one theorem per type, which together fix what a palette-level argument can prove.
Headline:

> **Barrier theorem (§8).** Every axiom of the paper's palette system is of one of four kinds:
> **(D)** direction-wise at one centre, **(L)** trace-linked to the colouring, **(B)** two-centre
> transport in a common direction, **(M)** multi-centre. **(D)**-systems have *no* locality content at all: satisfiable at one centre implies
> satisfied at *every* centre simultaneously (§3, Theorem A). Adding **(L)** keeps this true at
> *any countable* set of centres (§5, Theorem C, explicit witness). The single **(B)** axiom
> `(TE)`, evaluated at a countable centre set `X`, is *equivalent to `k`-colourability of the
> unit-distance graph on `X`* (§4, Theorem B) — so quantified over all countable `X` it is
> exactly `chi(R^2) <= k`, and at `k = 5` it is refuted at a **finite** centre set by the
> paper's own Theorem 1.1 + graph compactness (page 5), while at `k = 6` it is the open problem.
> The only two escapes for a palette-level proof of `(W)` at `k = 6` are therefore (i) a
> 7-chromatic finite unit-distance graph, or (ii) a step that is not confined to countably many
> centres — i.e. a measure-theoretic quantifier over a positive-measure family of centres, which
> is exactly what the paper's own §5.4 does at page 34.

Individual results:

| # | statement | status |
|---|---|---|
| **A** | Frozen-lift theorem: a direction-wise system satisfiable at one centre is satisfied at every centre of the plane by a single (hence jointly measurable) frozen field; the same with per-centre data. Consequently no direction-wise axiom has any locality content. | proved §3 |
| **B** | Countable split for the transport axiom: for countable `X`, `(TE)` on `X` `<=>` `chi(G[X]) <= k`; hence `(forall countable X: (TE) on X)` `<=>` `chi(R^2) <= k`. Calibration ladder `k = 3,4,5,6`. | proved §4 |
| **C** | The full palette system *with* the trace `(T)` is satisfiable at every **countable** centre set at `k = 6`, by an explicit colouring; the witness is a.e.-constant off a plane-null set. **C+**: when `G[X]` is `(k-2)`-colourable (at `k = 6`: `4`-colourable) even the transport axiom `(TE)` can be added, with an explicit non-frozen field. | proved §5 |
| **D** | `(5.2)` is not a direction-wise axiom: at one centre it is `3`-colourability of a collar graph (explicit `3`-colouring), and at *all* centres it is *equivalent in `S_1`* to self-avoidance `(SA)`, and implies `(SA)` in general. | proved §6 |
| **E** | `(T)` + `(5.7)` at every centre `<=>` `chi(R^2) <= k`; re-derived with the measurability point made explicit (Fubini is available because the violation set is colouring-defined; no joint measurability of `P` is assumed). This and `(TE)` at all centres (Corollary E1) are the only palette axioms whose all-centres version is the chromatic wall. | proved §7 |
| **F** | Non-vacuity: m13's `(M')`, m13's `(M)`, m6's survivor list (`16848 / 390936 / 268200 / 252`), m11/m4's frozen kill, Moser spindle, and the paper's finite non-5-colourable graph are each placed exactly. | §9 |

**What is not proved** (§10): nothing here decides `(W)` at `k = 6`; the barrier is a
*delimitation*, not a refutation. In particular the direction-wise fragment is *satisfiable*, so
it cannot exclude the accumulating locus — but it also cannot construct one, and no
colouring-level counterexample to `(W)` is produced here at any `k`.

---

## 1. Setting and the six axioms, with exact quantifier structure

Notation exactly as in the paper. `[k] = {1,...,k}`; `S = S^1` with normalised angular
probability `sigma`; `R` = rotation of *directions* by `kappa = pi/3`; `J` = rotation by `pi/2`;
`c : R^2 -> [k]` measurable ("weak measurable" = Definition 1.2, i.e. the monochromatic unit-pair
set has product measure zero); `A_i = c^{-1}(i)`; `P_x(e) sub [k]` the maximal palette of
Definition 5.1 at the centre `x` in direction `e`, defined up to angular null sets, nonempty a.e.

The quotations below are checked in `QUOTES.md` against two independent extractors
(`pdftotext -layout` and `mutool draw -F txt`); no formula here is used in a form that only one
extraction supports.

**(A1) `(5.2)` — palette transfer, first assertion** (p. 27, Lemma 5.2(1)):
for **every fixed centre** `x` and almost every independent-angle pair `(e,v) in S x S`,
```
        c(x + e + v)  not in  P_x(e)  union  P_x(v).                            (5.2)
```
Quantifier structure: one free centre, a.e. pair of directions; it involves the colouring at
points of `B(x,2)`.

**(A2) `(5.7)` — sixty-degree exclusion** (p. 29, Corollary 5.4): for **every fixed centre** `x`,
`P_x(f) ∩ P_x(Rf) = empty` for almost every `f in S`.

**(A3) `(5.3)` — smooth transport** (p. 27, Lemma 5.2(3)): for **two fixed centres** `z,x` and a
smooth representation `z + f = x + s(f) + t(f)` with `s,t` nonparallel and `s` a local
diffeomorphism in the angular coordinate, one has `P_z(f) ∩ P_x(s(f)) = empty` a.e. on the
domain. The instance used in the record (Remark 5.3, p. 29, with `z = x+a`, `s(f) = f`,
`t(f) = a`, `|a| = 1`) is the **unit-separation transport**
```
        (TE)      P_{x+a}(f) ∩ P_x(f) = empty   for every centre x, every |a| = 1, a.e. f.
```
`(TE)` is a *two-centre* relation: it constrains the palettes of two different centres at the
same direction.

**(A4) `(6.2)` — edge traces** (p. 35, Lemma 6.2): for every fixed centre `x` and every edge
`ij in Gamma_x`, `P_x(e)` is not contained in `{i,j}` for a.e. `e`. `Gamma_x` is the transition
graph of Definition 6.1 (p. 34): `ij in Gamma_x` iff for every ball `B` about `x`,
`limsup_{h->0} |D_ij(B,h)|/|h| > 0`, where `D_ij(B,h)` is the area of the `i↔j` transition set in
`B` at displacement `h`.

**(A5) nonemptiness** of `P_x(e)` a.e. (Definition 5.1 and the paragraph after it, p. 27).

**(A6) the palette bound.** At `k = 5`: `|P_x(e)| <= 2` a.e. (the main theorem of §5, p. 33-34).
At general `k` there is no bound at the single-centre level (the record's `m1`: only `K_6` is
excluded among the `2^15` graphs at `k = 6`). We therefore keep it as a *parameter* `|P| <= kappa`.

Two colouring-level properties of the maximal palette that are theorems (record, verified) and
that we use:

**(T) endpoint trace** (Lemma P of the record; constant sequences in Definition 5.1):
`c(x + e) in P_x(e)` for a.e. `e`, at every centre `x`.

**(SA) self-avoidance** (Lemma D of the record): if `x` is a density-one point of its own class,
`c(x) not in P_x(e)` for a.e. `e`.

**Remark 1.1 (null-set conventions and the `a.e.` in the centre).** Each axiom other than `(A3)`
is asserted "at every fixed centre", with an exceptional angular set that may depend on the
centre; the paper says so explicitly ("The null set in the last assertion may depend on the
individual trace, and the angular null sets may depend on `x`. ... **No joint measurability of
`P_x` in its center is assumed**", p. 27). This sentence is the pivot of everything below: it
means that a family `(P_x)` is *not* an object to which Fubini may be applied in `x`, and that
any statement obtained by integrating over centres must be justified separately.

---

## 2. The four types

**Definition 2.1.** Let `D` be a countable set of *label data* (a datum is a finite object: a
label, a finite graph on `[k]`, a finite family of palettes, ...).

* A **direction-wise** condition of type **(D)** is a condition on the a.e. equivalence class of
  a single measurable map `e |-> P_x(e)` (with values nonempty subsets of `[k]`), possibly
  depending on a datum `delta(x) in D` and on a finite list of directions related to `e` by
  isometries fixing `x`. It never mentions the colouring `c` and never mentions a second centre.
* A **trace-linked** condition of type **(L)** is a condition relating `P_x` to the colouring `c`
  at the single centre `x`: `(T)`, `(SA)`, `(5.2)`.
* A **transport** condition of type **(B)** relates the palettes at two distinct centres *in the
  same direction*: `(TE)`.
* A **multi-centre** condition of type **(M)** involves the palettes at several centres, possibly
  averaged over directions: `(5.3)` in its general form (paired directions `f`, `s(f)`), m9's
  averaged unit-triangle count, m12's sum-set density.

**(B) is the special case of (M) in which the constraint is "same direction, disjointness", and
it is the only (M)-form that Theorem B below decides exactly.**

**Proposition 2.2 (the classification is exhaustive for §5).**
`(A5)` nonemptiness, `(A2)` = `(5.7)`, `(A4)` = `(6.2)` with datum `delta(x) = Gamma_x`, and
`(A6)` the palette bound are of type **(D)**. Also of type **(D)** are the single-centre systems
the record decided: the complementary-palette exclusion, m11's bound `sigma{B sub P_x} <= 1/2`,
m1's `2^15` classification, and the `§8` orbit system of m6 (datum = centre colour and cycle
data). `(A1)` = `(5.2)`, `(T)`, `(SA)` and m7's circle bound
`|P_x(e)| + |Col(S(x+e,1))| <= k` are of type **(L)**. `(TE)` is of type **(B)**; `(5.3)` in
general, m9's averaged unit-triangle count `sum_i int_S |P_i| dsigma <= k` and m12's sum-set
density are of type **(M)**.

*Proof.* Immediate from the forms displayed in §1: each **(D)** item is a condition on the
a.e. class of `e |-> P_x(e)` alone; `(5.2)` contains `c(x+e+v)`; `(T)`, `(SA)` contain `c(x)`,
`c(x+e)`; m7's bound mentions the colouring on the circle about `x+e`; `(5.3)` contains palettes
at two centres at *paired* directions; m9's count integrates `|P_i|` at three centres. For the
`§8` system see m6's statement (`sprint/k6/REPORT.md` §4d and §6), whose variables are the six
`R`-orbit palettes at one centre together with the centre's colour and the cycle data. `square`

**Remark 2.2b (why (M) is separated from (B)).** Theorem B's proof extracts a *single* direction
`f` from a countable family of null sets and then reads off `min P_x(f)`; this needs the
constraint to be a same-direction disjointness. m9's and m12's constraints are *averaged* over
directions and are not decided by that argument, and indeed they do cut: m9's count is exactly
tight at `k = 6` (`2+2+2 = k`, and the residue it leaves on the vertices of a unit triangle
is excluded by decision, three independent ways), and m12's kills 7 of
the 9 palette models of the record. So (M) is *not* inert, and the barrier below does not claim
that it is.

**Remark 2.3 (`(5.2)` is *not* a direction-wise axiom in substance).** Although `(5.2)` is
quantified over directions at one centre, it is an a.e. condition on `c` over the **open disk**
`B(x,2)`, not on a circle: the map `(e,v) |-> x + e + v` is a submersion off the diagonal
`e = ± v`, with Jacobian
```
        |det d(e,v) (e+v)|  =  2 |sin(theta_e - theta_v)|,                    (2.1)
```
as one checks in the coordinates `e = e^{i(u+w)}`, `v = e^{i(u-w)}`, where `e + v = 2 cos(w) e^{iu}`
(exact certificate, `verify.py` §2, two methods). Hence `(5.2)` transports null sets of pairs to
null sets of *area* and back. This is what makes `(5.2)` a genuine hypothesis in §5 and what
makes it the **(L)**-axiom whose content is genuinely two-dimensional, and hence the one that the
"circles are null" heuristic of the barrier does not reach (§6, §10).

---

## 3. Theorem A: the frozen lift, and the absence of locality content in (D)

**Theorem A.** Let `Sigma` be a finite conjunction of **(D)**-conditions in the sense of
Definition 2.1 (with data `delta(x)`).
(i) If `Sigma` holds at one centre for some datum, it holds at every centre.
(ii) Let `X sub R^2` be **any** set (no countability, no measurability in `X`), and suppose that
for every `x in X` there is a measurable palette `P^{(x)}` satisfying `Sigma` at `x` with datum
`delta(x)`. Then the field `P_x := P^{(x)}` (`x in X`) satisfies `Sigma` at every `x in X`.
(iii) If the same `P^*` witnesses `Sigma` for every `x in X` (in particular if `Sigma` carries no
datum), then the frozen field `P_x := P^*` is **jointly measurable** in `(x,e)`: as a map
`R^2 x S -> 2^[k]` it is the composition of the projection with the measurable `P^*`.

*Proof.* (i), (ii) are immediate: a **(D)**-condition is a predicate on the single function
`e |-> P_x(e)` (and the datum), so it is evaluated centre by centre and imposes no relation
between distinct centres. (iii): `(x,e) |-> P^*(e)` is measurable as a composition; `2^[k]` is
finite, hence the target is standard. `square`

**Corollary A' (no direction-wise axiom has locality content).** A **(D)**-system cannot
distinguish one centre set from another, cannot exclude an accumulation, and cannot detect the
cardinality of `X`. In particular, if a **(D)**-system is satisfiable at one centre at label
count `k`, then it is satisfied at **every** centre of the plane simultaneously by a frozen
field — so it is compatible with every geometry of the centre set.

**Consequence for the record (a priori explanation of §4d).** Every decision problem that the
sprint decided at `k = 6` and that returned SAT — m1's `2^15` classification ("only `K_6`
excluded"), m6's orbit system (`16848 / 390936 / 268200 / 252` survivors, `0` at `k = 5`), m2's
five extra orbit conditions cutting nothing, m11's `sigma` bound — is a **(D)**-system. (The
record's two genuinely multi-centre constraints, m9's triangle count and m12's sum-set density,
are of type **(M)** and *do* cut; see Remark 2.2b, and §10 item (vii).) By Theorem A none of them *could* have cut: a **(D)**-system that is
satisfiable at one centre is satisfiable at every centre set, so its satisfiability is a
single-centre question, and m1 had already shown that only `K_6` is excluded at `k = 6`. The
SAT outcomes of §4d are therefore not empirical accidents; they are forced by the quantifier
structure. (Theorem A does not say that a **(D)**-system is satisfiable — only that its joint
satisfiability on any centre set is equivalent to its single-centre satisfiability.)

**Sharpness: which axioms are *not* of type (D), and why that matters.** `(T)`, `(SA)`, `(5.2)`
are **(L)**: they mention `c`, so they relate the palette at `x` to the palette at other centres
through the shared colouring. `(5.3)`, `(TE)` are **(B)**: they mention two centres. Of these,
the **(B)** axioms are the only ones that can be *unsatisfiable*, and §4 pins down exactly how.

---
## 4. Theorem B: the transport axiom at countably many centres is exactly finite unit-distance colouring

This is the load-bearing new statement of the note. It says that the **only** non-direction-wise,
non-trace palette axiom, evaluated at countably many centres, carries no information beyond the
existence of a `k`-colouring of a countable unit-distance graph — i.e. beyond the classical
finite problem, and nothing about the plane.

**Theorem B.** Let `k >= 2` and let `X sub R^2` be at most countable. For each `x in X` let
`P_x : S -> 2^[k]` be any map (no measurability, no regularity). Then the following are
equivalent:

1. **(TE) on `X`:** for every pair `x, x' in X` with `|x - x'| = 1`,
   `sigma { f in S : P_x(f) ∩ P_{x'}(f) ≠ empty } = 0`;
2. the unit-distance graph `G[X]` (vertex set `X`, edge `{x,x'}` iff `|x - x'| = 1`) admits a
   proper `k`-colouring.

Consequently:

3. `(TE)` holds on **every** countable `X sub R^2`, with palettes, if and only if
   `chi(R^2) <= k` — equivalently (de Bruijn–Erdős, [4, Theorem 1], quoted on p. 1 of the paper)
   if and only if every **finite** unit-distance graph is `k`-colourable.

*Proof.* `(1) => (2)`. `X` is countable, hence `X x X` is countable and the set of unit pairs
`E(X)` is countable. For each `{x,x'} in E(X)` let `N_{x,x'}` be the null set of directions where
the two palettes meet. Then `N := union_{E(X)} N_{x,x'}` is a countable union of `sigma`-null
sets, hence null; choose `f in S \ N`. For every unit pair, `P_x(f) ∩ P_{x'}(f) = empty`, and
both palettes are nonempty, so any selection `i(x) in P_x(f)` is a proper `k`-colouring of
`G[X]`: indeed `i(x) ≠ i(x')` for unit pairs because `i(x) in P_x(f)` and `i(x') in P_{x'}(f)`
lie in disjoint sets. The simplest selection is `i(x) = min P_x(f)`.

`(2) => (1)`. Let `i : X -> [k]` be a proper colouring of `G[X]` and put `P_x(f) := {i(x)}` for
all `f`. Unit pairs receive disjoint singleton palettes, so the exceptional set is empty.

`(3)`. `(<=)` A proper `k`-colouring of the whole plane restricts to a proper colouring of every
`G[X]`, so `(1)` holds for every `X` by the second part. `(=>)` If `(TE)` holds on every
countable `X`, then by `(1) => (2)` every countable unit-distance graph is `k`-colourable. Every
finite unit-distance graph is countable, so every finite unit-distance graph is `k`-colourable,
and the de Bruijn–Erdős compactness theorem gives a proper `k`-colouring of `R^2`. `square`

**Remark 4.1 (countability is not an artefact; it is the whole point).** The proof of
`(1) => (2)` uses countability of `X` twice: to have only countably many constraints, and to be
able to choose a *single* direction `f` that is good for all of them. For uncountable `X` the
union `union_{E(X)} N_{x,x'}` need not be null — a point `f` may lie in a null set for
uncountably many pairs — and the introduction of the paper warns exactly here: palettes are not
jointly measurable in the centre (p. 27), so there is no Fubini argument in `x` to replace the
countable union. Consequently `(TE)` at **all** centres is *strictly* stronger than `(TE)` at
every countable set of centres, and the two differ by exactly the content of the finite problem.

**Remark 4.2 (which pairs matter; sharpness of the class).** `(TE)` is used with `a` ranging over
the unit circle. If one replaces `a` by a countable set `A sub S` of unit vectors, `(1) => (2)`
still gives a colouring, but only a "colouring proper on the graph with differences in `A`",
which is a much weaker object (e.g. `A = {±1, ± i}` gives the square lattice, `chi = 2`). The
strength of Theorem B at distance one comes from `E(X)` being countable even though the
*direction* of each unit pair is arbitrary. In this form Theorem B covers arbitrarily many
centres at once and it is a statement about the paper's own axiom `(TE)`; the record's two-centre
CSP result (m10 / `sprint/k6/REPORT.md` §7) reaches the same 7-chromatic-finite-graph alternative
for a probe system with two centres, so the two are complementary, Theorem B having no bound on
the number of centres or on the geometry.

**Corollary B1 (calibration ladder — exactly where the paper's method has power).** Combine
Theorem B with the classical finite unit-distance graphs:

| `k` | finite unit-distance graph known not `k`-colourable | what `(TE)` at countable `X` says | `(TE)` refutable at finitely many centres? |
|---|---|---|---|
| 3 | Moser spindle, 7 vertices (1961) | `G[X]` 3-colourable | **yes** — `X` = spindle |
| 4 | de Grey (1581 vertices), Parts (509) | `G[X]` 4-colourable | **yes** — `X = V(H_4)` |
| 5 | the paper's own `H`: "Theorem 1.1 and graph compactness [4, Theorem 1] give a finite unit-distance graph `H` that is not five-colorable" (p. 5) | `G[X]` 5-colourable | **yes** — `X = V(H)`, *existentially* |
| 6 | **none known** | `G[X]` 6-colourable | **open** — a 7-chromatic finite unit-distance graph would do it |

The `k = 5` row is the exact sense in which the paper's method is a five-colour method: at
`k = 5` the transport axiom is already inconsistent at *finitely many* centres, and no
positive-measure family is needed to see it (the paper's actual proof nevertheless needs one, see
§8). At `k = 6` the transport axiom is consistent at every countable centre set exactly as long
as no 7-chromatic finite unit-distance graph exists. The `k = 3` row is verified in `verify.py` §1
(exact coordinates, a 4-colouring, and two independent refutations of 3-colourability).

**Corollary B2 (`(TE)` versus the general `(5.3)`).** `(TE)` is the instance `s(f) = f`,
`t(f) = a` of `(5.3)` (Remark 5.3, p. 29), so Theorem B applies to the palette field of any
weak measurable colouring. The *general* `(5.3)` is not of the form "same direction at two
centres" (`s(f) != f` in general) and Theorem B does not apply to it. That distinction is sharp:
for small separations `(5.3)` is satisfiable at **all** centres by a frozen field — m13's model
`(M')` satisfies `(P3)` for every distance `<= 1/50` at every centre — while `(TE)`, i.e. the
`d = 1` instance, is not (m11: a frozen field in `(TE)` reads `P(f) ∩ P(f) = empty`, so
`P(f) = empty` a.e., contradicting nonemptiness). So the transport axiom's content is carried by
the **unit** instance, not by the small-distance ones.

---

## 5. Theorem C: the trace-linked axioms are satisfiable at any countable centre set

**Theorem C.** Let `k >= 3`, let `X sub R^2` be countable, and let `P^* : S -> 2^[k]` be
measurable with
```
     P^*(f) ∩ P^*(Rf) = empty   for a.e. f                        (5.7)
```
and suppose there is a label `m in [k]` with `m not in P^*(e)` for a.e. `e`.
Then there are a measurable colouring `c : R^2 -> [k]` and palettes `(P_x)_{x in X}` such that at
every `x in X` all of the following hold:
```
   (T)      c(x+e) ∈ P_x(e)                         a.e. e
   (SA)     c(x) not in P_x(e)                      a.e. e
   (5.7)    P_x(f) ∩ P_x(Rf) = empty                a.e. f
   (5.2)    c(x+e+v) not in P_x(e) ∪ P_x(v)         a.e. (e,v)
   (D)      every direction-wise condition satisfied by P^* (with its datum)
```
Explicitly one may take `P_x := P^*` for every `x in X`, `Z := union_{x in X} S(x,1)` (a plane-null
set), and
```
   c(y) := m                          for y not in Z,
   c(y) := m                          for y in Z ∩ X            (priority),
   c(y) := min P^*(y - x)             for y in Z \ X, where x is the first centre
                                      of a fixed enumeration with y in S(x,1).
```

*Proof.* `Z` is a countable union of circles, hence Lebesgue-null and measurable; `c` is
measurable on each of the countably many measurable pieces (`S(x,1)` intersected with the set
where `x` is the first index) and on the complement of `Z`, with `y |-> min P^*(y-x)` measurable.
The last rule is well defined because `Z \ X = union_x (S(x,1) \ X)` and each point of it is
assigned by the first circle containing it.

`(T)` at `x`: for a.e. `e in S`, the point `x + e` lies on `S(x,1)`, and it is assigned by the
circle `S(x,1)` itself unless `x + e in X` or `x + e` lies on a circle `S(x',1)` with `x'`
earlier in the enumeration. Both exceptions are countable sets of directions `e` (one per point
of `X`, two per other centre), hence null. There `c(x+e) = min P^*(e) in P^*(e) = P_x(e)`.

`(SA)` at `x`: `x in X sub Z`, so `c(x) = m` by the priority rule, and `P_x(e) = P^*(e)` misses
`m` a.e.

`(5.7)` at `x`: by hypothesis on `P^*`.

`(5.2)` at `x`: the map `(e,v) |-> x + e + v` is nonsingular off the diagonal (Remark 2.3, (2.1)),
so the preimage of the null set `Z` (and of the countable set `X`) is a null set of pairs; for
`(e,v)` outside it, `c(x+e+v) = m`, while `P_x(e) ∪ P_x(v) = P^*(e) ∪ P^*(v)` misses `m` a.e.
(countable union of null sets over the two coordinates).

`(D)`: `P_x = P^*` and a **(D)**-condition depends only on `P_x` and its datum. `square`

**Corollary C1 (no countable-centre contradiction).** Let `Sigma` be the palette system consisting
of `(A5)`, `(A2)`, `(A6)` and any family of **(D)**-conditions, together with `(T)`, `(SA)`,
`(5.2)`. If `Sigma` is satisfiable at one centre (for `(A2)-(A6)` and the **(D)**-conditions) and
its data are those of a palette `P^*` admitting a label `m` absent a.e., then `Sigma` is
satisfied at **every** countable `X sub R^2` simultaneously, for every `k >= 3`. In particular the
palette axioms, including the trace, cannot be refuted at countably many centres.

**Theorem C+ (the whole system, including `(TE)`, at centre sets of small chromatic number).**
Let `k >= 4`, let `X sub R^2` be countable and suppose `G[X]` admits a proper colouring with at
most `k - 2` colours. Then there are a measurable colouring `c` and palettes `(P_x)_{x in X}`
such that at every `x in X`: `(T)`, `(SA)`, `(5.2)`, `(5.7)` **and `(TE)`** hold, together with
nonemptiness and the palette bound `|P_x| = 1`. In particular, at `k = 6` this holds for every
countable `X` whose unit-distance graph is `4`-colourable.

*Construction.* Let `i : X -> S sub [k]` be proper on `G[X]` with `|S| <= k-2`, and let `M, m` be
two distinct labels outside `S` (they exist because `|S| <= k-2`). Let `tau` be the cyclic
permutation of `S ∪ {M}` (no fixed points) and define, with
`phase(f) := floor(3 arg f / pi) mod 2` the parity of the sector of the direction `f`,
```
     P_x(f) := { i(x) }      if phase(f) = 0,
     P_x(f) := { tau(i(x)) } if phase(f) = 1.
```
`(5.7)`: `phase(Rf) = 1 - phase(f)` for every `f` (because `floor(3(theta+pi/3)/pi) =
floor(3 theta/pi) + 1`), so the two palettes are `{i(x)}` and `{tau(i(x))}`, distinct labels.
`(TE)`: `phase` does not depend on the centre, so at a fixed direction all centres are in the
same phase; both `i` and `tau o i` are proper colourings of `G[X]`, so unit-separated centres get
palettes `{i(x)} ≠ {i(x')}` (phase 0) or `{tau i(x)} ≠ {tau i(x')}` (phase 1). Nonemptiness and
`|P| = 1` are immediate. Finally build `c` exactly as in Theorem C with background label `m`:
`c := m` off `Z = union_x S(x,1)`, `c(x) := m` on `X`, and on `S(x,1) ∩ (phase 0)` put
`c := i(x)`, on `S(x,1) ∩ (phase 1)` put `c := tau(i(x))` (first circle in a fixed enumeration
wins on the countably many intersections, which is a null set of directions on each circle).
Then `(T)` holds a.e. on each circle by construction, `(SA)` because `c(x) = m` is not in
`S ∪ {M}`, and `(5.2)` because `x+e+v` is off `Z` for a.e. `(e,v)`, where `c = m` while
`P_x(e) ∪ P_x(v) sub S ∪ {M}`. `square`

**Corollary C+1.** At `k = 6`, for every countable `X` whose unit-distance graph is
`4`-colourable — in particular for the accumulating set of §9.5 — the three axiom types `(D)`,
`(L)`, `(B)` hold simultaneously at every `x in X`, with `(D)` comprising nonemptiness, the
singleton palette bound, `(5.7)`, and `(6.2)` vacuously (the witness colouring is `m` off a
plane-null set, so every transition set `D_ij(B,h)` is null and `Gamma_x = empty`). The general
`(M)` axiom `(5.3)` is not claimed; see §10(iii).

**Remark 5.1 (the witness is honest but flat: this is a consistency result, not a model of the
colouring problem).** In the construction, `c = m` off a plane-null set, so every transition set
`D_ij(B,h)` is null for small `h`: `Gamma_x = empty` for every `x`, hence `L(c) = empty` and
`(W)` holds trivially. Theorem C therefore establishes exactly one thing, and it is the thing
d3 asks for: **the palette axioms at countably many centres are mutually consistent**, so no
argument that evaluates them at countably many centres can derive a contradiction. It does *not*
exhibit a colouring with a large `L`; producing one is a genuinely 2-dimensional problem, since
`L` is defined through the transition areas `(6.1)` (§10, item (ii)).

**Remark 5.2 (the "free label" hypothesis is exactly what `(SA)` needs, and it is a
non-properness witness).** `(SA)` at `x` requires a label absent from `P_x` a.e.; Theorem C takes
that label as the colour of the centre. The record's `m2` (Thm R) proves that for a **proper**
colouring no label can be free in this sense (its class would be plane-null by Fubini over
circles). The tension is resolved by non-properness: in Theorem C the class of `m` is the
complement of a null set. So `(T) + (SA)` at countably many centres is a non-proper phenomenon,
and §7 shows that at *all* centres it is already the chromatic wall.

---
## 6. Theorem D: `(5.2)` is not a direction-wise axiom; it is self-avoidance in disguise

**Theorem D.** Let `c : R^2 -> [k]` be measurable and `(P_x)` palettes with `(T)` at every centre.

**(i) `(5.2)` at all centres implies `(SA)` at a.e. centre.** The set
`E := {x : sigma{e : c(x+e) = c(x)} > 0}` is Lebesgue-null.

**(ii) In the singleton class `S_1`** (every maximal palette a singleton a.e., i.e.
`P_x(e) = {c(x+e)}` a.e. for every `x`) the converse holds: if `E` is null then `(5.2)` holds at
every centre. Hence in `S_1`
```
     (5.2) at every centre   <=>   (SA) at a.e. point   <=>   for a.e. x: S(x,1) is a.e. free of the colour c(x).
```

**(iii) At one centre `(5.2)` has no chromatic content: it is satisfiable at `k = 3`, and `3` is
optimal.** In the singleton class, `(5.2)` at the centre `x` is exactly the statement that `c` is
a proper colouring of the **collar graph**
```
     H_x :  vertex set R^2,  edge {p,q}  iff  |p - q| = 1 and (p in S(x,1) or q in S(x,1)).
```
`H_x` contains the unit triangle `{x, x+e, x+Re}` (since `|1 - R| = 1`) and is 3-colourable; hence
`chi(H_x) = 3` exactly, and no `k >= 4` is needed. The colouring is the closed-form
`c_0 : R^2 -> {1,2,3}`,
```
     c_0(y) = 1 if |y| = 1 and floor(3 arg y / pi) is even,
     c_0(y) = 2 if |y| = 1 and floor(3 arg y / pi) is odd,
     c_0(y) = 3 if |y| != 1,
```
which satisfies `(T)`, `(SA)`, `(5.7)` and `(5.2)` at the centre `x_0 = 0` with
`P_0(e) := {c_0(e)}`, for every pair of directions outside a finite union of algebraic arcs (in
particular almost everywhere).

*Proof of (iii), collar graph.* In the singleton case `P_{x_0}(e) = {c(x_0+e)}`, so `(5.2)` at
`x_0` reads `c(x_0+e+v) != c(x_0+e)` and `!= c(x_0+v)` for a.e. `(e,v)`. With `p = x_0 + e` and
`q = x_0 + e + v` (so `|p - q| = 1` and `p in S(x_0,1)`) the first inequality says `c(q) != c(p)`
for a.e. pair with `p` on that circle; the second says the same with the roles of the two circle
points exchanged (`q` is also `x_0 + v + e`). Conversely, properness of `c` on `H_{x_0}` gives
both. So in the singleton class, `(5.2)` at `x_0` `<=>` `c` proper on `H_{x_0}`. For the
chromatic number: `{x_0, x_0+e, x_0+Re}` is a unit triangle (`|x_0 - (x_0+e)| = |e| = 1`,
`|x_0 - (x_0+Re)| = 1`, `|e - Re| = |1-R| = 1`), so `chi(H_x) >= 3`; and `c_0` is proper on
`H_{x_0}` because the circle is 2-coloured by the parity of `floor(3 arg/pi)`, which flips under
`R` and along every chord of length `1` (such a chord subtends `pi/3`), while every point off the
circle is adjacent to at most two circle points (two unit circles meet in at most two points) and
`x_0` is adjacent exactly to the circle. Colouring `x_0` and every off-circle point with `3` is
therefore proper on `H_{x_0}`, and `3` is optimal. Exact certificate: `verify.py` §4, checks
4.9-4.12.

*Proof of (i).* `(5.2)` at `x` says that the set `B_x := {(e,v) : c(x+e+v) in P_x(e) ∪ P_x(v)}` is
null. Let `N_x` be the null set of `e` where `(T)` fails at `x`. For `e not in N_x` we have
`c(x+e) in P_x(e)`, so for a.e. `v`
```
     c(x+e+v) not in P_x(e) ∪ P_x(v)   and   c(x+e) in P_x(e),
```
hence `c(x+e+v) != c(x+e)`. By Fubini, for a.e. `e not in N_x` the set `{v : c(x+e+v) = c(x+e)}`
is null, i.e. the point `x+e` is not in `E`. Therefore `sigma{e : x + e in E} = 0` for every `x`.
Now integrate over `x`: by Tonelli (all sets measurable, `1_E` and the translation action),
```
     |E| = ∫_{R^2} sigma{e : x + e in E} dx = 0,
```
so `E` is null. (ii) In `S_1`, `P_x(e) = {c(x+e)}` a.e., so `(5.2)` reads
`c(x+e+v) not in {c(x+e), c(x+v)}` a.e. If `E` is null, then for every `x` the section
`sigma{e : x+e in E} = 0` by the same Tonelli computation, so for a.e. `e` the point `x+e` has
`sigma{v : c(x+e+v) = c(x+e)} = 0`, giving the first inequality, and symmetrically the second.
(iii) Let `e = e^{i theta}`, `v = e^{i phi}` on `S(x_0,1) = S(0,1)`. `(T)`, `(SA)`, `(5.7)` are
immediate: `c_0(0) = 3 not in {1,2}`; and `floor(3(theta+pi/3)/pi) = floor(3 theta/pi + 1) =
floor(3 theta/pi) + 1` for every real `theta`, so the parity, hence `c_0`, flips under `R` and
`c_0(e) != c_0(Re)`. For `(5.2)`: if `|e+v| != 1` then `c_0(e+v) = 3 not in {1,2}`; if
`|e+v| = 1` then `{1, e, e+v}` is equilateral, so `e` and `v` are at angles `theta ∓ pi/3` where
`theta` is the direction of `e+v`, and the parity of both is opposite to that of `e+v`, giving
`c_0(e+v) not in {c_0(e), c_0(v)}`. `square`

**Corollary D1 (the record's Lemma D is not an independent hypothesis).** `(SA)` — which the
sprint records as a new colouring-level constraint and uses (with `(T)`) to kill all
centre-independent countermodels — is a **consequence** of the paper's own `(5.2)` together with
`(T)`, at every centre. In `S_1` the two are literally the same condition. So there is no
"extra" colouring-level axiom to be found here: the paper already has it.

**Remark 6.1 (`(5.2)` is a 2-dimensional axiom, hence not a `null-circles` axiom).** Combined
with Remark 2.3, Theorem D says `(5.2)` is an a.e. condition on the colouring over the *open
disk* `B(x,2)`: its trace part is self-avoidance at a.e. point of `S(x,1)`, and its remaining
part excludes `P_x(e) \ {c(x+e)}` at the sum points. This is why `(5.2)` cannot be treated by the
"circles are null" heuristic that governs the other one-centre axioms, and why Theorem A does not
cover it.

---

## 7. Theorem E: the trace plus `(5.7)` at all centres *is* the chromatic wall

The record contains two independent proofs of this equivalence (`m15` Theorem C, `m10` Theorem 4).
We re-derive it in order to make one point explicit that the record's statements leave implicit
and that §8 needs: the proof works because the *violation set is defined by the colouring alone*
and is therefore measurable in `(x,e)`, so Fubini in the centre is legitimate — **no joint
measurability of `P` is used**. This is precisely the property that `(TE)` lacks (Remark 4.1).

**Theorem E.** For every finite `k >= 2` the following are equivalent:

1. there is a measurable `c : R^2 -> [k]` and, for every centre `x`, a set `P_x(e) sub [k]` with
   `(T)` `c(x+e) in P_x(e)` for a.e. `e` and `(5.7)` `P_x(f) ∩ P_x(Rf) = empty` for a.e. `f`;
2. `chi(R^2) <= k`.

*Proof.* `(2) => (1)`: take a weak measurable `k`-colouring (which exists by the paper's Theorem
1.3) and put `P_x(e) := {c(x+e)}`. Then `(T)` holds identically, and `(5.7)` holds because
`c(x+e) != c(x+Re)` for a.e. `e` (the pairs `(x+e, x+Re)` are unit pairs, and the weak condition
excludes the monochromatic ones up to a null set of pairs; Fubini in `x`).

`(1) => (2)`: let `V := {(x,e) in R^2 x S : c(x+Re) = c(x+e)}`. This set is measurable: it is
the preimage of the diagonal under the measurable map `(x,e) |-> (c(x+Re), c(x+e))`. Suppose
`|V| > 0` in the product measure. By Fubini, `A := {x : sigma{e : (x,e) in V} > 0}` has positive
measure. Fix `x in A`; let `N_x` be the null set where `(T)` fails at `x` and `M_x` the null set
where `(5.7)` fails at `x`. For `e not in N_x ∪ M_x ∪ R^{-1}M_x`:
```
     c(x+e) in P_x(e),   c(x+Re) in P_x(Re)   (since Re not in M_x),   P_x(e) ∩ P_x(Re) = empty,
```
so `c(x+e) != c(x+Re)`, i.e. `(x,e) not in V`. Hence `sigma{e : (x,e) in V} = 0`, contradicting
`x in A`. So `V` is null.

Now transfer to unit pairs: the map
```
     Phi : R^2 x S -> {(u,w) : |w| = 1},      Phi(x,e) = (x + Re, e - Re)
```
is a bijection, with inverse `e = w/(1-R)`, `x = u - Re`; note `|1 - R| = 1` (the paper's own
observation, `kappa = pi/3`), so `e` is a unit vector and `|w| = |e - Re| = 1`. Its Jacobian in
the coordinates `e = e^{i theta}` is the `3 x 3` block matrix
`[[I, JRe],[0,(1-R)Je]]`, whose determinant is `det I · |(1-R)Je| = |1-R| = 1`; hence `Phi`
preserves the product of plane area with angular measure. Since `u + w = x + Re + e - Re = x + e`,
`Phi` maps `V` onto the set of monochromatic unit pairs `{(u,w) : |w| = 1, c(u) = c(u+w)}`, which
is therefore null. That is Definition 1.2, so `c` is a weak measurable `k`-colouring, and the
paper's Theorem 1.3 gives `chi(R^2) <= k`. `square`

**Remark 7.1 (why `(5.7)` and not `(TE)`).** The proof uses one fixed isometry `R` and one centre
per constraint, so the constraint set is a measurable subset of `R^2 x S` and one Fubini
argument disposes of it. For `(TE)` the constraint set
`{(x,a,f) : P_{x+a}(f) ∩ P_x(f) != empty}` involves the palettes at two centres and is not known
measurable in `(x,a)`; the paper explicitly does not assume the joint measurability that would be
needed (p. 27). The countable union in Theorem B is the only replacement, and it costs exactly
the countability of `X`. So the pair `{(T),(5.7)}` and the axiom `(TE)` sit on opposite sides of
the barrier *for a structural reason internal to the paper's own definitions*, not by accident.

**Corollary E1 (`(TE)` at all centres is also the wall).** If `(TE)` holds at every centre, then it
holds at every countable `X`, so by Theorem B `G[X]` is `k`-colourable for every countable `X`,
so every finite unit-distance graph is `k`-colourable, so `chi(R^2) <= k`. Conversely a proper
`k`-colouring gives singleton palettes satisfying `(TE)`. Hence
```
     (TE) at all centres   <=>   chi(R^2) <= k   <=>   (T)+(5.7) at all centres.
```

---

## 8. The barrier theorem, and where the record's decisions sit

Assemble §3–§7. Write `Sigma_pal` for the palette system `{(A5),(A2),(A4),(A6)}`, `Sigma_L` for
`{(T),(SA),(5.2)}` and `Sigma_B` for `{(5.3),(TE)}`.

**Barrier theorem.** Let `k >= 3`.

1. **(D) is inert.** Every data-free `(D)`-system satisfiable at one centre is satisfied at every
   centre of `R^2` by a jointly measurable frozen field, and every `(D)`-system satisfiable at
   each centre with its own datum is satisfied simultaneously on **any** centre set (Theorem A).
   So no direction-wise axiom has locality content, and the SAT outcomes of the sprint's
   single-centre decisions are forced by the quantifier structure rather than by the choice of
   axioms.
2. **(L) is inert at countably many centres.** `Sigma_pal ∪ Sigma_L` (with data of a palette
   admitting an absent label) is satisfied at every countable `X sub R^2` by an explicit
   measurable colouring and field (Theorem C). So the palette axioms *including the trace* cannot
   be refuted at countably many centres.
3. **(B) is exactly the finite problem.** `(TE)` on a countable `X` is equivalent to
   `k`-colourability of `G[X]` (Theorem B); `(TE)` at all centres is equivalent to
   `chi(R^2) <= k` (Corollary E1); and so is `(T)+(5.7)` at all centres (Theorem E). The two
   all-centres statements are equivalent *to each other only through their common equivalent*
   `chi(R^2) <= k`: `(T)+(5.7)` does not formally imply `(TE)` at the level of palette axioms.
4. **Therefore** any derivation of a contradiction from the palette axioms at a **countable**
   centre set `X` splits in two:
   (a) if it uses only the **(D)** and **(L)** axioms, it cannot succeed — Theorem C exhibits a
   model at `X`;
   (b) if it uses the **(B)** axiom, then by Theorem B its content is a `k`-colouring of the
   *countable* graph `G[X]`; by de Bruijn–Erdős this is a finite statement, so a genuine
   contradiction is already carried by a finite `X' sub X`, and at `k = 6` that `X'` is a
   7-chromatic finite unit-distance graph.
   So a palette-level proof of `(W)` at `k = 6` needs either a 7-chromatic finite unit-distance
   graph, or a step that is not confined to countably many centres.

**Where the paper's own §5 does this.** The one place in §5 that uses uncountably many centres is
the last paragraph of §5.4 (page 34):

> "The good angles still have positive measure, so they give infinitely many distinct binary
> centers on the compact circle `x + S`. Lemma 5.5 makes these centers uniformly separated. A
> uniformly separated subset of a compact metric space is finite, by a finite cover with
> sufficiently small balls. This contradiction proves the upper bound."

This step feeds a **positive-measure family** of centres on a compact circle into Lemma 5.5
(binary-centre separation), which is itself a `(B)`-type statement — its proof applies `(5.3)`
between two centres at distance `d < delta_*`. It cannot be replaced by a countable-centre
argument: by Theorem B a `(TE)`-type constraint at countably many centres is a `k`-colouring of a
countable graph, and "infinitely many distinct binary centres on a compact circle" is precisely
what makes the family uncountable. So the barrier is not vacuous: **the paper crosses it twice,
in §5.4 (page 34) and again in §6.3 (pages 38-41), where Lemma 5.5 is applied to an infinite
family of centres; the pairwise use of `(5.3)` inside Lemma 5.5 is allowed at countably many
centres, but the *finiteness via uniform separation* conclusion needs the quantifier over the
whole family.** The §7 and §8 stages, by contrast, are single-centre analyses of already
extracted data and are covered by the barrier. Consistent with that: at `k = 5` the finite
obstruction exists (Corollary B1), so the §5.4 crossing is not the only possible route at
`k = 5`; at `k = 6` no finite obstruction is known, and the `k = 5` palette bound `|P| <= 2` is
derived *by* §5.4, so it cannot be assumed.

**Table: the record's decisions and their type.**

| record item | type | what the barrier says |
|---|---|---|
| m1's single-centre classification (`2^15`, only `K_6` excluded) | (D) | forced: single-centre satisfiability propagates to every centre set |
| m6's §8 orbit system (`16848 / 390936 / 268200 / 252`, `0` at `k = 5`) | (D) with data | same; no cut *could* occur |
| m2's five extra orbit conditions `(SIN),(C1),(C2),(MON),(SA2)` cutting nothing | (D) | same; Theorem A predicts "cut nothing" a priori |
| m11's `sigma{B sub P_x} <= 1/2` | (D) | same |
| m7's circle bound `abs(P_x(e)) + abs(Col(S(x+e,1))) <= k` | (L) | needs the colouring; not a (D)-system |
| m9's averaged unit-triangle count; m12's sum-set density | (M) | **do cut** (Remark 2.2b); outside Theorem B's exact form |
| m13's `(M')`: frozen, `2`-valued, `(P1)-(P6)` at all centres | (D) | it is a frozen lift, i.e. the canonical (D)-model; killed only by `(TE)` |
| m13's `(M)`: frozen singleton, `(P1)-(P6)+(P7)` at all centres | (D)+(L-part) | satisfies `(5.2)` with `c ≡ 1`, fails `(T)` |
| m11/m4 frozen kill (`(TE)` `=>` `P(f) = empty`) | (B) | the sharp edge: frozen models die exactly at the transport axiom |
| paper §5.4 (page 34) | positive-measure family of binary centres + Lemma 5.5 | the only crossing; not replaceable at countably many centres |
| paper §6.3 (four/five-cycle cases, p. 38-41) | Lemma 5.5-type separation at a pair, applied to an *infinite* family of centres, plus the continuity Lemma 6.6 | pairwise `(B)`-use is allowed by the barrier; the failure at `k = 6` is the three-valued palette (m7 Lemma 4), not countability |
| paper §7, §8 | finitely many centres and `(D)`-data at one centre | cannot decide `(W)` at `k = 6` (barrier 4(a)) |

---
## 9. Non-vacuity and calibration

d3 requires the theorem to be tested for vacuity against the record's models. There are five
tests; each is exact, and each places one model on one side of the classification.

**9.1 m13's two models.** m13 (`smwfo9zkl/m13/no-go.md`, Theorem 2) exhibits, for `k = 6`,
`eps = 1/50`, two members of the class `P(6,eps)` on the **whole plane** `Z = R^2`:
```
     (M')  P_z(e^{it}) = Q_{s(t)},  Q_0 = {1,4}, Q_1 = {2,5}, Q_2 = {3,6},  s(t) = floor(9t/2pi) mod 3,
     (M)   P_z(e^{it}) = {4 + s(t)},
```
with every point a `T`-triangle point (`T = {1,2,3}`), and satisfying `(P1)-(P6)`, i.e.
nonemptiness, the palette bound `|P| <= k-3`, `(5.7)`, the exact `(5.3)` for every distance
`<= 1/50`, `(6.2)` for the triangle edges, and the no-complementary-triples condition.
* `(M')` is the **canonical (D)-model**: a frozen field, constant in the centre, which satisfies
  m13's direction-wise fragment `(P1)-(P6)` at *every* centre. By Theorem A it is exactly what a
  (D)-system can and cannot see: any (D)-system it satisfies at one centre is satisfied at every
  centre set, so no such axiom can exclude it. It is killed by the **(B)** axiom: a frozen
  field in `(TE)` reads `P(f) ∩ P(f) = empty`, hence `P(f) = empty` a.e., contradicting
  nonemptiness (this is m11's/m4's observation, one line). It also satisfies no `(L)` axiom: the
  union `Q_0 ∪ Q_1 ∪ Q_2 = [6]` contains every label, so `(SA)` fails at every centre, and `(5.2)`
  fails at positive-measure sets of directions with the constant colouring (because `1 in Q_0`).
* `(M)` is the **canonical (D)+(5.2)-model**: singleton palettes inside `O = {4,5,6}`, and `(5.2)`
  holds with `c ≡ 1` because `1 not in {4,5,6}`. It is killed by `(T)` (the trace would need
  `c(x+e) = 1 in P_x(e) = {4+s}`, false). It is also killed by `(TE)` (frozen).
So the pair `{(M'), (M)}` shows that the direction-wise fragment plus `(5.2)` is satisfiable at
every centre (m13's certificate), which is the non-vacuity witness for Theorem A and its
sharpness: **`(T)` and `(TE)` are the only axioms these models fail.** Theorem C then shows that
adding `(T)` and `(SA)` at countably many centres is still satisfiable, with the explicit
`a.e.`-constant colouring; i.e. the passage from "(M) at all centres" to "(M) at countably many
centres with the trace" is exactly where the colouring is allowed to degenerate.

**9.2 m6's survivors.** m6 (`smwfwi7rh/m6`) decided the `§8` orbit system at `k = 6` with
self-avoidance and every cell of the ray arrangement: `16848 / 390936 / 268200 / 252` surviving
configurations for `ell = 3,4,5,6`, and `0` at `k = 5` (the calibration reproducing Proposition
8.2). A surviving configuration is a triple (centre colour, starting cell, weak slip order of the
rays) together with palettes on the six `R`-orbit positions, and every condition in it is a
condition on the palettes and the centre datum at **one** centre. It is therefore a (D)-system,
and Theorem A applies with per-centre data: for **any** countable `X` and any assignment of a
survivor to each `x in X`, the pasted field satisfies m6's whole system at every `x in X`. So:
* m6's SAT outcome is not an accident of the encoding; Theorem A *predicts* it from m1's
  single-centre classification;
* the fact that the same system returns `0` at `k = 5` is compatible with Theorem A because
  single-centre satisfiability is `k`-dependent (`K_5`-type exclusions at `k = 5`), while
  *propagation* is `k`-independent.
Hence Theorem A is not vacuous on m6's data, and conversely m6's data do not test it: no
(D)-system can fail the propagation.

**9.3 m11 / m4 frozen kill (sharpness of Theorem B).** For a centre-independent field
`P_z = P`, `(TE)` at any unit pair reads `P(f) ∩ P(f) = empty`, so `P(f) = empty` a.e. and
nonemptiness fails. So the frozen lifts used by Theorem A and Theorem C never satisfy `(B)`; this
is exactly why the classification has three types rather than one, and it is the exact edge of
Theorem B: the `k`-colourability statement is what survives when the frozen field is ruled out.

**9.4 The paper's `k = 5` calibration.** By Corollary B1, at `k = 5` the transport axiom is
refuted at the **finite** set `V(H)`, where `H` is the finite unit-distance graph that the paper
extracts from Theorem 1.1 and graph compactness (p. 5). At `k = 6` the same statement is the open
problem, since a finite non-6-colourable unit-distance graph is a 7-chromatic unit-distance graph.
This is the exact sense in which the paper's method is a `k <= 5` method, sharper than the
record's "three-valued wall": the wall is not the number of values in a palette, it is the
existence of a finite obstruction at the *labelling level*, and at `k = 6` it is missing.

**9.5 An explicit accumulating centre set at `k = 6` where the whole system holds.** Let `p` be a
point, `u` a unit vector, and `X := V(M) ∪ {p + 3^{-n} u : n >= 1}`, where `M` is the Moser
spindle placed at distance `> 1/100` from the circle `S(p,1)`. Then:
* `X` is countably infinite with accumulation point `p`;
* `G[X]` is the spindle plus isolated vertices, hence 4-colourable with 4 = k-2 colours (exact
  certificate, `verify.py` §1 and §5);
* by Theorem B this makes `(TE)` satisfiable on `X` at `k = 6`, and by Theorem C+ the *same*
  field can also carry `(T)`, `(SA)`, `(5.2)` and `(5.7)`, with singletons `{i(x)}` / `{tau(i(x))}`
  alternating with the direction sector — checked exactly in `verify.py` §5 (5.6-5.8);
* alternatively, the palettes `P_x := P^*` from m13's `(M)` and the colouring `c` of Theorem C
  satisfy `(D)`, `(T)`, `(SA)`, `(5.2)`, `(5.7)` at every `x in X`, exactly, but not `(TE)`.
So at `k = 6` the **entire** palette system except the general `(5.3)` is satisfied on an
accumulating countable centre set. This is the concrete content of the barrier theorem, and it is
also its limit: the colouring constructed has `L = empty`, so it is *not* a counterexample to
`(W)` and does not touch the open problem.

**9.6 m15's block fields and m3's proper `k >= 7` colouring.**
* m15's three-block fields are frozen sector fields with pairwise disjoint block values; their
  frozenness makes them (D)-models in the sense of Theorem A (they satisfy the direction-wise
  fragment at every centre), and they die exactly at `(TE)` (m11/m4: a frozen field in `(TE)`
  gives `P(f) = empty`). So they test Theorem A's sharpness in the same way as m13's `(M')`, with
  a different block partition and a different palette size (`3` values instead of `2`).
* m3's proper measurable `7`-colouring with non-locally-finite `L` satisfies **every** axiom of
  §1 at every centre — with the single exception of the palette bound `(A6)`, which is a
  `k = 5`-specific statement — because all of them are theorems about arbitrary weak measurable
  colourings (Theorem 1.3 identifies proper and weak measurable colourings). Its `L` is not
  locally finite (one accumulation point), and `(W)` still holds for it. This is the sharpest
  available non-vacuity statement for the barrier: the palette axioms at all centres are
  simultaneously satisfied by a colouring whose cyclic locus accumulates — so the axioms cannot,
  by themselves, force `L` to be locally finite. What they *can* do is force `chi(R^2) <= 7`
  (Theorem E at `k = 7`), which is true. At `k = 6` the same statement would be `chi(R^2) <= 6`,
  which is the open problem: this is exactly the barrier.

---

## 10. What is not proved

(i) **Nothing here decides `(W)` at `k = 6`.** The note delimits the palette programme; it does
not settle the problem, and it does not produce a colouring whose `L` is infinite in a ball of
radius `> 1`.

(ii) **Theorem C's witness has `L = empty`** (Remark 5.1). Improving it to a witness with a large
`L` requires a 2-dimensional colouring, and by the record's tameness theorem (`m3` Lemma 1: for a
colouring constant on a locally finite partition with piecewise `C^1` boundaries, `Gamma_x` is the
interface graph and `L` is locally finite) any such colouring must be non-tame. This is the
remaining 2-dimensional problem, not a palette problem.

(iii) **Theorem B does not cover the general `(5.3)`** (only its `(TE)` instance, Remark 5.3).
For small separations the general `(5.3)` is satisfied at *all* centres by the frozen field
`(M')`, so it cannot be the binding axiom there; whether the general `(5.3)` has a countable
split analogous to Theorem B is open here.

(iv) **The paper's finite graph `H` at `k = 5` is existential** (p. 5). No explicit 6-chromatic
finite unit-distance graph is produced or recomputed here; the `k = 3` row of Corollary B1
(Moser spindle) is verified exactly, the `k = 4` row is cited from the literature quoted in the
paper's introduction, and the `k = 5` row is the paper's own existential statement.

(v) **Theorem A is about systems, not about colourings.** A (D)-system satisfiable at one centre
need not be the palette field of any colouring (that is what `(T)` adds, and by Theorem E,
`(T)+(5.7)` at all centres is the wall). So the barrier delimits what palette-level arguments can
*prove*, not what is true about the plane.

(vi) **No claim is made about `chi(R^2)`.** The note is consistent with both `chi = 6` and
`chi = 7`; indeed Corollary B1's `k = 6` row is exactly the alternative.

(vii) **The (M)-type constraints are outside the barrier.** m9's averaged unit-triangle count and
m12's sum-set density are multi-centre constraints, they do cut, and no countable/uncountable
split is proved for them here; Theorem B decides only the same-direction disjointness form
`(TE)`. So the precise statement of the barrier is: the **(D)** axioms are inert, the **(L)**
axioms are consistent at countably many centres, the **(B)** axiom at countably many centres is
the finite colouring problem, and the **(M)** axioms form a fourth family whose countable split
is open. This is compatible with what m9 and m12 achieve: they exclude *configuration residues*
at finitely many centres (the residue on a unit triangle; seven of nine palette models), not the
existence of a colouring.

---

## 11. Reproduction

```
python3 verify.py            # exact arithmetic only; prints one line per certificate
```

`verify.py` uses `fractions.Fraction` and `sympy` rational simplification only; no floating point
enters any decision. Every numerical claim has two independent implementations:

| section | claim | methods |
|---|---|---|
| 1 | Moser spindle is a 7-vertex, 11-edge unit-distance graph in `Q(sqrt3, sqrt11)`; 4-colourable; not 3-colourable; and the set-valued form of `(TE)` forces 3 colours | (a) exact distance test + exhibited 4-colouring + backtracking refutation; (b) full enumeration of all `3^7` assignments, and a direct exhaustive search over all `7^7` assignments of nonempty subsets of `[3]` |
| 2 | `(e,v) |-> e+v` is a submersion off `e = ±v`, `abs det = abs(sin(theta_e - theta_v))` (angle chart) and `2 abs(sin(theta_e - theta_v))` (`(u,w)` chart) | (a) sympy symbolic determinant in both charts; (b) the complex identity `det[i e, i v] = Im(conj(e) v)` checked symbolically |
| 3 | m13's sector words: `s(t + pi/3) - s(t) = 1 or 2 (mod 3)`; `(M)` satisfies `(5.7)`; `1 not in {4,5,6}`; `(M')` fails `(T)`/`(SA)` because `Q_0 ∪ Q_1 ∪ Q_2 = [6]` | (a) exact rational arithmetic on `t = 2 pi q` over 1000 grid points; (b) two further exact grids (denominators 997 and 128) plus the exact period check `s(q + 2/3) = s(q)` |
| 4 | Theorem D(iii): `c_0` satisfies `(5.2)`, `(5.7)`, `(T)`, `(SA)` at `0`; the collar graph `H_0` has `chi(H_0) = 3` exactly | (a) the equilateral identity `e^{i(theta-pi/3)} + e^{i(theta+pi/3)} = e^{i theta}`, the parity identity `floor(x+1) = floor(x)+1` and `abs(1-R) = 1`, symbolic, plus the exact unit triangle `{0, e, Re}` in `Q(sqrt3)`; (b) exhaustive exact checks on rational grids of directions (600 and 59 points) |
| 5 | the accumulating set `X` of 9.5: all unit pairs of `X` are exactly the spindle's 11 edges; `G[X]` 4-colourable; every spiral point is at distance `> 7` from every spindle vertex; and the phase field of Theorem C+ satisfies `(5.7)` and `(TE)` on all of `X` | (a) exact `Q(sqrt3,sqrt11)` arithmetic + the finite label algebra of `tau`; (b) exact rational interval enclosures of `sqrt3, sqrt11, sqrt33` (`Fraction` bounds, no floating point) |

The paper quotations in §1 and §8 were checked with two independent extractors
(`pdftotext -layout` and `mutool draw -F txt`); see `QUOTES.md`. All six displayed formulae used
above — `(5.2)`, `(5.3)`, `(5.7)`, `(6.1)`, `(6.2)`, `(1.1)` — appear identically in both
extractions, and the two sentences quoted in §8 (page 34) and §9.4 (page 5) do as well. No
formula in this note is taken from a single extraction.
