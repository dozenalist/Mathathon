# Integration note for Main — block `K15-REVIEW-0523-E`

One screen. Branch `kepler15/experimental/run-01`.

## Hashes

```
read (Main)        a6f3935    KeplerConjecture/Main/GEOMETRIC_LEMMA_0438.md
continued from (E) 93c61a8b926eeece8ea0abff10e231757d76a2cc
this block         7a0d9011becb3014b29b7b179560759156309bf5   certified enclosure + controls
                   f15a44ba0e7d4f9cae2505c61b6c40d29c583132   ledger E091-E093
                   2573ce3880d5d783b842c800215478e8d21b60ac   compactness slip quantified
                   585c5632ee3c25adc2de4b05be8d795eae64605d   R certified, not assumed
                   c847a7e8173ed77abde4773c286aef3cbeae6c97   box scaling
                   c2c0cedae9b59ca350eba7c8438f6d40fea835ad   reviewer obligations
                   b88982da9fd5d02a1be26a9ae5cd2b0f817c4200   tetrahedron control
                   e5dec3a63948eb911fc0b4bf335a5f92b5ed57fd   dependency overhead 6e5
                   5f319be46bd76f6fd7a2533da43bb1695c11de0b   empty-inner guard
                   b3b6a07235f0951b3eb78ab69eaeae94d888f9f2   out-of-sample cross-check
```

## What Main needs from this block

1. **A certified cell-volume enclosure exists and is validated** (`K15-E091`). Exact rational
   arithmetic end to end, no floating-point sign decision; π by Machin, sin/cos by Taylor, both
   with rational remainder bounds. Controls: cube `8`, regular tetrahedron `8/3` (non-symmetric,
   so it tests orientation), fcc and hcp `4√2`, C5 fixture `5.898017371803720` — all to `1e-18`.
   Out of sample it agrees with the independent float path to `9e-16`. This supersedes
   `barlow_contact_cell.py` for volume questions; that file remains a float check and Main is
   right to decline it as exact.
2. **Scope: one payer.** `(P')` is pairwise and `(CUT)` is simultaneous; this file bounds the
   former only, and says so in §2.3.
3. **The atom is calibrated and the obstruction is dimension, not cost** (`K15-E092`). A `0.1°`
   box already certifies `vol > 5.8712`, so the two-parameter C5 family is exhaustively
   certifiable with `~2×10⁴` boxes. The completion domain has up to 46 coordinates, so no such
   grid is reachable. The sandwich is also dependency-dominated (`6×10⁵` on a `1°` box), and a
   parameter-Lipschitz bound would give `~4e-3` per degree instead — the right next step.
4. **`K15-E075`'s constant was wrong and is corrected** (`K15-E093`): `1.125554845`, not
   `1.056487696`, matching Main's own computation. The conclusion is unaffected. Main's handling
   of the discrepancy — quoting its own value and not E's — was the right call.
5. **Theorem D audit**: the compactness is sound; the cone bound and the reduction to a compact
   admissible set both check out; the `N ≤ (2R)³` should be `(2R+1)³` (`11953` vs `10453`, a
   14% term, no conclusion affected). The load-bearing gap is unchanged and is the **equality
   case of Hales–McLaughlin** in step (3) — I could not replace it, and a self-contained
   Theorem D would need that equality case proved.

## What I owe next

The parameter-Lipschitz bound (`∂V/∂θ`, `∂V/∂φ`) — that is what makes the atom usable for
boxes, and it is the first deliverable of any next block on this route.
