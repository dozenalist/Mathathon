#!/usr/bin/env python3
"""Semantics-preserving scaffolding compression for lean/OAI (rewrite, v2).

Rules (each scope-local; declaration text is never touched):
 1 merge consecutive `open`/`open scoped` lines, deduplicating names          (safe)
 2 drop an `open`/`open scoped` line whose names are already open in scope     (safe)
 3 merge consecutive `variable` lines                                          (safe)
 4 merge consecutive `omit` lines                                              (safe)
 5 drop a `noncomputable section` whose enclosing scope is already
   noncomputable, together with its matching `end`                            (scope stack)
 6 merge an immediately nested `namespace A` / `namespace B` into
   `namespace A.B`, dropping the inner matching `end`                          (scope stack)
 7 collapse runs of blank lines                                                (safe)
Commands ending in ` in` (term-scoped syntax) are never touched.
"""
import os, re, sys

MERGE_NS = False
ROOT = os.environ.get("SCAFFOLD_ROOT", "/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI")

def files():
    out = []
    for dp, _, fs in os.walk(ROOT):
        for f in sorted(fs):
            if f.endswith(".lean"):
                out.append(os.path.join(dp, f))
    return sorted(out)

open_re = re.compile(r"^open\s+(scoped\s+)?(.+)$")
ns_re = re.compile(r"^namespace\s+([A-Za-z_][\w.']*)$")
sec_re = re.compile(r"^(noncomputable\s+)?section\b(.*)$")
end_re = re.compile(r"^end\b(.*)$")
var_re = re.compile(r"^variable\b")
omit_re = re.compile(r"^omit\b")

def transform(lines):
    out = []
    stack = []          # dicts: kind, out_idx, nc, drop_open, drop_end
    i, n = 0, len(lines)

    def cur_nc():
        return stack[-1]["nc"] if stack else False

    def prev_nonblank():
        j = len(out) - 1
        while j >= 0 and out[j] is not None and out[j].strip() == "":
            j -= 1
        return j

    while i < n:
        raw = lines[i]
        s = raw.strip()
        if s.endswith(" in"):
            out.append(raw); i += 1; continue
        if end_re.match(s) and stack:
            top = stack.pop()
            if top["drop_end"]:
                if top["drop_open"] and top["out_idx"] is not None:
                    out[top["out_idx"]] = None
                i += 1; continue
            out.append(raw); i += 1; continue
        m = ns_re.match(s)
        if m:
            name = m.group(1)
            j = prev_nonblank()
            if MERGE_NS and j >= 0 and out[j] is not None and stack and stack[-1]["out_idx"] == j:
                pm = ns_re.match(out[j].strip())
                if pm:
                    out[j] = "namespace " + pm.group(1) + "." + name
                    stack.append(dict(kind="ns", out_idx=None, nc=cur_nc(),
                                      drop_open=True, drop_end=True))
                    i += 1; continue
            out.append(raw)
            stack.append(dict(kind="ns", out_idx=len(out) - 1, nc=cur_nc(),
                              drop_open=False, drop_end=False))
            i += 1; continue
        m = sec_re.match(s)
        if m:
            nc = m.group(1) is not None
            drop = nc and cur_nc()
            out.append(raw)
            stack.append(dict(kind="sec", out_idx=len(out) - 1, nc=cur_nc() or nc,
                              drop_open=drop, drop_end=drop))
            i += 1; continue
        m = open_re.match(s)
        if m:
            scoped = bool(m.group(1))
            names = []
            for t in m.group(2).split():
                if t not in names:
                    names.append(t)
            j = prev_nonblank()
            if j >= 0 and out[j] is not None:
                pm = open_re.match(out[j].strip())
                if pm and bool(pm.group(1)) == scoped:
                    prev_names = pm.group(2).split()
                    merged = prev_names + [t for t in names if t not in prev_names]
                    out[j] = "open " + ("scoped " if scoped else "") + " ".join(merged)
                    i += 1; continue
            # already open in this scope?
            already, k = set(), len(out) - 1
            while k >= 0:
                q = out[k]
                if q is None:
                    k -= 1; continue
                qs = q.strip()
                qm = open_re.match(qs)
                if qm and bool(qm.group(1)) == scoped:
                    already.update(qm.group(2).split())
                if ns_re.match(qs) or sec_re.match(qs) or end_re.match(qs):
                    break
                k -= 1
            if set(names) <= already and already:
                i += 1; continue
            out.append(raw); i += 1; continue
        if var_re.match(s) and out and out[-1] is not None and var_re.match(out[-1].strip()):
            out[-1] = out[-1].rstrip() + " " + s[len("variable"):].strip()
            i += 1; continue
        if omit_re.match(s) and out and out[-1] is not None and omit_re.match(out[-1].strip()):
            out[-1] = out[-1].rstrip() + " " + s[len("omit"):].strip()
            i += 1; continue
        if s == "" and out and out[-1] is not None and out[-1].strip() == "":
            i += 1; continue
        out.append(raw); i += 1
    if stack:
        raise SystemExit("unbalanced scopes")
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
        total0 += len(src); total1 += len(new)
        rows.append((len(src) - len(new), os.path.relpath(p, ROOT), len(src), len(new)))
        if apply and dest:
            q = os.path.join(dest, "OAI", os.path.relpath(p, ROOT))
            os.makedirs(os.path.dirname(q), exist_ok=True)
            body = "\n".join(new)
            old = open(q, encoding="utf-8").read() if os.path.exists(q) else None
            if old != body:
                open(q, "w", encoding="utf-8").write(body)
    rows.sort(reverse=True)
    for d, p, a, b in rows:
        if d:
            print("%5d  %-58s %5d -> %5d" % (d, p, a, b))
    print("TOTAL %d -> %d   saved %d" % (total0, total1, total0 - total1))
