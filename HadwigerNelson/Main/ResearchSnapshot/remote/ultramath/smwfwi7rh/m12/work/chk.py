import numpy as np, sys
sys.path.insert(0,'work')
from fractions import Fraction as F
EA=[(0,10),(30,40),(120,130),(140,150),(250,270),(280,290)]
EB=[(90,110),(180,190),(210,230),(300,310),(330,350)]
def brute(w, EA, EB, step=0.02):
    best=(9e9,None)
    for lo,hi in EA:
        for a in np.arange(lo,hi,step):
            for lo2,hi2 in EB:
                for b in np.arange(lo2,hi2,step):
                    z=np.exp(1j*np.radians(a))+np.exp(1j*np.radians(b))
                    d=abs(z-w)
                    if d<best[0]: best=(d,(a,b,z))
    return best
for w in [0.26-0.14j, 0.25-0.14j, 1.26-0.14j, 0.76+0.726j, 0.75+0.866*0.99j]:
    d,(a,b,z)=brute(w,EA,EB,step=0.05)
    print("w=",w,"closest sum point:",np.round(z,4),"dist %.4f"%d,"angles",a,b)
# also: what is the actual unit triangle? search over the sum points for unit triangles
pts=[]
for lo,hi in EA:
    for a in np.arange(lo,hi,0.25):
        for lo2,hi2 in EB:
            for b in np.arange(lo2,hi2,0.25):
                pts.append(np.exp(1j*np.radians(a))+np.exp(1j*np.radians(b)))
pts=np.array(sorted(set(np.round(pts,6).tolist())))
print("cloud size",len(pts))
from scipy.spatial import cKDTree
tree=cKDTree(np.c_[pts.real,pts.imag])
pairs=tree.query_pairs(1.01,output_type='ndarray')
d=pts[pairs[:,1]]-pts[pairs[:,0]]
print("near-unit pairs:",(np.abs(np.abs(d)-1)<0.005).sum())
found=False
for (i,j),dv in zip(pairs,d):
    if abs(abs(dv)-1)>0.005: continue
    for s in (1,-1):
        w=pts[i]+dv*np.exp(1j*s*np.pi/3)
        dd,ii=tree.query([w.real,w.imag],k=1)
        if dd<0.005:
            print("TRIANGLE in cloud:", np.round([pts[i],pts[j],pts[ii]],4),"third-dist %.4f"%dd); found=True; break
    if found: break
print("done",found)
