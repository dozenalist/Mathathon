# Independent audit of `CELL-NOGO-v2.md` Theorem 2, and the resulting union

Target: `supervisor/solve-independent/CELL-NOGO-v2.md` (read-only). My checks:
`checks/cellnogo2.py`, output §[18]-[21] of `supervisor_checks.out`. Grades as before:
**[A]** machine-checked here, **[P]** exact derivation written out, **[S]** read, **[X]** claim only.

## 1. The theorem as stated, with every quantifier

> **Theorem 2.** Let `a > 1/√13` and let `c : ℝ² → {colours}` be constant on the interior of every
> honeycomb cell (values on the 1-skeleton arbitrary). Then `c` uses at least 7 colours. For `a > 1/2`
> this is vacuous (a cell interior then contains a unit pair); on `(1/√13, 1/2]` it is proved from the
> forced set below.

Quantifier inventory, made explicit:
* over **all** `a > 1/√13` (a real parameter, not a sequence; no uniformity in `a` is claimed beyond
  the interval decomposition);
* over **all** colourings `c : ℝ² → κ` for any colour set `κ` — the proof never uses finiteness, only
  that cells get one value each;
* the hypothesis is "constant on the **interior** of every cell", with the 1-skeleton arbitrary —
  so the conclusion is independent of any ownership rule for boundaries;
* the conclusion is a *lower bound on the number of colours*, i.e. a no-go; equivalently, no
  colouring with ≤ 6 colours (and no proper 2-, 3-, …-colouring of this class) exists;
* the family is fixed: the Voronoi cells of the triangular lattice of spacing `a√3`, interiors
  pairwise disjoint.

## 2. What it must be proved from — and the containment point

The only graph-theoretic input is: **the forced-offset set contains `{1,3,4}`** (Eisenstein norms).
Containment, not equality, is what is needed, because extra forced offsets only add edges and a
`K_7` in a subgraph forces ≥ 7 colours in the whole graph. The document states something stronger
(the *exact* forced set on three sub-intervals, `{1,3,4,7,9}`, `{1,3,4,7}`, `{1,3,4}`); the stronger
statement is not required by the proof and its extra content is used only for the sharpness discussion.
The three sub-intervals are `(1/√13, 1/√12)`, `(1/√12, 1/√7)`, `(1/√7, 1/2]`, and on each the set
contains `{1,3,4}` — verified exactly, not sampled [A] §3.

## 3. The certificate: an explicit finite graph, no search

**The obstruction is a `K_7`**, with no computation needed beyond integer arithmetic:

    S = {(0,0), (1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)}      (the centre plus its six ring-1 neighbours)

**All 21 pairwise differences have Eisenstein norm in `{1,3,4}`** [A]: norms realised are exactly
`{1,3,4}`, with `1` from the 6 unit steps, `3` from 6 of the "diagonal" pairs, and `4` from the 3
opposite pairs. So the seven cells `{H_a + a√3·v : v ∈ S}` are pairwise *strictly forced*, hence must
receive pairwise distinct colours: `c` uses ≥ 7 colours.

**Seven is attained** [A]: `(p,q) ↦ p + 3q mod 7` is zero-free on all **18** vectors with
`0 < N ≤ 4` (values `1,2,3,4,6` occur, `0` and `5` do not), so the induced Cayley graph is
7-colourable. Hence `χ(Cay(ℤ², {N ∈ {1,3,4}})) = 7` exactly.

Neither step is a search: the `K_7` is a 7-element witness and `p + 3q mod 7` is a closed-form
colouring. This is the "explicit finite graph or direct proof" in its cheapest possible form.

## 4. The windows, and the endpoints

Forcing of a ring is `μ_N < 1/a < ν_N` with `μ, ν` the `a = 1` extrema of the difference-body
polygon `2H` (exact `Q(√3)`, `checks/interval_a1.py`). The `a = 1` values `(μ², ν²)` and the windows
[A]/[P]:

| ring `N` | `μ²` | `ν²` | strictly forced on |
|---|---|---|---|
| 1 | 0 | 13 | `(1/√13, ∞)` |
| 3 | 1 | 25 | `(1/5, 1)` |
| 4 | 3 | 28 | `(1/√28, 1/√3)` |
| 7 | 7 | 43 | `(1/√43, 1/√7)` |
| 9 | 12 | 49 | `(1/7, 1/√12)` |
| 12 | 16 | 64 | `(1/8, 1/4)` |
| 13 | 19 | 67 | `(1/√67, 1/√19)` |

These agree with the document's table exactly, and with the two accepted certificates' rings
(`a = 1/5` also needs `13`, `a = 1/4` needs `{3,4,7,9}`).

**Window sufficiency** [A]: a ring forced at `a ≥ 1/√13` satisfies `μ² < 13`; among representable
norms only `N ∈ {1,3,4,7,9}` have `μ² < 13` (`μ² = 0,1,3,7,12`; `N = 12` has `μ² = 16`). So no ring
with `N ≥ 12` can ever be forced in this range and the enumeration is complete. (The document reaches
this via `dmin ≥ |v| − 2`; that is a valid one-sided bound — `dmin = dist(0,2H+v) ≥ |v| − 2a` — and the
conclusion is the same. My check uses the exact table instead.)

**Endpoint `a = 1/2` (included).** All three rings `1, 3, 4` are still strictly forced at `a = 1/2`
(`μ² < 4 < ν²` for `N = 1,3,4` [A]), so the `K_7` argument applies **at** `a = 1/2`; this is *not* the
vacuous case. The vacuity note in the document refers to `a > 1/2`, where a cell interior has diameter
`2a > 1` and does contain a unit pair, so no proper cell-constant colouring exists at all (the
statement is then true for the trivial reason). At `a = 1/2` exactly, the interior diameter is `1` as
a supremum between opposite vertices and is not attained inside, so cells are individually
unconstrained and the graph argument is the substance.

**Endpoint `a = 1/√13` (excluded, and the exclusion is genuine).** Ring 1 has `ν² = 13`, so
`1/ν = 1/√13` exactly: at `a = 1/√13` the offset's distance window is `(0, 1)` open and contains no
`1` realised by interior points (the unit pair is boundary-only), so ring 1 is **not** forced and the
`K_7` does not exist there. This is a real tangency, not a numerical artefact. What remains at
`a = 1/√13` is the forced set `{3,4,7,9}`-part, and whether *some other* finite 7-chromatic subgraph
sits there is **open** — the document says only `a > 1/√13` and that is the honest scope.

**Audit verdict on Theorem 2: accepted** as stated, for the restricted honeycomb family. Three
substantive qualifications, none of them an error: (i) it needs only `⊇ {1,3,4}`, so the exact-set
table is stronger than necessary; (ii) `a = 1/2` is covered by the clique, not by vacuity; (iii)
`a = 1/√13` is genuinely open rather than "nearly covered".

## 5. The union, now unconditional

* Machine certificate 1 (`p19`, audited): `a ∈ (1/√28, 1/√19)`.
* Machine certificate 2 (`p25`, audited): `a ∈ (1/5, 1/√12)`.
* Theorem 2 (audited here): `a ∈ (1/√13, 1/2]`.

`1/√13 = 0.2773501 < 0.2886751 = 1/√12`, so the third overlaps the union of the first two, and

> **For every `a ∈ (1/√28, 1/2]`, no colouring of the plane that is constant on the interiors of the
> Voronoi honeycomb cells (circumradius `a`, spacing `a√3`) is proper with six colours.**

is now **unconditional within the cell-constant family** (it needs no further audit). Above `1/2`
the family is vacuous; below `1/√28` nothing is known (the bottom sliver `(0, 1/√28]`).

**Scope, stated once more.** This is a statement about colourings that are constant on cell interiors.
A hypothetical 6-colouring of the plane need not be constant on any cell, so nothing here bounds
`χ(ℝ²)` in either direction. No `χ = 8` claim is made: the two patches certify only "no 6-colouring".

## 6. Correction carried out this block [P]

`|v| + 2h(v̂) = max_{w ∈ 2H} ⟨v + w, v̂⟩` is the maximum *projection* onto `v̂`; since
`|x| ≥ ⟨x, v̂⟩`, it is a **lower bound** for `dmax = max_w |v+w|`. A lower bound exceeding `1` therefore
**does** certify `dmax > 1` — that inference is valid and may be used. The earlier error was only in
calling the expression an *upper* bound (and hence unusable for the `dmax > 1` side). What is not
available from this quantity is an upper bound on `dmax`, which the certificate does not need: `dmin`
and `dmax` are computed exactly from the polygon. The blanket "cannot certify" sentence is removed from
`HONEYCOMB-FAMILY-CERTIFICATE.md` and `PATCH19-AUDIT.md`.
