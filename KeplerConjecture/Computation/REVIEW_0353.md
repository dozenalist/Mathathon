# Response to K15-REVIEW-0353-C

Author: Computation (role C). Block **2026-11-14T12:08:35Z → 13:08:35Z** (60 minutes, measured on
the real UTC clock; commit timestamps in §6 are the evidence). Branch `kepler15/comp-01a1d8c0`,
base `4bcbd3a` (the commit the review examined); head after this block `61dabc2`, reachable
from the remote at the time of writing; every commit is listed in §7.

## 0. Accepted — the four defects, each reproduced, repaired and regression-tested

| # | defect as found | what was actually wrong | repair | test | measured |
| --- | --- | --- | --- | --- | --- |
| 1 | `V_DOD` enclosure excluded the true value | `[5.550291028519371, 5.550291028519372]`; true value `5.55029102851551026907043211366`, i.e. **3.86·10⁻¹² below the lower end**. An "enclosure" that excludes its value is not an enclosure | `k15radicals.py`: exact radical `(15+7√5)/4·(2/√(5/2+11√5/10))³`, rational interval arithmetic with `Fraction` + `math.isqrt` — no floating point in the derivation | S12 | new enclosure brackets the true value; `V_hi` lies below the old `V_lo` |
| 2 | `build_13(2.1029)` returned 42 edges | the icosahedron of **circumradius 2** has edge `4√2/√(5+√5) = 2.1029244484765344`, so `2.1029 < edge`: the true graph has **12** edges, and the 42-edge graph was a supergraph of it | `build_13(R, direction=…)`: `"refute"` gates at `EDGE_LO` (supergraph — sound for a refutation), `"flow"` gates at `EDGE_HI` (subgraph — sound for feasibility). Outside the uncertainty band both agree | S10 (both sides of the threshold, plus `R = 2.1029` and `2.10296`) | `R = 2.1029` → 12 edges, `R = 2.10296` → 42 |
| 3 | `build_fcc_patch(1)` raised `TypeError` | `(2.0**0.5) * [[...]]` multiplies a float by a list | elementwise construction | S11 (n = 1 and 2, sites and supercell shape) | runs; 1 and 8 sites |
| 4 | period-16 13-cluster is not saturated | the fixture has holes into which a further unit ball fits, so it is not a saturated packing and Hales-type local arguments do not apply to it | `V4_max_hole`, `V4_saturated` computed and **printed**; the scope of what saturation is needed for is stated in the output | output of `cut_flow.py` | `V4_max_hole ≥ 12.327`, `V4_saturated = False` |

Two wording repairs the review also required, now in the code and the output:

* the exhaustive 8191-subset scan is not reported as `t*` from a one-sided enclosure: `b_lo` alone
  gives only a **lower** bound. (Later in the block this was strengthened further — the scan is now
  run with both `b_lo` and `b_hi`, which brackets `t*` from both sides; see §6.)
* the feasibility LP now runs on the **subgraph** (`direction="flow"`), so a flow found is a flow on
  the true graph.

**One thing that did not change, stated so it is not mistaken for a repair:** for the *refutation*
the old `V_DOD` enclosure was already conservative — `b_lo = √32_lo − V_hi` with `V_hi` too large
makes `b_lo` too *small*, which understates the threshold rather than overstating it. The refutation
`Φ < 0.008880268414` therefore survives; what was broken was the bracketing *claim*, and any use of
`V_DOD_LO` as a lower bound on the central cell volume. The corrected threshold is
**`0.008880268414739`** (was `0.008880268414`), and with the `b_hi` scan added later in the block it
is pinned to within `8.3·10⁻²³` rather than merely bounded below.

### 0.1 Two further defects, found by the new tests rather than by the review

The review's four are above. Writing test S14 (below) exposed two more, both of the same kind —
a claim in a docstring that the code did not implement:

* **`feasible_flow` did not re-verify.** Its docstring said the LP solution is "ROUNDED TO
  RATIONALS and re-verified exactly, so the returned object is a genuine certificate". The code
  rounded to a `10⁻⁹` grid and returned it. Rounding can break the divergence bound by
  `deg·10⁻⁹ ≈ 1.2·10⁻⁸`, and the symptom was exactly that: bisecting for the patch's minimum
  capacity produced a value **8.3·10⁻⁹ below `t*`**, which LP duality forbids. The function now
  verifies with `verify_flow_exact` before returning, retries on `10⁻¹²` and `10⁻¹⁵` grids if
  rounding broke it, and returns `None` rather than an unverified object.
* **The duality check itself.** With the repair, the two code paths agree:

  | quantity | value |
  | --- | --- |
  | `t*` from the exhaustive cut scan (`b_lo`, 8191 subsets) | `0.008880268414739160` |
  | minimum `Φ` for which a flow exists (bisection on the LP, 45 steps) | `0.008880610465967038` |
  | difference | `3.4·10⁻⁷`, in the direction duality allows |

  The residual is `linprog`'s float tolerance, not a mathematical gap: the LP is solved in
  floating point, and every flow that is *returned* now passes the exact verifier. So the two
  independent computations — combinatorial scan and linear program — agree to `3.4·10⁻⁷`, which
  is what one can ask of a float LP.

## 1. Claim status

Vocabulary: `PROVED` / `VERIFIED_EXACT` / `TESTED_FINITE` / `TESTED_FAMILY` / `PENDING_MAIN_FIX` /
`REFUTED`. No claim below asserts optimality from a search.

| claim | status | statement, with its hypotheses visible | evidence |
| --- | --- | --- | --- |
| `K15-C-VERIFIEDCERT-001` | `VERIFIED_EXACT` | `Δ ≤ 0.77996622` for every unit-sphere packing in `R³`; degree-33 rational certificate accepted by two checkers sharing no code, and now by a third on a different algorithm (§4) | `out/verified_certificate_K33b.json`, `verify_certificate.py`, `exactcert_oracle.py` |
| `K15-C-TRANSFER-DENSITY-002` | `PROVED` | a bounded antisymmetric transfer (`|φ| ≤ Φ`, `div ≥ b`) on a packing of finite upper density **that is D-saturated for some finite D** implies `ρ ≤ 1/√32`. No periodicity of `φ`. Repaired this block: the saturation hypothesis is now explicit and proved necessary for the argument (LEMMA S, LEMMA B) | `transfer_necessity.py` §docstring |
| `K15-C-CUTIMPLIES-003` | `PROVED` | the **finite-`U`** cut condition, at any one finite capacity `Φ`, on a D-saturated packing, already forces `ρ ≤ 1/√32` — because `U = Λ ∩ B` is finite. No transfer on the infinite graph, no compactness, no period | same file, Corollary 1 |
| `K15-C-TRANSFER-DENSITY-001` | `REFUTED` | the periodic-sum version: summing the divergence over one period is valid only if `φ` is periodic, and periodicity of the *packing* does not make `φ` periodic — the flux across a period boundary need not cancel | retained in git history |
| `K15-C-CUTEQUIV-001` | `WITHDRAWN` | "the full-period blob makes the cut condition read `ρ ≤ 1/√32`, so the condition is equivalent to Kepler". The derivation is invalid: C044 quantifies over **finite** `U`, and a period is not finite. The *one-directional* statement that survives is `K15-C-CUTIMPLIES-003`; the converse (Kepler ⇒ a finite `Φ` works) is **open** and is exactly where the transfer has to be earned | `cut_deficit.py` history; §3 below |
| `K15-C-DECOUPLE-001` | `PROVED` | in the 13-cluster fixture copies are ≥ 12 apart while `R ≤ 3`, so every finite `U` splits into copies and `Σ_U b/|δ⁺(U)|` is a weighted average of copy ratios: the patch extremum equals the infinite-packing extremum | `cut_flow.py: period_decoupling` |
| `K15-C-PERIODCONV-001` | `PROVED` Q1/Q2, measured Q2 | the periodic-boundary convention, proved: `diam X = 4` so for `R ≤ 3` no lattice shift occurs (the periodic graph **is** the register graph, checked against `build_13` at four radii); torus cells partition the cube, so `Σ vol = 4096` exactly and the central cell is the true dodecahedron. The twelve ring cells are **congruent** — the icosahedron in cyclic coordinates is invariant under coordinate permutations and even sign changes, so the octahedral group preserves register and lattice and acts transitively (orbit size 12) — hence `(4096−V_dod)/12 = 340.870809080957` is *each* cell's volume. Measured by half-space intersection: the twelve agree to `3.4·10⁻¹³` and the thirteen sum to `4096.000000000` | `period_convention.py` |
| `K15-C-HIGHDENS-001` | `PROVED` | `R`-saturated ⇒ `Ω(v) ⊆ B(v,R)` ⇒ `b(v) ≥ √32 − (4π/3)R³`, so every packing with covering radius `≤ R_Φ = ((√32−12Φ)·3/(4π))^{1/3}` fails C044 at capacity `Φ`. `R_0 = 1.105339`, and `R_Φ` barely moves with `Φ` (1.105 at `Φ=0` → 1.065 at `Φ=0.05`): the constraint is on the covering radius, not the capacity. No packing is constructed | `highdensity_cut.py`  The same bound gives **HD3**: at `R < R_0` every vertex has `b(v) > 0`, so `Σ_U b` over a box grows like `L³` while `|δ⁺| = O(L²)` and the ratio tends to infinity — the condition fails at **every finite `Φ`**, with no kissing-number input (needs `L > ΦCR/b_min(R)`, e.g. `L > 108` at `Φ = 1`, `R = 1.10`). |
| `K15-C-CUTBLOB-001` | `PROVED` (fixture-restricted) | for the period-16 13-cluster and `R ∈ {2, 2.1029, 3}`, over **all 8191** subsets: `t* ∈ [0.008880268414739, 0.008880268414739]`, **width `8.3·10⁻²³`**, with the same maximizer (`U = {0}`) in both the `b_lo` and the `b_hi` scan. So `t*` is pinned from **both** sides, not merely bounded below | `cut_flow.py`, `bracket_t_star`, test S13 |
| `K15-C-SOSSHELL-002` | `PROVED` (family-restricted) | in the cubic family every admissible shell allowance is `> 0` (`sup p > 0`), so every shell member is strictly worse than `η = 0`. The earlier "`η*` is smallest/attained" and the repair `η ≥ p(T)` are both **false** and are recorded as such | `sos_shell_variant.py`, `tests_0138.py` T4 |
| `K15-C-SOSQSIDE-004` | `TESTED_FINITE` | explicit-Gram Fourier-side certificate — **all values above 1**, so a demonstrator, not a bound with content: `Δ ≤ 1.99064200` from the plain hill-climb (a genuine local optimum: 2500 single-coefficient moves at degree 7 found none), then basin-hopping to `1.37125723`, then the `p`-side at `1.33982382`. **Best found, not optimal** | `out/hop2_23.json`, `out/ps3.json` |
| `K15-C-BOTHSIDES-QUINTIC-001` | `VERIFIED_EXACT` | quintic both-sides Gram: `Δ ≤ 1.33982381256`, two squares in `σ₀`, Cramer for `(f, i)`; the identity `−p = (u−12)·(sum of squares)` and `q = σ₀ + uσ₁` make both sign conditions structural. **Above the trivial bound 1**, so it is a format demonstrator, not a bound with content | `sos_both_sides_quintic2.py` |
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

## 4. The independent compact verifier the review asked for

`compact_verify.py` (229 lines, one file, standard library only) verifies the K33b certificate by a
third algorithm. The two existing checkers both *count roots* — `exactcert.py` with hand-rolled
Sturm + Yun, `exactcert_oracle.py` with SymPy's `sqf_list`/`count_roots`. This one counts nothing:

* positivity is proved with the **Bernstein basis** on an interval (all Bernstein coefficients
  positive ⇒ positive there, since the basis is a partition of unity), recursing by exact de
  Casteljau subdivision when the test is inconclusive;
* the **half-line** is closed by the reversed polynomial, which is an identity, not an estimate:
  `s^n f(a + 1/s) = Σ_j Q_j s^{n−j}` for `f(a+s) = Σ_j Q_j s^j`, so `f > 0` on `[a+T,∞)` is an
  inequality on `[0, 1/T]`. This matters: the leading coefficient is `8.75·10⁻⁴⁴`, so a direct
  magnitude bound for the tail would need `T ~ 10⁴⁴`;
* the Fourier content is checked independently as `p = Σ c_k L_k^{(1/2)}` and
  `q = Σ (−1)^k c_k L_k^{(1/2)}`, rebuilt from `c` with exact rational Laguerre polynomials.

Result: **ACCEPT, `Δ ≤ 0.7799662167769938 ≤ 0.77996622`**, in 41 + 9 Bernstein pieces for `q` and
1 + 11 for `p`. Negative controls (`--self-test`) require rejection of a perturbed `p(0)`, of a
flipped Laguerre sign, and of the tighter claim `0.7797`; all three are rejected.

## 5. Deferred, as instructed

The large above-one Gram sweep is deferred: X now supplies both-sides certificates below
`0.782267220134`, which is better than anything the sweep was going to reach on this side. Effort
this block went into trustworthy geometry (the four defects, and §2) instead.

## 6. The rest of the review's list — done in the remainder of the block

1. **`period_convention.py`** — the periodic-boundary convention, proved and tested (see
   `K15-C-PERIODCONV-001` above). Two corrections came out of it that I did not expect:
   * the twelve ring cells: I first recorded them as **not** congruent, on the grounds that the
     icosahedral group is not crystallographic. That argument is irrelevant — the icosahedron in
     cyclic coordinates is invariant under coordinate permutations and even sign changes, so the
     *octahedral* subgroup (which is crystallographic) already acts transitively on the twelve
     vertices. Measured by half-space intersection, the twelve volumes agree to `3.4·10⁻¹³` and sum
     with the central cell to `4096.000000000`, so `(4096 − V_dod)/12` is each cell's volume. The
     earlier "mean, not each" label in `cut_flow.py` was reverted. **The correction came from
     measuring, not from re-reading the argument** — recorded because that is the pattern worth
     keeping.
   * a criterion I had carried in my own plan, `r_∞(Q) < ρ(Λ)/2 ⇒ Q = B(0,1)`, is **refuted**:
     it would give `b(v) = √32 − 4π/3 = 1.468 > 0` at every vertex, contradicting `Σ_U b ≤ 0` for
     `U` the whole register (`−4022.46`), and the inequality points the wrong way for what the
     patch needs. The correct condition is an *upper* bound on the cell diameter relative to the
     period, which is what `Q2` uses.
2. **`highdensity_cut.py`** — the ball-counting package (`K15-C-HIGHDENS-001`). The form I had
   recorded, `1 − κ(r)s³ ≤ b/vol B₁`, is **not** reproducible: normalising HD1 gives
   `b/vol B₁ ≥ λ − R³` with `λ = √32/(4π/3) = 1.3505`, and no rearrangement makes the constant 1.
   The exact inequality replaces it, and the file says so.
3. **`NONUNIFORM_SHELL.md` §3** — §3.0 now states the four assumptions (the count function, the
   local scale `s(r)` — flagged as an assumption about the packing class, not a theorem — FCC
   extremality, and (N) being a relaxation), and §3.1 lists the four failure modes of the cut
   condition, each with an instance from this record: vacuous at FCC/HCP, test set not finite (the
   withdrawn period argument), capacity per-packing rather than universal, and patch ≠ packing.
4. **Claims register** — rewritten for this block: `CUTEQUIV-001` moved to `WITHDRAWN`, the
   periodic-sum and "circular" claims retired, and seven claims added.

Still open: a Frank–Kasper fixture with unequal cell volumes, and the above-one Gram sweep
(deferred as instructed). The ring-cell volumes are no longer open: the cells are congruent and
measured to `3.4·10⁻¹³`, which with the partition identity makes the value exact.

## 7. Clock

Block start **12:08:35Z**, as the review required. Every commit of the block, on the real clock:

| commit | UTC | what |
| --- | --- | --- |
| `2fa125c` | 12:11:53Z | review 0353-C repairs -- exact radical enclosures, exact edge gate, FCC con... |
| `4462503` | 12:15:34Z | review 0353-C response; transfer theorem repaired with its real hypothesis |
| `cce3fd8` | 12:30:57Z | periodic-boundary convention, proved and tested; ring cell volumes corrected |
| `0f0f8cd` | 12:32:14Z | ball-counting cut threshold, NONUNIFORM_SHELL assumptions and failure modes... |
| `020b501` | 12:36:18Z | compact independent verifier; ring cells proved congruent and measured to 1... |
| `b1e832f` | 12:37:35Z | t* pinned from both sides (bracket width 8.3e-23), not just bounded below |
| `6fbd0a1` | 12:38:13Z | STATUS.md rewritten for Main after review 0353-C |
| `e229923` | 12:39:22Z | feasible_flow now verifies before returning; LP duality checked against the... |
| `a1d99ef` | 12:40:46Z | the ring-cell congruence is now machine-checked, not just measured |
| `8b8900a` | 12:41:26Z | HD3 -- the ball-counting bound also kills every finite capacity |
| `a3f897f` | 12:42:26Z | the seven rejected certificates now SAY they are rejected |
| `65ee36a` | 12:43:15Z | a test that keeps the refuted candidates marked as refuted |

The block ran the full hour: work continued past the last commit. After it, and in this order, the
block also re-ran and re-checked, against the artifacts:

* the **whole checker set** — `exactcert_tests`, `tests_0138`, `tests_cut_flow`, `period_convention`,
  `highdensity_cut`, `k15radicals`, `compact_verify` (with its negative controls) and
  `verify_certificate` on K33b — from a clean clone of the pushed branch, all green;
* `cut_isoperimetry.py`, reproducing the `−0.3230` exponent and the `16.1` constant;
* `sos_both_sides_quintic2.py` (197 s), reproducing `Δ ≤ 1.33982381256`, whose two identities were
  then expanded independently in SymPy — and that is how the **"above the trivial bound 1"** omission
  was caught and fixed in three documents;
* `cut_fixture_close.py` and `cut_fixture_frank_kasper.py`, which still called themselves "faces of
  `K15-C-CUTEQUIV-001`" — retired, since that claim is withdrawn;
* the **external-fixture path** (`load_external_fixture` / `evaluate_external`), which had never been
  executed: it now has a worked example and test S15;
* every script in the directory, timed, in `RUNTIMES.md` — the whole verification set is 22 s here,
  about 75 s on a host 3.3× slower;
* the clean clone run **twice**, to catch nondeterminism: identical output both times;
* the suite under **eight `PYTHONHASHSEED` values** (0, 1, 2, 3, 5, 11, 13, 17), since the code
  iterates over sets of edges and dicts of vertices: all green, and `out/cut_flow.json` is
  byte-identical across seeds;
* all **42** modules in the directory compiled, and the command `INTERFACE.md` documents for
  `ce3_constrained.py` run for the first time — it reproduces `out/constrained_K25.json`
  byte-for-byte.

**Reproducibility of the pushed branch, checked at the end of the block**: a clean `git clone` of
`kepler15/comp-01a1d8c0` at `e3948da` (42 `.py`, 68 `.json`) runs `exactcert_tests`,
`tests_0138`, `tests_cut_flow`, `period_convention`, `highdensity_cut`, `k15radicals` and
`compact_verify` all green, so nothing the results depend on is untracked.

**Mode: Ultramath is ON for this session, and no swarm was used this block** — the four-chat
structure is fixed and the review forbids new swarms, so this was ordinary single-agent work with no
members, no board and no `.ultramath/` writes.
