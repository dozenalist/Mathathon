# Computation local run request — Astra

Owner: Computation (`kepler15/comp-01a1d8c0`). Reviewer: X, then Main.
Everything here is **1 CPU, ≤ 1 GiB, ≤ 10 minutes** unless a row says otherwise. No Lean, no
SDP, no network, no scratch-directory paths — every command runs inside `KeplerConjecture/Computation` and
writes under `KeplerConjecture/Computation/out/`.

Two of the scripts need Main's exact checker. It is **not** fetched from a scratch directory: the
command below writes it into the working directory, and the scripts take its path explicitly with
no default, so a missing checker fails loudly instead of silently using something else.

## 0. Setup (once)

```bash
cd KeplerConjecture/Computation
git show omm/kepler15/main:KeplerConjecture/Computation/shell_check.py > shell_check_ext.py
```

## 1. Certificate and checker regressions (~30 s)

```bash
cd KeplerConjecture/Computation
python3 verify_certificate.py out/verified_certificate_K33b.json   # Delta <= 0.77996622
python3 exactcert_tests.py                                       # ALL TESTS PASS
python3 exactcert_oracle.py                                      # exact oracle, not sampled
python3 tests_0138.py                                            # every 0138 claim, exact
```

## 2. Cut/flow evaluator (~1 s) — the C044 package

```bash
cd KeplerConjecture/Computation
python3 cut_flow.py                     # writes out/cut_flow.json
python3 tests_cut_flow.py               # truth-known tests: ALL CUT/FLOW TESTS PASS
python3 cut_isoperimetry.py             # FCC isoperimetric profile: exponent ~ -1/3
python3 transfer_necessity.py           # a transfer implies rho <= 1/sqrt(32)
python3 k15fourier.py                   # M upper triangular, diag (-1)^i, M^2 = I
python3 cut_flow.py --fixture out/fixture_example.json   # external-fixture path
```

Expected: FCC and HCP report `TRIVIAL_SATISFIED` with `b = 0`; the icosahedral fixture reports the
singleton-cut threshold `Phi >= 0.008880268291` and a `PATCH_FEASIBLE` flow above it.
**No row may be read as a certificate except an explicit violating cut.**

## 3. Explicit-Gram certificates (~5 s each)

```bash
cd KeplerConjecture/Computation
python3 sos_family.py                  # p-side, one square,   5.99152482
python3 sos_family2.py                 # p-side, two squares,  6.73788568
python3 sos_pside_many.py --m 4 --deg 2 --iters 2500 --seed 3     # 1.33982382
python3 sos_both_sides.py              # both sides, cubic q,  2.00171738
python3 sos_both_sides_lin.py --m 3 --iters 1200 --seed 1         # 2.4770679955
python3 sos_both_sides_quintic.py      # one-square ansatz: scoped negative with its bound
python3 sos_both_sides_quintic2.py     # two squares: SOLVED, Delta 1.33982381256
```

**Strength reminder, which the local run should confirm rather than override:** every one of these
is **above the trivial bound `Δ ≤ 1`**. They demonstrate the certificate *format*, not a
competitive bound.

## 4. Main's checker cross-checks (~10 s)

```bash
cd KeplerConjecture/Computation
python3 audit_fourier.py shell_check_ext.py
python3 shell_propose.py --checker shell_check_ext.py --degree 9
python3 shell_propose.py --checker shell_check_ext.py --degree 33 --tlo-exact --Umax 120
python3 shell_sos.py --checker shell_check_ext.py --degree 7      # ODD and <= 7 only
```

`shell_check.py` at `6626714` is **unsound** (three false accepts reproduced in
`REVIEW_0138.md` §1); these rows exist to reproduce and to cross-check, never as a source of
truth.

## 5. The sweep — one portable command, seed range, cap, schema

```bash
cd KeplerConjecture/Computation
timeout 900 python3 sweep_explicit_gram.py --seed-lo 100 --seed-hi 120 \
        --iters 4000 --uphill 0.05 --cap 300 --out-dir out/sweep
```

One JSON per seed, schema:

```json
{"seed": int, "degree": int, "iters": int, "uphill": float,
 "status": "VERIFIED_EXACT" | "FAILED" | "TIMEOUT",
 "delta": float | null, "q": "poly in u" | null, "p": "poly in u" | null,
 "r": [[coeffs..]..] | null, "s": [[coeffs..]..] | null,
 "verification": {"q_identity": bool}, "seconds": float}
```

A summary line per seed and a final best-seed line go to stdout, so a truncated run still yields
usable data. 20 seeds at ~40 s each is about 13 minutes on one core.

**Pilot results, and why the cap is 300 s.**
* Eight seeds at `--iters 1500` all returned the identical start value `1.99064200`: `1500`
  iterations does **not** escape the local optimum. The runs that reached `1.37125723` used
  `--iters 4000`, so **use `--iters 4000` or more**.
* Runtimes differ by **more than 3× between machines**: `--degree 7 --iters 4000` takes **27 s**
  here, while seeds 100–102 hit a **90 s cap** on the reviewer's host without producing a final
  candidate. Hence `--cap 300` and a budget of **30–100 minutes** for 20 seeds, not the 13 minutes
  quoted earlier. A capped seed is recorded as `TIMEOUT` and the sweep continues, so this degrades
  gracefully.

**Why the sweep matters.** The record moved `5.99 → 2.62 → 1.99 → 1.41 → 1.37` as search effort
increased, and twelve basin-hopping runs span `1.37 … 2.00` with the best appearing once. A few
hundred seeds is the cheapest open improvement, and it is a job for a bigger machine, not the
SAIR VM.

## 6. Resource caps and success criteria

| row | wall time | RAM | success criterion |
| --- | --- | --- | --- |
| §1 | < 60 s | < 300 MB | all exit 0; `Delta upper` = `0.779966216777` at 12 dp |
| §2 | ~10 s | < 200 MB | FCC/HCP `TRIVIAL_SATISFIED`; threshold `0.008880268291`; `tests_cut_flow.py` all pass; isoperimetry exponent between `-0.30` and `-0.36` |
| §3 | ~5 s | < 500 MB | each prints an `EXACT` line; identities `True`; `quintic2` reports `1.33982381256` |
| §4 | ~15 s | < 300 MB | `AUDIT PASS`; the two degree rows pass |
| §5 | ≤ 15 min | < 300 MB | one JSON per seed; at least one `VERIFIED_EXACT` |

## 7. What the checkers actually prove

`verify_certificate.py` proves: for the rational `p, q` in the JSON, `p < 0` on `[8·π_lo, ∞)` and
`q > 0` on `[0, ∞)`, with `π_lo < π`, so the region verified is *strictly larger* than required;
hence the Cohn–Elkies hypotheses hold and `Δ ≤ (4π/3) p(0)/q(0)` for every packing, by the cited
CE theorem. **Tails are not an obligation for this basis**: `p(t)e^{-t/2}` is Schwartz.

The both-sides certificates prove the same two sign conditions **by algebraic identity**, with no
Sturm sequence at all — but at strengths above 1, so they are format demonstrators.

`cut_flow.py` proves, for an explicit finite `U`, that `Σ_U b > Φ|δ⁺(U)|`. That is a genuine
obstruction for the infinite packing. A flow it reports is `PATCH_FEASIBLE` and nothing more.

## 8. Not shown, and open

* No equivalence between the cut condition and Kepler (`K15-C-CUTEQUIV-001` **withdrawn**); the
  missing lemma is a uniform perimeter-growth bound for finite `U`. See `REVIEW_0308.md` §2.
* No competitive explicit-Gram certificate: all are above the trivial bound 1.
* The quintic two-square ansatz is excluded for the p-side record certificate with a stated bound
  (`|f| ≥ 195.95`, `REVIEW_0308.md` §4), not by a failed search.
