# d11 — Ground-field spectrum of the Hadwiger–Nelson unit-distance graph

Member m5, swarm smwfcr56i. Direction d11.

Everything below is proved from scratch; the exact-arithmetic checks referenced as
`C1`–`C9` are in `verify.py`, whose output is `log.txt` (reproduce with
`python3 verify.py`). No floating point is used anywhere; the Moser spindle is
verified in the field $\mathbb{Q}(\sqrt3,\sqrt{11})$ with basis $1,\sqrt3,\sqrt{11},\sqrt{33}$.

## 0. Results

* **T1 (parity lemma).** No closed walk of unit steps with *rational* displacement
  vectors has odd length. Hence the rational-displacement unit-distance graph on
  $\mathbb{R}^2$ is bipartite — an independent proof of the fact quoted in the
  paper's §1 from Payne [22] — and consequently $\chi(\mathbb{Q}^2)=2$.
* **T2 (field ladder).** $\chi(\mathbb{Q}(\sqrt3)^2)\ge 3$,
  $\chi(\mathbb{Q}(\sqrt{11})^2)\ge 3$,
  $\chi(\mathbb{Q}(\sqrt3,\sqrt{11})^2)\ge 4$, with exact coordinates and a
  complete non-3-colourability proof of the 7-vertex Moser spindle.
* **T3 (arithmetization).** For every $k$: the plane is $k$-colourable **iff** the
  real-algebraic plane is. Hence $\chi(\mathbb{R}^2)=\chi(E^2)$, $E=$ real algebraic
  numbers, and moreover
  $\chi(\mathbb{R}^2)=\max\{\chi(F^2):F\subseteq\mathbb{R}\text{ a number field}\}$:
  a *single* number field's plane already has the chromatic number of the plane. So
  the de Bruijn–Erdős witness for a lower bound can always be taken with exact
  algebraic coordinates in one number field, and the Hadwiger–Nelson problem is
  equivalent to a problem about a *countable* graph. Moreover $\chi(F^2)$ is
  *constant*, equal to $\chi(\mathbb{R}^2)$, on all real closed subfields
  $F\subseteq\mathbb{R}$ (Theorem 7c).
* **T4 (delineation of the lower bound's necessary inputs).** $\mathbb{Q}$ is an
  ordered field and $\mathbb{Q}^2$ is dense in $\mathbb{R}^2$, yet
  $\chi(\mathbb{Q}^2)=2$ while $\chi(\mathbb{R}^2)\ge 6$; and $E$ is countable and
  not complete, yet $\chi(E^2)=\chi(\mathbb{R}^2)$. So a proof of
  $\chi(\mathbb{R}^2)\ge 6$ can rest neither on the ordered-field axioms (with
  density) nor on completeness or uncountability as such. What it must use is the one
  property $E$ has and $\mathbb{Q}$ lacks: real-closedness, i.e. realizability of
  every finite unit-distance configuration.

## 1. Notation

For a subfield $F\subseteq\mathbb{R}$, let $G_F$ be the graph with vertex set $F^2$
and $x\sim y$ iff $\lVert x-y\rVert=1$. Put $\chi(F^2):=\chi(G_F)$; $G_{\mathbb R}$
is the Hadwiger–Nelson graph. Let $G_{\mathrm{rat}}$ be the graph on $\mathbb{R}^2$
with $x\sim y$ iff $y-x\in\mathbb{Q}^2$ and $\lVert y-x\rVert=1$ ("unit steps in
rational directions"). $G_{\mathbb Q}$ is the induced subgraph of
$G_{\mathrm{rat}}$ on $\mathbb{Q}^2$: if $x,y\in\mathbb{Q}^2$ and
$\lVert x-y\rVert=1$, then $y-x$ is a rational unit vector. Both graphs are
loopless and $G_{\mathbb Q}\subseteq G_{\mathrm{rat}}[\,\mathbb{Q}^2\,]$.

Throughout, $E$ denotes the field of real algebraic numbers. (The paper's §1 uses the
letter $E$ for the complexification $F(i)$ of the real algebraic field $F$; that is
$F^2$ as an $F$-vector space, i.e. the same object as our $E^2$, so no confusion
arises once the identification is made.)

A *unit vector* is $u\in\mathbb{R}^2$ with $\lVert u\rVert=1$. A *walk of length
$n$* from $x$ to $y$ is a sequence $x=x_0,\dots,x_n=y$ with consecutive differences
in the relevant edge set; its displacement list is $(u_1,\dots,u_n)$,
$u_j=x_j-x_{j-1}$.

## 2. T1: the parity lemma

**Lemma 1.** Let $n\ge 1$ and let $u_1,\dots,u_n\in\mathbb{Q}^2$ be unit vectors with
$\sum_{j=1}^n u_j=0$. Then $n$ is even.

*Proof.* Write $u_j=(a_j/c_j,\;b_j/c_j)$ in lowest terms, i.e. $a_j,b_j\in\mathbb{Z}$,
$c_j\ge1$, $\gcd(a_j,b_j,c_j)=1$. Then

* $a_j^2+b_j^2=c_j^2$ (since $\lVert u_j\rVert=1$);
* $\gcd(a_j,b_j)=1$: a prime $p$ dividing $a_j$ and $b_j$ divides $c_j^2$, hence $c_j$,
  contradicting $\gcd(a_j,b_j,c_j)=1$;
* $c_j$ is odd: if $c_j$ were even then $a_j^2+b_j^2\equiv 0\pmod 4$, so $a_j,b_j$ are
  both even, contradicting $\gcd(a_j,b_j)=1$.

Let $D=\operatorname{lcm}(c_1,\dots,c_n)$, which is odd, and put
$v_j:=D\,u_j\in\mathbb{Z}^2$. Then $\lVert v_j\rVert^2=D^2$ and
$\sum_j v_j=D\sum_j u_j=0$. Since $D^2$ is odd, for every $j$ the two coordinates of
$v_j$ have opposite parity, so
$$s_j:=(v_j)_1+(v_j)_2\quad\text{is odd.}$$
Summing, $\sum_{j=1}^n s_j=(D\sum_j u_j)_1+(D\sum_j u_j)_2=0$. A sum of $n$ odd
integers is $\equiv n \pmod 2$; being $0$, it forces $n$ even. $\square$

The rationality hypothesis is essential: $(1,0)+(-1/2,\sqrt3/2)+(-1/2,-\sqrt3/2)=0$
is a closed walk of length $3$ (check `C4`), and the same in $5$ steps over
$\mathbb{Q}(\sqrt{11})$ is `C3`.

**Corollary 2.** (a) Every closed walk in $G_{\mathrm{rat}}$ has even length.
(b) $G_{\mathrm{rat}}$ is bipartite, hence so is every induced subgraph, in
particular $G_{\mathbb Q}$; therefore $\chi(\mathbb{Q}^2)=2$.

*Proof.* (a) The displacement list of a closed walk in $G_{\mathrm{rat}}$ consists of
rational unit vectors summing to $0$; apply Lemma 1.
(b) If $x,y$ lie in the same component of $G_{\mathrm{rat}}$ and $P,Q$ are walks from
$x$ to $y$ of lengths $m,n$, then $P$ followed by the reverse of $Q$ is a closed walk
of length $m+n$, even by (a); so $m\equiv n \pmod 2$. Fix once and for all a
well-ordering of $\mathbb{R}^2$ and, for each component $C$, let $b_C$ be its least
element. Define $\psi(x):=$ parity of the length of any walk $b_C\to x$, $C$ the
component of $x$. Then $x\sim y$ implies $\psi(x)\neq\psi(y)$, so
$x\mapsto\psi(x)\bmod 2$ is a proper $2$-colouring of $G_{\mathrm{rat}}$. Finally
$\chi(\mathbb{Q}^2)\ge2$ because $(0,0)\sim(1,0)$. For $G_{\mathbb Q}$ the
well-ordering used can be taken to be a definable well-ordering of the countable set
$\mathbb{Q}^2$ (e.g. via a fixed bijection with $\mathbb{N}$), so the $2$-colouring of
$\mathbb{Q}^2$ is definable in ZF without any choice principle. $\square$

**Proposition 3 (explicit form of the colouring on the component of the origin).**
Let $\Gamma\le\mathbb{R}^2$ be the subgroup generated by the rational unit vectors;
this is exactly the component of $0$ in $G_{\mathrm{rat}}$. Normalise the potential of
Corollary 2 on $\Gamma$ by $\psi(0)=0$ (this only flips colours inside $\Gamma$).
Then

1. $\mathbb{Z}^2\subseteq\Gamma$;
2. every element of $\Gamma$ has, in lowest terms, odd denominators;
3. for $x=(p/q,r/q)\in\Gamma$ with $q$ odd one has $\psi(x)\equiv p+r\pmod 2$, and
   this is independent of the representation: if also $x=(p'/q',r'/q')$ with $q'$
   odd, then $p+r\equiv p'+r'\pmod2$;
4. $\psi\colon\Gamma\to\mathbb{Z}/2$ is a homomorphism and $\psi(u)=1$ for every
   rational unit vector $u$.

*Proof.* 1: $(\pm1,0)$ and $(0,\pm1)$ are rational unit vectors. 2: a finite sum of
fractions with odd denominators has denominator dividing the lcm of those
denominators, which is odd. 3: from $pq'=p'q$ with $q,q'$ odd, $p\equiv p'\pmod 2$,
and likewise $r\equiv r'\pmod 2$, so the expression is well defined. It is a
homomorphism: for $x=(p_1/q,r_1/q)$, $y=(p_2/q,r_2/q)$ with $q$ odd, the sum
$x+y=((p_1+p_2)/q,(r_1+r_2)/q)$ equals $((p_1+p_2)/d,(r_1+r_2)/d)$ in lowest terms
with $d\mid q$ odd, and for odd $d$ one has
$(p_1+p_2)+(r_1+r_2)\equiv\frac{p_1+p_2}{d}+\frac{r_1+r_2}{d}\pmod 2$; hence
$\psi(x+y)\equiv\psi(x)+\psi(y)$. 4: a walk of length $1$ is a unit vector, so
$\psi(u)=1$ for a unit vector $u$ in $\Gamma$; and for $u=(a/c,b/c)$ primitive,
$a^2+b^2=c^2$ with $c$ odd (Lemma 1), so exactly one of $a,b$ is even and
$a+b\equiv1\pmod2$, in agreement with 3. $\square$

Checks `C8` (well-definedness, additivity, $\psi(u)=1$ for all $28$ unit vectors with
denominators in $\{1,5,13,17\}$, $20\,000$ random samples each) and `C1` (parity of
primitive hypotenuses for all $484$ triples with $c\le600$, $95$ of them primitive)
test 3 and 4.

**Corollary 4 (finite witnesses cannot be rational).** Every finite unit-distance
graph all of whose coordinates are rational is bipartite, hence $2$-colourable;
indeed every finite subgraph of $G_{\mathrm{rat}}$ is bipartite, i.e. has no odd
cycle. Consequently a de Bruijn–Erdős witness for
$\chi(\mathbb{R}^2)\ge k$ ($k\ge3$) cannot have all coordinates rational.

This is a genuine restriction on any finite-witness search (mandate H of the
swarm): rational coordinates are provably useless. `C2` illustrates it: with the
$28$ rational unit vectors of denominators $1,5,13,17$ there is no closed walk of
length $3$, $5$ or $7$ at all.

**Remark 5 (components).** $G_{\mathrm{rat}}$ is not connected: by Proposition 3(2)
every point of $\Gamma$ has odd denominators in lowest terms, so
$(\tfrac12,0)\notin\Gamma$, i.e. $(\tfrac12,0)$ and $(0,0)$ are in different
components. The base point $b_C$ in Corollary 2 is therefore genuinely needed: the
colouring is canonical on $\Gamma$ (Proposition 3(3)) and free by one bit per
component elsewhere. `C7` checks the induced subgraph of $G_{\mathrm{rat}}$ on the
$3225$ points $\{(p/q,r/q):q\in\{1,5,13\},\ |p|,|r|\le 2q\}$: $27\,936$ edges,
bipartite, and *every* edge flips the potential of Proposition 3 — a finite
confirmation of Corollary 2 in a case where a single component is involved.

## 3. T2: the field ladder

**Proposition 6.** (a) $\chi(\mathbb{Q}(\sqrt3)^2)\ge3$. (b)
$\chi(\mathbb{Q}(\sqrt{11})^2)\ge3$. (c) $\chi(\mathbb{Q}(\sqrt3,\sqrt{11})^2)\ge4$.

*Proof.* (a) Equilateral triangle $(0,0),(1,0),(\tfrac12,\tfrac{\sqrt3}2)$: the three
squared edge lengths are $1$ (check `C4`).

(b) The five points
$$(0,0),\quad(\tfrac35,\tfrac45),\quad(\tfrac65,0),\quad(\tfrac15,0),\quad(\tfrac1{10},\tfrac{3\sqrt{11}}{10})$$
are distinct and consecutive differences are
$(\tfrac35,\tfrac45)$, $(\tfrac35,-\tfrac45)$, $(-1,0)$,
$(\tfrac1{10}-\tfrac15,\tfrac{3\sqrt{11}}{10})=(-\tfrac1{10},\tfrac{3\sqrt{11}}{10})$
and $(-\tfrac1{10},-\tfrac{3\sqrt{11}}{10})$, each of squared length
$\tfrac1{100}+\tfrac{99}{100}=1$. So a $5$-cycle exists over
$\mathbb{Q}(\sqrt{11})$ (no $\sqrt3$ needed); in particular $G_{\mathbb{Q}(\sqrt{11})}$
is not bipartite (check `C3`).

(c) The Moser spindle. With $t_1=(0,0)$, $t_2=(\sqrt3,0)$,
$t_3=(\tfrac{\sqrt3}6,\tfrac{\sqrt{33}}6)$, one has
$\lVert t_1-t_2\rVert^2=\lVert t_2-t_3\rVert^2=3$ and $\lVert t_1-t_3\rVert^2=1$.
Let
$$u_{1,2}=\Big(\tfrac{\sqrt3}{2},\pm\tfrac12\Big),\qquad
v_{1,2}=\tfrac{t_2+t_3}{2}\pm\Big(-\tfrac{\sqrt{11}}{12},-\tfrac5{12}\Big).$$
Then $V=\{t_1,t_2,t_3,u_1,u_2,v_1,v_2\}$ are seven distinct points of
$\mathbb{Q}(\sqrt3,\sqrt{11})^2$, and the unit-distance pairs among them are exactly
the $11$ pairs
$$\{t_1u_1,t_1u_2,t_2u_1,t_2u_2,u_1u_2\}\ \cup\
\{t_2v_1,t_2v_2,t_3v_1,t_3v_2,v_1v_2\}\ \cup\ \{t_1t_3\}.$$
This is verified exactly in $\mathbb{Q}(\sqrt3,\sqrt{11})$ in `C5`: all $11$ listed
squared distances are $(1,0,0,0)$ and no other of the $21$ pairs has squared
distance $1$ (the others are $3$, $\tfrac32\mp\tfrac{\sqrt{33}}6$,
$\tfrac76\mp\tfrac{\sqrt{33}}6$, $\tfrac13$, each $\neq1$ in the basis
$1,\sqrt3,\sqrt{11},\sqrt{33}$).

$V$ is not $3$-colourable: let $c$ be a proper $3$-colouring. The four points
$t_1,t_2,u_1,u_2$ span $K_4$ minus the edge $t_1t_2$; since $t_1\not\sim t_2$ and
$u_1\sim u_2$, $u_1$ and $u_2$ are adjacent to both $t_1$ and $t_2$, so
$\{c(t_1),c(t_2)\}=\{1,2,3\}\setminus\{c(u_1)\}=\{1,2,3\}\setminus\{c(u_2)\}$ and
hence $c(t_1)=c(t_2)$. The same argument on $t_2,t_3,v_1,v_2$ gives
$c(t_2)=c(t_3)$. But $t_1\sim t_3$, contradiction. `C6` confirms this exhaustively:
$0$ proper colourings out of $3^7=2187$, while a proper $4$-colouring exists, e.g.
$t_1\mapsto0,t_2\mapsto0,t_3\mapsto1,u_1\mapsto1,u_2\mapsto2,v_1\mapsto2,v_2\mapsto3$.
$\square$

Together with Corollary 2 and monotonicity ($F\subseteq F'\Rightarrow
\chi(F^2)\le\chi(F'^2)$) this gives
$$2=\chi(\mathbb{Q}^2)\ \le\ \chi(\mathbb{Q}(\sqrt3)^2),\ \chi(\mathbb{Q}(\sqrt{11})^2)\ \le\ \chi(\mathbb{Q}(\sqrt3,\sqrt{11})^2),\quad
\chi(\mathbb{Q}(\sqrt3)^2)\ge3,\ \chi(\mathbb{Q}(\sqrt3,\sqrt{11})^2)\ge4.$$
The jumps are real: $\mathbb{Q}^2$ has no odd cycle at all (T1) while an odd cycle
already appears over $\mathbb{Q}(\sqrt3)$ and over $\mathbb{Q}(\sqrt{11})$.

## 4. T3: arithmetization

**Theorem 7.** Let $E\subseteq\mathbb{R}$ be the field of real algebraic numbers.

(a) For every positive integer $k$: $G_E$ is $k$-colourable $\iff$ $G_{\mathbb R}$
is $k$-colourable. Hence $\chi(E^2)=\chi(\mathbb{R}^2)$.

(b) $\chi(\mathbb{R}^2)=\max\{\chi(F^2):F\subseteq\mathbb{R}\ \text{number field}\}$:
the supremum over finite extensions of $\mathbb{Q}$ is attained.

Note that (b) is *not* the claim "$\chi(F^2)=\chi(\mathbb{R}^2)$ for each $F$": that
is false, $\chi(\mathbb{Q}^2)=2$ (Corollary 2) whereas $\chi(\mathbb{R}^2)\ge6$.
Realizations descend to some finite extension of $\mathbb{Q}$, not to a prescribed one.

*Proof.* (a), direction $\Leftarrow$: $G_E$ is the induced subgraph of $G_{\mathbb R}$
on $E^2$, so a $k$-colouring of $G_{\mathbb R}$ restricts to one of $G_E$.

(a), direction $\Rightarrow$: assume $G_E$ is $k$-colourable and let $X\subseteq
\mathbb{R}^2$ be finite. By Lemma 8 there is a finite $X'\subseteq E^2$ and a
bijection $X\to X'$ preserving unit distances, so
$\chi(G_{\mathbb R}[X])=\chi(G_E[X'])\le k$. Hence every finite unit-distance graph
realized in the plane is $k$-colourable, and by de Bruijn–Erdős $G_{\mathbb R}$ is
$k$-colourable.

(b) By de Bruijn–Erdős, for any $F\subseteq\mathbb{R}$,
$\chi(F^2)=\sup\{\chi(G_F[X]):X\subseteq F^2\ \text{finite}\}$, and $\chi$ is a
monotone function of $F$. Since every finite $X\subseteq E^2$ has algebraic
coordinates, the field $F_X=\mathbb{Q}(X)$ is a number field with $X\subseteq F_X^2$,
so
$$\chi(\mathbb{R}^2)\overset{(\mathrm a)}{=}\chi(E^2)=\sup_{X}\chi(G_E[X])\le
\sup_{F\ \text{number field}}\chi(F^2)\le\chi(\mathbb{R}^2),$$
the last inequality because $F^2\subseteq\mathbb{R}^2$. For attainment: $\chi(\mathbb{R}^2)\le7$
is finite, so by de Bruijn–Erdős $\chi(\mathbb{R}^2)=\chi(G_{\mathbb R}[X])$ for some
finite $X\subseteq\mathbb{R}^2$; Lemma 8 gives $X'\subseteq F^2$ with
$\chi(G_F[X'])=\chi(G_{\mathbb R}[X])$ for a number field $F$, whence
$\chi(F^2)=\chi(\mathbb{R}^2)$. $\square$

The transfer step, isolated:

**Lemma 8 (realizations descend to algebraic coordinates).** Let $G$ be a finite graph
with $m$ vertices. If $G$ is isomorphic to a unit-distance graph realized in
$\mathbb{R}^2$, then it is isomorphic to one realized in $E^2$, indeed in $F^2$ for
some number field $F$.

*Proof.* Enumerate $V(G)=\{1,\dots,m\}$ and let $\varphi(x_1,\dots,x_m)$ be the
first-order formula, in the language of ordered fields with integer parameters,
$$\exists x_1\dots\exists x_m\ \bigwedge_{ij\in E(G)}\lVert x_i-x_j\rVert^2=1\
\wedge\bigwedge_{\substack{i<j\\ ij\notin E(G)}}\lVert x_i-x_j\rVert^2\neq1 .$$
Here $\lVert x_i-x_j\rVert^2=(x_{i1}-x_{j1})^2+(x_{i2}-x_{j2})^2$ is a polynomial
with integer coefficients. A realization of $G$ in $\mathbb{R}^2$ is exactly a
witness for $\varphi$ in $\mathbb{R}$; note that distinctness of the vertices is
automatic, since an edge forces distance $1$. The theory of real closed fields is
model complete (Tarski–Seidenberg), $\mathbb{R}$ and $E$ are real closed, and
$\varphi$ has parameters in $\mathbb{Q}\subseteq E$; hence $\varphi$ holds in $E$.
The $2m$ witnesses are algebraic, so they lie in a common number field $F$. $\square$

**Theorem 7c (invariance on real closed subfields).** Let $F\subseteq\mathbb{R}$ be a
real closed subfield. Then $\chi(F^2)=\chi(\mathbb{R}^2)$. Since $E$ is the least real
closed subfield of $\mathbb{R}$, the value $\chi(\mathbb{R}^2)$ is already attained at
the least possible such field.

*Proof.* $\le$: $F^2\subseteq\mathbb{R}^2$. $\ge$: let $X\subseteq\mathbb{R}^2$ be
finite. The formula $\varphi$ of Lemma 8 for $G_{\mathbb R}[X]$ has parameters in
$\mathbb{Q}\subseteq F$, holds in the real closed field $\mathbb{R}$, hence holds in
the real closed field $F$; so $G_F$ contains a copy of $G_{\mathbb R}[X]$ and
$\chi(\mathbb{R}^2)=\sup_X\chi(G_{\mathbb R}[X])\le\chi(F^2)$. $\square$

So the plane's chromatic number is a property of the *real-closed* structure alone; the
only way to make it drop is to leave the class of real closed fields (over
$\mathbb{Q}$ it is $2$).

**Corollary 9 (what a finite witness looks like).** If $\chi(\mathbb{R}^2)\ge k$
then there is a finite unit-distance graph $G$ with $\chi(G)\ge k$ whose vertices
have *exact algebraic coordinates, all lying in a single number field*. (By
de Bruijn–Erdős such a $G$ exists at all; Lemma 8 upgrades its coordinates.)

So the exact-certificate format demanded by the problem statement ("vertices with
exact algebraic coordinates, complete edge list, exact verification") is attainable
in principle — it is not an extra restriction on the finite witness. It also
explains why all published 5-chromatic unit-distance graphs have algebraic
coordinates.

**Corollary 10 (the problem is about a countable graph).** For every $k$,
$\chi(\mathbb{R}^2)\le k \iff \chi(E^2)\le k$. Thus Hadwiger–Nelson is equivalent to
a statement about the countable graph $G_E$ — and, by Theorem 7, to a statement
about the family of plane unit-distance graphs over number fields.

**Corollary 11 (the paper's use of the algebraic plane loses nothing).** The paper's
§1 begins "Let $F$ be the field of real algebraic numbers, $E=F(i)$ the algebraic
plane, … restrict a proper coloring to the countable set $E$". Under the
identification of the paper's $E$ with $F^2$ (see §1), Corollary 10 says that the
final statement is unaffected by this restriction: $\chi(\mathbb{R}^2)\ge6$ iff
$\chi(F^2)\ge6$. (This is a check of the *statement*; the paper still needs its
measurable transfer to move colourings, not just chromatic numbers, between $F$ and
$\mathbb{R}$.)

**Proposition 12 (the top of the ladder).** Let $F\subseteq\mathbb{R}$ be a subfield
with $\mathbb{Q}(\sqrt3)\subseteq F$. Then $\chi(F^2)\le7$. In particular
$\chi(E^2)=\chi(\mathbb{R}^2)\le7$, and for $F=\mathbb{Q}(\sqrt3,\sqrt{11})$,
$$4\le\chi(F^2)\le7 .$$

*Proof.* Use the hexagonal colouring of the paper's §1 (Hadwiger/Isbell), with the
tie-break made canonical so that it is $F$-valued. Let $r=2/5$,
$\omega=e^{2\pi i/3}$, and $\Lambda=r\sqrt3\,(\mathbb{Z}+\mathbb{Z}\omega)\subseteq
\mathbb{Q}(\sqrt3)^2\subset F^2$; the Voronoi hexagons of $\Lambda$ have circumradius
$r$. For $x\in F^2$ let $m(x)\in\Lambda$ be the nearest lattice point, ties broken by
the lexicographically least lattice coordinate pair; since $x\in F^2$ and
$\Lambda\subseteq F^2$, all comparisons involved are between elements of $F$, so
$m(x)\in F^2$, and $c(x):=$ (the coset of $m(x)$ in $\Lambda/(2-\omega)\Lambda$,
a set of $7$ cosets, labelled $0,\dots,6$) is well defined and $F$-valued. If $\lVert
x-y\rVert=1$ then $x,y$ are not in the same hexagon, because a hexagon has diameter
$2r<1$; and they are not in distinct hexagons of the same colour, because centres of
distinct same-colour hexagons are at distance $\ge\sqrt{21}\,r$ and hexagons of
circumradius $r$ with centres at distance $d$ are at distance $\ge d-2r$, and
$(\sqrt{21}-2)r>1$. Hence $c$ is proper. $\square$

The two inequalities used are exact: $2r=4/5<1$, and $(\sqrt{21}-2)\cdot\frac25>1$
because $2\sqrt{21}>9$ (square: $84>81$), and $\sqrt{21}r=\lvert2-\omega\rvert\cdot
\sqrt3\,r$ with $\lvert2-\omega\rvert^2=7$. Check `C9` verifies
$\lvert 2-\omega\rvert^2=7$, $2\sqrt{21}>9$ and $2r<1$ in exact integer arithmetic.
(For a detailed boundary audit of this colouring see the m12 direction d8; the point
here is only that it is $F$-valued.)

So the ladder reads, with $F_0=\mathbb{Q}(\sqrt3,\sqrt{11})$,
$$2=\chi(\mathbb{Q}^2)\ \le\ 3\le\chi(\mathbb{Q}(\sqrt3)^2),\ \chi(\mathbb{Q}(\sqrt{11})^2)\ \le\ \chi(F_0^2)\ \le\ 7,
\qquad \chi(E^2)=\chi(\mathbb{R}^2)\in\{6,7\},$$
and $\chi(F^2)=\chi(\mathbb{R}^2)$ for *some* number field $F\subseteq E$ (Theorem 7(b)).

## 5. T4: what the lower bound can and cannot rest on

The paper proves $\chi(\mathbb{R}^2)\ge 6$ with no regularity hypothesis
(Theorem 1.1). Three consequences of T1/T3 delimit the possible inputs to any such
proof.

1. **Not the ordered-field axioms, even with density.** $\mathbb{Q}$ is an ordered
   field, $\mathbb{Q}^2$ is dense in $\mathbb{R}^2$, and $\chi(\mathbb{Q}^2)=2$
   (Corollary 2). So no proof of $\chi(\mathbb{R}^2)\ge6$ that is valid in the theory
   of ordered fields — or of dense ordered fields — can exist. In particular the
   argument must use more than the unit-distance *combinatorics of rational
   directions*: over $\mathbb{Q}$ there is no odd cycle at all.
2. **Not completeness, and not uncountability.** $E$ is countable and is not
   complete (it does not contain $\pi$; it is not Dedekind complete), yet
   $\chi(E^2)=\chi(\mathbb{R}^2)\ge6$ by Theorem 7. So neither uncountability nor
   the least-upper-bound property can be an indispensable ingredient, and measure
   theory on $\mathbb{R}^2$ is a *tool*, not a necessity at the level of the
   statement: the statement is already carried by a countable null set.
3. **What is indispensable is real-closedness** — the realization of all finite
   unit-distance configurations. $\mathbb{Q}$ fails already for the equilateral
   triangle (Proposition 6(a): the third vertex needs $\sqrt3$), and by Lemma 8 this
   is the *only* obstruction to descending realizations to a field: any field that
   is real closed (or merely closed under the algebraic realizations of unit-distance
   configurations) carries $\chi=\chi(\mathbb{R}^2)$. Consequently any proof of
   $\chi\ge6$ must combine the algebraic/geometric structure of $E$ with an
   ingredient that is *not* available over $\mathbb{Q}$ — in this paper, the
   measure-theoretic non-existence of a weak measurable 5-colouring
   (Theorem 1.4), which by Corollary 10 has a conclusion about the countable
   graph $G_E$ even though its proof uses Lebesgue measure on $\mathbb{R}^2$.

A remark connecting 1. and 3.: by Theorem 7 the chromatic number of the plane is the
maximum of $\chi(F^2)$ over number fields; with Proposition 6 the ladder starts
$2=\chi(\mathbb{Q}^2)$, then $\ge3$ over $\mathbb{Q}(\sqrt3)$ and
$\mathbb{Q}(\sqrt{11})$, then $\ge4$ over $\mathbb{Q}(\sqrt3,\sqrt{11})$, and reaches
the true value in $\{6,7\}$ at some number field (Corollary 9). The whole difficulty
of the problem is thus localized in a single jump between finite-degree fields.

## 6. Verification

`verify.py` (exact arithmetic only, no floats; field $\mathbb{Q}(\sqrt3,\sqrt{11})$
implemented as $a+b\sqrt3+c\sqrt{11}+d\sqrt{33}$, $a,b,c,d\in\mathbb{Q}$):

| check | content | result |
|---|---|---|
| C1 | primitive Pythagorean triples with $c\le600$ | $95$ primitive, all odd hypotenuse |
| C2 | closed rational unit walks of length $3,5,7$ over $28$ directions | none |
| C3 | $5$-cycle over $\mathbb{Q}(\sqrt{11})$ | $5$ distinct vertices, all $5$ edges unit |
| C4 | $3$-cycle over $\mathbb{Q}(\sqrt3)$ | all $3$ edges unit |
| C5 | Moser spindle in $\mathbb{Q}(\sqrt3,\sqrt{11})^2$ | $7$ vertices, $11$ edges, all unit, no other unit pair |
| C6 | colourings of the spindle | $0/2187$ proper $3$-colourings; a proper $4$-colouring exists |
| C7 | $G_{\mathrm{rat}}$ on $3225$ points, $q\in\{1,5,13\}$ | $27\,936$ edges, bipartite, every edge flips $\psi$ |
| C8 | potential $\psi(p/q,r/q)=p+r \bmod 2$ | well defined, $\psi(u)=1$ for all $28$ unit vectors, additive (no failures) |
| C9 | hexagonal colouring arithmetic: $\lvert2-\omega\rvert^2$, index, sublattice minimum, $2r<1$, $2\sqrt{21}>9$ | $7$, $7$, $7$, true, true |

Reproduce: `cd .ultramath/smwfcr56i/m5 && python3 verify.py`.

## 7. What is not claimed

* The rational-displacement $2$-colouring is not new as a fact: the paper's §1
  attributes it to Payne [22]. Lemma 1 and Corollaries 2–4 give a self-contained
  proof and the explicit potential of Proposition 3; no priority is claimed.
  Likewise the Moser spindle is Moser–Moser 1961; §3(c) only records it in exact
  arithmetic over the stated field.
* I could not check the literature for Theorem 7 (χ(R²) = χ(E²)) — web search was
  unavailable in this environment (HTTP 402). The theorem is proved here from
  Tarski–Seidenberg and de Bruijn–Erdős; I make no priority claim, but the proof is
  complete and the statement is the load-bearing part of this submission.
* Nothing here bears on 6 vs 7. T4 says only where a proof of the lower bound must
  get its input from.
