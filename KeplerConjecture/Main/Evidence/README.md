# Evidence exported from the recovered swarms

Review objection 10: arguments kept only in `.ultramath/` on the VM are not
reproducible from the pushed checkpoint. These files are byte-identical copies
of the swarm artifacts, taken 2026-11-14 from `.ultramath/smwg019eu/` and
`.ultramath/smwfyzz1k/`, with hashes in `MANIFEST.txt`. They are **evidence, not
accepted proofs**: every claim built on them still needs the named independent
reviewer.

| File | Origin | Used by |
| --- | --- | --- |
| `m2-proof.md` | `smwg019eu/m2/proof.md` | K15-C002, C003, C009 |
| `m2-verify.py`, `m2-verify-output.txt` | `smwg019eu/m2/` | K15-C002/C003 constants |
| `m1-certificate.json` | `smwg019eu/m1/certificate.json` | K15-C012 and the two raw signs quoted in K15-C005 |
| `m1-verify.py` | `smwg019eu/m1/verify.py` | re-run: 30/30 checks (constants and a finite family of kernels only — **not** an obstruction) |
| `m3-zero-density-obstruction.md` | `smwfyzz1k/m3/` | K15-C010b (its formula (B) carries the norm term Main dropped) |

`m1-verify.py` reports 30/30 and `m2-verify.py` 41/41 when re-run on the VM at
export time. Neither proves a universal statement.
