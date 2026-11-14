#!/usr/bin/env python3
"""
Bounded global search for a completion of the icosahedral cluster that beats the
C5-symmetric one.  Refutation test for (P') at the icosahedral pair.

Fixed: c and the five ring centres (the cluster's six neighbours of the payer w1).
Free: up to MAXFREE further centres, each legal (>= 2 from w1, from the fixed six and
from each other).  Objective: vol Omega(w1).  Refutation if the best legal value
< 5.763417471.

Bounded by design: --seconds cap, single core, no I/O inside the loop.  Started from the
C5 optimum and from random configurations, so it is not a local search around one basin.

Usage: python3 c5_global_search.py --seconds 900 [--seed 0]
Exit 0 always; prints the best legal value found and whether (P') is refuted.
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c5_fixture import C, W1, RING, SOUTH, cell_of

NEED = 5.763417470466
V_DOD = 5.5502910285155
MAXFREE = 10


def vol_of(free):
    F = [C] + RING + list(free)
    v, vol, rmax, bounded = cell_of(W1, F)
    if not bounded or not np.isfinite(vol) or rmax > 2.0:
        return np.inf
    return vol


def legal(free):
    pts = np.array([C, W1] + RING + list(free))
    d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    return d.min() >= 2.0 - 1e-9, d.min()


def random_in_shell(rng, rmax=2.8):
    u = rng.normal(size=3)
    u /= np.linalg.norm(u)
    return W1 + u * (2.0 + rng.random() * (rmax - 2.0))


def run(seconds, seed=0, verbose=True):
    rng = np.random.default_rng(seed)
    th = np.radians(112)
    c5 = [W1 + 2 * np.array([np.sin(th) * np.cos(np.radians(36 + 72 * k)),
                             np.sin(th) * np.sin(np.radians(36 + 72 * k)),
                             -np.cos(th)]) for k in range(5)] + [SOUTH]
    cur = list(c5) if seed % 2 == 0 else []
    while len(cur) < 6:                     # top up with legal random centres
        z = random_in_shell(rng)
        if legal(cur + [z])[0]:
            cur.append(z)
    cv = vol_of(cur)
    best = (cv, list(cur))
    t0 = time.time()
    it = 0
    T0, T1 = 0.06, 5e-4
    while time.time() - t0 < seconds:
        frac = (time.time() - t0) / seconds
        T = T0 * (T1 / T0) ** frac
        it += 1
        r = rng.random()
        cand = list(cur)
        if r < 0.15 and len(cand) < MAXFREE:
            cand.append(random_in_shell(rng))
        elif r < 0.25 and len(cand) > 0:
            cand.pop(int(rng.integers(len(cand))))
        elif len(cand) == 0:
            continue
        else:
            i = int(rng.integers(len(cand)))
            step = 0.35 * (0.08 ** rng.random())
            q = cand[i] + step * rng.normal(size=3)
            rho = np.linalg.norm(q - W1)
            if rho < 2.0:
                q = W1 + (q - W1) / rho * 2.0
            if rho > 3.2:
                continue
            cand[i] = q
        ok, _ = legal(cand)
        if not ok:
            continue
        v = vol_of(cand)
        if not np.isfinite(v):
            continue
        if v < cv or rng.random() < np.exp(-(v - cv) / max(T, 1e-4)):
            cur, cv = cand, v
            if v < best[0]:
                best = (v, list(cand))
                if verbose:
                    print(f"  [{time.time()-t0:7.1f}s] new best {v:.9f} "
                          f"({len(cand)} free centres) refutes={v < NEED}", flush=True)
    ok, m = legal(best[1])
    return dict(seconds=seconds, seed=seed, iterations=it, best=best[0],
                n_free=len(best[1]), minsep=m, legal=bool(ok),
                refutes=bool(best[0] < NEED), gap_to_need=best[0] - NEED,
                config=[[float(x) for x in p] for p in best[1]])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=600)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    print(f"seeded search: fixed c + 5 ring; free <= {MAXFREE} centres in 2 <= |z-w1| <= 2.8")
    print(f"need < {NEED:.9f} to refute (P'); V_dodeca floor {V_DOD:.9f}")
    res = run(a.seconds, a.seed)
    print(f"\nbest {res['best']:.9f} with {res['n_free']} free centres; "
          f"legal={res['legal']} minsep={res['minsep']:.9f}")
    print(f"  refutes (P')? {res['refutes']}   gap to the threshold {res['gap_to_need']:+.9f}")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "evidence", f"c5_global_search_{a.seed}.json"), "w") as f:
        json.dump(res, f, indent=1)
