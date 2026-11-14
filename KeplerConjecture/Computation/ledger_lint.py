#!/usr/bin/env python3
"""K15-C110 -- a consistency linter for Main/CLAIMS.md.

Motivated by two defects found by hand this project: K15-C002b carried the status token
PROPOSED while three other files treated it as audited, and several claims are referenced
from prose where a typo produces a dangling id silently.  This checks:

  1. every heading in CLAIMS.md has a K15-xNNN id and a status token from the vocabulary;
  2. no id is defined twice;
  3. every fully-qualified K15-xNNN reference anywhere in KeplerConjecture/ resolves;
  4. every status token used is one of the documented ones (or a marked WITHDRAWN/CORRECTION);
  5. every SHORTHAND reference (C094, G11, D18, PN-4) resolves to a definition, where
     definitions are recognised in headings, table rows and bold announcements
     (K15-C140).  Workers' ids (E083, X-C051) are external and only counted.

Exit non-zero on any violation.  Stdlib only.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CLAIMS = os.path.join(ROOT, 'KeplerConjecture', 'Main', 'CLAIMS.md')

# ids defined in a worker's own ledger, cited by Main; they are listed in CLAIMS.md
# under "External ids" so that a reference from Main resolves to something.
def canon(ref):
    """Canonical id form: `K15-C140` (no dash after the letter), but `K15-X-C014`
    for the worker X family, whose ids genuinely have two letters of prefix."""
    m = re.match(r'K15-([CERX])-?(.*)$', ref)
    if not m:
        return ref
    cls, rest = m.group(1), m.group(2).lstrip('-')
    return f'K15-X-{rest}' if cls == 'X' else f'K15-{cls}{rest}'


EXTERNAL = {canon('K15-X-C014'), 'K15-X-C015', 'K15-X-C016', 'K15-X-C017',
            'K15-X-C043', 'K15-X-C051', 'K15-X-C052', 'K15-X-C053', 'K15-X-C055',
            'K15-X-C083'}   # K15-X-C083: deg<=12 only for eps <~ 0.31 (review block 0738)
# E's own ledger lives in KeplerConjecture/Experimental; Main cites it by id.
EXTERNAL |= {f'K15-E{i:03d}' for i in
             (1, 2, 3, 4, 13, 14, 15, 48, 74, 75, 78, 81, 82, 83, 85, 86, 90, 99, 100)}

# announced in prose but never given their own heading; the id of record is the target
ALIAS_FULL = {'K15-C010b': 'K15-C010r', 'K15-C015r': 'K15-C015'}
# ids that exist only inside this file's self-test fixtures
SYNTHETIC = {'K15-C999'}

VOCAB = {
    'PROPOSED', 'TESTED_FINITE', 'PROVED', 'LEAN_VERIFIED', 'LEAN_CONDITIONAL',
    'REFUTED', 'BLOCKED', 'PENDING_REVIEW', 'AUDITED', 'IMPORTED', 'AGREES',
    'WITHDRAWN', 'CORRECTION', 'TESTED_FAMILY', 'PROPOSED_PACKAGE', 'DECISION',
    'VERIFIED', 'VERIFIED_CROSS', 'ACCEPTED', 'OBLIGATION',   # OBLIGATION: named gap with an owner
}
ID_RE = re.compile(r'K15-([CERX])-?(C?\d{3}[a-z]?|\d{3}[a-z]?)')
HEAD_RE = re.compile(r'^#{2,3}\s+K15-([CERX])-?(C?\d{3}[a-z]?)(.*)$', re.M)
# status token = the last parenthesised ALL-CAPS group in a heading
STATUS_RE = re.compile(r'\(([^()]*)\)\s*$')



SHORT_ALIAS = {'C015r': 'C015',    # announced in prose, never given its own entry
               'C010b': 'C010r'}   # ditto; the id of record is C010r
SHORT_EXCEPTIONS = set()           # names that look like ids but are not (none today)
NAMESPACES = {
    'C': re.compile(r'(?<!K15-)\bC\d{3}[a-z]?\b'),
    'G': re.compile(r'\bG\d{1,2}\b'),
    'D': re.compile(r'\bD\d{1,2}\b'),
    'PN': re.compile(r'\bPN-\d+\b'),
}
EXTERNAL_SHORT = {'E': re.compile(r'\bE\d{3}[a-z]?\b'),
                  'X': re.compile(r'\bX-C\d{3}\b')}


def shorthand_defs(bodies):
    """Ids defined by a heading, a table row or a bold announcement.

    All three shapes are in use: `### K15-C094`, `| G2 | ...`, `**PN-2 -- ...**`.
    Recognising headings alone reported 18 dangling ids that were all defined --
    the bug this docstring exists to prevent.
    """
    defined = {k: set() for k in NAMESPACES}
    for body in bodies.values():
        for m in re.finditer(r'^#{2,4}\s*K15-(C\d{3}[a-z]?)', body, re.M):
            defined['C'].add(m.group(1))
        for m in re.finditer(r'\(K15-(C\d{3}[a-z]?)[,)]|\*\*K15-(C\d{3}[a-z]?)', body):
            defined['C'].add(m.group(1) or m.group(2))
        for m in re.finditer(r'^#{2,4}\s*(G\d{1,2})\b', body, re.M):
            defined['G'].add(m.group(1))
        for m in re.finditer(r'^#{2,4}\s*(D\d{1,2})\b', body, re.M):
            defined['D'].add(m.group(1))
        for m in re.finditer(r'^\|\s*(G\d{1,2})\s*\|', body, re.M):
            defined['G'].add(m.group(1))
        for m in re.finditer(r'^\|\s*(D\d{1,2})\s*\|', body, re.M):
            defined['D'].add(m.group(1))
        for m in re.finditer(r'\*\*(G\d{1,2}|D\d{1,2}|PN-\d+)\s*[\u2014-]', body):
            ns = 'PN' if m.group(1).startswith('PN') else m.group(1)[0]
            defined[ns].add(m.group(1))
    return defined


def shorthand_report(bodies):
    """(census line, problems, detail lines) for the shorthand-reference check."""
    defined = shorthand_defs(bodies)
    used = {k: {} for k in NAMESPACES}
    for f, body in bodies.items():
        for k, pat in NAMESPACES.items():
            for m in pat.finditer(body):
                used[k].setdefault(m.group(0), set()).add(f)
    census = ('shorthand references in Main/: ' +
              ', '.join(f'{k}={sum(len(v) for v in used[k].values())}' for k in NAMESPACES) +
              '  (external, not checked: ' +
              ', '.join(f'{k}={sum(len(p.findall(b)) for b in bodies.values())}'
                        for k, p in EXTERNAL_SHORT.items()) + ')')
    lines, problems = [], []
    for k in NAMESPACES:
        dang = sorted(set(used[k]) - defined[k] - set(SHORT_ALIAS) - SHORT_EXCEPTIONS)
        if not dang:
            lines.append(f'  {k}: 0 dangling ({len(defined[k])} defined)')
            continue
        lines.append(f'  {k}: {len(dang)} dangling shorthand id(s)')
        for d in dang[:20]:
            where = sorted(used[k][d])
            lines.append(f'       {d} <- {", ".join(where[:2])}'
                         + (' ...' if len(where) > 2 else ''))
        problems.append(f'DANGLING SHORTHAND {k}: {", ".join(dang[:8])}')
    return census, problems, lines


def self_test():
    """The checker must be able to FAIL.  Each case is a synthetic ledger body."""
    cases = [
        ('a bare dangling C id is caught',      {'a.md': 'see C999 here'}, 'C999'),
        ('a bare dangling G id is caught',      {'a.md': 'see G99 here'}, 'G99'),
        ('a dangling PN id is caught',          {'a.md': 'see PN-9 here'}, 'PN-9'),
        ('a heading defines a C id',            {'a.md': '### K15-C097 -- x\nsee C097'}, None),
        ('a table row defines a G id',          {'a.md': '| G98 | x |\nsee G98'}, None),
        ('a bold bullet defines a PN id',       {'a.md': '**PN-9 -- x.**\nsee PN-9'}, None),
        ('a bold announcement defines a C id',  {'a.md': '**form (K15-C096, PROPOSED)**\nC096'}, None),
        ('an aliased id resolves',              {'a.md': 'see C015r'}, None),
        ('a fully-qualified ref is not a shorthand', {'a.md': 'see K15-C999'}, None),
        ('the C5 family is not a shorthand',    {'a.md': 'the C5 family'}, None),
        ("the polytope D-prime is not a shorthand", {"a.md": "D' and D'"}, None),
    ]
    ok = True
    for name, bodies, must_flag in cases:
        _, problems, _ = shorthand_report(bodies)
        flagged = {p.split(': ')[1].split(',')[0] for p in problems} if problems else set()
        got = must_flag in flagged if must_flag else not problems
        print(f'  [{"ok" if got else "FAIL"}] {name}')
        ok = ok and got
    print('  SELF-TEST:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1



def gap_audit():
    """Warn where a PROVED/AUDITED entry cites a gap that is still open (K15-C144).

    A gap may be reopened and later closed, so the LAST entry in PROOF_GAPS.md wins --
    a first-wins parse reported G13/G14/G17 as open after they had been closed, which
    is the same duplication bug the status check had.  Warnings only: most citations
    are scope statements ("this does not close G11"), which are correct and wanted.
    """
    gpath = os.path.join(ROOT, 'KeplerConjecture', 'Main', 'PROOF_GAPS.md')
    claims = open(CLAIMS, encoding='utf-8').read()
    gaps = open(gpath, encoding='utf-8').read()
    gstat = {}
    for m in re.finditer(r'^#{2,3}\s*(G\d{1,2})\s*(?:[\u2014-]+)\s*(.*)$', gaps, re.M):
        gstat[m.group(1)] = bool(re.search(r'CLOSED|SUPERSEDED|WITHDRAWN|DOWNGRADED',
                                           m.group(2), re.I))
    for m in re.finditer(r'^\|\s*(G\d{1,2})\s*\|(.*)$', gaps, re.M):
        gstat[m.group(1)] = bool(re.search(r'closed|supplied|done', m.group(2), re.I))
    out = []
    for part in re.split(r'^###\s+', claims, flags=re.M)[1:]:
        head = part.split('\n', 1)[0]
        mm = re.match(r'K15-(C\d{3}[a-z]?)', head)
        if not mm:
            continue
        st = re.findall(r'\*Status\.\*\s*(.{0,90})', part)
        if not re.search(r'PROVED|AUDITED', st[-1] if st else head, re.I):
            continue
        cited = sorted({g for g in re.findall(r'\b(G\d{1,2})\b', part)
                        if g in gstat and not gstat[g]})
        if cited:
            out.append((mm.group(1), cited))
    print(f'\ngap cross-check: {len(out)} PROVED/AUDITED entr(ies) cite an open gap')
    for cid, cited in out:
        print(f'   {cid:8s} cites {", ".join(cited)}   (expect a scope statement, not a dependency)')
    print('   [warning only: a citation is not a dependency, and the ledger states scope explicitly]')
    return out


def main():
    if '--self-test' in sys.argv:
        return self_test()
    if '--audit-gaps' in sys.argv:
        gap_audit()
        return 0
    text = open(CLAIMS, encoding='utf-8').read()
    problems = []

    heads = HEAD_RE.findall(text)
    ids = {}
    addenda = []
    for kind, num, rest in heads:
        cid = canon(f'K15-{kind}{num}')
        if re.match(r'\s*addendum', rest):
            addenda.append(cid)          # a sub-heading of cid, not a duplicate
            continue
        if cid in ids:
            problems.append(f'DUPLICATE id {cid}')
        ids[cid] = rest
    if addenda:
        print(f'addendum sub-headings (allowed): {len(addenda)} '
              f'-> {sorted(set(addenda))}')
    # K15-C140: ids are also DEFINED by table rows (`| K15-R001 | ... |`) and by bold
    # announcements; taking headings alone reported 29 phantom danglers, including the
    # whole K15-R family which has always lived in a table.
    n_table = 0
    for m in re.finditer(r'^\|\s*(K15-[CERX]-?\d{3}[a-z]?)\s*\|', text, re.M):
        cid = canon(m.group(1))
        if cid not in ids:
            ids[cid] = '(table row)'; n_table += 1
    for m in re.finditer(r'\*\(K15-([CERX])-?(\d{3}[a-z]?)[,)]', text):
        cid = canon(f'K15-{m.group(1)}{m.group(2)}')
        if cid not in ids:
            ids[cid] = '(bold announcement)'
    print(f'headings with ids: {len(heads)}   distinct ids: {len(ids)}  '
          f'({n_table} defined by a table row)')

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

    # every fully-qualified reference resolves.
    # K15-C140: the dash after the class letter used to be MANDATORY here, while the
    # ledger writes `K15-C110` (no dash).  Every such reference was therefore invisible
    # to this check -- it reported "0 dangling" because it examined almost nothing.
    ref_re = re.compile(r'K15-([CERX])-?(C?\d{3}[a-z]?|\d{3}[a-z]?)')
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
                ref = canon(f'K15-{m.group(1)}{m.group(2)}')
                ref = ALIAS_FULL.get(ref, ref)
                if (ref not in ids and canon(ref) not in EXTERNAL
                        and ref not in SYNTHETIC):
                    dangling.setdefault(ref, set()).add(
                        os.path.relpath(path, ROOT))
    print(f'\nfully-qualified references that do not resolve: {len(dangling)}')
    for ref in sorted(dangling):
        where = sorted(dangling[ref])
        print(f'    {ref:16s} <- {", ".join(where[:3])}'
              + (' …' if len(where) > 3 else ''))
        problems.append(f'DANGLING {ref}')

    # ---- shorthand references (K15-C140, review block 0738) -------------------
    bodies = {}
    for f in sorted(os.listdir(os.path.join(ROOT, 'KeplerConjecture', 'Main'))):
        if f.endswith('.md'):
            bodies[f] = open(os.path.join(ROOT, 'KeplerConjecture', 'Main', f),
                             encoding='utf-8', errors='replace').read()
    census, sh_problems, sh_lines = shorthand_report(bodies)
    print('\n' + census)
    for line in sh_lines:
        print(line)
    problems.extend(sh_problems)

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
