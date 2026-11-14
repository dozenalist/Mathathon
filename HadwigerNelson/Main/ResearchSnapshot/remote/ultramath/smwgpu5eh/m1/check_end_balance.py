#!/usr/bin/env python3
"""Tiny exact check: section/namespace/end balance for Lean files.

Strips -- line comments, nested /- -/ block comments and string literals,
then walks the remaining tokens tracking a scope stack.  Mirrors the shape of
Lean 4's elabEnd (Lean/Elab/BuiltinCommand.lean:241-266): an `end X` must name
the innermost open scope (or a dotted suffix of it).
"""
import sys


def strip(src):
    out = []
    i, n = 0, len(src)
    depth = 0
    while i < n:
        c = src[i]
        if depth > 0:
            if src.startswith('/-', i):
                depth += 1
                i += 2
            elif src.startswith('-/', i):
                depth -= 1
                i += 2
            else:
                if c == '\n':
                    out.append('\n')
                i += 1
            continue
        if src.startswith('/-', i):
            depth += 1
            i += 2
            continue
        if src.startswith('--', i):
            while i < n and src[i] != '\n':
                i += 1
            continue
        if c == '"':
            i += 1
            while i < n and src[i] != '"':
                i += 2 if src[i] == '\\' else 1
            i += 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def main(paths):
    for path in paths:
        src = open(path, encoding='utf-8').read()
        clean = strip(src)
        stack = []          # (kind, name, line)
        problems = []
        for lineno, line in enumerate(clean.split('\n'), 1):
            toks = line.split()
            if not toks:
                continue
            head = toks[0]
            if head == 'section' or (toks[-1] == 'section'):
                stack.append(('section', toks[1] if (head == 'section' and len(toks) > 1) else '', lineno))
            elif head == 'namespace':
                stack.append(('namespace', toks[1], lineno))
            elif head == 'end':
                want = toks[1] if len(toks) > 1 else None
                if not stack:
                    problems.append((lineno, 'end with empty stack'))
                    continue
                kind, name, oline = stack[-1]
                if want is None:
                    if name:
                        problems.append(
                            (lineno, "end without name closes named %s '%s' (opened line %d)"
                             % (kind, name, oline)))
                elif name != want:
                    problems.append(
                        (lineno, "end %s but innermost scope is %s '%s' (opened line %d)"
                         % (want, kind, name or '<anonymous>', oline)))
                stack.pop()
        for kind, name, oline in stack:
            problems.append((oline, "unclosed %s '%s'" % (kind, name)))
        status = 'OK' if not problems else 'PROBLEM'
        print('%-32s %s' % (path.split('/')[-1], status))
        for lineno, msg in problems:
            print('   line %d: %s' % (lineno, msg))


if __name__ == '__main__':
    main(sys.argv[1:])
