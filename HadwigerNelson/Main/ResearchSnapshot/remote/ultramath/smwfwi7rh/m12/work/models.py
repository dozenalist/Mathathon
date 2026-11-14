"""Sector palette models at k=6: direction sets of palette values (angles in degrees)."""
import numpy as np

def block_word(blocks, n=36, L=4):
    return [blocks[(i//L)%3] for i in range(n)]

BLOCKS = {
 "block_l3": [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})],
 "block_l4": [frozenset({0,2}), frozenset({1,4}), frozenset({3,5})],
 "block_l5": [frozenset({0,2}), frozenset({1,3}), frozenset({4,5})],
 "block_l6": [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})],
 "free_l3":  [frozenset({3}),    frozenset({4}),    frozenset({5})],
 "free_l4":  [frozenset({0,2}),  frozenset({1,3}),  frozenset({4})],
 "free_l5":  [frozenset({0,2}),  frozenset({1,3}),  frozenset({5})],
}
_free_l6_rows = [[(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
                 [(3,5),(3,5),(2,5),(2,5),(2,4,5),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
                 [(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)]]

def words():
    W = {k: (36, block_word(v)) for k,v in BLOCKS.items()}
    W["free_l6"] = (36, [frozenset(t) for r in _free_l6_rows for t in r])
    # m13 singleton triangle model: s(t) = floor(9t/2pi) mod 3, values {4+s}
    n=36; w=[]
    for i in range(n):
        th=(i+0.5)*2*np.pi/n
        w.append(frozenset({4+int(np.floor(9*th/(2*np.pi)))%3}))
    W["sing_l3"]=(n,w)
    return W

def dirset(n, word, value):
    """list of (lo,hi) degree intervals where word == value"""
    out=[]; i=0; step=360.0/n
    while i<n:
        if word[i]==value:
            j=i
            while j+1<n and word[j+1]==value: j+=1
            out.append((i*step,(j+1)*step)); i=j+1
        else: i+=1
    return out

def in_set(x, intervals):
    """x: array of degrees (any real). True where x mod 360 lies in one of the half-open intervals."""
    y = np.mod(x,360.0)
    m = np.zeros(y.shape, dtype=bool)
    for lo,hi in intervals:
        m |= (y>=lo)&(y<hi)
    return m

def member(W, IA, IB, tol_swap=True):
    """boolean array: which w (complex array) lie in IA+IB  (all angles in degrees)"""
    r = np.abs(W)
    out = np.zeros(W.shape, dtype=bool)
    ok = r<=2.0
    beta = np.zeros_like(r); np.arccos(np.clip(r/2,0,1), out=beta, where=ok)
    argw = np.angle(W, deg=True)
    for s in (+1,-1):
        th = argw + s*beta
        u = np.exp(1j*np.radians(th))
        v = W-u
        ph = np.angle(v, deg=True)
        # need |v|=1: only valid where r>0 (v is au  to unit by construction)
        good = ok & (r>1e-12) & in_set(th,IA) & in_set(ph,IB)
        out |= good
        if tol_swap:
            out |= ok & (r>1e-12) & in_set(th,IB) & in_set(ph,IA)
    # r == 0 : phi = theta+180 ; theta in IA, theta+180 in IB (or swapped)
    if np.any(r<=1e-12):
        # test a fine set of theta
        tt = np.arange(0,360,0.01)
        hitA = np.any(in_set(tt,IA) & in_set(tt+180.0,IB)) or np.any(in_set(tt,IB) & in_set(tt+180.0,IA))
        out |= (r<=1e-12) & hitA
    return out
