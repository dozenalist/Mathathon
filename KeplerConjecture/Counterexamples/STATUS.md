# Counterexamples (X) — what is in this directory and what backs it

Snapshot at block `K15-X-040`, `2026-11-14T12:35Z`, branch `kepler15/counterexamples/run-01`.
One line per artifact: what it is, what checks it, and what it is *not*. If a claim here and a
claim in `REGISTRY.md` differ, `REGISTRY.md` wins.

## Certificates (the only objects with a machine-checkable verdict)

| file | claim | verifier | status |
| --- | --- | --- | --- |
| `X_C010` (in `verify_all.py`) | `δ ≤ 0.818086808` | `verify_all.py` (exact sign + Li floor) | VERIFIED |
| `X_C013_certificate.json` | `δ ≤ 0.794809296` | `verify_all.py`; rebuilt independently by Astra | VERIFIED |
| `X_C014_certificate.json` | `δ ≤ 0.780718153` | `verify_all.py`; **p-side only** | VERIFIED |
| `X_C015_certificate.json` | `δ ≤ 0.813631102` | `verify_all.py`, no sign predicate | VERIFIED |
| `X_C016_certificate.json` | `δ ≤ 0.783097911` | `verify_all.py`, no sign predicate | VERIFIED |
| `X_C017_certificate.json` | `δ ≤ 0.782267220134` | `verify_all.py`, `verify_XC017_readable.py` | VERIFIED |
| `X_C017_small.json` | `δ ≤ 0.782267254856`, ≤ 20-digit entries | `verify_all.py`, `verify_XC017_readable.py X_C017_small.json` | VERIFIED (X-C019) |

None of these is a Kepler proof, and none is a new best bound: `0.782267 > 0.740480`, and
`0.782267 > 0.779966216777` (K33b). Their value is that `X_C015`–`X_C017`/`X_C017_small` need
**no** sign predicate — three rational `LDLᵀ` tests and one polynomial identity (see §3 of
`REPORT_X040.md`).

## Verifiers and their controls

| script | what it decides | control |
| --- | --- | --- |
| `verify_all.py` | every X certificate, in exact arithmetic | run it; exit 0 = ALL PASS |
| `verify_XC017_readable.py <cert>` | one certificate, printed step by step, sign-free | `Reviews/negative_control_readable.py` (3 tampered copies must be rejected) |
| `exact_sign.py` | sign of a rational polynomial on a half-line / interval | 21 witness-anchored controls, run by `verify_all.py` |
| `Reviews/x_family_check.py <checker>` | a *checker*, against three adversarial families | it fails on `5619c1d` (8/308 queries), so it is not vacuous |

## Reviews and audits

| file | subject | verdict |
| --- | --- | --- |
| `REVIEW_0308.md` | Main's checker lineage, C's numbers, the `η < 0` witness (§17) | mixed; §17 was the finding |
| `REVIEW_0353.md` | the first `CUT_FLOW_THEOREM.md` and C's `cut_flow.py` | 4 defects in each |
| `REPORT_X040.md` | **this block**: the repaired theorem, the size reduction, the verifier | see §5 for the claim list |
| `Reviews/audit_cutflow_repair.py` | the repaired theorem, 6 checks + 115 LP + 196 exact-FM instances | ALL PASS |
| `Reviews/repro_c_cutflow_defects.py` | C's five live `cut_flow.py` defects (+1 latent, +1 cosmetic), portably | 13/13 checks |
| `Reviews/verify_eta_closed.py` | whether Main's `5caa1c9` closed the `η` witness | closed, control unchanged |
| `Reviews/g8_checker_independence.py` | `PROOF_GAPS` G8: do the two exact checkers share code, and do they agree | no shared code; 52/52 agreement on the `q` side |
| `REVIEW_0523.md` | audit of Main's `GEOMETRIC_LEMMA_0438.md` / `EXPOSITION_0438.md` at `a6f3935`: C106–C108, Theorem B/C/D | six findings, `X-C037`…`X-C049` |
| `Reviews/witness_0438_audit.py` | exact witnesses W1–W3 for the 0438 audit (C_R, (M), the star) | runs clean |
| `Reviews/two_dodecahedra_indep.py` | Theorem D step 4 recomputed, and the E/Main discrepancy resolved | `sup_t m(t) = 1.125554844510 < 2` |
| `Reviews/p_le_eta_independent.py` | the bounded-interval `p ≤ η` predicate by Vincent–Descartes, no Sturm | 92 cases, 0 mismatches; found the `nsimplify` bug (`X-C045`) |
| `Reviews/crack_cell_indep.py` | crack-packing cell volumes by half-space clipping | `√32 + 2ε` exactly; the `6.985` confirmed |
| `Reviews/near_contact_band_indep.py` | the two-dodecahedra threshold, against `C116`'s `6/√5` | threshold `3.4555003`, attainable; `C116` 28.8% short |

## Known-wrong things in the tree (kept deliberately, do not quote)

- `REVIEW_0353.md` §3 row **W6** — restated correctly in `REPORT_X040.md` §1.1 (`t* = 2`).
- `Main/CUT_FLOW_THEOREM.md` §6 retains the first version's rejected text; that is intentional.
- `Reviews/K33/audit_K33_signs.py` is superseded.
- `Main/NEXT_PACKAGE.md` item 1 asks for `V = 5.40`, already implied by Hales–McLaughlin; see
  `REPORT_X040.md` §7.

## Reproduce everything in this block

```sh
python3 verify_all.py                                   # ALL PASS
python3 Reviews/audit_cutflow_repair.py                 # ALL PASS
python3 Reviews/repro_c_cutflow_defects.py              # 13/13 (5 live incl. D8 --fixture, 1 latent, 1 cosmetic)
python3 Reviews/verify_eta_closed.py                    # witness closed
python3 Reviews/negative_control_readable.py            # verifier has teeth
python3 x_c017_shrink.py                                # rewrites X_C017_small.json byte-identically
python3 verify_XC017_readable.py X_C017_small.json      # VALID CE CERTIFICATE
```
