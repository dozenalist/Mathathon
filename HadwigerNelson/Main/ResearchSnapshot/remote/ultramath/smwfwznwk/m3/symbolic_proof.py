"""Machine-checked symbolic proof: the 2m-word works for EVERY m >= 6.

Blocks as half-open integer intervals with affine endpoints in m:
    A = {1,3} on [0, m-3)   B = {1,4} on [m-3, m-1)   C = {2,4} on [m-1, 2m-4)
    D = {2,5} on [2m-4, 2m-2)                          E = {3,5} on [2m-2, 2m)
Requirement: for delta in {m-1, m, m+1} and every i mod 2m, W(i) perp W(i+delta),
perp = disjointness = adjacency in the 5-cycle A-C-E-B-D-A.

Every quantity below is affine in m, so every decision is a linear inequality over
m >= 6, decided exactly (see sign_for_m_ge).  Two facts make the reduction finite:
 * the reached interval [loX+delta, hiX+delta) has length < 2m, so it wraps at most
   once around the circle of 2m sectors, and its left endpoint is < 4m;
 * "half-open intervals [p,q) and [x,y) meet" is exactly  p < y and x < q.
"""
import sympy as sp

m = sp.symbols('m', positive=True)
MMIN = 6
blocks = {
    'A': (sp.Integer(0), m - 3),
    'B': (m - 3,         m - 1),
    'C': (m - 1,         2*m - 4),
    'D': (2*m - 4,       2*m - 2),
    'E': (2*m - 2,       2*m),
}
pal = {'A': '13', 'B': '14', 'C': '24', 'D': '25', 'E': '35'}
cyc = ['A', 'C', 'E', 'B', 'D']
def perp(X, Y):
    return ((cyc.index(Y) - cyc.index(X)) % 5) in (1, 4)

def sign_for_m_ge(f):
    """sign of the affine function f on [MMIN, inf): 'pos', 'neg', 'zero', 'mixed'."""
    f = sp.expand(f); a = sp.diff(f, m); b = sp.simplify(f.subs(m, 0))
    if a.is_zero:
        return 'zero' if b == 0 else ('pos' if b > 0 else 'neg')
    v6 = sp.simplify(f.subs(m, MMIN))
    if a.is_positive:
        return 'pos' if v6 > 0 else ('mixed' if v6 < 0 else 'mixed')
    return 'neg' if v6 < 0 else ('mixed' if v6 > 0 else 'mixed')

def meet(p, q, x, y):
    """do [p,q) and [x,y) meet for SOME m >= 6?"""
    # p < y and x < q, allowing uncertainty: report 'yes'/'no'/'maybe'
    s1 = sign_for_m_ge(sp.expand(y - p))     # p < y  <=>  y-p > 0
    s2 = sign_for_m_ge(sp.expand(q - x))     # x < q  <=>  q-x > 0
    if s1 == 'pos' and s2 == 'pos':
        return 'yes'
    if s1 == 'neg' or s1 == 'zero' or s2 == 'neg' or s2 == 'zero':
        return 'no'
    return 'maybe'

def split(lo, hi):
    """pieces of [lo,hi) mod 2m inside [0,2m), for all m >= 6 (list of (p,q))."""
    # normalise left endpoint: lo >= 0 always; lo may be >= 2m (never >= 4m here)
    if sign_for_m_ge(sp.expand(lo - 2*m)) == 'pos':
        lo = sp.expand(lo - 2*m); hi = sp.expand(hi - 2*m)
    s = sign_for_m_ge(sp.expand(hi - 2*m))
    if s in ('neg', 'zero'):
        return [(lo, hi)]
    if s == 'pos':
        return [(lo, 2*m), (sp.Integer(0), sp.expand(hi - 2*m))]
    # mixed: sometimes wraps -> the union of both, handled by caller as {hi<=2m case} u {wrap case}
    return [(lo, 2*m), (sp.Integer(0), sp.expand(hi - 2*m))]

print("blocks:", {k: (sp.sstr(v[0]), sp.sstr(v[1]), pal[k]) for k, v in blocks.items()})
print("perp 5-cycle:", " - ".join(cyc + ['A']), "\n")

allok = True
for X in blocks:
    lox, hix = blocks[X]
    for dname, delta in (('m-1', m - 1), ('m', m), ('m+1', m + 1)):
        lo, hi = sp.expand(lox + delta), sp.expand(hix + delta)
        hit, maybe = set(), set()
        for (p, q) in split(lo, hi):
            for Y in blocks:
                y0, y1 = blocks[Y]
                r = meet(p, q, y0, y1)
                if r == 'yes':
                    hit.add(Y)
                elif r == 'maybe':
                    maybe.add(Y)
        ok = all(perp(X, Y) for Y in hit) and not maybe
        allok &= ok
        print(f"  {X} + ({dname:3s}) [= {sp.sstr(lo)} .. {sp.sstr(hi)}): reaches {sorted(hit)}"
              f"{'  MAYBE ' + str(sorted(maybe)) if maybe else ''}   all perp to {X}: {ok}")
print("\nSYMBOLIC RESULT for every m >= 6:", allok)

# independent numeric corroboration of the same statement

