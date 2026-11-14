# Rigidity of structured colourings of the Euclidean plane

Member m10, swarm `smwfcr56i`, direction d10 ("structured-substitute rigidity").
Status: complete proofs; exact arithmetic checked by `verify_rigidity.py` (log: `verify_rigidity.log`).

**Notation.** $\mathbb R^2$ is the Euclidean plane, $|x-y|$ the Euclidean distance.
A set $A\subseteq\mathbb R^2$ is **unit-free** if $|x-y|\neq 1$ for all $x,y\in A$ with $x\neq y$.
A **colouring** is any map $c:\mathbb R^2\to\{1,\dots,k\}$; it is **proper** if
$|x-y|=1 \Rightarrow c(x)\neq c(y)$. Equivalently: every colour class $c^{-1}(i)$ is unit-free.
$\chi(\mathbb R^2)$ is the least $k$ for which a proper colouring exists; the attached paper proves
$\chi(\mathbb R^2)\ge 6$ (its Theorem 1.1) and $\chi(\mathbb R^2)\le 7$ (its §1), so $\chi\in\{6,7\}$.

**What this note does and does not do.** It does *not* produce a lower bound. It proves that
four explicitly stated structured families of colourings cannot be proper with finitely many
colours, **for every finite $k$** — i.e. those families are not merely unable to reach $6$, they
cannot reach any finite number. It also corrects one tempting but false strengthening
(§8), and records the resulting constraint on any hypothetical $6$- or $7$-colouring (§9).

---

## 1. The one geometric fact

**Lemma 1 (connected unit-free sets have diameter $\le 1$).**
Let $C\subseteq\mathbb R^2$ be connected and unit-free. Then $|x-y|\le 1$ for all $x,y\in C$.

*Proof.* Suppose $p,q\in C$ with $|p-q|>1$. The map $\varphi:C\times C\to\mathbb R$,
$\varphi(x,y)=|x-y|$, is continuous; $C\times C$ is connected (product of connected spaces), so
$\varphi(C\times C)$ is a connected subset of $\mathbb R$, i.e. an interval. It contains
$\varphi(p,p)=0$ and $\varphi(p,q)>1$, hence it contains $1$. So there are $x,y\in C$ with
$|x-y|=1$; since $1\neq0$ we have $x\neq y$, contradicting unit-freeness. $\square$

*Variant.* If $C$ is path-connected one can instead take a path $\gamma$ from $p$ to $q$ and apply
the intermediate value theorem to $t\mapsto|\gamma(t)-p|$; connectedness is all that is used above,
so no path-connectedness (and no local connectedness) is needed.

**Remark (forbidden-distance and higher-dimensional versions).** The proof uses nothing about the
plane. Let $D\subseteq(0,\infty)$ be any set of forbidden distances and let $A\subseteq\mathbb R^n$ be
$D$-free, i.e. $|x-y|\notin D$ for distinct $x,y\in A$. For a connected $C\subseteq A$ the set
$\{|x-y|:x,y\in C\}$ is an interval containing $0$ and disjoint from $D$. Hence, for example:
(i) $D=\{1\}$ gives $\operatorname{diam}C\le1$ (Lemma 1, in every $\mathbb R^n$);
(ii) $D=[1,2)$ or $D=(1,\infty)$ also give $\operatorname{diam}C\le1$ — the "$\varepsilon$-relaxed"
constraints, forbidding a whole interval of distances, are no easier for the connectedness mechanism;
(iii) $D\supseteq(0,1]$ forces $C$ to be a single point. In particular Theorem 5 below holds verbatim
in $\mathbb R^n$ for every $n\ge1$: *no finite cover of $\mathbb R^n$ by $D$-free sets with finitely
many components*, for $D=\{1\}$, and equally for any $D$ with $\inf D=1$ and $D\subseteq[1,\infty)$.

**Corollary 2.** Every connected component of a unit-free set has diameter $\le 1$. $\square$

**Lemma 3 ($\Delta$-exclusion; the mechanism of the paper's §7).**
Let $U\subseteq\mathbb R^2$ be unit-free, let $K\subseteq U$ be connected and let $z\in U$. Then
$$\text{not}\Big(\inf_{q\in K}|z-q|<1<\sup_{q\in K}|z-q|\Big).$$
*Proof.* $K$ is connected and $q\mapsto|z-q|$ is continuous, so its image is an interval with
infimum $<1$ and supremum $>1$; hence $1$ is attained: $|z-q|=1$ for some $q\in K$. Then
$q\neq z$ (as $|z-q|=1$) and $z,q\in U$, contradicting unit-freeness. $\square$

Lemma 3 is the exact statement used in the paper's §7: with $K=K_j$ a compact connected set
(strip: $\inf=\min$, $\sup=\max$) whose points are known to carry a label $\ell$, the set $\Delta(K_j)$
contains no point of colour $\ell$. Note the hypothesis $z\in U$: the exclusion is a statement
about points of the *same* class, which is why in the weak-measurable setting of the paper it can
only be asserted **almost everywhere** (a weak measurable colouring determines its classes only
up to null sets, and Lemma 3 has no null-set slack). Lemma 3 needs no compactness, no graph
theory, no planarity: connectedness alone gives the exact unit distance.

---

## 2. Sharpness of the diameter bound

**Proposition 4.** (a) The open disc $B(0,\tfrac12)$ is connected and unit-free, and its diameter is
exactly $1$ (a supremum, not attained). Hence the constant $1$ in Lemma 1 cannot be lowered.

(b) If $C$ is closed, connected and unit-free then $\operatorname{diam}C<1$.

(c) The bound in (b) is optimal: for every $\varepsilon>0$ the closed disc $\overline B(0,\tfrac{1-\varepsilon}2)$
is closed, connected, unit-free, and has diameter $1-\varepsilon$.

*Proof.* (a) For $x,y\in B(0,\tfrac12)$, $|x-y|\le|x|+|y|<1$; and $|te-(-te)|=2t\to1$ as $t\uparrow\tfrac12$
for any unit $e$.

(b) By Lemma 1, $\operatorname{diam}C\le1$, so $C$ is bounded and (being closed) compact; the
continuous function $(x,y)\mapsto|x-y|$ on the compact set $C\times C$ attains its maximum, so if
$\operatorname{diam}C=1$ there are $x,y\in C$ with $|x-y|=1$, $x\neq y$, contradicting unit-freeness.

(c) Clear: $\operatorname{diam}\overline B(0,r)=2r<1$ for $r<\tfrac12$. $\square$

---

## 3. No-go 1: finitely many components per class

**Theorem 5.** Let $k<\infty$. Then $\mathbb R^2$ cannot be written as a union of $k$ unit-free sets
$A_1,\dots,A_k$ each of which has only finitely many connected components. Equivalently: no proper
$k$-colouring of the plane, $k<\infty$, has all its colour classes of finitely many components.

*Proof.* By Corollary 2 each component of $A_i$ has diameter $\le1$, so $A_i$ is a finite union of
sets of finite diameter, hence $\operatorname{diam}A_i<\infty$. A finite union of bounded sets is
bounded, so $\mathbb R^2$ would be bounded — contradiction. $\square$

**Corollary 6.** There is no proper colouring $c:\mathbb R^2\to\{1,\dots,k\}$, $k<\infty$, all of whose
colour classes are of one of the following kinds:

(i) semialgebraic subsets of $\mathbb R^2$;
(ii) subsets definable in an o-minimal expansion of $(\mathbb R,+,\cdot)$ — e.g. subanalytic sets;
(iii) finite unions of convex sets;
(iv) finite unions of connected (equivalently, of path-connected) sets;
(v) finite unions of compact sets.

*Proof.* A semialgebraic set, and more generally an o-minimal definable set, has finitely many
connected components (finite cell decomposition; cells are connected). A convex set is connected;
a finite union of compact sets is bounded, so (v) is even more immediate. Now apply Theorem 5. $\square$

**Remark 7 (Theorem 5 is sharp, and its finiteness hypothesis cannot be relaxed).**
- *Sharp in the number of classes.* The map
  $$c(x_1,x_2)=\big(\lfloor 2x_1\rfloor,\ \lfloor 2x_2\rfloor\big)$$
  is a proper colouring of $\mathbb R^2$ with countably many classes; each class is a half-open
  square of side $\tfrac12$ and hence has diameter $\tfrac{\sqrt2}2<1$. Its classes are connected
  (indeed convex) and Borel. So with *countably* many classes, connected unit-free classes do
  cover the plane; only finite $k$ is excluded by Theorem 5.
- *Sharp in the number of components.* With $k=7$ classes and infinitely many bounded components
  per class there is a proper colouring: the hexagonal colouring of the paper's §1 with hexagon
  circumradius $r=\tfrac25$ (Lemma 8 below). So "finitely many components" cannot be weakened to
  "countably many components".

**Lemma 8 (the paper's §1 hexagonal colouring, verified).** There is a proper colouring
$c:\mathbb R^2\to\{1,\dots,7\}$ whose classes are unions of closed regular hexagons of circumradius
$r=\tfrac25$ from a locally finite tiling; in particular every class is closed (hence Borel, hence has
the Baire property), and has infinitely many bounded components.

*Proof (all constants exact; checked in `verify_rigidity.py`, items D1–D5).* Identify
$\mathbb R^2\cong\mathbb C$. Let $\omega=e^{2\pi i/3}$, $d=\sqrt3\,r$, $\Lambda=d(\mathbb Z+\omega\mathbb Z)$
(triangular lattice of nearest-neighbour distance $d$), and let $K$ be the closed Voronoi hexagon
of $0$, a regular hexagon of circumradius $r$; the translates $K+\lambda$, $\lambda\in\Lambda$, tile
the plane. Put $\Lambda'=(2-\omega)\Lambda$; since $|2-\omega|^2=7$, $\Lambda'$ has index $7$ in
$\Lambda$, and its shortest nonzero vector has length $\sqrt7\,d=\sqrt{21}\,r$ (an element of
$(2-\omega)\mathbb Z[\omega]$ is $(2-\omega)z$ with $|z|\ge1$). Colour the hexagon $K+\lambda$ by the
coset $\lambda+\Lambda'\in\Lambda/\Lambda'$ (seven cosets); a point lying on an edge or vertex of the
tiling belongs to several hexagons and may be given the colour of any one of them.
Let $p,q$ be at distance $1$, lying in hexagons of the same colour; say $p\in K+\lambda_1$,
$q\in K+\lambda_2$ with $\lambda_1+\Lambda'=\lambda_2+\Lambda'$. If $\lambda_1=\lambda_2$ then
$|p-q|\le\operatorname{diam}K=2r=\tfrac45<1$, contradiction. Otherwise
$t:=\lambda_1-\lambda_2$ satisfies $t\in\Lambda'\setminus\{0\}$, so $|t|\ge\sqrt{21}\,r$; and
$$|p-q|\ \ge\ \operatorname{dist}(K,K+t)\ =\ \operatorname{dist}\big(t,\,K-K\big)\ \ge\ |t|-2r\ \ge\ (\sqrt{21}-2)\,r\ >\ 1,$$
using $K-K=2K$ (a regular hexagon is centrally symmetric) and $\operatorname{dist}(t,2K)\ge|t|-2r$.
Since $(\sqrt{21}-2)\cdot\tfrac25>1\iff2\sqrt{21}>9\iff84>81$, this contradicts $|p-q|=1$. $\square$

---

## 4. No-go 2: colourings that factor through connected unbounded fibres

**Theorem 9.** Let $X$ be a set and $g:\mathbb R^2\to X$ a map all of whose fibres $g^{-1}(t)$
($t\in X$) are connected and unbounded. Then for no finite $k$ does there exist
$f:X\to\{1,\dots,k\}$ such that $f\circ g$ is proper.

*Proof.* If $f\circ g$ is proper, the class $\{x: f(g(x))=i\}=g^{-1}\big(f^{-1}(i)\big)$ is a union of
fibres, hence if nonempty contains a connected unbounded set, contradicting Lemma 1; so all
classes are empty, which is impossible. $\square$

**Corollary 10 (line-periodic colourings).** Let $v\neq0$ and let $c:\mathbb R^2\to\{1,\dots,k\}$,
$k<\infty$, satisfy $c(x+tv)=c(x)$ for all $x\in\mathbb R^2$, $t\in\mathbb R$ (i.e. $c$ is invariant
under the full one-parameter group $\mathbb R v$, not merely under a discrete subgroup). Then $c$
is not proper.

*Proof.* Take $X=\mathbb R^2/\mathbb R v\cong\mathbb R$ and $g$ the quotient map; the fibres are the
lines $x+\mathbb R v$, connected and unbounded. Apply Theorem 9. (Directly: a class containing a
point contains a whole line, which is connected and unbounded, contradicting Lemma 1.) $\square$

**Corollary 11.** Let $k<\infty$. Then no proper colouring is of either form
(a) $c(x)=f(\langle x,w\rangle)$ with $w\neq0$ ("stripe colouring"), or
(b) $c(x)=f(\operatorname{dist}(x,L))$ for a line $L$ ("bilateral stripe colouring").
In both cases every colour class is a union of full lines, and a full line is connected and
unbounded, so Lemma 1 forbids a nonempty class.
(For (a) this is also the special case of Theorem 9 with $g(x)=\langle x,w\rangle$; for (b) Theorem 9
does not apply as stated, since a level set $\{\operatorname{dist}(\cdot,L)=t\}$, $t>0$, is a union of
*two* lines and is not connected — the class-level argument is what is needed.)

**Remark 12.** The discreteness in Corollary 10 is essential: invariance under a *discrete*
subgroup $\mathbb Z v$ is a much weaker condition, and the analogue of Theorem 9 fails there.
Concretely, an invariant-under-$\mathbb Z v$ colouring is a colouring of the flat cylinder
$\mathbb R^2/\mathbb Z v$, and if $|v|=1/n$ for some $n\ge1$ **no** proper colouring at all exists with
any number of colours, since then $|nv|=1$ and $x$, $x+nv$ have equal colour at distance $1$; whereas
for other $|v|$ the question reduces to a unit-distance problem on the cylinder and is not
settled by the mechanism above. (Note $|v|=1/n$ with $n\ge1$ includes $|v|=1$.)

---

## 5. No-go 3: radial colourings

**Theorem 13.** Let $k<\infty$ and $c(x)=f(|x|)$ for some $f:[0,\infty)\to\{1,\dots,k\}$. Then $c$ is not
proper.

*Proof.* Let $A_i$ be a colour class, $A_i=\bigcup_{\rho\in f^{-1}(i)}C_\rho$ with
$C_\rho=\{x:|x|=\rho\}$. If $\rho\ge\tfrac12$ then $C_\rho$ contains two points at distance exactly
$1$: for the central angle $\theta$ with $2\rho\sin(\theta/2)=1$ (solvable because
$\sin(\theta/2)$ runs over $[0,1]$ and $1/(2\rho)\le1$) the corresponding chord has length $1$. So
$C_\rho\not\subseteq A_i$; hence $f^{-1}(i)\subseteq[0,\tfrac12)$ and $A_i\subseteq\overline B(0,\tfrac12)$.
Finitely many bounded classes cannot cover $\mathbb R^2$. $\square$

---

## 6. No-go 4: colour classes with finitely many convex pieces, via Lemma 3

Theorem 5 already covers Corollary 6(iii). The following is the form in which the *paper's*
mechanism (Lemma 3) gives it, and it is the reason no such colouring can exist:

**Proposition 14.** Let $A$ be unit-free and let $K_1,\dots,K_m$ be connected subsets of $A$ with
$A=\bigcup_jK_j$. Let $z\in A$. Then for each $j$ either $|z-q|\ge1$ for all $q\in K_j$, or
$|z-q|\le1$ for all $q\in K_j$.

*Proof.* Immediate from Lemma 3 applied to $U=A$. $\square$

---

## 7. What the structure theory cannot do

The following example is the reason none of §1–§6 yields a lower bound for $\chi(\mathbb R^2)$ and,
in particular, no improvement of the paper's Theorem 1.1 in this direction.

**Proposition 15.** There is a proper colouring of $\mathbb R^2$ with countably many classes such that
every class is convex (hence connected), Borel, bounded, and of diameter $<\tfrac34$. Consequently
any argument of the form "a colour class is a connected set, and connected unit-free sets are
small, so finitely many classes cannot cover the plane" *must* use finiteness of $k$, and cannot
be upgraded to a statement about $6$ or $7$ colours.

*Proof.* Take $c(x_1,x_2)=(\lfloor2x_1\rfloor,\lfloor2x_2\rfloor)$; each class is a half-open square of
side $\tfrac12$, convex, Borel, of diameter $\tfrac{\sqrt2}2<0.75$. Two points at distance $1$ lie in
different classes because classes have diameter $<1$. $\square$

---

## 8. A correct counterexample to a tempting category strengthening

A natural attempt to force a *finite* bound is a Baire-category argument of the following shape:

> **(False sublemma S).** If $A\subseteq\mathbb R^2$ has the Baire property and is unit-free, then $A$ is
> meager.

**(S) is false.** The open disc $B(0,\tfrac12)$ is unit-free (Proposition 4(a)), nonempty and open,
hence non-meager. More generally, by Corollary 2 a unit-free set whose component meets an open set
$U$ must have $\operatorname{diam}$ of that component $\le1$; so a unit-free set may perfectly well be
comeager in any open set of diameter $\le1$ (e.g. in $B(0,\tfrac12)$ itself). The naive proof of (S)
takes a class $A$ comeager in an open $U$ and a unit vector $u$, then claims that
$\{x\in U:x\in A\}$ and $\{x\in U:x+u\in A\}$ are both comeager in $U$; this is wrong unless
$U\cap(U-u)\neq\varnothing$, i.e. unless $U$ contains a *unit chord*.
The correct statement is therefore the following, and it is not enough for a lower bound.

**Proposition 16 (category obstruction, correct form).** Let $k<\infty$ and let $c:\mathbb R^2\to\{1,\dots,k\}$
have colour classes with the Baire property. Suppose some class $A$ is comeager in an open set $U$
for which there exist $x\in U$ and a unit vector $u$ with $x+u\in U$ (i.e. $U\cap(U-u)\neq\varnothing$).
Then $c$ has a monochromatic unit pair.

*Proof.* $W:=U\cap(U-u)$ is a nonempty open set. For $y\in W$: $y\in U$, and $y+u\in U$. Since $A$ is
comeager in $U$, both $\{y\in W:y\in A\}$ and $\{y\in W:y+u\in A\}$ are comeager in $W$. Their
intersection is comeager in $W$, hence nonempty; so $y,y+u\in A$ with $|u|=1$. $\square$

**Consequence.** Any category-based exclusion of finite colourings only rules out colourings in
which a class is comeager in an open set containing a unit chord; and by Corollary 2 such a
compact "comeagerness region" is compatible with unit-freeness as soon as it has diameter $\le1$.
So category gives no finite lower bound for $\chi(\mathbb R^2)$, and in particular cannot be used to
attack the $6$ versus $7$ question.

**Remark 17.** For completeness: (S) would be a strong statement, and it is also incompatible with
$\chi(\mathbb R^2)\le7$: by Lemma 8 the plane has a proper $7$-colouring all of whose classes are
closed, hence have the Baire property. So the failure of (S) is not an artefact of the example
chosen; no correct version of it can exclude finite Baire colourings.

---

## 9. The resulting constraint on any hypothetical $6$- or $7$-colouring

Combining Theorem 5 with the trivialities of the definition gives the following structural
description. It is the positive content of this note: it constrains the search space for a
$6$-colouring (the only open upper-bound question, given the paper's Theorem 1.1).

**Proposition 18.** Let $k<\infty$ and let $c:\mathbb R^2\to\{1,\dots,k\}$ be proper. Then:

(a) every colour class is unit-free, and each of its connected components has diameter $\le1$
(Corollary 2);
(b) distinct components of the same class never contain points at distance exactly $1$;
(c) no class contains a connected unbounded set: in particular no class contains a line, a ray, an
unbounded curve, a half-plane, a full circle of radius $\ge\tfrac12$, or any set of diameter $>1$ that
is connected;
(d) at least one class is unbounded, hence has infinitely many connected components; and no
class has only finitely many components unless it is bounded (Theorem 5);
(e) for every line $L$, every connected component of $A_i\cap L$ is an interval of length $\le1$;
(f) for every class $A_i$ and every open ball $B\subseteq A_i$ one has $\operatorname{diam}B\le1$, i.e.
no class of a proper colouring contains an open ball of radius $>\tfrac12$;
(g) consequently, a $6$-colouring of $\mathbb R^2$ (if one exists) must shatter the plane into
$6$ unit-free families of components of diameter $\le1$ with pairwise distances $\neq1$, each family
having infinitely many components: no colouring by finitely many semialgebraic, definable,
convex-piecewise or comparable cells can be the sought one.

*Proof.* (a),(b) are the definition plus Corollary 2. (c) is Lemma 1. (d) If all classes were
bounded they could not cover $\mathbb R^2$; and an unbounded set that is a finite union of sets of
diameter $\le1$ would be bounded, so an unbounded class has infinitely many components. (e) $A_i\cap L$
is a unit-free subset of the line $L$, so each of its components (intervals) has length $\le1$.
(f) $B$ lies in a single component of $A_i$. (g) is Corollary 6. $\square$

---

## 10. Reproduction

```
cd .ultramath/smwfcr56i/m10
python3 verify_rigidity.py      # 17/17 PASS, see verify_rigidity.log
```
The script checks, in exact arithmetic (`sympy`): A1–A4 (Proposition 4, including that no closed
connected unit-free set has diameter $1$), B (unit chords on circles: exists iff $2\rho\ge1$, used in
Theorem 13), C/Proposition 15 (half-open squares of side $\tfrac12$ have diameter $\sqrt2/2<1$),
D1–D5 (Lemma 8: $2r=\tfrac45<1$, $(\sqrt{21}-2)r>1\iff84>81$, $|2-\omega|^2=7$,
$\sqrt7\sqrt3\,r=\sqrt{21}\,r$), E1–E3 (Theorem 19: the three half-open arcs are unit-independent
and have total angular measure $\pi$).

## 11. Honest scope

Proved here: Lemma 1, Corollary 2, Lemma 3, Propositions 4, 14, 15, 16, 18, Theorems 5, 9, 13, 19,
Corollaries 6, 10, 11, 20, Lemma 8, Remarks 7, 12, 17 — with the exception of the standard fact used
in Corollary 6(ii) (o-minimal cell decomposition, whose cells are connected). Nothing here
improves $\chi(\mathbb R^2)\ge6$ or $\chi(\mathbb R^2)\le7$; what it does is close off the four structured
families listed in the direction statement with no finite $k$ at all, pin down exactly where
category/connectedness mechanisms stop, and give the sharp angular constant $\pi$ for the quantity
that the paper's footnote 1 discusses (where the paper's own example attains only $\pi/3$).

---

## 12. Appendix: the sharp angular constant for unit-independent subsets of the unit circle

The paper's footnote 1 discusses "the angular measure of a unit-independent subset of the unit
circle" and refutes a proposed strict bound $\pi/3$ by the half-open arc $\{e^{it}:0\le t<\pi/3\}$,
which has angular measure exactly $\pi/3$ and no unit pair. That refutation is correct, but the
example is far from extremal, and the sharp value of the quantity is worth recording (any argument
in §5–§8 that silently uses an angular bound below the sharp one would be wrong).

Throughout, identify $S^1=\{e^{it}\}\subseteq\mathbb C\cong\mathbb R^2$ with $\mathbb R/2\pi\mathbb Z$;
$\sigma$ is normalized angular measure, and $A\subseteq S^1$ is *unit-independent* if
$|u-v|\neq1$ for distinct $u,v\in A$. Note
$$|e^{it}-e^{is}|=2\big|\sin\tfrac{t-s}{2}\big|,$$
so $|e^{it}-e^{is}|=1\iff t-s\equiv\pm\tfrac{\pi}{3}\pmod{2\pi}$.

**Theorem 19.** Let $A\subseteq S^1$ be Lebesgue measurable and unit-independent. Then
$\sigma(A)\le\tfrac12$, i.e. the angular measure of $A$ is at most $\pi$. The constant is attained.

*Proof.* Let $R$ be the rotation $t\mapsto t+\pi/3$. If $u\in A\cap R(A)$ then $u=R(v)$ for some
$v\in A$, and $|u-v|=|e^{i\pi/3}v-v|=2\sin(\pi/6)=1$, contradicting unit-independence. So
$A\cap R(A)=\varnothing$; both sets are measurable of equal measure, whence
$2\sigma(A)\le\sigma(S^1)=1$.

For attainment take, in angular coordinates,
$$A=[0,\tfrac\pi3)\cup[\tfrac{2\pi}3,\pi)\cup[\tfrac{4\pi}3,\tfrac{5\pi}3),$$
three half-open arcs of total length $\pi$. For two points of the same arc the angular difference has
modulus $<\pi/3$; and for points in two different arcs the open interval of possible differences
contains neither $\pi/3$ nor $-\pi/3$ modulo $2\pi$ (checked exactly, arc pair by arc pair, in
`verify_rigidity.py`, items E1–E3). So $A$ is unit-independent and $\sigma(A)=\tfrac12$. $\square$

**Corollary 20.** If $A\subseteq S^1$ is closed and unit-independent then its angular measure is
strictly less than $\pi$; the bound $\pi$ is optimal for measurable (or $F_\sigma$, or half-open)
sets. In particular the sharp strict statement is $\sigma(A)<\tfrac12$ for closed $A$, and no
statement sharper than $\sigma(A)\le\tfrac12$ can hold for measurable $A$.

*Proof.* If $A$ is closed and $\sigma(A)=\tfrac12$ then $A$ and $R(A)$ are disjoint closed sets of
measure $\tfrac12$ each, so $\sigma(S^1\setminus(A\cup R(A)))=0$; but $S^1\setminus(A\cup R(A))$ is open, so it
would be empty, forcing $A\cup R(A)=S^1$ to be disconnected as a union of two disjoint nonempty closed
sets — contradicting connectedness of $S^1$. Hence $\sigma(A)<\tfrac12$. $\square$

This is the exact analogue, one dimension down, of Proposition 4: the extremal object must be
half-open, never closed. The paper's footnote-1 example has measure $\pi/3$, one third of the true
maximum $\pi$; the three-arc set above is extremal.
