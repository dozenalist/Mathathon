#!/usr/bin/env python3
"""Delete redundant duplicate `open`/`open scoped` lines inside one lexical scope.

Two `open` commands in the same enclosing scope stack are additive, so all
duplicates after the first can be replaced by a single merged command at the
first position.  Lines with `in`, `renaming`, `hiding` are left untouched.
Prints nothing; rewrites files in place (argv[1] = tree root).
"""
import os, re, sys

KW = re.compile(r'^(section|namespace)\b')
END = re.compile(r'^end\b')
OPEN = re.compile(r'^open(\s+scoped)?\s+(.*)$')

def main():
    root = sys.argv[1]
    tot = 0
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith('.lean'):
                continue
            p = os.path.join(dp, f)
            L = open(p).read().split('\n')
            stack = []
            first = {}          # (keystack, scoped) -> index in out
            out = []
            for line in L:
                s = line.strip()
                if END.match(s):
                    if stack:
                        stack.pop()
                    out.append(line)
                    continue
                m = OPEN.match(s)
                if m and not s.endswith(' in') and 'renaming' not in s and 'hiding' not in s:
                    scoped = m.group(1) is not None
                    key = (tuple(stack), scoped)
                    names = m.group(2).split()
                    if key in first:
                        i = first[key]
                        cur = out[i].split()
                        add = [n for n in names if n not in cur]
                        out[i] = out[i] + (' ' + ' '.join(add) if add else '')
                    else:
                        first[key] = len(out)
                        out.append(line)
                    continue
                out.append(line)
                mm = KW.match(s)
                if mm:
                    parts = s.split()
                    stack.append(parts[1] if len(parts) > 1 else mm.group(1))
            if len(out) != len(L):
                open(p, 'w').write('\n'.join(out))
                tot += len(L) - len(out)
                print(f'{len(L)-len(out):4d} {p}')
    print('total removed', tot)

main()
