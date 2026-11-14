# The accumulation limit at k = 6 adds nothing; unit circles, and where the missing input sits

Member `m7`, direction `d15` (renormalisation at accumulation points).
No toolchain needed; the four scripts are plain Python 3 / numpy.

**What this note delivers.** Three lemmas, one caution, and two decided finite computations
about the `k = 6` interface, plus a negative conclusion about a natural route to `(W)`:

* **Lemma 1 (circle–palette disjointness).** For every centre `x` and almost every unit
  direction `e`, the palette `P_x(e)` is disjoint from the set `Col(S(x+e,1))` of labels
  occupying positive angular measure on the unit circle `S(x+e,1)`.  Hence
  `|P_x(e)| + |Col(S(x+e,1))| <= k`.
* **Corollary 1.3.** At `k = 6` a ternary palette forces a continuum of unit circles each
  coloured (a.e.) by at most three labels.  Consequently the **geometric hypothesis**
  *no unit circle in the plane carries three or fewer labels on positive-measure sets*
  implies the missing palette input `|P_x(e)| <= 2` a.e. of K6-BARRIER §5 / m11 §6.  The
  converse implication would require evaluating the palette at a *specified* direction and
  is not available in the paper's framework (§4(a)); so this is a sufficient reformulation,
  and its equivalence to `|P| <= 2` is exactly as strong as joint measurability of the
  palette field in its centre.
* **Lemma 2 (two-coloured unit circles are rigid, and their centres are separated).** A unit
  circle coloured a.e. by two labels must alternate under the 60-degree rotation (each class
  then has angular measure exactly `pi`), and its centre is a *binary centre* for that pair;
  hence, by paper Lemma 5.5 (valid at every `k`), the centres of a.e.-two-coloured unit
  circles with a fixed colour pair are `delta*`-separated.  The three-label analogue is
  **false**, and that failure is exactly the `k = 5 -> k = 6` wall.
* **Lemma 3 (degeneration of the two-centre transport).** As the separation `d` of two
  centres tends to `0`, the exact two-centre transport exclusions of (5.3) converge
  *uniformly* to the single-centre sixty-degree exclusion (5.7) (explicit bound `5d` for
  `d <= 1/2`).  **Hence the accumulation (renormalisation) route is closed**: at an
  accumulation point of `L` the transport data imposes nothing beyond the single-centre
  system, which is satisfiable (m1: only `K_6` is excluded at `k = 6`).
* **Lemma 4 (the paper's binary-centre separation is a 2-valued-selection theorem).**  The
  proof of Lemma 5.5 uses only that the palette meets a fixed label set `T` in a *singleton*
  a.e. and that "different from `s`" determines the value.  Hence the same conclusion holds
  for any `T` (in particular for the outsider triple of a `k = 6` triangle) as soon as the
  `T`-part of the palette is a singleton a.e. taking only **two** values: such centres are
  `delta*`-separated.  With three values only the inequality `s_x(...) != s_y(...)` survives
  and the expanding-action step has nothing to act on — the exact first step where the
  transfer of the `k = 5` machinery must fail.
* **A caution (§4).** The paper explicitly assumes no joint measurability of `P_x(e)` in the
  centre.  Hence steps of the form "the palette at this `x` in this *specified* direction
  `e` contains `c(x+e)`" (e.g. at the inward direction of a unit circle) are not available,
  and neither are their uniform-in-`x` versions.  Lemma 2 is phrased so as to use only the
  a.e.-support form of a trace, which is rigorous.
* **Decided finite computations (§5).** (a) The single-circle systems at `k = 6` are
  enumerated exactly (transfer matrix plus independent brute force): they are all
  *satisfiable*.  So even if the specified-direction statements of §4(a) were granted, no
  argument carried out at the level of one unit circle could force `|P| <= 2` at `k = 6`.
  (b) The paper's own seven-colouring is checked numerically: its unit circles carry four or
  five labels with maximal colour fraction `0.33 < 1/2`, consistent with Corollary 1.2.

Nothing here decides `(W)`.  §6 states exactly what remains.

---

## 0. Setting, and the inputs used

`c` is a weak measurable `k`-colouring of the plane (paper Definition 1.2), `A_i` its
classes, `P_x(e)` the maximal palette at the centre `x` in the unit direction `e` (paper
Definition 5.1), `sigma` the normalised angular measure on `S = S^1`, `R` rotation of
directions by `kappa = pi/3`.  The only inputs used below are

* **(5.2)** (Lemma 5.2(1)): for almost every *independent* pair `(e,v) in S x S`,
  `c(x+e+v) not in P_x(e) union P_x(v)`;
* **(5.7)** (Corollary 5.4): `P_x(f) cap P_x(Rf) = empty` for a.e. `f`;
* the support property of Definition 5.1: for every trace `b in W_x` and every label `i`,
  `{e : b_i(e) > 0}` is contained in `D_{x,i} = {e : i in P_x(e)}` up to an angular null
  set; in particular, if a trace is supported in a set `T` a.e. then
  `P_x(f) cap T != empty` for a.e. `f`;
* the general palette bound `1 <= |P_x(e)| <= k-3` a.e. (the proof of paper Prop. 5.6 with
  `|A| = k-2`; K6-BARRIER §1), which at `k = 6` reads `|P_x(e)| <= 3`;
* paper Lemma 5.5 (binary-centre separation), which has no `k`-dependence;
* the paper's remark (p. 27) that **no joint measurability of `P_x` in its centre is
  assumed**.

For a circle `Gamma` of radius one, `Col(Gamma)` denotes the set of labels `j` such that
`{z in Gamma : c(z) = j}` has positive angular measure.

## 1. Lemma 1: the palette at `x` is disjoint from the colours of the circle at `x+e`

**Lemma 1.** For every centre `x` and `sigma`-almost every unit direction `e`,
`P_x(e) cap Col(S(x+e,1)) = empty`.

*Proof.*  Fix `x`.  By (5.2) there is a `sigma x sigma`-null set `N subset S x S` off which
`c(x+e+v) not in P_x(e) union P_x(v)`.  By Fubini, for `sigma`-almost every `e` the section
`N_e = {v : (e,v) in N}` is `sigma`-null.  For such `e` and every `v not in N_e` we have
`c(x+e+v) not in P_x(e)`.  Hence `{v : c(x+e+v) in P_x(e)}` is `sigma`-null, i.e. no label of
`P_x(e)` occupies positive angular measure on `S(x+e,1)`.  `square`

This is the mechanism the paper uses inside the proof of Proposition 5.6 (there with
`|P_x(e)| = k-2`, so that the complement is a *pair* and `x+e` becomes a binary centre).  In
this form it is the two-scale statement needed below.  Note the quantifier: the conclusion is
asserted for `sigma`-almost every `e` at a *fixed* centre `x`; this is the only form the
paper's framework supports (§4(a)).

**Corollary 1.1.** For every `x` and a.e. `e`, `|P_x(e)| + |Col(S(x+e,1))| <= k`.

**Corollary 1.2 (each colour occupies at most half of a unit circle).**  For every unit
circle `Gamma` and every label `j`, the `j`-set on `Gamma` has angular measure at most
`1/2`; the bound is attained by the alternating two-colouring.

*Proof.*  On a unit circle `|z-z'| = 1` holds exactly when the angular difference is `pi/3`,
so the `j`-set `A` is measurable with `A cap RA = empty` up to a null set, whence
`2 sigma(A) = sigma(A) + sigma(RA) <= 1`.  `square`

This is the circle-side image of m11's `sigma{T subset P_x} <= 1/2`; both are the
independence ratio `1/2` of the six-cycle.

**Corollary 1.3 (a geometric sufficient condition for the missing palette input).**  Let
`k = 6`.

1. Suppose `A subseteq P_x(e)` for all `e` in a set `E` of positive angular measure, at some
   centre `x`.  Then for a.e. `e in E`, `Col(S(x+e,1)) subseteq A^c`, so that circle carries
   at most `|A^c| <= 3` labels.  In particular a ternary palette produces a continuum of
   circles with at most three colours.
2. Hence: if **no unit circle in the plane carries three or fewer labels**, then
   `|P_x(e)| <= 2` for a.e. `e` at every centre — the missing palette input — because
   `|P_x(e)| >= 4` is excluded by the general bound `k-3 = 3`.
3. The converse ("pair-valued palettes force every unit circle to carry at least four
   labels") is *not* derived here: it needs the palette evaluated at the specified inward
   direction of a given circle, which requires joint measurability in the centre.  See §4(a)
   and §5.

*Proof.*  (1) Lemma 1.  (2) contraposition of (1).  `square`

So the missing input of K6-BARRIER §5 is *implied by* the geometric hypothesis

> **(C3-)** no unit circle in the plane is a.e. coloured by three or fewer labels.

`(C3-)` is not a consequence of the unit-distance graph of the circle, which is a disjoint
union of six-cycles and hence two-colourable (K6-BARRIER §1): it is a genuinely
two-dimensional statement.  It is not vacuous, and the two-colour part of it is *true*
(Lemma 2).

## 2. Lemma 2: two-coloured unit circles are rigid, and their centres are separated

**Lemma 2.** Let `y in R^2` be such that `(y,1)` is a typical circle sampling (this holds for
a.e. `y`), and suppose `Col(S(y,1)) subseteq {a,b}` with `a != b`.  Then

1. `c(z) != c(Rz)` and `c(R^2 z) = c(z)` for a.e. `z in S(y,1)`; each of `a,b` occupies
   angular measure exactly `pi`, and the colouring is determined by its restriction to one
   fundamental domain of `R`;
2. `y` is a **binary centre** for the pair `{a,b}`: `P_y(f) cap {a,b}` is a singleton for
   a.e. `f in S`;
3. for every fixed pair `{a,b}`, the set of such centres `y` is `delta`-separated, where
   `delta = delta*` is the absolute constant of paper Lemma 5.5; in particular that set is
   uniformly discrete.

*Proof.*  (1) Corollary 1.2 plus the fact that with exactly two labels the flip
`c(Rz) != c(z)` forces `c(Rz)` to be the other label, so `c(R^2 z) = c(z)`; the classes have
equal measure `1/2`.
(2) Since `(y,1)` is a typical sampling, the constant sequence `(y,1)` is permitted, so
`b = (a_i(y + .))_i in W_y`.  Its support is contained in `{a,b}` a.e.; by the support
property of Definition 5.1, `P_y(f) cap {a,b} != empty` for a.e. `f`.  By (5.7), the
intersection cannot meet both labels at `f` and `Rf`; with two labels it is therefore a
singleton a.e., alternating under `R`.
(3) Lemma 5.5 applies to the fixed pair `{a,b}`.  `square`

**Why there is no `k = 6` analogue.**  For a triple `T = Col(Gamma)` the trace only gives
`P_y(f) cap T != empty` a.e., and (5.7) only says that the `T`-parts at `f` and `Rf` are
disjoint.  With `|T| = 3` this is compatible with alternating *pairs*: the step in the proof
of Lemma 5.5 which upgrades "meets the pair" to "is the singleton" — invariance of the
selection under the expanding maps `F_j` — is lost, because `T \ {s}` has two elements
instead of one.  This is the label deficit `k - 3 = 3 > 2` recorded for §6.3 in this
member's earlier `AUDIT.md`, now visible at the level of a *single* unit circle, before any
use of `L` or of an accumulation.

## 2b. Lemma 4: the paper's binary-centre separation is really a 2-valued-selection theorem

The proof of Lemma 5.5 uses only two properties of the fixed pair `{i+, i-}`: that the
palette meets the pair in a *singleton* a.e., and that with only two labels "different from
`s`" *determines* the value.  Nothing uses `|{i+, i-}| = 2` otherwise.  Hence:

**Lemma 4.** Let `T` be a nonempty set of labels and let `x != y` be two centres with
`|x - y| < 1/2` such that

1. `|P_x(f) cap T| = |P_y(f) cap T| = 1` for a.e. `f`, and
2. the two selections `s_x(f) := P_x(f) cap T` and `s_y(f) := P_y(f) cap T` both take values
   in one fixed two-element subset `{a,b}` of `T`.

Then `x, y` are at distance at least `delta*` (the absolute constant of Lemma 5.5); in
particular such centres form a `delta*`-separated set.

*Proof.*  By (5.7) the singleton `s_x(f)` differs from `s_x(Rf)`, so with two values
`s_x(Rf) = the other value = s_x(f)` flipped; the same for `s_y`; in particular
`s_x(t + kappa) != s_x(t)` a.e. and `s_x(t + 2kappa) = s_x(t)` — exactly the two properties
(5.8) and the flip used in the proof of Lemma 5.5.  The exact decompositions
`y + f = x + s_pm(f) + t_pm(f)` of Lemma 3 give, by (5.3), `P_y(f) cap P_x(s_pm(f)) = empty`;
since `s_y(f) in P_y(f)` and `s_x(s_pm(f)) in P_x(s_pm(f)) cap T`, we get
`s_x(s_pm(f)) != s_y(f)`, hence `s_x(s_pm(f)) = the other value`.  This is verbatim the
identity `s_x(alpha_pm(t)) = -s_y(t)` of Lemma 5.5's proof, with the two-element set `{a,b}`
in place of `{i+, i-}`.  From here the proof of Lemma 5.5 (the maps
`H = alpha_+ o alpha_-^{-1}`, `F_j`, the expanding-action/bounded-distortion argument, and the
final contradiction with `s_x` having measure `pi` on each value) applies without change.
`square`

**Corollary 4.1 (a partial separation theorem for the `k = 6` triangle locus).**  At
`k = 6`, let `T` be the outsider triple of a triangle centre.  On the stratum where the
*outsider part* `P_x(f) cap T` is a singleton a.e. and takes only two values, the centres are
`delta*`-separated, hence locally finite.  The complementary stratum — outsider part a
singleton with three values, or of size `>= 2` — is exactly where the printed argument stops.

**Corollary 4.2 (the `k = 6` four-cycle locus on the binary-outsider stratum).**  Let
`{X,Y}` be any pair of labels (at a four-cycle centre, the pair of outsiders).  Then the set
of centres

  `{ x : |P_x(f) cap {X,Y}| = 1 for a.e. f }`

is `delta*`-separated.  In particular, at `k = 6` the four-cycle locus is locally finite on
the stratum where the palette meets the outsider pair in exactly one label a.e. — no
hypothesis on the palette size is needed for this.  The two remaining strata,
`P cap {X,Y} = empty` a.e. and `{X,Y} subseteq P` on a positive-measure set, are exactly the
ones that carry the ternary palettes (`{0,2,X}` and `{1,3,X}` in the notation of
`sprint/k6/REPORT.md` §4b'), and they are not touched by the printed technology.

*Proof.*  Lemma 4 with `T = {X,Y}`; the values are automatically the two labels of `T`.
`square`

**Sharpness (Lemma 4 is not a palette-level statement).**  m13's singleton model
(palettes `{4 + s(t)}`, `s(t) = floor(9t/2pi) mod 3`, `.ultramath/smwfo9zkl/m13/no-go.md`)
satisfies (P1)-(P6) including the exact local transport (5.3) at every distance `<= 1/50`,
and is translation invariant.  Take `T = {4,5,6}`, the set of its values: then
`|P cap T| = 1` at **every** centre, so `S_T` is the whole plane and is not separated.
Hence, exactly as for Lemma 5.5, the trace and properness input is essential:
`delta*`-separation of `S_T` is a colouring-level theorem and cannot be recovered from the
palette axioms plus the transport.  (The verifier is the swarm's own:
`.ultramath/smwfo9zkl/m13/model_check2.py`.)

This does not prove ternary separation in general: with three values, the transport yields
only `s_x(s_pm(f)) != s_y(f)`, and "different from" no longer determines the value, so the
selection is not invariant under `H` and the expanding-action step has nothing to act on.
That is the precise first step at which `d18`'s programme must fail if it fails.



## 3. Lemma 3: the two-centre transport degenerates to (5.7), so the accumulation route is closed

Fix centres `x` and `y = x + h` with `d = |h| in (0,1/2)`.  For a unit direction `f` put
`u = h + f`, `rho = |u|`, `J` = rotation by `pi/2`; the exact unit decompositions of `h + f`
are

  `s_pm(f) = u/2 +- sqrt(1 - rho^2/4) * Ju/rho`,

and (5.3) reads `P_y(f) cap P_x(s_pm(f)) = empty` for a.e. `f` (paper Lemma 5.2(3) with
`z = y`, `s = s_pm(f)` and `t` the other endpoint; `s` and `t` are nonparallel since
`|h+f| <= 1+d < 2`).

**Lemma 3.** For `0 < d <= 1/2` and every unit `f`, `|s_pm(f) - R^{+-1}f| <= 5d`; hence
`s_pm(f) -> R^{+-1}f` uniformly as `d -> 0`.  Consequently, along any family of centre pairs
with `d -> 0` — in particular along cycle centres converging to an accumulation point — the
transport exclusions of (5.3) converge, uniformly in the direction, to the single-centre
exclusions `P_x(f) cap P_x(R^{+-1}f) = empty`, i.e. to (5.7).

*Proof.*  At `d = 0`, `u = f` and `rho = 1`, so `s_pm = f/2 +- (sqrt3/2) Jf = R^{+-1}f`.  The
error is `(u-f)/2 +- [sqrt(1-rho^2/4) Ju/rho - (sqrt3/2) Jf]`, with `|(u-f)/2| <= d/2`,
`|u/rho - f| <= 2d/(1-d)`, and `|sqrt(1-rho^2/4) - sqrt3/2| <= (|1-rho^2|/4)/(sqrt3/2) <=
0.63 d`, since `|1-rho^2| = |2 d f_1 + d^2| <= 2d + d^2`.  Summing gives at most `4.7 d` for
`d <= 1/2`.  `square`

`work/degeneration.py` checks the inequality twice: over rational unit directions
(Pythagorean parametrisation) at five values of `d`, with an exact-algebraic evaluation of
`|s_pm - R^{+-1}f|/d` (worst ratio `1.16`), and over a dense floating grid (worst ratio
`1.28`), against the analytic certificate `4.7`.

**Consequence (the renormalisation route is closed).**  At an accumulation point `x_0` of
the cyclic locus `L`, every two-centre constraint available between a centre `x_n -> x_0` and
a nearby centre degenerates, as `n -> infinity`, to a constraint already implied by the
single-centre system at `x_0`.  That system is satisfiable at `k = 6`: by m1's classification
it excludes only `K_6` among the `2^15` graphs on six labels, and m11's sharp finite models
attain the density bound `sigma{|P| = 3} = 1/2`.  Hence **no accumulation-specific palette
obstruction exists at `k = 6`**; the renormalisation programme of direction `d15` cannot
decide `(W)` and cannot supply `|P| <= 2`.  This is the negative half of `d15`'s stated
dichotomy ("either `(W)` reduces to a finite free-label computation, or the reduction fails
with an explicit witness"); the witness is Lemma 3 together with m1's classification.

## 4. Two cautions for the `k = 6` programme

**(a) Specified directions are not available.**  `P_x(e)` is defined for fixed `x` up to
angular null sets, and joint measurability in `x` is explicitly not assumed.  Every rigorous
palette statement is therefore either "for `sigma`-almost every `e`, at this fixed `x`", or
the support form "if a trace at `y` is supported in `T` a.e. then `P_y(f) cap T != empty`
for a.e. `f`".  Statements of the form

  `c(x+e) in P_x(e)` for a **specified** direction `e` and a **specified** centre `x`

are not available, and neither are uniform-in-`x` consequences such as "at every point `x`
of a unit circle the inward palette contains `c(y)`" or "the inward palette at every point of
a 5-coloured circle is the singleton of the missing label".  The exceptional null set of
directions may contain the prescribed one, independently for each centre.  (Joint
measurability of `P_x(e)` in `x` would repair this: it would give the statements for a.e.
`x` on a given circle, though still not at every `x`.  The paper neither assumes nor proves
it, so nothing below uses it.)  Lemma 2 is
phrased so as to use only the support form, which is why it is rigorous; Corollary 1.3 is
phrased with the quantifier "for a.e. `e` in `E`", for the same reason.  Any argument of the
swarm that evaluates a palette at a prescribed direction of a prescribed centre should be
checked against this.

**(b) Blow-up limits are not colourings.**  The rescaled colourings `z |-> c(x_0 + eps z)`
converge, along subsequences, only weak-`*` in `L^infinity` on compact sets.  The limit of
`{0,1}`-valued functions need not be `{0,1}`-valued (a radial ring pattern
`c(x) = f(log log |x|)` with `f` equidistributed on two values has a fractional weak-`*`
blow-up limit), so it is not a colouring, and the unit-pair properness of Definition 1.2
does not pass to it.  Hence no compactness argument can transfer the `k = 6` hypotheses
across scales.  With Lemma 3 this is the exact reason why the accumulation analysis cannot
be pushed further at the palette level.

## 5. Decided finite computations

### 5a. The single-circle systems at `k = 6` are satisfiable

Grant the specified-direction statements of §4(a) (i.e. work with the *stronger* hypothesis
set).  For a circle with colour set `Col` and a triple `T = Col`, the circle-side system is:
partition the circle into `m` equal sectors (`m` divisible by 6, `R` = shift by `s = m/6`),

* a colouring `c : Z/m -> [6]` with `c(i) != c(i+s)` (properness on the unit circle);
* inward palettes `Q : Z/m -> 2^[6]` with `Q(i)` nonempty, `Q(i) subseteq Col^c`,
  `Q(i) cap Q(i+s) = empty` (Lemma 1 and (5.7); self-avoidance `c(i) not in Q(i)` is then
  automatic).

Every constraint is of the form "`i` compatible with `i+s`", so the constraint graph is a
disjoint union of `gcd(m,s) = s` six-cycles and the number of solutions is `tr(A^6)^s`.
`work/circles.py` computes the counts by transfer matrix and independently by brute-force
product enumeration:

| system | `m=6` | `m=12` | `m=18` | `m=24` |
|---|---|---|---|---|
| 2-colourings with `c(i) != c(i+s)` | 2 | 4 | 8 | 16 |
| 3-colourings with `c(i) != c(i+s)` | 66 | 4356 | 287496 | — |
| inward palettes `Q` of a `{1,2,3}`-circle | 234 | 54756 | 12812904 | 2998219536 |

Brute force agrees at `m = 6` for all three systems and at `m = 12` for the first two.  The
2-colour column is `2^s` and every solution satisfies Lemma 2's rigidity (`c(i) = c(i+2s)`,
`c(i) != c(i+3s)`, exactly `m/2` sectors per colour).  The 3-colour column is
`((3-1)^6 + (3-1))^s = 66^s`, the chromatic polynomial of the six-cycle, and there the
rigidity fails.  An explicit witness at `m = 12` is
`c = (1,1,2,2,3,3,1,1,2,2,3,3)` and `Q = ({4},{4},{5},{5},{4},{4},{5},{5},{4},{4},{5},{5})`.

**Verdict.**  The single-circle constraints are satisfiable with a large solution space.
Therefore no argument carried out at the level of one unit circle can establish `(C3-)`, nor
`|P| <= 2` at `k = 6`; the two-coloured stratum is rigid and separated (Lemma 2), the
three-coloured stratum is not, and that is the whole distance between `k = 5` and `k = 6`.

### 5b. The paper's seven-colouring satisfies Lemma 1 and Corollary 1.2

`work/hex7.py` implements the paper's seven-colouring exactly (hexagons of circumradius
`r = 2/5`; colour = coset of the index-seven sublattice `(2-omega)L`, i.e.
`phi(m,n) = (4m+n) mod 7` in the lattice basis `sqrt3 r (1, omega)`), and samples it:

* `0` monochromatic unit pairs among `40000` random pairs (properness);
* on four random unit circles the colour sets have `4` or `5` elements with maximal colour
  fraction `0.33 < 1/2`, in agreement with Corollary 1.2;
* the colouring is cell-constant, so every palette is a singleton `{c(x+e)}`: this is
  consistent with Lemma 1 (`|P| + |Col| = 1 + |Col| <= 7`) and with the palette bound
  `|P| <= k-3 = 4`.

### 5c. Independent reproduction of the swarm's single-centre orbit counts

`work/orbits_check.py` re-implements, from the specification in `sprint/k6/STRUCTURE.md`
(Theorem 5 items 1-7 together with the edge trace (6.2)), the single-centre `R`-orbit
enumeration, with a third code path (different alphabet construction, different DFS order,
and a whole-word re-check by an independent predicate).  It reproduces every reported count:

| cycle length | centre colour | alphabet | words (reported = reproduced) |
|---|---|---|---|
| 3 | in the cycle | 22 | 70194 |
| 3 | outside | 19 | 11888 |
| 4 | in the cycle | 20 | 18746 |
| 4 | outside | 17 | 2164 |
| 5 | in the cycle | 18 | 3720 |
| 5 | outside | 15 | 380 |
| 6 | in the cycle | 16 | 510 |

and the auxiliary numbers quoted in `sprint/k6/STRUCTURE.md` and `SYNTHESIS.md`: the
all-pairs stratum at `ell = 6` has `150` words, and the `(3,2,3,2,3,2)` size pattern has `6`.
So the orbit table is now backed by three independent implementations.

## 6. What is settled, and what is not

Settled here: Lemma 1 and Corollaries 1.1-1.3; Lemma 2; Lemma 3 and the closure of the
renormalisation route; Lemma 4 and Corollary 4.1; the two cautions of §4; the two decided
finite computations of §5 (and the independent reproduction of §5c).

Not settled (unchanged): `(W)`, `(ISO)`, local finiteness at `k = 6`, `(C3-)`, `|P| <= 2` at
`k = 6`, `chi(R^2) >= 7`, `chi(R^2) <= 6`.  In particular this note does **not** prove
`|P| <= 2` at `k = 6`.  What it does show is: (i) the missing palette input is *implied by*
a purely geometric statement about unit circles; (ii) the two-colour case of that statement
is true, rigid, and comes with `delta*`-separation of its centres; (iii) the three-colour
case is consistent with every single-circle constraint, so it cannot be settled at the level
of one circle, with or without the specified-direction steps; (iv) the accumulation layer of
the palette system contributes nothing new.

## 7. Files and how to check them

| file | content |
|---|---|
| `REPORT.md` | this note |
| `work/degeneration.py` | Lemma 3: exact-algebraic and dense-grid check of `|s_pm - R^{+-1}f| <= 5d` |
| `work/circles.py` | §5a: transfer-matrix counts, independent brute force, explicit witness |
| `work/hex7.py` | §5b: the paper's seven-colouring, properness and circle colour fractions |
| `work/orbits_check.py` | §5c: independent reproduction of the single-centre orbit counts |

```
python3 work/degeneration.py     # worst exact ratio 1.16, worst float ratio 1.28, PASS
python3 work/circles.py          # the table of §5a and the witness checks
python3 work/hex7.py             # properness 0/40000, circle colour fractions <= 1/2
python3 work/orbits_check.py     # the seven orbit counts of §5c, all reproduced
```
