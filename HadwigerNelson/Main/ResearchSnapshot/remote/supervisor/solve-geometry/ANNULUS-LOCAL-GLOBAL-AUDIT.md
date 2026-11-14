# Source-licensed ternary contract, and local/global audit of the nine-sector annulus model

Analysis only; no computation, no placement. Sources read: `lean/OAI/Geometry/PlaneColoring/
{Palettes,PaletteTransport,BinaryPalettes}.lean`. Grades: **[S]** source-read with line numbers,
**[P]** hand-proved here, **[C]** cited (Astra / graph worker), **[X]** not in the source.

## 1. The exact source objects [S]

| object | statement | where |
|---|---|---|
| `paletteSet x i` | `⋃_{b ∈ paletteGenerators x i} tracePositive x i b`, the essential (a.e.) union over the trace family at `x`; `palette x t := univ.filter (t ∈ paletteSet x i)` | Palettes.lean:13,17,44 |
| `IsTrace x b` | `(x,1,b) ∈ closure (sampleSet …)`, `sampleSet = {(y,r,b) : TypicalSampling c y r ∧ b = sampleCode c y r}` | Compactness.lean:259,261 |
| **`BinaryCenter x i j`** | **`∀ᵐ t ∂angularMeasure, t ∈ paletteSet x i ∨ t ∈ paletteSet x j`** — a property of the *centre* `x`, not of a single direction | **BinaryPalettes.lean:9** |
| `binary_alternation` | hypotheses `Measurable c`, **`WeakColoring k c`**, `BinaryCenter x i j`; conclusion: a.e. `t`, `(t+60° ∈ paletteSet x i ↔ t ∉ paletteSet x i) ∧ (t ∈ paletteSet x j ↔ t ∉ paletteSet x i)` | :11 |
| `binary_pair_distinct` | `BinaryCenter x i j ⟹ i ≠ j` (via alternation) | :28 |
| `palette_transport_param` | hypotheses: `Measurable c`, **`WeakColoring k c`**; two centres `x, z`; `a, s, t : ℝ → ℝ` with `HasDerivAt`s, **`1/2 ≤ Da r`** (the angular map is a lower-order local diffeomorphism), **`Ds r ≠ 0`**, **`sin(t r − s r) ≠ 0`** (the two unit directions are non-parallel), and the **exact circle identity** `circleTarget (samplingParameter x z 1, a r) = circleSum 1 (s r, t r)`. Conclusion: a.e. `r`, `a r ∈ liftPalette z i → s r ∉ liftPalette x i` | PaletteTransport.lean:362–368 |
| `binary_transport_invariant` | needs **`BinaryCenter` at both `x` and `z`**, plus `\|d\| < 1/2`, `1/2 ≤ 1 + d·binaryB d t`, and the angle condition on `z − x` | BinaryPalettes.lean:76 |
| `binary_centers_separated` | `∃ δ > 0, ∀ x z i j, BinaryCenter x i j → BinaryCenter z i j → x ≠ z → δ ≤ dist x z` — the separation theorem, hypothesis `WeakColoring k c` | :123 |
| `ae_not_binary_circle` | a.e. `t`, `¬ BinaryCenter (x + direction t) i j` | :182 |
| **`palette_triple_null`** | **`(c : ℂ → Fin 5)`**, `WeakColoring 5 c`, `S.card = 3` ⟹ `∀ᵐ t, ¬ S ⊆ palette x t` | :252 |
| `palette_cardinality` | **`(c : ℂ → Fin 5)`** ⟹ a.e. `1 ≤ \|palette x t\| ≤ 2` | :260 |

**Two hard facts about the ternary level.** (i) The tree's ternary statement is a **`k = 5` nullity**
 (`palette_triple_null`): at five colours, *no* 3-element label set sits inside a palette a.e. (ii) **There
 is no `k = 6` analogue in the source** [X]. At `k = 6` the analogous statement is *false*: a ternary palette
 exists, and the strongest recorded bound is the half-circle estimate `σ{e : T ⊆ P_x(e)} ≤ 1/2` from `m11`,
 which is a **different** (weaker) statement and is *external* to this Lean file. Any use of "the ternary
 analogue at `k = 6`" must cite `m11`-style output, **not** `palette_triple_null`.

## 2. The Astra local model, stated exactly [C]

`c_A(z) := ⌊9·arg z / (2π)⌋ mod 3` on the open annulus `A = {0.99 < |z| < 1.01}`: nine sectors of `40°`,
labels cycling `0,1,2,0,1,2,…`. It is defined on `A` only; **it is not a total function `ℂ → Fin 6`**, so it
is not an input to any lemma above.

**Claim 1 [P]: `(A, c_A)` is a proper 3-colouring of the induced unit-distance graph on `A`.** If
`z = r e^{iθ}`, `z' = r' e^{iθ'}` with `r, r' ∈ (0.99, 1.01)` and `|z − z'| = 1`, then
`cos(θ' − θ) = (r² + r'² − 1)/(2 r r')`. Over the closed square `[0.99, 1.01]²` this lies in
`[0.48985, 0.50985]` (extremes at `r = r' = 0.99` and `r = r' = 1.01`; the mixed case gives `0.50015`), so
`|θ' − θ| ∈ [59.34°, 60.66°]`. Equal labels require `|θ' − θ| ≡ 0 (mod 120°)`, which this window excludes.
So no monochromatic unit pair lies in `A`.

**Claim 2 [P]: `(5.7)` holds for every centre with `|x| ≤ 0.01`.** For such `x` and every direction `e`,
`x + e ∈ A` and `x + Re ∈ A` (where `R` is rotation by `60°`), because
`1 − |x| ≥ 0.99` and `1 + |x| ≤ 1.01`. Labels: `60° = 1.5` sectors exactly, so
`⌊(θ+60°)/40°⌋ = ⌊θ/40°⌋ + 1` or `+ 2` — never `≡ ⌊θ/40°⌋ (mod 3)`. Hence `c_A(x+e) ≠ c_A(x+Re)`
for **every** `e`, which for singleton palettes is exactly `P_x(e) ∩ P_x(Re) = ∅`.

**Claim 3 [P]: the admissible centre neighbourhood is exactly `|x| ≤ 0.01`, not `0.005`.** The trace
definition samples circles of radius `r_n → 1` about centres `y_n → x`; every sample point stays in `A` iff
`|y_n| + r_n ≤ 1.01` and `r_n − |y_n| ≥ 0.99` for all large `n`, i.e. `|x| ≤ 0.01`. The candidate's `0.005`
is a safe but unnecessary restriction; `0.01` is the exact threshold, and at `|x| = 0.01` both inequalities
are tight, so the *open* condition is `|x| < 0.01`.

**Claim 4 [C]/[P]: at such centres the palette is a singleton in `{0,1,2}`.** Every trace at `x` has its
support inside `{c_A(x+e)}` by construction; hence `P_x(e) = {c_A(x+e)} ⊆ {0,1,2}` a.e.

## 3. Local/global audit: which hypotheses the model meets [P]

| source hypothesis | status in the annulus model |
|---|---|
| totality `c : ℂ → Fin 6` | **NOT met.** `c_A` is partial. Every lemma above takes a total function; an extension must be *chosen*, and each extension yields possibly different palettes at centres outside `|x| < 0.01`. |
| `Measurable c` | met on `A` (piecewise constant); meaningless globally until extended. |
| **`WeakColoring 6 c`** | **NOT met and not checkable.** It is a statement about *all* unit pairs in the plane (a.e. in a product measure), including pairs in the disk `{\|z\| < 0.99}`, in the exterior, and straddling the two boundary circles — none of which is coloured. **This is the single hypothesis every theorem above assumes, and it is exactly what a local model cannot supply.** |
| `palette`/`paletteSet` well-defined | definable from `c_A` **only for centres `\|x\| < 0.01`**; for any other centre the trace circles leave `A`, so the trace family — and hence the palette — is determined by data the model does not contain. |
| `(5.7)` / `palette_sixty` | **met locally** (Claim 2), for `\|x\| < 0.01` only. |
| endpoint trace `c(x+e) ∈ P_x(e)` | holds by construction locally. |
| `(5.2)`, `c(x+e+v) ∉ P_x(e) ∪ P_x(v)` | **not instantiable**: `x + e + v` is at distance up to `2` from `x`, outside `A`. |
| `palette_transport_param` (two-centre transport) | **no instance exists in the model.** It needs *two* centres `x, z`. Keeping palettes inside the model requires both `\|x\|, \|z\| < 0.01`, so `dist(x,z) < 0.02`; but the identity `circleTarget (samplingParameter x z 1, a r) = circleSum 1 (s r, t r)` with `a` a local diffeomorphism and `sin(t−s) ≠ 0` describes the *two-unit decomposition of the far side*, and the lemma's conclusion relates palettes at `x` and `z` through a family of directions `r ↦ s r` — a relation that is checkable only when *both* palettes are determined, which for `dist(x,z) ≲ 0.02` is true, but then the lemma is trivially consistent with the model rather than a constraint on it. Conversely, the use the paper makes of it (`TE`, `(5.3)` at centre distance exactly `1`) is **not available**: the second centre is then at distance `1`, so `\|z\| ≈ 1` and its trace circles reach `\|z\| − 1 ≈ 0` — deep inside the uncoloured disk. |
| `BinaryCenter x i j` | **false at every model centre** for every pair: the singleton takes all three labels on positive-measure direction sets, so a.e. `t` is in neither of the two chosen `paletteSet`s for a positive-measure set of `t`. Hence `binary_alternation`, `binary_pair_distinct`, `binary_centers_separated` are all vacuous here. |
| `binary_transport_invariant` | **not instantiable**: needs two binary centres, and there are none; it also needs `\|d\| < 1/2` between them. |
| `palette_triple_null` | it is a `k = 5` statement; the model is a 3-colour sub-model of `k = 6`. No `k = 6` source statement exists [X]. A `k = 6` half-circle bound (`m11`) is satisfied *vacuously* here because palettes are singletons, i.e. `σ{T ⊆ P_x} = 0`. |

**Verdict.** The annulus model is a genuine, provable **local** object: a proper 3-colouring of the induced
unit graph of `A` that satisfies `(5.7)` and has singleton palettes in `{0,1,2}` for all `|x| < 0.01`. It
satisfies **no** theorem-level hypothesis of the source, because all of them carry `WeakColoring k c` and
`BinaryCenter`, and because palettes are undefined away from `|x| < 0.01`. It therefore **cannot** contradict
any source theorem, and it is **not** a step toward a global 6-colouring.

## 4. The source-licensed ternary contract (a checklist for any candidate) [S]

A candidate at `k = 6` must supply all of the following, in this order; no item may be replaced by a local
surrogate:

1. **(T1) Totality + measurability:** a total `c : ℂ → Fin 6` with `Measurable c`.
2. **(T2) Global weak properness:** `WeakColoring 6 c` (paper Def. 1.2), i.e. for every `R > 0`,
   `∑_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0`.
3. **(T3) Palette object:** `paletteSet`/`palette` from `Palettes.lean`, which needs (T1) only.
4. **(T4) Sixty-degree exclusion** (`palette_sixty`, (5.7)) — *derived* from (T1)+(T2); a candidate may not
   assume it independently.
5. **(T5) Binary centres:** `BinaryCenter x i j` at the centres of interest, then `binary_alternation`
   (needs (T2)), `binary_pair_distinct`, and — for separation — `binary_centers_separated` (needs (T2)).
6. **(T6) Two-centre transport:** an instance of `palette_transport_param` with **all** of: (T1), (T2), two
   centres, `a` with `HasDerivAt` and derivative `≥ 1/2`, `Ds ≠ 0`, `sin(t − s) ≠ 0`, and the exact circle
   identity. A candidate that supplies only the identity and not (T2) has supplied a *geometric* identity,
   not the transport theorem.
7. **(T7) Ternary at `k = 6`:** **no nullity**. The available forms are (a) the `m11` half-circle bound
   `σ{e : T ⊆ P_x(e)} ≤ 1/2` (external, computational, not Lean) and (b) the `k = 5` nullity
   `palette_triple_null`, which must **not** be transported to `k = 6` — at six colours a palette of size 3
   is possible, so the nullity is simply false there.

**The one-line rule for this audit:** a local partial colouring can satisfy (T3)–(T4) and the endpoint trace;
it cannot satisfy (T1)–(T2), and without those, (T5)–(T7) are vacuous.

## 5. What promoting the annulus model to a global 6-colouring would require [P]

1. **Colour the complement:** the disk `D = {|z| ≤ 0.99}` (diameter `1.98 > 1`, so it contains unit pairs and
   cannot be monochromatic) and the exterior `E = {|z| ≥ 1.01}`.
2. **Cross-boundary unit pairs:** for each `z ∈ A` the partner `z'` at distance `1` may lie in `D` or `E`;
   each such pair requires distinct colours. Since `A` carries all three labels in every `120°` window,
   every boundary point of `D` sees all three labels within its unit-distance reach: this is a genuine and
   non-trivial constraint on the extension, and it is the first place the local model could fail.
3. **Consistency of palettes:** after extension, the palettes at centres with `0.01 < |x| < 1.99` acquire
   values from the extension. Nothing in the local model controls them, so no conclusion about
   `BinaryCenter` at any centre can be drawn before step 1–2 are done.
4. **The `k = 6` ternary step:** even with (1)–(3), the ternary statement at six colours is the half-circle
   bound, not a nullity; a candidate must meet that bound with its *global* palettes.

**No claim is made here that such an extension exists or does not.** The local model is retained as a
verified local object with a precisely delimited interface, and the exact obstruction to promoting it is
item 2 above.
