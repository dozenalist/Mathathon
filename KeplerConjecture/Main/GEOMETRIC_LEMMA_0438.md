# The highest-value missing geometric lemma, and the global bridge it needs

Block `K15-REVIEW-0438-M`. Deliberately not a new conjecture: this file picks the one
geometric statement on the table whose *target is strictly stronger than the published
dodecahedral bound*, states it exactly, supplies the piece that is actually missing (the
global density bridge), proves what can be proved, and isolates what cannot.

## 0. The bar this has to clear

The brief says a target already weaker than the dodecahedral bound is not progress.
Reference point (kept in `ACCEPTED.md`): Hales–McLaughlin gives `vol Ω(v) ≥ V_dod =
5.550291028515510` for every cell, hence `δ ≤ 0.754697399337`. So a candidate lemma must aim
at something at least this strong, and preferably at `δ ≤ π/√18 = 0.740480489693` itself.

**Verdict up front.** The candidate is E's pair conjecture `(P′)` (`K15-E074`), and it clears
the bar: with the bridge below it would give `δ ≤ π/√18` *exactly*, not `0.754697…`. What
was missing is not the conjecture but the **global bridge**: E's own justification for `(P′)`
is "it implies the cut", and that is true only for the single cut `U =` the 13-cluster, with
`1.72%` to spare. A cut at one `U` is not a density bound. §3 supplies the bridge.

## 1. The local statement (`(P′)`, E's)

> **(L) Pair bound.** For every pair of centres `v, w` at distance exactly `2` (a *contact
> pair*) in a saturated 2-separated packing of `R³`,
>
> ```
> vol Ω(v) + vol Ω(w)  ≥  2√32  =  11.3137084990…
> ```

Provenance: E's `K15-E074`, tested by E on fcc (1752 pairs), hcp (212 pairs), A15 (10098
pairs) and two icosahedral fixtures; **unproved**.

**It is strictly stronger than the pointwise bound.** Hales–McLaughlin gives only
`vol Ω(v) + vol Ω(w) ≥ 2V_dod = 11.10058206`, which is `0.213` short. E's `K15-E075` closes
the obvious gap exactly: two adjacent centres cannot *both* be dodecahedral, because the two
icosahedral contact rings clash at distance `1.056487696` against a required `2`, for every
relative twist. So `2V_dod` is unattainable and `(L)` is a genuine strengthening, not a
restatement.

**Its equality case is exactly the Barlow family — and that is a proof, not evidence.** By
`K15-C094` every Voronoi cell of every Barlow packing has volume `√32` exactly, so every
contact pair there sums to `2√32`. Hence

> **(L) holds with equality on every Barlow packing** (`K15-C106`).

That is the whole known equality family, and `(L)` is sharp on it, so `(L)` cannot be
improved to `> 2√32`.

## 2. Why a local bound is not yet a density bound

`(L)` constrains *pairs*. The density statement is a statement about *vertices*: it needs
`Σ_{|v|≤R} vol Ω(v) ≥ √32·#{|v| ≤ R}` up to `o(R³)`. Going from edges to vertices requires a
combinatorial object, and this is exactly where E's "`(P′)` implies the cut with `1.72%`
margin" stops short: the arithmetic there is

```
12·(2√32) − 12·V_dod  =  69.1610096456   ≥   13√32 − V_dod  =  67.9888142149 ,
```

i.e. `(L)` gives `Σ_{i=1}^{12} vol Ω(w_i) ≥ 69.161` while the 13-cluster cut needs only
`67.989` — a margin of `1.172195`, `1.724%`. **That is one cut, not the density theorem.**
It is worth keeping (it is the binding fixture, `C081r`), but it must not be quoted as a
density result.

## 3. The bridge (new here, `K15-C106`)

Notation: `G` is the **contact graph** of a saturated 2-separated `Λ`, i.e. `v ~ w` iff
`|v−w| = 2`; `δ⁺` and `cap` are as in `CUT_FLOW_THEOREM.md`; `deg` is the contact degree
(so `deg(v) ≤ 12`, the kissing number).

> **Theorem B.** Let `Λ` be saturated and satisfy `(L)`. Suppose there are weights
> `c_e ≥ 0` on the contact edges with
>
> ```
> Σ_{e ∋ v} c_e  =  1     for every v outside a set E of upper density zero.        (M)
> ```
>
> Then `δ(Λ) ≤ π/√18`.

*Proof.* Fix `R`, put `B = Λ ∩ B(0,R)`. Since `Σ_{e∋v}c_e = 1` on `B∖E_B`,

```
Σ_{v∈B} vol Ω(v)  ≥  Σ_{v∈B∖E_B} vol Ω(v)
     = Σ_{v∈B∖E_B} (Σ_{e∋v} c_e) vol Ω(v)
     = Σ_e c_e  Σ_{v ∈ e ∩ (B∖E_B)} vol Ω(v)
     ≥ 2√32 · Σ_{e ⊆ B∖E_B} c_e ,
```

discarding the edges with an endpoint outside `B∖E_B` (their contribution is `≥ 0`). Count
those edges: writing `C_R := Σ_{e : e ⊄ B∖E_B} c_e`, and using `0 ≤ c_e ≤ 1` (which holds
because `c_e` is one summand of `Σ_{e'∋v}c_{e'} = 1`),

```
|B| − |E_B|  =  Σ_{v∈B∖E_B} Σ_{e∋v} c_e  =  2 Σ_{e ⊆ B∖E_B} c_e  +  C_R ,
```

so `Σ_{e⊆B∖E_B} c_e = (|B| − |E_B| − C_R)/2`, and therefore

```
Σ_{v∈B} vol Ω(v)  ≥  √32 ( |B| − |E_B| − C_R ) .
```

**A measurement of the error term (`Computation/bridge_boundary.py`).** Step (i) is the one
estimate that could be over-optimistic, so it was measured on fcc (all cells `√32` exactly):
`D(R) := √32·#{Λ ∩ B(0,R)} − (4π/3)R³` over `R = 4, 6, …, 16` gives `D/R² ∈ [0.17, 2.69]` and
`D/R³` small and oscillating (`0.031, 0.126, 0.030` at `R = 12, 14, 16`). So `D = O(R²)` with an
effective constant of order `1–3` in units of `√32`, consistent with step (i). The oscillation is
the expected shell effect (`D` jumps when a lattice shell enters the ball); the measurement is a
check of the *claim*, not its proof, which is the tiling argument.

Two estimates close it. **(i)** `Σ_{v∈B} vol Ω(v) = (4π/3)R³ + O(R²)`: the cells tile space,
`saturation` gives `Ω(v) ⊆ B(v,2)` (Hales' covering lemma, the same input `C087` needs), so
the cells of `B` cover `B(0,R−2)` and lie in `B(0,R+2)`. **(ii)** `C_R` splits into two kinds
of edge: those with an endpoint in the shell `{R−2 ≤ |x| ≤ R+2}` (a contact edge leaving `B`
must have such an endpoint, since `|v−w| = 2`), of which there are `O(R²)` because the centres
are 2-separated, each carrying at most `12` contact edges; and those incident with `E_B`,
contributing at most `12|E_B|`. Since `c_e ≤ 1`,

```
C_R  ≤  O(R²) + 12|E_B|  =  O(R²) + o(R³) .
```

With `|E_B| = o(R³)` by hypothesis,

```
√32 ( c(Λ)·(4π/3)R³ − o(R³) )  ≤  (4π/3)R³ + O(R²) ,
```

and dividing by `(4π/3)R³` and letting `R → ∞` gives `√32·c(Λ) ≤ 1`, i.e.
`δ(Λ) = (4π/3)c(Λ) ≤ 4π/(3√32) = π/√18`. ∎

> **Corollary B1 (no graph theory needed).** If in addition every vertex has `deg(v) = 12`,
> then `(M)` holds with `c_e = 1/12` on every contact edge, so **`(L)` implies
> `δ ≤ π/√18`** outright. This covers every Barlow packing (`C094`: 12 contacts per site),
> and any saturated packing realising the kissing number everywhere.

### 3.1 The payoff is continuous, and the whole gap is `1.92%` in one constant

Theorem B is monotone in the pair constant, and this is the single most useful fact in this
file. Let `K` be any valid pair constant, i.e. `vol Ω(v) + vol Ω(w) ≥ K` for every contact
pair. Reading the same proof with `K` in place of `2√32`:

```
Σ_{v∈B} vol Ω(v)  ≥  (K/2) ( |B| − |E_B| − C_R )   ⟹   c(Λ) ≤ 2/K
⟹   δ(Λ)  ≤  8π/(3K) .                                        (B_K)
```

Two evaluations:

| `K` | source | `8π/(3K)` |
| --- | --- | --- |
| `2V_dod = 11.100582057` | Hales–McLaughlin, one cell, applied twice | `0.754697399337` — **exactly the dodecahedral bound** |
| `2√32 = 11.313708499` | `(L)` | `0.740480489693` — **exactly `π/√18`**, the truth |

So the bridge interpolates between the published bound and the truth with **no sharpness
barrier**: for any `K > 2V_dod`, however small the excess, `(B_K)` is a genuine improvement on
`0.754697399337`. Quantitatively,

```
K = 2V_dod·(1+ε)   ⟹   δ ≤ 0.754697399337/(1+ε),
```

and `2√32/2V_dod = √32/V_dod = 1.01919957`, so

> **The entire remaining gap between this route's floor and the Kepler bound is a `1.92%`
> increase in the two-cell constant `K`, from `2V_dod` to `2√32`.**

This is what makes the pair route structurally different from the routes already explored, and
it is worth stating plainly because it is the opposite of the situation everywhere else in this
project:

- **Pointwise cell bounds are dead by sharpness.** `vol Ω(v) ≥ V_dod` is *attained* (the
  dodecahedral cell, `C069`/`C095`), so no pointwise improvement exists at all — the pointwise
  route is stuck at `0.754697399337` with zero room.
- **The two-point LP is dead by an obstruction** (Li 2024, Thm 6.1): the plain class is
  provably not sharp in `d = 3`.
- **The pair bound has room**: `2V_dod` is *unattainable* for a contact pair (E's `K15-E075`,
  exact: the two icosahedral rings clash at `1.056487696 < 2`), and `2√32` is attained, so the
  true infimum lies strictly between `11.100582` and `11.313708` and every part of that
  interval is worth a real improvement in the density bound.

**So the target should be stated in the weaker, monotone form**, not only as `(L)`:

> **(L_δ) Weak pair bound.** There is `δ > 0` such that `vol Ω(v) + vol Ω(w) ≥ 2V_dod + δ` for
> every contact pair of every saturated 2-separated packing of `R³`.

`(L_δ)` for *any* `δ > 0` beats the published dodecahedral bound via `(B_K)`, and is strictly
weaker than `(L)`. It is the right thing to ask the workers for.

**Why this is the right bridge and E's is not.** E's arithmetic shows `(L)` is *sufficient*
for the one cut that binds; Theorem B shows `(L)` plus a matching statement is sufficient for
the density bound, with the local statement used once per edge and the counting done by `(M)`.
The two are not the same claim, and only the second is a density result.

## 4. Where the bridge actually fails — the honest gap

`(M)` is a fractional perfect matching condition, and by the fractional Tutte theorem it holds
iff for every finite `S ⊆ V`, the number of isolated vertices of `G − S` is at most `|S|`.
**It can fail, and the failure is exactly an isolated icosahedral cluster.** Take `S = {v}`
and suppose twelve centres touch *only* `v`; then `G − S` has twelve isolated vertices against
`|S| = 1`, so `(M)` fails. That configuration is legal and even sharp: twelve centres on the
sphere of radius `2` about `v` with mutual distance `≥ 2` is exactly the icosahedral twelve
(Tammes-12), i.e. the 13-cluster of `K15-C092`. So:

> **The bridge's hypothesis is not automatic, and the obstruction is precisely the loose
> cluster whose cells are large** (`C095`: each of those cells exceeds `√32`; the centre's is
> `V_dod`, deficit `b = +0.1066`, and the twelve ring cells have `b < 0`).

That is the compensating direction, which is why the gap is not fatal — but it is a gap, and
it is **bookkeeping, not geometry**: a proof must show that the vertices left unmatched can be
charged against their own (larger) cell volumes. The natural repair is to allow slack
`d_v ≥ 0` with `d_v + Σ_{e∋v}c_e = 1`; then

```
Σ_{v∈B} vol Ω(v)  ≥  √32|B|  −  (2√32 − 2V_dod)·Σ_{v∈B} d_v  −  √32 C_R ,
```

so the conclusion survives whenever the unmatched set has density zero — a strictly weaker
requirement than `(M)`, and the one a proof should aim at. **No proof of either form is known
to Main.**

## 5. 3D test and witness (comparison against the closest known result)

| witness | contact pairs measured | min pair sum | vs `2√32 = 11.3137084990` |
| --- | --- | --- | --- |
| fcc | 1752 (E's count) | `11.313708499` | **equality** |
| hcp | 212 (E's count) | `11.313708499` | **equality** |
| every Barlow stacking | all | `11.313708499` | **equality** — *proved*, `C094`+`C106` |
| A15 | 10098 | `15.875` | above |
| crack packing (`C095`) | bulk–bulk | `11.313708499` | equality in the bulk; crack–bulk pairs larger (crack cells are `6.985`) |
| icosahedral pair, E's `C5` payer | 1 | `5.550291 + 5.897967 = 11.448258` | above by `0.134549` |

The last row is the near-critical one and is E's: `v` is the dodecahedral centre (`vol = V_dod`
exactly) and `w` the best completion found, `5.897967122` over the `C5`-symmetric family with
the cell **exact** (no legal centre can cut it, E's `K15-E081`). So the margin at the sharpest
known witness is `0.1345`, i.e. `1.19%` of `2√32`. **That is the number a proof has to beat**:
`(L)` needs `vol Ω(w) ≥ 5.763417470 = 2√32 − V_dod` and the best legal value found is
`5.897967`.

**Comparison with the closest published result.** `(L)` is a two-cell version of the
dodecahedral inequality. The published one-cell bound gives `δ ≤ 0.754697399337`; `(L)` with
Corollary B1 gives `δ ≤ 0.740480489693`, the exact value — so the target is strictly stronger
than the published bound and clears the brief's bar. **Novelty is not established**: a
web search for a two-cell version of the dodecahedral inequality returned nothing usable, and
E independently records the same caution ("it should be checked before being called new"). It
is therefore carried as `PROPOSED`, not as new.

## 6. What is proved, what is not

**Proved.** `(L)` holds with equality on every Barlow packing (`C106`, from `C094`). Theorem B
and Corollary B1: `(L)` + a fractional matching off a density-zero set ⟹ `δ ≤ π/√18`;
`(L)` + uniform degree 12 ⟹ `δ ≤ π/√18`. The failure mode of the matching hypothesis is an
isolated icosahedral cluster (exactly the 13-cluster), and the failure is in the compensating
direction.

**Not proved.** `(L)` itself — this is E's open conjecture, and the necessary next step is a
lower bound `vol Ω(w) ≥ 5.763417470` for the partner of a dodecahedral cell (E's "payer"
problem: "nothing in this block supplies one"). The matching hypothesis `(M)`, or the
density-zero-unmatched repair. Novelty.

**Independent reviewer:** X. **Not a density result yet, and not to be quoted as one.**

---

# 4. `(L_δ)` is true: a compactness proof, and what it buys

The last section reduced everything to `(L_δ)`: *some* `δ > 0` with
`vol Ω(v) + vol Ω(w) ≥ 2V_dod + δ` for every contact pair. That looks like a weaker
conjecture, but it is not a conjecture at all.

> **Theorem D (`K15-C108`).** Let
> `σ₀ := inf { vol Ω(v) + vol Ω(w) : 2-separated configurations in R³ containing a pair
> v, w at distance exactly 2 }`, the cells taken in the full configuration. Then
> `σ₀ > 2V_dod`.

*Proof.* Four steps.

**(1) `σ₀ ≥ 2V_dod`.** Hales–McLaughlin gives `vol Ω ≥ V_dod` for each cell.

**(2) The infimum is attained.** Let `Φ = vol Ω(v) + vol Ω(w)`. Restrict to configurations
with `Φ ≤ 2V_dod + 1 =: C`. Each cell contains the ball of radius 1 (every bisector is at
distance `≥ 1` because every neighbour is at distance `≥ 2`), and it is convex; so for any
`x` in the cell at distance `r` from the centre, the cone from `x` over a unit disc
perpendicular to `x` lies inside the cell and has volume `πr/3`. Hence `r ≤ 3C/π =: R_max`
and both cells lie in `B(·, R_max)`. A centre whose distance from `v` exceeds `2R_max` has its
bisector outside `B(v,R_max) ⊇ Ω(v)` and cannot cut `Ω(v)`; so **`Φ` is determined by the
centres within `2R_max` of `v` or `w`.** That region is bounded, the centres in it are
2-separated so there are at most `N_max = vol(B(0,2R_max))/ (4π/3)` of them, and the set of
such local configurations — after fixing `v = 0`, `w = (2,0,0)`, which uses the translation
and rotation freedom — is closed and bounded, hence compact. `Φ` depends continuously on the
local configuration (a cell is the intersection of the half-spaces of the centres within
`2R_max`, and no other centre contributes). So `Φ` attains its minimum on the admissible set
and `σ₀ = min Φ ≥ 2V_dod`.

**(3) The minimiser is two dodecahedra.** Suppose `σ₀ = 2V_dod`. Then at a minimiser both
`vol Ω(v)` and `vol Ω(w)` equal `V_dod` (each is `≥ V_dod`). By the **equality case of
Hales–McLaughlin**, `vol Ω = V_dod` forces `Ω` to be the regular dodecahedron of inradius 1,
i.e. the centre has twelve neighbours at distance exactly 2 in the icosahedral directions and
no other centre cuts the cell.

**(4) Contradiction.** `v` and `w` are at distance 2, so each is among the other's twelve
contacts, and both cells would be dodecahedral. **Two adjacent centres cannot both be
dodecahedral**, and Main verified this independently (`Computation/two_dodecahedra.py`) rather
than citing E: with both twelve-point sets icosahedral about the shared `v`–`w` axis, the two
eleven-point sets (partner pole removed — the shared contact is at `+2` in `v`'s frame and `−2`
in `w`'s) have minimum mutual distance

```
max over the relative twist  of  min cross-distance  =  1.12555484451 ,
t = 0°, 18°, 36°, 54°:   1.1256,  0.5982,  0.2111,  0.5982     (required: 2)
```

so for **every** twist some pair is closer than `2`, with a shortfall of `0.874`. Hence
`σ₀ ≠ 2V_dod`, and with (1), `σ₀ > 2V_dod`. ∎

Three things are used and none is re-proved: the **equality case** of Hales–McLaughlin
(standard, from their proof); that a dodecahedral cell forces twelve tangent neighbours in the
icosahedral arrangement (the same equality case); and the two-dodecahedra impossibility (Main's
own computation, `1.1255548 < 2`, a `44%` shortfall so convention-insensitive).

**Discrepancy with E, recorded and not resolved.** E's `K15-E075` quotes `1.056487696`; Main
gets `1.12555484451` for the same stated configuration. Both are `< 2` and the conclusion is
identical, so Theorem D is unaffected; Main cites its own value and does not use E's. Main's
first version also removed the wrong pole for `w`, which is the same bug E records having made,
so the convention is now stated explicitly in the script.

**A caveat on exactness, per the supervisor.** E's `barlow_contact_cell.py` admits vertices by
`sp.N(...,30) > 1e-25` and compares radii numerically, so **it is not fully exact and is not
advertised as such here**; the exactness `C094` now rests on is Main's own
`contact_cell_exact.py` (`C104`), which uses exact field arithmetic and interval sign
decisions. `two_dodecahedra.py` is 40-digit numerics, not certified, and is recorded
`TESTED_FINITE`.

## 4.1 What Theorem D buys, and what it does not

`δ₀ := σ₀ − 2V_dod > 0` is the explicit number `(L_δ)` needs. It is **not** explicit — step 2
is a compactness argument and gives no value. What it does give is a genuine *qualitative*
improvement over the published dodecahedral bound, via a weaker bridge that needs no matching.

> **Theorem C (`K15-C108`).** Let `Λ` be saturated, let `M` be a **maximal** matching of its
> contact graph with `P_B` edges inside `B(0,R)`, and suppose `P_B/|B| → ρ`. Note
> **`0 ≤ ρ ≤ 1/2`**, because each edge of `M` uses two vertices of `B`. Then
>
> ```
> δ(Λ)  ≤  (4π/3) / ( V_dod + δ₀·ρ )  <  0.754697399337     whenever ρ > 0.
> ```

*Proof.* Every vertex is either matched or (by maximality) has all its neighbours matched.
Summing cell volumes over `B = Λ ∩ B(0,R)`,

```
Σ_{v∈B} vol Ω(v) ≥ Σ_{pairs ⊆ B} (vol Ω(v) + vol Ω(w)) + Σ_{unmatched ∈ B} vol Ω(v)
                 ≥ (2V_dod + δ₀) P_B + V_dod (|B| − 2P_B)
                 = V_dod |B| + δ₀ P_B .
```

Now `Σ_{v∈B} vol Ω(v) = (4π/3)R³ + O(R²)` by saturation (Theorem B step (i)), and
`P_B = (ρ + o(1))|B| = (ρ + o(1)) c(Λ)(4π/3)R³`. Dividing by `(4π/3)R³` and letting `R → ∞`,

```
1  ≥  V_dod c + δ₀ ρ c  =  c (V_dod + δ₀ ρ) ,      so  c ≤ 1/(V_dod + δ₀ρ) . ∎
```

Four consequences worth stating plainly.

1. **The pair route beats the dodecahedral bound in principle, unconditionally.** No fractional
   matching, no `(M)`, no compactness theorem: a *maximal* matching always exists, and `δ₀ > 0`
   is proved. For any saturated packing with a positive density of contact pairs,
   `δ < 0.754697399337` — strictly.
2. **The equality case of the dodecahedral bound is empty.** Equality in
   `δ ≤ (4π/3)/V_dod` would need *every* cell to be a dodecahedron, hence (step 3) every centre
   to have twelve contacts, hence a positive density of contact pairs, which Theorem C forbids.
   So the dodecahedral density bound is **never attained** — a clean corollary that does not
   need the matching machinery at all.
3. **The gain is proportional to the matching density `ρ ≤ 1/2`**, and the maximum
   `ρ = 1/2` (a perfect matching) together with the sharp `δ₀ = 2√32 − 2V_dod` gives
   `V_dod + δ₀/2 = √32`, hence `c ≤ 1/√32` — the truth. (Main's first draft of this display
   wrote `ρ = 1`, which is impossible for a matching and made the formula appear to beat the
   truth; corrected here. Any reader re-deriving it should keep `P_B/|B| ≤ 1/2` in view.) So
   the whole remaining content of the pair route is concentrated in two numbers: `δ₀`
   (geometric, E's payer problem) and `ρ` (combinatorial).
4. **What it does not buy: a number.** With `δ₀` non-explicit the improvement has no
   quantitative value, so nothing here may be quoted as a bound. It is a strictness statement,
   not a constant.

## 4.2 The two things that would make it a bound

- **An explicit `δ₀`.** This is precisely E's "payer" problem in a different guise. Careful
  bookkeeping: `δ₀ = σ₀ − 2V_dod` is measured from the **trivial** pair bound, not from the
  sharp one, so the witness gives `δ₀ ≤ 11.448258 − 11.100582 = 0.347676`
  (`3.13%` of `2V_dod`), while the *sharp* conjecture `(L)` would put
  `δ₀ = 2√32 − 2V_dod = 0.213126` (`1.92%`). The icosahedral witness's margin to the **sharp**
  bound is the separate number `0.134549` (`1.19%` of `2√32`) quoted in §5. Any explicit
  `δ₀ > 0` — even far below `0.213126` — combines with Theorem C to give a number, which is
  why `(L_δ)` is the right target and `(L)` is a bonus.
- **`ρ > 0` for every saturated packing.** This is the *combinatorial* half and it can fail:
  a saturated packing in which no two centres are at distance exactly `2` has `ρ = 0` and
  Theorem C says nothing. Whether such packings can be dense is a separate question — and by
  Hales' theorem a densest packing has plenty of contacts, so this is a statement about
  *sub*-densest packings, which is where a density bound is not needed. **This is the cleanest
  division of labour this project has produced: the pair route needs geometry for `δ₀` and
  combinatorics for `ρ`, and neither is a sharpness barrier.**

## 4.3 Status

| item | status |
| --- | --- |
| `(L)` sharp pair bound `≥ 2√32` | `PROPOSED`, E's `K15-E074`; equality proved on all Barlow packings (`C106`) |
| `(L_δ)` weak pair bound, some `δ > 0` | **`PROVED`** (Theorem D, `C108`) — non-explicit |
| Theorem B / B1: bridge via fractional matching / degree 12 | **`PROVED`** (`C106`) |
| Theorem C: bridge via a maximal matching + `δ₀` | **`PROVED`** (`C108`) |
| explicit value of `δ₀` | **open** — E's payer problem; `δ₀ ≤ 0.1345496515` from the icosahedral witness |
| `ρ > 0` for every saturated packing | **open**, and can fail; not needed for dense packings |
| improvement on `0.754697399337` as a *number* | **not achieved** |
