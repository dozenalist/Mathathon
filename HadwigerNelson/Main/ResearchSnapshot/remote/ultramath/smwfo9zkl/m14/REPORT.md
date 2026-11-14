# The direction-local envelope of §8 at six colours, decided

Member m14, swarm smwfo9zkl, direction d17. Two decision procedures, exact integer arithmetic,
calibrated against the paper's Proposition 8.2 and against an independent previous computation.

## Verdict

The part of the paper's §5–§8 machinery that uses data at a *single direction* (palette bound,
(5.7) at every direction, the §8 sliver restrictions (8.1) at every direction, and the (5.2)
non-coverage at every direction) is **exactly as strong as its six-palette projection on one
π/3-orbit** (Theorem A), and at k = 6 it **excludes no cycle length at all**: it is satisfiable for
every ray geometry at ℓ = 3, 4 and for 225/1296 (ℓ = 5), 177/7776 (ℓ = 6) of them (Theorem C). The
calibration at k = 5 shows why this matters: the same direction-local system leaves **all** triangles
(36/36) and 14 of 216 four-cycle geometries alive, although the paper proves no such cyclic centre
exists at k = 5. So §8's ℓ = 3 and ℓ = 4 exclusions are *not* direction-local: they are carried by
the global machinery (Lemma 5.5 binary-centre separation, Lemma 6.6 continuity of states, Lemma 6.7
step bans), all of which run on the k = 5 palette bound |P| ≤ 2. At k = 6 the triangle argument forces no binary
centre, so the global step has nothing to run on: **§7/§8 cannot be made available at six colours by
the paper's method** (Corollary D).
A further geometric fact (Lemma E) shows that adjoining the true multi-centre point-exclusions,
which are strictly stronger than the unit-translation exclusion the prompt singles out, cannot help
either.

## 1. The direction-local system

Fix a weak measurable k-colouring, a cyclic centre x with simple label cycle T = {0,…,ℓ−1} in cyclic
order, outsiders U = Fin k \ T, and limiting ray directions v_j (paper Proposition 7.1 and §8).
Write R for rotation by π/3 and J for rotation by π/2. For a direction e not perpendicular to any v_j
put σ_j(e) = sign(e·v_j) and, as in Lemma 8.1,

    O(e) = U ∪ { j : σ_{j−1}(e) = σ_j(e) = −1 },
    I(e) = U ∪ { j : σ_{j−1}(e) = σ_j(e) = +1 }.

Then for almost every e ∈ S¹ (Lemmas 5.2, 5.5/Corollary 5.4, 8.1, and Proposition 5.6 in its
general-k form, all at the fixed centre x):

  (D1)  1 ≤ |P_x(e)| ≤ k−3                                        [palette bound]
  (D2)  P_x(e) ∩ O(e) ≠ ∅  and  P_x(e) ∩ I(e) ≠ ∅                 [(8.1)]
  (D3)  P_x(e) ∩ P_x(Re) = ∅                                       [(5.7)]
  (D4)  P_x(e) ∪ P_x(v) ≠ Fin k  for a.e. non-parallel pair (e,v)  [(5.2)]

I call a measurable P: S¹ → 2^{Fin k} satisfying (D1)–(D4) a *direction-local palette field*.
The combinatorial data is the cell vector c ∈ {0,…,5}^ℓ with v_j at angle 60(c_j+1)° (c_0 = 0 is a
global rotation of the whole picture, a symmetry of the system).

## 2. Theorem A (the field is six palettes)

**Theorem A.** For every k ≥ 5, every ℓ ∈ {3,…,k} and every ray geometry c there is a direction-local
palette field if and only if the six-palette orbit system

  (E1) 1 ≤ |P_t| ≤ k−3,  (E2) P_t meets O(a_t) and I(a_t),  (E3) P_t ∩ P_{t+1} = ∅ (t mod 6)

is satisfiable, where a_0,…,a_5 are the six directions of one R-orbit. If a field exists, one exists
taking at most two labels per palette, i.e. with |P_x(e)| ≤ 2 everywhere.

*Proof.*
(i) *Sign data is constant on 30° cells.* σ_j changes only where e ⊥ v_j, i.e. at angle
θ_j + 90° = 60(c_j+1) + 90° = 30(2c_j+5)°, an odd multiple of 30°. Hence the twelve open 30° cells
carry constant sign vectors, and the sign data therefore has at most six distinct values on the arcs
between consecutive perpendicular directions. All those arcs are unions of 30° cells and the
partition into 30° cells is invariant under R (which shifts a cell by +2). So the field may be taken
constant on 30° cells; call the resulting 12-tuple (P_0,…,P_11).
(ii) *Reduction to one parity class.* R maps cell i to cell i+2, preserving parity. The R-orbit of a
direction in cell i therefore meets exactly the six cells i, i+2, i+4, i+6, i+8, i+10. Restricting a
field to that orbit gives a solution of (E1)–(E3) for the ℓ-arc data of those six cells, because
O,I are constant on them. Conversely, a solution of (E1)–(E3) on one parity class, repeated on the
other class, is constant on cells and satisfies (D1)–(D3); it satisfies (D4) as soon as every
palette has at most two labels, since 2+2 = 4 < 5 ≤ k.
(iii) *Shrink.* A palette of size ≥ 3 that meets O and I contains a subset of size ≤ 2 meeting both:
take one element of P ∩ O ∩ I if that is non-empty, otherwise one element of P ∩ O and one of
P ∩ I. Subsets inherit disjointness, so (E1)–(E3) survive. ∎

*Parity.* The two parity classes are not independent duties: the sign changes sit at *odd* multiples
of 30°, so cells 2t+1 and 2t+2 always carry the same sign vector, and the hit sequence of the odd
class is the hit sequence of the even class cyclically rotated by one. An exact check over all 10872
instances (k = 5,6; ℓ = 3..k; every geometry) finds zero violations. Since the cycle system is
invariant under cyclic relabelling, the two parities have the same satisfiability, as they must.

Theorem A settles the question left open in the previous swarm's report ("I did not decide the full
one-centre palette field at ℓ = 5,6"): the field verdict *is* the orbit verdict, for every ℓ.

## 3. Theorem B (the exact counts)

Twelve cells, constraints (D1)–(D3) on each parity class (equivalently the system (E1)–(E3) of
Theorem A). Procedure A: recursive search over the six positions with incremental bitmask checks,
signs from an exact integer residue table. Procedure B: independent implementation that re-derives
O and I from actual cosines at three interior angles of every cell (floating point, guarded by
|cos| > 0.05), a different palette representation, and a forward reachability DP instead of a DFS.
The two agree on **every** instance (10872 comparisons).

A further check confirms Theorem A(iii) numerically: replacing the size bound 1 ≤ |P| ≤ k−3 by
1 ≤ |P| ≤ 2 leaves every count in the table unchanged (checked for all rows below). Hence the
non-coverage constraint (D4) is automatically satisfied by the surviving models, and the table is
also the verdict for the full direction-local system (D1)–(D4).

| k | ℓ | geometries | satisfiable |
|---|---|---|---|
| 5 | 3 | 36 | **36** |
| 5 | 4 | 216 | **14** |
| 5 | 5 | 1296 | **0** |
| 6 | 3 | 36 | **36** |
| 6 | 4 | 216 | **216** |
| 6 | 5 | 1296 | **225** |
| 6 | 6 | 7776 | **177** |
| 7 | 3 | 36 | 36 |
| 7 | 4 | 216 | 216 |
| 7 | 5 | 1296 | 1296 |
| 7 | 6 | 7776 | 2593 |
| 7 | 7 | 46656 | 4109 |

Calibration and non-vacuity:
* k = 5, ℓ = 5 gives 0/1296 — this is the paper's Proposition 8.2 (no five-cycle at five colours),
  recovered by the direction-local system alone. Automatic from Theorem A and the sign-word count.
* k = 5, ℓ = 4 gives 14/216 and ℓ = 3 gives 36/36, reproducing an earlier swarm's independent
  computation of the same orbit system, and the k = 7 row 36/216/1296/2593/4109 reproduces that
  computation exactly as well. Two different code bases, identical numbers.
* The systems are not vacuous in the other direction: k = 4 gives 0 satisfiable geometries at
  ℓ = 3, 4 (every triangle and square interface is impossible at four colours) — checked in the
  earlier calibration and consistent with the counts above.

## 4. Theorem C (nothing is excluded at k = 6)

**Theorem C.** At k = 6 and ℓ = 3, 4 every ray geometry admits a direction-local palette field; at
ℓ = 5 225 of 1296 do, and at ℓ = 6 177 of 7776 do. Hence no direction-local argument — using (5.7) at
every direction, the full sliver restrictions (8.1) at every direction, the (5.2) non-coverage at
every direction, and the general-k palette bound — can exclude a cyclic centre of any length at six
colours.

The surviving witnesses are explicit and small (see `counts.json`); e.g. at (k,ℓ) = (6,6) the
geometry c = (0,0,0,3,3,3) is satisfied by six two-label palettes alternating between two disjoint
pairs, and at (6,5) by three singleton outsider palettes and three pairs.

## 5. Corollary D: why §7 cannot be made available at six colours

At k = 5 the paper excludes cycles of length 3, 4, 5. Theorem C's calibration shows that at k = 5
the direction-local system already excludes length 5, but **not** lengths 3 and 4: 36/36 triangles
and 14/216 four-cycles survive it. Therefore

  §8's triangle and four-cycle exclusions are not consequences of direction-local data.

They are carried by global arguments, and each of those arguments uses the k = 5 palette bound
|P| ≤ 2 in an essential way:
* the triangle case: at a triangle centre every palette must meet the *outside pair* of labels,
  which is a set of size k−3 = 2 only at k = 5; the 60° exclusion then makes the centre binary for
  that pair, and Lemma 5.5 (binary centres are uniformly separated) gives local finiteness. At k = 6
  there are three outsiders, no fixed pair is forced, (5.7) therefore yields no alternating
  selection, and Lemma 5.5 cannot be invoked;
* the four-cycle case: at five colours a palette not containing the outsider X has exactly two
  labels and, by (6.2), must be one of the two diagonals, so there are exactly three canonical
  states X, U, V, they alternate by (5.7), and Lemma 6.6 extracts a continuous state. At six
  colours both outsiders may sit in one palette, or one outsider plus one cycle label, or three
  labels: the three-state analysis collapses, and Lemma 6.6's limit step (`two different state
  groups would require at least three palette labels`, excluded at k = 5 by (5.12)) has no k = 6
  analogue;
* the 1-skeleton step of §7 needs |P| ≤ 2 a.e. for a different reason (a point of the metric graph on
  k vertices has at most two positive barycentric coordinates), and (D1) at k = 6 only gives ≤ 3.

So at six colours both prerequisites of §7 fail, and Theorem C shows the first one cannot be
recovered inside the direction-local world. The second (local finiteness of the cyclic locus) is not
a palette statement at all: Γ_x is defined by transition *densities* (6.1), not by palettes, and the
only palette input to Theorem 6.5 is the same |P| ≤ 2 bound.

## 6. Lemma E (the arity bound: why extra two-centre constraints cannot help)

The prompt identifies P_x(f) ∩ P_{x+u}(f) = ∅ (|u| = 1) as the first genuinely two-centre constraint.
The complete two-centre family is larger. For centres z and a point y with 0 < |y−z| < 2, writing
A = (y−z)/2 and d = |y−z|, the two decompositions y = z + e + v with |e| = |v| = 1 are

    e = A ± √(1 − d²/4) · J(y−z)/d ,      v = A ∓ √(1 − d²/4) · J(y−z)/d ,

and (5.2) at z gives, for almost every y,

    c(y) ∉ P_z(e_+) ∪ P_z(e_−).                                    (E)

For a finite set Z of centres the colour of y therefore avoids the union of 2|Z| palettes; this is
strictly stronger than the unit-translation exclusion whenever at least two centres are involved,
and it is a new true constraint. Two complementary facts bound what it can ever prove:

* *Arity.* In one such constraint no three palettes are pairwise forced-disjoint. Forced disjointness
  comes only from (5.7) (one centre, directions 60° apart) or from the unit-translation exclusion
  (unit-separated centres, equal directions). Three of the first kind would need three directions on
  a circle pairwise 60° apart, which do not exist; three of the second kind would need three centres
  pairwise at distance 1 carrying the same direction f, and then the three points z_i + f are
  pairwise at distance 1 and each at distance 1 from y, a K₄ of unit distances in the plane, which
  does not exist (the equilateral dimension of R² is 3). Verified exactly on a catalogue of
  configurations (`arity.py`).
* *Neutrality.* Every finite constraint system built from (a) size bounds, (b) disjointness,
  (c) non-coverage P_1 ∪ … ∪ P_m ≠ Fin k, and (d) hitting conditions P ∩ S ≠ ∅ with the two-subset
  property of Theorem A(iii), is satisfiable iff it is satisfiable with every palette of size ≤ 2.
  (Replace each palette by a subset; disjointness, size bounds and non-coverage are inherited, hits
  are kept.) So a palette constraint can force a three-label palette only via a *three-fold* hitting
  pattern P ∩ S_1, P ∩ S_2, P ∩ S_3 with no two-element transversal — and the plane's geometry
  supplies no such pattern, by the arity fact.

Consequently the whole palette-level programme, single-centre or multi-centre, at finitely many
centres and directions, is satisfiability-neutral at k = 6; this includes (E) and the rotated
branches of (5.3) at every centre distance. A proof of χ(R²) ≥ 7 from this machinery therefore
cannot exist; the a.e. structure of the colouring (which the prompt notes is equivalent to the
problem) is unavoidable.

## 7. Class covered, and what is not claimed

* Covered: the direction-local system (D1)–(D4) at a cyclic centre, for all k ≥ 5, all cycle
  lengths 3 ≤ ℓ ≤ k, and all ray geometries, decided exactly; equivalently, by Theorem A, the full
  one-centre palette *field*.
* Covered: the neutrality statement of Theorem A(iii)/Lemma E for finite systems of the four listed
  constraint shapes.
* Not claimed: anything about χ(R²). The computation decides a relaxation. It does not prove
  χ(R²) ≥ 7, nor χ(R²) ≤ 6, nor local finiteness of the cyclic locus at k = 6 (that is a statement
  about transition densities, not palettes).
* Not claimed: that §8's ℓ = 3, 4 exclusions are *impossible* to prove at k = 6; only that they
  cannot be obtained from direction-local data, and that the paper's global arguments for them use
  the k = 5 bound |P| ≤ 2 in every line.

## 8. Files and commands

All paths relative to `.ultramath/smwfo9zkl/m14/`.

| file | what it is |
|---|---|
| `work/fieldlib.py` | geometry: exact integer sign table, O/I from (8.1), procedure A, witnesses |
| `work/cspB.py` | procedure B: angles re-derived from cosines, reachability DP |
| `work/field12.py` | the 12-cell system with the non-coverage constraint (D4) |
| `work/verify.py` | all six checks (encoding, rotation lemma, counts A = B, shrink, calibration, witnesses) |
| `work/arity.py` | exact geometry of (E): unit decompositions, K₄-freeness, arity of forced disjointness |
| `work/counts.json` | the table plus one re-verified witness per satisfiable instance |

    cd .ultramath/smwfo9zkl/m14/work
    python3 verify.py     # ~3 min; prints the table, exits 0 iff every check passes
    python3 arity.py      # instant; exits 0 iff the K4 and arity checks pass

Both scripts are self-contained (Python 3, no third-party imports) and use exact integer arithmetic
for every satisfiability verdict; floating point appears only as an independent cross-check of the
sign table and of the unit-decomposition identity.
