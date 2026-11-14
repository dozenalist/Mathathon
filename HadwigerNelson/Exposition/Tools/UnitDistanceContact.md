# How connectedness forces a unit-distance contact

Fix a short horizontal segment $K=[-0.6,0.6]\times\{0\}$. Place a point $z$ somewhere nearby and draw the circle of radius one around it. When must that circle meet the segment?

The useful condition is not “both endpoints look close.” It is that some part of the segment is nearer than one and another part is farther than one:

$$
\min_{q\in K}|z-q|<1<\max_{q\in K}|z-q|.
$$

Distance changes continuously as we move along the segment. It cannot go from below one to above one without taking the value one. This simple observation survives a much more irregular connected set: the continuous image of a connected set in the real line is an interval. No path or smooth boundary is required. Compactness ensures the displayed minimum and maximum exist.

The collection of such points $z$ is the **strict straddle region** $\Delta(K)$. Strict inequalities make it open: a small move of $z$ does not destroy the two inequalities. This robustness is useful when passing from approximate interfaces to limiting geometric information.

## Explore the picture

Open [the interactive model](unit-distance-contact.html) after downloading the repository, or use its inline version in the exposition chat. The sliders move $z$; the shaded region is $\Delta(K)$; the highlighted points are the unit-circle contacts. The numerical display is rounded, and contact calculations use floating-point tolerance. The mathematical argument above is exact.

The four examples are deliberately different:

| Example | Point $z$ | Minimum distance | Maximum distance | What to notice |
| --- | --- | --- | --- | --- |
| Straddles 1 | $(0.65,0.70)$ | $\sqrt{0.4925}$ | $\sqrt{2.0525}$ | One contact lies on the segment |
| All closer | $(0,0.20)$ | $0.20$ | $\sqrt{0.40}$ | The whole segment lies inside the unit circle |
| All farther | $(0,1.30)$ | $1.30$ | $\sqrt{2.05}$ | The whole segment lies outside |
| Middle matters | $(0,0.90)$ | $0.90$ | $\sqrt{1.17}$ | Both endpoints are farther than one, but two interior contacts exist |

In the last example, the contact coordinates are $(\pm\sqrt{0.19},0)$. Looking only at the endpoint disks would miss this case. The true minimum is the distance to the nearest point of the whole segment, found by perpendicular projection and clamping to an endpoint when necessary. The maximum is the farther endpoint distance. Geometrically the region is the radius-one capsule around the segment with the intersection of the endpoint disks removed; its boundary is excluded.

## What this contributes to the colouring proof

If $K$ were monochromatic in a proper colouring, a point in $\Delta(K)$ could not have that same colour: it has a neighbour of that colour exactly one unit away.

The supplied proof needs a stronger, subtler statement. It constructs actual connected interfaces carrying **two excluded labels**, and proves that both labels are absent almost everywhere in their straddle regions. Connectedness supplies the geometric contact; the analytic construction supplies the two-label exclusion. A random segment with two labels written beside it does not establish that hypothesis.

This is the connection to the team's CC60 theorem: several such verified exclusion regions can overlap. The geometry of their approach directions restricts how few colours may survive the overlap. Understanding one straddle region makes that larger argument tangible.

Read the [proof walkthrough](../ProofWalkthrough.md#bridge-two-manufacture-interfaces-instead-of-assuming-them) for where the interfaces come from, and the [source map](../SourceMap.md) for `Straddle`, `ApproachingContinuum`, and the exact support-exclusion hypotheses.

## Reproduce the checks

The [fragment source](unit-distance-contact.fragment.html) is the editable model; the [standalone version](unit-distance-contact.html) includes its display wrapper. The model uses no external data requests. Run `node HadwigerNelson/Exposition/Tools/verify-contact.cjs` from the repository root for five exact-formula examples and a 10,201-point numerical consistency check, including the interior-contact and boundary cases. The script also supports optional Playwright/browser paths for interaction and layout checks; see its header. These checks verify the teaching model, not the full colouring proof.
