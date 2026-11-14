# The 6-cycle common interface: why `m6` cannot globalise, and the surviving multi-state obstacle

Source audit + one reduction. **No computation, no Lean build.** Read-only inputs: `States.lean`,
`BinaryPalettes.lean`, `Interfaces.lean`, `Coloring.lean`, `PaletteDensity.lean`; Astra's licensed
finite witnesses (as relayed); the source-chain correction L6 ∧ F6 ⟹ FullApprox6 ⟹ cover/mesh
contradiction. Grades: **[machine]** = in the tree; **[licensed]** = Astra-checked finite data;
**[proposed]** = mine, unverified.

**Naming.** `L6` = transition cyclic core locally finite; `F6` = common interface graph acyclic;
`B2` = the two-palette (binary) hypothesis of the interface layer; `T6 -> B2` is useful but supplies
neither L6 nor F6, and B2 is not a direct hypothesis of `HoleApprox` once L6 is known.

> # RETRACTIONS (later block, `FOUR-PALETTE-MODEL.md` §0)
>
> **R1.** The sentence "finite `m6` is not the restriction of ANY whole-circle trace field" is **withdrawn**.
> §2 below proves only: no *naive fixed-`J,K`* extension with an a.e. 60° flip exists. Whole-circle fields with
> more palettes are untouched, and Astra's four-palette field is one.
> **R2.** The proposed 6-word `({0,2}, {3,5}, {1,4}, {3,5}, {0,2}, {3,5})` of §4 is **not a licensed model**:
> for fixed `m6` `q = (0,3,3,3,0,0)` the side-allowed sets are `{2,3}` and `{0,5}`, and `{1,4}` meets neither.
> The "minimal surviving obstacle" is withdrawn.
> **R3.** Hence the corollary "every genuine 6-cycle must use ≥ 3 palettes" does **not** imply that a
> ≥ 3-palette 6-cycle survives — Astra's 4-palette field is exactly such a model. Only the two-palette case is
> closed; the ≥ 3-palette case remains the live question.

## 1. The exact premises of `two_state_impossible` [machine]

`States.lean:243`, verbatim signature:

    lemma two_state_impossible {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (hw : WeakColoring k c)
        (x : ℂ) (J K : Finset (Fin k)) (hcard : (Finset.univ \ (J ∪ K)).card ≤ 2)
        (s : Angles → Bool) (hs : Measurable s)
        (hJ : RealState hc x {t : ℝ | s (t : Angles) = false} J)
        (hK : RealState hc x {t : ℝ | s (t : Angles) = true} K)
        (hflip : ∀ᵐ t ∂angularMeasure, s (t + (Real.pi/3 : ℝ)) = !(s t)) : False

with `Angles := AddCircle (2 * Real.pi)` (`Coloring.lean:16`), so `s` lives on the **whole circle of
directions** and `t + π/3` is a genuine 60° rotation; and (`States.lean:92`)

    def RealState (x : ℂ) (A : Set ℝ) (J : Finset (Fin k)) : Prop :=
      MeasurableSet A ∧ ∀ i ∈ J, A ≤ᵐ[volume] liftPalette c hc x i

i.e. *on the angle set `A`, every label of `J` is in the palette almost everywhere*
(`liftPalette` at `PaletteDensity.lean:431`). The two internal flip lemmas are
`bool_flip_three` (`States.lean:223`) and `bool_flip_even` (`:228`).

So there are exactly **five premises to match**: measurability and weakness of `c`; a centre `x`; two
label sets `J,K` with **at most two labels outside their union**; a measurable `Bool` side function `s`
whose two level sets are RealState-represented by `J` and `K`; and the a.e. 60° flip.

## 2. Why `m6`'s naive global completion violates it [proof]

`m6`: `m = 6`, `q = (0,3,3,3,0,0)`, `J = {0,2}`, `K = {3,5}`, labels `0..5`, `E_i = {i, i+1 mod 6}`,
`v_i = e^{i q_i π/3}`. Match the premises one at a time:

1. `hc`, `hw` — a genuine trace field would be a measurable weak 6-colouring, so `k = 6` and both hold.
2. `x` — the centre of the 6-cycle.
3. **`hcard` is exactly tight**: `J ∪ K = {0,2,3,5}`, so `Finset.univ \ (J ∪ K) = {1,4}` and
   `(2 ≤ 2)` holds **with equality**. `m6` is therefore the *maximal* configuration the lemma can still
   kill — nothing is slack.
4. `s` := the side bit, i.e. which of the two RealStates the direction at `t` realises. Measurable in any
   genuine trace field.
5. `hJ`, `hK`: on the `J`-side the palette **is** `{0,2}` a.e., and on the `K`-side it **is** `{3,5}`
   a.e.; hence `{s = false} ≤ᵐ liftPalette x 0 ∩ liftPalette x 2` and
   `{s = true} ≤ᵐ liftPalette x 3 ∩ liftPalette x 5`. These are exactly the two `RealState` conclusions.
6. `hflip`: the palettes alternate `J, K, J, K, …` at the six angles `t + jπ/3`, so
   `s (t + π/3) = ¬ s t` **at every one of the six sampled angles**; the *naive completion* is the
   assertion that this holds a.e. on the whole circle.

Given the naive completion, all six premises hold and `two_state_impossible` returns `False`. ∎

**What this proves and what it does not.** It proves that **`m6` is a finite orbit model and not the
restriction of any whole-circle trace field** — the naive completion is inconsistent, and the
inconsistency is located precisely in premise 6: the alternation is known only at six angles, not a.e.
It does **not** show `m6` is invalid: as a finite witness of the licensed premises at six angles it is
correct, and it correctly demonstrates that those premises alone do not force acyclicity. The gap between
"holds at six angles" and "holds a.e. on the circle" is the whole gap.

**A structural reading worth recording.** `two_state_impossible` is the machine-checked statement that
the *two-state* channel is closed. `m6` is precisely the finite pattern that saturates it. So `m6` is best
read as a **boundary marker**: it shows the two-state route cannot be pushed further, not that F6 fails.

## 3. The reduction: which 6-cycles force a two-state representation [proof]

Two licensed premises do the work: `P_j` is **not contained in any `E_i`**, and **adjacent palettes are
disjoint**. At `m = 6` the interfaces are `E_i = {i, i+1 mod 6}`, so `⋃_i E_i = {0,…,5}` — *every* label
lies in some interface.

*Lemma.* No singleton palette is licensed at `m = 6`: if `P = {a}` then `a ∈ E_a`, so `P ⊆ E_a`.

*Theorem (the two-state case is closed).* Let a genuine 6-cycle common interface have palettes
`P_0,…,P_5`, each nonempty of size `≤ 2`, adjacent ones disjoint, none contained in an `E_i`, and suppose
the palettes take **exactly two distinct values** `J ≠ K`. Then the configuration is impossible.

*Proof.* By the Lemma no `P_j` is a singleton, so `|J| = |K| = 2`; adjacency gives `J ∩ K = ∅`; hence
`|J ∪ K| = 4` and `|univ \ (J ∪ K)| = 2`, so `hcard` holds. Alternation gives `s(t + π/3) = ¬s(t)` on
the sampled angles, and `RealState` holds on each side as in §2. Completing to the circle and applying
`two_state_impossible` yields `False`. ∎

**Consequence.** Every genuine 6-cycle must use **at least three distinct palettes** — because the
two-palette case is not merely unproved but *impossible*. So the question "does every genuine 6-cycle with
B2 force a two-state representation?" has the answer **yes**, and that is fatal to the two-state ones:
B2 plus the licensed premises can only be satisfied by a **multi-palette** 6-cycle. **F6 for `m = 6` is
therefore reduced to: no 6-cycle uses three or more palettes.**

## 4. The minimal surviving multi-state obstacle [proposed]

The two-state escape is closed, so the smallest survivor uses three palettes. Take

    P = ( {0,2}, {3,5}, {1,4}, {3,5}, {0,2}, {3,5} )

i.e. `A = {0,2}`, `B = {3,5}`, `C = {1,4}` in the cyclic order `A, B, C, B, A, B`. Checks against the
licensed combinatorial premises:

* every palette has size exactly 2 and is a **non-consecutive** pair, hence `P_j ⊄ E_i` for all `i` ✓;
* adjacent palettes: `A∩B = ∅`, `B∩C = ∅`, `C∩B = ∅`, `B∩A = ∅`, `A∩B = ∅`, `B∩A = ∅` ✓ all six;
* three distinct palettes, so the side object is not a `Bool` and `two_state_impossible` is **silent**;
  in particular `|univ \ (A ∪ B)| = 2` and `|univ \ (B ∪ C)| = 2` both *would* satisfy `hcard` — the
  escape is not the count, it is the **multiplicity of states**.

**Outstanding (needs the graph worker's licensed checker, no compute here):** the sign-bit conditions —
that some `q ∈ {0,…,5}^6` gives actual scalar-product signs at the six angles `t + jπ/3` with opposite
sign bits, `P_j ∩ (C \ ⋃(E_i on that side)) ≠ ∅` on both sides, and `P_j` nonempty of size `≤ 2` — are
**not verified** for this palette sequence. It is offered as the shape of the minimal survivor, not as a
certified witness.

## 5. The missing analytic realisation, named

The tree contains `two_state_impossible` and, by grep over `lean/OAI/`, **no three-state, multi-state or
`r`-state analogue** (the only hits for `*_state_impossible` are the two occurrences of the two-state
lemma, at `Interfaces.lean:139` and `States.lean:378`). That absence is exactly the gap:

> **Missing lemma (MS).** Let `r ≥ 3`, `A_0,…,A_{r-1}` a measurable partition of `Angles` (mod null
> sets), `J_0,…,J_{r-1}` finsets with `RealState hc x A_l J_l`, and suppose the palettes are subject to a
> rotation law relating `l` at `t` to `l'` at `t + π/3`. Then `False`.

`two_state_impossible` is the case `r = 2` with the specific rotation law `s ↦ ¬s`. **Nothing in the tree
forbids `r ≥ 3`**, so the multi-palette 6-cycle of §4 is not excluded by any existing theorem. Whether
such an `(MS)` is *true* is a separate question and I make no claim; what is established is that the
`m = 6` reduction of §3 lands exactly on it.

**Why `m = 5` escapes the same argument (a useful contrast).** At `m = 5`, `E_i = {i, i+1 mod 5}` so
`⋃_i E_i = {0,…,4}` and label `5` lies in **no** interface; the singleton palette `{5}` of Astra's `m5`
witness is therefore licensed, `|J ∪ K| = 3`, and `|univ \ (J ∪ K)| = 3 > 2`. So `m5` escapes
`two_state_impossible` through the **count**, whereas `m6` (§4) escapes through the **number of states**.
The two escapes are different, and the `m = 6` one is the one with no machine-checked obstruction.

## 6. What is claimed

* **[proof]** `m6`'s naive whole-circle completion satisfies all six premises of `two_state_impossible`,
  with `hcard` tight, and is therefore impossible. `m6` is a finite orbit model only.
* **[proof]** Every genuine 6-cycle whose palettes take exactly two values is impossible (no singleton is
  licensed at `m = 6`, so both are 2-sets, disjoint, union 4, complement 2).
* **[proposed]** The minimal surviving obstacle is a 3-palette 6-cycle, shape given in §4, sign-bit
  compatibility unchecked.
* **[proposed]** The missing analytic realisation is a multi-state analogue `(MS)` of
  `two_state_impossible` for `r ≥ 3`; none exists in the tree.
* **Not claimed:** any numerical bound; any statement about cycle lengths other than 6; any resolution of
  L6; any claim that F6 holds or fails. `T6 -> B2` supplies neither L6 nor F6.

## 7. Handoff for the graph worker (file-based, no compute here)

Three items, in priority order, each a single licensed-checker run:
1. **Sign-bit test of §4's `P = ({0,2},{3,5},{1,4},{3,5},{0,2},{3,5})`**: does some `q ∈ {0,…,5}^6`
   realise the six scalar-product signs with opposite sign bits and both sides nonempty outside the
   side's interfaces? If yes, `m6`'s two-state boundary has a genuine multi-palette neighbour and F6 for
   `m = 6` needs `(MS)`; if no, the 3-palette family may itself be closed combinatorially.
2. **Exhaustive palette triples at `m = 6`**: over all non-consecutive 2-sets (there are 9) and all
   cyclic sequences of length 6 with adjacent disjointness, which use ≥ 3 distinct palettes? This is a
   small finite enumeration and would settle whether §4's shape is the only survivor family.
3. **`m = 5` count check**: confirm that Astra's `m5` singleton `{5}` is licensed only because label 5
   is outside every `E_i`, i.e. that the `m = 5` escape is purely the count and not a second state
   phenomenon.
