# ZetaFive progress

## 14 November 2026

Published an [exponent catalog](EXPONENT_CATALOG.md) for the original $K=40n$, $N=3n$, $h=37n$, $D_N^6$, $M=200$ construction and its proposed extension from $k=5$ to $k=7$.

- The catalog preserves the comparison table, links the relevant results in Fauzan and Lai, and derives the contributions from small primes, the compact inner range, the tail, the outer range, and the real estimate.
- Exact rational reconstruction gives an arithmetic increase of $751/768$, and the adapted final upper-bound coefficient is $+0.960456781075\ldots$. This estimate does not establish the decay needed for irrationality.
- `node ZetaFive/Computation/exponent_catalog.mjs` passes: it reconstructs the inner integral on 143 intervals, both outer integrals, the row-weight costs, and the reported totals without floating-point arithmetic.
- Claim status: the $k=7$ local determinant estimates still require uniform verification. The computation verifies the accounting, not a proof of irrationality or an impossibility result for other constructions.
