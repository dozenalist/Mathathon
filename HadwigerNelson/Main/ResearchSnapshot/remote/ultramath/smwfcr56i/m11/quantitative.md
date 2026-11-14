# Explicit constants in the proof that chi(R^2) >= 6

Member m11, direction d9 (mandate K: quantitative). Three results, each with a complete
proof. Notation and numbering follow the paper (Sections 5.3, 8.5, Corollary 1.5).

* **Theorem B** — the paper's *absolute constant* `δ*` of Lemma 5.5 (binary-centre
  separation, Section 5.3) is made effective: **`δ* = 1/100` works**. The displayed
  inequality (5.10) is proved with `c_0 = 1/2`, `C_0 = 2`, `d_1 = 1/100`, and the
  Section 5.3 growth argument is replayed with `L = 1/4`. Displayed inequality
  (5.10) is the one place in Sections 5–8 where the paper introduces constants
  (`c_0, C_0, d_1`) that it does not compute and then *defines* a numerical
  `δ*` from them, so effectivising (5.10) effectivises §5.3.
* **Theorem A** — the exact three-colour analogue of Corollary 1.5 with the explicitly
  computed constant `δ_3 = 1/11`, using the paper's own seven-vertex Moser graph (8.5).
* **Proposition C** — at `k = 5` the constant of Corollary 1.5 is exactly `1/m*`,
  where `m*` is the least edge count of a finite non-5-colourable unit-distance graph.
  It is therefore *not extractable* from the paper: no finite non-5-colourable
  unit-distance graph is known. Any explicit `δ > 0` at `k = 5` is a new result.

Scripts: `exact2.py` (exact arithmetic in `Q(sqrt3, sqrt11)`), `moser_badness.py`
(exhaustive), `check_dstar.py` (numerical validation of every estimate of Theorem B).

---

# Theorem B. Lemma 5.5 holds with the absolute constant δ* = 1/100

**Statement.** Let `κ = π/3` and `S = S^1`. Fix two distinct labels `i^+, i^-`. Call
`x ∈ R^2` *binary* for that pair if `P_x(e) ∩ {i^+, i^-} ≠ ∅` for almost every
`e ∈ S`, where `P_x` are the maximal palettes of Definition 5.1. Then any two distinct
binary centres for the same pair satisfy `|x - y| >= 1/100`.

This is Lemma 5.5 of the paper with `δ* = 1/100` replacing "some `δ* > 0`".

## 0. What has to be supplied

The paper's proof of Lemma 5.5 (Section 5.3) is complete except that it invokes
displayed inequality (5.10) with four constants it never computes:

> there are absolute constants `c_0, C_0, d_1 > 0`, `d_1 < 1/2`, such that for
> `0 < d < d_1` and every real `t`, with `F_j(t) := jκ + F(t - jκ)`,
> ```
>  max_{0<=j<=5} (F_j(t) - t) >= c_0 d ,      max_{0<=j<=5} F_j'(t) >= 1 + c_0 d ,        (5.10a)
>  |F_j(t) - t| , |F_j'(t) - 1| , |F_j''(t)| <= C_0 d .                                   (5.10b)
> ```
> (Here `F = H - 2κ` and `H = α_+ ∘ α_-^{-1}`, with `α_±` as in (0.1).)

The paper then sets `L <= min{c_0/C_0, π/4}` and `δ* = min{d_1, (2C_0)^{-1}, L/(2C_0)}`.
Below, §3 proves (5.10) with `c_0 = 1/2`, `C_0 = 2`, `d_1 = 1/100`, and §4 replays
every numerical step of the paper's growth/distortion argument with `L = 1/4`,
`δ* = min{1/100, 1/4, 1/16} = 1/100`.

## 1. The maps and the exact identities used

For `0 < d < 1/2` and real `t`, writing `c = cos t`, `s = sin t`:

```
rho(t)  = |d + e^{it}| = sqrt(1 + 2 d c + d^2) ,
Theta(t)= t + arg(1 + d e^{-it})            (principal branch, |arg| < pi/2) ,        (0.1)
beta(t) = arccos(rho(t)/2) ,
alpha_±(t) = Theta(t) ± beta(t) ,   H = alpha_+ o alpha_-^{-1} ,   F = H - 2κ .
```

**(P1) `α_±` are smooth degree-one lifts of circle diffeomorphisms.**
`Theta(t+2π) = Theta(t) + 2π` because `d + e^{i(t+2π)} = d + e^{it}`; `rho, beta` are
`2π`-periodic. By Lemma B and Lemma C below, `alpha_±' > 0` for `d <= 1/100`. So each
`α_±` induces an orientation-preserving `C^∞` diffeomorphism of `S`, and `α_-^{-1}` is a
`C^∞` degree-one lift.

**(P2) The representation identity.** `e^{i alpha_+(t)} + e^{i alpha_-(t)} = d + e^{it}`.
Indeed `e^{i alpha_+} + e^{i alpha_-} = 2 cos(beta(t)) e^{i Theta(t)} = rho(t) e^{i Theta(t)}
= d + e^{it}`, since `2 cos(arccos(rho/2)) = rho` and `rho e^{i Theta} = d + e^{it}` by
definition of `Theta`. Hence, for `y = x + d`,
`y + e^{it} = x + e^{i alpha_+(t)} + e^{i alpha_-(t)}` exactly, with the two unit
directions non-parallel (`2 beta ∈ (0, π)` because `0 < rho < 2`). This is the identity
the paper states just before (5.9); `check_dstar.py` check (1) confirms it to `1e-15`.

**(P3) Exact form of `F`.** Put `σ = α_-^{-1}`. Since `α_+ = α_- + 2β`,

```
F(t) = α_+(σ(t)) - 2κ = t + 2 β(σ(t)) - 2κ .                                          (0.2)
```

**(P4) Derivatives.** With `τ = σ(t)`, chain rule in (0.2):

```
F'(t)  = 1 + 2 β'(τ) / α_-'(τ) ,                                                       (0.3)
F''(t) = ( 2 β''(τ) α_-'(τ) - 2 β'(τ) α_-''(τ) ) / α_-'(τ)^3 .                         (0.4)
```

(check_dstar.py checks (3),(4): finite differences agree with (0.3),(0.4) to `8e-10`.)

**(P5) The six maps.** `F_j(t) = jκ + F(t - jκ)`, so with `τ_j = t - jκ`

```
F_j(t) - t = F(τ_j) - τ_j ,   F_j'(t) = F'(τ_j) ,   F_j''(t) = F''(τ_j) .               (0.5)
```

Throughout, `0 < d <= 1/100` (so `d^2 <= 10^{-4}`) and `t ∈ R` is arbitrary.

## 2. Five elementary lemmas

**Lemma A (range of `rho`).** `1 - d <= rho <= 1 + d`, hence `0.989 <= rho <= 1.011`
and `|rho - 1| <= 1.02 d`.

*Proof.* `rho^2 = 1 + 2dc + d^2 ∈ [(1-d)^2, (1+d)^2]` and `rho > 0`, so
`1-d <= rho <= 1+d`; and `(1-d)^2 >= 1-2d`. Then `rho <= 1.01`, `rho >= 0.99`,
`|rho-1| <= d <= 1.02d`. ∎

**Lemma B (`Theta`).** With `phi(t) = Theta(t) - t = atan2(-d s, 1 + d c)` (note
`1 + d c >= 1 - d > 0`):

```
|phi| <= 1.02 d ,      Theta'(t) = 1 - d(c+d)/rho^2 ,      |Theta' - 1| <= 1.04 d ,
Theta''(t) = d s (rho^2 - 2d(c+d)) / rho^4 ,               |Theta''| <= 1.09 d .
```

*Proof.* `|atan(y/x)| <= |y|/x` for `x > 0` gives the first bound. Differentiating
`atan2(-ds, 1+dc)` gives the numerator `(-dc)(1+dc) - (-ds)(-ds) = -(dc + d^2)` over
`(1+dc)^2 + d^2s^2 = rho^2`. Then `|Theta'-1| = d(c+d)/rho^2 <= d(1+d)/(1-d)^2 <= 1.04 d`.
For the second derivative use `rho' = -ds/rho`:
`Theta'' = -d [ (-s)rho^2 - (c+d)·2rho·(-ds/rho) ] / rho^4 = d s [ rho^2 - 2d(c+d) ] / rho^4`,
and `|rho^2 - 2d(c+d)| <= 1.0201 + 0.0202`, `rho^4 >= 0.989^4 > 0.956`, so
`|Theta''| <= 1.09 d`. ∎

**Lemma C (`beta`).** Let `h(r) = 1/(r sqrt(4-r^2))`. Then

```
beta'(t)  = d s h(rho) ,                    |beta'| <= 0.586 d ,
beta''(t) = d c h(rho) - d^2 s^2 h'(rho)/rho ,   |beta''| <= 0.586 d + 0.41 d^2 ,
|beta - κ| <= 0.60 d ,                      |beta' - (d/sqrt3) s| <= 0.42 d^2 .
```

*Proof.* `beta = arccos(rho/2)`, `dbeta/drho = -1/sqrt(4-rho^2)`, `rho' = -ds/rho`, so
`beta' = d s / (rho sqrt(4-rho^2)) = d s h(rho)`. On `rho ∈ [0.989, 1.011]`,
`rho sqrt(4-rho^2) >= 0.989·sqrt(2.9799) > 1.708`, hence `|beta'| <= 0.586 d`.
Next `|beta - κ| <= |rho/2 - 1/2| / min_{|u|<=0.5055} sqrt(1-u^2) <= (0.51 d)/0.8628
<= 0.60 d`. Further `h'(r) = (2r^2-4)/(r^2 (4-r^2)^{3/2})`, so
`|h'| <= 2.044/(0.978·5.144) < 0.41` on that range, and
`beta'' = d c h + d s h' rho' = d c h - d^2 s^2 h'/rho` gives the displayed bound.
Finally `|h(rho) - h(1)| <= 0.41 |rho - 1| <= 0.42 d`, whence
`|beta' - (d/sqrt3)s| = d|s||h(rho) - h(1)| <= 0.42 d^2`. ∎

**Lemma D (second-order law for `2 beta`).**

```
| 2 beta(t) - 2κ + (2d/sqrt3) cos t |  <=  1.38 d^2 .
```

*Proof.* Substituting `u = 1/2 + v` in `arccos`,

```
beta(t) - κ = - ∫_0^{Phi} g(v) dv ,     g(v) = (1 - (1/2+v)^2)^{-1/2} ,   Phi = (rho-1)/2 ,
```

so `g(0) = 2/sqrt3` and

```
2 beta(t) - 2κ = -(4/sqrt3) Phi - 2 ∫_0^{Phi} ( g(v) - g(0) ) dv ,
-(4/sqrt3) Phi = -(2/sqrt3)(rho - 1) = -(2/sqrt3)(2dc + d^2)/(rho + 1) .
```

Therefore

```
-(2/sqrt3)(rho-1) + (2d/sqrt3) c = -(2/sqrt3) · ( d c (1 - rho) - d^2 ) / (rho + 1) ,
```

of modulus at most `(2/sqrt3)(1.02 d^2 + d^2)/1.989 <= 1.18 d^2`.
And `|g(v) - g(0)| <= |v| sup|g'|`, while
`g'(v) = (1/2+v)(1-(1/2+v)^2)^{-3/2}`; on `|v| <= |Phi| <= 0.51 d <= 0.0051` we get
`sup|g'| <= 0.5051 · (0.74487)^{-3/2} <= 0.786`, so the integral term is at most
`0.786 (0.51 d)^2 <= 0.21 d^2`. The two bounds add to `<= 1.39 d^2`; keeping the
digits, `1.172 + 0.204 = 1.376 <= 1.38`. ∎

**Lemma E (`alpha_-` and its inverse).** For all `t`, with `u = t + κ` and
`tau = σ(t) = α_-^{-1}(t)`:

```
|alpha_-'(t) - 1| <= 1.63 d ,     |alpha_-''(t)| <= 1.68 d ,     |tau - u| <= 1.65 d .
```

*Proof.* `alpha_-' = Theta' - beta'` and `alpha_-'' = Theta'' - beta''`, so Lemmas B
and C give `|alpha_-'-1| <= 1.04d + 0.586d = 1.63d` and
`|alpha_-''| <= 1.09d + 0.586d + 0.0041d <= 1.68d`. For the last claim,
`alpha_-(u) - t = alpha_-(u) - (u - κ) = (Theta(u)-u) + (κ - beta(u))`, so
`|alpha_-(u) - t| <= 1.02d + 0.60d = 1.62d`; and `alpha_-' >= 1 - 1.63d >= 0.9837`.
Hence `|tau - u| = |alpha_-^{-1}(t) - alpha_-^{-1}(alpha_-(u))| <= 1.62d/0.9837 <= 1.65d`. ∎

**Lemma F (six equally spaced angles).** For every real `theta` and `k = 0,...,5` the set
`{theta + kπ/3}` is six points equally spaced by `π/3`, and

```
max_{0<=k<=5} ( - cos(theta + kπ/3) )  >=  sqrt3/2 ,      max_{0<=k<=5} sin(theta + kπ/3) >= sqrt3/2 .
```

*Proof.* The arcs `[-π/6, π/6] + kπ/3` tile the circle, so one of the six points has
argument within `π/6` of `0`; there `cos >= cos(π/6) = sqrt3/2`, so `-cos <= -sqrt3/2`.
Likewise the arcs `[π/3, 2π/3] + kπ/3` tile the circle, so one point has argument within
`π/6` of `π/2`, where `sin >= sin(π/3) = sqrt3/2`. ∎

## 3. Proof of (5.10) with c_0 = 1/2, C_0 = 2, d_1 = 1/100

Fix `t` and `j ∈ {0,...,5}`; put `tau = t - jκ`, `u = tau + κ = t + (1-j)κ`, and
`tau' = σ(tau)`, so `|tau' - u| <= 1.65 d` by Lemma E. Both `cos` and `sin` are
1-Lipschitz, so `cos tau' <= cos u + 1.65d` and `sin tau' >= sin u - 1.65d`.

**(a) Displacement (5.10a, first half).** By (0.5), (0.2), Lemma D at `tau'`, and
Lemma A:

```
F_j(t) - t = 2 beta(tau') - 2κ
           >= -(2d/sqrt3) cos(tau') - 1.38 d^2
           >= -(2d/sqrt3) cos u - (2/sqrt3)(1.65 d^2) - 1.38 d^2
           >= -(2d/sqrt3) cos u - 3.30 d^2 .
```

`u = t + (1-j)κ` with `j` running over six consecutive integers, so by Lemma F
`max_j ( - cos u_j ) >= sqrt3/2`. Hence

```
max_j ( F_j(t) - t ) >= (2d/sqrt3)(sqrt3/2) - 3.30 d^2 = d - 3.30 d^2 >= d/2 = c_0 d ,
```

since `d <= 1/100` gives `3.30 d <= 0.033 <= 1/2`.

**(b) Derivative (5.10a, second half).** By (0.5) and (0.3),
`F_j'(t) = 1 + 2 beta'(tau')/alpha_-'(tau')`. Write
`1/alpha_-' = 1 + (1 - alpha_-')/alpha_-'`; Lemma E gives
`|(1 - alpha_-')/alpha_-'| <= 1.63d/0.9837 <= 1.66 d`, while `|2 beta'(tau')| <= 1.172 d`
by Lemma C. Hence

```
| F_j'(t) - 1 - 2 beta'(tau') | <= 1.172 · 1.66 d^2 <= 1.95 d^2 .
```

Next, Lemma C gives `|2 beta'(tau') - (2d/sqrt3) sin tau'| <= 0.84 d^2`, and
`(2d/sqrt3)|sin tau' - sin u| <= (2/sqrt3)(1.65 d^2) <= 1.91 d^2`. Therefore

```
F_j'(t) >= 1 + (2d/sqrt3) sin u - (1.95 + 0.84 + 1.91) d^2 = 1 + (2d/sqrt3) sin u - 4.70 d^2 ,
```

and Lemma F gives `max_j F_j'(t) >= 1 + d - 4.70 d^2 >= 1 + d/2 = 1 + c_0 d`.

**(c) The `C_0 d` bounds (5.10b).** By Lemma D, `|F_j(t) - t| <= (2/sqrt3)d + 1.38 d^2 <=
1.16 d <= 2 d`. By Lemma E, `|F_j'(t) - 1| <= 1.172 d/0.9837 <= 1.20 d <= 2 d`. By (0.4)
with Lemmas C and E, `|2 beta''| <= 1.172d + 0.82 d^2`, `|alpha_-'| <= 1.02`,
`|2 beta'| <= 1.172 d`, `|alpha_-''| <= 1.68 d`, `|alpha_-'|^3 >= 0.964`, so

```
|F_j''(t)| <= (1.172 d · 1.02 + 1.172 d · 1.68 d) / 0.964 <= 1.26 d <= 2 d .
```

**Conclusion of §3.** Displayed (5.10) holds with `c_0 = 1/2`, `C_0 = 2`, `d_1 = 1/100`.
`check_dstar.py` check (6) reports, at `d = 1/100`, `min_t max_j (F_j-t)/d = 1.0001`,
`min_t max_j (F_j'-1)/d = 1.0034`, `sup|F-t|/d = 1.157`, `sup|F'-1|/d = 1.161`,
`sup|F''|/d = 1.170`: the constants above are valid and far from tight.
`check_dstar.py` check (5) confirms the paper's first-order law (5.9):
`sup_t |F(t) - t - (2d/sqrt3) sin(t - π/6)| <= 0.71 d^2`.

*Remark on optimality.* The constants `1/2, 2, 1/100` are chosen to make the proof
transparent, not to be optimal: the observed values at `d = 1/100` are `c_0 ≈ 1.000`,
`C_0 ≈ 1.18`, and they remain (numerically) valid up to `d = 0.1`. A sharper `δ*`
(morally `1/20`) is therefore available from the same proof with more careful
bookkeeping; `δ* = 1/100` already suffices, since the paper uses only `δ* > 0`.

## 4. Section 5.3 of the paper with δ* = 1/100

Take `L = 1/4` and `δ* = min{d_1, (2C_0)^{-1}, L/(2C_0)} = min{1/100, 1/4, 1/16} = 1/100`.
Let `x ≠ y` be binary for the same pair, `d = |y - x| ∈ (0, δ*)`, and rotate so that
`y - x = d`. By (P1),(P2) the hypotheses of Lemma 5.2 are met with both endpoint maps
`α_±` local diffeomorphisms; the paper's palette-transport step then produces a
measurable `2π`-periodic `s = s_x : R → {±1}` with

```
s(t + κ) = - s(t)   a.e.        and        s ∘ H = s   a.e.                            (5.8)
```

(the second because `s(α_+(t)) = s(α_-(t))` a.e. and `α_+ = H ∘ α_-` a.e., with `α_-` a
diffeomorphism). Since `s(u + 2κ) = s(u)`, (5.8) gives `s ∘ F = s` a.e. Consequently,
using `s(t - jκ) = (-1)^j s(t)`,

```
s( F_j(t) ) = s( jκ + F(t-jκ) ) = (-1)^j s( F(t-jκ) ) = (-1)^j s(t-jκ) = (-1)^{2j} s(t) = s(t)
```

almost everywhere, for every `j`. So `A := {t : s(t) = 1}` is `2π`-periodic, has measure
`π` in every period, and is invariant under every `F_j` up to a null set.

Now the paper's argument verbatim, with our constants. Every numerical step:

1. `|F_j' - 1| <= C_0 d <= 0.02`, so `0.98 <= F_j' <= 1.02`: every `F_j` and its inverse
   is bi-Lipschitz, and `|(log F_j')'| = |F_j''/F_j'| <= C_0 d/(1 - C_0d) <= 2 C_0 d`.
2. **Growth.** Let `I_0` have length `ℓ_0 < L = 1/4`. Suppose `I_r` has length
   `ℓ_r < L`. Since `L = 1/4 = c_0/C_0`, (5.10a) at the midpoint `m_r` of `I_r` gives
   `j_r` with `F_{j_r}'(m_r) >= 1 + c_0 d`; set `I_{r+1} = F_{j_r}(I_r)`. For `t ∈ I_r`,
   Taylor from the midpoint and (5.10b) give
   `F_{j_r}'(t) >= 1 + c_0 d - C_0 d |t - m_r| >= 1 + c_0 d - C_0 d ℓ_r/2 >= 1 + (c_0/2) d =: λ`,
   using `ℓ_r <= L = c_0/C_0`. So `λ > 1` and `ℓ_{r+1} >= λ ℓ_r`. The process stops at
   the first `N` with `ℓ_N >= L`, and then `L <= ℓ_N <= (1 + C_0 d) L`.
3. **Distortion.** For `G = F_{j_{N-1}} ∘ ... ∘ F_{j_0}`, the chain rule and step 1 give
   `osc_{I_0} log G' <= 2 C_0 d ∑_{r<N} ℓ_r <= 2 C_0 d · ℓ_N/(λ - 1)
   <= 2C_0 d (1+C_0d)L/((c_0/2)d) = 4C_0(1+C_0d)L/c_0 <= 4.1`.
   So `D := exp(4.1)` bounds `sup_{I_0} G' / inf_{I_0} G'` uniformly in `I_0`, `N`, `d`.
4. **Density point.** `|A| = π > 0`, so `A` has a Lebesgue density point with centred
   intervals `I_0` satisfying `|I_0 \ A|/|I_0| → 0`. The invariance of `A` under `G` up to
   null sets and the distortion bound give
   `|G(I_0) \ A|/|G(I_0)| <= D |I_0 \ A|/|I_0| → 0`. The intervals `J_n = G(I_0)` have
   lengths in `[L, (1+C_0d)L]`; after translation by multiples of `2π` a subsequence
   converges to an interval `J = [a,b]` with `b - a >= L` and `|J \ A| = 0`.
5. **Extension.** By (5.10a) choose `j` with `F_j(b) - b >= c_0 d`, so `F_j(b) >= b + c_0d`.
   Also `F_j(a) <= a + C_0 d <= a + 0.02 < a + L <= b`. Hence `F_j([a,b])` is conull in
   `A`, it overlaps `[a,b]`, and their union contains `[a, F_j(b)]`, a conull interval whose
   right endpoint advanced by at least `c_0 d`. Iterating with the same left endpoint
   yields, after finitely many steps, a conull interval of length `>= 2π`.
6. By periodicity `A` then has full measure in a period, contradicting `|A| = π < 2π`.

Hence no `0 < d < δ* = 1/100` occurs, i.e. `|x - y| >= 1/100`. ∎

## 5. Effect on the paper

Only positivity of `δ*` is used downstream: Proposition 5.6 needs that infinitely many
binary centres on the compact circle `x + S^1` cannot be `δ*`-separated. So Lemma 5.5,
Proposition 5.6, and therefore Sections 6–8 become effective in this explicit constant.
No statement is weakened and no hypothesis is added.

---

# Theorem A. Exact three-colour badness: the k = 3 analogue of Corollary 1.5, δ_3 = 1/11

Let `E(2)` be the isometry group of the plane, `R^2 = C`, and `µ` a normalized finitely
additive left-invariant measure on **all** subsets of `E(2)`.

**Theorem A.** For every `c : R^2 → {1,2,3}`,

```
p_3(c) := µ{ T ∈ E(2) : c(T^{-1}0) = c(T^{-1}1) }  >=  1/11 .
```

The constant is the exact value of the paper's formula `δ = 1/m` for the seven-vertex
graph (8.5). It is best possible *for this witness*: some 3-colouring of the graph has
exactly one monochromatic edge, so the averaging argument cannot give more than `1/11`
from `G`. (We do not claim that `inf_c p_3(c) = 1/11` for the plane; that is a separate
question.)

**The graph.** `G = {0, A, B, T, uA, uB, uT}` with `A = (√3+i)/2`, `B = (√3-i)/2`,
`T = √3`, `u = (5 + i√11)/6`, and the eleven edges
`0A, 0B, AB, TA, TB, uAuB, 0uA, 0uB, uTuA, uTuB, TuT`.
`exact2.py` verifies in exact arithmetic in `Q(√3,√11)` (exact `Fraction` coefficients,
rigorous rational enclosures of `√3, √11, √33`) that all eleven edges have `|·|^2`
**exactly** `1`. `G` is not 3-colourable: `{0,A,B}` and `{T,A,B}` are equilateral of
side 1, so `c(0) = c(T)`; `{0,uA,uB}` and `{uT,uA,uB}` are equilateral of side 1, so
`c(0) = c(uT)`; but `|T - uT|^2 = 3|1-u|^2 = 3·(12/36) = 1`, so `c(T) ≠ c(uT)`.

**Lemma A1 (averaging).** Let `H` be a finite unit-distance graph with vertex set
`v_1,...,v_n ⊂ R^2` and `m >= 1` edges, and let
`β_k(H) = min over k-colourings χ of H of (1/m)·#{edges of H monochromatic under χ}`.
Then for every `c : R^2 → {1,...,k}` and every `µ` as above,

```
(1/m) ∑_{(i,j) ∈ E(H)} µ{ T : c(T^{-1}v_i) = c(T^{-1}v_j) }  >=  β_k(H) .          (A.1)
```

*Proof.* For each `T`, `v ↦ c(T^{-1}v)` is a `k`-colouring of `H`, so at least
`β_k(H)·m` of the `m` summands `1[c(T^{-1}v_i) = c(T^{-1}v_j)]` equal `1`. Average this
finite sum against the finitely additive, normalized `µ`; only finite additivity is used. ∎

**Lemma A2 (all unit pairs have the same badness).** For each edge `(v_i,v_j)` of `H`,

```
µ{ T : c(T^{-1}v_i) = c(T^{-1}v_j) } = p_k(c) .
```

*Proof.* Choose `S ∈ E(2)` with `S^{-1}v_i = 0` and `S^{-1}v_j = 1` — possible because
`|v_i - v_j| = 1 = |1 - 0|`. For every `T ∈ E(2)`, `(S∘T)^{-1}v_i = T^{-1}0` and
`(S∘T)^{-1}v_j = T^{-1}1`. Hence
`S·{T : c(T^{-1}0) = c(T^{-1}1)} = {T : c(T^{-1}v_i) = c(T^{-1}v_j)}`, and
left-invariance of `µ` gives equality of the two measures. ∎

**Proof of Theorem A.** Apply A1 and A2 to `G` with `k = 3`: `m = 11`, and
`β_3(G) = 1/11`. `moser_badness.py` enumerates all `3^7 = 2187` 3-colourings of `G`; the
minimum number of monochromatic edges is `1`, attained `132` times, with distribution
`1:132, 2:342, 3:666, 4:456, 5:336, 6:144, 7:60, 8:48, 11:3`. This gives
`p_3(c) >= 1/11`. ∎

*Remark.* Corollary 1.5 of the paper is the same argument at `k = 5`, with the single
difference that no finite non-5-colourable unit-distance graph is known.

---

# Proposition C. Why the constant of Corollary 1.5 cannot be extracted

For `k >= 1` let `m*(k) = min{|E(H)| : H a finite unit-distance graph, χ(H) > k}`
(`= ∞` if none exists), and `δ*(k) = inf_c p_k(c)`.

**(i)** `δ*(k) >= sup_H β_k(H) >= 1/m*(k)`, the sup over finite unit-distance graphs `H`.
*Proof.* Lemma A1 with Lemma A2 says `p_k(c) >= β_k(H)` for every `H` and every `c`. ∎

**(ii)** Corollary 1.5 produces `δ = 1/m` with `m = |E(H)|` for the graph `H` that
de Bruijn–Erdős compactness supplies from Theorem 1.1. That step is non-constructive: `H`
is not exhibited and `m*(5)` is unknown. The paper's own words: "The graph and the
positive constant here are existential."

**(iii)** Consequences.
* `k = 3`: `m*(3) <= 11`, and `1/11` is exactly the value of the paper's formula for the
  paper's own graph; this is Theorem A, with a complete proof.
* `k = 4`: the literature cited by the paper (Heule; Parts) gives `m*(4) <= 553`,
  `<= 509`, but those coordinates are not reproduced here, so we claim no explicit `δ_4`.
* `k = 5`: `m*(5) < ∞` by Theorem 1.1 plus compactness, but no finite non-5-colourable
  unit-distance graph has ever been written down. Hence **any explicit `δ > 0` for
  Corollary 1.5 is a new result**; by (i) it is a quantitative strengthening of the
  finite-witness problem, which is exactly the sense in which mandate K's target is hard.

**No-go for the direction as literally stated.** One cannot read an explicit `δ` out of
the paper: Sections 2–8 prove "no weak measurable 5-colouring" by contradiction, and the
only route from there to badness (Corollary 1.5) goes through graph compactness, which is
non-effective. So `δ` is not a constant that was left unoptimised — there is nothing in
the text to optimise. The two constants of the paper that *can* be made effective are
`δ*` of Lemma 5.5 (Theorem B) and the seven-point Moser certificate of Lemma 8.9,
verified exactly below.

---

# Constants table (mandate K)

| constant | in the paper | value established here | status |
|---|---|---|---|
| `c_0, C_0, d_1` of (5.10) | "absolute constants" | `1/2`, `2`, `1/100` | §3, proved |
| `L` of Section 5.3 | any `<= min{c_0/C_0, π/4}` | `1/4` | §3–§4 |
| `δ*` of Lemma 5.5 | "an absolute constant `> 0`" | **`1/100`** | Theorem B |
| `C` in `Lip(p_i^ε) <= C/ε` (§7.1) | "an absolute constant" | `4` | one line below |
| `δ` of Corollary 1.5 | `1/m`, `m` existential | `1/m*(5)`, not computable | Proposition C |
| `δ_3` (analogue of Cor 1.5) | — | **`1/11`**, exact | Theorem A |
| (8.5)–(8.6), (8.4) Moser placement | rational certificate | verified exactly | `exact2.py` |

`C = 4`: for measurable `f` with `0 <= f <= 1`,
`p^ε(q) = (πε^2)^{-1} ∫_{B(0,ε)} f(q+v) dv` satisfies
`|p^ε(q) - p^ε(q')| <= |B(0,ε) △ B(q'-q,ε)| / (πε^2) <= (2|q - q'| · 2πε)/(πε^2) = 4|q-q'|/ε`,
because the symmetric difference of two radius-`ε` discs at distance `h` has area `<= 2h·2πε`.

---

# Files and check commands

```
python3 check_dstar.py    # validates (P2),(P3),(P4), the paper's (5.9), and every
                          # bound of Section 3 and of Lemmas B,C,D,E at d = 1/100
python3 exact2.py         # exact Q(sqrt3,sqrt11) verification: the eleven unit edges of
                          # (8.5) and the region (8.4) at all seven points of (8.6)
python3 moser_badness.py  # beta_3 of the seven-vertex graph = 1/11 (exhaustive 3^7)
```
