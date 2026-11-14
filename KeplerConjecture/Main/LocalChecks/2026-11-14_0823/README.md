# Local checks — 08:23 Pacific

Pinned sources and environment: `environment.json`. Four jobs finished with one
CPU, one BLAS/OpenMP thread and a monitored 1 GiB memory ceiling. Timings and
per-job caps are in `state.json`. Commands from the pinned KeplerConjecture root:

```
python Experimental/scripts/cell_certificate.py
python Main/LocalChecks/2026-11-14_0823/certificate_probe.py
python Computation/tests_exact_volume.py
python Computation/verify_certificate_independent.py
```

E's controls pass in 6.750 seconds (30-second cap), including duplicate,
proportional, redundant, edge-only and vertex-only planes. C's 25 tests pass in
0.516 seconds (90-second cap), and the separate signed-tetrahedron calculation
reproduces the stored dense-shell central volume in 0.515 seconds (30-second cap).
These are checked finite cases and consistency evidence, not generic soundness.

The supervisor's exact probe completes in 0.562 seconds (30-second cap) and
exposes two false accepts by C's standalone `check_certificate` at fbb124e:

1. Start from the valid six-plane cube certificate of volume 8. Duplicate the
   complete facet list and change the asserted volume to 16. It accepts 16.
2. Add x<=1/2 to the full `planes` list, leaving `candidate_planes` unchanged.
   It still accepts 8, although the full intersection is a box of volume 6.

Neither probe refutes the stored dense-shell number. They refute the claim that
this standalone verifier needs no trust in the producer: it does not enforce
facet uniqueness or recheck every original plane. The generic checker remains
pending repair and independent mathematical review. Logs retain the exact results.

Main's M-CERT-002 is NEEDS_IMPLEMENTATION / NEEDS_REVISION, not a running job:
the requested `l1_remainder.py` is absent at 89a9c5494a6ead7424caeffc4b5053ae800512b9,
the command uses stale constants/non-quotiented expressions, and strict positive
minimum over a domain containing the equality point is impossible. Main was
assigned a corrected executable handoff. No new Lean target was submitted.
