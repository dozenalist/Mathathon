# Kepler Conjecture: what the project has accomplished, and what remains open

Prepared November 14, 2026, Pacific time. This account consolidates the independently reviewed checkpoint of 08:23 Pacific and distinguishes it from later worker commits inspected around 09:00. It is intended for a reader who wants to understand the project without reading its code or technical claim ledgers.

**The project has built a useful research foundation, checked several concrete mathematical examples, and exposed important errors in proposed arguments and software. It has not produced a simpler proof of Kepler's theorem or an improvement over the established packing bounds discussed below.** The main geometric ideas still require substantial new proofs. Some newer implementations address earlier defects, but they have not yet earned the stronger claims made in their working reports.

At the user's request, the recurring 45-minute check-ins have been paused. Sair-Watch remains stopped. This is a publication and explanation checkpoint, not a declaration that the mathematical project is complete. No new SAIR research assignments were sent while preparing it. Previously assigned work was not interrupted.

## 1. The question we are trying to answer

Imagine filling a large box with identical solid balls. The familiar arrangement of oranges in a grocer's display fills about 74.048% of the available space. Kepler's theorem says that no arrangement of equal balls in three-dimensional space can do better in the large-scale limit. The exact fraction is pi divided by the square root of 18, approximately 0.740480489693.

This theorem is already known. Thomas Hales proved it, and the Flyspeck project subsequently formally verified a proof. Our task is to find a proof that is easier to understand, or a useful proved component that could reduce the complexity of such a proof. Recreating a complicated argument with new notation would not meet that aim. Nor would obtaining a short formula whose difficult assumptions have merely been moved elsewhere.

There are two principal sources of inspiration. Hales studies the geometry around individual balls and accounts for how unusually crowded regions must be balanced by other regions. Cohn and Elkies use specially chosen functions to turn packing restrictions into an upper bound on density. Viazovska's work in dimension eight, and the related result in dimension twenty-four, show how remarkably effective that second approach can be in special dimensions.

The project studies both approaches and possible combinations. Three dimensions remain the main test. A proposal that looks elegant on paper must actually give useful three-dimensional information before it is promoted as progress toward the goal.

## 2. A short account of the present state

| Part of the project | What has been accomplished | What has not been established |
| --- | --- | --- |
| Research plan and literature | A structured roadmap, source catalogue, precise theorem references, selected papers and review of recent Hexagon material | A newly discovered short proof in those sources |
| Function-based bounds | Reproducible numerical controls and several independently checked exact examples | A new best bound, or an exact Kepler proof by this route |
| Local geometry | Explicit test configurations, checked special-case volumes and useful obstructions to proposed arguments | A quantitative inequality covering every legal local configuration |
| Balancing crowded and uncrowded regions | Conditional mathematical statements and finite graph tests | Proof that the necessary balancing inequalities hold for every sphere packing |
| Verification software | Independent checks, reproducible failures and targeted repairs | A generally sound geometric certificate checker whose full guarantees have been established |
| Formal proof in Lean | A locally compiled algebraic normalization identity | A formal proof of the geometric or global packing argument |
| Publication and supervision | Preserved source revisions, review records, failed claims and a consolidated account | Continuous work for a full hour on every assignment; this was a requirement, not an established fact |

The most accurate description is **a research foundation with verified components and clearly identified gaps**. The gaps are mathematical, as well as computational. More computing time alone does not settle them.

## 3. What the literature work clarified

The literature collection records 17 sources and includes four selected primary-source PDFs. It links the original local-volume criterion in Hales's proof to the Cohn–Elkies method, the dimension-eight and dimension-twenty-four proofs, and stronger methods that consider more than pairs of sphere centers. The collection includes precise locations for the statements used. Checking a cited passage is different from independently reproducing an entire published proof; the source records make that distinction.

One especially important finding constrains the research strategy. A result of Rupert Li shows that the ordinary Cohn–Elkies method cannot reach the exact three-dimensional Kepler density. In everyday terms, a method that only uses that particular kind of pairwise information leaves unavoidable room above the true answer. Choosing a more beautiful function within the same framework does not remove this obstruction.

This does not make analytic functions useless. They can provide understandable weaker bounds, dependable controls for software, or ingredients in a stronger argument. But a proposed exact proof must explain what additional information it uses. Local geometric restrictions or constraints involving triples are possible sources of that information; neither becomes sufficient merely by being added to a formula.

The literature review also checked recent LLM-associated material, including Hexagon. The reviewed magic-function proposal did not supply all the global sign arguments needed to replace the established proofs. Higher-dimensional work remains a possible source of ideas, not an accepted three-dimensional solution. The project has not treated a claim on an LLM research site as established simply because it was posted there.

Another clarification concerns a classical geometric theorem. A theorem of Fejes Tóth, restated in Hales–McLaughlin, supplies a volume lower bound for a polyhedron with at most twelve faces containing the unit ball. That is an imported result, not a theorem discovered by this project. The full Hales–McLaughlin theorem about packing cells has a different scope. Confusing these statements led to misleading claims about what had already been proved; their distinct roles are now recorded.

See the [literature index](Literature/README.md), [core sources](Literature/CORE_SOURCES.md), [Hexagon review](Literature/HEXAGON_REVIEW.md) and [twelve-face source audit](Literature/TWELVE_FACE_SOURCE_AUDIT.md).

## 4. The function-based work: reliable controls, but no stronger result

The function-based method associates a numerical bound with a function satisfying several conditions. Two conditions are essential: one constrains the function itself, and another constrains its Fourier transform, which is a way of describing the function in terms of frequencies. Both must hold everywhere in their required ranges. Checking a long list of sample points is useful, but a failure between those points can invalidate the bound.

The project's first optimizer omitted the entire Fourier-positivity condition. Its output therefore could not support its claimed conclusion about the limitations of grid searches. Independent local execution exposed the omission, and that conclusion was withdrawn. This was a useful negative result about the implementation, not evidence that the mathematical method had failed.

A separate implementation included both conditions. Increasing the resolution changed a reported value from roughly 0.77970245 to 0.77974877. Another run gave about 0.77974577. Those numbers sit near the published ordinary Cohn–Elkies benchmark of about 0.779747, but small sign violations remained. The slightly smaller number is consequently **not** an improvement in a rigorous upper bound. The saved inputs and outputs allow the experiment to be reproduced and its limitations inspected.

The project also produced stronger evidence than sampled output: several specific certificates were reconstructed independently using exact arithmetic. Here a certificate means a concrete collection of polynomials, rational numbers and sign checks from which the bound can be verified under the established Cohn–Elkies theorem.

| Example | Reviewed outcome | Meaning |
| --- | --- | --- |
| K33b control | Approximately 0.77996622; separate strict-checker and symbolic checks passed | A checked control, weaker than the published ordinary benchmark |
| Counterexamples' X-C014 | A directed exact comparison proves a bound below 0.780718153344 | An independently reconstructed specific certificate |
| Compact matrix certificate C017 | A directed exact comparison proves a bound below 0.782267254857 | A smaller certificate with some loss of numerical strength |
| Fine-grid numerical output | Approximately 0.77974577, with sign violations | An experiment, not a certified bound |
| Kepler target | Approximately 0.740480489693 | The already known exact answer that a simpler proof must recover |

Smaller upper bounds are stronger. All the certified project examples in this table are weaker than the published ordinary control, and that control is itself well above the Kepler value. These results are valuable as reproducible examples and tests of the machinery. They are not new records in sphere packing.

The compact certificate is an understandable improvement in presentation: the largest rational matrix entry was reduced from 563 characters to 41, with a small loss in the bound. This is an actual simplification of one certificate. It should not be described as a simplification of the complete Kepler proof.

A proposed hybrid experiment allowed the auxiliary function to be slightly positive in a narrow distance range, with a geometric limit on the number of nearby centers intended to pay for that allowance. The tested instance did not establish a useful gain. The general lesson is that an appealing reformulation still needs valid hypotheses and demonstrated three-dimensional strength. More recent files continue this exploration, but no stronger hybrid bound is accepted here.

Details and exact checks are in the [03:08 review](Main/REVIEW_2026-11-14_0308.md), [04:38 review](Main/REVIEW_2026-11-14_0438.md) and their linked local logs. The comparison values from published work are collected separately in the [source record](Literature/CORE_SOURCES.md).

## 5. The geometric idea: small cells must be paid for elsewhere

For each ball center, imagine assigning to it every point of space closer to that center than to any other. The resulting region is called its Voronoi cell. These cells divide space without overlapping interiors. The ball occupies part of its cell, so the average cell volume is closely related to packing density.

For balls of radius one, the Kepler density corresponds to an average cell volume of 4 times the square root of 2, about 5.656854. It is tempting to try to prove that every individual cell is at least this large. That is false. A legal local arrangement can produce a smaller cell.

A particularly important example has twelve neighbors arranged in an icosahedral pattern around a central ball. Its central cell is a regular dodecahedron, with volume about 5.550291. This is smaller than the desired average. The surrounding configuration cannot simply repeat everywhere with every ball enjoying that same favorable cell. The difficulty is to turn that incompatibility into a quantitative proof.

The project's local strategy is therefore an accounting scheme. A cell smaller than 5.656854 has a deficit; a larger cell has a surplus. One tries to show that neighboring surpluses always compensate for deficits, using rules whose total correction contributes negligibly when a very large region is considered. This is closely related to Hales's starting criterion. The hoped-for advance would be a much simpler compensation rule with a complete proof.

Conditional results describe when such accounting can be done on a network of neighboring centers. For a finite network, one can test whether the available transfers can cover every deficit. Reviewing those statements and checking finite examples is useful. The decisive missing step is to show that **real sphere-packing geometry always supplies the required inequalities**. A theorem saying that compensation works if sufficient compensation is available is not yet the geometric theorem we need.

There has nevertheless been concrete progress in making the idea testable. The project constructed a periodic, rational-coordinate example with a genuine positive central deficit. Its central cell volume is approximately 5.554454804529. Exact coordinate and separation checks established the relevant local configuration. A second exact volume formula, applied to the saved boundary data, later reproduced the stored value; this is a consistency check, not independent validation of the complete geometric description. A twelve-edge transfer graph gives a threshold near 0.00853328708 for that particular test, conditional on its volume inputs.

This example provides something earlier arguments lacked: an actual configuration with a positive deficit. An earlier claimed universal transfer floor had used an upper bound on deficit as if it were a lower bound. Independent review refuted that inference and retained the counterargument. The explicit example repairs the evidentiary starting point for a narrower test. It does not show that the proposed rule works for all packings. The example is sparse and unsaturated: more balls can be inserted. It is not an example of a dense packing attaining a new extremum.

Exact special-case checks for the standard face-centered-cubic and hexagonal-close-packed arrangements reproduce the expected cell volume 4 times the square root of 2. These are useful equality controls. They do not prove that every other arrangement has at least the same average.

## 6. What the local geometric investigations have taught us

Several lines of work examine whether cells close to the unusually small dodecahedral cell force a compensating cost nearby.

**Two small cells near one another.** The agents studied the constraints on placing two exact dodecahedral cells close together. Cross-distances between their neighboring sphere centers can rule out proposed placements. Calculations for specific orientations and a conditional argument using how well the neighbor directions cover the sphere offer useful information. However, claims about all relative rotations require more than testing a selection of orientations. Some formulas and endpoints were wrong and were corrected. A weakening that tried to discard the assumption on the second cell was also invalid: one dodecahedral central cell can have legitimate touching neighbors.

**Moving selected cell faces outward.** Another proposal estimates how much a cell's volume grows when some of its bounding planes move away. The twelve-face theorem supplies a starting volume in an appropriate restricted setting. The rest of the argument needs a lower bound on the area of the actual moving face throughout the motion, taking every competing plane into account. An area in the surrounding plane is not automatically an area inside the cell. The agents have worked on this distinction and reported repairs, but the complete uniform argument has not been accepted in this checkpoint.

**Cells with more than twelve faces.** A proof restricted to twelve faces leaves a serious gap. Additional neighbors can create additional faces. Counting neighbors in one chosen distance range does not automatically control all faces of a cell. Nor does exhibiting a nice polyhedron with thirteen faces prove the minimum volume among all such cells. The project explicitly withdrew an inference from candidate examples to statements about true minima. Later work reports a concrete obstruction to a proposed counting shortcut; that report is preserved as newer, unreviewed work below.

**Cells that are almost regular.** A stability argument would say that a cell which differs noticeably from the smallest regular example must pay a definite volume penalty. Numerical second-derivative calculations suggested possible local estimates, but some constants were wrong and were corrected. Rotation is a particular difficulty: rotating the same cell changes its coordinates without changing its shape or volume. A valid estimate must measure genuine distortion rather than charge for a harmless rotation.

Removing directions corresponding to tiny rotations in a numerical calculation is not automatically a complete treatment of finite rotations. Even a correct estimate for very small distortions would leave another question: why must every relevant low-volume cell lie in that small neighborhood? Changes in the set of active faces must also be controlled. These are separate proof obligations, not finishing details.

Bounded local searches did not find a counterexample to one proposed pair-volume target. Across eight small search pilots, the best value was about 5.898007181, above the tested target of about 5.763417470. That is a finite experimental outcome. It neither proves the target nor establishes the true minimum over all allowed configurations.

## 7. Checking the checkers has been a substantial part of the work

A computer output becomes mathematical evidence only to the extent that its meaning is understood and its verification is reliable. The project has repeatedly found that a program labeled “exact” or “certified” still relied on an unchecked assumption.

One proposed analytic certificate near 0.78010544 failed an independent exact sign check. Its verification program also ignored failures when logging was disabled. Both the original input and the precise rejection were preserved. A quiet program completing successfully was not evidence that its mathematical conditions held.

The geometric software has had a similar progression. Earlier versions had problems with normalization, boundedness, face duplication and error allowances around floating-point geometry. Some named repairs now pass focused controls. For example, Experimental's duplicate-plane repair passed the supervisor's cube, rescaling, redundant-plane and standard-packing checks at the 08:23 review. That closes a particular defect; it does not prove every guarantee of the larger interval calculation.

The clearest remaining warning at that review concerned Computation's standalone volume-certificate checker. Its own 25 tests passed, and a second formula reproduced the stored example's volume. Nevertheless, independent adversarial inputs made it accept two wrong answers:

* A cube of true volume 8 was declared to have volume 16 by duplicating its face list.
* An extra constraint cut a cube down to volume 6, but the certificate omitted that constraint from an internal candidate list and the checker accepted volume 8.

These failures do not imply that the stored central-cell volume is wrong. They show that the general claim “the checker can verify the answer without trusting the producer” was false at the reviewed revision. Agreement between two volume formulas cannot fix a description that silently omits part of the intended region.

Later Computation commits add checks aimed at these attacks. They are real implementation changes, but their complete correctness remains unproved. In particular, verifying that every listed face is genuine is different from verifying that every genuine face has been listed. Repeated or malformed boundaries inside a face also need attention. The overview therefore credits targeted repairs without declaring the generic checker sound.

This adversarial work is a significant project accomplishment. It has prevented several false results from becoming accepted conclusions and supplies concrete regression cases for future development. It is also evidence that stronger claims must be made cautiously.

## 8. What has been formally verified

One algebraic normalization module was compiled locally in Lean 4.35, a proof assistant that checks formal deductions. Its targeted imports and reported axioms were inspected. This is a genuine, narrowly scoped formal result.

It is not a formalization of sphere-packing geometry. It does not establish the ball-volume formula, the connection between counting centers and occupied volume in the large-scale limit, or the proposed local-to-global argument. Later formalization attempts reached their bounded resource limits; those runs were not counted as completed proofs.

The benefit so far is a checked piece of algebra and an established local build workflow. The remaining formal work would need a stable mathematical argument worth formalizing. A proof assistant cannot supply missing geometric premises simply because a normalization identity compiles.

See the [Lean review](Lean/Review/README.md).

## 9. Newer pushed work: implemented, but not yet accepted

The mathematical acceptance decisions above are anchored to the 08:23 supervisor review. During preparation of this overview, the later immutable worker revisions listed below were fetched and their relevant source changes inspected. They remain available on public worker branches. Their full contents are not silently substituted for the reviewed checkpoint published here.

* **Main now supplies the previously missing stability pilot**, `Computation/l1_remainder.py`, with a bounded local-run handoff. It requires two rigorous inputs: a lower bound for a quadratic term and an upper bound for a higher derivative. Decimal command-line inputs do not prove those assumptions. The implementation uses floating arithmetic, and source inspection raises an additional problem in how rotation directions are selected. Some accompanying prose also retains inconsistent thresholds and an unsupported claim connecting twelve normals to a thirteen-face case. The correct status is an implemented pilot awaiting correction and validation, not a completed stability certificate.
* **Computation adds checks for the two wrong-volume examples**, membership in the complete constraint list, unique face planes and a rank condition. New test cases and an independent-checker update accompany these changes. The full boundary-completeness argument still needs review; no general checker theorem is accepted. A new radius-family calculation and saved certificates for an existing three-cell periodic test configuration are also present but were not independently validated for this overview.
* **Experimental reports further face-area arguments and an obstruction to a counting shortcut for thirteen-face cells.** These are substantive proposals. They do not establish the universal volume inequality. Even the new explanation of plane normalization needs care: rewriting a plane's right-hand side as 1 does not make its Euclidean distance from the origin equal to 1 unless its normal has length 1.
* **Counterexamples supplies additional audits and scoped separation calculations.** The distinction between a proved exclusion distance for a particular argument, an exact threshold in a restricted family, and the optimum over every rotation remains essential. Its additional numerical and geometric claims are not promoted to supervisor acceptance by inclusion in this source list.

| Role | Later revision inspected | Public source |
| --- | --- | --- |
| Main | `08692b37e1808579512ea25d4c0f06821f95c54e` | [Immutable tree](https://github.com/dozenalist/Mathathon/tree/08692b37e1808579512ea25d4c0f06821f95c54e/KeplerConjecture) |
| Computation | `b61f175cc18319a0afbb534547b16d0a14204ba3` | [Immutable tree](https://github.com/dozenalist/Mathathon/tree/b61f175cc18319a0afbb534547b16d0a14204ba3/KeplerConjecture) |
| Experimental | `0c15232ea4893ea92b1e6d46c00bd3dd3552c5ce` | [Immutable tree](https://github.com/dozenalist/Mathathon/tree/0c15232ea4893ea92b1e6d46c00bd3dd3552c5ce/KeplerConjecture) |
| Counterexamples | `72936410e1ae11bc853a9acf0e575f6332f382c2` | [Immutable tree](https://github.com/dozenalist/Mathathon/tree/72936410e1ae11bc853a9acf0e575f6332f382c2/KeplerConjecture) |

The live read-only snapshot around 08:57 Pacific showed Main and Experimental still active, and Computation and Counterexamples having completed their latest turns. All four latest recorded model calls used Ultramath. No follow-up was sent as part of this documentation request. These observations are a dated snapshot, not a promise of continued monitoring or a claim about what the chats are doing when this document is read.

## 10. The work still needed for a simpler Kepler proof

The main unfinished tasks can be stated without the project's internal claim numbers.

1. **Choose and prove a useful local rule.** Specify exactly which neighboring configurations are covered and prove an inequality with sufficiently strong constants. Include awkward orientations, extra faces, limiting configurations and equality cases. A sampled minimum does not meet this requirement.
2. **Show that local deficits are always compensated.** The geometric rule must imply the entire family of balancing inequalities needed by the accounting method. A successful example or a conditional network theorem is insufficient.
3. **Make the passage to the whole packing valid.** Control what happens near the boundary of large regions, justify any saturation or periodicity assumptions, and cover arbitrary infinite packings rather than only repeating examples. Several preliminary counting arguments have been repaired, but the entire bridge is not accepted.
4. **Close the stability gaps if that route is retained.** Treat rotations correctly, prove uniform derivative bounds, control changes of faces, and justify entry into the neighborhood where a local estimate applies. State exactly which parts depend on imported geometric theorems.
5. **Make computer certificates independently trustworthy.** Prove that the checker examines the intended complete object, rejects malformed certificates and uses justified arithmetic bounds. Then recheck every result that depends on a repaired verifier. Passing a small regression suite is necessary evidence, not a proof of universal correctness.
6. **Demonstrate genuine three-dimensional strength for analytic hybrids.** Account for all added hypotheses and compare with existing methods on an actual valid instance. A construction inside ordinary Cohn–Elkies alone cannot overcome the known obstruction.
7. **Explain and measure the simplification.** A successful argument should show what difficult case analysis, numerical workload or machinery it removes. It should not rely on a comparably difficult imported theorem without acknowledging that dependence. Formal verification can then strengthen confidence in a stable argument.

These are possible directions for a future resumed effort, not newly issued assignments. No single one is described as “the only remaining step.” The project's current evidence does not justify that description.

## 11. How to read the repository and judge its claims

The repository contains working research, not just final results. It deliberately preserves failed attempts, old code, agent reports and corrections. A historical file may still say “proved” next to a claim that a later review rejected. That label alone is not the current project verdict.

Use this overview for the consolidated assessment. The [cumulative progress record](PROGRESS_SUMMARY.md) gives the developing narrative, while [technical progress](PROGRESS.md) and [supervisor reviews](Main/) provide exact statements and evidence. The [08:23 review](Main/REVIEW_2026-11-14_0823.md) is the last completed independent research review used here. Its [local checks](Main/LocalChecks/2026-11-14_0823/README.md) document what was actually executed. The [roadmap](ROADMAP.md) describes objectives rather than achievements.

Four distinctions matter throughout:

* A **working claim** is an argument or result proposed by an agent.
* A **finite numerical test** says what happened for the tested inputs and numerical settings.
* A **checked specific certificate** establishes the stated finite object or bound under its recorded mathematical assumptions.
* A **general theorem** must cover every configuration in its stated domain. A proof of a special case, a software test or a plausible extension is not enough.

The publication merges the supervisor checkpoint `872fa211ecc827c8d78f0c302c1f99c882cbd590` into a checkout based on the existing GitHub main branch, retaining the research authors' Git history. The source revisions behind that checkpoint are listed in [SYNC_2026-11-14_0823.json](Main/SYNC_2026-11-14_0823.json). The later commits above are explicitly separate, unvalidated inputs. Changes for this publication are confined to KeplerConjecture; other Mathathon projects are preserved.

The lasting value of the work so far is a better-defined problem, reproducible examples, several checked certificates, and a much clearer map of where attractive arguments fail. The desired simpler proof remains open within this project.
