# §7 at six colours: the transfer theorem, conditional on local finiteness of L

**Status.** This is a theorem about weak measurable 6-colourings, proved by re-running the
paper's §7 with `k = 6`. It is *conditional on one hypothesis*: that the cyclic locus
`L = {x : Gamma_x contains a cycle}` is locally finite (equivalently, for the use below, closed
with finite intersection with every compact set). Local finiteness is Theorem 6.5 of the paper
and is a `k = 5` theorem; whether it holds at `k = 6` is the object of the parallel attack. What
is established here is that **local finiteness is the only missing input**: every other step of
§7 is label-blind and transfers with the constant `alpha < 1/6` in place of `alpha < 1/5`.

Everything is stated for a weak measurable `k`-colouring in the sense of the paper's
Definition 1.2, with maximal palettes `P_x(e)` (Definition 5.1) and the paper's (5.2), (5.7),
Lemma 5.2, Lemma 5.5, Definition 6.1 and Lemma 6.2. We write `I = Fin k`, `K_k` for the complete
graph on `I` (the one-skeleton of the simplex `Delta(I)`), `R` for rotation of directions by
`kappa = pi/3`, and `sigma` for angular measure on `S`.

## The theorem

**Theorem A (Proposition 7.1 at k = 6, conditional).** Let `c` be a weak measurable 6-colouring
and assume:

* **(P)** `1 <= |P_x(e)| <= 3` for every `x` and a.e. `e` (the general-`k` palette bound,
  `results/K6-BARRIER.md` §1 at `k = 6`);
* **(LF)** `L = {x : Gamma_x contains a cycle}` is closed and locally finite.

Then there exist `ell in {3,4,5,6}`, distinct labels `i_0,...,i_{ell-1}`, a point `x`, and a radius
`rho > 0` such that for every edge `i_j i_{j+1}` of the label cycle there are a compact connected
set `K_j subset B(x,rho)`, a direction `v_j in S`, and a sequence `q_{j,m} in K_j \ {x}` with
`q_{j,m} -> x`, `(q_{j,m}-x)/|q_{j,m}-x| -> v_j`, and

  `x in K_j`,  `K_j cap partial B(x,rho) != empty`,  `H_{i_j} cap Delta(K_j) = H_{i_{j+1}} cap Delta(K_j) = empty`,

where `H_i` is the closed essential support of the colour class `A_i` and `Delta(K)` is the
straddling region (7.1).

**Corollary (the cyclic locus is nonempty and meets every side-10 square whose boundary misses it).**
Under (P)+(LF), `L != empty`; indeed for every closed square `Q` of side ten with
`partial Q cap L = empty`, `L cap Q != empty`. In particular no weak measurable 6-colouring has
`Gamma_x` a forest for every `x`.

## Proof

The proof is the paper's §7 with `I = Fin 6`, `G = K_6`, `alpha in (0,1/6)`, and
`ell in {3,4,5,6}`. We check each of its inputs at `k = 6`; the only quantitative changes are the
two constants displayed.

### 1. Disk averages and support detection (Lemmas 7.2, 7.3)

`p^eps_i(q) = (1/(pi eps^2)) int_{B(0,eps)} a_i(q+v) dv`, `i in I`. These are continuous
probability coordinates with `Lip(p^eps_i) <= C/eps` and `p^eps_i -> a_i` in `L^1_loc` and a.e.

*Lemma 7.2* (`p^eps_i(q) + p^eps_i(z) <= 1` for `|q-z| = 1`; positive liminf forces `q in H_i`).
Its proof uses only: for a.e. translation `t in B(0,eps)`, both `q+t` and `z+t` are typical, and
two typical points at distance one have different colours (Lemma 4.3). Lemma 4.3 is stated and
proved for a general `k`. No change. `square`

*Lemma 7.3* (if `ij notin Gamma_x`, a ball `B` about `x` with `int_{B'} p^eps_i p^eps_j = o(eps)`,
and the violation set is covered by disks of total radius `-> 0`). The proof uses Definition 6.1,
nonnegativity, `|S a_s - S a_s(.+h)|_{L^2(B)} = o(|h|)` (equation (6.3)) and Fubini. Eq. (6.3) is
a Fourier estimate for normalized circle measure, independent of `k`; `sum_s a_s = 1` is not used
there except through boundedness. No change. `square`

### 2. Graph-valued maps outside small core disks (Lemma 7.4)

Fix `alpha in (0,1/6)`. This is the one constant that changes. Define

  `q^eps_i(z) = (p^eps_i(z) - alpha)_+ / sum_{l in I} (p^eps_l(z) - alpha)_+`,  `i in I`.

Since `sum_l p^eps_l = 1` and each `p^eps_l <= 1`, and since `k = 6`, at least one `p^eps_l > 1/6 > alpha`
(average argument: if all `p^eps_l <= alpha < 1/6`, the sum is `< 1`). So the denominator is
positive and `q^eps` is a continuous map into the simplex `Delta(I)`. Moreover `q^eps_i(z) > 0`
iff `p^eps_i(z) > alpha`. Let `G = K_6` be the one-skeleton of `Delta(I)`.

Choose a closed square `Q` of side ten with `partial Q cap L = empty`. Such a square exists
because `L` is closed and locally finite: a small translation of any side-ten square avoids the
finite set `L cap Q'` on the boundary. Choose a larger closed square `Q'` containing `Q` in its
interior and put `L_0 = L cap Q'`, a finite set by (LF).

*Lemma 7.4* (small holes and tree fillings). The proof has three ingredients.

(i) For `z` outside the original core disks `B(x,delta)`, `x in L_0`, `Gamma_z` is a forest.
This is the definition of `L` and holds at every `k`.

(ii) For each nonedge `ij` of `Gamma_z`, Lemma 7.3 gives a ball on which the violation set
`{p^eps_i > alpha, p^eps_j > alpha}` is covered by finitely many disks of total radius `-> 0`.
Finitely many nonedges, compactness of `M_delta = Q' \ union B(x,delta)`, and a Lebesgue number
give the marked family. At a point outside all marked disks, the positive coordinates of `q^eps`
form a clique in the forest `Gamma_z`. **A clique in a forest has at most two vertices, and a
two-element clique is an edge.** This is the label-blind step: it never uses `k = 5`. At `k = 6`
the positive set is a clique in a forest, hence has size at most 2 and, if 2, is an edge of
`Gamma_z`, i.e. a point of `G = K_6`. `square`

(iii) The tree-filling and merging argument: a finite forest is contractible, so boundary values
into a component tree extend; merging disks preserves the estimates. No `k`. `square`

### 3. The cover obstruction and the non-null core loop (Lemmas 7.5, 7.6)

*Lemma 7.5* (no relatively open cover of a closed side-ten square with multiplicity `<= 2` and
mesh `<= 2`). Its proof uses only the partition of unity, the fact that at most two weights are
positive, and Brouwer's fixed-point theorem. The number of labels enters nowhere. `square`

*Lemma 7.6* (for large `n`, some core disk `B_{n,x} subset Q` has a boundary loop whose image
under `g_n` is not null homotopic in `G`). Proof: otherwise extend all core boundary loops over
their disks in `G` and paste, obtaining `g~_n : Q -> G` equal to `q^{eps_n}` outside the holes. For
`i in I`, let `U_{n,i}` be the components of `{z in Q : (g~_n(z))_i > 0}`. They form a cover of
`Q` of multiplicity at most two, because **every point of the one-skeleton `G = K_6` has at most
two positive barycentric coordinates** — again label-blind. The mesh bound `<= 1 + o(1)` uses
Lemma 7.2 and (7.6), exactly as printed. For large `n` it is `<= 2`, contradicting Lemma 7.5.
`square`

### 4. Graph words and annular crossings (Lemmas 7.7, 7.8)

*Lemma 7.7* (midpoint detection by a reduced circuit). Pure graph theory for a finite connected
simple graph; the proof uses only that `G` has no loop edges and no multiple edges. `K_6` is such
a graph. `square`

*Lemma 7.8* (a connected midpoint preimage crosses the annulus). Uses the classification of the
fundamental group of an annulus, compactness, grid approximation and winding numbers. The target
graph is any finite connected simple graph. `square`

### 5. Limiting continua and the cycle (proof of Proposition 7.1)

`L_0 cap Q` is finite by (LF). Pass to a subsequence with a fixed `x in L_0 cap int(Q)` whose core
boundary loop is non-null at every index. Choose `rho > 0` with `B(x,rho) subset int(Q)` and
containing no other point of `L_0` (possible because `L_0` is finite, so the minimum distance from
`x` to `L_0 \ {x}` is positive). The rest is verbatim: `g_n` is defined on the annulus
`A_n = B(x,rho) \ B_{n,x}`; the reduced circuit `W_n` of the inner boundary contains a simple
cycle (Lemma 7.7); there are finitely many simple cycles in `K_6`, so a subsequence has a fixed
cycle of length `ell in {3,4,5,6}`; for each edge midpoint `m_j`, Lemma 7.8 gives a compact
connected `K_{n,j} subset g_n^{-1}({m_j}) cap A_n` meeting both boundaries; Hausdorff limits
`K_{n,j} -> K_j` are compact connected, contain `x`, meet `partial B(x,rho)`, and have the support
exclusion by the same `alpha`-estimate (7.7) with `k = 6`. Finally
`{|q-x| : q in K_j} = [0,rho]` by connectedness and the two contacts, giving the directions `v_j`
and the sequences `q_{j,m}` by choosing radii `rho/m`. `square`

### 6. The corollary

If `L = empty`, take any side-ten square `Q`: `partial Q cap L = empty` and `L_0 = empty`, so
Lemma 7.4 gives `g_n = q^{eps_n}` on `Q`, and Lemma 7.6's proof (with no core disks) produces the
multiplicity-two, mesh-`<=2` cover of `Q`, contradicting Lemma 7.5. So `L != empty`. More
generally, if `Q` is a side-ten square with `partial Q cap L = empty` and `L cap Q = empty`, the
same argument with `L_0 = L cap Q'` (and `Q'` a slightly larger square with `L cap Q' = empty`,
possible since `L` is closed and `Q` compact) gives the contradiction. Hence `L cap Q != empty`.
`square`

## What is *not* claimed

* No proof of (LF). The whole content of Sprint B Step 1 is exactly (LF).
* No use of the strengthened `k = 6` facts (C1) pairwise-complement exclusion and (C2) the
  orbit bound `sigma({|P| = 3}) <= pi`; §7 does not need them. They belong to the Step 3 CSP.
* The theorem is not vacuous *given* (LF): it produces a genuine cycle of exclusion continua and
  a length in `{3,4,5,6}`. At `k = 5` the same proof produces `ell in {3,4,5}` and §8 excludes the
  three lengths. At `k = 6` the new length `ell = 6` is one of the four outputs.
* The constant `alpha < 1/6` is sharp for this argument: at `alpha = 1/6` the denominator can
  vanish at a point where all six disk averages equal `1/6`. Any `alpha in (0,1/6)` works.

## Audit table

| paper step | k-dependence | at k = 6 |
|---|---|---|
| Lemma 7.2 | none (Lemma 4.3, any k) | verbatim |
| Lemma 7.3 | none (Definition 6.1, Fourier estimate) | verbatim |
| `alpha in (0,1/5)` | `1/k` | `alpha in (0,1/6)` |
| `G` = one-skeleton on 5 vertices | `K_k` | `K_6` |
| Lemma 7.4 clique-in-forest | none | verbatim |
| Lemma 7.5 cover obstruction | none | verbatim |
| Lemma 7.6 multiplicity `<= 2` | `<= 2` positive barycentric coordinates, any k | verbatim |
| Lemma 7.7 | any finite connected simple graph | `K_6` |
| Lemma 7.8 | any finite connected simple graph | `K_6` |
| cycle length | `3 <= ell <= k` | `ell in {3,4,5,6}` |
| `Q` with `partial Q cap L = empty`, `L_0` finite | Theorem 6.5 (k=5 only) | **(LF) assumed** |
