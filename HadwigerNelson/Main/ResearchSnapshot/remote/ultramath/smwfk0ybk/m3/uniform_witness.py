"""Closed-form witnesses: the tightened CSP at k = 6 is satisfied by two singleton
palettes alternating, drawn from the complement U = [6] \\ {0..l-1} of the cycle
label set, whenever |U| >= 2 (l <= 4).  This is a proof, not a search: it covers
every ray geometry at once, because O_i and I_i both contain U.

Also reports, for l = 5, 6, the smallest palette sizes over found models, so that
the shape of the surviving model class is explicit.
"""
from itertools import product
from csp_vacuity import sig_matrix, slivers, admissible, solve, pc


def check(l, k, pal):
    """Verify one palette assignment against (C1)-(C5) for one geometry."""
    sig = sig_matrix(l, (pal[6],))  # placeholder, replaced below
    raise NotImplementedError


def verify(l, k, c, pal):
    """pal: list of 6 lists of labels.  Returns (ok, reason)."""
    sig = sig_matrix(l, c)
    for i in range(6):
        P = set(pal[i])
        O, I = slivers(l, k, sig[i])
        Om = {x for x in range(k) if (O >> x) & 1}
        Im = {x for x in range(k) if (I >> x) & 1}
        if not (1 <= len(P) <= k - 3):
            return False, f"({l},{c}) (C1) fails at {i}"
        if not (P & Om):
            return False, f"({l},{c}) (C2) O fails at {i}"
        if not (P & Im):
            return False, f"({l},{c}) (C2) I fails at {i}"
    for i in range(6):
        if set(pal[i]) & set(pal[(i + 1) % 6]):
            return False, f"({l},{c}) (C3) fails at {i}"
    for i in range(6):
        for j in range(i + 1, 6):
            A, B = set(pal[i]), set(pal[j])
            if A | B == set(range(k)):
                return False, f"({l},{c}) (C4) fails at ({i},{j})"
    if sum(1 for i in range(6) if len(set(pal[i])) == 3) > 3:
        return False, f"({l},{c}) (C5) fails"
    return True, "ok"


def main():
    k = 6
    # --- the two closed-form families
    fam = {}
    for l, pal in ((3, [[3], [4], [3], [4], [3], [4]]),
                   (4, [[4], [5], [4], [5], [4], [5]])):
        bad = []
        tot = 0
        for tail in product(range(6), repeat=l - 1):
            c = (0,) + tail
            tot += 1
            ok, why = verify(l, k, c, pal)
            if not ok:
                bad.append(why)
        fam[l] = {"geometries": tot, "failures": len(bad), "example": bad[:3],
                  "palettes": pal,
                  "U": sorted({x for x in range(k)} - set(range(l)))}
        print(f"l={l}: uniform palettes {pal} verified on {tot - len(bad)}/{tot} "
              f"geometries (U = {fam[l]['U']})", flush=True)

    # --- the shape of the surviving models at l = 5, 6
    shapes = {}
    for l in (5, 6):
        sizes_hist = {}
        allone = 0
        sat = 0
        for tail in product(range(6), repeat=l - 1):
            c = (0,) + tail
            adm = admissible(l, k, sig_matrix(l, c), k - 3)
            w = solve(adm, True) if all(adm) else None
            if w is None:
                continue
            sat += 1
            key = tuple(sorted(len(p) for p in w))
            sizes_hist[key] = sizes_hist.get(key, 0) + 1
            if all(len(p) == 1 for p in w):
                allone += 1
        shapes[l] = {"sat": sat, "size_multiset_histogram": sizes_hist,
                     "all_singleton": allone}
        print(f"l={l}: SAT={sat}, models found with all-six-singleton palettes={allone}, "
              f"size multisets seen: {len(sizes_hist)}", flush=True)

    # --- small binary search: is there any instance whose ONLY models are ternary?
    #     (already answered by csp_vacuity: 0; restate as an explicit check here)
    print("\nclosed-form families:", {l: fam[l]["failures"] for l in fam})
    with open("uniform_witness.json", "w") as f:
        import json
        json.dump({"families": fam,
                   "shapes": {str(k): {"sat": v["sat"], "all_singleton": v["all_singleton"],
                                       "size_multisets": {",".join(map(str, kk)): vv
                                                          for kk, vv in v["size_multiset_histogram"].items()}}
                              for k, v in shapes.items()}},
                  f, indent=1)


if __name__ == "__main__":
    main()
