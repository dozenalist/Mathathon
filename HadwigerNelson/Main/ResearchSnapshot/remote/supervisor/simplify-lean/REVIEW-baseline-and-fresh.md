# Baseline packet verification + SignatureCheckFresh blind spots (block 14)

Source-only. No Lean, no compute beyond text comparison. Grades [C] computed here, [R] read,
[U] uncompiled.

## 1. [C] The two baseline definitions ARE the originals, character for character

Extracted the definition text of the pre-patch `FiniteEncodingApproximationAt`
(`lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean:266–280`) and `AmbientEncodingAt`
(`lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean:369–382`) from the frozen shared tree,
and the `Baseline…` copies from `SignatureEquivalence.lean`, then compared after whitespace
normalisation and renaming:

```
FINITE  identical after renaming: True
AMBIENT identical after renaming: True
```

No diff output was produced for either, so the ∃-shapes, binder names (`y` for the boundedness
conjunct in both), the `Integrable`/`∫` conjuncts, the `H i (p x)` / `H i x` arguments and the
`< γ^2` tail all match. The `variable` block in `SignatureEquivalence.lean` also reproduces the
original's ten-binder block (`{X Y W : Type*}` plus nine instances) with no addition.

**What this does not settle:** textual identity is not definitional identity in the *environment*
— the baseline lives in `OAI.SignatureCheck`, the original in `OAI.PlaneFiveColor.Spectral`, so their
`#check` output differs in the prefix. The `Iff.rfl` certificates are what upgrade text to defeq, and
those are [U] until compiled.

## 2. Blind spots in `SignatureCheckFresh.lean` — the honest list

The supervisor's point is right and I am narrowing my claim accordingly.

| # | blind spot | consequence |
|---|---|---|
| B1 | It is an **application-compatibility** test, not **binder equality**. | It proves the theorem is *usable* from a context supplying only our arguments. It does not prove the converse — that no extra binder exists. |
| B2 | An extra instance binder is invisible **if it is synthesizable**. | That is exactly why `sbY`/`neY` are plain: no instance entry exists for them. But see B3. |
| B3 | `Nonempty Y` in particular **may become derivable**. | If the file later gains `[Inhabited Y]`, `Nonempty Y` follows by instance; if it gains `[PolishSpace Y] [BorelSpace Y]`, `StandardBorelSpace Y` follows. Today neither is present, so the test is sound *as written* — but it degrades silently under a future edit. **Guard: the file must keep `set_option autoImplicit false` and must never gain a `[...]` binder or `letI` for a Y-instance outside the `control_*` theorems.** |
| B4 | A **dropped** binder is invisible. | Passing fewer arguments still succeeds. Not a risk here (`omit` already dropped the two), but it means the test cannot certify "exactly these binders". |
| B5 | Binder **position** changes are invisible. | Same cause. |
| B6 | The predicate **definitions** are not tested by it at all. | `SignatureEquivalence`'s `Iff.rfl` covers those; `SignatureCheckFresh` covers only the theorems. |
| B7 | A missing name in a failed elaboration yields no output rather than a diagnosis. | Mitigated in the new instrument: `BinderAudit.lean` prints `MISSING <name>` instead of erroring out. |

**Revised claim.** `SignatureCheckFresh` establishes: *each theorem applies, with no instance for
`StandardBorelSpace Y` or `Nonempty Y` available as an instance, at the original explicit binders.*
It does **not** establish binder equality. That now requires §3.

## 3. The instrument that does establish binder equality

Three parts, none of which assumes a successful build of anything else:

* **`lean/BinderAudit.lean`** — reads each constant's type from the *environment* and walks the forall
  telescope with `forallTelescopeReducing`, printing `BINDER <decl> <i> <name> <info> <type>` with
  `info ∈ {explicit, implicit, strict, instance}`. A missing constant prints `MISSING <name>`. It
  elaborates no *use* of the declaration, so partial failure still yields partial evidence, and the
  Lean side deliberately contains no expectation — the expected signature is not encoded where it is
  being tested.
* **`binder_expected.json`** — the expected signature, derived by reading the frozen originals. Its
  load-bearing content is negative: `forbidden_instance_types = ["StandardBorelSpace Y","Nonempty Y"]`,
  plus `required_instance_types = ["MeasurableSpace Y"]` and the exact 20-name explicit order.
* **`binder_snapshot.py`** — parses the capture, prints **every retained binder** (so the reader sees
  the full list, not just a verdict), tags forbidden ones inline, and returns pass / fail /
  inconclusive. A declaration absent from the capture is **inconclusive, never a pass**.

Verified on synthetic captures in this block:
* a faithful 31-binder capture of the finite theorem → `pass=1`, with `MeasurableSpace Y` retained and
  no forbidden binder;
* a capture carrying `StandardBorelSpace Y` and `Nonempty Y` → `FAIL: forbidden binder …` with both
  binders flagged inline, exit 1;
* an absent declaration → `INCONCLUSIVE`, exit 2, never counted as a pass.

This pairs with, and does not duplicate, `SignatureCheckFresh`: the application test says the theorem
is *usable*; the binder audit says what its type *is*. Binder equality needs the second.

## 4. Top-level statement audit — preserved, unchanged

`STATEMENT-AUDIT.md` stands as written. Summary of what it fixes:

* the certified root is `OAI.EuclideanFiveColor.no_proper_five_coloring :
  ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c`, with `ProperColoring k c := ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y`;
* the vertex domain is the whole plane, the edge predicate is distance exactly 1, the colouring is
  total and arbitrary, and **no measurability, choice or conditional hypothesis appears in the claim**;
* measurability, the algebraic plane and the tower machinery are proof-side only;
* `Problem160.ProperColoring` is *proven* equivalent by `planeProperColoring_iff`;
* `chromaticNumber_bounds : 6 ≤ χ ∧ χ ≤ 7`.

## 5. Scope correction: verifying the supplied proof does not create a new plane bound

Worth stating plainly, because the project's habit of measuring verification work in "results" invites
the opposite impression. Certifying the OpenAI argument — including every axiom print in
`AxiomRoots.lean` — establishes at most that the formalised statement

> there is no proper 5-colouring of the Euclidean plane

is true in the development, i.e. `χ(ℝ²) ≥ 6`, together with the already-present `χ(ℝ²) ≤ 7`.

It does **not** produce a new bound. Concretely: no 6-colouring of the plane is constructed, no
7-chromatic finite unit-distance graph is exhibited, and `planeChromaticNumber` is not determined. The
mathematical state after all our checks passes is the same as before them —
`6 ≤ χ(ℝ²) ≤ 7`, with `χ(ℝ²) ∈ {6,7}` open. The encoding-core reduction changes the length of a proof,
not the mathematics; the signature packets change what we can *claim*, not what is true. Any summary
that reports a "new bound" or a "bound improvement" from this workstream is wrong.

## 6. Status of each artefact

| artefact | status |
|---|---|
| baseline definitions ≡ originals (text) | **[C] verified** |
| baseline definitions ≡ new aliases (defeq) | **[U]** — `Iff.rfl`, uncompiled |
| `SignatureCheckFresh` application test | **[U]** — designed; blind spots B1–B7 documented |
| binder audit instrument | **[U]** — parser validated on synthetic captures; Lean side uncompiled |
| 82-module closure | **[S]** supervisor-reported pass |
| 9 exported root axioms | **[S]** supervisor-reported pass |
| top-level claim | **not locally verified here** |

## 7. Limitations

* `BinderAudit.lean` is unverified Lean. `forallTelescopeReducing` inside `liftTermElabM` in a
  `run_cmd` block, and `ppExpr` on a `LocalDecl` type, are the two places a build would most likely
  need a small fix; the failure would be a compile error in a 60-line file, not a wrong result.
* The expected explicit orders in `binder_expected.json` are read off the *sources*. If Lean reorders
  auto-bound implicit arguments relative to the source, the `explicit_order` check still holds (it
  filters by `binderInfo`), but the printed positions will differ from the source order.
* `binder_snapshot.py` matches a declaration by full name or by its last component; a capture from a
  differently-namespaced copy would be reported inconclusive rather than silently matched.
