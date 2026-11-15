# Cross-desk consistency audit — submission vs results ledger

Audited 2026-11-15 ~01:15Z by the results desk against [RESULTS-LEDGER.md](RESULTS-LEDGER.md) (batch 2, commit e196449).
The submission was read at commit f59c29e: `Exposition/Submission/report.tex` (1,178 lines), `Exposition/Submission/slides.tex`
(212 lines) and `Exposition/ProofWalkthrough.md` (Lessons 1–6, 895 lines). Status words are translated with the report's own key
(report.tex:603–612): `LEAN_VERIFIED` = "checked in Lean 4.34.1 (archived logs)"; `PROVED_PAPER_REVIEWED` = "proved (paper argument,
independently reviewed)"; `TESTED_FINITE` = "checked by computation"; `CANDIDATE` = "not claimed". The results desk did not edit
the exposition files. Mismatches were sent to the exposition desk with these line numbers.

**Verdict:** 39 statements checked. 35 match and 4 do not; every mismatch is a stale detail, not an overclaim. No document claims
a global chromatic result. No document cites an `UNAUDITED_NUMBER` or a `CANDIDATE` as established. (1/648 has since been upgraded to `TESTED_FINITE`.)

| # | Where | Ledger id | Status stated | Ledger status | Result |
| ---: | --- | --- | --- | --- | --- |
| 1 | report:226, 618, 1158; slides:54, 215; walkthrough:725, 789, 891 | headline | "No global chromatic result"; 6 ≤ χ ≤ 7 inherited | headline | MATCH |
| 2 | report:73, 144; slides:49 | THREE-CENTRE | proved; Lean 4.34.1 | LEAN_VERIFIED (+ referee) | MATCH |
| 3 | walkthrough:717 | THREE-CENTRE | identical statement and binders; recorded pass | LEAN_VERIFIED | MATCH |
| 4 | walkthrough:721, 791, 871, 887; slides:155; report:1161 | R1 | integrated, accepted 14 Nov; 27 modules + roots; gates are follow-ups | LEAN_VERIFIED; R1-GATES was OPEN at audit time, now TESTED_FINITE (PASS, 02:50Z) | MATCH at audit time; the "follow-ups" wording is now stale (report.tex already cites the gates as passed) |
| 5 | walkthrough:721 | R1 | States 764 → 566 | 764 → 566 | MATCH |
| 6 | report:74, 286–298; slides:50, 177; walkthrough:573, 793, 873 | CC60 | proved (refereed); Lean 4.34.1 | LEAN_VERIFIED | MATCH |
| 7 | report:330–339 | CC60 (OA120 part) | proved; Lean 4.34.1 | LEAN_VERIFIED | MATCH |
| 8 | report:428–440 | CC60 (ConeSurvivor consumer) | Lean 4.34.1 | LEAN_VERIFIED | MATCH |
| 9 | report:465–476; slides:186; walkthrough:793 | SHARPNESS-20 | proved (refereed), not Lean, 20 colours | PROVED_PAPER_REVIEWED | MATCH |
| 10 | report:650–656; walkthrough:794 | ENC-R4 | −126 lines; Lean 4.34.1 | LEAN_VERIFIED, −126 | MATCH |
| 11 | report:75, 673, 1115; slides:208 | ENC-R4 + R1 | 150 lines shorter (126 + 24) | −150 realised | MATCH |
| 12 | report:678–697; report:1116 | STEPBAN-V2, -CONSUMER, -CYCLICCORE, FIVESUPPORT-SWAP | Lean 4.34.1; structural; +61, about +23 | LEAN_VERIFIED; structural | MATCH |
| 13 | report:701–712; walkthrough:792 | JOINT-SUPPORT | Lean 4.34.1 (+ refereed); standalone | LEAN_VERIFIED | MATCH |
| 14 | report:718–722 | LEMMA67-IDENTITY | proved (refereed) | PROVED_PAPER_REVIEWED | MATCH |
| 15 | report:729–730, 1047–1055 | DIAMOND, FIVE-CYCLE-RESIDUES, CONNECTED-SET, NULL-TRANSFER | Lean 4.34.1 | LEAN_VERIFIED | MATCH |
| 16 | report:629 | DIAMOND | partial 4.35.0 exception | 4.35.0 core run printed axioms, no exit status recorded | MATCH |
| 17 | report:737–743 | AC-ALIGNED | proved (refereed) | PROVED_PAPER_REVIEWED | MATCH |
| 18 | report:749–756 | NR-TC | proved (refereed) | PROVED_PAPER_REVIEWED | MATCH |
| 19 | report:762–765 | RESIDUAL-GRAPH | proved (refereed) | PROVED_PAPER_REVIEWED | MATCH |
| 20 | report:771–775 | STRAIGHT-NEEDLE | proved (refereed) | PROVED_PAPER_REVIEWED | MATCH |
| 21 | report:778–792; slides:195 | A5-FOUR-LIST | proved (refereed); producer an unreviewed candidate | PROVED_PAPER_REVIEWED; A6-PAIRED-PRODUCER CANDIDATE | MATCH |
| 22 | report:794–805; slides:196 | EVENWALK-R6 | Lean 4.34.1 (desk compile); A5 not formalised | LEAN_VERIFIED | MATCH |
| 23 | report:807–831; slides:197; report:1119 | A6-FORCING, A6-BRIDGE-R2, A6-BRIDGE-R2-G3, G3-R2 | Lean 4.34.1, conditional on SignTable, ForcingLemma; A6-GLUE open | LEAN_VERIFIED; A6-GLUE OPEN | MATCH |
| 24 | **report:825** | G1-R2 | "G1 compiled only inside the bridge job" | LEAN_VERIFIED; **also a standalone desk compile** (G1-Finish-mB-r2, 23:49Z, 100 s, standard axioms) | **MISMATCH (stale)** |
| 25 | **report:1051** (Table `tab:lean-other`) | G1-R2 | "Compiled only inside the bridge job" | as row 24 | **MISMATCH (stale)** |
| 26 | report:954–959 | A6-CONTAINMENT | Lean 4.34.1; no axiom list printed | LEAN_VERIFIED with the same caveat | MATCH |
| 27 | report:848, 865, 979–981; slides:206 | DIR-FILTER | 7,776 → 1,420 → 174 → 6; 95 was a bug, 79 missed | TESTED_FINITE | MATCH |
| 28 | report:863–864, 881; slides:205 | HEULE-UNION, HEULE-NO-FORCING | computation; 1,048 / 5,487; 34 colourings | TESTED_FINITE | MATCH |
| 29 | report:866 | FIXED-PHASE-CENSUS | computation; 177 / 7,599 | TESTED_FINITE | MATCH |
| 30 | report:867, 986 | STAIRCASE-CENSUS | computation; 76,283 of 36,415,008; sufficiency not shown; typo corrected | TESTED_FINITE (necessary condition only) | MATCH |
| 31 | report:868 | SIX-ORBIT | computation; relaxation level | TESTED_FINITE | MATCH |
| 32 | report:869 | A5-SLIVER | computation; boxes certified elsewhere | TESTED_FINITE | MATCH |
| 33 | report:870 | HONEYCOMB-73, HONEYCOMB-K16 | computation; restricted family | TESTED_FINITE | MATCH |
| 34 | report:894–902; slides:207 | MC120-ENDPOINT | proved (refereed), 19 colours | PROVED_PAPER_REVIEWED | MATCH |
| 35 | report:911–951 | ANNULUS-3COL, SUPPORT-FLIP, FOUR-STATE-ANGULAR, VARIABLE-TRIANGLE, A7-CONTACT, LOCAL-TRANSITIONS | proved (refereed) | PROVED_PAPER_REVIEWED | MATCH |
| 36 | report:999–1000 | A5-FAR-APEX, A5-M5-TEMPLATE | refuted | RETRACTED_OR_REFUTED | MATCH |
| 37 | **report:1003** | LEAN-FAILED-REVISIONS | "eight failed jobs, all superseded" | **nine** (adds job 20261115T001551-0, CyclicCoreConsumerFromV2, a staging defect; superseded by the desk r2 compile) | **MISMATCH (count)** |
| 38 | **report:1010** | A6-GLUE | "compile the bridge with G1, G3 and the forcing lemma spliced in" | G3 is now spliced (A6-BRIDGE-R2-G3); open part is SignTable + ForcingLemma (formal lane also lists hsupp/pairing assembly) | **MISMATCH (stale wording)** |
| 39 | report:1022–1031 | CANDIDATE ids; RELAX-1-648 | not claimed; 1/648 omitted | CANDIDATE; RELAX-1-648 was UNAUDITED_NUMBER at audit time and is now TESTED_FINITE (results-desk recount, 01:20Z) | MATCH (omission is safe; citing is now allowed) |

Note on row 12: after this audit, the research desk compiled `FiveSupportSwapR1-noV1.lean`, a version with the old step ban deleted (exit 0, 30/30 signatures
identical). The measured change is +33 physical lines (354 → 387; code lines only +9), replacing the "about +23" estimate. The report text at 693–697 should follow.
