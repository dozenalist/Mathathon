# Weak-colouring lesson: bounded source audit

14 November 2026. Read-only audit of the proposed lesson against manuscript Definition 1.2 and Theorem 1.3, and `ProperColoring` / `WeakColoring` in [Coloring.lean](../../Main/ResearchSnapshot/local/work/encoding-integration/full-original/OAI/Geometry/PlaneColoring/Coloring.lean). Manuscript text: [paper.txt](../../Main/ResearchSnapshot/remote/supervisor/simplify-exposition/notes/paper.txt). No builds or full-proof review.

**Verdict:** the staged score → angular average → disk average explanation is correct, with these qualifications.

1. Say “a finite collection of measurable colour classes partitioning the plane,” not “finite measurable colour classes,” which could suggest finite sets. Each point has exactly one label. Then the sum defining $m(p,u)$ is exactly 1 when the endpoint labels agree and 0 otherwise; it never double-counts.
2. Choose Borel representatives forming a partition before defining $s(p)$ for **every fixed** $p$. For arbitrary Lebesgue-measurable representatives, the angular restriction on a particular circle need not be measurable; Fubini only guarantees the needed sections almost everywhere. This subtlety need not interrupt the main lesson: “We use measurable representatives for which these samples are defined” can be accompanied by a short precise note saying Borel. The manuscript explicitly permits this choice. Lean uses `AEMeasurable` and the product-almost-everywhere condition.
3. Normalize direction measure: $d\sigma=d\theta/(2\pi)$. On a bounded positive-area disk $B$, choose $p$ uniformly and independently of the uniformly chosen direction. Only the **starting point** must lie in $B$; the endpoint can lie outside it. There is no uniform probability distribution on the whole plane.
4. $P_B=0$ for every bounded positive-area disk is equivalent to the manuscript's formula for all origin-centred disks $B(0,R)$: multiply by the positive area; conversely, nonnegativity and containment in a sufficiently large origin-centred disk transfer zero integral to any disk. Countable exhaustion by origin-centred disks also shows equivalence to zero bad score almost everywhere in position-times-direction measure.
5. Zero average means almost every tested pair passes, not every pair or every starting point. A single bad pair, or even positive $s(p)$ at one specified $p$, does not alone refute weakness. Plane-null modifications can change the entire angular test at an exceptional centre while leaving weakness unchanged.
6. The transfer theorem constructs a **new** weak measurable colouring from the existence of an arbitrary proper colouring. The original classes need not be measurable. Do not present this as directly integrating the original colouring or merely smoothing its indicators. A measurable proper colouring does immediately satisfy weakness, but that easy special case is not the unrestricted transfer theorem.

## Half-plane example checked

Let red mean horizontal coordinate $<0$ and blue mean coordinate $\geq0$. At $p=(-1/2,0)$ the starting label is red, and the endpoint is red exactly when $\cos\theta<1/2$. For $0\leq\theta<2\pi$, this is $\pi/3<\theta<5\pi/3$, an arc of length $4\pi/3$. Hence $s(p)=2/3$. At the two boundary angles the endpoint is blue; these angles have measure zero.

This is an intentionally invalid colouring, useful for seeing what the score measures. To demonstrate rigorously that it is not weak, choose a disk of radius $1/4$ centred at $(-2,0)$. Every start has horizontal coordinate below $-1$, so every unit endpoint remains red. Consequently $P_B=1$. This avoids the invalid inference that one exceptional centre would refute an almost-everywhere requirement.

## Two explanatory bridges

- Before writing an indicator product: “Put a unit ruler at $p$ and rotate it. For one chosen colour, the first switch asks whether the start has that colour; the second asks whether the endpoint does. Multiplying requires both switches to be on. Adding over colours records one match or no match.” Then introduce $m$ and rotate the half-plane example until the two crossing angles explain the $2/3$ fraction.
- Before the outer integral: “So far we have watched one pivot. Now slide that pivot uniformly around a bounded disk and average the fractions we just measured. The disk limits where we start, not where the ruler ends. Weakness says this final probability is zero in every observation disk.” Only then compress the two experiments into the displayed formula, and explain how nonnegativity prevents bad pairs from cancelling good ones.


## Focused Claude reviews and integrated lesson

Two tool-free Claude subscription requests, both Claude Opus 5.5 / medium, completed on 14 November 2026. They received self-contained mathematical prompts about the score and half-plane example, with no repository source files uploaded.

| Role | UTC start / finish | SHA-256 of final answer |
| --- | --- | --- |
| Pedagogical sequence | 20:10:30 / 20:11:05 | <code>377b4c4e828943b2eb9a6dcea5d0c1d7bf71e42bb4efc152c5cc559751bfe4f1</code> |
| Quantifiers and exceptions | 20:10:48 / 20:11:18 | <code>ac3a2d0d979ddd0f2fb2bd99223dc455913ed79c1e17607ef4346bd8ae1dd4c9</code> |

Accepted after checking: the yes/no indicator interpretation, the two normalizations, the half-plane fraction, the disk with probability one, and the warning that a single exceptional centre does not refute weakness. The final lesson also explains how editing a single point can destroy properness while preserving weakness.

Corrections to the returned reviews: a countable disk cover gives a global *almost-everywhere* condition, not pointwise success everywhere. Borel sets need not be geometrically well behaved. The skeptical review's lack of knowledge of the transfer theorem does not refute the supplied manuscript's Theorem 1.3. Its categorical claim about fixed directions was too strong: Fubini alone gives almost every direction, but the supplied proof has an additional continuity argument upgrading to every fixed direction. Neither overclaim was incorporated.

Astra subsequently read the actual integrated sections 1–7 and found no substantive mathematical error. Its final clarification was to use a proper **seven**-colouring in the null-edit example, so the example cannot be confused with assuming the five-colouring under discussion. The exposition director checked the final prose, links, figure geometry and renderings. These bounded checks do not reverify the entire proof.


## Final Claude managerial pass

After the user explicitly approved the revised primary lesson, two tool-free Claude Opus 5.5 reviews returned exact editorial and reader-test suggestions. The user then assigned Claude the managerial role. A persistent Claude Opus 5.5 manager integrated the accepted edits and used two independent Claude subagents: one checked the proposed exception example and related claims; another checked the whole lesson after integration. The manager reported READY, with no figure changes. It rejected an overstatement in the reader report rather than adopting the report wholesale.

The manager could not open source files outside its restricted directory or view a rendered GitHub preview; those are not claimed as its checks. The exposition overseer checked relative-link resolution and retained the separately completed figure rendering checks. No new full-proof validation is claimed. The manager's local READY receipt has SHA-256 `4c391cfaf8242632e1031b90d7eec879acf80af2db4043fd6436d2674457ce6c`.
