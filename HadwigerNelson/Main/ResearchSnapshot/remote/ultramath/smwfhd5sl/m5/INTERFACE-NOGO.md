# The state level of the §8 interface mechanism is decided exactly: complete at k = 4, one length at k = 5, nothing at k = 6

**Kind of result.** A no-go theorem for a precisely delimited class of arguments (the *state-level*
arguments of §8 of the paper), proved by exhibiting exact models at k = 6; together with a
calibration that shows the class is not a strawman (it decides k = 4 completely and one interface
length at k = 5), a defect in the accepted diagnosis of where k = 6 fails, a refutation of the only
natural repair of the k = 5 triangle argument, and a falsifiable specification for a replacement.

Everything below is a statement about the paper's own objects. Nothing here re-derives R1–R6 or
W1–W7; those are cited. Two exact computations and one elementary certificate carry the weight; each
has an independent verifier and an exact check command (§11).

---

## 1. The interface data

Fix a weak measurable `k`-colouring (Definition 1.2 of the paper), a centre `x`, and the notation of
`results/SPINE.md`: `R` = rotation by `π/3`, `P_x(f) ⊆ {1,...,k}` the maximal palette at centre `x`
in direction `f` (paper, Definition 5.1), `σ` angular measure on `S¹`.

Suppose (as Proposition 7.1 supplies at a cyclic centre) that the label transition graph at `x`
contains a simple cycle of length `ℓ`, `3 ≤ ℓ ≤ k`. Write `T = Z/ℓ` for its labels, edge `j` joining
`j` and `j+1`, and `U = {1,...,k} \ T` for the *outsiders*, `m := |U| = k − ℓ`. Write `v_j` for the
limiting unit direction of the continuum `K_j` (paper, §8), and for `f = e_i := R^i e`
(`i = 0,...,5`, `e` a generic direction) put

    σ_j^(i) = sign(f · v_j),      O_i = U ∪ {j : σ_(j−1)^(i) = σ_j^(i) = −1},
                                  I_i = U ∪ {j : σ_(j−1)^(i) = σ_j^(i) = +1},

so `O_i`, `I_i` are the two allowed sets of paper Lemma 8.1 (`O` = what is left after deleting the
endpoints of the positive edges, `I` after the negative ones; labels outside the cycle belong to
both). The interface state system `IS(k,ℓ,σ)` is the following finite constraint system on six
palettes `P_0,...,P_5 ⊆ {1,...,k}`:

    (C1)  1 ≤ |P_i| ≤ k−3                       general-k palette bound (Prop 5.6; K6-BARRIER §1)
    (C2)  P_i ∩ O_i ≠ ∅  and  P_i ∩ I_i ≠ ∅     paper Lemma 8.1, display (8.1)
    (C3)  P_i ∩ P_(i+1) = ∅, indices mod 6      paper Corollary 5.4, display (5.7)

`(C1)` is the general-k form of Proposition 5.6 and holds for every `k ≥ 3` (at `k = 3` it is empty,
which is already a contradiction); `(C2)` and `(C3)` are proved in the paper for every `k`, since
neither proof uses the number of labels: `(C3)` is Corollary 5.4, and the proof of Lemma 8.1 uses only
the continua of Proposition 7.1 and the fact that an empty allowed set would exclude every colour from
a nonempty open strip — no count of labels occurs.

**Two reductions that make the system finite.**

*Ray data.* `σ_j^(i) = sign(cos(θ_j − iπ/3))` where `θ_j` is the angle of `v_j`. The sign changes
only at `θ_j ≡ (i + 1/2)π/3`, so the six signs of a single ray are constant on each of the six cells
`((c + 1/2)π/3, (c + 3/2)π/3)`, `c ∈ {0,...,5}`, and every ray configuration is described exactly by
its cell vector `c ∈ {0,...,5}^ℓ`. Concretely `σ_j^(i) = +1` iff `c_j + 1 − i ≡ 0, 1, 5 (mod 6)`.
Hence **`6^ℓ` instances cover every ray geometry**, and a global rotation by `π/3` is a symmetry, so
`6^(ℓ−1)` instances suffice.

*The orbit.* `(C3)` ties `P` at `f` to `P` at `Rf`. Since `R` has order 6 this closes up over six
positions. Including the antipodal half of the orbit (`±e`, twelve directions, which the paper's
Proposition 8.2 does use) gives nothing new: the sign matrix is 6-periodic in `i`, so the
twelve-position system is satisfiable iff the six-position one is — verified exactly,
`interface_csp12.py`, and the counts below are identical for both.

**The class of arguments.** A *state-level argument* is a derivation whose hypotheses about the
colouring are exactly `(C1)–(C3)` at the cyclic centre `x` (i.e. `(C1)` for a.e. direction, `(C2)`
for a.e. `f ∉ B` with `B` the finite set of directions perpendicular to some `v_j`, `(C3)` for a.e.
`f`) and whose conclusion is `⊥`. Equivalently: an argument that concludes `⊥` from the palette data
at `x` together with the signs of `f · v_j`.

---

## 2. Theorem 1 (the exact decision table)

Let `N(k,ℓ)` be the number of ray geometries (cell vectors, first cell normalised by the rotation
symmetry) for which `IS(k,ℓ,σ)` is satisfiable.

| k | ℓ | m = k−ℓ | geometries | satisfiable | status |
|---|---|---------|-----------|-------------|--------|
| 3 | 3 | 0 | 36 | 0 | unsatisfiable (`(C1)` is empty) |
| 4 | 3 | 1 | 36 | **0** | unsatisfiable for every geometry |
| 4 | 4 | 0 | 216 | **0** | unsatisfiable for every geometry |
| 5 | 3 | 2 | 36 | 36 | satisfiable for every geometry |
| 5 | 4 | 1 | 216 | 14 | satisfiable |
| 5 | 5 | 0 | 1296 | **0** | unsatisfiable for every geometry |
| 6 | 3 | 3 | 36 | 36 | satisfiable for every geometry |
| 6 | 4 | 2 | 216 | 216 | satisfiable for every geometry |
| 6 | 5 | 1 | 1296 | 225 | satisfiable |
| 6 | 6 | 0 | 7776 | 177 | satisfiable |
| 7 | 3,4,5,6,7 | — | 36,216,1296,7776,46656 | 36,216,1296,2593,4109 | all satisfiable |

Source: `interface_csp.py` (5 s), output `interface_csp_results.json`; the twelve-position version
`interface_csp12.py` gives identical counts. Two of the outcomes are known theorems of the paper and
serve as the calibration of the encoding: the `(5,5)` row is a strengthening of Proposition 8.2
(five-cycle exclusion — the paper's proof reaches the same conclusion through (5.12), (8.1), (5.7)
and the antipodal step, whereas the six-position system is already unsatisfiable), and the `(5,3)`
row being satisfiable for
*every* geometry is exactly why §8.4–8.6 needs the plane-level argument, not a state argument.

Two structural facts, both proved by hand and checked by machine:

* **Monotonicity in `k`.** A model for `(k,ℓ)` is a model for `(k+1,ℓ)`: the extra label is never
  used, `|P| ≤ k−3 ≤ k−2`, and `O_i`, `I_i` only grow when a label is added to `U`
  (`verify_interface.py`, CHECK 3).
* **`m ≥ 2` is trivial.** If `|U| ≥ 2` take `x ≠ y ∈ U` and alternate `P_0 = {x}`, `P_1 = {y}`;
  outsiders lie in every `O_i` and every `I_i`, and `|P| = 1 ≤ k−3` for `k ≥ 4`. So
  `IS(k,ℓ,·)` is satisfiable for **every** geometry whenever `k ≥ ℓ + 2`.

Hence, with monotonicity, `IS(k,ℓ,·)` is satisfiable for every `k ≥ 6` and every
`3 ≤ ℓ ≤ 7`. (The only pairs not covered by the table are `ℓ ≥ 8` with `k ∈ {ℓ, ℓ+1}`; they are
irrelevant to `k = 6` and are recorded as unverified in §9.)

---

## 3. Theorem 2 (calibration: the class decides k = 4 completely)

**Theorem 2.** For `k = 4` and each `ℓ ∈ {3,4}`, `IS(4,ℓ,σ)` is unsatisfiable for *every* sign
matrix `σ`; moreover the refutation uses no information about `σ` at all.

*Proof.* `(C1)` with `k = 4` gives `|P_i| ≤ 1`, so `P_i = {p_i}` and `(C2)` says
`p_i ∈ O_i ∩ I_i`.

`ℓ = 4`: `U = ∅` and `O_i ∩ I_i = ∅`, because a cycle label cannot have both its incident signs
positive and both negative (the second conjunct is the negation of the first). So there is no
admissible `P_i` at all.

`ℓ = 3`: two of the three signs agree. If two are `−1` then no label has both incident signs `+1`,
so `I_i = U = {4}`; if two are `+1` then `O_i = {4}`. Either way `p_i = 4` for every `i`, and then
`P_0 ∩ P_1 = {4} ≠ ∅`, contradicting `(C3)`. ∎

So the state level of the §5–§8 calculus, run at `k = 4`, excludes *every* interface length in the
range `3 ≤ ℓ ≤ k` supplied by Proposition 7.1, by a two-line argument that uses only `(C1)`, the
definition of `O`, `I`, and `(C3)`. This is the calibration demanded of the class: it is not a
strawman, it is a complete refutation at `k = 4`.

Both halves are machine-checked, without `sorry`, in `InterfaceStates.lean`:

    theorem state_level_complete_at_four :
        (∀ σ : Sig 3, ¬ ∃ P : Fin 6 → Finset (Fin 4), IsModel σ P) ∧
        (∀ σ : Sig 4, ¬ ∃ P : Fin 6 → Finset (Fin 4), IsModel σ P)

with `IsModel` literally `(C1) ∧ (C2) ∧ (C3)` and `O`, `I` literally the paper's definition
(`inO σ i l` = `l` is an endpoint of no positive edge). Check: `lean InterfaceStates.lean`
(Lean 4.33.1 + Mathlib, 2.7 s, 0 errors, 0 `sorry`; axioms `[propext, Classical.choice,
Quot.sound]`).

**What this does and does not give.** Conditional on the two general-k inputs the brief lists as
available — the transfer of `results/T1-algebraic-plane.md` (R1, machine-checked) and the
cycle-length bound `3 ≤ ℓ ≤ k` of Proposition 7.1 — Theorem 2 is a *finite reduction* of `χ ≥ 5` in
the sense of L3: the finite decision problem is the pair of instances
`{(k,ℓ) = (4,3, m=1), (4,4, m=0)}`, each of size `36`, resp. `216` sign matrices, and each refuted by
the two-line argument above. It is **not** an independent proof of `χ ≥ 5`: I do not reprove
Proposition 7.1 at `k = 4`, and the palette bound `|P| ≤ 1` also changes the shape of §7 at `k = 4`
(at most one positive coordinate per smoothed vector, so the map lands in the vertices of `K_4` and
the loop extraction of §7 would have to be re-examined there). Theorem 2 is therefore a calibration
of the state level, not a new lower bound.

---

## 4. Theorem 3 (at k = 5 the state level decides exactly one length)

The table shows: at `k = 5` the state level refutes `ℓ = 5` for every geometry, and refutes neither
`ℓ = 3` (satisfiable for all 36 geometries) nor `ℓ = 4` (satisfiable for 14 of 216). So the §8
engine at `k = 5` has three genuinely different strengths at the three lengths:

* `ℓ = 5`: state-level refutation (paper Prop 8.2);
* `ℓ = 4`: the state data already refutes 202 of the 216 geometries; the paper excludes all 216 by
  plane-level geometry — Lemma 8.3/8.4 (the four split rays, the diagonal arcs) plus the cross-word
  restriction;
* `ℓ = 3`: no state-level information at all; the paper's argument is entirely plane-level
  (Lemma 8.6 local constancy, Lemma 8.7 one boundary orbit, Lemma 8.8 the polynomial region, and
  the Moser spindle).

This is the precise sense in which the triangle interface at `k = 5` is the weakest link of the §8
chain — and, by Theorem 4, exactly the link that cannot be carried to `k = 6`.

---

## 5. Theorem 4 (no-go: no state-level argument refutes k = 6)

**Theorem 4.** For `k = 6` and every `ℓ ∈ {3,4,5,6}` there is an explicit ray geometry and an explicit
palette system satisfying `(C1)–(C3)`. Hence no state-level argument (in the sense of §1) refutes
`k = 6`, for any value of the constants `δ_*`, `L`, `c_0`, `C_0`, the mesh, or the multiplicity.

The models (labels `0..k−1`; `T = {0,...,ℓ−1}`; positions `i = 0..5`; `cells` = the ray cells `c_j`;
`palettes` = `P_0,...,P_5`), each verified twice: by the enumeration and, independently, from the
paper's own definition of `O_i`, `I_i` at three interior ray parameters (`verify_interface.py`,
CHECK 1):

    ell=3, cells (0,0,0):            {3} {4} {3} {4} {3} {4}            (outsiders 3,4,5 used)
    ell=4, cells (0,0,0,0):          {4} {5} {4} {5} {4} {5}            (outsiders 4,5)
    ell=5, cells (0,0,0,3,3):        {5} {1,4} {5} {1,4} {5} {1,4}      (outsider 5)
    ell=6, cells (0,0,0,3,3,3):      {1,4} {2,5} {1,4} {2,5} {1,4} {2,5}  (no outsiders)

For the first two, the model in fact works for *every* geometry (alternating two outsiders); the
last two are the interesting ones: `ℓ = 5` is the `k = 6` analogue of the five-cycle exclusion (which
*is* excluded at `k = 5`), and `ℓ = 6` is the length that Proposition 7.1 first makes available at
`k = 6`. The `ℓ = 6` model uses two labels per palette out of a bound of three — it is not a
degenerate solution.

**Non-vacuity.** By Theorem 2 and Theorem 3 the same class of arguments refutes `k = 4` at every
length and `k = 5` at `ℓ = 5`. So the class has real content and Theorem 4 is a genuine limit on it,
not a restriction to a strawman. In particular **every** `k = 6` proof by the §5–§8 route must use
information strictly beyond `(C1)–(C3)` at each of the four interface lengths.

Machine-checked, `sorry`-free, in `InterfaceStates.lean`:

    theorem state_level_silent_at_six :
        (∀ σ : Sig 3, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P) ∧     -- every geometry
        (∀ σ : Sig 4, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P) ∧     -- every geometry
        (∃ σ : Sig 5, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P) ∧     -- explicit geometry
        (∃ σ : Sig 6, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P)       -- explicit geometry

---

## 6. Theorem 5 (a defect: the natural k = 6 repair of Lemma 8.6 is false)

The one step of §8.4–8.6 whose proof consumes the number `5` is Lemma 8.6, *local binary rigidity*:
it shows that the outsider state is essentially constant on an angular neighbourhood, and its engine
is the five-vertex unit path of display (8.3), all of whose vertices lie in the union of two open
strips `U`, `V` which at `k = 5` are coloured by the fixed *pair* `{X,Y}`. Five vertices with colours
in a two-element set alternate, so `c(q) = c(q+h)`, and connectedness gives local constancy.

At `k = 6` an outer or inner strip at a triangle interface is coloured by the *triple* `U = {X,Y,Z}`
of outsiders (that is `(8.1)` and `|U| = k − 3 = 3`), and the alternation is gone. The natural repair
is to hope that a three-valued strip still forces local constancy. It does not:

**Theorem 5.** Put `A = { z : 19/20 < |z| < 21/20 }` and, for `z ≠ 0` with `arg z ∈ [0,2π)`,
`f(z) = ⌊ 9·arg(z)/(2π) ⌋ mod 3`. Then

 (i) `f` takes the three values `0,1,2`, and it is **not** essentially constant on any angular
     neighbourhood of any sector boundary: the nine boundary rays are all essential;
 (ii) `f(z) = f(z')` and `|z − z'| = 1` have **no** common solution in `A`.

So `A` is a strip of the shape Lemma 8.6 uses (it contains both an outer strip in a neighbourhood of
`e₀` and an inner strip in a neighbourhood of `Re₀`), it is coloured by three labels with no
monochromatic unit pair, and its colouring is nowhere locally constant. The inference
"three-valued strip with no unit pair ⇒ locally constant state" is therefore false, and no variant of
the alternation argument of Lemma 8.6 can be transported to `k = 6`.

*Proof of (ii).* Let `r = |z|`, `r' = |z'| ∈ (19/20, 21/20)` and `Δ ∈ [0,π]` the angle between them.
The law of cosines gives `cos Δ = g(r,r') = (r² + r'² − 1)/(2rr')`.

*Step 1 (exact range of `g`).* `∇g = 0` forces `r² = r'² − 1`, i.e. `r = √(r'²−1) ≤ √(41/400) < 19/20`,
outside the square: `g` has no interior critical point. On the four edges the one-variable derivative
numerator is `r² + 1 − (edge)² > 19/20² + 1 − 21/20² > 0`, so the extremes are at corners:

    161/361  ≤  cos Δ  ≤  241/441          (161/361 = 0.4459…, 241/441 = 0.5464…).

*Step 2 (equal colours ⇒ `Δ` is far from `π/3`).* Equal sector indices modulo 3 mean the signed
argument difference is within `2π/9` of a multiple of `2π/3`; for the unsigned `Δ ∈ [0,π]` this gives

    Δ ∈ (0, 2π/9)   or   Δ ∈ (4π/9, 8π/9).

*Step 3.* `cos` is strictly decreasing on `[0,π]`, so Step 1 gives `Δ ∈ [arccos(241/441),
arccos(161/361)]`, and it remains to separate the intervals. This is done exactly (no numerics) by
three rational facts:

  (a) `c := cos(2π/9)` satisfies `8c³ − 6c + 1 = 0` (from `cos 3x = 4c³ − 3c`, `cos(2π/3) = −1/2`).
      The cubic `p(x) = 8x³ − 6x + 1` has `p(11/20) = −969/1000 < 0 < p(4/5) = 37/125` and
      `p' = 24x² − 6 > 0` on `[11/20, 4/5]`, so `p` has exactly one root there, and that root is the
      largest one because `2π/9 < 4π/9 < 8π/9 ≤ π` and `cos` is strictly decreasing on `[0,π]`.
      Hence `11/20 < cos(2π/9) < 4/5`.
  (b) `cos(4π/9) = 2cos²(2π/9) − 1 < 2·(4/5)² − 1 = 7/25`.
  (c) `241/441 < 11/20` and `7/25 < 161/361`.

So `Δ > arccos(241/441) > 2π/9` and `Δ < arccos(161/361) < 4π/9`, contradicting Step 2. ∎

`annulus3.py` verifies every rational identity and inequality above exactly (`Fraction`
arithmetic), and sweeps 400000 unit-distance pairs inside the annulus, finding none monochromatic.

**Joint consistency with the strip data.** The two models of Theorems 4 and 5 are consistent with each
other, so the no-go is not an artefact of looking at the palettes alone. At `ℓ = 3` the palettes of
the model are `{3}` and `{4}`, and the strip colour values can be taken to be the outsider triple
`{3,4,5}`; then each palette meets the strip's colour set, which is what `(8.1)` links (the inner
strip's colour set is contained in `I(e)`, and the outer strip's in `O(e)`, and outsiders lie in
both). The outer strip at a `ℓ = 3` interface is `4`-valued at `k = 6` (one cycle label plus three
outsiders), so a `3`-valued colouring of it is admissible a fortiori. Hence "palette state data +
one-sided strip colour data at the triangle interface" is satisfiable at `k = 6` as well.

**What Theorem 5 rules out and what it does not.** It rules out every argument that concludes a
contradiction at the `k = 6` triangle interface from the *colour data of the strip* alone: three
values, no monochromatic unit pair, the strip geometry. That is exactly the class in which Lemma 8.6
lives. It does not rule out an argument that uses the *global* palette structure at `x` as well;
Theorem 4 already rules out the state-level part of such an argument, so between the two, a `k = 6`
triangle argument must use something new at the interface.

---

## 7. A defect in the accepted diagnosis (W6 / K6-BARRIER §3)

`results/continuation/W1-W4-W7.md` (W6) and `results/K6-BARRIER.md` §3 present the `k = 6`
triangle-interface failure as: the outsider state is a singleton at `k = 5` (two states, transition
graph a single edge, bipartite — "the binary flip") and a set of size ≤ 2 at `k = 6` (six states,
transition graph containing a triangle, **not bipartite**). Two things are wrong with using that as
the diagnosis of the failure:

1. **The outsider system is satisfiable at `k = 5`.** Its two solutions are exactly the alternating
   strings `{X},{Y},{X},{Y},{X},{Y}` and its reverse. So no `k = 5` argument can have concluded
   anything from *satisfiability* of the outsider system, and the `k = 6` system being satisfiable
   (`{X},{Y}` alternating; `{X,Y},{Z}` alternating; and so on: 6 states, 6 transitions) is not a
   change in that respect. Non-bipartiteness of the transition graph is neither necessary nor
   sufficient: `(C1)–(C3)` are satisfiable at `k = 6` for every one of the four lengths whatever the
   parity of the transition graph, and at `k = 5` the graph is bipartite yet `ℓ = 5` is refuted while
   `ℓ = 3` is not.
2. **The actual `k = 5` content of §8.4–8.6 is plane-level, not state-level.** It is Lemma 8.6
   (local constancy, from the two-valued strip) and Lemma 8.7 (one boundary orbit, sectors
   alternating), and by Theorem 5 neither can be reproduced at `k = 6`; by Theorem 4 the state data
   contributes nothing at `k = 6` whereas at `k = 5` it already decides `ℓ = 5` and 202/216 of the
   `ℓ = 4` geometries.

So the correct statement is: at `k = 6` the state level is *silent*, and the plane level fails at the
one step that uses two-valuedness. "Twelve state values instead of two" is bookkeeping; the number
that matters is `k − 3 = 3`, the size of the outsider set, which is the size of the strip's colour
set.

**One further state-level lemma of §6, for completeness.** Lemma 6.4 of the paper ("singleton–pair
alternation is impossible") is also a state-level statement, and it is not expressible in
`(C1)–(C3)` (it involves two angular state sets and a measurable selection), so it is outside the
table. Its engine is nevertheless the same arithmetic: it produces a unit equilateral triangle all of
whose vertices have colours in the two labels outside `{X} ∪ D`, and two labels cannot properly colour
a unit triangle. That complement has size `k − 3 = 2`, so Lemma 6.4 is a `k = 5`-specific lemma for
exactly the reason Proposition 5.6 is, and at `k = 6` the complement has three labels and a
three-coloured unit triangle is no contradiction. Every `k = 5`-specific engine in §§5–8 that I have
checked reduces to the same count.

---

## 8. Specification: what a replacement mechanism must have

Each item is a falsifiable requirement, with the test that falsifies it.

**S1 (non-factorisation).** Its hypothesis set must not be contained in `(C1)–(C3)` at any of the
four lengths `ℓ ∈ {3,4,5,6}`.
*Test:* run the models of Theorem 4 against the proposed hypotheses; if all four survive, the
mechanism cannot conclude.

**S2 (strip data insufficient).** If it concludes something about the outsider state of a strip, the
conclusion must not be derivable from "the strip is coloured by a set of three labels with no
monochromatic unit pair".
*Test:* the annulus colouring of Theorem 5 is a model of exactly those hypotheses and has nine
essential boundary rays; any proposed conclusion about local constancy is falsified by it.

**S3 (k-sensitivity at the right place).** The invariant it uses must change when `k` changes by one,
on an explicit object, and the change must be from "no model" to "no model".
*Test:* exhibit the object and the two values. The state-level invariant fails this in the sharpest
way: it is `N(5,5) = 0` and `N(6,5) = 225` — it is `k`-sensitive, and it is precisely for that reason
useless at `k = 6` (§9).

**S4 (third multiplicity / third value).** If it uses a cover obstruction, the obstruction must be
valid at multiplicity 3 (R4 + W4: the paper's Lemma 7.5 is sharp at multiplicity 2 for every mesh,
and no multiplicity-three relatively open cover obstruction of the printed shape exists).

**S5 (zero- and one-skeleton).** It must handle palettes of size 3 at `k = 6`, i.e. it must not be a
statement whose truth requires `|P_x(e)| ≤ 2`; `(C1)` gives only `≤ 3` and K6-BARRIER §1 shows the
printed proof of the bound cannot improve it at `k = 6` (the complement of a `(k−2)`-set is a triple).

**S6 (no reprieve from the second orbit).** It must not be a refinement of the six-position
`π/3`-orbit by the antipodal half: at the state level that refinement is vacuous (the sign matrix is
`6`-periodic, so the twelve-position system is satisfiable iff the six-position one is; verified
exactly, `interface_csp12.py`, identical counts).

---

## 9. The L4 example: a `k`-sensitive invariant that is exactly computed and useless

The demand is an explicit example in which a proposed replacement satisfies at least one of the
listed properties while the present method cannot. Take the invariant

    N(k,ℓ) = # { ray geometries for which IS(k,ℓ) is satisfiable } / 6^(ℓ−1),

computed exactly above. It satisfies S3's *letter*: it changes when `k` changes by one, on the
explicit instance `ℓ = 5`, where `N(5,5) = 0/1296` and `N(6,5) = 225/1296`; and it is a finite,
exactly computable, k-dependent invariant of the interface. The present method cannot use it,
because the change is in the wrong direction: the `k = 6` value is nonzero, so the invariant certifies
that the interface survives. This is the sharpest available illustration of why S3 has to be paired
with S1/S2: `k`-sensitivity is cheap, and at the interface the only quantity that is genuinely
`k`-sensitive is the palette bound `k − 3`, which is also exactly what makes the system satisfiable.

---

## 10. What is not claimed

* No claim about `χ(ℝ²)` itself. In particular I do not prove `χ ≥ 7`, and I do not prove `χ ≥ 5`
  unconditionally: Theorem 2 is conditional on the general-k inputs (transfer, Proposition 7.1) as
  the brief states them.
* Theorem 4 delimits the *state-level* arguments. It does not show that the whole cover-and-palette
  method fails at `k = 6` — that is the L4 core and needs the cover data (see §8, S4); it shows that
  the §8 half of the method contributes nothing at `k = 6` and locates the failure exactly.
* The pairs `(k,ℓ)` with `ℓ ≥ 8` and `k ∈ {ℓ, ℓ+1}` are not decided in the table; `k ≥ ℓ+2` is
  settled for all `k,ℓ` by the two-outsider model, and everything with `ℓ ≤ 7` is settled here.
  Irrelevant to `k = 6`.
* Theorem 5 is a statement about three-valued strips, not about `6`-colourings of the plane; it
  refutes an *inference*, not a colouring.

---

## 11. Files and exact check commands

All paths relative to this directory (`.ultramath/smwfhd5sl/m5/`).

| file | what it is | command |
|---|---|---|
| `InterfaceStates.lean` | machine-checked Theorems 2 and 4: the definitions of `O`, `I`, `(C1)–(C3)`, the `k = 4` impossibility for all sign matrices and both lengths, and the four `k = 6` models | `lean InterfaceStates.lean` (2.7 s, 0 errors, 0 `sorry`) |
| `interface_csp.py` | the six-position interface CSP, exhaustive over `6^(ℓ−1)` ray geometries for `k ≤ 7`, `3 ≤ ℓ ≤ k` | `python3 interface_csp.py` (5 s) |
| `interface_csp_results.json` | its output: counts and one witness per satisfiable case | — |
| `interface_csp12.py` | the same over the twelve-direction dihedral orbit | `python3 interface_csp12.py` (9 s) |
| `interface_csp12_results.json` | its output (counts identical to the six-position ones) | — |
| `verify_interface.py` | three independent checks: witnesses re-derived from the paper's `O`/`I` definition at three interior ray parameters; bitmask DP vs plain backtracking on 7848 instances; monotonicity in `k` | `python3 verify_interface.py` (6 s) |
| `annulus3.py` | the exact certificate for Theorem 5 (all comparisons in `Fraction`), plus a 400000-pair sweep | `python3 annulus3.py` |

Instance data, as required: `interface_csp.py` solves `6^(ℓ−1)` instances per `(k,ℓ)` (36, 216, 1296,
7776, 46656), each a six-position list-colouring instance with `k ≤ 7` labels, palette size `≤ k−3`,
and a cyclic disjointness constraint; the decision procedure is a bitmask reachability DP, checked
against an independent plain backtracking search; Python 3.11.2, no external solver, no floating
point in any decision. `annulus3.py` uses only `fractions.Fraction` for every decision; its
400000-pair sweep is a floating-point sanity check and carries no part of the proof.
