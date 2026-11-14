#!/usr/bin/env python3
"""Simulate semantics-preserving scaffolding compression on lean/OAI.

Transformations (all scope-local, statement text never touched):
 1. consecutive `open A` / `open scoped A` runs -> one merged line (same position, same set)
 2. an `open`/`open scoped` line whose namespaces are already open in the current scope -> drop
 3. consecutive `variable ...` lines -> merged  (only when they are a run with nothing between)
 4. consecutive `omit [...]` lines -> merged
 5. redundant `noncomputable section` (enclosing scope already noncomputable) -> drop with its `end`
 6. immediately nested `namespace A` / `namespace B` -> `namespace A.B`, merged `end`s
 7. runs of 2+ blank lines -> 1
"""
import os, re, sys

ROOT = "/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI"

def files():
    out = []
    for dp, _, fs in os.walk(ROOT):
        for f in sorted(fs):
            if f.endswith(".lean"):
                out.append(os.path.join(dp, f))
    return sorted(out)

open_re = re.compile(r"^(\s*)open\s+(scoped\s+)?(.+)$")
ns_re = re.compile(r"^(\s*)namespace\s+([A-Za-z_][\w.']*)\s*$")
sec_re = re.compile(r"^(\s*)(noncomputable\s+)?section\b(.*)$")
end_re = re.compile(r"^(\s*)end\b(.*)$")
var_re = re.compile(r"^(\s*)variable\b")
omit_re = re.compile(r"^(\s*)omit\b")

def transform(lines, do=(1,2,3,4,5,6,7)):
    out = []
    i = 0
    n = len(lines)
    # scope stack: dicts {kind, line_index in out, noncomp}
    stack = [dict(kind='file', nc=False, out_idx=None, name='')]
    while i < n:
        line = lines[i]
        s = line.strip()
        # 5/6: closing end
        m = end_re.match(line)
        if m and stack and stack[-1]['kind'] != 'file':
            top = stack.pop()
            if top.get('drop'):
                out[top['out_idx']] = None            # remove the opening line
                i += 1
                continue                              # and this end
            out.append(line)
            i += 1
            continue
        m = ns_re.match(line)
        if m:
            indent, name = m.group(1), m.group(2)
            nc = stack[-1]['nc']
            # 6: merge immediately nested namespace
            if 6 in do and out and out[-1] is not None and ns_re.match(out[-1] or ''):
                out[-1] = None
                i += 1
                continue
            if 6 in do and out:
                # allow merging when only blank lines separate
                j = len(out) - 1
                while j >= 0 and out[j] is not None and out[j].strip() == '':
                    j -= 1
                if j >= 0 and out[j] is not None and ns_re.match(out[j]):
                    out.append(indent + 'namespace ' + name)
                    stack.append(dict(kind='ns', nc=nc, out_idx=len(out) - 1, name=name, merge=True))
                    i += 1
                    continue
            out.append(line)
            stack.append(dict(kind='ns', nc=nc, out_idx=len(out) - 1, name=name))
            i += 1
            continue
        m = sec_re.match(line)
        if m:
            indent, noncomp, rest = m.group(1), m.group(2), m.group(3)
            drop = bool(noncomp) and stack[-1]['nc'] and 5 in do
            out.append(line)
            stack.append(dict(kind='sec', nc=stack[-1]['nc'] or bool(noncomp), out_idx=len(out) - 1, drop=drop))
            i += 1
            continue
        m = open_re.match(line)
        if m:
            indent, scoped, names = m.group(1), m.group(2) or '', m.group(3).strip()
            key = ('scoped:' if scoped else 'open:') + names
            if out:
                prev = out[-1]
                pm = open_re.match(prev) if prev is not None else None
                if pm and (pm.group(2) or '') == scoped and 1 in do:
                    out[-1] = indent + 'open ' + scoped + pm.group(3).strip() + ' ' + names
                    i += 1
                    continue
                if 2 in do:
                    # already open in this scope?  (scan back to nearest scope opener)
                    k = len(out) - 1
                    already = set()
                    while k >= 0:
                        q = out[k]
                        if q is None:
                            k -= 1
                            continue
                        qm = open_re.match(q)
                        if qm and (qm.group(2) or '') == scoped:
                            already.update(qm.group(3).split())
                        if ns_re.match(q) or sec_re.match(q) or end_re.match(q):
                            break
                        k -= 1
                    if set(names.split()) <= already:
                        i += 1
                        continue
            out.append(line)
            i += 1
            continue
        if 3 in do and var_re.match(line) and out and out[-1] is not None and var_re.match(out[-1]):
            out[-1] = out[-1].rstrip() + ' ' + s[len('variable'):].strip()
            i += 1
            continue
        if 4 in do and omit_re.match(line) and out and out[-1] is not None and omit_re.match(out[-1]):
            out[-1] = out[-1].rstrip() + ' ' + s[len('omit'):].strip()
            i += 1
            continue
        if 7 in do and s == '' and out and out[-1] is not None and out[-1].strip() == '':
            i += 1
            continue
        out.append(line)
        i += 1
    return [l for l in out if l is not None]

if __name__ == "__main__":
    apply = "--apply" in sys.argv
    dest = None
    for a in sys.argv[1:]:
        if a.startswith("--dest="):
            dest = a.split("=", 1)[1]
    total0 = total1 = 0
    rows = []
    for p in files():
        src = open(p, encoding="utf-8").read().split("\n")
        new = transform(src)
        total0 += len(src)
        total1 += len(new)
        rows.append((len(src) - len(new), os.path.relpath(p, ROOT), len(src), len(new)))
        if apply and dest:
            q = os.path.join(dest, os.path.relpath(p, os.path.dirname(ROOT)))
            os.makedirs(os.path.dirname(q), exist_ok=True)
            open(q, "w", encoding="utf-8").write("\n".join(new))
    rows.sort(reverse=True)
    for d, p, a, b in rows:
        if d:
            print("%5d  %-58s %5d -> %5d" % (d, p, a, b))
    print("TOTAL %d -> %d   saved %d" % (total0, total1, total0 - total1))
