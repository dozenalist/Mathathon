# Composing forced non-rainbow triples: what works, what does not, and the exact missing realisation

Analysis only. No SAT, no solver, no Lean, no computation beyond a hand-checkable finite count. One
input uses the graph worker's compute slot; nothing here queues behind it. Status of every claim is
graded in §6. **No unconditional gadget is asserted. No new forcing is claimed.**

## 0. Corrections to the previous block, before anything is built on it

1. **(C) repaired.** The form "every relation set has a realising colouring" is false as stated —
   arbitrary relations contradict each other (`c(u)=c(v)` together with `c(u)!=c(v)`). It is replaced
   by the **extension property** below, which is what the W6 example actually refutes.
2. **"Arity 3" is about joint unsatisfiability, not about the constraint language.** I previously wrote
   that an anti-rainbow triple "cannot be explained at arity 2 at all" / was a "genuine three-way
   phenomenon". That was imprecise and is corrected in §3: **every constraint here is binary** (an edge
   is one disequality; "rainbow on `T`" is exactly three pairwise disequalities on `T`). What is
   arity-3 is that the three pair-projection constraints on `T` are *jointly unsatisfiable while each
   pair is individually satisfiable elsewhere in the graph*.
3. **The common-neighbour argument is withdrawn.** I argued from `max common neighbours = 2` that the
   only available device forcing a pair equal is the diamond type. That does not follow: a common-
   neighbour count cannot exclude other forcing mechanisms. The operative fact is the *verified* one —
   no pair of `G_553` is forced equal at any `k >= 5` — and I rely on that alone, not on any mechanism
   classification.
4. **W6 used only for what it shows.** `W6` (centre + hexagon, `k = 4`) exhibits (A) `=>` not-(C): every
   pair is separable, yet a locally consistent partial assignment fails to extend. Its mechanism is a
   **palette exhaustion at a star** (the hub is adjacent to all six rim vertices), i.e. precisely the
   kind of common-neighbour palette constraint whose general exclusion is not available. So `W6`
   illustrates the *logical* gap and is **not** evidence for any higher-arity phenomenon in `G_553`. It
   is also a different graph and a different palette (7 vertices, `k = 4`) from `G_553` at `k = 5`;
   nothing transfers.
5. **Pair projections establish nothing at higher arity.** Conceded in full: the composition below does
   **not** infer anything from pair projections. It *assumes* the full triple-level facts.
6. **Non-vacuity is a standing obligation**, checked for every statement below: a hypothesis set that
   itself admits no proper `k`-colouring would make every conclusion vacuous.

> **REPAIR BANNER (later block, `SPARE-COLOUR.md` §0).** Three scope errors in this file are corrected
> there: (i) the "non-vacuity check" coloured only the five terminals, which shows terminal-level
> satisfiability and **not** that `G` is `k`-colourable — in Lemma C, `Omega_k(G) != empty` is a global
> hypothesis to be discharged separately; (ii) the claim that setting `c(u)=c(v)` forces the witnesses to
> need `4 <= k` colours is **wrong**: absent an explicit edge, `w_i` may take the same colour as `u,v`, so
> the terminal minimum is **3** (it is 4 only when `u` or `v` is adjacent to all three witnesses); (iii) the
> statement that a 5-level non-rainbow triple "buys nothing" because `chi(R^2) >= 6` is already proved is a
> **scope error** — an explicit finite non-5-colourable unit-distance graph would replace a 62-page analytic
> argument by a finite machine-checkable certificate, which serves the simplification objective. See
> `SPARE-COLOUR.md` §3. Lemma C itself is unchanged and remains correct.

## 1. The two properties, stated precisely

Let `G = (V,E)` be a finite unit-distance graph, `k >= 1`, and `Omega_k(G)` its set of proper
`k`-colourings.

* **(Sep_k)** for all distinct `p,q in V` there is `c in Omega_k(G)` with `c(p) != c(q)`. *(Verified for
  `G_553` at every `k >= 5` by the 34-witness chase.)*
* **(LC)** a partial assignment `sigma : S -> [k]`, `S` finite, is *locally consistent* when no edge of
  `G` has both endpoints in `S` with equal colours.
* **(Ext_k)** every locally consistent partial assignment extends to an element of `Omega_k(G)`.

**(Sep) and (Ext) are different, and (Ext) is not implied.** `W6` at `k = 4` satisfies (Sep_4) and fails
(Ext_4) on `sigma = {0|->1, 1|->2, 2|->3, 3|->4}`. Note also that (Ext) is a much stronger demand than
anything used below; the composition needs only *specific* simultaneous patterns, not all of them.

**Not-rainbow on a triple** `T = {u,v,w}` at level `k`: every `c in Omega_k(G)` has two of `c(u),c(v),c(w)`
equal. This is the conjunction of three binary disequalities being *unsatisfiable* over `Omega_k(G)`;
call such a triple a **non-rainbow triple** (NR-k). `T` must be independent, since a triangle is
rainbow in every colouring with `k >= 3`.

## 2. The composition: three non-rainbow triples force a pair equal

**Lemma C.** Let `G` be a finite unit-distance graph, `u,v in V`, and `w_1,w_2,w_3 in V` pairwise
adjacent, such that
  *(C-i)* `Omega_k(G) != empty` with `k >= 4`, and
  *(C-ii)* for each `i`, the triple `{u,v,w_i}` is NR-k.
Then `c(u) = c(v)` for every `c in Omega_k(G)`.

*Proof.* Suppose `c in Omega_k(G)` has `c(u) != c(v)`. For each `i`, (C-ii) says two of
`c(u), c(v), c(w_i)` agree; the first two differ, so `c(w_i) in {c(u), c(v)}`. The three `w_i` are
pairwise adjacent, so their colours are pairwise distinct; but they must all lie in the two-element set
`{c(u),c(v)}`. Three distinct values in a two-element set is impossible. ∎

**The count is exactly 3, and independent of `k`.** Checked by exhaustive case enumeration over
`c(u) != c(v)` for `k = 5` and `k = 6`: with `m <= 2` witnesses a colouring with `c(u) != c(v)` exists;
with `m = 3` none does. The argument never uses `k` except through (C-i): the palette for the witnesses
is always the *two-element* set `{c(u),c(v)}`. This is the crucial feature — **the composition is
`k`-independent once the triples are NR-k.**

**Non-vacuity (C-i) is real, not decorative.** Setting `c(u) = c(v) = alpha` satisfies all three
(C-ii) constraints outright, and then `w_1,w_2,w_3` need three distinct colours different from `alpha`,
so `4 <= k`. For `k = 5` and `k = 6` this holds. So the hypothesis set of Lemma C is satisfiable and the
lemma is not vacuous. (A hypothesis set with `u,v` adjacent would be unsatisfiable, and then "forced
equal" would be vacuous — excluded by (C-i).)

**What the composition is not.** It does not build new geometry. `u, v` are arbitrary vertices and each
NR-k fact is a statement about *all* colourings of `G`, so Lemma C is a relation-level implication
between global facts. It never decomposes an NR-k hypothesis into pair conditions — see §5.

## 3. Why this is not an arity-2 argument, stated correctly

Every constraint in the system is binary. What is arity-3 is this: for each `i` the three pair
constraints on `{u,v,w_i}` ("`u!=v`", "`v!=w_i`", "`u!=w_i`") are jointly unsatisfiable over
`Omega_k(G)`, although each is individually satisfiable *somewhere* — indeed (Sep_k) says each pair is
separable in some colouring. So NR-k is a **binary CSP with a non-extendable pair projection**, which is
exactly the phenomenon (Sep) does not see. I do not claim the constraint language is non-binary.

One further consequence worth stating, since it is what makes the hypothesis class non-trivial: if any
pair of `T` were forced equal, `T` would be NR-k *for that trivial reason*. Because (Sep_k) holds for
`G_553` at `k >= 5`, an NR-k triple of `G_553` could not arise that way. So on `G_553` the hypothesis of
Lemma C is a genuinely three-way condition. On a graph where (Sep) fails, it would be weaker and the
composition would be less interesting.

## 4. What the composition gives, and the obstruction that stops it

Feeding Lemma C's conclusion into the audited amplifier (Theorem A of `AUDIT.md`: a finite `k`-colourable
unit-distance graph with a distinct forced-equal pair yields a finite unit-distance graph that is not
`k`-colourable) gives the chain

    G k-colourable, Omega_k(G) != empty, three NR-k triples sharing {u,v}, witnesses pairwise adjacent
      ==>  u,v forced equal                          (Lemma C)
      ==>  a finite unit-distance graph that is not k-colourable   (Theorem A)
      ==>  chi(R^2) > k.

**The obstruction, at `k = 5`.** The chain terminates in "`chi(R^2) >= 6`", which is *already proved*
(`OAI.EuclideanFiveColor.no_proper_five_coloring`, and concretely `G_553` itself is a non-5-colourable
finite unit-distance graph). So a 5-level NR triple, even if realised, buys nothing: the strongest
conclusion the composition can reach at `k = 5` is a statement the project already has. Lemma C is
sound, and its 5-level instance is *useless*.

**The obstruction, at `k = 6`, is a transfer failure.** The composition would give `chi(R^2) >= 7`,
i.e. `chi(R^2) = 7` with the known upper bound. But:

> **NR-5 does not imply NR-6.** A triple that is non-rainbow at level 5 may be rainbow at level 6,
> because every proper 5-colouring is a proper 6-colouring but not conversely: a 6-colouring can use a
> third colour on `T` that no 5-colouring of `G` had available.

So the seeded relation (an NR triple established by 5-colourings, which is what the 34-witness machinery
is about) does **not** feed Lemma C at the only level where the conclusion is new. This is the exact
sense in which the arity-3 seed currently has no new consequence — not a defect of the composition, but
a level mismatch between the hypothesis the certificate can support and the level the conclusion needs.

## 5. The exact missing geometric realisation

To turn Lemma C into a proof of `chi(R^2) = 7`, the following must be exhibited — I state it as an
explicit shopping list and assert nothing about its satisfiability:

> **(M)** A finite unit-distance graph `G ⊂ R^2`, together with `u, v, w_1, w_2, w_3 in V(G)`, such that
> 1. `|w_i - w_j| = 1` for `1 <= i < j <= 3` (a unit equilateral triangle) — geometrically free: it exists;
> 2. `|u - w_i| != 1` and `|v - w_i| != 1` for all `i`, and `|u - v| != 1` (so each `{u,v,w_i}` is
>    independent, which NR-6 requires) — also free: place `u, v` generically away from the six unit
>    circles about `w_1,w_2,w_3` and about each other;
> 3. `Omega_6(G) != empty` (non-vacuity);
> 4. each triple `{u, v, w_i}` is **NR-6**.

**Where the difficulty is, exactly.** Conditions 1 and 2 are placement conditions and cost nothing.
Condition 3 is a chromatic upper bound on `G`, also nothing structural. **Condition 4 is the whole
content**: each NR-6 fact is a statement about *all* proper 6-colourings of the entire graph — a
universal property of `G`'s colouring space, not a local configuration. There is no local gadget that
delivers it: adding vertices and unit edges to force "not all three distinct" would have to be a gadget
whose own colourings already force a coincidence, and the only known such gadgets are the forced-equal
pair gadgets, which (Sep) rules out on `G_553` at `k >= 5`.

**Two independent gaps, kept separate.** (i) *Level*: the seed is a 5-level relation, (M) needs a
6-level one, and §4 shows there is no transfer. (ii) *Multiplicity*: even given one NR-6 triple, Lemma C
needs **three** of them **sharing the pair `{u,v}`** and with a triangle on the witnesses. A single NR
triple — the artifact I actually proposed — is one third of the hypothesis and says nothing about
whether the same pair can be completed to three.

**What would refute (M)?** A proof that for every finite unit-distance graph and every unit triangle of
vertices `w_1,w_2,w_3`, the colouring space has a 6-colouring that is rainbow on `{u,v,w_i}` for some
`i` — i.e. that NR-6 triples through a common pair cannot accumulate. I have no such argument, and I
explicitly do not claim (M) is impossible; it is simply unrealised, and the search for it is exactly the
open `chi(R^2) = 7` problem in this garb.

## 6. Grades

| item | grade |
|---|---|
| corrections 1-6 in §0 | **self-corrections**; items 2 and 3 retract claims from my previous block |
| (Sep)/(LC)/(Ext) definitions and `W6` as a separator | **proof**, hand-checked (`W6` arithmetic is small and exact: `Q(sqrt3)`) |
| Lemma C | **proof** (elementary, three lines); hypothesis satisfiability and the `m = 3` threshold checked by exhaustive case enumeration over colour pairs for `k = 5, 6` only |
| minimality of 3 witnesses | **proof from the same count**; holds for every `k`, since only the 2-element palette is used |
| §4 obstruction at `k = 5` | **proof** given that `chi(R^2) >= 6` is already established (prior work, not re-checked here) |
| NR-5 does not imply NR-6 | **proof** (a 5-colouring is a 6-colouring, not conversely) |
| (M) as a sufficient hypothesis | **proof** that (M) plus Lemma C plus Theorem A gives `chi(R^2) = 7` |
| (M) itself | **open**; nothing here shows it realisable, and nothing shows it impossible |
| any new forcing | **none** |

**Limitations.** I have not searched for an NR-6 triple, and no computation was run. Lemma C is a
relation-level lemma; it carries no geometric content beyond the free placements in (M1)-(M2). The
"no local gadget" remark in §5 is an observation about the known gadget inventory, not a theorem.

## 7. If a future block is authorised

The single useful target is (M4) at `k = 6`, not at `k = 5`. Anything that (i) establishes one NR-6
triple lets a second question be posed — whether a *second* NR-6 triple through the same pair exists —
but by Lemma C nobody should expect one triple to suffice, and by §4 a 5-level result is worthless
here. I would not spend a block on NR-5 at all.
