#!/usr/bin/env python3
"""Reproducible accounting for the strict-state-branch removal (swarm smwgpubt5, member m1).

Run from the repo root:  python3 .ultramath/smwgpubt5/m1/accounting.py
Every number printed here is used in budget.md.  Read-only: it opens files, writes nothing.
"""
import difflib, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
PC   = os.path.join(ROOT, 'lean', 'OAI', 'Geometry', 'PlaneColoring')
INT  = os.path.join(ROOT, 'supervisor', 'simplify-lean', 'integration')

def lines(p):
    t = open(p).read().split('\n')
    return t[:-1] if t and t[-1] == '' else t

def classify(path, lo=None, hi=None):
    L = lines(path); lo, hi = lo or 1, hi or len(L)
    depth = 0; blank = comment = code = 0
    for i in range(lo, hi + 1):
        l = L[i-1]; has_c = False; has_m = (depth > 0); j = 0
        while j < len(l):
            if depth == 0 and l.startswith('--', j): has_m = True; break
            if depth == 0 and l.startswith('/-', j): depth = 1; has_m = True; j += 2; continue
            if depth > 0:
                if l.startswith('/-', j): depth += 1; j += 2; continue
                if l.startswith('-/', j): depth -= 1; j += 2; continue
                j += 1; continue
            if not l[j].isspace(): has_c = True
            j += 1
        code += has_c; comment += (has_m and not has_c); blank += (not has_c and not has_m)
    return {'total': hi-lo+1, 'code': code, 'comment': comment, 'blank': blank}

DECL = re.compile(r'^(?:private\s+|protected\s+|noncomputable\s+|scoped\s+)*'
                  r'(lemma|theorem|def|abbrev|instance|structure|class)\s+([A-Za-z_][A-Za-z0-9_.\']*)')
STRUCT = re.compile(r'^(noncomputable section|section|namespace|end|open|variable|attribute|instance)')

def spans(path, lo, hi):
    L = lines(path); out = []; cur = None; struct = []
    for i in range(lo, hi+1):
        s = L[i-1]; st = s.strip(); m = DECL.match(s)
        if m:
            if cur: out.append(cur)
            cur = [m.group(2), i, i]
        elif STRUCT.match(st):
            if cur: out.append(cur); cur = None
            struct.append((i, st))
        elif cur:
            cur[2] = i
    if cur: out.append(cur)
    return out, struct

def enclosing(path, lineno, cache={}):
    L = cache.setdefault(path, lines(path))
    for k in range(min(lineno, len(L))-1, -1, -1):
        m = DECL.match(L[k])
        if m: return m.group(2), k+1
    return '<top>', 0

def consumers(name, files):
    pat = re.compile(r'(?<![A-Za-z0-9_.])' + re.escape(name) + r'(?![A-Za-z0-9_])')
    out = []
    for p in files:
        for i, l in enumerate(lines(p), 1):
            if pat.search(l):
                d, dl = enclosing(p, i); out.append((os.path.relpath(p, ROOT), i, d, dl))
    return out

def closure(imps, m):
    seen = set(); st = [m]
    while st:
        for y in imps.get(st.pop(), []):
            if y not in seen: seen.add(y); st.append(y)
    return seen

def main():
    orig = {f: os.path.join(PC, f) for f in
            ('FiveSupport.lean', 'Interfaces.lean', 'FourContinuity.lean', 'States.lean')}
    new = {f: os.path.join(INT, f) for f in os.listdir(INT) if f.endswith('.lean')}

    print('## 1. line counts (wc -l semantics)')
    for f, p in list(orig.items()) + sorted(new.items()):
        print(f'   {f:22s} {len(lines(p)):5d}')

    print('\n## 2. exact edit script (1-based, inclusive)')
    for f in ('FiveSupport.lean', 'Interfaces.lean', 'FourContinuity.lean', 'States.lean'):
        A, B = lines(orig[f]), lines(new[f])
        sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                print(f'   {f:20s} {tag:8s} old {i1+1}-{i2} ({i2-i1})  new {j1+1}-{j2} ({j2-j1})')

    print('\n## 3. removed States block: per-declaration budget')
    sp, st = spans(orig['States.lean'], 525, 722)
    tot = 0
    for n, a, b in sp:
        print(f'   {n:34s} {a:4d}-{b:4d}  {b-a+1:4d}'); tot += b-a+1
    print(f'   {"declaration lines":34s} {"":11s}{tot:4d}')
    print(f'   {"structural lines":34s} {"":11s}{len(st):4d}   {[i for i,_ in st]}')
    c = classify(orig['States.lean'], 525, 722)
    print(f'   {"blank lines":34s} {"":11s}{c["blank"]:4d}')
    print(f'   total {tot+len(st)+c["blank"]} (expect 198)')

    print('\n## 4. classification of every added / removed region')
    print('   AvoidingTrace.lean   ', classify(os.path.join(INT, 'AvoidingTrace.lean')))
    print('   States 525-722       ', classify(orig['States.lean'], 525, 722))
    print('   FiveSupport 9-31     ', classify(orig['FiveSupport.lean'], 9, 31))
    print('   FourContinuity 361-400', classify(orig['FourContinuity.lean'], 361, 400))
    print('   FourContinuity 451-457', classify(orig['FourContinuity.lean'], 451, 457))
    print('   FourContinuity 412-415', classify(os.path.join(INT, 'FourContinuity.lean'), 412, 415))

    print('\n## 5. net diff')
    files = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(ROOT, 'lean'))
             for f in fs if f.endswith('.lean')]
    add = rem = 0
    for f in ('FiveSupport.lean', 'Interfaces.lean', 'FourContinuity.lean', 'States.lean'):
        A, B = lines(orig[f]), lines(new[f])
        sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                add += j2-j1; rem += i2-i1
    add += len(lines(os.path.join(INT, 'AvoidingTrace.lean')))
    print(f'   additions {add}  removals {rem}  net {add-rem}   (AvoidingTrace +{len(lines(os.path.join(INT, "AvoidingTrace.lean")))})')
    print(f'   with the spurious `end Generic` (AvoidingTrace:230) deleted: net {add-rem-1}')

    print('\n## 6. consumers of the seven removed names, whole lean/ tree')
    for n in ('nonparallel_neighborhood', 'strict_state_sequence_local_false',
              'positive_state_support_point', 'support_density_direction',
              'support_density_sequence', 'strict_state_sequence_false',
              'strict_state_no_unit_support'):
        cs = consumers(n, files)
        print(f'   {n}:')
        for p, i, d, dl in cs: print(f'      {p}:{i}  in {d} (decl {dl})')

    print('\n## 7. consumers of the preserved declarations')
    for n in ('indicator_inter_positive', 'two_state_impossible', 'four_realState_continuity',
              'four_support_continuity', 'four_support_sequence_no_unit', 'five_support_step_ban'):
        cs = consumers(n, files)
        print(f'   {n}: ' + '; '.join(f'{p}:{i} in {d}' for p, i, d, _ in cs))

    print('\n## 8. section/namespace balance')
    def bal(path):
        stack = []; errs = []
        for i, l in enumerate(lines(path), 1):
            s_ = l.strip()
            if re.match(r'^(noncomputable section|section)(\s+\w+)?$', s_):
                nm = s_.split()[-1]
                stack.append([nm] if (s_.startswith('section') or s_ == 'section') else ['section'])
            elif re.match(r'^namespace\s+[\w.]+$', s_):
                for c in s_.split()[-1].split('.'): stack.append([c])
            elif s_ == 'end' or s_.startswith('end '):
                nm = s_[3:].strip()
                if not nm:
                    if stack: stack.pop()
                    else: errs.append((i, 'bare end, empty stack'))
                else:
                    comps = nm.split('.')[::-1]
                    if len(stack) >= len(comps) and [e[-1] for e in stack[-len(comps):]] == comps[::-1]:
                        for _ in comps: stack.pop()
                    else:
                        errs.append((i, 'end ' + nm + ' matches nothing; top=' +
                                     (stack[-1][-1] if stack else 'EMPTY')))
        return stack, errs
    for f, p in list(orig.items()) + sorted(new.items()):
        st, errs = bal(p)
        print(f'   {f:22s} unclosed={len(st)} {st}  errors={errs}')

    print('\n## 9. module closure')
    mods = {}
    for d, _, fs in os.walk(os.path.join(ROOT, 'lean')):
        for f in fs:
            if f.endswith('.lean'):
                p = os.path.join(d, f)
                mods[os.path.relpath(p, os.path.join(ROOT, 'lean'))[:-5].replace('/', '.')] = p
    imps = {m: re.findall(r'^import\s+(\S+)', open(p).read(), re.M) for m, p in mods.items()}
    cl = closure(imps, 'OAI.Geometry.PlaneColoring.BoundaryTrace')
    print(f'   closure(BoundaryTrace) = {len(cl)} modules')
    for bad in ('OAI.Geometry.PlaneColoring.FiveSupport', 'OAI.Geometry.PlaneColoring.Interfaces',
                'OAI.Geometry.PlaneColoring.FourContinuity', 'OAI.Geometry.PlaneColoring.Accumulation'):
        print(f'      contains {bad}? {bad in cl}')

if __name__ == '__main__':
    main()
