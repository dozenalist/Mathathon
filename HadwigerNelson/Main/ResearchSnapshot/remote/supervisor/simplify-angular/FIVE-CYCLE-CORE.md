# Replacement for §6.3.4: the five-cycle finite core is unsatisfiable with no case analysis

Status: **exact finite computation + hand proof, checked** (`checks/five_cycle_full.py`, rc 0).
Scope: the finite part of the five-cycle accumulation argument (paper §6.3.4, pp. 41-42); the
analytic inputs (state reduction, Lemma 6.2/6.3, weak-* passage) are untouched.

## Notation (all from the paper; nothing added)

`I = Z/5Z`. A.e. palette at a five-cycle centre is a diagonal `D_i = {i, i+2}`. `S(a) = {i : a`
lies in the closed essential support of state i}`. A nonempty `L ⊆ I` is **valid** iff
`⋂_{i∈L} D_i = ∅`. Positions `r ∈ Z/6Z`, `S(r) = S(R^r a)`. Four facts printed in the paper:

* (V) every `S(r)` is valid and nonempty [pp. 40-41];
* (D) `S(r) ∩ S(r+1) = ∅` ["S(a) ∩ S(Ra) = ∅", p. 41];
* (N) every `i ∈ S(r)` has a neighbour `i±1` in `S(r+1)` and in `S(r-1)`;
* (R) after relabelling, `0,1 ∈ S(0)`.

## Lemma (replacement). (V)(D)(N)(R) are inconsistent.

*Proof.* `I` has exactly **21** valid lists (5 adjacent pairs + 16 sets of size ≥ 3). Every valid
list inside `{2,3,4}` is `{2,3}`, `{3,4}` or `{2,3,4}`, so each **contains 3**; the only valid
list inside `{0,1}` is `{0,1}`.

1. `S(1) ⊆ I ∖ S(0) ⊆ {2,3,4}` by (D) and (R).
2. By (N) at `r=0`, `0` and `1` each have a neighbour in `S(1)`; `1,0 ∉ S(1)` by (D), so `4,2 ∈ S(1)`.
3. `{2,4}` is not valid (`D_2 ∩ D_4 = {4}`), so (V) gives `S(1) ⊋ {2,4}`; with step 1,
   `S(1) = {2,3,4}`. Same for `S(5)`.
4. `S(2) ⊆ I ∖ S(1) = {0,1}` with (V) forces `S(2) = {0,1}`; likewise `S(4) = {0,1}`.
5. `S(0) ⊆ I ∖ S(5) = {0,1}`. By (N) at `r=5`, `3 ∈ S(5)` needs a neighbour in `S(0)`, but
   `nb(3) = {2,4}` and `{2,4} ∩ {0,1} = ∅`. Contradiction. ∎

## Quantified effect

| | printed §6.3.4 | this |
|---|---|---|
| case splits | 5 residues `j`, then 2 branches | **0** |
| uses of Lemma 6.7 (step ban) | 2 | **0** |
| uses of the a.e. transition rule (6.6) | 1 (null state) | **0** |
| uses of "`S(3)` contains an adjacent pair" | yes (starts the `j` split) | **no** |
| argument length | 3 sentences + 2-branch case + Lemma 6.7's proof | 5 numbered steps |

Consequence at paper level: `Lemma 6.7` occurs exactly twice in the manuscript — its statement
(p. 41, `pdftotext` line 2139) and the single use at line 2196, which is the step replaced here.
So with this replacement **Lemma 6.7 and its trace/weak-* proof are dead and can be deleted from
§6.3.3** (about 19 lines plus the one use), and with them the only place in §6.3 needing the
two-endpoint avoiding-trace construction.

No hypothesis is dropped and no exceptional set is introduced on the way: the paper's closing
remark ("only the step bans at the two fixed directions have been used, so no union of exceptional
null sets is involved") is strengthened — no step ban is used at all.

## Sharpening (two positions suffice; independent replication)

An independent re-implementation (swarm member `m3`, `.ultramath/smwfycy1c/m3/check2.py`,
bitmask arithmetic, 15 assertions, exit 0) reproduces every claim above and adds the following,
which I re-derived by hand and accept:

* the hypothesis set of the forced prefix is again a **single** tuple, `(S0,S1) = ({0,1},{2,3,4})`;
* with the neighbour rule applied at **every** direction (the paper's own statement of it, hence
  mutual across an adjacent pair), the pair `(S(0),S(1))` is **already contradictory**: `3 in S(1)`
  has neighbours `{2,4}`, both in `S(1)`, so `3` has no neighbour in `S(0) = {0,1}`;
* consequently the accumulation contradiction in the five-cycle locus needs only the two
  directions `a` and `-a` — not the six positions `R^r a` — and the `j` analysis, Lemma 6.7 and
  `(6.6)` are all redundant.

So the shortest form of the finite core is: *one* forced pair of lists, killed by one neighbour
count. My five-step version above is the same argument carried through all six positions; keep it
if a self-contained six-position statement is wanted, but the two-position kill is the one to quote.

## Machine check

* `python3 checks/five_cycle_full.py` (rc 0): exhaustive backtracking over all 6-tuples of the 21
  valid lists under (D) and (N) starting from (R) returns **0 solutions**; steps 2-5 are checked as
  set identities; check 1 is the unsatisfiability claim itself.
* `checks/five_cycle_core.py` (rc 0 on A/B/C; its D5 line is a mis-stated auxiliary and is
  superseded by `five_cycle_full.py` check 4): keeps the 3-list version, reproduces the paper's
  `j ∈ {1,4}` split (D1) and shows the strengthening is exactly the extra content —
  `S(1) = {2,3,4}` rather than `{2,4} ⊆ S(1)`.
* `sprint/k6`/`results` `compressed-proof-verify.py` §7 tests only the weaker printed conclusion:
  its Claim-A hypothesis set has exactly **one** realisation (S0={0,1}, S1=S5={2,3,4}, of 32768
  raw combinations), so its "no case was missed" is a single-instance computation, not an
  exhaustive one. Not an error, but the quantifier it advertises is not what it checks.

Caveat: this shortens the finite argument *given* the paper's axioms; it does not re-derive (V),
which needs the state cover finiteness and Lemma 6.3.
