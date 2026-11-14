# Hales, *A Proof of the Kepler Conjecture (unabridged)* — summary and reading map

Source: `attachments/i-ve-attached-thomas-4iws/proof_kepler.pdf`
(Thomas C. Hales, 14 November 2005, 339 pp., "fullkepler").

## What the document is

Six papers bound as one volume, each with its own bibliography:

| Paper | Title | Chapters |
|---|---|---|
| I | Historical Overview of the Kepler Conjecture | 1–2 |
| II | A Formulation of the Kepler Conjecture | 3–7 |
| III | Sphere Packings III. Extremal Cases | 8–10 |
| IV | Sphere Packings IV. Detailed Bounds | 11–14 |
| V | Sphere Packings V. Pentahedral Prisms (Ferguson) | 15–17 |
| VI | Sphere Packings VI. Tame Graphs and Linear Programs | 18–25 |

This is the long version of the proof. The compressed published version is
[Hal05a] (Annals of Mathematics 162 (2005)); the code, data, the archival list
of tame graphs and the machine-checked inequalities are in [Hal05b]
(`annals.math.princeton.edu/keplerconjecture/`). Every computer-proved
inequality in the text is cited by a nine-digit identifier `calc-XXXXXXXXX`
that resolves to an entry in that archive.

## Formulation

Kepler: no packing of congruent balls in R^3 has density greater than
pi/sqrt(18) ~ 0.74048, attained by the face-centered cubic (fcc) packing.

Normalise to unit balls. A packing is *saturated* if no further ball fits.
For a centre v let Omega(v) be its Voronoi cell. The whole proof rests on one
lemma (Lemma 3.3): if A : Lambda -> R is

1. **negligible**: sum over Lambda cap B(x,r) of A(v) <= C r^2, and
2. **fcc-compatible**: vol Omega(v) + A(v) >= sqrt(32) for every v,

then the local density satisfies delta(x,r,Lambda) <= pi/sqrt(18) + C/r.
sqrt(32) ~ 5.657 is the Voronoi volume in fcc and in hcp. So it is enough to
exhibit a correction term A that (a) never lets the corrected volume drop below
the fcc value and (b) does not accumulate over large balls.

`vol Omega(v) + A(v)` is the "corrected volume" of a Voronoi cell.

## The logical skeleton (Section 3.3)

Six claims, each proved somewhere in the volume:

| Claim | Content | Proved in |
|---|---|---|
| 3.11 | max sigma = 8 pt on DS implies a negligible fcc-compatible A exists | Thm 7.14 |
| 3.12 | a contravening star's plane graph is tame | Thm 20.20 |
| 3.13 | every tame graph is on the archival list | Thm 19.1 |
| 3.14 | every archival graph is fcc, hcp or pentahedral prism | Thm 23.1 |
| 3.15 | no contravening star has the pentahedral-prism graph | Thm 3.10 (Paper V) |
| 3.16 | fcc and hcp score exactly 8 pt, and are the only maximisers | Cor 8.3 |

Lemmas 3.17–3.20 assemble these into the Kepler conjecture. The strategy is
proof by contradiction: a *contravening* star is one with sigma(D) >= 8 pt, and
every subsequent statement is really "no contravening star has property X".

## The argument in six moves

**1. Reduce to one cell (Ch. 3).** Lemma 3.3 above. The cost is that the
correction A must be built out of local data only.

**2. Discretise space (Ch. 4–7).** All decisions are made inside distance
2 t_0 = 2.51 of a centre. Two structures do the work:

* the **Q-system**: non-overlapping simplices with vertices at packing centres —
  *quasi-regular tetrahedra* (all six edges <= 2.51) and *quarters* (one
  "diagonal" edge in [2.51, 2 sqrt 2], the other five <= 2.51). It is a hybrid
  of the Delaunay decomposition (where sharp bounds are needed) and the Voronoi
  decomposition (where crude bounds suffice), and deliberately does *not*
  partition space. The constant 2.51 is where a tetrahedron with five edges 2
  and a sixth edge x drops below the octahedral density delta_oct ~ 0.72; it is
  rounded up from x_0 ~ 2.504.
* **decomposition stars** D(v,Lambda): the cluster of centres within 2 t_0,
  together with combinatorial markings (which simplices are tetrahedra or
  quarters, flat vs upright quarters, etc.). The space DS of all of them is
  compact and embeds in a finite-dimensional Euclidean space, and a star
  determines its own Voronoi cell.

**3. Turn the problem into one finite-dimensional maximum (Ch. 7).** Define a
continuous *score* sigma : DS -> R, a linear function of
vol Omega(D) + A_0(D), normalised so that fcc-compatibility becomes
sigma(D) <= 8 pt. Here

* pt = 4 arctan sqrt(2/5) - pi/3 ~ 0.05537 is the score of a regular
  tetrahedron of edge 2 (so "pt" = "point");
* 8 pt ~ 0.442989.

> **Theorem 3.7 (finite-dimensional reduction).** max over DS of sigma = 8 pt.

**4. Local optimality (Ch. 8).** The fcc and hcp stars score exactly 8 pt.
A vertex of either packing has 8 quasi-regular tetrahedra and 6 quad clusters:
each tetrahedron scores <= 1 pt, with equality only for the regular tetrahedron
of side 2 (Lemma 8.10, `calc-586468779`), and each quad cluster scores <= 0,
with equality only for a flat square of side 2 (Theorem 8.4). The estimates chop
clusters into *Rogers simplices* and invoke Rogers's monotonicity lemma to show
each piece has density at most delta_oct.

**5. Contravention forces a tame graph (Ch. 20–22).** Radial projection of the
star to the unit sphere gives a plane graph G(D): vertices are the balls within
2 t_0, faces are the "standard regions" (with aggregates merged). Such a graph
must be **tame**, i.e. satisfy eight conditions (Ch. 18.3): face lengths 3..8;
every 3-circuit is a face or the opposite of a face; 4-circuits lie on an
explicit list; degrees 2..6; no
degree-6 vertex on a face of length >= 5; sum over faces of c(len F) >= 8;
existence of an *admissible weight assignment* of total weight below the target
tgt = 14.8 (~ 4 pi zeta - 8 ~ 14.7947); and no two adjacent vertices of type
(4,0). The tables a(n), b(p,q), c(n), d(n) encode the numerical score bounds as
combinatorial data.

**6. Classify, then eliminate (Ch. 19, 23–25).** Tameness is local and finitely
checkable, so a computer enumerates *all* tame graphs: states are isomorphism
classes of partial plane graphs, transitions glue in "patches", and pruning
rules (bounded face length, weight already above target, canonical ordering of
vertex types) keep the search finite. The output is an archival list of some
five thousand graphs. For each graph G, the nonlinear problem "maximise sigma
over DS(G)" is relaxed to a linear program in variables

    alpha(v,F) interior angles, sigma(F) face scores, sol(F) solid angles,
    tau(F), y(v) heights, e(v,w) edge lengths

subject to the exact identities (angles at a vertex sum to 2 pi;
sol(F) = sum alpha - (len F - 2) pi; tau = sol zeta / pt - sigma) plus a large
family of linear inequalities that are themselves theorems proved by interval
arithmetic. An LP maximum below 8 pt kills G. When one LP is too weak, branch
and bound splits DS(G) (triangles by perimeter 6.25; quadrilaterals into flat /
quartered-octahedron / mixed; then pentagons, hexagons, upright diagonals, flat
quarters, loops, gaps, penalties), producing on the order of 10^5 linear
programs of 100–200 variables and 1000–2000 constraints. Only three graphs
survive: fcc, hcp, and the pentahedral prism, the last eliminated separately by
Ferguson (Paper V).

Then Lemma 3.3 closes the proof, and Theorem 3.9 gives the uniqueness statement:
the maximisers of sigma are exactly the fcc and hcp kissing arrangements, and any
packing all of whose stars are of these types is built from hexagonal layers
(Paper I, Section 1.1). Since density ignores bounded perturbations, that is the
strongest uniqueness that can hold.

## Tools, and why they count as proof

1. **Interval arithmetic** (Ch. 17). IEEE 754 with directed rounding; intervals
   are manipulated with outward-rounded +, -, *, / and monotone functions;
   arctan gets padding epsilon = 2^-49. Subdivision into cells plus
   partial-derivative sign tests handles the points where an inequality is
   tight (g(y_0) = 0). Because naive interval bounds blow up, the decisive
   trick is explicit *second (mixed) partial* bounds plus Taylor expansion
   (Calculations 17.4.6.1–8). This is rigorous: the interval encloses the true
   value, unlike bare floating point.
2. **Finite-state-machine enumeration and isomorphism testing** (Ch. 19), with
   numerical vertex invariants to reject non-isomorphic duplicates.
3. **Linear programming**: CPLEX, with an a posteriori certificate — if the
   numerically obtained dual solution z gives p pt + z.b < 7.9999 pt with
   constraint error epsilon < 10^-8, then sigma < 8 pt (Section 23.4).
4. **Branch and bound** (Ch. 25) for the tame graphs that a single LP cannot
   kill.
5. Nonlinear and symbolic optimisation packages for exploration (cfsqp is
   credited in Section 2.5).
6. Logistics: "a few gigabytes of code and data", organised and archived at
   [Hal05b], cited by `calc-` identifiers.

What this does *not* do is shrink the trusted base to nothing: it shifts it to
the correctness of the code, the compiler, and the archived data. That is the
gap the Flyspeck formalisation (HOL Light + Isabelle, completed 2014) later
closed; it postdates this document and is not among its references.

## Reference map (for orientation)

**Prehistory.** Kepler's 1611 *Strena* [Kep66]; Hariot's cannonball-pile
tables for Raleigh, his fcc/hcp distinction, and the "Pascal's triangle before
Pascal" diagram [Shi83, Mas66, Kar66]; the earliest written trace of the
triangular-pile count, Aryabhata's 499 CE *Aryabhatiya* with Bhaskara's 629 CE
commentary, translated by Plofker [Plo00].

**The modern problem.** Hilbert's 18th problem [Hil01] and Milnor's review
[Mil76] ("a scandalous situation since the correct answer has been known since
the time of Gauss").

**Kissing numbers.** Newton vs Gregory on 12 vs 13; the 19th-century "proofs"
[Ben74, Gun75, Hop74] and Boerdijk [Boe52] are not rigorous; the first proper
proof is Schutte–van der Waerden [SW53], with an elementary proof by Leech
[Lee56]. Fejes Toth made a quantitative Newton–Gregory estimate the first step
of his program [Fej53]; the same circle of ideas appears here as the conclusion
(Theorem 3.9) that a maximising star has exactly 12 centres within 2.51.

**Density bounds.** Blichfeldt 0.884, 0.835 [Bli19, Bli29]; Rankin 0.828
[Ran47]; Rogers 0.7797 [Rog58]; Lindsey 0.77844 [Lin86]; Muder 0.77836 and
0.7731 [Mud88, Mud93]. Rogers's monotonicity lemma and simplex decomposition
are used directly (Rogers simplices, Ch. 8); the function tau measures departure
from Rogers's bound; Muder's use of the full Voronoi cell is the step that makes
the modern approach possible.

**The dodecahedral conjecture.** [Fej42] implies density <= 0.755 and was
Fejes Toth's route in; he left one estimate ("relied to some extent solely on
intuitive observation") which resisted until McLaughlin [McL98]; see Bezdek
[Bez97]. This is why a single Voronoi cell cannot prove Kepler: one must average
over clusters of cells.

**Fejes Toth's program.** [Fej53, Fej64]: weighted averages of up to 13 Voronoi
cells, and the first proposal to use computers — the direct ancestor of the
present finite-dimensional reduction.

**A claimed proof that failed.** Hsiang [Hsi93a-c, Hsi02] and the responses
[CHMS94, Hal94, Hsi95, Fej95, Bez97, Mud97]; popular account in Szpiro [Szp02].

**Lattices and neighbours.** Lagrange and Thue in the plane [Thu92, Thu10]
(Thue's rigour questioned by Szpiro); Gauss for the fcc lattice in 3D [Gau31];
Korkine–Zolotareff in dimensions 4–5 and Blichfeldt in 6–8 [KZ73, KZ77, Bli35];
Cohn–Kumar in dimension 24 [CK04]. Adjacent optimisation problems (Tammes,
Lennard-Jones, Coulomb) in Section 2.3: Melissen [Mel97], Sloane–Hardin–Duff–
Conway [SHDC95], global optimisation background [HPT95].

**Surveys.** Conway–Sloane [CS93], G. Fejes Toth [Fej97], Rogers [Rog64],
Pach–Agarwal [PA95], Goodman–O'Rourke [Goo97].

**Hales's own chain.** Early work [Hal92, Hal93]; the five-step program
[Hal97a, Hal97b]; mid-stream correction [FH98]; steps III–VI [Hal98b, Hal98c,
Hal98d]; Ferguson's thesis [Fer97]; expository writing [Hal00] *Cannonballs and
Honeycombs* and [Hal03] *Some algorithms*; resources [arXiv, Hal05a, Hal05b].

## Suggested reading order

1. Paper I, Sections 1 and 2 — history, and the honest account of what was
   tried and abandoned (the origin of 2.51 and of the "quarters").
2. Chapter 3 — the whole proof on ten pages.
3. [Hal00] *Cannonballs and Honeycombs* — prose version for a general audience.
4. Chapter 8 — why fcc and hcp win locally.
5. Chapters 18 and 23 — how the machine part is organised, and what an LP bound
   actually certifies.
6. Chapter 17 — the proof technique behind every numerical claim.
7. Chapter 19 and Chapter 25 — the search and the branching, if you want the
   combinatorics.
