#!/usr/bin/env python3
"""Tiny exact check: transitive import closure from a module's import lines.

Reads only `import OAI...` headers of .lean files under lean/OAI/Geometry/PlaneColoring/
and resolves a module name M to file <last component>.lean (all packet modules live in
that one directory).  Prints the closure, then answers membership questions.
"""
import os
import sys

ROOT = 'lean/OAI/Geometry/PlaneColoring'
LEAN_ROOT = 'lean'


def imports_of(path):
    out = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            s = line.strip()
            if s.startswith('import '):
                for tok in s[len('import '):].split():
                    if tok.startswith('OAI.'):
                        out.append(tok)
            elif s and not s.startswith(('/', '--', '-!')):
                break          # header is over
    return out


def closure(start_module):
    seen, stack, missing = [], [start_module], []
    order = {start_module: None}
    while stack:
        m = stack.pop()
        path = os.path.join(LEAN_ROOT, m.replace('.', '/') + '.lean')
        if not os.path.exists(path):
            missing.append(m)
            continue
        for dep in imports_of(path):
            if dep not in order:
                order[dep] = m
                stack.append(dep)
    return [m for m in order if m != start_module], missing, order


def main():
    start = sys.argv[1]
    probe = sys.argv[2].split(',')
    got, missing, order = closure(start)
    short = sorted(m.split('.')[-1] for m in got)
    print('closure(%s) = %d modules' % (start.split('.')[-1], len(short)))
    print('  ' + ' '.join(short))
    if missing:
        print('UNRESOLVED modules (not in %s): %s' % (ROOT, ' '.join(missing)))
    print('probes:')
    for p in probe:
        print('  %-22s %s' % (p, 'IN closure' if p in short else 'NOT in closure'))
    print('witness paths from %s:' % start.split('.')[-1])
    for p in probe:
        if p in short:
            chain, cur = [p], p
            while order.get(cur) is not None:
                cur = order[cur]
                chain.append(cur.split('.')[-1])
            print('  ' + p + ' <- ' + ' <- '.join(chain[1:]))


if __name__ == '__main__':
    main()
