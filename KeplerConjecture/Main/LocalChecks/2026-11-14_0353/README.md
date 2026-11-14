# Local checks at the 03:53 Pacific review

`run_checks.py PRIVATE_PARENT` freezes the four stated Git revisions, then runs
five jobs using the previously recorded Windows affinity/resource monitor.
`run_followup_checks.py PRIVATE_PARENT` freezes the three later revisions for
the negative-eta witness, repaired regression suite and C5 candidate. Python,
dependency versions, source hashes, one-CPU affinity and 1 GiB monitored cap are
recorded in the environment JSONs; wall limits are in the two jobs JSONs. Supply
the existing private Python dependency directory through PYTHONPATH.

`independent_checks.py SNAPSHOT` implements its own exact PSD and Fourier checks,
with a rational Machin enclosure for the density comparison. Its first run
completed the arithmetic but failed JSON serialization of a SymPy Boolean. The
fix converts that output flag to a Python bool; the complete retry took under
five seconds. Both logs are preserved. `independent_results.json` is the retry's
output. A false `dodeca_enclosure` flag reports a worker-input defect, rather than
a failed supervisor test.

| Job | Result |
| --- | --- |
| Independent X-C015/016/017 reconstruction | Exact identities and PSD pass; X-C017 < 0.782267220134 |
| Independent C fixture probes | False dodecahedron interval, premature ring edges, broken FCC constructor; sparse fixture unsaturated |
| C cut test suite | Pass; does not cover those geometric defects |
| C fixture/external-input command | Exit 0; certificate claims remain suspended |
| C quintic2 solve | 45-second cap; no completed solve |
| E icosahedral constants | Exit 0; arithmetic controls only |
| X negative-eta witness | False acceptance independently reproduced against frozen old checker |
| Main repaired regression suite | 37 cases pass; generic soundness still pending |
| E C5 candidate | Displayed numeric geometry reproduced; 60-second cap during anneal |

No jobs remain running. No Lean build was requested or repeated. Search caps
prove neither impossibility nor an optimum. Floating geometry, finite scans and
an incomplete anneal do not provide rigorous lower cell-volume certificates.
