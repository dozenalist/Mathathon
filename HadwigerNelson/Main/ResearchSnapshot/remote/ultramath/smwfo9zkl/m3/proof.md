# Local finiteness of cyclic centres fails for every k >= 7

**An explicit proper measurable colouring with an accumulating cyclic locus, whose palettes are
singletons almost everywhere. What it settles about the k = 6 route, and what it does not.**

Member m3, direction d11 (sprint B, swarm smwfo9zkl).
Verifier: `verify.py` (32 checks, two independent exact decision procedures). Run
`python3 verify.py` in `.ultramath/smwfo9zkl/m3/`; exit status 0 means all checks pass.

---

## 0. The result

`P_x(e)` is the maximal palette of Definition 5.1, `Gamma_x` the transition graph of
Definition 6.1, and `L = { x : Gamma_x contains a cycle }` the cyclic locus of Theorem 6.5.
Labels are `{0,...,k-1}`.

> **Theorem A.** Let `k >= 7`. There is a Lebesgue measurable colouring `c : R^2 -> {0,...,k-1}`
> such that, with `P_x` and `Gamma_x` defined by Definitions 5.1 and 6.1 verbatim for the label
> set `{0,...,k-1}`,
>
> 1. `c` is **proper**: `|p - q| = 1 => c(p) != c(q)`. Hence `c` is a weak measurable
>    `k`-colouring in the sense of Definition 1.2 (its colour classes contain no unit pair, so
>    the integral there vanishes identically).
> 2. **Every palette is a singleton.** For every centre `x` and almost every direction `e`,
>    `P_x(e)` is a one-element set; explicitly `P_x(e) = { c(x+e) }` up to an angular null
>    set. In particular `|P_x(e)| = 1` almost everywhere, which is strictly stronger than
>    the `k = 5` palette bound `|P| <= 2` and than the `k = 6` bound `|P| <= 3`.
> 3. The cyclic locus `L` is **not locally finite**: `L` contains the distinct points
>    `q_n -> q_*` (`q_*` interior to a square of side `1/100`), and `Gamma_{q_n}` contains the
>    triangle `{0,2,3}`.
> 4. At those centres the palette is **not binary**: `e |-> P_{q_n}(e)` takes the four distinct
>    values `{1}, {4}, {5}, {6}` on sets of positive angular measure, and the triangle labels
>    `0, 2, 3` occur in no palette at `q_n`.

Hence the conclusion of Theorem 6.5 ("`L` is closed and locally finite") is **false** for every
`k >= 7`; it is not a statement about the number of labels that degrades gracefully.

> **Corollary B (the exact insufficiency).** The following hypotheses do not imply local
> finiteness of `L`: properness; Lebesgue measurability; `|P_x(e)| = 1` almost everywhere; the
> palette-transfer exclusion (5.2); the smooth-transport exclusion (5.3); the sixty-degree
> exclusion (5.7). All hold for the colouring of Theorem A, and (5.2), (5.3), (5.7) hold for
> *every* weak measurable colouring by Lemma 5.2 and Corollary 5.4 of the paper (whose proofs
> never use the number of labels). `L` is still not locally finite.

So the `k = 6` analogue of Theorem 6.5, if true, must be proved from something that
distinguishes `k = 6` from `k = 7`: none of the palette-theoretic input of §5 can do it. At
`k >= 7` the statement is not unproved but false.

---

## 1. Exactly which number of labels the printed `k = 5` argument uses

Theorem 6.5 is proved cycle by cycle on `I = {1,...,5}`. The triangle case reads (§6.3):

> "For a triangle, (6.2) for its three edges and Proposition 5.6 force `P_x(e)` to intersect
> the pair of outside labels almost everywhere. Indeed, a nonempty subset of the three
> triangle labels of size at most two lies in some triangle edge, which is forbidden. By
> (5.7) the intersection with the outside pair is unique almost everywhere and alternates
> under `R`. Thus every such `x` is binary for that fixed pair."

Let `T` be the three labels of a triangle and `O = I \ T` the outsiders (`|O| = k-3`).

| step | hypothesis used | at `k = 5` | at `k >= 6` |
|---|---|---|---|
| `P_x(e)` not contained in `{i,j}` for each triangle edge | (6.2) | holds | holds |
| `P_x(e)` disjoint from `T` implies `P_x(e)` not contained in `T` | `\|P_x(e)\| <= k-3` and `\|T\| = 3` | `\|P\| <= 2 < 3` | fails, `P_x(e) = T` allowed |
| `P_x(e)` meets `O` | nonemptiness of palettes | holds | holds |
| the palette is confined to a **fixed pair** | `\|O\| = k-3 = \|P\|` | `\|O\| = 2` | fails, `\|O\| = k-3 >= 3` |
| `P_x(e)` meet `P_x(Re)` empty forces a **two-valued alternation** | (5.7) | holds for `\|O\| = 2` | fails: only `c(x+e) != c(x+Re)` |
| two-valued alternation implies binary implies locally finite | Lemma 5.5 | holds | no binary conclusion |

The single coincidence is `|O| = k-3 = 2`, i.e. `k = 5`. At `k = 6`, `|O| = 3`; at `k = 7`,
`|O| = 4`. The colouring below is built so that at each cyclic centre the palette runs through
**four** outsider labels `{1,4,5,6}` (a singleton at each direction, the singleton value taking
all four values), while the cycle in `Gamma_{q_n}` sits on labels `{0,2,3}` which never appear
in a palette. That is precisely the configuration `k = 5` forbids and `k >= 6` permits, and it
realises the *failure of the conclusion*, not merely a gap in the printed proof.

---

## 2. The construction (all data exact)

Let `w = e^{2 pi i/3}`, `r = 2/5`, `d = sqrt(3) r = 2 sqrt3/5`, `Lambda = d (Z + Z w)`.
Voronoi cells of `Lambda` are regular hexagons of circumradius `r` and inradius `d/2 = sqrt3/5`.
For a lattice point `z = d(m + n w)` put `z |-> (m + 2n) mod 7`; since `Norm(2 - w) = 7`,
`Lambda -> Lambda/(2-w)Lambda = Z/7` is exactly the colouring of the seven cosets.

**`c_0`, the paper's own seven-colouring** (paper, proof of Theorem 1.1): the Voronoi hexagons
of a triangular lattice with circumradius `r = 2/5`, centres coloured by the seven cosets of
`(2-w)Lambda`. Concretely `c_0(q) = (m+2n) mod 7` for the lattice point `d(m+nw)` nearest `q`.

**The modification.**

* `p_0 = (1/55, 18/55)`, `ell = 1/100`, `W = p_0 + [-ell/2, ell/2]^2`;
  `diam W = ell sqrt2 = 0.0141... < 1`, and `W` lies inside the hexagon of the origin.
* `q_n = p_0 + (ell 2^(-n-3), 0)`, `rho_n = ell 2^(-n-14)`, `D_n = B(q_n, rho_n)`,
  `n = 0,1,2,...`. Then `q_n` and `D_n` lie in the interior of `W`, and the `D_n` are pairwise
  disjoint: `|q_n - q_m| >= ell 2^(-max(n,m)-4)` while `rho_n + rho_m <= ell 2^(-max(n,m)-13)`.
* On `D_n`: the *Mercedes* partition into three closed sectors of `120` degrees centred at
  `q_n` -- label `0` on directions `(-60,60)` degrees, label `2` on `(60,180)`, label `3` on
  `(180,300)`. Its three interface rays (angles `60, 180, 300` degrees) carry the three pairs
  `{0,2}`, `{2,3}`, `{0,3}`, one pair per ray.
* On `W` minus the union of the `D_n`: label `0` (background).
* On `R^2 \ W`: `c = c_0`.

`c` is Borel. For `k > 7` add unused labels.

---

## 3. Proof of Theorem A

### 3.1 `c_0` is proper

Same-colour centres differ by a nonzero element of `(2-w)Lambda`, whose least length is
`|2-w| d = sqrt7 * 2 sqrt3/5 = 2 sqrt21 / 5 = 1.8330...` (`= sqrt21 * r`, the number used in
the paper). So two points of the same hexagon are at distance at most `2r = 4/5 < 1`, and two
points of distinct same-colour hexagons are at distance at least `2 sqrt21/5 - 2r = 1.0330... > 1`.
No unit pair is monochromatic. (Checked exactly in `verify.py` A1: with
`|d(m+nw)|^2 = (12/25)(m^2 - mn + n^2)`,
`min { m^2 - mn + n^2 : (m,n) != (0,0), m + 2n = 0 mod 7 } = 7`.)

### 3.2 Shadow lemma

If `p in W`, `q not in W` and `|p - q| = 1`, then `|p - p_0| <= ell/sqrt2`, hence

    1 - ell/sqrt2  <=  |q - p_0|  <=  1 + ell/sqrt2.

### 3.3 The annulus certificate

With `eps = 71/10000 = 0.0071 > ell/sqrt2 = 0.0070711...`, let
`A = { q : 1 - eps <= |q - p_0| <= 1 + eps }`. Then

> **`A` contains no point of `c_0`-colour `0`, `2` or `3`; colours `1, 4, 5, 6` all occur in `A`.**

This is a finite exact statement about the hexagonal tiling, certified twice in exact
arithmetic in `Q(sqrt 3)` by independent algorithms.

* **Method 1** (`verify.py` A2a). For each lattice point `z` of colour `0, 2, 3` whose Voronoi
  hexagon could meet `A`, compute exactly the least and greatest distance `d_min`, `d_max`
  from `p_0` to that closed convex hexagon (point-to-polygon distance, exact). A convex set
  meets the closed annulus iff `d_min <= 1+eps` and `d_max >= 1-eps`; the certificate is
  `d_min > 1+eps` (hexagon beyond the outer circle) or `d_max < 1-eps` (hexagon inside the
  inner circle). Slacks (`= max(d_min - 1, 1 - d_max)`, must exceed `eps`): colour `0`: no
  hexagon near `A` at all; colour `2`: `0.028950`; colour `3`: `0.017079`. Negative controls
  on the same code path: colours `1,4,5,6` give slacks `-0.0289, -0.3215, -0.1218, -0.2533`,
  i.e. they *are* present -- the test is not vacuous.
* **Method 2** (`verify.py` A2b). Cover `A` by closed axis-parallel squares of side `1/200`
  and `1/500`. For each square `Q` and each lattice point `z` of colour `0, 2, 3` with
  `dist(z,Q) <= r`, exhibit one face of the hexagon of `z` whose supporting half-plane misses
  `Q` (an affine function attains its extrema at the four corners of `Q`, so the check is
  exact). Every square passes. Negative control: the identical procedure with colour `1`
  fails on `1268` resp. `6305` (square, centre) pairs.

### 3.4 `c` is proper

* Two points of `W`: distance `<= ell sqrt2 < 1`, no constraint.
* Two points outside `W`: `c = c_0`, proper by 3.1.
* `p in W`, `q not in W`, `|p-q| = 1`: by 3.2 `q in A`, so by 3.3
  `c(q) = c_0(q) in {1,4,5,6}` while `c(p) in {0,2,3}`. Different. QED

Independent Monte-Carlo check (`verify.py` A3): 500000 unit pairs for `c`, 200000 of them with
one endpoint inside `W`; 100000 for `c_0`; no violation.

### 3.5 Sector transition lemma

> **Lemma.** Let `x in R^2`, `rho > 0`; suppose the colouring equals `i` on the sector
> `S_i = { x + s e^{i theta} : 0 < s < rho, theta in (alpha, alpha + 2pi/3) }` and equals `j`
> on the neighbouring sector `S_j` (angles `(alpha + 2pi/3, alpha + 4pi/3)`), the common
> interface being the ray `R` at angle `alpha + 2pi/3`. Let `B = B(x,s)`, let `n` be the unit
> normal to `R` pointing into `S_j`, and `0 < tau <= min(rho,s)/4`. Then
>
>     | { q in B : c(q) = i, c(q + tau n) = j } |  >=  (min(rho,s)/8) tau .

*Proof.* Put `m = min(rho,s)/2` and `E = { q in B(x,m) : q in S_i, 0 < dist(q,R) < tau }`.
For `q in E`, `c(q) = i`, `q + tau n in S_j` and `|q + tau n - x| <= m + tau < rho`, so
`c(q + tau n) = j`. In polar coordinates `(sigma, theta)` about `x`, `E` contains
`{ tau < sigma < m, |theta - (alpha+2pi/3)| < tau/(2 sigma) }`, of area at least
`integral_tau^m (tau/(2 sigma)) sigma d sigma = tau (m - tau)/2 >= tau m /4 = min(rho,s) tau /8`. QED

So `limsup_{h -> 0} |D_ij(B,h)|/|h| >= min(rho,s)/8 > 0` for each of the three pairs, i.e.
`{0,2}, {2,3}, {0,3}` are all edges of `Gamma_x`.

### 3.6 Every `q_n` is a cyclic centre

At `x = q_n` the three sectors of `D_n` have `rho = rho_n` and meet pairwise along the three
rays, so by 3.5 the triangle `{0,2,3}` is a subgraph of `Gamma_{q_n}`, which is cyclic.
(Monte-Carlo `|D_ij|/|h|/rho` in `[0.76, 1.21]`, against the lemma's bound `1/8`;
`verify.py` A4 for `n = 0,2,4,6,8`.)

### 3.7 Conclusion

`q_n -> p_0`, and the compact disc `B(p_0, ell/8)` contains all of `q_0, q_1, q_2, ...`, which
are distinct points of `L`. So `L` is not locally finite. QED

### 3.8 Palettes are singletons, and they are not binary at `q_n`

If a colouring is constant on the cells of a Borel partition then every trace `b in W_x`
satisfies `{ e : b_i(e) > 0 }` contained in `{ e : x + e` in `closure(A_i) }`: `y_n + r_n e`
tends to `x + e` uniformly, so if `x + e_0` is at positive distance from `closure(A_i)` then
`b_i` vanishes on a neighbourhood of `e_0`. Consequently `P_x(e)` is contained in the set of
colours of cells whose closure contains `x+e`, and since cells are open and an interior point
lies in a single cell, `P_x(e) = { c(x+e) }` for almost every `e`: the cell boundaries are a
countable, locally finite union of segments and arcs, and the circle of radius one about `x`
meets them in a null set of directions (each `d D_n` contributes at most `O(rho_n)` in angular
measure, and `sum_n rho_n < infinity`). So `|P_x(e)| = 1` a.e. for every `x` (`verify.py` A8).

For `x = q_n` and `|e| = 1` the point `x+e` lies in `A` (3.2, 3.3), so
`P_{q_n}(e)` is contained in `{1,4,5,6}`; as `e` varies the singleton value runs through all
four (`verify.py` A8; `[1,4,5,6]` observed). The triangle labels `0,2,3` occur in no palette at
`q_n`. So `q_n` is not binary for any pair of labels, Lemma 5.5 does not apply, and (5.7) holds
for the trivial reason that `c_0(x+e) != c_0(x+Re)` (those two points are at distance
`|e - Re| = 1`).

### 3.9 The method in general (and the k = 6 conditional)

Only steps 3.2, 3.4 and 3.6 are used; 3.1 and 3.3 are the verification that the paper's own
seven-colouring has the required property. Abstractly:

> **Lemma C (gadget insertion).** Let `c` be a proper measurable `k`-colouring, let `W` be a
> closed square of side `ell` with `ell sqrt2 < 1`, and suppose the unit-distance shadow
> `{ q : |q - p| = 1 for some p in W }` contains no point of three prescribed labels `a, b, d`.
> Then any relabelling of `W` with values in `{a,b,d}` keeps `c` proper. If moreover the
> relabelling contains, for some `q_*` interior to `W`, a sequence `q_n -> q_*` such that
> three labels `a', b', d'` meet pairwise at `q_n` along three rays (the Mercedes
> configuration), then `Gamma_{q_n}` contains the triangle `{a',b',d'}` and `L` is not
> locally finite.

Theorem A is the case `c = c_0`, `{a,b,d} = {0,2,3}`, `W` and `p_0` as in §2, with `a',b',d'`
the same three labels; no relabelling inside `W` can then be "seen" from the shadow.

For `k = 6` this gives a precise conditional, which is the only `k = 6` statement made here:

> **Corollary D.** If there is a proper 6-colouring `c` and a square `W` of side `ell < 1/sqrt2`
> whose unit-distance shadow misses three of the six labels, then the `k = 6` analogue of
> Theorem 6.5 is **false**: `c` can be relabelled inside `W` to have an accumulating cyclic
> locus. Conversely, if the `k = 6` analogue of Theorem 6.5 is true, then in every proper
> 6-colouring every square of side `< 1/sqrt2` has its unit-distance shadow hitting at least
> four of the six labels.

The hypothesis of Corollary D is a strong-looking but entirely finite-looking condition on a
6-colouring; I have not been able to decide it, and it cannot be decided without a 6-colouring.

**Robustness.** The annulus condition is not a knife-edge coincidence of `p_0`: it is
equivalent to a purely geometric statement about finitely many hexagons, and it holds on a
set of centres of positive area. (In a scan of the fundamental hexagon, `745` of `1223`
sampled centres have at least two colours missing from their unit circle, and the chosen
`p_0` has three colours missing with slack `> 0.017` and `> 0.028` respectively.) Any one
such centre serves.

---

## 4. Non-vacuity of the definitions

For the **unmodified** `c_0` the same definitions give `L` = the vertex set of the hexagonal
tiling, a lattice, which *is* locally finite. Reason: an edge `ij` of `Gamma_x` forces the
closures of a colour-`i` and a colour-`j` cell to meet at `x`, and at most three cells meet at
a point; so `Gamma_x` has `0`, `1` or `3` edges according as `x` is interior to a cell, on an
edge, or at a vertex. (`verify.py` A6: at a tiling vertex the cycle on the three colours
`{0,1,3}` is found with transition ratios `0.79-1.00`; at generic points `Gamma_x` is acyclic.)
So Theorem A is a genuine failure caused by the modification, not an artefact of the
definition of `Gamma_x`.

---

## 5. Scope: what is and is not settled

**Settled.**

* The conclusion of Theorem 6.5 is false for every `k >= 7` (Theorem A, explicit rational data).
  Local finiteness of cyclic centres is a genuinely small-`k` phenomenon.
* Local finiteness is not implied by the `k`-free palette machinery plus *any* palette bound
  weaker than `|P| <= 2`: Theorem A satisfies the strongest available smallness
  (`|P_x(e)| = 1` a.e.) together with (5.2), (5.3), (5.7), properness and measurability, and
  still has a non-locally-finite `L` (Corollary B). In particular "take the printed `k = 5`
  proof and replace `|P| <= 2` by `|P| <= 3`" cannot produce a `k = 6` theorem.
* The exact place where the label count enters is `|O| = k-3 = 2`, i.e. the table of §1: at
  `k >= 6` the palette is confined to no pair and the printed alternation does not occur.

**Not settled -- no claim is made.**

* Nothing about `k = 6`. The construction needs a proper colouring of `R^2` off a small square
  (for `k = 6` that is a 6-colouring, i.e. the open problem) plus three labels absent from the
  unit-distance shadow of that square; it cannot be run at `k = 6`. Whether the `k = 6`
  analogue of Theorem 6.5 holds is open here. (Note it is *vacuous* if `chi(R^2) = 7`, so it is
  meaningful only inside a contradiction argument that begins with a 6-colouring.)
* Nothing about `chi(R^2)`: this is a statement about the architecture of §5-§8, not a bound.
* The `k = 5` theorem is untouched: at `k = 5`, `|O| = 2 = |P|`, the printed argument stands,
  and it is machine-checked in this repository.

---

## 6. Exact data and how to check

| object | value |
|---|---|
| lattice | `Lambda = d (Z + Z w)`, `w = e^{2 pi i/3}`, `d = 2 sqrt3/5` |
| lattice point `(m,n)` | `( sqrt3 (2m - n)/5 , 3n/5 )` |
| label of the cell of `d(m+nw)` | `(m + 2n) mod 7` |
| hexagon circumradius / inradius | `2/5` / `sqrt3/5` |
| `p_0` | `(1/55, 18/55)` |
| `ell`, `W` | `1/100`, `p_0 + [-1/200, 1/200]^2` |
| annulus half-width certified | `eps = 71/10000 > ell/sqrt2 = 1/(100 sqrt2) = 0.00707106...` |
| colours in that annulus | `{1,4,5,6}` (exactly; `0,2,3` absent) |
| `q_n`, `rho_n` | `p_0 + (2^(-n-3)/100, 0)`, `2^(-n-14)/100` |
| Mercedes sector labels | `0` on `(-60,60)`, `2` on `(60,180)`, `3` on `(180,300)` degrees |
| labels used on `W` | `{0,2,3}` (never in a palette at `q_n`) |
| palette | singleton a.e. at every centre; `{1,4,5,6}` all attained at `q_n` |

```
cd .ultramath/smwfo9zkl/m3
python3 verify.py       # 32 checks; exit 0 on success; about 60 s
```

`verify.py` is self-contained: exact `Q(sqrt 3)` arithmetic; exact properness of `c_0`; both
independent annulus certificates with negative controls; properness of `c` (500000 unit pairs,
200000 with an endpoint in `W`); the sector-transition Monte-Carlo test at `q_n`; the
palette-singleton and palette-range checks with a positive control (at a tiling vertex the
probe correctly reports three labels); and the non-vacuity checks for the unmodified `c_0`.
The two annulus certificates are *decisions* in exact arithmetic; the Monte-Carlo parts only
illustrate estimates that are proved in 3.8 and 3.5.

## 7. Summary

`|P_x(e)| <= 2` is the only palette-theoretic hypothesis that local finiteness at `k = 5`
consumes, and it is exactly `k-3 = 2`. Relaxing it to `|P_x(e)| <= k-3` is not a bookkeeping
loss: **for every `k >= 7` the conclusion is false**, and the counterexample is the paper's own
seven-colouring with a rational perturbation supported in a square of side `1/100`, whose
palettes are singletons almost everywhere. The `k = 6` keystone therefore needs a strictly
`k = 6` input; none of the §5 apparatus can supply it.
