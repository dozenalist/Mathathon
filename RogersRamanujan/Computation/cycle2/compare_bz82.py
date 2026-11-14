#!/usr/bin/env python3
"""
compare_bz82.py -- deliverable (iv): the minimal discrepancy list between the
fresh implementation `cycle2/bz82_audit.py` and the committed
`Computation/bz82.py`.

Run only AFTER bz82_audit.py was written, exhaustively tested and frozen; the
comparison is one-directional evidence (it can only show that the two agree or
where they do not), never a justification of the fresh transcription.

Compared over all of X(n) for n <= NMAX (default 30):
   * phi on every state of phi's domain,
   * psi on every state of psi's domain,
   * the endpoint map forward = Tinv . pi on every object of A_n, together
     with injectivity onto D_n for the fresh implementation,
   * phi_domain / psi_domain agreement on every state of X(n),
and the same three printed examples through the committed code.

Usage: python3 compare_bz82.py [NMAX]
Writes compare_cycle2.json.  Exit 0 iff there are no discrepancies.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bz82_audit as MINE          # noqa: E402
import bz82 as THEIRS             # noqa: E402

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30


def main():
    disc = []
    counts = dict(phi=0, psi=0, phi_domain=0, psi_domain=0,
                  forward=0, forward_injective=0, forward_onto_D=0,
                  inverse=0, examples=0)
    for n in range(NMAX + 1):
        for (j, lam) in MINE.states_of_weight(n):
            st = (j, lam)
            mine_dom = MINE.phi_domain(j, lam)
            their_dom = THEIRS.phi_domain(st, n)
            if mine_dom != their_dom:
                disc.append(dict(kind="phi_domain", state=[j, list(lam)], n=n,
                                 mine=mine_dom, theirs=their_dom))
            else:
                counts["phi_domain"] += 1
            mine_dom = MINE.psi_domain(j, lam)
            their_dom = THEIRS.psi_domain(st, n)
            if mine_dom != their_dom:
                disc.append(dict(kind="psi_domain", state=[j, list(lam)], n=n,
                                 mine=mine_dom, theirs=their_dom))
            else:
                counts["psi_domain"] += 1
            if MINE.phi_domain(j, lam):
                counts["phi"] += 1
                a = MINE.phi(j, lam)[0]
                try:
                    b = THEIRS.phi(st)
                except Exception as e:                      # pragma: no cover
                    disc.append(dict(kind="phi_raised", state=[j, list(lam)], n=n,
                                     err=repr(e)[:120]))
                    continue
                if a != b:
                    disc.append(dict(kind="phi", state=[j, list(lam)], n=n,
                                     mine=[a[0], list(a[1])], theirs=[b[0], list(b[1])]))
            if MINE.psi_domain(j, lam):
                counts["psi"] += 1
                a = MINE.psi(j, lam)[0]
                try:
                    b = THEIRS.psi(st)
                except Exception as e:                      # pragma: no cover
                    disc.append(dict(kind="psi_raised", state=[j, list(lam)], n=n,
                                     err=repr(e)[:120]))
                    continue
                if a != b:
                    disc.append(dict(kind="psi", state=[j, list(lam)], n=n,
                                     mine=[a[0], list(a[1])], theirs=[b[0], list(b[1])]))

        # ---- the endpoint map on A_n vs D_n ----
        images = {}
        for lam in MINE.partitions(n):
            if not MINE.in_A(lam):
                continue
            out, steps, _ = MINE.pi_iterate(lam)
            if not MINE.in_B(out):
                disc.append(dict(kind="pi_not_in_B", lam=list(lam), n=n, out=list(out)))
                continue
            d = MINE.Tinv(out)
            counts["forward"] += 1
            if not (all(d[i] >= d[i + 1] + 2 for i in range(len(d) - 1))):
                disc.append(dict(kind="Tinv_not_in_D", lam=list(lam), n=n, d=list(d)))
            if d in images:
                disc.append(dict(kind="forward_not_injective", lam=list(lam), n=n,
                                 clash=list(images[d])))
            else:
                images[d] = lam
                counts["forward_injective"] += 1
            b = THEIRS.forward(lam)
            if b != d:
                disc.append(dict(kind="forward", lam=list(lam), n=n,
                                 mine=list(d), theirs=list(b)))
        dset = set()
        for lam in MINE.partitions(n):
            if all(lam[i] >= lam[i + 1] + 2 for i in range(len(lam) - 1)):
                dset.add(lam)
        if set(images) != dset:
            disc.append(dict(kind="forward_not_onto_D", n=n,
                             missing=[list(x) for x in sorted(dset - set(images))],
                             extra=[list(x) for x in sorted(set(images) - dset)]))
        else:
            counts["forward_onto_D"] += 1

    # ---- the three printed examples through the committed code ----
    ex = []
    ex.append(dict(which="(1)", theirs=[list(x) if isinstance(x, tuple) else x
                                        for x in THEIRS.phi((2, (11, 9, 8, 7, 6, 1, 1, 1)))],
                   expected=[3, [10, 9, 7, 2, 2, 2]]))
    ex.append(dict(which="(2)", theirs=[list(x) if isinstance(x, tuple) else x
                                        for x in THEIRS.psi((-2, (15, 14, 9, 9, 8, 8, 8, 5, 5, 4, 3, 2, 1)))],
                   expected=[-3, [14, 10, 9, 9, 8, 8, 8, 4, 3, 2, 2, 1]]))
    ex.append(dict(which="(3)", theirs=[list(x) if isinstance(x, tuple) else x
                                        for x in THEIRS.forward((4, 1))],
                   expected=[4, 1]))
    for e in ex:
        e["ok"] = e["theirs"] == e["expected"]
        if not e["ok"]:
            disc.append(dict(kind="example_" + e["which"], mine=e["expected"],
                             theirs=e["theirs"]))
        counts["examples"] += 1

    out = dict(nmax=NMAX, counts=counts, discrepancies=disc,
               n_discrepancies=len(disc), examples=ex)
    with open("compare_cycle2.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)

    print("NMAX =", NMAX)
    print("compared: phi %d, psi %d, domains %d+%d, forward %d, onto-D per weight %d/%d, examples %d"
          % (counts["phi"], counts["psi"], counts["phi_domain"], counts["psi_domain"],
             counts["forward"], counts["forward_onto_D"], NMAX + 1, counts["examples"]))
    print("DISCREPANCIES:", len(disc))
    for d in disc[:15]:
        print("  ", d)
    print("examples through the committed code:", [e["ok"] for e in ex])
    return 0 if not disc else 1


if __name__ == "__main__":
    sys.exit(main())
