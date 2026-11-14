# From six approaching sets to the four-list contradiction

**14 November 2026.** The research supervisor checked these paper results; this addendum adds a bounded review of both reports, the six-row arithmetic, and relevant source contracts. It is not Lean verification or a full independent literature review. The previously missing producer is now supplied **for the exact paired configuration below**, connecting the [A5 four-list explanation](2026-11-14-geometry-update.md) to actual interface data.

## The precise input

Take a measurable weak six-colouring $c$ and one centre $x$. For each index $i$ modulo six, let $E_i=\{i,i+1\}$. Six sets $K_i$ have actual ApproachingContinuum data at $x$, with signed directions

$$
(v_0,\ldots,v_5)=(e(0),e(0),e(2\pi/3),e(2\pi/3),e(4\pi/3),e(4\pi/3)).
$$

Here $e(t)=\exp(it)$. For every $a\in E_i$, require its essential spatial support to be disjoint from $\operatorname{Straddle}(K_i)$: the open region of points having both a closer-than-unit and a farther-than-unit witness in $K_i$. All data concern the same colouring and centre. No palette-size bound is assumed, and paired sets need not coincide.

Write $Q(\theta)$ for the actual source palette at $x$. Group the indices into blocks $B_0=\{0,1\}$, $B_1=\{2,3\}$, $B_2=\{4,5\}$. Their excluded label unions are respectively $012$, $234$, and $045$; these digit strings denote sets.

## Hits become forced pairs

The source outer restriction gives a **hit** of the residual labels for blocks with positive directional inner product. The inner restriction gives a hit for negative blocks. Neither says that the entire palette lies in that residual set. Let $\tau=\pi/3$, choose $-\pi/6<t<\pi/6$, and put $Q_j=Q(t+j\tau)$.

| $j$ | Positive blocks | Outer residual | Negative blocks | Inner residual | Forced singleton | Second label |
|---|---|---|---|---|---|---|
| 0 | 0 | 345 | 1,2 | 1 | 1 | 4 |
| 1 | 0,1 | 5 | 2 | 123 | 5 | 2 |
| 2 | 1 | 015 | 0,2 | 3 | 3 | 0 |
| 3 | 1,2 | 1 | 0 | 345 | 1 | 4 |
| 4 | 2 | 123 | 0,1 | 5 | 5 | 2 |
| 5 | 0,2 | 3 | 1 | 015 | 3 | 0 |

For example, row 0 forces $1\in Q_0$ and a hit of $\{3,4,5\}$. The source also makes adjacent palettes $Q_j,Q_{j+1}$ disjoint almost everywhere. Neighbouring rows force $3\in Q_5$ and $5\in Q_1$. Therefore neither 3 nor 5 can supply row 0's hit: **4 must occur**. Repeating this step gives pairs

$$
A_0=\{1,4\},\quad A_1=\{2,5\},\quad A_2=\{0,3\},
\qquad
P(\theta)=A_{\lfloor(\theta+\pi/6)/\tau\rfloor\bmod3}.
$$

Intersecting finitely many shifted conull sets licenses all six rows and neighbour comparisons simultaneously. The six omitted sector endpoints have measure zero. Hence $P(\theta)\subseteq Q(\theta)$ almost everywhere. In fact the neighbouring pairs exclude every other label, forcing equality; containment already suffices.

This is the missing bridge to A5. Its two odd unit walks force both labels of $A_1$ and both labels of $A_2$ at neighbours of a vertex whose list is $A_1\cup A_2$. Source density and finite-realization lemmas turn the actual subpalette inclusion into the impossible finite list colouring. Thus the specified paired configuration cannot occur. Common rotations, reflections, and one global label permutation preserve the conclusion.

## Two carefully bounded extensions

**At most three distinct directions:** conditional on the accepted CC60 and strict-MC120 paper inputs, coincident blocks have at most two adjacent indices. Three directions must therefore carry the paired matching. Each pair of blocks excludes five labels, so strict MC120 forces their circular separation to be at least $120^\circ$. Three such directions must be equilateral, returning to the case just excluded. This does not classify four-, five-, or six-direction configurations.

**A uniform open neighbourhood:** fix one finite A5 obstruction before choosing any colouring. Its finitely many decomposition angles have a positive minimum margin $\eta$ from sector boundaries. Choosing, for example, $\epsilon_0=\min(\eta/4,\pi/24)$ permits independent perturbations of all six directions. On sectors trimmed by $\epsilon_0$, the sign table survives; the trimmed set is invariant under $60^\circ$ shifts. Local interval palette inclusions supply the density restrictions at the fixed vertices, even if individual angles are exceptional. This yields a uniform existential tolerance without MC120. No numerical tolerance or enumerated graph is supplied.

Read the [producer](../Sources/2026-11-14-a6/ASTRA-PAIRED-PRODUCER-A6.txt), [corollary audit](../Sources/2026-11-14-a6/ASTRA-PAIRED-COROLLARIES-A6.txt), and [provenance](../Sources/2026-11-14-a6/provenance.json). These results give no global six-colouring impossibility or improved global bound.
