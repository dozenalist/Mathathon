#!/usr/bin/env python3
"""Adversarial tests for exact_volume.py.  Every expectation is a hand value, not a re-run.

The point of each case is to break a specific shortcut that a naive exact-volume implementation
takes -- and, in particular, the three the reviewer named: a float determinant filter, a
completeness check that only looks at the vertices already found, and duplicate planes.

Run: python3 tests_exact_volume.py       (exit 0 iff every case passes)
"""
import sys
from fractions import Fraction as F
import exact_volume as EV

FAILS = []
N = [0]
def check(name, cond, info=None):
    N[0] += 1
    if not cond:
        FAILS.append(name)
    print("  %s %s%s" % ("PASS" if cond else "FAIL", name, "" if info is None else "  %r" % (info,)))

def box(a, b, c, interior=(0, 0, 0)):
    """The box [-a,a] x [-b,b] x [-c,c] as six half-spaces, with an explicit interior point."""
    a, b, c = F(a), F(b), F(c)
    return [((1, 0, 0), a), ((-1, 0, 0), a), ((0, 1, 0), b), ((0, -1, 0), b),
            ((0, 0, 1), c), ((0, 0, -1), c)], (F(interior[0]), F(interior[1]), F(interior[2]))

def planes_of(spec):
    return [(n[0], n[1], n[2], d) for (n, d) in spec]

def main():
    print("=" * 96)
    print("A. KNOWN VOLUMES, EXACT")
    print("=" * 96)
    spec, v = box(1, 1, 1)
    check("unit cube: volume 8", EV.volume(planes_of(spec), v) == 8, EV.volume(planes_of(spec), v))
    spec, v = box(1, 2, 3)
    check("box 2x4x6: volume 48", EV.volume(planes_of(spec), v) == 48, EV.volume(planes_of(spec), v))
    # the regular octahedron |x|+|y|+|z| <= 1 has volume 4/3
    octa = [((1, 1, 1), 1), ((1, 1, -1), 1), ((1, -1, 1), 1), ((1, -1, -1), 1),
            ((-1, 1, 1), 1), ((-1, 1, -1), 1), ((-1, -1, 1), 1), ((-1, -1, -1), 1)]
    check("octahedron |x|+|y|+|z| <= 1: volume 4/3",
          EV.volume(planes_of(octa), (F(0), F(0), F(0))) == F(4, 3),
          EV.volume(planes_of(octa), (F(0), F(0), F(0))))

    print("\n" + "=" * 96)
    print("B. DUPLICATE AND REDUNDANT CONSTRAINTS  (E's duplicate-face defect: 28/3 instead of 8)")
    print("=" * 96)
    spec, v = box(1, 1, 1)
    P = planes_of(spec)
    # (1) an identical duplicate
    try:
        vol, cert = EV.certify_volume(P + [P[0]], v)
        check("identical duplicate cube: volume still 8", vol == 8, vol)
        check("... and it is reported as dropped",
              any("duplicate" in why for _, why in cert["dropped"]), cert["dropped"])
    except ValueError as e:
        check("identical duplicate cube: volume still 8", False, str(e))
    # (2) a SCALED duplicate -- the same half-space written as (2,0,0,2)
    try:
        vol2, cert2 = EV.certify_volume(P + [(2, 0, 0, 2)], v)
        check("scaled duplicate (2,0,0,2) of (1,0,0,1): volume still 8", vol2 == 8, vol2)
        check("... reported as a duplicate, not a second face",
              any("duplicate" in why for _, why in cert2["dropped"]), cert2["dropped"])
    except ValueError as e:
        check("scaled duplicate (2,0,0,2): volume still 8", False, str(e))
    # (3) the naive failure mode, for the record: counting the duplicate face twice
    print("     (a naive fan over all six+1 planes would give 8 + 4/3 = 28/3 = %.4f)" % (28 / 3))
    # (4) a redundant plane far outside
    try:
        vol3, _ = EV.certify_volume(P + [(0, 0, 1, 100)], v)
        check("a far redundant plane changes nothing", vol3 == 8, vol3)
    except ValueError as e:
        check("a far redundant plane changes nothing", False, str(e))
    # (5) a nearly-coincident plane: offset 1 + 1/10^12
    try:
        vol4, cert4 = EV.certify_volume(P + [(0, 0, 1, F(10 ** 12 + 1, 10 ** 12))], v)
        check("a plane 1e-12 outside a face is redundant: volume 8", vol4 == 8, vol4)
        check("... and it is dropped as dominated",
              any("dominated" in why for _, why in cert4["dropped"]), cert4["dropped"])
    except ValueError as e:
        check("a plane 1e-12 outside a face is redundant: volume 8", False, str(e))

    print("\n" + "=" * 96)
    print("C. WHAT A FLOAT DETERMINANT FILTER GETS WRONG")
    print("=" * 96)
    # A box with one face tilted by a rational of size 1e-9: the triple at each of the four
    # vertices of that face has a determinant of order 1e-9, exactly the size the old filter dropped.
    eps = F(1, 10 ** 9)
    tilted = [(1, 0, 0, 1), (-1, 0, 0, 1), (0, 1, 0, 1), (0, -1, 0, 1),
              (0, 0, 1, 1), (eps, 0, -1, 1)]          # bottom face tilted by eps
    try:
        vol, cert = EV.certify_volume(tilted, (F(0), F(0), F(0)))
        # the exact volume: the bottom face is z = 1 + eps*x, so the height at x=+-1 is 1 -+ eps,
        # and the volume is the mean height times the base area: 2 * 2 * 2 * 1 = 8
        check("tilted-box volume is 8 (mean height 1)", vol == 8, vol)
        check("... with all 8 vertices found", len(cert["vertices"]) == 8, len(cert["vertices"]))
    except ValueError as e:
        check("tilted box with a 1e-9 angle", False, str(e))

    check("solve3 divides exactly (no float leak)",
          EV.solve3([(1, 0, 0, 1), (0, 1, 0, 1), (1, 0, -10 ** 9, 10 ** 9)])
          == (F(1), F(1), F(-999999999, 1000000000)),
          EV.solve3([(1, 0, 0, 1), (0, 1, 0, 1), (1, 0, -10 ** 9, 10 ** 9)]))
    check("... and the result is a Fraction, not a float",
          isinstance(EV.solve3([(1, 0, 0, 1), (0, 1, 0, 1), (1, 0, -10 ** 9, 10 ** 9)])[2], F))

    print("\n" + "=" * 96)
    print("D. DEGENERACIES ARE REJECTED, NOT APPROXIMATED")
    print("=" * 96)
    # (1) unbounded: three planes meeting in a corner
    try:
        EV.certify_volume([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)], (F(0), F(0), F(0)))
        check("three planes (unbounded) are rejected", False, "accepted")
    except ValueError as e:
        check("three planes (unbounded) are rejected", True, str(e)[:60])
    # (2) a slab of zero thickness
    try:
        EV.certify_volume([(1, 0, 0, 1), (-1, 0, 0, 1), (0, 1, 0, 1), (0, -1, 0, 1),
                           (0, 0, 1, 0), (0, 0, -1, 0)], (F(0), F(0), F(0)))
        check("a flat slab is rejected", False, "accepted")
    except ValueError as e:
        check("a flat slab is rejected", True, str(e)[:80])
    # (3) a zero normal
    try:
        EV.normalise((0, 0, 0, 1))
        check("a zero normal is rejected", False, "accepted")
    except ValueError:
        check("a zero normal is rejected", True)
    # (4) three planes sharing a line: exact determinant zero, no spurious vertex
    check("three planes through a common line give no vertex",
          EV.solve3([(1, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 2)]) is None)

    print("\n" + "=" * 96)
    print("E. A NON-SIMPLE POLYTOPE: vertices where FOUR planes meet")
    print("=" * 96)
    # the rhombic dodecahedron {|x|<=1, |y|<=1, |z|<=1, |x|+|y|+|z|<=2}: 12 faces,
    # 8 vertices of degree 3 and 6 of degree 4, volume 8 + 6*(1/6)*... computed below by hand:
    # cube of volume 8 with the 8 corners cut by the planes +-x+-y+-z = 2, each corner cut is a
    # pyramid of base area 3/2 and height (sqrt3/2 ... ) -- instead take the exact known value:
    rd = [(1, 0, 0, 1), (-1, 0, 0, 1), (0, 1, 0, 1), (0, -1, 0, 1), (0, 0, 1, 1), (0, 0, -1, 1),
          (1, 1, 1, 2), (1, 1, -1, 2), (1, -1, 1, 2), (1, -1, -1, 2),
          (-1, 1, 1, 2), (-1, 1, -1, 2), (-1, -1, 1, 2), (-1, -1, -1, 2)]
    vol, cert = EV.certify_volume(rd, (F(0), F(0), F(0)))
    # the cube is 8; each of the 8 corners is cut by a plane through the three adjacent edge
    # midpoints, removing a tetrahedron of volume (1/2)^3/6 = 1/48 each: 8 - 8/48 = 8 - 1/6
    # each corner (1,1,1) is cut by x+y+z = 2 through the edge midpoints (1,1,0),(1,0,1),(0,1,1):
    # the removed tetrahedron is |det[(0,0,-1),(0,-1,0),(-1,0,0)]|/6 = 1/6, eight corners: 8/6 = 4/3
    check("truncated cube: volume 8 - 8*(1/6) = 20/3", vol == F(20, 3), vol)
    # degree-4 vertices belong to the octahedron: (+-1,0,0) lies on four of its eight planes
    oct_planes = planes_of(octa)
    check("the octahedron has vertices where four planes meet",
          sum(1 for pl in oct_planes if pl[0]*1 + pl[1]*0 + pl[2]*0 == pl[3]) == 4,
          sum(1 for pl in oct_planes if pl[0]*1 + pl[1]*0 + pl[2]*0 == pl[3]))

    print("\n" + "=" * 96)
    print("F. THE CERTIFICATE IS CHECKED INDEPENDENTLY")
    print("=" * 96)
    spec, v = box(1, 1, 1)
    vol, cert = EV.certify_volume(planes_of(spec), v)
    # tampering must be caught
    import copy
    for name, mutate in (
            ("volume", lambda c: c.__setitem__("volume", "9")),
            ("a vertex moved", lambda c: c["vertices"].__setitem__(0, ["2", "0", "0"])),
            ("a facet dropped", lambda c: c["facets"].pop()),
            ("a facet reversed", lambda c: c["facets"][0]["verts"].reverse()),
            ("the interior point moved out", lambda c: c.__setitem__("interior", ["2", "0", "0"]))):
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            EV.check_certificate(bad)
            check("tampering with %s is caught" % name, False, "accepted")
        except (ValueError, KeyError, IndexError):
            check("tampering with %s is caught" % name, True)

    print("\n" + "=" * 96)
    print("G. THE TWO-PART ARGUMENT, AND NORMALISATION")
    print("=" * 96)
    spec, v = box(1, 1, 1)
    P = planes_of(spec)
    # (1) part (ii) of the argument: candidates = the six cube faces (bounded), and one more plane
    #     that CUTS the cube.  The candidate polytope certifies fine, so only the check of the
    #     remaining plane can catch the omission.
    cutting = (1, 1, 1, 2)                     # x+y+z <= 2, cuts the corner (1,1,1)
    try:
        EV.certify_volume(P + [cutting], v, candidates=P)
        check("a plane outside the candidate set that CUTS is caught", False, "accepted")
    except ValueError as e:
        check("a plane outside the candidate set that CUTS is caught",
              "cuts the polytope" in str(e), str(e)[:70])
    # ... and the same plane IS a facet when it is in the candidate set: the truncated cube
    vol_t, _ = EV.certify_volume(P + [cutting], v, candidates=P + [cutting])
    check("with the cutting plane as a candidate the volume is 8 - 1/6 = 47/6",
          vol_t == F(47, 6), vol_t)
    # (1b) an omission that leaves the candidate polytope unbounded is caught by V5 instead
    try:
        EV.certify_volume(P, v, candidates=[pl for pl in P if pl != (0, 0, 1, 1)])
        check("an unbounded candidate set is caught (V5)", False, "accepted")
    except ValueError as e:
        check("an unbounded candidate set is caught (V5)", "V5" in str(e), str(e)[:60])
    # (2) a candidate set containing all facets gives the right volume
    vol, cert = EV.certify_volume(P, v, candidates=P)
    check("the full candidate set gives volume 8", vol == 8, vol)
    # (3) opposite half-spaces are NOT duplicates: (1,0,0,1) is x<=1, (-1,0,0,-1) is x>=1
    check("(1,0,0,1) and (-1,0,0,-1) normalise differently",
          EV.normalise((1, 0, 0, 1)) != EV.normalise((-1, 0, 0, -1)),
          (EV.normalise((1, 0, 0, 1)), EV.normalise((-1, 0, 0, -1))))
    # (4) a positively scaled copy IS the same half-space
    check("(1,0,0,1) and (3,0,0,3) normalise the same",
          EV.normalise((1, 0, 0, 1)) == EV.normalise((3, 0, 0, 3)))
    # (5) the x>=1 half-space, added to the unit cube, leaves nothing: rejected
    try:
        EV.certify_volume(P + [(-1, 0, 0, -1)], v)
        check("cube + (x >= 1) is rejected (empty)", False, "accepted")
    except ValueError:
        check("cube + (x >= 1) is rejected (empty)", True)

    print("\n" + "=" * 96)
    print("H. THE REVIEWER'S TWO FALSE ACCEPTS (Astra, at fbb124e)")
    print("=" * 96)
    import copy as _copy
    spec, v = box(1, 1, 1)
    P = planes_of(spec)
    vol8, cert8 = EV.certify_volume(P, v)
    check("the cube certifies at volume 8", vol8 == 8, vol8)
    # (1) duplicate the complete facet list and claim 16: closure still holds (0 = 2*0)
    bad = _copy.deepcopy(cert8)
    bad["facets"] = bad["facets"] + _copy.deepcopy(bad["facets"])
    bad["volume"] = "16"
    try:
        EV.check_certificate(bad)
        check("duplicated facets with volume 16 is REJECTED", False, "accepted")
    except ValueError as e:
        check("duplicated facets with volume 16 is REJECTED", True, str(e)[:50])
    # (2) a constraint added to cert["planes"] only: the true volume is 6, not 8
    bad2 = _copy.deepcopy(cert8)
    bad2["planes"].append(["1", "0", "0", "1/2"])
    try:
        EV.check_certificate(bad2)
        check("an added constraint (volume would be 6) is REJECTED", False, "accepted")
    except ValueError as e:
        check("an added constraint (volume would be 6) is REJECTED", True, str(e)[:50])
    # (2b) the mirror image: a CANDIDATE plane that is not a constraint
    bad3 = _copy.deepcopy(cert8)
    bad3["candidate_planes"] = [list(pl) for pl in bad3["candidate_planes"]] + [[1, 0, 0, 0]]
    try:
        EV.check_certificate(bad3)
        check("a candidate plane outside the constraints is REJECTED", False, "accepted")
    except ValueError as e:
        check("a candidate plane outside the constraints is REJECTED", True, str(e)[:50])

    # (2c) the STANDALONE verifier must reject both witnesses too, independently of the producer
    import json as _json, os as _os
    import verify_certificate_independent as VI
    for name, mutate in (("duplicated facets", lambda c: (c.__setitem__("facets", c["facets"] + _copy.deepcopy(c["facets"])), c.__setitem__("volume", "16"), c)[-1]),
                         ("added constraint", lambda c: (c["planes"].append(["1", "0", "0", "1/2"]), c)[-1])):
        bad_c = _copy.deepcopy(cert8)
        bad_c = mutate(bad_c)
        _tmp = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".tmp_cert.json")
        _json.dump({"certificate": bad_c}, open(_tmp, "w"))
        try:
            VI.verify(_tmp)
            check("the standalone verifier rejects the %s witness" % name, False, "accepted")
        except SystemExit:
            check("the standalone verifier rejects the %s witness" % name, True)
        finally:
            _os.remove(_tmp)

    # (3) closure alone is not boundedness: the four side faces of a prism close, rank 2
    check("the four side-face normals span only 2 dimensions",
          EV._rank3([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]) is False)
    check("the cube's six normals span 3",
          EV._rank3([pl[:3] for pl in P]) is True)

    print()
    if FAILS:
        print("FAILED: %d -> %s" % (len(FAILS), FAILS))
        return 1
    print("ALL %d EXACT-VOLUME TESTS PASS" % N[0])
    return 0

if __name__ == "__main__":
    sys.exit(main())
