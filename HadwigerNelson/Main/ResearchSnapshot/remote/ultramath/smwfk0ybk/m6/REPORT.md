# Step 1 decided: the tightened interface CSP at k = 6 is SATISFIABLE at every length

Member m6, direction d1. Exact computation, two independent decision procedures, machine-checked
core, and the hypothesis audit of the induction lemma. `k = 6`, labels `Fin 6`. Procedure A is
exact integer arithmetic throughout; procedure B evaluates `cos` at multiples of `pi/3` (values
`+-1/2`, `+-1`, guarded by `|cos| > 0.4`) and is used only as an independent cross-check.

## 0. Verdict

| l | geometries (rotation-normalised) | (C1)-(C3) SAT | **(C1)-(C5) SAT** |
|---|---|---|---|
| 3 | 36 | 36 | **36** (every geometry) |
| 4 | 216 | 216 | **216** (every geometry) |
| 5 | 1296 | 225 | **225** |
| 6 | 7776 | 177 | **177** |

* **Step 1's decisive question answers SAT, not UNSAT**: at every `l in {3,4,5,6}` some — indeed at
  `l = 3, 4` every — `(l, sign matrix)` pair has a model, and the SAT sets are *identical* to the
  (C1)-(C3) ones. Hence Step 1 does not prove `chi(R^2) >= 7`; the computation gives the opposite,
  and no `(C4)+(C5)`-style tightening of the state level can change it.
* **Why — a theorem, not a coincidence** (`TightCore.lean : sat_tight_iff_sat_plain`). For every
  `k >= 5`, every `l` and every sign matrix, (C1)-(C5) is satisfiable iff (C1)-(C3) is, and the
  direction `(C1)-(C3) => (C1)-(C5)` yields a model with all `|P_i| <= 2` (§2). Mechanism: shrink
  each palette to at most two labels, keeping one from `P_i inter O_i` and one from `P_i inter I_i`;
  disjointness is inherited, and (C4), which at `k = 6` mentions only 3-sets, plus (C5) then hold
  vacuously. So *no* condition on ternary palettes can ever decide `k = 6` at this level.
* **Machine-checked form, with no enumeration**: for every `k >= 4` and every `l` with `l + 2 <= k`,
  and every sign matrix, the alternating two-outsider assignment `{u_0}, {u_1}, {u_0}, ...`
  satisfies (C1)-(C5) — `TightCore.lean : state_level_silent`. At `k = 6` that covers `l = 3, 4`
  for *all* ray geometries. For `l = 5, 6` the witnesses are also machine-checked
  (`model_five`, `model_six`).
* **Terminal outcome.** None of L1-L5 is reached by this step. It supplies L4's **third ingredient**
  exactly: a *proposed replacement mechanism* — augment the state level with (C4)+(C5) — whose
  hypothesis set is not contained in (C1)-(C3) (S1's letter: (C4) excludes the 20 all-ternary orbit
  patterns, (C5) excludes `sigma(E_x) > pi`), and which is `k`-sensitive in the right place (S3's
  letter: (C4) is vacuous for `k <= 5` because then `|P| <= k-3 <= 2`, and non-vacuous at `k = 6`),
  yet which cannot conclude: it fails S1's *test* (m5's Theorem 4 models survive it **unchanged**)
  and it violates S5 (it binds only palettes of size 3). It also extends L4's no-go from
  (C1)-(C3) to (C1)-(C5) and to the one- and two-further-centre systems of §5.
* **Second defect, independent of the above** (details in `INDUCTION.md` §3): the induction
  lemma's premise (H7) — Proposition 7.1's cycle extraction — is **not available at k = 6**. §6 of
  the paper makes the cyclic-centre locus locally finite via `|P| <= 2` (p.34), which is exactly the
  `k - 3 = 2` step, and §7's cover obstruction is multiplicity-2 only (m3's COVER NO-GO). So even
  an UNSAT answer would not have given `chi >= 7` without new work on (H7).

---

## 1. The decision: instance specification

Positions `i in Z/6` are the six directions `e_i = R^i e` of one `pi/3`-orbit at one centre `x`;
`R` = rotation of directions by `pi/3`. A ray geometry is a cell vector
`c in {0,...,5}^l` with `c_0 = 0` (global rotation is a symmetry; verified that the unnormalised
`6^l` count is exactly `6x` the normalised one), and

    SIG[i][j] = sign(cos((c_j + 1 - i) pi/3))          (no zeros),
    O_i = U union {j : SIG[i][j-1] = SIG[i][j] = -1},
    I_i = U union {j : SIG[i][j-1] = SIG[i][j] = +1},   U = Fin 6 \ {0,...,l-1}  (paper (8.1))

Constraints on `P_0,...,P_5 subset Fin 6`:

    (C1) 1 <= |P_i| <= 3          (C2) P_i meets O_i and I_i          (C3) P_i cap P_{i+1} = empty
    (C4) no two of the P_i are complementary 3-sets                    (C5) <= 3 of the P_i are ternary

**Procedure A** (`tight_csp.py`): depth-first search over the six positions, every constraint
checked incrementally, bitmask encoding of labels.
**Procedure B** (`tight_csp_indep.c`): C, no shared code; a forward reachability DP over the state
set `(last palette, bitmask of the ternary triples used so far)` iterated from each first palette;
`O_i`, `I_i` re-derived from the *actual* ray angles `cos(theta_j - i pi/3)` with an explicit
`|cos| > 0.4` guard instead of from the algebraic table.
**Agreement**: identical SAT/UNSAT on all 9324 instances (`compare_ab.py`), and the predicate is
invariant under the reflection `c -> -c` of the geometry (`verify_tight.py` CHECK 4).

**Independent encoding check** (`verify_tight.py` CHECK 1): `O_i`, `I_i` recomputed from three
interior ray angles per cell (`theta = (c_j+1) pi/3 + delta`, `delta in {-pi/12, 0, pi/12}`, where
`|cos| >= cos(5 pi/12) > 0.25`); 27972 (geometry, angle) pairs, 0 mismatches; the sign vector is
confirmed constant on each cell.

**Calibration** (`calibration.py`) — the same code with the label count changed reproduces known
theorems, so the encoding is not vacuous:

    k = 4:  l=3  0/36,   l=4  0/216        (INTERFACE-NOGO Thm 2: state level complete)
    k = 5:  l=3 36/36,   l=4 14/216,  l=5 0/1296   (l = 5 is the paper's Prop 8.2)
    k = 6:  36, 216, 225, 177              (m5's table, reproduced exactly)

---

## 2. Why the tightening is inert: a theorem, not an observation

**Theorem** (`TightCore.lean : sat_tight_iff_sat_plain`). For every `k >= 5`, every interface length
`l` and **every** sign matrix, the tightened system (C1)-(C5) is satisfiable if and only if the plain
system (C1)-(C3) is. Moreover the direction `(C1)-(C3) => (C1)-(C5)` produces a model with
`|P_i| <= 2` for all `i` (`TightCore.lean : tight_of_plain`).

*Proof (computational content checked exhaustively, then formalised).* Let `P` be a model of
(C1)-(C3). For each `i` the palette `P_i` meets `O_i` and `I_i`; replace `P_i` by
`{c}` if some `c in P_i inter O_i inter I_i`, and otherwise by `{a, b}` with
`a in P_i inter O_i`, `b in P_i inter I_i`, `a != b`. The result is nonempty, of size `<= 2 <= k-3`,
still meets both allowed sets, and is a subset of `P_i`, so the cyclic disjointness (C3) is
inherited. A model with no 3-set palette satisfies (C4) (which at `k = 6` mentions only 3-sets:
`A union B = Fin 6` with `|A|, |B| <= 3` forces `|A| = |B| = 3`) and (C5) vacuously. `square`

So the tightening cannot change any satisfiability question, at any length, for any geometry. The
only way a (C4)-type condition could bite at `k = 6` is on palettes of size 3, and every (C1)-(C3)
model can be shrunk out of that region. The same coordinatewise shrinking was found independently by
member m10 (board finding d2/f1); I verified it, formalised it, and it is what makes the counts of
§1 *provable* from m5's table rather than merely enumerated.

**Independent confirmation by enumeration.** I also checked the conclusion directly, twice: the
SAT *sets* of (C1)-(C3), of (C1)-(C5) and of the `|P| <= 2` variant are equal at every `l`
(`sets_compare.py`), and every one of the 654 satisfiable cases has an explicit model with all
`|P_i| <= 2` (`verify_tight.py` CHECK 3, `witnesses.json` field `palettes_pair_model`). Sizes of the
surviving models: `l = 3`: six singletons, alternating between two of the three outsiders; `l = 5`:
three singletons (all equal to the outsider) `+` three pairs; `l = 6`: **all six palettes are
pairs**, with `P_{i+3} = P_i`, e.g. cells `(0,0,0,3,3,3)` with palettes
`{1,4}, {2,5}, {1,4}, {2,5}, {1,4}, {2,5}`.

**Field-level remark (l <= k-2).** The alternating two-outsider closed form of
`TightCore.lean : state_level_silent` puts `u_0, u_1 in U subseteq O(f) inter I(f)` for *every*
direction `f` and alternates on the six `pi/3` cells, so it satisfies (8.1) and (5.7) at **every**
direction, not only at the six orbit points. So for `l <= k-2` even the full one-centre palette
*field* is consistent with the paper's constraints.

## 3. Machine-checked core (`TightCore.lean`, Lean 4.33.1 + Mathlib, < 10 s, no `sorry`)

    TightCSP.IsModel            -- literally (C1)-(C5) on six palettes, O_i, I_i from (8.1)
    TightCSP.IsPlain            -- (C1)-(C3) only
    TightCSP.sat_tight_iff_sat_plain, tight_of_plain, exists_small_subset
                                -- §2: the tightening is inert for every k >= 5, l, sigma
    TightCSP.state_level_silent : for all k l with 0 < l, l+2 <= k, k >= 4 and all sigma,
                                  exists P, IsModel k l sigma P
    TightCSP.k6_silent_three_four : l = 3 and l = 4 at k = 6, for every sign matrix
    TightCSP.model_five, model_six : the explicit l = 5 and l = 6 witnesses, decide-checked
    TightCSP.O5_values, I5_values, O6_values, I6_values : the O_i/I_i of the two witnesses,
                                  cross-checked against the Python values
    #print axioms -> [propext, Classical.choice, Quot.sound] for every theorem above

Command: `lean TightCore.lean` (exit 0).

---

## 4. The induction lemma

`INDUCTION.md` contains (IL) and its proof: every weak measurable 6-colouring with a cyclic centre of
length `l` (in the sense of Proposition 7.1) produces, on a conull set of orbit directions, six
palettes satisfying (C1)-(C5) for the sign matrix of its rays. The proof is the intersection of five
conull sets at the single centre `x`; each line is a quoted paper statement, and the audit in §3 of
that file records the one premise that is *not* available at `k = 6` — the cycle extraction (H7).
`INDUCTION.md` §4 states the exact implication that UNSAT would have given, and why it is vacuous
here.

---

## 5. What the surviving models are; what a (C6) must bind

The survivors violate nothing in (C1)-(C5). The unused inputs at one centre are the cross-centre
ones: Lemma 5.2(3) with Remark 5.3 gives

    P_y(f) cap P_x(f) = empty   for a.e. f,   whenever |y - x| = 1.            (5.3b)

I decided the system obtained by adding (5.3b) at further centres, at every orbit direction:

| system | result |
|---|---|
| (C1)-(C5) at `x` | SAT at all four lengths (table above) |
| `+` (C1),(C3),(C4),(C5) at `y = x+a` `+` `P_i cap Q_i = empty` | **SAT for all 654** satisfiable geometries (`twocentre.py`) |
| `+` a third centre `z = x+2a` with `Q_i cap R_i = empty` | **SAT for all 654** (`chain3.py`) |

So the natural (C6) is inert at `k = 6` too. Two reasons, both exact: (a) all 225 satisfiable
`l = 5` geometries and 125 of the 177 `l = 6` geometries admit a model `P` together with two labels
`m, m'` such that `m` is in no even-position palette and `m'` in no odd-position palette; then the
alternating singletons `{m}, {m'}` are a valid second centre (`twocentre.py`); (b) for the
remaining 52 the joint `(P,Q)` search succeeds anyway, because palettes of size `<= 3` in `6` labels
leave room. For reference the minimum label-set sizes are `l = 5`: `{3: 25, 4: 30, 5: 170}` and
`l = 6`: `{4: 3, 5: 12, 6: 162}` (`labels_used.py`) — the surviving models are *not* sparse in
labels, which is why (b) has to be checked by search rather than by an argument.

Consequently a (C6) that can bite must constrain the palette field at *all* unit translates in a
region, not at finitely many centres. That object is exactly m8's a.e.-collapse: the full palette
system is satisfiable iff `chi <= k`. So there is no cheap (C6), and Step 1 cannot be repaired by
strengthening inside the orbit level or at finitely many centres.

---

## 6. What is not claimed

* No claim about `chi(R^2)`. The decision is about a relaxation; SAT of a relaxation says nothing
  about `chi`, exactly as UNSAT would have (subject to (H7)).
* The counts for `l = 5, 6` are exhaustive for the six-position projection. I did **not** decide the
  full one-centre palette *field* at `l = 5, 6`: the field-level remark at the end of §2 settles only
  `l <= k-2`.
* No claim that the tightening is useless *as a theorem*: (C4) and (C5) are true, machine-checked,
  and they do exclude the 20 all-ternary orbit patterns and all fields with `sigma(E_x) > pi`. They
  are simply satisfiability-irrelevant.

---

## 7. Files and exact check commands

All paths relative to `.ultramath/smwfk0ybk/m6/`.

| file | what it is |
|---|---|
| `tight_csp.py` | procedure A: the tightened CSP, exhaustive sweep, `tight_csp_results.json` |
| `tight_csp_indep.c` | procedure B: independent C implementation (state-set DP, angle-derived O/I) |
| `compare_ab.py` | instance-level agreement of A and B on all 9324 instances + dihedral checks |
| `verify_tight.py` | CHECK 1 angle-based encoding, CHECK 2 all 654 witnesses, CHECK 3 pair-models, CHECK 4 symmetry |
| `calibration.py` | reproduces k = 4 (all UNSAT), k = 5 (Prop 8.2: l = 5 UNSAT) and m5's k = 6 table |
| `sets_compare.py` | the SAT *sets* of (C1)-(C3), (C1)-(C5) and the `|P| <= 2` variant are equal |
| `witnesses.py` / `witnesses.json` | one re-verified model for every satisfiable case (654), plus a pair-model |
| `labels_used.py` / `labels_used.json` | minimum number of labels per satisfiable geometry |
| `twocentre.py`, `chain3.py` | the candidate (C6) decisions of §5 |
| `TightCore.lean` | the machine-checked core of §3 |
| `INDUCTION.md` | the induction lemma, its proof, and the (H7) audit |

```
cd .ultramath/smwfk0ybk/m6
python3 tight_csp.py                                   # counts, ~1 s
gcc -O2 -o tight_csp_indep tight_csp_indep.c -lm && ./tight_csp_indep | tail -1
python3 compare_ab.py                                  # A = B on all 9324 instances
python3 verify_tight.py                                # all four checks pass
python3 calibration.py                                 # k = 4, k = 5 (Prop 8.2), m5's table
python3 witnesses.py                                   # 654 witnesses re-verified
python3 labels_used.py && python3 twocentre.py && python3 chain3.py
lean TightCore.lean                                    # exit 0, axioms [propext, choice, Quot.sound]
```
