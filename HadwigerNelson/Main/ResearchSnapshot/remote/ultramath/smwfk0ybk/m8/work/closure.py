import re, pathlib, sys, json
ROOT = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean")
mods = {}
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    deps = [m.group(1) for m in re.finditer(r"^import\s+(OAI\.[\w.]+)\s*$", p.read_text(errors="ignore"), re.M)]
    mods[name] = (p, deps)
def closure(roots):
    seen, st = set(), list(roots)
    while st:
        n = st.pop()
        if n in seen or n not in mods: continue
        seen.add(n)
        st.extend(mods[n][1])
    return seen
def lines(ns):
    return sum(len(mods[n][0].read_text(errors="ignore").splitlines()) for n in ns)
if __name__ == "__main__":
    roots = sys.argv[1:]
    C = closure(roots)
    tot = sum(len(mods[n][0].read_text(errors="ignore").splitlines()) for n in mods)
    print(f"roots={roots} closure={len(C)} modules, {lines(C)} lines (all OAI: {len(mods)} mods {tot} lines)")
    for n in sorted(C, key=lambda n: -len(mods[n][0].read_text(errors="ignore").splitlines())):
        print(f"{len(mods[n][0].read_text(errors='ignore').splitlines()):6d}  {n}")
