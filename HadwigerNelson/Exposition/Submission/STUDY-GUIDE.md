# Study guide for the presenters (two pages)

For Jarom, Andrew and Carter. It covers what you must be able to say without the slides. Everything here is in `report.tex`, and the section is in brackets. **The headline: no global chromatic result.** OpenAI's supplied proof gives $6\le\chi(\mathbb R^2)\le7$, and we change neither bound.

## 1. Definitions (say each in one sentence)

- **$\chi(\mathbb R^2)$:** the fewest colours such that no two points at distance exactly 1 share a colour.
- **Weak measurable colouring:** the colour classes are measurable, and *almost every* unit pair (measured over positions × directions) gets two colours. In ruler terms, a randomly dropped and turned unit ruler has both ends the same colour with probability 0 in every window. [§2.1]
- **Robust point (density one):** small disks around it are almost entirely one colour. [§2.2]
- **Straddle region $\Delta(K)$:** the points closer than 1 to some point of $K$ and farther than 1 from another. If $K$ is connected, each such point is exactly 1 from some point of $K$. [§2.3]
- **Palette $P_x(e)$:** the labels that persist in direction $e$ in limits of colourings of circles of radius close to 1 near the centre $x$. A palette is *not* the colour of a single point. [§2.4]
- **Interface (Proposition 7.1):** a connected set through a common centre that excludes both labels of one cycle edge from its straddle region. [§2.5]

## 2. The key step of each result

| Result | Status | Key step, in one breath |
| --- | --- | --- |
| Supplied: no 5-colouring [§2] | cited | (a) A proper colouring yields a weak measurable one (spectral, Theorem 1.3). (b) The density lemma: robust points of one colour are never 1 apart, because turning a ruler costs a factor of 4 in area, so $\varepsilon<1/5$ leaves a positive share of bad rulers. (c) Interfaces at one centre form a 3-, 4- or 5-cycle, and each length is refuted. |
| Three-centre proof of Lemma 6.3 [§3] | proved; Lean 4.34.1; in R1 | Two support directions $60^\circ$ apart give centres $x$, $x+e^{ib}$, $x+e^{id}$, all one unit apart, so their palettes are disjoint. Each outer palette needs a label outside $K$, and $J$ is already used at $x$. So both outer palettes contain the single leftover label $X$: contradiction. |
| CC60 [§4] | Lean 4.34.1 | If only labels $a,b$ survived, $W=\bigcap\Delta(K_i)$ would be two-coloured. Outer strips over a $120^\circ$ arc give one arc $S$ of radius $r\in(1,2)$ inside $W$. Turning by $\arccos(r/2)<60^\circ$ gives unit neighbours, so binary rigidity makes $S$ one colour. The ends of $S$ are $r>1$ apart, so there is a same-colour unit pair: contradiction. **The $60^\circ$ is used twice:** the arc is $180^\circ-60^\circ$, and $\arccos(r/2)<60^\circ$. |
| Sharpness [§4] | proved (refereed), not Lean | For any cone wider than $60^\circ$, two short segments and an explicit 20-colouring leave only two labels. So $60^\circ$ is sharp for *arbitrary* palettes, though not shown for six colours. |
| 867-line shorter Lean proof [§5] | Lean 4.34.1 | The total is the encoding refactor ($-126$), plus R1, the three-centre integration ($-24$), plus S1, dead-code deletion with Lemma 6.7 made branch-free ($-265$), plus S2, a second dead-code pass ($-452$). The root theorems are unchanged and use only the standard axioms. The chart on slide 15 shows the build after S1. |
| Canonical paired palette excluded [§5] | proved (refereed) | A finite unit-distance configuration in the list field has no proper list colouring, so no centre carries that palette. |
| Closed-$120^\circ$ MC120 is false [§5] | proved (refereed) | A 19-colour counterexample. |

## 3. The five questions the judges' guidelines list

1. **Definitions?** Use section 1 above. Lead with "weak = bad rulers have probability zero".
2. **The key step?** In the supplied proof, the density lemma. In our work, the CC60 key step: say where the $60^\circ$ is used.
3. **What is new versus known?** The five-colour theorem is OpenAI's. Ours:
   - the three-centre proof;
   - CC60 and its sharpness;
   - the 867-line shorter Lean proof;
   - the refereed lemmas and counterexamples;
   - the checked reader.
   CC60's novelty is **not** established: a bounded literature search found it only as a new candidate.
4. **What did the AI do?** Claude drafted and refereed the exposition, the report and the slides. Research workers produced and reviewed the local results and the Lean files. Every claim was checked against the sources, archived compiler logs or exact scripts. *(Jarom: confirm the roles before presenting.)*
5. **How sure are you?** See section 4.

## 4. Certainty levels: say these words, no stronger

| Label | Meaning | Say |
| --- | --- | --- |
| checked in Lean 4.34.1 | An archived compile with mathlib pinned at `d13f23b`, using only `propext`, `Classical.choice` and `Quot.sound` | "checked in Lean 4.34.1". **Not** "Lean-verified": the event track needs 4.35.0, and Carter's port is in progress. |
| proved (refereed) | A paper argument with an independent referee report on file | "proved, independently refereed" |
| computation | An exact check of one named finite object | "checked by computation, for that object only" |
| cited | The manuscript or the literature | "OpenAI's", "de Grey's" |
| candidate / open | Not established | "not claimed" |

**Traps to avoid:**
- "We proved six colours fail." We did not.
- "CC60 rules out six colours." It forbids a kind of local configuration.
- "Lean-verified."
- Saying S2 removed 717 lines on top of S1: S2's −717 is measured against R1 and *includes* S1's −265.
