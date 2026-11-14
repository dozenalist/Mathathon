# Kepler Conjecture: progress so far

Updated November 14, 2026 for the user's overview and main-branch publication
request. Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the extensive,
consolidated explanation of the entire project, its accomplishments and its
remaining mathematical gaps. The sections below preserve the dated development
of the work and must not be read as simultaneous current instructions.

**The 45-minute automation is paused. Sair-Watch remains stopped.** No new
research assignments were sent for this documentation request. Publication on
main is explicitly authorized by the latest user instruction.

The reviewed project has exact analytic control certificates, checked geometric
examples, a limited Lean normalization result and a substantial record of
independent error detection. It has no accepted simpler Kepler proof or improved
known packing bound. The geometric compensation argument, quantitative stability
and general certificate-checker guarantees remain open.

The 08:23 review found two false accepts in Computation's volume checker and a
missing Main stability program. Later public commits now implement targeted
checker repairs and that pilot. Source inspection does not establish their full
correctness; the overview separates these newer inputs from the independently
reviewed snapshot. This publication preserves the reviewed source history and
links those later immutable revisions without silently treating them as accepted.

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

## What the 02:23 scheduled review established

Counterexamples produced a rational sum-of-squares certificate for an ordinary
Cohn–Elkies bound below 0.794809295672. We independently reconstructed its
polynomials, Fourier transform, sign argument and final rational comparison.
This is a valid but weak control, worse than both known results and our earlier
degree-33 certificate. It adds a reproducible example, not a better packing bound.

Main's latest generic checker fixes the earlier examples but still misses a
very narrow negative interval between irrational roots. We supplied an exact
rational witness and asked Main to establish a complete decision rule, with
Counterexamples independently reviewing it. Passing the existing regression
suite is insufficient to accept the checker.

All ten local jobs finished with bounded resources. The four-seed geometric
search found no counterexample, but its upper-volume estimates cannot prove
the desired lower-volume inequality. Transfer and block fixtures remain finite
controls. The submitted SDP run produced no improvement. The smaller Lean
module exceeded one gigabyte of memory without verification, so only the older
algebraic normalization is accepted in Lean. A transfer constant, cut-condition
quantifiers and the infinite-packing extension still require reconciliation.

Main ended its block after 45.573 minutes and received a fresh hour of concrete
work, including an independent fallback after the checker repair. The other
three chats continue their existing blocks without interruption. Actual
Ultramath model calls are verified in all four. Detailed evidence, source hashes
and delivery records are in [the 02:23 review](Main/REVIEW_2026-11-14_0223.md).

## What the 03:08 scheduled review established

Counterexamples improved its own reproducible construction to a bound below
0.780718153344. Its rational factors, Fourier transform, signs and final comparison
passed independent exact checking. This is still weaker than the project's K33b
control and known bounds. Computation also supplied explicit rational algebraic
identities for both sign conditions; the identities and their Fourier relationship
check, but the resulting bound exceeds one and is only a format demonstration.

Main's proposed transfer threshold failed review. It used an upper bound on a
cluster's deficit as a lower bound, so its claimed necessary threshold does not
follow. Cut conditions also need their proper quantifiers: checking one whole
period does not establish all cuts, and a boundary estimate for balls cannot be
applied to arbitrary subsets. These obligations now guide the agents' work on
collective geometric compensation and a runnable cut/flow evaluator.

Main accepted the transfer objection, withdrew the original threshold and proposed
a weaker singleton version. Its distinction between a constant valid for all
packings and one specific fixture still needs care. The correction is integrated,
with rejected text and remaining obligations retained.

The latest sign-checker repair passes the exact examples that defeated previous
versions and its 35-case regression suite. A general proof is still pending;
successful examples alone do not establish completeness. Seven local jobs
completed normally. Three 4,000-iteration search pilots each reached their
90-second cap without a final candidate. A separate rescaled SDP pilot produced
only slightly weaker proposals than the frozen X certificate. There is no new
Lean result or universal geometric certificate.

The timing audit rejected all four previous blocks as full substantive hours:
Main, Computation and Counterexamples ended early; Experimental reached an hour
but used repeated sleeps near its end. Its earlier elapsed-time acknowledgement
was explicitly corrected. All four received fresh hour-long tasks in verified
Ultramath, with independent fallbacks and no permission to pad time. The review
records both mathematical evidence and [actual activity](Main/REVIEW_2026-11-14_0308.md).

Main then ended the next block after another 12.614 minutes. It was reassigned a
longer independent proof package so useful work can continue without waiting on
the other workers. No full substantive hour is claimed on the basis of a prompt.

## November 14, 03:53 review: clearer certificates, corrected claims

Counterexamples supplied three certificates with explicit rational matrices on
both sides of the Fourier bound. Independent exact checking verifies the
strongest below 0.782267220134. It uses three 6-by-6 matrices and about 10 KB of
input, with some large rational entries. It is easier to verify through matrix
identities, but remains weaker than the earlier X-C014 and K33b controls and
known bounds. The next assignment includes making this certificate easier to
read and reducing its coefficient size, without claiming a new packing result.

The new geometric cut evaluator passed its own tests but failed independent
checks of its input geometry: a volume enclosure misses the true value, ring
edges are added below their actual distance, and the FCC constructor crashes.
Its sparse periodic fixture is not saturated. Computation and Counterexamples
are repairing and auditing those premises before exact threshold claims can be
accepted. This illustrates why successful graph tests are not enough to certify
the packing they describe.

Main's cut/flow draft had mistakes in boundary placement, the capacity threshold
for a closed graph, and the compactness hypothesis. It incorporated the review
and preserved the rejected version. Independent checking of the repair
continues. A criterion that implies Kepler is not automatically circular;
the work must prove that criterion without assuming Kepler. Claims about all
finite cuts still require more than a whole-period density condition.

A new negative-allowance input makes the old checker falsely report a bound
near 0.0152. The local reproduction confirms it. Main now rejects negative
allowances, and 37 regression cases pass; this repairs the named defect while
the general soundness review remains open. Specific accepted certificates use
independent exact arithmetic rather than trust in this checker.

The geometric work includes a structured C5 candidate with numerical volume
about 5.8980 and a draft proof of constant Barlow cell volume. Neither is a new
accepted result: an upper volume does not prove the desired lower bound, and
the Barlow draft's redundancy argument needs repair. Experimental is tasked
with exact geometry, the missing lemma and honest scope for the finite searches.

All local checks finished or hit their explicit limits. The quintic search and
C5 anneal hit 45- and 60-second caps. No new Lean target was supplied. C, E and X
ended after 49.738, 47.894 and 41.969 minutes, respectively, so none completed
the required hour. Each received a fresh full-hour assignment with useful
fallbacks. Main's ongoing hour was preserved. Delivery and actual Ultramath
runtime evidence are recorded in the [03:53 review](Main/REVIEW_2026-11-14_0353.md).

## November 14, 04:38 review: repaired inputs and smaller certificates

The smaller C017 certificate reduces the largest rational entry from 563 to 41
characters. An independent exact reconstruction verifies a bound below
0.782267254857, slightly weaker than the original. Computation's repaired
dodecahedral enclosure, edge-distance threshold and FCC constructor now pass
the exact tests that failed earlier. These are targeted repairs; arbitrary
flow outputs still need independent checking.

Counterexamples reviewed the repaired finite/infinite graph theorem and checked
small instances with a separate exact procedure. It remains conditional on
the geometric cut inequalities, which are still the difficult part. Experimental
withdrew the unsupported irremovable-excess claim and supplied a contact-cell
repair for Barlow geometry. The scripts run, but some key decisions remain
floating-point comparisons, so their exact-proof labels are not yet accepted.

The new seed-0 local geometry pilot found no improvement. Seven further seeds
are a separately recorded local task, capped at one minute each and using one
CPU and at most 1 GiB. Their results await the next review. Main ended its prior
block after about 46.61 minutes and received another full-hour assignment.
The other three chats were already doing substantive work when refreshed, so
they were left on their existing tasks. No full substantive hour is inferred
from an interim push or a self-reported clock. The [04:38 review](Main/REVIEW_2026-11-14_0438.md)
records the exact source cutoff, scope and delivery evidence.

## What the 05:23 scheduled review established

The flow checker could overlook a vertex absent from its edge list. An isolated
vertex with a positive deficit was therefore accepted even though it cannot
receive any flow. We reproduced this independently on the current source,
including an entirely edgeless example. This refutes the software's acceptance,
not the correctly stated graph theorem. Computation is repairing the public
interface and Counterexamples will audit the fix.

Main's replacement calculation for the two Barlow contact-cell types uses
exact field arithmetic with directed interval signs. It passes locally and
supports the repaired contact-only containment step. A separate check found
agreement on 102 selected polynomial-sign cases; general soundness remains
an open proof obligation.

The seven delayed geometric searches all finished. Across the eight short
pilots the best value was 5.898007181138247, above the target needed for a
counterexample. These runs neither prove the proposed pair bound nor certify
all configurations. Main has drafted a conditional route from pair volumes to
density, but its matching hypothesis and compactness/equality arguments still
need independent checking. Those are now explicit worker assignments, not
accepted improvements. The [05:23 technical review](Main/REVIEW_2026-11-14_0523.md)
records sources, objections and exact delivery evidence.

## What the 06:08 scheduled review established

The previously failing isolated-vertex and empty-graph examples now reject,
and the repaired flow checker passes a 69-case audit locally. Computation
also produced exact nonuniform cell fixtures and reports 500 finite examples
with no positive transfer threshold. These cases do not yet test the difficult
positive-deficit regime needed by the proposed general geometric approach.
Its next task is a legal three-dimensional example that does.

The new interval-volume implementation has a mismatch between its error norm
and radius estimate. Its claimed radius validation also accepts an unbounded
cell because it checks vertices without excluding infinite rays. We saved
exact witnesses. A small requested box reproduces the author's numerical
output, but agreement cannot make the proof sound. Experimental is repairing
the argument and Counterexamples will audit it before a larger local sweep.

Main's proposed all-twists certificate omits a constant in the distance
formula and chooses the complement of the needed arcs. Its endpoint expansion
also cannot certify a cover by strict clashes. This invalidates that certificate,
not necessarily the underlying geometric impossibility statement. Main and
Counterexamples have the concrete failures, and the broader pair-to-packing
bridge remains unproved. The [06:08 technical review](Main/REVIEW_2026-11-14_0608.md)
preserves sources, corrections, tests and the distinction between working
claims and independently accepted results.

## What the 06:53 scheduled review established

The transfer experiment now has a useful nontrivial test: a rational shell of
twelve spheres surrounding a central one, repeated periodically. Its central
cell is smaller than the Kepler cell volume, so it needs an inward transfer.
The submitted calculation reproduced the cell values locally. A separate
exact probe checked that the coordinates form a legal packing, identified the
twelve transfer edges and verified a radial flow. The positive capacity is
about 0.0085333, conditional on the volume data. This tests one sparse periodic
example; it does not prove the condition for arbitrary saturated packings.

Experimental repaired the old error norm, but the new boundedness helper says
the origin is inside a triangle that lies entirely in x+y+z=1. That exact
counterexample and the unresolved numerical radius estimate block certificate
acceptance. Its claimed tiny volume for a unit-offset cell also contradicts
the fact that such a cell contains the unit ball, so the input and normalization
must be checked. Main's simpler axial twist derivation is useful working
mathematics, while the broader argument still needs correct neighbor counts,
boundary estimates, asymptotic limits and arbitrary orientations.

These are concrete advances in examples and error detection. They do not yet
improve the known packing bound or yield a simpler proof. Sources, local caps,
delivery records and the precise pending claims are in the
[06:53 technical review](Main/REVIEW_2026-11-14_0653.md).

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

## November 14, 07:38 Pacific: more precise proof obligations

Experimental fixed the earlier test that wrongly accepted a triangle of normals
as surrounding the origin, and replaced its sampled radius estimate with an
exact construction. The supplied controls now pass locally. A separate probe
found another problem: repeating one cube face makes the routine count that
face twice. The specific geometric fixtures remain useful evidence, but the
general certificate cannot yet be trusted without its input conditions and
facet accounting proved.

The classical twelve-face volume theorem does apply to the contracted
polyhedron used in the geometric route; the literature record now points to
the precise theorem and correct attribution. It does not automatically prove
the additional area and displacement estimates. Main also proposes a short
argument using the covering radius of an icosahedron to remove an orientation
restriction. Independent review is underway. Its accompanying global proof
still uses an inequality backwards, and examples of polyhedra were mistakenly
treated as optimal values. These are recorded as open work, not accepted results.

All four sessions stopped before sixty minutes. Fresh assignments include
substantive fallback work and exact review criteria, and all four are confirmed
to run Ultramath. The supervisor ran the small checks locally, integrated the
captured sources with authorship intact and preserved every failed version.
No mathematical improvement to the best known packing bound is claimed.

## November 14, 08:23 Pacific: repairs and a more concrete stability target

The duplicate-plane bug found last check is repaired on the tested inputs.
Experimental's controls, including redundant and scaled planes, now pass locally.
Computation replaced its floating determinant shortcut with exact enumeration
and a separate certificate checker. Twenty-five supplied tests pass, and another
volume formula reproduces the saved dense-shell result. Independent probes still
found two ways to fool the standalone checker: duplicate the entire boundary,
or add a cutting plane that only the producer checks. Both exact witnesses were
sent back immediately. The finite fixture remains useful; generic soundness is
still an open proof and implementation obligation.

Main repaired the reversed volume inequality and withdrew its inference from
example polyhedra to optimal values. Its new stability estimate is more concrete,
but remains based on sampling and unproved steps. The requested local certificate
command names a missing file and has inconsistent constants and success criteria.
Main now owns a runnable, properly scoped handoff. Independent review also found
that dropping the second-cell hypothesis from a geometric exclusion loses the
ordinary distance-two contacts. These distinctions prevent a local lemma or a
successful numerical sample from being mistaken for a universal packing bound.

Main and Experimental finished after roughly 44 and 22 minutes and were restarted
with substantive full-hour tasks and fallbacks. Computation and Counterexamples
kept their existing tasks. Runtime Ultramath and message deliveries are verified;
an hour of substantive work is still something to check, not assume. Four bounded
local checks finished, source authorship and rejected versions were preserved,
and both the agent and supervisor reports survived a filename collision.
