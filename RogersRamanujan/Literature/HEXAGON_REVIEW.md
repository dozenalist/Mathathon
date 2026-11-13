# Hexagon review and reproducibility

Accessed **2026-11-13**. Hexagon means the mathematics repository at
[hexagonmath.org](https://hexagonmath.org/).

## What was searched

The public [API description](https://hexagonmath.org/api/v1) links its
[OpenAPI contract](https://hexagonmath.org/api/v1/openapi.json). The documented
endpoint `GET /api/v1/works?q=...&limit=100` searches metadata such as title,
abstract, identifier, and listed contributor names. It is not full-text search.

| Query | Returned works | More pages |
| --- | ---: | --- |
| `Rogers` | 0 | No |
| `Ramanujan` | 7 | No |
| `partition bijection` | 0 | No |
| `biject` | 10 | No |
| `partition` | 38 | No |

[hexagon_search.json](hexagon_search.json) retains the queries, URLs, returned
IDs/titles, and pagination metadata. The unrelated hits were excluded from the
core reading list. Separate web searches for Rogers--Ramanujan on this domain
located the body-text connection in HEX26. Zero metadata matches is not evidence
that no relevant result exists. No directly applicable new residue-to-gap
bijection was identified in this search.

## Relevant record and usable mathematics

[HEX26: Riordan lattice paths counted by area](https://hexagonmath.org/2610.00705v1)
is contributed by Ilmar Gahramanov. The displayed header dates v1 to November 2,
2026; the version-history entry says October 31. Preserve the identifier rather
than resolving this display discrepancy by guessing. The record declares mixed
human/AI text and partial human checking. These are provenance declarations,
not verification certificates.

In the source, `F(x,y;q)` records area, up steps, and horizontal steps. Section 3
derives

\[
F(x,y;q)-1=qF(xq^2,yq;q)\big((x+y)F(x,y;q)-y\big).
\]

Section 4, equation (4.7), is the Rogers--Ramanujan-type specialization at
`y=0`; the exact TeX label is `eq:dyck`. Other useful locators are `sec:fe`,
`eq:fe`, and `eq:rec`.

**Project assessment:** the decomposition may inspire R3, but a proposed
connection must specify a reversible encoding of our actual partitions and
prove that its statistic is their weight. Similar series alone do not provide
that encoding. This paper is secondary to the classical bijection sources.

## Source preservation

The public source manifest supplied a single entry-point file `main.tex`.
It is retained unchanged as
[sources/hexagon_2610_00705v1.tex](sources/hexagon_2610_00705v1.tex), under the
record's CC BY 4.0 license. Its downloaded SHA-256 matched the manifest:

```text
c9e2e50b097412de3d59e0d7982f4b08a51f714de641b7106a22a28054074145
```

See [sources/README.md](sources/README.md) for attribution and links. The source
has been read as text; it has not been compiled or independently certified.

## Refresh procedure for Main

1. Repeat the recorded metadata queries; follow `next_cursor` if `has_more`
   becomes true, and record the new date instead of overwriting the old search.
2. Check the unversioned record for revisions, then cite any chosen version
   explicitly. Use the manifest's exact public file paths when reading source.
3. Search the body text of plausible papers as metadata search misses technical
   mentions. Log failed searches and excluded neighboring topics.
4. For any claimed breakthrough, extract the exact theorem, inspect its proof,
   reproduce examples, and assign X an independent review before citing it as
   an established input. Maintain a claim-status distinction in PROGRESS.
