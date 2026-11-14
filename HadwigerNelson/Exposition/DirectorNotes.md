# Exposition direction and continuity

The user appointed this chat exposition director on 14 November 2026. Scope: coherent mathematical synthesis, useful explanation tools, source-linked GitHub organization, independent Astra and substantial Claude participation, research feedback, and clear final deliverables.

**Publication scope:** the user subsequently required all committed exposition work to stay within the GitHub folder `HadwigerNelson/`. The packet now lives at `HadwigerNelson/Exposition/`; its earlier top-level location and root README were removed from the unpublished checkpoint. Keep future reports, slides, tools and source copies within this folder. The approved Claude input walkthrough is the same file relocated here; historical references to `Exposition/ProofWalkthrough.md` describe its original location.

User preferences confirmed in this chat: weave visual clarity, intuition, energy, and rigorous precision into one exposition. Give **hourly showcases of built material**. Reserve separate research-progress briefings for **major contributions**. Focus on explaining mathematics now; defer team identity and official submission details until the end. Do not ask those questions again during the explanatory work.

## Current teaching sequence

1. Proper versus weak measurable colourings and the two bridges of the supplied proof.
2. Density points: why almost-everywhere restrictions can force exact exclusions.
3. Connected-set straddling, shown by the unit-distance contact model.
4. Constructed two-label interfaces, their common-centre geometry, and CC60.
5. Three-centre palette contradiction and the relationship to the original state machinery.
6. A final proof map in which the reader can explain what each lemma contributes.

Use independent Claude roles for mathematical criticism, worked examples, and reader testing; accept actual outputs only after checking them against primary sources. Keep raw reasoning streams, credentials and runtime logs outside Git. Current dedicated exposition work uses `.scratch/exposition-claude/`; the main research supervisor owns a separate Claude queue. Do not mutate that queue.

The user explicitly approved exporting these three files to the Claude subscription for the two prepared first reviews: `Exposition/ProofWalkthrough.md`, `HadwigerNelson/Main/ResearchSnapshot/local/outputs/cone/ConeObstruction.lean`, and `HadwigerNelson/Main/ResearchSnapshot/local/outputs/MC120-ENDPOINT-CORRECTION.txt`. The approval followed a host-network auto-review block; initial sandbox attempts failed DNS with zero model tokens. Preserve that distinction in the review receipt. This scoped approval does not silently include additional private files. Public mathematical prompts and future source-export decisions should follow their actual authorization.

First review outcome: both broad high-effort requests reached 600-second caps without completed reports. Focused medium-effort geometry and skeptical-reader requests then completed in about 31 and 40 seconds and supplied checked improvements. Prefer sharply bounded review questions that yield usable explanations. The completed findings and answer hashes are in Reviews/Claude-FirstReview.md; all exposition Claude jobs from this work block have finished.

## Coordination

| Responsibility | Chat or location |
| --- | --- |
| Exposition director | `01a1db69-9bd7-75d2-8684-8efaa81d0cb9` |
| Active Hadwiger–Nelson research supervisor | `01a1d859-70aa-7eb1-a383-caf2f202642a`; workspace `C:/Users/jarom/Documents/Codex/2026-11-13/i` |
| Research archive integration | `01a1db41-f0fb-71a1-8364-ce430cac59e0` |
| Prior progress assessment | `01a1db58-c06f-7d11-a4f4-f94ef09aa518` |

The user explicitly authorizes communication with research agents and subsequently required **minimal cross-chat interaction**: contact another chat only for a genuinely important correction, an essential missing fact, or a handoff that materially changes the work. Prefer existing source artifacts. Do not send routine coordination, acknowledgements, duplicate progress messages or messages for their own sake. Preserve research ownership. Serialize Git operations in the shared checkout, stage only owned paths, and confirm pushes; coordinate with another writer only if a real concurrency or ownership issue requires it. Do not switch branches under other workers or sweep their local files into a commit.

## Quality and eventual handoff

Each teaching artifact should give a reader a new inference they can make, not merely a list of tasks performed. Keep exact hypotheses beside claims. Distinguish inherited results, team proofs, computations over finite domains, pending integrations and heuristic pictures. Keep the proof-source pins in SourceMap.md and update dated evidence only after review.

The official [judging guidelines](https://github.com/SAIRcompetition/mathathon-judge/blob/main/rules/judge-guidelines.md) reward correct explanations, motivation, interest and honest attribution. Our reader questions should exercise definitions, the key mechanism, contribution and certainty.

Before the November 15 noon Pacific deadline, assemble the strongest honest synthesis as a self-contained report source and PDF, PDF slides, and linked supplementary tools with a fixed repository revision. The [submission guidelines](https://github.com/SAIRcompetition/mathathon-judge/blob/main/rules/submission-guidelines.md) require all slide results to appear in the report and figure content to be explained in words. Source Lean 4.34.1 checks are historical evidence; the event's optional Lean submission requires its specified 4.35.0 environment. Do not label that migration completed without validation. This is a future handoff, not a claim that the current teaching packet is a submission-ready report or slide deck.

Prioritize mathematical explanation in current work. On November 15 begin final synthesis by 08:00 Pacific, freeze accepted claims by 10:00, and aim for a reviewable package by 11:00. These are internal working targets, not changes to the event deadline. Official selection and submission remain with the human team.


## Canonical reader and pacing: 14 November, 12:00 showcase

The user's latest correction is now the governing editorial direction: **one clear reading surface, understanding before comprehensiveness**. Develop <code>ProofWalkthrough.md</code> in place. The README should give it one prominent link; other artifacts are supporting references, not competing starting points. Do not create a new reader or showcase document merely to mark another hour.

The current main lesson motivates weak measurability through a unit-ruler score, an angular fraction and a disk average before expanding indicators and assembling the manuscript formula. Three static figures and a deliberate 16-second turn support those steps. The animation is optional and the static explanation is complete. The remainder of the old proof map is expandable below the lesson.

The next editorial priority is the bridge from density to exact exclusion. Retain slow transitions, a worked example, a place to pause and a concrete reader check. Do not treat the existence of sliders, an animation, or a correct formula as evidence that a concept is clear. Each visual should enable a specific inference and have a verbal explanation. Ask for feedback about the first sentence or picture where the reader loses the thread.

This showcase used one Astra audit and two completed focused Claude reviews of self-contained public mathematical prompts. The director checked and integrated their contributions; source-unsupported reviewer claims were rejected. Scope and receipts are in <code>Reviews/WeakColouringLesson-Astra.md</code>.


## Delegated production: latest user direction

The user now assigns the root agent exclusively to oversight: direction, ownership, deadlines, organization, publication and delivery. Claude is the lead producer and synthesizer. Use separate Claude instances for independent reader testing and mathematical criticism. OMM should perform substantial mathematical development and source work. Codex/Astra helpers may operate the runners and handle files, but must not substitute their own mathematical authorship for the delegated work. Preserve prior attribution; do not relabel already-written material as Claude's work.

The current walkthrough goes through a final Claude editorial and reader pass before publication. Claude also prepares the next OMM work assignment. Establish an exposition-owned OMM session in the existing Hadwiger–Nelson project, preserving other supervisors' sessions and queues. Other-chat interaction remains limited to material questions or handoffs.


Claude now has a persistent interactive **Mathathon Exposition Manager** session. The user confirmed that its interface is ready for direct instructions. Local operational handoffs live in `.scratch/exposition-claude/manager/`; consult its MANAGER-STATUS.md, READY.json and outbox before initiating new production tasks. A separate OMM worker received Claude's unchanged next-lesson brief with a one-hour bound; its ownership and collector are in `.scratch/exposition-omm/density-20261114/`. Preserve these sessions and avoid duplicate dispatch.
