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
| A1 | singleton, twelve neighbours on the icosahedral directions pushed out to `2.09` (legal: mutual distances `2.1976 > 2`) | the cell is the dodecahedron scaled by `1.045`, volume **`6.333804`** against `√32 = 5.656854`: deficit `−0.677`, i.e. **negative**, not positive. The cheapest known isolated-vertex candidate has the wrong sign by 12% |
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
