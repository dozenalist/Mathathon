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

## 2. The k-generic lemma: COMPLETE source, UNCOMPILED

File: `k_generic_transfer.lean` (sha256 `8a8fc2cb095321cd0d93a0f0aea6e0240bc9098362478e4ddf4f448876272af7`).
**The body is complete - there is no ellipsis anywhere in the proof.** (An earlier revision of this
packet described the body as "elided at `...`"; that label was stale, the file was checked, and it is
removed. The two `...` occurrences in the file are prose: one in the revision note, one in an import
chain comment. Verified mechanically: the text between the theorem header and `end
EuclideanFiveColor` contains 0 occurrences of `...` and ends with
`exact exists_properColoring_of_finset hfin`.) **Status remains UNCOMPILED: no Lean was run.**

    theorem exists_properColoring_of_compl_null {k : ℕ} [NeZero k] {Z : Set ℂ}
        (hZ : volume Z = 0) (c : ℂ → Fin k)
        (hc : ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y) :
        ∃ d : ℂ → Fin k, ProperColoring k d

The transcription is mechanical with **exactly two edits**: `Fin 5 → Fin k` in the type of `hfin` and
in the statement, and the final `exact no_proper_five_coloring (...)` replaced by
`exact exists_properColoring_of_finset hfin`. The inner proof term is kept in the original shape
(`have hfin : ∀ F : Finset ℂ, ∃ d : ℂ → Fin k, … := by intro F; …`) precisely so that the block is
character-identical to the source apart from the type.

**Why the `Fin 5 → Fin k` edit is low-risk:** the body of `hfin` never mentions `Fin` at all. It uses
only `volume`, `Set`, `Finset`, and `c`'s type, all of which are unchanged. Every closure
(`by ring`, `by positivity`, `by simpa only [add_sub_add_right_eq_sub]`) is `k`-free. So the body is
already type-generic as written.

**Binders and API checked by source reading (not by compiling):**

| item | source | check |
|---|---|---|
| `ProperColoring (k) (c : ℂ → Fin k) := ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y` | `Coloring.lean:7` | the form the conclusion needs; **not** the `Basic.lean:26` version on `Plane` |
| `exists_properColoring_of_finset {k} [NeZero k] (h : ∀ F : Finset ℂ, ∃ c : ℂ → Fin k, ∀ x ∈ F, ∀ y ∈ F, ‖x-y‖=1 → c x ≠ c y) : ∃ c, ProperColoring k c` | `Converse.lean:33` | my `hfin` has exactly this hypothesis shape, with `c` renamed `d` |
| `[NeZero k]` required | `Converse.lean:33` | carried on my statement; nothing in my body needs it |
| `c` is total `ℂ → Fin k`, constrained only off `Z` | `NullSetRobust.lean:22` | so the witness `fun x => c (x + v)` is total — no partiality to repair |
| `measure_preimage_add_right`, `Metric.measure_ball_pos`, `Set.mem_biUnion`, `Set.biUnion_insert`, `Finset.coe_insert`, `Set.eq_univ_of_forall`, `add_sub_add_right_eq_sub` | used unqualified in `NullSetRobust.lean` under the same `open MeasureTheory` | same names, same `open`s, same pinned mathlib `d13f23b` |
| imports | `import OAI.Geometry.PlaneColoring.Converse` only | `Five` is imported only by `CyclicCore`, `Chromatic`, `NullSetRobust`, none of which is in the `Converse → States → BinaryPalettes → … → Coloring → Mathlib` chain, so this module does not reach `Five` |

**Residual risk, stated honestly:** this is a transcription, not a verification. The plausible failure
points are (i) elaboration of the `⋃ x ∈ (F : Set ℂ), …` binder under a fresh file's section variables,
and (ii) mathlib deprecations that could rename `Set.mem_biUnion`. Neither can be settled without a
build. The file ends with

    #print axioms OAI.EuclideanFiveColor.exists_properColoring_of_compl_null

so a local check reports the axiom set in one line.

## 2b. The minimal local-check packet (preferred vehicle for checking)

File: `check_null_transfer.lean`, sha256
`682c2c0acfbca85a94e05d3f3e93f766c656b8c0c77b5f7f5fc288f359b0994d`. 142 lines, **0 `sorry`, 0
`admit`, 0 elisions in either proof body**, one import, two `#print axioms` commands.

**Why it exists.** `k_generic_transfer.lean` (§2) imports `Converse`, which drags in 17 OAI modules;
its check is queued behind the frozen tree's dependency build. But the *only* in-tree ingredient the
transfer lemma needs is the finite-compactness step. So this packet extracts that step and drops
everything else:

* **Import:** `OAI.Geometry.PlaneColoring.Coloring` only. That module is a leaf — its sole import is
  `Mathlib`, and it supplies the exact in-tree predicate `OAI.EuclideanFiveColor.ProperColoring`
  (`Coloring.lean:7`: `∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y`). So the check needs Mathlib plus one leaf
  module, and none of the 17-module weak-colouring machinery.
* **Extracted lemma 1** `NullTransferCheck.exists_properColoring_of_finset`: the finite-compactness /
  de Bruijn–Erdős step, statement identical to `Converse.lean:33`, proof a verbatim transcription.
  Verified mechanically: after the `:= by` the proof text is **byte-identical** to the source
  (`difflib` over the two bodies reports no difference at all).
* **Extracted lemma 2** `NullTransferCheck.null_transfer`: the k-generic null-set transfer. Its inner
  `hfin` block is the one from `NullSetRobust.lean:20` with `Fin 5 → Fin k`; a mechanical diff shows
  the only textual differences are two deliberate renamings to avoid variable capture (`intro h` →
  `intro hh`, `by_contra h` → `by_contra hcontra`) plus consistent indentation.
* **Private namespace** `NullTransferCheck`, so nothing collides with `OAI.EuclideanFiveColor`. Both
  conclusions are stated in terms of the **in-tree** predicate (written qualified as
  `OAI.EuclideanFiveColor.ProperColoring`), so the correspondence is definitional rather than
  something to argue about.
* **Assumptions preserved in full:** `[NeZero k]`, `volume Z = 0`, `c` arbitrary (`ℂ → Fin k`, no
  measurability, no regularity), constrained only on pairs avoiding `Z`. The conclusion is existence
  of *some* plane colouring — **not** an extension of `c` off `Z`.
* **Not imported, not reproved:** `Five`, `no_proper_five_coloring`, and anything from the weak-colouring
  chain. The packet re-checks the compactness step from a copy, so it is a check of a genuine generic
  fact, not a new theorem claim.

Expected output when built:

    'NullTransferCheck.exists_properColoring_of_finset' depends on axioms: [propext, Classical.choice, Quot.sound]
    'NullTransferCheck.null_transfer'                   depends on axioms: [propext, Classical.choice, Quot.sound]

(the axiom *list* is what the build will report; the names above are the expected ones, not something I
have observed).

## 3. What this is and is not

* **Mathematical proof** (mine, this and the previous block): the transfer lemma and its
  hypothesis analysis, with the four corrections recorded in `NULL-TRANSFER.md`.
* **Existing compiled theorem** (not built by me): `exists_properColoring_of_finset` and
  `finite_config_proper` in `Converse.lean`; `not_proper_five_coloring_compl_null` in
  `NullSetRobust.lean`; `finite_density_realization` in `States.lean`. These are reported as present in
  the tree and as passing in `results/VERIFICATION.md`'s build log; I read them, I did not compile them,
  and I make no independent axiom claim.
* **Newly written, uncompiled source**: `k_generic_transfer.lean`. The proof body is **complete** (no
  elisions), mechanically transcribed from the source, but it has **never been elaborated**. It is not
  an existing compiled theorem and must not be cited as one until a build reports success.

## 4. Next step if a local serial build is authorised

Check `check_null_transfer.lean` first (§2b): it needs `Mathlib` plus the leaf module
`OAI.Geometry.PlaneColoring.Coloring`, so it does not wait on the 17-module `Converse` queue. Build it
in the serial local-check workflow under the pinned toolchain and read the two `#print axioms` lines.
`k_generic_transfer.lean` (§2) is then redundant as a *checking* vehicle and is kept only as the
version that proves the in-tree lemma through the in-tree one; check it if the queue ever allows.

If `check_null_transfer.lean` fails, the likely causes, in order: (i) `Pi.compactSpace` /
`isClosed_discrete` / `inter_iInter_nonempty` name drift in the installed Mathlib; (ii) `Set.mem_biUnion`
deprecated in favour of a `mem_iUnion₂` spelling; (iii) the `⋃ x ∈ (F : Set ℂ), …` binder's elaboration
in a file with fresh section variables. All three are mechanical renames.
