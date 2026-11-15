# Formalization and project workflow

The formalization assignment concerns exact correspondences in the ζ(5) construction. It does not claim a Lean proof of irrationality. This records the latest completed review in **Find how to share a GitHub repo** on 14 November 2026; ongoing work should be checked against the current [progress record](../PROGRESS.md) and [formalization brief](../Lean/PARALLEL_CONSTRUCTIONS_TASK.md).

## Mathematical priorities

The requested order is the order of the source: polynomial and Bernoulli definitions; the terminating polynomial Euler–Maclaurin identity; forward differences and reflection; simple poles and harmonic increments; then the first μ–τ transport theorem. Residue and matrix results come after these foundations.

The three main correspondence targets are:

1. Prove the weighted transport identity from independently defined functionals, first for polynomials and then for the specified simple-pole domain:

   $$\mu_X(R)=\tau_X\bigl(x^5R(-x^2)\bigr).$$

2. For $R=P+\sum_j c_j/(t+j^2)$, prove affine parameter dependence with $\Lambda(R)=\sum_j c_jj^4$:

   $$\mu_u(R)-\mu_v(R)=(u-v)\Lambda(R).$$

   Its interpretation as a Laurent coefficient at infinity is a further semantic bridge, not a consequence of naming an abstract coefficient functional.

3. Prove that the resulting bilinear form yields an affine matrix pencil and establish change of basis:

   $$G(u)=G(v)+(u-v)M,\qquad
   \det(C^{\mathsf T}GC)=\det(C)^2\det(G).$$

Keep the variable of the rational function, the pullback variable, and the parameter distinct. An equality of representation data must be connected to equality of rational functions before claiming a `RatFunc` theorem. A rational-parameter theorem does not automatically establish the source's polynomial-parameter or real-parameter theorem. The concrete Gram construction also requires proof that its inputs belong to the functional's domain.

## Acceptance requirements

Reuse Mathlib, pinned with Lean to **v4.35.0**. The initial environment instead used v4.33.1, which was insufficient for final validation against Mathathon's pins. Check the convention $B_1=-1/2$; the useful sanity checks are $\tau(x^3)=1/4$, $\tau(x^4)=-1/2$, and $\mu(1)=5/12$.

Completed results require actual module builds, `lake build ZetaFive`, an axiom audit, and independent mathematical review. The brief excludes `sorry`, `admit`, added axioms, and `native_decide` in completed lemmas. It permits the usual `propext`, `Classical.choice`, and `Quot.sound` dependencies. Explicit hypotheses must not simply assume the correspondence being claimed.

The analytic integral representation, convergence, local valuation estimates, energy certificate, symmetric square-root normalization, eigenvalue claims, and quantitative root exclusion remain separate obligations unless individually proved. Finite Python checks support the exposition and help detect errors; they do not satisfy Lean acceptance requirements.

## Reviewed checkpoint

The candidate branch is [`codex/zeta5-correspondences-2026-11-14`](https://github.com/dozenalist/Mathathon/tree/codex/zeta5-correspondences-2026-11-14). The reviewed source checkpoint was [`909d07fa25797e44c0ee9e2c7e0b8f6e7cc90af8`](https://github.com/dozenalist/Mathathon/commit/909d07fa25797e44c0ee9e2c7e0b8f6e7cc90af8).

| Evidence in the completed review | What it establishes |
| --- | --- |
| Independent supervisor inspection found a substantive polynomial μ–τ transport proof from independent definitions. | A meaningful candidate correspondence proof, with its stated domain. |
| The first checkpoint reported elaboration of 20 declarations under Lean/Mathlib 4.33.1. | Historical build evidence; it did not meet the pinned version requirement. |
| Later VM evidence showed Lean 4.35.0, retrieval of 9,031 matching Mathlib cache files, and `lake build ZetaFive` returning `LAKE-EXIT=0`. | The existing six-module library built in the required environment. This was recorded in the [16:11 PST response](../ChatLogs/2026-11-14_16-11-02_PST_01a1dc21.md). |
| A 4.35.0 axiom audit, independent mathematical review, early functional identities, and representation/parameter/Gram bridges remained pending. | The complete assignment was not accepted as finished. |

The successful build used task-local `ELAN_HOME/bin`, cleared `LEAN_PATH`, and captured the pipeline status immediately. Mathlib's recorded revision was `56a005855ea17e0b0958f73ec801ae140b0a1679`. The build evidence resolved the version blocker; it did not resolve the mathematical obligations. The checkpoint was not merged into `main` in the reviewed history.

## Research coordination decisions

The owned SAIR session was **Formalize zeta 5 parallel constructions**, `chat-b81e1f1139`, in the existing ZetaFive project. The user requested DeepSeek workers through Ultramath. The reviewed launch created four DeepSeek V4.1 Flash workers with max reasoning in swarm `smwh2nngu`. A confirmed launch is evidence of work starting, not of completed proofs or independent review.

The initial block was 90 minutes, with a first checkpoint around 4:41 p.m. PST on 14 November 2026. Monitoring was configured through **7:11 p.m. PST that day**. These are historical run settings, not an assertion that monitoring is still active. The estimate of another one to three hours concerned a reviewed first set of early lemmas; no reliable completion estimate was given for the entire analytic framework.

Follow-up work belongs to the existing coordinator and should preserve completed later work while prioritizing earlier dependencies. Match completion callbacks to the assigned project, session, and completion sequence, and check whether the follow-up was already delivered. The reviewed duplicate callback did not justify a second assignment. Verify actual worker evidence before labeling a role an independent reviewer.

## Repository and credential handling

The repository is [dozenalist/Mathathon](https://github.com/dozenalist/Mathathon), and its ζ(5) folder is `ZetaFive`. A local project directory and the GitHub repository are separate working locations. Git read and push access were verified in the source chat. The GitHub connector's write was rejected in that earlier chat, while authenticated Git succeeded; repository notes were therefore published through Git.

SAIR's Model API key and Platform API key serve different purposes. The formalization session required the Platform API. Setup succeeded through the API after a local masked prompt stored the credential with Windows account encryption outside the repository. Credential values, private inputs, raw callback records, and machine-specific authentication material do not belong in this archive.

For continuing the research, use the existing [supervision guide](../../ASTRA.md), [formalization brief](../Lean/PARALLEL_CONSTRUCTIONS_TASK.md), and current [progress record](../PROGRESS.md). This consolidation does not launch, reassign, or stop any SAIR work.

## Source coverage

Source chat: **Find how to share a GitHub repo**, Codex ID `01a1dc21-5c33-7b31-b7cd-c913a53b5390`. All **11 turns across two history pages** were reviewed through the latest completed turn, `01a1dc88-680c-78d2-b1be-a23fd4a42fb5`. Setup-only exchanges are condensed above; final corrections take precedence over earlier provisional status reports.
