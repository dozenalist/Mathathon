# The six-cycle free-label case at k = 6: exact decision and its delimitation

Setting: `k = 6`, labels `[6] = {0,...,5}`, the six-cycle `C_6` with edge labels `0..5` in cyclic
order (edges `{i,i+1}` mod 6). At a cycle centre `x` every palette `P_x(e)` is admissible:

  (A) `2 <= |P_x(e)| <= 3` and `P_x(e)` is not contained in any cycle edge  (Lemma 6.2 / (6.2),
      with the palette bound `|P| <= 3`; singletons are excluded because every label lies in a
      cycle edge).

A **free label** is a label in no palette. **Non-proper self-avoidance** = there is a label `i`
with `i notin P_z(e)` for every centre `z` and a.e. direction `e`.

Everything below is at the palette level: a *sector field* is
`P_z(theta) = sigma(floor(theta/Delta) mod 6m)`, `Delta = 2 pi/(6m)`, `sigma : Z_{6m} -> palettes`,
independent of `z`. That is the class used by `sprint/k6/FREE-LABEL.md` and `Theorem C`.

---

## 0. The transport constraint in sector language

`Delta = 2pi/(6m)`, `d_0 = pi/(9m) = Delta/3`. Let `z,z'` be centres with `a = z'-z`,
`0 < |a| <= d_0`, `f` a unit direction, `W = f + a`, `r = |W|`. The two exact unit decompositions of
`z' + f` over `z` are `s_+- = W (1/2 +- i sqrt(1/r^2 - 1/4))`, and `s_+ + s_- = f + a` (both are
unit vectors, nonparallel for small `|a|`). **GEOM** (proved in `work/verify_geom.py`, exact
rationals and then numerically):

    | arg s_+- - (arg f +- pi/3) |  <=  (arcsin d) + d/sqrt(4-(1+d)^2)  <=  1.5938 |a|.

*Proof.* `|W - f| = |a| <= 1` gives `|arg W - arg f| <= arcsin|a|`; `arg s_+- = arg W +- arccos(r/2)`
and `|r-1| <= |a|` gives `|arccos(r/2) - pi/3| <= |a| / sqrt(4-(1+|a|)^2)` by the mean value
theorem. For `0 < d <= d_0 <= pi/45`, `arcsin d <= d(1 + d^2/6 + d^4/4)` and
`1/sqrt(4-(1+d)^2) <= 0.5918`, so the coefficient is at most `1 + 0.5918 + d_0^2/6 + d_0^4/4
<= 1.5938`; the script checks this in `Fraction` arithmetic (tightest margin 0.001182 at `m = 5`).
Also `1.5938 d_0 = 1.5938 pi/(9m) < pi/(3m) = Delta`, exactly `15938/90000 < 1/3`.

So `arg s_+-` lies within one sector width of `arg f +- pi/3`, whose sector index is `i +- m`
(`pi/3 = m Delta`). Hence (5.3) is implied by

  (T) `sigma(i) cap sigma(i+o) = empty` for all `i in Z_{6m}` and all six
      `o in {+-(m-1), +-m, +-(m+1)} mod 6m`.

(the converse inclusion is not needed: (T) is a *superset* of the instances that occur, so a word
satisfying (T) satisfies (5.3), and an impossibility proof for (T) gives impossibility for (5.3)).
Numerically, `work/verify_geom.py` samples the true geometry (`theta` grid x `psi` grid x 4 radii)
and finds max `|arg s - (arg f +- pi/3)|/|a| = 1.169 < 1.5938`, and realised sector displacements
exactly `{+-(m-1), +-m, +-(m+1)}`; no indexing or sign error is possible.

`o = m` is (5.7) (`P(e) cap P(Re) = empty`, `R` = rotation by `pi/3`), so (T) contains (5.7).
For `m >= 2` no offset is `0` (it would need `m = 1`).

---

## 1. THEOREM 1 (classification, exact)

**Theorem 1.** Let `m >= 2`, `n = 6m`, and let `V` be any set of palettes that are (A)-admissible
and avoid the fixed label `0` — in particular `V` may be the six pairs
`A={1,3}, B={1,4}, C={1,5}, D={2,4}, E={2,5}, F={3,5}`, or those six plus the ten triples of
`{1,...,5}`, or all of them. Then there is a word `sigma : Z_n -> V` with (T) **iff `m >= 5`**.

Equivalently: the six-cycle free-label sector model exists at resolution `m` iff `m >= 5`.

The disjointness graph `H` on the six pairs (edge = disjoint) is

    A--E, A--D, B--E, B--F, D--F, C--D          (a 5-cycle A-E-B-F-D-A plus the pendant C--D).

This is the whole combinatorial content: `H = C_5` + pendant, degrees `3,2,2,2,2,1`.

### 1a. `m >= 5`: the explicit uniform word

Let `u_m = A A B B D^{m-3} E E F^{m-3}`, a cyclic word of length `2m` (nonnegative counts because
`m >= 5`), and `sigma_m` = `u_m` repeated three times (length `6m`; `2m | 6m`).

*Proof of (T).* Modulo `2m` the six offsets reduce to `{m-1, m, m+1}` (because `2m - (m-1) = m+1`
and `2m - (m+1) = m-1`), so it suffices that `u_m(i) cap u_m(i+m+delta) = empty` for
`delta in {-1,0,1}` and all `i in Z_{2m}`. The position ranges of `u_m` are

    {0,1}=A   {2,3}=B   [4,m]=D   {m+1,m+2}=E   [m+3,2m-1]=F

and for each `i` the three partners `i+m-1, i+m, i+m+1` lie in the following letters:

| `i` | partners land in | letter pairs used |
|---|---|---|
| `{0,1}` | `{m-1,...,m+2}` = D,E | A-D, A-E |
| `{2,3}` | `{m+1,...,m+4}` = E,F | B-E, B-F |
| `[4,m]` | `[m+3, 2m+1]` = F on `[m+3,2m-1]`, A at `2m = 0` and `2m+1 = 1` | D-F, A-D |
| `{m+1,m+2}` | `{0,1,2,3}` = A,B | A-E, B-E |
| `[m+3,2m-1]` | `[2,m]` = B,D | B-F, D-F |

All six pairs are edges of `H`. (The D-range needs `m >= 4`, the E/F ranges `m >= 3`, and the
argument is uniform in `m`; `work/check1.py` additionally checks `m = 5..200` directly.)
`square`

The values used are `A,B,D,E,F`; `C` is never used; every value is a pair, so (A) holds, and every
value avoids `0` and `5`. In particular: all palettes are pairs, so `m2`'s two-centre bound gives
`2+2 = 4 <= 5`; `m11`'s ternary density is `0 <= 1/2`; (P6) has no complementary triple pair
(vacuous).

### 1b. `m = 2, 3`: three pairwise disjoint values are impossible

For `m = 2` (`n = 12`, offsets `+-1,+-2,+-3`) the sectors `0,1,2` are pairwise at offsets `1,1,2`,
so `sigma(0), sigma(1), sigma(2)` must be pairwise disjoint. For `m = 3` (`n = 18`, offsets
`+-2,+-3,+-4`) the sectors `0,2,4` are pairwise at offsets `2,2,4`, same conclusion. But three
pairwise disjoint admissible palettes avoiding `0` would be three disjoint subsets of the 5-element
set `{1,...,5}` of size `>= 2` — impossible. `square`

(In particular triples do not help: a triple and its complement pair are the largest pairwise
disjoint family in the full admissible domain.)

### 1c. `m = 4`: retraction to `C_5` and an arithmetic contradiction

For `m = 4`, `n = 24`, offsets `{+-3,+-4,+-5}`. Consider the eight consecutive sectors
`Z = {16,...,23}`. Since all differences inside `Z` are `1..7`, the induced constraint graph is the
circulant on `Z_8` with steps `3,4,5 = 3,4,-3`: the cubic circulant `C_8(3,4)` (the Wagner graph).

**(i) Every value with a partner retracts to the 5-cycle.** Define `r` on the admissible domain
avoiding `0` by `r(A)=A, r(E)=E, r(B)=B, r(F)=F, r(D)=D, r(C)=A` (so `r` on the five pairs
`A,E,B,F,D` is the identity of the 5-cycle `A-E-B-F-D-A`, and `r(C) = A` is adjacent to `r(D)=D`),
and for a triple `T` let `r(T)` be any vertex of the 5-cycle adjacent to `r(p)` where `p` is the
unique value compatible with `T` (a triple `T sub {1,...,5}` is compatible exactly with the pair
`{1,...,5} \ T`, if that pair is admissible). Then `r` is a graph homomorphism of the disjointness
graph into `C_5`: every value other than the four isolated triples (which have no compatible value,
hence never appear: every sector has six partners) has all of its (one or more) neighbours
`X` mapped consistently, because for a triple the condition is exactly `r(T) ~ r(p)`. Composing a
word with `r` therefore gives

    psi : Z_8 -> Z_5  with  psi(i+3) - psi(i) in {+-1}  and  psi(i+4) - psi(i) in {+-1}   (mod 5).

**(ii) No such psi exists.** Put `alpha_i = psi(i+3)-psi(i)` and `beta_i = psi(i+4)-psi(i)`,
both in `{1,-1} sub Z_5`. Summing four steps of 3 and using `12 = 4` in `Z_8`:

    alpha_i + alpha_{i+1} + alpha_{i+3} + alpha_{i+6} = psi(i+12) - psi(i)
                                                     = psi(i+4) - psi(i) = beta_i.

The left side is a sum of four elements of `{1,-1}`, i.e. an integer in `{-4,-2,0,2,4}`, and must be
`+-1` mod 5; the only possibilities are `+-4`, so all four alphas are equal and `beta_i = -alpha_i`.
Varying `i` gives `alpha_0 = alpha_1 = alpha_3 = alpha_6`, `alpha_2 = alpha_3 = alpha_5 = alpha_0`,
`alpha_4 = alpha_5 = alpha_7 = alpha_2`, so `alpha_i = alpha` for all `i` and `beta_i = -alpha` for
all `i`. Then

    0 = psi(i+8) - psi(i) = beta_i + beta_{i+4} = -2 alpha  != 0  in Z_5,

since `alpha = +-1`. Contradiction. `square`

### 1d. `m = 1` is infeasible

For `m = 1`: `Delta = pi/3` and `d_0 = pi/9`, and the offset `m-1 = 0` is realisable (a deviation
of at most `1.5938 d_0 = 0.53 Delta` can move the image direction back into the sector of `f`), so
the constraint set is `{0,+-1,+-2}`; offset `0` asks a palette to be disjoint from itself. Even the
reduced set `{+-1,+-2}` is unsatisfiable (verified by exhaustive search, `work/`): the transport
graph is then the octahedron `K_{2,2,2}`. So no sector model exists at `m = 1` either.

### 1e. Independent machine checks

`work/classify.py` decides (T) for `m = 2..30` by two independent complete procedures —
exhaustive backtracking with arc consistency and symmetry breaking (`work/generic.py:decide_dfs`,
node counts 1,1,3 for `m = 2,3,4`, and `<= 32` for `m <= 12`), and CaDiCaL on the obvious CNF
(`decide_sat`) — with the explicit word as a third determination. All three agree:
`UNSAT, UNSAT, UNSAT, SAT, SAT, ...` for `m = 2,3,4,5,6,...`, for the pair domain and for the
pairs+triples domain. The certificate for `m = 5,6,9,12,15,18` is `cert/sector_words.json`,
re-verified by `work/verify_cert.py` along two independent code paths.

---

## 2. The model is a countermodel to the palette-level route, and to nothing else

### 2a. THEOREM 2 (centre-independence is already impossible for a colouring)

The paper's Lemma 5.2(3) has no distance restriction, and it records the instance

    (x + a) + f = x + f + a       (s(f) = f, t(f) = a, admissible off f = +-a).

So for a weak measurable 6-colouring `c` with maximal palette field `P`, **for every unit vector
`t` and a.e. direction `f`**

  (S2) `P_{x+t}(f) cap P_x(f) = empty`.

Consequently a palette field that does not depend on the centre (`P_z = sigma` for all `z`) cannot
be the maximal palette field of any weak measurable colouring — proper *or improper* — unless
`sigma(f) = empty` a.e.: (S2) reads `sigma(f) cap sigma(f) = empty`. In particular **every**
free-label sector model of Theorem 1, at every `m >= 5` and with any free-label function, is not
induced by a colouring.

This is a correction of emphasis to the record's frontier statement ("the only constraint the
models fail is trace-consistency with a proper colouring"): properness is not what kills them.
What kills them is a palette-level constraint of the paper, (S2), which holds for *every*
colouring, and which any centre-independent field violates at once. The models satisfy the
`d_0`-restricted instances of (5.3) only because those instances always move the direction by
`~pi/3`; the same-direction instance at unit centre distance is not among them, and it cannot be
added.

### 2b. THEOREM 3 (support rigidity — a second, independent obstruction)

For any weak measurable colouring `c` and its maximal palette field `P`:

  (S1) for **every** centre `x` and a.e. direction `e`: `c(x+e) in P_x(e)`.

*Proof.* By Definition 5.1 a trace at `x` is a weak-* limit of `e' |-> (a_i(y_n + r_n e'))` with
`y_n -> x`, `r_n -> 1` typical circle samplings. Take `r_n = 1` and `y_n -> x` through typical
centres; for a.e. `e'` the point `x + e'` is typical, so `a_i(y_n + e') -> a_i(x+e')` pointwise
a.e. and the limit trace has `b_i = 1` on `{e' : c(x+e') = i}`. Hence `i in D_{x,i}` a.e. on that
set, i.e. `i in P_x(e')`. `square`

**Corollary 3.** Suppose `P_x = sigma` for a.e. `x` on the unit circle `Gamma_y` around some point
`y` (in particular, suppose the field is centre-independent on a disc of radius `> 1`). Then
`c(y) in intersection_e sigma(e)`. So if the total intersection of the values is empty — in
particular if `sigma` takes two *disjoint* values, or all six values of Theorem 1 — then `P` is the
maximal palette field of no weak measurable colouring.

*Proof.* Measurability of `{(x,e) : c(x+e) notin sigma(e)}` and Fubini give nullity of that set
(the `sigma`-slices are null by (S1)); then for a.e. `x in Gamma_y` and a.e. `e`,
`c(y) = c(x + (y-x)) in sigma((y-x)/|y-x|)`, and `x |-> (y-x)/|y-x|` maps `Gamma_y` onto `S`. `square`

So the models fail (S1) and (S2), two colouring-level necessary conditions. Both are of the
"trace-consistency/maximality" type; neither is properness.

### 2c. Answer to "can the free label vary with the centre?"

It can, in principle, but it does not matter: such a field is not a counterexample to local
finiteness. To be induced by a colouring a palette field has to satisfy (S1) **and** (S2); these
are not reachable by any centre-independent or sector-by-sector design, and (S1)+(S2)+(5.7)+(5.3)
is exactly the paper's setting. So the varying-free-label construction, if it exists, changes
nothing in the status of `(W)`, and if it does not exist, nothing is lost. The free-label family is
therefore closed off as a route to a six-colouring, and what it does prove — that no proof of
local finiteness can use only the palette axioms plus non-proper self-avoidance — is exactly
Theorem 1's content, now decided for every `m`.

---

## 3. Vacuity and non-vacuity: k = 5 and k = 7

**k = 5 (`ell = 5`, the longest cycle in 5 labels).** Palette bound `|P| <= 2` (Prop 5.6).
Admissible pairs avoiding `0`: `{1,3}, {1,4}, {2,4}`, and the only disjoint pair is
`{1,3}--{2,4}`; `{1,4}` has no partner at all. So a word must alternate `{1,3}` and `{2,4}` at all
six offsets — a proper 2-colouring of the transport graph `C_{6m}(+-(m-1),+-m,+-(m+1))`. That graph
is connected (`gcd(m-1,m,m+1) = 1`) and vertex-transitive, so it is bipartite iff all its offsets
are odd; but `m-1, m, m+1` are three consecutive integers, never all odd. **Hence at `k = 5` the
analogous free-label system is UNSAT for every `m >= 2`** (`work/contrast.py`, both procedures and
an explicit bipartiteness test, `m = 2..30`). This is consistent with, and explains, the paper's
local finiteness theorem at `k = 5`: the free-label route is a `k >= 6` phenomenon.

**k = 7 (`ell = 6`).** Three pairwise disjoint admissible palettes leave `k - 3 = 4` free labels, so
the `m15` 3-block word `M_0={1,3}, M_1={2,4}, M_2={5,6}` with `L = 2m/3` (`3 | m`) is a
free-label model at `k = 7` (checked for `m = 6` by `work/contrast.py`). This is non-vacuous: `m3`
has a genuine proper measurable 7-colouring with a non-locally-finite cyclic locus, so a `k = 7`
palette model is exactly what one expects, and the `k = 6` obstruction (three disjoint admissible
pairs must cover all six labels) is genuinely `k = 6`-specific.

---

## 4. What is claimed and what is not

Claimed and checked: Theorem 1 (all `m`, all admissible palette sizes, hand proof both directions
plus two independent complete decision procedures); the explicit certificate; the exact rational
GEOM chain; (S1), (S2) and their corollaries; the `k = 5` no-go; the `k = 7` positive contrast.

Not claimed: anything about `(W)` (local finiteness at `k = 6`); anything about general measurable
translation-invariant fields that are not sector-constant (Theorem 1 is a statement about sector
words, which is the class of every countermodel in the record — a non-sector field could in
principle do better on small `m`, but by Theorem 2 no centre-independent field is colouring-induced
anyway, so this cannot produce a six-colouring); and nothing about colourings with varying palette
fields, which is the open problem itself.

One quantitative remark on how much of (5.3) the models satisfy: the radius used in the record,
`d_0 = Delta/3`, is not optimal for the sector class. Disjointness at the six offsets follows from
any `rho` with `arcsin rho + rho/sqrt(4-(1+rho)^2) < Delta` (exactly the requirement that the image
direction not leave the neighbouring sector); that sufficient condition allows `rho` up to
`0.622 Delta = 1.865 d_0` at `m = 5` (`0.629 Delta = 1.888 d_0` as `m -> infinity`). It cannot be
pushed to `rho = 1`, by Theorem 2. The true optimum is larger still (the sampled deviation ratio is
`1.169`, not `1.577`), and we have not determined it.
