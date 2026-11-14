# Independent verification: the Astra annulus 3-colouring is a proper colouring

**Verdict: the candidate is CORRECT as a local proper colouring of the unit-distance graph on the open
annulus.** Verified here by an exact rational argument plus a standalone exact verifier that uses no
floating point in any decision.

Grades used throughout: **[P]** = proof written here (paper-reviewed by the reader, not machine
checked); **[C]** = computational, exact rational arithmetic, reproducible by one command;
**[proposed]** = relayed from Astra, not independently established by me.

## 0. Statement verified
Let `A = {z ∈ ℂ : 0.99 < |z| < 1.01}` (open). For `z = r e^{iθ}` with `θ` in degrees, let
`k ∈ {0,…,8}` be the unique index with `θ ∈ [40k, 40k+40)` (the sectors are **half-open**, so `k` is
well defined with no ambiguity on boundaries), and set `colour(z) = k mod 3`.

> **[P][C]** No two points of `A` with the same colour are at Euclidean distance exactly `1`.

Given the reformulation in §1, this is exactly: two same-coloured points have angular separation
`Δ < 40°` (case A) or `Δ > 80°` (case B), and in case A the distance is `< 1`, in case B `> 1`.

## 1. The angular dichotomy **[P][C]**
Sectors `S_k = [40k, 40k+40)` tile the circle. Same colour means `k ≡ l (mod 3)`, i.e. the forward
sector distance `m = (l−k) mod 9` is `0`, `3`, or `6`.

* `m = 0`: both points are in the same sector, so `Δ < 40°` by half-openness.
* `m = 3`: raw differences lie in the open interval `(80, 160)`; since `160 < 180`, the smaller angle
  equals the difference, so `Δ ∈ (80, 160)`.
* `m = 6`: raw differences lie in `(200, 280)`; the smaller angle is `360 − difference`, giving
  `Δ ∈ (80, 160)` again.

The verifier enumerates **all 18 ordered same-colour sector pairs** and confirms each has
`Δ ⊂ (80°, 160°)`, that no same-colour pair falls in the forbidden band `(40°, 80°)`, and that the two
regimes `[0,40)` and `(80,180]` are disjoint. **Wraparound** is handled by taking `m = (l−k) mod 9`
and by folding with `360 − d`; **sector boundaries** are handled by the half-open convention, which
assigns every angle to exactly one sector; **unequal radii** are handled in §2, where the radius
ranges enter explicitly.

## 2. Distance bounds for unequal radii **[P][C]**
Write `z_j = r_j e^{iθ_j}`, `Δ = |θ_1 − θ_2|` (smaller angle), `r_j ∈ (0.99, 1.01)`. Then exactly

```
|z1 − z2|² = (r1 − r2)² + 2 r1 r2 (1 − cos Δ).
```

**Case A (`Δ < 40°`).** Since `cos` decreases on `[0,180]`, `1 − cos Δ < 1 − cos 40°`. Also
`(r1−r2)² < (0.02)²` and `r1 r2 < (1.01)²`. Hence

```
|z1 − z2|² < (1/50)² + 2·(101/100)²·(1 − cos 40°)  ≤  1194517/2500000  =  0.4778068  <  1.
```

**Case B (`Δ > 80°`).** Now `cos Δ < cos 80°`, so `1 − cos Δ > 1 − cos 80°`, and `r1 r2 > (0.99)²`, so

```
|z1 − z2|² > 2·(99/100)²·(1 − cos 80°)  ≥  4035179511/2500000000  =  1.6140718  >  1.
```

Margins: case A has slack `0.5222`, case B has slack `0.6141`.

## 3. Rigorous rational bounds for cos 40° and cos 80° **[P][C]**
No decimal approximation is used. From `cos 3t = 4cos³t − 3cos t` with `t = 40°` and
`cos 120° = −1/2`, the number `c = cos 40°` satisfies

```
f(c) := 8c³ − 6c + 1 = 0.
```

`f'(c) = 24c² − 6 > 0` for `c > 1/2`, and `f(1/2) = −1 < 0 < 3 = f(1)`, so `f` has **exactly one**
root in `(1/2, 1)`, and that root is `c`. Exact rational evaluation gives

```
f(383/500) = −5613/15625000 < 0   ⟹   cos 40° > 383/500,
f(767/1000) = 967663/125000000 > 0 ⟹  cos 40° < 767/1000.
```

Monotonicity of `f` on the interval is what turns a sign test into a bracket, so these are rigorous,
not sampled. Then since `x ↦ 2x² − 1` is increasing for `x > 0`,

```
1 − cos 40°  ≤  1 − 383/500            = 117/500        = 0.234000,
1 − cos 80°  ≥  2 − 2·(767/1000)²      = 411711/500000  = 0.823422,
```

using `cos 80° = 2cos²40° − 1`.

## 4. Sampling circles inside the annulus **[P][C]**
By the reverse triangle inequality, if `|z − x| = r` then `r − |x| ≤ |z| ≤ r + |x|`. Hence for
`|x| < 0.005` and `|r − 1| ≤ 0.005`:

```
|z| ≥ r − |x| > 0.995 − 0.005 = 0.99,        |z| ≤ r + |x| < 1.005 + 0.005 = 1.01,
```

so **every** point of every such circle lies in `A`. In particular the unit circle `{|z − x| = 1}`
about any `|x| < 0.005` lies in `A` — indeed `|z| ∈ (0.995, 1.005)`.

**This lemma is tight, and that matters.** The two losses `0.005` (from `|x|`) and `0.005` (from
`|r−1|`) sum to exactly `0.01`, the annulus half-width. Both inequalities must therefore be strict:
`|x| < 0.005` and `|r − 1| < 0.005` (I have stated the radius condition as `≤` for the containment
bound, which is safe, but replacing the centre condition by `|x| ≤ 0.005` would break stricteness at
the boundary). Any implementation that samples on circles of radius near `1` about centres near the
boundary must respect this.

## 5. The verifier
`annulus_verify.py` — standalone, standard library only (`fractions`), **no floating point in any
decision**; decimals appear only in printed commentary. It performs: the `f`-bracket for `cos 40°`
(§3); the full enumeration of same-colour sector pairs (§1); the two distance bounds as exact
rational inequalities with the printed exact values (§2); and the sampling-circle containment (§4).
Exit code 0 on success, 1 on any failed check.

```
cd supervisor/solve-graphs && python3 annulus_verify.py     # <- 0.03 s, sole compute process
```
Last run: **ALL CHECKS PASS**, log `logs/annulus_verify.out`.

## 6. Precise assumptions and scope
**Assumptions.** (i) The colouring rule is as relayed: nine half-open `40°` sectors starting at angle
`0`, colour = index mod 3. (ii) The domain is the *open* annulus `0.99 < |z| < 1.01`. (iii) The metric
is Euclidean and angles are in degrees. (iv) The "sufficiently nearby sampling circles" condition is
read as `|r − 1| ≤ 0.005` with centres `|x| < 0.005`; a different reading needs a different check.

**What this establishes.** A proper 3-colouring of the unit-distance graph induced on the annulus `A`.
That is a **local** statement.

**What this does NOT establish, stated plainly.**
* It is **not** a 6-colouring of the plane, nor a piece of one assembled here.
* It is **not** a refutation of the global ternary theorem, nor any statement about global
  colourings of `ℝ²`.
* No palette-transport or compatibility claim is made or implied. Nothing here says this annulus
  colouring can be glued to a colouring of the inner disc, the outer region, or a neighbouring annulus;
  the sector colouring has no continuity across the annulus boundary in either direction.
* `chi(ℝ²) ∈ {6,7}` is unchanged and untouched.

**Residual gap, if any.** The only input not independently re-derived here is the colouring rule
itself (§6(i)), which is taken as relayed. Everything mathematical downstream of it is proved above and
machine-checked exactly.
