# SAIR127: verified specification

Source: [official problem 127](https://competition.sair.foundation/competitions/mathathon/problems/127),
title **Rogers Ramanujan Identity**, track/area **Combinatorics**.
Read in the SAIR browser interface on **2026-11-13**. The supplied URL's final
period was punctuation; the working address ends in `/127`.

## Official scope

The page describes the equality between the number of partitions with parts
in residue classes 1 and 4 modulo 5 and the number with differences at least 2.
It mentions the generating-function proof and the 1981 Garsia--Milne bijection,
and asks for a more natural bijection. Its two references are
[GM81a](https://doi.org/10.1073/pnas.78.4.2026) and
[GM81b](https://doi.org/10.1016/0097-3165(81)90062-5).

The displayed desired outcome is:

> Find a more natural bijection for the Rogers Ramanujan Identity.

The page does not supply a formal definition of naturalness. The criteria in
ROADMAP are the team's working criteria. The second Rogers--Ramanujan identity
is not the stated target; it may serve as an auxiliary comparison only.

## Normalized mathematical statement

For each natural number `n`, represent a partition as a finite descending list
`lambda_1 >= ... >= lambda_k > 0` with sum `n`. Define

```text
A(n) = { lambda : partition of n | every part modulo 5 is 1 or 4 }
D(n) = { lambda : partition of n | lambda_i >= lambda_(i+1) + 2 }
```

The gap condition applies to adjacent existing parts. There is no condition
`smallest part >= 2`; a smallest part equal to 1 is allowed. Both families
contain the empty partition at weight zero. Repeated parts are permitted on
the residue side. Positivity excludes zero as a part.

Seek explicit uniform functions `F_n : A(n) -> D(n)` and
`G_n : D(n) -> A(n)` with `G_n(F_n(a)) = a` and `F_n(G_n(d)) = d`, supported by
a structural explanation and comparison with prior constructions.

## Small fixtures

These fixtures follow directly from the definitions, independently of a
generating-function identity. They specify sets, not a preferred pairing.

| n | A(n) | D(n) |
| --- | --- | --- |
| 0 | `()` | `()` |
| 1 | `(1)` | `(1)` |
| 2 | `(1,1)` | `(2)` |
| 3 | `(1,1,1)` | `(3)` |
| 4 | `(4)`, `(1,1,1,1)` | `(4)`, `(3,1)` |
| 5 | `(4,1)`, `(1,1,1,1,1)` | `(5)`, `(4,1)` |
| 6 | `(6)`, `(4,1,1)`, `(1,1,1,1,1,1)` | `(6)`, `(5,1)`, `(4,2)` |

Equal counts, an arbitrary finite matching, or a ranking/unranking procedure
that presupposes equality is not by itself the desired explanatory result.
The project should still produce useful verified partial work if the all-weight
construction remains open.
