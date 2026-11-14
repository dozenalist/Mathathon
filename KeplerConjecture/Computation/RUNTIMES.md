# Measured runtimes on the SAIR VM

Why this page: the reviewer measured `sos_qside_polish.py --degree 7 --iters 4000` at **27 s here and
more than 90 s** on their host, a factor of about 3.3. Any estimate below should be multiplied by
that factor before being used to budget a run somewhere else. Measured 2026-11-14, one process at a
time, this repo's `python3`, warm cache.

## Verification only — the fast path

| script | here | what it proves |
| --- | --- | --- |
| `k15radicals.py` | 0.05 s | the two exact radical enclosures (`V_dod`, icosahedral edge) |
| `highdensity_cut.py` | 0.05 s | HD1–HD3, `R_Φ` table |
| `transfer_necessity.py` | 0.08 s | THEOREM A, LEMMA S/B, the two corollaries |
| `compact_verify.py` | 0.22 s | the K33b certificate by Bernstein + reversed polynomial |
| `tests_0138.py` | 0.30 s | every review-0138 claim |
| `tests_cut_flow.py` | 0.84 s | S1–S15, including the LP-duality and external-fixture checks |
| `verify_certificate.py` | 1.01 s | K33b through `exactcert` **and** the SymPy oracle |
| `cut_flow.py` | 1.27 s | the fixture evaluation, `out/cut_flow.json` |
| `period_convention.py` | 5.16 s | the convention, the congruence group, the Sobol and half-space volumes |
| `exactcert_tests.py` | 13.24 s | the checker's own regression suite, incl. the K = 9…21 rejections |
| `audit_cut_flow_api.py` | 0.3 s | 69 adversarial checks of the cut/flow API (X-C034/D8) |

**Whole verification set: about 22 s here, so roughly 75 s on a host 3.3× slower.** That is the
command set to run before quoting anything.

## Searches and constructions — the slow path

| script | here | note |
| --- | --- | --- |
| `sos_both_sides_quintic2.py` | 197 s | one linear system, no search; reproduces `Δ ≤ 1.33982381256` |
| `sos_qside_polish.py --degree 7 --iters 4000` | 27 s | measured earlier; **> 90 s** on the reviewer's host |
| `cut_isoperimetry.py` | 0.09 s | the FCC profile |
| `cut_fixture_close.py` | 0.22 s | the jamming negative |
| `cut_fixture_frank_kasper.py` | 0.10 s | the A15 negative |
| `fixture_nonuniform.py` | 29 s | exact Voronoi volumes, the nonuniform fixture, the near-contact scan and the engine cross-check |

## One-line reproduction of everything quoted in `REVIEW_0353.md`

```bash
cd KeplerConjecture/Computation
python3 verify_certificate.py out/verified_certificate_K33b.json && \
python3 compact_verify.py && python3 compact_verify.py --self-test && \
python3 exactcert_tests.py && python3 tests_0138.py && python3 tests_cut_flow.py && \
python3 period_convention.py && python3 highdensity_cut.py && python3 k15radicals.py
```
