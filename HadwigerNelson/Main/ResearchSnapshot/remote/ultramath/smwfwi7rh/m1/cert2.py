#!/usr/bin/env python3
"""
Second, independent implementation of the finite enumerations of cert.py.
Deliberately written with bitmask arithmetic and no shared code, so that the
two scripts can be diffed.

Reports, for k = 6 and palettes of size <= 2:
   four-cycle on {0,1,2,3}:   number of admissible palettes, those outside the
                              paper's X/U/V trichotomy, those representing two
                              canonical groups;
   five-cycle on {0,1,2,3,4}: number admissible, number of diagonals, others;
   triangle on {0,1,2}:       number admissible, number hitting the outsider
                              triple {3,4,5}.
"""

K = 6


def bit(c):
    return 1 << c


def contained_in_an_edge(mask, edges):
    return any(mask & ~(bit(u) | bit(v)) == 0 for (u, v) in edges)


def all_masks(max_size):
    out = []
    for m in range(1, 1 << K):
        if bin(m).count("1") <= max_size:
            out.append(m)
    return out


def admissibles(edges, max_size):
    return [m for m in all_masks(max_size) if not contained_in_an_edge(m, edges)]


E4 = [(0, 1), (1, 2), (2, 3), (3, 0)]
E5 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
E3 = [(0, 1), (1, 2), (2, 0)]


def labels(mask):
    return tuple(i for i in range(K) if mask & bit(i))


def report_four():
    A = admissibles(E4, 2)
    X, Y = bit(4), bit(5)
    U, V = bit(0) | bit(2), bit(1) | bit(3)
    outside, ambiguous = [], []
    for m in A:
        paper = None
        if m & X:
            paper = "X"
        elif m == U:
            paper = "U"
        elif m == V:
            paper = "V"
        if paper is None:
            outside.append(labels(m))
        g = 0
        if m & X:
            g += 1
        if m & Y:
            g += 1
        if m & U == U:
            g += 1
        if m & V == V:
            g += 1
        if g >= 2:
            ambiguous.append(labels(m))
    return len(A), sorted(outside), ambiguous


def report_five():
    A = admissibles(E5, 2)
    diags = {bit(i) | bit((i + 2) % 5) for i in range(5)}
    nd = [labels(m) for m in A if m not in diags]
    return len(A), sum(1 for m in A if m in diags), sorted(nd)


def report_three():
    A = admissibles(E3, 2)
    T = bit(3) | bit(4) | bit(5)
    hit = [m for m in A if m & T]
    return len(A), len(hit)


if __name__ == "__main__":
    n4, outside4, amb4 = report_four()
    print("four-cycle |P|<=2: admissible", n4)
    print("  outside X/U/V:", outside4)
    print("  ambiguous:", amb4)
    n5, d5, rest5 = report_five()
    print("five-cycle |P|<=2: admissible", n5, "diagonals", d5)
    print("  others:", rest5)
    n3, h3 = report_three()
    print("triangle |P|<=2: admissible", n3, "hitting outsider triple", h3)
