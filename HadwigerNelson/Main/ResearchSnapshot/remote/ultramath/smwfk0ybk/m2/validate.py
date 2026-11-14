"""Independent re-check of every witness in witnesses.json, from the geometric definition.

Ray cells: ray j lies in cell c_j, i.e. its angle theta_j satisfies
    theta_j in ( (c_j + 1/2)*pi/3 , (c_j + 3/2)*pi/3 )     (m5/INTERFACE-NOGO.md, 'Ray data').
We do NOT use the closed-form table: for each ray we evaluate sign(cos(theta - i*pi/3)) at
40 sample angles strictly inside the cell and check that all of them agree (constancy on the
cell), then use that sign for sigma_j^(i).  Labels are named 0..k-1.
"""
import json, math

K = 6
def signs_of_cell(c):
    """signs[i][j] for i = 0..5 : sign(f_i . v_j), f_i at angle i*pi/3."""
    lo = (c + 0.5) * math.pi / 3
    hi = (c + 1.5) * math.pi / 3
    out = []
    for i in range(5+1):
        vals = set()
        for t in range(1, 41):
            th = lo + (hi - lo) * t / 41
            x = math.cos(th - i * math.pi / 3)
            vals.add(1 if x > 1e-9 else (-1 if x < -1e-9 else 0))
        assert len(vals) == 1, (c, i, vals)   # sign is constant on the open cell, never 0
        out.append(vals.pop())
    return out

def OI(ell, cells):
    U = set(range(ell, K))
    Os, Is = [], []
    # sigma_j^(i) = sign(f_i . v_j) depends on ray j's cell and on the direction index i
    sig = [signs_of_cell(cells[j]) for j in range(ell)]      # sig[j][i]
    for i in range(6):
        O, I = set(U), set(U)
        for j in range(ell):
            a, b = sig[(j-1) % ell][i], sig[j][i]      # sigma_(j-1)^(i), sigma_j^(i)
            if a == -1 and b == -1: O.add(j)
            if a ==  1 and b ==  1: I.add(j)
        Os.append(O); Is.append(I)
    return Os, Is

def check(name, w):
    ell, cells, P = w['l'], tuple(w['cells']), [set(p) for p in w['P']]
    Os, Is = OI(ell, cells)
    fails = []
    assert len(P) == 6
    for i in range(6):
        if not (1 <= len(P[i]) <= K-3): fails.append(f'C1 at {i}: |P|={len(P[i])}')
        if not (P[i] & Os[i]): fails.append(f'C2 O at {i}: {P[i]} & {Os[i]}')
        if not (P[i] & Is[i]): fails.append(f'C2 I at {i}: {P[i]} & {Is[i]}')
        if P[i] & P[(i+1) % 6]: fails.append(f'C3 at {i}: {P[i]} & {P[(i+1)%6]}')
    tern = sum(1 for p in P if len(p) == 3)
    comp = [(a, b) for a in range(6) for b in range(a+1, 6)
            if len(P[a]) == 3 == len(P[b]) and (P[a] | P[b]) == set(range(K))]
    C4 = not comp; C5 = tern <= 3
    mean = sum(len(p) for p in P) / 6
    print(f'{name}: l={ell} cells={cells} P={[sorted(p) for p in P]}')
    print(f'   C1,C2,C3 fail: {fails if fails else "none"} | #ternary={tern} C4={C4} C5={C5} '
          f'mean={mean:.3f} complementary_pairs={comp}')
    return not fails, C4, C5, tern, comp

if __name__ == '__main__':
    D = json.load(open('witnesses.json'))
    print('=== SAT witnesses: must satisfy C1..C5 ===')
    for w in D['SAT_witnesses_C1_to_C5']:
        ok, C4, C5, tern, comp = check('SAT', w)
        assert ok and C4 and C5, 'SAT witness fails'
    print('=== non-redundancy: C1,C2,C3 hold, C4 fails ===')
    for w in D['C1_C2_C3_but_NOT_C4_adjacent_pair']:
        ok, C4, C5, tern, comp = check('ADJ', w); assert ok and not C4
        assert any(b-a == 1 for a, b in comp), 'expected an adjacent complementary pair'
    for w in D['C1_C2_C3_C5_but_NOT_C4_far_pair']:
        ok, C4, C5, tern, comp = check('FAR', w); assert ok and not C4 and C5
        assert all((b-a) in (2, 3, 4) for a, b in comp), 'expected only non-adjacent pairs'
    print('=== (C5) is not implied by (C1)-(C3) ===')
    for w in D['C1_C2_C3_but_NOT_C5_four_ternary']:
        ok, C4, C5, tern, comp = check('NOTC5', w); assert ok and not C5 and tern == 4
    print('=== mean-bound defect: >=4 ternary with mean <= 5/2 ===')
    for w in D['mean_bound_defect_orbit']:
        ok, C4, C5, tern, comp = check('MEAN', w)
        assert tern >= 4 and sum(len(p) for p in w['P']) / 6 <= 2.5
    print('=== extremal survivors: exactly 3 ternary, all six labels, C1-C5 ===')
    for w in D['extremal_survivors_three_ternary_all_labels']:
        ok, C4, C5, tern, comp = check('EXT', w)
        assert ok and C4 and C5 and tern == 3
        assert len(set().union(*[set(p) for p in w['P']])) == 6
    print('\nALL WITNESS CHECKS PASS')
