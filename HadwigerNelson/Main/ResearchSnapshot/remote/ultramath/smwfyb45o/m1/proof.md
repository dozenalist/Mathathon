# d3: equilateral-triangle cells on the triangular lattice — K6 and an honest negative

Cells (side $l$): U = conv(0,e1,e2), D = conv(e1,e2,e1+e2), e1=(1,0), e2=(1/2,√3/2) (times l);
tiling = all U+v and D+v, v in the triangular lattice.

## PROVED (hand-verified, no code dependency)

For every lattice vertex x, exactly six triangles of the tiling contain x (3 of type U, 3 of type D).
All 15 pairs share the point x, so dmin = 0 for every pair. For a pair sharing an edge through x
the farthest vertex pair is (e1, e2−e1) giving dmax² = |2e1−e2|² l² = 3l²; for the opposite pair
dmax² = 4l². Hence all 15 pairs are forced (1 ∈ [dmin,dmax]) exactly when 3l² ≥ 1, i.e. l² ≥ 1/3.

**Theorem.** For l² ≥ 1/3 the triangular-cell tiling needs at least 6 colours: those six cells are
pairwise in conflict. (This does NOT exclude 6 colours; it is a K6, not a K7.)

## Computed but NOT established (negative result, stated as such)

`tri_tiling.py` builds the typed forced set in exact Fraction arithmetic (distance interval of two
convex polygons: dmax from vertex pairs, dmin from point-segment minima) and reports clique numbers
3,3,4,5,6,7,6,7,7,7,14,... for l² = 1/100,1/40,1/25,1/16,1/12,1/9,1/8,3/20,1/6,1/5,1/4,...

**Those omega ≥ 7 values are NOT valid.** The clique routine tests mixed-type pairs by membership in
F_UD ∪ (−F_UD); F_UD is not symmetric, so mixed pairs can be wrongly accepted. Re-checking the
reported clique for l²=1/5 and l²=1/9 with direct per-pair polygon arithmetic (`interval.py`)
gives an empty admissible l²-interval, i.e. those 7-cliques do not exist. Note `interval.py` and
`k6check.py` themselves use the offset w = v1−v2 where v2−v1 is required, so they are only
trustworthy as a red flag, not as a disproof.

## Scope / status
No 6-colouring impossibility is established for any triangular-cell tiling. What survives is the K6
(l² ≥ 1/3). The 6-colourability question for this family is open here; my clique search must be
re-run with an asymmetric mixed-type test (F_UD = {w : U vs D+w}, tested as w = v2−v1) before any
K7 claim can be made.
