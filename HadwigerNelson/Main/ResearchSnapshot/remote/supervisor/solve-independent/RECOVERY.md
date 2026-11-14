# Recovery note (after the Open Math OS outage)

Written 2026-11-14T06:46 UTC by this chat, at Jarom's one-time recovery prompt.

## State reconciled

* **Jobs:** none. `shell_jobs` reports 0 running for this session; no background job, no Lean build,
  no search was in flight when the outage hit. Nothing to resume, nothing to kill.
* **Last block:** `STATUS.json` at `2026-11-14T06:22:03Z`, `status: completed_block`. It was finished
  and saved before the outage.
* **Artifact integrity re-checked, not assumed** (re-ran from the saved scripts, diffs against the
  saved outputs):
  * `forced_a1_5.py` -> rc 0, `forced_a1_5.out` **byte-identical**;
  * `verify_cell_nogo_v2.py` -> rc 0, `verify_cell_nogo_v2.out` **byte-identical**;
  * `square_family.py` -> rc 0;
  * `audit_rect.py` -> rc 0, same numbers (14301 witness pairs, 0 failures, 174 corner-equality pairs,
    coverage gap `0 < s <= 1/60`).
  So no partial or uncertain write exists in this directory; nothing was duplicated or re-derived.
* **Files outside this directory:** untouched. Other `supervisor/*` directories show fresh mtimes
  from other chats; I read them only.

## What stands (unchanged by this recovery)

* `CELL-A-FIFTH.md` — the exact `a = 1/5` honeycomb data: forced set `F = {N in {4,7,9,12,13}}` (42
  offsets), ring 3 a pure tangency with the six endpoint exceptions saved, ring 16 unforced because
  `dmin >= 1`, cluster structure (<= 4 cells, clusters >= 1.3856 apart), and the proved periodic
  index bound `16` attained by `4Z^2`.
* `CELL-NOGO-v2.md` — corrected cell-family theorem: strict criterion `dmin < 1 < dmax`, range
  `(1/sqrt13, 1/2]`, interiors disjoint with dense union but not a partition, and the K_7 diameter
  lemma scoped to the **clique** route below cell diameter 0.24407 only.
* `LEDGER.md` — valid / overbroad / unverified ledger for my v1, the retiring rectangle worker and
  the retiring graph worker.
* `CELL-NOGO.md` — v1, kept unmodified as changed evidence.

## Next concrete step (not started; unchanged by the recovery)

Decide six-colourability of **one** period at `a = 1/5`, at index `>= 16` (the bound makes anything
smaller provably empty), e.g. an index-16 or index-20 sublattice: the finite graph is the cosets of
`Lambda_p` in the triangular lattice with connection set `F mod Lambda_p`. Before any search, the
implications are fixed: UNSAT rules out colourings periodic with that exact period only; SAT yields a
> **REPAIR (later block, `NULL-TRANSFER.md`).** The sentence below is withdrawn: by the null-set
> transfer lemma, a colouring of **all** cell interiors separated on the strict forced pairs already
> gives `chi(R^2) <= k`. There is no residual ownership rule and no tangency obligation. (A *finite
> patch* still would not suffice — that part stands.)

labelling of the cell **interiors** only, and still owes an ownership rule on the 1-skeleton, exact
unit-distance checks on a fundamental domain, and compatibility with the six ring-3 tangency pairs.
Nothing in this line bounds `chi(R^2)` in either direction, and that must not drift in the handoff.

## Standing constraints carried forward

Single-agent; no swarms or subagents; write only `supervisor/solve-independent/`; read everything else
read-only; inherited rectangle certificates restricted to their verified open boxes `s > 1/60` off the
walls `60s, 60t in Z`; distinguish paper proof / exact check / conditional claim / open gap.
