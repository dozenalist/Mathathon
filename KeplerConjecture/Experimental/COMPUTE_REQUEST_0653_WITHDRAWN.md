# WITHDRAWN — `COMPUTE_REQUEST_0653.md`

Withdrawn at `K15-REVIEW-2026-11-14_0738`. Two reasons, either sufficient.

1. **The scan is unnecessary.** It was filed to test the premise `vol D' ≥ 5.5400` numerically.
   That premise is now *proved* — Fejes Tóth's theorem, as restated in Hales–McLaughlin
   Theorem 4.1 — so a numerical minimisation can neither strengthen nor weaken it.

2. **The request was mis-specified.** It asked for `premise_audit.py 600` under a "120 s per
   start" cap, but the script passed the whole budget to its *first* start, so the first start
   alone ran for the full 600 s. The script now caps every start at `120 s`
   (`per_start = min(120, max(5, secs/7))`), and it stays in the repository as a diagnostic
   anyone may run locally within that bound.

No job was ever filed with Astra under this request, so there is nothing to cancel.
