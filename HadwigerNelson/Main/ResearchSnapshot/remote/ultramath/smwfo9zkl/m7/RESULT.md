# The four-cycle stratum of Theorem 6.5 at `k = 6`

Member `m7`, swarm `smwfo9zkl`, direction `d7` (the four-cycle case of local finiteness of
cyclic centres, `§6.3.1`–`§6.3.2` of the paper).

**Status: a located no-go with exact certificates, plus one k=6 lemma that does survive, plus an
explicit object.** Nothing here decides `chi(R^2)`; nothing here is offered as a proof of
`6 <= chi <= 7`. Files and the exact commands are listed in `§8`; a second, independently coded
implementation of every number is `verify_indep.py`.

---

## 0. The question, and the answer in one paragraph

The paper proves that the set `L = {x : Gamma_x contains a cycle}` is closed and locally finite
for `k = 5` (Theorem 6.5). For a centre `x` whose `Gamma_x` contains the four-cycle `0-1-2-3` the
proof has two halves: `§6.3.1` reduces the palette to a canonical three-valued state and proves its
`L^1`-continuity in `x` (Lemma 6.6); `§6.3.2` transports supports by the local inverse of the
two-angle sum map and contradicts a strict angular margin. **Both halves are `k <= 5` arguments,
and they fail at `k = 6` for two independent reasons, which I isolate exactly:**

* `§6.3.1` needs *no admissible palette to carry two distinct state groups*.  A palette carrying
  `{X}` and `U = {0,2}` needs `|P| >= 3`, and `|P| <= k-3`; so the reduction holds iff `3 > k-3`,
  i.e. **iff `k <= 5`**.  At `k = 6` exactly two of the 33 admissible palettes are ambiguous
  (`{0,2,X}`, `{1,3,X}`), and the sentence of Lemma 6.6 that fails is quoted verbatim in `§2`.
* `§6.3.2` needs the *single* label `X` outside the two state groups.  What Lemma 5.2(2) actually
  gives at a nonparallel sum is `density one of I \ (G_1 ∪ G_2)`; with the two diagonal groups this
  set has size `k - 4`.  So the transport contradiction needs `k - 4 = 1`, i.e. **again `k = 5`**.
  This second failure is a **label-count** deficit, not a palette-size deficit: it is present in the
  most favourable palette hypothesis (all palettes of size 2), so *no palette hypothesis repairs it*.

I also prove a `k`-general form of the paper's Lemma 6.4 (`Theorem 2`, the `K_3` mechanism) whose
`k = 6` content is a sharp restriction on 2-valued palette maps at a cyclic centre
(`Theorem 2'`); and I show that the remaining pointwise system at `k = 6` is
**satisfiable** (`§5`, Theorem 4), so no pointwise argument can decide the stratum: any proof must
use the centre-coupling `(5.3)` and the accumulation device of `§6.3.2`.  `§6` gives an explicit
proper measurable 6-colouring of a strip with four-cycle centres, so the stratum is not vacuous.
Theorem 4' adds that the constraint level stays satisfiable *even with `(5.3)` at distance one*, on a
`4`-chromatic unit-distance configuration of seven four-cycle centres.

---

## 1. Inputs used, with the two-extraction check

Every statement below is quoted from the paper *and* re-derived symbolically (`verify.py` §A); this
is the check the sprint brief requires, done by proving the arithmetic content rather than by
reading a rendered glyph.

| input | content | use here |
|---|---|---|
| Def 6.1, (6.1) | `ij ∈ Gamma_x` iff for every ball `B` about `x`, `limsup_{h→0,h≠0} D_ij(B,h)/|h| > 0` | definition of `L` |
| Lemma 6.2, (6.2) | `ij ∈ Gamma_x ⇒ P_x(e) ⊄ {i,j}` for a.e. `e` | forbids singletons of cycle labels |
| Lemma 5.2(1), (5.2) | `c(x+e+v) ∉ P_x(e) ∪ P_x(v)` for a.e. independent pair `(e,v)` | `P_x(e) ∪ P_x(v) ≠ I` |
| Lemma 5.2(2) | `e` a density point of `D_{x,i}`, `v ∤ e` ⇒ `A_i` has density `0` at `x+e+v` | the separation conclusion |
| Lemma 5.2(3), (5.3) | `P_z(f) ∩ P_x(s(f)) = ∅` for `z+f = x+s+t` | two-centre exclusion (not used to derive anything below; it is the hypothesis a repair must use) |
| Cor 5.4, (5.7) | `P_x(f) ∩ P_x(Rf) = ∅` a.e. | alternation |
| Prop 5.6 / general-k bound | `1 <= |P_x(e)| <= k-3` a.e. | the `k`-dependence |
| Lemma 6.4 | `gamma = 2 arcsin(1/(2√3))`, `cos gamma = 5/6`, `gamma/pi` irrational | the `K_3` mechanism |
| Lemma 6.6, `§6.3.1` | three-valued canonical state, `L^1`-continuous in `x` | half 1 of the proof |
| `§6.3.2` | strict margins, support transport, no accumulation | half 2 of the proof |

Two-extraction check: `pdftotext -layout` and `pdftotext -raw` of the relevant pages agree on
(5.2), (5.3), (5.7), (6.1), (6.2); the one formula whose plain extraction is destroyed is
Lemma 6.4's `gamma = 2 arcsin(1/(2√3))` (the fraction and the radical are split across two lines).
`verify.py` §A pins that reading by proving `cos(2 arcsin(1/(2√3))) = 5/6`, which is exactly the
`cos gamma = 5/6` printed beside it, and then proves `|1-e^{i gamma}| = 1/√3` and that the triangle
`z_0 z_1 z_2` has side exactly `1`.

Setting throughout: `c` is a weak measurable `k`-colouring (paper Def 1.2), `I = {1..k}`,
`kappa = pi/3`, `R` = rotation by `kappa`, `S = S^1` with angular measure `sigma`, and `x` is a
centre whose `Gamma_x` contains the simple cycle `0-1-2-3`. Write

```
   T = {0,1,2,3},   U = {0,2},   V = {1,3},   O = I \ T   (the outsiders, |O| = k-4).
```

Call `P ⊆ I` **admissible** at `x` if `1 <= |P| <= k-3` and `P` is contained in no edge of the
four-cycle. `(6.2)` and Prop 5.6 say `P_x(e)` is admissible for a.e. `e`.

---

## 2. Theorem 1 — the exact `k`-threshold of the `§6.3.1` state reduction

**Theorem 1.** *Let `k >= 4` and let `x` be a four-cycle centre.*

*(a) The admissible palettes are exactly: the outsider singletons `{Z}`, `Z ∈ O`; the pairs not
equal to a cycle edge; and the triples (when `k >= 6`). Their number is*
`|O| + [pairs] + [triples]`, *equal to `7` for `k = 5` and `33` for `k = 6`.*

*(b) Fix `k >= 5` and let `G = {{X}, U, V}` with `X ∈ O` (so `|O| = 1`, i.e. `k = 5`, is the
case of the paper's `§6.3.1`). The following are equivalent: (i) every admissible palette carries at
most one member of `G`, so that the palette determines the state; (ii) `3 > k-3`; (iii) `k <= 5`.*

*Proof.* (a) A singleton `{i}` is admissible iff `i` lies in no cycle edge, i.e. iff `i ∈ O`, since
every cycle label of a cycle of length `>= 3` lies in an edge. A 2-element set is admissible iff it
is not an edge; a set of size `>= 3` is never contained in an edge. For `k = 5`: `1 + 6 = 7`
(`{X}`, `U`, `V`, `{i,X}` for `i ∈ T`). For `k = 6`: `2 + 11 + 20 = 33` (`2` outsider singletons,
`U`, `V`, `{i,X}`, `{i,Y}` for `i ∈ T`, `{X,Y}`, and all `20` triples).

(b) `{X} ∪ U` has three elements, so a palette contains both `{X}` and `U` iff `|P| >= 3`; by
Prop 5.6 this is possible iff `k - 3 >= 3`. The paper's `§6.3.1` computes the state as a function of
the palette and its Lemma 6.6 uses the sentence *"Two different state groups would require at least
three palette labels, contradicting Proposition 5.6."* — true at `k = 5` (`3 > 2`), false at `k = 6`
(`3 <= 3`). `verify.py` §C enumerates: `0` ambiguous palettes at `k = 5`, `2` at `k = 6`
(`{0,2,X}`, `{1,3,X}`), `11` at `k = 7`. ∎

Two remarks. At `k = 6` property (b)(i) fails twice over: `|O| = 2`, so "the outsider `X`" is not
even definable, and independently the two palettes above mix groups. So the `k = 6` four-cycle
stratum has no canonical state at all, not merely an ambiguous one.

So the first half of Theorem 6.5 stops working at `k = 6` at the **state reduction**, before any
geometry. The 33-element alphabet is `k6_nogo.md` (swarm `smwfcr56i`, m2) C1/C1b; Theorem 1(b) is
the sharp *iff* with the exact inequality, and it also fixes the *reason*: the bound `k-3` permits
`|P| = 3` from `k = 6` on, and `3` is exactly the size of `{X} ∪ U`.

---

## 3. Theorem 2 — the `K_3` mechanism (Lemma 6.4 at a cyclic centre) and its `k = 6` content

The paper's Lemma 6.4 is one instance of the following; the general form is what has `k = 6`
content.

**Theorem 2 (`K_3` mechanism).** *Let `k >= 4` be arbitrary and `x ∈ R^2`. Let `E_1, E_2 ⊆ S` be
measurable with
`sigma(E_j) > 0`, and let `G_1, G_2 ⊆ I` be disjoint with `G_j ⊆ P_x(e)` for a.e. `e ∈ E_j`. Suppose
there is a set of `t` of positive measure such that for `j = 0,1,2` the directions
`exp(i(t+2j kappa))` and `exp(i(t+pi+gamma+2j kappa))` are density-one points of `E_1`, resp.
`E_2`. Then*

```
        k - |G_1 ∪ G_2|  >=  3 .
```

*In particular `|G_1| + |G_2| >= k-2` is impossible.  (At `k = 5` with `G_1 = {X}`,
`G_2 = D` this is the paper's Lemma 6.4: `|G_1|+|G_2| = 3 = k-2`, contradiction.  Nothing in the
proof uses `k`, so the mechanism is `k`-general.)*

*Proof.* Let `T' = I \ (G_1 ∪ G_2)` and, for such a `t`, put

```
   a_j = exp(i(t+2j kappa)),   b_j = exp(i(t+pi+gamma+2j kappa)),   z_j = x + a_j + b_j.
```

*Nonparallel:* the angular difference of `a_j, b_j` is `pi+gamma`, not a multiple of `pi` (since
`gamma/pi` is irrational). *Density:* for `i ∈ G_1`, `a_j` is a density-one point of `D_{x,i}`
(because `E_1 ⊆ D_{x,i}` and a density point of `E_1` is one of `D_{x,i}`), so Lemma 5.2(2) gives
`A_i` of density zero at `z_j`; likewise for `i ∈ G_2` using `b_j`. Hence `T'` has density one at
`z_j` for `j = 0,1,2`. *Geometry:*

```
   z_j - x = exp(i(t+2j kappa)) (1 - e^{i gamma}),      |z_j - x| = |1-e^{i gamma}| = 1/√3,
   z_{j+1} - z_j = exp(i(t+2j kappa)) (e^{2i kappa}-1)(1-e^{i gamma}),
   |z_{j+1}-z_j| = 2 sin(kappa) · |1-e^{i gamma}| = √3 · (1/√3) = 1,
```

and `z_3 = z_0` because `6 kappa = 2 pi`. So `z_0 z_1 z_2` is a unit equilateral triangle (each
`z_j` is at distance `1/√3` from `x`). *Contradiction:* the typical set is conull, so for a.e. `w`
in a small disk all three `z_j + w` are typical; and each `z_j` is a density-one point of the finite
union `T'` of colour classes, so for `w` in a set of positive measure all three `z_j + w` lie in
`T'`. Combining, there are three typical points of `T'` at pairwise distance `1`; by Lemma 4.3 unit
pairs of typical points have different colours, so `T'` carries three distinct colours, i.e.
`|T'| >= 3`. ∎

**Theorem 2' (2-valued palette maps).** *Let `k >= 4`, `x` a centre, and suppose the palette map
`P_x` is 2-valued a.e. with values `A ≠ B`, both taken on sets of positive measure. Then*

```
        A ∩ B = ∅   and   |A| + |B| <= k-3 .
```

*Consequently, at a four-cycle centre: a palette of size `1` is an outsider singleton, so a
2-valued palette map at `k = 6` must be one of the 13 pairs*

```
   {X},{Y}  (sum 2);   {X} or {Y}  with one of  U, V, {0,Y}, {1,Y}, {2,Y}, {3,Y}
   (resp. with one of U, V, {0,X},{1,X},{2,X},{3,X})   (sum 3).
```

*Proof of the first display.* `(5.7)` and `A ∩ A = A ≠ ∅` force `P_x(Re) ≠ P_x(e)` for a.e. `e`;
hence the map alternates `A, B, A, B, …` and `A ∩ B = ∅`. In particular `P_x(s+2 kappa) = P_x(s)`
a.e. (two alternations) and `P_x(s+pi) = P_x(s+3 kappa) =` the other value a.e. (three alternations).
Let `F = {t : P_x(t+gamma) = P_x(t)}`. If `sigma(F) = 0` then the palette flips a.e. under the
`gamma`-rotation, hence is invariant under `2 gamma`; a measurable function invariant under an
irrational rotation is constant a.e. (nonconstant Fourier coefficients vanish, the rotation
eigenvalues being `≠ 1`), contradicting the alternation under `R` — this is verbatim the argument
of Lemma 6.4. So `sigma(F) > 0`. For `t ∈ F` (and `t` a density point of the palette-value sets;
they are invariant under `2 kappa` up to null sets, so a density point of one is a density point of
its `2j kappa`-translate) the directions of Theorem 2 satisfy

```
   P_x(t+2j kappa) = P_x(t) =: A,     P_x(t+pi+gamma+2j kappa) = other value =: B,
```

because `(t+pi+gamma+2j kappa) = (t+gamma) + 2j kappa + 3 kappa`. Theorem 2 then gives
`k - |A| - |B| >= 3`. ∎

The last display is exact and is enumerated in `verify.py` §D and `verify_indep.py` §4–§5:

| `(k, length of the cycle)` | disjoint palette pairs | pairs that escape Theorem 2 (`\|A\|+\|B\| <= k-3`) |
|---|---|---|
| `(5, 4)` | 7 | **0** — no 2-valued palette map |
| `(5, 5)` | 5 | **0** |
| `(5, 3)` | 13 | 1 (`{X}`,`{Y}`) |
| `(6, 4)` | 110 | **13** (all "outsider singleton + set of size `<= 2`") |
| `(6, 5)` | 85 | 5 (all `{Z}` + one diagonal) |
| `(6, 6)` | 64 | **0** — no 2-valued palette map |

So at `k = 6` the palette map at a **six-cycle** centre is never 2-valued (all `64` disjoint pairs
trigger Theorem 2, since every palette there has `>= 2` labels); at a **four-cycle** centre the
`13` surviving configurations all use an outsider singleton. At `k = 5` the mechanism excludes every
2-valued palette map, which is why `§6.3.1`'s state is genuinely three-valued there.

---

## 4. Theorem 3 — the outsider deficit: `§6.3.2` is not repairable by any palette hypothesis

**Theorem 3.** *Let `x` be a four-cycle centre, `E_1, E_2 ⊆ S` of positive measure, and
`G_j ⊆ P_x(e)` for `e ∈ E_j`, with `G_1 ∩ G_2 = ∅`. Let `a` be a density-one direction of `E_1` and
`b` a nonparallel density-one direction of `E_2`. Then*

```
        the label set  T' = I \ (G_1 ∪ G_2)  has density one at  x + a + b,  |T'| = k - |G_1 ∪ G_2| .
```

*This is the strongest consequence of the palette machinery at a sum of two nonparallel density
directions (it is Lemma 5.2(2) applied label by label; `verify.py` §D records the set
`G_1 ∪ G_2` for the states actually available).*

*Proof.* For `i ∈ G_1`: `E_1 ⊆ D_{x,i}` and `a` is a density point of `E_1`, hence of `D_{x,i}`;
Lemma 5.2(2) gives density zero of `A_i` at `x+a+b`. Same for `G_2` with `b`. Finitely many labels,
so the union has density zero. ∎

Now compare with the two steps of `§6.3.2` that consume it.

1. *Strict margins / Lemma 6.3.* The paper's Lemma 6.3 concludes that `x+a+b` has **density one of
   the single label `X`**; its hypothesis is that the two state groups are disjoint "whose union is
   `I \ {X}`, for a fixed label `X`". At `k = 5` with the two diagonals, `U ∪ V = T` and
   `|T'| = 1`. **At `k = 6`, `|T'| = k - 4 = 2`** for the diagonal states — `T' = {X,Y}`, the
   outsider pair.
2. *The transport contradiction.* The contradiction is produced by a *single* forbidden label: the
   paper writes "Neither output state can be `X`: the density consequence of Lemma 5.2 at `y` would
   then give density zero of `X` at the same spatial sum", against density one of `X`. At `k = 6`
   the forced set is `{X,Y}`; a state at the target centre whose group is `⊆ {X,Y}` (in particular
   the state "an outsider is in the palette") is *consistent* with the density-one conclusion, so
   the two statements no longer contradict.

**Corollary 3.1 (no palette hypothesis repairs it).** If both palettes at `x` are 2-element sets —
the most favourable palette hypothesis available at `k = 6`, and the exact `k = 5` situation —
then `|G_1 ∪ G_2| <= 4` for *every* pair of states, so `|T'| >= 2` always. `§6.3.2` needs
`|T'| = 1`. Hence **no bound, and no structural hypothesis, on the palette at `x` can make
`§6.3.2` run at `k = 6`**; the deficit `k - 4 - 1 = 1` is a *label-count* deficit.

**Corollary 3.2 (what would repair it).** `§6.3.2`'s contradiction is available at `k = 6` iff at
`x` there are two disjoint palette groups with

```
        |G_1| + |G_2| = k - 1 = 5,
```

i.e. a 3-label group disjoint from a 2-label group — for the four-cycle, e.g. the palettes `{0,2,X}`
and `{1,3}`, or `{0,1,2}` and `{3,X}`. Such configurations exist in the 33-element alphabet, but
nothing in `(6.2)`, `(5.7)`, `(5.2)` or the palette bound forces one, and Corollary 3.1 shows that
they are absent in the pure-pair case. `verify.py` §D lists all disjoint pairs of admissible
palettes with their `|A|+|B|`.

Note the contrast with the *triangle* interface, where the sprint brief records the barrier as the
outsider set of size `2` out of `3` (`results/K6-BARRIER.md` §3): **the same phenomenon occurs one
cycle length earlier, in `§6.3`, and it is not about palettes at all.**

---

## 5. Theorem 4 — the `k = 6` pointwise system is satisfiable, so no pointwise argument decides `L`

**Theorem 4.** *At `k = 6` the following set of conditions on a palette map `P : S -> 2^I` at a
four-cycle centre has a solution:*

* `P` is admissible a.e. (palette bound + `(6.2)` for the four cycle edges);*
* `P(e) ∩ P(Re) = ∅` a.e. `(5.7)`;*
* `P(e) ∪ P(v) ≠ I` for a.e. nonparallel pair `(e,v)` `(5.2)`;*
* *Theorem 2 with every disjoint pair: `|G_1| + |G_2| >= k-2` must not occur at the angles of
  Theorem 2.*

*Explicit solution: six sectors `[j kappa, (j+1) kappa)`, `j = 0..5`, with `P = {4}` on the even
sectors and `P = {0,2}` on the odd ones.*

*Proof.* Both values are admissible (`{4}` is an outsider singleton, `{0,2}` is a diagonal);
`{4} ∩ {0,2} = ∅` and `R` advances the sector index by one, so `(5.7)` holds on every sector;
`{4} ∪ {0,2} = {0,2,4} ≠ I` and the self-unions are smaller, so `(5.2)` holds at every pair of
sectors; the only disjoint pair used has `|A| + |B| = 3 <= k-3 = 3`, so Theorem 2 is silent.
`verify.py` §E and `verify_indep.py` §6 check all four clauses. ∎

Consequently a proof of local finiteness of the four-cycle locus at `k = 6` cannot be assembled from
the palette combinatorics of `§6.3.1` — at best it can exclude the 2-valued configurations of
Theorem 2', and the above survives. **The content of any such proof must come from the
centre-coupling, i.e. from `(5.3)`/Lemma 5.2(3) and the accumulation device of `§6.3.2`.** This is
the same verdict as the machine-checked "powerless class" theorem of swarm `smwfk0ybk` (m16) for
single-centre interface constraints, here specialized to the four-cycle stratum and extended to
include the `K_3` mechanism.

### Theorem 4' — even the distance-one two-centre exclusion is powerless

The sprint brief identifies `P_x(f) ∩ P_{x+u}(f) = ∅` for unit `u` as *the first genuinely
two-centre constraint*. It does not decide the four-cycle stratum at `k = 6` either.

Call a **sector palette system** at a set of centres `C ⊆ R^2` the data, for each `x ∈ C`, of a
palette `P^x_j ⊆ I` for each of the six sectors `[j kappa, (j+1) kappa)`, `j = 0..5`, of the
`R`-orbit at `x` (so `R` advances the sector index by one). This is a *subclass* of all palette
systems — a model in the subclass is a model of the constraint level itself.

**Theorem 4'.** *Let `C` be the seven vertices of the Moser spindle, a `4`-chromatic unit-distance
graph with the eleven unit pairs `01,02,12,13,23,34,35,45,46,56,06`. There is a sector palette
system at `C` such that, at every `x ∈ C`, `x` is a four-cycle centre and (palette bound), `(6.2)`,
`(5.7)`, `(5.2)` and the `K_3` mechanism hold; and such that for every unit pair `x, y ∈ C` the
palettes in the same sector are disjoint — equivalently `P_x(f) ∩ P_y(f) = ∅` for a.e. `f`, which is
`(5.3)` with `s = f` (the only admissible representation, by Remark 5.3, at distance exactly one).*

*The model (even-sector value, odd-sector value):*

```
   0: ({4}, {0,2})   1: ({5}, {1,3})   2: ({0,2}, {4})   3: ({4}, {5})
   4: ({5}, {0,2})   5: ({0,2}, {4})   6: ({1,3}, {5})
```

*Each is 2-periodic in the sector index, so `(5.7)` holds; each uses two disjoint palettes, so
`(5.2)` holds; the only disjoint pairs have `|A| + |B| <= 3`, so Theorem 2 is silent; and the eleven
unit pairs are sector-wise disjoint as listed. `verify.py` §H and `verify_indep.py` §10 check every
clause, and re-derive `chi(Moser) = 4` by counting proper 3-colourings (there are none).*

**What Theorem 4' does and does not say.** It shows that the constraint level consisting of the
pointwise palette constraints *plus* `(5.3)` at distance exactly one is satisfiable at `k = 6` on a
`4`-chromatic configuration of four-cycle centres — so no argument from those constraints can give
the four-cycle case. It does **not** settle the full content of `(5.3)`: for centre pairs at
distance `d ∈ (0,3)` there is a representation `u + f = s(f) + t(f)` with `s(f)` not the identity
(for `d → 0` one has `s(f) ≈ R^{±1} f`, and at `d = 1` one has `s = f` exactly, which is
Theorem 4'), so `(5.3)` links each centre to a *shifted* sector of its neighbours. If in addition
all pairwise distances of `C` were `<= 3`, every pair would contribute, and a sector would have to
carry `|C|` pairwise-disjoint non-empty palettes — more than six labels allow as soon as
`|C| >= 7`. Whether the full multi-scale content of `(5.3)` is satisfiable on a `4`-chromatic centre
configuration is therefore **open**, and it is the sharpest untested constraint this analysis
leaves.

---

## 6. Theorem 5 — the stratum is not vacuous: an explicit `k = 6` colouring with four-cycle centres

**Theorem 5.** *Let `a = 51/100`, `b = 43/50`, `W = 2b = 43/25 = 1.72`, and let
`c : R x [0,W) -> {0,...,5}` be given by*

```
        c(x,y) = ( floor(x/a) mod 3 ,  floor(y/b) mod 2 ).
```

*Then `c` is a proper measurable 6-colouring of the strip `R x [0,W)` (no two points of the same
colour are at distance exactly `1`), and for every `i ∈ Z` the centre `x_i = (i a, b)` satisfies
`Gamma_{x_i} ⊇ C_4`. Every other interior point has `Gamma_x` empty (cell interior) or a single edge
(interface interior). Hence `L = {(i a, b) : i ∈ Z}`: nonempty and locally finite.*

*Proof.* *Properness.* Two points of the same colour differ by `(delta_x, delta_y)` with
`delta_x ∈ [3am-a, 3am+a]` for some `m ∈ Z` (the columns of one colour are `3a` apart) and
`|delta_y| < b` (the colour determines the row, and the strip has only the two rows `j = 0,1`).
Cases: `m = 0` gives `delta_x^2 + delta_y^2 <= a^2+b^2 = 9997/10000 < 1`; `|m| = 1` gives
`|delta_x| >= 2a = 51/50 > 1`; `|m| >= 2` gives `|delta_x| >= 5a > 1`. So the distance is never
`1`.
*`Gamma_x ⊇ C_4`.* At `x_i` four cells meet, with the four distinct colours
`((i-1) mod 3, 0), (i mod 3, 0), ((i-1) mod 3, 1), (i mod 3, 1)`. For the pair across the vertical
interface below `x_i` and `h = (-t,0)`, the transition set inside `B(x_i,rho)` is
`[ia, ia+t) x [b-rho,b)`, of area `t·min(rho,b)`; so the ratio in `(6.1)` equals `min(rho,b) > 0` for
every ball and the edge is present. The same computation in the other three quadrants gives exactly
the four edges of a 4-cycle; non-adjacent colour pairs have empty transition sets for small `h`.
*Nothing else.* Off the corners only one interface passes through `x`, and inside a cell none.
`verify.py` §F–§G and `verify_indep.py` §7–§8. ∎

**The limit of this construction.** A palette at `x` is built from traces on circles of radius
`~1` about `x` (Definition 5.1), so a palette-level model needs a `6`-colouring of a neighbourhood
of a unit circle, hence of a set of width `>= 2`. For the rectangular family
`p` columns `x` `q` rows with `p q = 6` (colour `(i mod p, j mod q)`) the exact case analysis is:
`p = 1` and `p = 2` are improper for **every** `(a,b)`, because the same-colour `x`-intervals
`[pam-a, pam+a]` have half-width `a` and centres `p a` apart, hence tile the line for `p <= 2`, so
`1` lies in one of them; `p = 6` gives `W < 0.98`; and `p = 3` gives `W < sqrt(3)`, approached as
`a -> 1/2`. So the family caps at `sqrt(3) = 1.732 < 2` and cannot reach a unit circle.
More strongly: **if every strip were `6`-colourable then every
finite unit-distance graph would be `6`-colourable** (a finite graph of diameter `D` embeds in a
strip of width `D`), so by de Bruijn–Erdős `chi(R^2) <= 6`. Hence deciding strip `6`-colourability
in general is equivalent to `chi(R^2) <= 6`: the explicit-counterexample route at `k = 6` is not
independent of the original problem. Theorem 5 is therefore the strongest object this route gives:
a genuine `k = 6` four-cycle centre, with no palettes.

---

## 7. What a `k = 6` four-cycle proof must add, exactly

Given Theorems 1–4, a proof of local finiteness of the four-cycle locus at `k = 6` must supply all
of the following, and none is available in the paper:

1. **a state reduction without "the palette determines the state"** — the two ambiguous palettes
   `{0,2,X}`, `{1,3,X}` (Theorem 1) mean the canonical `{X}/U/V` state is undefined, so Lemma 6.6's
   weak-* passage ("two different state groups would need three palette labels") has no `k = 6`
   form. The conclusion of Theorem 2' (2-valued maps restricted to `13` pairs) is the only fragment
   of the reduction that survives, and Theorem 4 shows it does not suffice.
2. **a replacement for Lemma 6.3's single-label conclusion** — i.e. an argument that the outsider
   set `T' = I \ (G_1 ∪ G_2)` of Corollary 3.1 (size `2` in the best case) is excluded at the
   transported directions. This is a genuinely new geometric hypothesis; it is where the `k = 6`
   content must live, and it is *not* a palette-count condition.
3. **a replacement for Lemma 6.4 in the `>= 3`-valued regime.** Theorem 2 covers 2-valued palette
   maps; at `k = 6` the palette map may be 3-valued (e.g. `U, V, {X,Y}` on three arcs), and the
   `K_3` mechanism then needs the angle pair of Theorem 2 to fall in two *disjoint* letters, which
   for an arbitrary measurable 3-valued map is not automatic. `verify.py` §D gives the exact list of
   disjoint pairs that escape, so any such argument can be audited against it.

---

## 8. Files and verification

```
   RESULT.md            this file
   AUDIT.md             line-by-line dependence of §6.3.1–§6.3.2 on k = 5, with references
   verify.py            all exact computations, sections A-H; prints verify.out
   verify_indep.py      second implementation, different data structures and derivations;
                        prints verify_indep.out; ends with ALL INDEPENDENT CHECKS PASSED
   verify.out           log of verify.py
   verify_indep.out     log of verify_indep.py
   paper/paper.txt      pdftotext -layout of the paper
   work/pages/          per-page -layout and -raw extractions and 150 dpi PNGs of pp. 27,29,30,
                        33..40 (the pages carrying every input listed in §1)
```

Commands, from the repository root:

```
   python3 .ultramath/smwfo9zkl/m7/verify.py         | tail -40
   python3 .ultramath/smwfo9zkl/m7/verify_indep.py   | tail -5
   grep -c "OK" .ultramath/smwfo9zkl/m7/verify_indep.out        # 62, no FAIL
```

Every number in this file is produced by both programs. `verify.py` covers: §A the constants of
Lemma 6.4 by `sympy`; §B the palette alphabet for `k = 5,6,7` and every cycle length `3..k`; §C the
ambiguity count `0,2,11`; §D the disjoint-pair census and the escape lists; §E the model of
Theorem 4; §F the colouring of Theorem 5 by cases, plus a redundant `81 x 81`-period scan; §G the
exact transition areas. `verify_indep.py` recomputes §B by bitmask enumeration, §C–§D by direct
construction instead of filtering, §E on all six sectors, §F by `sympy` maximisation of `x^2+y^2`
over each rectangle for `-500 <= m <= 500`, and §H by a separate bitmask encoding plus an
independent count of the proper 3-colourings of the Moser spindle (none).
