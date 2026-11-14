# Review 0523 — the first rigorous piece of the interval branch-and-bound

Block `K15-REVIEW-0523-E`. Receipt `13:31:10Z`. Follow-up to `93c61a8`.
Read: Main `a6f3935` `GEOMETRIC_LEMMA_0438.md` (Theorems B, C, D), and `REVIEW_0353.md` §9.

The brief was: build the first genuinely rigorous component of the interval branch-and-bound
— an explicit finite domain, a completeness argument for its parameterisation, and a
directed/algebraic evaluation of a contact-polytope volume on one nontrivial box — starting
from the C5 fixture and the Barlow controls, and eliminating floating sign tests from any
artifact called exact.

**What is delivered.** A certified volume enclosure that decides everything by exact rational
comparison (`rational_interval.py`, `rigorous_cell_volume.py`), validated on three controls
with known answers; the finite domain and its completeness argument (§3); the statement of
what it does and does not bound (§2.3); and two audit findings on Main's file, one of which is
an error in **my own** published constant (§5).

---

## 1. No floating sign tests: what changed

Main's `GEOMETRIC_LEMMA_0438.md` §4 records, correctly, that `barlow_contact_cell.py` admits
vertices by `sp.N(expr, 30) > 1e-25` and compares radii numerically, "so it is not fully exact
and is not advertised as such here". That is right, and the artifact is not repaired by
renaming it: **every decision in the new machinery is a `Fraction` comparison.**

`rational_interval.py` provides

- `Iv`, a closed interval with `Fraction` endpoints and the four operations (multiplication by
  min/max over the four corner products, division only when the divisor excludes 0);
- `sqrt_iv`, rigorous square roots of rational intervals by integer `isqrt` at a chosen scale;
- `pi_iv`, a rigorous enclosure of π from **Machin's formula** with the alternating-series
  remainder bound, and `sin_cos_iv_of_pi_multiple`, Taylor series on the *interval* argument
  with the standard remainder bound.

There is no external interval library and no floating point anywhere in the decisions. The
self-tests check π against a 60-digit reference to `1e-45` (width `8e-72`), sin/cos likewise
(widths `1e-70`), and — this is the only *rigorous* internal check — that the enclosures
satisfy `sin² + cos² ∋ 1` for four angles, which uses no reference value at all.

One bug worth recording: the first version reported a width of `1e-44` for π because
`arctan(1/5)` was truncated at 30 terms, whose tail is `5^-61 ≈ 1e-43`. The Taylor series was
not the limitation; the arctan series was. Corrected by 50 terms for `1/5` and 25 for `1/239`
(`239^-51 ≈ 1e-129`), which also made the module 4× faster.

---

## 2. The certified volume enclosure

### 2.1 Method: a two-sided rational sandwich

For centres `p_i` and payer `w`, in coordinates `y = x − w`,

```
Omega(w) = B(w,2) ∩ { y : y·v_i <= c_i },      v_i = p_i − w,   c_i = |v_i|²/2 .
```

Each centre is known only through an interval. Writing `n_i = v_i/|v_i|` (unit) and
`b_i = |v_i|/2`, the half-space is `{y·n_i ≤ b_i}`. Choose rational `n_i'`, `b_i'` with
certified errors `|n_i − n_i'| ≤ e_i`, `|b_i − b_i'| ≤ f_i`, and a rational `R` bounding `|y|`
on the true polytope. Then for `|y| ≤ R`,

```
y·n_i ≤ b_i   ⟹   y·n_i' ≤ y·n_i + R e_i ≤ b_i + R e_i ≤ b_i' + (R e_i + f_i) ,
```

so

```
{ y·n_i' ≤ b_i' − (R e_i + f_i) }   ⊆   Omega(w)   ⊆   { y·n_i' ≤ b_i' + (R e_i + f_i) } .
```

Both bracketing polytopes have **rational** data, so their volumes are computed exactly.

`R` itself is not assumed: since the true cell is contained in the outer polytope, it suffices
that every *outer* vertex satisfies `|y| ≤ R`, and the code checks that exactly and raises if it
fails. `R = 3/2` certifies for all four controls. Without that check the error term `R e_i`
would be an assumption rather than a bound, which is the sort of thing an artifact called
"exact" must not contain.

### 2.2 The exact polytope volume, and the bug it replaced

Vertices are the feasible triple-plane intersections, by Cramer's rule over `Fraction`s, with
feasibility decided by exact rational comparison. Each face is put in cyclic order by an exact
angular sort (comparisons are cross-product signs, so the non-orthonormality of the in-plane
basis is harmless for an *order*), triangulated, and

```
V = (1/6) · | Σ over oriented boundary triangles of det(a, b, c) | .
```

That form is rational — no square root appears — and the orientation is outward because the
basis `(e1, e2, n)` with `e2 = n × e1` is right-handed.

**The first version used `V = (1/3) Σ d_i A_i` with the face areas from a shoelace formula in
a *non-orthonormal* basis, which silently scaled every area by `|e1||e2|` and returned
`5.4997` instead of `5.6568` for the fcc cell.** The control caught it. The determinant form
removes the failure mode rather than patching it, since there is no scale factor to get wrong.
A cube (`volume 8`, eight vertices) is checked before any geometric control.

### 2.3 Scope: one payer, not the cluster

This machinery bounds **one** payer's cell for **one** configuration. By `K15-E090` the twelve
pairs `(c, w_i)` are congruent under the icosahedral group, so a bound for the pair `(c, w_1)`
is a bound for each pair individually — but **simultaneous compensation of all twelve is a
different statement** and is not touched here. `(CUT)` needs the simultaneous form; `(P')` is
the pairwise form. Nothing in this file may be read as the former.

### 2.4 Controls

| control | reference | result |
| --- | --- | --- |
| cube `[-1,1]³` | `8` exactly | exact, 8 vertices |
| fcc contact cell | `4√2 = 5.656854249492381` | enclosure, 14 vertices |
| hcp contact cell | `4√2` | enclosure, 14 vertices |
| C5 payer fixture | `5.898017371803720` | enclosure, 20 vertices |

| control | reference | enclosure | width |
| --- | --- | --- | --- |
| cube `[-1,1]³` | `8` exactly | exact | `0` |
| regular tetrahedron | `8/3` exactly | exact, 4 vertices | `0` |
| fcc contact cell | `4√2` | `[5.656854249492381, 5.656854249492381]` | `1e-18` |
| hcp contact cell | `4√2` | same | `1e-18` |
| C5 payer fixture | `5.898017371803720` | `[5.898017371803721, 5.898017371803721]` | `8.7e-19` |

All three geometric controls contain their reference value; the whole run is 6.6 s.

**And out of sample.** The controls are fixed configurations, so the enclosure is also checked
against the independent float code path (`c5_fixture.py`: numpy plus a `ConvexHull` volume) at
random `(θ, φ)` in the legal window — `volume_crosscheck.py`. Agreement is to `~1e-15`, i.e.
the float's own accuracy, which is the strongest statement a float comparison can make.

*(The first version of that check demanded that the float value lie inside the `1e-18`-wide
enclosure and "failed" on a case whose values agreed to twelve digits. A float carries `1e-15`
error, so containment in a `1e-18` interval is not a meaningful test — the tolerance form is.)*

### 2.5 One nontrivial box — and the honest size of the step

The same sandwich accepts *interval* centres, so it evaluates a whole region at once. For the
C5 family with `θ ∈ [111.70°, 111.90°]` and `φ ∈ [35.5°, 36.5°]` (sin and cos are monotone on
both ranges, so the hull of the corner values is the exact range):

```
certified   [5.728055604988, 6.066297678036]      width 0.338
```

That is **correct and too wide**: the true variation of the volume over that box is of order
`1e-4`, so the `0.338` is dependency, not geometry — the normal error `e_i` of each interval
centre is multiplied by `R` in the sandwich and summed over twelve constraints.

So the atom must be calibrated, and it is worth doing here rather than guessing. Halving the
box around `(θ, φ) = (111.7975°, 36°)`:

```
 k   box width (deg)      certified enclosure            width
 0     0.1              [5.8712721949, 5.9246189771]    5.33e-02
 1     0.05             [5.8846251953, 5.9112982754]    2.67e-02
 2     0.025            [5.8912975480, 5.9046339975]    1.33e-02
 3     0.0125           [5.8946326818, 5.9013008823]    6.67e-03
 4     0.00625          [5.8962999874, 5.8996340814]    3.33e-03
 5     0.003125         [5.8971335748, 5.8988006202]    1.67e-03
```

**The width is linear in the box width**, as the dependency argument predicts, and — this is
the useful part — **the lower end is already useful at the coarsest box**: `0.1°` certifies
`vol > 5.8712`, which is `0.108` above the `(P')` threshold `5.7634`. A two-parameter family is
therefore exhaustively certifiable at `(14/0.1)² ≈ 2×10⁴` boxes, which is cheap.

**How much of that width is real?** Measured on the same `1° × 1°` box: evaluating the volume at
the centre and the four corners (each to `1e-18`) gives

```
true variation over the 1° box   [5.898239004, 5.898239907]   width 9.0e-07
sandwich over the same box       [5.629142811, 6.162489628]   width 5.3e-01
                                                     ratio   ~6e5
```

so the sandwich is dominated by dependency by nearly six orders of magnitude. The caveat is
that this box is centred on the family minimum, where `dV/dθ = 0`; over the whole legal window
the volume moves by `0.064`, i.e. a Lipschitz constant of about `4e-3` per degree. **Even that
is ~130× better than the sandwich**, so the obvious next improvement is a parameter-Lipschitz
bound (differentiate `V` in `(θ, φ)`) rather than a finer sandwich. That is a concrete design
input, not a repair done here.

The catch is the one that matters: **that is the C5 family, not the completion space.** The
domain of §3 has up to 200 coordinates, and no 0.1°-granular grid over it is remotely
reachable. So the atom is not the obstruction — the *dimension* is. A branch-and-bound would
have to be preceded by a reduction to a low-dimensional family, and no such reduction is known.
That is the honest state of the route, and it is the number the next block needs.

---

## 3. The finite domain, and its completeness argument

The atomic operation of §2 is only useful if the space of completions is finite-dimensional
and explicitly described. It is:

> **Domain `D`.** The added centres of a completion of the six fixed centres `{c, ring_0..4}`
> that can affect `Ω(w_1)` lie in
> `S = { z : 2 ≤ |z − w_1| < 2.603447 }`, and each is 2-separated from the six fixed centres
> and from the others.

**Completeness.** (i) A centre with `|z − w_1| ≥ ρ_max := 2.603447` has its bisector at
distance `≥ ρ_max/2 = 1.301724 > max|vertex| = 1.301723`, so it cannot meet the cell
(`REVIEW_0353` §2, where the two numbers are certified). (ii) A centre with `|z − w_1| < 2`
is illegal. (iii) Every legal `z` has a unique `(ρ, θ, φ) ∈ [2, ρ_max) × [0,π] × [0,2π)`, and
a finite set of centres is unordered, so sorting the tuples gives a unique representative.
(iv) The number of centres is bounded: they are 2-separated inside the shell, so
`N ≤ vol(B(0, ρ_max + 1))/(4π/3) = (ρ_max+1)³ ≈ 200` — crude but finite and explicit.

So `D ⊂ ⋃_{N≤200} ([2,ρ_max]×[0,π]×[0,2π))^N / 𝔖_N`, a finite union of compacta, and
`inf vol Ω(w_1)` over completions equals the infimum of the continuous functional over `D`.
**That is a genuine completeness statement, and it is not a size reduction**: 200 coordinates
is far past exhaustive search, and the bracketing volume of §2 is the only piece of it that is
currently rigorous.

**What is still missing for a bound.** A branch-and-bound needs (a) the bracketing volume —
supplied here — and (b) a *monotone* bound of the volume over a box *in the domain*, i.e. an
enclosure valid for every configuration whose centres lie in that box, not only for a fixed
configuration. §2 does exactly that as soon as the box is propagated into interval centres,
which is the next step and is the reason the domain statement above matters.

---

## 4. Audit of Main's Theorem D: the compactness is sound, the rigidity is the gap

Theorem D (`σ₀ > 2V_dod`) has four steps. Checked:

- **(2) the cone bound.** For `x ∈ Ω(v)` at distance `r`, the cone from `x` over the unit disc
  of `B(v,1) ⊆ Ω(v)` perpendicular to `vx` lies in `Ω(v)` by convexity and has volume `πr/3`,
  so `r ≤ 3C/π`. Correct, and `B(v,1) ⊆ Ω(v)` holds because every neighbour is at distance
  `≥ 2`. ✓
- **(2) the reduction to a compact set.** A centre at distance `> 2R_max` has its bisector
  outside `B(v,R_max) ⊇ Ω(v)`, so only centres within `2R_max` of `v` or `w` contribute; those
  form a bounded 2-separated set, and the admissible configurations form a finite union (over
  `N ≤ N_max`) of compacta on which `Φ` is continuous. ✓
- **Minor arithmetic slip, quantified.** `§4.1b` bounds the number of points by
  `(21.865)³ ≈ 10453`. For a 2-separated set in `B(0,R)` the correct bound is
  `vol(B(0,R+1))/(4π/3) = (R+1)³`, since the unit balls around the centres are disjoint and lie
  in `B(0,R+1)`. With Main's own `σ₀ ≤ 11.448258` this gives `R = 3σ₀/π = 10.9323`,
  `2R = 21.8646`, hence

  ```
  N ≤ (2R+1)³ = 11953      (Main writes 10453, which is (2R)³)       ratio 1.144
  ```

  and with the sharp `σ₀ ≤ 2√32` it is `11555`. No conclusion changes — both are "≈10⁴" — but
  the `+1` is the radius each centre reserves and it is a 14% term, so the number as written
  is not the one the argument gives.
- **(3) the rigidity — the load-bearing gap.** Step 3 needs: `vol Ω(v) = V_dod` forces `Ω(v)`
  to be the regular dodecahedron of inradius 1. That is the **equality case of
  Hales–McLaughlin**, imported and not re-derived, and Main flags it as the soft dependency.
  I confirm it is soft, and I could not replace it: the obvious route ("the cell is contained
  in the intersection of half-spaces at distance ≥ 1") gives no upper bound at all without a
  bound on the number of faces, and any such bound is the theorem itself. **A self-contained
  Theorem D would need the equality case proved, and that is a research problem.**
- **(4) two-dodecahedra.** True, and Main's constant is the correct one — see §5.

---

## 5. Correction to my own `K15-E075`

`K15-E075` states that two adjacent centres cannot both be dodecahedral, with the two
icosahedral rings clashing "at distance `1.056487696` against a required `2`". Main's file
gives `1.12555484451` for the same configuration and records the discrepancy.

**Main is right and I was wrong.** Recomputing independently: put `v` at the origin with its
twelve contacts at the icosahedron of circumradius `2`, `w` at `(0,0,2)` with its ring a
translation of `v`'s, remove the shared contact from each ring, and maximise over the relative
twist the minimum cross-distance. The maximum is

```
1.125554845   at twist 0°,      required 2
```

matching Main to nine digits. The error was a max/min slip in my script: the quantity `(P')`
needs is the **maximum over twists of the minimum distance** (a twist is excluded if *any*
pair clashes), and the minimum over twists is `0.211145618` at `36°`, which is not the
relevant number and is not `1.056487696` either.

**The conclusion of `K15-E075` is unaffected** — both values are well below `2`, so no twist
admits two dodecahedral cells, and `2V_dod` remains unattainable. The ledger entry is corrected.

---

## 6. What this block does not deliver

- **No bound over completions.** §2 encloses one cell of one configuration. The branch-and-bound
  needs the box-monotone version of §3(b), which is not written.
- **No new number for the payer.** The window at the icosahedral pair is unchanged:
  `[5.550291, 5.897967]` around a threshold of `5.763417`.
- **No repair of `barlow_contact_cell.py`.** It is still the artifact Main correctly declines to
  call exact; `rigorous_cell_volume.py` supersedes it for the volume question, and the old file
  should now be read as a float check only. (Replacing its sign test with the `Fraction`
  machinery of §1 is mechanical but was not done here, and saying so is cheaper than implying
  it.)

---

## 7. Reviewer obligations for X

Three things in this file are checkable and should be checked independently, in this order.

1. **The sandwich inequality (§2.1).** The claim is
   `{y·n_i' ≤ b_i' − (R e_i + f_i)} ⊆ Ω ⊆ {y·n_i' ≤ b_i' + (R e_i + f_i)}` from
   `|n_i − n_i'| ≤ e_i`, `|b_i − b_i'| ≤ f_i`, `|y| ≤ R`. It is one line, but the *direction* of
   each error matters and an inverted sign would still pass the controls if the reference
   values were taken from the same code. They are not — the references are `4√2` and
   `5.898017371803720`, both independently known.
2. **The exact volume (§2.2).** `V = (1/6)|Σ det(a,b,c)|` over oriented boundary triangles.
   The orientation argument (`(e1, e2, n)` right-handed with `e2 = n × e1`) is the only place a
   sign convention enters; a wrong orientation gives `−V`, which the `abs` hides. The cube
   control cannot see that, which is why a **non-symmetric** control with a rational volume was
   added: the regular tetrahedron `(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)` has volume exactly
   `8/3`, and a wrong face set or cyclic order changes it. Both are exact, not enclosures.
3. **The compactness constants of `§4`.** `(2R+1)³ = 11953` against Main's `10453`, and the
   cone bound `r ≤ 3C/π`. Both are elementary; the first is a 14% term.

What is **not** claimed and should not be reviewed as if it were: any bound over completions,
any improvement to the payer window `[5.550291, 5.897967]`, or any replacement of
`barlow_contact_cell.py`'s sign test (that file is still a float check and is superseded rather
than repaired).

## 8. Hashes

```
source read (Main)   a6f3935    KeplerConjecture/Main/GEOMETRIC_LEMMA_0438.md
continued from (E)   93c61a8b926eeece8ea0abff10e231757d76a2cc
this block           see the final commit; the tip is reported in chat and in the ledger
artefacts            Experimental/scripts/rational_interval.py
                     Experimental/scripts/rigorous_cell_volume.py
                     Experimental/REVIEW_0523.md
                     Experimental/COMPUTE_REQUEST_0523.md
ledger ids           K15-E091 (certified enclosure), E092 (box-blindness/scaling),
                     E093 (correction to E075)
```
