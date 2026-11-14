# Audit v2 — compact-tower simplification: P3 WITHDRAWN, (H2) NOT discharged

Block 2, single agent, write-scope `supervisor/simplify-architecture/` only. Supersedes block 1's
AUDIT.md in the places marked **RETRACTED**. Grades: **[read]** (statement checked in source),
**[proved here]** (complete paper-level proof given below, not machine-checked), **[imported]**
(cited, not verified), **[retracted]** (withdrawn).

## 0. Status of block 1's claims

| claim | status now |
|---|---|
| printed Lemma 2.7 is false without a non-factor-measurability hypothesis (`Y = X` ⇒ `δ_0`, `C ∋ 0`) | **kept**, [read] + machine-checked sharpness `differenceLaw_C_eq_one_of_diag` (m5 `D.lean`) |
| Theorem A′ = relative singularity from (H1) relative-product ergodicity + (H2) non-`Y`-measurability; wildness unused | **kept**, [read] m5's `relative_singularity_of_ergodic`, axioms `[propext, Classical.choice, Quot.sound]` |
| P2: (2.6) passes to countable joins **over a common base** | **kept**, [proved here]; note it does *not* apply to a tower (stages are compact over their *predecessor*, not over a common base) |
| P1: `D` is not a compact extension of a point | **weakened**: holds only w.r.t. Haar measure `m_D` (proof needs orthogonality of characters in `L²(µ)`, which a general `K`-invariant `µ` need not give). Not used in the paper's chain |
| **P3**: every tower stage is compact over the point, hence `Y_η ≠ D`, hence (H2) | **RETRACTED — false.** P3 needs transitivity of (2.6)-compactness, which fails (Counterexample 1) |
| "H2 is discharged for the paper's system" | **RETRACTED.** Nothing in this block discharges (H2) |
| "transitivity is cited by the paper (§3.1 preamble, Furstenberg 6.6/7.2)" | **RETRACTED.** The paper cites FZ for the compact/relative-weak-mixing *dichotomy* and for the module basis; it never invokes composition, and its printed induction does not need it. I supplied that citation myself; it is not load-bearing for the paper |
| m5's 120-line gap ("`∀ᵐ` diagonal ⇒ `d = g∘q`") is not needed for the application | **kept**, but it is not the binding gap; see §5 |

## 1. The exact definitions, pinned

**(2.6)** [read, paper p.9, verbatim]: at each successor `Y` over its predecessor `W`, *for every
bounded `H` on `Y` and every `ε > 0`, there are bounded functions `H_1,…,H_q` on `Y` and a finite
constant `B` such that, for every `k ∈ K`,*
`‖U_k H − Σ_r b^k_r H_r‖₂ < ε` *for some `b^k_r ∈ L^∞(W)` with `‖b^k_r‖_∞ ≤ B`. The basis
functions and bounds are fixed before `k` is chosen.*

This is the **finite-rank module form**: the orbit of `H` is covered, up to `ε`, by one finitely
generated `L^∞(W)`-module with sup-bounded coefficients. It is *not*:
* *orbit total boundedness of `U_k H` in `L²(Y)`* — strictly stronger, and **wrong** for compact
  extensions: in an isometric skew product the fibre coordinate `H(y,z) = z` has
  `U_kH = e^{2πiφ_k(y)}H`, whose `L²`-orbit is not totally bounded, while `Y → W` is compact. Any
  2ε composition proof written against orbit total boundedness proves a different theorem
  (block 1 fell into this; **retracted**);
* *distality* — a distal extension of a distal extension is distal, but (2.6) at both levels does
  not give (2.6) at the composite (Counterexample 1);
* *relative weak mixing* (`X ×_Y X` ergodic) — a logically independent property. It is what
  Theorem A′'s (H1) is, and it is the tower's *stopping* condition. A compact extension of a
  nontrivial factor has a *non*-ergodic relative product (the fibre diagonal is invariant), so (H1)
  and compactness are in tension, not equivalent.

**Tree counterpart** [read]: `At μ q H ε` (`MeasureTheory/CompactFactors/Functions.lean:45`) is
exactly (2.6): `∃ r B C (Hf : Fin r → X → ℂ)`, `∀ i, Measurable (Hf i)`, `∀ x, Σ_i ‖Hf i x‖ ≤ C`,
and `∀ k : K, ∃ a : Y → Fin r → ℂ` measurable, `∀ y, ‖a y‖ ≤ B`, `∫ dist(H (k•x), Σ_i a (q x) i * Hf i x)^2 ∂μ < ε^2`.
`Compact` = `∀ ε > 0, At … ε`. So the tree's notion is the module form, i.e. the *paper's* notion,
and not orbit total boundedness.

## 2. Counterexample 1 [proved here]: (2.6)-compactness is NOT transitive

Let `T(x,y) = (x+α, y+x)` on `𝕋² = 𝕋_x × 𝕋_y`, `α ∉ ℚ`, `µ =` Haar. Let `Y = 𝕋_x` with the
rotation `R_α`, `W =` point. Both extensions are *isometric*, i.e. the nicest possible compact ones.

(a) `Y → W` satisfies (2.6). Characters `χ_n(x) = e^{2πi n x}` are eigenfunctions:
`χ_n(R_α x) = e^{2πi n α} χ_n(x)`. **Extension from characters to every bounded `H`** (required —
character-by-character verification is not (2.6), which quantifies over all bounded `H`): let
`H = Σ_n c_n χ_n` with `|c_n| = |⟨H,χ_n⟩| ≤ ‖H‖₂ ≤ ‖H‖_∞`, take the truncation `H_N = Σ_{|n|≤N}c_nχ_n`
with `‖H − H_N‖₂ < ε`, and the family `{χ_{|n| ≤ N}}`, `B = max_{|n|≤N}|c_n| < ∞`, which is finite
and independent of `k`. Then `U_k H_N = Σ_{|n|≤N} (c_n e^{2πi n k α}) χ_n`, whose coefficient of
`χ_n` is a **constant** of modulus `|c_n| ≤ B`, and `‖U_k(H−H_N)‖₂ = ‖H−H_N‖₂ < ε` because `U_k` is
unitary. So (2.6) holds with error `ε` uniformly in `k`. ✓

(b) `X → Y` satisfies (2.6) with **zero error**. Write `χ_{n,m}(x,y) = e^{2πi(nx+my)}`. Then
`T^k(x,y) = (x+kα, y+kx+α k(k−1)/2)`, so
`U_k χ_{n,m} = c^k_{n,m}(x) · χ_{n,m}`, with `c^k_{n,m}(x) = e^{2πi(nkα + mαk(k−1)/2)} e^{2πi (mk) x}`,
a unit-modulus function of `x` alone, i.e. `∈ L^∞(Y)` with `‖c^k_{n,m}‖_∞ = 1`. Same extension
argument as (a): for bounded `H = Σ c_{n,m}χ_{n,m}`, truncate to a finite box `F` with
`‖H − H_F‖₂ < ε`; the family is `{χ_{n,m} : (n,m) ∈ F}`, the coefficient of `χ_{n,m}` is
`c_{n,m}c^k_{n,m}(x)` with sup-norm `|c_{n,m}| ≤ B < ∞` independent of `k` (the `k`-dependence sits
entirely in the unit-modulus factor of `x`), and again `‖U_k(H−H_F)‖₂ = ‖H−H_F‖₂`. So (2.6) holds
with `B = max_F|c_{n,m}|` and error `ε`, for every bounded `H`. ✓

(c) `X → W` does **not** satisfy (2.6). Take `H = χ_{0,1} = e^{2πi y}`, `ε = 1/10`. By (b),
`U_k H = ζ_k e^{2πi k x} H` with `|ζ_k| = 1`, and the functions `F_k := e^{2πi k x}H` are pairwise
orthonormal in `L²(µ)`: `⟨F_k,F_l⟩ = ∫∫ e^{2πi(k−l)x} dx dy = δ_{kl}`. If (2.6) held over the point,
the coefficients `b^k_r` would be **constants** with `|b^k_r| ≤ B`, so every `F_k` would lie in
`S + B(0,1/10)` where `S = {Σ_r b_r H_r : |b_r| ≤ B}`, a bounded subset of a finite-dimensional
space, hence totally bounded. A `1/10`-net for `S` then puts infinitely many of the pairwise-`√2`-
separated `F_k` within `1/10+1/10+1/10 < √2` of a single net point. Contradiction. ✓

**Conclusion.** Compact ∘ compact ≠ compact — even isometric ∘ isometric. Any "maximal compact
factor" argument that concludes compactness of the composite from compactness of the successors is
unsound. **P3 is withdrawn; it cannot be repaired from (2.6) alone, and I have found no extra
hypothesis short of assuming compactness over the base directly.**

## 3. Counterexample 2 [proved here]: the paper's tower can terminate at the TOP factor

Same system. The relative product `X ×_Y X` is `𝕋_x × 𝕋_y × 𝕋_y` with the diagonal skew action;
`(x, y_1, y_2) ↦ y_1 − y_2` is invariant and non-constant, so `X ×_Y X` is **not** ergodic, and the
paper's successor step applies: the invariant kernel `e^{2πi(y_1−y_2)}` is bounded, non-constant,
with both coordinate conditional expectations zero, and the fibre projection `Q_y` it produces
generates the fibre character `e^{2πi y}`. Hence the strict extension `Y'` is *the whole space*
`X = 𝕋²`. Now `X ×_X X` is the **diagonal copy** of `X`, not a point: its conditional measures are
`δ_x`, so `µ ×_X µ` is the diagonal image of `µ`, and it is ergodic **iff `µ` is ergodic** — true
here. So the tower stops with `Y_η = X`. (Correction of block 2, which said "a single point"; the
diagonal `X` and the point agree only for the *difference law*, where both give `δ_0`.)

Consequence: the hypotheses of the printed Lemma 2.7 do **not** exclude `Y = X`; at `Y = X`
conditionally independent samples coincide, `ν_Y = δ_0`, and `ν_Y(C) = 1` because `0 ∈ C`. So the
printed Lemma 2.7 fails *inside its own apparatus*, not only in a degenerate side case.

Two caveats, stated to avoid overclaiming. (i) The example has a `ℤ`-action, the paper's application
a `K`-action; the (2.6) definition and the tower construction are group-agnostic, so the tower
counterexample transfers, but see (ii). (ii) A *complete* refutation of the printed lemma needs one
instance satisfying *all* its hypotheses, including "$d$ is equivariant with wild law"; for the skew
shift that would mean a measurable `d : 𝕋² → D` with `d∘T = u·d` (`u ∈ K`, `u ≠ 1` fixed) and
`d_*µ = m_D`. I did **not** construct such a `d`, so what is established here is exactly:
*the tower's hypotheses do not exclude `Y_η = X`, and at `Y = X` the conclusion is false for every
`d`*. Whether the paper's own `(D,µ)` produces `Y_η = D` is `(M)`, still open (§5).

## 4. What survives, with corrected hypotheses

**Theorem A′ (unchanged).** `X` ergodic, `K`-action measure preserving, `q : X → Y` equivariant
factor, `d : X → D` equivariant Borel; assume (H1) `µ ×_Y µ` ergodic, (H2) `d` not `Y`-measurable.
Then the law `ν_Y` of `d(x)/d(x′)` over `Y` is `C`-null. No wildness, no compactness, no (2.6), no
transitivity. [read] m5's `relative_singularity_of_ergodic` (with (H2) in the `¬∀ᵐ`-diagonal form);
paper-level proof is the radial threshold `r = inf{t : µ_R(d(x)/d(x′)) ∈ j(B(0,t))} = 1}`, `r = 0` ⇔
(H2) fails, `r > 0` ⇒ four equidistant points (m5's `A.lean`/`B.lean`, machine-checked). The
block-1 remark stands: `sprint/simplify/REPORT.md` §5's `ρ = |j^{-1}(·)|` sketch does not parse.

**P1′ (Haar only).** With `µ = m_D`, `D` is not a (2.6)-compact extension of a point: `k·ψ_z =
ψ_{kz}` [read, `(ad)(z) = d(az)`, `ψ_z(d) = d(z)`], the `ψ_{kz}` are characters of distinct points,
hence orthonormal in `L²(m_D)` and `√2`-separated, while `S + B(0,ε)` is totally bounded. Not used:
for a general wild `µ` the characters are not orthogonal in `L²(µ)`, so the argument does not run,
and invoking `µ = m_D` would presuppose Theorem 2.3.

**P2 (unchanged, unused).** (2.6) is closed under countable joins over a common base `W`
(tail truncation in `L²`, coefficients in `L^∞(W)` with `max_n B_n`). It does not apply to the
paper's tower, whose stages are compact over their predecessors.

## 5. The precise missing lemma — and why the simplification is conditional, not free

**(M)** For `µ` ergodic, `K`-invariant on `D` with `µ(C) = 0`, the paper's tower for `(D,µ)`
has a **proper** terminal factor: `Y_η ≠ D`.

**(M‴)** Equivalent in practice, and sharpest: *(D,µ) is weakly mixing*, i.e. `µ × µ` is ergodic
under the diagonal `K`-action. Given (M‴), take the trivial factor: (H1) holds, and `C`-nullity of
the conditional difference law is **free** (`wild_independent_difference`, `Basic.lean:326`,
machine-checked = Lemma 2.4). Then §2.4 and §3.1 are deleted wholesale and Theorem A′ is not even
needed. Given only (M), Theorem A′ with (H2) from `Y_η ≠ D` replaces §2.4's induction.

Why this is not a simplification of the paper's proof: the tower exists precisely *because* (M‴) is
not known; `(M‴)` is strictly weaker than the paper's Theorem 2.3 (wild ⇒ `m_D`) but it is the same
kind of statement (Fourier/eigenvalue vanishing), and I found no cheap route: `µ`'s only inputs are
`K`-invariance, ergodicity and `µ(C) = 0`; `L²(µ)`-orthogonality of characters is exactly what one
does not have. **H2 is not discharged. No claim is made that the paper's §2.4 can be deleted.**

The honest ledger entry for the sprint's headline, then, is: *the ergodicity + four-equidistant-points
theorem is correct and machine-checked with (H2) explicit; it replaces §2.4 **conditional on (M)**, and
(M) is the paper's own open bookkeeping step, not a free gain.*

**Block 3 addition.** `(M)` and `(M‴)` are now separated and the first route to `(M‴)` is tested and
killed: see `OBSTRUCTION.md` (self-contained packet). Summary of that route: a non-constant
eigenfunction of `(D,µ)` with unimodular eigenvalue refutes `(M‴)` via the invariant
`f(x)\overline{f(y)}` [proved here]; but `|µ̂(z)| = 1` is a *support* condition (µ carried by a coset
of `ann(z)`), not an eigenfunction condition, and wildness plus ergodicity do not exclude it, since
`C ∩ (a·ann(z))` is a one-parameter family inside the coset. So the point-spectrum route does not
reach `(M‴)`; the trap that makes it look promising (`ψ_z(x)\overline{ψ_z(y)}` invariant) is false —
`(x,y) ↦ xy^{-1}` is equivariant, not invariant. Note also that Counterexample 2 above is a generic
skew shift: it refutes the general propagation `P3` and says **nothing** about the paper's specialised
`(D,µ)` system, and is not used as if it did.

## 6. Consequence for the Lean track (please route to it)

m4's successor step ("`q` in the class of `At`-compact extensions of the trivial factor, successor
`u` ⇒ `u` in the class") **is a (2.6)-transitivity statement, and Counterexample 1 refutes it**.
So R1–R4 (maximality over the class, one application of Theorem A) is unsound as designed, and m4's
"150–400 lines of total-boundedness work" would be spent proving a false statement. This is a
negative result worth acting on, not a cost estimate.

**Fallback (consolidated from the retiring `supervisor/simplify-lean/CENSUS.md`, [read], claims not
verified by me):** the largest declaration-level redundancy in the tree is a twin pair of
contradiction theorems — `Analysis/PlaneSpectrum/ConditionalSpectrum.lean:310`
`finite_uniform_precision_contradiction` (155 proof lines, `FiniteEncodingApproximationAt`,
`hwild` about `differenceLaw (µ.map (q∘p))`) and `MeasureTheory/CompactFactors/ConditionalLimits.lean:385`
`ambient_uniform_precision_contradiction` (153 proof lines, `AmbientEncodingAt`, `hwild` about
`differenceLaw (µ.map q)`) — same conclusion `False`, same 8 hypotheses except encoding and wild law,
near-verbatim proofs, neither an instance of the other. A common core lemma + two wrappers is the
candidate: ~300 lines touched, one shared low-level module needed for the `norm_integral_sq` dupe
(`Fourier.lean:96` vs `Kernels.lean:45`) because the import directions conflict. CENSUS also reports
the rigidity half has only ~70 lines of mechanical duplication (do not hunt there). Reproduce:
`python3 supervisor/simplify-lean/.scratch/census.py` then `.scratch/dup2.py` (113 s, no Lean).
**This is the recommended next build-free target if the tower route stays blocked.**

**Recorded, not consumed:** `supervisor/simplify-angular/FIVE-CYCLE-CORE.md` [read, first 40 lines] —
candidate to hand to the independent verifier: replaces paper §6.3.4's five-residue case analysis by a
5-step hand argument from (V)(D)(N)(R) over `I = ℤ/5ℤ` (21 valid lists; no Lemma 6.7, no (6.6), no
`S(3)` adjacent-pair input), with `checks/five_cycle_full.py` rc 0. Its task is untouched here.

## 7. Soundness ledger (this block)

| item | grade | depends on |
|---|---|---|
| (2.6) verbatim; `At`/`Compact` = module form; `0 ∈ C`; single application of Lemma 2.7 at `d = id_D` | [read] | paper p.9/14, `Functions.lean:45,52`, `Basic.lean:300` |
| Theorem A′ and its four-point argument | [read] machine-checked (m5) | `[propext, Classical.choice, Quot.sound]` |
| Lemma 2.4 = C-nullity at the trivial factor | [read] machine-checked | `wild_independent_difference` |
| Counterexample 1: (2.6) not transitive (isometric∘isometric) | [proved here], elementary, no machine check | explicit cocycle computation |
| Counterexample 2: tower can end at the top factor | [proved here] | same computation |
| P1′ Haar-only, P2 common-base joins | [proved here] | — |
| (M)/(M‴) is the missing lemma; H2 NOT discharged | assertion of a gap | no proof either way |
| CENSUS twin-pair fallback, FIVE-CYCLE-CORE | [read] another worker's claim, unverified | — |

## 8. Next exact obligation

Decide (M‴) for wild `µ` — equivalently, find a factor of `(D,µ)` whose relative product is ergodic
*without* first proving Fourier vanishing. Two concrete attacks, in order of cheapness:
(1) try to prove `µ × µ` ergodic from `µ(C) = 0` using only the coset structure (`wild_coset_null`)
plus divisibility of `K` — if this works, §2.4 + §3.1 + Theorem A′ all become unnecessary for the
paper, and `ergodic_wild_fourier` gets a 3-line proof at `q =` trivial;
(2) failing that, produce the first stage of the tower for `(D,µ)` explicitly and ask whether it is
proper — a counterexample to `Y_η = D` is a *positive* result and would settle (H2).
Do not start a Lean build for either.

---

> ### RETRACTION BANNER (block 5) — supersedes parts of §§9–11 below
> The current, corrected statement of every result and dependency is in **`LEDGER.md`**. Specifically
> retracted from this file: (R1) §10's scope sentence that constant-modulus eigenfunctions with
> nontrivial eigenvalue "must be tolerated" — **false**, they obstruct weak mixing via `f(x)\overline{f(y)}`
> (LEDGER §2, arrow (A)); (R2) the claim in §9 that Astra's Lemma A proof needed a repair — it does not,
> `K`-invariance transports the constant `c` directly; (R3) the tensor-correlation display in §11, where
> **both** factors transform and the second inner product is not `u`-independent (correct form: LEDGER
> eq. (T′)); (R4/R5) the "(U) ⇒ M3" arrow and the "(U) with upper Banach density 1" phrasing are
> **withdrawn**. Everything else in §§9–11 stands: Astra's Lemma A with its proof, the correction that
> `ann(z)` is not `K`-stable, the countably-many-lines description of `C ∩ (a·ann(z))`, the centered M3
> criterion, and the proof that (M3) ⇒ diagonal ergodicity (redone correctly in LEDGER §3).


# Block 4 — Astra's correction integrated, and one finite-character argument tested

Grades: **[verified here]** = I re-derived it in this block; **[Astra]** = supplied by Astra's review,
independently checked here; **[proved here]** = my own paper proof; **[classical/imported]** = cited.

## 9. Astra's lemma: statement, and independent verification

**Lemma A [Astra; verified here].** Let `µ` be a `K`-invariant probability on `D` (no ergodicity
needed), `z ≠ 0` in `E`. If `|a_z| = 1`, where `a_z = µ̂(z) = ∫ψ_z dµ`, then `a_z = 1` and
`µ = δ_{1_D}` (the trivial character). Consequently a **wild** `µ` satisfies `|a_z| < 1` for every
`z ≠ 0`.

*Proof.* (i) `span_ℤ K = E`. For real algebraic `t` pick `n ≥ 1` with `|t| ≤ 2n`; put
`u = t/(2n) + i√(1 − (t/2n)²)`, `v = ū`. As `F = ℚ̄∩ℝ` is real closed, the square root lies in `F`;
then `u ∈ E`, `|u|² = (t/2n)² + 1 − (t/2n)² = 1`, so `u ∈ K`, and `v ∈ K`; `t = n(u+v)`. Hence
`F ⊆ span_ℤ K`, and `iF ⊆ span_ℤ K` because `iK = K`; so `E = F + iF ⊆ span_ℤ K ⊆ E`. ✓
(ii) *Equality case of Cauchy–Schwarz*: `1 = |a_z| = |∫ψ_z dµ| ≤ ∫|ψ_z|dµ = 1`, so `ψ_z = c` µ-a.e.
for some `|c| = 1`.
(iii) `K`-invariance gives `a_{uz} = ∫ψ_{uz}dµ = ∫ψ_z(u·d)dµ = a_z` for each `u ∈ K`; by (ii)
`ψ_{uz} = c_u` µ-a.e. As `K` is countable, one conull `N` carries all these identities at once.
(iv) For any `w ∈ E` write `w = Σ_j n_j u_j z` (possible by (i)); then for `d ∈ N`,
`d(w) = Π_j d(u_j z)^{n_j} = Π_j c_{u_j}^{n_j}`, a number independent of the representation and of
`d ∈ N`. So every `ψ_w` is µ-a.e. constant with a value `c(w)`, and `c : E → 𝕋` is a homomorphism.
(v) The `ψ_w` separate points of `D`, so `µ({d : d(w) = c(w) ∀w}) = 1` and the set is a single point
`d_0`: **`µ = δ_{d_0}`**.
(vi) `δ_{d_0}` is `K`-invariant, so `d_0(uw) = d_0(w)` for all `u ∈ K`, `w ∈ E`: `d_0` kills `(K−1)E`.
For `r = (1+i√3)/2`, `s = r̄` both in `K` we have `(r−1) + (s−1) = r+s−2 = −1`, so `−1` is killed; then
for `u ∈ K`, `d_0(u) = d_0(1)·d_0(u−1) = 1·1`; by (i) `E = span_ℤ K`, so `d_0 ≡ 1`. ∎

*Note on the writeup.* Astra's line "`c = ψ_z = ψ_{rz}ψ_{sz} = c²`" needs the constants for `ψ_{rz}`,
`ψ_{sz}` to already equal `c`; that is exactly what step (vi) supplies via `K`-invariance, so the
conclusion is right but the ordering has to be: homomorphism first, `µ = δ_{d_0}`, invariance second,
`d_0` trivial third. Verified as repaired above.

**Effect on block 3.** The coset branch is **dead, and no counterexample of that shape exists**: block 3
offered "`µ` carried by a coset of `ann(z)` with `µ(C)=0`" as the candidate refutation of `(M‴)`. That
candidate required `|a_z| = 1`, which now forces `µ = δ_{1_D}`, i.e. `µ(C) = 1`. Closed; no further
search is warranted, and none was done.

## 10. Astra's corrections to block 3, accepted

1. **`H_z = ann(z)` is not `K`-stable**, so my "the induced action of `K` on `D/H_z ≅ 𝕋` constrains
   things" is **withdrawn**: `u·H_z = ann(uz)` [verified: `(u·d)(z) = d(uz)`], so `H_z` is stable only
   if `ℤuz = ℤz` for all `u ∈ K`, false since `u ∉ ℚ` generically. No quotient action exists.
2. **`C ∩ (a·ann(z))` is a countable union of parallel affine lines**, not one line [verified:
   `j(ξ)(z) = a(z)` reads `ξ·(Re z, Im z) = θ_0 + 2πk`, `k ∈ ℤ`]. Block 3's "one-parameter family"
   was loose; the qualitative conclusion it drew is now moot anyway (Lemma A).
3. **The M3 criterion, corrected.** Block 3's next step proposed `Avg_u |a_{uz−z}|² → 0`. That is the
   *uncentered* quantity and it is wrong: under M3 it converges to `|a_z|⁴`, and at `z = 0` it equals
   1 for every `u`. **Withdrawn.** The correct condition uses the centered characters
   `h_z = ψ_z − a_z` (character spans dense in `L²(µ)` by Stone–Weierstrass; no Haar orthogonality
   anywhere):
   **(M3)** for all `z, w ∈ E`, along a fixed finite Følner sequence `Φ_n ⊆ K`,
   `avg_{u∈Φ_n} |a_{uz−w} − a_z \overline{a_w}|² → 0`, with no uniformity over frequencies.
   Justification [verified here]: `⟨U_u h_z, h_w⟩ = a_{uz−w} − a_{uz}\overline{a_w} = a_{uz−w} − a_z\bar a_w`
   using `a_{uz} = a_z` (the `K`-invariance computation of step (iii) above). For `z = 0` or `w = 0`
   the quantity vanishes identically (`a_{−w} = \overline{a_w}`), so M3 is only about nonzero pairs.
4. **`(M‴) = M3`**, not a separate hypothesis: weak mixing `⇔` matrix coefficients of centered vectors
   decay in mean square `⇔` `µ⊗µ` ergodic for the diagonal action (classical: `T` weakly mixing iff
   `T×T` ergodic; the `⇒` direction is re-proved below in the finite-character form to keep the
   dependence explicit). So block 3's `(M‴)` and Astra's M3 are the same statement; M3 is the usable
   analytic form.
5. **M3 is not equivalent to H2**, and *first*-stage properness does not give *terminal* properness
   [verified: tower stages increase, `Y_0 ⊆ Y_1 ⊆ … ⊆ Y_η`, so `Y_1 ≠ D` leaves `Y_η = D` open; the
   converse direction `Y_η ≠ D ⇒ Y_1 ≠ D` does hold]. Block 3's option (B) ("compute the first stage
   and decide properness") is therefore **insufficient as stated**.

## 11. One targeted finite-character argument, and where it stops

**What it proves [proved here].** `(M3) ⇒ µ⊗µ` is ergodic (the diagonal action), with no Haar
classification and no compact-tower input.
*Proof.* Let `F ∈ L²(µ⊗µ)` be invariant, `∫F = 0`, `‖F‖ = 1`. Take a finite character polynomial
`G = Σ_{(z,w)∈Σ} c_{z,w} ψ_z⊗\bar ψ_w` with `‖F − G‖ ≤ η` and `∫G = 0` (drop the `(0,0)` coefficient;
`ψ_z⊗\bar ψ_w` span densely by Stone–Weierstrass). Invariance gives `‖U_{u⊗u}G − G‖ ≤ 2η` for all `u`.
On the other hand
`avg_u ‖U_{u⊗u}G − G‖² = 2‖G‖² − 2Re avg_u ⟨U_{u⊗u}G, G⟩` and
`⟨U_{u⊗u}G,G⟩ = Σ c_{z,w}\bar c_{z',w'} a_{uz−z'}\overline{a_{uw−w'}}`;
by M3 (finitely many pairs) the average tends to
`Σ c_{z,w}\bar c_{z',w'}(a_z\bar a_{z'})(\overline{a_w\bar a_{w'}}) = |Σ c_{z,w}a_z\bar a_w|² = |∫G|² = 0`.
(The passage of the product is legitimate: by M3 each factor converges to its constant in mean square,
hence in mean, and the product of a mean-square-convergent and a bounded sequence converges in mean by
Cauchy–Schwarz; finitely many pairs, so no uniformity is needed.)
So `avg_u‖U_{u⊗u}G−G‖² → 2‖G‖² ≥ 2(1−η)²`, contradicting `≤ 4η²` for `η < 1/3`. ∎
Two hypotheses were used and nothing else: density of characters (Stone–Weierstrass) and M3 at
finitely many frequency pairs. **No pointwise strictness, no Haar.**

**The target has to be restricted [proved here, with a witness].** "Exclude every nonconstant joint
Koopman eigenfunction" is *false as a goal*: constant-modulus eigenfunctions with a nontrivial
unimodular eigenvalue coexist with diagonal ergodicity. Witness: `G = ℤ` acting on `𝕋²` by
`(R_α, R_β)` with `1, α, β` rationally independent — the diagonal action is ergodic (only the trivial
character is invariant, since `mα + nβ ∈ ℤ` forces `m = n = 0`), yet `F = ψ_1⊗ψ_1` is a nonconstant
eigenfunction with `|F| ≡ 1` and eigenvalue `e^{2πi(α+β)} ≠ 1`. So the correct target is exactly
**(E0)** there is no nonconstant `F` with `U_{u⊗u}F = F` (invariant functions) — equivalently no
nonconstant joint eigenfunction that is either of non-constant modulus (`|F|` would then be a
nonconstant invariant) or of eigenvalue `1`. Eigenfunctions of modulus one with `χ ≠ 1` must be
*tolerated*, and any argument that kills them is wrong.

**Where pointwise strictness fails to supply a uniform bound — exactly here.**
Suppose `F` is a nonconstant invariant function and `G` its finite character approximant as above.
Write `λ_{z,z'}(u) := a_{z−u^{-1}z'}` (`= a_{uz−z'}` by invariance). Then
`‖U_{u⊗u}G − G‖² = 2‖G‖² − 2Re Σ_{z,z'} λ_{z,z'}(u)⟨f_{z'},f_z⟩`, `G = Σ_z ψ_z⊗f_z`,
and the whole `u`-dependence sits in the coefficients `λ_{z,z'}(u)` for `z ≠ z'`.
Invariance forces `Re Σ λ_{z,z'}(u)⟨f_{z'},f_z⟩ ≥ ‖G‖² − 2η²` **for every `u`**. A contradiction
requires a **uniform** statement:

> **(U) [the reduced lemma]** For every finite `Z ⊆ E` and `δ_0 > 0` there are `δ > 0` and a set
> `D ⊆ K` of upper Banach density `1` such that `|a_{z−u^{-1}z'}| ≤ 1 − δ` for all `u ∈ D` and all
> `z ≠ z' ∈ Z` (with `z ≠ u^{-1}z'`).

Lemma A gives only the pointwise statement `|a_{z−u^{-1}z'}| < 1` **for each individual `u`**, and for
the pair where `z = u^{-1}z'` the coefficient is exactly `1` (so the deficit is `0`, and the strict
inequality `|a_0| < 1` fails outright at `a_0 = 1`). Passing from "`< 1` for every `u`" to "`≤ 1 − δ`
off a density-zero set, **uniformly in `u` and across frequencies of unbounded size**, is precisely
what no hypothesis in the paper supplies: the only inputs are `K`-invariance, ergodicity and
`µ(C) = 0`, and Lemma A is a statement about *values* of `a` at frequencies whereas (U) is a statement
about *limits of `a` along `K`-orbits of frequencies*. Also `(U) ⇒ M3` strictly, so proving (U) would be
strictly harder than the paper's own §3: this route is a correct reduction, not a shortcut.

**Position of the two conditions.** `(U) ⇒ M3 = (M‴) ⇒ µ⊗µ` ergodic `⇒ (M)` with the trivial factor
usable (`wild_independent_difference`, machine-checked). The gap between Lemma A and M3 is the entire
remaining content, and it is a uniformity/decay statement, not a defect in Astra's lemma.
