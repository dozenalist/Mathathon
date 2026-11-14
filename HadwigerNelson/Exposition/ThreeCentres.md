# Three centres, one remaining label

A useful simplification of the supplied proof ends with a contradiction you can reproduce using three sets. Its force comes from connecting that finite argument to actual measurable colour data. The new argument replaces particular strict-state consumers; it does not improve the supplied plane-colouring bound. The [A2 report](../Main/ResearchSnapshot/local/outputs/ASTRA-JOINT-STATE-A2.txt) proposes the route, and [MovingThreeCentres.lean](../Main/ResearchSnapshot/local/outputs/three-centre/MovingThreeCentres.lean), `triangle_no_unit_of_avoiding_traces`, gives its precise implementation.

## Start with the triangle

Place three centres at

$$
x=(0,0),\qquad y=(1,0),\qquad z=(1/2,\sqrt3/2).
$$

All three distances are one. At a common angular parameter $t$, write $P,Q,R$ for the palettes at $x,y,z$. A palette records labels occurring positively in appropriate limiting angular samples; it need not be the singleton colour of the centre.

For a concrete five-label example, use the universe $\{0,1,2,3,4\}$ and set

$$
J=\{0,1\},\qquad K=\{2,3\},\qquad X=4.
$$

Suppose $J\subseteq P$, the three palettes are pairwise disjoint, and neither $Q$ nor $R$ is contained in $K$. Choose $j\in Q\setminus K$. Disjointness from $P$ rules out $0,1$, while the choice of $j$ rules out $2,3$. Therefore $j=4$. Repeating the argument for $R$ puts $4$ in both $Q$ and $R$, contradicting their disjointness.

We did **not** prove $Q=R=\{4\}$. Either palette could also contain labels in $K$. One forced common member is enough.

This is the entire finite-set argument. In general it needs only

$$
\text{all labels outside }J\cup K\text{ form the singleton }\{X\}.
$$

Neither a five-label universe nor a bound of two on palette size is required. The example makes the bookkeeping visible; it is not a claim that these impossible data arise from an actual colouring.

## How the geometry supplies disjoint palettes

Assume a measurable colouring satisfying the weak unit-distance condition: almost every unit pair, with respect to position times direction, has distinct labels. The source theorem `palette_neighbor_disjoint` in [FiveSupport.lean](../Main/ResearchSnapshot/local/work/encoding-integration/full-original/OAI/Geometry/PlaneColoring/FiveSupport.lean) says that palettes at two fixed unit-separated centres are disjoint for almost every **common** angular parameter.

The picture behind the theorem is that translating both centres by the same unit vector preserves their distance one. Passing from sampled labels to limiting palettes is nontrivial: the proof uses smooth palette transport, with the parallel-direction degeneracy discarded as an angular null set. One cannot justify the palette assertion merely by drawing three coloured vertices.

Apply the theorem to the triangle's three edges. There are only three exceptional angular sets to remove. Their union is null, so the three disjointness statements hold simultaneously almost everywhere. The centres and their connecting directions are fixed **before** choosing $t$; we are not intersecting uncountably many full-measure sets.

## Where the remaining two hypotheses come from

A `RealState hc x A J` means that $A$ is a measurable set of real angles and, for almost every $t\in A$, every label in $J$ belongs to the palette at $x$. It asserts inclusion, not equality. We require $A$ to have positive measure, so removing finitely many null exceptions still leaves an angle to use.

At the other two centres we require actual traces that vanish on every coordinate in $K$. A trace is a weak limit of colour-indicator samples around circles approaching the specified centre and radius one. Its coordinates are nonnegative and sum to one almost everywhere. If all $K$ coordinates vanish, some coordinate outside $K$ must be positive almost everywhere; positivity of a trace coordinate puts that label in the palette. Consequently the palette is not contained in $K$.

This is exactly `avoiding_trace_palette` in [BoundaryTrace.lean](../Main/ResearchSnapshot/local/work/encoding-integration/full-original/OAI/Geometry/PlaneColoring/BoundaryTrace.lean). Notice the careful conclusion: one avoiding trace does not make the *whole palette* disjoint from $K$, because other traces can contribute labels.

Pull the angular full-measure statements back to the real line, intersect them with the positive-measure state $A$, and choose one surviving $t$. At that angle all the finite-set hypotheses above hold. The contradiction is now unavoidable.

## From supported angles to the two traces

The fixed-state theorem begins with another represented state $B$ at $x$, this time containing $K$. Take angles $b,d$ in the support of the restricted measure $\mathrm{volume}|_B$ and set

$$
y=x+e^{ib},\qquad z=x+e^{id}.
$$

Support means every neighbourhood has positive $B$-measure; ordinary closure would be insufficient. The source `state_support_avoiding_trace` constructs $K$-avoiding traces at both centres by choosing good nearby angles and taking compact weak limits. If the chord between $e^{ib}$ and $e^{id}$ had length one, these centres would form our equilateral triangle and contradict the preceding argument. This proves `fixed_state_no_unit_three_centres` in [FixedStateThreeCentres.lean](../Main/ResearchSnapshot/local/outputs/three-centre/FixedStateThreeCentres.lean), with the original fixed-state statement unchanged.

The moving-centre extension stores this geometric information in $Z_K$, the set of centres admitting a $K$-avoiding trace. The declaration `isClosed_avoidingTraceCentre` proves $Z_K$ closed using trace compactness and the closed trace relation. Zero coordinates survive weak convergence by testing against the limiting coordinate itself; no unjustified strong continuity is needed. Thus supported points from converging centres stay in $Z_K$ at the limit. A positive $J$-state **at the limiting centre** supplies the triangle contradiction there.

This handles `four_support_sequence_no_unit` with its existing limit-centre hypotheses. The fixed replacement also handles [Interfaces.lean](../Main/ResearchSnapshot/local/work/encoding-integration/full-original/OAI/Geometry/PlaneColoring/Interfaces.lean), `interfaceStateSupport_no_unit`, without adding a `FourCenter` hypothesis that this consumer lacks.

**Try it:** if two labels remain outside $J\cup K$, which line fails? The two neighbours can choose different remaining labels. Our one-label forcing argument no longer contradicts disjointness.

The [validation log](../Main/ResearchSnapshot/local/outputs/three-centre/MOVING-VALIDATION.txt) records separate Lean passes, matching statements and binder flags, standard axioms, and excluded-dependency checks. Historical source headers still say “uncompiled as delivered”; the later log supersedes that status. Full integration remains in progress in the inspected snapshot. This explanation does not claim a completed integrated rebuild or a new global colouring theorem.
