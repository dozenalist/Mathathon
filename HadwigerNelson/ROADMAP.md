# Remaining work (updated 15 November 2026)

**No global chromatic result.** Each status below is taken from [RESULTS-LEDGER.md](RESULTS-LEDGER.md).

1. **Finish the Lean simplification.**
   - Done:
     - The three-centre integration is complete ([R1](RESULTS-LEDGER.md#r1), `LEAN_VERIFIED`).
     - Its contract and dependency gates pass ([R1-GATES](RESULTS-LEDGER.md#r1-gates)).
     - The dead-code pass [S1](RESULTS-LEDGER.md#s1) (`LEAN_VERIFIED`, −265 lines) also puts the branch-free step ban in place ([STEPBAN-SWAP](RESULTS-LEDGER.md#stepban-swap)). A second dead-code pass, [S2](RESULTS-LEDGER.md#s2) (`LEAN_VERIFIED`, −717 against R1), brings the realised total to −867 lines against the supplied original.
   - Remaining:
     - **Lean 4.35.0 port: Carter.** Rebuild the S1 tree, CC60 and the headline roots under the event's Lean 4.35.0, and re-run the axiom and signature gates ([LEAN-435](RESULTS-LEDGER.md#lean-435), open; handoff notes in [Lean/PORT-4.35.0-NOTES.md](Lean/PORT-4.35.0-NOTES.md)).
   - Keep `five_support_step_ban` (manuscript Lemma 6.7). Keep `state_support_avoiding_trace` (Lemma 6.2) too.
2. **Continue the geometric obstruction problem beyond CC60.** The open items are:
   - formalise the A5 obstruction and the support exclusions, the two named inputs left by the glued six-colour endgame ([A6-GLUE](RESULTS-LEDGER.md#a6-glue), `LEAN_VERIFIED` with those hypotheses);
   - [PALETTE-RIGIDITY](RESULTS-LEDGER.md#palette-rigidity);
   - [STAIRCASE-CONVERSE](RESULTS-LEDGER.md#staircase-converse);
   - [K6-PRODUCER](RESULTS-LEDGER.md#k6-producer);
   - [LOCALIZED-TWO-STATE](RESULTS-LEDGER.md#localized-two-state);
   - the conditional route to $\chi\ge7$ ([L6-F6](RESULTS-LEDGER.md#l6-f6)).
   
   Finite direction-grid results alone do not close this step.
3. **Outstanding independent reviews.**
   - Done: the four-list extension ([A5-FOUR-LIST](RESULTS-LEDGER.md#a5-four-list), `PROVED_PAPER_REVIEWED`).
   - Still `CANDIDATE`, each needing a referee:
     - the strict-$120^\circ$ obstruction ([MC120-STRICT](RESULTS-LEDGER.md#mc120-strict)), which has no referee file;
     - the explicit colouring of the two-list locus ([LIST-FIELD-A4](RESULTS-LEDGER.md#list-field-a4));
     - the paired-configuration producer ([A6-PAIRED-PRODUCER](RESULTS-LEDGER.md#a6-paired-producer)).
4. **Novelty of the sharpness theorem.** [SHARPNESS-20](RESULTS-LEDGER.md#sharpness-20) is refereed for arbitrary finite palettes. Still not established:
   - six-colour sharpness;
   - novelty priority against the literature.
5. **Imports.**
   - Done: the 15 November import (`Main/ResearchSnapshot/import-20261115/`), recorded in the results ledger.
   - Ongoing: import later results with their sources, independent checks and failure records. Reconcile newer evidence with the recorded status rather than promoting every worker-labelled success.

The original [research status](Main/ResearchSnapshot/local/outputs/RESEARCH-STATUS.txt) and [reboot plan](Main/ResearchSnapshot/local/outputs/RESEARCH-REBOOT-2026-11-14.txt) give the underlying contracts as of 14 November. This file launches no research jobs and changes no running coordinator or reporting schedule.
