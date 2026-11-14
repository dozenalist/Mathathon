# The k = 6 cyclic locus: which parts of the boundary are real

Member `m4`, swarm `smwfwi7rh`, direction `d3` (direct attack on **(W)** / delimited classes).

**Verifier:** `verify.py` in this directory. Run
`cd .ultramath/smwfwi7rh/m4 && python3 verify.py`; exit status 0 = all 33 checks pass. Exact integer / rational arithmetic throughout; the
satisfiability counts are decided by two unrelated algorithms (recursive DFS and an exact
integer DP over `(start, current, set-of-values-used)`).

---

## 0. What is delivered

| § | statement | kind |
|---|---|---|
| 2 | **Theorem 1** (unit-separation transport): for *every* weak measurable `k`-colouring, every centre `x`, every unit `a` and a.e. `f`, `P_{x+a}(f) ∩ P_x(f) = ∅` | theorem (from the paper's Lemma 5.2(3) + Remark 5.3) |
| 3 | **Corollary 2**: no palette field independent of the centre satisfies (5.3). Hence both accepted countermodels are *local* only, and the proposed six-cycle free-label sector search is vacuous | no-go, class stated, non-vacuous |
| 4 | **Theorem 3** (k = 6, class of a.e.-singleton palettes): no 5-cycle and no 6-cycle in any `Γ_x`; the 4-cycle locus is locally finite; so `L` is locally finite **iff** the 3-cycle locus is (hence **(W)** holds as soon as the 3-cycle locus is locally finite) | theorem, sharp |
| 5 | **Correction**: `m3`'s gadget needs **three** labels absent from the shadow of the square, not four. At `k = 6` exactly three are available | counterexample to a stated claim |
| 6 | `k = 6`, 6-cycle centre: the single-centre R-orbit system has exactly **510** pointwise admissible words (two procedures, plus agreement with `sprint/k6/orbit_correct.py`); **nothing** is excluded pointwise | decided computation |
| 7 | the unit-distance shadow of a square of side `ℓ < 1/√2` (a thin annulus) is **3-colourable** — exact rational certificate; so there is no geometric obstruction to `m3`'s `k = 6` condition | decided computation |
| 8 | the **global** palette system at `k = 6` restricted to a triangular lattice is **SAT**, with an explicit exact `Z²`-periodic witness | decided computation |

What this does **not** do: it does not decide **(W)**. §9 says exactly what is left.

---

## 1. Setting

As in the paper (`attachments/here-are-three-files-ni5n/paper.pdf`, §5–§6): `c` is a weak
measurable `k`-colouring, `P_x(e)` the maximal palette of Definition 5.1 (p. 26), `R` the rotation
of directions by `κ = π/3`, `Γ_x` the transition graph of Definition 6.1 (p. 34),
`L = {x : Γ_x contains a cycle}`, and "typical" = density-one point of its own colour class.
Two facts are used verbatim: `P_x(e)` is **nonempty** for a.e. `e` (p. 26, "It also gives
nonemptiness of `P_x(e)` almost everywhere"), and **(5.3)** holds at every fixed pair of centres
(Lemma 5.2(3), p. 27). The displayed formulas used here, (5.2), (5.3), (5.7), Lemma 5.5 and
Remark 5.3, were each re-extracted page by page in both `pdftotext -layout` and `pdftotext -raw`
mode; the two extractions agree, and the pages (27, 29, 30) were rendered with `pdftoppm` as well.

---

## 2. Theorem 1 (unit-separation transport)

> **Theorem 1.** Let `c` be a weak measurable `k`-colouring, `x ∈ R²`, `a` a unit vector. Then for
> almost every unit direction `f`,
> `P_{x+a}(f) ∩ P_x(f) = ∅`.
> No typicality of `x` or of `x+a` is needed.

*Proof.* Apply Lemma 5.2(3) with centres `z = x + a` and `x` and with the representation
`z + f = x + s(f) + t(f)`, `s(f) = f`, `t(f) = a`. Since `|a| = 1` we have `t(f) ∈ S`; the map
`s = id` is a local angular diffeomorphism; and `s(f) = f` is nonparallel to `t(f) = a` for every
`f ∈ S \ {±a}`, a null set of directions. Remark 5.3 (p. 29) states exactly this: "for any fixed
direction `a`, the representation `(x + a) + f = x + f + a` is admissible off `f = ±a`". The
conclusion of Lemma 5.2(3) is `P_z(f) ∩ P_x(s(f)) = ∅`, i.e. `P_{x+a}(f) ∩ P_x(f) = ∅`, a.e. ∎

The identity is the paper's own Remark 5.3. What is used below, and what the record of this
sprint does not, is that it is a **global** statement — every centre, every unit `a`, no size
restriction — and that both accepted countermodels violate it.

## 3. Corollary 2: no palette field independent of the centre

> **Corollary 2.** Let `P_z(e) = P(e)` be independent of `z`. If `P` satisfies (5.3) for all centre
> pairs, then `P(e) = ∅` for a.e. `e`. In particular no nonempty centre-independent palette field
> satisfies the paper's (5.3).

*Proof.* Take any unit `a`. By Theorem 1, `P(e) = P(e) ∩ P(e) = ∅` a.e. ∎

**Which class this kills, and that it is not vacuous.** The class is "palette fields independent
of the centre, nonempty, satisfying (5.3) at every pair of centres". It is *non-vacuous as a
specialisation of the published local axioms*: the two accepted countermodels of the previous
swarm are of exactly this shape, which I checked by reading their sources.

* `m15`'s uniform block field (`.ultramath/smwfo9zkl/m15/construction.py`, `system()`): the data is
  a **signature** `sig[i]` indexed by the sector `i` of the direction alone, with no centre
  argument. Its (P3) is claimed only for `|z − z'| ≤ d₀ = π/(9m)`.
* `m13`'s models (M), (M′) (`.ultramath/smwfo9zkl/m13/no-go.md`, Theorem 2): "`Z = R²`,
  `P_z(e^{it}) = Q_{s(t)}`", resp. `{4 + s(t)}`, again with no `z`-dependence; (P3) is claimed only
  for `|z − z'| ≤ ε = 1/50`.

Both therefore satisfy `P_{x+a}(f) ∩ P_x(f) = P(f) ≠ ∅` for **every** unit `a` and a.e. `f`. They
refute the *local* class `P(k, ε)` with `ε < 1`; they say nothing about the true, global system,
because they are not members of it.

**Two consequences for the swarm's direction.**

1. The report's frontier sentence — the countermodels' "only failure is trace-consistency with a
   proper colouring" (REPORT §5) — is incomplete. They fail the paper's own (5.3) already, at
   distance 1, before any colouring is mentioned. Self-avoidance is *a* colouring-level
   constraint; unit-separation transport is another, and it is stronger and cheaper.
2. The coordinator's lead (ii) asks whether "a translation-invariant sector field with a free label
   can satisfy the exact transport shifts". If the field is translation-invariant **and** the
   unit-pair shift is imposed, the answer is NO for every sector count `m`, every cycle length and
   every free label, for the single reason above. Any sector search should therefore *not* impose
   the unit-pair shift on a centre-independent field and then report NO as information; the
   informative question is centre-dependent fields, and there (5.3) is a global constraint
   equivalent to the colouring problem, so no finite search reaches it (this is `m14`'s
   satisfiability-neutrality, which §6 and §8 below confirm independently).

## 4. Theorem 3: at k = 6 with singleton palettes only the triangle matters

Say a weak measurable 6-colouring is **in class S₁** if for **every** centre `x`, `P_x(e)` is a
singleton for a.e. `e`. (Class S₁ contains every colouring that is constant on the cells of a
locally finite Borel partition with piecewise `C¹` boundaries — this is `m3`'s §3.8 argument — and
`m3`'s `k ≥ 7` counterexample is in S₁.)

> **Theorem 3.** Let `c` be a weak measurable 6-colouring in S₁. Then
> (i) `Γ_x` contains no 6-cycle, for every `x`;
> (ii) `Γ_x` contains no 5-cycle, for every `x`;
> (iii) `{x : Γ_x contains a 4-cycle}` is locally finite.
> Hence `L` is locally finite **iff** `{x : Γ_x contains a 3-cycle}` is locally finite.

*Proof.* Write `P_x(e) = {b_x(e)}` and let `C` be a simple cycle of `Γ_x` with vertex set `V(C)`.

(i) A 6-cycle on six labels has `V(C) = [6]`. Lemma 3 of `sprint/k6/STRUCTURE.md` (from Lemma 6.2
of the paper) says: a singleton palette `{b}` at a centre whose `Γ_x` contains a cycle `C` has
`b ∉ V(C)`. Here `b_x(e) ∈ [6] = V(C)`, and the palette is nonempty. Contradiction.

(ii) A 5-cycle has `|V(C)| = 5`; let `X` be the single label outside it. Lemma 3 gives
`b_x(e) = X` for a.e. `e`, i.e. `P_x(e) = {X}` a.e. Then (5.7) gives
`{X} = P_x(e) ∩ P_x(Re) = ∅` a.e. Contradiction.

(iii) A 4-cycle has a two-element complement `{X, Y}`. Lemma 3 gives `P_x(e) ∈ {{X},{Y}}`, and
(5.7) gives `P_x(e) ∩ P_x(Re) = ∅`, i.e. `P_x(Re) ≠ P_x(e)`. So `P_x(e) ∩ {X,Y} ≠ ∅` a.e.: `x` is
**binary for the pair `{X,Y}`** in the sense of the paper (§5.3, p. 30). Lemma 5.5 of the paper
("for every fixed pair of labels, any two distinct centres binary for that pair are at distance at
least `δ_*`") applies with no typicality hypothesis, so the set of all centres binary for
`{X,Y}` is `δ_*`-separated, hence locally finite. There are `C(6,4)·3 = 45` labelled 4-cycles on
six labels, and each 4-cycle locus lies in the binary set of its own complement pair. A finite
union of locally finite sets is locally finite.

Since `L` is the union of the loci of the simple label cycles, i.e. of the 3-, 4-, 5- and 6-cycle
loci (a 6-cycle on six labels is a Hamiltonian cycle), (i)–(iii) give the last assertion. ∎

The finite core of the proof is machine-checked in the verifier's block E: at a 6-cycle there is no
admissible singleton at all (E1); at a 5-cycle there is exactly one, so `P ≡ {X}` and (5.7) reads
`{X} ∩ {X} = ∅` (E2); at a 4-cycle there are exactly two, every (5.7)-compatible orbit alternates
(E3b) and every admissible value meets the outsider pair (E3c), which is precisely binarity for
that pair; and there are 45 labelled 4-cycles (E4).

**Sharpness, and why the class restriction is not vacuous.** At `k ≥ 7` the analogous reduction is
*false as a statement about L*: `m3` constructs a proper measurable `k`-colouring in S₁ whose `L`
is not locally finite, and its accumulating points are 3-cycle points (`Γ_{q_n} ⊇ {0,2,3}`). So
Theorem 3 is exactly the statement "the triangle is the only possible obstruction", and `m3` shows
that at `k ≥ 7` the triangle does obstruct. At `k = 6`:

> **Corollary 4.** If a proper 6-colouring `c` and a closed square `W` of side `ℓ < 1/√2` exist such
> that the unit-distance shadow of `W` misses three of the six labels, then local finiteness fails
> at `k = 6`.

This is `m3`'s Corollary D, restated; Theorem 3 is what makes it *the* mechanism rather than one
mechanism. Note the honest vacuity statement: at `k = 6`, S₁ ∩ {weak measurable 6-colourings} is
nonempty **iff** a 6-colouring exists, so Theorem 3 is vacuous under `χ(R²) = 7` and is meaningful
only inside a contradiction argument that starts from a 6-colouring. The same caveat applies to
every `k = 6` statement in this sprint, including REPORT §3b.

## 5. Correction: the label count is not the k = 6 obstruction

REPORT §3b (and the brief's "Frontier" paragraph) explains the `k ≥ 7` counterexample by "it needs
four outsider labels; at `k = 6` a triangle has only three, which is exactly the obstruction".
That is not what `m3` proves. `m3`'s own Lemma C / Corollary D (`m3/proof.md` §3.9) is:

> a proper `k`-colouring, plus a square `W` of side `ℓ < 1/√2` whose unit-distance shadow misses
> **three** prescribed labels `{a,b,d}`; then `W` may be relabelled from `{a,b,d}` and the Mercedes
> centres `q_n → q_*` give a triangle in `Γ_{q_n}`.

Three labels, not four. The four palette values `{1,4,5,6}` in Theorem A are an artefact of the
particular hexagonal 7-colouring; at every `q_n`,

* the palette is the singleton `{c(q_n+e)}`, with `q_n+e` in the shadow, so it is *automatically*
  outside `{a,b,d}`;
* (5.7) at `q_n` is automatic from properness: `c(q_n+e) ≠ c(q_n+Re)` because `|e − Re| = 1`;
* non-binarity needs only that all three remaining labels occur on the unit circle, and `k−3 = 3`
  at `k = 6`.

So at `k = 6` exactly three labels are available outside a triangle and exactly three suffice:
there is **no label-count obstruction**. Consequently the direction `d4` premise ("an accumulation
needs 4 labels free there") is, as stated, false, and the `k = 6` boundary is purely the chromatic
wall: local finiteness at `k = 6` is vacuous if `χ(R²) = 7` and fails (under Corollary 4's
condition) if `χ(R²) = 6`.

## 6. Decided computation: the six-cycle orbit system at a typical centre, k = 6

At a typical 6-cycle centre `x` (colour `i`, palettes inside `[6] \ {i}`) the accepted constraints
are: (E1) `P_j ∩ P_{j+1} = ∅` (5.7); (E2) `|P_j| = 3 ⇒ P_{j±1} = ([6]\{i}) \ P_j` (Lemma 2 of
`STRUCTURE.md` + self-avoidance + `|P| ≥ 2`); (E3) `P_j` not inside a cycle edge (6.2); (E4)
`i ∉ P_j` (self-avoidance). The verifier decides the number of admissibly-typed 6-tuples exactly:

| system | count |
|---|---|
| admissible palettes per position | **16** |
| (E1)+(E2) pointwise words | **510** |
| of those, words with ≥ 3 distinct values | 486 |
| words with exactly 2 distinct values | **24** = 12 all-pairs + 6 of pattern `(3,2,3,2,3,2)` + 6 of `(2,3,2,3,2,3)` |
| words with 3 / 4 distinct values | 228 / 258 |
| words with 5 or 6 distinct values | 0 |

The DFS and the DP agree, and both agree with the coordinator's independent
`sprint/k6/orbit_correct.py` (510). Note the necessary refinement of REPORT §6: it records only
that "the 2-periodic `(3,2,3,2,3,2)` pattern has exactly 6"; the 2-valued stratum in fact has 24
words, including 12 all-pairs ones. Careful: a 2-valued *word* is not a 2-valued *field*, so
`m7`/`m16` exclude only a field that is 2-valued almost everywhere; 510, not 486, is the pointwise
count. **Conclusion:** the single-centre constraints exclude nothing at a typical 6-cycle centre,
so no single-centre or finite-palette computation can decide `k = 6` — consistent with, and an
independent confirmation of, `m14`'s satisfiability-neutrality.

## 7. Decided computation: the shadow annulus is 3-colourable

`m3`'s `k = 6` condition (§5) is a geometric one: three of the six labels must be absent from the
unit-distance shadow of a small square. The shadow of a square of side `ℓ` is contained in the
annulus `A = {q : 1 − η ≤ |q − p₀| ≤ 1 + η}` with `η = ℓ/√2`; for `ℓ = 1/100`, `η = 1/(100√2) <
71/10000`.

> **Proposition 5.** `A` is 3-colourable, by `χ(θ, r) = ⌊((θ mod 120°)/40°)⌋`.

*Proof.* For `q, q' ∈ A` with `|q − q'| = 1`, the law of cosines gives
`cos Δ = (r² + r'² − 1)/(2rr')` where `Δ` is the angular difference and `r, r'` the two radii in
`[1−η, 1+η]`. This expression is increasing in each variable on the box (its `r`-derivative has the
sign of `r² − r'² + 1 > 0`), so its range is the corner range; exactly,
`cos Δ ∈ [0.492824, 0.507025] ⊂ (1/4, 3/4)`. Since `cos 40°` is the root in `(1/2,1)` of
`8t³ − 6t + 1` and that polynomial takes the value `−1/8` at `t = 3/4` and `25539/125000 > 0` at
`t = 79/100`, `cos 40° ∈ (3/4, 79/100)`, so `cos 80° = 2cos²40° − 1 < 2(79/100)² − 1 < 1/4`. Hence
`Δ ∈ (40°, 80°)`. Now if `y − x` mod `120°` lies in `(40°, 80°)` then
`⌊y/40°⌋ − ⌊x/40°⌋ ∈ {1,2}` or `∈ {−1,−2}`, never `0`; so the three arcs of `120°/3 = 40°` give a
proper 3-colouring. ∎

**Consequence.** There is no geometric obstruction to `m3`'s `k = 6` hypothesis. Three labels on the
shadow is geometrically feasible; the only remaining obstruction is the *global* one — whether such
a 3-coloured annulus extends to a proper 6-colouring of the plane, which is the open problem.

## 8. Decided computation: the global palette system is SAT on a lattice

To test whether some *lattice* argument might decide `k = 6`, take the triangular lattice
`Λ = Z + Zω`, `ω = e^{iπ/3}`, whose unit vectors are `±1, ±ω, ±(ω−1)`, and impose on it the global
constraints: palettes nonempty of size `2`, unit-separated points get disjoint palettes, self-
avoidance with an actual colour, and a 6-cycle in `Γ`. The verifier exhibits an exact
`Z²`-periodic witness: with classes `k(m,n) = (m + 2n) mod 3` and
`A₀ = {0,1}, A₁ = {2,3}, A₂ = {4,5}`, colours `c₀ = 2, c₁ = 4, c₂ = 0`,
`P(m,n) = A_{k(m,n)}`, `c(m,n) = c_{k(m,n)}`: every lattice neighbour changes the class, so
neighbouring palettes are disjoint and neighbouring colours differ; `c_k ∉ A_k`; and the 6-cycle
`(0,2,4,1,3,5)` uses all six labels while no palette value is contained in any of its edges.
Brute force over a `25 × 25` block finds no violation. **So the global palette system at `k = 6`
survives on a lattice**; no lattice-level (or finite) palette argument can decide `k = 6`.

## 9. The boundary, precisely

````text
(W) : L ∩ B(y,R) finite for some R > 1                                  OPEN
     implied by  χ(R²) ≥ 7  (vacuously);   ¬(W) ⇒ χ(R²) ≤ 6
     in class S₁ (a.e.-singleton palettes): (W) ⟺ 3-cycle locus locally finite   [Thm 3]
     3-cycle locus fails to be locally finite as soon as a 6-colouring has a square of
     side < 1/√2 whose shadow misses 3 labels                                     [m3 + Cor 4]
     such a shadow is 3-colourable, so no geometric obstruction there             [Prop 5]
     no finite / lattice / single-centre palette argument can reach it            [§6, §8, m14]
````

Not done, and claimed nowhere: any decision of `(W)`; any statement about `k = 6` that is
unconditional (all of them are vacuous if `χ(R²) = 7`); any bound on `δ_*`; the `k = 6` analogue of
the paper's §6.3.2 accumulation argument for the triangle locus.

## 10. Files

| file | content |
|---|---|
| `NOTE.md` | this note |
| `verify.py` | all 33 checks: block A (§3), B (§6), C (§7), D (§8), E (the finite core of Theorem 3); `python3 verify.py`, exit 0 |
| `orbit_lib.py` | the orbit system: admissible palettes, and the two independent decision procedures (DFS, DP) |
| `orbit_counts.py` | standalone run of both procedures with the value histograms |
