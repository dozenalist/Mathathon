# Speaker notes for `slides.pdf` (18 main slides plus 6 backups, about 20 minutes)

Timing: about 65 seconds per main slide. Slides 4, 11, 13 and 15 deserve more time; slides 1–2 and 16–18 less. Backups are for questions only. Every claim below is in `report.tex`; the section is given in brackets. Say "cited" when the result is the manuscript's, and "ours" when it is the team's.

## Talking points

1. **Title.** Name the team, the question and the repository.
2. **The question [§1].** Define χ(ℝ²) in one sentence. The known bounds are 4 (Moser spindle), 5 (de Grey 2018) and 7 (hexagons), all cited.
3. **What was supplied [§1–2].** OpenAI's manuscript proves 6 ≤ χ ≤ 7. Say clearly that this is not our theorem. It makes two moves; we teach the second.
4. **What we did [abstract, summary page].** Five products. Read the "what is new" sentence word for word, including the novelty caveat on CC60. Say "No global chromatic result" out loud.
5. **Why a local cone obstruction matters [summary page].** The proof ends at one centre. Six colours would need the analogous refutation. CC60 covers every configuration whose directions fit a 60° arc; 6 of 174 grid candidates survive. The only route to seven colours needs two open lemmas, L6 and F6.
6. **Weakness [§2.1].** The ruler experiment: half a unit from the boundary, 240° of 360° of directions are bad, a share of 2/3.
7. **Density [§2.2].** The key step of the supplied proof: turning costs a factor of 4 in area, so ε < 1/5 suffices.
8. **Straddling [§2.3].** Δ(K) and the intermediate value theorem. Mention the backup slide on the missing contact.
9. **Interfaces [§2.5].** Connected sets through one centre, each excluding two labels; a tiny one casts a thin shadow on the unit circle.
10. **Proof map [§2.6].** Walk the table. The case fan has exactly three branches.
11. **Three centres [§3].** State the theorem and give the idea in two sentences; the full proof is a backup. Status: proved; checked in Lean 4.34.1; integrated in R1.
12. **CC60 [§4].** Read the hypotheses slowly: signed directions, closed 60° arc, zero-area exclusions. The sets need not be connected.
13. **CC60 key step [§4].** Walk the five steps. End on where 60° is used: the 120° arc in step 2, and γ < 60° in step 4.
14. **Sharpness [§4].** A 20-colour construction defeats every wider cone. Six-colour sharpness and novelty are *not* established.
15. **867-line shorter Lean proof [§5].** Point to the two biggest bars, States −303 and ConditionalLimits −159, and the one new module, AvoidingTrace +237. S2 is not counted.
16. **Further local results [§5].** The four-list obstruction (refereed), even walks (Lean), and the producer pieces (still conditional).
17. **Computations and corrections [§5].** Exact certificates, the 95 → 174 recount, and the false closed-120° claim (a 19-colour counterexample).
18. **Honest status [§7–10].** The Lean 4.34.1 vs 4.35.0 gap, AI use, and how sure we are.

Backups B1–B6: definitions; the spectral transfer; the full three-centre proof; the sharpness construction; the interface model and missing contact; AI use and checking.

## Likely questions, with short answers

The judges' guidelines name five question areas: definitions, the key step, new versus known, the AI's role, and certainty.

- **What is a weak measurable colouring?** Measurable colour classes, with almost every unit pair (by position times direction) getting distinct colours. Changing a colouring on a null set keeps it weak. [§2.1]
- **What is the key step?** In the supplied proof, the density lemma (manuscript Lemma 4.3); in CC60, steps 2–5 on slide 13. It turns "almost never" into "never" at robust points. Everything after it uses exact exclusions. [§2.2]
- **What is new and what is known?** The five-colour theorem and its whole proof are the manuscript's. Ours: the exposition; the three-centre proof of Lemma 6.3; CC60 and its sharpness; the four-list obstruction and the other refereed lemmas; the Lean simplification; the computations. CC60's novelty is *not* established: a bounded search classed it as a new candidate only. [§9]
- **What did the AI do?** Claude drafted the exposition and the report, and separate Claude instances refereed each lesson against the manuscript and Lean sources. Research workers produced and reviewed the local results and the Lean files. Every claim was checked against the sources, archived compiler logs, or exact scripts. [§8] *(Team: confirm the tool list before presenting.)*
- **How sure are you?**
  - "Checked in Lean 4.34.1" means archived compile logs with only the three standard axioms; nothing has been rebuilt under 4.35.0.
  - "Proved" means a paper argument with an independent referee report on file.
  - Candidates and unaudited numbers are not claimed. [§7]
- **Does CC60 rule out six colours?** No. It forbids a kind of local configuration, and nothing shows that a six-colouring must produce it. [§4]
- **Why "closed" 60°?** The equality case at exactly 60° is included and used: the six-colour consumer puts directions at both ends of the arc. [§4]
- **Why does connectedness matter?** If K is only the two endpoints of a length-2 segment and z is one of them, z straddles K but has no unit contact. [§2.3]
