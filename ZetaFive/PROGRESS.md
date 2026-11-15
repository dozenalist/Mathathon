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
