"""Checker A (primary): the sector word satisfies every condition, by label bitmasks."""
import sys
sys.path.insert(0,'work')
from word import *

def check(w, m, quiet=True):
    n = 6*m; bad = []
    if len(w) != n: bad.append(f"length {len(w)} != {n}")
    V = set(domain(sizes=(2,3)))
    for i,S in enumerate(w):
        S = frozenset(S)
        if S not in V: bad.append(f"value {sorted(S)} at sector {i} is not an admissible pair")
        if 0 in S:    bad.append(f"free label 0 in palette at sector {i}")
        if len(S)!=2: bad.append(f"palette size {len(S)} at sector {i} (m2 forces pairs)")
    for o in offsets(m):
        if o % n == 0: bad.append("degenerate offset 0")
        for i in range(n):
            j = (i+o) % n
            if w[i] & w[j]: bad.append(f"palettes at {i},{j} (offset {o}) meet: "
                                       f"{sorted(w[i])} {sorted(w[j])}")
    # (5.7) rotation by pi/3 = shift by m sectors
    for i in range(n):
        if w[i] & w[(i+m) % n]: bad.append(f"(5.7) fails at {i}")
    if not quiet and bad: print("\n".join(bad[:20]))
    return (not bad), bad

if __name__=='__main__':
    for m in range(5, 201):
        ok,bad = check(uniform_word(m), m)
        assert ok, (m, bad[:4])
    print("checker A: uniform word w_m valid for every m = 5..200")
