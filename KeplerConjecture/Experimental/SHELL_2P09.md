# Thin-shell lemma at rho = 209/100

Role E. `K15-E014`. Status: **PROVED** — the directed enclosure is now supplied in
`Experimental/TAMMES13_ENCLOSURE.md` and `scripts/tammes13_enclosure.py` (rational
interval arithmetic, 0.25 s, margin `+3.8e-04`).
Reviewer: X. Local request: `Experimental/LOCAL_SHELL_2P09.md`.

## Target

For every 2-separated set, **at most 12 centres lie in the closed shell `[2, 2.09]`**
about any centre. This is the shell width the local-star and local-mass routes need.

## The exact rational endpoint

With `rho = 209/100` and `R = rho`, `K15-E011` in its valid range
(`delta = 0.09 <= sqrt5 - 1 = 1.2360679...`) gives

```
cos(theta_min) = 1 - 2/R^2 = 1 - 2/(209/100)^2 = 1 - 20000/43681 = 23681/43681,
```

**an exact rational**, with

```
23681/43681 = 0.542135024381310...        theta_min = arccos(23681/43681) = 57.1709021867... deg.
```

Both evaluated symbolically here; `23681` and `43681 = 209^2` are exact and the decimal
expansion is not used in the argument. The maximum in `K15-E011` is attained at `r = s = R`
because `R = 2.09 < 1 + sqrt5`, verified by
`1 - 2/R^2 - R/4 = 23681/43681 - 209/400 = +0.0196... > 0`.

## The external input

Musin and Tarasov, *The strong thirteen spheres problem*, arXiv:1002.1439v3, Theorem 1 in
Section 2 (printed p. 3), with the constant defined in the preceding Remark. The theorem
identifies the maximal minimal angular separation of thirteen points on `S^2` — the Tammes
`N = 13` problem — and its value is quoted as approximately `57.1367 deg`.

**Two disclosures, both required before use.** Both are now discharged in
`TAMMES13_ENCLOSURE.md`; the paragraphs below record the original requirement.

1. **A rounded decimal is not an upper enclosure.** The argument below needs
   `theta_13^+ < 57.1709 deg`, i.e. a *certified upper* bound on the true value with at
   least `0.034 deg` of slack. The published digits `57.1367` are consistent with that but
   do not establish it, because rounding direction is unknown and the true value could lie
   anywhere in `[57.13665, 57.13675]`.
2. **The source is computer-assisted.** Musin–Tarasov's result rests on an enumeration of
   combinatorial cases. The enclosure we need must either come from their stated
   enumeration (with the enumeration checked) or be derived independently from the
   defining equations of the extremal configuration. This is a dependency of the lemma,
   not a detail.

## The margin, stated honestly

```
theta_min(0.09) - 57.1367 deg = 0.034202187 deg = 0.0005969 rad.
```

The slack is **0.034 degrees**, or `1.0 * 10^-4` relative. Any certified enclosure must
resolve `theta_13` to better than that. This is why a rounded source value cannot be used
and why the local request below asks for directed interval arithmetic rather than a
floating-point recomputation.

## The lemma

**Proposition `K15-E014` (PROVED, conditional on `theta_13^+ < 57.1709 deg`).** Let
`Lambda` be 2-separated and `x in Lambda`. If some certified bound gives
`theta_13^+ < arccos(23681/43681)`, then `#{y in Lambda : 2 <= |y-x| <= 2.09} <= 12`.

*Proof.* Suppose 13 such `y`. By `K15-E011` every pair satisfies
`cos theta <= max(1 - 2/R^2, R/4) = 23681/43681`, so `theta >= arccos(23681/43681)`.
But thirteen points on the unit sphere satisfy `theta <= theta_13^+ < arccos(23681/43681)`,
a contradiction. ∎

## Equality fixtures

FCC and HCP: 12 centres at distance exactly `2`, next shell `2 sqrt 2 = 2.8284`, so the
count is exactly 12 on `[2, 2.09]` — the bound is **attained**, which is the strongest
possible check that it is compatible with the equality family. Barlow stackings are not
settled here (`K15-E013`); a stacking with a shell inside `[2, 2.09]` beyond the 12
contacts would refute the proposition, and that is a concrete finite test for C/X.

## What this does and does not give

It gives a finite local star: every centre has at most 12 neighbours within `2.09`, so a
local score sees a bounded star. It does **not** give a density bound, does not simplify
Hales's global argument, and its constant `2.09` is a choice, not an optimum. I claim no
novelty: the statement is the classical kissing-with-tolerance question, and the only
new content is the exact rational endpoint and the explicit directed-enclosure
requirement.

## Interval handoff

`Experimental/scripts/shell_2p09_interval.py` computes `arccos(23681/43681)` and the
slack with directed rounding, and prints rational-arithmetic cross-checks. A certified
`theta_13^+` enclosure must come from the local request, not from this script.
