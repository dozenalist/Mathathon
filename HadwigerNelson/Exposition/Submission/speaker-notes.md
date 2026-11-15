# Speaker notes for `slides.pdf` (14 slides, about 20 minutes)

Timing: roughly 80 seconds per slide, with slides 5, 9 and 10 longer and 1, 13 and 14 shorter. Every claim below is in `report.tex`; the section is in brackets. Say "cited" when the result is the manuscript's, and "ours" when it is the team's.

## Talking points

1. **The question [§1].** Define χ(ℝ²) in one sentence. Give the known bounds: 4 from the Moser spindle, 5 from de Grey in 2018, and 7 from hexagons. All are cited.
2. **What was supplied [§1–2].** OpenAI's manuscript proves 6 ≤ χ ≤ 7. Say clearly that this is not our theorem. Two moves: (1) a proper colouring yields a weak measurable one; (2) no weak measurable five-colouring exists. We teach move 2.
3. **What we did [abstract, §1].** Four products: the reader, the three-centre proof, CC60, and the computations and corrections. Say "No global chromatic result" out loud.
4. **Weakness [§2.1].** The ruler experiment. Half a unit from a half-plane boundary, 240° of the 360° of directions give a bad ruler, a share of 2/3. So the half-plane colouring is not weak.
5. **Density [§2.2].** The key step of the second move. Robust points of one colour are never 1 apart. Turning the ruler costs a factor of 4 in area, so ε < 1/5 suffices.
6. **Straddling [§2.3].** Δ(K), and the intermediate value theorem on a connected set. The gap figure shows why connectedness matters.
7. **Interfaces [§2.5].** The manuscript constructs connected sets through one centre, each excluding two labels. A tiny one casts a thin shadow just outside the unit circle on the side it points to.
8. **Proof map [§2.6].** Walk the table. The case fan: step 5 has exactly three branches.
9. **Three centres [§3].** State the theorem and give the proof in four lines. Then the status: proved; checked in Lean 4.34.1; integrated in the team build R1. What is new is the third centre in place of the manuscript's implicit-function step. The forced-label step itself already appears in the manuscript's Lemma 6.7.
10. **CC60 [§4].** Read the hypotheses slowly: signed directions, a closed 60° arc, zero-area exclusions. The sets need not be connected. Point to the red overlap in the figure.
11. **Sharpness [§4].** A 20-colour construction defeats every wider cone. Six-colour sharpness and novelty are *not* established.
12. **Further local results [§5].** The four-list obstruction (refereed), even walks (Lean), and the producer pieces (still conditional).
13. **Computations and corrections [§5].** Exact certificates. The 95 → 174 recount. The MC120 closed-120° claim was false, as shown by a 19-colour counterexample. Simplification: 150 lines shorter.
14. **Honest status [§7–10].** The Lean 4.34.1 vs 4.35.0 gap, how AI was used, and how sure we are.

## Likely questions, with short answers

The judges' guidelines name five question areas: definitions, the key step, new versus known, the AI's role, and certainty.

- **What is a weak measurable colouring?** Measurable colour classes, with almost every unit pair (by position times direction) getting distinct colours. Changing a colouring on a null set keeps it weak. [§2.1]
- **What is the key step?** The density lemma (manuscript Lemma 4.3). It turns "almost never" into "never" at robust points. Everything after it uses exact exclusions. [§2.2]
- **What is new and what is known?** The five-colour theorem and its whole proof are the manuscript's. Ours: the exposition; the three-centre proof of Lemma 6.3; CC60 and its sharpness; the four-list obstruction and the other refereed lemmas; the Lean simplification; the computations. CC60's novelty is *not* established: a bounded search classed it as a new candidate only. [§9]
- **What did the AI do?** Claude drafted the exposition and the report, and separate Claude instances refereed each lesson against the manuscript and Lean sources. Research workers produced and reviewed the local results and the Lean files. Every claim was checked against the sources, archived compiler logs, or exact scripts. [§8] *(Team: confirm the tool list before presenting.)*
- **How sure are you?**
  - "Checked in Lean 4.34.1" means archived compile logs with only the three standard axioms; nothing has been rebuilt under 4.35.0.
  - "Proved" means a paper argument with an independent referee report on file.
  - Candidates and unaudited numbers are not claimed. [§7]
- **Does CC60 rule out six colours?** No. It forbids a kind of local configuration, and nothing shows that a six-colouring must produce it. [§4]
- **Why "closed" 60°?** The equality case at exactly 60° is included and used: the six-colour consumer puts directions at both ends of the arc. [§4]
- **Why does connectedness matter?** If K is only the two endpoints of a length-2 segment and z is one of them, z straddles K but has no unit contact. [§2.3]
