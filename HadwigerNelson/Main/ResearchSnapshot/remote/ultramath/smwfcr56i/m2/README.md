# m2 / direction d1 — k = 6 analogue of the five-label architecture

Files
-----
| file | content |
|---|---|
| `k6_nogo.md` | the report: Theorems A–D, the k-dependence table of §5–§8, certificates, the exact list of inputs a six-label run needs, and an appendix verifying the paper's §1 seven-colouring with its actual constants |
| `check_k.py` | exact enumerations C1, C1b, C2, C3, C4, C5, C6, C7 (palettes at cycle loci, external state alphabets, the paper's own `Z/5` arithmetic, colouring certificates) |
| `check_moser.py` | exact interval-arithmetic verification of the k-independent endgame §8.5–8.6: eleven unit edges of the Moser graph, no proper 3-colouring, all seven placed vertices strictly inside region (8.4) |
| `check_gadget.py` | Lemma E on 3-equality gadgets (no 3-vertex gadget; the diamond forces equality at `sqrt 3`) |
| `check_seven.py` | exact verification of the paper's §1 hexagon constants: `r = 2/5`, `2r = 4/5 < 1`, `(sqrt21-2)r > 1`, `|2-omega|^2 = 7` |
| `*.out` | saved output of each script |

Reproduce (all under one second, no dependencies beyond python3)
-----------------------------------------------------------------

```text
python3 check_k.py
python3 check_moser.py
python3 check_gadget.py
python3 check_seven.py
```

Headline statements
-------------------
* **Theorem A**: for every weak measurable `k`-colouring and every centre `x`,
  `|P_x(e)| <= k-3` for a.e. `e`.  (`k=5`: 2, the paper's Prop. 5.6.  `k=6`: 3.)
* **Theorem B**: at a length-three interface, the outsider set
  `A(e) = P_x(e) ∩ T^c` satisfies `1 <= |A(e)| <= k-4` and `A(e) ∩ A(Re) = empty`.
  (`k=5`: singleton, alternating.  `k=6`: 1 or 2 of 3 labels, 6 states, non-bipartite.)
* Both are the inequality `k <= 5`.  A third label-count input, `ell <= k` for the
  extracted interface cycle, adds the case `ell = 6` at `k = 6`.
* Everything else in §5–§8 is `k`-independent, including the region (8.4) and the
  Moser step, which is verified here exactly.
