#!/usr/bin/env python3
"""Compare a BinderAudit.lean capture against binder_expected.json.
Usage: python3 binder_snapshot.py binders.txt [binder_expected.json]
Reports, per declaration: every retained binder; then PASS/FAIL for
  (a) forbidden instance binders absent,
  (b) the explicit argument order/count,
  (c) the required instance binder present present.
Exit 0 = all checks pass for every captured decl; 1 = a violation; 2 = a decl missing from the capture.
A missing decl is INCONCLUSIVE, never PASS."""
import json, re, sys
def load(path):
    d = {}
    for line in open(path, errors="ignore"):
        line = line.strip()
        if line.startswith("BINDER "):
            _, decl, i, nm, info, *ty = line.split(" ", 5)
            d.setdefault(decl, []).append((int(i), nm, info, (ty[0] if ty else "")))
        elif line.startswith("MISSING "):
            d.setdefault(line.split(" ", 1)[1], "MISSING")
    return d
def main():
    cap = load(sys.argv[1])
    exp = json.load(open(sys.argv[2] if len(sys.argv) > 2 else
                         "supervisor/simplify-lean/binder_expected.json"))
    viol, missing, ok = [], [], []
    for key in ("finite_uniform_precision_contradiction",
                "ambient_uniform_precision_contradiction",
                "uniform_precision_contradiction"):
        spec = exp[key]; fqn = spec["fqn"]; short = fqn.split(".")[-1]
        got = cap.get(short) or cap.get(fqn)
        print(f"\n== {fqn}")
        if not got or got == "MISSING":
            missing.append(fqn); print("   MISSING from capture -> INCONCLUSIVE"); continue
        for i, nm, info, ty in sorted(got):
            flag = ""
            if any(f in ty for f in exp["common"]["forbidden_instance_types"]): flag = "  <-- FORBIDDEN"
            print(f"   [{i:>2}] {nm:<10} {info:<9} {ty}{flag}")
        bad = []
        for i, nm, info, ty in got:
            if any(f in ty for f in exp["common"]["forbidden_instance_types"]):
                bad.append(f"forbidden binder {nm} : {ty}")
        expl = [nm for i, nm, info, ty in sorted(got) if info in ("explicit", "strict")]
        if expl != spec["explicit_order"]:
            bad.append(f"explicit order/count mismatch: got {len(expl)} {expl}")
        if not any(r in ty for i, nm, info, ty in got for r in exp["common"]["required_instance_types"]):
            bad.append("required instance MeasurableSpace Y absent")
        if bad:
            viol.append((fqn, bad)); print("   FAIL: " + "; ".join(bad))
        else:
            ok.append(fqn); print("   PASS: no forbidden instances, explicit order exact, MeasurableSpace Y retained")
    print(f"\nSUMMARY pass={len(ok)} fail={len(viol)} inconclusive={len(missing)}")
    return 0 if (not viol and not missing) else (1 if viol else 2)
if __name__ == "__main__":
    sys.exit(main())
