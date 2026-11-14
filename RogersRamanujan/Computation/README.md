# Computation (C) -- RR127

Canonical contract, exact enumeration, and the BZ82 reference map.

## Files

| File | Role |
| --- | --- |
| `rr_core.py` | The frozen contract: `is_partition`, `weight`, `is_residue`, `is_gap`, `enumerate_residue`, `enumerate_gap`, `count_*_dp`, `staircase`, `unstaircase`, `T`, `Tinv`. Rejects invalid input with `ValueError`. |
| `bz82.py` | Bressoud--Zeilberger 1982 reference map: signed states `X(n)`, the involutions `phi` and `psi`, the iteration, and `forward`/`inverse`. Source locators and every reconstruction decision are in the module docstring. |
| `run_checks.py` | Driver. Emits `results.json`. |
| `results.json` | The manifest for the recorded run (currently `NMAX = 50`). |
| `results_n30.json`, `results_n50.json` | Frozen copies of the two recorded runs. |

## Reproduction

```sh
cd RogersRamanujan/Computation
python3 run_checks.py 30      # 4.3 s, bijection verified through weight 30
python3 run_checks.py 50      # 257 s, bijection verified through weight 50
```

`results.json` keys: `fixtures`, `counts` (six methods per weight plus the
generic filter for `n <= 20`), `counts_all_agree`, `staircase_and_T`,
`bz82_bijection` (per-weight injectivity, surjectivity, both inverse laws,
determinism, weight), `involution_structure` (`phi^2 = id`, `psi^2 = id` per
weight), `elapsed_seconds`.

## Honesty notes

* Everything here is **TESTED_FINITE** over the stated bound. No all-n claim is
  made, and no count result is allowed to promote a claim above that level.
* The BZ82 iteration uses a **repeated-state detector**, not a step cap, so a
  cycle is reported as a failure instead of looking like a timeout.
* `Math.random` is not used anywhere; results are deterministic and seedless.
* The `phi` Case II tie-break is a reconstruction, documented in
  `../Main/DECISIONS.md` D-3. It is the only place where the source is not
  followed verbatim, and the deviation is forced by the source's own examples.
* `rr_core.A003114` is a recalled reference table kept only as a tripwire. Its
  tail (55 at `n = 24`) disagrees with all six methods and is believed wrong;
  do not use it as an oracle.
