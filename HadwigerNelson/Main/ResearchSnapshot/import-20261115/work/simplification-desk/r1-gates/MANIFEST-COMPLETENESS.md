# R1 (threecentre-r1) manifest completeness: PaletteTransport.lean

Simplification desk, 2026-11-15. Owned note; `lean-queue/threecentre-r1/frozen-manifest.json` is not edited.
This is the research-plan item 6 note.

## Finding: the exclusion is correct by construction

`frozen-manifest.json` lists the **rebuild set**, which is the 27 modules downstream of an R1 source change.
It does not list the whole closure. `PaletteTransport.lean` is not downstream of any R1 change, so it is
correctly absent. Its olean is the encoding-r4 verified olean, byte for byte.

The evidence was recomputed by `tools/manifest_complete.py`. Full per-module table:
`r1-gates/manifest-complete.json`, 83 modules: 82 baseline modules plus the new AvoidingTrace.

| Check | Result |
|---|---|
| Modules whose source differs from encoding-r4 | 5: States, AvoidingTrace (new), FiveSupport, FourContinuity, Interfaces |
| Downstream closure of those 5, from the `import` graph | 27 modules, exactly the frozen-manifest `order` list (`affectedAllInFrozen`, `frozenOnlyAffected` both true) |
| Frozen-manifest sha256 vs current R1 sources | all 27 match |
| Remaining 56 modules: source byte-identical to encoding-r4/src | true for all 56 |
| Remaining 56 modules: olean byte-identical to encoding-r4/build | true for all 56 |
| PaletteTransport source sha256 | `2d9b386950a8f25445838c43908dc7ced2be5932435c6e65fb80509b55eea196`, identical in R1, R4 and the R4 full-build plan (order 44) |
| PaletteTransport olean sha256 (R1 build = R4 build) | `cf218b2384460c7c0554b837293dc8d0b898807b03a64c068bf4d738684683d8` |
| PaletteTransport compile evidence | `lean-queue/encoding-r4-full-44.log`: Lean 4.34.1, source sha 2d9b3869…, Status passed, Exit 0 (R4 full 82-module build) |
| Importers of PaletteTransport | Rigidity, BinaryPalettes (both upstream-unchanged) |

`sixty` (`PaletteTransport.lean:390`) is therefore an unchanged, previously verified upstream
declaration. The R1 consumers that use it (FiveSupport, StepBanConsumer) were compiled against
that verified olean.

Side observation: 11 of the 27 rebuilt R1 oleans are byte-identical to their encoding-r4 oleans.
Lean's output is deterministic, and those modules' content did not change.

## Recommendation

No requeue is needed. For a self-contained manifest, `manifest-complete.json` can be shipped beside
`frozen-manifest.json`. It records role, source/olean sha256 and imports for all 83 modules.
