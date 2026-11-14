# The palette bridge: why "two labels" is a five-label fact

**Module 1 of a modular exposition + audit.** Owner: supervisor/simplify-exposition.
Block: 2026-11-14 05:10–05:40 UTC. Everything here is written for the Mathathon referee,
not as a project summary: it isolates ONE conceptual bridge, states exactly what each
hypothesis buys, and separates what is machine-checked from what rests on the paper.

**Grades used throughout** (never mixed):

| code | meaning |
|---|---|
| **M** | machine-checked in the pinned Lean 4.34.1 / mathlib `d13f23b` development, statement read from source |
| **P** | paper argument, read in `attachments/here-are-three-files-ni5n/paper.pdf`, not formalised |
| **E** | exact finite computation performed in this block, exhaustive over a declared finite space (`checks/`) |
| **C** | candidate / this block's own reasoning, *not* independently reviewed |

---

## 1. The bridge in one page

> **Bridge (Proposition 5.6, paper §5.4).** For a weak measurable 5-colouring and every
> centre `x`, the maximal palette satisfies `1 <= |P_x(e)| <= 2` for almost every direction
> `e`. **M**: `OAI.EuclideanFiveColor.palette_cardinality`
> (`lean/OAI/Geometry/PlaneColoring/BinaryPalettes.lean:260`).

Nothing downstream of §5 works without it:

| consumer | use of `|P| <= 2` | source |
|---|---|---|
| §6 state separation, transition graphs | pairs, not triples, are the states | `States.lean:319`, `Accumulation.lean:161,361` |
| §7.1 interface at a cyclic centre | the triangle case needs `|P| <= 2 = 5 - 3` | `Interfaces.lean:78` |
| §8 cycle exclusions | "palette bound forces every palette to be a pair" | `Exclusion.lean:130` |

Grep evidence: `rg -n 'palette_cardinality' lean/OAI` returns exactly those five call
sites. So the bridge is not decorative: it is the single place where the number **5**
enters the geometric half of the proof, and therefore the exact place where a six-colour
argument must fail or be replaced (`results/K6-BARRIER.md`).

**The bridge's logical shape.** The paper proves it by contradiction: a palette cannot
contain a fixed triple on a positive-measure set of directions, because then a *whole
circle* of centres would be "binary" for a fixed pair, and binary centres are uniformly
separated — too many of them for a compact circle. The three ingredients are

1. **exclusion**: at a.e. direction, the whole radius-one circle at `x + e` is coloured
   outside `P_x(e)`  (paper (5.2), **M** `palette_first_exclusion` / `ae_circle_palette_exclusion`);
2. **arity**: the complement of a 3-element subset of a **5**-element label set has
   **2** elements, and "meets a fixed 2-set a.e." is exactly binarity;
3. **separation**: distinct binary centres for a fixed pair are `delta_*`-apart, with
   `delta_* > 0` absolute (**M** `binary_centers_separated`).

Ingredient 2 is where five labels are spent. Ingredient 3 is where all the hard analysis
sits. Ingredient 1 is where weak measurability is spent.

---

## 2. The chain, node by node

| node | statement | grade | exact source |
|---|---|---|---|
| **A** | palettes: `P_x(e) = {i : e in D_{x,i}}`, `D_{x,i}` = essential union over circle traces `b` of `{b_i > 0}`; `P_x` nonempty a.e. | **M** | Def. 5.1; `Palettes.lean:10-40` (`paletteSet`, `palette`, `palette_nonempty`) |
| **B** | (5.2): for `sigma⊗sigma`-a.e. `(e,v)`, `c(x+e+v) not in P_x(e)`, and symmetrically `not in P_x(v)` | **M** | `PaletteDensity.lean:121,135,143` (`palette_first_exclusion`, `palette_second_exclusion`, `palette_transfer_pair`) |
| **C** | (5.7) `P_x(e) ∩ P_x(Re) = ∅` for a.e. `e`, `R` = rotation by `pi/3` | **M** | `PaletteTransport.lean:444-454` (`palette_sixty`, `palette_sixty_disjoint`) |
| **D** | a binary centre's selection is unique a.e. and flips under `R` — the paper's (5.8) | **M** | `BinaryPalettes.lean:11` (`binary_alternation`), plus `binary_pair_distinct` |
| **E** | Lemma 5.5: binary centres for a fixed pair are `delta_*`-separated, `delta_* > 0` absolute, every `k` | **M** | `BinaryPalettes.lean:123` (`binary_centers_separated`) via `BinaryDynamics.lean:410,497` |
| **F** | a `delta_*`-separated set in a compact metric space is finite, so a positive-measure set of distinct directions cannot inject into it | **P** | paper §5.4, last paragraph |
| **G** | no triple sits in `P_x(e)` on a positive-measure set ⇒ Prop 5.6 | **M** | `BinaryPalettes.lean:252,260` (`palette_triple_null`, `palette_cardinality`) |

Two fidelity notes, checked in source rather than trusted from summaries:

* **"Binary" means MEETS, not CONTAINS.** Paper §5.3: `x` is binary for `{i+,i-}` iff
  `P_x(e) ∩ {i+,i-} ≠ ∅` for a.e. `e`. The Lean definition is literally that disjunction:
  `BinaryCenter c hc x i j := ∀ᵐ t, t ∈ paletteSet c hc x i ∨ t ∈ paletteSet c hc x j`
  (`BinaryPalettes.lean:9`). Good: the paper's remark *"even if other traces add further
  labels to the maximal palette"* is honoured, and the k = 6 transfer below must not
  silently strengthen it to containment.
* **The formalised Lemma 5.5 does not use the paper's proof.** The paper runs six
  conjugate expanding circle maps `F_j` and a bounded-distortion argument (**P**, §5.3,
  eqs (5.9)–(5.11)). The Lean runs a single map `binaryCircleMap d` with expansion
  (`BinaryDynamics.expansion_alternation_false`, `binary_alternating_invariant_false`:
  a measurable `2π`-periodic `A` that flips under `+π/3` cannot be a.e. invariant under
  `binaryCircleMap d` for any `0 < d < delta`) plus the transport identity
  `binary_transport_invariant`. The *statement* is the paper's; the *proof* is a
  different, shorter route. Consequence for referees: the paper's constants
  (`c0, C0, L, delta_*` of (5.10)) are **not** certified by the formal proof, and any
  argument that needs their explicit form is still paper-level.

---

## 3. Why each hypothesis is necessary

Five hypotheses are in play. For each: what breaks without it, and the cheapest witness.

### H1 — weak measurability of the colouring (`WeakColoring`)  [used at A, B]
Definition 5.1 builds palettes out of *typical* circle samplings, i.e. density points of
the colour classes. Without measurability there are none: if a colour class is a Bernstein
set it has no density point anywhere (a density point would give a measurable subset of
positive measure inside the class, and a Bernstein set contains none), so the family of
typical samplings is empty, `W_x` is empty, and `P_x(e) = ∅` a.e. — the *lower* bound of
Prop 5.6 is already false. **Grade P** (standard fact stated, not formalised here).
This is also why the bridge is stated for weak measurable colourings: the paper's
Theorem 1.3 does the work of getting there, and that transfer is Step 2–3 of
`results/SPINE.md`, not this module.

### H2 — the 60-degree exclusion (5.7)  [used at D]
`palette_sixty` is what turns "meets the pair" into "exactly one member of the pair, and
it flips at `pi/3`". Drop it and no alternation, hence no hypothesis for the expansion
argument, hence no `delta_*`. This is a genuine theorem about the colouring (it is
Lemma 5.2 plus Lemma 5.3's transport machinery), not a bookkeeping convention.

### H3 — the label count is exactly 5  [used only at the arity step]
The triple `A ⊆ P_x(e)` has complement `I \ A` of size `5 - 3 = 2`. At `k = 6` the same
argument yields a complement of size 3, and "meets a fixed 3-set a.e." is **not** binarity
for any pair. Section 4 makes this exact: the pair case is *rigid*, the triple case is not.
The general count is `|P_x(e)| <= k - 3` (**C**, re-derived here; agrees with
`results/K6-BARRIER.md` §1 and I found no gap in it — see §5).

### H4 — typicality plus constant sequences  [used at the arity step]
The paper needs that the *actual* radius-one circle sampling at `x + e` is itself a trace
at `x + e`, so that the circle's colours are counted as belonging to the palette there.
Definition 5.1 permits constant sequences, and §5.4 checks that for a.e. `e ∈ B` the
sampling is typical. Without the "constant sequences permitted" clause the palette at
`x + e` could be smaller than the circle's colour set and the bridge would not close.
**M**, via `BinaryPalettes.lean:190-213` (`exact_sample_isTrace`, `typical_sample_palette`).

### H5 — absoluteness of `delta_*`  [used at F]
`binary_centers_separated` gives one `delta > 0` for all colourings, all `k`, all pairs.
That is what makes step F a compactness argument rather than a statement about one
colouring. The formal proof's `delta` comes from `binary_dynamics_controls` and is
absolute in exactly this sense (no colouring parameter appears in its type). **M**.

---

## 4. The exact combinatorial content: pairs are rigid, triples are not

The arity step H3 has a finite shadow, and it is decidable. A *palette field* of period
`N` (`6 | N`) on label set `I` is a map `P : Z/N -> nonempty subsets of I` satisfying
(5.7) `P(t) ∩ P(t + N/6) = ∅`; it is *binary for the pair `{i,j}`* when
`P(t) ∩ {i,j} ≠ ∅` for every `t`; it is *`T`-confined* when `P(t) ⊆ T` for all `t`.

All counts below are exhaustive over the stated finite space, by
`checks/triple_dichotomy.py` (**E**); nothing is sampled and no search is truncated.

| space | fields | non-binary | of which 3-cycles |
|---|---|---|---|
| `k = 6`, `T` a fixed 3-set, `N = 6`, sizes 1..3 | 234 | 132 | 6 |
| `k = 6`, `T` a fixed 3-set, `N = 12`, sizes 1..3 | 54 756 | 50 880 | 36 |
| `k = 6`, `T` fixed, sizes 2..3 (any `N`) | 0 | 0 | 0 |
| `k = 5`, `T` a fixed pair, `N = 6` | 2 | 0 | — |

Three readings, in increasing order of usefulness:

1. **Pairs leave no room.** With `|T| = 2`, nonemptiness plus (5.7) force `P(t)` to be a
   singleton and `P(t + 60°)` to be the other singleton: the field is exactly the
   paper's alternation (5.8). This is the combinatorial reason the five-label proof
   closes, and it is why H3 is *the* five-label hypothesis.
2. **Triples leave room, and a lot of it.** At `k = 6` a `T`-confined field can avoid
   every pair on some directions in 132 ways already at period 6. So the fact that
   "ternary circles exist" (`results/K6-BARRIER.md` §1) is not a quirk of one example;
   the residual object is genuinely non-rigid.
3. **Retraction (mine, this block).** I first believed the triple case was forced into a
   canonical 3-cycle `{0},{1},{2},{0},{1},{2}` (`l(v+180°) = l(v)`, `l(v+60°) ≠ l(v)`),
   which would have made a Lemma-5.5 analogue for 3-cycles the natural next target. The
   count refutes it: 132 non-binary fields, only 6 of them 3-cycles. The reason is that
   (5.7) relates `S(v)` to `S(v+60°)` only, so `S(v)` and `S(v+120°)` may overlap and
   `S` may take 2-element values. **Do not build on the 3-cycle claim.**

---

## 5. Transfer ledger: what the printed method gives at `k = 6`, and what it does not

**What survives (I checked each step; **C** but elementary).** The same argument with
`|A| = k - 2` in place of a triple gives, for every weak measurable `k`-colouring,
`1 <= |P_x(e)| <= k - 3` a.e.: the complement `I \ A` is a pair, step B colours the circle
at `x + e` by that pair, step H4 makes `x + e` binary for it, step E separates the centres
`x + e` as `e` runs over a positive-measure set of directions, and step F makes that set
finite. At `k = 6` this is `|P| <= 3`, and it is empty content for `|P| <= 2`.

**What fails.** `|P| <= 2` at `k = 6` would need the argument to run with `|A| = 3`; then
`I \ A` has 3 elements and the conclusion at `x + e` is only "the palette meets a fixed
3-set a.e.", which is not binarity. By §4 item 2 that is not a bookkeeping gap: the
constraint level genuinely admits non-binary `T`-confined fields. Therefore

> **(Missing lemma M6, stated exactly.)** For every weak measurable 6-colouring, every
> centre `y` and every 3-element label set `T`, at least one of the three sets
> `{v : P_y(v) ∩ T = {l}}` (`l ∈ T`) is angular-null — equivalently, `y` cannot meet a
> fixed triple `T` on a full-measure set of directions without being binary for some pair
> in `T`.

This is the precise hole, and it is narrower than "prove `|P| <= 2`": it is a statement
about *one centre and one triple*, i.e. one circle, not about all centres. Two remarks
that a worker can use immediately:

* It is **not** implied by (5.7) alone (§4) and **not** implied by the `k = 6` palette
  bound `|P| <= 3`, since the 132 witnesses respect both.
* It is **not** a statement about colourings of the circle: the unit-distance graph on a
  circle is a disjoint union of six-cycles and is 2-colourable, so a ternary circle
  colouring is not by itself absurd (already noted in `results/K6-BARRIER.md` §1).

---

## 6. Dependency diagram

`supervisor/simplify-exposition/artifacts/palette-bridge.dot` (render with
`dot -Tsvg`). Skeleton:

```
Def 5.1 (palettes, A) --(5.2)--> B --(R-step)--> C=(5.7) --(pair complement)--> D=(5.8)
                                                            |                       |
                        H1 weak measurability --------------+                       |
                                                                                    v
Lemma 5.2 transport -----> E (Lemma 5.5, delta_*) <--- expansion / ergodicity
                                   |
                                   v
                     F (compact => finitely many) --> G (Prop 5.6, |P|<=2)
                                   ^
                                   |
                     H3: |I| = 5  (complement of a triple is a pair)
```

---

## 7. Verification ledger (exact commands and evidence)

| what | command | result |
|---|---|---|
| palette bound is consumed 5×: §6, §7, §8 | `rg -n 'palette_cardinality' lean/OAI` | `Accumulation.lean:161,361`, `Interfaces.lean:78`, `Exclusion.lean:130`, `States.lean:319` |
| k = 5 rigidity, k = 6 non-rigidity | `python3 checks/triple_dichotomy.py` (`checks/triple_dichotomy.json`) | 2 fields / 0 non-binary at k = 5; 234 / 132 / 6 at k = 6, N = 6; 54 756 / 50 880 / 36 at N = 12 |
| hypothesis-by-hypothesis source audit | `sed -n` reads of `Palettes.lean`, `PaletteDensity.lean`, `PaletteTransport.lean`, `BinaryPalettes.lean`, `BinaryDynamics.lean` | statements quoted in §2; binary = meets confirmed at `BinaryPalettes.lean:9` |
| axiom certificate for the bridge | `supervisor/simplify-exposition/lean/run_axioms.sh` | **FAILED THIS BLOCK**: 600 s timeout, no output (re-elaboration under the pinned toolchain). Needs a backgrounded run; do not treat as evidence either way. |

**What these do NOT establish.** (i) Nothing here is a statement about `chi(R^2)`;
`|P| <= 2` is a lemma inside a five-colour proof, and (M6) is a lemma inside a
six-colour *attempt*. (ii) The counts in §4 are palette-constraint statements, not
colouring-level statements. (iii) The Lemma-5.5 statement is machine-checked, its paper
constants are not.

---

## 8. Steps delegated to a source (assumptions, labelled)

* **D1.** Lemma 5.2's two-direction exclusion (5.2), including the two-dimensional
  density-point estimate: **M** in Lean, **P** in the paper; the *paper's* constants and
  the "countable generating trace family" bookkeeping are not re-derived here.
* **D2.** Lemma 5.5's absolute `delta_*`: **M** as a statement; the paper's six-map
  expansion constants (**P**) are not certified by the formal route.
* **D3.** The rigidity theorem (§2–3 of the paper) and the transfer (§4): untouched by this
  module; see `results/SPINE.md` and the verification supervisor's directory.
* **D4.** The k = 6 palette bound `|P| <= 3`: **C** here (re-derived, no gap found),
  consistent with `results/K6-BARRIER.md` §1, not formalised.
