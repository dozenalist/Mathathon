"""Characterise the satisfiable k=6 instances by their sliver profile."""
from itertools import product
from profile2 import sign_word, slivers, first_model

K=6
for ell in (5,6):
    tot=0; sat=0; nonempty=0; nonempty_sat=0; empty_unsat=0
    for c in product(range(6), repeat=ell):
        tot+=1
        sl=slivers(ell,K,sign_word(ell,c))
        ne=all(O and I for (O,I) in sl)
        m=first_model(ell,K,c,True) is not None
        sat+=m; nonempty+=ne
        if ne and m: nonempty_sat+=1
        if (not ne) and (not m): empty_unsat+=1
    print(f"l={ell}: total={tot} SAT={sat} all-slivers-nonempty={nonempty} "
          f"nonempty&SAT={nonempty_sat} empty&UNSAT={empty_unsat}")
    # how many satisfy 'every row has at least one both-neg and one both-pos'
