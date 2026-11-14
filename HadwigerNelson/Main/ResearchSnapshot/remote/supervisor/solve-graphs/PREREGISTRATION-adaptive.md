# Pre-registration: adaptive class-refinement chase at k = 5

Written **before** execution. ONE process, 60 s TOTAL (all solver calls, all checks, harness
overhead). No coordinate changes, no new graph, no claim about `chi(R^2)`.

## Correction to the previous block
The previous block reported that steps 7–8 of the frozen 8-pair list gained nothing because of
"vertex-0 endpoint concentration". **That causation was wrong and is withdrawn.** The pairs (0,208)
and (0,255) had *already been separated* by earlier witnesses in the same run, so replaying them was
redundant work created by a **static** pre-registered pair list. The vertex-0 observation remains a
fact about that list; it is not established as the cause of the zero marginal gain.

## Baseline
All 18 saved verified colourings (8 ensemble partitions, the (0,39) witness, the (0,50) witness,
and the 8 chase witnesses). Survivor set
`S = {(i,j) : i<j, ij not an edge, c_w(i) = c_w(j) for every saved witness w}`,
with `|S| = 491`. Since two vertices with equal colour in a proper colouring are non-adjacent, the
491 pairs are exactly the within-class pairs of 24 **colour-signature classes**: a class is a set of
vertices with identical colour vector across all 18 witnesses, and it contributes `C(m,2)` pairs.
Claimed sizes 19,17,14,9,6,5,4,4,3,3 and fourteen of size 2 (sum of `C(m,2)` = 491). **Step 0 of the
run verifies this independently before any solver call**; if the structure does not reproduce, the
run reports the mismatch and stops.

## Deterministic ADAPTIVE selection rule (replaces the frozen list)
Nothing is pre-listed. At every step the rule is recomputed from the *current* state:

1. Recompute `S` from all witnesses so far, and the signature classes of the vertices in `S`.
2. Maintain `use[v]` = number of times `v` has been an endpoint of a tested pair.
3. For each untested pair `(i,j) in S` define the key
   `(-|class(i)|, use[i]+use[j], i, j)` and take the **lexicographic minimum**.
   That is: prefer the **largest surviving class**; among equals prefer the **least-used endpoints**
   (endpoint diversification); then smallest `i`, then smallest `j`.
4. Mark the pair tested, solve with the constraint `c(i) != c(j)`, i.e. the combinatorial
   **disequality** edge. Note `|p-q| != 1` for every survivor, so this edge is never a unit edge and
   the graph's coordinates are untouched.
5. On SAT: verify the witness against **all 2722 edges**; if invalid, stop. Otherwise append the
   witness, increment `use`, recompute `S` and the classes **immediately**.
6. On UNSAT: **stop at once**, save the CNF, and record it as a *solver-only candidate*, never as a
   certified forced equality.
7. A pair already separated is never retested, because the rule only ranges over the current `S`.
8. Hard cap **16** targeted pairs.

By construction each successful SAT target removes at least its own pair from `S`.

## Meaning of the outcomes
* **`|S| = 0`** — the accumulated witnesses separate every non-adjacent pair of this graph, i.e. the
  saved witnesses form a **finite witness certificate that no non-adjacent pair of THIS graph is
  forced equal at k = 5**. This is a statement about this 553-vertex graph only.
* **`|S| > 0`** — report the remaining candidates and the measured gain per step. Survivors are
  **untested candidates, not forcing evidence**.
* **UNSAT at some step** — that pair is a candidate forced equality (solver-reported only until a
  certificate is independently checked). Not claimed as forcing certified.

## Diversification note
The first-occurrence symmetry-breaking clauses used in the earlier ensemble are **dropped** here:
they exist to make a partition uniquely nameable for blocking, and blocking is not used in this run.
Each solve differs by its split constraint, so repeated partitions cannot arise from this schedule.
