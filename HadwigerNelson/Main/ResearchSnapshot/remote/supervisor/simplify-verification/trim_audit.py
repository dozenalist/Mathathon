#!/usr/bin/env python3
"""Audit a deletion-only "trim" patch for statement fidelity.

Checks, all from the patch plus the two trees (no Lean):
  1. the patch is deletion-only (counts of '+'/'-' content lines);
  2. which declaration blocks it deletes (kind, name);
  3. no deleted name occurs anywhere in the trimmed tree (no dangling reference);
  4. the trimmed tree has the same module set as the pristine tree;
  5. no deleted line is an attribute line (nothing silently leaves a simp/instance set).

Usage: python3 trim_audit.py <patch> <pristine/OAI> <trimmed/OAI>
Reproduces the numbers quoted in NOTES.md section 4.
"""
import re, sys, collections, glob, os

DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe|scoped)\s+)*"
    r"(theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\s+"
    r"([A-Za-z_][A-Za-z0-9_'\u2080-\u209c]*[!?]?)")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_'\u2080-\u209c]*[!?]?")

def counts(root):
    c = collections.Counter()
    for p in glob.glob(os.path.join(root, '**', '*.lean'), recursive=True):
        c.update(TOK.findall(open(p, encoding='utf-8', errors='ignore').read()))
    return c

def modules(root):
    return sorted(os.path.relpath(p, root)
                  for p in glob.glob(os.path.join(root, '**', '*.lean'), recursive=True))

def main(patch, pristine, trimmed):
    lines = open(patch, encoding='utf-8').read().split('\n')
    adds = [l for l in lines if l.startswith('+') and not l.startswith('+++')]
    dels = [l for l in lines if l.startswith('-') and not l.startswith('---')]
    hunks = [l for l in lines if l.startswith('@@')]
    print(f'[1] added content lines: {len(adds)}   deleted content lines: {len(dels)}   hunks: {len(hunks)}')
    print(f'    deletion-only: {len(adds) == 0}')
    kinds = collections.Counter()
    names = []
    for l in dels:
        m = DECL.match(l[1:])
        if m:
            kinds[m.group(1)] += 1
            names.append(m.group(2))
    print(f'[2] deleted declaration blocks: {len(names)}  kinds: {dict(kinds)}')
    print(f'    deleted attribute lines: {sum(1 for l in dels if l[1:].lstrip().startswith("@["))}')
    ct, cp = counts(trimmed), counts(pristine)
    dangling = [n for n in names if ct[n] > 0]
    print(f'[3] deleted names still occurring in trimmed tree: {len(dangling)} {dangling[:8]}')
    multi = [(n, cp[n]) for n in names if cp[n] != 1]
    print(f'    deleted names with pristine count != 1 (removed in later rounds): {len(multi)}')
    same = modules(pristine) == modules(trimmed)
    print(f'[4] module sets equal: {same}  ({len(modules(trimmed))} files)')
    return 0 if (len(adds) == 0 and not dangling and same) else 1

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
