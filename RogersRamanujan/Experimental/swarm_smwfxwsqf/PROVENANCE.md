# Provenance: Ultramath swarm `smwfxwsqf` (2026-11-14)

These directories are **verbatim copies** of the four member working
directories, preserved because `.ultramath/` is git-ignored by the swarm tool's
own convention while the reports are cited as evidence in
`../../Main/CLAIMS.md` and `../../Counterexamples/REGISTRY.md`.

Original location: `.ultramath/smwfxwsqf/m{1,2,3,4}/` in the same checkout.
Model: `deepseek/deepseek-v4.1-flash`, reasoning effort `max`, 8 targeted
directions of which 4 were taken; all four reports were judged and **accepted**
by Main. Nothing here is edited; Main's verification of each report is in
`../../Main/CLAIMS.md` (the row that names the member) and the corrections Main
recorded are in `../../Main/DECISIONS.md`.

| member | direction | what it delivered | Main's verdict |
| --- | --- | --- | --- |
| m1 | exact enumeration | 4 counters for `A_n`, `D_n`; 31-row table; intact sets for `n<=30` | accepted; table identical to Main's six-method baseline |
| m2 | largest-part obstruction | forced-object table with minimal witnesses; largest-part and length distribution diffs | accepted; reproduced by Main and promoted to an all-`n` proof (RR-C004) |
| m3 | BZ82 `psi` | all-`n` written proof that `psi` is an involution, plus the derived domain claim | accepted; refereed line by line, promoted to PROVED (RR-C008) |
| m4 | structural candidate | level-splitting reformulation of the problem; three natural level rules refuted | accepted as a bounded deliverable, not a solution |

Coordinate clash worth noting: m2 registered "refinement obstruction" and m4
registered "structural candidate" under board ids `d4` and `d3`, i.e. the board
ids do not match the D1-D4 numbering of the assignment. Identify a report by
its member name and file paths, not by its board id.
