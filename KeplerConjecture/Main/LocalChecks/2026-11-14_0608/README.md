# Local evidence at the 06:08 Pacific review

Pinned sources, hashes, Python/package versions and resource limits are in
`environment.json`. All jobs finished. No Lean build was requested.

- `independent_probes.py/json`: the repaired C checker rejects the original
  isolated-positive and edgeless witnesses; the all-negative threshold is zero.
  The same probe supplies exact witnesses against E's generic norm estimate
  and its claimed boundedness/radius validation. See the technical review for
  the important distinction between a failed validation and a valid radius premise.
- `checks/cut_api_audit.log`: C's 69-case audit passes in 3.031 seconds at cde39fa.
  The integrated bf7998c has the identical cut_flow.py blob. Subsequent audit
  changes only make temporary-file paths independent of the working directory.
  Finite tests do not prove universal soundness.
- `checks/volume_controls.log`: E's named controls pass in 24.610 seconds.
  They do not exercise the newly found defects.
- `one_box.json`: the requested box theta=[110,110.1], phi=[35,35.1] degrees
  reproduces output [5.874627182294318,5.927479311634412], 20 inner/outer vertices.
  Exact rational outputs are retained. The first run completed the calculation
  but failed while converting huge integers to strings; its traceback remains
  in `checks/one_box.log`. Enabling integer serialization in the local harness
  produced the saved output in 65.438 seconds. This does not repair the certifier.
- `twist_review.json`: exact constant-term and arc-orientation counterexamples
  to Main's all-twists certificate implementation, plus its wrong rounding direction.
- `partition_review.json`: a rational domain-width example omitted by rounding
  the number of boxes. It does not show a hole in E's divisible default region.

The runner used one CPU, one BLAS/OpenMP thread, a monitored 1 GiB memory ceiling,
and respective 60/90/120-second limits; peak observed usage was below 91 MB.
Run the public probe with arguments pointing to the pinned Computation and
Experimental/scripts directories. Run `one_box.py <pinned Experimental/scripts>`
for the small box, with Python 3.12 and the environment's package versions.
Run `python Computation/audit_cut_flow_api.py` and
`python Experimental/scripts/rigorous_cell_volume.py` from the pinned Kepler folder.
The requested large region sweep is deferred until the mathematical enclosure
argument is repaired. No remaining local job is hidden or running.
