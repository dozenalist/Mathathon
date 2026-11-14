# Sum-set density transport at six colours

member `m12`, swarm `smwfwi7rh`, direction `d17`
Files: `THEOREM.md` (this file), `verify.py`, `verify_indep.py`, `verify.out`, `verify_indep.out`.

**Headline.** The paper's Lemma 6.4 mechanism generalises verbatim from the unit triangle to an
arbitrary finite unit-distance graph: the *chromatic number of a finite unit-distance graph inside a
direction-sum set* bounds the number of labels that two disjoint palette groups force outside
themselves (Theorem 1). The mechanism uses only Lemma 4.3 and Lemma 5.2(2) — no palette bound, no
self-avoidance, no properness of a label function, no maximality. Two consequences:

* **Theorem 3 (new no-go, exact).** Every *pair-valued* palette-level countermodel produced by the
  previous swarm — the `m15` uniform block field for `ell = 3,4,5,6` and the `FREE-LABEL` word for
  `ell = 4,5,6` — is impossible as the maximal palette field of *any* weak measurable 6-colouring.
  Seven of the nine models die; the only survivors are the two *singleton-valued* ones, and a
  six-cycle centre has no singleton palette. Exact rational certificates, two independent
  implementations.
* **Correction of the record.** `sprint/k6/REPORT.md` §5 and `sprint/k6/FREE-LABEL.md` conclude that
  "the only constraint that removes these models is **properness** of the colouring", and the sprint
  ledger lists as the exact frontier "trace-consistency with a proper 6-colouring". That is wrong:
  Lemma 5.2(2) already removes them, with no properness, no trace-consistency and no maximality
  hypothesis. The correct frontier is one step further in (§6 below).

The mechanism does **not** decide the six-cycle case: it leaves a sharply described "fragmented"
class alive (§6c), so the open problem at `k = 6` is unchanged in substance, but its boundary moves.

---

## 1. The inputs used, and the check

Paper: `attachments/here-are-three-files-ni5n/paper.pdf`. Notation: `c` a weak measurable
`k`-colouring (Def 1.2), `A_i` its colour classes, `H_i` the closed essential supports,
`I = {1,...,k}`, `S = S^1` with angular measure `sigma`, `kappa = pi/3`, `R` = rotation of
directions by `kappa`, `P_x` the maximal palette at the centre `x` (Def 5.1), `Gamma_x` the
transition graph (Def 6.1), `L = {x : Gamma_x has a cycle}`.

| input | statement used | where |
|---|---|---|
| Lemma 4.3 | the full-density-point set of each `A_i` contains no unit pair; the density-point sets are disjoint and their union is conull | p. 25 |
| Lemma 5.2(2) | if `e` is an angular density-one point of `D_{x,i} = {e' : i in P_x(e')}` then for every `v` not parallel to `e` the spatial density of `A_i` at `x + e + v` is **zero** | p. 27-28 |
| Lemma 5.2(1) | `c(x+e+v) notin P_x(e) u P_x(v)` for a.e. independent pair | p. 27 |
| Cor. 5.4 (5.7) | `P_x(f) cap P_x(Rf) = empty` a.e. | p. 29 |
| Lemmas 6.2, (6.2) | `ij in Gamma_x` gives a trace `b` with `b_i = b_j = 0` a.e., supported in the palette | p. 34-35 |
| Lemma 6.4 | `gamma = 2 arcsin(1/(2 sqrt 3))`, `cos gamma = 5/6`, `z_j = x + e^{i(t+2j kappa)} + e^{i(t+pi+gamma+2j kappa)}` form a unit equilateral triangle | p. 37 |

*Extraction check.* `pdftotext -layout` and `pdftotext -raw` of p. 37 agree textually on Lemma 6.4
("`gamma = 2 arcsin 1/(2 sqrt 3), cos gamma = 5/6`" and "`z_j = x + e^{i(t+2j kappa)} +
e^{i(t+pi+gamma+2j kappa)} = x + e^{i(t+2j kappa)}(1 - e^{i gamma})`", "distance `|1-e^{i gamma}| =
1/sqrt 3`", "equilateral triangle of side one"); p. 27-28 agree on Lemma 5.2(2). The arithmetic
content is re-derived exactly in `verify.py` §A: `cos(2 arcsin(1/(2 sqrt3))) = 1 - 2/12 = 5/6`,
`|1-e^{i gamma}|^2 = 2 - 2 cos gamma = 1/3`, `|e^{2 i kappa} - 1|^2 = 3`, hence the side is
`sqrt(3) * (1/sqrt 3) = 1`. (This session has no image channel; the check is textual cross-extraction
plus exact re-derivation of every displayed constant, as above.)

Also used, from the sprint's own record (`sprint/k6/STRUCTURE.md`, Lemma 3 and Corollary 4, with
proof): **at a centre whose `Gamma_x` contains a cycle with vertex set `V(C)`, no palette is a
singleton with its label in `V(C)`.** In particular at a six-cycle centre (`V(C) = [6]`) every
palette has at least two labels. Proof restated: if `P_x(e) = {b}` on a positive-measure set and
`b in {u,v}` for an edge `uv` of the cycle, Lemma 6.2's trace `b^{uv}` is supported in `P_x(e)`, so
it vanishes at `u` and `v` a.e., contradicting `sum_l b^{uv}_l = 1`.

---

## 2. Theorem 1 (chromatic content of a direction-sum set)

**Theorem 1.** Let `k >= 3`, `c` a weak measurable `k`-colouring, `x in R^2` a centre,
`G_1, G_2 <= I` disjoint label groups, and `E_1, E_2 <= S` measurable with `sigma(E_j) > 0` and
`G_j <= P_x(e)` for almost every `e in E_j`. Let `E_j^*` be the angular density-one points of
`E_j` and put

```
   Z = { x + e^{ia} + e^{ib}  :  a in E_1^*,  b in E_2^*,  e^{ia} not parallel e^{ib} } .
```

Then for every **finite unit-distance graph** `Q <= Z` (a finite set of points of `Z` whose unit
pairs are the edges):

```
        | I \ (G_1 u G_2) |  >=  chi(Q) .
```

*Proof.* Fix `a in E_1^*`, `b in E_2^*` nonparallel and put `z = x + a + b`. For `i in G_1` we have
`E_1 <= D_{x,i}`, so `a` is an angular density-one point of `D_{x,i}`, and Lemma 5.2(2) gives that
`A_i` has spatial density zero at `z`. The same with `b` for `i in G_2`. Since finitely many sets of
density zero cannot fill a ball, the union `U` of the colour classes with labels in
`T' := I \ (G_1 u G_2)` has (upper) density one at `z`. Hence **every** point of `Z` is a
density-one point of `U`.

Now let `Q = {q_1,...,q_n}` be a finite unit-distance graph contained in `Z`. For each `j` the set
`W_j = {w : q_j + w in U}` has density one at `0` (it is `U` translated back), so
`W = W_1 cap ... cap W_n` has density one at `0`, in particular positive measure. The set of `w`
for which all `q_j + w` are typical points (density-one points of their own colour class) is conull
(Lemma 4.3). Choose `w` in the intersection: then all `q_j + w` are typical points of `U`, so each
carries a colour in `T'`; and for each unit pair of `Q` the two points are typical points at
distance one, so their colours differ (Lemma 4.3). Thus `c` restricted to `Q + w` is a proper
colouring of the unit-distance graph `Q` with colours in `T'`, so `|T'| >= chi(Q)`. `square`

**Remarks.**
1. No palette bound, no self-avoidance, no properness of a label function, no maximality is used.
   The only inputs are Lemmas 4.3 and 5.2(2). In particular Theorem 1 does **not** contradict
   Theorem C of the sprint report (which says that the *palette-level* hypotheses admit these
   models); it says something different and stronger: a *density-transfer* consequence of being a
   colouring's palette field already excludes them.
2. Any `Q` may be used. `chi(Q) = 3` (unit triangle) is the paper's Lemma 6.4; `chi(Q) = 4`
   (Moser spindle) and `chi(Q) = 5` (a 5-chromatic unit-distance graph, e.g. de Grey's or
   Heule's) are stronger rules, available when `Z` is fat enough.
3. Because `Z <= {|z - x| <= 2}`, only unit-distance graphs of diameter at most 4 can ever appear,
   and by de Bruijn-Erdos `chi(Q)` is at most `chi(R^2)`. The power of the mechanism is therefore
   tied to the chromatic number of the plane; §3 makes the arithmetic exact.

**Corollary 2 (k-arithmetic).** In the notation of Theorem 1, a contradiction follows whenever

```
        k - |G_1 u G_2|  <  chi(Q)     for some finite unit-distance graph Q <= Z.
```

The content at `k = 6`:

| `|G_1 u G_2|` | `|T'|` | a contradiction needs |
|---|---|---|
| 6 | 0 | nothing: (5.2) alone |
| 5 | 1 | a single unit edge (`chi = 2`) |
| 4 | 2 | a unit triangle (`chi = 3`) — the paper's Lemma 6.4 geometry |
| 3 | 3 | the Moser spindle (`chi = 4`) |
| 2 | 4 | a 5-chromatic unit-distance graph (`chi = 5`) |

---

## 3. Theorem 2 (the gamma criterion, exactly decided)

Write `kappa = pi/3`, `gamma = 2 arcsin(1/(2 sqrt 3))`, `psi = pi + gamma`.

**Theorem 2.** In the notation of Theorem 1 suppose there is `t in S` with

```
        e^{i(t+2j kappa)} in E_1^*   and   e^{i(t+psi+2j kappa)} in E_2^*     for j = 0,1,2,
```

or the same with `E_1, E_2` interchanged. Then `Z` contains a unit equilateral triangle, hence
`|I \ (G_1 u G_2)| >= 3` by Theorem 1.

*Proof.* Put `a_j = e^{i(t+2j kappa)}`, `b_j = e^{i psi} a_j = e^{i(t+pi+gamma+2j kappa)}` and
`z_j = x + a_j + b_j`. Then `a_j in E_1^*`, `b_j in E_2^*`, `a_j` and `b_j` are nonparallel
(`gamma/pi` irrational), so `z_j in Z`; and
`z_j - x = a_j (1 + e^{i(pi+gamma)}) = a_j (1 - e^{i gamma})`, so
`z_{j+1} - z_j = e^{i(t+2j kappa)} (e^{2 i kappa} - 1)(1 - e^{i gamma})` and
`|z_{j+1} - z_j| = |e^{2i kappa}-1| * |1 - e^{i gamma}| = sqrt(3) * (1/sqrt 3) = 1`. Also
`z_3 = z_0`. So `{z_0,z_1,z_2}` is a unit equilateral triangle in `Z`. `square`

This is the paper's Lemma 6.4 triangle; the statement above differs from the printed one in two
respects that matter for applications: (i) the roles of `G_1, G_2` are interchangeable (Lemma 6.4
is stated for a 2-valued state and does not display the swap), and (ii) no invariance of a palette
*state* is assumed — only membership of three explicit directions in each of the two direction
sets. Point (i) is responsible for every elimination below: without the swap the block fields
survive, with it they die.

**Decision procedure.** Since `E_j` here are finite unions of rational arcs (degrees), the
existence of `t` is decided by exact interval algebra: with `[psi_lo,psi_hi]` a rational enclosure
of `psi` (`width < 1e-40` degrees, computed by bisection on `cos psi = -5/6` in `verify.py` and
independently from the arcsin series in `verify_indep.py`),

```
   witness set = ( E_1 cap (E_1 - 120) cap (E_1 - 240) )  cap
                 ( (E_2 - psi) cap (E_2 - psi - 120) cap (E_2 - psi - 240) )
```

(union with the swapped expression), intersected as unions of rational intervals modulo 360. A
nonempty intersection yields a rational witness `t`, which is then re-checked pointwise for the
whole enclosure `[psi_lo, psi_hi]`.

---

## 4. Theorem 3 (elimination of the pair-valued palette-level countermodels)

The models (verbatim from the sprint record):

* `m15` uniform block field, `ell = 3,4,5,6`
  (`sprint/k6/REPORT.md` Theorem C, `.ultramath/smwfo9zkl/m15/`):
  `P_z(e^{i theta}) = M_{floor( floor(theta/Delta) / L ) mod 3}` with `Delta = 2 pi/(6m)`,
  `L = 2m/3`, `m >= 6` divisible by 3 (`m = 6` was used). For every `m` the blocks are
  `[40 j, 40(j+1)) + 120 k` degrees, so all these fields have the **same** direction sets;
  the computation below therefore covers the whole family, not one member.
* `FREE-LABEL`, `ell = 3,4,5` (same blocks) and `ell = 6` (the 36-sector word of
  `sprint/k6/FREE-LABEL.md`; note it is **not** 120-degree periodic — one entry differs — so no
  reduction modulo 120 degrees may be used).
* `m13` singleton triangle field (`s = floor(9t/2 pi) mod 3`, palettes `{4+s(t)}`).

**Theorem 3.** Of these nine fields, seven are not the maximal palette field of any weak measurable
6-colouring. The two that survive are exactly the singleton-valued ones.

The certificate for each eliminated model is a pair of palette values `A, B` with `A cap B = empty`,
positive-measure direction sets, **and** a direction `t` with the six membership conditions of
Theorem 2 — so `|I \ (A u B)| >= 3`; while `|A u B| >= 4` in every listed case, a contradiction.

`verify.py` (exact rational interval algebra, §C) and `verify_indep.py` (the fields rebuilt as
functions of the angle, a scan over `t`, membership tested at both ends of the `psi` enclosure,
`gamma` from the arcsin series instead of the cosine bisection) agree on every entry:

```
model                        values  120-periodic  verdict     witness
m15 uniform blocks, ell=3      3        yes        ELIMINATED  A={0,3} B={1,4}: t = 53.221345 deg (role B->A), |AuB|=4
m15 uniform blocks, ell=4      3        yes        ELIMINATED  A={0,2} B={1,4}: t = 53.221345 deg (role B->A), |AuB|=4
m15 uniform blocks, ell=5      3        yes        ELIMINATED  A={0,2} B={1,3}: t = 53.221345 deg (role B->A), |AuB|=4
m15 uniform blocks, ell=6      3        yes        ELIMINATED  A={0,3} B={1,4}: t = 53.221345 deg (role B->A), |AuB|=4
FREE-LABEL, ell=3              3        yes        survives    (singletons: |AuB| = 2, |T'| = 4 >= 3)
FREE-LABEL, ell=4              3        yes        ELIMINATED  A={0,2} B={1,3}: t = 53.221345 deg (role B->A), |AuB|=4
FREE-LABEL, ell=5              3        yes        ELIMINATED  A={0,2} B={1,3}: t = 53.221345 deg (role B->A), |AuB|=4
FREE-LABEL, ell=6              6        no         ELIMINATED  A={1,3} B={2,4}: t = 93.221345 deg (role A->B), |AuB|=4
m13 singleton triangle         3        yes        survives    (singletons: |AuB| = 2, |T'| = 4 >= 3)
```

In each eliminated row the valid `t` form a union of arcs of total length at least `19` degrees
(`79` degrees for the periodic blocks; the shortest single arc used is `6.44` degrees long), and
every witness lies more than `3.2` degrees inside its arc, so no conclusion is a boundary case.
The `t` tabulated is the midpoint of the widest arc; both scripts also *verify* their witness
pointwise, for the whole `psi` enclosure.

One item relevant to the sprint's direction 2: the coordinator's lead (i) there is the four-cycle
block model (values `{0,2},{1,3},{4}`, accumulating). Its pair-valued part is exactly the `ell = 4`
row above, so that four-cycle palette-level countermodel is not colouring-realizable either; the
four-cycle case itself remains open (its singleton-outsider configurations are not touched).

Two remarks on the record.
* `sprint/k6/FREE-LABEL.md` states "The only constraint that removes these models is **properness**
  of the colouring". By Theorem 3 this is false for six of its seven constructions (and for all
  four `m15` block fields). Neither properness, nor trace-consistency, nor maximality of the palette
  field is used: Lemma 5.2(2) suffices.
* The distinction the sprint drew — palette-level hypotheses vs. colouring-level input — is still
  correct and Theorem C still stands. The point is that Lemma 5.2(2) is *not* a palette-level
  hypothesis; it is a density statement about the colouring, and it is much cheaper to use than
  properness of a label function.

---

## 5. Consequence for the six-cycle case (the new necessary condition)

**Corollary 3.** Let `k = 6`, let `x` be a centre whose `Gamma_x` contains a cycle meeting every
label (in particular a six-cycle centre), and let `A != B` be palette values with `A cap B = empty`
carried on direction sets `E_A, E_B` of positive measure (these exist at every centre satisfying
(5.7): `P(f) cap P(Rf) = empty` a.e. forces a disjoint pair on positive measure). Then no `t`
satisfies the hypothesis of Theorem 2 for the pair `(A,B)`. Equivalently:

```
   ( E_A cap (E_A - 120) cap (E_A - 240) )  cap  ( (E_B - psi) cap (E_B - psi - 120) cap (E_B - psi - 240) )  =  empty
```

and the same with `A, B` interchanged.

*Proof.* At such a centre every palette has at least two labels (Lemma 3 of `STRUCTURE.md`, §1
above), so `|A u B| >= 4` and `|T'| <= 2 < 3 = chi(triangle)`; Theorem 2 would give `|T'| >= 3`.
`square`

So a six-cycle countermodel at `k = 6` must be **gamma-avoiding**: for every disjoint pair of
values, the two direction sets must not carry the two 120-degree orbits in the `psi`-shifted
position. All six-cycle palettes-level models in the sprint record violate this (rows 4 and 8 of the
table), and there is no six-cycle model left in the record.

---

## 5b. A further exact constraint: ternary palettes are fragmented at scale `gamma`

The `|G_1 u G_2| = 5` row of Corollary 2 needs only a **unit edge**, and at a six-cycle centre the
sixty-degree exclusion supplies a whole family of them. Recall `kappa = pi/3` and
`gamma = 2 arcsin(1/(2 sqrt 3))`.

**Theorem 5 (ternary successor).** Let `k = 6` and let `x` be a centre whose `Gamma_x` contains a
cycle meeting every label (so every palette has at least two labels). Let `T` be a palette value
with `|T| = 3`, carried on a direction set `E_T` of positive measure, let `V` be a palette value
with `|V| = 2` and `V cap T = empty`, and put `E = {a in E_T : P_x(Ra) = V}`. Then for every arc
`I` of length `>= gamma` (`gamma = 33.5573...` degrees) one has `sigma(E cap I) < sigma(I)`; that
is, no arc of length `gamma` is contained in `E` up to a null set.

*Proof.* (i) For a.e. `a in E_T`, (5.7) gives `P_x(Ra) cap T = empty`, so `P_x(Ra)` is a pair or
triple inside `T^c := [6] \ T`. A triple into `T^c` must equal `T^c`, and two complementary triples
cannot both occur on positive-measure direction sets: if `P = T` on `E_1` and `P = T^c` on `E_2`,
both of positive measure, then `P(e) u P(v) = [6]` for a.e. nonparallel `(e,v) in E_1 x E_2`, which
contradicts (5.2) on a product set of positive measure. Hence for a.e. `a in E_T` the palette
`P_x(Ra)` is a pair inside `T^c`; in particular `E` is the union of at most three such pieces.
(ii) Now let `a in E`; then `Ra in E_V`, so
`z(a) := e^{ia} + e^{iRa} = e^{ia}(1 + e^{i kappa}) = sqrt(3) e^{i(a + 30 deg)}` lies in the sum
set `E_T + E_V`. Two such points at angular separation `gamma` have distance
`2 sqrt(3) sin(gamma/2) = 2 sqrt(3) * 1/(2 sqrt 3) = 1`. So if `E` contains an arc of length
`>= gamma`, the sum set contains a unit edge. (iii) But `|T u V| = 3 + 2 = 5`, so
`|I \ (T u V)| = 1 < 2 = chi(unit edge)`, and Theorem 1 gives a contradiction. `square`

**Consistency.** In the `FREE-LABEL, ell = 6` word the only ternary value is `{2,4,5}` and it sits
on a single `10`-degree sector, with `R`-successor `{1,3}` (the pair inside its complement
`{0,1,3}`); `10 < 33.557` — the model is consistent with Theorem 5, and only just. In the `m15`
block fields there are no ternary values at all. `work/ternary.py` prints the check.

**What Theorem 5 does not do.** It bounds the ternary stratum, not the pair stratum: if every
palette at a six-cycle centre is a pair, the mechanism's cheapest contradiction needs a unit
triangle (`|G_1 u G_2| = 4`), and the pair stratum is where the open problem lives.

---

## 6. What the mechanism does *not* do (sharpness and limits)

**(a) It is strictly stronger than the gamma criterion — rigorously.** Let `E_1 = (0,120)`,
`E_2 = (120,240)` (degrees). Neither contains a 120-degree orbit, so Theorem 2 is silent; yet
`E_1 + E_2` contains a disc of radius `0.717 > 1/sqrt 3` and hence a unit triangle
(`verify.py` §D, `verify_indep.py` last block). The lemma used:

**Theorem 4 (arc-sum lemma).** Let `I = (theta_0 - delta, theta_0 + delta)`,
`J = (phi_0 - delta, phi_0 + delta)`, put `psi = phi_0 - theta_0` and `sigma = 2|sin(psi/2)|`. Then

```
   Phi(I x J)  contains the disc  B( Phi(theta_0,phi_0) , delta*sigma - delta^2 ) ,
   Phi(theta,phi) = e^{i theta} + e^{i phi} .
```

*Proof.* `Phi(theta_0+u, phi_0+v) = Phi(theta_0,phi_0) + i e^{i theta_0} u + i e^{i phi_0} v +
R(u,v)` with `|R| <= (u^2+v^2)/2` (Taylor remainder of the exponential). The two columns
`i e^{i theta_0}`, `i e^{i phi_0}` are unit vectors at angle `psi`, so the linear map has singular
values `2|cos(psi/2)|` and `2|sin(psi/2)| = sigma`; the image of the square `[-delta,delta]^2`
contains the disc of radius `delta*sigma`. Adding the remainder loses at most `delta^2`. `square`

Since every disc of radius `r >= 1/sqrt 3` contains a unit equilateral triangle (circumradius
`1/sqrt 3`), Theorem 1 gives `|T'| >= 3` whenever two arcs of the direction sets satisfy
`delta*sigma - delta^2 >= 1/sqrt 3`.

**(b) It reaches beyond the gamma criterion in practice too.** The field

```
   sectors 0..35 of 10 degrees, palettes
   [1,4] [1,2,4] [2,4] [1,4] [1,3,4] [1,3,5] [2,3,5] [3,5] [3,5] [2,5] [2,5] [2,4]
   [1,4] [2,4] [1,4] [1,3,4] [1,3,4] [1,3,5] [2,5] [3,5] [2,3,5] [2,5] [2,5] [2,4]
   [1,3] [1,4] [1,4] [1,3,4] [1,4] [1,5] [2,5] [3,5] [3,5] [2,5] [2,5] [2,4]
```

is gamma-avoiding (checked for all disjoint pairs, exactly), satisfies (5.7) and every palette is
admissible for the six-cycle and avoids the centre colour `0` — yet it is also dead: for the values
`{1,4}`, `{2,5}` the sum set contains the exact unit triangle
`{c, c+u, c+u e^{i pi/3}}` with `c = (-27/50, -1/50)`, `u = e^{i 326 deg}`, whose three vertices
have membership margins `2.20, 2.36, 3.39` degrees (`work/marg2.py`; membership angles evaluated at
50 digits by Lemma 5.2(2)'s decomposition `e^{i theta} = w/2 +- i w sqrt(4-|w|^2)/(2r)`). This
certificate is margin-based rather than algebraic and is labelled as such.

**(c) It does not decide the six-cycle case.** Theorem 1 leaves alive every palette field in which
every disjoint-value sum set is unit-triangle-free. A field with each value confined to short
scattered arcs is of that type (the sum of two short arcs has diameter at most the sum of the
diameters), and such fields satisfy the palette axioms and (5.7). So the open `k = 6` problem is not
settled here; what is settled is that no argument is needed beyond Lemma 5.2(2) to kill the
sprint's palette-level countermodels, and the exact condition a surviving countermodel must meet is
Corollary 3 plus "every disjoint-value sum is triangle-free".

**(d) Consistency (vacuity tests).** (i) The two surviving rows of Theorem 3 have `|A u B| = 2`, so
`|T'| = 4 >= 3`: the criterion fires but the arithmetic gives no contradiction — the mechanism is
not vacuously true. (ii) At `k = 5` the paper's own use is the row `|G_1 u G_2| = k - 2 = 3`,
`|T'| = 2 < 3` — consistent with the table of Corollary 2. (iii) A genuine 6-colouring with cyclic
centres exists (`m7`'s Theorem 5 strip colouring, four-cycle centres, singleton outsider palettes):
its disjoint value pairs have `|A u B| = 2`, so nothing in Theorem 1 contradicts it.

---

## 7. Files, commands, verification status

```
   python3 verify.py          # exact rational arithmetic; ~4 s;  writes nothing
   python3 verify_indep.py    # independent implementation; ~70 s
```
`verify.py` prints: exact constants (§A), the k-arithmetic (§B), the elimination table with witness
intervals and widths (§C), the strict-strength disc computation (§D).
`verify_indep.py` prints its own `gamma` derivation, its own reconstruction of the nine fields and
the same verdicts, plus the disc bound. Both scripts end with the same nine-row verdict list
(7 eliminated, 2 survivors).

Auxiliary scripts used during the work (not needed to reproduce the theorem):
`work/orbit_crit.py` (exact orbit criterion), `work/scan4.py` (numerical triangle search in sum
sets), `work/marg2.py` (the fragmented-field certificate), `work/avoid.py` (the gamma-avoiding
field), `work/pages/` (150 dpi renders of pp. 27, 28, 37).

**Status of each claim.** Theorem 1: proved above from Lemma 4.3 + Lemma 5.2(2) (no machine check;
the argument is the paper's own Lemma 6.4 argument with `Q` in place of the triangle). Theorem 2:
proved. Theorem 3: exact computation, two independent implementations. Theorem 4: proved.
Corollary 3: proved. §6(b) is a margin-based certificate, not an algebraic identity — labelled.
