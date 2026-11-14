# Clause (D) of bridge (B): what is provable, and the exact gap
> # RETRACTION (block 19): §6 of this file is WITHDRAWN
>
> The construction `A ⊆ F` countable and dense in `F` is **invalid for the actual support notion**.
> The source defines `fiveSupport x i := (volume.restrict (fiveRealState x i)).support`
> (`FiveSupport.lean:83`). For a countable (or any null) set `A`, `volume.restrict A = 0`, and the
> support of the zero measure is `∅` — **not** `closure A`. So `supp A = ∅` for my `A`, and the
> "obstruction" collapses: it never had a point of support intersection at all.
>
> Consequences, all accepted:
> * §6 is retracted in full and **not** replaced by another model (no unreviewed models in this file).
> * §7's sentence "every proper weakening fails / no proper weakening will do" is **retracted**: that
>   was not proved, only asserted. What stands is the positive identification of the premise the
>   finite argument consumes (step 1 needs full disjointness); no minimality *claim*.
> * The historical countermodels in earlier blocks that used `closure(A)` as `supp A` shared this
>   error; they are marked abstract-only already, and now unusable for support-level conclusions.
>
> §2 Steps 1-5 (the level-set facts, cited to source) are unaffected. See §8 for the valid
> replacement, which is Astra's candidate, audited below.

> # CORRECTIONS (block 18) — two errors in this file, and a replacement obstruction
>
> **(E1) The §2 Step-6 witness is INVALID.** `A = ⋃_{k∈ℤ}⋃_{n≥1}(60k + (0,ε_n))` is **60-periodic**, so
> `A − 60 = A` and `A ∩ (A−60) = A ≠ ∅`: the very premise it was meant to satisfy fails. My claim
> "`A ∩ (A−60) = ∅`" was simply false.
>
> **(E2) Wrong kind of objection.** Even had it held, a *single* point `a` with `a, a+60 ∈ supp A` does
> not refute an **a.e.** disjointness conclusion. To refute (D) one needs a set of `a` of **positive
> measure**. The old witness was therefore not a counterexample to the statement under discussion.
>
> Both are fixed in **§6** below, which gives a valid abstract obstruction with the correct measure
> quantifier, and in **§7**, which pins the exact weakest support-level premise. §2's Steps 1–5 are
> unaffected and stand. **§2 Step 6 and its witness are withdrawn.**


Source/analysis only. No build, no cloud compute, no agent launched. Clock: 2026-11-14 15:2x UTC
(`date -u` read at the start of the block).

## 0. Two corrections first

**C1 (applicability of the block-16 countermodels).** The two models in `FIVE-CYCLE-INTERFACE.md` §9 are
models of the **abstract data** `(S : ℝ → Finset (Fin 5), θ : ℝ → Fin 5)` only. They are **not**
instances of the actual objects: `Angles = AddCircle (2*Real.pi)` (`Coloring.lean:16`) so a state
function must be 2π-periodic, which my `θ t = (g t + ⌊t/60⌋) mod 5` is not (it gains +6 ≡ +1 per full
turn), and the second model's closed-interval supports overlap at the endpoints, so its "single state at
0" premise fails. **Applicability retracted**; what survives is only the quantifier observation that
"(O″) is a ∀∃ over support sets" and "(SB) is a ∀¬ over θ-values", which is what incomparability needed.

**C2 (my block-16 §10.3 claim about (D) was wrong).** I wrote that "(D) is not
`palette_neighbor_disjoint` … nothing else in the tree supplies (D)". The first half stands, the second
is false: `PaletteTransport.lean:450` has

```lean
lemma palette_sixty_disjoint (hw : WeakColoring k c) (x : ℂ) :
    ∀ᵐ f ∂angularMeasure, Disjoint (palette c hc x f) (palette c hc x (f+(sixty : Angles)))
```
with `sixty : ℝ := Real.pi/3` (`PaletteTransport.lean:390`) and `angularMeasure =
AddCircle.haarAddCircle` (`Coloring.lean:17`). That is exactly the **one centre, two angles 60° apart**
statement I said was missing — at the *palette* level. And `Accumulation.lean:392` `fiveState_adj`
already upgrades it to the **level-set** level. So (D)'s palette and level-set forms are in the tree;
what is missing is one specific upgrade. This file pins it.

## 1. The objects, cited

| name | definition | source |
|---|---|---|
| `Angles` | `AddCircle (2*Real.pi)` | `Coloring.lean:16` |
| `angularMeasure` | `AddCircle.haarAddCircle` (Haar probability) | `Coloring.lean:17` |
| `sixty` | `Real.pi/3` | `PaletteTransport.lean:390` |
| `fiveDiag i` | `{i, i+2}` | `Exclusion.lean:8` |
| `fiveAdj i j` | `i+1 = j ∨ j+1 = i` | `Exclusion.lean:9` |
| `FiveCenter x` | `∀ i : Fin 5, TransitionEdge c i (i+1) x` | `Accumulation.lean:358` |
| `fiveState x t` | `fiveCanonical (palette c hc x t)` | `Accumulation.lean:364` |
| `fiveRealState x i` | `{t : ℝ | fiveState x (t : Angles) = i}` | `FiveSupport.lean:82` |
| `fiveSupport x i` | `(volume.restrict (fiveRealState x i)).support` | `FiveSupport.lean:83` |
| `TransitionEdge i j x` | `i ≠ j ∧ ∀ R > 0, 0 < limsup (transitionRatio x R) (𝓝[≠] 0)` | `Transitions.lean:23` |
| `transitionSet i j x R h` | `{q | q ∈ ball x R ∧ ((c q = i ∧ c(q+h) = j) ∨ (c q = j ∧ c(q+h) = i))}` | `Transitions.lean:9` |
| `transitionRatio i j x R h` | `volume (transitionSet …) / ofReal ‖h‖` | `Transitions.lean:21` |

**(D), the clause to decide.** For a five-cycle centre `x` and a weak 5-colouring `c`, for a.e.
`a : ℝ`: `Disjoint {i | a ∈ fiveSupport x i} {i | a + 60 ∈ fiveSupport x i}`.

Equivalently, with `A_i := fiveRealState x i` (a Borel subset of `ℝ`): no `i` has both `a` and `a+60`
in the closed support of `vol.restrict A_i`.

## 2. Line-by-line: everything the tree gives, with premises supplied

**Step 1** [premise: `hw : WeakColoring 5 c`, `hx : FiveCenter c x`]
`fiveState_diag` (`Accumulation.lean:379`): `∀ᵐ t ∂angularMeasure, palette c hc x t = fiveDiag (fiveState x t)`.

**Step 2** [premise: `palette_sixty_disjoint hw x`, `PaletteTransport.lean:450`]
`∀ᵐ t ∂angularMeasure, Disjoint (palette x t) (palette x (t+sixty))`.

**Step 3** [1 + 2 + `five_diag_disjoint` (`Exclusion.lean:20`, `by decide`)]
`∀ᵐ t ∂angularMeasure, fiveAdj (fiveState x t) (fiveState x (t+sixty))`. This is exactly
`fiveState_adj` (`Accumulation.lean:392`); its proof is the three lines quoted above, so no new premise.

**Step 4** [3 + `fiveAdj` def, `Exclusion.lean:9`]
`fiveAdj i i` is `i+1 = i ∨ i+1 = i`, false in `Fin 5`. Hence **`∀ᵐ t ∂angularMeasure, fiveState x t ≠
fiveState x (t+sixty)`** — the states at 60° separation are a.e. *distinct*.

**Step 5** [4, transported to `ℝ` by `angleMk_quasiMeasurePreserving`]
For each `i`: `vol ({t : ℝ | fiveState x (t:Angles) = i} ∩ (({t | fiveState x (t:Angles) = i}) - sixty)) = 0`.
In the notation above: `vol (A_i ∩ (A_i - 60)) = 0` for every `i`.

**Step 6 — THE GAP.** One wants: `supp(A_i) ∩ (supp(A_i) - 60) = ∅`.
Step 5 gives only that `A_i` and its 60-shift meet in a **null** set. That does **not** imply their
*closed supports* are disjoint, and the inference is not a technicality:

> **Witness that Step 5 ⇏ Step 6** (measure-theoretic, on `ℝ` with Lebesgue measure — an abstract model
> of the inference, **not** a colouring, and claiming nothing about (D)): let
> `A := ⋃_{k∈ℤ} ⋃_{n≥1} (60k + (0, ε_n))` with `Σ ε_n < 60`. Then `A ∩ (A - 60) = ∅`, so Step 5's
> conclusion holds with room to spare, while `0 ∈ supp A` and `60 ∈ supp A` (both are accumulation
> points of the union), so `supp A ∩ (supp A - 60) ∋ 0 ≠ ∅`. The mechanism is exactly thin
> accumulation: `A_i` may creep towards `a` and towards `a+60` through sets of vanishing measure. ∎

Nothing in the tree forbids this creep: `fiveSupport` is defined through `Measure.support`
(`FiveSupport.lean:83`), a purely *topological* closure condition on the restricted measure. It carries
no lower density bound at any scale, and no lemma in the 82-module tree states one.

**Why the promising tools do not close the gap.** `hx` speaks about *position* space:
`TransitionEdge c i (i+1) x` is `0 < limsup_h volume(transitionSet … x R h)/‖h‖` (`Transitions.lean:21-23`),
a positive-density statement for pairs `(q, q+h)` inside a **ball around `x`**, i.e. about the colouring
in a neighbourhood of `x`. `A_i` lives in *angle* space: the directions from `x` along which state `i`
is the palette representative. `transition_abundance` (`Transitions.lean:25`) extracts a scale `a > 0`
and a filter `h → 0` with `a‖h‖ < volume.real (transitionSet …)`; `transitionEdge_closed`
(`Accumulation.lean:197`) is about *closedness in `x`*; `missing_edge_lim` (`Accumulation.lean:214`)
converts a *missing* edge into a limit. None of the three converts angular thin accumulation into a
density statement, and none mentions `fiveSupport` at all.

## 3. The smallest missing lemma

> **(M) — level-set/support upgrade at the 60° step.**
> ```lean
> lemma five_support_sixty_disjoint (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) :
>     ∀ᵐ a : ℝ ∂volume, Disjoint {i : Fin 5 | a ∈ fiveSupport c hc x i}
>       {i : Fin 5 | a + (sixty : ℝ) ∈ fiveSupport c hc x i}
> ```

This *is* (D). It is not a restatement of anything in the tree: its premises would be Steps 1–5, and
its conclusion is Step 6, which Step 5 does not give. The tree's nearest neighbours are:

* `fiveState_adj` — the level-set form (Step 3), strictly weaker by the witness above;
* `palette_sixty_disjoint` — the palette form, weaker still;
* `five_support_step_ban` — a *transition* ban for adjacent pairs present in `S a`; it consumes `S a`
  memberships rather than producing them, so it cannot supply (D);
* `transition_abundance` / `transitionEdge_closed` / `missing_edge_lim` — position-space density and
  closedness, no angular density content.

**Is (M) plausible?** Yes: the closed walk constraint agrees with it. Since `fiveState x (t+sixty)` is
adjacent to `fiveState x t` a.e. (Step 3) and the angle is periodic with `6·60° = 360°`, the six states
at `t, t+60, …, t+300` form a closed walk of 6 steps with increments `±1` on the 5-cycle; the increments
must sum to `0 ∈ ℤ/5` with six even terms, forcing three `+1` and three `−1` and forbidding a repeat at
step 1 (which is exactly `≠` at 60°, Step 4). Revisits are forced at distance ≥ 2 steps (120°). So (M)
is consistent with the combinatorics; what it adds is that the *supports* — not just the level sets —
inherit that separation.

## 4. Verdict

* **(D) is not proved here, and not refuted.** Steps 1–5 are a complete, premise-cited derivation of the
  level-set form; Step 6 is exactly the missing inference, and it is missing for a structural reason
  (closure of a restricted measure says nothing about density), witnessed by an explicit
  measure-theoretic model.
* **(M) is the smallest precise missing lemma**, it respects every base assumption (`hw`, `hx` only, no
  second `FiveCenter`, no bridge hypothesis), and it is stated in the tree's own vocabulary.
* **Bridge (B) is therefore still blocked at (D)**, as well as at (V) (the missing centre construction
  of §10.3). (B) must not be assumed anywhere.

## 5. Grades

| item | grade |
|---|---|
| C1: the §9 models are abstract-only; applicability retracted | [verified here] |
| C2: `palette_sixty_disjoint` exists and gives the one-centre two-angle form | [read] `PaletteTransport.lean:450` |
| Steps 1–5 with premises | [read + argued] each premise cited to a line; the deduction Step 4 uses only `fiveAdj`'s definition |
| Step 5 ⇏ Step 6, with witness | [proved here] on `ℝ` — an abstract model of the inference only |
| (M) is not in the tree; (D) unproved | [argued here] from the inspected declarations |
| plausibility of (M) via the closed 6-step walk | [argued here], arithmetic `3·(+1) + 3·(−1) = 0` |


---

# §6 A VALID abstract obstruction (replaces the §2 Step-6 witness)

The inference under scrutiny is

> **(L) ⇒ (S-a.e.)**  where
> **(L)** `vol (A ∩ (A − 60)) = 0`   (the level-set premise, the shadow the tree actually supplies), and
> **(S-a.e.)** `vol {a : a ∈ supp A ∧ a + 60 ∈ supp A} = 0`   (the support-level a.e. premise (D)).

**Construction.** Let `E ⊆ [0,1]` be closed with `vol E > 0` (a fat Cantor set). Put
`F := E ∪ (E + 60)`, and let `A ⊆ F` be **countable and dense in `F`** — e.g. a countable dense subset
of `E` together with its translate by 60.

* `vol A = 0`, hence `vol (A ∩ (A − 60)) = 0`: **(L) holds.**
* `A` is dense in the closed set `F`, so `supp A = closure A = F`. Therefore
  `{a : a ∈ supp A ∧ a + 60 ∈ supp A} = {a : a ∈ F ∧ a + 60 ∈ F} ⊇ E`, since `E ⊆ F` and `E + 60 ⊆ F`.
  `vol E > 0`, so **(S-a.e.) fails.** ∎

**Scope, stated exactly.** This is an obstruction *at the level of the implication between the two
measure statements*: it shows (L) does not imply (S-a.e.) for measurable `A ⊆ ℝ`, **with the a.e.
quantifier respected** (the failure set has positive measure). It is **not** a weak-colouring
counterexample and says nothing about whether (D) holds for palettes of actual 5-colourings. It refutes
only the *inference*, which is what §2 Step 6 asserted.

# §7 The exact weakest support-level premise, and why nothing weaker will do

> **(D-a.e.)** `∀ᵐ a : ℝ ∂volume, ∀ i : Fin 5, a ∈ fiveSupport c hc x i → a + (sixty : ℝ) ∉ fiveSupport c hc x i`
> — equivalently, for a.e. `a`: `Disjoint (S a) (S (a + 60))` with `S a := {i | a ∈ fiveSupport c hc x i}`.

**Why it is not weaker than this.** The finite asset's first step is
`S(1) ⊆ I ∖ S(0)` (FIVE-CYCLE-CORE step 1, driven by (D) and (R)), i.e. it consumes **full**
disjointness of consecutive lists. Two weakenings suggest themselves and both fail:

* *Excluding only the distinguished state.* The tempting weakening is "no `i ∈ S a ∩ S(a+60)` with
  `i ≠ fiveState x (a)`", since `fiveState_adj` already separates the *distinguished* states at 60°
  (`state a ≠ state(a+60)`). This does **not** give (D): it leaves open the case
  `fiveState x (a) ∈ S (a + 60)`, which `fiveState_adj` does not exclude — that lemma separates the
  two *states*, not support memberships. Since `S(a) ∋ fiveState x (a)` a.e. (`five_ae_mem_support`),
  the distinguished state is a *bona fide* member of `S a`, so the inclusion `S(1) ⊆ I ∖ S(0)` would
  fail for it.
* *Restricting to one angle.* (D) is consumed at all six consecutive pairs, so a single-`a` statement
  cannot serve; and by (E2) only an a.e. statement can be both true and useful.

So the weakest premise that fires the shortcut is **(D-a.e.) itself**, not a variant of it.

**What the tree gives instead, exactly.** `fiveState_adj` (`Accumulation.lean:392`) yields, for a.e.
`t`, `fiveAdj (state t) (state (t + sixty))`; with `fiveAdj i j := i+1 = j ∨ j+1 = i`
(`Exclusion.lean:9`) this gives `state t ≠ state (t + sixty)`. That is: **the distinguished state at `a`
is not the distinguished state at `a + 60`** — a statement about two specific *values* of `θ`. (D-a.e.)
is a statement about the two *support sets*, which contain those values and possibly more. The gap
between them is exactly §6's (L) ⇏ (S-a.e.).

**Attempt at a derivation from local lemmas — where it stops.** Suppose `i ∈ S a ∩ S(a+60)`. Then:
`five_support_trace` (`FiveSupport.lean:86`) gives a trace vector `b₁` at `x + direction a` vanishing on
`fiveDiag i`, and `b₂` at `x + direction(a+60)` vanishing on the same `fiveDiag i`. Two trace vectors at
two points at distance exactly 1, each avoiding the same two labels. Nothing in the tree forbids that
pair: `transition_abundance`/`transitionEdge_closed`/`missing_edge_lim` concern transitions between
*different* colours in a ball around `x`; two points that both *avoid* `D_i` are exactly what unit
distance permits (they take the other three colours). So no contradiction is reached, and the
obstruction is mathematical, not a missing case split.

**Verdict.** (D-a.e.) is the exact weakest premise; it is not derivable from the tree's local lemmas;
and §6 shows it is not implied by the level-set shadow those lemmas do provide. Bridge (B) remains
blocked at (D) and (V), and (D) is now stated as the single precise target.


---

# §8 Astra's candidate, independently audited (VALID)

## 8.1 The statement, in the tree's own generality

Let `I` be a **finite** label type, `f : ℝ → I` measurable, `μ` a σ-finite translation-invariant
Borel measure (Lebesgue here), `d ≠ 0`, `T t := t + d`, and for `i : I`

```
S_i := (μ.restrict {t | f t = i}).support          -- exactly fiveSupport's shape
Q_ij := {t | f t = i ∧ f (t + d) = j}              -- the joint pair set
```

> **(PA) premise.** For all `i j`, `S_i ∩ S_j ≠ ∅  ⇒  μ(Q_ij) = 0`.
> **(PA claim).** Then `S_i ∩ T⁻¹(S_i) = ∅` for every `i`.

`S_i ∩ T⁻¹(S_i)` is the set of `a` with `a ∈ S_i` and `a + d ∈ S_i`; so the claim is precisely
`a ∈ S_i → a + d ∉ S_i`, i.e. the **pointwise** form of clause (D), which is exactly the shape of
`five_support_no_sixty` (`FiveSupport.lean:138`).

## 8.2 Every step, checked, with the requirement that makes it true

1. **Cover.** `{f = i} = ⋃_{j∈I} Q_ij` — exact set equality, because `f(t+d)` is a single label.
   *Requires `I` finite only for the next step.*
2. **Additivity.** `μ.restrict {f = i} = Σ_{j∈I} μ.restrict Q_ij` — the `Q_ij` are pairwise disjoint
   and their union is the set. *Requires `Q_ij` measurable:* `Q_ij = A_i ∩ (A_j − d)` with
   `A_i = {f = i}` measurable since `f` is; translation preserves measurability. ✓
3. **Support of a finite sum.** `supp (Σ_{j} ν_j) = ⋃_{j} supp ν_j`.
   `⊇` is monotonicity. `⊆`: if `x ∉ supp ν_j` for every `j`, choose open `U_j ∋ x` with
   `ν_j(U_j) = 0`; then `U := ⋂_j U_j` is open, contains `x`, and `Σ_j ν_j(U) ≤ Σ_j ν_j(U_j) = 0`.
   *This is where finiteness of `I` is essential and cannot be dropped:* for a countable sum
   `supp(Σ_n ν_n) ⊋ ⋃_n supp ν_n` in general (take `ν_n = 2^{-n} δ_{x_n}` with `x_n → x`).
   The tree's `I = Fin 5` ✓.
4. **Support membership propagates.** If `a ∈ supp(μ.restrict Q_ij)` then `a + d ∈ S_j`.
   For open `U ∋ a+d`: `U − d` is open and contains `a`, so `μ(Q_ij ∩ (U − d)) > 0`; and
   `Q_ij ⊆ {f(·+d) = j} = A_j − d`, hence `Q_ij ∩ (U−d) ⊆ (A_j ∩ U) − d`, so
   `μ(A_j ∩ U) = μ((A_j ∩ U) − d) ≥ μ(Q_ij ∩ (U−d)) > 0`. *Requires translation invariance and that
   `U ↦ U − d` stays open; no measurability of `Q_ij` beyond step 2.* ✓
5. **The contradiction.** Let `a ∈ S_i ∩ (S_i − d)`. By steps 1–3, `S_i = ⋃_j supp(μ.restrict Q_ij)`,
   so pick `j` with `a ∈ supp(μ.restrict Q_ij)`. By step 4, `a + d ∈ S_j`; and `a + d ∈ S_i` by
   hypothesis, so `S_i ∩ S_j ∋ a+d ≠ ∅`. Premise (PA) gives `μ(Q_ij) = 0`, hence
   `supp(μ.restrict Q_ij) = ∅`, contradicting `a ∈ supp(…)`. ∎

**Verdict: the argument is correct as stated.** No step assumes a second `FiveCenter`, no bridge
hypothesis, no minimality claim. The only structural requirements are (i) `I` finite, (ii) `μ`
translation-invariant σ-finite, (iii) `f` measurable, (iv) `d ≠ 0` for the conclusion to be
non-vacuous.

## 8.3 Does (PA) hold in the tree? Yes — split by adjacency

Take `I = Fin 5`, `μ` the circular measure on `Angles` (or Lebesgue on ℝ), `f = fiveState x`, `d = 60°`.

* **Non-adjacent `(i,j)` (`¬ fiveAdj i j`, including `i = j`):** `fiveState_adj`
  (`Accumulation.lean:392`) gives, for a.e. `t`, `fiveAdj (fiveState x t) (fiveState x (t+sixty))`.
  Hence `Q_ij` is null, i.e. `μ(Q_ij) = 0` ✓ — with **no** contact hypothesis needed.
* **Adjacent `(i,j)` with `S_i ∩ S_j ≠ ∅`:** choose a contact point `a₀ ∈ S_i ∩ S_j`; then
  `five_support_step_ban` (`FiveSupport.lean:89`) — verbatim manuscript **Lemma 6.7**, see
  `MANUSCRIPT-LEMMA67.txt` — gives a.e. absence of both transitions, i.e. `μ(Q_ij) = 0` and
  `μ(Q_ji) = 0` ✓. When `S_i ∩ S_j = ∅` the premise is vacuous.
* **Adjacent `(i,j)` with `S_i ∩ S_j = ∅`:** nothing to prove; `Q_ij` may be anything.

So (PA) holds **exactly**: the contact hypothesis in (PA) is precisely the hypothesis Lemma 6.7 needs,
and the non-contact case is where Lemma 6.7 has nothing to say. This is why the candidate fits.

**One technical step to flag.** `fiveState_adj` and `five_support_step_ban` are stated a.e. w.r.t.
`angularMeasure` on `Angles = AddCircle (2π)`, while `fiveSupport` uses `volume` on `ℝ` through
`fiveRealState`. The candidate's (PA) is needed in the `volume`-on-`ℝ` measure. The transport is
routine and the tree already does exactly this: `five_support_prev` (`FiveSupport.lean:128–137`)
passes from `angleMk_quasiMeasurePreserving.ae` to a.e. on `ℝ` via
`measurePreserving_add_right volume (-sixty)`. So the transport is an *identified, precedented* step,
not a gap — but it must be done, and it is the one place where a formalisation could still snag.

## 8.4 What this changes, and what it does not

* It **proves clause (D)** (the pointwise form `a ∈ S_i → a + d ∉ S_i`, which is `five_support_no_sixty`),
  given the two cited lemmas and the transport. It does **not** touch clause (V).
* It would remove `strict_state_no_unit_support` (`States.lean:704`) from the `five_support_no_sixty`
  path, replacing the strict-state sequence machinery by a finite-union support identity.
* **Lemma 6.7 is retained, not deleted.** The manuscript's Lemma 6.7 *is* `five_support_step_ban`, and
  the candidate *uses* it. Calling this a "6.7 deletion" would be wrong, as the supervisor notes.
* Grade: **proposed, independently audited here at proof level, NOT machine-checked.** The
  measure theory (steps 1–5) is standard and each identity is checked above; the Lean-side
  application depends on (i) the Haar→volume transport and (ii) `five_support_step_ban`'s exact
  hypotheses, both cited.

## 8.5 Grades for this section

| item | grade |
|---|---|
| §6 retraction (`volume.restrict A = 0 ⇒ support = ∅`) | [verified here] from `FiveSupport.lean:83` and the definition of `Measure.support` |
| §7 minimality sentence retracted | [verified here] it was asserted, not proved |
| Astra's steps 1–5 | [audited here, proof level] every measure and support identity checked; finiteness of `I` identified as essential |
| (PA) from `fiveState_adj` + `five_support_step_ban` | [read] exact hypotheses matched, including the contact condition |
| the Haar→volume transport | [read] template exists at `FiveSupport.lean:128–137`; not done here |
| machine verification | **none** — no build, per policy |
