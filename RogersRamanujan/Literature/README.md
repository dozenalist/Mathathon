# Literature index for problem 127

Last reviewed: **2026-11-13**. Start with [PROBLEM_SPEC.md](PROBLEM_SPEC.md),
then the role-specific reading order in [ROADMAP.md](../ROADMAP.md).

This is an agent-readable research bundle: original concise notes and precise
source locators, not a collection of unverified abstracts presented as proofs.
The notes record what was actually accessible and read. Read the original
argument before implementing a delicate transformation or relying on a theorem.

| File | Use |
| --- | --- |
| [PROBLEM_SPEC.md](PROBLEM_SPEC.md) | Verified target, notation, conventions, and scope |
| [READING_NOTES.md](READING_NOTES.md) | Source cards, mathematical takeaways, limitations, and tasks |
| [sources.json](sources.json) | Structured source IDs, URLs, locators, access/review status, and role assignments |
| [references.bib](references.bib) | Citation metadata for the eventual write-up |
| [HEXAGON_REVIEW.md](HEXAGON_REVIEW.md) | Recent-source assessment and reproducible search method |
| [hexagon_search.json](hexagon_search.json) | Dated public catalog results with pagination status |
| [LEAN_API.md](LEAN_API.md) | References to the exact locally inspected mathlib revision |
| [sources/README.md](sources/README.md) | Attribution, license, integrity, and retrieval instructions |
| [sources/hexagon_2610_00705v1.tex](sources/hexagon_2610_00705v1.tex) | Unmodified CC BY 4.0 source for the Hexagon paper |

## Source map

| ID | Source | Priority / use |
| --- | --- | --- |
| SAIR127 | Official problem page | Binding project target |
| GM81a | Garsia--Milne, PNAS announcement | Competition reference; method overview |
| GM81b | Garsia--Milne, full bijection paper | Competition reference; historical baseline |
| BZ82 | Bressoud--Zeilberger, short bijection | First implementation target |
| BP06 | Boulet--Pak, combinatorial proof | Durfee/rank route and notation bridge |
| PAK06 | Pak, partition-bijection survey | Techniques and involution-principle context |
| PAK04 | Pak, asymptotic stability preprint | Precisely scoped geometric framework |
| PAK18 | Pak, complexity survey | Complexity, ranking caveat, geometric obstruction statement |
| SOODAK18 | Soodak, exploratory REU paper | A concrete conjecture to audit, not an established extension |
| MSZ09 | McLaughlin--Sills--Zimmer, computer searches | Experimental-method precedent |
| HEX26 | Gahramanov, Riordan paths | Secondary path/recurrence inspiration |

## Reading and update protocol

1. Resolve a source ID in `sources.json`; use the listed section/equation, not
   an unversioned search snippet. Older preprint and journal pagination differ.
2. Translate its notation into `A_n` (residues) and `D_n` (gaps). Authors use
   different letters and sometimes a third, square-based partition family.
3. Record a source claim separately from a project claim. Preprint existence,
   AI provenance, and finite checks do not constitute independent verification.
4. For a new source, add author/title/year, stable URL and version, locator,
   access status, relevant takeaway, limitations, and the responsible agent.
5. Do not invent missing DOI, theorem numbers, licenses, or bibliographic data.
   Preserve attributions and license conditions for redistributed source files.

The bundle intentionally centers the bijection problem. General q-series,
modular-form, and hard-hexagon statistical-mechanics literature is useful only
when it supplies a concrete step in a selected route. **Hexagon** here means
the [Hexagon mathematics repository](https://hexagonmath.org/), not the
hard-hexagon lattice model.
