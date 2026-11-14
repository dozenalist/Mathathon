# Integration note for Main — block `K15-REVIEW-0353-E`

One screen. Everything below is on branch `kepler15/experimental/run-01`; source hashes are
exact and were confirmed against the remote with `git ls-remote`.

## Hashes

```
audited (Main)     b42c8d1    KeplerConjecture/Main/BARLOW_CELLS.md
                             KeplerConjecture/Main/GAP_FIXTURE.md
continued from (E) 212d13292b2f86d6c9114b7160642228644942a3
this block         0ae14cc4c88ea0e74bf9c7c361a6e610f1d7d01e   fixture, theorem, withdrawal
                   f3d7fdd8989665e4675b847580d4a90a34416601   crack-table verification
                   c76194f9abb914d9519ec86e0cb67a6cb55f85bb   review 0353 final hashes
                   d57587e1fb2c1ed2b7896e7e9a0a128062d1638f   rejected 3.237838 + offload request
                   3c9bbfea50b5b5b2ada1a66450a6fa40cd9ddb0a   theta family
                   18f6e1c9aed71edfbfa589d4bb5d989f1b76403b   crack density + one Main overstatement
                   a72214f6eac741a79f8f24d848164e586af7aee4   azimuth resolved
                   bf950918eeb9bbdbef843a7aae37ca3611e98fcd   Barlow Lemma 1' exact
                   4b6b5fef8b00b74ef23ca3a1e98ed2ce7779ac74   random stackings
                   37c66af3e172e5db0efcb0c8e5ec447fbd7c77c8   what the withdrawal leaves
                   565b1f960fa8fddf51dd30197dc544ede131ab7d   crack at other widths
                   307eb8dddc0e4b6a4299957dc5d8eb5e85d318ae   family optimum 111.7975
                   9d2ced71ed2d5e9bba6186ffe51d9fc720482558   270 layers / 40 stackings
```

## The four things Main needs to know

1. **The payer fixture is frozen and its cell is exact** (coordinates in the degree-8 field
   `Q(√5, √(10+2√5), √55)` — `sin 72°` is a nested radical, so not the degree-4 field an
   earlier draft claimed). `(θ, φ) = (111.80°, 36°)` minimises
   `vol Ω(w1) = 5.897967122` over the C5-symmetric family, and the cell is *exact* (no
   completion changes it). The frozen fixture uses `cos θ = −3/8` (exact coordinates) and
   gets `5.898017372`, `5.0e-5` above the family optimum. `(P')` needs `5.763417470`, so the
   margin is `+0.1345`.
2. **`K15-E078` ("97.4 % irremovable") is WITHDRAWN.** It rested on failed searches. What
   survives is `K15-E082`, an angular exclusion for head-on cuts only.
3. **Main's `BARLOW_CELLS.md` Lemma 1 is circular** and the repair is `K15-E083`: redundancy
   of a non-contact half-space needs `K ⊆ H_c` for the contact-only `K`, which is *not*
   `Ω ⊆ H_c`. `K ⊆ B(v,√2)` is true and is now proved exactly (14 vertices, `|x|² ∈ {3/2,2}`,
   `vol K = 4√2`, both local types). The theorem survives the repair unchanged.
4. **`GAP_FIXTURE` checks out**, with one overstatement: "for `d > 1.633` … saturated" needs
   the upper bound `d ≤ 2H = 3.266`. The saturation bound itself is sharp, the volume table
   reproduces exactly, and the pattern (defective surfaces, `√32` bulk) holds at other `d`.

## What E owes next

A lower bound above `V_dodeca` for the payer — that is the only thing standing between the
current state and a proof of `(P')` at this pair. Nothing in this block supplies one.
