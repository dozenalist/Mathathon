import json, os, re, subprocess, sys, pathlib, collections, time

M9 = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.ultramath/smwfoekgk/m9")
TREE = M9 / sys.argv[1]            # e.g. work4
OV = M9 / sys.argv[2]              # e.g. ov4
MODS = [l.strip() for l in open(M9 / sys.argv[3]) if l.strip()]
PAR = int(sys.argv[4]) if len(sys.argv) > 4 else 8

# import graph over the whole tree
deps = {}
for p in sorted(TREE.glob("OAI/**/*.lean")):
    n = ".".join(p.relative_to(TREE).with_suffix("").parts)
    deps[n] = [m.group(1) for m in re.finditer(r"^import\s+(OAI\.[\w.]+)\s*$",
                                              p.read_text(errors="ignore"), re.M)]

built = set()
for p in OV.glob("OAI/**/*.olean"):
    built.add(".".join(p.relative_to(OV).with_suffix("").parts))
stamp = OV / ".built_new"
newly = set()
if stamp.exists():
    newly = set(stamp.read_text().split())

env = dict(os.environ)
env["LEAN_PATH"] = "%s:%s" % (OV, env.get("LEAN_PATH", ""))
pending = list(MODS)
failed = {}
round_no = 0
while pending:
    round_no += 1
    ready = [m for m in pending if all((d in built and (d not in MODS or d in newly)) for d in deps[m] if d in deps)]
    if not ready:
        print("DEADLOCK; pending:", pending[:10], flush=True)
        break
    wave = ready[:PAR]
    procs = []
    for m in wave:
        out = OV / (m.replace(".", "/") + ".olean")
        out.parent.mkdir(parents=True, exist_ok=True)
        log = open("/tmp/w_%s.log" % m.replace(".", "_"), "w")
        p = subprocess.Popen(["lean", "-o", str(out), m.replace(".", "/") + ".lean"],
                             cwd=str(TREE), env=env, stdout=log, stderr=subprocess.STDOUT)
        procs.append((m, p, out, log))
    for m, p, out, log in procs:
        rc = p.wait()
        log.close()
        pending.remove(m)
        if rc == 0:
            built.add(m)
            newly.add(m)
            print("OK   " + m, flush=True)
        else:
            failed[m] = True
            if out.exists():
                out.unlink()
            print("FAIL " + m, flush=True)
    stamp.write_text("\n".join(sorted(newly)))
print("failed:", len(failed), flush=True)
for m in failed:
    print("  FAILED " + m, flush=True)
