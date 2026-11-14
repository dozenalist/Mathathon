# Independent audit of `supervisor/solve-geometry/AMPLIFIER.md`

Frozen at `audit-amplifier/AMPLIFIER.frozen.md`, sha256
`492bcae49c35dc268a7e87ce546da05ef394e261263a59631d4925b0c89c689a` (byte-identical to the file read).
Analysis block: no Lean, no solver. One exact-arithmetic check
(`audit-amplifier/chain_k2_n3.py`, field `Q(sqrt5, sqrt7)`, `Fraction` coefficients, ~25 ms) is used
only to verify distances and to test a new instance; it performs no search. Author labels `[P]`/`[C]`
are not relied on: everything endorsed below is re-derived here.

## 0. Verdict

**The core claim survives, with one false lemma.** The amplifier construction is correct as a route
from a forced-equal pair to a finite non-`k`-colourable unit-distance graph. But:

* **Lemma 1 as stated is false**: the chain is *not* monochromatic; only the *anchors* are forced
  equal. The theorem's proof only needs the anchor form, so the lower bound is intact.
* **A fourth accident class is missing** from §5: accidental unit *distances* between different copies
  *of the same chain*.
* The `k = 3` validation reproduces the Moser spindle exactly, but it runs at `n* = 1`, so it exercises
  **none** of §2's chaining. §7's remark that it is "the strongest available check of the formulas in
  §2-§3" overstates for §2.
* One **overclaim** in §4's consequence paragraph: "a negative answer to the forcing-pair question is
  exactly as hard as `chi(R^2) <= 6`". Absence of a forcing pair is *necessary* for `chi(R^2) <= 6`, not
  sufficient.

Everything else audited — `D > 1/2`, the vertex/edge counts (with one caveat), the field extension, and
the `(H4)` upper-bound argument — is sound, and I confirm `(H4)` on a new instance below.

No forcing pair is asserted to exist anywhere, and I assert none. The construction, when its
hypotheses are met, yields a **finite** unit-distance graph, hence a genuine lower bound via
`chi(R^2) >= chi(F)`; it is not a structural statement about the plane.

## 1. Lemma 1 is false as stated — corrected statement and counterexample

The file's §0 says "the whole chain is monochromatic in every `k`-colouring" and §2's Lemma 1 says
every point of the chain has the same colour `α`. Both are false. The proof given establishes only
that consecutive *anchors* agree.

**Lemma 1' (corrected).** Let `c` be a proper `k`-colouring of the induced unit-distance graph on
`C_n`. Then for each `i`, `c(p + i d u) = c(q + i d u)`; consequently

    c(p) = c(p + d u) = c(p + 2 d u) = ... = c(p + n d u).

Nothing is asserted about any other point of `C_n`.

*Proof.* `P_i = P + i d u` is an isometry, so `c|P_i` is a proper `k`-colouring of the induced graph on
`P_i`, which is isomorphic to `G` under `p |-> p + i d u`, `q |-> q + i d u`. Apply `(H2)`. Then
`q + i d u = p + (i + 1) d u` by definition of `u`. ∎

**Counterexample to the original wording.** Explicit, at `k = 2`, with the chaining switched on
(`audit-amplifier/chain_k2_n3.py`). Gadget
`G = {p = (0,0), r = (1/8, 3√7/8), q = (1/4, 0)}` — a path `p - r - q`, `V = 3`, `E = 2`. It is
bipartite, so any proper 2-colouring puts `p` and `q` in one part and `r` in the other; hence `(H2)`
holds at `k = 2` with `d = |p - q| = 1/4`. Here `n* = min{n : n/4 > 1/2} = 3`, `D = 3/4`.

`C_3` has the `7` points `p_0..p_3` on the `x`-axis and `r_0..r_2` at height `3√7/8`, its six unit
edges are exactly the six within-copy edges, and it is a path
`p_0 - r_0 - p_1 - r_1 - p_2 - r_2 - p_3`. So the two 2-colourings give all `p_i` one colour and all
`r_j` the other: `c(p_0) = c(p_3)` as Lemma 1' says, but `c(r_0) != c(p_0)`. The chain is **not**
monochromatic.

The same failure occurs in the file's own `k = 3` example: in every proper 3-colouring of the diamond
the vertex `B = (1,0)` takes a colour different from `α = c(A) = c(T2)`. So the error is visible at
`n = 1` too; it just is not used there.

**Does this break the theorem?** No. §4's lower-bound proof says "Lemma 1 makes `c` equal `α` on all
its points, so both ends ... have colour `α`" — only the ends are used. With Lemma 1' the same
conclusion follows. The defect is in the statement of a lemma, not in the theorem.

## 2. Accident classes: a fourth one is missing

§5 lists (1) coincidences inside the chain, (2) coincidences between the two chains, (3) accidental
unit distances between the two chains. **Missing: (4) accidental unit distances between distinct
copies of the same chain.** These are exactly the pairs `x + i d u`, `y + j d u` with `i != j`,
`x, y ∈ P`, at distance `1`; §5.1's coincidence test only covers distance `0`.

Why it is not harmless for everything:

* lower bound: harmless (extra edges only add constraints) — see §3 below, where I make this explicit;
* the `(H4)` gluing argument of §4: **not** harmless. `(H4)` colours each copy properly, but says
  nothing about cross-copy edges, so a cross-copy unit edge can join two equally-coloured points;
* the edge count `nE`: it is only a lower bound, since cross-copy edges can add more.

In the `k = 2, n = 3` instance above there happen to be **no** such accidents (the six edges are exactly
the six within-copy ones), and likewise no cross-chain accidents (`|E(X)| = 2nE + 1 = 13` exactly). So
the class is unexercised rather than refuted; it must be checked, as §5.3's own principle demands, but
for the chain as well as across chains. *(My own first hand estimate here invented an accident that the
exact computation then refuted; recorded because it is the same trap the file warns about.)*

## 3. Corrected self-contained lower-bound proof (all accidents covered for free)

**Theorem A.** Assume `(H1)`, `(H2)`. Let `n >= 1`, `D = n d`, `u = (q - p)/d`, and define `X` as in §3
of the file (`p = 0`, rotation `R_theta` about `0` with `cos theta = 1 - 1/(2D^2)`). If `D >= 1/2` then
`X` carries no proper `k`-colouring.

*Proof.* Suppose `c` is a proper `k`-colouring of the induced graph on `X`. Since `C_n subset X`,
`c|C_n` is a proper `k`-colouring of the induced graph on `C_n`, so Lemma 1' gives `c(0) = c(D u)`.
Since `R_theta C_n` is an isometric copy of `C_n` and is contained in `X`, the same argument gives
`c(0) = c(D R_theta u)`. Hence `c(D u) = c(D R_theta u)`. But
`|D u - D R_theta u|^2 = 2D^2 (1 - cos theta) = 1`, and both points lie in `X`, so a proper colouring
must separate them. Contradiction. ∎

**No accident hypothesis is needed** for this direction. Coincidences and accidental unit edges, inside
a chain or between the chains, can only add constraints; the argument never uses the counts, never uses
the edge set beyond `C_n subset X` and the final unit edge, and never uses monochromaticity of the whole
chain. This is worth stating explicitly because it means **the lower bound is completely robust to every
accident class**, including the missing one.

**Two corrections to the file's §2/§3 embedded here.**

* *`D > 1/2` is sufficient, not necessary.* At `D = 1/2`, `cos theta = -1`, `theta = pi`, the two far
  ends are `D u` and `-D u` at distance `2D = 1`, and the proof above goes through unchanged. So the
  file's "**Strictness matters**" is a hygiene statement (keeping `0 < theta < pi`), not a logical
  requirement; the file itself half-concedes this ("the condition `D > 1/2` is exactly the solvability
  condition `2D >= 1` ... made strict to keep `0 < theta < pi`"). Theorem A needs only `D >= 1/2`.
* *`D >= 1/2` is sharp.* A chord of length `1` on a circle of radius `D` needs `2D >= 1`; below that no
  `theta` exists. Correct.

## 4. Audits of the remaining items

**`D = 1/2`.** As above: admissible for the lower bound. What actually fails at `theta = pi` is the
*edge count* picture (the two chains are mirror images, so coincidences between them are likely and
`|X| < 2|C_n| - 1`), and possibly `(H4)`. It is a convenience to avoid it, not a necessity.

**Vertex and edge counts.** `|C_n| = nV - (n-1)` needs no coincidence `x - y = m d u` with
`1 <= |m| <= n-1`; §5.1 flags this correctly, but §2 states the count as an equality without the
caveat inline. `nE` is stated in §2 as the number of edges; it is a **lower** bound, since cross-copy
unit edges (class (4)) can add more. §3 handles the corresponding statement for `X` correctly with
`<=`. Minor internal inconsistency, no effect on the lower bound.

**Field extension (§6).** Correct, and confirmed on a new instance. In §4's `(H4)` argument the
palette needs a colour `beta != alpha`, which is why `k + 1 >= 3` appears; for `k >= 2` that is
automatic, and `X` always has the final unit edge so `chi(X) >= 2 = k + 1` when `k = 1`. The phrase
"which needs `k + 1 >= 3`" is therefore right in substance but loose in its reason.

**`(H4)` upper bound (§4).** The gluing is sound *for the idealised graph*: chain 1 uses `(H4)` at
`(alpha, alpha)` on every copy, chain 2 the same except the last copy at `(alpha, beta)` with
`beta != alpha`; all shared anchors are `alpha`, so the gluing is consistent, and the final unit edge
joins `alpha` to `beta`. But it must be re-verified on the **actual** point set: cross-copy edges
(classes (4) and (3)) can join two `alpha`-coloured points. §5.3 states this principle for cross-chain
edges; it must be applied to within-chain edges too. Note `chi(X) >= k + 1` always follows from
Theorem A, so only `chi(X) <= k + 1` is at risk.

**New instance confirming the full theorem, including `(H4)`, at `n = 3`.** For the `k = 2` gadget of
§1: `chi(X) = 3 = k + 1`. `(H4)` at 3 colours holds for a path (`p` and `q` prescribed, `r` gets any
other colour), and the accident check is exact: `|X| = 13 = 2|C_3| - 1` with all points distinct, and
`|E(X)| = 13 = 2nE + 1`, so `X`'s edge set is exactly the `2n` copies' edges plus the final edge, and the
gluing colouring is proper on it. Also `|far_1 - far_2|^2 = 1` exactly, in `Q(sqrt5, sqrt7)`, matching
§6's predicted field: `K = Q(sqrt7)` (from `h = 3 sqrt7 / 8`), `d = 1/4`, `4n^2 d^2 - 1 = 5/4`, so
`K' = K(sqrt5)`. This is the first instance I know of in which the **chaining** is exercised, and it
behaves as the file predicts.

**The `k = 3` validation (§7).** Verified independently and it is correct: `d = sqrt3`, `cos theta = 5/6`,
`sin theta = sqrt11/6`, `K' = Q(sqrt3, sqrt11)`, counts `2*4 - 1 = 7` and `2*5 + 1 = 11` — the Moser
spindle. Good evidence for §3's rotation arithmetic. But `n* = 1`, so it tests none of §2: no chaining,
no coincidence class, no `nV - (n-1)`. Its description as the "strongest available check of the formulas
in §2-§3" is accurate for §3 and empty for §2.

**The `k = 6` consequence and one overclaim.** The main inference is valid: a forced-equal pair in a
6-colourable finite unit-distance graph gives a finite graph that is not 6-colourable, hence of
chromatic number `>= 7`, hence (vertex-minimal subgraph) one of chromatic number exactly `7`, hence
`chi(R^2) >= 7`; with the known `chi(R^2) <= 7` that is `chi(R^2) = 7`. **Overclaim:** "a negative
answer to the forcing-pair question is exactly as hard as `chi(R^2) <= 6`". The valid statement is only
the contrapositive — `chi(R^2) <= 6` implies no such pair exists — so absence of a forcing pair is a
*necessary* condition for six colours, and this construction gives no route from that absence to an
upper bound. "Exactly as hard" is unsupported and should be weakened to "necessary".

**Global vs existence.** Properly handled in the file: §0 and §8 both say no forcing pair is asserted.
I confirm that nothing in the construction produces one, and that `(H2)` — a statement about *all*
proper `k`-colourings — is where the real difficulty lies, not in the geometry.

## 5. Findings ledger

| # | item | grade | verdict |
|---|---|---|---|
| 1 | top-level claim: `(H1)+(H2)` `=>` `X` is not `k`-colourable | **proof** (re-derived, Theorem A) | **correct**, and stronger than stated: no accident hypothesis needed, `D >= 1/2` suffices |
| 2 | Lemma 1, "the whole chain is monochromatic" | **false as stated** | corrected to Lemma 1'; counterexample at `k = 2` and visible at `k = 3`; theorem unaffected |
| 3 | accident classes §5 | **incomplete** | missing class (4): cross-copy unit distances *within* a chain |
| 4 | `D > 1/2` / `D = 1/2` degenerate | correct but **overstated** | `D >= 1/2` suffices for the lower bound; strictness is hygiene |
| 5 | `|C_n| = nV - (n-1)` | correct **with** the no-coincidence caveat | caveat in §5.1, equality asserted in §2 |
| 6 | `nE` edges in the chain | **lower bound only** | cross-copy edges can add; §3 uses `<=` correctly |
| 7 | field extension §6 | **correct** | confirmed on a new instance (`Q(sqrt7, sqrt5)`) |
| 8 | `(H4)` `=>` `chi(X) = k+1` | sound in structure, **conditional on accident checks** | confirmed exactly on the new `k = 2, n = 3` instance (`chi = 3`) |
| 9 | §7 Moser-spindle validation | **correct** | but tests §3 only; `n* = 1`, so §2 is untested by it |
| 10 | §4 "exactly as hard as `chi(R^2) <= 6`" | **overclaim** | weaken to: absence of a forcing pair is *necessary* for `chi(R^2) <= 6` |
| 11 | no forcing pair asserted | **correct / unchanged** | none found; none claimed |

## 6. Limitations of this audit

* I did not search for a forcing pair and did not attempt any construction at `k = 6`; the audit is
  about the amplifier's validity, not about whether its hypothesis is satisfiable.
* The `k = 2, n = 3` instance verifies distances, counts, distinctness, the final unit edge, and
  `(H4)`-consistency by exact arithmetic. It does **not** independently re-derive `chi(X) = 3` by a
  colouring algorithm; the `<=` direction is argued from `(H4)` plus the exact edge-count equality.
* Accident class (4) is shown to be missing from the file's list; it is **not** shown to occur. The one
  instance I built has none.
* Everything here is a statement about finite unit-distance graphs. No global-plane conclusion follows.

## 7. Reproduce

    python3 audit-amplifier/chain_k2_n3.py
