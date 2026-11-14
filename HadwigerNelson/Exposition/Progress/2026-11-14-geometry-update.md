# Two accepted geometry results: curvature and four-label obstruction

**Later same-day update:** the [A6 paired-configuration addendum](2026-11-14-paired-configuration.md) supplies the missing producer for the exact equilateral paired case; the account below records the earlier A5 scope.

**14 November 2026 — paper-level results, independently refereed; not Lean verified.** These contributions supplement the [Proof Walkthrough](../ProofWalkthrough.md). They settle a generic endpoint question and exclude one precise six-colour palette pattern. They do not settle the six-colour endpoint problem or improve the global colouring bound.

## Why a tiny bend changes the endpoint

For a compact connected set $K$, define its **straddling region** by

$$
\operatorname{Straddle}(K)=\{z:\exists p,q\in K,
\ |z-p|<1<|z-q|\}.
$$

A point here sees part of $K$ inside its unit circle and part outside. If certain colours have essential spatial support disjoint from this open region, those colours are unavailable there, up to null sets. Essential support means the support of area measure restricted to a colour class.

The generic strict-aperture MC120 theorem forces a contradiction when its approach directions fit inside a cone narrower than $120^\circ$ and the support exclusions leave at most one colour. **Replacing “narrower than” by “at most” is false.**

The [endpoint proof](../Sources/2026-11-14-a5/ASTRA-MC120-ENDPOINT-A5.txt) constructs actual arcs, not merely a limiting angular picture. With $e(t)=(\cos t,\sin t)$, take

$$
K_\pm=\{t e(\pm(\pi/3+2t)):0\leq t\leq1/100\}.
$$

Both are compact embedded arcs through the same centre, zero. Their limiting signed directions are exactly $+60^\circ$ and $-60^\circ$. The hypothesis constrains those **limiting directions**; the arcs themselves bend outside that closed cone at positive radius. A theorem requiring containment of the whole arcs would be a different question.

Put $W=\operatorname{Straddle}(K_+)\cap\operatorname{Straddle}(K_-)$. Its outer part lies in the open radius-$1/2$ disk centred at $(\sqrt3/2,0)$; its inner part lies in the corresponding disk centred at $(-\sqrt3/2,0)$. There are no points of $W$ on the unit circle. Points within either part are less than one unit apart. Points from opposite parts are more than $199\sqrt3/200>1$ apart. This last estimate matters: the union of the two whole disks would not suffice. Consequently **$W$ has no unit-distance pair**.

That geometry supports a whole-plane Borel, pointwise proper 19-colouring. Start with a proper nine-colour square-grid colouring: cells have side $3/5$, with coordinate indices coloured modulo three. Use one copy of its nine labels outside the plus straddling region, a disjoint copy on the plus-only region, and label 18 on $W$. The plus region excludes the first nine labels; the minus region excludes the second nine. Their combined exclusions leave exactly label 18. Openness upgrades these pointwise absences to the required essential-support exclusions, including the boundary issue.

Straight segments on the same two limiting rays behave differently: for every positive pair of lengths, their common straddling region **does** contain a unit pair. The proof supplies exact coordinates. The curved arcs' outward angular displacement $2t$ dominates the inner angular allowance $\arcsin(t/(2r))<2t$. At the sharp boundary, a bend tending to zero still removes the contact that straight needles force.

The [endpoint referee](../Sources/2026-11-14-a5/ASTRA-MC120-ENDPOINT-REFEREE.txt) accepts all radial regimes, support exclusions, and the straight-segment contrast. This supersedes earlier “endpoint unresolved” descriptions **for generic closed-aperture MC120 only**. The strict theorem survives; the special six-colour endpoint remains unresolved here.

## How odd walks exhaust a four-element list

The [four-list proof](../Sources/2026-11-14-a5/ASTRA-FOUR-LIST-A5.txt) fixes six labels and three disjoint pairs:

$$
A_0=\{1,4\},\quad A_1=\{2,5\},\quad A_2=\{0,3\},\qquad
P(t)=A_{\lfloor(t+\pi/6)/(\pi/3)\rfloor\bmod3}.
$$

Thus six successive open $60^\circ$ sectors carry pairs $A_0,A_1,A_2,A_0,A_1,A_2$. In $0<|z|<2$, remove the six circles $|z-e(\pi/6+k\pi/3)|=1$. On the resulting open domain $D$, the unordered decomposition $z=e(a)+e(b)$ is unique, with distinct nonantipodal vectors away from sector boundaries. Define the available list

$$
L(z)=\{0,1,2,3,4,5\}\setminus(P(a)\cup P(b)).
$$

The region $H=\{e(a)+e(b):\pi/6<a<\pi/2<b<5\pi/6\}$ has constant list $A_0$. Rotate it by $60^\circ$ to obtain $H_1$, with list $A_1$, and reflect $H_1$ across the vertical axis to obtain $H_2$, with list $A_2$. The central point $z_0=i/2$ instead has the four-element list $A_1\cup A_2$.

Here is the finite combinatorial mechanism, independently of its geometric construction. Take a three-edge walk $u_0,u_1,u_2,u_3$, all with list $\{2,5\}$, and make both endpoints adjacent to $z_0$. If $u_0$ receives 2, the labels must be $2,5,2,5$; starting with 5 reverses them. Either way, the endpoints forbid **both** 2 and 5 at $z_0$. A second three-edge walk with list $\{0,3\}$ similarly forbids 0 and 3. The central list is exhausted. This is a concrete nine-vertex abstract example, not a claimed coordinate certificate for the geometric configuration. Any finite odd lengths give the same argument.

The geometric work proves that suitable odd unit-distance walks exist in $H_1,H_2$, with all four endpoints unit neighbours of $z_0$. Locally, two nonparallel unit directions produce an exact four-edge walk to every sufficiently nearby point. Connected active lobes therefore admit finite even walks between their points. A single explicit anchor edge joining opposite lobes turns even-plus-even into odd. Exact contact coordinates place the required endpoints strictly inside these lobes. The proof never assumes that the entire two-list region has one rigid colour.

Taking the union of both finite walks and $z_0$ gives a finite non-list-colourable configuration, entirely inside open cells. Complete walk coordinates, vertex count, and an enumerated edge certificate are **not supplied**.

## What this excludes in an actual colouring

For a measurable weak six-colouring, suppose the actual palette at one fixed centre contains $P(t)$ for almost every angle. The source density lemmas give density-one restrictions to $L(y)$ at every selected vertex. `finite_density_realization` would then produce a proper list colouring of this finite configuration—a contradiction. Thus even almost-everywhere **containment**, not just equality, of this canonical palette is impossible at an actual centre.

The [four-list referee](../Sources/2026-11-14-a5/ASTRA-FOUR-LIST-REFEREE.txt) accepts both conclusions. Producing this canonical pattern from general common-interface data remains a separate obligation. Neither report supplies that producer, a general interface exclusion, or a global bound. Source copies and SHA-256 provenance are recorded [here](../Sources/2026-11-14-a5/provenance.json).
