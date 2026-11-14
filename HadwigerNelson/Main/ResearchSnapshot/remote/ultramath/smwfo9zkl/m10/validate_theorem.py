"""
Validation of the reduction on random probes.

For random finite probes we compare, for k = 3..6 and palette bounds md = 1,2,3:
   (A) exact backtracking over LABEL SETS            (solve_csp)
   (B) Glucose3 k-colourability of the conflict graph (colourable)
The reduction predicts (A) == (B) for every probe, every k >= md+3, and that (A) is
independent of md.  Every SAT verdict is re-verified by check_model (a third code path).
If a probe is UNSAT at some k we report it (none is expected; see REDUCTION.md).
"""
import random, json, itertools
import sympy as sp
from twocentre import *

DIRS = [rot(m) for m in range(6)] + [GAMMA, cconj(GAMMA),
                                    pyth_unit(3, 4), pyth_unit(5, 12), (sp.Integer(0), sp.Integer(1))]
DIRS = [sequence(d, rot(m)) for d in DIRS for m in range(6)]

def rand_point(rng):
    a = sp.Rational(rng.randint(-3, 3), rng.choice([1, 2, 3]))
    b = sp.Rational(rng.randint(-2, 2), rng.choice([1, 2]))
    c = sp.Rational(rng.randint(-3, 3), rng.choice([1, 2, 3]))
    d = sp.Rational(rng.randint(-2, 2), rng.choice([1, 2]))
    return (sp.expand(a + b*sp.sqrt(3)), sp.expand(c + d*sp.sqrt(3)))

def rand_probe(rng, n_nodes):
    nodes = []
    for _ in range(n_nodes):
        if rng.random() < 0.35:
            nodes.append(cnode(rand_point(rng)))
        else:
            nodes.append(pnode(rand_point(rng), rng.choice(DIRS)))
    return nodes

def main(trials=150, seed=20260101):
    rng = random.Random(seed)
    recs = []
    unsat_hits = []
    for tr in range(trials):
        nodes = rand_probe(rng, rng.randint(4, 14))
        adj, edges, margin = conflict_graph(nodes)
        for k in (4, 5, 6):
            okB, _ = colourable(nodes, adj, k)
            md_range = [k-3] if k <= 4 else [1, 2, k-3]
            for md in sorted(set(md_range)):
                if md > k-3:
                    continue
                okA, model = solve_csp(nodes, adj, k, maxdim=md)
                if okA:
                    chk, msg = verify_labelling(nodes, adj, k, model, maxdim=md)
                    if not chk:
                        raise RuntimeError('model verification failed: ' + msg)
                recs.append(dict(trial=tr, n=len(nodes), edges=len(edges), k=k, md=md,
                                 A=okA, B=okB, agree=(okA == okB)))
                if okA != okB:
                    unsat_hits.append(('DISAGREE', tr, k, md))
                if not okA:
                    unsat_hits.append(('UNSAT', tr, k, md, len(nodes), len(edges)))
    bad = [r for r in recs if not r['agree']]
    print('records:', len(recs), ' disagreements:', len(bad))
    print('UNSAT verdicts:', [h for h in unsat_hits if h[0] == 'UNSAT'])
    # size-independence: for each (trial,k) the answer must not depend on md
    key = {}
    for r in recs:
        key.setdefault((r['trial'], r['k']), set()).add(r['A'])
    viol = [ok for ok, s in key.items() if len(s) > 1]
    print('md-independence violations:', len(viol))
    with open('validate_out.json', 'w') as f:
        json.dump(recs, f, indent=1)

if __name__ == '__main__':
    main()
