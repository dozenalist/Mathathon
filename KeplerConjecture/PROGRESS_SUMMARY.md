# Kepler Conjecture: progress so far

Updated at the November 14, 2026, 01:38 Pacific scheduled review. Worker commits
and corrections are combined in the review branch. Local checking found a
geometric proof gap and additional sign-verifier defects. The agents received
further full-hour work after early endings; actual Ultramath runtime is verified,
but an hour of continuous work has not been established. Sair-Watch remains
stopped and the 45-minute cadence is unchanged. No new best packing bound or
simpler Kepler proof has been accepted. This cumulative account is updated
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
full independent review. At that checkpoint, the strengthened benchmark and
rigorous angle-enclosure programs were still unwritten. The repaired Gaussian
driver reports its solver
error honestly, but another local test found integer truncation in its comparison
helper. All small checks have finished. No extra prompt cycle was started;
these completions were triaged into the subsequent assignments.

## What the 01:38 scheduled review established

Main withdrew a proposed geometric proof after we found that it bounded a
positive subset sum using a total that could contain negative contributions.
The corrected accounting statement includes those negative contributions.
The transfer and cluster arguments remain under independent review, with
their boundary and realizability assumptions explicit.

Two general sign checkers had exact false accepts. One ignored irrational
roots; another mishandled endpoint roots. Main's first repair fixed the reported
examples but still accepted squared polynomials that vanished at every chosen
test point. We reproduced these failures exactly and returned the witnesses to
Main and Counterexamples. General checker acceptance remains suspended. X's
replacement passed the named local controls; independent audit continues.

The particular degree-33 rational certificates separately passed Computation's
strict checker and SymPy oracle. The better file's recomputed upper display is
approximately 0.77996622, weaker than known results. The verifier defects do not
by themselves refute those files, and the successful checks do not establish
a new best bound or validate every generic checker.

The rational Tammes comparison reproduced locally. Its connection to the
optimal thirteen-point spherical configuration still depends on the primary
theorem and its computer enumeration. Barlow, transfer, cluster and arithmetic
scripts passed finite controls. These are not universal geometric certificates.
The tested thin-shell allowance gave no gain. Neither that finite experiment
nor the ceiling for one directional estimator closes an entire research route.

The new ball-volume Lean draft did not verify within the local budgets: its
broad import timed out, and an import-only diagnostic version reached the
one-gigabyte memory limit. Main received the logs and owns revision. The earlier
algebraic normalization remains the only accepted Lean component. The submitted
shell proposer command had incompatible degree restrictions; Computation has
the correction task. All local jobs for these snapshots finished.

Main and Experimental ended prior blocks after about 22 and 25 minutes;
Computation and Counterexamples ended after about 40. These do not count as
full-hour completion. Fresh substantive tasks, independent fallbacks and
actual-clock requirements were delivered in verified Ultramath mode. Main leads
the mathematical choices and integration; the supervisor supplies evidence and
local execution. Source revisions, failures, pending work and delivery IDs are
recorded in [the review](Main/REVIEW_2026-11-14_0138.md).

## How the next stages will run

The latest instruction sets checks every **45 minutes** and cancels Sair-Watch.
A brief requested restoration was stopped when the user changed the cadence;
all four monitor exits were verified. The active schedule reads the existing
SAIR chats directly, reviews completed evidence, runs actionable heavy work
locally and sends concise follow-ups to idle chats. Busy work continues.

All four chats have now received fresh **full 60-minute assignments**, with
actual UTC start/finish requirements, interim checkpoints and independent
fallback tasks. Main integrates and reconciles the proof-to-certificate
interface; Computation develops a structured shell proposer; Experimental
works on geometric cell compensation; Counterexamples independently audits
the certificates, Tammes enclosure and shell theorem. SAIR owns the research.
Actual model-call records now verify Ultramath in all four chats. This is
stronger evidence than the earlier maximum-effort settings, which still ran
in standard mode. Delivery is confirmed; the full hour of work is not yet
observed. The scheduled review checks for early endings and continues useful
unfinished work. No historical swarms or extra chats were created.

At the earlier 01:20 checkpoint, fetched worker commits reported a rational control near
0.7799665, repaired positive test fixtures, a directed Tammes enclosure, an
exact Barlow shell argument and a free-width Gaussian implementation. These
were pending independent audit and integration; the subsequent review above
records the local results and remaining obligations. The reported control is weaker
than known bounds and is not a new best packing result. Finite failures of
particular optimizers do not establish that a whole mathematical family is
impossible. The new assignments explicitly require correcting that distinction.

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
