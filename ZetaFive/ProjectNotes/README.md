# Zeta 5 project notes

This folder consolidates the useful results of the **Zeta 5** project chats through **14 November 2026 (America/Los_Angeles)**. It includes the completed explanations, corrections, unsuccessful extensions, exact computations, editable reports, and formalization decisions that were spread across those chats.

The central distinction is between understanding the determinant argument and verifying every bound it needs. The elementary irrationality implication is conditional on suitable integral polynomials with positive, sufficiently small values. The ζ(7) and ζ(9) investigations preserve useful algebra and positivity but expose arithmetic obstructions in the specified transfers. The Lean correspondence work remains a separate, partially completed project.

## Start here

| Note | Contents |
| --- | --- |
| [Proof and bounds](PROOF_AND_BOUNDS.md) | The irrationality criterion, Hankel and Gram representations, Andréief, Sections 8–11, arithmetic corrections, and remaining proof obligations. |
| [Parallel constructions](PARALLEL_CONSTRUCTIONS.md) | How the functionals, residues, matrix pencils, normalizations, and classical interpretations connect; what is already in the source. |
| [Extensions](EXTENSIONS.md) | The ζ(7) counterexample and failed repairs, Eisenstein and modulo-four distinctions, and the conditional ζ(9) draft. |
| [Formalization and workflow](FORMALIZATION_AND_WORKFLOW.md) | Source order, independent definitions, domain requirements, Mathlib reuse, reviewed build status, and research coordination decisions. |
| [Chat coverage](CHAT_INDEX.md) | Every project chat reviewed, its contribution, and the one unavailable historical PDF. |
| [Reproduction guide](REPRODUCIBILITY.md) | Artifact layout, dependencies, commands, integrity manifest, and verification scope. |

## Reports and editable sources

| Artifact | Reading copy | Editable source |
| --- | --- | --- |
| Whole irrationality argument | [PDF](artifacts/ProofOverview/zeta5_irrationality_overview.pdf) | [TeX](artifacts/ProofOverview/zeta5_irrationality_overview.tex) |
| Parallel constructions in Lai Sections 1–7 | [PDF](artifacts/ParallelSections/lai_parallel_constructions.pdf) | [TeX](artifacts/ParallelSections/lai_parallel_constructions.tex) |
| Revised unified framework | [PDF](artifacts/UnifiedFramework/zeta5_unified_framework.pdf) | [TeX](artifacts/UnifiedFramework/zeta5_unified_framework.tex) |
| ζ(7) transfer audit | [PDF](artifacts/Extensions/output/zeta7_argument_audit.pdf) | [Report builder](artifacts/Extensions/build_report.py) and [derivations](artifacts/Extensions/algebra_notes.txt) |
| ζ(9) formal analogue | [PDF](artifacts/Extensions/output/zeta9_formal_analogue.pdf) | [TeX entry point](artifacts/Extensions/zeta9_draft/zeta9_formal_analogue.tex) |

The revised unified framework is a separate snapshot. The earlier [formalization input and manifest](../Literature/ParallelConstructions/README.md) remain intact so that historical proof assignments retain their exact source. Likewise, the extension artifacts retain their original status labels and historical notes; the topic notes explain which later results supersede earlier statements.

## Relationship to existing repository material

The [proof overview](../PROOF_OVERVIEW.md), [expanded proof guide](../ProofGuide/01_IRRATIONALITY_CRITERION.md), [exponent catalog](../EXPONENT_CATALOG.md), [literature survey](../Literature/EXPOSITION_AND_EXTENSIONS.md), [formalization brief](../Lean/PARALLEL_CONSTRUCTIONS_TASK.md), and [progress record](../PROGRESS.md) remain the established project references. This folder adds the later chat results and the previously local artifacts without duplicating those guides or changing their historical claims. The [earlier chat summary](../ChatLogs/2026-11-14_research_chat_summary.md) is a historical snapshot; some discussions marked pending there are completed here.

The archive is organized by subject rather than as raw transcripts. It retains useful negative results, corrections, provenance, and reproduction instructions. Credentials, private setup inputs, raw tool payloads, caches, temporary builds, duplicate ZIP bundles, and unrelated chats are excluded. Third-party manuscripts are identified by version, URL, and available hashes rather than republished here.
