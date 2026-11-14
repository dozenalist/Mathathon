"""
Independent NUMERICAL sanity check (not part of the proof) of the colouring
formula  c(x) = a + 2b mod 7  where a + b*omega is a nearest point of the
triangular lattice d*(Z + Z omega), omega = -1/2 + i sqrt3/2.
"""
import numpy as np, math, random
S3 = math.sqrt(3); W = complex(-0.5, S3/2)

def nearest(y):                      # y in lattice units (complex)
    best=None; bestd=None
    a0 = round(y.real + y.imag/S3)   # solve y = a + b W  => b = 2 Im y / sqrt3
    b0 = round(2*y.imag/S3)
    for a in range(a0-2, a0+3):
        for b in range(b0-2, b0+3):
            z = a + b*W
            d = abs(z-y)
            if bestd is None or d < bestd-1e-15:
                bestd = d; best = (a,b)
    return best, bestd

def colour(x, d):
    (a,b), _ = nearest(complex(x[0],x[1])/d)
    return (a + 2*b) % 7

random.seed(12345)
for d in [2*S3/5, 0.7, 0.8, math.sqrt(3/7)]:
    bad = 0; N = 40000
    for _ in range(N):
        x = (random.uniform(-30,30), random.uniform(-30,30))
        th = random.uniform(0, 2*math.pi)
        y = (x[0]+math.cos(th), x[1]+math.sin(th))
        if colour(x,d) == colour(y,d): bad += 1
    print(f"  d = {d:.6f} : monochromatic unit pairs found in {N} random trials: {bad}")

print("\n  threshold test: d^2 vs 3/7 =", 3/7)
for d in [0.64, 0.652, 0.654, 0.655, 0.66, 0.68]:
    bad = 0; N = 200000
    random.seed(7)
    for _ in range(N):
        x = (random.uniform(-12,12), random.uniform(-12,12))
        th = random.uniform(0, 2*math.pi)
        y = (x[0]+math.cos(th), x[1]+math.sin(th))
        if colour(x,d) == colour(y,d): bad += 1
    print(f"  d = {d:.4f} (d^2 = {d*d:.5f}) : {bad} monochromatic unit pairs in {N} trials")

print("\n  (explicit constructive pairs are given in theorem.md section 4;")
print("   here we only check the colouring formula numerically.)")
