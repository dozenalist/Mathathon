#!/usr/bin/env python3
"""Exact decision of the single-centre palette state systems at a cyclic centre.

Model.  Labels I = range(k).  Directions are the six elements t = 0..5 of one
R-orbit (R = rotation by kappa = pi/3, order six).  A model assigns to each
direction a palette P(t), a nonempty subset of I.  Constraints:

  (EX60)  P(t) & P(t+1) = {}            -- paper (5.7), 60 degrees
  (EX120) does not exist: at a single centre (5.3) with z = x gives
           x + F = x + s(F) + t(F) with |s| = |t| = |F| = 1, whose solutions
           have s, t at 60 degrees from F; so it republishes (EX60).
  (NC)    P(t) | P(u) != I for all t,u  -- paper (5.2): x+e+v has a colour
                                           outside P(e) | P(v)
  (BOUND) |P(t)| <= k-3                 -- general-k palette bound
  (CYC)   no edge of the label cycle C sits inside P(t)   -- paper (6.2)

Every one of the five is a consequence of the paper's hypotheses at every fixed
centre for a weak measurable k-colouring.  (EX60), (NC), (BOUND) hold for
almost every direction; they are imposed here on all six positions of the
orbit, so the finite model is a *strengthening* of the paper's constraints.
A satisfiable finite model therefore certifies that the paper's constraints do
not refute it.  (A model of the full plane would need the joint and the
a.e.-strength structure; none is claimed here.)

Two independent decision procedures:
  A. streaming depth-first enumeration with incremental pruning;
  B. 0/1 integer programming solved by scipy.optimize.milp (HiGHS).
"""
import itertools
import json

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def popcount(m):
    return bin(m).count("1")


def palettes(k, cycle):
    """Nonempty S with |S| <= k-3 and S not contained in an edge of the cycle.

    (6.2) of the paper reads P_x(e) not-a-subset-of {i,j} for every cycle edge
    i j, so the condition is S <= edge being forbidden, not edge <= S.
    """
    edges = set()
    L = len(cycle)
    for j in range(L):
        edges.add(frozenset((cycle[j], cycle[(j + 1) % L])))
    out = []
    for m in range(1, 1 << k):
        if popcount(m) > k - 3:
            continue
        S = frozenset(i for i in range(k) if m >> i & 1)
        if any(S <= e for e in edges):
            continue
        out.append(m)
    return out


PAIRS = {}


def pairs_of(k):
    if k not in PAIRS:
        PAIRS[k] = [m for m in range(1, 1 << k) if popcount(m) == 2]
    return PAIRS[k]


def stream_models(k, allowed, sink):
    """Procedure A: streaming DFS over the six positions of one R-orbit."""
    full = (1 << k) - 1
    assign = []

    def rec():
        t = len(assign)
        if t == 6:
            if assign[0] & assign[5]:
                return
            sink(tuple(assign), full, pairs_of(k))
            return
        for m in allowed:
            bad = False
            if t - 1 >= 0 and assign[t - 1] & m:
                bad = True
            if bad:
                continue
            for m2 in assign:
                if (m | m2) == full:
                    bad = True
                    break
            if bad:
                continue
            assign.append(m)
            rec()
            assign.pop()

    rec()


def brute_force_models(k, allowed):
    """Independent plain enumeration, used only when the space is small."""
    full = (1 << k) - 1
    sols = []
    for tup in itertools.product(allowed, repeat=6):
        good = True
        for t in range(6):
            if tup[t] & tup[(t + 1) % 6]:
                good = False
                break
        if not good:
            continue
        for a in range(6):
            for b in range(6):
                if (tup[a] | tup[b]) == full:
                    good = False
                    break
            if not good:
                break
        if good:
            sols.append(tup)
    return sols


def _base_rows(k, allowed, A, nv, big):
    rows, lo, hi = [], [], []

    def row(coefs, l, h):
        r = np.zeros(nv)
        for idx, v in coefs:
            r[idx] = v
        rows.append(r); lo.append(l); hi.append(h)

    for t in range(6):
        row([(t * A + i, 1) for i in range(A)], 1, 1)
    for t in range(6):
        u = (t + 1) % 6
        if t < u:
            for i in range(A):
                for j in range(A):
                    if allowed[i] & allowed[j]:
                        row([(t * A + i, 1), (u * A + j, 1)], -np.inf, 1)
    for t in range(6):
        for u in range(t, 6):
            for i in range(A):
                for j in range(A):
                    if (allowed[i] | allowed[j]) == big:
                        row([(t * A + i, 1), (u * A + j, 1)], -np.inf, 1)
    return rows, lo, hi


def milp_max_heavy(k, allowed, heavy_pred):
    A = len(allowed)
    nv = 6 * A
    big = (1 << k) - 1
    rows, lo, hi = _base_rows(k, allowed, A, nv, big)
    c = np.zeros(nv)
    for t in range(6):
        for i in range(A):
            if heavy_pred(allowed[i]):
                c[t * A + i] = -1.0
    res = milp(c=c, constraints=LinearConstraint(np.array(rows), np.array(lo), np.array(hi)),
               integrality=np.ones(nv), bounds=Bounds(0, 1))
    return (int(round(-res.fun)), "ok") if res.success else (None, str(res.message)[:100])


def milp_exists_no_hitting_pair(k, allowed):
    A = len(allowed)
    nv = 6 * A
    big = (1 << k) - 1
    rows, lo, hi = _base_rows(k, allowed, A, nv, big)
    for H in pairs_of(k):
        coefs = [(t * A + i, 1) for t in range(6) for i in range(A) if allowed[i] & H == 0]
        if not coefs:
            return False, "no allowed palette avoids pair %s" % bin(H)
        r = np.zeros(nv)
        for idx, v in coefs:
            r[idx] = v
        rows.append(r); lo.append(1); hi.append(np.inf)
    res = milp(c=np.zeros(nv), constraints=LinearConstraint(np.array(rows), np.array(lo), np.array(hi)),
               integrality=np.ones(nv), bounds=Bounds(0, 1))
    return bool(res.success), ("ok" if res.success else str(res.message)[:100])


def analyse(k, cycle, cross_check=False):
    allowed = palettes(k, cycle)
    heavy = lambda m: popcount(m) == k - 3

    stats = dict(n_models=0, max_heavy=-1, best_heavy_example=None,
                 n_no_hit=0, no_hit_example=None,
                 best_class={m: 0 for m in allowed})
    prs = pairs_of(k)

    def sink(tup, full, _pairs):
        stats["n_models"] += 1
        h = sum(1 for m in tup if heavy(m))
        if h > stats["max_heavy"]:
            stats["max_heavy"] = h
            stats["best_heavy_example"] = [bin(m) for m in tup]
        if not [H for H in prs if all(m & H for m in tup)]:
            stats["n_no_hit"] += 1
            if stats["no_hit_example"] is None:
                stats["no_hit_example"] = [bin(m) for m in tup]
        for m in set(tup):
            c = sum(1 for x in tup if x == m)
            if c > stats["best_class"][m]:
                stats["best_class"][m] = c

    stream_models(k, allowed, sink)

    out = dict(k=k, cycle=list(cycle), n_allowed=len(allowed),
               n_allowed_heavy=sum(1 for m in allowed if heavy(m)),
               n_models=stats["n_models"], max_heavy=stats["max_heavy"],
               best_heavy_example=stats["best_heavy_example"],
               n_no_hit=stats["n_no_hit"], no_hit_example=stats["no_hit_example"],
               max_class_over_directions={bin(m): c for m, c in sorted(stats["best_class"].items()) if c})
    if cross_check and len(allowed) ** 6 <= 2_000_000:
        bf = brute_force_models(k, allowed)
        assert len(bf) == stats["n_models"], (len(bf), stats["n_models"])
        out["cross_checked_bruteforce"] = len(bf)
    return out, allowed, heavy


def main():
    results = []
    print("=" * 74, flush=True)
    print("k = 5 (the paper's case), triangle cycle", flush=True)
    r, allowed, heavy = analyse(5, [0, 1, 2], cross_check=True)
    print(json.dumps(r, indent=1)[:2200], flush=True)
    results.append(r)
    for cyc in ([0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5]):
        print("=" * 74, flush=True)
        print("k = 6, cycle", cyc, flush=True)
        r, allowed, heavy = analyse(6, cyc)
        print(json.dumps(r, indent=1)[:2200], flush=True)
        mh, msg = milp_max_heavy(6, allowed, heavy)
        print("  [B] MILP max #{|P| = 3} per orbit:", mh, "| DFS:", r["max_heavy"], msg, flush=True)
        ex, msg2 = milp_exists_no_hitting_pair(6, allowed)
        print("  [B] MILP: model with no hitting pair exists:", ex, "| DFS count:",
              r["n_no_hit"], msg2, flush=True)
        results.append({kk: vv for kk, vv in r.items() if kk != "max_class_over_directions"})
    print("=" * 74, flush=True)
    print("k = 7, triangle cycle: mechanism check (heavy = |P| = k-3 = 4)", flush=True)
    allowed7 = palettes(7, [0, 1, 2])
    mh, msg = milp_max_heavy(7, allowed7, lambda m: popcount(m) == 4)
    print("  [B] MILP max #{|P| = 4} per orbit:", mh, msg, flush=True)
    results.append(dict(k=7, cycle=[0,1,2], n_allowed=len(allowed7), milp_max_heavy=mh))
    with open("verify/state_models_results.json", "w") as f:
        json.dump(results, f, indent=1)
    print("\nwrote verify/state_models_results.json", flush=True)


if __name__ == "__main__":
    main()
