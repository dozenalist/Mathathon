# A reusable contact/shift theorem, and the five-cycle branch rewritten on top of it

Source/analysis only; no build, no compute. Grades at the end. Retained assets cited by path:line.
**Lemma 6.7 is retained** (= `five_support_step_ban`), and no global `States` deletion is proposed.

## 1. The general theorem (no finite-sum machinery)

The tree already contains the only mechanism needed:

> **`stateSupport_shift_relation`** — `FiveSupport.lean:55`
> ```lean
> lemma stateSupport_shift_relation {f : ℝ → ι} (hf : Measurable f) {R : ι → ι → Prop} {d : ℝ}
>     (hR : ∀ᵐ t ∂volume, R (f t) (f (t + d))) {i : ι} {a : ℝ}
>     (ha : a ∈ stateSupport f i) : ∃ j, R i j ∧ a + d ∈ stateSupport f j
> ```
> with `stateSupport f i := (volume.restrict {t | f t = i}).support` (`FiveSupport.lean:39`) — note this is
> *syntactically* the definition of `fiveSupport` (`FiveSupport.lean:83`) with
> `f := fun t : ℝ => fiveState x (t : Angles)`.

Instantiating `R` with **support disjointness** gives the contact/transition theorem in one step:

> **Theorem T (contact/shift).** Let `f : ℝ → ι` be measurable, `ι` finite, `d : ℝ`, `S i := stateSupport f i`.
> Assume
> **(H)** `∀ᵐ t ∂volume, Disjoint (S (f t)) (S (f (t + d)))`.
> Then for every `i` and every `a ∈ S i`: `a + d ∉ S i`.
>
> *Proof.* Apply `stateSupport_shift_relation` with `R i j := Disjoint (S i) (S j)` and `hR := (H)`: there is
> `j` with `Disjoint (S i) (S j)` and `a + d ∈ S j`. If also `a + d ∈ S i`, then
> `a + d ∈ S i ∩ S j`, contradicting the disjointness. ∎

Two remarks that make T worth having:

* It is stated for **any** finite `ι` and **any** measurable `f`, so it is not five-cycle-specific. The
  five-cycle case is `ι = Fin 5`, `f = fiveState x (· : Angles)`, `d = sixty` (`PaletteTransport.lean:390`).
* Its hypothesis is *disjointness of the supports of the two states that actually occur*, not a
  statement about all pairs. That is what makes it cheap to discharge (§2).

**Corollary T′ (adjacency form).** With `R := fiveAdj` and `hR` the a.e. adjacency statement, T becomes
`a ∈ S i → ∃ j, fiveAdj i j ∧ a + d ∈ S j`. This is exactly `five_support_next` (`FiveSupport.lean:124`)
and its mirror `five_support_prev` (`:128`), which the tree proves that way. So T **unifies the
"neighbour" and "no self-contact" facts as two instances of one statement** — that is its conceptual value.

## 2. Discharging (H) in the tree — a finite union of null sets

`(H)` says: for a.e. `t`, the supports of the two states that occur at `t` and `t + sixty` are disjoint.
Its failure set is

```
E := {t : ¬ Disjoint (S (f t)) (S (f (t + sixty)))} = ⋃_{(i,j) : S i ∩ S j ≠ ∅} Q_ij,
   Q_ij := {t : f t = i ∧ f (t + sixty) = j}
```

a **finite** union (`ι = Fin 5`), so it suffices that each `Q_ij` with `S i ∩ S j ≠ ∅` is null. Two cases:

* **`¬ fiveAdj i j`** (this includes `i = j`, since `fiveAdj i i` is `i+1 = i ∨ i+1 = i`, false in `Fin 5`):
  `fiveState_adj` (`Accumulation.lean:392`) says `∀ᵐ t ∂angularMeasure, fiveAdj (state t) (state (t+sixty))`,
  so `Q_ij` is null. **No contact hypothesis needed.**
* **`fiveAdj i j` with `S i ∩ S j ≠ ∅`:** pick the contact point; **Lemma 6.7** (`five_support_step_ban`,
  `FiveSupport.lean:89`) gives a.e. absence of both transitions `i → j` and `j → i`, i.e. `Q_ij` and `Q_ji`
  null.

Hence `volume E = 0` and (H) holds. ∎

This is a finite union of null sets — *not* the identity `supp(Σ_j ν_j) = ⋃_j supp ν_j`. So this route
discharges T using **only** `fiveState_adj` + Lemma 6.7 + `stateSupport_shift_relation`, and it avoids both
the finite-sum support identity (Astra's route, audited in `FIVE-CYCLE-D.md` §8) and the varying-state
strict-sequence machinery. Two independent derivations of the same clause now exist; this one is shorter
and uses only existing API, so it is the one I recommend.

**Measure bookkeeping (the one technical step).** `fiveState_adj` and Lemma 6.7 are a.e. w.r.t.
`angularMeasure` on `Angles = AddCircle (2π)` (`Coloring.lean:17`), while `stateSupport` uses `volume` on
`ℝ`. `E` is a subset of `ℝ`; the nullity must be transported. The tree does exactly this in
`five_support_prev` (`FiveSupport.lean:128–137`): `angleMk_quasiMeasurePreserving.ae` followed by
`(measurePreserving_add_right volume (-sixty)).quasiMeasurePreserving.ae`. Same two lines apply to `E`.
I flag it because it is the only place a formalisation could snag; it is precedented, not new.

## 3. The exact input contract of the five-cycle branch

Reading `five_opposite_contacts_false` (`FiveSupport.lean:199`) and its ingredients:

| # | input | statement | source | role |
|---|---|---|---|---|
| C0 | adjacency | `∀ᵐ t, fiveAdj (state t) (state (t+sixty))` | `fiveState_adj`, `Accumulation.lean:392` | non-adjacent pairs never occur |
| C1 | contact propagation | contact at `a` (states `i, i+1` in `S a`) ⇒ `{i-1, i+2} ⊆ S(a+sixty)`-list (and the mirror at `a−sixty`) | `five_contact_next` `:171`, `five_contact_prev` `:185`; uses `five_support_next/prev` + **D** + `FiveComb.contact_neighbors` | moves a contact one step |
| C2 | **no 60° self-contact** | `a ∈ S i → a + sixty ∉ S i` | formerly `five_support_no_sixty` `:138` via `strict_state_no_unit_support` `States.lean:704`; **now Theorem T** | the single analytic input |
| C3 | finite graph arithmetic | `opposite_contacts` `:156`, `two_bans` `:160`, `contact_neighbors` `:153`, `neighbors` `:159` (all `by decide`) | `FiveSupport.lean:150–163` | pure `Fin 5` |
| C4 | step ban | `five_support_step_ban` `:89` = **manuscript Lemma 6.7**, p. 41 | `FiveSupport.lean:89` | closes, and (via §2) supplies (H) |

## 4. The five-cycle branch, human-readable

Fix `x` with `hx : FiveCenter c x` and a weak 5-colouring `c`. Write `S(a) := fiveSupportList x a` and
`state(a) := fiveState x a`.

1. **[C0]** For a.e. `a`, `state(a + 60)` is adjacent to `state(a)`.
2. **[T]** Hence, for every `a` and every `i`, `a ∈ S i → a + 60 ∉ S i` (§1–§2). This is (D).
   *Nothing here says anything about angles other than 60° shifts of a given `a`; in particular it does
   not license validity `(V)` at new angles.*
3. **[C1]** If `i, i+1 ∈ S(a)` (a *contact* at `a`), then `i−1, i+2 ∈ S(a + 60)` and also
   `i−1, i+2 ∈ S(a − 60)`. Proof: `C1` is exactly `five_contact_next`/`five_contact_prev`, whose inputs are
   `five_support_next`/`_prev` (instance T′) and two applications of (D) to rule out `i` and `i+1`
   themselves being in the shifted list.
4. **[C3+C2 ⇒ disjointness]** Suppose contacts at `a` (pair `i, i+1`) and at `b = a + 3·sixty`
   (pair `j, j+1`). By step 3, `{i−1, i+2} ⊆ S(a+sixty)` and `{j−1, j+2} ⊆ S(b−sixty) = S(a+2·sixty)`.
   If a state `k` lay in both lists, then `a + sixty ∈ S k` **and** `a + 2·sixty = (a+sixty) + sixty ∈ S k`,
   contradicting (D). So the two 2-element lists are **disjoint** — and this is where the branch spends
   (D), and only (D).
5. **[C3]** `FiveComb.opposite_contacts` then forces `j = i+1 ∨ j+1 = i`; `FiveComb.two_bans` produces a
   state `s` adjacent to both pairs, all of whose steps are one of the four banned ones.
6. **[C4]** The contact at `s` and the banned step together give `False` — this is the step ban of
   Lemma 6.7 again, and it is what makes `five_opposite_contacts_false` (`:199`) conclude `False`.

Conclusion: **two contacts 180° apart are impossible at a five-cycle centre.** That is
`five_opposite_contacts_false`, and it is the input to `CyclicCore.lean:119`, which uses it to kill the
accumulation sequence of five-cycle centres (`five_sequence_no_accumulation`).

## 5. What changes, and what is retained

**Retained, unchanged:** Lemma 6.7 (`five_support_step_ban`) — used twice above (steps 2 and 6); the trace
machinery (`five_support_trace` `:86`); the transport pattern (`five_support_prev` `:128`); the finite
`FiveComb` layer; `five_opposite_contacts_false` itself and every `CyclicCore` consumer.
**Removed from *this branch only*:** `strict_state_no_unit_support` (`States.lean:704`) and the
`strict_state_sequence_*` support it needs — they leave the branch because (D) no longer goes through
`five_support_no_sixty`'s old proof.
**Not removed:** `States.lean` itself. No global deletion is proposed.

## 6. Does graph structure alone give the contradiction? Contract, then countermodel

**No.** The finite layer's key lemma is
`opposite_contacts : ∀ i j, Disjoint ({i-1,i+2} : Finset (Fin 5)) {j-1,j+2} → (j = i+1 ∨ j+1 = i)`
(`FiveSupport.lean:156`) — it **takes the disjointness as a hypothesis**. Step 4 above is precisely the
proof of that hypothesis, and it uses (D); nothing in `Fin 5` supplies it.

**Exact input contract** for `five_opposite_contacts_false`: `C0 + (D) + FiveComb.{contact_neighbors,
opposite_contacts, neighbors, two_bans} + Lemma 6.7`. Removing `(D)` leaves the contract unsatisfied;
removing any `FiveComb` lemma leaves the final contradiction unreachable; removing C0 breaks step 1.

**Countermodel to "graph alone".** Take the contact pair to be the *same* pair at both ends:
`i = j = 0`, contacts at `a` (states `0, 1`) and at `a + 3·sixty` (states `0, 1`). All the finite facts
`contact_neighbors`, `neighbors`, `adjacent_oriented`, `two_bans` remain satisfied (`Adj` is still the
5-cycle), but `Disjoint ({4,2}) ({4,2})` is **false**, so `opposite_contacts` yields nothing and no
contradiction is derivable from the finite layer. What rules this configuration out is exactly (D): with
both contacts of the same pair 180° apart, state `4` would need `a+sixty` and `a+2·sixty` in its support.
So the contradiction is *not* graph-structural; the graph is consistent, and the measure/support input is
what forbids the configuration. (This is a model of the finite layer, not a colouring.)

## 7. Grades and non-licences

| item | grade |
|---|---|
| Theorem T and its corollary T′ | [proved here] — one application of `stateSupport_shift_relation` plus `Set.disjoint_left` |
| (H) from `fiveState_adj` + Lemma 6.7 (finite union of nulls) | [argued here] with every premise cited; the `angularMeasure → volume` transport is precedented (`FiveSupport.lean:128–137`) but not performed |
| input contract C0–C4 | [read] each row cited to a line |
| the five-cycle branch steps 1–6 | [read + rewritten] faithful to `five_opposite_contacts_false` `:199` and `CyclicCore.lean:119` |
| graph-alone insufficiency + model | [argued here] on the finite layer only, labelled as such |
| machine verification | **none** — no build in this block |

**Not licensed by this document.** Nothing above produces `(V)` (validity, `∀ k ∃ i ∈ S, k ∉ D i`) at any
angle other than where `five_endpoint_no_common` (`CyclicCore.lean:25`) already gives it. Clause (D) is now
proved; clause (V) remains the one open input of bridge (B), and its obstruction is unchanged: no lemma
constructs a second five-cycle centre.
