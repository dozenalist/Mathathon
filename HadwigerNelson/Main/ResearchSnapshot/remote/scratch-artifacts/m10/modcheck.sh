#!/bin/bash
# compile each module touched by the prune against the PRISTINE oleans, report errors
set -u
R=/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo
cd $R
source scripts/env4341.sh
export LEAN_PATH="$R/lean/build/lib:$LEAN_PATH"
OUT=.scratch/m10/mc.log
: > $OUT
MODS=$(python3 - <<'PY'
import json
pr = json.load(open("sprint/simplify/m10/harness/PRUNE.json"))
mods = sorted(set(v["mod"] for v in pr["drop_decls"].values()) | set(pr["drop_modules"]) | set(pr["drop_imports"]))
for m in mods: print(m)
PY
)
for m in $MODS; do
  f=".scratch/m10/tree2/lean/$(echo $m | tr '.' '/').lean"
  [ -f "$f" ] || { echo "SKIP $m (deleted)" >> $OUT; continue; }
  if timeout 400 lean "$f" >> $OUT 2>&1; then echo "OK   $m" >> $OUT; else echo "FAIL $m" >> $OUT; fi
done
grep -c '^OK' $OUT; grep -c '^FAIL' $OUT
grep -o 'Unknown identifier `[^`]*`' $OUT | sort -u | tr '\n' ' '; echo
