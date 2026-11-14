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
