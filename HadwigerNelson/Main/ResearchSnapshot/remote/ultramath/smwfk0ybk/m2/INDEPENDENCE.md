# The tightening (C4)+(C5) at k = 6 is genuine but decides nothing, and (C5) is a theorem of (C3)+(C4)

Member m2, direction d3 (board D4, *constraint independence*). Everything below is about m5's
interface CSP `IS(6, l, σ)` (`m5/interface_csp.py`, `m5/INTERFACE-NOGO.md` §1) with m6's two
constraints added (`m6/proof.md`, Theorem 1 = (C4), Theorem 2 = (C5)). Nothing here re-derives
R1–R6 or any previous result; the m5/m6 statements are *cited* and used as the objects to be
tested for logical dependence.

**Verdict for Step 1, immediately.** With (C4) and (C5) added at k = 6 the CSP is still
**satisfiable for every (l, sign matrix) that was satisfiable before**: the SAT count does not
move at a single one of the 9 324 instances (36 + 216 + 1296 + 7776). So the tightened CSP at
k = 6 does **not** yield `χ(ℝ²) ≥ 7`; no terminal outcome is reached this round, and the
induction lemma is moot for it. The exact models that survive are dumped as 654 explicit objects
(`survivors.json`) — those are precisely the objects that the next constraint (C6) has to kill.

---

## 1. What is decided, with counts

### 1.1 Orbit level (one π/3-orbit, no geometry, no (C2))

The set of six-palette orbits with (C1) `1 ≤ |P_i| ≤ 3` and (C3) `P_i ∩ P_{i+1} = ∅` cyclically
has `tr(A^6) = 10 581 680` elements (independent C enumeration, `orbit.c`; reproduces m6's table
exactly). Splitting by the tightening:

| predicate | count |
|---|---|
| (C1) ∧ (C3) | 10 581 680 |
| (C4) — no two palettes complementary (`A ∪ B = Fin 6`) | 9 752 220 |
| ¬(C4) | 829 460 |
| ¬(C4) via an **adjacent** complementary pair | 751 700 |
| ¬(C4) only via a pair at circular distance **2 or 3** | 77 760 |
| ¬(C5) — four or more ternary palettes | 27 740 |
| (C4) ∧ ¬(C5) | **0** |
| (C5) ∧ ¬(C4) | 801 720 |
| ¬(C5) while the *mean* palette size is ≤ 5/2 | 22 680 |

Ternary histogram: `0:2 789 820, 1:4 739 400, 2:2 552 040, 3:472 680, 4:27 000, 5:720, 6:20`
(the 20 all-ternary orbits are m6's alternating `A, Aᶜ, A, Aᶜ, A, Aᶜ`).

### 1.2 Geometry level (k = 6, all ray geometries, (C2) included)

`6^(l−1)` cell vectors per `l` (first cell normalised by the π/3 rotation symmetry), exactly as
in m5. Labels `0..5`; `O_i = U ∪ {j : σ_{j−1}^{(i)} = σ_j^{(i)} = −1}`,
`I_i = U ∪ {j : … = +1}`, `U =` labels `≥ l`.

| l | geometries | SAT (C1)–(C3) | SAT (C1)–(C5) | status changed | geometries with a (C4)-violating model | with a ≥4-ternary model | with a (C5)-model having a non-adjacent complementary pair |
|---|---|---|---|---|---|---|---|
| 3 | 36 | 36 | **36** | 0 | 36 | 36 | 36 |
| 4 | 216 | 216 | **216** | 0 | 216 | 216 | 216 |
| 5 | 1296 | 225 | **225** | 0 | 65 | 65 | 55 |
| 6 | 7776 | 177 | **177** | 0 | 29 | 29 | 17 |

(The `l = 3, 4` rows are m5's trivial construction: two outsiders alternating `{x}, {y}` satisfy
(C1)–(C5) for every geometry. So no constraint system that allows 1-label palettes on outsider
labels can ever refute `l = 3, 4`.)

Further exact facts about the survivors, each obtained by exhaustive search per geometry:

* every one of the 654 satisfiable geometries has a (C1)–(C5) model using **all six labels**
  (so no "unused label" constraint can bite);
* at every `l` there is a geometry with a (C1)–(C5) model having **exactly three ternary
  palettes** — the equality case of m6's Theorem 2 — and using all six labels
  (36 / 216 / 115 / 125 geometries respectively);
* number of (C1)–(C4) models: 571 070 at `l = 5`, 11 648 at `l = 6` (so the survivors are not a
  handful of isolated points).

## 2. Theorem R ((C5) is redundant given (C3) and (C4))

**Theorem R.** Let `k = 6`, `P_0,…,P_5 ⊆ Fin 6` with `P_i ∩ P_{i+1} = ∅` for `i ∈ ℤ/6` (C3) and
no two of the six palettes complementary ((C4)). Then at most three of the six are ternary
((C5)); the sharper form holds: the ternary positions form an independent set of the 6-cycle.
Consequently the mean palette size is `≤ (3·3 + 3·2)/6 = 5/2` (m6's second bound), and every
model of (C1)–(C3)–(C4) is a model of (C1)–(C5).

*Proof.* If `|P_i| = |P_{i+1}| = 3` then disjointness gives `|P_i ∪ P_{i+1}| = 6 = |Fin 6|`, so
`P_{i+1} = P_iᶜ`, contradicting (C4). Hence no two ternary positions are adjacent, i.e. they form
an independent set of `C_6`; an independent set of the 6-cycle has at most 3 elements (each of the
three disjoint edges `{0,1}, {2,3}, {4,5}` meets it at most once). ∎

Notes.

* (C1), (C2) and the ray geometry are **not used**. The implication is a property of the 6-cycle
  alone, so it holds at every `(l, σ)` and also for non-geometric palette tuples.
* Machine-checked: `Indep.lean` (`lean Indep.lean`, 2.4 s, exit 0, `#print axioms` =
  `[propext, Classical.choice, Quot.sound]`). `card_ternary_le_three` is the implication;
  `card_ternary_le_three_union_form` is the same from m6's literal form of (C4)
  (`A ∪ B = univ`), connected by `union_univ_iff_disjoint_of_card_three`.
* Exhaustive verification on all 10 581 680 orbits: `(C4) ∧ ¬(C5) = 0` (`orbit.c`).
* **Consequence for the swarm.** d1's system `(C1)–(C5)` *is* `(C1)–(C4)`: (C5) removes no model.
  And the induction lemma (d2) does **not** need m6's Theorem 2 at all — only Theorem 1 — because
  Theorem 2's orbit content is a two-line consequence of Theorem 1 plus (5.7).

## 3. Theorem N ((C4) is not redundant)

**(C4) is not implied by (C1)–(C3), even together with (C5).** Exact instances (verified in
`validate.py` from the geometric definition of the sign matrix, not from a table):

* non-adjacent complementary pair, `(C5)` true: `l = 3`, cells `(0,0,0)`,
  `P = ({3},{4},{0,1,3},{4},{3},{2,4,5})`. (C1), (C2), (C3) hold, two ternary palettes, and
  `P_2 = {0,1,3}`, `P_5 = {2,4,5}` are complementary at distance 3. Same phenomenon with
  `l = 5` (cells `(0,0,0,3,3)`) and `l = 6` (cells `(0,0,0,3,3,3)`).
* adjacent complementary pair: `l = 3`, cells `(0,0,0)`,
  `P = ({3},{4},{3},{4},{0,1,3},{2,4,5})` — again with only two ternary palettes.
* ≥ 4 ternary palettes: `l = 3`, cells `(0,0,0)`,
  `P = ({3},{4},{0,1,3},{2,4,5},{0,1,3},{2,4,5})`; also `l = 5`, cells `(0,0,0,3,3)`.

So the tightening is a genuine strengthening: (C2) alone leaves 36 / 216 / 65 / 29 geometries
(for `l = 3,4,5,6`) in which (C4) excludes models. But — by §1.2 — it never excludes the last one.

## 4. Defect: (C5) is *not* equivalent to the mean bound

`m6/proof.md` (§ "What this changes for L4") writes: "(C2) … `σ(E_x) ≤ π`; **equivalently** the
mean palette size is at most 5/2, and in every `R`-orbit at least three of the six palettes are
pairs (or smaller)". The last clause is the sharp statement (Theorem 2, first assertion); it is
**not** equivalent to the mean bound, and the mean bound does not imply it:

* orbit `(A, Aᶜ, A, Aᶜ, {u}, {v})` with `A` a triple: four ternary palettes, mean size
  `14/6 = 7/3 ≤ 5/2`. There are **22 680** such (C1)∧(C3) orbits at k = 6 (`orbit2.c`).
* Inside (C1)∧(C2)∧(C3) it survives too: `l = 5`, cells `(0,0,0,3,3)`,
  `P = ({1,4},{5},{0,1,4},{2,3,5},{0,1,4},{2,3,5})` has four ternary palettes, mean exactly `5/2`,
  and satisfies (C1),(C2),(C3) (`validate.py`). Counts of geometries with such a model:
  36 / 216 / 65 / 0 for `l = 3,4,5,6`.
* Similarly `σ(E_x) ≤ π` is an *average* statement: `f ≡ 6` on a set of directions of measure
  `2π/3` and `f ≡ 1` elsewhere gives `σ(E_x) ≤ π` with four-to-six ternary palettes on a
  positive-measure set. The pointwise orbit bound is the one to encode.
* **Implementation caution for d1:** if (C5) is encoded as `mean ≤ 5/2` (or as `σ(E_x) ≤ π`)
  rather than as "at most three ternary per orbit", the model set is strictly larger
  (36/216/65 geometries more at `l = 3,4,5`), and any UNSAT verdict obtained that way would be
  unsound.

## 5. Conclusion for Step 1 and for the next round

1. **Step 1 answer with the current tightening: SAT at every `l` and every sign matrix** —
   counts in §1.2, i.e. exactly m5's. `χ(ℝ²) ≥ 7` is **not** reached. Which of L1–L5 is reached:
   none of the terminal outcomes; this is the "SAT → need (C6)" branch of the brief.
2. The effective tightened system is `(C1)∧(C2)∧(C3)∧(C4)`; (C5) is free (§2). The whole
   non-redundant content of (C4) *beyond* what (5.7) already gives is the exclusion of
   **non-adjacent complementary triples** (distance 2 or 3, 77 760 orbits): adjacency is already
   excluded by (C3)+(C5), and conversely (C4) ⟹ (C5).
3. Any (C6) must kill the 654 explicit models in `survivors.json`. They include, at every `l`,
   models that (i) use all six labels, (ii) are extremal for m6's Theorem 2 (exactly three
   ternary palettes), (iii) at `l = 3,4` are m5's trivial alternating-outsider patterns. So a
   (C6) cannot be a size bound, a label-coverage bound, or a ternary-distribution bound; it must
   constrain *which* labels occur, or couple at least two centres.
4. For d2 (induction lemma): only (C4) needs transferring, and only for non-adjacent pairs. Note
   that m6's Theorem 1 is a **positive-measure** statement about the direction sets `B_A`,
   `B_{Aᶜ}`; its transfer to the six single directions of one orbit is *not* automatic and is the
   one place where non-exceptionality has to be produced.

## 6. Files and exact check commands

From the project root (`.scratch` here is my own `scratch/`, not a shared cache):

```
lean .ultramath/smwfk0ybk/m2/Indep.lean                                 # 2.4 s, exit 0, axioms clean
gcc -O2 -o .ultramath/smwfk0ybk/m2/scratch/o  .ultramath/smwfk0ybk/m2/orbit.c  && .ultramath/smwfk0ybk/m2/scratch/o
gcc -O2 -o .ultramath/smwfk0ybk/m2/scratch/o2 .ultramath/smwfk0ybk/m2/orbit2.c && .ultramath/smwfk0ybk/m2/scratch/o2
python3 .ultramath/smwfk0ybk/m2/indep.py              # procedure 1: DFS left-to-right, §1.2 + witnesses
python3 .ultramath/smwfk0ybk/m2/indep2.py             # procedure 2: forward DP + DFS right-to-left
python3 .ultramath/smwfk0ybk/m2/validate.py           # re-checks witnesses.json from the geometry
python3 .ultramath/smwfk0ybk/m2/mean_vs_count_csp.py  # mean bound vs count bound inside (C1)-(C3)
python3 .ultramath/smwfk0ybk/m2/models_structure.py   # 571 070 / 11 648 models, size profiles
python3 .ultramath/smwfk0ybk/m2/survivors.py          # writes the 654 surviving models
```

All nine commands were run from the project root against this directory and their output is as
quoted above.

| file | what it is |
|---|---|
| `INDEPENDENCE.md` | this report |
| `Indep.lean` | machine-checked Theorem R (2 theorems + the (C4)-form equivalence) |
| `orbit.c`, `orbit2.c` | orbit-level exhaustive enumeration (all 10 581 680 orbits), mean-bound counts |
| `indep.py` | decision procedure 1 + first counterexample extraction |
| `indep2.py` | decision procedure 2 (different algorithm: reachability DP over `(first,last)` pairs; right-to-left DFS for (C4)) |
| `validate.py`, `witnesses.json` | every witness re-checked from `sign(cos(θ_j − iπ/3))` sampled inside the ray cell, not from a sign table |
| `survivors.json` | one (C1)–(C5) model for each of the 654 satisfiable (l, geometry) pairs |
| `models_structure.py` | model counts and size profiles of the survivors |
| `mean_vs_count_csp.py` | whether the mean bound implies the orbit count bound inside (C1)–(C3) |

Agreement: procedures 1 and 2 give identical counts (36/216/225/177 and `flips = 0` at every `l`)
and both reproduce m5's independent implementation exactly. Three implementations, two of them
mine and of different algorithm, agree on all 9 324 instances.

## 7. What is not claimed

* Not a proof that no single-centre constraint can decide k = 6 — only that these two do not, and
  that the explicit survivors rule out the three natural families (size, label coverage,
  ternary distribution).
* The mean-vs-count defect does not affect m6's Theorems 1–2 as *theorems* (both are true and the
  count form is the strong one); it affects the claim that the two are equivalent, and any
  implementation that keeps only the mean bound.
* No new constraint is proposed here; §5.3 states exactly what a (C6) must be able to do.
