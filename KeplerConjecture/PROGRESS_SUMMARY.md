# Kepler Conjecture: progress so far

Updated November 14, 2026, after the 00:53 Pacific instruction to check every
45 minutes. The mathematical status remains that of the preceding review,
which rejected the submitted certificate. This cumulative account is updated
at each scheduled check, with a short entry in
[HourlyUpdates](HourlyUpdates/).

## Where the project stands

We have not yet found a simpler proof of Kepler's theorem or a new best packing
bound. We have established a research plan, assembled the key literature,
recovered earlier agent work, reproduced numerical controls locally, and found
several errors that would otherwise have led the project down false paths.

The goal remains a clearer proof of the three-dimensional density bound
`pi/sqrt(18)`, approximately 0.74048. We are comparing local geometry, analytic
auxiliary functions, and methods that combine more than pairwise information.
The known obstruction to sharp ordinary Cohn–Elkies bounds in dimension three
means that a purely two-point construction is a control experiment, not by
itself a route to the exact Kepler value.

## Work completed and checked

The roadmap follows the requested seven-part structure. The literature
collection contains 17 source records, precise theorem locators, four selected
primary-source PDFs, and a versioned review of recent Hexagon material. It
connects Hales's local accounting lemma with Cohn–Elkies and the dimension-eight
and dimension-24 constructions, while keeping their differing hypotheses clear.

Independent review corrected a false rational-point counterexample, an
overstated finite-zero obstruction, sign mistakes in proposed hybrid bounds,
and errors in density and polynomial-variable conventions. Later reviews found
gaps in the exported periodic-approximation and counting proofs. The rejected
versions and objections are retained so they are not rediscovered as results.

Local numerical execution found that Main's first optimizer omitted the entire
Fourier-positivity constraint. Its claimed failure of grid methods was therefore
invalid and has been withdrawn. A separate implementation includes both sign
conditions. At degree 31, refining its grid changed the reported density value
from about 0.77970245 to 0.77974877. Degree 41 on the finer grid gave about
0.77974577. Small sign violations remain, so these are useful controls, not
rigorous packing bounds. Full inputs, versions, commands and outputs are saved.

The normalization module passed local Lean 4.35 checks with targeted imports
and only the permitted axioms. It proves an algebraic normalization identity.
It does not prove the geometric ball-volume formula, the counting-to-volume
bridge, or Kepler's theorem.

## What the first hourly review established

The latest four SAIR branch checkpoints have been combined into the public
review branch. Their source hashes are in [HOURLY_SYNC.json](Main/HOURLY_SYNC.json).
They remain working research artifacts. The new independent review found two
concrete failures and narrowed several geometric claims.

- Computation's claimed certificate near 0.78010544 is invalid. Its checker
  ignores failures when logging is disabled, and independent exact arithmetic
  finds a negative value in the Fourier polynomial where nonnegativity is
  required. We saved the precise rational counterexample and original inputs.
  The entire claimed certified ladder needs fresh checking after the software
  is repaired. No new packing bound was accepted.
- Counterexamples' Gaussian search reported infeasibility, but a simple exact
  feasible example disproves that conclusion. Running its actual model locally
  produced a solver model error. We also corrected its density normalization,
  which was wrong by a factor of pi. These are useful repairs to the research
  tools, not an improvement to the known bound.
- Some periodic-counting repairs survive review. Several other arguments need
  narrower statements: averaging over space differs from averaging over sphere
  centers, the shell-angle estimate has a restricted radius range, and a local
  geometric strategy must construct suitable groups of cells rather than
  demand that every possible group works. An elementary boundary-shell estimate
  repairs one accounting step.

The next concrete analytic experiment allows a small positive auxiliary-function
value in a thin shell while charging for at most twelve nearby centers. Its
proposed radius, 2.09, still needs a rigorous justification from the added
Tammes-13 source and the repaired geometry. That source uses computer-assisted
enumeration, which must be included when comparing proof complexity. The actual
three-dimensional numerical strength of this experiment is still unknown.
Alongside it, Experimental is assigned an explicit geometric partition rule,
so analytic reformulations do not displace the local-geometry route.

Both actionable diagnostic jobs ran locally with small resource budgets. There
is no outstanding long-running job and no newly submitted Lean module. Four
focused follow-ups were delivered at 00:25 Pacific, with pushed checkpoints
due by 01:00. The detailed review and delivery records are in
[Main's hourly review](Main/HOURLY_REVIEW_2026-11-14_0008.md).

The workers completed that block before publication, and their new commits are
also included. Main has reconciled the central retractions. Computation supplied
a repaired checker whose regression tests pass locally, while Experimental
supplied revised geometric statements and a partition candidate. These await
full independent review. The strengthened benchmark and rigorous angle-enclosure
programs are still unwritten. The repaired Gaussian driver reports its solver
error honestly, but another local test found integer truncation in its comparison
helper. All small checks have finished. No extra prompt cycle was started;
these completions were triaged into the subsequent assignments.

## How the next stages will run

The latest instruction sets checks every **45 minutes** and cancels Sair-Watch.
A brief requested restoration was stopped when the user changed the cadence;
all four monitor exits were verified. The active schedule reads the existing
SAIR chats directly, reviews completed evidence, runs actionable heavy work
locally and sends concise follow-ups to idle chats. Busy work continues.

All four chats received new research assignments and the requested **30–90
minute work blocks, normally 60–90 minutes**. Main integrates; Computation
implements the strengthened benchmark; Experimental develops the rigorous
angle enclosure and partition route; Counterexamples audits and repairs the
numerical tools. SAIR owns the bulk of the research. Delivery is confirmed for
both assignments and timing updates. This verifies the instructions were received,
not that each agent actually worked for the full requested duration. There are
at most four owned chats; no historical swarms were resumed. Actual Ultramath
runtime activation remains unresolved.

Each scheduled push includes a short readable update, this refreshed cumulative
summary, technical evidence, and a dated copy of the user-facing response.
GitHub synchronization preserves worker commits and separates published working
claims from independently accepted results. The current publication destination
is the review branch in [PR #1](https://github.com/dozenalist/Mathathon/pull/1).
Integration into the shared default branch remains pending authorization.

The immediate priorities are to repair and independently test certification,
finish the local geometric lemmas, and numerically evaluate the shell-count
candidate against an ordinary analytic control. Approximately the final nine
hours before November 15 at noon Pacific are reserved for independent checking,
integration and an honest exposition of the strongest result obtained.
