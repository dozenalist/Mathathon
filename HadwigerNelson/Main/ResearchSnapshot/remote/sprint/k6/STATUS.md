# Status after the Open Math OS outage — checks I ran by hand

Ultramath is switched off: the three swarms were interrupted by the VM restart and are not
resumed. Their boards and every member directory are on disk under `.ultramath/`
(`smwfwi7rh`, `smwfwznwk`, `smwfycxze`); nothing was deleted. Four submissions that were queued
when the runtime stopped, plus two already-accepted ones, were checked directly with the members'
own scripts. Exit statuses below are from this session.

## Checked and accepted (by direct check, not by verdict — the verdict channel is gone)

### m11 / d9 (smwfwi7rh) — frozen fields, exact radii
- `lean frozen_core.lean` → **exit 0**; `union_eq_of_three_disjoint`, `not_disjoint_fourth`,
  `exists_card_le_one_of_free_label` on `[propext, Classical.choice, Quot.sound]`.
- `python3 model_radii.py` → **exit 0**. Transport radius of the three-block fields:
  **0.28558**, not the `pi/54 = 0.05818` quoted in the report until now; the ell=6 free-label
  word: **0.14715**.
- `python3 wordsearch2.py` → **exit 0**. Sector class SAT to `d = 0.175`, UNSAT from `0.180`.
- Content: a centre-independent field satisfies `(5.3)` at separation 1 only with `P(f) = empty`,
  so every countermodel of §4 is inadmissible — the fourth independent derivation of that, after
  m4 Thm 1, m15 Thm C and smwfwznwk m1/m4.

### m13 / d1 (smwfwi7rh) — the exact sector threshold
- `python3 sector_sat.py` → **exit 0**: satisfiable iff `K <= floor(m/5)` for every `m <= 30`.
- `python3 construct_closed.py` → **exit 0**: full offset check for `m = 5..120`, adjacency for
  `m = 5..5000`, explicit `K`-block constructions.
- `python3 geometry_fast.py` → **exit 0**: `d* = 0.17557050458494626033`.
- Content: the sector class meets the transport up to distance `d` iff
  `Sigma(d) <= pi floor(m/5)/(3m)`, so `d <= d* = Sigma^{-1}(pi/15)`, **sharp**; no member of the
  class satisfies `(5.3)` unrestricted in distance. Without the free label the radius is
  `0.2855752194`, so the free label is not what binds. Adds to m11's radius numbers.

### m2 / d1 (smwfycxze) — §8 at `k = 6`, `ell = 5`
- `python3 work/final_verify.py` → **exit 0**, `ALL ASSERTIONS HOLD`. All 1000 geometry-free cases
  UNSAT when the outsider is absent, with **five** independent decision procedures; the `k = 5`
  calibration gives 0/1000 (Lemma A reproduces Proposition 8.2); sharpness SAT 1000/1000 with
  nothing absent, 704/1000 with a cycle label absent, 0/1000 with the outsider absent; the
  case analysis closes on exactly the four 0-mod-5 triples `(1,1,3),(1,2,2),(2,4,4),(3,3,4)`.
- Explicit three-valued countermodel with `sigma{X in P} = 1/3`, satisfying `(8.1)`, `(5.7)`,
  `|P| <= 2`, `(6.2)`, `(SUM)`, the `m11` bound, and avoiding a cycle label.
- Content: the gap for `ell = 5` at `k = 6` is exactly "the outsider is absent a.e.", and that is
  false; it does **not** exclude the 5-cycle.

## Already accepted before the outage (checks re-run earlier in this session)
m3 (d16), m15, m7, m1 (d18), m6, m9, m12, m16, m8, m2 (d10) in `smwfwi7rh`; m1, m2, m4 in
`smwfwznwk`; m4, m1 in `smwfycxze`. Every one was reproduced from its own verifier.

## Not checked
- `smwfycxze` m3 (`A`-parameterised accumulation sets) — its output was never read.
- `smwfycxze`'s fourth member (the ell=4 direction) — no report was submitted.

## Resolved since (by `smwg1r9lg`)
- **`m2`'s claim that `m6`'s `{5}/{1,3}` `STRIP(6,5)` witness is killed by Lemma 6.4 is FALSE**
  (`smwg1r9lg` m2, defect D7, `m6strip.py` exit 0): `|A u B| = 3 = k-3`, so `|T'| = 3` and the
  mechanism needs `chi(Q) >= 4`, i.e. a 4-chromatic finite unit-distance graph inside the direction
  sum set, which the record does not have. The witness stands.
- The record's Lemma D *proof* is broken; the statement is true via `(5.2)+(T)`
  (`smwg1r9lg` m5 Thm D(i)) — see REPORT §3b.
