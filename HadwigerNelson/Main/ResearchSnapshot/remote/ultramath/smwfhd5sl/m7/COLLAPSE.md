# L4: the palette-transfer collapse — what the §5–§7 palette inputs can and cannot decide

Swarm `smwfhd5sl`, member `m7`, direction D1 (L4 core).  Everything below is a theorem with a
complete proof, a machine-checked lemma, an exact computation, or an explicit statement of what is
open.  Files, and the exact check commands:

* `collapse_check.py` — exact checks CHECK 1–5.  Run: `python3 collapse_check.py`.
* `Collapse.lean` — `exists_coloring_of_palette`, `six_coloring_of_palette_six`,
  `five_coloring_of_palette_five`, `no_palette_five_of_no_five_coloring`, `exists_unit_avoiding`;
  all machine-checked.  Run: `lean Collapse.lean` (Mathlib on `LEAN_PATH`; 2.4 s; axioms
  `[propext, Classical.choice, Quot.sound]`).

**Answer in one paragraph.**  The §5–§7 method consumes the palette through a short list of inputs
whose c-free core is the palette-transfer disjointness of Lemma 5.2(3).  Read *pointwise*, that
input is **equivalent to k-colourability of the plane** (Theorem 1, Lean-checked): a nonempty
palette field with the transfer property is a k-colouring in disguise.  Hence the brief's §2
"natural route" to L4 — *exhibit a palette system at k = 6 satisfying (a)–(f)* — is not a no-go
certificate: it is an explicit **6-colouring**, i.e. terminal outcome L2 (Corollary A).  The
paper's actual strength is the *a.e.-in-angle* form, and that form is genuinely weaker: even with
joint measurability in the centre, its consequence is only "the bad set is null on the constraint
manifold", a statement satisfied by objects that are not colourings (Theorem 2, CHECK 5).  This
locates the L4 problem exactly: the class of palette-transfer arguments that is not equivalent to
the problem is the a.e. class, and its satisfiability at k = 6 is untouched by any argument here or
in the paper.  §6 turns that into the falsifiable specification a replacement mechanism must meet.

Throughout, `ℂ = R^2` with the Euclidean norm, `S^1 = {s : ‖s‖ = 1}`, and `|·|` is angular measure
on `S^1`.

---

## 1. The class, precisely

**Definition 1.1 (palette field).**  A *palette field at level k* is a map `Q : Fin k → ℂ → Set ℂ`,
in *circle-point coordinates*: `Q i a = {σ ∈ S^1 : i ∈ P_{a-σ}(σ)}`, where `P_x(e)` is the maximal
palette of Definition 5.1 of the paper at centre `x` in direction `e`.  Nothing is assumed beyond
the axioms listed.

**Axioms.**  Each is an input of §5–§7, in the form the paper supplies it.  The *quantifier* is the
entire subject of this note.

* **(P0) Nonemptiness.**  For all `a` and all unit `σ`, some `i` has `σ ∈ Q i a`.
  *(Paper: Prop. 5.6's lower bound `1 ≤ |P_x(e)|`, derived from one trace in `W_x`; no colouring
  needed.)*
* **(P1) Transfer, pointwise.**  For all `a b s f` with `‖s‖ = ‖f‖ = 1`, `‖a - b‖ = 1` and `b - a`
  not parallel to `s`: there is no `i` with `s ∈ Q i a` and `f ∈ Q i b`.
* **(P2) Transfer, a.e. in the angle.**  For every pair of centres `(x,z)` there is a null set
  `N(x,z) ⊂ S^1` such that (P1)'s conclusion holds at every `f ∉ N(x,z)`, for each of the two
  branches of `f ↦ s(f)`.  *(This is Lemma 5.2(3) as printed — "almost everywhere on that domain" —
  with the exceptional set depending on the fixed pair of centres; Remark 5.3.)*
* **(P3) Joint measurability.**  `(x,e) ↦ P_x(e)` is jointly measurable.  *(Not assumed in the
  paper: "No joint measurability of `P_x` in its center is assumed.")*

The remaining §5–§7 inputs are *not* palette axioms and are not used below: the bound
`|P_x(e)| ≤ k-3` (Prop. 5.6), binary-centre separation (Lemma 5.5), the cover lemma (Lemma 7.5 with
R4's mesh `d < 5`, multiplicity `≤ 2`, sharp by W4), the cycle bound `3 ≤ ℓ ≤ k` (Prop. 7.1) and the
`ℓ = 3,4,5` exclusions of §8.  §6 records what their omission buys.

**Definition 1.2.**  `CAP(k)` = the arguments from `(P0)+(P1)`; `CAP_ae(k)` = from `(P0)+(P2)`;
`CAP_ae^meas(k)` = from `(P0)+(P2)+(P3)`.

---

## 2. Where the transfer axiom comes from, exactly

Take `a, b` with `‖a - b‖ = 1`, unit `s, f`, and put `t := b - a`, `x := a - s`, `z := b - f`.
Then `z + f = x + s + t` with `|t| = 1`: the representation of Lemma 5.2(3) with *constant* second
endpoint map `t(f) ≡ t` and `s(f) ≡ s`.

**CHECK 1 (`collapse_check.py`, exact).**  The two-circle construction of `s(f)` is transversal at
`f` exactly when `0 < |t + s|^2 < 4`; and `|t+s|^2 = 2 + 2⟨t,s⟩ ∈ (0,4)` with `|t| = |s| = 1`
precisely when `t` is not parallel to `s` (Lagrange: `(t×s)^2 = |t|^2|s|^2 - ⟨t,s⟩^2 ≠ 0`).
So "nonparallel" in the lemma is *equivalent* to the local-diffeomorphism hypothesis it needs: no
degenerate case is hidden in (P1).

Applying the lemma: for every fixed pair of centres `(x,z)`, for almost every `f`, and for each
branch of `s(f)`, `P_z(f) ∩ P_x(s(f)) = ∅`.  In circle-point coordinates (`a = x + s(f)`,
`b = z + f`) that is **(P2)**, not **(P1)**: the exceptional set is per centre pair.  Remark 5.3
confirms the reading — "the proof applies at every fixed pair of centers and never needs a common
exceptional angular set over an uncountable family of centers" — and §5.1 declines joint
measurability in the centre.

So (P1) is a pointwise strengthening of what the paper proves.  Theorem 1 shows the strengthening
has zero slack; Theorem 2 shows that (P2)+(P3) does *not* have zero slack.  The gap between (P1)
and (P2) is therefore exactly the L4 locus.

---

## 3. Theorem 1 (collapse): `(P0)+(P1)` ⟺ the plane is k-colourable

**Theorem 1.**  Let `Q : Fin k → ℂ → Set ℂ` satisfy (P0) and (P1).  Then there is
`c : ℂ → Fin k` with `c a ≠ c b` whenever `‖a - b‖ = 1`.  Conversely a proper k-colouring yields
such a `Q` (singleton palettes).  Hence

    a palette field at level k satisfying (P0)+(P1) exists   <=>   χ(R^2) ≤ k.

*Proof.*  Restrict to unit directions: `P i a := Q i a ∩ S^1`.  Call `a` **i-good** if `P i a` is
nonempty and is not contained in any antipodal pair `{u,-u}`.  Let `B_i` be the set of `i`-good
points.

*Step 1 (cover).*  Every `a` is good for some `i`.  Suppose not.  For each `i`, either `P i a = ∅`,
and then `P i a ⊆ {1,-1}`, or `P i a` is nonempty and, not being good, `P i a ⊆ {u_i,-u_i}` for some
unit `u_i`.  By (P0) every unit `s` lies in some `P i a`, hence in `{u_i,-u_i}` for that `i`, hence
in the finite set `{u_1,-u_1,…,u_k,-u_k}`.  A finite set cannot contain `S^1`:
`PaletteCollapse.exists_unit_avoiding` produces a unit vector outside any `2k` prescribed signed
values (Pythagorean parametrisation `n ↦ ((n²-1) + 2n i)/(n²+1)`, whose real part is strictly
increasing).  Contradiction; so `R^2 = ∪_i B_i`.

*Step 2 (rigidity).*  Let `a, b ∈ B_i` with `‖a - b‖ = 1`.  Take `s ∈ P i a`, `f ∈ P i b` (both
nonempty).  If `b - a` were not parallel to `s`, (P1) would give `P i a ∩ P i b = ∅`, contradicting
`s ∈ P i a`, `f ∈ P i b`.  So `b - a ∥ s`, and `‖s‖ = 1 = ‖b - a‖` gives `s = ±(b - a)`.  As
`s ∈ P i a` was arbitrary, `P i a ⊆ {b-a, -(b-a)}` with `‖b-a‖ = 1`: `a` is not `i`-good,
contradiction.

*Step 3.*  Each `B_i` is unit-distance free and `R^2 = ∪_i B_i`; choosing `c a ∈ {i : a ∈ B_i}` gives
a proper k-colouring.  ∎

*Machine check.*  `PaletteCollapse.exists_coloring_of_palette` (all `k`, arbitrary `Q`, no
measurability, no cardinality bound), with axioms `[propext, Classical.choice, Quot.sound]`.  The
combinatorial core is independently stress-tested by exhaustive random search on finite instances
(CHECK 2: 6000 instances, 247 satisfying `(P0)+(P1)` with `|S| > 2k`, all 247 correctly coloured by
this construction; no failure).  Both hypotheses are needed (CHECK 3): dropping (P0) admits
`Q ≡ ∅`; dropping (P1) admits `Q ≡ S^1`.

**Corollary A (the brief's suggested L4 certificate *is* L2).**  By Theorem 1, a palette system at
`k = 6` satisfying (a)–(f) — indeed satisfying only (P0)+(P1) — *is* a proper 6-colouring of the
plane (`PaletteCollapse.six_coloring_of_palette_six`).  So §2 of the brief's "natural route" to L4
produces terminal outcome **L2**, not L4; any L4 certificate of that shape is simultaneously a
disproof of `χ ≥ 7`.  This is a defect in the brief as stated (acceptance clause (d)).

**Corollary B (non-vacuity: the class decides k = 5, provably).**  Theorem 1 at `k = 5`
(`five_coloring_of_palette_five`) turns (P0)+(P1) into a proper 5-colouring; W1
(`OAI.EuclideanFiveColor.no_proper_five_coloring`, machine-checked) says none exists.  Hence
**`CAP(5)` is unsatisfiable** — the palette-transfer axioms alone refute five labels, with no appeal
to the paper's §6–§8 geometry.  Formal form, machine-checked:
`PaletteCollapse.no_palette_five_of_no_five_coloring`, which takes W1 as its only hypothesis.  So `CAP` is not a strawman: it proves the project's headline lower
bound at `k = 5`, and by Theorem 1 it can decide `k = 6` only by deciding `χ ≤ 6`.  For "any value
of its constants": no constant occurs in (P0)+(P1).

**Corollary C (the cardinality bound is not where k enters).**  Neither the statement nor the proof
of Theorem 1 uses `|P_x(e)| ≤ k-3`; palettes may have any cardinality.  So R5 ("Proposition 5.6 is
the unique locus of the k = 6 failure") holds for the paper's route, not for the palette inputs: the
transfer axiom already carries the whole strength.  Consequently a mechanism that only sharpens the
cardinality bound — route B, "force `|P| ≤ 2` at `k = 6`" — cannot succeed from the palette axioms:
by Corollary B those axioms already decide `k = 5`, and by Theorem 1 they decide `k = 6` only if one
decides `χ ≤ 6`.  Route B must therefore use content outside (P0)+(P1) — the actual colouring
(paper (5.2)) plus density arguments — and cannot be a finite palette check.

---

## 4. The explicit computed example: the collapse is inhabited at k = 7

**CHECK 4 (`collapse_check.py`, exact in `Q(√3)`).**  Let `s = (2/5)√3`, `u = (s,0)`,
`v = (s/2, s√3/2)`, `Λ = ℤu + ℤv` (hexagonal, spacing `s`), and `Λ' = ⟨2u+v, -u+3v⟩ ⊂ Λ`.  Regular
hexagons of circumradius `L = 2/5` about `Λ` tile the plane (inradius `L√3/2 = s/2`).  Then
`[Λ:Λ'] = 7`; the shortest vector of `Λ'` has squared length `84/25 = 7s²`; hexagon diameter
`2L = 4/5 < 1`; and distinct cells of one `Λ'`-coset are at distance `≥ √(84/25) - 4/5 > 1` because
`84/25 > 81/25` (exact rational comparison).  So colouring each cell by its coset is a proper
7-colouring of the plane.

Its palette field is `Q i a = S^1` or `∅` according as `a` lies in class `i`.  (P0) and (P1) hold
(the latter vacuously: a unit pair never shares a label), `|P| ≡ 1 ≤ 7-3`, and every `D_i(a)` is
`∅` or all of `S^1` — which is exactly what makes Step 1 of Theorem 1 fire.  At `k = 6` Step 1 is
precisely the assertion `χ ≤ 6`.

---

## 5. Theorem 2: what joint measurability gives — and what it does not

Write `M := {(a,s,b,f) : ‖a - b‖ = 1, ‖s‖ = ‖f‖ = 1}` (a 5-dimensional manifold) and

    Bad_i := {(a,s,b,f) ∈ M : s ∈ Q i a, f ∈ Q i b, b - a not parallel to s}.

**Theorem 2.**  Assume (P0), (P2), (P3).  Then `Bad_i` is null in `M` for every `i`; consequently,
for almost every unit pair `(a,b)` and every `i`,

    min( |Q i a| , |Q i b| ) = 0.        (★)

*Proof.*  For `(x,z,f)` with `|z - x + f| ≤ 2` let `s_±(x,z,f)` be the two solutions of
`|z + f - x - s| = 1`, `‖s‖ = 1`, and put `Ψ(x,z,f,±) := (x + s_±, s_±, z + f, f)`.  `Ψ` maps onto
`M` (inverse: `(a,s,b,f) ↦ (a - s, b - f, f, branch of s)`), smoothly and 2-to-1, hence carries
null sets to null sets.  By (P2), `Ψ(x,z,f,±) ∈ Bad_i` forces `f ∈ N(x,z)`.  The set
`{(x,z,f) : f ∈ N(x,z)}` has null fibres over `(x,z)` and is null by Fubini; measurability of that
set and of `Bad_i` is exactly what (P3) supplies.  So `Bad_i` is null.  Then Fubini on `M` fibred
over `{(a,b) : ‖a-b‖ = 1}` (a 3-dimensional family of 2-dimensional fibres `S^1 × S^1`) gives (★)
for a.e. unit pair: if `|Q i a| > 0` and `|Q i b| > 0`, the set
`{(s,f) ∈ Q i a × Q i b : b - a ∦ s}` has measure `2π|Q i b| > 0` (the excluded `s` are `±(b-a)`),
so it meets the null set `Bad_i` in the fibre's complement, exhibiting `s ∈ Q i a`, `f ∈ Q i b` with
`‖a - b‖ = 1` and `b - a ∦ s`, which (P2) forbids.  ∎

**CHECK 5 (`collapse_check.py`, exact).**  (★) does **not** imply k-colourability: the point set
`B = {(t, 3k/2) : t ∈ ℝ, k ∈ ℤ}` (parallel lines, spacing `3/2 > 1`) has, at each of its points,
exactly two points of `B` on the unit circle (a null set of directions) and yet contains the unit
pair `(0,0)-(1,0)`.  Correspondingly, for a palette field supported on such a set the pairs
`(a,b)` with both `a, b ∈ B_i` form a set of measure zero in the 3-dimensional family of unit pairs.
So (★) — the whole measurable content of (P2) — is satisfied by structures that are not colourings.

**Corollary D (where the k = 6 problem lives).**  `CAP_ae(k)` is *not* shown equivalent to
k-colourability by (P0)+(P2)+(P3); the measurable a.e. form yields only (★), which is strictly
weaker.  Hence:

* `CAP(k)` (pointwise) is equivalent to `χ ≤ k` — Theorem 1, and it decides `k = 5` (Corollary B).
* `CAP_ae(k)` is the only palette class left in which an L4 no-go could be true, and neither its
  satisfiability nor its unsatisfiability at `k = 6` follows from anything here or in the paper.
  Note that W1 gives unsatisfiability of `CAP(5)` only (via Theorem 1); it gives nothing about
  `CAP_ae(5)`, since (P2) does not yield a colouring.
* Adding (P3) does not remove it from that position: (P3) buys (★) only.

This is the precise sense in which the whole k = 6 failure of the palette side is the *a.e.
quantifier* of Lemma 5.2(3), and not the value of any constant, the cover mesh, the multiplicity, or
the cardinality bound.

---

## 6. Specification: falsifiable requirements for a replacement mechanism

Each item is a requirement with a test that can fail, derived from §3–§5.

**S1 (no collapse).**  The invariant `I_k` must be strictly weaker than (P0)+(P1) in this exact
sense: there must exist an explicit structure `X` with `I_6(X)` true on which Step 2 of Theorem 1
fails, i.e. some circle-point `a` carries two labels whose direction sets are both outside every
antipodal pair while `∪_i D_i(a) = S^1` remains true.  *Test:* run Steps 1–2 of Theorem 1 on `X`.
If the rigidity goes through, `X` *is* a 6-colouring and `I_6` collapses.  *Detected failure modes:*
any mechanism whose only hypotheses are (P0)+(P1).

**S2 (no cardinality-only k-dependence).**  `I_k` must not be (P0) plus a bound `|P| ≤ b(k)`: by
Corollary C the cardinality bound is invisible to the collapse.  *Test:* replace `b(k) = k-3` by an
arbitrary `b : ℕ → ℕ` with `b(k) ≥ 1`; if the derived contradiction is unchanged, the mechanism is
cardinality-only and inherits Corollary C.  This is the falsification test for route B.

**S3 (k-sensitivity in a structural slot).**  There must be an explicitly computed family on which
`I_6` holds and `I_5` fails by a mechanism other than `b(k)`.  *Positive example, computed exactly:*
the rigidity invariant of Theorem 1 satisfies S1 and S3 and is calibrated at `k = 7` by CHECK 4 —
but it forecloses L4, since by Theorem 1 it decides `k` exactly when the problem is decided.  The
present method cannot even do this: at `k = 7` its cover step needs multiplicity `≤ k-3 = 4`, and
W4's explicit multiplicity-3 cover of Euclidean mesh 2 meets that hypothesis, so the §7 step is
unavailable for **every** `k ≥ 6`, not only `k = 6`.

**S4 (cover components must survive multiplicity 3).**  Any cover-theoretic component must be valid
at multiplicity `3`, mesh `< 5`.  By R4 and W4 the present shape cannot be: W4's triangular-lattice
cover (radius-1 discs at spacing `6/5`, covering radius `0.6928 < 1`, nearest non-vertex at
`√3·(6/5)/2 = 1.0392 > 1`) is a relatively open multiplicity-3 cover of `[-5,5]^2` of mesh 2.
*Test:* instantiate the component on that cover; it must not derive a contradiction, because the
configuration is realised.

**S5 (interface states must break bipartiteness).**  Any state-based component must handle the
six-state, non-bipartite transition system of W6 at the triangle interface; the two-colouring of the
state graph (the "binary flip" of §8) is unavailable at `k = 6`.  *Test:* W6's transition graph
contains the triangle `{x}→{y}→{z}→{x}`.

**S6 (cycle length 6 excluded or shown absent).**  By Prop. 7.1 the method needs all `3 ≤ ℓ ≤ k`; at
`k = 6` the case `ℓ = 6` is new and §8 has no argument for it.  *Test:* exhibit a derivation for
`ℓ = 6`, or prove the case cannot occur.

**S7 (must be non-trivial without joint measurability, and stronger than (★)).**  By Theorem 2 and
CHECK 5 a mechanism that assumes joint measurability in the centre gains only (★), which structures
that are not colourings satisfy.  So a replacement must (a) be statable without joint measurability,
and (b) exclude at least one object satisfying (★) — e.g. it must not be satisfied by "palette support
contained in a union of parallel lines".  *Test:* check the mechanism against the CHECK 5 witness.

---

## 7. What is proved, and what is not

**Proved here.**  Theorem 1, complete proof, machine-checked for all `k` (no measurability, no
cardinality bound, no compactness, no density).  Corollaries A, B, C.  Theorem 2 with complete proof
(Fubini steps supplied by (P3)).  CHECK 1–5, exact.  The all-`k ≥ 6` cover observation in S3, from
W4 + R4 alone.

**Not proved, and not claimed.**  (i) No L4 no-go is established for `CAP_ae(6)`: it is the only
palette class not shown equivalent to the problem, and it is neither shown satisfiable at `k = 6`
(which would not by itself give a colouring) nor unsatisfiable.  (ii) No 6-chromatic graph, no
6-colouring, no `χ ≥ 7`.  (iii) §6–§8 of the paper are not re-derived; S4–S6 cite R4, W1, W4, W6.
(iv) The statement in Corollary A is about the *palette-transfer* inputs; the paper's own route uses
more — in particular (5.2) applied to the actual colouring, which is what makes Prop. 5.6
non-vacuous — and nothing here says the paper's §6–§8 argument has a defect.
