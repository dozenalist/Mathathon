#!/usr/bin/env python3
"""Transcription check: does the audit's psi/phi (written from the brief) agree
with the committed reference implementation Computation/bz82.py?

This is NOT a census (direction A owns that); it is here so that the audit in
AMENDED_PROOF.md is provably about BZ82's map and not about a variant of it.
Both maps are also compared on their *domain*, i.e. on which states they refuse.

Run: python3 crosscheck.py 26
"""
import sys, os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', '..', 'Computation', 'bz82.py')
sys.path.insert(0, os.path.dirname(os.path.abspath(REF)))   # bz82 imports rr_core
spec = importlib.util.spec_from_file_location('bz82_ref', REF)
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)

import psi_audit as A
import phi_skeleton as F

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 26
    bad_psi = bad_phi = bad_dom_psi = bad_dom_phi = 0
    n_states = n_dom = 0
    for n in range(N + 1):
        for (j, lam) in A.states(n):
            s = (j, lam); n_states += 1
            # ---- psi
            try:
                mine = A.psi(j, lam); mine_ok = True
            except A.Undef:
                mine_ok = False
            try:
                theirs = ref.psi(s); theirs_ok = True
            except ValueError:
                theirs_ok = False
            if mine_ok != theirs_ok:
                bad_dom_psi += 1
                if bad_dom_psi == 1:
                    print('psi domain disagreement at %r: mine=%s ref=%s' % (s, mine_ok, theirs_ok))
            elif mine_ok:
                n_dom += 1
                if mine != theirs:
                    bad_psi += 1
                    if bad_psi == 1:
                        print('psi value disagreement at %r: mine=%r ref=%r' % (s, mine, theirs))
            # ---- phi
            try:
                mine = F.phi(j, lam); mine_ok = True
            except F.Undef:
                mine_ok = False
            try:
                theirs = ref.phi(s); theirs_ok = True
            except ValueError:
                theirs_ok = False
            if mine_ok != theirs_ok:
                bad_dom_phi += 1
                if bad_dom_phi == 1:
                    print('phi domain disagreement at %r: mine=%s ref=%s' % (s, mine_ok, theirs_ok))
            elif mine_ok and mine != theirs:
                bad_phi += 1
                if bad_phi == 1:
                    print('phi value disagreement at %r: mine=%r ref=%r' % (s, mine, theirs))
    print('n = 0..%d, %d states of X(n), %d in the psi domain' % (N, n_states, n_dom))
    print('psi: domain disagreements %d, value disagreements %d' % (bad_dom_psi, bad_psi))
    print('phi: domain disagreements %d, value disagreements %d' % (bad_dom_phi, bad_phi))
    print('VERDICT: %s' % ('identical maps on the tested range'
                           if not (bad_psi or bad_phi or bad_dom_psi or bad_dom_phi) else 'DIFFERENCES'))
    return 0 if not (bad_psi or bad_phi or bad_dom_psi or bad_dom_phi) else 1

if __name__ == '__main__':
    sys.exit(main())
