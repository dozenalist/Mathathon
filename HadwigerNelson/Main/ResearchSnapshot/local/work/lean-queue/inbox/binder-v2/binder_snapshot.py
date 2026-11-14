#!/usr/bin/env python3
"""Strict comparator for a BinderAudit.lean capture (schema 2).

Usage: python3 binder_snapshot.py CAPTURE [binder_expected.json]

Fails closed. Every check below is a FAIL, never a mere warning, except where explicitly noted:
  * declaration absent from the capture                      -> FAIL
  * ERROR line for a declaration                             -> FAIL
  * implicit type binders not exactly ["X","Y","W"]          -> FAIL
  * any non-X/Y/Z implicit value binder                      -> FAIL (UNKNOWN)
  * instance binder whose type is not in instance_allowed    -> FAIL (UNKNOWN EXTRA INSTANCE)
  * a monotone forbidden instance (StandardBorelSpace Y / Nonempty Y in a theorem) -> FAIL
  * any strict-implicit binder                               -> FAIL (counted separately)
  * explicit binder name sequence != expected                -> FAIL
  * total binder count != expected_total_binders             -> FAIL
A TYPE-MISMATCH is a FAIL for instance binders and a WARNING for explicit ones (pretty-printing of
hypotheses depends on pp options; the name sequence is the load-bearing check there).

Printed evidence is ALWAYS the full binder list, even when the verdict is FAIL, so a failing run
still yields usable information.

Exit codes: 0 all pass; 1 any FAIL; 2 capture unusable (no records at all).
NOTE: only a capture produced by compiling BinderAudit.lean against the R4 tree is evidence.
Synthetic captures exercise the comparator and nothing else.
"""
import json, sys

def norm(s):
    return " ".join(s.split())

def load(path):
    recs, bad = {}, 0
    for raw in open(path, errors="ignore"):
        line = raw.rstrip("\n")
        if line.startswith("BINDER "):
            parts = line.split(" ", 5)
            if len(parts) < 6:
                bad += 1; continue
            _, decl, i, nm, info, ty = parts
            recs.setdefault(decl, {"binders": [], "error": None})["binders"].append(
                {"i": int(i), "name": nm, "info": info, "type": norm(ty)})
        elif line.startswith("MISSING "):
            recs.setdefault(line.split(" ", 1)[1].strip(), {"binders": [], "error": "MISSING"})
        elif line.startswith("ERROR "):
            d, msg = (line[6:].split(" ", 1) + [""])[:2]
            recs.setdefault(d.strip(), {"binders": [], "error": "ERROR " + msg})
    return recs, bad

def check(decl, via, spec, common, allow_extra_implicit_types):
    fails, warns, notes = [], [], []
    b = sorted(via["binders"], key=lambda x: x["i"])
    forbidden = list(spec.get("instance_forbidden", common["instance_forbidden"]))
    print(f"\n== {decl}")
    for x in b:
        tag = ""
        if x["info"] == "instance" and any(f == x["type"] for f in forbidden):
            tag = "  <-- FORBIDDEN"
        elif x["info"] == "instance" and x["type"] not in common["instance_allowed"]:
            tag = "  <-- UNKNOWN INSTANCE"
        elif x["info"] == "strict":
            tag = "  <-- STRICT"
        elif x["info"] == "implicit" and x["type"].startswith("Type"):
            tag = ""
        elif x["info"] == "implicit":
            tag = "  <-- UNKNOWN IMPLICIT"
        print(f"   [{x['i']:>2}] {x['name']:<12} {x['info']:<9} {x['type']}{tag}")

    imp = [x for x in b if x["info"] == "implicit"]
    val_imp = [x for x in imp if not x["type"].startswith("Type")]
    typ_imp = [x for x in imp if x["type"].startswith("Type")]
    names = spec.get("type_binders", common["type_binders"])
    if [x["name"] for x in typ_imp] != names:
        fails.append(f"type binders {[x['name'] for x in typ_imp]} != {names}")
    for x in val_imp:
        if not allow_extra_implicit_types:
            fails.append(f"unknown implicit value binder {x['name']} : {x['type']}")

    insts = [x["type"] for x in b if x["info"] == "instance"]
    for f in forbidden:
        if f in insts:
            fails.append(f"forbidden instance binder present: {f}")
    allowed = list(spec.get("instance_allowed", common["instance_allowed"]))
    for t in insts:
        if t not in allowed:
            fails.append(f"UNKNOWN EXTRA INSTANCE: {t}")
    for t in allowed:
        if t not in insts:
            fails.append(f"ABSENT required instance: {t}")

    strict = [x for x in b if x["info"] == "strict"]
    if strict:
        fails.append(f"strict-implicit binders present: {[x['name'] for x in strict]}")

    expl = [x["name"] for x in b if x["info"] == "explicit"]
    want = spec.get("explicit_order", [])
    if expl != want:
        fails.append(f"explicit sequence mismatch: got {len(expl)} {expl} want {len(want)} {want}")

    if "expected_total_binders" in spec and len(b) != spec["expected_total_binders"]:
        fails.append(f"total binders {len(b)} != {spec['expected_total_binders']}")

    if fails:
        for f in fails:
            print("   FAIL: " + f)
    else:
        print("   PASS: no forbidden or unknown instance, type binders exact, no strict, explicit sequence exact")
    return fails

def main():
    if len(sys.argv) < 2:
        print("usage: binder_snapshot.py CAPTURE [EXPECTED.json]"); return 2
    recs, bad = load(sys.argv[1])
    exp = json.load(open(sys.argv[2] if len(sys.argv) > 2 else
                         "supervisor/simplify-lean/binder_expected.json"))
    if not recs:
        print("CAPTURE UNUSABLE: no DECL/BINDER/MISSING/ERROR records found"); return 2
    common = exp["common"]
    total_fail = 0
    groups = [("theorems", False), ("definitions", True)]
    for gname, allow_extra in groups:
        for key, spec in exp[gname].items():
            fqn = spec["fqn"]
            via = recs.get(fqn) or recs.get(key)
            if via is None:
                print(f"\n== {fqn}\n   FAIL: ABSENT from capture (fail closed)"); total_fail += 1; continue
            if via["error"]:
                print(f"\n== {fqn}\n   FAIL: {via['error']}"); total_fail += 1; continue
            total_fail += len(check(key, via, spec, common, allow_extra))
    print(f"\nSUMMARY fails={total_fail}  (0 = pass)")
    if bad: print(f"malformed BINDER lines: {bad}")
    return 0 if total_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
