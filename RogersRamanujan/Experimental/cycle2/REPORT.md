# Direction C (experimental) --- cycle 2 report

Folder: `RogersRamanujan/Experimental/cycle2/`.  Nothing outside it was edited;
`Computation/bz82.py` and `rr_core.py` are imported read-only.

## Outcome in one line

The objective is **not** met.  Delivered instead: a **proved closed form for the
whole all-ones family** `(1^s)` under BZ82's map (four of five residue classes
for all `s`, the fifth proved only on a window and provably not closable
beyond it), two fully specified mechanisms with their exact blocking lemma, and
frozen conjectures that failed on held-out parameters with the failures listed.

## Files

| file | content |
|---|---|
| `PROOF_families.md` | Lemmas 0-2 and Theorems F, G: the case analyses, with the inequalities |
| `MECHANISMS.md` | M1 (collapse-and-singleton), M2 (free window), C1-C4 frozen + failures |
| `DATA.md` | raw tables: `(1^s)` for `s <= 60`, `(4^r)` for `r <= 20`, the `(4^r,1^s)` grid, free-window sizes |
| `lemma_checks.py` | instantiates every lemma on `s,p <= 200`, `r <= 60` |
| `family_rules.py` | the derived rules vs the committed `bz82.py`; C1/C2 held-out tests |
| `make_data.py`, `window.py`, `run_all.sh` | table generation, free-window counts, exact commands |

## Commands and key output lines

```
$ sh run_all.sh
$ python3 lemma_checks.py
Lemma 0 (one phi collapses the ones-ray): checked s = 3..200, fails = 0
Lemma 1 (psi on a singleton) branch counts over p = 0..200: {'a': 41, 'b': 79, 'c': 40, 'd1': 1, 'd2': 39} ; fails = 0
Lemma 2 (six-step chain): 39 parameters p = 8..200, p = 3 mod 5 ; fails = 0
Lemma 3 (fours-ray, window 5..8): fails = 0
Lemma 6 (fours-ray, r >= 9): 52 parameters, fails = 0
Theorem F end-to-end: claimed s = 0..120, mismatches = 0
ALL LEMMA CHECKS PASS

$ python3 family_rules.py
    train    agreements 26 / 26
    heldout  agreements 76 / 76
    failures: 7 / 7          <- C1, the fifth residue class, k = 6..12
ALL CLAIMED RANGES AGREE

$ python3 window.py
free-window fraction over n<=40: 255/3251 = 0.078
```

## The mathematical content

`phi(0;(1^s)) = (-1;(s-3))` for every `s >= 3` (one step).  On a singleton
`(-1;(p))`, `psi` is closed form in all five residue classes of `p`: `(p+3)` for
`p = 0`, `(p,3)` for `p = 1,4`, `(5^{(p+3)/5})` for `p = 2`, `(3,3)` for `p = 3`
and a six-step chain to `(p-2,5)` for `p = 3`, `p >= 8`.  Hence, on the
`B`-side, BZ82 sends `(1^s)` to `(s)`, `(s-3,3)`, `(s-5,5)` or `(5^{s/5})`
according to `s mod 5`, and to `Tinv` of those on the `D`-side
(`(s)`, `(s-2,2)`, `(s-4,4)`, `(6+s/5-2i)`).  The path length is `<= 6`
everywhere in four classes; the single class `s = 0 mod 5`, `s >= 30` is the
only place it grows (`220, 574, 124, 452, 44, 454, 672` for
`s = 30,35,...,60`), and the reason is proved: the two-step output `(5^{s/5})`
stops lying in `B` exactly when `5 < s/5`.

## Honest status

* PROVED: Lemmas 0,1,2, Theorems F and G (first steps only for `G`).
* TESTED_FINITE only: the equality of the derived rules with the committed
  implementation over `s <= 120` (a transcription cross-check, not a proof of it).
* REFUTED: C1, C2, C3, C4 --- see `MECHANISMS.md`.
* NOT ACHIEVED: a bijection for the objective; a closed form for `s = 0 mod 5`,
  `s >= 30`; any rule at all for the two-parameter family `(4^r,1^s)`; the
  single lemma of each mechanism (L-M1, L-M2) is open.
* Not claimed: any growth class for path lengths (per correction C4), any
  all-`n` statement about the maps themselves.
