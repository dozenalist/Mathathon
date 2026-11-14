# The triangle case of Theorem 6.5 does not generalise to six colours: an exact analytic counter-model

m13, swarm `smwfo9zkl`, direction d5 (triangle locus at k = 6).
Files: `no-go.md` (this file), `alpha_bounds.py`, `model_check2.py`, `structural_check.py`,
`run_all.sh`, `run_all.log`.

**Result in one line.** The hypothesis list that the paper's triangle case of Theorem 6.5 actually
uses — `(6.2)` for the three edges of a triangle `T`, the palette bound `|P_x| <= k-3`, the
sixty-degree exclusion `(5.7)`, and the *exact analytic* two-centre transport `(5.3)` at every
distance `<= eps` — has no member with two triangle centres at distance `< min(delta_*, eps)` when
`k = 5` (this is precisely the printed proof), and has a member whose triangle locus is **the whole
plane** when `k = 6`. The member is explicit and closed-form:

```text
  s(t) = floor(9t/(2 pi)) mod 3 in Z/3,        Q_0 = {1,4}, Q_1 = {2,5}, Q_2 = {3,6},
  P_z(e^{it}) = Q_{s(t)}      for every centre z in R^2, every direction e^{it}.          (M')
```

Every palette has two labels, meets `T = {1,2,3}` and meets `O = {4,5,6}`, palettes of different
colour are disjoint, and the model satisfies every palette-level consequence of the paper's
hypotheses. So the printed triangle case is a `k <= 5` statement in the precise sense that its
hypotheses do not imply its conclusion at `k = 6` — and in particular the "3-ary separation"
statement recorded as the missing lemma in `.ultramath/smwfcr56i/m2/k6_nogo.md` (N1) is not
derivable from those hypotheses; it is false for (M').

A second, degenerate model (M) of the same shape — `P_z(e^{it}) = {4 + s(t)}`, singletons inside `O` —
satisfies (5.2) itself, in the form "there is a function `c` with `c(x+e+v) ∉ P_x(e) ∪ P_x(v)`"
(namely `c ≡ 1`), with no local finiteness. So the only ingredient of the paper's hypotheses that
(M) fails is the *maximality* of the palettes, i.e. exactly the link between the palettes and a proper
colouring.

---

## 0. Results

Notation: `I = {1,...,k}` labels, `S = S^1` with angular probability `sigma`, `R` = rotation by
`kappa = pi/3`, `P_x(e) subset I` a palette, `T = {1,2,3}` a fixed triangle, `O = I \ T`.

**Definition 0.1 (the class `P(k, eps)`).** Fix `k >= 3`, a three-element `T subset I` and
`0 < eps < 1/2`. A member of `P(k, eps)` is `(Z, P, W)` with `Z subset R^2` a set of centres,
`P_z : S -> 2^I \ {emptyset}` measurable for `z in Z`, and `W_z` a set of measurable
probability-vector functions on `S`, such that

* **(P1)** `1 <= |P_z(e)| <= k-3` for almost every `e`;
* **(P2)** `P_z(e) ∩ P_z(Re) = empty` for almost every `e`   [the paper's (5.7)];
* **(P3)** for all distinct `z, z' in Z` with `|z - z'| <= eps` and almost every unit vector `w`:
  if `s, t' in S` and `s + t' = (z' - z) + w`, then `P_{z'}(w) ∩ P_z(s) = empty` and
  `P_{z'}(w) ∩ P_z(t') = empty`   [the paper's (5.3), in the exact form used by Lemma 5.5];
* **(P4)** `P_z(e)` is not contained in `{1,2}`, `{1,3}` or `{2,3}`, for almost every `e`
  [the paper's (6.2) for the three triangle edges];
* **(P5)** for each edge `{i,j}` of `T` there is `b in W_z` with `b_i = b_j = 0` a.e., and every
  `b in W_z` has `supp b subseteq P_z` a.e.   [Lemma 6.2];
* **(P6)** for `k = 6` only: no two complementary three-element sets both occur with positive
  angular measure at the same centre   [the palette-level content of (5.2) at `k = 6`];
* **(P7)** there is a function `c : R^2 -> I` such that for every `z in Z` and almost every
  `(e,v) in S x S`:  `c(z + e + v) ∉ P_z(e) ∪ P_z(v)`   [the paper's (5.2), with the colouring
  kept as an unconstrained function — every genuine palette system satisfies it with `c` the
  colouring].

A point `z in Z` is a **`T`-triangle point** of the member if (P4) and (P5) hold at `z`; it is
**`T`-ary** if `P_z(e) ∩ T != empty` for almost every `e`. The `T`-triangle locus is the set of
`T`-triangle points.

**Theorem 1 (`k = 5`: the printed argument is a theorem about `P(5, eps)`).** Let `(Z,P,W)` be in
`P(5, eps)` and let `delta_* > 0` be the absolute constant of the paper's Lemma 5.5. Then any two
distinct `T`-triangle points of the member are at distance `>= min(delta_*, eps)`.

**Theorem 2 (`k = 6`: the conclusion fails, explicitly).** Let `eps = 1/50`. With
`s(t) = floor(9t/(2 pi)) mod 3` and `Q_0 = {1,4}, Q_1 = {2,5}, Q_2 = {3,6}`, the following two
triples are members of `P(6, 1/50)`:

```text
  (M')  Z = R^2,  P_z(e^{it}) = Q_{s(t)}          (two labels per palette, T-ary everywhere),
  (M)   Z = R^2,  P_z(e^{it}) = {4 + s(t)}         (singleton palettes inside O),
```

and `W_z` is, in each case, the set of measurable probability vectors supported in `P_z(.)`. Both
satisfy **(P6)**; (M) satisfies **(P7)** with `c ≡ 1`; (M') additionally satisfies, at every
direction, `|P| = 2`, `P ∩ T != empty` and `P ∩ O != empty`. In **both** models every point of the
plane is a `T`-triangle point, and in (M') every point is `T`-ary. Consequently, in `P(6, 1/50)` the
`T`-triangle locus can be the whole plane, the `T`-ary set can be the whole plane, and distinct
`T`-ary points need not be separated at all.

*(Inspection of (P7) for (M): its palettes are singletons inside `O = {4,5,6}`, and `c ≡ 1`, so
`c(z+e+v) = 1 ∉ P(e) ∪ P(v)` holds identically. For (M'): at a fixed point `z` the pairs decomposing
`z - x` as `x` runs over a neighbourhood of `z` realise all three unions `Q_0 ∪ Q_1`, `Q_0 ∪ Q_2`,
`Q_1 ∪ Q_2`, whose union is `I`, so (M') is *not* (P7)-completable with `Z = R^2`
(`structural_check.py` S4b); this is why both witnesses are stated.)*

**Corollary 3 (the exact step that fails at `k = 6`; the `|P| <= 2` dependence is essential).** The
printed triangle case of Theorem 6.5 — *"(6.2) for its three edges and Proposition 5.6 force `P_x` to
meet the outside pair; (5.7) makes the intersection a singleton, alternating; so `x` is binary for
that pair; Lemma 5.5 gives local finiteness"* — is a theorem about `P(5, eps)` and nothing weaker: its
hypotheses are (P1)–(P5) (Theorem 1). At `k = 6` those same hypotheses admit (M'), where there is no
separation whatsoever (Theorem 2). Hence the triangle case at `k = 6` needs an input that is **not** a
palette-level consequence of the paper's hypotheses. In the wording of the sprint brief: the triangle
case's dependence on `|P| <= 2` is *essential* — it cannot be replaced by any combination of
(P1)–(P6), the palette bound `|P| <= 3`, the extra conditions `|P| >= 2`, `P ∩ T != empty`,
`P ∩ O != empty`, or the ternary bound `sigma{|P| = 3} <= pi/3` of `smwfk0ybk/m6` (Theorem 2's model
satisfies them all).

**Corollary 4 (what a `k = 6` proof must supply — and how sharp (M') is).** In `P(k, eps)`, if there
is a **fixed** pair `{a,b} subset I` such that every `T`-triangle point is binary for `{a,b}`
(`P_z(e) ∩ {a,b} != empty` a.e.), then the `T`-triangle locus is `min(delta_*,eps)`-separated
(Lemma 5.5). Model (M') violates this for all `15` pairs, since `Q_0,Q_1,Q_2` partition `I` and a
two-element `{a,b}` can meet at most two of them. Moreover (M') satisfies, in addition to (P1)–(P6),
the palette-level conditions

```text
  |P_x(e)| >= 2 ,    P_x(e) ∩ T != empty ,    P_x(e) ∩ O != empty ,
  P_x(e) not a subset of O ,    P_x(e) not a singleton ,
```

so none of those is a usable repair either. **The only palette-level hypotheses that kill (M') are
ones that exclude the matched pairs `{1,4},{2,5},{3,6}` from being the palette at every direction** —
e.g. a fixed-pair binarity condition, or a condition forcing `|P| = 3` on a set of positive measure,
or a condition restricting which labels a palette may hold. None of these is derivable from the
paper's hypotheses (each is violated by (M')), so a `k = 6` proof must use colouring-level input.

**What is not claimed.** Neither model is the maximal-palette system of a colouring, and Theorem 2
does not assert that a weak measurable 6-colouring has a non-locally-finite triangle locus (that is
open). It asserts that the local-finiteness conclusion is not *derivable* from the printed
hypotheses: everything in the paper's §5–§6 that is a consequence of those hypotheses *and does not
use maximality* is satisfied by (M) or by (M'), one of the two. See §5 for the delimitation and the
vacuity test.

---

## 1. Why `P(k, eps)` is the class that matters

The paper's triangle case (p. 38) reads, verbatim:

> For a triangle, (6.2) for its three edges and Proposition 5.6 force `P_x(e)` to intersect the pair
> of outside labels almost everywhere. Indeed, a nonempty subset of the three triangle labels of
> size at most two lies in some triangle edge, which is forbidden. By (5.7) the intersection with the
> outside pair is unique almost everywhere and alternates under `R`. Thus every such `x` is binary
> for that fixed pair. Lemma 5.5 proves local finiteness of the triangle locus.

Its hypotheses, item by item:

| printed ingredient | in the class as |
|---|---|
| `ij in Gamma_x` for the three edges, used only through (6.2) | (P4) with (P5) |
| Proposition 5.6, `1 <= |P_x(e)| <= 2` | (P1) at `k = 5` |
| (5.7) | (P2) |
| Lemma 5.5, whose input is `P_y(e^{it}) ∩ P_x(e^{i alpha_pm(t)}) = empty` | (P3) |

Moreover:

1. **Each (Pi) is a consequence of the paper's hypotheses.** (P1) is the general-`k` palette bound
   (`results/K6-BARRIER.md` §1; Proposition 5.6 when `k = 5`). (P2) is Corollary 5.4. (P3) is
   Lemma 5.2(3) together with the two-angle decomposition used in Lemma 5.5's proof. (P4)+(P5) are
   Lemma 6.2 with (6.2). (P6): at `k = 6` with `|P| <= 3`, `P(e) ∪ P(v) = I` holds exactly for
   complementary triples, so the colouring statement (5.2), `c(x+e+v) in I \ (P(e) ∪ P(v))`, has
   exactly (P6) as its palette-level content and nothing else.
2. **Lemma 5.5's proof does not use anything else.** Its key step
   `s_x(alpha_+(t)) = s_x(alpha_-(t)) = -s_y(t)` uses only that the two centres are binary for the
   same fixed pair and the transport exclusions; the expansions (5.9)–(5.11) and the
   bounded-distortion argument are properties of `Theta_d, alpha_pm` alone. Hence `delta_*` is
   available inside `P(k, eps)` verbatim, which is what makes Theorem 1 a theorem about the class
   and not about colourings.
3. **(P5) is not vacuous in the interesting model.** In (M') the trace for the edge `{i,j}` is the
   uniform vector on `P_z(e) \ {i,j}`, a nonempty set by (P4); see `model_check2.py`, check G.

---

## 2. The two-angle maps: Proposition 3.1

**Proposition 3.1.** Let `0 < d <= 1/2`, `t in R`, `Theta_d(t) = t + arg(1 + d e^{-it})`,
`rho(t) = |d + e^{it}|` and `alpha_pm(t) = Theta_d(t) +/- arccos(rho(t)/2)`. Then

```text
   d + e^{it} = e^{i alpha_+(t)} + e^{i alpha_-(t)},                                     (2ang)
   | alpha_pm(t) - (t +/- pi/3) | <= 4 d      for every t.                              (3.1)
```

*Proof.* (2ang) is the paper's identity (p. 30); `alpha_bounds.py` verifies the residual
`< 1e-15` for `d in {0.001,0.01,0.05,0.1,0.25,0.49}` and `2.10^4` angles. For (3.1), put
`z = d e^{-it}`. Then `Re(1+z) = 1 + d cos t >= 1 - d > 0`, and

* `|arg(1+z)| <= arctan(|z|/(1-|z|)) <= d/(1-d) <= 2d` for `d <= 1/2`;
* `rho^2 = 1 + 2d cos t + d^2`, so `|rho^2 - 1| <= 2d + d^2` and, since `rho + 1 >= 2 - d >= 3/2`,
  `|rho - 1| <= (2d + d^2)/(3/2) <= 1.7 d`;
* `u |-> arccos u` has derivative `-1/sqrt(1-u^2)` and `rho/2 in [1/4,3/4]`, so
  `|arccos(rho/2) - arccos(1/2)| <= (4/sqrt 7)|rho/2 - 1/2| = (2/sqrt 7)|rho - 1| <= 0.76|rho-1|`.

Adding: `<= 2d + 0.76 * 1.7 d <= 3.3 d <= 4d`. `square`

*(`alpha_bounds.py` recomputes the three constants from the formulas (`1.047`, `1.000`, `0.649`), and
the supremum of the deviation ratio over `d in (0,0.49]` and `60001` angles is `1.294`, with
`mpmath.iv` interval enclosures as an independent path. The bound `4d` is chosen because it is
proved, not because it is tight.)*

**Rotation equivariance.** For `z' - z = d e^{i theta}` and `w = e^{i tau}`, rotate by `-theta`:
`d + e^{i(tau-theta)} = e^{i alpha_+} + e^{i alpha_-}`, so the two unit vectors `s, t'` with
`s + t' = (z'-z) + w` are `e^{i(theta + alpha_pm(tau - theta))}` and

```text
   arg(s) - tau = alpha_pm(tau - theta) - (tau - theta) = +/- pi/3 + xi,    |xi| <= 4 d.     (3.2)
```

**Proposition 3.2 (shift lemma).** Let `s(t) = floor(9t/(2 pi)) mod 3`.

1. `s(t + 2 pi) = s(t)` for every `t` (`floor(9(t+2pi)/(2pi)) = floor(9t/(2pi)) + 9`, and `9 = 0`
   mod `3`), so `s` descends to a measurable `S -> Z/3`; its step length is `2pi/9` and its period
   is `2pi/3`.
2. If `9b/(2 pi) in (1,2) ∪ (-2,-1)` then `s(t+b) != s(t)` for **every** `t`.
3. Hence if `|b -/+ pi/3| <= 4/50` then `s(t+b) != s(t)` for every `t`.

*Proof.* Put `u = 9t/(2pi)`, `beta = 9b/(2pi)`, and write `u = n + x` with `n = floor(u) in Z`,
`x in [0,1)`. Then `floor(u+beta) - floor(u) = floor(x+beta)`. If `beta in (1,2)` then
`x + beta in [1,3)`, so the increment is `1` or `2`; if `beta in (-2,-1)` then `x + beta in (-2,1)`,
so the increment is `-2` or `-1`. In neither case is the increment `0 mod 3`, and
`s(t+b) - s(t) = floor(u+beta) - floor(u)` mod `3`. For (3): `|b -/+ pi/3| <= 4/50` gives
`beta in [1.5 - 9*0.08/(2pi), 1.5 + 9*0.08/(2pi)] = [1.3848, 1.6152] subset (1,2)` for one sign and
the mirror interval `subset (-2,-1)` for the other. `square`

`model_check2.py` check F redoes both intervals in exact rational arithmetic, with
`333/106 < pi < 22/7`, so part 3 does not rest on floating point.

---

## 3. Proof of Theorem 2

Let `Z = R^2`, `P_z(e^{it}) = Q_{s(t)}` with `s` as in Proposition 3.2 and
`Q_0 = {1,4}, Q_1 = {2,5}, Q_2 = {3,6}`, and let `W_z` be the measurable probability vectors
supported in `P_z(.)`.

* **(P1)** `|P_z| = 2 <= 3`. `square`
* **(P2)** `P_z(e) ∩ P_z(Re)` is nonempty only if `s(t) = s(t + pi/3)`, and `|(pi/3) - (pi/3)| = 0`,
  so Proposition 3.2(3) applies with `b = pi/3`: the step indices differ, and different `Q`'s are
  disjoint. So the intersection is empty for **every** `t`. `square`
* **(P3)** Let `z != z'`, `d = |z'-z| <= 1/50`, `w = e^{i tau}`, and `s + t' = (z'-z) + w` with
  `s, t' in S`. By (3.2), `arg s - tau = pi/3 + xi` and `arg t' - tau = -pi/3 + xi'` with
  `|xi|, |xi'| <= 4d <= 4/50`. By Proposition 3.2(3), `s(tau) != s(arg s)` and
  `s(tau) != s(arg t')`; distinct step indices carry disjoint palettes, so
  `P_{z'}(w) ∩ P_z(s) = empty` and `P_{z'}(w) ∩ P_z(t') = empty`. `square`
* **(P4)** `Q_j ∩ T = {j+1}` and `Q_j ∩ O = {j+4}`, so `Q_j` is contained in none of `{1,2}`,
  `{1,3}`, `{2,3}`. `square`
* **(P5)** For the edge `{i,j}`, `Q_m \ {i,j}` is nonempty (it contains one element of `T` and one of
  `O`, and `{i,j} subset T`), so the uniform vector on it is a trace supported in the palette with
  zero `i`- and `j`-coordinates, measurably in `t`. `square`
* **(P6)** No palette has three elements. `square`
* **(P7)** For (M): `P_z(e) ⊆ O` and `c ≡ 1 ∉ O`, so `c(z+e+v) ∉ P_z(e) ∪ P_z(v)` holds for all
  `(e,v)`. For (M') we do **not** claim (P7) (see §5(f)). `square`

Everything holds for **every** `t` (not merely almost everywhere), so the model is insensitive to the
choice of null sets, and (P3) is asserted for the *exact* maps of the paper rather than for
approximations. Every `z in R^2` is a `T`-triangle point and is `T`-ary, so the `T`-triangle locus of
this member is the whole plane. `square`

**Numerical corroboration** (`model_check2.py`, two independent code paths; both models):

```text
  (M') T-ary pair model          (M) singleton variant
  C  (5.7), 200000 directions        0 violations      0 violations
  A  transport, general decomposition, 80000 random checks   0 violations, max dev 0.0231
  B  transport, paper's alpha_pm,      60000 random checks   0 violations, max dev 0.0231
  D/E palette bound + (6.2) + T-arity + "P meets O"          0 violations
  G  traces (P5) for all three edges                         0 violations
  F  exact rational band check, beta in [1.3848, 1.6152]     0 violations
  H  the k = 5 analogue fails (agreement set of measure 0.5491 for some shift near pi/3)
```

`max dev 0.0231` is `<= 4 d` for every drawn `d <= 1/50`, as required.

---

## 4. Proof of Theorem 1, and Corollary 4

**Theorem 1.** Let `(Z,P,W) in P(5,eps)` and `z in Z`. By (P1) `|P_z(e)| <= 2` a.e.; by (P4) the
palette is contained in none of `{1,2}`, `{1,3}`, `{2,3}`. A nonempty subset of `T = {1,2,3}` of
size at most two *is* contained in one of those pairs, so `P_z(e) ∩ {4,5} != empty` a.e., i.e. `z` is
binary for `{4,5}`. Lemma 5.5 then applies to any two such centres — its proof uses only binarity for
the fixed pair, (P2) and (P3), the expansions being properties of the maps — and gives separation
`>= min(delta_*, eps)`. `square`

`structural_check.py` S1 verifies the combinatorial step exhaustively: at `k = 5` there are `9`
palettes with `1 <= |P| <= 2` not contained in a triangle edge, and **all 9** meet `{4,5}`.

**Corollary 4.** Binarity for a fixed pair plus (P2)+(P3) is exactly the hypothesis of Lemma 5.5, so
it gives separation. In (M') the palettes are the three members of a partition of `I` into pairs, and
a fixed two-element `{a,b}` misses at least one of them (it is disjoint from the pair containing
neither of its labels); hence no fixed pair is binary, and Corollary 4's hypothesis fails in (M').
`structural_check.py` S3 records this together with the other candidate hypotheses.

---

## 5. Delimitation, vacuity test, and the recorded item (N1)

**(a) What `P` does not contain.** `P(k,eps)` contains (5.2) in the form (P7), with `c` an
unconstrained function, and it contains the whole palette-level content of (5.2) as (P6). What it
does **not** contain is the *maximality* of the palettes (Definition 5.1) — the statement that `P_x(e)`
contains every label that can appear on a unit circle at `x` in direction `e`. Maximality is what
makes (5.2) strong, and it cannot be imposed without a proper colouring: imposing it would make the
class equivalent to "there is a six-colouring". So Theorem 2 delimits exactly: *the triangle case of
Theorem 6.5 is not derivable from anything in §5–§6 except maximality.*

**(b) The models are not colourings.** (M) and (M') cannot be the maximal-palette systems of a weak
measurable colouring, since that would be a six-colouring of the plane. In (M)'s case the failure is
visible in the witness `c ≡ 1` of (P7): a colouring cannot be constant. This is not a defect of the
construction — it is the content of Corollary 4: the missing input is the colouring itself.

**(c) Vacuity test.** A no-go is vacuous if the same argument also kills a case known to exist. Here
the opposite happens: at `k = 5` the class `P(5,eps)` **is** strong enough to prove the paper's
theorem (Theorem 1, via the paper's own Lemma 5.5), and at `k = 4` it is stronger still. So the class
decides the triangle case at `k = 5` and fails to decide it at `k = 6`: the threshold is real, and it
sits exactly at the step where "a subset of `T` of size `<= 2` lies in an edge" needs
`|T^c| = 2 = k - 3`.

**(d) Relation to (N1) of `.ultramath/smwfcr56i/m2/k6_nogo.md`.** That note isolates the missing
statement at `k = 6` as: *"for every fixed 3-element `T` there is `delta_T > 0` such that two distinct
centres that are `T`-ary are at distance `>= delta_T`"*. Model (M') is `T`-ary at **every** point of
the plane, so (N1) is false for `P(6,1/50)`: it is not a consequence of the palette-level hypotheses
and cannot serve as the missing lemma in that form. (Whether (N1) holds for genuine colourings
remains open, together with the rest of the `k = 6` problem.)

**(e) What would repair it.** By Corollary 4 and (M'), the only palette-level repairs are hypotheses
that exclude the matched partition `{1,4},{2,5},{3,6}` at a triangle centre: (i) a **fixed** pair
`{a,b}` that is binary at every triangle centre; (ii) a condition forcing `|P_x(e)| = 3` on a set of
positive angular measure (note that `|P| <= 2` alone does not help — (M') has `|P| = 2` everywhere);
(iii) a condition restricting which labels a palette may hold (note that
`P_x(e) ∩ T != empty` **and** `P_x(e) ∩ O != empty` together do *not* suffice — (M') satisfies
both). Every such condition is violated by (M'), hence none is derivable from the paper's
hypotheses, so a `k = 6` triangle proof must bring in the colouring. This also independently confirms
item S8 of `.ultramath/smwfk0ybk/m3/RESULTS.md` §5 ("a replacement must be violated by all-singleton
palettes drawn from the outsiders"): that family survives even the full analytic two-centre transport
(model (M)), and so does the larger matched-pair family (M').

**(f) How (M) and (M') stand with respect to (5.2) itself.** (P7) is satisfied by (M) with `c ≡ 1`,
because its palette classes occupy only the three labels of `O`: no constraint ever forbids a label of
`T`. (M') is different: its three colour classes are the matching pairs `Q_0,Q_1,Q_2`, so for two
directions in different classes the forbidden set `P(e) ∪ P(v)` is a 4-set, and — because at a fixed
point `z` the decompositions of `z - x` for `x` in a neighbourhood of `z` realise all three unions
`Q_0 ∪ Q_1`, `Q_0 ∪ Q_2`, `Q_1 ∪ Q_2` — the union of the constraints at one point is `I`. Hence (M')
admits no `c` at all when `Z = R^2` (`structural_check.py` S4b). The structural reason is a
two-versus-three tension worth recording:

* (P2) and (P3) force palettes of distinct classes to be disjoint along the `pi/3`-shift; with only
  two classes, "disjoint" means "different class", so the class function is a measurable
  two-colouring of the band graph and the argument of Lemma 5.5 (verbatim: replace the sign function
  by the class indicator) gives a contradiction on any centre set with pairs closer than `delta_*`.
  Hence at least three classes are needed.
* (P7) at a thick centre set forces the union of the realised pairwise unions `P(e) ∪ P(v)` to miss
  a label. Three pairwise disjoint classes of two labels each already exhaust `I`; three singleton
  classes must lie in `O` by (P4), which is exactly (M).

So a `k = 6` triangle-locus proof that uses (P7) *plus* the class conditions must exploit a
configuration that is neither `T`-ary (else (P7) fails at thick centre sets) nor singleton-in-`O`
(else (P4)-type information is unavailable). Deciding whether such a configuration exists with a
*thin, accumulating* centre set is left open here; it is the natural next step, and it is exactly
where the remaining gap between `P(6,eps)` and the colouring problem sits.

---

## 6. Reproduction

```text
cd .ultramath/smwfo9zkl/m13
bash run_all.sh            # about 60 s; writes run_all.log
```

* `alpha_bounds.py` — (2ang) residual; the deviation table (sup ratio `1.29` over
  `d in (0,0.49]`), an independent `mpmath.iv` enclosure path, and the three constants of
  Proposition 3.1.
* `model_check2.py` — checks A–H of §3 for both models (M') and (M): transport by the general
  decomposition and by the paper's `alpha_pm`; (5.7); the palette census and (6.2); the trace
  supports; the exact rational band check; and the failure of the two-valued (`k = 5`) analogue.
* `structural_check.py` — S1 (`k = 5` census: the combinatorial step of Theorem 1), S2 (`k = 6`
  census: 35 admissible palettes, 3/12/20 of sizes 1/2/3, 20 ordered complementary pairs = exactly
  what (P6) excludes), S3 (candidate extra hypotheses versus the models), S4/S4b ((P7): the forbidden
  sets of (M) at a single centre lie inside `O`, so `c ≡ 1` works; the forbidden sets of (M') at a
  single centre cover `I` once the centres fill a neighbourhood, so (M') is not (P7)-completable),
  S5 (finite shadow: 4 centres x 720 directions, 8640 constraints, 0 violations).
