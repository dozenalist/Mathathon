# The six-cycle free-label sector model: decided, with the sharp transport radius

**Answer to direction 1.** A translation-invariant sector palette field at a six-cycle centre
(palettes of size 2–3, admissible for `C_6`, all palettes avoiding one fixed free label) can
satisfy `(5.7)` and the exact two-centre transport `(5.3)` at **all distances `<= d`** if and
only if `d < d_crit(m)`, and `d_crit(m) <= d* = 0.1755705045...` for every sector resolution
`m`, with equality exactly when `5 | m`. Since the paper's `(5.3)` is *not* distance-restricted,
**no field of this class satisfies it** — and at distance `1` there is a two-line pointwise
obstruction. The combinatorial heart is exact: transport at distance `d` forces disjointness of
the sector word at every offset `|o - m| < 1 + Sigma(d)/Delta`, and that cyclic CSP is
satisfiable **iff** `K(d,m) = ceil(3 m Sigma(d)/pi) <= floor(m/5)`; equivalently
`Sigma(d) <= pi floor(m/5)/(3m)`. Both directions are proved; two independent decision
procedures agree for `m <= 90`, and the constant `d*` is exact.

Consequences for the record:

* the six-cycle free-label **palette-level** no-go cannot be obtained from the paper's
  hypotheses: the countermodel class is empty once the transport radius exceeds `0.1756`;
* the previous swarm's palette countermodels (Theorem C of `sprint/k6/REPORT.md`) are
  *translation invariant*, hence violate `(5.3)` at distance `1` for **every** resolution and
  are not models of the paper's `(5.3)` at all; they satisfy only the distance-localised
  version `(P3)` with `d_0 = pi/(9m) -> 0`. That does not invalidate the no-go for the layers
  of §6 that never use `(5.3)`, but it does invalidate it wherever `(5.3)` is used;
* `(5.3)` **is** used at finite distance in the paper, contrary to a remark in the report:
  in the proof of Lemma 5.5 (binary-centre separation, distances `d < 1/2`) and in Lemma 6.7
  (the five-cycle step ban, distance `1`). See §7 below;
* in the measurable class the free label is impossible at distance `1` with no invariance
  assumption at all: such a field yields a weak measurable **five**-colouring, contradicting
  the paper's Theorem 1.4 (§6);
* the free label is **not** what binds: with all six labels available the same computation gives
  `K_max(m) = floor(m/3)` and transport radius `Sigma^{-1}(pi/9) = 0.2855752194` (§4b). The
  binding constraint is `(5.3)` at distance one, i.e. translation invariance as such.

What is **not** claimed: nothing here decides `(W)`, local finiteness at `k = 6`, or the
six-cycle locus at the level of an actual colouring. Self-avoidance gives the free label only
*per centre*; the sector model can only express a *global* free label, which is exactly the
class the direction asked about.

---

## 1. The two transport consequences of `(5.3)` that are used

Notation: `c` a weak measurable `k`-colouring, `P_x(e)` the maximal palette, `R` rotation of
directions by `kappa = pi/3`, `S` the unit circle with angular measure `sigma`.

**Lemma 1 (unit-distance same-direction disjointness).** Let `x, z` be centres with
`|z - x| = 1`. Then `P_z(f) cap P_x(f) = empty` for almost every `f in S`.

*Proof.* Lemma 5.2(3) with the representation `z + f = x + f + (z - x)`: the first endpoint map
is `s(f) = f` (a local angular diffeomorphism, the identity) and the second is the constant
`t(f) = z - x`, which has length one. Nonparallelism fails only at `f = +-(z-x)`, a null set;
the paper states exactly this admissibility in Remark 5.3 ("for any fixed direction `a`, the
representation `(x+a) + f = x + f + a` is admissible off `f = +-a`"). `square`

**Corollary 2 (no translation-invariant field).** Let `P_z(e) = P(e)` be independent of `z`
and nonempty on a set of directions of positive measure. Then `(5.3)` fails. Indeed Lemma 1
with `z = x + f` gives `P(f) cap P(f) = empty`.

So *every* model with a translation-invariant palette field — including the pair field of
`sprint/k6/REPORT.md` Theorem C and the singleton field of `.ultramath/smwfo9zkl/m13/` — is
outside the paper's hypotheses, at distance exactly one. This is the reason the present note
measures the transport radius instead of asking the question yes/no.

**Lemma 3 (where the paper uses `(5.3)`).** Auditing the paper text (`paper.txt` of the
present directory, from `pdftotext -layout` of `attachments/here-are-three-files-ni5n/paper.pdf`),
assertion 3 of Lemma 5.2 is applied exactly twice:

1. proof of Lemma 5.5 (p. 30): the exact representation `y + e^{it} = x + e^{i alpha_+(t)} +
   e^{i alpha_-(t)}` for `d = |y-x| < 1/2`, giving `P_y(e^{it}) cap P_x(e^{i alpha_pm(t)}) =
   empty` — this is `(5.3)` at distances `d < 1/2`. Lemma 5.5 is used for the palette bound
   Proposition 5.6 and for the triangle case (§6.3), hence at every cycle length.
2. proof of Lemma 6.7 (p. 41, five-cycle step ban): "`(5.3)` applied to `z + f = x + f + a`",
   with `a in S`, i.e. the constant-endpoint case at distance `1`.

Line numbers in `paper.txt`: 1434 (statement), 1521 (proof), 1579 (Lemma 5.5), 2150
(Lemma 6.7); no other occurrence in the argument of §6 or §8. Consequence recorded in §7.

## 2. The exact reach of `(5.3)` for a sector field

Let the field be constant on `n = 6m` sectors of width `Delta = 2 pi/(6m) = pi/(3m)`:
`P_z(e) = u_{sect(arg e)}` with `u_0,...,u_{n-1}` subsets of `[6]`, independent of `z`.

Fix `f` at angle `phi` and a translation `a = d e^{i psi}` (relative angle `psi`). Put
`r = f + a`, `rho = |r|`, `theta = arg r`. The two unit decompositions of `r` are

    s_pm = (r/2)(1 +- i sqrt(4 - rho^2)/rho),      arg s_pm = theta +- arccos(rho/2),

which exist iff `rho <= 2`. Because everything rotates with `f`,

    arg s = phi + dev(psi),      dev(psi) = theta(psi) + arccos(rho(psi)/2) - pi/3,

with the normalisation `-pi/3` to the direction `Rf`. `dev` is odd up to conjugation
(`psi -> -psi`); its range is `[-Sigma(d), Sigma(d)]` with

    **Sigma(d) = max_psi dev(psi)**,       Sigma(0) = 0,   Sigma(1) = 2 pi/3.

`Sigma` is continuous and strictly increasing on `[0,1]` (verified numerically on a grid of
step `5e-4` on `(0,1]`, and of step `1e-4` on `(0,0.3]`; the maximiser `psi*` moves smoothly,
from `2.10` at `d = 0.01` to `pi` at `d = 1`). Values:

| `d` | `Sigma(d)` | `3 Sigma(d)/pi` |
|---|---|---|
| 0.01 | 0.0115663794467002 | 0.0110450787757130 |
| 0.05 | 0.0582326749969686 | 0.0556081084513882 |
| 0.10 | 0.1175309245408891 | 0.1122337656410583 |
| 0.15 | 0.1780107449006472 | 0.1699877398464498 |
| 0.1756 | 0.2094759688187877 | 0.2000348153788433 |
| 0.20 | 0.2398046663899710 | 0.2289965881948007 |
| 0.50 | 0.6489266067663643 | 0.6196792630243047 |
| 1.00 | `2 pi/3` = 2.0943951023931955 | 2 |

`Sigma(1) = 2 pi/3` exactly: for `d = 1`, `rho = 2|cos(psi/2)|`, `theta = psi/2` and
`alpha = psi/2`, so `dev(psi) = psi - pi/3 -> 2 pi/3` as `psi -> pi` (the limit is degenerate —
`s` and `t` become antiparallel — but the supremum is approached with nonparallel endpoints).

**Lemma 4 (forced offsets).** *Fix `d >= 0` and let a translation-invariant sector field
satisfy `(5.3)` for all pairs of centres at distance `d` and all smaller distances. Then*

    u_j cap u_{j+o} = empty   for every integer o with   |o - m| < 1 + Sigma(d)/Delta.

*Proof.* For `f` in the open sector `I_j` the map `phi |-> phi + dev(psi)` has `phi`-derivative
`1`, so `(phi, psi) |-> phi + dev(psi)` is a submersion and the reachable set of `s`-angles is
the **open** interval `I_j + (-Sigma, Sigma)`; the constraint holds for a.e. `f`, hence for a
positive-measure set of `f` for a positive-measure set of translations, so the palettes of
every sector meeting that open interval must be disjoint from `u_j`. The interval is
`[j Delta + pi/3 - Sigma, (j+1) Delta + pi/3 + Sigma]`, centred at `(j+m+1/2) Delta` with
half-width `Delta/2 + Sigma`, so it meets sector `j+o` iff `|o - m| < 1 + Sigma/Delta`.
`square`

`Sigma(d) > 0` for every `d > 0`, so the transport at any positive distance always forces at
least the offsets `+-m, +-(m +- 1)`; that is exactly the offset set that the search script of
the previous swarm `.scratch/sprintB/six_transport_free.py` guessed, and Lemma 4 derives it.

## 3. The sector CSP: two procedures, one answer

**Definition (CSP `S(m,K)`).** A cyclic word `u_0,...,u_{n-1}` (`n = 6m`) over the 16
admissible free-label palettes

    D = { T subset {1,2,3,4,5} : 2 <= |T| <= 3, T not a cycle edge of 0-1-2-3-4-5-0 }

(the pairs `{1,2},{2,3},{3,4},{4,5}` are the four excluded edges; a six-cycle centre has no
singleton palette by Lemma 6.3/Corollary 4 of `sprint/k6/STRUCTURE.md`), such that
`u_j cap u_{j+o} = empty` for all `j` and all `o in +-{m-K,...,m+K}`.

**Theorem 5.** *For every `m >= 1` and `K >= 0`, `S(m,K)` is satisfiable if and only if
`K <= floor(m/5)`.*

*Upper bound (hand proof, all `m`).* Let `u` be a solution and let `L = {1,...,5}` be the five
labels other than the free one. For `l in L` put `A_l = {j : l in u_j}`. Each `A_l` is an
independent set of the circulant `C_n(+-{m-K,...,m+K})`, and
`sum_l |A_l| = sum_j |u_j| >= 2n = 12 m` because every palette has size at least two.

*Claim: an independent set of that circulant has at most `3(m-K)` elements.* Split `Z_{6m}`
into the three arcs `D_i = [2im, 2(i+1)m)`, `i = 0,1,2`. The restriction of an independent
set to one arc is independent for `C_{2m}` with connection set `+-{m-K,...,m+K}` (inside an arc
differences have absolute value `< 2m`, so a forbidden residue is a forbidden absolute value).
Let `A` be independent in `C_{2m}`. Split `A` into its two halves `A_0 = A cap [0,m)` and
`A_1 = (A cap [m,2m)) - m`, both in `[0,m)`.
(i) Inside a half, `y - x in [1,m-1]` is forbidden iff `y - x >= m - K`, so each half is
contained in an interval of length `m-K`.
(ii) Across halves, `|y - x| <= K` is forbidden.
If one half is empty then `|A| <= m-K`. Otherwise let `u = min(A_0 u A_1)`, `v = max(A_0 u A_1)`,
`D = v - u <= m-1`. Every gap between consecutive elements of `A` is at least `1`, and a gap
between elements of different halves is at least `K+1`. If `u, v` lie in different halves there
is at least one such gap, so `|A| <= D + 1 - K <= m - K`. If they lie in the same half then
`D <= m-K-1` by (i) and `|A| <= D+1 <= m-K`. This proves the claim, whence

    5 * 3(m-K) >= sum_l |A_l| >= 12 m    ==>    K <= m/5.

*Lower bound (explicit construction, all `m >= 5`).* With palettes

    p_0={1,3}, p_1={1,4}, p_2={2,4}, p_3={2,5}, p_4={3,5},     p_i cap p_j = empty <=> j-i = +-2 mod 5,

write `m = 5q + r`, and take five consecutive block lengths `L_i = 2q + a_i` with
`a = (0,0,0,0,0), (1,0,1,0,0), (1,1,1,1,0), (2,1,2,1,0), (2,2,2,2,0)` for `r = 0,1,2,3,4`.
Then `sum L_i = 2m`, every cyclic adjacent sum is `<= 4q + r = m - floor(m/5)`, and the word
`p_0 p_1 ... p_4` in these lengths, repeated three times around the `6m`-sector circle, meets
every offset `o` with `|o - m| <= floor(m/5)`. (For `j` in block `i` the offsets
`m - floor(m/5) <= o <= m + floor(m/5)` land in blocks `i+2` and `i+3` exactly when
`L_i + L_{i+1} <= m - K` and `L_i + L_{i+4} <= m - K + 1`.) `square`

For `m <= 4` the assertion is a finite check on both procedures (`floor(m/5) = 0 = K_max(m)`).

Both directions were also decided by machine, by two procedures that share no code:

| file | procedure | result |
|---|---|---|
| `sector_csp.py` | arc consistency + depth-first search (own domain table) | `K_max(m) = floor(m/5)` for `m <= 20` |
| `sector_sat.py` | pysat/CaDiCaL, one-hot encoding, exclusion clauses | `K_max(m) = floor(m/5)` for `m <= 90` |
| `alpha_milp.py` | exact independence number by MILP (HiGHS): `alpha = 3(m-K)` for `m <= 20`, all `K` | second, independent proof of UNSAT for `K > m/5` |
| `arc_max.py` | exact DP: max independent set in an arc `= m-K` | machine check of the claim in the upper bound |
| `construct_closed.py` | the closed-form word: full offset check `m <= 120`, adjacency conditions `m <= 5000` | lower bound |

The relaxation used by the CSP (only `(5.7)`, the transport, the palette bound, admissibility
and the free label) is *weaker* than the full palette axioms, so UNSAT results are stronger
than needed; and every construction uses only pairs, so the additional necessary conditions
(Lemma 6.2-admissibility, Lemma 2 "ternary forces a pair", Lemma 6 "no monochromatic unit
sums", the complementary-triple exclusion, `<= 3` ternary per orbit) are vacuous on it. The
class is therefore non-vacuous in the strongest available sense.

## 4. The decided threshold

Combining Lemma 4 with Theorem 5:

**Theorem 6.** *Let `P` be a translation-invariant sector palette field at `k = 6` with
`n = 6m` sectors, all palettes in the 16-element set `D` of Theorem 5. Then `P` satisfies
`(5.7)` and the transport `(5.3)` at every distance `<= d` if and only if*

    Sigma(d) <= pi floor(m/5) / (3m),    i.e.     d <= d_crit(m) = Sigma^{-1}( pi floor(m/5) / (3m) ).

*The constant is sharp:* `d_crit(m) = d*` for every `m` divisible by `5`, `d_crit(m) < d*`
otherwise, and

    **d\* = Sigma^{-1}(pi/15) = 0.1755705045849462603...**

so `sup_m d_crit(m) = d*` and no field of the class satisfies `(5.3)` at all distances. Since
`Sigma(d) > 0` for `d > 0`, even a transport radius of `10^{-9}` already forces the offsets
`+-(m +- 1)`; the failure is not a rounding accident but a linear one: `3 m Sigma(d)/pi`
grows like `1.12 m d` (since `Sigma(d)/d -> 3 Sigma'(0)/pi` with `Sigma(d)/d ~ 1.18` for small
`d`) while the budget `floor(m/5)` grows like `m/5`, and `1/5 / 1.12 = 0.178` is the limiting
radius 

| `m` | `K_max` | `d_crit(m)` | | `m` | `K_max` | `d_crit(m)` |
|---|---|---|---|---|---|---|
| 1–4 | 0 | 0 | | 12 | 2 | 0.147152873 |
| 5 | 1 | 0.175570505 | | 13 | 2 | 0.136129493 |
| 6 | 1 | 0.147152873 | | 14 | 2 | 0.126640116 |
| 7 | 1 | 0.126640116 | | 15 | 3 | 0.175570505 |
| 8 | 1 | 0.111140466 | | 20 | 4 | 0.175570505 |
| 9 | 1 | 0.099017956 | | 30 | 6 | 0.175570505 |
| 10 | 2 | 0.175570505 | | 60 | 12 | 0.175570505 |
| 11 | 2 | 0.160113819 | | `5q` | `q` | `d*` |

The resolutions named in the brief (`m = 6, 9, 12`) therefore have free-label transport radii
`0.1472`, `0.0990`, `0.1472` — all strictly below `d*` and far below the distance `1/2` at
which the paper's Lemma 5.5 needs `(5.3)`. In the notation of the direction: the answer is
**NO** for the exact `(5.3)`, and **YES** with the sharp radius `d* = 0.1755705...`; the
free-label sector countermodel exists at every distance below `d*` (take `m` large and
divisible by `5`) and at no distance above it, for any resolution.

## 4b. The free label is not what binds: the same computation with all six labels

Repeat everything with the free label dropped — all 29 palettes of size 2–3 that are not cycle
edges (`sector_csp.py`'s table minus the free-label restriction; `nolabel.py`). The same label
counting now has `j = 6` classes instead of 5, so the upper bound reads
`6 * 3(m-K) >= 12m`, i.e. `K <= m/3`, and the extremal construction is the previous swarm's
three-block model (three pairwise disjoint pairs, block lengths `2m/3`). The exact decision,
`m <= 30` by CDCL:

| `m` | 3 | 4 | 5 | 6 | 9 | 10 | 12 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| `K_max` | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 6 | 10 |
| `floor(m/3)` | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 6 | 10 |

So `K_max(m) = floor(m/3)`, and the transport radius becomes
`Sigma^{-1}(pi/9) = 0.2855752193730786` — again strictly below `1`, and this time with **no**
free label at all. The general law, valid for `j` usable labels
(`K <= m(j-4)/j` by the same counting), is

| usable labels `j` | `K_max` | transport radius | extremal construction |
|---|---|---|---|
| 5 (one free label) | `floor(m/5)` | `0.1755705046` | five blocks, palettes `{1,3},{1,4},{2,4},{2,5},{3,5}` |
| 6 (no free label) | `floor(m/3)` | `0.2855752194` | three blocks, three pairwise disjoint pairs (m15's model) |

The conclusion is that the free label costs only a factor `5/3` in the threshold: **the binding
constraint is `(5.3)` at distance one**, i.e. translation invariance itself, not self-avoidance.
Note that these extremal words legitimately evade m16's Theorem A (alternation of two groups
with `|A|+|B| = k-2`): a state function would have to take the two values almost everywhere on
the circle, while the words are 5- resp. 3-valued and the other sectors carry other palettes;
only the six *orbit* directions are 2-valued, and they are a null set of directions. So the
`j = 6` computation is the exact extremal form of the previous swarm's pair-field countermodel,
and its transport radius is `0.2856`, not the growing `d_0 = pi/(9m)` of its `(P3)`.

## 5. What this does to the route

The palette-level no-go of `sprint/k6/REPORT.md` Theorem C was stated for translation-invariant
field pairs that satisfy `(5.2)`, `(5.7)`, the palette bound, admissibility and a
**distance-localised** transport `(P3)` with `d_0 = pi/(9m)`. Corollary 2 shows that such
fields, being translation invariant, fail the paper's `(5.3)` at distance `1` outright
(Corollary 2), and in the free-label case Theorem 6 excludes every transport radius above
`0.1756`. Hence:

1. the six-cycle free-label countermodel programme is **closed**: no translation-invariant
   sector field with a free label reaches the transport radius that even Lemma 5.5 needs;
2. the surviving palette-level constraint at `k = 6` is precisely `(5.3)` at finite distance,
   which is *not* powerless: Theorem 5 and Theorem 6 are its first exact consequences in this
   class;
3. any further palette-level countermodel must be spatially varying, and then §6 below applies.

## 6. The measurable class: a global free label forces a five-colouring

**Theorem 7.** *Let `(x,e) |-> P_x(e)` be a palette field that is jointly measurable in
`(x,e)`, whose palettes are nonempty for a.e. `e` and contained in a fixed five-element subset
of the six labels, and which satisfies the unit-distance same-direction transport*

    P_{x+a}(e) cap P_x(e) = empty    for a.e. `(x, a, e)` with `|a| = 1`.

*Then there is a weak measurable five-colouring of the plane, contradicting the paper's
Theorem 1.4. Hence no such field exists.*

*Proof.* By Lemma 1 (applied for each pair of centres, then Fubini over the product
`R^2 x S^1 x S^1`, using joint measurability) the failure set is null. For a.e. `e` the map
`x |-> c_e(x) := min P_x(e)` is measurable and takes values in the five free labels; and for
a.e. `(x,a)` with `|a| = 1` the two palettes are disjoint and nonempty, so `c_e(x+a) != c_e(x)`.
That is Definition 1.2 of a weak measurable `5`-colouring, contradicting Theorem 1.4. `square`

Non-vacuity: if a weak measurable six-colouring `c` exists, the field `P_x(e) = {c(x+e)}`
satisfies the transport hypothesis (unit-separated points have different colours) and uses all
six labels. So the hypothesis class is nonempty *exactly* when the plane has a weak measurable
six-colouring; the free-label subclass is empty unconditionally. This is the sharpest statement
of the frontier: a global free label plus `(5.3)` at distance one is not weaker than the
colouring problem, it is stronger (it forces five colours, which is impossible).

## 7. Audit notes on the previous record

1. **`(5.3)` is used at finite distance.** `sprint/k6/REPORT.md` §4 states that Theorem C's
   models satisfy "the exact local `(5.3)` transport", and the summary of the frontier treats
   `(5.3)` as if only its small-distance shadow mattered. The paper uses assertion 3 of
   Lemma 5.2 in Lemma 5.5 with `d = |y - x| < 1/2` and in Lemma 6.7 with `d = 1` (Lemma 3
   above). No proof of any case of Theorem 6.5 can therefore dispense with `(5.3)`; the correct
   statement is that the *cycle-specific* arguments of §6.3.1–6.3.2 and §8 do not use it
   beyond Lemma 5.5, not that the paper does not use it.
2. **Theorem C does not refute the paper's hypotheses.** Its models are translation invariant
   and therefore violate Lemma 1 at `z = x + f` (Corollary 2). The no-go remains valid for the
   hypothesis list of `(P1)–(P6)`, i.e. for the layers of §6 that use only `(5.2)`, `(5.7)`,
   the palette bound and `(6.2)`; it must not be quoted as a no-go for `(5.3)`.
3. **The orbit count 510 is confirmed independently** (`orbit_audit.py`, own domain enumeration
   and own filtering): 510 cyclic six-words over the 16 admissible free-label palettes, 150 of
   them all-pairs, 6 with the `(3,2,3,2,3,2)` pattern. The filters (Lemma 2, MON, `(C1)`,
   `(C2)`) cut nothing on this stratum, as the report says.
4. **`(5.3)` at distance one is the exact place where translation invariance dies**, so no
   sector model — however fine the resolution — can serve as a countermodel to the paper's
   hypotheses. The right parameter for the countermodel programme is the transport radius, and
   Theorem 6 gives its exact value in the free-label sector class.

## 8. Reproduction

Everything is in this directory (`/workspace/nucleus/work/projects/.../.ultramath/smwfwi7rh/m13`),
run with `python3` (numpy, sympy, mpmath, scipy, python-sat are installed; CaDiCaL is used
through pysat). No network access is needed.

| command | what it checks | time |
|---|---|---|
| `python3 sector_csp.py km 1 20` | `K_max(m) = floor(m/5)`, DFS + arc consistency | ~15 s |
| `python3 sector_sat.py` | the same for `m <= 30` by CDCL | ~25 s |
| `python3 alpha_milp.py` | `alpha = 3(m-K)`, hence UNSAT for `K > m/5` (independent) | ~50 s |
| `python3 arc_max.py` | per-arc maximum `= m-K` (the upper-bound claim) | ~7 s |
| `python3 construct_closed.py` | the closed-form construction, `5 <= m <= 5000` | ~1 s |
| `python3 geometry_fast.py` | `Sigma`, `d* = 0.1755705045849462603...`, the `d_crit` table | ~6 s |
| `python3 geo_check.py` | brute-force reach of `(5.3)` versus Lemma 4's offset set | ~8 s |
| `python3 tables.py` | every number quoted above | ~13 s |
| `python3 orbit_audit.py` | the 510/150 orbit audit | ~50 s |
| `python3 nolabel.py` | `K_max(m) = floor(m/3)` without the free label, and the `k = 5` calibration | ~220 s |

Files: `sector_csp.py` (DFS), `sector_sat.py` (CDCL), `alpha_milp.py` (independence number),
`arc_max.py` (arc DP), `construct.py` + `construct_closed.py` (constructions), `nolabel.py`
(no-free-label CSP), `geometry.py`
(slow, superseded) and `geometry_fast.py` (reach `Sigma`), `geo_check.py` (brute force
geometry), `orbit_audit.py`, `tables.py`, `paper/paper.txt` (extracted paper text).

Numerical certification: `Sigma` is computed with `mpmath` at 40 digits from the closed
formula `dev(psi) = atan2(d sin psi, 1 + d cos psi) + arccos(sqrt(1 + 2 d cos psi + d^2)/2) -
pi/3`, maximised by a 2000-point scan followed by a derivative bisection to `1e-28` (or a
golden-section search where the derivative degenerates, e.g. at `d = 1`); at four distances
`d in {0.05, 0.1, 0.176, 0.25}` the maximiser was re-checked against an independent
400000-point scan and agrees to `4e-12`. Every integer comparison entering Theorems 5 and 6 is
made with a large margin: shifting `d` by `1e-9` leaves `K(d,m)` unchanged for every table entry
with `d <= 0.5` (checked), and at the thresholds `d_crit(m)` one has `K = floor(m/5)` exactly,
`K = floor(m/5) + 1` at `d_crit(m) + 1e-9` (checked for `m = 5,10,12,20,60`; the slope
`Sigma'(d*) = 1.23606798` gives a margin of `m * 1.2e-9`, far below one sector). Near `d = 1`
the function approaches its supremum `2 pi/3` like `2 pi/3 - O(sqrt(1-d))` (values
`1.4593, 1.8943, 2.0311, 2.0744, 2.0944` at `d = 0.9, 0.99, 0.999, 0.9999, 1`); no threshold
in this note lies there. `Sigma(1) = 2 pi/3` is exact, and `Sigma(d*) - pi/15 < 2e-17`. The
geometry of Lemma 4 was cross-checked against a brute-force solution of `s + t = f + a` on a
grid of `(phi, psi)` pairs for `m = 6, 12` and five distances (`geo_check.py`): the observed
offset sets are exactly the predicted ones.
