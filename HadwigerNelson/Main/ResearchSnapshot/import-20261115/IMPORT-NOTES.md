# Import 2026-11-15 (results desk)

Captured 2026-11-15T06:37:51.125Z from the research workspace `C:/Users/jarom/Documents/Codex/2026-11-13/i` by the results desk. Files keep their workspace-relative paths under this folder; MANIFEST.json records each one with `source`, `sourceModifiedUtc` and `capturedAtUtc`. Compiled objects (.olean) are excluded, as in the original import. Nothing here was recompiled by the results desk: the excerpts below are copied from the existing compile records. See [../../../RESULTS-LEDGER.md](../../../RESULTS-LEDGER.md) for the reviewed status of each result.

## Banked Lean results: exit code and `#print axioms` excerpts

Environment for all rows: Lean 4.34.1 (commit 5045d0056413266e57c625dcd7c365b10e377c52), Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612, threecentre-r1 build path.

### A6-FORCING

- Job `claude-lean-20261114t212205-0`: status `passed`, exitCode `0`, 62.72 s, finished 2026-11-14T21:25:32.533605+00:00
- Source `work/lean-queue/claude-admissions/claude-lean-20261114t212205-0/Candidate.lean` sha256 `27e45caf4c79389767a97d8bf705980462849d4f0a6d268e849989b253a916c8` (recomputed: match)
- **No `#print axioms` output in this record.**

### STEPBAN-V2

- Job `claude-lean-20261114t220720-0`: status `passed`, exitCode `0`, 64.62 s, finished 2026-11-14T22:10:43.295156+00:00
- Source `work/lean-queue/claude-admissions/claude-lean-20261114t220720-0/Candidate.lean` sha256 `19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655` (recomputed: match)

```
'OAI.EuclideanFiveColor.five_support_step_ban_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### STEPBAN-V2 (duplicate run)

- Job `claude-lean-20261114t222227-0`: status `passed`, exitCode `0`, 176.67 s, finished 2026-11-14T22:26:56.011457+00:00
- Source `work/lean-queue/claude-admissions/claude-lean-20261114t222227-0/Candidate.lean` sha256 `19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655` (recomputed: match)

```
'OAI.EuclideanFiveColor.five_support_step_ban_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### A6-BRIDGE-R2 + G1-R2

- Job `claude-lean-20261114t231544-0`: status `passed`, exitCode `0`, 66.86 s, finished 2026-11-14T23:18:26.825637+00:00
- Source `work/lean-queue/claude-admissions/claude-lean-20261114t231544-0/Candidate.lean` sha256 `74402da9ef754964e3a732c879e1b31fa3af419db1a465255e6a78b467f9b333` (recomputed: match)
- Axioms from `work/research-desk/bridge-r2-axioms/axioms.log`

```
'OAI.EuclideanFiveColor.A6.ae_restrictions' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.ae_six_inputs' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.ae_canonical_subpalette' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.ae_canonical_subpalette_global' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.cos_sign_strict' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.sign_of_paired_fin' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.signTable_of_paired' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.signTable_of_paired_fin' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### STEPBAN-CONSUMER

- Job `claude-lean-20261114t232057-0`: status `passed`, exitCode `0`, 58.56 s, finished 2026-11-14T23:23:27.058924+00:00
- Source `work/lean-queue/claude-admissions/claude-lean-20261114t232057-0/Candidate.lean` sha256 `718b581518b553c471e9a984dc0dd44e8d6c54d3d9ed25209f1728a8a3a7310e` (recomputed: match)

```
'OAI.EuclideanFiveColor.five_support_step_ban_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.five_opposite_contacts_false_from_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### G3-R2

- Desk compile (research desk, same toolchain). Source `work/research-desk/G3-r2/G3-ArcCover-r2.lean` sha256 `39a02e68c878c0d0df0493d53114679ffd6cb01c3354329cd33f3867b9558c6e`
- Desk log line: `2026-11-14T22:32:04Z G3-r2 local compile PASSED exit 0, 83 s; arcCover axioms [propext, Classical.choice, Quot.sound]; 0 errors/sorry; log research-desk/G3-r2/compile.log`
- Axioms from `work/research-desk/G3-r2/compile.log`

```
'OAI.EuclideanFiveColor.A6.arcCover' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### G1-R2 (standalone)

- Desk compile (research desk, same toolchain). Source `work/research-desk/G1-r2/G1-Finish-mB-r2.lean` sha256 `fd3549e5acccd7b5ed18dbcc09c0e91c0dc03e638b6ee48d2efea734e27385d4`
- Desk log line: `2026-11-14T23:49:28Z G1-Finish-mB-r2 desk compile PASSED (100 s, std axioms); ledger updated`
- Axioms from `work/research-desk/G1-r2/compile.log`

```
'OAI.EuclideanFiveColor.A6.cos_sign_strict' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.sign_of_paired_fin' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.signTableT_of_paired' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.A6.signTableT_of_paired_fin' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### A6-BRIDGE-R2-G3

- Desk compile (research desk, same toolchain). Source `work/research-desk/Bridge-r2-G3/A6-Bridge-r2-G3.lean` sha256 `2e04f2115ac3b561f59946c652d8010005f88da57fe3eea782a0d5ef71e77334`
- Desk log line: `2026-11-15T00:32:22Z A6-Bridge-r2-G3 desk compile PASSED exit 0 167 s; ae_canonical_subpalette_unconditional std axioms; no sorry`
- Axioms from `work/research-desk/Bridge-r2-G3/compile.log`

```
'OAI.EuclideanFiveColor.A6.ae_canonical_subpalette_unconditional' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### STEPBAN-CYCLICCORE

- Desk compile (research desk, same toolchain). Source `work/research-desk/CyclicCore-r2/CyclicCoreConsumerFromV2-r2.lean` sha256 `1212d4e1825c0b652219956445909cbaa96700f3ad7d1016737b369c515a61cc`
- Desk log line: `2026-11-15T00:34:32Z CyclicCoreConsumerFromV2-r2 (inbox file minus stray '\' line 1) desk compile PASSED exit 0 122 s; #check pair identical; _from_v2 std axioms`
- Axioms from `work/research-desk/CyclicCore-r2/compile.log`

```
'OAI.EuclideanFiveColor.five_sequence_small_no_accumulation_from_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### FIVESUPPORT-SWAP (R1 port)

- Desk compile (research desk, same toolchain). Source `work/research-desk/FiveSupport-swap/FiveSupportSwapR1.lean` sha256 `e531cf133a213e524b00008a9956c9206d98f09fb1a0faff3ae5ff35080f2c9f`
- Desk log line: `2026-11-15T01:01:32Z FiveSupportSwapR1 PASSED exit 0 323 s; five_opposite_contacts_false + five_support_step_ban_v2 std axioms; 31/31 public #check signatures identical to R1 FiveSupport. Deleted desk .olean/.ilean outputs (disk rule)`
- Axioms from `work/research-desk/FiveSupport-swap/swapR1.log`

```
'OAI.EuclideanFiveColor.five_opposite_contacts_false' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.five_support_step_ban_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### FIVESUPPORT-SWAP (v1 deleted)

- Desk compile (research desk, same toolchain). Source `work/research-desk/FiveSupport-swap/FiveSupportSwapR1-noV1.lean` sha256 `0aaee265081c94ba692f3d0c91ca9a58770108c99013942ab81ac390f7daea86`
- Desk log line: `2026-11-15T01:17:25Z FiveSupportSwapR1-noV1 PASSED 181 s; 30/30 signatures identical; v1 deletion verified; ledger updated`
- Axioms from `work/research-desk/FiveSupport-swap/noV1.log`

```
'OAI.EuclideanFiveColor.five_opposite_contacts_false' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.five_support_step_ban_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### A6-FORCING (axiom spot-check)

- Desk compile (research desk, same toolchain). Source `work/research-desk/spotcheck/A6Forcing-axioms.lean` sha256 `83e6dfa36be808073a9591eb5fca67d01390c00cde2a5374c1c9c6a6dc5e8178`
- Desk log line: `not found`
- Axioms from `work/research-desk/spotcheck/A6Forcing-axioms.log`

```
'A6Forcing.a6_canonical_pairs' depends on axioms: [propext, Classical.choice, Quot.sound]
'A6Forcing.a6_canonical_pairs_add_three' depends on axioms: [propext, Classical.choice, Quot.sound]
'A6Forcing.a6_containment_unsatisfiable' depends on axioms: [propext, Classical.choice, Quot.sound]
'A6Forcing.a6_hypotheses_satisfiable' depends on axioms: [propext, Classical.choice, Quot.sound]
'A6Forcing.disjointness_necessary' depends on axioms: [propext, Classical.choice, Quot.sound]
'A6Forcing.outer_hit_necessary' depends on axioms: [propext, Classical.choice, Quot.sound]
'A6Forcing.A6canonical_hypotheses' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### EVENWALK-R6

- Desk compile (research desk, same toolchain). Source `work/research-desk/EvenWalk-rev6/EvenWalkReachability-rev6.lean` sha256 `4439cf5dd4088ea6765337286399f5af462fd1c3f4976c82c99d77019bfb9904`
- Desk log line: `2026-11-14T23:27:27Z EvenWalk rev6 desk compile PASSED exit 0 63 s, 3 endpoints standard axioms; StepBanConsumer 232057-0 PASSED; sent both to coordinator via user-inbox; touched WAKE_COORDINATION`
- Axioms from `work/research-desk/EvenWalk-rev6/compile.log`

```
'OAI.EuclideanFiveColor.evenWalk_reachable' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.finite_list_obstruction' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.two_list_obstruction_of_even_walk' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### R1 root axioms

- Job `threecentre-r1-axiomroots`: status `passed`, exitCode `0`, 68.72 s, finished 2026-11-14T20:48:14.977884+00:00
- Source `work/lean-queue/threecentre-r1/src/AxiomRoots.lean` sha256 `cac851851383970f3d33e42c8bf4ae4ce5963059f43c44328f12542bbf96f26d` (recomputed: match)

```
'OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlaneFiveColor.Spectral.finite_uniform_successor_contradiction' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlaneFiveColor.Spectral.relative_singularity_successor' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlaneFiveColor.Spectral.relative_singularity_approximation' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.no_proper_five_coloring' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Problem160.properColoring_seven' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Problem160.weakMeasurableColoring_seven' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Contents

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `work/lean-queue/claude-admissions/claude-lean-20261114t205744-0/Candidate.lean` | 15630 | `081d89537f0548148f25a6790f975cdf75863bb977150bbf156b1ff665ff1c01` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t212205-0/Candidate.lean` | 12174 | `27e45caf4c79389767a97d8bf705980462849d4f0a6d268e849989b253a916c8` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t212205-1/Candidate.lean` | 4168 | `fbcd3f139bf8725245ce59c6887c9be067a7bafe4f22ba0d29b94b1f83c71d28` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t213711-0/Candidate.lean` | 15449 | `3ac02303c7112cdcfb9aea9f7b2febd0ee106087435c009547df126498a0cc9e` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t215215-0/Candidate.lean` | 16732 | `3adb35ed4c5ab9f370279df992a9d20c4f622e5004bed4d41a57f1f2de88a33c` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t215215-1/Candidate.lean` | 18606 | `2be419fa16f26b6f3fd1d16b20f9fa7993443e5804b9fcbbcc117f207c0482f6` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t220720-0/Candidate.lean` | 5755 | `19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t220720-1/Candidate.lean` | 9426 | `f3da75d1274efdc281652b0422f61b9b0b9e098fc752712446d23fd847875270` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t222227-0/Candidate.lean` | 5755 | `19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t222600-0/Candidate.lean` | 18319 | `8731e2f56a5a33307ffaf73eec02da5cf243cfc58b14bc6f7e72a6190a0e466f` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t231544-0/Candidate.lean` | 40189 | `74402da9ef754964e3a732c879e1b31fa3af419db1a465255e6a78b467f9b333` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t232057-0/Candidate.lean` | 16619 | `718b581518b553c471e9a984dc0dd44e8d6c54d3d9ed25209f1728a8a3a7310e` |
| `work/lean-queue/claude-admissions/claude-lean-20261114t232057-1/Candidate.lean` | 18827 | `7daed4740626d178760fea23f6a007189db873b6568a864902934e75fe7bad43` |
| `work/lean-queue/claude-admissions/claude-lean-20261115t001551-0/Candidate.lean` | 8020 | `cb8a35d78cc87e212f838ce143f46dbdf93622e5b0adbf08b2ac50794af4d923` |
| `work/lean-queue/claude-admissions/claude-lean-20261115t031143-0/Candidate.lean` | 5755 | `19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655` |
| `work/lean-queue/claude-lean-20261114t205744-0.progress.json` | 3848 | `60a193944c7f9708bf40aa71a35a309f57b3c69567c1074f5d6d00dd87cd502a` |
| `work/lean-queue/claude-lean-20261114t212205-0.progress.json` | 3406 | `729f92a0cf31b8e5ab2d59be7966bc76d5aa595071f0cca6d7b2f4f6385a8f54` |
| `work/lean-queue/claude-lean-20261114t212205-1.progress.json` | 3415 | `81fa534eed8a1fae883f33b236a1d3957f5722221bd9786c43f6ad8e4a028e5b` |
| `work/lean-queue/claude-lean-20261114t213711-0.progress.json` | 3605 | `4672cd9e5714d3e047a364f51b56eaf630de90846470a80240c899df30ea54ac` |
| `work/lean-queue/claude-lean-20261114t215215-0.progress.json` | 3628 | `1f7cfbfc1bd3339c1440ccac27ccb8759207e24e548e5e75980695c5b1a98961` |
| `work/lean-queue/claude-lean-20261114t215215-1.progress.json` | 3466 | `f26f8e8d3fdd6ad4f55cd52481d10d01eb9e1c3958208f52644c0ae4bdeec425` |
| `work/lean-queue/claude-lean-20261114t220720-0.progress.json` | 3397 | `1bd90cc006806f4ec222757e986652c1c786c779fb7f2c36840d43687b6a1593` |
| `work/lean-queue/claude-lean-20261114t220720-1.progress.json` | 3328 | `77a4f9b1466000548facde54b74b9dfcb1e993de59403a586d7802d8d3a3536f` |
| `work/lean-queue/claude-lean-20261114t222227-0.progress.json` | 3663 | `f2803e863e1a8530b006b0e3b7a29f9bb59b6c452c94a19c07e0cb92112c4d59` |
| `work/lean-queue/claude-lean-20261114t222600-0.progress.json` | 3364 | `6f2ea526d6d66806fdb0a6daf0c173691f3fc2bb14d7fd5038ba6dd6d30947ad` |
| `work/lean-queue/claude-lean-20261114t231544-0.progress.json` | 3550 | `5c7b4cb2f3ff873b8bc5c87bb70e46fd1dea4d0ffc0f478bbcb12dd7614cdc5a` |
| `work/lean-queue/claude-lean-20261114t232057-0.progress.json` | 3554 | `03d7116c943d8a2947e5cc273f79e9e3e3ca11601744482554af9d3cd287b018` |
| `work/lean-queue/claude-lean-20261114t232057-1.progress.json` | 3461 | `511113316141b4184c818f1d96b6833e7e824ae81ce5c324dca82cb11a5497eb` |
| `work/lean-queue/claude-lean-20261115t001551-0.progress.json` | 3568 | `6abd117b03d0e180e140dda18a20a52eef6425aeff837e8d47dea9ca61cef5ff` |
| `work/lean-queue/claude-lean-20261115t031143-0.progress.json` | 3597 | `859d21e3c37eebc39cfa64d024b373c122631da4e4595cd19b21b19b5c2e2f15` |
| `work/lean-queue/claude-lean-20261114t205744-0.python.log` | 19218 | `0ba87c5f89d850e300b4080c2e35f6975d0c97489f0fe7fb6df2dec1d274d934` |
| `work/lean-queue/claude-lean-20261114t212205-0.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/claude-lean-20261114t212205-1.python.log` | 1644 | `fa2c81635f24c9474aebacdfef543579fc2321183f6287000fc4b8fed43c8c4c` |
| `work/lean-queue/claude-lean-20261114t213711-0.python.log` | 908 | `b07b1a4f1205cd28efc34c48716406d3b817056d466e6881f64a51afbee62414` |
| `work/lean-queue/claude-lean-20261114t215215-0.python.log` | 10699 | `0eb58242ec553de383f0245dd31aae5d31ccdc1ef09ec4d1cf1f27ba8ba1c9ed` |
| `work/lean-queue/claude-lean-20261114t215215-1.python.log` | 760 | `bb63908de9326585f10afea25fd4fb9fd7ffcf5124d6a7051938e492bde7f2f2` |
| `work/lean-queue/claude-lean-20261114t220720-0.python.log` | 1148 | `d1e054998bdb19b5a2e555c3d386d783a512f9db34d5c38e82e7f386609bcfd9` |
| `work/lean-queue/claude-lean-20261114t220720-1.python.log` | 798 | `f5e36cdb335db8b19d49869d7c363eb316b0cc6db98fc9c59ec6492cfb2bea83` |
| `work/lean-queue/claude-lean-20261114t222227-0.python.log` | 1148 | `d1e054998bdb19b5a2e555c3d386d783a512f9db34d5c38e82e7f386609bcfd9` |
| `work/lean-queue/claude-lean-20261114t222600-0.python.log` | 9417 | `3f7b20dc10d1e65fb3cd4d43d35ddf08dd29234147412fecaf386f9c670482dc` |
| `work/lean-queue/claude-lean-20261114t231544-0.python.log` | 1128 | `bdcc69a00d00bb0e3bb7816f044053fde29afbbf17233bd57de1851bd1198665` |
| `work/lean-queue/claude-lean-20261114t232057-0.python.log` | 2083 | `a8886d567be5d8d8156dfd676bee6f7a91f953be9cef823718d3370dd8e6285c` |
| `work/lean-queue/claude-lean-20261114t232057-1.python.log` | 2494 | `8a20747d7708aaad87f117ff57be2fc9a27beddee523747f72af990e9009b3e0` |
| `work/lean-queue/claude-lean-20261115t001551-0.python.log` | 381 | `4b676e02a8b63d91ef7852b1d6bd02c3090f7092ca77660cf27f986cbdbc472c` |
| `work/lean-queue/claude-lean-20261115t031143-0.python.log` | 1148 | `d1e054998bdb19b5a2e555c3d386d783a512f9db34d5c38e82e7f386609bcfd9` |
| `work/lean-queue/threecentre-r1-13-graphrealization.log` | 239 | `fa6cb0531c5f4cc732bba0dbdba66968ba6495fa1d86fe1d1861ee70e2c1bc2b` |
| `work/lean-queue/threecentre-r1-14-interfaces.log` | 239 | `3d03786828e1624bfe5cb5de57d962cfe2c9e6905c82d2ca7fb4bd82986f720d` |
| `work/lean-queue/threecentre-r1-15-sectors.log` | 241 | `c56884d17bef3d364390ddd48f807a93073d0e20b380c6755aa8e39440e0bfe5` |
| `work/lean-queue/threecentre-r1-15-sectors.progress.json` | 3795 | `e6eab3c5a08f73bfc6b1c0ebb6f95b76c515f6c818a304462bf03bb6a6242500` |
| `work/lean-queue/threecentre-r1-16-continuumlimits.progress.json` | 3561 | `e6bc06857621e012fc8aa17fed948a2716a623e02197c40ca4e8cdfa90fb307e` |
| `work/lean-queue/threecentre-r1-17-diskextension.progress.json` | 3558 | `f83d6114ac1e6e85140e2d7e3b4e21c3b67473b99a6402d4cec8e1b56609e26a` |
| `work/lean-queue/threecentre-r1-18-graphcuts.progress.json` | 3518 | `bfe9e8261eeafd000ce110eee0c10400883659e95c3fe69697b16af8026186c7` |
| `work/lean-queue/threecentre-r1-19-holeapproximation.progress.json` | 3573 | `bec93b2e21ffe6651c52712da0420ca47fcb0104980e8b1174b8312f27f0f31d` |
| `work/lean-queue/threecentre-r1-20-graphpatches.progress.json` | 3550 | `5f97758161263289adb88b771a4bf25fa800dee35e1fba8a05ba21aa2434a56f` |
| `work/lean-queue/threecentre-r1-21-fullapproximation.progress.json` | 3576 | `82af98e9a41f87134eaa74c503d12d7c2a809da6b6c523d29bcf87729f5e0746` |
| `work/lean-queue/threecentre-r1-22-mesh.progress.json` | 3498 | `48678157ddfff53d69e72bd8cd8b780ef57247965f03c7ced3f62d5557716ae9` |
| `work/lean-queue/threecentre-r1-23-five.progress.json` | 3490 | `382451de5d766da9209cf3bff0f3e722de74dacdc59fd60db1f6c0b2692f08dd` |
| `work/lean-queue/threecentre-r1-24-chromatic.progress.json` | 3522 | `86efcbb75457e823fcca6e8ada49f05d4071ac5fa5a0ae481c53d8ca1ccebddb` |
| `work/lean-queue/threecentre-r1-25-converse.progress.json` | 3519 | `51096377d5c3f4af7975f6b024b57ffd5cfa92bef96037c13f18df5dd48065f8` |
| `work/lean-queue/threecentre-r1-26-nullsetrobust.progress.json` | 3543 | `d592dd1834d07d2acdf16a7d55da31a46f7aedd901c35ff15d3f156d88fd2235` |
| `work/lean-queue/threecentre-r1-27-transfer.progress.json` | 3525 | `f0bf78d3b7b482a7ea7dbc22dc2dc0026a1144a587e843ae292530978ed38b72` |
| `work/lean-queue/threecentre-r1-15-sectors.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-16-continuumlimits.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-17-diskextension.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-18-graphcuts.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-19-holeapproximation.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-20-graphpatches.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-21-fullapproximation.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-22-mesh.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-23-five.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-24-chromatic.python.log` | 581 | `bae247cd36091170573dd614431639f722d39c84475ef773532e0e5b8077803d` |
| `work/lean-queue/threecentre-r1-25-converse.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-26-nullsetrobust.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-27-transfer.python.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work/lean-queue/threecentre-r1-axiomroots.progress.json` | 3345 | `ca4b961283a98933d08ccfdd6ca490e05945bbd4f6a12c065b1c2dbd52f173a9` |
| `work/lean-queue/threecentre-r1-axiomroots.python.log` | 3506 | `85aaef1671d5777e50378e07a2f2c94cedd630c610fbe9fc7c4d0601c8d6df29` |
| `work/research-desk/BANKED.md` | 9903 | `d5ba3a6f80cd6c8ac1ba82168ba614fa31d8263476b6ae5746f2f399212dd437` |
| `work/research-desk/LOG.md` | 14706 | `5ae120414f51f6d718d87977496060e3a8d27dd144980d1d7a019353b9fefb56` |
| `work/research-desk/G3-r2/G3-ArcCover-r2.lean` | 9476 | `39a02e68c878c0d0df0493d53114679ffd6cb01c3354329cd33f3867b9558c6e` |
| `work/research-desk/G3-r2/compile.log` | 96 | `e1a47fad00213af7a5bfff1a1a8db0403e6d941814cc164b7dc6b8177767203a` |
| `work/research-desk/EvenWalk-rev6/EvenWalkReachability-rev6.lean` | 19063 | `4439cf5dd4088ea6765337286399f5af462fd1c3f4976c82c99d77019bfb9904` |
| `work/research-desk/EvenWalk-rev6/compile.log` | 1561 | `23bc2c29a2846046d3041e54f7d79519090e49159b046c67f0e320fc05493634` |
| `work/research-desk/bridge-r2-axioms/Axioms.lean` | 324 | `5c94e491337de75d4623858f0ef236c8699b274f063cda4cb292b31a2363632a` |
| `work/research-desk/bridge-r2-axioms/axioms.log` | 860 | `31893654154de1e638f12913bfdcdd35e1eb4c960ca8e378876cd1aba3ebd625` |
| `work/research-desk/census/census.py` | 7385 | `fa6436d577d4a1c1b604431b0250d35a01564307472b7a087556a794f0759702` |
| `work/research-desk/census/census_full.out` | 313 | `a2c2df5acae23a79aa8b12f780f40019ad206a88e85f5b46927eb149c6b75d2f` |
| `work/research-desk/census/independent_census.py` | 3232 | `175b6861afbe4467071da852cc977adbe74d2d028dfd1bbaf0f9bf3a0f4dbf81` |
| `work/research-desk/census/independent_census.out` | 213 | `1ac79d65205b9e49cb28f886a33c7517c7ca6bee27a58e071ea56681ca191282` |
| `work/research-desk/G1-r2/G1-Finish-mB-r2.lean` | 18901 | `fd3549e5acccd7b5ed18dbcc09c0e91c0dc03e638b6ee48d2efea734e27385d4` |
| `work/research-desk/G1-r2/compile.log` | 1147 | `fbf7d62384b9f62cf60b14cf64f30f35a71fac30469ed4ff5bfea8df5a37e572` |
| `work/research-desk/Bridge-r2-G3/A6-Bridge-r2-G3.lean` | 44390 | `2e04f2115ac3b561f59946c652d8010005f88da57fe3eea782a0d5ef71e77334` |
| `work/research-desk/Bridge-r2-G3/compile.log` | 847 | `b670399ddedbfdc832cd408da6cb7824f1c3471351006cec790ae77879baca2c` |
| `work/research-desk/CyclicCore-r2/CyclicCoreConsumerFromV2-r2.lean` | 8165 | `1212d4e1825c0b652219956445909cbaa96700f3ad7d1016737b369c515a61cc` |
| `work/research-desk/CyclicCore-r2/compile.log` | 804 | `b90e12cf06aa5cf556c3c11eb5c4375d12688dfeed9eee1d8abcdaaa4d2cccd2` |
| `work/research-desk/FiveSupport-swap/swap.log` | 10430 | `41d849c3929bf37bf3bb8cdf365d360d1e0567d87142b458a2f8521afff9c419` |
| `work/research-desk/FiveSupport-swap/FiveSupportSwapR1.lean` | 25380 | `e531cf133a213e524b00008a9956c9206d98f09fb1a0faff3ae5ff35080f2c9f` |
| `work/research-desk/FiveSupport-swap/swapR1.log` | 10325 | `7bbaece10131d754ed62845653384de4a7534b9a8b9e0a7c07b25a319cc09092` |
| `work/research-desk/FiveSupport-swap/orig.log` | 10103 | `749c21cfff0461ad92f6640ad7e8c82a18386f9b625cc9ef3feeb75d928012a9` |
| `work/research-desk/FiveSupport-swap/OrigChecks.lean` | 1697 | `235cefcf2e8c0923843244e49d0849a24eac8d42ff56d2da32e8ec05d84f6e11` |
| `work/research-desk/FiveSupport-swap/FiveSupportSwap.lean` | 28320 | `aa0c4cb692f6e8e8a131825050e02bc433dd9d201b3bdc1b0eadf099de933e7e` |
| `work/research-desk/FiveSupport-swap/FiveSupportSwapR1-noV1.lean` | 23780 | `0aaee265081c94ba692f3d0c91ca9a58770108c99013942ab81ac390f7daea86` |
| `work/research-desk/FiveSupport-swap/noV1.log` | 9437 | `4d9e0814064756a20ab550cfed7e58e6d8f5152b03e8e17b88fb17926a366be2` |
| `work/research-desk/spotcheck/A6Forcing-axioms.lean` | 12512 | `83e6dfa36be808073a9591eb5fca67d01390c00cde2a5374c1c9c6a6dc5e8178` |
| `work/research-desk/spotcheck/A6Forcing-axioms.log` | 666 | `31518f332044b24f412eca03b4ae710202f65becab8ad488b423c93be2a43357` |
| `work/research-desk/ln-checks/LN1/indep_ln1.py` | 15991 | `b6c3e7b4fc59fc05632a3c148c7006c73803b3f3a14f2bd647216a0beb73ef4e` |
| `work/research-desk/ln-checks/LN1/indep_ln1.out` | 4183 | `401c98a9a9fe8af4a936f4625c0cd12154660c0f30d8dc4be45f58990f4452e7` |
| `work/research-desk/ln-checks/LN1/indep_ln1_xcheck.out` | 4324 | `79391329868fdfbc0e59b7c19edfd40bde48f6641298ae5faa996c16bca3cf74` |
| `work/research-desk/ln-checks/LN2/indep_ln2.py` | 33717 | `7b92389eb27be76e2cfc92df0d432ce9b6380d9bbc551700430044db60faf839` |
| `work/research-desk/ln-checks/LN2/indep_ln2.out` | 14219 | `7b424bb78c677c2f67606499c44f50db0e0a80c7857131135e45d3a5af2f50c3` |
| `work/research-desk/ln-checks/LN3/indep_ln3.py` | 22385 | `fdbaf0c04632ea1bab408f144a897e74c934869ae6045f891473e2473d4eb3d6` |
| `work/research-desk/ln-checks/LN3/indep_ln3.out` | 5921 | `9f478cfc9519b8bd7d572daac0f90f2051c728109ba30692533704ff2bca430b` |
| `work/research-desk/ln-checks/SIGNCELL/indep_signcell.py` | 30617 | `e556895c0de11ff5ea3fe9b2e092bb90ffcc712d89fcb41cdd90ad7d7b79a90a` |
| `work/research-desk/ln-checks/SIGNCELL/indep_signcell.out` | 6268 | `b7a5890d91d2fae52198230a3ab42439bd4bea3272c3b3fc41a85d972f848290` |
| `work/research-desk/ln-checks/SIGNCELL/desk_sat_dump.py` | 876 | `b038995fe7f55263ddd56529ce4e80d1ff4f244290c70b35ae7cd0a3f6ed7ff9` |
| `work/research-desk/ln-checks/SIGNCELL/desk_sat_dump.out` | 345 | `e158706474bfa1e35b288bf34cddde89a1143b1697bbed2d72c07048b03889b4` |
| `work/research-desk/ln-checks/SIGNCELL/desk_sat177.txt` | 2301 | `9d5c7686b6064a181da7c2b60386ba48e4834abd99169c5adf2d82ee6317d909` |
| `work/research-desk/contracts/ConsumerContracts.lean` | 4690 | `a3ea701ab15d29a7941f27ac02566feca014b4ae241d5a1b49abba404055c57f` |
| `work/research-desk/contracts/compile.log` | 16399 | `6ee4315e14db61b84f3d4b15c05fb2c1bdc0f198ec26844ed104aeb3eef05eb7` |
| `work/cloud-supervisor/a5-sliver/CERTIFICATE.md` | 7196 | `d09708787fbe0e41b96b7ebac5c3cc5bed60d06baebfb08c14dd75434edfa173` |
| `work/cloud-supervisor/a5-sliver/README.md` | 1427 | `ed053b8bcbf63e10111957f57b9a61a73183b7d7b8c30284303b5b30bd28adba` |
| `work/cloud-supervisor/a5-sliver/certify_sliver.py` | 11877 | `63e84a36bfa95ea99103e314530dbaf38a9fa42667a8ac85b960882ff351e341` |
| `work/cloud-supervisor/a5-sliver/certificate_output.txt` | 2677 | `68507c241873c543d5e56d7c6e162fb46ba96c1d19bbd431ad4b763fb4bfba41` |
| `work/cloud-supervisor/a5-sliver/certify_full.py` | 7210 | `25ab2cfa85d28bf232b6fc5c92e4242d1b74504af40e5ff09c9760c42b00a429` |
| `work/cloud-supervisor/a5-sliver/full_output.txt` | 806 | `c076169b95b00432534c462f82ca9e69b07fa2c2157385ed31a905173de34839` |
| `work/cloud-supervisor/a5-sliver/certify_arc_ends.py` | 4239 | `8ea21bf663493518696487cea22fa433521122e6840a7bf1b330706e0df8a6f5` |
| `work/cloud-supervisor/a5-sliver/arc_ends_output.txt` | 2512 | `045489e1e380f1618c0a29884b25f0a5e7441c488776d34b0758cf04db04c903` |
| `work/automation-supervisor/inbox/20261114T224105-download-4-A5-SLIVER-DEFS.md` | 15314 | `714b2eb2a7eeb9a899774748855d2e6ec65ce231075579df145464ab04849f6d` |
| `work/automation-supervisor/inbox/20261115T002122-download-1-FiveSupport-swap.lean` | 27124 | `3291ad95a0c3cc82b71df83ef16ebb63e6fe0691721c391815e7298dc3c732ff` |
| `work/automation-supervisor/inbox/20261115T002122-download-2-FiveSupport-swap.diff` | 6625 | `a33fa8dbccaae12b8f885dcae96ea1da7f017b2b761e531150ea07488268b9ba` |
| `work/automation-supervisor/inbox/20261115T002122-download-3-REFEREE.md` | 25682 | `4aa0931aefc47eb10ef7301b7309efe51b0161d63f29aa4c279390a223d48ced` |
| `work/automation-supervisor/inbox/20261115T002122-download-5-STATUS.json` | 69078 | `ccc9384768d9534a579ab4045fe30742a2f910dd2405bc2028ae60c0c5ccfbc6` |
| `work/automation-supervisor/inbox/20261114T205744-download-5-ALL-PHASE-REFEREE.md` | 10612 | `087e6efc55b766cdf07bd4a8abd9c4f77896a300bcc6010a6d87ad72783c33e2` |
| `work/openmath-supervisor/checkins/20261114T191820Z/inner-outer-orbit-certificates.json` | 115033 | `6f546fb260b779a5bd05cee38bebd01894224da23861fd97c74fb990f185d67e` |
| `work/openmath-supervisor/checkins/20261114T191820Z/verify-inner-outer-orbits.js` | 1648 | `ae6c4d2beebe8c96c35cc9335ba6df34910693d7a498e81137903a585b2ce279` |
| `work/openmath-supervisor/checkins/20261114T191820Z/PROGRESS-REPORT.txt` | 2112 | `8973d2a1936137675d767cab21f0795d39193288a4596acd57ff1615618c3d96` |
| `work/openmath-supervisor/checkins/20261114T194118Z/graph-m2-REPORT.txt` | 11109 | `826555e70beeed2d6b1f8bf0559f5d0cfc9886087b7f8b5c033bce39e0f2eadc` |
| `work/openmath-supervisor/checkins/20261114T194118Z/q4-q5-forced-palette.json` | 2319 | `c7a71a223470b5b00db33d2ad901954907f0ffb441c9e7119ef292ba06e1641b` |
| `work/openmath-supervisor/checkins/20261114T194118Z/corner-all-phase-validation.json` | 1957 | `15a31adcb7c5ee267ca1e7d0c66b27d322bc36d518265d91ef991fd619efbcf6` |
| `work/openmath-supervisor/checkins/20261114T194118Z/PROGRESS-REPORT.txt` | 3586 | `8f6744bf837882600e2f7b71b2dce0cb048efecf36b39f13d6ea3d56b578ca33` |
| `work/openmath-supervisor/checkins/20261114T183522Z/PROGRESS-REPORT.txt` | 2480 | `c2aa01a9d8cebfd1dcd5f81c9c61c9434fbcef4c2d6bdc42858564fbb46444fc` |
| `work/openmath-supervisor/checkins/20261114T183522Z/TWO-TRIANGLE.md` | 4257 | `507982dc9879158e42512a5e09ee41e84e88d99f2b74a62c3d3966542caadb87` |
| `work/openmath-supervisor/checkins/20261114T200919Z/PROGRESS-REPORT.txt` | 7525 | `4a8423bb7092235b8bc6ce95b471938ee9e1e2cad5915eb2180afdec7eaa0fc8` |
| `work/openmath-supervisor/checkins/20261114T200919Z/CHECKIN.json` | 780 | `8f4c53eb956044f424de14b213c589b2d16983bc754d1726d0f6c5e6b7f8650b` |
| `work/openmath-supervisor/checkins/20261114T200919Z/fixed-phase-census.json` | 1447788 | `82a316c947daf743df9c5913e147834e004fac701f7ca4e44564bbe823390edc` |
| `work/openmath-supervisor/checkins/20261114T200919Z/classes_all.jsonl` | 1640146 | `47aa181e2d43ad861e09513a4fe14d700702997fac30cce3d2adc92435409d96` |
| `work/openmath-supervisor/checkins/20261114T200919Z/census-crosscheck.json` | 173 | `d02d98585b61bd8f11629e5546ccbbf130f3d8432acb7fa8e18b4b517475d701` |
| `work/openmath-supervisor/checkins/20261114T200919Z/census-verifier.js` | 1457 | `c4fbde4ef0e3f08616c088b9d3fab2ac8e78cad5d903c8d5fed9781184d1e007` |
| `work/openmath-supervisor/checkins/20261114T200919Z/phase-theorem.txt` | 12091 | `75aeedd978c516c628bfb9f5da04ce49e47e7c166115ebb0a887bbd6d4bbd005` |
| `work/openmath-supervisor/checkins/20261114T200919Z/core.py` | 9137 | `72a9b6f69ae9fa34e0abdb599ed9e1790a9bb888a86b6e08f09ae6d4d366f76b` |
| `work/openmath-supervisor/checkins/20261114T200919Z/enumerate_classes.py` | 3706 | `12e1f4b6a26914533ec306981d48422b52999dc6dd2cc0a38aa4ace8eced9378` |
| `work/automation-supervisor/replies/20261114T204019.json` | 3048 | `90b804299a234875240e955e2352690b64dc6a4f4d612fefe35e2c70beb4fcbe` |
| `work/automation-supervisor/replies/20261114T205744.json` | 4530 | `d8a7e058f68a28d8dd23748a960d14d136a3b58ace8613a25d6817f89d2e3f6e` |
| `work/automation-supervisor/replies/20261114T211858.json` | 3543 | `38dfd3f6e676e5716970b38465048bb4aae5e1529226662c9503b8f670309036` |
| `work/automation-supervisor/replies/20261114T212205.json` | 1956 | `a54251624e33462f6877711ba8532aa1f1b14a31d843506b189ea6f845432d4c` |
| `work/automation-supervisor/replies/20261114T213711.json` | 4774 | `a4e92721f26a9125294f95ec1867c3b3ad3be41f2a481b1abd105a84f989faa4` |
| `work/automation-supervisor/replies/20261114T215215.json` | 3238 | `1c12138b378a5afe440a1e84628cc044eef65226cc910c117b20873341540728` |
| `work/automation-supervisor/replies/20261114T220720.json` | 3049 | `a7ede616df103628007a003907cbb58e417d80898a67488d695b5d0b9da43bd9` |
| `work/automation-supervisor/replies/20261114T222227.json` | 3063 | `0d1dcc720cb5a49197e7eac2cd09b2008c73d619d3382b4c0710ded83d668039` |
| `work/automation-supervisor/replies/20261114T222600.json` | 2542 | `77d8de85057a6d4fb546da585d8ade2c78710d56a561add6002c297f8b4c41a2` |
| `work/automation-supervisor/replies/20261114T224105.json` | 3043 | `2961164d6f47088280743f65af89c314244cebb7cffd427ebeee2c14b1c7f41a` |
| `work/automation-supervisor/replies/20261114T231544.json` | 3422 | `ddff8ae9f004658196707b6e664db29cdf317efbfc0a50e2edd4eabab2f94119` |
| `work/automation-supervisor/replies/20261114T232057.json` | 2199 | `238811eba4b5022a58422191de2de97d758f3cd7143b6e7d46f2b31ab0a91940` |
| `work/automation-supervisor/replies/20261114T232732.json` | 3095 | `12d89f3952e85c526b7d20442eb284059bf637c2e21e50c915a150dcd879484f` |
| `work/automation-supervisor/replies/20261115T001250.json` | 3887 | `de2ae43d01c0af00985c42a77faabbf3f85bf3ab3b461759cac24fb0f510ea53` |
| `work/automation-supervisor/replies/20261115T001551.json` | 4227 | `43534fdb10bbb9e1086dba16298839aa9ab097a3be3e0cf85344033cf48fdee7` |
| `work/automation-supervisor/replies/20261115T002122.json` | 3871 | `d3add921516ef36bb467c50447e99339f7432904ce0994a3e9d79cb71f883b76` |
| `work/automation-supervisor/replies/20261115T005413.json` | 3303 | `a29f684e3e0e6c68328d15fd182a9ac46052ed3e6597228da44686e740fa511d` |
| `work/automation-supervisor/replies/20261115T010921.json` | 3579 | `52bb62e86a146f7035cc6b6a11544b683765384540a018ab60f9cfde5b9fb1d5` |
| `work/automation-supervisor/replies/20261115T012427.json` | 2621 | `6146088cd60058d62d5f7ade9e1199c178b4b229d1bd4e3c6e25ab8280e9467f` |
| `work/automation-supervisor/replies/20261115T014638.json` | 2536 | `b6f73b2d2d4d8626119f0ca92829f4926f33268c1534be96970a63a4201ca51a` |
| `work/automation-supervisor/replies/20261115T021643.json` | 3149 | `45a527743b0025032633efeb0bb7cd406aad3640babce6d692c5cb4a446dbb0e` |
| `work/automation-supervisor/replies/20261115T024133.json` | 3454 | `bb174bcb83faaff428201fefd877b3032c4f1674440f6d1f2f70f715a726b598` |
| `work/automation-supervisor/replies/20261115T025639.json` | 4208 | `813afa68526ba1c06666cac03ff2f2ece5eacf04939710425e0c9791ac7ebd44` |
| `work/automation-supervisor/replies/20261115T031143.json` | 3618 | `a48e073f270b6f30c19c023d70cab95529efb57e8eef59117b244c2439175377` |
| `work/automation-supervisor/replies/20261115T032647.json` | 4159 | `c6b695dc42397184e77a3f083f17d3778af9747d9c32d189e91874ccacb04113` |
| `work/automation-supervisor/replies/20261115T034153.json` | 3004 | `813f9a1844c95d6776a10fc74034ded3af23ff0d6b4f52227dab768cd63b7485` |
| `work/automation-supervisor/replies/20261115T035658.json` | 2811 | `4a65efafb1ccf686a228ca1c2c551dffd71067778c9fc0fcd73be563cd7a96da` |
| `work/automation-supervisor/replies/20261115T041204.json` | 3697 | `3363c295cba59ffced5a27559fc5bb6183c38ecf3ad2bda5d48a90385096787f` |
| `work/automation-supervisor/replies/20261115T042709.json` | 2230 | `9ddbf46aed9ebe26863bc22370518433d1d5044bc210e75fba520630f26619c9` |
| `work/automation-supervisor/replies/20261115T044215.json` | 3763 | `b20683bf9d6312cf416b242245da2c00357616df029c5635dcd3f1a655492820` |
| `work/automation-supervisor/replies/20261115T045717.json` | 3039 | `e4287b444310018b5489166214bc2dfe0789b9cff810a153742c50c582cc5d93` |
| `work/automation-supervisor/replies/20261115T051222.json` | 2310 | `0a56680724587f16c03295e1286d5de95b692a74efe51dd8a66e8c7d721ca0e6` |
| `work/automation-supervisor/replies/20261115T052726.json` | 3789 | `b0711c2e2d0f875e1a70558a12e9bc96d408eebcce8d1f9d499e3346d021a69e` |
| `work/automation-supervisor/replies/20261115T054231.json` | 2925 | `1291827247eae690d7b3e1cfc7052682255a84bad84957e292c01121510ead46` |
| `work/automation-supervisor/replies/20261115T055734.json` | 3213 | `bc91ca308d57b05f6c4a54dcd3ce02716fc386d501786b0fb951f413b10a818b` |
| `work/automation-supervisor/replies/20261115T061238.json` | 2417 | `022fc311372492e75253a4bcb85708c07b5db8b3cb52b37cfbfbb9ab285dc57f` |
| `work/automation-supervisor/replies/20261115T062744.json` | 3841 | `d9955b9829fb94042e33780b6b32285d8fd99aafbabcd8b6066db489f903fe61` |
| `work/automation-supervisor/research-plan.json` | 1287 | `01f297f0eae4e0c1b400247bdd9b64fed3ca5a13d1d654b01d723665b8400b95` |
| `work/simplification-desk/s1/logs/01-States.log` | 1250 | `dd82f0b2a9712e7059fb82e748346594d2c6b441782f07389899abcd7a45eba3` |
| `work/simplification-desk/s1/logs/02-BoundaryTrace.log` | 1257 | `0d94aaaf275e19626c107e8b0fcacc0668f3f36cd3897eb5e7da933e8095b029` |
| `work/simplification-desk/s1/logs/03-AngularBoundary.log` | 1259 | `53844dfe64b3bd7b29d3ea921ec358982420d7c1303955aa8cbccc7371712382` |
| `work/simplification-desk/s1/logs/04-Exclusion.log` | 1253 | `08bf68e58f381f2049d57ed7c6c6a93195deeded7b908f76f4edb67c4f683dd2` |
| `work/simplification-desk/s1/logs/05-AvoidingTrace.log` | 1509 | `895472595e785005df7a380cf6f2f377883aea250073d1cc18abfad83e597857` |
| `work/simplification-desk/s1/logs/06-FourContinuity.log` | 1258 | `a573d901e27306c89b027118c9b345f90f134026f0c120935bb2dc3f0188dc49` |
| `work/simplification-desk/s1/logs/07-FourTransport.log` | 1257 | `8d49dce72eb5436b479ed6022d646132c0525891a69c9922c3974f9edcb1b973` |
| `work/simplification-desk/s1/logs/08-Accumulation.log` | 1257 | `08af7b758b670cf94c4294af52febec0107bd71fe4bcd983b3ea4c4bd7d7cf3a` |
| `work/simplification-desk/s1/logs/09-FiveSupport.log` | 1255 | `319b31eb5f8cf98b3288edd1815fc264aebfb4ccc3ae5501ade17676503ab47c` |
| `work/simplification-desk/s1/logs/10-CyclicCore.log` | 1254 | `942e4c93f3b7bd12902c2b6221a4ce6a32a166f61d05b0f1e9c10e51d11f2e05` |
| `work/simplification-desk/s1/logs/11-DiskAverages.log` | 1256 | `602a072ec85a65576f5a52a54937a1dc8e941433a12198b83b011e2c9a9248cf` |
| `work/simplification-desk/s1/logs/12-PlanarCovers.log` | 1256 | `5884b0d5f990b2da69fc64ea6341ae09a0cee172a68c623aed80111ff2f4ad54` |
| `work/simplification-desk/s1/logs/13-GraphRealization.log` | 1260 | `9b1ba1d9507a11198114256e8c5e57e872e7075f438c2ac73bdd6083a2339705` |
| `work/simplification-desk/s1/logs/14-Interfaces.log` | 1254 | `afebc1fe57c7ef37e2086a7697759c309ac10a28fbf7e253d5e033e7721b0849` |
| `work/simplification-desk/s1/logs/15-Sectors.log` | 1251 | `f28a11f4285919bc9f9dd42a16265f8826c3df3c6e795067f137a08c30781e97` |
| `work/simplification-desk/s1/logs/16-ContinuumLimits.log` | 1259 | `8f426d8486f3176821468f78cdad5c7ee4673b6592fdf0a781dee62eb0b99859` |
| `work/simplification-desk/s1/logs/17-DiskExtension.log` | 1257 | `9eed6a8c46a3db467cb2d2602ea2996299b29aade2e11274a7fa18c43dfc5038` |
| `work/simplification-desk/s1/logs/18-GraphCuts.log` | 1253 | `2c27ac781182f78c8740a6a1fe4ec56d72511e535df7743150668f5498b4d56a` |
| `work/simplification-desk/s1/logs/19-HoleApproximation.log` | 1261 | `0f328da0543eeba38e4b3f3eea02d8777f93882d4457573c0ed233b2deb98fe9` |
| `work/simplification-desk/s1/logs/20-GraphPatches.log` | 1256 | `ef11d689c6e33e65b7841ebe6bc712058672dc1c9a22e71f36cc1b46ef708c73` |
| `work/simplification-desk/s1/logs/21-FullApproximation.log` | 1261 | `4a3acafdb00ac3688cecf6a91442b49f0f685949c60c62b41df67658ad7ec038` |
| `work/simplification-desk/s1/logs/22-Mesh.log` | 1248 | `0e8a51377f1ed3c6d52a95142e8aa5e8b786c91d084b7c984147ebbfc9d3ed98` |
| `work/simplification-desk/s1/logs/23-Five.log` | 1248 | `56bdb08ad010dc1e4168c6317b0b4b26ce2bc90868da6d6301c5b8669486c9ab` |
| `work/simplification-desk/s1/logs/24-Chromatic.log` | 1833 | `8483a2fb429796c9641e05cc346971cf865dc28ba6d3c8dcb47d2e718078ba58` |
| `work/simplification-desk/s1/logs/25-Converse.log` | 1252 | `0b22a1ad5f137636cc1eb56c73123bcab9111d38410e35c7302f3d0b07d1dbda` |
| `work/simplification-desk/s1/logs/26-NullSetRobust.log` | 1257 | `5af64331611e64aef194f6b50faa3961cf814dd561e0f8ab2ba6fd895715db1e` |
| `work/simplification-desk/s1/logs/27-Transfer.log` | 1252 | `4909e50f091fccfa75eb533375c90d254c7a04e8d685e41b5f949ba64ba9e8f7` |
| `work/simplification-desk/s1/logs/axiomroots.STALE-RUN-0201Z-failed.log` | 2506 | `522675612c257677c2d5a35ba1c7e231cbe4406ee4b17f2e567e3c3911707729` |
| `work/simplification-desk/s1/logs/deadaudit14-s1.STALE-RUN-0201Z-failed.log` | 2513 | `87cb0d40aa98eec6741777809529e6c36fb03ba3974ecc7e2fd099b081286e12` |
| `work/simplification-desk/s1/logs/sigdump-s1.STALE-RUN-0201Z-failed.log` | 2505 | `6eed4e4eafb7e29bf66a11bbc66eaec54594e9e090b339b719e8a72b5f055f0c` |
| `work/simplification-desk/s1/logs-r2/01-States.log` | 1253 | `513b026b8e4c3a651018712d271e190b65b1f23bdcef8cad3287c9caf2860045` |
| `work/simplification-desk/s1/logs-r2/02-BoundaryTrace.log` | 1260 | `10577969d1ea6ac2846691402fca213852149349c327535edff1a21755ed2b95` |
| `work/simplification-desk/s1/logs-r2/03-AngularBoundary.log` | 1262 | `85dcf22d756c71275aba27e3e01d254c845a2de63f63d44a9f6ba5b4a831b133` |
| `work/simplification-desk/s1/logs-r2/04-Exclusion.log` | 1256 | `6fa122d352661681b7286a1b18a8860ea3c35ba226e3450428d9cdce4b3c0055` |
| `work/simplification-desk/s1/logs-r2/05-AvoidingTrace.log` | 1512 | `68df0f4395cfd963d23ec48cbeb405d4d5b79b008818334ef3ee5214c7c32f62` |
| `work/simplification-desk/s1/logs-r2/06-FourContinuity.log` | 1261 | `42b6dc00b968397f33ff252b10518af196dd21a11d3d53bcafc100a6330d52c3` |
| `work/simplification-desk/s1/logs-r2/07-FourTransport.log` | 1260 | `2a89e42f9ffb490dfdfe02b921f573428375a18dda6bebaddc42537b172410d4` |
| `work/simplification-desk/s1/logs-r2/08-Accumulation.log` | 1259 | `2486b4aca7fae63081b397d26448dcc90206015b90c3a9eb124ea586914edcfd` |
| `work/simplification-desk/s1/logs-r2/09-FiveSupport.log` | 1258 | `358d7e5ec3bc1393280f4331bf4dbd1677c9024215926883db629d24df0f5442` |
| `work/simplification-desk/s1/logs-r2/10-CyclicCore.log` | 1257 | `975b2f87078bbcf0282ec16ce6a759a97b3132f55f38bd57a9d7da14ee6c338e` |
| `work/simplification-desk/s1/logs-r2/11-DiskAverages.log` | 1259 | `24caf2c11f650fed9c20a353bf67c6095349d8930d880871ad18481d6944ac61` |
| `work/simplification-desk/s1/logs-r2/12-PlanarCovers.log` | 1259 | `9769475d3dedb3e1cf4e70f7381c28fd84483c995388ed670efeeae64f630add` |
| `work/simplification-desk/s1/logs-r2/13-GraphRealization.log` | 1263 | `9bf1e53fe0fc58c98d85da36225e85517c629bd664d844ee76f6889b7e578e8d` |
| `work/simplification-desk/s1/logs-r2/14-Interfaces.log` | 1257 | `062987665775c324b6eb290559522f906552fce38e3625edcc03e11a8d4cd731` |
| `work/simplification-desk/s1/logs-r2/15-Sectors.log` | 1254 | `c0a62833509b9d1237b70a72d5ab21b1c28673336e5186d800ffb8023ae0a79c` |
| `work/simplification-desk/s1/logs-r2/16-ContinuumLimits.log` | 1262 | `8e8caf5aaeadf050b1fc78fa3a4a6f1a000c1cff29a5a1e368b0d5801c70552e` |
| `work/simplification-desk/s1/logs-r2/17-DiskExtension.log` | 1260 | `a7f31254ef2f3122e3ffb22ff962a0c426722d5dbbcbf0bee424d62779364e91` |
| `work/simplification-desk/s1/logs-r2/18-GraphCuts.log` | 1257 | `4ac39cf249625d1cb593b824477b02bd587a941be3629782e5543dca9e74c513` |
| `work/simplification-desk/s1/logs-r2/19-HoleApproximation.log` | 1265 | `f8ae27beee055dc4869d6b7b68f4f200b199a318188fafffdbb21217585248b6` |
| `work/simplification-desk/s1/logs-r2/20-GraphPatches.log` | 1259 | `3e4bd735c2c9eea6271a218d33151eae522904dfe7b57f0488d06a15e949beb9` |
| `work/simplification-desk/s1/logs-r2/21-FullApproximation.log` | 1265 | `5b2ca42d9ce915557aeb1853869cab59885dabf9b0c1df1a4ff178781fb2a7ad` |
| `work/simplification-desk/s1/logs-r2/22-Mesh.log` | 1251 | `5606c90483db7d2479f446acc62371050c798be3e0d71769aaee5ccf9cda95a8` |
| `work/simplification-desk/s1/logs-r2/23-Five.log` | 1251 | `d4a750d93cecfa421c3b882f9f2984dcb1be28f27d717f7d7ccc132616cceb8a` |
| `work/simplification-desk/s1/logs-r2/24-Chromatic.log` | 1836 | `9fd1054a8a879244c5d54845cfec6c4d47cb6e84cf769afd035bf0570fe9a132` |
| `work/simplification-desk/s1/logs-r2/25-Converse.log` | 1256 | `fd918622123cc60fc8861fe3cad6313ee59c76d9475c4d6c975a856c5d3f3dc3` |
| `work/simplification-desk/s1/logs-r2/26-NullSetRobust.log` | 1260 | `4e83255b60d98343a8269007a39b7f53f70315cbb14a561cc64d63d423707796` |
| `work/simplification-desk/s1/logs-r2/27-Transfer.log` | 1255 | `bce6876fa9716f5b05dd6b978af04e7918f8cc6c4ac4aa1dec9678cab7f12ccd` |
| `work/simplification-desk/s1/logs-r2/axiomroots-s1-r2.log` | 5360 | `02c2e87433f6b37d0b1e0a47c0f05f49e8c4304d19b15b1e83ce479d12bdb110` |
| `work/simplification-desk/s1/logs-r2/sigdump-s1-r2.log` | 3099 | `5fc63e23754384e43258372768b550f73a3963567d22f785e42216a88b3d0643` |
| `work/simplification-desk/s1/MANIFEST.md` | 4714 | `c076468610b1f1cf419d5cd2ef97b91c0e1781d339b9a888157eddff41496f3e` |
| `work/simplification-desk/s1/sigs-s1-r2.tsv` | 426665 | `8a93cff3eedb4fa3ebd67b8294d3b8bd567b07cbec91e19ee0a0baf396a819d7` |
| `work/simplification-desk/s2/MANIFEST.md` | 8422 | `c6316d7dd9e609524a3464ac3aecea072f6db8affa313046e68801025e45bf90` |
| `work/simplification-desk/s2/AxiomRoots.lean` | 3814 | `4dda63592232d24a6da91e045980d93e2761c14488fcd427c82c3baa7d3842f5` |
| `work/simplification-desk/s2/changed-modules.txt` | 1688 | `b536c876c4733000820586c4b2b9c911cf6370656d82b40d38b328b254c15cc0` |
| `work/simplification-desk/s2/dead-deletions.json` | 6722 | `9c25a6e0604a51a18306a4c63d42cb81411fbee72e401a31ceca37d777490230` |
| `work/simplification-desk/s2/line-accounting-s2-vs-r1.json` | 18494 | `e9755b05fdd423ef3f3649ee6ba24f99bf18cfb4eea68f5bac23fbf0699b0579` |
| `work/simplification-desk/s2/line-accounting-s2-vs-s1.json` | 12246 | `49f95959fef349ec3391c7816ba4b77a124b31134bbdd6efd719bd375692a36a` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/CircleOperator.lean` | 17281 | `1a1523f435af9f6efbb10806ef4dc5ccd76f69b226642b997ad0c98398287de1` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` | 26846 | `fcb77a76a2023bce5438bd5736984c50f07ba5f6e82cd1b765a8aa550eef693f` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/Energy.lean` | 21763 | `10895c85c9d1ca9be76885fec41c4a1c63dc009ce0e6b2d4e8af47b16dc1adca` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/FourierTests.lean` | 12526 | `73910dcd4dfda8fcf3491dccabe81d99322abe3452d5939859315a1895c29216` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/InvariantMean.lean` | 45768 | `db71947b617c30ef32bff4cb2761ba9979d91339c216713213cb5e3a3952d769` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/Multipliers.lean` | 13716 | `9437aff41e64bac8f6b4d476f1471e82bd42368f1fc839823474504f1b6949c3` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/PhaseCollision.lean` | 21625 | `01d0a2f337e6f80cce42f67566df0109bbaddf2dc44df131aafe9b3648557f98` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/Representations.lean` | 25402 | `a2880f4e65bdbf701589b4ea50e35fae7e1fec623cf0c32a1060c6636578d799` |
| `work/simplification-desk/s2/OAI/Analysis/PlaneSpectrum/SpectralMeasure.lean` | 20499 | `376c8087607945e0074d19c28516a73e05e91a272593c45019b623d9739af96b` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/AngularBoundary.lean` | 25509 | `796414de07e4fb2ce5ae862530bc85742e6ba318ce6c12307644265d08e6c663` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/BinaryPalettes.lean` | 20217 | `5e2ffdb80a1afd9101bf21b9e5a81a1874fb5dcc91ca485ae0679ac75eca25b3` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/BorelTransfer.lean` | 25485 | `4e90138bb6baea8806982342fb74ec4aa702c4edb35645a11a732fe67887c441` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/BoundaryTrace.lean` | 18356 | `6bb884aa073edd320672ede4145b8488af533c82550606603ea3da49683ab017` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Compactness.lean` | 20667 | `51897e8f294ca13bc33798bf36c3ee3f9bccd1b40e9ae628dc1184bf5d598930` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/ContinuumLimits.lean` | 17828 | `cfa79b5f6d8e9449b0ef6beb8a8d40265cec5a9d939dfb14979389fed5081ca0` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/CyclicCore.lean` | 13402 | `d55a1601a3d9d3679cc2ae6d16302f1eac71d71ace20a21c276c81e2e3d164ab` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/DiskExtension.lean` | 29141 | `ef64358d8261d6a96c8b03469bee12f2ab0abd4647a9f1230b41059fc914ac64` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Exclusion.lean` | 8799 | `1613d1543f72813e05301a0e141e684bb4289e65a8d4905cc4f47b32057c8b67` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Expansion.lean` | 37338 | `b3684b996cc4bbf40eaf5697b8fa747b053f4c098f585f17e2e4298a21e4e348` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/FiveSupport.lean` | 19132 | `b12dad93faddcbaf07dcb6e92a86c36ffb1e3a80f62192e64916ae936599eb65` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/FourContinuity.lean` | 29242 | `46efa82aa091fd03ebe10a4d61142f96ad4f8a8533d7c84fa2d8117d5e18c6c9` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/GraphCuts.lean` | 15270 | `9aa4f41d6e5ffc105ef0d1e416491e0c7dce2fd59735179545730098a4f06830` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/GraphRealization.lean` | 20835 | `def12054e6260a4b85dfd13d19a06dc6355f39fb8cbeadbfe1ef1fa45f2e2d7a` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/HoleApproximation.lean` | 16915 | `cbee4d2ae2fcf691333a7d21b274ddbb549cc30d39d00918f873e75b2c50176e` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Interfaces.lean` | 30004 | `c3348acdd555cc4196de9c9f14f1f32cb37f2f59dbfd54fccf591a3303b88e02` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Lattice.lean` | 2113 | `688cc2b73931dbdd4a05148d5c8e53d155ce976d587d40308c627a53a2db669f` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Moser.lean` | 20769 | `b2da0e254b41919a3858d23acf72bc643339871d1a4f0951d5ceb32f1a3fedcf` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/PaletteDensity.lean` | 25009 | `24d1525a3efafe117962d32aff754f30949371234d7d14f3099361e1c0b0d68c` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Palettes.lean` | 6689 | `74585bde311823dbb9b9fbabce6ec89415134a8b298f7da66c31207e37e2646b` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/Sectors.lean` | 23972 | `8acd47b52ea091d61506b8cbf529be6f59626812e90dddec6c7c1de7430e9e62` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/States.lean` | 25612 | `7b411cc583485431fa957070a8d4c678ed35ba8cc7cec8b465925a0e03744520` |
| `work/simplification-desk/s2/OAI/Geometry/PlaneColoring/WeakColoring.lean` | 9687 | `7994f86994c903d2fb76cb60dcbe02cbb3f53047d282d42170122b578bf3c90b` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/Amenability.lean` | 17452 | `08d0ae62ede2e89c3328801e0cbd5fbbde35c1cb8d4af3ae39e4f6406b9f8c19` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/BoundedFunctions.lean` | 9681 | `f1750185aa305ce18f0937b6949d898d686e2dcdc297606f7c14aef5607bc58e` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/Centers.lean` | 30205 | `51a370e921f6fcb8825d502538d5871d53bcb4f546f0d95580351bb63275019c` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean` | 23314 | `675f780669891ce6ff5bc604670da0be6c1f12391ee6eac052598a444807396a` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/Factors.lean` | 27873 | `548ec497e431bf2cff7165b4b0ce39f6d8a5b7542dcfe476ac67a30d4ea6c291` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/Functions.lean` | 45777 | `c3ffaf6e817bf4fdcc8f51d9355c7b6a56d2a6a2e22c835b6d463845cf60e902` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/RelativeCenters.lean` | 27057 | `40010491b6e6f343d1b4191471f930fb5b18817a29a072c4180fbbfa8e03eb13` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/RelativeProducts.lean` | 20960 | `f5abd2b8e32dae69da826d234f3310c41813989deb1438c0354795935c4c8d76` |
| `work/simplification-desk/s2/OAI/MeasureTheory/CompactFactors/Separability.lean` | 25596 | `bd2e5ea3afc7843aa5d2d269882c92db1cc8cb3779fd5d2108a1f8e936c01c1c` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/01-WeakColoring.log` | 1256 | `cbb5e121311f6d0bfe583155c508c39f9d7fda2d4420707201528e950c3b9d6c` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/02-Compactness.log` | 1256 | `a8b9473ff9f723089b6f353cafe1fb27b1c0a7865e4ab948d7e08cb87b6465e0` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/03-CircleOperator.log` | 1258 | `ea9bc571a140f296f6477b44e2f7d4e6780381354382a293ae97553a544d4fb2` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/04-InvariantMean.log` | 1257 | `54a089cb364babff10e1ac37171d16c37f221f96be5764ff09d4f183c26da1e0` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/05-Multipliers.log` | 1256 | `cae525cfefc2790404862faacddd444e43c34d4fece9bc2ee1bd14c934303b59` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/06-FourierTests.log` | 1256 | `89f100301f8d586b9660b9c916ba5cdbb96d82b5bf60b87a545ba53956085602` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/07-PhaseCollision.log` | 1259 | `a9c7f0095a0d6dd99d77b376717d47ff6608d93faf39ab1e518f4264400c5d1b` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/08-ConditionalSelection.log` | 1270 | `1457e209ee04171bd9dae9d20545a80dc17e20a946a723794496897c7085fd8e` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/09-ConditionalSpectrum.log` | 1263 | `ae7fda7b08781e9902f8945cb3f0e5d2604f9ea2d13dd91962333ce803b245af` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/10-Amenability.log` | 1261 | `cfea264f8fc2bef6123ad201020890859bdc37fef534734616016aa965278123` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/11-Centers.log` | 1257 | `5ef3fb4f478e1aa9d6db008440d674610a66bd18ee312e47e665fb9d9f201dfa` |
| `work/simplification-desk/s2/logs-attempt1-failed-omit-prefix/12-RelativeCenters.log` | 19385 | `80e4ee9936f66237cbdc69ca7b9ffbc2bb2485b6b14861335b8506aa68d34d13` |
| `work/simplification-desk/s2/logs/01-WeakColoring.log` | 1257 | `dd083ec889c1078d61f778c363d937fec8f44c8dc418f9ed0f93325cfe96b348` |
| `work/simplification-desk/s2/logs/02-Compactness.log` | 1256 | `aacb3ab6d6c62a8c613ef519d3dbe7396c49bd58af0bb4659f4a2dacfcc38a4e` |
| `work/simplification-desk/s2/logs/03-CircleOperator.log` | 1259 | `b175676ef191d9f78d8ef96f23094df8bee7b692a3c3c5a127ff202a71164c55` |
| `work/simplification-desk/s2/logs/04-InvariantMean.log` | 1258 | `947cc7b55c4a7299b53063e2f9bf6abdc5489318d2b80613f2d2646f6e0ccfa5` |
| `work/simplification-desk/s2/logs/05-Multipliers.log` | 1256 | `42150487731b369eac05c87bdbeb7dd41bc22037de080f00b9f64e1f7925ccd9` |
| `work/simplification-desk/s2/logs/06-FourierTests.log` | 1256 | `a6fc883dae337ced66b2499fa238121acb9003a36c7f3d608499f19a2f5afd57` |
| `work/simplification-desk/s2/logs/07-PhaseCollision.log` | 1258 | `84f2eef28dd5ff69038be11641f7354514869222df089eea8704b1fcae67205b` |
| `work/simplification-desk/s2/logs/08-ConditionalSelection.log` | 1271 | `8a7fbd8d2701bc22bf841f5e75680c20ed36ef48f263dd4486ba7f2298e49f13` |
| `work/simplification-desk/s2/logs/09-ConditionalSpectrum.log` | 1264 | `ffc62acf0f57da33d1effae57ada49438be8decbc04c0e1fb1cd68c97d60fd59` |
| `work/simplification-desk/s2/logs/10-Amenability.log` | 1262 | `d8de0fbf2d1b96bc75dc60b2c0662a7fb96853f01b7b659993d6ebc1ecd1a72e` |
| `work/simplification-desk/s2/logs/11-Centers.log` | 1258 | `b715be65e94f150ec161c8dc53a25c4e9720cf1d4fb1b4f7fa02bb132e66e6a1` |
| `work/simplification-desk/s2/logs/12-RelativeCenters.log` | 1266 | `972ba52d275e6810000d01427863b88b65f62e72f64ba6928253f102d60b6268` |
| `work/simplification-desk/s2/logs/13-Approximation.log` | 1263 | `c810693d79a9a07726071dbdd734718ed28d318f87232f72abc8397a0c1aab05` |
| `work/simplification-desk/s2/logs/14-ConditionalLimits.log` | 1268 | `a3864a6a5a75b853d3e0f2970ae92dbb52da9212e7ab96bb68b1d043b2792d0e` |
| `work/simplification-desk/s2/logs/15-Kernels.log` | 1258 | `c2134d114af262ffd76f7875597eda122405a687dc4e90132172b3693cd45b52` |
| `work/simplification-desk/s2/logs/16-BoundedFunctions.log` | 1267 | `5d257c6549d8bee71c9be224bedeb8b15db32771c3d7fc5e1ecc52b579a607f5` |
| `work/simplification-desk/s2/logs/17-RelativeProducts.log` | 1266 | `dcb626077a3131c87637661e96e8a6bf11dafe8c01e152854d547cb0d1914226` |
| `work/simplification-desk/s2/logs/18-Separability.log` | 1263 | `4c748c020478c257d61b0d4265c43ebc9a96f5454b87692a22747a040c3726e4` |
| `work/simplification-desk/s2/logs/19-AlgebraModels.log` | 1263 | `7a9b9d932c2df88ae9eb506e2e2ba0c7a7b58d317ef04a94c4f0a516d5c56e4b` |
| `work/simplification-desk/s2/logs/20-Functions.log` | 1259 | `6a5d695ba9233962d113faa5718599a15135e10fccbb0776e77730c883a0073c` |
| `work/simplification-desk/s2/logs/21-Factors.log` | 1257 | `918c9691d6d56d2f9a74210813e570b04a4171936cde2a008e1cd203aa98a228` |
| `work/simplification-desk/s2/logs/22-Stationary.log` | 1260 | `a45a07ee7d046dd676016c3999ff5530a8d5492c52a4a6557fb0e62afde4b1e3` |
| `work/simplification-desk/s2/logs/23-Representations.log` | 1260 | `28dec03921eff749b3653ebbc65e13ea71a094ab3ce28e4139030c99ea16a8b1` |
| `work/simplification-desk/s2/logs/24-Energy.log` | 1250 | `22489eae3d3b532f2b1aceabac9e13ae7d38fecaba4dc1fc9ca6947a419f4dc1` |
| `work/simplification-desk/s2/logs/25-RadialEnergy.log` | 1256 | `b0ae444069a5cec9ff521d6f4b9f6dc1774597f96b6c2dbbad8cc99b3bca0aff` |
| `work/simplification-desk/s2/logs/26-SpectralMeasure.log` | 1259 | `fcceeb28c90c287136901c6d5752bdd607261a24f04e8bcaa7224e5df7bc5a8f` |
| `work/simplification-desk/s2/logs/27-Ergodicity.log` | 1254 | `55581bf2e17139d7633071c0bd028590e33c879ee6cc2a083b6268b3952343e9` |
| `work/simplification-desk/s2/logs/28-Expansion.log` | 1253 | `e0f46e6ef0e7067a48d13c8b426cab8e50e1f7f760981fa74abeccde0bf39ff5` |
| `work/simplification-desk/s2/logs/29-BinaryDynamics.log` | 1258 | `ff1c5e9e5d7648f0ba0a6534dd8f442e2fbba437f0c95d531dd5bbf1c5983772` |
| `work/simplification-desk/s2/logs/30-CircleTransport.log` | 1259 | `1ec150beb1eddb01cbc7f793a80d6b6e58bab129f42d63d2d206d28f6a3d5808` |
| `work/simplification-desk/s2/logs/31-Transitions.log` | 1255 | `95db59e5b3662290bd94293a0a7932f32db996bc1a593e55b89a527203b5230e` |
| `work/simplification-desk/s2/logs/32-Palettes.log` | 1252 | `0fe0c0b1ae9b66b4e0d3ff409c69d80570701c5035f96c0bb564aaf6057a9d61` |
| `work/simplification-desk/s2/logs/33-PaletteDensity.log` | 1258 | `53097cef1c216509cd48b5655938e21a7d7e36150b3c237b657ec9f664853146` |
| `work/simplification-desk/s2/logs/34-PaletteTransport.log` | 1260 | `fd7dfa2d33459037136026a0597e261803df37fb77993f87b11a5a0322030d70` |
| `work/simplification-desk/s2/logs/35-Rigidity.log` | 1252 | `4227fefcca89f9c01fa71e5ae01cea18c5aa591e838b180cdf15d2b75976ff3d` |
| `work/simplification-desk/s2/logs/36-BinaryPalettes.log` | 1258 | `7b5fd0efcc6674139e81ce212dd32714753a6a138214b227b3c7a67ea678dbf6` |
| `work/simplification-desk/s2/logs/37-States.log` | 1250 | `c21bf2248f204199325f6be574ad9e0201ef3071f17d4784a9f707555aba9dd7` |
| `work/simplification-desk/s2/logs/38-BoundaryTrace.log` | 1257 | `40fdad2136f03096d6964d888524307e4559f888df18853de5b4e578f460561d` |
| `work/simplification-desk/s2/logs/39-AngularBoundary.log` | 1259 | `a71f88d63610cec51f3874248988ba16a1060628747a73681651227b1aae8c87` |
| `work/simplification-desk/s2/logs/40-Exclusion.log` | 1253 | `0885b3ef594d849a6b48663cc2450367323d444552da4e17ddb7aac73ba51f19` |
| `work/simplification-desk/s2/logs/41-AvoidingTrace.log` | 1509 | `cba163eedd53e0550dfc23d28f1097dd91e50031b3a14636310a4211d14d152a` |
| `work/simplification-desk/s2/logs/42-FourContinuity.log` | 1258 | `b65259f5eca9be959c7022e24475572f6d54f5a381cdc392d9b1cc11974f98d3` |
| `work/simplification-desk/s2/logs/43-FourTransport.log` | 1257 | `8489cd889241a0f8ef82f7575c30797b4d6cdf4c2854827b3a63f549f3c6c022` |
| `work/simplification-desk/s2/logs/44-Accumulation.log` | 1256 | `d362c123600dca1e66361bd3a1fd25d93d42e02e384d744f07078d73b28efe26` |
| `work/simplification-desk/s2/logs/45-BorelTransfer.log` | 1257 | `51cc4aeb7df3753b2e66db38ba0a2d5fa502962f70ba85aa72c46d9bc646f2dc` |
| `work/simplification-desk/s2/logs/46-FiveSupport.log` | 1255 | `74c56487e00d722177f28882515268d1de29ba74a4d0fbd9ded64a30bcf43b2f` |
| `work/simplification-desk/s2/logs/47-CyclicCore.log` | 1254 | `62b89a39d6eb9c80ff2e2b9d2299d40f1d6d3c4e996257255a38ad1d0d1e97d9` |
| `work/simplification-desk/s2/logs/48-DiskAverages.log` | 1256 | `95d10a81c769cfcefd5c7401b414f321a642b118e6257eabe3faed4a6a12609e` |
| `work/simplification-desk/s2/logs/49-PlanarCovers.log` | 1256 | `cdbbb51c5b6253960aedeff703f7636fb6dfe168772ae34830ef3bc31cef3871` |
| `work/simplification-desk/s2/logs/50-GraphRealization.log` | 1260 | `9ce397aa8f6a22f9d9ca6890872bba10a81fdc97a91343ac15c60e5c60ec896a` |
| `work/simplification-desk/s2/logs/51-Interfaces.log` | 1254 | `93818dedeb848d41d0666095cdec169472b4b6497ee32e6be1717c35155d7207` |
| `work/simplification-desk/s2/logs/52-Moser.log` | 1250 | `59fa5fa92c8c93e6ab4632e8d4a5b7218d819b05969366e36e418dd890d37e84` |
| `work/simplification-desk/s2/logs/53-Sectors.log` | 1251 | `61368d0c0c955e75c4c05a57fb86270f60a2c51cd592778449486ab50caf5f77` |
| `work/simplification-desk/s2/logs/54-ContinuumLimits.log` | 1259 | `4fe8cf7ec792bd08d6f47a130a91baae2c7f92c758ae809f730ad95b8f1fd9bd` |
| `work/simplification-desk/s2/logs/55-DiskExtension.log` | 1257 | `eae23f4f3dff7592680b46add4345fdf72359ee87c6664787f53c2583d35affd` |
| `work/simplification-desk/s2/logs/56-GraphCuts.log` | 1253 | `415cefd3058d916fe8a96c1d9224c6f7c0976c5653581cfb1c2b0168684786a7` |
| `work/simplification-desk/s2/logs/57-HoleApproximation.log` | 1261 | `389a389ed49f8ae9727f831d5b4ce982363ee3a9d031c4e58c269396c4a93ef0` |
| `work/simplification-desk/s2/logs/58-GraphPatches.log` | 1256 | `009822ed1b90aa637ed643637b6e22147a1f5f05343860a09c0e829325886b1f` |
| `work/simplification-desk/s2/logs/59-FullApproximation.log` | 1261 | `50240d8d267ecbe15cebd8a5140f4cbb63c6ac876982a73a90f78d504156be9c` |
| `work/simplification-desk/s2/logs/60-Mesh.log` | 1248 | `80b2a53522a94c15cf459fe56c5a4002da89fc57ab5ba16bc2a35179ec12690d` |
| `work/simplification-desk/s2/logs/61-Five.log` | 1248 | `b2db1273ac1a06c5a42831a920d4ccdf6fa651a446ee04c8200e744c57edca1a` |
| `work/simplification-desk/s2/logs/62-Lattice.log` | 1251 | `c88e330034eb064b1ff66095c3827ab4624f197ad77ca105a2c86849cec22a4a` |
| `work/simplification-desk/s2/logs/63-Seven.log` | 1249 | `6f5e331cd39055a6ac82cc38b8a9ed197ddbd67cc66be1e231e2743415946f8d` |
| `work/simplification-desk/s2/logs/64-Chromatic.log` | 1833 | `667af56c10147fcfb592426df8075f4a8db3d48bc6316ac8d9430ae14cffbb68` |
| `work/simplification-desk/s2/logs/65-Converse.log` | 1252 | `b4ba2f163539b1327a4bbb58fe3140204f7fe018dc47c3f20fcc6ee3e695e00b` |
| `work/simplification-desk/s2/logs/66-NullSetRobust.log` | 1257 | `598fb0353cf73a18ec33d06068f573a3af3cb034b872d223a85c6d065b10007f` |
| `work/simplification-desk/s2/logs/67-Transfer.log` | 1252 | `d02888c1aac9da083701106d3ea40dd3a1d68b249358e0940c2d7adcc9cb5bdc` |
| `work/simplification-desk/s2/logs/axiomroots-s2.log` | 5356 | `b01833ec872ccabb102ea9df70ae45a37e2019d2a3b27aeed51f9dbf1c490962` |
| `work/simplification-desk/s2/logs/sigdump-s2.log` | 6669 | `11ee8fc62f59bba5dcabd9c30d26a4b6709178751423ce2439f99d2c26fd28f2` |
| `work/simplification-desk/s2/sigs-s2.tsv` | 418092 | `44bdbeea5d12cf9f5590908e3741e009c3c57c2f3358ee5e605a853423b17102` |
| `work/simplification-desk/s2/AUXCHECK-NOTE.md` | 1660 | `233c5a30deeb671a2c5f844326bc5110f43a1b1b23d08bded73dba8e35393dca` |
| `work/simplification-desk/s2/AuxCheck.lean` | 1424 | `7c6a12adae47dbf7f72477c187180b5f1d4a739e7f91fa7a051d733eb7f1871d` |
| `work/simplification-desk/s2/auxcheck-s2.log` | 4966 | `8e05f1ca231fe9d286c4c6542796f8245402939d2a5d8eb8527a4027b6470bf5` |
| `work/simplification-desk/s2/auxcheck-r1.log` | 4950 | `3d5ac560d832dd4687e03be427ebbde7325864ea476f569f3e354743d10347c4` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/States.lean` | 25612 | `7b411cc583485431fa957070a8d4c678ed35ba8cc7cec8b465925a0e03744520` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/BoundaryTrace.lean` | 18356 | `6bb884aa073edd320672ede4145b8488af533c82550606603ea3da49683ab017` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/CyclicCore.lean` | 13402 | `d55a1601a3d9d3679cc2ae6d16302f1eac71d71ace20a21c276c81e2e3d164ab` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/FiveSupport.lean` | 19132 | `b12dad93faddcbaf07dcb6e92a86c36ffb1e3a80f62192e64916ae936599eb65` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/ContinuumLimits.lean` | 17828 | `cfa79b5f6d8e9449b0ef6beb8a8d40265cec5a9d939dfb14979389fed5081ca0` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/Interfaces.lean` | 30004 | `c3348acdd555cc4196de9c9f14f1f32cb37f2f59dbfd54fccf591a3303b88e02` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/DiskExtension.lean` | 29141 | `ef64358d8261d6a96c8b03469bee12f2ab0abd4647a9f1230b41059fc914ac64` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/AngularBoundary.lean` | 25509 | `796414de07e4fb2ce5ae862530bc85742e6ba318ce6c12307644265d08e6c663` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/FourContinuity.lean` | 29242 | `46efa82aa091fd03ebe10a4d61142f96ad4f8a8533d7c84fa2d8117d5e18c6c9` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/GraphRealization.lean` | 20835 | `def12054e6260a4b85dfd13d19a06dc6355f39fb8cbeadbfe1ef1fa45f2e2d7a` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/HoleApproximation.lean` | 16915 | `cbee4d2ae2fcf691333a7d21b274ddbb549cc30d39d00918f873e75b2c50176e` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/GraphCuts.lean` | 15270 | `9aa4f41d6e5ffc105ef0d1e416491e0c7dce2fd59735179545730098a4f06830` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/Exclusion.lean` | 8799 | `1613d1543f72813e05301a0e141e684bb4289e65a8d4905cc4f47b32057c8b67` |
| `work/simplification-desk/s1/OAI/Geometry/PlaneColoring/Sectors.lean` | 23972 | `8acd47b52ea091d61506b8cbf529be6f59626812e90dddec6c7c1de7430e9e62` |
| `work/automation-supervisor/inbox/20261115T021643-download-4-R1-1-BASELINE.md` | 8557 | `8501a0a088af9e7fcd122c21561dee55005f0c0adc8fcfaa472edeafb9770aee` |
| `work/automation-supervisor/inbox/20261115T021643-download-5-r11_baseline.py` | 14250 | `93847c7b6703154a4a57699d88096de135c8e038f303b1ae0a6905c3135a201b` |
| `work/automation-supervisor/inbox/20261115T034153-download-1-SIGNCEL-COUNT.md` | 6611 | `f6baa6b98c8382896ddf535e96ac7060f1c2bfac38b7f8b43e1199959cc90871` |
| `work/results-desk/L-R1/L-R1-QUEUE.md` | 2300 | `3ce1e9cb5dbbd5312697a9205763e64117a180a82c31f23d7158d9c5080cae9d` |
| `work/results-desk/L-R1/R1-1.txt` | 3964 | `8a68f825005a91644cb3363627eb25a41ee0c9d0441279a2222c43ce174a9ac9` |
| `work/results-desk/L-R1/R1-2.txt` | 3572 | `b3ae2032ed83e40c417222310b770e75a6bfb9ec0303b8ba650bd8226c829ede` |
| `work/results-desk/L-R1/R1-3.txt` | 4202 | `94b2f187c4151e6659a11543db6d1284d2a39a7d9d2eb36209a0829b97732822` |
| `work/results-desk/L-R1/R1-4.txt` | 3961 | `796478a36119a6cbddabb51a3ac2dc44a5c17ab172ac977ee813e28347828e60` |
| `work/results-desk/L-R1/R1-3-referee-lane.txt` | 4341 | `c30a87cb7080fd17ea112aa0df6079a4c7bc3f515df92b36f68d3ce91e0249b8` |
| `work/results-desk/L-R1/R1-4-referee-lane.txt` | 4100 | `c3fdb4aa3af347f7517c64a67bf63888fa330884b05cc02af54cb91ceab3a7c1` |
| `work/results-desk/L-R1/R1-1-followup-d.txt` | 1699 | `05cc55baf8a2086c1c5c829a057428e5936d0ddf6dcaf4c4dda71868ba9f0e6e` |
| `work/results-desk/L-R1/SENT.log` | 190 | `26cddb450d579b0f9bbcf1b02ce595d7bca537fafd6ee2cf9241bc1d1c37e563` |
| `work/results-desk/allphase/allphase_desk.py` | 4155 | `07c89fab37168a9e5df855f65319ae5c0ae311eea148be100de9aeacba9ea110` |
| `work/results-desk/allphase/allphase_desk.out` | 463 | `81f5c38f9adb36a5774810c442551463ade3ced4fd931564f4a75a62a1735d53` |
| `work/results-desk/allphase/mc_signcells.py` | 2426 | `1e8b0525aa995d6d4de9ce2ae9234e7456ff9a1b12c95bd9bb0503708d27523c` |
| `work/results-desk/allphase/mc_signcells.out` | 700 | `1be8f3f562a606b2fa6bfbf828224398fc8c558c30cd20bfe3d0ff4817dac1d5` |
| `work/results-desk/allphase/lift_labels.py` | 5367 | `94d8b5e888fda075dce6747c296da78016cee9cd47c95fa97f5072bd22fd2972` |
| `work/results-desk/allphase/lift_labels.out` | 768 | `1f4230df777d6c2978dc0363282f995c08718800b54d323e7a29e73e16370062` |
| `work/simplification-desk/r1-gates/MANIFEST-COMPLETENESS.md` | 2437 | `5521b496101778f1e400b704160c6e1c61c5e411743a822954c0f99ab1e4012d` |
| `work/simplification-desk/r1-gates/manifest-complete.json` | 58066 | `4c24ee676e79c450d0167fe326ea2e384bb97d41511ae388b967d6b239fb9d46` |
| `work/simplification-desk/r1-gates/line-accounting-r1-desk.json` | 2363 | `2233250bae3b9a2b973d3b7c865bad0f6eab738e56a515439126bfeb27f622fd` |
| `work/simplification-desk/jointpair/JOINT-PAIR-DECISION.md` | 2118 | `1c45c20940c3c23e71cc24a6e3927583455bee61b02b8c34f973a0761c18934d` |
| `work/simplification-desk/lean435/FEASIBILITY.md` | 3236 | `03a835b6307b8cdaee67867f6f9dae4d7ca34608971e417d68c80ad6c426711c` |
| `work/simplification-desk/r1-gates/R1-GATES.md` | 4736 | `a5df90aa838611f76d4af8fb9a2451a20fbe5b11c6d6418c5e74d8cd78da947d` |
| `work/simplification-desk/r1-gates/sig-compare-r4-r1.json` | 1379 | `62c8e7ef17fb446e3c0fe90b9378687c33ffaef1488588bbcb200840f4489265` |
| `work/simplification-desk/r1-gates/sigdump-r1.log` | 1882 | `405ab9a40ed32a27ca2a05dba515303538d289e81874957a6d9a42a460882897` |
| `work/simplification-desk/r1-gates/sigdump-r4.log` | 1888 | `496d94c0e5b78ff745395701667827aaa1cdc75dbd336b752f9538cf4d121f90` |
| `work/simplification-desk/r1-gates/sigs-r1.tsv` | 429981 | `87804fe988c547dff4e5b6b7480cc932a3624b0f38669e17584f1b0f1c408a60` |
| `work/simplification-desk/r1-gates/sigs-r4.tsv` | 430321 | `fa93e701a42a680bf3ee9e23b9aad9ac855199a564232a4aeff06382c567e4e1` |
| `work/simplification-desk/s1/BANKED-S1.json` | 3984 | `cb03beb06da77f378b31d856dc15a4e512e23eff65ccd71ebc5a14d8c3a184a1` |
| `work/simplification-desk/s1/line-accounting-s1.json` | 6390 | `79162e51db570a51e1fd1005dd800d42f7162961c28b560e56d92a1bae5d1997` |
| `work/simplification-desk/s1/dead-deletions.json` | 3027 | `bf403ef34c40414d3445b0d017085c13ae5c36755f1ad52b87a3aaa1c92409ce` |
| `work/simplification-desk/s1/sigs-s1.tsv` | 426665 | `8a93cff3eedb4fa3ebd67b8294d3b8bd567b07cbec91e19ee0a0baf396a819d7` |
| `work/simplification-desk/s1/AxiomRoots.lean` | 3814 | `4dda63592232d24a6da91e045980d93e2761c14488fcd427c82c3baa7d3842f5` |
| `work/simplification-desk/LOG.md` | 9867 | `a1e531d408810fed203e5fb145e497ee61f88566d05f319ada934c60bfd6e645` |
| `outputs/ASTRA-DISJUNCTIVE-PALETTE-A8.txt` | 15221 | `d292fa5a44fa857d957ed8eeb4895b192d4ca505f6f872c1ba5e644b80a6b437` |
| `outputs/ASTRA-FOUR-LIST-A5.txt` | 15053 | `799cef0737b23deb8e17d1cb5ca197b394c4e9a19e3c5a79acebed2671f3955e` |
| `outputs/ASTRA-FOUR-LIST-REFEREE.txt` | 15430 | `29e3800ecb740d9699254787d5a5b8689372d505b69a178eb08e447eada7548f` |
| `outputs/ASTRA-MC120-ENDPOINT-A5.txt` | 11571 | `78503d6ee09748eed6368e2080e88571b9700c7cfbb761db028c14d85c0ce25e` |
| `outputs/ASTRA-MC120-ENDPOINT-REFEREE.txt` | 14684 | `318773a2908246dc86186ed84a58a3cd1df2056481dc0379f02b35d3d6d5ce77` |
| `outputs/ASTRA-PAIRED-COROLLARIES-A6.txt` | 9630 | `94a6b50a2c0530555f494e9ef7618e1f8afa051d559ebf03f54994639c02a03f` |
| `outputs/ASTRA-PAIRED-PRODUCER-A6.txt` | 14588 | `2a7e4aed6b6db4ebcbff0d09e43c002ae4dae86b13bf3bf1606c19435ec9649e` |
| `outputs/ASTRA-PARTIAL-PALETTE-A7.txt` | 12861 | `cfa34f367d772dd720a6377d88ed7f84b549d1dbf8a9c5a5406c56899ec24872` |
| `outputs/CLAUDE-A7-CONTACT-AUDIT.txt` | 6251 | `596fdbac4c7bde20e1cec4e8094eb5fc67905f723c5222fb5e67ba5738e711ad` |
| `outputs/CLAUDE-SIX-ORBIT-PROOFS.txt` | 5210 | `34ed301a1133977bd00aebd23a9213898eabf23a7e4b4e76b43a0dea655dc4c1` |
| `outputs/CONSOLIDATED-FINDINGS.txt` | 64008 | `5de1cbed9b1194cf182a871dd0bc9657f32626e1f6592de43c9f43502fc7974b` |
| `outputs/PROGRESS-LOG.txt` | 69979 | `e2d2329f6ce4660172a88d4652f4bf7d5f99def54403a485508a0436c7ed0cf9` |
| `outputs/RESEARCH-STATUS.txt` | 7973 | `01c6c9d311eeae6b81aa6dc55c4fb78ba2ce10d4715c9eed2722c2b1de511e5c` |
| `outputs/RunLeanQueue.py` | 9451 | `c063969225cec881cdb63ebea165434a2fdc7d3d381528cc6d8e870dd286b2b6` |
| `outputs/LeanSourceGate.py` | 2246 | `721e47d80c4459e9125a9b66fe880ab31c37260e9797d23669a9a228c8f4e721` |
| `work/cloud-supervisor/RESEARCH-STATUS.md` | 3506 | `461dfcc8d25a2971038bbff6a6d691701008009583c04f8c8f7cca030ff3de50` |
| `work/cloud-supervisor/LOG.md` | 19245 | `13ccbdfb14837d21bda83d36ed14ee42cb354f277ea2cd6c4734b564e5adae33` |
