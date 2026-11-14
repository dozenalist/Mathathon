import sys, itertools
sys.path.insert(0,'work')
from fractions import Fraction as F
from orbit_crit import criterion, width, widest, verify, in_set, norm
from models import words, dirset
W=words()
def arcs(n,word,val): return [(F(int(lo)),F(int(hi))) for lo,hi in dirset(n,word,val)]
from gamma_crit import PSI_LO, PSI_HI
print("psi in (%.9f, %.9f)"%(float(PSI_LO),float(PSI_HI)))
for name in ["block_l3","block_l4","block_l5","block_l6","free_l3","free_l4","free_l5","free_l6","sing_l3"]:
    n,word=W[name]; vals=sorted(set(word), key=lambda s:(len(s),sorted(s)))
    print("="*78); print(name, "periodic12:", all(word[i]==word[(i+12)%n] for i in range(n)))
    for A,B in itertools.combinations(vals,2):
        if A&B: continue
        EA=arcs(n,word,A); EB=arcs(n,word,B)
        w1,w2=criterion(EA,EB,PSI_LO,PSI_HI)
        u=len(A|B); Tp=6-u
        got=None
        for role,w in (('A->B',w1),('B->A',w2)):
            if width(w)>0:
                t=widest(w)[0] if widest(w) else None
                # try the midpoint of the widest piece
                lo,hi=widest(w); t=(lo+hi)/2
                ok=verify(EA,EB,t,PSI_LO,PSI_HI,role)
                if ok: got=(role,t,width(w),ok); break
        tag = ("KILL" if (got and Tp<3) else ("FIRE-noContra" if got else "silent"))
        print("  A=%-9s B=%-9s |AuB|=%d T'=%d  %-13s %s"%(sorted(A),sorted(B),u,Tp,tag,
              ("role %s t=%.6f deg width %.3f"%(got[0],float(got[1]),float(got[2]))) if got else ""))
