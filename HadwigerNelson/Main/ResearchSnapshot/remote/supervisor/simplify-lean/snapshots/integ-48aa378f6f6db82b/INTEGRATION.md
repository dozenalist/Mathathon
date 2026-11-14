# Integration patch: common encoding core into the two shared modules

**STATUS: UNCOMPILED.** No `lean`, `lake` or remote build was run in this block. Every quantitative
claim below is *textual* and measured by `../integrate.py`; the type-level claims are what the local
queue must confirm. The line saving is **not** verified until that run passes.

> **CORRECTION (block 9).** The block-8 insertion anchor for the common theorem was **invalid**: it
> placed `uniform_precision_contradiction` before `two_array_norm_bound` and `simultaneous_test_budget`,
> which its proof calls — a definite declaration-order error, found by the local source audit. The
> anchor is now *after both helpers and immediately before the finite wrapper*. §3 and §6 below are
> superseded by **§9**, which gives the corrected anchors, the mechanical declaration-order audit, and
> the measured counts. Patches, patched copies, `META.json` and hashes are regenerated; the smoke
> roots are unchanged in content. `INTEGRATION.md` §1–§8 otherwise stand.


## 1. Frozen inputs (integrate.py refuses to run if either hash moves)

| file | sha256 | lines |
|---|---|---|
| `lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` | `6602b9d8f20bbdfd447f2f3fcfa523f2c33d09c247e3d2983be7503df9f2dc9b` | 497 |
| `lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean` | `ca74ba1033fead55133670218739a36b4c75173d9b04d765affd19da9d215cc0` | 701 |

Patch hashes: `0001…patch` `d9b56eac3d65…`, `0002…patch` `64b657d3159a…` (full digests in
`META.json`, together with the patched-copy and smoke-root digests). Apply check: `patch -p1
--dry-run` on frozen copies returns **rc 0** for both (`APPLY-CHECK.txt`).

## 2. Apply order

```bash
cd <repo>
patch -p1 < supervisor/simplify-architecture/encoding-core/integration/0001-conditional-spectrum.patch
patch -p1 < supervisor/simplify-architecture/encoding-core/integration/0002-conditional-limits.patch
```

The order is not load-bearing (different files); 0002 is listed second only because the ambient
theorem lives textually later in the build order. `integrate.py` regenerates both patches, and the
patched copies under `OAI/…` so a reviewer can read the result without applying anything.

## 3. What each patch does, by anchor

### 0001 `ConditionalSpectrum.lean` (+33 net: 191 added, 158 removed)

1. **Inserts** `def EncodingApproximationAt` and `theorem uniform_precision_contradiction` (with the
   full 151-line transplanted body) immediately **before** the old `def
   FiniteEncodingApproximationAt`. Insertion point is after the `variable {X Y W : Type*} …` block
   (old line 263) and hence also after the `local instance : MeasurableSpace Circle := borel Circle`
   / `local instance : BorelSpace Circle := ⟨rfl⟩` pair at old lines **260-261**, so `harc`'s
   `Measure Circle` and `ω.real` elaborate exactly as before. No instance is added.
2. **Replaces the body** of `def FiniteEncodingApproximationAt` by an `abbrev` alias
   (`EncodingApproximationAt μ p (fun x => q (p x)) p b m γ`). Same binders, same order, same
   explicitness (`μ`, `[IsProbabilityMeasure μ]`, `p`, `q`, `b`, `m`, `γ`) ⇒ every application in
   the tree elaborates untouched.
3. **Replaces the 153-line body** of `finite_uniform_precision_contradiction` by the two-line call
   `uniform_precision_contradiction μ p (fun x => q (p x)) (Z := Y) p b hp (hq.comp hp) hb m hm g hg
   hwild ρ c N hρ hc hN harc happrox`. The statement (old lines 308-323) is byte-identical.

### 0002 `ConditionalLimits.lean` (−159 net: 6 added, 165 removed)

1. **Replaces the body** of `def AmbientEncodingAt` by an `abbrev` alias to
   `EncodingApproximationAt μ p q id b m γ` — visible in that file because `ConditionalLimits`
   already imports `ConditionalSpectrum` (`no_import_added: true`).
2. **Replaces the 153-line body** of `ambient_uniform_precision_contradiction` by
   `uniform_precision_contradiction μ p q (Z := X) id b hp hq hb m hm g hg hwild ρ c N hρ hc hN harc
   happrox`. Note `hP := hq` was *already* the old proof's first line, so nothing is assumed that
   was not assumed before; the `IsProbabilityMeasure (μ.map P)` instance keeps the explicit
   `.map`-branch route taken from the finite proof.
   The `local instance … Circle` pair at old lines **363-364** precedes both edit sites (369, 385) —
   again no instance added.

## 4. Why this cannot prove a wrapper by importing itself

* Neither patch adds an import (`no_import_added: true` in `META.json`).
* The alias right-hand side is `EncodingApproximationAt`, a **definition**, not a theorem.
* The two theorem bodies call `uniform_precision_contradiction`, which exists exactly once, in
  `ConditionalSpectrum`, *above* both call sites, and is not named after either public theorem.
* `EncodingCore.lean` / `Wrappers.lean` from the previous block — including the review-only `_core`
  suffixed copies and the `Iff.rfl` certificates — are **not** part of the patch and import nothing
  from the tree that this patch touches. After integration they are redundant; the definitional
  equality they certified is now literal (the old name *is* the alias).
* `grep` over the patch bodies: zero occurrences of `sorry`, `admit`, `axiom`, `native_decide`.

## 5. Public statements and all downstream consumers retained

Statement delta (**must be empty**) — measured by re-extracting the statement text from original and
patched copy:

| public theorem | identical | statement sha (both) |
|---|---|---|
| `finite_uniform_precision_contradiction` | **yes** | `2dde28358ab09934…` |
| `ambient_uniform_precision_contradiction` | **yes** | `ab6dd548d3a6bb53…` |

The two *definitions* change kind (`def` → `abbrev`) with identical binders; the proposition is
unchanged by construction. This is the one place where `#check` output could look different to a
reviewer, and it is a display change, not a statement change.

Call sites that must keep elaborating (all positional, hence real signature checks):

| consumer | file:line | depends on |
|---|---|---|
| `finite_uniform_successor_contradiction` | `ConditionalSpectrum.lean:479` (patched 512) | the finite theorem |
| its caller | `MeasureTheory/CompactFactors/Approximation.lean:414` | the successor theorem |
| `… finite_uniform_precision_contradiction μ p (q n ∘ v n) …` | `ConditionalLimits.lean:322` | the finite theorem, **cross-module** |
| `… ambient_uniform_precision_contradiction …` | `ConditionalLimits.lean:660` | the ambient theorem |

A successful build of `ConditionalLimits` and `Approximation` type-checks all four, so it is the
strongest available statement-preservation test — stronger than any `#check` I could add.

## 6. Measured line change (textual, UNCOMPILED)

| module | before | after | net | removed | added |
|---|---|---|---|---|---|
| `ConditionalSpectrum.lean` | 497 | 530 | **+33** | 158 | 191 |
| `ConditionalLimits.lean` | 701 | 542 | **−159** | 165 | 6 |
| total | 1198 | 1072 | **−126** | | |

The earlier "~150 lines" projection is **superseded by this measurement: −126 net**, and neither
figure is verified until the local integration build and axiom run pass.

## 7. Narrow smoke roots

`SmokeFinite.lean` imports only `ConditionalSpectrum`; `SmokeAmbient.lean` imports only
`ConditionalLimits` (which pulls in `Approximation`, hence the deep consumer). Each prints
`#print axioms` and `#check @…` for the replacement theorem, the public root, and the consumer(s).

```bash
cd <repo>
source scripts/env4341.sh
python3 scripts/build_lean.py                      # oleans for lean/OAI/**
EC=supervisor/simplify-architecture/encoding-core/integration
lean $EC/SmokeFinite.lean
lean $EC/SmokeAmbient.lean
```

Expected: no errors; every `#print axioms` prints exactly `[propext, Classical.choice, Quot.sound]`.
`sorryAx` in any line means the transplanted body was not substituted.

## 8. What only the build can settle

1. That the inserted block elaborates at its anchor (name resolution for `FiniteBins`, `MomentTest`,
   `predecessor_moment_sq`, `IsWild`, `C`, `kCoeff`).
2. That both `abbrev` aliases are accepted where the old `def`s were, including inside `refine ⟨…⟩`
   at `ConditionalLimits:592` (existential arity preserved: `r, B, C, H` remain the four components).
3. That `EncodingApproximationAt μ p q id b m γ` elaborates with `S := id` (`H i (id x)` vs `H i x`).
4. That the four `change` lines and the `hbins` application re-elaborate at `S`.
5. That the axiom sets of both public theorems and of all three consumers stay
   `[propext, Classical.choice, Quot.sound]`.

## 9. CORRECTED ANCHORS (supersedes §3) and the declaration-order audit

Measured declaration order in the patched `ConditionalSpectrum.lean`:

| line | declaration | note |
|---|---|---|
| 273 | `def EncodingApproximationAt` | generic definition, inserted early: needs nothing from the helpers |
| 291 | `abbrev FiniteEncodingApproximationAt` | alias, right-hand side resolves upward |
| 295 | `def FiniteEncodingApproximation` | pre-existing, uses the alias above it |
| 299 | `lemma two_array_norm_bound` | pre-existing helper |
| 305 | `lemma simultaneous_test_budget` | pre-existing helper (ends 319) |
| **325** | **`theorem uniform_precision_contradiction`** | **after both helpers, before the wrapper** |
| 494 | `theorem finite_uniform_precision_contradiction` | public statement byte-identical, body = 2-line call |
| 512 | `theorem finite_uniform_successor_contradiction` | pre-existing consumer, untouched |

`integrate.py` now refuses to emit a patch unless, for every inserted block, every identifier the
block uses *in code* (comments and docstrings stripped) is declared earlier in the same file. Result
on the regenerated files:

* `ConditionalSpectrum`: anchors `{EncodingApproximationAt: 273, FiniteEncodingApproximationAt: 291,
  uniform_precision_contradiction: 325}`, **forward references: 0**.
* `ConditionalLimits`: anchor `{AmbientEncodingAt: 371}`, **forward references: 0**.

New identifiers introduced below the insertion points, checked for namespace/visibility:

| identifier | namespace | private? | used from the other module? |
|---|---|---|---|
| `EncodingApproximationAt` | `OAI.PlaneFiveColor.Spectral` | no | yes, by the ambient alias in `ConditionalLimits` |
| `uniform_precision_contradiction` | `OAI.PlaneFiveColor.Spectral` | no | yes, by the ambient wrapper (same namespace, imported) |
| `FiniteEncodingApproximationAt` (abbrev) | same | no | yes, downstream |
| `AmbientEncodingAt` (abbrev) | same | no | yes, its own module's conversion lemma at 592 |

No `private`, no `local` declaration is introduced; the only `local` items involved are the
pre-existing `MeasurableSpace`/`BorelSpace Circle` instances, which stay where they were.

## 10. Regenerated artefacts and hashes

| artefact | sha256 (first 16) |
|---|---|
| `0001-conditional-spectrum.patch` | `87236acd52ff0169` |
| `0002-conditional-limits.patch` | `64b657d3159ade37` |
| patched `ConditionalSpectrum.lean` | `48aa378f6f6db82b` |
| patched `ConditionalLimits.lean` | `58707f0495837a89` |

Apply check re-run on frozen copies: `rc = [0, 0]`.
Measured net line change: `ConditionalSpectrum +33`, `ConditionalLimits -159`, **total -126**
(textual only). Statement delta: both public statements **identical** (`2dde28358ab09934`, `ab6dd548d3a6bb53`).

## 11. Source freeze for the local run

`SOURCE-FREEZE.md` lists, with sha256: the two post-patch files (the revision the build must
reproduce), the two input originals, and the **root-closed 14-module OAI closure** plus the Mathlib
import roots and the pinned toolchain. Local compilation should target exactly that revision: after
applying the two patches, `sha256sum` of the two edited modules must equal the values recorded there;
anything else is a different revision than the one reviewed.
