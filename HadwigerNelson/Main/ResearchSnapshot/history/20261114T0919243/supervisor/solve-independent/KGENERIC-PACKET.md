# Source packet: the k-generic finite-translation/compactness lemma

Purpose: pin down exactly what already exists, what is `Fin 5`-specific, and what a k-generic version
would add. **Nothing here was compiled.** No Lean was launched in this block. Everything marked
"existing" is quoted from source I read this block; everything marked "proposed" is **new,
uncompiled source** and carries no authority until built.

Paths are relative to the repository root. Hashes are of the files as read this block.

| file | sha256 |
|---|---|
| `lean/OAI/Geometry/PlaneColoring/Converse.lean` | `5bde95d2ec3cb518a2ece36f544b69eb25f550f3f2f231a7df5c8a9ba4098248` |
| `lean/OAI/Geometry/PlaneColoring/NullSetRobust.lean` | `887a6bbe6b83f87a3baf60823cf586a4b2f9539e3549697caa9732942d627cc9` |
| `lean/OAI/Geometry/PlaneColoring/States.lean` | `941fcbdcd90fb50426d4588d62ea10f9bdc882d455f546f2095ead91a0439340` |
| `lean/OAI/Geometry/PlaneColoring/Coloring.lean` | `70a2f493ed99008d6a6c37da50c32c22461832469773352406178790fa078898` |

## 1. The three ingredients, with exact names and locations

**(a) Compactness / de Bruijn–Erdős — already k-generic.**
`theorem exists_properColoring_of_finset` at `Converse.lean:33`:

    theorem exists_properColoring_of_finset {k : ℕ} [NeZero k]
        (h : ∀ F : Finset ℂ, ∃ c : ℂ → Fin k,
          ∀ x ∈ F, ∀ y ∈ F, ‖x - y‖ = 1 → c x ≠ c y) :
        ∃ c : ℂ → Fin k, ProperColoring k c

Proof mechanism (read, not built): `letI : CompactSpace (ℂ → Fin k) := Pi.compactSpace`, the closed
sets `t p = {c | c p.1 ≠ c p.2} ∪ {c | ¬ ‖p.1 - p.2‖ = 1}` for `p : ℂ × ℂ`, the finite intersection
property supplied by the hypothesis `h` applied to `u.image Prod.fst ∪ u.image Prod.snd`, and
`IsCompact.inter_iInter_nonempty`-style closure. **No `Fin 5` anywhere. Usable verbatim at any `k`.**

**(b) Translation with a uniform density limit — already k-generic, but heavier than needed.**
`theorem finite_config_proper` at `Converse.lean:13`:

    theorem finite_config_proper {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (hw : WeakColoring k c)
        {ι : Type*} [Finite ι] (z : ι → ℂ) :
        ∃ q : ℂ, ∀ v w : ι, ‖z v - z w‖ = 1 → c (q + z v) ≠ c (q + z w)

Depends on `lemma finite_density_realization` at `States.lean:173` (statement quoted there:
`(hc : Measurable c) (hw : WeakColoring k c) (z : ι → ℂ) (J : ι → Finset (Fin k))
(hz : ∀ v, DensityOne {q | c q ∈ J v} (z v)) : ∃ q, (∀ v, c (q + z v) ∈ J v) ∧ ∀ v w, ‖z v - z w‖ = 1 →
c (q + z v) ≠ c (q + z w)`), with `DensityOne` defined at `WeakColoring.lean:119`.
Both are k-generic. **But this route needs `Measurable` and `WeakColoring`** — i.e. the density of a
*measurable* colouring — so it does **not** apply to an arbitrary colouring of a null-set complement.
It is the wrong tool for the transfer lemma; it is the tool for the weak-to-strong direction.

**(c) Null-set translation and the `Fin 5` conclusion — k-generic in the middle, specific at the ends.**
`theorem not_proper_five_coloring_compl_null` at `NullSetRobust.lean:20`:

    theorem not_proper_five_coloring_compl_null {Z : Set ℂ} (hZ : volume Z = 0) :
        ¬ ∃ c : ℂ → Fin 5, ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y

Its proof body splits cleanly:

| step | code | k-generic? |
|---|---|---|
| `hsingle` | `∀ x, volume ((fun z => z - x) '' Z) = 0`, via `measure_preimage_add_right` | **generic** (no `k`, no `Fin 5`) |
| `hbad` | `volume (⋃ x ∈ (F : Set ℂ), (fun z => z - x) '' Z) = 0`, induction on `F` | **generic** |
| `hne` | that union is `≠ univ`, because `volume (univ) = 0` contradicts `volume (ball 0 1) > 0` | **generic** |
| `hv` | pick `v` outside it | **generic** |
| witness | `refine ⟨fun x => c (x + v), ?_⟩`, then `x + v ∉ Z` and `y + v ∉ Z` from `v`'s choice, and `hc (x+v) … (y+v) …` | **generic** |
| conclusion | `exact no_proper_five_coloring (exists_properColoring_of_finset hfin)` | **`Fin 5`-specific**: `no_proper_five_coloring` is `Five.lean:133`, `¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c` |

So the `Fin 5` dependence is exactly **one line**, at the end, and `Fin 5` also appears in the theorem's
own signature. Everything between is already generic.

*Note on `ProperColoring`:* there are two definitions —
`Coloring.lean:7` (`def ProperColoring (k : ℕ) (c : ℂ → Fin k)`) and `Basic.lean:26`
(`def ProperColoring (k : ℕ) : Prop`, on `Plane`). The transfer lemma needs the **former**; the latter
belongs to the `planeChromaticNumber` development. Do not mix them.

## 2. Proposed k-generic lemma (NEW, UNCOMPILED, no authority)

Stated in the same namespace, to sit beside `not_proper_five_coloring_compl_null`:

    /-- A proper k-colouring of the complement of a null set gives a proper k-colouring of the plane.
    (Null-set transfer, upper-bound direction; the file's `not_proper_five_coloring_compl_null` is the
    k = 5 lower-bound counterpart.) -/
    theorem exists_properColoring_of_compl_null {k : ℕ} [NeZero k] {Z : Set ℂ}
        (hZ : volume Z = 0) (c : ℂ → Fin k)
        (hc : ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y) :
        ∃ d : ℂ → Fin k, ProperColoring k d := by
      refine exists_properColoring_of_finset (fun F => ?_)
      -- same body as `hfin` in `not_proper_five_coloring_compl_null`, verbatim
      ...

The body is the existing `hfin` block with `Fin 5` → `Fin k` and the trailing contradiction dropped.
Expected import needs: `Converse` (for `exists_properColoring_of_finset`) and `MeasureTheory` for
`measure_preimage_add_right`; **`Five` is not needed**, which also removes the heavy downstream
dependency from the statement. Note `NeZero k` is only there because `exists_properColoring_of_finset`
requires it (it needs `Fin k` inhabited to write down the colouring).

**Known risks for a local check** (not resolved here): (i) `Finset.induction_on` and the `Set.biUnion`
rewriting are transcribed from the existing proof, so they should go through, but `Fin 5 → Fin k` may
change `simp` behaviour in `hzero`/`hpos`; (ii) `hpos.ne'` and the `le_antisymm` step are
cardinality-free and should be unaffected; (iii) the `by ring` closing `x + v - x = v` is
sign-convention dependent — the existing file uses `z - x` images and `x + v`, which is consistent, so
keep both conventions together.

## 3. What this is and is not

* **Mathematical proof** (mine, this and the previous block): the transfer lemma and its
  hypothesis analysis, with the four corrections recorded in `NULL-TRANSFER.md`.
* **Existing compiled theorem** (not built by me): `exists_properColoring_of_finset` and
  `finite_config_proper` in `Converse.lean`; `not_proper_five_coloring_compl_null` in
  `NullSetRobust.lean`; `finite_density_realization` in `States.lean`. These are reported as present in
  the tree and as passing in `results/VERIFICATION.md`'s build log; I read them, I did not compile them,
  and I make no independent axiom claim.
* **Newly written, uncompiled source**: the `exists_properColoring_of_compl_null` stub above. It is a
  sketch with an elided body, not a proof.

## 4. Next step if a local serial build is authorised

Add the stub (with the body filled in) to `NullSetRobust.lean` or a new module importing only
`Converse`; build with the pinned `source scripts/env4341.sh` toolchain under the serial local-check
workflow; then `#print axioms` on the new theorem. Cheap and self-contained; **not done here** because
this block runs no Lean.
