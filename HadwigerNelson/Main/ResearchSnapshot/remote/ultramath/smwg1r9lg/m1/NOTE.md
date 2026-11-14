# d1: composing the §8 orbit layer with m7's circle constraint, m9's unit-triangle count and m11's density bound

**Member m1, swarm `smwg1r9lg`, direction `d1`.**
Deliverable type: **a decided finite computation plus a certified dead-route statement**
for a delimited class. Everything below is exact integer arithmetic; no floating point is
used in any decision. Commands are in §8.

---

## 0. Result in one paragraph

At `k = 6` the §8 pointwise layer at a cyclic centre (m6's per-cell orbit system) is
**saturated** with respect to the three extra families: adding

* m7's circle–palette inequality `|P_x(e)| + |Col(S(x+e,1))| <= k`,
* m9's unit-triangle count `sum_{p,q,r} int_S |P| dsigma/2pi <= k`,
* m11's `sigma{B subset P_x} <= 1/2` (every nonempty `B`),

and even the two further single-centre constraints of the record `(C1)` (no complementary
triple values) and `(MON)` (no monochromatic unit sum), and even `(5.3)` at separation one
(`(TE)`) on the six unit neighbours `x + R^j e` of the centre, changes **nothing**: the
satisfiable `(label, cell)` pairs are exactly m6's, the surviving configurations are exactly
m6's (`16848 / 390936 / 268200 / 252` for `ell = 3,4,5,6`), and — this is the sharpest form
— **every word** that satisfies the per-cell system in a satisfiable cell already satisfies
all of them (verified exhaustively: `3168` words over the `108` satisfiable `(label,cell)`
pairs at `ell = 6`, `669960` words over the `2880` pairs at `ell = 5`; `0` exceptions).

Moreover this is not an accident of the enumeration. Four of the five additions — m11's bound
(Lemma N1), m9's count (Lemma N3), m9's ternary rigidity (Lemma N4) and `(C1)` (corollary of
`(SA)`) — are **consequences of the per-cell system**, so they cannot cut; the fifth, m7's
inequality, is strictly weaker than the palette bound `(PB)` (Lemma N2). `(MON)` is the only
item without a proof of redundancy, and the census shows it cuts nothing either. The remaining
item, `(TE)` at separation one, is inert for a structural reason: the six neighbour palettes it
constrains are not determined by the orbit word (§4).

Calibration: at `k = 5`, `ell = 5` the same decision returns **0** survivors, reproducing
Proposition 8.2 (§6).

---

## 1. The class, exactly

Fix `k`, `ell in {3,4,5,6}`, a weak measurable `k`-colouring `c` with the paper's notation
(`P_x(e)` the maximal palette of Definition 5.1, `R` rotation of directions by `pi/3`,
`sigma` normalised angular measure, `i = c(x)` the colour of a typical centre `x`), and a
cyclic centre `x` whose `Gamma_x` contains a simple cycle on the labels `0..ell-1`, edges
`j = {j, j+1}`, with limiting directions `v_j` as supplied by §7 (Theorem A of
`sprint/k6/REPORT.md`). Let `e` be a base direction, `y_j = x + R^j e`.

**COMBO(ell,k)** is the following finite system on the 42 palettes

    P_p := P_x(R^p e)        (p in Z/6)          the orbit at the centre x
    Q_{j,m} := P_{y_j}(R^m e)  (j,m in Z/6)      the six unit neighbours, same six directions

together with the centre colours `i = c(x)` and `c_j := c(y_j)` and the circle colour sets
`C_p := Col(S(y_p,1))`:

| item | statement | source | legitimate because |
|---|---|---|---|
| (S14) | `P_p cap O_p != empty`, `P_p cap I_p != empty`, with `O_p,I_p` the allowed sets of Lemma 8.1 in the cell containing `e` | Lemma 8.1, (8.1) | a.e. statement at the fixed centre `x` |
| (PB) | `1 <= |P_p| <= k-3` | Prop. 5.6 (the `k=6` case is `|P| <= 3`) | a.e. at `x` |
| (5.7) | `P_p cap P_{p+1} = empty` | Cor. 5.4 | a.e. at `x` |
| (E) | `P_p` is not contained in any edge of the cycle | Lemma 6.2, (6.2) | at `x` |
| (SA) | `i notin P_p` | Lemma D of `sprint/k6/STRUCTURE.md` | at a typical `x` |
| (TR1) | `Q_{j,m} cap P_m = empty` | (5.3) + Remark 5.3 at the unit pair `(x, y_j)`: `y_j + f = x + f + R^j e` | a.e. in `f`, at the fixed pair |
| (TR2) | `Q_{j,m} cap Q_{j+1,m} = empty` | (5.3) at the unit pair `(y_j, y_{j+1})` | `|y_{j+1}-y_j| = |e-Re| = 1` |
| (TR3) | `Q_{j,m} cap Q_{j,m+1} = empty` | (5.7) at `y_j` | a.e. at `y_j` |
| (TR4) | `1 <= |Q_{j,m}| <= k-3` | (PB) at `y_j` | a.e. at `y_j` |
| (TR5) | `c_j notin Q_{j,m}` | (SA) at `y_j` | `y_j` typical |
| (TR6) | `c_j in P_j` and `c_j != c_{j+1}` | endpoint trace `c(x+e) in P_x(e)` (Lemma P) and properness on the unit pair `(y_j,y_{j+1})` | a.e. in the base direction |
| (A) | `|P_p| + |C_p| <= k`, `C_p cap P_p = empty`, `|C_p| >= 2` | m7 Lemma 1 / Cor. 1.1, 1.3 | at the fixed centre `x` |
| (B) | `|P_m| + |Q_{j,m}| + |Q_{j+1,m}| <= k` | m9 Theorem 1, pointwise form, at the unit triangle `(x, y_j, y_{j+1})` | a.e. in the common direction `R^m e` |
| (C) | `sigma{B subset P_x} <= 1/2` for every nonempty `B` | m11 | measure statement at `x` |

All twelve items are a.e.-in-direction statements at **finitely many** centres, so a common
conull set of directions exists and the base direction `e` may be chosen in it; each item is
therefore legitimate at the specified directions. Nothing here evaluates a palette at a
"prescribed" direction against a centre chosen afterwards, which is exactly the step m7's
caution (§4(a) of its report) forbids: the paper assumes no joint measurability of
`P_x(e)` in `x`, so all directional quantifiers are taken first, and only then is `e` fixed.

**Not in the class** (and why): `(5.3)` between a pair of cluster centres at a separation
`!= 1` couples `Q_{j,m}` to `P_x(s(R^m e))` for directions `s(R^m e)` outside the six orbit
directions, so it is not a finite system on these 42 variables; and the endpoint trace at a
second centre, together with `(5.7)`, is equivalent to `chi(R^2) <= k` (m10 Thm 4, m15 Thm C,
m11 Thm B). Those are the boundaries of the class, not omissions.

---

## 2. Lemma N1 and Lemma N2: (C) and (A) are consequences of what is already there

**Lemma N1.** For every centre `x` and every nonempty `B subset [k]`, put
`S_B = {e : B subset P_x(e)}`. Then `(5.7)` at `x` gives `S_B cap R^{-1}S_B = empty`, hence
`sigma(S_B) <= 1/2`. So m11's bound is a consequence of `(5.7)` alone and adds nothing to any
system that contains `(5.7)` a.e. at `x`.

*Proof.* If `e in S_B cap R^{-1}S_B` then `B subset P_x(e)` and `B subset P_x(Re)`, so
`P_x(e) cap P_x(Re) supseteq B != empty`, which `(5.7)` excludes a.e. Hence
`sigma(S_B) + sigma(R^{-1}S_B) = sigma(S_B cup R^{-1}S_B) <= 1` and the two measures are
equal. `square`

Sharpness is m11's: equality is attained by any two-valued alternating field. Note `B` may
be a triple, so this covers the ternary case that m11 proves separately.

**Lemma N2.** Let `y` be a point such that `(y,1)` is a typical circle sampling (a.e. `y`).
Then `|Col(S(y,1))| >= 2`. Consequently `(A)` follows from `(PB)`: `(A)` reads
`|P_x(e)| <= k - |C_p| <= k - 2`, while `(PB)` gives `|P_x(e)| <= k-3 < k-2`.

*Proof.* `Col(S(y,1)) = {b}` would put `A_b` of full angular measure on `S(y,1)`; two points of
`S(y,1)` at angular distance `pi/3` are at distance one, so two typical points of `A_b` would be
at distance one, contradicting Lemma 4.3. (This is m7's Corollary 1.2: every label occupies at
most half of a unit circle, so a unit circle carries at least two labels.) `square`

So **m7's inequality is strictly weaker than the palette bound** at every `k >= 4`: it permits
palettes of size `k-2`, the palette bound permits `k-3`. Its positive content (m7's Cor. 1.3:
a ternary palette forces the circle about `x+e` to be at most 3-coloured) is a statement about
a *different* centre and is satisfiable by m7's own single-circle computation (234 solutions at
`m = 6` sectors for a 3-coloured circle). In COMBO it is carried by the explicit `C_p` variable,
and `C_p` always exists: `[k] \ P_p` has at least `k-3 >= 3` elements, and any set of `>= 2`
labels is realisable as the colour set of a proper measurable colouring of a unit circle (the
circle's unit-distance graph is a disjoint union of `6`-cycles, each 2-colourable, and m7's
Corollary 1.2 is then attained with equality).

---

## 3. Lemma N3 and Lemma N4: (B) and m9's rigidity are theorems of the per-cell system

**Lemma N3.** At a unit triangle `p,q,r` and for a.e. common direction `f` the three palettes
are pairwise disjoint, hence `|P_p(f)|+|P_q(f)|+|P_r(f)| <= k` pointwise; integrating gives
m9's Theorem 1. Conversely m9's inequality is implied by the pointwise statement, i.e. by
`(5.3)` at separation one. So in COMBO the whole content of `(B)` is `(TR1)`+`(TR2)`.

*Proof.* Pairwise disjointness is `(5.3)` with `s(f) = f` and `t` constant (Remark 5.3) at each
of the three unit pairs. `square`

**Lemma N4 (m9's ternary rigidity is a theorem of the per-cell system).** Let `x` be typical
with `c(x) = i` and suppose no palette on the `R`-orbit of `e` is a singleton. Then `(5.7)`,
`(SA)` and nonemptiness give

    if |P_x(e)| = 3 then P_x(Re) = [k] \ (P_x(e) union {i})  and  P_x(R^2 e) subseteq P_x(e).

(This is m9's Lemma 5.) *Proof.* `(5.7)` gives `P_x(Re) cap P_x(e) = empty` and `(SA)` gives
`i notin P_x(Re)`, so `P_x(Re) subseteq [k] \ (P_x(e) union {i})`, a set of `6-3-1 = 2`
elements; nonemptiness plus "no singleton" forces equality. Then `(5.7)` at `Re` and `(SA)`
give `P_x(R^2e) subseteq [k] \ (P_x(Re) union {i}) = P_x(e)`. `square`

In the per-cell system of §1 the hypothesis "no singleton on the orbit" is automatic at
`ell = 6`: a singleton `P = {b}` would satisfy `P subseteq {b,b+1}`, and `{b,b+1}` is an edge
of `C_6` on all six labels, which `(E)` forbids. Hence at `ell = 6` **m9's rigidity is a
consequence of `(PB)`+`(5.7)`+`(E)`+`(SA)` and cannot cut anything**; at `ell <= 5` the same
argument applies to every word that has no singleton, and on a word that does have one the
hypothesis of the lemma fails. So the rigidity is redundant at *every* `ell` — it is stated
here as a theorem, and the census of §5 confirms it independently.

**Corollary.** `(C1)` (no two values of the word are complementary triples) is a consequence of
`(SA)`: if `P_p = A` then `i notin A`, so `i in [k] \ A`, and no palette can equal `[k] \ A`.

So of the five added families, four — `(C)`, `(B)`, m9's rigidity and `(C1)` — are theorems of
what the §8 layer already contains, and the fifth, `(A)`, is weaker than `(PB)`. This is why the
computation of §5 is a *saturation* rather than a near miss.

---

## 4. Why (TE) is inert: the rim data are under-determined

`(TR1)`–`(TR5)` constrain 36 palettes `Q_{j,m}` by (up to) `108` disjointness conditions against
sets `P_m` of size at most `3`. For a fixed choice of the six rim colours `c_j` the admissible
set at `(j,m)` is `[k] \ (P_m union {c_j})`, of size at least `2`, and a proper colouring of the
grid `C_6 x C_6` (which is `4`-regular and bipartite) by these lists always exists here. The
verification is exhaustive: for **every** word of §5 the system has an explicit solution
(`rim.py`, checker `rim.verify_rim`), and additionally for

* all `20` words with all six palettes ternary and consecutively disjoint,
* `400` random words satisfying `(PB)`+`(5.7)`+`(SA)` at each `ell`,

the rim system is satisfiable (0 failures). So `(TE)` at the six unit neighbours of the centre
imposes no condition on the orbit word at `k = 6`. A general proof of this statement is open;
what is proved here is the exhaustive statement for the class of words that arise, which is all
the decision needs.

---

## 5. The decision

Two independent implementations:

* **A** (`implA.py`, `implA_fast.py`, `combo.py`): row model — a configuration is a choice vector
  `ch in (Z/6)^ell` (the cyclic 3-interval carried by each limiting ray) plus a weak order of the
  ray slippages; per-cell satisfiability by depth-first backtracking over the six cycle positions.
* **B** (`implB.py`): the per-cell decision by a transfer computation over the six-position cycle
  (state = feasible last palette), and the orbit tuples generated from the sign sets directly.
* **Geometry** (`geom.py`): for every weak order and starting cell an explicit rational ray
  configuration `r_j` (in units of `pi`) is built and the cell sequence recomputed from
  `sigma_j(p) = sign cos(pi(q + p/3 - r_j))`; `952` configurations checked (all orders at
  `ell <= 4`, `300` random ones at `ell = 5,6`), `0` mismatches with the row model. The geometric
  walk advances the row index by `-1`; the two conventions `+-1` give identical survivor counts
  (verified separately for all four `ell`), so the convention is immaterial.

**Result at `k = 6`** (certificates `cert_{ell}_6.json`, one per `ell`):

| `ell` | satisfiable `(label, cell)` pairs | words in those cells | survivors (= m6) | SHA-256 of survivor list |
|---|---|---|---|---|
| 3 | 1296 | — (not enumerated) | **16848** | `cc13b8f4927fb836…` |
| 4 | 5352 | — (not enumerated) | **390936** | `12e731e2d82b130d…` |
| 5 | 2880 | 669960 | **268200** | `92a6b83d4c8e84db…` |
| 6 | 108 | 3168 | **252** | `186614b0613b322a…` |

**Saturation.** For `ell = 6` and `ell = 5` all words of all satisfiable cells were enumerated and
tested against each extra family separately:

| addition | `ell = 6` (3168 words) | `ell = 5` (669960 words) |
|---|---|---|
| (L5) m9 ternary rigidity | 3168 | 669960 |
| (C1) no complementary triples | 3168 | 669960 |
| (MON) no monochromatic unit sum | 3168 | 669960 |
| all three | 3168 | 669960 |
| hexagon (TE) | 3168 | 669960 |

So the composition does not exclude one word, one `(label,cell)` pair or one configuration:
**no superposition of m7's Lemma 1, m9's count and m11's bound with the §8 layer can exclude a
cycle of any length at `k = 6`.**

**The residual list** (survivors, exactly as m6 recorded them) is unchanged, and the shape of the
surviving words is unchanged too: at `ell = 6` the minimal witnesses are all pair-valued
(`(2,2,2,2,2,2)` in all 108 cells) and at `ell = 5` the witness patterns are
`(1,2,1,2,1,2)`, `(2,1,2,2,1,2)`, `(1,2,2,1,2,2)`, `(2,2,1,2,2,1)`, `(2,1,2,1,2,1)` with
multiplicities `700/700/700/640/140`. So each added constraint failed to bite for its own
recorded reason and not for want of a witness:

* `(C)` — implied by `(5.7)` (Lemma N1);
* `(A)` — implied by `(PB)` (Lemma N2), i.e. it would only bite if `|P| = k-2` were allowed;
* `(B)` — its pointwise form is `(TE)`, whose rim variables are free (§4);
* m9's rigidity — a theorem of the per-cell system at `ell = 6` (Lemma N4);
* `(C1)` — a consequence of `(SA)` (corollary in §3).

---

## 6. Calibration, and vacuity tests

**`k = 5`, `ell = 5` (Proposition 8.2).** `cert_5_5.json`: `0` satisfiable `(label,cell)` pairs,
`0` survivors, with all five added families present. So the decision procedure reproduces the
paper's `k = 5` exclusion, and the composed system is not vacuously satisfiable.

**`k = 5`, `ell = 3, 4`.** `8424` and `24` survivors respectively — the paper excludes those by
§8.4/§8.10, which are not part of this layer, so the calibration shows the layer is honest at
`k = 5`: it is *not* strong enough to exclude the triangle and four-cycle either.

**Vacuity on the known models.** m13's singleton field and m15's block fields are *abstract*
palette fields (no colouring is defined), so only the palette-level families apply to them;
m3's colouring is a genuine colouring and all six apply.

| model | (L5) | (C1) | (MON) | (TE) |
|---|---|---|---|---|
| m13's singleton triangle field (`P = {4+s(t)}`, translation invariant) | vacuous (no ternary palette) | vacuous | vacuous (`1+1 != k-1`) | **fails**: frozen, `P(f) cap P(f) = P(f) != empty` |
| m15's three-block fields (`{3},{4},{5}` / `{0,2},{1,3},{4}` / `{0,2},{1,3},{5}`) | vacuous (no ternary palette) | vacuous | vacuous | **fails**: frozen |
| m3's proper `k = 7` colouring | vacuous (singleton palettes) | vacuous | vacuous | holds (cell-constant, `|P|=1`) |

and, for m3's colouring, where the other two families are evaluated against the colouring
itself: `(C)` holds with `sigma{B subset P} = 1 <= 1/2`, and `(A)` holds with
`|P| + |Col(S(y,1))| = 1 + 5 = 6 <= 7` on the five-coloured circles and `1 + 4 = 5` on the
four-coloured ones (m7's §5b computation of this colouring). So none of the added families is
empty: `(TE)` — the only one of them independent of the §8 layer — already kills every frozen
countermodel of the record (this is m11's Theorem A, seen here as the `(TR1)` instance). What
§5 shows is that at a genuine cyclic centre it kills nothing.

---

## 7. What this does and does not prove; the boundary

**Proved / decided here.**

1. Lemmas N1, N2, N3, N4 and the `(C1)` corollary — proofs, §2–§3.
2. COMBO(`ell`,6) is satisfiable for `ell = 3,4,5,6`, with the exact survivor counts
   `16848 / 390936 / 268200 / 252` and exact certificates; it is *saturated*: no word, pair or
   configuration is excluded by the added families (§5).
3. COMBO(5,5) is unsatisfiable (`0`), reproducing Proposition 8.2 exactly (§6).
4. Hence: **no proof using only these families at the cyclic centre and its six unit neighbours
   can exclude any cycle length at `k = 6`** — a certified dead route for that class.

**Not proved.** Nothing here decides `(W)`, local finiteness at `k = 6`, or `chi(R^2)`. The
result is about the named families; §4's inertness of `(TE)` is exhaustive for the words that
arise but is not proved in general. Adding the endpoint trace at a *second* centre, or `(5.3)`
at separations `!= 1`, leaves the class and lands on `chi(R^2) <= k` (m10 Thm 4, m15 Thm C,
m11 Thm B); so the frontier this note measures is exactly the frontier of the record: only
properness of the colouring, or the two-valued selection step of Lemma 5.5, remains.

---

## 8. Exact commands

All from `.ultramath/smwg1r9lg/m1`, plain `python3` (standard library only).

```
python3 implA_fast.py 6 6          # A: the per-cell system alone      -> 252
python3 combo.py 6 6               # A: COMBO at ell = 6                -> 252
python3 combo.py 5 5               # calibration                        -> 0
python3 implB.py 6 6               # B (transfer computation)           -> 252
python3 geom.py                    # geometric validation of the row model
python3 cert2.py build 6 6         # write cert_6_6.json
python3 cert2.py verify 6 6        # re-run + check every word and rim witness -> 0 errors
python3 cert2.py build 5 5         # calibration certificate
python3 cert2.py verify 5 5
```

Recorded outputs: `combo.py 6 6` → `surviving configurations 252`; `combo.py 5 5` →
`surviving configurations 0`; `implB.py 6 6` → `252`; `geom.py` → `952 configurations,
0 mismatches`; `cert2.py verify` → `errors 0` for `(3,6), (4,6), (5,6), (6,6), (5,5)`.

| file | content |
|---|---|
| `implA.py`, `implA_fast.py` | implementation A: row model, backtracking decision |
| `implB.py` | implementation B: transfer computation |
| `combo.py` | COMBO decision driver (per-cell system + extras + rim) |
| `rim.py` | the hexagon (TE) system and its exact checker |
| `geom.py` | explicit rational rays, cell reconstruction, row-model validation |
| `cert2.py` | certificate build/verify |
| `cert_{ell}_{k}.json` | certificates: wordbook with (TE) witnesses, satisfiable pairs, survivor list, SHA-256 |
| `wordcensus.txt` | the saturation table of §5 |
