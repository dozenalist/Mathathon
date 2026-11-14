#!/usr/bin/env python3
"""Independent Python cross-check of the ENCODING used in ShiftT.lean.

The Lean file defines
    shiftT  lam = (subStair lam).map (fun x => x + lam.length)
    shiftInv b  = (addStair b).map  (fun x => x - b.length)
with Nat (truncating) subtraction.  The mathematics wants
    T(lam)_i = lam_i - k + 2i - 1     (1-based i, k = length)
    T^-1(b)_i = b_i + k - 2i + 1
in the integers.  This script checks, for every D_n with n <= 20, that the
truncating Nat encoding agrees with the integer formula, that T lands in
B_n = {descending, smallest part >= length}, that the weight is preserved,
and that T is a bijection D_n -> B_n with the stated inverse.

stdlib only, exact integers, no network.
"""
import sys

NMAX = 20


def D(n):
    """Descending lists of positive ints, weight n, adjacent gaps >= 2."""
    out = set()

    def rec(rem, prev_max, acc):
        for p in range(prev_max, 0, -1):
            if rem - p < 0:
                continue
            if rem - p == 0:
                out.add(tuple(acc + [p]))
            elif p - 2 >= 1:
                rec(rem - p, p - 2, acc + [p])

    if n == 0:
        out.add(())
    else:
        rec(n, n, [])
    return sorted(out)


def B(n):
    """Independent enumeration of {descending b, sum n, every entry >= length}."""
    out = set()
    for m in range(0, n + 1):
        if m == 0:
            if n == 0:
                out.add(())
            continue

        def recB(rem, last, acc):
            if len(acc) == m:
                if rem == 0:
                    out.add(tuple(acc))
                return
            for p in range(min(last, rem), m - 1, -1):
                recB(rem - p, p, acc + [p])

        recB(n, n, [])
    return out


def is_D(lam):
    if any(x <= 0 for x in lam):
        return False
    return all(lam[i] >= lam[i + 1] + 2 for i in range(len(lam) - 1))


def is_B(b):
    if any(b[i] < b[i + 1] for i in range(len(b) - 1)):
        return False
    k = len(b)
    return all(x >= k for x in b)


def subStair_nat(lam):
    k = len(lam)
    return tuple(max(0, lam[i] - (2 * (k - i - 1) + 1)) for i in range(k))


def addStair_nat(b):
    k = len(b)
    return tuple(b[i] + (2 * (k - i - 1) + 1) for i in range(k))


def shiftT_lean(lam):
    return tuple(x + len(lam) for x in subStair_nat(lam))


def shiftInv_lean(b):
    return tuple(max(0, x - len(b)) for x in addStair_nat(b))


def T_int(lam):
    k = len(lam)
    return tuple(lam[i] - k + 2 * (i + 1) - 1 for i in range(k))


fails = 0


def check(name, ok, detail=""):
    global fails
    print(("PASS  " if ok else "FAIL  ") + name + (("  " + detail) if detail and not ok else ""))
    if not ok:
        fails += 1


tot_d = tot_b = 0
bad_enc, bad_img, bad_wt, bad_inj, bad_inv, bad_bij = [], [], [], [], [], []
for n in range(0, NMAX + 1):
    dn = D(n)
    tot_d += len(dn)
    imgs = {}
    for lam in dn:
        assert is_D(lam), lam
        b = shiftT_lean(lam)
        if b != T_int(lam):
            bad_enc.append((lam, b, T_int(lam)))
        if min(T_int(lam), default=0) < len(lam):
            bad_img.append((lam, T_int(lam)))
        if not is_B(b):
            bad_img.append((lam, b))
        if sum(b) != sum(lam):
            bad_wt.append((lam, b))
        if b in imgs:
            bad_inj.append((lam, imgs[b], b))
        imgs[b] = lam
        if shiftInv_lean(b) != lam:
            bad_inv.append(("left", lam, b, shiftInv_lean(b)))
        if shiftT_lean(shiftInv_lean(b)) != b:
            bad_inv.append(("right", lam, b, shiftT_lean(shiftInv_lean(b))))
    bset = B(n)
    tot_b += len(bset)
    if set(imgs) != bset:
        bad_bij.append((n, sorted(set(imgs) - bset)[:3], sorted(bset - set(imgs))[:3]))

check("encoding: shiftT_lean == integer formula T(lam)_i = lam_i-k+2i-1 on all D_n, n<=%d" % NMAX,
      not bad_enc, str(bad_enc[:3]))
check("image: T(D_n) subset of B_n (descending, smallest part >= k), n<=%d" % NMAX,
      not bad_img, str(bad_img[:3]))
check("weight: sum(T(lam)) == sum(lam) on all D_n, n<=%d" % NMAX,
      not bad_wt, str(bad_wt[:3]))
check("injectivity: T is injective on D_n, n<=%d" % NMAX,
      not bad_inj, str(bad_inj[:3]))
check("inverse laws: shiftInv(shiftT lam) == lam and shiftT(shiftInv b) == b",
      not bad_inv, str(bad_inv[:3]))
check("bijection: T(D_n) == B_n as sets, for every n<=%d" % NMAX,
      not bad_bij, str(bad_bij[:3]))
check("counts: |D_n| == |B_n| for n<=%d (both enumerated independently)" % NMAX,
      tot_d == tot_b, "|D|=%d |B|=%d" % (tot_d, tot_b))

check("control: [1,3] is Pos but not Gap and T loses weight there",
      all(x > 0 for x in (1, 3)) and not is_D([1, 3])
      and sum(shiftT_lean((1, 3))) != sum((1, 3)),
      str((shiftT_lean((1, 3)), sum(shiftT_lean((1, 3))))))
check("control: T collapses [0] and [1] (Pos is needed for injectivity)",
      shiftT_lean((0,)) == shiftT_lean((1,)),
      str((shiftT_lean((0,)), shiftT_lean((1,)))))
check("control: [2,5] meets the entry bound but is not descending, and shiftInv [2,5] is not a gap list",
      all(x >= 2 for x in (2, 5)) and not is_B((2, 5)) and not is_D(shiftInv_lean((2, 5))),
      str(shiftInv_lean((2, 5))))

print()
print("total: 10 checks, %d FAIL" % fails)
print("objects: %d D-objects, %d B-objects for n <= %d" % (tot_d, tot_b, NMAX))
sys.exit(1 if fails else 0)
