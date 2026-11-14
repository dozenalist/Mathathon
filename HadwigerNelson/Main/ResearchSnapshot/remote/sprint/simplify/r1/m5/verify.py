#!/usr/bin/env python3
"""Compile every module of --base that differs from --pristine, in dependency order,
against the seeded build dir; report the ones that fail with their first real error."""
import argparse, os, re, subprocess, pathlib, sys

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
IMP = re.compile(r"^import\s+([\w.]+)\s*$", re.M)
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")

def names(text):
    stack, out = [], set()
    for ln in text.splitlines():
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
        if d and d.group(2) not in ("where", "at", "at'"): out.add(d.group(2))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pristine", required=True); ap.add_argument("--base", required=True)
    ap.add_argument("--env", required=True); ap.add_argument("--stop", type=int, default=99)
    a = ap.parse_args()
    pri = pathlib.Path(a.pristine).resolve() / "lean"
    base = pathlib.Path(a.base).resolve() / "lean"
    build = base / "build" / "lib"
    env = dict(os.environ)
    o = subprocess.run(["bash", "-c",
        f"source {a.env} >/dev/null 2>&1; printf '%s\\n' \"$LEAN_PATH\"; printf '%s\\n' \"$PATH\""],
        capture_output=True, text=True, check=True).stdout.splitlines()
    env["LEAN_PATH"] = f"{build}:{o[0]}"; env["PATH"] = o[1]
    deps, pmap = {}, {}
    for p in sorted((pri / "OAI").rglob("*.lean")):
        m = ".".join(p.relative_to(pri).with_suffix("").parts)
        pmap[m] = p
        deps[m] = [x for x in IMP.findall(p.read_text(errors="ignore")) if x.startswith("OAI.")]
    order, seen = [], set()
    def visit(m):
        if m in seen: return
        seen.add(m)
        for d in deps.get(m, ()):
            if d in pmap: visit(d)
        order.append(m)
    for m in sorted(pmap): visit(m)
    fails = []
    for m in order:
        p = pri / (m.replace(".", "/") + ".lean")
        q = base / (m.replace(".", "/") + ".lean")
        if not q.exists():
            continue
        if p.read_text(errors="ignore") == q.read_text(errors="ignore"):
            continue
        olean = build / (m.replace(".", "/") + ".olean")
        olean.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["lean", "-o", str(olean), str(q)], cwd=base, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        gone = names(p.read_text(errors="ignore")) - names(q.read_text(errors="ignore"))
        if r.returncode == 0:
            print(f"OK   {m}  dropped {len(gone)}", flush=True)
        else:
            first = [l for l in r.stdout.splitlines() if "error" in l][:2]
            print(f"FAIL {m} : {first}", flush=True)
            fails.append(m)
            if len(fails) >= a.stop: break
    print(f"\n{len(fails)} failures")

main()
