# Audit of the six-colour palette layer: the single-centre system collapses, and two exact certificates

Member `m2`, swarm `smwfwi7rh`, direction `d10` (AUDIT + REPAIR).
Target: the accepted results of swarm `smwfo9zkl` as summarised in `sprint/k6/REPORT.md`,
checked against the paper `attachments/here-are-three-files-ni5n/paper.pdf`.

**Verdict in one line.** The four single-centre orbit rows, the `k = 6` palette bound and the
paper's final seven-point Moser certificate all check out exactly; the seven constraint groups of
`sprint/k6/STRUCTURE.md` Theorem 5 **collapse to two** (Theorem R), so the 510 words at `ell = 6`
carry no information beyond "palettes are 2- or 3-subsets of the five non-centre labels avoiding
cycle edges, and consecutive ones are disjoint"; `alpha < 1/6` in §7 is exactly optimal (§4); and
the `k = 6` frontier recorded in `REPORT.md` §4-§5 is **superseded**: the palette countermodels are
killed already by the translation exclusion (T), an instance of (5.3) at centre distance exactly
one, which they escape only because their `(P3)` is restricted to distances `<= d_0` (§4c). Three
errata, one formula-reading warning, one confirmation and two supersession notes follow (§5).
Nothing here contradicts the *statements* `REPORT.md` marks as theorems; one number in it is wrong
(§6's decomposition) and several scopes need narrowing.

Everything below is exact integer or exact algebraic arithmetic. Reproduction commands are in §7.

---

## 1. Theorem R: the single-centre orbit system at `k = 6` is a two-constraint system

Setup: `c` a weak measurable 6-colouring, `x` a typical centre with `c(x) = i` whose transition
graph `Gamma_x` contains a simple cycle `C` on `ell` labels, `V = V(C)`, `R` rotation by `kappa = pi/3`.
`P_x` is the maximal palette of Definition 5.1, measured up to angular null sets; `P_j = P_x(R^j e)`
for `j in Z/6Z`.

The necessary conditions that the sprint uses (`sprint/k6/STRUCTURE.md`, Theorem 5, items 1-7):

| tag | statement | source |
|---|---|---|
| (SA) | `i notin P_j` | self-avoidance (Lemma 1 there) |
| (PB) | `1 <= \|P_j\| <= 3` | palette bound, `results/K6-BARRIER.md` §1 |
| (T) | `P_j cap P_{j+1} = empty` | (5.7) of the paper |
| (EDG) | `P_j` is not contained in a cycle edge `{v,v+1}` | Lemma 6.2, (6.2) |
| (SIN) | `\|P_j\| = 1 => ` its label is outside `V` | Lemma 3 there (Lemma 6.2) |
| (SA2) | `\|P_j\| = 3 => \|P_{j+1}\| <= 2` | Lemma 2 there |
| (C1) | no two `P_j, P_l` are complementary 3-sets | (5.2), non-coverage |
| (C2) | at most three of the six are ternary | m11 density bound |
| (MON) | `\|P_j\|+\|P_{j+2}\| = 5` and disjoint is impossible | unit-sum lemma there |

**Theorem R.** Let `A` be the *alphabet*
```
A = { P : nonempty, P subset [6] \ {i}, |P| <= 3, P not contained in any {v, v+1}, v in Z/ell } .
```
For every 6-tuple `(P_0,...,P_5)` in `A^6`, the tuple satisfies (SA), (PB), (T), (EDG), (SIN),
(SA2), (C1), (C2), (MON) **iff** it satisfies (T). Consequently the orbit tables are exactly the
closed 6-walk counts `tr(A^6)` of the disjointness matrix of `A`.

*Proof.* (SA), (PB), (EDG) are built into `A`; (T) is the hypothesis. The remaining five are
consequences.

* (SIN). If `|P_j| = 1`, `P_j = {b}` with `b != i`. Every `b in V` lies in a cycle edge
  (`{b, b+1}` or `{b-1, b}`), so `{b}` would be contained in one, contradicting (EDG). Hence
  `b notin V`. (This is why the `ell = 6` row has no singletons: `V = [6]`.)
* (SA2). Put `Q = P_j` with `|Q| = 3`. By (T), `P_{j+1} cap Q = empty`, and by (SA) `i notin P_{j+1}`;
  hence `P_{j+1} subset [6] \ (Q union {i})`, a 2-element set, so `|P_{j+1}| <= 2`.
* (C1). If `P_j, P_l` are 3-sets with empty intersection, their union is `[6]`, which contains `i`,
  contradicting (SA) for both.
* (C2). By (SA2) applied at `j-1` and at `j`, a ternary position has no ternary neighbour. A subset
  of `Z/6Z` with no two adjacent elements has at most 3 elements.
* (MON). Suppose `P_j = Q`, `P_{j+2} = S` are disjoint with `|Q|+|S| = 5`. Both avoid `i` and lie in
  the 5-element set `[6]\{i}`, so `Q union S = [6]\{i}`. Then
  `P_{j+1} subset [6]\(P_j union {i}) = [6]\(Q union {i}) = S`, using (T) and (SA); but
  `P_{j+1} cap S = P_{j+1} cap P_{j+2} = empty` by (T). So `P_{j+1} = empty`, contradicting
  nonemptiness. `square`

So the sprint's list contains **no** information beyond (PB), (EDG), (SA), (T). Note that (MON) is
implied *because* of the rigidity chain that a ternary palette forces: `|P_j| = 3` forces
`P_{j+1} = [6]\(P_j union {i})` and then `P_{j+2} subset P_j`. (Those two facts are also worth
recording; they follow from (T)+(SA)+nonemptiness and were used by the sprint only as (SA2).)

**Corollary R1 (alphabet size).** With `delta = 0` if `i in V` and `delta = 1` otherwise,
```
|A| = (k - ell - delta) + ( C(k-1,2) - (ell - 2 + 2 delta) ) + sum_{r=3}^{k-3} C(k-1,r),
```
which at `k = 6` is `28 - 2 ell` for `i in V` and `25 - 2 ell` for `i notin V`: the values
22, 20, 18, 16 and 19, 17, 15 recorded by the sprint.

**Corollary R2 (the counts).** The four rows are

| `ell` | centre colour | `\|A\|` | words |
|---|---|---|---|
| 3 | in the cycle | 22 | 70194 |
| 3 | outside | 19 | 11888 |
| 4 | in the cycle | 20 | 18746 |
| 4 | outside | 17 | 2164 |
| 5 | in the cycle | 18 | 3720 |
| 5 | outside | 15 | 380 |
| 6 | in the cycle | 16 | 510 |

reproduced here by three procedures that share no code with `sprint/k6/orbit_correct.py`
(see §2). Every value equals `tr(A^6)`.

**Consequence for the sprint's conclusion.** `REPORT.md` §6 says "the single-centre constraints do
not decide any cycle length: the cross-centre structure is essential". Theorem R upgrades that
from an observation about a particular list to a statement about the *whole* single-centre layer:
the layer's content is (PB)+(EDG)+(T), and no strengthening of the listed constraints can change
any count, because each of them is already a theorem. In particular the remark "the (C1) and
monochromatic-sum filters cut nothing" is not an accident of the `ell` range: *all five* extra
groups cut nothing, provably.

---

## 1b. Calibration: the same system reproduces the paper's `k = 5` triangle conclusion, and pinpoints the `k = 6` degradation

Theorem R is a statement about `k = 6`, but the alphabet plus (T) is the same object at any `k`
(with the palette bound `k-3`). Running it at `k = 5` for a triangle (`ell = 3`) gives:

| `k` | centre colour | `\|A\|` | words | does every palette meet the outsiders? |
|---|---|---|---|---|
| 5 | in the triangle | 7 | 398 | **yes**, and the outsiders are a *pair* `{3,4}` |
| 5 | outside the triangle | 4 | **0** | yes, vacuously |
| 6 | in the triangle | 22 | 70194 | yes, but the outsiders are a *triple* `{3,4,5}` |
| 6 | outside the triangle | 19 | 11888 | **no**: the triangle triple `{0,1,2}` is admissible |

Three readings:

* At `k = 5` with `c(x)` a triangle label, every admissible palette meets the outside **pair**
  `{3,4}`, so by (5.7) the centre is binary for `{3,4}` almost everywhere and Lemma 5.5 gives
  local finiteness of the triangle locus — this is exactly the paper's `§6.3` triangle case, and
  it comes out of the alphabet alone (no (MON), no (C1), no (C2)).
* At `k = 5` with `c(x)` outside the triangle, `|A| = 4` and `tr(A^6) = 0`: the four palettes
  `{4}, {0,4}, {1,4}, {2,4}` are pairwise *non*-disjoint, so no 6-tuple can satisfy (T). The
  single-centre system already refutes this case outright, consistently with the paper.
* At `k = 6` the degradation is carried by exactly one palette: with `c(x)` outside the triangle,
  the set `{0,1,2}` (the whole triangle) is admissible, because a 3-set is contained in no cycle
  edge; with `c(x)` inside the triangle the palettes do meet the outsider set, but that set now has
  three elements, so "meets it" no longer means "binary". This is the same
  `k - 3`-versus-`2` threshold that `REPORT.md` §3b and `results/K6-BARRIER.md` record, now visible
  as a property of one 3-set.

---

## 2. Independent re-derivation of the four rows (decided finite computation)

`certify_orbit.py` implements three procedures in exact integer arithmetic:

* **(A)** depth-first search over the alphabet with the sprint's full list (and, separately, with
  the reduced list of Theorem R);
* **(B)** brute force over the entire tuple space `|A|^6` (numpy, no pruning), run for every row
  with `|A|^6 <= 4*10^8`;
* **(C)** the transfer-matrix count `tr(A^6)` computed by explicit integer matrix products.

All three agree on every row, and (A)-reduced equals (A)-full, which is the numerical content of
Theorem R:

```
row         |A|  DFS(full)  DFS(reduced)  tr(A^6)     brute  sprint
3in          22      70194         70194    70194     70194   70194   OK
3out         19      11888         11888    11888     11888   11888   OK
4in          20      18746         18746    18746     18746   18746   OK
4out         17       2164          2164     2164      2164    2164   OK
5in          18       3720          3720     3720      3720    3720   OK
5out         15        380           380      380       380     380   OK
6in          16        510           510      510       510     510   OK
```

A per-constraint ablation, reproduced by `certify_orbit.py` (DFS, one group dropped at a
time; `size<=2` *tightens* (PB) to `|P| <= 2` rather than dropping it):

```
drop         3in    3out     4in    4out     5in    5out     6in
none       70194   11888   18746    2164    3720     380     510
EDG       446960  446960  446960  446960  446960  446960  446960
SIN        70194   11888   18746    2164    3720     380     510
C1         70194   11888   18746    2164    3720     380     510
C2         70194   11888   18746    2164    3720     380     510
MON        70194   11888   18746    2164    3720     380     510
SA2        70194   11888   18746    2164    3720     380     510
size<=2    26706    2600    5358     362     800     100     150
```

Exactly three things are load-bearing: the alphabet's edge condition (EDG) — without it the
alphabet is all 25 nonempty subsets of size at most 3 of `[6]\{i}`, the cycle length stops
mattering, and every row becomes 446960 — the palette bound (tightening it to `|P| <= 2` gives the
all-pairs counts 150 at `ell = 6`), and (T). The five remaining groups move no count at all, which
is Theorem R.


---

## 3. The paper's final geometric certificate (Lemma 8.9) verified exactly

`certify_8_9.py` recomputes, in `Q(sqrt 3, sqrt 11)`, everything the paper's last step needs.

* The Moser coordinates (8.5) are correct: all ten drawn edges of `G` have squared length exactly
  `1`, and the contradicted edge `T--uT` satisfies `|T - uT|^2 = 3 |1-u|^2 = 1`.
* The multiplier of (8.6) has `|35+12i|^2 = 37^2`, so it is a rotation.
* **All seven vertices `z_g` satisfy `0 < |z_g|^2 < 4` and the inequality (8.4)**, exactly, with
  the exact margins

| `g` | `|z_g|^2` | `P` (8.4 left) | `P'` (8.4 right) | `P' - P` |
|---|---|---|---|---|
| 0 | 1.70082 | 0.866124 | 1.38897 | 0.522848 |
| A | 1.28764 | 0.0895503 | 0.119773 | 0.0302224 |
| B | 0.09564 | 1.68999e-06 | 0.00069832 | 0.00069663 |
| T | 0.68246 | 0.0221255 | 0.0265819 | 0.00445644 |
| uA | 2.73501 | 9.72524 | 19.4763 | 9.75105 |
| uB | 0.45925 | 0.00199268 | 0.025071 | 0.0230783 |
| uT | 2.49344 | 12.5744 | 13.0226 | 0.448211 |

  (decimals of exact rationals in `Q(sqrt3, sqrt11, sqrt33)`; every sign above is decided by
  `sympy.sign` on an exact algebraic number, not by floating point).
* Every entry of Table 1 of the paper is correct as an upper bound `P < P+` and a lower bound
  `P-' < P'`, in all seven rows. Table 1's coordinates agree with the exact `z_g` to the stated
  `h = 0.00011`.
* The two identities that the proof of Lemma 8.8 uses are correct:
  `sin^2(3 phi) = ups^2 (3 xi^2 - ups^2)^2 / l^3` and `sin(3 delta) = sqrt(1-l/4) (l-1)`, so
  (8.4) is exactly `sin^2(3 phi) < sin^2(3 delta)`, i.e. the two endpoint directions of the
  decomposition of `z` carry opposite outsider signs.

**Warning on reading (8.6).** The displayed placement has two readings that are both consistent
with the sentence "this is a rotation followed by a translation":
```
 (i) composed :  z_g = ROT * (g + TR)          ROT = (35+12i)/37,  TR = (-290+149i)/250
 (ii) affine  :  z_g = ROT * g + TR
```
Under (i) all seven vertices satisfy the certificate and the coordinates match Table 1.
Under (ii) the coordinates are `(-1.16, 0.596)` for `g = 0` instead of `(-1.2906, 0.1876)`, and
the certificate **fails** at three of the seven vertices (`0`, `uB`, `uT`). So (i) is the intended
formula and Table 1 disambiguates it; but any formalisation of §8.5 must use (i). This is the one
place where I nearly introduced an error by trusting a text extraction.

---

## 4. The constant `alpha` in §7: exact admissible range

`REPORT.md` §2 asserts that `§7` transfers at `k = 6` with "the only changes ... `alpha < 1/6`,
`G = K_6`, `ell <= k`". The `alpha` claim is correct and is exactly optimal. Here is the audit.

The map (7.4) is `q_i^eps(z) = (p_i^eps(z) - alpha)_+ / sum_{l in I} (p_l^eps(z) - alpha)_+`.
The construction needs the denominator to be positive at every `z`. The only information available
is `p^eps(z) >= 0`, `sum_l p_l^eps(z) = 1`, hence
```
 sum_l (p_l^eps(z) - alpha)_+  >=  sum_l p_l^eps(z) - k alpha  =  1 - k alpha ,
```
which is positive exactly when `alpha < 1/k`. So `alpha < 1/6` at `k = 6` and `alpha < 1/5` at
`k = 5` (which is what the paper fixes). Conversely `alpha >= 1/k` gives nothing: the bound is
`<= 0`, and the uniform vector `p = (1/k, ..., 1/k)` — which satisfies the paper's only constraint
on `p^eps`, namely (7.2) `p_i(q) + p_i(z) <= 1` for `|q-z| = 1`, with equality — makes every
`(p_l - alpha)_+` vanish. So `1/k` is the exact threshold of the printed construction and cannot
be improved.

Every other occurrence of `alpha` in §7 is monotone in the harmless direction or `alpha`-free, so
nothing else constrains the constant:
* `q_i^eps(z) > 0` iff `p_i^eps(z) > alpha` (any `alpha > 0`);
* Lemma 7.3's violation set `{p_i > alpha, p_j > alpha}` and its grid `c_alpha eps` (any `alpha > 0`);
* Lemma 7.4(2), the "clique in a forest" step (label-blind, `k`-free);
* Lemma 7.6: `p_i^{eps_n}(a_n) > alpha` plus (7.2) gives `p_i^{eps_n}(z) <= 1 - alpha` (any
  `alpha in (0,1)`);
* (7.7): `alpha |A_i cap U| <= ||p_i - a_i||_{L^1(U)} + alpha |E_n cap U|` (any `alpha > 0`).

I also re-derived (7.7) line by line, because the printed display is easy to mis-derive: on
`U \ E_n` one has `p_i^eps <= 1 - alpha`, so
`alpha 1_{A_i}(z) - (a_i(z) - p_i^eps(z))` equals `alpha - 1 + p_i^eps(z) <= 0` on `A_i` and
`p_i^eps(z) >= 0` off `A_i`; integrating gives the display. It is correct.

The `k`-independence of the rest of §7 (Lemma 7.2, 7.4, 7.5, 7.7, 7.8 use only (7.2), the
clique-in-a-forest fact for an arbitrary finite graph, and topology on `K_k`) is confirmed:
the only place the number `5` occurs is `G = K_5` and "the five probabilities sum to one", both of
which are `k` in general.

---

## 4b. The cover-obstruction constant: "side ten" is not sharp (partly anticipated by d2)

The paper's Lemma 7.5 states: *a closed square of side ten has no relatively open cover of
multiplicity at most two and mesh at most two.* Its proof uses only three properties: convexity of
`Q`, `diam U <= mesh` for the members, and the existence of a point `y in Q` with
`dist(y, partial Q) > mesh`. So the lemma is about the inradius, and it sharpens to:

**Lemma 7.5'.** Let `Q ⊂ R^2` be compact and convex with nonempty interior and let `m > 0`. If
`{y in Q : dist(y, partial Q) > m}` has nonempty interior, then `Q` admits no relatively open cover
of multiplicity at most 2 and mesh at most `m`. In particular (i) a closed square of side `> 2m`;
(ii) a closed disk of radius `> m`; (iii) with the paper's `m = 2`, side `> 4` instead of ten.

*Proof.* The paper's, verbatim, with `2` replaced by `m`: finite subcover, `z_a in U_a`, partition
of unity `phi_a` (well defined since `diam U_a <= m < ` inradius); `F(z) = sum_a phi_a(z) z_a`
satisfies `F(Q) ⊂ Q` by convexity, `|F(z) - z| <= m`, and at most two weights are positive so
`F(Q)` lies in a finite union of segments; and for `y` with `dist(y, partial Q) > m` the continuous
map `z |-> y + z - F(z)` maps `Q` into itself, so Brouwer gives `F(z) = y`. A finite union of
segments does not contain a set with nonempty interior. `square`

**Attribution.** The sharp threshold "inradius `> mesh`", together with the (correct) sharpness
statement that "inradius `>= mesh`" cannot replace it, is `.ultramath/smwfwi7rh/m5` finding f7(1)
(direction d2), which I read after deriving it; I agree with it and the derivation above is an
independent re-derivation of the same statement. What I add here is only the following
consequence, which fixes why the ball form of `(W)` is not exchangeable for the square form of
`(F)`:

* `REPORT.md` Theorem A (`(W)` with `R > 1`) needs the **disk** form (ii), and no square-shaped
  version of the cover lemma can replace it. A closed disk of radius `R' in (1, sqrt 2)` contains
  no closed square of side `2`, so inside the ball of `(W)` there is no square to which a
  square-shaped lemma applies. This is the precise reason why the disk version of the cover lemma
  (m12) is *necessary*, and why `sqrt 2` is not the relevant threshold for `(W)` — a point
  `WEAKEST.md` raises and d2's f7(1) settles from the other side.
* `REPORT.md` Theorem B (m5: `L` meets every closed square of side `> 2`) runs Lemma 7.6's mesh
  bound `1 + o(1)` with `m_n = mesh_n` and `Q` of side `> 2`; this is consistent with Lemma 7.5'
  and sharp, because Lemma 7.6's proof stops exactly when one component of `U_{n,i}` holds two
  points at distance `> 1`, and `1` is the unit distance of (7.2).

---

## 4c. The palette-level countermodels are killed by (5.3) at centre distance exactly one

This is the single most important correction to the record, and it is **d18's**
(`.ultramath/smwfwi7rh/m1/note.md` §4, finding f24); I re-derived it independently while auditing
`REPORT.md` §5 and I confirm it. It is recorded here because `REPORT.md` §5's frontier statement
is superseded by it.

Remark 5.3 of the paper permits, in Lemma 5.2(3), the representation
`(x+a) + f = x + f + a` for every **unit** direction `a` and every `f != ±a`, with
`s(f) = f` (the identity, a local diffeomorphism of the angular coordinate) and `t(f) = a`
(constant, as the remark explicitly allows). Both are unit and nonparallel. Hence every palette
field of a weak measurable `k`-colouring satisfies, for every fixed centre `x` and every fixed unit
vector `a`,

```
(T)   P_{x+a}(f) cap P_x(f) = empty      for a.e. direction f.
```

This is an instance of (5.3) at centre distance **exactly 1**. It is *not* an instance of the
`(P3)` used in `REPORT.md` Theorem C, which is restricted to `|z - z'| <= d_0 = pi/(9m)`, and not of
the `m13` model's form, which is restricted to distances `<= 1/50`. So:

* Every countermodel in the record (`m13`'s singleton field `{4+s(t)}`, `m15`'s block fields for
  `ell = 3,4,5,6`, the `FREE-LABEL` words, `uniform_nogo`) is space-translation-invariant, hence
  has `P_{x+a}(f) = P_x(f)`, and (T) forces `P_x(f) = empty` a.e. — contradicting nonemptiness.
  They fail (T) at **every** direction and every unit step, not merely at one point.
* Therefore `REPORT.md` §5's "the only constraint it fails is **trace-consistency** with a proper
  colouring" is superseded: the countermodels fail `(T)`, a two-line consequence of Lemma 5.2(3)
  that needs nothing but two centres at distance one. The same applies to §4's sentence "No proof
  of any case of Theorem 6.5 ... can use only the palette-level hypotheses at `k = 6`": the
  hypotheses of Theorem C are strictly weaker than the palette-level hypotheses, which include
  (T).
* Consequently no space-translation-invariant palette field is admissible at all, and any open
  stratum must be genuinely `x`-dependent. Precisely: a singleton-valued palette field satisfying
  (T) is a measurable proper 6-colouring of the plane in each direction `f`, so the existence of
  such a field is *equivalent* to `chi_m(R^2) <= 6` (one admissible direction suffices; conversely
  a measurable 6-colouring gives the field `sigma(x,f) = c(x)`). The stratum that is not reducible
  to that problem in this way is the six-cycle stratum, where `V = [6]` forces every palette to have
  size at least 2. This matches `REPORT.md` §5's conclusion about which stratum is open, but for a
  different and much cheaper reason.

(T) is a *two-centre* constraint and is invisible to every single-centre enumeration, so none of
§1, §1b, §2 above is affected by it.

**How the omission happened (audit point).** (T) is not a new observation: Remark 5.3 of the paper
says in so many words *"the second endpoint map `t` may be constant ... In particular, for any fixed
direction `a`, the representation `(x+a) + f = x + f + a` is admissible off `f = ± a`"*. The
transcription of Lemma 5.2(3) into `REPORT.md` Theorem C's `(P3)` kept the general shape
`s + t = (z' - z) + w` but bounded the centre distance by `d_0`, which silently discards exactly the
case `|z' - z| = 1` that Remark 5.3 singles out. Every subsequent countermodel inherited the
restriction. So the frontier recorded in `REPORT.md` §4-§5 is not wrong about the weaker system it
describes; it is a statement about a system whose axiom list is missing one line of the paper.


---

## 5. Errata

**E1 (`REPORT.md` §6, quantitative, arithmetic error).** The text reads

> At `ell = 6` there is no singleton, the all-pairs stratum has 150 words, the 2-periodic
> `(3,2,3,2,3,2)` pattern has 6, and 354 words have one or two ternary palettes.

The exact counts (by number of ternary palettes in the word) are
```
0 ternary : 150        1 ternary : 240        2 ternary : 108        3 ternary : 12
```
total 510. So "354" should be **348**, and the 12 words with three ternary palettes are 6 of
pattern `(3,2,3,2,3,2)` and 6 of pattern `(2,3,2,3,2,3)`. The quoted total 510 is right
(150 + 6 + 354 = 150 + 348 + 12 = 510), so the slip is only in the split. Check:
`python3 certify_orbit.py` prints the four numbers.

**E2 (`sprint/k6/STRUCTURE.md`, Theorem 5, item 7 — incomplete justification, statement true).**
Item 7 reads "at most three of the six are ternary (the orbit bound (C2),
`sigma({|P| = 3}) <= pi`)". The measure statement is a statement about *all* directions, and its
consequence for *one* orbit is not immediate: writing `f(t) = #{j : |P_x(Re^{i(t+j kappa)})| = 3}`
one only gets `int_0^kappa f <= 3 kappa`, hence `f <= 3` on a set of positive measure of `t`, not
at every `t`. The correct deduction is the one the sprint actually needs and uses: since the
`t` with `f(t) <= 3` have positive measure while all the almost-everywhere constraints hold for
almost every `t`, some `t` satisfies both. With that reading the item is true. (In any case
(C2) is implied by (SA2) by Theorem R, so no count depends on it.)

**E3 (`REPORT.md` §6, scope of a remark — true, and stronger than stated).** "The `(C1)` and
monochromatic-sum filters cut nothing on the transition-admissible stratum" is a theorem, not an
accident: by Theorem R *every* group beyond `(PB)`, `(EDG)`, `(SA)`, `(T)` cuts nothing, at every
`ell in {3,4,5,6}`, and (SIN) is itself implied by (EDG) (`STRUCTURE.md` Corollary 4 is therefore
not needed for the `ell = 6` computation; the underlying Lemma 3 is still needed elsewhere, e.g.
`m7`'s four-cycle state reduction).

**E4 (paper (8.6), reading warning — see §3).** Not an error in the paper, but an ambiguity a
formalisation can fall into; Table 1 selects the composed reading.

**E5 (confirmation, no change).** `results/K6-BARRIER.md` §1's general-`k` palette bound
`1 <= |P_x(e)| <= k-3` is correct as printed: it is the paper's proof of Proposition 5.6 with a
`(k-2)`-element set `A`, whose complement has exactly two elements, so that the centre `x + e` is
binary for a fixed pair and Lemma 5.5 (uniform separation of binary centres) applies. At `k = 6`
this gives `|P_x(e)| <= 3` at *every* centre, which is the input every `k = 6` computation in the
sprint assumes. I re-derived it independently and I agree. (d18's Theorem A is the same argument,
and its Theorem B isolates correctly that the missing step to `|P| <= 2` is a *separation theorem
for T-hitting centres with `|T| = 3`*, which does not follow from the printed technology.)

**E6 (`REPORT.md` §4 and §5, frontier statement — superseded, see §4c).** §5 says of the palette
countermodels "the only constraint it fails is trace-consistency with a proper colouring", and §4
concludes "no proof of any case of Theorem 6.5 can use only the palette-level hypotheses at
`k = 6`". Both are superseded by (T): the countermodels fail the translation exclusion, which is
an instance of (5.3) at centre distance exactly one and therefore *is* a palette-level hypothesis.
The `(P1)-(P6)` lists of Theorem C and the `(P3)` of the countermodel verifiers are restricted to
`|z - z'| <= d_0` (or `<= 1/50`) and simply do not reach distance one. Discovery: d18 /
`.ultramath/smwfwi7rh/m1/note.md` §4; independently re-derived and confirmed here.

**E7 (`REPORT.md` §4b (Theorem C') and §4, scope note).** §4b's table "`STRIP(k,ell)` is UNSAT
exactly for `(k,ell) = (4,3), (4,4), (5,5)`" and §4's "the palette-level route is dead for every
cycle length" are statements about systems that do not contain (T). By E6 they must be read as
statements about that weaker system; they do not by themselves exclude any cycle length at `k = 6`
for a genuine colouring. `REPORT.md` §5 already says "a proof of `(W)` from palette-level data is
impossible (Theorem C)" — that clause is what E6 withdraws.


---

## 6. What I did **not** check

* §2-§4 of the paper (the spectral rigidity Theorem 2.3 and the transfer Theorem 1.3). These are
  large and are the least self-contained part; they are untouched by the `k = 6` question and I
  did not audit them. `REPORT.md` does not rely on them beyond citing Theorem 1.3.
* `m3`'s proper 7-colouring with a non-locally-finite `L` (the `k >= 7` row of the phase table).
  I read its description in `REPORT.md` §3b and `sprint/k6/PHASE-TRANSITION.md` but did not
  independently re-run its `Q(sqrt3)` annulus certificate; that object is `m16`'s direction `d4`,
  and duplicating it is not useful. The row "`k >= 7` false" therefore remains single-sourced in
  my reading.
* `m16`'s Theorem A, `m7`'s `k`-general Lemma 6.4, `m4`'s label merging, `m1`'s `2^15`
  classification, `m14`'s neutrality, `m11`'s Lean files: read, not re-computed. The two `m14`
  steps I did re-derive by hand — the "shrink to `|P| <= 2`" step and Theorem A(iii) — are
  correct as stated in `.ultramath/smwfo9zkl/m14/REPORT.md`.
* Of this sprint's own work I read and cross-checked two accepted findings that my audit touches:
  d2 / `.ultramath/smwfwi7rh/m5` f7(1) (the sharp inradius threshold; I re-derived it
  independently and agree, see §4b) and d18 / `.ultramath/smwfwi7rh/m1` f24 ((T); re-derived
  independently and agree, see §4c). I did **not** re-run `m5`'s `verify.py` or `m1`'s `cert*.py`.
  `m1`'s further claim f22 — that even granting `|P| <= 2` the printed §6.3 four-cycle machinery
  cannot be repaired at `k = 6` — I read but did not re-run; it is consistent with my §1b
  calibration (at `k = 6` the obstruction is a 3-element outsider set, not a 2-element one).

* **The Lean check of §2 did not run.** `k6_orbit_count.lean` in this directory states
  `tr(A^6) = 510` for the `ell = 6` alphabet with an explicit 16x16 matrix and a kernel `decide`,
  but on this VM `import Mathlib` alone did not finish within 5 minutes (4 cores, ~11 GB of 15
  already in use by the other members' processes), and a 20-minute attempt also timed out. The
  file is therefore **unchecked** and must not be cited as machine-checked until someone runs
  `lean k6_orbit_count.lean` on an idle machine. The numbers it encodes are certified three other
  ways by `certify_orbit.py`.

---

## 7. Reproduction

```
cd .ultramath/smwfwi7rh/m2
python3 certify_orbit.py     # Theorem R + the four rows (3 procedures) + the ablation (~75 s)
python3 certify_8_9.py       # Lemma 8.9, Table 1, both readings of (8.6) (~6 s)
python3 calibrate_k5.py      # section 1b: the k=5 calibration (< 1 s)
```

`certify_orbit.py` prints the three-way agreement table and the ablation table of §2. The
brute-force procedure allocates `6 * |A|^6` bytes, so it runs for every row above (the largest is
`22^6 = 1.1 * 10^8`); no row is skipped.

Paper extract used for the formula audit: `pdftotext -layout` of
`attachments/here-are-three-files-ni5n/paper.pdf`. I could not view rendered page images from this
session, so every displayed formula was instead checked by (i) re-deriving the identity
symbolically, and (ii) recomputing its numerical content exactly — which is what caught
the (8.6) ambiguity in §3.
