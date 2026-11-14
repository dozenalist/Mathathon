# cycle 3 — worker m1, direction D: valid two-parameter family $(4^r,1^s)$

Folder: `RogersRamanujan/Experimental/cycle3/`.
Files: `fam45.py` (the only script), `results_fam45.json` (machine readable),
`PROOF_fam45.md` (Theorem 1–3 with proofs, conjectures, question), this file.

Exact command (from the repository root) and full output, 4.5 s:

```
$ python3 -u RogersRamanujan/Experimental/cycle3/fam45.py
PASS   C0 negative controls                           (5^k) not in A_n; (11,6,1,1,1) IS in A_20 but in no (4^r,1^s)
PASS   C1 A_n membership of fam(r,s)                  2666 objects, weight<=160, 0 bad
PASS   C2 Theorem 1 phi closed form vs bz82.phi       3315 states, 0 mismatches, excluded set = Lemma 2
PASS   C3 Theorem 2 psi o phi (Case I, r>=1)          20 states, 0 mismatches
PASS   C4 Theorem 3 endpoint of (4,1^s)               120 s values, 0 mismatches, chain length [2] always
PASS   C5 endpoint table weight <= 40                 231 (r,s) pairs, 225 with a full chain
PASS   C6 P2: r=2, s=2 mod 5, s<=402                  80 values, 0 failures, chain length [8]
PASS   C7 P3: r=3, s=2 mod 5 is REFUTED               7 ok (s<=57), first failure s=62, 4 failures in range
PASS   C8 r=1 classes 0,4 mod 5 have no closed form   s=0 mod 5: max finite chain 18702, 6 of 40 exceed the cap; s=4 mod 5: max finite chain 15452, 15 of 40 exceed the cap

TOTAL: 9/9 checks passed
wrote .../RogersRamanujan/Experimental/cycle3/results_fam45.json
```

The script imports the committed `Computation/bz82.py` and `rr_core.py` (nothing
is edited outside this folder); every comparison is against `bz82.phi`,
`bz82.psi`, `bz82.pi_forward` and `rr_core.Tinv`.

## What is proved (in `PROOF_fam45.md`)

* **Lemma 1** — the local BZ82 data $(a,L,\mu,\lambda_\mu,t^*)$ on the whole
  family, six-line table, proved.
* **Lemma 2** — the family members lying in the excluded set $0\times B(n)$ are
  exactly $(0,0),(0,1),(1,0),(2,0),(3,0),(4,0)$: i.e. $()$, $(1)$, and
  $(4^r)$ for $1\le r\le4$. This *derives* RR-C014's "undefined for $r\le4$"
  instead of observing it.
* **Theorem 1** — $\varphi$ in closed form on the **whole** family (all
  $r,s\ge0$), six cases: $r=0$ with $s=2$ vs $s\ge3$; $1\le r\le4$ with
  $t\le5$ vs $t\ge6$; $r\ge5$ with $t\le8$ vs $t\ge9$. The Case-I/II
  threshold depends on $t=r+s$ **only**, so the family is a genuine
  two-parameter simplification, not twelve examples. Nonnegativity of every
  created part, of the inserted count, and $a\ne\mu$ (deletion validity) are
  read off the proof.
* **Theorem 2** — $\psi\circ\varphi$ in closed form on the complete Case-I
  parameter set ($r\ge1$): the $5$-block created by $\varphi$ is **cancelled
  exactly** by $\psi$'s branch I(a) and the state returns to $j=0$ with the same
  weight, $(0;(5r-3,2^{s-1},1^{5-t}))$ resp. $(0;(5r-8,2^s,1^{8-t}))$. All 20
  parameters are covered, so C3 is a complete check, not a range.
* **Theorem 3** — the **full BZ82 endpoint** for $r=1$, two steps:
  $b(4,1^s)=(s-2,3,3)$ for $s\equiv1,3\pmod5$ ($s\ge6,8$),
  $b(4,1^s)=(s+1,3)$ for $s\equiv2\pmod5$, $s\ge7$, plus $b(4,1^5)=(3,3,3)$
  and $b(4,1^9)=(5,5,3)$. This is a closed form on an infinite subfamily that
  includes the whole chain, not only one step.

## What is conjecture, and what failed

* **P2** (frozen, open): $b(4^2,1^s)=(s-1,6,3)$ for all $s\equiv2\pmod5$,
  $s\ge7$. Held-out test $s=7..402$: 0 failures, chain length exactly 8 steps
  throughout. Not proved; missing lemma named in the proof file.
* **P3** (REFUTED): the same shape for $r=3$ holds at $s=27,\dots,57$ and
  **fails at $s=62$** ($n=74$), true image $(25,17,8,8,8,8)$ after 1911 steps;
  also fails at $s=67,72,77$.
* $r=1$, $s\equiv0,4\pmod5$: no closed form found; 21 of 80 parameters exceed a
  20000-step cap (largest finite chains 18702 and 15452). $b(4,1^{150})$
  exceeds $10^6$ steps. This is the cost of BZ82 on this family, and it is far
  above the 672 quoted for the ones-ray in RR-C015.
* **Extension question** stated in §8 of the proof file, with the smallest
  parameters ($s=39$, $n=43$; $s=44$, $n=48$) that settle its first open case.

## Proposed change to Main (not made here)

Nothing outside this folder was touched. Suggested ledger entries: RR-C018
(Theorem 1, PROVED, family only), RR-C019 (Theorem 3, PROVED, family only),
RR-C020 (P2, TESTED_FINITE on 80 held-out parameters + refutation P3).
The negative control in `main`'s brief should read: $(11,6,1,1,1)$ **is** in
$A_{20}$ ($11\equiv6\equiv1\equiv1\pmod5$); what is false is placing it in
$(4^r,1^s)$. Also, the longest-path object at $n=30$ cited in RR-C011,
$(4^7,1,1)$, is indeed a member of this family.
