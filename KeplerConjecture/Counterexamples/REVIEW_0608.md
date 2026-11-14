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

So the theorem is true and certified: **for every relative twist, some pair of the two eleven-point
sets is strictly closer than 2, hence two regular dodecahedral cells of inradius 1 cannot have
centres at distance exactly 2.** That restores `C108` step (4) — as `X-C057`, replacing `C112` and
`C123` as the load-bearing certificate.

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

## 7. Fallback (not needed)

The fallback asked for was either a proof of the general bounded-interval sign method under its
input contract, or a near-contact obstruction for the 13–20-face route. Both were addressed earlier
(`X-C046`: the Vincent–Descartes decider with 92 cases and the `nsimplify` defect it found; `X-C051`:
the `3.4555003` threshold). Nothing new is claimed here beyond pointing `C116` at `X-C051`.

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
