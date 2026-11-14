#!/usr/bin/env python3
"""Audit a code-*moving* patch for statement fidelity at the text level.

For every added line, is it matched by a deleted line of the same content?  For every deleted
line, does it reappear among the added lines?  A patch that only moves blocks scores 0 unmatched
on both sides except for import/namespace/section boilerplate.

Usage: python3 move_audit.py <patch>
Reproduces the numbers quoted in NOTES.md section 5.
"""
import sys, collections

def main(patch):
    lines = open(patch, encoding='utf-8').read().split('\n')
    adds = [l[1:].strip() for l in lines if l.startswith('+') and not l.startswith('+++')]
    dels = [l[1:].strip() for l in lines if l.startswith('-') and not l.startswith('---')]
    ca = collections.Counter(l for l in adds if l)
    cd = collections.Counter(l for l in dels if l)
    new = [(k, v) for k, v in ca.items() if cd[k] < v]
    gone = [(k, v) for k, v in cd.items() if ca[k] == 0]
    print(f'added content lines: {len(adds)}  deleted content lines: {len(dels)}')
    print(f'added lines with no matching deletion: {len(new)}')
    for k, v in new:
        print(f'  NEW ({v}x): {k[:110]}')
    print(f'deleted lines with no matching addition: {len(gone)}')
    for k, v in gone:
        print(f'  LOST ({v}x): {k[:110]}')
    return 0 if not gone else 1

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
