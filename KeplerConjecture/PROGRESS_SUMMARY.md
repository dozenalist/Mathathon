# Kepler Conjecture: progress so far

Updated at the transition to hourly supervision, November 14, 2026, Pacific
time. This is the cumulative human-readable account; each hourly check updates
it and adds a short entry in [HourlyUpdates](HourlyUpdates/).

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
collection contains 16 source records, precise theorem locators, three selected
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

## New SAIR work awaiting the next independent review

The latest four SAIR branch checkpoints have been combined into the public
review branch. Their source hashes are in [HOURLY_SYNC.json](Main/HOURLY_SYNC.json).
They are working research artifacts, with the following review priorities.

- Computation now supplies an exact rational sign checker and reports a
  certificate giving density at most about 0.78010544. This is weaker than the
  classical analytic control, and it has not yet been independently reproduced
  locally. Its potential value is a small, checkable baseline. The next review
  must inspect the Fourier map, rational arithmetic, treatment of pi, roots and
  signs at infinity before accepting the claim.
- Experimental has clarified a conditional cluster-averaging criterion and a
  proposed way to add local neighbor counts to a higher-point analytic method.
  The difficult geometric inequality remains open. A proposed explicit thin-shell
  neighbor bound still needs its primary-source constant and varying-radius
  argument checked. No proof simplification is claimed from the accounting
  reformulation alone.
- Main has withdrawn the faulty numerical conclusion and proposed repairs to
  its counting and hybrid arguments. Counterexamples has supplied a new
  independent review. These need reconciliation before they become accepted
  statements in the consolidated account.

## How the next stages will run

The four Sair-Watch processes have been stopped. Hourly reviews in this Codex
chat now read the existing SAIR sessions directly, review new evidence, run
actionable heavy computations locally, and send concrete next prompts. There
will be at most four active SAIR chats, including Main; historical swarms will
not be resumed. Actual Ultramath runtime activation remains unresolved.

Each hourly push includes a short readable update, this refreshed cumulative
summary, technical evidence, and a dated copy of the user-facing response.
GitHub synchronization preserves worker commits and separates published working
claims from independently accepted results. The current publication destination
is the review branch in [PR #1](https://github.com/dozenalist/Mathathon/pull/1).
Integration into the shared default branch remains pending authorization.

The immediate priorities are to validate the new certificate, check the local
geometric lemmas, and test whether one concrete hybrid candidate improves on
the controls. The final part of the event is reserved for independent checking,
integration and an honest exposition of the strongest result obtained.
