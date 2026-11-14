# R1 certified: what it deletes (3453 lines), what it must prove, and the gap

Read `budget.md` for the measurement method and the R2/R5/R6 verdicts.

## 1. The interface R1 has to hit

`exists_terminal_factor` (Stationary.lean:126) is used at exactly one place, a pattern
match in `ergodic_wild_fourier` (Ergodicity.lean:54), and only the `d = id` instance of
UniversalGood is consumed there:

    obtain ⟨q,hq,hqc,hgood,hmix⟩ := exists_terminal_factor μ
    have hd : IsWild (DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ)) :=
      ⟨relative_difference_invariant μ id q ... , hgood id measurable_id ... (by simpa using hw)⟩
    exact fourier_vanish_of_terminal μ q hq hqc hd z hz

So two target statements are admissible.

(S1, unchanged)   ∃ p, Measurable p ∧ equivariant ∧ UniversalGood μ p ∧ Ergodic (rel prod).
(S2, weakened)    ∃ p, Measurable p ∧ equivariant ∧ IsWild (differenceLaw (μ.map p)
                                                          (condDistrib id p μ)) ∧ Ergodic (rel prod).

(S2) costs ~3 lines in Ergodicity.lean and leaves `ergodic_wild_fourier`'s statement, and
hence `no_proper_five_coloring`, byte-identical. `exists_terminal_factor` has no other
consumer, so either target is legitimate; (S2) is the right one for R1.
Note the `ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)` argument in
`fourier_vanish_of_terminal` is just ergodicity of the relative product, which (S2) supplies.

## 2. What R1 must prove, given Theorem A

    Y* := maximal element of { q : q is a compact extension of the trivial factor }
    (a)  Ergodic (rel prod over Y*) : if not, `CompactTower.strict_compact_successor`
         (Factors.lean:206) yields u = extend(Y*,H) strictly beyond Y*, compact over Y*,
         hence compact over the point -- contradiction.
    (b)  C-null conditional difference law for d = id: Theorem A, whose (H2) is
         "id is not Y*-measurable".

(a) is the join-closure/transitivity work. (b) is the deliverable that is missing.

## 3. The gap: (H2) is not a consequence of (a) or of maximality

Fact 1. `1 ∈ C`. C = `jHom.range` (Basic.lean:100) and `j 0 = 1` (`j_zero`).

Fact 2. If `id =ᵐ g ∘ q` with g measurable then `condDistrib id q μ y = δ_{g y}` a.e., so
the conditional difference law is `δ_1` and its C-mass is `δ_1(C) = 1 ≠ 0`: the conclusion
of (S2)/(S1) FAILS at q.

Fact 3. The relative product over a complete q IS ergodic: if `id = g ∘ q` then the relative
product is carried by `{(d, g(q d))}` and is isomorphic to `(D, μ)` under `d ↦ d`, and
`ErgodicSMul K D μ` is a standing hypothesis.

Therefore ergodicity of the relative product, maximality, and compactness of the extension
chain can all hold at a factor where the conclusion is false. Explicitly: q = id has an
ergodic relative product and C-mass 1.

Consequence (contrapositive of Fact 2, and this is the whole content of the present
architecture): `UniversalGood μ a` at the maximal model `a` IMPLIES that no wild equivariant
`d` is `a`-measurable. That is what UniversalGood buys and what the brief calls "bought
indirectly". It cannot be reproduced by a maximality over compactness.

### The theorem R1 needs (not in the paper, not in the Lean)

    (N)  μ a probability on D, K-invariant, ErgodicSMul K D μ, IsWild μ
         =>  μ is NOT a compact extension of the trivial factor
         <=> the join Y* of all compact extensions of the point satisfies
             L²(Y*) ⊊ L²(μ)   <=>   id is not Y*-measurable.

(N) is necessary, not merely sufficient: if μ were compact over the point, Y* would be the
top factor, over which the difference law is δ_1, and no R1-shaped proof can conclude.

(N) is also a *silent hypothesis of the paper*: printed Lemma 2.7 carries no (H2), and the
top factor violates it (`δ_1(C) = 1`), so the printed tower argument is valid only because
the tower cannot terminate at the top -- which is exactly (N). The Lean never noticed
because UniversalGood encodes (N)'s consequence.

Status of (N): absent from `lean/OAI`. `Basic.lean` has the wild ingredients
(`wild_coset_null` :306, `wild_div_mem_null` :321, `wild_independent_difference` :329:
every C-coset is nought) but nothing relating them to compactness. No proof in the paper.

Proof strategy for (N) (not carried out): suppose μ is compact over the point, i.e.
{ k . F } is precompact in L² for every bounded F. Apply this to characters
`eval z`, z ≠ 0, whose translates are the characters `eval (kCoeff k · z)`. Compactness
confines them to a finite-dimensional space up to ε; to conclude one needs the Gram matrix
`μ̂((kCoeff k - kCoeff l) z)` to be far from singular, which is where the C-coset-null
conditions must enter. This is the hard part and I did not do it.

## 4. The three closure obligations, costed against what exists

    (O1) base: z₀ satisfies the predicate                      ~10 lines, trivial
    (O2) join closure along `ChainJoin.code`                   the expensive one
    (O3) transitivity: Comp(q) + Compact μ q H => Comp(extend q H)
    (N)  incompleteness of Y*                                  new theorem, nothing to reuse

(O2) is the same shape as the existing `hjoin` (Stationary.lean:139-148), whose proof is
`ChainJoin.approximation` + `relative_singularity_approximation`; the ChainJoin half
(Factors.lean:395-495, 101 lines, incl. `approximation`) is retained by R1, so (O2) is
bounded work but not small: `bounded_vector_approximation` (ConditionalLimits.lean:70-188),
`lift_at`, `compact_descend` (Functions.lean:803-885) are all in place. (O3) is the shape of
`compact_orbit_extension`/`compact_descend`, also in place. So (O1)+(O2)+(O3) is plausibly
500-900 lines of new Lean -- affordable against a 3453-line prize. (N) is not.

## 5. Verdicts

* R1 as written: NOT a drop-in saving. It is gated on (N), a new theorem about wild laws and
  compact systems, not on Lean engineering. Do not book R1's 3453 lines until (N) exists.
* R1' (maximality over {Comq} ∩ {C-mass < 1}): swaps (N) for "the C-mass cannot reach 1 across
  a strict compact successor", which is unproven and is not obviously true (the mass is a
  quadratic functional of the conditional kernel and is *not* monotone under refinement; it
  goes 0 at the point, 1 at the top).
* R3 (keep UniversalGood, cheapen (O2)/(O3)): the only route that needs nothing new. Its best
  narrow target is (O3) specialised to the successors `strict_compact_successor` actually
  produces (H = `applyKernel κ q L f` from a centered kernel), which is what
  `relative_singularity_successor` proves in the general form. Specialising the input is the
  cheapest unexplored cut and preserves the prize (3453 lines).
* R2, R5, R6: see budget.md §4 -- at most 87 lines of machinery to trade, all with the same
  closure obligations. Certified negative as line-saving routes.

## 6. Cheapest admissible path to the sprint target, in order

1. R7 dead-declaration trimming: measured 1771 lines, no new mathematics. Clears 1500 with a
   small margin. (m9, direction d1.)
2. R3 specialisation of `relative_singularity_successor`: prize 3453, obligation known true.
3. (N), if someone wants R1: it is one clean theorem with a concrete strategy, but it is
   research, and R1 additionally needs (O2)+(O3).
4. R4 (Theorem A in Lean) does not shorten the tree by itself: Theorem A is not needed by the
   present architecture at all. Its value is as (N)-adjacent infrastructure.

## 7. Machine-checked part (`H2.lean`, compiling, axiom-clean)

    OAI.PlaneFiveColor.Spectral.one_mem_C                        : (1 : D) ∈ C
    OAI.PlaneFiveColor.Spectral.differenceLaw_deterministic      : differenceLaw ν (det g) C = 1
    OAI.PlaneFiveColor.Spectral.differenceLaw_congr              : a.e. equal kernels, same law
    OAI.PlaneFiveColor.Spectral.not_universalGood_of_factorizable
        : (fun d => g (q d)) =ᵐ[μ] id  ->  ¬ UniversalGood μ q      (μ prob., IsWild μ)

All four `#print axioms` = [propext, Classical.choice, Quot.sound]; no sorry, no axioms added.
Check (from repo/lean):

    source ../scripts/env4341.sh
    lean ../.ultramath/smwfoekgk/m12/H2.lean

which prints the four axiom lines. The file imports `OAI.MeasureTheory.CompactFactors.ConditionalLimits`
and uses `condDistrib_comp_self`, `Measure.compProd_deterministic`, `Kernel.deterministic_prod_deterministic`.
Note the last theorem is a *pure* statement about the existing definitions: it does not mention
compactness, so it holds for R1's Y* as well as for the present maximal model `a`.

WHAT IS NOT MACHINE-CHECKED (stated honestly): Fact 3 of §3 (the relative product over a
complete factor is ergodic). It is elementary -- the relative product is carried by the graph
of `g` and is isomorphic to `(D, μ)`, which is ergodic by hypothesis -- but I did not formalise
the isomorphism. Fact 3 is not needed for the negative result; it is needed only to show that
ergodicity cannot *rule out* the failure case, and that is a two-line argument.

## 8. Sanity check on (N): the model case is consistent, and it says what (N) is not

Take `mu = Haar(D)` (D is compact, so Haar exists). Then

* `mu` is `IsWild`: it is invariant under every automorphism of `D`, and `C = range j` is a
  Borel subgroup which is NOT closed. Proof that it is not closed: `ker j = {xi : <xi,z> in 2pi Z
  for all z in E}` is `{0}` because `E` contains `1/n` for every `n` (so `Re xi = Im xi = 0`),
  hence `C = range j` is isomorphic as an abstract group to `CC`, which is not compact, whereas
  a closed subgroup of the compact `D` would be compact. A Borel subgroup of positive Haar
  measure is open, hence closed, hence `Haar(C) = 0`.
* `mu` is ergodic under `K`: `K` is a divisible subgroup of the circle, so `K` is the group of
  roots of unity and `kCoeff` is its inclusion into `E`; the dual action on the character
  `z in E = dual of D` is `z |-> zeta * z`, whose orbits are infinite for `z != 0`. An invariant
  L^2 function has Fourier coefficients constant on these orbits, and a nonzero constant on an
  infinite orbit violates square-summability; so only the trivial character survives.
* `mu` is NOT a compact extension of the point: the characters are an orthonormal basis of
  `L^2(Haar)` and the translate of a character is another character, so the orbit of `chi_z`
  (`z != 0`) is an infinite orthonormal set, whose span is infinite-dimensional, so it is not
  confined to a finite-dimensional space up to `eps`.

So the one obvious candidate for "wild and compact" fails exactly as (N) predicts, and it pins
down what (N) must use: not orthogonality of characters (that is special to Haar), but the
C-coset-null conditions `wild_coset_null` / `wild_div_mem_null` (Basic.lean:306, :321), which
say that no coset of C carries mass. A proof of (N) has to convert "no mass on any C-coset"
into "some bounded function has an infinite-dimensional orbit span", which is where I stopped.
