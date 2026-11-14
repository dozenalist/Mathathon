# Continuation run `smwfhd5sl`: what the board shows

Eight members, eight directions, eight submissions accepted. Target was L4. The headline is that
L4 is **closed in the strongest possible way for the full palette class** — the class is equivalent
to the problem — and **achieved for the weakened classes**.

## The eight accepted results

| # | direction | result |
|---|---|---|
| m7 | D1 | **Pointwise collapse** (Lean): a palette field with non-emptiness and pointwise transfer is a `k`-colouring. The pointwise class is not a relaxation of the problem. |
| m2 | D2 | **Sliver invariant**: `|O|,|I| = k - l + #{runs}`, palette-independent. At `k = 6`, `l = 3` gives `>= 3` labels for every sign word, so local rigidity is unavailable; `l = 5` never gives two-element slivers; `l = 6` gives disjoint pairs; `l = 4` only for non-generic rays. Also: at `k = 4` the architecture is **empty** (the cyclic-centre locus vanishes), so the §5–§8 method cannot even reproduce `chi >= 5`. |
| m5 | D3 | **Exact decision of the interface CSP** for all `(k,l)` and all `6^l` ray geometries, two independent algorithms: UNSAT for `k <= 4` and `(5,5)`; SAT at `k = 6` for every length. Plus the **annulus counterexample**: `0.95 < |z| < 1.05` with `floor(9 arg z/2pi) mod 3` is 3-valued, nowhere locally constant, no monochromatic unit pair. |
| m3 | D4 | **Invariance/transport** of the six structural inputs; the exclusion list is not closed upward. **All-constants cover no-go**: multiplicity-3 covers of arbitrarily fine mesh exist, so Lemma 7.5 never applies at `k >= 6`. Two rigid instances of Lemma 5.2(3), one of them new: `P_x(e) ∩ P_{x+u}(e) = empty` for all unit `u`. |
| m4 | D5 | **Irreducibility**: each named input of §8 deleted in turn with an explicit model of the rest. **Proposition 8.2 is exactly the palette level at `(5,5)`**: 100 of 15625 walks survive free, 0 with the antipodal linkage. |
| m8 | D6 | **A.e. collapse**: the palette system with (H1) and the paper's own (5.3) is satisfiable at level `k` iff `chi <= k`. Hence `UNSAT` at `k = 6` iff `chi >= 7`. **The palette framework is the problem.** Also: all-ternary palettes impossible at `k = 6` (`chi_f >= 7/2 > 2`), so pair-forcing is necessary. |
| m1 | D7 | **Circle classification**: `chi(S_r) <= 3`, `= 3` iff `theta/2pi = p/q` with `q` odd, attained at `r = 1/sqrt3`. **Germ freedom**: no single-centre circle argument excludes a ternary palette. **Negative `k`-sensitivity**: the window invariant satisfies `I_5 = I_6` on all 128 windows while separating 4 from 5. |
| m6 | D8 | **Pair exclusion** (C1) and the **orbit bound** (C2): at most three ternary palettes per `pi/3`-orbit, so `sigma{|P| = 3} <= pi` and mean palette size `<= 5/2`, both attained. Lean-checked. |

## What this changes

1. **L4 is unattainable for the palette class** — not because the method is weak, but because it is
   complete: unsatisfiable at `k = 6` is `chi >= 7` and satisfiable is `chi = 6` (m8, m7).
2. **L4 is attained for the weakened six-step relaxation** (m5, m4, m2, m3), and the no-go is now
   all-constants (m3's Thm C).
3. **R5 is corrected**: the binding cardinality is `k - l` (the sliver), not `|P| <= k - 3` (m2,
   m7). Proposition 5.6 is not the unique locus.
4. **Positive constraints on any 6-colouring** now exist: pair-forcing is necessary (m8); 3-valued
   slivers need not be rigid (m5's annulus); `chi(B(x,1)) >= 4` (m1).
5. **The next computation** is to re-decide m5's CSP with m6's (C1)+(C2). Because every 6-colouring
   induces a model of that relaxation, unsatisfiability at every length and geometry would prove
   `chi >= 7`; satisfiability proves nothing.

## Corrections made during the run

* My brief's §2 branch "exhibit a palette system at `k = 6`" is void: it is L2, not L4 (m7).
* My synthesis's claim that "the a.e. class is the only place an L4 can live" is false (m8).
* My verdict claim that adding (C1)+(C2) "cannot bound `chi`" was wrong: UNSAT of the relaxation
  would prove `chi >= 7` (recorded in `L4-SYNTHESIS.md`).
* The paper's displayed (8.6) must be read with the bracket; confirmed independently three times.
