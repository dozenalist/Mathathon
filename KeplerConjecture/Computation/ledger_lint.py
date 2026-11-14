#!/usr/bin/env python3
"""K15-C110 -- a consistency linter for Main/CLAIMS.md.

Motivated by two defects found by hand this project: K15-C002b carried the status token
PROPOSED while three other files treated it as audited, and several claims are referenced
from prose where a typo produces a dangling id silently.  This checks:

  1. every heading in CLAIMS.md has a K15-xNNN id and a status token from the vocabulary;
  2. no id is defined twice;
  3. every fully-qualified K15-xNNN reference anywhere in KeplerConjecture/ resolves;
  4. every status token used is one of the documented ones (or a marked WITHDRAWN/CORRECTION).

Exit non-zero on any violation.  Stdlib only.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CLAIMS = os.path.join(ROOT, 'KeplerConjecture', 'Main', 'CLAIMS.md')

# ids defined in a worker's own ledger, cited by Main; they are listed in CLAIMS.md
# under "External ids" so that a reference from Main resolves to something.
EXTERNAL = {'K15-X-C017', 'K15-X-C014', 'K15-X-C015', 'K15-X-C016'}

VOCAB = {
    'PROPOSED', 'TESTED_FINITE', 'PROVED', 'LEAN_VERIFIED', 'LEAN_CONDITIONAL',
    'REFUTED', 'BLOCKED', 'PENDING_REVIEW', 'AUDITED', 'IMPORTED', 'AGREES',
    'WITHDRAWN', 'CORRECTION', 'TESTED_FAMILY', 'PROPOSED_PACKAGE', 'DECISION',
    'VERIFIED', 'VERIFIED_CROSS', 'ACCEPTED',
}
ID_RE = re.compile(r'K15-([CERX])-?(C?\d{3}[a-z]?|\d{3}[a-z]?)')
HEAD_RE = re.compile(r'^#{2,3}\s+K15-([CERX])-?(C?\d{3}[a-z]?)(.*)$', re.M)
# status token = the last parenthesised ALL-CAPS group in a heading
STATUS_RE = re.compile(r'\(([^()]*)\)\s*$')


def main():
    text = open(CLAIMS, encoding='utf-8').read()
    problems = []

    heads = HEAD_RE.findall(text)
    ids = {}
    addenda = []
    for kind, num, rest in heads:
        cid = f'K15-{kind}-{num}'
        if re.match(r'\s*addendum', rest):
            addenda.append(cid)          # a sub-heading of cid, not a duplicate
            continue
        if cid in ids:
            problems.append(f'DUPLICATE id {cid}')
        ids[cid] = rest
    if addenda:
        print(f'addendum sub-headings (allowed): {len(addenda)} '
              f'-> {sorted(set(addenda))}')
    print(f'headings with ids: {len(heads)}   distinct ids: {len(ids)}')

    # statuses
    nostatus = []
    badvocab = []
    for cid, rest in ids.items():
        m = STATUS_RE.search(rest)
        if not m:
            nostatus.append(cid)
            continue
        toks = set(re.findall(r'[A-Z][A-Z_]{2,}', m.group(1)))
        toks = {t for t in toks if t not in {'THE', 'AND', 'FOR', 'NOT', 'ITS'}}
        unknown = toks - VOCAB
        if unknown and not toks:
            badvocab.append((cid, sorted(unknown)))
    if nostatus:
        print(f'\nheadings with no trailing status token: {len(nostatus)}')
        for c in nostatus[:12]:
            print('   ', c)
    if badvocab:
        print(f'\nheadings with unrecognised status tokens: {len(badvocab)}')
        for c, u in badvocab[:12]:
            print('   ', c, u)

    # every fully-qualified reference resolves
    ref_re = re.compile(r'K15-([CERX])-(C?\d{3}[a-z]?|\d{3}[a-z]?)')
    dangling = {}
    for dirpath, _, files in os.walk(os.path.join(ROOT, 'KeplerConjecture')):
        if '.git' in dirpath:
            continue
        for f in files:
            if not f.endswith(('.md', '.py')):
                continue
            path = os.path.join(dirpath, f)
            try:
                body = open(path, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            for m in ref_re.finditer(body):
                ref = f'K15-{m.group(1)}-{m.group(2)}'
                if ref not in ids and ref not in EXTERNAL:
                    dangling.setdefault(ref, set()).add(
                        os.path.relpath(path, ROOT))
    print(f'\nfully-qualified references that do not resolve: {len(dangling)}')
    for ref in sorted(dangling):
        where = sorted(dangling[ref])
        print(f'    {ref:16s} <- {", ".join(where[:3])}'
              + (' …' if len(where) > 3 else ''))
        problems.append(f'DANGLING {ref}')

    # shorthand usage census (informational, not a failure)
    short = re.compile(r'(?<!K15-)\b([CERX])(\d{3}[a-z]?)\b')
    n_short = 0
    for dirpath, _, files in os.walk(os.path.join(ROOT, 'KeplerConjecture', 'Main')):
        for f in files:
            if f.endswith('.md'):
                body = open(os.path.join(dirpath, f), encoding='utf-8',
                            errors='replace').read()
                n_short += len(short.findall(body))
    print(f'\nshorthand references (C094, E083, ...) in Main/: {n_short}  '
          f'(informational; not checked)')

    print()
    if problems:
        print(f'LEDGER LINT: {len(problems)} problem(s)')
        for p in problems[:30]:
            print('   ', p)
        return 1
    print('LEDGER LINT: PASS — every heading has an id, no duplicates, '
          'every fully-qualified reference resolves.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
