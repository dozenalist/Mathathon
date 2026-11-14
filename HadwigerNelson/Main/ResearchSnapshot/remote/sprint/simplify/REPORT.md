# Sprint A, hour 1: the projected -2000-line deletion is impossible in the current Lean
# architecture; the paper-level deletion is real and is written out below

## 1. What m11's Theorem A actually replaces

Theorem A: X ergodic K-system, Y invariant factor, X x_Y X ergodic, d : X -> D equivariant
measurable wild, d NOT Y-measurable  =>  the relative difference law over Y is C-null.
Proof: F = {d(x)/d(x') in C} is invariant, so has measure 0 or 1; if 1, rho = |j^{-1}(...)|
is invariant, hence constant r; r = 0 makes d Y-measurable; r > 0 gives four conditionally
independent samples whose pairwise differences are four equidistant points of R^2, which the Gram
obstruction forbids.

The paper uses Lemma 2.7 exactly once, at the terminal factor of Lemma 3.1, where X x_Y X IS
ergodic. So at the level of the *paper*, Theorem A replaces the whole of §2.4 and makes the
approximation property (2.6) unused. That part of the sprint's premise is correct.

## 2. Why the Lean cannot simply delete the induction

The Lean does not use Lemma 2.7. It defines

  UniversalGood mu p  :=  forall d, Measurable d -> equivariant -> IsWild (mu.map d) ->
                          differenceLaw (mu.map p) (condDistrib d p mu) C = 0

(ConditionalLimits.lean:669) and proves `exists_terminal_factor` (Stationary.lean:126) by
maximality over UniversalGood. The approximation property is consumed at TWO places, and neither
is the terminal-factor application:

* Stationary.lean:144 (`hjoin`), to prove UniversalGood for the join of a chain, via
  `relative_singularity_approximation`;
* Stationary.lean:159 (`hug`), to prove UniversalGood for the STRICT COMPACT SUCCESSOR u of a
  maximal factor, again via `relative_singularity_approximation` plus
  `ChainJoin.approximation`.

At both sites the relative product is NOT known to be ergodic — indeed the successor exists
precisely because it is not — so Theorem A does not apply. UniversalGood must be *propagated*
across every extension step, and that propagation is exactly what (2.6) and the phase-collision
induction provide. Deleting `relative_singularity_approximation` therefore breaks
`exists_terminal_factor`, not just §3.3.

Consequence: the projected -2000 lines cannot be obtained by deletion inside the present
architecture. The current architecture avoids transfinite recursion by encoding the tower as a
maximality over a join- and successor-closed property, and the approximation is the price of that
encoding.

## 3. The restructure that WOULD work (and its cost)

Replace maximality-over-UniversalGood by maximality-over-compact, and apply Theorem A once:

  R1. Let Psi be the class of factors that are compact extensions of the trivial factor.
  R2. Let Y* be the join of all of them. Joins of compact extensions are compact extensions.
  R3. If X x_{Y*} X were not ergodic, `CompactTower.strict_compact_successor` would produce a
      compact extension strictly beyond Y*, contradicting the join.
  R4. Apply Theorem A at Y*: for every wild d that is not Y*-measurable, the difference law is
      C-null.

What this needs that does not exist yet: a predicate `IsCompactExtension` with join closure, and
step R4 must supply the non-measurability hypothesis for each d (in the present architecture that
is what UniversalGood buys indirectly). Estimated cost: a new definition plus join closure, a
strict-successor contradiction, and one application of Theorem A — plausibly 300-500 lines of new
Lean replacing ~2053 lines of induction, but the join closure of compactness is real work and I
would not promise a net saving without building it. This is the route to take if the sprint is
continued on the Lean side; it is the only one I have found that removes the induction.

## 4. A defect in the paper's Lemma 2.7, found while checking the interface

Lemma 2.7 as printed has no non-measurability hypothesis, and it is FALSE without one: take
Y = X, the top factor. Conditionally independent samples over X coincide, so nu_Y = delta_0, and
delta_0(C) = 1 because 0 in C. The lemma asserts nu_Y(C) = 0. The tower of Lemma 3.1 can terminate
at X (the relative product X x_X X is a point, hence ergodic), so this is not excluded by the
printed hypotheses. The correct statement carries "d is not Y-measurable", which is what Theorem A
proves with. The Lean is unaffected: `UniversalGood` over p = id fails for d = id (wild, law mu,
difference law delta_0 with C-mass 1), so the maximality argument cannot return the top factor.

## 5. Paper-level replacement text (the deliverable that survives)

Replace §2.4 (Lemma 2.7 and its proof, ~4.5 pages) by:

  Theorem 2.7'. Let X be an ergodic standard probability-preserving K-system, Y an invariant
  factor with X x_Y X ergodic, and d : X -> D a Borel equivariant map with d_*mu(C) = 0 which
  does not agree mu-a.e. with a Y-measurable map. Then the law nu_Y of d(x)/d(x') for
  conditionally independent samples over Y satisfies nu_Y(C) = 0.

  Proof. F = {(x,x') : d(x)/d(x') in C} is Borel and invariant under the diagonal action, since
  every k in K is an automorphism of D carrying C to C; by ergodicity of X x_Y X, mu_R(F) is 0
  or 1. If it is 1, rho = |j^{-1}(d(x)/d(x'))| is invariant (the action on parameters is
  orthogonal) and finite, hence equals some r a.e. If r = 0 then d(x) = d(x') mu_R-a.e., so d is
  Y-measurable, contrary to hypothesis. If r > 0, choose four conditionally independent samples
  over a good fibre: the pairwise difference vectors are four points of R^2 at distance r from
  one another, impossible. Hence mu_R(F) = 0. QED

and delete the approximation property (2.6) from Lemma 3.1's statement, since nothing consumes it
once Lemma 2.7 is replaced. The tower itself (strict compact extensions, iterated) is unchanged;
only its bookkeeping shrinks.

Savings at paper level: §2.4 (about 4.5 pages) -> 8 lines; (2.6) deleted from Lemma 3.1 and from
its proof; the phase-list and collision machinery disappears from the paper entirely.

## 6. Status

- Verified: the two Lean sites that consume the approximation (Stationary.lean:144, :159) and the
  reason Theorem A cannot serve them.
- Verified: the Y = X counterexample to Lemma 2.7 as printed.
- Written: the replacement text of §5, which is a complete paper-level simplification.
- Not done: the R1-R4 Lean restructure; it is the only route to a shorter development and it is a
  build, not a cut. Recommended as the next block if the sprint continues.
