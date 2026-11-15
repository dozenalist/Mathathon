# Source coverage for parallel constructions

Reviewed on 14 November 2026 with the chat-history API, including all user and assistant messages. Both API responses reported `hasMore=false` and `nextCursor=null`. Original titles below retain the app's displayed ellipses. Tool logs and reasoning records were excluded from the publication material.

| Chat | ID | Coverage | Useful outcome |
|---|---|---|---|
| Find parallel constructions in the Zeta(5)… | `01a1dc1f-f2bf-7531-976e-7f07e6a19ab0` | All 4 turns, first correspondence request through final provenance correction | Correspondence dictionary, classical interpretations, audits/cautions, revised framework and corrected attribution |
| Draft parallel constructions for sections… | `01a1dc62-6e6c-73c2-a38a-de232fb0c764` | All 3 turns, initial sections 1–7 draft through whole-argument overview and correctness check | Six-page scoped draft; later five-page overview conditional on two stated estimates |

No user or final assistant message exceeded the API's 20,000-character message limit. The largest final message was 11,610 characters. Initial bulk tool output was clipped by the display; the stored structured responses were then parsed and each relevant message read without clipping. The public synthesis is `PARALLEL_CONSTRUCTIONS.md`; no raw chat transcript is proposed for publication.

## Retained artifacts and revision history

- The Sections 1–7 PDF, matching TeX, and original README are preserved under [ParallelSections](../artifacts/ParallelSections/). The six-page draft was independently reviewed and visually checked in its originating chat.
- The **revised** framework TeX and PDF are preserved under [UnifiedFramework](../artifacts/UnifiedFramework/). The existing `ZetaFive/Literature/ParallelConstructions/` snapshot predates the final provenance correction and remains intact as the earlier formalization input.
- The current framework TeX SHA-256 is `AA4D266A6CD21EC515E5290AD1A5F2A3B8734E842E00FCD3EE4AE10C59C91F72`; current PDF SHA-256 is `8A16B3B181D599F1329147E1FF3E894604C79DFBCA23E8394313C3C894E15A34`. Existing repository manifest values are respectively `31748E326DF2BAF9D741DE76DD557316C2F34A5BB577DAD15FBE922791141874` and `A5D7A775BA6ECA9D62F4826E3DC8F7D726A1C115967CF25EB4BE4D65C6435C14`.
- `framework_checks.py` is unchanged from the earlier repository snapshot (SHA-256 `6E2AEB2482ADF2D224A2C659429AC06F619591C680FBF1471C44C231B186A832`) and is included beside the revised companion. `framework_checks.json` retains its exact and numerical output.
- The three `framework_*_notes.txt` derivations, three `audit_*.txt` correctness reviews, and three `provenance_*.txt` source comparisons are retained. These are working research notes, subordinate to the final revised companion; the final provenance correction takes precedence over early novelty wording. The synthesized note preserves their main useful cautions and uniform product estimate.
- The later whole-argument overview is preserved once under [ProofOverview](../artifacts/ProofOverview/), with PDF, TeX, and README. It remains conditional on two estimates and explicitly uses Fauzan's arithmetic estimate in place of Lai's problematic printed correction.

The current companion's change from the repository snapshot was inspected with a text diff. It adds explicit source attribution throughout and a provenance table, changes the title to an explanatory companion, removes novelty implications, and retains the mathematical interpretations. No existing repository/source file was modified by this review.
