# Review 0138 — withdrawal of K15-C029 and what replaces it

Source withdrawn-from: `6626714125c35292d78943cd0fe8d18ec0051b38`.
Reviewer finding (immediate, independent): the proof of `K15-C029` is invalid.
Main accepts it in full. This file records the withdrawal, the rejected text, the
correct estimate with the negative part, and what of the surrounding programme
survives.

## 1. What was wrong

`K15-C029` argued: `A(v) ≥ θ` on `D_θ`, and `Σ_{v∈Λ∩B(x,r)} A(v) ≤ C₁r²`, hence
`θ·#(D_θ ∩ B(x,r)) ≤ C₁r²`.

The middle step is false. Negligibility bounds a **signed sum**; the negative
terms of `A` outside `D_θ` can cancel the positive terms inside it, so the sum
carries no information about `#D_θ`. The proof silently assumed `A ≥ 0`, which is
not among the hypotheses — and is not true for the `A` Hales actually uses
(where `A` must be negative on cells larger than `√32`).

**Minimal illustration of the logical gap** (arithmetic, not a geometric packing
counterexample): let `Λ = 2ℤ³` and let `S ⊂ Λ` be a sublattice of density `δ`.
Set `A = θ` off `S` and `A = −θ/δ` on `S`. Then `Σ_{Λ∩B(x,r)} A = o(r³)` while
`A ≥ θ` on a set of full density, so no bound of the form `#D_θ ≤ C₁r²/θ` can
follow. Whether such an `A` is *realizable* by a packing is a separate question;
it does not need to be, because the step being refuted is logical, not geometric.

## 2. Withdrawn text (kept as rejected evidence)

The full `K15-C029` entry remains in `Main/CLAIMS.md`, marked
`WITHDRAWN (proof invalid, review 0138)`. Nothing dependent on it may be cited.

Dependent statements withdrawn at the same time:

| Where | Statement withdrawn |
| --- | --- |
| `CLAIMS.md` K15-C029 (2) | "a proposed `A` uniformly positive on a positive-density set cannot be negligible" |
| `CLAIMS.md` K15-C029 (3) | "the average of `A` is `o(1)`, so `A` must be negative on a full-density set" |
| `CLAIMS.md` K15-C029 (4) | the "usable objective" containing "`A` must be negative on a set of vertices of full density" |
| `RESULTS.md` §2 item 5 | "defect density is zero" as a proved statement |
| `PROOF_GAPS.md` G7 | the falsification test derived from it |
| `PARTITION_SPEC.md` R3 | "K15-C029 applies: `A` must be positive at defect vertices and negative on a full-density set" |
| `PROGRESS.md` K15-MAIN-007 | the same claim in the block entry |

## 3. The correct estimate (K15-C029r, `PROVED`)

Same hypotheses: `Λ` saturated 2-separated, `vol Ω(v) + A(v) ≥ √32` for all `v`,
`Σ_{v∈Λ∩B(x,r)} A(v) ≤ C₁r²` for all `x`, `r ≥ 1`.

**Lemma.** For every `θ > 0`, every `x` and every `r ≥ 1`,
```
θ · #(D_θ ∩ B(x,r))  ≤  C₁ r²  +  N_A(x,r),        N_A(x,r) := Σ_{v∈Λ∩B(x,r)} max(−A(v), 0).
```
*Proof.* `Σ_{B} A = Σ_{D∩B} A + Σ_{B∖D} A ≥ θ·#(D∩B) − N_A`, since `A ≥ θ` on
`D` and `A ≥ −max(−A,0)` everywhere; combine with the negligibility bound. ∎

**Reading.** The defect count is controlled by the *negative mass* of `A`, not by
`C₁` alone. Any use of this lemma must supply a bound on `N_A`. Two ways:

1. **Conditional lemma, `A ≥ 0`** (recorded separately, since it is what the old
   entry actually proved): if in addition `A ≥ 0` pointwise, then `N_A = 0` and
   `#D_θ ∩ B(x,r) ≤ C₁r²/θ`. This is true and may be cited *with that
   hypothesis*. It is not Hales' situation.
2. **Bounded-range transfers** (`K15-C035` below): if `A` comes from an
   antisymmetric transfer of range `R` and bound `Φ`, then
   `N_A ≤ Φ·k_R·#(Λ∩B(x,r))`, and the lemma becomes a *relative* bound: the
   density of `D_θ` is at most `(Φ k_R/θ)·c(Λ)`. That is the form in which the
   estimate is usable, and it is what the transfer construction supplies.

## 4. What survives, and what does not

- **Survives:** Lemma 3.3 itself (which needs only one-sided negligibility,
  because it combines it pointwise with fcc-compatibility). `K15-C002b`,
  `K15-C003r`, `K15-C004`, the verified certificate `K15-C023`, the interface and
  the checkers are untouched by this withdrawal.
- **Does not survive:** any statement that fcc-compatibility plus negligibility
  forces the small-cell set to have density zero, or that `A` must be negative on
  a full-density set. Those were the "usable objective" of the last block; the
  objective is now the weaker and correct one in §3.
- **Scope retraction (second review point).** The last block's claim that the
  shell and two-point families are "closed" is narrowed: finite-optimiser
  failures and one fixture support only the tested scope. `K15-C028`'s fixture
  shows the allowance is unprofitable *at degree 3 in that family*, and C's
  saturation is a statement about *that certifier*; neither is an impossibility
  theorem. The word "closed" is replaced by "no gain found in the tested scope".
