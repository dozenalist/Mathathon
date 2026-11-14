# Six colours: the Section 8 strip layer is provably powerless

**Deliverable.** A theorem about the paper's §8 architecture at `k = 6`, plus a
decided finite computation with two independent decision procedures and an
exact certificate. It is a **negative** result about a delimited inference
layer: the angular-obstruction layer of §8 — the part that excludes cycles of
length 3, 4, 5 at five colours — **cannot exclude any cycle length at six
colours**, and the theorem identifies, per cycle length, the exact five-colour
input that fails. The witnesses are closed-form, exact, and hold at *every*
direction, not merely almost every one.

It does *not* prove `chi(R^2) = 7`, construct a six-colouring, or decide local
finiteness of the cyclic locus. Section 8 delimits the class and states what is
not proved.

**Verification**: `python3 work/verify.py` (about 9 s, exit 0) prints every
table below: the classification table, the two-procedure cross-check, the
construction for `4 <= k <= 40`, the exact rational certificate, and the
global check of the palette field.

---

## 0. Results

`k` is the number of colours, `I = {0,...,k-1}` the label set, `x` a centre,
`P_x(e)` the maximal palette at `x` in direction `e` (Definition 5.1), `R`
rotation by `pi/3`, `Gamma_x` the transition graph (Definition 6.1), `S` the
unit circle of directions.

### The strip layer of §8

At a cyclic centre `x` carrying a cycle of common exclusion continua of length
`ell` from Proposition 7.1, with limiting directions `v_0,...,v_{ell-1}`, let
`B` be the finite set of directions perpendicular to some `v_i`. For
`u not in B` give edge `i` sign `sign(u . v_i)`, let `E_+` be the set of labels
that are endpoints of *positive* edges and `E_-` the same for negative edges,
and put `O(u) = I \ E_+`, `I(u) = I \ E_-` (§8.1; labels outside the cycle lie
in both). The constraints the paper uses in this range are

```
STRIP(k,ell), at a.e. direction u:
   S0  O(u) != empty and I(u) != empty                  Lemma 8.1
   S1  1 <= |P(u)| <= k-3                               Prop 5.6 / K6-BARRIER §1
   S2  P(u) meets O(u) and P(u) meets I(u)               Lemma 8.1, (8.1)
   S3  P(u) and P(Ru) are disjoint                       Corollary 5.4, (5.7)
   S4  (optional; used in every verdict below)
       P(u) is not contained in a cycle edge             Lemma 6.2, (6.2)
```

`P(u)` is the palette at `x` in direction `u`. Section 1 derives each item from
the paper; the only `k`-dependent item is `S1`.

> **Theorem 1 (classification of the strip layer).**
> For `k >= 4` and `3 <= ell <= k`, evaluated at the six `R`-orbit positions of
> one generic direction, `STRIP(k,ell)` is unsatisfiable for exactly
> `(k,ell) in {(4,3),(4,4),(5,5)}` and satisfiable otherwise. The `(5,5)` case
> is precisely Proposition 8.2. Hence for **every** `k >= 6` and **every**
> `ell in {3,...,k}` it is satisfiable.

> **Theorem 2 (global witnesses at six colours).** For `k = 6` and each
> `ell in {3,4,5,6}` there is an explicit measurable palette field on the whole
> circle of directions satisfying `S0`–`S4` at **every** direction `u` outside
> the finite exceptional set (the arc boundaries and the directions
> perpendicular to some `v_i`). Take
> `v_i = e^{i pi/3}` for `i < p = floor(ell/2)` and `v_i = e^{i 4 pi/3}`
> otherwise, and set
> ```
>    Phi(u) = P  if u in (r*pi/3, (r+1)*pi/3) with r even
>    Phi(u) = Q  if u in (r*pi/3, (r+1)*pi/3) with r odd
> ```
> with
> ```
>  ell=3 : P = {4},     Q = {5}
>  ell=4 : P = {4},     Q = {5}
>  ell=5 : P = {5},     Q = {1,3}
>  ell=6 : P = {1,4},   Q = {2,5}
> ```
> These are the closed forms `P = {k-2}, Q = {k-1}` for `k-ell >= 2`,
> `P = {k-1}, Q = {1,p+1}` for `k-ell = 1`, and `P = {1,p+1}, Q = {2,p+2}` for
> `ell = k`, specialised to `k = 6`. Every entry is a rational label set; no
> trigonometry beyond `cos(pi/3) = 1/2` is involved. The general-`k` form of the
> same construction is checked for `4 <= k <= 40`.

> **Corollary 3 (what §8 can no longer do at six colours).** No argument that
> derives a contradiction from `S0`–`S4` can work at `k >= 6`, for any cycle
> length. In particular
> * there is no six-colour analogue of Proposition 8.2 (the five-cycle
>   exclusion) — even though the six-cycle case has *no outsiders at all*;
> * the new `ell = 6` case is not decided by this layer either;
> * any successful six-colour angular argument must use at least one further
>   true constraint — for instance the two-centre exclusion (5.3), the sector
>   geometry of §8.4, or Lemma 6.3's state separation — not merely a better
>   case analysis of the printed data.

> **Theorem 4 (attribution, per §8 case).** The five-colour inputs of the four
> §8 cases, and what fails at `k = 6`:
>
> | §8 case | input beyond the strip layer | why it fails at `k = 6` | certificate |
> |---|---|---|---|
> | `ell=5`, Prop 8.2 | none — the strip layer *is* the proof | `\|P\| <= 2 = k-3` forces palettes to be pairs; at `k=6` a palette may be an outsider singleton or have three labels | `STRIP(5,5)` UNSAT; `STRIP(6,5)` SAT with `{5}`/`{1,3}` alternating |
> | `ell=4`, §8.3 + Lemma 6.4 | Lemma 6.4: no measurable state alternating between `{X}` and a fixed pair `D` | its last step needs the complement of `{X} u D` to be a **pair**; at `k=6` that complement has three labels and a unit equilateral triangle carries three colours without contradiction | `STRIP(5,4)` SAT, and its witness is exactly the `{X}`/diagonal state Lemma 6.4 must kill; `STRIP(6,4)` SAT with two outsider singletons |
> | `ell=3`, §8.4–8.6 | binary outsider state `s(e) in {X,Y}`, local constancy (8.6), Moser certificate (8.8) | the paper's step *"There cannot be two outsiders in such a palette, since (5.7) would leave no outsider at `Re`"* needs an outsider set of size `2 = k-3`; at `k=6` there are three outsiders, two may coexist, and the third serves `Re` | `STRIP(6,3)` SAT |
> | `ell=6` (new) | — the paper has no argument | the strip layer is satisfiable | Theorem 2, certificate §5 |
>
> The `ell=4` and `ell=3` rows also show that at `k=5` the strip layer is
> already powerless (`STRIP(5,3)`, `STRIP(5,4)` SAT): the printed five-colour
> proof needs Lemma 6.4 and §8.4–8.6 there. The *only* five-colour cycle the
> strip layer decides by itself is `ell=5`, and Theorem 1 says that decision
> does not survive to `k >= 6`.

### Relation to §7 (checked; agrees with `results/K6-BARRIER.md` correction (i))

§7 is label-blind: at a point `z` outside the removed core disks `Gamma_z` is a
forest, the support of `q^eps(z)` is a clique in it and therefore has at most
two elements (*"They therefore number at most two"*, proof of Lemma 7.4), so
the cover of Lemma 7.5 has multiplicity at most two at every `k`. The only
`k`-dependence of §7 is finiteness of `L_0 = L cap Q'`, i.e. Theorem 6.5. So
the printed architecture's `k`-dependence is exactly: **(a)** local finiteness
of the cyclic locus (triangle, four-cycle, five-cycle cases, and a new
six-cycle case) and **(b)** the pair-forcing content of §8, which Theorem 1
shows is unrecoverable at `k >= 6`. Theorems 1–4 concern (b); (a) is untouched
here and remains open.

---

## 1. The model, derived from the paper

Each item is quoted; all except the palette bound are `k`-blind.

**(1.1) The cycle.** Proposition 7.1 supplies a simple label cycle
`i_0,...,i_{ell-1}`, a centre `x`, a radius `rho`, compact connected continua
`K_j` and directions `v_j` with `q_{j,n} = x + r_{j,n} w_{j,n}`, `r_{j,n} -> 0`,
`w_{j,n} -> v_j`. The cycle is simple in the complete graph on the labels, so
`3 <= ell <= k`; the paper uses `ell in {3,4,5}` at `k=5`, and there is a new
`ell = 6` at `k = 6`. Relabel it `0..ell-1`, edge `i` joining `i` and
`i+1 mod ell`. *"All palettes in this section are at this fixed center."*

**(1.2) Strip sets and (8.1).** §8.1: *"Let `B` be the finite, antipodally
symmetric set of directions perpendicular to at least one `v_j`. At
`e not in B`, give edge `j` sign `+` or `-` according as `e.v_j` is positive or
negative. Let `O(e)` be the set of labels remaining after the endpoints of
every positive edge are removed, and let `I(e)` be the set remaining after the
endpoints of every negative edge are removed. Labels outside the cycle belong
to both sets."* Lemma 8.1: *"Both `O(e)` and `I(e)` are nonempty for every
`e not in B`… Moreover, `P_x(e) cap O(e) != empty`, `P_x(e) cap I(e) != empty`
for almost every `e in S \ B`."* The proof uses only Proposition 7.1's
exclusion `H_{i_j} cap Delta(K_j) = empty` and the measurable partition of the
plane: no use of the number of colours. This gives `S0` and `S2`. A cycle label
is an endpoint of its two incident edges, so `O(u) cap I(u)` is exactly the set
of labels outside the cycle.

**(1.3) Sixty-degree exclusion.** Corollary 5.4: `P_x(f) cap P_x(Rf) = empty`
for a.e. `f`, from Lemma 5.2 assertion 3 with `x + f = x + Rf + R^{-1}f`. This
is `S3`, `k`-blind.

**(1.4) Palette bound.** Proposition 5.6 gives `1 <= |P_x(e)| <= 2` at `k = 5`;
the general bound `1 <= |P_x(e)| <= k-3` is `results/K6-BARRIER.md` §1, giving
`|P| in {1,2,3}` at `k = 6`. This is `S1`, the only `k`-dependent input.

**(1.5) Lemma 6.2.** `ij in Gamma_x` implies `P_x(e)` is not contained in
`{i,j}` for a.e. `e` ((6.2)). In the models I take `Gamma_x` to contain the
extracted cycle; that is the minimal choice consistent with `x in L` and it can
only add constraints, so `S4` strengthens every satisfiability verdict.

**(1.6) One `R`-orbit.** §8.2: *"Choose a direction on a full six-position
`R`-orbit for which all the preceding almost-everywhere assertions and (5.7)
hold."* Note `R^3 = -1`, so the orbit contains `e` and `-e`.

**(1.7) Completeness of the phase reduction.** For fixed `e`, the sign of edge
`i` at `R^j e` is `sign(cos(j pi/3 - arg v_i))`. The set `{u : u.v_i > 0}` is
an open semicircle of angular length `pi = 3(pi/3)`, the six directions `R^j e`
are equally spaced by `pi/3`, and none is perpendicular to `v_i` because
`e not in R^{-j}B`; hence exactly **three consecutive** positions are positive,
so the sign vector of edge `i` is determined by the start `delta_i in Z/6` of
its positive run, and `delta` ranges over all of `(Z/6)^ell`. That exhausts the
data, and the decision procedures below quantify over all of it.

---

## 2. Proof of Theorem 1

The three unsatisfiable cases first.

* `(4,4)`: `ell = k`, so there are no outsiders and `O(u) cap I(u) = empty`;
  `|P| <= 1` makes `P` a singleton inside `O cap I`, contradicting `S2` for
  every `delta`.
* `(4,3)`: `|P| <= 1` and `O cap I = {3}`, the unique outsider, so `P_j = {3}`
  at every position and `S3` fails.
* `(5,5)`: Proposition 8.2 of the paper; `verify.py` reproduces the verdict
  from the clauses alone (Section 4).

For the satisfiable cases write `p = floor(ell/2)` and take `delta_i = 0` for
`i < p`, `delta_i = 3` for `i >= p`, i.e. `v_i = e^{i pi/3}` for `i < p` and
`e^{i 4 pi/3}` for `i >= p`. At the positions `j = 0,1,2` the positive edges
are `{0,...,p-1}`, with endpoints `{0,...,p}`, and the negative edges are
`{p,...,ell-1}`, with endpoints `{0} u {p,...,ell-1}`; hence

```
   O = {p+1,...,k-1},     I = {1,...,p-1} u {ell,...,k-1}     (j = 0,1,2),
```

and at `j = 3,4,5` the two sets are exchanged. Take the word `P,Q,P,Q,P,Q`:

* **(A) `k - ell >= 2`:** `P = {k-2}`, `Q = {k-1}`. Both are labels outside the
  cycle (`k-2 >= ell`), hence lie in `O cap I` at every position; they are
  disjoint, have size `1 <= k-3` (`k >= 4`), and are singletons, so no cycle
  edge contains them.
* **(B) `k - ell == 1`:** `P = {k-1}`, `Q = {1,p+1}`, with `p >= 2` for
  `k >= 5`. The unique outsider meets both strip sets everywhere, and
  `p+1 <= k-1 = ell`, `p+1 >= 3`, so `P cap Q = empty`. At `j in {0,1,2}`,
  `1 in I` (as `p >= 2`) and `p+1 in O`; at `j in {3,4,5}` the sets are
  exchanged and the same memberships hold. `|Q| = 2 <= k-3` for `k >= 5`.
  `{1,p+1}` is not a cycle edge: `p+1 = 2` forces `p = 1`, and the only edge
  containing `0` is `{0,ell-1}`.
* **(C) `ell == k`:** `p = floor(k/2) >= 3` and `p+2 <= k-1` for `k >= 6`;
  `P = {1,p+1}`, `Q = {2,p+2}`. At `j in {0,1,2}`, `O = {p+1,...,k-1}` contains
  `p+1,p+2` and `I = {1,...,p-1}` contains `1,2`; at `j in {3,4,5}` the sets
  are exchanged. `P cap Q = empty`, `|P| = |Q| = 2 <= k-3`, and neither pair is
  a cycle edge (`p+1 >= 4`, `p+2 >= 5`, neither contains `0`). `S0` holds since
  `p+1 <= k-1` and `p-1 >= 2`.

This covers every `(k,ell)` with `k >= 6`, together with `(5,3)` and `(5,4)`;
the three cases above are the rest, so Theorem 1 follows. `verify.py` checks
the closed form against the checker for all `4 <= k <= 40`, `3 <= ell <= k`:
737 pairs verified, failures exactly at `(4,3)`, `(4,4)`, `(5,5)`.

## 2'. Proof of Theorem 2 (global field)

The two values `e^{i pi/3}` and `e^{i 4 pi/3}` are antipodal, so for every `u`
not perpendicular to either, exactly one of the groups `{i < p}`, `{i >= p}` is
positive. Hence at every direction the strip sets are

```
   {p+1,...,k-1}   and   {1,...,p-1} u {ell,...,k-1}
```

in one order or the other; since `S2` asks for a palette meeting *both*, the
condition is the same at every direction. The sets `P`, `Q` above meet both and
have size at most `k-3`, giving `S0`, `S1`, `S2`, `S4`. Rotation by `pi/3`
shifts the arc index `r` by exactly one, so `Phi(Ru)` is the other member of
the disjoint pair `{P,Q}`, giving `S3`. The exceptional directions are the six
arc boundaries and the two perpendiculars to the `v_i`; they are finite, so the
field is defined and satisfies the system almost everywhere — in fact
everywhere else. `verify.py` re-checks the field at 180
equally spaced directions with exact rational angles for `k = 5,6`: at `k = 6`
every length passes at every direction, and at `(k,ell) = (5,5)` the field
necessarily fails on half of them, consistent with `STRIP(5,5)` being
unsatisfiable.

---

## 3. The two decision procedures

* **Procedure 1** (`p1_decide`): for each `delta` in `(Z/6)^ell`, build the
  strip sets, discard `delta` if some allowed set is empty, list the admissible
  palettes at each of the six positions, and search for a closed six-tuple with
  consecutive disjointness by backtracking.
* **Procedure 2** (`p2_decide`): a propositional CNF over the variables "label
  `i` belongs to `P_j`" — nonemptiness, `|P_j| <= k-3` as one clause per
  `(k-2)`-subset, one clause per strip set, one binary clause per
  `(j, j+1, i)` for disjointness, and one per cycle edge for `S4` — decided by
  a from-scratch DPLL run twice with opposite branching orders. Every CNF model
  is re-verified by the from-scratch checker.

They agree on all `(k,ell)` with `4 <= k <= 7`, `3 <= ell <= k`, with and
without `S4`: 24 verdicts, **zero disagreements**; the two procedures find
*different* witnesses, as they should.

```
$ python3 verify.py
  k=4 ell=3   procedure1=UNSAT procedure2=UNSAT
  k=4 ell=4   procedure1=UNSAT procedure2=UNSAT
  k=5 ell=3   procedure1=SAT   procedure2=SAT
  k=5 ell=4   procedure1=SAT   procedure2=SAT
  k=5 ell=5   procedure1=UNSAT procedure2=UNSAT      <- Proposition 8.2
  k=6 ell=3   procedure1=SAT   procedure2=SAT
  k=6 ell=4   procedure1=SAT   procedure2=SAT
  k=6 ell=5   procedure1=SAT   procedure2=SAT
  k=6 ell=6   procedure1=SAT   procedure2=SAT       <- the new case
  k=7 ell=3..7                     SAT (all)
  disagreements between the two procedures: NONE
```

---

## 4. Validation against the paper (vacuity test)

`STRIP(5,5) = UNSAT` is the check that the model *is* the paper's.
Proposition 8.2 uses only `S0`–`S3` at `k = ell = 5`, and the machine
reproduces its conclusion from those clauses with no further input. The
reasoning is visible in the blocking data: with no outsiders
`O_j cap I_j = empty`, `|P_j| <= 2` and `S2` force palettes to be pairs meeting
both allowed sets; nonemptiness forces exactly one positive and one negative
run (lengths 2 and 3); one of `O_j, I_j` is a singleton; the forced pair plus
the flip under `R` gives the parity contradiction of §8.2.

Conversely `STRIP(5,3)` and `STRIP(5,4)` are SAT, matching the fact that
§8.4–8.6 and §8.3 need extra input at `k = 5`, and the `(5,4)` witness *is* the
`{X}`/diagonal state that Lemma 6.4 kills. So the model is neither too weak
(it reproduces the one five-colour case the strip layer decides) nor arbitrary
(at the other five-colour cases its witnesses are exactly the configurations
the paper's remaining lemmas attack).

---

## 5. Exact certificate for `k = ell = 6`

Centre `x = (0,0)`, test direction `e = (1,0)`,

```
   v_0 = v_1 = v_2 = (1/2, sqrt3/2) = e^{i pi/3}
   v_3 = v_4 = v_5 = (-1/2, -sqrt3/2) = e^{i 4 pi/3}
   P(R^j e) = {1,4} for j = 0,2,4      and     {2,5} for j = 1,3,5
```

Every inner product `R^j e . v_i` equals `+-1` or `+-1/2`, all rational (stored
as `(cx, sy)` meaning `(cx, sy sqrt3/2)`, so that `cx cx' + (3/4) sy sy'` is an
exact rational). The sign matrix is

```
   edges 0,1,2 :  + + + - - -
   edges 3,4,5 :  - - - + + +
```

hence `O_j = {4,5}`, `I_j = {1,2}` for `j = 0,1,2` and the exchange for
`j = 3,4,5`. `{1,4}` and `{2,5}` meet both, are disjoint, have size `2 <= 3`,
and are not cycle edges; the word closes because `P_5 = {2,5}` is disjoint from
`P_0 = {1,4}`. This is the phase vector `delta = (0,0,0,3,3,3)`, and it is the
`ell = 6` row of Theorem 2.

**Reading.** The certificate is a palette *system*, not a colouring: it says
that `S0`–`S4` are simultaneously satisfiable at every direction, so an
argument asserting exactly those things cannot be contradictory. It is
compatible with `chi(R^2) = 7`.

---

## 6. Why each five-colour §8 case fails at `k = 6`

* **`ell = 5` (Prop 8.2).** *"The allowed sets are the internal vertices of
  these runs, of sizes one and two. They are disjoint. The palette size bound
  (5.12) and (8.1) imply that almost every palette is a pair, containing one
  vertex from each allowed set."* At `k = 6` one outsider is left; it lies in
  both strip sets, so `{outsider}` is admissible and `|P| <= 3` allows
  `{5}`/`{1,3}` to alternate.
* **`ell = 4` (§8.3).** Reduces to a state with values `{X}` and a diagonal
  `D`, killed by Lemma 6.4, whose proof puts three points `z_j` forming a unit
  equilateral triangle, each of density one in *"the union of the two labels
  outside `{X} u D`"*, and concludes *"the resulting unit equilateral triangle
  would be properly colored with two labels, a contradiction."* That needs the
  complement of `{X} u D` to be a pair, i.e. `k = 5`. At `k = 6` there are two
  outsiders, the complement has three labels, and a unit equilateral triangle
  carries three colours without contradiction. The `k = 6` witness is
  `{4}`/`{5}`, whose complement has four labels.
* **`ell = 3` (§8.4).** *"There cannot be two outsiders in such a palette,
  since (5.7) would leave no outsider at `Re`."* This is where an outsider set
  of size `2 = k-3` is used. With three outsiders a palette may contain two of
  them and the third is available at `Re`, so the binary state `s(e)` is not
  forced and Lemmata 8.6–8.8 with the seven-point certificate have no `k = 6`
  analogue.
* **`ell = 6` (new).** No argument exists, and the strip layer cannot supply
  one: Section 5.

---

## 7. Files and commands

All paths relative to `.ultramath/smwfo9zkl/m6/`.

| file | contents |
|---|---|
| `RESULTS.md` | this document |
| `work/verify.py` | **self-contained; run this**: model + checker, procedure 1, procedure 2 (CNF/DPLL), closed-form construction, exact certificate, global-field check, main table |
| `work/global_field.py` | the global palette field as a standalone script |
| `work/model.py` | model + from-scratch checker (used by the exploration scripts) |
| `work/search1.py`, `work/search2.py` | the two procedures as standalone scripts, with `strip_table.json`, `strip_table_cnf.json` and the cross-check |
| `work/construction.py` | the closed-form word, checked for `4 <= k <= 40` |
| `work/certificate_k6.py` | the exact rational certificate for `k = ell = 6` |
| `work/paper.txt` | `pdftotext -layout` working copy of the paper |

```
$ python3 work/verify.py        # everything, ~9 s, exit status 0
$ python3 work/global_field.py  # global field on a finer mesh
$ python3 work/certificate_k6.py
$ python3 work/search1.py && python3 work/search2.py   # two procedures + cross-check
$ python3 work/construction.py
```

**Formula checking.** Every formula used is quoted verbatim in Section 1 from
both `pdftotext -layout` and `pdftotext -raw`, which agree glyph for glyph; the
symbol content of (8.1) (`cap`, `neq`, `empty`) was re-confirmed from the PDF
glyph boxes with `pdftotext -bbox`. Pages 50–51 were also rendered with
`pdftoppm -r 150`; I could not inspect them visually (no image channel on my
side), so the check is the two-extraction agreement plus the glyph-box check,
not a rendered image. The only numerical identities used beyond the quoted
statements are `cos(pi/3) = 1/2` and `cos(2 pi/3) = -1/2`.

---

## 8. Exact class covered, and what is not proved

**Class covered.** The constraints `S0`–`S4` of Section 0, at a cyclic centre
`x` carrying a cycle of common exclusion continua of length `ell` as produced
by Proposition 7.1, evaluated either at the six `R`-orbit positions of one
generic direction (Theorem 1) or at every direction (Theorem 2). By Section 4
this is exactly the input of Proposition 8.2's proof, and it includes
Lemma 6.2 as an optional strengthening.

**Proved.** Theorem 1 (classification, hence powerlessness for every `k >= 6`
and every `ell`), Theorem 2 (explicit global six-colour fields, including the
new `ell = 6`), Corollary 3, Theorem 4 (per-case attribution with
certificates).

**Not proved.**
* No six-colouring is constructed and no lower bound on `chi(R^2)` is improved;
  `chi(R^2) >= 7` is **not** proved.
* Nothing is asserted about local finiteness of
  `L = {x : Gamma_x contains a cycle}` (Theorem 6.5) at `k = 6`, which §7 needs;
  that remains open and is another direction's problem.
* The witnesses are palette systems, not colourings. The result concerns an
  inference layer and is compatible with `chi(R^2) = 7`.
* The strip layer is not all of §8. The theorem shows that the remaining
  five-colour inputs — Lemma 6.4, the binary outsider state, the Moser
  certificate — must be replaced by something else at six colours; it does not
  show that no six-colour angular argument exists.
