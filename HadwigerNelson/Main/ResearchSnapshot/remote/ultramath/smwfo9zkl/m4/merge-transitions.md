# Label merging at six colours: every colour pair is transition-active

**Direction d18, member m4, swarm smwfo9zkl.** Object: the *transition measure* carried by a pair of
colour classes of a six-colouring. Method: collapse two labels and apply the paper's five-colour
obstruction. Nothing below uses local finiteness, cyclic centres, or Sections 6-8 of the paper.

Notation and inputs are the paper's (`attachments/here-are-three-files-ni5n/paper.pdf`):
Definition 1.2 (weak measurable colouring), Theorem 1.1 (no proper five-colouring), Theorem 1.3
(transfer, every `k`), Theorem 1.4 (no weak measurable five-colouring), Corollary 1.5 (positive
five-colour badness). I write `{1..m}` for the label set and `A_i` for the class of colour `i`.

---

## 0. Two ways of measuring the unit pairs that carry a given colour pair

**(a) Measure form.** Let `c : R^2 -> {1..6}` be Lebesgue measurable with classes `A_i`. For a unit
direction `u` and a Borel `D ⊆ R^2` put

```
m_ij(D) = ∫_D ∫_{S^1} ( 1_{A_i}(x) 1_{A_j}(x+u) + 1_{A_j}(x) 1_{A_i}(x+u) ) dσ(u) dx ,
m_ij    = sup_{R>0} m_ij(B(0,R)) ∈ [0,∞] ,          m_S = Σ_{i<j, i,j∈S} m_ij ,
```

with `σ` normalised arc length and completed product measure, exactly as Definition 1.2. Thus
`m_S` is the measure of the set of unit pairs whose two colours both lie in `S`.

**(b) Mean form** (the paper's Corollary 1.5 setting, valid for *arbitrary* colourings). For a
normalised finitely additive left-invariant mean `µ` on the plane isometry group `E(2)`, and a
colouring `c : R^2 -> {1..6}` with no regularity, put

```
p_ij(c,µ) = µ{ T ∈ E(2) : {c(T^{-1}0), c(T^{-1}1)} = {i,j} } ,   p_S = Σ_{i<j, i,j∈S} p_ij .
```

Every isometry sends the unit segment `[0,1]` to a unit segment, so `Σ_{i<j} p_ij = 1` and
`p_ij ≥ 0`; `p_S` is the `µ`-measure of the isometries for which both endpoints get colours in `S`.
This is exactly the "badness" of the merged colouring used in Corollary 1.5(i).

## 1. The merging lemma

**Lemma 1.1 (measure form).** Let `c` be a weak measurable six-colouring and fix a pair `{i,j}`.
If `m_ij = 0` then merging the classes `A_i`, `A_j` into one class gives a *weak measurable
five-colouring*.

*Proof.* Relabel so that `{i,j} = {5,6}` (the assertions are invariant under relabelling). Define
`c' : R^2 -> {1..5}` by `c'(x) = 5` if `c(x) ∈ {5,6}` and `c'(x) = c(x)` otherwise; its classes are
`A_1,...,A_4, A_5 ∪ A_6`. It is measurable, being a Borel function of the measurable `c`. For `R > 0`,

```
Σ_{s=1}^{5} ∫_{B(0,R)} ∫ 1_{A'_s}(x) 1_{A'_s}(x+u) dσ(u) dx
  = Σ_{s=1}^{4} m_ss(B(0,R)) + m_55(B(0,R)) + m_66(B(0,R)) + m_56(B(0,R)) = 0 ,
```

because the diagonal terms vanish by weak measurability of `c` (Definition 1.2 applied to `c`) and
`m_56(B(0,R)) ≤ m_56 = 0`. So `c'` satisfies Definition 1.2 with `k = 5`. ∎

**Lemma 1.2 (mean form, no regularity).** Let `c : R^2 -> {1..6}` be any colouring and `µ` an
invariant mean. Merging `A_i`, `A_j` gives a colouring `c'` with five labels whose badness in the
sense of Corollary 1.5(i) is exactly `p_ij(c,µ)`.

*Proof.* For every isometry `T`, the merged colouring `c'` has `c'(T^{-1}0) = c'(T^{-1}1)` iff the two
endpoint colours `c(T^{-1}0), c(T^{-1}1)` lie in the same merged class. The labels `{1..6}` are
partitioned into `{i,j}` and four singletons, and the merge map is injective off `{i,j}`; so this
happens iff `{c(T^{-1}0), c(T^{-1}1)} = {i,j}`. Hence the badness of `c'` is `p_ij(c,µ)`. ∎

Only the number six is used: the merge has five labels.

## 2. Theorem A: every colour pair is transition-active, at six colours and at no other

**Theorem A (measure form).** Let `c` be a weak measurable six-colouring. Then `m_ij > 0` for all
fifteen pairs `{i,j} ⊂ {1..6}`.

*Proof.* If `m_ij = 0`, Lemma 1.1 gives a weak measurable five-colouring, contradicting Theorem 1.4. ∎

**Theorem A' (mean form, arbitrary colourings).** Let `c : R^2 -> {1..6}` be *any* six-colouring and
`µ` any normalised finitely additive left-invariant mean on `E(2)`. Then `p_ij(c,µ) > 0` for all
fifteen pairs.

*Proof.* By Lemma 1.2 the merged colouring has five labels and badness `p_ij(c,µ)`; Corollary 1.5(i)
gives a constant `δ > 0` with badness `≥ δ` for *every* five-colouring and every mean. Hence
`p_ij(c,µ) ≥ δ > 0`. ∎

**Corollary A1 (geometric form).** For a weak measurable six-colouring and each pair `{i,j}` there is
a set `E_ij ⊆ R^2` of positive Lebesgue measure such that, for every `x ∈ E_ij`, the unit circle about
`x` meets colour `j` in a set of directions of positive angular measure (and symmetrically with `i`,
`j` exchanged). *Proof.* Fubini applied to `m_ij > 0`. ∎

**Corollary A2 (unrestricted, qualitative).** Let `c : R^2 -> {1..6}` be a proper six-colouring, with
no regularity whatsoever. Then for every pair `{i,j}` there are points `x,y` at distance one with
`c(x) = i`, `c(y) = j`.

*Proof.* Merge `A_i`, `A_j` to obtain a five-colouring `c'`. Theorem 1.1 says every five-colouring of
the plane has a monochromatic unit pair, i.e. there are `x,y` with `|x-y| = 1` and `c'(x) = c'(y)`.
By the proof of Lemma 1.2 this means `{c(x), c(y)} = {i,j}`; the case `c(x) = c(y)` is impossible
because `c` is proper. ∎

**Six is the last number of colours at which merging bites.** At `k ≥ 7` the merge has `k-1 ≥ 6`
labels and no obstruction to those is available, so the argument yields nothing. At `k = 5` the
assertion is vacuous (no weak measurable five-colouring exists, Theorem 1.4). The content of
Theorem A is therefore specific to `k = 6`.

**Reading.** No two colours of a six-colouring can be *separated*: every one of the fifteen pairs must
be realised by unit segments, in positive measure for measurable colourings. Equivalently the
colour-interaction graph on the six labels - with `{i,j}` an edge iff some unit segment carries colours
`i` and `j` - is complete. The seven-colouring of the plane has a complete interaction graph as well,
so the statement is consistent with the known constructions; it is a *necessary* condition, not a
contradiction.

## 3. Theorem B: explicit constants from merging into two and three labels

The qualitative statement of Theorem A uses Theorem 1.4, which is non-effective. Merging into **two**
or **three** labels instead gives explicit constants, because explicit finite obstructions for two and
three colours are known.

**Lemma 3.1 (finite-graph bound; the paper's Corollary 1.5 mechanism).** Let `H` be a finite
unit-distance graph, `c` a colouring, and `µ` an invariant mean. Write `p_H(c,µ)` for the `µ`-average,
over all placements of `H` by isometries, of `1/|E(H)|` times the number of monochromatic edges. If `H`
is not `r`-colourable and `c` takes at most `r` values, then `p_H(c,µ) ≥ 1/|E(H)|`.

*Proof.* For every isometry `T` the placed graph `T H` is not monochromatic-edge-free, so the average
number of its monochromatic edges is at least one; average over the finitely many edges and use that
the isometry group acts transitively on unit segments. (This is [12, Lemma 2.10 and Theorem 2.11], as
used in the proof of Corollary 1.5.) ∎

Two obstructions, both verified in exact arithmetic in `code/moser_exact.py`
(output `code/moser_spindle_exact.json`):

* `K_3`, the unit equilateral triangle: three unit edges, not two-colourable. Constant `1/3`.
* `M`, the Moser spindle: seven vertices, **eleven** unit edges, not three-colourable, four-colourable.
  Coordinates used: `A = 0`, `B = √3`, `B' = √3(5/6 + i√11/6)`, `C± = √3/2 ± i/2`,
  `D± = B'/2 ± (i/2)·B'/√3`, all in `Q(√3, √11, i)`; all 21 pair distances are decided exactly,
  exactly eleven are unit, `3`-colourability is UNSAT, and a four-colouring is exhibited and checked
  edge by edge. Constant `1/11`.

**Theorem B.** Let `c : R^2 -> {1..6}` be any six-colouring and `µ` any invariant mean. Then
`p_S(c,µ) ≥ 1/3` for every `S` with `|S| = 5`, and `p_S(c,µ) ≥ 1/11` for every `S` with `|S| = 4`.

*Proof.* Merge `S` into one class (Lemma 1.2 extends to merging several labels: the merge map is
injective off `S`). If `|S| = 5` the result is a two-colouring whose badness is `p_S`; apply Lemma 3.1
with `H = K_3`. If `|S| = 4` the result is a three-colouring; apply Lemma 3.1 with `H = M`. ∎

For `|S| = 3` the merge has four labels and an explicit bound would need an explicit
not-four-colourable unit-distance graph; for `|S| = 2` it would need an explicit not-five-colourable
one, which is precisely an explicit finite witness for `χ(R^2) ≥ 6`, and is not known. So at the level
of single pairs only the qualitative Theorem A survives.

## 4. Theorem C: the merged constraints are consistent - merging cannot prove `χ(R^2) ≥ 7`

The method produces necessary conditions on a six-colouring. They cannot contradict each other:

**Theorem C.** The system

```
(0) Σ_{i<j} p_ij = 1 ,  p_ij ≥ 0        (each unit pair carries two distinct labels)
(1) p_ij > 0  for all fifteen pairs     (Theorem A')
(2) p_S ≥ 1/3  for all |S| = 5          (Theorem B, K_3)
(3) p_S ≥ 1/11 for all |S| = 4          (Theorem B, Moser spindle)
```

is satisfiable: the uniform point `p_ij = 1/15` satisfies it.

*Proof.* `1/15 > 0`; for `|S| = 5`, `p_S = C(5,2)/15 = 2/3 ≥ 1/3`; for `|S| = 4`,
`p_S = C(4,2)/15 = 2/5 ≥ 1/11`; and `Σ p_ij = 1`. Exact rational arithmetic; `code/merge_lp.py`. ∎

**The constants are weak in a precise sense.** The "bipartite" point, which puts mass `1/9` on each of
the nine pairs crossing a fixed split `{0,1,2} | {3,4,5}` and zero elsewhere, satisfies (0), satisfies
(2) with `p_S = 2/3` for every 5-subset and (3) with `p_S ≥ 1/3` for every 4-subset, and violates
exactly (1): the six pairs inside the two triples get zero. So the quantitative bounds of Theorem B
cannot exclude a bipartite arrangement; it is the qualitative positivity of Theorem A that does.
Moreover the constants `1/3` and `1/11` are far from the best a linear argument could give: counting
shows `Σ_{|S|=5} p_S = 4·Σ p_ij = 4` and `Σ_{|S|=4} p_S = 6·Σ p_ij = 6`, so `min_{|S|=5} p_S ≤ 2/3`
and `min_{|S|=4} p_S ≤ 2/5`, both attained at the uniform point, whereas the merging constants are
`1/3` and `1/11`. Merging is not a sharp instrument.

**Consequence (a no-go for this method).** No contradiction, hence no proof of `χ(R^2) ≥ 7`, can be
extracted from label merging alone: any six-colouring may well satisfy every constraint that the
collapse of two classes produces. A proof of `χ(R^2) ≥ 7` must use strictly more than the
colour-interaction counts - in the paper's architecture, the palette and interface structure of
Sections 5-8 rather than the pair counts.

## 5. What is proved, what is checked, what is not

* Theorems A, A', B, C and Corollaries A1, A2 are proved above from Theorem 1.1, Theorem 1.4,
  Corollary 1.5 and Definition 1.2. Each hypothesis of those inputs has been checked against the
  paper: Definition 1.2 quantifies over every `R > 0` with the completed product measure, which is
  what Lemma 1.1 reproduces; the merge is measurable and carries five labels; the merged colouring is
  weak measurable exactly when `m_ij = 0`; Corollary 1.5(i) applies to *every* five-colouring and
  every invariant mean, which is what Theorem A' consumes; Theorem 1.1 needs no regularity, which is
  what Corollary A2 consumes.
* The Moser spindle data (seven vertices, eleven unit edges, not three-colourable, four-colourable) is
  verified in exact arithmetic over `Q(√3, √11, i)`; `code/moser_exact.py`.
* The linear-system arithmetic of Theorem C and the bipartite sharpness are verified exactly;
  `code/merge_lp.py`.
* **Not** claimed: any contradiction; any lower bound on a single `p_ij`; any statement about the
  existence of a six-colouring. The pair-level constant is tied to an explicit finite witness for
  `χ(R^2) ≥ 6`, which the paper's non-effective argument does not provide.
* Non-vacuity: at `k ≥ 7` the argument gives nothing and at `k = 5` it is vacuous, so the statement
  exists exactly at `k = 6`; and in the hexagonal seven-colouring all twenty-one label pairs do occur
  at unit distance (`code/hex_pairs.py`), so "every pair occurs" is not an impossible demand.

## 5b. Machine-checked versions

`lean/MergeSixK6.lean` proves both six-colour statements in Lean 4.34.1 on the bundle's own
definitions (`OAI.EuclideanFiveColor.ProperColoring`, `WeakColoring`, `no_proper_five_coloring`,
`no_measurable_weak_five_coloring`), with the standard axiom certificate only:

```
OAI.EuclideanFiveColor.exists_unit_pair_of_pair :
  ∀ (c : ℂ → Fin 6), ProperColoring 6 c → ∀ (i j : Fin 6), i ≠ j →
    ∃ x y : ℂ, ‖x - y‖ = 1 ∧ c x = i ∧ c y = j
OAI.EuclideanFiveColor.pair_transition_not_null :
  ∀ (c : ℂ → Fin 6), Measurable c → WeakColoring 6 c → ∀ (i j : Fin 6), i ≠ j →
    ¬ ∀ᵐ p ∂(volume.prod angularMeasure),
        ¬ ((c p.1 = i ∧ c (p.1 + direction p.2) = j) ∨
           (c p.1 = j ∧ c (p.1 + direction p.2) = i))
#print axioms  -- both: [propext, Classical.choice, Quot.sound]
```

Check with

```
bash scripts/fetch_exact_env.sh          # only if .scratch has been aged out
source scripts/env4341.sh
lean .ultramath/smwfo9zkl/m4/lean/MergeSixK6.lean
```

The second statement is the Lean form of Theorem A: the unit pairs carrying a fixed label pair are
not a null set. The merge map is `mergePair i j = merge01 ∘ permToZeroOne i j` with the explicit
2-to-1 `merge01 = ![0,0,1,2,3,4]`; its kernel is proved to be exactly `{a = b} ∪ {a,b} = {i,j}`,
and the merged colouring is fed to `no_measurable_weak_five_coloring`.


## 6. Consequences for the finite CSP programme

A finite model that is meant to be induced by a six-colouring - palettes at finitely many centres, ray
geometries, the a.e. palette bound, pair exclusion, two-centre translation exclusion - must be
compatible with Theorem A: each of the fifteen label pairs must occur as a unit transition somewhere
in the model's plane. A model in which some pair never meets at unit distance is automatically
unfaithful, so Theorem A is a sound spuriousness test, and Theorem B adds the explicit quantitative
tests `p_S ≥ 1/11` (`|S| = 4`) and `p_S ≥ 1/3` (`|S| = 5`). By Theorem C those tests can prune a model
but can never by themselves make the system unsatisfiable, so they cannot carry a proof of
`χ(R^2) ≥ 7`; in the two-centre CSP they are filters, not the deciding constraint.
