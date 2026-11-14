# The closed-component question: attempts, exact failures, one proved obstruction

Block `K15-REVIEW-0308-M-CONTINUE`, task 1. The question (`K15-C080`, `K15-C089`
step 0): **can a saturated 2-separated packing in `R³` have a closed component of the
`R = 2.09` graph with positive signed deficit `Σ_C b > 0`?** A "yes" refutes the
transfer route (not Kepler); a "no" removes the only case where `(T')` cannot be
avoided.

Definitions: `C` closed ⟺ no centre outside `C` is within `2.09` of a centre of `C`
(equivalently `|δ⁺_{2.09}(C)| = 0`); `b(v) = √32 − vol Ω(v)`.

## Proved obstruction (this block)

**Covering lemma.** If `v` is isolated at scale `2.09` (no other centre within
`2.09`) in a **saturated** packing, then at least **five** other centres lie in the
annulus `2.09 < |w−v| ≤ 4`.

*Proof.* Saturation: for every unit `u`, the point `x = v + 2u` must be within `2` of
some centre (otherwise a unit ball fits at `x`). That centre is not `v` itself
(distance exactly `2`), and by isolation it is not within `2.09` of `v`. So for each
`u` there is `w` with `ρ_w = |w−v| ∈ (2.09, 4]` and `|x − w| < 2`, which gives
`⟨û_w, u⟩ > ρ_w/4`. Thus `S²` is covered by the caps `C_w = {u : ⟨û_w,u⟩ > ρ_w/4}`,
of area `2π(1 − ρ_w/4)`. Since `ρ_w > 2.09`, each term is `< 0.4775`, and covering
`S²` needs `Σ(1 − ρ_w/4) ≥ 2`, hence `#A ≥ 5`. ∎

The bound is weak — it does not contradict anything — but it is a real constraint: an
isolated vertex is never "alone", it forces a shell of at least five centres.

## Attempt ledger

| # | attempt | exact failed condition |
| --- | --- | --- |
| A1 | singleton, twelve neighbours on the icosahedral directions pushed out to `2.09` (legal: mutual distances `2.1976 > 2`) | the cell is the dodecahedron scaled by `1.045`, volume **`6.333804`** against `√32 = 5.656854`: deficit `−0.677`, i.e. **negative**, not positive. The cheapest known isolated-vertex candidate has the wrong sign by 12%. **Upgraded by `K15-C102`**: `6.333804` is now the *true* cell volume, not the volume of the 12-half-space intersection, because no admissible extra centre can cut the cell (nearest admissible centre at `3.206871 > 2·R_cell = 2.955706`) |
| A2 | singleton, general | needs *all* faces at distance `≥ 1.045` **and** `vol Ω(v) < 5.6569`. Hales–McLaughlin gives only `vol ≥ V_dod = 5.5503`, so the admissible window is `(5.5503, 5.6569)` — `1.9%` wide. No argument closes it and no example fills it. **Open.** What a proof needs is stability of the dodecahedral inequality: cells with inradius `≥ 1.045` have volume `≥ V_dod·(1.045)³` **or** a bound in the same direction — neither is available |
| A3 | isolated dimer (two touching spheres, nothing within `2.09` outside) | each cell has a face at distance `1` (from its partner), so the "all faces far" argument is unavailable; no obstruction found. Volumes were not computed because the configuration is unbounded (an isolated dimer has unbounded cells) and any completion re-introduces edges. **No conclusion** |
| A4 | clusters of `≥ 3` | every cell has at least one near face inside the cluster, so the far-face argument gives nothing; the deficit is a *sum* over the cluster and could in principle be positive. **Open** |

## What is settled, and what it costs

- **Singleton closed component: not excluded, but the natural candidate has negative
  deficit** (A1) and the admissible volume window is `1.9%` wide (A2). A proof would
  need a stability version of Hales–McLaughlin; nobody has one.
- **No packing counterexample was constructed.** Every attempt failed on a named
  condition, recorded above.
- **The question stays open**, and it is `K15-C089`'s step 0: until it is settled, a
  proof of the cut condition must handle the closed case, and a single example would
  close the *transfer route* (though not Kepler).

---

# Addendum (block `K15-REVIEW-0308-M-CONTINUE`): three corrections and one sharp target

## A. "Closed" must mean "bounded"

The question above implicitly assumed `C` finite. That assumption is not removable: the
**crack packing** of `K15-C095` (`Main/GAP_FIXTURE.md`, `Computation/gap_fixture.py`) is a
saturated 2-separated packing whose `2.09`-graph has **two closed infinite components** —
two fcc half-spaces separated by a crack of width `d ∈ (1.633, 3.266]`, with the upper
half shifted sideways by `T` so the minimum cross-crack distance is `> 2.09` once
`d > 1.633`. Infinite closed components are therefore not exotic, and they are harmless:
every finite `U ⊆ C` still has out-edges, into `C∖U`.

> **Corrected obligation.** No **bounded** closed component `C` has `Σ_C b > 0`.

(Same correction applied in `K15-C089`, ledger.)

## B. A void is never the counterexample

In the crack packing at `d = 2.4` every crack-face cell has `vol Ω = 6.985349063`, i.e.
`b = −1.328495`, while every bulk cell has `vol Ω = √32` exactly. Cells next to a void
are *bigger* than `√32`, so `b < 0` there and the cut condition holds for free. So the
search for a violating component should not look at voids, vacancies, gaps or surfaces:
**only compression can produce `b > 0`.** The known source is the icosahedral 13-cluster
(`K15-C081r`). This is worth writing down because "find a packing that breaks the cut
condition" naturally suggests looking at holes, and holes are the wrong direction.

## C. A2 becomes a sharp, finite, testable target

A2 said the singleton case needs "a stability version of Hales–McLaughlin", that the
admissible window is `1.9%` wide, and that no such result is available. That is still
true, but the target can now be stated exactly (`K15-C096`):

```
V(ρ) := min{ vol Ω(0) : C 2-separated, every |c| ≥ ρ },     V(2) = V_dod (Hales–McLaughlin)
conjecture (S):   V(ρ) = V_dod·(ρ/2)³   on  2 ≤ ρ ≤ ρ_c
sharp threshold:  ρ* = 2(√32/V_dod)^{1/3} = 2.012718662…   ← √32 is crossed here
state at ρ=2.09:  V_dod(1.045)³ = 6.333804106 = 1.1197·√32
```

Three things this buys:

1. **The margin is 12%, not 1.9%.** The 1.9% window above is the *volume* window for an
   arbitrary cell; for an isolated vertex the cheapest configuration clears `√32` by
   `11.97%`. So the singleton case is not marginal at all — if `(S)` holds.
2. **A sharp constant to aim at.** Proving `V(ρ) ≥ V_dod(1 + 0.2133(ρ−2))` on `[2, 2.09]`
   suffices; proving `(S)` gives it for every `ρ ≥ 2.0127` at once.
3. **`ρ* < 2.09` is informative.** The threshold is `0.64%` above 2, whereas the graph
   radius is `4.5%` above 2. So the geometry is not close to the boundary — which is why
   the numerical probe finds a 12% margin rather than a near miss.

## D. What is still open

`|C| ≥ 2` is untouched by C. A member `v` of a multi-point `C` has neighbours *inside*
`C` at distance exactly 2, so `(S)` — which assumes all neighbours are far — does not
apply. Whether a small `C` can have all its cells below `√32` on average remains open, no
construction was found (A1–A4), and `A3`/`A4` were not computed. **The honest status is
unchanged: open, with the singleton case now reduced to a single explicit inequality.**
