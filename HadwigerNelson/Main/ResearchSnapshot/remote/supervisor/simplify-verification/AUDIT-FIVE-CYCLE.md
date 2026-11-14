# Audit: `supervisor/simplify-angular/FIVE-CYCLE-CORE.md` against the paper and its sources

Verdict in one line: **(N) is fine — it is a pointwise fact about the *closed* supports, not an a.e.
rule lifted by hand — but the advertised elimination of Lemma 6.7 is not valid: steps 3 and 4 apply
the validity fact (V) at positions 1, 2, 4, 5, where the paper proves nothing of the kind.** The
finite lemma is still *true* with (V) at all six positions (two independent exhaustive checks); what
fails is the claim that (D)(N)(R) plus the paper's licensed uses of (V) give it. See §0a for two
corrections to the first version of this audit.

Grades: **[E]** exact exhaustive computation, reproducible (`checks/five_cycle_licence.py`);
**[PS]** paper text, read with `pdftotext -layout` from `attachments/here-are-three-files-ni5n/paper.pdf`
and checked on the p. 40–42 renders; **[SR]** source read, not compiled; **[C]** this block's reasoning.

## 0b. RETRACTION (block 5): the reflection sentence of §4a/§4b was ill-typed

> **Retracted as written.** §4a and §4b said "the reflection `i ↦ 1 − i`" interchanges the two
> families and treated it as a symmetry of the whole configuration, and `lean/FiveCycleResidues.lean`
> proved `refl '' D i = D (4 - i)` with `refl k = 1 − k`. Those two statements are about **different
> maps on different sets**, and the file's header drew a *state*-level conclusion from a *label*-level
> identity. The nine finite statements are all true; using one map for both levels is not.

The corrected statement, which is now what §4a/§4b and the Lean file say. The five-cycle data live on
two copies of `Z/5Z` that must not be identified:

| level | objects | map |
|---|---|---|
| vertex labels `k` (colour names) | `D i = {i, i+2} ⊂ Z/5Z` (p. 40, l. 2114–2117) | `g(k) = 3 − k` |
| state indices `i` (of `S_i`, `S(a)`) | `P j = {j−1, j+2}` (p. 42, l. 2188), `{0,1}` (l. 2184), `{2,4}` | `h(i) = 1 − i` |

and the two are tied by the **commuting identity**

$$g\,(D_i) = D_{h(i)} \qquad 	ext{for all } i \in \mathbb{Z}/5\mathbb{Z}$$

which is machine-decidable and is `g_induces_h` in the Lean file. Check by hand:
$g(D_i) = \{3-i,\,3-i-2\} = \{3-i,\,1-i\}$ and $D_{1-i} = \{1-i,\,3-i\}$ — the same set. ∎

**[block 6] Second correction, inside the block-5 file.** The block-5 Lean file also asserted
`∀ j, (P j).image h = P (h j)`, which is **false**: at `j = 0`, `h '' P 0 = h '' {4,2} = {2,4}`
while `P (h 0) = P 1 = {0,3}`. The correct target is `P (-j)` — `h_image_P` now states that, and it is
the only generality the argument needs, since the argument uses `j = 1` alone
(`h '' P 1 = P (-1) = P 4`). Two companion identities were checked in the same pass and are correct:
`h '' Nb i = Nb (h i)` and `g '' D i = D (h i)`. So the block-5 pairing `(g,h) = (3-k, 1-i)` stands;
what was wrong was one generalised *conclusion* drawn about `P`, not the pairing.

What the *old* map does instead: `k ↦ 1−k` sends `D i` to `{1−i, 4−i} = D (4−i)`, i.e. it induces
the state map `i ↦ 4−i` (`one_minus_k_induces_four_minus_i`), and that state map does **not** swap
`P 1 = {0,3}` with `P 4 = {1,3}`: `h'(P 1) = {4,1} ≠ P 4`. So the old pairing could not have
supported step 5 at all.

## 0a. Corrections to the first version of this audit (block 3)

Two statements in the first version were wrong. Both are corrected below and in place; the
conclusions they supported are restated.

**(C1) "a minimal countermodel violates exactly two of the four positions" — false.** All **eight**
solutions of the licensed system are invalid at **all four** of positions 1, 2, 4, 5:

```
invalid positions, for each of the eight:  [1,2,4,5] [1,2,4,5] [1,2,4,5] [1,2,4,5]
                                           [1,2,4,5] [1,2,4,5] [1,2,4,5] [1,2,4,5]
```

**(C2) the reading of the "drop one" runs had its implication backwards.** Those runs show:
validity at all positions **except** one of 1, 2, 4, 5 still gives 0 solutions — i.e. **relaxing a
single position is not enough to build a model**. That is a statement about the *insufficiency of one
relaxation*, not about each position being "individually load-bearing". Correct reading: at least two
relaxations are necessary, and in fact every solution of the licensed system relaxes all four at once.
The one claim that does survive is the direct observation on the eight: all eight have
`S(1) = S(5) = {2,4}`, so **adding (NC) at position 1 alone, or at 5 alone, removes all eight** —
verified by re-running the search with those sets, not inferred from the drop-one runs.

**(C3) the proof of (N) used the wrong choice of approximants.** Support membership alone does not
give `w(a_n) = i`. The approximants must come from the **state set** `E_i` intersected with the conull
set, not from `S_i`. Fixed in §1 below.

## 0. Exact source locations (paper, `pdftotext -layout` line numbers of this PDF)

| fact | location | text |
|---|---|---|
| a.e. palette is a diagonal, and the transition rule | p. 40, l. 2114–2118 | "almost every palette is exactly one of its diagonals `D_i = {i,i+2}` … `w_x(Re) = w_x(e) ± 1 (mod 5)` almost everywhere. **(6.6)**" |
| `S_i` = closed essential support, `S(a) = {i : a ∈ S_i}` | p. 40, l. 2119–2123 | "Let `S_i` be the closed essential support of state `i`, and let `S(a) = {i : a ∈ S_i}`" |
| nonemptiness of every list | p. 40, l. 2124–2126 | "Every list is nonempty, since the finitely many supports cover the circle" |
| strict separation, hence **(D)** at every `a` | p. 41, l. 2128–2134 | "It follows that, for every direction `a`, `S(a) ∩ S(Ra) = ∅`." |
| **(N)**, at every `a`, both ways | p. 41, l. 2135–2137 | "Also, each `i ∈ S(a)` has an index adjacent to it in each of `S(Ra)` and `S(R⁻¹a)`. Approach `a` by generic directions of state `i`, use (6.6), and pass to a constant adjacent index along a subsequence and then to its closed support." |
| **Lemma 6.7** (statement) | p. 41, l. 2139–2141 | "If `i, i+1 ∈ S(a)` at any direction `a`, then the transitions `i → i+1` and `i+1 → i` under `R` are absent almost everywhere on the entire angular circle at `x`." |
| Lemma 6.7 (proof, global step ban) | pp. 41–42, l. 2145–2156 | ends "The statements used hold on a common conull set, also after pulling back by `R`, proving the global step ban." |
| **(V) is proved only at the two endpoint directions** | p. 42, l. 2163–2181 | "For either endpoint `s = a_n^±` … the diagonals in `S(s)` have no common label. … This contradicts `y_n ∈ H_k`, which holds for every label because all five cycle edges are present at `y_n`. The no-common-label property passes to `a` and `−a`." |
| the only general statement about lists | p. 42, l. 2180–2183 | "A nonempty index list whose diagonals have empty intersection contains adjacent indices." |
| **(R)**, and the `j`-split | p. 42, l. 2184–2193 | "Both `S(0)` and `S(3)` contain adjacent index pairs. Rotate the label indices so that `0,1 ∈ S(0)`." |
| the use of 6.7 and of (6.6) | p. 42, l. 2194–2199 | "…so Lemma 6.7 bans both possible steps from state 1 … In either case (6.6) makes the shared state null, contradicting its membership in `S(0)`." |
| the paper's own care about null sets | p. 42, l. 2199–2201 | "Only the step bans at the two fixed directions `a, −a` have been used, so no union of exceptional null sets over arbitrary directions is involved." |

`grep -c "Lemma 6.7"` on the paper text = **2** (l. 2139 statement, l. 2196 use), so
FIVE-CYCLE-CORE's bibliographic claim is exact **[PS]**.

## 1. (N) is sound, pointwise, both ways, with no simultaneity problem  **[C]**

Notation: `E_i ⊆ S` is the **state set** of `i` at `x` (the directions whose palette is exactly the
diagonal `D_i`; this is the set of *positive measure* whose closed essential support is `S_i`), and
`S_i = cl-ess supp(E_i)` is the closed essential support, so `E_i ⊆ S_i` and every neighbourhood of a
point of `S_i` meets `E_i` in positive measure.

The worry — that (N) silently lifts the a.e. rule (6.6) to every element of the closed supports at a
fixed direction — does not materialise. Here is the proof the paper compresses into one sentence.

Let `G` be the conull set of directions on which (6.6) holds; put `G' = G ∩ R G` (conull, since `R` is
a rotation). Fix `a` and `i ∈ S(a)`. For each `n`, the set `E_i ∩ G' ∩ B(a, 1/n)` has **positive
measure**, because `a ∈ S_i`. Choose `a_n` in it. Then

* `w_x(a_n) = i` by construction (`a_n ∈ E_i`) — this is the step that support membership alone does
  not give, and it is why the approximants must come from `E_i`;
* `a_n ∈ G` gives `w_x(R a_n) = i ± 1`, so `R a_n ∈ E_{i+1}` or `E_{i-1}`;
* `a_n ∈ R G` gives, applying (6.6) at `R⁻¹ a_n`, `w_x(R⁻¹ a_n) = i ∓ 1`.

Pass to a subsequence on which the sign is constant, say `w_x(R a_n) = i + 1`. Then `R a_n ∈ E_{i+1} ⊆
S_{i+1}`, and `R a_n → R a`; `S_{i+1}` is **closed**, so `R a ∈ S_{i+1}`. Symmetrically `R⁻¹ a ∈
S_{i-1}` or `S_{i+1}`. ∎

Why this is not a hidden lifting:

1. (6.6) is used **only at the approximants** `a_n`, never at `a`; the passage to `a` is closedness of
   the essential supports.
2. The exceptional set is **one fixed null set** `(G')^c`, chosen once for the whole argument.
   Nothing is asked at six positions simultaneously: each `S(r)` gets its own proof at the point
   `R^r a` with its own approximating sequence. "Simultaneous exceptional sets" is a non-issue here,
   and the paper's remark that "no union of exceptional null sets over arbitrary directions is
   involved" (l. 2199) concerns Lemma 6.7, not (N).
3. What (N) does *not* give: nothing about the state at `a` itself, only membership of a neighbour in
   the neighbouring position's closed support. That is exactly what steps 2 and 5 use.

Same status for **(D)** (l. 2128–2134): `S(a) ∩ S(Ra) = ∅` is pointwise, from strict separation of
`S_i` from `R^{-1}S_i` (an isometric copy of the separation of `S_i` from `R S_i`).

## 2. (V) is the load-bearing hypothesis, and the paper licenses it only at positions 0 and 3  **[PS]**

FIVE-CYCLE-CORE's five steps:

| step | uses | licensed by the paper? |
|---|---|---|
| 1 | (D), (R) | **yes** (l. 2134, 2184) |
| 2 | (N) at `r = 0` | **yes** (l. 2135) |
| 3 | **validity of `S(1)`** and of `S(5)` to get `3 ∈ S(1) ∩ S(5)` | **no** |
| 4 | **validity of `S(2)` and `S(4)`** to get `S(2) = S(4) = {0,1}` | **no** |
| 5 | (N) at `r = 5` | **yes** |

The paper's (V)-type conclusion — "the diagonals in `S(s)` have no common label", which implies
validity and even excludes singletons — is proved at `s = a_n^±` and passed to `a` and `−a`
(l. 2163–2178), i.e. positions `r = 0` and `r = 3` only. That proof spends two things that are
available at no other position:

* the **endpoint pair** structure `(a_n^+, a_n^-)`: nonparallel directions whose sum is `h_n`, which is
  what makes "almost every direction in a neighbourhood of `s` carries label `k`" turn, through
  (5.2) and the local diffeomorphism of the sum map, into "`A_k` has zero area near `y_n`";
* the **five-cycle edges at `y_n`**, which give `y_n ∈ H_k` for *every* label `k`.

At a general position `r` there is no partner direction and no centre whose edges are known, so the
mechanism does not transfer. Validity at a general direction is **not** stated anywhere in §6.3, and
I did not find a proof of it: the paper's only general list statement is l. 2180–2183 (valid lists
contain adjacent indices), which is a consequence of validity, not a route to it. So this is a silent
strengthening of the hypotheses — of exactly the kind the brief asked to look for, just at (V)
rather than at (N).

## 3. The finite lemma is true as stated; the licensed version is not  **[E]**

`checks/five_cycle_licence.py` (my own implementation) and
`supervisor/simplify-angular/checks/five_cycle_full.py` (theirs, re-run here, rc 0) agree:

* validity of all six lists + (D) + (N) + (R): **0 solutions** — the combinatorial core of
  FIVE-CYCLE-CORE is correct, and its "21 valid lists" count is confirmed.
* validity of `S(0)` and `S(3)` only (what the paper proves) + (D) + (N) + (R): **8 solutions**, e.g.

  ```
  S(0) = {0,1}   S(1) = {2,4}   S(2) = {0,3}   S(3) = {1,2}   S(4) = {0,3}   S(5) = {2,4}
  ```

  Check by hand: (D) adjacent lists disjoint ✓; (N) at `0`: `nb(0) = {4,1}` meets `S(1)` at 4 ✓,
  `nb(1) = {0,2}` meets `S(1)` at 2 ✓, and symmetrically upward; (R) `0,1 ∈ S(0)` ✓; `S(0)`, `S(3)`
  valid ✓ (`{0,1}`: `D_0 ∩ D_1 = ∅`; `{1,2}`: `D_1 ∩ D_2 = ∅`); `S(1)` and `S(5)` are invalid
  (`D_2 ∩ D_4 = {4}`), `S(2)`, `S(4)` invalid (`D_0 ∩ D_3 = {0}`).
* relaxing a **single** one of the positions 1, 2, 4, 5 (validity required at the other five) still
  gives 0 solutions: one relaxation is *not sufficient* to obtain a model. Every one of the eight
  relaxes all four at once — there is no solution with fewer.
* all eight have `S(1) = S(5) = {2,4}`, so requiring validity at position 1 alone (or at 5 alone) on
  top of 0 and 3 leaves 0 solutions. (Direct re-run with those validity sets, not an inference from
  the single-relaxation runs.)

What this countermodel is and is not: it satisfies the four hypotheses the paper licenses at that
stage and *violates the paper's conclusion* (state 1 has both steps banned, so (6.6) + Lemma 6.7 make
it null, contradicting `1 ∈ S(0)`). So it is a sharp refutation of "these hypotheses suffice", not a
counterexample to §6.3.4. Read positively: it shows that the last step of the printed argument is
**not** redundant — Lemma 6.7 (or something with its force) is exactly what excludes these eight
configurations.

## 4. Corrected theorem and proof  **[E] for the finite statement, [PS] for the hypotheses**

If the replacement is to stand, it must quantify over the fact it uses:

> **Theorem (finite core, corrected).** Let `S(0),…,S(5) ⊂ Z/5Z` be nonempty. Suppose
> (i) `0,1 ∈ S(0)`; (ii) `S(r) ∩ S(r+1) = ∅` for all `r mod 6`; (iii) every `i ∈ S(r)` has `i±1` in
> each of `S(r+1)`, `S(r-1)`; (iv) **every** `S(r)` is valid (`⋂_{i∈S(r)} D_i = ∅`).
> Then contradiction. — *Proof:* exhaustive over the 21 valid lists, two independent programs.

That is exactly FIVE-CYCLE-CORE's lemma. It is a real compression of the `j`-split, and it needs

> **(NC-r)** the diagonals in `S(R^r u)` have no common label, at the positions `r` it is applied to,

which the paper proves only at `r = 0, 3` (l. 2163–2178). Two honest routes, in order of cost:

1. **Prove (NC-1) (or (NC-5)) — one new direction fact, not four.** By §3 all eight configurations
   have `S(1) = {2,4}`, so a single extra validity statement at position 1 (or 5) makes the finite core
   apply with no case analysis at all. Whether (NC-1) is true is open: the printed mechanism needs a
   partner direction whose sum with `u` is near a centre at which all five edges are present, and the
   accumulation construction supplies no partner at `r = 1`.
2. **Keep Lemma 6.7.** Then the reachable target is the six-step argument of §4b: fewer cases than
   the printed five-residue split, but 6.7 and (6.6) retained. This is the version to hand to a
   referee, because it asks for nothing the paper does not already prove.

### 4a. Classification of the eight configurations  **[E]**

Writing them out shows a rigid shape. In every one:

| position | value | count |
|---|---|---|
| `S(1) = S(5)` | `{2,4}` (forced: (N) at 0 gives `4` for label `0` and `2` for label `1`, both ways) | 1 |
| `S(2) = S(4)` | `{0,3}` or `{1,3}` (always equal to each other) | 2 |
| `S(0)` | `{0,1}` or `{0,1,3}` | 2 |
| `S(3)` | `{1,2}`, `{1,2,4}`, `{0,4}`, `{0,2,4}` | 2 per family |

`8 = 2 · 2 · 2`. The four with `{1,2} ⊆ S(3)` ("`j = 1` family") pair off against the four with
`{0,4} ⊆ S(3)` ("`j = 4` family") under the **state** reflection `h(i) = 1 − i (mod 5)`, which fixes
`{0,1}` setwise (`h_fixes_anchor`), fixes `{2,4}` setwise (`h_fixes_pair24`), and exchanges
`{0,3} ↔ {1,3}` (`h_swaps_allowed_pairs`) — checked on all eight **[E]** and machine-decidable
**[source, unbuilt]**. For this to be a legitimate relabelling and not an arbitrary permutation of
state indices, it must be induced by a relabelling of the *labels*, and it is: `g(k) = 3 − k`
satisfies `g(D_i) = D_{h(i)}` (§0b). The compatible pair is `(g, h) = (3 − k, 1 − i)`; the pair
`(1 − k, 4 − i)` is true but useless here. State reflection + label reflection together preserve
(V), (D), (N) and the two normalisations — the transport is written out in the Lean file's header,
one bullet per condition.

### 4b. Shortest valid finite conclusion that *keeps* Lemma 6.7  **[C], mapped to source**

Take as finite inputs exactly what the paper licenses:

* **(V0)** `S(0)` has no common label — l. 2163–2178 (endpoint argument);
* **(V3)** `S(3)` has no common label — same passage;
* (D) l. 2134, (N) l. 2135–2137, (R) l. 2184;
* **the content of Lemma 6.7** (l. 2139–2156), in the two forms it is used in:
  (i) an adjacent pair `{i,i+1} ⊆ S(u)` at *any* direction `u` bans the step `i ↔ i+1` **a.e. on the
  whole angular circle** (its conclusion is global — that is exactly what makes the two endpoint
  applications at `a` and `−a` combine);
  (ii) hence *nullness*: if both steps out of state `i` are banned (a zero-valued state has only the
  two neighbours available by (6.6)), then `E_i` is null, contradicting `i ∈ S(w)` for any `w`
  (l. 2198, "(6.6) makes the shared state null").

**Proof (6 steps).**

1. By (R) relabel so that `{0,1} ⊆ S(0)`; by (V0) this pair is what `S(0)` supplies. 6.7 at `a` bans
   `0 ↔ 1`.
2. By (V3), `S(3)` contains an adjacent pair `{j, j+1}`.
3. **(D)+(N) step** (l. 2188–2192): `S(1) ⊆ I ∖ S(0) ⊆ {2,3,4}` and label `0` needs a neighbour in
   `S(1)` — `nb(0) = {4,1}` — so `4 ∈ S(1)`; label `1` needs one in `S(1)` — `nb(1) = {0,2}` — so
   `2 ∈ S(1)`. The same in the `r = 5` direction and at `r = 3`: `2,4 ∈ S(1) ∩ S(5)` and
   `{j−1, j+2} ⊆ S(2) ∩ S(4)`.
4. **One finite count, replacing "checking the five possible residues of `j`"**: the five pairs
   `{j−1, j+2}` are exactly the five distance-2 pairs `{0,2}, {1,3}, {2,4}, {3,0}, {4,1}`, and exactly
   **two** of them avoid `{2,4}`, namely `{0,3}` (`j = 1`) and `{1,3}` (`j = 4`). So for `j ∈ {0,2,3}`,
   `{j−1,j+2} ∩ {2,4} ≠ ∅`; a label lying in `S(2) ∩ S(1)` (or `S(4) ∩ S(5)`) contradicts (D).
5. So `j ∈ {1,4}`. By the state reflection `h(i) = 1−i` of §4a — legitimate because the label map
   `g(k) = 3−k` satisfies `g(D_i) = D_{h(i)}` and every list condition transports (§0b) — it is
   enough to treat `j = 1`.
6. `j = 1`: `{1,2} ⊆ S(3)` bans `1 ↔ 2` by 6.7 at `−a`; with step 1 both steps out of state `1` are
   banned, so `E_1` is null (6.7(ii)) — contradicting `1 ∈ S(0)`. ∎

Length: six lines, of which the only case analysis is the single count in step 4 and the symmetry in
step 5. **Against the printed text this is a compression of the residue split from five residues to
"two of five distance-2 pairs" plus an explicit reflection — an exposition gain, not a hypothesis
gain.** It is *not* a simplification of Lemma 6.7's role: the lemma is retained and used exactly as
the paper uses it, at the two endpoint directions.

Assessed against FIVE-CYCLE-CORE: its stated advantage ("0 uses of 6.7, 0 uses of (6.6), 0 case
splits") is unattainable with the hypotheses the paper supplies, because steps 3–4 of *its* proof are
the steps that need the unlicensed (V) at positions 1, 2, 4, 5. The reachable target is the six-step
argument above: it still uses 6.7 and (6.6), and removes one case split.

### 4c. [block 5] The repair is cheaper than §4 recorded: only (NC-1) is needed

Validity at positions **0 and 1** alone — plus (D), (N), (R) — already gives 0 solutions
(`checks/five_cycle_licence.py`, validity sets `{0,1}` and `{0,5}` both 0). Then:
(D) gives `S(1) ⊆ I ∖ S(0) = {2,3,4}` since `S(0) = {0,1}`; (N) gives `{2,4} ⊆ S(1)`; validity of
`{2,4}` fails because `D_2 ∩ D_4 = {4}`, so `3 ∈ S(1)`; but `3 ∈ S(1)` needs a neighbour in
`S(0) = {0,1}` and `nb(3) = {2,4}`. Three lines instead of six, and position 3 is not used at all.

So the finite part of §6.3.4 needs exactly **(NC-1)** on top of the printed (V0) — not (V3), and not
four positions. That is consistent with (and explains) the angular worker's independently reported
"two positions suffice"; their computation establishes the finite fact, not the hypothesis.

Kept as the referee-ready version anyway: the six-step argument of §4b, because it needs no new
direction fact — it uses only (V0), (V3) and Lemma 6.7 as printed.

### 4d. [block 6] The symmetry-transport interface, stated at the paper's own quantifiers

Steps 4-5 of §4b reflect a configuration of six lists. The reflection must preserve the three list
conditions the paper has at that point. In `lean/FiveCycleResidues.lean` (unbuilt) this is now proved
for the general predicates rather than for the eight configurations:

| condition | paper form | Lean predicate | transport theorem |
|---|---|---|---|
| (V) no common label | `⋂_{i∈L} D_i = ∅`, p. 42, l. 2180-2183 | `NotCommon L := ∀ k, ∃ i ∈ L, k ∉ D i` | `notCommon_image` |
| (D) adjacent lists disjoint | `S(a) ∩ S(Ra) = ∅`, p. 41, l. 2134 | `Disjoint (S r) (S (r+1))` | `disjoint_image` |
| (N) neighbour existence, both ways | p. 41, l. 2135-2137 | `HasNbr L M := ∀ i ∈ L, (Nb i ∩ M).Nonempty` | `hasNbr_image` |

with positions fixed: `push S := fun r => (S r).image h`, and `valid_family_push`,
`disjoint_family_push`, `neighbour_family_push` state the three transports on configurations
`ZMod 6 → Finset (ZMod 5)`. Each list-level proof is three lines: (V) applies the hypothesis to the
relabelled label `g k` and moves the membership failure back with `g '' D (h i) = D i` and
`h (h i) = i`; (D) is injectivity of `h`; (N) is `h '' Nb i = Nb (h i)`, which is where the
order-reversal `h (i+1) = h i - 1` is absorbed.

What these theorems do **not** do, and must not be read as doing:

* they do not supply `(NC-1)`: (V) at position 1 remains a hypothesis, and the eight countermodels of
  §3 are untouched — the transport says a reflection preserves no-common-label, not that the
  configuration has it;
* they say nothing about accumulation of five-cycle centres; they are finite statements about lists;
* Lemma 6.7 is retained and still applied at `a` and `-a` as printed.

## 5. What else in FIVE-CYCLE-CORE checks out

* "Lemma 6.7 occurs exactly twice" — confirmed by grep **[PS]**.
* "21 valid lists", "every valid list inside `{2,3,4}` contains 3", "(V) alone excludes `{2,4}`" —
  confirmed independently **[E]**.
* the caveat that (V) itself is not re-derived — correct and well stated.
* the remark that `compressed-proof-verify.py`'s Claim-A has a single realisation: **not checked
  here** (out of this block's scope).

## 6. Reproduction

```
python3 supervisor/simplify-verification/checks/five_cycle_licence.py     # [A]-[F] above, rc 0
python3 supervisor/simplify-angular/checks/five_cycle_full.py            # their check, rc 0
```
