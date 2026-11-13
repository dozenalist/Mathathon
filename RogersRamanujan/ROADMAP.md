# Problem 127: a more natural Rogers--Ramanujan bijection

Prepared 2026-11-13 for a DeepSeek Ultramath coordinated research team.
Repository: [dozenalist/Mathathon](https://github.com/dozenalist/Mathathon).
Official task: [SAIR Mathathon problem 127](https://competition.sair.foundation/competitions/mathathon/problems/127).

## 1. Objective and starting point

Construct an explicit, weight-preserving bijection between partitions into parts
congruent to 1 or 4 modulo 5 and partitions whose consecutive parts differ by at
least 2. The competition asks for a **more natural bijection**, not another proof
that the two classes have equal cardinality. Its references are Garsia--Milne's
1981 announcement and full paper. The official statement was read in the SAIR
browser interface on 2026-11-13; see [the specification](Literature/PROBLEM_SPEC.md).

This is a research plan, not a claim that the problem is solved. The initial
checkout contained empty work directories and empty ROADMAP/PROGRESS files.
This preparation adds literature, a specification, and assignments; the research
programs, candidate maps, and Lean proofs below are **planned deliverables**.

Use these success levels, in descending order:

1. **Full result:** an all-weight bijection with an independently described
   inverse, a complete proof, and a convincing comparison with existing maps.
2. **Substantial partial result:** a new proved map on a precisely specified
   infinite subfamily; a proved simplification of an existing map; a useful
   statistic/refinement; or a theorem excluding a clearly defined class of maps.
3. **Reusable foundation:** verified implementations, reproducible counterexamples
   to specific proposals, a formalized intermediate equivalence, and a clear
   account of the remaining mathematical obstruction.

Levels 2 and 3 are legitimate progress, but must not be presented as level 1.
Formalizing an existing theorem is valuable and must be credited as such.

## 2. Mathematical contract

All executable partitions are descending tuples of positive integers; `()` is
the unique partition of zero. Set

\[
A_n=\{\lambda\vdash n: \lambda_i\equiv1,4\pmod5\},\qquad
D_n=\{\lambda\vdash n: \lambda_i\ge\lambda_{i+1}+2\}.
\]

The deliverable is a uniform family `forward : A_n -> D_n` and
`inverse : D_n -> A_n`, including `n = 0`, satisfying both inverse laws.
Sorting is part of the representation convention, not a way to discard invalid
parts. Never silently delete negative entries or deduplicate multiplicities.

Agree on these common interfaces before workers build competing implementations:

| Interface | Required behavior |
| --- | --- |
| `is_partition(p)` | Positivity and descending order; empty tuple allowed |
| `weight(p)` | Exact integer sum |
| `is_residue(p)` / `is_gap(p)` | Membership in the two families, including representation validity |
| `enumerate_residue(n)` / `enumerate_gap(n)` | Every member exactly once, in a documented order |
| `forward(p)` / `inverse(p)` | Deterministic result on the declared domain; invalid inputs reported |
| `trace(p, direction)` | Optional diagnostic states; inverse must not require the saved forward trace |

Use exact integer arithmetic. State every auxiliary parameter, zero-padding
convention, boundary case, and tie-breaking rule in candidate specifications.
Do not impose length preservation: already at weight 2, `A_2 = {(1,1)}` and
`D_2 = {(2)}`. Fixing the intersection `A_n ∩ D_n` is a possible design choice,
not a requirement of the problem.

### Early reusable equivalences

For `lambda in D_n` of length `k`, put, with indices starting at 1,

\[
\mu_i=\lambda_i-(2(k-i)+1).
\]

Then `mu` is a weakly decreasing, nonnegative vector of length `k`, of weight
`n-k^2`. Retain `k` when trailing zeros are omitted. Adding the same odd staircase
is the inverse. This is a standard reduction, not the missing residue-side map.

Also define

\[
T(\lambda)_i=\lambda_i-k+2i-1.
\]

This is a same-weight bijection from `D_n` to partitions of length `k` whose
smallest part is at least `k`; its inverse subtracts the displayed shift.
For instance, `T(7,3,1) = (5,3,3)`. This translates the intermediate family used
in [BZ82 and BP06](Literature/READING_NOTES.md). The two reductions are compatible:
`T(lambda)_i = mu_i + k`. Prove this small bridge early in Lean.

### What counts as natural

Main should maintain a comparison table for each serious candidate:

- Number and conceptual meaning of rules, auxiliary states, and special cases.
- Whether both directions can be explained from the input alone.
- A termination argument and bounds on operations and intermediate size.
- A structural consequence: transported statistic, refinement, recursion, or
  a recognizable family of examples explained uniformly.
- Dependence on prior equinumerosity, signed cancellation, or global enumeration.

These are project criteria, not an invented official judging rubric. Ranking
both finite sets and matching equal ranks is a useful control experiment, but
does not by itself meet the research objective. Faster execution or shorter code
alone does not establish mathematical naturalness. Specify whether a complexity
bound is in weight `n` or in the binary encoding length of the partition.

## 3. Ultramath delegation and ownership

Use one Main coordinator and four specialist workers initially. These are
assignments to instantiate in the user's Ultramath system, not agents launched by
this documentation update. If capacity is limited, time-slice the roles while
retaining independent review of candidates. Add workers only for distinct,
bounded questions; do not duplicate an entire search without a reason.

| Agent | Primary directory | Responsibility | First deliverable | Reviewer |
| --- | --- | --- | --- | --- |
| **M: Main / Ultramath coordinator** | `Main/` | Definitions, strategy, proof synthesis, novelty comparison, task board, integration | `Main/DECISIONS.md` and `Main/CLAIMS.md` | X for claims; L for formal interfaces |
| **C: Computation** | `Computation/` | Exact enumeration, baseline implementation, benchmarks and reproducible data | `Computation/README.md`, partition library, baseline count report | X independently checks counts and maps |
| **X: Counterexamples** | `Counterexamples/` | Adversarial review, minimal witnesses, failed-map classification | `Counterexamples/REGISTRY.md` and independent checker | M validates interpretation |
| **E: Experimental** | `Experimental/` | Structural conjectures, candidate algorithms, controlled search | At most three candidate specifications with both directions | C executes; X attacks |
| **L: Lean** | `Lean/` | Executable definitions, reusable equivalences, selected proofs and axiom audit | `Lean/README.md`, definitions, staircase/shift equivalence | M checks statement matches mathematics |

Main owns `ROADMAP.md`, literature curation, root build integration, and the
consolidated state in [PROGRESS.md](PROGRESS.md). Every agent must still append
its own major-result entry to PROGRESS on its branch. Main preserves and merges
these entries. Workers own files in their role directory and coordinate changes
to shared interfaces through Main.

### Copyable assignment: M / Main

> Coordinate problem 127 using this roadmap and the Literature index. Freeze
> notation and interfaces first. Keep a queue of bounded tasks, one owner per
> claim, and explicit dependencies. Assign C to exact infrastructure and BZ82,
> X to independent falsification and literature-obstruction checks, E to at most
> three structural candidates, and L to definitions and the staircase bridge.
> Read the workers' evidence before promoting a claim. Maintain Main/CLAIMS.md
> with hypotheses, proof obligations, source IDs, owner, reviewer, and status.
> At each checkpoint choose which route to continue, revise, or stop. Write a
> coherent proof or partial-result account; maintain the novelty comparison.
> Integrate reviewed changes, update PROGRESS, and push regularly.

### Copyable assignment: C / Computation

> Work in Computation. Implement canonical partition validators and two
> independent ways to count the target families: direct constrained enumeration
> and dynamic programming. Verify empty, singleton, repeated-residue, and tight
> staircase cases. Reproduce Bressoud--Zeilberger's 1982 algorithm with source
> locators, both directions, and state traces; check the scan before translating
> formulas. Supply run commands, exact bounds, timings, environment versions,
> and compact JSON results. Test E's frozen candidate specifications without
> changing their mathematical rules. Return every failure to X and M. Do not
> infer an all-n theorem from a finite table. Update PROGRESS and push checkpoints.

### Copyable assignment: X / Counterexamples

> Work in Counterexamples. Write a checker independently of C's candidate code.
> Attack membership, weight preservation, determinism, collisions, coverage,
> both inverse laws, and termination claims. Test degenerate cases and families
> designed to trigger carry/borrow boundaries. Minimize failures by weight, then
> a fixed lexicographic order; save the candidate version and exact witness.
> Audit proposed statistics before anyone tries to preserve them. Check the
> precise scope of Pak's geometric framework; do not turn a restricted
> obstruction into an impossibility claim about all natural bijections. Audit
> Soodak's Conjecture 4.6 as a bounded experiment with explicit conventions.
> Review major claims independently, update PROGRESS, and push useful failures.

### Copyable assignment: E / Experimental

> Work in Experimental. Start from staircase coordinates, multiplicities modulo
> 5, and the baseline's state traces. Propose at most three mechanisms, each with
> a uniform forward rule, independently recoverable inverse, invariant, possible
> decreasing measure, worked examples, and a precise unresolved lemma. Use
> finite matching or rule synthesis only to discover structure. Distinguish
> fitted examples from held-out weights. Hand frozen specifications to C and X.
> After two checkpoints without a new invariant, reproducible phenomenon, or
> proof lemma, give Main a stop/reformulate recommendation. Keep the Hexagon
> path idea secondary until an actual bridge to A_n and D_n is identified.
> Update PROGRESS and push reproducible candidates, including failed ones.

### Copyable assignment: L / Lean

> Work in Lean with the repository's pinned Lean/mathlib v4.35.0. Read
> Literature/LEAN_API.md and coordinate the representation with C and M.
> Formalize membership and the two intermediate equivalences first. Separate
> executable maps from proofs of membership, weight, termination, and inverse
> laws. Ask M for a precise lemma whenever a candidate is underspecified. Once
> a candidate survives X, formalize its smallest useful proved component or
> complete equivalence. Maintain a dependency table and report exact build
> commands and axiom output. A finite computation or a theorem conditional on
> an unproved hypothesis is not a full solution. Update PROGRESS and push
> compiling checkpoints; label unfinished proof files clearly.

## 4. Work packages and acceptance gates

Times below are suggested elapsed research budgets, not promises. Check SAIR's
live deadline and rules before preparing a submission. Reserve the last quarter
of the available time for independent review, integration, and exposition.

### P0: specification and shared baseline (first 1--2 hours)

- M: read the official formulation and core notes; establish claim IDs
  `RR-C001`, `RR-X001`, etc.; record task ownership and decisions.
- C: enumerate both families through weight 30 and compare with independent
  counts. Publish initial fixtures, including weight zero.
- X: reproduce counts with a separately written method and challenge the
  partition convention; check the length-preservation obstruction above.
- L: confirm the actual build command and namespace, then define the families.
- E: translate the two staircase reductions and give worked examples in both
  directions before inventing new moves.

**Gate:** agreed definitions, exact reproducible counts, and an explicit build
integration plan. A successful empty root `lake build` is not evidence that a
file in `RogersRamanujan/Lean/` has been compiled.

### P1: classical-map benchmark and first proved components (hours 2--6)

- C: implement BZ82 as the first executable reference; reproduce its printed
  examples in its own notation, then translate endpoints via `T`. Add operation
  counts and traces. Start exhaustive map checks through weight 30; extend to
  50 after runtime is measured. Count-only computations may go to 1000 without
  enumerating every ordinary partition.
- X: validate C's map independently, distinguishing implementation mistakes from
  defects in proposed new mathematics. Treat runtime caps as inconclusive, not
  as proofs of nontermination.
- L: prove positivity, order, weight change/preservation, and both inverse laws
  for the staircase/shift bridge, including `k = 0`.
- M: document what the baseline actually does and what improvement would be
  meaningful. Keep full GM81b reproduction as a follow-up if access and time
  permit; do not let its length block the shorter baseline.

**Gate:** one trusted existing map and at least one reusable proved component,
or a precise implementation obstruction with a smaller validated deliverable.

### P2: focused discovery and elimination (hours 4--12, overlapping P1)

Explore these in priority order; M assigns a separate claim ID to each branch.

| Route | Concrete question | Required evidence to continue | Stop or redirect when |
| --- | --- | --- | --- |
| **R1: simplify baseline dynamics** | Can a repeated segment of the involution walk be replaced by a proved arithmetic rule with a direct inverse? | Exact trace pattern, general formula, and a lemma proving the same endpoints | It only caches previous examples or assumes the desired final state |
| **R2: staircase and Durfee coordinates** | Can residue multiplicities determine `k` and the residual partition without global ranking? Can BP06 rank symmetries expose the missing structure? | A reversible encoding, or a proved invariant/refinement on a stated subfamily | Only one side has an encoding; the other side is still selected by exhaustive search |
| **R3: recursive insertion, abacus, or paths** | Can modulo-5 carry rules implement matched recursive decompositions of the two families? | Disjoint cases with paired inverse branches and a decreasing parameter | Matching finite counts is the only justification, or added state cannot be recovered |

Subtasks suitable for small additional workers, if Ultramath has capacity:

- C2: profile baseline orbit lengths and intermediate sizes; label empirical
  growth separately from proved complexity.
- E2: search for statistic correspondences using training weights at most 20,
  then evaluate frozen rules at weights 21--40 and on stress families.
- X2: independently extend Soodak's published check beyond 20, specifying what
  happens when a transferred part disappears or a new part is created.
- L2: prove generic finite-involution path lemmas if they will serve a selected
  route; this is infrastructure, not evidence of a more natural endpoint map.

Hexagon's Riordan-path source is a **secondary inspiration** for R3. Its
Rogers--Ramanujan-type series quotient is not a map between our partition sets.
Read [the review](Literature/HEXAGON_REVIEW.md) before spending a worker on it.

**Gate:** retain at most two candidates, each with forward and inverse
specifications, reproducible independent tests, and a named all-n proof gap.
Archive rejected routes with their smallest known witness and scope.

### P3: proof, formalization, and adversarial review (next 6--12 hours)

For the selected candidate, M breaks the argument into:

1. Every branch is defined and mutually compatible; cases cover the domain.
2. Each step preserves the stated invariant and yields valid auxiliary objects.
3. A well-founded measure decreases, or a finite-path argument proves exit.
4. Terminal objects lie in the required target class with the correct weight.
5. The proposed inverse is defined on every target and recovers each branch.
6. Both compositions are identity maps; all exceptional cases are covered.
7. The claimed improvement and any transported statistic are proved separately.

X reviews the proof independently of the code. C freezes a reproducible
candidate version and reruns the agreed checks. L formalizes stable lemmas and
reports precisely which proof obligations remain. Avoid spending the whole
project formalizing analytic machinery irrelevant to the chosen map.

**Gate:** either a complete proof package, or a clean partial theorem with
explicit hypotheses and an honest explanation of the missing extension.

### P4: consolidate a reviewable result (final quarter of available time)

- M writes `Main/RESULTS.md`: exact claim, relation to prior work, forward and
  inverse algorithms, proof, examples, scope, limitations, and remaining gaps.
- C provides one-command reproduction and a compact verified results manifest.
- X provides a final independent review and all unresolved objections.
- L records toolchain, commit, checked theorem names, build logs, and axioms.
- M updates PROGRESS, reconciles literature versions, pushes reviewed work, and
  prepares a SAIR-ready account. The human project lead handles the final
  competition submission and declarations under the current rules.

## 5. Experimental and proof discipline

Use direct enumeration, count-only recurrences, and candidate tests for different
purposes. For the gap family, with minimum part `s`, let `d_s(n,m)` count
partitions of weight `n` with largest part at most `m`. Then

\[
d_s(n,m)=d_s(n,m-1)+d_s(n-m,m-2)\quad(m\ge s),
\]

with `d_s(0,m)=1`, `d_s(n,m)=0` for `n<0`, and `d_s(n,m)=0` for
`n>0, m<s`. Use signed indices or explicit guards at boundaries. On the residue
side use unbounded coin-change DP with positive allowed parts at most `n`.
Neither method may call the other side's count as an oracle.

Do not assume equal largest-part cutoffs produce a finite Rogers--Ramanujan
identity. For example, at weight 5 with cutoff 4, the residue side has two
partitions and the gap side has one. A refined or finitized identity needs its
own correct boundary conditions and proof.

Candidate validation must check domain, codomain, exact weight, output
uniqueness, target coverage, and both inverse laws. Include empty partitions,
all ones, one allowed part, repeated large residues, tight odd staircases,
large gaps, and boundaries where a local rule changes branch. Random tests
supplement exhaustive small weights; record their generator and seed.

Every result record includes:

```text
claim_id / candidate_id / candidate_version
owner / independent_reviewer
status: PROPOSED | TESTED_FINITE | PROVED | LEAN_VERIFIED | REFUTED | BLOCKED
statement and exact hypotheses
source_ids and source locators
artifact paths and git commit
reproduction command, environment, seed, bounds, runtime
evidence or minimal counterexample
remaining proof obligations and next task
```

`PROVED` requires a written argument, `LEAN_VERIFIED` a matching kernel-checked
statement with disclosed assumptions, and `REFUTED` an actual witness to the
stated claim. A failed search is not an impossibility theorem. If a broader
claim fails, give a corrected claim a new ID and preserve the earlier record.

Suggested handoff: E writes `Experimental/<candidate>/SPEC.md` and a tiny
example file; C adds an implementation and report; X adds an independent
review/witness; M writes the proof outline; L adds the corresponding theorem
dependencies. Proposed paths are created when work begins, not assumed to exist.

## 6. GitHub synchronization and PROGRESS policy

**Every agent must periodically commit and push its work to the Mathathon
GitHub repository and update PROGRESS.md with major results.** Use the following
cadence while actively working:

- Push a coherent checkpoint at least every **30--60 minutes**, after a major
  result, and before handoff or stopping. Include useful negative results.
- Update PROGRESS immediately for a new theorem, a significant counterexample,
  a candidate promotion/rejection, a formalization milestone, or a blocking gap.
- M reviews worker updates roughly hourly, integrates compatible changes, and
  records the next dependency to resolve. Avoid status-only noise when nothing
  has changed.

Start by checking the actual remote, branch, and dirty files. Prefer one worktree
and branch per role, such as `rr127/main`, `rr127/computation`,
`rr127/counterexamples`, `rr127/experimental`, and `rr127/lean`. Branch from the
same agreed base. If all workers share a checkout, serialize Git operations;
do not switch the branch underneath another worker. Keep unrelated projects out
of commits. Main coordinates root build edits and merges conflicting PROGRESS
entries without deleting evidence.

Example checkpoint commands, from the repository root and an established
worker branch (replace the role and message):

```sh
git status --short
git diff --check
git add RogersRamanujan/Computation/<specific-files> RogersRamanujan/PROGRESS.md
git commit -m "RR127 computation: describe the actual checkpoint"
git push -u origin HEAD
```

Do not run the placeholder path literally. Stage explicit reviewed files, run
the checks appropriate to the change, and inspect the staged diff. Do not
force-push shared work. On a push failure, retain the local commit and log the
failure; a checkpoint is not uploaded until the push succeeds. Keep large
generated dumps out of Git when a generator, checksum, and compact certificate
suffice. Never put service tokens or account credentials in research artifacts.

Each PROGRESS entry uses a unique ID and records the date/time with timezone,
agent, claim and status, evidence, scope, reproduction, and next action. An
entry may refer to the parent/source commit and a unique run ID; do not attempt
to embed a commit's own hash inside itself. M can add the reviewed commit hash
in the next integration entry. Retain an append-only chronology plus a concise
current-state table at the top.

## 7. Reading order and novelty checks

Start with [Literature/README.md](Literature/README.md). The bundle includes
short source cards, exact locators and access status, a JSON catalog, BibTeX,
a Hexagon search log, and one licensed TeX source.

| Role | Essential reading | Reason |
| --- | --- | --- |
| All | Specification; GM81a; BZ82 | Know the target and the benchmark |
| M | GM81b metadata; BP06; PAK06; PAK18 | Compare mathematical contribution and proof architecture |
| C | BZ82; MSZ09 | Implement a reference map and separate discovery from certification |
| X | PAK04; PAK18; SOODAK18 | Audit scope, proposed statistics, and bounded conjectures |
| E | BP06; SOODAK18; HEX26 | Reusable encodings, testable ideas, and secondary path methods |
| L | LEAN_API; BZ82/BP06 notation bridge | Avoid mismatched definitions and vacuous build claims |

Pak's 2018 survey states a no-geometric-bijection theorem for a specified
framework. The older stability manuscript points to a separate forthcoming
argument. Treat this as a serious constraint requiring a precise hypothesis
audit, not a reason to declare every natural algorithm impossible. Similarly,
do not report conjectural runtime lower bounds as established theorems.

Before claiming novelty, identify the closest existing map, compare it after
normalizing notation, and check whether the proposed algorithm merely computes
the same correspondence differently. A new implementation, a faster algorithm,
a new proof, and a genuinely different map are distinct contributions. Refresh
the targeted literature/Hexagon search before the final account, and record the
date and version of every source actually used.
