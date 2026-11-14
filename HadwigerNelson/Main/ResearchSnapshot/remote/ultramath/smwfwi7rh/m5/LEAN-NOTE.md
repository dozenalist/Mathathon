# Machine-checking: scope statement for direction d2

**Short version: this direction claims no Lean artifact.**  `verify.py` (with `results.txt`) is
the executable certificate; `SHARP-HYPOTHESIS.md` carries the proofs.  This note says exactly why
a Lean file would add nothing here, so that the coordinator can judge the claim without
re-running an absent check.

## What the five statements rest on

| statement | mathematics it needs | machine-checkable? | what is done instead |
|---|---|---|---|
| **Thm 1** (content ⟹ Lemma 7.4) | the paper's §7.2 argument verbatim, plus the net-to-cover implication `|N_{δ/2}(L₀)| = o(δ) ⟹` covers with total radius `→ 0` | yes in principle, but it needs the paper's Lemmas 7.2/7.3 (disk averages, `L¹` convergence, threshold violation covers) formalised, which is a large analysis development and not part of this direction | human proof, structured as a line-by-line modification of the printed proof, with the substituted inequality displayed |
| **Prop 2** (printed Lemma 7.4 forces `|L₀| < ∞`) | `|L₀| ≤ |H_n|` for a finite family plus an injection | yes, and it is a two-line `Finset` counting argument; formalising it would be a `Fintype.card_le_of_injective` restatement, no content from the paper | stated and proved in one line |
| **Thm 3** (no hole-free annulus) | pick `y ∈ L ∩ B(x,ρ) ∖ {x}` (non-isolation), then `y ∉ B_n` once `rad B_n < |y−x|/3` | yes, and again purely elementary: `y ∈ B_n ⊆ B(x,d/3)` contradicts `|y−x| = d`.  A Lean file would contain `not_lt_of_ge` twice and no idea from the paper | proved in four lines |
| **Thm 3′** (Lemma 7.8 false on a punctured annulus) | the identity `f(z) = −i ⟺ |z−1| = 1` on the circle, the sign of `cos(φ/2)`, the two degrees `±1` | the *algebraic* half is Lean-trivial; the *topological* half (a compact set has a component meeting both circles or not — `g^{-1}(m)` is a specific arc, verified by the parameterisation) is not a Lean statement about the paper but about an explicit arc, and the script checks it symbolically (sympy, exact) and numerically (sampling, exact degree integral) | `verify.py` A1–A4′ |
| **Thm 4** (perfect `1`-dense zero-content locus) | elementary estimates on the tubular neighbourhood of a scaled Cantor set | the construction is an infinite union; the exact part is `|N_δ(εC)| ≤ 12 δ^{2−s} ε^s`, i.e. a covering-count estimate; the decay `δ^{1−s} → 0` is the whole point (`s < 1`) | `verify.py` C1–C4, including the exact rational computation of the thickened lengths at the scales `3^{-n}`, `n ≤ 11` |
| **Thm 5** (sharp cover) | sector diameters `= R`, multiplicity `≤ 2`, `diam A₀ ≤ R+2δ` | yes: it is a finite geometric inequality; Lean would need `Real.sin (π/6) = 1/2`-style facts about the chord of a `π/3` sector, i.e. a small trigonometry development | `verify.py` B1–B4: exact corner distances plus a `401×401` grid check of cover and multiplicity |

## Why this is the honest allocation of effort

The four claims that decide the direction are of three kinds:

1. two **modifications of a printed proof** (Thm 1, Prop 2), whose correctness is a matter of
   checking that nothing else in §7.2 uses the finiteness of `L₀`;
2. two **explicit objects** (Thm 3′: the map `g`, Thm 4: the set `L*`), whose properties are
   decidable by exact computation and whose statements are falsifiable — if the level set were not
   the arc I claim, `verify.py` A2 fails; if the cover had multiplicity three somewhere, B1 fails;
   if the content did not decay, C2/C3 fail;
3. one **combinatorial-geometric inequality** (Thm 5) with an exact certificate.

A Lean development of (1) would need the paper's §7 formalised (disk averages `p^ε`, `L¹`
convergence, Lemma 7.3's violation covers, merging of disks), which is exactly what `smwfo9zkl`'s
`m9` did *for the combinatorial core only* (`.ultramath/smwfo9zkl/m9/k6_s7_engine.lean`, the
"clique in a forest has at most two vertices" engine).  The statements added here sit *before* and
*after* that engine, not in it:

* Theorem 1 changes the hypothesis of the hole construction (no combinatorial content);
* Proposition 2 and Theorem 3 are counting/elementary-metric (no combinatorial content);
* Theorem 3′ and Theorem 4 are explicit objects (content = the objects, checked by script);
* Theorem 5 is the sharpness of the cover obstruction, and `m12`'s §5.3 already supplies the
  analogous multiplicity-3 sharpness by exact `Q(√3)` arithmetic rather than in Lean.

So the split in this direction is: **proofs in the note, objects and inequalities in `verify.py`**.
If the coordinator wants one statement from here in Lean, the cheapest useful one is Theorem 3's
`y ∉ B_n` bookkeeping together with Proposition 2's `|L₀| ≤ |H_n|`; both are restatements of
`Finset`/`Metric` lemmas and neither would test the paper.

## Reproducing

```
cd .ultramath/smwfwi7rh/m5
python3 verify.py      # 20 checks, exit 0, "ALL CHECKS PASSED"
diff <(python3 verify.py) results.txt   # identical
```

No Lean toolchain is invoked by this direction, so the pinned `4.34.1` environment is untouched.
