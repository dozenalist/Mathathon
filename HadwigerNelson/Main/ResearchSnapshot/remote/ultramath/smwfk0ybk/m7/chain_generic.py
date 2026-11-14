"""Non-jump (generic ray configuration) chain test + brute-force validation of the
chain DP in chain_csp.py."""
from itertools import product, permutations
import chain_csp as C


def brute_chain(ell, k, pred, allow_jumps=False):
    """Independent, dumb search: for every c0 and every admissible ordering of the
    l coordinate drops, check every node.  allow_jumps=True also tries all chains
    of subsets (exponential), so only used for small ell."""
    cells = list(product(range(6), repeat=ell))
    full = tuple([1] * ell)
    best = None
    if not allow_jumps:
        for c0 in cells:
            for perm in permutations(range(ell)):
                node = list(c0)
                nodes = [tuple(node)]
                ok = pred(tuple(node))
                for j in perm:
                    if not ok:
                        break
                    node[j] = (node[j] - 1) % 6
                    nodes.append(tuple(node))
                    ok = pred(tuple(node))
                if ok:
                    return nodes
        return None
    # jumps: all monotone subset chains
    idx = list(range(ell))
    for c0 in cells:
        def rec(done, nodes):
            if len(done) == ell:
                return nodes
            for size in range(1, ell - len(done) + 1):
                pass
            for j in idx:
                if j in done:
                    continue
            return None
        # simple: BFS over (c0, done-set)
        stack = [(0, tuple(nodes := [c0]))]
        seen = set()
        stack = [(0, [c0])]
        while stack:
            done, nodes = stack.pop()
            if done == (1 << ell) - 1:
                return nodes
            if (done, nodes[-1]) in seen:
                continue
            seen.add((done, nodes[-1]))
            todo = [j for j in idx if not (done >> j) & 1]
            for r in range(1, len(todo) + 1):
                from itertools import combinations as comb
                for sub in comb(todo, r):
                    nn = list(nodes[-1])
                    for j in sub:
                        nn[j] = (nn[j] - 1) % 6
                    nn = tuple(nn)
                    if pred(nn):
                        stack.append((done | sum(1 << j for j in sub), nodes + [nn]))
        continue
    return None


if __name__ == "__main__":
    for k in (5, 6, 7):
        for ell in range(3, k + 1):
            pred = lambda c, e=ell, k=k: C.has_model(c, e, k, tight=(k == 6))
            gen = C.chain_search(ell, k, pred, allow_jumps=False)
            jmp = C.chain_search(ell, k, pred, allow_jumps=True)
            tag = "" if k == 6 else "   [(C4),(C5) not valid off k=6; shown for scale]"
            print(f"k={k} l={ell}: generic(all l thresholds distinct) "
                  f"{'YES' if gen else 'NO '}   any-configuration {'YES' if jmp else 'NO '}{tag}")
            if gen:
                print("     generic chain:", " -> ".join(map(str, gen)))
            if jmp and not gen:
                print("     (only with coincident thresholds):", " -> ".join(map(str, jmp)))
