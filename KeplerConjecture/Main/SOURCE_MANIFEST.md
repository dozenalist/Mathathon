# Source manifest — block K15-HOUR-20261114-M

Read and integrated 2026-11-14, block start `09:14:25Z`. Every hash is a full
Git object name or a file SHA-256.

## Revisions read

| Source | Revision | What was taken |
| --- | --- | --- |
| supervisor `kepler15/setup-01a1d8c0` | `83cb448` | task framing, review text |
| Computation `kepler15/comp-01a1d8c0` | `90cc632` | `exactcert.py`, `verify_certificate.py`, `out/verified_certificate_K33b.json`, `shell_bench.py`, `out/sb_rho2.09.json` |
| Experimental `kepler15/experimental/run-01` | `8aca235` | `TAMMES13_ENCLOSURE.md`, `scripts/tammes13_enclosure.py`, `evidence/tammes13_enclosure.txt` (not integrated as a proof; see G2) |
| Counterexamples `kepler15/counterexamples/run-01` | `237cc3b` | `ce_exact_gauss.py` (convention X), `REPORT_width_and_E030.md` |
| Main `kepler15/main` (this branch) | parent `6b903a3`, then `3903154` | ledger being extended |

## Artifact hashes used in this block

| Artifact | SHA-256 |
| --- | --- |
| Computation `out/verified_certificate_K33b.json` | `525d1d556e23d2a6be97fa175abb4c462af4b15d0ccb55ab02784a67f078546a` |
| Main `Computation/shell_check.py` (after this block) | `ca976ce4fd8710e6e6d786443dbb6da6e34cf1091f9e1b16cc337d078cb509e1` |
| Main `Computation/verify_comp_cert.py` | `6a179b349005fbe34f2238270cd63d7c73180c16ad34a4428fa3498a14abdaf8` |

## Verifications actually executed by Main this block

| Command | Result | Time |
| --- | --- | --- |
| `python3 verify_certificate.py out/cert.json` (Computation's own two checkers, extracted from `90cc632`) | `ACCEPT`, `Δ ≤ 0.779966216777`, ratio matches | ≈1 s |
| `python3 KeplerConjecture/Computation/shell_check.py --self-test` | ALL PASS | ≈1 s |
| `python3 KeplerConjecture/Computation/interface_xcheck.py --degree 3` | `p(t) = P(t/2)`, `q(t) = Q(t/2)` identically; both checkers reject the same vector | <1 s |
| `python3 KeplerConjecture/Computation/verify_comp_cert.py out/cert.json` | `ACCEPT`, same ratio, `Δ ∈ (0.779966216777, 0.779966216777)` | ≈4 s |

No Lean build and no heavy solve was run on the VM. The only floating-point
computation in the block was a five-second LP diagnostic, which failed and is
recorded (K15-C022).
