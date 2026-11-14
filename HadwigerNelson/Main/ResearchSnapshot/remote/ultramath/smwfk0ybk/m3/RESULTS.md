# The tightened interface CSP at k = 6 is SATISFIABLE — Step 1 is decided, negatively

m3, swarm `smwfk0ybk`, direction d16. Files in this directory. Every claim below is a proof or an
exhaustive computation with a check command; nothing depends on the INDUCTION LEMMA.

## 0. Answer to the decisive question

> With (C4) and (C5) added, is there ANY satisfiable (l, sign matrix) at k = 6?

**Yes.** There are 654 of them out of 9324, and at l = 3 and l = 4 there is a closed-form witness
valid for *every* ray geometry and every `k >= l+2`. So the branch "UNSAT for every l and every sign
matrix" is empty: the tightened CSP cannot prove `chi(R^2) >= 7`, at k = 6 or at any other k, and
no induction lemma is needed to see that. The SAT branch is the live one, and the mission's own
instruction applies: report the models and what they violate, as the input to the (C6) round (§5).

## 0b. Agreement with the rest of the swarm (independent, same answer)

m6 (d1, `f2`/`f27`, `TightCore.lean`) and m10 (d2, `f1`) reached the same verdict independently. Our
three computations agree on all 9324 instances. m6's `TightCore.lean` is the stronger *general*
statement and my closed-form family is a special case of it: **coordinatewise shrinking**. Given any
(C1)-(C3) model, replace `P_i` by `{c}` if `P_i ∩ O_i ∩ I_i ≠ ∅`, else by `{a,b}` with
`a ∈ P_i ∩ O_i`, `b ∈ P_i ∩ I_i` (`a ≠ b` because `P_i ∩ O_i ∩ I_i = ∅`). The result is nonempty,
has size `<= 2 <= k-3` (needs `k >= 5`), still meets both slivers, is a subset of `P_i` so inherits
(C3), and has no 3-set, so (C4) and (C5) are vacuous. Hence `(C1)-(C5)` is satisfiable iff
`(C1)-(C3)` is, for every `k >= 5` and every length. I re-derived this argument and then compiled
m6's file in my own directory: `lean check_TightCore_copy.lean` (a copy of `../m6/TightCore.lean`)
exits 0 and `#print axioms` gives `[propext, Classical.choice, Quot.sound]` for all eight theorems,
so no `sorryAx` and no `native_decide`. My closed-form family of §1 is not subsumed in value: it is
what identifies *why* the tightening is inert — the outsiders lie in both slivers — and it is the
family that any candidate (C6) must kill (§5).

What my computation adds to theirs: exact **model counts** (not just SAT/UNSAT), the third
independent decision procedure, and the encoding check against the paper's literal definition in §4.

## 1. The witnesses, and why they exist (closed form, no search)

Paper §8.1 defines, verbatim: *"Let `O(e)` be the set of labels remaining after the endpoints of
every positive edge are removed, and let `I(e)` be the set remaining after the endpoints of every
negative edge are removed. Labels outside the cycle belong to both sets."*

Let `U = {l, l+1, ..., k-1}` be the labels outside the cycle. The paper's last sentence is

  **(S)  `U` is contained in `O(e)` and in `I(e)`, for every direction `e` outside `B`.**

**Theorem.** Let `k >= l+2` with `l in {3,4}` (so `k >= 5` for `l = 3`, `k >= 6` for `l = 4`), and
let `(c_0..c_{l-1})` be any ray geometry. Then the palettes

    P_i = {l}        for i even
    P_i = {l+1}      for i odd                     (six positions i = 0..5)

satisfy (C1)-(C5): at k = 6, l = 3 they are `{3},{4},{3},{4},{3},{4}`, and at l = 4
`{4},{5},{4},{5},{4},{5}`.

*Proof.* `l` and `l+1` lie in `U = {l, ..., k-1}` because `l+1 <= k-1`. By (S), `P_i` is contained in
both `O_i` and `I_i`, so `P_i ∩ O_i ≠ ∅` and `P_i ∩ I_i ≠ ∅` (C2). `1 <= |P_i| = 1 <= k-3` (C1).
Consecutive palettes are `{l}` and `{l+1}`, and so are the cyclic pair `(5,0)`: all
intersections are empty (C3). Every palette is a singleton, so no two palettes cover `Fin k`
(`|A ∪ B| <= 2 < k`) — this is (C4), and it is the *general-k* form of pair exclusion, not only the
k = 6 form. (C5) holds because no palette is ternary, hence no palette of size `k-3 = 3`. ∎

So the pair-exclusion constraint (C4) and the orbit bound (C5) *never bite at l = 3 or l = 4, for any
k*. Verified: `uniform_witness.py` checks the two families against every clause of (C1)-(C5) on
36/36 and 216/216 geometries at k = 6 (and `extract_witnesses.py` checks the same two against the
paper's literal definition of `O`, `I`, below).

## 2. Exact counts over all (l, sign matrix) at k = 6

Instance count is `6^(l-1)` (`c_0 = 0` fixed by the `pi/3` rotation symmetry, as in m5).

| l | instances | (C1)-(C3) SAT | (C1)-(C5) SAT | SAT with all `|P_i| <= 2` | tightened models | of which binary |
|---|---|---|---|---|---|---|
| 3 |    36 |    36 |    36 |    36 |  30 976 992 | 5 258 520 |
| 4 |   216 |   216 |   216 |   216 |  26 094 140 | 2 979 348 |
| 5 |  1296 |   225 |   225 |   225 |     571 070 |    35 320 |
| 6 |  7776 |   177 |   177 |   177 |      11 648 |     1 728 |
| total | 9324 | 654 | **654** | **654** | 57 653 850 | 8 274 916 |

The (C1)-(C3) column reproduces m5's accepted table `36/36, 216/216, 225/1296, 177/7776` exactly,
from a different implementation. The (C1)-(C5) column equals it: **the tightening kills no
instance**. The fourth column equals it too: **every satisfiable instance has a model with all six
palettes of size <= 2**, on which (C4) and (C5) are vacuous. By-products (same program): k = 4 gives
0/36, 0/216; k = 5 gives 36/36, 14/216, 0/1296 (again m5's table); k = 7 gives all of l = 3,4,5
satisfiable and 2593/7776, 4109/46656 at l = 6, 7, every satisfiable one with a binary model (k = 7
there uses the k = 6 form of (C4), so it is not evidence about the general-k pair exclusion; the
theorem of §1 settles l = 3,4 at every k independently).

## 3. Model-level strength versus instance-level strength

(C4) is **not** implied by (C1)-(C3) as a constraint on models: `model_vs_instance.py` exhibits, for
each l, an explicit (C1)-(C3) model of a satisfiable instance containing a complementary pair — e.g.
at l = 3, `cells = (0,0,0)`, model `{3},{4},{3},{4},{0,1,3},{2,4,5}`, complementary pair `(4,5)`.
And (C5) *is* implied by (C3)+(C4) at k = 6, so it is not an independent constraint: two disjoint
3-sets in `Fin 6` are complementary, so (C3) and (C4) together forbid any two ternary palettes from
being disjoint, and consecutive positions are disjoint; ternary positions are therefore an
independent set of the 6-cycle, of size at most 3. So m6's Theorem 2 adds nothing at the CSP level.
What remains is the exact statement of this section: the tightening changes the *model class* and
not the *set of satisfiable instances*.

## 4. Two decision procedures, their agreement, and the encoding check

* `csp_vacuity.py` — backtracking over the six positions, (C4) checked pairwise at insertion; runs
  the search three times per instance ((C1)-(C3); (C1)-(C5); sizes <= 2). 1.2 s for all 9324
  k = 6 instances.
* `csp_count.py` — a forward DP over states `(previous palette, set of ternary palettes used)` that
  **counts** models rather than deciding; 22 s. The two agree instance by instance, and the counts
  in the last two columns of the table are exact integers from the DP.
* Encoding check, `paper_defs.py` — the sliver sets recomputed from the paper's literal definition
  (`O(e) = [k] minus the endpoints of every positive edge`, `I(e)` likewise for negative edges)
  agree with m5's encoding on **402 624** (k, l, geometry, position) triples with **0 mismatches**,
  and property (S) holds on every one. This is the only place my conclusion touches m5's encoding,
  and it is a positive check.
* `extract_witnesses.py` — writes an explicit witness for each of the 654 satisfiable k = 6 instances
  to `witnesses_k6.json`, and re-verifies each one against the paper's literal `O`, `I` and against
  every clause of (C1)-(C5); `all_witnesses_binary` is true at every l.

Check command (about 30 s):
`cd .ultramath/smwfk0ybk/m3 && python3 paper_defs.py && python3 general_k.py && python3 extract_witnesses.py && python3 csp_vacuity.py 6 && python3 csp_count.py && python3 uniform_witness.py && python3 model_vs_instance.py`

`general_k.py` is the closed-form theorem of §1 checked directly for k = 4..9: 1044 geometries,
0 failures.

## 5. What the (C6) round must do — the precise target

A constraint that is to rescue the CSP route has to be violated by the families of §1. Since those
palettes are singletons drawn from `U` and alternate, any candidate (C6) that is a function of
palette *sizes*, of consecutive disjointness, or of "meets the slivers" is dead on arrival: it is
satisfied by `{l},{l+1},{l},{l+1},{l},{l+1}` at every geometry and every `k >= l+2`. Equivalently —
this is m6's shrinking lemma (`f27`), which is stronger and needs no explicit family: *every*
(C1)-(C3) model shrinks to one with all `|P_i| <= 2`, so no constraint can bite unless it is
violated by some model with `|P_i| <= 2` at every `i`. Concretely, a successful (C6) must exclude, at
k = 6 and l = 3, the model `{3},{4},{3},{4},{3},{4}` for all 36 sign matrices — so it must forbid
*singleton palettes* (a genuine lower bound on `|P_x(e)|`), or it must tie the palette to data the
six-position system does not see.

Two honest observations about where such a constraint can come from.

1. The paper's own exclusions of length 5, 4, 3 are Propositions 8.2, 8.5, 8.10. Of these only
   Proposition 8.2 is "CSP-shaped": its proof runs entirely inside the palette-pair structure plus
   (5.7), and indeed the (C1)-(C3) system already reproduces it (`k = 5, l = 5: 0/1296`). Propositions
   8.5 and 8.10 are not: 8.5 runs on the cross-word restriction, the compact essential supports and
   the projective arc geometry of Lemma 8.4; 8.10 runs on a *spatial* gadget (the seven-vertex Moser
   spindle in the polynomial three-label region (8.4), Lemma 8.8/8.9). Both use the two-dimensional
   geometry of the plane, which no single-centre palette system encodes.
2. At k = 6 the l = 3 argument is the one that really changes shape. Lemma 8.8's region is restricted
   to the three triangle labels because both outsiders are excluded at the sum of two directions;
   at k = 5 there are exactly two outsiders, at k = 6 there are three, and the sum excludes at most
   the two outsiders attached to the two endpoints. So the region is not restricted to the triangle
   labels and the Moser obstruction does not transfer as stated. This is consistent with the
   computation: at l = 3 the tightened CSP is satisfiable on every geometry, so the missing
   constraint there is not palette-combinatorial.

I do **not** claim a no-go for `l in {5,6}`: 402 of those 9072 instances are satisfiable and a (C6)
could still kill them. I claim only that `l in {3,4}` is closed to this method (proved, all k), that
(C4)+(C5) close nothing at k = 6 (exhaustive), and hence that the mission's decisive question has
answer YES. Note also m6's `f16`/`f20`: adjoining a second centre at a unit translate, with
cross-centre disjointness `P_y(f) ∩ P_x(f) = ∅` from Lemma 5.2(3)+Remark 5.3, and even a third centre
on a chain, stays satisfiable for all 654 of the satisfiable geometries. So a finite-centre (C6) is
dead too; the only remaining object of that shape is m8's full a.e. palette system, which is the
problem.

## 6. Which terminal outcome this reaches (d16's deliverable)

Read against the standing brief's own texts. My work reaches no L1-L2 and cannot; here is the exact
state of each, with the reason.

* **L1, L2** (explicit finite unit-distance graph with `chi(G) = k` plus an explicit `k`-colouring,
  or one half of it): untouched. Nothing in this note produces a graph or a colouring.
* **L3 (certified finite reduction): the CSP candidate is certified dead, and this is the sharpest
  negative result of the run.** L3's first form needs a finite `P` with a machine-checked
  "`P` unsatisfiable implies `chi >= 6`" (or `>= 7`). The tightened interface CSP was the leading
  candidate for `P`, because it is a relaxation with only 9324 instances and an UNSAT verdict would
  have been decisive. It is satisfiable at *every* k, so no such implication exists on this route —
  and by m6's shrinking lemma this is a theorem about the whole (C1)-(C5) level, not a fact about
  k = 6. L3's second form (`P` satisfiable with an exhibited solution implies `chi <= 6`) is not
  reachable from a relaxation at all: it needs `P` to be *equivalent* to the colouring problem, which
  by m8's collapse is only the full a.e. palette system, whose satisfiability is the problem.
* **L4 (certified no-go plus specification): the no-go class is extended and one specification item
  is added.** The accepted L4 (`L4-SYNTHESIS.md`) certifies that the six-step relaxation cannot
  decide k = 6 and lists S1-S7 for a replacement. This note adds: (i) the no-go survives m6's two
  orbit constraints, at every `k >= l+2` for l in {3,4} (proof) and exhaustively at k = 6 for l in
  {5,6} — so the tightening was never an input, only a rename; (ii) a new falsifiable item in L4's
  format: **S8 — a replacement must be violated by all-singleton palettes drawn from the outsiders.**
  *Refuted by:* the explicit family `{l},{l+1}` alternating, which satisfies every existing clause at
  every geometry and every `k >= l+2`; equivalently (m6's shrinking) by the fact that every
  (C1)-(C3) model has a model with `|P_i| <= 2` underneath it. Any replacement that does not force
  `|P_x(e)| >= 2` (or import a second, non-finitely-generated centre) fails before it starts. This
  is exactly the item that the §6/§7 chain needs and does not have at k = 6 — m6's `INDUCTION.md`
  identifies the missing premise as (H7), Prop 7.1's cycle extraction, which at k = 6 needs `|P| <= 2`
  (the binary centre) and a multiplicity-2 cover, neither of which is available (the second is my
  predecessor's COVER NO-GO).
* **L5 (calibration and irreducibility): unreached, with a certified obstruction.** L5 asks the
  machinery to reproduce `chi >= 5` "through its own route, with an explicit finite witness". The
  previous run's m2 already showed the §5-§8 architecture is *empty* at k = 4 (the cyclic-centre locus
  vanishes), and §5 here shows it is permanently satisfiable at k = 6 for l <= 4; the machinery
  therefore cannot even reproduce `chi >= 5`, which needs k = 4, let alone `chi >= 6`. The
  irreducibility half was done in the previous run (m4, Prop 8.2 = the palette level at (5,5)).

So: **the run reaches L4-for-the-tightened-class, and it certifies that Step 1's decisive
computation is answered in the negative for every k — Step 1 can never yield `chi >= 7`.** The only
live route to `chi >= 7` in this project is no longer a finite relaxation; it is the full a.e. palette
system (m8), i.e. the problem.

## 7. What is not verified here

* The INDUCTION LEMMA (that every weak measurable 6-colouring induces a (C1)-(C5) model) is not
  proved here — d2 and m6's `INDUCTION.md` own it. My conclusion does not need it: SAT of the
  relaxation refutes the UNSAT branch of the mission whatever the induction lemma says.
* I have not verified m6's orbit lemmas themselves; I test their *CSP-level consequences* (C4) and
  (C5) as stated in the mission, and (C5) I show to be implied by (C3)+(C4).
* k = 7 numbers in §2 use the k = 6 form of (C4) and should not be read as a calibration; m6's `f18`
  is right that the k-general form has size pairs (4,4), (4,3) at k = 7 and is not proved there.
* The claim in §5 that Proposition 8.10's three-label region degrades at k = 6 is a reading of the
  paper (Lemmas 8.8, 8.9 and the k = 5 assertion "there cannot be two outsiders in such a palette"),
  not a formalised theorem.
