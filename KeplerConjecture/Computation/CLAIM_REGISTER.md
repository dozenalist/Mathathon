# Computation claim register — after review 0138-C

Single place for Main to see every claim I hold, its status, and its evidence. Statuses follow
the roadmap vocabulary with two additions used only where the reviewer required them:
`TESTED_FAMILY` (finite search over a parameter family; **no** optimality or closure implied) and
`PENDING_MAIN_FIX` (evidence depended on Main's `shell_check`, unsound per review 0138-C).

## Exactly verified

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| `K15-C-VERIFIEDCERT-001` | `VERIFIED_EXACT` | `Δ ≤ 0.77996622` for every unit-sphere packing in `R³`; degree-33 rational certificate, accepted by `exactcert` **and** the independent SymPy oracle | `out/verified_certificate_K33b.json`, `verify_certificate.py` |
| `K15-C-REVALIDATE-001` | `VERIFIED_EXACT` | four shell-route verdicts survive my checker after exact basis conversion: `0.78037032` (`n=27`, unconditional) and `0.78033446` (`n=12`, conditional), both `η` variants | `REVIEW_0138.md` §2 |
| `K15-C-SOSQSIDE-003/004` | `VERIFIED_EXACT` | best explicit-Gram certificate: `q = (1/12)² + (11u/6 − 19/4)² + u(7/4 − 2u/3)²`, `Δ ≤ 1.99064200`. Reached by hill-climbing; three further seeds land in `[1.9906, 1.9989]`, so the family has **plateaued at ≈2** — best-found, not optimal | `sos_qside_polish.py`, `REVIEW_0138.md` §11 |
| `K15-C-SOSFAMILY-001` | `VERIFIED_EXACT` | explicit rational square on the `p` side: `−p = 0 + (u−T)(u−c)²`, `Δ ≤ 5.99152482` | `sos_family.py` |
| `K15-C-SOSGRAM2-001` | `VERIFIED_EXACT` | degree-5 two-square family, best `Δ ≤ 6.73788568`; extra freedom did **not** help | `sos_family2.py` |
| `K15-C-SOSSHELL-001` | `PROVED` (family-restricted) | in the cubic family, `eta_suff = (T'-T)M^2` is a *sufficient* allowance and `sup p > 0` on `[T,T']` always, so every admissible `eta` is positive and every shell member is strictly worse than `eta=0`. **Corrected**: an earlier version called it 'the smallest, attained' -- false -- and the repair `eta >= p(T)` is false at `c = T` | `sos_shell_variant.py`, `tests_0138.py` T4 |
| `K15-C-CUTEQUIV-001` | `PROVED` (elementary) | the full-period blob makes the cut condition read `ρ ≤ 1/√32` — **the Kepler bound itself**, so the condition is equivalent to Kepler rather than independent | `cut_deficit.py`, `REVIEW_0138.md` §7 |
| `K15-C-FOURIER-AUDIT-001` | `PROVED` A1/A2, `TESTED_FINITE` A3 | Main's `fourier_map` correct: 49/49 exact agreement, `M² = I`, quadrature to `1e-13` | `audit_fourier.py` |
| `K15-C-POSCERT-001` | `PROVED` (elementary) | `c=(4,1)` ⟹ `Δ ≤ 44π/15 = 9.215339`; hand-checkable positive control | `CERTIFIER.md` |

## Finite-search evidence — **not** optima, **not** closures

| claim | status | statement |
| --- | --- | --- |
| `K15-C-FAMTESTED-001` | `TESTED_FAMILY` | best value found in the tested `(K, Umax)` grid is `0.78037032` at `(33,120)`. The ladder is non-monotone (`K=17` worse than `K=15`), so the search is **not** exhaustive |
| `K15-C-SHELLGAIN-002/003` | `TESTED_FAMILY` | the *uniform* `n`-neighbour allowance was not used by the LP in the cases tested (16 exact comparisons, two bases). Says **nothing** about local/configurational strengthenings |
| `K15-C-SHELLBENCH-001` | `TESTED_FINITE` | grid LP, `η = 0` throughout; held-out tests exposed under-resolution at `K ≥ 21` |
| `K15-C-CUTBLOB-001` | measured | `Φ > 0.008880` from one fixture; a **lower bound**, not a refutation |
| `K15-C-TESTS-0138` | `PROVED` (machine-checked) | `tests_0138.py`: every review-0138 claim checked by exact expansion -- both Gram identities, `eta_suff` sufficiency, `sup p > 0`, the cut equivalence, the 12-contact jamming | `tests_0138.py` |
| `K15-C-CUTJAM-001` | `TESTED_FINITE` (negative) | FCC/HCP at separation 2 are jammed (12 contacts at exactly 2), so no perturbation preserves separation: amplitudes 0.06 → 1.894, 0.01 → 1.982. **No near-Kepler cut fixture by perturbation** |
| `K15-C-SOSQSIDE-002` | measured | degree-7 `q`-side squares give `38.136` — worse than degree 5; bounds what a naive search may claim |
| `K15-C-SOSIRRED-001` | `TESTED_FAMILY` (negative) | LP-optimal certificates are irreducible over `Q` at degrees 5, 7, 9, 13, 33, so no factorisation-based rational Gram export exists |
| `K15-C-SATURATION-001` | `TESTED_FAMILY` | the Laguerre pipeline's best is at degree 33 (`0.77996622`); degree 37–41 failed at every grid/margin tried |

## Pending Main's checker fix

| claim | status | why |
| --- | --- | --- |
| shell-route numbers quoted from `shell_check` alone | `PENDING_MAIN_FIX` | `shell_check` at `6626714` falsely accepts three inputs (`REVIEW_0138.md` §1). The certificates themselves were re-verified by my checker and stand; only `shell_check`'s *agreement* is uninformative until audited |

## Refuted / withdrawn (retained as evidence)

| claim | status | note |
| --- | --- | --- |
| `K15-C-EXACTCERT-001` and the `K = 9…21` ladder | `REFUTED` | review 48443: ten simple positive roots of `q`; the checker had a verbosity-gated failure return and `yun_odd_part` lost the leading sign. All `out/certificate_K*.json` are failed candidates, retained |
| `K15-C-BUG-001 … -005` | `PROVED` (defects) | five defects in my own code, four caught only by an independent checker |

## Open obligations

1. **One certificate with obvious rational Gram on BOTH sides at useful strength.** Each side is
   individually demonstrable (`K15-C-SOSQSIDE-003` Fourier side, `K15-C-SOSFAMILY-001` `p` side);
   doing both needs an SDP with rational Gram rounding — no solver on the SAIR VM.
2. **A near-Kepler fixture with unequal cell volumes** for the cut-deficit scan. Perturbation is
   *ruled out* (`K15-C-CUTJAM-001`: close packings are jammed), so this needs a Frank–Kasper phase
   (A15, σ) constructed exactly. This is the next concrete build.
3. **Re-run every `PENDING_MAIN_FIX` item** after Main's `shell_check` fix is audited.
4. `shell_sos.py`'s SOS structure is unimplemented; it is an LP.
