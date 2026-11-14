"""Exact verification of Lemma 8.9 / Table 1 of the paper (the seven-point Moser certificate).

All arithmetic is exact over  Q(sqrt 3, sqrt 11, sqrt 33) = Q(sqrt3, sqrt11).
Two readings of the printed (8.6) are tested; only one reproduces Table 1.

Run:  python3 certify_8_9.py
"""
import sympy as sp

s3, s11 = sp.sqrt(3), sp.sqrt(11)
I = sp.I

A = (s3 + I) / 2
B = (s3 - I) / 2
T = s3
u = (5 + I * s11) / 6
G = [("0", sp.Integer(0)), ("A", A), ("B", B), ("T", T),
     ("uA", u * A), ("uB", u * B), ("uT", u * T)]

ROT = (sp.Integer(35) + 12 * I) / sp.Integer(37)
TR = (sp.Integer(-290) + 149 * I) / sp.Integer(250)

TABLE1 = {"0": (-1.2906, 0.1876, 0.90, 1.35),
          "A": (-0.6335, 0.9414, 0.095, 0.110),
          "B": (-0.3092, -0.0045, 0.000002, 0.00065),
          "T": (0.3478, 0.7493, 0.023, 0.026),
          "uA": (-1.1598, 1.1790, 9.8, 19.0),
          "uB": (-0.3666, 0.5700, 0.0022, 0.024),
          "uT": (-0.2358, 1.5614, 12.65, 12.9)}


def place(g, reading):
    if reading == "composed":       # rotation, then translation: rot*(g + tr)
        return sp.expand(ROT * (g + TR))
    elif reading == "affine":       # rot*g + tr
        return sp.expand(ROT * g + TR)
    raise ValueError(reading)


def polys(z):
    xi, up = sp.expand(sp.re(z)), sp.expand(sp.im(z))
    l = sp.expand(xi ** 2 + up ** 2)
    P = sp.expand(up ** 2 * (3 * xi ** 2 - up ** 2) ** 2)      # (8.4) left
    Pp = sp.expand(l ** 3 * (1 - l / 4) * (l - 1) ** 2)        # (8.4) right
    return xi, up, l, P, Pp


def main():
    print("unit multiplier check:  |35+12i|^2 =", sp.expand(sp.Abs(ROT) ** 2), "= 37^2/37^2")
    print()
    print("Moser spindle coordinates (8.5): unit edges of G")
    edges = [("0", "A"), ("0", "B"), ("A", "B"), ("T", "A"), ("T", "B"),
             ("uA", "uB"), ("uA", "uT"), ("uB", "uT"), ("0", "uA"), ("0", "uB")]
    d = dict(G)
    bad = [e for e in edges if sp.simplify(sp.Abs(d[e[0]] - d[e[1]]) ** 2 - 1) != 0]
    print("   all ten edges of G have |difference|^2 = 1:", not bad, bad)
    print("   the contradicted edge T--uT:",
          sp.simplify(sp.Abs(T - u * T) ** 2), "= 1")
    print()

    for reading in ("composed", "affine"):
        print(f"=== reading '{reading}':",
              "z_g = ROT*(g + TR)" if reading == "composed" else "z_g = ROT*g + TR")
        ok_all = True
        print(f"{'g':3s} {'xi':>11s} {'ups':>11s} {'|z|^2':>10s} {'P':>12s} "
              f"{'Ppin':>12s} {'0<l<4':>6s} {'P<Ppin':>7s}  table1 coords match")
        for name, g in G:
            z = place(g, reading)
            xi, up, l, P, Pp = polys(z)
            okr = bool(sp.simplify(l) > 0 and sp.simplify(4 - l) > 0)
            oki = bool(sp.simplify(Pp - P) > 0)
            ok_all &= okr and oki
            tx, ty = TABLE1[name][0], TABLE1[name][1]
            match = abs(float(xi) - tx) < 0.00011 and abs(float(up) - ty) < 0.00011
            print(f"{name:3s} {float(xi):11.5f} {float(up):11.5f} {float(l):10.5f} "
                  f"{float(P):12.6g} {float(Pp):12.6g} {str(okr):>6s} {str(oki):>7s}  {match}")
        print(f"    -> Lemma 8.9 holds on this reading: {ok_all}")
        print()

    print("=== Table 1's own bounds P < P+ and P-' < P', recomputed exactly")
    print(f"{'g':3s} {'P':>12s} {'P+ (paper)':>11s} {'P<P+':>6s} "
          f"{'Ppin':>12s} {"P-' (paper)":>12s} {'P-`<Ppin':>9s}")
    for name, g in G:
        z = place(g, "composed")
        xi, up, l, P, Pp = polys(z)
        _, _, Pplus, Pminus = TABLE1[name]
        a = bool(sp.simplify(sp.Rational(str(Pplus)) * 10 ** 8 -
                             sp.nsimplify(P * 10 ** 8)) > 0)
        b = bool(sp.simplify(sp.nsimplify(Pp * 10 ** 8) -
                             sp.Rational(str(Pminus)) * 10 ** 8) > 0)
        print(f"{name:3s} {float(P):12.6g} {Pplus:11.6g} {str(a):>6s} "
              f"{float(Pp):12.6g} {Pminus:12.6g} {str(b):>9s}")


if __name__ == "__main__":
    main()
