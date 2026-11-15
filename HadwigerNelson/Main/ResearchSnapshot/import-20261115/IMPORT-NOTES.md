# Import 2026-11-15 (results desk)

Captured 2026-11-15T00:23:02.218Z from the research workspace `C:/Users/jarom/Documents/Codex/2026-11-13/i` by the results desk. Files keep their workspace-relative paths under this folder; MANIFEST.json records each one with `source`, `sourceModifiedUtc` and `capturedAtUtc`. Compiled objects (.olean) are excluded, as in the original import. Nothing here was recompiled by the results desk: the excerpts below are copied from the existing compile records. See [../../../RESULTS-LEDGER.md](../../../RESULTS-LEDGER.md) for the reviewed status of each result.

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
| `work/research-desk/BANKED.md` | 3005 | `11eb30e070d5dc1d4b26248dcba5bfd481e132162bdc6927d33d7d255b7b61a5` |
| `work/research-desk/LOG.md` | 5829 | `bd2f55785a239bb2ad0885388014f0a2a59df46217a2bd528e979fd8b5136598` |
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
| `work/cloud-supervisor/a5-sliver/CERTIFICATE.md` | 4646 | `b6ac39dd14d55157abb05a593a775bf84362b71da007e1edf3d3c71eb9e5ca33` |
| `work/cloud-supervisor/a5-sliver/README.md` | 1427 | `ed053b8bcbf63e10111957f57b9a61a73183b7d7b8c30284303b5b30bd28adba` |
| `work/cloud-supervisor/a5-sliver/certify_sliver.py` | 11877 | `63e84a36bfa95ea99103e314530dbaf38a9fa42667a8ac85b960882ff351e341` |
| `work/cloud-supervisor/a5-sliver/certificate_output.txt` | 2677 | `68507c241873c543d5e56d7c6e162fb46ba96c1d19bbd431ad4b763fb4bfba41` |
| `work/automation-supervisor/inbox/20261114T224105-download-4-A5-SLIVER-DEFS.md` | 15314 | `714b2eb2a7eeb9a899774748855d2e6ec65ce231075579df145464ab04849f6d` |
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
| `work/automation-supervisor/research-plan.json` | 1241 | `4d3dd58ecfc1fc1454f364d82bc7a94a89c7f826521ab685b36029e8df12859f` |
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
| `work/cloud-supervisor/LOG.md` | 5757 | `9d66d7dabb4f66a71b4d9193d02737730a82df977f0bcd5ce53f27c40bc003ea` |
| `work/openmath-supervisor/checkins/20261114T191820Z/inner-outer-orbit-certificates.json` | 115033 | `6f546fb260b779a5bd05cee38bebd01894224da23861fd97c74fb990f185d67e` |
| `work/openmath-supervisor/checkins/20261114T191820Z/verify-inner-outer-orbits.js` | 1648 | `ae6c4d2beebe8c96c35cc9335ba6df34910693d7a498e81137903a585b2ce279` |
| `work/openmath-supervisor/checkins/20261114T191820Z/PROGRESS-REPORT.txt` | 2112 | `8973d2a1936137675d767cab21f0795d39193288a4596acd57ff1615618c3d96` |
| `work/openmath-supervisor/checkins/20261114T194118Z/graph-m2-REPORT.txt` | 11109 | `826555e70beeed2d6b1f8bf0559f5d0cfc9886087b7f8b5c033bce39e0f2eadc` |
| `work/openmath-supervisor/checkins/20261114T194118Z/q4-q5-forced-palette.json` | 2319 | `c7a71a223470b5b00db33d2ad901954907f0ffb441c9e7119ef292ba06e1641b` |
| `work/openmath-supervisor/checkins/20261114T194118Z/corner-all-phase-validation.json` | 1957 | `15a31adcb7c5ee267ca1e7d0c66b27d322bc36d518265d91ef991fd619efbcf6` |
| `work/openmath-supervisor/checkins/20261114T194118Z/PROGRESS-REPORT.txt` | 3586 | `8f6744bf837882600e2f7b71b2dce0cb048efecf36b39f13d6ea3d56b578ca33` |
| `work/openmath-supervisor/checkins/20261114T183522Z/PROGRESS-REPORT.txt` | 2480 | `c2aa01a9d8cebfd1dcd5f81c9c61c9434fbcef4c2d6bdc42858564fbb46444fc` |
| `work/openmath-supervisor/checkins/20261114T183522Z/TWO-TRIANGLE.md` | 4257 | `507982dc9879158e42512a5e09ee41e84e88d99f2b74a62c3d3966542caadb87` |
