# Handoff for the next scheduled review

> **Recovery note (2026-11-14T06:48Z).** After the Open Math OS outage the block was reconciled
> rather than repeated: every script and artifact was rerun from disk and gives identical output,
> no shell job survived, no stray write remains in `attachments/`, and no new swarm was started.
> This assignment is complete. First concrete step for the next block is item 1 below.

## One-line state
The solve track's strongest candidate implication does not reach a numeral, and its most
load-bearing lemma (self-avoidance) survived my attack: its proof was wrong, its statement is true.

## What I did (20-minute block, no edits outside this directory)
1. Read the paper's actual statements (Definition 5.1, Lemma 5.2 and Remark 5.3, Corollary 5.4,
   Definition 6.1, Lemma 7.5, Lemma 7.6) in `notes/paper-layout.txt`, plus `sprint/k6/REPORT.md`,
   `sprint/k6/WEAKEST.md`, `results/K6-BARRIER.md`, `results/continuation/*`, and the two other
   solve supervisors' paths.
2. Chose the target: `(W) => Prop 7.1 at k=6` (Theorem A) as the strongest implication, and
   "self-avoidance" (Lemma D) as its most attackable support, since the `S_1` reduction of `(W)`
   to the 3-cycle locus uses it.
3. Attacked Lemma D and produced a verdict plus a repair: `notes/LEMMA-D-REPAIRED.md`.
4. Adjudicated the multiplicity conflict between `sprint/k6/REPORT.md` and
   `results/continuation/SUMMARY.md` (the latter's inference is a non-sequitur).
5. Ran a 4-member swarm `smwfyfc11` on four disjoint audits; it hit its 14-minute cap without
   formal submissions but left two scripts; I ran m2's and it corroborates the repair.

## The ranked ledger
`LEDGER.md`. Short form: R1 `(W) => §7` viable but reaches nothing; R2 §8 at `k=6` failed at the
palette level and cannot be closed without trace-consistency (= the colouring, T3); R3 the `S_1`
reduction is the sharpest live attack surface on `(W)`; R4 Lemma D repaired here; R5 multiplicity
adjudicated; R6 dead routes.

## What the next block should do, in order
1. **Outstanding from this block**: recount the orbit words of `sprint/k6/REPORT.md` §6 with
   constraint 1 deleted and with it weakened, so the record knows which published numbers are
   unconditional. `sprint/k6/orbit_correct.py` is the reference enumerator; my subagent's
   `.ultramath/smwfyfc11/m1/orbit_audit.py` was not run.
2. **The alternative route** (the only formulation of `(W)` that is sharp and reachable without a
   colouring): at `k=6` in `S_1`, prove no accumulation of 3-cycle centres. First falsifiable
   sub-lemma: a 3-cycle centre with `|P_x(e)| = 3` on a positive-measure arc forces `|P_y(e)| <= 2`
   at unit neighbours `y = x+a`; decide by exhaustive finite check over 6-label palette systems at
   three consecutive centres with (5.7), m2's `|P_x|+|P_y| <= 5`, and Lemma 6.2's avoiding trace.
3. Do **not** re-run: finite two-centre CSP as a route to `chi >= 7`; palette-level §8 at `k=6`;
   size/content conditions on `L`; recolouring m3's `k >= 7` gadget.

## Escalation candidate (see STATUS.json `escalation`)
`(W)` in the sharpest form: in `S_1`, the 3-cycle locus has no accumulation point at `k = 6`.
Everything needed (definitions, hypotheses, attempted approaches, the desired output, and the
acceptable weaker output in terms of m2's bound) is in `STATUS.json`.
