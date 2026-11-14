# Local evidence at the 06:53 Pacific review

Exact source hashes and versions are in `environment.json`. The jobs used one
CPU, one BLAS/OpenMP thread and a monitored 1 GiB memory ceiling. No Lean target
was submitted. All local jobs have stopped; none is running in the background.

- `independent_probes.py/json` records an exact false origin-interior result
  from E's new verifier, an 18-neighbor counterexample to Main's degree premise,
  and the elementary nesting argument for at-most-F face classes.
- `volume_v2_controls.log`: E's old two defect witnesses and five named controls
  pass in 24.766 seconds under a 90-second cap. They miss the new false helper
  acceptance. This is not a soundness certificate.
- `dense_shell.log`: C's complete fixture program was capped at 120.188 seconds.
  Before the cap it recomputed the thirteen rational cell volumes, their sum 512,
  the central value 5.554454804528846, periods 8/12/16 checks and a radial flow.
  It was still running the parameter-family search when killed. The entire
  program is therefore not recorded as PASS. The generic engine's floating
  determinant filter and completeness proof remain separate review obligations.
- `fixture_probe.py/json`: a separate 0.828-second exact calculation verifies
  the saved rational coordinates, periodic separation, twelve-edge graph and
  flow using the supplied volume data. It proves the star-flow threshold bracket
  approximately 0.00853328708029453 conditional on those volumes; it is not an
  independent volume algorithm. It uses exact fractions without the worker's
  flow solver. The source packing is a sparse periodic example, not arbitrary
  saturated geometry.

Reproduce the probes by passing the pinned `Experimental/scripts` or
`Computation` directory respectively. Run the original programs with
`python Experimental/scripts/cell_certificate.py` and
`python Computation/fixture_dense_shell.py` from the pinned Kepler directory,
under the limits above. Their complete stdout and timing state are preserved.
The requested 100-box and full-window region sweeps are deferred because the
new verifier's mathematical contract still fails; more boxes cannot repair it.
