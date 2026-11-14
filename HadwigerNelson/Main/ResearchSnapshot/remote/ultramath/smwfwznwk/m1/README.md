# m1 — the six-cycle free-label case at k = 6

Read `REPORT.md` first (what is decided), then `proof.md` (the proofs). `run_all.sh` reproduces
every number in about 30 seconds:

    cd .ultramath/smwfwznwk/m1 && ./run_all.sh      # prints "ALL CHECKS PASSED"

## What is here

| path | content |
|---|---|
| `REPORT.md` | the answer to the handoff, in five sections (tasks 1–5) |
| `proof.md` | Theorem 1 (classification, hand proof both directions), Theorem 2, Theorem 3, the exact geometry, the condition list |
| `cert/sector_words.json` | explicit pair-only witnesses for `m = 5,6,9,12,15,18` |
| `run_all.sh`, `run_all.log` | the reproduction script and its output |
| `work/word.py` | letters `A..F`, the uniform word `A^2 B^2 D^(m-3) E^2 F^(m-3)`, offsets |
| `work/domain.py` | the admissible-palette domain and the disjointness graph `H = C_5 + pendant` |
| `work/check1.py` | direct bitmask check of the uniform word, `m = 5..200` |
| `work/make_cert.py`, `work/verify_cert.py` | write / verify the certificate along two independent paths, and check the full condition list incl. (P5), m2, m11 |
| `work/generic.py` | the CSP; `decide_dfs` (exhaustive backtracking with arc consistency and symmetry breaking) and `decide_sat` (CaDiCaL) |
| `work/classify.py` | the classification table, three independent determinations per `m` |
| `work/verify_geom.py` | GEOM: exact-rational chain `1.5938 d_0 < Delta`, plus a numeric sampling of the true geometry |
| `work/minobs.py` | the `m = 4` obstruction: the induced 8-vertex Wagner subgraph `C_8(3,4)` |
| `work/contrast.py` | `k = 5` (never satisfiable) and `k = 7` (3-block word) |
| `work/prop.py`, `work/dfs.py`, `work/sub.py`, `work/solve.py`, `work/csp.py`, `work/sector_word.py` | exploratory scripts kept for audit (arc consistency alone refutes `m = 2,3`; `sub.py` shows which subsets of the offsets already force UNSAT) |

## The two decisive statements

1. A free-label translation-invariant **sector word** for the six-cycle at `k = 6` exists **iff
   `m >= 5`** (palettes = admissible pairs and/or triples avoiding the free label). So the
   `m = 6,9,12,15,18` SAT results are confirmed and the family is settled for every `m`.
2. **No centre-independent palette field is the maximal palette field of any weak measurable
   colouring**, proper or not: the paper's Lemma 5.2(3) applied to `(x+a) + f = x + f + a` at unit
   `|a|` gives `P_{x+t}(f) ∩ P_x(f) = ∅`, which a centre-independent field cannot satisfy. The
   free-label models therefore refute the palette-level route and nothing at the colouring level;
   properness is not the discriminating hypothesis.

## Conventions

`sprint/k6/` and everything outside this directory is read-only and unmodified. `pdftotext -layout`
for the paper, `pdftohtml -xml` as the independent extraction, and the repository's Lean
`PaletteTransport.lean` as the machine-checked statement of the two displays used (see the end of
`REPORT.md`).
