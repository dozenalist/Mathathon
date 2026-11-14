# The exact frozen-field threshold at six colours

**Member m8, swarm smwg1r9lg, direction d6 (board id d4).** Paper: `attachments/here-are-three-files-ni5n/paper.pdf`,
Lemma 5.2(3), Remark 5.3, Corollary 5.4 (display (5.7)). The record referred to is `sprint/k6/REPORT.md`
and the two earlier frozen-field notes `.ultramath/smwfwi7rh/m11/RESULTS.md` (m11) and
`.ultramath/smwfwi7rh/m13/RESULTS.md` (m13).

---

## 0. The result

A **frozen field** at `k` colours is a measurable map `P : S -> 2^[k] \ {empty}` on the direction
circle (no dependence on the centre). By m11 Theorem A no frozen field satisfies the paper's
transport axiom (5.3) at centre separation `1`, so the frozen class is empty once (5.3) is imposed at
`d = 1`. m11 quantified the gap from below (`d <= 0.4609`, or `0.3044` with a free label) and m13
quantified a *sector* subclass. This note decides the question exactly, for the whole class.

**Theorem A (exact frozen-field threshold, k = 6).** Let `0 < D < 1`. There is a frozen
measurable field `P : S -> 2^[6] \ {empty}` satisfying the paper's (5.3) for **every** pair of
centres at distance `<= D` if and only if

> `D <= D* := 2 cos(2 pi/9) - 1 = 0.5320888862...`,

the unique root in `(0,1)` of `D^3 + 3 D^2 = 1`. The extremal field is explicit: the 18-sector
field `P(theta) = {floor(9 theta/pi) mod 6}` (all palettes singletons, sector width `pi/9`), and
`D*` is where its transport radius ends. `1 - D* = 0.46791...` is the exact amount by which the
frozen class falls short of the separation `d = 1` that the paper's Lemma 6.7 needs.

**Theorem B (general form).** Fix `k >= 4`, `m in {1,...,k}` and `D in (0,1)`, and put
`L = 2 pi`, `a(D) = 2 arcsin((1-D)/2)`, `b(D) = 2 arcsin((1+D)/2)`.

* (i) *(necessity, every `m`)* If a frozen field with `|P(f)| >= m` for a.e. `f` satisfies (5.3) at
  every centre separation `<= D` and `b(D) > 2 a(D)` (i.e. `D > 0.3043792`), then there is an
  integer `N >= 1` with

  > `k N a(D) >= m L`   and   `k N b(D) <= (k - m) L`.

  In particular `b(D) <= (k/m - 1) a(D)`.

* (ii) *(sufficiency at `m = 1`, and exactness)* If `k N a(D) >= L` and `k N b(D) <= (k-1) L` for
  some integer `N`, the frozen field with `k N` sectors of width `L/(kN)` labelled
  `0,1,...,k-1` cyclically satisfies (5.3) at every centre separation `<= D`. Conversely a frozen
  field with nonempty palettes satisfies (5.3) at every separation `<= D` only if such an `N`
  exists — the case `D <= 0.3043792`, where (i) is not available, being settled by the explicit `N`
  listed in §3.1. Hence at `m = 1` and `k >= 4`: `D` is feasible iff such an `N` exists.

* (iii) *(thresholds)* For `m = 1` the supremum of feasible `D` is

  > `D*(k,1) = max_{N >= 1} min { 1 - 2 sin(pi/(kN)) , 2 sin((k-1) pi/(kN)) - 1 }`,

  and `D` is feasible iff `D <= D*(k,1)`. The same formula with `(k-m)` in place of `(k-1)` is the
  value of the criterion (i) for `m >= 2`, and is a rigorous upper bound for the true threshold.

  At `k = 6`: `D*(6,1) = 2cos(2pi/9) - 1 = 0.5320888862` (exact, Theorem A);
  `D*(6,2) = 2 sin(2pi/9) - 1 = 0.2855752194` (criterion; the true threshold lies in
  `[0.2855752194, 0.3043792]`, both ends certified — see §4);
  `D*(5,1) = 0.4862896510`; `D*(5,2) = 2 sin(pi/5) - 1 = 0.1755705046`.

The last two numbers are exactly m13's two published constants `0.2855752194` ("without a free
label") and `0.1755705045` ("with a free label"): m13's sector computation is the `(k,m) = (6,2)`
and `(5,2)` member of this family. The `m = 2` bound `b <= 2a` is strictly stronger than **both** of
m11's Theorems C and D, and unlike m11's Theorem D it needs no free-label hypothesis (see §4).

The mechanism is not an estimate. (5.3) at a frozen field says that two directions sharing a label
must avoid a band of angular separations around `pi/3` whose width grows with `D`; a band of that
shape forces every label's support to be a union of narrow clusters separated by at least `b`, and
`k` such supports must cover the direction circle. Covering and the cluster geometry are in exact
opposition, and the integer `N` (the number of clusters per label) is what makes the opposition
sharp: `D*` is the last point at which an integer fits.

---

## 1. The transport axiom for a frozen field: one band condition

Let `S = S^1` with its angular measure, `L = 2 pi`, and write `c(f,g)` for the circular distance in
`[0,pi]` and `|f - g| = 2 sin(c(f,g)/2)` for the chordal distance. Fix `0 < D < 1`.

### 1.1 The shift set

**Lemma 1.1.** *Fix a separation `d in (0,1)`, centres `x` and `z = x + a` with `|a| = d`, and a
unit direction `f`. The admissible representations `z + f = x + s + t` of Lemma 5.2(3) (with
`s, t` unit, `s` a local angular diffeomorphism, `s` not parallel to `t`) have a shift
`delta = c(f,s) = arg s - arg f` in `[0,pi]`, and the set of shifts realised as `a` and `f` vary
with `|a| = d` is exactly*

> `Sh(d) = [a(d), b(d)],   a(d) = 2 arcsin((1-d)/2),  b(d) = 2 arcsin((1+d)/2)`,

*taken with both signs (`delta` and `-delta`).*

*Proof.* `s + t = a + f` with `|s| = |t| = 1` is a unit decomposition of the vector `w = a + f`.
Such decompositions exist iff `|w| <= 2`, and there are exactly two, symmetric about `w`; they are
`s = w/2 +- i (w/|w|) sqrt(1 - |w|^2/4)`, and `arg s = arg w +- arccos(|w|/2)`. Hence the pair
`(f,s)` is realisable for some `a` with `|a| = d` iff there is a unit vector `t` with
`a = s + t - f`, i.e. iff the circle of radius `1` about `s - f` meets the circle of radius `d`
about `0`. That holds iff `| |s-f| - 1 | <= d <= |s-f| + 1`; the right inequality is automatic for
`d <= 1`. With `|s - f| = 2 sin(delta/2)`, `delta in [0,pi]`, this reads
`1 - d <= 2 sin(delta/2) <= 1 + d`, i.e. `delta in [a(d), b(d)]`. Non-parallelism of `s` and `t`
fails only at `|w| in {0,2}`, i.e. only at `d = 1`; for `d < 1` both decompositions are admissible
except at the isolated directions where `s` fails to be a local diffeomorphism (isolated zeros of
`delta'(psi)`, m11 Lemma 4.1). `square`

The closed form agrees to nine digits with m11's independently computed table
(`d = 0.5`: `0.505360510 / 1.696124158`; `d = 0.4609`: `0.545851409 / 1.637961219`;
see `check1.py`), and `Sh(d)` is increasing in `d` (m11 Lemma 4.2). Note `Sh(d) -> {pi/3}` as
`d -> 0`, which is (5.7) at `d = 0`.

### 1.2 From (5.3) to a null band

**Lemma 1.2 (band form).** *Let `P : S -> 2^[k]` be measurable and frozen. Suppose that for every
fixed pair of centres at distance `<= D` and for each of the two branches of Lemma 5.2(3), (5.3)
holds. Then for every label `i` the set*

> `{(f,g) in S x S : i in P(f) cap P(g), 1 - D < |f - g| < 1 + D}`

*is null. Equivalently: `P(f) cap P(g) = empty` for almost every pair of directions whose chordal
distance lies in `(1-D, 1+D)`.*

*Proof.* Fix `d in (0,D)` and a branch `eps` and put `A_i = {f : i in P(f)}`, measurable. Writing
`f = e^{i theta}`, `a = d e^{i alpha}`, `psi = alpha - theta`, the branch is
`s = e^{i(theta + delta_eps(psi))}` with `delta_eps` the smooth shift of Lemma 1.1 (Lemma 4.1 of
m11). (5.3) says: for each fixed `alpha`, for almost every `theta`,
`not (theta in A_i and theta + delta_eps(alpha - theta) in A_i)`. Substituting `psi = alpha - theta`
(a measure preserving change of variables for each fixed `alpha`), the bad set
`Z = {(alpha, psi) : alpha - psi in A_i, alpha - psi + delta_eps(psi) in A_i}` is measurable and
every `alpha`-section of `Z` is null, so `Z` is null by Fubini. The map

> `Psi(alpha, psi) = ( e^{i(alpha-psi)}, e^{i(alpha-psi+delta_eps(psi))} )`

has Jacobian determinant `delta_eps'(psi)` (in the angular coordinates the map is
`(alpha,psi) |-> (alpha - psi, alpha - psi + delta_eps(psi))`, a shear composed with
`psi |-> psi + delta_eps(psi)`). Off the finitely many zeros of `delta_eps'` it is a local
diffeomorphism, so the image of the null set `Z` is null; the zeros themselves are finitely many
lines `psi = const`, whose images are null. Hence the bad set of pairs at separation `d` is null.
Taking a sequence `d_n -> D` and a countable union over the two branches and the `k` labels gives
the claim for the union of the bands, which is the open band `(1-D, 1+D)`. `square`

*Remark 1.3.* Nothing here uses joint measurability of `P` in the centre; the field is frozen, so a
single measurable `P` on the circle carries everything. Conversely, the band condition of Lemma 1.2
implies (5.3) at every separation `<= D`: at separation `d`, the realised shifts are in `Sh(d)`, and
the only shifts not in the open band are the two endpoints `delta = a(d), b(d)`, attained for
finitely many `f` (the extrema of `delta_eps`), a null set of directions. So Lemma 1.2 is an
equivalence at the level of a.e. statements, and no generality is lost by working with the band.

**Corollary 1.4.** In terms of circular distance, the forbidden band is
`c(f,g) in [a(D), b(D)]`; the chordal and circular formulations agree because `a(D), b(D) <= pi`
(`b(D) <= pi` always, `b(D) = pi` only at `D = 1`).

---

## 2. The cluster-packing lemma

Throughout this section `0 < a < b <= L/2`, `L > 0`, the circle is `R/LZ` and `c(.,.)` is the
circular distance. A set `A` is **`(a,b)`-free** if no two of its points are at circular distance
in `(a,b)`.

**Lemma 2.1 (structure, closed case).** *Let `F` be closed and suppose every pair `x,y in F` has
`c(x,y) not in (a,b)`. If `b > 2a` then `F` is a finite disjoint union of closed classes
`C_1,...,C_n` ("clusters") with*

* *`c(x,y) <= a` for all `x,y in C_j` (circular diameter `<= a`);*
* *`c(x,y) >= b` for all `x in C_j`, `y in C_l`, `j != l`;*
* *`n <= L/b`.*

*Proof.* Define `x ~ y` iff `c(x,y) <= a` on `F`. Reflexive and symmetric. Transitive: if
`c(x,y) <= a` and `c(y,z) <= a` then `c(x,z) <= 2a < b` by the triangle inequality, and `c(x,z)` is
not in `(a,b)`, hence `c(x,z) <= a`. The classes are closed (`F` closed, `c` continuous), of
circular diameter `<= a`. A cross pair has distance `> a` (else it relates the two points) and not
in `(a,b)`, so every cross pair has distance `>= b`. Consecutive classes in the circular order are
therefore separated by gaps of length `>= b`, so `n b <= L`. `square`

**Lemma 2.2 (packing bound).** *Let `A` be measurable with `(A x A) cap {a < c < b}` null and
`b > 2a`. Then*

> `|A| <= max_{n >= 1} min(n a, L - n b) <= L a/(a + b)`.

*Proof.* For `eps > 0` take `F <= A` closed with `|A \ F| < eps`. If `x,y in F` had
`c(x,y) in (a,b)` then, `c` being continuous and `(a,b)` open, a whole product neighbourhood of
`(x,y)` would lie in the bad set, contradicting its nullity; so `F` satisfies the hypothesis of
Lemma 2.1 pointwise, and its clusters `C_1,...,C_n` have diameter `<= a` and are `b` apart. Each
`C_j` lies in an arc of length `<= a` (a set of circular diameter `<= a < L/2` lies in an arc of
that length) and consecutive clusters are separated by gaps `>= b`, so
`L >= sum_j |arc(C_j)| + n b >= |F| + n b` and `|F| <= n a`. Hence
`|A| <= min(n a, L - n b) + eps`, and letting `eps -> 0` (and noting the last display is
`<= L a/(a+b)` for every integer `n`: if `n a <= L - n b` then `n(a+b) <= L` and `n a <= L a/(a+b)`,
otherwise `L - n b <= L a/(a+b)` because `n(a+b) >= L`) gives the claim. `square`

*Remark 2.3.* This is where `b > 2a` is used. It holds automatically in the application: at the
threshold `D* = 0.532` one has `a = 0.4723`, `b = 1.7453 > 2a = 0.9446`, and `b > 2a` is equivalent
to `D > 0.3043792` (the `m = 2` continuum bound, m11 Theorem D).

---

## 3. Proof of Theorems A and B

### 3.1 Necessity

Let a frozen field `P` with `|P(f)| >= m` a.e. satisfy (5.3) at all separations `<= D`. Put
`A_i = {f : i in P(f)}`. By Lemma 1.2, each `A_i` is `(a(D), b(D))`-free (up to a null set, which
we discard).

*Case `D > 0.3043792`* (`b > 2a`, Lemma 2.2 available). Lemma 2.2 gives
`|A_i| <= Psi(D) := max_{n >= 1} min(n a, L - n b)` for every `i`. By `|P| >= m` the `A_i` cover
the circle with multiplicity at least `m`, so

> `m L <= sum_i |A_i| <= k Psi(D)`, i.e. `Psi(D) >= m L / k`.

Therefore some integer `n` has `n a >= m L/k` and `L - n b >= m L/k`, i.e.
`n >= m L/(k a)` and `n <= (k-m) L/(k b)`. This is (i). It also gives an upper bound in closed
form: `Psi(D) <= L a/(a+b)`, hence `m(a+b) <= k a`, i.e. `b <= (k/m - 1) a` — already enough to
see that the threshold is strictly below `d = 1`. (For `m = 1`, `k = 6` this reads `b <= 5a`, which
is `D <= 0.6234`; the integrality of `n` is what sharpens `0.6234` to `0.5321` in §3.3.)

*Case `D <= 0.3043792`.* Here no cluster argument is available (`b <= 2a`), and none is needed for
the exactness claim at `m = 1`: for `k = 4,5,6,7,8` a single integer `N` works for *every*
`D <= 0.3043792` simultaneously, because `a(D) >= a(0.3043792) = 0.71045` and
`b(D) <= b(0.3043792) = 1.42097`, so it is enough that `N k (0.71045) >= 2 pi` and
`N k (1.42097) <= (k-1) 2 pi`. The admissible `N` are `N = 3` for `k = 4` (`a >= 0.5236`,
`b <= 1.5708`) and for `k = 5` (`a >= 0.4189`, `b <= 1.6755`), and `N = 2` for `k = 6`
(`a >= 0.5236`, `b <= 2.6180`), `k = 7` (`a >= 0.4488`, `b <= 2.6928`) and `k = 8`
(`a >= 0.3927`, `b <= 2.7489`). Hence for `m = 1`, `k >= 4` the criterion (i) holds for every `D`,
and with §3.2 it is equivalent to feasibility.

### 3.2 Sufficiency and exactness at `m = 1`

Suppose `N >= 1` with `k N a(D) >= L` and `k N b(D) <= (k-1) L`. Partition the circle into `k N`
arcs of width `w = L/(k N)` and give arc `j` the singleton palette `{j mod k}`. Then

* each point carries exactly one label, so palettes are nonempty and singletons;
* for a fixed label, the arcs are `k` apart, so the circular distances between points of `A_i` lie
  in `(0, w) union ( (k-1)w, (k+1)w ) union ... `; the smallest value exceeding `w` is `(k-1) w`;
* `w = L/(kN) <= a(D)` and `(k-1) w = (k-1)L/(kN) >= b(D)`;

so no pair of directions sharing a label has circular distance in `[a(D), b(D)]`, and by Remark 1.3
(5.3) holds at every centre separation `<= D`.

Together with necessity, then: a frozen field with nonempty palettes exists iff there is an integer
`N` with `k N a(D) >= L` and `k N b(D) <= (k-1)L`. Solving the two inequalities for `D` gives

> `D <= 1 - 2 sin(pi/(kN))` and `D <= 2 sin((k-1) pi/(kN)) - 1`,

so the supremum of feasible `D` is `max_N min(...)`, which is finite and attained.

### 3.3 `k = 6`, `m = 1`: the exact value

`a(D) = L/(6N)` is equivalent to `D = 1 - 2 sin(pi/(6N))`, and `b(D) = 5L/(6N)` to
`D = 2 sin(5 pi/(6N)) - 1`. For `N = 3` both hold at `D = 2 sin(5 pi/18) - 1`, and
`sin(5 pi/18) = cos(2 pi/9)`, so that value is `D* = 2 cos(2 pi/9) - 1`. Indeed at `D*`
`a(D*) = 0.47229 >= pi/9 = 0.34907` and `b(D*) = 5 pi/9` exactly, so `N = 3` is admissible at `D*`.
For every other `N`:

* `N = 1`: `min = 0 < D*`;
* `N = 2`: `min = 1 - 2 sin(pi/12) = 0.4823619098 < D*`;
* `N = 4`: `min = 2 sin(5 pi/24) - 1 = 0.2175228580 < D*`;
* `N >= 5`: `5 pi/(6N) <= pi/6`, so `2 sin(5 pi/(6N)) - 1 <= 0 < D*`.

Hence `D* = max_N min(...)` — the maximum is attained at `N = 3` — and `D` is feasible iff
`D <= D*`.

**The algebraic identity.** `D* = 2 cos(2 pi/9) - 1`. With `x = 2 cos(2 pi/9)`, the triple angle
formula `2 cos 3 t = x^3 - 3x` at `t = 2 pi/9` gives `x^3 - 3x = 2 cos(2 pi/3) = -1`; substituting
`x = D + 1` gives `(D+1)^3 - 3(D+1) + 1 = D^3 + 3 D^2 - 1 = 0`. `D |-> D^3 + 3 D^2` is strictly
increasing on `(0,1)` from `0` to `4`, so `D*` is its unique root there. Numerically
`D* = 0.5320888862379560704047853011108333478717...` (`check1.py`, 40 digits; the cubic evaluated
at the two ends of the certified rational enclosure straddles `0` — `verify_exact.py`).

**Both admissibility conditions at `D*` hold exactly.** `b(D*) = 2 arcsin(cos(2 pi/9)) = 2(pi/2 - 2 pi/9) = 5 pi/9 = 5 L/18` using `arcsin(cos t) = pi/2 - t` on `[0, pi/2]`; and
`a(D*) >= pi/9 = L/18` because `1 - cos(2 pi/9) = 2 sin^2(pi/9)` and, writing
`sin(pi/9) = 2 sin(pi/18) cos(pi/18)`, the inequality `2 sin^2(pi/9) >= sin(pi/18)` is equivalent to
`4 sin(pi/9) cos(pi/18) >= 1`, i.e. by `2 sin A cos B = sin(A+B) + sin(A-B)` to
`2(sin(pi/6) + sin(pi/18)) >= 1`, i.e. to `2 sin(pi/18) >= 0`. So `N = 3` is admissible at `D*`
with slack only in the `a`-condition.

For `D > D*`: `b(D) > 5 pi/9`, so `6 N b <= 5 L` forces `N <= 2`; `N = 2` needs
`a(D) >= L/12 = pi/6`, i.e. `D <= 1 - 2 sin(pi/12) = 0.4824 < D*`; `N = 1` needs `D = 0`. So no `N`
exists and there is no frozen field. **Theorem A is proved.**

---

## 4. Tables and consequences

`verify_exact.py` computes every entry below in rational interval arithmetic (`pi` from Machin's formula,
`sin`/`cos` from Taylor series with an alternating-remainder bound, all comparisons decided on
`Fraction` endpoints).

**Criterion value** `C(k,m) := max_N min { 1 - 2 sin(pi/(kN)), 2 sin((k-m) pi/(kN)) - 1 }`:

| `k` | `m = 1` (exact) | `m = 2` | `m = 3` |
|---|---|---|---|
| 4 | 0.4142135624 = `sqrt2 - 1` (`N=3`) | 0 (`N=3`) | `<= 0` |
| 5 | 0.4862896510 (`N=3`) | 0.1755705046 = `2 sin(pi/5)-1` (`N=3`) | `<= 0` |
| 6 | **0.5320888862 = `2cos(2pi/9)-1`** (`N=3`) | 0.2855752194 = `2sin(2pi/9)-1` (`N=3`) | 0 (`N=3`) |
| 7 | 0.5636630 (`N=3`) | 0.3603455 (`N=3`) | 0.1266401 (`N=3`) |
| 8 | 0.6098194 (`N=2`) | 0.4142136 (`N=3`) | 0.2175229 (`N=3`) |

(`<= 0` means: the criterion has no positive solution, so no frozen field of that multiplicity at any
`D > 0` in the regime `b > 2a`, i.e. for `D > 0.3043792`.)

Only the `m = 1` column is proved to be the exact threshold (Theorem B(ii); the `D <= 0.3044`
case is settled by the explicit `N` of §3.1). For `m >= 2` the column is the value of the criterion
(i); the part of it above `0.3043792` is a rigorous upper bound on the threshold, and below that
level it is only a lower-bound-by-construction. The `m = 2` entry is where m13's constants appear
and where the certified bracket `[0.2855752194, 0.3043792]` lives.

**Corollary 4.1 (strengthens m11 Theorems C and D).** m11 Theorem C excludes frozen fields with all
palettes of size `>= 2` for every `d >= 0.4608111`; m11 Theorem D does the same under the extra
hypothesis of a free label, for `d >= 0.3043792`. Theorem B(i) with `m = 2` gives
`b <= 2a`, i.e. the same constant `0.3043792` **without the free-label hypothesis**, and strictly
below m11's Theorem C. (The integrality-refined value of the criterion is `0.2855752`; the explicit
double cover of §7 shows the true `m = 2` threshold is at least that, and the cluster argument does
not reach it because at `0.2855752` one has `b < 2a`, where Lemma 2.1 does not apply. So the
`m = 2` threshold is bracketed by `[0.2855752194, 0.3043792]` and I do not claim its value.)

**Corollary 4.2 (m13's constants are members of this family).** m13's sector computation gives
`satisfiable iff K <= floor(m/5)`, with sharp radius `0.1755705045` for the free-label class and
`0.2855752194` without it. Those are `2 sin(pi/5) - 1` and `2 sin(2pi/9) - 1`, i.e. the
`(k,m,D) = (5,2)` and `(6,2)` values of the criterion above. So m13's numbers are the two-label
members of the same family, and their sector ansatz with a fixed number of clusters per label
reproduces the criterion value exactly at `m = 2` and falls a factor `~3` short at `m = 1`
(`0.1756 = D*(5,2)` against `D*(6,1) = 0.5321` for the free-label/`m=1` comparison).

**Corollary 4.4 (a globally free label).** If some label is absent from every palette (the shape of
every frozen countermodel in the record: `Theorem C`'s pair field uses all six labels, but the
three-block fields, the `ell = 6` free-label word and m13's singleton field all omit one label),
then the cover uses only `k - 1` labels and Theorem A applies with `k = 5`: `(5.3)` at separations
`<= D` forces `D <= D*(5,1) = 0.4862896510`. m13's `0.1755705045` is consistent and far below.

**Corollary 4.3 (which hypothesis forces the threshold below 1).** Nothing in (5.3) itself is a
bound on `D`: as `D -> 0` the forbidden band collapses to the single angular value `pi/3`, i.e. to
(5.7), which frozen fields do satisfy (Lemma 1.1, and the construction of §3.2 at `N = 1`). The
threshold is forced by two things acting together: (i) *nonemptiness* of the palettes — the `k`
supports must cover the direction circle; and (ii) the *geometry of the band*: for
`D > 0.3043792` one has `b(D) > 2a(D)`, which is what makes the cluster relation transitive and so
forces every label's support to be a union of narrow clusters separated by `b(D)`. At `d = 1` the
band is `[0, pi]` — every pair of directions is forbidden — and nonemptiness then contradicts (5.3)
outright: that is m11's Theorem A, the endpoint of the family. `D* = 0.5321` is where covering and
packing meet, i.e. where the integer `N` — the number of clusters per label — runs out. The paper
needs (5.3) at `d = 1` (Lemma 6.7) and at `d < 1/2` (Lemma 5.5); `D* > 1/2`, so the frozen class
survives the Lemma 5.5 range and dies `0.4679` short of Lemma 6.7.

---

## 5. Calibration and non-vacuity

1. **The threshold is attained, so the theorem is not vacuous.** `verify_construct.py` evaluates
   Lemma 5.2(3) in its own form (`z + f = x + s + t`, `s` from complex arithmetic) on the explicit
   fields: the 18-sector singleton field gives `0` violations in `800000` sampled
   `(d, alpha, f, branch)` quadruples at `D = 0.3`, `D = 0.5` and `D = D* = 0.5320889`, and the
   `m = 2` double cover of §7 gives `0` violations at `D = 0.2` and `D = 0.2855752`. Above `D*` the
   same field violates: `40` violations in `800000` at `D = 0.55`, `921` at `D = 0.6`, `7691` at
   `D = 0.7`, the first ones at angular separation `|delta| = 1.7709 > 5 pi/9 = 1.7453` — exactly
   the predicted failure (the band `[a(D), b(D)] = [0.4539, 1.7734]` has grown past the smallest
   same-label separation `5w = 5 pi/9`).
2. **Calibration against m11.** My `Sh(d)` agrees with m11's independently computed table to nine
   digits (Lemma 1.1); m11's Theorem D constant `0.3043792` is exactly the condition `b = 2a`, which
   Theorem B(i) at `m = 2` gives *without* the free-label hypothesis m11 needed; m11's Theorem C
   constant `0.4608111` is `b = 3a`, which `b <= 2a` supersedes; m11's Theorem A (the `d = 1` kill)
   is the endpoint of the same inequality.
3. **Calibration against m13.** m13's two sharp radii are exactly `D*(6,2)` and `D*(5,2)` (§4),
   and their sector condition `K <= floor(m/5)` is the `N`-integrality of §3 in sector language.
4. **Calibration against the paper at `k = 5`.** The same criterion at `k = 5` gives `D*(5,1) =
   0.4862896510` and `D*(5,2) = 0.1755705046`. The paper's own `k = 5` result is not a frozen-field
   statement (it excludes proper colourings, not frozen fields), so the calibration available is
   the `k = 5` members of the family, which are consistent with m13's `k = 5` computation.
5. **The known frozen models of the record.** m11 measured m15's block fields at radius `0.28558`
   and the `ell = 6` free-label word at `0.14715`; m13 measured its own sector classes at
   `0.2855752194` and `0.1755705045`. All are `<= D* = 0.5321`, and all are excluded above it — no
   contradiction; the theorem is exactly the statement that those radii cannot be pushed past
   `0.5321`, and they are the *attained* radii of much narrower ansaetze.
6. **m3's proper `k >= 7` colouring is not frozen** (its palette field depends on the centre), so no
   claim here applies to it; the theorem is a statement about the centre-independent class only.

---

## 6. What is not proved

* Nothing here decides `(W)`, local finiteness at `k = 6`, or `chi(R^2)`. The frozen class is a
  small class: it is already empty at `d = 1` by m11 Theorem A, and the theorem above only
  quantifies the gap. No non-frozen palette field is treated.
* Theorem B(ii) is proved exactly for `m = 1`. For `m >= 2` only the necessity (i) is proved in
  general; the `m = 2` construction at `k = 6` is written out in §7 below and checked numerically,
  but I do not claim the general `m` sufficiency.
* The equivalence "band condition iff (5.3)" (Remark 1.3) is at the level of a.e. statements; the
  two endpoint shifts `a(d), b(d)` are excluded, which is legitimate because they are attained only
  at finitely many directions for each fixed separation. Whether a field can be refused at an
  endpoint value of `Sh(d)` (which would move the threshold) is *not* decided here: all thresholds
  are computed with the open band, and the constructions are strictly inside it except at `D*`
  itself, where the boundary value `5w = b` is attained only on a null set of directions.
* `D*(k,m)` for `k >= 7` is computed by the formula but is not of independent interest: at those
  `k` the colouring problem itself is open, and the frozen class is excluded at `d = 1` in any case.

---

## 7. The `m = 2` construction at `k = 6` (checked, not needed for Theorem A)

At `D*(6,2) = 2 sin(2pi/9) - 1 = 0.2855752194`, `a = 0.73056`, `b = 4 pi/9 = 1.39626`. Take the six
supports to be the `2 pi/3`-periodic sets whose period-arc is `[0, 2 pi/9]`, `[0, 2 pi/9]`,
`[2 pi/9, 4 pi/9]`, `[2 pi/9, 4 pi/9]`, `[4 pi/9, 2 pi/3]`, `[4 pi/9, 2 pi/3]`. Every direction lies
in exactly two of them (double cover, so all palettes have size exactly 2), each support is a union
of arcs of width `2 pi/9 < a` at period `2 pi/3`, and the same-support circular distances lie in
`(0, 2 pi/9) union (4 pi/9, 8 pi/9)`, while the band is `[a, b] = [0.73056, 4 pi/9]`:
`(4 pi/9, 8 pi/9)` meets it only in its own left endpoint `b = 4 pi/9`, and no same-support pair
attains that value (a point `x` of the first period-arc has `x + 4 pi/9` in the gap). So (5.3) holds
at `D = D*(6,2)`.

---

## 8. Reproducing

```
cd .ultramath/smwg1r9lg/m8
python3 check1.py        # 40-digit values, Sh(d) vs m11's table, max over N, m11/m13 identities
python3 verify_exact.py   # rigorous rational-interval certificate: pi, sin, all comparisons of §3.3
python3 check3.py        # 40-digit recomputation of the shift extremes + direct evaluation of (5.3)
python3 verify_construct.py   # both constructions of §3.2 and §7 against (5.3)
```
