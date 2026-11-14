# Section 7 at six colours

*Swarm smwfo9zkl, member m8, direction d16.*
Paper: `attachments/here-are-three-files-ni5n/paper.pdf`, "The Euclidean plane is not
five-colorable". Section numbers, equation numbers and printed page numbers below refer to
that paper (Section 7 occupies printed pages 42–50).

---

## 0. What is proved here

Let $k\ge 3$, let $c$ be a weak measurable $k$-colouring in the sense of the paper's
Definition 1.2, let $H_1,\dots,H_k$ be the closed essential supports, $\Gamma_x$ the transition
graph of Definition 6.1, and

$$L=\{x\in\mathbb R^2:\ \Gamma_x\text{ contains a cycle}\}$$

the cyclic locus.

**Theorem 1 (cyclic centres exist, unconditionally).** *For every closed square $Q$ with
$\operatorname{side}(Q)>2$ one has $L\cap Q\neq\emptyset$. In particular $L\neq\emptyset$; and by
the transfer Theorem 1.3 of the paper the same conclusion holds for every proper $k$-colouring of
the plane, with no regularity assumption. No hypothesis on $L$ is used: neither local finiteness,
nor closedness, nor any palette bound.*

This settles the nonemptiness half of the sprint's missing prerequisite, at every $k$, and leaves
only finiteness. Proof: §2.1.

**Theorem 2 (Section 7 at $k$ colours, with the sharp hypothesis).**
*Suppose*

* **(H)** *there is a closed square $\widetilde Q$ with $\operatorname{side}(\widetilde Q)>2$ such
  that $L\cap\widetilde Q$ is finite and nonempty.*

*Then there exist a point $x\in L\cap\operatorname{int}\widetilde Q$, an integer
$\ell\in\{3,\dots,k\}$, distinct labels
$i_0,\dots,i_{\ell-1}\in\{1,\dots,k\}$, a radius $\rho>0$ and, for each edge $i_ji_{j+1}$ of
the simple cycle (indices mod $\ell$), a compact connected set $K_j\subset B(x,\rho)$, a
direction $v_j\in S^1$ and a sequence $q_{j,t}\in K_j\setminus\{x\}$ such that*

1. $x\in K_j$ and $K_j\cap\partial B(x,\rho)\neq\emptyset$;
2. $q_{j,t}\to x$ and $(q_{j,t}-x)/|q_{j,t}-x|\to v_j$;
3. $H_{i_j}\cap\Delta(K_j)=H_{i_{j+1}}\cap\Delta(K_j)=\emptyset$, where
   $\Delta(K)=\{z:\min_{q\in K}|z-q|<1<\max_{q\in K}|z-q|\}$.

This is Proposition 7.1 of the paper, at an arbitrary number of colours, under a hypothesis
strictly weaker than the paper's input (Theorem 6.5). The paper's Proposition 7.1 is the case
$k=5$; at $k=6$ the conclusion is a cycle of exclusion continua of length $3$, $4$, $5$ or $6$.

**Theorem 3 (the step that turns a three-label palette into a point of the 1-skeleton).**
It is Lemma 7.4 together with Lemma 7.3, not the palette bound. Precisely: on the region where
Theorem 2 is proved, for every point $w$ outside the hole disks, the label set
$S_w=\{i:p_i^\varepsilon(w)>\alpha\}$ is a clique of the forest $\Gamma_z$ of every selected ball
containing $w$, hence has at most two elements. Section 7 never uses $|P_x(e)|\le 2$,
never cites Proposition 5.6, Lemma 5.5, (5.2) or (5.3), and this is checked mechanically
(§7 below). The dependence on the number of colours is three constants only:
$\alpha<1/k$, $G=K_k$, and $\ell\le k$.

**Theorem 4 (the covering step cannot be repaired at multiplicity three).**
(a) *(Sharp form of Lemma 7.5.)* For a closed square of side $S$ and $0<\mu<S/2$, there is no
relatively open cover of it with multiplicity at most two and mesh at most $\mu$.
(b) For every $S>0$ and every $\mu>0$ a closed square of side $S$ has a relatively open cover
with multiplicity at most three and mesh at most $\mu$; explicit rational certificates, in five
parameter settings, with two independent exact decision procedures, are in
`cover_cert.py` (§8).
Consequently no cover-theoretic strengthening of Section 7 can close the gap left by a
three-label palette: at multiplicity three there is no mesh obstruction at all.

**Corollary 5 (where the six-colour problem now stands).**
At $k=6$ the hypothesis (H) of Theorem 2 has two halves. Theorem 1 supplies the nonemptiness half
unconditionally and at every scale $>2$. The finiteness half is what remains: **(H) holds at
$k=6$ as soon as some closed square of side greater than two contains only finitely many cyclic
centres.** Theorem 6.5 of the paper at $k=6$ would give exactly that, and it is strictly weaker
than local finiteness: it asks for finiteness of $L$ on **one** square of side greater than two,
not on every compact set (Proposition 5.2). Nothing else in Section 7 depends on the number of
colours.

---

## 1. Conventions taken verbatim from the paper

* Weak measurable $k$-colouring: Definition 1.2 (measurable $c:\mathbb R^2\to\{1,\dots,k\}$
  with $\sum_i\iint_{B(0,R)\times S^1} 1_{A_i}(x)1_{A_i}(x+u)\,d\sigma(u)\,dx=0$ for all $R$).
* Typical point, closed essential support
  $H_i=\{q: |A_i\cap B(q,r)|>0 \text{ for all } r>0\}$: §5.1.
* Circle traces $W_x$ and maximal palettes $P_x(e)$: Definition 5.1.
* Transition graph: Definition 6.1, $ij\in\Gamma_x$ iff for every ball $B$ about $x$
  $\limsup_{h\to0,h\ne0} |D_{ij}(B,h)|/|h|>0$.
* Density-point properness: Lemma 4.3, *stated for a weak measurable $k$-colouring*, so valid at
  every $k$.
* $\Delta(K)$: (7.1). Disk averages $p_i^\varepsilon$ and (7.2): Lemma 7.2.
* The thresholded coordinates $q_i^\varepsilon$: (7.4). Target graph $G$: the one-skeleton of
  the simplex of probability vectors on the label set $I$, i.e. the complete graph $K_{|I|}$.

---

## 2. Proof of Theorem 2

The proof is the paper's proof of Proposition 7.1, with each item audited for its dependence on
$|I|$. I state each item in $k$-general form and record what changes.

**Step 0 (choice of the squares).** By (H) choose closed squares $Q\subset\operatorname{int}\widetilde Q$
with $\operatorname{side}(Q)>2$, and put $Q':=\widetilde Q$, $L_0:=L\cap Q'$, a finite nonempty
set with $L\cap Q=L\cap Q'$ and $\partial Q\cap L=\emptyset$. (Paper: $Q$ a closed square of side
ten with $\partial Q\cap L=\emptyset$ and $Q'\supset Q$ with $L_0=L\cap Q'$ finite.) *Hypotheses
used:* (H) for finiteness and nonemptiness. No dependence on $|I|$. The paper's Theorem 6.5
supplies (H) because $L$ is closed and locally finite.

**Step 1 (Lemma 7.2, disk inequalities).** For $|q-z|=1$ and every label $i$,
$p_i^\varepsilon(q)+p_i^\varepsilon(z)\le 1$; and $q_n\to q$, $\varepsilon_n\to0$,
$\liminf p_i^{\varepsilon_n}(q_n)>0$ imply $q\in H_i$. *Proof:* translation-averaging plus the
fact that two typical points at distance one carry different colours (Lemma 4.3). Both
statements are about a single label and use no bound on $|I|$. **$k$-free.**

**Step 2 (Lemma 7.3, a missing edge has small overlap).** If $ij\notin\Gamma_x$ there is a ball
$B$ about $x$ such that for every ball $B'\subset B$
$\int_{B'}p_i^\varepsilon p_j^\varepsilon\,dq=o(\varepsilon)$, and for $B''\subset B'$ the set
$\{q\in B'':p_i^\varepsilon(q)>\alpha,\ p_j^\varepsilon(q)>\alpha\}$ is covered by finitely many
open disks whose total radii tend to $0$. *Proof:* the negation of (6.1) at $x$ gives
$|D_{ij}(B,h)|=o(|h|)$; expand the product of the two disk averages and change the root. The only
inequality used about the colouring is properness ($h_1=h_2$ gives an empty event).
$\alpha>0$ is arbitrary. **$k$-free.**

**Step 3 (the target graph).** Fix $0<\alpha<1/k$ and set
$q_i^\varepsilon(z)=(p_i^\varepsilon(z)-\alpha)_+/\sum_{m\in I}(p_m^\varepsilon(z)-\alpha)_+$.
*Changes from the paper:* the paper writes $0<\alpha<1/5$ and "the denominator is positive
because the five probabilities sum to one". At $k$ colours the sum is still one, and
$\max_m p_m^\varepsilon\ge 1/|I|$ at every point, so the denominator is positive **iff**
$\alpha<1/|I|$. At $k=6$ this is $\alpha<1/6$, and the constant is forced: at $\alpha=1/6$ the
constant vector $p\equiv1/6$ makes (7.4) undefined. This is the first $k$-dependent constant.
$G$ is the one-skeleton of the simplex on $I$, i.e. $K_k$ (paper: "complete graph on its five
vertices"). **$k$-dependent constant 2.**

**Step 4 (Lemma 7.4, small holes and tree fillings).** With $\delta>0$,
$M_\delta=Q'\setminus\bigcup_{y\in L_0}B(y,\delta)$, every $\Gamma_z$, $z\in M_\delta$, is a
forest: $M_\delta\cap L=\emptyset$ because $L\cap Q'=L_0$. For each $z\in M_\delta$ and each
nonedge $ij$ of $\Gamma_z$, Step 2 supplies a disk cover of the violation set in $B(z,s_z)$ with
total radii $\to0$; finitely many balls $B(z,s_z)$ cover $M_\delta$. Marking those disks and
merging until closures are disjoint gives families $H_n$ with total radii
$\le|L_0|\delta+m_{\delta,\varepsilon}+\eta\to0$, one core disk $B_{n,x}$ per point of $L_0$,
and a continuous $g_n:Q\setminus\bigcup_{y\in L_0\cap Q}B_{n,y}\to G$ equal to
$q^{\varepsilon_n}$ off the holes. **This is the only place where the number of labels could
enter, and it does not:** see Theorem 3 below. The finiteness of $|L_0|$ is used for the total
radius bound and for "no final disk contains two points of $L_0$", i.e. for (H).

**Step 5 (Lemma 7.5, cover obstruction, sharpened).** See Theorem 4(a). It is a statement about
relatively open covers of a square and mentions no colouring. **$k$-free.** The paper states it
for side ten and mesh at most two; the proof gives mesh $<\operatorname{side}/2$, which is what
Step 7 needs when the square is not the paper's.

**Step 6 (Lemma 7.6, non-null core loops).** If every core boundary loop were null homotopic, the
loops extend over their disks and paste to a continuous $\tilde g_n:Q\to G$ equal to
$q^{\varepsilon_n}$ off the holes. For $i\in I$ let $U_{n,i}$ be the components of
$\{z\in Q:(\tilde g_n(z))_i>0\}$. Every point of $G=K_k$ has at most two positive barycentric
coordinates, so this is an open cover of multiplicity at most two; its mesh is at most
$1+o(1)$: otherwise paths in one $U_{n,i}$ join points $a_n,b_n$ with $|a_n-b_n|>1+c-o(1)$, the
limit $a$ lies in $H_i$ by Step 1, and the path-crossing distance argument of the paper with
(7.2) gives $\alpha|A_i\cap U|\le\|p_i^{\varepsilon_n}-a_i\|_{L^1(U)}+\alpha|E_n\cap U|\to0$,
contradicting $a\in H_i$. For large $n$ the mesh is below $\operatorname{side}(Q)/2$, so Step 5
applies. All constants ($1$, $\alpha$) are $k$-free; the multiplicity bound is the $k$-free
statement "a point of a one-skeleton has at most two positive barycentric coordinates".

**Step 7 (Lemmas 7.7 and 7.8, reduced words and annulus crossings).** Pure graph theory and
continuum topology for a finite connected simple graph $G$ and a closed annulus. **$k$-free.**

**Step 8 (assembly).** Passing to a subsequence, fix $x\in L_0\cap\operatorname{int}Q$ whose core
loop is non-null at every index (Step 6); choose $\rho>0$ with $B(x,\rho)\subset
\operatorname{int}Q$ and $B(x,\rho)\cap L_0=\{x\}$ (possible because $L_0$ is finite with
$x\in\operatorname{int}Q$, so the other points of $L_0$ and $\partial Q$ are at positive
distance), so
$g_n$ is defined on the annulus $A_n=B(x,\rho)\setminus B_{n,x}$. Its inner boundary word
contains a simple cycle (Lemma 7.7); there are finitely many simple cycles in $K_k$, so fix one,
of length $\ell\in\{3,\dots,k\}$ — **$k$-dependent constant 3** (paper: "$\ell\in\{3,4,5\}$",
from "the complete graph on five vertices"). Edge midpoints give, by Lemma 7.8, compact connected
$K_{n,j}$ crossing $A_n$; Hausdorff limits $K_j$ meet both $\partial B_{n,x}$ and
$\partial B(x,\rho)$, hence contain $x$ and meet $\partial B(x,\rho)$. For the exclusion: off the
holes $g_n=q^{\varepsilon_n}$ equals an edge midpoint, whose two endpoint coordinates are $1/2$,
so $p_i^{\varepsilon_n}>\alpha$ there; for $z$ in a closed ball $U\subset\Delta(K_j)$ some point
of $K_{n,j}$ is at distance exactly one from $z$ (connectedness of
$q\mapsto|z-q|$ plus the uniform strict margins on $U$), so (7.2) gives
$p_i^{\varepsilon_n}(z)\le1-\alpha$, and the estimate
$\alpha|A_i\cap U|\le\|p_i^{\varepsilon_n}-a_i\|_{L^1(U)}+\alpha|E_n\cap U|\to0$ gives
$H_i\cap\Delta(K_j)=\emptyset$ for both endpoint labels. Finally
$\{|q-x|:q\in K_j\}=[0,\rho]$ because $K_j$ is connected and meets both boundary circles, and
choosing points at radii $\rho/t$ and passing to a subsequence of directions gives the $v_j$ and
$q_{j,t}$. ✓

*Notation.* The paper's proof writes "choose points in $K_j$ at radii $\rho/k$, $k\ge2$";
that $k$ is a dummy radius index and has nothing to do with the number of colours. It is
written $\rho/t$ here.

**Vacuity check.** At $k=5$, Steps 0–8 are literally the paper's proof and Theorem 2's conclusion
is the paper's Proposition 7.1, so the generalisation is not vacuous: it reproduces the known
$k=5$ statement. At $k=6$ the only differences in the whole of Section 7 are
$\alpha<1/6$, $G=K_6$ and $\ell\in\{3,4,5,6\}$.

### 2.1 Proof of Theorem 1: no colouring is without a cyclic centre

The paper's Lemma 7.6 ends with the sentence "This argument also rules out the possibility of
having no core disks in $Q$." Read literally, that sentence needs no hypothesis on $L$ at all, and
that reading is Theorem 1.

*Proof of Theorem 1.* Let $Q$ be a closed square with $\operatorname{side}(Q)>2$ and suppose
$L\cap Q=\emptyset$. Run the paper's construction with $Q':=Q$ and $L_0:=L\cap Q'=\emptyset$; then
$M_\delta=Q'\setminus\bigcup_{y\in L_0}B(y,\delta)=Q$.

*Every $\Gamma_z$, $z\in Q$, is a forest*, because $Q\cap L=\emptyset$. No finiteness of $L$ is
needed: $L_0$ is empty.

*The hole families exist.* For each $z\in Q$ and each nonedge $ij$ of $\Gamma_z$, Lemma 7.3
supplies a ball $B(z,3s_z)$ and disk covers, with total radii $\to0$, of the violation set
$\{q\in B(z,s_z):p_i^\varepsilon(q)>\alpha,\ p_j^\varepsilon(q)>\alpha\}$; there are finitely many
nonedges, so one radius $s_z$ works, and finitely many balls $B(z,s_z)$ cover the compact $Q$.
Marking all these disks and merging until closures are disjoint gives finite families $H_n$ of open
disks with pairwise disjoint closures and total radii at most
$|L_0|\delta+m_{\delta,\varepsilon}+\eta=m_{\delta,\varepsilon}+\eta\to0$, and
$q^{\varepsilon_n}$ takes values in $G=K_k$ on $Q\setminus\bigcup_{B\in H_n}B$ by the
clique-in-a-forest argument of §3.

*Pasting gives a graph-valued map on the whole square.* Every disk of $H_n$ is non-core, since
$L_0=\emptyset$. The boundary of such a disk is mapped by $q^{\varepsilon_n}$ into the forest
$\Gamma_z$ of the selected ball containing it (it avoids all marked interiors); a connected subset
of a forest lies in one component tree, a finite tree is contractible, so the boundary map extends
continuously over the closed disk; if the disk crosses $\partial Q$, extend on the whole disk and
restrict. Finitely many disks with disjoint closures, continuous pasting. This gives a continuous
$$g_n:Q\longrightarrow G=K_k,\qquad g_n=q^{\varepsilon_n}\ \text{off}\ \textstyle\bigcup H_n .$$

*The cover.* There are no core disks, so the hypothesis "every core boundary loop is null
homotopic" of Lemma 7.6 holds vacuously with $\tilde g_n:=g_n$. For $i\in I$ let $U_{n,i}$ be the
components of $\{z\in Q:(g_n(z))_i>0\}$; $Q$ and its relatively open subsets are locally path
connected, so these components are relatively open and path connected, and they cover $Q$. Every
point of $G=K_k$ has at most two positive barycentric coordinates, so the cover has multiplicity at
most two. Its mesh is at most $1+o(1)$: otherwise, exactly as in the paper, paths in one $U_{n,i}$
join points $a_n,b_n$ with $|a_n-b_n|>1+c-o(1)$; endpoints lying in a hole are replaced by boundary
points of the same path, legitimate because the disks are non-core and $q^{\varepsilon_n}$ is
preserved on their boundaries; the limits satisfy $|a-b|>1$ and $a\in H_i$ by Lemma 7.2; then for
$z$ in a small ball $U$ about $a$ the distances to $a_n$ and $b_n$ straddle $1$, so some point of
the path is at distance exactly $1$ from $z$, and if $z\notin E_n$ that point is outside all closed
holes, where $g_n=q^{\varepsilon_n}$ has positive $i$-th coordinate, so
$p_i^{\varepsilon_n}(z)>\alpha$ and (7.2) gives $p_i^{\varepsilon_n}(z)\le1-\alpha$; hence
$\alpha|A_i\cap U|\le\|p_i^{\varepsilon_n}-a_i\|_{L^1(U)}+\alpha|E_n\cap U|\to0$, contradicting
$a\in H_i$.

For large $n$, then, $Q$ carries a relatively open cover of multiplicity at most two and mesh
$<\operatorname{side}(Q)/2$, contradicting Theorem 4(a). Hence $L\cap Q\neq\emptyset$. $\square$

*Consistency.* (i) For $k\le5$ the hypothesis of Theorem 1 is false (the paper proves that no weak
measurable five-colouring exists), so the statement is vacuous there and nothing is contradicted.
(ii) For $k\ge7$ the hexagonal colouring exists, so Theorem 1 is non-vacuous. (iii) At $k=2$ the
same argument would say that a weak measurable $2$-colouring has a cyclic centre, which is
impossible because $\Gamma_x\subseteq K_2$ is acyclic; the argument therefore proves that no weak
measurable $2$-colouring exists, which is true, so the argument is not in trouble. (iv) The
constant $2$ is what the argument gives: the covering mesh is $1+o(1)$ and the obstruction needs
mesh below half the side. Nothing is asserted about squares of side at most two.

*What it does not give.* Theorem 1 is existential at scale $2$; it says nothing about finiteness.
At $k=6$ it removes the nonemptiness half of the missing prerequisite and leaves the finiteness
half, i.e. (H) with "finite" as the only open condition.

---

## 3. Theorem 3: which step converts a palette to a point of the 1-skeleton

The question the sprint asks is what happens at $k=6$ to the sentence "outside disks with
vanishing total radii, these modified vectors have at most two positive coordinates, so they lie
in the complete graph on the five labels". There are three candidate answers, and only one is
correct.

*Not the palette bound.* Section 5 proves $|P_x(e)|\le2$ at $k=5$ (Proposition 5.6). Its proof
breaks at $k=6$: a $3$-set $A$ in $P_x(e)$ forces the circle $v\mapsto x+e+v$ to be coloured, off
a null set, by the complement of $A$, which has $6-3=3$ labels, whereas the conversion of such a
circle into a binary centre uses the angular exclusion (5.7) under the rotation $R$ of order six,
which alternates the two members of a *two-element* palette and says nothing about a three-element
one. So at $k=6$ one gets $|P_x(e)|\le3$ and no further.

*Not the threshold either.* Thresholding at $\alpha$ does not by itself reduce the number of
positive coordinates: $p_i>\alpha$ can hold for three labels simultaneously, and then
$q^\varepsilon$ is a point of a 2-simplex, not of $G$.

*It is Lemma 7.3 plus Lemma 7.4.* Let $w\in Q$ be outside all hole disks of $H_n$ and let
$B(z,s_z)$ be a selected ball containing $w$. Let $P=\{i:p_i^{\varepsilon_n}(w)>\alpha\}$; this
is $\{i:q_i^{\varepsilon_n}(w)>0\}$ by (7.4). If $\{i,j\}\subseteq P$ were a nonedge of
$\Gamma_z$, then $w$ would lie in the violation set of Step 2 for the nonedge $ij$, hence in the
interior of one of the marked disks — contradiction. So $P$ is a clique of $\Gamma_z$. Since
$z\in M_\delta$, $\Gamma_z$ is a forest, and a forest has no clique of size three. Hence
$|P|\le2$, and a two-element clique in a graph is an edge of $G$. $\square$

Two remarks that matter for the $k=6$ transfer.

(i) The argument is uniform in the palette: the size of the maximal palette $P_x(e)$ is never
used, only the size of the clique, and the forest property is a property of $\Gamma_z$ for
$z\notin L$, which is where Step 4 lives.

(ii) The hypothesis "$\Gamma_z$ is a forest" is available on $Q\setminus\{\text{core disks}\}$,
i.e. exactly where Theorem 2 uses it, and the core disks are those around $L_0$; so the whole
mechanism is tied to the cyclic locus and to nothing else. This is why the sharp hypothesis of
Theorem 2 is a statement about $L$ alone.

(iii) What the argument controls is the number of positive *disk averages* $p_i^\varepsilon(w)$,
not the size of the angular palette $P_x(e)$. No relation between the two is used, and none is
needed: Definition 5.1 (angular traces at a centre) and (7.4) (spatial averages around a point)
are different objects, and the only bridge Section 7 uses is the transition graph, through Lemma
7.3. So a proposed repair of the $k=6$ transfer that tries to bound $|P_x(e)|$ directly is aimed
at a quantity Section 7 never reads.

---

## 4. What Theorem 2 consumes, and that the consumption is exact

**Proposition 5.1 (local finiteness gives (H)).** If $L$ is closed, locally finite and nonempty,
then every closed square of side $3$ meets $L$ in a finite set, so translating it to meet $L$
gives a square $\widetilde Q$ of side $3$ with $L\cap\widetilde Q$ finite and nonempty. Hence (H).
$\square$

So Corollary 5 follows from Theorem 2: the paper's Theorem 6.5 at $k=6$ gives (H) at $k=6$.

**Proposition 5.2 ((H) is strictly weaker than local finiteness).** The closed set
$L=\{0\}\cup\{10^6+1/n:n\ge1\}$ has $L\cap[-1.5,1.5]^2=\{0\}$ finite, but is not locally finite
near $10^6$. So (H) does not imply local finiteness. (This is a statement about the hypotheses of
the argument, not about which sets arise as cyclic loci of colourings — that is the open
question.) $\square$

**Proposition 5.3 (three things this proof cannot do without).**

1. *Finiteness in one square.* Lemma 7.4 needs one core disk per point of $L_0$ and the total
   radius bound $|L_0|\delta+m_{\delta,\varepsilon}+\eta\to0$. With $L\cap Q'$ infinite neither
   is available. A thinness variant survives the radius bound — a set coverable by finitely many
   disks of total radius below any given $\eta$, such as $\{1/n\}$, would do — but then the
   clauses "different points give different core disks" and "no final disk contains two points of
   $L_0$" fail, and clause 2 below does not.
2. *Isolation of the chosen centre.* Step 8 needs $g_n$ defined on the closed annulus
   $B(x,\rho)\setminus B_{n,x}$, and $g_n$ is defined only off the core disks. Hence $B(x,\rho)$
   must meet no other core disk, i.e. $x$ must be an isolated point of $L$. If every point of $L$
   is an accumulation point of $L$, no $x$ can be used, whatever the other hypotheses.
3. *A square wider than two.* Step 6 gives the covering mesh only as $1+o(1)$, and Step 5 needs
   mesh $<$ half the side of the square. So $\operatorname{side}(\widetilde Q)>2$ is required and
   $2$ cannot be replaced by anything smaller.

So the exact input is (H). In particular neither $L\ne\emptyset$ alone nor "L has an accumulation
point" runs this argument; and a further, strictly weaker hypothesis exists (isolated $x$ plus the
thinness condition of clause 1) but does not appear to be easier to establish than (H), since (H)
is what the paper's Theorem 6.5 delivers.

## 5. Theorem 4: the covering step is irreparable at multiplicity three

**Proof of (a).** Let $\mathcal U$ be a relatively open cover of the closed square $Q$, of
multiplicity at most two and mesh at most $\mu<\operatorname{side}(Q)/2$. Compactness gives a
finite subcover $U_1,\dots,U_N$ with the same bounds; no $U_a$ equals $Q$ because
$\operatorname{diam}Q=\operatorname{side}(Q)\sqrt2>\mu$. Let $\varphi_a$ be a partition of unity
subordinate to $U_a$ and put $F(z)=\sum_a\varphi_a(z)z_a$ with $z_a\in U_a$. Then $F(Q)\subset Q$
by convexity, at most two weights are positive at any point, so $F(Q)$ lies in a finite union of
segments $[z_a,z_b]$ and points, and $|F(z)-z|\le\sum_a\varphi_a(z)|z_a-z|\le\mu$. For
$y\in Q$ with $\operatorname{dist}(y,\partial Q)>\mu$ the map $z\mapsto y+z-F(z)$ sends $Q$ into
the closed $\mu$-ball about $y$, which lies in $Q$; Brouwer's fixed point theorem gives $z$ with
$F(z)=y$. Hence $F(Q)$ contains $\{y\in Q:\operatorname{dist}(y,\partial Q)>\mu\}$, which is
nonempty and open because $\mu<\operatorname{side}(Q)/2$, and is contained in no finite union of
segments. Contradiction. $\square$

The paper states this with $\operatorname{side}(Q)=10$ and $\mu=2$; the proof above is the same
proof with the constants kept, and it is the form Step 6 needs when the square is chosen around
an isolated cyclic centre rather than being of side ten.

**Proof of (b).** Let $L,h>0$ and $\varepsilon<\min(L,h)/2$, and tile the plane by closed bricks
$[iL,(i+1)L]\times[jh,(j+1)h]$ with the rows of odd $j$ shifted by $L/2$. Every point of the plane
lies in the closure of at least one brick, and in the closure of at most three (one in the
interior of a brick, two on a brick edge, three at a T-junction; the alternate-row shift is what
keeps the valence at three). Replacing each brick by its open $\varepsilon$-enlargement
$(x_0-\varepsilon,x_1+\varepsilon)\times(y_0-\varepsilon,y_1+\varepsilon)$ therefore yields a
relatively open cover of every closed square with multiplicity at most three, and every member
has diameter $\sqrt{(L+2\varepsilon)^2+(h+2\varepsilon)^2}$. Given $\mu>0$ choose
$L=h=\mu/4$, $\varepsilon=\mu/100$; then the diameter is $<0.36\mu<\mu$. $\square$

**Machine check.** `cover_cert.py` verifies (i) covering, (ii) multiplicity at most three,
(iii) diameters, for five exact parameter settings, using integer arithmetic only, by two
independent decision procedures: an arrangement decomposition into strata with exact
containment tests, and a sweep that solves a one-dimensional open-interval covering problem and
an open-interval maximum-depth problem at every abscissa. Every instance reports maximum
multiplicity exactly $3$, i.e. the same families are *not* multiplicity-two covers. That is the
sharpness control demanded of any no-go: the computation does not also destroy the
multiplicity-two case, which is known to be obstructed.

**Why it matters.** If a $k=6$ colouring could produce a covering of multiplicity three at the
Section 7 stage, no mesh bound would contradict it, since (b) produces multiplicity-three covers
of arbitrarily small mesh. So Theorem 4 rules out the natural attempted repair of Section 7 at
six colours ("run Lemma 7.5 with multiplicity three") and shows that the reduction to the
1-skeleton must come from the transition graph — which, by Theorem 3, it does, at every $k$.

---

## 6. Where the six-colour problem stands after Theorems 1 and 2

Section 7 is not where the six-colour case fails. Assuming only (H) — one closed square of side
greater than two that contains finitely many, and at least one, cyclic centres — Section 7
delivers the cycle of exclusion continua with $\ell\in\{3,4,5,6\}$. Two things remain, and they
are an input to Section 7 and a consumer of its output, not parts of it.

1. **(H) at $k=6$**, of which only the finiteness half is open: by Theorem 1 every closed square
   of side greater than two meets $L$, so what is missing is that *one* such square meets it
   finitely. The paper's route to finiteness is Theorem 6.5, whose proof uses $|P_x(e)|\le2$
   (Proposition 5.6) in every case, and at $k=6$ one has only $|P_x(e)|\le3$. Theorem 2 shows that
   Section 7 needs (H) and nothing stronger, so (H) is the target; full local finiteness is more
   than necessary.
2. **Section 8 at $k=6$.** The output of Proposition 7.1 has to be contradicted for each of
   $\ell=3,4,5,6$. The paper excludes $\ell=3,4,5$ at $k=5$, and its arguments compute with
   palettes of size at most two: a five-cycle leaves one label outside, a four-cycle two
   antipodal pairs, a three-cycle leaves two outside labels and produces an open region using
   only the three cycle labels, into which the Moser spindle is placed. At $k=6$ a three-cycle
   leaves *three* outside labels, so the last step of the triangle case produces an open region
   carrying three labels almost everywhere rather than the two needed for the Moser
   contradiction, and $\ell=6$ is a cycle length with no $k=5$ analogue. Those are the remaining
   tasks, and neither is a defect of Section 7.

The value of the transfer is therefore a reduction: **the six-colour gap is the finiteness of $L$
on one square of side greater than two, plus Section 8 at $\ell=3,4,5,6$; Section 7 itself,
including its covering step, needs no new geometry at six colours, and the existence of cyclic
centres is not a gap at all.**

## 7. Reproducing the audit of Section 7

`python3 audit_s7.py` extracts Section 7 from the PDF with `pdftotext -layout` and reports

* every occurrence of `(5.2) (5.3) (5.5) (5.6) (5.7) Lemma 5.5 Proposition 5.6 palette
  "two labels" |P cardinality` inside Section 7 — **zero**;
* every occurrence of "five", for hand checking: five occurrences, of which two are the standing
  hypothesis ("a weak measurable five-coloring is given" and the statement of Proposition 7.1)
  and three are the allowed shapes ("the five probabilities sum to one", "complete graph on its
  five vertices" twice);
* the three $k$-dependent constants: `Fix 0 < α < 1/5`, `complete graph on its five vertices`,
  `of length ℓ ∈ {3, 4, 5}`.

Current output: `audit passes: True`.

The displayed formulas (7.1)–(7.7), Lemma 7.5's "side ten / mesh at most two" and Lemma 7.6's
"mesh at most 1 + o(1)" were checked against a second, independent extraction (`mutool draw
-F stext`, which reports glyph positions rather than layout columns); the two agree on every
formula quoted above, including `Fix 0 < α < 1/5` and (7.4).

---

## 8. Reproducing the certificates

```
python3 cover_cert.py
python3 audit_s7.py
```

`cover_cert.py` prints five certified instances and exits 0. Requirements: Python 3, no
third-party packages.

---

## Appendix: what is not claimed

* Theorem 2 is conditional on (H). Theorem 1 supplies the nonemptiness half of (H) at every $k$
  but says nothing about finiteness, so neither theorem proves $\chi(\mathbb R^2)\ge7$.
* Theorem 1 is a *reading* of a sentence already present in the paper (the last clause of Lemma
  7.6), not a new method: its content is that the clause needs no hypothesis on $L$. It is
  nevertheless the statement the sprint asked for, since the sprint lists nonemptiness of the
  cyclic locus at $k=6$ as unknown.
* Theorem 2 does not address Section 8. The output at $k=6$ is a cycle of length up to six; the
  exclusion of lengths $3,4,5,6$ at three-label palettes is not done here.
* Theorem 4(a) is the paper's argument with the constants kept; it is a sharpening, not a new
  method. Theorem 4(b) is a certificate for a known-sharp phenomenon, included because the
  no-repair conclusion of §5 needs it and because the sprint requires certificates for
  satisfiability claims.
* The computations certify the finitely many stated instances; the statement "at every mesh" in
  Theorem 4(b) is the parametric construction, whose correctness is the short proof in §5, not a
  computation.
