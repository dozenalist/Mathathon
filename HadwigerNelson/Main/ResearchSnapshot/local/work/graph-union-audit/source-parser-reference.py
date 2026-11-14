"""Independent exact validation of a published Heule 5-chromatic unit-distance graph.

Heule (arXiv:1805.12181) publishes, per graph, a .vtx file of Mathematica-style exact
coordinates and an .edge file.  His own checker (check_dist_one.py) rewrites these into
Singular input and reduces distance-polynomials modulo the ideal
(r3*Sqrt3-1, s11^2-11, s5^2-5, s3^2-3).  We do not run Singular: we parse the same
coordinates into our own exact field Q(sqrt3, sqrt5, sqrt11) and decide every pairwise
squared distance by an exact field identity, cross-checked at 60 decimal digits.
"""
import re
from fractions import Fraction as Fr

from .exact import Field


class Expr:
    """tokens: int, '+', '-', '*', '/', '(', ')', 'sqrt3','sqrt5','sqrt11',
    's11_3' = sqrt(11/3), 's165','s33','s15','s55'."""

    def __init__(self, s):
        self.toks = self._lex(s)
        self.i = 0

    @staticmethod
    def _lex(s):
        s = s.replace('Sqrt[11/3]', '\x01')      # sqrt(11/3)
        s = re.sub(r'Sqrt\[(\d+)\]', lambda m: '\x02' + m.group(1) + '\x03', s)
        out = []
        for piece in re.findall(r'\x01|\x02\d+\x03|[0-9]+|[-+*/()]', s):
            if piece == '\x01':
                out.append('s11_3')
            elif piece.startswith('\x02'):
                n = piece[1:-1]
                out.append({'3': 'sqrt3', '5': 'sqrt5', '11': 'sqrt11', '15': 's15',
                            '33': 's33', '55': 's55', '165': 's165'}[n])
            else:
                out.append(piece)
        return out

    def expr(self):
        v = self.term()
        while self.i < len(self.toks) and self.toks[self.i] in '+-':
            op = self.toks[self.i]; self.i += 1
            r = self.term()
            v = ('add', v, r) if op == '+' else ('sub', v, r)
        return v

    def term(self):
        v = self.unary()
        while self.i < len(self.toks) and self.toks[self.i] in '*/':
            op = self.toks[self.i]; self.i += 1
            r = self.unary()
            v = ('mul', v, r) if op == '*' else ('div', v, r)
        return v

    def unary(self):
        if self.i < len(self.toks) and self.toks[self.i] == '-':
            self.i += 1
            return ('neg', self.unary())
        if self.i < len(self.toks) and self.toks[self.i] == '+':
            self.i += 1
            return self.unary()
        return self.atom()

    def atom(self):
        t = self.toks[self.i]; self.i += 1
        if t == '(':
            v = self.expr()
            assert self.toks[self.i] == ')'
            self.i += 1
            return v
        if t.isdigit():
            return ('int', int(t))
        return ('sym', t)


def _clean(s):
    s = s.replace('**', '^')
    s = re.sub(r'\^(\d+)', lambda m: '^' + m.group(1), s)
    return s


def _eval(ast, F, cache):
    """Evaluate into Q(sqrt3,sqrt5,sqrt11). Division is by rationals only here, which we
    assert (the published coordinates divide only by integers)."""
    def rec(node):
        tag = node[0]
        if tag == 'int':
            return F.rat(node[1])
        if tag == 'sym':
            if node[1] in cache:
                return cache[node[1]]
            raise KeyError(node[1])
        if tag == 'neg':
            return F.neg(rec(node[1]))
        if tag == 'add':
            return F.add(rec(node[1]), rec(node[2]))
        if tag == 'sub':
            return F.sub(rec(node[1]), rec(node[2]))
        if tag == 'mul':
            return F.mul(rec(node[1]), rec(node[2]))
        if tag == 'div':
            return _div_rat(F, rec(node[1]), node[2])
        raise ValueError(tag)
    return rec(ast)


_INV3 = None


def _div_rat(F, num, den_node):
    """Divide by a monomial c*sqrt(3)^e.  Only den * sqrt(3)^e_fixed forms occur in the
    published data: integers, and integers times Sqrt[3].  Dividing by sqrt(3) is
    multiplication by sqrt(3)/3, which stays inside the basis (no inversion needed)."""
    global _INV3
    if den_node[0] == 'int':
        return tuple(c / Fr(den_node[1]) for c in num)
    if den_node[0] == 'sym' and den_node[1] == 'sqrt3':
        return F.mul(num, tuple(c / Fr(3) for c in F.sqrt(3)))     # 1/sqrt3 = sqrt3/3
    if den_node[0] == 'mul' and den_node[1][0] == 'int':
        # (c * X) in the denominator: 1/(c*X) = (1/c) * 1/X
        num = tuple(c / Fr(den_node[1][1]) for c in num)
        return _div_rat(F, num, den_node[2])
    raise AssertionError(f"unexpected denominator form {den_node}")


def load(path_vtx, F):
    txt = open(path_vtx).read().replace('\n', '')
    rows = re.findall(r'\{([^{}]*)\}', txt)
    pts = []
    cache = {
        'sqrt3': F.sqrt(3), 'sqrt5': F.sqrt(5), 'sqrt11': F.sqrt(11),
        's15': F.sqrt(15), 's33': F.sqrt(33), 's55': F.sqrt(55), 's165': F.sqrt(165),
        's11_3': F.mul(F.sqrt(11), F.sqrt(3)),  # sqrt(11/3) is NOT in the basis; handled below
    }
    # sqrt(11/3) = sqrt(33)/3 : replace before evaluation
    cache['s11_3'] = tuple(c / Fr(3) for c in F.sqrt(33))
    for row in rows:
        parts = _split_top(row)
        assert len(parts) == 2, row
        c = []
        for p in parts:
            e = Expr(p)
            ast = e.expr()
            assert e.i == len(e.toks), (p, e.toks, e.i)
            c.append(_eval(ast, F, cache))
        pts.append(tuple(c))
    return pts


def _split_top(row):
    depth = 0
    for i, ch in enumerate(row):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == ',' and depth == 0:
            return [row[:i], row[i + 1:]]
    return [row]


def load_edges(path_edg):
    lines = [l.split() for l in open(path_edg) if l.strip()]
    assert lines[0][0] == 'p', lines[0]
    m = int(lines[0][3])
    es = [(int(a[1]) - 1, int(a[2]) - 1) for a in lines[1:]]
    assert len(es) == m, (len(es), m)
    return es
