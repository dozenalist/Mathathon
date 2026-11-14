# Independent audit of §7 — the load-bearing transfer

**Headline (the sharpest correct statement of the transfer).** For every `k ≥ 3`: *if a weak
measurable `k`-colouring has `L ∩ B(y,R)` finite for some `y` and some `R > 1`, then Proposition 7.1
holds at `k` with a cycle length `ℓ ∈ {3,…,k}`.* §7 uses no palette input at all — no palette bound,
no `(5.2)`, `(5.3)`, `(5.7)`, `(5.12)`, no Lemma 5.5, no `(6.2)`, no closedness of `L`, no
properness, no tameness — and not even the circle-measure Fourier estimate `(6.3)` (E9). The
constant `1` is exact for this method (Lemma C + Lemma S). The two
constants the record quotes for `(W)`/`(F)` (`R > 1`, side `> 2`) require the sharpened cover lemma,
which the printed Lemma 7.5 and the machine-checked engine do not supply (errata E3, E7).

**Scope.** This is an audit of the only step of the five-colour proof that Sprint B needs at
`k = 6`: §7 of the paper (pp. 42–50), which turns *one isolated cyclic centre* into a cycle of
compact connected common exclusion continua. Deliverables, in the order they appear below:

1. **Theorem A\*** (§5): the sharp form of the transfer, valid for **every** `k ≥ 3`, with the exact
   hypothesis list. `(W)` with `R > 1` is confirmed as the correct hypothesis; nothing else from
   §5–§6 is used.
2. **Lemma C** (§3): the sharpened cover obstruction — *inradius > mesh*, not the printed
   "side ten, mesh two". This is the missing piece that makes `(W)` with `R > 1` rigorous: the
   printed Lemma 7.5 only reaches inradius > 2, and the machine-checked engine
   (`k6_s7_engine.lean`) only reaches a ball of radius 5 with mesh 2 (errata E7).
3. **Lemma S** (§4): the constant 1 is **optimal as the threshold of the cover obstruction** — for
   every `η > 0` the closed unit disk admits a multiplicity-≤2 relatively open cover of mesh
   `≤ 1 + η`, while Lemma C forbids mesh `< 1`. So the threshold is exactly the inradius, and at
   `R = 1` (inradius 1, component-cover mesh `1 + o(1)`) the obstruction is **unavailable**: the
   printed route cannot be pushed to `R = 1`. Exact certificate: `verify_constants.py`, checks C5.
4. **Errata list** (§6, E1–E10): every item is either a proof or an explicit numerical
   counterexample. Three of them bear on the record's proofs rather than on the paper: E2 (the
   side-ten step needs `L ∩ B(y,5√2)` finite, not `R > 1`), E7 (the machine-checked engine needs a
   ball of radius 5 with mesh 2, so the `R > 1` form is not machine-checked), E5 (`WEAKEST.md`'s
   `4 < s < r/√2` should be `s ≤ r√2`); E1 (a redundant hypothesis) and E9 (`TRANSFER.md`'s
   misattribution of `(6.3)`) make the dependency list *smaller*; E3/E4/E6/E8 verify and sharpen
   constants; E10 corrects a stale overstatement in `.ultramath/smwfwi7rh/m3/report.md` (the
   `k ≥ 7` example refutes local finiteness, not `(W)`).

**What this audit does not do.** It does not prove `(W)`, does not improve any bound on
`χ(R²)`, and does not decide anything new at `k = 6`: Theorem A\* is conditional on `(W)` and is
vacuous if `χ(R²) = 7` (no six-colouring exists). See §8.

---

## 1. What was checked, and against what

* **Text.** `pdftotext -layout -f 24 -l 34` (§5.1–§6.1), `-f 34 -l 41` (§6.1–§6.3), `-f 40 -l 52`
  (§6.3.3–§8.3), and `-f 40 -l 52` again for §7 in full.
* **Rendered formulas (second, independent readout).** `formula_check.py` (in this directory)
  reads the glyph geometry that `mutool draw -F stext.json` extracts — per-span bounding boxes,
  baselines and **font sizes** — rebuilds super/subscripts from size and vertical offset, and
  prints each line with explicit `^{…}` / `_{…}` groups. Two independent extractors therefore
  agree *character by character with position information*, which is what catches the failure
  mode of the `(8.6)` trap (an extensible delimiter that flat text drops or duplicates).
  Reproduce: `python3 formula_check.py <paper.pdf> 44 45 46 47 48 35` (and `35 36` for
  `(6.1)`,`(6.2)`,`(6.3)`).
* **Limit of the check, stated plainly.** I have no image channel: I did not look at a
  `pdftoppm` render. Every displayed formula used below was verified by (i) `pdftotext -layout`,
  (ii) glyph-level geometry with font sizes, and (iii) an arithmetic re-derivation in exact
  arithmetic (`verify_constants.py`). For the formulas used here that is stronger than a visual
  check for the specific failure mode at issue (missing large delimiters, lost sub/superscripts),
  but it is not a statement about typography or about formulas I do not use.
* **Exact arithmetic.** `python3 verify_constants.py` (exit 0, `ALL EXACT CHECKS PASS`): checks
  C1–C7, no floating-point comparison in any decision; block C5c is a grid scan and is labelled a
  sanity check, not part of any proof.
* **The Lean engine.** I did not re-run `k6_s7_engine.lean` (that is another member's direction);
  I read its statement, which matters for errata E7, from
  `lean/OAI/Geometry/PlaneColoring/PlanarCovers.lean` and `.ultramath/smwfo9zkl/m9/`.

* **Citation census of §7 (evidence for "no palette input").** Extracting §7's text
  (`awk '/^7 +Extraction/,/^8 +Angular/'`) and listing every cross-reference in it leaves exactly
  three external items besides §7's own lemmas: **Theorem 6.5** (once — only for "`L_0` is finite",
  the seat of `(W)`), **`(6.1)`** (once, in Lemma 7.3's proof), and **Theorem 1.9** (Brouwer). In
  particular `(5.2)`, `(5.3)`, `(5.7)`, `(5.12)`, `(6.2)`, `(6.3)`, Lemma 5.5, Lemma 6.2 and
  Lemma 4.3 are **not cited anywhere in §7** — `(6.3)` and the Fourier decay are not used at all
  (errata E9), and Lemma 4.3 is used only through its *content* ("two typical points at unit
  distance differ"), which Lemma 7.2's proof invokes verbally.

The formulas used, as verified:
`(6.1)` `limsup_{h→0,h≠0} D_ij(B,h)/|h| > 0`; `(6.2)` `P_x(e) ⊄ {i,j}`;
`(6.3)` `‖S a_s − S a_s(·+h)‖_{L²(B)} = o(|h|)`; `(7.2)` `p_i^ε(q) + p_i^ε(z) ≤ 1` for `|q−z| = 1`;
`(7.3)` `∫_{B'} p_i^ε p_j^ε = o(ε)`; `(7.4)`
`q_i^ε(z) = (p_i^ε(z) − α)_+ / Σ_{k∈I}(p_k^ε(z) − α)_+` with `0 < α < 1/5` printed;
`(7.6)` `E_n = ⋃_{B(u,r)∈H_n} E(u,r)`, `|E_n| ≤ 4π Σ r → 0`; `(7.7)`
`α|A_i ∩ U| ≤ ‖p_i^{ε_n} − a_i‖_{L¹(U)} + α|E_n ∩ U| → 0`; Lemma 7.5 (side ten, multiplicity ≤ 2,
mesh ≤ 2, mesh = sup of Euclidean diameters); Lemma 7.6 (mesh of the component cover `≤ 1+o(1)`);
Proposition 7.1 (`ℓ ∈ {3,4,5}`, `x ∈ K_j`, `K_j ∩ ∂B(x,ρ) ≠ ∅`, `H_{i_j} ∩ Δ(K_j) = H_{i_{j+1}} ∩ Δ(K_j) = ∅`).

---

## 2. The hypothesis list, with the anchor for each step

`I` is the label set, `|I| = k`; `c` is a weak measurable `k`-colouring (Definition 1.2), `A_i` its
classes, `H_i` the closed essential supports, `R` rotation by `π/3`, `P_x` the maximal palettes of
Definition 5.1, `Γ_x` the transition graph of Definition 6.1, `L = {x : Γ_x contains a cycle}`.

| §7 step | what it actually uses | `k`-dependence |
|---|---|---|
| Lemma 7.2 | Lemma 4.3 (density-point properness: two typical points at unit distance differ) — *"Translate q and z … They cannot then both have color i"* | none |
| Lemma 7.3 | the negation of `(6.1)` (Definition 6.1 is a **definition**, not a theorem), Fubini, the root change `r = q + h_1`, the grid of side `ℓ = c_α ε`, `N_ε ε = o(1)` | none |
| the constants in `(7.4)` | denominator `Σ_k (p_k^ε − α)_+ ≥ 1 − kα`; the printed text says *"Fix 0 < α < 1/5 … The denominator is positive because the five probabilities sum to one"* | `α < 1/k` |
| target space | *"Let G be the one-skeleton of that simplex, realized as the complete graph on its five vertices"* | `G = K_k` |
| Lemma 7.4 | in a forest a clique has `≤ 2` vertices — *"They therefore number at most two, and a two-element set is a forest edge"*; plus compactness of `M_δ = Q' ∖ ⋃B(x,δ)`, a Lebesgue number, disk merging, tree extension. **No palette bound is used anywhere** | none |
| Lemma 7.5 | partition of unity, `|F(z) − z| ≤ Σϕ_a|z_a − z| ≤ 2`, `F(Q) ⊆` finite union of segments, Brouwer | none (any `k`), but see Lemma C |
| Lemma 7.6 | *"multiplicity at most two, since every point of G has at most two positive coordinates"*; the mesh bound by Lemma 7.2 and `(7.6)`, giving `≤ 1 + o(1)` | none |
| Lemma 7.7, 7.8 | any finite connected simple graph — free homotopy classes, reduced words, fundamental group of the annulus | none |
| the cycle length | *"There are only finitely many simple cycles in the complete graph on five vertices … of length ℓ ∈ {3,4,5}"* | `ℓ ∈ {3,…,k}` |
| **`(W)`** | `Q` with `∂Q ∩ L = ∅`; `L_0 = L ∩ Q'` **finite**; later `x ∈ L_0 ∩ int Q` with `B(x,ρ)` containing no other point of `L_0` | the only non-label input |

Consequences, all of which I verified line by line:

* **No palette input, and no Fourier input.** `(5.2)`, `(5.3)`, `(5.7)`, `(5.12)` (Prop. 5.6),
  Lemma 5.5, Lemma 6.2 `(6.2)`, the palette bound, self-avoidance, closedness of `L`, **and the
  Fourier estimate `(6.3)`** are **not used** by §7 (`(6.3)` is used in §6.1's Lemma 6.2, not in
  §7 — see E9). The only inputs are Definition 1.2 with Lemma 4.3's content (used verbally inside
  Lemma 7.2), Definition 6.1 `(6.1)` (a *definition*), and `(W)`.
* **No properness, no tameness, no measurability beyond Definition 1.2.** In particular the
  transfer applies to every weak measurable `k`-colouring, `k ≥ 3`.
* **The order of quantifiers used is the printed one**: `Q` is chosen first, then the subsequence
  with non-null core loop fixed (Lemma 7.6 supplies *some* core disk of `Q`), then `ρ`, then the
  subsequence with a fixed simple cycle. Nothing is chosen depending on `L` in a way that needs
  more than `L ∩ Q'` finite.

---

## 3. Lemma C — the cover obstruction at its true constant

**Lemma C.** Let `Q ⊆ R²` be compact, convex, nonempty, with **inradius** `> m`
(`inradius(Q) := sup{r : ∃y, B̄(y,r) ⊆ Q}`). Then `Q` has no relatively open cover of multiplicity
at most two and mesh at most `m`, where mesh is the supremum of the Euclidean diameters of the
members.

*Proof.* Let `U_a` be such a cover. Compactness gives a finite subcover with the same bounds;
pass to it. Since `diam(U_a) ≤ m < 2·inradius(Q) ≤ diam(Q)`, no `U_a` equals `Q`, so
`d_a(z) = dist(z, Q ∖ U_a)` is finite-valued and continuous, and normalizing `Σ_a d_a` (positive on
`Q` because the `U_a` cover) gives a continuous partition of unity `ϕ_a` with `ϕ_a(z) > 0 ⟹ z ∈ U_a`.
Pick `z_a ∈ U_a` and put `F(z) = Σ_a ϕ_a(z) z_a`. Each `z` lies in at most two `U_a`, hence at most
two weights are positive, so `F(Q)` is contained in the finite union of the segments `[z_a,z_b]`
and the singleton vertices `z_a`; and `F` is continuous with `F(Q) ⊆ Q` by convexity and
`|F(z) − z| = |Σ_a ϕ_a(z)(z_a − z)| ≤ Σ_a ϕ_a(z)·m = m`.
Fix `y` with `B̄(y,m) ⊆ Q` (such `y` exists because the inradius exceeds `m`). Then
`Φ(z) = y + z − F(z)` satisfies `|Φ(z) − y| = |z − F(z)| ≤ m`, so `Φ(Q) ⊆ B̄(y,m) ⊆ Q`: `Φ` is a
continuous self-map of the nonempty compact convex set `Q`, hence (Brouwer) has a fixed point
`Φ(z) = z`, i.e. `F(z) = y`. Therefore
`{y ∈ Q : B̄(y,m) ⊆ Q} ⊆ F(Q) ⊆` finite union of segments.
But `{y : B̄(y,m) ⊆ Q}` contains an **open** set: if `B̄(y₀,ρ) ⊆ Q` with `ρ > m` then
`B(y₀, ρ−m) ⊆ {y : B̄(y,m) ⊆ Q}`. A finite union of segments has empty interior. Contradiction. ∎

*Relation to the paper.* The printed Lemma 7.5 is the special case `Q` = closed square of side ten
(inradius 5) and `m = 2`; the proof above is the printed proof with the constant `2` replaced by the
mesh `m`, and with the square replaced by an arbitrary compact convex `Q` (the paper's proof uses
only compactness, convexity and mesh — no property of a square that a convex set lacks, and the
only place `5` appears is `dist(y,∂Q) > 2 ≠ ∅`). Nothing new is claimed here beyond the exact
constant condition; what *is* new is (i) the constant condition "inradius > mesh" and (ii) its
optimality, Lemma S.

**Corollary C′ (the forms §7 actually needs).**
(a) A closed disk of radius `R > 1` admits no multiplicity-≤2 cover of mesh `≤ 1 + o(1)`, for `n`
large enough that `1 + o(1) < R`.
(b) A closed square of side `s > 2` has inradius `s/2 > 1`, so (a) holds with the square in place of
the disk.
(c) With the printed constants (`m = 2`): a closed square of side `s > 4` (inradius `s/2 > 2`) and a
closed ball of radius `R > 2` are the regions the printed Lemma 7.5 reaches.

---

## 4. Lemma S — the threshold of the cover obstruction is exactly the inradius

**Lemma S.** For every `η > 0` the closed unit disk `D̄ = B̄(0,1)` admits a relatively open cover of
multiplicity at most two and mesh at most `1 + η`. Together with Lemma C — which forbids mesh
`<` inradius — this pins the threshold of the cover obstruction at exactly the inradius: no
version of Lemma C with the hypothesis "inradius `≥` mesh" can hold, and the obstruction is
unavailable precisely when the mesh exceeds the inradius.

*Construction (13 sets; parameters `η > 0`, `β = η`, `a = (1+η)/2`, `γ = 2β`).* Relative to `D̄`:
`A₀ = {|z| < a}`; `S_k = {a < |z| ≤ 1, dist(arg z, kπ/3) < π/6 − β}` for `k = 0,…,5` (six sectors,
notched by `β` at each side); `T_k = {1/2 < |z| ≤ 1, |arg z − (k+½)π/3| < γ}` for `k = 0,…,5` (six
spokes on the sector boundaries). All are intersections of `D̄` with open sets.

*Diameters (exact, `verify_constants.py` C5).* `diam(A₀) = 2a = 1 + η`. For two points of `S_k` with
moduli `r, r' ∈ [0,1]` and angular separation `φ < π/3 − 2β`,
`|z − z'|² = r² + r'² − 2rr' cos φ` is convex in `(r,r')`, so its maximum over the square `[0,1]²` is
attained at a vertex and equals `max(1, 2 − 2cos φ) = 1`, because `2 − 2cos φ < 1 ⟺ cos φ > 1/2 ⟺
φ < π/3`. So `diam(S_k) ≤ 1` (attained by an apex–arc pair). For two points of `T_k`, `r, r' ∈
[1/2, 1]` and `φ < 2γ = 4β`, and the same vertex check gives
`diam(T_k)² ≤ max(5/4 − cos 4β, 4 sin² 2β) = 1/4 + 2 sin² 2β < 1` (using `cos 4β > 1 − 8β² > 1/4`).
So the mesh is `≤ 1 + η`.

*Coverage.* `|z| < a` lies in `A₀`. For `|z| ≥ a`: if `arg z` is within `γ` of one of the six sector
boundaries `(k+½)π/3`, then `z ∈ T_k` (as `|z| ≥ a > 1/2`); otherwise `arg z` is at distance `> γ =
2β > β` from both sides of the unique sector containing it, so `z ∈ S_k`.

*Multiplicity.* A point of a sector has `|z| > a`, so `A₀` meets no sector. `A₀` meets at most one
spoke (spokes are `π/3` apart, `2γ ≪ π/3`). A point off the six rays lies in at most one sector, and
in at most one spoke. Hence at most two sets contain any point. ∎

**Consequence for the transfer.** Lemma 7.6 produces a multiplicity-two component cover of `Q` of
mesh `1 + o(1)`; the region `Q` of Theorem A\* has inradius `R' ∈ (1,R)`. If `R > 1`, then
`1 + o(1) < R'` for large `n` and Lemma C forbids the cover — that is the contradiction. If
`R = 1`, the inradius is `1 < 1 + o(1)`, Lemma C says nothing, and Lemma S exhibits
multiplicity-two covers of mesh `1 + η` for every `η > 0`, i.e. of the same mesh as the component
cover; so the printed method yields **no** contradiction at `R = 1`. The constant `1` in `(W)` is
therefore exactly the constant of this method. (That does not show that
`R = 1` is insufficient for the *conclusion* of Theorem A\*; see §8.)

---

## 5. Theorem A\* — the sharp form of the transfer

**Theorem A\*.** Let `k ≥ 3`, let `c` be a weak measurable `k`-colouring of `R²` (Definition 1.2),
let `Γ_x` be its transition graph (Definition 6.1) and `L = {x : Γ_x contains a cycle}`. Assume

> **(W)** there are `y ∈ R²` and `R > 1` with `L ∩ B(y,R)` finite,

and (the form in which it is used, implied by `(W)`: take `Q = B̄(y,R')` and `Q' = B̄(y,R'')` with
`1 < R' < R'' < R`) there are a compact convex `Q` of inradius `> 1` and a closed `Q' ⊇ Q` with
`L ∩ Q'` finite.

Then there are `ℓ ∈ {3,…,k}`, distinct labels `i₀,…,i_{ℓ−1}`, a point `x`, a radius `ρ > 0`, and, for
every edge `i_j i_{j+1}` (indices mod `ℓ`), a compact connected set `K_j ⊆ B(x,ρ)`, a direction
`v_j ∈ S`, and a sequence `q_{j,m} ∈ K_j ∖ {x}` with

1. `x ∈ K_j` and `K_j ∩ ∂B(x,ρ) ≠ ∅`;
2. `q_{j,m} → x` and `(q_{j,m} − x)/|q_{j,m} − x| → v_j`;
3. `H_{i_j} ∩ Δ(K_j) = H_{i_{j+1}} ∩ Δ(K_j) = ∅`, with `Δ(K) = {z : min_{q∈K}|z−q| < 1 < max_{q∈K}|z−q|}`.

No palette bound, no `(5.2)`, `(5.3)`, `(5.7)`, `(5.12)`, no Lemma 5.5, no `(6.2)`, no closedness or
local finiteness of `L`, and no tameness is used.

*Proof.* Run the printed §7 with `I` of size `k`, `α ∈ (0,1/k)`, `G = K_k`. Steps 7.1–7.4 (Lemmas
7.2–7.8) are label-blind by §2 and require no changes. Three modifications are needed, all
consequences of the region and the constants; they are the content of errata E2–E4.

(i) *Region.* By `(W)` fix `y`, `R > 1` and choose `R' ∈ (1,R)` such that `∂B(y,R') ∩ L = ∅` — the
only radii to avoid are those of the finitely many points of `L ∩ B(y,R)`, so such `R'` exists.
Put `Q = B̄(y,R')`, `Q' = B̄(y,R'')` with `R' < R'' < R`; then `Q ⊆ int Q' ⊆ Q'` and `L ∩ Q'` is
finite, so `L_0 = L ∩ Q'` is a finite set. Lemma 7.4 applies verbatim, with `Q` a disk instead of a
square: it uses only compactness of `M_δ = Q' ∖ ⋃_{x∈L_0} B(x,δ)`, the Lebesgue number of a finite
cover, disk merging, and the positive distances from the finite set `L_0` to `∂Q` (to place each
core disk in `int Q`, resp. outside `Q`). Local path connectedness of `Q` and its relatively open
subsets (used in Lemma 7.6) holds for a disk as for a square.

(ii) *Mesh and cover.* Lemma 7.6's component cover of `Q` has mesh `≤ 1 + o(1)` (printed proof,
unchanged: Lemma 7.2 forces `|a − b| > 1` for a violating pair, then `(7.7)` contradicts
`a ∈ H_i`). The inradius of `Q` is `R' > 1`, so for all large `n` the mesh is `< R'`, and Lemma C
with `Q` in place of the square forbids the cover. This replaces the printed use of Lemma 7.5 on a
side-ten square; note that this is exactly where the printed constants would have required
`R' > 2` (errata E3) and a side-ten square would have required `R > 5√2` (errata E2).

(iii) *Extraction.* Unchanged: `L_0 ∩ Q` is finite, so pass to a subsequence with a fixed
`x ∈ L_0 ∩ int Q` whose core boundary loop is non-null at every index (Lemma 7.6); choose
`ρ > 0` with `B(x,ρ) ⊂ int Q` and `B(x,ρ) ∩ L_0 = {x}` (possible: `L_0` finite, `x ≠ x'`);
decreasing `ρ`, the other core disks miss `B(x,ρ)` for large `n` while `B_{n,x} ⊂ B(x,ρ)`;
`g_n` is defined on the closed annulus `A_n = B̄(x,ρ) ∖ B_{n,x}`; the inner boundary word is
nonempty and cyclically reduced, contains a simple cycle (Lemma 7.7); there are finitely many
simple cycles in `K_k`, so a subsequence has a fixed cycle of length `ℓ ∈ {3,…,k}` — exactly
`20 + 45 + 72 + 60 = 197` simple cycles for `k = 6` (formula and brute-force enumeration agree,
`verify_constants.py` C7; `37` for `k = 5`, the paper's case split); Lemma 7.8
gives compact connected components of `g_n^{-1}({m_j})` meeting both boundaries for each edge
midpoint; Hausdorff limits are compact connected, contain `x`, meet `∂B(x,ρ)`, and the support
exclusion follows from the `α`-estimate `(7.7)` at `k` labels. ∎

*Sharpness of the hypothesis, within this method.* By Lemma S the cover obstruction is unavailable
at `R = 1` (inradius `1`, mesh `1 + o(1)`), and by Lemma C no `R < 1` can work either; so `R > 1`
is exactly the constant of the printed method. (Moreover the proof shows that the region only has
to be *some* compact convex set of inradius `> 1`, with a finite `L`-trace in a neighbourhood — e.g.
a closed square of side `> 2` gives the record's `(F)`.)

---

## 6. Errata

**E1. `(P)` in `TRANSFER.md`'s Theorem A is redundant and should be deleted.**
`TRANSFER.md` lists `1 ≤ |P_x(e)| ≤ 3` as a hypothesis. By the table of §2 no step of §7 uses a
palette bound (the thresholded vector is graph-valued because a clique in a forest has at most two
vertices, not because palettes are small). Hence Theorem A\* holds for *every* weak measurable
`k`-colouring, with no palette hypothesis. The parenthetical justification in `TRANSFER.md` also
merits a correction: `(5.12)` of the paper is `1 ≤ |P_x(e)| ≤ 2` and its proof (p. 33) needs the
complement of a triple to have exactly two elements, i.e. `k = 5`; the correct general statement is
`|P_x(e)| ≤ k − 3` (`results/K6-BARRIER.md` §1, whose proof uses `(5.2)` + `(5.7)` + Lemma 5.5),
which at `k = 6` gives `3`. That theorem is true, and it is *not* what `§7` uses. *Proof:* the
step-by-step anchors of §2.

**E2. The record's proof of Theorem A, as literally written, needs `L ∩ B(y, 7.08)` finite, not
`R > 1`.** `TRANSFER.md`'s proof and the report `§2` run §7 on *"a closed square Q of side ten"*.
A closed square of side 10 has circumradius `5√2 = 7.0710678…`, so `Q ⊆ B(y,R)` forces
`R > 5√2` (*exact*: `5√2 > 7`, and `7 > 1.1`; `verify_constants.py` C2, C6). *Explicit
counterexample to the literal step*: with `R = 11/10` (or any `R ∈ (1, 5√2)`) there is no side-ten
square inside `B(y,R)`, so the displayed choice of `Q` is impossible. *Repair:* Theorem A\* — the
region must be a compact convex set of inradius `> 1` (a disk of radius `R' ∈ (1,R)`), and the
cover obstruction must be Lemma C. `WEAKEST.md` contains this sharpening in the `(ISO)` form; the
report's Theorem A and `TRANSFER.md` do not state it.

**E3. The printed Lemma 7.5 reaches only inradius `> 2`.** Its proof uses
`|F(z) − z| ≤ 2` (from mesh `≤ 2`) and then the central region `{y ∈ Q : dist(y,∂Q) > 2}`; the
Brouwer step needs `B̄(y,2) ⊆ Q`. Hence with the printed constants the hypothesis of the cover
obstruction is "contains a closed ball of radius `2`", i.e. inradius `> 2`: closed squares of side
`> 4`, closed balls of radius `> 2`. *Where the constant enters*: `Σ_a ϕ_a(z)|z_a − z| ≤ mesh`, and
`y` ranges over `{y : B̄(y,mesh) ⊆ Q}`. By Lemma S this strict inequality is *exactly* the
threshold: no version of the cover obstruction with "inradius `≥` mesh" can hold.
Consequently the record's constants `(F): square of side > 2` and `(W): R > 1` are **not**
consequences of the printed Lemma 7.5; they are consequences of Lemma C.

**E4. The paper's "side ten" is not a threshold.** A closed square of side `s` has inradius `s/2`
(exact), so the printed Lemma 7.5 holds for every compact convex region of inradius `> 2` in
particular for squares of side `> 4`; the number ten is a convenient constant, not a condition.
With Lemma C the threshold drops to side `> 2`. (`verify_constants.py` C4.)

**E5. `WEAKEST.md`'s displayed inequality is arithmetically inconsistent with its own conclusion.**
`WEAKEST.md` asks for `"a closed square Q centred at x_0 with side s, where 4 < s < r/sqrt 2, so
Q subset B(x_0,r)"`. A square of side `s` has circumradius `s/√2`, so `Q ⊆ B(x_0,r)` is
`s ≤ r√2`, not `s ≤ r/√2`. With the displayed inequality the demand `4 < s < r/√2` is empty
whenever `r ≤ 4√2`, so in particular for every `r ∈ (√2, 4√2]` — the display and the stated
constant `r > √2` are incompatible. For the *stated* sharpened requirement `s > 2` the correct
inclusion `s ≤ r√2` gives a solution exactly when `r√2 > 2`, i.e. `r > √2`: the theorem's constant
is right and the display is wrong. *Explicit numbers*: `r = 3/2` gives `r√2 = 2.1213…`, so
`s = 2.05` works (`2 < 2.05 < r√2`, `Q ⊆ B(x_0,r)`), whereas the display reads `4 < s < 1.06` and
has no solution; with the printed constants (`s > 4`) the hypothesis would have to be `r > 2√2`
(`verify_constants.py` C3).

**E6. Label-blindness has exactly three seats, and they are the three that must change.** The only
occurrences of `k` in §7 are: (i) `α < 1/k` in `(7.4)` — the printed *"the denominator is positive
because the five probabilities sum to one"* becomes `"the k averages sum to one"`, giving the exact
condition (C1: the uniform vector `(1/k,…,1/k)` makes the denominator vanish at `α = 1/k`, and
`Σ(p−α)_+ ≥ 1 − kα > 0` for `α < 1/k`); (ii) `G = K_k` (*"the complete graph on its five
vertices"*); (iii) the cycle-length range `{3,…,k}` (*"only finitely many simple cycles in the
complete graph on five vertices … ℓ ∈ {3,4,5}"*). There is no fourth seat: Lemmas 7.2, 7.3, 7.4,
7.5, 7.6, 7.7, 7.8 use only Lemma 4.3, the *definition* `(6.1)`, the circle-measure Fourier estimate
`(6.3)`, Fubini, compactness, the clique-in-a-forest bound, the partition of unity, Brouwer, graph
homotopy and the fundamental group of the annulus.

**E7. The machine-checked §7 engine does not cover the form of Theorem A needed at `k = 6`.**
`k6_s7_engine.lean`'s geometric engine is
`graph_map_small_mesh_impossible_generic (F : C(Metric.closedBall (0:ℂ) 5, GraphSpace (⊤ : SimpleGraph V)))`
with mesh `≤ 2`, resting on `PlanarCover.compact_open_cover_impossible` whose hypothesis is
`Metric.ball (0:ℂ) 5 ⊆ Q` and `‖x − y‖ ≤ 2`. That is the printed (side-ten, mesh-two) regime: it
needs a closed ball of radius **5**, not inradius `> 1`. So the record's `(W)`/`R > 1` and its
`(ISO)`/`r > √2` forms are *not* machine-checked; the machine-checked layer supports the
local-finiteness form `(LF)` (which gives `R` arbitrarily large). The gap is exactly Lemma C, proved
in §3; a formalisation of Lemma C would need Brouwer on a compact convex set, which the existing
development (`finite_partition_impossible`) already uses in the ball-of-radius-5 form.

**E8. The quantitative steps of §7 that carry an `ε`-loss are correct as printed, including their
constants.** Verified: `|E_n| ≤ 4π Σ r` (an annulus of inner radius `1−r`, outer `1+r`, has area
`4πr`); the covering count in Lemma 7.3 (`ℓ = c_α ε` gives `N_ε α²ℓ²/4 ≤ ∫ p_i p_j = o(ε)`, whence
`N_ε ε = o(1)` and total radii `N_ε ℓ = o(1)`); Lemma 7.6's replacement step (`1 + c − o(1)` with
`c > 0`, and distinct hole disks for the two endpoints, so the pairwise distance bound survives);
the `α`-estimate `(7.7)` (`α|A_i ∩ U| ≤ ‖p_i^ε − a_i‖_{L¹(U)} + α|E_n ∩ U|`, using `p_i^ε(q) > α` at
the exact-unit-distance point together with `(7.2)`). No correction needed.

**E9. `TRANSFER.md` attributes `(6.3)` to Lemma 7.3; the printed proof does not use it.**
`TRANSFER.md`'s audit table says Lemma 7.3 *"uses Definition 6.1, nonnegativity,
`‖S a_s − S a_s(·+h)‖_{L²(B)} = o(|h|)` (equation (6.3)) and Fubini"*. The printed proof instead
takes the ball `B` from the negation of `(6.1)`, writes
`ω(r) = sup_{0<|h|≤r} D_ij(B,h)/|h| → 0`, and after the root change `r = q + h_1` bounds the double
average by `D_ij(B, h_2 − h_1) ≤ 2εω(2ε)`, which is `o(ε)` after dividing by `(πε²)²`. No circle
average and no Fourier estimate occurs; the citation census above confirms that `(6.3)` and the
Fourier decay do not appear anywhere in §7. The mathematics is unaffected — the dependency list
gets *smaller*, which matters because it says §7 needs no spectral input at any `k`: the sharp
hypothesis list is Definition 1.2, the *definition* `(6.1)`, and `(W)`.

**E10 (record, `.ultramath/smwfwi7rh/m3/report.md` item 3).** That item says of the accumulating
`k ≥ 7` colouring: *"So `L(c)` is closed, countable, and not locally finite — the failure of `(W)`
at `k ≥ 7` is witnessed by a countable set with one accumulation point."* The concluding clause is
false, as the same item's own display shows: `L(c) = V ∪ {q_n, z_n : n ∈ N} ∪ {p_0}` with `V` the
honeycomb lattice of side `2/5` and `p_0` the only accumulation point, so for any `y` with
`|y − p_0| > 2` the ball `B(y,3/2)` meets `V` in finitely many points (minimum separation `2/5`)
and none of the `q_n, z_n`, hence `L(c) ∩ B(y,3/2)` is **finite** and `(W)` *holds*. What the
example refutes is local finiteness, not `(W)` (`sprint/k6/REPORT.md` §3b carries the correction; the
report item is stale). This matters for the record's ledger, where `(W)` "is not refuted at any
`k`", and it is used in §7 below.


---

## 7. Calibration, and non-vacuity of Theorem A\*

* **`k = 5` (the paper).** Theorem 6.5 gives `L` locally finite, hence `(W)` for every `R`, hence
  `(F)` and Theorem A\* with `ℓ ∈ {3,4,5}`: the printed Proposition 7.1. The audit therefore
  reproduces the paper's own use exactly, including the constant `α < 1/5`.
* **`k = 7` (`m3`'s proper colouring, `.ultramath/smwfwi7rh/m3`).** There `L = V ∪ {q_n, z_n} ∪
  {p_0}` is closed, countable, with one accumulation point, so `L ∩ B(y,3/2)` is finite for any `y`
  at distance `> 2` from `p_0`: `(W)` holds (errata E10 corrects the opposite claim in that
  report's item 3). Theorem A\* then applies at `k = 7` and produces
  `ℓ ∈ {3,…,7}`; and indeed at each `q_n` the transition graph contains the triangle
  `{0,2},{2,3},{3,0}`, so `ℓ = 3` is the realised length. The theorem is therefore non-vacuous on the
  one model of the record that satisfies its hypothesis.
* **`k = 6` (conditional).** No six-colouring is known (`χ(R²) ∈ {6,7}`), so Theorem A\* at
  `k = 6` is an implication whose hypothesis is open; it is *vacuous* if `χ(R²) = 7`, and it can
  fail only if a six-colouring exists whose `L` is infinite in every ball of radius `> 1`. That
  conditionality is the record's, unchanged; the audit adds nothing to either side of it.
* **The other models are outside the hypothesis.** Lemma S's cover, the block/sector fields of
  `§4` and the three-valued fields are palette fields, not colourings, so they have no `Γ_x`, no `L`
  and no `(W)`; they are not tests of Theorem A\* (they are tests of the *palette* axioms, which §7
  does not use).

---

## 8. What I did not prove

* Not `(W)` at `k = 6`, and no bound on `χ(R²)` in either direction.
* Not that `R = 1` is insufficient for the *conclusion* of Theorem A\*: Lemma C plus Lemma S show
  only that the printed route's cover obstruction is unavailable at `R = 1`. Deciding whether
  `L ∩ B(y,1)` finite suffices would need a different extraction, and the obstruction's absence at
  `R = 1` is not evidence either way.
* Not a machine-checked version of Lemma C or Lemma S (§3, §4 are proofs in prose; the geometric
  inequalities of Lemma S are certified in exact arithmetic by `verify_constants.py`, and its
  coverage/multiplicity claims are additionally checked on a grid — a sanity check, not a proof).
* Not a pixel-level inspection of the paper (§1 states exactly what was checked and how).
* Nothing here is a claim about the *sharpness* of `1 + o(1)` in Lemma 7.6 beyond "the argument
  gives no fixed positive margin": the bound is `≤ 1 + o(1)` and the cover obstruction needs a
  strict inequality against the inradius, which is why `R > 1` (not `R ≥ 1`) is the constant.

## 9. Reproducing

```
cd .ultramath/smwg1r9lg/m3                          # the audit's directory
python3 verify_constants.py                         # exit 0, "ALL EXACT CHECKS PASS" (C1-C7)
python3 formula_check.py ../../../attachments/here-are-three-files-ni5n/paper.pdf 44 45 46 47 48 35
                                                    # exit 0, 273 lines of render-verified formulas
cd ../../..                                          # repo root
pdftotext -layout -f 40 -l 52 attachments/here-are-three-files-ni5n/paper.pdf .scratch/paper/s7.txt
awk '/^7 +Extraction of common exclusion/,/^8 +Angular/' .scratch/paper/s7.txt > .scratch/paper/s7only.txt
grep -o "(5\.[0-9]*)\|\(6\.[0-9]*\)\|\(7\.[0-9]*\)\|Lemma [0-9]\.[0-9]*\|Theorem [0-9]\.[0-9]*" \
     .scratch/paper/s7only.txt | sort | uniq -c | sort -rn     # the citation census of §1
```

Both scripts were run from that directory in this session; exit statuses `0` and `0`. The two
`grep`/`awk` lines produce the census quoted in §1 (only `Theorem 6.5`, `(6.1)` and `Theorem 1.9`
are external to §7).
