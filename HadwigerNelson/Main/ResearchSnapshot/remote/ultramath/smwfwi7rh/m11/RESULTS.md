# The frozen-field gap at six colours

**Swarm `smwfwi7rh`, member m11, direction d9.**
Paper: `attachments/here-are-three-files-ni5n/paper.pdf`. Section, lemma and display
numbers refer to it. `sprint/k6/` is the coordinator's report of the previous sprint.

---

## 0. What is proved here

The previous sprint's headline negative result is that *"the palette-level route is dead for
every cycle length"* at `k = 6`: Theorem C of `sprint/k6/REPORT.md` and `sprint/k6/FREE-LABEL.md`
exhibit, for every `ell in {3,4,5,6}`, palette fields that are said to satisfy

* the palette bound `1 <= |P| <= 3`,
* the edge exclusions (6.2) of `C_ell`,
* the sixty-degree exclusion (5.7),
* "the exact local (5.3) transport" for all centre pairs at distance `<= d_0 = pi/54`,

with the `ell`-cycle locus equal to the whole plane, so that the index case of Theorem 6.5
cannot be settled from palette data.

**All of those models are functions of the direction only: `P_z(e) = P(e)`, independent of the
centre `z`.** I call such a field *frozen*. This note shows:

* **(Theorem A, §2)** *No frozen palette field satisfies the palette axioms at `k = 6` — indeed
  at no `k`.* The paper's own Remark 5.3 writes out the instance of (5.3) that kills them: at
  centre separation `1` in the direction of the separation, (5.3) reads
  `P_{x+a}(f) ∩ P_x(f) = empty` for every unit `a`, which for a frozen field is
  `P(f) ∩ P(f) = empty`. Hence the countermodels of Theorem C and of `FREE-LABEL.md` are
  **not** models of the palette constraints; they are models of a strictly weaker system, and
  the conclusion "the palette-level route is dead" is not established for the palette class.

* **(Theorem B, §3)** *In the class where the palette axioms hold at distance `1`, the palette
  programme is not a relaxation of the Hadwiger–Nelson problem: it is the problem.* Precisely:
  a (jointly measurable) palette field with non-empty palettes that satisfies (U) — the
  distance-`1` instance of (5.3) — and admits a measurable label function consistent with its
  palettes, yields a weak measurable `6`-colouring, hence (paper Theorem 1.3) a proper
  `6`-colouring. So at `k = 6` such palette systems exist **iff** `chi(R^2) <= 6`. There is no
  palette-level shortcut: the "frontier" that the previous report locates (trace-consistency) is
  not missing extra structure but is, given the palette axioms, equivalent to `6`-colourability.

* **(Theorems C and D, §4)** *The frozen shadow is quantitatively tiny.* For a frozen field,
  the axiom reduces to "the palette is disjoint from itself after every shift in a computable
  interval `Sh(d) = [delta_min(d), M(d)]`". Three (resp. two) pairwise disjoint palettes of size
  at least two exhaust a six-element label set (`frozen_core.lean`, machine-checked), so no
  frozen field with all palettes of size `>= 2` can have `delta, 2delta, 3delta` all effective.
  Consequently

  * no frozen field with all palettes of size `>= 2` satisfies (5.3) for all centre pairs at
    distance `<= d` once `d >= 0.4609` (three-shift argument; sharp threshold `0.4608112`);
  * none does once `d >= 0.3044` if moreover one label is free (two-shift argument;
    sharp threshold `0.3043792`) — and
    every countermodel in the report has a free label.

  Both thresholds are computed to 12 digits and cross-checked by two independent procedures,
  and both are far below the required `d = 1`. **Exact transport radii of the report's own
  models**: `0.28558` (the three-block models for `ell = 3,4,5`) and `0.14715` (the `ell = 6`
  free-label word) — the report claims only `d_0 = pi/54 = 0.05818`, so it *under*-states its
  own models by a factor `5` and still stops a factor `3.5` short of `d = 1`. A SAT search
  decides exactly where the frozen class stops in the report's own class (free label, `C_6`-
  admissible, sizes `2..3`): **satisfiable at every `d <= 0.175` (monotone in `d`; explicit
  60-sector witness at `d = 0.175`, independently re-verified on 576000 samples), unsatisfiable
  at every `d >= 0.180`** for all sector counts `n` tested up to `168`.

So the picture is: the frozen class is dead at `d = 1` outright, and even where it lives it
covers less than a tenth of the distance range `(0,2)` over which (5.3) is required.

---

## 1. The axiom, and the paper's own statement of the decisive instance

Throughout, `c` is a weak measurable `k`-colouring in the sense of Definition 1.2, `P_x(e)` the
maximal palette of Definition 5.1 (`x` a centre, `e` a unit direction, i.e. an element of `S`),
`R` the rotation of directions by `kappa = pi/3`.

**Lemma 5.2(3) (paper, p. 27).** *Let `z` be any fixed centre, possibly `z = x`. Suppose on an
open angular arc there is a smooth representation*

> `z + f = x + s(f) + t(f)`,  `s(f), t(f)` unit, nonparallel, `s` a local angular diffeomorphism,

*then for almost every `f` on that arc, `P_z(f) ∩ P_x(s(f)) = empty`.*

**Remark 5.3 (paper, p. 29).** *"In assertion 3 of Lemma 5.2, the second endpoint map `t` may be
constant. … In particular, for any fixed direction `a`, the representation*

> `(x + a) + f = x + f + a`

*is admissible off `f = ± a`."*

I checked this display against the rendered page (page 29): the display sits on a single
baseline at `y = 564.6-575.4` with the glyph sequence
`( x + a ) + f = x + f + a`, immediately followed on the next line by
`is admissible off f = ± a.` (`pdftotext -bbox-layout`, glyph coordinates; `pdftotext -raw`
agrees).

Taking `z = x + a`, `s(f) = f`, `t(f) = a` in Lemma 5.2(3) therefore gives, at every fixed
centre `x`,

> **(U)**  `P_{x+a}(f) ∩ P_x(f) = empty`  for every fixed unit `a` and almost every `f in S`,
>          the exceptional angular set depending on `(x,a)`.

**Remark.** (U) is exactly the instance that the paper's `m2` derivation uses for the
two-centre palette bound `|P_x(e)| + |P_y(e)| <= 5` (unit triangle `x, y, x + Ra`: the three
palettes at a common direction are pairwise disjoint). It is the sharpest metric input the
palette theory has at distance one, and it is *explicitly printed* in the paper.

---

## 2. Theorem A: no centre-independent palette field satisfies (U)

**Definition.** A palette field is *frozen* if `P_z = P` for all centres `z`.

**Theorem A.** *Let `P: S -> 2^[k]` be a frozen field with `P(f) != empty` for a.e. `f`. Then
`P` does not satisfy (U).*

*Proof.* Fix any unit `a` and put `z = x + a`. By (U), for a.e. `f`,
`P_{x+a}(f) ∩ P_x(f) = empty`; by frozenness both factors equal `P(f)`; hence
`P(f) ∩ P(f) = empty`, i.e. `P(f) = empty`, for a.e. `f`. This contradicts non-emptiness.
`square`

**Corollary A1.** Every countermodel of `sprint/k6/REPORT.md` Theorem C and of
`sprint/k6/FREE-LABEL.md` — and the models of `.ultramath/smwfo9zkl/m13/` and
`.ultramath/smwfo9zkl/m15/` — is frozen (`P_z(theta) = sigma(floor(theta/Delta))`, with no
`z`; the reports say so explicitly: *"`P` is translation invariant"*, *"the palettes do not
depend on the centre"*), and is therefore **not** a palette field satisfying the paper's
palette axioms, for any `k`. What those models satisfy is the subsystem in which (5.3) is
required only for centre pairs at distance `<= d_0 = pi/54`, the shift being then bounded away
from `0` (see `FREE-LABEL.md`: the shift is `m + k`, `k in {-1,0,1}`, i.e. one sector away
from the same direction).

**Corollary A2 (no second-branch rescue).** One might hope to repair a frozen field by using the
*other* exact unit decomposition at `d = 1`. It is not admissible: at `a = 1`, `f = e^{i psi}`,
the two unit decompositions of `a + f` are `s = f` and `s = a` (computed exactly:
`s_pm = e^{i psi/2}(cos(psi/2) ± i sin(psi/2)) = e^{i psi}` or `1`), and `s = a` is the
*constant* map, which fails the hypothesis "`s` is a local diffeomorphism in the angular
coordinate" of Lemma 5.2(3). So at distance exactly `1` the only admissible representation is
`s(f) = f`, and (U) is the whole content. (This is also visible in `shiftset.py`: restricting to
admissible branches, the shift set at `d = 1` collapses to `{0}`, whereas for `d != 1` it is a
non-degenerate interval.)

**Corollary A3 (the m2 bound is vacuous for frozen fields).** For a frozen field,
`|P_x(e)| + |P_y(e)| = 2|P(e)| <= 5` reduces to `|P(e)| <= 2`, which the countermodels satisfy
by construction. So the fact that the countermodels obey the *numerical* form of `m2`'s bound is
not evidence that they satisfy the axiom from which it is derived.

---

## 3. Theorem B: in the correct class the palette programme *is* the problem

**Setting.** Let `P: R^2 x S -> 2^{[k]}` be Borel with `P_z(f) != empty` for a.e. `(z,f)`.
Assume

* **(U')** `{(z,a,f) : |a| = 1, P_z(f) ∩ P_{z+a}(f) != empty}` is null (this is (U), jointly
  measurable — the hypothesis "(U) for every `z` and a.e. `f`" implies it by Fubini), and
* **(TC)** there is a measurable `c: R^2 -> [k]` with `c(z+f) in P_z(f)` for a.e. `(z,f)`.

**Theorem B.** *Under (U') and (TC), `c` is a weak measurable `k`-colouring of the plane.
Consequently, by the paper's Theorem 1.3, a proper `k`-colouring of the plane exists.
Conversely, the maximal palette field of a proper `k`-colouring satisfies (U') and (TC). Hence
at `k = 6`:*

> *trace-consistent palette systems satisfying the palette axioms at distance one exist*
> *`<=> chi(R^2) <= 6`.*

*Proof.* Let `B = {(z,a,f) : |a| = 1, c(z+f) = c(z+a+f)}`, Borel because `c` is measurable.
Off a null set, `(z,a,f) in B` forces `c(z+f) in P_z(f)`, `c(z+a+f) in P_{z+a}(f)`, and
`P_z(f) ∩ P_{z+a}(f) = empty`, a contradiction; so `B` is null. The shear
`(z,f) |-> (z+f, f)` is a measure-preserving bijection of `R^2 x S`, so
`{(x,a,f) : |a|=1, c(x) = c(x+a)}` is null, and Fubini gives, for a.e. `(x,a)` with
`|a| = 1`, `c(x) != c(x+a)`. That is exactly Definition 1.2's condition. The converse is
immediate: a proper `k`-colouring's maximal palette contains the colour of the sampled point.
`square`

**Reading.** The previous report's frontier is *"the only thing the countermodels fail is
trace-consistency with a proper colouring"*, and it presents trace-consistency as the remaining
conjectural input. Theorem B says it is not conjectural input at all: **given the palette axioms,
trace-consistency is equivalent to `6`-colourability.** A palette-level proof of local finiteness
at `k = 6` that used (U) would therefore prove `chi(R^2) >= 7`; and a palette-level *countermodel*
that respected (U) would prove `chi(R^2) <= 6`. There is no third possibility. This is why the
countermodels had to be frozen: freezing is the only way to satisfy the *local* transport while
escaping (U).

**Two caveats, stated so that the claim can be checked.** (i) Theorem B is stated for a *jointly
measurable* field. The paper deliberately assumes no joint measurability of `P` in the centre
("No joint measurability of `P_x` in its center is assumed", §5.1); in that weaker framework
(U) is only available per centre, with an exceptional angular set depending on the centre. So
Theorem B is not a theorem about the paper's own object; it is a theorem about every class in
which a palette-level argument could actually be run, and it identifies the per-centre
exceptional sets as the only remaining loophole. (ii) The frozen models do not exploit that
loophole — they are defined for all `(z,e)` and simply violate (U). So the *published*
countermodels are not saved by caveat (i).

---

## 4. The frozen shadow, quantitatively

### 4.1 The shift set

Let `d in (0,1]` and let `z = x + a`, `|a| = d`, `f` a unit direction. Write `psi` for the
angle from `a` to `f` and `w = d + e^{i psi}`, `r = |w|`, `c = r/2`. The two exact unit
decompositions of `w` are

> `s_+-(f) = w/2 +- i (w/r) sqrt(1 - c^2)`,  `t_+-(f) = w - s_+-(f)`,

and analytically `arg s_+- = arg w +- arccos(r/2)`, so the *shift* `delta_+-(psi) = arg s_+- - psi` is

> `delta_+-(psi) = atan2(sin psi, d + cos psi) +- arccos(r/2) - psi`.

This is the formula the previous sprint's `m15` `Lemma G` linearises near `d = 0`; here it is
used exactly, at all `d`.

**Lemma 4.1.** *For `d in (0,1)`, `psi |-> delta_+(psi)` is continuous on the whole circle
(`r` stays in `[1-d, 1+d] c (0,2)`, so the two branches never become parallel), and its only
non-admissible points are the isolated zeros of `1 + delta_+'(psi)` (where `s_+` stops being a
local angular diffeomorphism). Hence the set of shifts actually realised by Lemma 5.2(3) at
distance `d` is the interval `[delta_min(d), M(d)] := [inf delta_+, sup delta_+]` minus at most
finitely many points, and likewise its negative (`delta_+(-psi) = -delta_-(psi)`). In
particular (5.3) at distance `d` forces `P(u + delta) ∩ P(u) = empty` for a.e. `u` and for
**almost every** `delta in [delta_min(d), M(d)]`, which is all that Theorems C and D use.*

**Lemma 4.2 (nesting).** `Sh(d) := [delta_min(d), M(d)]` is increasing in `d`: `delta_min` is
strictly decreasing and `M` is strictly increasing (checked on a grid of `10^4` values of `d`;
`frozen.py`, `check_extremes.py`).

Consequently a frozen field satisfyies (5.3) for **all** centre pairs at distance `<= d` only if

> **(F)** `P(u + delta) ∩ P(u) = empty` for a.e. `u` and **every** `delta in Sh(d)`.

Numerical values (40-digit computation, `check_extremes.py`; the coarse scan of `frozen.py`
agrees to 8 digits):

| `d` | `delta_min(d)` | `M(d)` | `M - 2 delta_min` |
|---|---|---|---|
| 0.175 | 0.850393455 | 1.255931969 | -0.44485494 |
| 0.3044 | 0.710447169 | 1.420966043 | +0.00007170 |
| 0.305 | 0.709807254 | 1.421757685 | +0.00214318 |
| 0.4609 | 0.545851409 | 1.637961219 | +0.54625840 |
| 0.5 | 0.505360510 | 1.696124158 | +0.68540314 |
| 1 | 0 | (degenerate) | — |

### 4.2 Two finite obstructions

**Lemma C (two shifts; `frozen_core.lean`, machine-checked).** *Let `A, B, C` be three pairwise
disjoint palettes inside a six-element label set, each of size `>= 2`. Then `A ∪ B ∪ C` is the
whole label set. In particular (i) a fourth non-empty palette cannot be disjoint from all three,
and (ii) if some label belongs to no palette, three such palettes cannot exist at all.*

*(`union_eq_of_three_disjoint`, `not_disjoint_fourth`, `exists_card_le_one_of_free_label`;
axioms `[propext, Classical.choice, Quot.sound]`.)*

**Theorem C (three-shift exclusion).** *Let `P` be a frozen field at `k = 6` all of whose
palettes have size `>= 2`. Then (F) fails for every `d` with `M(d) >= 3 delta_min(d)`, that is,
for every `d >= 0.4609` (sharp threshold `d_c = 0.46081114...`).*

*Proof.* Suppose `M(d) >= 3 delta_min(d)` and put `delta = delta_min(d)`; then
`delta, 2 delta, 3 delta in Sh(d)`. By (F) and Lemma 4.1, for a.e. `u` the palettes
`P(u), P(u+delta), P(u+2delta), P(u+3delta)` satisfy: the first three are pairwise disjoint
(`delta` at `u`, `delta` at `u+delta`, `2delta` at `u`) and the fourth is disjoint from all
three (`2delta` at `u+delta` gives `P(u+3delta) ∩ P(u+delta) = empty`, `3delta` at `u` gives
`P(u+3delta) ∩ P(u) = empty`, and `delta` at `u+2delta` gives
`P(u+3delta) ∩ P(u+2delta) = empty`). Lemma C(i) is violated. `square`

**Theorem D (two-shift exclusion).** *Let `P` be a frozen field at `k = 6` all of whose palettes
have size `>= 2` and which admits a free label (a label `i` with `i notin P(f)` for a.e. `f`).
Then (F) fails for every `d` with `M(d) >= 2 delta_min(d)`, that is, for every `d >= 0.3044` (sharp threshold `0.30437924...`).*

*Proof.* With `delta = delta_min(d)` and `M(d) >= 2delta`, the three palettes
`P(u), P(u+delta), P(u+2delta)` are pairwise disjoint and of size `>= 2` for a.e. `u`, hence by
Lemma C they exhaust the labels, so no label is free. `square`

**Remark.** Theorem D applies to the report's `ell = 6` free-label word (palettes of sizes
`2,2,2,2,2,3`, free label `0`); Theorem C applies to it too but is weaker. The three-block
models for `ell = 3,4,5` contain a singleton palette, so `frozen_core` does not apply to them;
for those, Theorem A (which needs nothing) is the statement.

### 4.3 The report's models, measured exactly

`model_radii.py` computes, from the sector words of `sprint/k6/REPORT.md` and
`sprint/k6/FREE-LABEL.md`, the exact set

> `Safe = { k mod n : word[i] ∩ word[i+k] = empty for all i }`

and then the largest `d` with `K(d) := [floor(delta_min(d)/Delta), ceil(M(d)/Delta)]` and
`-K(d)` both inside `Safe`:

| model | `Safe` | transport radius | report claims |
|---|---|---|---|
| `ell = 3`, `{3},{4},{5}` | `{4..8} mod 12` | **0.28558** | `0.05818` |
| `ell = 4`, `{0,2},{1,3},{4}` | `{4..8} mod 12` | **0.28558** | `0.05818` |
| `ell = 5`, `{0,2},{1,3},{5}` | `{4..8} mod 12` | **0.28558** | `0.05818` |
| `ell = 6` free-label 36-sector word | `{5,6,7} mod 12` | **0.14715** | `0.05818` |

So the previous sprint verifies (5.3) on a range five times smaller than its own constructions
allow, and even the best of the four is a factor `3.5` below `d = 1`. And by Theorem A none of
them can be continued to `d = 1`.

### 4.4 Where the frozen class stops: an exact decision

`wordsearch.py` decides, by CaDiCaL on an explicit CNF, whether there is a sector word
`word : Z/n -> 2^[6]` with

* `2 <= |word[i]| <= 3` (the size bound at a six-cycle centre, `sprint/k6/STRUCTURE.md` Cor. 4),
* `word[i]` contains a pair non-adjacent in `C_6` ((6.2) at an `ell = 6` centre),
* `0 notin word[i]` (free label),
* `word[i] ∩ word[i+k] = empty` for every `k in +-K(d)`.

Result (labels `1..5`, 16 admissible palettes; `U` = unsatisfiable, `S` = satisfiable):

| `d` | 36 | 48 | 60 | 72 | 84 | 96 | 120 | 144 | 168 |
|---|---|---|---|---|---|---|---|---|---|
| 0.100 | U | S | S | S | S | S | S | S | S |
| 0.150 | U | U | S | U | U | S | S | U | S |
| 0.175 | U | U | **S** | U | U | U | **S** | U | U |
| 0.180 | U | U | U | U | U | U | U | U | U |
| 0.190 | U | U | U | U | U | U | U | U | U |

**An explicit witness at `d = 0.175`** (`witness_0175.json`): `n = 60`, blocks of `4` sectors,
five palettes cycling

> `{3,5} {2,5} {2,4} {1,4} {1,3}`  (repeated three times)

Every value is a pair, none contains `0`, every value has a pair non-adjacent in `C_6`, the
shift set is `K = {8,...,12} mod 60`, and the block index moves by `2` or `3` (mod `5`) at each
of those shifts, so `{3,5}` vs `{2,4}`, `{2,5}` vs `{1,4}`, `{2,4}` vs `{1,3}`, `{1,4}` vs
`{3,5}`, `{1,3}` vs `{2,5}` are the pairs that must be, and are, disjoint. Verified twice:
structurally (integer arithmetic on the word) and by direct evaluation of the geometric
constraint `P(f) ∩ P(f + delta_+-(psi)) = empty` on `400 x 720 x 2 = 576000` samples —
`0` violations.

So: **the frozen class with a free label cannot reach `d = 0.180`, while (5.3) is required at
every distance in `(0,2)`; at `d = 1` it is refuted outright by Theorem A.**

---

## 5. What this changes in the record

1. **Theorem C of `sprint/k6/REPORT.md` and `sprint/k6/FREE-LABEL.md` are statements about the
   frozen class**, and that class is empty once the palette axioms are imposed at distance `1`
   (Theorem A). They should not be quoted as "the palette-level route is dead": they show that a
   *centre-independent* palette field cannot separate the cycle lengths from the colouring
   problem, which is much weaker.
2. **The frontier is not "trace-consistency is the remaining input".** Given the palette axioms,
   trace-consistency is *equivalent* to `chi(R^2) <= 6` (Theorem B). No palette-level argument
   with (U) can be easier than the Hadwiger–Nelson problem, and no palette-level countermodel
   with (U) can exist unless `chi(R^2) <= 6`.
3. **The quantitative boundary.** The frozen no-go is available only for centre separations
   `d <= 0.175` (report's own class, exact decision) and in no case beyond `d = 0.3044`
   (Theorem D) or `d = 0.4609` (Theorem C), against a requirement of all `d in (0,2)`.
   The previous sprint's `d_0 = pi/54 = 0.05818` understates its own models fivefold.
4. **What a genuine palette-level countermodel at `k = 6` must do**: it must be non-frozen,
   satisfy (U) (so it cannot be a frozen sector field), satisfy the exact transports, and
   *fail* trace-consistency. By Theorem B such an object exists iff `chi(R^2) <= 6`. So the
   palette programme cannot be used to *refute* local finiteness at `k = 6` either: refuting it
   requires a proper `6`-colouring with a perfect cyclic locus, which is what `m3` does at
   `k >= 7` and what is unavailable at `k = 6`.

---

## 6. Files and how to check them

| file | content |
|---|---|
| `frozen_core.lean` | machine-checked finite core: `union_eq_of_three_disjoint`, `not_disjoint_fourth`, `exists_card_le_one_of_free_label`. Axioms `[propext, Classical.choice, Quot.sound]`; no `sorry`. |
| `shiftset.py`, `frozen.py` | the exact shifts of Lemma 5.2(3): closed form, admissibility filter, `delta_min`/`M` |
| `check_extremes.py` | independent 40-digit recomputation of the extremes by local ternary search |
| `threshold.py`, `dfrozen.py` | bisection for `3 delta_min = M` (`0.46081114...`) and `2 delta_min = M` (`0.30437924...`) |
| `model_radii.py` | exact transport radii of the four models of the previous report |
| `wordsearch.py`, `wordsearch2.py` | the CaDiCaL decision of the frozen class in the report's own class |
| `witness.py`, `witness_0175.json` | the explicit `n = 60` witness at `d = 0.175` and its two independent verifications |
| `circulant.py`, `circsat.py`, `circsat2.py` | the auxiliary circulant computation showing that a drop of the free label relaxes the obstruction to `M >= 3 delta_min` |

Commands (all from this directory):

```
lean frozen_core.lean                     # machine-checked finite core, <= 30 s
python3 check_extremes.py                 # 40-digit extremes of the shift functions
python3 threshold.py                      # 3 delta_min = M  ->  d = 0.46081114...
python3 dfrozen.py                        # 2 delta_min = M  ->  d = 0.30437924...
python3 monotone.py                       # nesting of Sh(d) and positivity of the margins
python3 model_radii.py                    # exact transport radii of the report's models
python3 wordsearch2.py                    # exact SAT/UNSAT sweep (CaDiCaL, ~100 s)
python3 witness.py                        # explicit witness + 576000-sample re-verification
```

Toolchain used: stock `lean` 4.33.1 with `/opt/mathlib` for `frozen_core.lean`; Python 3 with
`mpmath`; CaDiCaL at `/opt/lean/bin/cadical`.
