import sys, itertools
sys.path.insert(0,'work')
from fractions import Fraction as F
from gamma_crit import gamma_kill, width, intervals_mod120, PSI_LO, PSI_HI
from models import words, dirset

W = words()
def arcs(n, word, val):
    return [(F(int(lo)), F(int(hi))) for lo,hi in dirset(n,word,val)]

print("psi = pi + gamma = (%.6f, %.6f) deg;   psi mod 120 = (%.6f, %.6f)" % (
      float(PSI_LO), float(PSI_HI), float(PSI_LO%120), float(PSI_HI%120)))
print()
print("%-11s %-9s %-9s %3s %3s   %-7s  %s" % ("model","A","B","|A|","|B|","killed?","witness t mod 120 (deg)"))
for name in ["block_l3","block_l4","block_l5","block_l6","free_l3","free_l4","free_l5","free_l6","sing_l3"]:
    n,word = W[name]
    vals = sorted(set(word), key=lambda s:(len(s),sorted(s)))
    for A,B in itertools.combinations(vals,2):
        if A & B: continue
        EA=arcs(n,word,A); EB=arcs(n,word,B)
        h1,h2 = gamma_kill(EA,EB)
        u=len(A|B); Tp=6-u
        # a 3-chromatic witness is needed when T' <= 2 ; a unit edge (chi=2) when T' == 1
        need = 3 if Tp<=2 else (2 if Tp==1 else 5)
        killed = (width(h1)+width(h2))>0
        tag = "KILL" if (killed and (Tp<=2)) else ("edge-KILL" if (killed and Tp==1) else "survives")
        w = h1 if width(h1)>0 else h2
        print("%-11s %-9s %-9s %3d %3d   %-8s %s" % (name, sorted(A), sorted(B), len(A), len(B), tag,
              ("%.3f..%.3f (width %.3f)"%(float(w[0][0]),float(w[0][1]),float(width(w))) if killed else "")))
