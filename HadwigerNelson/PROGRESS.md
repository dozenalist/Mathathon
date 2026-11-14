# Progress — 14 November 2026

This entry imports the existing Hadwiger–Nelson research into the shared repository.
It reports the status supported by the archived local checks and reviews. It does
not treat every downloaded worker report as an accepted result.

| Result | Status and evidence | Scope / outstanding work |
| --- | --- | --- |
| Closed 60-degree cone obstruction (CC60), including the equality case | `LEAN_VERIFIED`: [validation manifest](Main/ResearchSnapshot/local/outputs/cone/VALIDATION.json), [axiom audit](Main/ResearchSnapshot/local/outputs/cone/cone-audit-v3.log), and three source modules | Under the actual same-centre approaching-continuum and support-exclusion hypotheses, at least three labels remain. The concrete six-colour consumer also passed. The printed axioms are `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`. This is a local obstruction, not a plane-colouring solution. |
| Common-encoding refactor | `LEAN_VERIFIED`: [R4 validation](Main/ResearchSnapshot/local/outputs/ENCODING-REFACTOR-VALIDATION.txt), [final sources](Main/ResearchSnapshot/local/outputs/encoding-refactor/), and [compiler/fidelity records](Main/ResearchSnapshot/local/work/lean-queue/encoding-r4/) | Net reduction of 126 lines; 82-module affected closure, nine root axiom checks, statement/fresh-context checks, and 133 binders across six declarations. This simplifies the supplied proof; it is not a new bound. |
| Fixed and moving three-centre replacements | `LEAN_VERIFIED`: [sources and logs](Main/ResearchSnapshot/local/outputs/three-centre/) | Exact types/binder flags and transitive forbidden-dependency gates passed. Full consumer integration and deletion of the old branch remain pending. Keep manuscript Lemma 6.7 (`five_support_step_ban`). |
| Joint-pair support theorem | `LEAN_VERIFIED`: [source and validation](Main/ResearchSnapshot/local/outputs/joint-support/) | The standalone theorem passed; this does not establish a complete deletion of the original States development. |
| Translated Heule union | `TESTED_FINITE`: [exact certificate](Main/ResearchSnapshot/local/outputs/HEULE-UNION-CERTIFICATE.json), [independent verifier](Main/ResearchSnapshot/local/outputs/Verify-HeuleUnion.mjs), [validation](Main/ResearchSnapshot/local/outputs/HEULE-UNION-VALIDATION.txt) | 1,048 vertices, 5,487 edges, 58 overlapping vertices, 184 new connecting edges. All 548,628 unordered pairs were checked with exact arithmetic and a proper five-colouring verified. The verifier does not rerun a four-colour UNSAT proof for the embedded Heule graph. |
| No forced-equal pairs in the two studied Heule graphs | `TESTED_FINITE`: [553-vertex certificate](Main/ResearchSnapshot/local/outputs/HEULE553-NO-FORCING-CERTIFICATE.json), [1,048-vertex certificate](Main/ResearchSnapshot/local/outputs/HEULE-UNION-NO-FORCING.json) | Each graph has 34 proper five-colourings giving every vertex a distinct colour signature. Every distinct pair is separated in at least one witness. This closes these specific forcing-pair searches. |
| Generic sharpness above 60 degrees | `PROVED` at paper-review level: [construction and novelty audit](Main/ResearchSnapshot/scale-up/ULTRA-CONE-NOVELTY-AUDIT.txt), [independent referee](Main/ResearchSnapshot/scale-up/ULTRA-SHARPNESS-REFEREE.txt) | An accepted 20-colour construction prevents widening CC60 for arbitrary finite palettes. Six-colour sharpness and novelty priority are not established. |
| Discrete direction filtering | `TESTED_FINITE`: [independent audit and certificates](Main/ResearchSnapshot/local/work/checkin-artifacts/20261114T172056Z/) | The corrected counts are 7,776 grid vectors, 1,420 after aligned constraints, 174 after orbit constraints, and six after conditional CC60 filtering. The old count of 95 was a reconstruction bug. Grid exhaustion is not a classification of arbitrary directions. |
| Continuous cone/list-field investigations | Paper results and candidates: [continuous classification](Main/ResearchSnapshot/local/outputs/ASTRA-CONTINUOUS-SIX-A4.txt), [list-field report](Main/ResearchSnapshot/local/outputs/ASTRA-LIST-FIELD-A4.txt) | The original status report distinguishes completed paper arguments from outstanding independent reviews. No full-disk extension or global six-colouring is inferred. |

The original [progress log](Main/ResearchSnapshot/local/outputs/PROGRESS-LOG.txt),
[consolidated findings](Main/ResearchSnapshot/local/outputs/CONSOLIDATED-FINDINGS.txt),
and [research status](Main/ResearchSnapshot/local/outputs/RESEARCH-STATUS.txt)
retain the sequence of corrections and handoffs. Historical policy, quota, and
deadline statements in those reports describe their original times.

## Import validation

The repository import checks exact file hashes, the stated cone and R4 source
hashes, certificate structure, and graph-colouring witnesses. Results and the
reproduction command are recorded in
[Main/IMPORT-VALIDATION.json](Main/IMPORT-VALIDATION.json). Existing Lean compiler
logs are preserved as prior verification evidence; the import does not claim a
fresh complete Lean rebuild or integration into the repository's 4.35.0 target.
