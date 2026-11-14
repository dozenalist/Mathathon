#!/usr/bin/env python3
"""Comparator v4 for a BinderAudit.lean capture. Supplementary inspection only.

Hardened after the supervisor's review of v3, on four named defects:
  H1  `setdefault` after an ERROR could leave an existing record's error unset -> the error markers
      are now written UNCONDITIONALLY, and appending a binder never clears a recorded error.
  H2  malformed records did not reliably fail -> every malformed line is a FAIL and is counted.
  H3  extra implicit VALUE binders were only labelled -> they are now a FAIL.
  H4  instance membership is not multiplicity -> instance lists are compared as multisets (Counter),
      so a duplicated or an omitted instance fails even when the set looks right.
Also: type binder NAMES and INDICES are both checked, the explicit sequence must match exactly, the
total binder count must match, and each declaration must report the expected number of instances.

VALIDITY: a capture is evidence only if `lean` reported no error for BinderAudit.lean. Lean leaves
placeholders after elaboration errors, so a green parse can hide an audit that never ran.
SYNTHETIC captures exercise this script only; they say nothing about the OAI tree.

Exit: 0 all pass; 1 any FAIL; 2 capture unusable.
"""
import json, sys
from collections import Counter

def norm(s):
    return " ".join(s.split())

def load(path):
    recs, malformed = {}, []
    def rec(decl):
        # H1: create once; never overwrite an existing record (and never clear its error).
        return recs.setdefault(decl, {"binders": [], "error": None})
    for n, raw in enumerate(open(path, errors="ignore"), 1):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if line.startswith("BINDER "):
            parts = line.split(" ", 5)
            if len(parts) < 6:
                malformed.append((n, "BINDER with < 6 fields")); continue
            _, decl, i, nm, info, ty = parts
            if not i.isdigit():
                malformed.append((n, "BINDER index not an integer")); continue
            if info not in ("explicit", "implicit", "strict", "instance"):
                malformed.append((n, f"unknown binder kind {info!r}")); continue
            r = rec(decl)                      # H1: keeps any error already recorded
            r["binders"].append({"i": int(i), "name": nm, "info": info, "type": norm(ty)})
        elif line.startswith("DECL "):
            parts = line.split(" ", 2)
            if len(parts) < 2:
                malformed.append((n, "DECL with no name")); continue
            rec(parts[1])                      # H1: register, keep any error already seen
        elif line.startswith("MISSING "):
            recs.setdefault(line.split(" ", 1)[1].strip(), {"binders": [], "error": None})["error"] = "MISSING"
        elif line.startswith("ERROR "):
            d, msg = (line[6:].split(" ", 1) + [""])[:2]
            recs.setdefault(d.strip(), {"binders": [], "error": None})["error"] = "ERROR " + msg
        else:
            malformed.append((n, f"unrecognised line {line[:40]!r}"))
    return recs, malformed

def check(key, via, spec, forbidden_all):
    fails = []
    b = sorted(via["binders"], key=lambda x: x["i"])
    allowed = spec["instance_allowed"]; forbidden = list(forbidden_all) + list(spec.get("instance_forbidden", []))
    print(f"\n== {key}   [frozen: {spec['total_binders']} binders, {spec['instance_count']} instances]")
    for x in b:
        tag = ""
        if x["info"] == "instance" and x["type"] in forbidden: tag = "  <-- FORBIDDEN"
        elif x["info"] == "instance" and x["type"] not in allowed: tag = "  <-- UNKNOWN INSTANCE"
        elif x["info"] == "strict": tag = "  <-- STRICT"
        elif x["info"] == "implicit" and not x["type"].startswith("Type"): tag = "  <-- EXTRA IMPLICIT (value)"
        print(f"   [{x['i']:>2}] {x['name']:<12} {x['info']:<9} {x['type']}{tag}")

    # indices must be 0..n-1 with no gap or repeat
    if [x["i"] for x in b] != list(range(len(b))):
        fails.append("binder indices are not consecutive 0..n-1")

    # type binders: name, index and universe for each expected entry
    want = spec["type_binders"]; widx = spec["type_binder_indices"]; wuniv = spec["type_binder_universes"]
    got_t = {x["name"]: x for x in b if x["info"] == "implicit" and x["type"].startswith("Type")}
    if sorted(got_t) != sorted(want):
        fails.append(f"type binders {sorted(got_t)} != {sorted(want)}")
    for nme in want:
        if nme in got_t:
            if got_t[nme]["i"] != widx[nme]:
                fails.append(f"type binder {nme} at index {got_t[nme]['i']}, expected {widx[nme]}")
            if norm(got_t[nme]["type"]) != norm(wuniv[nme]):
                fails.append(f"type binder {nme} universe {got_t[nme]['type']!r} != {wuniv[nme]!r}")

    # H3: any implicit binder that is not one of the expected type binders is a FAIL
    for x in b:
        if x["info"] == "implicit" and x["name"] not in want:
            fails.append(f"EXTRA IMPLICIT BINDER {x['name']} : {x['type']}")

    # H4: multiset comparison of instances
    insts = [x["type"] for x in b if x["info"] == "instance"]
    if Counter(insts) != Counter(allowed):
        for t, c in (Counter(insts) - Counter(allowed)).items():
            fails.append(f"UNKNOWN/EXTRA INSTANCE {t} (x{c})")
        for t, c in (Counter(allowed) - Counter(insts)).items():
            fails.append(f"ABSENT INSTANCE {t} (x{c})")
    if len(insts) != spec["instance_count"]:
        fails.append(f"instance count {len(insts)} != {spec['instance_count']}")
    for f in forbidden:
        if f in insts:
            fails.append(f"FORBIDDEN instance present: {f}")

    strict = [x["name"] for x in b if x["info"] == "strict"]
    if strict:
        fails.append(f"strict-implicit binders present: {strict}")

    expl = [x["name"] for x in b if x["info"] == "explicit"]
    if expl != spec["explicit_order"]:
        fails.append(f"explicit sequence mismatch: got {len(expl)} want {len(spec['explicit_order'])}")

    if len(b) != spec["total_binders"]:
        fails.append(f"total binders {len(b)} != {spec['total_binders']}")

    print("   PASS" if not fails else "   FAIL:\n     - " + "\n     - ".join(fails))
    return fails

def main():
    if len(sys.argv) < 2:
        print("usage: binder_snapshot.py CAPTURE [EXPECTED.json]"); return 2
    recs, malformed = load(sys.argv[1])
    exp = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "binder_expected.json"))
    if not recs:
        print("CAPTURE UNUSABLE: no DECL/BINDER/MISSING/ERROR records. Not a pass."); return 2
    total = 0
    # H2: malformed input is a failure, not a footnote
    for n, why in malformed:
        print(f"MALFORMED line {n}: {why}"); total += 1
    for group in ("theorems", "definitions"):
        for key, spec in exp[group].items():
            via = recs.get(spec["fqn"]) or recs.get(key)
            if via is None:
                print(f"\n== {key}\n   FAIL: ABSENT from capture (fail closed)"); total += 1; continue
            if via["error"]:
                print(f"\n== {key}\n   FAIL: {via['error']}"); total += 1; continue
            total += len(check(key, via, spec, exp["forbidden_all"]))
    print(f"\nSUMMARY fails={total}  malformed={len(malformed)}")
    return 0 if total == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
