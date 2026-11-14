#!/usr/bin/env python3
"""Reconstruct page text from mutool stext XML, annotating baseline shifts and
font-size changes so that sub/superscripts and dropped fractions are visible.

Usage: render.py PGXML [pageno...]
Each char carries x, y (baseline) and its font size.  Chars are grouped into
lines by baseline; within a line, a char whose baseline sits more than 1.5pt
above the line baseline is wrapped in ^{}, more than 1.5pt below in _{}.
A horizontal gap larger than 1.2 * fontsize is printed as a visible space run.
"""
import sys, re, xml.etree.ElementTree as ET
from collections import defaultdict


def read_page(path):
    tree = ET.parse(path)
    root = tree.getroot()
    chars = []
    for line in root.iter('line'):
        for f in line.iter('font'):
            size = float(f.get('size'))
            for c in f.iter('char'):
                q = [float(v) for v in c.get('quad').split()]
                # quad: x0 y0(top) x1 y1 x2 y2(bottom) x3 y3
                ybase = float(c.get('y'))
                chars.append((ybase, q[0], q[2] - q[0], size, c.get('c')))
    return chars


def render(path, ytol=2.0, sizetol=0.35):
    chars = read_page(path)
    if not chars:
        return ''
    # group by baseline
    chars.sort(key=lambda t: (round(t[0], 1), t[1]))
    lines = []
    for ch in chars:
        if lines and abs(ch[0] - lines[-1][0][0]) <= ytol:
            lines[-1].append(ch)
        else:
            lines.append([ch])
    out = []
    for ln in lines:
        ln.sort(key=lambda t: t[1])
        base = max(set(round(t[0], 1) for t in ln),
                   key=lambda r: sum(1 for t in ln if round(t[0], 1) == r))
        domsize = max(set(round(t[3], 1) for t in ln),
                      key=lambda r: sum(1 for t in ln if round(t[3], 1) == r))
        s = []
        prev = None
        mode = None
        for (y, x, w, size, c) in ln:
            if prev is not None and x - prev > 1.1 * domsize:
                s.append(' ' * max(1, int(round((x - prev) / (0.45 * domsize)))))
                if mode:
                    s.append('}' if mode else '}')
                    s[-1] = '}' if mode == 'sup' else '}'
                    mode = None
            newmode = None
            if size < domsize - sizetol:
                newmode = 'sup' if y < base - 1.0 else ('sub' if y > base + 1.0 else None)
            if newmode != mode:
                if mode:
                    s.append('}')
                if newmode:
                    s.append('^{' if newmode == 'sup' else '_{')
                mode = newmode
            s.append(c)
            prev = x + w
        if mode:
            s.append('}')
        out.append(''.join(s))
    return '\n'.join(out)


if __name__ == '__main__':
    base = sys.argv[1]
    pages = sys.argv[2:]
    for p in pages:
        print('=' * 20, 'page', p, '=' * 20)
        print(render(base % int(p)))
