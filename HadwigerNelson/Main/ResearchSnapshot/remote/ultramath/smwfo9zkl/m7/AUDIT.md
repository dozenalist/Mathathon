# Audit: where `§6.3.1`–`§6.3.2` of the paper uses `k = 5`

Member `m7`, swarm `smwfo9zkl`, direction `d7`. References are to the paper
*The Euclidean plane is not five-colorable* (OpenAI, 23 Sep 2026), printed page numbers; the
extractions used are `paper/paper.txt` (`pdftotext -layout`) and `work/pages/pNN.txt` /
`pNN_raw.txt` (per-page `-layout` and `-raw`) with 150 dpi PNGs in `work/pages/pgNN-NN.png`.
Everything in the "status at `k = 6`" column is verified by `verify.py` / `verify_indep.py`.

Setting: `x` with `0-1-2-3 ⊆ Gamma_x`; `U = {0,2}`, `V = {1,3}`, `T = {0,1,2,3}`,
`O = I \ T` the outsiders (`|O| = k-4`), `X` the outsider of `k = 5`.

| # | paper, page | what is used | `k`-dependence | status at `k = 6` |
|---|---|---|---|---|
| 1 | `§6.3.1`, p. 38 | "with fifth label `X`"; the canonical state is `X` if `X ∈ P_x(e)`, else `U` or `V` | needs `\|O\| = 1` | **undefined**: `\|O\| = 2`. Which of `X, Y` plays `X`? No canonical choice; the palette map has 33 values. |
| 2 | `§6.3.1`, p. 38 | "A palette not containing `X` has size at most two, and (6.2) excludes every singleton and every adjacent pair of the four-cycle, leaving precisely the two diagonals." | `\|P\| <= 2` | **false**: `\|P\| <= 3`. Cycle-label-only palettes: `6` instead of `2` (`U, V` and the four triples of `T`); all `20` triples of `I` are admissible. |
| 3 | Lemma 6.6, p. 38 | state groups are distinguishable: "Two different state groups would require at least three palette labels, contradicting Proposition 5.6." | `3 > k-3` | **false**: `3 <= 3`. Exact witnesses `{0,2,X}` (carries `U` and `\{X\}`) and `{1,3,X}`. This is the sentence that makes the palette determine the state and hence gives `L^1`-continuity; `k6_nogo.md` C1b records the same witnesses. Counts: `0` ambiguous palettes at `k=5`, `2` at `k=6`, `11` at `k=7`. |
| 4 | Lemma 6.6, p. 38 | "a diagonal already fills both palette slots" | `\|P\| = 2` | **false**: `\{0,2\}` does not fill three slots; `\{\{0,2,X\}\}` carries a diagonal *and* a singleton. |
| 5 | `§6.3.1`, p. 38 | "If either [diagonal state] were null, the other and `X` would give the impossible alternation of Lemma 6.4." | Lemma 6.4's final step needs `3 > k-3` | the paper's `k = 6` form fails (`chi(K_3) = 3 = k-3`), **but** Theorem 2 of `RESULT.md` recovers it at a cyclic centre: at `k = 6` no 2-valued palette map with `\|A\|+\|B\| >= 4` exists. At a four-cycle centre the surviving 2-valued maps are the `13` pairs "outsider singleton + set of size `<= 2`". |
| 6 | `§6.3.1`, p. 38 | "Both supports are nonempty. Across their nonparallel density directions, the four represented labels force singleton density one of `X`. Lemma 6.3 therefore gives a strict margin…" | `\|I \ (U ∪ V)\| = 1` | **fails**: `\|I \ (U ∪ V)\| = k-4 = 2` (`\{X,Y\}`). Theorem 3 of `RESULT.md`: what Lemma 5.2(2) gives is density one of `I \ (G_1 ∪ G_2)`, size `2`. |
| 7 | `§6.3.1`, p. 38–39 | "On every component gap of `S \ N_x` the state is `X` almost everywhere"; gaps have length `<= kappa` "contrary to the state-change rule" | three states, pairwise disjoint | **fails**: with `>= 3` values not pairwise disjoint (`\{0,2\}` vs `\{0,2,X\}`) the phrase "the state is `X`" has no meaning, and the gap bound uses that gaps carry a *single* state. |
| 8 | `§6.3.2`, p. 39 | transport rule: "The spatial sums of every such nonparallel pair have density one of `X`. … Neither output state can be `X`." | a *single* forbidden label | **fails**: the forced set is `\{X,Y\}`; the state "an outsider is in the palette" (group `⊆ \{X,Y\}`) is consistent with density one of `\{X,Y\}`, so there is no contradiction. |
| 9 | `§6.3.2`, p. 40 | "Immediately to the right of `a` the state is `X` almost everywhere, so immediately to the right of `R a` it is non-`X` almost everywhere. It must therefore be `V`…" | exactly 3 states, one of them a singleton | **fails**: "non-`X`" is a `2`-label set at `k = 6`, and "therefore `V`" needs `\{U, V, X\}` to be the whole alphabet. |

**Summary of the audit.** The four-cycle half of Theorem 6.5 is a `k <= 5` argument at *four*
independent places: rows 1, 2, 3/4 (the state reduction, `3 > k-3`), and rows 6, 8, 9 (the
single-label separation, `k-4 = 1`). Rows 1–4 are palette-size failures, repaired — as far as they
can be — by Theorem 2'. Rows 6, 8, 9 are **label-count** failures, and Corollary 3.1 of `RESULT.md`
shows that they survive the strongest palette hypothesis (all palettes of size `2`); they are
therefore not repairable by any statement about palettes.

**Relation to the triangle-interface barrier.** `results/K6-BARRIER.md` §3 and `k6_nogo.md`
Theorem B record that at a *triangle* interface at `k = 6` the outsider set has size `2` of `3`,
so the external state graph is not bipartite. Rows 6, 8, 9 above are the same phenomenon
(`missing single label` ↦ `2-label set`) occurring at the *four-cycle stratum of §6.3*, i.e. one
stage earlier in the paper than the `§8` barriers. So at `k = 6` the "two outsiders instead of one"
obstruction is not confined to `§8`.

**Non-vacuity.** Two checks that this audit is not an artefact:
(i) at `k = 5` every inequality in the table has the right direction, and the audit reproduces the
paper's own structure (7 admissible palettes, 3 states, all 7 disjoint pairs trigger Theorem 2);
(ii) the four-cycle stratum is non-empty at `k = 6`: `RESULT.md` Theorem 5 exhibits an explicit
proper measurable 6-colouring of a strip with `Gamma_x ⊇ C_4` at every lattice corner, verified
exactly. So the failures above are failures of *proof steps about a non-empty stratum*, not of a
vacuous hypothesis.

---

## Inputs quoted, with the rendered-page check

The sprint brief warns that `pdftotext` alone loses fractions, radicals and delimiters. Every input
I use was checked two ways: both extraction modes agree on its *form*, and its *arithmetic content*
is proved exactly by `verify.py` §A (which is stronger than a visual check for the two formulas that
matter most).

| input | `-layout` | `-raw` | symbolic check |
|---|---|---|---|
| (5.2) p. 27 | `c(x+e+v) ∈/ P_x(e) ∪ P_x(v)` | `c(x + e + v) / ∈ Px(e) ∪ Px(v)` | — |
| (5.3) p. 27 | `P_z(f) ∩ P_x(s(f)) = ∅` | same | — |
| (5.7) p. 29 | `P_x(f) ∩ P_x(R f) = ∅` | same | — |
| (6.1) p. 34 | `limsup_{h→0,h≠0} D_ij(B,h)/\|h\| > 0` | same | — |
| (6.2) p. 35 | `P_x(e) ⊄ {i,j}` | same | — |
| Lemma 6.4, p. 37 | `γ = 2 arcsin(1/(2√3))`, `cos γ = 5/6` — **the fraction and the radical are split across two lines by `-layout`, and the `-raw` extraction drops the display entirely** | — | proved: `cos(2 arcsin(1/(2√3))) = 5/6`, `sin γ = √11/6`, `\|1-e^{iγ}\| = 1/√3`, triangle side `= 2 sin(κ)·\|1-e^{iγ}\| = 1` |

The two facts about `γ` used in Theorem 2 are exactly (i) `cos γ = 5/6`, which fixes `γ` up to sign
and pins the reading of the destroyed fraction, and (ii) `γ/π ∉ Q`, for which the paper's own
argument is quoted in the PNG of p. 37 (`2 cos γ = 5/3` would be a rational algebraic integer).
No other displayed formula in `§6.3` is used quantitatively.
