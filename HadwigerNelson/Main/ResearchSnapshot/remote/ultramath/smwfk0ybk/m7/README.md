# Step 1 is decided: the tightened interface CSP at k = 6 is SATISFIABLE at every length, and no strengthening that uses one centre's palette data can change that

Member m7, direction d4. This note (a) decides the mission's tightened CSP at k = 6 exactly, (b) shows
*why* the answer cannot be UNSAT — the tightening is structurally empty — (c) derives two further TRUE
constraints the interface CSP omits, decides them, and finds them also satisfiable, and (d) proves a
no-go: an **explicit measurable palette field at a single centre satisfies every one-centre consequence
of the paper we can derive** — (C1), the whole-circle a.e. form of (5.7), Lemma 8.1's (8.1) for every
ray configuration, (C4), (C5), the continuum condition (C6), and the second-order form of (5.2) (C7) —
so no refutation of k = 6 whose hypotheses are among those can exist. The consequence is that Step 1
cannot reach chi >= 7 in any one-centre form, and the next round must be two-centre.

None of R1-R6 or the previous run's results is re-derived; each is cited at the point of use.

---

## 1. The decision, exactly

The object is m5's interface system `IS(k,l,sigma)` (`smwfhd5sl/m5/INTERFACE-NOGO.md` Sec. 1) with
(C4) (pair exclusion, m6 Thm 1) and (C5) (at most three ternary palettes in a pi/3-orbit, m6 Thm 2)
adjoined. I enumerate **all** `6^l` cell vectors (not only the `6^(l-1)` with `c_0 = 0`), so no
symmetry normalisation is used; the normalised counts are printed beside m5's for comparability.

| k | l | geoms | SAT (C1-C3) | SAT (C1-C5) | normalised (C1-C5) | m5's (C1-C3) | witness (cells -> palettes) |
|---|---|-------|-------------|-------------|--------------------|--------------|------------------------------|
| 6 | 3 | 216   | 216   | **216**  | 36/36     | 36/36   | (0,0,0) -> {3} {4} {3} {4} {3} {4} |
| 6 | 4 | 1296  | 1296  | **1296** | 216/216   | 216/216 | (0,0,0,0) -> {4} {5} {4} {5} {4} {5} |
| 6 | 5 | 7776  | 1350  | **1350** | 225/1296  | 225/1296| (0,0,0,3,3) -> {5} {1,4} {5} {1,4} {5} {1,4} |
| 6 | 6 | 46656 | 1062  | **1062** | 177/7776  | 177/7776| (0,0,0,3,3,3) -> {1,4} {2,5} {1,4} {2,5} {1,4} {2,5} |

Labels `0..5`, palettes listed at orbit positions `i = 0..5` (`e, Re, ..., R^5 e`). Every witness is
re-verified from the paper's own words (Lemma 8.1, display (8.1): `P_x(e) ∩ O(e) ≠ ∅`,
`P_x(e) ∩ I(e) ≠ ∅`, "labels outside the cycle belong to both") and not from the bitmask code path;
`all_witnesses.json` carries a verified model for **each of the 3924 satisfiable instances**.

**So the mission's decisive question has the SAT answer at every l**, with (C4) and (C5) present. There
is no `(l, sigma)` at k = 6 for which the tightened system is unsatisfiable, so Step 1 delivers no
lower bound. Nothing here depends on the INDUCTION LEMMA: a SAT answer needs no bridge to colourings.

## 2. Why the tightening is empty at k = 6 — the structural reason, not an accident

**(C4) and (C5) can only delete models that contain a palette of size `k-3 = 3`.** Both are vacuous on a
model whose six palettes all have size `<= 2`. And such a model exists for *every* satisfiable instance:

> **Fact (exhaustive).** At k = 6, for every `l` in `{3,4,5,6}` and every cell vector, if the instance
> has a `(C1)-(C3)` model then it has one with all six palettes of size `<= 2`. Measured:
> all **3924** satisfiable instances at k = 6 carry such a model (and therefore a `(C4)+(C5)`-clean one).
> Hence `SAT(C1-C3) = SAT(C1-C5)` at every l, i.e. **(C4) and (C5) change no decision at all.**

Structurally, for `l <= k-2` this is forced and needs no computation: with `U = {l,...,k-1}` and
`|U| = k-l >= 2`, take two outsiders `a ≠ b` and alternate `P_i = {a}` (i even), `{b}` (i odd). Both lie
in `U ⊆ O_i ∩ I_i` for every `i` and every sign matrix, so `(C2)` holds; consecutive and closing pairs
are disjoint, so `(C3)` holds; `|P_i| = 1 <= k-3`, so `(C1)` holds; no palette is a 3-set, so `(C4)` and
`(C5)` hold. **At k = 6 this covers `l = 3` and `l = 4` unconditionally**, which is exactly the two
lengths whose interfaces survive, and it is the reason `l = 3, 4` are satisfiable for *every* geometry.

At `l = 5, 6` at k = 6 there are too few outsiders (1, resp. 0) for that model, but the exhaustive count
shows every satisfiable instance still keeps a pair-model. The informative lengths for k = 6 are
therefore `l = 3, 4`, not `l = 5, 6`: the 225/1296 and 177/7776 rows are the *hardest* cases and the
`l = 3, 4` rows are free.

**The failure mode to warn the next round about.** A tightening built out of *palette-cardinality*
inequalities cannot bite at k = 6: the models that matter have `|P| <= 2`, below every bound of the form
`|P| <= k-3`. This is why (C4) and (C5) — both of which are genuine, machine-checked theorems, m6
Theorems 1 and 2 — are nevertheless inert here. Their content is about *ternary* palettes, and at k = 6
the palette system can avoid ternaries completely on the whole circle (Sec. 4).

## 3. Two further TRUE constraints, derived, decided — also satisfiable

Both are consequences of the paper that `IS(k,l,sigma)` does not use. Both are stated with the exact
hypothesis used, both are decided exhaustively, both are SAT at k = 6. So they are available to the next
round and they do not close it; anybody proposing them again should read this section first.

### (C6) The continuum condition: the palette field is indexed by ALL directions, not by one orbit

**Derivation.** Fix the cyclic centre `x` and the `l` limiting directions `v_j` of Prop. 7.1 (`q_{j,n} =
x + r_{j,n} w_{j,n} ∈ K_j`, `w_{j,n} -> v_j`; paper §8.1). Let `phi ∈ [0,pi/3)` be the phase of the
`R`-orbit and put `c_j(phi) :=` the cell of `theta_j - phi`. Write `x_j := theta_j/(pi/3) - 1/2`,
`psi := phi/(pi/3)`. Then `c_j(phi) = floor(x_j - psi)`, so on `psi ∈ [0,1)` **each coordinate decreases
by exactly one**, at the single threshold `psi = frac(x_j)`. The cell vectors that actually occur are
therefore the nodes of one monotone lattice path
`c^{(0)}, c^{(0)} - e_{j_1}, ..., c^{(0)} - (1,...,1)`; each node occupies an interval of `phi` of
**positive** length (coincident thresholds only *delete* a node, so jumps must be allowed).

The paper supplies (5.2)->Cor 5.4 (=(C3)/(5.7)), Lemma 8.1 (=(C2)) and Prop 5.6/R5 (=(C1)) for
**a.e.** direction, and `x` is fixed, so for a.e. `phi` the six palettes at `f_i = R^i f` model the
instance with cell vector `c(phi)`. The a.e.-assertions fail only on the finite set `B` of directions
perpendicular to some `v_j`, and for each of the six positions separately, so the good set of `phi` is
conull. **Hence every node of the path must be satisfiable.** This is not implied by m5's table, which
decides one node at a time.

**Decision (`chain_csp.py`, `chain_generic.py`).** For every `l` at k = 6 a fully satisfiable path
exists, both with all `l` thresholds distinct (generic ray configuration) and with jumps allowed
(any ray configuration):

```
l=3  (0,0,0)->(1,0,0)->(1,1,0)->(1,1,1)
l=4  (0,0,0,0)->(1,0,0,0)->(1,1,0,0)->(1,1,1,0)->(1,1,1,1)
l=5  (0,0,0,3,3)->(1,0,0,3,3)->(1,0,0,4,3)->(1,1,0,4,3)->(1,1,0,4,4)->(1,1,1,4,4)
l=6  (0,0,1,2,3,4)->(0,1,1,2,3,4)->(0,1,2,2,3,4)->(0,1,2,3,3,4)->(0,1,2,3,4,4)->(0,1,2,3,4,5)->(1,1,2,3,4,5)
```

(Sequences are in the order the sweep *leaves* them; the physical order as `phi` increases is the
reverse, each step subtracting 1 from one coordinate.)

**How much (C6) bites — exact counts (`chain_count.py`, 105 s).** A ray configuration is a cell vector
`c0` together with the linear order in which the `l` thresholds are crossed; the two are independent
parameters (`c_j = floor(x_j - psi)` and `frac(x_j)` are read off the same `x_j`, and every
`(floor, frac)` pair occurs), so the configuration space is `6^l * l!`.

| k | l | configurations admitting a palette field on the whole circle | fraction | per-node SAT (m5-type) |
|---|---|-----|------|------|
| 5 | 3 | 1296 / 1296      | 100%     | 100% |
| 5 | 4 | 192 / 31104      | **0.617%** | 6.48% (84/1296 cell vectors) |
| 5 | 5 | 0 / 933120       | **0%**   | 0% (paper Prop 8.2) |
| 6 | 3 | 1296 / 1296      | 100%     | 100% |
| 6 | 4 | 31104 / 31104    | 100%     | 100% |
| 6 | 5 | 33960 / 933120   | **3.639%** | 17.36% |
| 6 | 6 | 51840 / 33592320 | **0.154%** | 2.28% |

So (C6) is a genuine discriminator with content that m5's per-geometry table cannot see: at k = 5 it
cuts the surviving `l = 4` configurations by a factor 10.5, and at k = 6 a palette field at a length-5
or length-6 cyclic centre forces an almost rigid ray geometry (3.6%, resp. 0.15% of configurations).
It does not close anything, because `l = 3` — and `l = 4` — are 100% at k = 6. At k = 4 the path is
UNSAT for `l = 3, 4`; at k = 7 it is SAT for every `l`.

### (C7) The second-order form of (5.2): a finite list-colouring condition

**Derivation.** (5.2) at the single centre `x`: `c(x + e + v) ∉ P_x(e) ∪ P_x(v)` a.e. Fix the orbit
`f_i = R^i f` and, for ordered pairs with `d = j - i ≠ 3 (mod 6)` (the case `d = 3` has `f_i + f_j = 0`,
`p = x`, `v = -e`, which is a measure-zero and hence unproved instance of (5.2), so it is excluded),
put `p_{ij} := x + f_i + f_j` and `L_{ij} := Fin k \ (P_i ∪ P_j)`. Then, for a.e. `f` and simultaneously
over the finitely many pairs, `c(p_{ij}) ∈ L_{ij}`, and `c(p_{ij}) ≠ c(p_{kl})` whenever
`|p_{ij} - p_{kl}| = 1`. With `w = e^{i pi/3}` and angles in units of `pi/6`,
`f_i + f_j = 2cos(d pi/6) w^{2i+d}`, so all these points are `s e^{i m pi/6}` with `s ∈ {2, ±√3, ±1}` and
`|p - q|^2 = s^2 + t^2 - 2 s t cos((m-m')pi/6) ∈ Q(√3)`: every unit-distance test is **exact in Q(√3)**.

**Decision (`secondorder.py`).** The finite graph has **18 points and 36 unit edges**. Admissible
palette assignments must make it properly list-colourable. Checked on seven orbits, including the parity
field of Sec. 4, m5's k = 6 witnesses for `l = 5, 6`, m6's sharp three-ternary orbit, and the
(C4)-violating alternating-triple orbit: **all seven are list-colourable**, with list sizes 1..5. So
(C7) is true and does not bite either. Note in particular that (C7) does *not* imply (C4): the
alternating-triple orbit violates m6 Theorem 1 and passes (C7).

## 4. The no-go: no one-centre strengthening can refute k = 6

> **Theorem.** Let k = 6. There is an explicit, measurable palette field `P : S^1 -> 2^{Fin 6}` such that
> for `l = 3` **and for every ray configuration** `(v_0,v_1,v_2)`:
> (i) every palette is a singleton, so `1 <= |P(f)| <= k-3` and no palette is ternary;
> (ii) `P(f) ∩ P(f + pi/3) = ∅` for **every** `f` (not merely a.e.);
> (iii) `P(f) ∩ O_l(f) ≠ ∅` and `P(f) ∩ I_l(f) ≠ ∅` for **every** `f ∉ B`, with `O_l, I_l` the paper's
> own sets;
> (iv) no two palettes in an `R`-orbit are complementary, and at most three are ternary — i.e. (C4) and
> (C5) both hold with room;
> (v) the field is constant in the orbit phase, so the whole continuum condition (C6) holds as well;
> (vi) the second-order condition (C7) holds (Sec. 3).
> Consequently **any refutation of k = 6 whose hypotheses are all among (i)-(vi) is impossible**, and
> Step 1 is closed in every one-centre form covered by that list.
>
> *Construction.* With `U = {3,4,5}` the outsiders of a length-3 cycle, put `P(f) = {3}` if `f` lies in
> a `pi/3`-cell `[m pi/3, (m+1)pi/3)` of even index and `P(f) = {4}` if odd. `f -> f + pi/3` flips the
> parity, giving (ii) for every `f`; both labels lie in `U ⊆ O_l(f) ∩ I_l(f)` for every `f` and every
> ray configuration, giving (iii); (i),(iv),(v) are immediate; (vi) is the list-colouring check. For
> `l = 4` the same field with `{4}/{5}` works (`U = {4,5}`).
>
> *Verified:* `verify_chain.py` CHECK 3 — (ii),(i),(iv) identically, (iii) at all six orbit positions
> for **all** 216 (`l = 3`) resp. 1296 (`l = 4`) ray cell vectors.

**Why `l = 3` suffices.** Prop. 7.1 supplies a cyclic centre with *some* length `l ∈ {3,...,k}`. A
one-centre argument must derive `⊥` from the palette data at that centre for **every** admissible `l`.
The theorem exhibits a palette field satisfying all of it at `l = 3`, so no such derivation exists. (For
`l = 5, 6` at k = 6 an all-singleton field is impossible — with `|U| = 1` or `0` a singleton palette can
never meet both `O_i` and `I_i` as `O_i ∩ I_i = U` for cycle labels — but that is irrelevant: one
surviving length is enough.)

**What is *not* claimed, and the exact next target.** The theorem is about one centre. Whether the
parity field is the maximal palette field of an actual colouring is *not* a one-centre question: m8's
Theorem A says the full palette system at `k` (all centres, (H1)+(H2)) is satisfiable iff
`chi(R^2) <= k`. So the parity field's realizability is exactly `chi(R^2) <= 6`. The next hypothesis to
adjoin must therefore be a **two-centre instance at a unit pair** — by m8's Lemma 1 the only such
instance is the translation one, `P_x(e) ∩ P_{x+d}(e) = ∅` for `|d| = 1` — and by m8's Theorem A
adjoining it makes the system equivalent to `chi(R^2) <= 6`. Nothing weaker can close Step 1. Corollary
4 of m8 locates the cut the same way.

## 5. Audit: m5's encoding is faithful to the printed (8.1)

Checked against `pdftotext -layout` of `attachments/here-are-three-files-ni5n/paper.pdf`, §8.1,
p. 51-52: "Let `O(e)` be the set of labels remaining after the endpoints of every positive edge are
removed, and let `I(e)` be the set remaining after the endpoints of every negative edge are removed.
Labels outside the cycle belong to both sets." and Lemma 8.1's display
`P_x(e) ∩ O(e) ≠ ∅, P_x(e) ∩ I(e) ≠ ∅ for almost every e ∈ S \ B`. That is a **meets** condition, not a
containment `P_x(e) ⊆ O(e) ∩ I(e)` — the two differ decisively (containment would make `l = 6` at
k = 6 trivially unsatisfiable since `O_i ∩ I_i = ∅` there, and would "prove" chi >= 7 on the spot). m5
encodes the printed meets form. Definition 5.1 and (5.2),(5.3) also match m8's and m6's quotations.

## 6. What this reaches, and what it rules out for the next round

* **None of L1-L5 is reached.** Step 1's own branch is the SAT branch: the tightened CSP is satisfiable
  at every length, so it certifies nothing about `chi`, and no INDUCTION LEMMA is needed or used.
* **Dead routes, with certificates.** (a) any tightening by palette-cardinality inequalities at k = 6
  (Sec. 2: the models have `|P| <= 2`); (b) any tightening confined to one centre, including all of
  `(C4),(C5)`, the whole-circle a.e. form of `(5.7)`, `(8.1)` and `(5.2)`, and the continuum condition
  (Sec. 4); (c) the second-order form of `(5.2)` (Sec. 3, (C7)).
* **The live target.** A sound constraint on two centres, of the same-direction kind at a unit pair, is
  the problem (m8 Thm A). The only remaining finitely checkable direction is a two-centre instance with
  *different* directions — e.g. the paper's own Lemma 5.5 at `|x-y| < 1/2` — and the falsification test
  for any candidate is: does it exclude the parity field of Sec. 4 at `l = 3`? If not, it cannot close
  k = 6 either, by Sec. 4.

## 7. Files and exact check commands

All paths relative to `.ultramath/smwfk0ybk/m7/`. Python 3.11, integer/`Fraction`/`Q(√3)` arithmetic
only; no floating point in any decision; no external solver.

| file | what it is | command |
|---|---|---|
| `chain_csp.py` | the six-position instance, the `O_i/I_i` construction, the model enumerator (plain backtracking), and the chain (continuum) DP | `python3 chain_csp.py 6` (12 s) |
| `chain_generic.py` | generic (all thresholds distinct) vs any-configuration chains, k = 5,6,7 | `python3 chain_generic.py` (10 min) |
| `verify_chain.py` | CHECK 1 agreement with m5's independent bitmask DP on 66744 instances; CHECK 2 chain DP vs brute force; CHECK 3 the Sec. 4 field; CHECK 4 `(C4)+(C5)` never bind | `python3 verify_chain.py` (6 s) |
| `witnesses.py` | the Sec. 1 table; `--all` writes every witness | `python3 witnesses.py` (5 s), `python3 witnesses.py --all` |
| `secondorder.py` | (C7): the 18-point/36-edge graph and exact `Q(√3)` list-colouring | `python3 secondorder.py` (0.1 s) |
| `chain_count.py` | the exact counts of ray configurations admitting a whole-circle palette field | `python3 chain_count.py` (105 s) |
| `all_witnesses.json` | 3924 satisfiable `(l, cell vector)` at k = 6 with a verified model and a pair-model |

**Non-vacuity of the negative results.** Each of the three strengthenings is shown to be a real
discriminator before being shown inert at k = 6: (C4) excludes the 20 all-ternary orbits at k = 6 (m6);
(C5) is a theorem at k = 6 and vacuous at k = 5 (m6); (C6) is UNSAT at `(k,l) = (4,3), (4,4), (5,5)` and
at `(6, l)` would be UNSAT if any node of a chain failed (Sec. 3); (C7) has list sizes down to 1 and is
not implied by (C4) (Sec. 3).
