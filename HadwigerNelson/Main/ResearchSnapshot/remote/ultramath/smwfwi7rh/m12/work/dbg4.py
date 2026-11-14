import numpy as np, sys
sys.path.insert(0,'work')
from sumtest import member, in_set
IA=[(0,10),(30,40),(120,130),(140,150),(250,270),(280,290)]
IB=[(90,110),(180,190),(210,230),(300,310),(330,350)]
pts=[]
for lo,hi in IA:
    for a in np.linspace(lo,hi,15):
        for lo2,hi2 in IB:
            for b in np.linspace(lo2,hi2,15):
                pts.append(np.exp(1j*np.radians(a))+np.exp(1j*np.radians(b)))
P=np.array(pts)
print("n points", len(P), "r range", np.abs(P).min(), np.abs(P).max())
M=member(P,np.array(IA,dtype=float),np.array(IB,dtype=float))
print("member fraction", M.mean())
bad=np.argwhere(~M)[:5]
for i in bad:
    w=P[i[0]]
    print("missed:", w, " r=",abs(w))
