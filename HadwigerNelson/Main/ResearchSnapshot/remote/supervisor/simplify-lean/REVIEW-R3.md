# R3 review + minimal build closure (block 11)

Object: the **R3** revision of the integration, reviewed from the R2 bytes I hold plus the three
described syntax changes. **The R3 files are not present on this VM** — the architect directory still
contains R2 (`ConditionalSpectrum` `48aa378f…`, `ConditionalLimits` `58707f04…`), and a search for
either R3 hash finds nothing. So:

* R3 hashes `d26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48` (Spectrum, **PASSED
  locally** per the supervisor) and `fed6e99a17a7723240f9b598b1967183b41c5800d23d789e41e020cfe3dffedf`
  (Limits, **pending locally**) are recorded as *reported*, grade **[S] supervisor-reported**, not
  independently verified here.
* Everything below about the three changes is a check that the *diagnosis* is correct and complete
  against the R2 text, plus a statement of what a pass does and does not establish.

## 1. [C] Both R2 failures reproduce as described

**Failure 1 — `omit` after a doc comment.** Frozen R2, `ConditionalSpectrum.lean:322–325`:

```
/-- Both uniform-precision contradictions are this statement at `S := p, P := q ∘ p` and
… -/
omit [StandardBorelSpace Y] [Nonempty Y] in
theorem uniform_precision_contradiction
```

The `/-- … -/` is a **doc** comment (attachment syntax), so the parser is committed to a declaration
at that point and rejects the `omit` modifier that follows. The reported fix — move `omit` above the
comment — is the standard ordering and is the minimal edit. Note the *other two* `omit … in` in the
same file (lines 492, 511) are followed directly by `theorem` and are unaffected, which matches
"exactly 3 syntax changes" (one `omit` move + two `exact`s).

Robustness remark, not a demand: because R3 passes locally, no action is needed; but had the block
used a plain `/- … -/` comment instead of `/-- … -/`, the adjacency would never have been fragile.
Worth remembering for the next insertion.

**Failure 2 — bare term inside a `by` block.** Frozen R2, `ConditionalSpectrum.lean:508–509`:

```
    (happrox : FiniteEncodingApproximationAt … ) : False := by
  uniform_precision_contradiction μ p (fun x => q (p x)) (Z := Y) p b
```

and `ConditionalLimits.lean:389–390` identically with the ambient wrapper. A term application is not
a tactic, so `by` rejects it; prefixing `exact` is the fix. Both sites confirmed; no third site exists
(`finite_uniform_successor_contradiction` is the untouched original body).

**Assessment:** the three changes are correctly diagnosed, are syntax-only in intent, and nothing in
them touches a statement, a hypothesis or a proof step. What a pass proves: the file **elaborates** at
its real types. What it does **not** prove: that the printed signatures are unchanged — `omit`
placement controls *which instance binders appear* in the declaration, so the `omit` move is exactly
the kind of edit that can silently alter a public signature while compiling. That is why
`AxiomRoots.lean` §A4 now demands a full `pp.explicit`/`pp.universes` `#check` diff against the
pre-patch build. Grade for that item: **open**.

## 2. [C] Minimal build closure — and the number that matters is 82

Computed from `MANIFEST-full.json` (set algebra over the stored import graph; no new scan).
`BUILD-PLAN.json` carries the per-module rows.

| quantity | value |
|---|---|
| edited modules | 2 |
| **descendants-only** (reverse-dependent) | **19** |
| **union with edits** | **21** |
| **complete ancestor closure, from scratch** | **82** |
| unaffected | **1** |

**The 19 are not import-closed.** Building just them dangles on 10 direct imports, including
`ConditionalSpectrum` itself, `Selections`, `Geometry.PlaneColoring.Basic/Coloring/Converse/Mesh`.
So "19" answers *what can be affected*, never *what must be built*; the two questions differ by 61
modules.

**The single unaffected module is `OAI.Geometry.PlaneColoring.ConnectedUnitFree`** (build order 80) —
it neither reaches the edits nor is reached by them (consistent with its known status as a
machine-checked lemma with no consumer in the tree). Everything else in the tree must be present to
compile the affected modules from scratch.

**A diamond worth naming**, because it explains the smoke closure: `ConditionalLimits` imports
`Approximation`, which imports `ConditionalSpectrum`. So `Approximation` is simultaneously a
**descendant** of the Spectrum edit and an **ancestor** of the Limits edit. The two edits are not
comparable, and the 14-module smoke closure already contains the deep consumer.

### Reuse accounting: 12, not 9

The supervisor reports **nine** unchanged dependencies compiled locally. The manifest gives **twelve**
non-edit ancestors in the 14-module smoke closure:

`Basic`(1), `Characters`(2), `InvariantMean`(9), `Multipliers`(10), `FourierTests`(11),
`SmallArcs`(12), `PhaseEncoding`(13), `PhaseCollision`(14), `ConditionalSelection`(15),
`Centers`(18), `RelativeCenters`(19), `Approximation`(20).

I cannot reconcile nine with twelve from the record. Two readings are compatible with the numbers:
nine were *compiled* and three were *reused* from a warm olean cache, or the private build rooted at a
different module set. `BUILD-PLAN.json` flags all twelve with `reused_candidate: true`; the operator
should mark which nine, rather than have me guess. Flagged, not resolved.

## 3. [C] What the affected set reaches, and what it does not

* `OAI.EuclideanFiveColor.no_proper_five_coloring` (`Five.lean:133`, order 72) — **descendant**,
  inside the affected set. Must be re-certified.
* `OAI.Problem160.properColoring_seven` / `weakMeasurableColoring_seven` (`Seven.lean:36,60`, order 78)
  — **not** descendants. They are, however, *ancestors* of `Chromatic`(79), which is a descendant, so
  `Seven` is needed in a from-scratch build while being unaffected by the edit. Both facts are true and
  must not be merged: **needed-to-build ≠ affected**. That is why the axiom file puts the upper-bound
  roots in Part B.

## 4. Axiom policy and the axiom-root file

Acceptance is **subset** of `{propext, Classical.choice, Quot.sound}`; subsets are normal.

`lean/AxiomRoots.lean` is now split:

* **Part A (required, affected):** the common core, the two rewritten wrappers, the three named
  consumers, and `no_proper_five_coloring` — 7 roots. Plus §A4's statement-preservation `#check`s.
* **Part B (optional, unaffected):** `properColoring_seven`, `weakMeasurableColoring_seven` — printed
  in a separate section so an unaffected result cannot inflate the dependency claim.

`axiom_gate.py` was updated to match: a missing Part A root is a failure (the file did not
elaborate), a missing Part B root is informational only. Re-verified on synthetic input: a 1-element
set `[propext]` PASSes, a wrapped 3-element set PASSes, an absent Part B root prints
`absent (optional, unaffected)`, and `[propext, sorryAx]` FAILs with
`sorryAx present -- transplanted body not substituted`.

## 5. Status of the review chain

| item | evidence | status |
|---|---|---|
| R2 → R3 diff is exactly 3 syntax changes | described + reproduced against R2 bytes | **[C] accepted as diagnosis** |
| R3Spectrum elaborates | supervisor's local run | **[S] reported PASSED, not verified here** |
| R3Limits elaborates | — | **pending** |
| public statements unchanged | not yet checked | **open** — §A4 decides it |
| axioms within the standard set | not yet run | **open** — gate ready |
| 83-module downstream elaboration | not yet run | **open** |

## 6. Limitations

* The R3 bytes are absent from this VM; I reviewed the described diff, not the files. My conclusion is
  about the *diagnosis*, which I could test, not about the R3 hashes.
* Counts come from the stored manifest, i.e. from `lean/OAI` as of 05:00Z today; if the shared tree has
  changed since, the closure must be recomputed (cheap; the script is in `.scratch/`).
* "Complete ancestor closure = 82" assumes every module in it is needed as an *olean*; with a warm
  cache only the 2 edited modules and the 19 descendants actually re-elaborate. The 61 ancestor-only
  modules are the from-scratch requirement the brief asked for.
