# Handoff answer: the six-cycle free-label case at k = 6 is decided

**Bottom line.** The pair-only claim in the handoff is **correct and sharpened**: a
translation-invariant free-label sector word for the six-cycle exists for **every `m >= 5`** and for
**no `m <= 4`** (with or without ternary palettes). So the palette-level route is dead at full
resolution, not just at `m = 6`. But the same analysis shows the models are *not* colouring-level
counterexamples for a reason that is stronger and more useful than "the free label is fixed":
any centre-independent palette field violates a palette-level constraint the paper already proves
for every colouring, at unit centre distance. Both facts are proved below and machine-checked;
the exact frontier is restated at the end.

Files: [proof.md](proof.md) (the mathematics), `run_all.sh` (reproduces every number),
`cert/sector_words.json` (the witnesses), `work/` (the checkers).

---

## 1. Task 1 — extraction and verification of the pair-only solutions

The handoff's SAT claim is confirmed, with two independent complete decision procedures and a
uniform construction that supersedes the `m = 6,9,12,15,18` sample.

**Explicit family.** With `A={1,3}, B={1,4}, C={1,5}, D={2,4}, E={2,5}, F={3,5}` (the admissible
pairs avoiding label `0`), let

    u_m = A A B B D^(m-3) E E F^(m-3)        (length 2m, defined for m >= 5)

and `sigma_m` = `u_m` repeated three times (length `6m`). Then `sigma_m(i) cap sigma_m(i+o) = empty`
for every sector `i` and every transport offset `o in {+-(m-1), +-m, +-(m+1)} mod 6m`.
`m = 6` gives `AABBDDDEEFFFAABBDDDEEFFFAABBDDDEEFFF` (36 sectors); `m = 5` gives
`AABBDDEEFF` repeated (30 sectors, the smallest model).

**Why it works** (uniform in `m >= 5`, not a case check): `2m | 6m`, and modulo `2m` the six
offsets collapse to `{m-1,m,m+1}`, so only `u_m(i) cap u_m(i+m+delta) = empty`, `delta in {-1,0,1}`,
matters. The position ranges `{0,1}=A, {2,3}=B, [4,m]=D, {m+1,m+2}=E, [m+3,2m-1]=F` map the three
partners of each `i` into the letter pairs `{A,D},{A,E},{B,E},{B,F},{A,B},{D,F}`, which are exactly
the edges of the disjointness graph on the six pairs. The disjointness graph is
`C_5` (`A-E-B-F-D-A`) plus the pendant `C-D`; five of its six vertices are used.

**Checks.** `work/check1.py` (direct bitmask check, `m = 5..200`); `work/make_cert.py` +
`work/verify_cert.py` (certificate read back and checked along two independent paths, `m = 5,6,9,12,
15,18`); `work/generic.py` (exhaustive DFS and CaDiCaL, decide the CSP rather than check a word).
`work/verify_geom.py` proves the geometric reduction in exact rational arithmetic and then samples
the actual geometry.

**The geometric lemma, exact.** `Delta = 2pi/(6m)`, `d_0 = pi/(9m) = Delta/3`. For unit `f`, `|a| <= d_0`,
the two exact unit decompositions `s_+-` of `f + a` satisfy
`|arg s_+- - (arg f +- pi/3)| <= arcsin|a| + |a|/sqrt(4-(1+|a|)^2) <= 1.5938 |a|`.
The script proves the coefficient bound in `Fraction` arithmetic from `pi < 355/113`,
`arcsin d <= d(1+d^2/6+d^4/4)` and `1/sqrt(4-(1+d)^2) <= 0.5918` (tightest margin 0.001182 at
`m = 5`), and `1.5938/9 < 1/3` exactly. Hence the deviation is at most `0.53 Delta`, the sector index
of `s_+-` lies in `{i+-m-1, i+-m, i+-m+1}`, and (5.3) follows from disjointness at the six offsets.
The numeric sampling finds max deviation ratio `1.169` (bound `1.5938`) and realised displacements
exactly `{+-(m-1), +-m, +-(m+1)}` — so the reduction has no sign or indexing error.

The accumulating-centre argument is unchanged and uses no new input: the field is translation
invariant with every value admissible, so every point of the plane is a six-cycle point in the
(6.2) sense, and `y_k = (d_0/3) 2^{-k} (3/5,4/5)` accumulate at `0`.

## 2. Task 3 — the general translation-invariant question, decided

**Theorem 1.** For `m >= 2` let `V` be any set of palettes that are admissible for `C_6` and avoid
the fixed label `0` (the six pairs, or those plus the ten triples of `{1,...,5}`, or all of them).
There is `sigma : Z_{6m} -> V` with `sigma(i) cap sigma(i+o) = empty` for all six transport offsets
**iff `m >= 5`.**

*`m >= 5`*: the word above. *`m = 2,3`*: sectors `0,1,2` (resp. `0,2,4`) are pairwise at offsets
inside the offset set, so three palettes would have to be pairwise disjoint — three disjoint subsets
of `{1,...,5}` of size `>= 2` do not exist. *`m = 4`*: the eight sectors `{16,...,23}` induce the
cubic circulant `C_8(3,4)` (Wagner graph), which is uncolourable: the disjointness graph retracts
onto its 5-cycle (`C |-> A`), so a word would give `psi : Z_8 -> Z_5` with `psi(i+3)-psi(i)` and
`psi(i+4)-psi(i)` in `{+-1}`; summing four 3-steps gives
`alpha_i + alpha_{i+1} + alpha_{i+3} + alpha_{i+6} = beta_i`, forcing all `alpha_i = alpha` and
`beta_i = -alpha`, whence `0 = psi(i+8)-psi(i) = -2 alpha != 0`. *`m = 1`*: offset `0` is realisable
(`1.5938 d_0 = 0.53 Delta` can pull the image back into the sector of `f`), so a palette must be
disjoint from itself; even the reduced set `{+-1,+-2}` is unsatisfiable (octahedron).

So the `m = 6` model is not special: there is a free-label model at **every** resolution `m >= 5`,
and the smallest is `m = 5` (30 sectors). `m <= 4` is impossible for the sector class, so the
`d_0 = pi/(9m)` refinement in the record is not where the freedom lies.

Machine cross-check: `work/classify.py` decides `m = 2..15` by exhaustive DFS *and* CaDiCaL (and by
the explicit word) for the pair domain, and `m = 2..10` for the pairs+triples domain — identical
verdicts in both;
`work/minobs.py` extracts the 8-vertex uncolourable certificate for `m = 4`.

## 3. Task 2 — every necessary condition of the paper, checked

Verified for the model at `m = 5,6,9,12,15,18` (`work/verify_cert.py`):

| condition | status |
|---|---|
| (P1) `1 <= |P| <= 3` | all palettes are pairs |
| (6.2) `P` not contained in a cycle edge | yes, all five values are admissible |
| (5.7) `P(e) cap P(Re) = empty` | yes (offset `m`, checked separately) |
| (5.3) exact transport at `|z-z'| <= d_0` | yes (six offsets; geometry proved exactly) |
| non-proper self-avoidance | label `0` in no palette; labels `1..5` all occur |
| m2 two-centre bound `|P_x|+|P_y| <= 5` | `2+2 = 4 <= 5` (translation invariance) |
| m11 ternary density `sigma{T subset P} <= 1/2` | no triples; max over `T` is `0.400` (`m=5`), `0.4167` (`m=6`) |
| (P5) edge trace killing both edge labels | implied by admissibility for pairs: some member of `P` is outside `{i,i+1}`, and the trace `delta_a` on it is supported in `P` — checked for every value and all six edges |
| (P6) no complementary triple pair | vacuous |
| (C1) disjoint `120^deg` palettes with total size 5 | vacuous (total size 4) |
| m1 single-centre classification | consistent: only `K_6` is excluded, `C_6` is realised |
| m14 neutrality | satisfied (the system is pair-valued, which is the neutral stratum) |
| m4 label-merging filter | a colouring-level filter; no constraint on a palette field |

So the model passes every necessary palette condition in the record, including the two-centre bound
that killed the earlier ternary witness. **No condition is failed.**

## 4. Task 4 — what a proper 6-colouring must do, and why "vary the free label" is the wrong target

Two theorems, both about *any* weak measurable colouring (proper or not). Neither is properness.

**Theorem 2 (centre-independence is impossible).** Lemma 5.2(3) carries no distance restriction,
and the paper records the instance `(x+a) + f = x + f + a` (`s(f)=f`, `t(f)=a`), which is admissible
off `f = +-a`. So for a colouring's maximal palette field: for every **unit** `t` and a.e. `f`,

    P_{x+t}(f) cap P_x(f) = empty.

A field with `P_z = sigma` for all `z` therefore needs `sigma(f) cap sigma(f) = empty`, i.e.
`sigma(f) = empty`: **no centre-independent palette field is the maximal palette field of any weak
measurable colouring, proper or improper.** Every free-label sector model is of this form; the
models satisfy the `d_0`-restricted instances of (5.3) only because those always move the direction
by approximately `pi/3`, and the same-direction instance at unit centre distance can never be added.

This corrects the record's frontier sentence "the models fail only trace-consistency with a *proper*
colouring": they fail a palette-level constraint that holds for every colouring. Properness is not
the discriminating hypothesis.

**Theorem 3 (support rigidity).** For every centre `x` and a.e. direction `e`,
`c(x+e) in P_x(e)` (the limiting trace at `x` built from radius exactly one sees the colours on the
circle `x + S`). Hence if `P` is centre-independent on the unit circle around `y`, then
`c(y) in intersection` of the values; so any field taking two disjoint values, or all six values of
Theorem 1, is induced by no colouring — again including the improper constant ones. (This is what
kills the constant-colouring reading of (5.2): a field with empty total intersection cannot be the
maximal palette field of `c = const`.)

**Answer to "can the free label vary with the centre?"** It can in principle, but it is not the
point and would not produce a counterexample: by Theorems 2 and 3 an induced field must satisfy
`P_{x+t}(f) cap P_x(f) = empty` at unit distance and be supported by the colouring, which no
sector-by-sector design achieves, and satisfying them together with (5.7)+(5.3) is exactly the
original six-colouring problem. The sharpest true statement is therefore: *what the models cannot do
is change with the centre in a way that is consistent with a colouring's own colours*; the free label
being locally constant is a consequence of centre-independence, not the obstruction.

## 5. Task 5 — vacuity and non-vacuity

**k = 5.** The analogous system (`ell = 5`, palette bound `|P| <= 2`, free label `0`) has admissible
values `{1,3},{1,4},{2,4}` with the single disjointness edge `{1,3}--{2,4}`, so a word must
2-colour the transport graph. That graph is connected (`gcd(m-1,m,m+1)=1`) and circulant, hence
bipartite iff all offsets are odd — impossible for three consecutive offsets `m-1,m,m+1`. So at
`k = 5` the free-label system is **unsatisfiable for every `m >= 2`** (`work/contrast.py`, both
procedures and an explicit bipartiteness test for `m = 2..30`). The free-label phenomenon is a
`k >= 6` effect, and the paper's `k = 5` local-finiteness theorem is untouched.

**k = 7.** Three pairwise disjoint admissible palettes leave `k-3 = 4` free labels, so the `m15`
3-block word (`M_0={1,3}, M_1={2,4}, M_2={5,6}`, `L = 2m/3`) is a free-label model at `k = 7`
(checked at `m = 6`). Non-vacuous: `m3` has a genuine proper measurable 7-colouring with a
non-locally-finite cyclic locus, so models at `k = 7` are expected, and the `k = 6` obstruction
(three disjoint admissible pairs must cover all six labels) is genuinely six-colour specific.

## 6. What must now be said about the frontier

Unchanged: `chi(R^2)` is 6 or 7; `(W)` is open; no finite palette system decides `k = 6`.

Sharpened by this run:

1. The free-label sector family is **decided**: it exists exactly for `m >= 5`, at every such `m`,
   with all palette-level necessary conditions of the paper satisfied. So no argument from those
   conditions plus non-proper self-avoidance can ever exclude `ell = 6`, and `m = 6` was not a lucky
   case (the smallest model is `m = 5`).
2. The family is **provably not colouring-realizable**, and the operative reason is a palette-level
   constraint of the paper that every colouring satisfies (Theorem 2), not properness. The record's
   frontier sentence should be amended accordingly.
3. `k = 5` admits no such model at any `m`; `k >= 7` admits the trivial 3-block model. `k = 6` is
   the unique case in which the free-label question is non-trivial *and* decidable, and it is now
   decided in both directions.
4. The radius `d_0 = pi/(9m)` in the record is not optimal: the sector machinery works for every
   `rho` with `arcsin rho + rho/sqrt(4-(1+rho)^2) < Delta` (up to `1.865 d_0` at `m = 5`, `1.888 d_0`
   asymptotically), and no `rho >= 1` can work (Theorem 2). The models therefore satisfy (5.3) on a
   *non-optimal but positive-radius* neighbourhood of every centre, and that is the exact sense in
   which they are countermodels.

## 7. Reproduce

    cd .ultramath/smwfwznwk/m1 && ./run_all.sh        # everything, ~30 s, prints "ALL CHECKS PASSED"

Individual pieces: `python3 work/verify_cert.py` (certificate, two paths),
`python3 work/verify_geom.py` (exact + numeric geometry), `python3 work/classify.py 2 3 4 5 6 7 8`
(three independent determinations of Theorem 1), `python3 work/minobs.py` (the `m = 4` certificate),
`python3 work/contrast.py` (`k = 5` no-go, `k = 7` model), `python3 work/check1.py` (the uniform
word for `m = 5..200`).

Nothing outside `.ultramath/smwfwznwk/m1/` was modified.

**How the paper's formulae were checked.** The paper was read with `pdftotext -layout`. The four
displays this work depends on are Lemma 5.2(3) with (5.3), the sentence "the representation
`(x+a)+f = x+f+a` is admissible off `f = ±a`", Corollary 5.4 with (5.7), and Lemma 6.2 with (6.2).
No OCR engine is installed and I cannot view rasterised images, so instead of a visual check each
display was confirmed two other ways: (i) an independent extraction with `pdftohtml -xml`, which
yields positioned text runs from a different code path and reproduces the same symbols and the same
`z`/`x` role assignments (in particular "Let `z` be any fixed center, possibly `z = x`", with no
distance restriction); and (ii) the repository's own Lean formalisation
(`lean/OAI/Geometry/PlaneColoring/PaletteTransport.lean`): `palette_smooth_transport` has free
`{x z : ℂ}` (no distance hypothesis — this is the statement Theorem 2 uses) and
`palette_sixty_disjoint : ∀ᵐ f, Disjoint (palette x f) (palette x (f + sixty))` is (5.7). The pages
were also rendered with `pdftoppm` (no error) purely to confirm the PDF page geometry.
