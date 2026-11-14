# Problem 15 — a simpler proof of the Kepler theorem

Prepared 2026-11-13 for the SAIR Ultramath research team. The project is confined
to `KeplerConjecture/` in the Mathathon repository. The objective and initial
research directions come from the user's assignment and the official problem.
[Repository](https://github.com/dozenalist/Mathathon) ·
[SAIR problem 15](https://competition.sair.foundation/competitions/mathathon/problems/15?q=kepler)

## 1. Objective and starting point

Find a more understandable proof that the maximum density of equal sphere
packings in three-dimensional Euclidean space is

\[
\Delta_3=\frac{\pi}{\sqrt{18}}\approx0.740480489693.
\]

Hales's theorem and the Flyspeck verification establish the answer. The research
objective is a meaningful simplification of its proof or a useful proved step
toward that objective. The initial Kepler Git checkout has empty ROADMAP and
PROGRESS files and role directories. Existing Kepler SAIR chats contain earlier,
unpushed research that must be recovered and independently audited before new
work is assigned. See [the prior-work record](Literature/PRIOR_WORK.md).
Deliverables described below are research assignments, with their actual status
recorded in [PROGRESS.md](PROGRESS.md).
Source metadata, locators, access limitations, and attribution are in
[Literature/README.md](Literature/README.md).

Begin by comparing Hales's local auxiliary correction, specifically Chapter 3,
Definition 3.2 and Lemma 3.3 of the unabridged proof, with the Cohn–Elkies Fourier
linear programming bound. Study how Viazovska and collaborators make the latter
sharp in dimensions 8 and 24. Explore symmetric functions, local geometry,
higher-point correlations, and genuinely different mechanisms. Allocate initial
effort across these directions. Higher dimensions can supply controls and
transferable ideas, while every research cycle must explain its contribution
to the three-dimensional problem.

**An essential constraint is already known.** Li proves that the ordinary
Cohn–Elkies linear programming bound is strictly above the optimal packing
density in dimension 3. His Theorem 6.1 gives a lower bound greater than
`0.18398089` for the optimum in center-density units, above the Kepler value
`2^(-5/2)`. Any proposal for an exact bound must explain the additional geometric
information or strengthened inequality that takes it beyond this obstruction.
Pure Cohn–Elkies function searches remain useful as reproducible controls and
sources of components. Read the precise theorem and normalization before
interpreting a numerical comparison. [Li, §6, Theorem 6.1](https://arxiv.org/html/2206.09876v3)

Use these success levels, in descending order.

1. **Full result.** A complete proof of the exact three-dimensional upper bound,
   with an independently reviewed argument and an explicit simplification
   relative to the closest known proof. Pair it with the standard FCC lower bound.
2. **Substantial partial result.** A proved local inequality replacing a difficult
   case family, a rigorously stronger and simpler hybrid bound, a proved reduction
   with verified three-dimensional strength, or an obstruction that eliminates
   a precisely specified candidate class.
3. **Reusable foundation.** Reproduced numerical baselines, checked certificates,
   minimized counterexamples, a useful formalized component, or a source audit
   isolating a concrete mathematical gap.

State the achieved level explicitly. Compare simplicity using the hypotheses,
independent inequalities, geometric case count, optimization variables,
certificate size, numerical verification burden, and explanation needed by a
reader. Short notation and an elegant reduction alone do not settle that comparison.

## 2. Mathematical contract

Use unit-radius spheres throughout. A packing center set
`Lambda ⊂ R³` has pairwise distances at least 2. For a fixed origin, its upper
occupied-volume density is

\[
\overline\delta(\Lambda)=\limsup_{R\to\infty}
\frac{\operatorname{vol}(B(0,R)\cap\bigcup_{v\in\Lambda}B(v,1))}
{\operatorname{vol}(B(0,R))}.
\]

The target upper bound covers every such packing, including nonperiodic
packings. Any proof using periodicity, saturation, bounded Voronoi cells, or a
limiting procedure must supply the extension to this statement. With separation
2, boundary errors relate occupied volume and center counts at order `O(R²)`.
The FCC packing attains the target. Include HCP and other Barlow stackings when
testing equality behavior, since equality patterns extend beyond FCC.

### The two starting bounds

For a saturated packing, let `Omega(v)` be the Voronoi cell of `v`. Hales calls
`A : Lambda -> R` negligible when a constant `C1` satisfies

\[
\sum_{v\in\Lambda\cap B(x,r)}A(v)\le C_1r^2
\qquad(x\in\mathbb R^3,\ r\ge1),
\]

and FCC-compatible when

\[
4\sqrt2\le\operatorname{vol}(\Omega(v))+A(v)
\qquad(v\in\Lambda).
\]

Lemma 3.3 bounds the finite occupied density by
`pi/sqrt(18) + C/r`, with `C` depending on the packing through `C1`.
A candidate correction must prove both properties, including the uniform
boundary estimate. A local formula that only succeeds on FCC does not establish
either property for arbitrary saturated packings. Use Definition 3.2 and Lemma
3.3 on printed page 34 of the November 14, 2005 unabridged edition, PDF page 46.
[Hales, unabridged proof](https://annals.math.princeton.edu/supplemental/2005/162-3/p01/proof_kepler.pdf)

For the Fourier route, fix

\[
\widehat f(t)=\int_{\mathbb R^3} f(x)e^{-2\pi i\langle x,t\rangle}\,dx.
\]

A real radial Schwartz function with `f(x) <= 0` for `|x| >= 2`,
`hat f(t) >= 0` for all `t`, and `hat f(0) > 0` yields the Cohn–Elkies bound

\[
\overline\delta(\Lambda)\le\frac{4\pi}{3}\frac{f(0)}{\widehat f(0)}.
\]

Schwartz regularity is a convenient sufficient starting hypothesis. Any broader
admissible class needs its own analytic justification. The formal Kepler target
would require `f(0)/hat f(0) <= 1/(4 sqrt(2))`; Li's obstruction prevents this
within the ordinary bound. Never mix the unit-radius formula with a minimum
separation 1 experiment without explicitly rescaling both the bound and functions.
[Cohn–Elkies](https://arxiv.org/abs/math/0110009) ·
[Li](https://arxiv.org/html/2206.09876v3)

Agree on the following interfaces before implementing candidates.

| Interface | Required content |
| --- | --- |
| Packing fixture | Coordinates, separation normalization, periodic cell or finite boundary convention, exact or interval validation |
| Local correction | Explicit `A(v)`, neighborhood radius, degeneracy handling, FCC compatibility, and a global negligibility argument |
| Fourier candidate | Formula or coefficients, transform convention, regularity, sign regions, normalization, and tail treatment |
| Hybrid theorem | All hypotheses, the extra local or higher-point constraint, proof of applicability to arbitrary packings, and computable objective |
| Numerical report | Candidate hash, dimension, actual density bound, solver status, global feasibility status, precision, and reproduction command |
| Proof dependency | Exact lemma, sources, assumptions, owner, reviewer, and remaining obligations |

## 3. Ultramath delegation and ownership

**Run at most four SAIR chats at once in the Kepler project, counting Main and
all delegated sessions.** Reuse the four existing chats assigned by the
supervisor as Main, Computation, Experimental, and Counterexamples. Combine the five
logical roles in ASTRA.md as below, and time-slice additional specialties.
Main records the actual session IDs and delegation evidence. Historical swarms
ended after a VM restart and must fit the four-chat capacity before any restart.
Count existing active Kepler chats before creating another. Every session and attachment must
be bound to the canonical Kepler project resolved by the supervisor.

| Chat / role | Primary directory | Responsibility | First deliverable | Reviewer |
| --- | --- | --- | --- | --- |
| **M — Main and Lean planning** | `Main/`, `Lean/` | Mathematical contract, proof synthesis, novelty, dependencies, integration, selected Lean source | `Main/CLAIMS.md`, `Main/DECISIONS.md`, task board, formalization scope | X for mathematical claims, C for numerical interfaces |
| **C — Computation** | `Computation/` | Reproducible CE baseline, candidate evaluators, compact certificates, local execution requests | Reference implementation, benchmark specification, first offload request | X independently checks normalization and feasibility |
| **E — Experimental** | `Experimental/` | Hales correction simplification, hybrid and alternative mechanisms | At most three explicit candidate specifications with a named missing lemma | X attacks, C evaluates |
| **X — Counterexamples** | `Counterexamples/` | Independent source and hypothesis review, adversarial configurations, sign checks | `Counterexamples/REGISTRY.md`, obstruction audit, independent small checker | M validates interpretation, C reviews checker implementation |

Main owns ROADMAP, Literature, consolidated PROGRESS, and integration of shared
files. Workers append major results to PROGRESS on their own branches and Main
merges these records. Main coordinates Lean drafting with the local supervisor.
The supervisor performs Lean builds and heavy numerical computations on the
user's computer by default. Keep every tracked change under `KeplerConjecture/`.

### Copyable assignment — M / Main

> Coordinate problem 15 using this roadmap, PROGRESS, and the Literature index.
> Use a 90-minute initial work budget, including collection and review. Recover
> the prior notes and audit their claims before repeating earlier work. Inspect
> the available delegation facility and existing Kepler sessions, then ensure
> the total active chat count never exceeds four. Retain worker IDs and collect
> their outputs before completing. Freeze the unit-radius contract, create the
> claim ledger, and assign bounded tasks to C, E, and X. Maintain genuinely
> different initial routes. Audit Li's obstruction and the precise Hales lemma.
> Require actual 3D numerical evaluation before promoting a CE-like extension.
> Select a small stable lemma for Lean only when it serves a research dependency.
> Have the local supervisor execute Lean and heavy computations using the
> request protocol below. Integrate reviewed evidence, update PROGRESS, push
> a coherent checkpoint, and end with results, reviewer findings, full commit
> hashes, unresolved gaps, and the highest-value next assignment.

### Copyable assignment — C / Computation

> Work in Computation for the initial 90-minute block. Specify and implement a
> small radial polynomial-times-Gaussian CE benchmark in dimension 3, with a
> documented transform, objective, and normalization. Include an independently
> computable elementary fixture. Reproduce a published reference value only
> to the precision and feasibility actually checked. Give X the implementation
> and certificate format. Prepare local execution requests for optimization,
> interval/SOS checks, and larger searches, with bounded runtime and memory.
> Push a runnable request within 30–45 minutes if computation is a dependency.
> For each frozen E candidate report its actual 3D value, gap to Kepler,
> comparison with the control, and whether global sign/positivity conditions
> are certified. Return infeasibility witnesses and inconclusive runs honestly.
> Update PROGRESS and push reproducible code and compact data.

### Copyable assignment — E / Experimental

> Work in Experimental for the initial 90-minute block. Reconstruct Hales's
> negligible/FCC-compatible mechanism and identify a small local inequality
> whose simplification would remove real proof work. Develop at most three
> explicit proposals across local geometry, strengthened Fourier/higher-point
> bounds, and an independent alternative such as transport or geometric
> decomposition. Allocate an initial bounded pass to each before prioritizing.
> Give each proposal a theorem statement, exact auxiliary object, domain,
> equality cases, computational evaluator, and its hardest missing lemma.
> Send the specifications to C and X. Symmetric functions are welcome when
> their additional information escapes the ordinary CE obstruction. Consult
> the Hexagon review, checking whether a transferred construction inherits
> the hard sign proof. Update PROGRESS and preserve useful failed proposals.

### Copyable assignment — X / Counterexamples

> Work in Counterexamples for the initial 90-minute block. Independently audit
> Hales Lemma 3.3, Li's 3D CE obstruction, and all numerical normalizations.
> Test E's proposed claims on FCC, HCP, Barlow stacking variations, perturbed
> periodic packings, boundary clusters, and degenerate local configurations
> that actually satisfy their hypotheses. Check global sign claims between
> sampled radii and in the tails. Validate saturation, boundary terms, and
> higher-point positivity assumptions. Record exact or interval witnesses
> with candidate versions and the scope of each refutation. Supply an
> independent check of C's small baseline. Submit heavy checks to the local
> supervisor. Review claims you did not author and update PROGRESS.

### Lean work within the four-chat limit

Main can time-slice Lean source drafting within its chat or repurpose a finished
worker. Use the pinned Lean/mathlib `v4.35.0` environment. Prioritize a stable
normalization lemma, boundary estimate, finite certificate checker, or a useful
local inequality. Record theorem names and exact mathematical statements.
Push source and explicit commands for local checking. The supervisor returns
logs, exit statuses, and `#print axioms` output. Label source awaiting compilation
`PROPOSED` or `LEAN_CONDITIONAL` as appropriate. Kernel verification requires
matching statements, complete dependencies, and the permitted axioms
`propext`, `Classical.choice`, and `Quot.sound` under the current event rules.
An empty default build provides no evidence about a Kepler module.

## 4. Work packages and acceptance gates

The latest user instruction replaces Sair-Watch with hourly supervisor reviews.
Normally use research blocks of up to 60 minutes to the next review. At each
hourly check, review new completed work, send useful bounded follow-ups, and
push the synchronized Kepler work with a brief hourly update and a refreshed
cumulative `PROGRESS_SUMMARY.md`. Do not restart the retired watchers or
duplicate a task because an old callback arrives. End a block early with a concrete offload
handoff when local execution is the next dependency. Check the current event
deadline and reserve the final quarter for review, integration, and exposition.

### P0 — specification, source audit, and diversity (first block)

- M inventories prior SAIR transcripts, attachments, and unpushed files, records
  their provenance, and recovers useful project artifacts to GitHub. X audits
  previous impossibility and uniqueness claims and every ambiguous use of
  `delta` for center number density versus occupied-volume density. Preserve
  original claims with their status and record corrected versions separately.
- M freezes the mathematical contract and creates claim IDs such as `K15-C001`,
  including hypotheses, owner, independent reviewer, and source locators.
- C specifies a reproducible CE baseline and pushes the first local computation
  request. Include the exact target and an elementary transform/control case.
- X verifies the local and Fourier bounds independently, audits Li's theorem,
  and reviews the convention used in each published numerical table.
- E sketches one local correction route, one strengthened Fourier/higher-point
  route, and one alternative route, each with a testable question.
- M chooses one useful mathematical lemma suitable for proof or later Lean
  checking and maps all remaining dependencies.

**Gate.** Agreed definitions, identified source versions, reproducible baseline
inputs, three bounded research questions, and an actionable local execution
request. A source reconstruction is recorded with attribution.

### P1 — verified controls and first useful components (next 1–3 blocks)

- C obtains and checks a local numerical baseline, with X independently auditing
  a small case and the conversion to occupied-volume density.
- E and M prove a modest component of the Hales/local route or isolate a
  falsifiable correction inequality. State precisely which later step it serves.
- C evaluates at least one concrete strengthened-bound candidate in dimension
  3. Record the value even if it is uncompetitive, infeasible, or uncertified.
- X attacks candidate hypotheses and equality behavior. Retain minimal useful
  witnesses and distinguish implementation errors from false conjectures.
- Main compares the implementation/proof burden to its nearest published
  baseline and commissions local Lean checking only for stable claims.

**Gate.** A reproducible numerical control and either a useful proved component
or an explicit obstruction that narrows the next research question.

### P2 — focused discovery and elimination (overlapping P1)

The rows below are a diverse portfolio, with allocation determined by evidence.
Main records time spent, strongest evidence, proof burden, and the reason for
continuing or stopping each route in `Main/DECISIONS.md`.

| Route | Concrete question | Evidence needed to continue | Redirect when |
| --- | --- | --- | --- |
| **R1 — local geometry and correction** | Can a short local correction or discharging identity imply FCC compatibility with a transparent negligible boundary term? | Explicit formula, challenging configurations, a proved local lemma, and boundary accounting | The correction is defined using the desired global bound or only fits close-packed examples |
| **R2 — strengthened Fourier and higher-point bounds** | Can local exclusion, angular correlations, or a three-point constraint improve the 3D bound with a small certificate? | Precise stronger theorem, independently checked hypotheses, actual 3D optimization, and a feasible/certified candidate | The formulation reduces to ordinary CE, or no numerical strength is demonstrated |
| **R3 — symmetric functions and interpolation** | Can a tractable function family solve a component of R1/R2 or expose a useful sign identity? | Formula, transform, proved sign mechanism or bounded sign-check request, and a concrete 3D role | Equality constraints alone determine a formal object while positivity and strength remain unsupported |
| **R4 — alternative geometric mechanism** | Can transport, a decomposition, stability, or averaged cell geometry supply a smaller universal inequality? | Exact scope, explicit local/global bridge, a proved lemma or reproducible counterexample test | It assumes crystalline order or extrapolates FCC optimality within a restricted family to all packings |

Dimensions 8 and 24 can test a transform, interpolation, or certificate method
against known sharp cases. A higher-dimensional hybrid result is a legitimate
secondary contribution with stated scope. Main must prevent these controls from
absorbing the entire three-dimensional program.

An elegant CE-like reduction receives no promotion without a numerical test in
dimension 3 to the extent the formulation permits. If evaluation is blocked,
identify the exact missing evaluator, resource, or feasibility issue and keep
the route's strength unresolved. After two blocks without a new invariant,
reproducible phenomenon, useful lemma, or clearer obstruction, reformulate or
stop that route. Retain at most two serious candidates after the initial
exploration, with one independent reviewer for each.

### P3 — proof, certification, and adversarial review

For a selected candidate, Main turns the argument into explicit obligations.

1. The stated hypotheses cover the intended packing class, including limits,
   saturation, periodic approximations, and degenerate cases as needed.
2. Every auxiliary function, correction, transform, and operator is well-defined.
3. All sign, positivity, local geometric, and boundary assertions hold over
   their full domains.
4. The inequalities combine to yield the claimed normalized density bound.
5. Equality or sharpness claims cover the relevant close-packed configurations.
6. Numerical components have reproducible certificates and independent review.
7. The simplification and novelty comparison identify the closest existing work.

X reviews the written mathematics independently of the candidate code. C freezes
the certificate and reproduction inputs. The local supervisor compiles selected
Lean modules and returns evidence. Main preserves conditional statements with
their unresolved assumptions.

**Gate.** A complete proof package or a clean partial theorem whose missing
extension is explicit and whose contribution survives independent review.

### P4 — a reviewable result (final quarter of the research window)

- M writes `Main/RESULTS.md` with the exact statement, proof, role of computation,
  closest prior work, simplification achieved, and remaining limitations.
- C supplies one-command reproduction, compact certificates, numerical status,
  environment versions, and a results manifest.
- X supplies the independent review and unresolved objections.
- M records local Lean evidence, theorem statements, assumptions, and build logs.
- M reconciles source versions, integrates PROGRESS, and pushes the reviewed
  checkpoint. Prepare the report and slides required by the current event
  rules. The human project lead handles the official submission.

## 5. Experimental and proof discipline

Published comparison values provide targets for reproduction. Cohn, de Laat,
and Salmon's Table 1.1 reports 3D occupied-volume upper bounds `0.779747` for CE,
`0.773080` for de Laat–de Oliveira Filho–Vallentin's strengthened two-point
bound, and `0.770271` for the general
general three-point bound. Its lattice-only three-point value `0.741506` has a
restricted domain. Preserve that distinction in every comparison. These are
published reference values, with our own reproduction status tracked separately.
[Cohn–de Laat–Salmon, Table 1.1 and Theorems 1.1/1.4](https://arxiv.org/pdf/2206.15373)

Also compare with the dodecahedral theorem's occupied-volume bound of about
`0.7546974`. Hales–McLaughlin derive it from a lower bound on Voronoi-cell
volume. Its proof has substantial computational components, so record the
proof burden when using it as a benchmark for a simpler new bound.
[Hales–McLaughlin, Sections 1.1 and 3](https://www.cs.cmu.edu/~seanmcl/papers/McLaughlin-Dodec.pdf)

Start numerical work with explicit radial polynomial-times-Gaussian candidates
or an equally reproducible basis. Save coefficients, dimension, scale,
normalization, solver version, precision, seed where used, and residuals.
Record the maximum tested sign violation and the tested radius range.
Inspect contact radii, near-multiple zeros, large radii, and narrow unsampled
intervals. A finite grid supplies experimental evidence. A rigorous bound
requires a global sign argument, interval covering with certified tails,
an exact polynomial/SOS certificate where applicable, or another proved method.

Report each objective in both its native normalization and occupied-volume
density. Include the absolute gap to `pi/sqrt(18)`, uncertainty, feasibility
status, and the comparison to the agreed baseline. A rigorous dual obstruction
for an optimization method bounds that method's capability. Record separately
the packing-density theorem established by a feasible upper-bound certificate.

For local geometry, verify that fixtures meet their claimed separation and
saturation conditions. Include FCC, HCP/Barlow examples, perturbations, boundary
effects, and degeneracies. A locally dense cell can occur without implying a
globally dense packing. Test any compensation rule on configurations that
stress the global summation and boundary estimate.

### Local Lean and heavy-computation handoff

Workers write requests in their own role directories, push the required
code and inputs, and alert Main. Main collects them in
`Main/LOCAL_COMPUTE_REQUESTS.md` and includes pending requests in its completion
response so the next hourly review collects them for local execution. If this is the critical
dependency, hand off after 30–45 minutes rather than spending the rest of the
block on the VM. Continue independent mathematical work while a request is pending.

Each request supplies the following fields.

```text
request_id, claim_id, owner, independent_reviewer
purpose and exact mathematical question
repository branch and full source commit
tracked script / Lean module / input paths under KeplerConjecture
exact command, working directory, toolchain and pinned dependency versions
CPU / RAM estimate, elapsed-time cap, precision, seed, parameter bounds
expected output paths, success criterion, and certificate/checker format
whether output is exploratory, a rigorous certificate, or a Lean build
current state and next independent task while execution is pending
```

The supervisor reviews the request, executes it locally within its stated
resources, and returns the exact revision, command, runtime, exit status, logs,
compact output, and verification limitations. Large outputs stay reproducible
from generators and checksums. Lean requests include the actual module target
and `#print axioms` commands. Coordinate imports and any project-local build
wrapper with Main. Keep root build files outside the assigned change set.

Every claim record includes the following fields.

```text
claim_id / candidate_id / candidate_version
owner / independent_reviewer
status: PROPOSED | TESTED_FINITE | PROVED | LEAN_VERIFIED |
        LEAN_CONDITIONAL | REFUTED | BLOCKED
exact statement, domain, normalization, and hypotheses
source IDs, versions, and theorem/page locators
artifact paths, source commit, reproduction command, environment
precision, bounds, seed where applicable, and runtime
proof / certificate / counterexample / experimental evidence
remaining obligations, next action, and responsible owner
```

`PROVED` requires a written argument with justified dependencies.
`LEAN_VERIFIED` requires a matching kernel-checked statement and a disclosed
axiom audit. `REFUTED` requires a witness or a theorem applicable to the exact
claim. Preserve failed claims and give corrected statements new IDs. Distinguish
source reconstruction, experimental evidence, and a new mathematical contribution.

## 6. GitHub synchronization and PROGRESS policy

Every agent commits and pushes coherent project work after major results,
before a handoff, and every 30–60 minutes while actively researching. Main
maintains a concise current-state table and dated history in `PROGRESS.md`.
Each significant entry records date/time with timezone, author, claim ID,
status, independent reviewer, exact statement, sources, evidence, reproduction,
remaining gap, next task, branch, and confirmed push status.

Use isolated branches and worktrees based on the agreed source revision, such
as `kepler15/<role>/<run-id>`. Record the actual branch rather than assuming a
name already exists. Main integrates reviewed worker commits. Serialize Git
operations if a shared checkout is unavoidable. Keep tracked modifications
exclusively within `KeplerConjecture/`, and stage explicit reviewed paths.

Before a checkpoint, inspect status, run `git diff --check`, inspect the staged
diff, and execute the checks appropriate to the changed artifacts. A push counts
as successful only after the remote confirms it. On a rejected push, fetch,
integrate compatible changes, rerun affected checks, and retry normally. Preserve
the local commit and record a remaining blocker if integration cannot proceed.
Retain useful negative results and all unresolved reviewer objections.

Put a reviewed commit hash in a later integration record or external run
manifest. Use parent/source commits and unique run IDs inside a checkpoint's
own files. Preserve source attribution and source access status. Service
credentials belong in the local protected credential store.

## 7. Reading order and novelty checks

Start with the [literature index](Literature/README.md),
[core source cards](Literature/CORE_SOURCES.md),
[problem specification](Literature/PROBLEM_SPEC.md), and
[Hexagon review](Literature/HEXAGON_REVIEW.md). Use the bibliography and catalog
to record every source actually built upon.

| Role | Essential reading | Purpose |
| --- | --- | --- |
| All | Problem specification, Hales Definition 3.2/Lemma 3.3, Cohn–Elkies | Understand the target and the two auxiliary-bound mechanisms |
| M | Hales/Flyspeck overview, Li obstruction, Cohn–de Laat–Salmon | Identify the proof burden, known barriers, and genuine strengthened bounds |
| C | Cohn–Elkies constructions, published numerical tables, higher-point formulations | Establish reproducible controls and the correct objective |
| X | Hales's exact hypotheses, Li Theorem 6.1, global feasibility arguments | Audit scope, normalization, certificates, and boundary terms |
| E | Viazovska, the 24D proof, higher-point methods, Hexagon review | Extract mechanisms that could survive in dimension 3 |
| Lean drafting | Selected stable lemma and pinned mathlib APIs | Match the checked statement to the mathematics |

Hexagon's October 2026 infinite-linear-system construction in dimensions 8 and
24 is a candidate source of ideas. Audit the inherited global sign inequalities
and its dependence on the known magic functions before assigning a simplification
claim. Admit an LLM-generated result into a proof only after its argument and
dependencies survive the same independent review as other sources. Read the
versioned assessment and search log. [Hexagon review](Literature/HEXAGON_REVIEW.md)

Before claiming novelty, normalize the candidate and its closest published
comparison to the same sphere radius, packing class, and density convention.
Identify whether the contribution is a new proof, a new inequality, a shorter
certificate, a stronger computed bound, or a reconstruction of known work.
Refresh the targeted literature and LLM-site searches before the final account.
Record access dates, versions, precise theorem locators, and verification status
for every source used.
