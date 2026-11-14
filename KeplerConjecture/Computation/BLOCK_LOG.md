# Block log — review 0353-C (12:08:35Z → 13:08:35Z)

The review asked for checkpoints at 12:28, 12:48 and 13:08. This file records what was true at each,
**reconstructed from the commit timestamps** rather than written live, and says so.

## 12:28 — repairs in, theorem repair in, the convention under way

Committed and pushed by this point:

* `2fa125c` (12:11:53Z) — the review's four defects, each with a regression test (S10–S12):
  the exact radical enclosures, the exact icosahedral edge gate with a direction per soundness
  requirement, the FCC constructor, and the saturation flag.
* `4462503` (12:15:34Z) — `REVIEW_0353.md` with the claim-status table, and the **theorem repair**:
  the large-box proof needed a `D`-saturation hypothesis it had never stated, and the valid
  replacement for the withdrawn equivalence (`K15-C-CUTIMPLIES-003`) was proved.

In progress at 12:28: the periodic-boundary convention (`period_convention.py`).

## 12:48 — convention, ball counting, verifier, duality, bracket

Everything above, plus:

* `cce3fd8` (12:30:57Z) — the periodic convention; ring-cell volumes computed.
* `0f0f8cd` (12:32:14Z) — `highdensity_cut.py` and `NONUNIFORM_SHELL.md` §3.0/§3.1.
* `020b501` (12:36:18Z) — `compact_verify.py`, the third checker; ring cells proved **congruent**
  (correcting my own earlier claim) and measured to 3.4·10⁻¹³.
* `b1e832f` (12:37:35Z) — `t*` bracketed from both sides, width 8.3·10⁻²³.
* `6fbd0a1` (12:38:13Z) — `STATUS.md` rewritten for Main.
* `e229923` (12:39:22Z) — `feasible_flow` defect found by the new duality test and fixed.

At 12:48 the remaining work was: HD3, the refuted-certificate marking, the clock section.

## After 12:48 — everything else in the block

* `a1d99ef` (12:40:46) — the ring-cell congruence is now machine-checked, not just measured
* `8b8900a` (12:41:26) — HD3 -- the ball-counting bound also kills every finite capacity
* `a3f897f` (12:42:26) — the seven rejected certificates now SAY they are rejected
* `65ee36a` (12:43:15) — a test that keeps the refuted candidates marked as refuted
* `e3948da` (12:43:52) — block clock section -- every commit with its UTC time
* `f89aff8` (12:44:51) — record the clean-clone check of the pushed branch
* `9635c5e` (12:45:44) — exercise the external-fixture path end to end, with a worked example
* `66f1fa1` (12:46:30) — retire the last references to the withdrawn 'equivalent to Kepler' ...
* `716a1b3` (12:50:36) — say out loud that the explicit-Gram bounds are above 1
* `b1147f5` (12:51:26) — measured runtimes, so a host elsewhere can budget its runs
* `8b0cef9` (12:52:06) — the averaging line needs o(|B|), not O(L^2), in the count
* `576d349` (12:53:39) — record the twice-run clean-clone determinism check
* `03386cd` (12:54:26) — test the PROVISIONAL stamping path, which was documented but never run
* `8934270` (12:54:53) — quote the V_dod gap exactly (3.86e-12, not a rounded 3.9e-12)
* `825e7db` (12:55:12) — checkpoint log for the block, reconstructed from commit times
* `5ce3d4d` (12:56:33) — hash-seed robustness check
* `24951b8` (12:57:02) — ce3_baseline writes into out/ like every other script
* `d6a1b08` (12:58:46) — withdrawal banners on the two historical review responses
* `61dabc2` (12:59:14) — INTERFACE.md no longer says 'no output here is a certificate'

Beyond the commits: the whole checker set re-run from a clean clone (twice), the
suite under five `PYTHONHASHSEED` values, every script timed into `RUNTIMES.md`,
the external-fixture path exercised for the first time, and every headline number in
`REVIEW_0353.md` recomputed and compared with the document (one rounding was
corrected as a result).

## 13:08 — block complete

Full detail in `REVIEW_0353.md` §7, which lists every commit with its UTC time and what was re-run
after the last one.
