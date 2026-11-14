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

---

## 5. Audit request — the repaired cut/flow theorem (`K15-C093`, `CUT_FLOW_THEOREM.md`)

Requested by the reviewer at `K15-REVIEW-0353-M-EVIDENCE`. Four defects were reported and
are repaired; **what is wanted is an audit of the repaired statement, not of the old one.**

**What to check, in order.**

1. **The directed model.** `CUT_FLOW_THEOREM.md` §1: each undirected edge gets **two** arcs
   `v→w`, `w→v`, each with the full capacity `Φ_{vw}`; the transfer is the net
   `ψ(v,w) = f(v→w) − f(w→v)`. Check (a) `|ψ| ≤ Φ_{vw}`, (b) that every transfer arises
   this way, (c) that the two models have the same achievable divergence vectors.
2. **The cut orientation.** Finite-capacity `s`–`t` cuts must have `X = S ∖ F = ∅` — any
   outside vertex on the source side puts its infinite arc `w→t` across the cut. Check the
   capacity computation `Σ_{F∖U}b⁺ + Σ_U b⁻ + cap(U) = Σ_F b⁺ − Σ_U b + cap(U)`, and hence
   that `min-cut ≥ Σ_F b⁺ ⟺ (C)`.
3. **The transfer satisfies the demand.** From the saturated `s`-arcs,
   `div_ψ(v) = b(v)` for `b(v) > 0` and `≥ b(v)` for `b(v) ≤ 0`. This is the step where the
   `b(v)⁻ = 0` capacity matters; check it for `b(v) = 0` too.
4. **The second proof.** §1, duality + coarea: keep the box multipliers (`z₁, z₂`) so the
   alternative is `Σ_F y_v b(v) > Σ_e Φ_e|y_v − y_w|`; then
   `Σ_F y_v b = ∫_0^∞ Σ_{U_t} b` and `Σ_e Φ_e|y_v−y_w| = ∫_0^∞ cap(U_t)` with
   `U_t = {v : y_v > t}` for `y ≥ 0`. Check both identities and that `U_t ⊆ F`.
5. **Theorem 2.** `K := ∏_e[−Φ_e, Φ_e]` is compact by Tychonoff **without** a uniform
   bound; `S_F` is closed because `div_φ(v)` is a finite sum (local finiteness only); the
   finite intersection property applies. Check that no step secretly uses
   `sup_e Φ_e < ∞`.
6. **The threshold formula.** `t* = +∞` if some `U ⊆ F` has `δ⁺(U) = ∅` and `Σ_U b > 0`;
   otherwise `max(0, sup_{δ⁺(U)≠∅} Σ_U b/|δ⁺(U)|)`. Check both branches, including that the
   `max(0,·)` is needed and that the empty-boundary case is capacity-free.

**What is not at issue.** The graph theory is elementary and standard; the question is
whether the reduction is written correctly. Nothing here bears on the density bound.

**One specific thing to try to break.** Find a deficit vector and a graph where the two
proofs disagree, or where the threshold formula's two branches are both needed for the same
instance. That would be the cheapest way to find a fifth defect.

---

## 6. Audit request — the Barlow chain (`K15-C094`, `C095`, `C096`, `C101`, `C102`)

This is a chain: each claim is used by the next, so a defect anywhere invalidates the
downstream statements. Please audit in this order and stop at the first failure.

**6.1 `K15-C094` — every Barlow cell is `√32`.** `BARLOW_CELLS.md` §1–§3. Four steps.
- (F1) distances: exactly 12 at 2, everything else `≥ 2√2`. Check the three-Λ-point claim
  (`T` is the centroid of `{0,a₁,a₂}`, so `|T| = 2/√3` with multiplicity exactly 3) and the
  enumeration of the distance spectrum in the table.
- (F3) covering radius `≤ √2` via `(2/√3)² + (H/2)² = 2`. Check that the slab argument
  covers *every* point, not just those in the layer planes.
- Lemma 1 (cell = contact cell) and Lemma 2 (two contact configurations up to isometry).
  **Lemma 2 is the load-bearing one**: the two non-zero cosets of `Λ` in `(1/3)Λ` are `±T`,
  their in-plane nearest sets are `𝒜 = {30°,150°,270°}` and `ℬ = 𝒜+60°`, and a `60°`
  rotation plus `z ↦ −z` collapse four sign combinations to two. Check that the `60°`
  rotation is used only as an isometry of `R³` and **not** as a packing symmetry (it is not
  one: fcc has three-fold, not six-fold, symmetry about `[111]`).
- Step 4: the average is `2√3·H = 4√2` in *every* Barlow packing, `ABC…` is fcc-configured
  in every layer, `ABA…` hcp-configured in every layer, hence both cell volumes are `4√2`.
  Check the "every layer" part — this is where a slip would let one case escape.
- **Specifically try to break Lemma 2** by finding a Barlow stacking whose contact set is
  neither of the two. `Computation/barlow_cells.py --sweep 6` runs 48 random stackings
  (346 layers) and prints the classification per layer; all were one of the two.

**6.2 `K15-C095` — the crack packing.** Two analytic bounds (`H ≤ d ≤ 2H` for 2-separation
respectively saturation), the two infinite closed components at `d > 2.09`, the crack-face
`b = −1.328495`, and the density claim `δ = π/√18` (the `O(r²)` count). Check that the
density argument needs only "one crack is a surface", i.e. that the displaced layers number
`O(1)` and not `O(r)`.

**6.3 `K15-C096`/`C101`/`C102` — the `V(2.09)` chain.**
- `ρ* = 2(√32/V_dod)^{1/3} = 2.012718662` and `V_dod(1.045)³ = 6.333804106`.
- `C101`: the Tammes-13 split. **This one leans on `θ₁₃ = 57.1367°` from Musin–Tarasov**,
  which is `ACCEPTED WITH SCOPE` in `ACCEPTED.md`; check the direction of the inequality
  (`2.09` is *below* the threshold, so at most 12 points) and that case (A)'s scaling
  `x ↦ 2x/ρ` is legitimate.
- `C102`: the nearest admissible extra centre. The minimisation is over a 2-parameter family
  with the closed form `r₊ = ⟨u,x⟩ + √(⟨u,x⟩² − (ρ²−4))`, so it is *checkable to interval
  arithmetic standard* — Main ran it numerically only (**2×10⁶ directions + Nelder–Mead**).
  **This is the weakest link in the chain and the one place where a certified computation
  would upgrade a `PROVED` claim.** Target: certify `min|p| ≥ 2.955706346`.
- `BARLOW_CELLS.md` Lemma 3 (support-function truncation criterion) and the tangency remark
  (`2R_cell = 2√2` = the next distance).

**6.4 What is *not* claimed, so do not accept it as a target.** `V(2.09) = 6.333804` is a
**conjecture** (settled at the icosahedral base only); `b ≡ 0` does not characterise Barlow
packings; and no bound in `RESULTS.md` moves. If a finding would make any of these look
established, that is itself a defect to report.
