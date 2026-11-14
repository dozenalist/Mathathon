import Mathlib

namespace OAI

noncomputable section

namespace EuclideanFiveColor

/-- **Connected unit-free sets have diameter at most one.**

If `C` is preconnected and contains no pair of points at distance exactly one, then every
distance inside `C` is at most one.  This is the whole geometric content of the paper's
connected-set exclusion for `Delta(K_j)` (Proposition 7.1): only connectedness and continuity
of the distance are used, not planarity, compactness or any topology of the plane.

Sharp: the open ball of radius `1/2` is connected and unit-free, and its diameter is exactly `1`
(not attained). -/

If `C` is preconnected and no point of `C` is at distance exactly one from `z`, then `C` cannot
have points both strictly inside and strictly outside the unit circle about `z`. Equivalently: a
set that is connected, lies in one colour class, and is hit by the circle of radius one at no
point, cannot straddle that circle.  This is the a.e. exclusion the paper applies with
`C = K_j` and `z` a point carrying an endpoint label of edge `j`. -/
proper colouring is unit-free, hence has diameter at most one. -/

end EuclideanFiveColor
end
end OAI
