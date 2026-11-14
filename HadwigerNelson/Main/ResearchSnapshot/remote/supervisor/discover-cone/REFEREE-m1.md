# Referee report on m1's submission (direction d1), swarm smwgphe8q

Verdict: **REJECTED ON SCOPE, MATHEMATICS CONFIRMED CORRECT.** Date 2026-11-14T18:1xZ.
My own checker: `referee_check3.py` in this directory (independent of m1's code).

## 1. What m1 claims
Theorems 1-3 (combinatorial core; general arbitrary-label form; exact solution set
`CC60^arc iff dist(v_i,v_j) > pi/3 on the nine non-consecutive pairs` = the triangular
prism K6 minus C6), Corollary 3 (all degenerate cases), section 5 (openness,
full-dimensionality, explicit non-grid certificate v* and a 4-parameter family),
Theorem 6 (width threshold 2pi/3), Theorem 7 + Corollary 7' (maximal confinement
forces the alternating grid). No plane claim.

## 2. Independent verification (my own implementation)
I did **not** reuse m1's pairwise reduction. I enumerated closed arcs of length w
directly at every critical left endpoint (the v_i and the v_i - w) and at the
midpoints between consecutive critical values, and for each such arc built the index
set and the union of interfaces over all 64 slot subsets. Fractions only.

| claim | check | result |
|---|---|---|
| Theorem 3 (both directions) | direct arc enumeration vs pairwise form, all 46656 grid tuples | 0 mismatches |
| Theorem 3 | same, 6000 random rational tuples with denominator 36 | 0 mismatches |
| Lemma 4 / grid count | all 6^6 tuples | 36 survivors = 6 x 6, as claimed |
| six survivors | q_0 = 0 slice | exactly the six AC-CONE-SIX words |
| v* certificate | exact distances | min = 13/20 pi; sup-box radius rho = 19 deg gives 13/20 - 2rho = 79/180 pi > pi/3 |
| 4-parameter family | corners + 600 random in-hypothesis points | 606/606 inside V; min at (pi/4,0,0) is exactly 5/12 pi |
| family corner (pi/4,pi/4,pi/4) | distinctness | six distinct non-grid angles |
| Theorem 6 ceiling | 300-start exact local search on min constrained distance | max found 7/12 pi < 2/3 pi; no counterexample |
| Theorem 7 | reduction re-derived by hand | sigma_i = s_i + s_{i+1} > pi/3 with s_{i+1} <= pi/3 gives s_i > 0; sum > 0 forces winding 1; six steps <= pi/3 summing to 2pi are all pi/3 — correct |
| Corollary 7' | m = 0 branch sampling | 0 configurations in V, as claimed |

## 3. Defects found (none fatal)
1. Section [7] of `cone_arc.py` tests theta >= 2pi/3 only by 2000 random tries; the
   written proof (three points cut the circle into arcs each > theta, so 2pi > 3theta)
   is what carries the statement, and it is correct. The script should say so.
2. Theorem 7 Step 1 ("by connectedness of the 6-cycle all sigma_i have one sign") is
   redundant: (7.1) already gives sigma_i > pi/3 for every i, and that alone yields
   s_i > 0. Harmless.
3. `W_empty = empty` in section 9 is correct only on the reading "close on K, far on
   every other pair (including the other consecutive pairs)". Stated ambiguously.
4. Section 5(i) says V is "not a finite union of grid-like strata"; the precise content
   is openness + nonemptiness, which is what the proof gives. Rhetorical, not wrong.

## 4. Why rejected anyway
The result is Astra's completed classification (non-adjacent pair distances > 60 deg;
gap form g_r > 60 for non-adjacent consecutive indices and g_r + g_{r+1} > 60; 57 of
60 six-distinct cyclic orders feasible). Independent re-derivation = corroboration,
not new knowledge. The block target moved to 4/5/6 distinct directions.

Banked from this submission, and not dependent on the verdict label:
**the survivor set is open and 6-dimensional, so the interface combinatorics forces
no excluded arc.** That is the justification for the pivot.

## 5. Delivered to m1 in the verdict reason
The pivot, the three admissible deliverables (T1 geometric obstruction / T2 equilateral
paired exclusion / T3 certified 4/5/6 family), the two banned grounds, and the warning
that a second rejection ends the direction.
