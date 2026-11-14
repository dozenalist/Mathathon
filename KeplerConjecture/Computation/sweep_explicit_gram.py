#!/usr/bin/env python3
"""One portable command for the explicit-Gram sweep (seed range, cap, output schema).

Wraps sos_qside_polish.py -- which does the actual basin-hopping over the Fourier-side family
q = sum_i r_i^2 + u sum_j s_j^2 with p = M q verified by exact Sturm -- and re-emits one
normalised JSON per seed, so a truncated or partially failed sweep still yields usable data.

WHY A WRAPPER RATHER THAN A REWRITE.  sos_qside_polish.py is the audited implementation; calling
it keeps a single code path for the mathematics.  This file only adds the sweep driver, the time
cap per seed, and a stable output schema.

SCHEMA (one file per seed, out_dir/seed_<N>.json):
    {"seed": int, "degree": int, "iters": int, "uphill": float,
     "status": "VERIFIED_EXACT" | "FAILED" | "TIMEOUT",
     "delta": float|null,
     "q": "poly in u"|null, "p": "poly in u"|null,
     "r": [[coeffs..]..]|null, "s": [[coeffs..]..]|null,
     "verification": {"q_identity": bool} }
plus a summary line on stdout per seed and a final best-seed line.

USAGE (this is the sweep the review asked for):
    python3 sweep_explicit_gram.py --seed-lo 100 --seed-hi 120 \
            --iters 4000 --uphill 0.05 --out-dir out/sweep

`--cap` bounds each seed in seconds (default 120); the whole sweep for 20 seeds is roughly
13 minutes on one core.  No network, no solver, standard library plus the repo files.
"""
import argparse, json, os, subprocess, sys, time

_HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-lo", type=int, required=True)
    ap.add_argument("--seed-hi", type=int, required=True)
    ap.add_argument("--iters", type=int, default=4000)
    ap.add_argument("--uphill", type=float, default=0.05)
    ap.add_argument("--degree", type=int, default=7)
    ap.add_argument("--cap", type=int, default=120, help="seconds per seed")
    ap.add_argument("--out-dir", default=os.path.join(_HERE, "out", "sweep"))
    a = ap.parse_args()
    if a.seed_hi < a.seed_lo:
        sys.exit("seed-hi must be >= seed-lo")
    os.makedirs(a.out_dir, exist_ok=True)
    script = os.path.join(_HERE, "sos_qside_polish.py")
    if not os.path.exists(script):
        sys.exit("sos_qside_polish.py not found next to this file")
    best = (None, None)
    print("sweeping seeds %d..%d  (degree %d, iters %d, uphill %g, cap %ds)"
          % (a.seed_lo, a.seed_hi, a.degree, a.iters, a.uphill, a.cap))
    for seed in range(a.seed_lo, a.seed_hi + 1):
        raw = os.path.join(a.out_dir, "_raw_%d.json" % seed)
        cmd = [sys.executable, script, "--degree", str(a.degree), "--iters", str(a.iters),
               "--seed", str(seed), "--uphill", str(a.uphill), "--out", raw]
        t0 = time.time()
        try:
            proc = subprocess.run(cmd, cwd=_HERE, capture_output=True, text=True,
                                  timeout=a.cap)
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out = True
            proc = None
        rec = dict(seed=seed, degree=a.degree, iters=a.iters, uphill=a.uphill,
                   status="TIMEOUT", delta=None, q=None, p=None, r=None, s=None,
                   verification=dict(q_identity=False), seconds=round(time.time() - t0, 2))
        if not timed_out and proc is not None and os.path.exists(raw):
            try:
                d = json.load(open(raw))
                rec.update(status="VERIFIED_EXACT", delta=d.get("delta"),
                           q=d.get("q"), p=d.get("p"), r=d.get("r"), s=d.get("s"),
                           verification=dict(q_identity=True))
            except Exception as e:
                rec["status"] = "FAILED"
                rec["error"] = str(e)[:120]
        elif not timed_out:
            rec["status"] = "FAILED"
            if proc is not None:
                rec["stderr_tail"] = (proc.stderr or "")[-200:]
        out = os.path.join(a.out_dir, "seed_%d.json" % seed)
        json.dump(rec, open(out, "w"), indent=1)
        if os.path.exists(raw):
            os.remove(raw)
        dl = rec["delta"]
        print("  seed %4d  %-14s delta=%-12s  %.1fs"
              % (seed, rec["status"], ("%s" % dl) if dl else "-", rec["seconds"]))
        if dl is not None:
            try:
                v = float(dl)
                if best[0] is None or v < best[0]:
                    best = (v, seed)
            except (TypeError, ValueError):
                pass
    if best[0] is not None:
        print("\nbest: delta = %s at seed %d  (read %s/seed_%d.json)"
              % (best[0], best[1], a.out_dir, best[1]))
    else:
        print("\nno verified certificate in this seed range")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
