# Triage of reported errata in the paper

Several swarm members audited the paper against `pdftotext` output. That output drops fractions,
superscripts, radicals and large delimiters, and it reflows displayed formulas. Four reported
"defects" are artifacts of the extraction; one is a terseness, not a gap. Each verdict below was
checked against a **rendered image** of the page, not against the extracted text.

| # | Reported defect | Where | Verdict |
|---|---|---|---|
| 1 | The §1 seven-colouring takes `r = sqrt(2/5)`, so `2r = 1.2649 > 1` and the colouring is not proper | §1, p. 2 | **Artifact.** The PDF reads "circumradius `r = 2/5`"; the radical belongs to "nearest-neighbor distance `√3 r`". With `r = 2/5`: `2r = 4/5 < 1` and `(√21 − 2)(2/5) > 1 ⟺ 84 > 81`. The colouring is correct. |
| 2 | Lemma 5.5 needs `L ≤ c_0/(2C_0)`, not `L ≤ c_0/C_0`; `C_0 d ℓ_r ≤ ½ c_0 d` is false on an admissible `ℓ_r` | §5.3, p. 32 | **Artifact.** The display reads `F'_{j_r}(t) ≥ 1 + c_0 d − ½ C_0 d ℓ_r ≥ 1 + ½ c_0 d`. The factor `½` is printed and dropped by the extraction; with it, `ℓ_r < L ≤ c_0/C_0` gives the bound. |
| 3 | §3.2 says "averages of `a(h)²` tend to zero" but the pair criterion gives `a(h)` | §3.2, p. 17 | **Artifact/no error.** `a(h) = ‖P F_{j*,h}‖₂` is the L² norm; the pair criterion gives `Avg a(h)² → 0` exactly, and Cauchy–Schwarz gives `Avg a(h) → 0`. The printed sentence is right. |
| 4 | Display (8.6) is ambiguous: `((35+12i)/37)(g + t)` vs `((35+12i)/37)g + t` | §8.6, p. 57 | **Artifact.** The PDF prints the large parentheses; only the bracketed reading matches Tables 1–2, and it is the printed one. |
| 5 | Lemma 8.6 assumes without proof that the permissible shifts contain a neighbourhood of `0` | §8.3, p. 55 | **Not a gap.** The proof fixes `U'` so that `q + v'_j ∈ V` for all `q ∈ U'`; at `h = 0` the constructed neighbour is `q + v'_j ∈ V`, and `V` is open, so the permissible `h`-set is a neighbourhood of `0`, uniformly on a compact sub-ball. The paper then says "in a still smaller ball". Terse, but correct. |
| 6 | §8.6 final display gives `(2.49, 2.50)` for `u_T` while Table 2 gives `(2.493, 2.495)` | §8.6 | **Cosmetic.** Both intervals contain the exact value `2.4934375511…`; the stricter printed interval is the correct one. |
| 7 | §8.6 says "the other six rows … by the same two products" but does not print them | §8.6 | **Exposition.** The six rows are correct; they are now machine-checked (see below). |

## The genuinely new check that survives

The finite certificate of §8.5–8.6 is now machine-checked twice, independently:

* Lean (`OAI_Audit_Moser.lean`, swarm member m6, compiled here under Lean 4.34.1): the seven exact
  points `0, A, B, T, uA, uB, uT` in `Q(√3, √11)`; exactly eleven unit edges; no other unit pair;
  pairwise distinct; not 3-colourable; all seven in the region (8.4). Axioms
  `[propext, Classical.choice, Quot.sound]`.
* Exact arithmetic in `Q(√3, √11)` (swarm member m11, `exact2.py`): the same eleven edges with
  squared length exactly 1, the same non-3-colourability by the equilateral-triangle argument
  `c(0) = c(T) = c(uT)` against `|T − uT| = 1`, and the region inequality for all seven points
  with explicit margins.

## Lesson for anyone auditing this paper

`pdftotext` is not a faithful rendering of this PDF for displayed mathematics. Any claimed
erratum in a formula must be checked against `pdftoppm` output. In this audit, five of five
formula-level "defects" evaporated on inspection. No correction to a *displayed formula* of the
paper survived scrutiny; what remains a matter of judgement is only whether some prose steps are
terse enough to deserve expansion, which is a different question.
