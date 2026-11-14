# d10 (R2 transfinite / stabilization): measured verdict

**Headline.** The tower has length **one**. The class of compact extensions of the
trivial factor is a complete lattice of sigma-algebras whose greatest element the tree
*already defines* (`compactSigma`, `MeasureTheory/CompactFactors/Functions.lean:652`).
So chain-join closure, `CodedMax`/Zorn and ordinal recursion are **not** where the
difficulty of `exists_terminal_factor` lives: all of them are free, and what remains is
one lemma, the successor step ("compact over compact is compact"). That lemma is *not*
cheap in the present encoding, and the reason is a concrete defect of the encoding
(below), not of the mathematics.

## What is verified

`sprint/simplify/m4/probe/P5.lean` (92 lines, compiles, no new axioms):
`, .ultramath/smwfoekgk/m4/P5.lean`

| lemma | content |
|---|---|
| `topSigma` | `compactSigma μ (fun _ => ()) hpres`, the top of the class |
| `measurable_topSigma_of_compact` | bounded + `Compact` over triv => top-measurable |
| `compact_of_measurable_topSigma` | bounded + top-measurable => `Compact` over triv |
| `compact_of_inClass` | every bounded function of a member of the class is `Compact` over triv |
| `join_inClass` | **join of any family of members is a member**: `iSup_le`, one line |
| `topSigma_inClass` | the class has a greatest element |

`#print axioms` for all six: `[propext, Classical.choice, Quot.sound]`.

Check (from `repo/lean`, ~1 min warm, up to 5 min under swarm load):
```
source ../scripts/env4341.sh && lean ../sprint/simplify/m4/probe/P5.lean
```
(needs `lean/build/lib` oleans, which are present; the file only imports
`OAI.MeasureTheory.CompactFactors.Functions`).

Consequences, exactly:
* `UniversalGood`'s `hjoin` obligation (`Stationary.lean:144`) is discharged by
  `join_inClass`; `ChainJoin.approximation` + `relative_singularity_approximation`
  are not needed for it.
* Maximality over the class is a definition, not a Zorn lemma: the class has an
  explicit top, so `CodedMax.exists_maximal` can be replaced (only its countable
  coding of the top remains to be supplied, see "coding" below).
* R2 (transfinite) therefore costs nothing beyond R1: the ordinal length is 1.

## What is not verified, and why it is the crux

The successor step needs: if `q` is in the class and `X x_q X` is not ergodic, then
`u := extend q H` (`CompactTower.strict_compact_successor`) is in the class, i.e. `H`
is compact over the **trivial** factor. The successor gives only that everything is
compact over `u`.

The naive epsilon/3 composition **fails**, and this is a defect of `CompactFunctions.At`
(`Functions.lean:44`), not of the argument: `At μ q H ε` quantifies
`∀ k : K, ∃ a : Y → Fin r → ℂ`, i.e. **the coefficient functions depend on `k`**, while
the approximating family `Hf : Fin r → X → ℂ` is fixed. Composing
`G(k.x) ~ sum_i a_i^k(q x) Hf_i(x)` with `a_i^k(q .) ~ sum_j c_ij(k) Kf_ij^k(x)` needs a
`k`-independent family, so it needs total boundedness of `{a^k : k in K}` in `L2(mu.map q)`,
which `At` does not provide. The classical (Furstenberg-Zimmer) proof of "compact over
compact is compact" supplies it by a total-boundedness/Riesz argument, i.e. it is real
work: 150-400 lines of new theory, and its statement must be added to the tree's API.
Until that exists, R1/d3's "prove the predicate transitive" is the whole sprint.

## The prize, measured

Import graph of `lean/OAI` (83 modules, 31277 lines; script
`sprint/simplify/m4/probe/closure.py`, `usecheck.py`).
The relative-singularity chain is 14 modules / **7533 lines**:

```
  735 Analysis.PlaneSpectrum.Basic              20 of 96 decls used outside the chain
  560 Analysis.PlaneSpectrum.Characters          3 of 42
  497 Analysis.PlaneSpectrum.ConditionalSpectrum 8 of 30
  295 Analysis.PlaneSpectrum.FourierTests        1 of 16
 1078 Analysis.PlaneSpectrum.InvariantMean      30 of 130
  314 Analysis.PlaneSpectrum.Multipliers         3 of 30
  537 Analysis.PlaneSpectrum.PhaseCollision      0   <- fully dead
  255 Analysis.PlaneSpectrum.PhaseEncoding       0   <- fully dead
  322 Analysis.PlaneSpectrum.SmallArcs           0   <- fully dead
  496 MeasureTheory.CompactFactors.Approximation 4 of 14
  703 MeasureTheory.CompactFactors.Centers       5 of 93
  701 MeasureTheory.CompactFactors.ConditionalLimits 4 of 19
  442 MeasureTheory.CompactFactors.ConditionalSelection 4 of 17
  598 MeasureTheory.CompactFactors.RelativeCenters 0  <- fully dead
```
**1712 lines are outright dead** once the chain is replaced (PhaseCollision,
PhaseEncoding, SmallArcs, RelativeCenters). The rest is "definitions survive, proofs
go". So the sprint target of -1500/-2000 is not the ceiling: the ceiling is -7500, and
the deletion is worth doing only together with the successor lemma.

## Coding (the only other real cost)

`RelativeProduct.law`/`condDistrib` take a **map** `q : X → Y`, so the top sigma-algebra
must be coded by a measurable map into a StandardBorel space; the top need not be
countably generated as a sigma-algebra (sub-sigma-algebras of countably generated ones
need not be), which is exactly why `CodedMax`'s countable/L2-separable machinery exists.
Two ways out:
1. keep `CodedMax` and feed it `Good q := comap q ≤ topSigma`; then `hjoin` is
   `join_inClass` (verified) and `hbase` is `topSigma_inClass`, and only `hug` = the
   successor lemma is missing;
2. drop maps and restate `RelativeProduct`/`condDistrib` for a sub-sigma-algebra; that
   removes `Factors`(586)+`Functions`(884)+`Kernels`(774)+`Separability`(573)+
   `AlgebraModels`(664)+`RelativeProducts`(472) = 3953 lines of map-coding, but it is a
   rewrite, not a deletion, and it is the wrong first move for a 24h sprint.

Recommendation: 1, plus the successor lemma. Nothing else in R1/R2/R5/R6 needs work.
