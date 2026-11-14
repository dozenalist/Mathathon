# Independent audit of §§5–8 of "The Euclidean plane is not five-colorable" (OpenAI, 23 Sep 2026)

Member m6, swarm smwfcr56i. Direction d2: exact finite-core audit of §§5–8.

**Headline verdict: no defect found in §§5–8. Every finite and every quantitative step that
I restated precisely and re-derived mechanically is correct, including the two places where
the paper delegates a computation. Three cosmetic errata are listed in §6.**

Everything below was re-derived from the paper's own statements; nothing was taken on trust
from the paper, from the Lean bundle, or from the board.

---

## 1. The finite geometric certificate of §8.5–8.6 (the load-bearing finite object)

### 1.1 Exact coordinates, exactly eleven unit edges, no merged vertices

Eq. (8.5): `A = (√3+i)/2`, `B = (√3−i)/2`, `T = √3`, `u = (5+i√11)/6`,
`G = {0, A, B, T, uA, uB, uT}`.

Computed in the exact field `K = Q(√3,√11)` (elements `a0 + a1√3 + a2√11 + a3√33`, `a_i ∈ Q`):
the pair `(√3+i)/2, (√3−i)/2` gives `√3/2 ± i/2`; the products are

```
uA = ((5√3 − √11)/12, (√33 + 5)/12)
uB = ((5√3 + √11)/12, (√33 − 5)/12)
uT = (5√3/6, √33/6)
```

(these match the paper's displayed `uA, uB, uT`). Over all 21 pairs:

* exactly **11** pairs have squared distance exactly `1` — namely
  `0A, 0B, 0uA, 0uB, AB, AT, BT, T·uT, uA·uB, uA·uT, uB·uT` — the eleven edges of Figure 3;
* the other **10** pairs have exact squared distance
  `3, 3, 1/3, 7/6 − √33/6, 3/2 − √33/6, 7/6 + √33/6, 1/3, 3/2 + √33/6, 3/2 + √33/6, 3/2 − √33/6`,
  none of which is `1`; in particular all ten are `> 0`, so the seven points are **pairwise distinct**
  (no duplicated or merged vertices);
* `|u|² = (25+11)/36 = 1` and `|T − uT|² = 3|1−u|² = 3·12/36 = 1`, both exact.

### 1.2 Non-3-colourability — three independent proofs

1. **Exhaustive**: all `3^7 = 2187` colourings of the 7 vertices were checked against the eleven
   edges; **0** are proper.
2. **Forcing chain** (the paper's argument, fully expanded): the triangles `{0,A,B}` and `{T,A,B}`
   share the edge `AB`, so in a proper 3-colouring both `c(0)` and `c(T)` must equal the unique
   element of `Fin 3 \ {c(A), c(B)}`; hence `c(0) = c(T)`. The triangles `{0,uA,uB}` and
   `{uT,uA,uB}` share the edge `uA·uB`, so `c(0) = c(uT)`. Then `c(T) = c(uT)`, contradicting
   `|T − uT| = 1`. Note the two diamonds (`{0,A,B,T}` and `{0,uA,uB,uT}`) use 3 new vertices each,
   so the construction needs exactly `4 + 3 = 7` vertices.
3. **In Lean 4 / Mathlib** (see §2).

### 1.3 The placement (8.6) and the strict-membership certificate (Lemma 8.9)

The typesetting of (8.6) is `z_g = (35+12i)/37 · g + (−290+149i)/250` in flat text; the
parenthesisation that is consistent with Table 1, Table 2 **and** the displayed residual table is

```
z_g = ((35+12i)/37) · ( g + (−290+149i)/250 ),      |(35+12i)/37| = 1  since 35²+12² = 37².
```

For `g = 0` this gives `z_0 = −11938/9250 + i·1735/9250 = (−1.290595…, 0.187568…)`, matching
Table 1's `(−1.2906, 0.1876)`; the other parenthesisation gives `(−1.16, 0.596)` and matches
nothing. **I reproduced all seven entries of the paper's residual table exactly**
(denominators `710400000000`, numerators as printed), which pins the formula down beyond doubt.

Exact values (verified twice: symbolically in `K`, and by rigorous rational interval arithmetic
at 40 decimal digits with brackets for `√3, √11` verified by exact squaring):

| g | ξ | υ | `|z_g|²` exactly | `P` | `P'` |
|---|---|---|---|---|
| 0 | −1.2905945946 | 0.1875675676 | `106301/62500` | 0.8661244194 | 1.3889728356 |
| A | −0.6335435370 | 0.9414136445 | `206051/62500 − (29/25)√3` | 0.0895503190 | 0.1197727189 |
| B | −0.3092192126 | −0.0045323015 | `131551/62500 − (29/25)√3` | 0.0000016900 | 0.0006983199 |
| T | 0.3478318450 | 0.7493137754 | `293801/62500 − (58/25)√3` | 0.0221254901 | 0.0265819267 |
| uA | −1.1597561444 | 1.1789712694 | `149882/46875 − (29/30)√3 + (29/150)√11 + (149/1500)√33` | 9.7252412566 | 19.4762921470 |
| uB | −0.3665945783 | 0.5699599968 | `206639/93750 − (29/30)√3 − (29/150)√11 + (149/1500)√33` | 0.0019926823 | 0.0250709836 |
| uT | −0.2357561281 | 1.5613636986 | `293801/62500 − (29/15)√3 + (149/750)√33` | 12.5743610605 | 13.0225720287 |

where `P = υ²(3ξ²−υ²)²` and `P' = l³(1−l/4)(l−1)²`, `l = ξ²+υ²`.

**Result: for all seven vertices `0 < |z_g|² < 4` and `P < P'` (8.4).** With the paper's
`h = 0.00011`, `P⁺ < P'⁻` in all seven rows, and the box `(a,b)` of Table 2 contains the exact
`|z_g|²` in all seven rows, and `(a,b) ⊂ (0,4)` avoiding `1`, in all seven rows.

This fills in the paper's own gap: §8.6 says of the rational box certificate *"The other six rows
give the corresponding displayed strict bounds by the same two products"* and prints only the last
row. All six remaining rows are now checked explicitly.

### 1.3′ A decimal-free certificate (sharper than the paper's)

`exact_certificate.py` gives, for each vertex, an explicit **rational** lower bound for
`P' − P` and for `min(|z_g|², 4 − |z_g|²)`, obtained from the rational brackets

```
108253175473/62500000000 < √3  < 1732050807569/1000000000000       (lo² ≤ 3 ≤ hi² exact)
663324958071/200000000000 < √11 < 829156197589/250000000000        (lo² ≤ 11 ≤ hi² exact)
```

by exact `Fraction` interval arithmetic — no decimal approximation enters the certificate, and the
validity of the brackets is a matter of squaring integers. The resulting lower bounds are

```
P' − P  >  0.52284842 (g=0),  0.03022240 (A),  0.00069663 (B),  0.00445642 (T),
           9.75105089 (uA),  0.02307830 (uB),  0.44821095 (uT)          [exact rationals]
|z_g|²  >  1.70081600 (0), 1.28763706 (A), 0.09563706 (B), 0.68245813 (T),
           2.73500757 (uA), 0.45924598 (uB), 2.49343755 (uT)
4 − |z_g|² > 2.29918400 (0), …, 0.50656245 (uT)
```

(the printed script gives the exact fractions as well). So Lemma 8.9 does not need decimal
arithmetic at all: seven rational lower bounds settle it.

### 1.4 Lemma 8.8's region algebra

Checked by hand and symbolically: `sin 3φ = υ(3ξ²−υ²)/l^{3/2}`, `sin(3δ) = √(1−l/4)(l−1)` with
`cos δ = r/2`, and `sin3(φ−δ)sin3(φ+δ) = sin²3φ − sin²3δ`. So (8.4) `⟺` that product is negative
`⟺` the two endpoint directions lie strictly in opposite sectors, and `0 < l < 4`, `l ≠ 1` give
`δ ∈ (0, π/2)` so the two directions are nonparallel with `sin 2δ ≠ 0`. All of this is as claimed.

---

## 2. Machine-checked Lean 4 formalisation of §1

`OAI_Audit_Moser.lean` (this directory) compiles under the local toolchain
**Lean 4.33.1 + Mathlib**, in ~7 s, with **no `sorry`, no `axiom`, no `native_decide`,
no `implemented_by`, no `opaque`**:

```
$ lean OAI_Audit_Moser.lean
'OAI.Audit.Moser.edges_unit'              depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Audit.Moser.nonedges_not_unit'       depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Audit.Moser.P_injective'             depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Audit.Moser.not_three_colorable'     depends on axioms: [propext]
'OAI.Audit.Moser.placed_edges_unit'       depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Audit.Moser.placed_nonedges_not_unit' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Audit.Moser.Q_injective'             depends on axioms: [propext, Classical.choice, Quot.sound]
```

* `edges_unit : ∀ a b : Fin 7, Adj a b → dist (P a) (P b) = 1`
* `nonedges_not_unit : ∀ a b : Fin 7, ¬ Adj a b → dist (P a) (P b) ≠ 1`
* `P_injective : Function.Injective P`
* `not_three_colorable : ¬ ∃ c : Fin 7 → Fin 3, ∀ a b, Adj a b → c a ≠ c b`
* `placed_edges_unit`, `placed_nonedges_not_unit`, `Q_injective` — the same facts for the
  **placed** points `Q g = μ·(P g + τ)` of (8.6), using `‖μ‖ = 1` so `dist (Q a) (Q b) = dist (P a) (P b)`.
  The only thing about §8.5 that is *not* in Lean is the region membership (8.4), which is
  verified exactly in `verify_sec8.py` / `exact_certificate.py`.

`P` carries the paper's exact coordinates (`Real.sqrt 3`, `Real.sqrt 11`); `Adj` is the eleven-edge
relation. The proof of `not_three_colorable` is the paper's forcing chain, via
`fin3_third : a ≠ b → x ≠ a → x ≠ b → y ≠ a → y ≠ b → x = y` on `Fin 3`.

This is a Lean proof of the *statement* Proposition 8.10 needs (a 4-chromatic unit-distance graph),
not a port of the paper's bundle and not a weakening of anything.

---

## 3. The uniform expansion (5.9) and the constants (5.10) of §5.3 — verified symbolically

Lemma 5.5 (binary-centre separation, `δ_*`) is what forces `|P_x(e)| ≤ 2` in Proposition 5.6, so
its quantitative content is load-bearing for everything in §§6–8. Re-derived with `sympy` from the
definitions `Θ_d(t) = t + Im log(1+de^{−it})`, `α_± = Θ_d ± arccos(|d+e^{it}|/2)`:

```
a_+(t) = −sin t − cos t/√3          (d-coefficient of α_+(t) − (t+κ))        ✓ paper
a_−(t) = −sin t + cos t/√3          (d-coefficient of α_−(t) − (t−κ))        ✓ paper
F(t) = t + d·(a_+(t+κ) − a_−(t+κ)) + O(d²)
     = t + (2d/√3) sin(t − π/6) + O(d²) = t − (2d/√3) cos(t+κ) + O(d²)      ✓ (5.9)
min_t max_{0≤j≤5} sin(t − jπ/3 − π/6) = min_t max_j cos(t − jπ/3 − π/6) = √3/2   ✓ (5.10)
```

Two things worth recording.

* The substitution is delicate: **`a_+(t) − a_−(t+κ)` vanishes identically**, so had the paper
  written `a_+(t)` instead of `a_+(t+κ)` the whole `O(d)` term would have cancelled and (5.10)
  would be false. I confirmed the printed form is the correct one (`a_−∘`-inverse contributes the
  `κ`-shift). This is a place where the argument could easily have been wrong and is not.
* Full nonlinear check: solving `α_−(u) = t` by Newton at 40 digits, the ratio
  `|F(t) − t − d·(2/√3)sin(t−π/6)| / d²` is bounded by `0.723` uniformly over a `t`-grid and
  `d = 10^{-1},…,10^{-4}`, so the `O(d²)` remainder of (5.9) is uniform and (5.10) holds with
  `c_0 = 1 − O(d)`, `C_0` absolute.

---

## 4. Finite combinatorics of §§8.2, 8.3, 8.5, 6.3.4 — exhaustively checked

All statements below were restated as exact finite claims and decided by exhaustive enumeration
(`verify_combinatorics.py`); none depends on measure theory.

**(a) §8.2 five-cycle signs.** Over all `2^5 = 32` sign patterns of the 5-cycle with
`I(σ) = {i : σ_{i−1}=σ_i=+1}`, `O(σ) = {i : σ_{i−1}=σ_i=−1}`: `I ≠ ∅` **and** `O ≠ ∅` **⟺**
`σ` is one `+` run and one `−` run of lengths `2` and `3` in some order (the paper's counting
argument: two runs of each kind would occupy ≥ 6 > 5 edges). ✓ For each of the 10 qualifying
patterns every allowed palette option is a diagonal `D_x = {x,x+2}`, the index difference inside
the option set is `±2` mod 5, and **`options(σ) = options(−σ)`** — the antipodal claim of §8.2. ✓

**(b) §8.2 closing word argument.** Over all `5^6 = 15625` words `p : Z/6 → Z/5` there is **no**
word with `p_{j+1} − p_j = ±1` for all `j` (disjointness of neighbouring palettes, from (5.7)) and
`p_{j+3} − p_j ∈ {0,±2}` for all `j` (identical option sets at `e` and `−e`). ✓
The excluded sums of three steps are `{−3,−1,1,3}`, whose residues mod 5 are `{1,2,3,4}` — never 0,
and `±2` mod 5 forces `±3`, i.e. all three signs equal, exactly as the paper argues.

**(c) §8.3/8.5 six-position words.** Over `{X,U,V}^6` with *adjacency inequality* and
*antipodal equality when both non-`X`*, exactly **34** words are legal; **every** one contains `X`
(Lemma 8.3's first assertion) ✓. Exactly **6** have `X` on both parities, and each is 3-periodic
`(X,A,B,X,A,B)` with `A ≠ B` — precisely Lemma 8.3's second paragraph ✓. Each of the 6 is
**isolated under the cross-word restriction** (the only legal word whose every diagonal avoids the
diagonals at adjacent positions of the original is the original itself) ✓, and a 3-periodic word is
**not** equal to its one-position shift ✓, so the dense-set propagation gives the contradiction. The
final arc count of Prop. 8.5 is exact: three projective positions spaced `π/3` force an open arc of
length `> 2π/3 > π/2`.

**(d) §6.3.4 five-cycle accumulation.** With `S(0) ⊇ {0,1}` and `S(3) ⊇ {j, j+1}` and the two
adjacent-index rules, the residue check leaves `j ∈ {1,4}` and no other; `j = 1` bans both steps
from state 1 (`{0,1}` and `{1,2}`), `j = 4` bans both steps from state 0 (`{0,1}` and `{4,0}`), and
in either case (6.6) makes the shared state null. ✓

---

## 5. Prose steps I checked by hand and accept

These are not machine-checkable finite claims; I re-derived each and record the verdict.

* **Lemma 5.5** end to end, including: `α_±` are smooth degree-one lifts with derivatives → 1;
  `A = {s_x = 1}` has measure `π` per period; the growth/`λ = 1 + c_0 d/2` iteration reaches length
  `[L, (1+C_0 d)L]`; distortion `D_dist = exp(6C_0 L/c_0)`; the density-point extraction; the
  right-endpoint advance `≥ c_0 d`; the measure-`π` contradiction. Correct.
* **Proposition 5.6** (palette cardinality): the triple-`A`, binary-centre, uniform-separation
  argument. Correct.
* **Lemmas 6.3, 6.4** (`γ = 2 arcsin(1/(2√3))`, `cos γ = 5/6`, `γ/π` irrational, the three points
  `z_j` at distance `1/√3` forming a unit equilateral triangle). Correct.
* **Lemma 7.5** (cover obstruction on a square). The proof is correct; note the final step needs
  the observation that a finite union of segments has empty interior (it lies in a finite union of
  lines), which the paper leaves implicit. The number `10` is far from optimal: the same proof gives
  the statement for a closed square of **any side `> 4`** (equivalently for any compact convex `Q`
  whose inradius exceeds the mesh bound).
* **Lemmas 7.7, 7.8, and the proof of Proposition 7.1.** Correct as stated; the only gaps are
  cosmetic (Lemma 7.8 writes `C_1 = Z_1 ∪ B` with `B` open where the closed disk is meant, and
  `A = B(x,ρ) \ B` should be read as a closed annulus).

---

## 6. Errata (all cosmetic; none affects a conclusion)

1. **§5.3, display before (5.11).** "`F'_{j_r}(t) ≥ 1 + c_0 d − C_0 d ℓ_r ≥ 1 + ½c_0 d`" — the
   first `ℓ_r` should be `ℓ_r/2`: the bound is `|F'_j(t) − F'_j(mid)| ≤ C_0 d·ℓ_r/2`. With `ℓ_r`
   the second inequality would need `C_0 L ≤ c_0/2`, whereas the paper only chose `L ≤ c_0/C_0`.
   The correct statement, and the paper's choice of `L`, are consistent.
2. **§8.6, final display.** The list of squared-radius intervals ends "`(2.49, 2.50)`" for `u_T`,
   while Table 2 gives `(2.493, 2.495)`. Both contain the exact value `2.4934375511…`.
3. **§8.6, Lemma 8.9 proof.** "The other six rows give the corresponding displayed strict bounds
   by the same two products" — the six rows are not printed. They are all correct (see §1.3).

In addition, `§8.6` and `§8.2` rely on the correct reading of (8.6) as
`((35+12i)/37)(g + t)`, not `((35+12i)/37)g + t`; only the former matches Table 1, Table 2 and the
residual table. (This is a typesetting issue in the PDF, not an error in the argument: both
readings are similarities, but only the former places the graph in the region (8.4).)

---

## 7. What this audit does **not** cover

Sections 2–4 (Haar rigidity of wild character laws, compact-factor towers, conditional multiple
averages, the radial difference inequality, the proper↔weak-measurable transfer) are outside this
direction, and the measure-theoretic prose of §§5.1–5.2, 6.1–6.3, 7.1–7.5 (weak-* traces, avoiding
traces, support transport, Hausdorff limits) was refereed by reading, not by machine. No claim here
should be read as certifying those steps.

The one thing this audit establishes without qualification is that **the finite endgame of §8 is
correct**: the Moser certificate realises and cannot be 3-coloured (machine-checked), and it is
placed strictly inside the three-label region (exact, two independent methods). If §7 delivers the
interface cycle of length 3, Proposition 8.10 does go through.
