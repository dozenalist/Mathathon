# Local checks — 07:38 Pacific

Exact executed sources and environment are in `environment.json`; timing and
limits are in `state.json`. Both jobs finished. One CPU, one BLAS/OpenMP thread,
monitored 1 GiB memory ceiling; 90-second controls and 30-second probe caps.

From KeplerConjecture at Experimental source 6ae7dbf834295aa688076d94caa091a77a127ce2:

```
python Experimental/scripts/cell_certificate.py
python Main/LocalChecks/2026-11-14_0738/gate_probe.py
```

The first command passed all supplied controls in 24.406 seconds. The second
ran in 0.313 seconds and independently checked the named positive-axis rejection,
cube volume 8 and a positive rational radius lower bound with 3*c*c <= 1.
It also demonstrated an uncorrected input-contract failure: repeating the e1
half-space changes the cube's returned volume from 8 to 28/3. This is an exact
counterexample to duplicate-constraint invariance, not a refutation of the
specific twelve-distinct-normal C5 fixture. General certification remains open.

No new Lean target was submitted. `X-ORIENT-001` was withdrawn by Main in favor
of an analytic argument, which is independently assigned for review. E's
`premise_audit.py 600` request is deferred: its first start alone takes 600 seconds,
contradicting the proposed 120-second per-start cap, and a primary twelve-face
volume theorem supplies its intended premise. The agent must withdraw or replace
the now potentially redundant request. No 100-box rerun was launched while the
general verifier contract and geometric proof obligations remain open.
