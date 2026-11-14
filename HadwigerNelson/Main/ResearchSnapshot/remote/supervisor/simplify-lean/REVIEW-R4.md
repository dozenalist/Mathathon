# R4 review (block 12)

Independent source review. No build, no cloud operation. Grades: [C] computed here, [R] read,
[S] supervisor-reported.

## 1. [C] R3 is now present, and my block-11 absence report was a timing artifact — confirmed

The architect directory now holds exactly the R3 hashes:

| file | sha256 on disk | expected |
|---|---|---|
| `ConditionalSpectrum.lean` | `d26d569088faea89e5ae5cc2309809797fcbe76cf6d927f4484bc39db7880d48` | match |
| `ConditionalLimits.lean` | `fed6e99a17a7723240f9b598b1967183b41c5800d23d789e41e020cfe3dffedf` | match (the block-11 "pending" hash) |

Frozen at `supervisor/simplify-lean/snapshots/integ-d26d569088faea89/` with `SHA256SUMS.txt`.
Block 11's "R3 bytes absent" was correct at the time of the search and is superseded; nothing in that
review depended on the bytes, since it tested the *diagnosis* against R2.

## 2. [C] R4 reconstructed byte-identically from R3 + the one-line change

Applied exactly one substitution to the frozen R3 `ConditionalLimits.lean`:

```
- by rw [← integral_congr_ae he]; exact hae
+ by simpa only [id_eq] using ((integral_congr_ae he) ▸ hae)
```

in `recon/ConditionalLimits.R4-recon.lean`:

* the old text occurs **exactly once** in the file (asserted before substituting, so no silent
  multi-site edit);
* the result hashes to **`24f89dd33533a0f61b9f35940e43b3a26c2b27b00424949a92cfdafc8de60d9b`**, the
  supplied R4 hash, **exactly**.

That is a stronger statement than "the diff looks like what was described": it proves R4 differs
from R3 in that one line and in nothing else, byte for byte, without needing the architect's copy.
Spectrum is unchanged between R3 and R4 (same hash supplied for both).

### Where that line sits, and why it is proof-only

Frozen R3 `ConditionalLimits.lean:457`, inside an anonymous constructor:

```lean
  exact ⟨a, hab, hai.congr he, by rw [← integral_congr_ae he]; exact hae⟩
```

It is the **fourth component of a 4-tuple** — a proof term in an `exact`, in the middle of a proof.
No statement, binder, hypothesis or definition is touched. The substitution changes a `rw`-then-`exact`
into a single `simpa … using (… ▸ …)`; the `▸` transports `hae` along `integral_congr_ae he`, which is
what the `rw [← …]` was trying to do. Semantically the same obligation discharged by a term that
elaborates where the tactic did not.

## 3. [C] Correction to my block-11 wording: the two edited modules ARE comparable

Block 11 said "the two edits are not comparable". **That was wrong.** `ConditionalSpectrum` is an
**ancestor** of `ConditionalLimits`: `ConditionalLimits` imports `Approximation`, which imports
`ConditionalSpectrum`. So in dependency order

```
ConditionalSpectrum  →  …  →  Approximation  →  …  →  ConditionalLimits
```

and the pair is totally ordered. What is true, and is what I actually observed, is that
`Approximation` is *simultaneously* a descendant of the first edit and an ancestor of the second —
a diamond consistent with comparability, not an obstruction to it. Consequence for the build:
the edit to `Limits` can never affect `Spectrum`, so a single build order suffices and there is no
need for a fixed-point or two-pass rebuild.

## 4. [C] Reuse accounting: resolved

Block 11 flagged that the supervisor's "nine unchanged dependencies" did not match the manifest's
twelve non-edit ancestors. The explanation given (nine was the initial snapshot; all fourteen
immediate modules are now compiled) is consistent with the manifest, and the twelve-ancestor count in
`BUILD-PLAN.json` is correct. **No disagreement remains**; `reused_candidate` stays a truthful
description of the twelve and the earlier flag can be closed.

## 5. [S] What the supervisor's local run establishes, stated precisely

Reported: the 14 immediate modules and both smoke roots PASSED; 4 distinct theorems show standard
axioms with no `sorryAx`; the 82-module build is running.

* The 14-module result is a genuine **type-checking** result over the immediate closure: the R3
  syntax fixes and the R4 proof-term change both elaborate at their real types.
* "4 distinct theorems standard axioms" is a **subset** statement only if the sets are subsets of
  `{propext, Classical.choice, Quot.sound}`; that is the acceptance rule and it is satisfied as
  reported. It does not tell us *which* four, so `AxiomRoots.lean` remains the instrument for the
  named Part A roots.
* A passing 82-module build will establish **downstream elaboration**. It will not by itself
  establish that the public statements are unchanged — see §6.

## 6. Signature preservation: the packet

`lean/SignatureEquivalence.lean` (195 lines) answers the one question a green build cannot:

1. **Baseline predicates.** The pre-patch `FiniteEncodingApproximationAt` (from
   `ConditionalSpectrum.lean:266–280`) and `AmbientEncodingAt` (from `ConditionalLimits.lean:369–382`)
   are copied **verbatim** under `SignatureCheck.Baseline…` names. No import of the pre-patch tree is
   needed — only the 14-module immediate closure R4 already compiles.
2. **Definitional equality.** `baseline_finite_iff` and `baseline_ambient_iff` are `Iff.rfl`. These
   fail unless the new aliases are *literally* the old predicates. This is the decisive test of
   `S := id`: if `H i (id x)` were not reducible to `H i x`, the ambient one fails.
3. **Public statement preservation.** The two ORIGINAL public statements are restated with their
   original binders — including the omitted `[StandardBorelSpace Y] [Nonempty Y]` — and **proved** by
   direct call to the R4 theorems. This shows no hypothesis was dropped or strengthened and that the
   old `happrox` type is accepted.
4. **Implicit-binder inspection.** `#check @…` under `pp.explicit`/`pp.universes` for textual diff
   against the pre-patch build.
5. **Axiom footprint** of the two baseline wrappers.

**Documented limitation (also inside the file).** Section 3 alone cannot detect an *added* implicit
binder, because it lives inside the module's `variable` block and such an argument would be filled
automatically. An added binder is caught only by the section-4 textual diff. Both checks are needed.

## 7. Status table

| claim | evidence | status |
|---|---|---|
| R3 hashes as supplied | [C] on-disk match | verified |
| R4 = R3 + exactly one line | [C] byte-identical reconstruction, hash match | **verified** |
| R4 change is proof-only | [R] it is the 4th component of a 4-tuple in an `exact` | verified by reading |
| Spectrum ancestor of Limits | [C] from the manifest import graph | verified; block-11 wording corrected |
| 14 modules + smoke roots typecheck | [S] | reported, not re-run |
| 4 theorems within standard axioms | [S] | reported; named roots still owed |
| 82-module downstream elaboration | [S] running | open |
| public statements unchanged | packet prepared | **open until run** |

## 8. Limitations

* No compilation in this block; every Lean claim is textual or reported.
* The R4 reconstruction is a *hash* verification, not a build: identical bytes, unproven elaboration.
* `SignatureEquivalence.lean` has not been elaborated, and one detail is genuinely uncertain without a
  build: whether `open PlaneFiveColor.Spectral` plus `open EuclideanFiveColor` resolves every name in
  the copied baselines (`eval`, `kCoeff`, `K`, `D`, `E`, `IsWild`, `DifferenceFourier`,
  `PhaseEncoding.kernelEncoding`). I checked the declaration sites (`eval` in
  `PlaneFiveColor.Spectral`, `kCoeff`/`K`/`D`/`E`/`IsWild` in Basic, `kernelEncoding` in PhaseEncoding)
  and opened both namespaces, but a build is the only confirmation.
