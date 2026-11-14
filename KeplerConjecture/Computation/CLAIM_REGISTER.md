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
| `K15-C-SOSQSIDE-003` | `VERIFIED_EXACT` | best explicit-Gram certificate: `q = 3² + (3u/2−6)² + u(3/2−2u/3)²`, `Δ ≤ 2.61993314` | `sos_qside.py`, `REVIEW_0138.md` §11 |
| `K15-C-SOSFAMILY-001` | `VERIFIED_EXACT` | explicit rational square on the `p` side: `−p = 0 + (u−T)(u−c)²`, `Δ ≤ 5.99152482` | `sos_family.py` |
| `K15-C-SOSGRAM2-001` | `VERIFIED_EXACT` | degree-5 two-square family, best `Δ ≤ 6.73788568`; extra freedom did **not** help | `sos_family2.py` |
| `K15-C-SOSSHELL-001` | `PROVED` (family-restricted) | `η* = (T'−T)M²` is the smallest allowance in the cubic family, exact and attained, so every shell member is strictly worse than `η=0` | `sos_shell_variant.py` |
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
2. **A near-Kepler fixture with unequal cell volumes** for the cut-deficit scan. The present
   fixture's density is 55× below Kepler because its ring cells are huge; a close-packing
   perturbation needs a periodic Voronoi volume routine. This is the next concrete build.
3. **Re-run every `PENDING_MAIN_FIX` item** after Main's `shell_check` fix is audited.
4. `shell_sos.py`'s SOS structure is unimplemented; it is an LP.
