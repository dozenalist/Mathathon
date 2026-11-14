# The crack packing: an infinite closed component, an equality case, and a
# correction to the closed-component question

Block `K15-REVIEW-0308-M-CONTINUE`, task 1 (addendum). Prompted by `K15-C089`, which
says that a packing with a *closed* component of the `R`-graph and `Σ_C b > 0` has
`t*(Λ) = ∞`. This file shows that the statement is only true for **bounded** `C`, by
constructing a saturated 2-separated packing with two **infinite** closed components.
The construction is elementary and turns out to be interesting on its own: it is a
*second* equality case of Kepler's bound, and it is not a Barlow packing.

## 1. The construction

`Λ` triangular with nearest neighbour 2, `T = (a₁+a₂)/3`, `H = √(8/3)`. Take the `ABC`
stacking (i.e. fcc) and cut it at the plane `z = 0`; keep the layers `k ≤ 0`. Keep the
layers `k ≥ 0` as well, but translate them **up by `d`** and sideways by `T`:

```
lower half:  ( Λ + (k mod 3)T ) × {kH},          k ≤ 0
upper half:  ( Λ + ((1+k) mod 3)T ) × {d + kH},  k ≥ 0
```

Both halves are fcc; the horizontal offset `T` is what keeps the two halves 2-separated
across a wide crack (it makes the in-plane nearest distance `2/√3` instead of `0`).

`Computation/gap_fixture.py` checks, for a range of `d`, the minimum separation over
**all** pairs and the covering radius:

| `d` | min separation | min cross-crack distance | 2.09-graph | covering radius (sampled) |
| --- | --- | --- | --- | --- |
| 1.633 | 2.000000 | 2.000006 | connected | 1.379 |
| 1.800 | 2.000000 | 2.138535 | **disconnected** | 1.427 |
| 2.000 | 2.000000 | 2.309401 | **disconnected** | 1.469 |
| 2.090 | 2.000000 | 2.387767 | **disconnected** | 1.512 |
| 2.400 | 2.000000 | 2.663331 | **disconnected** | 1.635 |
| 2.800 | 2.000000 | 3.028751 | **disconnected** | 1.754 |
| 3.200 | 2.000000 | 3.401960 | **disconnected** | 1.932 |

So for `1.633 < d ≤ 3.266` the packing is 2-separated **and saturated** (the upper bound is
required: `d ≤ 2H = 3.265986` is exactly the saturation condition, and without it the crack
is a void too wide to be covered — E's review catches this as an overstatement in the first
version, which said only `d > 1.633`), and for `2.09 < d ≤ 3.266` the `2.09`-graph has two
connected components, each closed (no edge crosses the crack). Two
bounds are analytic, not just sampled:

- *2-separation across the crack* needs `d² + 4/3 ≥ 4`, i.e. `d ≥ √(8/3) = H = 1.633`
  (hence the sharp first row);
- *saturation* needs `d/2 ≤ √(4 − 4/3)`, i.e. `d ≤ 2H = 3.266` — the mid-crack point is
  at distance `√((d/2)² + (2/√3)²) ≤ 2`, and points outside the crack are in a
  half-space of fcc, covered at `√2`.

## 2. Why this corrects `K15-C089`

`K15-C089`'s prior obligation reads: "if a packing has a **closed** component `C` with
`Σ_C b > 0`, then `t*(Λ) = ∞` and no transfer exists". For a **bounded** `C` that is
right: `δ⁺(C) = ∅`, so the cut condition reads `Σ_C b ≤ 0`.

For an **infinite** `C` it is not right, and the crack packing is the counterexample to
the framing: `C` is closed, yet every *finite* `U ⊆ C` has `δ⁺(U) ≠ ∅` (its edges to
`C∖U`), so the cut condition is a genuine finite-cut condition there. Nothing degenerates.
The corrected statement, which is what the ledger should carry:

> **The obstruction is a bounded closed component.** A finite set `C` with `δ⁺_R(C) = ∅`
> and `Σ_C b > 0` gives `t* = ∞` and refutes the transfer route. Infinite closed
> components exist (this file) and are harmless.

Consequently `Main/CLOSED_COMPONENT.md`'s question is correctly about *bounded* `C`,
which is what its `Σ_C b` implicitly assumed; the ledger entry is amended.

## 3. The crack costs volume — in the **helpful** direction

Cell volumes in the crack packing at `d = 2.4`, computed by the half-space machinery of
`Computation/barlow_cells.py`, per layer (all cells in a layer are congruent, the packing
being `Λ`-periodic in each half):

| layer | `vol Ω` | `b = √32 − vol Ω` |
| --- | --- | --- |
| lower `k = 0` (crack face) | 6.985349063 | **−1.328495** |
| lower `k = −1, −2, −3` | 5.656854249 | 0.000000 |
| upper `k = 0` (crack face) | 6.985349063 | **−1.328495** |
| upper `k = 1, 2, 3` | 5.656854249 | 0.000000 |

Two things to read off:

1. **A void never violates the cut condition.** Cells next to a crack are *larger* than
   `√32`, so `b < 0` there and `Σ_U b ≤ 0 ≤ Φ|δ⁺(U)|` holds for free. Only *compression*
   (`b > 0`, cells smaller than `√32`) can force `Φ > 0`; the only known source of that
   is the icosahedral cluster (`K15-C081r`). This is worth stating once because "find a
   packing that breaks the cut condition" is a natural instinct, and voids are the wrong
   place to look.
2. **The surfaces are the only defective part.** The bulk is exactly `√32` — the same
   number `K15-C094` proves for Barlow packings — which is a second, independent check of
   that value.

The *crack energy* is `2 × 1.328495 × (2√3)⁻¹ = 0.767` per unit area of crack. It is
`O(r²)` in a ball of radius `r`, so it does not affect the density.

## 4. A second equality case of Kepler's bound, and what it rules out

Count the centres in `B(0,r)` centred on the crack: the lower half and the upper half each
contribute `c_fcc·(half ball)` minus an `O(r²)` correction, and the layers displaced by
the crack contribute an `O(r²)` deficit (one crack is a single surface, so the layers
"lost" number `d/H − 1 = O(1)`, not `O(r)`). Hence

```
lim_{r→∞} #(Λ ∩ B(0,r)) / vol B(0,r)  =  1/√32 ,
```

so `δ(Λ) = π/√18` **exactly**. The packing is saturated, is not fcc, is not hcp, and is
**not a Barlow packing** (its layers are not at height `kH` with `±1 mod 3` steps: the
step across the crack is `d/H ∉ Z`). So:

> **The equality case of Kepler's bound contains packings that are not Barlow.** Any
> planar fault — a crack as here, a twin, a stack of faults — is an equality case, so
> there are continuum many equality cases and they are not classified.

Two consequences for this project:

- **`densest` does not imply `b ≡ 0`.** `K15-C094`'s corollary says Barlow `⟹ b ≡ 0`;
  this file shows the converse fails at the level of *equality cases*, so "all cells are
  `√32`" is strictly stronger than "densest". Combined with `K15-C069` (the dodecahedral
  cell of the 13-cluster satisfies `vol Ω < √32` in a saturated packing), `b ≤ 0`
  everywhere is **false**, hence the cut condition at `Φ = 0` is false, hence `Φ > 0` is
  necessary — a second, independent route to the conclusion of `K15-C081r`.
- **A sharp certificate in `d = 3` cannot rest on uniqueness of the extremiser.** This is
  the concrete form of the non-uniqueness obstruction recorded in the `d = 3`
  sharp-certificate study: complementary slackness for a sharp `f` would need `f` to
  vanish on the shell radii of *every* equality case.

## 5. Not claimed

- Not a counterexample to Kepler: the crack packing is an equality case, as it must be.
- Not a new bound, and no number in `RESULTS.md` moves.
- The crack energy `0.767` per unit area is computed for `d = 2.4` only; the other `d`
  were not measured. It is not used anywhere.
