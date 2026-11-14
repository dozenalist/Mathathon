# d17 — the circle layer at k = 6: what it can and cannot force

*Swarm smwfk0ybk, member m1. Everything below is either proved here or checked by the named
script, exactly or by an integer identity; nothing is numerical evidence presented as a theorem.*

Files in this directory: `csp45.py`, `cert_singleton.py` (Section 1–2), `two_circles.py`,
`two_circles_proof.py` (Section 3).

---

## 0. Results

**R1 (the mission's Step 1 is decided, and the answer is YES).** The `(C4)+(C5)`-tightened
interface CSP at `k = 6` is satisfiable, at **every** interface length:

| `k` | `l` | geometries | `(C1)-(C3)` SAT | `(C1)-(C5)` SAT |
|---|---|---|---|---|
| 4 | 3 | 36 | 0 | 0 |
| 4 | 4 | 216 | 0 | 0 |
| 5 | 3 | 36 | 36 | 36 |
| 5 | 4 | 216 | 14 | 14 |
| 5 | 5 | 1296 | 0 | 0 |
| 6 | 3 | 36 | **36** | **36** |
| 6 | 4 | 216 | **216** | **216** |
| 6 | 5 | 1296 | **225** | **225** |
| 6 | 6 | 7776 | **177** | **177** |

So the decisive question of the brief has the answer *no UNSAT everywhere*: there are satisfiable
instances at `k = 6` at every `l in {3,4,5,6}`, and by the induction lemma (Step 1 of the brief)
`UNSAT at k = 6` would have been the only route to `chi >= 7`. **No terminal outcome L1–L5 is
reached by Step 1.** The counts are also an independent confirmation of m5's table: the two
implementations share no code (`csp45.py` rebuilds the sign matrix from the cell formula
`sigma_j^(i) = +1 iff (c_j + 1 - i) mod 6 in {0,1,5}` and the allowed sets from display (8.1)),
and agree **row by row against m5's stored `interface_csp_results.json` on 13 of its 14 rows** —
all of `k = 4,5,6` and `k = 7` at `l = 3,4,5,6` (the last two being `1296/1296` and `2593/7776`);
only `k = 7, l = 7` was not re-run here.

**Why the certificate is robust to its one dependency.** The single paper input it needs is the
definition of the allowed sets, and that is prose, not a display: *"Let `O(e)` be the set of labels
remaining after the endpoints of every positive edge are removed, and let `I(e)` be the set
remaining after the endpoints of every negative edge are removed. **Labels outside the cycle belong
to both sets.**"* (paper §8.1, `pdftotext -layout`; display (8.1) is
`P_x(e) ∩ O(e) ≠ ∅`, `P_x(e) ∩ I(e) ≠ ∅` a.e.). The certificate uses only `|P| = 1 <= k-3`, so it
is insensitive to whether the upper bound `k-3` is proved for general `k` or only at `k = 5`.

**R2 (why: the outsiders are never deleted).** In (8.1) the allowed sets are
`O_i = U ∪ {j : both incident signs −1}`, `I_i = U ∪ {j : both +1}` with `U = {l+1,...,k}` the
labels outside the cycle. An outsider is never an endpoint of an edge of the cycle, so it is
never deleted: `U ⊆ O_i ∩ I_i` for every `i`. Hence at `k = 6`, `l = 3` the palettes
`P_i = {4}` (i even), `P_i = {5}` (i odd) satisfy `(C1)` (size 1), `(C2)` (through `U`),
`(C3)` (alternate, cyclically), and `(C4)+(C5)` hold **vacuously** (no 3-set occurs). Same at
`l = 4` with `{5}/{6}` (labels are `1..k` as in the paper, so `U = {l+1,...,k}`). This is a
five-line certificate, verified on all `6^l` geometries by `cert_singleton.py`; no search is needed
and no constraint of the system can refute it.

**R3 (calibration: the `l = 3` level carries no information about `chi`).** The same witness
`[{4},{5},{4},{5},{4},{5}]` is a model for `k = 5, 6, 7` alike (`csp45.py`), i.e. the `l = 3`
system is SAT at `k = 5`, where the machine-checked truth is that no 5-colouring exists. So the
interface CSP at `l = 3` cannot certify any lower bound for any `k`; anything that could would
have to be a constraint that fails on this exhibition. The paper's own power sits at `l = 5`
(its Prop 8.2), which is exactly the one `k = 5` row that is UNSAT. **Consequence for any (C6)
round: a new constraint bites at `k = 6` only if it forbids, or restricts, mean-palette-size-1
configurations; and it must survive at `k = 7` (the hexagonal 7-colouring has singleton palettes
almost everywhere in angle, see R5).**

**R4 (new: two concentric circles never force a fourth colour, generically).** Extending m1's
prior no-go (single radius) to *two* radii: for every `x` and almost every pair `(r,s)` of radii,
the graph on `S_r(x) ∪ S_s(x)` with unit-distance edges is 3-colourable, by an explicit formula
(Theorem 3.1 below). So no single-centre window built from two concentric circles forces four
colours; in particular the paper's two strips (Lemma 8.1) do not derive their power from a
chromatic obstruction on the two circles, and cannot be replaced by one.

**R5 (singleton palettes are real, so `|P| >= 2` is not a truth about palettes).** The 7-colouring
of `Seven.lean` (`properColoring_seven`, `exists_measurable_proper_seven`) assigns to `x` the label
of the least centre of the triangular lattice within distance `7/15` in a fixed enumeration. Its
value changes only across the circles `|x - p| = 7/15`, a countable union of circles, hence a null
set; so the colouring is **locally constant off a null set**, and for a.e. direction `e` the palette
is the single label of the value near `x + e`: `|P_x(e)| = 1` for a.e. `e`, every `x`. Hence
`|P| >= 2` — the only shape a `k`-general (C6) could take to bite on the R2 models — is **false at
`k = 7`**. At `k = 6` it is not refuted by anything here, but it is not derivable from the circle
layer either (R6).

**R6 (the circle layer is provably empty at `k = 6`; cited, not re-derived).** From the previous
run (`m1/d7-SPHERE-CAP.md`, Theorems A–B and the window ladder): `chi(S_r(x)) <= 3` for all
`r`, with equality iff `theta(r)/2 pi = p/q`, `q` odd; `3` is attained (at `r = 1/sqrt 3` and at
every odd `q`); and by germ freedom no label set is excluded from a palette by one circle at any
radius. At `k = 6` the palette bound is `k - 3 = 3`, which is exactly the maximum number of colours
a circle can carry — so the circle layer can neither forbid a ternary palette nor force a second
label. The exact ladder at radius one is `chi(S_1) = 2`, `chi(S_1 ∪ {x}) = 3`, `chi(B(x,1)) >= 4`
(the Moser spindle sits in radius `3/sqrt 11 < 1`), and by R4 two radii do not raise the second
entry to 4. What is *not* proved here: that `chi(B(x,1)) = 4`, and that a three-radius window
cannot force four colours.

---

## 1. The computation (R1) and the certificate (R2)

`csp45.py` decides, for each `(k,l)`, every ray geometry (`6^l` cell vectors, of which `6^(l-1)`
after the rotation normalisation, counted once), whether some six palettes `P_0..P_5` satisfy

    (C1) 1 <= |P_i| <= k-3,   (C2) P_i meets O_i and I_i,   (C3) P_i cap P_(i+1) = empty,
    (C4) no two of the six are complementary 3-sets (k=6),   (C5) at most three are ternary (k=6).

It returned counts identical to m5's table for `(C1)-(C3)`, and, with `(C4)+(C5)` added, the same
counts again: **the tightening is inert at the level of satisfiability** in the computed range. That
includes `(5,4)` (14/216), which is therefore also a statement about the tightened system.

```
cd .ultramath/smwfk0ybk/m1 && python3 csp45.py      # 0.9 s, writes csp45_results.json
python3 cert_singleton.py                            # all 6^3 and 6^4 geometries, 0 rejections
```

Two comments on R2, since they are the load-bearing facts.

* **(8.1) is sound as used here.** `O` is what is left of `{1..k}` after deleting the endpoints of
  the positive edges of the cycle, `I` after deleting the endpoints of the negative ones; an
  outsider is an endpoint of no edge of the cycle, so it survives both deletions. This is
  independent of `k` and of the geometry.
* **`(C4)` and `(C5)` are inert for a structural reason, not by luck.** `(C3)` with `(C4)` forces
  `(C5)` (two disjoint ternary palettes in `Fin 6` are complementary, so ternary positions form an
  independent set of the 6-cycle), and no instance in the range needs a ternary palette at all,
  because the singleton construction is available whenever `k - l >= 2`.

---

## 2. What this does to the brief's Step 1

The brief asks: *with (C4) and (C5) added, is there any satisfiable `(l, sign matrix)` at `k = 6`?*
The answer is yes, at every `l`, and the `l = 3` models are singletons that violate nothing. So

* the induction lemma is not needed to settle Step 1 — its conclusion is false-as-a-no-go
  regardless, because the CSP is SAT;
* the interface CSP cannot reach L1 (`chi >= 7`) — nor L2–L5, which are outcomes of the other
  routes;
* any further round must add a constraint that fails on `P = [{4},{5},{4},{5},{4},{5}]`. By R5
  the only obvious candidate (`|P| >= 2`) is false at `k = 7`; so the honest target is a
  **`k = 6`-specific** constraint on singleton palettes, and by R6 it cannot come from one circle
  or from two concentric circles at all — it must come from the cross-centre structure (the
  translation representation, palette transport (5.2), or Lemma 5.5 separation).

---

## 3. Theorem: two concentric circles are 3-colourable, generically

**Setting.** Fix `x in R^2`, `r, s > 0`, `r != s`. Let `Gamma(r,s)` be the graph on the disjoint
union `S_r(x) ⊔ S_s(x)` with `p ~ q` iff `|p - q| = 1`. Write `p(alpha) = x + r e^{i alpha}` and
`q(beta) = x + s e^{i beta}`. Then

* `p(alpha) ~ p(alpha')` iff `alpha - alpha' = +- theta_r`, where `2 r sin(theta_r/2) = 1`
  (`theta_r = 2 arcsin(1/(2r)) in (0, pi]`, defined iff `r >= 1/2`; no inside edges if `r < 1/2`);
* `q(beta) ~ q(beta')` iff `beta - beta' = +- theta_s`;
* `p(alpha) ~ q(beta)` iff `alpha - beta = +- phi`, where `cos phi = gamma := (r^2+s^2-1)/(2rs)`
  (no cross edges if `|gamma| > 1`).

**Theorem 3.1.** Assume `r, s >= 1/2`, `|gamma| <= 1`, and:

> **(P)** every integer relation `m theta_r + n theta_s + 2k phi ≡ 0 (mod 2 pi)` has `m + n` even.

Then `Gamma(r,s)` is 3-colourable. An explicit colouring (`S^1` written additively, angles in
`R/2 pi Z`, colours in `{0,1,2}`) is: pick any function `F : S^1 -> Z/2` with
`F(u + theta_r) = F(u) + 1`, `F(u + theta_s) = F(u) + 1` and `F(u + 2 phi) = F(u)` — (P) is exactly
the compatibility that makes such an `F` exist — and set

    colour(p(alpha)) = F(alpha),        colour(q(beta)) = F(beta + phi) + 1   (mod 3).

**Proof.** *Existence of `F`.* Let `G = <theta_r, theta_s, 2 phi> <= S^1` and `H = <2 phi>`. By (P)
the assignment `theta_r H -> 1`, `theta_s H -> 1` is a well defined homomorphism `G/H -> Z/2`.
Since `S^1/H` is divisible and `Z/2` is divisible (hence injective as a `Z`-module), it extends to
`Psi : S^1/H -> Z/2`. Put `F(u) = Psi(u + H)`. Then `F(u + 2phi) = F(u)`, and
`F(u + theta_r) = F(u) + 1`, `F(u + theta_s) = F(u) + 1`.

*The colouring is proper.* Inside `S_r`: `F(alpha + theta_r) = F(alpha) + 1 != F(alpha)` (in `Z/3`).
Inside `S_s`: `F(beta + theta_s + phi) + 1 = F(beta + phi) + 1 + 1 = F(beta + phi) + 2`, which
differs from `F(beta + phi) + 1` in `Z/3`. Cross edges: if `alpha = beta + phi` then
`F(alpha) = F(beta + phi)` differs from `F(beta + phi) + 1`; if `alpha = beta - phi` then
`F(alpha) = F(beta - phi) = F(beta + phi - 2 phi) = F(beta + phi)`, again differing. *QED*

**Corollary 3.2.** For almost every pair `(r,s)` (complement of a countable union of proper real
analytic curves), and every `x`, `Gamma(r,s)` is 3-colourable. In particular no argument that
considers two concentric circles at one centre and only their chromatic number can force a fourth
colour at `k = 6`.

**Corollary 3.3 (the coordinate form used for verification).** Write an angle on `S_r` as
`a theta_r + b theta_s + 2c phi` and an angle on `S_s` as `a theta_r + b theta_s + (2c+1) phi`,
`a,b,c in Z`. Then (P) is precisely the statement that the assignment

    (a,b,c) on S_r  |->  (a + b) mod 2,        (a,b,c) on S_s  |->  (a + b) mod 2 + 1

is constant on coordinate classes with equal angle, so it descends to `Gamma(r,s)`. This is what
`two_circles_proof.py` checks: on the coordinate ball of radius 8 (777 vertices, 1272 edges) every
edge joins two different colours (**0 bad edges**), and the descent condition holds (collisions
carry equal colours) for the radii pairs listed. Note that the coordinate graph *covers*
`Gamma(r,s)` — distinct coordinates may be the same angle — so properness on the cover plus
constancy on the identified classes is exactly a proof for the true graph.

Pairs where (P) fails (found by the script, so these are the honest exceptions):
`(r,s) = (1, 1/sqrt 2)`, where `3 theta_r + 2 theta_s = pi + pi ≡ 0 (mod 2 pi)` has `m+n = 5` odd,
and `(1, 1/(2 sin(pi/q)))` for odd `q in {5,7}`, where `q theta_s ≡ 0 (mod 2 pi)` has `m+n = q`
odd. The construction fails there; `two_circles.py` nevertheless finds a 3-colouring of the finite
balls by backtracking for all ten tested pairs, so these are not counterexamples, only pairs
outside the theorem. **Nothing here proves `chi(Gamma(r,s)) <= 3` for all `(r,s)`; that remains
open.**

```
cd .ultramath/smwfk0ybk/m1 && python3 two_circles_proof.py   # coordinate check, exact integers
python3 two_circles.py                                       # 3-colouring search on finite balls
```

---

## 4. What is not claimed

* R1/R2/R3 are statements about the interface CSP *as encoded by m5 from (8.1), (5.7), Prop 5.6*.
  If that encoding misreads the paper, they inherit the error — they do not audit it (that is d2's
  and d14's job).
* R4 says nothing about three or more concentric radii, nor about windows that use directions
  rather than radii; the ball threshold `chi(B(x,1)) >= 4` and `chi(B(x,r)) = 4` for small `r` are
  open here.
* R5 is a statement about the a.e.-in-angle reading of palettes; under a definition that demands
  positive weight in a *fixed* angular window the hexagonal colouring's palettes would still be
  singletons a.e. but the argument should be re-run.
* No bound on `chi(R^2)` is proved or disproved anywhere in this note.
