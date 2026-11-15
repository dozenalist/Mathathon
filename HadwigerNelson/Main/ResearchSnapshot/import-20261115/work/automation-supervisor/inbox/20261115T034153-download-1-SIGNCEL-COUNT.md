# Sign cell / base chamber: the disputed count, and a verdict table on each record sentence

First-pass settlement for task (iii), written while swarm `smwh90qeq` is running (so no new swarm was
started). The full two-algorithm recount goes to the successor, as the desk specified; everything below is
what can be settled now from source text plus checks already run in this lane.

---

## 1. The three objects, defined exactly

None of "sign cell", "base chamber" or "resonance cell" is a Lean identifier. They are audit objects induced
by the Lean definitions, so I fix them here and name the Lean anchors.

**Anchors.** `Coloring.lean:15` `direction : Angles → ℂ` (the unit vector at angle `t`); `Coloring.lean:27`
`WeakColoring k c`; `Palettes.lean:35` `palette c hc x t`; `AngularBoundary.lean:259/:279` the two
restriction lemmas. The sign of interface `i` at phase `t` is `s_i(t) = sgn ⟨direction t, e^{iα_i}⟩ =
sgn cos(t − α_i)`; nothing in the tree names the cells, but the whole one-centre analysis depends only on
this sign function and on the six interface labels, so the arrangements below are the intrinsic ones.

**The two wall arrangements on `T^6 = (ℝ/360)^6`.**
* `W_60 := ⋃_{i<j} {α_i ≡ α_j (mod 60°)}` — the phases at which two interface directions have the same
  residue mod `60°`, equivalently the cut points `α_i ± 90° mod 60°` collide.
* `W_180 := ⋃_{i<j} {α_i ≡ α_j (mod 180°)}` — the same for `mod 180°`; note `W_60 ⊆ W_180` is FALSE and
  neither contains the other.

**Resonance cell** := a connected component of `T^6 ∖ W_60`. Count `933120 = 5!·6^5 = 120·7776`. These
are the cells that matter for the relaxation census, because the six-phase system on a shift orbit is
constant on them.

**Sign cell** := a connected component of `T^6 ∖ W_180`. Count `3840 = 5!·2^5 = 120·32`
(covering-space: `T^6 → (ℝ/180)^6` is a `(ℤ/2)^6`-cover, each base chamber lifts to `[(ℤ/2)^6:⟨(1,…,1)⟩] = 32`
pieces).

**Base chamber** := a connected component of `(ℝ/180)^6 ∖ {α_i ≡ α_j (mod 180°)}`, i.e. a **cyclic order**
of the six residues mod `180°`. Count `120 = 5!`. A sign cell is a base chamber plus a lift class
`ε ∈ (ℤ/2)^6/⟨(1,…,1)⟩`, so `3840 = 120 × 32`.

**A second, different 120.** A cyclic order of the six residues mod `60°` also numbers `5! = 120`. The two
120s are different objects and the whole dispute is a collision between them. This is the root cause, and
it should be named in any summary.

---

## 2. Verdict table on the disputed sentences

| sentence | verdict | exact reason |
|---|---|---|
| "16 of 3840 sign cells" | **FALSE** (category error) | 16 is a count of *base chambers* met (out of 120), not of sign cells. The SAT set meets **62** of the 3840 sign cells (m4's full census, whose 62 fills I checked sum to 1440), and my own ten-order sample already reaches **44** distinct sign cells, so 16 cannot be the sign-cell figure. |
| "16 of 120 base chambers" | **TRUE** | The SAT set meets exactly 16 of the 120 base chambers, each carrying exactly 90 of its SAT resonance cells: `16 × 90 = 1440`. Uniform at that level. |
| "720 of 3840" (L-R1 recount) | **FALSE** as stated | `720 = 6!` is the number of *linear* orders of six points, a third level that appears in no cell count here. The sign-cell figure met is 62; the base-chamber figure is 16; the linear-order figure is not a component count at all. |
| "120 of 120" (L-R1 recount) | **TRUE only at the mod-60 level** | All 120 mod-`60°` cyclic orders are met, each with exactly 12 SAT resonance cells (`120 × 12 = 1440`). At the mod-`180°` level it is **16 of 120**, not 120 of 120. So the sentence is true of one 120 and false of the other. |
| R1-1(e) "one sign cell" | **ILL-POSED** when the first vector is a wall point | A wall point lies in no open cell, so "the sign cell of that vector" has no referent. The sentence must name an open cell (a representative strictly inside it) or be restated at the wall as a limit. |

---

## 3. Evidence behind each row

* `933120 = 120·7776` and `3840 = 120·32`: derived twice in this lane (diagonal quotient and
  covering-space monodromy), independently reproduced by three members of the previous swarm, and the
  covering-space argument was BFS-checked at `n = 2,3,4` giving `2, 8, 48 = (n−1)!2^{n−1}`.
* SAT count `1440 = 120 × 12`: I verified **12 SAT resonance cells for each of ten random mod-60 orders**
  by enumerating all 7776 lifts per order with my own orbit solver (`CHECK-ORBIT.py`), and five members
  reproduced 1440 by different routes.
* The 16 base chambers: the earlier swarm's sixteen explicit representatives are 16 distinct mod-180
  cyclic orders, I verified every one is SAT, and m4's full census independently reports "90 per mod-180
  cyclic order, 16 met, uniform".
* The 62 sign cells: m4's full enumeration, run by me; the fills list has 62 entries summing to 1440 with
  values 1…83, so **every met sign cell is mixed** (each holds 243 resonance cells).
* My ten-order sample reaching 44 distinct sign cells is the independent check that kills "16 sign cells":
  a sample of ten orders cannot meet more cells than the whole census does.

---

## 4. What the successor must still produce for task (iii)

A full recount with **two independent algorithms** over all `933120` resonance cells, exact integer or
rational arithmetic, open cells only, walls handled explicitly, one checker script under a second with
sha256, plus the verdict table above checked against both. Concretely:

1. Algorithm A: enumerate `(cyclic order mod 60, m ∈ (ℤ/6)^5)` directly and decide each cell's six-cycle
   system by exact DP, memoised on the orbit data.
2. Algorithm B: enumerate by `(cyclic order mod 180, ε, layer)` — i.e. build the sign cells first and
   subdivide each into its 243 resonance cells — and decide by a different solver (e.g. a Petersen-graph
   formulation of the three-colour-free transition, as one member proposed).
3. Report `#{cells met}` at each of the four levels: resonance (1440), sign cell (62), base chamber (16),
   mod-60 cyclic order (120), and check `1440 = 62·?` is not asserted (it is not a clean product) while
   `1440 = 120·12 = 16·90` both hold.

Until that lands, the quotable sentences are: **"1440 of the 933120 resonance cells are SAT; the SAT set
meets 16 of the 120 base chambers with 90 each, and 62 of the 3840 sign cells with non-uniform fills"** —
and no sentence of the form "16 of 3840".
