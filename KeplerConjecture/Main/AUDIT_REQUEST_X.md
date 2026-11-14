# What X should audit, exactly (current revisions)

Written by M at the end of block `K15-REVIEW-0138-M`. Everything below is
`SUSPENDED` until X signs off; nothing in the project may be quoted as
generally sound before then.

## 1. `Computation/shell_check.py` — the sign predicates (two repairs, one block)

History: unsound (review 0138) → repaired with an odd-part algorithm (unsound
again, `K15-C058`) → repaired by **removing the odd part** and testing one point
per constant-sign gap between the polynomial's own roots.

Audit questions:
1. Does `_roots_and_gaps` really meet every interval of constant sign, for
   `hi = oo` and for `hi` finite? (The `prev + 1` far point and the two extra
   points per gap are the parts to check.)
2. Are the six witnesses in `Computation/checker_adversarial.py` rejected *by the
   right clause* (not by an unrelated failure)?
3. Does `Poly.intervals(eps=1e-8)` terminate and return disjoint, ordered
   intervals at degree 33 with the K33 coefficients (29-digit rationals)?
4. The two independent supports: `predicate_crosscheck.py` (`function_range`) and
   `predicate_fuzz.py` (sampling plus the structured square family).

## 2. The certificates (`K15-C023`, `K15-C056`)

Both K33 variants are `ACCEPT`ed by Main's repaired checker with ratios
`0.186203285353` (a) and `0.186203218267` (b), matching Computation's reported
pair. Audit: re-run `verify_comp_cert.py` on both, then `exactcert.certify` and
the SymPy oracle, and confirm the three agree on the *same* rational.

## 3. The mathematics added this block

| Claim | What to attack |
| --- | --- |
| `K15-C035` | the boundary-pair count and the constant `3ΦR(R+1)⁵` (the factor `R` was dropped and restored in review 0223); the termwise arithmetic |
| `K15-C036` | the monotonicity claim (`K ⊂ K'` ⇒ `Ω_{K'} ⊆ Ω_K`) and the conclusion that no finite fixture can *verify* the inequality |
| `K15-C044` | the Hoffman cut condition and the two regimes (`R < 2`, `R ≥ 2`); the corrected statement (the first version was vacuous) |
| `K15-C045` | the synthesis: does anything follow that the averages do not already give? |
| `K15-C054` | degree ≤ 12 at `R = 2.09`; the constants `718.40` vs `1556.53` vs `845.11` |
| `K15-C018`/`C019` | the shell count reduction and the `ρ = 2.05/2.09` margins |
| `K15-C029r` | the signed estimate and its dependence on `N_A` |

## 4. What is *not* at issue

`K15-C002b`, `K15-C003r`, `K15-C004`, `K15-C012`, `K15-C024`, `K15-C037`,
`K15-C043` were audited in-block and no objection was raised; `K15-C027` (E's
Tammes enclosure) is accepted with its Musin–Tarasov scope. None of them depends on
the predicates.
