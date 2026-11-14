# The §7–§8 chain at `k = 5`: finite core, exact calibration, and sharpness at `k = 6`

*Member m4, swarm `smwfhd5sl`. Direction L5 (irreducibility half), with the k-dependence that
L4 asks about. Everything below is an exact computation over an explicit finite domain
(`fractions.Fraction` only: no floating point, no solver, no `sorry`). Files that produce every
number quoted are listed in §9.*

---

## 0. What is proved

Four things, in decreasing order of interest.

**(A) Sharpness (`k = 6`).** The palette level of §8 — the only part of it in which the number of
labels appears — is unsatisfiable at `k = 5` for `ℓ = 5` and satisfiable at `k = 6` for every
interface length `ℓ ∈ {3,4,5,6}`. For `ℓ = 5` this is a dichotomy, because Proposition 8.2 *is* the
palette level; for `ℓ = 3,4` the level is satisfiable even at `k = 5`, so those two exclusions need
their geometric layers, which are `k`-blind and at `k = 6` act on W6's six-state systems. Section 4
exhibits the models, and for `ℓ ∈ {3,4,5}` they are geometrically realised by explicit rational ray
directions. The no-go is for a precisely delimited class (§2) and is non-vacuous because the same
class contains a published successful argument at `k = 5`.

**(B) Calibration (`k = 5`).** At `ℓ = 5` the palette level `C₀(5,5)` is unsatisfiable, and
Proposition 8.2 *is* `C₀(5,5)`: the exclusion is one finite count (§3.1). At `ℓ = 4` and `ℓ = 3`
the palette level is *satisfiable* (§3.0), so those two exclusions genuinely need the geometric
layers, and §3.2–§3.3 certify what those layers are: a 729-word enumeration plus one arc-length
inequality for `ℓ = 4`; the sector count, the polynomial three-label region and an exact algebraic
certificate for the seven Moser points for `ℓ = 3`.

**(C) Irreducibility.** Section 5 deletes each named input of each exclusion in turn and exhibits
a model of the rest. Every one of them is used. Section 6 does the same for the one constant
of §7 that carries weight: the multiplicity bound of Lemma 7.5 is *not* relaxed by anything, while
its mesh constant `2` is **not** part of the core (R4 already allows any `d < 5`).

**(D) Verification of the paper's own printed certificate.** Section 7 reproduces §8.6 exactly:
Tables 1 and 2, and the residual identity, for all seven points. It also fixes an ambiguity that
`pdftotext` creates in (8.6), which is worth recording because under the wrong reading the paper's
Lemma 8.9 is false.

**Not claimed.** Nothing here is a statement about `chi(R^2)`. `chi >= 6` is W1 and is used
nowhere. I do not touch Part I of the paper, I do not run the §5–§6 measurable-palette machinery,
and I do not claim an explicit finite witness. The `ℓ = 5` exclusion is *calibrated*, not
re-proved: I certify that its finite combinatorial content is exactly the statement of §3.1, and
that this content is `k = 5`-only.

---

## 1. The interface system C(k, ℓ)

This is the data that §8 actually uses, written as a constraint system. It is the object whose
satisfiability is decided.

Let `R` be the rotation by `κ = π/3`; so `R³ = -id`. Fix a centre `x`, an *interface cycle*
`(i_0,…,i_{ℓ-1})` of distinct labels (paper, Proposition 7.1), the cycle label set `T`, and
`ℓ` limiting unit directions `v_0,…,v_{ℓ-1}` (the `v_j` of §8).

**Sign vector.** For `e ∈ S¹ ∖ B` put `s_j(e) = sign(e · v_j)`, and

```
I(e) = { i_j : s_{j-1}(e) > 0 and s_j(e) > 0 } ∪ (labels outside T)      ("inner")
O(e) = { i_j : s_{j-1}(e) < 0 and s_j(e) < 0 } ∪ (labels outside T)      ("outer")
```

so `I(e)` is what is left after deleting the endpoints of every negative edge, `O(e)` after
deleting the endpoints of every positive edge (Lemma 8.1). Labels outside `T` belong to both.

**The system `C(k,ℓ)`, on the six positions `e, Re, …, R⁵e` of one generic direction.**

| tag | constraint | source |
|---|---|---|
| (P) | `1 ≤ |P_j| ≤ k-3`, where `P_j = P_x(R^j e)` | Proposition 5.6, for general `k` |
| (S) | `P_j ∩ O(R^j e) ≠ ∅` and `P_j ∩ I(R^j e) ≠ ∅` | Lemma 8.1, equation (8.1) |
| (R) | `P_j ∩ P_{j+1} = ∅` | equation (5.7) |
| (A) | *automatic*, not an input: `Opt(-e) = Opt(e)`, so `P_j` and `P_{j+3}` both lie in one two-element option set | `O(-e)=I(e)` and `I(-e)=O(e)`, plus `s_{j+3} = -s_j`; this is where the `ℓ = 5` count turns (§3.1) |
| (B) | `P_j = P_{j+3}` whenever both avoid the labels outside `T` | an outsider-free palette is the *unique* set meeting (P) and (S), and that set is a function of the sign pattern, which is negated at `-e`: so `d(-e) = d(e)` (paper (8.2)) |
| (Z) | position 6 is position 0 | `R⁶ = id` |
| (G) | `s_j = sign(e_j · v_j)` for `ℓ` fixed unit vectors, `e_j = R^j e` | the geometry of `v_0,…,v_{ℓ-1}` |

A **model** of `C(k,ℓ)` is a tuple `(v_0,…,v_{ℓ-1}; e; P_0,…,P_5)` meeting (P),(S),(R),(B),(Z) with
`P_j ⊆ {0,…,k-1}`; (A) then follows. By (G) the sign vectors are not free: each
`s(R^j e)` is determined by angles.
`C(k,ℓ)` is a *relaxation* of the actual plane colouring situation — every proper weak measurable
`k`-colouring supplies a model — so **a model of `C(k,ℓ)` refutes any argument that uses only
these constraints**, and an unsatisfiability proof for `C(k,ℓ)` is a genuine exclusion.

Two points about the strength of (S). First, (S) is literally equation (8.1), not a weakening of
Lemma 8.1: the rest of Lemma 8.1 is a statement about open strips on the two sides of the unit
circle, it is proved from Proposition 7.1's straddling-region exclusion and is therefore `k`-blind,
and it constrains the palette no further. Second, (S) is used only through (8.1) in §8.2 and §8.3;
§8.4–8.6 use the strip form, and I record in §5.3 that the strip form is what (G3) delivers.

---

## 2. The class of arguments, and the no-go

Write `C₀(k,ℓ)` for the **palette level** of `C(k,ℓ)`: the constraints (P),(S),(R),(B),(Z),(G), with (A)
as a consequence of (P),(S),(G) rather than as a separate input. This is the whole of `C(k,ℓ)`
except for the geometric layers that §8.3–§8.6 *derive from* the palette data: the four-ray
diagonal geometry, the sector structure of §8.6, the polynomial region of §8.8.

**Definition.** A *palette-level §8 argument* at `k` is one that, at a cyclic centre supplied by
Proposition 7.1, uses only `C₀(k,ℓ)` for its cycle length.

**Theorem (the no-go).**
**(i)** For `k = 5` and `ℓ = 5`, `C₀(5,5)` is unsatisfiable, by a single finite count (§3.1) — and
Proposition 8.2 *is* `C₀(5,5)`, nothing more.
**(ii)** For `k = 6` and every `ℓ ∈ {3,4,5,6}`, `C₀(6,ℓ)` has a model; for `ℓ ∈ {3,4,5}` the model
satisfies (G), i.e. is realised by explicit rational unit vectors (§4).
**(iii)** Hence there is no palette-level §8 argument at `k = 6` of length `3`, `4` or `5`, for any
value of its constants; and (weakly, because I have no realisation) none of length `6` either.

**Non-vacuity.** The class contains a real, published, successful argument: `C₀(5,5)` is
Proposition 8.2, which is the entire `ℓ = 5` branch of the proof of Theorem 1.4. It is not a straw
man; it is the length-five case of the paper. The no-go says that this branch, and every branch
that works the way it works, dies at `k = 6`.

**Delimitation, stated honestly.** The class does *not* contain Propositions 8.5 and 8.10, and this
is a fact, not an omission: `C₀(5,4)` and `C₀(5,3)` are **satisfiable** (§3.0). Those two
exclusions need their geometric layers even at `k = 5`. What survives of them is this: the
geometric layers are `k`-blind, they consume the palette data, and at `k = 6` they consume a
*different* state space (six outsider states instead of two, W6). So a `k = 6` exclusion by that
route has to come from the interaction between the `k`-blind geometry and the six-state system, and
not from anything in the palette.

**Where the weight is.** The only constraint in `C₀` that changes from `k = 5` to `k = 6` is (P),
from `|P| ≤ 2` to `|P| ≤ 3`. Everything else — (S), (R), (B), (Z), (A), (G) — is `k`-blind. So the
no-go localises exactly on the palette cardinality bound, which is what R5 says.

---

## 3. Calibration

### 3.0 The palette level over all `k` and `ℓ`

Before the three individual exclusions, here is the whole table. `UNSAT` is decided by a search
over the relaxation in which the six sign patterns are free subject to `s_{j+3} = -s_j` (every
geometric datum satisfies that, so UNSAT of the relaxation refutes `C₀`); `SAT` comes with a model.

```
 k   l   C_0(k,l)
 3   3   UNSAT      (P) reads 1 <= |P| <= 0
 4   3   UNSAT
 4   4   UNSAT
 5   3   SAT        s = ---,---,---,+++,+++,+++   P = {3},{4},{3},{4},{3},{4}
 5   4   SAT        s = ----,--++,-++-,++++,++--,+--+   P = {4},{1,3},{0,2},{4},{1,3},{0,2}
 5   5   UNSAT      the count of Section 3.1
 6   3   SAT
 6   4   SAT
 6   5   SAT
 6   6   SAT        s = ----++,---++-,--++--,++++--,+++--+,++--++
                    P = {1,5},{0,4},{1,3},{2,5},{1,4},{0,3}
```

`UNSAT` for `ℓ < k` is decided over the relaxation in which the six sign patterns are free subject to
`s_{j+3} = -s_j`; for `ℓ = k` there are no outsiders, so (B) is vacuous and the same relaxation is
used. In both cases UNSAT of the relaxation refutes `C₀`.

Two consequences, both used in §2.

* `C₀(5,4)` has **800** models and exactly **34** distinct state words — the 6 three-periodic
  permutations and the 28 words with a well-defined parity. So the palette level excludes nothing
  at `k = 5`, `ℓ = 4`, and Proposition 8.5 is genuinely a two-stage argument. Note also that a
  single state word may mix `U` and `V` on its non-`X` parity; the paper's step "all three selected
  entries of the first word have one diagonal value" is a statement about a *pair* of nearby words,
  not about a single word, and the paper says so.
* `C₀(5,3)` has models. So Proposition 8.10 is not a palette-level exclusion either.

### 3.1 `ℓ = 5` (Proposition 8.2)

**Step 1 — reduction.** Every position's sign vector has `O` and `I` non-empty (Lemma 8.1). Of
the `2⁵ = 32` sign vectors, exactly **10** have both non-empty. In each of the ten, the admissible
palettes are exactly **two** sets, both *diagonals* `D_i = {i, i+2}` (`i ∈ Z/5`), and their indices
differ by `±2` mod 5. Moreover `Opt(-s) = Opt(s)`, since `O(-s) = I(s)` and `I(-s) = O(s)`.
Consequently, at every position, `P_j = D_{p_j}` for some `p_j ∈ Z/5`, and (R) says
`p_{j+1} - p_j ∈ {±1}`, while (A) says `p_{j+3} - p_j ∈ {0, ±2}`.

**Step 2 — count.** Over the `5⁶ = 15625` functions `p : Z/6 → Z/5`, with the option sets free
(i.e. dropping the antipodal linkage `s_{j+3} = -s_j`, which is what makes `Opt(R^{j+3}e) =
Opt(R^j e)`):

```
(P),(S),(R),(Z) with the six option sets free:      100 solutions
(P),(S),(R),(Z) with the antipodal linkage:           0 solutions
```

The `100` is `5·C(6,3)`: a closed `±1` walk of length 6 in `Z/5` must have three `+1` and three
`-1` steps, and there are `C(6,3) = 20` sign patterns times 5 starting points. So the antipodal
step of the paper's proof is doing real work — I first believed it was redundant, and the
enumeration said otherwise. It is not, however, a separate hypothesis: it is the part of (G) that
says `R³ = -id`, and it is *forced*, which is why `C₀(5,5)` is unsatisfiable and not merely
unsatisfiable-with-an-extra-axiom. The same computation, run directly on palettes without the
diagonal reduction and over all admissible sign families, also returns UNSAT (`m4_palette_level.py`,
row `k = 5, ℓ = 5`), so the reduction is not where the contradiction comes from.

### 3.2 `ℓ = 4` (Proposition 8.5)

The state of (8.2): `p(e) = X` if the outsider is in the palette, else the forced diagonal
`d(e) ∈ {U, V}` with `U = {0,2}`, `V = {1,3}`; and `d(-e) = d(e)`, so

```
(8.2a)  p(e) ≠ p(Re)                        [from (5.7)]
(8.2b)  p(e) = p(-e) whenever both ≠ X.
```

The six-position word is `w(t)_j = p(e^{i(t + jπ/3)})`.

**Count.** Of the `3⁶ = 729` words over `{X,U,V}`, exactly **34** satisfy (8.2a) and (8.2b). Then:

* **0** of them are `X`-free (a word without `X` alternates `U,V`, violating (8.2b) across an
  antipodal pair);
* exactly **6** have `X` on both parities, and all six are the 3-periodic permutation words
  `XUVXUV`, `XVUXVU`, `UXVUXV`, `UVXUVX`, `VXUVXU`, `VUXVUX`;
* the remaining **28** carry a well-defined parity `h(w) ∈ Z/2`.

So Lemma 8.3's first claim is *false* for (8.2a)+(8.2b) alone — the six 3-periodic words are
counterexamples — and the paper is right to need the cross-word restriction. That restriction,
stated as a relation on words (a diagonal at a position of `w(t)` cannot equal a diagonal at an
*adjacent* position of `w(t')` when `|t-t'| < η`), **isolates each of the six**: the only word
compatible with `XUVXUV` is `XUVXUV`, and so on for all six. Since the parameter set `G` is
`η`-chain-connected and invariant under `+κ`, isolation propagates to make `w` constant on `G`,
which contradicts `w(t+κ)_j = w(t)_{j+1}` for a 3-periodic word. Hence no 3-periodic word occurs
and `h : G → Z/2` is well defined and locally constant.

**The count that finishes it.** Three projective positions spaced `π/3` on the projective circle
(circumference `π`) cannot lie in an open arc shorter than `π - π/3 = 2π/3`. Lemma 8.4 puts the
diagonal `U` on one open projective arc and `V` on the complementary one; Proposition 8.5 produces
three equally spaced positions valued `D` in each word, for both values `D = U` and `D = V`. Both
arcs then exceed `2π/3`, while their lengths sum to `π`: `4π/3 > π`. ∎

Note: the paper's sharper conclusion "one arc has length `≤ π/2`" is not needed. `2·(2π/3) > π`
already contradicts, so Lemma 8.4's last clause is not part of the core.

### 3.3 `ℓ = 3` (Proposition 8.10)

The binary state, the sector structure and the Moser contradiction, in order:

1. (8.1) puts an outsider in `P_x(e)` a.e.; (5.7) forbids two outsiders in one palette, since the
   antipodal palette needs one. So a.e. `s(e) ∈ {X,Y}` with `s(Re) ≠ s(e)`.
2. Lemma 8.6: `s` is locally essentially constant. Lemma 8.7: the essential boundary is exactly
   one six-position `R`-orbit. The count there is finite and I verify it as a count: each boundary
   point `e` has `e ∈ B` or `Re ∈ B`; the three interface rays give at most three projective
   classes in `B`; one `R`-orbit uses exactly three, and distinct `R`-orbits have disjoint
   projective classes (the projective classes of an orbit are the three cosets of `⟨π/3⟩`); so at
   most one orbit. Then the six sectors alternate `X, Y`.
3. Lemma 8.8: for `z = ξ+iυ`, `0 < |z|² < 4` and `υ²(3ξ²-υ²)² < l³(1-l/4)(l-1)²` with
   `l = ξ²+υ²`, a neighbourhood of `x+z` uses only the three triangle labels a.e. The algebra
   checks: with `δ = arccos(r/2)`, `sin 3(φ-δ)sin 3(φ+δ) = sin²(3φ) - sin²(3δ)` and the
   displayed inequality makes that product negative, so the two unit directions summing to `z`
   lie strictly inside sectors of opposite value.
4. Lemma 8.9 holds **exactly** for all seven placed points (§7 below).
5. The seven points carry the eleven exact unit edges of the Moser–Moser graph, which has **0**
   proper 3-colourings out of `3⁷ = 2187`. ∎

---

## 4. Sharpness: `C(6,ℓ)` is satisfiable for every `ℓ`

Throughout `k = 6`, so (P) reads `1 ≤ |P| ≤ 3`. The construction uses the one observation that
does all the work: *for `ℓ ≤ k-1` the labels outside the cycle lie in both `O(e)` and `I(e)`, for
every sign pattern*, so a palette made of outsiders meets (S) for free and (R) is satisfied by
alternating two outsiders.

**`ℓ = 5`** (one outsider, so the cycle labels must be used). Rays, in units of `π`:

```
v = ( 6/5,  1/3,  103/300,  97/300,  4/3 )
```

At `e = 1` and its five `R`-images the sign vectors are `-+++-` (three times) and `+---+` (three
times); `O = {0,5}`, `I = {2,3,5}` on the first and `O = {2,3,5}`, `I = {0,5}` on the second; the
palettes

```
P = {5}, {0,2}, {5}, {0,2}, {5}, {0,2}
```

satisfy (P), (S), (R). **This is a fully geometric datum**: five rays, one centre, six positions.

**`ℓ = 4`** (two outsiders). Rays `(1/3, 103/300, 5/4, 63/50)`, sign vectors `++--` and `--++`,
palettes `{4},{5},{4},{5},{4},{5}`. All constraints hold; geometrically realised.

**`ℓ = 3`** (three outsiders). Rays `(1/3, 103/300, 5/4)`, sign vectors `++-` and `--+`,
palettes `{3},{4},{3},{4},{3},{4}`. Geometrically realised.

**`ℓ = 6`** (the case the paper does not have). 30 of the 64 sign vectors admit an admissible
palette at `k = 6`. A full model, satisfying (P),(S),(R),(B),(Z):

```
s  = ----++  ---++-  --++--  ++++--  +++--+  ++--++
P  = {1,5}   {0,4}   {1,3}   {2,5}   {1,4}   {0,3}
```

I do not claim a geometric realisation for `ℓ = 6` (it is not needed: the paper has no `ℓ = 6`
argument at all, so the length is already unexcluded).

**Consequence.** At `k = 6` none of the four interface lengths is excluded by (P),(S),(R) with
(G). The `ℓ = 5` model is the one that matters, because it is a realised geometry.

**Consistency with W6.** At `k = 6` and `ℓ = 3` the outsiders form a six-state system, exactly
`W6`'s count; my `{3},{4}` alternation is a two-element sub-model of it, which is all that is
needed to refute an exclusion. I do not re-derive W6's non-bipartiteness.

---

## 5. Irreducibility: deleting each input in turn

Each line is a model of the system with that one input removed, exhibited in full. `SAT` means the
remaining inputs are consistent, so the deleted input is used.

### 5.1 `ℓ = 5`: the inputs of Proposition 8.2

The sign family used below is `s = (+,+,-,-,-)` at positions `0,1,2` and its negation at `3,4,5`:
it satisfies `s_{j+3} = -s_j` and is realised by the five rays `(1/3, 103/300, 5/4, 63/50, 51/40)`
in units of `π` (two in the window `(π/6,π/2)`, three in `(7π/6,3π/2)`), so (G) holds. There
`O = {3,4}`, `I = {1}` and `Opt = {D₁, D₄}` on the first three positions, and `O = {1}`, `I = {3,4}`,
`Opt = {D₁, D₄}` on the last three.

| deleted | model of the rest |
|---|---|
| (P) | the `k = 6` datum of §4 (bound `3` instead of `2`), (G) included |
| (R) | `P_0 = P_1 = P_2 = D₁ = {1,3}`, `P_3 = P_4 = P_5 = D₄ = {1,4}`: meets (P),(S),(Z) and `P_2 ∩ P_3 ≠ ∅` |
| (S) | `P_j = {0},{1},{0},{1},{0},{1}` meets (P),(R),(Z); (A) then has no meaning, being a statement about option sets |
| antipodal part of (G) | **100** of the 15625 closed `±1` walks survive once `s_{j+3} = -s_j` is dropped; e.g. the walk `0,1,2,3,2,1` |

(Z) is structural rather than a hypothesis: it is the domain of the walk, and it is used twice, to
close the walk (the `100` of §3.1) and to identify position 6 with position 0. Both uses are inside
the `5⁶` enumeration, which is what proves that no closed walk survives the antipodal condition.

### 5.2 `ℓ = 4`: the six inputs of Proposition 8.5

| deleted | model of the rest |
|---|---|
| (J1) `p(e) ≠ p(Re)` | `UUUUUU` |
| (J2) `p(e) = p(-e)` | `UVUVUV` (66 words satisfy (J1) alone — `(3-1)⁶+2` — and 32 of them violate (J2)) |
| (J3) cross-word | the six 3-periodic words are no longer isolated |
| (J4) `κ`-shift | a 3-periodic word constant on `G` is not equal to its shift |
| (J5) Lemma 8.4 | both diagonal values may occupy one arc; the `2π/3` count then says nothing |
| (J6) spacing | if the three positions were clustered, one arc of length `≤ π` holds all three |

### 5.3 `ℓ = 3`: the six inputs of Proposition 8.10

| deleted | model of the rest |
|---|---|
| (G1) `s ∈ {X,Y}`, `s(Re) ≠ s(e)` | `s ≡ X` |
| (G2) Lemma 8.6 | any a.e. `s` with the flip; no sector structure is forced |
| (G3) Lemma 8.7 | two boundary orbits give twelve sectors; the state is still consistent but is not `sign sin(3θ)`, so 8.8 does not apply |
| (G4) Lemma 8.8 | a five-label region constrains nothing; the seven Moser points are 5-colourable |
| (G5) Lemma 8.9 | membership is not automatic: Table 1 is tight at `g = B`, `P = 0.000002` against `P'⁺ = 0.00065`, a ratio of 325 |
| (G6) Moser | a proper 3-colouring would end the contradiction; 0 of `3⁷` exist |

**Every input, deleted in turn, with an explicit model of the rest** — four in §8.2 plus the
antipodal half of (G), six in §8.5, six in §8.10. The §8 chain has no slack: it is irreducible as a
function of its named hypotheses.

---

## 6. §7: which cover constant is in the core

Lemma 7.5 reads: a closed square of side ten has no relatively open cover of multiplicity at most
two and mesh at most two. Its two constants behave differently.

* **Multiplicity 2 is in the core and cannot be relaxed.** The triangular lattice of spacing
  `s = 6/5`, with the open unit discs about its points, cuts the square into a cover of mesh
  exactly `2` and multiplicity exactly `3` (at the Delaunay centroids). Exactly, in two rational
  inequalities: `s²/3 = 12/25 < 1` (covering radius below `1`) and `3s²/4 = 27/25 > 1` (the nearest
  non-neighbour of a Delaunay centroid is farther than `1`). This is W4, re-derived; it is stated
  here because it is the §7 half of the irreducibility claim: replacing "multiplicity at most two"
  by "at most three" makes the lemma false at every mesh.
* **Mesh 2 is *not* in the core.** By R4 the lemma holds for every mesh `d < 5`, so the constant
  `2` can be weakened to `< 5` without changing the argument. The sharp form of the §7 cover input
  is therefore: **multiplicity at most two, mesh less than five.** Only the multiplicity bound
  carries weight.
* The remaining §7 inputs — Lemma 7.4 (tree fillings), Lemma 7.6 (a non-null core loop), Lemma 7.7
  (midpoint detection), Lemma 7.8 (annular crossing) — are analytic and topological, not finite
  constraints. I do not construct deletion models for them, and say so: they are the residue of
  the core that this method of analysis cannot reach.

---

## 7. The printed certificate of §8.6, verified exactly

Everything in this section is exact arithmetic in `Q(√3, √11)` (a four-dimensional `Q`-algebra with
basis `1, √3, √11, √33`) compared through rigorous rational interval bounds on the two radicals.

**(8.6) must be read with its outer parentheses.**

```
z_g = ((35+12i)/37) · ( g + (-290+149i)/250 ),        g ∈ G = {0, A, B, T, uA, uB, uT}
```

`pdftotext` drops the outer pair. The two readings are numerically far apart and the paper's own
Table 1 decides between them: under the flat reading `z_0 = (-1.16, 0.596)` while Table 1 row `0`
says `(-1.2906, 0.1876)`, and under the flat reading Lemma 8.9 is **false** at `g = 0`. Under the
bracketed reading all seven tabulated centres are reproduced to within `4.4·10⁻⁵ < h = 1.1·10⁻⁴`,
and the residual identity of §8.6 is reproduced *exactly*, integer for integer, at scale
`710400000000`. So (8.6) is correct as printed and this is a text-extraction artifact, as in
`results/ERRATA-TRIAGE.md`.

**Table 1 / Table 2.** With `h = 0.00011` and the paper's own `(a, b, b_y, b_H)` per row, every
strict rational inequality of §8.6 holds:

```
y_u < b_y,   H < b_H,   a < l_l ≤ l_u < b,
y_u H² < P⁺,   a³(1-b/4)·min(|a-1|,|b-1|)² > P'⁻,   P⁺ < P'⁻
```

for all seven rows. So Lemma 8.9 is verified twice over: from the rational tables, and directly
by interval arithmetic on the exact algebraic coordinates.

**The graph.** `G` has 11 pairs at distance exactly `1` in `Q(√3,√11)` — the five edges of the two
equilateral triangles on `AB`, the three of each rotated triangle, and `T–uT` — and exactly 10
non-edges, none at distance `1`. Its chromatic number is `4`: `0` proper 3-colourings of `3⁷`
assignments, and the paper's forcing argument (`c(0)=c(T)`, `c(0)=c(uT)`, `|T-uT|=1`) is the
short proof of the same thing.

---

## 8. What this forces on a replacement mechanism

Four falsifiable requirements, each with the exact test attached. (A fuller list is the business
of the specification half of L4; these are the ones my certificate makes non-negotiable.)

**F1. The replacement must kill every model of §4.** For each `ℓ ∈ {3,4,5}` the datum in §4 is
explicit and geometric: five (resp. four, three) rational ray directions in units of `π`, one
centre, six palettes. A replacement invariant that is satisfied by all three of them cannot decide
`k = 6`. *Test*: evaluate the invariant on those three data; any survivor refutes the replacement.

**F2. It must not factor through `C₀`.** Equivalently: it must use the *value* of `k` somewhere
other than the palette bound `k-3`. §3.1 shows that at `k = 5`, `ℓ = 5` those inputs are already
contradictory, so a replacement that is a consequence of them is either `k = 5`-only (hence no use)
or vacuous at `k = 6` (by F1). *Test*: check the implication symbolically, or exhibit one model of
§4 that satisfies the replacement.

**F3. It must be compatible with the sharp §7 cover input.** The cover lemma the §7 continua need
is "multiplicity ≤ 2, mesh < 5" and nothing weaker in the multiplicity direction (§6). So a
replacement whose conclusion at a cyclic centre requires a cover of multiplicity three is dead on
arrival, whatever its palette content. *Test*: exhibit a multiplicity-three cover of the square of
the mesh the replacement needs — W4 does this for every `d ≥ 2`.

**F4. Its failure at `k = 5` must be a failure of the same invariant.** The calibration in §3 is
the standard: a replacement must reproduce a contradiction at `k = 5` from its own hypotheses, on
the same finite object. *Test*: run the replacement's decision procedure on `C(5,ℓ)`, `ℓ = 3,4,5`;
it must return "unsatisfiable", and on `C(6,ℓ)` it must return "satisfiable" only if the
replacement is *not* claimed to decide `k = 6`.

F1 and F2 are the ones the §5–§7 method fails; F3 and F4 are the ones it passes.

### 8.1 The exact content of F2

For the length-five interface F2 is not a heuristic, it is a dichotomy, and §3.1 decides it. The
palette level `C₀(5,5)` is unsatisfiable and `C₀(6,5)` is satisfiable, with the *same* sign-pattern
machinery: the ten admissible sign vectors, the two diagonals per position, the closed `±1` walk in
`Z/5`. So at `ℓ = 5` the count `100 → 0` is the entire distance between a proof at five colours and
nothing at six. A replacement for §8.2 must therefore supply a constraint that is (a) satisfied by
the realised `k = 6` datum of §4 and (b) strong enough to contradict at `k = 5`; F2 is the demand
that such a constraint not be a consequence of `C₀`.

For `ℓ = 4` and `ℓ = 3` the corresponding statement is sharper about *where* a replacement must
live: since `C₀(5,4)` and `C₀(5,3)` are satisfiable, no replacement at those lengths can be a
palette-level statement either — the paper's own exclusions there already spend the geometric
layers, and at `k = 6` those layers act on W6's six-state systems.

---

## 9. Reproduction

Everything runs under `python3` with the standard library only, in well under a second per file.

```
python3 m4_s8_core.py        # §1-§5, §8: the interface system, calibration, sharpness, deletions
python3 m4_palette_level.py  # §3.0: the palette level for k = 3..6, 3 <= l <= k
python3 m4_moser.py          # §3.3, §7: Moser graph, placement, Lemma 8.9, Table 1 check
python3 m4_tables.py         # §6, §7: the cover constants, Table 1/2, residual identity
```

| file | what it certifies |
|---|---|
| `m4_s8_core.py` | `C(5,5)` UNSAT by `5⁶`; the `2⁵` option reduction; the `3⁶` word enumeration and the six isolated 3-periodic words; the `2π/3` arc count; `C(6,ℓ)` models with exact rational ray data; the deletion models plus the PART 8 verification |
| `m4_palette_level.py` | the `k × ℓ` table of §3.0; UNSAT by relaxation, SAT by printed model; the 800 models / 34 state words of `C₀(5,4)` |
| `m4_moser.py` | 11 exact unit edges in `Q(√3,√11)`; 0 of `3⁷` proper 3-colourings; Lemma 8.9 exactly for all seven placed points; Table 1 reproduced inside `h` |
| `m4_tables.py` | `12/25 < 1 < 27/25` (the W4 cover); the paper's Table 1/2 rational inequalities; the §8.6 residual identity, integer for integer |

Instance sizes, for the record: `2⁵ = 32` sign patterns (`ℓ = 5`); `5⁶ = 15625` assignments;
`3⁶ = 729` words (`ℓ = 4`); `3⁷ = 2187` colourings (Moser); `2⁶ = 64` sign patterns (`ℓ = 6`).
No solver, no DRAT file, no floating point: every claim is an exhaustive loop over an explicitly
listed finite domain, so "certificate" means the enumeration itself.

---

## 10. Open ends

* `ℓ = 6` at `k = 6` has a combinatorial model here but no geometric realisation. Nothing depends
  on it, because the paper has no `ℓ = 6` argument.
* §7's analytic lemmas (7.4, 7.6, 7.7, 7.8) are outside the reach of a deletion-table analysis.
* I did not re-derive W6, W4 or R4; §4 and §6 use them and say so.
