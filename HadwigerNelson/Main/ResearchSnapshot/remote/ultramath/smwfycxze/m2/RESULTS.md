# d2 — §8 at six colours, cycle length ℓ = 5

Member m2, swarm `smwfycxze`. Direction d2: the five-cycle side of §8 at `k = 6`, on the
strip / exclusion-continuum / covering layer, not on the C5 palette system.

**Deliverable.** A theorem (the *outsider gate*: at a `k = 6` centre carrying an interface
5-cycle, the §8.2 argument transfers **iff** the single outsider label is absent from the
palette a.e.), an unconditional quantitative restriction on every `k = 6` 5-cycle centre
(`σ{X ∈ P} ≥ π/3`), a calibration that reproduces Proposition 8.2, and an **exact** sharpness
result: the decisive hypothesis is the *identity* of the absent label, not any bound on `|P|`.
Decided finite computations, each with two independent procedures (backtracking over palette
sets and a CaDiCaL CNF encoding), plus one exact measurable palette field written out in closed
form. `chi(R^2)` is not addressed and nothing here settles `(W)`.

---

## 0. The answer to the question d2 was asked

> *"An odd cycle cannot 2-alternate, so the `k = 5` argument's binary step has no direct
> analogue; decide whether a three-valued odd analogue suffices at `k = 6` and give the exact
> bound."*

**No three-valued analogue suffices, and the exact bound is not a bound on the palette size at
all.** The correct statement is a dichotomy in the *absent label*:

| hypothesis at a `k = 6` 5-cycle centre | six-position system | six-position system |
|---|---|---|
| (labels `0..4` the cycle, `5 = X` the outsider) | geometry-free, 1000 cases | all 7776 realisable geometries |
| no label known absent | SAT 1000/1000 | SAT 1350/7776 |
| a **cycle** label absent a.e. | SAT 704/1000 | SAT 576/7776 |
| the **outsider** `X` absent a.e. | **UNSAT 0/1000** | **UNSAT 0/7776** |

and the UNSAT column is independent of the palette bound: it holds for `|P| ≤ b` with
`b = 1,2,3,4,5` alike, i.e. **the §8.2 argument at `k = 6` does not need the palette bound
(5.12) at all**, whereas `k = 5` and `k = 6` are the *same* theorem with one hypothesis
supplied for free at `k = 5` (`k − ℓ = 0` outsiders) and unavailable at `k = 6`
(`k − ℓ = 1`). The exact bound is the integer `k − ℓ`: the argument is rigid iff the palette
avoids the whole of `O(e) ∩ I(e) = [k] ∖ (cycle labels)` almost everywhere.

Unconditionally at `k = 6`, the hypothesis cannot be weakened and cannot be verified either:

> **Theorem 2.** At every weak measurable 6-colouring and every centre `x` whose `Γ_x` contains
> a 5-cycle with outsider `X`, the set `D = {e : X ∈ P_x(e)}` satisfies
> `π/3 ≤ σ(D) ≤ π`  (between one sixth and one half of the circle).

So the outsider is present on a set of directions of measure `≥ π/3` and absent on one of
measure `≥ π`: the §8.2 route is *exhausted* at `k = 6`. It follows (Corollary 2.2) that a
`k = 6` 5-cycle centre cannot carry the outsider's own colour, at any self-avoidance point of
its colour class.

---

## 1. Setting and the exact list of available constraints

`c` is a weak measurable `k`-colouring (paper, Definition 1.2); `A_i` its classes; `P_x(e)` the
maximal palette at the centre `x` in direction `e` (Definition 5.1); `Γ_x` the transition graph;
`R` = rotation of directions by `κ = π/3`, `R³ = −1`; `Δ(K)` the straddling region (7.1).

At a centre `x` whose `Γ_x` contains a simple 5-cycle with labels `0,…,4` in cyclic order
(edge `j` joins `j` and `j+1`, indices mod 5) we use only the following, each quoted with its
exact reference and each label-blind, i.e. valid at `k = 6` by the transfer of
`sprint/k6/REPORT.md` §2:

* **(8.1)** *(Lemma 8.1, printed p. 51; proof label-blind)* with `B` the finite set of
  directions perpendicular to some limiting direction `v_j`, and for `e ∉ B` the sign of edge
  `j` being `sign(e·v_j)`: `O(e)` = labels that are not endpoints of any positive edge,
  `I(e)` = labels that are not endpoints of any negative edge, so
  `I(e) = {i : both incident edges +} ∪ outsiders`, `O(e) = {i : both incident edges −} ∪ outsiders`.
  Then `P_x(e) ∩ I(e) ≠ ∅` and `P_x(e) ∩ O(e) ≠ ∅` for a.e. `e`.
* **(5.7)** *(Corollary 5.4)* `P_x(e) ∩ P_x(Re) = ∅` a.e.
* **(6.2)** *(Lemma 6.2)* `P_x(e) ⊄ {i,j}` a.e., for every edge `ij ∈ Γ_x`.
* **(SUM)** *(palette-only content of (5.2))* if `e, v` are nonparallel and
  `P_x(e) ∩ P_x(v) = ∅` then `|P_x(e)| + |P_x(v)| ≤ k − 1`; the point `x+e+v` must carry a
  colour outside the union. Since `h = e+v` has exactly one unordered unit representation, this
  is the *complete* palette-only content of (5.2) at a single centre.
* **(PAL)** `|P_x(e)| ≤ k − 3` *(Proposition 5.6's method, transferred to `k = 6`)* — used only
  in the countermodel section; Theorems 1 and 2 do not use it.
* **(M11)** the directions whose palette contains `T` have angular measure at most `π`
  (half the circle), for every nonempty `T` *(m11, `k6-ternary-palette.md` Theorem 3)*.
  Throughout, `σ` is unnormalised angular measure on `S¹`, so `σ(S¹) = 2π`.
* **(L63)** *(Lemma 6.3)* strict state separation; **(L64)** *(Lemma 6.4)* no measurable state
  function with only the values `{X}` and a fixed disjoint pair `D` changing under `R`.

Every claim below is stated in the class "**single-centre palette data at a 5-cycle centre**".
That is exactly the class §8.2 argues in — its proof says "choose a direction on a full
six-position `R`-orbit for which all the preceding almost-everywhere assertions and (5.7)
hold" — and it is *not* the class of palette fields of actual colourings (see §8).

---

## 2. Lemma A — the structural reason `k = 5` and `k = 6` differ

Fix `k ≥ ℓ = 5`, a sign pattern `Q ⊆ Z/5` (the set of positive edges at direction `e`), and let
`c(Q)` be the number of sign changes round the 5-cycle (`c = 0` if `Q` is constant). Put
`outs = [k] ∖ {0,…,4}`.

**Lemma A.** `|O(e) ∪ I(e)| = k − c(Q)` and `|O(e) ∩ I(e)| = outs`.
*Proof.* A cycle label `i` is outside both sets exactly when it is the endpoint of one positive
and one negative edge, i.e. at a sign change; the second identity is immediate since a cycle
label cannot have both its incident edges positive and negative. `square`
*(machine-checked for every `(k,ℓ)` with `5 ≤ k ≤ 8`, `3 ≤ ℓ ≤ 6` and every pattern:
`work/verify2_d2.py` S1.)*

Consequences, and this is the whole `k = 5 → 6` story:

* `k = ℓ = 5`: `O ∩ I = ∅`, so Lemma 8.1's *non-emptiness* is a real constraint and forces
  `c = 2` runs of lengths `2` and `3` (if some sign has all its runs of length 1, its allowed
  set is empty). Then
  `|O| + |I| = ℓ − 2 = 3`, one of them a singleton, and a palette meeting both has the form
  `{s, x}` with `s` the *forced* vertex. Exactly two options; the paper's "two diagonals
  `D_1 = {1,3}`, `D_4 = {4,1}`".
* `k = 6, ℓ = 5`: `O ∩ I = {X}`, so `I(e)` and `O(e)` are **never empty** and Lemma 8.1 carries
  no information about the sign pattern. A palette not containing `X` still has the forced form
  `{s, x}`, but a palette containing `X` is admissible for *every* pattern (since
  `X ∈ O ∩ I`). The option set jumps from 2 to 12 unbounded, 7 under `|P| ≤ 3`.

So the `k = 5` rigidity is a *transversal* rigidity: it needs `O ∩ I = ∅`. Lemma A says this is
exactly `k = ℓ`.

**Lemma A′ (the forced-vertex structure).** For `Q ∈ G` := {patterns with exactly two runs, of
lengths 2 and 3} — and `|G| = 10`, these are exactly the patterns for which `I∖outs` and
`O∖outs` are both non-empty — let `s(Q)` be the interior vertex of the length-2 run and `A(Q)`
the set of interior vertices of the length-3 run. Then

  `A(Q) = {s(Q)+2, s(Q)+3} (mod 5)`,  `s(complement Q) = s(Q)`,  `A(complement Q) = A(Q)`.

*(machine-checked for all 32 patterns, `work/verify_d2.py` `lemmaA()`.)*

The second identity is the *odd-cycle* phenomenon behind the whole theorem: it holds because the
unique length-2 run and the unique length-3 run exchange roles under complementation, and it
fails for even `ℓ`, where the two runs of a split have equal length.

---

## 3. Theorem 1 — the outsider gate at `k = 6`

> **Theorem 1.** Let `c` be a weak measurable 6-colouring and `x` a centre whose `Γ_x` contains a
> simple 5-cycle on `0,…,4`, with outsider `X = 5`. If `X ∉ P_x(e)` for almost every direction
> `e`, then contradiction. Equivalently: at every `k = 6` centre carrying an interface 5-cycle,
> `X ∈ P_x(e)` on a set of directions of positive angular measure.

**Proof.** Choose `e` outside the null set where the finitely many a.e. assertions fail for any
of the six directions `e, Re, …, R⁵e`; this is possible since `B` is finite and the exceptional
sets are null. Write `Q_i = Q_x(R^i e)` (the positive-edge set at `R^i e`), `P_i = P_x(R^i e)`.

*Step 1 (reduction).* `X ∉ P_i`, and `P_i` meets `I(Q_i)` and `O(Q_i)` by (8.1). By Lemma A the
sets `I(Q_i)∖{X}` and `O(Q_i)∖{X}` are both non-empty and met by `P_i`, hence `Q_i ∈ G`.
*Step 2 (forced vertex).* By Lemma A′, `s_i := s(Q_i) ∈ P_i` and there is
`x_i ∈ A(Q_i) ∩ P_i ≠ ∅`; write `x_i = s_i + δ_i` with `δ_i ∈ {2,3}` (all indices mod 5).
*Step 3 (antipodal collapse).* `Q(−e) = complement Q(e)` because `(−e)·v_j = −(e·v_j)`; hence
by Lemma A′ `s_{i+3} = s_i`. (This is where `k = 6, ℓ = 5, R³ = −1` is used, and where an even
cycle length would fail.)
*Step 4 (step table).* (5.7) gives `P_i ∩ P_{i+1} = ∅`, so `{s_i, x_i} ∩ {s_{i+1}, x_{i+1}} = ∅`.
With `d_i := s_i − s_{i+1} (mod 5)` this is the four conditions
`d_i ∉ {0, δ_{i+1}, −δ_i, δ_{i+1}−δ_i}`, i.e.

  `(δ_i,δ_{i+1}) = (2,2) ⇒ d_i ∈ {1,4}`, `(2,3) ⇒ {2,4}`, `(3,2) ⇒ {1,3}`, `(3,3) ⇒ {1,4}`.

In particular **`d_i = 2` forces a rise `(2,3)` and `d_i = 3` forces a fall `(3,2)`** (a rise is
`(δ_i,δ_{i+1}) = (2,3)`, a fall `(3,2)`).
*Step 5 (the closing condition).* `Σ_{i=0}^{5} d_i ≡ 0 (mod 5)` (telescoping, `s_6 = s_0`), and
`d_{i+3} = s_{i+3} − s_{i+4} = s_i − s_{i+1} = d_i` by Step 3. So `2(d_0+d_1+d_2) ≡ 0`, hence
`d_0+d_1+d_2 ≡ 0 (mod 5)`. Each `d_i ∈ {1,2,3,4}` and the sum lies in `[3,12]`, so the multiset
`{d_0,d_1,d_2}` is one of `{1,1,3}`, `{1,2,2}`, `{2,4,4}`, `{3,3,4}` (exhaustively verified:
`work/final_verify.py` `case_analysis()`). The six values are `d_0,d_1,d_2,d_0,d_1,d_2`.
*Step 6 (four cases).* Relabelling `i ↦ i+j` cyclically preserves every hypothesis, so:

1. `{1,1,3}`, the `3` at position 0: `d_0 = 3` forces a fall, so `#falls ≥ 2` (at 0 and 3);
   `#rises = #falls > 0`, but a rise needs `d ∈ {2,4}` and no `d` is `2` or `4`. Contradiction.
2. `{1,2,2}`, the `1` at position 0: the two `2`'s sit at two of the positions `0,1,2`, hence
   at four distinct positions among the six each `d_i = 2` forces a rise. So `#rises ≥ 4`, but
   `#rises = #falls ≤ 3`. Contradiction.
3. `{2,4,4}`, the `2` at position 0: `(δ_0,δ_1) = (2,3)`. `d_1 = 4` with `δ_1 = 3` is
   compatible only with `δ_2 = 3` (const, `d ∈ {1,4}`) and not with `δ_2 = 2` (fall,
   `d ∈ {1,3}`). Then `d_2 = 4` similarly forces `δ_3 = 3`. But `d_3 = d_0 = 2` forces the rise
   `(δ_3,δ_4) = (2,3)`, i.e. `δ_3 = 2`. Contradiction.
4. `{3,3,4}`, the `4` at position 2: `d_0 = d_1 = 3` forces falls at `0` and `1`, i.e.
   `(δ_0,δ_1) = (3,2)` so `δ_1 = 2`, and `(δ_1,δ_2) = (3,2)` so `δ_1 = 3`. Contradiction.

`square`

**Remarks.** (i) No palette bound is used anywhere — `(PAL)` is not invoked, so Theorem 1 is
stronger than the `k = 5` argument, which does invoke (5.12). (ii) The hypothesis is *one*
label, and it is used twice: to force `Q_i ∈ G` (Step 1) and to force `s_i ∈ P_i` (Step 2).
(iii) The proof is geometry-free: the only geometric input is the exact identity
`Q(−e) = complement Q(e)`.

**Machine verification.** `work/verify_d2.py` and `work/final_verify.py`, five independent
searches over the geometry-free family `{(Q_0,Q_1,Q_2, comp Q_0, comp Q_1, comp Q_2)}`,
1000 cases: (a) the reduced `s`/`δ` search of Step 6, (b) backtracking over *all* palette sets
with `|P| ≤ 3`, (c) backtracking with no palette bound at all, (d) and (e) the same two as CNF
instances solved by CaDiCaL (via `pysat`). All report `SAT 0/1000`. The restriction to
`(Q_0,Q_1,Q_2)` free and `Q_{i+3} = comp Q_i` is *exact*, not generic: `Q(−e) = comp Q(e)`.

---

## 4. Theorem 2 — the quantitative, unconditional form

> **Theorem 2.** Let `c` be a weak measurable 6-colouring and `x` a centre whose `Γ_x` contains a
> 5-cycle on `0,…,4` with outsider `X`. Then for a.e. direction `e` there is `i ∈ {0,…,5}` with
> `X ∈ P_x(R^i e)`. Consequently `π/3 ≤ σ{e : X ∈ P_x(e)} ≤ π`.

**Proof.** If for a set of positive angular measure of `e` all six rotations `R^i e` avoided `X`,
Theorem 1's argument applied at one such `e` (outside the null exceptional sets) would give a
contradiction; so this set is null. Hence `∪_{i=0}^{5} R^{-i} D` is conull with
`D = {X ∈ P_x}`, so `2π ≤ Σ_i σ(R^{-i}D) = 6 σ(D)`. The upper bound is (5.7): `X` cannot lie in
two consecutive palettes of an `R`-orbit of length 6. `square`

**Sharpness of the constant.** `work/min_count.py` shows that the minimum of
`#{i : X ∈ P_i}` over *all* admissible six-position configurations is exactly `1`, in the
geometry-free family and in the 7776 realisable geometries, with `(6.2)`, `(PAL)` and without
them. So `1/6` is the best constant this orbit argument can give, and the widest possible
window is `[π/3, π]`.

> **Corollary 2.2.** Let `x` be a `k = 6` centre with `Γ_x ⊇ C_5` and outsider `X`, and suppose
> the self-avoidance of the record's Lemma D holds at `x` (i.e. `c(x) ∉ P_x(e)` a.e.). Then
> `c(x) ≠ X`: the centre of a `k = 6` five-cycle carries one of the cycle labels.

*Proof.* `c(x) = X` would give `X ∉ P_x(e)` a.e., contradicting `σ(D) ≥ π/3 > 0`. `square`
This is the exact sense in which every `k = 6` five-cycle centre is *near* a cycle label; it
does not exclude it, and §6–§7 show it cannot: with the outsider allowed in the palette the
constraint list of §1 is satisfiable.

**Caveat, stated deliberately.** I quote self-avoidance as a *hypothesis* above rather than
deriving it. The record's Lemma D (`sprint/k6/REPORT.md` §5) needs, for a fixed centre `x`, that
`x + δ` be a density-one point of `A_i` for a.e. `δ` on the unit circle; that conull statement is
true for a.e. centre `x` in `A_i` (Fubini for the family of unit circles), not for every
density-one point. More importantly, the direct route from (5.2) to self-avoidance fails
structurally: the sum map `(e,v) ↦ e + v` is singular exactly on the antiparallel diagonal, so
(5.2) at the centre `x` carries no information at `x` itself, and the set of points it does
constrain near `x` is a 1-parameter family of circles through `x`, which a density-one point can
carry. I therefore state Corollary 2.2 with the hypothesis explicit and claim Theorem 2 as the
unconditional statement.

---

## 5. Theorem 3 — calibration: Proposition 8.2, without (5.12)

> **Theorem 3.** At `k = ℓ = 5` the six-position system of §1 is unsatisfiable for every sign
> geometry, with or without the palette bound (5.12).

**Proof.** There is no outsider, so Lemma A gives `O ∩ I = ∅`, and Lemma 8.1's non-emptiness
forces `c(Q) = 2` with run lengths `2,3`: `Q ∈ G`. Then Lemma A′ gives the same forced-vertex
structure `{s_i, x_i}` and Steps 3–6 of Theorem 1's proof run verbatim. `square`

The printed proof of Proposition 8.2 instead invokes (5.12) to make every palette *equal* to a
two-element transversal, and then runs a six-position sign argument on the two diagonals. The
six-position argument survives without that step, so **(5.12) is not needed for Proposition
8.2** — a small strengthening, and it is what makes `k = 5` and `k = 6` one theorem rather than
two.

**Machine verification** (`work/final_verify.py` [3]): 1000/1000 UNSAT with `|P| ≤ 2` and
1000/1000 with no palette bound, by both backtracking and CaDiCaL. Because the two runs agree
with the paper's conclusion, the encoding is calibrated.

---

## 6. Theorem 4 — the exact bound: not the palette size, the absent label

> **Theorem 4 (decided finite computation).** For the six-position system of §1 at `k = 6` with
> palettes bounded by `|P| ≤ b`:
> 1. with `X` absent a.e.: UNSAT for every `b ≥ 1` and every geometry (Theorem 1);
> 2. with a **cycle** label absent a.e.: SAT for `b = 2,3,4,5` in `704/1000` geometry-free cases
>    and `576/7776` realisable geometries;
> 3. with **no** label absent: SAT in `1000/1000` geometry-free cases and `1350/7776` realisable
>    geometries, for every `b ≥ 2`;
> 4. with `b = 1`: UNSAT in all three columns (a singleton palette must meet `O ∩ I = {X}`, so
>    it must be `{X}`, and six copies of `{X}` violate (5.7)) — so `b = 1` is the only
>    palette-size threshold and it is vacuous. The counts in items 1–3 are *constant* in
>    `b ≥ 2`, verified for `b = 2,3,4,5` on all 1000 and all 7776 instances.

The absence of `X` is thus the *only* sufficient hypothesis in this class, and no bound on `|P|`
substitutes for it. Hence "three-valued" (or any `b`-valued) is the wrong axis.

**Realisability of the geometry.** A six-tuple of sign patterns arising this way is realisable
iff it arises from five angles `β_j = arg v_j`; the six sampled directions are `60°` apart, so
with `φ_j = β_j + 90°` the relevant datum is the assignment of each `φ_j` to one of the six open
`60°` gaps, and the pattern at sample `m` is `{j : gap(j) − m ∈ {0,1,2}}`. All `6⁵ = 7776`
assignments give distinct six-tuples and each is realised by `φ_j` strictly inside its gap
(so the samples are never in the exceptional set `B`). The counts in Theorem 4 are over these.

**Both procedures.** Backtracking over admissible palette sets with pruning
(`csp_solve`) and a CaDiCaL CNF instance (`csp_solve_cadical`, at-most-`b` clauses plus
"meet `I`"/"meet `O`"/avoid clauses plus `(5.7)` binary clauses). Identical verdicts on all
1000 and all 7776 instances.

### 6a. A vacuity test that changed the answer

The first witnesses found were `{5}` / `{1,4}` alternating on the six positions — until Lemma 6.4
was applied. **Lemma 6.4 forbids exactly a two-valued state function `{X}` / fixed pair `D`
changing under `R`, so those witnesses are inadmissible**, and `m6`'s `STRIP(6,5)` witness
`{5}` / `{1,3}` (recorded in `sprint/k6/REPORT.md` §4b) is excluded by the same lemma for the
same reason. `work/vacuity.py` re-decides with the requirement that at least three *distinct*
palette values occur among the six directions — a sufficient certificate that the underlying
field is not a two-valued state function — and the counts in Theorem 4 are unchanged
(`1350/7776` and `576/7776`), with witnesses such as `{5}, {1,4}, {5}, {1,4}, {5}, {2,4}`. So
the no-go survives Lemma 6.4. **Correction to the record:** `STRIP(6,5)`'s SAT status is a
statement about `m6`'s own constraint list `S0–S4`, which does not include Lemma 6.4; it should
not be read as exhibiting an admissible §8 witness. The three-valued fields of §7 below repair
this.

---

## 7. Theorem 5 — an exact measurable palette field

Six sampled palettes are not yet a field. Here is one, in closed form, on the whole direction
circle. Take the limiting directions at `β_j = 18° + 72°j`, `j = 0,…,4` (so the sign-pattern
arcs are the multiples of `36°`), and define, with all angles in degrees,

  `P(e) = {1,3}` for `θ ∈ (0,60) ∪ (180,240)`,
  `P(e) = {2,4}` for `θ ∈ (72,132) ∪ (252,312)`,
  `P(e) = {5}`   for the remaining `120°`: `(60,72) ∪ (132,180) ∪ (240,252) ∪ (312,360)`.

> **Theorem 5.** This `P` is a measurable set-valued field on `S¹` with, at a `k = 6` centre
> carrying an interface 5-cycle with limiting directions `β_j`, the properties:
> **(8.1)**, **(5.7)**, `|P| ≤ 2`, **(6.2)**, **(SUM)**, **(M11)**, the whole constraint list of
> `sprint/k6/STRUCTURE.md` Theorem 5 (items 1–7, with the centre colour `i = 0`), and
> `0 ∉ P(e)` for every `e` — i.e. self-avoidance for the *cycle* label `0`. It is not a
> two-valued state function (three values, so Lemma 6.4 does not apply), and it makes Lemma 6.3
> vacuous (`|P| ≤ 2` everywhere, so no state represents a group of three labels). Finally
> `σ{X ∈ P} = 2π/3` (one third of the circle), inside Theorem 2's window `[π/3, π]`, and
> `max_T σ{T ⊆ P} = 2π/3 ≤ π` for (M11).

*Verification.* `work/final_verify.py` [5] discretises `S¹` into `360` cells of `1°`; since `60`
is a whole number of cells the constraint set splits into `60` independent six-cell problems and
a cell-constant field satisfying the constraints on every cell satisfies them a.e. All patterns
are constant on the `36°` arcs, so no cell straddles an arc boundary and the discretisation is
exact. Every constraint is asserted on all 360 cells; the run is exact (`Fraction`, degrees);
the `(SUM)` check is over all `360²` ordered pairs of cells.

**Reading.** Theorem 5 is the sharpness half of Theorem 1: it satisfies Theorem 1's hypotheses
*except* the absent label, and it does so as a genuine measurable field, not merely as six
sample values. Hence no argument from the class of §1 can exclude a `k = 6` five-cycle at a
centre whose palette avoids a cycle label — in particular not one that adds `(PAL)` = 3,
`(6.2)`, `(M11)`, `(SUM)`, `(L63)`, `(L64)`, or any palette-size hypothesis.

**Class of the no-go.** This is a countermodel at the *single-centre palette* level. It is
**not** the palette field of any weak measurable 6-colouring: by the record's endpoint-trace
argument (`m10`) and `m4` Corollary 2, any palette field carrying a trace consistent with a
proper colouring is killed, and by `m10` no centre-independent field survives the endpoint trace
either; and by Theorem C of `sprint/k6/REPORT.md` the palette axioms are satisfiable for every
cycle length, so a countermodel here is expected. What is new is not that the palette level is
dead, but *where exactly* in the palette data the death occurs — the identity of the absent
label — and that the §8.2 mechanism survives the transfer to `k = 6` verbatim once that one
condition is in place.

**Vacuity test against the record's models.**
* `m13`'s singleton triangle model is at `ℓ = 3`, and its palettes are singletons; at a 5-cycle a
  singleton palette must be `{X}` ((6.2) plus Corollary 4 of `STRUCTURE.md`), so it is not an
  `ℓ = 5` object. It is not a witness for or against Theorem 1.
* `m15`'s block fields are built for the palette axioms, not for (8.1): they use three pairwise
  disjoint pairs and all six labels, so they fail self-avoidance (the record says so) and say
  nothing about the §8 strip layer. They do **not** supersede Theorem 5: `m15` never checks
  (8.1), and (8.1) is the constraint that makes the §8.2 layer non-trivial.
* `m3`'s proper colouring is at `k ≥ 7`, outside Theorem 1's scope by design: at `k − ℓ ≥ 2` the
  outsider set has two or more labels, so a palette avoiding only the centre's colour still meets
  `O ∩ I`, and the reduction of Step 1 fails. This is consistent with `m3`'s existence.
* Theorem 5 itself was re-checked against every item of the record's own six-orbit constraint
  list (`sprint/k6/STRUCTURE.md` Theorem 5, items 1–7) — it satisfies all of them, and
  `work/vacuity.py` re-runs the no-go with Lemma 6.4 imposed (≥ 3 distinct palette values).

---

## 8. What is claimed, what is not

**Proved here.**
* Theorem 1: the outsider gate at `k = 6` for `ℓ = 5`. No palette bound, no geometry input
  beyond `Q(−e) = comp Q(e)`; fully hand-proved (§3) and machine-verified five ways.
* Theorem 2: `π/3 ≤ σ{X ∈ P} ≤ π` at every `k = 6` five-cycle centre. Unconditional.
  Corollary 2.2: the centre cannot carry the outsider's colour, at a self-avoidance point.
* Theorem 3: Proposition 8.2 follows from the same argument, and does not need (5.12).
* Lemma A / A′: `|O ∪ I| = k − c`, `|O ∩ I| = k − ℓ`; the forced-vertex identities. The exact
  reason `k = 5` is rigid and `k = 6` is not.
* Theorem 4: the decided finite computation; the exact bound is `k − ℓ` and the identity of the
  absent label, not `|P|`.
* Theorem 5: an exact measurable palette field, closed form, satisfying the whole record's
  single-centre constraint list.

**Not claimed.**
* `(W)`, `chi(R²) ≥ 7`, `chi(R²) ≤ 6`: untouched.
* **The five-cycle case at `k = 6` is NOT excluded.** Theorem 1 excludes it only when the
  outsider is absent a.e.; Theorem 2 shows the outsider is present on `≥ 1/6` of the circle; §6
  and §7 show that no constraint in §1 can bridge the gap. So the §8.2 route stops exactly here,
  and the missing lemma is `σ{e : X ∈ P_x(e)} = 0` — refuted by Theorem 2. That is the sharp
  frontier, not a solution.
* No claim about `ℓ = 3, 4, 6` at `k = 6` (those are d1, d3, d4 and the prior record).
* No claim that `k = 6` five-cycles exist in any colouring; `m4` Theorem 3 shows they do not in
  the a.e.-singleton class `S_1`. Theorem 1 and Theorem 5 are about the non-singleton stratum.
* Theorem 5 is not realisable by a colouring (§7, "Class of the no-go").
* I did not re-prove the record's Lemma D at every density-one point; see the caveat in §4.
* I did not verify `(PAL)` `|P| ≤ 3` independently for `k = 6`; it is cited from
  `results/K6-BARRIER.md` §1 / `m11`, and Theorems 1–2 do not use it.

---

## 9. Reproducibility

```
cd <repo>/.ultramath/smwfycxze/m2
python3 work/final_verify.py      # the whole package; exit 0 iff every assertion holds (~5 s)
python3 work/verify_d2.py         # Lemma A, Theorem 1 (5 searches), calibration, sharpness, sweep
python3 work/verify2_d2.py        # Lemma A formulas, k=5 without (5.12), realisable witnesses
python3 work/vacuity.py           # the Lemma 6.4 vacuity test (>=3 distinct palette values)
python3 work/min_count.py         # sharpness of the constant 1/6   (~8 min)
python3 work/arcmodel.py          # the arc-constant model (UNSAT -- why the cell model is used)
python3 work/cellfield2.py        # 1-degree cell fields, all strata
```

All arithmetic is exact: integers, `fractions.Fraction` degrees, finite set algebra. No floating
point enters any decision (`float` appears only in printed log lines). Every satisfiability claim
is produced by two algorithms: a pruned backtracking search over palette sets, and a CNF instance
solved by CaDiCaL (`pysat`, `/opt/lean/bin/cadical`).

| file | content |
|---|---|
| `work/verify_d2.py` | Lemma A, Theorem 1 (5 searches), calibration, sharpness, geometry sweep |
| `work/verify2_d2.py` | the two structural identities, `k = 5` without (5.12), realisable witnesses |
| `work/vacuity.py` | the Lemma 6.4 test; no-go survives with ≥3 distinct palette values |
| `work/min_count.py` | the constant `1/6` is the best the orbit argument gives |
| `work/arcmodel.py`, `work/cellfield2.py`, `work/cellfield.py` | the measurable fields |
| `work/final_verify.py` | everything, with the four-case skeleton of §3 Step 6 |
| `work/k6_ell5.py` | first pass (superseded, kept for the record) |
| `work/pages/p{27,29,33,35,42,51}.png` | renders of the pages carrying (5.2), (5.7), (5.12), (6.2), (7.1), (8.1) |

**Paper check.** Formulas were extracted with `pdftotext -layout` on PDF pages 27, 29, 33, 35, 42,
51 and confirmed token by token: (8.1) `Px(e) ∩ O(e) ≠ ∅, Px(e) ∩ I(e) ≠ ∅ for almost every
e ∈ S \ B`; (5.7) `Px(f) ∩ Px(Rf) = ∅`; (5.12) `1 ≤ |Px(e)| ≤ 2`; (6.2)
`Px(e) ⊄ {i,j} for almost every e`; (7.1) `Δ(K) = {z : min|z−q| < 1 < max|z−q|}`. The sign
convention of Lemma 8.1 (positive edge ⇒ *outer* strip excluded for its endpoints) was checked
against the displayed identity `|x + e − q_{j,n}|² = 1 + r²_{j,n} − 2r_{j,n}(e·w_{j,n})` and its
surrounding prose on the same page. Page renders are stored under `work/pages/`.
