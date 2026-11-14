# Calibration of the tightened interface CSP: (C4) and (C5) are satisfiability-neutral at every k ≥ 6

Member m16, swarm smwfk0ybk, direction d9. Requested object of study: whether the m6 tightening
of the m5 interface CSP is *sound at its ceiling* — i.e. whether (C4)+(C5) can be the constraints
that produce UNSAT at k = 6 without overshooting at k = 7, where a colouring exists. The answer
is negative, and the reason is a two-line proof rather than a computation: **on the satisfiable
side of the m5 system the palettes can always be taken of size ≤ 2, and on that stratum both m6
constraints are vacuous.** Step 1 of this run's brief is therefore decision-negative for a
structural reason, not by accident of the ray-geometry enumeration; the INDUCTION LEMMA, whether
or not it is proved, has nothing to act on.

All numbers below are exact; every computation is reproducible with the commands in §8 and the
machine-checked statements are in §6.

---

## 1. The system, exactly as decided

This is m5's encoding (`INTERFACE-NOGO.md` §1), quoted so that the statement of the result is
self-contained. Labels `Fin k`; a cyclic centre `x`; a simple label cycle of length `ℓ`,
`3 ≤ ℓ ≤ k` (paper Proposition 7.1); cycle labels `T = {0,…,ℓ−1}`, outsiders `U = Fin k \ T`;
rays `v_0,…,v_{ℓ−1}` with cell vector `c ∈ {0,…,5}^ℓ`, six orbit directions `e_i = R^i e`,
`R` = rotation by `π/3`;

  `σ_j^(i) = sign(e_i · v_j) = +1 ⟺ (c_j + 1 − i) mod 6 ∈ {0,1,5}`,

  `O_i = U ∪ { j ∈ T : σ_(j−1)^(i) = σ_j^(i) = −1 }`,
  `I_i = U ∪ { j ∈ T : σ_(j−1)^(i) = σ_j^(i) = +1 }`   (paper Lemma 8.1, display (8.1)),

and the system on six palettes `P_0,…,P_5 ⊆ Fin k`:

  (C1) `1 ≤ |P_i| ≤ k−3`                       general-k palette bound (R5, Prop. 5.6)
  (C2) `P_i ∩ O_i ≠ ∅` and `P_i ∩ I_i ≠ ∅`      Lemma 8.1
  (C3) `P_i ∩ P_(i+1) = ∅`, indices mod 6      Corollary 5.4, display (5.7)
  (C4) no two of the six palettes `A,B` have `A ∪ B = Fin k`      m6, Theorem 1 (general k)
  (C5) at most three of the six have `|P_i| = k−3`               m6, Theorem 2 (general k)

At `k = 6`, (C4) says exactly: no two palettes are complementary 3-element sets. (C5) says: at
most three are ternary. Both are true theorems about weak measurable colourings (m6), so they may
not be dropped from a faithful model; the question is whether they *bind*.

**Two remarks on faithfulness, both needed for the conclusion.**

* (C4) is applied at a.e. `e`, at the six positions of one `R`-orbit — the form m6 uses in the
  proof of its Theorem 2: if the orbit at a positive-measure set of `e` carried a pair `A, A^c`,
  then the measurable sets `B_A` and `B_A^c` would both have positive measure, contradicting
  Theorem 1. So the orbit-level constraint implemented here is the one the paper's inputs give.
* (C5) is applied at the same six positions; m6's Theorem 2 is exactly `#{j : |P_x(R^j e)|=3} ≤ 3`.

---

## 2. Theorem 1 (shrink lemma)

For `k ≥ 5` let `(P_0,…,P_5)` satisfy (C1)–(C3) for some sliver data `(O_i, I_i)`. Then there are
`Q_i ⊆ P_i` with `|Q_i| ≤ 2` satisfying (C1)–(C3) for the same data.

*Proof.* Fix `i`. If `|P_i| ≤ 2`, put `Q_i = P_i`. Otherwise `|P_i| ≥ 3`, so by (C2) choose
`o ∈ P_i ∩ O_i` and `n ∈ P_i ∩ I_i`. If `o ≠ n` put `Q_i = {o,n}`; if `o = n` choose any
`w ∈ P_i \ {o}` (nonempty because `|P_i| ≥ 3 > 1`) and put `Q_i = {o,w}`. In both cases
`Q_i ⊆ P_i`, `|Q_i| = 2`, and `Q_i` meets `O_i` and `I_i`. Then:

* (C1): `1 ≤ |Q_i| ≤ 2 ≤ k−3` because `k ≥ 5`.
* (C2): by construction.
* (C3): `Q_i ∩ Q_(i+1) ⊆ P_i ∩ P_(i+1) = ∅`.

The six choices are independent, so the construction is simultaneous. ∎

Note what the proof does *not* use: no arithmetic of the sliver sets beyond (C2), no information
about the ray geometry, no information about `ℓ`. Only the inequality `2 ≤ k−3`.

## 3. Corollary 1 (the class of powerless constraints)

Call a predicate `Φ` on six-tuples of palettes **pair-satisfied** if `Φ(Q)` holds for every
`Q` with `|Q_i| ≤ 2` (`i = 0,…,5`).

**Theorem.** For every `k ≥ 6`, every `ℓ ∈ {3,…,k}`, every ray geometry and every pair-satisfied
`Φ`: `(C1)-(C3) ∧ Φ` is satisfiable if and only if `(C1)-(C3)` is.

*Proof.* `(⇒)` trivial. `(⇐)` apply Theorem 1 and then `Φ`. ∎

**Membership.** (C4) is pair-satisfied for `k ≥ 6`: `A ∪ B = Fin k` forces
`|A| + |B| ≥ k ≥ 6 > 4 = 2 + 2`. (C5) is pair-satisfied for `k ≥ 6`: `k − 3 ≥ 3 > 2`. So is any
"at most `N` palettes of size ≥ 3", "no two palettes of size ≥ 3 are disjoint", "`Σ_i |P_i| ≤ 15`"
(the mean-`5/2` form of m6's Theorem 2), etc.

**Non-vacuity of the class, and of its complement.** The class contains two genuine theorems about
colourings (m6's Theorem 1 and Theorem 2), so it is not a strawman. It is also a proper class: the
restriction `|P_i| ≥ 3` is *not* pair-satisfied and it does bite — `17` satisfiable geometries at
`(k,ℓ) = (6,6)` instead of `177`; restricting the six palettes to be pairwise distinct also bites
(`125` instead of `177`); `0 ∈ P_i` for all `i` gives `0` geometries, as it must, since it
contradicts (C3). So the hypothesis of the theorem is doing real work in both directions
(`cal_liveness.py`, §4).

## 4. Theorem 2 (exact counts; the tightening changes nothing)

Exhaustive decision over all `6^(ℓ−1)` ray geometries (`c_0 = 0` is a rotation symmetry), exact
integer bitmask arithmetic, no floating point. Variants: `base` = (C1)-(C3); `C4`, `C5`, `C4C5`;
`cap2` = (C1)-(C3) with the upper bound replaced by 2; `C4C5cap2`; control `C5b` = "at most two
of size `k−3`".

| k | ℓ | geometries | base | C4 | C5 | C4C5 | cap2 | C4C5cap2 | C5b (control) |
|---|---|-----------|------|----|----|------|------|----------|----------------|
| 6 | 3 | 36     | 36   | 36 | 36 | 36   | 36   | 36       | 36   |
| 6 | 4 | 216    | 216  | 216| 216| 216  | 216  | 216      | 216  |
| 6 | 5 | 1296   | 225  | 225| 225| 225  | 225  | 225      | 225  |
| 6 | 6 | 7776   | 177  | 177| 177| 177  | 177  | 177      | 177  |
| 7 | 3 | 36     | 36   | 36 | 36 | 36   | 36   | 36       | 36   |
| 7 | 4 | 216    | 216  | 216| 216| 216  | 216  | 216      | 216  |
| 7 | 5 | 1296   | 1296 |1296|1296| 1296 | 1296 | 1296     | 1296 |
| 7 | 6 | 7776   | 2593 |2593|2593| 2593 | 2593 | 2593     | 2593 |
| 7 | 7 | 46656  | 4109 |4109|4109| 4109 | 4109 | 4109     | 4109 |

(`k = 8`, `ℓ ≤ 6` was also run before the time cutoff: `36, 216, 1296, 7776` for both base and
`C4C5`, i.e. also unchanged; `ℓ = 7,8` at `k = 8` were not run.)

The `base` column is an independent re-derivation of m5's table (`INTERFACE-CSP` Theorem 1) and
reproduces it exactly — `36/36, 216/216, 225/1296, 177/7776` at `k = 6`; `36, 216, 1296, 2593, 4109`
at `k = 7` — which calibrates the implementation against m5's two algorithms. On top of that, the
`C4C5` column equals `base`, `cap2` equals `base`, and `C4C5cap2` equals `cap2` in every row: the
exhaustive computation confirms Theorem 1's prediction and adds that the *pair stratum is not
smaller* than the whole model space at any `ℓ` or geometry.

**Consequence for Step 1 (the priority item of the brief).** At `k = 6` the tightened CSP is
satisfiable for every interface length:

| ℓ | tightened CSP |
|---|---------------|
| 3 | SAT for all 36 geometries (m5's alternating outsider pair `{3},{4},…` is already pair-stratum) |
| 4 | SAT for all 216 geometries (`{4},{5},…`) |
| 5 | SAT for 225 of 1296 geometries (m5's witness `{5},{1,4},{5},{1,4},{5},{1,4}`, all sizes ≤ 2) |
| 6 | SAT for 177 of 7776 geometries (m5's witness `{1,4},{2,5},…`, all sizes 2) |

So there is **no `(ℓ, sign matrix)` at `k = 6` at which (C1)–(C5) is unsatisfiable**, and Step 1 is
decision-negative. The INDUCTION LEMMA is not needed for that conclusion and could not rescue the
route: the conclusion is not "UNSAT, hence `χ ≥ 7`" but "SAT at every `ℓ`, hence nothing".

This does not contradict m6. Theorems 1 and 2 of m6 are true statements about weak measurable
colourings; m5's witnesses show that they are *satisfied* by the models, i.e. they carry no
satisfiability content at the interface. The same holds for the k-general forms, so there is no
overshoot at `k = 7` either: the tightened system at `k = 7` is satisfiable at exactly the base
geometries (`36, 216, 1296, 2593, 4109`), and in particular none of the `k = 7` instances that are
UNSAT can be blamed on the tightening — by Corollary 1 they are already UNSAT without it.

## 5. What the surviving model space is (the input for the next strengthening round)

By Theorem 1 the faithful model space that the next round must kill lies entirely in the pair
stratum. Its exact shape at `k = 6`:

* **`ℓ = 6`** (`U = ∅`, so `O_i ∩ I_i = ∅`): every palette has size exactly `2`, one label from
  `O_i` and one from `I_i`; the `cap2+min2` scan gives `177`, i.e. no size-1 or size-3 palette is
  ever needed. The `177` satisfiable geometries carry `1728` pair models in total, with per-geometry
  counts `1 : 52, 4 : 5, 6 : 48, 11 : 48, 34 : 12, 36 : 12` (min 1, median 6, max 36).
* **`ℓ = 5`** (`U = {5}`): palettes are `{5}` or `{5,x}` or pairs; `225` geometries, `35320` pair
  models, min 4 per geometry.
* The `52` geometries with a *unique* pair model are structurally uniform: the unique model is
  `3`-periodic, `P_(i+3) = P_i`, and its three distinct palettes are pairwise disjoint 2-sets
  partitioning `Fin 6` (verified for all `52`, listed in `cal_fragile.json`). These are the
  geometries where a new constraint has the best chance: one constraint applied to one of the `52`
  removes it at once. Conversely a geometry carrying 36 models needs a constraint that cuts all 36.

**Remark (field-level form, not machine-checked).** The shrink also applies to a whole palette
field `P_x : Angles → Finset (Fin k)`, not only to one orbit: on the measurable set where
`|P_x(e)| ≥ 3` choose `o(e) = min(P_x(e) ∩ O_x(e))`, `n(e) = min(P_x(e) ∩ I_x(e))` and put
`Q_x(e) = {o(e), n(e)}` when `o(e) ≠ n(e)`, else `{o(e), w(e)}` with `w(e) = min(P_x(e) \ {o(e)})`.
Each `o, n, w` is measurable (its value is a finite Boolean combination of the measurable sets
`{e : λ ∈ P_x(e)}`, `{e : λ ∈ O_x(e)}`, `{e : λ ∈ I_x(e)}` — m6's `paletteSet_measurable` is the
input), so `Q_x` is a measurable selection, (C1)–(C3) and the a.e. statements are preserved, and
`Q_x` has no palette of size ≥ 3 at all. Consequently **field-level** constraints which are
satisfied by every field with `|Q| ≤ 2` are powerless too — in particular the cross-orbit form of
Theorem 1 ("at a centre `x`, at most one of `A`, `A^c` is palette-positive on a set of positive
measure", which is stronger than the within-orbit (C4) used here).

**Why this does not contradict the A.E. COLLAPSE (m8).** The shrink preserves (C1)–(C3) only. It
destroys the exactness relation between the palette and the cluster colours of any colouring, i.e.
the palette-transfer condition (5.2)/(H2) that makes the palette system *equivalent* to a colouring
(m7's collapse, m8's a.e. collapse). That is the whole content of this no-go: the interface
language cannot distinguish a palette from a 2-element subset of it. **Moral for the next round:**
any `k = 6` argument of the §5–§8 type must use the transfer relation (5.2) *directly* — it must
speak about the colours of points other than `x`, e.g. the six radius-1 points `x + dir e_i` and
their mutual unit edges — because every constraint obtained by *deriving* conditions on the six
palette sets alone is pair-satisfied and hence powerless.

**Specification item forced by Theorem 1 (call it S7, adding to m5's S1–S6).**
A replacement mechanism that argues at a cyclic centre must exclude at least one pair-stratum
model, i.e. it must fail on a six-tuple with all `|P_i| ≤ 2`.
*Test:* run the proposed constraint against the pair-stratum models of `cal_fragile.json` (and
those of the `ℓ = 5` geometries); if it holds on all of them at every geometry, Theorem 1 proves it
is powerless and the mechanism cannot conclude. Both m6 constraints fail this test.

## 6. Machine-checked statements

`PaletteShrink.lean` (Lean 4.33.1 + Mathlib; no `sorry`; `#print axioms` =
`[propext, Classical.choice, Quot.sound]`):

* `PaletteShrink.exists_small_subset` — the pointwise shrink (Theorem 1's core).
* `PaletteShrink.union_ne_univ`, `PaletteShrink.card_ne_top` — (C4), (C5) are vacuous on the
  `|P| ≤ 2` stratum for `k ≥ 6`.
* `PaletteShrink.c4_of_pair`, `PaletteShrink.c5_of_pair` — the two constraints as pair-satisfied
  predicates.
* `PaletteShrink.neutral_of_pair_satisfied` — **Corollary 1 in full generality**: for `k ≥ 6`,
  any sliver data `O,I`, any `Φ` satisfying `(∀ Q, (∀ i, |Q_i| ≤ 2) → Φ Q)`, and any model `P` of
  (C1)-(C3), there is a model `Q` of (C1)-(C3) with `Φ Q`.
* `PaletteShrink.neutral_c4_c5` — the conjunction of (C4) and (C5) is neutral.

`Tightened.lean` (imports the above and m5's `InterfaceStates`, copied verbatim into
`M5Interface.lean` with attribution and not modified):

* `InterfaceStates.HasC4`, `InterfaceStates.HasC5` — m6's constraints at the orbit level.
* `InterfaceStates.exists_tightened_of_isModel` — every (C1)-(C3) model can be replaced by a
  (C1)-(C5) model, at any `k ≥ 6`.
* `InterfaceStates.tightened_silent_at_six` — **the end-to-end statement**: at `k = 6`, for `ℓ = 3`
  and `ℓ = 4` for *every* sign matrix, and for `ℓ = 5`, `ℓ = 6` at m5's explicit geometries, there
  is a palette system satisfying (C1)-(C5).
* `InterfaceStates.P6_has_C4_C5` — m5's `ℓ = 6` witness already satisfies both constraints.

## 7. Which outcome this reaches

The brief's terminal outcomes: this is the **no-go component of L4**, in a stronger form than the
previous run's. Previous run: *the state level (C1)-(C3) decides `k = 4` completely, `k = 5` at
`ℓ = 5`, and is silent at `k = 6`* (m5). This run's addition: *silence at `k = 6` is not repaired by
any true constraint that is vacuous on the pair stratum, in particular not by m6's (C4)+(C5), and
not by any of their `k`-general forms* — a theorem, not a count. Together with m5's S1–S6 the
specification of a replacement now has the sharp test S7 of §5, and §5 supplies the exact finite
object that test must be run against. L1, L2, L3 and L5 are not reached; `χ(ℝ²)` is not decided
here and no `χ ≥ 7` claim is made.

## 8. What is not claimed, and what was not done

* No claim about `χ(ℝ²)`. In particular the tunnel "tightened CSP UNSAT ⟹ `χ ≥ 7`" is *not* used;
  it is void because the tightened CSP is SAT at every `ℓ`.
* No claim that the interface route cannot decide `k = 6` at all: Corollary 1 excludes exactly the
  pair-satisfied constraints. A constraint that fails on some pair-stratum model — e.g. one using
  the geometry of the six radius-1 points around the centre, the two-centre/translation structure
  of m8, or Lemma 5.5 separation — is *not* excluded, and §5 says where to look for it.
* The `k = 7` calibration promised in the direction was reduced to Corollary 1 and does not need a
  separate computation: the tightening is neutral at every `k ≥ 6`, so it cannot overshoot at
  `k = 7`. I did *not* compute the palette field of the hexagonal 7-colouring; that check would be
  vacuous anyway, since in the hexagonal tiling a point lies in the closure of at most three cells,
  so every palette there has size ≤ 3 < k−3 = 4 and both m6 constraints hold trivially.
* `k = 8`, `ℓ ∈ {7,8}` and `ℓ ≥ 8` at `k ∈ {ℓ, ℓ+1}` were not run. They are irrelevant to the
  claims above, which are uniform in `k ≥ 6` and proved, not enumerated.

## 9. Reproduction

From the project root:

```
cd .ultramath/smwfk0ybk/m16
python3 cal_csp.py        # base vs tightened counts, k=6,7,8 (k=8 ell<=6 before the cutoff)
python3 cal_variants.py   # the table of section 4  (~5 min)
python3 cal_liveness.py   # the non-vacuity controls of section 3
python3 cal_slack.py      # per-geometry pair-model counts (section 5)
LEAN_PATH=$PWD:$LEAN_PATH lean -o M5Interface.olean M5Interface.lean
LEAN_PATH=$PWD:$LEAN_PATH lean -o PaletteShrink.olean PaletteShrink.lean
LEAN_PATH=$PWD:$LEAN_PATH lean Tightened.lean    # prints the axiom sets
```

Files: `cal_csp.py`, `cal_variants.py`, `cal_liveness.py`, `cal_slack.py`,
`cal_csp_results.json`, `cal_variants.json`, `cal_slack.json`, `cal_fragile.json`,
`PaletteShrink.lean`, `Tightened.lean`, `M5Interface.lean`.
