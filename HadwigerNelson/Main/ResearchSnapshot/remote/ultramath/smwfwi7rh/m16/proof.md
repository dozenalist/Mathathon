# The label budget of the `m3` accumulation gadget is exactly 6

Member `m16`, direction `d4` (sprint B+, swarm `smwfwi7rh`).
Self-contained note; verification: `python3 verify.py` in this directory (two independent
procedures, exact rational arithmetic, exit status 0).

---

## 0. Result

`m3`'s construction (`.ultramath/smwfo9zkl/m3/proof.md`: a proper measurable colouring whose
cyclic locus `L` is not locally finite, for every `k >= 7`) is a **square-replacement gadget**.
One takes a proper colouring, a closed square `W` of side `ell` with `ell sqrt2 < 1`, recolours
`W` with three labels `{a,b,d}` (background plus an accumulating Mercedes triple of sectors),
and keeps properness by requiring that the **unit shadow**

    Sh(W) = { q : exists p in W with |p - q| = 1 }

meets none of `{a,b,d}`.

I compute the label cost of the whole family exactly. It is `ell + 3`, where `ell >= 3` is the
length of the cycle planted in `W`; so `m3`'s own instance (`ell = 3`) costs exactly **6**, and the
family is a `k >= 6` phenomenon with no slack at `k = 6`:

> **Theorem 2 (= 1.4 below).** Let `c` be a proper `k`-colouring, `U` a set of diameter `< 1`
> with `c(U) = L`, `|L| = ell`. Then `c` maps `Sh(U)` into `[k] \ L`, so
> `k - ell >= chi_meas(Sh(U))`; and if `U` contains a disc of positive radius then
> `chi_meas(Sh(U)) >= 3`. For `m3`'s square `chi_meas(Sh(W)) = 3` exactly. Hence
> `k >= ell + 3 >= 6`, with equality possible only for `ell = 3`, and equality in labels is
> attained by the `m3` square.

The two halves of `chi_meas(Sh) = 3` are new and independent of the paper:

* **(up) an explicit 3-colouring.** For every `0 < w <= 1/5`, the annulus
  `A_w = { z : 1-w <= |z| <= 1+w }` is properly 3-coloured by
  `z |-> floor(9 arg(z) / 2 pi) mod 3` (the 9 sectors of 40 degrees). Exact certificate below;
  the key point is that two points of `A_w` at unit distance subtend an angle in
  `(59.53, 60.48)` degrees, comfortably inside `(40, 80)`.
* **(down) no measurable 2-colouring.** A measurable proper 2-colouring of `A_w` would force,
  on the circle of radius `r`, the flip rule `f_r(theta + gamma(r)) = 1 - f_r(theta)` with
  `gamma(r) = 2 arcsin(1/(2r))`; for a.e. `r` the rotation by `2 gamma(r)` is ergodic, so `f_r`
  is constant, contradicting the flip. So `chi_meas(A_w) = 3` for every `w > 0`.

**Consequences for the `k = 6` question.**

1. **There is no label-counting obstruction at `k = 6`.** The `m3` gadget's budget at `k = 6`
   is met with zero slack, so the statement "there is no `k = 6` analogue of `m3`'s gadget" is
   *false as a counting statement*. Any obstruction must be a statement about 6-colourings
   themselves: at `k = 6` the gadget needs a proper 6-colouring whose **unit shadow of the square**
   (a thin band at radius 1, radial half-width between `ell/2` and `ell/sqrt2`) carries only 3
   labels. It is enough (but not necessary) that the whole annulus of half-width `ell/sqrt2`
   carries 3 labels.
2. **The `5 | 6` phase transition in this family is exactly this budget:** `3 + 3 = 6`. For
   `k <= 5` the budget is missed (`k - ell <= 5 - 3 = 2 < 3`), for `k = 6` it is exactly met.
   The paper's own counting coincidence `|O| = k - 3 = 2` at `k = 5` (which makes a cyclic
   centre binary, Lemma 5.5) is the same inequality seen from the palette side.
3. **A `k = 6` counterexample of this type is strictly constrained.** It needs a 6-colouring whose
   unit shadow band carries only 3 of the 6 labels. The paper's hexagonal 7-colouring has
   **4** labels there (`m3`, section 3.3: colours `{1,4,5,6}`), and `chi_meas = 3 < 4`: so a
   `k = 6` implementation needs a colouring strictly more label-efficient than the hexagon
   colouring on that annulus. Nothing in the palette machinery can produce it (the sprint's
   Theorem C), and nothing in counting can forbid it.
4. **The threshold is positive radius.** The sector-transition lemma that makes `q_n` cyclic
   needs sectors of positive radius `rho > 0`; a disc of radius `rho` forces `Sh(U)` to contain
   the annulus of radial half-width `rho`. An insertion confined to a single point would leave
   only the unit circle as shadow, which is measurably 2-colourable (it is a union of hexagons
   `C_6`), so that degenerate budget would be `3 + 2 = 5`. The cost therefore jumps from 5 at
   radius 0 to 6 at every positive radius — and the degenerate case is impossible anyway, because
   `L` is insensitive to modifications on Lebesgue-null sets (Lemma 3).

Nothing here bears on `chi(R^2)` or on `(W)`; the `k = 6` question stays open. What is settled
is the exact size of the label resource that the only known family of counterexamples consumes,
and therefore where a `k = 6` obstruction can and cannot live.

---

## 1. The three lemmas

Throughout `[k] = {0,1,...,k-1}`, `S^1` is the unit circle with angular Lebesgue measure,
`c : R^2 -> [k]`.

**Definition 1.1** (proper, measurable, weak measurable).
`c` is *proper* if `|p - q| = 1 => c(p) != c(q)`. It is *measurable* if all `c^{-1}(i)` are
Lebesgue measurable. It is a *weak measurable `k`-colouring* in the sense of the paper
(Definition 1.2) if `c^{-1}(i)` contains no unit pair up to null sets; by Lemma 4.3 of the paper
a weak measurable colouring differs from a proper measurable one on a null set, and by Lemma 3
below that modification does not change `L`. So all statements below for proper colourings
transfer to the paper's setting.

**Definition 1.2** (unit shadow). For `U subseteq R^2`,
`Sh(U) = { q in R^2 : exists p in U, |p - q| = 1 }`.

**Definition 1.3** (annulus, measurable chromatic number). `A_w(r) = { q : 1 - w <= |q - r| <= 1 + w }`,
`A_w = A_w(0)`. `chi_meas(X)` is the least `m` such that the unit-distance graph of `X` admits a
proper *measurable* `m`-colouring. (Only the measurable number is relevant: the paper's colourings
are measurable, and the graph-theoretic number of `A_w` is a different, harder question — see 4.4.)

### 1.1 Lemma 1 (shadow containments)

* (i) If `U` contains the closed disc `B(r,rho)` then `Sh(U)` contains `A_rho(r)`.
* (ii) If `U` is contained in `B(r,rho)` then `Sh(U)` is contained in `A_rho(r)`.
* (iii) In particular, for `m3`'s square `W = p_0 + [-ell/2,ell/2]^2`, `ell = 1/100`:
  `Sh(W)` contains `A_{ell/2}(p_0)` and is contained in `A_{ell/sqrt2}(p_0)`.

*Proof.* (i) Let `q = r + (1+t)u`, `|u| = 1`, `|t| <= rho`.
If `t >= 0` put `p = r + t u`; if `t < 0` put `p = r + t u` as well: then `|p - r| = |t| <= rho` and
`|q - p| = |u| = 1`. Either way `p in B(r,rho)` and `|q - p| = 1`.
(ii) `q = p + e` with `p in U`, `|e| = 1` gives `|q - r| <= |p - r| + 1 <= rho + 1` and
`|q - r| >= 1 - |p - r| >= 1 - rho`.
(iii) Every `p in W` has `|p - p_0| <= ell/sqrt2` (half-diagonal), and `W` contains `B(p_0, ell/2)`.
`square`

### 1.2 Theorem 1 (the annulus has measurable chromatic number 3)

Let `0 < w <= 1/5`.

**(a) Up.** The Borel function `chi(z) = floor(9 theta(z)/(2 pi)) mod 3`, where
`theta(z) in [0,2 pi)` is the argument, is a proper 3-colouring of the unit-distance graph of `A_w`.

*Proof.* Let `z_1 = r_1 e^{i theta_1}`, `z_2 = r_2 e^{i theta_2}` be in `A_w` with `|z_1 - z_2| = 1`,
and let `Delta = |theta_1 - theta_2| mod 2 pi in [0, pi]`. The cosine rule gives

    cos Delta = (r_1^2 + r_2^2 - 1) / (2 r_1 r_2) =: g(r_1, r_2).

`d g / d r_1 = (1 + r_1^2 - r_2^2) / (2 r_1 r_2) > 0` on `[1-w, 1+w]^2` (the numerator is at least
`1 + (1-w)^2 - (1+w)^2 > 0`), and likewise in `r_2`; so `g` is strictly increasing in each variable
and

    g(1-w, 1-w) = 1 - 1/(2(1-w)^2)  <=  cos Delta  <=  1 - 1/(2(1+w)^2) = g(1+w, 1+w).

At `w = 71/10000` these endpoints are `0.492824...` and `0.507025...`; at `w = 1/5` they are
`7/32 = 0.21875` and `47/72 = 0.652777...`. Both intervals are contained in
`(cos 80 deg, cos 40 deg)`, and the two comparisons are decided exactly, without any floating
point, by the cubic `p(x) = 8x^3 - 6x + 1`:

* `p(-1/2) = 3 > 0 > -1 = p(1/2)` and `p -> +-infinity`, so `p` has exactly one root in each of
  `(-inf,-1/2)`, `(-1/2,1/2)`, `(1/2,inf)`. The roots are `cos 160`, `cos 80`, `cos 40` degrees,
  because `cos 3t = 4 cos^3 t - 3 cos t = -1/2` for `t = 40, 80, 160` degrees, and
  `cos 160 < -1/2 < cos 80 < 1/2 < cos 40`.
* `p(173/1000) > 0 > p(174/1000)`, so the middle root satisfies `cos 80 deg < 174/1000`.
* `p(766/1000) < 0 < p(767/1000)`, so the largest root satisfies `cos 40 deg > 766/1000`.

Hence `0.1736... = cos 80 deg < 174/1000 < cos Delta < 766/1000 < cos 40 deg`, and since `cos` is
strictly decreasing on `[0,pi]`, `Delta in (40, 80)` degrees.

Now `theta -> 9 theta / (2 pi)` is `theta` measured in units of 40 degrees, so the two points land
in bins `b_1, b_2` with `|b_1 - b_2|` equal to 1 or 2 modulo 9: because `Delta` lies strictly
between one and two bin widths (and no bin boundary is crossed twice, and the wrap at `2 pi` is
handled by the fact that the bin count `9` is a multiple of `3`, so the bin index is defined modulo
9 on the circle). Bins differing by 1 or 2 modulo 9 differ modulo 3, so `chi(z_1) != chi(z_2)`.
`square`

**(b) Down.** There is no measurable proper 2-colouring of `A_w`.

*Proof.* Suppose `c : A_w -> {0,1}` is measurable and proper. Put
`gamma(r) = 2 arcsin(1/(2 r)) in (0, pi)` for `r in [1-w, 1+w]` (this is well defined because
`r >= 1-w > 1/2`). For every `theta` the point `r e^{i(theta + gamma(r))}` is at distance
`2 r sin(gamma(r)/2) = 1` from `r e^{i theta}`, so properness gives

    f_r(theta + gamma(r)) = 1 - f_r(theta)                                        (1.1)

for every `theta`, where `f_r(theta) := c(r e^{i theta})`. Applying (1.1) twice,

    f_r(theta + 2 gamma(r)) = f_r(theta).                                         (1.2)

`c` is measurable, so by Fubini in polar coordinates `f_r` is measurable for almost every `r`.
Pick `r` such that `f_r` is measurable and `gamma(r)/pi` is irrational; this is possible because
`gamma` is real analytic and strictly monotone on `(1/2, inf)`, hence `gamma(r)/pi` is rational for
only countably many `r`. For this `r` the rotation of the circle by `2 gamma(r)` is ergodic
(rotation by `alpha` is ergodic iff `alpha/(2 pi)` is irrational; equivalently, a bounded
measurable `h` with `h(theta + alpha) = h(theta)` a.e. is a.e. constant — two-line Fourier proof).
By (1.2) `f_r` is invariant, hence a.e. constant, contradicting (1.1), which forbids any constant.
`square`

**Corollary 1.2.1.** `chi_meas(A_w) = 3` for every `0 < w <= 1/5`; and `chi_meas(Sh(W)) = 3` for
`m3`'s square, and more generally for every `U` with `B(r,rho) subseteq U subseteq B(r,rho')`,
`0 < rho <= rho' <= 1/5`, by Lemma 1 and monotonicity of `chi_meas` under inclusion.

### 1.3 Lemma 3 (null modifications do not move `L`)

Let `c, c'` be colourings differing on a Lebesgue-null set `N`. Then their transition graphs
(`Definition 6.1` of the paper, equation (6.1)) agree at every centre: `Gamma_x = Gamma'_x`, hence
`L = L'`.

*Proof.* For distinct labels `i,j`, a bounded ball `B` and `h != 0`,
`D'_{ij}(B,h) = { q in B : (c'(q), c'(q+h)) in {(i,j),(j,i)} }` differs from `D_{ij}(B,h)` only
inside `N union (N - h)`, a null set. So the areas agree, all `limsup` in (6.1) agree for every
ball, and the edge sets of `Gamma_x, Gamma'_x` agree for every `x`. `square`

**Remark 1.4.** Lemma 1.3 is why the gadget must act on a set of positive measure; combined with
the positive radius that the sector lemma needs (see 2.1), it is also why the annulus, and not just
the circle, appears in the budget.

### 1.4 Theorem 2 (the budget theorem)

Let `c` be a proper `k`-colouring, `U subseteq R^2` with `diam U < 1`, `L = c(U)`,
`ell = |L|`. Then

* (i) `c` maps `Sh(U)` into `[k] \ L`; consequently `k - ell >= chi_meas(Sh(U))`;
* (ii) if `U` contains a disc of radius `rho > 0`, then `chi_meas(Sh(U)) >= 3`; and
  `chi_meas(Sh(U)) = 3` whenever `U` is contained in a disc of radius `<= 1/5`;
* (iii) hence `k >= ell + 3`, and `k = ell + 3` is attained for `m3`'s square
  (`ell = 3`, `U = W`).

*Proof.* (i) `q in Sh(U)` means `q = p + e` with `p in U`, `|e| = 1`, so properness gives
`c(q) != c(p) in L`. Since (i) holds for every `q in Sh(U)`, the restriction of `c` to `Sh(U)` is a
proper measurable `(k - ell)`-colouring of the unit-distance graph of `Sh(U)`, whence
`k - ell >= chi_meas(Sh(U))`. (`diam U < 1` is not needed for (i); it is what makes the gadget
proper *inside* `U` in the first place.)
(ii) `Sh(U) supseteq A_rho(r)` by Lemma 1(i), so `chi_meas(Sh(U)) >= chi_meas(A_rho(r)) = 3` by
Corollary 1.2.1. If moreover `U subseteq B(r,rho')` with `rho' <= 1/5` then Lemma 1(ii) and
Corollary 1.2.1 give `chi_meas(Sh(U)) <= chi_meas(A_{rho'}(r)) = 3`, hence equality. (For a fat `U`
the shadow may well need more than three labels; that is why the gadget takes `W` small, and it is
all the budget theorem needs.)
(iii) is (i)+(ii) with `m3`'s data: `U = W`, `ell = 1/100`, `Sh(W) subseteq A_{71/10000}(p_0)`
because `ell/sqrt2 = 1/(100 sqrt 2) = 0.00707106... < 0.0071 = 71/10000` (exact:
`ell^2 < 2 (71/10000)^2`), and `Sh(W) supseteq A_{ell/2}(p_0)`. Either annulus is a legal `A_w`
with `0 < w <= 1/5`, so `chi_meas(Sh(W)) = 3`. `square`

---

## 2. The gadget, and why `k = 6` is exactly its budget

### 2.1 The gadget's own requirements, in the `m3` normalisation

`m3`'s data: `ell = 1/100`, `p_0 = (1/55, 18/55)`, `W = p_0 + [-ell/2, ell/2]^2` (so
`diam W = ell sqrt2 = 0.01414... < 1`), centres `q_n = p_0 + (ell 2^{-n-3}, 0) -> p_0`, discs
`D_n = B(q_n, rho_n)`, `rho_n = ell 2^{-n-14} > 0`, and a Mercedes partition of `D_n` into three
sectors of 120 degrees labelled `0, 2, 3`. What the construction uses:

* **positive radius:** the sector-transition lemma needs sectors of radius `rho > 0` and produces
  `|D_{ij}(B,h)| >= min(rho,s) tau/8 > 0`, i.e. the three pairs `{0,2},{2,3},{0,3}` are edges of
  `Gamma_{q_n}`. So `U` contains a disc of radius `rho_0 > 0` (any one of the `D_n`);
* **three labels on `U`:** `Gamma_{q_n}` must contain a cycle, and a cycle has at least three
  labels, all of them used near `q_n` (a small ball about the interior point `q_n` lies in `U`,
  so every vertex of `Gamma_{q_n}` is a colour of a point of `U`). So `ell >= 3`;
* **properness across the boundary:** every point of `Sh(U)` is at unit distance from a point of
  `U`, so `Sh(U)` must avoid all `ell` labels of `U` — this is exactly Theorem 2(i).

Hence the three requirements are `ell >= 3`, `k - ell >= chi_meas(Sh(U)) >= 3`, `rho > 0`, i.e.
`k >= 6`, and `m3` at `k = 7` uses `ell = 3`, `k - ell = 4 >= 3` with one label of slack. At
`k = 6` there is no slack: the three cycle labels and the three shadow labels must partition `[6]`.

### 2.2 Specification of what a `k = 6` countermodel of this family must be

Combining 2.1, 2.3 and Theorem 2, a counterexample to local finiteness at `k = 6` built by
square replacement must satisfy all of:

* **(S1) triangular accumulation.** `ell = 3` and the planted cycle is a triangle: at `k = 6`,
  `ell + 3 <= k` forces `ell = 3`, so every accumulating centre has a triangle in `Gamma` and no
  longer cycle can be planted. (The `ell = 4,5,6` variants need `k >= 7,8,9`.)
* **(S2) exact partition of the labels.** The three planted labels and the three labels occurring
  on the shadow annulus are complementary subsets of `[6]`. So the shadow can afford no fourth
  label anywhere: one label of slack, as in `m3` at `k = 7`, is not available.
* **(S3) three-valued palettes with the right values.** At each accumulating centre `q` the
  maximal palette is a.e. a singleton (`P_q(e) = {c(q+e)}`) whose set of values is exactly the
  shadow triple; the cycle triple never appears in a palette, so self-avoidance
  (`c(q) not in P_q(e)`) holds automatically and Lemma 5.5 cannot apply.
* **(S4) positive radius.** The insertion region contains a disc of positive radius, hence the
  shadow contains a fat annulus of radius 1; a null insertion cannot move `L` at all (Lemma 3).
* **(S5) the hard part.** The 6-colouring must be *globally* proper, and its restriction to that
  annulus must be one of the three-labelled colourings of Theorem 1(a). Since the annulus is
  globally constrained by its own shadow (and so on), this is a statement about a 6-colouring of
  the plane, not a local construction.

(S1)-(S4) are label-level and are now decided; (S5) is exactly the open problem. This is the
precise sense in which `k = 6` is "the same gadget with no slack" rather than a different
construction.

### 2.3 The palette form of the same statement

At a centre `q_n in W`, the maximal palette (paper, Definition 5.1) is the singleton
`P_{q_n}(e) = { c(q_n + e) }` a.e., and `q_n + e` runs over the unit circle about `q_n`, which
lies in `Sh(W)`; so

    P_{q_n}(e) subseteq [k] \ L  for a.e. e,  and  { P_{q_n}(e) : e } = c(S^1(q_n)).

So in the palette language: **a `k=6` counterexample of this family must have a cyclic centre whose
whole palette field takes values in a fixed 3-element set disjoint from its cycle labels.** This is
exactly the extremal configuration that the plan's "six-cycle free-label" and "four-cycle
free-label" analyses study, with the extra geometric content that the 3-element set is realised by
an actual colouring of an actual thin annulus. `m3`'s instance has a 4-element palette
`{1,4,5,6}`; at `k = 6` it would have to be 3.

### 2.4 What `k = 6` needs, and what it cannot need

**Corollary 2.1 (general local-modification no-go at `k <= 5`).** The square is not used. Let `c`
be a proper measurable colouring, `c'` another that agrees with `c` off a bounded set `U` of
diameter `< 1`, and `q` an interior point of `U` with `Gamma'_q` cyclic. Then `k >= 6`.
*Proof.* An edge `ij` of `Gamma'_q` needs a ball `B ⊆ U` with `limsup |D'_{ij}(B,h)|/|h| > 0`;
picking `q' in B` with `c'(q') = i` and `c'(q'+h) = j` for arbitrarily small `h` shows that `q'`
and `q'+h` both lie in `U`, so `i, j in c'(U)`. Hence every vertex of `Gamma'_q` is a colour used
on `U`, so `ell := |c'(U)| >= 3`, and Theorem 2 gives `k >= ell + chi_meas(Sh(U)) >= 3 + 3 = 6`.
`square`
So no bounded local modification of diameter `< 1` can create a cyclic centre at `k <= 5` by any
mechanism, and at `k = 6` exactly the configuration (S1)-(S4) is possible.

**Corollary 2.2 (no counting obstruction).** For every `k` and every gadget of this type,
`k >= 6`. Consequently:

* no accumulation gadget of this type exists at `k <= 5` — the `5 | 6` transition of the paper's
  Theorem 6.5 is *matched exactly* by the gadget's label budget `3 + 3`;
* at `k = 6` the budget is met, so **no statement about label counts, palette sizes, shadows,
  chromatic numbers of the shadow region, or their densities can exclude a `k = 6` analogue of
  `m3`.** Such an exclusion would have to be a statement about the 6-colouring itself, i.e. it
  would have to prove that no proper 6-colouring carries only 3 labels on a thin annulus of radius
  1 — a colouring-level statement of exactly the kind the sprint's frontier identifies.

**Remark 2.3 (why the square is small and the annulus is thin).** `m3`'s `W` is chosen small so
that `diam W < 1` (properness inside `W` is free) and so that `Sh(W)` is thin. The thinness is what
makes `chi_meas(Sh(W))` equal 3 rather than 4: a thin annulus is *not* 2-colourable (Theorem 1(b)),
yet it is 3-colourable (Theorem 1(a)), and for a fat annulus — say half-width `1/2` — the 3-colouring
fails (e.g. `(1/2,0)` and `(3/2,0)` are at unit distance with equal colour). `m3`'s
annulus is far thinner than the range `w <= 1/5` where the 3-colouring is certified, so the
certificate has a wide margin: `Delta` lies in `(59.53, 60.48)` degrees against the window
`(40, 80)`.

---

## 3. What this settles about the directions of the brief

**Direction 6 (the `k = 7` counterexample).** The question was: *why can `m3` not be pushed to
`k = 6`, and can a variant with three outsiders and a different cycle structure work?* Answer:
the gadget is label-neutral at `k = 6`. Its cost is `ell + 3` with `ell >= 3` the length of the
cycle planted in `W`, so

* every variant with a longer cycle (`ell = 4,5,6`, the four- and six-cycle variants the
  coordinator's leads (i) and (ii) discuss) costs strictly more: `7, 8, 9` labels. The triangle is
  the optimal planted cycle and cannot be improved;
* a variant with "three outsiders" is exactly the `k = 6` shape of the `m3` gadget (three shadow
  labels), and it is feasible in labels;
* the actual obstruction at `k = 6` is not in the gadget at all: it is the *input colouring*. `m3`
  consumes one proper `k`-colouring whose shadow band carries `k - 3` labels; at `k = 7` the
  paper's hexagon colouring supplies one (with `4 >= 3` labels on the band), and at `k = 6` the
  existence of *any* proper 6-colouring is the open problem. So an obstruction theorem "no `k = 6`
  analogue of `m3`'s gadget" is **not** available from counting, and would be a strictly stronger
  theorem about 6-colourings.

**The frontier, restated with the new constraint.** A `k = 6` counterexample of this family is
produced by:

    a proper 6-colouring  +  a point p and 0 < rho <= 1/5 with the annulus A_rho(p) carrying <= 3
    labels, plus a square W inside B(p, rho/2) whose own 3 labels are exactly the complement

and the same statement with `A_rho(p)` replaced by the (smaller) unit shadow of `W` is what the
construction actually requires.

Both halves are now measured: the annulus can carry 3 labels (explicitly), it cannot carry 2 (no
measurable 2-colouring), and the paper's own 7-colouring carries 4 there. So the `k = 6` question,
in this family, is precisely: *does a 6-colouring exist that is one label more efficient than the
hexagonal one on a thin annulus of radius 1?*

**What this does not do.** It does not prove or refute `(W)`; it does not decide `k = 6`; it does
not produce a 6-colouring; and it says nothing about gadgets that are not of square-replacement
type. It removes one candidate for a `k = 6` obstruction, with a proof and an exact certificate,
and it sharpens the boundary: the `m3` family is exactly a `k >= 6` phenomenon in labels, so the
`5 | 6` transition is not evidence that the family is a `k = 7`-only trick.

---

## 4. Remarks, sharpenings, and a sub-question

**4.1 The degenerate case `rho = 0` would cost 5.** The unit circle `S^1` has unit-distance graph
a disjoint union of hexagons `C_6` (each `theta`-orbit of the map `theta -> theta + pi/3`), and
`theta -> floor(3 theta/pi) mod 2` is a proper measurable 2-colouring of it. So an insertion
confined to a single point would need only `3 + 2 = 5` labels. It is excluded twice over: a null
insertion does not change `L` (Lemma 1.3), and the sector lemma needs `rho > 0`.

**4.2 Consistency with the printed `k = 5` proof.** At `k = 5`, `k - ell = 2 < 3`: the shadow
cannot be coloured, so no `m3`-type accumulation exists. This is the geometric counterpart of the
printed argument's `|O| = k - 3 = 2 = |P|` (Lemma 5.5 applies, cyclic centres are binary and hence
separated by `delta_*`). Both statements say: at `k = 5` the three cycle labels leave too few
labels for the unit circle's neighbourhood.

**4.3 The `m3` shadow is *not* optimal in the 7-colouring.** `m3` certifies that the annulus
`1 +- 71/10000` around `p_0` in the hexagon colouring meets exactly the four colours `{1,4,5,6}`.
Since `chi_meas` of that annulus is 3, the hexagon colouring spends one label more than necessary.
A `k = 6` gadget therefore needs a colouring that is *better tuned* than the paper's 7-colouring at
that annulus — a concrete, finite-looking requirement, but a global one.

**4.4 The graph-theoretic number of `A_w` is a separate question (open here).** Theorem 1(b) is a
measurability statement. For *arbitrary* 2-colourings one would need an odd cycle in the
unit-distance graph of `A_w`. Angular accounting bounds its length from below: every unit pair in
`A_w` has angular difference in `[gamma(1+w), gamma(1-w)]` with
`gamma(r) = 2 arcsin(1/(2r))`, and a closed odd polygon needs a signed sum
`sum +- x_i = 2 pi m` with `x_i` in that window; since `p - q - 6m` is odd, one gets
`n >= pi / (3 (gamma(1-w) - pi/3))`, which is `>= 127` for `w = 71/10000` and `>= 0.9/w` in
general. So no short odd cycle exists and the bipartiteness of `A_w` is a long-range question; I
make no claim about it, and the application does not need it (the paper's colourings are
measurable).

**4.5 Nothing is special about radius 1.** Theorem 1(b) holds for `A_w(R)` at every `R > 1/2`
and every `w > 0` (`gamma(r) = 2 arcsin(1/(2 r))` is the same function of the radius `r`, and
`R > 1/2` makes the arcsin well defined). Theorem 1(a)'s nine-sector colouring works for every
`R, w` with `0.778 < R - w` and `R + w < 1.462` (the window `(40, 80)` in degrees). Radius 1 is
only where the gadget puts its shadow, because the palette is a radius-one object
(Definition 5.1 of the paper).

**4.6 The `w <= 1/5` range is not the truth.** The 9-sector colouring is proper as long as
`g(1-w,1-w) > cos 80` and `g(1+w,1+w) < cos 40`, i.e. `w < 0.2221...`; the bound `1/5` is chosen
for an exact rational certificate (`7/32 > 174/1000` and `47/72 < 766/1000`). Larger `w` needs more
labels or a better colouring; I use only `w <= 71/10000`.

---

## 5. Exact data and how to check

| object | value |
|---|---|
| annulus colouring | `chi(z) = floor(9 arg(z)/(2 pi)) mod 3`, 9 sectors of 40 degrees |
| certified range | `0 < w <= 1/5` (truth: `w < 0.2221...`) |
| `cos Delta theta` at `w = 71/10000` | `[0.492824..., 0.507025...]` |
| `cos Delta theta` at `w = 1/5` | `[7/32, 47/72]` |
| window needed | `(cos 80, cos 40) = (0.1736..., 0.7660...)` |
| exact cosine bounds | `8x^3-6x+1` changes sign on `(173,174)/1000` and `(766,767)/1000` |
| `m3` square | `ell = 1/100`, `p_0 = (1/55, 18/55)`, `W = p_0 + [-1/200,1/200]^2` |
| shadow containment | `A_{1/200}(p_0) subseteq Sh(W) subseteq A_{71/10000}(p_0)` |
| budget | `k >= ell + 3`, `ell >= 3`; `m3` attains `3 + 3 = 6` at `k = 6` in labels |
| measurability down-proof | `gamma(r) = 2 arcsin(1/(2r))`, ergodicity of the rotation by `2 gamma(r)` |

```
cd .ultramath/smwfwi7rh/m16
python3 verify.py     # exit 0 = all checks pass (about 15 s)
```

A Lean 4 formalisation of the two cosine bounds and of the rational range statement
(`cubic_mono_right`, `cubic_mono_mid`, `cos_two_pi_div_nine_bounds`, `cos_four_pi_div_nine_bounds`,
`annulus_cos_range`) was written for this note but **could not be compiled**: while this swarm runs,
the VM is at load 26-32 on 4 cores with about 3 GB free, and `lean` on a file importing
`Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic` did not finish in 600 s (1.6 s of user CPU
in that time — the process is starved, not slow). It is therefore **not** part of the certificate
and is not included. The certificate is exact rational arithmetic (`fractions.Fraction`) with an
independent sampling cross-check, i.e. a two-path exact verification of the same two inequalities.

`verify.py` runs two independent procedures for the load-bearing inequality — (A) the exact
algebraic reduction to the monotonicity of `g` plus rational endpoint evaluation plus the cubic
sign checks, and (B) direct sampling of exactly-unit pairs in the annulus (200000 random, and a
vectorised grid of `1.44 * 10^6` radius pairs times 60 angles times 2 orientations), both finding
zero colour clashes — together with the exact shadow-containment algebra and three vacuity
controls (the thick annulus where the colouring provably fails, the unit circle where a 2-colouring
exists, and the `m3` diameter/annulus inequalities).
