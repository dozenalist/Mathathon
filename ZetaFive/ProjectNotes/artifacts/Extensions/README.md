# Higher odd zeta extension artifacts

This collection preserves the useful outputs of **Explore zeta(5) proof for zeta(7)**, including its later zeta(9) followups, from 14 November 2026. These are research notes and checked finite calculations, with the mathematical qualifications stated in the reports. They are not a proof that zeta(7) or zeta(9) is irrational.

Start with [the zeta(7) report](output/zeta7_argument_audit.pdf) and [the zeta(9) formal draft](output/zeta9_formal_analogue.pdf). The original `README.txt` files describe their original bundle layout. This Git collection omits duplicated third-party manuscript files, ZIP bundles, tool downloads, caches, render previews and build logs.

## Reproduce the mathematical checks

Run these commands from this directory, using standard-library Python:

```text
python experiments/exact_checks.py
python arithmetic_costs.py
python arithmetic_exact_inner.py
python experiments/single_point_certificate.py
python experiments/main_measure_certificate.py
```

The third command regenerates `arithmetic_variant_results.json`, required by the fourth. Keep these files in their current relative layout. The core checks do not require the source PDF, NumPy, ReportLab or TeX.

`experiments/zeta9_local_check.json` records the separate exact ninth-order example. To recompute its two valuations, run the following from this directory:

```python
import sys
sys.path.insert(0, 'experiments')
from exact_checks import matrix_affine, det, valuation, determinant_valuation_modular
a = [[entry[0] for entry in row] for row in matrix_affine(9, 40, 3)]
print(valuation(det(a), 29))  # -104
print(determinant_valuation_modular(a, 29))
```

The ninth-order budget uses dependency-free Node.js:

```text
node zeta9_draft/checks/section5_exact.mjs
```

Compare its JSON output with `zeta9_draft/checks/section5_exact_results.json`. This verifies exact rational arithmetic for the proposed certificate; it does not verify its formal inner analytic transfer. The NumPy scripts `arithmetic_variant.py` and `experiments/energy_probe.py` are optional explorations and do not establish the interval-certificate conclusions.

## Edit and rebuild the reports

The seventh-order PDF source is `build_report.py`, which requires ReportLab and the Windows Cambria fonts referenced in the script. The mathematical check scripts have no such dependency.

The ninth-order TeX entry point is `zeta9_draft/zeta9_formal_analogue.tex`, with all included fragments under `zeta9_draft/parts/`. Run `tectonic --untrusted zeta9_formal_analogue.tex` or two `pdflatex` passes from that directory. Copy the resulting PDF to `output/` if updating the browsable artifact. The main assembled TeX is authoritative where historical section handoffs contain unreconciled draft estimates; notably the arithmetic remainder is `o_M(K^2)` at fixed cutoff, not a proven `O_M(K log K)` bound.

The `editorial_contract.txt`, `coordination_log.txt`, and section handoffs preserve the original draft's mathematical scope and interfaces. They are historical authoring records, not instructions to future agents. The earlier `zeta9_parity_notes.txt` predates the full formal draft; its final statement about the missing budget was superseded by the later conditional budget, not by an irrationality proof.

## Obtain the exact source manuscript

Both reports refer to Aabir Fauzan's *ζ(5) is irrational*, 17 September 2026, Zenodo v1, 32 pages. Download the [PDF from the versioned Zenodo record](https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf?download=1), or use a shared Mathathon source copy with the matching hash:

```text
SHA-256 a42c05ccc46b9a7c36428913453c4617202c59109713ba20f464ab9ec640d0da
MD5     30dafe4adbb13a79f202e94a046c8c8d
```

The legacy path `sources/Fauzan_2026_zeta5.pdf` is relative to this collection's root. `sources/Fauzan_2026_zeta5.txt` was a text extraction of that PDF, with page markers. Neither is needed to run the mathematical checks. `sources/source_ledger.json` preserves the complete source trail; `zeta9_draft/source_ledger.json` preserves the later draft's scope.

The latter ledger's original ZIP aliases map to this collection as follows:

| Original bundle reference | Retained location |
|---|---|
| `sources/original_exploration_source_ledger.json` | `sources/source_ledger.json` |
| `prior_checks/exact_checks.py` | `experiments/exact_checks.py` |
| `prior_checks/zeta9_local_check.json` | `experiments/zeta9_local_check.json` |
| `prior_checks/zeta9_parity_notes.txt` | `zeta9_parity_notes.txt` |
| `checks/section5_exact.mjs` and results | `zeta9_draft/checks/` |

The ledgers' original render/validation statements describe work done in the source chat. They are provenance statements, not new verification performed during consolidation.
