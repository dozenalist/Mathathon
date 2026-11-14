# Specification: the partition rule for the cluster criterion (G4)

What is missing for K15-C025 is a partition of the packing into clusters over
which the averaged inequality `Σ_{v∈K}(vol Ω(v)+A(v)) ≥ V_0|K|` can be *proved*.
E's `K15-E001` leaves the partition free, and its universal form is false
(`K15-C015`: a singleton at the icosahedral vertex gives `5.55029 < √32`).
This file fixes the requirements so that a proposed rule can be checked rather
than argued about. Author M; reviewer E, then X.

## R1 — The rule must be determined by the packing

`Π = Π(Λ)` must be a function of the point set, not a choice made after seeing
the inequality it must satisfy. Concretely: specify a radius `σ` and let `K` be
the set of vertices within graph distance `m` of a seed chosen by a *local* rule
(e.g. the lexicographically least vertex in each `σ`-ball). The rule may use the
whole packing's coordinates, but it may not depend on `V_0`, on `A`, or on the
outcome of the inequality.

## R2 — The boundary term must be explicit

Cluster averages are only useful if the boundary is `o(1)` per vertex. The
requirement: `#{v : v ∈ K, the whole σ-ball about v meets K} = O(∂K)` with
`Σ_K ∂|K| ≤ C·r²` inside `B(x,r)` — i.e. the number of vertices "near a cluster
boundary" is `O(r²)`, not `O(r³)`. This is the analogue of negligibility and it
is where a naive rule (e.g. touching clusters) fails: the boundary of a Voronoi
decomposition of clusters is a surface, so its vertices are `O(r²)` only if the
clusters are fixed in size, which forces `D` bounded — and then the icosahedral
cluster (diameter 4) is admissible while larger defects are not.

## R3 — The cluster inequality itself

For every cluster `K` produced by R1 with `diam K ≤ D`:
`Σ_{v∈K} (vol Ω(v) + A(v)) ≥ V_0 |K|`, with `V_0 > 5.550291` for progress and
`V_0 = √32` for Kepler. Two admissible ways to prove it, both analytic:

1. **Rogers-type.** Decompose `∪_{v∈K} Ω(v)` into simplices with vertices at
   centres in `K ∪ (one layer outside K)`; the cap estimate of Rogers gives a
   lower bound depending on the number of Delaunay simplices attached to each
   vertex. The constant to beat is `√32`, and Rogers' simplex bound
   (`σ₃ = 0.779635570044… → V_0 = (4π/3)/σ₃ = 5.372754099…`) is *below* it, so a
   bare Rogers estimate is not enough: the cluster structure must beat Rogers by
   `√32/5.372754 = 1.0529` (5.29%) on the configurations that occur. For scale the
   ladder in cell-volume units is `4.188790` (ball) < `5.372754` (Rogers) <
   `5.550291` (dodecahedral) < `5.656854` (Kepler).
2. **Fejes Tóth-type.** A weighted average over the cells of `K` with weights from
   the contact graph, as in L. Fejes Tóth's programme; the weight exists only if
   the contact graph's structure is controlled, which is the hard part.

If `A` is a bounded-range antisymmetric transfer (K15-C035) then `Σ A ≤ C₁r²`
holds automatically with `C₁ = 3Φ(R+1)⁵`, so negligibility is not a separate
obligation; what remains is the pointwise inequality `Σ_w φ(v,w) ≥ √32 − vol Ω(v)`
and hence the analytic cluster-volume bound. *(The earlier sentence here — that
`A` must be "negative on a full-density set" — came from K15-C029 and is
**withdrawn**, review 0138: the correct statement is the signed estimate
`θ#(D_θ) ≤ C₁r² + N_A` of K15-C029r.)*

## R4 — Test cases the rule must survive

| Configuration | Required behaviour |
| --- | --- |
| the icosahedral 13-cluster (diameter 4) | must be a single cluster; the inequality must hold there with `A ≥ 0.106563` |
| fcc (all clusters identical) | equality `V_0 = √32`; any rule that gives `< √32` here is wrong |
| hcp and ABA/ABC mixtures (`K15-C033`) | the same values as fcc; the rule must not distinguish them by symmetry |
| a packing with an isolated defect pair | the defect cluster must be small, and the boundary count must stay `O(r²)` |
| zero-density defect sets | must not affect the average: the inequality is per cluster, and clusters in a zero-density set contribute `o(1)` |

## R5 — What counts as progress

A rule satisfying R1–R2 plus *any* proved `V_0 > 4π/3 · ... ` (i.e. better than
the trivial ball bound `4.19`) with a stated `D` is a publishable component; the
threshold `5.550291` (dodecahedral) is the first genuinely interesting target, and
`√32` is the theorem. Report `V_0` and `D` together, never `V_0` alone.
