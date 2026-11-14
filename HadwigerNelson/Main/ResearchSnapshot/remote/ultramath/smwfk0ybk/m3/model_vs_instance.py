"""Model-level vs instance-level strength of (C4)+(C5) at k = 6.

1. (C4) is NOT implied by (C1)-(C3) at the level of models: find an explicit
   (C1)-(C3) model of a satisfiable instance that contains two complementary
   palettes.  So the tightening does change the model class.
2. (C4)+(C5) IS vacuous at the level of instances: no instance loses
   satisfiability, because every satisfiable instance has a model with all
   palettes of size <= 2 (csp_vacuity.py, column C = column B).
3. Report the concrete model shapes at l = 5, 6 and the exact l = 3, 4 families.
"""
from itertools import product
from csp_vacuity import sig_matrix, slivers, admissible, solve, pc

K = 6


def complementary_pair(model):
    for i in range(6):
        for j in range(i + 1, 6):
            A, B = set(model[i]), set(model[j])
            if A | B == set(range(K)):
                return (i, j)
    return None


def find_c4_violating(l):
    """first instance with a (C1)-(C3) model containing a complementary pair"""
    for tail in product(range(6), repeat=l - 1):
        c = (0,) + tail
        adm = admissible(l, K, sig_matrix(l, c), K - 3)
        if any(not a for a in adm):
            continue
        # DFS over all models, looking for one with a complementary pair
        stack = []

        def dfs(i):
            if i == 6:
                if stack[5] & stack[0]:
                    return None
                pair = complementary_pair(
                    [sorted(x for x in range(K) if (p >> x) & 1) for p in stack])
                return list(stack) if pair else None
            for q in adm[i]:
                if i and (stack[i - 1] & q):
                    continue
                stack.append(q)
                r = dfs(i + 1)
                if r is not None:
                    return r
                stack.pop()
            return None

        r = dfs(0)
        if r is not None:
            return c, [sorted(x for x in range(K) if (p >> x) & 1) for p in r]
    return None, None


if __name__ == "__main__":
    for l in (3, 4, 5, 6):
        c, m = find_c4_violating(l)
        if c is None:
            print(f"l={l}: no (C1)-(C3) model contains a complementary pair")
        else:
            print(f"l={l}: instance cells={c} has (C1)-(C3) model {m}, "
                  f"complementary pair {complementary_pair(m)}")
    # explicit l=3 and l=4 families (the vacuity certificate)
    print()
    for l, pal in ((3, [[3], [4], [3], [4], [3], [4]]),
                   (4, [[4], [5], [4], [5], [4], [5]])):
        U = sorted(set(range(K)) - set(range(l)))
        print(f"l={l}: U={U}, palettes={pal}, sizes={[len(p) for p in pal]}")
