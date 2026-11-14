import sys,time
R='/workspace/nucleus/work/projects/p-9021becf3f0d47a89b3f3c794c1e872b/repo/RogersRamanujan/Computation'
sys.path.insert(0,R)
import bz82
def fam(r,s): return tuple([4]*r+[1]*s)
t0=time.time()
fails=[]
mx=0
for s in range(7,403,5):
    b,tr=bz82.pi_forward(fam(2,s)); mx=max(mx,len(tr))
    if b!=(s-1,6,3): fails.append((s,8+s,len(tr),b))
print("r=2 s=2mod5 range 7..402: fails",len(fails),"maxL",mx)
for f in fails[:12]: print("   ",f)
fails=[];mx=0
for s in range(27,203,5):
    b,tr=bz82.pi_forward(fam(3,s)); mx=max(mx,len(tr))
    if b!=(s+2,7,3): fails.append((s,12+s,len(tr),b))
print("r=3 s=2mod5 range 27..202: fails",len(fails),"maxL",mx)
for f in fails[:12]: print("   ",f)
print("t=%.1f"%(time.time()-t0))
