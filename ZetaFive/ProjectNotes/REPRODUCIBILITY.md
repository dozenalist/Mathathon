# Reproduce and maintain the project notes

The artifact folders preserve original source layouts where scripts depend on relative imports or neighboring data. The PDFs and TeX files are unchanged copies of the reports delivered in the source chats. The [manifest](MANIFEST.json) records every copied artifact's path, size, SHA-256, and original path relative to the Zeta 5 workspace. Newly written archive notes and artifact indexes are identified separately.

## Artifact layout

| Folder | Preserved material |
| --- | --- |
| [ProofOverview](artifacts/ProofOverview/) | The reviewed whole-argument PDF, TeX, and original README. |
| [LaiArithmetic](artifacts/LaiArithmetic/) | Exact rational check of the eight printed comparison rows and 5,738 identity samples, plus recorded output. |
| [ParallelSections](artifacts/ParallelSections/) | The Sections 1–7 PDF, TeX, and original README. |
| [UnifiedFramework](artifacts/UnifiedFramework/) | Revised framework PDF and TeX, finite checks and results, derivations, correctness audits, and provenance reviews. |
| [Extensions](artifacts/Extensions/) | ζ(7) and ζ(9) reports, exact code and data, optional numerical probes, complete ζ(9) TeX parts, source ledgers, and mathematical handoffs. |

The extension [README](artifacts/Extensions/README.md) maps legacy ZIP paths to retained paths and identifies the exact source manuscript. Old README files and ledgers retain their original bundle descriptions; ZIPs, manuscript copies, temporary render files, and tool caches are not duplicated in this archive.

## Mathematical checks

These commands require Python 3 with its standard library unless noted. Run them from the indicated working directory. Some regenerate their adjacent JSON output; run in a working copy when preserving an exact historical snapshot.

From `ZetaFive/ProjectNotes/artifacts/LaiArithmetic`:

```sh
python check_arithmetic.py
```

From `ZetaFive/ProjectNotes/artifacts/UnifiedFramework`:

```sh
python framework_checks.py
```

From `ZetaFive/ProjectNotes/artifacts/Extensions`, in this order:

```sh
python experiments/exact_checks.py
python arithmetic_costs.py
python arithmetic_exact_inner.py
python experiments/single_point_certificate.py
python experiments/main_measure_certificate.py
node zeta9_draft/checks/section5_exact.mjs
```

The Node.js check has no package dependencies. The [extension README](artifacts/Extensions/README.md#reproduce-the-mathematical-checks) also gives the exact ninth-order determinant example. The optional `arithmetic_variant.py` and `experiments/energy_probe.py` require NumPy; their numerical probes are separate from the exact interval certificates. The existing repository calculation remains available as `node ZetaFive/Computation/exponent_catalog.mjs` from the repository root.

The source checks mix exact algebra, exact rational interval arithmetic, finite examples, and numerical sanity checks. Their passing results do not prove the imported uniform estimates or the complete irrationality claims. See the [verification record](VALIDATION.json) for commands actually rerun during this consolidation and the corresponding scope.

## Rebuild the reports

Use a standard LaTeX distribution or Tectonic for the four TeX-based reports. Each artifact folder has its own README; invoke its TeX entry point from that folder. The ζ(9) entry point includes all its fragments under `parts/`. No shell escape or external images are needed for that draft.

The ζ(7) report uses `build_report.py`, ReportLab, and the Windows Cambria fonts referenced in that script. Those are PDF-authoring dependencies only. The archived mathematical checks do not require TeX, ReportLab, the original manuscript PDF, or network access.

This consolidation did not alter or retypeset the reports. Their originating chats recorded visual inspection; the current import verifies file identity and retains both reading and editable copies.

## Check file integrity

From `ZetaFive/ProjectNotes`, this standard-library Python snippet checks all manifest entries:

```python
import hashlib, json
from pathlib import Path
manifest = json.loads(Path('MANIFEST.json').read_text(encoding='utf-8'))
for entry in manifest['files']:
    data = Path(entry['path']).read_bytes()
    assert len(data) == entry['bytes'], entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
print(f"Verified {len(manifest['files'])} files")
```

The manifest excludes itself to avoid a circular hash. When deliberately updating a copied artifact, retain its source version and verification scope, update the relevant note, and regenerate its manifest entry. A newer build result should not silently replace a historical source snapshot or turn a conditional mathematical statement into an accepted theorem.
