#!/usr/bin/env python3
"""
Procedure 1 (exhaustive, product-graph) for STRIP(k,ell) with variants.

For every delta in (Z/6)^ell:
  build O_j, I_j (j = 0..5);
  if some O_j or I_j is empty  -> delta blocked by S0 (k-blind: an open strip
                                  with no colour);
  build the option list Opt_j of admissible palettes at position j;
  decide whether the constraint graph on Opt_0 x ... x Opt_5 (edge between
  consecutive positions iff the palettes are disjoint) has a 6-cycle.

Verdicts and certificates:
  SAT   -> (delta, word); certified by model.check.
  UNSAT -> the list of per-delta blocking data: for each delta either a position
           with an empty allowed set, or the tuple of option lists (which the
           independent checker search2.py re-decides in CNF form).
"""
import itertools, json, sys
from model import allowed, cycle_edges

def options(k, ell, O, I, strong):
    cap = k - 3
    CE = cycle_edges(ell) if strong else []
    res = []
    for size in range(1, cap + 1):
        for P in itertools.combinations(range(k), size):
            Ps = frozenset(P)
            if (Ps & O) and (Ps & I) and not any(Ps <= ed for ed in CE):
                res.append(Ps)
    return res

def decide(k, ell, strong=False, collect_blocked=False):
    n_delta = 0
    blocked = []
    for delta in itertools.product(range(6), repeat=ell):
        n_delta += 1
        AI = allowed(k, ell, delta)
        if any(not O or not I for O, I in AI):
            if collect_blocked:
                blocked.append((delta, "S0"))
            continue
        opts = [options(k, ell, O, I, strong) for O, I in AI]
        if any(not o for o in opts):
            if collect_blocked:
                blocked.append((delta, "no-option"))
            continue
        # reachability with the first palette remembered: state = (first, current)
        # simple approach: for each first palette, forward DP over positions 1..5
        found = None
        for first in opts[0]:
            reach = {first}
            layers = [reach]
            for j in range(1, 6):
                nxt = set()
                for P in opts[j]:
                    if any(not (P & Q) for Q in reach):
                        nxt.add(P)
                layers.append(nxt)
                reach = nxt
                if not reach:
                    break
            if reach:
                # close: some last palette disjoint from first
                if any(not (P & first) for P in reach):
                    # reconstruct
                    word = [first]
                    for j in range(5, 0, -1):
                        target = word[0]
                        for P in opts[j]:
                            if not (P & layers[j - 1] & frozenset()) if False else False:
                                pass
                        break
                    found = (delta, layers, first)
                    break
        if found:
            # reconstruct a word by backwards search
            delta_, layers, first = found
            word = build_word(opts, first)
            return ("SAT", {"k": k, "ell": ell, "strong": strong,
                            "delta": list(delta_), "word": [sorted(w) for w in word]})
        if collect_blocked:
            blocked.append((delta, "no-word"))
    return ("UNSAT", {"k": k, "ell": ell, "strong": strong,
                      "n_delta": n_delta, "blocked": blocked if collect_blocked else "omitted"})

def build_word(opts, first):
    word = [first]
    for j in range(1, 6):
        for P in opts[j]:
            if not (P & word[-1]):
                word.append(P)
                break
        else:
            return None
    if word[-1] & first:
        # backtracking needed for tight cases
        def bt(j):
            if j == 6:
                return not (word[5] & first)
            for P in opts[j]:
                if j and (P & word[j - 1]):
                    continue
                word[j] = P
                if bt(j + 1):
                    return True
                word[j] = None
            return False
        w2 = [None] * 6
        for P0 in opts[0]:
            w2[0] = P0
            if bt(1):
                return w2
        return None
    return word

if __name__ == "__main__":
    out = {}
    for strong in (False, True):
        for k in range(4, 8):
            for ell in range(3, k + 1):
                v, cert = decide(k, ell, strong=strong)
                key = f"k{k}_l{ell}_{'strong' if strong else 'weak'}"
                out[key] = {"verdict": v, **{a: b for a, b in cert.items() if a != "blocked"}}
                msg = f"k={k} ell={ell} {'[+S4]' if strong else '     '}: {v}"
                if v == "SAT":
                    msg += f"   delta={cert['delta']} word={cert['word']}"
                print(msg)
    with open("strip_table.json", "w") as f:
        json.dump(out, f, indent=1)
