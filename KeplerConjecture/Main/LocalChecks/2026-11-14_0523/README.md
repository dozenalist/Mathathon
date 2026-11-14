# Local checks at the 05:23 Pacific review

Sources and package versions are in `environment.json`; hashes identify the
actual worker artifacts. No Lean build was requested. All local jobs finished.

- `flow_probe.json`: an independent three-case probe of Computation a25f5be.
  A positive isolated deficit is ignored by three entry points; an edgeless
  positive instance also falsely passes, and its exhaustive scan raises.
  All-negative input reports a negative threshold. These are defects, not
  mathematical counterexamples to the correctly stated cut theorem.
- `completed/contact_polytope.log`: Main's exact field arithmetic plus directed
  interval sign check passes for both FCC and HCP contact-only polytopes.
  Each has 14 vertices, squared radii 3/2 and 2, and maximum 2. This checks
  these particular polytopes; the broader geometric proof is reviewed separately.
- `completed/g8_crosscheck.log`: 52 half-line and 50 interval cases agree.
  Finite agreement and distinct code paths do not prove general soundness.
- `seed_summary.json`: the previous seven delayed runs and seed 0, all 45-second
  search pilots. Best value 5.898007181138247; no tested candidate beats
  5.763417470. Floating separation is approximately 2, not an exact certificate.

The two new checker jobs took 1.343 and 3.141 seconds under 90/60-second hard
caps, one CPU, 1 GiB. Their first attempt lacked PYTHONPATH and did no mathematics;
those logs are retained in `initial_missing_dependency/`. Retry used the existing
local dependency directory and passed. Seven delayed seeds each took about
47 seconds and at most 80 MB, finishing at 12:55:43.784 UTC.

Reproduce with Python 3.12 and the package versions in `environment.json`:
check out the stated source in a separate directory; run
`python probe_flow.py <that checkout>/KeplerConjecture/Computation`,
`python KeplerConjecture/Computation/contact_cell_exact.py`, and
`python KeplerConjecture/Counterexamples/Reviews/g8_checker_independence.py`.
The flow probe intentionally asserts that the pinned bad revision fails its
mathematical contract; it is historical evidence, not a repair acceptance test.
Seed reproduction uses Experimental 498cfc3 and
`python Experimental/scripts/c5_global_search.py --seconds 45 --seed N`
from `KeplerConjecture`, with N=0,...,7. Timing affects stochastic search output.
