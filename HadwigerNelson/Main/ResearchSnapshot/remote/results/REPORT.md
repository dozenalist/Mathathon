# Hadwiger–Nelson: verification, sharpening, and why the method stops at five

**What this session did.** Three resources were combined: the standing problem statement, the
62-page proof that the plane is not five-colourable (OpenAI, 23 Sep 2026), and its 78-module Lean
development. The theorem was machine-verified in this VM; two strengthenings and two small
structural lemmas were proved and formalised; the exact point where the method fails for six
colours was isolated; and five reported "errata" were shown to be artifacts of text extraction.
The value `chi(R^2)` remains 6 or 7: this session does not settle it, and §6 says precisely what
would be needed.

---

## 1. The state of the art, as established by the sources

The paper proves **Theorem 1.1**: every colouring of the Euclidean plane with five colours has a
monochromatic unit-distance pair, with no regularity assumption on the colour classes. Hence
`6 <= chi(R^2)`, and the classical hexagonal colouring gives `chi(R^2) <= 7`.

Its architecture is a two-stage argument.

* **A transfer theorem (Theorem 1.3, every `k`, ZFC).** A proper `k`-colouring of the plane exists
  if and only if a *weak measurable* `k`-colouring exists (measurable, with the set of monochromatic
  unit pairs of product measure zero). The forward direction is Proposition 4.2: take the invariant
  law on proper labellings of the algebraic plane, project the label indicators onto the continuous
  part of the Koopman representation, use Haar rigidity (Theorem 2.3) to kill the orthogonal part,
  and select a measurable sample. The converse is density points plus compactness.
* **A measurable obstruction (Theorem 1.4, five labels only).** No weak measurable 5-colouring
  exists. Palettes have at most two labels (Proposition 5.6); disk smoothing produces continuous
  maps into the one-skeleton of `K_5`; a planar cover obstruction produces a cycle of common
  exclusion continua; and cycles of length 3, 4 and 5 are each impossible.

`results/SPINE.md` gives the twelve load-bearing steps with the corresponding Lean modules.

## 2. Machine verification (this VM)

The bundle targets Lean 4.34.1 and mathlib `d13f23b`. The VM default is 4.33.1, under which 47
modules fail with ordinary API drift. Rather than port backwards, the exact environment was fetched
and cached (`scripts/fetch_exact_env.sh`), and the development compiled **78/78 modules, zero
patches**, in topological order.

```
source scripts/env4341.sh && lean results/lean/Check3.lean
```

reports, for both main theorems and for every theorem added below,

```
[propext, Classical.choice, Quot.sound]
```

with no `sorry`, `axiom`, `native_decide`, `@[implemented_by]` or `opaque` anywhere in the 78
modules. Details: `results/VERIFICATION.md`.

Statement fidelity was checked against the paper's own definitions (and independently by a swarm
member, who machine-checked that the Lean `WeakColoring` is *equivalent* to the paper's iterated
integral form, `results/lean/Def12.lean`). `ProperColoring` quantifies over all pairs at distance
one with no regularity. `no_proper_five_coloring` is the paper's Theorem 1.1.

## 3. New results proved and formalised here

### T1. The chromatic number of the plane is the chromatic number of the algebraic plane.

Let `E = algebraicClosure(Q, C)`, a countable dense subfield of `C`, with its unit-distance graph.
Then for every `k >= 1`: `E` is `k`-colourable iff `C` is `k`-colourable. Consequently
`6 <= chi(E) = chi(C) <= 7`, and by de Bruijn–Erdős any finite witness of `chi >= 6` can be taken
with algebraic coordinates.

The proof is a one-line observation about Proposition 4.2 — its first line is "restrict the given
colouring to `E`", the compact space of labellings is a space of labellings of `E`, and the
character group is the dual of `E^disc` — so the hypothesis can be weakened from the plane to `E`.
Everything else is the paper's. Formalised: `BorelTransfer.lean` (`proper_to_borel_weak_algebraic`),
`Five.lean` (`no_proper_five_coloring_algebraic`), and `Transfer.lean`
(`algebraic_colorable_iff`). Full statement: `results/T1-algebraic-plane.md`.

### T2. The lower bound survives deleting any null set.

For every Lebesgue-null `Z ⊆ C`, the graph on `C \ Z` has no proper 5-colouring:

```
not_proper_five_coloring_compl_null : volume Z = 0 → ¬ ∃ c, ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y
```

The proof uses the finite characterisation of colourability: every finite configuration can be
translated off `Z`, since the bad translations form a finite union of null sets; compactness then
produces a 5-colouring of the plane, contradicting Theorem 1.1. Formalised in `NullSetRobust.lean`;
statement and consequences in `results/T2-null-sets.md`.

### The connected-set exclusion, isolated.

The paper's Proposition 7.1 asserts that both endpoint labels of an edge are absent from
`Delta(K) = {z : min_{q in K} |z - q| < 1 < max_{q in K} |z - q|}`. That is exactly the statement
that a connected set containing no point at unit distance from `z` cannot straddle the unit circle
about `z`. Formalised, in a general normed space, in `ConnectedUnitFree.lean`:

```
diam_le_one_of_preconnected_unitFree  : IsPreconnected C → (∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ ≠ 1) → ∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ ≤ 1
not_straddle_of_isPreconnected       : IsPreconnected C → (∀ q ∈ C, ‖z - q‖ ≠ 1) → ¬ ((∃ q ∈ C, ‖z - q‖ < 1) ∧ ∃ q ∈ C, 1 < ‖z - q‖)
```

No planarity, compactness or measure theory enters. This also gives the sharpness that makes the
a.e. formulation necessary: an open disc of radius `1/2` is connected, unit-free, and has diameter
exactly `1`.

### The paper's displayed inequality `6 <= chi <= 7`, formalised.

The bundle proves the two endpoint facts but never states the numerical consequence. It is now
`OAI.Problem160.chromaticNumber_bounds : 6 ≤ planeChromaticNumber ∧ planeChromaticNumber ≤ 7`
(contributed by a swarm member, integrated as `Chromatic.lean`, transported along an explicit
isometry `C ≃ Plane`).

## 4. Where the method stops: the six-colour barrier

**The printed argument cannot give `chi >= 7`.** It is a `k <= 5` argument, and there are three
independent `k`-dependent steps (analysis in `results/K6-BARRIER.md`, from a swarm member's audit
plus my own check of the first):

1. **Palette cardinality.** For general `k`, the proof of Proposition 5.6 gives only
   `|P_x(e)| <= k − 3`: the argument takes a fixed `(k−2)`-set `A` in the palette, observes that the
   complementary set `B = I \ A` has two elements, and uses binary-centre separation. At `k = 6`
   this gives `|P_x(e)| <= 3`, and `3` is not excluded: a circle of radius one is 2-colourable, so a
   centre whose circle uses three labels is consistent. With three positive coordinates the
   smoothed map lands in the two-skeleton, and the cover obstruction of Lemma 7.5 — multiplicity at
   most two and mesh at most two — no longer applies (fine covers have multiplicity one).
2. **Triangle interfaces.** At a length-three interface the outside state satisfies
   `1 <= |A(e)| <= k − 4`, a singleton exactly when `k = 5`; at `k = 6` it can be a pair.
3. **A new cycle length.** Proposition 7.1 produces a simple cycle of length `3 <= ℓ <= k`; at
   `k = 6` there is a length-six case for which the paper has no argument.

A proof of `chi >= 7` along these lines therefore needs at least one genuinely new idea:
a palette bound of two for six colours, or a multiplicity-three replacement for the planar cover
obstruction, or an exclusion of six-cycles together with the six-colour state analysis.

**What `chi <= 6` would need** is an actual proper 6-colouring. By T1 it is enough to colour the
countable algebraic plane `E`, but `E` is exactly the graph on which the transfer and the rigidity
theorem operate, so no measurability, periodicity or density shortcut is available; and the
structural no-go results below rule out all the classical candidates (lattice, stripe, radial,
definable, finite-component).

## 5. What the swarm established

Twelve members worked twelve directions. All twelve submissions were accepted after checking
(one after a rejection and resubmission):

* **Statement fidelity and axiom certificate** (m1): 27 declarations checked, the
  `WeakColoring ≡ Definition 1.2` equivalence machine-checked, the chromatic-number bounds
  formalised, the upper-bound constants verified in integer arithmetic.
* **The finite certificate of §8.5–8.6, machine-checked** (m6): seven exact points in `Q(√3,√11)`,
  exactly eleven unit edges, no other unit pair, pairwise distinct, not 3-colourable, and placed in
  the region (8.4) — `OAI_Audit_Moser.lean`, compiled here.
* **The k = 6 barrier** (m2): the general palette bound `k − 3` proved; the triangle-interface
  bound `k − 4`; constraint-level certificates showing the printed constraints are satisfiable at
  `k = 6`; the new `ℓ = 6` case identified.
* **A named black box eliminated** (m7): a complete, self-contained proof of the measurable
  fibre-orthonormal-basis selection that the paper's Lemma 3.1 asserts in one sentence.
* **Structured-substitute no-go theorems** (m10): connected unit-free sets have diameter `<= 1`
  (hence no class contains a line, ray, unbounded connected set or ball of radius `> 1/2`); no
  colouring factors through connected unbounded fibres; no radial colouring; and the sharp angular
  bound `sigma(A) <= 1/2` for measurable unit-independent subsets of the circle, attained by three
  half-open arcs — which places the paper's footnote-1 counterexample (measure `pi/3`) as
  non-extremal.
* **A port to the VM's stock toolchain** (m8): all 83 modules, including the five added here,
  compile under Lean 4.33.1 + the installed Mathlib (38 files, 109 hunks, whole run 5 min 10 s,
  reproduced here). No declaration line is altered; the three added lemmas are needed because
  `Filter.EventuallyConst` is a `Subsingleton` predicate in this Mathlib.
* **A referee-checkable compression of the whole paper** (m4): every lemma restated in the form its
  use consumes, complete proofs of the transfer and the rigidity chain, the assembly and dependency
  DAG, an explicit list of the steps the compression accepts, and expanded proofs of the two terse
  steps. Kept as `results/COMPRESSED-PROOF.md`. Its glyph-coordinate reconstruction of the p. 32
  display is independently confirmed here.
* **Deletion stability of the lower bound** (m9): `chi(C \ Z) = chi(C)` for every `Z` that is null,
  meagre, of cardinality `< c`, of finite outer measure, or contained in a closed half-plane.
  Machine-checked (`Robust.lean`, 20 declarations, compiled here, axioms clean). This contains T2
  and is the definitive form: a 5-colourable set must have complement non-null, non-meagre, of
  cardinality `c`, of infinite outer measure and not contained in a half-plane.
* **A no-go for the hexagonal family at six colours** (m12): the hexagonal-cell construction, at any
  spacing and with any tie-breaking, cannot be 6-colourable: three explicit exact 7-cliques give
  `d`-windows, the coset inequality `M(k)^2 > 16/3` with `M(6)^2 = 4 < 16/3` settles every coset
  colouring, and solver certificates cover the remaining windows. Correctly scoped as a statement
  about the family, not about `chi(R^2)`.
* **The §7 cover obstruction, sharpened** (m3): a complete elementary proof (no Brouwer, no measure
  theory) that a relatively open cover of `B(y,R)` of multiplicity at most two has
  `sup diam U_i >= R`. This relaxes the mesh constant in Lemma 7.5, in
  `PlanarCover.compact_open_cover_impossible` and in `graph_map_large_positive` from `2` to any
  `d < 5`, and shows the §7 step is blind to the number of labels: the k = 6 failure is upstream,
  at the palette bound, not in the cover lemma.
* **The ground-field spectrum** (m5): a parity lemma showing that rational unit vectors summing to
  zero are even in number, hence `chi(Q^2) = 2`; an independent proof of T1 by Tarski–Seidenberg
  (finite realizations descend to algebraic coordinates) and the sharper statement that
  `chi(R^2) = max{chi(F^2) : F a number field}`, attained; and an explicit ladder
  `chi(Q^2)=2`, `chi(Q(√3)^2) >= 3`, `chi(Q(√11)^2) >= 3`, `chi(Q(√3,√11)^2) >= 4` (Moser),
  `chi(F^2) <= 7` for `F ∋ √3`. This shows the lower bound rests neither on density nor on
  completeness but on real-closedness.
* **Explicit constants** (m11): `delta_3 = 1/11` for the three-colour analogue of Corollary 1.5,
  from the eleven-edge Moser graph; the structural point that any explicit `delta` at `k = 5`
  presupposes an explicit finite witness; and a claimed effectivisation `delta_* = 1/100` of
  Lemma 5.5, numerically validated here but whose analytic proof was not checked line by line.

## 6. Referee notes: the paper has no formula-level errors of the kind reported

Five separate "errata" were reported during the audit, and all five are artifacts of `pdftotext`,
which drops fractions, superscripts, radicals and large delimiters in this PDF. Each was checked
against a rendered image of the page: the seven-colouring really takes `r = 2/5` (not `sqrt(2/5)`);
Lemma 5.5's display really contains the factor `1/2`; `a(h)` really denotes the `L^2` norm so that
the pair criterion gives `Avg a(h)^2 -> 0`; display (8.6) really has the large parentheses; and
Lemma 8.6's "still smaller ball" really supplies the uniform neighbourhood. Details:
`results/ERRATA-TRIAGE.md`. The lesson is procedural: a claimed erratum in displayed mathematics
must be checked against the rendered page.

## 7. What remains open, stated plainly

`chi(R^2) ∈ {6, 7}`. This session did not decide which, and neither the paper nor the method
decides it.

* To prove `chi = 7` one needs a finite unit-distance graph that is not 6-colourable, or a new
  argument that no 6-colouring exists. §4 shows that the existing architecture cannot supply the
  latter without a new idea.
* To prove `chi = 6` one needs an explicit proper 6-colouring, and §5's structural results say what
  it cannot look like.
* A finite witness of `chi >= 6` exists by compactness and can be taken with algebraic coordinates
  (T1), but it is not explicit; making it explicit would be a substantial result in its own right.

## 8. Deliverables

| file | contents |
|---|---|
| `results/VERIFICATION.md` | environment, build, axiom certificate, fidelity, new modules |
| `results/SPINE.md` | the proof in twelve steps, with Lean modules |
| `results/T1-algebraic-plane.md` | T1, with proof and formalisation |
| `results/T2-null-sets.md` | T2, with proof and consequences |
| `results/K6-BARRIER.md` | the exact `k = 6` failures |
| `results/ERRATA-TRIAGE.md` | the five artifacts and the machine-checked finite core |
| `results/COMPRESSED-PROOF.md` | a referee-checkable compression of the 62-page proof (swarm member m4) |
| `lean/OAI/Geometry/PlaneColoring/{Converse,Transfer,Chromatic,NullSetRobust,ConnectedUnitFree}.lean` | new Lean modules |
| `results/lean/Check*.lean`, `Def12.lean`, `ChromaticNumber.lean` | axiom-check drivers |
| `scripts/{fetch_exact_env.sh,env4341.sh,build_lean.py}` | reproducible build |
