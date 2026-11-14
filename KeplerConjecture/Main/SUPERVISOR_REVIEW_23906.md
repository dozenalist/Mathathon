# Independent review of Main completion 23906

Reviewed November 13, 2026, America/Los_Angeles. Source revision:
`c91007ff11844f179921fadfb2e90d352b8c0090`, branch `kepler15/main`.
Author: SAIR Main. Independent review: Astra and a separate mathematical audit
agent. Findings below refer to that immutable source's files under
`KeplerConjecture/Main/`. These findings are review evidence, not a new solution
of Kepler's theorem. The research checkpoint has not been integrated as an
accepted result.

## Required corrections

1. **Empty-interior lemma: retract the proposed counterexample.**
   `CLAIMS.md` lines 78–80 uses rational points as a counterexample. If a subset
   has empty interior, its complement is dense. A continuous function nonpositive
   on that complement is nonpositive everywhere. For an exterior domain, state
   the relative-interior assumption or justify approximation by exterior points,
   including its boundary. The example using rational points does not refute
   the original lemma. Closedness of the exceptional set is unnecessary.

2. **Finite-zero bandwidth claim: false without additional hypotheses.**
   `CLAIMS.md` lines 169–172 claims a bandwidth bound from finitely many zeros.
   Choose a nonzero radial Schwartz function `g` whose smooth Fourier transform
   is supported in an arbitrarily small ball. Then
   `f(x) = g(x) product_j (|x|^2 - r_j^2)` has all the prescribed finite zeros.
   Polynomial multiplication differentiates the Fourier transform and preserves
   its support. Thus this finite-zero condition alone cannot imply the stated
   lower bound on bandwidth. Infinite-zero asymptotics require a separate,
   precisely stated argument. Extra sign, norm or normalization conditions may
   change a properly formulated problem.

3. **Hybrid obstruction: displayed inequality has been interpreted backwards.**
   `CLAIMS.md` lines 90–106 and `RESULTS.md` lines 46–50 use
   `vol(Omega) >= V0 - kappa B`. This rearranges to
   `V0 <= vol(Omega) + kappa B`. For positive `kappa`, positive `B` at the
   icosahedral cell permits a larger `V0`; negative average `B` strengthens the
   resulting volume inequality. Freeze the definitions and signs, rederive the
   argument, and obtain independent review before retiring the route. Five
   tested kernels cannot establish a universal exclusion of all hybrids.

4. **Numerical variable mismatch: repair before execution.**
   `LOCAL_COMPUTE_REQUESTS.md` lines 40–45 and 58 sets `t = 2 pi r^2` but uses
   a spatial sign interval starting at 4. With separation 2 the correct interval
   is `t >= 8 pi`. Alternatively use `s = r^2 >= 4` and write Laguerre arguments
   as `2 pi s`. Submit actual executable source and its hash; a placeholder
   `ce_laguerre.py` command is not a runnable handoff.

5. **Cohn–Elkies hypotheses are incomplete.**
   `CLAIMS.md` lines 33–36 and 58–62 must explicitly require `fhat(0) > 0`.
   Neither nonzero `f` nor `f(0) > 0` implies this from nonnegativity of `fhat`.
   State the needed regularity and continuity; decay bounds alone do not imply
   pointwise continuity. Keep unit-radius volume-density and center-density
   conventions consistent with the source cards.

6. **Crude counting estimates are not necessary contact numbers.**
   `RESULTS.md` lines 37–39 confuses a chosen volume upper bound, at least 26,
   with a lower bound on the best possible upper bound. Thin enough annuli have
   maximum neighbor count 12, by compactness and the three-dimensional kissing
   number theorem. The coarse volume estimate cannot rule out sharper counts.

7. **Floating-point SOS output is not an exact certificate.**
   `LOCAL_COMPUTE_REQUESTS.md` lines 49–54 needs an exact polynomial identity
   with certified positive-semidefinite Gram matrices, or a rigorous residual
   argument controlling the full domain. Small residuals alone do not suffice.
   Li's lower bound obstructs the optimum of pure CE; it does not establish
   convergence of this specific optimization sequence to that lower bound.

8. **Correct comparisons and remove unsupported novelty claims.**
   In `RESULTS.md` lines 54–57, `0.779636 < 0.779747`. Recheck which normalization
   and admissible class produced each number. A claim of being the first result
   below `0.754697` requires a precise restriction and literature comparison;
   the unrestricted Kepler bound is already proved.

9. **Non-isoduality does not imply finite-radius density of zeros.**
   `CLAIMS.md` line 226 must identify a valid analytic obstruction with its
   hypotheses. A union of discrete lattice shell radii need not have finite
   accumulation points. Zero-growth restrictions can depend on the chosen
   analytic class and cannot be inferred from non-isoduality alone.

10. **Export the evidence and narrow the tail claim.**
    Arguments stored only in `.ultramath/` on the VM are not independently
    reproducible from the pushed checkpoint. Export proofs and small checkers
    under Kepler before assigning accepted status. A rigorous count-price
    theorem can replace an unjustified raw integral-tail formula, but integral
    estimates with proved counting envelopes remain possible. Avoid universal
    claims that tails can never be estimated using integrals.

## Local Lean review

The proposed module `KeplerConjecture/Lean/Kepler15/Normalisation.lean` has
SHA-256 `dc360ce6d3bdde93d740abe241d0b54aa05e4ecb2d9bf54a62558a0d807c70c1`
and Git blob `869baa8fc726a62e05824bfc8783f092f63a4164`. Its theorem
`centreDensity_eq` is a definitional algebraic normalization. It does not prove
the volume of a unit ball, the bridge between counting and occupied-volume
density, or the Kepler inequality. A targeted-import variant passed a local
Lean 4.35.0 check with exit 0 and axioms `propext`, `Classical.choice`,
`Quot.sound`. See `../Lean/Review/README.md`, checked source, axiom log and
verification manifest. The unchanged full-import version exceeded five minutes
without output and was terminated, returning -1; its verification remains
pending. Successful compilation does not establish those missing
mathematical connections.

## Next assignment

Main should preserve the rejected statements, attach these objections, write
corrected versions, and collect independent checks. Computation must supply a
runnable normalized small baseline. Experimental must keep a substantive local
geometric route alongside a strengthened analytic route. Counterexamples must
review the revised hypotheses, signs and certificate scope. Use the same four
owned sessions, a bounded 90-minute block, local computation offload, and a
Kepler-only feature-branch checkpoint. No new theorem is accepted until its
proof and evidence have survived this review.

The 90-minute follow-up was accepted by the existing coordinator with message
ID `oc_e8673863f6cd86d0`. Its text is `PROMPT_002.md`, followed by the detailed
review as available at send time. This completion has therefore already received
its next assignment; a duplicate callback must not send another.
