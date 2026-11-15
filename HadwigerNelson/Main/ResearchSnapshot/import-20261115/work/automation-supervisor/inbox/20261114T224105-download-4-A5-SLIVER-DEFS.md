# A5 sliver: definitions extracted verbatim from m2's own files (no re-derivation)

Block 38. Read-only extraction for the parent's interval checker. Nothing here is computed or re-derived;
every formula is quoted with `file:line` from swarm `smwguidy9`, member m2. Where a quantity the request asks
for is **not** defined in those files, that is stated explicitly in §5.

## 0. The files (request d)

All paths are relative to the project repository root.

| file | lines | what it holds |
|---|---|---|
| `.ultramath/smwguidy9/m2/report.md` | 91 | claim classes, cone table, the exact obstruction (§C), the corner closed form, the sliver |
| `.ultramath/smwguidy9/m2/manifest.md` | 37 | the three claim classes C1/C2/C3 and the criterion formula |
| `.ultramath/smwguidy9/m2/sliver_scan.py` | 42 | the only place where `u_j, s_j, sigma, alpha_j` are actually **evaluated** |
| `.ultramath/smwguidy9/m2/block4_check.py` | — | the exact rational boxes and the `u`-parameterisation of the arcs |
| `.ultramath/smwguidy9/m2/levelsets.py` | — | the C3 search only (not needed for the sliver) |

## 1. (a) The quantities, as m2 defines them

**Bases and contact points** (`sliver_scan.py:3-5`):
```
s=mp.sqrt(3)/2
qm=mp.matrix([-mp.sqrt(3)/24,(6+mp.sqrt(429))/24]); qp=mp.matrix([mp.sqrt(3)/12,(3+2*mp.sqrt(33))/12])
ap=mp.matrix([mp.mpf(1)/2,mp.mpf(3)/2]); am=mp.matrix([-mp.mpf(1)/2,mp.mpf(3)/2])
```

**The two vertices of the fold** (`sliver_scan.py:10`):
```
def P(th,base): return mp.matrix([base[0]+mp.cos(th),base[1]+mp.sin(th)])
```
so `v1 = base1 + (cos θ1, sin θ1)` and `v3 = base3 + (cos θ3, sin θ3)`, with
`(base1, base3) = (qm, ap)` for **B1** and `(am, qp)` for **B2** (`sliver_scan.py:17-18`).

**The apexes** (`sliver_scan.py:11-13`; the same construction is spelled out in `report.md:45-46`):
```
def apexes(v1,v3):
    D=v3-v1; d=mp.sqrt(D[0]**2+D[1]**2); h=mp.sqrt(1-d*d/4); n=mp.matrix([-D[1]/d,D[0]/d])
    M=(v1+v3)/2; return [M+h*n,M-h*n]
```
i.e. `A± = (v1+v3)/2 ± h·n`, `n = (−D_y, D_x)/|D|`, `h = √(1 − |D|²/4)`, `D = v3 − v1`
(`report.md:46` states it identically).

**The corner coordinates** (`sliver_scan.py:30-32`), with the corner `ci = (0,1)` written explicitly as the
`−1` in the second coordinate:
```
s1=1-mp.sqrt((v1[0])**2+(v1[1]-1)**2); s3=1-mp.sqrt((v3[0])**2+(v3[1]-1)**2)
u1=mp.matrix([v1[0],v1[1]-1])/mp.sqrt(v1[0]**2+(v1[1]-1)**2)
u3=mp.matrix([v3[0],v3[1]-1])/mp.sqrt(v3[0]**2+(v3[1]-1)**2)
```
so, verbatim, `s_j = 1 − |v_j − ci|` and `u_j = (v_j − ci)/|v_j − ci|` with `ci = (0,1)`. `report.md:62-63`
states the same relation in closed form: `v_j = ci + (1 − s_j) u_j` with `|u_j| = 1`, `s_j > 0` inside `H`,
`s_j = 0` exactly at the arc end.

**The residual vector and `sigma`** (`sliver_scan.py:34`):
```
w=mp.matrix([A[0],A[1]-1]); sig2=w[0]**2+w[1]**2
```
so `w = A − ci` and `sigma² = |w|²` (`report.md:63` writes `w = A - ci`, `sigma^2 = |w|^2`). **`sigma` itself is
never formed**: only `sigma² = sig2` is ever used.

**`alpha_j`** (`sliver_scan.py:35`; `report.md:64`; `manifest.md:16`):
```
al=(sig2-2*s1+s1**2)/(2*(1-s1)); be=(sig2-2*s3+s3**2)/(2*(1-s3))
```
i.e. `alpha_j = (sigma² − 2 s_j + s_j²) / (2 (1 − s_j))` — the parent's formula, confirmed verbatim in all
three files.

**`det` and the criterion** (`report.md:64-67`):
> "hence with `u1=(0.80481,0.59354)`, `u3=(-0.41140,0.91151)`, `det=u1_x u3_y-u1_y u3_x=0.97771>0`:
> `w_y = (u1_x*alpha_3 + |u3_x|*alpha_1)/det`, so the apex is *below the floor* `v=1` (i.e. outside H,
> `m_floor<0`) **iff the single scalar inequality `u1_x*alpha_3 + |u3_x|*alpha_1 <= 0` holds**."

The numeric `u1, u3, det` there are the values **at one corner point**; `det`'s *formula*
`u1_x u3_y − u1_y u3_x` is given, but no other numeric `det` appears anywhere.

## 2. (b) The second parameter, its name and its exact ranges

The second parameter is **`theta1`** — the angle of the first unit step at `base1` (`report.md:45`: "For `v1`
in the qminus entry arc and `v3` in the aplus exit arc"). It is *not* free over all of ℝ: it ranges over the
certified entry arc of `base1`. m2 gives that arc **exactly** only in the rational `u`-parameterisation
`u = tan(θ/2)` (shift 0) or `u = tan((θ − π)/2)` (shift π):

| block | arc box used for the F5 exclusion | verbatim (`block4_check.py`) | generous box |
|---|---|---|---|
| B1, θ1 at `qm` | `E1` | `arc_box(qm, 0, F(201,1000), F(2565,10000))` | `E1c = arc_box(qm, 0, F(201,1000), F(257,1000))` |
| B1, θ3 at `ap` | `X1` | `arc_box(ap, 1, F(-2152,10000), F(36,1000))` | `X1c = arc_box(ap, 1, F(-216,1000), F(36,1000))` |
| B2, θ1 at `am` | `E2` | `arc_box(am, 0, F(-35,1000), F(217,1000))` | `E2c = arc_box(am, 0, F(-36,1000), F(217,1000))` |
| B2, θ3 at `qp` | `X2` | `arc_box(qp, 1, F(-245,1000), F(-1485,10000))` | `X2c = arc_box(qp, 1, F(-246,1000), F(-148,1000))` |

The parameterisation is `pt_from_u` (`block4_check.py:101-108`): `cos θ = (1−u²)/(1+u²)`,
`sin θ = 2u/(1+u²)`, both negated when the shift is `π`. So the exact closed ranges are, e.g. for B1's θ1,
`u ∈ [201/1000, 2565/10000]`, i.e. `θ1 = 2 arctan u ∈ [2 arctan 0.201, 2 arctan 0.2565]`
≈ `[22.74°, 28.72°]` — the degree renderings appear in `report.md:50` as `(22.73,28.77)` and in
`report.md:34` as `(22.73, 28.83)` for the *generous* arc.

`sliver_scan.py` does **not** range θ1 analytically: it samples 41 values over the arc,
`t1 = thb − radians((arc1_hi − arc1_lo − 1.0)·i/40)` for `i = 0..40`, skipping values below `arc1_lo`
(`sliver_scan.py:22-24`), where `thb = root_mhi(base1, arc1_lo, arc1_hi)` (`:19`) is the numerically found
root of `1 − |base + e^{iθ} − ci|² = 0` (`:14-16`). The same construction gives `thc` for `base3`, and the
sliver is sampled as 21 values `t3 = thc + radians(0.0038·j/20)` (`:26`), i.e. `0.0038` **degrees** of width,
matching `manifest.md:14`.

## 3. (c) The sliver domain and the inequality that is needed

**The domain, as m2 states it** (`report.md:55-57`, repeated in `manifest.md:14`):
> "The exclusion box excludes exactly `theta3 in (155.704811 deg, 155.708600 deg)` (B1) and
> `theta3 in (152.426823 deg, 152.430600 deg)` (B2), with `theta1` free in its own arc."

**The inequality, non-strict** (`report.md:67`, `manifest.md:15`): `u1_x*alpha_3 + |u3_x|*alpha_1 <= 0`.

**What the downstream argument needs.** The apex must be outside `H`. `H` is open and
`p ∈ H ⟺` all five margins `> 0` (`report.md:16`), the relevant one being `m_floor = v − 1 > 0`. The
criterion gives `w_y ≤ 0`, i.e. `m_floor ≤ 0`; at equality the apex has `v = 1` exactly and is **still
outside** the open `H`. So the **non-strict** form `≤ 0` is what is needed and what m2 states.

**Where the sliver comes from, exactly.** It is the complement of the shrunk `F5` boxes inside the generous
arc boxes (`block4_check.py:116-125`, comment: "shrunk boxes (used for the F5 exclusion; they miss only a
sliver of angular width < 0.03 deg at the arc ends that touch the corner ci=(0,1)")`. The shrunk boxes are
exact rationals (§2), so one end of each sliver is an exact rational `u`; the *other* end — the corner at
which the endpoint `v3` reaches distance exactly 1 from `ci` — is only ever computed numerically by
`findroot` (`sliver_scan.py:14-16,19`), and reported to six decimal places.

## 4. What m2's numbers say (quoted, not recomputed)

* sliver verdicts: all sampled points have `w_y < 0`, worst `w_y = −4.045e−3` (B1) and `−6.186e−3` (B2)
  (`report.md:69-70`, `manifest.md:16-17`);
* the far apex has `m_hi < 0` there (`|A_far − ci| > 1.5`) (`report.md:70`);
* the exact failure at the closed corner `(θ1, θ3) = (28.717498, 155.704811)°`: `v1 = (0.80481, 1.593543)`,
  `v3 = (−0.411403, 1.911514)`, `|D| = 1.257092`, `h = 0.777772`, `A− = (−2.827e−5, 1.0000482)`,
  `m_lo = +9.7e−5`, `m_lo2 = −1.0e−6`, `m_floor = +4.8e−5` (`report.md:58-60`);
* the sliver check is **not** interval-certified (`report.md:71-73`, `manifest.md:17`).

## 5. Quantities the request asks for that m2's files do NOT define

1. **Closed forms of `u_1, u_3, s_1, s_3, sigma` as explicit functions of `(θ1, θ3)`.** None appear. What
   appears is the *composite* definition of §1 (`sliver_scan.py:30-34`), evaluated numerically. A checker
   must therefore implement the composite, not a formula in the parameters.
2. **`sigma` itself.** Only `sigma² = |A − ci|²` is ever formed (`sliver_scan.py:34`).
3. **The exact sliver endpoint at the corner.** It is defined only as the root of
   `1 − |base + e^{iθ} − ci|² = 0`, found numerically (`sliver_scan.py:14-16,19`) and quoted to six places.
   No algebraic or closed-form description of that root is given in any of m2's files.
4. **Open versus closed endpoints of the sliver.** Not stated. The boxes are closed rational intervals
   (`block4_check.py`), while `report.md:50,55-56` renders the regions with parentheses. The corner
   evaluation at `θ3 = 155.704811°` is called "the closed corner" (`report.md:58`), which suggests the corner
   is intended to be included, but the box language suggests otherwise.
5. **Whether the `θ1`-side shrink is covered by the sliver argument.** The `F5` boxes also shrink the entry
   arc at its *upper* end (`2565/10000` against the generous `257/1000`), and `sliver_scan.py` samples `θ1`
   only *below* `thb` (`:22-24`). m2's report does not discuss a `θ1`-side sliver; presumably that region is
   where `v1` itself leaves `H` (`m_hi < 0`), but **that is not stated**.

**Reviewer note (mine, not m2's).** Points 3 and 5 are the ones that matter for the parent's checker: without
an exact algebraic description of the corner and without an explicit statement about the `θ1`-side shrink, a
certificate over "the sliver" has to fix the domain itself, and the two stated degree intervals
(`155.704811–155.708600`, `152.426823–152.430600`) are wider than the exact box gaps, so the checker must
decide which domain it is certifying.

---

# Addendum (block 42): exact endpoints, the corner, and the theta1-side coverage

Sources for this addendum: member m2 of swarm `smwgy3s8k`, files
`.ultramath/smwgy3s8k/m2/{manifest.md,report.md,crosscheck.py}` (its X1–X6 items, `crosscheck.py`
26/26 PASS in 0.09 s). The original extraction above is unchanged; this section answers the two
questions it left open (items 3 and 5 of §5).

## A1. The eight arc ends, with rational isolating brackets

`manifest.md:19-25` (§X1) gives each arc end as an explicit radical, with (a) an exact interval making the
margin's quadratic numerator enclose `0`, and (b) a rational bracket `[u−1e−9, u+1e−9]` carrying a **strict**
sign change of the margin. The `u`-values and the corresponding degrees:

| block | base | `u` | angle (deg) |
|---|---|---|---|
| B1 | qm | `0.201264277832277` | 22.759134449 |
| B1 | qm | `0.255989076986739` | 28.717498385 |
| B1 | ap | `−0.215250437021530` | 155.704811055 |
| B1 | ap | `0.035230739064970` | 184.035476250 |
| B2 | am | `−0.035230739064970` | −4.035476250 |
| B2 | am | `0.215250437021530` | 24.295188945 |
| B2 | qp | `−0.245375379412415` | 152.426822625 |
| B2 | qp | `−0.148788059725258` | 163.074314996 |

These are **closed** endpoints of the true arcs: the arc is the closed interval between the two ends of its
base, and each end is decided by the corresponding margin vanishing (`m_hi = 0` at the ends that touch `ci`,
`m_lo` or `m_lo2 = 0` at the others; `report.md:39-41` of the predecessor). The exact rational brackets are
what a checker should use; the decimal angles are renderings only.

## A2. The corner, as an exact enclosure

The corner where both arcs touch `ci` is **exactly** characterised, not merely enclosed:

> **Endpoint theorem** (m2 `report.md` §3, and re-derived by the coordinator in closed form). If
> `a = v1 − ci`, `b = v3 − ci` are unit vectors with `a × b > 0`, then
> `(v1+v3)/2 + h·n = ci` exactly, where `D = v3 − v1`, `h = √(1−|D|²/4)`, `n = (−D_y, D_x)/|D|`.

Closed-form check (coordinator): writing `a = e^{iα}`, `b = e^{iβ}`, `θ = β−α ∈ (0,π)`, one has
`h = cos(θ/2)` and `rot₉₀(D) = −2 sin(θ/2) e^{i(α+β)/2}`, so
`A₁ − ci = cos(θ/2)e^{i(α+β)/2} − cos(θ/2)e^{i(α+β)/2} = 0`.

Consequently at the closed corner the **lower** apex is `ci` itself, so
`m_lo = m_lo2 = m_floor = 0`, `m_hi = 1`, `m_edge = 3/4`, and `F = u1_x α_3 + |u3_x| α_1 = 0`: the
**non-strict** criterion holds with **equality**. The predecessor's `m_lo2 = −1.0e−6` (`report.md:58-60`) is
6-digit rounding noise (from the printed `A−` it is `−7.6e−7`; from the printed `v1, v3` it is `+7.5e−8`; at
the exact corner it is `0`), so **no `m_lo2` witness is needed at the endpoint**.

Numerical enclosure, as a cross-check only: `|A₁ − ci| ≤ 2.1e−12` (B1) and `≤ 1.6e−12` (B2)
(`manifest.md:26-29`, X3). The **exact** statement is the identity above, not the enclosure.

## A3. How the theta1-side shrink is covered

The F5 boxes shrink the entry arcs at their upper ends (B1: `2565/10000` against generous `257/1000`;
B2: `−35/1000` against generous `−36/1000`). `manifest.md:30-35` (§X4, §X5) settles both:

| gap | verdict | exact witnesses |
|---|---|---|
| B1, `u1 ∈ [2565/10000, 257/1000]` | **vacuous** — `v1 ∉ H` throughout | `m_hi < 0`: `m_hi(0.2565) = −2.56584481e−4`, `m_hi'(0.2565) = −0.535321596 < 0`, and `m_hi` is concave there (`A2 = −0.162317869 < 0`) |
| B2, `u1 ∈ [−36/1000, −35/1000]` | **must be INCLUDED** in the certified domain | `m_lo(−35/1000) = +8.31221328e−4`, `m_lo(−36/1000) = −2.76671136e−3`; `m_lo` is convex and increasing there, so its root lies in `(−36/1000, −35/1000)` and `m_lo > 0` on `(root, −35/1000]` |

So the θ1-side shrink is covered by an exact inequality on one side (B1: the endpoint itself leaves `H`) and
demands an enlargement of the domain on the other (B2: the piece `(−4.035476250°, −4.035476250° + …]` in
angle terms is inside `H` and must be certified).

## A4. The corrected three-piece domain

Uncovered by the shrunk F5 boxes, and therefore the domain a checker must certify:

1. B1: `θ3 ∈ (155.704811055°, 155.710334839°)` (the predecessor's stated window stopped at `155.708600`,
   covering only 68.6% of the gap);
2. B2: `θ3 ∈ (152.426822625°, 152.467398629°)` (stated window stopped at `152.430600`, covering 9.3%);
3. B2: `θ1 ∈ (−4.035476250°, −4.009068064°)` for all `θ3` of the exit arc (**not mentioned** in the
   predecessor's report at all).

## A5. Recommended exact target

`m_floor(A₁) ≤ 0`, equivalently the polynomial inequality (`manifest.md:52-56`)

  `R = (1 − |D|²/4)·D_x² − |D|²·Δ² ≥ 0`,  `Δ = (v1_y + v3_y)/2 − 1`,

which is sign-equivalent on the domain (`Δ ≥ 0`, `D_x < 0`) and involves **no square root, no `det` and no
division** — the cleanest form for an interval checker. m2 reports zero mismatches between `R` and
`m_floor(A₁)` over a 401×401×5 grid (numerical agreement, not a proof).
