# S2 banking manifest (simplification desk)

Generated 2026-11-15T05:24Z by `tools/make_manifest.py s2`. Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; all desk runs are local, one Lean process at a time.

## Claim

S1, plus 55 more declarations that no root theorem reaches, deleted from the 27 modules outside the R1 closure (spectral, compact-factor and palette layers). Any `omit/include .. in` prefix is deleted with its declaration.

| Measure | vs accepted R1 | vs supplied original |
|---|---|---|
| physical lines | -717 | -867 |
| nonblank lines | -713 | -883 |
| code lines | -700 | -908 |

Files changed vs R1: 41. Declarations removed: 77 unreachable plus `five_forced_label` (replaced). Added: `five_state_forced_label`.

Public statements: every declaration surviving from R1 keeps its exact type, binder flags, universe parameters and definition-value hash. This is checked by the signature gate below.

## Files (changed vs R1)

| Module | R1 lines | new lines | delta | sha256 (raw = LF) |
|---|---|---|---|---|
| OAI.Analysis.PlaneSpectrum.CircleOperator | 308 | 292 | -16 | `1a1523f435af9f6efbb10806ef4dc5ccd76f69b226642b997ad0c98398287de1` |
| OAI.Analysis.PlaneSpectrum.ConditionalSpectrum | 530 | 529 | -1 | `fcb77a76a2023bce5438bd5736984c50f07ba5f6e82cd1b765a8aa550eef693f` |
| OAI.Analysis.PlaneSpectrum.Energy | 453 | 449 | -4 | `10895c85c9d1ca9be76885fec41c4a1c63dc009ce0e6b2d4e8af47b16dc1adca` |
| OAI.Analysis.PlaneSpectrum.FourierTests | 295 | 287 | -8 | `73910dcd4dfda8fcf3491dccabe81d99322abe3452d5939859315a1895c29216` |
| OAI.Analysis.PlaneSpectrum.InvariantMean | 1078 | 1031 | -47 | `db71947b617c30ef32bff4cb2761ba9979d91339c216713213cb5e3a3952d769` |
| OAI.Analysis.PlaneSpectrum.Multipliers | 314 | 300 | -14 | `9437aff41e64bac8f6b4d476f1471e82bd42368f1fc839823474504f1b6949c3` |
| OAI.Analysis.PlaneSpectrum.PhaseCollision | 537 | 471 | -66 | `01d0a2f337e6f80cce42f67566df0109bbaddf2dc44df131aafe9b3648557f98` |
| OAI.Analysis.PlaneSpectrum.Representations | 477 | 471 | -6 | `a2880f4e65bdbf701589b4ea50e35fae7e1fec623cf0c32a1060c6636578d799` |
| OAI.Analysis.PlaneSpectrum.SpectralMeasure | 388 | 386 | -2 | `376c8087607945e0074d19c28516a73e05e91a272593c45019b623d9739af96b` |
| OAI.Geometry.PlaneColoring.AngularBoundary | 503 | 497 | -6 | `796414de07e4fb2ce5ae862530bc85742e6ba318ce6c12307644265d08e6c663` |
| OAI.Geometry.PlaneColoring.BinaryPalettes | 375 | 365 | -10 | `5e2ffdb80a1afd9101bf21b9e5a81a1874fb5dcc91ca485ae0679ac75eca25b3` |
| OAI.Geometry.PlaneColoring.BorelTransfer | 458 | 454 | -4 | `4e90138bb6baea8806982342fb74ec4aa702c4edb35645a11a732fe67887c441` |
| OAI.Geometry.PlaneColoring.BoundaryTrace | 367 | 313 | -54 | `6bb884aa073edd320672ede4145b8488af533c82550606603ea3da49683ab017` |
| OAI.Geometry.PlaneColoring.Compactness | 379 | 353 | -26 | `51897e8f294ca13bc33798bf36c3ee3f9bccd1b40e9ae628dc1184bf5d598930` |
| OAI.Geometry.PlaneColoring.ContinuumLimits | 353 | 337 | -16 | `cfa79b5f6d8e9449b0ef6beb8a8d40265cec5a9d939dfb14979389fed5081ca0` |
| OAI.Geometry.PlaneColoring.CyclicCore | 280 | 256 | -24 | `d55a1601a3d9d3679cc2ae6d16302f1eac71d71ace20a21c276c81e2e3d164ab` |
| OAI.Geometry.PlaneColoring.DiskExtension | 611 | 603 | -8 | `ef64358d8261d6a96c8b03469bee12f2ab0abd4647a9f1230b41059fc914ac64` |
| OAI.Geometry.PlaneColoring.Exclusion | 165 | 163 | -2 | `1613d1543f72813e05301a0e141e684bb4289e65a8d4905cc4f47b32057c8b67` |
| OAI.Geometry.PlaneColoring.Expansion | 725 | 715 | -10 | `b3684b996cc4bbf40eaf5697b8fa747b053f4c098f585f17e2e4298a21e4e348` |
| OAI.Geometry.PlaneColoring.FiveSupport | 354 | 337 | -17 | `b12dad93faddcbaf07dcb6e92a86c36ffb1e3a80f62192e64916ae936599eb65` |
| OAI.Geometry.PlaneColoring.FourContinuity | 509 | 503 | -6 | `46efa82aa091fd03ebe10a4d61142f96ad4f8a8533d7c84fa2d8117d5e18c6c9` |
| OAI.Geometry.PlaneColoring.GraphCuts | 314 | 310 | -4 | `9aa4f41d6e5ffc105ef0d1e416491e0c7dce2fd59735179545730098a4f06830` |
| OAI.Geometry.PlaneColoring.GraphRealization | 415 | 410 | -5 | `def12054e6260a4b85dfd13d19a06dc6355f39fb8cbeadbfe1ef1fa45f2e2d7a` |
| OAI.Geometry.PlaneColoring.HoleApproximation | 328 | 323 | -5 | `cbee4d2ae2fcf691333a7d21b274ddbb549cc30d39d00918f873e75b2c50176e` |
| OAI.Geometry.PlaneColoring.Interfaces | 528 | 517 | -11 | `c3348acdd555cc4196de9c9f14f1f32cb37f2f59dbfd54fccf591a3303b88e02` |
| OAI.Geometry.PlaneColoring.Lattice | 66 | 63 | -3 | `688cc2b73931dbdd4a05148d5c8e53d155ce976d587d40308c627a53a2db669f` |
| OAI.Geometry.PlaneColoring.Moser | 439 | 436 | -3 | `b2da0e254b41919a3858d23acf72bc643339871d1a4f0951d5ceb32f1a3fedcf` |
| OAI.Geometry.PlaneColoring.PaletteDensity | 485 | 463 | -22 | `24d1525a3efafe117962d32aff754f30949371234d7d14f3099361e1c0b0d68c` |
| OAI.Geometry.PlaneColoring.Palettes | 124 | 115 | -9 | `74585bde311823dbb9b9fbabce6ec89415134a8b298f7da66c31207e37e2646b` |
| OAI.Geometry.PlaneColoring.Sectors | 453 | 451 | -2 | `8acd47b52ea091d61506b8cbf529be6f59626812e90dddec6c7c1de7430e9e62` |
| OAI.Geometry.PlaneColoring.States | 566 | 461 | -105 | `7b411cc583485431fa957070a8d4c678ed35ba8cc7cec8b465925a0e03744520` |
| OAI.Geometry.PlaneColoring.WeakColoring | 176 | 174 | -2 | `7994f86994c903d2fb76cb60dcbe02cbb3f53047d282d42170122b578bf3c90b` |
| OAI.MeasureTheory.CompactFactors.Amenability | 411 | 401 | -10 | `08d0ae62ede2e89c3328801e0cbd5fbbde35c1cb8d4af3ae39e4f6406b9f8c19` |
| OAI.MeasureTheory.CompactFactors.BoundedFunctions | 223 | 219 | -4 | `f1750185aa305ce18f0937b6949d898d686e2dcdc297606f7c14aef5607bc58e` |
| OAI.MeasureTheory.CompactFactors.Centers | 703 | 700 | -3 | `51a370e921f6fcb8825d502538d5871d53bcb4f546f0d95580351bb63275019c` |
| OAI.MeasureTheory.CompactFactors.ConditionalLimits | 542 | 446 | -96 | `675f780669891ce6ff5bc604670da0be6c1f12391ee6eac052598a444807396a` |
| OAI.MeasureTheory.CompactFactors.Factors | 586 | 584 | -2 | `548ec497e431bf2cff7165b4b0ce39f6d8a5b7542dcfe476ac67a30d4ea6c291` |
| OAI.MeasureTheory.CompactFactors.Functions | 884 | 864 | -20 | `c3ffaf6e817bf4fdcc8f51d9355c7b6a56d2a6a2e22c835b6d463845cf60e902` |
| OAI.MeasureTheory.CompactFactors.RelativeCenters | 598 | 588 | -10 | `40010491b6e6f343d1b4191471f930fb5b18817a29a072c4180fbbfa8e03eb13` |
| OAI.MeasureTheory.CompactFactors.RelativeProducts | 472 | 445 | -27 | `f5abd2b8e32dae69da826d234f3310c41813989deb1438c0354795935c4c8d76` |
| OAI.MeasureTheory.CompactFactors.Separability | 573 | 546 | -27 | `bd2e5ea3afc7843aa5d2d269882c92db1cc8cb3779fd5d2108a1f8e936c01c1c` |

The deleted declarations are listed in `s1/dead-deletions.json`, `s2/dead-deletions.json` (module, start, end, name).

## Expected gate outputs

1. Rebuild: 67 modules (the downstream closure of the changed files) compile, each `exit 0`, with the logged sha256 equal to the source above. Logs: `s2/logs/NN-<Module>.log`.
2. Root axioms: `s2/logs/axiomroots-s2.log`. Every root prints exactly `[propext, Classical.choice, Quot.sound]` and none prints `sorryAx`. The 14 roots are: uniform_precision_contradiction, finite_uniform_precision_contradiction, ambient_uniform_precision_contradiction, finite_uniform_successor_contradiction, relative_singularity_successor, relative_singularity_approximation, no_proper_five_coloring, properColoring_seven, weakMeasurableColoring_seven, no_measurable_weak_five_coloring, no_proper_five_coloring_algebraic, five_support_step_ban, five_state_forced_label, five_opposite_contacts_false.
3. Signature dump: `s2/logs/sigdump-s2.log` writes `s2/sigs-s2.tsv`; compared with `r1-gates/sigs-r1.tsv`. Expected: 0 changed common declarations; removed = the 77 listed names, plus `five_forced_label`, plus auto-generated equation lemmas of deleted declarations; added = `five_state_forced_label` only; `FORBIDDEN_ABSENT` for all 78 deleted names.

## Results

- Rebuild: 67/67 module logs have exit 0 with a sha256 that matches the current source (67 logs present).
- Root axioms (s2/logs/axiomroots-s2.log): exit 0; 14/14 roots standard-only; sorryAx present: False.
- Signature dump (s2/logs/sigdump-s2.log): exit 0; common 3038, changed 4 ['OAI.EuclideanFiveColor.BoundedMeasurable.Family.avg', 'OAI.EuclideanFiveColor.BoundedMeasurable.Family.l2Linear', 'OAI.EuclideanFiveColor.BoundedMeasurable.Family.toL2', 'OAI.EuclideanFiveColor.BoundedMeasurable.pairSequence'], removed 84, added ['OAI.EuclideanFiveColor.five_state_forced_label']; FORBIDDEN_ABSENT 78, FORBIDDEN_PRESENT 0.
