# Block `K15-REVIEW-0608-M` — two bugs of Main's own, a stalled branch, and a closed hypothesis

Received `2026-11-14T14:14:05.884Z`. Sources: C `cde39fa67448ac995b4b8a6b9def56522d06d59e`,
E `d289bef49fa25aea10c4c8c0c7299d5d5449fdd0`, X `729df1e` (inside
`kepler15/counterexamples/run-01`, now at `ee1848c`), supervisor
`d958324309b66c0c705d15f014140ff19ca97b53` plus the `…-LOCAL` evidence. Main from `8dc264e`.

The brief asked for a full hour, at least two sustained attempts, and no stopping after a repair.
It also named two defects in Main's arc cover. **Both were real, and a third was found while fixing
them.** That is the main content: two attempts (§2, §3), one of which stalled and one of which
succeeded, plus a soundness repair that had to come first (§1).

## 1. The arc cover: two bugs, both making the test report success

Both are named in the brief and in `K15-REVIEW-0608-M-LOCAL`; Main confirms both and records them as
`C126` and `C127`.

**1.1 A dropped algebraic term (`C126`).** With `R_t` a rotation about the `x`-axis and `u = w − a`,

```
d²(t) = |u|² + |q|² + 2⟨u, R_t q⟩
      = |u|² + |q|² + 2u_x q_x + 2(u_y q_y + u_z q_z)cos t + 2(u_z q_y − u_y q_z) sin t ,
```

and the first version omitted `2u_x q_x` — the `x`-components are untouched by a rotation about `x`,
so that term does not vanish. Verified on a pair at `d = 2.7`: direct `min_t d² = 7.29` against
`A − R = 4.06`, and `4.06 + 2u_x q_x = 7.29` exactly.

**1.2 The arcs were the opposite inequality (`C127`).** Since `cos` is decreasing on `[0,π]`,

```
{ t : cos(t − ψ) < c } = { |t − ψ| > arccos(c) },
```

i.e. the arc **centred at `ψ + π` with half-width `π − arccos(c)`** — exactly the supervisor's
formulation. Every earlier version covered the arcs **centred at `ψ`**, which are the *safe* sets.
**A cover by safe sets proves nothing**, and it is monotone the wrong way, so it kept reporting
"certified" out to `d = 3.5` where a clash in fact stops at `3.4555`.

**1.3 What exposed it.** Not Main's own checks. Two of Main's computations disagreed — the arc test
said "certified" at `d = 3.46`, a direct twist scan said otherwise — and reconciling X's `X-C051`
value (`3.4555003444`) with Main's `6/√5` showed the arithmetic was wrong too. **A certificate that
cannot fail is not a certificate**, and the scan's only value here was that it could disagree.

**1.4 The corrected certificate, and its confirmation.** Violation arcs are now the complement,
reduced into the five period cells of `R/(2π/5)` (exactly `2π = 5·(2π/5)`), endpoints shrunk inward
by `1e−30` so each piece is a strict subset:

| `d` | corrected arc test | independent twist scan | agree? |
| --- | --- | --- | --- |
| `2.0000` | cover | clash everywhere (`max min dist = 1.1255548`) | **yes** |
| `2.6000` | cover | `1.3712215` | **yes** |
| `3.0000` | cover | `1.6398674` | **yes** |
| `3.4000` | cover | `1.9539912` | **yes** |
| `3.4555` | cover | `1.9999997` | **yes** |
| `3.4600` | **no cover** | `2.0037512` | **yes** |
| `3.5000` | **no cover** | `2.0372311` | **yes** |

Bisection gives the threshold **`3.4555003444044642049`**, and X's `X-C051` `3.4555003444` agrees to
**ten significant figures**. Two independent methods now agree at every point tested, and an
independent worker's number is reproduced.

**1.5 Net effect on the claims.** `C116`'s constant is **reinstated as X's**: the two-dodecahedra
threshold is `3.4555003444…`, band `ε < 1.4555003444`, not `6/√5`. `C126`'s withdrawal of the *band*
is itself withdrawn; what it correctly recorded is that Main's `6/√5` was wrong. **Theorem D step (4)
is certified** by a sound certificate and independently by the scan. `C112`/`C123`/`C127` stay
`PENDING_REVIEW` — X's audit is the gate.

## 2. Attempt 1 (literature, stalled): the 13–20-face circumscribed-volume constants

For `K15-C122`'s extension (`c_F ≥ 4.958` for circumscribed polyhedra with `≤ 20` faces). Recorded as
`C125`. **Three independent reasons to stop:**

**(a) The constants are unproved for seven of the eight values needed.** `c_F` for `F = 4, 5, 6, 8,
10, 12, 14` is proved (Fejes Tóth, *Regular Figures* p. 263 Thm 2.1 and the Goldberg–Steinitz bound;
*Symmetry* **9** (2017) 41 for 8, 10, 14). For `F = 13, 15, 16, 17, 18, 19, 20` the optima are
**conjectures** — N. Mutoh, JCDCG, LNCS **2866** (2002) 204–214, computer-aided, `F = 4..30`.
Fejes Tóth's Theorem 2.1 itself does **not** give `c_F`: it is a two-sided bound in `(f, v, e, r, R)`
and depends on `v` and `e`, which are free for our cells.

**(b) The monotonicity `C122` assumed is false.** With inradius `1`: tetrahedron `13.8564` (4 faces),
cube `8.0000` (6), octahedron `6.9282` (8), **truncated octahedron `6.1584` (14)**, icosahedron
`5.0541` (20). The 14-face solid is **22% worse** than the 20-face one, so "more faces ⟹ smaller
minimum" fails and the target cannot be aimed at `F = 20` on that basis.

**(c) A count-based estimate cannot reach the threshold.** With tangency points `w_i`,
`V = (1/3)Σ_i ∫_{S_i} sec θ dσ` over the normal-fan tiling. For `F = 20` equal caps (angular radius
`0.451027`) this gives `V ≈ 4.413331`, **below** `C122`'s `4.957082`. The threshold would need the
minimiser to be `12%` *worse* than equal caps, and nothing here says so.

**Verdict: stop.** `G11` unaffected. Revival condition: a *proved* `c_F ≥ 4.958` for `F ≤ 20`, which
is exactly the open part of Mutoh's conjecture.

## 3. Attempt 2 (proof, succeeded): the near-contact bridge with no contact-density hypothesis

Review 0608: *"do not assume positive exact-contact density."* `C108`/`C114` did. `C124` removes the
hypothesis by a two-case split against the inball bound, and the missing implication is a counting
fact.

**The counting step.** Let `S_ε := {v : ∃w, 0 < |v−w| ≤ 2+ε}` and let `M` be a **maximal** matching of
the `(2+ε)`-graph. Every `v ∈ S_ε` is matched or adjacent to a matched vertex, so with `deg ≤ 12`,

```
|S_ε ∩ B| ≤ 2|M ∩ B| + 12·2|M ∩ B| = 26|M ∩ B| .
```

So `ρ_ε = 0` forces `S_ε` to have density zero — the pair bridge never needed `ρ_ε > 0`; where it
fails the packing is *asymptotically ε-loose*, which the trivial bound handles:

```
ρ_ε > 0 :  δ ≤ (4π/3)/(V_dod + δ₀(ε)ρ_ε) < 0.754697399337        (strict, via C108/C114)
ρ_ε = 0 :  δ ≤ 1/(1+ε/2)³  = 0.414086  at ε = 0.6832816          (explicit)
```

> **Theorem (`C124`).** Every saturated 2-separated packing in `R³` has `δ < 0.754697399337`
> **strictly**, with no hypothesis on contact density.

Three consequences. (i) **`G13` closes as a hypothesis** — nothing beyond saturation and separation is
assumed. (ii) **The dodecahedral bound is not attained**, restored on a sound proof: `C113` retracted
an earlier version of this because it used an invalid average-to-pointwise inference; the present
argument has no such step, bounding the density directly from the cell-volume sum in the `ρ_ε = 0`
branch. `G14` closes. (iii) **Still not a number**: `δ₀(ε)` is non-explicit, so branch 1 gives
strictness and no constant. **Nothing here is a new packing bound and `RESULTS.md` does not move.**

The `ε` needed is only `0.1967082337` (where the inball radius reaches `V_dod`'s threshold — the same
constant as `C119`), and the certified band supplies `1.4555`, **7.4× more room than required**.

## 4. Worker state, as evidenced

**C `cde39fa`** — broad near-contact scan, 284 instances, `t* = 0` everywhere. The supervisor's local
audit reports C rejects the isolated/edgeless witnesses and passes a 69-case API audit. Main's own
`D8` check of the previous repair (`C103`) is unchanged; **C's repair is under local audit and Main
does not re-certify it here.**

**E `d289bef`** — one full square degree of the family certified. The supervisor reports that an
**exact norm witness disproves E's general slack estimate**, and that an **unbounded five-centre cell
receives a finite enclosure near `4/3`**; both routed to E. Main records this without adjudicating —
it is E's and X's to settle — and **holds no certification claim that depends on it.** E's payer
value itself is independently reproduced by Main (`C118`, `1e−15`) and by X (`X-C055`, `1e−12`), and
its family scanned (`C120`), so the *fixture* is safe even though the *general estimate* is not.

**X `729df1e`** — `X-C043` verifies Theorem D step 4 to twelve digits and **resolves the E/Main twist
discrepancy** (different twist origins; both numbers right). `X-C051` gives the corrected threshold
(reproduced here to ten digits). `X-C052`/`X-C053` confirm A15 and the `C119`/`C122` arithmetic.
`X-C055` reproduces the payer fixture. X's full-hour audit now includes E's certifier.

**Held pending repair/audit:** `C106`, `C107`, `C108`, `C112`, `C114`, `C116`, `C123`, `C124`,
`C127` — every claim on the pair chain. Per review 0608 they stay `PENDING_REVIEW` until X checks the
exact statements.

## 4a. A by-product worth more than the repair: a ONE-PAIR certificate (`C128`)

Fixing `C127` made the arc cover *work*, and then showed it was wildly redundant: **one pair settles
the whole step.** With `a = A[1]`, `q = Q[8]`, `d = 2`,

```
R = 6.4 = 32/5,   c = (4−A)/R = −(3−√5)/2,   h = arccos(c) = 112.4555°,
|T| = 2π − 2h = 135.0890°  >  72° = the twist period,
```

and since the physical twist space is `R/(2π/5)` (a `72°` rotation about the shared vertex axis is a
symmetry of the icosahedron), `T` meets every coset of `72°`. So for every physical twist some
representative puts a point at distance `< 2` from `a`. Verified directly:
`max over τ of min over shifts of d²(τ + 72k°) = 1.266873708 < 4`.

**This is better than the cover** and should be the certificate of record. The cover needed the
mod-period reduction and a merge test — both of which had already produced two errors in this
object. The one-pair argument needs one algebraic identity (`R = 32/5`), one comparison
(`h < 4π/5 = 144°`) and the `72°` symmetry. **It is hand-checkable.**

## 4b. The band in CLOSED FORM — the hour's actual deliverable (`C129`)

`C128`'s one pair extends to the whole band in exact arithmetic, and the band end is a closed form.
In `v`'s frame take `a = (2/√5, 0, −4/√5)` and `q = (−2/√5, 0, 4/√5)` (both in the `xz`-plane, both of
norm 2). Then `u = w − a` has `u_y, u_z` independent of `d`, so

```
R = √(B² + C²) = 2·(4/√5)·(4/√5) = 32/5      — constant in d.
```

The violation set is `{|t−ψ| > h}`, `h = arccos((4−A(d))/R)`, and it covers every physical twist iff
`2π − 2h > 2π/5`, i.e. `h < 4π/5`, i.e. `(4 − A(d))/R > cos(4π/5) = −(1+√5)/4`. With
`x = d − 2/√5` this is the quadratic `x² − (4/√5)x + (8 − 8√5)/5 = 0`, so

> **`d_max = 4/√5 + 2√((2√5 − 1)/5) = 3.4555003444044642…`**

| closed form | bisection (`C127`) | X's `X-C051` |
| --- | --- | --- |
| `3.4555003444044642048` | `3.4555003444044642049` | `3.4555003444` |

agreement `4×10⁻¹⁵` / **ten significant figures**.

**Why this is the deliverable rather than the repair.** The arc cover needed covering, merging, a
`2π = 5·(2π/5)` reduction and an inward margin — and that machinery produced **two** errors
(`C126`, `C127`). The closed form needs one observation (`R = 32/5` is constant in `d`), one
trigonometric value (`cos 4π/5 = −(1+√5)/4`) and one quadratic. **Every step is hand-checkable**, it
confirms an independent worker's constant exactly, and it feeds `C124` with `7.40×` the room it
needs. `G15` is thereby downgraded: the mod-period reduction is no longer load-bearing.

## 5. What is standing, and what is not

**Proved and not in doubt:** `C094`/`C104` (Barlow cells, repaired), `C093`/`D18` (cut/flow),
`C115` (primary-source equality case), `C119`/`C125` (the locating bounds and the stalled branch),
`C121` (the explicit `≤ 12`-face stability bound).

**Proved but pending X:** `C124` (the contact-density-free strictness) and `C128` (the one-pair
certificate). **Open and recorded as `G15`:** whether the mod-period reduction inside the arc test is
sound for arcs longer than the period — it does not matter any more, because `C128` proves the
`d = 2` case without that machinery.

**Open:** an explicit `δ₀ > 0` (`G11`); the sharp `(L)`; the `13–20`-face constants (branch stopped);
`shell_check` soundness (`G12`).

**Not a bound.** `0.754697399337` remains the record to beat analytically; the best certificate is
`Δ ≤ 0.779966216777`, not an improvement on `0.779747`.

## 6. Honest accounting

**Repaired:** two soundness bugs of Main's own, both of which made a test report success (§1), found
only by cross-checking against an independent computation and against X's number. **Stalled, with
reasons:** the `13–20`-face branch (§2), three independent reasons, locators given. **Succeeded:**
`C124`, which removes the hypothesis the brief said not to assume and closes `G13` (as a hypothesis)
and `G14`. **Not achieved:** any number, any improvement over `0.754697399337`, any progress on the
sharp `2√32`. **Timing** is stated in the covering message as measured.
