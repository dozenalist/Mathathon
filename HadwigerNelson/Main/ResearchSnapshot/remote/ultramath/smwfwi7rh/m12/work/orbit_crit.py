"""Exact orbit criterion on the direction circle, no periodicity assumed.
Sets are unions of rational arcs in degrees, kept normalised to [0,360)."""
from fractions import Fraction as F

def merge(iv):
    iv = sorted(iv); out = []
    for lo,hi in iv:
        if out and lo <= out[-1][1]: out[-1] = (out[-1][0], max(out[-1][1],hi))
        else: out.append((lo,hi))
    return out

def norm(E):
    """union of arcs -> normalised union of arcs inside [0,360)"""
    out=[]
    for lo,hi in E:
        lo=F(lo); hi=F(hi)
        if hi-lo >= 360: return [(F(0),F(360))]
        a = lo % 360; rem = hi-lo
        while rem > 0:
            take = min(F(360)-a, rem); out.append((a,a+take)); rem -= take; a = F(0)
    return merge(out)

def shift(E, s_lo, s_hi):
    """union over s in [s_lo,s_hi] of (E - s) mod 360"""
    E = norm(E); out=[]
    for lo,hi in E:
        a = (lo - s_hi) % 360
        length = (hi - s_lo) - (lo - s_hi)
        if length >= 360: return [(F(0),F(360))]
        x = a
        while length > 0:
            take = min(F(360)-x, length); out.append((x,x+take)); length -= take; x = F(0)
    return merge(out)

def inter(P,Q):
    P=norm(P); Q=norm(Q); out=[]
    for a1,a2 in P:
        for b1,b2 in Q:
            lo,hi = max(a1,b1), min(a2,b2)
            if hi>lo: out.append((lo,hi))
    return merge(out)

def width(E): return sum(hi-lo for lo,hi in E)

def widest(E):
    E=norm(E)
    return max(E, key=lambda t: t[1]-t[0]) if E else None

def orbit3(E):
    return inter(inter(E, shift(E,120,120)), shift(E,240,240))

def criterion(EA, EB, PSI_LO, PSI_HI):
    """returns (role, witness interval) for both role assignments"""
    OA, OB = orbit3(EA), orbit3(EB)
    def shifted3(E):
        return inter(inter(shift(E, PSI_LO, PSI_HI), shift(E, PSI_LO+120, PSI_HI+120)),
                     shift(E, PSI_LO+240, PSI_HI+240))
    w1 = inter(OA, shifted3(EB))         # t in E_A-orbit, t+psi in E_B
    w2 = inter(OB, shifted3(EA))         # t in E_B-orbit, t+psi in E_A
    return w1, w2

def in_set(x, E):
    E = norm(E); x = F(x) % 360
    return any(lo <= x < hi for lo,hi in E)

def verify(EA, EB, t, psi_lo, psi_hi, role):
    """rigorous check of a concrete witness t for the whole psi enclosure"""
    if role == 'A->B':
        cond = all(in_set(t+120*j, EA) for j in range(3))
        cond = cond and all(in_set(t+psi+120*j, EB) for psi in (psi_lo,psi_hi) for j in range(3))
    else:
        cond = all(in_set(t+120*j, EB) for j in range(3))
        cond = cond and all(in_set(t+psi+120*j, EA) for psi in (psi_lo,psi_hi) for j in range(3))
    return cond
