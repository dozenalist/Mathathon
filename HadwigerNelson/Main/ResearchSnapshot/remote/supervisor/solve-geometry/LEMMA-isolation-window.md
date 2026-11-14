# The isolation window for cyclic centres, and what lattices do and do not refute

**Convention (fixed this block).** `B(x,r)` is the **open** ball. The *isolation radius* of `x` is
`r*(x) = sup{r : L ∩ B(x,r) = {x}}`; for a lattice `aZ²` this is `a` (the nearest neighbours sit at
distance exactly `a`, hence are excluded from the open ball of radius `a`). It is **not** the
packing radius `a/2`, which is the radius of pairwise disjoint balls. The previous version of this
file used `a/2` and therefore mis-stated which thresholds the examples refute.

`c` is a weak measurable 6-colouring (paper Def. 1.2), `L = {x : Gamma_x contains a cycle}` —
closed and `1`-dense (every closed disk of radius `> 1` meets `L`).

## Proposition 1 (no wide isolated cyclic centre) [C+P+A]

If `x in L` and `L ∩ B(x,rho) = {x}` then `rho <= 2`.

*Proof.* Suppose `rho > 2`. Take `r` with `1 < r < rho/2` and `eps > 0` with `2r + eps < rho`, and a
unit vector `u`. The closed disk `D` of radius `r` about `c_0 = x + (r+eps)u` satisfies
`D ⊆ B(x, 2r+eps) ⊆ B(x,rho)`, so `L ∩ D ⊆ {x}`; and `x ∉ D` since `|c_0 - x| = r + eps > r`. So
`L ∩ D = ∅` with `r > 1`, contradicting the density theorem (`m12` Thm D). `square`

The bound is not attained and is not needed: it rules out *large* gaps only. It is consistent with
every example below (`r* = 1`, `r* = 6/5`, `r* = 3/2`) and with `m3`'s `k >= 7` accumulation, whose
isolation radii tend to `0`.

## Proposition 2 (sharp threshold, and the two lattice refutations) [A]+[P]

**Sharp form.** `(ISO)(r)`: `exists x in L, L ∩ B(x,r) = {x}`. If `r > 1` then `(W)` holds, hence
Prop. 7.1 at `k = 6` — take the **disk** `B̄(x,rho')`, `1 < rho' < r`, as the region: its inradius is
its radius, and `1` is the component-cover mesh (`m12` Lem. 5.1). No square is needed, so the
threshold is `1`, not `sqrt2`, and by Prop. 1 the usable window is `1 < r <= 2`.

**What the lattices refute — exactly.**
* `L = Z²`: closed, locally finite, covering radius `1/sqrt2 = 0.7071 <= 1` (**1-dense**),
  isolation radius exactly `1`. So **`(LF)` + 1-density does not imply `(ISO)(r)` for any `r > 1`.**
* `L = (6/5)Z²`: same properties, isolation radius exactly `6/5 = 1.2`, covering radius
  `0.8486 <= 1`. It does **not** refute `(ISO)(r)` for `r > 1` (it satisfies it); it refutes
  `(ISO)(r)` for `r > 6/5`, in particular for `r > sqrt2 = 1.4142` — which is exactly the hypothesis
  printed in `sprint/k6/WEAKEST.md`, so that formulation is false as an implication from `(LF)`.
* Neither lattice refutes anything about colourings: whether any 6-colouring has such an `L` is the
  open problem. What they refute is the *implication between hypotheses*, which is what the
  dependency map needs.

**And what `(W)` is not.** `L = {0} ∪ ⋃_{k>=1} S(0, 3k/2)` is closed, `0.75`-dense, has
`|L ∩ B(0,1.2)| = 1` (so `(W)` holds with `R = 1.2`) and `|L ∩ B(y,2)| = infinity` for every `y`
(every radius-2 ball cuts some circle in an arc). So `(W)` does not imply `(W2)`, the radius-2 form;
`(W2)` is strictly stronger and is not what §7 needs. [A]

All numbers in this file: `checks/constants.py` sections [3], [6], [7].

## What is not claimed

Nothing here produces or excludes a 6-colouring, and neither proposition is machine-checked; both
use m12's density theorem, a paper-level argument I did not re-verify, and the arithmetic only.
