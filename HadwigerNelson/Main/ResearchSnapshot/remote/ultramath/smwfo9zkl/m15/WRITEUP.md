# The six-cycle locus at k = 6 is not decided by the palette constraints

*Sprint B, direction d2. This note contains: a new k = 6 constraint (Lemma 2), an explicit
palette system with an infinite set of accumulating cycle centres for **every** cycle length
3,4,5,6 at k = 6 (Theorem 1, exact certificate), and a proof that the same constraint system is
unsatisfiable in the one case where the paper's §6.3 does decide by palette combinatorics alone
(Theorem 2). Consequence: local finiteness at k = 6, for any cycle length, cannot be proved from
the palette constraints; the trace families `W_x`, the density conclusion of Lemma 5.2(2) and the
supports `H_i` are essential. No claim is made about local finiteness itself.*

Everything is checked by `bash run_all.sh`.

---

## 1. The constraint system

Paper references are to `attachments/here-are-three-files-ni5n/paper.pdf`; `R` is rotation by
`pi/3`, `kappa = pi/3`, `I = {0,1,2,3,4,5}`, `P_x(e)` the maximal palette at centre `x` in
direction `e` (Definition 5.1), `Gamma_x` the transition graph (Definition 6.1),
`L = {x : Gamma_x contains a cycle}` (6.4).

Fix a simple cycle `C` of length `ell` on the labels `0,...,ell-1` in cyclic order (edges
`{i,i+1} mod ell`); the remaining labels are unused by `C`. Call

> `S` **admissible** if `1 <= |S| <= k-3` and `S` is contained in no edge of `C`.

A **`C`-palette system** is a measurable `P : R^2 x S^1 -> 2^I`, `z |-> P_z`, with `P_z(e)`
admissible for a.e. `e`. It is a `C`-palette system **at every point of a set `Y`**.

The following are necessary conditions for a `C`-centre of a weak measurable `k`-colouring, and
they are all that is used below.

| | statement | provenance |
|---|---|---|
| (P0) | `1 <= |P_x(e)| <= k-3` a.e. | general-k palette bound, `results/K6-BARRIER.md` §1 (paper Prop. 5.6 is the case `k=5`) |
| (P1) | `P_x(e) ⊄ {i,i+1}` for each cycle edge, a.e. | paper Lemma 6.2, equation (6.2) |
| (P2) | `P_x(e) ∩ P_x(Re) = ∅` a.e. | paper Cor. 5.4, equation (5.7) |
| (P3) | no two complementary 3-sets are both attained on positive-measure direction sets (`k=6`) | paper (5.2); see Lemma 2 |
| (P4) | **two-centre exclusion**: for distinct centres `z,z'` and a.e. `f`, `P_z(f) ∩ P_{z'}(s(f)) = ∅` for each exact unit decomposition `(z'-z) + f = s + t`, `|s| = |t| = 1` | paper Lemma 5.2(3), equation (5.3) |

**(P4) is where all the metric information sits.** For `|z'-z| = d < 1` the two solutions are
explicit:

$$w = (z'-z) + f,\quad r = |w|,\quad s_\pm(f) = \frac{w}{2} \pm i\,\frac{w}{r}\sqrt{1-\frac{r^2}{4}} ,$$

and `s_+ + t_- = s_- + t_+ = w` with `|t_\pm| = 1`. At `d = 0` this collapses to
`s_\pm = f\,e^{\pm i\kappa}`, i.e. (P2) is the `d -> 0` limit of (P4).

## 2. Lemma 2 (new constraint at k = 6)

> **Lemma 2.** Let `k = 6`. At any centre `x` and for any 3-element `A ⊂ I`, put
> `E_A = {e : P_x(e) = A}` and `E_{A^c} = {e : P_x(e) = A^c}`; at least one of the two is angular
> null. This is **(P3)**.

*Proof.* Suppose both have positive angular measure. By (5.2), `c(x+e+v) ∉ P_x(e) ∪ P_x(v)` for
a.e. independent-angle pair `(e,v)`. The exceptional set is angular-product null, the set of pairs
with `e ∥ v` is null, and `E_A x E_{A^c}` has positive product measure, so some pair
`(e,v) ∈ E_A x E_{A^c}` with `e ∦ v` is non-exceptional. At that pair
`P_x(e) ∪ P_x(v) = A ∪ A^c = I`, so no colour is available for the point `x+e+v`. ∎

At `k = 5` Lemma 2 is vacuous (`|P| <= 2`, so a union of two palettes has at most 4 < 5 labels).
At `k = 6` it bites. Two consequences used below:

* for a.e. `e` with `|P_x(e)| = 3` and value `A`, (P2) gives `P_x(Re) ⊆ A^c`, and (P3) rules out
  `P_x(Re) = A^c` on a set of positive measure, so `|P_x(Re)| <= 2` a.e.: **a triple forces a
  strict pair one `R`-step away**;
* a palette system never uses both members of a complementary triple pair.

(P3) is the *whole* palette-level content of (5.2): without modelling the colouring `c`, the only
information (5.2) carries about palettes is `P(e) ∪ P(v) ≠ I`.

## 3. Theorem 1: an accumulating `C`-palette system, for every cycle length, at k = 6

> **Theorem 1.** Let `k = 6` and `ell ∈ {3,4,5,6}`. There is a full-plane `C_ell`-palette system
> with (P0), (P1), (P2), (P3), (P4) at every point of an infinite set `Y` of centres accumulating
> at the origin. `Y` lies in a closed disc of radius `d0 = pi/(9m)` for every `m >= 6`, `3 | m`.

### 3.1 The construction

Labels `I = {0,...,5}`. Fix `m >= 6` with `3 | m`, put `n = 6m`, `Delta = 2 pi / n`,
`L = 2m/3`, and let sector `i` be `[i Delta, (i+1) Delta)`. Choose three **pairwise disjoint
admissible** palettes:

| `ell` | `A_0` | `A_1` | `A_2` |
|---|---|---|---|
| 6 | {0,3} | {1,4} | {2,5} |
| 5 | {0,2} | {1,3} | {5} |
| 4 | {0,2} | {4} | {5} |
| 3 | {3} | {4} | {5} |

and define, for every `z` in the plane,

$$\sigma(i) = A_{\lfloor i/L\rfloor \bmod 3},\qquad P_z(\theta) = \sigma\!\left(\left\lfloor \theta/\Delta \right\rfloor\right).$$

`P` is translation invariant, piecewise constant, measurable, and every value is a member of a
pairwise disjoint triple, so (P0) and (P1) hold by the table and (P3) holds because no value is a
3-set.

### 3.2 The block lemma

> **Lemma (block).** With `L = 2m/3`, for every `i ∈ Z/n` and every
> `t ∈ {±(m-1), ±m, ±(m+1)} (mod n)`, `floor((i+t)/L) - floor(i/L) ∈ {1,2}`, hence the two block
> indices differ mod 3 and the palettes are two different members of `{A_0,A_1,A_2}`.

*Proof.* Write `i = Lq + r`, `0 <= r < L`; then `floor((i+t)/L) = q + floor((r+t)/L)`.
For `t ∈ [m-1, m+1]` and `0 <= r < L` the quotient ranges over
`[floor((m-1)/L), floor((L+m)/L)]`. Now `floor((m-1)/L) = 1` exactly when `L <= m-1 < 2L`, and
`floor((L+m)/L) = 1 + floor(m/L) = 2` exactly when `L <= m < 2L`. For
`t ∈ {-(m+1), -m, -(m-1)}` the quotient ranges over `[floor(-(m+1)/L), floor((L-m)/L)]`, which
lies in `{-2,-1}` when `m > L` and `m+1 < 3L`. With `L = 2m/3` all four conditions read
`m >= 3`. Finally, if `i+t` leaves `[0,n)` the sector is reduced mod `n`, and
`n/L = 9` is an integer congruent to `0` mod 3, so the block index mod 3 is unchanged. Hence the
block lemma holds for every `m >= 3` with `3 | m`; the hypothesis `m >= 6` in Theorem 1 is only
what Lemma G's constants `1.6 / 0.66 / 1.69` require (`d0 <= pi/54`). Both the sharp condition and
the range are checked in `construction.py:block_inequality`. ∎

**(P2)** is the case `t = m`; **(P4)** is the case of all six offsets, once Lemma G below converts
the exact shift into a sector offset.

### 3.3 Lemma G (the geometric input), with proof

> **Lemma G.** Let `f = e^{i theta}` and let `delta` be complex with `|delta| = d <= d0 <= pi/54`.
> Then for each of the two first endpoints `s_pm` of `delta + f = s + t`:
> 1. `|arg s_pm - (theta ± kappa)| <= 1.6 d <= 1.6 d0 < Delta`;
> 2. `theta |-> arg s_pm` is a local diffeomorphism: `|d/dtheta (arg s_pm) - 1| <= 0.66`;
> 3. `|s_+ - s_-| >= 1.69`, so the two endpoints are never parallel.

*Proof.* `arg s_pm = arg w ± atan(sqrt(4-r^2)/r)` and `arg w - theta = arg(1 + delta/f)`.
(a) `1 + z` with `|z| <= d0` lies in the closed disc of centre 1 and radius `d0`, so
`|arg(1+z)| <= arcsin(d0) <= d0/sqrt(1-d0^2) <= 1.005 d0`. (b) `g(r) = atan(sqrt(4-r^2)/r)` has
`g(1) = pi/3` and `g'(r) = -1/sqrt(4-r^2)`, so `|g(r) - pi/3| <= d0/sqrt(4-(1+d0)^2) <= 0.592 d0`
by the mean value theorem, since `r ∈ [1-d0, 1+d0]`. Adding gives (1) with `1.597 < 1.6`; note
`1.6 d0 < Delta` because `d0 = pi/(9m)` and `Delta = pi/(3m)`. (c) With `z = delta/f`,
`d/dtheta arg(1+z) = Im[-iz/(1+z)]`, of modulus at most `d0/(1-d0)`, and `|dr/dtheta| <= 1`, so
`|d/dtheta(arg s_pm) - 1| <= d0/(1-d0) + 0.592 <= 0.653 < 0.66`. (d)
`|s_+ - s_-| = 2 sqrt(1-r^2/4) >= 2 sqrt(1-(1+d0)^2/4) >= 1.69` because `d0 <= pi/54`. ∎

The three numerical bounds (`1/sqrt(1-d0^2) <= 1.005`, `1/sqrt(4-(1+d0)^2) <= 0.592`,
`4(1-(1+d0)^2/4) >= 1.69^2`) are evaluated in `verify.py` in **exact rational arithmetic** using
`pi <= 22/7`, so no transcendental quantity is evaluated numerically.

### 3.4 Conclusion of Theorem 1

Let `Y = {y_k}` with `y_k = (d0/3) 2^{-k} u` for a fixed unit vector `u` (the palettes do not
depend on the centre, so the choice of `u` is irrelevant); `Y` is infinite, accumulates at the
origin, and has diameter `<= d0`. For `z ≠ z'` in `Y` apply Lemma G to
`delta = z'-z` and (P4): the two directions `f` and `s_±(f)` lie in sectors whose indices differ by
one of `±(m-1), ±m, ±(m+1)`, and by the block lemma the two palettes are different members of a
pairwise disjoint triple, hence disjoint. Since `P_z` is independent of `z`, this is exactly the
sector condition verified in `construction.py`. ∎

**Exact verification** (`construction.py`): for each of `ell = 3,4,5,6` and
`m = 6, 9, 12, 15, 21, 30, 60, 201, 600` (`n` up to 3600) every one of (P0),(P1),(P2),(P3),(P4)
and the block lemma is checked in integer arithmetic: **zero violations**. `verify.py` repeats
the check with independently written code (different data path, explicit while-loop schedule) and
carries the exact-rational Lemma G.

### 3.5 Corollary (the no-go)

> **Corollary 1.** Local finiteness of the `C_ell`-locus at `k = 6` is **not a consequence** of
> (P0)–(P4). Hence no proof of local finiteness at `k = 6`, for any `ell ∈ {3,4,5,6}`, can rest on
> the palette constraints and the two-centre exclusion alone.

The corollary is about the class of *all* systems satisfying (P0)–(P4): a single model of that
class violates local finiteness, and Theorem 1 supplies one — a sector system — so nothing is lost
by the piecewise-constant form of the construction. The class is stated exactly: **(P0)–(P4) as
listed in §1.**
Outside it lie, and are therefore *essential* to any k = 6 proof:

1. the definition (6.1) of `Gamma_x` itself (an area/limsup condition on the colouring, not a
   palette condition) — only its consequence (6.2) is in the class;
2. the trace families `W_x` of Definition 5.1 and the avoiding traces of Lemma 6.2 — used by the
   paper in Lemma 6.7 to ban steps;
3. the **density conclusion** of Lemma 5.2(2), which the 4-cycle transport rule of §6.3.2 uses
   explicitly ("the density consequence of Lemma 5.2 at `y` would then give density zero of `X`
   at the same spatial sum"), and which the 5-cycle argument of §6.3.3 uses through §6.3.3's
   trace construction;
4. the spatial essential supports `H_i` and their closedness.

## 4. Theorem 2: the same system does decide the one palette-level case, at k = 5

> **Theorem 2.** For `k = 5` and the triangle, the system (P0)–(P4) has **no** accumulating model,
> for every `m >= 2`. The proof is a two-colouring argument, and it is the palette-level content of
> the paper's §6.3 triangle proof (the only case in §6.3 that uses the palette constraints alone).

> **Lemma 3 (2-type obstruction).** Fix `k`, `C`, and a 2-set `{a,b} ⊂ I`. Suppose every
> *occurrable* admissible palette (one having a disjoint admissible partner) meets `{a,b}` in
> exactly one label. Then no accumulating sector model exists.

*Proof.* Put `type(i) = ` the unique element of `sigma(i) ∩ {a,b}`; disjointness forces
`type(i) ≠ type(j)`.
**Step 1** `type(i) = type(i+2)`: `i+m+1` is joined to both `i` and `i+2`, since
`(i+m+1) - i = m+1` and `(i+m+1) - (i+2) = m-1` both lie in `D`; both types differ from
`type(i+m+1)`, an element of a two-element set.
**Step 2** `m` even: `i` and `i+m` have the same parity, so `type(i) = type(i+m)` by Step 1,
contradicting the arc `i -- i+m` (`m ∈ D`).
**Step 3** `m` odd: then `m-1` is even and `g = gcd(m-1, 6m) = gcd(m-1,6) ∈ {2,6}`, so the orbit
of `i` under adding `m-1` has length `6m/g ∈ {m, 3m}`, which is **odd**. Consecutive points of the
orbit are joined by `m-1 ∈ D`, so the types alternate around an odd cycle. ∎

For `(k,C) = (5, triangle)` the outsider pair `{3,4}` has the required property: every
admissible palette is `{3}, {4},` or a pair containing `3` or `4`, and `{3,4}` itself is
admissible but not occurrable (it is disjoint from no admissible palette). The machine check
`nonvacuity.py` confirms that `(5, triangle)` is the **only** case with `k ∈ {5,6}` and
`3 <= ell <= k` having such a 2-set:

| | `ell=3` | `ell=4` | `ell=5` | `ell=6` |
|---|---|---|---|---|
| `k=5` | **`{3,4}`: UNSAT for every `m`** | none: SAT from `m=6` | none: SAT from `m=10` | – |
| `k=6` | none: SAT at `m=6` | none: SAT at `m=6` | none: SAT at `m=6` | none: SAT at `m=6` |

(`k=5, ell=4` has clique number 3 in its disjointness graph yet the system is satisfiable, and
`k=5, ell=5` has clique number 2: **clique number alone does not decide satisfiability**. What
decides the `k=5, ell=3` case is the presence of a 2-type. The point of the table is that the
paper's 4-cycle and 5-cycle proofs of local finiteness at `k=5` are *not* palette-level, while its
triangle proof is.) Machine decision: CaDiCaL
(`python-sat`, `Cadical153`) reports UNSAT for `k=5, ell=3` at
`m = 2,3,4,6,9,12,18,30,60`, and an independently written backtracking search on the CSP (no CNF,
no SAT library) reports UNSAT for `m = 2,3,4,6`. For `k=6` and each `ell ∈ {3,4,5,6}`, CaDiCaL
reports SAT at `m = 6` and explicit witnesses are stored in `witnesses_k6.json`.

**Why six.** At `k = 5` two disjoint palettes use at most `2(k-3) = 4 < 5` labels, so an
**outsider label** always survives a disjointness step; that is the mechanism of Lemma 6.7 and of
the triangle and 5-cycle arguments. At `k = 6`, `2(k-3) = 6 = k`, and in fact **three pairwise
disjoint admissible palettes exist for every `ell`** (the `A_0,A_1,A_2` of §3.1; clique number 3
for `ell = 5,6` and 4 for `ell = 3,4`). Three disjoint palettes can exhaust the label set, no
outsider survives, and no two-type invariant exists.

## 5. Theorem 3: no step rule at `k = 6`

The three case proofs of §6.3 all begin by reducing the palette to a small state space with a
*step rule*: for `k=5, ell=5` the palette is exactly one of the five diagonals `D_i = {i,i+2}` and
`w(Re) = w(e) ± 1` (equation (6.6)); for `k=5, ell=4` the state is one of `X, U, V` and `(5.7)`
forces `w(Re) ≠ w(e)`; for `k=5, ell=3` (P2) forces a binary centre with alternation. At `k = 6`
this reduction is impossible:

> **Theorem 3.** At a six-cycle centre at `k = 6` there are 29 admissible palettes, and **every**
> disjoint pair `(v,w)` of admissible palettes that is not a complementary triple pair is realised
> as `(sigma(e), sigma(Re))` by a model of (P0)–(P4). The complementary triple pairs are exactly
> the pairs excluded by Lemma 2, and they are the only exceptions. Hence the relation induced by
> `R` at a six-cycle centre is the full disjointness relation: there is no step rule and no finite
> state space to run §6.3 on.

Certified in `step_relation.py`: all 29 values are realised (`29/29`), all `128` ordered disjoint
pairs were tested, `108` are realised, and the `20` unrealised ones are precisely the complementary
triple pairs. For comparison the same computation at `k=5, ell=5` returns the 5 diagonals, each
with exactly 2 disjoint partners, i.e. the `C_5` adjacency of (6.6).

## 6. Where §7 actually uses local finiteness

This matters for the sprint's question, so it is worth being exact. §7 of the paper uses Theorem
6.5 in exactly one place, the proof of Lemma 7.4, and there through two quantitative facts:

1. *the total-radii estimate.* The proof ends with "the total final radii are at most
   `|L0| delta + m_{delta,epsilon} + eta`" and then takes `delta_n -> 0`; the term `|L0| delta`
   tends to zero **because `|L0| < infinity`**. `L0 = L ∩ Q'`.
2. *one core disk per point.* "For large `n`, no final disk can contain two distinct points of
   `L0`: its diameter is smaller than their minimum positive separation", and later "the positive
   distances between the finitely many points of `L0` and `∂Q`". Both use that a finite set of
   points has a positive minimum separation.

Also, before Lemma 7.4: "Choose a closed square `Q` of side ten with `∂Q ∩ L = ∅` … local finiteness
leaves only finitely many points to avoid", which only needs `L` not to be dense.

So the hypothesis §7 needs is **not** local finiteness but the following, which is strictly weaker:

> **(L\*)** for every compact `Q'` and every `delta > 0`, `L ∩ Q'` can be covered by `N(delta)`
> closed disks of radius `delta` with `N(delta) · delta -> 0` as `delta -> 0` — i.e. `L` has zero
> upper 1-dimensional Minkowski content on compacts. Local finiteness implies (L\*); (L\*) does not
> imply local finiteness (a compact set of Hausdorff dimension `< 1` satisfies (L\*) and can
> accumulate).

Finiteness enters the printed proof at exactly the two points above and both are implied by (L\*),
with "one core disk per point of `L0`" replaced by a `delta`-cover of `L ∩ Q'`; conversely (L\*) is
what the estimate `N(delta) delta -> 0` is. *I have not rewritten the rest of Lemma 7.4 under
(L\*)*: what is established here is that (L\*) is the property the printed estimates use and that it
is strictly weaker than Theorem 6.5. In particular **a k = 6 proof does not need local finiteness,
it needs a covering-content bound on the cyclic locus**, and Corollary 1 does not rule that out:
it is a statement about palette models, and says nothing about the locus of a genuine colouring.

## 7. What is and is not established

* Established: Corollary 1 (the no-go, class (P0)–(P4)), Theorem 2 (the k = 5 comparison and the
  `2`-type obstruction Lemma 3), Theorem 3 (no step rule at k = 6), Lemma 2 (the new k = 6
  constraint).
* **Not** established: any statement about local finiteness of `L` at `k = 6` for a genuine
  colouring, in either direction. Theorem 1's object is a palette system, not a colouring: it
  satisfies the necessary conditions (P0)–(P4), which is exactly what makes it a no-go for the
  class and not a counterexample to the theorem.
* The class is a strict subset of the paper's toolkit (§3.5, items 1–4). The first thing a k = 6
  local-finiteness proof must supply beyond this note is a use of the density conclusion of Lemma
  5.2(2) or of the trace families `W_x` at *several* centres at once — the two mechanisms the
  paper uses in §6.3.2 and §6.3.3 and which no palette condition can express.

## 8. Files and how to check them

```
bash run_all.sh          # everything, about 2 minutes; logs to stdout
```

| file | content |
|---|---|
| `construction.py` | the construction of §3, exact integer verification of (P0)–(P4) + the block lemma for 4 cycle lengths and 9 resolutions |
| `verify.py` | independent re-verification (separate code path) + Lemma G in exact rational arithmetic + the accumulating centre set |
| `nonvacuity.py` | Lemma 3 and its machine checks; k=5 triangle UNSAT by CaDiCaL and by an independent DPLL; k=6 SAT for all four lengths |
| `step_relation.py` | Theorem 3: the value space and the completeness of the step relation |
| `k5_control.py` | the k=5 resolution thresholds of the table in §4 (UNSAT at `ell=3` for every `m`; SAT from `m=6` for `ell=4` and from `m=10` for `ell=5`) |
| `palette.py` | shared definitions; the exact two-branch shift `s_±` |
| `sector_csp_general.py`, `make_witnesses.py`, `witnesses_k6.json` | the SAT encoding, the witness generator, the stored k=6 witnesses |
