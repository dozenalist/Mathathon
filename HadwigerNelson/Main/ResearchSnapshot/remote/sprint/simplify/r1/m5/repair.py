#!/usr/bin/env python3
"""Materialise a cut tree and repair it against the compiler.

For every module that differs from the pristine one, the module is rebuilt from the
pristine source by deleting only the declarations in its current drop-set.  The
module is then compiled against the staged build; on a parseable error the offending
declaration names are removed from the drop-set and the module is rebuilt and
recompiled.  If it still fails after N rounds the whole module is restored.

  python3 repair.py --pristine DIR --base DIR --staged DIR --env ENV.sh
"""
import argparse, os, re, subprocess, sys, pathlib, json

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
ENDL = re.compile(r"^\s*end(?:\s+[\w.]+)?\s*$")
STRUCT = re.compile(r"^\s*(variable|open|section|omit|attribute|set_option|universe|local\b|private\b|scoped\b|noncomputable\b|include\b)\b")
UNK = re.compile(r"Unknown identifier `([^`]+)`")
UNK2 = re.compile(r"unknownIdentifier.*?`([^`]+)`")

def spans(lines):
    stack, found = [], []
    for i, ln in enumerate(lines, 1):
        m = NS.match(ln)
        if m: stack.append(m.group(1)); continue
        if SEC.match(ln) or MUT.match(ln): stack.append(""); continue
        eo = END.match(ln)
        if eo:
            nm = eo.group(1)
            if nm and nm in stack:
                while stack and stack.pop() != nm: pass
            elif stack: stack.pop()
            continue
        d = DECL.match(ln)
        if d:
            kind, name = d.group(1), d.group(2)
            if name in ("where", "at", "at'"): continue
            pre = ".".join(x for x in stack if x)
            found.append((kind, name, (pre + "." + name) if pre else name, i))
    out = []
    for j, (kind, name, full, i) in enumerate(found):
        end = (found[j+1][3] - 1) if j + 1 < len(found) else len(lines)
        out.append(dict(kind=kind, name=name, full=full, line=i, end=end))
    return out

def region(lines, start, end):
    j = end
    while j > start and lines[j-1].strip() == '': j -= 1
    while j > start and (ENDL.match(lines[j-1]) or STRUCT.match(lines[j-1])
                         or lines[j-1].lstrip().startswith('--')): j -= 1
    if j > start and lines[j-1].strip().endswith('-/'):
        k = j - 1
        while k > start and not lines[k-1].strip().startswith('/--'): k -= 1
        j = k
    while j > start and lines[j-1].strip() == '': j -= 1
    return j

def materialise(pristine_text, drop):
    lines = pristine_text.splitlines()
    sp = spans(lines)
    for d in sorted([d for d in sp if d["name"] in drop], key=lambda d: -d["line"]):
        j = region(lines, d["line"], min(d["end"], len(lines)))
        del lines[d["line"]-1:j]
    return "\n".join(lines) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pristine", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--staged", required=True)
    ap.add_argument("--env", required=True)
    ap.add_argument("--rounds", type=int, default=6)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    pri = pathlib.Path(a.pristine).resolve() / "lean"
    base = pathlib.Path(a.base).resolve() / "lean"
    build = base / "build" / "lib"
    build.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    out = subprocess.run(["bash", "-c",
        f"source {a.env} >/dev/null 2>&1; printf '%s\\n' \"$LEAN_PATH\"; printf '%s\\n' \"$PATH\""],
        capture_output=True, text=True, check=True).stdout.splitlines()
    env["LEAN_PATH"] = f"{build}:{out[0]}"
    env["PATH"] = out[1]
    report = {"repaired": {}, "restored": [], "final_lines": 0}
    allmods = sorted((pri / "OAI").rglob("*.lean"))
    IMP2 = re.compile(r"^import\s+([\w.]+)\s*$", re.M)
    deps, pmap = {}, {}
    for p in allmods:
        m = ".".join(p.relative_to(pri).with_suffix("").parts)
        pmap[m] = p
        deps[m] = [x for x in IMP2.findall(p.read_text(errors="ignore")) if x.startswith("OAI.")]
    order, mark = [], {}
    def visit(m, stack=()):
        if mark.get(m) == 2: return
        if mark.get(m) == 1: return
        mark[m] = 1
        for d in deps.get(m, ()):
            if d in pmap: visit(d, stack + (m,))
        mark[m] = 2; order.append(m)
    for m in sorted(pmap): visit(m)
    mods = [pmap[m] for m in order]
    for p in mods:
        rel = p.relative_to(pri)
        q = base / rel
        if not q.exists():
            continue
        pris = p.read_text(errors="ignore")
        cur = q.read_text(errors="ignore")
        names_pris = {d["name"] for d in spans(pris.splitlines())}
        names_cur = {d["name"] for d in spans(cur.splitlines())}
        drop = names_pris - names_cur
        if not drop:
            q.write_text(pris)
            drop = set()
        mod = ".".join(rel.with_suffix("").parts)
        olean = build / (mod.replace(".", "/") + ".olean")
        olean.parent.mkdir(parents=True, exist_ok=True)
        if not drop:
            r = subprocess.run(["lean", "-o", str(olean), str(q)], cwd=base, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if r.returncode != 0:
                print(f"BASE FAIL {mod}\n{r.stdout[:600]}", flush=True)
            continue
        for rnd in range(a.rounds + 1):
            q.write_text(materialise(pris, drop))
            r = subprocess.run(["lean", "-o", str(olean), str(q)], cwd=base, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if r.returncode == 0:
                print(f"OK   {mod} (drop {len(drop)})", flush=True)
                report["repaired"][mod] = sorted(drop)
                break
            missing = set()
            for mm in list(UNK.finditer(r.stdout)) + list(UNK2.finditer(r.stdout)):
                missing.add(mm.group(1).split(".")[-1])
            add = (missing & drop)
            if not add:
                print(f"RESTORE {mod}: unparsable failure\n{r.stdout[:800]}", flush=True)
                q.write_text(pris)
                report["restored"].append(mod)
                subprocess.run(["lean", "-o", str(olean), str(q)], cwd=base, env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
            drop -= add
            print(f"  readd {sorted(add)} in {mod}", flush=True)
        else:
            print(f"RESTORE {mod}: rounds exhausted", flush=True)
            q.write_text(pris)
            report["restored"].append(mod)
    n = sum(1 for f in (base / "OAI").rglob("*.lean") for _ in open(f, errors="ignore"))
    report["final_lines"] = n
    print(f"\nfinal tree {n} raw lines over {len(list((base / 'OAI').rglob('*.lean')))} modules; "
          f"restored {len(report['restored'])} modules")
    if a.report: json.dump(report, open(a.report, "w"), indent=1)

main()
