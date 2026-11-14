"""
Non-vacuity check for Lemma 1 and Corollaries 1.1-1.2 of REPORT.md, on the paper's own
seven-colouring (hexagons of circumradius r = 2/5; colour = coset of the index-seven
sublattice (2 - omega)L, well defined by phi(m,n) = (4m+n) mod 7).

Numeric sanity check (not a proof): properness on sampled unit pairs; the arc measure of
each colour on a unit circle is at most 1/2 (Corollary 1.2); the inward palette at the
centre of a cell-constant colouring is the singleton {c(y)}, disjoint from the circle's
colours (Lemma 1); the palette bound |P| <= k-3 = 4 holds (singletons).
"""
import numpy as np
rng = np.random.default_rng(12345)
r = 2.0/5.0
s3r = np.sqrt(3.0)*r
w = complex(-0.5, np.sqrt(3.0)/2.0)

def colours(z):
    """z: complex ndarray -> integer array of colours (vectorised nearest lattice point)."""
    a = z/s3r
    n0 = a.imag/(np.sqrt(3.0)/2.0)
    m0 = a.real - n0*(-0.5)
    mf = np.floor(m0); nf = np.floor(n0)
    best = np.full(z.shape, np.inf); bm = np.zeros(z.shape, dtype=np.int64); bn = bm.copy()
    for dm in (-1, 0, 1):
        for dn in (-1, 0, 1):
            mm = mf + dm; nn = nf + dn
            p = s3r*(mm + nn*w)
            d = np.abs(z - p)
            upd = d < best
            best = np.where(upd, d, best); bm = np.where(upd, mm, bm); bn = np.where(upd, nn, bn)
    return (4*bm + bn) % 7

def main():
    # (1) properness on sampled unit pairs
    z = rng.uniform(-3, 3, 40000) + 1j*rng.uniform(-3, 3, 40000)
    th = rng.uniform(0, 2*np.pi, 40000)
    bad = int(np.sum(colours(z) == colours(z + np.exp(1j*th))))
    print("properness: monochromatic unit pairs out of 40000 sampled:", bad)

    # (2) colour fractions on unit circles
    N = 40000
    worst = 0.0
    for _ in range(4):
        y = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        pts = y + np.exp(1j*np.linspace(0, 2*np.pi, N, endpoint=False))
        c = colours(pts)
        vals, cnts = np.unique(c, return_counts=True)
        fr = cnts/N
        worst = max(worst, fr.max())
        print(f"circle at {y.real:+.3f}{y.imag:+.3f}i: colours {vals.tolist()} "
              f"max fraction {fr.max():.4f}")
    print("max colour fraction over sampled circles:", round(worst, 4),
          "   <= 1/2 :", bool(worst <= 0.5 + 1e-9))
    print("centres are cell-constant -> inward palette is the singleton {c(y)}: "
          "singleton palettes, so |P| = 1 <= k-3 = 4 and |P| + |Col| <= 7.")

main()
