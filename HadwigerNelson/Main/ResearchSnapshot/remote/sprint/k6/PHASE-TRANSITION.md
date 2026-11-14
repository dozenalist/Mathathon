# The cyclic locus in the number of colours: true at 5, open at 6, false at >= 7

**Theorem.** For a weak measurable `k`-colouring of the plane let
`L_k = {x : Gamma_x contains a cycle}` (paper Definition 6.1 and (6.4)).

1. **`k = 5`:** `L_5` is closed and locally finite (Theorem 6.5 of the paper;
   machine-checked in the repository's Lean development).
2. **`k = 6`:** `L_6` is closed, non-empty and `1`-dense; whether it is locally finite for every
   weak measurable 6-colouring is **open**. Every palette-level necessary condition of the
   paper, including non-proper self-avoidance, is satisfied by explicit accumulating models
   (`sprint/k6/FREE-LABEL.md`), so no palette-level argument can decide it.
3. **`k >= 7`:** there is a **proper Lebesgue measurable** `k`-colouring with `L_k` **not locally
   finite**. Hence Theorem 6.5 is not a general-`k` theorem.

*Caveat (added later).* This is a phase transition for **local finiteness**, not for the hypothesis
`(W)` that §7 actually needs (finite `L` in one ball of radius `> 1`): the `k >= 7` colouring of
part 3 has a closed countable `L` with one accumulation point, and it **satisfies** `(W)` — a ball
of radius `3/2` centred away from the accumulation point meets only the base lattice. `(W)` is not
known to fail for any colouring at any `k` (`smwfycxze` m1, Prop. 7).

The phase transition is exactly at `k = 6`. The mechanism is the size of the outsider set of a
triangle, `k - 3`: it is `2` at `k = 5` (which forces binarity and Lemma 5.5), `3` at `k = 6`
(where a palette can meet the outsider triple in two or three labels), and `>= 4` at `k >= 7`
(which is what lets the construction of part 3 run four outsider palette values against a
three-label cycle).

## Part 1: `k = 5`

The paper's Theorem 6.5, pp. 37-41, proves closedness and local finiteness cycle by cycle
(triangle, four-cycle, five-cycle). The Lean module
`lean/OAI/Geometry/PlaneColoring/CyclicCore.lean` (and the surrounding `Transitions`,
`States`, `FourContinuity`, `FourTransport`, `FiveSupport` modules) machine-checks it; the
repository's build is `scripts/build_lean.py`, 83 modules, axioms
`[propext, Classical.choice, Quot.sound]`.

## Part 2: `k = 6`

* **Closed.** `L_6` is a finite union over simple cycles `C` of the closed sets
  `intersection_{ij in C} E_{ij}`, where `E_{ij} = {x : ij in Gamma_x}` is closed; the argument
  is the paper's and uses no palette information (`m12`, Theorem A).
* **Non-empty and `1`-dense.** `L_6` meets every closed square of side `> 2` (`m5`) and every
  closed disk of radius `> 1` (`m12`). The proof runs Lemma 7.4 with `L_0 = empty` and
  Lemma 7.6's cover argument with no core disks.
* **Open.** Whether `L_6` is locally finite is not decided. The conditional transfer
  (`sprint/k6/TRANSFER.md`, `WEAKEST.md`) shows that finiteness of `L_6` in one ball of radius
  `> 1` suffices for Proposition 7.1, and `sprint/k6/FREE-LABEL.md` shows that every
  palette-level constraint of §5-§6, including non-proper self-avoidance, is consistent with
  accumulating `ell`-cycle points for every `ell in {3,4,5,6}`.

## Part 3: `k >= 7` (the construction)

This is `m3`'s object, with its exact certificate in
`.ultramath/smwfo9zkl/m3/proof.md` and `verify.py` (32 checks). We recall the data.

Let `w = e^{2 pi i/3}`, `r = 2/5`, `d = sqrt(3) r = 2 sqrt 3/5`, `Lambda = d(Z + Z w)`. The
Voronoi hexagons of `Lambda` have circumradius `r` and inradius `sqrt 3/5`. Colour the centre
`d(m + n w)` by `(m + 2n) mod 7`; since `Norm(2 - w) = 7`, this is the paper's proper
seven-colouring `c_0` (same-colour centres are at distance at least `sqrt 21 r = 2 sqrt 21/5 =
1.8330... > 1 + 2r`).

Fix

```
p_0 = (1/55, 18/55),   ell = 1/100,   W = p_0 + [-ell/2, ell/2]^2,
q_n = p_0 + (ell 2^(-n-3), 0),   rho_n = ell 2^(-n-14),   D_n = B(q_n, rho_n).
```

The `D_n` are pairwise disjoint and lie inside `W`, and `diam W = ell sqrt 2 < 1`. Define `c`:

* on `D_n`, the Mercedes partition into three closed sectors of `120` degrees with labels
  `0`, `2`, `3`;
* on `W` minus the union of the `D_n`, label `0`;
* on the complement of `W`, `c = c_0`.

**Properness.** Two points of `W` are at distance `< 1`. Two points outside `W` have the same
colour as in `c_0`, which is proper. For `p in W` and `q not in W` with `|p - q| = 1`, the
shadow lemma gives `1 - eps <= |q - p_0| <= 1 + eps` with `eps = 71/10000 > ell/sqrt 2`; the
annulus `A = {1 - eps <= |q - p_0| <= 1 + eps}` meets no hexagon of `c_0`-colour `0`, `2` or `3`
(exact `Q(sqrt 3)` certificate, two independent methods: point-to-hexagon distances with slacks
`0.028950` for colour 2 and `0.017079` for colour 3, and a square cover with half-plane tests;
negative controls show colours `1,4,5,6` do occur in `A`). Hence `c(q) in {1,4,5,6}` while
`c(p) in {0,2,3}`.

**Cyclic centres.** At `x = q_n` the three sector interfaces are rays of the Mercedes partition.
The sector-transition lemma: if the colour is `i` on a sector of radius `rho` and `j` on the
neighbouring sector, then for `0 < tau <= min(rho,s)/4`,

```
|{q in B(x,s) : c(q) = i, c(q + tau n) = j}| >= (min(rho,s)/8) tau,
```

so `limsup_{h -> 0} |D_ij(B,h)|/|h| >= min(rho,s)/8 > 0`. Hence `{0,2}`, `{2,3}`, `{3,0}` are
all edges of `Gamma_{q_n}`, and `Gamma_{q_n}` contains the triangle `{0,2,3}`. The `q_n` are
distinct and converge to `p_0`, so `L_k` is not locally finite.

**Palettes.** The colouring is constant on the cells of a Borel partition with piecewise smooth
boundaries (hexagons, sectors, the background), so for every centre and a.e. direction
`P_x(e) = {c(x+e)}`: every palette is a singleton a.e., strictly stronger than the `k=5` and
`k=6` palette bounds. At the cyclic centres the singleton value runs through all four labels
`{1,4,5,6}`, and the triangle labels `{0,2,3}` occur in no palette, so the centres are not
binary for any fixed pair and Lemma 5.5 cannot apply.

## What the phase transition does and does not say

It does not decide `k = 6`, and it does not bound `chi(R^2)`. It shows that the printed
architecture's `k`-dependence is real and sits exactly at `k = 6`: a proof of the `k = 6` case
cannot be a general-`k` argument, and it cannot be a palette-level argument; it must use a
constraint that distinguishes a hypothetical 6-colouring from m3's 7-colouring, whose only
visible such feature is that the latter has four outsider labels rather than three.
