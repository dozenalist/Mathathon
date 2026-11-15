# Results ledger — Hadwiger–Nelson Mathathon entry

Built 2026-11-15T06:38Z by the results desk. Machine-readable copy: [results-ledger.json](results-ledger.json). Every artifact hash below was recomputed when the ledger was built. A 16-character prefix is shown here; the JSON has the full SHA-256. Paths starting `I/` are in the research workspace `C:/Users/jarom/Documents/Codex/2026-11-13/i`, outside the repository; other paths are repository-relative from the repository root.

**No global chromatic result. The bounds 6 ≤ χ(ℝ²) ≤ 7 come from the supplied proof ("The Euclidean plane is not five-colorable") and the classical 7-colouring; nothing the team has added changes them. Every entry below is a simplification of the supplied proof, a local or conditional lemma, a finite computation, or a negative result. The only route to χ ≥ 7 on record is conditional on the open lemmas L6 and F6 (see L6-F6).**

Status vocabulary (exactly one per entry): `LEAN_VERIFIED`, `PROVED_PAPER_REVIEWED`, `TESTED_FINITE`, `CANDIDATE`, `UNAUDITED_NUMBER`, `RETRACTED_OR_REFUTED`, `OPEN`. `LEAN_VERIFIED` means a local Lean 4.34.1 compile against pinned Mathlib `d13f23b` with exit 0 and a printed axiom list. A coordinator or worker saying "banked" is treated as a claim; the "Checked by the results desk" line says what was actually re-checked.

## Summary

### Simplification of the supplied proof (net line deltas)

| Item | Status | Line change | Notes |
| --- | --- | --- | --- |
| [ENC-R4](#enc-r4) common-encoding refactor | `LEAN_VERIFIED` | **−126** (ConditionalSpectrum 497→530, ConditionalLimits 701→542) | 82-module closure, 9 root axiom checks |
| [R1](#r1) three-centre integration (threecentre-r1) | `LEAN_VERIFIED`, accepted by Jarom ~23:25Z | **−24 net** (States 764→566, FourContinuity 551→509, FiveSupport 376→354, Interfaces 527→528, new AvoidingTrace +237) | 27/27 modules + 9 roots; desk recount matches line-accounting.json |
| [STEPBAN-V2](#stepban-v2) branch-free step ban | `LEAN_VERIFIED` (standalone) | proof body 21→15 lines; but the module grows (see FIVESUPPORT-SWAP) | jobs 220720-0, 232057-0 |
| [STEPBAN-CONSUMER](#stepban-consumer) consumer on v2 | `LEAN_VERIFIED` (standalone) | 0 realised (swap pending) | job 232057-0; identical `#check` telescopes |
| [STEPBAN-CYCLICCORE](#stepban-cycliccore) CyclicCore consumer on v2 | `LEAN_VERIFIED` (desk) | 0 realised (swap pending) | identical `#check` telescope |
| [FIVESUPPORT-SWAP](#fivesupport-swap) same-name swap in FiveSupport (R1 port) | `LEAN_VERIFIED` (desk) | **+61 as ported** (v1 kept); **measured +33** with v1 deleted (354→387 physical; code lines only 341→350, +9) | 30/30 signatures identical after deleting v1; structural, not a length, simplification |
| [S1](#s1) dead-code deletion + in-place branch-free step ban (simplification desk) | `LEAN_VERIFIED` (re-verified 03:3x–03:44Z) | **−265** (14 files; recounted) | 27-module rebuild, 14 roots standard axioms, 3,094 signatures unchanged |
| [S2](#s2) S1 + 52 more unreachable declarations in the spectral, compact-factor and palette layers | `LEAN_VERIFIED` (gates ~05:20Z) | **−717 vs R1** (41 files; −452 beyond S1) | 67-module rebuild, 14 roots standard axioms, 3,038 signatures unchanged (aux-name renames only) |
| [JOINT-SUPPORT](#joint-support) joint-pair support theorem | `LEAN_VERIFIED` (standalone) | not measured | does not by itself delete the original States development |
| **Total realised (LEAN_VERIFIED chain)** |  | **−126 + −24 + −265 + −452 = −867 lines** vs the supplied original | S2 includes S1; −908 code lines |

### Strongest new results

- [CC60](#cc60) — closed 60° cone obstruction (equality case included), Lean-verified with standard axioms; sharp for arbitrary finite palettes by the reviewed 20-colour construction [SHARPNESS-20](#sharpness-20).
- [ENC-R4](#enc-r4), [R1](#r1) and [S1](#s1) — the supplied proof now compiles in a simplified form 867 lines shorter (with [S2](#s2)), with Lemma 6.7 branch-free under its original name, every surviving statement unchanged, and the root theorems (incl. `no_proper_five_coloring`, `weakMeasurableColoring_seven`) on standard axioms only.
- A6 six-colour producer chain in Lean: [A6-FORCING](#a6-forcing), [G1-R2](#g1-r2), [G3-R2](#g3-r2), [A6-BRIDGE-R2-G3](#a6-bridge-r2-g3) and the glued endgame [A6-GLUE](#a6-glue): SignTable, ForcingLemma and ArcCover are discharged, so the A6 endgame reduces to two named inputs, `A5Obstruction` and `hsupp`.
- [A5-FOUR-LIST](#a5-four-list) — refereed: no centre of a weak measurable 6-colouring has an actual palette containing the canonical paired palette; with the paired producer [A6-PAIRED-PRODUCER](#a6-paired-producer) (paper, its finite core Lean-verified) this excludes the paired interface configuration.
- [MC120-ENDPOINT](#mc120-endpoint) — refereed 19-colour counterexample: the closed-120° version of MC120 is false; [SIX-ORBIT](#six-orbit) — six direction configurations that pass every cone test are excluded by the exact relaxation.
- [EVENWALK-R6](#evenwalk-r6) — even unit-distance walk reachability and the finite list / two-list parity obstructions for weak measurable k-colourings, Lean-verified.
- Finite certificates: [HEULE-UNION](#heule-union) (1,048 vertices, exact) and [HEULE-NO-FORCING](#heule-no-forcing); [FIXED-PHASE-CENSUS](#fixed-phase-census) 177 SAT / 7,599 UNSAT; [STAIRCASE-CENSUS](#staircase-census) 76,283 of 36,415,008; [A5-SLIVER](#a5-sliver) interval certificate.

### Main open gaps

- **No global chromatic result.** No reviewed proof changes any bound on χ(ℝ²) or on the measurable chromatic number.
- [A6-GLUE](#a6-glue): the glued endgame compiles, but `A5Obstruction` (paper, not in Lean) and the support exclusions `hsupp` remain named hypotheses.
- [PALETTE-RIGIDITY](#palette-rigidity), [STAIRCASE-CONVERSE](#staircase-converse), [K6-PRODUCER](#k6-producer): the missing lemmas for the six-colour programme.
- [SHARPNESS-20](#sharpness-20): six-colour sharpness of CC60 and novelty priority are not established.
- [MC120-STRICT](#mc120-strict): strict MC120 is called "accepted paper" in the status file but has no referee file; [A6-COROLLARIES](#a6-corollaries) and [CONTINUOUS-SIX](#continuous-six) depend on it.
- [L6-F6](#l6-f6): the only recorded route to χ ≥ 7 needs two open lemmas; [LOCALIZED-TWO-STATE](#localized-two-state) is open.

### Counts

| Theme | LEAN_VERIFIED | PROVED_PAPER_REVIEWED | TESTED_FINITE | CANDIDATE | UNAUDITED_NUMBER | RETRACTED_OR_REFUTED | OPEN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Simplification of the supplied proof | 14 | 1 | 1 |  |  |  |  |
| New mathematics | 10 | 8 | 10 | 18 |  |  | 5 |
| Negative results and counterexamples | 1 | 7 | 6 | 7 |  | 8 |  |
| Infrastructure | 1 |  | 1 |  |  | 1 | 1 |

## Index

- **Simplification of the supplied proof**: [DIAMOND](#diamond) `LEAN_VERIFIED`, [ENC-R4](#enc-r4) `LEAN_VERIFIED`, [FIVE-CYCLE-RESIDUES](#five-cycle-residues) `LEAN_VERIFIED`, [FIVESUPPORT-SWAP](#fivesupport-swap) `LEAN_VERIFIED`, [JOINT-SUPPORT](#joint-support) `LEAN_VERIFIED`, [R1](#r1) `LEAN_VERIFIED`, [S1](#s1) `LEAN_VERIFIED`, [S2](#s2) `LEAN_VERIFIED`, [STEPBAN-CONSUMER](#stepban-consumer) `LEAN_VERIFIED`, [STEPBAN-CYCLICCORE](#stepban-cycliccore) `LEAN_VERIFIED`, [STEPBAN-SWAP](#stepban-swap) `LEAN_VERIFIED`, [STEPBAN-V2](#stepban-v2) `LEAN_VERIFIED`, [STEPBAN-V3](#stepban-v3) `LEAN_VERIFIED`, [THREE-CENTRE](#three-centre) `LEAN_VERIFIED`, [LEMMA67-IDENTITY](#lemma67-identity) `PROVED_PAPER_REVIEWED`, [R1-GATES](#r1-gates) `TESTED_FINITE`
- **New mathematics**: [A6-BRIDGE-R2](#a6-bridge-r2) `LEAN_VERIFIED`, [A6-BRIDGE-R2-G3](#a6-bridge-r2-g3) `LEAN_VERIFIED`, [A6-FORCING](#a6-forcing) `LEAN_VERIFIED`, [A6-GLUE](#a6-glue) `LEAN_VERIFIED`, [CC60](#cc60) `LEAN_VERIFIED`, [CONNECTED-SET](#connected-set) `LEAN_VERIFIED`, [EVENWALK-R6](#evenwalk-r6) `LEAN_VERIFIED`, [G1-R2](#g1-r2) `LEAN_VERIFIED`, [G3-R2](#g3-r2) `LEAN_VERIFIED`, [NULL-TRANSFER](#null-transfer) `LEAN_VERIFIED`, [A5-FOUR-LIST](#a5-four-list) `PROVED_PAPER_REVIEWED`, [A6-PAIRED-PRODUCER](#a6-paired-producer) `PROVED_PAPER_REVIEWED`, [AC-ALIGNED](#ac-aligned) `PROVED_PAPER_REVIEWED`, [MC120-STRICT](#mc120-strict) `PROVED_PAPER_REVIEWED`, [NR-TC](#nr-tc) `PROVED_PAPER_REVIEWED`, [RESIDUAL-GRAPH](#residual-graph) `PROVED_PAPER_REVIEWED`, [SHARPNESS-20](#sharpness-20) `PROVED_PAPER_REVIEWED`, [STRAIGHT-NEEDLE](#straight-needle) `PROVED_PAPER_REVIEWED`, [A5-SLIVER](#a5-sliver) `TESTED_FINITE`, [DIR-FILTER](#dir-filter) `TESTED_FINITE`, [FIXED-PHASE-CENSUS](#fixed-phase-census) `TESTED_FINITE`, [HEULE-UNION](#heule-union) `TESTED_FINITE`, [HONEYCOMB-73](#honeycomb-73) `TESTED_FINITE`, [LN1-ORBITS](#ln1-orbits) `TESTED_FINITE`, [LN3-T1-T3](#ln3-t1-t3) `TESTED_FINITE`, [RELAX-1-648](#relax-1-648) `TESTED_FINITE`, [SIX-ORBIT](#six-orbit) `TESTED_FINITE`, [STAIRCASE-CENSUS](#staircase-census) `TESTED_FINITE`, [A5-ODD-WALK](#a5-odd-walk) `CANDIDATE`, [A6-COROLLARIES](#a6-corollaries) `CANDIDATE`, [A7-PARTIAL-INDEPENDENT](#a7-partial-independent) `CANDIDATE`, [AMPLIFIER](#amplifier) `CANDIDATE`, [CENSUS-COMPLETE-60Z](#census-complete-60z) `CANDIDATE`, [CLAUDE-LEMMA-A](#claude-lemma-a) `CANDIDATE`, [CONTINUOUS-SIX](#continuous-six) `CANDIDATE`, [HONEYCOMB-RESTRICTED](#honeycomb-restricted) `CANDIDATE`, [J-DEPTH](#j-depth) `CANDIDATE`, [K6-M3-DOOR](#k6-m3-door) `CANDIDATE`, [LIST-FIELD-A4](#list-field-a4) `CANDIDATE`, [Q4Q5-PINNING](#q4q5-pinning) `CANDIDATE`, [R0-CHI4](#r0-chi4) `CANDIDATE`, [RELAX-CIRCULANT](#relax-circulant) `CANDIDATE`, [T6-B2](#t6-b2) `CANDIDATE`, [THM-BPRIME](#thm-bprime) `CANDIDATE`, [TRANSLATION-CRITERION](#translation-criterion) `CANDIDATE`, [WILD-LAW](#wild-law) `CANDIDATE`, [K6-PRODUCER](#k6-producer) `OPEN`, [L6-F6](#l6-f6) `OPEN`, [LOCALIZED-TWO-STATE](#localized-two-state) `OPEN`, [PALETTE-RIGIDITY](#palette-rigidity) `OPEN`, [STAIRCASE-CONVERSE](#staircase-converse) `OPEN`
- **Negative results and counterexamples**: [A6-CONTAINMENT](#a6-containment) `LEAN_VERIFIED`, [A7-CONTACT](#a7-contact) `PROVED_PAPER_REVIEWED`, [ANNULUS-3COL](#annulus-3col) `PROVED_PAPER_REVIEWED`, [FOUR-STATE-ANGULAR](#four-state-angular) `PROVED_PAPER_REVIEWED`, [LOCAL-TRANSITIONS](#local-transitions) `PROVED_PAPER_REVIEWED`, [MC120-ENDPOINT](#mc120-endpoint) `PROVED_PAPER_REVIEWED`, [SUPPORT-FLIP](#support-flip) `PROVED_PAPER_REVIEWED`, [VARIABLE-TRIANGLE](#variable-triangle) `PROVED_PAPER_REVIEWED`, [HEULE-NO-FORCING](#heule-no-forcing) `TESTED_FINITE`, [HISTORIC-8](#historic-8) `TESTED_FINITE`, [HONEYCOMB-K16](#honeycomb-k16) `TESTED_FINITE`, [LN2-COUNTERMODEL](#ln2-countermodel) `TESTED_FINITE`, [Q4Q5-CONTROLS](#q4q5-controls) `TESTED_FINITE`, [RELAX-WITNESSES](#relax-witnesses) `TESTED_FINITE`, [A8-PALETTE](#a8-palette) `CANDIDATE`, [ALPHA-SHARP](#alpha-sharp) `CANDIDATE`, [FOURWAY-SPLIT](#fourway-split) `CANDIDATE`, [GEOM-Q4Q5](#geom-q4q5) `CANDIDATE`, [GEOM-TWO-STEP](#geom-two-step) `CANDIDATE`, [Q4Q5-APEX](#q4q5-apex) `CANDIDATE`, [TERNARY-COUNTERMODEL](#ternary-countermodel) `CANDIDATE`, [A5-FAR-APEX](#a5-far-apex) `RETRACTED_OR_REFUTED`, [A5-M5-TEMPLATE](#a5-m5-template) `RETRACTED_OR_REFUTED`, [AC-AXIS](#ac-axis) `RETRACTED_OR_REFUTED`, [ALT-TRIPLE](#alt-triple) `RETRACTED_OR_REFUTED`, [CLAUDE05-VERDICT](#claude05-verdict) `RETRACTED_OR_REFUTED`, [OVERNIGHT-WITHDRAWN](#overnight-withdrawn) `RETRACTED_OR_REFUTED`, [PALETTE-EQ-F](#palette-eq-f) `RETRACTED_OR_REFUTED`, [TWO-TRIANGLE](#two-triangle) `RETRACTED_OR_REFUTED`
- **Infrastructure**: [ENC-R4-AUX](#enc-r4-aux) `LEAN_VERIFIED`, [SNAPSHOT-VALIDATION](#snapshot-validation) `TESTED_FINITE`, [LEAN-FAILED-REVISIONS](#lean-failed-revisions) `RETRACTED_OR_REFUTED`, [LEAN-435](#lean-435) `OPEN`

## Simplification of the supplied proof

### DIAMOND

**Diamond equality lemma (three-colour diamond, tips equal)** — `LEAN_VERIFIED`

- **Statement:** `SimplifyAngular.three_color_diamond_omega` and `SimplifyAngular.diamond_tips`: the diamond equality lemma and its corollary (finite colour argument).
- **Evidence:** diamond-pinned-core.log: Lean 4.34.1, exit 0; axioms [propext, Quot.sound] (a subset of the standard three). First run on Lean 4.35.0 core Omega.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/DiamondStandalone.lean` — source — `67cdbc7be0b14601…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/diamond-pinned-core.log` — compile log (4.34.1) — `129eedc3a1694aeb…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/diamond-standalone.log` — first log — `6bfba1214e0f46f4…`
- **Checked by the results desk:** Read the archived log: Version 4.34.1, "Status: passed", "Exit code: 0", logged Source SHA256 equals the archived source (hash recomputed), axiom lines parsed. Did not recompile.
- **Provenance:** Simplification (angular) lane, overnight 13–14 Nov.

### ENC-R4

**Common-encoding refactor (encoding-r4) of the supplied spectral argument** — `LEAN_VERIFIED`

- **Statement:** The supplied proof's conditional spectrum/limit development is rewritten over one common encoding; ConditionalSpectrum.lean 497→530 lines and ConditionalLimits.lean 701→542 lines, net −126. The public precision-contradiction theorem headers are unchanged (fidelity checked after whitespace/name normalisation).
- **Hypotheses:** Same statements as the supplied proof; no new hypotheses. The nine root theorems include `OAI.EuclideanFiveColor.no_proper_five_coloring`, `OAI.Problem160.properColoring_seven`, `OAI.Problem160.weakMeasurableColoring_seven`.
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; full 82-module affected closure passed; nine root axiom sets exactly [propext, Classical.choice, Quot.sound]; no sorryAx; 6 declarations / 133 binders inspected (BINDER-INSPECTION.txt).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ENCODING-REFACTOR-VALIDATION.txt` — validation record — `b63f700ffed8eec1…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/encoding-refactor/ConditionalSpectrum.lean` — source — `d26d569088faea89…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/encoding-refactor/ConditionalLimits.lean` — source — `24f89dd33533a0f6…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/encoding-refactor/BINDER-INSPECTION.txt` — binder inspection — `27df4e42e37f6aca…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/encoding-r4-axiomroots.log` — root axiom log — `e6d173c7e694e64b…`
- **Checked by the results desk:** 2026-11-14 23:50Z: re-ran `node HadwigerNelson/Main/verify-snapshot.mjs` (passed, 11 s), which re-hashes both sources against the pinned values; source hashes recomputed at build. Did not recompile.
- **Provenance:** Local Lean queue, encoding-r2→r4 revisions, 2026-11-14 01:20–07:09Z (Pacific 07:09 binder inspection).
- **Correction history:** a "−150 lines" projection and a 718-line deletion patch were not accepted (CONSOLIDATED-FINDINGS); r2/r3 revisions failed and were repaired (logs encoding-r2-*, encoding-r3-*); axiom-output parser fixed to allow an apostrophe in `exists_strictAnti_scale'`
- **Used for:** Baseline for R1 (frozen-manifest "baseline: encoding-r4 verified"); simplification ledger.

### FIVE-CYCLE-RESIDUES

**Five-cycle residue finite facts (reflection lemmas and residue reductions)** — `LEAN_VERIFIED`

- **Statement:** Finite facts about five-cycle residues: 14 reflection lemmas then 21 theorems, including `five_residues_reduce_to_two`, `label_transport`, `g_involutive`, `h_involutive`.
- **Evidence:** five-cycle-residues-v4.log: Lean 4.34.1, exit 0, [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/FiveCycleResiduesV4.lean` — source — `602bda97b14d38eb…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/five-cycle-residues-v4.log` — compile log — `23bbd9363d30735d…`
- **Checked by the results desk:** Read the archived log: Version 4.34.1, "Status: passed", "Exit code: 0", logged Source SHA256 equals the archived source (hash recomputed), axiom lines parsed. Did not recompile.
- **Provenance:** Simplification lane, overnight 13–14 Nov.
- **Correction history:** h(P_j) = P(−j), not P(hj)
- **Caveats:** Supported the five-cycle shortcut, which was withheld (see OVERNIGHT-WITHDRAWN); Lemma 6.7 retained.

### FIVESUPPORT-SWAP

**Same-name step-ban swap inside FiveSupport (R1 port)** — `LEAN_VERIFIED`

- **Statement:** FiveSupportSwapR1.lean = the accepted R1 FiveSupport.lean plus the block `five_outsider_unique`, `five_pair_meet`, `five_support_step_ban_v2` inserted before `five_opposite_contacts_false`, whose two callees are switched from `five_support_step_ban` to `_v2`. All 31 public declarations keep their exact statements.
- **Hypotheses:** Unchanged statements (31/31 `#check` outputs identical to the R1 FiveSupport module). The old `five_support_step_ban` is still present (not deleted).
- **Evidence:** Desk compile (research desk) exit 0, 323 s; `five_opposite_contacts_false` and `five_support_step_ban_v2` [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/FiveSupport-swap/FiveSupportSwapR1.lean` — R1 port source — `e531cf133a213e52…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/FiveSupport-swap/swapR1.log` — compile log: 31 #check outputs + axioms — `7bbaece10131d754…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/FiveSupport-swap/FiveSupportSwapR1-noV1.lean` — variant with the old step ban deleted — `0aaee265081c94ba…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/FiveSupport-swap/noV1.log` — compile log of the v1-deleted variant: 30 #check outputs + axioms — `4d9e0814064756a2…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/FiveSupport-swap/orig.log` — 31 #check outputs of the R1 FiveSupport module — `749c21cfff0461ad…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/FiveSupport-swap/swap.log` — first compile of the swarm file (failed on R1) — `41d849c3929bf37b…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T002122-download-1-FiveSupport-swap.lean` — swarm source (targets encoding-r4) — `3291ad95a0c3cc82…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T002122-download-3-REFEREE.md` — swarm referee report (m5) — `4aa0931aefc47eb1…`
- **Checked by the results desk:** 2026-11-15 ~01:05Z: parsed the 31 `#check` blocks in swapR1.log and orig.log and compared them: 31 common names, 0 differences, none missing on either side; read both axiom lines. Line accounting (desk diff against R1 FiveSupport.lean, 354 lines): the port is 415 lines without #check/#print lines = 2 call lines changed + 3-line comment + 58-line v2 block inserted; nothing deleted. Deleting the old step ban (FiveSupport.lean:68–99, 32 lines) and `five_forced_label` (Exclusion.lean:26–28, 3 lines) would still leave about +23 lines, because the new block carries long docstrings and two helper lemmas. So this is a structural simplification (the case split and one finite lemma go away), not a line saving. Exit code from the desk LOG.md 01:01:32Z. UPDATE 01:21Z: the variant with the old step ban deleted (FiveSupportSwapR1-noV1, desk compile exit 0, 181 s) passes. I compared its 30 `#check` outputs with R1: 30 identical, only `five_support_step_ban` is gone (the desk grep found no other R1 consumer). Measured: 354 → 387 physical lines (+33, excluding the 3-line provenance comment and #check/#print lines), non-blank +26, code lines excluding comments 341 → 350 (+9, desk metric). The earlier +23 estimate is superseded.
- **Provenance:** Architecture swarm smwh11dth (m1 swap, m5 referee); research desk R1 port and compile 00:40Z, rerun after the power loss 00:55–01:01Z.
- **Correction history:** the swarm file targets encoding-r4 and fails on R1 (palette_neighbor_* redeclared; `strict_state_no_unit_support` unknown, removed by R1); the desk ported it; the "21→15 lines" figure is the proof body only; with the helper lemmas and docstrings the module grows; line estimate after deleting v1: about +23 (results desk, 01:05Z), measured +33 (01:21Z)
- **Depends on:** [STEPBAN-V2](#stepban-v2), [STEPBAN-CONSUMER](#stepban-consumer), [R1](#r1)
- **Caveats:** m4 branch-free `hdis` reconstruction (FiveSupport:205–216) is NOT in this port; still a swarm candidate. Not yet substituted into the tree or re-checked against downstream modules.

### JOINT-SUPPORT

**Joint-pair support theorem (generic finite contact-ban support)** — `LEAN_VERIFIED`

- **Statement:** A generic finite contact-ban support theorem, and an unchanged-statement replacement of `five_support_no_sixty` that removes the strict-state-sequence call from this branch.
- **Hypotheses:** Uses existing `stateSupport_shift_relation`; retains manuscript Lemma 6.7 (step ban) and upstream analysis.
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; two statements, [propext, Classical.choice, Quot.sound]; log joint-pair-support-v2.log.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/joint-support/JointPairSupport.lean` — source — `9a904d4d7165889a…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/joint-support/VALIDATION.txt` — validation — `036a3daf10b6e42d…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-REBOOT-REFEREE.txt` — paper referee ("ACCEPT the finite pair-support theorem and its proposed application") — `ceab2e0167e9fc5d…`
- **Checked by the results desk:** Hash recomputed at build; referee quote confirmed verbatim. Did not recompile.
- **Provenance:** Astra joint lead derivation, independent Astra referee + OS review; Codex local validation (before 18:39Z snapshot).
- **Caveats:** Standalone; NOT integrated, by decision of the simplification desk: after R1, five_support_no_sixty is 8 lines and the joint-pair route is 41 (+33), and fixed_state_no_unit_three_centres stays live via Interfaces:278 (simplification-desk/jointpair/JOINT-PAIR-DECISION.md). Not validated against the competition 4.35 target.

### R1

**Three-centre integration (threecentre-r1): old strict-state branch replaced by AvoidingTrace** — `LEAN_VERIFIED`

- **Statement:** The 27 affected modules of the supplied proof, with the three-centre argument routed through the new module `AvoidingTrace` (`fixed_state_no_unit_three_centres`, `strict_state_sequence_no_unit_three_centres`), all compile, and the nine root theorems (as in ENC-R4) depend only on standard axioms. Net −24 physical lines: States 764→566 (−198), FourContinuity 551→509 (−42), FiveSupport 376→354 (−22), Interfaces 527→528 (+1), AvoidingTrace new (+237).
- **Hypotheses:** Statements of the supplied root theorems unchanged. Baseline oleans for unaffected modules (incl. PaletteTransport) are copied from encoding-r4 ("copiedBaselineOleansNotValidation": true).
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; modules 01–14 logs and 15–27 progress records all exit 0; axiomroots job: 9 roots [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/threecentre-r1/frozen-manifest.json` — frozen manifest (27 modules) — `a480c6759658b5a5…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/threecentre-r1/line-accounting.json` — line accounting — `e1dc97d513cca049…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/threecentre-r1/src/AxiomRoots.lean` — root axiom file — `cac851851383970f…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/threecentre-r1-axiomroots.progress.json` — root axiom job record (exit 0) — `ca4b961283a98933…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/threecentre-r1-axiomroots.python.log` — root axiom log — `85aaef1671d5777e…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/threecentre-r1-27-transfer.progress.json` — last module job record (exit 0) — `f0bf78d3b7b482a7…`
  - `I/work/lean-queue/threecentre-r1-05-avoidingtrace.log` — AvoidingTrace log with axioms — `144a25e58697f00d…`
- **Checked by the results desk:** 2026-11-15 ~00:00Z: recomputed SHA-256 of all 27 frozen sources — 27/27 match frozen-manifest.json; module logs 01–14 carry matching "Source SHA256" and "Exit code: 0"; progress records 15–27 have exitCode 0 and sourceSha256 equal to the manifest; axiomroots log prints 9 roots, all [propext, Classical.choice, Quot.sound], no sorryAx; recounted physical lines of the five changed files against encoding-r4/src — matches line-accounting.json exactly (−24). PaletteTransport.lean in the R1 tree is byte-identical to encoding-r4 (same SHA-256), so its absence from the frozen manifest is a manifest gap, not an unverified change. The workspace R1 sources equal the repo snapshot copies (404 files compared, 0 differ). Did not recompile.
- **Provenance:** Lean queue jobs threecentre-r1-01…27 and -axiomroots, 2026-11-14 ~19:00–20:48Z; accepted by Jarom in the research-desk chat ~23:25Z (research-desk LOG.md 23:25:36Z).
- **Correction history:** alternative metrics (simplification desk recount, r1-gates/line-accounting-r1-desk.json): physical −24 (matches), non-blank −41, code excluding comments −67; the ledger quotes the physical count; a private packet claim of "net −66" was rejected (it omitted 236 new-module lines); the accepted accounting is net −24 (check-ins 17:20:56Z, 18:15:21Z); optional further 104 unused-helper lines pending a separate build (check-in 18:35:22Z); Module 15 (Sectors) first .log run did not pass; re-run via the Python runner passed 20:32Z (sectors.progress.json); PROGRESS.md (snapshot 18:39Z) said "full consumer integration and deletion of the old branch remain pending"; R1 is that integration and is now accepted
- **Used for:** Formal baseline pin for every later queue job (StepBan, A6 bridge, EvenWalk import R1 oleans).
- **Depends on:** [ENC-R4](#enc-r4), [THREE-CENTRE](#three-centre)
- **Caveats:** Contract and dependency gates now PASS (see [R1-GATES](#r1-gates), whole-closure signature comparison with R4). PaletteTransport is absent from frozen-manifest.json only because it is an unchanged baseline module (byte-identical source and olean to R4); manifest completeness passed.

### S1

**S1: delete 25 unreachable declarations and make the step ban branch-free in place (−265 physical lines on top of R1)** — `LEAN_VERIFIED`

- **Statement:** On top of the accepted R1 tree: 25 declarations unreachable from every root are deleted (e.g. States varying_pullback_L1, near_identity_circle_in, circleEndpoint_identity_neighborhood; BoundaryTrace unit_antipodes_of_no_positive, four_split_antipodes; CyclicCore cyclicCore_closed), `five_forced_label` is replaced by `five_state_forced_label`, and `five_support_step_ban` is rewritten branch-free under its original name; empty sections removed. 14 files change: States 566→461, BoundaryTrace 367→313, CyclicCore 280→256, FiveSupport 354→337, ContinuumLimits 353→337, Interfaces 528→517, DiskExtension 611→603, AngularBoundary 503→497, FourContinuity 509→503, GraphRealization 415→410, HoleApproximation 328→323, GraphCuts 314→310, Exclusion 165→163, Sectors 453→451: net −265 physical (−255 code).
- **Hypotheses:** Every remaining declaration keeps its exact statement (claimed and, from the signature tables, confirmed for 3,094 declarations incl. five_support_step_ban, no_proper_five_coloring, five_opposite_contacts_false).
- **Evidence:** Re-verification (simplification desk, Lean 4.34.1 / Mathlib d13f23b): fresh 27-module closure build in s1/build-r2, logs s1/logs-r2/01–27 all exit 0; s1/logs-r2/axiomroots-s1-r2.log exit 0, 14 roots [propext, Classical.choice, Quot.sound], no sorryAx; s1/logs-r2/sigdump-s1-r2.log exit 0, writing s1/sigs-s1-r2.tsv: 3,094 common declarations unchanged vs R1, 28 removed (26 named + 2 auto equation lemmas, all absent), 1 added (five_state_forced_label). The 14 roots: the 6 spectral roots, no_proper_five_coloring, no_measurable_weak_five_coloring, no_proper_five_coloring_algebraic, properColoring_seven, weakMeasurableColoring_seven, five_support_step_ban, five_state_forced_label, five_opposite_contacts_false.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/MANIFEST.md` — S1 manifest (claim, per-file sha256, expected gate outputs) — `c076468610b1f1cf…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/BANKED-S1.json` — banked record — `cb03beb06da77f37…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/line-accounting-s1.json` — per-file line accounting — `79162e51db570a51…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/dead-deletions.json` — deleted declarations — `bf403ef34c40414d…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/logs/01-States.log` — first module compile log (exit 0) — `dd82f0b2a9712e70…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/logs/27-Transfer.log` — last module compile log (exit 0) — `4909e50f091fccfa…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/sigs-s1.tsv` — S1 signature table — `8a93cff3eedb4fa3…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/logs-r2/axiomroots-s1-r2.log` — root-axiom log, re-verification (exit 0, 14 roots standard) — `02c2e87433f6b37d…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/logs-r2/sigdump-s1-r2.log` — signature-dump log, re-verification (exit 0) — `5fc63e23754384e4…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/sigs-s1-r2.tsv` — S1 signature table (re-verification) — `8a93cff3eedb4fa3…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/logs/axiomroots.STALE-RUN-0201Z-failed.log` — superseded: failed stray rerun (exit 1) — `522675612c257677…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s1/logs/sigdump-s1.STALE-RUN-0201Z-failed.log` — superseded: failed stray rerun (exit 1) — `6eed4e4eafb7e29b…`
- **Checked by the results desk:** 2026-11-15 ~02:50Z. PASSED: (1) the 14 S1 sources hash to the sha256 values in BANKED-S1.json and their physical line counts recount to exactly −265; the other 13 closure modules are byte-identical to R1. (2) All 27 module logs show exit 0, no error or sorry, and a logged sha256 equal to the current S1 source. (3) Comparing sigs-s1.tsv with sigs-r1.tsv myself: 3,094 common declarations identical in kind, levels, type hash, binder flags and value hash; 28 removed (26 intended + 2 auto-generated equation lemmas); 1 added (five_state_forced_label). NOT ON FILE: logs/axiomroots.log (started 02:01:31Z), logs/sigdump-s1.log (02:02:04Z) and logs/deadaudit14-s1.log all record exit 1 "unknown module prefix OAI", i.e. reruns after s1/build was deleted; they overwrote any passing runs. So the root-axiom print for S1 has no surviving evidence, and the provenance of sigs-s1.tsv (written 02:01:18Z) has no passing log. Requested from the simplification desk, which confirmed the incident (a surviving inner shell of a stopped chain re-ran the gates after s1/build was deleted, 02:45:47Z), downgraded S1 to CANDIDATE itself and queued s1_reverify. Status stays CANDIDATE until passing axiom-root and signature-dump logs are archived. UPGRADE ~04:00Z after the re-verification: all 27 logs in s1/logs-r2/ show exit 0, no error or sorry, and a logged sha256 equal to the current S1 source; axiomroots-s1-r2.log (started 03:41:05Z) exit 0 with 14 roots, all standard; sigdump-s1-r2.log (03:43:12Z) exit 0; my comparison of sigs-s1-r2.tsv with sigs-r1.tsv: 3,094 common, 0 differing, 28 removed, 1 added (five_state_forced_label); sigs-s1-r2.tsv is byte-identical to the earlier sigs-s1.tsv. S1 MANIFEST.md sha256 c0764686…. Status LEAN_VERIFIED.
- **Provenance:** Simplification desk, 00:38–02:01Z (s1/, LOG.md "S1 BANKED" 02:01:43Z).
- **Correction history:** CANDIDATE 02:50–04:00Z: the first passing axiom/sigdump logs were overwritten by a stray failed rerun; regenerated under new names (logs-r2) and checked
- **Used for:** Brings the realised simplification to −415 lines vs the supplied original (ENC-R4 −126, R1 −24, S1 −265); −463 code lines.
- **Depends on:** [R1](#r1), [R1-GATES](#r1-gates), [STEPBAN-V3](#stepban-v3)

### S2

**S2: S1 plus 52 more unreachable declarations deleted outside the R1 closure (−717 physical lines vs R1; −867 vs the supplied original)** — `LEAN_VERIFIED`

- **Statement:** Cumulative on S1: 52 further declarations that no root theorem reaches are deleted from 27 modules outside the R1 closure (spectral, compact-factor and palette layers), each with any `omit/include .. in` prefix. 41 files change versus R1 (e.g. PhaseCollision 537→471, InvariantMean 1078→1031, Compactness 379→353); in total 77 unreachable declarations plus `five_forced_label` are removed and `five_state_forced_label` is added. Net −717 physical lines versus R1; −867 versus the supplied original (manifest of 03:39Z).
- **Hypotheses:** Every surviving declaration keeps its exact statement (signature gate below).
- **Evidence:** Simplification desk (run by the research desk), Lean 4.34.1 / Mathlib d13f23b, one Lean at a time: 67/67 module rebuild exit 0 (s2/logs/01–67, each logging the current source sha256); axiomroots-s2.log exit 0, 14/14 roots on [propext, Classical.choice, Quot.sound], no sorryAx; sigdump-s2.log exit 0 writing sigs-s2.tsv: 3,038 common declarations vs R1, 1 added (five_state_forced_label), 84 removed (the deletions, five_forced_label, auto eq/congr lemmas). The dump flagged 4 value-hash differences in RelativeProducts (Family.avg, Family.l2Linear, Family.toL2, pairSequence); AuxCheck.lean (compiled against both builds) shows identical types, identical normalised values and identical aux-proof type multisets: only the auto-generated _proof_N constants are renamed (they were named after the deleted projectCLM). Two Open Math lanes grep-reviewed the deletions (L-S3 36/36 PASS; L-S1 47 PASS, 5 conditional, 0 FAIL).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/MANIFEST.md` — S2 manifest (claim, per-file sha256, expected gate outputs) — `c6316d7dd9e60952…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/line-accounting-s2-vs-r1.json` — line accounting vs R1 — `e9755b05fdd423ef…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/line-accounting-s2-vs-s1.json` — line accounting vs S1 — `49f95959fef349ec…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/dead-deletions.json` — deleted declarations — `9c25a6e0604a51a1…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/changed-modules.txt` — the 41 changed modules — `b536c876c4733000…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/logs/axiomroots-s2.log` — root-axiom log (exit 0, 14 roots standard) — `b01833ec872ccabb…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/logs/sigdump-s2.log` — signature-dump log (exit 0) — `11ee8fc62f59bba5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/sigs-s2.tsv` — S2 signature table — `44bdbeea5d12cf9f…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/AUXCHECK-NOTE.md` — aux-name rename analysis of the 4 value-hash differences — `233c5a30deeb671a…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/AuxCheck.lean` — aux check source — `7c6a12adae47dbf7…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/auxcheck-s2.log` — aux check vs S2 build — `8e05f1ca231fe9d2…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/auxcheck-r1.log` — aux check vs R1 build — `3d5ac560d832dd46…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/logs/01-WeakColoring.log` — first module compile log (exit 0) — `dd083ec889c1078d…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/s2/logs/67-Transfer.log` — last module compile log (exit 0) — `d02888c1aac9da08…`
- **Checked by the results desk:** 2026-11-15 ~03:45Z, on the CORRECTED tree: the 41 changed S2 sources hash to the sha256 values in the 03:39Z MANIFEST.md; their physical lines recount to exactly −717 against the R1 tree; still 41 changed files (changed-modules.txt equals the manifest set); the other 42 S2 modules are byte-identical to R1. (The earlier 03:30Z recount of −727 matched the previous manifest.) ~05:40Z (exposition desk, ledger owner): re-ran verify_s2.py (41 manifest rows hash-match, recount −717 vs R1, 42 other modules byte-identical to R1); verify_s2_gates.py: all 67 module logs end with `exit 0` and contain no error; axiomroots 14 roots all standard, no sorryAx; sigs-s2.tsv vs sigs-r1.tsv: 3,038 common, 1 added, 84 removed, 5 rows differ: the 4 RelativeProducts value hashes (explained by AUXCHECK-NOTE; aux logs read, not re-run) and palette.congr_simp, an auto-generated congruence lemma whose type hash and binder flags are identical and only its recorded module moved (PaletteDensity → BinaryPalettes). 0 substantive statement changes.
- **Provenance:** Simplification desk, 01:32–03:12Z (s2/, LOG.md; manifest generated 03:12Z).
- **Correction history:** ~03:40Z: an Open Math review (lane L-S3) found two S2 deletions still referenced by qualified name in simp lists; the simplification desk restored them: 55 → 52 deletions beyond S1, −727 → −717 vs R1 (−877 → −867 vs the original); carried into the ledger by the supervisor (commit 49f745d) and recounted by the results desk; attempt 1 failed (12/67 modules) on a dangling omit prefix; logs kept in s2/logs-attempt1-failed-omit-prefix/
- **Used for:** Brings the realised simplification to −867 lines vs the supplied original (ENC-R4 −126, R1 −24, S1 −265, S2 −452 beyond S1); code lines −908.
- **Depends on:** [S1](#s1)

### STEPBAN-CONSUMER

**Consumer `five_opposite_contacts_false_from_v2` rebuilt on the v2 step ban** — `LEAN_VERIFIED`

- **Statement:** Same statement as `five_opposite_contacts_false`: for a weak measurable 5-colouring and a FiveCenter x, if b = a + 3·60°, a ∈ fiveSupport i ∩ fiveSupport (i+1) and b ∈ fiveSupport j ∩ fiveSupport (j+1), then False.
- **Hypotheses:** Identical telescope to the original consumer (verified from the `#check` output).
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; job claude-lean-20261114t232057-0 exit 0, 58.6 s; both `_v2` declarations [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-admissions/claude-lean-20261114t232057-0/Candidate.lean` — source — `718b581518b553c4…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t232057-0.progress.json` — job record — `03d7116c943d8a29…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t232057-0.python.log` — compile log with #check pairs and #print axioms — `a8886d567be5d8d8…`
- **Checked by the results desk:** Recomputed source hash = record; exit 0; read the log: both `#check` pairs (v1 vs `_v2`, consumer vs `_from_v2`) print identical signatures apart from the name; both axiom lines are the standard three. This answers the coordinator's needs_parent of cycle 232732.
- **Provenance:** Architecture lane StepBanConsumer.lean (270 lines, 3-line diff claimed); coordinator cycle 232057; finished 23:23:27Z.
- **Used for:** Unlocks the in-place same-name swap ([STEPBAN-SWAP](#stepban-swap)).
- **Depends on:** [STEPBAN-V2](#stepban-v2)

### STEPBAN-CYCLICCORE

**CyclicCore consumer `five_sequence_small_no_accumulation` rerouted through the v2 step ban** — `LEAN_VERIFIED`

- **Statement:** `five_sequence_small_no_accumulation_from_v2`: for measurable `c : ℂ → Fin 5` with `WeakColoring 5 c`, FiveCenters `yn n` converging to a FiveCenter x with `yn n ≠ x` and `‖yn n − x‖ < 2` for all n: False. Same statement as the CyclicCore original, proved through `five_support_step_ban_v2`.
- **Hypotheses:** Identical telescope to `five_sequence_small_no_accumulation` (the `#check` pair in the log prints the same type).
- **Evidence:** Desk compile exit 0, 122 s; `_from_v2` [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/CyclicCore-r2/CyclicCoreConsumerFromV2-r2.lean` — source (inbox file minus the stray backslash line 1; LF sha256 884ed9bc… as in desk BANKED.md) — `1212d4e1825c0b65…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/CyclicCore-r2/compile.log` — compile log with #check pair and #print axioms — `b90e12cf06aa5cf5…`
- **Checked by the results desk:** Read compile.log: the two `#check` outputs are character-identical apart from the name; one axiom line, standard three. Exit code from desk LOG.md 00:34:32Z.
- **Provenance:** Architecture lane CyclicCoreConsumerFromV2 (queue job 001551-0 failed on a staging defect); research desk r2 compile 00:32–00:34Z.
- **Correction history:** queue job 001551-0 failed only because the staged text began with a stray backslash
- **Depends on:** [STEPBAN-V2](#stepban-v2), [STEPBAN-CONSUMER](#stepban-consumer)

### STEPBAN-SWAP

**Branch-free step ban in the integrated tree (achieved by S1, with the v3 proof)** — `LEAN_VERIFIED`

- **Statement:** The integrated tree now proves Lemma 6.7 `five_support_step_ban` branch-free under its original name and statement, `five_forced_label` is gone, the downstream closure is rebuilt and the roots re-checked. This was done by S1 using the simplification desk v3 proof (shorter), not by substituting FiveSupportSwapR1 (v2, longer).
- **Checked by the results desk:** See S1.
- **Provenance:** Simplification desk S1, re-verified 03:4xZ.
- **Correction history:** was OPEN (planned as the FiveSupportSwapR1 substitution, +33 lines); superseded by S1 (FiveSupport 354 → 337)
- **Depends on:** [S1](#s1), [STEPBAN-V3](#stepban-v3)

### STEPBAN-V2

**Branch-free step ban `five_support_step_ban_v2`** — `LEAN_VERIFIED`

- **Statement:** For measurable `c : ℂ → Fin 5` with `WeakColoring 5 c`, a `FiveCenter c x`, and `a ∈ fiveSupport c hc x i ∩ fiveSupport c hc x j` with `fiveAdj i j`: for a.e. angle t, the state never steps i→j nor j→i across a 60° shift. Same statement as manuscript Lemma 6.7 `five_support_step_ban`; the proof replaces the two-branch case split by the finite core `five_pair_meet` (label-level `decide` over 625 quadruples).
- **Hypotheses:** Identical telescope to `five_support_step_ban` (desk compared the `#check` output in job 232057-0).
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; job claude-lean-20261114t220720-0 exit 0, 64.6 s, `five_support_step_ban_v2` [propext, Classical.choice, Quot.sound]; duplicate job 222227-0 (same source hash) exit 0, 176.7 s; re-checked in 232057-0.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-admissions/claude-lean-20261114t220720-0/Candidate.lean` — source — `19bffbcd71bed9b8…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t220720-0.progress.json` — job record — `1bd90cc006806f4e…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t220720-0.python.log` — compile log with #print axioms — `d1e054998bdb19b5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t222227-0.progress.json` — duplicate job record (not new evidence) — `f2803e863e1a8530…`
- **Checked by the results desk:** Recomputed source SHA-256 = recorded sourceSha256; exitCode 0; parsed the axiom line from the log; no "declaration uses sorry". Counted the original proof body at FiveSupport.lean:72–92 = 21 lines (claim "21→15" consistent on the v1 side; v2 count not independently measured). `five_forced_label` (Exclusion.lean:26) is used only at FiveSupport.lean:83,85 in the R1 tree, so it becomes deletable after the swap. v2 adds helper lemmas `five_outsider_unique` and `five_pair_meet`, so the net physical-line change after the swap is not yet measured.
- **Provenance:** Architecture lane (m1 `five_pair_meet` route); coordinator cycles 20:40Z–22:28Z; job 220720-0 finished 22:10:43Z (mapping corrected: 220720-0 is StepBanShort-r2, not G1).
- **Correction history:** r1 (job 212205-1) failed: Decidable instance on `fiveAdj` not synthesised, and the log shows sorryAx in the v1 attempt; coordinator cycle 222227 briefly mapped job 220720-0 to G1; corrected by the research desk
- **Used for:** Simplification of the supplied proof (removes a case split and the `five_forced_label` lemma).
- **Depends on:** [R1](#r1)

### STEPBAN-V3

**Simplification desk step ban v3: branch-free, in place under the original name (now part of S1)** — `LEAN_VERIFIED`

- **Statement:** `five_support_step_ban` rewritten in place, branch-free, through one `decide` lemma `five_state_forced_label` (Exclusion; disjunction form `Disjoint p (fiveDiag i) ∨ Disjoint p (fiveDiag j)`) that replaces `five_forced_label`. Same statement as Lemma 6.7.
- **Evidence:** Standalone test r3 (as five_support_step_ban_v3) passed 01:20Z, exit 0, 175.7 s, [propext, Classical.choice, Quot.sound], Expr.equal statement and binder check against five_support_step_ban passed (simplification desk LOG.md). In place, it is part of S1.
- **Checked by the results desk:** The in-place version is LEAN_VERIFIED through S1: five_support_step_ban and five_state_forced_label are among the 14 roots with standard axioms in s1/logs-r2/axiomroots-s1-r2.log, and the five_support_step_ban signature row is identical to R1. The standalone r3 test log itself was not inspected.
- **Provenance:** Simplification desk, stepban/ and s1/.
- **Correction history:** r1 failed (rewrite elaboration), r2 failed (Decidable synthesis), r3 passed
- **Depends on:** [STEPBAN-V2](#stepban-v2)

### THREE-CENTRE

**Fixed and moving three-centre replacement theorems (standalone)** — `LEAN_VERIFIED`

- **Statement:** Replacement proofs of the fixed-state and strict-state-sequence three-centre lemmas whose statements and binder flags match the original States declarations; transitive type/value dependency traversals (51,271 and 61,231 constants) contain none of `strict_state_sequence_local_false`, `strict_state_sequence_false`, `strict_state_no_unit_support` or sorryAx.
- **Hypotheses:** Original statements (header identical after whitespace normalisation).
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; standard axioms; logs three-centre-fixed-v2, three-centre-moving-v4-audit.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/three-centre/MovingThreeCentres.lean` — source — `ee52e7412a673673…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/three-centre/FixedStateThreeCentres.lean` — source — `b812e7222f6a7dd8…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/three-centre/VALIDATION.txt` — validation — `c8f9c937b0001560…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/three-centre/MOVING-VALIDATION.txt` — validation — `9d66237c84b360bf…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-A2-REFEREE.txt` — paper referee ("ACCEPT both principal A2 claims at paper level") — `5adfbe3c70ff3ba2…`
- **Checked by the results desk:** verify-snapshot.mjs (23:50Z) re-checked the MovingThreeCentres hash; referee quote confirmed verbatim. Did not recompile.
- **Provenance:** Astra A2 lead paper proof + independent Astra A2 referee + OS reviews; local Lean queue, check-in 17:20:56Z.
- **Used for:** Integrated into the tree by [R1](#r1) (AvoidingTrace).

### LEMMA67-IDENTITY

**Manuscript Lemma 6.7 is `five_support_step_ban`; it is retained** — `PROVED_PAPER_REVIEWED`

- **Statement:** Manuscript Lemma 6.7 ("A support contact bans an angular step", The Euclidean plane is not five-colorable, 2026-09-23, p.41) is the Lean declaration `FiveSupport.five_support_step_ban`. Any description of the joint-support work as "Lemma 6.7 deleted" is rejected.
- **Evidence:** Source identification; ASTRA-REBOOT-REFEREE confirms.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/checkin-artifacts/20261114T163226Z/MANUSCRIPT-LEMMA67.txt` — manuscript excerpt — `40dc2441cf4c283c…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-REBOOT-REFEREE.txt` — referee — `ceab2e0167e9fc5d…`
- **Provenance:** Check-in 16:32:26Z.
- **Used for:** STEPBAN-V2 re-proves this lemma with the same statement.

### R1-GATES

**R1 contract and dependency gates: PASS (whole-closure signature comparison R4 vs R1; manifest completeness)** — `TESTED_FINITE`

- **Statement:** Every declaration of R1 that also exists in the encoding-r4 baseline (3,116) is identical to it: kind, universe parameters, type hash, nested binder flags and definition-value hash. Two moved module unchanged (palette_neighbor_real, palette_neighbor_disjoint: FiveSupport -> AvoidingTrace). The 8 removed declarations are exactly the strict-state branch (nonparallel_neighborhood, positive_state_support_point, strict_state_no_unit_support, strict_state_sequence_false, strict_state_sequence_local_false, strict_state_uniform_on_compact, support_density_direction, support_density_sequence); the 6 added are exactly the three-centre machinery in AvoidingTrace. frozen-manifest.json is exactly the 27-module downstream closure of the 5 changed files; the other 56 modules (incl. PaletteTransport) are byte-identical to R4.
- **Hypotheses:** Signatures compared by structural Expr hashes produced by the simplification desk tool SigDump.lean (sha256 fdb59798…); a hash collision would be needed to hide a change.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/r1-gates/R1-GATES.md` — gate report — `a5df90aa838611f7…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/r1-gates/sigdump-r4.log` — R4 dump log (exit 0, 185 s) — `496d94c0e5b78ff7…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/r1-gates/sigdump-r1.log` — R1 dump log (exit 0, 94 s) — `405ab9a40ed32a27…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/r1-gates/sigs-r4.tsv` — R4 signature table — `fa93e701a42a680b…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/r1-gates/sigs-r1.tsv` — R1 signature table — `87804fe988c547df…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/r1-gates/sig-compare-r4-r1.json` — desk comparison — `62c8e7ef17fb446e…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/simplification-desk/r1-gates/MANIFEST-COMPLETENESS.md` — manifest completeness note — `5521b496101778f1…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/contracts/ConsumerContracts.lean` — research-desk contract gate source — `a3ea701ab15d29a7…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/contracts/ConsumerContracts-r2.lean` — contract gate r2 source — `5ecda4d6d18c1c3f…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/contracts/compile-r2.log` — contract gate r2 log (exit 0, 75 s; binder/type contracts; axioms standard for 3 consumers and 3 headline roots; checked by the exposition desk ~06:10Z) — `96d620b6f0ebd89c…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/contracts/compile.log` — contract gate log (axioms OK; binder examples failed on missing opens) — `6ee4315e14db61b8…`
- **Checked by the results desk:** 2026-11-15 ~02:50Z: read both dump logs (exit 0) and re-did the comparison myself from the two .tsv tables: 3,124 vs 3,122 names, 3,116 common, 0 differing in kind/levels/type/binders/value, 2 moved, the 8 removed and 6 added exactly as listed. PaletteTransport byte-identity was checked by the results desk earlier. I did not re-run SigDump. Supporting (research desk contracts gate, contracts/compile.log, Lean 4.34.1 on the R1 build): #print axioms gives the standard three for no_proper_five_coloring, properColoring_seven, chromaticNumber_bounds, four_support_sequence_no_unit, interfaceStateSupport_no_unit and five_support_no_sixty (parsed by the results desk); the binder-contract `example`s in that file failed only on missing `open` lines (25 unknown-identifier errors); r2 with one added `open` line is compiling.
- **Provenance:** Simplification desk, 01:13–01:29Z (R1-GATES.md); manifest completeness 00:26Z.
- **Correction history:** was OPEN (caveats recorded with the acceptance of R1 at 23:25Z)
- **Depends on:** [R1](#r1)

## New mathematics

### A6-BRIDGE-R2

**A6 bridge r2: a.e. canonical subpalette, conditional on SignTable, ForcingLemma, ArcCover** — `LEAN_VERIFIED`

- **Statement:** `ae_canonical_subpalette_global`: for measurable `c : ℂ → Fin 6` with `WeakColoring 6 c`, sets `K i` approaching x in directions `v i`, and support exclusion `Disjoint (spatialSupport c j) (Straddle (K i))` for `j ∈ eSet i`, together with `SignTable v`, `ForcingLemma` and `ArcCover`: for angular-a.e. θ there is j with `f j` and `f j + 3` in `palette c hc x θ`. Also `ae_six_inputs`, `ae_restrictions`, `ae_canonical_subpalette` (arc form).
- **Hypotheses:** `hsign : SignTable v`, `hforce : ForcingLemma`, `hcover : ArcCover` are explicit hypotheses in this file (G3 not glued).
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; job claude-lean-20261114t231544-0 exit 0, 66.9 s, linter warnings only, unchanged maxHeartbeats. The job file prints no axioms; the research desk ran a separate `#print axioms` on its olean: 8 endpoints [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-admissions/claude-lean-20261114t231544-0/Candidate.lean` — source — `74402da9ef754964…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t231544-0.progress.json` — job record — `5c7b4cb2f3ff873b…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t231544-0.python.log` — compile log (warnings only) — `bdcc69a00d00bb0e…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/bridge-r2-axioms/Axioms.lean` — desk axiom-print file — `5c94e491337de75d…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/bridge-r2-axioms/axioms.log` — desk axiom log (8 endpoints) — `31893654154de1e6…`
- **Checked by the results desk:** Recomputed source hash = record; exitCode 0; job log has no errors and no axiom lines; read the desk axioms.log: 8 lines, each the standard three. Confirmed in the source that SignTable/ForcingLemma/ArcCover are hypotheses of the global theorem.
- **Provenance:** Formal lane B: swarm smwguinbz A6-Bridge-m2 + smwgwui56 G1-Finish-mB (folded at r2); r2 written by the coordinator; cycle 231544; finished 23:18:26Z; desk axiom check 23:20:56Z.
- **Correction history:** Bridge-m2 (job 213711-0) failed: `ae_restrictions` whnf timeout and a genuine shift-direction bug in the ArcCover composition (must use −sixAngle j); fixed in r2
- **Used for:** Six-colour producer chain (k=6); superseded for callers by A6-BRIDGE-R2-G3.
- **Depends on:** [R1](#r1), [G1-R2](#g1-r2)

### A6-BRIDGE-R2-G3

**A6 bridge with G3 glued: a.e. canonical subpalette with the arc cover discharged** — `LEAN_VERIFIED`

- **Statement:** `ae_canonical_subpalette_unconditional`: for measurable `c : ℂ → Fin 6` with `WeakColoring 6 c`, sets `K i` approaching x in directions `v i` with support exclusions `Disjoint (spatialSupport c j) (Straddle (K i))` for j ∈ eSet i, `SignTable v` and `ForcingLemma`: for angular-a.e. θ there is j with `f j` and `f j + 3` in `palette c hc x θ`. The `ArcCover` hypothesis of A6-BRIDGE-R2 is discharged by the glued G3 proof `arcCover`.
- **Hypotheses:** `hsign : SignTable v` and `hforce : ForcingLemma` remain hypotheses in this file (G1-R2 proves SignTable for paired directions and A6-FORCING proves the finite lemma separately; the single fully glued statement is still A6-GLUE).
- **Evidence:** Desk compile (research desk, same toolchain) exit 0, 167 s, linter warnings only; `ae_canonical_subpalette_unconditional` [propext, Classical.choice, Quot.sound]; no sorry.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/Bridge-r2-G3/A6-Bridge-r2-G3.lean` — source (864 lines; LF sha256 164f26bb…) — `2e04f2115ac3b561…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/Bridge-r2-G3/compile.log` — compile log with #print axioms — `b670399ddedbfdc8…`
- **Checked by the results desk:** Recomputed the source hash (identical to inbox downloads 20261115T001250-3 and 001551-0); read compile.log: warnings only, one axiom line with the standard three. Exit code and runtime are from the desk LOG.md (00:32:22Z), not a queue record. Confirmed in the source that the theorem still takes hsign and hforce.
- **Provenance:** Formal lane L1 (WITH_G3 splice); downloaded 00:12Z; research desk compile 00:29–00:32Z (too large for the coordinator review filter, so not queued).
- **Depends on:** [A6-BRIDGE-R2](#a6-bridge-r2), [G3-R2](#g3-r2)

### A6-FORCING

**A6 finite forcing lemma (hit form), with necessity checks** — `LEAN_VERIFIED`

- **Statement:** `A6Forcing.a6_canonical_pairs_add_three`: for any palettes `P : Fin 6 → Finset (Fin 6)` with an inner hit `(P j ∩ {f j}).Nonempty`, an outer hit `(P j ∩ H j).Nonempty` and cyclic adjacent disjointness `Disjoint (P j) (P (j+1))`, every `P j` contains `f j` and `f j + 3`. Here f = source table, H = ({3,4,5},{1,2,3},{0,1,5},…), g = f+3 = (4,2,0,4,2,0). The same file proves the hypotheses satisfiable (`a6_hypotheses_satisfiable`) and that disjointness and the outer hit are each necessary.
- **Hypotheses:** Purely finite (Mathlib only); no cardinality premise. The link to geometry is via the A6 bridge hypotheses `ForcingLemma` (see A6-GLUE).
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; job claude-lean-20261114t212205-0 exit 0, 62.7 s, empty compiler output.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-admissions/claude-lean-20261114t212205-0/Candidate.lean` — source — `27e45caf4c793897…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t212205-0.progress.json` — job record — `729f92a0cf31b8e5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t212205-0.python.log` — compile log (empty) — `e3b0c44298fc1c14…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/spotcheck/A6Forcing-axioms.lean` — desk spot-check: job source plus #print axioms lines only — `83e6dfa36be80807…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/spotcheck/A6Forcing-axioms.log` — spot-check log: 7 axiom lines — `31518f332044b24f…`
- **Checked by the results desk:** Recomputed source hash = record; exitCode 0; the job log is empty (no sorry warning) because the source has no `#print axioms`. Flag CLOSED 01:20Z: the research desk recompiled the same source with axiom prints appended. I diffed the spot-check file against the job source: the only changes are 8 added `#print` lines. Its log lists 7 endpoints (a6_canonical_pairs, a6_canonical_pairs_add_three, a6_containment_unsatisfiable, a6_hypotheses_satisfiable, disjointness_necessary, outer_hit_necessary, A6canonical_hypotheses), each [propext, Classical.choice, Quot.sound]. Not printed: `a6_canonical_pair_subset` (the research desk notes a non-standard axiom could enter only through its own short body; a queue job would close this).
- **Provenance:** Formal lane A (swarm smwgviqtr m1, "A6-Forcing-m1"); coordinator cycle 212205; finished 21:25:32Z.
- **Correction history:** A6 finite check corrected to "exactly one model P=[{1,4},{2,5},{0,3}]×2, with no cardinality premise" (cycle 204019)
- **Used for:** Discharges `ForcingLemma` in the A6 bridge once glued; it is the finite core of A6-PAIRED-PRODUCER.
- **Caveats:** `a6_canonical_pair_subset` has no printed axiom list (the other 7 endpoints do).

### A6-GLUE

**Glued A6 endgame (A6-Bridge-v4-r2): SignTable, ForcingLemma and ArcCover discharged in one compiled file; two named hypotheses remain** — `LEAN_VERIFIED`

- **Statement:** `no_six_paired_interfaces_of_arcCover`: assuming the named Prop `A5Obstruction` (no measurable WeakColoring 6 has, at any centre, a palette carrying the canonical pairs a.e.), for every measurable `c : ℂ → Fin 6` with `WeakColoring 6 c`, six `ApproachingContinuum x (K i) (v i)` in the exact paired directions (`A6Pairing v`) and support exclusions `hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i))`: False. Inside the file ForcingLemma is proved (`forcingLemma_proof`), SignTable follows from `A6Pairing`, and ArcCover is the G3 `arcCover`; also `ae_palette_eq_pair_unconditional` (the palette is exactly {f j, f j+3} a.e.) and `ae_canonical_subpalette_unconditional`.
- **Hypotheses:** Two named hypotheses are NOT discharged in Lean: `A5Obstruction` (supported by the refereed paper result A5-FOUR-LIST and the A5-SLIVER interval certificate; no Lean declaration) and `hsupp` (the support-exclusion data, an input; Hsupp-r2 gives only equivalent reformulations). Exact three-fold pairing only (R1-4 referee C1).
- **Evidence:** Research desk desk compile (desk_lean, Lean 4.34.1 / Mathlib d13f23b, on R1): A6-Bridge-v4-r2.lean (formal-lane v4 minus one redundant `decide`), exit 0, 53 s; `#print axioms` standard-only for no_six_paired_interfaces_of_arcCover, ae_palette_eq_pair_unconditional, ae_canonical_subpalette_unconditional.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/Bridge-v4/A6-Bridge-v4-r2.lean` — glued bridge source — `74759b093f94e622…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/Bridge-v4/compile-r2.log` — compile log with #print axioms (exit 0) — `721cfe4bd5298ad5…`
- **Checked by the results desk:** ~06:10Z (exposition desk, ledger owner): source sha256 matches BANKED.md and the log header; log `exit 0`; the 3 printed axiom lists are exactly [propext, Classical.choice, Quot.sound]; no sorryAx in the log; the 3 textual hits for sorry/admit in the source are comments; read the endgame theorem statement and the `A5Obstruction` definition (lines 1167–1190, 1301–1317). Not recompiled.
- **Provenance:** Formal lane L1 (v4) + research desk (r2 fix and compile), ~05:50–06:05Z; earlier A6-Bridge-r2-G3 (00:32Z).
- **Used for:** In Lean, the A6 six-colour endgame reduces to two named inputs: the A5 obstruction and the support exclusions.
- **Depends on:** [A6-BRIDGE-R2-G3](#a6-bridge-r2-g3), [A6-BRIDGE-R2](#a6-bridge-r2), [G1-R2](#g1-r2), [G3-R2](#g3-r2), [A6-FORCING](#a6-forcing), [A5-FOUR-LIST](#a5-four-list)

### CC60

**Closed 60° cone obstruction (CC60), equality case included** — `LEAN_VERIFIED`

- **Statement:** `closed60_exclusions_three_le`: for a weak measurable colouring, a finite family of actual common-exclusion continua approaching one centre with signed directions in a closed cone of width ≤ 60° cannot leave only two labels — at least three labels remain. Also `outer120_binary_impossible`. Rules out q=(0,0,1,3,3,4).
- **Hypotheses:** Same-centre approaching-continuum and support-exclusion hypotheses as stated in ConeObstruction.lean; no palette-size premise.
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; ConeGeometry v2, ConeObstruction v3, ConeSurvivor v4 (concrete six-colour consumer) and ConeAudit v3 all exit 0; four audited declarations [propext, Classical.choice, Quot.sound]; no sorryAx.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/cone/VALIDATION.json` — validation manifest — `37bf7b83026d665e…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/cone/ConeObstruction.lean` — source — `41298784d3226ccd…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/cone/ConeGeometry.lean` — source — `12c254d0520f7623…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/cone/ConeSurvivor.lean` — source — `527c74754eaa73c9…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/cone/cone-audit-v3.log` — axiom audit log — `15e9426040492af5…`
- **Checked by the results desk:** verify-snapshot.mjs (23:50Z) re-checked all cone source hashes against VALIDATION.json, the audit log status, exit 0, absence of sorryAx and four axiom lines. Did not recompile.
- **Provenance:** Paper theorem in ASTRA-NONALIGNED-A3 with independent ASTRA-CONE-REFEREE; formalised in ASTRA-CONE-FORMAL-A4; Lean queue ~09:56–10:12 Pacific (17:56–18:12Z) 2026-11-14.
- **Correction history:** old AC-axis mixed inner/outer proof rejected (check-in 17:20:56Z)
- **Used for:** Filters the discrete direction grid 174→6 ([DIR-FILTER](#dir-filter)); local obstruction only — not a plane-colouring result.

### CONNECTED-SET

**Connected unit-free sets: no straddling, pairwise distance < 1, diameter ≤ 1 (sharp)** — `LEAN_VERIFIED`

- **Statement:** `unitFree_not_straddle`, `unitFree_pairwise_lt`, `diam_le_one_of_preconnected_unitFree'`: a preconnected set in a normed group with no unit-distance pair cannot straddle the unit sphere about any of its points, has all pairwise distances < 1, and has diameter ≤ 1; `unitFree_sharp` shows diameter 1 is attained (pairwise < 1 permits diameter = 1). Plus the IVT helper `preconnected_forall_lt_or_forall_gt`.
- **Evidence:** connected-set-minimal.log: Lean 4.34.1, exit 0, five theorems [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/ConnectedSetExclusionMinimal.lean` — source — `c243da2d52bba6b2…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/connected-set-minimal.log` — compile log — `50b627e36e23c2e8…`
- **Checked by the results desk:** Read the archived log: Version 4.34.1, "Status: passed", "Exit code: 0", logged Source SHA256 equals the archived source (hash recomputed), axiom lines parsed. Did not recompile.
- **Provenance:** Overnight 13–14 Nov.
- **Correction history:** a first narrowed-import local attempt failed (missing ContinuousSub instance, sorryAx); superseded by the minimal version

### EVENWALK-R6

**Even unit-distance walks: reachability and finite list / parity obstructions** — `LEAN_VERIFIED`

- **Statement:** `evenWalk_reachable`: if W ⊆ ℂ is open, T ⊆ W connected and every point of T has a unit neighbour in W, any two points of T are joined by a finite even-length unit-distance walk in W. `finite_list_obstruction`: for a weak measurable k-colouring, a finite unit-distance pattern whose vertices carry lists of full density (`ListDensity`) and which has no list-respecting proper colouring is impossible. `two_list_obstruction_of_even_walk`: an even unit walk whose vertices are all density-one points of the same ≤2-element list cannot have endpoints at unit distance.
- **Hypotheses:** `Measurable c`, `WeakColoring k c`; density hypotheses as stated; imports R1 `Rigidity` and `States`.
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; desk compile exit 0, 63 s; three endpoints [propext, Classical.choice, Quot.sound]; deprecation/linter warnings only.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/EvenWalk-rev6/EvenWalkReachability-rev6.lean` — source — `4439cf5dd4088ea6…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/EvenWalk-rev6/compile.log` — compile log with #print axioms — `23bc2c29a2846046…`
- **Checked by the results desk:** Recomputed source hash = BANKED.md value; read compile.log: three standard axiom lines, warnings only, no errors. Exit code from desk LOG.md 23:27:27Z.
- **Provenance:** Verifier lane (swarm smwguidy9 → smwgzthki); rev6 = rev5 + one `show` line before `rw [he]` at L90, research desk 23:26Z.
- **Correction history:** rev1 job 205744-0 failed (28 errors); rev2 job 215215-0 failed (13 errors); rev3 job 222600-0 failed (5 errors); rev4 failed (min-clamp motive); rev5 job 232057-1 failed (1 error); superseded by rev6
- **Used for:** A5 consumer chain (finite list obstructions for k=6).
- **Depends on:** [R1](#r1)

### G1-R2

**G1: strict cosine sign table and `SignTable` from paired directions** — `LEAN_VERIFIED`

- **Statement:** `cos_sign_strict`: for |s| < π/6 and m : ℕ, cos(s + m·π/3) > 0 iff m mod 6 ∈ {0,1,5}, and < 0 iff m mod 6 ∈ {2,3,4}. `signTable_of_paired`: if `v i = direction (sixAngle (k i))` with `(k i).val = 2·(i.val/2)`, then `SignTable v`.
- **Hypotheses:** As stated (pure trigonometry plus the bridge definitions).
- **Evidence:** Compiled inside A6-BRIDGE-R2 (job 231544-0); desk axiom log lists cos_sign_strict, sign_of_paired_fin, signTable_of_paired, signTable_of_paired_fin with standard axioms.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-admissions/claude-lean-20261114t231544-0/Candidate.lean` — source (§9) — `74402da9ef754964…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/bridge-r2-axioms/axioms.log` — desk axiom log — `31893654154de1e6…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/G1-r2/G1-Finish-mB-r2.lean` — standalone source — `fd3549e5acccd7b5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/G1-r2/compile.log` — standalone compile log — `fbf7d62384b9f62c…`
- **Checked by the results desk:** As A6-BRIDGE-R2; also read the standalone desk compile.log (23:49Z, 100 s): linter warnings only; cos_sign_strict, sign_of_paired_fin, signTableT_of_paired, signTableT_of_paired_fin with the standard three axioms.
- **Provenance:** G1-Finish-mB (swarm smwgwui56), r2 with the `m % 6 < 6` bound before interval_cases.
- **Correction history:** G1-Sign-m2 withdrawn as defective (missing Interfaces import, free-binder decide) — cycle 213711; G1-Finish-mB r1 (job 215215-1) failed on a missing `m%6<6` bound; G1-r2 was first banked only through the bridge; a standalone desk compile (G1-Finish-mB-r2, mB plus the hm6 line from the bridge) passed 23:49Z
- **Used for:** Discharges `SignTable` in the A6 bridge for paired directions.

### G3-R2

**G3: six translates of the open fundamental arc cover the circle a.e.** — `LEAN_VERIFIED`

- **Statement:** `arcCover : ∀ᵐ θ ∂angularMeasure, ∃ t ∈ arc, ∃ j : Fin 6, θ = t + sixAngle j` (the bridge's `ArcCover`); the exceptional set is the six points π/6 + m·60°.
- **Hypotheses:** None beyond the definitions (Mathlib only, verbatim local copies of Angles/angularMeasure/sixty/sixAngle).
- **Evidence:** Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; desk compile (not a queue job) exit 0, 83 s; `arcCover` [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/G3-r2/G3-ArcCover-r2.lean` — source — `39a02e68c878c0d0…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/G3-r2/compile.log` — compile log with #print axioms — `e1a47fad00213af7…`
- **Checked by the results desk:** Recomputed source hash = BANKED.md value; read compile.log: one axiom line, standard three, no errors. Exit code is from the desk LOG.md (22:32:04Z), not from a queue record.
- **Provenance:** Formal lane mA (G3-ArcCover-mA, inbox 20261114T215215-download-2); research desk r2 22:30Z (le_or_lt→le_or_gt at L160, L168).
- **Correction history:** G3 standalone r1 (job 220720-1) failed only on removed `le_or_lt`
- **Used for:** Discharges `ArcCover` once glued ([A6-GLUE](#a6-glue)).

### NULL-TRANSFER

**Proper colouring off a null set gives a global proper colouring** — `LEAN_VERIFIED`

- **Statement:** `exists_properColoring_of_compl_null`: for k > 0, a set Z ⊆ ℂ with volume Z = 0 and any c : ℂ → Fin k that is proper on unit pairs outside Z, there is some proper k-colouring d of ℂ (no agreement with c promised).
- **Hypotheses:** `[NeZero k]`, `volume Z = 0`, properness of c off Z.
- **Evidence:** k-generic-transfer-v1.log: Lean 4.34.1, exit 0, [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/encoding-r4/src/KGenericTransfer.lean` — source — `8a8fc2cb095321cd…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/k-generic-transfer-v1.log` — compile log — `3e1d15f3b1fb548d…`
- **Checked by the results desk:** Read the archived log: Version 4.34.1, "Status: passed", "Exit code: 0", logged Source SHA256 equals the archived source (hash recomputed), axiom lines parsed. Did not recompile.
- **Provenance:** Independent lane; overnight 13–14 Nov (CONSOLIDATED-FINDINGS 02:51).
- **Used for:** General transfer lemma (finite compactness); no bound by itself.

### A5-FOUR-LIST

**The canonical paired palette is excluded at one centre (finite four-list obstruction)** — `PROVED_PAPER_REVIEWED`

- **Statement:** (P) For measurable `c : ℂ → Fin 6` with `WeakColoring 6 c`, no centre x has an actual palette containing the canonical paired palette P(t) = A_(⌊(t+π/6)/(π/3)⌋ mod 3), A0={1,4}, A1={2,5}, A2={0,3}, for a.e. t. (F) The underlying list field L has a finite unit-distance configuration with strict cell margins and no proper L-colouring: two odd walks in rotated H-lobes (lists A1, A2) whose endpoints are unit-adjacent to z0 = i/2 (list A1 ∪ A2), with explicit contacts q− = (−√3/24, (6+√429)/24), q+ = (√3/12, (3+2√33)/12).
- **Hypotheses:** Containment P(t) ⊆ palette a.e. suffices; no palette-cardinality bound. Uses `states_densityOne` and `finite_density_realization` from the supplied source.
- **Evidence:** Paper proof ASTRA-FOUR-LIST-A5; independent referee ASTRA-FOUR-LIST-REFEREE: "ACCEPT the complete candidate … at the mathematical paper level".
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-FOUR-LIST-A5.txt` — paper proof — `799cef0737b23deb…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-FOUR-LIST-REFEREE.txt` — referee (ACCEPT) — `29e3800ecb740d96…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A5 lane with independent referee; check-in 18:35:22Z; RESEARCH-STATUS.
- **Correction history:** contradicts and supersedes Claude05's verdict that "none of the one-centre necessary conditions … excludes this field" (see CLAUDE05-VERDICT)
- **Used for:** Endpoint of the A6 paired-producer route (A6-PAIRED-PRODUCER + A5 ⇒ False).
- **Caveats:** Finite existence only: walk coordinates and vertex count are not enumerated (see A5-ODD-WALK, A5-SLIVER). Not Lean-checked; EVENWALK-R6 now supplies the generic Lean list/parity lemmas but the A5 configuration itself is not formalised. Does not by itself exclude any interface configuration.

### A6-PAIRED-PRODUCER

**A6 paired producer: paired interface directions force the canonical palette (hence False with A5)** — `PROVED_PAPER_REVIEWED`

- **Statement:** For measurable WeakColoring 6, one centre x and six actual `ApproachingContinuum x K_i v_i` with v0=v1=e(0), v2=v3=e(2π/3), v4=v5=e(4π/3) and exclusions E_i={i,i+1}: the OUT/IN hits and `palette_sixty_disjoint` force f=(1,5,3,1,5,3), hit sets ({3,4,5},{1,2,3},{0,1,5})×2 and second labels g=(4,2,0,4,2,0), so the canonical paired palette P ⊆ palette a.e.; with A5-FOUR-LIST this gives False. Extends to common rotations; a colour renaming transports the statement; a reflection is a rotation composed with a renaming (referee C3, C4).
- **Hypotheses:** Actual common-interface hypotheses at one centre with the EXACT three-fold paired direction pattern (referee C1: no neighbourhood or perturbed pairing is covered; the ε > 0 failure is the witness). Hit reading Q_j ∩ T_j ≠ ∅, not containment (C5). Period 180° (C2).
- **Evidence:** Independent adversarial referee (OMM referee lane chat-2345d7f398, swarm smwh90qeq), R1-4-REFEREE: ACCEPT WITH CORRECTIONS. The finite core and the a.e. bridge are correct; the forcing uses no palette-cardinality premise (CHECK-A6.py part F: all 64 subsets allowed, exactly one solution); composition with A5 is modus ponens. Table and forcing recomputed from cosine signs by CHECK-A6.py (sha256 821422505c8abb85863bd9f9977e936834d6df04c7943e36ce4fb178db89a972). Earlier: ASTRA-PAIRED-PRODUCER-A6 audit; parent check of the six-row table. Formal status: the finite core is LEAN_VERIFIED (A6-FORCING) and the a.e. bridge compiles conditionally (A6-BRIDGE-R2); glue open (A6-GLUE).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T045717-download-1-R1-4-REFEREE.md` — independent referee verdict R1-4 (ACCEPT WITH CORRECTIONS) — `15a48005bf7f006d…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-PAIRED-PRODUCER-A6.txt` — paper — `2a7e4aed6b6db4eb…`
- **Checked by the results desk:** Exposition desk (ledger owner) read the referee report in full ~05:05Z; CHECK-A6.py not re-run by the desk. Referee scope: no chromatic-number claim; nothing about unpaired or nearly paired directions or other centres. A5 is taken on the parent statement (A5-FOUR-LIST), with P normalised as period 180°, A_0 on (−30°,30°).
- **Provenance:** Astra A6 lane + parent; check-in 18:35:22Z.
- **Correction history:** formal coordinator claimed "A6 table false" after misreading hit sets as containment; retracted (RESEARCH-STATUS); A6-CONTAINMENT formalises why containment is vacuous
- **Depends on:** [A5-FOUR-LIST](#a5-four-list), [A6-FORCING](#a6-forcing), [A6-BRIDGE-R2](#a6-bridge-r2)

### AC-ALIGNED

**Aligned exclusion (AC): same signed direction leaves at least three labels** — `PROVED_PAPER_REVIEWED`

- **Statement:** For measurable weak `c : ℂ → Fin k`, one centre x, one unit vector v and finitely many K_i with `ApproachingContinuum x K_i v` and `Disjoint (spatialSupport c j) (Straddle K_i)` for j ∈ H_i: if ⋃H_i leaves at most two labels then False. Six-colour consumer: three consecutive cycle edges with a common oriented direction are impossible (kills q=(0,3,3,3,0,0)).
- **Hypotheses:** Same SIGNED direction for every continuum (the unsigned-axis extension is false, see AC-AXIS).
- **Evidence:** ASTRA-SIX-COLOUR-A2 §6; referee ASTRA-AC-REFEREE: "ACCEPT AC at paper level." AC is the zero-width case of the Lean-verified CC60.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-A2.txt` — paper proof — `fb2ad23a7600cde8…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-AC-REFEREE.txt` — referee (ACCEPT) — `56c5d614f875471b…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A2 lane, 2026-11-14 ~09:02Z; check-in 16:53:26Z.

### MC120-STRICT

**Strict MC120: one residual label forbids a cone of aperture < 120°** — `PROVED_PAPER_REVIEWED`

- **Statement:** For actual same-centre continua with support exclusions leaving ≤ 1 residual label, the directions cannot lie in a cone of aperture strictly < 120°. (Table: ≥4 excluded ⇒ ≤60° forbidden (CC60); ≥5 ⇒ <120°; 6 ⇒ <180°.)
- **Evidence:** Independent adversarial referee (OMM referee lane chat-2345d7f398, swarm smwh90qeq), R1-3-REFEREE: ACCEPT WITH CORRECTIONS, no mathematical gap; two swarm members independently confirmed the arc lemma and the input-side/strip audit (referee checks CHECK-120.py, CHECK-ORBIT.py; member checks m2_arc_check.py, m2_threshold_check.py, m1_checks.py). Every hypothesis anchored to the supplied sources (Coloring.lean:27; AngularBoundary.lean:147, :235, :244, :259, :279, :317; Rigidity.lean:171). Earlier: ASTRA-CONTINUOUS-SIX-A4 §4–5; compactness step re-verified in MC120-ENDPOINT-CORRECTION; RESEARCH-STATUS calls it "accepted paper", but no referee verdict file exists; the Lean wrapper (StrictMC120) is uncompiled.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T045717-download-0-R1-3-REFEREE.md` — independent referee verdict R1-3 (ACCEPT WITH CORRECTIONS) — `0b295e593daf9438…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-CONTINUOUS-SIX-A4.txt` — paper — `70a91bc5d72681f2…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/MC120-ENDPOINT-CORRECTION.txt` — parent correction note — `ce20448c29cb9091…`
- **Checked by the results desk:** Exposition desk (ledger owner) read the referee report in full ~05:05Z; referee and member scripts were not re-run by the desk.
- **Provenance:** Astra A4 lane; check-ins 18:15:21Z, 19:18:20Z.
- **Caveats:** Closed 120° is false (MC120-ENDPOINT); the theorem is silent at aperture exactly 120° (referee C6). Finiteness of the family is load-bearing (C6: K_n = {0,(1/n,0)} witness). The span L is the minimal closed arc containing the directions, not the pairwise diameter (C1); the uniform strip needs a closed sub-arc and a finite subcover, since the strip width has no lower bound on the open arc (C2); the empty-residual case J = ∅ is immediate (C3). No Lean build.

### NR-TC

**Null return (NR) and triangle constraint (TC) at one centre** — `PROVED_PAPER_REVIEWED`

- **Statement:** NR: for one centre, |Fin k∖(J∪K)| ≤ 2, RealStates on B̃0 (J) and B̃1 (K) and the τ-swap law (τ=π/3), μ(B0 ∩ (B0−γ)) = μ(B1 ∩ (B1−γ)) = 0 with γ = arccos(5/6). TC: if a finite measurable represented state map satisfies f(t+2τ)=f(t) a.e., then for a.e. t, |Fin k ∖ (L_f(t) ∪ L_f(t+π+γ))| ≥ 3; for 120°-periodic palettes |P(t) ∪ P(t+π+γ)| ≤ k−3 (= 3 at k=6).
- **Hypotheses:** As stated; NR does not give μ(A) = 0.
- **Evidence:** ASTRA-SIX-COLOUR-A2 §1–3; referee ASTRA-AC-REFEREE: "ACCEPT NR and TC as the stated null-return/necessary-condition theorems."
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-A2.txt` — paper proof — `fb2ad23a7600cde8…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-AC-REFEREE.txt` — referee (ACCEPT) — `56c5d614f875471b…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A2 lane, 2026-11-14.
- **Caveats:** Referee notes `Accumulation.palette_eq_measurable` is typed Fin 5 and needs generalisation; use `angle_preimage_positive`.

### RESIDUAL-GRAPH

**Residual-colour graph on Z_K ∩ unit circle** — `PROVED_PAPER_REVIEWED`

- **Statement:** Given a positive J-state at x, every finite unit-distance graph on Z_K ∩ unitCircle(x) is colourable by the residual labels outside J∪K. One residual label excludes unit edges; two give only bipartiteness, which already holds on one unit circle.
- **Evidence:** ASTRA-JOINT-STATE-A2 §6; referee ASTRA-A2-REFEREE §6 (ACCEPT).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-JOINT-STATE-A2.txt` — paper proof — `53bee357f537e799…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-A2-REFEREE.txt` — referee — `5adfbe3c70ff3ba2…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A2 joint lane, 2026-11-14 ~08:57Z.

### SHARPNESS-20

**Generic sharpness above 60°: CC60 cannot be widened for arbitrary finite palettes** — `PROVED_PAPER_REVIEWED`

- **Statement:** An explicit 20-colour construction shows the closed-cone width 60° in CC60 cannot be increased for arbitrary finite palettes.
- **Hypotheses:** Arbitrary finite palette size (20 colours); not a six-colour statement.
- **Evidence:** Construction and novelty audit, plus an independent referee report accepting it.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/scale-up/ULTRA-CONE-NOVELTY-AUDIT.txt` — construction + novelty audit — `40635be5b2a591ef…`
  - `HadwigerNelson/Main/ResearchSnapshot/scale-up/ULTRA-SHARPNESS-REFEREE.txt` — independent referee — `1a91529aec65a9b7…`
- **Checked by the results desk:** Hashes recomputed; referee quote "ACCEPT at the paper-proof level" confirmed. The author file exists only in the repo snapshot (scale-up/), not in the research workspace. Did not re-read the proof.
- **Provenance:** Ultra scale-up lane, 2026-11-14 (before 18:39Z snapshot).
- **Depends on:** [CC60](#cc60)
- **Caveats:** Six-colour sharpness and novelty priority not established.

### STRAIGHT-NEEDLE

**Two straight needles at ±60° always have a common straddling unit pair** — `PROVED_PAPER_REVIEWED`

- **Statement:** K+ = [0, L+·e(π/3)] and K− = [0, L−·e(−π/3)] always admit a common straddling unit pair; explicit witnesses d = t²/(2(t+√3)), z± = (−(√3/2−d), ±1/2).
- **Evidence:** ASTRA-MC120-ENDPOINT-A5 §5; referee ASTRA-MC120-ENDPOINT-REFEREE §7 ("The exact straight-needle contrast is also CORRECT").
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-MC120-ENDPOINT-A5.txt` — paper — `78503d6ee09748ee…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-MC120-ENDPOINT-REFEREE.txt` — referee — `318773a2908246dc…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A5 lane, 2026-11-14.
- **Used for:** Contrast with MC120-ENDPOINT (curved arcs needed).

### A5-SLIVER

**A5 apex exclusion: exact interval certificate over the full domain (including the corner where the bound is attained)** — `TESTED_FINITE`

- **Statement:** Full domain (update 2026-11-15, certify_full.py): for every (u1,u3) in arc1 × arc3 of both blocks B1 and B2, both unit apexes of (v1,v3) lie outside the open region H (all five margins m_lo, m_lo2, m_hi, m_edge, m_floor > 0, block4_check.py:65–75): near each corner by monotonicity (dR/du1 < 0, dR/du3 > 0) and the exact corner identity; elsewhere by 580 exact interval sub-boxes, each with a margin of A1 strictly negative and A2 excluded by m_hi. All 8 arc ends are certified unique roots (certify_arc_ends.py). Earlier piece: on the three pieces P1, P2, P3 left uncovered by the F5 exclusion boxes in arc1 × arc3, the quantity R = (1 − |D|²/4)·D_x² − |D|²·Δ² is ≥ 0, so the lower apex A1 has m_floor(A1) ≤ 0 and lies outside the open region H; equality only at the exact corner, where the apex is ci ∈ ∂H.
- **Hypotheses:** The one stated assumption is the reading of the claim (both unit apexes lie outside the open H) with the quoted margin definitions. The earlier dependencies (complement exactly P1 ∪ P2 ∪ P3; the 1,469 + 889 F5 boxes certified elsewhere; unverified non-corner arc ends) are superseded: the full-domain certificate re-derives C2 and certifies all arc ends.
- **Evidence:** certify_full.py (exact Fraction intervals, outward rounding 2⁻¹²⁰, √ constants by isqrt, no floats in any decision; "ALL BLOCKS CERTIFIED: True") and certify_arc_ends.py ("ALL ARC ENDS CERTIFIED: True"). Earlier: certify_sliver.py: exact Fraction intervals rounded outward to 2⁻¹²⁰, interval forward-mode derivatives, rational trig parametrisation; 0.4 s, "ALL PIECES CERTIFIED: True".
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/CERTIFICATE.md` — certificate write-up — `d09708787fbe0e41…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/certify_sliver.py` — certifier — `63e84a36bfa95ea9…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/certificate_output.txt` — output — `68507c241873c543…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/certify_full.py` — full-domain certifier — `25ab2cfa85d28bf2…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/full_output.txt` — full-domain output — `c076169b95b00432…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/certify_arc_ends.py` — arc-end certifier — `8ea21bf663493518…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/arc_ends_output.txt` — arc-end output — `045489e1e380f161…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261114T224105-download-4-A5-SLIVER-DEFS.md` — domain/target definitions (swarm smwgy3s8k m2) — `714b2eb2a7eeb9a8…`
- **Checked by the results desk:** ~07:00Z (exposition desk, ledger owner): re-ran certify_full.py (sha256 25ab2cfa85d28bf2…) and certify_arc_ends.py (8ea21bf663493518…) in a scratch copy with python -I: "ALL BLOCKS CERTIFIED: True (1.2 s)" and "ALL ARC ENDS CERTIFIED: True". Earlier: hashes recomputed and CERTIFICATE.md read by the results desk.
- **Provenance:** Verifier lane m2 definitions; certificate by the research desk 2026-11-14 23:45:56Z.
- **Correction history:** the domain file's claim |A_far − ci| > 1.5 is false on part of P1 (|A2−ci|² ∈ [2.2004, 2.2339]); the weaker > 1 is certified everywhere (see A5-FAR-APEX)
- **Used for:** Closes the sliver gap and the C2-box dependency in [A5-ODD-WALK](#a5-odd-walk); the walk coordinates there are still not enumerated.

### DIR-FILTER

**Discrete direction filtering: 7,776 → 1,420 → 174 → 6** — `TESTED_FINITE`

- **Statement:** On the declared grid q ∈ {0}×{0..5}⁵ (7,776 vectors), 1,420 pass the aligned (AC) constraints, 174 also admit a cyclic palette witness, and the CC60 filter leaves six.
- **Hypotheses:** Finite relaxation only; conditional on AC and the source premises; the 174→6 step is conditional on CC60. Not a classification of arbitrary directions or of actual WeakColoring 6.
- **Evidence:** ac_filter_enum.py + independent complete path reconstruction audit_ac_filter.py; conditional-cone-filter.json.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/checkin-artifacts/20261114T172056Z/audit_ac_filter.py` — independent audit script — `2f33743108995cad…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/checkin-artifacts/20261114T172056Z/ac_filter_enum.py` — enumeration script — `83480a73b9f9936d…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/checkin-artifacts/20261114T172056Z/ac-independent-audit.json` — audit output (174 witnesses) — `5e1e25c4f2f013e3…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/checkin-artifacts/20261114T172056Z/conditional-cone-filter.json` — CC60 filter output (6 survivors) — `ddf2d42c1f449ab8…`
- **Checked by the results desk:** 2026-11-15 ~00:05Z: copied the two archived scripts to a scratch folder and ran `python -I audit_ac_filter.py` (1 s): counts {total 7776, pass_ac 1420, true_survivors 174, old_survivors 95}; the regenerated JSON is identical to the archived ac-independent-audit.json (174 survivors, 79 previously missed). The 174→6 CC60 filter output was not re-run.
- **Provenance:** Check-in 2026-11-14T17:20:56Z (parent audit + worker DP/DFS confirmation).
- **Correction history:** 95 → 174: the earlier count 95 came from a greedy witness-reconstruction bug; complete path reconstruction gives 174 (79 missed)
- **Depends on:** [CC60](#cc60)

### FIXED-PHASE-CENSUS

**Fixed-phase census of the six-direction relaxation: 177 SAT / 7,599 UNSAT** — `TESTED_FINITE`

- **Statement:** Modulo phase rotation there are 7,776 sign classes of the six-direction palette CSP R(t,α); 177 are satisfiable and 7,599 unsatisfiable, and every UNSAT class is refuted by forced-label propagation (862 UNSAT classes have no empty hitting side).
- **Hypotheses:** Fixed phase only. Lemma 0 (witness reduction) makes UNSAT a statement about the palette CSP, not a search restriction. Not a classification of whole direction configurations (every positive phase interval must be SAT).
- **Evidence:** Parent unrestricted 64-palette check + reduced checks + independently authored Python DFS/half-cycle join agree on every class (census-crosscheck.json). The research desk also recomputed SAT=177/UNSAT=7599 with its own transfer-matrix implementation; SAT sets identical class by class.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T200919Z/fixed-phase-census.json` — census — `82a316c947daf743…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T200919Z/census-crosscheck.json` — cross-check — `d02d98585b61bd8f…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T200919Z/census-verifier.js` — parent verifier — `c4fbde4ef0e3f086…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T200919Z/phase-theorem.txt` — phase theorem (exact geometry, Lemma 0, zero lemma) — `75aeedd978c516c6…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/census/independent_census.py` — desk independent reimplementation — `175b6861afbe4467…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/census/independent_census.out` — desk output — `1ac79d65205b9e49…`
- **Checked by the results desk:** 2026-11-15 ~00:40Z: ran the parent supervisor census-verifier.js (archived in import-20261115, pure computation, no I/O) from a scratch copy: {sat 177, unsat 7599, nonemptyUnsat 862, unitIncomplete 0, mismatches 0} — so every UNSAT class is refuted by propagation and the 2-palette and full-palette deciders agree on all 7,776 classes. Also read the research desk outputs (SAT=177, UNSAT=7599). L-R1 judge baseline (02:16Z, read only): 177 / 7599 / 862, 6,737 with an empty side, label-level propagation incomplete 0; DFS vs DP and minimal vs unrestricted palettes agree on all 7,776 classes. Caveat from that report: palette-level propagation (as opposed to label-level) leaves 72 UNSAT classes unrefuted, so "refuted by propagation" refers to label-level forced-label propagation.
- **Provenance:** Check-in 2026-11-14T20:09:19Z (parent supervisor); research-desk recomputation 23:30:52Z.
- **Used for:** Base table for the staircase census and Thm B'.

### HEULE-UNION

**Translated Heule union: exact 1,048-vertex unit-distance graph with a proper 5-colouring** — `TESTED_FINITE`

- **Statement:** The union of the 553-vertex Heule graph and a translate is an exact unit-distance graph with 1,048 vertices, 5,487 edges, 58 overlapping vertices and 184 new connecting edges; all 548,628 unordered pairs were tested in exact multiquadratic arithmetic, and an explicit proper 5-colouring is verified.
- **Hypotheses:** Coordinates in ℚ(√3,√5,√11); the lower bound 5 comes from the embedded Heule553 subgraph whose 4-UNSAT proof is not re-run here.
- **Evidence:** Independent strict-expression parser with exact arithmetic (Verify-HeuleUnion.mjs); safe-integer bound proved with BigInt.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/HEULE-UNION-CERTIFICATE.json` — certificate — `cd3f9ff3a47f93d5…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/Verify-HeuleUnion.mjs` — verifier — `ca9510a2dfd81fbb…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/HEULE-UNION-VALIDATION.txt` — validation — `e611fb63e2086a00…`
  - `HadwigerNelson/Main/IMPORT-VALIDATION.json` — import validation record — `6016a27ed9bba204…`
- **Checked by the results desk:** 2026-11-14 23:50Z: re-ran `node HadwigerNelson/Main/verify-snapshot.mjs` (exit 0, 11 s), which re-runs Verify-HeuleUnion.mjs: passed, 548,628 pairs, 1,048 vertices, 5,487 edges, proper 5-colouring.
- **Provenance:** Graph lanes (graph-union-audit), 2026-11-14; import validation 18:58Z.
- **Correction history:** 17 colourings reduced candidate pairs 110,015 → 1,145, then 34 colourings separated all 543,141 nonadjacent pairs; unreconciled wording: 177 survivor pairs inside the original H locally vs 112 in remote wording (HEULE-UNION-VALIDATION.txt records remainingPairsInsideOriginalH 177); moot after the full separation certificate
- **Used for:** Finite evidence base; no new plane bound.

### HONEYCOMB-73

**73-cell honeycomb patches are not 6-colourable (a = 1/5 and a = 1/4)** — `TESTED_FINITE`

- **Statement:** The 73-cell honeycomb conflict graph at a = 1/5 (888 edges, 6,496 clauses) and at a = 1/4 (723 edges, 5,506 clauses) has no proper 6-colouring; exact persistence intervals (1/√28, 1/√19) and (1/5, 1/√12).
- **Hypotheses:** Restricted family: colourings constant on honeycomb cell interiors. Not a bound for unrestricted plane colourings.
- **Evidence:** drat-trim "s VERIFIED" (remote, independent; local regeneration of edges/clauses with SHA match).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CONSOLIDATED-FINDINGS.txt` — record (snapshot copy) — `eac30d0ed71409ec…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/patch25-audit/drat_run.log` — a=1/4 drat-trim log — `a02875f45b7a7ca3…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/patch25-audit/A-QUARTER-AUDIT.md` — a=1/4 audit — `adf745d81fc93870…`
- **Checked by the results desk:** Not re-run by the results desk.
- **Provenance:** Overnight 13–14 Nov graph lane (CONSOLIDATED-FINDINGS).
- **Correction history:** a handwritten checker had a counting bug (superseded by drat-trim)

### LN1-ORBITS

**Symmetries of the 177 SAT classes; the orbit-65 staircase obstruction** — `TESTED_FINITE`

- **Statement:** For the six-direction relaxation (fixed-phase census, classes tau in (Z/6)^6 modulo a constant shift): SAT is invariant under the index rotation rot (tau_i -> tau_{i-1}), the index reversal rho (tau_i -> tau_{5-i}) and negation neg (tau -> -tau), on all 7,776 classes. The 177 SAT classes form 89 rho-orbits, 35 rot-orbits and 18 dihedral <rot,rho>-orbits (sizes 2,3,4,6,12); adding neg (a group of order 24, the full stabiliser of the SAT set among signed index permutations) leaves 13 orbits. The L-N1 m1 shard of 22 classes is exactly 8 dihedral orbits. Orbit 65 = {013542, 023154}: each class is SAT, has exactly one SAT level-1 decrement (j* = 3, resp. 2), all five level-2 decrements are UNSAT, so none of its 720 decrement staircases is all-SAT. Of the 177 SAT classes, 126 have at least one all-SAT generic staircase and 51 have none.
- **Hypotheses:** Relaxation level only; the "realised generic" certificates of the L-N1 swarm (20 JSONs) were not available and are not covered (item (d) UNDETERMINED).
- **Evidence:** Independent checker written by the research desk (indep_ln1.py, two SAT deciders agreeing on all 7,776 classes; cross-check against the desk independent_census.py SAT set: identical 177).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/LN1/indep_ln1.py` — independent checker — `b6c3e7b4fc59fc05…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/LN1/indep_ln1.out` — output (24 s) — `401c98a9a9fe8af4…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/LN1/indep_ln1_xcheck.out` — output with census cross-check — `79391329868fdfbc…`
- **Checked by the results desk:** 2026-11-15 ~03:18Z: hashed the three files (checker sha = BANKED.md value); re-ran indep_ln1.py from a scratch copy (python -I, exit 0): every line identical to the archived output apart from paths and timing, 0 FAIL lines, verdicts (a) (b) (c) CONFIRMED, (d) UNDETERMINED.
- **Provenance:** L-N1 lane (chat-8cf5afe743, swarm smwh3vfw7, owner research desk); independent checker by a research-desk subagent, banked 03:12:57Z.
- **Correction history:** new beyond the lane claim: the negation symmetry reduces 18 dihedral orbits to 13
- **Depends on:** [FIXED-PHASE-CENSUS](#fixed-phase-census), [STAIRCASE-CENSUS](#staircase-census)
- **Caveats:** Orbit 65 is an obstruction only for generic (one coordinate at a time) staircases: it survives tied-coordinate staircases with 2–3 blocks (ordered-partition counts by blocks {1: 1, 2: 2, 3: 1}).

### LN3-T1-T3

**A6 paired-palette counts (T1) and J-depth at (m,w) = (7,3) (T3)** — `TESTED_FINITE`

- **Statement:** T1: per position, 28 subsets of Fin 6 satisfy the hit conditions H1 and H2 (28^6 = 481,890,304 families); exactly 729 two-label families satisfy H1 and H2 (the same set under every reading); adding H3 (cyclic disjointness) leaves exactly one family, {f_j, g_j}; with the path-only version of H3 there are 64 families (4 in the two-label space). T3: at (m,w) = (7,3) the permutation-chain J-depth is 8; the longest simple in-W path from a J state is NOT 13 — an explicit verified simple path of 226 states exists and a rigorous upper bound is 1,928. Calibration at N = 6: exact longest simple path 3 (agrees with J-DEPTH).
- **Hypotheses:** Finite relaxation statements; T1 uses the A6 source table; T3 uses the discovery-lane state graph definitions (W, J).
- **Evidence:** Independent checker by the research desk (indep_ln3.py); T1 by backtracking and transfer matrix; T3 by exact DAG longest path at N = 6 and SCC-condensation bounds at N = 7.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/LN3/indep_ln3.py` — independent checker — `fdbaf0c04632ea1b…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/LN3/indep_ln3.out` — output — `9f478cfc9519b8bd…`
- **Checked by the results desk:** 2026-11-15 ~03:25Z: re-ran indep_ln3.py from a scratch copy (python -I, exit 0): output identical to the archived one apart from timings, no FAIL lines.
- **Provenance:** L-N3 lane (chat-4ac4b34cf7, owner research desk); research-desk checker 03:15Z.
- **Correction history:** T3b: the lane figure "13" for the simple-path depth at (7,3) is only a lower bound and is refuted as an exact maximum (true value in [226, 1928]); the permutation-chain value 8 is confirmed (the earlier "≥ 13, not 8" coordinator wording mixed the two notions)
- **Depends on:** [A6-FORCING](#a6-forcing), [J-DEPTH](#j-depth)

### RELAX-1-648

**All-phase relaxation: the field set has measure exactly 1/648 (1,440 of 933,120 resonance cells) and meets 16 of 3,840 sign cells** — `TESTED_FINITE`

- **Statement:** For alpha in (R/360Z)^6 with alpha_0 = 0, call a resonance cell a component of the complement of {alpha_i - alpha_j in 60Z}: integer parts floor(alpha_i/60) and the order of the parts alpha_i mod 60, so 6^5 x 5! = 933,120 congruent cells. Exactly 1,440 cells admit a relaxation field (R(t,alpha) SAT for every t); 919,512 fail because some arc has an empty side (Rp or Rn empty) and 12,168 fail by the cyclic disjointness system alone. Hence the field set has Lebesgue measure exactly 1440/933120 = 1/648. With sign cells = components of the complement of {alpha_i - alpha_j in 180Z} (2^5 x 5! = 3,840): the results desk finds the field set meets 16 sign cells (16 of the 120 mod-180 orders; all 120 mod-60 orders occur), confirmed by the L-R1 judge after it corrected a sign-cell key bug (its first report said 720); each met sign cell holds 90 field cells.
- **Hypotheses:** Relaxation level only (inner/outer hits and 60-degree disjointness; palettes of size <= 2 WLOG). Says nothing directly about colourings.
- **Evidence:** Two independent implementations agree: the discovery m2 scripts (referee6.py, run and reproduced by the all-phase referee, unaudited) and an exact implementation written by the results desk from the model definitions (allphase_desk.py, integer angles in units of 1/14 degree, one interior representative per cell, all six arcs tested).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/results-desk/allphase/allphase_desk.py` — results-desk independent implementation — `07c89fab37168a9e…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/results-desk/allphase/allphase_desk.out` — command and output (92.6 s) — `81f5c38f9adb36a5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261114T205744-download-5-ALL-PHASE-REFEREE.md` — all-phase referee note, section 8 (m2 figures) — `087e6efc55b766cd…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/results-desk/allphase/mc_signcells.py` — results-desk Monte Carlo sign-cell check — `1e8b0525aa995d6d…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/results-desk/allphase/mc_signcells.out` — Monte Carlo output (225 field hits, 16 sign cells) — `1be8f3f562a606b2…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/results-desk/allphase/lift_labels.py` — results-desk lift-label test — `94d8b5e888fda075…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/results-desk/allphase/lift_labels.out` — lift-label test output (16 components; naive lift 96 labels) — `1f4230df777d6c29…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T034153-download-1-SIGNCEL-COUNT.md` — first-pass referee (lane chat-2345d7f398, swarm smwh90qeq): claimed 62 sign cells (refuted) — `f6baa6b98c838289…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/SIGNCELL/indep_signcell.py` — research-desk two-method sign-cell recount — `e556895c0de11ff5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/SIGNCELL/indep_signcell.out` — recount output (166 s; 0 FAIL) — `b7a5890d91d2fae5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T021643-download-4-R1-1-BASELINE.md` — L-R1 judge baseline report (R1-1) — `8501a0a088af9e7f…`
- **Checked by the results desk:** 2026-11-15 ~01:20Z: wrote and ran allphase_desk.py (python -I, 92.6 s): cells 933,120; field 1,440; empty side 919,512; cyclic-disjointness only 12,168; measure 1/648; sign cells meeting the field set 16 of 3,840; mod-180 orders 16 of 120; mod-60 orders 120 of 120. Cells are congruent simplices (fixed integer parts and a fixed order of five fractional parts), so the measure is the cell fraction. THIRD IMPLEMENTATION (L-R1 judge baseline, delivered 02:16Z; read, script not run by the desk): reproduces 933,120 / 1,440 / 919,512 / 12,168 and 1/648 exactly, but reports that 720 of 3,840 sign cells meet the field set (2 field cells each) and 120 of 120 base chambers. DISPUTE on the sign-cell count, resolved for now in favour of 16: (i) my exact enumeration, with sign cells recomputed directly from the representative angles, gives 16 sign cells holding 90 field cells each; (ii) an independent Monte Carlo (150,000 uniform random exact configurations, no cell enumeration) gave 225 field hits (rate 0.0015 ≈ 1/648) spread over 207 distinct resonance cells but only 16 distinct sign cells, whereas 720 sign cells would give about 190 distinct sign cells for 225 hits. The L-R1 lane was asked to recheck its sign-cell extraction; its corrected run reproduces 16 of 3,840 (cycle 031143). FINAL (~04:30Z): read the research-desk recount output (0 FAIL; A and B identical cell by cell; 1,424/1,424 certified wall-free paths to the 16 class representatives; all 52,930 naive-label splits resolved). Four independent supports for 16: results-desk enumeration, results-desk Monte Carlo, corrected L-R1 judge, research-desk two-method recount. Not re-run by the results desk (166 s).
- **Provenance:** Discovery m2 (smwgui6l9 d1, unsubmitted) via the all-phase referee 20:57Z; adversarial final wording cycle 001250; results desk recount 01:20Z.
- **Correction history:** ~04:10Z a first-pass referee (chat-2345d7f398, swarm smwh90qeq, SIGNCEL-COUNT.md) agrees on 1,440 cells and on 16 of 120 mod-180 base chambers with 90 field cells each, but claims the field set meets 62 of the 3,840 sign cells (from member m4's census, labelling a sign cell by a base chamber plus a lift class in (Z/2)^6/<1,...,1>). Results-desk test (lift_labels.py): that lift, read off as floor(alpha_i/180) without fixing alpha_0, is not constant on W_180 components: one global rotation per field representative keeps each in its component, and the alpha_0-normalised label stays at 16 while the naive lift gives 96 labels. So 62 is consistent with a labelling artifact; the ledger keeps 16. The referee also states that neither of W_60, W_180 contains the other; in fact W_180 is contained in W_60 (a difference in 180Z lies in 60Z), so each resonance cell lies in one sign cell. CLOSED ~04:30Z: the research-desk independent recount (indep_signcell.py, two methods — combinatorial cells with alpha_0 = 0, and one random exact point per cell with gauge-free pairwise labels floor(((alpha_j - alpha_i) mod 360)/180) — agreeing cell by cell on all 933,120 cells) gives 3,840 sign cells of 243 resonance cells each, 16 of 120 base chambers × 90 and 16 sign cells × 90; every one of the 52,930 same-chamber SAT pairs that the naive lift separates is joined by a certified W_180-free path; the naive chart key gives 16, 30, 48, 50, 53, 56, 79 or 96 depending on the global rotation, so 62 is a chart artefact. The referee lane was told to record 62 as FALSE; sign-cell dispute RESOLVED: the L-R1 judge baseline first reported 720 of 3,840 (02:16Z); the coordinator traced this to a sign-cell key bug in that baseline (mod-60 order and n mod 2 used instead of the mod-180 order and floor(alpha/180)) (cycle 025639), and the corrected L-R1 run reproduces 16 of 3,840 with 90 field cells each (cycle 031143); the graph lane is consistent (1440 = 120 x 12 = 16 x 90); (e) correction from the L-R1 baseline: (0,30,90,150,240,300) lies on walls of the mod-60 arrangement (fractional parts not distinct), so the claim that the two example vectors lie in one sign cell is ill-posed; the example still illustrates that the field property is constant on resonance cells, not on sign cells; RECONCILED (was UNRECONCILED): "16 of the 3840 sign cells" (referee addendum) and "16 of 120 base chambers" (adversarial lane, cycle 001250) are both true. The 16 met sign cells map to 16 distinct mod-180 orders. Read "base chamber" as an order of the parts mod 180; with orders mod 60 the count would be 120 of 120; the referee note called sign cells "finer" than resonance cells; they are coarser (each sign cell contains 243 resonance cells on average); status history: UNAUDITED_NUMBER until 01:20Z (coordinator cycle 213711 had called it "confirmed by three lanes" without an audit artifact); the 8640/(7776*720) "fully split rate" equals 1/648 exactly, consistent with the staircase k=6 count
- **Used for:** Quantifies how rare relaxation fields are; explains the 0/400 and 1/900 random-sample observations.
- **Depends on:** [FIXED-PHASE-CENSUS](#fixed-phase-census)

### SIX-ORBIT

**Six six-direction configurations excluded by the inner/outer-hit relaxation** — `TESTED_FINITE`

- **Statement:** The configurations (0,30,90,120,180,210), (0,30,90,120,270,300), (0,30,180,210,270,300), (0,60,90,150,180,330), (0,60,90,240,270,330), (0,150,180,240,270,330) (degrees) survive CC60 and MC120 but are UNSAT in the relaxation R(t,α) (inner/outer hits + 60° disjointness, any palette size) on one positive phase cell; each has an open simultaneous ℓ∞ 15° exclusion neighbourhood (fixed-phase box radii 15/45). Dropping only the wrap edge leaves 2 of the 6 UNSAT.
- **Hypotheses:** Excluded for actual interfaces only under the same source producers as A6 (R must hold a.e. in t). Relaxation-level statement.
- **Evidence:** Parent reproduced all 6 exact checks and 378 cone checks; readable forced-label proofs (CLAUDE-SIX-ORBIT-PROOFS) checked against the exact tables; graph m2 confirms with three procedures incl. unreduced 64-palette DP.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/CLAUDE-SIX-ORBIT-PROOFS.txt` — forced-label proofs — `34ed301a1133977b…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T191820Z/inner-outer-orbit-certificates.json` — certificates — `6f546fb260b779a5…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T191820Z/verify-inner-outer-orbits.js` — parent verifier — `ae6c4d2beebe8c96…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T194118Z/graph-m2-REPORT.txt` — graph m2 report — `826555e70beeed2d…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T194118Z/corner-all-phase-validation.json` — 15° corner validation — `15a31adcb7c5ee26…`
- **Checked by the results desk:** 2026-11-15 ~00:40Z: ran the parent supervisor verify-inner-outer-orbits.js (archived in import-20261115, pure computation) from a scratch copy; its output is identical to the `data` field of the archived inner-outer-orbit-certificates.json for all 11 vectors. Each of the six configurations has exactly one UNSAT cell — (0,30), (30,60), (0,30), (30,60), (0,30), (30,60) in table order — and the five controls have none. The 15° neighbourhood and chain results were not re-run.
- **Provenance:** Claude09/11 proofs; parent check-ins 19:18:20Z and 19:41:18Z; graph m2 (smwgui92e).
- **Correction history:** sixth vector's UNSAT cell corrected (0,30) → (30,60) by m1; an earlier m2 claim "all six survive the wrap-dropped chain test" came from a buggy solver and is void (2 of 6 stay UNSAT); 15° called "sharp" (simultaneous ℓ∞, parent) vs "not sharp" (single-coordinate moves <30°, m1): different metrics; exact global radius open

### STAIRCASE-CENSUS

**Staircase census: 76,283 surviving staircases of 36,415,008** — `TESTED_FINITE`

- **Statement:** Over 7,776 sign classes × 4,683 ordered set partitions of {0..5} (= 36,415,008 staircases), exactly 76,283 survive; by number of blocks k=1..6: [177, 2576, 12762, 26928, 25200, 8640].
- **Hypotheses:** A necessary condition only (survival is necessary, not sufficient, for a field); converse open.
- **Evidence:** census.py --full (2.06 s) and an independent desk reimplementation (explicit enumeration of 4,683 ordered partitions, 13.3 s) agree exactly.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/census/census.py` — worker script (inbox 20261114T224105-download-1; LF sha256 da28d617…) — `fa6436d577d4a1c1…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/census/census_full.out` — output — `a2c2df5acae23a79…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/census/independent_census.py` — desk independent script — `175b6861afbe4467…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/census/independent_census.out` — desk output — `1ac79d65205b9e49…`
- **Checked by the results desk:** Hashes recomputed; read both outputs (identical by_k and totals); checked 7776·4683 = 36,415,008 and that by_k sums to 76,283. 2026-11-15 ~00:45Z: re-ran the research desk independent_census.py (archived in import-20261115) from a scratch copy: SAT 177 / UNSAT 7599, 4,683 ordered partitions, by_k [177, 2576, 12762, 26928, 25200, 8640], total 76,283 of 36,415,008 (29.5 s). The worker census.py (inbox download) was not run by the results desk. L-R1 judge baseline (02:16Z, read only) reproduces by_k [177, 2576, 12762, 26928, 25200, 8640], 76,283 of 36,415,008 and the Fubini slices 1, 62, 540, 1560, 1800, 720; it also notes that tau -> -tau preserves SAT, so the +1_A and -1_A staircase conventions agree, and that 8,640 = 6 × 1,440 links the census to RELAX-1-648.
- **Provenance:** Graphs lane smwgui92e m2 census.py; coordinator cycles 204019–231544; run locally by the research desk 23:30:52Z.
- **Correction history:** staircase.md total typo 36,415,608 → 36,415,008 (cycle 211858); Staircase.lean has a Fintype type error and `sorry` — not Lean evidence
- **Used for:** Staircase classification ([STAIRCASE-CONVERSE](#staircase-converse)).
- **Depends on:** [FIXED-PHASE-CENSUS](#fixed-phase-census)

### A5-ODD-WALK

**Explicit A5 odd walk needs at least 15 edges** — `CANDIDATE`

- **Statement:** The explicit odd unit walk in the A5 four-list obstruction (A5-FOUR-LIST) needs at least 15 edges; walk coordinates and vertex count are still not enumerated.
- **Hypotheses:** Relies on C1 exact margins, C2 interval boxes (1,469 + 889, verifier m2 report) and the A5 sliver certificate; C3 is a grid search only.
- **Checked by the results desk:** Not checked by the results desk beyond A5-SLIVER. C2 boxes not re-run locally.
- **Provenance:** Verifier lane (cycle 205744 "modulo one sliver not yet interval-certified").
- **Depends on:** [A5-SLIVER](#a5-sliver), [A5-FOUR-LIST](#a5-four-list)

### A6-COROLLARIES

**A6 corollaries: ≤3 distinct directions impossible; uniform ε₀-neighbourhood of the paired configuration** — `CANDIDATE`

- **Statement:** Under the common actual hypotheses the six edge directions cannot take ≤ 3 distinct values (CC60 ⇒ matching blocks; strict MC120 ⇒ 120° spacing; A6+A5 excludes it). There is ε₀ = min(η/4, π/24) > 0 such that every independent perturbation within ε₀ of the paired configuration is impossible.
- **Hypotheses:** Conditional on strict MC120 (MC120-STRICT, refereed ACCEPT WITH CORRECTIONS ~05:00Z) and on A6-PAIRED-PRODUCER. CAUTION: the R1-4 referee (C1) states that A6 is not stable under separating a pair and that no neighbourhood version is proved; the ε₀-neighbourhood claim here therefore needs its own referee before any upgrade.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-PAIRED-COROLLARIES-A6.txt` — paper ("concise independent audit", author-side) — `94a6b50a2c053055…`
- **Provenance:** Astra A6 corollaries; check-ins 19:18:20Z, 19:41:18Z.
- **Correction history:** adversarial coordinator withdrew its objection to the neighbourhood result (19:41:18Z)
- **Depends on:** [A6-PAIRED-PRODUCER](#a6-paired-producer), [MC120-STRICT](#mc120-strict), [CC60](#cc60)

### A7-PARTIAL-INDEPENDENT

**A7: every two-list locus of the q4/q5 partial field is unit-distance independent** — `CANDIDATE`

- **Statement:** For the period-180° partial field F with bins {1,4},{2},{2,5},{3},{0,3},{1}, every two-list locus R_j is unit-distance independent (pieces of diameter < 1, cross gaps > 1), so binary-rigidity ignition has no starting point.
- **Evidence:** Paper; "parent reviewed" (19:41:18Z); no referee file for this part.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-PARTIAL-PALETTE-A7.txt` — paper — `cfa34f367d772dd7…`
- **Provenance:** Astra A7 lane.

### AMPLIFIER

**Amplifier: a forced-equal pair yields a finite (k+1)-chromatic unit-distance set** — `CANDIDATE`

- **Statement:** A finite k-colourable induced unit-distance set with a distinct pair forced equal in every k-colouring yields a finite non-k-colourable point set (anchors only equal; D ≥ 1/2 allowed; coordinates in K(√(4n²‖v‖²−1))).
- **Hypotheses:** Conditional route to a global bound: needs a forcing pair, and none exists in the studied Heule graphs (HEULE-NO-FORCING); a k=5 forcing pair would only reproduce χ ≥ 6.
- **Evidence:** "ACCEPTED MATHEMATICAL IMPLICATION" by the supervisor (CONSOLIDATED-FINDINGS); no separate referee file; controls (13,13,2), (9,9,2), (7,11,3) checked exhaustively.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CONSOLIDATED-FINDINGS.txt` — record — `eac30d0ed71409ec…`
- **Provenance:** Overnight 13–14 Nov (02:06, 02:30).
- **Correction history:** draft claim "all chain vertices monochromatic" false; 2nE+1 bound and H4 compatibility corrected

### CENSUS-COMPLETE-60Z

**Fixed-phase census is complete for the relaxation iff all pairwise α differences lie in 60°ℤ** — `CANDIDATE`

- **Statement:** The fixed-phase census is complete for the relaxation if and only if all pairwise differences of α lie in 60°ℤ.
- **Checked by the results desk:** No artifact located yet.
- **Provenance:** Coordinator cycle 205744.
- **Depends on:** [FIXED-PHASE-CENSUS](#fixed-phase-census)

### CLAUDE-LEMMA-A

**Claude Lemma A (triangle coincidence impossible) and Corollary B** — `CANDIDATE`

- **Statement:** Measurable weak c, any x, |univ∖(J∪K)| ≤ 2 and μ(M_{J,K}) > 0 imply False, where M_{J,K} = {t : J ⊆ P(t+2jπ/3), K ⊆ P(t+2jπ/3+π+α)}. Corollary B: under H2, `two_state_impossible` applies iff the palette is essentially two-valued.
- **Evidence:** Paper (Claude Max); same density-triangle mechanism as refereed NR/TC; no referee file for Lemma A itself.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CLAUDE-FIRST-RESEARCH-2026-11-14.txt` — paper — `8c90ddb223c2b14e…`
- **Provenance:** Claude first research run, 2026-11-14.

### CONTINUOUS-SIX

**Continuous CC60 classification of six-cycle directions (Theorems G, O, Corollary P)** — `CANDIDATE`

- **Statement:** "Every closed 60° arc covers ≤ 3 labels" ⇔ circular distance > 60° for every nonadjacent edge-index pair; Theorem O: a cyclic order of six distinct directions is feasible iff it has a C6-adjacent consecutive pair (57 of 60; forbidden (0,2,4,1,5,3), (0,2,5,3,1,4), (0,3,1,5,2,4)); Corollary P: with three distinct directions the blocks are a perfect matching 120° apart (needs strict MC120); four-direction partial results.
- **Evidence:** Paper. Corollary P (three distinct directions ⇒ perfect-matching blocks exactly 120° apart, using CC60 and strict MC120) was refereed ACCEPT in R1-3-REFEREE §2 (~05:00Z); Theorems G and O have no referee verdict, so the entry stays CANDIDATE.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-CONTINUOUS-SIX-A4.txt` — paper — `70a91bc5d72681f2…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T045717-download-0-R1-3-REFEREE.md` — referee verdict covering Corollary P only — `0b295e593daf9438…`
- **Provenance:** Astra A4 lane, 2026-11-14.
- **Depends on:** [CC60](#cc60), [MC120-STRICT](#mc120-strict)

### HONEYCOMB-RESTRICTED

**No cell-constant proper 6-colouring of the honeycomb for a ∈ (1/√28, 1/2]** — `CANDIDATE`

- **Statement:** For a ∈ (1/√28, 1/2] there is no proper 6-colouring constant on every honeycomb cell interior (HONEYCOMB-73 on (1/√28, 1/√12), K7 for a ∈ (1/√13, 1/2]; above 1/2 within-cell unit pairs prohibit any cell-constant colouring).
- **Hypotheses:** Restricted family; does not bound unrestricted plane colourings.
- **Evidence:** "ACCEPTED restricted-family theorem" by the supervisor (CONSOLIDATED-FINDINGS 01:27); no separate referee file.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CONSOLIDATED-FINDINGS.txt` — record — `eac30d0ed71409ec…`
- **Provenance:** Overnight 13–14 Nov.
- **Depends on:** [HONEYCOMB-73](#honeycomb-73)

### J-DEPTH

**Relaxation rigidity: J-depth is at most 3, and 3 is attained** — `CANDIDATE`

- **Statement:** In the discovery lane's rigidity reduction, the J-depth of states is ≤ 3 and the bound is attained; the I(σ) table holds on J only (648 counterexamples on W); the statement fails at (m,w) = (7,3).
- **Evidence:** Swarm smwh11ydr: proved twice independently, 0.75 s certificate, 12/12 live mutation controls (coordinator report). No local artifact yet.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T002122-download-5-STATUS.json` — discovery swarm STATUS (route B proof outline, finite lemmas FL1-FL4) — `ccc9384768d9534a…`
- **Checked by the results desk:** Read the STATUS.json: route B claims rank r(sigma) <= 2 on J and strictly decreasing on J->J steps, so a J-run has at most 3 states; depth 3 attained at (2,2,4,0,5,3); four finite lemmas machine-checked (FL1-prime 1836 cases, FL2 18 sinks, FL3, FL4); all 51,840 full chains inside W contain a circulant state. Not reproduced by the desk; route A independence check was still running. Queued for L-R1 (R1-6).
- **Provenance:** Discovery swarm smwh11ydr (5/6 members accepted); cycles 001250, 002122.
- **Correction history:** related but separate: the synthesis lane (L-N3) T3 run length at (m,w) = (7,3) was reported as at least 13, not 8 (cycle 024133), then retracted; the T3 target is 8 (cycle 031143; research desk 03:05Z). Now settled by the research desk checker: see LN3-T1-T3
- **Depends on:** [RELAX-CIRCULANT](#relax-circulant)

### K6-M3-DOOR

**k=6, m=3 two-label door closed (Moser spindle is 3-degenerate, hence 4-choosable)** — `CANDIDATE`

- **Statement:** In the k=6 producer audit, the m=3 two-label case closes because the Moser spindle is 3-degenerate and therefore 4-choosable.
- **Checked by the results desk:** Graph fact is standard; the reduction to it is not checked by the results desk.
- **Provenance:** Independent-route lane; coordinator cycle 205744.

### LIST-FIELD-A4

**Two-list locus of the canonical palette has an explicit Borel proper colouring** — `CANDIDATE`

- **Statement:** For the canonical P, the set T of points of the radius-2 domain with |L(y)| = 2 (T = R0 ⊔ R1 ⊔ R2) has an explicit Borel proper L-colouring (bit rule by |z| ≤ 1 on ±V, Re z ≥ 0 on ±H, rotated); 2⁹ flip variants. Hence every finite obstruction must use a 4-list vertex.
- **Evidence:** Paper; independent geometric referee was "running" (17:45Z), no verdict file found. The H half-lobe sub-claim (§4c) is independently re-verified in CLAUDE-A7-CONTACT-AUDIT §3.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-LIST-FIELD-A4.txt` — paper — `0f22a9a734746eb1…`
- **Provenance:** Astra A4 lane.
- **Used for:** Explains why A5-FOUR-LIST needs the 4-list vertex z0.

### Q4Q5-PINNING

**q4/q5: palette = F on the even 30° bins** — `CANDIDATE`

- **Statement:** For the q4/q5 configurations the palette equals F on the even 30° bins: the complement of F(t) is F(t+60) ∪ F(t−60), and the even bins are closed under ±60° mod 180°.
- **Checked by the results desk:** Not checked by the desk.
- **Provenance:** Geometry lane (m2 even-bin pinning); cycles 001250, 001551.
- **Depends on:** [Q4Q5-CONTROLS](#q4q5-controls)

### R0-CHI4

**The two-list region R0 has chromatic number ≥ 4; non-binary sector states are contradictory** — `CANDIDATE`

- **Statement:** χ(R0) ≥ 4 is certified three ways, and the non-binary sector states are contradictory; whether R0 contains a 5-chromatic unit-distance graph is open.
- **Checked by the results desk:** No artifact located yet.
- **Provenance:** Independent lane; cycle 001250 (follow-up swarm smwh32u04 running).
- **Depends on:** [K6-PRODUCER](#k6-producer)

### RELAX-CIRCULANT

**Relaxation classification: a field exists iff the configuration is a circulant orbit** — `CANDIDATE`

- **Statement:** A field exists iff circulant orbit; the ⟸ direction was referee-tested, the ⟹ direction is verified on 720 orders only (not hand-proved); rigidity reduced to one machine-verified finite lemma (J-depth ≤ 3 states).
- **Checked by the results desk:** No artifact checked.
- **Provenance:** Discovery lane (smwgylyok → smwh11ydr); cycles 213711, 215215, 231544.

### T6-B2

**T6 implies B2 (palettes of size 1 or 2) for weak 6-colourings** — `CANDIDATE`

- **Statement:** For measurable weak c : ℂ → Fin 6, if for every x and 3-set S, a.e. palette at x+e(t) misses S (T6), then 1 ≤ |P_x(t)| ≤ 2 for a.e. t (B2). T6 itself is a conjecture.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-LEAD.txt` — paper §2 — `19df768a00da39dd…`
- **Checked by the results desk:** The reboot referee accepts the packet as local/finite obstructions but does not re-derive T6 ⇒ B2.
- **Provenance:** Astra six-colour lead.

### THM-BPRIME

**Thm B': census₀ is sufficient but not necessary off R_all** — `CANDIDATE`

- **Statement:** Census₀ plus one test per component is sufficient for the relaxation, but not necessary off R_all; witness α# is a pure (C2) obstruction with every side nonempty.
- **Checked by the results desk:** No referee artifact located yet.
- **Provenance:** Adversarial m2 (swarm smwgw43qj); "accepted" by the coordinator in cycle 212205.
- **Depends on:** [FIXED-PHASE-CENSUS](#fixed-phase-census)

### TRANSLATION-CRITERION

**Finite translation criterion for k-colourability of the plane** — `CANDIDATE`

- **Statement:** If every finite configuration translates into a properly k-coloured domain, the plane is k-colourable (finite-graph compactness); plane-null complements and half-planes satisfy the hypothesis.
- **Evidence:** "PROOF ARGUMENT ACCEPTED" by the supervisor; generic Lean source pending; the converse was rejected.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CONSOLIDATED-FINDINGS.txt` — record — `eac30d0ed71409ec…`
- **Provenance:** Overnight 13–14 Nov (01:10, 01:27).

### WILD-LAW

**Wild-law lemma for K-invariant laws on the dual of F(i)** — `CANDIDATE`

- **Statement:** For F the real algebraic numbers, E = F(i) discrete, D its dual and μ a K-invariant Borel probability on D: if |a_z| = 1 for some nonzero z then μ is the point mass at the trivial character; hence a wild law has |a_z| < 1 for all z ≠ 0.
- **Evidence:** Reviewed by the supervisor only ("not Lean-checked"); corrects the DeepSeek packet (H_z not K-stable).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-WILD-LAW-REVIEW.txt` — review — `1cd50f017d08e779…`
- **Provenance:** Overnight 13–14 Nov.

### K6-PRODUCER

**k=6 producer: two named missing declarations** — `OPEN`

- **Statement:** The m=3 case at k=6 reduces to either a binary collapse producer or a non-4-colourable finite certificate; Criterion C reduces the obligation to a unit-distance graph inside R0 with pair-complement lists (no candidate yet).
- **Provenance:** Independent-route lane; cycles 215215, 224105.

### L6-F6

**Conditional route to χ ≥ 7: L6 (locally finite cyclic transition core) and F6 (acyclic common-interface graph)** — `OPEN`

- **Statement:** proper 6-colouring → measurable weak 6-colouring (BorelTransfer, already in source); then L6 + F6 → FullApprox₆ → planar-cover/mesh contradiction. L6 and F6 are open; no arrow from B2 to L6 or F6 is proved. If both were proved the result would be χ ≥ 7.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-LEAD.txt` — roadmap §3 — `19df768a00da39dd…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-REBOOT-REFEREE.txt` — referee §7 ("supports their distinct roles") — `ceab2e0167e9fc5d…`
- **Provenance:** Astra six-colour lead packet, 2026-11-14 ~08:22Z.
- **Used for:** Explains the "No global chromatic result" headline: the route exists only conditionally.

### LOCALIZED-TWO-STATE

**Every positive-measure partial two-state field is impossible (colouring level)** — `OPEN`

- **Statement:** Open; NR/TC and the near-full-measure model (FOUR-STATE-ANGULAR) show no measure threshold below 1 suffices.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-A2.txt` — statement — `fb2ad23a7600cde8…`
- **Provenance:** Astra A2 lane.

### PALETTE-RIGIDITY

**Missing lemma: palette rigidity (M) / |J∪K| ≥ 3 with RealState on both sectors** — `OPEN`

- **Statement:** The source licenses only |P| ≤ k−3, which is inert; the missing lemma is palette rigidity (M), equivalently |J∪K| ≥ 3 with RealState on both sectors.
- **Provenance:** Coordinator cycles 205744, 211858.

### STAIRCASE-CONVERSE

**Staircase classification converse** — `OPEN`

- **Statement:** Show that every surviving staircase (STAIRCASE-CENSUS) is realised, or classify the obstruction; Theorems A, B, C are consistent with Thm B'.
- **Provenance:** Coordinator cycles 205744, 211858, 232732.
- **Depends on:** [STAIRCASE-CENSUS](#staircase-census)

## Negative results and counterexamples

### A6-CONTAINMENT

**Containment reading of the A6 source restriction is inconsistent** — `LEAN_VERIFIED`

- **Statement:** `A6Forcing.a6_containment_unsatisfiable`: if `f j ∈ P j`, `H j ⊆ P j` and `Disjoint (P j) (P (j+1))` for all j, then False. So a forcing lemma stated with containment would be vacuous; the hit form is the right one.
- **Hypotheses:** Finite statement over `Fin 6`.
- **Evidence:** Same file and job as A6-FORCING.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-admissions/claude-lean-20261114t212205-0/Candidate.lean` — source — `27e45caf4c793897…`
- **Checked by the results desk:** As A6-FORCING: `a6_containment_unsatisfiable` is [propext, Classical.choice, Quot.sound] in the desk spot-check log (01:20Z).
- **Provenance:** As A6-FORCING.
- **Depends on:** [A6-FORCING](#a6-forcing)

### A7-CONTACT

**The old A5 support is properly colourable from the A7 lists (A5 construction cannot be reused)** — `PROVED_PAPER_REVIEWED`

- **Statement:** Every unit contact of z′ = (√3/4, 1/4) in H lies in M = e((π/6,π/3)) + e((2π/3,5π/6)); diam(M)² ≤ 6 − 3√3 < 1; H half-lobes have all distances < 1; hence H1 ∪ H2 ∪ {i/2} has an explicit proper colouring from the A7 lists.
- **Evidence:** CLAUDE-A7-CONTACT-AUDIT: "Verdict: all three claims are true" (the three geometric sub-claims). The assembled colouring is parent-reviewed only.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-PARTIAL-PALETTE-A7.txt` — paper — `cfa34f367d772dd7…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/CLAUDE-A7-CONTACT-AUDIT.txt` — audit (all three claims true) — `596fdbac4c7bde20…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A7 + Claude audit.
- **Correction history:** "since 27<36" is an arithmetic typo; correct justification 75 < 81; A7 v-bound "≤" corrected to strict

### ANNULUS-3COL

**Local annulus countermodel to ternary separation** — `PROVED_PAPER_REVIEWED`

- **Statement:** On A = {0.99 < |z| < 1.01}, nine half-open 40° sectors coloured j mod 3 properly colour all unit pairs inside A (|z−w|² < 10207/15000 within a sector; > 3267/2500 between same-colour sectors). Refutes only the LOCAL implication to ternary separation.
- **Hypotheses:** The extension outside A is not a WeakColoring.
- **Evidence:** ASTRA-SIX-COLOUR-LEAD §4; referee ASTRA-REBOOT-REFEREE §5: "ACCEPTED WITH LOCAL SCOPE".
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-LEAD.txt` — paper — `19df768a00da39dd…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-REBOOT-REFEREE.txt` — referee — `ceab2e0167e9fc5d…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra six-colour lead, 2026-11-14 ~08:22Z.

### FOUR-STATE-ANGULAR

**Four-state angular model refutes the orbitwise-to-global reduction; no measure threshold below 1** — `PROVED_PAPER_REVIEWED`

- **Statement:** f(t) = ⌊t/(π/6)⌋ mod 4 with palettes {0,2},{0,3},{3,5},{2,5} satisfies orbitwise alternation, strip-side compatibility for v=(1,−1,−1,−1,1,1), NR and TC, yet has four palettes. Also: for every ε > 0 a τ-invariant A with μ(A) > 1−ε and a flipping Boolean with no same-phase γ-return.
- **Hypotheses:** Angular models only; AC excludes the actual-interface realisation.
- **Evidence:** Referee ASTRA-AC-REFEREE §6–7 (accepted as angular countermodels).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-A2.txt` — paper — `fb2ad23a7600cde8…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-AC-REFEREE.txt` — referee — `56c5d614f875471b…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A2 lane.
- **Depends on:** [AC-ALIGNED](#ac-aligned)

### LOCAL-TRANSITIONS

**Local transition abundance and unit exclusions do not force L6** — `PROVED_PAPER_REVIEWED`

- **Statement:** An actual local proper 6-colouring of B(0,ρ) (disks at q_n = ρ2⁻ⁿ with three 120° sectors 0,1,2 and annulus 3,4,5) has transition triangles at every q_n and at 0 while nearby palettes stay singleton.
- **Hypotheses:** Local only; not a counterexample to L6 for global weak colourings.
- **Evidence:** Referee ASTRA-REBOOT-REFEREE §6: "ACTUAL LOCAL INTERFACES AND TRANSITIONS — ACCEPTED".
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-SIX-COLOUR-LEAD.txt` — paper — `19df768a00da39dd…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-REBOOT-REFEREE.txt` — referee — `ceab2e0167e9fc5d…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra six-colour lead.
- **Depends on:** [L6-F6](#l6-f6)

### MC120-ENDPOINT

**Closed-120° MC120 is false (19-colour counterexample)** — `PROVED_PAPER_REVIEWED`

- **Statement:** Curved arcs q±(t) = t·e(±(π/3+2t)), t ∈ [0, 1/100], approach 0 in directions ±60° (exactly 120° apart); there is a Borel pointwise-proper 19-colouring (9-colour grid background, P+={0..8}, P−={9..17}, a=18) whose exact support exclusions leave the residual {18}, and W = S+ ∩ S− has no unit pair.
- **Hypotheses:** k = 19; only the limiting directions lie in the closed cone (the arcs bend outside). Not a six-colour statement.
- **Evidence:** ASTRA-MC120-ENDPOINT-A5; referee ASTRA-MC120-ENDPOINT-REFEREE: "ACCEPT the complete paper proof in outputs/ASTRA-MC120-ENDPOINT-A5.txt." (adds nonemptiness margins −18071/4000000, 18729/4000000).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-MC120-ENDPOINT-A5.txt` — paper — `78503d6ee09748ee…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-MC120-ENDPOINT-REFEREE.txt` — referee (ACCEPT) — `318773a2908246dc…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/MC120-ENDPOINT-CORRECTION.txt` — parent correction (open-Reuleaux counterexample) — `ce20448c29cb9091…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra A5 lane; check-ins 18:15:21Z, 18:35:22Z.
- **Correction history:** geometry coordinator first claimed the closed-120 endpoint; the parent rejected it (open-Reuleaux counterexample, universal strip-width bound false) and the coordinator retracted (18:15:21Z)

### SUPPORT-FLIP

**Joint correlations plus adjacency do not upgrade level-set to support disjointness** — `PROVED_PAPER_REVIEWED`

- **Statement:** There is a Borel 2π-periodic two-state angular f with f(t+π/3) = 1 − f(t) pointwise and S0 = S1 = ℝ (built from a Borel set of positive measure in every interval).
- **Evidence:** Referee ASTRA-REBOOT-REFEREE §4: "ACCEPT the packet's periodic positive-measure angular countermodel".
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-JOINT-STATE-LEAD.txt` — paper — `ee5ea9f5091ca286…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-REBOOT-REFEREE.txt` — referee — `ceab2e0167e9fc5d…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Astra joint lead A1.
- **Correction history:** the indicator of the rationals is not an alternative counterexample (referee); an architecture "null dense-set counterexample" was retracted (check-in 16:12:25Z)

### VARIABLE-TRIANGLE

**Fixed-base partner-pair triangle method fails for the four-state palette** — `PROVED_PAPER_REVIEWED`

- **Statement:** For base centre 0 and the half-open four-state palette, no unit equilateral triangle (any translation or rotation) has all three vertices in closure(G), G = {e(a)+e(b) : P(a), P(b) a partner pair}.
- **Evidence:** CLAUDE-VARIABLE-TRIANGLE; referee ASTRA-CLAUDE-TRIANGLE-REFEREE: "ACCEPT the main geometric theorem, including its stronger closure version" (exact rational certificate, e.g. 39/50 − 547/703 = 67/35150).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CLAUDE-VARIABLE-TRIANGLE-2026-11-14.txt` — paper — `2a27ff4ec3e0a0a5…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-CLAUDE-TRIANGLE-REFEREE.txt` — referee (ACCEPT with corrections) — `948cc794594192d0…`
- **Checked by the results desk:** Referee verdict quote confirmed verbatim in the referee file by the results desk (grep). Proof not re-derived by the desk.
- **Provenance:** Claude Max run + Astra referee, 2026-11-14.
- **Correction history:** referee corrections: oriented-difference list omits (270°,330°); inner-spike condition half-open; reflection invariance only for the closure; Claude's ~2.3° decimal slack not certified

### HEULE-NO-FORCING

**No forced-equal pairs in the 553- and 1,048-vertex Heule graphs** — `TESTED_FINITE`

- **Statement:** Each graph has 34 proper 5-colourings that give every vertex a distinct colour signature, so every pair of distinct vertices is separated by some proper 5-colouring: neither graph forces two vertices to share a colour.
- **Hypotheses:** These two specific graphs only.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/HEULE553-NO-FORCING-CERTIFICATE.json` — certificate (553) — `9cb811e361ebc9d5…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/HEULE-UNION-NO-FORCING.json` — certificate (1,048) — `4e8799e7d499804b…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/Verify-HeuleNoForcing.py` — verifier — `484ac96a160e3757…`
- **Checked by the results desk:** 2026-11-14 23:50Z: verify-snapshot.mjs re-verified both: 553 vertices / 2,722 edges and 1,048 / 5,487, 34 proper colourings each, distinct signatures 553 and 1,048; the 1,048 edge set equals the geometric graph.
- **Provenance:** Graph no-forcing audit, 2026-11-14 (before 18:39Z).
- **Used for:** Closes these forcing-pair searches.

### HISTORIC-8

**The eight historic list models are not countermodels to the pair-support theorem** — `TESTED_FINITE`

- **Statement:** All eight normalised historic V0/V3/D/N list models have exact projections of genuine closed C5 six-words (compatible counts 3,8,3,8,8,22,8,22; after contact bans 1,5,1,5,5,18,5,18), and every filtered family loses a required support projection; the referee enumerated 5⁶ words and found exactly 100 closed C5 walks.
- **Hypotheses:** Claim is "none is a countermodel", not "zero surviving words"; normalisation exhaustiveness not checked by the referee.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/astra-referee/verify-certificates.mjs` — independent checker — `f4678bcb40700f92…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/astra-referee/certificate-check.json` — checker output — `b975a1e6220bfd78…`
- **Checked by the results desk:** 2026-11-15 ~00:23Z: re-ran the archived verify-certificates.mjs in a scratch copy: PASS, closedC5Words 100, primary compatible/survivor counts exactly as stated, projectionRetained false for all eight.
- **Provenance:** Astra joint lead + reboot referee §4.
- **Depends on:** [JOINT-SUPPORT](#joint-support)

### HONEYCOMB-K16

**Period-4 honeycomb quotient at a = 1/5 is K16** — `TESTED_FINITE`

- **Statement:** The period-4, 16-vertex honeycomb quotient at a = 1/5 is the complete graph K16 (all 120 strict interior-edge witnesses verified), which excludes that periodic family.
- **Hypotheses:** Only the period-4 honeycomb family; no whole-plane conclusion.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/quotient16-audit/verify_quotient16.py` — exact verifier — `d61543f768451fa8…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/quotient16-audit/quotient16_cert.json` — certificate — `eb3a9f31a6c8652b…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/quotient16-audit/local-result.json` — recorded run — `d9273f0ea3ecd9df…`
- **Checked by the results desk:** 2026-11-15 ~00:36Z: re-ran the archived verify_quotient16.py on a scratch copy of the certificate: exit 0, "checks run; failures = 0", "CERTIFICATE VALID".
- **Provenance:** Overnight 13–14 Nov graph lane.

### LN2-COUNTERMODEL

**Palette-level counter-model: no palette-level producer of binary collapse (L-N2)** — `TESTED_FINITE`

- **Statement:** On the unit triangle A = 0, B = 1, C = 1/2 + (sqrt3/2) i, the L-N2 palette field (sector-constant palettes with declared traces) satisfies, exactly in Q(sqrt3): unit sides; palette disjointness at every unit pair for all a.e. directions (the Lean palette_neighbor_disjoint reading); disjointness under the pi/3 shift including the wrap 5 -> 0; 18 valid traces (entries in [0,1], sum 1, positivity set = palette); |P_A| + |P_C| = 5 (saturating); C11 absent sets {4,5}, {0,1,2,5}, {1,2,3} with the cap |P_x| <= |supp_x| - 1; and all 19 lane predicates as coded (4 of them carry no model information). So the palette-level conditions alone do not force binary collapse at k = 6. The ladder finite facts (L5–L7: two-complement predicate over Fin 5 and Fin 6; hcomp unsatisfiable at k = 6; C = {0,1,3,4} plus {2,5} covers Fin 6 without an alternating triple) are confirmed.
- **Hypotheses:** Palette-field class only; 3 centres; condition C9 checked only at t = 0. Not a colouring.
- **Evidence:** Independent checker by the research desk (indep_ln2.py, exact Q(sqrt3) arithmetic).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/LN2/indep_ln2.py` — independent checker — `7b92389eb27be76e…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/research-desk/ln-checks/LN2/indep_ln2.out` — output — `7b424bb78c677c2f…`
- **Checked by the results desk:** 2026-11-15 ~03:25Z: re-ran indep_ln2.py from a scratch copy (python -I, exit 0): output identical to the archived one apart from timings, no FAIL lines.
- **Provenance:** L-N2 lane (chat-bb40251b97, owner research desk); research-desk checker 03:1xZ.
- **Correction history:** DISAGREES with the lane sub-claim C12 "A/C not binary for any pair": under the Lean BinaryCenter definition A is binary for {0,3}, {1,3}, {2,3} and C for {0,4}, {0,5}; nothing downstream is violated; ladder file:line citations only partly match (6/10); the ladder TRUE/UNPROVED verdicts on Lean steps are proof-status claims, not checked
- **Depends on:** [A6-PAIRED-PRODUCER](#a6-paired-producer)

### Q4Q5-CONTROLS

**q4, q5, q6 and controls are SAT in every phase cell of the relaxation** — `TESTED_FINITE`

- **Statement:** q4 (0,0,120,150,240,240), q5 (0,30,120,150,240,240), q6 (0,30,120,150,240,250), paired a (0,0,120,120,240,240) and b (0,60,…,300) are SAT on every positive phase cell, so the relaxation cannot exclude them; q4/q5 forced masks are pairs {1,4},{2,5},{0,3} on (0,30) and singletons {2},{3},{1} on (30,60).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T194118Z/q4-q5-forced-palette.json` — forced palettes — `c7a71a223470b5b0…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T194118Z/graph-m2-REPORT.txt` — graph m2 report §3 — `826555e70beeed2d…`
- **Checked by the results desk:** Re-ran the parent supervisor verify-inner-outer-orbits.js (see SIX-ORBIT): q4 counts (1,6), q5 (1,6), q6 (1,4,6), paired a (1,1), b (4,4); every cell SAT.
- **Provenance:** Parent + graph m2, check-in 19:41:18Z.
- **Correction history:** control b witness count: the parent supervisor verifier (re-run by the results desk, ~00:40Z) gives cyclic witness counts 4 and 4 on its two cells, agreeing with the graph m2 count of 4; the parent-relayed "(1,1)" is not reproduced
- **Used for:** Refutes TWO-TRIANGLE; motivates A7/A8.

### RELAX-WITNESSES

**Six-position interface relaxation is SAT for cycle lengths m = 3, 4, 5, 6** — `TESTED_FINITE`

- **Statement:** Exact SAT witnesses: m=3 q=(0,0,0) J={3} K={4}; m=4 (0,0,0,0) {4} {5}; m=5 (0,3,3,0,0) {0,2} {5}; m=6 (0,3,3,3,0,0) {0,2} {3,5}. So R1–R6 alone do not imply "no cycle".
- **Hypotheses:** Relaxation only; the m=6 geometry is excluded for actual interfaces by AC.
- **Evidence:** exact_obstacles.mjs (19 ms) + independent checker verify-certificates.mjs (PASS, 17 ms); referee ASTRA-REBOOT-REFEREE §7.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/astra-six-colour/exact_obstacles.mjs` — producer — `58de9a1ac5d198b4…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/astra-six-colour/exact-obstacles.json` — witnesses — `a0ca6c8b048d7d17…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/astra-referee/verify-certificates.mjs` — independent checker — `f4678bcb40700f92…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/astra-referee/certificate-check.json` — checker output — `b975a1e6220bfd78…`
- **Checked by the results desk:** 2026-11-15 ~00:23Z: copied the archived checker and its two input JSONs to a scratch folder and ran `node work/astra-referee/verify-certificates.mjs` (exit 0, 260 ms): status PASS, finiteCycles m=3,4,5,6 all accepted, 100 closed C5 words, 9 same-colour pairs; output matches the archived certificate-check.json apart from the runtime field.
- **Provenance:** Astra six-colour lead.

### A8-PALETTE

**A8 disjunctive palette report (unbanked, unreviewed)** — `CANDIDATE`

- **Statement:** Claims in ASTRA-DISJUNCTIVE-PALETTE-A8.txt; a claim-by-claim referee was requested but the geometry lane could not reach the file.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/ASTRA-DISJUNCTIVE-PALETTE-A8.txt` — report — `d292fa5a44fa857d…`
- **Provenance:** Coordinator cycles 222600, 224105, 232732 ("A8 remains unbanked").

### ALPHA-SHARP

**α = (0,2,3,184,185,186): six-phase SAT does not imply a field; fixed phase is not all-phase** — `CANDIDATE`

- **Statement:** For α* = (0,2,3,184,185,186) the configuration is SAT at the six census phases but fails by an empty residual at t = 92.5, so six-phase satisfiability does not imply a field.
- **Checked by the results desk:** No certificate located yet; requested.
- **Provenance:** Coordinator cycles 204019, 205744.

### FOURWAY-SPLIT

**Limits of the FiveSupport simplification: hn/hp are load-bearing; the four-way split is irreducible** — `CANDIDATE`

- **Statement:** Deleting hn/hp is refuted (tauto closes those goals by `assumption`); the four-way split at FiveSupport:225–231 is irreducible (witness (0,1,1,0)). v1 step_ban has no further consumers once the swap lands.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/automation-supervisor/inbox/20261115T002122-download-3-REFEREE.md` — swarm referee report — `4aa0931aefc47eb1…`
- **Checked by the results desk:** Not checked by the desk.
- **Provenance:** Architecture swarm smwh11dth; cycles 001551, 002122.

### GEOM-Q4Q5

**No q4/q5 disjunctive or hit argument forces a colour (T1, T2)** — `CANDIDATE`

- **Statement:** No q4/q5 disjunctive or hit argument forces a colour (lemmas T1 and T2); two referees agree.
- **Checked by the results desk:** Referee artifacts not yet located; status will move to PROVED_PAPER_REVIEWED when they are.
- **Provenance:** Geometry lane; coordinator cycle 231544.

### GEOM-TWO-STEP

**A unit triangle of two-step sums forces no colour (Theorems A and B)** — `CANDIDATE`

- **Statement:** A unit triangle of two-step sums forces no colour; the list rule is sound only at a single anchor.
- **Checked by the results desk:** No referee artifact located yet.
- **Provenance:** Geometry lane; coordinator cycle 204019.

### Q4Q5-APEX

**q4/q5 field bounds the apex colour, not the apex palette** — `CANDIDATE`

- **Statement:** Four geometry members agree that the q4/q5 field constrains the apex colour, not the apex palette; the open question is geometric reachability of the forcing bin triples (m4's 198 exact placements found none).
- **Checked by the results desk:** Not checked by the desk.
- **Provenance:** Geometry swarm smwh11xw7; cycle 001551.
- **Depends on:** [Q4Q5-PINNING](#q4q5-pinning)

### TERNARY-COUNTERMODEL

**Countermodel (3,4,5,3,4,5) satisfies the six-position facts** — `CANDIDATE`

- **Statement:** m1's countermodel (3,4,5,3,4,5) satisfies all six-position facts, so the k=6 ternary door needs a source-licensed third sector label.
- **Provenance:** Coordinator cycle 211858.

### A5-FAR-APEX

**Refuted: |A_far − ci| > 1.5 on the A5 sliver** — `RETRACTED_OR_REFUTED`

- **Statement:** The A5 domain file (§4, quoting the m2 report) claims |A_far − ci| > 1.5. This is false on part of P1: on u1 ∈ [0.201000, 0.204437], u3 ∈ [−0.215250438, −0.2152], |A2 − ci|² ∈ [2.2004, 2.2339] < 9/4. The weaker |A2 − ci| > 1 holds everywhere, so the conclusion that the far apex is outside H survives.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/cloud-supervisor/a5-sliver/CERTIFICATE.md` — certificate (Discrepancy section) — `d09708787fbe0e41…`
- **Provenance:** Research desk certificate 23:45:56Z.
- **Depends on:** [A5-SLIVER](#a5-sliver)

### A5-M5-TEMPLATE

**k=6 producer audit: the m=5 template is refuted** — `RETRACTED_OR_REFUTED`

- **Statement:** The m=5 template for the k=6 producer is refuted; the shortest open case is m=3 (triangle).
- **Provenance:** Independent lane; coordinator cycle 204019.

### AC-AXIS

**Unsigned-axis extension of AC is invalid** — `RETRACTED_OR_REFUTED`

- **Statement:** Extending AC to a common unsigned axis with per-continuum radial sides fails: K+ = [0,ρ], K− = [−ρ,0] have disjoint straddle sets (1,1+ρ) and (1−ρ,1) on the positive ray.
- **Evidence:** ASTRA-NONALIGNED-A3 §1 ("The proposed AC-axis argument is INVALID"); cone referee concurs.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-NONALIGNED-A3.txt` — refutation — `ce6e2f5f9fc98fae…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/ASTRA-CONE-REFEREE.txt` — referee — `76052706cc46ff8b…`
- **Provenance:** Astra A3; check-in 17:20:56Z.

### ALT-TRIPLE

**"A label set covers all labels iff it contains an alternating triple" is false** — `RETRACTED_OR_REFUTED`

- **Statement:** C = {0,1,3,4} covers all six labels and contains neither alternating triple; the general index-cycle vertex-cover criterion is retained.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/outputs/RESEARCH-STATUS.txt` — ESSENTIAL CORRECTIONS — `01c6c9d311eeae6b…`
- **Provenance:** Parent correction.

### CLAUDE05-VERDICT

**Claude05 verdict "no one-centre condition excludes the canonical palette" is contradicted** — `RETRACTED_OR_REFUTED`

- **Statement:** CLAUDE-THREE-PALETTE says none of the source's one-centre necessary conditions excludes the canonical palette and hand checks "lean towards the lists being colourable"; A5-FOUR-LIST (refereed) excludes it at one centre. Its "iff/exhaustive" claims are rejected as unproved (ASTRA-LIST-FIELD-A4 §8). The list-field derivation itself is re-verified.
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CLAUDE-THREE-PALETTE-2026-11-14.txt` — superseded report — `362a1d4e413b6f4a…`
- **Provenance:** Claude05 (Claude Max), 2026-11-14.
- **Depends on:** [A5-FOUR-LIST](#a5-four-list)

### OVERNIGHT-WITHDRAWN

**Overnight withdrawals: five-cycle shortcut, P3/H2 discharge, 681/720 cell family, canonical 3-cycle** — `RETRACTED_OR_REFUTED`

- **Statement:** Withheld or withdrawn: the angular five-cycle shortcut (8 countermodels to its licensed assumptions; Lemma 6.7 retained); the claimed H2 discharge (compact extensions do not compose) and related eigenfunction/uniform-deficit claims; the 681 excluded / 720 undecided cell-family theorem; "triple constraints force a canonical 3-cycle".
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/outputs/CONSOLIDATED-FINDINGS.txt` — record — `eac30d0ed71409ec…`
- **Provenance:** Overnight 13–14 Nov.

### PALETTE-EQ-F

**"409/969 realised-palette" route rejected: assumes palette = F** — `RETRACTED_OR_REFUTED`

- **Statement:** The route assumes palette = F, which is not licensed; the source gives only F ⊆ palette a.e.
- **Provenance:** Geometry lane referees; coordinator cycle 231544.

### TWO-TRIANGLE

**"Two-triangle" direction classification refuted** — `RETRACTED_OR_REFUTED`

- **Statement:** The claim that 4 or 5 distinct directions are impossible under CC60 + MC120(a) + a 60°-arc outer-strip premise is false: q4 (4 directions) and q5 (5 directions) pass the cone tests and are SAT; the premise misstates OA120 (needs an open 120° arc).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/openmath-supervisor/checkins/20261114T194118Z/q4-q5-forced-palette.json` — counterexamples — `c7a71a223470b5b0…`
- **Provenance:** TWO-TRIANGLE.md (check-in 18:35:22Z, self-labelled not independently verified); refuted by the parent the same check-in.
- **Depends on:** [Q4Q5-CONTROLS](#q4q5-controls)

## Infrastructure

### ENC-R4-AUX

**Auxiliary checks for the R4 refactor: witness selection, signature equivalence, fresh contexts** — `LEAN_VERIFIED`

- **Statement:** WitnessSelectionV4 (6 printed lemmas incl. `exists_strictAnti_scale'`), SignatureEquivalenceR5 (baseline theorem wrappers and definitional iff checks) and SignatureFreshR5 (control/fresh applications) compile; 14 printed axiom sets are standard.
- **Evidence:** witness-selection-v4.log, signature-equivalence-r5.log, signature-fresh-r5.log: Lean 4.34.1, exit 0, [propext, Classical.choice, Quot.sound].
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/encoding-r4/src/WitnessSelectionV4.lean` — source — `3ff5d5c86fd49e42…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/encoding-r4/src/SignatureEquivalenceR5.lean` — source — `bbc58eac177e99a2…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/encoding-r4/src/SignatureCheckFreshR5.lean` — source — `b0853a037a55d465…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/witness-selection-v4.log` — log — `1ad17940631fac6c…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/signature-equivalence-r5.log` — log — `909ec5e630255e14…`
  - `HadwigerNelson/Main/ResearchSnapshot/local/work/lean-queue/signature-fresh-r5.log` — log — `9e68cf42ede31dda…`
- **Checked by the results desk:** Read the archived log: Version 4.34.1, "Status: passed", "Exit code: 0", logged Source SHA256 equals the archived source (hash recomputed), axiom lines parsed. Did not recompile.
- **Provenance:** Encoding-r4 validation, 14 Nov ~03:00–07:09Z.
- **Correction history:** V1–V3 and R4 attempts failed (sorryAx) and were superseded
- **Depends on:** [ENC-R4](#enc-r4)

### SNAPSHOT-VALIDATION

**Repository research snapshot integrity** — `TESTED_FINITE`

- **Statement:** All 11,556 archived files (358,349,948 bytes) match MANIFEST.json, the frozen Lean source hashes match their validation records, and the finite graph certificates verify.
- **Artifacts:**
  - `HadwigerNelson/Main/verify-snapshot.mjs` — verifier — `eb40b4b59188cd81…`
  - `HadwigerNelson/Main/IMPORT-VALIDATION.json` — recorded run (18:58Z) — `6016a27ed9bba204…`
- **Checked by the results desk:** Re-ran 2026-11-14 23:50Z: status passed, exit 0, 11 s.
- **Provenance:** Supervisor import, 2026-11-14 18:57Z.

### LEAN-FAILED-REVISIONS

**Failed Lean jobs (superseded) — kept for the correction history** — `RETRACTED_OR_REFUTED`

- **Statement:** Jobs that exited 1 and were superseded: 205744-0 EvenWalk r1; 212205-1 StepBanShort r1 (Decidable; sorryAx in log); 213711-0 A6-Bridge-m2 (whnf timeout + shift-direction bug); 215215-0 EvenWalk r2; 215215-1 G1-Finish-mB r1; 220720-1 G3 standalone r1 (`le_or_lt`); 222600-0 EvenWalk r3; 232057-1 EvenWalk r5; 001551-0 CyclicCoreConsumerFromV2 (staged text began with a stray backslash, error "unexpected token" at 1:0; a staging defect, mathematics untested).
- **Artifacts:**
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t205744-0.progress.json` — record — `60a193944c7f9708…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t212205-1.progress.json` — record — `81fa534eed8a1fae…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t213711-0.progress.json` — record — `4672cd9e5714d3e0…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t215215-0.progress.json` — record — `1f7cfbfc1bd3339c…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t215215-1.progress.json` — record — `f26f8e8d3fdd6ad4…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t220720-1.progress.json` — record — `77a4f9b146600054…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t222600-0.progress.json` — record — `6f2ea526d6d66806…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261114t232057-1.progress.json` — record — `511113316141b418…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261115t001551-0.progress.json` — record — `6abd117b03d0e180…`
  - `HadwigerNelson/Main/ResearchSnapshot/import-20261115/work/lean-queue/claude-lean-20261115t001551-0.python.log` — log — `4b676e02a8b63d91…`
- **Checked by the results desk:** Read every record: exitCode 1 and recorded source hash = recomputed hash for each.
- **Provenance:** Local Lean queue, 2026-11-14 21:21–23:24Z.

### LEAN-435

**Rebuild under Lean 4.35.0: assigned to Carter** — `OPEN`

- **Statement:** Port and rebuild the team Lean results under the event toolchain (repo root: lean-toolchain leanprover/lean4:v4.35.0, lakefile Mathlib rev v4.35.0). All current Lean evidence in this ledger is Lean 4.34.1 with pinned Mathlib d13f23b; no team result has a 4.35.0 build yet. Handoff notes: HadwigerNelson/Lean/PORT-4.35.0-NOTES.md.
- **Checked by the results desk:** Not applicable.
- **Provenance:** Team decision (Jarom, 2026-11-15): reopened and assigned to Carter after a brief "not attempted" closure.
- **Correction history:** briefly closed as "not attempted (team decision)", then reopened and assigned to Carter
