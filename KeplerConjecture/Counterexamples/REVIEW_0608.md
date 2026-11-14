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

1. **boundedness** — prove it, don't inherit it: either exhibit a positive combination of the
   normals summing to zero, or impose `|y| ≤ R` as a *constraint* in both polytopes and check it;
2. **norm choice** — slack `R‖n − n'‖₂`, or renormalise so that `‖n − n'‖₂ ≤ √3 max|·|` is paid for;
3. **radius bootstrap** — `R` must be an a-priori bound (`R = 2` follows from `Ω(w) ⊆ B(w,2)`
   independently of any enumeration), not a property checked against the vertices that were found;
4. **inner inclusion** — with (1)–(3) the two-sided inclusion is valid; the lower bound must fall
   back to `0` when the inner polytope is empty (the code does this ✓);
5. **domain coverage** — bounding one cell of one configuration is not bounding a family; the
   branch-and-bound must cover the parameter domain exactly, boundary included.

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

## 9. Limits

- The corrected cover is evaluated at 60 digits with a `1e-30` inner shrink, and its margin is 2°;
  a fully exact (algebraic-endpoint) version would replace the `acos` comparisons by iterated
  resultants. The margin makes the numerical version safe, not exact.
- E's repair is not on the branch yet (`d289bef`); §5 is a specification, not an audit of a repair.
- C's `cde39fa` near-contact scan passed the original witnesses and the 69 audit cases; that is
  finite evidence, as the brief says, and I am not upgrading it to a soundness proof.
- Nothing here is a bound on packing density.
