"""Minimal exact counterexamples to the frozen Main and X sign helpers.

This diagnoses generic predicates, not the validity of either stored K33 vector.
Pass an immutable copied KeplerConjecture tree as argv[1].
"""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import sympy as sp

root = Path(sys.argv[1]).resolve()
main_path = root / 'Computation/shell_check.py'
spec = importlib.util.spec_from_file_location('frozen_shell_check', main_path)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

results = []
for label, got, value in [
    ('Main compact interval: u*(1-u) <= 0 on [0,1]',
     main.le_on_interval([0, 1, -1], 0, 0, 1), sp.Rational(1, 4)),
    ('Main half-line: u*(u-1) >= 0 on [0,infinity)',
     main.nonneg_on_half_line([0, -1, 1]), -sp.Rational(1, 4)),
    ('Main ray: u*(1-u) <= 0 on [0,infinity)',
     main._ray([0, 1, -1], 0), sp.Rational(1, 4)),
]:
    results.append(dict(test=label, claimed_accept=bool(got),
                        correct_accept=False, witness_argument='1/2',
                        witness_value=str(value)))

# Load only the two reviewed pure functions, without running the audit's
# top-level long computation or its writes to audit_numbers.json.
x_path = root / 'Counterexamples/Reviews/K33/audit_K33_signs.py'
tree = ast.parse(x_path.read_text(encoding='utf-8-sig'))
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name in {'multiplicity_at', 'half_line_verdict'}]
assert len(functions) == 2
t = sp.Symbol('t')
ns = {'sp': sp, 't': t}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(x_path), 'exec'), ns)
poly = sp.Poly((t*t-2)*(t*t-3), t)
got = ns['half_line_verdict'](poly, sp.Integer(0), 1)
results.append(dict(test='X: (t^2-2)*(t^2-3) >= 0 on [0,infinity)',
                    claimed_accept=bool(got[0]), correct_accept=False,
                    witness_argument='3/2', witness_value=str(poly.eval(sp.Rational(3,2))),
                    ignored_irrational_roots=['sqrt(2)', 'sqrt(3)']))
print(json.dumps(dict(
    scope='Generic sign-checker failures; not a refutation of stored K33 coefficients',
    source_sha256={str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in [main_path, x_path]}, results=results), indent=2))
assert all(r['claimed_accept'] for r in results), 'Frozen failure changed: inspect source/version'
assert poly.eval(sp.Rational(3, 2)) == -sp.Rational(3, 16)
