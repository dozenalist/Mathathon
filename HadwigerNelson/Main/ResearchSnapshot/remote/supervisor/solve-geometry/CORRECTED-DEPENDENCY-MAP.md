# Corrected cyclic-locus map: the minimal §7 input at k = 6, with constants, retractions and consolidation

Consolidates (read-only, cited, claims treated as candidates and checked here):
`supervisor/solve-traces/NOTE-far-field.md` (call it **FF**), `supervisor/solve-synthesis/LEDGER.md`
(**LED**), `supervisor/solve-synthesis/notes/LEMMA-D-REPAIRED.md` (**LD**). Supersedes the first
version of this file.

Grades: **[A]** arithmetic, machine-checked by `checks/constants.py` (output `supervisor_checks.out`);
**[P]** paper-level argument written or transcribed, not machine-checked; **[C]** cited from another
worker, checked only as noted; **[S]** source-checked at the cited Lean lines by that worker;
**[X]** record only.

## 0. Retractions (mine, from the previous block)

1. **Isolation-radius convention.** I wrote that `L = (6/5)Z^2` has "every isolation radius exactly
   `3/5`". Wrong. With `B` **open**, `L ∩ B(x,r) = {x}` iff `r <= 6/5`, so the maximal isolation
   radius is `6/5 = 1.2`; `3/5` is the *disjoint-ball packing radius* (half the nearest-neighbour
   distance). Consequently **(6/5)Z² does not refute `(ISO)(r)` for `r > 1`** — it satisfies it.
   What it refutes is `(ISO)(r)` for `r > 6/5`, hence for `r > sqrt2 ≈ 1.4142` [A].
2. **Which claim is disproved, stated once.** WEAKEST.md's hypothesis is `(ISO)` with `r > sqrt2`;
   (6/5)Z² is locally finite, 1-dense (covering radius `0.8486 <= 1`) and has no point isolated in a
   ball of radius `> sqrt2`. So it refutes **"`(LF)` ⟹ `(ISO)(sqrt2)`"** [A]. The distinct claim
   "`(LF)` + 1-density ⟹ `(ISO)(r)` for some `r > 1`" is refuted by **`L = Z²`** instead: packing
   radius `1/2`, isolation radius exactly `1`, covering radius `0.7071 <= 1` [A]. Both lattices are
   closed, locally finite and 1-dense, so neither refutation needs any colouring fact.
3. **`(W)` vs `(W2)` are not equivalent.** I previously displayed them as "the same when `R >= 2`".
   They are not the same hypothesis. `(W2)` ⟹ `(W)` (take `R = 2`), and `(W)` with `R >= 2` ⟹
   `(W2)`; but `(W)` with `R in (1,2)` implies nothing about `(W2)`, and I have a counterexample
   below. `(W2)` is *stronger*. Only `(W)` is needed.
4. **"`rho > 1 >= mesh`" was written in the previous version. It is meaningless**: the mesh is
   `1 + o(1)` in the precision `eps`, so `1` is an infimum and never a value. The correct order is
   `rho` first, then `eps` (§9, P7).
5. **"`L` has an isolated point" is not the missing input.** Already corrected last block, kept here
   because LED R1/REPORT §2 still use the phrase: the input is finiteness, `(W)`.

## 1. What §7 consumes, exactly (unchanged by §0)

| step | what it needs about `L` | source |
|---|---|---|
| (a) cover obstruction applies on the region `Q` | `Q` compact convex, **inradius(Q) > mesh**, mesh `1+o(1)` | [P] paper Lem. 7.5; m12 Lem. 5.1 |
| (b) one core disk per point of `L_0 = L ∩ Q` | `|L_0| < infinity` | [P] paper Lem. 7.4 |
| (c) `Q` can be positioned | `L` closed | [P] |
| (d) pigeonhole to one non-null loop; gap `B(x,rho')` at its centre | `|L_0| < infinity`; **no lower bound on `rho'`** | [P] paper Prop. 7.1 |
| (e) `L_0 != empty` | every closed disk of radius `> 1` meets `L` | [C] m12 Thm D / m5 (paper-level, unverified by me) |

Nothing else about `L` is used, and no palette bound, no properness, and no `k`-specific
combinatorics enters except `G = K_6`, `alpha in (0,1/6)`, `ell in {3,4,5,6}` (LED R5 agrees: the
multiplicity-2 obstruction is `k`-uniform).

## 2. Constants (three live errors in the shared notes, all [A])

1. `sprint/k6/WEAKEST.md` prints `4 < s < r/sqrt2` for "square inside `B(x_0,r)`". Containment is
   `s < sqrt2 * r`. That printed line needs `r > 4 sqrt2 = 5.657`, contradicting its own `r > sqrt2`.
   Correct line: **`2 < s < sqrt2 * r`** (the `s > 2` range is the sharp mesh range).
2. `sprint/k6/WEAKEST.md`: "`(LF)` implies `(ISO)`" — **false**, §0.2. What holds is `(LF) ⟹ (W)`.
3. `sprint/k6/REPORT.md` §2 mixes two constants: the mesh gives the **inradius** threshold `> 1`,
   the square route needs `R > sqrt2`, the disk route needs `R > 1`. Only the disk route is sharp.

## 3. The sharp isolation statement [P]+[C]+[A]

**Proposition 1.** `x in L`, `L ∩ B(x,rho) = {x}` (open ball) ⟹ `rho <= 2`.
*Proof.* If `rho > 2`, choose `r` with `1 < r < rho/2` and `eps > 0` with `2r+eps < rho`; the closed
disk of radius `r > 1` about `x + (r+eps)u` lies in `B(x,rho)` and misses `x`, so it misses `L`,
contradicting the density theorem (`m12` Thm D). `square`

**Proposition 2 (sharp form of the isolation route).** `(ISO)(r)` with `r > 1` ⟹ `(W)` ⟹ Prop. 7.1.
By Prop. 1 the usable window is **`1 < rho <= 2`**, and the threshold is `1`, not `sqrt2`: no square
is needed, take `Q = B̄(x,rho')` with `1 < rho' < rho` (a disk's inradius is its radius).

So: no worker can profit from proving a *large*-radius isolated centre (impossible, Prop. 1), and no
worker should aim at `r > sqrt2` (not sharp). `m3`'s `k >= 7` accumulation (`q_n -> p_0`) has
isolation radii `-> 0` and is untouched by Prop. 1.

## 4. Consolidated dependency proposition (corrected minimal input)

Let `c` be a weak measurable 6-colouring, `L` its cyclic locus (closed, `1`-dense), and put

* `(LF)`: `L` finite in every bounded set;
* `(Iso_r)`: `exists x in L, L ∩ B(x,r) = {x}` (`B` open);
* `(W_R)`: `exists y, |L ∩ B(y,R)| < infinity`;
* `(W2)`: `(W_2)`, i.e. `R = 2`.

**Proposition 3 (minimal dependency).**
(i) **[P]** `(W_R)` with `R > 1` ⟹ Prop. 7.1 at `k = 6`. *(Choose `rho in (1,R)` avoiding the finitely
many radii `|p-y|`, `p in L ∩ B(y,R)`; then `∂B(y,rho) ∩ L = empty` — derived, not assumed — the
region is `Q = B̄(y,rho)` with inradius `rho > 1`, and the precision is then chosen so that
`mesh(eps_n) < rho` (see §9 P7: `rho` first, `eps` after — never `rho > 1 >= mesh`), `L_0` finite
and non-empty.)*
(ii) **[P]** `(Iso_r)` with `r > 1` ⟹ `(W_R)` for every `R < r` (take `R in (1,r)`), hence (i); and
     `(Iso_r) ⟹ r <= 2` (Prop. 1). Note `R < r`, not `R = 1.5`: the finiteness is inherited only
     downwards, which is the same slip as §0.1 and §0.3.
(iii) **[P]** `(LF)` + `L != empty` ⟹ `(W_R)` for every `R > 1`.
(iv) **[A]** `(LF)` + 1-density ⇏ `(Iso_r)` for any `r > 1` (`L = Z²`); and ⇏ for `r > sqrt2`
     either (`L = (6/5)Z²`, the case WEAKEST.md actually needs).
(v) **[A]** `(W)` ⇏ `(W2)`. `L = {0} ∪ ⋃_{k>=1} S(0, 3k/2)` is closed, `0.75`-dense, has
     `|L ∩ B(0,1.2)| = 1`, and `|L ∩ B(y,2)| = infinity` for **every** `y` (every radius-2 ball cuts
     some circle in an arc). So `(W)` and `(W2)` differ on closed 1-dense sets.
(vi) **[X]** No item in the record implies `(W)`, `(W2)`, or their negations; and `(W)` is the
     weakest of the listed *sufficient* hypotheses. Necessity of `(W)` is not known — only that
     `m3`'s `k >= 7` colouring fails it and that §7 fails there for exactly that reason.

**Therefore: the minimal dependency proposition is (i) with `(W_R)`, `R > 1`.** `(W2)` is a
convenient single-scale restatement that is strictly stronger and buys nothing; `(Iso)`, `(LF)` and
"`L` has an isolated point" are all either stronger or false summaries of it.

## 5. Consolidated retired-worker contributions

**5.1 Far-field decoupling (FF §2-§4c).** **[S]+[P]** *Lemma FF-D:* `c = c'` off `B(x_0,1-eps)`,
`0 < eps <= 1` ⟹ `P^c_{x_0}(e) = P^{c'}_{x_0}(e)` for a.e. `e`; no a.e. quantifier is spent. Two
consequences I keep: **(FF-C1)** the palette is a far-field object (radius-1 cluster trace), so the
palette cannot see the accumulation of cyclic centres — this is *why* `m3` works and why
`sprint/k6/FREE-LABEL.md`'s countermodels are possible; **(FF-C2)** `R < 1` is sharp, `R = 1` fails
(a recolouring supported on the closed exterior of the unit ball moves the palette on a set of full
angular measure) — so `m3`'s "gadget inside `B(q_n,1/2)`" is exactly what is needed, and the palette
is a measure-class invariant (null-set recolourings are invisible).
*Vacuity guard:* FF-D is stated for **measurable colourings**, not proper ones, and the constant `1`
is a genuine threshold; do not quote it as "the palette is invariant under any perturbation".

**5.2 Self-avoidance, repaired (LD + LED R4).** **[P]+[A]** *Statement (true):* at a density-one point
`x` of its own colour class, `c(x) = i ⟹ i notin P_x(e)` for a.e. `e`. The proof recorded in
`sprint/k6/REPORT.md` §5 is **invalid** (it uses Lemma 5.2(2) on the circle of radius one about
`x + e_0`, which meets the unit circle about `x` in exactly two points, and the relevant one is the
excluded antiparallel direction). Valid proof uses (5.2) with the sector Jacobian: a positive-measure
angular set `D` of directions with `i in P_x(e)` kills a fraction `|iD ∪ -iD|/(2 pi) >= |D|/(2 pi)` of
every `B(x,h)`, contradicting density one. *Citation change:* the 510-word orbit count, `m4`'s
singleton-class reduction and "self-avoidance is the frontier" stand, but must cite LD, not Lemma
5.2(2).

**5.3 Naming collision, flagged.** There are **two different "Lemma D"** in the record: FF's *far-field
decoupling*, and the *self-avoidance* lemma of LD. They are independent. Anything citing "Lemma D"
without a file is ambiguous; I use FF-D and LD-D below.

**5.4 Ledger items kept (LED).** R1 = Prop. 3(i) (with the constants corrected here). R2: the §8
strip layer is UNSAT only at `(4,3),(4,4),(5,5)` and SAT for all `k >= 6`, `ell`, so §8 fails at
`k = 6` for attributable reasons; with FF-C2 and `m10` T3 this kills every palette-only route. R3
(the sharpest attack surface): in the singleton class `S_1` at `k = 6` there is no 5-cycle and no
6-cycle in any `Gamma_x` and the 4-cycle locus is locally finite, so **`L` is locally finite iff the
3-cycle locus is** [X]; `m3` accumulates at 3-cycle centres, so a 6-colouring refuting `(W)` must be
outside `S_1`. R5: the cover obstruction is multiplicity-2 and `k`-uniform; the continuation note's
"multiplicity-3 covers exist" is a non-sequitur against §7. R6: dead routes (two-centre palette CSP =
the finite unit-distance graph problem; finite palette systems are neutral at `k = 6`; porosity /
content / density bounds on `L` cannot give `(W)`; recolouring the `k >= 7` gadget is circular).

## 6. Independent scrutiny: does far-field decoupling give a no-go for proper colourings?

**No, and it cannot.** Four reasons, in decreasing strength.

1. **Insensitivity is not impossibility.** FF-D says an invariant is *unchanged* by a perturbation
   class; it constrains neither the value of `P_x` on the proper sublattice nor whether `L` can
   accumulate. A no-go needs a perturbation *within* the class of proper 6-colourings, and FF-D's
   class is all measurable colourings.
2. **The perturbation class used by FF-C2 breaks properness.** A recolouring supported in
   `B(x,1-eps)` with `1-eps > 1/2` contains pairs at distance exactly 1, so an arbitrary recolouring
   of it is not proper; only a *proper 6-colouring of the disk compatible with the outside on the
   unit shell* is admissible, and whether one exists is not known. So FF-C2's freedom is a freedom
   over non-proper colourings — precisely the freedom `m3` uses, because its gadget has radius
   `1/100` and therefore **contains no unit pair at all**.
3. **The properness obligation reappears as a palette-resource count, where it bites.** For `m3` the
   internal properness of the gadget is free and the entire cost is the shell condition: the gadget's
   cycle labels `{0,2,3}` must be avoided by the annulus colours `{1,4,5,6}`. That is a count of
   available labels — four at `k >= 7`, three at `k = 6` (`m11`: ternary palettes, at most half the
   circle; no two ternary palettes at unit distance in the same direction). So the `k = 6` obstruction
   is quantitative-chromatic, not decoupling-theoretic.
4. **A no-go from palette axioms alone would decide the problem; a colouring-level no-go is not
   excluded.** By `m10` T3 ((A1) trace + (A2) two-centre disjointness ⟹ properness), any
   inconsistency derivable from the *palette axioms* would prove `chi(R^2) > 6`, so that route is
   closed. This does **not** say that no colouring-level no-go can exist: no-gos that use the
   colouring beyond its palette axioms do exist and are the useful ones here — LD-D (self-avoidance,
   from density-one types), `m12`'s Theorem 3 (every pair-valued model is impossible as the maximal
   palette field of *any* weak measurable 6-colouring, from Lemma 5.2(2), no properness needed), and
   Theorem 3 of `m4` (§10 below). The correct scope of FF-D/FF-C2 is therefore narrower than
   "methodological": they forbid **arguments that read the near field `Gamma_x` off the far field
   `P_x` at one centre**, and nothing more. (I withdraw the stronger phrasing "never which
   colourings are impossible".)

**One asymmetry worth keeping** (my addition, not in FF): the implication that does exist runs the
other way. LD-D derives a *far-field* constraint (`i notin P_x(e)`) from a *near-field* density
hypothesis at `x`. So the faithful summary of FF-C2 is "`P_x` does not determine `Gamma_x`", not "`P`
and `Gamma` are independent": near-field density information does constrain the palette.

## 7. What remains open (exact list)

1. `(W)`: is there a weak measurable 6-colouring and a ball of radius `> 1` containing finitely many
   cyclic centres? Not proved, not refuted, and no weaker sufficient geometric condition is known
   (Prop. 3(iv),(v) remove `(Iso)` and `(LF)` as substitutes; LED R6 removes content/porosity bounds).
2. `(W2)` is strictly stronger than `(W)` and open for the same reason; it is *not* the target.
3. `(W3)` (§10, Lemma R3\*): in `S_1` at `k = 6`, does some ball of radius `> 1` contain finitely
   many 3-cycle centres? Exactly equivalent to `(W)` inside `S_1`; not implied by anything in the
   record. Its three supporting inputs (I1)-(I3) are now checked against the paper; all three need
   `c in S_1`.
6. **(G2)** With `(W)` granted, no `k = 6` replacement for §8 exists (strip layer SAT for `k >= 6`,
   every `ell`), so the §7 route stops at Prop. 7.1. Both gaps must be quoted together.
4. Whether LD-D's repaired proof survives in Lean: everything in 5.2 is paper-level plus a numerical
   check of the sector geometry (`supervisor/solve-synthesis/checks/sector_lemma.py`), which I did not
   re-run.
5. Nothing here bears on `chi(R^2) = 6` or `= 7`; `6 <= chi(R^2) <= 7` is unchanged and is the only
   machine-checked numeral in the project.

## 8. Files

| file | content |
|---|---|
| this file | corrected map, retractions, consolidation, scrutiny |
| `LEMMA-isolation-window.md` | Props. 1-2 with the open-ball convention, and the two lattice examples |
| `checks/constants.py`, `supervisor_checks.out` | [A] all arithmetic quoted above, sections [1]-[7] |


## 9. Chain audit: the §7 hypotheses at k = 6, enumerated, with the eps-after-rho ordering

Read against `results/COMPRESSED-PROOF.md` §7, paper Lemmas 7.2-7.8, and `m12` Lemma 5.1. No step
below says "runs verbatim"; each input is named and its `k`-dependence stated.

**P1.** `c` weak measurable 6-colouring (paper Def. 1.2; Lean `WeakColoring`). Used only through
Lemma 4.3 (full-density-point sets are disjoint, conull, contain no unit pair). `k`-independent. [S]

**P2.** Palette/transition axioms: (5.2), (5.3) with Remark 5.3, (5.7), Lemmas 5.2, 5.5, 6.2, Def.
6.1, Fourier decay (6.3) of circle measure. `k`-independent. **Caveat that must travel with any
citation:** (5.3) is used at centre distances equal to `1` (Lemma 6.7) and below `1/2` (Lemma 5.5),
whereas the sprint's SAT countermodels satisfy it only for distances `<= d_0 = pi/(9m)`; quote (5.3)
in its global form or not at all (`smwfwznwk/m4` §1). [P]

**P3.** `alpha in (0,1/6)`: the denominator of (7.4) is `sum_l (p_l - alpha)_+ >= 1 - 6 alpha > 0`.
Needs `alpha < 1/6` (at `k = 5` it is `1/5`). [P]

**P4.** `G = K_6`, the one-skeleton of `Delta([6])`; a simple cycle in `K_6` has `ell in {3,4,5,6}`
(Lemma 7.7 produces a simple cycle in the reduced circuit). [P]

**P5.** `L` closed. From `E_ij` closed and finitely many cycles; `k`-independent. [P]

**P6.** `(W_R)`: `exists y, R > 1, |L ∩ B(y,R)| < infinity`. Open (§4).

**P7. Region and the ordering of rho and eps (the correction).** Fix `rho` with `1 < rho < R`
(possible because `R > 1`), drop the finitely many radii with `L ∩ ∂B(y,rho) != empty` (§1
Consequence 1), and set `Q = B̄(y,rho)`, `inradius(Q) = rho`. The cover produced by Lemmas 7.4/7.6
at precision `eps_n` has `mesh_n <= 1 + eta_n`, where `eta_n -> 0` as `n -> infinity` and `eta_n`
depends only on the `L^1` approximation `p^{eps_n} -> a_i` on the compact `Q`, on `alpha`, and on
the total core-disk/marked-disk radius — not on `k`, not on `Q`'s size. **Then choose `n` with
`eta_n < rho - 1`,** so `mesh_n < rho = inradius(Q)` and the inradius form of the cover obstruction
applies. Writing `rho > 1 >= mesh` is meaningless: there is no `eps` at which the mesh equals `1`.
[P]

**P8.** `L_0 = L ∩ Q` is finite (P6) and non-empty. Non-emptiness is the density theorem, itself an
instance of the same machinery with `L_0 = empty`; the mild circularity is harmless (a separate
instance), but it should be stated rather than assumed. [C]

**P9. Local pasting (Lemma 7.4 part 3), full hypotheses.** (a) pairwise disjoint closed disks, one
core disk per point of `L_0`, total radius `|L_0| delta_n -> 0` — needs `|L_0| < infinity` (P6);
(b) `Gamma_z` acyclic for `z` outside the core disks — the definition of `L`; (c) a finite forest is
contractible, so a boundary loop whose image lies in one component tree extends over its disk
(the loop's image must lie in a *single* component; that is what the marked disks enforce);
(d) finitely many marked disks per `n`, total radius `-> 0`, from Lemma 7.3 applied to each nonedge
of `K_6` (15 nonedges at most, `k`-independent). [P]

**P10.** Multiplicity `<= 2` for the component cover of `Q`: `tilde g_n` takes values in the
one-skeleton, so at most two barycentric coordinates are positive. `k`-independent. [P]

**P11.** Lemmas 7.7 and 7.8 for a finite connected simple graph; `K_6` qualifies. [P]

**P12. Where the chain stops.** Prop. 7.1 at `k = 6` yields `ell in {3,4,5,6}` and the exclusion
continua; the printed §8 then excludes `ell in {3,4,5}` **at `k = 5` only** — the strip layer is SAT
for every `k >= 6` and every `ell` (LED R2, `m6`). So even with P6 granted the chain does **not**
close: `(W_R)` is necessary for this route and not sufficient. Two independent gaps, and they are
often conflated: **(G1)** `(W_R)` unproved; **(G2)** no `k = 6` replacement for §8, for any `ell`.
Both must be recorded whenever §7 at `k = 6` is cited.

## 10. Audit of ledger R3 (the `S_1` singleton-class reduction), and the exact residual lemma

R3's source is `.ultramath/smwfwi7rh/m4/NOTE.md` Theorem 3 (not `smwfo9zkl/m4`). The three inputs,
checked here against `supervisor/solve-geometry/.scratch/paper.txt`:

* **(I1) no 6-cycle.** Uses paper Lemma 6.2 via "Lemma 3" of `sprint/k6/STRUCTURE.md`: a singleton
  palette `{b}` at a centre whose `Gamma_x` contains a cycle `C` satisfies `b notin V(C)`. For a
  6-cycle `V(C) = [6]`, so no singleton value is admissible. ✔ Sound. **Needs `S_1`**: outside it a
  2-element palette in a non-edge is allowed by (6.2) — a 6-cycle has 6 edges among the 15 pairs, so
  9 pairs are permitted [A]. So (I1) does not extend beyond `S_1` by these axioms.
* **(I2) no 5-cycle.** Lemma 3 forces `P_x(e) = {X}` a.e. (`X` the unique outsider), and (5.7) gives
  `{X} ∩ {X} = empty`. ✔ Sound (the rotation `R` preserves null sets). **Needs `S_1`.**
* **(I3) 4-cycle locus locally finite.** Lemma 3 gives `P_x(e) in {{X},{Y}}`; so
  `P_x(e) ∩ {X,Y} != empty` a.e., which is the paper's definition of *binary for the pair* (paper
  §5.3: "`P_x(e) ∩ {i+,i-} != empty` for a.e. `e`" — the weaker of the two readings, so no
  alternation is needed for the hypothesis, though Lemma 5.5 derives it internally). Lemma 5.5 is
  `k`-uniform as stated: "an absolute constant `delta_* > 0` such that, **for every fixed pair of
  labels**, any two distinct centers binary for that pair are at distance at least `delta_*`". The
  labelled 4-cycles number `C(6,4)·3 = 45` [A]. ✔ Sound. **Needs `S_1`**: outside it Lemma 3 permits
  11 of the 15 pairs, e.g. `{0,2}` for the 4-cycle `0-1-2-3`, which meets no complement label, so
  binarity fails and Lemma 5.5 gives nothing [A].

So all three inputs check out, and **all three need the `S_1` restriction**. Two scope corrections
to the ledger: (a) R3 is a reduction *inside* `S_1`, not of `(W)` as such; outside `S_1` the 5-, 6-
and 4-cycle loci are not controlled by the cited axioms, and `m12`'s Theorem 3 shows that palette
*models* with pair values are impossible as palettes of 6-colourings, which is a different (and
complementary) statement. (b) "m3 Lemma 1 shows `(W)` holds in the tame class at every `k`" does not
make `S_1` harmless: `S_1` is much larger than the tame class, and it is where a wild 6-colouring
would live.

**Lemma R3\* (exact residual lemma; proved here).** *Let `c` be a weak measurable 6-colouring in
`S_1`, and let `T = {x : Gamma_x contains a 3-cycle}`. Then for every ball `B`:*
`|L ∩ B| < infinity` **iff** `|T ∩ B| < infinity`. *In particular*
`(W)` ⟺ `(W3)`: `exists y, R > 1, |T ∩ B(y,R)| < infinity`.

*Proof.* `L` is the union of the 3-, 4-, 5- and 6-cycle loci over the finitely many simple cycles in
`K_6` (20, 45, 72, 60 undirected cycle types [A]; only 20+45 appear as loci here). By (I1), (I2) the
5- and 6-cycle loci are empty; by (I3) the 4-cycle locus is locally finite, hence finite in every
bounded set. So `L ∩ B = (T ∩ B) ∪ (finite set)`, and the two finiteness conditions agree. `square`

**What Lemma R3\* does and does not buy.** It converts P6 into a statement about *one* cycle length in
`S_1`, which is the sharpest known reduction of `(W)`; it is an equivalence, so it loses nothing.
It does **not** prove `(W3)`, and it does not touch (G2). Residual target, exactly: *in `S_1` at
`k = 6`, some ball of radius `> 1` contains finitely many 3-cycle centres* — with the three-cycle
structure at `k = 6` constrained by (6.2) on three edges, (5.7), Lemma 5.5's binarity for the
complement pair of the triangle (`k - 3 = 3` outsiders) and `m11`'s ternary bound.

**Minimal failure mode if `S_1` is dropped.** No colouring counterexample is available at `k = 6`
(the class is empty unless `chi(R^2) <= 6`). The finite obstruction is label-theoretic and exact:
at a 6-cycle centre (6.2) permits 9 of the 15 pairs, and at a 4-cycle centre 11 of the 15, so
nothing in Lemmas 5.5/6.2 forces binarity there. Hence (I1)-(I3) cannot be extended past `S_1` by
the paper's palette axioms, and any use of R3 must carry the hypothesis `c in S_1` explicitly.
