# Understanding the supplied five-colour obstruction

**Reading guide, 14 November 2026.** The supplied proof is OpenAI's *The Euclidean plane is not five-colorable*, dated 23 September 2026. Its result is that every five-colouring of the entire plane has two equally coloured points exactly one unit apart, **even if the colour classes are not measurable**. Together with the seven-colouring construction, its conclusion is $6\leq\chi(\mathbb R^2)\leq7$. It does not decide between six and seven. This document explains the supplied result; the Mathathon team's subsequent simplifications and local theorems are separate contributions.

The [manuscript](../Main/ResearchSnapshot/remote/attachments/here-are-three-files-ni5n/paper.pdf), Theorems 1.1–1.4, states this scope explicitly. The [source bundle](../Main/ResearchSnapshot/remote/attachments/here-are-three-files-ni5n/hadwiger-nelson-lean-review-bundle.md) identifies OpenAI commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, Lean 4.34.1, and mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. The public pinned source is [openai/math](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). A source map with declaration names appears in [SourceMap.md](SourceMap.md).

## The question in one picture

Imagine that every point of an infinite sheet receives one of five labels. Whenever two points are exactly distance one apart, their labels must differ. This is a graph-colouring problem with infinitely many vertices: points are vertices and unit-distance pairs are edges. Crossing edges in a drawing are allowed. The problem is about distances, not colouring the faces of a planar map.

To disprove five-colourability, assume such a colouring exists and derive a contradiction. The difficulty is that its colour classes could be extremely irregular. We cannot begin by drawing smooth boundaries between coloured regions, or even by assigning an ordinary area to each class.

The supplied proof therefore has two major bridges:

1. Replace an unrestricted proper colouring by a measurable object that still forbids almost all monochromatic unit pairs.
2. Extract enough geometric structure from that weak measurable object to force a contradiction with only five labels.

The first bridge works for every finite number of colours. The second uses five in essential ways.

## What “weak measurable” means

Write $A_i$ for colour class $i$, and let $u$ range over the unit circle with normalized arc-length measure. A weak measurable colouring requires that, for every bounded disk $B$,

$$
\sum_i\int_B\int_{S^1}1_{A_i}(x)1_{A_i}(x+u)\,d\sigma(u)\,dx=0.
$$

The integrand is nonnegative. Thus a randomly positioned, randomly directed unit segment almost surely has different endpoint colours. Exceptional unit pairs are allowed. Changing the colouring on a plane-null set does not change this condition. To see why, cover the exceptional set by a Borel null set. For each fixed direction, translating that set preserves its zero area; integrating these zero-measure slices over directions shows that the parameter pairs hitting it at either endpoint have product measure zero.

This is weaker than requiring every unit pair to have distinct colours. It is also not merely a statement about almost every pair of plane points: the second endpoint is constrained to be exactly one unit from the first. The relevant measure is position times direction. The manuscript uses Lebesgue-measurable classes and completed measures; the formal proof can choose Borel representatives. These are regularity properties of the *replacement*, not assumptions on the original proper colouring. See Definition 1.2 and [Coloring.lean](../Main/ResearchSnapshot/local/work/encoding-integration/full-original/OAI/Geometry/PlaneColoring/Coloring.lean), `WeakColoring`.

## Bridge one: extracting measurable structure

First restrict the assumed proper colouring to the countable algebraic plane. Average its translates and algebraic rotations to produce a symmetry-invariant probability law on labelings. Randomization gives symmetry, but does not by itself give a measurable plane colouring.

The next step is the deep analytic part. Translation operators acting on square-integrable random variables have a spectral description by characters: functions that turn addition into multiplication by complex numbers of modulus one. Ordinary characters have the familiar form $z\mapsto\exp(i\xi\cdot z)$. The discrete algebraic plane also admits less regular characters.

The manuscript's Theorem 2.3 proves a rigidity result: a rotation-invariant probability law concentrated away from ordinary characters must be Haar probability. Sections 2–3 establish this using compact factors, conditional averaging, and Fourier identities. Consequently the irregular remainder has zero correlation under every nonzero algebraic translation.

Projecting each colour indicator onto the ordinary-character part preserves its nonnegativity and preserves the sum of all coordinates as one, because this projection is conditional expectation. Removing the irregular remainder preserves the zero correlations at unit translations. The remaining translation action extends continuously to the real plane and yields jointly measurable fields.

For a suitable sample, select the least label whose field coordinate is positive wherever the coordinates sum to one. Assign a fixed default label on the remaining plane-null set, so the colouring is defined everywhere. Two selected equal labels would make the corresponding product positive, which the zero-correlation statement forbids almost everywhere. Changing the null set does not affect weakness. This produces the required weak measurable colouring. The explanation here identifies what each analytic ingredient accomplishes; it is not an independent reconstruction of the compact-factor argument. See manuscript Sections 2–4, especially Theorem 2.3 and Proposition 4.2.

## A worked lemma: density turns “almost always” into exact exclusion

A density-one point of $A_i$ is a point around which the fraction of a sufficiently small disk occupied by $A_i$ tends to one. Manuscript Lemma 4.3 says two density-one points of the same class cannot be exactly one unit apart.

Suppose otherwise that $y=x+u$, with both points having density one in $A_i$. Perturb $x$ uniformly inside a disk of radius $h$, and independently perturb $u$ inside a small arc with $|u'-u|<h$. The new endpoint $x'+u'$ remains within $2h$ of $y$.

The chance that $x'$ misses $A_i$ tends to zero. The distribution of $x'+u'$ has density at most $1/(\pi h^2)$, so its chance of missing $A_i$ is bounded by the area missing from the radius-$2h$ disk divided by $\pi h^2$, which also tends to zero. Hence both endpoints lie in $A_i$ with positive probability. Their distance is still exactly one. The sampling law is the normalized restriction of position-times-direction measure to a disk times a positive-measure arc, so positive probability here means a positive-measure set of forbidden unit pairs. This contradicts the weak condition.

Almost every plane point is a density-one point of its class. Any fixed finite configuration can be translated entirely into this full-measure set, since only finitely many null sets must be avoided. The lemma then properly colours that finite graph. Graph compactness assembles finite satisfiability into a proper colouring of the whole plane. This proves the converse direction of Theorem 1.3; the final five-colour contradiction only needs the forward direction.

## Bridge two: manufacture interfaces instead of assuming them

At a fixed centre, inspect colour proportions around nearby circles whose radii approach one. Weak limits of these angular samples define a **palette**: the labels that can persist at a direction. This is a measure-based limiting object, not simply the colour of the point on the circle. Section 5 proves that almost every such palette has at most two labels in the five-colour setting.

Section 6 organizes substantial transitions into a graph on the colour labels. The centres where this graph contains a cycle form a closed, locally finite set. Circle-averaging estimates control the irregularity. In Section 7, smoothed colour indicators become continuous maps into the complete graph on five labels, apart from controlled holes. Away from cyclic centres the relevant graph is a forest, allowing holes to be filled. A planar topological obstruction forces a nontrivial loop near a cyclic centre.

A simple cycle in that loop supplies compact connected sets $K_j$ sharing a centre $x$, each carrying a pair of forbidden labels. Their exclusion region is

$$
\Delta(K)=\{z:\min_{q\in K}|z-q|<1<\max_{q\in K}|z-q|\}.
$$

Both labels associated with $K_j$ are absent almost everywhere in $\Delta(K_j)$. This conclusion requires the analytic interface construction; connectedness alone does not establish a two-label prohibition. See manuscript Section 7 and [AngularBoundary.lean](../Main/ResearchSnapshot/local/work/encoding-integration/full-original/OAI/Geometry/PlaneColoring/AngularBoundary.lean), `Straddle` and the support-exclusion lemmas.

For geometric intuition, take $K$ to be a short segment. A point in $\Delta(K)$ is less than one from some part of the segment and more than one from another part. Distance varies continuously along the segment, so somewhere it equals one. More generally, the continuous image of any connected $K$ is an interval, giving the same contact conclusion without assuming a path inside $K$.

For an accurate drawing, the minimum distance is to the **whole segment**, computed by perpendicular projection with endpoint clamping. The maximum occurs at an endpoint. The region is the open radius-one capsule about the segment, restricted to points more than one from at least one endpoint. Points strictly inside one endpoint disk and strictly outside the other closed disk give a sufficient subset. They omit contacts created by the segment interior; using a literal symmetric difference also mishandles equality at the disk boundary. This is a useful visualization of why the word “straddle” captures a robust unit-distance contact.

## Why the extracted cycle cannot exist

A simple cycle on five labels has length three, four, or five. The manuscript's Section 8 eliminates all three.

For length five, approaching directions in the continua restrict allowed labels on the inner and outer sides of the unit circle. Six directions spaced by $60^\circ$ must obey incompatible finite transition rules. Length four forces antipodal direction pairs and a contradictory parity rule. Length three forces alternating sectors for the two labels outside the cycle. The resulting open region uses only the three cycle labels almost everywhere; a certified placement of the seven-vertex Moser obstruction inside that region contradicts three-colourability, with exceptional null sets handled in the proof.

The Lean assembly packages this geometry through continuous full approximations and a large-connected-region obstruction, rather than literally following the manuscript's final narrative line by line. Its root [Five.lean](../Main/ResearchSnapshot/local/work/encoding-integration/full-original/OAI/Geometry/PlaneColoring/Five.lean) states `no_measurable_weak_five_coloring` and then `no_proper_five_coloring`, whose hypothesis contains no measurability requirement.

## What our team adds, and what remains open

Our simplification work replaces part of the strict-state machinery by three-centre arguments. The latest inspected [research status](../Main/ResearchSnapshot/local/outputs/RESEARCH-STATUS.txt), saved at 10:25 Pacific on 14 November, reports separate fixed- and moving-centre passes but an ongoing integrated rebuild. It does not yet justify declaring the full replacement integrated.

The team's local **CC60** theorem says that a finite family of actual approaching continua at one common centre, with signed approach directions in a closed cone of width at most $60^\circ$, cannot jointly exclude all but two labels. It assumes the actual spatial-support exclusions and a weak measurable colouring. It is generic in the number of colours and includes equality at $60^\circ$. The [cone packet](../Main/ResearchSnapshot/local/outputs/cone/REPORT.txt) records successful Lean checks and standard-only axiom audits; its [independent referee report](../Main/ResearchSnapshot/local/outputs/ASTRA-CONE-REFEREE.txt) explains the geometric hypotheses.

CC60 is a local obstruction, not an unrestricted six-colour impossibility theorem. Finite palette searches likewise test stated relaxations, not all plane colourings. The team's work has not improved the supplied $6\leq\chi\leq7$ bound or constructed a global six-colouring. This walkthrough checks source statements and selected arguments; it does not independently reverify the entire supplied proof, its full Lean closure, or novelty priority of the local results.
