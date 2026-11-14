"""Independent exact audit of the submitted K21 certificate, not a generator.

Run from any directory with SymPy 1.14.0 available. Writes evidence next to
this script unless --out is supplied. The candidate and checker are immutable
inputs from the source commit recorded below. No networking is performed.
"""
import argparse
import contextlib
from fractions import Fraction
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import time

import sympy as sp

HERE = Path(__file__).resolve().parent
COMP = HERE / 'source'
SOURCE_COMMIT = 'e681fbfddb8c5962333380c271d5f7a67f44a07b'


def load_module(path):
    spec = importlib.util.spec_from_file_location('submitted_exactcert', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arctan_bounds(q, n):
    s = sum((Fraction((-1)**k, (2*k+1)*q**(2*k+1)) for k in range(n)), Fraction(0))
    other = s + Fraction((-1)**n, (2*n+1)*q**(2*n+1))
    return min(s, other), max(s, other)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'audit.json'))
    args = ap.parse_args()
    started = time.monotonic()
    checker_path = COMP / 'exactcert.py'
    candidate_path = COMP / 'certificate_K21.json'
    ec = load_module(checker_path)
    candidate = json.loads(candidate_path.read_text(encoding='utf-8-sig'))
    rec = candidate['certificate']
    result = {
        'source_commit': SOURCE_COMMIT,
        'checker_sha256': hashlib.sha256(checker_path.read_bytes()).hexdigest(),
        'candidate_sha256': hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        'python': sys.version, 'sympy': sp.__version__,
        'submitted_ok': rec['ok'], 'submitted_reason': rec.get('reason'),
    }
    quiet = ec.certify_relaxed([2, -1], verbose=False)
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        loud = ec.certify_relaxed([2, -1], verbose=True)
    result['minimal_false_positive'] = {
        'laguerre_coefficients': ['2', '-1'],
        'p': 't + 1/2', 'q': '7/2 - t',
        'quiet_ok': quiet['ok'], 'verbose_ok': loud['ok'],
        'quiet_beats_kepler': quiet.get('beats_kepler'),
        'p_at_26': '53/2 > 0, violates exterior sign',
        'q_at_4': '-1/2 < 0, violates Fourier sign',
        'verbose_output': stream.getvalue(),
    }
    odd = ec.yun_odd_part([Fraction(-1), Fraction(-1)])
    result['lost_leading_sign'] = {
        'input': '-t-1', 'returned_odd_part': [str(x) for x in odd],
        'input_at_0': -1, 'odd_part_at_0': str(ec.peval(odd, Fraction(0))),
    }

    # Rebuild using a separate library's exact Laguerre recurrence; do not trust
    # either the checker polynomial arithmetic or the JSON's p/q fields.
    t = sp.Symbol('t')
    cs = [sp.Rational(x) for x in rec['c']]
    p = sp.Poly(sum(c*sp.assoc_laguerre(k, sp.Rational(1,2), t) for k,c in enumerate(cs)), t, domain=sp.QQ)
    q = sp.Poly(sum((-1)**k*c*sp.assoc_laguerre(k, sp.Rational(1,2), t) for k,c in enumerate(cs)), t, domain=sp.QQ)
    stored_p = sp.Poly(sum(sp.Rational(v)*t**i for i,v in enumerate(rec['p'])), t, domain=sp.QQ)
    stored_q = sp.Poly(sum(sp.Rational(v)*t**i for i,v in enumerate(rec['q'])), t, domain=sp.QQ)
    result['stored_polynomials_match_independent_reconstruction'] = p == stored_p and q == stored_q
    result['positive_q_roots_exact'] = int(q.count_roots(0, sp.oo))
    result['q_squarefree'] = q.gcd(q.diff()).degree() == 0
    intervals = q.intervals(eps=sp.Rational(1,10**6))
    positive = [(a,b,m) for (a,b),m in intervals if a > 0]
    witness = None
    for (_,b,_), (a,_,_) in zip(positive, positive[1:]):
        x = (a+b)/2
        value = q.eval(x)
        if value < 0:
            witness = {'t':str(x), 'q_at_t':str(value), 'q_at_t_decimal':str(sp.N(value,16))}
            break
    result['exact_negative_q_witness'] = witness
    result['certificate_valid'] = False if witness else None
    result['reason'] = 'An exact rational negative Fourier-polynomial value refutes the stored certificate.' if witness else 'No witness found; audit incomplete.'

    # Independent rational enclosure. Machin's identity follows from tan(4 atan
    # (1/5))=120/119 and tan(4 atan(1/5)-atan(1/239))=1, with the angle in (0,pi/2).
    a0,a1 = arctan_bounds(5,40)
    b0,b1 = arctan_bounds(239,12)
    pi_lo,pi_hi = 16*a0-4*b1, 16*a1-4*b0
    result['pi_check'] = {
        'machin_lower':str(pi_lo), 'machin_upper':str(pi_hi),
        'submitted_lower_strictly_below_proved_lower': ec.PI_LO < pi_lo,
        'submitted_upper_strictly_above_proved_upper': ec.PI_HI > pi_hi,
    }
    result['elapsed_seconds'] = round(time.monotonic()-started,3)
    Path(args.out).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['minimal_false_positive','positive_q_roots_exact','q_squarefree','certificate_valid','reason','elapsed_seconds']}, indent=2))
    if not (quiet['ok'] and not loud['ok'] and witness and result['stored_polynomials_match_independent_reconstruction']):
        raise SystemExit('Expected independent rejection was not established.')


if __name__ == '__main__':
    main()
