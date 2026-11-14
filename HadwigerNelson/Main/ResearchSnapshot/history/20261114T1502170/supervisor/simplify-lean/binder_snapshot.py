#!/usr/bin/env python3
"""Comparator v3 for a BinderAudit.lean capture. Supplementary inspection only.

Usage: python3 binder_snapshot.py CAPTURE [binder_expected.json]

Three modes per declaration, set by the spec:
  frozen    (unfrozen=false): strict -- type binders exact, instance multiset must equal
             instance_allowed, unknown instance or absent required one -> FAIL, explicit sequence
             exact, total count checked if no_total_check is false.
  unfrozen  (unfrozen=true) : the instance set is NOT known yet, so it is not guessed. The observed
             multiset is printed and emitted as FREEZE-CANDIDATE; only forbidden instances, strict
             binders, type binders and the explicit sequence are enforced.
Always: absent declaration or ERROR line -> FAIL (fail closed); every binder is printed even on FAIL.

VALIDITY: a capture is evidence only if `lean` reported NO error for BinderAudit.lean. Lean inserts
placeholders after elaboration errors, so a file that "parses" can still have skipped the audit. If in
doubt, discard the capture -- a missing/partial capture is not a pass.

SYNTHETIC captures exercise this script only; they say nothing about the OAI tree.

Exit: 0 all pass; 1 any FAIL; 2 unusable capture.
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

def check(key, via, spec):
    fails, freezes = [], []
    b = sorted(via["binders"], key=lambda x: x["i"])
    forbidden = list(spec.get("instance_forbidden", []))
    unfrozen = bool(spec.get("unfrozen", False))
    allowed = spec.get("instance_allowed")
    print(f"\n== {key}   [{'UNFROZEN instance set' if unfrozen else 'frozen'}]")
    for x in b:
        tag = ""
        if x["info"] == "instance" and x["type"] in forbidden:
            tag = "  <-- FORBIDDEN"
        elif x["info"] == "instance" and (not unfrozen) and allowed is not None and x["type"] not in allowed:
            tag = "  <-- UNKNOWN INSTANCE"
        elif x["info"] == "strict":
            tag = "  <-- STRICT"
        elif x["info"] == "implicit" and not x["type"].startswith("Type"):
            tag = "  <-- EXTRA IMPLICIT (value)"
        print(f"   [{x['i']:>2}] {x['name']:<12} {x['info']:<9} {x['type']}{tag}")

    typ_imp = [x for x in b if x["info"] == "implicit" and x["type"].startswith("Type")]
    want_t = spec.get("type_binders", [])
    if [x["name"] for x in typ_imp] != want_t:
        fails.append(f"type binders {[x['name'] for x in typ_imp]} != {want_t}")

    insts = [x["type"] for x in b if x["info"] == "instance"]
    for f in forbidden:
        if f in insts:
            fails.append(f"FORBIDDEN instance present: {f}")
    if unfrozen:
        freezes.append(insts)
        print(f"   FREEZE-CANDIDATE instances = {insts}")
    elif allowed is not None:
        for t in insts:
            if t not in allowed:
                fails.append(f"UNKNOWN EXTRA INSTANCE: {t}")
        for t in allowed:
            if t not in insts:
                fails.append(f"ABSENT required instance: {t}")

    strict = [x["name"] for x in b if x["info"] == "strict"]
    if strict:
        fails.append(f"strict-implicit binders present: {strict}")

    expl = [x["name"] for x in b if x["info"] == "explicit"]
    if expl != spec.get("explicit_order", []):
        fails.append(f"explicit sequence mismatch: got {len(expl)} {expl} want {len(spec.get('explicit_order', []))} {spec.get('explicit_order')}")

    if (not unfrozen) and (not spec.get("no_total_check", False)) and "expected_total_binders" in spec:
        if len(b) != spec["expected_total_binders"]:
            fails.append(f"total binders {len(b)} != {spec['expected_total_binders']}")

    if fails:
        for f in fails:
            print("   FAIL: " + f)
    else:
        print("   PASS" + (" (instance set recorded, not enforced)" if unfrozen else ""))
    return fails, freezes

def main():
    if len(sys.argv) < 2:
        print("usage: binder_snapshot.py CAPTURE [EXPECTED.json]"); return 2
    recs, bad = load(sys.argv[1])
    exp = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "binder_expected.json"))
    if not recs:
        print("CAPTURE UNUSABLE: no records. Not a pass."); return 2
    total, freezes = 0, []
    for group in ("theorems", "definitions"):
        for key, spec in exp[group].items():
            fqn = spec["fqn"]
            via = recs.get(fqn) or recs.get(key)
            if via is None:
                print(f"\n== {key}\n   FAIL: ABSENT from capture (fail closed)"); total += 1; continue
            if via["error"]:
                print(f"\n== {key}\n   FAIL: {via['error']}"); total += 1; continue
            f, fr = check(key, via, spec)
            total += len(f); freezes += [x for x in fr]
    print(f"\nSUMMARY fails={total}")
    if freezes:
        print("UNFROZEN instance sets to paste into binder_expected.json:")
        for fr in freezes:
            print("   " + json.dumps(fr, ensure_ascii=False))
    if bad:
        print(f"malformed BINDER lines: {bad}")
    return 0 if total == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
