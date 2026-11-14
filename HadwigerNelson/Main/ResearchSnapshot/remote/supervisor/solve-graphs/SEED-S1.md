# Proposed seed S1: the √3-translated double spindle (not run; prepared only)

## Why this shape, in one paragraph
By Theorem B (`GLUING.md`) a palette excluder for a non-adjacent pair `p,q` lies in
`N(p) ∩ N(q)`, the intersection of two unit circles, so it has **at most 2 vertices**. At `k = 4`,
forcing `c(p) = c(q)` needs the palette to have size `k − 3 = 1`, i.e. **three** excluded colours.
Two of them can come from a shared unit edge (the diamond, palette `k−2 = 2`). **The third cannot
come from a common neighbour.** So a `GADGET_4` candidate must obtain an extra exclusion through a
channel that is *not* a common neighbourhood. The only unexplored channel with exact coordinates in
hand is a **cross-unit edge between two rigidly related copies** — precisely the union the
clique-sum theorem does *not* cover. That is what S1 isolates.

## Exact specification
**Base object.** `M` = Moser spindle, 7 vertices, 11 edges, `chi = 4`, built by
`udg/build.py::moser()` in the field `Q(√3, √11)` with basis `{1, √3, √11, √33}`: hub `K = (0,0)`,
tips `C1`, `C2` at unit distance, and two diamonds `K–C1`, `K–C2` with exact apexes.
Every construction step asserts `|apex − tip|² = 1` exactly.

**Transform.** `τ = (3/2, √3/2)`, exact in the field, of length
`|τ|² = 9/4 + 3/4 = 3`, i.e. **`|τ| = √3`**. Applying `V(M) + τ`.

`√3` is chosen deliberately, not for convenience: `√3` is the diamond's characteristic tip
separation (`Theorem C`), so a `√3` translate places the image's tip structure where it can form
**new diamonds with the originals**. A generic translate would produce a disjoint union with only
incidental cross edges; a `√3` translate targets the one configuration that already carries palette
information.

The transform is an exact isometry of `Q(√3, √11)`: translation by a field vector preserves the
field, and the field is closed under multiplication by `√3`
(`√3·{1,√3,√11,√33} = {√3, 3, √33, 3√11}`, still in the basis). So no coordinate is ever a float
and no closure is required beyond translation.

**Point set.** `P = V(M) ∪ (V(M) + τ)`.

**Deduplication.** Merge any two points whose coordinates are **exactly equal** as field vectors
(both components `eq` in `udg.exact.Field`). Record the number of coincidences. Any coincidence makes
the overlap a clique; the script reports the overlap size so the interface is known rather than
assumed.

**All-induced-edge construction (the only edge rule).** `uv` is an edge of `S1` iff
`|u − v|² = 1` holds as an exact field identity. No other rule, no exception, no distance threshold.
Within-copy edges are reproduced automatically by this rule; **cross edges are whatever geometry
supplies**, which is the whole point.

**Finite bounds.** `|P| ≤ 14`. Candidate pairs `≤ C(14,2) = 91`, each decided by one exact field
comparison. Whole validation is microseconds; the only nontrivial cost is CDCL.

## Deterministic first test (this is the whole of the next block's computation)
Run in this fixed order and **stop at the first failure**:
1. Build `S1`; assert every edge is exactly unit and every non-edge is not; assert all points distinct
   after dedup; report `|P|`, `|E|`, coincidence count, **cross-edge count**, and the clique number
   (must be 3 — a `K_4` would indicate an arithmetic bug, since four equidistant plane points cannot
   exist).
2. Report whether Theorem A's hypothesis holds: it requires **zero** cross edges. Record the count
   either way. If the count is 0 the seed is a disjoint/clique-sum union and therefore uninteresting
   *by our own theorem* — recorded as a measured negative for this `τ`, not silently replaced.
3. Decide **5-colourability** of `S1` by CDCL.
   * **SAT** → verify the colouring against **all** edges. Only a verified 5-colouring licenses any
     further 5-forcing interpretation. Report the colouring.
   * **UNSAT** → **stop**. Save the CNF; attempt a DRAT proof and check it with `tools/drat-trim`.
     Report as a **separate candidate** and label it *solver-reported only* until `drat-trim` says
     `s VERIFIED`. A 5-UNSAT here would mean `chi >= 6` from 14 vertices, which is
     extraordinarily unlikely; the script treats it as a red flag to be checked, not a result.
4. Only if step 3 is SAT and verified: measure the palette structure of the `√3` pair carried over
   from the shared `C1, C2`... and report **without** any forcing claim. Any forced-equality claim
   requires its own pre-registration and a separating-witness certificate as in
   `CERTIFICATE-k5-no-forcing.md`.

## Honest expectation and its basis
`S1` has 13–14 vertices against the 553 at which `chi = 5` first appears in published work, and
Theorem B still caps the common-neighbour channel at 2 excluded colours, so **at `k = 5` this seed is
expected to be easily 5-colourable with no forced pair** — the same outcome as Heule553, for the same
structural reason. Its value is not the expected outcome; it is that it isolates the one channel
Theorem B leaves open (cross-unit edges around a `√3` pair) at a size where every step is exactly
checkable. If it returns 5-colourable with no forcing, that is a *measured* statement about this
channel at this size, and the next seed should move to `k = 4` on a genuinely 4-colourable graph —
the `GADGET_4` question — rather than to a larger `k = 5` object.

## Explicitly not claimed
* Not a new unit-distance graph result, no `chi(R^2)` claim, no `chi >= 6` claim.
* No claim that `S1` will force anything, and no claim that it cannot.
* The certificate on Heule553 says nothing about this seed.
