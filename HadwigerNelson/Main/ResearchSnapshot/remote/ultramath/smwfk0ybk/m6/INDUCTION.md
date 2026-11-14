# The induction lemma at k = 6, and the exact hypothesis audit

Member m6, direction d1. Everything below is either quoted from the paper
(`attachments/here-are-three-files-ni5n/paper.pdf`, page numbers of the printed
text) or from the project record (R1-R6, m3, m5, m6). Nothing is re-derived.

The purpose of this file is to fix the logical status of Step 1 exactly: the
induction lemma *is* valid at k = 6 in the form (IL) below, its only unfilled
hypothesis is (H7) (cycle extraction), and (H7) is **not** available at k = 6
from the paper. Consequently the tightened CSP's decision, whatever it had
been, could not have settled k = 6 without a new proof of (H7).

---

## 0. Notation

`c : R^2 -> Fin k` is a **weak measurable k-colouring** (paper Definition 1.2:
Lebesgue measurable, and for every `R > 0` the integral over `B(0,R) x S^1` of
`1_{A_i}(x) 1_{A_i}(x+u)` in `d sigma(u) dx` vanishes for every label `i`).
`R` = rotation of directions by `kappa = pi/3` (order 6 on `S^1`); `sigma` is
angular measure, normalised so that `sigma(Angles)/2pi = 1`; `Angles = R/2pi Z`.
`P_x(e) subset Fin k` is the maximal palette at the centre `x` in direction `e`
(paper Definition 5.1), defined up to angular null sets; `B_A = {e : P_x(e) = A}`.

**Inputs used, with their exact statements.**

| tag | statement | source |
|---|---|---|
| (P6k) | `1 <= |P_x(e)| <= k-3` for a.e. `e` | Prop 5.6's proof at k = 5, `5 -> k` (R5, `results/K6-BARRIER.md` §1); uses Lemma 5.5 |
| (5.2) | for a.e. `(e,v)` in `S^1 x S^1`: `c(x+e+v) notin P_x(e) union P_x(v)` | Lemma 5.2(1), p.27, all k |
| (5.3) | same-centre/cross-centre exclusion for a smooth representation | Lemma 5.2(3), p.27, all k |
| (5.7) | `P_x(f) inter P_x(Rf) = empty` for a.e. `f` | Corollary 5.4, p.29; machine-checked all k, `palette_sixty_disjoint` |
| (8.1) | `O(e)`, `I(e)` as in §8.1; `P_x(e) inter O(e) != empty`, `P_x(e) inter I(e) != empty` for a.e. `e in S^1 \ B` | Lemma 8.1, p.51, all k |
| T1 | at k = 6, not both `sigma(B_A) > 0` and `sigma(B_{A^c}) > 0` | m6 Theorem 1, from (5.2) |
| T2 | at k = 6, `#{j in Z/6 : |P_x(R^j e)| = 3} <= 3` for a.e. `e` | m6 Theorem 2, from (P6k), (5.7), T1 |
| (H7) | cycle extraction | paper Prop 7.1, p.42; **k = 5 only as printed** |

---

## 1. Statement of the induction lemma

**(IL).** Let `k = 6`, let `c` be a weak measurable 6-colouring, and assume
(H7): there are `x in R^2`, `rho > 0`, `l in {3,...,6}`, distinct labels
`i_0,...,i_{l-1}`, and, for each `j in Z/l`, a compact connected
`K_j subset B(x,rho)` with `x in K_j`, a direction `v_j in S^1` and points
`q_{j,n} in K_j \ {x}` with `q_{j,n} -> x` and `(q_{j,n}-x)/|q_{j,n}| -> v_j`.

Then there is a direction `e in S^1` such that the six palettes
`P_i := P_x(R^i e)` (`i in Z/6`) satisfy, with
`sigma_j^{(i)} := sign(R^i e . v_j)` and `O_i`, `I_i` the paper's (8.1) sets
attached to the sign row `(sigma_j^{(i)})_j`:

* (C1) `1 <= |P_i| <= 3` for every `i`;
* (C2) `P_i inter O_i != empty` and `P_i inter I_i != empty` for every `i`;
* (C3) `P_i inter P_{i+1} = empty` for every `i` (indices mod 6);
* (C4) no two of `P_0,...,P_5` are complementary 3-sets;
* (C5) at most three of `P_0,...,P_5` are ternary.

So the six palettes are a model of the tightened CSP attached to the sign
matrix `(sigma_j^{(i)})`, i.e. to the cell vector of `(v_j)` relative to `e`.

*What (IL) does not say*: nothing about the size of the palettes beyond (C1);
in particular (IL) cannot be strengthened to "ternary-free", and the palettes
`P_i` are the **actual** palettes of the colouring, not a chosen model.

---

## 2. Proof of (IL)

All five constraints are "for almost every direction" statements at the single
centre `x`; `R` preserves `sigma`, so each can be transported along the orbit.
The proof is the intersection of six conull sets and a finite bad set.

1. **The finite bad set.** Let `B = {f : f . v_j = 0 for some j}`; `B` is finite
   and antipodally symmetric (paper §8.1). Put `B' = union_{i in Z/6} R^{-i} B`,
   still finite. For `e notin B'` every `R^i e . v_j` is nonzero, so every sign
   `sigma_j^{(i)}` is defined and `(C2)` is in the form the paper states.

2. **(C1).** `N_1 := {e : |P_x(e)| notin [1,3]}` is `sigma`-null by (P6k) with
   `k = 6`. *This is the only line that uses Lemma 5.5.*

3. **(C2).** By (8.1) there is a `sigma`-null set `N_OI` with both intersections
   nonempty off `N_OI union B` (paper: "for almost every `e in S^1 \ B`"). Put
   `N_2 = union_i R^{-i}(N_OI union B)`. Off `N_2`, (C2) holds at all six
   positions: note `O_i` is `O(e_i)` for `e_i = R^i e`, and the six positions see
   six possibly different sign rows, but (8.1) is a statement about *every*
   direction, not about one fixed sign row.

4. **(C3).** By (5.7) there is a `sigma`-null `N_perp` with
   `P_x(f) inter P_x(Rf) = empty` off `N_perp`; put
   `N_3 = union_i R^{-i} N_perp`. Off `N_3`, `P_i inter P_{i+1} = empty` for all
   `i` because `e_{i+1} = R e_i`.

5. **(C4).** For a fixed pair `i != j` and a fixed 3-set `A`, let
   `G = {e : P_x(R^i e) = A, P_x(R^j e) = A^c}`. If `sigma(G) > 0` then
   `B_A supseteq R^{-i}G` and `B_{A^c} supseteq R^{-j}G` both have positive
   `sigma`, contradicting T1 (since `A union A^c = Fin 6`). So `G` is null; there
   are finitely many `(i,j,A)`, so `N_4`, their union, is null and (C4) holds off
   `N_4`. **This is the step where the orbit form of T1 is legitimate**: the
   nullity of `G` is proved from T1, not from the product-measure nullity of the
   set where (5.2) fails. (The latter would *not* give a vertical statement: a
   null subset of `S^1 x S^1` may meet every vertical fibre in a set of full
   measure.)

6. **(C5).** `N_5 := {e : #{j : |P_x(R^j e)| = 3} >= 4}` is null by T2 (m6
   Theorem 2, whose proof is exactly this statement, from (P6k), (5.7) and T1).

7. **Conclusion.** `N = B' union N_1 union N_2 union N_3 union N_4 union N_5` is
   a finite union of null sets and a finite set, hence null; `sigma` is a
   probability measure on `Angles`, so `Angles \ N != empty`. Pick `e` there; the
   six palettes satisfy (C1)-(C5) with the sign matrix of `e`. Two directions in
   the same *cell* give the same sign matrix, and the sign matrix determines the
   instance, so the model is identified by the cell vector
   `c_j in Z/6`. `square`

**Status of the proof.** Every step is either a quotation or a two-line argument
from a quotation. The a.e. quantifiers are all at the fixed centre `x`, so no
uniformity over centres is needed and no uncountable intersection occurs.

---

## 3. Hypothesis audit: is (H7) available at k = 6?

**No, not from the paper.** This is the one premise of (IL) that is not proved
at `k = 6`, and it fails for two independent reasons, both already in the
project record.

*Audit a (the local finiteness of cyclic centres, paper §6).* The extraction of
Prop 7.1 needs the set of cyclic centres to be locally finite, so that finitely
many small disks can be removed. The paper's engine at `k = 5` is that a cyclic
centre is **binary for a fixed pair**: "For a triangle, (6.2) for its three edges and Proposition 5.6 force
`P_x(e)` to intersect the pair of [`U`]... the pair is unique almost everywhere
and alternates under `R`. Thus every such `x` is binary for that fixed pair.
Lemma 5.5 proves local finiteness of the triangle locus." (p.34). This is
**exactly** the step whose arithmetic is `k - 3 = 2` and which supplies
`l <= 5` — not the count `l <= k` itself: at `k = 6` the palette
meets a **triple** allowed set, and a triple does not define a binary centre.
So the paper's mechanism for making the cyclic-centre locus locally finite does
not run at `k = 6`. (This is R5's correction reproduced as a dependency: the
binding cardinality is the sliver size `k - l`, and at `(k,l) = (6,3)` it is 3.)

*Audit b (the cover obstruction, paper §7).* Prop 7.1's extraction is: remove
small disks around the cyclic centres, average the colour indicators, and force
a nontrivial loop by the cover obstruction of Lemma 7.5 ("A closed square of
side ten has no relatively open cover of multiplicity at most two and mesh at
most two", p.46; applied at p.47 as "at most two, contradicting Lemma 7.5"). m3
(`m3/L4.md`, `results/continuation/L4-SYNTHESIS.md`) shows that
multiplicity-3 relatively open covers of `[-5,5]^2` exist at **every** mesh, so
Lemma 7.5 — which is sharp at multiplicity 2 — never applies at `k >= 6` for any
constants. So the extraction step itself is unavailable at `k = 6`.

*Consequence.* (H7) is an **open hypothesis** at `k = 6`, for every `l`, and for
`l = 6` there is not even a printed `k = 5` analogue. The mission lists
"Proposition 7.1 supplies a simple label cycle of length `l in {3,...,6}`" as an
accepted input; the audit says it is not an input at `k = 6`, it is a target.

*Why this does not weaken the negative verdict.* My decision is SAT, so no
conclusion is drawn from (IL) at all. The audit matters for the *next* round: a
proof of `chi >= 7` along this route needs (H7) **and** an unsatisfiable
tightening, and the second is now known to be false for the tightening
(C1)-(C5).

---

## 4. Logical status of Step 1

Let `Sat(l,g)` be the assertion that the tightened CSP is satisfiable for
interface length `l` and ray geometry `g`.

* **(IL)** gives: every weak measurable 6-colouring with a cyclic centre of
  length `l` produces a model for at least one geometry `g` (the cell vector of
  its rays `v_j`).
* Hence: if for some `l` and **every** `g` we had `not Sat(l,g)`, and if (H7)
  held for that `l`, then no weak measurable 6-colouring would have a cyclic
  centre of length `l`. If this held for all `l in {3,...,6}`, then no weak
  measurable 6-colouring would exist, hence (paper Theorem 1.3, all `k`) no
  proper 6-colouring would exist, hence `chi(R^2) >= 7`.
* **The exhaustive decision gives `Sat(l,g)` for many `g` at every
  `l in {3,4,5,6}`** (indeed for all `g` at `l in {3,4}`), so the antecedent is
  false and the contrapositive is vacuous. Step 1 therefore reaches **none** of
  L1-L5: it does not deliver `chi >= 7`, and it does not deliver `chi = 6`.

The one thing it does deliver is a theorem about the *method*: no argument from
(C1)-(C5) at one orbit can refute `k = 6` (see `REPORT.md` §4 for the
machine-checked form and for what a `(C6)` would have to bind).
