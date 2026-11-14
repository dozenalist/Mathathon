"""
Exploratory search for N(rho): max number of centres with pairwise distance >= 2
inside a ball of radius rho about a centre.  Unit-sphere normalisation.

STATUS: exploratory.  A found configuration with N centres is a LOWER bound for N(rho).
An exhaustive/certified upper bound is NOT provided here; N(rho) is uncertified until a
separate upper-bound argument (spherical-cap / kissing-type / certified branch-and-bound)
is supplied.  The kissing value N(2) = 12 is the control.
"""
import numpy as np, json, argparse
from scipy.spatial.distance import cdist

def best_packing(rho, trials=60, seed=0, rounds=2000):
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(trials):
        # start from init random points, enforce separation 2 greedily
        P = []
        for _ in range(rounds):
            u = rng.normal(size=3); u /= np.linalg.norm(u)
            r = rho*rng.random()**(1/3)
            p = u*r
            if P:
                Pa = np.asarray(P)
                if np.min(np.einsum('ij,ij->i', Pa-p, Pa-p)) < 4.0: continue
            P.append(p)
            if len(P) >= (best if best else 10**9): break
        if P and (best is None or len(P) > best): best = len(P)
    return best

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rho-max", type=float, default=3.0)
    ap.add_argument("--step", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    out = {}
    r = 2.0
    while r <= a.rho_max + 1e-9:
        out[f"{r:.2f}"] = best_packing(r, seed=a.seed)
        r += a.step
    print(json.dumps({"status": "TESTED_FINITE_lower_bounds_only", "N_lower": out}, indent=2))
