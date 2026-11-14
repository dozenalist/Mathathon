# Dependency ledger: the generic null-transfer / compactness upper bound

Source-only. No build, no compute beyond reading import lines. **Conclusion up front: the compactness
argument does not depend on the five-colour impossibility theorem, and there is no useful import
reduction available. No candidate packet is proposed.**

## 1. The theorem, and what it is

`lean/OAI/Geometry/PlaneColoring/Converse.lean:33`

```lean
theorem exists_properColoring_of_finset {k : ℕ} [NeZero k]
    (h : ∀ F : Finset ℂ, ∃ c : ℂ → Fin k,
      ∀ x ∈ F, ∀ y ∈ F, ‖x - y‖ = 1 → c x ≠ c y) :
    ∃ c : ℂ → Fin k, ProperColoring k c
```

A Tychonoff compactness argument: the sets `t p = {c | c p.1 ≠ c p.2} ∪ {c | ¬ ‖p.1 - p.2‖ = 1}` are
closed in the compact `ℂ → Fin k`, have the finite intersection property by hypothesis `h`, so the
whole intersection is inhabited, and any point of it is a proper colouring. It is **direction-neutral**:
it manufactures a global colouring from finite data. Nothing about five colours enters — `k` is a
parameter.

## 2. Declaration-level ledger [C]

Every OAI-defined identifier each theorem's proof term mentions, with the module that defines it
(scan of the proof blocks; `F`, `apply`, `mono`, `closedBall` are local names or tactics and are not
dependencies):

| theorem | OAI dependencies | module |
|---|---|---|
| `exists_properColoring_of_finset` | `ProperColoring` | `PlaneColoring/Coloring.lean` |
| `finite_config_proper` | `DensityOne`, `finite_density_realization` | `PlaneColoring/States.lean` |
| `properColoring_of_weak` | `ProperColoring`, `WeakColoring` (+ the two theorems above) | `PlaneColoring/Coloring.lean` |

So the compactness theorem's entire OAI surface is **one definition** (`ProperColoring`, which is
`∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y`, `Coloring.lean:7`); everything else in its proof is Mathlib
(`Pi.compactSpace`, `isClosed_discrete`, `isCompact_univ`, `IsCompact.inter_iInter_nonempty`).

`Converse.lean` needs `States` for a *different* theorem (`finite_config_proper`, via `DensityOne` and
`finite_density_realization`), not for this one.

## 3. Module-level ledger [C]

| module | import closure | contains `Five`? | contains `BorelTransfer`? | contains `ConditionalSpectrum`? |
|---|---|---|---|---|
| `Converse` | **16** modules | **no** | **no** | **no** |
| `Coloring` | 0 (Mathlib only) | no | no | no |
| `States` | 15 | no | no | no |
| `Five` | 69 | — | yes | yes |

`Converse`'s closure does not reach `Five`, `BorelTransfer`, `ConditionalSpectrum` or `Approximation`.
The impossibility theorem is therefore not reachable from the compactness argument by any path.

## 4. Answer to the question asked

**Does the upper bound depend on the supplied five-colour impossibility?** No, on three independent
readings:

1. **Declaration**: `exists_properColoring_of_finset` uses one OAI name, `ProperColoring`.
2. **Module**: its file's 16-module closure excludes every module in the impossibility's cone.
3. **Logical**: the theorem *consumes* a finite-colouring hypothesis and *produces* a colouring; the
   impossibility consumes colourings. They compose in exactly one place,
   `NullSetRobust.lean:62` — `exact no_proper_five_coloring (exists_properColoring_of_finset hfin)` —
   which is the lower bound applied to the compactness lemma's output, not a dependence of one on the
   other.

The one hypothesis I checked for removability is `[NeZero k]`. It is load-bearing: the argument extracts
a point `⟨c, -, hc⟩` from `IsCompact.inter_iInter_nonempty` applied to `Set.univ`, which needs the type
`ℂ → Fin k` to be nonempty, i.e. `Fin k` nonempty. Not removable, and per instruction the assumptions
are left alone.

## 5. Why there is no useful reduction [C]

The obvious move — extract `exists_properColoring_of_finset` into a small module importing only
`Coloring` and have `Converse` import it — is a **re-layering, not a simplification**. Measured against
every actual consumer:

| consumer | what it needs from `Converse.lean` | saving if the split were made |
|---|---|---|
| `properColoring_of_weak` (same file) | all three theorems | 0 |
| `NullSetRobust.lean:62` | `exists_properColoring_of_finset` | **0** — see below |
| `Transfer.lean:20,30` | `properColoring_of_weak` | 0 |

`NullSetRobust` is the only external consumer, and it also imports `Five` (`NullSetRobust.lean:2`). Since
`States ∈ closure(Five)` and `closure(Five)` is 69 modules, dropping the `Converse` import in favour of a
small module would take `closure(NullSetRobust)` from 71 to 71: **the saving is exactly zero modules**,
and the split costs one new module plus a moved 40-line proof.

The reverse direction is worse: `Converse.lean` cannot shed its `States` import, because
`finite_config_proper` needs `DensityOne` and `finite_density_realization` from there.

So the honest answer to "can the imports be narrowed by extracting only the finite-graph compactness
interface" is: the *declaration's* interface is already minimal, and the *module's* cannot shrink. The
extraction would improve conceptual layering — an upper-bound lemma provable with no access to the
lower-bound machinery — and that is worth recording as a fact about the development, but it is a
reorganisation with a net cost, which is exactly the kind of cosmetic change the brief rules out.

## 6. Status

* **[C] verified by source reading and import-closure computation:** the ledger in §2 and the closure
  numbers in §3 and §5.
* **[S] reported, not re-run:** the supervisor's local `KGenericTransfer.lean` run (generic theorem,
  nonzero `k`, `nullZ`, proper unit pairs outside `Z` ⇒ some global proper `k`-colouring, **no agreement
  guarantee**). I could not locate `KGenericTransfer.lean` anywhere in this repository, so my review is
  against the in-tree `Converse.lean` source, and I make no claim about the supervisor's file.
* **[C] conclusion:** no useful reduction; no candidate packet delivered, by design.
* Unchanged: `6 ≤ χ(ℝ²) ≤ 7`; nothing here creates a new plane bound. Exact binder identity remains
  supplementary and is not touched by this block.

## 7. Limitations

* The declaration-level ledger is a name scan of the proof blocks, not an elaboration trace. It is
  reliable for "which OAI constants appear", and it would miss a dependency reached only through an
  instance whose name is generated — for `ProperColoring` (a plain `∀`-definition with no instance
  arguments) there is no such route, but the caveat is stated rather than glossed.
* Closure counts come from `^import` lines in `lean/OAI` as of this block.
