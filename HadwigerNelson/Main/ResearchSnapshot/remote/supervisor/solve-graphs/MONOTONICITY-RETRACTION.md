# Retraction: I had the monotonicity of forced equality backwards

## The error
In `NEXTSTEP-CORRECTION.md` I wrote that "forced-ness is monotone **upward** in `k` ... so a
`k`-forced pair stays forced at `k+1`". **That is false and is retracted.**

The `k`-colourings are a subset of the `(k+1)`-colourings, so a statement of the form *"every
`k`-colouring does X"* does **not** transfer to `(k+1)`-colourings. Forced equality has exactly that
form. It is **non-forcing** that is preserved upward: if some `k`-colouring separates `p` and `q`,
that same colouring is a `(k+1)`-colouring separating them.

So the correct directions are:

* **forcing is downward-closed in `k`** (forced at `k` does not imply forced at `k+1`);
* **non-forcing is upward-closed in `k`** (not forced at `k` implies not forced at `k+1`).

The second is exactly the corollary I correctly used for the 553-vertex certificate: the
34 witnesses are proper 5-colourings, hence proper `k`-colourings for `k >= 5`, so the `k >= 5`
statement stands. That part was sound.

## The sharp lemma this gives, and what it forbids
**Lemma.** If `G` is `(k-1)`-colourable, then no pair of distinct vertices is forced equal at `k`.

*Proof.* Let `c` be a proper `(k-1)`-colouring using colours `1..k-1`, and let `p, q` be distinct. If
`c(p) != c(q)` we are done. Otherwise let `alpha = c(p) = c(q)` and recolour `p` with the spare colour
`k`. Every neighbour of `p` has colour in `1..k-1` and none has colour `alpha`, so colour `k` is unused
on `N(p)`: the result is a proper `k`-colouring, and it separates `p` from `q`. ∎

**Consequence, which decides the seed question.** A non-vacuous forced-equality candidate at `k = 5`
requires a graph that is **not** 4-colourable, i.e. `chi(G) >= 5`. A 4-colourable seed is therefore
**useless** for `k = 5` forcing — not merely weak, but provably incapable of exhibiting one. This
retracts the framing of my earlier `GADGET_4`-first recommendation as a route to a `k = 5` pair, and it
is why the seed for this block must contain the 5-chromatic `H` as an induced subgraph.

## Scope of the retraction
It does **not** damage the accepted certificate (which is a `k >= 5` statement and uses only the
upward-preserving direction). It damages only my earlier prose about "monotone upward", and the
suggestion that a 4-colourable configuration could serve a `k = 5` forced-pair search.
