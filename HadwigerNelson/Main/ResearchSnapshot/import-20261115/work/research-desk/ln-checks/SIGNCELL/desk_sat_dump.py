"""Helper (written for the SIGNCELL recount): run the TRUSTED desk model
research-desk/census/independent_census.py via runpy (no import, no .pyc written)
and dump its 177 SAT classes (tau with tau_0 = 0) to desk_sat177.txt next to this file.
Run with:  python -B -P -E desk_sat_dump.py   (numpy needed by the desk file)
"""
import os, sys, runpy
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DESK = os.path.normpath(os.path.join(HERE, '..', '..', 'census', 'independent_census.py'))
g = runpy.run_path(DESK, run_name='desk_independent_census')
SAT, decode = g['SAT'], g['decode']
rows = [decode(c) for c in range(len(SAT)) if bool(SAT[c])]
with open(os.path.join(HERE, 'desk_sat177.txt'), 'w') as f:
    for t in rows:
        f.write(' '.join(str(int(x)) for x in t) + '\n')
print('[desk dump] wrote', len(rows), 'SAT classes from', DESK)
