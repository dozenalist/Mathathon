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

## 7. Narrow smoke roots, built in ONE cohesive private OAI tree

The local diagnostic established the operational rule: **do not** let the build see an `OAI` root that
is only partially populated, and do not expect a per-file fallback into another `LEAN_PATH` entry once
an `OAI` root has been found. A private R3 tree with 9 of the 14 closure oleans produced a
missing-olean error even though the same modules existed elsewhere; the fix was to put the whole
closure into that one root. The recipe therefore uses exactly one source tree and one output root.

```bash
cd <repo>
source scripts/env4341.sh          # Lean 4.34.1 + pinned Mathlib paths ONLY
# deliberately NOT lean/build/lib: stale original OAI oleans must be unreachable
EC=supervisor/simplify-architecture/encoding-core
PRIV=$EC/private-r3
rm -rf "$PRIV"; mkdir -p "$PRIV/src" "$PRIV/lib"

# 1. one cohesive SOURCE tree: the frozen 14-module closure, with the two patched modules in place
cp -r lean/OAI "$PRIV/src/OAI"
cp $EC/integration/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean  "$PRIV/src/OAI/Analysis/PlaneSpectrum/"
cp $EC/integration/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean "$PRIV/src/OAI/MeasureTheory/CompactFactors/"

# 2. one OUTPUT root, topological order (scripts/build_lean.py has the same logic; ROOT is private)
cd "$PRIV/src"
python3 - "$PRIV" <<'L'
import pathlib, re, subprocess, sys, os
priv = pathlib.Path(sys.argv[1]); root = priv / "src"
mods = {}
for p in sorted(root.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(root).with_suffix("").parts)
    mods[name] = (p, re.findall(r"^import\s+(OAI\.[\w.]+)\s*$", p.read_text(errors="ignore"), re.M))
order, seen = [], set()
def go(m):
    if m in seen: return
    seen.add(m)
    for d in mods[m][1]: go(d)
    order.append(m)
for m in mods: go(m)
env = dict(os.environ, LEAN_PATH=str(priv / "lib"))
for m in order:
    out = priv / "lib" / (m.replace(".", "/") + ".olean"); out.parent.mkdir(parents=True, exist_ok=True)
    p, _ = mods[m]
    r = subprocess.run(["lean", "-o", str(out), str(p)], env=env, capture_output=True, text=True)
    print(("OK   " if r.returncode == 0 else "FAIL ") + m)
    if r.returncode: print(r.stdout, r.stderr); raise SystemExit(1)
L

# 3. smoke roots, against that same single root
LEAN_PATH="$PRIV/lib" lean $EC/integration/SmokeFinite.lean
LEAN_PATH="$PRIV/lib" lean $EC/integration/SmokeAmbient.lean
```

Expected: every module `OK`; both smoke roots clean; every `#print axioms` line
`[propext, Classical.choice, Quot.sound]`. Three invariants the recipe enforces: one source tree, one
output root, no shared `lean/build/lib` on `LEAN_PATH`.

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

## 10. Regenerated artefacts and hashes (R4 revision)

| artefact | sha256 |
|---|---|
| `0001-conditional-spectrum.patch` | `a631dc3c0e49a1b4154f405c2d9b62394a96b82c3dec0e8c36ea465bb0437af1` |
| `0002-conditional-limits.patch` | `eab14daa47ba1b0df329690da10b527ef04b7e8e233d37441fbd123253efaad4` |
| patched `ConditionalSpectrum.lean` | `d26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48` |
| patched `ConditionalLimits.lean` | `24f89dd33533a0f61b9f35940e43b3a26c2b27b00424949a92cfdafc8de60d9b` |

Apply check re-run on frozen copies: `rc = [0, 0]`.
Measured net line change: `ConditionalSpectrum +33`, `ConditionalLimits -159`, **total -126**
(textual only). Statement delta: both public statements **identical** (`2dde28358ab09934`, `ab6dd548d3a6bb53`).

## 11. Source freeze for the local run

`SOURCE-FREEZE.md` lists, with sha256: the two post-patch files (the revision the build must
reproduce), the two input originals, and the **root-closed 14-module OAI closure** plus the Mathlib
import roots and the pinned toolchain. Local compilation should target exactly that revision: after
applying the two patches, `sha256sum` of the two edited modules must equal the values recorded there;
anything else is a different revision than the one reviewed.

## 12. R3 syntax fixes (adopted verbatim) and hash confirmation

The local diagnostic found two syntax (not mathematical) defects in the block-9 revision, and the
supervisor produced a private R3 copy with exactly three edits. All three are now in the generator, and
regenerating reproduces the R3 copy **byte for byte**:

| # | edit | where |
|---|---|---|
| 1 | `omit [StandardBorelSpace Y] [Nonempty Y] in` moved **above** the `/-- Both uniform-precision … -/` doc comment | patched `ConditionalSpectrum`, `omit` now at 321, doc comment 322-324, `theorem` at 325 |
| 2 | `exact` added before `uniform_precision_contradiction` | finite wrapper body, line 508 |
| 3 | `exact` added before that call | ambient wrapper body, line 390 |

Why (2) and (3) were needed: the transplanted statement ends `:= by`, so the body is a *tactic* block
and a bare term is not a tactic — `exact` supplies the tactic. Why (1) was needed: `omit … in` must
immediately govern the declaration, and a preceding doc comment is not part of that command.

**Hash confirmation** (my regeneration vs the supervisor's private R3 copy):

| file | regenerated sha256 | R3 sha256 | match |
|---|---|---|---|
| patched `ConditionalSpectrum.lean` | `d26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48` | `d26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48` | **yes** |
| patched `ConditionalLimits.lean` | `fed6e99a17a7723240f9b598b1967183b41c5800d23d789e41e020cfe3dffedf` | `fed6e99a17a7723240f9b598b1967183b41c5800d23d789e41e020cfe3dffedf` | **yes** |

Nothing else was changed: statement delta still empty, net still `-126`, apply check `rc = [0, 0]`.
`SOURCE-FREEZE.md` now records the R3 hashes as the post-patch values, so the build target and the
reviewed copy are the same revision.

## 13. R4: one downstream line, caused by the alias, and its hash confirmation

The immediate 14-module local build (R3) surfaced a single further failure, not in either wrapper
theorem but in the **conversion lemma** `CompactApproximation.At → AmbientEncodingAt`
(`ConditionalLimits`, patched line 457). Its closing term was

```lean
by rw [← integral_congr_ae he]; exact hae
```

and it failed to unify because the alias phrases that lemma's goal with `Hf i (id x)` rather than
`Hf i x` — i.e. the `id` of `S := id` is now *visible in the goal* at every site the alias reaches.
R4 replaces **that proof term only** with

```lean
by simpa only [id_eq] using ((integral_congr_ae he) ▸ hae)
```

which transports the same integral equality and beta/id-normalises. No hypothesis, statement or
binder is touched.

**Hash confirmation** (regenerated vs R4):

| file | regenerated sha256 | R4 sha256 | match |
|---|---|---|---|
| patched `ConditionalSpectrum.lean` | `d26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48` | `d26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48` | **yes (unchanged)** |
| patched `ConditionalLimits.lean` | `24f89dd33533a0f61b9f35940e43b3a26c2b27b00424949a92cfdafc8de60d9b` | `24f89dd33533a0f61b9f35940e43b3a26c2b27b00424949a92cfdafc8de60d9b` | **yes** |

The line is a genuine, minimal cost of the merge and belongs in the referee's ledger: the abstraction
is not literally free downstream — it costs **one** `simpa only [id_eq]` in the conversion lemma,
because `abbrev` makes `S := id` visible where the old `def` kept it under a name. Net line change is
unchanged at `-126` (one line replaced by one line).
