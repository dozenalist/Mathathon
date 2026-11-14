# Independent review for supervisor review 27616 — role X

Author: Counterexamples (X), session `i-ve-attached-viazovska-f7hh`.
Branch `kepler15/counterexamples/run-01`. All tracked paths under `KeplerConjecture/`.
Ultramath is **off** for this block (no swarm was started, resumed, or consulted; my only
swarm `smwfwicjx` ended solved in an earlier block and is not resumed).

Audited revision: the checkpoint named in the assignment,
`a08f378be6a03f80ac075b34f8ba99aeb8201d9e` (`kepler15/main`), plus
`kepler15/experimental/run-01` @ `7cdec5deee2b3c60845be49c9c5cecc1f3592f78`, and
`kepler15/comp-01a1d8c0` @ `4b509e33fe1f5d50d37f7dd19b698d708312d35a`.

**Provenance warning.** `kepler15/main` has moved since the assignment was written: its tip is
now `0c3ee751254b1b61f16eb175d9bd8d571f842b18`, and `Main/CLAIMS.md` grew by 192 lines between
`a08f378` and `0c3ee75`. `Main/Evidence/m2-proof.md` and `Main/Evidence/m1-certificate.json` are
**byte-identical** at both commits, so every finding below about the exported proof applies to
the current tip as well. The *ledger* text I audited is the `a08f378` version
(`CLAIMS.md` blob `1529675e`); the newer `CLAIMS.md` (blob `f9bbb291`) is **not** audited here.

## Immutable source hashes

| Object | Blob SHA-1 |
| --- | --- |
| `Main/CLAIMS.md` @ `a08f378` (audited) | `1529675e519cadb20ba9fcb051db20c37104dd53` |
| `Main/CLAIMS.md` @ `0c3ee75` (NOT audited) | `f9bbb29156d3e3af9d0911d7ef17d8926c3dc503` |
| `Main/Evidence/m2-proof.md` (both tips) | `485bd5f3a004e36048a4fa0491a3bb700c7cd6a9` |
| `Main/Evidence/m1-certificate.json` | `1c63c6a3d41f1551ea4b603797d9940f28c2929e` |
| `Experimental/CLAIMS_FOR_X.md` | `af6ca3fe5765de4317c2baf4f653a766077e9ed5` |
| `Experimental/LOCAL_CRITERION.md` | `9f3162e7f480d67defd3d28713f79cc2d06f6256` |
| `Computation/RESULTS_baseline.md` | `db6b18af83dea4309b23c6aafd924c6437e0ff67` |
| `Computation/INTERFACE.md` | `e205669e13efa2284a5aa243da48447e2ab4fcda` |

Evidence for this review: `Counterexamples/review_27616_checks.py` and its log
`Counterexamples/evidence/review_27616_checks.out` (15 check points, no failures).

## Verdict table

| Claim | Verdict | One-line basis |
| --- | --- | --- |
| K15-C002 periodic approximation | **REPAIRED** | direction error at the division confirmed; `#C_in <= vol(B_R)/S^3` fixes it and the statement survives |
| K15-C003 count-price indexing | **REPAIRED** | `fix j` gives `nk²`; `fix l` gives `nk`; statement survives with the *same* constant |
| K15-C004 empty-interior vacuity | **ACCEPTED** | proof correct; Main's earlier `Q³` "counterexample" is not one |
| K15-C005 (ii) `mean B_kappa <= 0` | **REFUTED** | exact: `mean B_kappa = kappa·c·fhat(0) > 0` for every periodic packing |
| K15-C005 (i) 12-contact value | **REPAIRED (scope)** | valid only for λ-compactly-supported `f`; not the infinite-packing sum |
| K15-C010b log-norm term | **REPAIRED (scope)** | in the PD class `‖fhat‖₁ = f(0)`, so the term is *identically zero* |
| K15-C013 (a) count bound | **ACCEPTED**, threshold **REPAIRED** | `δ < 28^(1/3)−3 = 0.036589…`, not `0.0366` |
| K15-C013 (b) explicit `δ₀` | **REPAIRED → PROVED with value** | `δ₀ ≥ 0.0910` via Musin–Tarasov `d₁₃`; see §D |
| K15-C014 grid LP | **ACCEPTED as invalid** (local rerun authoritative) | artifact set absent from every fetched branch — provenance gap |
| K15-E001 cluster criterion | **ACCEPTED with caveat** | boundary/absorption step sound; hypotheses realisable with `D=4, Vmax=27` |
| K15-E002 dodecahedral fixture | **ACCEPTED** (matches my X-C003) | closed form reproduces `5.5502910285`; realisation question settled YES |
| K15-E003 monotonicity | **ACCEPTED** | `vol_{K'} Ω ≤ vol_K Ω` for `K ⊆ K'`; unbounded cells only strengthen |
| K15-E004 open cluster question | **OPEN (agreed)** | still no witness; see O2 below |
| K15-E2 `N(2)=12` row | **REPAIRED (scope)** | valid at `ρ=2` by kissing number; `ρ=2+ε` now proved for `ε ≤ 0.0910` |
| K15-E3 Delaunay obstruction | **UNRESOLVED** | source locator not checked in this block |

## A. C002 — the periodic approximation: direction error confirmed, repair verified

`m2-proof.md` Step 1 (lines 118–131) proves
`Σ_{C∈C_in} vol C ≥ vol B_R (1−O(S/R))`, which yields a **lower** bound
`#C_in ≥ vol(B_R)(1−O(S/R))/S³`. The next display then divides by `#C_in` and keeps the same
inequality. That is invalid: from a lower bound on `#C_in` one gets only
`1/#C_in ≤ S³/(vol(B_R)(1−O(S/R)))`, so the chain gives `n(C*) ≥` (a quantity) `/` (something
smaller than `#C_in`) — no conclusion. The supervisor's diagnosis is correct.

*Repair (verified to be sufficient).* The tiles of `C_in` are disjoint and contained in `B(0,R)`,
so `#C_in ≤ vol(B_R)/S³` **trivially**, whence
`n(C*) ≥ N(0,R)·S³/vol(B_R) − O(S³·R²S/vol B_R) = c S³(1+o(1))`.
No shell correction is needed, the errors stay additive, and `c = 0` gives the trivial bound.
*The statement of C002 is therefore sound; only the exported proof needs the one-line repair.*
Additionally the ledger's corrected hypotheses (`f`, `f̂` continuous, decay `(1+|x|)^{-3-η}`,
`f̂(0) > 0`) are **still absent** from `m2-proof.md` lines 48–60, 77–95 and 239 at both tips —
that defect is real and unfixed in the artifact, exactly as the review says.

## B. C003 — count price: indexing error confirmed, same constant survives

Published (lines 258–265): *fix `j`*, then "by (LC(A,n)) summed over the `k` centres …
`#{bad with this j} ≤ nk`, so `Σ_bad f ≤ nk·max(M,0)`". But the bound is *per `j`*, and there are
`k` values of `j`, so the displayed total should be `k·nk = nk²`, not `nk`.

*Repair (supervisor's, verified).* Fix `l` instead. For fixed `l`, the map
`(x,j) ↦ x + v_j` is a bijection onto the whole periodic set `Π`, so
`#{bad with this l} = #{c' ∈ Π : c' − v_l ∈ A} ≤ n` by `(LC(A,n))` at the point `v_l ∈ Π`.
Summing over the `k` base centres gives `Σ_bad ≤ nk`, which is exactly the claimed constant.
`Σ_rest ≤ 0` still holds because every off-diagonal difference is a difference of two distinct
centres (`|x+v_j−v_l| ≥ 2`) and off `A`. **K15-C003 survives with constant `nk`.** The
strengthening of C002 is therefore real (the price is a count, never an integral), and the only
change needed is the index letter plus one sentence.

## C. C005 — the hybrid score mean, derived from the definition with distant centres

Definition (as recorded): `B_κ(v) = κ Σ_{μ∈Λ} f(v−μ)`. For a periodic packing with `k` centres
per cell of volume `V`, centre density `c = k/V`:

  mean_v B_κ = (κ/V) Σ_j ∫_cell Σ_{x∈L} f(v−x−v_j) dv = (κ/V) Σ_j ∫_{R³} f = κ (k/V) f̂(0)
            = **κ c f̂(0)**.

The unfolding step is exact for `f ∈ L¹` and uses no Voronoi geometry. Hence for `κ > 0`,
`f̂(0) > 0` the mean is **strictly positive**, so C005(ii) ("`mean_v B_κ ≤ 0`") is **refuted** —
the sign is opposite. For FCC at separation 2, `c = 1/(4√2)`, so the mean is
`κ f̂(0)/(4√2)`, i.e. the *same constant* C005(i) quoted as a lower bound for `B_κ(ico)`; the
claimed "opposite signs at the icosahedral cell versus the average" contrast is void.

*Distant centres.* `B_κ(ico) = κ(f(0) + 12f(2))` holds **iff** every centre beyond the first shell
gives `f(v₀−μ) = 0`. The icosahedral cluster's second-shell radius is `2.102924 > 2`
(computed), so the formula is exact only for `f` supported in `B(0, 2.1029)`; for any such `f`,
`f(2)` is a boundary value of the support. For a CE-type `f` (necessarily of unbounded support,
by the bandwidth obstruction) the tail contributes and the 12-term formula is simply not the sum.
Numerically, for `f = e^{-a|x|²}` the contact term is `22%` of the centre term at `a=1` and
`5·10⁻¹⁷` at `a=10` — the formula is not a harmless approximation. **Freeze one score definition
(with the full sum) before any further hybrid obstruction claim.**

## D. Tammes-13: primary source, and the varying-radius reduction with an explicit δ₀

*Closest primary source.* **O. R. Musin and A. V. Tarasov, "The strong thirteen spheres problem",
Discrete Comput. Geom. 48 (2012) 128–141, arXiv:1002.1439v3**: the Tammes problem for `N = 13` is
solved, the optimal arrangement `P13` is unique up to isometry, and
`d₁₃ = ψ(P13) ≈ 57.1367°`. (Their companion `N = 14` paper is arXiv:1410.2536.) The older
`N ≤ 12` cases are Fejes Tóth, Schütte–van der Waerden; Danzer for `N = 10, 11`.

*The reduction audited.* Let `y₁,…,y₁₃` have `|y_i| ∈ [2, 2+δ]` and `|y_i−y_j| ≥ 2`, and project
`y_i' = y_i/|y_i|`. For radii `u,v ∈ [2,2+δ]`,
`|y_i−y_j|² = u²+v²−2uv cos θ ≥ 4` gives `cos θ ≤ (u²+v²−4)/(2uv)`, and this is increasing in
both arguments (at `u=v=s` it equals `1−2/s²`, increasing in `s`), so the worst case is
`u=v=2+δ`:
  **`θ ≥ α(δ) := arccos(1 − 2/(2+δ)²)`.**
At `δ=0`, `α = 60°` — exactly the kissing-number threshold. The contradiction with
Musin–Tarasov arises whenever `α(δ) > d₁₃`, i.e.
  **`δ < δ_max = √(2/(1−cos d₁₃)) − 2`.**
With `d₁₃ = 57.1367°`, `δ_max = 0.091146`; using the conservative upper bound `d₁₃ ≤ 57.14°`,
`δ_max = 0.091035`. So: **`N(ρ) = 12` for `2 ≤ ρ ≤ 2 + 0.0910`**, proved for *every*
2-separated set.

*Status and attribution.* This is an elementary reduction plus an explicit constant; the
mathematical input is Musin–Tarasov's `d₁₃`, and the qualitative version (`δ₀ > 0`) is just the
kissing number. **I claim no novelty** — it converts C013's "no value of `δ₀` extracted here"
into a proved explicit tolerance, which is what E2's `ρ = 2+ε` row needs. The cap bound
`2 arccos(11/13) = 64.41° > 60°` gives nothing (C013's own remark is correct), and the direction
is `θ ≤ 2 arccos(11/13)`, not the reverse.

Also confirmed exactly: the count bound is `n ≤ (3+δ)³ − 1`, so "at most 26" needs
`δ < 28^{1/3} − 3 = 0.036589…`; the rounded `0.0366` is **larger** than the true threshold and
therefore a false statement in `[0.036589, 0.0366)`.

## E. E001–E004 and E2/E3

*E001 (bounded-cluster criterion).* The boundary/absorption step is Hales's Lemma 3.3 with the
per-vertex inequality replaced by a cluster average, and it is sound: saturation gives
`dist(x,Λ) ≤ 2` (else a unit ball fits at `x`), so `Ω(v) ⊆ B(v,2)` and
`∪_{v∈Λ(x,r+1)} Ω(v) ⊆ B(x,r+3)`; Step 3's count `|Λ∩B(y,ρ)| ≤ (ρ+1)³` is valid for all `ρ ≥ 0`
(disjoint unit balls inside `B(y,ρ+1)`); the annulus estimate is `O(r²)` uniformly for `r ≥ 1`
with `D` fixed. **The hypotheses are satisfiable**: covering `R³` by balls `B(y,2)` (possible by
saturation) gives clusters with `diam ≤ 4` and `|K| ≤ 27`. Its worry 1 (partition vs cover) is a
non-issue *provided* `Π` is a genuine partition; worry 4 is also a non-issue (`A` is used only for
non-negativity and in a finite sum, so bounded below suffices). The real content is that the
cluster inequality is *harder* than Hales's per-vertex one for small `D` and *equals Kepler* as
`D → ∞` — E001 changes the hypothesis, not the difficulty.

*E002.* Closed form reproduces `5.5502910285` exactly, and
`√32 − V_dod = 0.106563 > 0`, so no fcc-compatible `A` vanishes identically. **Realisation
question settled YES**: the 13-ball icosahedral cluster is a valid packing (outer mutual distance
`2.102924 > 2`) and every packing is contained in a maximal one, so a saturated packing contains
it. This independently agrees with my `K15-X-C003` (`REGISTRY.md`).

*E003.* Accepted: `K ⊆ K' ⟹ vol_{K'} Ω(v) ≤ vol_K Ω(v)`, so finite computations bound cell
volumes from **above** and cannot certify a cluster-average lower bound; unbounded cells give
`+∞`, which only strengthens the point. E's `8.69`/`12.90` must not be quoted as evidence for E004.

*E004 / E2 / E3.* E004 remains open (no witness found here either). E2: `N(2) = 12` is valid for
every 2-separated set by the kissing number, and now for `2 ≤ ρ ≤ 2+0.0910` by §D; the row must
use `ρ` in that range, and it is tight on FCC/HCP/all Barlow stackings (all are close packings).
E3 is **not audited** in this block (the Hales §2.1 locator and the `x₀ ≈ 2.504` crossing were not
checked); status stays unresolved.

## F. C014 — accepted as invalid, with a provenance gap

The supervisor's local rerun is authoritative and I did not repeat it (heavy solve; offloaded by
policy). Two checks *are* possible without running the optimizer, and both support the review:
the review states the script never passes `M_hat_s` (or its negative) to `linprog`, so **both**
LPs omit Fourier positivity; and the box `|a_k| ≤ 10⁶` means a finite minimiser is not evidence of
an unbounded ray. **Provenance gap:** the artifact set named in the review
(`Computation/Reviews/27616/`, script SHA-256 `b17badbc…`) is **not present** on any of the four
fetched branches, so I could not verify the hash or the artifact contents myself. Recording this
as UNRESOLVED-PROVENANCE rather than accepting it on trust.

## G. X-R01 repair: what was wrong, what is now exact

My previous `ce_laguerre_exact.py` had the two defects the review names, and both are now fixed
in `ce_exact_gauss.py`:

1. **Coefficient field.** The old basis `L_k^{1/2}(2πs)` has coefficients in `Q[π]`; treating them
   as rational was wrong. The new family is
   **`f(x) = P(|x|²)e^{−|x|²}, P ∈ Q[s]`**, all coefficients rational, with the CE threshold
   `|x| ≥ 2` becoming the *rational* half-line `s ≥ 4`.
2. **Fourier map, exactly.** From `(−d/dλ)^n[(π/λ)^{3/2}e^{−π²|t|²/λ}]_{λ=1}` one gets the exact
   linear map `P ↦ Q` with `f̂(t) = π^{3/2}Q(v)e^{−v}`, `v = π²|t|²`, all coefficients rational
   (no `π` anywhere in `P` or `Q`). Verified against independent 3-D radial quadrature to
   `≤ 1.8×10⁻¹⁵`; **the map itself is applied by exact differentiation, so no float residual is
   used as an identity** — the quadrature is only a cross-check.
3. **Sign test.** The old test treated any real root as failure. The new
   `sign_on_half_line` decides `P ≤ 0` on `[4,∞)` and `Q ≥ 0` on `[0,∞)` exactly via
   square-free factorisation plus root isolation: it **accepts even-multiplicity zeros** (as at a
   contact radius) and rejects odd-multiplicity roots, which are exactly the sign changes.
   Demonstrated on `−(s−4)²` (accepted), `−(s−4)` (accepted, zero at the endpoint), `−(s−6)(s−4)²`
   (rejected: `p > 0` on `(4,6)`), `(v−1)²` (accepted), `v−1` (rejected).
4. **Kepler comparison** reduces to `32 P(0)² < π Q(0)²`, decidable with rational enclosures of
   `π`; the bound itself is `(4√π/3)P(0)/Q(0)`.

`x_r01_driver.py` is now a **runnable** driver (LP + cutting planes + exact certification), not a
sketch. Honest result of the in-VM run at degree 6: **the LP is infeasible at iteration 0**
(`evidence` in the run log). Diagnosis: the family has a *fixed* Gaussian width `a = 1`, which is
too rigid — the CE-optimal functions need the width as a free parameter. The correct family is
`P(|x|²)e^{−a|x|²}` with `a ∈ Q_{>0}`; the same λ-differentiation gives a rational map with the
output variable `v = π²|t|²/a` and bound `(4a^{3/2}/(3√π))P(0)/Q(0)`. That extension is the
submitted local request **X-R03**, and until it is run **no 3-D CE number is claimed by X**.

## H. Local execution request — X-R03 (runnable, supersedes X-R01)

```text
request_id            X-R03            (supersedes X-R01, which had a sketch driver)
claim_id              K15-X-C008       (rev. 2)
owner                 X (i-ve-attached-viazovska-f7hh)
independent_reviewer  C (using-the-chats-in-mcl6)
purpose               Certify, or prove infeasible, the ordinary 3-D CE optimum inside the
                      rational family f = P(|x|^2) e^{-a|x|^2}, a in Q_{>0}, P in Q[s],
                      with the exact Fourier map f^(t) = pi^{3/2} Q(v) e^{-v}, v = pi^2|t|^2/a.
                      Output is a THEOREM for all unit-ball packings when the exact sign
                      certificate passes; otherwise no bound is claimed.
repository branch     kepler15/counterexamples/run-01
source commit         <this commit>
tracked paths         KeplerConjecture/Counterexamples/ce_exact_gauss.py
                      KeplerConjecture/Counterexamples/x_r01_driver.py
exact command         cd KeplerConjecture/Counterexamples
                      python3 x_r01_driver.py <DEG> <ITERS>          # to be extended with width a
deps                  python 3.12, sympy 1.14.0, numpy 2.5.3, scipy 1.18.1
resources             < 4 GB RAM, 1 thread, <= 25 min for DEG <= 14
precision             exact rationals in the certificate and in the Fourier map; floats only
                      in the LP search step, which is then discarded unless the exact check passes
parameter bounds      DEG in 4..14 ; a in {1/4,1/2,1,2,4} ; grid 2000 points on [4,120] and
                      [0,400] with cutting-plane refinement, <= 300 rounds
success criterion     (i) exact certificate passes; (ii) result reported as
                      (4 a^{3/2}/(3 sqrt pi)) P0/Q0 with P0,Q0 exact rationals;
                      (iii) sanity: the value must stay ABOVE 2^{-5/2}*4pi/3 = 0.740480489
                      (Li, Thm 6.1), otherwise it is an implementation error, not a theorem
expected outputs      Counterexamples/evidence/x_r03_deg{DEG}_a{a}.json with exact P, Q, P0, Q0,
                      the certification verdict and the Sturm/multiplicity report
certificate format    exact rational coefficient vectors + the multiplicity report; re-checkable
                      by re-running ce_exact_gauss.certify(P)
status                driver runs; degree 6 with fixed a=1 is LP-INFEASIBLE (too rigid) — the
                      width parameter is the missing ingredient, not a bug
next X task while pending: O2 (soft CE non-sharpness from Barlow difference sets) and the
                      distributional form of K15-X-C001.
```

## I. Gaps in this review

* **G1.** `Main/CLAIMS.md` at the current tip (`f9bbb291`, +192 lines) is **not** audited; only
  the `a08f378` version is. Some of Main's repairs may already address items in §A–§C.
* **G2.** C's baseline (`ce3_baseline.py`, `evaluator.py`, `INTERFACE.md`) was read only at the
  level of its normalization claims; the coefficient field, `π` handling, Gaussian scaling, `r0`
  volume factor, rounded coefficients and tail treatment are **NOT yet verified** — that is
  Priority 2 and did not fit in this block. The assignment's warning about `P,Q` versus their
  Gaussian-weighted values stands: C's `audit_min_fhat` / `audit_max_f_on_region` fields are
  polynomials, not function values, and must be relabelled.
* **G3.** C014's artifact set is missing from all fetched branches (provenance).
* **G4.** E3's Hales §2.1 locator not checked.

## J. Next bounded task

Audit C's `evaluator.py` + `ce3_baseline.py` against the frozen contract (coefficient field,
`π`, Gaussian scaling, `r0`, rounded coefficients, full-domain signs, tails) using
`ce_exact_gauss.py`'s exact map as the reference, and reconcile C's `K31/K41` values
(`0.779702445785607`, `0.779745768082807`, both `TESTED_FINITE`) with the published CDS22 CE value
`0.779747`. Then re-audit `CLAIMS.md` at the current tip.
