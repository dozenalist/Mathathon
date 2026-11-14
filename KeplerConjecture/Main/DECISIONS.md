# Decision record — Kepler problem 15

Each entry: what was decided, the evidence, and what would reverse it. Main keeps
this file; workers may propose entries in their own branches.

## D1 — Freeze one mathematical contract (2026-11-14, M)

Adopt unit balls (radius 1), minimum separation 2, `δ` = occupied-volume upper
density, `c = 3δ/(4π)`, `f̂(t) = ∫f(x)e^{−2πi⟨x,t⟩}dx`, and quote CDS/higher-point
numbers in occupied-volume units with the centre-density equivalent alongside.
**Reason.** The recovered material mixes three conventions (radius 1/2 with
separation 1 and number density; CE "table units"; occupied volume), and
`Literature/PRIOR_WORK.md` records a dual-shell enumeration bug that was a pure
normalisation error. **Reverse if** a source theorem can only be cited in its
native scale — then convert in the same paragraph (K15-C007), do not re-freeze.

## D2 — Ordinary Cohn–Elkies is a control, not a target (M)

No effort goes into searching for a single admissible `f` that proves
`π/√18`. By Li (Adv. Math. 460 (2024) 110043, Thm 6.1) the CE optimum in `d=3`
is `> 0.18398089` in centre units against `2^{−5/2} = 0.176776695…`
(K15-C006). Two-point function searches stay useful only as (i) reproducibility
controls, (ii) components of a hybrid that carries extra geometric information.
**Reverse if** someone exhibits a proof that Li's bound is misquoted in this
range — the local reproduction of `0.18398089` is still pending.

## D3 — Re-anchor "better" to 0.754697399337 (M)

The comparison target is the dodecahedral bound `(4π/3)/V_HM` (K15-C008), not
the Fourier-family record `0.770271`. A new analytic or hybrid bound counts as
progress only below `0.754697399337`, or as a materially shorter proof of a
bound at least that strong. **Reason.** ROADMAP §5 lists the CDS values but the
frontier is set by Hales–McLaughlin; without this anchor the team would present
a `0.7703` re-derivation as state of the art. **Reverse if** X establishes that
a stronger published non-Kepler bound exists.

## D4 — The hybrid price must be a local count, not an integral (M)

Demote the "positive tail `I = ∫_{|x|>R} f`" interface that the earlier brief
proposed. A proved replacement exists: Theorem B / K15-C003 charges
`n·max(M,0)` where `n` is a contact number of the region where `f > 0`.
**Evidence.** `smwg019eu` m2 §3: the integral form is equivalent to a global
equidistribution statement about the tail; a purely local argument loses a
factor `1/(c·vol B_1) = 1.3505`, and any refutation of the integral form must
beat the two-point optimum by `5.30%` (`f̂(0)/f(0) = 5.3719879` at the CE
optimum). **Reverse if** someone proves the equidistribution inequality for a
class of packings — then the integral form is available again on that class.

## D5 — Contact-sphere relaxation is closed (M, m2)

"Let `f > 0` on `{|x| = 2}`, price it with the kissing number 12" is vacuous
(K15-C004/C011). **Reverse if** the relaxation set has interior — which means
a genuine tolerance in the kissing problem, i.e. a *new* local theorem. That
would be a result in its own right and would re-open the route.

## D6 — Additive two-point corrections to Voronoi volume are closed (M)

`vol Ω(v) ≥ V_0 − κB_κ(v)` with `B_κ` from a positive-definite kernel cannot
reach `V_0 > V_HM` (K15-C005): the correction is positive at the icosahedral
cell and non-positive on average. **Reverse if** the correction is made
multiplicative or normalised per cell (so that the fcc slack is not spent
twice), which is a different inequality and needs its own proof.

## D7 — Sharpness and uniqueness claims must survive zero-density defects (M)

Any statement of the form "every maximal-density packing is …" must state how
zero-density regions (holes, unbounded defects, non-ergodic mixtures) are
handled. The recovered `smwfyzz1k` material contains uniqueness-flavoured
claims; they are `PENDING_REVIEW` (K15-R001…R005) and may not be cited.
Likewise the retracted "every smooth sharp certificate must vanish" argument
(PRIOR_WORK) stays retracted; Viazovska's `g` in `d=8` is a counterexample to
the blanket form.

## D8 — Lean scope: definitions and finite lemmas only (M)

No analysis formalisation. The two candidates worth compiling are
(1) the exact dodecahedral constant `V_HM` including `π`-free algebra
(`K15-COMPUTE-002`) and (2) the density-conversion identity `δ = (4π/3)c`
together with the finite count `n(δ) = ⌊(3+δ)³⌋−1` of K15-C003 Cor. 2.3.
Both are stable, small, and serve a concrete dependency. Everything else waits.

## D9 — Keep recovered drafts verbatim, supersede by ledger (M)

`Roadmaps/dim-3-analytic-bound-prompt.md` and `Roadmaps/sharp-bound-in-three-dimensions.md`
are committed unchanged, with checksums, and are marked superseded. Editing them
would destroy the audit trail for K15-C009 and D4. Corrections live in
`Main/CLAIMS.md`.
