# Lemma D (self-avoidance): the recorded proof is invalid, the statement is true

Claim under audit: let c be a weak measurable k-colouring (Definition 1.2, a.e. proper) and x a
density-one point of its own colour class A_i, c(x) = i. Then i notin P_x(e) for a.e. unit e.

Verdict: statement TRUE, the proof recorded in sprint/k6/REPORT.md section 5 is INVALID, and a
valid proof exists that uses (5.2) instead of Lemma 5.2(2).

## The gap in the recorded proof
The recorded proof takes e_0 a density point of D = {e : i in P_x(e)}, invokes Lemma 5.2(2)
(zero A_i-density at x + e_0 + v for every unit v nonparallel to e_0), sets v = -e_0 + delta so
that the point is x + delta with |delta - e_0| = 1, and concludes that x + delta is a
density-one point of A_i "for conull many delta on that circle, by Fubini". That step has no
content: {delta : |delta - e_0| = 1} is the circle of radius one about x + e_0, not about x, and
nothing in the paper gives A_i positive 1-dimensional measure on it. Worse, exactly two points
of that circle lie at distance 1 from x, because

  {v in S : |e_0 + v| = 1} = {-e_0, v_120}   (two points, angles 120 and 240 degrees),

and the one that is x is v = -e_0, the direction Lemma 5.2(2) excludes. Verified in
checks/sector_lemma.py step (5).

## The repair (uses (5.2) and the sector Jacobian)
Suppose i in P_x(e) for a.e. e in D with |D| = d > 0. Lemma 5.2 assertion 1, equation (5.2), at
the fixed centre x gives c(x+e+v) notin P_x(e) union P_x(v) for a.e. (e,v) in S x S; for e in D
a.e. this reads c(x+e+v) != i for a.e. v. Let E_h = {x+e+v : e in D, |e+v| <= h} inside B(x,h).
For |z| <= h < 1 the equation |z - e| = 1 has exactly the two solutions
e = (|z|/2) zhat +- sqrt(1-|z|^2/4) i zhat, tending to +- i zhat as z -> 0. So, to leading order,
z in E_h iff i zhat or -i zhat lies in D, i.e. E_h is the preimage of the angular set
iD union -iD, and

  lim_{h->0} |E_h| / (pi h^2) = |iD union -iD| / (2 pi) >= d / (2 pi) > 0.

Because c != i a.e. on E_h (the (5.2)-exceptional set is product-null and C^1 images of null sets
are null),

  |A_i cap B(x,h)| / (pi h^2) <= 1 - |iD union -iD|/(2 pi) + o(1) <= 1 - d/(2 pi) + o(1),

contradicting density one at x. The degeneracy of (e,v) -> e+v at v = -e is exactly compensated:
the Jacobian |sin(arg v - arg e)| vanishes linearly in |e+v|, so the killed region is a genuine
sector of every B(x,h), not an o(h^2) sliver.

Quantitative form: the deficit is |iD union -iD|/(2 pi) >= |D|/(2 pi); if |D| >= pi the whole
disc is killed and the density is 0.

## What this changes
The record's frontier (self-avoidance as the first colouring-level constraint that removes the
countermodels), constraint 1 of the orbit enumeration (510 words at ell = 6) and m4's
singleton-class reduction are all SUPPORTED, but the justification must cite this proof and not
Lemma 5.2(2). The audit therefore does not have to withdraw the numbers that depend on them.

Machine-checked part: python3 supervisor/solve-synthesis/checks/sector_lemma.py (rc 0) checks
(1) the solution formula, (3) |iD union -iD| >= |D| for four arcs, (4) the fraction of B(x,h)
killed for h = 1e-2 and 3e-3 (measured 0.1902 against predicted 0.1910 for |D| = 0.6), and
(5) the two-point intersection. Statement and proof are paper-level; the arithmetic is
machine-checked.
