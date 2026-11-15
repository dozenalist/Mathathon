# OMM lane L-R1 (chat-0a863015ff) — "audit and reproduce" — task queue

Owner: results desk (per Jarom's 00:00Z guiding principle; lane assigned by the supervisor 00:16Z).
Rule: one pending results-desk message in automation-supervisor/user-inbox at a time. Send the next task only
after the previous one has been consumed (moved to user-archive). Results come back via coordinator
downloads in automation-supervisor/inbox/; the ledger status changes only after the desk checks them.

| Task | File | Size | Purpose | Ledger ids affected | Status |
| --- | --- | ---: | --- | --- | --- |
| R1-1 | R1-1.txt | 3964 | Exact two-way re-implementation: fixed-phase census 177/7599/862, staircase census 76283/36415008 by k, all-phase 933120/1440/919512/12168 cells and measure 1/648, the 16-of-3840 vs 16-of-120 discrepancy, the sign-cell pair | FIXED-PHASE-CENSUS, STAIRCASE-CENSUS, RELAX-1-648 | SENT 00:39:30Z (user-inbox 6ac770873d624c6eb674445643f1617e); pending (coordinator down 00:41–00:54Z) |
| R1-2 | R1-2.txt | 3572 | α* = (0,2,3,184,185,186) certificate; 60°ℤ completeness criterion; Thm B' (pure C2 obstruction witness) | ALPHA-SHARP, CENSUS-COMPLETE-60Z, THM-BPRIME | queued |
| R1-3 | R1-3.txt | 4202 | Adversarial referee of strict MC120 and Corollary P (no referee file exists) | MC120-STRICT, CONTINUOUS-SIX, A6-COROLLARIES | queued |
| R1-4 | R1-4.txt | 3961 | Adversarial referee of the A6 paired producer (table, forcing, a.e. bookkeeping, phase alignment, extensions) | A6-PAIRED-PRODUCER | queued |
| R1-5 | (to write) | | Explicit A5 odd-walk coordinates and vertex count (finite existence only today) | A5-ODD-WALK, A5-FOUR-LIST | idea |
| R1-6 | (to write) | | Independent re-derivation of J-depth ≤ 3 / circulant-orbit rigidity from the discovery STATUS (inbox 20261115T002122-download-5) | J-DEPTH, RELAX-CIRCULANT | idea |

Acceptance for every task: two independent checks or a line-by-line referee against quoted definitions;
explicit certificates; nothing marked proved without a written argument; no chromatic-number claims.
