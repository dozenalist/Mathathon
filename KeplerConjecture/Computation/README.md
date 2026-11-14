# Computation/ — code index (Main's tools)

Everything here runs on the SAIR VM in seconds, needs only `numpy`, `scipy`,
`sympy` (plus `mpmath`), and decides its claims **exactly** unless labelled
otherwise. Nothing here is a certificate for a packing bound; the one certificate
in the project lives in Computation's own branch (`exactcert.py`, `out/…K33b.json`).

| File | What it does | Command | Time |
| --- | --- | --- | --- |
| `run_all_checks.py` | runs every check below in one go; `--cert` adds a certificate verification | `python3 run_all_checks.py [--cert X.json] [--quick]` | 4–7 s |
| `constants_check.py` | re-derives every constant the ledger quotes (26 checks) | `python3 constants_check.py` | 0.1 s |
| `shell_check.py` | the exact sign predicates and the shell-allowance checker; `--self-test` runs its built-ins | `python3 shell_check.py --self-test` | 0.2 s |
| `checker_adversarial.py` | 24 adversarial cases for the predicates; `--against-exactcert DIR` cross-runs them through Computation's engine | `python3 checker_adversarial.py [--against-exactcert DIR]` | 0.2 s |
| `predicate_crosscheck.py` | compares the predicates with SymPy's exact `function_range` | `python3 predicate_crosscheck.py` | 0.5–1.5 s |
| `predicate_fuzz.py` | differential fuzz (random + **structured perfect squares**) against sampling; flags only "predicate true, sample violates" | `python3 predicate_fuzz.py --n 300` | 2–3 s |
| `verify_comp_cert.py` | converts a Computation-format certificate to Main's basis and re-decides it | `python3 verify_comp_cert.py cert.json` | 2–4 s |
| `interface_xcheck.py` | proves `p(t) = P(t/2)` and `q(t) = Q(t/2)` for a test vector (the convention dictionary) | `python3 interface_xcheck.py --degree 3` | 0.2 s |
| `shell_fixture.py` | exact shell-allowance fixture: family `P = (T−u)S`, `S ≥ 0` by non-negative coefficients; searches, then certifies | `python3 shell_fixture.py --m 2 --rho 2 --eta 0` | 4–8 s |
| `transfer_check.py` | numerically exercises the transfer lemma's negligibility bound on fcc | `python3 transfer_check.py --R 2 --rmax 4` | 0.2 s |
| `cluster_fixture.py` | the icosahedral 13-cluster: centre cell volume and the monotonicity of completions (validated to be packings) | `python3 cluster_fixture.py` | 0.5 s |
| `ce_laguerre.py` | **historical, broken** grid LP kept as evidence for `K15-C014r`; do not use | — | 1 s |
| `barlow_cells.py` | `K15-C094`: Barlow cells — 12 contacts, cell volume `√32`, the fcc/hcp two-shape dichotomy and its tangency slack; `--sweep N` adds random stackings of period 3–10 | `python3 barlow_cells.py [--sweep 6]` | 23 s; 6 min with `--sweep 6` |
| `gap_fixture.py` | `K15-C095`: the crack packing — min separation, cross-crack distance, sampled covering radius over a range of `d` | `python3 gap_fixture.py` | 6 s |
| `rho_probe.py` | `K15-C096`: the icosahedral-scaled cell volume against `√32`, and whether a 13th point in an icosahedral hole can cut it | `python3 rho_probe.py` | 1 s |
| `twist_cover.py` | `K15-C112`: two adjacent dodecahedral centres are impossible for **all** relative twists — the "too close" set of each pair is a single arc, and the arcs cover the twist circle with zero gaps (supersedes the sampled grid) | `python3 twist_cover.py` | 0.06 s |
| `a15_pair.py` | `K15-C111`: A15 cell volumes (exact rationals `125/16`, `129/16`) and the contact-pair type; corrects E's A–B-for-B–B entry | `python3 a15_pair.py` | 0.3 s |
| `ledger_lint.py` | `K15-C110`: CLAIMS.md consistency — ids, addenda, status vocabulary, and that every fully-qualified `K15-…` reference resolves | `python3 ledger_lint.py` | 0.05 s |
| `contact_cell_exact.py` | `K15-C104`: exact contact-polytope bound `K ⊆ B(v,√2)` for both local types in `Q(√2,√3)` with interval sign decisions | `python3 contact_cell_exact.py` | 0.3 s |
| `two_dodecahedra.py` | `K15-C108` step (4): two adjacent centres cannot both be dodecahedral; max over the relative twist of the min cross-distance | `python3 two_dodecahedra.py` | 18 s |
| `bridge_boundary.py` | `K15-C106` step (i): measures the `O(R²)` boundary term of the cell-volume sum on fcc | `python3 bridge_boundary.py` | 0.5 s |
| `nearest_13th.py` | `K15-C102`: how close a 13th centre can get to the icosahedral twelve at radius `rho` (closed form for the admissible radius per direction), and whether that is inside `2·R_cell` | `python3 nearest_13th.py` | 1 s |

## Conventions

`u = π|x|²`, `f = e^{−π|x|²} Σ a_k u^k`, `f̂ = e^{−π|x|²} Σ b_k u^k` with `b = M a`
and `M` rational (`fourier_map`). Thresholds are `4·PI_LO` and `PI_LO·ρ²`, both
rational and `≤` the true ones, so there is no rounding loss. See
`Main/INTERFACE.md` for the dictionary to Computation's `t = 2π|x|²` convention.

## Warnings learnt the hard way

1. A grid-sampled sign condition is worthless (`K15-C014r`, `K15-C022`).
2. A test suite is not evidence unless it can fail; two repairs in one block were
   each caught by an outside reproduction rather than by their own tests
   (`K15-C049`, `K15-C058`).
3. Test points for `p ≤ 0` must come from the roots of `p` itself; any argument
   that inspects only the odd part is unsound for perfect squares.
