# m7 — closing one black box of the lower-bound proof (§3.1 of the paper)

**Deliverable.** `fibre-selection.md`: a complete, self-contained proof of the one step the paper asserts in a
single sentence and everything downstream depends on — the **measurable fibre-orthonormal-basis selection** inside
the compact-tower lemma (paper §3.1). Every estimate is explicit ($1/4$, $3/4$, $1$, then
$\delta^{-1}\|L\|_\infty^2$, $d$, $\sqrt d$, $\varepsilon$), and the whole measurability layer of Lemma 3.1 is then
carried out with it, so no assertion of that lemma is left unchecked.

The black box, quoted from the paper:

> "Their fiber scalar products make rank and linear-independence tests measurable. Selecting the first available
> independent section at each step and applying fiberwise Gram–Schmidt gives measurable fiber-orthonormal sections
> $e_1,\dots,e_d$ spanning the range of $Q_y$."

What `fibre-selection.md` contains:

* §1 the standard formalism of a measurable field of Hilbert spaces, with the two axioms (F1)–(F2) and the closure
  lemmas (norm and inner product of measurable sections are measurable; measurable fields of operators act on
  measurable sections);
* §2 **Lemma S** (rank measurability + canonical first-fit selection of a fibre-orthonormal basis), proved in four
  steps: measurability of the selection index and of each section; the test succeeds whenever the range has room
  ($\|Q_y\zeta\|\ge 1-1/4$); the test fails exactly when the range is exhausted; exactly $d$ orthonormal vectors,
  hence a basis;
* §3 the application: the level $\delta$, the uniform rank bound $\delta^{-1}\|L\|_\infty^2$, constancy of the rank
  by ergodicity, the bound $\sum_i|e_i(x)|^2=d$ (hence $\|e_i\|_\infty\le\sqrt d$), strictness of the extension
  $Y'=Y\vee\sigma(e_1,\dots,e_d)$, and property (2.6) with an explicit basis and bound;
* §5 the two retractions below.

## Retractions (from my first report)

1. **Withdrawn:** "in Lemma 3.2, `averages of a(h)²` should read `averages of a(h)`." In (3.7) the paper defines
   $a(h)=\|PF_{j^*,h}\|_2$ — the **norm**. The pair criterion gives $\operatorname{Avg}a^2\to0$ and Cauchy–Schwarz
   gives $\operatorname{Avg}a\to0$, exactly as the paper says. Nothing to repair.
2. **Withdrawn:** "the proof of Lemma 3.3 identifies $\psi_{A-Bu^2}$ with $\psi_{-L+(A-B)u+Lu^2}$." The paper never
   does: it applies (3.2) with exponents $0,1,2$ to the **second side** $R_u=-L+(A-B)u+Lu^2$, bounds
   $\|g_{-L}U_ug_{A-B}U_{u^2}g_L\|\le\|g_{A-B}\|$ using $|g_{\pm L}|\le1$, and compares the two sides through the
   *modulus* identity (3.14) plus radiality of $m$ ("equal moduli give equal m-values"). No gap.

Both retractions are recorded in `analytic-core.md` §4.0, with the corrected readings in Remarks 3.2.6 and 3.3.7.

## Supporting material

* `analytic-core.md` — an independent verification of §2–§4 (Theorems 2.3 and 1.3, Lemmas 2.4–2.7, 3.1–3.5, 4.1, 4.3,
  Prop. 4.2), with the classical inputs listed exactly. Its verdict: §2–§4 is sound; no step needs repair.
  It also contains two sharpenings (Borel weak colouring; $\chi_m(\mathbb R^2)\ge6$) and one new lemma (every
  algebraic $z$ with $|z|\le2$ is a sum of two algebraic units, so $\langle K\rangle=E$ and the only
  $K$-invariant closed subgroups of $D$ are $\{0\}$ and $D$).
* `work/moser_certificate.py` — exact rational interval certificate for the paper's **last** step (§8.5–8.6): the
  seven-vertex graph of (8.5) has all eleven edges of length exactly 1 and is not 3-colourable; the placement (8.6)
  is a congruence; all seven placed vertices satisfy $0<|z|^2<4$ and $P<P'$ in (8.4) strictly.
* `work/check_algebra.py`, `work/paper_identities.py`, `work/finite_words.py` — exact/symbolic checks of the
  algebraic identity (3.14), of the §8.5 trigonometric identities, of the §5.3 expansions, and of the §8.2/§8.3
  finite combinatorics.

## Check commands

```
cd .ultramath/smwfcr56i/m7
python3 work/moser_certificate.py      # exact certificate for section 8.5-8.6
python3 work/check_algebra.py          # (3.14) moduli, unit-sum lemma, hexagonal 7-colouring constants
python3 work/paper_identities.py       # section 8.5 trig identities; Lemma 5.3 expansions (about 8 s)
python3 work/finite_words.py           # section 8.2 five-cycle and 8.3 four-cycle finite combinatorics
```

`work/paper.txt` is `pdftotext -layout` of the paper, used only for reading.
