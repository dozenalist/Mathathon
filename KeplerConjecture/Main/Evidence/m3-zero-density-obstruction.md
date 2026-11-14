# A bandwidth budget for sharp Cohn–Elkies certificates, and the contact-shell degeneracy

**Member m3, swarm smwfyzz1k, direction d8. Revision 2.** Files: `scripts/budget.py`,
`scripts/budget.out` (supersedes `scripts/shells_and_zeros.*` of revision 1).

**Summary.** The main new content is *quantitative*: an explicit budget for how many shell
conditions a Cohn–Elkies certificate of given bandwidth (or of given support radius) can satisfy.
The budget is
$$\operatorname{supp}\hat f\subseteq B(0,R)\ \Longrightarrow\ R \;\ge\;
\frac{K\log 2 - \tfrac12\log\!\big(\|\hat f\|_1/f(0)\big)}{2\pi\, r_K}\tag{B}$$
whenever $f$ vanishes at the first $K$ shell radii $r_1<\dots<r_K$ of the lattice; with the sharp
classical zero-density constant the corresponding statement is $R\ge K/(2r_K)-o(1)$. For the FCC
lattice this gives $R\ge 0.3489,\,1.0665,\,3.3414,\,10.564,\,33.401$ for $K=10,10^2,10^3,10^4,10^5$
and a shell budget of $K\lesssim 89.6\,R^2$ (elementary) or $K\lesssim 4.4\,R^2$ (sharp constant);
the dual form constrains the support radius against the dual shells. The qualitative consequence —
no band-limited and no compactly supported certificate is sharp in $d\ge2$ — is *not* new: it is
already accepted from m4/d1 (finding f10) and the present derivation is an independent version of
the same Jensen argument. What is new beyond (B) is Theorem 7 below, the quantitative *contact-shell
degeneracy*, which replaces a false proposition of revision 1.

---

## 0. Revision note: retracted and corrected items

**Retraction.** Revision 1 contained a "Proposition 4.7" asserting that a sharp certificate is never
$C^2$ with admissible Laplacian, hence never Schwartz, with the consequences "no sharp certificate is
a Schwartz function" and "the $d=8,24$ magic functions have non-summable second-moment data". **That
proposition and both consequences are false and are retracted.** The error was the passage from

> $f(\lambda)=0$ is a maximum of $f$ on $\{\|x\|\ge1\}$, hence $\operatorname{Hess}f(\lambda)\preceq0$,

which is invalid at a point of the *contact shell* $\|\lambda\|=1$: there the admissible set is the
exterior of a ball, so for $h$ with $\langle h,\lambda\rangle\ge0$ one only gets
$\varphi(t):=f(\lambda+th)\le \varphi(0)$ for $t\ge0$, hence $\varphi'(0)\le0$, and nothing about
$\varphi''(0)$ (e.g. $\varphi(t)=-t+t^2$). Evenness of the Hessian quadratic form does not repair
this: what is missing is the behaviour at $t<0$, i.e. inside the ball, not the direction $-h$. The
inference $\operatorname{Hess}f(\lambda)\preceq 0$ is valid precisely for $\|\lambda\|>1$, where
$f\le0$ holds in a whole neighbourhood of $\lambda$.

**Decisive counterexample** (as pointed out in the referee report): Viazovska's function $g$ for
$d=8$ (M. Viazovska, *The sphere packing problem in dimension 8*, Ann. of Math. 185 (2017),
arXiv:1603.04246, Thm 3) is $C^\infty$ (indeed Schwartz), satisfies $g\le0$ for $\|x\|\ge\sqrt2$,
$\hat g\ge0$, $g(0)=\hat g(0)=1$, is sharp at the unimodular self-dual lattice $\Lambda_8$, and by the
equality case vanishes on $\Lambda_8\setminus\{0\}$ together with $\hat g$. Then
$\sum_{\lambda\in\Lambda_8}\Delta g(\lambda)=-4\pi^2\sum_{\mu}\|\mu\|^2\hat g(\mu)=0$ while
$\Delta g(0)=-4\pi^2\int\|y\|^2\hat g(y)\,dy<0$; so $\Delta g>0$ somewhere on the contact shell, i.e.
on some of the $240$ minimal vectors. Revision 1's proposition would have forced $g\equiv0$. The
correct repair is Theorem 7, and it is the *opposite* in spirit: a positive structural statement, not
a nonexistence theorem.

**Credit.** That the FCC first shell lies on $\|x\|=1$, where the sign hypothesis degenerates so that
"double zeros in $s=\|x\|^2$" hold only at shells of radius $>1$, was recorded (independently, and
correctly) by member m7 in direction d2 and accepted there. Theorem 7 is the quantitative form of
that observation (a signed sum over the contact shell), and I make no claim of priority for the
qualitative remark.

**Second correction.** Revision 1 also asserted in its verification table "at most $\approx 90R^2$
FCC shells" for bandwidth $R$ without showing the derivation. Section 5 now gives the derivation, the
crossover radius $r_*=(12/11)cR$ and the budget $K_*=(12/11)c^2R^2$, so that every number is
recomputable: the elementary Jensen constant $c=2\pi/\log2=9.065$ gives $r_*=9.889R$ and
$K_*=89.6R^2$, and the sharp Carlson constant $c=2$ gives $r_*=2.182R$ and $K_*=4.4R^2$. The value
$\approx0.92R^2$ quoted in the referee report equals $(11/12)R^2$, i.e. it corresponds to the crossover
radius being exactly $R$ (constant $c=11/12$); that is what one gets if the vanishing radius is
identified with the bandwidth, which is not a consequence of any zero-counting inequality (a
band-limited function of bandwidth $R$ can have zeros at arbitrarily large radii, at density $2R$ per
unit length, as $\sin(2\pi Rt)$ shows). Section 5 states both constants side by side; I have kept the
number that the derivation gives rather than the smaller one, since the smaller one is not proved.

---

## 1. What is new here, and what is not

Used as inputs (all previously established in this swarm; reproved below only for completeness, with
no priority claimed):

* **equality case** ($f=0$ on $L\setminus\{0\}$ and $\hat f=0$ on $L^*\setminus\{0\}$ for a sharp
  certificate): m2/d6, m4/d1 (Thm 2.1), m7/d2; also invoked in the problem statement's starting
  points;
* **radialisation** is WLOG (standard, Lemma 3.2);
* **exact FCC/BCC shell arithmetic** and the density $11/12$: m7/d2 (finding f6), m4/d1 (finding f2);
* **qualitative no-band-limited-certificate**: m4/d1 (finding f10), where the same Jensen argument is
  given, with explicit credit to this direction;
* **contact-shell degeneracy, qualitative**: m7/d2 and m4/d1.

New in this revision:

* **(B)** and its dual (support-radius) form, with the exact additive constants (Theorem 4.1, 4.2);
* the crossover analysis, i.e. the *shell budget* as a function of $R$ and of the shell density, with
  both the elementary and the sharp zero-density constant, and the explicit verification table (§5);
* the reading of $d=1$ as the exact borderline of the mechanism (§6);
* **Theorem 7**, the quantitative contact-shell degeneracy (§7), repairing revision 1.

---

## 2. Conventions

* Lattices $L\subset\mathbb R^d$, covolume $\det L$, dual $L^*$; always scaled so that the minimal
  distance is $\ge1$. FCC: $L=D_3/\sqrt2$, minimal distance $1$, $\det L=1/\sqrt2$, centre density
  $\sqrt2$.
* $\hat f(y)=\int f(x)e^{-2\pi i\langle x,y\rangle}dx$; $f$ **admissible**: continuous with
  $|f(x)|,|\hat f(x)|\le C(1+\|x\|)^{-d-\delta}$ (so Poisson summation and Fourier inversion hold in
  their absolutely convergent form).
* **Cohn–Elkies theorem** (Cohn–Elkies, *New bounds on sphere packings I*, Ann. of Math. 157 (2003),
  Thm 3, in the normalisation fixed by the problem): if $f$ is admissible, $\hat f\ge0$ and
  $f\le0$ off the unit ball, then every packing of minimal distance $\ge1$ has centre density
  $\le A(f)=f(0)/\hat f(0)$. $f$ is **sharp at $L$** if $A(f)=1/\det L$.
* Shell radii of $L$: the numbers $\|\lambda\|$, $\lambda\in L\setminus\{0\}$;
  $N_L(r)=\#\{\text{shell radii}\le r\}$; **contact shell**: the shell of radius $1$.

---

## 3. Inputs

**Lemma 3.1 (equality case).** *Let $f$ be admissible, $\hat f\ge0$, $f\le0$ off the unit ball,
$\hat f(0)>0$, and $A(f)=1/\det L$ for a lattice $L$ of minimal distance $\ge1$. Then $f(\lambda)=0$
for $\lambda\in L\setminus\{0\}$ and $\hat f(\mu)=0$ for $\mu\in L^*\setminus\{0\}$.*

*Proof.* Poisson at $0$: $\sum_{\lambda\in L}f(\lambda)=\det(L)^{-1}\sum_{\mu\in L^*}\hat f(\mu)$.
The left side is $\le f(0)$ (all $\lambda\ne0$ have $\|\lambda\|\ge1$), the right side is
$\ge\hat f(0)/\det L=f(0)$. So both are equalities and each summand of
$\sum_{\lambda\ne0}f(\lambda)\le0$ and of $\sum_{\mu\ne0}\hat f(\mu)\ge0$ vanishes. $\square$

**Lemma 3.2 (radialisation).** *Let $S$ be rotation-invariant and $f$ admissible with $\hat f\ge0$ and
$f\le0$ on $S$. Then $\bar f(x)=\int_{SO(d)}f(\sigma x)d\sigma$ is admissible and radial, $\hat{\bar
f}\ge0$, $\bar f\le0$ on $S$, $\bar f(0)=f(0)$, $\hat{\bar f}(0)=\hat f(0)$, and
$\operatorname{supp}\hat f\subseteq B(0,R)\Rightarrow\operatorname{supp}\hat{\bar
f}\subseteq B(0,R)$, $\operatorname{supp}f\subseteq B(0,S_0)\Rightarrow\operatorname{supp}\bar
f\subseteq B(0,S_0)$.*

*Proof.* $\hat{\bar f}(y)=\int_{SO(d)}\hat f(\sigma^{-1}y)d\sigma$ by Fubini; for fixed $y$ this
averages the nonnegative function $\hat f$ over the sphere of radius $\|y\|$, so it is $\ge0$ and
supported in $B(0,R)$. The remaining claims are immediate. $\square$

**Warning (used below).** Radialisation does **not** preserve the property "$\hat f$ vanishes on
$L^*\setminus\{0\}$" ($\sigma^{-1}\mu\notin L^*$ in general). It does preserve *radiality* of $\hat
f$, and the equality case is applied only *after* radialising, to the radialised function, which is
again sharp.

---

## 4. The budget theorem

**Theorem 4.1 (band-limited certificates).** *Let $d\ge2$, $L$ a lattice of minimal distance $\ge1$
with $N_L(r)/r\to\infty$, and $0<R<\infty$. Then there is no admissible $f$ with
$\operatorname{supp}\hat f\subseteq B(0,R)$, $\hat f\ge0$, $f\le0$ off the unit ball and
$A(f)=1/\det L$. Quantitatively, if such an $f$ vanishes at the first $K$ shell radii, then* (B)
*holds.*

*Proof.* By Lemma 3.2, $\bar f$ is radial with $\operatorname{supp}\hat{\bar f}\subseteq B(0,R)$,
$\hat{\bar f}\ge0$, $\bar f\le0$ off the unit ball, $A(\bar f)=1/\det L$; by Lemma 3.1 (applied to
$\bar f$), $\bar f=0$ on $L\setminus\{0\}$. Fix a unit vector $u$. Since $\hat{\bar f}\in L^1$ is
supported in $B(0,R)$,
$$F(z):=\bar f(zu)=\int_{B(0,R)}\hat{\bar f}(y)e^{2\pi i\langle zu,y\rangle}dy$$
is entire, $|F(z)|\le\|\hat{\bar f}\|_1e^{2\pi R|\operatorname{Im}z|}$, $F(0)=f(0)\ne0$, and by
radiality $F(\pm r_j)=0$ for $j\le K$, i.e. $2K$ distinct zeros. Jensen
($n(\rho)\log(R_0/\rho)\le\log M(R_0)-\log|F(0)|$) with $\rho=r_K$, $R_0=2r_K$ gives
$2K\log2\le n(r_K)\log2\le4\pi Rr_K+\log(\|\hat{\bar f}\|_1/f(0))$; since
$\|\hat{\bar f}\|_1=\|\hat f\|_1$, this is (B). Finally $N_L(r_K)=K$ and $N_L(r)/r\to\infty$, so the
right side of (B) is unbounded in $K$ and must exceed the fixed $R$: contradiction. $\square$

**Theorem 4.2 (compactly supported certificates, dual form).** *Let $d\ge2$, $L$ a lattice of minimal
distance $\ge1$ with $N_{L^*}(r)/r\to\infty$, and $0<S_0<\infty$. Then there is no admissible $f$ with
$\operatorname{supp}f\subseteq B(0,S_0)$, $\hat f\ge0$, $f\le0$ off the unit ball and
$A(f)=1/\det L$. Quantitatively, if $f$ vanishes at the first $K$ dual shell radii
$s_1<\dots<s_K$, then*
$$S_0\;\ge\;\frac{K\log2-\tfrac12\log\!\big(\|f\|_1/|\hat f(0)|\big)}{2\pi\,s_K}.\tag{4.2}$$

*Proof.* Apply Lemma 3.2 to get the radial $\bar f$ (compactly supported, same $A$), Lemma 3.1 to get
$\hat{\bar f}=0$ on $L^*\setminus\{0\}$; $\hat{\bar f}$ is radial, hence vanishes at $\pm s_j$. Since
$\bar f$ is supported in $B(0,S_0)$ and admissible, $G(z):=\hat{\bar f}(zu)=\int_{B(0,S_0)}\bar
f(x)e^{-2\pi i\langle zu,x\rangle}dx$ is entire with $|G(z)|\le\|\bar f\|_1e^{2\pi S_0|z|}$ and
$2K$ prescribed zeros; Jensen as above gives (4.2). $\square$

**Corollary 4.3 (qualitative form).** *In $d\ge2$, no band-limited and no compactly supported
certificate is sharp at any lattice with superlinear shell growth (in particular at FCC, where
$N_L(r)\sim\frac{11}{12}r^2$).* This is the statement already obtained by m4/d1 (finding f10).

**Remark 4.4 (the shell hypothesis is automatic in the cases of interest).** $N_L(r)/r\to\infty$
holds for: (i) $L=\mathbb Z^d$, $d\ge4$ — by Lagrange's four-square theorem every $\sqrt m$ is a shell
radius, so $N_L(r)=\lfloor r^2\rfloor$; (ii) FCC and its dual — $N(r)=\frac{11}{12}r^2+o(r^2)$
(shell arithmetic of m7/d2 and m4/d1, re-verified exactly in §9, parts (A)–(B)); (iii) any lattice with integral squared-norm form
$Q$ — the standard representation-number bound $r_Q(m)=O_\varepsilon(m^{\frac d2-1+\varepsilon})$
gives $N_L(r)\ge c\,r^{2-\varepsilon}$ for every $\varepsilon>0$. The hypothesis fails exactly in
$d=1$ (§6).

---

## 5. The numbers: crossover radius and shell budget

Write $c$ for the constant in the zero-counting inequality $N_L(r)\le c\,R\,r+O(1)$ that one is
willing to use. Two choices:

* **elementary** (Jensen only, as in Theorem 4.1): $c=2\pi/\log2=9.0647$;
* **sharp** (classical zero density for entire functions of exponential type $\tau$, which gives at
  most $\tau/\pi$ zeros per unit length; Carlson, Beurling; see Levin, *Lectures on Entire
  Functions*, Ch. V): $c=2$, and it is attained by $\sin(2\pi Rt)$ (script part (G)).

With $N_L(r)\sim\frac{11}{12}r^2$ the budget $K\approx\frac{11}{12}r^2$ meets $K\approx cRr$ at
$$r_*=\frac{12}{11}cR,\qquad K_*=\frac{11}{12}r_*^2=\frac{12}{11}c^2R^2,\tag{5.2}$$
i.e.

| constant | $c$ | crossover radius $r_*$ | shell budget $K_*$ |
|---|---|---|---|
| elementary (Jensen) | $2\pi/\log2=9.0647$ | $9.889\,R$ | $89.6\,R^2$ |
| sharp (Carlson) | $2$ | $2.182\,R$ | $4.4\,R^2$ |

The figure $\approx0.92\,R^2$ corresponds to $c=11/12$, i.e. to a crossover radius $r_*=R$ exactly:
it is what one gets if the vanishing radius is identified with the bandwidth. No zero-counting
inequality gives so small a constant: the sharp (Carlson) constant is $c=2$, giving $r_*=2.182R$ and
$K_*=4.4R^2$, and the elementary Jensen constant is $c=9.065$, giving $r_*=9.889R$ and $K_*=89.6R^2$.
The derivation (5.2) is printed by the script, part (C), so that every number in the three-column
table is recomputable from the formula.

Exact evaluation of (B) at the $K$-th FCC shell (script part (D); $m_K$ = $K$-th non-empty squared
radius):

| $K$ | $m_K$ | $\sqrt{m_K}$ | $R\ \ge\ K\log2/(2\pi\sqrt{m_K})$ |
|---|---|---|---|
| 10 | 10 | 3.162 | 0.3489 |
| $10^2$ | 107 | 10.344 | 1.0665 |
| $10^3$ | 1090 | 33.015 | 3.3414 |
| $10^4$ | 10905 | 104.427 | 10.5641 |
| $10^5$ | 109087 | 330.283 | 33.4010 |

Dual form (4.2) (script part (E)): $S_0\ge0.3489,\,1.0640,\,3.3414$ for $K=10,10^2,10^3$ dual shells.

Since sharpness forces *all* shell conditions (Lemma 3.1), (B) shows that a sharp certificate must
have unbounded Fourier support and unbounded support, and it quantifies the cost: the $K$-th shell
condition costs bandwidth at least $K\log2/(2\pi r_K)\approx 0.11\sqrt K$.

---

## 6. $d=1$ is the exact borderline

For $L=\mathbb Z$ the shell radii are $1,2,3,\dots$, so $N_{\mathbb Z}(r)=\lfloor r\rfloor$ is
*linear*, and (B) is compatible with bounded $R$: $1\le 2\pi/\log2=9.065$ per unit radius. Indeed the
triangle $f(t)=(1-|t|)_+$ is admissible, compactly supported, $\hat f=\operatorname{sinc}^2\ge0$,
$f\le0$ off the unit ball, $f(0)/\hat f(0)=1=1/\det\mathbb Z$: sharp, with $\hat f$ vanishing exactly
on the dual shell set $\mathbb Z\setminus\{0\}$ (Lemma 3.1). So the mechanism of §4 is unavailable
exactly in dimension $1$: the growth of $N_L$ is $r^1$ instead of $r^d$. (In $d\ge2$ the shell set is
quadratically dense: for FCC and for its dual, $N(r)=\frac{11}{12}r^2+o(r^2)$.) Note that the
sharpness of the plain CE program in $d=2$ is, as m4/d1 (finding f2) records, a *conjecture* (CE
Conjectures 7.3/8.1), not a theorem; §4 then predicts only that a sharp $d=2$ certificate, if it
exists, cannot be band-limited or compactly supported.

---

## 7. Theorem 7: the contact-shell degeneracy (repair of revision 1's Proposition 4.7)

**Theorem 7.** *Let $f$ be admissible and $C^2$ with $\Delta f$ admissible, $\hat f\ge0$, $f\le0$ for
$\|x\|\ge1$, and $f$ sharp at a lattice $L$ of minimal distance $1$ ($A(f)=1/\det L$). Then*
$$\sum_{\substack{\lambda\in L\\ \|\lambda\|=1}}\Delta f(\lambda)\;=\;-\Delta f(0)-\!\!\sum_{\substack{\lambda\in L\\ \|\lambda\|>1}}\!\!\Delta f(\lambda)\;\ge\;-\Delta f(0)\;=\;4\pi^2\!\int_{\mathbb R^d}\|y\|^2\hat f(y)\,dy\;>\;0 .$$
*In particular some contact-shell lattice point $\lambda$ satisfies $\Delta f(\lambda)>0$; in $d=3$ at
FCC there are twelve such points available, in $d=8$ at $\Lambda_8$ two hundred and forty.*

*Proof.*
(i) **Off the contact shell.** If $\lambda\in L$, $\|\lambda\|>1$, then $\lambda$ lies in the open set
$\{\|x\|>1\}$ on which $f\le0$; since $f(\lambda)=0$ (Lemma 3.1), $\lambda$ is a local maximum of
$f$, so $\operatorname{Hess}f(\lambda)\preceq0$ and $\Delta f(\lambda)\le0$.
(ii) **At the origin.** $\Delta f(0)=\int(-4\pi^2\|y\|^2)\hat f(y)dy=-4\pi^2\int\|y\|^2\hat f(y)dy$ by
Fourier inversion for the admissible function $\Delta f$; the integrand is $\ge0$, $\hat f$ is
continuous and $\hat f(0)>0$, so the integral is $>0$ and $\Delta f(0)<0$ (strictly: $\hat f>0$ near
$0$).
(iii) **Poisson for $\Delta f$.** $\sum_{\lambda\in L}\Delta f(\lambda)
=\det(L)^{-1}\sum_{\mu\in L^*}\widehat{\Delta f}(\mu)
=-(4\pi^2/\det L)\sum_{\mu\in L^*}\|\mu\|^2\hat f(\mu)=0$, because $\hat f$ vanishes on
$L^*\setminus\{0\}$ (Lemma 3.1) and the $\mu=0$ term carries the factor $\|\mu\|^2=0$.
(iv) Solving (iii) for the contact-shell sum and inserting (i), (ii) gives the displayed inequality.
*(No claim is made about the sign of $\Delta f$ at contact points; that is exactly the point.)* $\square$

**Corollary 7.1 (radial/tangential form).** At a contact point $\lambda$ with $\Delta f(\lambda)>0$,
write $\Delta=\Delta_{S^{d-1}(1)}+\partial_r^2+\frac{d-1}{r}\partial_r$ at $r=\|\lambda\|=1$. Since
$f\le0$ on the unit sphere with $f(\lambda)=0$, $\lambda$ maximises $f|_{S^{d-1}(1)}$, so
$\Delta_{S^{d-1}}f(\lambda)\le0$; and $\partial_rf(\lambda)\ge0$ because $f(\lambda+t\lambda)\le0=f(\lambda)$
for $t\ge0$. Hence
$$\partial_r^2f(\lambda)+(d-1)\partial_rf(\lambda)\;>\;-\Delta_{S^{d-1}}f(\lambda)\;\ge\;0 .$$

**Remarks.**
1. *Consistency with $d=8$.* For Viazovska's $g$ (sharp at the unimodular $\Lambda_8=\Lambda_8^*$)
the identity gives $\sum_{\|\lambda\|=\sqrt2}\Delta g(\lambda)=-\Delta g(0)>0$, so $g$ has positive
Laplacian at some of the $240$ minimal vectors — no contradiction, and this is exactly where revision
1's false proposition failed.
2. *Double zeros only off the contact shell.* For $\|\lambda\|>1$, not only $\Delta f(\lambda)\le0$:
$f$ has a local maximum with value $0$, so in radial coordinates $f$ has a double zero at every shell
radius $>1$ (this is m4/d1's and m7/d2's observation, and it is why the FCC contact shell is
qualitatively different from the $d=8,24$ situation where all shells have radius $\ge\sqrt2>1$ after
the standard normalisation).
3. *Status.* Theorem 7 is a structural constraint, not a nonexistence result; it is the correct
replacement for revision 1's Proposition 4.7 and says nothing about whether a sharp certificate
exists.

---

## 8. Scope: what is proved, what is not

**Proved.** (B) and (4.2) with proofs (Thms 4.1, 4.2); the crossover and shell-budget analysis of §5
(script part (C)–(E)); the $d=1$ borderline (§6); Theorem 7 and Corollary 7.1. The shell data of part
(A)–(B) of the script re-verifies results of m7/d2 and m4/d1 and is not claimed as new.

**Not proved / not claimed.** (i) Nothing here decides the existence question for general admissible
$f$: in $d=3$ the plain program is not sharp by Li's theorem (R. Li, *Dual linear programming bounds
for sphere packing via discrete reductions*, Adv. Math. 2024, arXiv:2206.09876, Thm 6.1), which is
independent of this note. (ii) The constant in (B) is the elementary Jensen constant; the sharp
constant is discussed in §5 but not proved here (it is classical). (iii) Theorem 7 requires $C^2$ and
an admissible Laplacian; in particular it is stated for functions for which Poisson summation applies
to $\Delta f$. (iv) Revision 1's Proposition 4.7 and its consequences are withdrawn; no statement
about Schwartz functions or about the decay of the $d=8,24$ magic functions is made.

---

## 9. Numerical verification

`scripts/budget.py` (standard library only; exact integer arithmetic via Legendre's three-square
theorem) produces `scripts/budget.out`. Every quantity is printed together with the formula used.

| part | content | check |
|---|---|---|
| (A) | FCC shells: $m$ is a shell $\iff 2m$ is a sum of three squares; empty shells $\{2\cdot4^k(8b+7)\}$ | agreement for all $m<400$ (32 empty shells listed); $366670$ non-empty $m\le4\cdot10^5$ vs $11M/12=366666.7$ |
| (B) | dual BCC shells $\{2m\}\cup\{3/2+2k\}$ | first fourteen $1.5,2,3.5,4,\dots$; density $0.916675$ vs $11/12$ |
| (C) | budget: $2K\le n(r_K)\le(4\pi Rr_K+\log(\|\hat f\|_1/f(0)))/\log2$; crossover $r_*=(12/11)cR$, $K_*=(12/11)c^2R^2$ | $c=9.0647\Rightarrow r_*=9.889R$, $K_*=89.6R^2$; $c=2\Rightarrow r_*=2.182R$, $K_*=4.4R^2$ |
| (D) | (B) at the $K$-th FCC shell | $R\ge0.3489,1.0665,3.3414,10.564,33.401$ for $K=10,10^2,10^3,10^4,10^5$ |
| (E) | dual form (4.2) | $S_0\ge0.3489,1.0640,3.3414$ for $K=10,10^2,10^3$ |
| (F) | $d=1$: $N_{\mathbb Z}(r)=\lfloor r\rfloor$, triangle sharp | $1\le9.065$: no obstruction, as it must be |
| (G) | sharpness of the Carlson constant | $\sin(2\pi Rt)$ has type $2\pi R$ and $2R=\tau/\pi$ zeros per unit length |

Note on priorities: (A)–(B) reproduce the shell data of m7/d2 and m4/d1; (F)–(G) are consistency
checks, not new results; the new numerical content is (C)–(E).
