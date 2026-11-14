# T2. The lower bound survives deleting any null set

**Status: proved and machine-verified** (`lean/OAI/Geometry/PlaneColoring/NullSetRobust.lean`).

## Theorem T2

For every Lebesgue-null set `Z ⊆ ℂ`, the unit-distance graph induced on `ℂ \ Z` has no proper
5-colouring:

```
OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null :
  ∀ {Z : Set ℂ}, volume Z = 0 → ¬ ∃ c, ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y
```

`#print axioms` reports `[propext, Classical.choice, Quot.sound]`.

## Proof

Let `c` 5-colour `ℂ \ Z`. Every finite `F : Finset ℂ` can be translated off `Z`: the set of bad
translations is `⋃_{x ∈ F} (Z − x)`, a finite union of null sets, hence null, hence not all of `ℂ`.
So `x ↦ c (x + v)` properly colours `F`. Thus every finite configuration is 5-colourable, and the
compactness theorem `exists_properColoring_of_finset` (proved in `Converse.lean`) produces a proper
5-colouring of the plane, contradicting `no_proper_five_coloring`.

## Consequences

* Removing a point, a line, a circle, or any countable set does not lower the chromatic number:
  `χ(ℂ \ Z) ≥ 6` for every null `Z`. In particular `χ(ℂ \ {0}) ≥ 6`: the lower bound is not an
  artefact of a single point or of a degenerate configuration.
* Any proper 6-colouring of the plane (if one exists) must be irreducibly global: it cannot be
  obtained by colouring the plane minus a null set and extending, since by Theorem 1.3 the
  deleted set would still have to carry a 5-colouring obstruction.
* The same argument gives the meager version whenever `ℂ` is replaced by a space in which meager
  sets are not everything (Baire), and the cardinality version for `|Z| < 𝔠`; the Lean proof above
  implements the measure case only.

## Stronger form (swarm member m9)

The deletion-stability proved here for null sets holds verbatim for `Z` null, meagre, of
cardinality `< c`, of finite outer measure, or contained in a closed half-plane:
`chi(C \ Z) = chi(C)` in all five cases. The bad-translation set `U_{w in W} (Z - w)` is
respectively null, meagre, of cardinality `< c`, of finite outer measure, or contained in a
half-plane, hence never all of `C`. The sharp example `Z_0 = C \ B(0,2/5)` is sigma-finite, of
cardinality `c`, non-meagre and of infinite outer measure, yet `C \ Z_0` is 1-colourable — so no
relaxation to sigma-finite or arbitrary `Z` is possible. Lean: `.ultramath/smwfcr56i/m9/Robust.lean`
(20 declarations, compiled here under Lean 4.34.1, axioms clean); the theorem below is the null
case, proved independently in `NullSetRobust.lean`.

## Why it is a strengthening, not a variant

Theorem 1.1 says that the plane is not 5-colourable. T2 says that the plane minus *any* null set
is not 5-colourable, which is strictly stronger: it quantifies over all null `Z` and forbids
colourings that use the points of `Z` as "holes". It also shows that the finite-witness existence
(finite characterisation) is not merely a compactness artefact: the witness can be moved away from
any prescribed null set.
