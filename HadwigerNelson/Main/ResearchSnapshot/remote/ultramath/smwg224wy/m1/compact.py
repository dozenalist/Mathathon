#!/usr/bin/env python3
"""Scope-aware scaffolding compaction for the OAI tree.

Rule 1 (safe by construction): drop an `open ...` / `open scoped ...` line when an
IDENTICAL line is already active in the current scope.  `open` is additive and
idempotent, so dropping a duplicate cannot change name resolution.  Scope is tracked
with a stack: `namespace X` / `section` push, `end` pops; when a scope is popped, the
opens that were introduced at or above it stop being active.

Rule 2: collapse a run of 2+ blank lines to a single blank line.

Both rules are line-local and produce a tree in which every declaration's elaborated
type is unchanged (verified by rebuilding all modules and re-running CheckBoth.lean).
Usage: compact.py OAI_DIR [--apply]
"""
import sys, pathlib, collections

def compact_text(text):
    lines = text.split('\n')
    out = []
    stack = []
    active = set()          # (depth, stripped-line)
    removed = collections.Counter()
    run = 0
    for ln in lines:
        s = ln.strip()
        if s.startswith('namespace ') or s == 'section' or s.startswith('section '):
            stack.append(s)
        elif s.startswith('end') and (s == 'end' or s.startswith('end ')):
            if stack:
                stack.pop()
            active = {x for x in active if x[0] < len(stack)}
        if s.startswith('open ') or s.startswith('open scoped '):
            # only plain opens (no `open ... in`) are idempotent across lines
            if not s.endswith(' in') and ' in\n' not in s:
                key = (len(stack), s)
                if key in active:
                    removed['dup_open'] += 1
                    continue
                active.add(key)
        if s == '':
            run += 1
            if run >= 2:
                removed['blank'] += 1
                continue
        else:
            run = 0
        out.append(ln)
    return '\n'.join(out), removed

def main():
    root = pathlib.Path(sys.argv[1])
    apply = '--apply' in sys.argv
    tot_before = tot_after = 0
    per = {}
    agg = collections.Counter()
    for f in sorted(root.rglob('*.lean')):
        text = f.read_text()
        new, rem = compact_text(text)
        b = text.count('\n') - (1 if text.endswith('\n') else 0)
        a = new.count('\n') - (1 if new.endswith('\n') else 0)
        # normalise: keep a trailing newline
        if new and not new.endswith('\n'):
            new += '\n'
        tot_before += b; tot_after += a
        agg.update(rem)
        if b != a:
            per[str(f.relative_to(root))] = (b, a)
        if apply:
            f.write_text(new)
    for k, v in per.items():
        print(f"{k}: {v[0]} -> {v[1]}  (-{v[0]-v[1]})")
    print("---")
    print("removed by rule:", dict(agg))
    print(f"total {tot_before} -> {tot_after} (-{tot_before - tot_after})")
    if not apply:
        print("(dry run; pass --apply to write)")

main()
