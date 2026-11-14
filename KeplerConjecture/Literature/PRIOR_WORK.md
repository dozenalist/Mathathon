# Earlier Kepler research in SAIR

Reviewed for provenance on 2026-11-13, America/Los_Angeles. The GitHub
KeplerConjecture scaffold was empty at source commit
`099c194972c54b9326b119fdd9ad93a09985b408`. The SAIR project contains earlier
research and working files. Main must recover and audit this work before
repeating experiments or promoting its claims.

## Session and artifact inventory

All sessions below belong to SAIR project `KeplerConjecture`, canonical name
`p-36b7a2950416475fab4b275b5afdfeb2`, in `BYU Mathathon Team`.

| Session | Prior work | Initial recovery assignment |
| --- | --- | --- |
| `based-on-the-chats-e0wz` | Analytic-bound research brief and swarm `smwg019eu` | Main inventories reports and outstanding claims, then coordinates the four assigned sessions |
| `using-the-chats-in-mcl6` | CE experiments, FCC/BCC shell diagnostics, local and higher-point proposals, swarm `smwfyzz1k` | Computation recovers executable inputs and corrects normalization before local reproduction |
| `i-ve-attached-thomas-4iws` | Hales reconstruction and discussion of local/global bounds | Experimental checks each proposed local inequality against the primary source |
| `i-ve-attached-viazovska-f7hh` | 8D proof reconstruction and formula checks | Counterexamples audits new Kepler candidates and any proposed transfer from 8D |

Both named swarms have `ultramath_ended` records reporting a VM-runtime restart.
The older eight-member assignments exceed the current four-chat capacity.
The new plan uses the four listed sessions with their explicit assignments.
Their historical results remain available for read-only recovery.

The API exposes these earlier files within the Kepler project workspace.

| Path | Recovery status |
| --- | --- |
| `KeplerConjecture/Literature/hales-2005-proof-summary.md` | Downloaded to the supervisor's private run archive, SHA-256 `f12aa0e229b01eaf0b0b64aca78cda4b5e88521d5809f5c452e454fd0ba0f0bd` |
| `KeplerConjecture/Literature/sharp-bounds-in-dimension-3.md` | Downloaded to the private archive, SHA-256 `b7990d4be0ace6c9d3a7dae41df8c8dd3d837db1a4e8180d80d93092a0530260` |
| `KeplerConjecture/Literature/fig-CE-dim3.png` and `fig-CE-dim3-log.png` | Listed by the API, numerical provenance awaits recovery |
| `KeplerConjecture/Roadmaps/dim-3-analytic-bound-prompt.md` | Referenced in the coordinator transcript, contents await recovery |

The private archive is under the ignored supervisor run directory recorded in
the local ownership manifest. These earlier notes are AI-generated research
artifacts. Their claims need independent checks before integration into the
project's accepted results.

## Questions the first cycle must settle

- Recover the original Gaussian/Laguerre coefficients, grids, solver settings,
  and FCC/BCC shell enumerators. An earlier transcript identifies and repairs
  a dual-shell enumeration bug. Reproduce the final version locally.
- Audit all uses of `delta`. Some earlier notes use it for number density at
  minimum separation one, with FCC value `sqrt(2)`. Convert to occupied volume
  fraction by multiplication by `pi/6` before comparing numerical bounds.
- Check the primary theorem behind every impossibility assertion. Li's
  ordinary CE obstruction has a precise scope. Claims excluding all
  higher-point, local, or hybrid bounds require separate arguments.
- Retain the retracted claim that every smooth sharp certificate must vanish.
  The transcript records a one-sided boundary derivative error and a
  Viazovska counterexample. Verify the proposed contact-shell repair before
  treating it as a theorem.
- Audit the periodized icosahedral/dodecahedral local-cell witness and any
  proposed averaging correction. A lower bound on every individual Voronoi
  cell that fails on this witness cannot establish general packing density.
- Check restricted grid/lattice claims against their exact hypotheses.
  Equality classifications for all maximal-density packings need attention
  to zero-density defects and periodicity assumptions.
- Recover the final Fourier-sign computation for the last interrupted report.
  A negative Fourier value invalidates a CE certificate even when its proposed
  zeros and value at the origin are correct.

The initial status for these recovered claims is `PENDING_REVIEW`. The first
research cycle must assign claim IDs, named reviewers, original file locations,
and reproducible evidence. Published sources in CORE_SOURCES.md provide the
reference standard for established theorems.
