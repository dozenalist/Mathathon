"""Small exact checks of two specified LOCAL relaxations, not plane colourings.

Only Python's standard library. No SAT solver or numerical geometry is used.
Run time limit is 45 seconds. The printed JSON is independently verifiable.
Source contract is explained in CONTRACT.txt and the lead report.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json
import time

START = time.monotonic()


def check_time():
    if time.monotonic() - START > 45:
        raise RuntimeError("45 second internal limit")


def sign(j, v):
    # sign cos((j-v)*pi/3); cos is 1, 1/2, -1/2 or -1.
    return ((j-v) % 6) in (0, 1, 5)


def allowed(m, dirs, j, side):
    forbidden = set()
    for e in range(m):
        if sign(j, dirs[e]) == side:
            forbidden.update((e, (e+1) % m))
    return set(range(6)) - forbidden


PALETTES = [frozenset(p) for n in (1, 2)
            for p in combinations(range(6), n)]


def verify(m, dirs, palettes):
    edges = [{i, (i+1) % m} for i in range(m)]
    assert len(dirs) == m and len(palettes) == 6
    for j, p in enumerate(palettes):
        assert 1 <= len(p) <= 2
        assert p <= set(range(6))
        assert p.isdisjoint(palettes[(j+1) % 6])
        for e in edges:
            assert not p <= e
        for b in (False, True):
            assert p & allowed(m, dirs, j, b)
        for e in range(m):
            assert sign((j+3) % 6, dirs[e]) != sign(j, dirs[e])


def solve(m):
    # A common rotation lets the first actual unit vector have angle zero.
    for tail in product(range(6), repeat=m-1):
        check_time()
        dirs = (0,) + tail
        options = []
        for j in range(6):
            ap, am = allowed(m, dirs, j, True), allowed(m, dirs, j, False)
            options.append([p for p in PALETTES if p & ap and p & am])
        if any(not row for row in options):
            continue

        def dfs(word):
            j = len(word)
            if j == 6:
                return word if word[-1].isdisjoint(word[0]) else None
            for p in options[j]:
                if word and not p.isdisjoint(word[-1]):
                    continue
                if j == 5 and not p.isdisjoint(word[0]):
                    continue
                found = dfs(word + [p])
                if found is not None:
                    return found
            return None

        word = dfs([])
        if word is not None:
            verify(m, dirs, word)
            return {"cycle_length": m, "vector_angle_units_pi_over_3": dirs,
                    "palettes": [sorted(p) for p in word],
                    "signs": [[int(sign(j, v)) for v in dirs] for j in range(6)]}
    return None


def annulus_exact():
    # Analytic facts used separately in the written proof:
    # cos(2*pi/9) > cos(pi/4) > 2/3;
    # cos(4*pi/9) < cos(5*pi/12) < 1/3.
    # Their elementary radical bounds are checked here rationally.
    assert F(1, 2) > F(4, 9)  # sqrt(2)/2 > 2/3.
    # cos(75)^2=(2-sqrt(3))/4 < 1/9 iff sqrt(3)>14/9.
    assert F(3) > F(14, 9)**2
    inner, outer = F(99, 100), F(101, 100)
    same_sector_sq = (outer-inner)**2 + 2*outer**2*F(1, 3)
    separated_sector_sq = 2*inner**2*F(2, 3)
    assert same_sector_sq < 1 < separated_sector_sq
    # Same colour among nine sectors means equal index modulo three.
    # Different same-colour sectors have circular angular separation >= 80 deg.
    pairs = []
    for a, b in combinations(range(9), 2):
        if a % 3 == b % 3:
            gap = min((b-a) % 9, (a-b) % 9)
            assert gap == 3
            pairs.append([a, b])
    return {"inner_radius": str(inner), "outer_radius": str(outer),
            "same_sector_distance_squared_upper": str(same_sector_sq),
            "different_same_colour_distance_squared_lower": str(separated_sector_sq),
            "same_colour_sector_pairs": pairs,
            "ternary_centre_ball_radius": "1/200"}


if __name__ == "__main__":
    result = {"scope": "Local relaxations only; no global weak plane colouring",
              "annulus": annulus_exact(), "interface_orbits": []}
    for length in range(3, 7):
        witness = solve(length)
        assert witness is not None, ("No model found", length)
        result["interface_orbits"].append(witness)
    result["seconds"] = round(time.monotonic()-START, 6)
    print(json.dumps(result, indent=2))
