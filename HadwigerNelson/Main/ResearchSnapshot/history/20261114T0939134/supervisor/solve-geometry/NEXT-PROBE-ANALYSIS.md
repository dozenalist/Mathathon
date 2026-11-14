# Analysis only: a rigorous search window for the bottom sliver, and the next probe

No experiment in this block (the graph chat owns the compute slot). Everything below is derivation;
grades **[P]** exact hand derivation, **[A]** previously machine-checked in this directory,
**[X]** estimate, not computed.

## 0. The corrected standing result, with properness explicit

**Theorem (honeycomb, cell-constant, proper).** Let `a ∈ (1/√28, 1/2]`. Then **no proper colouring of
the plane with at most 6 colours** is constant on the interior of every Voronoi cell of the triangular
lattice of spacing `a√3`. (Properness is essential and is part of the statement: a constant colouring
is interior-constant and uses one colour.) Unconditional: two accepted machine certificates cover
`(1/√28, 1/√19)` and `(1/5, 1/√12)`, and the audited `K_7` argument covers `(1/√13, 1/2]`.

**Scope, stated to prevent the standard over-read.** This excludes the six-colourability of *one
family* — colourings constant on honeycomb cell interiors — over one interval of one parameter. A
6-colouring of the plane need not be constant on any cell, and it need not respect any tiling, so
nothing here bounds `χ(ℝ²)` in either direction; in particular, excluding every cell-constant family
would still not settle the plane. No `χ = 8` claim is made or implied.

## 1. Rigorous finite search window for strictly forced offsets, at any `a` [P]

Let `H` be a cell (circumradius `a`, inradius `a√3/2`) and recall that distances realised between `H`
and `H + v` fill the open interval whose endpoints are the distances from the origin to the
Minkowski difference `2H + v`. With `|v| = a√3·√N` and `2H` of circumradius `2a`, the two one-sided
bounds are exact and elementary:

    dist(0, 2H+v) ≥ |v| − 2a,        max_{w ∈ 2H} |v+w| ≤ |v| + 2a.

Strict forcing at `a` means `dist(0,2H+v) < 1 < max|v+w|`, so a **necessary** condition is

    |v| − 2a < 1 < |v| + 2a        ⟺        |√(3N) − 1/a| < 2      (using |v|/a = √(3N))

i.e.

> **window(a):** `N` can be strictly forced only if `(1/a − 2)² < 3N < (1/a + 2)²`.

Both ends are strict, both are computed from exact rationals once `a` is rational, and no search
truncation is involved. Two consequences:

* **It is finite for every `a > 0`** and computable by hand: at `a = 1/6`, `(4)² = 16 < 3N < 64` gives
  `5.34 < N < 21.33`, so `N ∈ {7, 9, 12, 13, 16, 19, 21}`.
* **It grows as `a` shrinks**, roughly like `N < 4/(3a²)`: to reach smaller `a` the forced offsets move
  outward, so the patch radius must grow like `1/a²`. That is the real obstacle in the bottom sliver,
  not the algebra.

Ring windows from the accepted exact table [A] (`μ², ν²` at `a = 1`), with ring 16 added here [P]
(`μ16² = 27` since the neighbour direction is the edge normal and `2H` has inradius `√3`;
`ν16² = 76` from `48 + 4 + 2·4√3·2·cos30° = 76`):

| ring `N` | `μ²` | `ν²` | strictly forced on |
|---|---|---|---|
| 4 | 3 | 28 | `(1/√28, 1/√3)` = (0.188982, 0.577350) |
| 7 | 7 | 43 | `(1/√43, 1/√7)` = (0.152499, 0.377964) |
| 9 | 12 | 49 | `(1/7, 1/√12)` = (0.142857, 0.288675) |
| 12 | 16 | 64 | `(1/8, 1/4)` = (0.125, 0.25) |
| 13 | 19 | 67 | `(1/√67, 1/√19)` = (0.122169, 0.229416) |
| 16 | 27 | 76 | `(1/√76, 1/√27)` = (0.114708, 0.192450) |

These are the **regime boundaries** of the family: each is the point at which one ring enters or
leaves the forced set, and by the interval argument each patch certificate covers exactly the
`a`-range on which its own rings stay forced. The bottom sliver `(0, 1/√28]` therefore contains
infinitely many such intervals; it cannot be closed by finitely many certificates of this shape
without a uniform argument, and that is worth knowing before anyone plans a sweep.

## 2. The proposed next probe (specification, to be run by whoever holds the compute slot)

**Parameter: `a = 1/6`** (rational, `a² = 1/36`, so `|v|² = 3a²N = N/12` — exact arithmetic in `Q(√3)`
throughout). It lies in `(1/√43, 1/√28) = (0.1525, 0.1890)`, so rings `{7,9,12,13,16}` are all strictly
forced there (`36` offsets: `12+6+6+12+6`), and rings `19, 21` are *candidates* by `window(1/6)` and
must be decided exactly at run time.

**Patch: `P = {v : N(v) ≤ 25}`, 91 cells.** Sizing [P]: `|{N ≤ 19}| = 73`, `+12` for `N = 21` (`r = 6`),
`+6` for `N = 25` (`r(25) = 6` since `5²` with `5 ≡ 2 mod 3` even exponent) gives `73 + 12 + 6 = 91`.
The radius must exceed the largest forced `N` for the offsets to be usable near the centre; 25 is the
smallest ball that does so with margin if `N = 21` is forced. Fallback: if the run-time forced set is
`{7,9,12,13,16}` only, `P = {N ≤ 19}` (73 cells) suffices.

**Estimated counts [X]** (method: `E = (|F|/2)·n·ρ` with `ρ` calibrated on the accepted patches,
`ρ = 888/(21·73) = 0.579` for `a = 1/5`):
* variables `6·91 = 546`;
* `|F| = 36` (or up to `66` if rings 19 and 21 are forced), centre degree `|F|`;
* edges `E ≈ 0.579·18·91 = 948` for `|F| = 36`, rising to `≈ 1739` for `|F| = 66`; range
  `950 ≤ E ≤ 1750`, expected `≈ 1300` [X];
* clauses `= 91 + 91·15 + 6E = 1456 + 6E ∈ [7156, 11956]`, expected `≈ 9300` [X].

That is the same order as the accepted instances (6496 and 5506 clauses, 3.4 MB and 74 KB proofs), so
one bounded run with the established `drat-trim` is realistic.

**Exit criteria.** UNSAT ⟹ no proper interior-constant 6-colouring for every
`a ∈ (1/√43, 1/√28)` (the interval on which rings 7–16 stay forced), and with `§0` the union becomes
`(1/√43, 1/2]`. SAT ⟹ an explicit cell-constant 6-colouring at `a = 1/6`, i.e. a new positive object
for the family (not for the plane).

## 3. Why this probe, and not another periodic quotient

1. **Decisive in both outcomes.** A patch UNSAT is a no-go for *all* colourings of the infinite graph —
   it cannot be evaded by dropping a period. A periodic quotient `ℤ²/mΛ` decides only its own period
   class: UNSAT excludes periodic colourings with that period and nothing else, while SAT *does* give a
   genuine periodic colouring. So quotients are informative in the **positive** direction, patches in
   the **negative** direction, and the bottom sliver's open question is negative.
2. **Interval robustness.** A patch certificate at one `a` covers the whole `a`-range on which its rings
   stay forced (precedent: `p19` covered `0.189–0.229`, `p25` covered `0.200–0.289` — length `0.04` and
   `0.09` from single runs). A periodic colouring is one parameter value, with no such transfer.
3. **The periodic direction is already where the positives are.** The paper's own seven-colouring is
   `(m,n) ↦ m + 2n mod 7` on the index-7 sublattice at `a = 2/5`, and the `K_7` obstruction is a
   quotient-free witness; the family's remaining questions are all negative ones.
4. **Both outcomes transfer.** If the patch is SAT, the colouring is a real object (it would say the
   family is 6-colourable at `a = 1/6`); if UNSAT, the interval extends. Nothing is wasted either way.

## 4. What this does not do

It does not touch `χ(ℝ²)`; it does not exclude cell-constant colourings of *other* tilings; it says
nothing above `1/2` (vacuous) and nothing about the infinitely many intervals below `1/√43` that this
probe would leave; and no `χ = 8` statement is supported by any certificate in the family.
