"""Is the circulant C_n(a..b) (distances a,a+1,...,b on Z/n) 3-colourable?

A frozen palette field with three pairwise disjoint palettes of size 2 (so exactly
three colours) whose 'safe' shift set contains the integer interval [a,b] is exactly
a proper 3-colouring of C_n(a..b) (symmetrically: also of the negative shifts, which
for C_n is the same graph because distances are symmetric).

C_n(a..b) contains a K_4 as soon as there is k with k, 2k, 3k all in [a,b]: the
vertices 0,k,2k,3k are pairwise at circular distance in {k,2k,3k} c [a,b].
So b >= 3a  =>  not 3-colourable.  Question: is b < 3a sufficient?
"""
import sys

def colourable3(n, a, b, verbose=False):
    """DFS 3-colouring of the circulant with connection set {a..b} (and negatives)."""
    K = set()
    for k in range(a, b+1):
        K.add(k % n); K.add((-k) % n)
    K.discard(0)
    adj = [[ (i+k) % n for k in sorted(K)] for i in range(n)]
    colour = [-1]*n
    # symmetry break: vertex 0 gets colour 0; vertex of minimal index adjacent to 0 gets 1
    colour[0] = 0
    # order: BFS from 0 for pruning
    order = []
    seen = [False]*n
    stack = [0]; seen[0] = True
    while stack:
        v = stack.pop(); order.append(v)
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True; stack.append(w)
    for v in range(n):
        if not seen[v]:
            seen[v]=True; order.append(v); stack=[v]
            while stack:
                u=stack.pop()
                for w in adj[u]:
                    if not seen[w]:
                        seen[w]=True; stack.append(w); order.append(w)
    def bt(idx):
        if idx == len(order): return True
        v = order[idx]
        used = set(colour[w] for w in adj[v] if colour[w] >= 0)
        for c in range(3):
            if c in used: continue
            colour[v] = c
            if bt(idx+1): return True
            colour[v] = -1
        return False
    return bt(0)

if __name__ == "__main__":
    tests = [(12,4,11),(18,6,17),(30,10,29),
             (60,10,19),(60,10,20),(60,10,25),(60,10,28),(60,10,30),
             (90,15,29),(90,15,35),(90,15,40),(90,15,44),(90,15,45),
             (120,20,39),(120,20,45),(120,20,55),(120,20,59),(120,20,60)]
    for (n,a,b) in tests:
        r = colourable3(n,a,b)
        print(f"n={n:4d} a={a:3d} b={b:3d}  b/a={b/a:.3f}  3-colourable={r}")
