# Response to K15-REVIEW-0353-C

Author: Computation (role C). Block **2026-11-14T12:08:35Z → 13:08:35Z** (60 minutes, measured on
the real UTC clock; commit timestamps in §6 are the evidence). Branch `kepler15/comp-01a1d8c0`,
base `4bcbd3a` (the commit the review examined), head after this block in §6.

## 0. Accepted — the four defects, each reproduced, repaired and regression-tested

| # | defect as found | what was actually wrong | repair | test | measured |
| --- | --- | --- | --- | --- | --- |
| 1 | `V_DOD` enclosure excluded the true value | `[5.550291028519371, 5.550291028519372]`; true value `5.55029102851551026907043211366`, i.e. **3.9·10⁻¹² below the lower end**. An "enclosure" that excludes its value is not an enclosure | `k15radicals.py`: exact radical `(15+7√5)/4·(2/√(5/2+11√5/10))³`, rational interval arithmetic with `Fraction` + `math.isqrt` — no floating point in the derivation | S12 | new enclosure brackets the true value; `V_hi` lies below the old `V_lo` |
| 2 | `build_13(2.1029)` returned 42 edges | the icosahedron of **circumradius 2** has edge `4√2/√(5+√5) = 2.1029244484765344`, so `2.1029 < edge`: the true graph has **12** edges, and the 42-edge graph was a supergraph of it | `build_13(R, direction=…)`: `"refute"` gates at `EDGE_LO` (supergraph — sound for a refutation), `"flow"` gates at `EDGE_HI` (subgraph — sound for feasibility). Outside the uncertainty band both agree | S10 (both sides of the threshold, plus `R = 2.1029` and `2.10296`) | `R = 2.1029` → 12 edges, `R = 2.10296` → 42 |
| 3 | `build_fcc_patch(1)` raised `TypeError` | `(2.0**0.5) * [[...]]` multiplies a float by a list | elementwise construction | S11 (n = 1 and 2, sites and supercell shape) | runs; 1 and 8 sites |
| 4 | period-16 13-cluster is not saturated | the fixture has holes into which a further unit ball fits, so it is not a saturated packing and Hales-type local arguments do not apply to it | `V4_max_hole`, `V4_saturated` computed and **printed**; the scope of what saturation is needed for is stated in the output | output of `cut_flow.py` | `V4_max_hole ≥ 12.327`, `V4_saturated = False` |

Two wording repairs the review also required, now in the code and the output:

* the exhaustive 8191-subset scan is reported as a **CERTIFIED LOWER BOUND on `t*`** (`b_lo` gives a
  lower bound; equality with the irrational optimum would need interval arithmetic on both sides),
  not as `t*` itself;
* the feasibility LP now runs on the **subgraph** (`direction="flow"`), so a flow found is a flow on
  the true graph.

**One thing that did not change, stated so it is not mistaken for a repair:** for the *refutation*
the old `V_DOD` enclosure was already conservative — `b_lo = √32_lo − V_hi` with `V_hi` too large
makes `b_lo` too *small*, which understates the threshold rather than overstating it. The refutation
`Φ < 0.008880268414` therefore survives; what was broken was the bracketing *claim*, and any use of
`V_DOD_LO` as a lower bound on the central cell volume. The corrected threshold is
**`0.008880268414739`** (was `0.008880268414`), and it is still a lower bound.

## 1. Claim status

Vocabulary: `PROVED` / `VERIFIED_EXACT` / `TESTED_FINITE` / `TESTED_FAMILY` / `PENDING_MAIN_FIX` /
`REFUTED`. No claim below asserts optimality from a search.

| claim | status | statement, with its hypotheses visible | evidence |
| --- | --- | --- | --- |
| `K15-C-VERIFIEDCERT-001` | `VERIFIED_EXACT` | `Δ ≤ 0.77996622` for every unit-sphere packing in `R³`; degree-33 rational certificate accepted by two checkers sharing no code | `out/verified_certificate_K33b.json`, `verify_certificate.py`, `exactcert_oracle.py` |
| `K15-C-TRANSFER-DENSITY-002` | `PROVED` | a bounded antisymmetric transfer (`|φ| ≤ Φ`, `div ≥ b`) on a packing of finite upper density **that is D-saturated for some finite D** implies `ρ ≤ 1/√32`. No periodicity of `φ`. Repaired this block: the saturation hypothesis is now explicit and proved necessary for the argument (LEMMA S, LEMMA B) | `transfer_necessity.py` §docstring |
| `K15-C-CUTIMPLIES-003` | `PROVED` | the **finite-`U`** cut condition, at any one finite capacity `Φ`, on a D-saturated packing, already forces `ρ ≤ 1/√32` — because `U = Λ ∩ B` is finite. No transfer on the infinite graph, no compactness, no period | same file, Corollary 1 |
| `K15-C-TRANSFER-DENSITY-001` | `REFUTED` | the periodic-sum version: summing the divergence over one period is valid only if `φ` is periodic, and periodicity of the *packing* does not make `φ` periodic — the flux across a period boundary need not cancel | retained in git history |
| `K15-C-CUTEQUIV-001` | `WITHDRAWN` | "the full-period blob makes the cut condition read `ρ ≤ 1/√32`, so the condition is equivalent to Kepler". The derivation is invalid: C044 quantifies over **finite** `U`, and a period is not finite. The *one-directional* statement that survives is `K15-C-CUTIMPLIES-003`; the converse (Kepler ⇒ a finite `Φ` works) is **open** and is exactly where the transfer has to be earned | `cut_deficit.py` history; §3 below |
| `K15-C-DECOUPLE-001` | `PROVED` | in the 13-cluster fixture copies are ≥ 12 apart while `R ≤ 3`, so every finite `U` splits into copies and `Σ_U b/|δ⁺(U)|` is a weighted average of copy ratios: the patch extremum equals the infinite-packing extremum | `cut_flow.py: period_decoupling` |
| `K15-C-CUTBLOB-001` | `PROVED` (fixture-restricted) | for the period-16 13-cluster and `R ∈ {2, 2.1029, 3}`: `max_U Σ_U b/|δ⁺(U)| ≥ 0.008880268414739`, attained at the singleton, over **all 8191** subsets. A lower bound on `t*`, and a constraint on any `Φ` that must serve every packing — **not** a refutation of the transfer route | `cut_flow.py`, output row `R = 2` |
| `K15-C-SOSSHELL-002` | `PROVED` (family-restricted) | in the cubic family every admissible shell allowance is `> 0` (`sup p > 0`), so every shell member is strictly worse than `η = 0`. The earlier "`η*` is smallest/attained" and the repair `η ≥ p(T)` are both **false** and are recorded as such | `sos_shell_variant.py`, `tests_0138.py` T4 |
| `K15-C-SOSQSIDE-004` | `TESTED_FINITE` | explicit-Gram Fourier-side certificate `Δ ≤ 1.99064200` from the plain hill-climb (a genuine local optimum: 2500 single-coefficient moves at degree 7 found none), then basin-hopping to `1.37125723`, then the `p`-side at `1.33982382`. **Best found, not optimal** | `out/hop2_23.json`, `out/ps3.json` |
| `K15-C-BOTHSIDES-QUINTIC-001` | `VERIFIED_EXACT` | quintic both-sides Gram: `Δ ≤ 1.33982381256`, two squares in `σ₀`, Cramer for `(f, i)`; accepted by `exactcert` | `sos_both_sides_quintic2.py` |
| `K15-C-ISOPERIM-001` | `TESTED_FINITE` | FCC kissing-graph profile `|δ⁺U|/|U|` has exponent `−0.3230 ≈ −1/3` and `|δ⁺|/|U|^{2/3} → 16.1`, on one complex. A mechanism for the open perimeter lemma, not a proof of it | `cut_isoperimetry.py` |

## 2. The theorem this block had to repair (found while writing the table above)

`transfer_necessity.py` asserted

> `Σ_{v∈B} vol Ω(v) = |B| + O(L²)` **because the cells tile space**

and that is not a consequence of tiling. Counterexample: FCC in a half-space, empty above it. For a
box in the void, `Λ ∩ B = ∅`, so the sum is `0` while `|B| = L³`. The cells of an unbounded void
have unbounded diameter, and their volume is what breaks the identity.

The repair keeps the review's large-box averaging and adds the hypothesis the passage actually uses:

* **LEMMA S.** "every point is within `D` of a centre" ⟺ "`diam Ω(v) ≤ D` for every `v`".
* **LEMMA B.** For a `D`-saturated packing, `|B| − O_D(L²) ≤ Σ_{v∈Λ∩B} vol Ω(v) ≤ |B| + O_D(L²)`.
  Upper: each cell of a centre in `B` lies in `B` grown by `D`. Lower: a point of `B` further than
  `D` from `∂B` is within `D` of some centre, and that centre must lie in `B`.
* **THEOREM A.** finite upper density + `D`-saturation + bounded transfer ⇒ `ρ ≤ 1/√32`.

Why this costs nothing in the cases that matter: saturating a packing only raises its density, and a
saturated packing has `D = 2`. It does **not** cover the sparse period-16 13-cluster (cells of
diameter ≥ 12.3), and it does not need to — there `ρ = 0.0032` and the cut/flow work is a
*refutation of a capacity*, not a density bound. Flagged as a scope limit in the JSON
(`does_not_apply_to`). Whether THEOREM A holds without `D`-saturation is left **open**; nothing
below depends on the answer.

## 3. What replaced the withdrawn equivalence

`K15-C-CUTEQUIV-001` claimed the cut condition is *equivalent* to Kepler. Both halves needed
separating, and only one survives:

* **Cut ⇒ density bound: proved** (`K15-C-CUTIMPLIES-003`). Take `U = Λ ∩ B`. `U` is finite because
  the packing has finite density, so C044's criterion applies to it verbatim, and the averaging of
  §2 gives `√32ρ − 1 ≤ 0`. No period, no compactness, no transfer on the infinite graph.
* **Density bound ⇒ cut at a finite `Φ`: open.** This is the direction that would need a
  Hoffman-type transfer to exist, and it is the whole difficulty.

A consequence worth recording: since *any* finite `Φ` suffices for the first direction, C044's
content is not in the size of `Φ` but in whether a finite `Φ` can be exhibited at all. That is the
precise sense in which "exhibiting a bounded transfer is strictly stronger than the density bound".

## 4. Deferred, as instructed

The large above-one Gram sweep is deferred: X now supplies both-sides certificates below
`0.782267220134`, which is better than anything the sweep was going to reach on this side. Effort
this block went into trustworthy geometry (the four defects, and §2) instead.

## 5. Still open at the end of this block

1. `period_convention.py` — the periodic-boundary convention for the 13-cluster (`16Z³`), and the
   derivation `r_∞(Q) < ρ(Λ)/2 ⇒ Q = B(0,1)`.
2. `highdensity_cut.py` — the ball-counting violation package.
3. `NONUNIFORM_SHELL.md` §3 — the assumption paragraph and the four failure modes.
4. The claims register update (`CLAIM_REGISTER.md` predates this block).

## 6. Clock

| event | UTC |
| --- | --- |
| block start (as required by the review) | 2026-11-14T12:08:35Z |
| first commit of this block (`2fa125c`, the four repairs) | see `git log --format=%cI 2fa125c` |
END_OF_BLOCK_STAMP
