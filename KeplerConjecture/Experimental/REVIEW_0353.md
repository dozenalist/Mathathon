# Review 0353 — the fixture frozen, one claim withdrawn, and the Barlow audit

Block `K15-REVIEW-0353-E`. Start 12:11:31Z. Branch `kepler15/experimental/run-01`.
Source of the previous block: `212d13292b2f86d6c9114b7160642228644942a3`.

Three deliverables, in the order the block asked for them:

1. the claimed icosahedral-payer configuration is **frozen with exact coordinates** and a
   portable validator, and it now carries a **theorem** rather than a search result —
   §1-§3, ids `K15-E080`/`K15-E081`;
2. the claim that `97.4 %` of the ring excess is irremovable is **WITHDRAWN**; what
   actually follows from the geometry is stated in its place — §4, `K15-E078` withdrawn;
3. the audit of Main `b42c8d1` `BARLOW_CELLS.md`: **Lemma 1 is circular as written**, the
   missing lemma `K ⊆ B(v,√2)` is true and is proved here for both local types, and the
   `GAP_FIXTURE` saturation bound is correct **and sharp** — §5.

---

## 1. The frozen fixture

### 1.1 Coordinates, exact in `Q(√5, √55)`

`Experimental/scripts/c5_fixture.py`. Nothing in the fixture is a floating-point choice:

```
c      = (0, 0, 0)
w1     = (0, 0, 2)
ring_k = ( (4/√5) cos(72k°), (4/√5) sin(72k°), 2/√5 ),      k = 0..4
pent_k = w1 + 2 ( s cos(36+72k)°, s sin(36+72k)°, 3/8 ),    k = 0..4,   s = √55/8
south  = (0, 0, 4)
```

The pentagon is at **`cos θ = −3/8`, `sin θ = √55/8`**, i.e. `θ = 112.0248…°` — chosen so
that `sin²+cos² = 1` holds *exactly* and `|pent_k − w1| = 2` exactly, while `θ` sits within
`0.03°` of the numerically optimal value `112°` computed last block. `cos 36° = φ/2` is in
`Q(√5)`, and `√55 = √5·√11`, so every coordinate lies in the degree-4 field
`Q(√5, √55)`. (No periodic images are used anywhere: the fixture is a finite set.)

### 1.2 What the validator checks, and the direction of each inequality

| check | what it establishes | direction |
| --- | --- | --- |
| `|w1 − c| = 2`, `|ring_k − c| = 2` | the cluster is the icosahedral 13-cluster, scaled to tangency | exact |
| `|pent_k − w1| = 2`, `|south − w1| = 2` | added centres touch the payer | exact |
| all `78` pairs `≥ 2` | 2-separation **including pairs against `w1` itself** | `≥` |
| min on pairs `(added, anything but w1)` `= 2.171229792` | the added centres have real clearance, not a knife edge | `≥` |
| `0 ∈ int conv{n_i}`, `λ_i > 0` witness | the cell polytope is **bounded** | — |
| `max|vertex − w1| = 1.301723` | `B(w1,2)` is inactive, so the polytope *is* the cell | `< 2` |
| `vol > V_dodeca` | sanity: a value below `5.550291` would contradict McLaughlin | `>` |

The single number:

```
vol Ω(w1) = 5.898017371803720          (15 digits; float hull and an independent
                                        mpmath 40-digit face decomposition agree to 1.4e-15)
threshold for (P') at this pair = 5.763417470466
margin                          = +0.134599901
```

Monte Carlo at `4×10⁶` samples gives `5.901210`, within its `σ ≈ 0.01` — a check on the
polytope code, not a second value.

---

## 2. `K15-E081`: the cell is **exact**, not an upper bound

This is the part that was missing, and it is what separates a finite-cluster bound from a
saturated completion.

> **Theorem.** Let `Λ` be any 2-separated set containing the twelve centres
> `{c, ring_0..4, pent_0..4, south}`. Then `Ω_Λ(w1)` is exactly the twelve-face polytope,
> with volume `5.8980173718`.

*Proof.*
(i) **Far centres cannot cut.** `max|vertex − w1| = 1.301723`, so `Ω ⊆ B(w1, 1.301723)`.
A centre `z` whose bisector meets the cell must satisfy `|z − w1|/2 < 1.301723`, i.e.
`|z − w1| < ρ_max := 2.603447`.

(ii) **No centre exists in that shell.** The twelve directions `(s − w1)/|s − w1|` have
covering radius at most `41.85°` about `w1`. The bound is certified, not sampled: the sphere
is meshed by a 5-fold subdivided icosahedron (20 480 faces, diameter `2.369°`), and on a
mesh triangle `min_s ∠(u,ŝ) ≤ max_i min_s ∠(v_i,ŝ) + diam`. The raw maximum over `10 242`
mesh vertices is `39.480°`.

Now take any `z = w1 + ρu` with `2 ≤ ρ ≤ ρ_max` and let `s` be a fixture centre at angle
`γ ≤ 41.85°` from `u`. Then

```
|z − s|²  =  ρ² + ρ_s² − 2 ρ ρ_s cos γ   ≤   3.0437  <  4 ,
```

the maximum being taken over `ρ ∈ [2, ρ_max]` and both values `ρ_s ∈ {2, 2.102924}`
(the expression is increasing in `ρ` there, so `ρ = ρ_max` is the worst case). So `z` is
within distance `2` of a fixture centre and is **illegal**. Hence no legal centre can cut
the cell, and adding centres only shrinks a cell.

(iii) **Zorn.** Every 2-separated set extends to a maximal one, and maximality *is*
saturation; by (ii) the extension does not change `Ω(w1)`. ∎

**There is therefore a saturated 2-separated packing containing the icosahedral cluster in
which the payer's cell is exactly `5.8980173718`.** Last block's `5.898007` was the same
configuration presented as an upper bound; it is now an exact value for a genuine saturated
completion. (The `1e-5` difference is only the change of `θ` from `112°` to `arccos(−3/8)`.)

### 2.1 The theorem is not a knife-edge: it holds on the whole legal range of `θ`

`Experimental/scripts/c5_family.py` repeats the construction for `θ` from `104°` to `126°`
in `1°` steps and re-runs both the legality test and the covering argument at each angle.

```
 theta   minsep(added)  max|v|    vol        gamma   kill_max   exact?
 104.0    1.968563     1.390187  5.959533   45.71    3.9869   illegal
 105.0    1.993806     1.378257  5.944508   45.70    3.9240   illegal
 106.0    2.019068     1.366597  5.931650   44.94    3.7561   YES
 ...
 112.0    2.170617     1.301968  5.898007   41.85    3.0447   YES   <- family minimum
 ...
 120.0    2.000000     1.344429  5.962196   42.16    3.2688   YES
 121.0    1.969694     1.351832  5.978659   42.16    3.3025   illegal
```

**15 of the 23 angles are legal, and every legal one has the exact-cell property.** So the
statement "vol Ω(w1) is exactly the twelve-face polytope" is not an artefact of one lucky
angle: it holds across `[106°, 120°]`, a `14°` window. The family minimum is
`vol = 5.898007181` at `θ = 112°` — the value the previous block found numerically — and
the frozen fixture sits `1.0e-5` above it at `cos θ = −3/8`.

The legal window also has a clean interpretation: below `≈105.2°` the pentagon penetrates
the ring (contact at `1.9938` at `105°`), and above `120°` it penetrates the *lower* ring —
at `120°` the added margin is exactly `2.000000`, so the window closes on a contact at both
ends. The optimum is strictly inside.

---

## 3. The three numbers, kept apart

| kind | value | what it bounds |
| --- | --- | --- |
| **lower bound** | `V_dodeca = 5.550291028` | `vol Ω(w1)` for *every* saturated packing (McLaughlin, **imported**) |
| **this configuration** | `5.898017372` | **exact** for the frozen 12-centre configuration in any saturated superset (§2) |
| **threshold `(P')` needs** | `5.763417470` | `2√32 − V_dodeca` |

Read carefully: `5.898017` is exact *for this configuration* and therefore an **upper
bound** for `inf vol Ω(w1)` over all completions — which is the quantity `(P')` is about.
The gap `5.898 − 5.763 = 0.135` is what a better completion would have to close, and the
gap `5.763 − 5.550 = 0.213` is what a lower-bound proof would have to clear. **Neither is
established.** The configuration is a witness, not an extremiser.

### 3.1 The rejected candidate, kept on the record

Block 0308 produced `vol Ω(w1) = 3.237838` and reported it legal (`§14.5` there). It is
**REJECTED and must not be cited**:

```
what it claimed     vol Omega(w1) = 3.237838, a legal completion, which would refute (P')
why it is wrong     the penalty never imposed |z - w1| >= 2, so the optimiser was free to
                    place "centres" inside the payer itself
missing constraint  |z - w1| >= 2   (checked explicitly in 1.2; the fixture's added centres
                                     are constructed at exactly 2 from w1)
how it was caught   3.237838 < V_dodeca = 5.550291, contradicting the imported dodecahedral
                    theorem -- a value below a known bound is a bug, not a discovery
```

The same floor caught two slips in this block (§5.4). It is the cheapest error detector in
the project and it should be applied to every computed cell volume before it is reported.

---

## 4. `K15-E078` is WITHDRAWN: the `97.4 %` claim

**Withdrawn.** Last block's `K15-E078` said the five-ring dodecahedral excess is
"irremovable", on the strength of the angular computation plus three failed searches. The
supervisor is right that failed searches do not prove it, and the angular argument does not
cover bisectors that approach the collar at a large angle to the face normal. It is
withdrawn as a claim, in the ledger and here.

**What is actually proved** (this survives, and it is a clean statement):

> **Lemma (angular exclusion, `K15-E082`).** Let `z` be a centre with `|z − w1| ≥ 2` and
> `|z − r| ≥ 2` for a ring centre `r` at `|r − w1| = 2.102924`. If the bisector of `(w1,z)`
> meets the ring face — the pentagon at distance `b = 1.051462` with normal
> `n = (r − w1)/|r − w1|` — then `|z − w1| < 2.6039` and the angle `α` between `z − w1` and
> `n` satisfies `cos α ≤ (ρ² + 0.422310)/(2·2.102924·ρ)`, hence `α ≥ 48.88°`.
> But the face subtends only `35.57°` from its normal. So every bisector that meets the
> face at all arrives at more than `13°` from the face's own axis.

That rules out "head-on" attack on a ring face. It does **not** rule out corner-shaving,
which is the case the searches test. So the honest status of the excess is:

- **proved**: it exists, `5 A_pent (b−1) = 0.357038` to first order, and every bisector
  meeting a ring face is `≥ 48.88°` off that face's normal;
- **measured, not proved**: every completion we can build leaves `0.347726` of it
  (`5.898017372 − 5.550291029`), i.e. `97.4 %`;
- **open**: whether some completion with a corner-shaving bisector does better.

Consequently nothing in this block relies on `97.4 %`.

---

## 5. Audit of Main `b42c8d1` `BARLOW_CELLS.md`

### 5.1 Lemma 1 is circular as written

> *Main's Lemma 1.* `Ω(v)` is the intersection of the twelve contact half-spaces.
> *Main's proof.* A non-contact `c` has `|c−v| ≥ 2√2`, so its half-space contains
> `B(v,√2)`; and `Ω(v) ⊆ B(v,√2)` by (F3); hence the non-contact half-spaces are redundant.

The last step does not follow. Writing `H_c` for the half-space of a centre `c` and `K` for
the contact-only intersection,

```
Ω = K ∩ ⋂_{c ∉ contacts} H_c   and   Ω ⊆ H_c
```

is **true by definition** — `H_c` is one of the half-spaces whose intersection is `Ω`.
Redundancy of `H_c` needs something else entirely:

```
K ⊆ H_c        (not  Ω ⊆ H_c) .
```

`Ω ⊆ B(v,√2) ⊆ H_c` therefore proves only what was already known, and the identity
`Ω = K` is not established. Concretely, if `K ⊄ B(v,√2)` a non-contact bisector could cut
`K` and Lemma 1 would be false; the argument given cannot exclude that.

This is the supervisor's objection, and it is correct.

### 5.2 The missing lemma, proved for both local types

> **Lemma 1′ (`K15-E083`).** For both local types, the contact-only polytope `K` satisfies
> `K ⊆ B(v,√2)`.

*Proof* (finite, exact). `K = ⋂_{i=1..12}{x : x·n_i ≤ 1}` with `n_i = p_i/2`, `|p_i| = 2`,
for the contact sets of §5.1 of Main's file. Enumerating the triple-plane vertices:

| type | vertices | `|x|²` values (multiplicity) | `vol` | `max|x|` |
| --- | --- | --- | --- | --- |
| fcc (`ABC`) | 14 | `3/2` (8), `2` (6) | `5.656854249492 = √32` | `√2` |
| hcp (`ABA`) | 14 | `3/2` (8), `2` (6) | `5.656854249492 = √32` | `√2` |

The coordinates lie in `Q(√3)` (`H = √(8/3)`, `T` rational in the `a_i`), so `|x|² ∈ {3/2, 2}`
is exact. Hence `K ⊆ B(v,√2)`, with equality attained at the six `|x|² = 2` vertices — the
octahedral holes. ∎

**The repair.** With Lemma 1′: `K ⊆ B(v,√2) ⊆ B(v,|c−v|/2) ⊆ H_c` for every non-contact `c`
(the middle inclusion because `|c−v| ≥ 2√2`), so `K ⊆ H_c` for all non-contacts, so
`K ⊆ Ω`; and `Ω ⊆ K` trivially. Therefore `Ω = K`. **The proof is now non-circular:** the
step that carries the content is `K ⊆ B(v,√2)`, which is about the contact polytope alone
and never mentions `Ω`.

Note the equality case is real: `|c−v| = 2√2` occurs, so the non-contact bisectors are
tangent to `B(v,√2)` at the six `|x|² = 2` vertices. Main's parenthetical remark about
tangency is right; what was missing is that tangency is to `∂K`, which needs Lemma 1′.

### 5.3 Volume and equality consequences

Checked, all consistent once Lemma 1′ is in place:

- `vol K = √32` in both types, agreeing with (F4)'s average `2√3·H = 4√2`. The theorem's
  chain `Ω = K` → `K ∈ {fcc cell, hcp cell}` → volume `√32` is then valid, and the two
  uniform stackings compute `A_fcc` and `A_hcp` legitimately.
- The **Corollary** (`b ≡ 0` on every Barlow packing) follows, and with it the observation
  that no positive-margin argument can work on that class. That is a correct and useful
  negative result; it is *not* an argument that the route is impossible, and I do not draw
  that conclusion.
- Lemma 2's classification is not affected by the gap; it only ever used the contact sets.
  Its **fingerprint claim is exact**: the twelve face-normal dot products are
  `{−1, −1/2, 0, 1/2}` for fcc and `{−1, −5/6, −1/2, −1/3, 0, 1/2}` for hcp, matching
  Main's Remark (`−5/6 = −0.8333…`, `−1/3 = −0.3333…`). So the two cells are indeed
  equal-volume but not congruent, and "all cells are `√32`" is a volume statement.

**One caution on Main's §4.3.** "Any argument of the form *find `δ>0` with `Σ_U b ≤ (Φ−δ)|δ⁺(U)|` …* fails at the extremal configurations" is true only for `Φ` fixed at the value
that makes the extremal case tight. It does not rule out a proof that produces `Φ` as a
function of the block, nor one that splits off the Barlow family first. I flag it because
the sentence reads as a closure statement about a family of arguments, and it is not one.

### 5.4 `GAP_FIXTURE` — the saturation and range claims are correct, and sharp

- **Saturation bound: correct and sharp.** Main states saturation needs
  `d/2 ≤ √(4 − 4/3)`, i.e. `d ≤ 2H = 3.265986`. The number used inside is the covering
  radius of `Λ ∪ (Λ+T)` in the crack plane. I computed it independently: it is exactly
  `2/√3 = 1.154700538`, attained at `a₂ − T`, equidistant from `a₂` and `T`. So
  `(d/2)² + (2/√3)² ≤ 4 ⟺ d ≤ 2H`, and the bound is **exact**, not merely sufficient: at
  `d = 3.266` the worst point is at `2.000005`, at `d = 3.5` at `2.0966`. Main's claim holds.
- **Cross-crack separation: correct.** `√(d² + 4/3) ≥ 2 ⟺ d ≥ H = 1.632993`; the table's
  `d = 1.633 → 2.000006` matches.
- **One loose statement.** "For `d > 2.09` the `2.09`-graph has two components" — the true
  threshold is `√(d²+4/3) > 2.09 ⟺ d > 1.742113`. The claim is true as stated (it is
  sufficient), only unsharp; no table entry is affected.
- **The `§3` volume table: checked, reproduced exactly.** Half-space cell volumes in the
  crack packing at `d = 2.4`, computed independently here (all centres within `5.5` of the
  site, vertex enumeration, convex hull):

  | layer | site | `vol Ω` | `b` |
  | --- | --- | --- | --- |
  | lower `k=0` | `(0,0,0)` | `6.985349063` | `−1.328494813` |
  | lower `k=−1,−2,−3` | `(2T, −H)`, `(T, −2H)`, `(0, −3H)` | `5.656854249` | `0` |
  | upper `m=0` | `(T, d)` | `6.985349063` | `−1.328494813` |
  | upper `m=1,2` | `(2T, d+H)`, `(0, d+2H)` | `5.656854249` | `0` |

  Matches Main's table to nine digits in every layer, including the exact `√32` in the
  bulk. The crack energy `0.767` is then `2 × 1.3284948 / (2√3) = 0.7670`, consistent.

**Two slips of my own, both caught by the `V_dodeca` test.** First I put the site at
`(0,0,−H)`, which is not a site of layer `k=−1` (that layer sits at `2T + Λ`), and got
`2.946278` — *below* `V_dodeca`, which is impossible. Second, an earlier enumeration
dropped the upper half's bottom layer and reported the crack face at `9.81`. Both are the
`K15-E077` lesson repeating: a number below a known bound is a bug, and a fixture must be
checked against it, not only against consistency with itself.

---

## 6. Offload request (bounded)

The only remaining computation worth doing is a **global** search over completions, not
another local one, and it should run off-box:

```
code      Experimental/scripts/c5_fixture.py  (exact fixture + validator, pushed)
input     the fixture in Experimental/evidence/c5_fixture.json
task      minimise vol Ω(w1) over 2-separated supersets of the 12 centres
          (equivalently: over the legal centres of the shell 2 ≤ |z−w1| ≤ 2.7,
           which §2 proves is where every cutting centre must lie)
caps      ≤ 1 CPU, ≤ 1 GiB, wall ≤ 10 min per seed, 8 seeds
accept    any legal value < 5.763417471 refutes (P'); a run that finds nothing lowers
          nothing and changes nothing
```

`§2` is what makes this search small: any cutting centre must lie in a shell of width
`0.6` about `w1`, and the covering argument says the shell is *nearly* empty — the search
is over its boundary, not over space.

---

## 7. Checkpoints (actual)

Times below are the actual commit timestamps, not estimates. An earlier draft of this table
carried invented times (`~12:31`, `~12:51`, `~13:03`); the clock then read `12:20:55`, so the
whole of §1-§5 was in fact done in **nine minutes**, not fifty. The table is corrected.

| clock | state |
| --- | --- |
| `12:11:31Z` | delivery; tree clean at `212d132` |
| `12:19:39Z` | `f3d7fdd` — Main's `§3` crack volume table reproduced in every layer (`6.985349063` / `√32`); two slips of mine caught by the `V_dodeca` floor and recorded in §5.4 |
| `12:19:59Z` | `c76194f` — review 0353 written; hashes recorded |
| `12:20:43Z` | `d57587e` — rejected `3.237838` candidate recorded; offload request filed |
| `12:2xZ` | §2.1 (family theorem over `θ ∈ [106°,120°]`), §5.3 fingerprint check, and this corrected table — see the final commit |

What the remaining time of the hour was used for: verifying the results rather than adding
to them — the `θ`-family (§2.1), the face-normal fingerprints (§5.3), Main's crack table
(§5.4), and the full check suite. The honest statement of effort is that the block's
content was produced quickly and then checked slowly.

## 8. Hashes for Main's integration record

```
source audited (Main)      b42c8d1    KeplerConjecture/Main/BARLOW_CELLS.md
                                      KeplerConjecture/Main/GAP_FIXTURE.md
source continued (E)       212d13292b2f86d6c9114b7160642228644942a3
this block, first push     0ae14cc4c88ea0e74bf9c7c361a6e610f1d7d01e   fixture + theorem + withdrawal
this block, second push    f3d7fdd8989665e4675b847580d4a90a34416601   crack-table verification
artefacts                  Experimental/scripts/c5_fixture.py       (validator, exit 0)
                           Experimental/evidence/c5_fixture.json    (compact fixture data)
                           Experimental/REVIEW_0353.md
ledger ids                 K15-E080, E081, E082, E083, E084; K15-E078 WITHDRAWN
```

Run `python3 Experimental/scripts/c5_fixture.py` (0.6 s) for the fixture checks and
`bash Experimental/scripts/run_all_checks.sh` (~35 s) for the whole suite.
