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

## Block K15-REVIEW-0138-M — additions

Receipt `2026-11-14T09:42:58Z`. Revisions read at receipt:

| Source | Full hash |
| --- | --- |
| supervisor `kepler15/setup-01a1d8c0` | `3c8ea4b0dd5d2749bb3c2760afb59f3b642167a6` |
| Computation `kepler15/comp-01a1d8c0` | `5c10267703d89ed285a01112aeba717018fb67bc` |
| Experimental `kepler15/experimental/run-01` | `4ea4e8b96eea76b9f045325f9d18229a2157aeb5` |
| Counterexamples `kepler15/counterexamples/run-01` | `e3a63a184a5cc94ce63512f1f3285f0622d089df` |
| Main `kepler15/main` at receipt | `6626714125c35292d78943cd0fe8d18ec0051b38` |

New worker artifacts read but **not** imported as claims (attribution preserved,
status unchanged): C `shell_propose.py` / `shell_sos.py` and their JSON outputs;
E `interval_selfaudit.py`, `outer_cell_angular_bound.py`, revised
`tammes13_enclosure.py`; X `Reviews/audit_shell_check.py`,
`Reviews/shell_check_main.py` (an independent copy of Main's checker with a
quadrature audit of `fourier_map`), `Reviews/K33/witness_bisect.py`.

Quality-control note: a previous run of `Computation/checker_adversarial.py`
against `exactcert` depended on files extracted to a scratch directory that is
not part of the repository. The runnable command therefore is:

```
git show 5c10267703d89ed285a01112aeba717018fb67bc:KeplerConjecture/Computation/exactcert.py > /tmp/exactcert.py
python3 KeplerConjecture/Computation/checker_adversarial.py --against-exactcert /tmp
```

with the caveat that `exactcert.py` imports nothing else. `Computation/transfer_check.py`
needs only numpy.

## Additional runs this block (commands and outcomes)

| Command | Outcome |
| --- | --- |
| `python3 Computation/transfer_check.py --R 2 --rmax 4` | bound of `K15-C035` holds at `r = 1..6` on fcc (1099 centres); sums `O(10)` vs bounds `O(10³)` |
| `python3 Computation/cluster_fixture.py` | centre cell `5.550291` in every completion; nested sums `+157.87, +63.71, +17.91` decreasing, all upper bounds |
| `python3 Reviews/audit_shell_check.py` (X's copy, from `e3a63a1`) | quadrature confirms `fourier_map` to `4.9e−15`; script then crashes at section 3 (SymPy `Float.imag`) |
| `git show 5c10267:…/exactcert.py`-based cross-run (previous block) | 10/10 agreement, unchanged |

## Sign-predicate repair (K15-C049)

| What | Where |
| --- | --- |
| Reproducer of the three false accepts | supervisor branch, `Main/LocalChecks/2026-11-14_0138/reproduce_sign_defects.py` |
| Repaired predicates | `Computation/shell_check.py` (`_count_roots_open`, `_test_points`, and the three predicates) |
| Permanent regressions | `Computation/checker_adversarial.py` (19 cases, incl. the three reported) |
| Re-verified | `--self-test` ALL PASS; adversarial 19/19; `verify_comp_cert.py` on K33b → ACCEPT, unchanged value; `shell_fixture.py --m 2 --rho 2` → unchanged `R` |

## Immutable revisions for X's audit (end of block `K15-REVIEW-0138-M`)

The checker and its three supports, with file hashes, so that an audit can pin
exactly what it examined:

| File | SHA-256 |
| --- | --- |
| `Computation/shell_check.py` (the repaired predicates) | see below |
| `Computation/checker_adversarial.py` (24 cases) | see below |
| `Computation/predicate_fuzz.py` (random + 2 structured families) | see below |
| `Computation/predicate_crosscheck.py` (`function_range`) | see below |
| `Computation/run_all_checks.py` (one command) | see below |
| `Computation/constants_check.py` (26 constants) | see below |

The authoritative values are the hashes printed by
`sha256sum KeplerConjecture/Computation/*.py` at the pushed tip of
`kepler15/main`; they are recorded in the block's final commit message rather than
in this file, so that this file does not have to be edited whenever the code moves.
Any audit should quote the `kepler15/main` commit it used.
