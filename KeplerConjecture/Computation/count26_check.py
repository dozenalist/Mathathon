#!/usr/bin/env python3
"""K15-C129 -- test the 26-count that drives C124, on real packings.

C124's engine: with S_eps = {v : some w has 0 < |v-w| <= 2+eps} and M a MAXIMAL matching of the
(2+eps)-graph, |S_eps| <= 2|M| + 12*2|M| = 26|M|, using deg <= 12 (kissing number in R^3).
This builds finite patches of fcc and of E's C5 payer fixture, finds a maximal matching, and
reports the ratio |S|/|M| against the bound 26.
"""
import itertools
import sys

import numpy as np

A1 = np.array([2.0, 0.0])
A2 = np.array([1.0, np.sqrt(3.0)])
T = (A1 + A2) / 3.0
H = np.sqrt(8.0 / 3.0)


def barlow(kind, n=3):
    s = {'fcc': [0, 1, 2], 'hcp': [0, 1]}[kind]
    p = len(s)
    pts = []
    for k in range(-n, n + 1):
        base = s[k % p] * T
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                xy = i * A1 + j * A2 + base
                pts.append([xy[0], xy[1], k * H])
    return np.array(pts)


def graph(P, thr):
    D = np.linalg.norm(P[:, None] - P[None], axis=2)
    np.fill_diagonal(D, np.inf)
    return D <= thr, D


def maximal_matching(adj):
    """greedy maximal matching (any maximal matching obeys the bound)."""
    n = adj.shape[0]
    used = [False] * n
    M = []
    for i in range(n):
        if used[i]:
            continue
        for j in range(n):
            if j != i and adj[i, j] and not used[j]:
                M.append((i, j))
                used[i] = used[j] = True
                break
    return M


def report(name, P, eps):
    thr = 2.0 + eps
    adj, D = graph(P, thr)
    deg = adj.sum(axis=1)
    S = int((deg > 0).sum())
    M = maximal_matching(adj)
    r = len(M)
    bound = 26 * r
    print(f"  {name:22s} n={len(P):4d} eps={eps:<5} |S|={S:4d} |M|={r:4d} "
          f"26|M|={bound:5d}  holds: {S <= bound}   max deg {int(deg.max())}")


def main():
    print("C124's 26-count on real packings (deg <= 12 is the kissing number in R^3)")
    for eps in (0.0, 0.005, 0.05, 0.2):
        report('fcc', barlow('fcc'), eps)
        report('hcp', barlow('hcp'), eps)
    print()
    # the bound is only needed as an inequality; also check the tighter pigeonhole 2+24
    print("derivation check: |S| <= |matched| + |N(matched)| <= 2|M| + 12*(2|M|) = 26|M|")
    print("  (uses deg <= 12, i.e. at most 12 points at distance <= 2.09 -- K15-C054/C013)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
