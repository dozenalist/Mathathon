# Sharp Cohn–Elkies-type bounds in dimension three

### Can there be a sharp linear-programming bound in $\mathbb R^3$? What the Cohn–Elkies program can and cannot do in three dimensions, with the numbers

---

## 0. The question, and the answer

The question this note addresses:

> Cohn–Elkies (2003) turned the sphere-packing problem into an infinite-dimensional linear program: a single admissible function $f:\mathbb R^d\to\mathbb R$ with $f\le 0$ off the unit ball and $\widehat f\ge 0$ certifies that no packing has centre density above $f(0)/\widehat f(0)$. In $d=8$ and $d=24$ that bound is exactly sharp, and the certificate ("magic function") was found by solving an inverse problem — the zeros forced by the equality case, then a modular form that produces them. **Is there a sharp bound of this kind in $d=3$, possibly with a modified program and a different inverse problem?**

The answer, in the form I can defend:

1. **Not with the Cohn–Elkies linear program itself.** This is a theorem, not a numerical accident: Li (Adv. Math. 2024, arXiv:2206.09876, Thm 6.1) proves the $d=3$ LP value is $>0.18398089$ in the Cohn–Elkies radius-$1$ table convention, i.e. $>1.471847$ in the normalisation of this note, while the truth is $\sqrt2=1.414214$. So the LP is strictly non-sharp in $d=3$ — as it is in $3,4,5,6,12,16$ and conjecturally everywhere except $1,2,8,24$.
2. **And this is not an accident of analysis but of arithmetic.** A sharp certificate at the extremal lattice $L$ must vanish on $L\setminus\{0\}$ and its transform on $L^*\setminus\{0\}$ (CE 2003, §5). In $d=1,2,8,24$ the extremal lattice is *isodual* — $L$ is homothetic to $L^*$ — so the two zero families coincide, one theta series is self-dual under the Fricke involution $\tau\mapsto-1/\tau$, and the modular machine has something to build on. In $d=3$ the extremal lattice is $A_3=\mathrm{FCC}$, whose dual is $\mathrm{BCC}$; these are **not** similar ($12$ minimal vectors versus $8$). The two zero families are different sets of radii ($\{k: 2k \text{ a sum of 3 squares}\}$ versus $\{2m:m\text{ a sum of 3 squares}\}\cup\{4j+\tfrac32\}$), no single theta series carries both, and there is nothing for the Fricke involution to close on. Section 3 makes this precise.
3. **Also, the "eigenfunction" mechanism cannot be transplanted even in principle**: *no* non-zero Fourier eigenfunction is ever a Cohn–Elkies certificate, in any dimension (Lemma 2.2). Viazovska's $g$ is a *sum* of a $+1$- and a $-1$-eigenfunction; the two are built in $d=8$ because there both zero families coincide. In $d=3$ there is no such coincidence to exploit.
4. **What survives — and I would argue is the honest three-dimensional analogue of the CE/Viazovska program — is a *localised* linear program.** The global LP is blind to local geometry: it applies to "weighted configurations" that are not packings at all, and its value is the optimum over those. A bound that is sharp at $\mathrm{FCC}$ must use locality. And this is not a matter of taste: in $d=3$ the local (Voronoi-cell) bound of Hales–McLaughlin sits $1.9\%$ above the truth, while the best global Fourier bound sits $4.0\%$ above and the CE LP $5.3\%$ above — locality is already ahead by a factor two in the error. The known sharp architecture is Hales': a finite-dimensional score $\sigma$ on *decomposition stars* (a centre, its neighbours within $2.51$, plus combinatorial markings), with the local inequality $\sigma(D)\le 8\,\mathrm{pt}$, proved for each of finitely many combinatorial types by a **linear program** ($100$–$200$ variables, $1000$–$2000$ constraints) plus branch and bound (Hales 2005, Ch. 23, Ch. 25). The score plays the role of the magic function; the inverse problem "find the score that is tight exactly at $\mathrm{FCC}$" is the $d=3$ analogue of "find the weight-$(-2)$ modular form", and it is the right place to look. Sections 5–6 say exactly what is missing.

The rest of the note is the evidence: conventions and numbers (§1), the equality case at $\mathrm{FCC}$ (§2), the arithmetic obstruction (§3), my own computation of the $d=3$ LP value and of where its slack lives (§4), the three surviving architectures (§5), a concrete proposal (§6), the computation log (§7).

---

## 1. Conventions, the CE theorem, and the numbers

### 1.1 Normalisation used here

$X\subset\mathbb R^3$ with $\|x-y\|\ge1$ for distinct $x,y$; balls of radius $1/2$; $\delta(X)=\#$centres per unit volume ("centre density"); packing density $=\frac{\pi}{6}\,\delta$. Fourier transform $\widehat f(y)=\int_{\mathbb R^3}f(x)e^{-2\pi i\langle x,y\rangle}dx$. Poisson summation
$$\sum_{x\in L}F(x+t)=\frac1{\det L}\sum_{\mu\in L^*}\widehat F(\mu)\,e^{2\pi i\langle\mu,t\rangle}.$$
$f$ is *admissible* if continuous with $|f(x)|,|\widehat f(x)|\le C(1+\|x\|)^{-3-\varepsilon}$.

> **Theorem (Cohn–Elkies 2003).** If $f$ is admissible, $f\not\equiv0$, $f(x)\le0$ for $\|x\|\ge1$ and $\widehat f\ge0$, then every packing has
> $$\delta\le A(f):=\frac{f(0)}{\widehat f(0)} .$$

The proof is the double count $Nf(0)\ge\sum_{x,y}\sum_{\lambda}f(x-y+\lambda)\ge N^2\widehat f(0)/\det L$ for a periodic packing. I reproduce it in §2.1 because the equality case is what everything below turns on. Two remarks used later: $\widehat f\ge0$ makes $f$ positive definite, so $|f(x)|\le f(0)$; and $f$ need not be non-negative on the unit ball, the only constraint there is $\int f=\widehat f(0)>0$.

Cohn–Elkies' Theorem 3.2 is the same statement in the form "minimise the last sign change". If $f\le0$ for $\|x\|\ge r$ and $\widehat f\ge0$, rescaling gives, for packings of minimal distance $1$,
$$\delta\;\le\; r^3\,\frac{f(0)}{\widehat f(0)}, \qquad\text{equivalently}\qquad \Delta\le\frac{\pi r^3}{6}\cdot\frac{f(0)}{\widehat f(0)} .$$
For a sharp bound one needs $r^3f(0)/\widehat f(0)=\sqrt2$; with the normalisation $f(0)=\widehat f(0)$ this reads $r=2^{1/6}=1.12246$ — *strictly larger than the minimal distance* $1$. This is a small point that matters for the equality analysis: the threshold $r$ is not the contact distance, and the certificate is only asked to be non-positive *outside* the ball of radius $r$, while the packing is rescaled so that its minimal distance equals $r$. The equality case below is stated for the case $r=1$ (certificate non-positive off the unit ball, lattice of minimal distance $1$); the general case is the same statement for the rescaled lattice $rA_3$, whose shortest vector has length exactly $r$, and the two normalisations agree because $r^3A(f)=\sqrt2=1/\det A_3$ reduces to $A(f)=1/\det L$ when $r=1$. All the computations of §4 use $r=1$, so the shells there are at $\sqrt k$; with $f(0)=\widehat f(0)$ they would sit at $2^{1/6}\sqrt k$, and the arithmetic of *which* $k$ occur is unchanged.

### 1.2 The numbers, and the fact that local bounds already win in $d=3$

| quantity | packing density $\Delta$ | centre density $\delta=\tfrac{6}{\pi}\Delta$ | ratio to truth | method |
|---|---|---|---|---|
| truth $\delta_3$ (Kepler; Hales 2005, Flyspeck 2014) | $0.7404805$ | $\sqrt2=1.414214$ | $1$ | exact, not Fourier |
| best known bound other than Kepler: dodecahedral (Fejes Tóth 1943; **Hales–McLaughlin, JAMS 23 (2010) 299–344**) | $0.7546974$ | $1.441366$ | $1.0192$ | **local**: every Voronoi cell $\ge$ regular dodecahedron of inradius $1$ |
| three-point / SDP (Cohn–de Laat–Salmon 2022) | $0.7702704$ | $1.471108$ | $1.0402$ | global Fourier, 3-point |
| Muder 1998 | $0.773055$ | $1.476426$ | $1.0440$ | local (Voronoi) + cone decomposition |
| CE 2003 linear programming | $0.7797468$ | $1.489207$ | $1.0530$ | global Fourier, 2-point |
| CE LP value, my computation (§4) | $0.779746$ | $1.489202$ | $1.0530$ | 31-term Laguerre basis |

Conversions: $\delta=6\Delta/\pi$; multiply CE-table centre densities by $8$. Two cross-checks of the arithmetic: CE's $0.779746762$ converts to $1.489207$, matching my computed LP value $1.489202$ to six digits; CDLS's $0.770270440$ converts to $1.471108$, matching the $1.471112$ in Li's paper (rounding). The dodecahedral entry is recomputed from scratch: a regular dodecahedron of inradius $1$ has edge $2/\sqrt{5/2+\frac{11}{10}\sqrt5}$, volume $5.5502910$, so $\Delta\le(4\pi/3)/5.5502910=0.7546974$.

**Read that table again with the order in mind.** In $d=3$ the *local* bound (Voronoi cells) is $1.9\%$ above the truth; the *global Fourier* bounds are $4.0\%$ and $5.3\%$ above. The best known bound in dimension three, apart from Kepler's theorem itself, is not a Fourier bound at all. This is worth stating plainly because the two literatures are usually compared within themselves: Li's paper says "the best upper bound on $\delta_3$ not using Hales is $0.183889$" (CdLS), which is the best *Fourier-analytic* bound; the dodecahedral bound $0.18017$ (CE units) is older and better. The lesson for the question in this note is direct: **the three-dimensional route to sharpness runs through locality, not through better test functions.**

The CE value corresponds to last sign change $r=2\cdot0.18616^{1/3}=1.14234$, against the ideal $2\cdot0.1767767^{1/3}=1.12247$: the LP misses the Kepler threshold by $1.77\%$ in $r$, which cubes to the $5.3\%$ in density.

### 1.3 The two lattices

$D_3=\{y\in\mathbb Z^3:\ y_1+y_2+y_3 \text{ even}\}$ has covolume $2$ and minimal norm$^2$ $2$. The FCC lattice of minimal distance $1$ is
$$L=A_3=\tfrac1{\sqrt2}D_3,\qquad \det L=2^{-3/2}=\tfrac1{\sqrt2},\qquad \delta(L)=\tfrac1{\det L}=\sqrt2,$$
with $12$ minimal vectors (kissing number) and dual
$$L^*=\sqrt2\,D_3^*,\qquad D_3^*=\mathbb Z^3\cup\big(\mathbb Z^3+(\tfrac12,\tfrac12,\tfrac12)\big),\qquad \det L^*=\sqrt2 .$$
$L^*$ is the BCC lattice; it has $8$ minimal vectors of length $\sqrt{3/2}$. **$L$ and $L^*$ are not similar**, because similarity preserves the number of minimal vectors and $12\ne8$. This single line is, in my view, the structural reason $d=3$ is the first dimension in which the CE program cannot be sharp (see §3).

---

## 2. The equality case at FCC: what a sharp certificate would have to be

### 2.1 The theorem

> **Theorem 2.1 (equality case; Cohn–Elkies 2003 §5, proved here in the shape needed).** Let $L$ be a lattice of minimal distance $1$ and covolume $D$. Let $f$ be admissible with $f\le0$ off the unit ball, $\widehat f\ge0$, and suppose $A(f)=f(0)/\widehat f(0)=1/D$ (i.e. the bound is sharp at $L$). Then
> $$f(\lambda)=0\quad\forall\lambda\in L\setminus\{0\},\qquad \widehat f(\mu)=0\quad\forall\mu\in L^*\setminus\{0\},$$
> and consequently the **sum rule**
> $$\sum_{\lambda\in L}f(\lambda+t)=\frac{\widehat f(0)}{\det L}=f(0)\qquad\text{for every } t\in\mathbb R^3 .$$

*Proof.* Poisson summation with $F=f(\cdot+t)$ gives $\sum_{\lambda}f(\lambda+t)=\frac1D\sum_\mu \widehat f(\mu)e^{2\pi i\langle\mu,t\rangle}\ge \widehat f(0)/D$. For $t=0$ the left side is $\le f(0)$ (all terms with $\lambda\ne0$ are $\le0$), so $f(0)\ge\widehat f(0)/D$, with equality by hypothesis. Hence every term with $\lambda\ne0$ vanishes and every term with $\mu\ne0$ in the Poisson sum vanishes; substituting back gives the sum rule for all $t$. $\square$

(The direction of the inequality is worth stating once explicitly: the CE bound is $\delta\le A(f)$ and $\delta(L)=1/\det L$, so **sharpness at $L$ means $A(f)=1/\det L$, not $A(f)=\det L$**. For $\mathrm{FCC}$ that is $A(f)=\sqrt2$.)

Three consequences, all used below.

**(a) The two spectra.** By Theorem 2.1, a sharp $f$ vanishes at every $\|\lambda\|$, $\lambda\in L\setminus0$, and $\widehat f$ at every $\|\mu\|$, $\mu\in L^*\setminus0$. These are

$$\mathcal S(L)=\{k\ge1:\ 2k \text{ is a sum of three squares}\},\qquad
\mathcal S(L^*)=\{2m:\ m\ge1 \text{ is a sum of three squares}\}\cup\{4j+\tfrac32:\ j\ge0\}.$$

Legendre's three-square theorem turns the first into $\mathcal S(L)=\{k\ge1:\ k\ne2^{2a-1}(8b+7),\ a\ge1\}$, so $k=14,30,46,56,62,\dots$ are **not** squared radii of $L$; the first shells with multiplicities are $1\!:\!12,\ 2\!:\!6,\ 3\!:\!24,\ 4\!:\!12,\ 5\!:\!24,\ 6\!:\!8,\ 7\!:\!48,\ 8\!:\!6,\dots$. On the dual side the first shells are $\tfrac32\!:\!8,\ 2\!:\!6,\ 4\!:\!12,\ \tfrac{11}2\!:\!24,\ 6\!:\!8,\dots$ — note $\tfrac32\notin\mathcal S(L)$ and $3\in\mathcal S(L)$ but $3\notin\mathcal S(L^*)$. **The two zero families are different and neither contains the other.** (I verified both descriptions by exact enumeration to $r^2\le400$; see §7.)

**(b) Double zeros.** Since $f\le0$ on $[1,\infty)$ and $f$ is real analytic, every zero at a radius $>1$ is a local maximum of a non-positive function, hence of order at least $2$; likewise $\widehat f\ge0$ vanishes to second order at every dual shell (including the first, $\sqrt{3/2}$). At the contact radius $1$ only the one-sided conclusion $f'(1)\le0$ is available; for $f=\widehat f$-normalised certificates (§1.1) the analogous statement is at $r$.

**(b′) A tempting argument that fails — and the constraint that replaces it.** Since $f$ vanishes on $L\setminus\{0\}$ and $f\le0$ off $B_1$, one is tempted to say $f$ has a local maximum at every lattice point, hence $\Delta f(\lambda)\le0$, and then to sum: by Poisson summation and the vanishing of $\widehat f$ on $L^*\setminus\{0\}$,
$$\sum_{\lambda\in L}\Delta f(\lambda)=-\frac{4\pi^2}{\det L}\sum_{\mu\in L^*}\|\mu\|^2\widehat f(\mu)=0 ,$$
while $\Delta f(0)=-4\pi^2\int\|y\|^2\widehat f(y)\,dy<0$ for any non-zero certificate ($\widehat f\ge0$, $\widehat f(0)>0$). That looks like a contradiction and hence like a proof that no smooth sharp certificate exists. **It is wrong**, and the reason is worth recording. Away from the contact shell ($\|\lambda\|>1$) the sign condition holds in a full neighbourhood, so $f$ genuinely has a local maximum there and $\Delta f(\lambda)\le0$; but *at* a contact point $\|\lambda\|=1$ the constraint region is the exterior of a ball, so one only gets $f(\lambda+th)\le f(\lambda)$ for $t\ge0$ and $\langle h,\lambda\rangle\ge0$ — a one-sided condition in $t$, which yields $\partial_tf\le0$ and says nothing about $\partial_t^2f$. (A one-sided inequality $\varphi(t)\le\varphi(0)$, $t\ge0$, is compatible with $\varphi''(0)>0$: take $\varphi(t)=-t+t^2$.) The decisive check is Viazovska's $g$ in $d=8$: it is Schwartz, sharp, $\widehat g$ vanishes on $\Lambda_8\setminus\{0\}$ and $\det\Lambda_8=1$, so the computation above gives $\sum_{\ell}\Delta g(\ell)=0$ with $\Delta g(0)<0$, forcing $\Delta g(\ell)>0$ at some non-zero lattice point. What the computation *does* give is a genuine constraint: $\Delta f\le0$ at every non-contact lattice point and at $0$, hence
$$\sum_{\|\lambda\|=1}\Delta f(\lambda)\ \ge\ -\Delta f(0)\ >\ 0 ,$$
so a non-zero $C^2$ sharp certificate with admissible Laplacian must have $\Delta f>0$ at some *contact-shell* point ($d=3$: one of the twelve neighbours — it is "concave outward" there). The contact shell is exactly where the three-dimensional argument is delicate, and it is the same degeneracy that defeats the naive "at most one nearby point" step. (Version 1 of the swarm member's note asserted the opposite — that no $C^2$ sharp certificate exists — and the counterexample above is what refutes it; the repaired statement is his Theorem 7, which I checked.)

**(c) The sum rule is a strong local constraint.** For every $t$, $\sum_{\lambda\in L}f(\lambda+t)=f(0)$ *exactly*. Since $f\le0$ outside the unit ball, the terms with $\|\lambda+t\|\ge1$ are all $\le0$, so
$$\sum_{\lambda\in L,\ \|\lambda+t\|<1}f(\lambda+t)\;\ge\;f(0)\qquad\text{for every }t.$$
At most $12$ lattice points can satisfy $\|\lambda+t\|<1$ (kissing number), and for $t$ at a lattice point the left side is $f(0)$ alone. Averaging the inequality over $t$ in a fundamental domain and using $\int f=\widehat f(0)$ shows that the sum rule is *compatible* with the sign conditions to first order — there is no immediate contradiction, and indeed none is available from local considerations alone (this is where a naive "one nearby point" argument fails: for every $t$ the ball $B(-t,1)$ contains at least two lattice points unless $-t\in L$).

### 2.2 What this rules out

> **Lemma 2.2 (no eigenfunction certificate).** There is no non-zero Fourier eigenfunction $f$ (i.e. $\widehat f=\varepsilon f$, $\varepsilon\in\{\pm1\}$) satisfying the CE sign conditions $f\le0$ off $B_1$, $\widehat f\ge0$ — in any dimension.

*Proof.* If $\varepsilon=+1$: $\widehat f\ge0$ gives $f\ge0$ everywhere; $f\le0$ off $B_1$ then gives $f=0$ off $B_1$, so $f$ is compactly supported and entire (being equal to $\widehat f$, an entire function), hence $f\equiv0$. If $\varepsilon=-1$: $\widehat f\ge0$ gives $f\le0$ everywhere, and $\int f=\widehat f(0)=-f(0)\ge0$ with $f\le0$ forces $f\equiv0$. $\square$

So the phrase "the magic function is a Fourier eigenfunction" is a shorthand that needs care: Viazovska's $g=\frac{\pi i}{8640}a+\frac{i}{240\pi}b$ is a *combination* of a $(+1)$-eigenfunction $a$ and a $(-1)$-eigenfunction $b$; each is built from a weight-$(-2)$ modular form, and the combination is what satisfies the sign conditions. In $d=3$ the weight would be $2-d/2=\tfrac12$, and neither half of the construction has an isodual lattice to stand on (§3).

---

## 3. Why the failure in $d=3$ is structural

### 3.1 The $d=1,2,8,24$ pattern

In each of the four dimensions where a sharp CE bound is expected or known, the extremal lattice is homothetic to its dual:

| $d$ | extremal lattice | isodual? | sharp CE bound |
|---|---|---|---|
| 1 | $\mathbb Z$ | yes (self-dual) | yes, elementary |
| 2 | $A_2$ (hexagonal) | yes, after rescaling (rotation) | CE Conjecture 8.1; the packing problem itself is Thue/Fejes Tóth |
| 3 | $A_3$ = FCC | **no** ($A_3^*$ = BCC, $12\ne8$ minimal vectors) | **no** (Li 2024) |
| 8 | $E_8$ | yes (self-dual) | yes (Viazovska 2017) |
| 24 | Leech | yes (self-dual) | yes (Cohn–Kumar–Miller–Radchenko–Viazovska 2017) |

Cohn–Elkies say this explicitly in §5 of their paper: they work with isodual lattices because "each of these lattices except $A_2$ actually equals its dual", and note that "when $\Lambda$ is isodual, the vector lengths in $\Lambda$ and $\Lambda^*$ are the same, so $f$ and $\widehat f$ must both vanish on $\Lambda\setminus\{0\}$." In $d=3$ that sentence fails: $f$ and $\widehat f$ must vanish on two different sets of spheres, one of which contains radii the other does not.

### 3.2 The theta-series form of the obstruction

The Gaussian superposition machine rests on one identity: $\widehat{G_z}=z^{-d/2}G_{-1/z}$ for $G_z(x)=e^{\pi iz\|x\|^2}$, so that a superposition $\int_C\varphi(z)G_z\,dz$ is a Fourier eigenfunction exactly when $\varphi$ is modular of weight $2-d/2$ for $\tau:z\mapsto-1/z$. For a lattice the same identity appears as Poisson reciprocity for the theta series:
$$\Theta_{L^*}\!\Big(-\frac1\tau\Big)=\det(L)\Big(\frac{\tau}{i}\Big)^{d/2}\Theta_L(\tau).$$
In $d=3$, with $q=e^{2\pi i\tau}$,
$$\Theta_{A_3}(\tau)=\tfrac12\big(\theta_3(\tau/2)^3+\theta_4(\tau/2)^3\big),\qquad \Theta_{A_3^*}(\tau)=\theta_3(2\tau)^3+\theta_2(2\tau)^3,$$
both of weight $3/2$ for $\Gamma_0(4)$ with a character (I verified both closed forms against direct enumeration to $r^2\le1600$, and the reciprocity law numerically to $10^{-40}$ — §7). Reciprocity relates $\Theta_{A_3}$ to $\Theta_{A_3^*}$, i.e. **to a different modular form**; there is no $\tau\mapsto-1/\tau$ eigen-relation for a single theta series, because $A_3$ is not similar to $A_3^*$. In $d=8,24$ the corresponding relation is $\Theta(-1/\tau)=\tau^{d/2}\Theta(\tau)$ — self-duality — and that is exactly the equation a weight-$(2-d/2)$ modular form is designed to satisfy.

So the obstruction has a clean shape: **a "$d=3$ Viazovska theorem" would have to produce, from one weight-$1/2$ object, a function whose zeros are $\mathcal S(A_3)$ and whose transform's zeros are $\mathcal S(A_3^*)$ — two arithmetically unrelated families. In $d=8$ and $24$ the two families coincide, and the construction is possible. In $d=3$ half-integral weight is available (the $\theta_{00},\theta_{01},\theta_{10}$ ring), but the Fricke involution that made the $d=8$ proof work does not close.**

One sharp statement that can be made in this direction (swarm member m2, Theorem 4.4, which I verified): every $d=3$ certificate has $A(f)\ge\sqrt2>1$ by the equality argument applied to $\mathrm{FCC}$, whereas the transplanted $d=8,24$ construction is normalised so that $f(0)=\widehat f(0)=1$, i.e. $A(f)=1$. So that mechanism, taken with its own normalisation, can only ever prove $\delta\le1$, and $\delta_3=\sqrt2>1$: the failure is the arithmetic inequality $\delta_3\ne1$.

This is a diagnosis, not a theorem, and I flag it as such: what is proved is (i) Lemma 2.2, (ii) Li's theorem, (iii) the arithmetic facts about the two spectra and the non-similarity of $A_3,A_3^*$. The claim that "no weight-$1/2$ construction can work" is the natural explanation of (i)–(iii), not an independent proof. (A proof along these lines would be a genuine result: it would give an *analytic* proof of non-sharpness in $d=3$, replacing Li's computer-assisted $7000$-digit rational certificate. This is the same program that de Courcy-Ireland–Dostert–Viazovska are carrying out for $d=6$.)

---

## 4. The quantitative picture: how much the LP misses, and where the slack lives

### 4.1 Computing the $d=3$ LP value

Radial functions in $d=3$ have the Laguerre–Gaussian eigenbasis
$$\varphi_k(x)=L_k^{(1/2)}(2\pi\|x\|^2)\,e^{-\pi\|x\|^2},\qquad \widehat{\varphi_k}=(-1)^k\varphi_k ,$$
which I checked against direct quadrature for $k\le20$ (error $<10^{-10}$ relative). I solved the LP
$$\text{minimise } \frac{1}{\widehat f(0)}\quad\text{over } f=\sum_{k\le K}c_k\varphi_k,\quad f(0)=1,\quad f\le0\ \text{on }[1,\infty),\quad \widehat f\ge0\ \text{on }[0,\infty)$$
with the sign conditions imposed on $2000$-point grids and the asymptotic condition $c_K\ge0$ ($K$ odd) that makes the leading polynomial terms have the right signs at infinity. Results ($\delta\le1/\widehat f(0)$):

| $K$ | 5 | 9 | 13 | 19 | 23 | 27 | 31 | 41 |
|---|---|---|---|---|---|---|---|---|
| bound | 1.511183 | 1.493247 | 1.490095 | 1.489257 | 1.489225 | 1.489211 | 1.489203 | 1.489202 |

So the LP value is $\approx1.48920$: the sequence is monotone and converged to five digits, it is below CE's rigorous $m=6$ value $1.48928$ (as it must be), and it sits $1.2\%$ above Li's rigorous lower bound. **The $5.3\%$ gap between the LP and the truth is a property of the linear program, not of a truncated basis.**

The optimal certificate is instructive: it is *nearly* sharp in the sense of §2. Its values at the shells are ($K=31$ optimum, evaluated in double precision; the $K=41$ optimum has the same structure with different small values)

| $r$ | $\sqrt1$ | $\sqrt2$ | $\sqrt3$ | $\sqrt4$ | $\sqrt5$ | $\sqrt6$ | $\sqrt7$ | $\sqrt8$ |
|---|---|---|---|---|---|---|---|---|
| $f(r)$ | $-2\cdot10^{-17}$ | $-2.6\cdot10^{-3}$ | $-4.1\cdot10^{-5}$ | $-2.0\cdot10^{-6}$ | $-1.0\cdot10^{-5}$ | $+3\cdot10^{-9}$ | $+6\cdot10^{-9}$ | $-6\cdot10^{-8}$ |
| $\widehat f$ at dual shells | $\sqrt{3/2}$: $1.6\cdot10^{-3}$ | $\sqrt2$: $1.3\cdot10^{-3}$ | $2$: $1.6\cdot10^{-4}$ | $\sqrt{5.5}$: $2.5\cdot10^{-5}$ | $\sqrt6$: $9\cdot10^{-6}$ | $\sqrt8$: $9\cdot10^{-6}$ | | |

(Values at the shells where the two families overlap are distinct because the two rows are different functions evaluated at different radii.) The certificate hugs zero at the required radii to $10^{-3}$–$10^{-8}$ but cannot reach zero, and can never do so: that is Li's theorem expressed quantitatively.

### 4.2 A slack identity, and the 1/3–2/3 split

For any admissible $f$ with $f\le0$ off $B_1$, $\widehat f\ge0$ and $A(f)$ finite, Poisson summation for the lattice $L=A_3$ gives the exact identity
$$\underbrace{f(0)-\frac{\widehat f(0)}{\det L}}_{\text{slack }= f(0)-\sqrt2\widehat f(0)}\;=\;\underbrace{\big(f(0)-\textstyle\sum_{\lambda\in L}f(\lambda)\big)}_{\text{primal mass}\ \ge0}\;+\;\underbrace{\sqrt2\Big(\sum_{\mu\in L^*}\widehat f(\mu)-\widehat f(0)\Big)}_{\text{dual mass}\ \ge0},$$
both masses being non-negative by the sign conditions. Sharpness requires both to vanish; the slack $f(0)-\widehat f(0)/\det L$ is precisely how much the CE inequality loses at $L$.

For the optimal certificate of §4.1 ($f(0)=1$, $\widehat f(0)=0.6714968$, slack $0.0503602$) the two sums evaluate — I checked both by brute-force lattice enumeration, and they agree to all digits, which is also a strong check of the whole computation — to
$$\text{primal mass}=0.0170940\ (33.9\%),\qquad \text{dual mass}=0.0332862\ (66.1\%).$$
So **two thirds of the failure comes from $\widehat f$ not vanishing on the dual BCC lattice, one third from $f$ not vanishing on FCC.** The primal zeros are "cheap" (the optimiser nearly achieves them), the dual ones are "expensive".

### 4.3 The inverse problem, made explicit: it cannot be solved, and it is expensive to even attempt

The most direct reading of "sharp bound as an inverse problem" is: *impose the zeros that §2 says are necessary, and see whether the LP value drops to $\sqrt2$.* It does not; it rises. Solving the same LP with the necessary equalities added ($K=41$, bounds in the $\delta$ normalisation, ratio to $\sqrt2$ in brackets):

| constraints added | bound | ratio |
|---|---|---|
| none | 1.489202 | 1.0530 |
| $f=0$ on $\sqrt1,\dots,\sqrt6$ | 1.528131 | 1.0806 |
| $f=0$ on $\sqrt1,\sqrt2$ | 1.527110 | 1.0798 |
| $\widehat f=0$ on $\sqrt{3/2},\sqrt2$ | 1.593434 | 1.1267 |
| $\widehat f=0$ on the first six dual shells | 1.611267 | 1.1393 |
| both, one shell each | 1.537891 | 1.0875 |
| both, four shells each | 1.757025 | 1.2424 |

Adding *necessary* conditions cannot improve a linear-programming bound — it only shrinks the feasible set — so the table is not evidence against the inverse problem, it is a measurement of its price: the equality conditions of §2 are not merely unattainable (Li), they are *expensive*, and each dual condition costs roughly twice as much as a primal one, consistent with the $1/3$–$2/3$ split of §4.2. (These are numerical values for a fixed basis; the true constrained LP values are no larger. The $n$-dependence within each row is flat, so the reported numbers are converged in the number of imposed shells.)

---

## 5. What a sharp bound in three dimensions can be

There are exactly three architectures I know of that keep the CE features — a linear program, an explicit certificate, an inverse problem to find it — while being able to be sharp in $d=3$.

### 5.1 Local (cell-wise / star-wise) linear programs

*Why the global LP cannot be sharp, in one sentence:* the CE LP is the dual of a problem over **weighted** configurations — measures with $\mu\ge0$ off the ball — and in $d=3$ the optimal weighted configuration has density above $\sqrt2$ although no true packing does. Li's proof exhibits exactly such a configuration (a discrete reduction to $\mathbb Z_m^3$, with a rational dual certificate). Locality is precisely the information that rules weighted configurations out.

*The architecture (Hales', recast as an inverse problem).*
1. **Localise.** The Kepler problem is equivalent to a statement about Voronoi cells: since $B_{1/2}(p)\subset V_p$ always, $\delta=\frac{\pi/6}{\langle\operatorname{vol}V_p\rangle}$, so it suffices to show that the average Voronoi volume is $\ge1/\sqrt2$. No *pointwise* cell bound can hold (Voronoi cells of a min-distance-$1$ packing can be smaller than $1/\sqrt2$; see §5.4), so the bound must be an average over clusters.
2. **Discretise.** For each centre $p$, take the *decomposition star* $D(p)$: the centres within distance $2.51$, the Delaunay/Q-system simplices among them, and combinatorial markings (tetrahedron/quarter, flat/upright). The space of stars is compact and finite-dimensional, and the Voronoi cell of $p$ is determined by $D(p)$.
3. **Score.** Define $\sigma(D)$ as a linear function of $\operatorname{vol}\Omega(D)+\mathcal A(D)$, normalised so that "FCC-compatible" becomes $\sigma(D)\le 8\,\mathrm{pt}$ with $\mathrm{pt}=4\arctan\sqrt{2/5}-\pi/3$ the score of the regular tetrahedron of edge $2$. The theorem to prove is $\max_{D}\sigma(D)=8\,\mathrm{pt}$, with equality exactly at the FCC and HCP stars.
4. **Prove it by LP.** For each of the finitely many combinatorial types, $\max\sigma$ is relaxed to a linear program in variables (angles $\alpha(v,F)$, face scores $\sigma(F)$, solid angles $\mathrm{sol}(F)$, heights, edge lengths) subject to exact identities and to a family of linear inequalities that are themselves interval-arithmetic theorems. An LP maximum below $8\,\mathrm{pt}$ kills the type; branch and bound handles the rest. This is literally Hales 2005, Ch. 23 and Ch. 25: $10^5$ LPs of $100$–$200$ variables and $1000$–$2000$ constraints.

So in $d=3$ **the role of the magic function is played by the score $\sigma$, and the role of the inverse problem is "find $\sigma$ that is tight exactly at FCC/HCP".** That is a well-posed inverse problem: the equality case pins down the tightness conditions (regular tetrahedron of edge $2$ scoring $1\,\mathrm{pt}$; flat square of side $2$ scoring $0$), and one looks for a local functional satisfying them and dominated elsewhere. Hales found one by a mixture of geometry and optimisation; a systematic search over "scores of LP type" has, as far as I can tell, never been carried out and is the natural $d=3$ analogue of Cohn–Elkies' §8 inverse problem.

**A word on what this is not.** It is not a bound $f(0)/\widehat f(0)$ from a single function, and the "certificate" is a finite list of LP dual solutions rather than one closed form. That is the price of locality, and Li's theorem says the price must be paid.

### 5.2 The $p$-point hierarchy (Cohn–de Laat–Salmon)

The systematic way to strengthen the LP without going local is to add higher-order positivity: a three-point bound uses a kernel $f_3(x,y)$ positive definite on triples in addition to the two-point $f_2$, with the truncated Cohn–de Laat–Salmon inequalities (arXiv:2206.15373, Thm 1.1, which I checked against the source)
$$f_2(x)+f_3(x,0)+f_3(0,x)+f_3(x,x)\le0\ (1\le\|x\|\le R),\quad f_2(x)\le0\ (\|x\|\ge R),\quad f_3(x,y)\le0\ (\|x\|,\|y\|\le R,\ \|x-y\|\ge1),$$
giving $\delta\le f_2(0)+f_3(0,0)$. CDS compute these bounds by SDP with a truncation radius $R$; their $d=3$ value is $0.770271$ in packing density, i.e. $1.471108$ in the normalisation of this note — the best Fourier bound in $d=3$, $4.0\%$ above truth. They also state that they do not know whether the three-point bound is ever sharp outside the cases already settled by the two-point bound, and that their data suggest it is not, up to dimension sixteen.

The equality case is instructive and can be pinned down (I verified the following against CDS's Theorem 1.1 and re-derived the chain; the argument is due to swarm member m1 and I checked every step). Suppose the three-point bound is attained at a lattice $L$ of covolume $V$, so $f_2(0)+f_3(0,0)=1/V$. Then $f_2$ alone satisfies the *dual* half of the two-point equality conditions — $\widehat f_2=0$ on $L^*\setminus\{0\}$, and $\sum_{\lambda\in L}f_2(\lambda+t)=1/V$ for all $t$ — it fails only the *primal* sign condition, being positive at some lattice points of the annulus $[1,R]$. Moreover, if $f_3(0,0)=0$ then positive definiteness on $\{0,x\}$ gives $f_3(0,x)\equiv0$, hence $f_2\le0$ off $B_1$, hence $f_2$ is a sharp *two-point* certificate — contradicting Li in $d=3$. So a sharp three-point certificate in $d=3$, if one exists, must have $f_3(0,0)>0$, must have $f_3$ vanishing on all pairs of distinct lattice points in $B_R$, and must have $f_3(u,u)=-f_3(u,0)=-f_2(u)\ge0$ on them, with $\sum_{u}f_3(u,u)=f_3(0,0)$: the gain over the two-point bound is carried entirely by the *diagonal* of the kernel at contact-shell lattice points. That is a precise and rather surprising target for an inverse problem — and it is the one place where a sharp $d=3$ bound could still come from a global positivity argument.

### 5.3 What "sharp in $d=3$" definitely can be: restricted-class theorems

Two miniature sharp theorems, both of the CE type (LP duality / positive definite functions) and both provable:

**(i) The dodecahedral theorem — the model sharp local certificate.** Fejes Tóth's dodecahedral conjecture (1943), proved by Hales and McLaughlin (*J. Amer. Math. Soc.* **23** (2010) 299–344), states that every Voronoi cell of a packing of unit balls has volume at least that of a regular dodecahedron of inradius $1$. Since $\delta=\frac{\pi/6}{\langle\operatorname{vol}V_p\rangle}$, this gives $\delta\le1.441366$ for *every* packing — the best bound in dimension three other than Kepler's theorem, and better than every Fourier-analytic bound by a wide margin. Structurally it is exactly the local certificate this note argues for: one inequality per cell, sharp at a single cell shape, glued by the trivial identity "density = ball volume / mean cell volume". (The regular dodecahedron does not tile — which is why the bound is $1.9\%$ off rather than exact: no packing has all cells dodecahedral.)

**How far the local method goes, exactly** (swarm member m6; I recomputed every constant). Two statements pin the family down. (a) *The class on which the local inequality is sharp.* For a lattice cell, $\operatorname{vol}V=\det L$ and $\operatorname{inr}V=\lambda_1/2$, so Gauss's lattice theorem gives $\operatorname{vol}V\ge4\sqrt2\,\operatorname{inr}(V)^3$, with equality iff $V$ is the rhombic dodecahedron. Hence **every packing all of whose Voronoi cells satisfy that one local inequality has $\delta\le\sqrt2$, with equality iff every cell is a rhombic dodecahedron of inradius $1/2$** — a sharp, purely local certificate on a class much larger than "one cell type", since the shapes may vary from cell to cell. This is the closest thing in dimension three to a sharp Cohn–Elkies bound: one inequality per point, no Fourier analysis, tight exactly at FCC. (b) *The inequality itself fails in general, and the family cannot be pushed further.* The 12 icosahedral unit vectors together with the origin, periodised on $8\mathbb Z^3$, form a packing of minimal distance exactly $1$ whose central Voronoi cell is the *regular* dodecahedron of inradius $1/2$ and volume $0.6937864$ — strictly less than $1/\sqrt2=0.7071068$. So no per-cell volume bound can hold at $1/\sqrt2$; and since every "each point controls at least $c$ volume" certificate must have $c\le V_{\mathrm{dod}}=0.693786378564$, the whole family is capped at
$$\delta\le\frac1{V_{\mathrm{dod}}}=\frac{4}{5(5\sqrt5-11)\sqrt{2\sqrt5+5}}=1.4413658597\ldots$$
which is exactly Hales–McLaughlin, with the exact loss factor $4\sqrt2/\ell_{\mathrm{dod}}=1.0191995736$ ($\ell_{\mathrm{dod}}=8V_{\mathrm{dod}}$). The interesting part is the bookkeeping of what is elementary and what is not: the *impossibility* side ($c\le V_{\mathrm{dod}}$) is the explicit icosahedral packing, no computer; the *attainability* side is the computer-assisted dodecahedral theorem. So in the local world, dimension three is exactly $1.9\%$ too hard — the counterpart of "the LP is $4\%$ too weak". Whether a *cluster* version (two or three cells at a time) closes the gap is open, and is the sharpest concrete question this note leaves.

A clean special case worth isolating: if all Voronoi cells are translates of one polyhedron $K$ (so the cells tile by translations and $\delta=1/\operatorname{vol}K$), then the inradius condition reads $\operatorname{inr}K\ge1/2$ and the minimum of $\operatorname{vol}K$ over the five Fedorov parallelohedra is attained at the rhombic dodecahedron, $\operatorname{vol}=1/\sqrt2$ (cube $1$; hexagonal prism $\sqrt3/2$; truncated octahedron $4/(3\sqrt3)=0.7698$). So one-cell-type packings satisfy $\delta\le\sqrt2$ with equality iff FCC — by Fedorov's classification this is the lattice case of Kepler, a theorem since Voronoi (1908) and Fejes Tóth. The content here is the reduction, whose proof is a finite check.

**(ii) A grid packing: the exact answer, by an LP dual, is a perfect matching.** Take the class of packings inside the cubic grid $\Lambda=2^{-1/2}\mathbb Z^3$ (spacing $2^{-1/2}<1$, so a packing contains at most one site of each adjacent pair). The exact optimum on this class is $\delta=\sqrt2$, attained by $\mathrm{FCC}$ (a sublattice of index $2$): pair each site with its neighbour along $e_1$ into a domino; through a box of side $N\sqrt2$ (volume $2^{3/2}N^3$, $8N^3$ sites) the dominoes are exactly $4N^3$ in number, so a packing has at most $4N^3$ points and $\delta\le4N^3/(2^{3/2}N^3)=\sqrt2$. This is a **linear-programming dual certificate** — the dual of fractional independent set on the grid graph — and it is *local*: it uses only that adjacent sites conflict. And here the global Fourier method provably loses a factor two: any admissible $f$ with $\widehat f\ge0$ and $f\le0$ on $\Lambda\setminus\{0\}$ satisfies, by Poisson summation on $\Lambda$,
$$A(f)=\frac{f(0)}{\widehat f(0)}\ \ge\ \frac1{\det\Lambda}=2^{3/2}=2\sqrt2 ,$$
twice the truth of the class. This is the cleanest small instance of the whole thesis: where the extremal configuration is determined by *local* constraints, the sharp certificate is a local LP dual, and no global test function can match it however it is chosen or inverted for. (This miniature is swarm member m4's Theorem 7.1; I verified the count and the factor-2 argument.)

**(iii) Difference bodies.** The mechanism that gives the sharp bound in $d=1$ — $f=g*g$ with $g=\mathbf 1_{[-1/2,1/2]}$, i.e. the triangle function — has a dimension-dependent ceiling. If $f=g*\widetilde g$ with $g\ge0$ and $\operatorname{diam}(\operatorname{supp}g)\le1$, then $f$ is a valid CE certificate with $f(0)/\widehat f(0)=\|g\|_2^2/(\int g)^2\ge1/|B_{1/2}|=6/\pi=1.9099$ in $d=3$ (versus $1$ in $d=1$, where the triangle is extremal). So the autocorrelation mechanism is *provably $35\%$ too weak* in $d=3$: a clean quantitative no-go, and a good illustration of how $d$-dependent the "guess the function from its zeros" strategy is. (This is member m7's direction $d_2$ in the swarm; the Cauchy–Schwarz step is immediate and I reproduce the computation in §7.)

### 5.4 What cannot work, and why (a checklist of dead ends)

* **Pointwise Voronoi-volume bounds.** False, with an explicit counterexample: the 13-point icosahedral cluster $\{0\}\cup(\text{12 icosahedral unit vectors})$, periodised on $8\mathbb Z^3$, is a packing of minimal distance $1$ whose central Voronoi cell is the regular dodecahedron of inradius $1/2$ and volume $0.6937864<1/\sqrt2$. (The regular dodecahedron does not tile, which is exactly why it can occur as a single cell.) Only the average is bounded below, and every per-point volume certificate is capped at $1.4413658597$ (§5.3(i)).
* **Band-limited certificates.** Impossible, and quantitatively so (CE §5 for the mechanism; the budget is swarm member m3's, rechecked here against the constant — and note that I initially got this constant wrong myself, by implicitly setting the vanishing radius equal to the bandwidth). If $\widehat f$ is supported in $B(0,R)$, then for each direction $u$ the function $z\mapsto f(zu)$ is entire of exponential type $2\pi R$; a zero-count bound gives at most $cR\rho$ zeros in $|z|\le\rho$, with $c=2\pi/\log2$ from plain Jensen and $c=2$ at the sharp Carlson constant (this second value is attained by $\sin(2\pi Rt)$, whose zero density is $2R$). Matching against the shell count $N_L(\rho)\approx\frac{11}{12}\rho^2$ gives
$$K\ \le\ \tfrac{12}{11}c^2R^2\ =\ 4.4\,R^2\ \ (c=2),\qquad 89.6\,R^2\ \ (c=2\pi/\log 2),$$
so a band-limited certificate can meet at most about $4R^2$ (sharp) or $90R^2$ (crude) of the FCC shells; conversely the first $K$ shells force $R\gtrsim0.349,\ 1.067,\ 3.34,\ 10.56$ for $K=10,10^2,10^3,10^4$. Either way the bandwidth must diverge, which is CE's argument made quantitative — and it says nothing about the unbounded-bandwidth class where the real problem lives.
* **Fourier eigenfunctions.** Impossible by Lemma 2.2.
* **Adding the necessary zeros to the LP.** Provably counterproductive (§4.3).
* **Making a two-point positivity sum rule tight.** For a lattice $\Lambda$ and any nonzero finitely supported $w$, $\sum_{x,y\in\Lambda}f(x-y)w(x)\overline{w(y)}=\int\widehat f|W|^2>0$ whenever $\widehat f\ge0$, $\widehat f\not\equiv0$ (since $|W|^2>0$ off a null set). So every *positive-definiteness* sum rule is strictly slack at every lattice, in every dimension: no strengthening of the LP that needs one of them tight can be sharp. (The CE chain itself is unaffected — it is the signed identity $\sum_\Lambda f=\det(\Lambda)^{-1}\sum_{\Lambda^*}\widehat f$, which can be tight — but this rules out a natural family of attempted repairs. Verified against swarm member m5's Theorem 2.1.)
* **Any two-point sum rule at all.** Not merely non-sharp but provably non-sharp with a $4\%$ margin (Li).
* **$d=8$ technology transplanted via half-integral weight.** Obstructed by the non-similarity of $A_3$ and $A_3^*$ (§3.2): the Fricke involution has nothing to close on.

---

## 6. What I would actually try

1. **The local inverse problem, honestly posed.** Fix the Q-system/Delaunay marking scheme, and parametrise scores $\sigma$ of the form "linear functional of (vol $\Omega$, angles, solid angles, edge lengths)". Impose the equality conditions of the FCC star; solve the resulting finite LP for the score coefficients; then check $\sigma<8\,\mathrm{pt}$ on a discretisation of the star space. A successful run would give a *new proof of the local optimality of the FCC/HCP stars* — a real theorem, though one that Hales already proved by less systematic means. The interesting part is that this is the exact $d=3$ analogue of "solve for the magic function from its forced zeros", and unlike the global version it is not ruled out by Li's theorem.
2. **Beat the dodecahedral bound $1.4414$.** This, not $1.4711$, is the real frontier: the record in $d=3$ other than Kepler is Hales–McLaughlin's local bound ($1.9\%$ above truth), which leaves a $1.9\%$ window for a sharper local argument. A plausible route is a *cluster* version of the dodecahedral inequality — replace "one cell $\ge$ dodecahedron" by a two- or three-cell inequality (a small LP over the shapes of adjacent Voronoi cells and their shared facet), which is exactly the "average over clusters" mechanism Hales uses in the Kepler proof. Even a bound at $1.43$ would be the best known in $d=3$ after Kepler. The cap of §5.3(i) makes this necessity rather than preference: the entire per-point-volume family is provably capped at $1.4413658597$, so beating it *requires* a genuine multi-cell (cluster) inequality.
3. **An analytic proof of non-sharpness in $d=3$.** Upgrade §3.2 from diagnosis to theorem: show that any weight-$1/2$ Gaussian superposition whose weight is modular for the Fricke involution produces $f,\widehat f$ vanishing on *the same* radius family, hence cannot satisfy both zero conditions. This would remove the computer from Li's $d=3$ result.
4. **Sharpen the $\sqrt2$-vs-$1.4892$ picture.** Is the $d=3$ LP value exactly CE's $1.48928$, or strictly below? My computation says $1.48920\pm0.00002$; a rigorous proof needs a Sturm-type argument on the optimal polynomial (§7 gives the routine).

---

## 7. Log of computations

All scripts are in `.scratch/dim3/` of this repository; all numbers below are reproducible from them.

* `basis_check.py` — verifies $\widehat{\varphi_k}=(-1)^k\varphi_k$ in $d=3$ by direct radial quadrature ($f\mapsto\widehat f$ via $\widehat f(s)=\frac2s\int_0^\infty rf(r)\sin(2\pi sr)\,dr$), for $k\le4$ at six radii; agreement to $10^{-12}$ or better except where the values themselves are $<10^{-16}$.
* `CE3.py` — the $d=3$ LP in the Laguerre basis, grid $2000$ points on each side, `scipy.optimize.linprog`/HiGHS. Produces the convergence table of §4.1, limit $1.48920$.
* `hp.py`, `hpdiag.py` — re-evaluation of the optimal certificate at $50$–$60$ decimal digits with `mpmath` (Laguerre three-term recurrence); confirms $\max_{r\ge1}f(r)\le10^{-8}$, $\min\widehat f\ge-10^{-7}$ (grid artefacts of the float LP solution) and the shell values of §4.1.
* `poisson.py`, `ptest2.py`, `diag.py` — lattice enumeration: $r_3(n)$ by brute force to $n=2400$, shells of $A_3$ and $A_3^*$, multiplicities, and the Poisson identity $\sum_Lf=\sqrt2\sum_{L^*}\widehat f$ checked to all printed digits ($0.982905991434$ both ways). (An earlier version of this script had a bug in the half-integer shell multiplicities; the brute-force enumeration over $\mathbb Z^3\cup(\mathbb Z+\frac12)^3$ is what settled it.)
* `constrained.py` — the constrained LPs of §4.3.
* `fig.py`, `fig2.py` — the figures (`fig-CE-dim3.png`, `fig-CE-dim3-log.png`): the optimal certificate and its transform, with the two shell families marked.

Checks of the arithmetic facts of §2–§3: exact enumeration of $\mathcal S(A_3)$ and $\mathcal S(A_3^*)$ to $r^2=400$ and beyond (Legendre form confirmed, $k=14,30,46,56$ empty); closed theta forms $\Theta_{A_3}=\frac12(\theta_3^3(\tau/2)+\theta_4^3(\tau/2))$ and $\Theta_{A_3^*}=\theta_3^3(2\tau)+\theta_2^3(2\tau)$ matched against enumeration to $r^2=1600$; Poisson reciprocity $\Theta_{A_3^*}(-1/\tau)=\det(L)(\tau/i)^{3/2}\Theta_{A_3}(\tau)$ verified at $\tau=i,2i$ to $10^{-40}$; minimal-vector counts $12$ versus $8$ (whence non-similarity).

**What is not verified.** Li's theorem is used as a black box (I read the statement and the $d=3$ constants, not the $7000$-digit certificate). CDLS's $0.183889$ is quoted from Li's paper, where it appears as the best non-Hales bound; I did not recompute it. CE's $0.18616$ is quoted from their Table 3, which I read in the source text. My LP values are numerical (grid + float LP); the *upper* bounds they suggest are not rigorous, but CE's $1.48928$ is, and my value lies below it, as it must.

---

## 8. Summary of what changed in my understanding

Before doing this I would have said: "the CE bound is $5\%$ off in $d=3$, and Viazovska's method works in $8$ and $24$, so presumably a cleverer function would fix $d=3$." Four things are now clear and each is a real constraint on any attempt:

1. It is **not** a matter of cleverness: the LP is provably non-sharp (Li 2024), with a rigorous margin of $4\%$.
2. The obstruction has an **arithmetic shape**: $A_3$ is the first extremal lattice that is not isodual, so the sharp certificate's two zero families are different ($\{k:2k\in 3\text{-squares}\}$ versus $\{2m\}\cup\{4j+\frac32\}$), and the Fricke/modular mechanism has nothing to close on.
3. The LP-optimal $d=3$ certificate is **nearly** sharp — it satisfies the complementary-slackness zeros to $10^{-3}$–$10^{-8}$ and cannot do better; the slack splits $1{:}2$ between primal and dual mass. The failure is quantitative and located, not mysterious.
4. The sharp $d=3$ bounds that do exist are **local** (Hales' star score, proved by $10^5$ small LPs). So the honest answer to "a sharp CE-type bound in three dimensions" is: *not one function, but one score; not an inverse problem over modular forms, but an inverse problem over local configurations — and that problem is open and concrete.*
