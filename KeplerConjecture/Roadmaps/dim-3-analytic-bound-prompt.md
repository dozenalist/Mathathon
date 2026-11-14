# Prompt: an upper bound in dimension 3 in the spirit of Viazovska

Written to be handed to a strong LLM with a computer (Python, an SDP solver, Lean).
The mathematical situation in three dimensions is not the same as in eight: the exact
answer is *known* (Kepler, Hales), so "a nicer bound" cannot mean a smaller constant than
$\pi/\sqrt{18}$. What it can mean — and what the prompt below asks for — is a bound
**below the best known non-Kepler bound** $0.754697\ldots$ (which comes from the
dodecahedral conjecture, not from Fourier analysis), or a much shorter proof of a
comparable bound.

Current frontier for packings of unit balls in $\mathbb R^3$:

| density $\delta$ | source | method |
|---|---|---|
| $0.740480489693\ldots = \pi/\sqrt{18}$ | Hales 2005 (+ Flyspeck) | exact; 300-page computer-assisted proof |
| $0.754697399\ldots$ | Hales–McLaughlin 2010 | Voronoi cell $\ge$ dodecahedron of inradius 1 |
| $0.770270440\ldots$ | Cohn–de Laat–Salmon 2022 | three-point / SDP, truncation radius $1.886835$ |
| $0.773055\ldots$ | Muder 1998 | Voronoi cell $\ge 5.41848$, cone decomposition |
| $0.779746762\ldots$ | Cohn–Elkies 2003 | two-point (linear programming) bound |

The Voronoi-based rows and the Fourier-based rows are from different communities and are
never compared against each other. The Fourier-analytic family is stuck at $0.7797$
(two-point, marginally *worse* than Rogers' 1958 simplex bound) and $0.7703$ (three-point),
both far above the dodecahedral bound of $0.7547$. That gap is the opportunity.

---

## The prompt

You are a research mathematician with a computer. Your task is to prove a new upper
bound on the density of sphere packings in three dimensions, in the style of the
Cohn–Elkies linear-programming bound and Viazovska's dimension-8 proof: an explicit
certificate plus a finite, checkable computation. A **hybrid** argument — an analytic
certificate combined with a local (Voronoi/Delaunay) geometric input — is acceptable and
is probably necessary. Work to the standard set out in §8: no step may rest on a
numerical computation you have not certified.

### 1. Conventions (fix these before writing anything)

A packing is a set $\Lambda \subset \mathbb R^3$ with $|x-y| \ge 2$ for distinct
$x,y \in \Lambda$; the balls have radius $1$. Density:
$$\delta(\Lambda) = \limsup_{R\to\infty} \frac{\operatorname{vol}\big(B(0,R)\cap \bigcup_{\lambda\in\Lambda} B(\lambda,1)\big)}{\operatorname{vol} B(0,R)}.$$
Write $B_1 = B(0,1)$, so $\operatorname{vol} B_1 = 4\pi/3$, and let
$c(\Lambda) = \delta(\Lambda)\cdot 3/(4\pi)$ be the centre density. Fourier transform:
$\hat f(t) = \int_{\mathbb R^3} f(x)e^{-2\pi i t\cdot x}\,dx$. Every inequality you write
must say which of $\delta$ and $c$ it is about. Most published tables quote centre
density; the table in §3 quotes both.

### 2. The theorem to prove

> **Target.** Every packing of unit balls in $\mathbb R^3$ satisfies
> $\delta(\Lambda) \le D$ for an explicit real number $D$, with a proof and a certificate
> that a referee can check by running one script.

The value of $D$ you obtain decides whether the result is new; §4 says how. Do not weaken
the target to lattices: the lattice case was settled by Voronoi in 1908
(every lattice packing has density $\le \pi/\sqrt{18}$, with equality only for fcc), so a
lattice-only bound is worthless here. The whole difficulty is non-lattice packings.

### 3. Benchmarks (both normalisations, so there is no ambiguity)

| $\delta$ | $c = 3\delta/4\pi$ | what it is |
|---|---|---|
| $0.740480489693$ | $0.176776695$ | $\pi/\sqrt{18}$; Hales; the truth |
| $0.754697399337$ | $0.180170732$ | Hales–McLaughlin, dodecahedral conjecture |
| $0.770270440$ | $0.183888522$ | Cohn–de Laat–Salmon, three-point bound |
| $0.773055$ | $0.184553$ | Muder, Voronoi cells $\ge 5.41848$ |
| $0.779746762$ | $0.186150827$ | Cohn–Elkies, two-point bound |
| $0.779636$ | $0.186124$ | Rogers 1958, simplex bound |

Note the order: in dimension 3 the two-point bound is *worse* than Rogers' 1958 bound,
and the best Fourier bound is worse than the dodecahedral bound. Also note
$c \le f(0)/\hat f(0)$ in the normalisation of §5.1, so the column $c$ is exactly the
quantity an analytic certificate controls.

### 4. What counts as success

Report the strongest tier you reached, with the exact constant.

- **Tier 0 — calibration.** An explicit admissible $f$ (see §5.1) with
  $f(0)/\hat f(0) \le 0.186150827$, i.e. $\delta \le 0.779746762$, certified and
  reproducible. This only reproduces the literature value; it is the sanity check that your
  pipeline works, not a result.
- **Tier 1.** $f(0)/\hat f(0) < 0.186150827$: a genuine improvement in the two-point class.
  State by how much.
- **Tier 2.** $\delta \le 0.770270440$ (beat the best published three-point bound), or the
  same constant from a strictly simpler certificate (e.g. two-point only, or no
  floating-point optimisation anywhere).
- **Tier 2b — the "nicer proof" reading.** A short, self-contained, fully verifiable proof
  of $\delta \le 0.754697$ that replaces the Hales–McLaughlin computation. A cheaper proof
  of the same constant is a real result.
- **Tier 3 — the prize.** $\delta \le D$ with $D < 0.754697399337$: the first analytic or
  hybrid bound in dimension 3 to beat the dodecahedral bound.
- **Tier 4 — out of scope.** $D = \pi/\sqrt{18}$. That is Kepler's conjecture. Claim it
  only if you have a genuinely new mechanism *and* a complete machine-checkable proof; a
  sketch here is worse than useless.

Intermediate quantitative goals are welcome, e.g. "this hybrid gives
$\delta \le 0.7620$ if the local inequality (L2) below holds for all cell shapes, and
$0.7547$ is the barrier for that whole family".

### 5. Machinery you may use, stated precisely

#### 5.1 The two-point (Cohn–Elkies) bound

**Theorem.** Let $f:\mathbb R^3\to\mathbb R$ be continuous and $L^1$ with
$\hat f \ge 0$ everywhere and $f(x) \le 0$ for $|x| \ge 2$. Then every packing satisfies
$$\delta(\Lambda) \le \operatorname{vol}(B_1)\,\frac{f(0)}{\hat f(0)} = \frac{4\pi}{3}\cdot\frac{f(0)}{\hat f(0)},\qquad c(\Lambda)\le \frac{f(0)}{\hat f(0)}.$$

In the lattice case the proof is two lines of Poisson summation: for a lattice $\Lambda$
of covolume $V$, $\sum_{\lambda\in\Lambda}f(\lambda) = V^{-1}\sum_{\mu\in\Lambda^*}\hat f(\mu)
\ge \hat f(0)/V$, while the left side is $f(0)+\sum_{\lambda\ne0}f(\lambda) \le f(0)$,
so $V \ge \hat f(0)/f(0)$ and $\delta = \operatorname{vol}(B_1)/V \le
\operatorname{vol}(B_1)f(0)/\hat f(0)$.

For periodic packings with several centres per cell the phases in Poisson summation do
**not** cancel, and for arbitrary packings there is no Poisson summation at all; that is
the content of Cohn–Elkies, *New upper bounds on sphere packings I*, Annals 157 (2003)
689–714, Theorem 3.1. Cite it with its exact hypotheses and either reproduce its argument
or state precisely which of its lemmas you are using. Do not wave at compactness, and do
not generalise the lattice computation above by hand — it is not valid as written for
$k>1$.

#### 5.2 A function class in which $\hat f \ge 0$ is exact

Use radial Gaussians times Laguerre polynomials:
$$\varphi_k(x) = e^{-\pi|x|^2}L_k^{1/2}\big(2\pi|x|^2\big),\qquad
\widehat{\varphi_k} = (-1)^k\varphi_k .$$
(This is the radial $d=3$ Hermite eigenbasis; verified numerically to $10^{-20}$ before
writing this note.) Hence for $f = \sum_{k=0}^{n} a_k\varphi_k$ one has
$\hat f = \sum_k (-1)^k a_k\varphi_k$, and with $t = 2\pi r^2$,
$P(t) = \sum a_kL_k^{1/2}(t)$, $Q(t) = \sum(-1)^ka_kL_k^{1/2}(t)$:

- $f \le 0$ on $|x|\ge2$ $\iff$ $-P \ge 0$ on $[4,\infty)$ $\iff$ $-P = s_0(t) + (t-4)s_1(t)$ with $s_0,s_1$ sums of squares of univariate polynomials (Markov–Lukács);
- $\hat f\ge0$ $\iff$ $Q \ge 0$ on $[0,\infty)$ $\iff$ $Q = u_0(t) + t\,u_1(t)$, $u_0,u_1$ SOS.

So the LP bound becomes a *univariate* semidefinite programme in the coefficients $a_k$
and the SOS multipliers. Solve it to high precision, round the coefficients outward,
re-evaluate, and you have a certificate that is a finite algebraic object — not a solver
log. This is the recommended route to Tier 0/1; do not trust a bound obtained from a
floating-point SDP alone.

#### 5.3 The truncation identity (the hybrid interface)

If $f$ is Schwartz, $\hat f\ge0$, and $f\le 0$ on $2\le|x|\le R$ but possibly positive
beyond $R$, the same Poisson argument in the lattice case ($k=1$, covolume $V$) gives
$$V\,f(0) \ \ge\ \hat f(0) - I,\qquad I = \int_{|x|>R} f(x)\,dx,$$
hence
$$\delta(\Lambda) \le \frac{4\pi}{3}\cdot\frac{f(0)}{\hat f(0)-I}\qquad (I<\hat f(0)).$$
This is the exact bookkeeping for "allow a positive tail and pay for it in the
denominator". Getting from here to arbitrary packings is the work: the step
$\sum_{|x|>R}f(x) \approx (\text{number density})\cdot I$ is a Riemann sum for a lattice
and a *theorem about pair correlations* for a general packing — say which one you are
using, and prove it or bound the error.

#### 5.4 Local density and the dodecahedral barrier

For a packing, let $\Omega(v)$ be the Voronoi cell of $v$.
- (L1) Muder 1998: $\operatorname{vol}\Omega(v) \ge 5.41848\ldots$ for every $v$, giving
  $\delta \le 4\pi/(3\cdot 5.41848\ldots) = 0.773055\ldots$ (cone decomposition,
  convexity, the worst case being 13 equal solid angles).
- (L2) Hales–McLaughlin 2010: $\operatorname{vol}\Omega(v) \ge 5.550291028515\ldots$, the
  regular dodecahedron of inradius 1, i.e. the icosahedral kissing configuration; giving
  $\delta \le 0.754697399337\ldots$.

Any argument that bounds *each* cell by a constant dies at (L2). The extremal
configuration — 12 neighbours at the vertices of a regular icosahedron — is rigid, and the
icosahedral cluster does not extend to a dense packing (it is the local motif of
quasicrystals, not of crystals). To go below $0.754697$ you must charge for that
incompatibility. That is exactly what Hales' scoring function does, and it is where a
"hybrid" bound can win.

#### 5.5 Coupling the two: score functions

The two-point inequality, averaged over centres, is a constraint on each ball's
neighbourhood. Positive-definiteness applied to the points of $\Lambda$ in a ball of
radius $R$ gives $0 \le N f(0)+\sum_{x\ne y}f(x-y)$, hence
$$\frac1N\sum_{x}\sum_{y\ne x}\big(-f(x-y)\big)\ \le\ f(0) + o(1)$$
(average over the $N$ centres, boundary error $O(R^2)/N \to 0$). A certificate is sharp
only if every pair distance of the extremal packing lies in the zero set $\{f=0\}$; in
general $f$ is a *cost function on local configurations*, saying how much "negative mass"
a neighbourhood may carry. Combine with a local bound of the form
$$\operatorname{vol}\Omega(v) \ge V_0 + \text{(penalty for non-icosahedral neighbours)},$$
and you have a feasible programme: cells that are too small must be near-icosahedral, near-
icosahedral clusters force large cells nearby, and $f$ bounds how many of each can coexist.
Formalise the averaging step before using it.

### 6. Candidate architectures

- **(A) Certified two-point bound.** §5.2, degree $n \approx 20$–$40$. Fast, rigorous,
  likely reaches Tier 0 and maybe Tier 1. Report the degree–constant curve.
- **(B) Truncated certificate with a certified tail.** §5.3 with the tail $I$ estimated from
  local geometry (kissing-number-type bounds on the number of pairs at each distance),
  not from a crude global density bound.
- **(C) Three-point / PSD with local structure.** The 2022 bound uses rotationally
  invariant test functions of $(|x|,|y|,|x-y|)$. Push the degree (their $d_3=9$ is far
  from converged) or restrict test functions to triples that are *locally realisable*.
  Cheapest known route to a number below $0.7703$.
- **(D) Score-function hybrid (Fejes Tóth / Hales in miniature).** Find
  $A$ on local configurations with $\operatorname{vol}\Omega(v) + A(v) \ge V_0$ and
  $\sum_v A(v) \ge 0$ provable from an analytic certificate. Then
  $\delta \le 4\pi/(3V_0)$. With $V_0 > 5.550291$ this is Tier 3.
- **(E) Defect accounting.** Prove: if $\operatorname{vol}\Omega(v) < 5.550291 + \varepsilon$
  then the 12 neighbours are $\varepsilon'$-close to icosahedral, and such a ball forces its
  neighbours' cells to have volume $\ge 5.550291 + c(\varepsilon)$ with $c>0$ linear; sum.
  This is the conceptual core of the Kepler proof; a quantitative version with explicit
  constants is a publishable bound even if it lands at $0.74$–$0.75$.

Say which architecture you chose and why, and report what each other one would have
needed.

### 7. Obstructions — do not rediscover these

- The two-point bound is sharp only in dimensions $1,2,8,24$. Whether its optimum in
  dimension 3 equals $\pi/\sqrt{18}$ is **open**; no sharp certificate is known, and
  Cohn–Elkies' truncation conjecture (that truncations approach the optimum) is unproved.
- There is no known dimension-3 analogue of the modular-forms mechanism: Viazovska's
  $\varphi$ is built from the $E_8$ theta series, which is a modular form, and no
  three-dimensional lattice supplies the corresponding arithmetic. Treat "find the
  three-dimensional modular form" as a dead end, not a research direction.
- A sharp certificate for fcc would have to vanish on the whole fcc distance set
  $(\sqrt2,\ 2,\ \sqrt6,\ 2\sqrt2,\ldots)$ and have $\hat f$ vanish on the dual lattice.
  No such function is known. If you find one you have solved a famous problem; check it ten
  times before claiming it.
- Rounding errors in an SDP optimum are not a proof. Neither is checking $\hat f\ge0$ on a
  grid.

### 8. Rigour protocol

1. Every constant: at least 9 significant digits, and a stated interval width.
2. Every sign condition ($\hat f \ge 0$, $f\le 0$ off the ball, a polynomial nonnegative on
   a half-line or in a polytope): certified by an algebraic identity (SOS with rational
   coefficients, or an interval-arithmetic subdivision with a stated mesh and a Lipschitz
   bound). Grid evaluation alone is not a certificate.
3. One script `verify.py` that takes the certificate file and re-derives the final constant,
   printing PASS/FAIL with intervals. Run it from a clean directory. Its output goes in the
   report.
4. Separate what is *proved*, what is *computed*, and what is *assumed*. A numbered list of
   gaps is required even when the result is complete ("gap list: none").
5. If you use Lean 4 + Mathlib, the highest-value targets are the combinatorial parts
   (kissing/13-neighbour lemmas, the score-function inequality on a finite list of
   configurations), not the analysis. Say what you formalised.

### 9. Deliverables

1. **Theorem** with the exact constant and its interval.
2. **Certificate**: coefficients / matrices, in a machine-readable file, plus its size.
3. **Proof**: the argument, each step labelled with the inequality it uses and the
   normalisation.
4. **`verify.py`** and its output.
5. **Gap list** and **what would falsify the result**.
6. **Comparison table** putting your constant against all six rows of §3, with the
   difference stated in both $\delta$ and $c$.

### 10. Failure modes

- Reporting a numerical optimum as a theorem.
- Mixing normalisations (radius 1 vs $1/2$; min distance 2 vs 1; $\delta$ vs $c$). This is
  the single most common error in this literature.
- Proving the bound for lattices, or for saturated packings, and not saying so.
- Citing the dodecahedral bound as if it were the goal, or the Kepler bound as if it were a
  benchmark to beat.
- "By a standard limiting argument" where the argument is the actual content.
- Presenting a bound of, say, $0.7799$ as an improvement when it is worse than Rogers 1958.

---

## Notes for the reader of this file (do not paste into the prompt)

**Provenance of the table.** $\pi/\sqrt{18}$: Hales, *A proof of the Kepler conjecture*,
Annals of Math. 162 (2005); formal verification (Flyspeck) 2014–2017. The dodecahedral
bound: Hales–McLaughlin, *The dodecahedral conjecture*, J. Amer. Math. Soc. 23 (2010)
299–344, DOI 10.1090/S0894-0347-09-00647-X — the cell bound $5.5502910\ldots$ is the
regular dodecahedron of inradius 1, and Muder's 1998 paper says explicitly that proving the
conjecture "would reduce" the best bound to $0.7547$. Muder: *A new bound on the
local density of sphere packings*, Discrete Comput. Geom. 20 (1998),
DOI 10.1007/BF02573984. Cohn–Elkies: Annals 157 (2003) 689–714, Table 3 gives
$0.18616$ in centre density for dimension 3. Cohn–de Laat–Salmon: *Three-point bounds for
sphere packing*, arXiv:2206.15373, Table 1.1 ($n=3$: $R = 1.886835$, $d_2=24$, $d_3=9$,
bound $0.770271$) and Table 6.1 (the degree trend $0.773719,\ 0.772303,\ 0.770802,\
0.770270$ for $d_3 = 6,7,8,9$ — not yet converged). Rogers' 1958 value and the historical
list ($0.884$, $0.835$, $0.828$, $0.7797$, $0.77844$, $0.77836$, $0.7731$) are from
Hales, *An overview of the Kepler conjecture*, §1.4.1.

**What I checked myself.** $\operatorname{vol}\Omega_{\text{dodeca}}(r=1) =
5.550291028515510\ldots$ and $4\pi/3$ over it $= 0.754697399337\ldots$; the identity
$\delta = \operatorname{vol}(B_1)f(0)/\hat f(0)$ against the sharp 8-dimensional case
($f(0)/\hat f(0) = 16$ gives $\pi^4/384$); the thresholds $c = 3\delta/4\pi$ in the table;
Rogers' simplex bound in $d=3$ ($4$ caps over a regular tetrahedron of edge 2
$= 0.7796356$, i.e. below the 2003 LP bound $0.7797468$); and the Laguerre eigenfunction
relation in §5.2 by numerical radial Fourier transforms to $10^{-20}$.

**Judgement calls.** (i) The prompt treats $0.754697$ as the record to beat, because it
is: the Fourier family is at $0.7703$ and nobody in that community compares against the
dodecahedral bound. If you would rather aim at the weaker, purely-analytic record, delete
Tier 3 and the §5.4/§5.5 material and the prompt becomes much easier — and much less
interesting. (ii) Tier 2b is included because "nicer" in your two chats meant *both* a
better constant and a better proof; a short proof of $0.7547$ is a legitimate reading.
(iii) The function class in §5.2 is a suggestion, not a constraint: its virtue is that
$\hat f\ge0$ becomes an exact SOS condition, which is what makes a certified LP bound a
finite object. (iv) **One claim here is mine, not a quotation**: that $0.7547$ is *the*
best known non-Kepler bound. It follows in one line from a published theorem
(Hales–McLaughlin) plus the standard "cells partition space" argument, and Hales' overview
says the same ("the dodecahedral conjecture implies a bound of 0.755"), but no recent
survey headlines it — papers that say "best known bound $\approx 0.77$" mean the best bound
in the LP/SDP family. If you quote the $0.7547$ figure, quote it with the derivation, not
as a citation.
