# d8 — independent recomputation and statement audit of the cited Lean cores: result

**Result.** The four cited Lean cores of the record (`smwfo9zkl/m9` engine + `check_engine`,
`smwfwi7rh/m8/repair31.lean`, `smwfwi7rh/m11/frozen_core.lean`, `smwfwznwk/m4/count_lemma.lean`)
**compile from scratch on the pinned toolchain (Lean 4.34.1 + pinned Mathlib), exit 0, with
exactly the axiom sets the record reports and no `sorryAx`**; each theorem's statement matches
the record's itemised claim about it; and the record's bookkeeping carries eight defects — one
recorded command that cannot work, one broken path, three over-attributions of "machine-checked",
two scope compressions and one documentational biconditional that is false — none of which
changes a mathematical conclusion.  All eight are proved, fixed and itemised in `AUDIT.md`.

Two of them matter beyond bookkeeping:

* the report's §2 recipe for the engine does not reproduce (`lean check_engine.lean` exits 1:
  Lean never searches the working directory, and `lean f.lean` writes no `.olean`);
* the ledger's "repaired to the confined form R1 (`m8`, Lean-checked)" is false: `repair31.lean`
  contains no measure theory at all — what is checked is the three-point pigeonhole, the shift
  rigidity `Re v = -5/6`, and the two-valued sector no-go.

**New certificates** (written for this audit, all on `[propext, Classical.choice, Quot.sound]`):

* `m7_sharpness.lean` — four theorems showing that the acyclicity hypothesis, the size-`≥2`
  hypothesis, the absent-label hypothesis and the two-valued hypothesis of the four cores are
  each necessary;
* `m7_cover_radius.lean` — the engine's cover obstruction fails on every disk of radius `≤ 1`
  (the mesh hypothesis is automatic there), so its radius constant is essential, and the
  formalised instance has slack over the sharp form needed for `(W)`'s `R > 1`;
* `indep_check.py` — exact-arithmetic (no Lean, no floating point) re-derivation of every finite
  fact the four cores rely on, plus an exact census of sector fields, two independent
  algorithms: **0 two-valued** and `6 / 12 / 30 / 4398 / 130020 / 2793606` three-valued
  solutions at `n = 6m`, `m = 1..6`.  That is the sprint's three-valued wall of `REPORT.md` §5c
  in finite, machine-checked form.

## Files and commands

| file | what it is |
|---|---|
| `CERTIFICATE.md` | commands, timings, exit statuses, verbatim axiom listings, md5 of every audited copy |
| `AUDIT.md` | statement-by-statement match against the record, defect list D1–D8 with proofs and fixes, the exact "not machine-checked" boundary, sharpness results |
| `lean-audit/` | the copies, the run outputs (`*.out`), `m7_sharpness.lean`, `m7_cover_radius.lean`, `indep_check.py` |

Reproduce (from the repository root; `<repo>/.ultramath/smwg1r9lg/m7/lean-audit`):

```
source scripts/env4341.sh
lean -o k6_s7_engine.olean k6_s7_engine.lean          # exit 0
LEAN_PATH=".:$LEAN_PATH" lean check_engine.lean       # exit 0  (7 declarations)
lean repair31.lean                                    # exit 0  (3)
lean frozen_core.lean                                 # exit 0  (3)
lean count_lemma.lean                                 # exit 0  (3)
lean m7_sharpness.lean                                # exit 0  (4)
lean m7_cover_radius.lean                             # exit 0  (2)
python3 indep_check.py                                # exit 0, ALL ASSERTIONS HOLD
```

## What was not done

The audit certifies compilation, statements and axioms; it does not re-audit the paper-level
mathematics.  In particular §7 Lemmas 7.2, 7.3, 7.7, 7.8, the sharpened scale-invariant cover
lemma, `(TE)`, `R1`, and m11's shift-set Lemmas 4.1–4.2 are *not* machine-checked by any file
audited here (list in `AUDIT.md` §3).  I did not modify any file outside
`.ultramath/smwg1r9lg/m7/`.
