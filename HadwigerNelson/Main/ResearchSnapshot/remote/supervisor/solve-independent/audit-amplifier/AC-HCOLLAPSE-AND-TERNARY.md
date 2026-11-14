# AC's `H i → J` collapse, proved; and why the three-label residual has no rigidity

Source-only. **No computation, no Lean.** Read-only: `AngularBoundary.lean`, `BoundaryTrace.lean`,
`Rigidity.lean`, `BinaryPalettes.lean`. Grades: **[proof]** = mine, written out; **[source]** = declaration
read with its line; **[candidate]** = paper-level, unverified.

## 1. The `H i → J` collapse, finished

**Setting.** `c : ℂ → Fin k` measurable, `WeakColoring k c`; `ι` a finite type; `K : ι → Set ℂ`;
`H : ι → Finset (Fin k)`; hypothesis **(H2)** `∀ i, ∀ j ∈ H i, Disjoint (spatialSupport c j) (Straddle (K i))`,
where (`AngularBoundary.lean:308`) `spatialSupport c j = (volume.restrict {z | c z = j}).support`.

**Lemma A (support exclusion ⟹ a.e. colour exclusion on the straddle).**
For every `i` and every `j ∈ H i`, the set `{z ∈ Straddle (K i) | c z = j}` is null.

*Proof.* Write `A_j := {z | c z = j}`, measurable since `c` is. Let `D_j` be the set of Lebesgue
density-one points of `A_j`; the density theorem gives `volume (A_j \ D_j) = 0`. Take
`z ∈ A_j ∩ D_j ∩ Straddle (K i)`. `Straddle (K i)` is open (`straddle_isOpen`, `AngularBoundary`), hence a
neighbourhood of `z`; so for every `r > 0` small enough that `B(z,r) ⊆ Straddle (K i)` we have
`volume ((volume.restrict A_j) (B(z,r))) = volume (A_j ∩ B(z,r)) > 0`, because `z` is a density-one point
of `A_j` (the ratio tends to `1`). As the balls are a neighbourhood base, `volume.restrict A_j` charges
every neighbourhood of `z`, i.e. `z ∈ spatialSupport c j`. That contradicts (H2). Hence
`A_j ∩ D_j ∩ Straddle (K i) = ∅`, and since `A_j ∩ Straddle (K i) ⊆ (A_j \ D_j) ∪ (A_j ∩ D_j ∩ Straddle (K i))`
the left side is null. ∎

**Lemma B (the collapse).** Under (H2), with `J := univ \ ⋃ i, H i`,

    ∀ᵐ z, (∀ i, z ∈ Straddle (K i)) → c z ∈ J .

*Proof.* By Lemma A, for each pair `(i, j)` with `j ∈ H i` the set `{c = j} ∩ Straddle (K i)` is null.
The index set `ι` and each `H i` are finite, so the union over all such `(i,j)` is null. Off that null set,
`z ∈ Straddle (K i)` implies `c z ∉ H i` for every `i`, hence `c z ∉ ⋃ i, H i`, i.e. `c z ∈ J`. ∎

**Why this is the collapse and not a weakening.** The residual `J` is a *single* set, independent of `i`,
precisely because the intersection is taken over **all** of `ι`. That is what
`continuum_outer_restriction` (`AngularBoundary.lean:259`) needs: its hypothesis is
`hJ : ∀ᵐ z, (∀ i ∈ E, z ∈ Straddle (K i)) → c z ∈ J` for one fixed `J`, and by Lemma B it is discharged
with `E := Finset.univ` and `J := univ \ ⋃ i, H i`. The `E`-dependence of the conclusion (the side
condition `∀ i ∈ E, 0 < ⟪direction t, v i⟫`) is *not* affected: it is a condition on `t`, and with the
common `v` of (H1) it reduces to `0 < ⟪direction t, v⟫`. So my previously flagged step closes, and the
reason the `H i`-dependence is harmless is exactly the finiteness of both `ι` and each `H i`.

**Consumer, stated.** Under (H1)–(H3) with `J = {a,b}`, Lemma B plus `continuum_outer_restriction`
(for `⟪direction t, v⟫ > 0`) and `continuum_inner_restriction` (`:279`, for `< 0`) give
`(palette c hc x t ∩ {a,b}).Nonempty` a.e., i.e. `BinaryCenter c hc x a b`, which is the input to
`binary_alternation`. **Note on sides (per the instruction):** the two restrictions are applied at
*different* `t`-signs, each licensed by its own strip lemma; no claim is made that one `W` carries
per-continuum incompatible radial sides.

## 2. The three-label residual: what would replace the rigidity, and where it fails

Set `|J| = 3`, `J = {a,b,d}`. Lemma B still gives `(palette ∩ {a,b,d}).Nonempty` a.e. — a **ternary hit**.
But `binary_alternation` needs a *pair* hit, so the binary route stops here.

**The statement that would be needed [proposed].**

> **(TR3)** Let `c` be measurable weak, `U, V` open with `c q ∈ {a,b,d}` a.e. on each, `p ∈ U`,
> `p+v ∈ V`, `p+w ∈ V` with `‖v‖ = ‖w‖ = 1` and `transverseDet v w ≠ 0`. Then
> `∃ r > 0, ∃ i ∈ {a,b,d}, ∀ᵐ q ∈ B(p,r), c q = i`.

This is the exact `{a,b} → {a,b,d}` transposition of `binary_open_local_rigidity` (`Rigidity.lean:179`),
whose conclusion is the same with `∃ i : Fin k` (no membership clause).

**Where the proof fails, exactly — a named step that becomes false.** The whole two-label content of
`binary_open_local_rigidity` is one invocation, at the line
`have he02 := binary_two_edges (hcol 0) (hcol 1) (hcol 2) (hqp 0) (hqp 1)`. That lemma
(`Rigidity.lean:168`) is

    lemma binary_two_edges {ι} {a b u v w : ι} (hu : u=a ∨ u=b) (hv : v=a ∨ v=b) (hw : w=a ∨ w=b)
        (huv : u≠v) (hvw : v≠w) : u = w

— the two-label pigeonhole: on the even path, three successive points coloured in `{a,b}` with two unit
pairs have their *outer* labels **equal**. The ternary transposition is

    (hu : u ∈ {a,b,d}) (hv : v ∈ {a,b,d}) (hw : w ∈ {a,b,d}) (huv : u≠v) (hvw : v≠w) : u = w

and this is **false**, with the one-line counterexample `u = a`, `v = b`, `w = d` (all three distinct, so
`u ≠ v` and `v ≠ w` both hold, yet `u ≠ w`). Over three labels a unit-pair chain does **not** determine the
label at the far end; only the two-label case does, because there `≠` is the same as "the other one".

**Consequence, propagated.** With `binary_two_edges` unavailable, `binary_open_local_rigidity` cannot
produce its conclusion `∃ r>0, ∃ i, c = i a.e. on B(p,r)`. The next lemma in the chain,
`connected_local_ae_constant` (`Rigidity.lean:418`), takes `hl : ∀ p ∈ S, ∃ i, p ∈ essentialLocalSet c i`
and is **label-agnostic** — it would work verbatim for a three-element palette — but it receives no input,
so it cannot fire. Hence `binary_strip_rigidity` (`BoundaryTrace.lean:248`) and therefore
`binary_strip_palette_rigidity` (`:280`) have no three-label analogue by this route. **The failure is not a
missing estimate; it is a false combinatorial step.**

**Explicit local data witnessing the failure.** At a transverse contact `p` with unit `v, w`
(`transverseDet v w ≠ 0`), put three points at unit separation: `q_u := p + v`, `q_v := p + v + e`,
`q_w := p + v + 2e` with `‖e‖ = 1` chosen so the even-path edges hold, and assign
`c(q_u) = a`, `c(q_v) = b`, `c(q_w) = d`. Then `huv` and `hvw` hold (unit pairs) and all three colours lie
in `{a,b,d}`, yet `c(q_u) ≠ c(q_w)` — the exact negation of the needed conclusion. This is **local data
only**: it is a three-point label pattern, not a plane colouring, and I do **not** claim it extends to a
`WeakColoring`; it is offered solely as the witness that the named step is false as transposed.

**A source-licensed restricted version, with a consumer.** There is one clean restriction: if the third
residual label is **a.e. absent from the palette at `x`**, i.e. `liftPalette x d` is null, then
`(palette ∩ {a,b,d}).Nonempty` a.e. upgrades to `(palette ∩ {a,b}).Nonempty` a.e., i.e.
`BinaryCenter c hc x a b`, and the whole binary chain (alternation, `binary_strip_palette_rigidity`) applies
unchanged. *Finite-interface consumer:* in the 6-cycle setting, **two** consecutive aligned interfaces
`E_1 = {1,2}`, `E_2 = {2,3}` exclude `{1,2,3}`, leaving the **three**-label residual `{0,4,5}`; the
restricted version applies **iff** label `4` is a.e. absent at `x`, which is *not* implied by the interface
data. So the consumer is conditional, and I flag that the condition is the whole content — it is not
discharged here.

## 3. Scope

* **[proof]** Lemma A, Lemma B, and the closure of the previously flagged step. The collapse needs only
  measurability, the density theorem, openness of `Straddle`, finiteness of `ι` and of each `H i`.
* **[proof]** The transposition of `binary_two_edges` to a three-element palette is **false**, with the
  explicit counterexample `(u,v,w) = (a,b,d)`.
* **[proposed]** `(TR3)`; **[local data]** the three-point witness for the false step, explicitly not a plane
  colouring.
* **[conditional]** The restricted version needs `liftPalette x d` null; consumer = two aligned interfaces,
  residual `{0,4,5}`, conditional on label `4` being absent at `x`.
* **Not claimed:** any global conclusion; any model as `WeakColoring`; any blanket no-go — the ternary case
  is left as an open problem with a located obstruction, not as an impossibility. AC is unchanged and still
  a paper-level candidate; non-aligned geometry is Astra's parallel track and is not touched here.
