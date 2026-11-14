# Quotations used in `THEOREM.md`, and the two-extractor check

Every displayed formula and sentence used in `THEOREM.md` is listed here with (a) its page in
`attachments/here-are-three-files-ni5n/paper.pdf`, (b) the `pdftotext -layout` extraction, and
(c) the `mutool draw -F txt` extraction. The two extractors are independent implementations; the
formula labels `(5.2)`, `(5.3)`, `(5.7)`, `(6.1)`, `(6.2)`, `(1.1)` and the two prose sentences of
§8/§9.4 are recovered identically by both. No formula in `THEOREM.md` rests on a single
extraction, and none of them is used in a form where the flat text is ambiguous (there is no
fraction, radical, or nested delimiter in any of the five; the only display with a `limsup` is
`(6.1)`, which is quoted below in full).

Command lines used:

```
pdftotext -layout attachments/here-are-three-files-ni5n/paper.pdf out.txt
mutool draw -F txt -o - attachments/here-are-three-files-ni5n/paper.pdf <page>
```

---

## 1. `(5.2)` — Lemma 5.2(1), page 27

`pdftotext -layout`:

```
   1. For almost every independent-angle pair (e, v) ∈ S × S,
                                           c( x + e + v) ∈
                                                         / Px (e) ∪ Px (v).                               (5.2)
```

`mutool draw -F txt`:

```
1. For almost every independent-angle pair (e, v) ∈S × S,

c(x + e + v) /∈Px(e) ∪Px(v).
(5.2)
```

Both readings: `c(x+e+v) not in P_x(e) union P_x(v)`, for a.e. `(e,v) in S x S`, at every fixed
centre `x`. (The `∈ /` of pdftotext is the negated membership symbol split by the layout.)

## 2. `(5.3)` — Lemma 5.2(3), page 27

`pdftotext -layout`:

```
   3. Let z be any fixed center, possibly z = x. Suppose on an open angular arc, or locally on a union of
      such arcs, there is a smooth representation
                                  z + f = x + s ( f ) + t ( f ),   s( f ), t( f ) ∈ S,
      with s( f ), t( f ) nonparallel and s a local diffeomorphism in the angular coordinate. Then almost
      everywhere on that domain,
                                               Pz ( f ) ∩ Px (s( f )) = ∅.                           (5.3)
```

`mutool draw -F txt`:

```
3. Let z be any fixed center, possibly z = x. Suppose on an open angular arc, or locally on a union of
such arcs, there is a smooth representation

z + f = x + s( f ) + t( f ),
s( f ), t( f ) ∈S,

with s( f ), t( f ) nonparallel and s a local diffeomorphism in the angular coordinate. Then almost
everywhere on that domain,
Pz( f ) ∩Px(s( f )) = ∅.
(5.3)
```

## 3. `(5.7)` — Corollary 5.4, page 29

`pdftotext -layout` / `mutool draw -F txt` (identical modulo spacing):

```
Corollary 5.4 (Sixty-degree exclusion). At every fixed center x,
                              Px ( f ) ∩ Px ( R f ) = ∅           for almost every f ∈ S.                (5.7)
Proof. Use x + f = x + R f + R−1 f in Lemma 5.2. The endpoint directions are nonparallel and the
first endpoint map is a rotation.
```

## 4. `(6.1)` — Definition 6.1, page 34

`pdftotext -layout`:

```
Definition 6.1 (Transition graph). For x ∈ R2 , let Γ x be the simple graph on I in which ij is an
edge precisely when, for every ball B centered at x with positive finite radius,
                                                       Dij ( B, h)
                                           lim sup                 > 0.                          (6.1)
                                              h →0       |h|
                                              h ̸ =0
```

`mutool draw -F txt`: the same display with the label `(6.1)` at line 55 of the page; the `limsup`
and the `D_ij(B,h)/|h|` ratio are recovered identically.

## 5. `(6.2)` — Lemma 6.2, page 35

```
Lemma 6.2 (An edge has an avoiding trace). If ij ∈ Γ x , there is a trace bij ∈ W x with bi = b j = 0
almost everywhere. Consequently,
                           Px (e) ̸⊂ {i, j}   for almost every e ∈ S,       ij ∈ Γ x .               (6.2)
```

## 6. `(1.1)` — Theorem 1.3, page 2

```
Theorem 1.3 (Transfer of colorability). For every positive integer k, in ZFC,
                                           a proper k-coloring of R2 exists
                                                         ⇐⇒                                                     (1.1)
                                     a weak measurable k-coloring of R2 exists.
```

## 7. Page 34, the uncountable step of §5.4 (quoted in `THEOREM.md` §8)

`pdftotext -layout`:

```
    The good angles still have positive measure, so they give infinitely many distinct binary centers
on the compact circle x + S. Lemma 5.5 makes these centers uniformly separated. A uniformly
separated subset of a compact metric space is finite, by a finite cover with sufficiently small balls.
This contradiction proves the upper bound.
```

`mutool draw -F txt` (page 34, lines 1-4 and following): the same three sentences, identical
wording.

## 8. Page 5, the finite non-5-colourable graph (quoted in `THEOREM.md` §9.4)

`pdftotext -layout` and `mutool draw -F txt` agree (mutool line 67):

```
Proof. Theorem 1.1 and graph compactness [4, Theorem 1] give a finite unit-distance graph H that
is not five-colorable. Set m = | E( H )| and δ = 1/m. Every five-coloring of H has at least one
monochromatic edge.
```

## 9. Page 27, the non-joint-measurability sentence (quoted in `THEOREM.md` §1, Remark 1.1)

`pdftotext -layout`:

```
The null set in the last assertion may depend on the individual trace, and the angular null sets
may depend on x. We shall use countable generating trace families whenever a conclusion is to be
asserted for the whole palette. No joint measurability of Px in its center is assumed.
```

`mutool draw -F txt`: identical.

## 10. Remark 5.3 on page 29, the `(TE)` instance

```
Remark 5.3. In assertion 3 of Lemma 5.2, the second endpoint map t may be constant. Nonparallel-
ness makes the two-dimensional sum map invertible, while the local diffeomorphism requirement
on s alone controls preimages of angular null sets. In particular, for any fixed direction a, the
representation
                                     ( x + a) + f = x + f + a
is admissible off f = ± a. The proof applies at every fixed pair of centers and never needs a
common exceptional angular set over an uncountable family of centers.
```

Both extractors agree; note the last sentence, which is the paper's own statement of the
"per-pair null sets" convention used in Theorem B's proof.
