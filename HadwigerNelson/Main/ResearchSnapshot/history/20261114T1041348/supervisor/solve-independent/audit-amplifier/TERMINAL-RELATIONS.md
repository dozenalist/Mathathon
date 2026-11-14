# What the Heule-553 separation certificate does not say, and one arity-3 relation worth testing

Analysis block: no computation, no solver, no Lean. Read artifacts (frozen here with hashes):
`supervisor/solve-graphs/certs/adaptive_k5.json` -> `audit-amplifier/adaptive_k5.frozen.json` and
`supervisor/solve-graphs/certs/census_heule553.json` -> `audit-amplifier/census_heule553.frozen.json`.
Nothing below is evidence of new forcing; **no forcing pair is claimed and none is known.**

## 0. What the certificate actually is

From the artifact: `n = 553`, `m = 2722`, `n_witnesses = 34`, `verified_witnesses = 18`, `steps = 16`,
every step `SAT`, `baseline = 491`, `sum_choose2 = 491`, **`final_survivors = 0`**. Each witness is a
length-553 list over labels `{0,1,2,3,4}`; witness 1's class sizes are `[129,116,115,103,90]`.

The mechanism is an **adaptive chase**: take a proper 5-colouring, find a largest monochromatic class,
pick a pair in it, add the inequality for that pair, re-solve, and repeat. After 16 steps the survivor
set is empty, i.e.

> **(Sep)** for every distinct pair `(p,q)` of vertices there is a witness `w` with `w(p) != w(q)`.

Hence no pair is forced equal in every proper 5-colouring — and since a proper 5-colouring is also a
proper `k`-colouring for every `k >= 5`, **no pair is forced equal at any `k >= 5`**. (At `k = 4` the
statement is vacuous: the graph has no proper 4-colouring, so "equal in every 4-colouring" is true of
every pair. The forcing question only means something where colourings exist.)

Because the chase is adaptive, the 34 witnesses are a **targeted subset** of `Omega(G,5)`, not orbit
representatives and certainly not an enumeration. That is the single most important thing to keep
straight below.

## 1. What the certificate does NOT imply — simultaneous patterns

The four logical forms, which must not be conflated:

| form | statement | status |
|---|---|---|
| **(A)** `forall pairs exists colouring` | for each pair there is a colouring separating it | **verified** — this is exactly (Sep) |
| **(B)** `exists colouring forall pairs` | one colouring separates every pair | **false**, trivially: it is an injective 5-colouring of 553 vertices |
| **(C)** `forall relation-sets exists colouring` | every requested set of relations is individually realisable | **open**, and (A) says nothing about it |
| **(D)** `exists colouring realising all requested relations` | a *simultaneous* pattern | **open**; this is what one SAT query decides for one instance |

(A) does not imply (C) or (D): the quantifiers `forall pairs exists colouring` and `exists colouring
forall relations` do not commute. Concretely, (A) is consistent with *every* triple of vertices being
non-rainbow in all colourings while *each of its three pairs* is separated in some colouring. That is
precisely the gap a higher-arity test probes.

Four further limits, stated so they are not over-read:

1. **No completeness.** Any pattern *absent* from the 34 may still be realisable in a colouring outside
   the chase. Absence in the witnesses is a filter, never a proof of impossibility.
2. **Pairs only.** Nothing about colour *class sizes*, about which sets are simultaneously
   monochromatic, or about patterns on `>= 3` vertices.
3. **Separation, not merging.** (Sep) says pairs can be *split*; it says nothing about whether a given
   set can be *merged*, nor that merging is impossible beyond the pair level.
4. **Not a limit statement.** (Sep) is about single colourings, not about patterns attained in the limit
   of a sequence of colourings; no "terminal" object is produced by it.

## 2. A concrete induced unit-distance example of (Sep) without precolouring extension

Take `W_6`: the centre plus the regular hexagon, `V = 7`, `E = 12` — rim edges plus 6 spokes. It is an
**induced** unit-distance graph: rim points at `60k` degrees on the unit circle, so rim-adjacent chords
are `1`, rim skip-one chords are `sqrt3`, opposite is `2`, spokes are `1` — exactly 12 unit pairs, no
others. Coordinates in `Q(sqrt3)`.

**(Sep) holds at `k = 4`** — every one of the 21 pairs is separated by some proper 4-colouring: rim
edges and spokes are edges (separated in *every* colouring); the 9 non-adjacent rim pairs split into 6
skip-one and 3 opposite, and by symmetry two cases suffice:
`(1,3,2,1,2,3)` with hub `4` separates `{0,2}`; `(1,2,3,2,1,3)` with hub `4` separates `{0,3}`
(rim cycle `0-1-2-3-4-5-0`).

**Arbitrary precolouring extension fails at `k = 4`.** Prescribe `c(0)=1, c(1)=2, c(2)=3, c(3)=4`.
This is *locally consistent* — the only rim edges among these are `0-1`, `1-2`, `2-3`, and the colours
are distinct. It extends on the rim itself (`c(4)=2, c(5)=3` works). But the hub is adjacent to all six
rim vertices, hence needs a colour outside `{1,2,3,4}`, and only 4 colours exist. So the prescription
has **no** extension, by a star constraint of arity 7 — nothing pairwise.

So (Sep) at `k=4` coexists with a non-extendable locally consistent prescription: (A) does not give (D).
At `k = 3` the same graph fails (Sep): the rim must be properly 2-coloured and the hub takes the third
colour, so `c(0) = c(2)` always. (`W_6` at `k=3` is thus another (H2)-type forced-equal gadget, with
`p = 0`, `q = 2` at distance `sqrt3`, hand-verified here; it is not minimal — the diamond is smaller —
and I make no claim that it is new.)

## 3. The one relation worth testing on Heule-553

**R3 (anti-rainbow triple, `k = 5`).** An independent triple `T = {u,v,w}` such that **no** proper
5-colouring of `G_553` gives `T` three distinct colours; equivalently every proper 5-colouring merges two
of `T`.

Why this one, and not something cheaper:

* **Not an existing edge.** `T` is independent by construction (it is contained in one colour class of
  a witness), so R3 is not the trivial "adjacent implies different".
* **Not an obvious common-neighbour palette constraint.** The census gives `max common neighbours = 2`
  (`P2_max_cn_le_2: true`; histogram `0: 132261, 1: 9744, 2: 7901`), so the only common-neighbour
  palette device available in this graph is the diamond-type one, and every such device forces a
  **pair** equal — which the certificate refutes for **every** pair. More sharply: if `T` were forced
  non-rainbow *because* some pair of `T` were forced equal, that is excluded; if some pair of `T` were
  forced *different*, that would push towards rainbow, not away. So an UNSAT for R3 **cannot** be
  explained at arity 2 at all. That is exactly what makes it a genuine escalation, and it is a direct
  consequence of the property (A) that was verified.
* It is the minimal arity beyond the certificate, and it is one SAT query.

It would be a *terminal relation* in the following precise sense: a pattern (the partition of `T` by
colour) that every colouring respects. Whether the project's terminal-factor machinery uses the word
the same way is not something I assert.

## 4. The deterministic selection rule (small, no search over triples)

**Rule S.**
1. Read the 34 witnesses in artifact order; let `w_1` be the first.
2. `C` := a colour class of `w_1` of maximum size; ties broken by smallest label. (`C` is independent
   because `w_1` is proper.)
3. Sort `C` by vertex index: `c_1 < c_2 < ...`. Form candidate triples in lexicographic index order,
   taking only the first **30**: `(c_1,c_2,c_3)`, `(c_1,c_2,c_4)`, `(c_1,c_3,c_4)`, ... .
4. For each candidate `T`, compute `r(T) = #{ j : w_j is rainbow on T }` — purely a lookup.
5. Take the **first** `T` with `r(T) = 0`. If all 30 have `r(T) >= 1`, stop: the filter found no live
   candidate in the largest class of `w_1`, and **no SAT run happens**.

This is deterministic, needs no search, and uses the witnesses only as filters. Note what step 5 does
*not* license: `r(T) = 0` is not evidence that `T` is forced non-rainbow — only the SAT run decides
that. (`r(T) >= 1` *is* conclusive, in the opposite direction: that witness realises the rainbow.)

## 5. Exact SAT constraints for the single bounded test

Variables `x[v][c]`, `v in V(G_553)` (`553`), `c in {0,1,2,3,4}` — `2765` variables.

1. **At least one colour**, for each `v`: `(x[v][0] or x[v][1] or x[v][2] or x[v][3] or x[v][4])` —
   553 clauses, width 5.
2. **At most one colour**, for each `v` and each `c < c'`: `(-x[v][c] or -x[v][c'])` — 5530 binary.
3. **Every edge differs**, for each edge `{u,v}` and each `c`: `(-x[u][c] or -x[v][c])` — 13610 binary.
4. **Rainbow on `T = {u,v,w}`**, for each `c`: `(-x[u][c] or -x[v][c])`, `(-x[v][c] or -x[w][c])`,
   `(-x[u][c] or -x[w][c])` — 15 binary.

Total `19708` clauses. Clause types 1-3 are exactly the standard 5-colouring encoding; type 4 is the
only addition, and it adds no auxiliary variables, so the encoding is a drop-in for the existing
pipeline.

**Pre-registered decision table (one triple, one run, no follow-up sweep):**

| outcome | conclusion | what it is not |
|---|---|---|
| UNSAT | `T` is a forced anti-rainbow triple at `k=5`: a genuine arity-3 terminal relation, not explainable by any pair (see §3) | not evidence about other triples, and not a forcing *pair* |
| SAT | `T` is rainbow-realisable; the model is a new verified witness and `r(T)=0` was a filter artefact | not evidence that *no* anti-rainbow triple exists |
| timeout | inconclusive | — |

Either way the run is bounded: one triple, ~20k clauses, no sweep; if SAT, no second triple is tried in
the same block.

## 6. Grades and limitations

| item | grade |
|---|---|
| certificate structure and (Sep) | **read from the artifact** (`adaptive_k5.json`); the 34 witnesses are verified per the supervisor, not re-verified by me |
| "no forced equal pair at `k >= 5`" | **valid consequence** of (Sep), with the `k = 4` vacuity caveat recorded |
| the `(A)/(B)/(C)/(D)` separation | **proof** (quantifier reasoning); `W_6` example **proof**, hand-checked |
| `max common neighbours = 2` | read from `census_heule553.json`; not re-derived |
| R3 not reducible to arity 2 | **proof** given (Sep) |
| Rule S | specification only; **not executed** |
| the SAT encoding | specified; **not run** — this block is analysis only |
| any new forcing | **none claimed**; no anti-rainbow triple is asserted to exist |

Limitations: the census numbers (`max_cn = 2`, triangle count `1093`) are inherited from the frozen
artifact, not recomputed here. The claim that R3 is not a "common-neighbour palette constraint" rests on
that census plus (Sep); if the census were wrong the argument would need revisiting. And the whole probe
is one triple: a negative answer at `T` leaves 553-choose-3 minus 30 candidates untouched.

## 7. Reproduce (next block, if authorised)

    # 1. filter: read the 34 witnesses, apply Rule S, report r(T)
    # 2. if r(T) = 0: build the 19708-clause CNF above and run the single cadical call
    # no other triple, no second run

Nothing was run here.
