# Counterexamples / independent-audit registry

Role **X** for Mathathon problem 15. Branch `kepler15/counterexamples/run-01`, based on
source commit `69f3213aa6f2b636ec1b0e25a7394acfecae986b` (`origin/kepler15/setup-01a1d8c0`).
Every tracked change is under `KeplerConjecture/`.

**Frozen contract used throughout** (matches `Literature/PROBLEM_SPEC.md` and the
`ROADMAP.md` §2 interfaces): unit balls (radius 1), minimum separation 2,
$\widehat f(t)=\int_{\mathbb R^3}f(x)e^{-2\pi i\langle x,t\rangle}dx$, and the
Cohn–Elkies (CE) bound $\overline\delta(\Lambda)\le\frac{4\pi}{3}\frac{f(0)}{\widehat f(0)}$.

Artifacts in this directory:

| Path | What it is | Status |
| --- | --- | --- |
| `normalization_check.py` | 28 independent exact checks of every normalization in use | all pass |
| `ce_laguerre_exact.py` | exact (Sturm) sign certifier for the 3D radial Fourier eigenbasis | runs; basis verified |
| `ce_lp_search.py` | grid-LP search + exact certification loop | negative result, recorded |
| `evidence/normalization_check.out` | run log of the 28 checks | evidence |
| `evidence/hales-p34-def32-046.png` | page image of Hales p34 showing $\sqrt{32}$ (text layer drops the radical) | source evidence |
| `local-requests/LOCAL_COMPUTE_REQUESTS.md` | offload requests for Astra | X-R01 **superseded by X-R03** (REPORT_27616.md §H) |
| `NOTE_41644.md` | note for Main at the 00:08 checkpoint: C certifier sign loss (REFUTED), my constant repair, spatial-vs-centre average, E001 quantifier | delivered |
| `REPORT_27616.md` | independent review for supervisor review 27616 (C002/C003/C004/C005/C010b/C013/C014, E001–E004, E2/E3, Tammes-13) | delivered |
| `review_27616_checks.py` | audit computations for that review (15 checks) | runs, no failures |
| `ce_exact_gauss.py` | exact rational family `P(s)e^{-s}` + exact Fourier map + even-multiplicity sign test | supersedes the certifier in `ce_laguerre_exact.py` |
| `x_r01_driver.py` | runnable LP + cutting-plane + exact-certification driver | runs; deg-6 fixed-width LP infeasible |

---

## 1. Source audits

### X-SRC-01 — Hales, Definition 3.2 and Lemma 3.3 (unabridged 2005, printed p34 / PDF p46)

**Read directly from `Literature/Papers/Hales2005-unabridged.pdf`, and the page image was
inspected because the text layer is wrong on the one detail that matters.**

*The text-extraction trap.* `pdftotext -f 46 -l 47` renders the thresholds as `32`, and the
density as `π/√18`. The printed page reads $\sqrt{32}\le\operatorname{vol}(\Omega(v))+A(v)$ and
says the FCC Voronoi-cell volume is $\sqrt{32}$. This is confirmed in
`evidence/hales-p34-def32-046.png`. Since $\sqrt{32}=4\sqrt2=5.656854$ while the text's literal
`32` would be off by a factor $4\sqrt2$, and since
$$\frac{4\pi/3}{\sqrt{32}}=\frac{\pi}{3\sqrt2}=\frac{\pi}{\sqrt{18}},$$
only the radical-bearing reading is dimensionally consistent with the stated density
`normalization_check.py` §1 verifies both directions exactly. **Anyone who transcribes this
page from text extraction will get a threshold wrong by $5.66\times$.**

*The mechanism, verified.* Negligible means $\sum_{v\in\Lambda(x,r)}A(v)\le C_1r^2$ for all
$x$, $r\ge1$; fcc-compatible means $4\sqrt2\le\operatorname{vol}(\Omega(v))+A(v)$ for all $v$.
Lemma 3.3's chain is
$$\operatorname{vol}B(x,r,\Lambda)\overset{(3.1)}{\le}|\Lambda(x,r+1)|\tfrac{4\pi}{3},
\qquad
\sqrt{32}\,|\Lambda(x,r+1)|\overset{(3.2)}{\le} C_1(r+1)^2+\operatorname{vol}B(x,r+3),$$
using (i) saturation to get $\Omega(v)\subseteq B(v,2)$, so that
$\bigcup_{v\in\Lambda(x,r+1)}\Omega(v)\subseteq B(x,r+3)$, and (ii) fcc-compatibility to convert
a count of centres into a volume. Dividing,
$$\delta(x,r,\Lambda)\le\frac{\pi}{\sqrt{18}}\Bigl(1+\frac3r\Bigr)^3+\frac{C_1(r+1)^2}{r^3\sqrt{32}}.$$
*Audit verdict:* the argument is correct as printed, and it is **two-dimensional**: the whole
proof of an optimal three-dimensional bound is a counting argument in the plane. Both
$O(r^2)$ errors are what the final $\limsup_{r\to\infty}$ kills. **Nothing in the statement
requires $A\ge0$**: the correction may be negative where cells are large, which is essential
(see X-C003) and is the freedom a discharging construction must exploit.

### X-SRC-02 — Li, Theorem 6.1 (arXiv:2206.09876v3, §6, p11)

**Read directly from `Literature/Papers/Li2022-v3.pdf`.** Verbatim:

> **Theorem 6.1.** The 3-dimensional Cohn–Elkies linear programming bound is greater than
> 0.18398089.

with proof by a discrete dual feasible point, $m=53$, $r=89$, objective $m^{-d/2}\lambda_0$
truncated to eight decimals; exact rational data in the arXiv supplement. The paper's frame is
"$\delta_3=2^{-5/2}<0.17677670$" for Hales's center density.

*Three normalization points audited, all confirmed (see `normalization_check.py` §3):*

1. $0.18398089$ is in **CE center-density units**, i.e. $\delta=f(0)/\widehat f(0)$, related to
   occupied-volume density by $\Delta=\frac{4\pi}{3}\delta$. So Li's number corresponds to
   occupied volume $0.770657$.
2. It is a **lower bound on the CE optimum**, not an upper bound on density. The CE optimum is
   the *infimum* of $f(0)/\widehat f(0)$ over admissible $f$; a certificate with a *small* ratio
   gives a *good* (small) bound. Hence Li's theorem says: no admissible $f$ can push the bound
   below $0.18398089$. Equivalently the Kepler target $2^{-5/2}$ is unreachable **inside
   ordinary CE**. The number sits *below* CDS22's achieved value (0.779747 occupied
   $=0.186151$ center density) because those are on opposite sides of the true optimum:
   $$0.18398089<\text{(CE optimum)}\le 0.186151 .$$
3. $2^{-5/2}=1/(4\sqrt2)$ is exactly FCC's center density at separation 2 (covolume $4\sqrt2$),
   and $\frac{4\pi}{3}2^{-5/2}=\pi/\sqrt{18}$ exactly.

*Scope audited (this is the load-bearing limitation).* Li's program (Problem 5.1) is the
discrete reduction of a **single** auxiliary function, linear in one $f$, with positivity of
$\widehat f$ only. It says nothing about methods that add local geometric constraints, a second
function, or higher-point (3-point) positivity. **Claims that Li obstructs "all" Fourier or
"all" hybrid methods are unsupported and must not be repeated.** See X-C005.

---

## 2. Claim registry

Statuses follow `ROADMAP.md` §5. "PROVED" here means a written argument in this file that a
reviewer can check line by line; nothing in this section depends on an unverified computation.

### X-C001 — contact-shell Laplacian positivity (PROVED, replaces retracted Prop. 4.7)

> **Theorem.** Let $\Lambda\subset\mathbb R^d$ be a lattice with minimal nonzero norm $\rho$ and
> covolume $V$. Let $f$ be Schwartz with $f\le0$ on $\{\lVert x\rVert\ge\rho\}$,
> $\widehat f\ge0$, and suppose $f$ is **sharp**, i.e. $f(0)=\widehat f(0)/V$ (equality in CE).
> Then $\Delta f(\lambda)>0$ for at least one $\lambda\in\Lambda$ with
> $\lVert\lambda\rVert=\rho$; consequently $\operatorname{Hess}f(\lambda)\not\preceq0$ there.

*Proof.* Sharpness gives $f(\lambda)=0$ for all $\lambda\in\Lambda\setminus\{0\}$ and
$\widehat f(\mu)=0$ for all $\mu\in\Lambda^*\setminus\{0\}$: indeed
$$f(0)\;\ge\;\sum_{\lambda\in\Lambda}f(\lambda)\;=\;\frac1V\sum_{\mu\in\Lambda^*}\widehat f(\mu)\;\ge\;\frac{\widehat f(0)}{V}\;=\;f(0),$$
so every inequality is an equality and every non-positive (resp. non-negative) summand
vanishes. Now $\widehat{\Delta f}(t)=-4\pi^2\lVert t\rVert^2\widehat f(t)$, and $\Delta f$ is
Schwartz, so Poisson summation applies to it:
$$0\;=\;-4\pi^2\sum_{\mu\in\Lambda^*}\lVert\mu\rVert^2\widehat f(\mu)\;=\;\sum_{\lambda\in\Lambda}\Delta f(\lambda)
\;=\;\Delta f(0)+\sum_{\lambda\ne0}\Delta f(\lambda),$$
the first sum vanishing because $\widehat f=0$ off $0$ and the $\mu=0$ term carries
$\lVert\mu\rVert^2=0$. Also
$\Delta f(0)=-4\pi^2\int\lVert y\rVert^2\widehat f(y)\,dy<0$, since $\widehat f\ge0$ is
continuous and $\widehat f(0)>0$. For $\lambda\in\Lambda\setminus\{0\}$ with
$\lVert\lambda\rVert>\rho$, the point $\lambda$ is an *interior* point of the open set
$\{\lVert x\rVert>\rho\}$, on which $f\le0$ with $f(\lambda)=0$; so $\lambda$ is an interior
local maximum and $\Delta f(\lambda)\le0$. Hence
$$\sum_{\lVert\lambda\rVert=\rho}\Delta f(\lambda)=-\Delta f(0)-\sum_{\lVert\lambda\rVert>\rho}\Delta f(\lambda)\;\ge\;-\Delta f(0)\;>\;0,$$
so some contact vector has $\Delta f>0$. $\blacksquare$

*Why this matters.* The retracted Proposition 4.7 (recovered at
`.ultramath/smwfyzz1k/m3/zero-density-obstruction.md`, §0) inferred
$\operatorname{Hess}f(\lambda)\preceq0$ at every zero of a sharp certificate and concluded that
no sharp certificate can be $C^2$, hence none can be Schwartz. The inference is valid only for
$\lVert\lambda\rVert>\rho$. **X-C001 is the correct, quantitative repair**: the sign of the
Laplacian on the contact shell is not merely unconstrained, it is forced to be *positive
somewhere*. So a sharp certificate must be *non-convex* at some contact point — the opposite
of the retracted conclusion.

*Two independent confirmations.*

1. **Exact, hand-checkable, $d=1$.** $f=(1-|x|)_+$ is the sharp 1D certificate
   ($f(0)=\widehat f(0)=1$, $\Lambda=\mathbb Z$, $\rho=1$). Distributionally
   $$f''=-2\delta_0+\delta_{-1}+\delta_{1},$$
   so $\sum_{n\in\mathbb Z}f''(n)=-2+1+1=0$ (matching
   $-4\pi^2\sum_m m^2\widehat f(m)=0$), and $f''$ is *positive exactly at the two contact
   points* $\pm1$ and negative at the origin. This is X-C001's conclusion in closed form. It also
   shows the theorem must be stated distributionally when $f\notin C^2$.
2. **Viazovska's 8D function** is $C^\infty$ (Schwartz), sharp at the unimodular self-dual
   $\Lambda_8$, and satisfies the hypotheses with $\rho=\sqrt2$; X-C001 therefore *proves*
   $\Delta g(\lambda)>0$ for some minimal vector. This settles the Viazovska counterexample
   *without* any numerics — the earlier session's contour-integral evaluation of $g$
   (`.scratch/verify/gfun2.py`, values $g(\sqrt2)=0$, $g'(\sqrt2)=-\sqrt2/60$) is consistent
   but is not needed.

*Residual objection.* X-C001 does not by itself refute any *specific* proposed argument; it
refutes only those which require $\operatorname{Hess}\preceq0$ (or $\Delta\le0$) at a contact
point. Each such proposal must be checked against it individually.

### X-C002 — the 3D maximizer is not unique (PROVED; constrains every equality argument)

> **Proposition.** There are infinitely many distinct maximizers of the 3D packing problem.
> In particular HCP attains density $\pi/\sqrt{18}$, and HCP is not a lattice.

*Proof/verification.* `normalization_check.py` §2, exactly (sympy, in $\mathbb Q(\sqrt3)$):
the A layers are the triangular lattice of spacing 2, the B layers sit in the hollows at
in-plane offset $(1,\sqrt3/3)$ and height $c=2\sqrt6/3=\sqrt{8/3}$; then
$\lVert\text{offset}\rVert^2+c^2=4$ so the nearest A–B distance is exactly 2, the cell volume is
$2\sqrt3\cdot 2c=8\sqrt2$ with 2 points per cell, so the volume per point is $4\sqrt2$ — the FCC
value — and the density is exactly $\pi/\sqrt{18}$. HCP is not a lattice: with
$d=(1,\sqrt3/3,c)$ a B-layer vector, $2d=(2,2\sqrt3/3,2c)$ would have to lie in the A layer at
height $2c$, but $(2,2\sqrt3/3)\notin\langle(2,0),(1,\sqrt3)\rangle$ (it needs $n=2/3$).

*Consequences, which are binding on candidate proofs.*

1. No 3D proof may end with "hence the packing is FCC", and no equality-classification step may
   assume the contact graph or Voronoi cells of FCC. (Contrast $d=8,24$, where Cohn–Elkies §8
   *does* give uniqueness — that transfer fails in 3D.) Since Barlow stackings are an
   uncountable family with the same density, "the set of maximizers is a single orbit" is false.
2. A sharp 2-point certificate in 3D would have to vanish on the difference sets of *all*
   Barlow packings simultaneously — a much stronger requirement than the 8D one. Combined with
   X-SRC-02 (no sharp certificate exists at all), this shows the 8D mechanism cannot be
   transferred by "run the same proof".
3. Gauss's uniqueness theorem for *lattices* is untouched, because HCP is not a lattice. Any
   claim of the form "the densest lattice is unique, therefore ..." must state the lattice
   restriction explicitly.

### X-C003 — the icosahedral-cell obstruction to purely local cell-volume arguments (PROVED)

Let $v_0$ be the centre of a cluster of 13 balls: one at $v_0$ and 12 at distance exactly 2 in
the 12 icosahedral directions.

> **Proposition.** (i) $\Omega(v_0)$ is the regular dodecahedron of inradius 1, of volume
> $V_{\mathrm{dod}}=5.550291\ldots$; (ii) $V_{\mathrm{dod}}<4\sqrt2=5.656854$; (iii) every
> packing containing this cluster extends to a *saturated* packing (Zorn), so a saturated
> packing can contain a vertex with $\operatorname{vol}\Omega(v_0)=V_{\mathrm{dod}}$; hence
> (iv) $A\equiv0$ is **not** fcc-compatible, and every fcc-compatible $A$ satisfies
> $$A(v_0)\;\ge\;4\sqrt2-V_{\mathrm{dod}}\;=\;0.106563\ldots>0 .$$

*Verification.* `normalization_check.py` §4 computes both polytope volumes by exact plane-triple
enumeration plus convex-hull volume: the rhombic dodecahedron of inradius 1 gives
$5.656854249=4\sqrt2$ (matching Hales's $\sqrt{32}$ and the FCC covolume), the regular
dodecahedron of inradius 1 gives $5.550291$, and the 12 icosahedral neighbours are at distance
exactly 2 with nearest neighbour-neighbour distance $2.102924>2$, so the cluster is a genuine
packing.

*Consequences.*

1. **Dodecahedral ceiling.** Any bound of the form $\bar\delta\le(4\pi/3)/V_0$ obtained from a
   *universal* per-cell volume bound $V_0$ satisfies
   $$\frac{4\pi/3}{V_{\mathrm{dod}}}=0.754697\ldots>\frac{\pi}{\sqrt{18}}=0.740480\ldots$$
   and the bound is attained in the limit by the dodecahedral value. Since Hales–McLaughlin's
   theorem gives exactly $\operatorname{vol}\Omega\ge V_{\mathrm{dod}}$, **the best possible
   conclusion from cell volumes alone is $0.754697$, and no refinement of a cell-volume estimate
   can ever reach Kepler.** This is the precise obstruction to route R1 taken in isolation, and
   it is why Hales needs the additive correction $A$ rather than a bare volume bound.
2. **The defect set is sparse.** By negligibility,
   $\lvert\{v:\lVert v-x\rVert\le r,\ A(v)>0\}\rvert\le C_1r^2/0.106563=O(r^2)$, which is
   $o(r^3)$: any fcc-compatible correction with a uniformly positive lower bound on defect
   vertices is supported on a density-zero set. A discharging proof must therefore (a) be
   *negative* on the generic (near-FCC) vertices, compensating, and (b) keep the defect mass
   $O(r^2)$. This is a genuine constraint on the design of $A$, not a technicality.
3. **Realizability vs. extendability.** The 13-ball cluster is locally realizable at minimal
   separation 2 and locally as dense as the dodecahedron allows, yet it cannot be extended to a
   packing of density $0.7547$: the icosahedral symmetry is frustrated by the surrounding
   layers. So a locally optimal cell is not evidence of a globally dense packing — the cheap
   counterexample to any "improve each cell locally" strategy.

### X-C004 — audit of the recovered "zero-density / bandwidth" obstruction (ACCEPTED with corrected scope)

The recovered report `.ultramath/smwfyzz1k/m3/zero-density-obstruction.md` (revision 2) claims:
a certificate with $\operatorname{supp}\widehat f\subseteq B(0,R)$ vanishing at the first $K$
shell radii needs $R\ge(K\log2-\frac12\log(\lVert\widehat f\rVert_1/f(0)))/(2\pi r_K)$, hence no
band-limited and no compactly supported certificate is ever sharp in $d\ge2$.

*Audit.* The qualitative statement is the standard Jensen/exponential-type argument also used by
Cohn–Elkies §5 ("if $\widehat f$ is supported in $B(0,R)$ then $f$ has exponential type
$2\pi R$ and its zeros are at most linearly spaced"), and the shell spacings
$\sqrt{2(n+1)}-\sqrt{2n}\to0$ do make it incompatible with vanishing on every shell. **I accept
it, with the scope restriction that it constrains *band-limited* certificates only.** It has no
bearing on certificates of unbounded bandwidth, and hence no bearing on Viazovska-type
constructions or on any candidate in the class X-C006 considers. The report's own retraction
(§0) of the $C^2$ claim is correct and matches X-C001.

### X-C005 — "obstructs all higher-point methods": REFUTED as stated

No source in the project establishes an obstruction to higher-point methods, and the published
numbers contradict such a claim outright. From Cohn–de Laat–Salmon, Table 1.1 (occupied-volume
density, all general packings unless marked):

| Bound | Occupied volume | Center density $\Delta/(4\pi/3)$ | Gap to $\pi/\sqrt{18}$ |
| --- | --- | --- | --- |
| ordinary CE (2-point) | 0.779747 | 0.186151 | +0.039267 |
| strengthened 2-point | 0.773080 | 0.184559 | +0.032600 |
| general 3-point | 0.770271 | 0.183889 | +0.029791 |
| **lattice-only** 3-point | 0.741506 | 0.177022 | **+0.001026** |

(conversions recomputed in `normalization_check.py` §3). Three conclusions.

1. Higher-point bounds are **strictly stronger** than CE in 3D ($0.770271<0.779747$), so Li's
   theorem does not obstruct them. Any project statement to the effect that all higher-point
   methods fail is unsupported; the honest statement is that no published general bound of any
   order reaches Kepler.
2. The lattice-only value $0.741506$ is **not comparable** to the others: it bounds lattice
   packings only. It is the closest published value to the truth, and quoting it as a general
   3D bound would be a domain error. By X-C002 the general case genuinely is larger.
3. Li's lower bound ($0.18398089$) and CDS22's CE upper bound ($0.186151$) bracket the true CE
   optimum; the width $0.0022$ is a *certified* uncertainty in the CE value, not a gap to
   Kepler. The gap to Kepler is $\ge0.0072$ in center-density units and is not going away.

### X-C006 — the recovered smooth-certificate impossibility claim: REFUTED, origin preserved

*Original claim, preserved verbatim in substance* (from the revision-1 "Proposition 4.7"
recovered at `.ultramath/smwfyzz1k/m3/zero-density-obstruction.md` §0): a sharp certificate is
never $C^2$ with admissible Laplacian, hence never Schwartz; and the $d=8,24$ magic functions
have non-summable second-moment data.

*Status: REFUTED.* Two independent refutations, neither requiring the paper's numerics:

1. **Structural: X-C001.** At a contact point, positivity of $\Delta f$ is forced, so the
   claimed negative-semidefinite Hessian is impossible there; the retracted inference used
   two-sided information that the sign hypothesis does not supply on the boundary of
   $\{\lVert x\rVert\ge\rho\}$.
2. **External: Viazovska's $g$** is Schwartz, sharp, and satisfies every hypothesis, so the
   blanket "never Schwartz" statement is false. (The report's revision 2 already retracts it;
   this entry preserves the original claim, its diagnosis, and the repair, per `PRIOR_WORK.md`.)

*Auxiliary claim also refuted.* "The $d=8,24$ magic functions have non-summable second-moment
data" is false: those functions are Schwartz, so all moments are finite; what is true is that
$\Delta g$ takes a positive value somewhere on the contact shell (X-C001).

### X-C007 — negative result: grid-LP feasibility is not feasibility (recorded for C's interface)

`ce_lp_search.py` solves the linear program "minimise $f(0)$ subject to $f\le0$ on a grid of
$[4,\infty)$, $\widehat f\ge0$ on a grid of $[0,\infty)$, $\widehat f(0)=1$" inside the
Laguerre–Gaussian family, then attempts an **exact Sturm certificate** for the rounded rational
candidate. Outcome (`evidence/ce_lp_search.out`): for $K=2,\dots,5$ the LP reports objective
values *below* the Kepler center density ($0.468$, $0.468$, $0.287$), which is impossible by
Li's theorem; the exact certifier **rejects every one of them**, finding a sign violation
between grid points. Only the trivial $K=1$ point survived.

Two lessons, both directly useful to C and to Main.

1. **A grid-feasible LP point is not a certificate**, and the failure mode is silent: the
   objective looks like a breakthrough. Any candidate must be certified by an argument covering
   the *whole* sign domain. In the Laguerre–Gaussian family this is cheap (`ce_laguerre_exact.py`:
   Sturm sequences on one-variable polynomials, no tails, no grids — see X-C008), and it should
   be the default for that family.
2. **The LP formulation must impose $f(0)>0$.** Without it the homogeneous problem drives
   $f(0)$ negative and "succeeds" vacuously. This is an interface bug worth fixing in the shared
   solver code before any number is reported.

### X-C008 — an exactly certifiable 3D control family (PROVED: the certificate scheme is sound)

In $d=3$, with $\alpha=\tfrac12$ and $\varphi_k(x)=L_k^{1/2}(2\pi\lVert x\rVert^2)e^{-\pi\lVert x\rVert^2}$,
one has $\widehat{\varphi_k}=(-1)^k\varphi_k$ exactly. So for
$f=\sum_k c_k\varphi_k$ both $f$ and $\widehat f$ are $p(s)e^{-\pi s}$, $q(s)e^{-\pi s}$ with
$s=\lVert x\rVert^2$ and $p,q$ polynomials linear in $c$. Therefore

* $f(0)=p(0)$, $\widehat f(0)=q(0)$ are exact rationals;
* the CE hypotheses "$f\le0$ for $s\ge4$" and "$\widehat f\ge0$ for $s\ge0$" are polynomial sign
  conditions on half-lines, decided **exactly** by Sturm sequences;
* the resulting bound $\frac{4\pi}{3}p(0)/q(0)$ is a theorem with no numerical residual.

`ce_laguerre_exact.py` §0 verifies the eigenbasis from scratch (independent radial quadrature in
$\mathbb R^3$, residuals $\le4.6\times10^{-15}$ for $k\le3$). The optimisation over this family is
semialgebraic and exactly decidable; its *ceiling* is nevertheless above $\pi/\sqrt{18}$ by
X-SRC-02, so the family is a certified control, never a route to the theorem. Handing the
optimisation to Astra is request `X-R01`.

---

## 3. Objections and open items (unresolved)

* **O1.** X-C001's hypothesis "Schwartz with admissible Laplacian" is stronger than
  admissibility. The distributional version ($f$ piecewise $C^2$) is what the 1D witness
  suggests, but I have not written it out; it would let the theorem cover the tent function and
  degenerate candidates directly. *Owner: X. Low priority (no current candidate depends on it).*
* **O2.** X-C002 forces any sharp 3D certificate to vanish on all Barlow difference sets. I have
  not determined whether the union of those zero sets is itself inconsistent with
  $\widehat f\ge0$ and $f\le0$ off the ball — i.e. whether a *soft* proof of Li's non-sharpness
  in 3D exists, replacing Li's 7000-digit certificate. This is the most interesting open
  question I found; a positive answer would be a genuine simplification of the obstruction.
* **O3.** The constant in X-C003(2) is only a first draft: $A\ge0.106563$ at the icosahedral
  vertex, but Hales's actual $A$ may be negative there and compensate elsewhere, so the sparse
  defect set need not coincide with $\{A>0\}$. The correct statement concerns
  $\{A>4\sqrt2-\operatorname{vol}\Omega\}$.
* **O4.** I have not audited E's or C's current candidates: no E or C artifacts existed on the
  setup commit, and their branches are not merged into mine. This audit is therefore limited to
  the recovered historical claims and the primary sources. **This is the largest gap in my role
  report** and is the first item for the next block.

## 4. Reviewer findings summary

| Claim | Status | Basis | Reviewer needed |
| --- | --- | --- | --- |
| Hales Def 3.2 / Lemma 3.3 as transcribed here ($\sqrt{32}$) | PROVED (source) | page image + exact arithmetic | M (contract) |
| Li Thm 6.1 value, units, scope | VERIFIED (source) | paper text + conversions | M |
| X-C001 contact-shell Laplacian | PROVED | written proof + 1D exact witness | M or E |
| X-C002 non-uniqueness in 3D | PROVED | exact computation in $\mathbb Q(\sqrt3)$ | M |
| X-C003 icosahedral cell obstruction | PROVED | exact + convex-hull volumes | M |
| X-C004 bandwidth obstruction (scope-limited) | ACCEPTED | recovered report + CE §5 | — |
| X-C005 "all higher-point methods fail" | REFUTED | CDS22 Table 1.1 | M |
| X-C006 "no smooth sharp certificate" | REFUTED | X-C001 + Viazovska | M |
| X-C007 grid-LP feasibility | REFUTED (negative result) | `evidence/ce_lp_search.out` | C |
| X-C008 exact control family | PROVED (scheme) | Sturm + quadrature check | C |

*Requested review.* M should rule on whether X-C001 and X-C002 change the accepted claim ledger,
and C should adopt the exact Sturm certificate as the acceptance test for the Laguerre–Gaussian
family before reporting any CE number.

---

## K15-X-C010 — a certified Cohn–Elkies bound in dimension 3 (PROVED, weak)

Added in the full-hour block `2026-11-14T09:17:25Z` (see
`REPORT_FULL_HOUR_20261114.md`, `REPORT_FULL_HOUR_P2.md`).

> **Theorem.** Every packing of unit-radius balls in `R^3` (pairwise centre distances `>= 2`)
> has occupied-volume upper density
> $$\Delta \;\le\; \frac{4}{3\sqrt\pi}\cdot\frac{60952}{56047}\;=\;0.818086808\ldots$$

*Proof.* Let `s = |x|²`,
$$H(s)=\frac{17}{4096}\bigl(6144s^{2}+6848s+22857\bigr)>0,\qquad P(s)=-(s-4)H(s),$$
and `f(x) = P(s)e^{−s}`. Since `H > 0` on all of `R` and `s − 4 >= 0` on `s >= 4`, we have
`f(x) <= 0` whenever `|x| >= 2` (**CE1 holds by construction — no sign test is used**).
With the exact Fourier map of `ce_exact_gauss.py`,
$$\widehat f(t)=\pi^{3/2}Q(w)e^{-w},\qquad w=\pi^{2}|t|^{2},$$
and `Q` was verified to satisfy `Q >= 0` on `[0,∞)` by two independent exact routes (Sturm with
even-multiplicity handling; and `count_roots(Q,0,∞) = 0` with `Q(0) = 2858397/8192 > 0`), so
**CE2 holds**. Cohn–Elkies (Theorem 3.1) then gives
`Δ <= (4π/3)f(0)/f̂(0) = (4/(3√π))·P(0)/Q(0) = (4/(3√π))·(60952/56047)`. ∎

*Status:* **PROVED**. *Value:* weak — `0.0777` above Kepler and `0.0382` above `K15-C033`
(`0.77996650`); it is a pipeline demonstration, not a competitive bound. *Artifacts:*
`x_r03_sos.py`, `x_r03_sos_descend.py`; reproduce with
`python3 x_r03_sos.py` (gives `0.826434`) then `python3 x_r03_sos_descend.py` (gives the frozen
value). *Reviewer:* C or Main. *Remaining obligation:* none for the stated bound; the obvious
extension is an SDP over `H` of higher degree (`X-R03b`), which is an offload, not a gap in this
claim.

## K15-X-C011 — the width-π / width-1 interface constraint (PROVED, interface)

C's `exactcert` and Main's `shell_check` use the width-`π` Gaussian (`e^{−π|x|²}`, Laguerre
basis) and are interconvertible by the **rational** substitution `t = 2u`. My structural family
uses width `1` (`e^{−|x|²}`); the rescaling `x = y/√π` maps it to width `π` but sends the
polynomial argument `s = |x|² ↦ u/π²`, which is **irrational** in `u`. Hence:
**certificates cannot be transported between the two widths by a change of variable; each must be
re-derived in the target width.** Consequence for review practice: a cross-check between `K15-C033`
(in `t`) and Main's checker (in `u`) is valid and I performed it; a cross-check between
`K15-X-C010` (width 1) and either of those is *not* available, and its absence is not evidence
against the bound.

---

## Claim records added in review block 0138 (second hour)

All three are ordinary Cohn–Elkies certificates in the family `f(x)=P(|x|²)e^{−|x|²}` with
`f̂(t) = π^{3/2}Q(w)e^{−w}`, `w = π²|t|²`, so `Δ ≤ (4/(3√π))·P(0)/Q(0)`. In every case **CE1 holds
by construction** — `H` is an explicit sum of squares and `P = −(s−4)H` — so the only obligation is
CE2 (`Q ≥ 0` on `[0,∞)`), decided exactly by `exact_sign.sign_on_half_line`.

| claim | certificate | `P(0)/Q(0)` | bound | status |
| --- | --- | --- | --- | --- |
| `K15-X-C010` | `H = (17/4096)(6144s²+6848s+22857)` | `1.0874…` | `0.818086808` | PROVED (superseded) |
| `K15-X-C013` | 3 rational cubics, `X_C013_certificate.json` | `1.0565721` | `0.794809296` | PROVED |
| **`K15-X-C014`** | 6 rational quintics in `s/8`, `X_C014_certificate.json` | `1.0378402` | **`0.780718153`** | **PROVED (current best)** |

**Necessary sanity filter for any future candidate in this family:** Li's theorem gives
`P(0)/Q(0) ≥ 1.024466` for every admissible `f` (since the CE optimum exceeds `0.18398089` in centre
density). Any SDP or search output below that is **infeasible by theorem** — it is a bug, not a
discovery. (This filter would not have caught my own invalid `0.810774751`, whose `P0/Q0 = 1.0778`
was above the floor; that one was caught only by checking `H ≥ 0`. Both checks are needed.)

**What these are not.** They are not competitive: CDS22's optimised CE value is `0.779747` and C's
`K15-C033` is `0.77996650`, both below `X-C014`. They are an independent, exactly certified
demonstration that X can generate and verify ordinary-CE bounds without reusing C's or Main's code.

**Reproduction.** `python3 x_r03_sos_descend.py` (C010) · `python3 x_r03b_sos_from_sdp.py` (C013,
needs cvxpy) · `python3 x_r03b_rescaled.py` (C014, ~140 s). Each prints the exact certificate and the
exact sign verdict; none reports a float as a bound.

---

## Claim records added in review block 0308

### K15-X-C015 and K15-X-C016 — certificates with an explicit rational Gram on BOTH sides

Both are ordinary Cohn–Elkies certificates of the form

* `H(s) = v(s/S)ᵀ G v(s/S)`, `P = −(s−4)H`, `f(x) = P(|x|²)e^{−|x|²}`
  ⇒ `f ≤ 0` for `|x| ≥ 2` **by construction** (`G ⪰ 0`);
* `Q(u) = v(u/S)ᵀ A v(u/S) + u·v(u/S)ᵀ B v(u/S)`
  ⇒ `f̂ ≥ 0` **by construction** (`A, B ⪰ 0`), where `v(x) = (1, x/S, …, (x/S)^m)`;
* the link is the exact coefficient identity
  `Q_k = S^{−k}Σ_{i+j=k}A_{ij} + S^{−(k−1)}Σ_{i+j=k−1}B_{ij}`, verified by expansion to equal the
  Fourier image of `P`.

| claim | `m, S` | `P(0)/Q(0)` | bound | status |
| --- | --- | --- | --- | --- |
| `K15-X-C015` | 2, 4 | `1.0815926849` | `0.813631102` | **PROVED** (first both-sides object) |
| **`K15-X-C016`** | 4, 8 | `1.0411662228` | **`0.783220184`** | **PROVED** (both sides, useful strength) |

**No sign predicate, no root isolation, no Sturm sequence is needed for either**: every sign
condition is the statement that a rational symmetric matrix is positive semidefinite, checkable by
rational `LDLᵀ`. `verify_all.py` performs exactly those checks.

**Necessary condition on `G`:** it is *singular* at any optimum, because `P(4) = 0` forces a double
root of `H` at `s = 4`; the correct requirement is `G ⪰ 0`, not `G ≻ 0`.

**Comparison.** C's best explicit-Gram object (`K15-C-SOSQSIDE-005`) is `1.413704545`; `X-C016` is
`0.783220184`, i.e. `0.63` better, and within `0.0033` of the best certificate in the project
(C's `K33` at `0.779966500`). `X-C014` (`0.780718153`) remains the strongest X certificate overall
but has only the p-side explicit. **`X-C016` closes C's first open obligation** — "one certificate
with obvious rational Gram on BOTH sides at useful strength".

**Reproduction.** `python3 both_sides_strong.py` (≈12 s) → matrices; `python3 verify_all.py` → all
checks. `both_sides_gram5.py` reproduces `X-C015`.

**Caveat, stated once.** These are ordinary-CE bounds, so Li's theorem governs them
(`P(0)/Q(0) ≥ 1.024466` necessarily); both satisfy it. Neither is competitive with CDS22
(`0.779747`), and no such claim is made.

### K15-X-C017 — both-sides explicit rational Gram at `0.782267220134`

Same construction as `X-C015`/`X-C016` with a **margin on `G`** (`ε_G = 10⁻²`): `P = −(s−4)H` gives
`P(4) = 0` for any `H`, so `H` need not vanish at `s = 4` and `G` need not be singular — the singular
`G` at the `m ≥ 5` optima was a coincidence that exact rounding broke. `m = 5`, `S = 8`, rational
`6×6` `G, A, B`, all PSD by exact rational `LDLᵀ`, identity and link exact by expansion, density
`0.782267220134`. **No sign predicate, no root isolation, no Sturm sequence is needed.**

Ladder of both-sides objects: `C SOSQSIDE-005 1.413704545` → `X-C015 0.813631102` →
`X-C016 0.783097911` → **`X-C017 0.782267220`** → (`X-C014 0.780718153` has p-side only) →
`C K33 0.779966500` (neither side). `X-C017` is within `0.0023` of the project's best bound with
every sign condition reduced to three rational PSD tests.

Reproduce: `python3 both_sides_gmargin.py` (single configuration, ≈6 s); verify:
`python3 verify_all.py` (**ALL PASS**).

### K15-X-C018 — the repaired flow theorem is correct at all six requested points

`Main/CUT_FLOW_THEOREM.md` at `aa52147` (main tip `9d6414d`) passes the audit Main requested in
`AUDIT_REQUEST_X.md` §5: directed model, cut orientation with `X = ∅` forced, demand satisfaction
including `b(v) = 0`, Farkas + coarea, Theorem 2 without `sup_e Φ_e < ∞`, and the two-branch
threshold formula. No fifth defect found. Evidence: `Reviews/audit_cutflow_repair.py` (exits 0),
which agrees with a direct LP on 115 random instances: `(C) ⟺ LP feasible ⟺ Φ ≥ t*`. One instance
needs both threshold branches at once (isolated `+1` vertex disjoint from the §5(b′) star:
finite branch `4/3`, answer `+∞`).

### K15-X-C019 — `X_C017_small`: 3.80× smaller certificate at `0.782267254856`

`X_C017_small.json`: same both-sides Gram construction, entries on the grid `2⁻²⁴`, ≤ 20 digits
(was 281), 2,646 bytes (was 10,056), density `0.782267254856` (`3.5·10⁻⁸` weaker than `X-C017`).
`L p = 0` exactly; `G, A, B ⪰ 0` by rational `LDLᵀ`; no sign predicate. Verified by
`python3 verify_XC017_readable.py X_C017_small.json`. Not a new best bound, not a Kepler proof.

### K15-X-C020 — erratum: witness W6 of `REVIEW_0353` §3 is wrong

The two-disjoint-edges row (`b = (1,−1)` and `(2,−2)`, `F = V`) is neither "infeasible" nor
"feasible for every `Φ > 0`": the singleton cuts bind, so `t* = 2` and it is feasible iff
`Φ ≥ 2`. The point the row was meant to pin is still valid — `U = V` has `Σ_U b = 0 ≤ 0` with
`δ⁺(U) = ∅`, so an empty boundary with zero sum is **not** an obstruction. W1–W5 stand.

### K15-X-C021 — the height of `X_C017` is lcm blow-up, not the pivot block

Each term of a constraint row has a `≤ 17`-digit denominator; the terms' denominators are
mutually coprime and the lcm of 21 of them is 118 digits. Rounding to `10⁻ᵐ` cannot help; rounding
to the dyadic grid `2⁻ᵐ` that `S = 8` already uses removes the blow-up. Grids coarser than `10⁻⁶`
break `A`, whose margin was forced to `10⁻⁶` by the SDP (`G` survives coarser grids: `ε_G = 10⁻²`).

### K15-X-C022 — no small-denominator both-sides triple exists in the `S = 8` Gram basis

Frontier over the forced margin `ε_AB` (each row: the coarsest dyadic grid that survives exact
`LDLᵀ`, and the resulting size): `ε_AB = 10⁻⁶` → density `0.7822673`, grid `2⁻²⁴`, 20 digits,
2,646 bytes; `10⁻³` → `0.783625`, `2⁻¹⁸`, 18 digits, 2,231 bytes; `10⁻²` → `0.795846`, `2⁻¹²`,
16 digits, 1,833 bytes; `5·10⁻²` → `0.850160`, `2⁻¹⁰`, 16 digits, 1,732 bytes. Every row cheaper
than 2,646 bytes is worse than `X-C016` (`0.783097911`), so nothing is gained at comparable
strength. The digit floor is structural: row 11's pivot coefficient is `S⁻¹⁰`, so the solve
multiplies by `8¹⁰ ≈ 1.07·10⁹` (~9–10 digits; corrected from an earlier `8¹¹`) on top of magnitude
and grid. A 5-digit certificate in this basis does not exist; `S = 1` would remove `8¹⁰` but reintroduce the lcm problem through
the Fourier map's own denominators. Reproduce: `python3 x_c017_shrink.py`.

### K15-X-C023 — C's four `cut_flow.py` defects are reproducible by one portable script

`python3 Reviews/repro_c_cutflow_defects.py` (7/7 checks, exit 0) against
`Reviews/C_cut_flow_4bcbd3a.py`, a byte copy of blob `700e44f6` (unchanged at the current `comp`
tip `790efa73`): (D1) `V_DOD_LO − V_dod = +3.861·10⁻¹²`, so the whole enclosure is above the
truth and `b0 = √32 − V_DOD` is over-estimated; (D2) `build_13(2.1029)` returns 42 edges, not
12 — the gate is `2.4448·10⁻⁵` below the true edge `4√2/√(5+√5) = 2.102924448476534`, and
phantom edges make every cut cheaper, so the row's `t*` is too small and belongs to
`R ≥ 2.1029244`; (D3) `build_fcc_patch(1)` raises `TypeError` before any geometry; (D4) at
period 16 the copies do not interact (gap 12 > R) and all 12 ring cells are extreme points of
the cluster's convex hull, hence unbounded, hence `b = −∞` on them — `(C)` holds at `Φ = 0` for
every `U` and the fixture is no evidence at any `Φ`.

### K15-X-C024 — Theorem 1 and the threshold formula, decided in exact arithmetic

`Reviews/audit_cutflow_repair.py` §E: 297 random small instances (`n ≤ 6`, `b ∈ {−2..2}ⁿ`,
`Φ ∈ {0,1,2,3}`, random `F ⊆ V`) decided by **Fourier–Motzkin elimination over ℚ** agree with the
cut condition in every case (`0/297`; one further instance undecided by the blow-up guard). A fixed
elimination order ran out of memory at `n = 6`; a min-cost order fixed it. Two earlier versions of
the routine were also wrong (a sign convention, then a premature contradiction test) and were
caught by this same comparison. Combined with §D (115 instances via HiGHS and via
`Φ ≥ t*`), Theorem 1's statement and the threshold formula are verified against two independent
decision procedures, one of which uses no floating point at all.

### K15-X-C025 — Main's `η ≥ 0` guard closes the REVIEW_0308 §17 witness without moving a number

`Reviews/verify_eta_closed.py` (exit 0): blob `909a50a` on C's row `n = 27`, `ρ = 41/20`, with
`η = −7611431/500000000` returns density `0.015185801` (the 1.5% witness); blob `5caa1c9` returns
`None`; the `η = 0` control returns `0.780370311` on both, unchanged. The three adversarial
families (`Reviews/x_family_check.py`) give **0 wrong verdicts** against `5caa1c9`. Integration
note: `check()` now returns `None` for `η < 0`, so a caller that computes `η` as `max p` on the
shell will fail loudly (intended); `shell_fixture.py` exits 2, `checker_adversarial.py` tests it.

### K15-X-C026 — the repaired checker passes 9,000 further adversarial queries

`Reviews/x_family_check.py Reviews/shell_check_5caa1c9.py 3000 23`: **0 wrong verdicts in 9,000
random-family queries** (roots in `[0,2]`, multiplicities 1–2, both signs of the leading
coefficient), 0 in the probe-targeted family, 0/8 in the near-touching family `(u−r)² ∓ ε`. The
truth is the proven algebraic rule, computed independently of any checker. This is a regression
check on the predicate part only: the `5caa1c9` change is the `η ≥ 0` precondition, so no
predicate should have moved, and none did.

**Correction to X-C025's scope.** C's `solve_laguerre` has carried the constraint `−η ≥ 0` since
at least `4bcbd3a` (with a comment recording that the opposite sign let the objective drive `η` to
the `−1e5` box bound). So the C-side pipeline was already guarded; the exposure was confined to
the checker's licence, which is what `5caa1c9` closes. The `X_eta_negative_witness` input is
synthetic (C's committed row with `η` replaced by the shell maximum), not a run C produced.

### K15-X-C027 — the readable verifier rejects tampered certificates

`Reviews/negative_control_readable.py` (exit 0): of four copies of `X_C017_small.json`,
`G[0,1] += 1/1000`, `A[1,1] += 10⁻⁶` and `A[0,1] = 100` are all REJECTED by
`verify_XC017_readable.py`, and the unmodified copy is VALID. The `10⁻⁶` perturbation moves the
density in the 7th decimal only, so it would pass any float comparison of the bound; it fails
because the exact identity `L p = 0` breaks. A verifier that accepted it would be checking nothing.

### K15-X-C028 — Main's D18 reverse condition is not triggered; D3 and D16 states

`X-C018` found no fifth defect in the repaired `CUT_FLOW_THEOREM.md`, so D18's reverse condition
("reverse if X's audit of the repaired statement finds a further defect") is **not** triggered.
D16's acceptance test stands at `5caa1c9` on the evidence of `X-C025`/`X-C026`, with generic
predicate soundness still `SUSPENDED` as Main's docstring says. D3's anchor is respected: nothing
here is progress below `0.754697399337`. Still live and unchanged from an earlier block:
`Main/NEXT_PACKAGE.md` item 1 asks for `Σ_{v∈K} vol Ω(v) ≥ 13V` with "even `V = 5.40`", which
Hales–McLaughlin already implies (`13 V_dod = 72.1538 > 70.2`); the item needs rewording before a
block follows it.

### K15-X-C029 — `CLAIMS.md` `K15-C093` still states two claims its own repair note refutes

The bullet list at the head of the `K15-C093` entry carries pre-repair text: Theorem 2 "and
`sup Φ < ∞`" with "Tychonoff on `∏_e[−Φ₀,Φ₀]`" (removed by the repair), and "the variant
`b(a) = 4` is infeasible at `Φ = 1` with the violating cut `{a}`" (the violating cut is `F`, and
infeasibility holds at every `Φ`). The repair note 20 lines below says both are wrong. Editorial,
not mathematical: the document is correct, the ledger's summary of it is not. Consequence if
unfixed: a reader takes away a superfluous hypothesis and `4/3` as the threshold of a vector that
has none. No published claim depends on either (`C084`, `C085` do not use `4/3`), so this is
documentation only.

### K15-X-C030 — `0.008880268414417` is a lower bound, not "the exact threshold"

The exact singleton constant is `(4√2 − V_dod)/12 = 0.0088802684147391605…` with
`V_dod = 100(3√10+7√2)/(25+11√5)^{3/2}`. Main's `0.008880268414417` is lower by `3.22·10⁻¹³ =
3.8607·10⁻¹²/12`, i.e. it inherits C's `V_DOD` enclosure error (D1 of `X-C023`), and the claim
that "the two routes give the same number" holds only because both use that enclosure. The
direction is safe (an over-estimate of `V_dod` weakens a necessary condition), so the number is a
valid floor; the word "exact" is what is wrong. Quote `0.0088802684147391605`, or call it a bound.

### K15-X-C031 — the family suite catches `a8526a8` (50/900) and `5619c1d` (8/308), and is blind to others

Same three families against five checker blobs, blob ids verified by `git hash-object`:
`a8526a8` (`Reviews/shell_check_main.py`) **50/900 random, 3 probe-targeted wrong**; `5619c1d`
(`shell_check_9461aae.py`) 0/900, **5 targeted**, **3/8 near-touching**; `7dc6be58`
(`shell_check_0a85bee.py`) 0/900, 0, 0/8; `909a50a` (`shell_check_7c56c5ee.py`) 0/900, 0, 0/8;
`5caa1c9` 0/3600, 0, 0/8. The suite is therefore not vacuous. It is blind to two defect kinds: a
missing precondition (`909a50a`'s `η` licence, caught by `X-C025`'s witness instead) and whatever
`7dc6be58` is — that blob is not in my recorded sequence `a8526a8 → 5619c1d → 812105c3 → 909a50a`,
so no claim is made about it. Passing the families is evidence, not proof; `K15-C098`'s
`SUSPENDED` label stays correct. **Correction recorded here:** my first version of this table
labelled `shell_check_0a85bee.py` as `a8526a8`; it is `7dc6be58`, and running the real `a8526a8`
changed the conclusion from "the suite misses this one" to "the suite catches it 50/900".

**Latent fifth defect (not live).** `exhaustive_cut_scan(b_lo, edges)` raises
`TypeError: 'NoneType' object is not subscriptable` when no subset has a crossing edge — `best`
stays `None` and is indexed at `best[0]`. `main()` guards this with `if not edges`, so
`python3 cut_flow.py` runs; the gap is in the function's contract (its docstring promises `None`
only for an oversized scan) and for any caller that evaluates the `R < 2` regime through it.
Recorded in `Reviews/repro_c_cutflow_defects.py` as D5, labelled latent.

**Cosmetic mismatch (D7).** `exhaustive_cut_scan` returns `t_star = max_U Σ_U b/|δ⁺(U)|` without
the repaired theorem's `max(0,·)`, so on an all-negative instance it reports `t_star = −1` where
`t* = 0`. `Φ ≥ t*` is unaffected (`Φ ≥ 0` is a hypothesis); the number itself is not the theorem's
`t*`.

### K15-X-C032 — `PROOF_GAPS` G8, part one: the two exact checkers share no code

`Reviews/g8_checker_independence.py` (exit 0). **No shared code path:** `exactcert.py` (comp
`5c10267`) imports `fractions.Fraction` only and hand-writes `pmul`, `pdivmod`, `pgcd`,
`sturm_chain`, `sign_variations`, `cauchy_bound`; `shell_check.py` (`5caa1c9`) imports `sympy` +
`fractions` and delegates root isolation to SymPy; neither imports the other. **Agreement:** on
`q ≥ 0` on `[0,∞)`, **four** routes — Main's SymPy predicate, C's hand-rolled Sturm, X's
`exact_sign.py` and the algebraic odd-part rule — agree on all 52 vectors tried — both leading signs, roots at 0, repeated roots, and 12
near-touching cases `(t−r)² ∓ ε` with `ε = 10⁻²⁰, 10⁻⁸`. **Not closed:** finite sample, `q`-side
only; the `p ≤ η` predicate and the `η` precondition are outside it (the latter is `X-C025`). G8
should read "independence established; agreement sampled, not proved".

### K15-X-C033 — C's `feasible_flow` agrees with the cut condition on 38 instances

`Reviews/audit_cutflow_repair.py` §F: C's max-flow constructor (blob `700e44f6`, scipy search,
then rounded to rationals and re-verified exactly) returns a flow exactly when the cut condition
holds, on 38 random instances with `n ≤ 5` (25 infeasible, 13 feasible, 0 mismatches). That makes
four independent decision procedures for Theorem 1 on the same instances — the cut scan, my
HiGHS LP, my exact Fourier–Motzkin routine, and C's flow constructor.

### K15-X-C034 — three functions take their vertex set from the edge list and accept an impossible instance

`verify_flow_exact`, `find_violating_cut` and `feasible_flow` all infer the vertex set as
`n = max(max(e) for e in edges)+1`, so a vertex with no incident edge is never checked. Witness:
`b = (−1,−1,+1)`, `edges = [(0,1)]`, `Φ = 1` — vertex 2 is isolated with a unit deficit, so the
instance is infeasible at *every* `Φ`. `verify_flow_exact(b, E, 1, {})` → `(True, True, [0,0])`;
`find_violating_cut(b, E, 1)` → `None`; `feasible_flow(b, E, 1)` → a flow. All three wrong; only
`exhaustive_cut_scan` is right (`empty_boundary_positive = [([2], '1')]`). The module contradicts itself here: the cut scan
reports `[([2], '1')]` as an empty-boundary positive set, i.e. infeasible at every `Φ`. **Reachable through `--fixture`:** `load_external_fixture` validates edge indices but not that
every vertex appears in an edge, so a five-vertex fixture with edges on `0..3` and
`b = (−1,−1,−1,−1,+1)` makes `evaluate_external` print "POSITIVE DEFICIT AT DEGREE ZERO at [4]:
INFEASIBLE at any Phi" and then emit `status: PATCH_FEASIBLE`. Not reachable from `main()`'s own
fixtures (`build_13` gives every vertex an edge for `R ≥ 2−10⁻⁹`; the edgeless regime is skipped),
so no published number is affected. Fix: `n = len(b)` in all three functions. D8 of
`Reviews/repro_c_cutflow_defects.py` (11/11 checks).

### K15-X-C035 — Main's `le_on_interval` agrees with X's `sign_on_interval` on 50 vectors

`Reviews/g8_checker_independence.py`, second section: 50 polynomials with roots in `[0,2]`,
multiplicities 1–2, both leading signs, decided for `p ≤ η` on closed intervals with rational
endpoints and `η ∈ {0, ±1/2}` — Main's `le_on_interval` and X's `sign_on_interval` agree on all 50.
C's `exactcert` has no bounded-interval decision, so this is a two-way test. The failure mode my
own `exact_sign` docstring warns about (reading the sign from `sign(lc)`, which is only the
rightmost gap) does not occur in Main's current version.

### K15-X-C036 — C's repair closes D1, D2, D3 and leaves D4, D5, D7, D8 open

`cut_flow.py` moved `700e44f6` → **`c2127cee`** at comp tip `716a1b3` (commits `2fa125c`, `e229923`,
`a1d99ef`, whose messages name review 0353-C). Re-running `Reviews/repro_c_cutflow_defects.py`
against the new blob: **D1 (the `V_DOD` enclosure), D2 (the `build_13` ring gate) and D3
(`build_fcc_patch(1)`) no longer reproduce** — verified by the same witnesses, not by reading the
commit message. **D4** (period-16 unsaturation), **D5** (`exhaustive_cut_scan` on edgeless input,
latent), **D7** (`max(0,·)` omitted, cosmetic) and **D8** (vertex set taken from the edge list —
still producing `status: PATCH_FEASIBLE` through `--fixture` on an instance infeasible at every
`Φ`) still reproduce. The repro script now takes the module path as an argument so any future
revision can be audited the same way. **Why `e229923`'s new self-check does not catch D8:**
`feasible_flow` now calls `verify_flow_exact` before returning, but that verifier computes its
vertex range the same way (`n` from the edge list), so both agree on a truncated vertex set. The
self-check is a genuine repair of the `1e-9`-grid defect it names (`8.3·10⁻⁹` below the cut scan's
`t*`), and it cannot test an assumption it shares.

### K15-X-C037 — `C_R` in Theorem B is defined as the wrong set; the identity needs the one-endpoint sum

`GEOMETRIC_LEMMA_0438.md` (a6f3935) line 90 defines `C_R := Σ_{e : e ⊄ B∖E_B} c_e` (every edge not
contained in `B∖E_B`), while line 94 uses it in `|B| − |E_B| = 2Σ_{e⊆B∖E_B}c_e + C_R`. The middle
sum counts each edge with multiplicity `#{e ∩ (B∖E_B)}`, so the identity holds iff `C_R` is the sum
over edges with **exactly one** endpoint in `B∖E_B`. With line 90's set, an edge entirely outside
`B` with `c_e > 0` breaks it, and for a translation-invariant weighting there are infinitely many,
so `C_R = +∞` and line 100 is vacuous. The document's own self-audit at line 409 states the correct
object, so this is a definition typo; `C_R ≤ O(R²) + 12|E_B|` (line 120) is right for the corrected
definition. Exact witness: `Reviews/witness_0438_audit.py` W1 — `|B|−|E_B| = 4`, `2S₂+S₁ = 4`,
`2S₂+(S₁+S₀) = 13/3`, discrepancy exactly the weight of one edge touching `B` neither.

### K15-X-C038 — `(M)`'s characterisation is the FRACTIONAL Tutte condition and is correct (my first reading was wrong)

Line 197: `(M)` holds iff for every finite `S`, `#isolated vertices of G−S ≤ |S|`. That is the
fractional condition `ν*(G) = min_S (|V|+|S|−iso(G−S))/2 = |V|/2`, and it is **correct**: verified
against an LP on **all 33,867 graphs with `n ≤ 6`**, 0 mismatches (`Reviews/witness_0438_audit.py`
W2 runs `n ≤ 5`). An earlier draft of this review read it as Tutte's *integral* condition (odd
components) and "refuted" it with the triangle; the triangle refutes only the integral form, and
that claim is withdrawn. The practical certificate form is Farkas: `(M)` infeasible ⟺ ∃`y` with
`y_u+y_v ≤ 0` on every edge and `Σy > 0`; on `K_{1,12}` the certificate is `y = −1` at the centre,
`y = +3/4` at the twelve leaves (edge sums `−1/4`, total `8`).

### K15-X-C039 — the failure of `(M)` is not "exactly" an icosahedral cluster (wording)

The mechanism is "some `S` with `iso(G−S) > |S|`". The icosahedral 13-cluster is its extremal
geometric instance, not the only one: `K_{1,3}` fails via `S =` its centre, and three contacts at a
centre is a legal local configuration. The conclusion the document draws (the bridge's hypothesis is
not automatic) is unaffected; the word "exactly" should go.

### K15-X-C040 — "(L)'s equality case is exactly the Barlow family" is refuted by C095

Line 40 asserts the converse (equality in `(L)` ⟹ Barlow) and proves only Barlow ⟹ equality. `C095`
gives the counterexample: the crack packing is saturated, **every bulk cell has volume `√32`
exactly**, so any bulk–bulk contact pair has `vol Ω(v)+vol Ω(w) = 2√32` — equality in `(L)` — and
`C095` §4 states the packing is **not** Barlow (layer spacing `d ≠ H` across the crack). The same
file's §5 table records this ("crack packing | bulk–bulk | equality in the bulk"), so line 40
contradicts line 240. Repair: "attained on every Barlow packing and on the bulk of every planar-fault
packing; the equality family is not classified".

### K15-X-C041 — Theorem C's "the equality case of the dodecahedral bound is empty" needs a stability theorem

Consequence 2 (line 385) infers from equality of *density* that "every cell is a dodecahedron". The
bound is a limit of averages and all terms are `≥ V_dod`, so equality gives only
`density{vol Ω > V_dod + ε} = 0` for each `ε > 0`; cells of volume `V_dod + ε_v` with `ε_v → 0` are
compatible with that and are not dodecahedral. Closing the step needs: `vol Ω(vₙ) → V_dod` ⟹ cells
asymptotically dodecahedral ⟹ asymptotically twelve contacts — a **quantitative stability version of
Hales–McLaughlin**, which `EXPOSITION_0438.md` §6 itself names as unavailable. The corollary is not
refuted (it may well be true); the argument given is not a proof of it. Theorem C itself is correct
and I checked its split, its two-sided volume estimate and `ρ ≤ 1/2`.

### K15-X-C042 — the slack display is correct under the repair's reading and false if `E` is kept

The split gives `Σ_B vol Ω ≥ √32(|B| − |E_B|) − (√32−V_dod)(Σd_v + C_R')` with
`√32−V_dod = 0.106563221` on both terms. The display at line 215 has `2(√32−V_dod)` on `Σd_v`,
`√32` on `C_R`, and no `|E_B|` term. **If the exceptional set is absorbed into the slack (`E = ∅`,
which is what the repair intends) the display is weaker than the split and true**; the difference is
`−(√32−V_dod)Σd_v − V_dod C_R' ≤ 0`. **If `E` is kept alongside `d`, it can fail**: `R = 0` with
`B = {v}`, `v ∈ E`, `d_v = 0`, `vol Ω(v) = V_dod` gives the display `V_dod ≥ √32` ✗ while the split
gives `V_dod ≥ 0` ✓. The finding is the ambiguity — the sentence does not say whether `E = ∅` — and
the repair is to state it, or to replace the display by the derived form. Conclusion unaffected
(`|E_B|`, `Σd_v`, `C_R'` are all `o(R³)`). This entry has been rewritten twice; the two readings are
why the block's swarm split 3–2 on it.

### K15-X-C043 — Theorem D step 4 confirmed independently, and the E/Main discrepancy resolved

`Reviews/two_dodecahedra_indep.py`: building the two icosahedral rings from the dodecahedron's face
normals, putting the centres at distance 2 and maximising over the twist about the `v`–`w` axis gives
`sup_t m(t) = 1.125554844510` at `t = 36°` (required 2; shortfall 0.8744) — Main's
`1.12555484451` confirmed to twelve digits, over a *superset* of the legal configurations (legality
forces the shared pentagon to coincide, a multiple of 72°), so the impossibility is a fortiori.
**The "unresolved discrepancy" with E is resolved:** `1.056487696` is a value of the same function,
attained at twist `33.636862°` and `38.363138°`, while its supremum is `1.1255548`. E sampled
another twist; Main's number is the supremum. Main's four tabulated values at `0°, 18°, 36°, 54°`
are this script's `m` at `36°, 54°, 0°, 18°` (twist origin shifted by 36°).

### K15-X-C044 — `cut_flow.py` at `a25f5be` still truncates the vertex set in three functions, line-specifically

Blob `c2127cee`. `singleton_bounds` (line 236) and `load_external_fixture` (line 415) use
`n = len(b_lo)` ✓; `exhaustive_cut_scan` computes `n` from the edges at line 306 but repairs it at
line 307 with `n = max(n, len(b_lo))` ✓. The three that still truncate: **`find_violating_cut`
line 269**, **`feasible_flow` line 352**, **`verify_flow_exact` line 390** — all
`n = max(max(e) for e in edges) + 1 if edges else 0`. So D8 is unchanged, the one-line fix pattern
already exists two functions away, and `evaluate_external` still emits `status: PATCH_FEASIBLE` on a
fixture that is infeasible at every `Φ` (five vertices, edges on `0..3`,
`b = (−1,−1,−1,−1,+1)`). `Reviews/repro_c_cutflow_defects.py Reviews/C_cut_flow_a25f5be.py` → 9/13
checks reproduce, the four that do not being D1/D2/D3.

### K15-X-C045 — `exact_sign.py` decided signs on the wrong interval for some exact rational endpoints

`sign_on_interval` (and `sign_on_half_line`) converted endpoints with `sp.nsimplify`. For an exact
rational with a long denominator, `nsimplify` **invents a radical**:
`nsimplify(Rational(353553390593273762200422181, 250000000000)) = 1000*sqrt(2)` = 1414.21 rather
than 1.41421. The predicate then decided a sign on a different interval, or raised
`CoercionFailed` when `count_roots` received the radical. **No published certificate is affected**
— every X certificate is decided on `[0,∞)` or `[0,4]`, where `nsimplify` is the identity — and
`verify_all.py` still reports ALL PASS after the fix. Fixed with an `_endpoint` helper that passes
`Rational`/`Fraction`/`int` through exactly and only calls `nsimplify` on symbolic input.
Regression test: section C of `Reviews/p_le_eta_independent.py`. Found by an independently
implemented decider, which is the point of having one.

### K15-X-C046 — bounded-interval `p ≤ η` closed by an independent Vincent–Descartes decider

`Reviews/p_le_eta_independent.py`: exact rational arithmetic, `w = p/gcd(p,p')`, Möbius transform
of `(a,b)` to `(0,∞)`, Descartes' count `V` (`V = 0` no root, `V = 1` exactly one, bisect while
`V ≥ 2`), then one rational sample per gap between consecutive roots plus the endpoints. No Sturm
sequence, no `sqf_list`, no SymPy root isolation. Agrees with X's `exact_sign.sign_on_interval` and
Main's `shell_check.le_on_interval` on **60 rational-endpoint cases** (endpoints at, between and
within `10⁻¹²` of roots) and **32 algebraic-endpoint cases** (`√2`, `√3`, `√5/2`, `φ`, bracketed
into root-free rational zones) — 0 mismatches. Records the two implementation traps that produced
wrong answers first (endpoint values decide nothing when an endpoint is a root; the shrink point
must not be a zero of `p`). G8 stays open: finite sample, and no proof of correctness for any of
the three implementations.

### K15-X-C047 — Hales–McLaughlin's equality case verified from the primary source

The load-bearing external input of Theorem D (`C108`) step (3) is
"`vol Ω(v) = V_dod` ⟺ `Ω(v)` regular dodecahedron of inradius 1". It is **stated explicitly** in
Hales–McLaughlin, *The dodecahedral conjecture*, arXiv:math/9811079v3 §1: "…for every set of points
`Λ ⊂ R³` whose pairwise distances are at least the diameter `2`. **The case of equality occurs
exactly when `Ω(Λ,v)` is congruent to a regular dodecahedron of inradius 1**", and again in the
strong form (§2.1): "Equality holds exactly when `Ω(Λ,v₀)` is congruent to `Ω(Λ_dod,0)`". Two
consequences: step (3) is exactly as strong as the source (no hidden stability assumption), and the
inequality is stated for **every 2-separated point set**, not only saturated packings — which is
what Theorem D's minimiser is. Caveats: the source is computer-assisted (interval arithmetic over
tame Voronoi graphs), and its `Λ_dod` has inradius 2 with pairwise distances `≥ 2`, so a conversion
to this project's inradius-1 normalisation is needed.

### K15-X-C048 — "twelve centres at mutual distance ≥ 2 on radius 2 is exactly the icosahedral twelve" is false

`GEOMETRIC_LEMMA_0438.md` line 204 asserts uniqueness of the twelve-point configuration. The
icosahedral twelve on radius 2 have minimum mutual distance `4√2/√(5+√5) = 2.102924448 > 2`, so
every sufficiently small perturbation is still admissible and the admissible set is
**positive-dimensional**; Tammes-12 is the optimiser of the minimum distance, not the solution set
of the inequality. Second reason (after `K_{1,3}`) that "the failure is exactly an isolated
icosahedral cluster" is too strong. **Explicit family:** keeping eleven icosahedral points fixed and rotating the twelfth about `e₁`
by `t` (renormalised to radius 2) keeps the minimum mutual distance `≥ 2` for `t = 0.5°, 1°, 2°, 4°,
6°` (`2.0955, 2.0880, 2.0730, 2.0427, 2.0120`), so the admissible set is at least one-dimensional.
**A failure with no cluster and minimum degree 2** (swarm member `m6`, verified exactly): the five
points `v = 0`, `w = (2,0,0)`, `p₁ = (1,√3,0)`, `p₂ = (1,−√3/2,3/2)`, `p₃ = (1,−√3/2,−3/2)` have
contact graph `K₅` minus a triangle (degrees `4,4,2,2,2`), and `S = {v,w}` leaves three isolated
vertices against `|S| = 2`; Farkas `y = (−1,−1,+1,+1,+1)`, edge sums `≤ 0`, `Σy = 1`. So "exactly an
isolated icosahedral cluster" is wrong even with all degrees `≥ 2`. Also: `K_{1,3}` is geometrically realisable — `v = 0` plus
`2·(1,1,1)/√3`, `2·(1,−1,−1)/√3`, `2·(−1,1,−1)/√3`, mutual distances `√(32/3) = 3.266 ≥ 2` — so
`(M)` fails on a legal configuration of four points, not only on the 13-cluster.

### K15-X-C049 — the "equality case is empty" corollary is true, in two lines from Hales

`π/√18 = 0.740480489693 < 0.754697399337 = (4π/3)/V_dod`, so Hales' theorem alone forbids equality in
the dodecahedral bound. The corollary is therefore **true**, and it cannot be used as independent
evidence inside a route whose purpose is to prove Kepler — which is what `X-C041` records as the gap
in Main's route (that route goes through Theorem C and needs a stability version of
Hales–McLaughlin). A swarm finding, checked and corrected: its derivation addressed "`vol Ω = V_dod`
off a density-zero set", which is stronger than density equality, so it proves the different (also
true) statement that almost-everywhere exact dodecahedral cells are impossible.

### K15-X-C050 — `C121` (explicit stability for `≤ 12`-face cells) is correct, sharp, and does not close the corollary

`main` at `8dc264e` (post-dating the audit target). Lemma: `Ω(v)` with `≤ 12` faces and all
neighbours at distance `≥ 2ρ` (`ρ ≥ 1`) has `vol Ω(v) ≥ V_dod ρ³`. **Correct**: scale by `1/ρ`, the
scaled cell is again a Voronoi cell (of a packing with minimum distance still `≥ 2`), has `≤ 12`
faces, contains `B(0,1)` and has faces at distance `≥ 1`, so Fejes Tóth's Theorem 4.1 (quoted in
`C115`) gives volume `≥ ω_dod`. Arithmetic exact: `V_dod·1.045³ = 6.333804106 = 1.119669·√32`; the
no-face-count form's threshold is `(3V_dod/4π)^{1/3} = 1.0983541`. **Sharp**, with equality at the
twelve-icosahedral-directions-at-circumradius-`2ρ` family — which has no contact at all, so `C121`
is exactly the statement that volume stability cannot produce contacts, and the corollary gap of
`X-C041`/`X-C049` survives: Theorem C needs contacts (distance exactly 2), `C121` gives neighbours
within `2ρ` (≤ 2.09 at ρ = 1.045; `C116`'s band is 2.683). What it does close is the *singleton*
question for `≤ 12`-face cells. **Flag, outside the audited target:** `C115` writes
"`t_dod = 3 tan(π/5) ≈ 1.258`", but `3 tan 36° = 2.17963` while `1.2584 = √3 tan(π/5)` — the formula
and the decimal disagree by `√3`; check against the paper before quoting.

### K15-X-C051 — the two-dodecahedra threshold is `3.4555003`, so C116's `6/√5` is valid but 28.8% short

**Corrected entry — the first version of it claimed `2φ` and is withdrawn.** The first script scaled
*v's* icosahedral ring by the separation `d` as well as w's (`d*V[i]` instead of `2*V[i]`), which
produced a spurious threshold at `2φ = 3.236068`. With v's ring fixed at radius 2 — the only version
that models two dodecahedral cells — the computation gives:

```
max over twist of the minimum cross-distance = 2 exactly at   d* = 3.4555003444
(twist 36 deg; and at d* no other centre cuts either cell, so the two dodecahedral cells are
actually attainable there)
```

So the threshold for two dodecahedral cells is `d* = 3.4555003`, and C116's `6/√5 = 2.6832816`
(main `8dc264e`) is a **valid but 28.8% short** bound (`d*/2.6832816 = 1.287789`). The configuration
is the same as `X-C043` with the separation free: v at 0 with its twelve neighbours at `2u_i`, w at
`d·u₀` with its twelve at `d·u₀ + 2R_t u_j`. `Reviews/near_contact_band_indep.py` reproduces `d*`
and the attainability check (0 cutting centres). Route impact: none — `C114` needs only
`ε < 0.6832816`, and `d* − 2 = 1.4555`.

### K15-X-C052 — A15's Voronoi volumes confirmed: 125/16 (A) and 129/16 (B), so E's 15.875 was the A–B pair

`Reviews/a15_pair_indep.py` computes the eight Voronoi cells of the Cr₃Si / A15 structure by
half-space clipping with `a = 4` (nearest distance `a/2 = 2` exactly): the two A sites have volume
`125/16 = 7.8125` each, the six B sites `129/16 = 8.0625` each, the weighted sum is
`2·125/16 + 6·129/16 = 64 = a³` exactly, the minimum site distance is `a/2 = 2`, and the A–B
distance is `√5 = 2.2360679`. **Main's post-target correction (`C111`, commit `c4134c2`) is right**:
the contact pairs in A15 are the B–B chain bonds at `a/2`, with pair sum `2·129/16 = 16.125`, and the
`15.875` in the audited §5 table is the A–B sum, which is not a contact pair. Nothing is refuted
either way — both exceed `2√32 = 11.3137` — but the table's A15 row should read 16.125.

### K15-X-C053 — the arithmetic of `C119` and `C122` (post-target) checks exactly

Recomputed: `(4π/3)/V_dod = 0.754697399337`; `8/d³ = 0.754697399337` gives `d = 2.1967082337`
(C119's threshold, and `(4π/3)(d/2)³ = 5.550291029 = V_dod` at that `d`, which is the same
comparison); `√32/1.045³ = 4.95708216846` (C122's required `c_F`); the regular icosahedron of
inradius 1 has `V_ico = 5.054056144` (C122 prints 5.054056) and `V_ico·1.045³ = 5.767517665`
(prints 5.767518), i.e. `+1.96%` over `√32`, against `V_dod·1.045³ = 6.333804106` at `+11.97%`.
No discrepancy. Both entries post-date the audit target; they are checked because they carry the
numbers a later block would quote.

### K15-X-C055 — E's payer fixture reproduced independently, and it is NOT the value §5 quotes

`Reviews/payer_fixture_indep.py` runs the closed-form fixture written down in Main's `C118`
(`c = 0`, `w1 = (0,0,2)`, five ring points at `(4/√5 cos72k, 4/√5 sin72k, 2/√5)`, five pentagon
points at `w1 + 2(s cos(36+72k), s sin(36+72k), 3/8)` with `s = √55/8`, `south = (0,0,4)`) through
an independent half-space clipping: **`vol Ω(w1) = 5.89801737180372`** — `C118`'s value to every
digit it quotes — with **20 cell vertices** and minimum pairwise distance exactly 2. So `C118`'s
reproduction is sound. **But this is not the `5.897967122` quoted in §5 of the audited
`GEOMETRIC_LEMMA_0438`**: that is a different, slightly sharper completion from E's `C5` search.
Both exceed the payer target `2√32 − V_dod = 5.763417470`; the §5 margin `0.134549652` belongs to
E's value and this fixture's margin is `0.134599902`. No claim is affected, but the two numbers
should not be quoted interchangeably.

### K15-X-C056 — the two `CDS22` three-point numbers are in the source

`EXPOSITION_0438` §4 quotes `0.770271` (general three-point) and `0.741506` (lattice three-point) as
`CDS22`. Checked against the paper: Cohn, de Laat and Salmon, *Three-point bounds for sphere
packing*, arXiv:2206.15373 — the HTML full text contains **`0.770271` twice and `0.741506` twice**
(a table and a comparison). So the attribution is right. Note for a later reader: the paper's
*abstract* advertises new bounds only "in dimension 4 through 7 and 9 through 16", because `d = 3`
is not new territory — the `d = 3` values are there, but a reader who stops at the abstract will
think they are the project's own computation. They are not.

### K15-X-C057 — `twist_cover.py` is unsound in BOTH revisions: missing `2u_x q_x`, and the arcs are the complements

Audited blobs `469fc9f181f976598fd866d9d6473527d4e4a6f8` (C112, main `8dc264e`) and
`67d5c97345cbdb049461b1ea8c50d743b0bf58f1` (C123, main `6d542f5`). **D1:** with `u = w − a` and the
twist about the v–w axis, `d²(t) = |u|²+|q|²+2u_x q_x + 2(u_y q_y+u_z q_z)cos t + 2(u_z q_y−u_y q_z) sin t`;
both revisions set `A = |u|²+|q|²` and drop `2u_x q_x`, which is nonzero for **121 of 121 pairs** and
makes `A` too large when `q_x > 0` (unsafe). Exact witness: code `A = 8.422291236` vs true
`6.444582472`; at `t = 10.3°` the code gives `d² = 4.0006` (safe) while the truth is `2.0229` (clash),
and the direct recomputation agrees with the corrected constant. **D2:** `{t : cos(t−ψ) < c}` is
centred at `ψ+π` with half-width `π−acos c`; both revisions use `[ψ∓acos c, ψ±acos c]`, the **far**
set. Over the 121 pairs `c ≤ −0.381966`, so true clash half-widths are `≤ 67.54°` while the code
uses `≥ 112.46°`, and **all 50 emitted arcs are centred where `d² = 16.8`** (the far point). C123's
claim that its arcs are "subsets of the true violation sets" is the reverse. Reproduce:
`Reviews/twist/audit_twist_cover.py`.

### K15-X-C058 — the two-dodecahedra theorem at distance 2 is TRUE, and the corrected cover certifies it

`Reviews/twist/corrected_cover.py`: same configuration, both defects fixed (`A` includes `2u_x q_x`;
arcs centred at `ψ+π`, half-width `π−acos c`; inner shrink `1e-30` at 60 digits). Result: 45 raw arcs
merging to **one interval `[0°, 72°]`**, full coverage of the twist circle with no gaps, and the
cover **survives shrinking every arc by 2°**. Validated by 175 inside/outside samples against the
direct distance (0 disagreements) and by the sampled maximum of the minimum distance
`1.125554845 < 2`. So: for every relative twist some pair is strictly closer than 2, and two regular
dodecahedral cells of inradius 1 cannot have centres at distance 2. This restores `C108` step (4);
`ACCEPTED.md`'s "modulo ... `C112`" should read "modulo the corrected cover".

### K15-X-C059 — `C116`'s `6/√5` inherits both arc defects; the statement is true but the threshold is `3.4555003`

`near_contact_band.py:43` uses `twist_cover.inner_arcs`, so the near-contact band computation
inherits D1 and D2 of `X-C057`. The *statement* ("two dodecahedral cells impossible for centre
distance below `6/√5 = 2.6832816`") is true, but proved by `X-C051`'s direct computation, which
gives the true threshold `3.4555003` (attained, with no other centre cutting either cell). Since
`3.4555003 > 6/√5`, impossibility below `6/√5` follows from `X-C051`, not from `C116`.

### K15-X-C060 — E's `rigorous_cell_volume.py`: componentwise error used where the Euclidean norm is needed

Blob `d015a2e1e322853286322ff2c6ec4a5a88f03550` (experimental `d289bef`). The code sets
`e = max((x.hi − x.lo)/2 for x in n)` and then `slack = R*e + f`, but the inclusion
`{y·n' ≤ b' − slack} ⊆ Ω` needs `|y·(n − n')| ≤ R‖n − n'‖₂`, and `‖·‖₂ ≤ √3‖·‖_∞`. Exact rational
witness with `R = 1`: `n₀ = (1,0,0)`, `n = (3/5,4/5,0)` gives `‖n−n₀‖_∞ = 4/5` but
`‖n−n₀‖₂ = 0.894427`, and `y = (−4/9,8/9,0)` (`|y| = 0.993808`) has `y·(n−n₀) = 8/9 = 0.888889 > 4/5`.
So the allowance is smaller than the perturbation it must absorb and the inner inclusion can fail.
Reproduce: `Reviews/twist/audit_E_cell_volume.py`.

### K15-X-C061 — E's `rigorous_cell_volume.py`: an unbounded cell gets a finite "certified" volume

Same blob. `polytope_volume` accepts any body with ≥ 4 feasible triple-plane vertices and never tests
boundedness; `sandwich`'s `R`-check inspects only the vertices it found, so an unbounded body passes
vacuously. Witness: centres `(±2,0,0)`, `(0,±2,0)`, `(0,0,−2)` give the cell
`{|x| ≤ 1, |y| ≤ 1, z ≥ −1}` with recession ray `(0,0,1)` and **infinite** volume; E's
`sandwich(centres, R=2)` returns `[1.3333333333333333, 1.3333333333333333]`. The rational polytope
machinery is exact (cube `8`, tetrahedron `8/3`, fcc control `4√2` all ✓); the enclosure argument is
what fails. Repair requirements: boundedness, norm choice, radius bootstrap, inner inclusion, exact
domain coverage.

### K15-X-C062 — the §4 slack display appears in three `main` files and is true only with `E = ∅`

`Claims` `C106`/`GEOMETRIC_LEMMA_0438.md`/`PROOF_GAPS.md` all carry
`Σvol ≥ √32|B| − (2√32−2V_dod)Σd_v − √32 C_R`. Under the repair's reading, where the exceptional set
is absorbed into the slack (`E = ∅`, so `d_v + Σc_e = 1` for every `v`), it follows from the derived
form `√32(|B|−|E_B|) − (√32−V_dod)(Σd_v + C_R')` with difference
`−(√32−V_dod)Σd_v − V_dod C_R' ≤ 0`. If a non-empty `E` is kept alongside `d`, it is **false**
(`R = 0`, `B = {v}`, `v ∈ E`, `d_v = 0`, `vol Ω(v) = V_dod` reads `V_dod ≥ √32`). Each of the three
files should state `E = ∅` or use the derived form.

### K15-X-C063 — the repair for E's cell certifier is cheap, and the box alone is not enough

`Reviews/twist/repaired_sandwich.py`. Two changes to E's `sandwich`: slack
`R·√3·(e + QERR) + f + QERR` (the Euclidean norm, `X-C060`), and the box `|y_i| ≤ R` on both
polytopes (`X-C061`). **The fcc control still closes** at width `1.4·10⁻¹⁸` for `R = 2, 3, 4`, so
the norm fix is free. **But the box does not detect unboundedness**: on the
`{|x|≤1, |y|≤1, z≥−1}` witness the boxed sandwich returns `[12.000000, 12.000000]`, finite and not
the cell's volume, because the box cut it. What detects it is a **saturation check** — every outer
vertex within 2 of some centre, which is what licenses the a-priori bound `R = 2` — and on that
witness 4 of the 8 outer vertices fail it. So requirement (1) is "boundedness *plus* the covering
check", not "add a box". E's `certify_region.py` imports `rigorous_cell_volume as R` and uses
`R.box_volume`, so the certified *region* at `d289bef` inherits both defects until the atom is
repaired.

### K15-X-C064 — the two-dodecahedra threshold is CERTIFIED at `3.455500344` (not sampled)

`Reviews/twist/certified_threshold.py`: the corrected arc cover run with the partner centre at
`d·u₀` covers the twist circle for `d = 2.0, 2.5, 3.0, 3.3, 3.4, 3.45, 3.455` and fails at
`3.456`, `3.46`, `3.5`; bisection gives `d_c ∈ [3.455500344, 3.455500344]`. That matches `X-C051`'s
sampled threshold `3.455500344` to nine decimals and upgrades it from "maximised over a grid" to
"covered for every twist". Consequence: `C116`'s `6/√5 = 2.6832816` should be `3.455500344`, and the
statement ("two dodecahedral cells impossible below `d_c`") is certified rather than inferred.

### K15-X-C065 — E's `certify_region.py` box grid can leave a gap and still say "CERTIFIED for the whole region"

Blob at experimental `d289bef`. The grid is `n = int(round((hi − lo)/w))` then `n` boxes at
`lo + i·w`; nothing checks the remainder, and the epilogue prints "CERTIFIED for the whole region"
regardless. Replicating the index arithmetic: `[110°, 111.05°]` at `w = 0.1°` is covered only to
`111°` (gap `0.05°`); `[110°, 111°]` at `w = 0.3°` only to `110.9°` (gap `0.1°`). The default region
`[110,111] × [35,36]` at `0.1°` is an exact multiple, so that run is unaffected. Fix: require the
extent to be an integer multiple of `w`, or add the remainder box. (Independently, the region's
certification inherits `X-C060`/`X-C061` through `rigorous_cell_volume.box_volume`.)

### K15-X-C066 — the 13–20-face route has no obstruction but needs an unproved classical constant

`C122`'s (B_F) needs `c_F > √32/1.045³ = 4.957082168`. No obstruction exists for `F ≤ 20`: the
20-faced constant is `V_ico = 5.054056144` (regular icosahedron of inradius 1) and
`V_ico·1.045³ = 5.767517665 > √32`, a **1.96% margin** (against the dodecahedron's `11.97%` at
`F = 12`). **But the optimality of the icosahedron among 20-faced circumscribed bodies is not
proved**: Lindelöf's theorem gives only the shape of an optimum (faces tangent at centroids);
proved optimality covers `n = 4, 5, 6, 12` (Fejes Tóth) — the same `≤ 12` boundary as the
dodecahedral theorem — while `n = 20` is classical conjecture with numerical support (Goldberg;
Mutoh's computer-aided search, `4 ≤ n ≤ 30`). So the 13–20-face case closes *if* that conjecture
holds, with 1.96% margin, and the route does fail for large `F` since `4π/3 = 4.188790 < 4.957082`.
The obstruction the brief asked for exists only in the large-`F` direction, and it is the ball.

### K15-X-C067 — E's sin/cos interval extension is sound (checked), unlike the enclosing steps

`range_of` in `rigorous_cell_volume.py` (blob `d015a2e1...`) returns the hull of the corner values
plus the quarter-turn points inside the box; that is a valid interval extension, and a direct test
gives **504 samples over 12 random boxes, 0 outside the interval**. Recorded so that `X-C060`/
`X-C061` are not read as "E's arithmetic is wrong": the rational polytope machinery (cube `8`,
tetrahedron `8/3`, fcc `4√2`) and the trigonometric enclosure are exact; the defects are the
Euclidean-slack step, the boundedness step and the region grid.

### K15-X-C068 — C's near-contact scan does not inherit the arc defect, and its 500 instances are exact

`nearcontact_scan.py` (comp `cde39fa`) imports `fixture_nonuniform` and `cut_flow`, not
`twist_cover`, so `X-C057` does not touch it. Its output at comp tip `bf7998c`:
**500 instances, `with_positive_t_star: 0`, all `t_star` exactly `0`**, density range
`[0.620562, 0.739247]` — below Kepler throughout. Exhaustive over `2^4` subsets with exact rational
cell volumes, so `t* = 0` is exact for those fixtures; the docstring's scope caveat is correct and I
am not upgrading it. Interaction with D7 (`X-C044`): `exhaustive_cut_scan` has no `max(0,·)`, so a
raw `t_star` of exactly `0` over all 500 instances means some cut has `Σ_U b = 0` exactly.

### K15-X-C069 — C's exact cell volumes satisfy the right tiling identity on all 500 rows

Checked against `out/nearcontact_scan.json` (comp tip `bf7998c`): the four cells in each row satisfy
`Σvol = a³` exactly in the 488 cubic rows and `Σvol = a³·t` in the 12 tetragonal (`F2`) rows with
`t = 1.01, 1.02, …` — the correct identity per family, in exact rational arithmetic. The stored
densities equal `(4π/3)/mean(vols)` in 200/200 rows checked. So C's volume engine is consistent with
its own data; the finite scope is the only limit, and the docstring states it.

### K15-X-C070 — C102's constant `3.206870905` is CORRECT; `3.178617889` is the same function at `ρ = 2`

The previous block queued an entry saying C102's `min |p| = 3.206870905` was 0.881% too high and that
the true minimum was `3.178617889` at C102's own direction. **That entry was wrong and is withdrawn
before it was ever written**: the two numbers are the same function evaluated at different radii.
`Reviews/twist/nearest_13th_indep.py` (exit 0) recomputes at `ρ = 2.09`, the radius C102 uses:

- independent mpmath (dps 30) implementation of `r₊(c) = c + √(c² − (ρ²−4))`: **`3.206870905245`**,
  deviation from C102's `3.206870905` is `2.45e-10`; Nelder–Mead from 32 starts returns the same
  value at the cube-corner direction `(−1,1,1)/√3`; 2·10⁶ random directions give `3.207307899`;
- **closed form** `ρκ + √(ρ²κ² − ρ² + 4)` with `κ = √((5+2√5)/15) = 0.794654472292`, the cosine of the
  icosahedral face's angular radius — the same number to 12 digits;
- the minimisation is **exactly a covering-radius problem and it is proved, not sampled**: `r₊` is
  strictly increasing on its domain, so `min_u max_i r₊(⟨u,x_i⟩) = r₊(ρ·min_u max_i⟨u,x̂_i⟩)`, and for
  `u` in a face triangle, `u = Σλ_k a_k/|Σλ_k a_k|`, `Σλ_k = 1`, `t = max λ_k ≥ 1/3`, gives
  `max_j⟨u,a_j⟩ = ((1−m)t+m)/|Σλ a|` with `m = 1/√5` and `|Σλ a|² = (1−m)Σλ² + m ≤ (1−m)t+m`, so
  `max_j⟨u,a_j⟩ ≥ w/√w ≥ κ` once `w = (1−m)t+m ≥ w(1/3) = (1+2m)/3 = κ²`. Equality only at the 20 face
  centres. Hence the minimum over **all** directions is the face-centre value, exactly.
- `3.178617889` is what the same function gives at `ρ = 2` with the contacts at radius 2 (floor 2,
  discriminant `c²−0`, so `r₊ = 2c`). `3.206871/3.178618 = 1.008888 ≠ 1.045`, because **the problem is
  not scale invariant** — the contact distance stays 2 while `ρ` moves, so `ρ = 2` (distance = radius)
  and `ρ = 2.09` are different problems. Comparing one against the other is the error.

**Two real, minor defects in `Computation/nearest_13th.py`, neither affecting the constant.**
(i) Its `dd` block is labelled "dodecahedral (hole) directions" but yields **12** directions with
`max_i⟨u,x̂_i⟩ = 2/√5 = 0.894427`, i.e. a second icosahedron, not the 20 face centres (which have
`0.794654`). The printed "nearest admissible radius among holes: 4.09" is therefore not a hole value
(the set's own value is `3.637510062`); the true face-centre value `3.206871` *is* the global minimum.
(ii) `CLAIMS.md:3012` describes the minimising direction `(0.934172, 0.356822, 0)` as "an edge-midpoint
direction of the icosahedron (not a face centre)" — it is `(φ, 1/φ, 0)/√3`, a **face centre**
(dodecahedron vertex); its `max_i⟨u,x̂_i⟩ = κ`, and it is exactly where the bound is attained.

**Conclusion unaffected and with room**: against C102's conservative `2·R_cell = 2.955706345` the margin
is `0.251165`; against the true cell circumradius `2·1.045·1.258408572 = 2.630073915` it is `0.576797`.
Status: **constant CONFIRMED, conclusion stands**; two auxiliary/prose defects recorded.

### K15-X-C071 — Main's third `twist_cover.py` (`a34a3ff1`, their C127) fixes both defects and its certificate closes

Blob `a34a3ff104fc9be7d2e358cbbcf4151715c69e0c` at main `4dc1cc9` (supersedes `67d5c973`). Read as
byte copy `Reviews/twist/twist_cover_a34a3ff1.py` and run (exit 0): it adds `2*u_x*q_x` to `Aij`,
uses `violation = |t − ψ| > h` with `h = arccos c`, shrinks endpoints inward by `MARGIN = 1e-30`, and
reduces mod the twist period `2π/5`. **53 proper arcs → 65 pieces → one merged interval
`[0, 2π/5]`, no gaps**, at 60 digits. This is the repair `X-C058`/`corrected_cover.py` specified, and
the two agree (45 raw arcs there because that script keeps the pair list unmerged). So `X-C057`'s
refutation is *of the first two revisions only*, and `C127` now stands.

**One caveat, sound but sloppy.** `L = max(lo, k·PERIOD) − k·PERIOD` folds only the part of the
violation interval `[lo,hi] = [ψ+h, ψ+2π−h]` lying in `[0, 2π]`. Instrumented run: **5 pairs have
`lo < 0`** (down to `−0.550555`) and **5 have `hi > 2π`** (up to `6.833740`), so those pieces are
dropped rather than folded. Dropped pieces are *true* violations, so the emitted arcs remain strict
subsets of the violation sets — the certificate stays **sound** — and the cover still closes with no
gap. But the right operation is reduction mod `2π` before the period split; as written, a different
instance could silently lose coverage. Fix before reuse.

### K15-X-C072 — E's repair of the cell certifier: the five requirements are met, and the old defects are still live in the old files

At experimental tip `f502b9a` (supersedes `d289bef`):

- `Experimental/scripts/rigorous_cell_volume.py` is **byte-identical** to the audited
  `d015a2e1e322853286322ff2c6ec4a5a88f03550` (only the path moved from `Computation/` to
  `Experimental/scripts/`). So `X-C060` (norm) and `X-C061` (boundedness) are **still live in that
  file**, and `Experimental/scripts/certify_region.py` is still `540b4ed1` — `X-C065`'s dropped
  remainder is live there too.
- **New**: `Experimental/scripts/cell_certificate.py` and `certify_region_v2.py` (`ec1eaeda`), which
  name `X-C060`/`X-C061`/`X-C065` explicitly and repair them. Audited line by line:

| requirement (`REVIEW_0608` §5) | repair | verdict |
| --- | --- | --- |
| norm | slack `R·(7/4)·e_i + f_i`, `√3 ≤ 7/4` rational | **sound** |
| radius bootstrap | `R₀ = b_max/(c − (7/4)e_max)`, `b_max` includes `f_i`, `c` a rigorous *lower* bound for `min_u max_i u·n_i` | **sound**: `max_i u·n_i` is 1‑Lipschitz, so `min_mesh − diam` is a lower bound; the mesh diameter (max edge) is a valid covering radius for a spherical triangle — acute gives `L/(2 sin A_max) ≤ L/√3`, obtuse puts the max on an edge at `≤ L/2` |
| boundedness | `Out` bounded iff `0 ∈ int conv{n_i}`, decided by supporting planes of the hull | **DEFECTIVE — see the erratum at the end of this entry.** The idea is right and better than "four normals with a positive dependence" (which rejects the cube), but the implementation's contract is false. |
| inner inclusion | `Inn = {y·n_i' ≤ b_i' − slack}` and `Inn ⊆ Ω ∩ B_R` | **sound** |
| domain coverage | `n = ceil(span/width)`, box width `span/n` exactly, with `assert lo + n*w == hi` | **sound** |

Run: `cell_certificate.py` exits 0, reproduces **both my witnesses** (W1 `y·δn = 8/9 > R·e = 4/5`,
ratio 1.111; W2 the four-vertex unbounded polyhedron **refused**) and its five controls stay exact
(cube `8`, tetrahedron `8/3`, fcc and hcp `4√2`, C5 `5.8980173718`) at enclosure width `1.2e-18`.

Two limits: `spanning_constant` evaluates the rational normals in float and deducts a flat `1e-9`,
which covers the ~`1e-16` conversion error but is a fudge, not an interval computation; and the old
`certify_region.py`/`rigorous_cell_volume.py` are still in the tree, so any number they produce keeps
the old defects — only the `_v2` path is repaired.

**Erratum (same block, after `REVIEW_0653` steering).** The boundedness row above was marked *sound*
on the strength of E's controls. It is not. `origin_interior_certificate` returns `(True, 1, 1)` for
`[(1,0,0),(0,1,0),(0,0,1)]`, whose hull is a triangle in `x+y+z=1` and does not contain the origin at
all; and it returns `(True, 1, 4)` for `[(1,0,0),(0,1,0),(0,0,1),(1,1,1)]`, where **all four points have
`x+y+z = 1`, so `0 ∉ conv` outright** — a full-dimensional hull, not a degenerate one. The cause is not
the `b×c` vs `(b−a)×(c−a)` inconsistency alone (that is a real inconsistency, but replacing it does not
fix the three-point probe: with edge vectors the triangle still returns `(True, 1, 1)`). The cause is
that the routine never checks the hull is **3-dimensional**: for any set whose hull is at most
2-dimensional, some plane contains all the points, every point is on one side of it, and the origin is
strictly inside it, so the "all supporting planes" test is vacuous. Consequence: the **boundedness
decision** in `polytope_volume` is unreliable — a false positive on a set with ≥ 4 vertices would give a
finite volume for an unbounded polyhedron, i.e. the `X-C061` failure mode through a new door. On the
full-dimensional witness it happens to fail safe (`polytope_volume` returns `None`, 0 vertices, and
`certify` would then raise on `None` rather than return a number), so I have **no** demonstrated false
*volume*; what is refuted is the helper's contract and the boundedness guarantee, which `X-C072`'s table
had marked sound. Fix: require `0 ∈ int conv{n_i}` by proving the hull 3-dimensional (a positive
spanning subset with a strictly positive dependence, *plus* the supporting-plane scan with
`(b−a)×(c−a)` normals), and refuse otherwise.

**Full default region, reproduced.** `certify_region_v2.py 110 111 35 36 0.1 --out …` (100 boxes,
~13 min) **exits 0: "CERTIFIED for the whole region: `[5.859536248896, 5.940277014469]`"**, worst box at
`θ = 110.9°, φ = 35.0°`, target `5.763417470` cleared by `+0.096119`. Certificate kept as
`Reviews/twist/reg_default_110_111_35_36.json`. So the repaired path does what it claims end-to-end —
*subject to* `X-C080`: the boundedness gate it relies on is unsound as written, and the `1e-9` in
`spanning_constant` is a fudge, so this run is evidence that the numbers come out consistently, not yet
a proof.

### K15-X-C073 — C's *extended* near-contact scan (two- and three-site displacements) still gives `t* = 0`, and its tiling identity is exact on all 500 rows

C added families `F4` (two sites displaced in opposite directions — the multi-site case their own
`fixture_nonuniform.py` §C does not cover) and `F5` (three sites along independent random directions)
to `nearcontact_scan.py` (`9b41169a` → `9c37b1d4` at comp `926cdb7`), and re-ran. Audited the shipped
`out/nearcontact_scan.json` directly, in exact rational arithmetic:

- **500 rows, family counts `F1` 198, `F2` 14, `F3` 72, `F4` 144, `F5` 72; `t_star` takes the single
  value `0` on every row**, `with_positive_t_star: 0`, density range `[0.620562, 0.739247]`;
- the **tiling identity holds in all 500 rows with no exception**: `Σvol = a³` for `F1`, `F3`, `F4`,
  `F5` and `Σvol = a³·t_ax` for the 14 tetragonal `F2` rows;
- the stored `density` equals `(4π/3)/mean(vols)` in **500/500** rows (to 1e-12).

So the multi-site families — the ones the single-site argument misses — behave exactly like the
single-site ones on these instances, and C's bookkeeping is exact. Scope unchanged: this is finite
evidence, as the module docstring says, and `X-C068`'s reading of `t* = 0` (some cut attains `Σ_U b = 0`
exactly, because `exhaustive_cut_scan` has no `max(0,·)`) applies here too.

### K15-X-C074 — C116's `6/√5` is contradicted by Main's own corrected machinery: its script certifies to `d = 3.00`

After the third `twist_cover.py` (`a34a3ff1`, `X-C071`), `near_contact_band.py` at main `4dc1cc9`
imports the repaired `inner_arcs`. Run as shipped (`Reviews` copy under `.scratch`, exit 0):

```
       d   cover?   coverage
    2.00     True     1.2566      ...     2.80     True     1.2566
    3.00     True     1.2566
largest tested d with a certified cover: 3.00
```

So Main's own script **certifies the two-dodecahedra clash out to `d = 3.00`**, the end of its table —
well beyond `6/√5 = 2.6832816`, which `CLAIMS.md:3561` still states as `PROVED` and "sharp". The
documents are inconsistent with each other: `CLAIMS.md:3340` already records `K15-X-C051` —
"the two-dodecahedra threshold is `3.4555003444`; Main's `6/√5` was wrong (missing term, `C126`)" — as
**adopted by Main**, while `C116` (`:3561`), `Computation/README.md:28` and `CONTINUATION_0308.md:407`
still carry `6/√5`. The certified value is `X-C051`'s `3.4555003444`, reproduced by `X-C064`'s
`certified_threshold.py`; `6/√5` is a lower bound, not the threshold, and "sharp" is wrong in both
directions (it is neither the value nor the limit of the corrected certificate, which reaches `3.4555`).
The consequence for `C114`/Theorem D is favourable: the near-contact band is `1.4555` wide, not
`0.6833` — 2.13× wider than claimed.

Its **module docstring is also stale and self-contradictory**: lines 10–12 still say "the 'closer than
2' set of each pair is a single arc in the twist, the arcs are inflated by EPS", while the `covers()`
docstring ten lines below says the opposite ("Uses `twist_cover.inner_arcs`, i.e. rigorous inner arcs …
An earlier version of this file inflated endpoints OUTWARD by 1e-20, which cannot certify an
all-twists exclusion"). `EPS` is now referenced only in that dead sentence. The prose should be
corrected with the number.

### K15-X-C075 — `ACCEPTED.md:28`'s parenthetical cites the *defective* constant, but its conclusion survives

`ACCEPTED.md:28` justifies citing `C112` (rather than a single-pair argument) with "a one-pair argument
is impossible (`min max_t d² = 8.4223 > 4`)". `8.4223` is the code's `A = |u|²+|q|²`, i.e. exactly the
constant that omits `2u_xq_x` (`X-C057` D1) — so the number is the defective one. Recomputed with the
correct `A` over the same 121 pairs (`A − R ≤ d²(t) ≤ A + R`, `R = √(B²+C²)`):

- `min over pairs of max_t d² = A + R` is **`12.844582472`**, not `8.4223`; no pair has `A + R < 4`, so
  **no single pair clashes for every twist** — the conclusion `ACCEPTED.md` draws is correct;
- `min over pairs of min_t d² = A − R` is **`0.044582472`**, and **37 of 121 pairs** have `A − R < 4`,
  i.e. clash for some twist. That near-zero `0.0446` is why a per-pair argument cannot work and the
  arc cover over all pairs is needed.

So: correct the number in the parenthetical to `12.844582472`, keep the conclusion. Same pattern as
`X-C062` — a display that is right in its verdict and stale in its constant.

### K15-X-C076 — `rho_probe.py` is consistent with C102, and its three test radii straddle the threshold

`Computation/rho_probe.py` at main `4dc1cc9`, run as shipped (1.0 s, exit 0):

```
rho = 2.0127   vol = 5.656696899  (V_dod (rho/2)^3, identical)   vs sqrt32 -0.0028%
rho = 2.09     vol = 6.333804106                                 vs sqrt32 +11.9669%
rho = 2.2      vol = 7.387437359                                 vs sqrt32 +30.5927%
      no extra point in a face-centre direction is admissible AND cuts the cell   (all three)
```

Three points.

1. **The construction is right.** The 20 directions in `dodeca_dir()` are the dodecahedron vertices
   (4 of type `(0,±1/φ,±φ)` plus 16 of type `(±1/φ,±φ,0)`, `(±φ,0,±1/φ)`), i.e. the icosahedron's
   face centres — the correct set, by `X-C070` the very set where the nearest admissible radius is
   minimised. The half-spaces are `⟨p,x⟩ ≤ |p|²/2` with the extra centre at its own radius, and the
   base cell `⟨x_i,x⟩ ≤ ρ²/2` is the dodecahedron of inradius `ρ/2`, not the ball — correct.
2. **The negative output is exactly what C102 predicts**: along a face centre the smallest admissible
   radius is `3.206870905`, and any cutter needs `|p| < 2·R_cell = 2.63 < 3.2069`, so no `r` can be
   both admissible and cutting, at any `ρ` in the swept range.
3. **The three radii straddle the crossing.** `V_dod(ρ/2)³ = √32` at `ρ = 2.0127…`, and at
   `ρ = 2.0127` the cell is **`0.0028%` below** `√32`, while at `2.09` it is `11.97%` above. So the
   probe's first row is not a "singleton works" case at all — it is the knife edge where the singleton
   *fails* — and C102's redundancy statement is load-bearing precisely there. Main's `C101` text reads
   as if all three radii are above target; only two are.

### K15-X-C077 — `constants_check.py` ("every ledger constant re-derived") does not re-derive C102's constant

Parsed all **143** `chk(...)` calls in `Computation/constants_check.py` at main `4dc1cc9` and compared the
`got` and `want` arguments textually. **Two are self-comparisons** — identical expressions, so they
cannot fail:

- `chk("  theta_min (deg) at rho=%s" % rho, degrees(acos(c)), degrees(acos(c)))` (inside the `rho` loop);
- `chk("nearest admissible 13th centre at rho=2.09", 3.206870905, 3.206870905, tol=1e-9)` — and this is
  the only ledger line for `C102`'s constant, which is the value that matters for `C101` case (B).

A third is a semantic self-comparison with a mislabelled name:
`chk("2.09 is below the 13-point threshold", mpf('2.09'), 2.09)` compares `2.09` with `2.09`; it does
**not** test `2.09 < 2.091145548…`, and would pass at any radius.

So `run_all_checks.py`'s row "constants: every ledger constant re-derived — PASS" is true of 140 of
143 entries but not of `C102`'s. The value is nevertheless **correct** (`X-C070`, an independent
mpmath recomputation plus a proof of the covering step), so this is a gap in the regression net, not a
wrong number: if `nearest_13th.py` regressed, `constants_check.py` would not notice. The fix is a
one-line `chk` against `nearest_13th.min_admissible`, or against the closed form
`ρκ + √(ρ²κ²−ρ²+4)` used in `nearest_13th_indep.py`.

### K15-X-C078 — why my cover has 45 arcs and Main's has "53 proper": 14 pairs are tangential with zero-width arcs

`corrected_cover.arcs()` returns **45** raw arcs where Main's repaired `inner_arcs` reports **53**
proper arcs. Reconciled exactly, over the same 121 pairs at `d = 2`:

| class | count | note |
| --- | --- | --- |
| never closer than 2 (`A − R > 4`) | 69 (Main: 68) | no arc |
| **tangential**: `min_t d² = A − R = 4` exactly | **14** | zero-width arcs; `c = −1`, `half = π − acos(−1) = 0`; contribute nothing |
| genuinely violating (`A − R < 4 < A + R`) | **39** | these carry the cover; folding them mod `2π/5` gives the 45 raw pieces |

`68 + 53 = 121` and `69 + 39 + 13 = 121`: Main's "proper" count includes the 14 tangential pairs
(one of which my 60-digit code classifies as "empty" because `A − R` comes out `4 + 10⁻⁵⁸`). Both
implementations therefore agree on the *set* that matters — 39 pairs, merged to `[0, 2π/5]` — and the
counts differ only by zero-width bookkeeping.

Two things worth stating because they are easy to lose: the certificate is carried by **39 of 121**
pairs, and **14 pairs are tangent at distance exactly 2** for exactly one twist each. A strict-inequality
treatment would have to exclude those 14 explicitly; the inner-arc formulation does it automatically,
since their arcs are empty after the margin. The cover does not depend on any of them.

**A 1-count difference remains**: `A − R = 4` for 14 pairs, and at 60 digits one of them computes as
`4 + 1e-58` and falls into "empty". It changes no arc, but it shows the classification is exactly at a
numerical boundary for those pairs — the reason Main's `1e-30` inner margin, not a `1e-58` epsilon, is
the right device.

### K15-X-C079 — E's new interval trigonometry is sound; and the default region does not contain E's own C5 fixture

**Trig.** `cell_certificate._sincos` is `rational_interval.sin_cos_iv_of_pi_multiple(mult, terms=24,
pi_terms=32)`, and `_range_of` takes the hull of the endpoints plus every quarter-turn inside the box —
no monotonicity assumption. Tested the enclosure directly: **344 rational multiples of π in `[−2, 2]`**
(denominators 5, 10, 20, 50), exact values inside the returned intervals in **344/344** cases, maximum
interval width **`1.18e-37`**. So the same verdict as `X-C067` for the old module: the trigonometric
enclosure is exact rational arithmetic and sound; the flat `1e-9` in `spanning_constant` (`X-C072`) is
the only non-interval step in the chain.

**Scope of the default region.** The C5 control in `cell_certificate.py` is built at
`tsin = √55/8`, `tcos = −3/8`, i.e. **θ = 112.02°**, and certifies `5.8980173718`. The default region of
`certify_region_v2.py` is **θ ∈ [110°, 111°]**, which **does not contain 112.02°**: the region certifies
a *different* one-parameter family (there `z = −2cos θ ∈ [0.68, 0.70]`, radius `2 sin θ ∈ [1.879,
1.884]`, volume `[5.861827, 5.940277]`), not a neighbourhood of the C5 fixture. Both are above the
`5.763417470` target, so nothing false is claimed — but "CERTIFIED for the whole region" should not be
read as "certified around C5", and the region and the control are two different objects.

### K15-X-C080 — `origin_interior_certificate`'s contract is false, and `spanning_constant` is not rigorous

1. **The helper.** Reproduced exactly:
   `origin_interior_certificate([(1,0,0),(0,1,0),(0,0,1)])` → `(True, 1, 1)`, while the hull is the
   triangle in `x+y+z=1` and does not contain the origin. **Stronger**: on
   `[(1,0,0),(0,1,0),(0,0,1),(1,1,1)]` it returns `(True, 1, 4)` although all four points have
   `x+y+z = 1`, so `0 ∉ conv` — and this hull *is* 3-dimensional, so the failure is not only the
   degenerate case. The `b×c` normals (instead of `(b−a)×(c−a)`) are a genuine inconsistency, but they
   are **not** the operative cause of the three-point probe: with edge-vector normals the answer is
   still `(True, 1, 1)`. The operative cause is the missing **3-dimensionality** check.
2. **Consequence, stated exactly.** The boundedness decision in `polytope_volume` (and hence in
   `certify`) rests on this helper. On the full-dimensional witness the failure is *safe* —
   `polytope_volume` returns `None` with 0 vertices and `certify` would raise — so I have no
   demonstrated false volume. What is refuted is the guarantee itself; a false positive on a normal set
   with ≥ 4 vertices would yield a finite volume for an unbounded cell, which is `X-C061` again.
3. **The radius path is not rigorous either.** `spanning_constant` evaluates the rational normals in
   `numpy` floats and returns `F(vals.min()) − F(diam) − 1e-9`: the LaTeX-side argument (1‑Lipschitz,
   mesh diameter as covering radius) is correct, but the float error is not *bounded*, it is assumed
   below `1e-9`. So `R₀`, and with it the outer polytope's truncation, is not a certified bound. The
   fix is to do the mesh evaluation in `Iv`/`Fraction` (the mesh can be generated with rational
   directions from the icosahedral subdivision, or the `min` can be bounded below on each mesh triangle
   by its vertices minus the diameter, evaluated exactly), and to drop the `1e-9`.

**Status of `X-C072`**: its table row on boundedness is **withdrawn** (see the erratum there). The other
four rows stand: the `√3` slack, the inner inclusion, the exact domain tiling and the a-priori-radius
*formula* are correct as algebra — the defect is in the two inputs to that formula (the helper's verdict
and `c`'s lower bound).

### K15-X-C081 — `C125(b)` refutes exact-`F` monotonicity, not the nested infimum; `C124`'s `deg ≤ 12` needs its radius

**(a) The classes are nested.** If `C122`'s `c_F` is the minimum volume of a convex body containing
`B(0,1)` with **at most** `F` faces, then `c_F` is **non-increasing** in `F` by inclusion, and nothing can
refute it. `C125(b)`'s table — truncated octahedron, 14 faces, `6.158403`, versus icosahedron, 20 faces,
`5.054056` — shows only that the minimum over **exactly** `F` faces is *not* monotone (it can rise from
`F = 14` to `F = 20`). That is true and worth recording, but it is a different statement: a
larger-volume 14-face example cannot refute a non-increasing infimum over nested "at most `F`" classes.
So `C125`'s obstruction rests on **(a)** the seven unproved values of `F` and **(c)** the equal-cap
estimate, not on (b). This is the same conflation as my own §7/X-C066, corrected in `REVIEW` §21 — the
error is mine as much as Main's, and it points the same way: `c_20` (at most 20) is what `C122` needs,
and it is not available.

**(b) `C124`'s `deg ≤ 12`.** `CLAIMS.md` uses "`S_ε ⊆ matched ∪ N(matched)`, and with `deg ≤ 12`,
`|S_ε ∩ B| ≤ 26|M ∩ B|`" — so it needs a per-point bound of 12 on neighbours. The steering's witness,
the origin plus the 18 vectors in `{−2,0,2}³` of squared norm 4 or 8, is a fragment of the fcc lattice:
I verified **19 points, minimum pairwise distance exactly 2, circumradius `2√2 = 2.828427`**. That
refutes "at most 12 points in a ball of radius `2√2`", but **it does not refute `deg ≤ 12`**: in that
fragment the origin has degree `6` and a corner point has degree `5`. So, read as written, `deg ≤ 12` is
not touched by this witness; what it shows is that the *ball count* version of the bound fails at large
radius, i.e. `C124` cannot replace `deg ≤ 12` by a counting argument at that scale. Whether `deg ≤ 12`
itself holds depends on the radius over which neighbours are counted, which `C124` does not state at the
place I can see; the safe statement is that it needs the kissing-number-12 theorem (Schütte–van der
Corput) applied to a *sphere of contacts*, and that substituting a finite-ball count is invalid.

### K15-X-C082 — a correct replacement for the boundedness gate (exact, rational, no plane scan)

`Reviews/twist/fixed_boundedness.py` (exit 0) decides `{y : y·n_i ≤ d_i}` bounded **exactly** and without
E's plane scan. Criterion: the recession cone `R = {d : d·n_i ≤ 0 ∀i}` is `{0}`; `R` is a polyhedral cone,
so if `R ≠ {0}` it contains a nonzero candidate among `±n_i` (when `R` is a halfspace or a line) or
`±(n_i × n_j)` (an extreme ray is the intersection of two of the planes). Rational arithmetic, finite
check.

| case | verdict |
| --- | --- |
| `[(1,0,0),(0,1,0),(0,0,1)]` (triangle, origin outside) | **False** — E's helper says True |
| `[(1,0,0),(0,1,0),(0,0,1),(1,1,1)]` (all `x+y+z=1`) | **False** — E's helper says True |
| tetra `e1,e2,e3,(−1,−1,−1)` | True |
| cube's six normals | True, and `{|y_i| ≤ 1}` has 8 vertices |
| octahedron's six normals | True |
| unbounded tetra `{y·n_i ≤ 1}` | **refused**, with the ray `(0,−1,0)` |

This is the fix to file against `X-C080`: replace the gate, keep E's `√3`-slack and inner inclusion, and
make `spanning_constant` rational as `X-C080` §3 says.

### K15-X-C083 — `C124`'s `deg ≤ 12` is FALSE in the `(2+ε)`-graph: an exact 17-neighbour witness at `ε = 0.6832816`

`C124` writes: `M` a maximal matching of the **`(2+ε)`-graph**, `S_ε ⊆ matched ∪ N(matched)`, "and with
`deg ≤ 12`, `|S_ε ∩ B| ≤ 26|M ∩ B|`". The domination step uses neighbourhoods in the `(2+ε)`-graph, so
`deg` must be the degree there — and that degree is **not** bounded by 12 once `ε > 0`. Exact witness
(`Reviews/twist/deg13_witness.json`, rationals with denominator 100, greedy construction, seed 11):

- **17 points**, all rational, minimum pairwise **squared** distance `4.1129 ≥ 4`, maximum modulus
  `2.6647889222 < 2.6832816 = 2 + 0.6832816`;
- together with the origin they form a 2-separated set (every `|q| ≥ 2.65`), and the origin has **17
  neighbours at distance `≤ 2.6648 ≤ 2+ε`**.

So `deg ≥ 17 > 12` at the band end `ε = 0.6832816`, and the constant `26` is wrong (the same domination
argument gives `2 + 2·deg ≥ 36` here, and without a bound on `deg` at all it gives nothing uniform). This
is a refutation of a **step**, not of `C124`'s conclusion: the conclusion `ρ_ε = 0 ⟹ S_ε` has density
zero needs only that the multiplier be finite, and a shell-degree bound of the form
`deg_ε ≤ C(1+ε/2)²` (kissing in a shell, not the kissing number 12) would still give it. What cannot be
used is `12`, or the number `26`. `C124` is marked `PROVED`; this step needs replacing before that
stand.

Also note the safe direction: 12 *is* the bound for neighbours at distance **exactly** 2 on a sphere
(kissing number, Schütte–van der Corput), which is why `C112`-type contact arguments are unaffected.

### K15-X-C084 — ERRATUM to `X-C075`: `C128`'s one-pair argument is VALID; my "no single pair" was computed on the wrong twist space

`X-C075` above says "no single pair clashes for every twist — the conclusion `ACCEPTED.md` draws is
correct". **That is wrong**, and `C128` is right. My statement used `A − R ≤ d² ≤ A + R` over the whole
`360°` twist circle; the physical twist space is `R/(2π/5)`, a circle of circumference **`72°`**, because
a `72°` rotation about the vertex axis maps the icosahedron to itself. A violation set that is an arc of
length `> 72°` meets **every** coset, so one pair suffices.

Checked exactly for the pair with `A = 6.444582472`, `R = 6.4` (in my `build()` ordering it is
`A[5]`, `Q[10]`, not `A[1]`, `Q[8]`; the pair is identified by its invariants):

- `c = (4−A)/R = −(3−√5)/2 = −0.381966011250`, `h = arccos c = 112.4555152°`, `|T| = 2π − 2h =
  135.0889696° > 72°` ✓ — so `T` meets every coset;
- direct maximisation, `max over τ ∈ [0°,72°) of min over k∈{0..4} d²(τ + 72k°)` =
  **`1.266873708`** at `τ = 0`, matching `C128` to `1e-9` — and `1.2669 < 4`, i.e. this one pair is
  closer than `2` at some representative of every physical twist.

So `C128`'s three-line proof stands and is the better certificate of record. What remains true from
`X-C075`: `ACCEPTED.md:28`'s number `8.4223` is the defective `A` (the true `A + R` is `12.844582472`),
**and** its parenthetical conclusion — "a one-pair argument is impossible" — is also wrong, for the
independent reason that it maximises over `360°` instead of `72°`. Both halves of that parenthetical
should go: the correct pair certificate is `max_τ min_k d² = 1.266873708 < 4`.
