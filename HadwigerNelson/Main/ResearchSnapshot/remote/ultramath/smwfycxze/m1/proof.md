# The k = 6 triangle gate: exclusion capacity 2, and what that does and does not settle

Member `m1`, swarm `smwfycxze`, direction `d2` (geometric/tameness side, restated in §0).
Verifier: `verify.py` in this directory — `python3 verify.py`, 58 checks, exit status 0.
All decisions exact (rationals; `Q(sqrt3, sqrt11, sqrt33)` with two independent sign
procedures); everything numerical that is not a decision is labelled as such.

---

## 0. What this note delivers, and why it is in this direction

The swarm's target is **(W)**: *some ball of radius `> 1` meets `L` in finitely many points*
(`L = {x : Gamma_x has a cycle}`), because §7 transfers at `k = 6` under exactly (W)
(`sprint/k6/REPORT.md` Theorem A). Two inputs were declared live: the `k = 6` exclusion side of
§8, and (W) inside the a.e.-singleton class `S_1`.

This note works on the **mechanism** of §8's last case (§8.4–§8.5, the triangle), which is the
one case that reduces to a *single-centre* computation and can therefore be pinned down
exactly. Three deliverables:

| § | statement | kind |
|---|---|---|
| 2–4 | **Theorem 2 / Corollary 3** ((5.2) exclusion capacity): at one centre the paper's two-term sum exclusion can exclude **at most two** labels from the colour of a point, for every `k`. So the §8.5 mechanism — which must exclude the `k-3` outsiders — works **exactly for `k <= 5`**, and at `k = 6` it is exactly one label short. Sharp; and the only other single-centre rule (Lemma 6.3, a *forcing* rule) needs palette groups of total size `k-1`, which is unavailable at a singleton-palette triangle centre at `k = 6` | theorem (no-go with exact bound) |
| 5–6 | **Theorem 4** (calibration at `k = 5`): the set of `z` at which *both* outsiders are excluded is **exactly** the paper's region (8.4), and the seven placed Moser vertices lie strictly inside it — re-verified exactly, two procedures. Also a parenthesisation **erratum** in (8.6): the displayed formula does not verify its own Table 1 | decided computation + calibration |
| 7–9 | **Theorem 5 / Theorem 6** (`S_1`, `k = 6`): the complete one-centre picture at a triangle centre (the outer strip is `O`-valued and its colour is *determined* by the exclusion pair; the inner strip is 2-valued; a 3-valued centre must be coloured by its own triangle labels and has no unit-distance partner), hence **(W) in `S_1` at `k = 6` is equivalent to "the 3-valued triangle locus is finite in one ball of radius `> 1`"**, plus **Proposition 8**: no finite unit-distance gadget can supply the missing label (the paper's 3-colourable annulus forbids every "3-colour local-constancy" gadget). The exact missing statement `(S)` is isolated | theorem + no-go |

**What is NOT claimed.** I do not decide (W), and I do not decide the `k = 6` triangle locus.
§11 lists the non-claims. §10 explains why the direction I registered (weaken m3's tameness
hypothesis and prove (W) for the enlarged class at `k = 6`) cannot succeed as stated: every
non-tame accumulation at `k = 6` needs a unit circle carrying only three labels, i.e. it needs a
6-colouring — the chromatic wall — so that route is not a route to (W) but a restatement of the
`k = 6` problem. What survives of it is §10.

---

## 1. Setting and cited facts

`c` is a weak measurable `k`-colouring of `R^2` (Definition 1.2); `A_i = c^{-1}(i)`;
`H_i` its closed spatial essential support; `P_x(e)` the maximal palette at the centre `x` in
direction `e` (Definition 5.1); `R` rotation of directions by `kappa = pi/3`; `Gamma_x` the
transition graph (Definition 6.1); `L = {x : Gamma_x contains a cycle}`; a point is *typical* if
it has density one of its own colour.

Cited verbatim (no re-derivation):

* **(5.2)** for a.e. independent-angle pair `(e,v)`: `c(x+e+v) notin P_x(e) union P_x(v)`
  (Lemma 5.2(1)).
* **(5.3)** Lemma 5.2(3) with the trivial representation of Remark 5.3.
* **(5.7)** `P_x(e) inter P_x(Re) = empty` a.e. (Corollary 5.4).
* **Lemma 5.5** (binary-centre separation: centres *binary for a fixed pair*, i.e. with
  `P_x(e) inter {i_+,i_-} != empty` a.e., are `delta_*`-separated, `delta_* > 0` absolute).
* **Lemma 6.2 / (6.2)**: `ij in Gamma_x` implies `P_x(e)` is not contained in `{i,j}` a.e.
* **Lemma 8.1** (one-sided strips) and the definition of `O(e)`, `I(e)` (§8.1).
* **Lemma D** (self-avoidance, `sprint/k6/REPORT.md` §5): if `x` is typical and `c(x) = i` then
  `i notin P_x(e)` for a.e. `e`.
* **m4** (`.ultramath/smwfwi7rh/m4/NOTE.md`): Theorem 1 (unit-separation transport), Theorem 3
  (`S_1` at `k = 6`: no 5- or 6-cycle; the 4-cycle locus is locally finite), Proposition 5 (the
  thin annulus is properly 3-colourable).
* `L` is closed and `1`-dense (`sprint/k6/REPORT.md` Theorem B).

`S_1` is the class of weak measurable `k`-colourings such that for **every** centre `x`,
`P_x(e)` is a singleton for a.e. `e`.

---

## 2. Lemma 1 (unique unit decomposition)

> **Lemma 1.** Let `z in R^2`.
> (i) If `0 < |z| < 2` the solutions of `s + t = z`, `|s| = |t| = 1`, are exactly
> `(s_+, t_+)` and `(t_+, s_+)` where `s_+ = z/2 + i (z/|z|) sqrt(1 - |z|^2/4)`,
> `t_+ = z/2 - i (z/|z|) sqrt(1 - |z|^2/4)`. In particular the **unordered** pair is unique.
> (ii) If `|z| = 2` there is exactly one solution, `s = t = z/2`.
> (iii) If `|z| > 2` there is none.
> (iv) If `z = 0` the solutions are `(s, -s)` for every `s in S` — a one-parameter family.

*Proof.* `|z - s| = |t| = 1` together with `|s| = 1` gives
`|z|^2 - 2 <z,s> + 1 = 1`, i.e. `<z,s> = |z|^2/2`. So `s` ranges over `S inter L` where `L` is
the line `<z, s> = |z|^2/2`, whose distance from the origin is `|z|/2`. A line at distance `< 1`
from the origin meets `S` in exactly two points, at distance `= 1` in one, at distance `> 1` in
none. Writing `s = z/2 + w` with `w perp z` and `|w|^2 = 1 - |z|^2/4` gives the displayed form;
`t = z - s`. (iv) is immediate. `square`

`verify.py` block A checks `|s_+| = 1` as the exact rational identity
`r^2 (1/4 + (1/r^2 - 1/4)) = 1`, the symmetry `s_+ + s_- = z`, and the strict cases.

**Remark.** Lemma 1(iv) is exactly why self-avoidance (Lemma D) is *not* an instance of the
sum exclusion: at `z = 0` the decomposition is not rigid, the map `(e,v) -> e+v` is not a
submersion there, and no exclusion follows from (5.2). This single degeneracy is what separates
"the colour of the centre" from "the colour of every other point".

---

## 3. Theorem 2 (the two-term exclusion at one centre)

> **Theorem 2.** Let `c` be a weak measurable `k`-colouring and `x in R^2`. Then for a.e.
> `z` with `0 < |z| < 2`, with `{e_z, f_z}` the unique unit decomposition of `z` (Lemma 1),
> `c(x + z) notin P_x(e_z) union P_x(f_z)`.
> Equivalently: **the two-term sum exclusion at a single centre excludes at most two palette
> values at any point `x + z != x` with `|z| < 2`, and nothing at all for `|z| > 2`.**

*Proof.* Let `Phi : S x S -> B(0,2)`, `Phi(e,v) = e+v`. Off the set `{e = +-v}` (a union of two
circles in the torus, hence `sigma x sigma`-null) `Phi` is a smooth submersion: in angular
coordinates its differential is `[Je, Jv]`, of determinant `|e x v|`, which vanishes exactly on
`e = +-v`. For `z` with `0 < |z| < 2` the fibre is the two points `(e_z,f_z)`, `(f_z,e_z)` of
Lemma 1, and at each of them `|e x v|^2 = |z|^2 (1 - |z|^2/4) > 0`. Consequently the pushforward
`Phi_*(sigma x sigma)` is, on `B(0,2) \ {0}`, absolutely continuous with respect to Lebesgue
measure with density `2 / (|z| sqrt(1 - |z|^2/4)) > 0` (change of variables for a two-to-one
proper submersion). Pulling the `sigma x sigma`-null exceptional set of (5.2) back through `Phi`
therefore gives a Lebesgue-null set of `z`, and (5.2) holds at both preimages. The angular null
sets inside `P_x` need no separate treatment, the right-hand side being a union of two palettes.
`square`

(Theorem 2 is, in effect, the exact content of the paper's change-of-variables step in the proof
of Lemma 8.8, "change of variables transports the product-null exceptions to a spatial null set",
isolated as a statement about one centre. The novelty is not the step but the count it gives; see
Corollary 3.)

---

## 4. Corollary 3 (the (5.2) exclusion capacity is 2, and the exact `k`-threshold)

> **Corollary 3.** Fix a centre `x`. For every `z` with `0 < |z| < 2` the two-term sum exclusion
> (5.2) at `x` excludes at most **two** labels from `c(x+z)`, and it is the only exclusion rule
> available at one centre that has this form. Consequently the step of §8.5 that produces the
> three-label region — which at a triangle centre must exclude all `k - 3` outsiders at a point —
> is available exactly when `k - 3 <= 2`, i.e. **for `k <= 5`**; at `k = 6` it is exactly one
> label short, and no refinement of the (5.2) data at `x` repairs it.

*Proof.* By Theorem 2 the labels excluded at `x + z` (`z != 0`) by (5.2) are the at most two
members of `P_x(e_z) union P_x(f_z)`; by Lemma 1 there is no other unit decomposition of `z`. The
other single-centre rules produce no exclusion of this form at `x + z`: (5.7) is the special case
`|z| = 1` of (5.2); (6.2) constrains `P_x` itself; Lemma D constrains `c(x)`. At `z = 0`
Lemma 1(iv) makes the decomposition non-rigid — the sum map is not a submersion there — and the
only surviving statement is Lemma D, which concerns `c(x)`, not `c(x+z)`.

The `k`-dependence is then arithmetic: at a triangle centre of a weak measurable `k`-colouring the
labels outside the triangle number `k - 3`. For `k = 5` this is `2` and the mechanism excludes
both (this is exactly the paper's §8.5, see Theorem 4). For `k = 6` it is `3`, and at least one
outsider survives at every point at distance `(0,2)` from `x`. `square`

**Scope, stated exactly (the one other single-centre rule).** The paper's Lemma 6.3 is a second
single-centre rule and it *forces* rather than excludes: two states at `x` representing disjoint
label groups whose union is `[k] \ {X}` force `X` at the sum of a nonparallel pair, i.e. they
exclude `k-1` labels at once. That rule needs palette groups of total size `k-1`. In `S_1` every
palette is a singleton, so the two groups have total size `2`; at `k = 6` that is `2 < 5`, so
Lemma 6.3 is unavailable at a triangle centre in `S_1` and Corollary 3 is the whole single-centre
content there. (Outside `S_1`, at `k = 6`, Lemma 6.3 does apply to state pairs of sizes `3 + 2`;
I do not claim anything against it, and §8.5 does not use it.)

**Sharpness (checked, `verify.py` block D).** The bound is attained and not vacuous: for both
recorded 3-valued singleton fields (equal thirds, and `m13`'s `floor(9t/2pi) mod 3`), the
exclusion set has size `2` at 2/3 of sampled positions and size `1` at the rest, never `3`, and
every one of the three values survives as the unexcluded label somewhere. So the third outsider
is genuinely available at `k = 6`; the mechanism does not merely fail to be sharp, it is
structurally unable to reach it.

**Why this is not a restatement of a known dead end.** The recorded dead ends are results about
*satisfiability* of palette systems (`m6`, `m14`, `m15`, `m13`) or about *size* conditions on `L`
(`m5`). Corollary 3 is neither: it is a bound on how many labels one centre can pin down at one
point, it is unconditional, it holds for every `k` and every colouring, and it explains the
`k = 5 / k = 6` transition as an instance of the arithmetic `k - 3 <= 2`. It also predicts, for
every cycle length, that the *last* step of any §8 case based on the sum exclusion cannot be
carried out at `k >= 6`.

**Direction note (§0).** The direction I registered was: weaken m3's tameness hypothesis
(allow accumulating interfaces) and prove (W) at `k = 6` for the enlarged class. That cannot work
as stated, for a reason worth recording: by m3's Corollary 4 / m4's §5, a `k = 6` colouring whose
cyclic locus is not locally finite must contain a Mercedes gadget, hence a point whose unit circle
carries at most three labels; and by the count of Corollary 3 that is precisely what a
`k = 6` failure needs. So "non-tame at `k = 6`" and "the chromatic wall" are the same condition,
and an enlarged tameness class big enough to contain a potential countermodel is already the whole
problem. I therefore record the direction as abandoned in that form and deliver instead the exact
mechanism bound and the reduction of §7–§9.

---

## 5. Theorem 4 (`k = 5` calibration: the mechanism reproduces §8.5 exactly)

> **Theorem 4.** Work at `k = 5` at a triangle centre `x` with triangle labels `{0,1,2}` and
> outsiders `{X,Y}`, in the situation of the paper's §8.4 (binary outsider state `s`, locally
> essentially constant, essential boundary one `R`-orbit; Lemma 8.6–8.7). For `z = r e^{i phi}`,
> `0 < r < 2`, put `delta = arccos(r/2)`. Then the two labels excluded at `x + z` by Theorem 2 are
> `s(phi - delta)` and `s(phi + delta)`, and they are **distinct if and only if**
> `sin^2(3 phi) < sin^2(3 delta)`, which is **exactly the paper's region (8.4)**
> `ups^2 (3 xi^2 - ups^2)^2 < l^3 (1 - l/4)(l - 1)^2` (`z = xi + i ups`, `l = |z|^2`).
> Hence the set on which §8.5's three-labelled region lives is exactly (8.4), and on it
> `c(x+z) in {0,1,2}`.

*Proof.* (a) Lemma 1 gives the decomposition directions `phi +- delta` with `delta = arccos(r/2)`
(the pair of points `e^{i(phi +- delta)}` sums to `2 cos(delta) e^{i phi} = r e^{i phi}`); their
palette values are `s(phi +- delta)`.

(b) By Lemma 8.7 the state is `s(e^{i theta}) = X` iff `sin(3 theta) > 0` (up to exchanging
`X, Y`), because its essential boundary is one `R`-orbit and it alternates. So the two values are
distinct iff `sin(3(phi - delta)) sin(3(phi + delta)) < 0`, and by
`sin(A - B) sin(A + B) = sin^2 A - sin^2 B` this is `sin^2(3 phi) < sin^2(3 delta)`.

(c) The two trigonometric conversions to the algebraic form are exactly the paper's:
`sin^2(3 phi) = ups^2 (3 xi^2 - ups^2)^2 / l^3`, and `sin(3 delta) = s (4 cos^2 delta - 1) =
sqrt(1 - l/4) (l - 1)` with `s = sin delta`, `cos delta = r/2`, `l = r^2`. Both are checked
symbolically in `verify.py` block B. So "distinct" `= (8.4)`, which is open, and on it both
outsiders are excluded, leaving the three triangle labels. `square`

**The certificate (`verify.py` block C).** The seven placed Moser vertices of (8.5)–(8.6) satisfy
`0 < |z_g|^2 < 4` and (8.4) **strictly**, decided in `Q(sqrt3, sqrt11, sqrt33)` with two
independent sign procedures (rigorous rational interval arithmetic; exact field arithmetic with
nested rational brackets of `sqrt3` from bisection on squares and of `sqrt11` from its continued
fraction). The eleven drawn unit edges and the contradiction edge `|T - uT| = 1` are re-verified
exactly. This reproduces the paper's Lemma 8.9 and Proposition 8.10 from my mechanism, which is
the required calibration: at `k = 5` the count of Corollary 3 is exactly `k - 3`.

**Erratum (found while calibrating).** The displayed (8.6) of the paper reads
`z_g = ((35+12i)/37) g + (-290+149i)/250`, but the paper's Table 1 corresponds to
`z_g = ((35+12i)/37) (g + (-290+149i)/250)` — the translation is applied *before* the rotation.
The two placements differ by a rotation of the translation vector (the multiplier has norm one),
and the region (8.4) is not rotation-invariant, so this is not cosmetic: with the literal
parenthesisation the vertex `g = 0` is at `(-1.16, 0.596)`, where `P > P'`, i.e. (8.4) **fails**
(`verify.py` check `C6`), whereas Table 1 lists `(-1.2906, 0.1876)`, which is the other
placement and does satisfy it. The mathematical conclusion of §8.5 is unaffected — the second
placement is a legitimate unit-distance embedding of the Moser graph and the certificate is valid
for it — but the displayed formula and its own table disagree.

---

## 6. Theorem 5 (the complete one-centre picture at a triangle centre in `S_1`, `k = 6`)

Throughout: `k = 6`, `c in S_1`, `T = {i_0,i_1,i_2} ⊂ [6]` a triangle, `O = [6] \ T` the three
outsiders, and `x` a **type-`T` triangle centre**: `T` spans a `K_3` in `Gamma_x`. Write
`P_x(e) = {b_x(e)}` (so `b_x : S -> [6]` is measurable) and `V_x = {b in O : sigma{b_x = b} > 0}`.

> **Theorem 5.** In the situation above:
> **(a)** `b_x(e) in O` for a.e. `e`; and `P_x(e) = {c(x+e)}` for a.e. `e` (the endpoint trace
> `c(x+e) in P_x(e)` holds for every fixed centre, `m10` Lemma 1; with a singleton palette it
> gives equality), so the palette at `x` *is* the colouring of the unit circle about `x`.
> **(b)** `|V_x| >= 1`, and `sigma{b_x = b} <= 1/2` for every `b in O` (m11's bound).
> **(c)** ('outer strip is `O`-valued, identically in the direction') For a.e. direction `f` there
> is `eta(f) > 0` such that `c in O` a.e. on the outer strip
> `{x + r e^{i theta} : theta near f, 1 < r < 1 + eta(f)}`.
> **(d)** ('the survivor is determined') On the outer strip, at a.e. `z` with `0 < |z| < 2` whose
> two decomposition values are **distinct**, `c(x + z)` equals the *third* outsider `b_3(z)`
> — the one label of `O` not excluded.
> **(e)** ('the inner strip is two-valued') If exactly one of the three edge signs at `e` is
> negative, let `m(e) in T` be its middle label; then `I(e) = O union {m(e)}`, and at a.e. `z` in
> the inner strip with that sign pattern and distinct decomposition values,
> `c(x+z) in {b_3(z), m(e)}`. If all three signs agree, `I(e) = [6]` and the conclusion is only
> `c(x+z) in {b_3(z)} union T`.
> **(f)** (self-avoidance) `c(x) != b` for every `b in V_x`; in particular if `|V_x| = 3` then
> `c(x) in T`.
> **(g)** (no unit-distance partners for a 3-valued centre) If `|V_x| = 3` and `y` is a typical
> type-`T` centre with `|V_y| = 3` and `|x - y| = 1`, then `c(y) in O` (by (a) at `x`) and
> `c(y) in T` (by (f) at `y`), a contradiction. Hence the set of 3-valued type-`T` centres
> contains no unit pair of typical points.
> **(h)** If `|V_x| <= 2` then `x` is **binary for the pair `V_x`** in the sense of §5.3 of the
> paper, hence the set of type-`T` centres with `|V_x| <= 2` is `delta_*`-separated
> (Lemma 5.5), hence locally finite.

*Proof.*
(a) For `ij in Gamma_x`, (6.2) gives `b_x(e) notin {i,j}` a.e.; applying this to the three edges
of the triangle, `b_x(e) notin {i_0,i_1} union {i_1,i_2} union {i_0,i_2} = T`, so `b_x(e) in O`
a.e. The second assertion is the endpoint trace (`m10` Lemma 1): `c(x+e) in P_x(e)` for a.e. `e`
at every fixed centre; with `|P_x(e)| = 1` this is `P_x(e) = {c(x+e)}`.

(b) Nonemptiness of `P_x` a.e. (p. 26 of the paper) gives `|V_x| >= 1`. The bound is m11's
`sigma{T' subset P_x} <= 1/2` applied to the singletons `T' = {b}`.

(c) Lemma 8.1: for `e notin B` there is an angular neighbourhood on which the outer strip uses
only `O(e)`, the labels left after deleting the endpoints of every **positive** edge; and two of
the three signs agree, and those two edges cover all three triangle labels, so `O(e) = O` for
*every* `e notin B` (which is the `k = 6` special feature: `k - 3 = 3` and the outsider set is
exactly what remains). The angular widths and radial widths of Lemma 8.1 are measurable in `e`
and positive a.e., so for a.e. `f` an interval of radii survives; polar-coordinate Fubini gives
the statement a.e. on the strip.

(d) Theorem 2 gives `c(x+z) notin {b_1(z), b_2(z)}`; (c) gives `c(x+z) in O`. If the two are
distinct, `O \ {b_1,b_2}` is the singleton `{b_3}`.

(e) Same, with Lemma 8.1's inner strip. Either the three signs agree — then `I(e) = [6]` and the
inner strip gives no constraint, so `c(x+z) in {b_3(z)} union T` — or exactly one edge is negative,
and its two endpoints are removed, leaving the four-element set `O union {m(e)}`, so
`c(x+z) in {b_3(z), m(e)}` a.e. on a strip piece with that sign pattern.

(f) Lemma D at `x`.

(g) `y = x + e` with `|e| = 1`; by (a) at `x` and typicality of `y`, `c(y) = b_x(e) in O`. By (f)
at `y` (which needs `|V_y| = 3` and typicality), `c(y) in T`. `O inter T = empty`.

(h) `|V_x| <= 2`: if `|V_x| = 1`, `b_x` is essentially a single label `b`, and
`P_x(e) inter {b,b'} != empty` a.e. for any `b' != b`, so `x` is binary for `{b,b'}`. If
`|V_x| = 2`, `V_x = {b,b'}` and `P_x(e) in {{b},{b'}}` a.e., so `P_x(e) inter {b,b'} != empty`
a.e. Either way Lemma 5.5 applies to an explicit pair that depends only on the finite set `V_x`
(it needs no typicality), and `V_x` ranges over the finitely many subsets of `O` of size `<= 2`.
So the set of type-`T` centres with `|V_x| <= 2` is a finite union of `delta_*`-separated sets,
hence locally finite. `square`

**Remark (the first genuine interaction between the palette field and the geometry at `k = 6`).**
By (d) the outer strip has a *determined* colour: `c(x+z) = b_3(z)`. Properness on typical unit
pairs then forces the exclusion *pair* to vary: for a.e. `z, z'` in the outer strip with
`|z - z'| = 1`, the two-element sets `{b_1(z), b_2(z)}` and `{b_1(z'), b_2(z')}` must differ.
Concretely, with `z = r e^{i phi}`, `z' = r e^{i psi}` at the same radius and angular separation
`psi - phi = +- 2 arcsin(1/(2r))` (the unit-distance separation in the annulus), the pair field
`phi |-> {b_x(phi - delta_r), b_x(phi + delta_r)}` with `delta_r = arccos(r/2)` is not allowed to
repeat. So at `k = 6` a 3-valued triangle centre imposes a *functional* condition linking the
palette field at three different angles, beyond (5.7). I have not extracted a contradiction from
it, and the equal-thirds field satisfies it, so it is consistent; I record it because it is the
only constraint in this note in which the strip geometry acts on the circle field.

**Consequence (the reduction).** Combine Theorem 5(h) with m4's Theorem 3 (at `k = 6` in `S_1`
there is no 5- or 6-cycle and the 4-cycle locus is locally finite). Writing
`L_T^{(3)} = {x : Gamma_x contains the triangle T and |V_x| = 3}`, there are 20 triangles and

> **Corollary 5'.** For a weak measurable 6-colouring in `S_1`,
> `L` is locally finite `<=>` `union_T L_T^{(3)}` is locally finite,
> and **(W) `<=>` some ball of radius `> 1` meets `union_T L_T^{(3)}` in finitely many points.**

The second form is the useful one: (W) does not require local finiteness of anything, only that the
accumulation stop somewhere. So the honest target at `k = 6` is not "the triangle locus is
discrete" but "it is not locally infinite everywhere".

---

## 7. Proposition 7 (`(W)` is strictly weaker than local finiteness; a known countermodel does not touch it)

> **Proposition 7.** (i) `not (W)` holds iff `L` is infinite in every ball of radius `> 1`.
> (ii) `m3`'s proper measurable `k >= 7` colouring, whose cyclic locus is
> `V union {q_n, z_n : n in N} union {p_0}` (closed, countable, one accumulation point),
> **satisfies (W)**. So the established failure of local finiteness at `k >= 7` is not a
> failure of (W), and the phase-transition table for local finiteness does not transfer to (W).

*Proof.* (i) is the negation of the definition. (ii): the `q_n, z_n` all lie in a bounded set of
diameter `< 1` around `p_0` (they are the Mercedes centres inside a square of side `1/100`), and
`V` is a lattice, hence locally finite. Take `y` with `dist(y, {p_0}) > 2` and `R = 3/2`; then
`L inter B(y, 3/2)` consists of the finitely many points of `V` in that ball. `square`

**Consequence for the swarm.** By Corollary 5' and Proposition 7, a countermodel to (W) at
`k = 6` must make the 3-valued triangle locus *locally infinite everywhere* — a `1`-dense
accumulation set, not merely one accumulation point. Conversely, a single isolated 3-valued
triangle centre already suffices for (W). This is a strictly easier target than m4's Theorem 3 and
it is the version of the `k = 6` problem that (W) actually asks for.

---

## 8. Proposition 8 (no finite gadget supplies the missing label)

At `k = 6` the natural repair of §8.4's breakdown is: replace the paper's local-constancy path
gadget (Lemma 8.6) by some larger finite unit-distance figure that forces the colour at `p` to
equal the colour at `q` inside the 3-labelled strip. This is impossible.

> **Proposition 8.** Let `A = {q : 1 - eta <= |q| <= 1 + eta}` with `eta = 71/10000`, and let
> `chi` be m4's 3-arc colouring `chi(theta) = floor((theta mod 120^circ)/40^circ)`, which is a
> proper 3-colouring of `A` (m4 Prop. 5). Then there is **no** finite unit-distance graph `W`
> admitting a congruent copy in `A` and two distinct vertices `p, q` of `W` such that every proper
> 3-colouring of `W` gives `c(p) = c(q)`.

*Proof.* Suppose `W` is such. Place `W` by a rotation `R` and translation `t` inside `A`; the set
of admissible `(R,t)` is open. The restriction of `chi` to the placed copy is a proper 3-colouring
of `W`, so `chi(t + R p) = chi(t + R q)` for every admissible `t`, i.e.
`chi(y) = chi(y + h)` for a.e. `y` in a nonempty open set, with `h = R(q - p) != 0`. Applying this
with the rotation `R` and small translations, and then with the roles of `p,q` exchanged and with a
basis of directions, gives essential local constancy of `chi` in every direction, hence (by
connectedness of `A` and a countable subcover) `chi` is essentially constant on `A`. But `A`
contains unit pairs: the points of radius `1` at angular separation `60^circ` are at distance
exactly `1`, and `chi` gives them colours `0` and `1`. Contradiction. `square`

**Checked (`verify.py` block G).** `cos Delta = (r^2 + r'^2 - 1)/(2 r r')` is increasing in each
variable on the box `r, r' in [1 - eta, 1 + eta]`, so its range is the corner range, and exactly
`[0.492824, 0.507025]`, which lies strictly inside `(1/4, 3/4)`; hence `Delta in (40^circ, 80^circ)`
and the three 40-degree arcs give different colours (checked exhaustively on an exact rational
grid). The unit pair at angular separation `60^circ` on radius `1` is exact.

**Sharpness.** The same statement is *false* for two colours: the 4-edge path of Lemma 8.6 forces
equality for 2 colourings (endpoints alternate), which is precisely why §8.4 works at `k = 5`
where the strips are 2-labelled. And it is false for a 3-colouring if one allows *infinitely* many
vertices — the "constancy" is then a limiting statement, not a finite gadget.

**Class and vacuity.** The class is: arguments that derive a label equality at two points of a
3-labelled region from a finite set of unit-distance constraints. The obstruction is not vacuous:
the host `A` is an explicit proper 3-coloured region containing unit pairs, and the 2-colour
analogue (the paper's path) does exist, so the proposition separates the two cases rather than
excluding the whole method. It does not apply to measure-theoretic arguments that use the
colouring at points outside a bounded neighbourhood.

---

## 9. Theorem 6 (conditional: the exact missing statement `(S)`)

The one-centre data at a type-`T` triangle centre `x` with `|V_x| = 3` is, by Theorem 5 and
Corollary 3, exactly one exclusion short of a three-label region. I now name the missing exclusion
precisely. Two points `w`, `z` with `w = x + z`: the only rule that can exclude the label of the
*point itself* rather than of a sum is self-avoidance (Lemma D), and it excludes exactly the labels
carried by the unit circle about that point. So:

> **Definition (S).** For every weak measurable 6-colouring in `S_1`, every triangle `T`, and
> every type-`T` triangle centre `x` with `|V_x| = 3`, there is a nonempty open set
> `U subset {z : 0 < |z| < 2}` such that for a.e. `z in U`: (i) the two unit-decomposition values
> of `z` are distinct, and (ii) the third outsider `b_3(z)` belongs to `ess-img(P_{x+z})`
> (equivalently, `b_3(z)` occurs on the unit circle about `x + z`).
>
> **Theorem 6.** `(S)` implies `(W)` in `S_1` at `k = 6`.

*Proof.* Fix `x` with `|V_x| = 3` and the open `U` of `(S)`. For a.e. `z in U`: Theorem 2 excludes
`b_1(z), b_2(z)` from `c(x+z)`, and `(S)` plus Lemma D at `x+z` excludes `b_3(z)`. So
`c(x+z) in T` a.e. on the open set `x + U`. The paper's Proposition 8.10 argument then applies
verbatim: place the seven-point Moser figure of (8.5) inside `x + U` with a margin `rho`, choose
`t in B(0,rho)` outside the seven null exceptional sets, and all seven translated vertices are
typical and carry only the three triangle labels; typical-point properness gives a proper
3-colouring of a graph of chromatic number 4 — contradiction. So no 3-valued type-`T` centre
exists; Theorem 5(h) makes the whole triangle locus locally finite; m4's Theorem 3 makes the rest
of `L` locally finite; `(W)` follows. `square`

**Why `(S)` is exactly the gap, and what it costs.**
* By Corollary 3, the two-term sum exclusion at `x` cannot exclude three labels at any point, so
  the third exclusion must come from a second centre. The only two available are: self-avoidance
  at `x+z` (the form stated in `(S)`), and the sum exclusion at a second centre. Both are
  colouring-level, and neither is implied by the palette data at `x` (that is Corollary 3's
  content).
* By Theorem 5(c)(d) the outer strip is *not* where `(S)` can hold: there the surviving outsider
  is not excluded but **forced**, so `(S)`'s open set must lie away from the outer strip (for
  instance in the inner region `|z| < 1`), where `(e)` gives the two-valued inner picture.
* By Proposition 8 the "local constancy" style repair — deriving label equalities inside the
  3-labelled pieces from finitely many unit-distance constraints — cannot work at three labels.
  So a proof of `(S)` must be genuinely two-centre and measure-theoretic (density-point and
  transport), of the same type as the paper's §6.3.2 four-cycle accumulation argument — which is
  not available for a 3-valued state because there is no parity to alternate.
* A weaker pointwise version of `(S)` (the exclusion holding at a positive-measure set of `z`
  without stability) does **not** suffice: the Moser step needs seven open neighbourhoods, i.e. an
  open 3-labelled region. This is the same distinction that made the `k = 5` case work (there the
  region (8.4) is *open*, by local constancy of the binary state) and that Proposition 8 blocks
  from being recreated at three labels.

I do not prove `(S)`; I claim only that it is the precise statement that both live routes (d1/d2's
`k = 6` §8 exclusion and d4's triangle gate) end up needing, and that the two natural mechanisms
for it are excluded (Corollary 3, Proposition 8).

---

## 10. What survives of the registered direction

The registered direction was: weaken m3's tameness hypothesis and prove (W) at `k = 6` for the
enlarged class. Two clean fragments survive, and one honest correction.

**(i) There is no enlarged tameness class at `k = 6` that is bigger than "has a 6-colouring".**
m3's hypothesis has two halves (finitely many cells; finitely many interface arcs per ball), and
m3's `k >= 7` countermodel fails both. At `k = 6` every known construction of an accumulating
cyclic locus runs through a point whose unit circle carries only three labels (m3's Lemma C / m4's
§5 need exactly three free labels, and `k - 3 = 3` at `k = 6`); such a point exists only if the
ambient colouring exists, i.e. only if `chi(R^2) <= 6`. So any class of `k = 6` colourings large
enough to contain a potential countermodel already presupposes the open problem. This is the right
sense in which "the `k = 6` boundary is the chromatic wall", and it is why I abandon this form of
the direction rather than push it.

**(ii) A countermodel to (W) must be locally infinite everywhere.** By Proposition 7, `not (W)` is
not "some accumulation point" but "`L` infinite in every ball of radius `> 1`". Corollary 5'
turns this into a concrete target at `k = 6` in `S_1`: not local finiteness of the triangle locus,
but its finiteness in one ball of radius `> 1`. m3's countermodel has exactly one accumulation
point and therefore does **not** refute (W) at `k = 7`; the phase-transition table for local
finiteness does not transfer to (W), and (W) at `k >= 7` is, as far as this note establishes, open.

**(iii) Heuristic, not a theorem.** Each `k >= 7` gadget needs three free labels on a unit circle,
so a `1`-dense family of gadgets would force the ambient colouring to be `(k-3)`-coloured on a
`1`-dense union of unit annuli, i.e. essentially on the plane. For `k = 7` that is a 4-colouring of
a dense open set, which `chi(R^2) >= 5` forbids. I have **not** turned this into a proof (the
"essentially on the plane" step is not rigorous), so I do not claim (W) at `k >= 7`.

---

## 11. What is NOT claimed

* Not (W), and not its negation, at any `k`; not `chi(R^2)`.
* Not the local finiteness of the `k = 6` triangle locus, not `(S)`, not the discreteness of a
  single 3-valued centre.
* Nothing conditional-free about `k = 6`: every statement in §6–§9 about `k = 6` colourings is
  vacuous if `chi(R^2) = 7` (there is then no weak measurable 6-colouring and `S_1` is empty).
  Corollary 3, Theorem 4 and Proposition 8 are unconditional.
* The bound in Corollary 3 is a bound on the (5.2) two-term sum exclusion at one centre. It is
  not a proof that no `k = 6` argument exists, and it does not cover Lemma 6.3's forcing rule
  outside `S_1`. Proposition 8 excludes finite-gadget repairs of §8.4's local-constancy step only.
* No claim about `ell = 4, 5, 6` beyond the observation that the sum-exclusion step is
  `k`-blind in the same way; those cases use the palette-size bound and the word combinatorics,
  which are `m6`/`m7`/`m2`'s territory.
* Theorem 5(d)(e) are `k = 6`-specific in the sense that `O(e) = O` identically only when the
  agreeing pair of edges covers the whole triangle and `k - 3` equals the size of the outsider
  set, which is true for every `k`; what is `k = 6`-specific is that the outsider set has three
  elements, so that (d) fixes one survivor out of three.

---

## 12. Files and reproduction

| file | content |
|---|---|
| `proof.md` | this note |
| `verify.py` | all 58 checks; blocks A (§2), B (§5), C (§5), D (§4), E (§6), F (§11 vacuity), G (§8). `python3 verify.py` exits 0 |
| `RESULTS.txt` | the recorded output of `verify.py` |

Reproduce: `cd .ultramath/smwfycxze/m1 && python3 verify.py`.
Two independent decision procedures are used for every sign decision (rigorous rational interval
arithmetic; exact `Q(sqrt3, sqrt11, sqrt33)` arithmetic with brackets from two different families),
and they agree in every case.
