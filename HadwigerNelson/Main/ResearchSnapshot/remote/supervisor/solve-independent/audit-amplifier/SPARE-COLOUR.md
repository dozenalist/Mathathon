# The spare-colour obstruction, and why the level-5 target is the valuable one

Analysis only. No solver, no Lean, no nested agents. One hand-checkable pattern enumeration (below).
**No unconditional gadget is claimed; nothing here is evidence of new forcing.**

## 0. Corrections to `COMPOSITION.md` (Lemma C's scope)

1. **Terminal satisfiability is not global colourability.** My non-vacuity "check" coloured only the five
   terminals `u,v,w_1,w_2,w_3`. That shows the *terminal-level* constraint set is satisfiable; it is **not**
   evidence that `G` is `k`-colourable. In Lemma C, `Omega_k(G) != empty` is a hypothesis about the whole
   graph and must be discharged separately. Conflating the two would be exactly the error the project has
   had to repair elsewhere (a patch colouring is not a plane colouring).
2. **`w_i` need not differ from `alpha` when `c(u) = c(v)`.** Unless an explicit edge `u w_i` (or `v w_i`)
   is present, `w_i` may take the same colour as `u,v`. So my "`4 <= k`" was wrong: the terminal-level
   minimum is **3** colours (the three `w_i` are pairwise adjacent, so need three distinct colours, and one
   of them may be `alpha`). It is 4 only in the special case where `u` or `v` is adjacent to all three
   `w_i`. *Sharpening:* in a **5-colourable** graph an NR-6 triple forces `u,v` non-adjacent to all `w_i`
   automatically (§2 Cor. 1 + monochromaticity would contradict an edge), so under the 5-colourable
   hypothesis the 4-colour case cannot arise.
3. **Level 5 is not useless — this was a scope error on my part.** I wrote that since `chi(R^2) >= 6` is
   already proved, an NR-5 triple "buys nothing". That confuses *proved* with *cheaply proved*. The
   supplied lower bound is a 62-page analytic argument; an **explicit, exactly coordinated, finite
   non-5-colourable unit-distance graph** would replace it by a finite machine-checkable certificate —
   a direct win on the simplification objective, even though it does not decide 6 versus 7. §3 makes
   this precise.

## 1. The spare-colour lemma

**Lemma S.** Let `G` be a finite graph, `k >= 2`, `T = {a,b,c} ⊆ V(G)`. Suppose
  *(i)* `G` is `(k-1)`-colourable, and
  *(ii)* `T` is NR-k, i.e. no proper `k`-colouring of `G` gives `T` three distinct colours.
Then `T` is **monochromatic in every proper `(k-1)`-colouring** of `G`.

*Proof.* Let `c` be a proper `(k-1)`-colouring, whose palette is `[k-1] ⊆ [k]`. Case 1: `T` has 3
distinct colours under `c`; then `c` is itself a proper `k`-colouring rainbow on `T`, contradicting (ii).
Case 2: `T` has exactly 2 distinct colours under `c`; two of `a,b,c` share a colour, say `c(a) = c(b)`;
recolour `a` to the **fresh** colour `k`. Colour `k` is used by no other vertex, so no edge becomes
monochromatic: the recolouring is a proper `k`-colouring. It is rainbow on `T` (colours `k, c(b), c(c)`,
pairwise distinct) — contradicting (ii). Case 3: `T` is monochromatic under `c`, which is the assertion. ∎

**Sharpness.** The monochromatic case genuinely survives: recolouring one vertex of a monochromatic triple
to a single fresh colour leaves only two colours on `T`. Two fresh colours would be needed, and only one
is available. Enumerated over all three patterns and all three recolouring choices, for `k = 5` and
`k = 6`: pattern `(1,1,1)` never becomes rainbow, `(1,1,2)` becomes `(k,1,2)`, `(1,2,3)` was already
rainbow. So "monochromatic" is exactly the surviving pattern, and Lemma S is one-directional — it is a
*necessary* condition, hence a filter, not a characterisation.

**Why the recolouring is legitimate.** No counting or structural condition is used beyond the freshness of
colour `k`: it appears in no vertex, so it collides with nothing. This is why the lemma needs only
`(k-1)`-colourability of the whole graph and no local hypothesis at all.

## 2. Two corollaries, the second stronger than the first

**Corollary 1 (a single triple, given pair separation).** If `G` is `(k-1)`-colourable **and** every pair
of vertices is separated by some proper `(k-1)`-colouring, then `G` has **no** NR-k triple.

*Proof.* Let `T = {a,b,c}` be NR-k. By Lemma S every `(k-1)`-colouring is monochromatic on `T`. But pair
separation gives a `(k-1)`-colouring with `c(a) != c(b)`, so `T` is not monochromatic. ∎

**Specialisation to the project's actual objects.** `G_553` is 5-colourable (it is 5-chromatic), and
(Sep_5) is verified for it by the 34-witness chase. Take `k = 6`, so `k-1 = 5`:

> **`G_553` admits no NR-6 triple. Not one, anywhere.** Not merely "none found" — none can exist.

That closes `(M4)` of `COMPOSITION.md` on Heule 553 outright, and with it the k = 6 instance of the
arity-3 route *on that graph*.

**Corollary 2 (the whole composition, and stronger: no pair separation needed).** Let `G` be
`(k-1)`-colourable with `u,v` and `w_1,w_2,w_3` pairwise adjacent, each `{u,v,w_i}` NR-k. Then no such
configuration exists.

*Proof.* Take any proper `(k-1)`-colouring `c`. By Lemma S each `T_i` is monochromatic under `c`, so
`c(u) = c(v) = c(w_i)` for every `i`; hence `c(w_1) = c(w_2) = c(w_3)`, contradicting pairwise
adjacency. ∎

Corollary 2 uses no pair separation, only `(k-1)`-colourability. Specialised at `k = 6`:

> **The three-witness composition cannot live in any 5-colourable graph.** Hence realising it requires a
> finite unit-distance graph that is 6-colourable and **not** 5-colourable — i.e. exactly 6-chromatic.

## 3. The dependency, and why level 5 is the valuable target

Corollary 2 makes the k = 6 route **presuppose** its own prerequisite: to run Lemma C at `k = 6` you must
first have an explicit exactly-6-chromatic finite unit-distance graph. That object is not in hand:

* `G_553` is **5**-chromatic, so it certifies only `chi(R^2) >= 5`.
* The paper's `chi(R^2) >= 6` is analytic; by de Bruijn–Erdos it entails *some* finite non-5-colourable
  unit-distance graph, but the argument exhibits none. Extracting an explicit one is open.

So the k = 6 arity-3 route is not a shortcut: it is downstream of the cheaper target. That cheaper target
is level 5, where the obstruction of Lemma S **does not apply** (`G_553` is not 4-colourable, so the
"`(k-1)`-colourable" hypothesis fails at `k = 5`):

> **Level-5 route (live).** An NR-5 triple in `G_553` — not excluded by anything above — feeds Lemma C at
> `k = 5`, giving a forced-equal pair at level 5; the audited amplifier then produces a finite
> unit-distance graph that is **not 5-colourable**, with exact coordinates in a quadratic extension of the
> gadget's field (`K' = K(sqrt(4n^2 d^2 - 1))`) and at most `2nV - 2n + 1` vertices.

That is precisely an **explicit 6-chromatic finite unit-distance graph**: a short, finite, machine-checkable
certificate for `chi(R^2) >= 6`, replacing a 62-page analytic argument. It does not decide 6 versus 7, and
it does not need to — reducing the length and trust surface of the lower bound is the user's simplification
objective, and this is the one route on the table that could deliver it.

## 4. Realizability / non-vacuity specification for composing three NR gadgets

The composition is legitimate because of one monotonicity fact, which must be used explicitly:

**(MON)** NR is preserved under extension. If `T` is NR-k in `H` and `H ⊆ G` (same vertex set on `T`,
any extra vertices/edges), then `T` is NR-k in `G`: every proper `k`-colouring of `G` restricts to one of
`H`, which is non-rainbow on `T`. So gluing gadgets never destroys an NR fact.

What gluing **can** destroy is global colourability — the mirror image of (MON). Hence the specification:

> **(S)** A composition of three NR gadgets with common `u,v` and a unit triangle `w_1,w_2,w_3` is a datum
> `(G; u, v, w_1, w_2, w_3; H_1, H_2, H_3)` with:
> 1. **Exact geometry.** `G` a finite set of points in `K^2` for a number field `K` of finite degree; all
>    coordinates exact; the only admissible test is "squared distance `= 1`" as an identity in `K`.
> 2. **The triangle.** `|w_i - w_j| = 1` for `i < j` (so `w_1,w_2,w_3` are the vertices of a unit
>    equilateral triangle; this pins them up to isometry).
> 3. **Terminals.** `u != v`, `|u - v| != 1` (forced: Lemma C gives `c(u) = c(v)`, which a unit edge
>    would contradict, so `G` would not be `k`-colourable and (S6) would fail).
> 4. **Sub-gadgets.** `H_i ⊆ G` with `u, v, w_i ∈ V(H_i)`, and `{u,v,w_i}` NR-k **in `H_i`**; by (MON) this
>    transports to `G`.
> 5. **Accident audit on the assembled graph** — three classes, each decided exactly:
>    (a) *coincidences*: any two of the `|G|` points equal (this silently merges terminals or collapses a
>    `w_i`, and must be excluded or accounted for);
>    (b) *accidental unit edges between different gadgets, or gadget-to-terminal*: these are harmless for
>    (S4) by (MON), but they can destroy (S6), and an edge `u w_i` or `v w_i` would make `T_i` non-independent
>    (permitted in principle, but then Lemma S's 4-colour case of §0(2) applies and the terminal minimum
>    rises);
>    (c) *accidental unit edges that make some `{u,v,w_i}` a triangle*: impossible while `u,v` is a non-edge,
>    and if `|u - v| = 1` arose by accident then no colouring exists at all.
> 6. **Global colourability — a separate obligation.** `Omega_k(G) != empty`, established for the
>    **assembled** graph. This is *not* implied by any terminal-level colouring (§0(1)) and *not* implied by
>    `Omega_k(H_i) != empty` for the parts, since (MON)'s dual failure is exactly here. Per Lemma S this is
>    the hard condition: at `k = 6` it forces `G` to be non-5-colourable (§2 Cor. 2).
> 7. **Exhaustiveness of the edge set.** `E(G)` is the full induced unit-distance graph of the point set —
>    no "selected" edges. (`(S5b)` is the reason: unlisted accidental edges change the colouring space.)

The condition that carries all the difficulty is (S6); everything else is bookkeeping or free placement.
I assert nothing about whether (S) is satisfiable — that is the open problem.

## 5. Grades

| item | grade |
|---|---|
| corrections in §0(1),(2) | **self-corrections**; the `4 <= k` figure of `COMPOSITION.md` is withdrawn, correct terminal minimum is 3 (4 in the stated special case) |
| correction §0(3) | **self-correction of scope**; level 5 is a live and valuable target |
| Lemma S | **proof** (case analysis; freshness of colour `k` is the whole content) |
| sharpness (monochromatic is the only survivor) | **exact pattern enumeration**, 3 patterns × 3 recolourings × `k in {5,6}`; no graph, no solver |
| Corollary 1 and the `G_553` no-NR-6 statement | **proof**, using `G_553` 5-colourable + verified (Sep_5) |
| Corollary 2 and "needs a 6-chromatic graph at level 6" | **proof** |
| level-5 route value | **proof** of the implication chain (Lemma C + audited amplifier); the *existence* of an NR-5 triple in `G_553` is **open**, and the amplification's coordinates/exactness are per the audited `AUDIT.md`, not re-derived here |
| `(MON)` and specification (S) | **proof** of monotonicity; (S) is a specification, not an instance |
| any new forcing | **none** |

**Limitations.** Lemma S needs `(k-1)`-colourability of the whole graph; it says nothing where that fails,
which is exactly why it is silent at level 5 on a 5-chromatic graph. The no-NR-6 result is about `G_553`
(and any 5-colourable pair-separating graph), not about all graphs. No NR-5 triple is known; none is
claimed. No computation beyond the pattern enumeration.

## 6. Consequence for planning

The arity-3 seed has one live instance, at level 5, and its payoff would be a finite exactly coordinated
non-5-colourable unit-distance graph — a shortening of the analytic lower bound, not a decision of
6 versus 7. The level-6 instance is *not* available on `G_553` at all, and in general presupposes the very
object the level-5 route aims to build. I would not pursue level 6 before level 5 is settled.
