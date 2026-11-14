# The six-cycle free-label case at $k=6$: exact dictionary, triple-free model, exact delimiter

Member `m3`, direction `d4` (geometry / realisability audit). Files: `dictionary.py`,
`word.py`, `symbolic_proof.py`, `certificates/cert_m_le_4.json`.
Nothing outside this directory was modified.

---

## 0. Results

**R1 (dictionary, exact).** For a palette field that depends only on the direction
(`P_z(e) = W(sector(arg e))`, `n = 6m` sectors of width `Delta = 2*pi/(6m) = pi/(3m)`),
the paper's (5.3) *for every pair of centres with `|z-z'| <= d0 = pi/(9m)`* and (5.7)
hold **iff**

  `W(i) ∩ W(i+delta) = ∅` for every `i ∈ Z_{6m}` and every
  `delta ∈ {±(m-1), ±m, ±(m+1)}` mod `6m`.                                   (C)

The free-label hypotheses on top of (C) are exactly: `W(i)` an admissible `C_6` palette
and `0 ∉ W(i)`.

*Both* directions of the dictionary are certified: no other sector shift can occur
(D1, D2), and each of the six offsets really occurs, on an open set of configurations
(D3). The record proves the first direction (`m15`'s Lemma G: deviation `<= 1.6 d0` for
`m >= 6`) and checks the block-shift property of the three-block constructions; what is
missing there is the second direction, and without it a no-go proved from the word
system would be vacuous — the geometry could force strictly fewer constraints than the
word system imposes. `dictionary.py` — all checks pass.

**R2 (the word, for every $m\ge5$, triple-free).** The `2m`-periodic word

  `A^{m-3} B^2 C^{m-3} D^2 E^2`,  repeated 3 times on `Z_{6m}`, with
  `A={1,3}`, `B={1,4}`, `C={2,4}`, `D={2,5}`, `E={3,5}`

satisfies (A),(B),(C) for **every** `m ≥ 5`. Verified exactly for `m = 5..1500` and
proved by a machine-checked symbolic argument (all comparisons are linear inequalities
in `m`) for every `m ≥ 6`; `m = 5` is checked directly. Example, `m = 6` (`n = 36`):

```
{1,3}{1,3}{1,3} {1,4}{1,4} {2,4}{2,4}{2,4} {2,5}{2,5} {3,5}{3,5}   (x3)
```

This replaces the 36-sector witness of `sprint/k6/six_free_witness.json`, which uses the
triple `{2,4,5}` and therefore violates m2's bound `|P_x(e)|+|P_y(e)| ≤ 5` in a
translation-invariant field (`2·3 = 6 > 5`). The new word uses only pairs, so
`2+2 = 4 ≤ 5`: **m2 is satisfied**, and m11 is vacuous (no ternary palette). The
free-label model is therefore *not* killed by the two-centre palette bound.

**R3 (exact class).** The system is satisfiable **iff `m ≥ 5`**, for the pairs-only
domain and for the pairs+triples domain alike. `m = 1,2,3,4` are UNSAT, certified by
three procedures (complete forward DFS, complete reverse DFS, Cadical) plus a
replayable search-tree certificate; `m = 1,2,3` also have a one-line hand proof
(a triangle in the constraint graph).

**R4 (countermodel + delimiter).** For every `m ≥ 5` the field above is a
translation-invariant palette field with every palette an admissible `C_6` palette of
size 2, free label `0`, satisfying (6.2), (5.7), (5.3) exactly, and the trace condition
(P5) for every cycle edge at *every* point of the plane; the cyclic centres include the
distinct points `y_k = (d0/3) 2^{-k} (3/5,4/5)` accumulating at `0`. It is **not** the
palette field of any weak measurable 6-colouring: the only label absent from the field
is `0`, so by self-avoidance (Lemma D) every typical point would carry colour `0`,
contradicting Lemma 4.3. That is the exact delimiter — see §5.

---

## 1. Why the six offsets and nothing else (the dictionary)

Fix `m`, `Delta = pi/(3m)`, `d0 = pi/(9m)`. Let `z, x` be centres with `a = z-x`,
`d = |a| <= d0`, and `f` a unit direction. The representation of Lemma 5.2(3) is
`z + f = x + s + t`, i.e. `s + t = f + a` with `|s| = |t| = 1`. Put
`rho = |f + a| ∈ [1-d, 1+d]`; then

  `s = (f+a)/2 ± h`,  `h ⟂ (f+a)`,  `|h| = sqrt(1 - rho²/4)`,
  `arg s = arg(f+a) ± phi`,  `phi = arccos(rho/2)`,
  `arg(f+a) = arg f + psi`.

With `rho^2 = 1 + 2 d cos(theta) + d^2` (`theta` the angle between `f` and `a`), the
law of sines `sin psi = d sin(theta)/rho` and `|phi - pi/3| = |∫_1^rho du/sqrt(4-u²)|`
give, using `|rho - 1| <= d|cos(theta)| + d^2/2` and `4 - (1+d)^2 > 25/9`,

  `dev <= c1 |sin(theta)| + c2 |cos(theta)| + c3 <= sqrt(c1² + c2²) + c3`,
  `c1 = (d/(1-d))(1 + (d/(1-d))²)`,  `c2 = (3/5) d`,  `c3 = (3/10) d²`,

and therefore, for `d <= d0` and every `m >= 5`,

  `dev <= 1.2574 d`,   `dev/Delta <= 0.4191 < 1`.                           (D1)

The sharp constant is `sup_theta (|sin theta| + |cos theta|/sqrt 3) = 2/sqrt 3 = 1.1547`,
so the certified one is within 9% of sharp. `dictionary.py` certifies (D1) with
`Fraction` arithmetic, a 31-digit rational enclosure of `pi` and an exact integer
square root; no floating point decides anything. Since `B(d)/d` is increasing in `d`
and `d0` decreases in `m`, the worst case is `m = 5`.

Two remarks. (i) The record's version — `m15`'s Lemma G, `|arg s_pm - (theta +- pi/3)| <= 1.6 d0`
for `d0 <= pi/54`, proved by exact rationals in `.ultramath/smwfo9zkl/m15/verify.py` — is
*valid* (its mean-value bound on `g(r) = atan(sqrt(4-r²)/r)` over `r ∈ [1-d0, 1+d0]`
needs no case split); I withdraw any reading of it as needing `rho >= 1`. (ii) It is
loose because it adds the two terms as if independent, and it is stated for `m >= 6`
(`d0 <= pi/54`); the certificate here is sharper (`1.2574` vs `1.6`) and covers `m >= 5`.
Either way the conclusion is the same: a factor `> 2` of slack against `Delta`.

Consequently `arg s = arg f + pi/3 + dev` with `|dev| < Delta`, so

  `sector(arg s) = sector(arg f) + m + k`,  `k ∈ {-1,0,+1}`                 (D2)

(`pi/3 = m·Delta`), giving the six offsets `±(m-1), ±m, ±(m+1)` once both branches and
both orders of the two centres are used. The second branch is legitimate: applying
(5.3) with the centres exchanged needs `t` to be a local diffeomorphism in the angular
coordinate, which is verified (`d arg t/d arg g ∈ [0.93,1.07]`), as is `s`
(`d arg s/d arg f ∈ [0.93,1.01]`), and `s, t` are nonparallel (angle `>= 2.02`). (D4)

*Attainment* (D3). It is not enough that no other shift is possible; each of the six
must be realised, or the word system would be an over-strengthening and a no-go from it
would prove nothing. Explicit configurations at `d = d0`, `m = 6`, with both sector
indices at least `0.18` sectors from a boundary (so an open set of configurations
works):

| offset | `arg f` | `arg(z-x)` | branch |
|---|---|---|---|
| `+5` | 4.57058 | 3.30740 | `+` |
| `+6` | 4.80184 | 2.15548 | `+` |
| `+7` | 2.93433 | 4.80838 | `+` |
| `-5` | 4.57058 | 2.19039 | `-` |
| `-6` | 4.80184 | 1.16937 | `-` |
| `-7` | 2.93433 | 3.83100 | `-` |

A dense sweep over `(f, a)` for `m = 3,5,6,9,12,15,18` reproduces exactly the six
offsets and nothing else. Combined with (D2), the word system is *equivalent* to
(5.3)+(5.7) for such a field. The case `a = 0` (`d = 0`) is allowed by (5.3)
("possibly `z = x`") and gives `s + t = f`, i.e. `arg s = arg f ± pi/3` exactly: that
is (5.7), the offset `±m`, so Corollary 5.4 is a special case.

*Accumulation* (D5). `y_k = (d0/3) 2^{-k} (3/5,4/5)`: distinct (exactly, as dyadic
multiples), `|y_k| <= d0/3`, `|y_k - y_{k+1}| = (d0/6) 2^{-k} <= d0`, so every pair of
them is inside the range where (5.3) applies, and `y_k -> 0`. Nothing in the geometry
requires `m ≡ 0 (mod 3)`: that restriction belongs to the *block* construction of
Theorem C (`L = 2m/3`), not to the transport.

## 2. The word (R2)

Disjointness on the six admissible pairs avoiding `0` is the 5-cycle
`A - C - E - B - D - A`; the word is a walk on it, with the sector-order block sequence
`A, B, C, D, E`. All comparisons are linear in `m`, so the statement is proved for all
`m >= 6` by deciding linear inequalities (`symbolic_proof.py`); here is its output:

```
A + (m-1) reaches [C]        A + (m) reaches [C,D]      A + (m+1) reaches [C,D]
B + (m-1) reaches [D]        B + (m) reaches [D,E]      B + (m+1) reaches [E]
C + (m-1) reaches [A,E]      C + (m) reaches [A,E]      C + (m+1) reaches [A]
D + (m-1) reaches [A]        D + (m) reaches [A,B]      D + (m+1) reaches [B]
E + (m-1) reaches [B]        E + (m) reaches [B,C]      E + (m+1) reaches [C]
```

Each entry is a block disjoint from the source block, so (C) holds at every sector for
every `m >= 6`. The word has period `2m`, and `2m | 6m`, so on `Z_{6m}` the offsets
reduce mod `2m` to `{m-1, m, m+1}` (because `-(m-1) = m+1` and `-m = m` mod `2m`).

## 3. The exact class (R3)

`m = 1`: the offset `0` occurs (`0 ∈ {±(m-1), ±m, ±(m+1)} mod 6`), so a palette would
have to be disjoint from itself.
`m = 2`: `1, 2, 1` all occur as offsets mod 12, so sectors `0,1,2` need three pairwise
disjoint palettes; each has size `>= 2` and there are only 5 usable labels, `6 > 5`.
`m = 3`: `2, 4, 2` occur mod 18; same triangle obstruction.
`m = 4`: no triangle; decided by complete enumeration (`1211` nodes pairs-only,
`13737` nodes pairs+triples), by Cadical on the same CNF, and by a reverse-order DFS;
the search tree is dumped to `certificates/cert_m_le_4.json` and replayed by an
independent verifier that recomputes, at every node, the exact set of locally
consistent values and checks the tree lists exactly those.
`m >= 5`: the word of §2.

## 4. Side conditions checked on the model

* (P1) `1 <= |P| <= 3`: every value has size 2 — no singleton, no triple.
* (6.2)/(P4) admissibility for `C_6`: all five values are admissible.
* non-proper self-avoidance: `0` is absent from every palette.
* **m2** (`|P_x(e)|+|P_y(e)| <= 5` at unit distance): with a translation-invariant
  field this reads `2|P| <= 5`; here `2·2 = 4 <= 5`. Satisfied. (This is exactly what
  the old triple witness failed.)
* **m11** (ternary palettes occupy at most half the circle): vacuous, no triples.
* **(P5)** trace condition: for every cycle edge `{i,i+1}` and every palette value `V`,
  `V ⊄ {i,i+1}`, so a point mass at some label of `V \ {i,i+1}` is a trace supported in
  `V` killing both edge labels; choosing that label measurably in each sector gives a
  single trace killing the edge a.e. So every edge of `C_6` has its (P5) trace at every
  point.
* (5.2) with the *constant* label function `c = 0`: `0 ∉ P_x(e) ∪ P_x(v)`, so (5.2)
  holds formally — the same phenomenon the record notes for the singleton model.
* m4/m1/m14 concern colourings or finite palette systems and are not constraints on a
  palette field; the model neither meets nor violates them.

## 5. The delimiter: precisely what the model cannot do

Let `c` be a weak measurable 6-colouring whose maximal palette field is `P`
(Definition 5.1). The field above takes the values `{1,3},{1,4},{2,4},{2,5},{3,5}`;
their union is `{1,2,3,4,5}`, so **`0` is the only label that never lies in a palette**.
At a typical (density-one) point `x`, Lemma D gives `c(x) ∉ P_x(e)` for a.e. `e`; if
`c(x) = i ∈ {1,...,5}` then `i ∈ P_x(e)` on a set of directions of positive measure,
contradiction. Hence `c(x) = 0` for a.e. `x`, so `A_0` is conull, and two typical
points at unit distance are both in `A_0` — contradicting Lemma 4.3. So:

> no weak measurable 6-colouring has this palette field, and no proper 6-colouring can
> avoid the palettes (`c ≡ 0` is the only avoiding label function, and it is not proper).

The sharpest true statement of what a proper colouring must do that the model cannot:
a proper colouring must place, at a.e. point, a label that *is* in the palette of some
direction at that point — i.e. the palette must be the *maximal* palette of a colouring
whose traces are circle-sample limits, not an abstract family. In the model, for every
point, every label except `0` occurs in the palette on a set of directions of positive
measure; that is exactly the "trace-consistency with a proper colouring" that
`FREE-LABEL.md` identifies as the only remaining constraint. The model therefore
delimits the palette-level programme exactly, at every `m >= 5`, with no triple and
within m2's bound.

## 5b. The free-label budget at $k=6$ is exactly one

The delimiter of §5 uses that exactly one label is absent from the palette field. That
is not an accident of the construction:

**Lemma (free-label budget).** Let `m >= 3` and let `W : Z_{6m} -> 2^[6]` satisfy (A)
admissibility and (C). Then `|∪_i W(i)| >= 5`, i.e. **at most one label can be free.**

*Proof.* Suppose the union lies in a 4-set `A`. For a constrained pair, `W(i)` and
`W(i+δ)` are disjoint admissible subsets of `A`; admissible sets have size 2 or 3 and
`2+3 > 4`, so both have size 2 and `W(i+δ) = A \ W(i)`, the unique such partner (if
`A \ W(i)` is not admissible the constraint already fails). Hence for every `i` and
every `δ ∈ {±(m-1), ±m, ±(m+1)}`, `W(i+δ) = A \ W(i)`. Apply this at `j = i+m-1` with
`δ' = -(m+1)`: `W(i-2) = A \ W(i+m-1) = A \ (A \ W(i)) = W(i)`. So `W` is 2-periodic.
One of `m-1, m, m+1` is even; for that even `δ` (which is an offset, hence
constrained) 2-periodicity gives `W(i+δ) = W(i)`, and a nonempty palette is not
disjoint from itself. Contradiction. ∎

Certified in `word.py` (`free_budget`): the combinatorial step for all 15 four-subsets,
the parity fact for every `m >= 3`, and the absence of 2-periodic 4-set words for
`m = 3..600`; the direct complete searches at `m = 5, 6` agree (UNSAT for all 15
four-subsets). Together with §5:

> at `k = 6`, a translation-invariant field satisfying the palette constraints and
> non-proper self-avoidance has **exactly one** free label, so its palette union has 5
> labels, so *every* label function avoiding the palettes is constant. At `k >= 7`
> this fails: `m3`'s accumulating proper colouring has a palette field whose free set
> has size 3 (`{0,2,3}` never appear in a palette at the `q_n`), which is what lets the
> colouring be proper there.

So the `k = 6` obstruction is a *budget* obstruction: one free label is enough to make
the field satisfy all palette + trace hypotheses, and not enough to colour with.

## 6. Scope — what is *not* claimed

1. The traces of the model are declared (measurable point-mass selections supported in
   `P_x(e)`), not limits of circle samples of a colouring; so "every point is a
   `C_6`-cycle point" is meant in the abstract palette + trace sense, exactly as in
   `FREE-LABEL.md`. `Gamma_x` is defined geometrically by (6.1) and is not computed
   here; (P5) is the *necessary* condition of Lemma 6.2, not a sufficient one, so what
   is proved is that the necessary conditions used in §6 are satisfiable at every point
   of the plane, with accumulation.
2. The model is stronger than the accumulation argument needs. The pairs
   `(y_k, y_{k+1})` are at distance `(d0/6)2^{-k}`, where the deviation is much smaller
   and only some of the six offsets are realisable; but a translation-invariant field
   must satisfy (5.3) for *all* centre pairs at distance `<= d0`, and that is what makes
   all six offsets binding. A minimal countermodel would have to be
   non-translation-invariant — which is the same place where the free label would have
   to vary, and where the first real obstruction might live.
3. The declared trace family is legitimate as an *abstract* family: it consists of
   measurable point-mass selections `delta_{a(e)}`, `a(e) ∈ P_x(e)`, which is closed
   under weak-* limits and independent of the centre, so (5.1) and the compactness part
   of Definition 5.1 hold. What it is not is the family of circle-sample limits of a
   colouring — that is precisely the failing item (§5).
4. The classification `m >= 5` is for this specific six-offset transport system at
   `d0 = Delta/3`; it says nothing about other transport radii.

## 7. Verification

```bash
cd .ultramath/smwfwznwk/m3
python3 dictionary.py        # D1..D5, geometric dictionary     -> ALL CHECKS PASS (~60 s)
python3 word.py --cert       # R1,R2,R3 + certificate replay    -> ALL CHECKS PASS (~90 s)
python3 symbolic_proof.py    # the all-m proof of the block table (sympy)
```

`sprint/k6/six_free_witness.json` is re-verified too (it satisfies (A),(B),(C), but
fails m2 because of its triple `{2,4,5}`); the `word.py` word at `m = 6` is the
m2-compatible replacement.
