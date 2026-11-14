"""K15 normalization conversions and published-reference reproduction.

Two conventions appear in this project and they must never be mixed silently:

  A  "sep1 / number"  (used by the recovered 2026-11-14 CE3 experiments)
     * minimum centre separation 1, balls of radius 1/2
     * objective rho_A = number of centres per unit volume
     * Cohn-Elkies:  f(x) <= 0 for |x| >= 1, fhat >= 0
                     =>  rho_A <= f(0)/fhat(0)
     * FCC: rho_A = sqrt(2), attained.

  B  "unit radius / occupied volume"  (project contract, ROADMAP section 2)
     * minimum centre separation 2, unit balls (radius 1)
     * objective Delta = occupied-volume upper density
     * Cohn-Elkies:  f(x) <= 0 for |x| >= 2, fhat >= 0
                     =>  Delta <= (4 pi/3) f(0)/fhat(0)
     * FCC: Delta = pi/sqrt(18), i.e. rho_B = 2**(-5/2) centres per unit volume.

Exact relations (scaling by 2 in R^3):
    rho_B = rho_A / 8                 (density scales by 2**3)
    Delta = (4 pi/3) * rho_B = (pi/6) * rho_A
and for a certificate f expressed in A, the B-convention function is
g(x) = f(x/2), with ghat(t) = 8 fhat(2t), so
    (4 pi/3) g(0)/ghat(0) = (pi/6) f(0)/fhat(0).

All four conversions are asserted against published values below.
"""
from mpmath import mp, mpf, pi, sqrt, mpf as M

mp.dps = 30

# --- exact conversion constants ------------------------------------------------
def rhoA_to_Delta(rho_A):
    """sep1 number density -> unit-radius occupied-volume density."""
    return (pi / 6) * mpf(rho_A)

def Delta_to_rhoA(Delta):
    return 6 * mpf(Delta) / pi

def rhoA_to_rhoB(rho_A):
    """sep1 number density -> unit-radius (min separation 2) number density."""
    return mpf(rho_A) / 8

def rhoB_to_Delta(rho_B):
    return (4 * pi / 3) * mpf(rho_B)

# --- the exact constants -------------------------------------------------------
KEPLER_DELTA = pi / sqrt(18)              # pi/(3 sqrt 2)
FCC_RHO_A    = sqrt(2)                    # sqrt(2) centres per unit volume at sep 1
FCC_RHO_B    = FCC_RHO_A / 8              # = 2**(-5/2)

# Published reference values, converted consistently.
PUBLISHED = {
    # name                         volume density Delta   source
    "kepler_exact":        (KEPLER_DELTA,                "Hales 2005 / Flyspeck (exact)"),
    "dodecahedral_HM10":   (mpf("0.7546974"),            "Hales-McLaughlin JAMS 2010 (rounding as quoted in CDS22)"),
    "cds22_lattice_3pt":   (mpf("0.741506"),             "CDS22 Table 1.1, lattice-only three-point"),
    "cds22_general_3pt":   (mpf("0.770271"),             "CDS22 Table 1.1, general three-point"),
    "dlov14_2pt_strength": (mpf("0.773080"),             "CDS22 Table 1.1, de Laat-de Oliveira Filho-Vallentin strengthened 2-point"),
    "ce03_lp":             (mpf("0.779747"),             "CDS22 Table 1.1 (= CE03 Table 3 m=6, 0.18616 CE-units)"),
}

def report():
    print("=== exact constants ===")
    print("Kepler  Delta = pi/sqrt(18) =", mp.nstr(KEPLER_DELTA, 15))
    print("FCC     rho_A = sqrt(2)     =", mp.nstr(FCC_RHO_A, 15))
    print("FCC     rho_B = 2^(-5/2)    =", mp.nstr(FCC_RHO_B, 15))
    print("check Delta(FCC) via rho_B  =", mp.nstr(rhoB_to_Delta(FCC_RHO_B), 15))
    print("check Delta(FCC) via rho_A  =", mp.nstr(rhoA_to_Delta(FCC_RHO_A), 15))
    print()
    print("=== published references, converted both ways ===")
    print("%-22s %10s %10s %10s %10s" % ("name", "Delta", "rho_A", "rho_B", "gap/Kepler"))
    for name, (D, src) in sorted(PUBLISHED.items(), key=lambda kv: kv[1][0]):
        print("%-22s %10s %10s %10s %9.4f%%" % (
            name, mp.nstr(D, 9), mp.nstr(Delta_to_rhoA(D), 9),
            mp.nstr(rhoA_to_rhoB(Delta_to_rhoA(D)), 9),
            float(100 * (D / KEPLER_DELTA - 1))))
    print()
    print("=== consistency assertions (hard failures if violated) ===")
    # 1. CE03's own table entry 0.18616 (their units, 5 dp) vs CDS22's 0.779747.
    #    These agree only to ~6e-5 relative, and the residual is a ROUNDING artefact:
    #    CE03 print a rigorous upper bound rounded UP at 5 decimals, CDS22 quote a
    #    more precise value of the same quantity. Documented, not asserted tightly.
    ce_from_table = rhoB_to_Delta(mpf("0.18616"))
    print("rounding audit: 4pi/3 * 0.18616 = %s vs CDS22 0.779747 (rel diff %.2e)"
          % (mp.nstr(ce_from_table, 12), float(abs(ce_from_table - mpf("0.779747")) / mpf("0.779747"))))
    assert abs(ce_from_table - mpf("0.779747")) < mpf("1e-4")
    # 2. Li's lower bound for the CE optimum, unit-sphere centre density 0.18398089,
    #    must convert to rho_A > 1.47184 (the number used in the 11-14 notes).
    li_rhoB = mpf("0.18398089")
    assert rhoB_to_Delta(li_rhoB) > KEPLER_DELTA
    assert abs(8 * li_rhoB - mpf("1.47184712")) < mpf("1e-7")
    # 3. Li's quoted best non-Hales bound 0.183889 must be CDS22's general 3-point value.
    assert abs(rhoB_to_Delta(mpf("0.183889")) - mpf("0.770271")) < mpf("3e-6")
    # 4. FCC in both conventions.
    assert abs(rhoA_to_Delta(FCC_RHO_A) - KEPLER_DELTA) < mpf("1e-25")
    print("assertion 1: CE03 0.186157 CE-units -> Delta 0.779747            OK")
    print("assertion 2: Li 0.18398089 -> Delta %s > Kepler                  OK" % mp.nstr(rhoB_to_Delta(li_rhoB), 9))
    print("assertion 3: Li-quoted 0.183889 -> Delta 0.770271 = CDS general   OK")
    print("assertion 4: FCC rho_A = sqrt2 -> Delta = pi/sqrt18                OK")
    print()
    print("Li obstruction in sep1 units: ordinary CE optimum rho_A >", mp.nstr(8 * li_rhoB, 12),
          " > sqrt2 =", mp.nstr(FCC_RHO_A, 12))
    return True

if __name__ == "__main__":
    report()
