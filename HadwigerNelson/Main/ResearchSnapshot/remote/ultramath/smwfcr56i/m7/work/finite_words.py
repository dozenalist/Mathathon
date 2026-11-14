"""
Exhaustive checks of the two finite combinatorial claims of section 8 that the paper settles by
one-line pigeonhole arguments.

(8.2) five-cycle (Prop. 8.2).  Steps eps_j in {+1,-1}, j in Z/6Z, palette index
      p_{j+1} = p_j + eps_j (mod 5), closing after six steps; antipodal positions j and j+3
      must have index difference in {0,+-2} mod 5.  Claim: no such sequence.

(8.3) four-cycle (Lemma 8.3).  A word w in {X,U,V}^6 with
      (i)  w_j != w_{j+1} for all j            (the state changes under R, (8.2)),
      (ii) w_j = w_{j+3} whenever w_j != X     (antipodal equality, (8.2)).
      The paper's dichotomy is: either all X-positions have the same parity, or the word is a
      3-periodic permutation of X,U,V (which is then excluded separately by the cross-word
      restriction).  We verify the dichotomy exhaustively.
"""
import itertools

print("=== (8.2) five-cycle: no closed step sequence ===")
sols = []
for eps in itertools.product((1, -1), repeat=6):
    if sum(eps) % 5 != 0:
        continue
    triples = [sum(eps[j] for j in range(j, j+3)) if j + 3 <= 6 else
               sum(eps[(j + i) % 6] for i in range(3)) for j in range(6)]
    if all(s % 5 in (0, 2, 3) for s in triples):
        sols.append(eps)
print("   closed step sequences satisfying the antipodal rule:", sols)
print("   (each triple sum lies in {-3,-1,1,3} and only +-3 are congruent to 0 or +-2 mod 5,")
print("    so every three consecutive signs agree; hence all six agree and the sum is +-6 != 0)")

print()
print("=== (8.3) four-cycle: the parity dichotomy ===")
admissible = []
for w in itertools.product('XUV', repeat=6):
    if any(w[j] == w[(j+1) % 6] for j in range(6)):
        continue
    if any(w[j] != 'X' and w[j] != w[(j+3) % 6] for j in range(6)):
        continue
    admissible.append(w)
print("   admissible words:", admissible)
threeper = [w for w in admissible if all(w[j] == w[(j+3) % 6] for j in range(3))]
onepar = [w for w in admissible if len({j % 2 for j in range(6) if w[j] == 'X'}) == 1]
noparity = [w for w in admissible if len({j % 2 for j in range(6) if w[j] == 'X'}) > 1]
print("   of these, 3-periodic (X on both parities):", len(threeper), threeper)
print("   of these, X on a single parity          :", len(onepar))
print("   with no X at all                        :", [w for w in admissible if 'X' not in w])
print("   dichotomy holds (every word either 3-periodic or X on one parity):",
      len(threeper) + len(onepar) == len(admissible))
