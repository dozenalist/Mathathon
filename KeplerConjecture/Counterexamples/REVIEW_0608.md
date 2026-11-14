# K15-REVIEW-0608-X — the twist certificate is unsound in both revisions; E's cell certifier is unsound in two ways

Receipt `2026-11-14T14:20:31Z`. Audited, with exact blobs:

| object | blob | where |
| --- | --- | --- |
| `Computation/twist_cover.py` (K15-C112, "inflated arcs") | `469fc9f181f976598fd866d9d6473527d4e4a6f8` | main `8dc264e` |
| `Computation/twist_cover.py` (K15-C123, "rigorous inner arcs") | `67d5c97345cbdb049461b1ea8c50d743b0bf58f1` | main `6d542f5` |
| `Experimental/scripts/rigorous_cell_volume.py` | `d015a2e1e322853286322ff2c6ec4a5a88f03550` | experimental `d289bef` |

Witnesses: `Counterexamples/Reviews/twist/audit_twist_cover.py`, `.../audit_E_cell_volume.py`, and the
replacement certificate `.../corrected_cover.py`. All run in under two seconds.

**Verdict.** `twist_cover.py` is unsound in **both** revisions, for two independent reasons, and the
C123 rewrite fixed the rounding direction while leaving both reasons in place. The *theorem* it is
meant to certify — two adjacent dodecahedral cells are impossible at centre distance 2 — is true,
and is now certified by a corrected cover with a two-degree margin. E's `rigorous_cell_volume.py`
is exact in its polytope machinery and unsound in its enclosure: a componentwise error is used
where the Euclidean norm is needed, and an unbounded cell receives a finite "certified" volume.

---

## 1. `twist_cover.py`: the constant term (both revisions)

The distance between v's contact `a` and w's contact `R_t q` (w's frame), with `u = w − a` and the
twist about the v–w axis (the `x`-axis here), is

```
d²(t) = |u|² + |q|² + 2 u_x q_x + 2(u_y q_y + u_z q_z) cos t + 2(u_z q_y − u_y q_z) sin t .
```

Both revisions compute `A = (u_x²+u_y²+u_z²) + (q_x²+q_y²+q_z²)` and drop `2 u_x q_x`
(`twist_cover.py:70` in both blobs). The term is **nonzero for all 121 pairs** (`u_x = a_x − 2 ≤ 0`,
`q_x ∈ [−2,2]`), and its omission is not conservative: for `q_x > 0` it makes `A` too large, so the
code under-estimates the clash. **Exact unsafe witness**, reproduced on both blobs: a pair with the
code's `A = 8.422291236` and the true `A = 6.444582472`, at twist `t = 10.3°` —
code `d² = 4.0006` (safe, the certificate would allow this twist) versus true `d² = 2.0229`
(a clash). The direct recomputation `|a − w − R_t q|² = 2.0229` agrees with the corrected constant,
not with the code's.

## 2. `twist_cover.py`: the arc is the complement of the clash set (both revisions)

`{t : cos(t − ψ) < c}` is the arc **centred at `ψ + π` with half-width `π − acos(c)`**. Both
revisions write `[ψ − h, ψ + h]` with `h = acos(c)` (lines 81–83 of the C123 blob), which is the set
where `cos(t − ψ) > c` — the **far** set. So the union covers the circle exactly where the pairs are
*apart*.

That is not a near-miss: over the 121 pairs the code's `c = (4 − A)/R` never exceeds `−0.381966`
(so `acos(c) ≥ 112.46°` and the true clash half-width is at most `67.54°`), and **every one of the 50
emitted arcs is centred where `d² = 16.8`** — the far point of that sinusoid. C123's docstring
asserts "the arcs used are subsets of the true violation sets"; the measurement says they are
subsets of the complements, 50 out of 50.

**Consequence.** The certificate is vacuous as a proof: it covers the circle with sets on which the
configuration is *safe*. `run_all_checks.py:30` runs it as a passing check, and `ACCEPTED.md:28–29`
records `C112` as `PROVED` and `σ₀ > 2V_dod` as `PROVED modulo ... C112`.

## 3. The replacement: a corrected cover that does work

`Reviews/twist/corrected_cover.py` rebuilds the cover with both defects fixed (`A` including
`2u_x q_x`; arcs centred at `ψ+π` with half-width `π−acos c`; inner shrink by `1e-30`). Result:

```
45 raw arcs from the 121 pairs, merging to ONE interval  [0°, 72°]  — full coverage of the
twist circle (period 2π/5), no gaps.
```

It is validated three ways in `audit_twist_cover.py` and in the run itself: (i) all 25
non-degenerate corrected arcs contain only twists with `d² < 4` and their `±1%` enlargements do not
(0 disagreements in 175 samples); (ii) the cover survives shrinking every arc by **2°**, so the
certificate has a two-degree margin — far more than any rounding error at 60 digits; (iii) the
sampled maximum of the minimum distance over the twist is `1.125554845 < 2`, consistent with the
cover.

**The cover is complete**, which is worth one paragraph because a reader will ask whether the
`11 × 11` pairs are all that can clash. The other four families are twist-independently safe:
`w` to `v`'s ring is the icosahedron edge `2.102924448 ≥ 2`; within either ring the twist is a
rotation, so distances are preserved and the same `2.102924448` is the minimum; the shared pair is
the contact, exactly 2; and `v` to `w`'s ring has `|w + R_t q|² = 8 + 4q_x ≥ 8 − 4(2/√5) = 4.4223`,
i.e. distance `≥ 2.102924448` for **every** twist (the `q_x = −2` antipode is the excluded contact).
So only the 121 cross pairs can clash, and the cover over them settles all twists.

**And the one-parameter family is everything.** Fixing v's cell so that the shared contact is `+x`
leaves w's cell determined by a rotation `R` with `R u = −u₀` for some icosahedral direction `u`;
the remaining freedom is `R_t · A₀` with `R_t` the rotation about the v–w axis, period `2π/5`.
Choosing a different `u` gives `A₀·g` for an icosahedral symmetry `g`, which permutes the standard
set, so it produces no new configuration. The twist circle is therefore the complete moduli space
for a pair of dodecahedral cells at a contact.

**Precision.** The cover is not a 60-digit artefact: it holds identically at `mp.dps = 30`, `60` and
`100`, and it survives shrinking every arc by `2°` — four orders of magnitude more margin than the
`1e-30` inflation at 60 digits.

So the theorem is true and certified: **for every relative twist, some pair of the two eleven-point
sets is strictly closer than 2, hence two regular dodecahedral cells of inradius 1 cannot have
centres at distance exactly 2.** That restores `C108` step (4) — as `X-C058`, replacing `C112` and
`C123` as the load-bearing certificate.

**And it certifies the threshold, not just the endpoint.** Running the same corrected cover with the
partner centre at `d·u₀` (`Reviews/twist/certified_threshold.py`) gives a cover for every
`d < d_c` and a failure just above, with

```
covered at d = 3.455,  fails at d = 3.456,  bisection:  d_c ∈ [3.455500344, 3.455500344]
```

matching `X-C051`'s sampled `3.455500344` to nine decimals. So `C116`'s `6/√5 = 2.6832816` is
replaced by a *certified* `3.455500344`, 28.8% larger, with the same one-line repair of the arcs.

## 4. The failure is the certificate, not the theorem — and `C116` inherits the defect

`near_contact_band.py:43` uses `twist_cover.inner_arcs` to compute the near-contact band, so
**`C116`'s `6/√5 = 2.6832816` inherits both defects** and is unproved by that method. The
*statement* is nonetheless true and can be strengthened: `X-C051` computes the two-dodecahedra
threshold directly (same configuration, no arcs) as `3.4555003`, attained with no other centre
cutting either cell. Since `3.4555003 > 6/√5`, impossibility below `6/√5` follows — but from that
computation, not from `C116`'s arc cover. `C116`'s own sharpness caveat ("sharpness is for this
certificate") should now read: the certificate is invalid, and the true threshold is `3.4555003`.

## 5. E's `rigorous_cell_volume.py`: two defects, both exact

**V1 — norm choice.** The slack for the perturbed normal is computed componentwise
(`rigorous_cell_volume.py`, `e = max((x.hi − x.lo)/2 for x in n)`) and then used as
`slacks.append(R * eq + fq)`. The inclusion `{y·n' ≤ b' − slack} ⊆ Ω` needs `|y·(n − n')| ≤ R‖n − n'‖₂`,
and `‖·‖₂` can exceed `‖·‖_∞` by `√3`. Exact witness (rational, `R = 1`): `n₀ = (1,0,0)`,
`n = (3/5,4/5,0)`, so `‖n − n₀‖_∞ = 4/5` but `‖n − n₀‖₂ = 0.894427`; with `y = (−4/9,8/9,0)`
(so `|y| = 0.993808 ≤ 1`) we get `y·(n − n₀) = 8/9 = 0.888889 > 4/5`. The allowance is smaller than
the perturbation it must absorb, so the "inner" polytope need not lie inside the cell.

**V2 — boundedness.** `polytope_volume` accepts any body with at least four feasible triple-plane
vertices and never tests boundedness; `sandwich`'s `R`-check inspects only the vertices it found, so
an unbounded body passes it vacuously. Exact witness: centres `(±2,0,0)`, `(0,±2,0)`, `(0,0,−2)`
give the cell `{|x| ≤ 1, |y| ≤ 1, z ≥ −1}`, which has the recession ray `(0,0,1)` and **infinite
volume**; E's `sandwich(centres, R=2)` returns `[1.3333333333333333, 1.3333333333333333]` — a finite
*certified* enclosure of an infinite set.

**What is exact and does work.** The rational polytope machinery is sound: the cube (`8`) and the
regular tetrahedron (`8/3`) self-tests pass, and the fcc control encloses `4√2` at
`[5.656854249492, 5.656854249492]`. The defect is in the enclosure argument, not the arithmetic.

**The repair is cheap, and I implemented it to be sure.** `Reviews/twist/repaired_sandwich.py`
makes the two changes and nothing else — slack `R·√3·(e + QERR) + f + QERR`, and the box
`|y_i| ≤ R` on both polytopes — and the fcc control still closes, at width `1.4·10⁻¹⁸`, for
`R = 2, 3, 4`. So the norm fix costs nothing numerically.

**But the box alone does not detect unboundedness**, and that is worth stating because it is
tempting to think it does: on the `{|x|≤1, |y|≤1, z≥−1}` witness the boxed version returns
`[12.000000, 12.000000]` — finite, and *not* the cell's volume, because the box cut it. What
detects it is a **saturation check**: if `Ω(w) ⊆ B(w,2)` is to be used, every point of the outer
polytope must be within 2 of some centre, and on that witness **4 of the 8 outer vertices fail the
test**. So requirement (1) below is really "boundedness *plus* the covering check that licenses
`R = 2`", not "add a box".

**What a repair must do** (the five requirements, in the order they bind):

1. **boundedness** — prove it, don't inherit it: impose `|y| ≤ R` as a *constraint* in both
   polytopes **and** check the covering hypothesis that licenses `R` (every outer vertex within 2 of
   some centre). The box alone is not enough — it makes the polytope bounded but returns the volume
   of `Ω ∩ box`, which is `12.0` on the witness above;
2. **norm choice** — slack `R‖n − n'‖₂`, or renormalise so that `‖n − n'‖₂ ≤ √3 max|·|` is paid for;
3. **radius bootstrap** — `R` must be an a-priori bound (`R = 2` follows from `Ω(w) ⊆ B(w,2)`
   independently of any enumeration), not a property checked against the vertices that were found;
4. **inner inclusion** — with (1)–(3) the two-sided inclusion is valid; the lower bound must fall
   back to `0` when the inner polytope is empty (the code does this ✓);
5. **domain coverage** — bounding one cell of one configuration is not bounding a family; the
   branch-and-bound must cover the parameter domain exactly, boundary included.

**What in E's chain is sound.** Checked separately, so the audit does not overstate: the
sin/cos interval extension `range_of` (hull of corner values plus the quarter-turn points inside
the box) contains the true range — 504 samples over 12 random boxes, 0 outside; and the rational
polytope machinery is exact (cube `8`, tetrahedron `8/3`, fcc `4√2`). The failures are the two
enclosure steps and the grid, not the arithmetic.

**Requirement 5 also fails, in `certify_region.py` itself.** The box grid is
`n = int(round((hi − lo)/w))` followed by `n` boxes at `lo + i·w`, and nothing checks the
remainder: a region `[110°, 111.05°]` at `w = 0.1°` is covered only to `111°` (**a 0.05° gap**), and
`[110°, 111°]` at `w = 0.3°` only to `110.9°` (**0.1° gap**) — while the program still prints
"CERTIFIED for the whole region". The default region `[110,111] × [35,36]` at `0.1°` happens to be
an exact multiple, so *that* run is unaffected; any other region is not, and the fix is one line
(require `(hi − lo)/w` integral, or add the remainder box).

## 6. What survives in `C106`–`C108`, and the slack scope

- **`C106`** (the Theorem B bridge and the `1.92%` gap): unaffected by the twist defect — it is the
  mass/matching argument. **But it is one of three files carrying the §4 slack display**
  (`CLAIMS.md`, `GEOMETRIC_LEMMA_0438.md`, `PROOF_GAPS.md`), and that display is true only under the
  reading where the exceptional set is absorbed into the slack (`E = ∅`, differences
  `−(√32−V_dod)Σd_v − V_dod C_R' ≤ 0`) and **false** if a non-empty `E` is kept alongside `d` (the
  `R = 0` witness of `X-C042`). All three should state `E = ∅` or use the derived form
  `√32(|B|−|E_B|) − (√32−V_dod)(Σd_v + C_R')`.
- **`C107`** (the monotone reduction): independent of both defects ✓.
- **`C108`** (Theorems D and C): Theorem C is independent ✓; **Theorem D's step 4 depended on
  `C112`, so as recorded it does not stand** — it is restored by the corrected cover (`X-C057`), and
  `ACCEPTED.md`'s "`PROVED` modulo ML's equality case and `C112`" should read "modulo ML's equality
  case and the corrected cover `X-C057`".
- **The uniqueness claim is not propagated.** The thirteen-cluster is *a* failing configuration for
  `(M)`, not the only one, and the twelve-point set at distance ≥ 2 on radius 2 is
  positive-dimensional (`X-C048`) — nothing in this review rests on either uniqueness.

## 7. The 13–20-face route: no obstruction, but the constant it needs is a *conjecture*

`C122` asks for a bound (B_F): a convex body containing the unit ball, with at most `F` faces all at
distance `≥ ρ`, has volume `≥ c_F ρ³`, and the isolated-vertex argument needs
`c_F > √32/1.045³ = 4.957082168`.

- **No obstruction exists for `F ≤ 20`.** The best 20-faced constant is `V_ico = 5.054056144`, and
  `V_ico·1.045³ = 5.767517665 > 5.656854249 = √32` — a **1.96% margin**. So if the 20-faced
  optimum is the icosahedron, the whole 13–20-face range is settled, with the dodecahedron's
  `11.97%` at `F = 12` and the icosahedron's `1.96%` at `F = 20` bracketing it.
- **But that constant is not proved.** Lindelöf's theorem constrains the *shape* of an optimal
  circumscribed polyhedron (all faces tangent, at their centroids); the *optimality* of the
  icosahedron among 20-faced bodies is classical *conjecture* with strong numerical support
  (Goldberg's optimised geometries, Mutoh's computer-aided search for `4 ≤ n ≤ 30`), and Fejes Tóth's
  proof covers only `n = 4, 5, 6, 12` — the same `≤ 12` boundary as the dodecahedral theorem itself.
  So `(B_20)` with `c_20 = V_ico` is **conditional on an unproved classical conjecture**, and the
  honest statement of the 13–20-face route is: *it closes if the icosahedron is the 20-face
  optimum, and the margin it would have is 1.96%.*
- **The route does fail for large `F`**: `4π/3 = 4.188790 < 4.957082`, so no ball-like bound can
  work beyond the crossover; the exact crossover needs the `n`-face optima, which are unknown.

So the answer to "give an explicit near-contact obstruction" is: none for `F ≤ 20`, and the
obstruction for large `F` is the ball itself (`4π/3`). What the route actually needs is not an
obstruction but the `n`-face optimality for `13 ≤ n ≤ 20`.

## 7.1 The other fallback (already done)

The general bounded-interval sign method was addressed in the previous block (`X-C046`: the
Vincent–Descartes decider, 92 cases, 0 mismatches, and the `nsimplify` defect it found in
`exact_sign.py`).

## 8. Status changes asked for

| id | claim | verdict |
| --- | --- | --- |
| `X-C057` | `twist_cover.py` is unsound in both revisions: missing `2u_x q_x` (121/121 pairs; unsafe witness at `t = 10.3°`, code `d² = 4.0006` vs true `2.0229`) and arcs on the far set (50/50 emitted arcs centred at `d² = 16.8`) | **REFUTED (certificate)**; `audit_twist_cover.py` |
| `X-C058` | the two-dodecahedra theorem at distance 2 is **true**, and the corrected cover certifies it: 45 arcs, one merged interval `[0°,72°]`, margin 2° | **PROVED (modulo 60-digit interval arithmetic)**; `corrected_cover.py` |
| `X-C059` | `C116`'s `6/√5` inherits both defects via `near_contact_band.py:43`; the statement is true but the true threshold is `3.4555003` (`X-C051`) | **certificate unsound, statement true** |
| `X-C060` | E's `rigorous_cell_volume.py`: componentwise error used as Euclidean (exact rational witness `y·(n−n₀) = 8/9 > 4/5`, `R = 1`) | **DEFECT (unsound inner inclusion)** |
| `X-C061` | E's `rigorous_cell_volume.py`: unbounded cell returns a finite enclosure (`[4/3, 4/3]` for `{|x|≤1,|y|≤1,z≥−1}`) | **DEFECT (false upper bound)** |
| `X-C062` | the §4 slack display still appears in three `main` files and is true only with `E = ∅` | **scope correction** |

## 8.1 C's near-contact scan: independent of the arc machinery, and honestly labelled

`nearcontact_scan.py` at comp `cde39fa` imports `fixture_nonuniform` and `cut_flow` — **not**
`twist_cover` — so it does not inherit `X-C057`. Its output (`out/nearcontact_scan.json`, tip
`bf7998c`): **500 instances, `with_positive_t_star: 0`, every `t_star` exactly `0`**, density range
`[0.620562, 0.739247]` — all below Kepler. The scan is exhaustive over the `2^4` subsets of a
four-site patch with exact rational cell volumes, so `t* = 0` is exact *for those fixtures*; the
docstring's own caveat ("evidence about the geometry of the near-contact regime, not a theorem about
all packings") is the right scope, and I am not upgrading it. Note the interaction with `X-C044`'s
D7: `exhaustive_cut_scan` omits the theorem's `max(0,·)`, so a `t_star` of exactly `0` across all
500 means some cut attains `Σ_U b = 0` exactly (otherwise the raw maximum would be negative); the
JSON is then right either way, but the two conventions should not be mixed.

**And C's exact volume engine checks out on its own data.** Over the 500 rows, the four cell
volumes satisfy the tiling identity for their own family: `Σvol = a³` exactly in the 488 cubic rows,
and `Σvol = a³·t` in the 12 tetragonal (`F2`) rows with `t = 1.01, 1.02, …` — the right identity in
both cases, in exact rational arithmetic. The stored densities also equal `(4π/3)/mean(vols)` in
every row I checked (200/200). So the scan's *numbers* are consistent; only its scope is finite, as
its own docstring says.

## 9. Limits

- The corrected cover is evaluated at 60 digits with a `1e-30` inner shrink, and its margin is 2°;
  a fully exact (algebraic-endpoint) version would replace the `acos` comparisons by iterated
  resultants. The margin makes the numerical version safe, not exact.
- E's repair is not on the branch yet (`d289bef`); §5 is a specification, not an audit of a repair.
- C's `cde39fa` near-contact scan passed the original witnesses and the 69 audit cases; that is
  finite evidence, as the brief says, and I am not upgrading it to a soundness proof.
- Nothing here is a bound on packing density.

## 10. C102's constant: correct, and one error of my own corrected before it was published

The handover for this block carried a pending entry (`X-C070`) saying C102's
`min |p| = 3.206870905` at `ρ = 2.09` was **0.881% too high** and that the true minimum was
`3.178617889`, "already at C102's own direction". I checked it before writing it up, and it is wrong:
the two numbers are the same function at different radii, and **the problem is not scale invariant** —
the contact distance stays 2 while `ρ` moves, so `ρ = 2` (contact distance = radius, discriminant
`c²−0`, `r₊ = 2c`) and `ρ = 2.09` are different problems. The ratio of the two values is `1.008888`,
not `ρ`-ratio `1.045`, which is exactly the signature of that mistake.

`Reviews/twist/nearest_13th_indep.py` (exit 0) recomputes at `ρ = 2.09` and **reproduces C102 to
`2.45e-10`**: the face-centre value is `3.206870905245`, the closed form
`ρκ + √(ρ²κ²−ρ²+4)` with `κ = √((5+2√5)/15) = 0.794654472292` gives the same, Nelder–Mead from 32
starts returns it at the cube-corner direction, and 2·10⁶ random directions give `3.207307899`.

What upgrades this from "reproduced" to "decided": `r₊` is strictly increasing on its domain, so the
minimisation is a **covering-radius** problem, and the covering bound `max_i⟨u,x̂_i⟩ ≥ κ` for every unit
`u` has a three-line proof (§ X-C070): for `u` in a face triangle, `u = Σλ_k a_k/|Σλ_k a_k|` with
`Σλ_k = 1`, `t = max λ_k ≥ 1/3`, `m = 1/√5`, one has `max_j⟨u,a_j⟩ ≥ w/√w ≥ κ` because
`|Σλ a|² = (1−m)Σλ² + m ≤ (1−m)t + m = w` and `w ≥ w(1/3) = (1+2m)/3 = κ²`. Equality only at the 20
face centres. So the minimum over all directions is exactly `r₊(ρκ)`, and it is attained at a face
centre — which is what `(0.934172, 0.356822, 0) = (φ,1/φ,0)/√3` is, not an "edge midpoint" as
`CLAIMS.md:3012` says. The script's own "dodecahedral (hole)" enumeration is also wrong: it returns
**12** directions with `max_i⟨u,x̂_i⟩ = 2/√5`, i.e. a second icosahedron, not the 20 face centres, so
its printed "nearest among holes: 4.09" is that set's value, not a hole value. Neither defect touches
the constant or the conclusion: `3.206871 > 2·R_cell = 2.955706345` by `0.251165`, and
`> 2·1.045·1.258408572 = 2.630073915` by `0.576797`.

**Recorded as an error of this block**: the "0.881% too high" reading was a `ρ = 2` vs `ρ = 2.09`
confusion, caught before publication. The lesson is the same one `X-C062` taught: a constant is only
meaningful together with the normalisation it was computed in.

### 10.1 Main's third `twist_cover.py` (`a34a3ff1`, their C127) is correct

While checking the tips I found `twist_cover.py` had moved again, from `67d5c973` to
`a34a3ff104fc9be7d2e358cbbcf4151715c69e0c` (main `4dc1cc9`). The new revision fixes **both** defects
independently and in the same way `corrected_cover.py` does: `Aij` now carries `2u_xq_x`, and the
violation set is `|t − ψ| > h` with `h = arccos c`, endpoints shrunk inward by `1e-30`, reduced mod the
twist period `2π/5`. Run as `Reviews/twist/twist_cover_a34a3ff1.py` (exit 0): **53 proper arcs → 65
pieces → one merged interval `[0, 2π/5]`, no gaps**, 60 digits. So `X-C057` refutes the first two
revisions only, and `C127` now stands on a sound certificate.

One caveat, sound but sloppy: the fold `L = max(lo,kP) − kP` keeps only the part of `[lo,hi]` inside
`[0,2π]`. The instrumented run shows **5 pairs with `lo < 0`** (to `−0.550555`) and **5 with
`hi > 2π`** (to `6.833740`), so those pieces are dropped rather than wrapped. Dropped pieces are true
violations, so the emitted arcs remain strict subsets of the violation sets — the certificate is
**sound** and still closes — but the fold should be a reduction mod `2π`; otherwise a different
instance can lose coverage silently. Worth fixing before reuse, not a hole in `C127`.

## 11. Limits (this block)

- C102's value is confirmed with a *proof* of the covering step, but the cell-circumradius bound
  `2·R_cell = 2.955706345` is still C102's conservative `(ρ/2)√2`; the sharper `2.630074` uses my
  `1.258408572` for the `ρ = 2` dodecahedral cell, which is itself numerical.
- `C127` was checked by running the blob and instrumenting its fold; I did not re-derive its 53 pair
  constants. The soundness argument for the dropped pieces is analytic (periodicity), not machine-checked.
- The `ρ = 2` vs `ρ = 2.09` error above was mine, caught before it reached the registry.

## 12. E's repair of the cell certifier (experimental `f502b9a`) — audited, and it meets §5

Two things at the new experimental tip, and they must not be confused:

- `Experimental/scripts/rigorous_cell_volume.py` is **byte-identical** to the audited
  `d015a2e1e322853286322ff2c6ec4a5a88f03550` — only the path moved. `X-C060` and `X-C061` are
  therefore **still live in that file**, and `Experimental/scripts/certify_region.py` is still
  `540b4ed1`, so `X-C065`'s dropped remainder is live there too. Any number those files produce keeps
  the old defects.
- `Experimental/scripts/cell_certificate.py` and `certify_region_v2.py` (`ec1eaeda`) are new, name
  `X-C060`/`X-C061`/`X-C065` in their own docstrings, and implement the five requirements of §5.

Audit of the repair, by requirement:

1. **Norm.** Slack is `R·(7/4)·e_i + f_i` with the rational bound `√3 ≤ 7/4`. Sound: for `|y| ≤ R`,
   `|y·(n_i−n_i')| ≤ R‖n_i−n_i'‖₂ ≤ R√3 e_i`, and `7/4 ≥ √3` keeps it rational.
2. **Radius bootstrap.** `R₀ = b_max/(c − (7/4)e_max)` with `b_max` including `f_i`, and `c` a rigorous
   *lower* bound for `min_{|u|=1} max_i u·n_i'`: `max_i u·n_i'` is 1‑Lipschitz in `u`, so its minimum
   over the sphere is at least its minimum over a `δ`-net minus `δ`; they take `δ` = the longest mesh
   edge, which is a valid covering radius for a spherical triangle (acute: circumradius
   `L/(2 sin A_max) ≤ L/√3`; obtuse: the max of the distance to the nearest vertex is on an edge and
   `≤ L/2`). No vertex enumeration, no volume — not circular. Then `r(c − √3e_max) ≤ b_max` gives
   `|y| ≤ R₀` for every `y ∈ Ω`, so `Ω = Ω ∩ B_R` and the outer polytope is a genuine outer bound.
3. **Boundedness.** `Out` is bounded iff `0 ∈ int conv{n_i}` (the recession cone `{d : d·n_i ≤ 0}` is
   `{0}` exactly then), decided by scanning the supporting planes of `conv{n_i}` and requiring the
   origin strictly inside each, with a positive margin. This is *better than what I asked for*: my
   "four normals with a strictly positive dependence" is only sufficient and **rejects the cube** (any
   four of its six normals contain an antipodal pair); E caught that with their own control.
4. **Inner inclusion.** `Inn = {y·n_i' ≤ b_i' − slack}` gives `Inn ⊆ Ω ∩ B_R`, using the same `R`.
5. **Domain coverage.** `n = ceil(span/width)`, box width `span/n` exactly, `assert lo + n·w == hi`.
   The `[110°,111.05°]` / `0.3°` cases from `X-C065` can no longer lose a strip.

Run: `cell_certificate.py` exits 0, **reproduces both of my witnesses** (`y·δn = 8/9 > R·e = 4/5`,
ratio `1.111`; the four-vertex unbounded polyhedron **refused** with "0 is not in the interior of
conv(n_i), supporting planes checked: 1") and its five controls stay exact — cube `8`, tetrahedron
`8/3`, fcc and hcp `4√2`, C5 `5.8980173718` — with enclosure width `1.2e-18`.

Two limits, stated as such: `spanning_constant` evaluates the rational normals in `float` and deducts a
flat `1e-9`, which covers the `~1e-16` conversion error but is a fudge rather than an interval
computation; and the repaired path is `_v2` only — the old modules remain in the tree.

**What I ran of it.** The full default region `[110°,111°]×[35°,36°]` at `0.1°` (100 boxes, ~13 min)
**exits 0: "CERTIFIED for the whole region: `[5.859536248896, 5.940277014469]`"**, worst box at
`θ = 110.9°, φ = 35.0°`, target `5.763417470` cleared by `+0.096119`; certificate at
`Reviews/twist/reg_default_110_111_35_36.json`. So the repaired path is reproducible end-to-end — but
given `X-C080` it is *not yet a proof*: the gate and the `1e-9` must be fixed first.

## 13. C's extended near-contact scan (two- and three-site displacements)

`nearcontact_scan.py` moved `9b41169a → 9c37b1d4` (comp tip `926cdb7`) and gained `F4` (two sites
displaced in opposite directions — the multi-site case their own single-site argument does not cover)
and `F5` (three sites along independent random directions). The shipped `out/nearcontact_scan.json`,
checked in exact rational arithmetic: **500 rows** (`F1` 198, `F2` 14, `F3` 72, `F4` 144, `F5` 72),
**`t_star` is the single value `0` on every row**, density range `[0.620562, 0.739247]`; the **tiling
identity holds in every row** (`Σvol = a³` for `F1/F3/F4/F5`, `Σvol = a³·t_ax` for `F2`) and the stored
density equals `(4π/3)/mean(vols)` in 500/500 rows. So the multi-site families behave like the
single-site ones on these instances and the bookkeeping is exact. Scope is unchanged — finite evidence,
as the module's own docstring says.

## 14. C116's `6/√5` is now contradicted by Main's own script

With `twist_cover.py` repaired (`X-C071`), `near_contact_band.py` at main `4dc1cc9` — unmodified, run as
shipped — prints `cover? True` at every tabulated `d` up to **`3.00`**, its table's last row, and
"largest tested d with a certified cover: 3.00". `CLAIMS.md:3561` still states `C116` as `PROVED` at
`6/√5 = 2.6832816` and "sharp", and `Computation/README.md:28`, `CONTINUATION_0308.md:407` carry the
same number. `CLAIMS.md:3340` in the very same file already lists `K15-X-C051` — "the threshold is
`3.4555003444`; Main's `6/√5` was wrong (missing term, `C126`)" — as **adopted by Main**.

So the correct statement is the one in `X-C051`/`X-C064`: the certified band is `[2, 3.4555003444)`,
2.13× wider than C116 claims, and `6/√5` is a lower bound only. This is a documentation/consistency
defect, not a new mathematical one, and it resolves *in Main's favour*: Theorem D's near-contact
widening `ε < 1.4555` rather than `ε < 0.6833`.

## 15. `ACCEPTED.md:28`'s parenthetical number is the defective one

`ACCEPTED.md:28` writes "a one-pair argument is impossible (`min max_t d² = 8.4223 > 4`)". `8.4223` is
`A = |u|²+|q|²` with the missing `2u_xq_x` — the `X-C057` D1 constant. With the correct `A`, over the
same 121 pairs: `min over pairs of max_t d² = A+R = 12.844582472` (so still no pair clashes for all
twists: the *conclusion* holds) and `min over pairs of min_t d² = A−R = 0.044582472`, with **37 of 121
pairs** clashing for some twist. The near-zero `0.0446` is precisely why a one-pair argument cannot
work. Fix the number, keep the verdict.

## 16. Status asked for, consolidated (`X-C057` … `X-C076`)

| id | claim | verdict | witness |
| --- | --- | --- | --- |
| `X-C057` | `twist_cover.py` unsound in its first two revisions (missing `2u_xq_x`; arcs on the far set) | **REFUTED** | `audit_twist_cover.py` |
| `X-C058` | two-dodecahedra theorem at `d = 2` is true; the corrected cover certifies it | **PROVED** (60-digit interval arithmetic, 2° margin) | `corrected_cover.py` |
| `X-C059` | `C116` inherits both defects; statement true, threshold `3.4555003` | certificate unsound, statement true | `near_contact_band.py` run |
| `X-C060` | E: componentwise error used as Euclidean | **DEFECT** (`y·δn = 8/9 > 4/5`) | `audit_E_cell_volume.py` |
| `X-C061` | E: unbounded cell gets a finite enclosure | **DEFECT** (`[4/3,4/3]`) | `audit_E_cell_volume.py` |
| `X-C062` | §4 slack display true only with `E = ∅` | scope correction | `REVIEW` §4 |
| `X-C063` | the box alone does not repair the sandwich; a saturation check is needed | repair specification | `repaired_sandwich.py` |
| `X-C064` | the two-dodecahedra threshold is CERTIFIED at `3.455500344` | **PROVED** | `certified_threshold.py` |
| `X-C065` | E's region grid drops the remainder while printing "whole region" | **DEFECT** | `REVIEW` §5 |
| `X-C066` | no 13–20-face obstruction; needs unproved 20-face optimality | negative result | `REVIEW` §7 |
| `X-C067` | E's sin/cos interval extension is sound | **checked, sound** | `REVIEW` §5 |
| `X-C068` | C's near-contact scan is independent of the arc machinery | **checked** | `C_fixture_nonuniform.py` |
| `X-C069` | C's cell volumes satisfy the tiling identity on all rows | **checked** | `REVIEW` §8.1 |
| `X-C070` | C102's `3.206870905` is **correct**; the handover's `3.178617889` was the `ρ = 2` value | **CONFIRMED**, two auxiliary defects | `nearest_13th_indep.py` |
| `X-C071` | Main's third `twist_cover.py` (`a34a3ff1`) fixes both defects and closes | **checked**, one soundness-preserving sloppiness | `twist_cover_a34a3ff1.py` |
| `X-C072` | E's `cell_certificate.py` meets the five requirements; old defects live in the old files | **checked** | `cell_certificate.py` run |
| `X-C073` | C's `F4`/`F5` multi-site families still give `t* = 0`, tiling exact on 500 rows | **checked** | JSON audit |
| `X-C074` | `C116`'s `6/√5` contradicted by Main's own script (certifies to `d = 3.00`) | **documentation defect, in Main's favour** | `near_contact_band.py` run |
| `X-C075` | `ACCEPTED.md:28`'s `8.4223` is the defective constant; conclusion survives | number wrong, verdict right | 121-pair recomputation |
| `X-C076` | `rho_probe.py` consistent with C102; its `ρ = 2.0127` row is *below* `√32` | **checked** | `rho_probe.py` run |

Nothing here is a bound on packing density, and none of it is a Kepler proof.

## 17. Main's constants check does not cover C102

`Computation/constants_check.py` has 143 `chk(...)` calls. Two compare a value with itself —
`degrees(acos(c))` vs `degrees(acos(c))`, and `3.206870905` vs `3.206870905` — and the second is the
**only** ledger entry for `C102`'s nearest-thirteenth constant. A third, `chk("2.09 is below the
13-point threshold", mpf('2.09'), 2.09)`, compares `2.09` with `2.09` and tests nothing. So
`run_all_checks.py`'s "every ledger constant re-derived — PASS" (`X-C071`-era tip, all 17 checks pass
once `Main/` is present) is accurate for 140 of 143 entries and silent on the one that decides
`C101` case (B). The number is right (`X-C070`); the regression net has a hole where that number lives.

## 18. The 45-vs-53 arc counts reconcile, and 14 pairs are tangential

Cross-checked my `corrected_cover.arcs()` (45 raw pieces) against Main's repaired `inner_arcs`
(53 "proper"): identical pair set, and the difference is zero-width bookkeeping. Of the 121 pairs at
`d = 2`, **69** never come closer than 2, **14 are tangential** (`min_t d² = A − R = 4` exactly, so
`c = −1` and `half = π − acos(−1) = 0` — a single touching twist, no arc), and **39 genuinely violate**
for some twist and fold into the 45 pieces. Main counts the 14 tangential ones as "proper"; my 60-digit
code classifies one of them as "empty" because `A − R` evaluates to `4 + 10⁻⁵⁸`. So both covers rest on
the same 39 pairs, and the conclusion is unaffected.

The worth-knowing part: the certificate is carried by **39 of 121 pairs**, and 14 pairs sit exactly at
distance 2 for exactly one twist each — a strict-inequality argument would have to exclude those
explicitly, while the inner-arc formulation disposes of them automatically (their arcs are empty after
the margin). It also shows why Main's `1e-30` margin, rather than a `1e-58` epsilon, is the right device.

## 19. E's interval trigonometry, and what the default region actually covers

`cell_certificate._sincos` delegates to `rational_interval.sin_cos_iv_of_pi_multiple(·, 24, 32)` and
`_range_of` hulls the endpoints with every quarter-turn inside the box. Checked directly on **344
rational multiples of π in `[−2,2]`**: the exact values lie inside the returned intervals in every case,
maximum width `1.18e-37`. So the trig is sound, as `X-C067` found for the old module, and the only
non-interval step in E's chain is the flat `1e-9` inside `spanning_constant`.

One scope point. The C5 control is built at `sin θ = √55/8`, `cos θ = −3/8`, i.e. `θ = 112.02°`, and
certifies `5.8980173718`. The default region is `θ ∈ [110°,111°]`, which **does not contain** `112.02°`;
it certifies a neighbouring family (volume `[5.861827, 5.940277]`). Both clear the `5.763417470` target,
so no false claim is made, but "certified for the whole region" is not a statement about the C5 fixture
the self-test uses, and the two should not be conflated in the ledger.

## 20. Correction: `cell_certificate`'s boundedness test is not sound (my §12 over-credited it)

`REVIEW_0653` steering flagged `origin_interior_certificate`. Reproduced, and it is worse than the
steering's repro:

```
origin_interior_certificate([(1,0,0),(0,1,0),(0,0,1)])              -> (True, 1, 1)
   hull is a triangle in x+y+z=1; the origin is not in it
origin_interior_certificate([(1,0,0),(0,1,0),(0,0,1),(1,1,1)])      -> (True, 1, 4)
   all four points have x+y+z = 1, so 0 is NOT in conv -- and this hull IS 3-dimensional
```

The `b×c`-instead-of-`(b−a)×(c−a)` normals are a real inconsistency, but they are **not** the reason
the three-point probe passes: I re-ran the same scan with edge-vector normals and it still returns
`(True, 1, 1)`. The operative defect is that the routine never tests the hull's **dimension**. If
`conv{n_i}` is at most 2-dimensional, some plane contains every `n_i`, all points are on one side of it,
the origin is strictly on the inner side, and the "every supporting plane" argument is vacuous. Hence the
contract "0 lies in the interior of conv{normals}" is false.

What this does and does not break: the verdict feeds the boundedness decision in `polytope_volume`, so
the *guarantee* is gone. On the full-dimensional witness the failure is safe in practice —
`polytope_volume` returns `None` with 0 vertices and `certify` then raises on `None`. I have **no
demonstrated false volume**; what is refuted is the guarantee, and a false positive on a set with ≥ 4
vertices would reproduce `X-C061` exactly. So `X-C072`'s boundedness row is **withdrawn**; the other four
rows stand as algebra.

Second, independent: `spanning_constant` returns `F(vals.min()) − F(diam) − 1e-9` from a `numpy` mesh.
The 1‑Lipschitz + mesh-diameter argument is right, but the float error is assumed below `1e-9`, not
bounded. §12 called this "a fudge"; it belongs in the defect list, not the limits list, because `R₀`
truncates the outer polytope.

## 21. Two corrections to my own §7 (13–20-face route)

1. **The classes are nested.** `{polytopes with ≤ F faces}` increases with `F`, so the infimum of the
   cell volume over the class is **non-increasing** in `F`. My §7 compared the dodecahedron's 11.97%
   margin at `F = 12` with the icosahedron's 1.96% at `F = 20` and concluded "no obstruction for
   `F ≤ 20`". That inference is invalid: a larger margin at a smaller `F` says nothing about larger `F`,
   and a larger-volume 14-face example cannot refute a non-increasing infimum. What §7 actually
   establishes is narrower: *the icosahedron itself*, at `F = 20`, clears `√32` by 1.96% after the
   `1.045³` scaling — a statement about one polytope, not about the infimum over the class. The
   infimum statement still needs 20-face optimality, which is exactly the unproved input §7 named.
2. **Axial, not all-orientation.** The arc cover — mine (`X-C058`, `X-C064`) and Main's `C127`
   (`X-C071`) — varies the **twist about the shared vertex axis** with the two dodecahedra in one fixed
   relative orientation. It is not a theorem about arbitrary relative orientation, and any near-contact
   statement (`C116`, `C124`) that consumes it inherits that restriction. The gap between "all twists
   about the axis" and "all orientations" is not small and is not addressed here.

I did **not** audit `C124`/`C125`/`C128`/`C129`; the 19-point configuration named in the steering
(origin plus the 18 vectors in `{−2,0,2}³` of squared norm 4 or 8) does have minimum pairwise distance
exactly `2` and circumradius `2√2 = 2.828427`, which I verified — but I have not read those claims'
statements, so I assert no refutation of them.

## 22. `C125(b)`, `C124`'s `deg ≤ 12`, and what the 19-point fragment does and does not refute

`C125(b)` argues that "more faces ⟹ smaller minimum" is false, with the truncated octahedron
(14 faces, `6.158403`) against the icosahedron (20 faces, `5.054056`). That refutes monotonicity in
**exactly** `F`. It does not refute monotonicity of the infimum over **at most** `F` faces, which is
non-increasing by inclusion — and "at most `F`" is the quantity a bound on circumscribed volume needs.
So `C125`'s conclusion (stop the branch) survives on (a) alone — seven of the eight needed `F` have no
proved constant — but (b) is not an independent argument, and the same conflation appears in my §7
(corrected in §21).

`C124` uses `deg ≤ 12`. The steering's 19-point fragment (origin plus the 18 vectors in `{−2,0,2}³` of
squared norm 4 or 8) I verified directly: **19 points, min pairwise distance exactly `2`, circumradius
`2√2`**. It is an fcc fragment. Since the origin's degree in it is `6`, it does **not** refute a
per-point degree bound of 12; it refutes "≤ 12 points in a ball of radius `2√2`". So `C124` cannot use a
finite-ball count in place of `deg ≤ 12` at that scale, and `deg ≤ 12` itself still needs the
kissing-number theorem applied to a contact sphere, with the counting radius stated. I did not audit
`C128`/`C129`.

## 23. `C124`'s `deg ≤ 12` fails in the `(2+ε)`-graph — exact 17-neighbour witness

`C124` uses `S_ε ⊆ matched ∪ N(matched)` with a maximal matching of the `(2+ε)`-graph and then
"`deg ≤ 12`" to get `|S_ε ∩ B| ≤ 26|M ∩ B|`. The neighbourhoods in that domination step are taken in the
`(2+ε)`-graph, where 12 is not a bound: it is the kissing number for distance **exactly** 2.

Witness (`Reviews/twist/deg13_witness.json`): **17 rational points** with denominator 100, minimum
pairwise squared distance `4.1129`, maximum modulus `2.6647889 < 2 + 0.6832816`. With the origin they
form a 2-separated set, and the origin has 17 neighbours within `2+ε`. So at the band end `ε = 0.6832816`
the degree is at least 17 and the constant is at least `2 + 2·17 = 36`, not 26.

This refutes the step, not the theorem: the density-zero conclusion only needs a finite multiplier, and
a shell-kissing bound `deg_ε ≤ C(1+ε/2)²` would carry it. But `26` and `deg ≤ 12` cannot be used as
written, and `C124` is marked `PROVED`.

## 24. Erratum: `C128`'s one-pair proof is valid; my §15 was wrong

§15 ("`ACCEPTED.md:28`'s parenthetical number is the defective one") concluded that the parenthetical's
*verdict* — "a one-pair argument is impossible" — was right and only its number stale. **The verdict is
wrong too, and `C128` is right.** I maximised over the full `360°` twist circle; the physical twist space
is `72°` (`R/(2π/5)`, since a `72°` rotation about the vertex axis is an icosahedral symmetry). For the
pair with `A = 6.444582472`, `R = 6.4`: `h = arccos(−(3−√5)/2) = 112.4555152°`, so its violation arc has
length `2π − 2h = 135.0889696° > 72°` and meets every coset of `72°`; directly,
`max over τ ∈ [0°,72°) of min over k d²(τ + 72k°) = 1.266873708 < 4`, reproducing `C128`'s number to
`1e-9`. So a single pair does settle the step, and `C128` should replace the 65-piece cover.

What survives from §15: `8.4223` is the defective `A`, and the true `A + R` is `12.844582472`. But the
parenthetical in `ACCEPTED.md:28` is wrong on both counts and should be replaced by the pair certificate.
