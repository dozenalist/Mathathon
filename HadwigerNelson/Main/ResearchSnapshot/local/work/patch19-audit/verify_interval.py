"""Check the interval table with the previously reviewed exact geometry checker.

Run from work/quotient16-audit so its original certificate is also rechecked.
This does not run a SAT solver or verify a RUP proof.
"""
from pathlib import Path
from fractions import Fraction
import json
import re

root = Path(__file__).resolve().parent
source = (root.parent / 'quotient16-audit' / 'verify_quotient16.py').read_text()
assert source.count('sys.exit(1 if fails else 0)') == 1
env = {}
exec(compile(source.replace('sys.exit(1 if fails else 0)', 'assert not fails'),
             'reviewed_quotient_checker', 'exec'), env)
cert = json.loads((root / 'interval_cert.json').read_text())
rows = cert['per_offset_at_a_eq_1']
assert len(rows) == 42
assert {tuple(row['v']) for row in rows} == env['FS']
def parse_q3(value):
    match = re.fullmatch(r'\(([^)]+)\)\+\(([^)]+)\)r3', value)
    assert match, value
    return env['Q3'](Fraction(match[1]), Fraction(match[2]))
min_max, max_min = [], []
for row in rows:
    lower, upper = env['rng2'](*row['v'])
    mu2, nu2 = lower * 25, upper * 25
    assert mu2 == parse_q3(row['mu2']) and nu2 == parse_q3(row['nu2']), row
    assert row['N'] == env['Norm'](*row['v'])
    assert mu2 <= 19 and nu2 >= 28
    min_max.append(nu2)
    max_min.append(mu2)
assert min(min_max) == 28 and max(max_min) == 19
assert Fraction(19, 100)**2 > Fraction(1, 28)
assert Fraction(11, 50)**2 < Fraction(1, 19)
result = {'offsets_checked': 42, 'failures': 0,
          'exact_interval': '(1/sqrt(28), 1/sqrt(19))',
          'rational_closed_subinterval': '[19/100, 11/50]',
          'scope': 'Exact distance table and homothety margins; UNSAT supplied by separately verified certificate.'}
(root / 'local-interval-check.json').write_text(json.dumps(result, indent=2) + '\n')
print('INTERVAL CERTIFICATE VALID: all 42 offsets and exact margins')
