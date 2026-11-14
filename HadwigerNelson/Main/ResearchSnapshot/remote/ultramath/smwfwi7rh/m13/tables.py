"""All numbers quoted in RESULTS.md, reproduced from geometry_fast + sector_csp."""
import mpmath as mp
import geometry_fast as G

mp.mp.dps = 25
PI = mp.pi


def dcrit(m):
    """Largest d with ceil(3 m Sig(d)/pi) <= floor(m/5), i.e. Sig(d) <= pi floor(m/5)/(3m)."""
    tgt = PI * (m // 5) / (3 * m)
    lo, hi = mp.mpf(0), mp.mpf(1)
    for _ in range(80):
        mid = (lo + hi) / 2
        if G.sigma(mid)[0] <= tgt:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    print("=== Sigma(d): the transport reach, and the forced band width ===")
    for d in (0.01, 0.05, 0.1, 0.15, 0.1756, 0.2, 0.3, 0.5, 0.7):
        s, psi, _ = G.sigma(d)
        print(f"  d={d:7.4f}  Sig={mp.nstr(s, 18):22s} 3Sig/pi={mp.nstr(3*s/PI, 15):18s} "
              f"psi*={psi:.6f}")
    print(f"  d=1:  Sig = {mp.nstr(G.sigma(1)[0], 20)}   (exactly 2*pi/3 = "
          f"{mp.nstr(2*PI/3, 20)})")
    print()
    print("=== d* : the sharp transport radius of the free-label sector class ===")
    tgt = PI / 15
    lo, hi = mp.mpf(0), mp.mpf(1)
    for _ in range(100):
        mid = (lo + hi) / 2
        if G.sigma(mid)[0] <= tgt:
            lo = mid
        else:
            hi = mid
    dstar = (lo + hi) / 2
    print("  d* = Sig^{-1}(pi/15) =", mp.nstr(dstar, 22))
    print("  check Sig(d*) - pi/15 =", mp.nstr(G.sigma(dstar)[0] - tgt, 5))
    print("  Sig'(d*) (slope) ~", mp.nstr((G.sigma(dstar + mp.mpf('1e-6'))[0]
                                          - G.sigma(dstar - mp.mpf('1e-6'))[0]) / mp.mpf('2e-6'), 10))
    print()
    print("=== d_crit(m) = Sig^{-1}(pi floor(m/5)/(3m)) : exact threshold per resolution ===")
    for m in list(range(1, 16)) + [20, 25, 30, 40, 50, 60, 100, 200, 1000]:
        print(f"  m={m:5d}  K_max={m//5:4d}  d_crit={mp.nstr(dcrit(m), 12)}")
    print()
    print("=== forced band K(d,m) = ceil(3m Sig(d)/pi) versus the budget floor(m/5) ===")
    print("     d       " + "".join(f"  m={m:<3d}" for m in (6, 12, 30, 60, 300)))
    for d in (0.05, 0.10, 0.15, 0.17557, 0.20, 0.5, 1.0):
        row = ""
        for m in (6, 12, 30, 60, 300):
            k = int(mp.ceil(3 * m * G.sigma(d)[0] / PI))
            row += f"  {k:3d}/{m//5:<3d}"
        print(f"  {d:7.5f}  " + row + "   (K/budget)")
