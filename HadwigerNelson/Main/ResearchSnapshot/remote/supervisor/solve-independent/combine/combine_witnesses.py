"""Witness combination for glued unit-distance copies -- SOURCE ONLY, not executed here.

Pure stdlib. One bounded entry point: `python3 combine_witnesses.py fixtures.json`.
It does NOT search, does not solve SAT, and never decides colourability of a union.

The mathematical contract (see ../audit-amplifier/WITNESS-COMBINATION.md):

  Two copies A, B of a point graph, an identification list I (index pairs that are the SAME
  point) and a cross-edge list Ex (index pairs at unit distance, one in each copy).  A joint
  colouring is (cA, cB) in C_k(A) x C_k(B) with
      (b) cA[u] == cB[v]  for all (u,v) in I
      (x) cA[x] != cB[y]  for all (x,y) in Ex.

  Given certified families PhiA, PhiB of proper k-colourings, we look for
  phi in PhiA, psi in PhiB and a permutation pi of [k] with
      (P) pi[psi[v]] == phi[u]      for all (u,v) in I        -- "pins"
      (F) pi[psi[y]] != phi[x]      for all (x,y) in Ex       -- "forbidden cells"
  and emit cA = phi, cB = pi o psi.

  NORMALISATION (corrected).  Restricting the search to a permutation applied to B alone is
  justified *up to a common global relabelling*, NOT by literal equality of labelled pairs:
  a simultaneous relabelling rho maps (cA,cB) |-> (rho cA, rho cB), which preserves every
  equality (b) and every disequality (x), so J is invariant under the diagonal S_k action.
  Hence (piA phi, piB psi) in J  <=>  (phi, piA^{-1} piB psi) in J.  The pairs differ as
  labelled objects; membership is what transfers.

  SOUNDNESS.  A returned witness is re-verified from scratch by verify_joint(), which shares
  no code path with the pin/matching logic.
  INCOMPLETENESS.  NO_WITNESS below means "no witness from the sampled families".  It is NOT
  a proof that the union is not k-colourable.
"""
from __future__ import annotations
import json
import sys

# ---------------------------------------------------------------- reason codes


class Reason:
    # --- invalid input: the whole call is rejected, no inference at all
    BAD_INDEX = "BAD_INDEX"                       # index out of range
    DUPLICATE_INDEX = "DUPLICATE_INDEX"           # repeated entry in a list that must be a set
    MISSING_BOUNDARY = "MISSING_BOUNDARY"         # a certified coincidence missing from I
    EXTRA_BOUNDARY = "EXTRA_BOUNDARY"             # an entry of I that is not a coincidence
    SEED_INCONSISTENT = "SEED_INCONSISTENT"       # e.g. a cross edge on an identified pair
    FAMILY_NOT_PROPER = "FAMILY_NOT_PROPER"       # a supplied colouring is not proper
    FAMILY_BAD_SHAPE = "FAMILY_BAD_SHAPE"         # wrong length or colour outside [k]
    # --- per-pair failure: this (phi,psi) yields nothing; others may still succeed
    PIN_INCONSISTENT = "PIN_INCONSISTENT"         # a key pinned to two values
    PIN_NOT_INJECTIVE = "PIN_NOT_INJECTIVE"       # two keys pinned to one value
    PIN_FORBIDDEN = "PIN_FORBIDDEN"               # a pinned cell lies in D
    NO_MATCHING = "NO_MATCHING"                   # residual bipartite matching fails


SEED_LEVEL = {
    Reason.BAD_INDEX, Reason.DUPLICATE_INDEX, Reason.MISSING_BOUNDARY,
    Reason.EXTRA_BOUNDARY, Reason.SEED_INCONSISTENT,
    Reason.FAMILY_NOT_PROPER, Reason.FAMILY_BAD_SHAPE,
}


# ---------------------------------------------------------------- validation


def _check_pairs(pairs, nA, nB, what):
    """Range checks and duplicate detection for a list of (i,j) index pairs."""
    seen = set()
    for pr in pairs:
        if len(pr) != 2:
            return f"{Reason.BAD_INDEX}:{what}:not a pair {pr}"
        i, j = int(pr[0]), int(pr[1])
        if not (0 <= i < nA) or not (0 <= j < nB):
            return f"{Reason.BAD_INDEX}:{what}:{pr}"
        if (i, j) in seen:
            return f"{Reason.DUPLICATE_INDEX}:{what}:{pr}"
        seen.add((i, j))
    return None


def validate_seed(k, nA, nB, I, coincident, Ex):
    """Structural validation. Returns None or a 'REASON:detail' string (seed-level)."""
    if k < 1:
        return f"{Reason.BAD_INDEX}:k"
    for pairs, what in ((I, "I"), (Ex, "Ex"), (coincident, "coincident")):
        err = _check_pairs(pairs, nA, nB, what)
        if err:
            return err
    # completeness of the boundary: I must be exactly the certified coincidence set
    Iset, Cset = {(int(a), int(b)) for a, b in I}, {(int(a), int(b)) for a, b in coincident}
    if Cset - Iset:
        return f"{Reason.MISSING_BOUNDARY}:{sorted(Cset - Iset)}"
    if Iset - Cset:
        return f"{Reason.EXTRA_BOUNDARY}:{sorted(Iset - Cset)}"
    # a cross edge on an identified pair is an immediate contradiction
    for (x, y) in Iset:
        if (x, y) in {(int(a), int(b)) for a, b in Ex}:
            return f"{Reason.SEED_INCONSISTENT}:cross_on_identified:{x},{y}"
    return None


def validate_family(k, n, edges, fam, name):
    """Every supplied colouring must be a proper k-colouring of its copy."""
    for idx, c in enumerate(fam):
        if len(c) != n:
            return f"{Reason.FAMILY_BAD_SHAPE}:{name}[{idx}]:len{len(c)}!={n}"
        if any(not (0 <= int(v) < k) for v in c):
            return f"{Reason.FAMILY_BAD_SHAPE}:{name}[{idx}]:colour_out_of_range"
        for (i, j) in edges:
            if int(c[int(i)]) == int(c[int(j)]):
                return f"{Reason.FAMILY_NOT_PROPER}:{name}[{idx}]:edge({i},{j})"
    return None


# ---------------------------------------------------------------- constraints


def build_constraints(k, I, Ex, phi, psi):
    """Pins sigma (dict) and forbidden cells D (set of (key,value)) for one (phi,psi).

    Returns (None, 'REASON:detail') on a per-pair failure, else (sigma, D).
    """
    sigma = {}
    for (u, v) in I:
        key, val = int(psi[int(v)]), int(phi[int(u)])
        if key in sigma and sigma[key] != val:
            return None, f"{Reason.PIN_INCONSISTENT}:key{key}->{sigma[key]}|{val}"
        sigma[key] = val
    if len(set(sigma.values())) != len(sigma):
        return None, f"{Reason.PIN_NOT_INJECTIVE}:{sorted(sigma.items())}"
    D = {(int(psi[int(y)]), int(phi[int(x)])) for (x, y) in Ex}
    for key, val in sigma.items():
        if (key, val) in D:
            return None, f"{Reason.PIN_FORBIDDEN}:({key},{val})"
    return (sigma, D), None


def residual_match(k, sigma, D):
    """Complete sigma to a permutation of [k] avoiding D, by augmenting paths on the residual.

    Preferred over enumerating all k! permutations: after the pins only k-|sigma| domain
    elements remain, and the residual bipartite graph has at most k*k cells.  O(k^3) worst
    case, k <= 6.  Returns a dict pi or None.
    """
    used_dom, used_cod = set(sigma), set(sigma.values())
    dom = [a for a in range(k) if a not in used_dom]
    cod = [b for b in range(k) if b not in used_cod]
    match_cod = {}                                    # codomain element -> domain element

    def augment(a, seen):
        for b in cod:
            if b in seen or (a, b) in D:
                continue
            seen.add(b)
            if b not in match_cod or augment(match_cod[b], seen):
                match_cod[b] = a
                return True
        return False

    for a in dom:
        if not augment(a, set()):
            return None
    pi = dict(sigma)
    for b, a in match_cod.items():
        pi[a] = b
    return pi


# ---------------------------------------------------------------- verification


def verify_joint(k, nA, nB, edgesA, edgesB, I, Ex, cA, cB):
    """Independent check of an emitted witness. Shares no code with the matching logic.

    Returns a list of error strings (empty means the witness is a genuine member of J).
    """
    errs = []
    for (name, c, n) in (("cA", cA, nA), ("cB", cB, nB)):
        if c is None or len(c) != n:
            errs.append(f"{name}:bad_length")
            continue
        if any(not (0 <= int(v) < k) for v in c):
            errs.append(f"{name}:colour_out_of_range")
    if errs:
        return errs
    for (i, j) in edgesA:
        if int(cA[int(i)]) == int(cA[int(j)]):
            errs.append(f"cA:not_proper:({i},{j})")
    for (i, j) in edgesB:
        if int(cB[int(i)]) == int(cB[int(j)]):
            errs.append(f"cB:not_proper:({i},{j})")
    for (u, v) in I:
        if int(cA[int(u)]) != int(cB[int(v)]):
            errs.append(f"boundary:({u},{v}):{cA[int(u)]}!={cB[int(v)]}")
    for (x, y) in Ex:
        if int(cA[int(x)]) == int(cB[int(y)]):
            errs.append(f"cross:({x},{y}):both {cA[int(x)]}")
    return errs


# ---------------------------------------------------------------- driver


def combine(k, nA, nB, edgesA, edgesB, I, coincident, Ex, PhiA, PhiB, dedupe=True):
    """Return (dict outcome). Never raises on bad input; always reports a reason code."""
    seed_err = validate_seed(k, nA, nB, I, coincident, Ex)
    if seed_err:
        return {"outcome": "seed_rejected", "reason": seed_err}
    for fam, n, edges, name in ((PhiA, nA, edgesA, "PhiA"), (PhiB, nB, edgesB, "PhiB")):
        err = validate_family(k, n, edges, fam, name)
        if err:
            return {"outcome": "seed_rejected", "reason": err}

    # dedupe by signature on the active set: the constraints see only these coordinates
    actA = sorted({int(u) for u, _ in I} | {int(x) for x, _ in Ex})
    actB = sorted({int(v) for _, v in I} | {int(y) for _, y in Ex})
    FA = _dedupe(PhiA, actA) if dedupe else [(c, None) for c in PhiA]
    FB = _dedupe(PhiB, actB) if dedupe else [(c, None) for c in PhiB]

    pair_failures = {}
    for phi, _ in FA:
        for psi, _ in FB:
            got, why = build_constraints(k, I, Ex, phi, psi)
            if got is None:
                pair_failures[why.split(":")[0]] = pair_failures.get(why.split(":")[0], 0) + 1
                continue
            sigma, D = got
            pi = residual_match(k, sigma, D)
            if pi is None:
                pair_failures[Reason.NO_MATCHING] = pair_failures.get(Reason.NO_MATCHING, 0) + 1
                continue
            cA = [int(v) for v in phi]
            cB = [int(pi[int(v)]) for v in psi]
            errs = verify_joint(k, nA, nB, edgesA, edgesB, I, Ex, cA, cB)
            if errs:
                # a bug, not a near miss: the matcher and the verifier disagree
                return {"outcome": "internal_inconsistency", "errors": errs}
            return {"outcome": "witness", "cA": cA, "cB": cB,
                    "pi": {int(a): int(b) for a, b in pi.items()},
                    "pairs_tried_failed": pair_failures}
    return {"outcome": "no_witness", "reason": "sampled_families_only",
            "pair_failures": pair_failures,
            "note": "NOT a proof that the union is not k-colourable"}


def _dedupe(fam, act):
    seen, out = set(), []
    for c in fam:
        sig = tuple(int(c[i]) for i in act)
        if sig not in seen:
            seen.add(sig)
            out.append((c, sig))
    return out


# ---------------------------------------------------------------- fixtures


def run_fixture(fx):
    res = combine(fx["k"], fx["nA"], fx["nB"], fx["edgesA"], fx["edgesB"],
                  fx["I"], fx["coincident"], fx["Ex"], fx["PhiA"], fx["PhiB"])
    exp = fx["expect"]
    ok = res["outcome"] == exp["outcome"]
    if ok and exp["outcome"] == "seed_rejected":
        ok = res["reason"].split(":")[0] == exp["reason"]
    if ok and exp["outcome"] == "witness":
        ok = len(verify_joint(fx["k"], fx["nA"], fx["nB"], fx["edgesA"], fx["edgesB"],
                              fx["I"], fx["Ex"], res["cA"], res["cB"])) == 0
    return ok, res, exp


def main(argv):
    path = argv[1] if len(argv) > 1 else "fixtures.json"
    doc = json.load(open(path))
    bad = 0
    for fx in doc["fixtures"]:
        ok, res, exp = run_fixture(fx)
        bad += 0 if ok else 1
        print(f"[{'PASS' if ok else 'FAIL'}] {fx['name']}: got {res['outcome']}"
              f"{'/' + res.get('reason', '') if res.get('reason') else ''}"
              f"  expected {exp['outcome']}{'/' + exp.get('reason', '') if exp.get('reason') else ''}")
    print(f"\n{len(doc['fixtures']) - bad}/{len(doc['fixtures'])} fixtures agree with expectation")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
