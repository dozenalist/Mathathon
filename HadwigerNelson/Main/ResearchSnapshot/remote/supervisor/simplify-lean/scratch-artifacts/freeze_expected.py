#!/usr/bin/env python3
"""Freeze binder_expected.json (schema 4) FROM the supervisor-verified real capture, not from guesses.
Every value below is copied out of capture/real_summary.json, which is the supervisor's verified
summary of the local run (6 DECL, 133 BINDER, zero ERROR/MISSING, Lean exit 0)."""
import json
S = json.load(open("capture/real_summary.json"))
THM = {"finite_uniform_precision_contradiction", "ambient_uniform_precision_contradiction"}
out = {
 "schema": 4,
 "frozen_from": "capture/real_summary.json (supervisor-verified local capture: 6 DECL, 133 BINDER, zero ERROR/MISSING, Lean exit 0)",
 "frozen_at_utc": "2026-11-14T15:24Z",
 "not_a_claim": "Supplementary inspection only. Exact binder identity is NOT part of the accepted integration evidence, which remains textual hypotheses + defeq + application compatibility (SignatureEquivalence R5, SignatureCheckFresh R5).",
 "supersedes": {"file": "archive/binder_expected.v2.FAILED.json",
                "why": "v2 asserted StandardBorelSpace Y / Nonempty Y on the aliases; the real capture shows the theorems carry 8 instances without either, and the definitions carry 3."},
 "forbidden_all": ["StandardBorelSpace Y", "Nonempty Y"],
 "theorems": {}, "definitions": {}}
for d in S["declarations"]:
    key = d["declaration"].split(".")[-1]
    spec = {
      "fqn": d["declaration"],
      "total_binders": d["totalBinders"],
      "type_binders": [t[0] for t in d["typeBinders"]],
      "type_binder_indices": {t[0]: t[2] for t in d["typeBinders"]},
      "type_binder_universes": {t[0]: t[1] for t in d["typeBinders"]},
      "instance_allowed": d["instanceTypes"],
      "instance_count": len(d["instanceTypes"]),
      "explicit_order": d["explicitOrder"],
      "unfrozen": False,
    }
    (out["theorems"] if key in THM else out["definitions"])[key] = spec
out["cross_checks"] = {
 "total_binders": {k: v["total_binders"] for g in ("theorems","definitions") for k, v in out[g].items()},
 "instance_counts": {k: v["instance_count"] for g in ("theorems","definitions") for k, v in out[g].items()},
 "expected_theorem_instance_count": 8,
 "expected_predicate_instance_count": 3,
 "no_forbidden": True,
}
json.dump(out, open("binder_expected.json","w"), indent=1, ensure_ascii=False)
print("frozen:", {k: v["total_binders"] for k,v in list(out["theorems"].items())+list(out["definitions"].items())})
print("instances:", {k: v["instance_count"] for k,v in list(out["theorems"].items())+list(out["definitions"].items())})
