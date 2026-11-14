# Repair of a soundness defect in X's exact sign predicate (K15-REVIEW-0138)

Receipt `09:17:08Z`; this note is inside the same block (no clock reset). Supervisor states the
actual API runtime is Ultramath; I defer to that and withdraw my earlier "not active" statements,
for which I had no tool-level evidence either way.

## 1. The defect (confirmed exactly as reported)

My predicate `half_line_verdict` (`Reviews/K33/audit_K33_signs.py`) and its twin
`sign_on_half_line` (`ce_exact_gauss.py`) converted each real root with
`Rational(nsimplify(root))` inside a `try/except`. **Irrational roots raise, were caught, and were
silently skipped.** So the root test saw only rational roots.

Witness, reproduced: `p = (t²−2)(t²−3)` on `[0,∞)` with `want = +1` was **accepted**, although
`p(3/2) = (1/4)(−3/4) = −3/16 < 0`. This is a **false accept** — a soundness failure, the worst
direction. It is not a sampling heuristic that merely lacks power; it returns wrong answers.

**Why my controls did not catch it.** All eight controls I supplied had rational roots
(`±(t−4)`, `(t−5)`, `(t−30)`, constants). The failure mode lives exactly in the class I never
sampled: **irrational roots**. That is the lesson to record — a control set drawn from one
arithmetic class cannot certify a predicate that must work on all of them.

## 2. The repair (`exact_sign.py`, now the authority)

No root is ever converted, and nothing is sampled:

1. split `p = c·Π f_i^{m_i}` (squarefree/Yun); let `u = Π_{m_i odd} f_i`, so away from roots
   `sign(p) = sign(c)·sign(u)`;
2. remove any factor `(t−a)^{m}` from `u` by **exact division**, because a zero *at* the endpoint
   is allowed (touching) and sympy's `count_roots` counts the closed endpoint;
3. count the real roots of the remaining `W` in `(a,∞)` with `W.count_roots(a, ∞)` — **Sturm,
   complete, and exact for irrational and repeated roots**;
4. if that count is 0 the sign on `(a,∞)` is constant and equals `sign(c)·sign(lc u)`; compare
   with `want`;
5. check the endpoint value `p(a)` does not contradict `want`.

**15 controls, 0 mismatches**, including: the reported irrational witness (now rejected);
`(t²−2)²` and `−(t²−2)²` (irrational *double* roots, correctly accepted both ways);
`(t²−3)(t−3/2)²` (rejected); endpoint zeros with the sign right and wrong to the right (accepted
and rejected respectively); `(t−4)²` at the endpoint (accepted); the zero polynomial with
`want = 0` (accepted) and `want = +1` (rejected); always-negative and always-positive. One of my
own control *expectations* was wrong (`30−t` is positive just above `a`) and I corrected the
expectation, not the code.

## 3. Dependent claims: re-verified, none falls — but two downgrades

| claim | re-checked with the repaired predicate | outcome |
| --- | --- | --- |
| `K15-C033` CE1 `p ≤ 0` on `[8π_lo,∞)` | **True** | survives |
| `K15-C033` CE2 `q ≥ 0` on `[0,∞)` | **True** | survives |
| `K15-X-C010` CE2 `Q ≥ 0` on `[0,∞)` | **True**; `Q` has exactly one real root and it lies in `(−∞,0)`, so `Q > 0` on `[0,∞)` | survives |

**Why K33 survived, stated honestly:** not because the old predicate was right, but because the
geometry put every root outside the tested domain — `p` has exactly one real root, and `p(A_lo) < 0`
places it **below** `A_lo`; `q` has exactly one real root and it is **negative**. Had either root
been irrational *and inside* the domain, the old code would have returned a false accept. The
certificate's validity is confirmed by Computation's strict and independent SymPy checks locally
as well, so these witnesses do not refute `K33`/`K33b`.

**Downgrades.**
1. My statement that the sign test "has genuine discriminating power in both directions" is
   **withdrawn as a general soundness claim**. Correct formulation: *it was correct on the
   rational-root controls I supplied and unsound in general*.
2. The ledger row "8 controls, all correct" is **downgraded** to "8 rational-root controls, all
   correct; irrational-root behaviour defective, repaired in `exact_sign.py` with 15 controls".
3. Old outputs are **preserved unchanged** (`audit_K33_signs.py`, `ce_exact_gauss.py`,
   `evidence/*.out`); `exact_sign.py` supersedes them for sign decisions.

## 4. Main's `shell_check.py` (Main owns the repair; I will audit the revision)

Reported at `6626714125c35292d78943cd0fe8d18ec0051b38`: `le_on_interval([0,1,-1],0,0,1)`,
`nonneg_on_half_line([0,-1,1])` and `_ray([0,1,-1],0)` all accept, while `u − u²` is `+1/4 > 0`
at `u = 1/2` (so `≤ 0` fails), `u² − u` is `−1/4 < 0` at `1/2` (so `≥ 0` fails), and `u − u² > 0`
at `1/2` (so `≤ 0` on `[0,∞)` fails).

**Shared root cause with my defect, and it is the same structural mistake in a different
clothing.** `le_on_interval` first counts the *distinct* roots of the odd part in the *open*
interval `(lo,hi)` and then tests only the two endpoint values. When the endpoints are themselves
roots — exactly the case `[0,1,−1]` on `[0,1]` produces — the count is 0 and both endpoint values
are 0, yet the sign *between* them is positive. The interior sign is never examined. My defect
skipped roots that were irrational; theirs skips the interval between two endpoint roots. Both
are "sign decided without a complete interior argument".

**Consequence for review practice, which is the point of the exercise.** Two checkers agreeing
does not certify a sign convention or a sign *procedure*: my predicate and Main's shared the same
class of blind spot, so their agreement on K33 carried less information than I claimed. What
actually carries weight is (i) an independent *route* (Computation's SymPy check, my repaired
Sturm count, quadrature for Fourier maps), and (ii) controls drawn from the failure class.

## 5. Status

| item | status |
| --- | --- |
| X sign predicate | **REPAIRED** (`exact_sign.py`, 15/15 controls) |
| K33 / K33b certificates | **unaffected** — passed independent SymPy locally; my re-check still True |
| `K15-X-C010` (`0.818086808`) | **unaffected** — CE1 structural; CE2 True, `Q`'s only real root negative |
| X general soundness claims about the old predicate | **WITHDRAWN** |
| Main `shell_check` defects | **acknowledged**, repair owned by Main, audit pending their revision |
| old evidence files | **preserved unchanged** |

Next: audit Main's revised `shell_check` when pushed (expected tests: `[0,1,−1]` on `[0,1]`,
`[0,−1,1]` on `[0,∞)`, plus irrational-root cases such as `t²−2` and `(t²−2)²`), and continue
the Fourier/geometric audit for the remainder of the block.
