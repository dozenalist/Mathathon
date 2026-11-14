"""Geometric audit of the sector-word dictionary (fast version).

(1) exact rational certificate for the deviation bound |arg s - (arg f +- pi/3)| <= B d
    with B < 1.666, hence dev < 0.556 Delta < Delta  (d0 = pi/(9m), Delta = pi/(3m));
(2) attainment of each of the six offsets +-(m-1), +-m, +-(m+1) by an explicit
    configuration with d <= d0  (so the word constraint is forced, not decorative);
(3) sweep: no other sector shift is realised (sanity check of the bound in (1));
(4) the hypotheses of (5.3): s,t nonparallel, s a local diffeo in the angular
    coordinate;
(5) the accumulating centre data y_k = (d0/3) 2^-k (3/5, 4/5).
"""
from fractions import Fraction as F
import numpy as np

print("=== (1) exact rational deviation certificate ===")
PI_LO = F(31415926535897932384626433832795, 10**31)
PI_HI = PI_LO + F(1, 10**30)
rows = []
for m in (3, 6, 9, 12, 15, 18, 24, 30, 60, 120):
    d_hi = PI_HI / (9 * m)                      # >= d0
    x = d_hi / (1 - d_hi)
    t1 = x * (1 + x**2 / 2 + F(3, 8) * x**4) * (1 + x**2)   # >= arcsin(d/(1-d))
    u = 1 + d_hi
    t2 = d_hi * (1 + u**2 / 8) / 2                          # >= d/sqrt(4-(1+d)^2)
    B = t1 + t2
    ratio = B / d_hi
    frac = ratio * F(1, 3)                      # dev/Delta, since d0/Delta = 1/3
    rows.append((m, float(ratio), float(frac), frac < 1))
    print(f"m={m:4d}: dev <= {float(ratio):.5f}*d ;  dev/Delta <= {float(frac):.5f} < 1 : {frac < 1}")
print("worst ratio:", max(r[1] for r in rows), " worst dev/Delta:", max(r[2] for r in rows))
print("=> sector(s) = sector(f) + m + k, k in {-1,0,+1}; no other shift possible.")
print("   record's 1.5938 gives dev/Delta =", 1.5938 / 3)

print()
print("=== (2)/(3)/(4) configuration sweep ===")


def sweep(m, nf=181, nd=25):
    Delta = 2 * np.pi / (6 * m)
    d0 = np.pi / (9 * m)
    argf = (np.arange(nf) + 0.5) * 2 * np.pi / nf
    arga = np.arange(nf) * 2 * np.pi / nf
    F1 = np.stack([np.cos(argf), np.sin(argf)], 1)
    A1 = np.stack([np.cos(arga), np.sin(arga)], 1)
    seen = set()
    worst = 0.0
    minst = 1e9
    for j in range(1, nd + 1):
        d = d0 * j / nd
        P = (F1[:, None, :] + d * A1[None, :, :]).reshape(-1, 2)
        f = np.repeat(F1, nf, 0)
        rho = np.linalg.norm(P, axis=1)
        ok = rho <= 2
        P, f, rho = P[ok], f[ok], rho[ok]
        h = np.sqrt(1 - rho**2 / 4)
        perp = np.stack([-P[:, 1], P[:, 0]], 1) / rho[:, None]
        for sgn in (1.0, -1.0):
            S = P / 2 + sgn * h[:, None] * perp
            T = P - S
            ang = np.arctan2(S[:, 1], S[:, 0])
            dev = np.mod(ang - (np.arctan2(f[:, 1], f[:, 0]) + np.pi / 3) + np.pi, 2 * np.pi) - np.pi
            worst = max(worst, float(np.abs(dev).max()))
            cross = S[:, 0] * T[:, 1] - S[:, 1] * T[:, 0]
            dot = (S * T).sum(1)
            minst = min(minst, float(np.abs(np.arctan2(cross, dot)).min()))
            i0 = np.floor(np.arctan2(f[:, 1], f[:, 0]) / Delta)
            i1 = np.floor(ang / Delta)
            for jj in np.unique((i1 - i0) % (6 * m)):
                seen.add(int(jj))
    exp = sorted({(m + k) % (6 * m) for k in (-1, 0, 1)} | {(-m + k) % (6 * m) for k in (-1, 0, 1)})
    print(f"m={m:3d}: realised shifts {sorted(seen)}")
    print(f"        required offsets {exp}  identical: {sorted(seen) == exp}")
    print(f"        worst |dev| = {worst:.6g} < 1.666*d0 = {1.666 * d0:.6g};"
          f" min angle(s,t) = {minst:.4f} rad > 0")
    t = np.linspace(-1.2, 1.2, 20001)
    for dd in (d0 / 2, d0):
        a = dd * np.array([np.cos(1.0), np.sin(1.0)])
        fx, fy = np.cos(t) + a[0], np.sin(t) + a[1]
        rr = np.hypot(fx, fy)
        hh = np.sqrt(1 - rr**2 / 4)
        arg = np.unwrap(np.arctan2(fy / 2 + hh * fx / rr, fx / 2 - hh * fy / rr))
        der = np.diff(arg) / np.diff(t)
        print(f"        d={('d0/2' if dd < d0 else 'd0')}: d arg s/d arg f in"
              f" [{der.min():.3f},{der.max():.3f}] (bounded away from 0)")
    return sorted(seen) == exp


for m in (3, 4, 5, 6, 9, 12):
    sweep(m)

print()
print("=== (2b) explicit attaining configurations (m=6, d=d0) ===")
m = 6
n = 6 * m
Delta = 2 * np.pi / n
d0 = np.pi / (9 * m)
targets = [(m + k) % n for k in (-1, 0, 1)] + [(-m + k) % n for k in (-1, 0, 1)]
found = {}
for i in range(720):
    argf = 2 * np.pi * (i + 0.5) / 720
    for k in range(1440):
        arga = 2 * np.pi * k / 1440
        a = d0 * np.array([np.cos(arga), np.sin(arga)])
        fx, fy = np.cos(argf) + a[0], np.sin(argf) + a[1]
        rho = np.hypot(fx, fy)
        h = np.sqrt(1 - rho**2 / 4)
        for sgn in (1, -1):
            sx, sy = fx / 2 + sgn * h * (-fy) / rho, fy / 2 + sgn * h * fx / rho
            j = (int(np.floor(np.arctan2(sy, sx) / Delta)) - int(np.floor(argf / Delta))) % n
            if j in targets and j not in found:
                found[j] = (round(argf, 6), round(arga, 6), float(d0))
for j in sorted(set(targets)):
    print(f"  offset {j:2d}: {found.get(j)}")
print("all six attained:", set(found) >= set(targets))

print()
print("=== (5) accumulating centres y_k = (d0/3) 2^-k (3/5,4/5) ===")
for m in (6, 9, 12):
    d0 = np.pi / (9 * m)
    u = np.array([3 / 5, 4 / 5])
    ys = np.array([d0 / 3 * 2.0**(-k) for k in range(60)])
    pts = ys[:, None] * u[None, :]
    steps = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    print(f"m={m}: |y_k| -> 0; all |y_k| <= d0/3 = {d0/3:.6g}; max step = {steps.max():.6g}"
          f" <= d0 : {steps.max() <= d0}; distinct: {len(np.unique(pts.round(20), axis=0)) == len(pts)}")
