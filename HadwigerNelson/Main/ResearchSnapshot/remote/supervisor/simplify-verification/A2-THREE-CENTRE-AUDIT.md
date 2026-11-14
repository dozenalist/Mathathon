# Independent audit of A2 (three-centre fixed-state support exclusion)

Block 21. Source reading and proof analysis only; no builds, no computation. Grades **[S]** source read,
**[S+]** source read and the step follows at the quoted line, **[P-v]** I checked the mathematics myself,
**[C]** my reading, **[R]** retraction of my own earlier text. Timestamp in `STATUS.json` (from the clock).

## 0. Two retractions of my own earlier claims

**(R1) The "strict inclusion" remark is withdrawn.** For a **finite** index set
`closure (⋃_j Q_ij) = ⋃_j closure (Q_ij)`, so my sentence that "closure of a union is in general strictly
larger than the union of closures" is **wrong in this setting** and is struck. Consequence stated plainly: the
closure reading of the joint-pair theorem is **open** — I have neither proof nor counterexample — and I stop
producing abstract counterexamples for it. The positive-support theorem (which is what the Lean and A2 use) is
unaffected.

**(R2) The `FourSupport` bridge is invalid, and my §8.2 of `JOINT-PAIR-SUPPORT-AUDIT.md` is withdrawn.** Two
independent reasons, both verified at source:

* **type-level**: `interfaceStateSupport_no_unit` (`Interfaces.lean:266-268`) assumes only
  `hg : ∀ᵐ t, fourGroup (fourState c hc x t) ⊆ palette c hc x t`. It carries **no** `FourCenter c x`.
  `four_support_no_sixty` (`FourTransport.lean:218-219`) **requires** `hx : FourCenter c x`. No chord or
  lift lemma can manufacture `FourCenter` from `hg`;
* **dependency-level**: `four_support_no_sixty`'s proof goes through `four_support_sequence_no_unit`
  (`FourContinuity.lean:441`), whose first line is `exact strict_state_sequence_false …` (`:452`) — i.e. it
  reaches `States:683`, one of the three declarations A2 is required to avoid.

So the FourTransport route is not an independent replacement, exactly as the referee says. My earlier line
"`four_support_no_sixty` already exists without `States:704`" was literally true and practically useless: it
buys `:683` instead.

## 1. Statement match with `States.lean:704`

| `strict_state_no_unit_support` (`States.lean:704-711`) | A2's target | match |
|---|---|---|
| `hc : Measurable c`, `hw : WeakColoring k c` | same | ✓ |
| `{x : ℂ}`, `{J K : Finset (Fin k)}`, `{X : Fin k}` | same | ✓ |
| `hlabels : ∀ i, i ∉ J ∪ K ↔ i = X` | same | ✓ |
| `hA : RealState hc x A J`, `hB : RealState hc x B K` | same | ✓ |
| `hp : 0 < volume A` | same (positivity of **A** only) | ✓ |
| `hb : b ∈ (volume.restrict B).support`, `hd : d ∈ …` | same | ✓ |
| conclusion `‖direction b - direction d‖ ≠ 1` | same | ✓ |

**No hypothesis is added and none dropped.** In particular no `FourCenter`, no `FiveCenter`, no interface data,
no positivity of `B`, and no periodicity of `A` ✓.

## 2. The three ingredients, checked at source (verbatim statements)

1. `state_support_avoiding_trace` (`BoundaryTrace.lean:24-27`):
   `(hA : RealState hc x A J) {a : ℝ} (ha : a ∈ (volume.restrict A).support) →
    ∃ b : TraceVector k, IsTrace c hc (x + direction (a : Angles)) b ∧ ∀ i ∈ J, traceValue b i = 0`.
   **General in `k`** (the file's `variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)`), and its hypothesis is
   membership in the **support**, not positivity — so A2's "no positivity of B" is correct.
2. `avoiding_trace_palette` (`:53-55`): `(hb : IsTrace c hc x b) (hJ : ∀ i ∈ J, traceValue b i = 0) →
    ∀ᵐ t ∂angularMeasure, ¬ palette c hc x t ⊆ J`.
3. `palette_neighbor_disjoint` (`FiveSupport.lean:23-24`):
   `(hw : WeakColoring k c) (x : ℂ) (a : ℝ) → ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc (x + direction (a : Angles)) t) (palette c hc x t)`.
   **General in `k`** (`FiveSupport.lean:7` `variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)`), with the
   **same** angular parameter `t` at both centres — exactly the shape A2 uses.

**Dependency claim verified by count**: `grep -c strict_state` over the three files gives
`BoundaryTrace.lean: 0`, `PaletteTransport.lean: 0`, `FiveSupport.lean: 1` — and that single occurrence is in
`five_support_no_sixty` (`:144`), **after** the two general neighbour lemmas at `:9` and `:23`. So the three
ingredients do not invoke `States:547`, `:683` or `:704`. ✓

## 3. The three disjointness directions

Let `y = x + direction b`, `z = x + direction d`. Hypothesis `‖direction b - direction d‖ = 1` with both
vectors of norm 1 is **equivalent** to the included angle being `π/3`, hence by the law of cosines
`‖y - z‖² = 1 + 1 - 2·(1/2) = 1`. So `x, y, z` is an equilateral unit triangle ✓ **[P-v]**.

* `P_y ⊥ P_x`: `palette_neighbor_disjoint hw x b` (displacement `direction b = y - x`) ✓
* `P_z ⊥ P_x`: `palette_neighbor_disjoint hw x d` (displacement `direction d = z - x`) ✓
* `P_y ⊥ P_z`: `palette_neighbor_disjoint hw y α` where `direction α = z - y` exists because `‖z - y‖ = 1`;
  then the theorem at base `y` with displacement `z - y` gives `P_{y + (z-y)} = P_z ⊥ P_y` ✓

Three applications, three exceptional null sets, one finite intersection. All centres and angles are fixed
before the exceptional sets are taken — A2's sentence is correct and matters (no centre-dependent null set).

## 4. The unique-outsider forcing, and the a.e. bookkeeping

*`RealState hc x A J := MeasurableSet A ∧ ∀ i ∈ J, A ≤ᵐ[volume] liftPalette c hc x i` (`States.lean:92-93`),
so after a finite intersection over `i ∈ J`, `t ∈ A → J ⊆ palette x t` for a.e. **real** `t` ✓ — and this is
precisely the device `state_support_avoiding_trace` itself uses internally
(`ae_all_iff.mpr (fun i => ae_all_iff.mpr (fun hi => hA.2 i hi))`).

*Finite label fact*: if `i ∈ P_y \ K`, then `i ∉ P_x` by disjointness, so `i ∉ J` because `J ⊆ P_x`; with
`i ∉ K` this gives `i ∉ J ∪ K`, hence `i = X` by `hlabels`; so `X ∈ P_y`. Symmetrically `X ∈ P_z`. Contradicts
`P_y ⊥ P_z`. **[P-v]** — correct, and it needs neither a palette cardinality bound nor `Disjoint J K`.

*Eighth-of-a-point bookkeeping*: the five statements live on two spaces — (i) `RealState` on `ℝ`, (ii) the trace
and `avoiding_trace_palette` statements, (iii) `palette_neighbor_disjoint`, all on `Angles` with
`angularMeasure`. Pulling (ii),(iii) back along `angleMk` (`angleMk_quasiMeasurePreserving.ae`, used inside
`state_support_avoiding_trace` itself) makes all five conull statements about **real** `t`; a finite
intersection is conull; and `0 < volume A` gives a real `t ∈ A` satisfying all of them ✓. No a.e. statement is
used at a point where it is unavailable, and nothing is claimed about the *centre* `x` beyond `RealState`.

## 5. Verdict on A2

**The paper argument is sound**, with no added hypothesis, no use of `States:547/:683/:704`, and its three
ingredients matching the uses verbatim (checked above). The only new mathematics is (a) the equilateral-triangle
observation (elementary, and stated in the right direction: the *unit chord* hypothesis **is** the *unit side*
of the triangle), and (b) the finite-label forcing fact (elementary, general in the label universe). This is a
**paper candidate**: I found no gap, but it is not a Lean result and no integration is claimed.

**What it would remove if formalised**: the *fixed-state* consumers' dependence on the strict sequence chain —
i.e. the call at `FiveSupport.lean:144` inside `five_support_no_sixty`, and the call at `Interfaces.lean:277`
once the body is swapped (its statement is identical). It does **not** remove
`strict_state_sequence_false` itself (the moving-centre theorem), and `States:704` as a *declaration* could only
be deleted once both consumers are switched **and** the source-order/cycle issue A2 describes is resolved.

## 6. Closed avoiding-trace carrier: the three questions

The referenced packet (`a2-closed-carrier-proof.txt`) is **not present** in the tree
(`find . -name '*closed-carrier*'` returns nothing), so I audit the mathematical questions only and flag that
the packet itself is unaudited.

1. **Is the carrier projection closed because `TraceVector` is compact?** `TraceVector k` is compact — the
   existing proof uses `isCompact_univ` on it (`BoundaryTrace.lean:46`). The carrier set is
   `{b : TraceVector k | ∀ i ∈ K, traceValue b i = 0}`. If `b ↦ traceValue b i` is continuous (it is, in the
   topology used by `traceCode_tendsto_iff`, which is entrywise), then each fibre condition is closed and a
   finite intersection of closed sets is closed ✓. So yes — **the compactness route works**, provided the
   carrier is defined as a subset of `TraceVector k` *with the same topology*. That the limit of traces at
   `x_n → x` is a trace at `x` is `trace_of_realization`, already used in `state_support_avoiding_trace` ✓.
2. **Are zero L² coordinates closed?** Yes: `{b | traceValue b i = 0}` is the preimage of `{0}` under a
   continuous map into `L²(angularMeasure)`, and `{0}` is closed ✓ (finite intersection over `i ∈ K`).
3. **Can the limit positive `J`-state replace the `A_n`-L¹ input?** At a single centre, `RealState` gives
   `A ≤ᵐ liftPalette i` and `0 < volume A` gives the point; the sequence data `A_n` is then unused. In
   `FourContinuity.lean:441-455` positivity at the **limit** centre is precisely how the existing proof gets it
   (`hy : FourCenter c y`, `four_realState_positive … y r`). So the shape is plausible; **what I cannot verify
   is whether the existing consumer's hypotheses suffice to run A2's three-centre argument at the limit** —
   that requires reading the consumer, which needs the missing packet. Flagged as the open item.

**No global conclusion is drawn from any angular or local model**: everything above is about the named
declarations at the cited lines.

## 7. Banked from the local run

The generic contact-ban theorem and `five_support_no_sixty_joint_pair` are reported **passed** locally
(Lean 4.34.1 / mathlib `d13f23b`, standard axioms, source sha256
`9a904d4d7165889a5b12c77ea4e1646e436a0f5de4d4d057e2ee20d5e6f82ba1`), originals unchanged, Lemma 6.7
retained. That is a local result reported to me; I did not re-run it.
