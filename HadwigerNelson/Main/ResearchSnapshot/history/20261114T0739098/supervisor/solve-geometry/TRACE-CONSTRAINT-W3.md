# One colouring-level constraint toward `(W3)`: what the unit circle about a triangle centre is allowed to be

Block scope: one obligation, in the class `S_1`, at `k = 6`. Grades: **[P]** paper-level argument
written here (assumptions and a.e. quantifiers explicit); **[A]** arithmetic, machine-checked by
`checks/trace_limit.py` (output appended to `supervisor_checks.out`); **[C]** cited, not re-verified;
**[S]** source-checked at Lean lines by another worker.

## 0. Setting, once

`c` is a weak measurable 6-colouring (paper Def. 1.2), labels `[6] = {0,...,5}`, `S = S^1` with
normalised angular measure `sigma`, `R` the rotation of directions by `kappa = pi/3`.
`P_x(e)` is the maximal palette (Def. 5.1) — the essential support of the circle traces at the
centre `x` — and `Gamma_x` the transition graph (Def. 6.1). `L = {x : Gamma_x contains a cycle}`,
`T = {x : Gamma_x contains a 3-cycle}`.

`S_1`: for **every** centre `x`, `P_x(e)` is a singleton for a.e. `e ∈ S`. In `S_1` write
`P_x(e) = {b_x(e)}` with `b_x : R^2 x S -> [6]` jointly measurable (a measurable selection exists by
a.e. uniqueness in `S_1`).

Two paper facts are used, both quoted from `paper.pdf` (text render in `.scratch/paper.txt`):

* **(6.2) / Lemma 6.2** (p. 35): if `ij` is an edge of `Gamma_x` then `P_x(e)` is not contained in
  `{i,j}`; and there is a trace supported in `P_x` that kills `i` and `j`.
* **(A1) endpoint trace** (Lemma 1 of `m10`, from `trace_realization`): for a.e. `e`, `c(x+e) ∈ P_x(e)`.

**(A1) is the constraint the palette models omit.** It involves the colouring, not the palette field;
the abstract models of `sprint/k6/FREE-LABEL.md` and Theorem C satisfy every palette axiom of record
and fail (A1) on a set of full angular measure (`m10` §1, verified there by two programs).

## 1. Why the target is not the m10 two-centre CSP (checked before choosing it)

`m10`'s CSP (`REDUCTION.md`, `twocentre.py`) is over **pairs of centres at distance exactly 1**: its
conflict graph is the pullback of the plane's unit-distance graph along `pi(x,e) = x+e`, so a finite
two-centre CSP that is UNSAT at `k = 6` exists **iff** a 7-chromatic finite unit-distance graph
exists (`sprint/k6/REPORT.md` §7). The object I proposed last block — two *triangle centres* at
separation `d ∈ (1,2)` — differs in three ways: (i) `d != 1`, so properness links no point of the
two centres' unit circles to the other centre, and the conflict graph is not a unit-distance pullback;
(ii) the transfer is (5.3) with a non-trivial angular diffeomorphism `s_±`, `|arg s_±(f) - (arg f ±
pi/3)| <= 1.5938 d`, not with the constant endpoint `s = id`; (iii) it is not a finite object: a
genuine two-centre system at `d` has a continuum of angular data, and **discretising it into a sector
word is exactly the ansatz killed by `m10`'s Theorem 2** (no centre-independent palette field exists
for any measurable colouring at any `k`).

So the `d ∈ (1,2)` problem is *neither* the m10 CSP *nor* a finite problem, and I am not relabelling
it as progress: I drop it for this block and say why, rather than reporting a reduction that would be
either a re-encoding of the colouring problem (`m8`'s collapse) or a sector ansatz already excluded.

## 2. Proposition A (proved): the unit circle about a triangle centre is a.e. valued in the complement triple

**Prop. A [P].** Let `c` be a weak measurable 6-colouring in `S_1`. Let `x` be a centre whose
`Gamma_x` contains a triangle with label set `V` (`|V| = 3`), and put `T = [6] \ V`. Then
`c(x+e) ∈ T` for a.e. `e ∈ S`. Consequently `P_x(e) = {c(x+e)}` for a.e. `e`, i.e. in `S_1` the
palette field at a triangle centre *is* the circle colouring, three-valued.

*Proof.* By `S_1`, `P_x(e) = {b_x(e)}` for a.e. `e`. By Lemma 6.2 applied to each of the three edges
of the triangle, the singleton `{b_x(e)}` is not contained in an edge, so `b_x(e) ∉ V` for a.e. `e`
(any `i ∈ V` lies on a triangle edge). Hence `b_x(e) ∈ T` a.e. By (A1), `c(x+e) ∈ P_x(e) = {b_x(e)}`
for a.e. `e`, so `c(x+e) = b_x(e) ∈ T` a.e. `square`

**Consistency check against the only explicit colouring in the record [C]+[A].** `m3`'s proper
measurable `k >= 7` colouring has `Gamma_{q_n} ⊇ {0,2,3}`, `V = {0,2,3}`, `T = {1,4,5,6}`,
`|T| = k - 3 = 4`; its gadget sits inside `B(q_n, 1/2)`, so the unit circle about `q_n` is background
and carries exactly the four labels `{1,4,5,6} = T`. Prop. A holds there **with equality**, and the
size `|T| = k - 3` is precisely the resource that `k >= 7` has and `k = 6` does not. Prop. A is
therefore not vacuous and is sharp at `k >= 7`.

**Grade honesty.** Prop. A is an implication from the paper's (6.2) and (A1) plus the class hypothesis
`S_1`. It is *not* new mathematics about the paper, and it does *not* by itself bound `T`.

## 3. Proposition 4 (proved): a constraint on an accumulation pair

**Prop. 4 [P].** Let `c` be in `S_1`, and let `x_n ∈ T` with `x_n -> p`, each `Gamma_{x_n}` containing
a triangle whose label set is the **same** `V` (pass to such a subsequence: there are only
`C(6,3) = 20` label sets [A], so it always exists). Then `p ∈ T` (the 3-cycle locus is closed,
being a finite intersection of closed sets `E_ij`), say with label set `V'`; and

  `[6] \ (V ∪ V') != empty`, i.e. the two triangles share a missing label; equivalently
  `T ∩ T' != empty` with `T = [6]\V`, `T' = [6]\V'`.

*Proof.* Each `b_{x_n}` is `T`-valued a.e. (Prop. A), so it is an a.e.-defined measurable map into the
finite set `T`. The set of such maps is compact in the topology of convergence in measure (it is a
closed bounded subset of `L^0` of a finite measure space); hence a subsequence converges in measure,
and a further subsequence converges **pointwise `sigma`-a.e.** to some `b_inf`, which is `T`-valued.
Bounded pointwise convergence is `L^2` convergence, so `1_{b_inf} ∈ W_p` is a trace at `p` (take the
centres `x_{n_k} -> p`, radius `r = 1`, and typicality a.e. from Lemma 4.3). By (C1) of `m10`
(every trace has its positive coordinates in the palette), `{b_inf(e)} ⊆ P_p(e)` for a.e. `e`. Since
`p ∈ S_1`, `P_p(e) = {b_p(e)}` a.e., so `b_inf = b_p` a.e. At `p`, Lemma 6.2 for the triangle `V'`
gives `b_p(e) ∈ T'` a.e. Hence `b_inf` takes values in `T ∩ T'` a.e., and that set is non-empty.
`square`

**What Prop. 4 buys and does not buy.** It rules out one half of the label geometry at an
accumulation: the accumulating triangles cannot have `V ∪ V' = [6]` (`T ∩ T' = empty`). Exhaustively,
20 of the 400 ordered pairs `(V,V')`, 10 of 210 unordered pairs, are excluded [A]. It does **not**
give `(W3)`: the surviving pairs are 380 of 400 and nothing in the record removes them. In particular
`V = V'` is *consistent* with Prop. 4, so an accumulation of identical triangles is not excluded by
this route.

## 4. The step that fails, stated exactly (why Prop. A does not reach `(W3)`)

The natural attempt is: at the accumulation point `p`, `T ⊆ P_p(e)` a.e., so `|P_p| >= 3`, which
contradicts `S_1`. **This is invalid**, and the reason is exact: it needs the singleton fields to pass
to the limit, and they do not. `W_p` is the set of **strong** `L^2` limits of sample codes
(`trace_realization`), so a limit of one-hot fields that is not one-hot is not a trace.

The minimal countermodel to the weakened form [A]: on a 12-sector circle with `T = {3,4,5}`, let
`b_n(s) = 3 + ((s+n) mod 3)`. Every `b_n` is one-hot and `T`-valued; pairwise `L^2` inner products are
`0` or `1`; the average of three consecutive distinct members is the **uniform** field
`(1/3,1/3,1/3)`, whose support is all of `T`. If weak `L^2` limits counted as traces, (C1) would give
`|P_p| >= 3` and `(W3)` at `k = 6` would follow. Since only strong limits count, the conclusion is
only the much weaker `{b_inf} ⊆ P_p` of Prop. 4. (The family has finitely many distinct members, so
this is an illustration of the inference, not of non-compactness; the compactness needed in Prop. 4
is genuine.)

**The residual obligation, exact.** To get `(W3)` from Prop. A one needs a condition forcing
`b_inf` to take **at least three distinct values on positive-measure sets** (then `|P_p| >= 3`), or
forcing `T ∩ T'` to be empty. Neither is available: (5.7) gives only two values
(`b_inf(e) != b_inf(Re)` a.e.), a.e.-singleton fields carry no smoothness, and every surviving label
pair of Prop. 4 is consistent with (6.2), (5.7) and (5.3).

## 5. Independence of the two gaps (kept separate, as required)

* **(G1)** `(W)`/`(W3)`: finitely many cyclic (triangle) centres in one ball of radius `> 1`. This
  block adds Prop. A and Prop. 4 toward it; it does not reach it.
* **(G2)** §8 at `k = 6`: with `(W)` granted, Prop. 7.1 yields `ell ∈ {3,4,5,6}` and the printed §8
  excludes `ell ∈ {3,4,5}` only at `k = 5`; the strip layer is SAT for every `k >= 6` and every
  `ell`. Nothing in this block touches (G2).
* Neither gap implies a bound on `chi(R^2)` alone; `6 <= chi(R^2) <= 7` is unchanged.

## 6. Files

| file | content |
|---|---|
| this file | Prop. A, Prop. 4, the failing step, the residual obligation |
| `checks/trace_limit.py` | [A] sections [9]-[11]: the weak-limit countermodel, the label counts 20/400 and 10/210, the `m3` `k = 7` consistency check |
| `CORRECTED-DEPENDENCY-MAP.md` | §9 ledger, §10 R3 audit; unchanged by this block |
