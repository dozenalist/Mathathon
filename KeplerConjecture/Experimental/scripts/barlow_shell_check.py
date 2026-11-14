"""
Distance spectrum of Barlow (hexagonal-layer) packings about a centre.
Unit spheres, minimum separation 2.  Exact rational/surd arithmetic where possible.
K15-E013: is the shell (2, 2.09) empty, i.e. are there at most 12 centres in [2,2.09]?
"""
import numpy as np, json
s3=np.sqrt(3.0)

def layer(z, shift=(0.0,0.0)):
    """triangular lattice, spacing 2, at height z, shifted in the plane."""
    sx,sy=shift
    P=[]
    for m in range(-4,5):
        for n in range(-4,5):
            P.append([2*m + n*1.0 + sx, n*s3 + sy, z])
    return np.array(P)

def stack(seq, h):
    """seq: shifts per layer; the CENTRE layer is the middle element (index len//2)."""
    mid=len(seq)//2
    sx,sy=seq[mid]                      # translate so the origin IS a centre
    P=[layer((i-mid)*h, (s[0]-sx, s[1]-sy)) for i,s in enumerate(seq)]
    return np.vstack(P)

def spectrum(P, tol=1e-9):
    d=np.linalg.norm(P,axis=1)
    d=d[d>tol]
    d=np.sort(d)
    # group
    out=[]; cur=[d[0]]
    for x in d[1:]:
        if x-cur[-1]<1e-6: cur.append(x)
        else: out.append((float(np.mean(cur)), len(cur))); cur=[x]
    out.append((float(np.mean(cur)), len(cur)))
    return out[:8]

h = 2*np.sqrt(2.0/3.0)
res={}
A=(0.0,0.0); B=(1.0, s3/3.0); C=(1.0, -s3/3.0)     # the two hollows
for name, seq in [("fcc (ABC)",[A,B,C,A,B,C,A]),
                  ("hcp (AB)",[A,B,A,B,A,B,A]),
                  ("mixed (ABCB)",[A,B,C,B,A,B,C]),
                  ("mixed (ABAC)",[A,B,A,C,A,B,A])]:
    P=stack(seq,h)
    # keep centres within radius 4 to speed up
    P=P[np.linalg.norm(P,axis=1)<4.0]
    sp=spectrum(P)
    res[name]=sp
    n_in=[ (r,c) for r,c in sp if 2-1e-9<=r<=2.09+1e-9]
    tot=sum(c for r,c in sp if 2-1e-9<=r<=2.09+1e-9)
    print(f"{name}: h={h:.6f}")
    for r,c in sp: print(f"    r={r:.6f}  count={c}")
    print(f"    -> centres in [2,2.09]: {tot}")
    print()
print(json.dumps({"h":h,"spectra":{k:[list(x) for x in v] for k,v in res.items()}},indent=1)[:400])
