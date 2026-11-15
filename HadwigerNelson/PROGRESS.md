# Progress — 15 November 2026

**No global chromatic result.** The bounds 6 ≤ χ(ℝ²) ≤ 7 come from the supplied
proof and the classical seven-colouring. Nothing the team has added changes them.
The only recorded route to χ ≥ 7 is conditional on two open lemmas, L6 and F6.

The canonical, sourced list of every result is the
[results ledger](RESULTS-LEDGER.md) ([JSON](results-ledger.json)). Each ledger
entry gives the exact statement with its hypotheses, a single status, artifact
paths with SHA-256, provenance, the correction history, and what the results desk
re-checked. This page summarises it. Status words are the ledger's:
`LEAN_VERIFIED` (local Lean 4.34.1, Mathlib `d13f23b`, printed axiom list),
`PROVED_PAPER_REVIEWED` (named referee file), `TESTED_FINITE` (exact computation),
`CANDIDATE`, `UNAUDITED_NUMBER`, `RETRACTED_OR_REFUTED` and `OPEN`.

## Simplification of the supplied proof

| Result | Status and evidence | Line change / scope |
| --- | --- | --- |
| Common-encoding refactor ([ENC-R4](RESULTS-LEDGER.md#enc-r4)) | `LEAN_VERIFIED`: [R4 validation](Main/ResearchSnapshot/local/outputs/ENCODING-REFACTOR-VALIDATION.txt), [sources](Main/ResearchSnapshot/local/outputs/encoding-refactor/) | **−126 lines** (ConditionalSpectrum 497→530, ConditionalLimits 701→542). 82-module closure; nine root theorems on standard axioms. |
| Three-centre integration ([R1](RESULTS-LEDGER.md#r1)) | `LEAN_VERIFIED`; accepted by Jarom ~23:25Z on 14 Nov: [frozen manifest](Main/ResearchSnapshot/local/work/lean-queue/threecentre-r1/frozen-manifest.json), [line accounting](Main/ResearchSnapshot/local/work/lean-queue/threecentre-r1/line-accounting.json), [root axiom log](Main/ResearchSnapshot/import-20261115/work/lean-queue/threecentre-r1-axiomroots.python.log) | **−24 lines net** (States 764→566, FourContinuity 551→509, FiveSupport 376→354, Interfaces +1, new AvoidingTrace +237). All 27 modules compile, and the nine roots (including `no_proper_five_coloring`) use standard axioms only. The results desk re-hashed all 27 sources and recounted the lines. Follow-ups: contract and dependency gates were not re-run, and PaletteTransport (unchanged since R4) is missing from the manifest. |
| Branch-free step ban and its consumer ([STEPBAN-V2](RESULTS-LEDGER.md#stepban-v2), [STEPBAN-CONSUMER](RESULTS-LEDGER.md#stepban-consumer)) | `LEAN_VERIFIED` standalone: jobs 220720-0 and 232057-0 ([import notes](Main/ResearchSnapshot/import-20261115/IMPORT-NOTES.md)) | Same statements as manuscript Lemma 6.7 and its consumers (identical `#check` output, including the CyclicCore consumer, [STEPBAN-CYCLICCORE](RESULTS-LEDGER.md#stepban-cycliccore)). The same-name swap inside FiveSupport compiles on R1 with all 31 public signatures unchanged ([FIVESUPPORT-SWAP](RESULTS-LEDGER.md#fivesupport-swap)). This removes a case split and one finite lemma but **adds lines**: +61 as ported, and a measured +33 (354 → 387) with the old step ban deleted, all 30 remaining signatures unchanged. It is not yet substituted into the tree. A shorter desk version (v3, FiveSupport −15 staged) is not yet compiled. |
| Fixed/moving three-centre theorems and the joint-pair support theorem | `LEAN_VERIFIED` and paper-refereed: [three-centre](Main/ResearchSnapshot/local/outputs/three-centre/), [joint support](Main/ResearchSnapshot/local/outputs/joint-support/) | The three-centre theorems are now integrated by R1. The joint-pair support theorem stays standalone. Lemma 6.7 (`five_support_step_ban`) is retained. |

The integrated tree is **−150 lines** in total (−126 and −24). The step-ban work is a structural simplification and is not counted as a line saving.

## New mathematics (all local, conditional, or finite)

| Result | Status and evidence | Scope / outstanding work |
| --- | --- | --- |
| Closed 60° cone obstruction ([CC60](RESULTS-LEDGER.md#cc60)) | `LEAN_VERIFIED`: [validation](Main/ResearchSnapshot/local/outputs/cone/VALIDATION.json), [axiom audit](Main/ResearchSnapshot/local/outputs/cone/cone-audit-v3.log) | Under the same-centre approaching-continuum and support-exclusion hypotheses, at least three labels remain. Local obstruction only. |
| Generic sharpness of CC60 ([SHARPNESS-20](RESULTS-LEDGER.md#sharpness-20)) | `PROVED_PAPER_REVIEWED`: [construction](Main/ResearchSnapshot/scale-up/ULTRA-CONE-NOVELTY-AUDIT.txt), [referee](Main/ResearchSnapshot/scale-up/ULTRA-SHARPNESS-REFEREE.txt) | 20 colours. Six-colour sharpness and priority are not established. |
| Canonical paired palette excluded at one centre ([A5-FOUR-LIST](RESULTS-LEDGER.md#a5-four-list)) | `PROVED_PAPER_REVIEWED`: [proof](Main/ResearchSnapshot/import-20261115/outputs/ASTRA-FOUR-LIST-A5.txt), [referee](Main/ResearchSnapshot/import-20261115/outputs/ASTRA-FOUR-LIST-REFEREE.txt) | Finite existence only (walk coordinates not enumerated); not in Lean. The [sliver interval certificate](RESULTS-LEDGER.md#a5-sliver) is `TESTED_FINITE`. |
| A6 producer chain ([A6-FORCING](RESULTS-LEDGER.md#a6-forcing), [A6-BRIDGE-R2](RESULTS-LEDGER.md#a6-bridge-r2), [G1-R2](RESULTS-LEDGER.md#g1-r2), [G3-R2](RESULTS-LEDGER.md#g3-r2)) | `LEAN_VERIFIED` pieces: [import notes](Main/ResearchSnapshot/import-20261115/IMPORT-NOTES.md) | The glued bridge ([A6-BRIDGE-R2-G3](RESULTS-LEDGER.md#a6-bridge-r2-g3)) now proves `ArcCover` but still takes `SignTable` and `ForcingLemma` as hypotheses; the fully glued file is `OPEN`. The forcing job printed no axiom list. The paper producer ([A6-PAIRED-PRODUCER](RESULTS-LEDGER.md#a6-paired-producer)) is a `CANDIDATE` (parent-checked, no referee file). |
| Even-walk reachability and list/parity obstructions ([EVENWALK-R6](RESULTS-LEDGER.md#evenwalk-r6)) | `LEAN_VERIFIED` (desk compile, standard axioms) | For weak measurable k-colourings. Revisions r1–r5 failed and were superseded. |
| Six six-direction configurations excluded ([SIX-ORBIT](RESULTS-LEDGER.md#six-orbit)) | `TESTED_FINITE`: [certificates](Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T191820Z/inner-outer-orbit-certificates.json) | Relaxation level, with an open 15° exclusion neighbourhood. The exact global radius is open. |
| Fixed-phase census and staircase census ([FIXED-PHASE-CENSUS](RESULTS-LEDGER.md#fixed-phase-census), [STAIRCASE-CENSUS](RESULTS-LEDGER.md#staircase-census)) | `TESTED_FINITE`: two independent implementations each | 177 SAT / 7,599 UNSAT. 76,283 of 36,415,008 staircases survive, which is a necessary condition only. The earlier total 36,415,608 was a typo. |
| Discrete direction filtering ([DIR-FILTER](RESULTS-LEDGER.md#dir-filter)) | `TESTED_FINITE`, re-run by the results desk: [audit](Main/ResearchSnapshot/local/work/checkin-artifacts/20261114T172056Z/) | 7,776 → 1,420 → 174 → 6. The old count of 95 came from a reconstruction bug. Grid only. |
| Heule union and no-forcing ([HEULE-UNION](RESULTS-LEDGER.md#heule-union), [HEULE-NO-FORCING](RESULTS-LEDGER.md#heule-no-forcing)) | `TESTED_FINITE`, re-verified at 23:50Z on 14 Nov | 1,048 vertices, exact geometry. No forced-equal pair in either graph. |
| All-phase field set has measure exactly 1/648 ([RELAX-1-648](RESULTS-LEDGER.md#relax-1-648)) | `TESTED_FINITE`: two independent exact implementations (discovery m2 scripts; [results-desk recount](Main/ResearchSnapshot/import-20261115/work/results-desk/allphase/allphase_desk.out)) | 1,440 of 933,120 resonance cells. The two disputed wordings are both true: 16 of the 3,840 mod-180 sign cells, which lie in 16 of the 120 mod-180 orders. Relaxation level only. |

## Negative results

[MC120-ENDPOINT](RESULTS-LEDGER.md#mc120-endpoint): the closed-120° MC120 is false,
shown by a refereed 19-colour counterexample. Other refereed local countermodels are
[ANNULUS-3COL](RESULTS-LEDGER.md#annulus-3col),
[SUPPORT-FLIP](RESULTS-LEDGER.md#support-flip),
[FOUR-STATE-ANGULAR](RESULTS-LEDGER.md#four-state-angular) and
[VARIABLE-TRIANGLE](RESULTS-LEDGER.md#variable-triangle). The ledger also lists the
refuted claims (AC-axis, two-triangle classification, alternating triple, the
Claude05 verdict, overnight withdrawals) and every failed Lean revision.

## Main open gaps

The glued A6 producer; the step-ban swap; the R1 contract/dependency gates; a
referee for strict MC120 (A6 corollaries and the continuous classification depend
on it); palette rigidity; the staircase converse; and L6/F6.

The original [progress log](Main/ResearchSnapshot/local/outputs/PROGRESS-LOG.txt),
[consolidated findings](Main/ResearchSnapshot/local/outputs/CONSOLIDATED-FINDINGS.txt),
and [research status](Main/ResearchSnapshot/local/outputs/RESEARCH-STATUS.txt)
keep the sequence of corrections and handoffs. Newer copies are in
[import-20261115](Main/ResearchSnapshot/import-20261115/IMPORT-NOTES.md). Historical
policy, quota and deadline statements in those reports describe their original
times.

## Import validation

The repository import checks exact file hashes, the stated cone and R4 source
hashes, certificate structure, and graph-colouring witnesses. Results and the
reproduction command are recorded in
[Main/IMPORT-VALIDATION.json](Main/IMPORT-VALIDATION.json). On 15 November the
results desk added `Main/ResearchSnapshot/import-20261115/`: the Lean sources,
compile logs and axiom checks banked after the first capture, together with the
census, sliver and six-orbit evidence and the newer reports. After that import,
`node HadwigerNelson/Main/verify-snapshot.mjs` passes on 11,698 files. Existing
Lean compiler logs are kept as prior verification evidence. The import does not
claim a fresh complete Lean rebuild, or integration into the repository's 4.35.0
target.
