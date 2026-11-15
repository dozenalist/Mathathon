# Slides outline (about 20 minutes, 14 slides)

Rule: every result on a slide also appears in `report.tex`. The report section is given in brackets. Figures are the reader's SVGs; each slide states the one inference its figure enables, in words. The outline is realised in `slides.tex` (Beamer). It compiles to `slides.pdf` with Tectonic 0.15.0, using PNG renders of the SVGs in `slide-figures/`, produced by Edge headless at 2× scale.

1. **The question.** Colour the plane so that points at distance 1 differ. Known: $4\le\chi$ (Moser spindle), $5\le\chi$ (de Grey 2018), $\chi\le7$ (hexagons). [§1]
2. **What was supplied.** OpenAI's manuscript, 23 September 2026: no five-colouring, so $6\le\chi\le7$. Not our result. Two bridges: transfer to weak measurable colourings, then geometry. [§1, §2]
3. **What we did in 40 hours.** A six-lesson checked reader; a three-centre proof of Lemma 6.3; CC60; computations and corrections. Status legend. No global chromatic result. [abstract, §1]
4. **Weakness as a ruler experiment.** Figure `weak-turning-ruler.svg`. Inference: a half-plane colouring has a bad share of two thirds at points half a unit from the boundary, so it is not weak. [§2.1, §6]
5. **"Almost never" becomes "never".** Figure `density-turn.svg`. Inference: turning costs a factor of 4 in area, so $\varepsilon<1/5$ leaves a positive share of bad rulers (Lemma 4.3). [§2.2, §6]
6. **Straddling a connected set.** Figures `straddle-band.svg` and `straddle-gap.svg`. Inference: connectedness turns one zero-area circle into a band of positive area; without it, the contact can be missing. [§2.3, §6]
7. **Interfaces at a centre.** Figures `interface-model.svg` and `interface-shadow.svg`. Inference: a tiny interface excludes its two labels on a thin band hugging the unit circle, outside on the side it points to. [§2.5, §6]
8. **The proof map.** Table of steps: transfer, density, palettes, states, interfaces, strips, cycles. [§2.6]
9. **Three centres, one leftover label.** Figures `three-centre-triangle.svg` and `three-centre-count.svg`. Theorem 3.1 and the counting lemma, with the full proof on one slide. Status: proved; Lean 4.34.1; integrated in the team build R1. [§3]
10. **CC60.** Figure `interface-cone.svg`. The exact statement: signed directions in a closed $60^\circ$ arc, zero-area exclusions on $\Delta(K_i)$, at least three labels survive. Status: Lean 4.34.1. [§4]
11. **Sharpness and limits of CC60.** The 20-colour construction above $60^\circ$ (paper-level, refereed). What CC60 does not say. [§4]
12. **Further local results.** The canonical paired palette is excluded for six colours (refereed); even-walk parity obstructions (Lean 4.34.1); the producer pieces, which are still conditional. [§5]
13. **Computations and corrections.** Heule-union certificate, no forced pairs, direction-filter counts, and the MC120 correction. [§5]
14. **Honest status.** The claim table, with "no global chromatic result" in bold, the Lean 4.34.1 vs 4.35.0 gap, AI use and checking, and the questions we expect. [§7–§10]

Talking points and prepared answers are in `speaker-notes.md`. Speaker check, for each slide: can the presenter explain the definitions, the key step, what is new versus cited, what the AI did, and how sure we are? (These are the judges' Q&A topics.)
