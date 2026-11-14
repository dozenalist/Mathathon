"""Classification: for which m does a free-label translation-invariant sector word exist?

k=6, C_6, free label 0, palettes of size 2 (pairs) / size 2 or 3.
Three independent determinations per m:
  build -- the explicit uniform word  A^2 B^2 D^(m-3) E^2 F^(m-3)  (period 2m), checked directly;
  dfs   -- exhaustive backtracking (complete);
  sat   -- CaDiCaL on the CNF (complete, different algorithm).
"""
import sys, time
sys.path.insert(0,'work')
from generic import *
from word import uniform_word, BY_NAME

def build(m):
    if m < 5: return None
    w=uniform_word(m)
    return None if check(6,6,0,w,m,(2,)) else w

def table(ms, sizes, label):
    print(f"--- k=6, C_6, free label 0, palette sizes {sizes}   ({label})")
    print(f"{'m':>4} {'n=6m':>5} {'explicit word':>14} {'exhaustive DFS':>15} {'CaDiCaL':>9} {'DFS nodes':>10}")
    for m in ms:
        b=build(m)   # the explicit word is pair-valued, hence lies in every domain
        ok_dfs,w_dfs,nodes=decide_dfs(6,6,0,sizes,m)
        ok_sat,w_sat=decide_sat(6,6,0,sizes,m)
        assert ok_dfs==ok_sat, (m, ok_dfs, ok_sat)
        if True:
            assert (b is not None)==ok_dfs, (m, b is not None, ok_dfs)
            bad = check(6,6,0,b,m,sizes) if b else []
            assert not bad, (m,bad)
        print(f"{m:>4} {6*m:>5} {('yes' if b else 'no'):>14} {('SAT' if ok_dfs else 'UNSAT'):>15} "
              f"{('SAT' if ok_sat else 'UNSAT'):>9} {nodes:>10}")

if __name__=='__main__':
    ms=[int(x) for x in sys.argv[1:]] or list(range(2,31))
    table(ms,(2,),'pairs only')
    print()
    table([m for m in ms if m<=10],(2,3),'pairs and triples')
