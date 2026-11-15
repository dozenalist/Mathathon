# ZetaFive progress

## 14 November 2026

Published an [exponent catalog](EXPONENT_CATALOG.md) for the original $K=40n$, $N=3n$, $h=37n$, $D_N^6$, $M=200$ construction and its proposed extension from $k=5$ to $k=7$.

- The catalog preserves the comparison table, links the relevant results in Fauzan and Lai, and derives the contributions from small primes, the compact inner range, the tail, the outer range, and the real estimate.
- Exact rational reconstruction gives an arithmetic increase of $751/768$, and the adapted final upper-bound coefficient is $+0.960456781075\ldots$. This estimate does not establish the decay needed for irrationality.
- `node ZetaFive/Computation/exponent_catalog.mjs` passes: it reconstructs the inner integral on 143 intervals, both outer integrals, the row-weight costs, and the reported totals without floating-point arithmetic.
- Claim status: the $k=7$ local determinant estimates still require uniform verification. The computation verifies the accounting, not a proof of irrationality or an impossibility result for other constructions.

## 14 November 2026 at 3:11 p.m. PST

Started a 90-minute SAIR formalization block for the **parallel constructions in the zeta 5 argument**, in the existing ZetaFive project. The session is `chat-b81e1f1139`, titled **Formalize zeta 5 parallel constructions**, using DeepSeek V4.1 Flash with high reasoning.

- Inputs: [formalization brief](Lean/PARALLEL_CONSTRUCTIONS_TASK.md) and [unified framework sources](Literature/ParallelConstructions/README.md), including the TeX note, PDF, supporting checks and SHA-256 manifest. A follow-up message supplied the independently reviewed revision, preserving the same formalization targets and clarifying the domains of later analytic statements.
- Targets: weighted μ–τ transport from independent definitions; affine parameter dependence and its residue interpretation; the affine matrix pencil and change-of-basis identities.
- Acceptance: Lean/Mathlib v4.35.0, compiling project modules, explicit theorem statements and hypotheses, independent review, and recorded axiom output. No `sorry`, added axioms or `native_decide` in completed lemmas.
- Status: **STARTED**. The API confirmed delivery and session history showed the agent inspecting the VM files. No correspondence lemma is claimed as Lean-verified at launch.
- Ownership: the coordinator is to collect functional-algebra, matrix and independent-review work. Source commit: `5f20e2fac14d7f38a56459a2e69d1dd406efaa5e`; later repository changes must be preserved. A local completion watcher will request review of this session through 7:11 p.m. PST, subject to the computer remaining awake and connected.

The API credential is stored outside the repository using Windows account encryption. No credential values are included in the research prompt or source material.

### Earlier parts first

The user directed the same SAIR session to proceed in source order, prioritizing the polynomial/Bernoulli definitions, Euler–Maclaurin polynomial identities, pole extension and first μ–τ transport lemmas before residue and matrix constructions. The API accepted the instruction with message ID `oc_609858b673cd2a45`. The current work budget and proof-quality requirements remain unchanged; no additional mathematical result is claimed by this priority update.

### DeepSeek Ultramath workers and first checkpoint review

The user requested DeepSeek agents on Ultramath. The existing coordinator launched swarm `smwh2nngu` with four members (`m1`–`m4`), model `deepseek/deepseek-v4.1-flash`, and **max** reasoning. The successful `ultramath_start` result is sequence 15373 in the owned session `chat-b81e1f1139`. The launch allows 35 minutes and 60 steps per member, keeping the original approximately 4:41 p.m. PST checkpoint. The formalization brief now preserves this model/facility preference for future workers.

The assignment prioritizes the terminating polynomial Euler–Maclaurin identity, forward-difference/reflection laws, simple-pole and harmonic identities, and independent review. Workers must reuse Mathlib and keep candidate files isolated. A swarm launch establishes that work started, not that its lemmas are proved.

The coordinator's first, pre-swarm checkpoint was independently fetched from branch `codex/zeta5-correspondences-2026-11-14`, commit `909d07fa25797e44c0ee9e2c7e0b8f6e7cc90af8`. Supervisor inspection found a substantive polynomial transport proof from independent μ and τ definitions. The branch reports direct elaboration of 20 declarations under Lean/Mathlib **4.33.1**; it has not completed the pinned **4.35.0** Lake build. This checkpoint remains provisional and has not been merged into main.

Review also identified missing early functional identities, representation-independence and `RatFunc` bridges, extension from rational parameters to the source's polynomial/real parameter setting, and the concrete bilinear Gram interpretation. These are explicit remaining obligations. The first checkpoint's review was self-review; the new swarm is instructed to supply independent review. A follow-up recorded these findings, corrected the B₀/B₁ sanity-check distinction, and requested investigation of the matching official Mathlib artifact cache before assuming a full source build is required. Follow-up message: `oc_c24d7e3f78b45704`; completed turn reviewed: 15347. Monitoring remains attached to the same coordinator.

### Pinned 4.35.0 build succeeded

During review of completion 15489, the supervisor inspected fresh VM evidence: task-local Lean **4.35.0** installation (session sequence 15524), successful retrieval/decompression of 9,031 Mathlib cache files (15538), and `lake build ZetaFive` completing successfully with **`LAKE-EXIT=0`** (15552). The build selected the task-local `ELAN_HOME/bin`, cleared `LEAN_PATH`, and captured the build's pipeline status immediately using `${PIPESTATUS[0]}`. This was the existing six-module library; the matching repository pins are Lean/Mathlib v4.35.0 and Mathlib revision `56a005855ea17e0b0958f73ec801ae140b0a1679`. The earlier toolchain blocker is resolved.

This establishes a successful pinned-environment build, not completion of the requested correspondences. A 4.35.0 axiom audit, independent mathematical review, the missing early functional identities, and the representation/parameter/Gram bridges remain separate obligations. The published research branch was still at `909d07fa25797e44c0ee9e2c7e0b8f6e7cc90af8` when checked; its historical build log will need the coordinator's updated evidence.

Completion 15489 reports the swarm launch, not finished proofs. The already-sent bounded collection/review instruction `oc_c24d7e3f78b45704` was delivered at sequence 15491 and covers this checkpoint. No duplicate assignment or swarm was created. Four workers remained active; their specific directions and any independent reviewer report must be checked from actual worker evidence. The original monitoring deadline remains 7:11 p.m. PST on 14 November 2026.

### 14 November 2026, 5:10 p.m. PST — early-foundations checkpoint reviewed

The supervisor verified completion 16384 against the owned SAIR target and independently fetched commit `2a2b6111ae97a533dce9e3908a1d05750aeb31ed` from `codex/zeta5-correspondences-2026-11-14`. Two independent supervisor reviewers inspected the new declarations and their scope. The four-member DeepSeek Ultramath swarm `smwh2nngu` has finished; its accepted code is on that research branch.

- `M1.L_comp_X_add_one_sub` and `M1.τ_comp_X_add_one_sub` establish the Bernoulli functional and τ forward-difference laws for every rational polynomial. `M3.L_reflect` and `M3.τ_reflect` establish polynomial reflection. These are meaningful consequences of the frozen definitions and Mathlib Bernoulli results.
- `M4.pole_values_unique` establishes uniqueness for a sequence `a : ℤ → ℚ`, from its boundary value, recurrence at positive indices, and reflection at every integer. The explicit candidate satisfies recurrence at nonzero indices. This is sequence-level existence/uniqueness; a theorem deriving these conditions for a rational-function functional remains open. `M3.tauX_reflect` remains a theorem about `XRep` data.
- Raw command results confirm the pinned 4.35.0 build, a clean rebuild of the committed tree, and axiom-driver exit 0. The driver directly checks **22 selected declarations**, all using only permitted axioms. It does not directly audit every new export: the four candidate files contain 76 theorem/lemma declarations. A complete exported-theorem audit is assigned next.
- Review found a false ledger claim: `mu_affine_polynomial` is named as completed but does not exist in the Lean code. The polynomial/real parameter extension remains open. Other corrections concern stale version/Bernoulli comments and the setup script's mismatch with the successful task-local elan path. These reporting/reproduction issues do not negate the observed successful build.

Targets 1–3 remain incomplete. One **60-minute** follow-up was sent to the same coordinator (message `oc_48c8b20b3578a9b2`), ending by approximately **6:10 p.m. PST**. It requests a new bounded DeepSeek Ultramath block with explicit roles: finite Euler–Maclaurin identity first; assembly of the representation-level transport and rational-function interpretation; polynomial-valued parameters and evaluation; and an independent reviewer with no implementation assignment. The coordinator must collect the results, correct the ledger, run the pinned build and full declared axiom audit, and push a coherent checkpoint. The overall **7:11 p.m. PST** deadline is unchanged. Other contributors' main-branch work was preserved; the formalization branch is not yet merged into main.
