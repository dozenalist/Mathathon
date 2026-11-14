# m13 / d14 — The tightened interface CSP at k = 6 is SATISFIABLE: (C4)+(C5) change no decision

**Answer to the mission's decisive question.** *Is there any satisfiable (l, sign matrix) at k = 6 with
(C4) and (C5) added?* **Yes — 3924 of the 55944 instances (654 of 9324 up to rotation), including every
instance at l = 3 and every instance at l = 4.** Hence the UNSAT branch of Step 1 is impossible:
**the tightened interface CSP cannot prove chi(R^2) >= 7**, with or without the INDUCTION LEMMA. The
route is dead; no L1–L5 lower-bound outcome is reached from it. I make no claim about chi(R^2) itself.

All numbers below are exact integers from exhaustive enumeration over the paper's own definitions at
k = 6. Check command: `python3 verify_m13b.py` (16 s).

---

## 0. The object (m5's encoding, audited)

Paper Definition 5.1 / Lemma 8.1 / Corollary 5.4, as used by m5 (`INTERFACE-NOGO.md` §1) and m2
(`L4-k-ladder.md` Lemma 1.1). At a centre x with a simple label cycle of length l and rays v_j:

* `sig[i][j] = sign(e_i . v_j)` with `e_i` at angle `i*pi/3`, ray `v_j` in cell `c_j in {0..5}`;
  `sign(cos(t*pi/3)) = +1` for `t = 0,1,5`, `-1` for `t = 2,3,4`. `c in {0..5}^l` covers all ray
  geometries; rotation by `pi/3` is a symmetry, so `6^(l-1)` instances suffice.
* `U = {l,...,k-1}` (the `k-l` outsiders),
  `O_i = U u {j : sig[i][j-1] = sig[i][j] = -1}`, `I_i = U u {j : sig[i][j-1] = sig[i][j] = +1}`.
* **(C1)** `1 <= |P_i| <= k-3`; **(C2)** `P_i cap O_i` and `P_i cap I_i` nonempty; **(C3)**
  `P_i cap P_{i+1} = empty`, indices mod 6; **(C4)** no two of the six palettes are complementary
  3-sets; **(C5)** at most three of the six palettes are ternary.

**Encoding audit (CHECK 0).** On **all 55944** instances the sets `O_i, I_i` computed from the paper's
set description ("delete the endpoints of every positive, resp. negative, edge; labels outside the
cycle lie in both") equal m5's bitmask `allowed_sets`, and m2's cardinality formula
`|O_i| = (k-l) + #{both incident negative}`, `|I_i| = (k-l) + #{both incident positive}` holds on every
one of them. Mismatches: 0, 0, 0. (C4) at k = 6 is the whole of m6's Theorem 1 restricted by
`|P| <= 3`: `A u B = Fin 6` with `|A|,|B| <= 3` forces `|A| = |B| = 3`. (C5) is m6's Theorem 2 at the
orbit level. Nothing in (C4)/(C5) is weakened here.

---

## 1. Theorem 1 (the two-outsider model) — a proof, not an enumeration

**Theorem 1.** *Let k = 6 and l in {3,4}. For **every** ray geometry c in {0,...,5}^l the alternating
singleton palettes `P_i = {l}` (i even), `P_i = {l+1}` (i odd) satisfy (C1)–(C5).*

*Proof.* Here `|U| = 6 - l >= 2`, so `l` and `l+1` are distinct outsiders. By the definition of
`O_i, I_i`, every outsider lies in both: `U subset O_i cap I_i` for all i. Then `|P_i| = 1 <= 3 = k-3`
(C1); `P_i cap O_i` contains `l` (resp. `l+1`) and `P_i cap I_i` likewise (C2); `P_i cap P_{i+1} = empty`
since `l != l+1` (C3); no palette has three elements, so (C4) and (C5) are vacuous. QED

Verified instance by instance (CHECK 3) on all `6^3 + 6^4 = 1512` geometries: failures 0. This alone
answers the mission's question: at l = 3 the tightened system is satisfiable for **every** geometry
(216/216 unnormalised, 36/36 normalised), so no UNSAT certificate can exist. **Step 1 as stated cannot
reach chi(R^2) >= 7.**

The same argument is the "m >= 2 is trivial" remark of m5 §2; what is new here is that it *survives the
tightening*, and that it is not an accident of l = 3,4 (Theorem 2).

---

## 2. Theorem 2 (the tightening is decision-inert at k = 6) — exhaustive

**Theorem 2.** *For k = 6, every l in {3,4,5,6}, and every ray geometry: a (C1)-(C3) model exists iff a
(C1)-(C3) model with **all** `|P_i| <= 2` exists. Such a model satisfies (C4) and (C5) automatically.
Hence the (C1)-(C5) decision equals the (C1)-(C3) decision instance by instance.*

| l | geometries | (C1)-(C3) SAT | has model with all `|P_i| <= 2` | (C1)-(C5) SAT |
|---|---|---|---|---|
| 3 | 216 | 216 | 216 | 216 |
| 4 | 1296 | 1296 | 1296 | 1296 |
| 5 | 7776 | 1350 | 1350 | 1350 |
| 6 | 46656 | 1062 | 1062 | 1062 |

(Up to rotation: 36/36, 216/216, 225/1296, 177/7776 — identical to m5's table.) The two middle
columns are equal at every l, and that is the theorem: **no instance loses its last model.**

How much (C4)+(C5) *do* prune, counted over all models (`count_models.py`, 555 s): l=3 217067040 ->
185861952 (-14.4%), l=4 203472072 -> 156564840 (-23.1%), l=5 4522200 -> 3426420 (-24.2%),
l=6 99864 -> 69888 (-30.0%); instances killed entirely: **0** at every l. So (C4)/(C5) are genuine
constraints (they cut up to 30% of the models) that are nevertheless *decision-inert* at k = 6.

**Every SAT case has an extracted witness.** `witnesses.py` writes one (C1)-(C5) model for each of the
654 satisfiable instances (c_0 = 0 normalisation) to `witnesses.json`, and re-checks each one against
(C1)–(C5) from the paper's set definition with no search code: 654 witnesses, 0 failures. The size
distribution is itself informative: all palettes of size 1 on 252 instances (= all 36 of l = 3 and all
216 of l = 4, the two-outsider models); all palettes of size 2 on 177 instances (= **all** of l = 6);
`(1,1,2,2,2,2)` on 160 and `(1,1,1,2,2,2)` on 65 (the 225 of l = 5). **No witness uses a ternary
palette.**

---

## 3. Verification: three procedures, no disagreements

`verify_m13b.py`, all 55944 instances at k = 6:

* **m5's bitmask reachability DP** (`interface_csp.sat_geometry`, palettes of size <= k-3);
* **my recursive DFS** (`profile2.first_model`, early exit, cyclic pruning);
* **my size-<=2 reachability DP** (`sat_small_DP`, a different algorithm and a different palette
  family).

Disagreements on the per-instance SAT/UNSAT decision: **0**. Plus (i) rotation invariance of the
decision under all five nontrivial shifts, all l: **0 violations** (this validates m5's `6^(l-1)`
normalisation and my full `6^l` counts, which are exactly 6x m5's); (ii) a no-pruning product
enumeration on 120 random satisfiable instances: 0 failures; (iii) CHECK 0 above.

---

## 4. What the surviving models violate — the input to the next round (C6)

The survivors violate **nothing** in (C1)–(C5); that is the content of Theorem 2. Three structural
facts say what a decisive (C6) must therefore look like. All are exact computations (`variants.py`).

1. **(C4)/(C5) only see ternary palettes, and every instance has a ternary-free model.** Any further
   constraint of the same shape — bounding `|P|` from above, or restricting only `|P| = 3` — is inert
   at k = 6 for the same reason. The mission's hope for this tightening is structurally unavailable.
2. **The palette-size window does not matter down to 2.** Replacing (C1) by `2 <= |P_i| <= 3` gives
   *identical* counts: 216, 1296, 1350, 1062 (first witnesses for l = 3: `{0,3},{1,4},...`; l = 4:
   `{0,4},{1,5},...`; l = 5: `{0,5},{1,4},...`; l = 6: `{1,4},{2,5},...`). So forbidding singleton
   palettes changes nothing.
3. **All-ternary is refuted by (C4) at every l.** Restricting (C1) to `|P_i| = 3` gives 216, 1296, 330,
   102 without (C4) — and **0/216, 0/1296, 0/7776, 0/46656 with (C4)+(C5)**. So the k = 6 interface
   lives entirely in the **2-element** palettes: the system is SAT with `|P| in {2,3}` and UNSAT with
   `|P| = 3`. A (C6) that forces `|P_i| = 3` (for all i, at a positive-measure set of directions) would
   be decisive; a (C6) that only bounds sizes from above or restricts triples cannot be.

Sharper diagnosis of the l = 5,6 counts, by (C2) versus (C3): at l = 6 (`U = empty`) **40422 of 46656**
geometries already fail (C2) (some `O_i` or `I_i` is empty — a single empty sliver admits no palette);
of the 6234 with all six slivers nonempty, 1062 are satisfiable, so 5172 die on the disjointness cycle
(C3) (+C1). At l = 5 (`U = {5}`) no sliver is ever empty, so all 7776 geometries pass (C2) and the
entire obstruction 6426/7776 is (C3) (+C1). The `k-l` outsiders are exactly what keeps (C2) alive; this
is m2's sliver count and m5's `m >= 2` remark, sharpened to the k = 6 instance level.

**Reading of (C4).** In the paper (m6 Thm 1) the exclusion is between *positive-angular-measure* sets
`B_A, B_{A^c}`, so the pointwise six-palette version used in the CSP is the **strongest** reading. The
inertness proved above is therefore a fortiori true for the a.e. reading: no reading of (C4)+(C5)
rescues the route.

**The antipodal (twelve-direction) refinement changes nothing.** Take any witness of `witnesses.json`
and repeat it on the antipodal half: `P_{j+6} := P_j`. The allowed sets are 6-periodic in `i`
(m5 §1), so (C1),(C2) hold at all twelve positions; (C3) holds on the twelve-cycle; (C4) holds because
the multiset of twelve palettes is the six palettes doubled; and the twelve directions split into two
`π/3`-orbits (even and odd `j`), each carrying at most three ternary palettes. So the twelve-position
tightened system is satisfiable in the same 654 instances — m5's observation that the antipodal
refinement is vacuous for (C1)-(C3) survives the tightening.

---

## 5. Consequence for the mission

* **Step 1 returns YES (satisfiable), so the UNSAT branch is impossible.** The tightened CSP at k = 6
  is satisfiable, in 3924 instances, including all of l = 3 and l = 4 for every ray geometry. The
  INDUCTION LEMMA is moot for this purpose: it would only *produce* a model, and models exist in
  abundance.
* Since the mission's Step 1 was "the one computation that can prove chi >= 7", and it returns SAT,
  no lower-bound terminal outcome (L1–L5) is reached by this route. This says nothing about chi(R^2):
  it neither proves chi = 6 nor chi >= 7.
* What would be needed to revive the route is a **true** constraint outside (C1)–(C5) that is violated
  by every model with all `|P_i| <= 2` — the natural candidates are inter-centre constraints
  ((5.3)/translation, m8's a.e. collapse, m7's (C6) round), not any further cardinality bound at a
  single centre. The exact threshold exhibited in §4.3 is the target: prove that a palette of size 3
  is forced (or that a 2-element palette is impossible in the relevant angular configuration).

**Not claimed.** No induction lemma, no Step-2 work, no bound on chi(R^2), no claim that the full
palette system of m8 at k = 6 is satisfiable (that is equivalent to chi <= 6 and remains open). The
statement is exactly: the finite relaxation (C1)-(C5) at one centre is satisfiable, so it cannot
certify chi >= 7.

---

## 6. Files and exact check commands (all relative to this directory)

| file | what it is | command |
|---|---|---|
| `verify_m13b.py` | CHECKs 0–5: encoding audit, rotation invariance, three-procedure agreement, two-outsider theorem, ternary-free models, product-enumeration sample | `python3 verify_m13b.py` (16 s) |
| `verify_m13.log` | its output | — |
| `profile2.py` | the CSP from the paper's definitions (independent of m5's code), DFS decision, profile/scan to `profile_results.json` | `python3 profile2.py` (9 s) |
| `variants.py` | palette-window sweep `[1,3]`, `[2,3]`, `[3,3]`, `[1,2]`, with and without (C4)+(C5) | `python3 variants.py` (30 s) |
| `count_models.py` | model counts before/after the tightening for all 55944 instances | `python3 count_models.py` (555 s) |
| `characterise.py` | the (C2)-versus-(C3) breakdown of the l = 5,6 counts | `python3 characterise.py` (5 s) |
| `profile_results.json` | per-instance sliver profiles, first witnesses, SAT counts | — |
| `witnesses.py` / `witnesses.json` | one (C1)-(C5) model for each of the 654 satisfiable instances, each re-checked independently | `python3 witnesses.py` (1 s) |
