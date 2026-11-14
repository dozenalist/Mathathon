# The circle cap and the ball threshold

### Exact window chromatic numbers, a certified no-go for single-centre circle arguments at $k=6$, and the specification they generate

*Direction d7 of swarm smwfhd5sl (route C, "k-sensitive invariants"). All statements below are
either proved or verified in exact arithmetic by the scripts named at the end; nothing is
numerical evidence presented as a theorem.*

---

## 0. Results

Let $\Delta_W$ be the graph on a set $W\subseteq\mathbb R^2$ with an edge for every pair at
Euclidean distance exactly $1$, and write $\chi(W):=\chi(\Delta_W)$.

**Theorem A (circle chord graphs).** For $x\in\mathbb R^2$, $r>0$ let
$\theta(r)=2\arcsin\frac1{2r}$.
* $r<\tfrac12$: $\Delta_{S_r(x)}$ has no edge, $\chi=1$.
* $r\ge\tfrac12$: every connected component of $\Delta_{S_r(x)}$ is an orbit of the rotation by
  $\theta(r)$ about $x$. If $\theta(r)/2\pi=p/q$ in lowest terms the component is a $q$-cycle;
  otherwise it is a bi-infinite path. Hence
  $$\chi(S_r(x))=\begin{cases}3,& q \text{ odd},\ q\ge 3,\\ 2,&\text{otherwise.}\end{cases}$$
  Equivalently $\chi(S_r(x))=3$ iff $r=\bigl(2\sin\frac{\pi p}{q}\bigr)^{-1}$ with $q$ odd,
  $1\le p\le q/2$, $\gcd(p,q)=1$.
* Consequently $\chi(S_r(x))\le 3$ **for every $x$ and every $r$**, and $3$ is attained. The set
  of $3$-chromatic radii is dense in $[\tfrac12,\infty)$ with infimum $\tfrac12$ not attained;
  its complement in $[\tfrac12,\infty)$ (the $2$-chromatic radii) is also dense and has full
  measure. At the palette radius $r=1$: $\theta=\pi/3$, $q=6$, so $\chi(S_1(x))=2$, the components
  being six-cycles (this reproduces the observation in `results/K6-BARRIER.md` §1).

**Lemma B (germ freedom).** Let $x$, $r$, a direction $e$ and $\delta<\theta(r)/2$ be given. The
arc $A=\{x+re^{it}: |t-t_e|<\delta\}$ contains no unit pair. Hence every labelling of $A$ by
arbitrary labels is proper for $\Delta_{S_r(x)}$.

**Theorem B (no-go for single-centre circle arguments).** Delimit the class $\mathcal C$ of
*single-centre circle arguments*: those that bound $P_x(e)$ at one centre $x$ using only (i) the
unit-distance constraints inside spheres $S_r(x)$ about that centre, at finitely many radii, and
(ii) label-set combinatorics. Then no argument in $\mathcal C$ proves $|P_x(e)|\le 2$ for a
proper $6$-colouring, for any radius, any constant and any combination of radii. Three reasons,
in increasing strength: (a) by Lemma B the local (germ) constraint is empty, so no label set is
excluded from a palette by circle geometry; (b) globally, by Theorem A the strongest statement
available is $\chi(S_r(x))\le 3$; (c) $3$ is attained, so even the global cap cannot be sharpened,
and $3=k-3$ is exactly the bound Proposition 5.6 gives at $k=6$. The class is not a strawman:
it contains the natural repair attempt — "a ternary palette forces three colours onto the circle,
which no circle admits" — which is false at every radius, and it is exactly the *local* half of
the paper's own Proposition 5.6. What the paper actually uses and what lies outside $\mathcal C$
is the cross-centre machinery: palette transport (5.2) via Fubini, and Lemma 5.5.

**Theorem C (the window ladder at radius one).** Exactly:
$$\chi(S_1(x))=2,\qquad \chi(S_1(x)\cup\{x\})=3,\qquad \chi(B(x,1))\ge 4 .$$
The middle value is exact and attained: the centre is at distance $1$ from every circle point, and
the circle is a disjoint union of six-cycles, so the cone over those cycles has chromatic number
exactly $3=6-3$. The right-hand inequality is witnessed by an explicit seven-point configuration
with exact coordinates in $\mathbb Q(\sqrt3,\sqrt{11})$ — the Moser spindle already formalised in
`lean/OAI/Geometry/PlaneColoring/Moser.lean` — whose minimal enclosing circle has centre
$(\frac{\sqrt3}{2},\frac{\sqrt{33}}{22})$ and radius $\frac{3}{\sqrt{11}}<1$. Moreover two
*circles* suffice: the four points $p_1,p_3,p_5,p_6$ are concyclic (exact $4\times4$ determinant
vanishing) with centre $\bigl(\frac{\sqrt{11}+11\sqrt3}{16},\frac{1+\sqrt{33}}{16}\bigr)$ and
$r^2=\frac{15-\sqrt{33}}{32}$, and $p_0,p_2,p_4$ lie on the circle with centre
$\bigl(\frac{\sqrt{11}+11\sqrt3}{32},\frac{1+\sqrt{33}}{32}\bigr)$, $r^2=\frac{51+3\sqrt{33}}{128}$;
both radii are $<3/4$.

**Theorem D (k-sensitivity of window colour counts).** For finite $S\subseteq\mathbb R^2$,
$W\subseteq\mathbb R^2$, $k\ge1$ put
$$I_k(S,W)=\min\bigl\{|c(S\cap W)|:\ c:S\to\{1,\dots,k\}\ \text{proper}\bigr\}\in\mathbb N\cup\{\infty\}.$$
Then $I_k(S,W)=\infty$ iff $k<\chi(S)$; $I_k\ge\chi(S\cap W)$; $I_k$ is non-increasing in $k$.
For the seven-vertex spindle $S$ and all $128$ windows $W\subseteq S$, exact enumeration gives
$I_4\ne I_5$ for $51$ windows — for example $W=S\setminus\{p_5\}$ has
$(I_4,I_5,I_6)=(4,3,3)$ and $W=\{p_0,p_6\}$ has $(2,1,1)$ — while $I_5=I_6$ for **all** $128$
windows. So a window colour count is a genuine k-sensitive invariant, it does change when $k$
changes by one, and on this configuration it does not change between $5$ and $6$.

---

## 1. Windows

The palette $P_x(e)$ of Definition 5.1 of the paper is built from circle samples of radius
tending to $1$ about $x$. Every bound on $|P_x(e)|$ is therefore a bound obtained, at the level of
geometry, from a *window*: the data of $\Delta_W$ for some $W$ built from $x$ and circles about
$x$. This note computes exactly which bounds each window can give, which is the only way to say
what "the cover-and-palette method cannot decide $k=6$" means for the palette step (R5).

A window is a subset $W\subseteq\mathbb R^2$; its chromatic number $\chi(W)$ is that of
$\Delta_W$; a window is *single-centre* if $W\subseteq S_r(x)$ or $W=S_r(x)\cup\{x\}$ for one
centre $x$.

## 2. Theorem A: the exact chromatic number of a circle

**Proof.** Fix $x=0$, $r>0$. Two points $re^{is}$, $re^{it}$ are at distance $1$ iff
$2r|\sin\frac{s-t}{2}|=1$. Since $\arcsin\frac1{2r}$ is defined iff $r\ge\frac12$, there is no
edge when $r<\frac12$. For $r\ge\frac12$ put $\theta=2\arcsin\frac1{2r}\in(0,\pi]$; then the
condition reads $|s-t|\equiv\theta \pmod{2\pi}$, i.e. $t\in\{s+\theta,s-\theta\}$. So
$\Delta_{S_r(x)}$ is the Cayley graph of the circle group $\mathbb R/2\pi\mathbb Z$ with
connection $\{\pm\theta\}$; its connected components are the cosets of the subgroup
$\langle\theta\rangle$ generated by $\theta$.

If $\theta/2\pi$ is irrational, $\langle\theta\rangle\cong\mathbb Z$ and the component of $0$ is
the bi-infinite path $\{k\theta\}_{k\in\mathbb Z}$, so $\chi=2$. If $\theta/2\pi=p/q$ in lowest
terms, $\langle\theta\rangle$ is cyclic of order $q$ (order $2$ when $q=2$ and $\theta=\pi$), and
the component is $\mathrm{Cay}(\mathbb Z_q,\{\pm p\})$, which is the cycle $C_q$ because
$\gcd(p,q)=1$. Hence $\chi=3$ iff $q$ is odd and $q\ge3$, and $\chi=2$ otherwise. $\square$

**Corollary A1.** $\chi(S_r(x))\le3$ for all $x,r$: no circle ever needs four colours. (The
clique bound already gives $\omega\le3$; the corollary is about $\chi$.)

**Corollary A2.** $3$ is attained: $r=1/\sqrt3$ gives $\theta=2\pi/3$, $q=3$, and the component is
an equilateral triangle inscribed in the circle, side $1$ — three points mutually at distance
exactly one. More generally every odd $q$ gives one.

**Corollary A3 (density).** $\{1/(2\sin(\pi p/q)):\ q\ \text{odd}\}$ is dense in $[\frac12,\infty)$
because the fractions with odd denominator are dense; its infimum $\frac12$ is not attained
($q=2$ is even and gives $\chi=2$). The $2$-chromatic radii (irrational $\theta/2\pi$, plus even
$q$) are dense as well and have full measure. So "$3$ colours on a circle" is exceptional but
unavoidable, and every radius can be perturbed to a $2$-chromatic one.

**Corollary A4 (the palette radius).** At $r=1$, $\theta=\pi/3$ and the components are six-cycles,
$\chi=2$. Also $\chi(S_{1/2}(x))=2$ (antipodal pairs, $q=2$) and
$\chi(S_{1/\sqrt2}(x))=2$ (squares, $q=4$).

*Verified exactly by `verify_sphere.py`: the criterion for $r\in\{\frac12,\frac1{\sqrt3},
\frac1{\sqrt2},1,\frac1{2\sin(\pi/5)},\frac1{2\sin(2\pi/5)},\frac1{2\sin(\pi/7)},
\frac1{2\sin(2\pi/9)}\}$, the exact squared distances $=1$ of the three triangle vertices and of
six consecutive orbit points at $r=1$, the "next-nearest distance squared $=3$" (so the degree is
exactly two), all $158$ odd-denominator instances with $q\le39$, and the orbit-length computation
$2,3,4,6,5,5,7,9$ for the radii $\tfrac12,\tfrac1{\sqrt3},\tfrac1{\sqrt2},1$ and the five odd-$q$
instances, matching the predicted $q$ in each case.*

## 3. Lemma B and Theorem B: what a circle cannot do

**Lemma B (germ freedom).** The chord subtending the angle $\theta(r)$ has length $1$, and
$2r\sin(|s-t|/2)$ is strictly increasing in $|s-t|\in[0,\pi]$; so an arc of angular width
$< \theta(r)$ contains no unit pair. Assigning arbitrary labels to its points is therefore a
proper colouring of the induced subgraph, whatever the labels are. $\square$

**Corollary B1 (no label is excluded locally).** Let $k\ge1$, a centre $x$, a radius $r$, a
direction $e$ and $\delta<\theta(r)/2$ be given, and let $A\subseteq\{1,\dots,k\}$ be any label
set. Some proper colouring of $\Delta_{S_r(x)}$ assigns exactly the labels $A$ to the arc
$\{x+re^{it}:|t-t_e|<\delta\}$, and arbitrary labels elsewhere: take the labelling constant on
each orbit of the rotation by $\theta(r)$ intersected with the arc, and extend it to the orbit so
that no orbit receives more than $\max(\chi(S_r(x)),|A|)\le\max(3,|A|)$ labels (for $k<3$ and
$\chi(S_r(x))=3$ no proper colouring exists at all). Hence no argument whose only geometric
input is $\Delta_{S_r(x)}$ can exclude any label, or any set of labels, from the palette at a
direction.

**Theorem B (restated precisely).** *Class $\mathcal C$*: an argument that concludes a bound
$|P_x(e)|\le m$ from (i) the unit-distance constraints satisfied inside **one** sphere $S_r(x)$
about a single centre $x$ — the geometry of Definition 5.1, where $r$ tends to $1$ — and
(ii) label combinatorics. Then no argument in $\mathcal C$ yields $m\le2$ for $k=6$, for any
radius, arc width or constant:
1. *The germ carries no constraint.* By Corollary B1 every label set $A$ can be realised on any
   arc shorter than $\theta(r)$. So circle geometry excludes no label set from a palette.
2. *The only circle bound available is a lower bound on needed colours, and it is capped at $3$.*
   A $\mathcal C$-argument could only contradict a palette by deriving "a circle must receive at
   least $4$ labels" (or "at least $m+1$"). But every constraint system of the form "two points of
   $S_r(x)$ at distance $1$ carry different labels" is satisfied by a $3$-colouring of
   $\Delta_{S_r(x)}$ (Theorem A), and $3$ is attained (A2). So no such derivation exists, at any
   radius. At $k=6$ in particular a ternary palette is realisable on the sphere itself: at
   $r=1/\sqrt3$ put labels $1,2,3$ on any short arc and extend.
3. Hence $\mathcal C$ cannot beat $3=k-3$ at $k=6$, and in particular cannot prove $|P_x(e)|\le2$.

**Non-vacuity.** (1) The natural attempt that $\mathcal C$ refutes is a real one: at $k=6$ the
complement of a palette triple is a triple, and the tempting move is to say that a circle cannot
carry three labels. Corollary A2 exhibits a circle that carries exactly three, at
$r=1/\sqrt3$, and Theorem A shows that no radius does better than three. (2) $\mathcal C$ is
exactly the local half of Proposition 5.6: the paper's proof of $|P|\le k-3$ proceeds by showing
that if a $(k-2)$-set sits in a palette then a *complementary pair* colour the circle and the
centres become binary, and then invokes cross-centre separation. The part that is inside
$\mathcal C$ cannot be sharpened; the part that is outside $\mathcal C$ — Fubini transport (5.2)
and binary-centre separation (Lemma 5.5) — is where all the $k$-dependence lives. So Theorem B
neither re-derives R5 nor contradicts it: it identifies, geometrically and exactly, which
ingredient $\mathcal C$ is missing. (3) $\mathcal C$ is deliberately single-radius, because that
is the palette geometry ($r\to1$); with **two** radii at one centre the analogous cap is not
proved here — two circles do carry a $4$-chromatic configuration (Proposition C3) — although for
the obvious candidate it fails: an exact search over all candidate centres
(`verify_concentric.py`) shows the spindle is **not** realisable on two *concentric* circles, so
no counterexample to a concentric two-radius version comes from it.

**Remark (why the failure is at $k=6$ and not at $k=5$).** At $k=5$ the object whose absence is
contradictory is a *pair*; the palette argument then needs an alternating selection
$s_x(t+\kappa)=-s_x(t)$ (paper (5.8)), i.e. a two-element state, and separation of binary
centres. At $k=6$ the analogous object is a triple, for which (5.7) forces nothing: two disjoint
non-empty subsets of a three-element set need not be complementary, so there is no unique
selection and no (5.8). This is the same loss as in W6 (`results/continuation/W1-W4-W7.md`). What
this note adds is that no amount of circle geometry can undo it, with exact numbers: $3$ is the
maximum number of colours a circle can carry, and it is attained.

## 4. Theorem C: the window ladder, and the exact threshold

**Proposition C1.** $\chi(S_1(x)\cup\{x\})=3$.

*Proof.* The centre $x$ is at distance $1$ from every point of $S_1(x)$, so $x$ is adjacent to all
of them and no circle point can share the centre's colour. By Theorem A the circle is a disjoint
union of six-cycles (A4), which are bipartite; two colours therefore colour the circle, and three
colours are necessary (a circle point and its two neighbours need two colours, neither of which
may be the centre's). Hence $\chi=3$. $\square$

*Verified exhaustively in `verify_ball.py` on the finite sub-configuration of one six-cycle plus
the centre (the cone over $C_6$): not $2$-colourable, and
$\{x\mapsto0,\ p_k\mapsto1+(k\bmod 2)\}$ is a proper $3$-colouring.*

**Proposition C2.** $\chi(B(x,\tfrac{3}{\sqrt{11}}))\ge4$ for every $x$.

*Proof.* The seven points
$$p_0=0,\quad p_1=\tfrac{\sqrt3+i}{2},\quad p_2=\tfrac{\sqrt3-i}{2},\quad p_3=\sqrt3,\quad
p_4=Up_1,\quad p_5=Up_2,\quad p_6=Up_3,\qquad U=\tfrac{5+i\sqrt{11}}{6}$$
with the eleven unit distances of `Moser.lean` form a $4$-chromatic unit-distance graph (that file
proves non-$3$-colourability; `verify_ball.py` re-derives it exhaustively and confirms that the
coordinate unit pairs are exactly the eleven listed edges). All seven points are at distance at
most $3/\sqrt{11}$ from $c=(\frac{\sqrt3}{2},\frac{\sqrt{33}}{22})$: for $p_0,p_3$ the squared
distance is $\frac34+\frac{33}{484}=\frac9{11}$, for $p_6$ it is
$\frac13+\frac{16\cdot33}{33^2}=\frac9{11}$, and the remaining four are strictly closer (checked
exactly). Since $\frac{3}{\sqrt{11}}=0.9045\ldots<1$, the ball $B(x,1)$ contains a congruent copy
for every $x$. $\square$

**Proposition C3 (two circles suffice).** The four points $p_1,p_3,p_5,p_6$ are concyclic: the
$4\times4$ determinant with rows $(x,y,x^2+y^2,1)$ vanishes identically in
$\mathbb Q(\sqrt3,\sqrt{11})$. The circle is
$$\Bigl(\tfrac{\sqrt{11}+11\sqrt3}{16},\ \tfrac{1+\sqrt{33}}{16}\Bigr),\quad
r^2=\tfrac{15-\sqrt{33}}{32}\approx0.2892,$$
and the three remaining points $p_0,p_2,p_4$ lie on
$$\Bigl(\tfrac{\sqrt{11}+11\sqrt3}{32},\ \tfrac{1+\sqrt{33}}{32}\Bigr),\quad
r^2=\tfrac{51+3\sqrt{33}}{128}\approx0.5331.$$
So the seven vertices of a $4$-chromatic unit-distance configuration lie on **two** circles, of
radii $0.5378\ldots$ and $0.7301\ldots$, both $<3/4$; by Theorem A one circle could never carry
four colours, so two is the exact minimum. Consequently the bound of $\mathcal C$ is broken by
coupling two centres, at small radii.

**The ladder at radius one:**

| window | colours forced | exact value | source |
|---|---|---|---|
| $S_1(x)$ | 2 | $\chi=2$ (six-cycles) | Theorem A |
| $S_1(x)\cup\{x\}$ | 3 | $\chi=3$ | Proposition C1 |
| two circles ($r<3/4$) | 4 | explicit, concyclic quadruple | Proposition C3 |
| $B(x,3/\sqrt{11})$ | $\ge4$ | explicit seven-point configuration | Proposition C2 |
| $B(x,1)$ | $\ge4$ | contains the above | Proposition C2 |

At $k=6$ the palette bound is $k-3=3$: exactly the value of the sphere-plus-centre window. So the
palette bound is *attained by the window* — nothing at radius $1$ contradicts a three-label
palette — while the ball of the same radius already forces four.

## 5. Theorem D: k-sensitivity, exactly

**Proposition D1.** With $I_k(S,W)$ as in §0: (i) $I_k(S,W)=\infty$ iff $k<\chi(S)$;
(ii) $I_k(S,W)\ge\chi(S\cap W)$; (iii) $I_k\ge I_{k+1}$; (iv) $I_k(S,W)=I_{|S|}(S,W)$ for
$k\ge|S|$; (v) if $W\subseteq W'$ then $I_k(S,W)\le I_k(S,W')$.

*Proof.* (i) is the definition of $\chi$. (ii) A proper $k$-colouring restricts to a proper
colouring of $S\cap W$. (iii) Every $k$-colouring is a $(k+1)$-colouring with the same value.
(iv) There are at most $|S|$ labels in use. (v) $|c(W)|\le|c(W')|$. $\square$

So $I_k$ is a genuine invariant of the pair $(S,W)$ whose *kink* is at the chromatic threshold: it
is infinite below $\chi(S)$ and it can drop when a colour becomes available. D6's acceptance test
asks for an explicit example where the invariant changes when $k$ changes by one; the exact
enumeration of `verify_windows.py` supplies one and delimits it.

**The spindle, all $128$ windows, exact.** Number of proper $k$-colourings of the spindle:
$0$ at $k=3$, $12$ at $k=4$, $672$ at $k=5$, $7200$ at $k=6$. The attainable tuples
$(I_4,I_5,I_6)$ and their multiplicities over the $128$ windows are
$(0,0,0):1$, $(1,1,1):12$, $(2,2,2):37$, $(3,3,3):26$, $(4,4,4):1$, and — the k-sensitive ones —
$(2,1,1):5$, $(3,2,2):26$, $(4,3,3):20$. Hence:

* $I_4\ne I_5$ for exactly $51$ of the $128$ windows: **the invariant changes when $k$ changes
  by one**. Examples: $W=\{p_0,p_6\}$ has $(I_4,I_5,I_6)=(2,1,1)$, witnessed by
  $c=(1,2,3,1,2,3,0)$ at $k=4$ (two colours on $W$) and $c=(1,2,3,4,2,3,1)$ at $k=5$ (one
  colour on $W$); $W=S\setminus\{p_5\}$ has $(4,3,3)$, witnessed by $c=(1,2,3,1,2,3,0)$ and
  $c=(1,2,3,1,2,4,3)$.
* $I_5=I_6$ for **all** $128$ windows of this configuration. No window of the spindle separates
  $k=5$ from $k=6$.

So the acceptance test of route C is met literally and exactly, at the adjacent pair $4\to5$, by
an explicit unit-distance configuration; and on the same configuration the $5\to6$ pair is
provably not separated. This is the honest scope: a colour-count invariant is $k$-sensitive, but
the sensitivity need not occur at the pair one wants, and verifying that it does is itself a
finite computation — which makes it a falsifiable requirement (R3 below) rather than a slogan.

## 6. The specification: falsifiable requirements for a replacement mechanism

A replacement must satisfy each requirement below; each comes with the test that would refute it,
and with the present method's status, as computed in this note.

**R1 (cross-centre).** It must use information coupling at least two distinct centres.
*Refuted if* it factors through single-centre circle data. *Present method:* passes — it uses
(5.2) and Lemma 5.5. *Constraint on any replacement:* by Theorem B a single-centre variant is
provably limited to $3$ labels on a circle, at every radius, and $3=k-3$.

**R2 (interior).** Or it must use a point at distance $<1$ from the centre (strictly inside the
palette window, or another radius). *Refuted if* its window is $S_1(x)\cup\{x\}$ or a circle.
*Exact threshold:* at radius one, sphere $=2$, sphere-plus-centre $=3$, ball $\ge4$
(Theorem C); two circles of radius $<3/4$ already give $4$ (Proposition C3).

**R3 (k-sensitivity at the required pair).** It must exhibit a computed instance on which its
output differs between $k=5$ and $k=6$. *Refuted if* the two values agree on all instances it
computes. *Present method:* this is exactly the locus recorded as R5 in the brief — the palette bound
changes $2\to3$ but the *conclusion* $|P|\le2$ is what §7 needs, and the §7 cover lemma is
label-blind.
*Warning, computed:* a window colour count does change when $k$ changes by one, but for the
spindle it changes at $4\to5$ and not at $5\to6$ (Theorem D). So "it changes when $k$ changes by
one" is not enough; the pair must be $5,6$.

**R4 (explicit certificate).** Every instance of the mechanism must be a finite object with exact
coordinates, exact unit lengths and a checkable certificate. *Refuted if* a claimed instance has no
exact verification. *This note:* all statements about configurations are exact in
$\mathbb Q(\sqrt3,\sqrt{11})$ (see the scripts).

**R5 (no relabelling artefact).** Its invariant must be invariant under relabelling of the
$k$ labels while being $k$-sensitive. *Refuted if* it is a relabelling of a statement about the
number of labels (e.g. "$k\ge5$"). *Present method:* the §7 cover lemmas are label-blind (R4 of
the brief); the $k$-dependence sits entirely in Proposition 5.6.

**R6 (multiplicity three).** If it produces a planar-cover obstruction, the obstruction must be
valid at multiplicity three; multiplicity two is unavailable at $k=6$. *Refuted if* its cover
lemma has a multiplicity-two hypothesis. *Present method:* fails, exactly, by W4 (explicit
multiplicity-three cover of mesh $2$).

**The example L4 demands.** A proposed replacement that satisfies at least one requirement while
the present method cannot: *use the ball of radius one about the palette centre.* By Proposition
C2 the ball $B(x,1)$ forces four colours, while the present palette window $S_1(x)\cup\{x\}$
forces exactly three. So the replacement satisfies R2 with a computed margin ($4$ versus $3$ at
the same radius, exact coordinates, exact certification) — a property the present method provably
cannot have, because $\chi(S_1(x)\cup\{x\})=3$ is exact (Proposition C1) and no single-centre
circle data does better (Theorem B). It is a proposal, not a solution: nothing here shows that
four colours inside the ball contradict a six-colouring.

## 7. What is not claimed

* This is not the L4 no-go for the whole §§5–7 method. It is a proved no-go for the
  single-centre circle class $\mathcal C$, which is a proper subclass, plus exact window numbers
  at radius one. The full constraint system is direction d1; singleton forcing is d2; the
  $k=4$ calibration is d3; label transport is d4.
* No new bound on $\chi(\mathbb R^2)$ is proved, and no six- or seven-chromatic graph is claimed.
* Theorem D's exhaustive facts are about the seven-vertex spindle only; Propositions D1(i)–(v)
  are the general statements.

## 8. Verification

Scripts (all exact where it matters; run from this directory):

```
python3 verify_sphere.py      # Theorem A: criterion, orbit structure, exact distances
python3 verify_ball.py        # Propositions C1, C2, chi(spindle)=4, exact minimal enclosing circle
python3 verify_two_circles.py # Proposition C3: concyclicity determinants, two exact circles
python3 verify_windows.py     # Theorem D: all 128 windows x k = 4,5,6
python3 verify_windows2.py    # witnesses for the changing windows
python3 verify_concentric.py  # the spindle is not realisable on two concentric circles
```

Key exact outputs: $r=1$ gives six-cycles ($\chi=2$); $r=1/\sqrt3$ gives a triangle of side $1$
($\chi=3$); all $158$ odd-denominator radii with $q\le39$ satisfy the criterion; the eleven
coordinate unit pairs of the spindle coincide with the Lean edge list, $\chi=4$ (no
$3$-colouring among $3^7$ assignments, a $4$-colouring exists); the minimal enclosing circle of
the spindle is exactly $r=3/\sqrt{11}<1$; the concyclic quadruples are $(1,2,4,5)$, $(1,3,5,6)$,
$(2,3,4,6)$ and no others, with the two circle data above; and the window table of Theorem D.

The spindle's non-$3$-colourability and its unit lengths are machine-checked in
`lean/OAI/Geometry/PlaneColoring/Moser.lean` (`moser_not_three_colorable`, `moser_edge_unit`);
this note re-derives both by exhaustive enumeration so that the two routes agree.
