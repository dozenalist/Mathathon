"""Integer-arithmetic fast checker (valid when all angles are integers)."""
MC = [(0,2,4),(1,3,5)]+[(i,(i+1)%6,(i+3)%6) for i in range(6)]+[(i,(i+1)%6,(i+4)%6) for i in range(6)]
EM = [(0,2,4),(1,3,5),(0,1,3,4),(0,2,3,5),(1,2,4,5)]
PAIRS = [(i,j) for i in range(6) for j in range(i+1,6) if (j-i)%6 in (2,3,4)]

def diam(S):
    pts=sorted(set(S))
    if len(pts)<=1: return 0
    mg=max([pts[k+1]-pts[k] for k in range(len(pts)-1)]+[pts[0]+360-pts[-1]])
    return 360-mg

def ok(al):
    a=[x%360 for x in al]
    for i,j in PAIRS:
        if diam((a[i],a[j]))<=60: return False
    for G in MC:
        if diam([a[i] for i in G])<120: return False
    for G in EM:
        if diam([a[i] for i in G])<180: return False
    return True
