#!/usr/bin/env python3
"""Remove `open` commands that are provably redundant.

An `open`/`open scoped` command is deleted exactly when every name it opens is
already open at that point in the same scope stack.  Deleting such a command
leaves the set of opened names in force at every later token unchanged, so the
elaborated term is unchanged (Lean resolves names against the open set, and
`open` commands commute).  `open ... in`, `renaming`, `hiding` are untouched.

usage: redundant_open.py TREE_ROOT [TREE_ROOT2 ...]
"""
import os, re, sys

OPEN = re.compile(r'^open(\s+scoped)?\s+(.*)$')
SCOPE = re.compile(r'^(?:(?:noncomputable|private|protected|scoped)\s+)*section\b|^namespace\b')
END = re.compile(r'^end\b')


def inert(line):
    """A line that resolves no names: blank, comment, or an `open` command."""
    s = line.strip()
    return (s == '' or s.startswith('--') or s.startswith('/-') or s.startswith('-/')
            or OPEN.match(s) is not None)


def process(text):
    L = text.split('\n')
    stack = [set()]          # plain opened names, per scope
    sstack = [set()]         # scoped opened names, per scope
    out = []
    removed = []
    # last index in `out` of an open line of each kind, and whether everything
    # after it is inert (so a later open can be folded into it)
    last = {}               # (depth, scoped) -> index in out
    inert_since = {}        # (depth, scoped) -> bool
    for i, line in enumerate(L):
        s = line.strip()
        if END.match(s):
            if len(stack) > 1:
                stack.pop(); sstack.pop()
            last.clear(); inert_since.clear()
            out.append(line)
            continue
        m = OPEN.match(s)
        if m and not s.endswith(' in') and 'renaming' not in s and 'hiding' not in s:
            scoped = m.group(1) is not None
            names = m.group(2).split()
            cur = sstack if scoped else stack
            key = (len(stack), scoped)
            if all(n in cur[-1] for n in names):
                removed.append(i + 1)
                continue
            if key in last and inert_since.get(key, False):
                j = last[key]
                have = out[j].split()
                add = [n for n in names if n not in have]
                if add:
                    out[j] = out[j] + ' ' + ' '.join(add)
                cur[-1].update(names)
                removed.append(i + 1)
                continue
            cur[-1].update(names)
            last[key] = len(out)
            inert_since[key] = True
            out.append(line)
            continue
        if not inert(line):
            for k in list(inert_since):
                inert_since[k] = False
        out.append(line)
        if SCOPE.match(s):
            stack.append(set(stack[-1]))
            sstack.append(set(sstack[-1]))
            # a new scope invalidates every recorded position: sibling scopes
            # have the same key but are not the same scope
            last.clear()
            inert_since.clear()
    return '\n'.join(out), removed


def main():
    total = 0
    for root in sys.argv[1:]:
        for dp, dn, fn in os.walk(root):
            for f in sorted(fn):
                if not f.endswith('.lean'):
                    continue
                p = os.path.join(dp, f)
                t = open(p).read()
                new, rem = process(t)
                if rem:
                    open(p, 'w').write(new)
                    total += len(rem)
                    print(f'{len(rem):4d} {p}')
    print('total redundant open lines removed:', total)


main()
