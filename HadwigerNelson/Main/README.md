# Research archive and provenance

[ResearchSnapshot](ResearchSnapshot/) preserves the local and Open Math OS
Hadwiger–Nelson research collected on 14 November 2026. The snapshot is intentionally
separate from live coordinator state and from the repository's main Lean target.

| Directory | Contents |
| --- | --- |
| `local/outputs` | Research reports, reviewed proof sources, final certificates, compiler logs, and historical helper scripts. |
| `local/work` | Source packets, exact audits, failed and corrected Lean revisions, and completed Claude reports. |
| `remote` | Selected files read from the existing Hadwiger–Nelson Open Math OS project, including supervisor work and mathematical worker artifacts. |
| `history` | Distinct versions of downloaded mathematical artifacts recovered from saved local checkpoints. |
| `scale-up` | The two independent sharpness reports and the existing scale-up receipt/helper sources. |

[MANIFEST.json](ResearchSnapshot/MANIFEST.json) records every included file's path,
size, SHA-256, and source provenance. For remote files it records the original
project-relative path and download time. Hidden scratch/worker directories are
mapped to ordinary archive directory names so Git ignore rules do not hide the
research (`.scratch` becomes `scratch-artifacts`, `.ultramath` becomes
`ultramath`). A case-colliding filename receives a stable suffix recorded in the
manifest. [IMPORT-SCOPE.json](ResearchSnapshot/IMPORT-SCOPE.json) records selection
rules, omitted remote files, and directory exclusions.

Credentials, authentication exports, live transport state, raw chat/model event
streams, downloaded app bundles, compiled objects, installed dependencies, and
large generated cache files are excluded. Mathematical reports, source code,
compact certificates, and relevant proof/check logs are preserved. Historical
helper scripts are source records; they are not configured to run automatically
from this checkout.

The large `heule553_k4.drat` proof trace is stored as `.drat.gz`. Its manifest
records both the compressed and original hashes and sizes; the verifier checks
lossless decompression. This packaging check does not replay the DRAT proof.

The original local workspace was
`C:\Users\jarom\Documents\Codex\2026-11-13\i`. References to its `outputs/` and
`work/` trees resolve beneath `local/` here, except for checkpoint transport data,
whose mathematical artifacts were extracted into `history/` and
`local/work/checkin-artifacts/`. Original absolute paths in reports remain
historical provenance and are not portable build commands.

The remote source is the existing Open Math OS project
`p-a4e2849861784c708dd751c46b0f4f64`. Its file inventory and downloads were read-only.
Research continued while the snapshot was collected, so it is a set of dated
file captures rather than an atomic image of a stopped research VM. New results
after those capture times require a later commit. Failed/retracted historical
claims are preserved; [PROGRESS.md](../PROGRESS.md) is the reviewed entry point.

To verify the archive and the finite graph certificates:

```sh
node HadwigerNelson/Main/verify-snapshot.mjs
```

[IMPORT-VALIDATION.json](IMPORT-VALIDATION.json) records the import run. The check
hashes the archived bytes, matches accepted Lean source hashes to their existing
validation records, reconstructs the exact translated graph, and verifies the
separating five-colouring witnesses. It performs no network operations and no
Lean builds. The existing Lean logs retain their original environment and scope.
