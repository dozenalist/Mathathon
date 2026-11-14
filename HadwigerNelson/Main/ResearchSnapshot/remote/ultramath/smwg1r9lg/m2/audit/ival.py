"""Exact rational interval algebra on the circle of directions (degrees, mod 360)."""
from fractions import Fraction as F

def norm(iv):
    """normalise a list of (lo,hi) rational intervals modulo 360, merged."""
    out = []
    for lo, hi in iv:
        lo, hi = F(lo), F(hi)
        if hi - lo >= 360:
            return [(F(0), F(360))]
        a = lo % 360
        rem = hi - lo
        while rem > 0:
            take = min(F(360) - a, rem)
            out.append((a, a + take))
            rem -= take
            a = F(0)
    out.sort()
    merged = []
    for lo, hi in out:
        if merged and lo <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged

def inter(P, Q):
    P, Q = norm(P), norm(Q)
    out = []
    for a1, a2 in P:
        for b1, b2 in Q:
            lo, hi = max(a1, b1), min(a2, b2)
            if hi > lo:
                out.append((lo, hi))
    return norm(out)

def rotate(E, s):
    """E - s  (mod 360)"""
    s = F(s)
    return norm([(lo - s, hi - s) for lo, hi in norm(E)])

def diff(P, Q):
    """{q - p mod 360} for p in P, q in Q."""
    out = []
    for p1, p2 in norm(P):
        for q1, q2 in norm(Q):
            out.append((q1 - p2, q2 - p1))
    return norm(out)

def contains(E, lo, hi):
    """is the whole closed interval [lo,hi] inside E up to its interior?"""
    E = norm(E)
    lo, hi = F(lo) % 360, F(hi) % 360
    if hi < lo:            # wraps
        return contains(E, lo, F(360)) and contains(E, F(0), hi)
    for a, b in E:
        if a <= lo and hi < b:
            return True
    return False

def member(E, x):
    x = F(x) % 360
    return any(a <= x < b for a, b in norm(E))

def width(E):
    return sum(hi - lo for lo, hi in norm(E))

def maxint(E):
    E = norm(E)
    return max(E, key=lambda t: t[1] - t[0])

# ---------------------------------------------------------------- models -----
def sector_word(values, n=36, L=4):
    """values: list of 3 iterables; block length L sectors of 10 degrees, period 120 deg."""
    sets = [frozenset(v) for v in values]
    return [sets[(i // L) % 3] for i in range(n)]

def word_from_spec(spec, n=36):
    return [frozenset(s) for s in spec]

def dirset(word, value, n=36):
    step = F(360, n)
    out, i = [], 0
    while i < n:
        if word[i] == value:
            j = i
            while j + 1 < n and word[j + 1] == value:
                j += 1
            out.append((i * step, (j + 1) * step))
            i = j + 1
        else:
            i += 1
    return norm(out)

# the models named in the record -------------------------------------------------
BLOCK_MODELS = {
 "TheoremC/m15 block ell=3": [(0,3),(1,4),(2,5)],
 "TheoremC/m15 block ell=4": [(0,2),(1,4),(3,5)],
 "TheoremC/m15 block ell=5": [(0,2),(1,3),(4,5)],
 "TheoremC/m15 block ell=6": [(0,3),(1,4),(2,5)],
 "FREE-LABEL block ell=3":   [(3,),(4,),(5,)],
 "FREE-LABEL block ell=4":   [(0,2),(1,3),(4,)],
 "FREE-LABEL block ell=5":   [(0,2),(1,3),(5,)],
}
# the CURRENT ell=6 free-label word (FREE-LABEL.md, "withdrawn" replacement): period 12
WORD6_NEW = [[1,3],[1,3],[1,3],[1,4],[1,4],[2,4],[2,4],[2,4],[2,5],[2,5],[3,5],[3,5]] * 3
# the WITHDRAWN ell=6 word still used by m11/model_radii.py and m12/verify.py
WORD6_OLD = [[3,5],[3,5],[2,5],[2,5],[2,4],[2,4],[2,4],[1,4],[1,4],[1,3],[1,3],[1,3],
             [3,5],[3,5],[2,5],[2,5],[2,4,5],[2,4],[2,4],[1,4],[1,4],[1,3],[1,3],[1,3],
             [3,5],[3,5],[2,5],[2,5],[2,4],[2,4],[2,4],[1,4],[1,4],[1,3],[1,3],[1,3]]
# m13 singleton triangle field: P(t) = {4 + floor(9t/2pi) mod 3}
WORD_M13 = []
for _i in range(36):
    _s = (9 * (2 * _i + 1)) // (2 * 36) % 3       # s at the sector midpoint
    WORD_M13.append([4 + _s])

def models():
    M = {}
    for name, vals in BLOCK_MODELS.items():
        M[name] = sector_word(vals)
    M["FREE-LABEL ell=6 (current word)"] = word_from_spec(WORD6_NEW)
    M["FREE-LABEL ell=6 (withdrawn word)"] = word_from_spec(WORD6_OLD)
    M["m13 singleton triangle"] = word_from_spec(WORD_M13)
    return M

if __name__ == "__main__":
    for name, w in models().items():
        vals = sorted(set(w), key=lambda s: (len(s), sorted(s)))
        print("%-36s values=%s" % (name, [sorted(v) for v in vals]))
