# The six-cycle free-label case at k = 6: decided, and the exact delimitation

Member m4, swarm `smwfwznwk`, direction d3 (cross-condition audit of the free-label class).
Files: this note, `audit.py`, `audit2.py`, `pairs_only.py`, `count_lemma.lean`.

**Headline.** The free-label class at `k = 6` — a palette field with *one label absent from every
palette* (non-proper self-avoidance) — is **empty** once the paper's transport lemma (5.3) is
imposed, and it is empty for a reason that has nothing to do with translation invariance: at a
unit equilateral triangle the transport gives three pairwise disjoint palettes, and if a label
`i0` is absent from all of them only five labels are available while three admissible palettes at
a 6-cycle centre need `2 + 2 + 2 = 6`. Globally, the same hypothesis forces `chi(R^2) <= 5` and
contradicts the paper's theorem. The SAT models of `sprint/k6/FREE-LABEL.md` are not countermodels
to the paper's palette hypotheses: they satisfy (5.3) only for centre distances `<= d_0 = pi/(9m)`,
while the printed argument uses (5.3) at distance exactly `1` (Lemma 6.7) and at all distances
`< 1/2` (Lemma 5.5). The coordinator's pairs-only SAT claim is nevertheless **correct**: a
pairs-only sector word exists at `m = 6, 9, 12` (I re-derived it with my own CNF, `pairs_only.py`).
It decides a strictly weaker system.

---

## 1. Setting and the facts that are cited, not re-derived

`c` is a weak measurable `k`-colouring of `C = R^2`, `P_x(e)` the maximal palette of Definition
5.1 (maximal essential support of the circle traces at the centre `x`), `sigma` normalised angular
measure, `R` rotation of directions by `pi/3`. Labels are `[k] = {0, ..., k-1}`; `C_ell` is the
cycle `0-1-...-(ell-1)-0`.

* **(5.2)** (Lemma 5.2.1) for a.e. independent `(e,v)`: `c(x+e+v) notin P_x(e) union P_x(v)`.
* **(5.3)** (Lemma 5.2.3) for a smooth representation `z + f = x + s(f) + t(f)` with
  `s(f), t(f) in S` non-parallel and `s` a local diffeomorphism in the angular coordinate:
  `P_z(f) cap P_x(s(f)) = empty` a.e. on the arc. Centre `z` arbitrary, including far from `x`.
* **(TE)** (the translation exclusion) `P_{x+a}(f) cap P_x(f) = empty` for a.e. `f`, every centre
  `x` and every unit vector `a`. This is (5.3) with `s = id`, `t = a`: Remark 5.3 of the paper
  says the constant second endpoint is permitted and the excluded directions `f = +-a` are null.
  The paper uses exactly this form in the proof of Lemma 6.7 (printed p. 41): *"On the other hand,
  (5.3) applied to `z + f = x + f + a` gives `P_z(f) cap P_x(f) = empty` almost everywhere. Its
  first endpoint map is `f |-> f`, a local angular diffeomorphism; its second endpoint is
  constant, which is permitted."* `m2` (swarm `smwfo9zkl`) derived it independently as (TE).
* **(5.7)** (Cor. 5.4) `P_x(f) cap P_x(Rf) = empty` a.e.
* **(6.2)** (Lemma 6.2) if `ij` is an edge of the transition graph `Gamma_x` then
  `P_x(e)` is not contained in `{i,j}`, and there is a trace supported in `P_x` killing `i` and `j`.
* **Palette bound** `1 <= |P_x(e)| <= k-3` (`results/K6-BARRIER.md` §1).

**Fact 1 (admissible palettes at a 6-cycle centre).** If `Gamma_x` contains a `6`-cycle then its
vertex set is `[6]`, every label lies in a cycle edge, and by (6.2) a palette is never a singleton;
with the palette bound every palette has size **2 or 3** and is contained in no cycle edge. (Cited
from the handoff; re-verified as `admissible_card_ge_two` in `count_lemma.lean`.)

**Fact 2 (no singletons among admissible values at k = 6).** Conversely, an arbitrary value of
size `1` is contained in a cycle edge, so *admissible* means size `2` or `3` — no extra
hypothesis is needed to exclude singletons from the free-label class: `audit.py` part A checks
`all(not admissible({b}) for b in range(6))`.

## 2. The kill

**Theorem 3 (local form, unconditional).** Let `X` be a set of centres carrying palettes with:
(i) `TE` at the three unit pairs of a unit equilateral triangle `{x,y,z} subset X`;
(ii) `P_w(f) != empty` for `w in {x,y,z}`;
(iii) one label `i0` absent from all three palettes;
(iv) all three palettes are admissible for `C_6` (contained in no edge of `C_6`).
Then `False`.

*Proof.* Let `N` be the union of the three (null) exceptional direction sets of (i); for
`f notin N` the three palettes are pairwise disjoint nonempty subsets of `[6] \ {i0}`, a `5`-set,
and by (iv) each has at least two elements. Then `6 = 2+2+2 <= |P_x|+|P_y|+|P_z| <= 5`. `square`

**Corollary 4.** In particular the free-label class of `FREE-LABEL.md` — every centre a 6-cycle
centre, so (iv) holds everywhere; every palette avoiding the fixed label `0`; (5.3) for all centre
pairs — is empty at `k = 6`. The unit triangle can be taken anywhere.

**Theorem 5 (global form, uses the paper's theorem).** There is no palette field on `C` with
`P_x(e) != empty`, `TE` for every unit pair, and a label `i0` absent from every palette.

*Proof.* Such a field is a palette system of **level `k-1`** on `X = C` in the sense of `m2`'s
Theorem A (all values lie in `[k] \ {i0}`). `m2`'s theorem (a palette system of level `m` on `X`
exists **iff** the unit-distance graph on `X` is `m`-colourable; proof: for a finite `F subset X`
choose `f` outside the finitely many null exceptional sets and take `w |-> min P_w(f)`, then
de Bruijn–Erdős) gives a proper `5`-colouring of `C`, contradicting the paper's theorem that the
plane is not 5-colourable (machine-checked: `OAI.EuclideanFiveColor.no_proper_five_coloring`).
`square`

**Theorem 6 (rigidity at unit triangles, a new necessary condition at k = 6).** Let `{x,y,z}` be
a unit equilateral triangle all three of whose vertices are 6-cycle centres of a weak measurable
6-colouring. Then for a.e. direction `f` the three palettes are **pairs and they partition `[6]`**.
In particular, if all three vertices of a unit triangle are cyclic centres **none of them is
ternary**: a ternary cyclic centre has a non-cyclic vertex in each unit triangle through it. The
statement strengthens `m2`'s (B1) (`|P_x(e)| = 3 => |P_y(e)| <= 2` at every unit neighbour `y`,
which already excludes two ternary vertices at unit distance) exactly by using admissibility,
hence `|P| >= 2`, at all three vertices.

*Proof.* `TE` makes the three palettes pairwise disjoint; Fact 1 gives sizes in `{2,3}`; three
pairwise disjoint subsets of `[6]` with sizes in `{2,3}` have total at most `6`, so all are `2`
and the union is `[6]`. `audit2.py` part K enumerates all pairwise disjoint admissible triples:
the only size pattern occurring is `(2,2,2)` with `|A u B u C| = 6`. `square`

Two consequences that delimit the survivors exactly:

* `TE` + nonempty palettes on the plane **is** 6-colourability (`m2` Theorem A). So no
  palette-level countermodel at `k = 6` can exist; the only objects satisfying the palette axioms
  plus `TE` on an unbounded set are restrictions of 6-colourings. This is why the free-label
  programme cannot be repaired by dropping translation invariance.
* What a *varying* free label can buy: if instead of one fixed `i0` each centre `x` avoids its own
  colour `c(x)` (the paper's self-avoidance, Lemma D), the object is exactly a 6-colouring with
  accumulating cyclic centres — the open problem, with no palette-level shortcut.

**Remark 7 (how far the rigidity reaches, and where it stops).** Iterate the rigidity over a unit
rhombus `{x, x+u, x+v, x+u+v}` with `|u| = |v| = |u-v| = 1` and all four vertices cyclic: the
triangle at `x` gives `P_x = [6] \ (P_{x+u} u P_{x+v})` and the triangle at `x+u+v` gives
`P_{x+u+v} = [6] \ (P_{x+u} u P_{x+v})`, so `P_x(f) = P_{x+u+v}(f)` a.e. — the palette field is
periodic under the long diagonal `u+v` of length `sqrt 3`. On the triangular lattice
`Lambda = Z e_1 + Z e_2` (`|e_1| = |e_2| = |e_1-e_2| = 1`) the long diagonals generate
`Lambda' = {p e_1 + q e_2 : p = q mod 3}`, whose shortest vector has length `sqrt 3 > 1`. So the
periodicity is consistent with `TE` (a unit vector is never a period) and yields no contradiction:
the rigidity constrains a 6-colouring with many cyclic centres but does not forbid one. The
restriction `Lambda'` has index 3, which is exactly the three-pair structure of the rigidity.

**Remark 8 (ternary cyclic centres are unit-isolated).** Let `x` be a ternary cyclic centre,
`|P_x(f)| = 3`, and `C = [6] \ P_x(f)` (three labels). For every unit `a`, `TE` puts both
`P_{x+a}(f)` and `P_{x+Ra}(f)` inside `C`, and they are disjoint, so
`|P_{x+a}(f)| + |P_{x+Ra}(f)| <= 3`: **at most one of `x+a`, `x+Ra` can be a cyclic centre** (a
cyclic centre has `|P| >= 2`). This is the local form of the same count as Theorem 6.


## 3. What the sector-word models actually satisfy

All numbers below are produced by `python3 audit.py` and `python3 audit2.py` (two independent
implementations: tuple/set enumeration vs. 6-bit mask arithmetic, plus an external SAT solver).

| condition | sector-word model at `m = 6` | verdict |
|---|---|---|
| values admissible for `C_6` | 36/36 | holds |
| free label `0` absent | 36/36 | holds |
| transport offsets `+-5,+-6,+-7 mod 36` disjoint | yes at every sector | holds |
| (5.7) `P(f) cap P(Rf) = empty` (offset `m`) | yes at every sector | holds |
| **(TE) at unit distance** | `P_{x+a}(f) = P_x(f) != empty` | **fails at every unit pair and every direction** (8640/8640 sampled triples) |
| geometric margin `1.5938 d0 < Delta` | `1.5938 * 11/189 < Delta` in exact rationals | holds |
| trace condition (P5) / (6.2) | every pair value has `delta_b`, `b` outside the edge, for all 6 edges | holds |
| m2 two-centre bound `|P_x|+|P_y| <= 5` | `2+2 = 4 <= 5` | conclusion holds |
| m2's *hypothesis* (unit-triangle pairwise disjointness) | all three palettes coincide | **fails** |
| m11 ternary density `sigma{|P|=3} <= pi` | no triples in the pairs-only model | vacuous |
| m4 (label merging), m1 (single centre), m14 (finite neutrality) | about colourings / finite systems | not applicable |

The pairs-only claim of the handoff is correct. `pairs_only.py` writes its own CNF (different
variable order and clause generation from `sprint/k6/six_sat2.py`), calls
`/opt/lean/bin/cadical`, decodes the model and re-checks every constraint from scratch: SAT with
5760/8640/11520 clauses at `m = 6/9/12`. The witness uses the five values
`{1,3},{1,4},{2,4},{2,5},{3,5}` (the sixth, `{1,5}`, is not needed). It fails (TE) in exactly
the same way, because it is a sector word.

So the correct statement of what the models show is: **the `d <= d_0` fragment of (5.3)** —
together with admissibility, (5.7), the traces and the free label — is satisfiable and admits
accumulating centres. That fragment is *necessary* for the palette axioms, not equivalent to
them. `m2`'s report already isolates this: keeping `TE` at all unit pairs turns the palette system
into a `k`-colouring, and dropping `TE` at even one unit pair is not a relaxation of the colouring
problem.

## 4. Why the fragment is not the hypothesis set

* Lemma 6.7 (printed p. 41) and §6.3.4 use (5.3) with `|z - x| = 1` — exactly `TE` — in the
  five-cycle accumulation argument. The sentence quoted in §1 above is the printed derivation.
* Lemma 5.5 (binary-centre separation) uses (5.3) for **every** `d < 1/2`, via the exact
  decomposition `y + e^{it} = x + e^{i alpha_+(t)} + e^{i alpha_-(t)}`; the deviation there is
  `O(d)`, and the model's sector arithmetic only covers `d <= d_0 = Delta/3` with
  `Delta = 2 pi/(6m)`.
* A sector model can never satisfy (5.3) beyond a bounded window: the direction shift is
  `+- pi/3` only in the limit `d -> 0` with error `1.5938 d`, so the required disjointness at
  offsets `m + k` with `|k| <= 1.5938 d/Delta` grows with `d`; at `d = 1` the offset is `0` and
  the requirement becomes `P(f) cap P(f) = empty`, which every nonempty palette violates.

Hence "the palette-level route is dead" (`REPORT.md` §4, `SYNTHESIS.md` §3, ledger row
"palette constraints + non-proper self-avoidance: satisfiable, accumulating") is established only
for the fragment. For the true palette axioms the correct statement is the opposite: the
free-label case is *empty* (Theorems 3 and 5), so this route is not dead — it is closed in the
direction of the models and open only in the direction "6-colour the plane" (`m2` Theorem A).

## 5. The k = 5 and k = 7 contrast (non-vacuity)

* **k = 5.** Admissible palettes at a 5-cycle centre are exactly the five diagonals; avoiding a
  label leaves three pairs `{1,3},{1,4},{2,4}`, and only `{1,3},{2,4}` are disjoint. Since the
  offset `m` is one of the transport offsets, every sector needs a disjoint partner, so `{1,4}`
  cannot occur; then the offset `m` forces the value to alternate at distance `m`, and the offset
  `m-1` forces consecutive values to be equal — so the word is constant, contradiction. Hence the
  **fragment itself is UNSAT at `k = 5` for every `m >= 2`** (SAT check at
  `m = 6, 9, 12, 15, 18, 24`; hand proof above). This is the exact contrast: at `k = 5` the
  free-label idea fails already combinatorially, at `k = 6` it needs `TE` to fail.
* **k = 7.** The free-label fragment is SAT (`m = 6, 9`, `audit2.py` part L), and three pairwise
  disjoint admissible values avoiding a label exist (`{0,2},{1,4},{3,5}` avoiding `6`). But a
  *globally* free label at `k = 7` is, by Theorem 5's argument, equivalent to `chi(R^2) <= 6`,
  which is open. So the counting obstruction at `k = 6` is sharp: it disappears exactly at
  `k = 7`, where the corresponding statement becomes the six-colour problem.
* **Non-vacuity of the no-go.** `m3`'s proper measurable 7-colouring with non-locally-finite
  cyclic locus has singleton palettes `{c(x+e)}`, so two centres at unit distance have different
  labels and `TE` holds **automatically**. The counting kill needs `|P| >= 2`, so it does not
  touch `m3`'s model: the no-go separates exactly `k = 6` from `k >= 7` instead of excluding the
  known construction. Likewise it does not touch `m13`'s singleton triangle model (singletons, and
  it is not claimed to satisfy `TE`).

## 6. Task-by-task answers to the handoff

1. **Extract and verify the pairs-only solution.** Confirmed at `m = 6, 9, 12` with my own
   encoding (`pairs_only.py`), all constraints re-checked: admissibility, free label, six
   offsets, and the exact margin `1.5938 * 11/189 < 2*3.14159/36`. Exactness: the margin needs
   `pi <= 22/7` and `pi >= 3.14159`, both used in `audit.py` part I; the deviation lemma itself is
   `m15/verify.py`'s Lemma G (exact rational arithmetic) and is not re-derived here.
2. **All necessary conditions.** `m11`, `m4`, `m1`, `m14`: satisfied or inapplicable, see the
   table. `(P5)`/`(6.2)`: satisfied. `m2`'s conclusion: satisfied. **But** (TE), which is a
   printed consequence of (5.3) and the one ingredient that relates different centres at relevant
   distances, **fails**. That is the constraint the class cannot meet, and it is not a missing
   refinement: at `k = 6` it literally forbids the free label.
3. **The general translation-invariant question.** For every `m` and every value set (pairs,
   triples, free label or not) a translation-invariant sector word violates (TE) at every unit
   pair, so it satisfies no version of the palette axioms at `k = 6`. The interesting decision is
   therefore about the fragment, and there the answer is: `k = 6` pairs-only SAT for
   `m = 6, 9, 12`; `k = 5` UNSAT for all `m`; `k = 7` SAT. Whether the pairs-only fragment is
   SAT for *all* `m >= 6` is left to d1's dynamic programme; it is not needed for the verdict.
4. **The colouring-level question.** A proper colouring's free labels are the colours `c(x)`, so
   they must vary; `TE` plus nonempty palettes is exactly a 6-colouring (`m2` Theorem A), and the
   self-avoidance label `c(x)` is then the colour of `x`. Hence there is no palette-level
   countermodel to be found at `k = 6`, and the sharpest true statement is Theorem 6 plus: any
   model of "palette axioms + self-avoidance" is a 6-colouring, and the open question is only
   whether one has accumulating cyclic centres.
5. **Vacuity.** §5 above.

## 7. Independent confirmation inside the swarm, and one distinction that matters

* `m1` (f4) and `m2` (f2, f8) reached the same conclusion from the *colouring* side: no
  centre-independent palette field is the maximal palette field of any weak measurable
  6-colouring; `m2`'s Lemma P/Theorem R even show that a globally free label forces the colour
  class `A_i` to be plane-null, without using the paper's theorem; `m2`'s (X1) shows `TE` forces
  the type partition of a piecewise-direction-invariant field to be a proper colouring. Those
  arguments quantify over colourings.
* The kill of §2 is **palette-level and unconditional**: it needs no colouring, no properness, no
  measurability and no translation invariance, only `TE` at the three unit pairs of one unit
  triangle plus admissibility of three palettes. So it also kills abstract palette systems that no
  colouring induces, which is exactly the object the free-label programme builds. The counting
  step is machine-checked (`count_lemma.lean`, standard axioms only). Theorem 5 is the global
  version and does use the paper's theorem.
* `m1`'s Theorem (f3, the fragment word exists iff `m >= 5`) shows the fragment is SAT for
  *every* `m >= 5`, so the fragment's satisfiability is not a small-`m` artifact; and `m1`'s k=5
  result (the transport graph is connected and circulant, hence not bipartite for three
  consecutive offsets) is the same decision as §5's hand proof, by a different argument.

## 8. Corrections to the sprint record

1. `FREE-LABEL.md` line "the exact two-centre transport (5.3) for all pairs of centres at distance
   `<= d_0`" is accurate; the report's summary of it as satisfying the palette-level hypotheses is
   not. The models satisfy a fragment.
2. `REPORT.md` §5 and the ledger row "palette constraints + non-proper self-avoidance at `k = 6`:
   satisfiable, accumulating" must be read as "with (5.3) restricted to `|z'-z| <= d_0`". With
   (5.3) in full the class is empty (Theorems 3, 5).
3. `REPORT.md` §4 and `SYNTHESIS.md` §3's "the palette-level route is dead at `k = 6`" is not
   established by the models for the reason above. What *is* established is `m2`'s Theorem A: a
   palette system with `TE` on the plane exists iff `chi(R^2) <= 6`.
4. A further, softer gap in the same direction: "each palette is admissible, hence every `y_k` is
   an `ell`-cycle point" is the *converse* of (6.2). Admissibility of palettes is necessary for
   `x in L`, not sufficient (cyclic means the transition graph `Gamma_x` contains the cycle, via
   positive-density transition sets). So the models do not exhibit an accumulating cyclic locus of
   any colouring at all; they exhibit accumulating centres where the necessary condition (6.2)
   holds.

## 9. Files and commands

```bash
cd .ultramath/smwfwznwk/m4
python3 audit.py        # A-I: domain, counting kill, witness re-verification, (TE) failure,
                        #      (P5), m2, m11, exact geometric margin   (exit 0 = all pass)
python3 audit2.py       # J-N: bitmask recount, unit-triangle rigidity, k=5/7 fragment SAT,
                        #      fresh pairs-only witness, m3 non-vacuity control
python3 pairs_only.py 6 9 12     # own CNF + CaDiCaL, decoded model re-checked
lean count_lemma.lean   # machine-checked counting step; compiles in ~3 min, axioms
                        # [propext, Classical.choice, Quot.sound] only
```

| file | content |
|---|---|
| `audit.py` | first implementation of all model checks (set/tuple enumeration) |
| `audit2.py` | second implementation (6-bit masks), rigidity, fragment decision at k=5,7 |
| `pairs_only.py` | independent CNF for the pairs-only sector word, CaDiCaL, model re-check |
| `count_lemma.lean` | `card_three_disjoint_le`, `no_free_label_triangle`, `admissible_card_ge_two` |
| `work/paper.txt` | `pdftotext -layout` of the paper, used for the line references |
