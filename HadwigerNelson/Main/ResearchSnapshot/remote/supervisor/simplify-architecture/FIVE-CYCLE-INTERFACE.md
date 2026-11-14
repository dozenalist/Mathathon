# The interface still blocking replacement of the Lemma 6.7 branch by the finite residue asset

Analysis only. No build, no edit outside this directory. Shared files read-only.
The finite asset is `supervisor/simplify-verification/lean/FiveCycleResidues.lean` (another worker's
file, read-only here); the analytic side is `lean/OAI/Geometry/PlaneColoring/`.

## 1. What the finite asset actually concludes (fixed, 21 local lemmas)

| declaration | content |
|---|---|
| `g_induces_h`, `label_transport`, `one_minus_k_induces_four_minus_i` | a state relabelling `h i = 1 - i` is legitimate only with the **vertex** map `g k = 3 - k` (`g '' D i = D (h i)`), not with `k ↦ 1-k` |
| `five_residues_reduce_to_two` | `P j ∩ {2,4} = ∅ ↔ j = 1 ∨ j = 4` — five residues reduce to two |
| `residue_zero_collides`, `residue_two_collides`, `residue_three_collides` | `j ∈ {0,2,3}` ⇒ `P j` meets the anchor pair `{2,4}` |
| `h_fixes_anchor`, `h_fixes_pair24`, `h_swaps_allowed_pairs` | the relabelling fixes `{0,1}` and `{2,4}` and exchanges `P 1` with `P 4` |
| `notCommon_image`, `disjoint_image`, `hasNbr_image`, `valid_family_push`, `disjoint_family_push`, `neighbour_family_push` | the three hypothesis families (V), (D), (N) are **invariant** under that two-level relabelling |

So the asset is a complete finite normal-form reduction: *given* a family `S : ZMod 6 → Finset (ZMod 5)`
satisfying (V) not-common, (D) disjoint-from-successor, (N) neighbour and (R) `S 0 = {0,1}`, the only
open combinatorial cases are `j ∈ {1,4}` and they are the same case under a legitimate symmetry. It
proves **nothing** about supports, palettes, colourings or the plane.

## 2. The current branch, exactly

The Lean form of the paper's Lemma 6.7 is

**`five_support_step_ban`** — `lean/OAI/Geometry/PlaneColoring/FiveSupport.lean:89`

```lean
lemma five_support_step_ban (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i j : Fin 5}
    (hi : a ∈ fiveSupport c hc x i) (hj : a ∈ fiveSupport c hc x j) (hij : fiveAdj i j) :
    ∀ᵐ t ∂angularMeasure, ¬(fiveState c hc x t = i ∧ fiveState c hc x (t + (sixty : Angles)) = j) ∧
      ¬(fiveState c hc x t = j ∧ fiveState c hc x (t + (sixty : Angles)) = i)
```

Inputs: a weak 5-colouring `hw`; a five-cycle centre `hx`; two supports both containing the base angle
`a` (`hi`, `hj`); and state-adjacency `hij : fiveAdj i j` (i.e. `i+1 = j ∨ j+1 = i`).
Output: at a.e. angle, the state cannot step from `i` to `j` **or** from `j` to `i` across `sixty` (60°).

Its analytic support is `five_support_trace` (`FiveSupport.lean:86`), which turns membership
`a ∈ fiveSupport i` into a trace vector `b` with `IsTrace c hc (x + direction a) b` vanishing on
`fiveDiag i`, feeding `avoiding_trace_palette` and `five_adj_four`.

The finite core that already exists beside it, both `by decide`, purely combinatorial:

```lean
lemma five_no_common_adj : ∀ I : Finset (Fin 5), I.Nonempty → (∀ k, ∃ i ∈ I, k ∉ fiveDiag i) →
    ∃ i ∈ I, ∃ j ∈ I, fiveAdj i j                                    -- Exclusion.lean:24
lemma five_forced_label : ∀ i j X : Fin 5, fiveAdj i j →
    (∀ k, k ∉ fiveDiag i ∪ fiveDiag j ↔ k = X) → ∀ p, Disjoint p (fiveDiag i) →
    ¬ p ⊆ fiveDiag j → X ∈ p                                          -- Exclusion.lean:26
```

Note what `five_no_common_adj` *takes as a hypothesis*: exactly (V) — "no label is available in every
state of `I`". That is the interface the finite machine needs and cannot supply.

## 3. The interface, stated once

Write `S_r(a) := {i : Fin 5 | a + r * (sixty : ℝ) ∈ fiveSupport c hc x i}` for `r : ℕ` (the paper's
`S(R^r a)`, six positions because `6 · 60° = 360°`), and
`NotCommon L : Prop := ∀ k : Fin 5, ∃ i ∈ L, k ∉ fiveDiag i`.

> **(I) Positional validity at all six positions.**
> ```lean
> lemma five_position_valid (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) (r : ℕ) :
>     ∀ᵐ a ∂volume, ∀ k : Fin 5, ∃ i : Fin 5,
>       a + r * (sixty : ℝ) ∈ fiveSupport c hc x i ∧ k ∉ fiveDiag i
> ```
> i.e. `NotCommon (S_r a)` for a.e. `a`, for every one of the six positions.

**This is the whole interface.** Everything else the finite asset needs is already either finite
(§1, proved) or analytic and present: (R) is a normalisation of the labelling; (D) and (N) transport
through the existing support machinery; `five_endpoint_no_common` already produces `NotCommon` — but
**only at one position and only under an extra centre hypothesis**:

```lean
lemma five_endpoint_no_common (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a b : ℝ}
    (hab : Real.sin (b - a) ≠ 0) (hy : FiveCenter c (x + direction (a : Angles) + direction (b : Angles))) :
    ∀ k : Fin 5, ∃ i, a ∈ fiveSupport c hc x i ∧ k ∉ fiveDiag i        -- CyclicCore.lean:25
```

## 4. Why (I) does not follow today — the precise obstruction

`five_endpoint_no_common` gives `NotCommon` at the angle `a` *provided* there is a second angle `b`
with `sin (b−a) ≠ 0` **and** `x + direction a + direction b` is again a five-cycle centre (`hy`). Its
proof is: `five_local_palette` builds an open set of angles carrying label `k`; `palette_open_exclusion`
turns that into a null open set using `hab`; `transitionEdge_no_open_exclusion` finishes with `hy`.

Two independent reasons the six positions cannot all be obtained this way from what the tree has:

1. **`hy` is a centre-existence hypothesis, not a transport.** To reuse the lemma at position `r` one
   must show `FiveCenter c (x + direction (a + r·60°) + direction b)` for some `b` with
   `sin (b − (a + r·60°)) ≠ 0`. The tree contains no lemma producing new five-cycle centres from old
   ones by adding two unit directions; `FiveCenter` is defined (`Accumulation.lean:358`) as
   `∀ i, TransitionEdge c i (i+1) x` and is only ever *assumed*.
2. **The step ban is not a validity transport.** `five_support_step_ban` is stated at the 60° step and
   yields a forbidden *transition*, not `NotCommon` of a support list at a distant angle. It gives (D)
   in the form the paper uses it, but nothing in the tree converts (D)-plus-(N) back into (V) at a
   position other than the endpoint one — that conversion is exactly what the paper performs with the
   endpoint-pair mechanism at positions 0 and 3.

**Measured against the corrected audit of the finite argument:** with (V) available only at two
positions, the finite system has exactly **8** solutions, and every one of them satisfies
`S(1) = S(5) = {2,4}` — and `{2,4}` is *not* `NotCommon` because `fiveDiag 2 ∩ fiveDiag 4 = {4}`. So a
single additional validity fact at position 1 (or 5) collapses all eight. That is why (I) is the right
and *minimal* interface: it is not "six new inputs", it is one input type, and one of its six instances
suffices to make the finite classification bite.

## 5. Dependency and cost comparison, if (I) is proved

| | current branch | with (I) proved |
|---|---|---|
| analytic input | `five_support_step_ban` (FiveSupport:89) + `five_support_trace` (:86) + `avoiding_trace_palette`, `five_adj_four`, and the `sixty`-step machinery | `(I)` alone |
| combinatorial input | `five_no_common_adj`, `five_forced_label` (Exclusion:24,26), 5-residue case split | the 21-lemma finite asset: normal form + two cases exchanged by a legitimate two-level relabelling |
| hypotheses changed | — | none: (I) is a statement about `fiveSupport`/`fiveDiag` already in scope; it introduces no new hypothesis on `c`, `x` or `a` beyond `hw`, `hx`, `a.e. a` |
| line cost of the new input | — | one lemma; if derivable from `five_endpoint_no_common` it is 15–40 lines, otherwise it is the whole endpoint mechanism re-done |
| line cost of the deletion | ≥ the body of `five_support_step_ban` from line 89 to its end (not measured this block) | plus its two uses |
| net | unknown | plausibly −20 to −60, **unmeasured** |

I do not claim a number. What is measured is only the shape: one hypothesis-free-of-new-assumptions
lemma in, one 60°-step machinery out.

## 6. The single obligation, sharply

> **(O)** For a weak 5-colouring `c`, a five-cycle centre `x`, for a.e. `a : ℝ` and for `r = 1`:
> `∀ k : Fin 5, ∃ i : Fin 5, a + (sixty : ℝ) ∈ fiveSupport c hc x i ∧ k ∉ fiveDiag i`.

*Short derivation attempted.* Apply `five_endpoint_no_common` with the base angle `a' := a + 60°`.
It needs (i) `b` with `sin (b − a') ≠ 0` and (ii) `hy : FiveCenter c (x + direction a' + direction b)`.
(i) is free (choose `b` avoiding a countable set, and the hypothesis is a.e.-stable). (ii) is the whole
difficulty: no existing lemma yields a five-cycle centre at `x + direction a' + direction b`. Hence the
derivation is **not** available from the current lemmas, and the obligation reduces to a
centre-existence statement:

> **(O′)** A five-cycle centre `x` presents a.e. angle `a` with `FiveCenter c (x + direction a + direction b)`
> for some `b` with `sin (b − a) ≠ 0`.

(O′) is *not* obviously true, and I will not assert it. What can be said is that (O′) is stronger than
the endpoint mechanism uses (which needs one such pair, at the endpoint, not a.e.); so (O) is best
attacked not through (O′) but through a **support-transport at the 60° step**:

> **(O″)** `∀ᵐ a, ∀ i, a ∈ fiveSupport c hc x i → ∃ j, fiveAdj i j ∧ a + (sixty : ℝ) ∈ fiveSupport c hc x j`
> — the `stateSupport_shift_relation` instance (`FiveSupport.lean:55`) at `d = sixty` with `R := fiveAdj`.

(O″) is the missing `hR` hypothesis of `stateSupport_shift_relation`, and it is *strictly weaker* than
`five_support_step_ban`: the step ban forbids the transition a.e.; (O″) only says supports move to
adjacent states. If (O″) holds, then (D)/(N) transport across all six positions, and validity at
position 1 follows from validity at 0 by the finite asset's own `neighbour_family_push`. That is the
sharpest form I can defend: **(O″) is the smallest analytic statement whose proof would let the finite
asset operate on all six positions.**

## 7. What is *not* claimed

* The finite residue classification does **not** remove the analytic bridge. It replaces a case
  analysis, not an input: the (V) fact is still needed, and it still comes from the plane.
* (O), (O′) and (O″) are **not** proved here, and (O′) may be false as stated.
* No line saving is claimed; §5 gives shape, not measurement.
* The 72°-versus-60° reading: the six positions are `r · 60°` (`6 · 60° = 360°`), consistent with
  `sixty : Angles` in `five_support_step_ban`; I flag it because an earlier note of mine guessed 72°,
  which was wrong for this indexing.

## 8. Grades

| item | grade |
|---|---|
| the 21 finite lemmas and their content | [read] from `FiveCycleResidues.lean`, externally local-passed (21/21 reported) |
| the exact statements of `five_support_step_ban`, `five_support_trace`, `five_endpoint_no_common`, `five_no_common_adj`, `five_forced_label`, `stateSupport_shift_relation`, `FiveCenter` | [read] at the cited lines |
| that (I) is the interface, and that (O″) is its weakest sufficient transport form | [argued here] from the hypothesis shapes; not machine-checked |
| the "8 solutions, all with S(1)=S(5)={2,4}" claim | [imported] from the corrected audit, not re-derived here |
| (O), (O′), (O″) | **open**; no proof, and (O′) not asserted true |

---

# §9 CORRECTION: the (O″) claim is RETRACTED (models are abstract-only — see the block-17 banner above)

**Withdrawn:** §6's sentence "strictly weaker than the step ban", and the framing of (O″) as a bridge.

## 9.1 Quantifier analysis — the two statements are not comparable

Write `S a := {i : a ∈ fiveSupport c hc x i}` and `θ t := fiveState c hc x t`.

* **(O″)** `∀ᵐ a, ∀ i ∈ S a, ∃ j, fiveAdj i j ∧ j ∈ S (a + 60)` — a `∀∃` over **support sets**, with the
  witness `j` depending on `(a, i)`; nothing about `θ`'s values.
* **(SB)** (`five_support_step_ban`) for a *fixed* `a₀` and adjacent `i, j` with `i, j ∈ S a₀`:
  `∀ᵐ t ∂angularMeasure, ¬(θ t = i ∧ θ (t+60) = j) ∧ ¬(θ t = j ∧ θ (t+60) = i)` — a universal negation
  over **pairs of θ-values**.

Different quantifier shapes over different objects (`S` versus `θ`); membership `a ∈ S i` is a *closed
support* statement and does not determine `θ a`. Neither is a substitution instance of the other.

## 9.2 Countermodel: (O″) holds while (SB) fails ⇒ (O″) ⇏ (SB)

Take `ι = Fin 5` with `fiveAdj` the cycle. Let `g : ℝ → Fin 5` be 60-periodic, measurable, with every
level set dense (e.g. `g(t) = ⌊5 · frac(t/60)⌋` composed with a dense-set partition), and put
`θ t := (g t + ⌊t/60⌋) mod 5`.

* Every level set `{θ = i}` is dense: it is a union over `n ∈ ℤ` of `{g = i − n} ∩ [60n, 60(n+1))`,
  dense in each interval. Hence `fiveSupport` of every `i` is `ℝ,` so `S a = Fin 5` for every `a`.
* **(O″) holds:** for any `a` and any `i ∈ S a = Fin 5`, choose `j := i+1` (`fiveAdj i (i+1)`), and
  `j ∈ S (a+60) = Fin 5`. ✓
* **(SB) fails:** `θ (t+60) = θ t + 1` for a.e. `t`, so `{t : θ t = i ∧ θ(t+60) = i+1}` has full
  measure for every `i` — an adjacent transition occurring a.e., exactly what (SB) forbids. Its
  hypotheses are satisfied (`i, i+1 ∈ S a₀` for every `a₀`). ∎

So (O″) does not imply the step ban: the obstruction is that supports do not see `θ`'s transitions.

## 9.3 Countermodel: (SB) holds while (O″) fails ⇒ (SB) ⇏ (O″)

Let `supp i := ⋃_{n∈ℤ} [5n + i, 5n + i + 1]` (intervals of length 1, period 5 in the index), realised by
any `θ` constant on each interval with those level sets. Then `supp i ∩ supp j = ∅` for `i ≠ j`, so
**(SB)'s hypotheses are never satisfied and (SB) holds vacuously.** But for `a = 0`: `0 ∈ supp 0`, and
`60 ∈ supp 0` while `60 ∉ supp j` for `j ∈ {1,4} = Nb 0`; so the required witness `j` does not exist and
**(O″) fails** at `a = 0`. ∎

**Verdict (revised, block 18): the claim of strict weakness is withdrawn; incomparability is NOT claimed.** Quantifier shapes alone establish nothing, and the two models offered here are models of the abstract data only, so they cannot carry an incomparability claim about the actual objects. What stands is the weaker, sufficient statement: **no derivation of (O″) from (SB) is available**, and (O″) is withdrawn as a bridge. Any derivation of
one from the other must use more than `hw`/`hx` supply through these lemmas — i.e. a genuinely new
geometric input. §6's (O″) is therefore withdrawn as a bridge, and (O′)'s a.e. centre-existence claim is
withdrawn as unmotivated.


> **CORRECTIONS (block 17).** (i) §9's two countermodels are models of the **abstract** data
> `(S, θ)` only; their applicability to the actual objects is **retracted** — under
> `Angles = AddCircle (2*π)` a state function must be 2π-periodic (my `θ` gains +1 per turn), and the
> second model's closed-interval supports overlap at the endpoints. Only the quantifier observation
> survives. (ii) §10.3's clause "nothing else in the tree supplies (D)" is **wrong**:
> `PaletteTransport.lean:450 palette_sixty_disjoint` gives the one-centre two-angle palette form, and
> `Accumulation.lean:392 fiveState_adj` gives the level-set form. What is missing is the level-set →
> support upgrade; see `FIVE-CYCLE-D.md`, which supersedes §10.3's (D) paragraph.

# §10 The one bridge I can defend, and the obstruction made concrete

## 10.1 What the tree actually supplies, with exact types

| declaration | statement (abbreviated) |
|---|---|
| `Accumulation.lean:378` `fiveState_diag` | `(hw)(hx) : ∀ᵐ t : ℝ ∂volume, palette c hc x (t:Angles) = fiveDiag (fiveState c hc x (t:Angles))` |
| `Accumulation.lean:381` `fiveState_represents` | `(hw)(hx)(i) : …` (the state's palette is `fiveDiag i` a.e. on `{θ = i}`) |
| `FiveSupport.lean:86` `five_support_trace` | `(hw)(hx)(ha : a ∈ fiveSupport i) : ∃ b : TraceVector 5, IsTrace c hc (x + direction a) b ∧ ∀ j ∈ fiveDiag i, traceValue b j = 0` |
| `FiveSupport.lean:89` `five_support_step_ban` | as (SB) above |
| `FiveSupport.lean:23` `palette_neighbor_disjoint` | `(hw)(x)(a) : ∀ᵐ t ∂angularMeasure, Disjoint (palette c hc (x + direction a) t) (palette c hc x t)` |
| `FiveSupport.lean:9` `palette_neighbor_real` | `(hw)(x)(a)(i) : ∀ᵐ t : ℝ ∂volume, t ∈ liftPalette (x + direction a) i → t ∉ liftPalette x i` |
| `FiveSupport.lean:55` `stateSupport_shift_relation` | `(hf)(hR : ∀ᵐ t, R (f t) (f (t+d)))(ha : a ∈ stateSupport f i) : ∃ j, R i j ∧ a + d ∈ stateSupport f j` |
| `CyclicCore.lean:25` `five_endpoint_no_common` | `(hw)(hx)(hab : Real.sin (b−a) ≠ 0)(hy : FiveCenter c (x + direction a + direction b)) : ∀ k, ∃ i, a ∈ fiveSupport i ∧ k ∉ fiveDiag i` |

## 10.2 The bridge, stated once (no new `FiveCenter` hypothesis)

> **(B)** For a.e. `a : ℝ`, the six lists `S r := {i : a + r·(sixty:ℝ) ∈ fiveSupport c hc x i}`
> (`r : Fin 6`) satisfy (R) `S 0 = {0,1}` up to relabelling, (D) `Disjoint (S r) (S (r+1))`,
> (N) `∀ i ∈ S r, (Nb i ∩ S (r+1)).Nonempty`, and (V) `NotCommon (S r)`.
> Then the finite 21-lemma asset yields `False`.

(B) is not a new hypothesis about the *plane*: its four clauses are exactly the paper's (V)(D)(N)(R) over
the predicates the tree already has, and the finite asset's `valid_family_push`, `disjoint_family_push`,
`neighbour_family_push` are precisely the invariance lemmas needed to spend (B) after the relabelling.
The asset is proved; the bridge is therefore **only** about producing (B) from `hw, hx` alone.

## 10.3 Why (B) is not available from `hw, hx` — the obstruction, concretely

Of the four clauses, three have a mechanism in the tree and one does not:

* **(R)** is a relabelling/normalisation — no geometry needed.
* **(D)** is *not* `palette_neighbor_disjoint`: that lemma compares two **different centres**
  (`x` and `x + direction a`) at the same angle `t`, whereas (D) compares the **same centre** at two
  angles 60° apart. The tempting identification is invalid, and nothing else in the tree yields (D).
  A derivation would have to go through the transition machinery (`transition_abundance` +
  `transitionEdge_closed` at distance 1, plus `fiveState_diag`), which is a real argument, not a lookup.
* **(N)** likewise needs (D)-grade input: it asserts a neighbour of every state of `S r` sits in `S (r+1)`.
* **(V)** is produced by exactly one lemma, `five_endpoint_no_common`, and only under
  `hy : FiveCenter c (x + direction a + direction b)`. **No lemma in the 82-module tree constructs a
  five-cycle centre from an existing one.** `FiveCenter` is defined (`Accumulation.lean:358`) as
  `∀ i, TransitionEdge c i (i+1) x` and appears downstream only in hypothesis position.

Concretely: `five_support_trace` supplies, *per state* `i ∈ S r`, a trace vector vanishing on `fiveDiag i`.
(V) is a statement about the **union** structure of the labels — "some label is missing from every `D_i`,
`i ∈ S r`" — and there is no lemma converting a family of individual trace vectors into a joint-missing
label. The only route that does so is `five_local_palette → palette_open_exclusion →
transitionEdge_no_open_exclusion`, and its last step consumes `hy`, i.e. the second centre. That is the
whole obstruction, and it is a *missing construction*, not a missing estimate.

## 10.4 Grades for §§9–10

| item | grade |
|---|---|
| the rfl/proof-irrelevance correction (dedup smoke test) | [verified here] by definition of proof irrelevance; smoke file and CANDIDATE.md corrected |
| both countermodels in §9 | [proved here] on the abstract data `(S, θ)`; they refute implication *from that data*, and do not claim the implication fails for colouring-derived data |
| the retraction of "strictly weaker" | [concluded here] from §9.1–9.3 |
| (B) as the sufficient bridge, no new `FiveCenter` | [argued here] — the four clauses are exactly the asset's hypotheses, checked against `FiveCycleResidues.lean` |
| (D) ≠ `palette_neighbor_disjoint`, and (V)'s single producer | [read] at the cited lines |
| availability of (B) from `hw, hx` | **not available**; obstruction stated in §10.3 |
