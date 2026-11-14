# Reader checks

Try these after the [first briefing](Progress/2026-11-14-first-briefing.md). Answer aloud or on paper before opening the answer. Success means explaining the distinction in your own words, not recalling project codes.

1. **A direction-grid search leaves six configurations. Why has it not classified all possible plane colourings?**

<details><summary>Answer</summary>

The search covers only its specified discrete directions and licensed constraints. Arbitrary directions may fall outside the grid. Even a surviving abstract configuration need not arise from an actual colouring. Both coverage and the geometric connection require proof.

</details>

2. **What does CC60 forbid, and name two hypotheses that stop us from applying it to an arbitrary colour-list puzzle.**

<details><summary>Answer</summary>

It forbids the residual colours fitting into only two labels. It requires actual approaching connected sets sharing a centre, signed directions within a closed cone of width at most 60 degrees, a measurable weak colouring, and the stated support exclusions. Any two of these, correctly explained, distinguish the theorem from an arbitrary list puzzle.

</details>

3. **Thirty-four proper five-colourings give every vertex a different signature. What does this prove about pairs, and what does it leave open?**

<details><summary>Answer</summary>

A signature lists a vertex's colours across the witnesses. Different signatures mean every distinct pair receives different colours in at least one witness. No pair is forced equal in all proper five-colourings of that graph. This says nothing comparable about all other graphs and does not colour the whole plane.

</details>

4. **Why does one small Voronoi cell not disprove Kepler, and what must a compensation argument establish?**

<details><summary>Answer</summary>

Packing density depends on large-scale averages. A small cell may be offset by larger neighbours. A successful proof needs a universally valid geometric compensation rule and a justified passage to arbitrary large regions or infinite packings, including boundary effects. One successful finite transfer example is insufficient.

</details>

5. **Undo the staircase subtraction `(4,1) → (1,0)`. Why must the zero be retained, and what major bijection is still missing?**

<details><summary>Answer</summary>

The retained length is two, so add the odd staircase `(3,1)` to recover `(4,1)`. Dropping the zero loses length information needed to select the staircase. The bridge relates gap partitions to coordinates; it does not provide the new natural correspondence from parts congruent to 1 or 4 modulo 5 to gap partitions.

</details>

6. **A Lean theorem says that assumptions H imply conclusion C, and a Python program passes a million tests intended to establish H. Can we report C for every input?**

<details><summary>Answer</summary>

No. Lean has certified the implication as stated, while the tests cover their tested inputs and implementation. We still need a proof of H throughout the claimed domain, and must check that H and C actually describe the intended mathematics. The same distinction separates Kepler's normalization from geometry and Hadwiger–Nelson's local obstruction from a global bound.

</details>
