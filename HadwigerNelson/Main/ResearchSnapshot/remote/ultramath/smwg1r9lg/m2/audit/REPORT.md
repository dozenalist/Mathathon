# Audit of the four palette-level constraints the `k = 6` record rests on

**Member m2, swarm `smwg1r9lg`, direction `d8`.**
Object: m7's circle–palette disjointness (Lemma 1) and two-coloured-circle rigidity (Lemma 2);
m9's unit-triangle count; m12's sum-set density transport; m11/m13's frozen-field transport radii.
These are the four constraints that d1 plans to add to m6's single-centre decision problem, and
none of them is machine-checked.

**Verdict.** All four are *correct as mathematics*: each statement, re-read from the paper's
hypotheses, is true and I re-derive it here (§1). Seven defects were found (§3); none of them
changes a `k = 6` verdict, two of them mean that a certificate printed in the record belongs to a
model that another record file has withdrawn, and one of them (D7) *settles an item the record
lists as unchecked*: the claim that m6's `STRIP(6,5)` witness is excluded by Lemma 6.4 is false,
and m7's own `(6,5)` table already says so. The finite computations were re-decided from scratch by two
independent programs (§2); every elimination in m12's table is reproduced with an explicit
witness, the frozen radii are re-derived and confirmed, and two of the four (m9's, m12's) are not
single-centre palette constraints, which matters for the composition d1 plans (§4).

Everything below is either proved from the paper's hypotheses or decided by an exact computation
whose output is in this directory. Nothing here decides `(W)` at six colours.

---

## 1. The four constraints, with their exact hypotheses, re-derived

Notation as in the record: `c` a weak measurable `k`-colouring, `A_i` its classes, `P_x(e)` the
maximal palette in direction `e` at the centre `x`, `D_{x,i} = {e : i in P_x(e)}`, `R` rotation of
directions by `kappa = pi/3`, `sigma` angular measure on `S^1`. The inputs used, all from the
paper unless stated:

* **(5.2)** for a.e. pair `(e,v)` of directions, `c(x+e+v) notin P_x(e) union P_x(v)`;
* **Lemma 5.2(2)** if `e` is an angular density-one point of `D_{x,i}`, then for every `v` not
  parallel to `e` the spatial density of `A_i` at `x+e+v` is zero;
* **(5.3)** Lemma 5.2(3), in the constant-endpoint instance of Remark 5.3, `(x+a)+f = x+f+a` with
  `|a| = 1`: **`P_{x+a}(f) cap P_x(f) = empty` for a.e. `f`** (this is (TE) of the record);
* **(5.7)** Corollary 5.4: `P_x(f) cap P_x(Rf) = empty` a.e.;
* **Lemma 4.3**: two spatial density-one points of one class are never at distance exactly one;
  the non-density set is plane-null;
* **support property** of Definition 5.1: if a trace `b in W_x` is supported in `T` a.e. then
  `P_x(f) cap T != empty` for a.e. `f`;
* **(SA)** self-avoidance (record, `STRUCTURE.md` L.1): `c(x) notin P_x(e)` a.e. at a typical `x`.

### 1.1 m7 Lemma 1 (circle–palette disjointness) — correct

**Statement.** For every centre `x` and `sigma`-a.e. unit direction `e`,
`P_x(e) cap Col(S(x+e,1)) = empty`, where `Col(Gamma)` is the set of labels occupying positive
angular measure on the circle `Gamma`. Hence `|P_x(e)| + |Col(S(x+e,1))| <= k`.

**Proof (re-derived).** Fix `x`. By (5.2) the set `N = {(e,v) : c(x+e+v) in P_x(e) union P_x(v)}`
is `sigma x sigma`-null. For `sigma`-a.e. `e` the section `N_e` is `sigma`-null, so
`{v : c(x+e+v) in P_x(e)} ⊆ N_e` is angularly null. A label `j in P_x(e)` would put
`{v : c(x+e+v) = j}` inside that null set, so `j notin Col(S(x+e,1))`. ∎

*Quantifier.* The null set of `e` depends on `x`; the statement is "for a.e. `e`, at this fixed
`x`", which is the only form the paper supports (no joint measurability of `P` in the centre).

**Corollary (m7 1.2, the circle independence ratio), re-derived.** On a unit circle, `|z-z'| = 1`
iff the angular difference is `+-pi/3`, so a measurable set `A` carrying one label satisfies
`A cap RA = empty`, whence `2 sigma(A) = sigma(A) + sigma(RA) <= 2 pi`, i.e. `sigma(A) <= pi`.
The bound is attained by alternating half-arcs of length `pi/6`. Correct; the three-label analogue
of the rigidity statement fails (a `3`-periodic assignment `a -> b -> c -> a` under `R` is proper).

### 1.2 m9 Theorem 1 (unit-triangle count) — correct (with one displayed-formula defect)

**Statement.** For a unit equilateral triangle `p,q,r`,
`sum_{i in {p,q,r}} (1/2pi) int_S |P_i(f)| dsigma(f) <= k`.

**Proof (re-derived).** For `a` of length one, (TE) gives `P_{x+a}(f) cap P_x(f) = empty` for
`f` outside a null set; intersecting three such statements gives, for a.e. `f`, that
`P_p(f), P_q(f), P_r(f)` are pairwise disjoint subsets of `[k]`. Hence
`|P_p(f)|+|P_q(f)|+|P_r(f)| <= k` a.e. and the integral bound follows. ∎

**The `k = 6` residue.** If all three are `>= 2` a.e. then `2+2+2 = 6 = k`, so equality forces all
three to be pairs a.e. If `|P_p| = 3` on a positive-measure set `E`, then for a.e. `e in E`
`|P_q(e)| + |P_r(e)| <= 3`, so one of `q,r` has a positive-measure singleton set. Both claims hold
and are pointwise (no palette bound is used). *Calibration:* at `k = 5` the same line reads
`2+2+2 > 5`, so a unit triangle never carries three pairs a.e. — the paper's `k = 5` mechanism.

**Defect D1.** The summary of m9's own report displays `int_S |P_i(f)| dsigma(f) <= k` without the
`1/(2pi)`; with `sigma` of total mass `2pi` and `|P_i| >= 1` that display is false (`3*2pi > 6`).
The theorem inside the report, line 135, has the correct normalisation. Formula-level only.

### 1.3 m12 Theorem 1 (sum-set density transport) — correct

**Statement.** Let `G_1, G_2 <= [k]` be disjoint and `E_1, E_2 <= S` measurable with
`sigma(E_j) > 0` and `G_j <= P_x(e)` for a.e. `e in E_j`. Put
`Z = {x + e^{ia} + e^{ib} : a in E_1^*, b in E_2^*, non-parallel}`, `E_j^*` the density-one points.
Then for every finite `Q <= Z` whose unit pairs are its edges, `|[k] \ (G_1 u G_2)| >= chi(Q)`.

**Proof (re-derived, and it checks out step by step).** For `a in E_1^*`, `b in E_2^*` non-parallel:
`E_1 \ D_{x,i}` is null for `i in G_1`, so `a` is a density-one point of `D_{x,i}`, and Lemma
5.2(2) makes `z = x+a+b` a point of density zero for `A_i`; same for `i in G_2` from `b`. Finitely
many density-zero sets cannot fill a ball, so `U = union_{i in T'} A_i`, `T' = [k]\(G_1 u G_2)`,
has upper density one at every point of `Z`. Given `Q = {q_1..q_n} <= Z`, the sets
`W_j = {w : q_j + w in U}` have density one at `0`, so does their intersection, and the set of `w`
for which all `q_j+w` are density-one points of their own class is conull; choose `w` in both. Then
`q_j + w` carries a colour in `T'` and unit pairs of `Q` get different colours (Lemma 4.3), so `c`
restricted to `Q+w` is a proper colouring of `Q` by `|T'|` colours. ∎

*Consequence used in the record:* `k - |G_1 u G_2| < chi(Q)` is a contradiction. At `k = 6`:
`|G_1 u G_2| = 5` needs a unit edge, `= 4` a unit triangle, `= 3` a 4-chromatic unit-distance graph,
`= 2` a 5-chromatic one. The realised instance is m12's Theorem 2 (the paper's Lemma 6.4 triangle):
`gamma = 2 arcsin(1/(2 sqrt3))`, `cos gamma = 5/6`, `|1-e^{i gamma}| = 1/sqrt 3`, `psi = pi+gamma`;
if `t, t+120, t+240 in E_1` and `t+psi+{0,120,240} in E_2` (or swapped), then
`z_j = x + e^{i(t+2j kappa)}(1 - e^{i gamma})` is a unit equilateral triangle in `Z`. I re-checked
the three identities exactly (`2 - 2*(5/6) = 1/3`, `|e^{2i kappa}-1|^2 = 3`, `3*(1/3) = 1`).

### 1.4 m11/m13 (frozen-field transport radii) — correct, but only one-sided as recorded

A centre-independent ("frozen") field has `P_z = P`, so (TE)/`(5.3)` at separation `d` reads
`P(f) cap P(f + delta_pm(d,psi)) = empty` a.e. in `f = e^{i psi}`, where for `w = d + e^{i psi}`,
`r = |w|`,
`delta_pm = arg w +- arccos(r/2) - psi` are the two shifts of Lemma 5.2(3). For a sector word of
period `Delta = 10 deg` this is a condition on the integers
`j in [floor(m(d)/Delta), floor(M(d)/Delta)+1]`, `M = max |delta|`, `m = min |delta|`, and it holds
iff every such `j` (and `-j`) is *safe*: `word[i] cap word[i+j] = empty` for all `i`.

I re-derived `M(d), m(d)` independently (`radii.py`, 4e6 grid, 30-digit refinement):

| `d` | `M(d)` deg | `m(d)` deg |
|---|---|---|
| 0.1 | 66.734026 | 53.487368 |
| 0.14715 | 69.999799 | 50.481789 |
| 0.28558 | 80.000358 | 41.857902 |
| 0.3 | 81.083204 | 40.974630 |

The block words have safe set `{4..8} mod 12`, so their window is `[40,80)` deg and the flip is at
`M = 80 deg`, i.e. `d = 0.28558`; the two ell=6 words have safe set `{5,6,7} mod 12`, window
`[50,70)`, flip at `M = 70 deg`, i.e. `d = 0.14715`. Both recorded numbers are confirmed. **Defect
D3** is that these are *lower* bounds as recorded (see §3).

---

## 2. The finite computations, re-decided from scratch

Two independent programs, no shared code with the record:

* `audit_gamma.py` — exact rational interval algebra on direction sets. `U_j = orbit3(E_j)` is
  computed exactly, and the criterion `psi in U_B - U_A` (or swapped) is decided by testing the
  *whole* rational enclosure of `psi` (`consts.py`: `psi = 213.55730976192071...deg`, width
  `4e-38`, from interval arithmetic on `cos gamma = 5/6` with exact dyadic boundaries) against the
  exact rational difference set; witnesses are then verified by interval containment for the whole
  enclosure.
* `second_check.py` — brute-force scan of `t` over a `0.05 deg` rational grid testing the six
  membership conditions directly.

Both agree on every model. Output (`out_audit_gamma.txt`, `out_second_check.txt`):

| model (as named in the record) | values | verdict |
|---|---|---|
| Theorem C / m15 block, `ell=3,4,5,6` | 3 pairs | ELIMINATED (4 of 4) |
| FREE-LABEL block `ell=3` | `{3},{4},{5}` | survives (singleton values) |
| FREE-LABEL block `ell=4`, `ell=5` | pairs + singleton | ELIMINATED |
| FREE-LABEL `ell=6`, **withdrawn** 36-sector word | 5 pairs + ternary | ELIMINATED (`A={1,3},B={2,4}, t=93.221345deg`, role `A->B`) |
| FREE-LABEL `ell=6`, **current** 36-sector word | 5 pairs | ELIMINATED (`A={1,3},B={2,5}, t=3.221345deg`, role `A->B`) |
| m13 singleton triangle field | `{4},{5},{6}` | survives (singleton values) |

This reproduces m12's "7 of 9" exactly, including its witness angles, and adds the verdict for the
current `ell=6` word, which the record does not contain (see D2).

**The frozen radii** (§1.4) are re-derived; `M(d), m(d)` above confirm `0.28558` and `0.14715` to
six decimals. The radii apply to *frozen* fields; all are `< 1/2 < 1`, so no frozen field satisfies
`(5.3)` at the two places the paper uses it (`d < 1/2` in Lemma 5.5, `d = 1` in Lemma 6.7).

---

## 3. Defects

**D1 (m9, presentational).** The summary display of the unit-triangle count omits the `1/(2pi)`
normalisation; with `sigma(S^1) = 2pi` the display is false. The theorem in the body is right.

**D2 (m11 + m12 + `sprint/k6/REPORT.md`, stale certificate — the substantive one).**
`sprint/k6/FREE-LABEL.md` withdraws the 36-sector `ell = 6` word that contains the ternary value
`{2,4,5}` and replaces it by the period-12 pair-valued word
`[1,3][1,3][1,3][1,4][1,4][2,4][2,4][2,4][2,5][2,5][3,5][3,5]` (repeated three times).
`m11/model_radii.py` (`W6`), `m12/verify.py` (`FREE_L6`), `sprint/k6/six_free_witness.json` and the
report's §4d/§5 ("a 36-sector word with six values") all still use the withdrawn word.
*Consequence:* no verdict changes — I verified that the current word is eliminated too, that both
words have the same safe set `{5,6,7} mod 12` hence the same transport radius `0.14715`, and that
the current word still satisfies the six transport offsets `{+-5,+-6,+-7}`. But the printed
certificate (`A={1,3},B={2,4},t=93.221345deg`, and the "not 120-degree periodic" remark, which the
current word contradicts: it *is* period-12) belongs to the withdrawn model — `FREE-LABEL.md` has
withdrawn it, while `sprint/k6/REPORT.md` §4d/§5 still describe it, so the two record files also
disagree with each other on which word is *the* `ell = 6` free-label witness.

**D3 (m11, methodological).** `model_radii.py` bisects on a floating-point grid (`sh_interval`,
`N = 4000` samples) and, from the sampled `lo, hi`, requires *every* integer
`k in [floor(lo/Delta), ceil(hi/Delta)]` to be safe. Requiring more than is achieved can only
shrink the computed radius, so what is certified is "`(5.3)` holds for all `d <= 0.28558`", not
"only for". The record's phrasing ("meet (5.3) **only** for `|z-z'| <= 0.28558`") is an
overstatement; in fact both flips are located exactly at `M(d) = 80deg` resp. `70deg`, which is
what makes the numbers right (my §1.4 recomputation). Two-sided rigorous bounds are available from
the Lipschitz bound `|d delta/d psi| <= 1 + d/(1-d)^2 + d/(2(1-d) sqrt(1-(1+d)^2/4)) < 2` for
`d <= 0.31` together with a grid maximum, giving brackets of width `~1e-5` around the two values.

**D4 (m12, methodological).** `m12/verify.py:check_witness` tests `t + psi + 120j in E_B` only at
the two endpoints `psi_lo, psi_hi` of its enclosure, not on the whole enclosure; an enclosure that
straddles a boundary of `E_B` would pass. It cannot happen for the printed witnesses (they lie
degrees inside their arcs), but the check as written is not a proof. My `audit_gamma.py` checks
interval containment for the whole enclosure.

**D5 (record, overstatement).** The ledger line "Lemma 5.2(2) alone kills 7 of the 9" should read
"without properness, trace-consistency or maximality": Theorem 1 uses Lemma 5.2(2) *and* Lemma 4.3
and the measurability of the colour classes.

**D6 (record, sharpness).** "The survivors are exactly the singleton-valued ones" is arithmetical,
not geometrical: for singleton values `|A u B| = 2`, so `|T'| = 4 >= 3 = chi(triangle)` and the
mechanism cannot bite whatever the direction sets are. A kill of a singleton model would need a
5-chromatic finite unit-distance graph inside the sum set. So the correct statement is: *no model
in the record is killed by this mechanism unless it has two values with `|A u B| >= 4`*, and no
model with only singleton values is excluded by it at all.

**D7 (record, false claim; settles the `STATUS.md` open item).** `STATUS.md` lists as unchecked
"`m2`'s claim that `m6`'s `{5}/{1,3}` `STRIP(6,5)` witness is killed by Lemma 6.4". The claim is
false. m6's witness has palette values `A = {5}`, `B = {1,3}`, so `|A u B| = 3 = k-3`, and the
k-general Lemma 6.4 (m7's Theorem 2') forces `|A| + |B| <= k-3`, which is met with **equality**;
m7's own table for `(k,ell) = (6,5)` lists exactly the five pairs that escape, "all `{Z}` + one
diagonal". The m12 mechanism then reads `|T'| >= chi(Q)`, i.e. `3 >= 3`, and is silent
(`m6strip.py`: `orbit3` of both direction sets is the whole set, `psi` lies in both difference
sets, so a unit triangle does exist in the sum set — and it is properly 3-colourable, costing
exactly the three labels of `T'`). So `smwfycxze/m2`'s `RESULTS.md` §6a ("Correction to the
record: ... is excluded by the same lemma for the same reason") is itself in need of correction:
`m6`'s `STRIP(6,5)` SAT verdict is not touched by Lemma 6.4. m2's *conclusion* is unaffected —
its three-valued field of Theorem 5 repairs the example — but its stated reason is not.
A kill of this witness would need a 4-chromatic unit-distance graph inside
`Z(E_{5}, E_{1,3})`; nothing in the record exhibits one (§5 gives the exact criterion).

---

## 4. What each constraint bites at `k = 6`, with witnesses

| constraint | objects it speaks about | does it bite at `k = 6`? | witness that it does not bite further |
|---|---|---|---|
| m7 Lemma 1 | one centre `x`, a.e. direction `e`, **plus the colouring of the circle** `S(x+e,1)` | yes, but only against the circle: `|P_x(e)| + |Col| <= k` | m13's field: palettes are singletons, so the constraint reads `1 + |Col| <= 6`; nothing is excluded. The *converse* (pair palettes force fat circles) needs the palette at a prescribed direction, i.e. joint measurability in the centre — m7's own caution, which is correct |
| m9 Theorem 1 | a **unit triangle** (three centres) | tight: `2+2+2 = 6` | attained: three disjoint pairs at a common direction satisfy it with equality; m13's field has `1+1+1 = 3`, far from tight |
| m12 Theorem 1/2 | two palette values on positive-measure direction sets, **plus the colouring's density transfer** | kills 4/4 block fields and 3/3 free-label pair fields | the two singleton models: `|A u B| = 2`, so only a 5-chromatic graph in the sum set would kill them; none is known in a disc of radius 2 |
| m11/m13 radii | centre-independent fields only | excludes every frozen field at `d = 1` and at `d < 1/2` | a frozen field is excluded *already* by (TE) alone (`P(f) cap P(f) = empty`, m13 Cor. 2), so the radii add no constraint on colourings |

Two consequences for the composition planned in d1:

1. **Neither m9's count nor m12's transport is a single-centre palette constraint.** m9 needs three
   centres at mutual distance one; m12 needs the spatial density transfer of Lemma 5.2(2) at the
   points `x + e + v`. Only m7's Lemma 1 and m11's density bound are available at one centre — and
   even m7's needs a second kind of variable, the colouring of a unit circle, which is why m7's own
   single-circle layer is the honest form of it (m7 §5 decided that layer satisfiable at `k = 6`).
2. **The `k = 5` calibration of the mechanism.** At `k = 5` the same table reads
   `k - |G_1 u G_2| < chi(Q)`, so `|G_1 u G_2| = 3 = k-2` already dies by a unit triangle: that is
   the paper's Lemma 6.4. At `k = 6` the same group size needs a 4-chromatic graph. So the
   mechanism loses exactly one label of power between five and six colours, matching m9's count.

---

## 5. One new necessary condition (chromatic form; overlapping palette values)

m12's Theorem 1 is stated for *disjoint* groups and is applied to *disjoint* palette values. The
mechanism needs neither.

**Theorem S.** Let `c` be a weak measurable `k`-colouring, `x` a centre, and `A != B` two palette
values (any subsets of `[k]`, possibly overlapping), with `E_A = {e : A <= P_x(e)}` and
`E_B = {e : B <= P_x(e)}` both of positive angular measure. Put `T = [k] \ (A u B)` and
`Z = {x + e^{ia} + e^{ib} : a in E_A^*, b in E_B^*, non-parallel}`. Then every finite set
`Q <= Z` with unit edges satisfies `chi(Q) <= |T|`.

*Proof.* Apply Theorem 1 to `G_1 = A`, `G_2 = B \ A`. They are disjoint, `G_1 <= P_x(e)` on `E_A`
and `G_2 <= P_x(e)` on `E_B`, and `[k] \ (G_1 u G_2) = T`. ∎

Consequences not in the record:
(i) m12's Corollary 3 is the case `A cap B = empty`, `|A u B| >= 4`;
(ii) the "unit triangle" of Theorem 2 can be replaced by **any non-bipartite finite unit-distance
graph in `Z`** — e.g. a closed odd walk of unit steps — since `chi >= 3` is all that is used on the
`|A u B| >= 4` row;
(iii) at a six-cycle centre, where no palette is a singleton (trace argument of Lemma 6.2,
`STRUCTURE.md` L.3), two *distinct* values with `|A u B| = 3` (two pairs sharing a label) are
covered: `Z` must then contain no 4-chromatic unit-distance graph, in particular no Moser spindle.
The record's tools are silent on `|A u B| = 3` because they insist on disjoint values.

Sharpness: nothing here kills the singleton models (`|A u B| = 2` needs `chi >= 5`), so Theorem S
does not change the frontier; it sharpens the necessary condition that a six-cycle countermodel at
`k = 6` must satisfy.

Instances that the record leaves open, and that Theorem S covers: (a) at a *four-cycle* centre the
13 pairs that escape m7's Theorem 2' ("outsider singleton + a set of size `<= 2`") are exactly the
`|A u B| = 3` case, so for each of them `Z` must contain no 4-chromatic unit-distance graph;
(b) `m6`'s `STRIP(6,5)` witness `{5}/{1,3}` (D7) is the same case at a five-cycle centre.

---

## 6. What I did **not** do

* I did not decide `(W)`; nothing here bounds `chi(R^2)`.
* I did not decide whether an odd closed unit walk or a Moser spindle can sit inside the sum sets of
  the two surviving models, nor inside `Z(E_{5},E_{1,3})` of D7; Theorem S is a necessary
  condition, not a decision. That decision is a 3-parameter rigid-motion search (the Moser spindle
  is rigid), and it is what a positive answer to D7 would require.
* I did not re-run the Lean cores (that is d8/d6 of the board, member m7) nor the paper's §7 (m3), nor
  m6's orbit system (m1).
* The radii brackets in D3 are stated via a Lipschitz bound; the numbers printed in §1.4 are
  high-precision values, and the *bracket* statement is `M(d) = 80 deg` at `d = 0.28558 +- 1e-5`.

## 7. Reproducing

```
cd .ultramath/smwg1r9lg/m2/audit
python3 consts.py        # rigorous psi enclosure (interval arithmetic, exact dyadic bounds)
python3 audit_gamma.py   # exact interval-algebra decision of m12's criterion, all 10 models
python3 second_check.py  # independent grid scan of the same criterion
python3 radii.py         # M(d), m(d) for the frozen fields
python3 m6strip.py       # the D7 arithmetic on m6's STRIP(6,5) witness
```
Outputs in `out_consts.txt`, `out_audit_gamma.txt`, `out_second_check.txt`,
`out_radii.txt`, `out_m6strip.txt` (all exit 0 at the time of writing).
