# d13 — the palette-system reduction at six colours, and the k=6 two-centre palette bound

Member m2, swarm smwfo9zkl. Files: this report, `verify.py` (exact checker), `raw.json` (output).

```bash
cd .ultramath/smwfo9zkl/m2 && python3 verify.py       # ~5 min, writes the JSON printed to stdout
```

## 0. Input facts (cited, not re-proved)

Paper §5 setting: `c` a weak measurable `k`-colouring of `C = R^2`; for a centre `x` the maximal
palette `P_x(e) ⊆ {1..k}` in direction `e ∈ S := S^1` is built from the weak-* closed family `W_x`
of circle traces (Definition 5.1), modulo angular null sets; `σ` = normalised angular measure;
`R` = rotation by `π/3`.

* **(5.2)** (Lemma 5.2.1) for a.e. independent `(e,v)`: `c(x+e+v) ∉ P_x(e) ∪ P_x(v)`.
* **(5.3)** (Lemma 5.2.3) for each smooth representation `z+f = x+s(f)+t(f)` with `s(f),t(f) ∈ S`
  non-parallel and `s` a local diffeomorphism: `P_z(f) ∩ P_x(s(f)) = ∅` a.e. `f`.
* **(5.7)** (Cor. 5.4) `P_x(f) ∩ P_x(Rf) = ∅` a.e. `f`.
* **Non-emptiness**: `P_x(e) ≠ ∅` for a.e. `e`, every `x` (Definition 5.1).
* **Palette bound**: `1 ≤ |P_x(e)| ≤ k-3` a.e. `e`, every `x` (`results/K6-BARRIER.md` §1; at `k=5`
  the paper's Prop. 5.6).
* **T2** (`results/T2-null-sets.md`): every null `Z ⊆ C` has `χ(C\Z) ≥ 6`.
* **de Bruijn–Erdős**: a graph is `k`-colourable iff all its finite subgraphs are (used by T1).

*Derived form of (5.3) used below — the translation exclusion.* Put `z = x+a`, `|a| = 1`,
`s(f) = f`, `t(f) = a` in Lemma 5.2.3; by Remark 5.3 ("the second endpoint map `t` may be
constant"; `s = id` is a local diffeomorphism and `s,t` are non-parallel off `f = ±a`) this is
admissible, so for every centre `x` and every unit vector `a`

  **(TE)** `P_{x+a}(e) ∩ P_x(e) = ∅` for `σ`-a.e. `e`, the exceptional set depending on the pair.

## 1. Theorem A — the reduction Step 3 rests on, decided

A *palette system of level k on `X ⊆ C`* is a family `P_x : S → 2^{[k]}\setminus\{∅}` (`x ∈ X`)
satisfying **(TE)** for every unit pair of `X`; no size bound and no measurability in `x` is needed.

**Theorem A.** For any `X ⊆ C`, a palette system of level `k` on `X` exists iff the unit-distance
graph on `X` is `k`-colourable. In particular a palette system of level `k` on `C` exists iff
`χ(R^2) ≤ k`, and on the algebraic plane `E` iff `χ(R^2) ≤ k` (T1).

*Proof.* (⇒) Let `F ⊆ X` be finite. There are finitely many unit pairs in `F`; let `N` be the
union of their `(TE)`-exceptional null sets, a null set, and fix `e ∉ N`. Every `P_x(e)`, `x ∈ F`,
is non-empty, and for a unit pair `x,y ∈ F` the two are disjoint, so
`f_e(x) := min P_x(e)` is well defined and `f_e(x) ≠ f_e(y)`. Thus every finite subgraph of `X` is
`k`-colourable, and de Bruijn–Erdős finishes. (⇐) A proper `k`-colouring `c` gives the system
`P_x(e) = {c(x)}`, of size `1 ≤ k-3` for `k ≥ 4`, and `(TE)` holds since `c(x) ≠ c(x+a)`. ∎

So the palette formalism is *exactly* `k`-colourability, and Step 3 has no middle ground: an UNSAT
instance proves `χ ≥ 7`, while a SAT instance *is* a 6-colouring, written down in closed form by
`f_e` on each finite subgraph. Two consequences that decide parts of the sprint's framing:

* **(A1) The content is not in the a.e./measure structure.** The proof uses one direction `e` and
  the pointwise exclusion `(TE)`. Neither (5.2), nor (5.7), nor binary/ternary centres, nor any
  measure-theoretic palette statement is used. So (i) a system keeping `(TE)` at all unit pairs can
  never be satisfiable at `k = 6` unless `χ(R^2) ≤ 6`, and (ii) a system that drops `(TE)` at even
  one unit pair is not a relaxation of the problem (see (W3)).
* **(A2) Why single-centre constraints are powerless.** Min-selection is the only passage from sets
  to labels, and it consumes exactly the two-centre exclusion. This is the structural reason behind
  the machine-checked powerless class of the sprint statement.

## 2. Theorem B — the k=6 two-centre palette bound (new)

**Theorem B.** Let `c` be a weak measurable `k`-colouring (`k ≥ 4`), `x,y ∈ C` with `|x-y| = 1`.
Then, for `σ`-a.e. `e ∈ S`,

  **`|P_x(e)|` and `|P_y(e)|` cannot both be
  `k-3`**; equivalently `|P_x(e)| + |P_y(e)| ≤ 2k-7` for `k ≥ 6`, and at `k = 6` this reads

  **`|P_x(e)| + |P_y(e)| ≤ 5 = k-1`.**

Combined with disjointness (`|P_x(e)| + |P_y(e)| ≤ k`) the sharp content is
`|P_x(e)| + |P_y(e)| ≤ min(k, 2k-7)`, a strict improvement over disjointness only at `k = 6`.

*Proof.* Let `a := y-x`, `z := x + Ra` (`R` = rotation by `π/3`). Then `|z-x| = |a| = 1` and
`|z-y| = |Ra - a| = 1`, so `(x,y)`, `(x,z)`, `(y,z)` are all unit pairs. Let `N` be the union of the
three `(TE)`-exceptional null sets and of the null set where `P_z = ∅`; fix `e ∉ N`. The three
palettes are pairwise disjoint and non-empty. If `|P_x(e)| = |P_y(e)| = k-3` then
`|P_x ∪ P_y| = 2k-6 ≥ k` for `k ≥ 6`, hence `P_x ∪ P_y = [k]` and
`P_z(e) ⊆ [k] \ (P_x ∪ P_y) = ∅`, contradicting non-emptiness. For `k ≤ 5` the claim is vacuous:
`2(k-3) ≤ k-1`. ∎

**Sharpness — this constraint exists only at `k = 6`.** Two maximal palettes (size `b = k-3`) can be
disjoint only if `2b ≤ k`, i.e. `k ≤ 6`, and they exhaust `[k]` only if `2b = k`, i.e. `k = 6`.
Exhaustive counts of unordered pairs of maximal palettes (`verify.py`, `e1`):

| k | bound b | disjoint maximal pairs | of these, filling all k labels |
|---|---|---|---|
| 4 | 1 | 6 | 0 |
| 5 | 2 | 15 | 0 |
| **6** | **3** | **10** | **10** |
| 7 | 4 | 0 | 0 |
| 8 | 5 | 0 | 0 |

At `k ≤ 5` the inequality is trivial (which is why no `k=5` argument ever sees it); at `k ≥ 7` its
premise is unsatisfiable; `k = 6` is the unique label count at which it bites. In words: *at six
labels two maximal palettes at unit distance would be a partition of the label set, leaving no colour
for the equilateral completion.*

**Corollaries at k=6** (in any weak measurable 6-colouring):

* **(B1)** `|P_x(e)| = 3` ⇒ every unit-neighbour `y` of `x` has `|P_y(e)| ≤ 2`. For a countable set
  of unit-neighbours simultaneously, for a.e. `e`.
* **(B2)** On the algebraic plane `E`: for `σ`-a.e. `e`, the ternary locus
  `Z_e = {x ∈ E : |P_x(e)| = 3}` contains no two points at distance exactly `1`.
* **(B3)** For contrast (and *not* new — it is the "mean 5/2" clause of the machine-checked powerless
  class): (5.7) plus the union form of (5.2) give `|P_x(e)| + |P_x(Re)| ≤ 5`, so at each centre at
  most half the directions are ternary. (B1)–(B2) are spatial, (B3) is angular; only (B1)–(B2) are
  two-centre.

**What B does not give.** Not `|P_x(e)| ≤ 2` a.e., so it does not unlock §7. The counting *admits*
the pattern `(3,2)` at a unit pair (exactly one label survives for the completion), and by check E3
single-centre data admits ternary palettes, so no single-centre or counting refinement improves `5`
to `4`. The remaining `k=6` gap is exactly: *exclude a 3-element palette at a.e. direction at one
centre* — the step the paper performs at `k=5` by turning a positive-measure 3-palette into a binary
centre and invoking Lemma 5.5.

## 3. What breaks when the a.e. quantifier in (5.3) is weakened

* **(W1) Keep only the translations `s = id`, drop all other representations.** Nothing is lost:
  Theorem A uses only those.
* **(W2) Impose (5.3) in a single direction, or on any null set of directions, instead of a.e. `e`.**
  Nothing is lost on a countable centre set (discard the null exceptional sets pair by pair); for an
  arbitrary centre set apply the finite-subgraph argument of Theorem A. So the paper's a.e. qualifier
  is not where the difficulty lives.
* **(W3) Impose (TE) only for a finite set of offsets `U`.** Then the system is exactly "the
  `U`-graph on `X` is `k`-colourable" (Theorem A applied to the subgraph). For `|U| = 1`, `k = 2`,
  there is a closed-form model: with `u = (1,0)` and `A = {x : x_1 mod 2 ∈ [0,1)}`, put
  `P_x = {1}` on `A` and `P_x = {2}` off `A`; then `P_x ∩ P_{x+u} = ∅` for every `x`. So dropping
  the "all unit `u`" quantifier destroys the content completely.
* **(W4) Impose (TE) for a.e. `x` instead of all `x`.** Theorem A then yields a proper `k`-colouring
  of `C\Z` for a null `Z`. At `k = 5` this is still contradictory, by **T2**. At `k = 6` the
  weakening is genuine: it reduces the problem to *is there a null `Z` with `χ(C\Z) ≤ 6`?*, the
  null-set-robust form of the six-colour problem, whose status is not known.

## 4. Machine checks (`verify.py`; exact; two independent decision procedures)

* **E1** the table of §2, exhaustive over all pairs of palettes for `k = 4..8`.
* **E2** Theorem A on a non-trivial unit-distance graph: the Moser spindle, `7` vertices, `11`
  edges, `χ = 4`, realised in **exact** coordinates in `Q(√3,√11)` (sympy radicals; all 11 edges
  verified at squared distance exactly 1, every other pair at squared distance ≠ 1).

  | CSP | backtracking | sympy DPLL on a CNF encoding |
  |---|---|---|
  | `k=2`, palettes of any size | UNSAT | — |
  | `k=3`, palettes of any size | **UNSAT** | **UNSAT** |
  | `k=4` | SAT, witness `{1}{2}{3}{1}{2}{3}{4}` | SAT |
  | `k=4`, `|P| ≤ 1` | SAT; 384 solutions, min-map proper in all 384 | — |
  | `k=6`, `|P| ≤ 3` | SAT | — |

  The `k=3` row is the point: **the set-valued palette relaxation is not a relaxation** — a
  4-chromatic unit-distance graph admits no system of non-empty label sets with pairwise disjointness
  on its 11 edges over 3 labels. That is Theorem A observed on a real graph, and it is why (A2)
  holds: only disjointness across centres converts sets into labels.
* **E3** vacuity check for Theorem B: the single-centre constraints at `k=6` — (5.7) at `60°` and the
  "union never exhausted" consequence of (5.2) — do admit a ternary palette, namely
  `(A_0,…,A_5) = ({1,2,3},{4},{1},{2},{1},{4})` on the six rotations of a direction (all six
  `60°`-pairs disjoint, all non-antipodal unions `≠ {1..6}`). So Theorem B is not obtainable from
  single-centre data and does not contradict the machine-checked powerless class: it is genuinely
  two-centre.

## 5. Scope

Proved: Theorem A (the palette-system reduction is exactly `k`-colourability; the hypotheses are
named, and the a.e. structure is not needed), Theorem B (the new necessary condition at unit pairs,
non-trivial exactly at `k = 6`, sharp within counting), the weakening analysis (W1)–(W4), and the
three exact checks.

Not proved, not implied: `|P_x(e)| ≤ 2` at `k=6`; local finiteness or non-emptiness of any cycle
locus at `k=6`; `χ(R^2) ≥ 7`.
