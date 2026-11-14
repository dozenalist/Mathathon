# Step 2 audit + the Step-1 no-go: two certifications from direction d5

**Step 1 headline (this run, §Appendix).** The tightened interface CSP (C1)–(C5) at `k = 6` is
satisfiable, and the tightening (C4)+(C5) is *vacuous*: for every `ℓ ∈ {3,4,5,6}` and every one of
the `6^ℓ` sign words the system with (C1)–(C3) and the system with (C1)–(C5) are satisfiable
together, and the tightened counts equal the previous run's untightened counts exactly
(36/36, 216/216, 225/1296, 177/7776 up to rotation). Hence there is no UNSAT certificate, this
route cannot prove `chi(R²) ≥ 7`, and the INDUCTION LEMMA is moot for the lower bound.

**Step 2 headline (§0–§6).** In the Lean development the forward half of the transfer costs
32 modules / 16 006 lines, of which 15 096 (94.3%) are the rigidity theorem alone, consumed through
one lemma at one site; and route (a) (the palette equivalence) is circular, provably.

Direction d5 of swarm `smwfk0ybk`. Object of study: paper Theorem 1.3 (transfer of colourability),
`attachments/here-are-three-files-ni5n/paper.pdf`, and its Lean counterpart `lean/OAI/**`.
Everything below is either a measurement (recomputable, §2), a definition read off the paper
(§1), or a proof written out (§3). Nothing is quoted from another member.

---

## 0. Summary

1. **Where the cost is.** In the Lean development the forward half of the transfer
   (Proposition 4.2) has a transitive dependency closure of **32 modules / 16 006 lines**.
   **15 096 of those lines (94.3%), in 29 modules, are reachable only through
   `OAI.Analysis.PlaneSpectrum.Ergodicity`** — the Lean home of the paper's Theorem 2.3
   (rigidity of wild character laws, paper §2–§3). The transfer itself, with the plane and
   algebraic-vector input, is **3 modules / 910 lines**. The backward half (Lemma 4.3 plus
   graph compactness) costs 5 853 lines. So Step 2 is *not* a question about a 62-page proof:
   it is a question about one theorem.
2. **The interface is one lemma, used once.** The forward transfer consumes the heavy layer
   through exactly one Lean lemma, `PlaneFiveColor.Spectral.residual_fourier`, applied at
   exactly one site (`BorelTransfer.lean:61`). §2.3 shows that this lemma cannot be weakened
   on the class where it is used, so route (e) has no interface-saving move; a shorter transfer
   requires a shorter proof of the rigidity.
3. **Route (a) is circular, provably.** A *jointly measurable* palette field satisfying
   (H1)+(H2) at `k` yields a weak measurable `k`-colouring (§3, Theorem A-meas): the palette
   collapse delivers the transfer's *conclusion* from a palette field, and *no analysis at all*
   enters the proof. But the palettes of a colouring are defined (paper Definition 5.1) from
   circle averages of the colour-class indicators, so the field is available only after the
   colouring is Lebesgue measurable. Route (a) therefore asks for exactly the step that is
   missing. The rigidity theorem's whole job is to manufacture that measurability from an
   invariant law.
4. Routes (b), (c), (d) have no purchase; each is refuted below by a specific reason, and §4
   gives two *positive* structural facts that show why: any admissible countable base group
   must contain the algebraic units `K` (otherwise the zero-correlation identity cannot be
   extended from the averaging group to `S¹` by density) and an isometric copy of every finite
   unit-distance configuration (otherwise a colouring of it says nothing about the plane). Then
   `C ≅ R²` is a *proper dense* Borel subgroup of the compact dual `D` — so "wild" laws exist and
   `Haar` is one of them — and the divisibility of `K` is exactly what makes the `K`-action on
   `(D, Haar)` ergodic, so `K` cannot be replaced by a smaller unit group (the units of `Z[i]`,
   for instance, have finite orbits and the action degenerates).

**Class of the no-go.** This note delimits *the printed architecture* (Følner average →
conditional expectation onto the continuous spectral factor → measurable sample). It does **not**
prove that no shorter proof of Theorem 1.3 exists, and it does not claim a new proof. What it
does give is: the exact cost, the exact interface, one new lemma (Theorem A-meas), and four
falsification tests that were run and failed.

---

## 1. The object, and what each step uses

**Definition 1.2 (paper).** A *weak measurable `k`-colouring* is a Lebesgue measurable
`c : R² → {1,…,k}` with, for every `R > 0`,

  ∑_{i=1..k} ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0.

**Theorem 1.3 (paper).** A proper `k`-colouring exists ⇔ a weak measurable one does, every `k`.

The forward direction is Proposition 4.2. Its five steps, with what each consumes:

| step | content | cost |
|---|---|---|
| (i) | restrict the colouring to `E`, Følner-average translates and rotations: an invariant Borel probability `μ` on the compact set `Ω ⊆ {1..k}^E` of proper labelings | amenability of `E ⋊ K`; cheap |
| (ii) | (4.1): `∫ f_i T_u f_i dμ = 0` for `u ∈ K` | properness only |
| (iii) | Lemma 4.1: `H_c = {v : T_z v → v}` is `L²` of a factor; projection is conditional expectation; the `R²`-representation extends strongly continuously | spectral theorem for `E_disc` + Bochner; self-contained, no FZ |
| (iv) | **Theorem 2.3**: the scalar spectral measure of `b_i = f_i − E(f_i|F_c)` is `K`-invariant and `C`-null, hence a multiple of Haar, hence `⟨b_i, T_z b_i⟩ = 0` for `z ≠ 0` | **the whole of paper §2–§3: compact tower (Lemma 3.1), relative singularity (Lemma 2.7), conditional multiple averages (Lemma 3.2), radial difference inequality (Lemma 3.3), number-field lemmas (3.4, 3.5)** |
| (v) | jointly measurable field in `x`, one sample, least positive label; then `H_c` has `L²`-continuous translation orbits so the identity extends from `K` to `S¹` by density | Fubini/Tonelli, a diagonal over a countable exhaustion; cheap |

So (i), (ii), (iii), (v) are elementary or standard; **all of the difficulty is (iv)**, and (iv)
is used only to conclude `⟨b_i, T_u b_i⟩ = 0` at algebraic unit directions `u`.

---

## 2. Measurement in the Lean development

Check: `python3 .ultramath/smwfk0ybk/m5/closure_measure.py` (reads `lean/OAI/**/*.lean`, builds
the import graph, prints the table below; 60 ms).

```
83 modules, 31360 lines
forward transfer (Prop 4.2):      32 modules, 16006 lines   [PlaneColoring.BorelTransfer]
backward transfer (Lemma 4.3):    17 modules,  5853 lines   [PlaneColoring.Converse]
Theorem 1.3 (both):               49 modules, 21862 lines   [PlaneColoring.Transfer]

reachable ONLY through Analysis.PlaneSpectrum.Ergodicity: 29 modules, 15096 lines = 94.3%
transfer proper (everything else):                         3 modules,   910 lines
```

The 15 096 lines split as 7 354 in `Analysis/PlaneSpectrum` (spectral measures, invariant means,
number fields, phase collision, radial energy, small arcs, multipliers) and 7 742 in
`MeasureTheory/CompactFactors` (the Furstenberg–Zimmer layer: kernels, relative products,
relative centers, conditional limits, stationary factors, amenability).

### 2.1 The single interface

The only occurrence of the heavy layer outside its own module is

```
OAI.Geometry.PlaneColoring.BorelTransfer:61
  have hb := residual_fourier (representation k ω) (rotation k ω) (rotation_covariance k ω) …
```

with the lemma (`Analysis/PlaneSpectrum/Ergodicity.lean:403`)

```
lemma residual_fourier (v : H) (hv : v ∈ (ContinuousVectors.space U)ᗮ)
    (hfix : ∀ k, (W k : H →L[ℂ] H) v = v) (z : E) (hz : z ≠ 0) :
    ⟪v, ContinuousVectors.op U z v⟫_ℂ = 0
```

proved as `finite_wild_fourier (measure (calculus U) v) …` ← `wild_fourier` ← conditional
ergodic fibres ← `ergodic_wild_fourier` ← the tower.

### 2.2 The consumed statement is the paper's Theorem 2.3, not a weaker corollary

The paper states Theorem 2.3 as "wild ⇒ Haar". Prop 4.2 uses only "coefficients vanish at
nonzero `z`", and that is *equivalent*: a probability on the compact abelian `D` whose
nontrivial Fourier coefficients all vanish is Haar (the characters of `D` are `E`, they form a
conjugation-closed unital algebra separating points, so Stone–Weierstrass gives uniqueness of
the coefficients). So nothing is spent in passing between the two forms.

### 2.3 No interface narrowing exists (why route (e) cannot save lines)

One might hope to need `residual_fourier` only at `z = 1`. On the class used it is *equivalent*:
if `v` is rotation-fixed then `⟨v, T_{uz}v⟩ = ⟨v, T_z v⟩` for every `u ∈ K` (apply unitarity of
`W u` and the covariance `(W u)(op U z w) = op U (kCoeff u * z)((W u)w)`), and `K` acts
transitively on the algebraic vectors of each modulus. So the `z = 1` instance gives all
`z ∈ K`, and conversely. Hence the interface cannot be made smaller by weakening its statement;
only a shorter proof of it helps. (`hfix` is available: `projected_rotation_fixed`.)

---

## 3. Route (a): the palette collapse is circular — and what it shows the rigidity is *for*

Recall (m8, `smwfhd5sl/m8/l4_obstruction.md`, Theorem A): palette systems at `k` — a field
`P_x(e) ⊆ {1..k}` with (H1) `1 ≤ |P_x(e)| ≤ k−3` for a.e. `e` and (H2) the paper's transport
exclusion (5.3) — exist iff `chi(R²) ≤ k`. The `⇒` direction selects one label per palette
(choice for a family of finite non-empty sets indexed by a continuum) and uses only the
translation instance of (H2) at unit-distance pairs.

**Theorem A-meas.** Let `P` be a palette system at `k` such that (a) for every `e ∈ S¹` the map
`x ↦ P_x(e)` is Borel, (b) `(x,e) ↦ P_x(e)` is jointly Borel, and (c) (H1) holds for all
centres. Then a weak measurable `k`-colouring exists (Definition 1.2). **No ergodic theory,
no spectral theory, and no rigidity enters the proof.**

*Proof.* For `x ∈ R²` and unit `d` put `N_{x,d} = {e ∈ S¹ : P_x(e) ∩ P_{x+d}(e) ≠ ∅}`. By (H2)
applied to the translation representation `(x+d) + f = x + f + d` (paper Remark 5.3; the
admissible branch is unique by the uniqueness of the pair of unit vectors with a given sum),
`N_{x,d}` is angular-null for every `(x,d)`. By (b) the set `{(x,d,e) : e ∈ N_{x,d}}` is Borel, so
Fubini gives a conull set of `e ∈ S¹` such that `{(x,d) : e ∈ N_{x,d}}` is null. Fix such an `e`;
by (a) and (c), `q(x) := min P_x(e)` is a well-defined Borel function `R² → {1..k}`, and for
almost every `(x,d)` with `|d| = 1` we have `q(x) ≠ q(x+d)`. Fubini in `(x,u) ∈ B(0,R) × S¹`
gives the display of Definition 1.2. ∎

Two consequences, and they are the answer to route (a).

* **The collapse delivers the conclusion from a measurable field.** So a proof of the transfer
  through the palette collapse must first produce a *jointly measurable* palette field from an
  arbitrary proper colouring. That is not available: the palette of paper Definition 5.1 is
  built from weak-\* limits of the circle traces `e ↦ (1_{A_i}(y_n + r_n e))_i` of the colour-class
  indicators, i.e. it presupposes that the classes are measurable ("we choose Borel
  representatives forming a partition"). Hence route (a) reduces the transfer to the transfer.
* **What the rigidity buys, exactly, is measurability in `x`.** Everything else in the transfer
  — the exclusion (H2), the selection, the a.e. conclusion — is elementary (Theorem A-meas,
  Lemma 4.3, compactness). The printed proof manufactures the missing measurability by
  projecting onto the `L²`-continuous spectral factor and then proving that the discarded part
  has no correlations at all; that last point is exactly Theorem 2.3. So the heavy analysis is
  the price of the *loss of regularity*, not of the geometry, and route (a) cannot pay it.

---

## 4. Routes (b), (c), (d): no purchase, with the structural reason

### 4.1 Why the base group cannot be chosen to make the rigidity easy (and why route (b) is not a shortcut)

Two requirements pin the countable group `Λ ⊆ C` on which the averaging is done:

1. **Density extension.** The transfer concludes zero correlations at *every* unit direction
   `u ∈ S¹`, but the averaging only proves them at the unit directions *inside* `Λ`. The passage
   uses that `K` (the algebraic units) is dense in `S¹`. Hence `K ⊆ Λ`.
2. **Plane colourings.** To conclude `chi(R²) ≤ k` from a colouring of `Λ`, every finite
   unit-distance configuration must embed in `Λ`; by Tarski–Seidenberg the configurations can be
   taken with algebraic coordinates (this is exactly R1's mechanism), and the printed proof takes
   `Λ = E` for that reason. Any replacement `Λ` must therefore contain an isometric copy of every
   finite unit-distance configuration; in particular it cannot be finitely generated, and it must
   already carry the whole unit circle `K`.

So `Λ` must contain the algebraic plane `E = F(i)` and its unit circle `K`. Then:

* **`C` is a proper dense Borel subgroup of `D = Λ^`.** `C = j(R²)` is dense because its
  annihilator in `E` is `{0}` (if `ξ·z ∈ 2πZ` for all `z ∈ E` then `ξ = 0`). It is proper: `D` is
  the dual of a countable discrete group, so a character is free on a `Q`-basis of `E`, whereas
  `j(ξ)` is fixed by the two real parameters `ξ`; explicitly, on the `Q`-independent triple
  `1, i, √2 ∈ E`, any character with `d(1) = d(i) = 1` and `d(√2) = e^{2πiα}`, `α ∉ Z`, is not of
  the form `j(ξ)` (such a `d` would force `ξ = 0` and then `d(√2) = 1`). Hence `Haar(C) = 0` — a
  Borel subgroup of positive Haar measure is open, and a dense proper subgroup is not open — i.e.
  **Haar is itself a "wild" law.** So "`ν(C) = 0`" is non-vacuous *and* sharp: it is satisfied by
  the Haar law, and by nothing else (that is the theorem).
* **`K` cannot be shrunk.** `K` is divisible, so every `K`-orbit in `E` is infinite (`K·z` is the
  set of algebraic vectors of modulus `|z|`). Consequently the only `K`-orbit-invariant
  coefficient family `(c_z)_{z∈E} ∈ ℓ²(E)` is `c = c_0 δ_0`, i.e. **Haar is ergodic for the
  `K`-action on `D`** — the fact the rigidity proof needs at its first step ("fix an ergodic
  wild `K`-invariant probability"). A smaller unit group (for instance the units of `Z[i]`) has
  *finite* orbits on its character group, the action is then not ergodic, and the argument stops.

These two facts are the reason the rigidity is a theorem about the *algebraic* dual and not a
general ergodic-theoretic statement, and they are what makes route (b)'s suggestion unavailable:

* The tower of Lemma 3.1 **is** the standard Furstenberg–Zimmer construction of the maximal
  factor over which the system is relatively weakly mixing. Its stopping rule ("`X ×_Y X`
  ergodic") is the definition of that factor, and relative-product ergodicity is what Lemma 3.2
  (conditional multiple averages, applied at exponents `0,1,2`) needs. A "single compact factor"
  is stage 1 of the tower; nothing in the paper, and no general theorem, gives relative product
  ergodicity at stage 1. Reducing the tower to one stage would be a new theorem about `(D, μ)`,
  not a simplification of the printed argument.
* The difference inequality (3.12) is derived through the conditional independence identity
  (3.15) `Avgu m(A − Bu²) → m(A)m(B)`, i.e. from the *relative product* being ergodic. With the
  trivial factor the corresponding statement is a mixing statement for the `K`-action on
  `(D, μ)`, which fails for exactly the compact systems that make `(D, μ)` interesting. So the
  tower is load-bearing in the step that produces (3.12), not decoration.

### 4.2 Route (c) (Tarski–Seidenberg plus measurable selection)

Tarski–Seidenberg is *already* consumed, and completely, at R1: it is what lets a finite witness
be taken with algebraic coordinates, and it is requirement 2 of §4.1. It has no second use here:
the objects the transfer must handle are *arbitrary* colour classes, on which no definability
structure is available, and the conclusion is a regularity statement about such a class. A
definability argument would have to produce a definable object from an arbitrary one first —
which is the averaging step, i.e. the transfer. So route (c) is not a weaker route; it is the
same route with the mechanism renamed.

### 4.3 Route (d) (quasi-tiling, amenability used directly)

Amenability is already used, and it is *cheap*: the whole Følner averaging step of Proposition
4.2 is five lines of the paper and 412 Lean lines (`CompactFactors/Amenability.lean`, of the
15 096). What remains costs 14 684 lines and is not an averaging statement at all: it is
(a) the construction of a relatively weakly mixing factor, (b) a relative singularity argument
along that tower, and (c) a Fourier/arithmetic rigidity argument (number fields, general-position
rotations, an integer-combination bound). Kieffer/Ornstein–Weiss quasi-tiling produces Følner
sets, which the paper already has; it produces no information about character laws on `D`.

---

## 5. Route (e): what a dependency reduction would require

The measurement in §2 answers the question the brief asks route (e) to answer, before and after:

* before: 32 modules / 16 006 lines for the forward transfer; 49 / 21 862 for the whole of
  Theorem 1.3;
* after any of the routes (a)–(d): unchanged (§3, §4);
* after a hypothetical direct proof of the interface lemma: 3 modules / 910 lines for the forward
  transfer, plus whatever that proof costs. By §2.3 the interface cannot be weakened, so the
  saving is exactly "the 15 096 lines minus the cost of a new proof of the rigidity".

The precise statement a shorter proof must establish (paper form): *every `K`-invariant
probability `ν` on the dual of the discrete algebraic plane with `ν(C) = 0` is Haar probability*,
equivalently: its Fourier coefficients vanish at every nonzero `z ∈ E`.

---

## 6. What is not claimed, and the tests that were run

* **Not claimed:** that Theorem 1.3 has no shorter proof; that Theorem 2.3 is indispensable in
  ZFC; any new transfer theorem. The class of the no-go is §0's, and it is not vacuous: the four
  candidate routes are named, and each is killed by a specific statement above, not by prose.
* **Ran and failed (route (a)):** the attempt to derive the transfer from the palette collapse.
  It fails at measurability of the field; Theorem A-meas shows that *that* is the only gap, and
  paper Definition 5.1 shows the gap cannot be closed from the collapse side.
* **Ran and failed (route (b)):** the attempt to use the trivial factor. §4.1 shows the
  conditional-independence identity behind (3.12) has no trivial-factor analogue.
* **Ran and failed (route (e)):** interface narrowing at `z = 1`. §2.3 shows it is an equivalence
  on the class used.
* **Checked, with a negative outcome (recorded so nobody repeats it):** I checked the paper's
  ergodic-decomposition step ("almost every ergodic component is wild; the ergodic case makes
  each Haar") against the possibility that Haar is not `K`-ergodic — which would be a defect in
  Theorem 2.3. It is not: `K` is divisible, its orbits in `E` are infinite, and the only
  invariant `ℓ²` coefficient families are trivial (§4.1). The proof is consistent.
* **Not verified here:** nothing in this note re-derives R1–R6 or the earlier run's results; they
  are cited. The lean measurement is of *imports*, not of proof terms, and line counts are a
  proxy for proof size, not a measure of it.

---

## Appendix: the Step-1 no-go, decided in this run (board findings f3, f32)

**Theorem (extended state-level no-go at k = 6).** Let `C_k(ℓ, σ)` be the six-palette system at one
cyclic centre for interface length `ℓ` and ray geometry `σ ∈ {0,…,5}^ℓ`: (C1) `1 ≤ |P_i| ≤ k−3`,
(C2) `P_i` meets both allowed sets of Lemma 8.1, (C3) `P_i ∩ P_{i+1} = ∅` cyclically, and at `k = 6`
in addition (C4) no two palettes are complementary 3-sets and (C5) at most three are ternary. Then

* **the tightening is vacuous:** for every `ℓ ∈ {3,4,5,6}` and **every one of the `6^ℓ` sign words**,
  satisfiability with (C1)–(C3) and with (C1)–(C5) agree — the sets of satisfiable words coincide,
  so (C4) and (C5) remove no instance at `k = 6`;
* hence no argument from this data can decide `k = 6`: the system is satisfiable at every `ℓ`, so
  there is no UNSAT certificate, so this route cannot yield `chi(R²) ≥ 7` — with or without the
  INDUCTION LEMMA (the lemma is moot: nothing is being refuted);
* **the class is not vacuous:** the same code decides `k = 4` at `ℓ = 3,4` (0/216, 0/1296) and
  `k = 5` at `ℓ = 5` (0/7776);
* the explicit `k = 6` model, for `ℓ = 3` and every `σ`: outsiders `{3,4,5}`, palettes
  `P_0 = P_2 = P_4 = {3}`, `P_1 = P_3 = P_5 = {4}`; for `ℓ = 4`: shift to `{4},{5}`. Outsiders lie in
  both allowed sets of Lemma 8.1, so (C2) holds; all palettes are singletons, so (C3) is the only
  live constraint and (C4), (C5) have nothing to see.

**Exact tightened counts at k = 6 (independent implementation).**

| ℓ | satisfiable / all sign words | up to the π/3 rotation symmetry | prior run (untightened) |
|---|---|---|---|
| 3 | 216 / 216 | 36 / 36 | 36 / 36 |
| 4 | 1296 / 1296 | 216 / 216 | 216 / 216 |
| 5 | 1350 / 7776 | 225 / 1296 | 225 / 1296 |
| 6 | 1062 / 46656 | 177 / 7776 | 177 / 7776 |

The fourth column is the previous run's table (`smwfhd5sl/m5/INTERFACE-NOGO.md`, Theorem 1); the
agreement is exact, and the first three columns are new: the tightened counts equal the untightened
ones, which is the vacuity statement. A first `ℓ = 6` witness: cells `(0,0,0,3,3,3)`, palettes
`{1,4},{2,5},{1,4},{2,5},{1,4},{2,5}`.

Checks (integer/bitmask exact, 8 s total, no code shared with the earlier run):
`python3 .ultramath/smwfk0ybk/m5/csp_nogo.py` (witness + calibration),
`python3 .ultramath/smwfk0ybk/m5/compare.py` (the vacuity comparison over all 55 944 instances),
`python3 .ultramath/smwfk0ybk/m5/step1_vacuity.py` (the hand-checkable singleton certificate).
