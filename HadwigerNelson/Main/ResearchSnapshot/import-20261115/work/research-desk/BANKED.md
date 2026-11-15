# Research desk: banked local Lean results

Pinned Lean 4.34.1 + Mathlib (threecentre-r1 pin). All are local checks and proof simplifications or partial results. No global chromatic result.
R1 (threecentre-r1, 27 modules + root axiom check) was ACCEPTED by user decision on 2026-11-14 at about 23:25Z.

| Result | Where compiled | Source (work/...) | sha256 (LF) | Outcome | Note |
|---|---|---|---|---|---|
| A6-Forcing-m1 | queue job claude-lean-20261114t212205-0 | `lean-queue/claude-admissions/claude-lean-20261114t212205-0/Candidate.lean` | `27e45caf4c79389767a97d8bf705980462849d4f0a6d268e849989b253a916c8` | exit 0, 62.7 s | Mathlib-only |
| StepBanShort-r2 | queue job claude-lean-20261114t220720-0 | `lean-queue/claude-admissions/claude-lean-20261114t220720-0/Candidate.lean` | `19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655` | exit 0, 64.6 s; five_support_step_ban_v2 standard axioms | same telescope as v1 |
| G3-ArcCover-r2 | DESK compile | `research-desk/G3-r2/G3-ArcCover-r2.lean` | `39a02e68c878c0d0df0493d53114679ffd6cb01c3354329cd33f3867b9558c6e` | exit 0, 83 s; arcCover standard axioms | mA + le_or_gt (L160,L168) + #print axioms |
| A6-Bridge-r2 (incl. G1-r2) | queue job claude-lean-20261114t231544-0 | `lean-queue/claude-admissions/claude-lean-20261114t231544-0/Candidate.lean` | `74402da9ef754964e3a732c879e1b31fa3af419db1a465255e6a78b467f9b333` | exit 0, 66.9 s; 8 endpoints standard axioms (desk check research-desk/bridge-r2-axioms/axioms.log) | G3 not glued |
| StepBanConsumer | queue job claude-lean-20261114t232057-0 | `lean-queue/claude-admissions/claude-lean-20261114t232057-0/Candidate.lean` | `718b581518b553c471e9a984dc0dd44e8d6c54d3d9ed25209f1728a8a3a7310e` | exit 0, 58.6 s; both _v2 standard axioms; #check pairs identical (desk-verified) |  |
| EvenWalkReachability-rev6 | DESK compile | `research-desk/EvenWalk-rev6/EvenWalkReachability-rev6.lean` | `4439cf5dd4088ea6765337286399f5af462fd1c3f4976c82c99d77019bfb9904` | exit 0, 63 s; evenWalk_reachable, finite_list_obstruction, two_list_obstruction_of_even_walk standard axioms | rev5 + one show line + #print axioms |
| G1-Finish-mB-r2 (standalone) | DESK compile | `research-desk/G1-r2/G1-Finish-mB-r2.lean` | `fd3549e5acccd7b5ed18dbcc09c0e91c0dc03e638b6ee48d2efea734e27385d4` | exit 0, 100 s; cos_sign_strict, sign_of_paired_fin, signTableT_of_paired(_fin) standard axioms | mB + bridge's hm6 line + #print axioms |

## Exact computations / certificates

| Result | Artifact | sha256 | Outcome |
|---|---|---|---|
| Staircase census (necessary condition) | `research-desk/census/` (census.py LF da28d617…, independent_census.py) | — | SAT 177/7599; 76283 of 36415008; by k [177,2576,12762,26928,25200,8640]; two implementations agree |
| A5 sliver interval certificate | `cloud-supervisor/a5-sliver/certify_sliver.py` + CERTIFICATE.md | `63e84a36bfa95ea99103e314530dbaf38a9fa42667a8ac85b960882ff351e341` | ALL PIECES CERTIFIED (0.4 s); dependencies listed in CERTIFICATE.md |
