#!/bin/bash
# one repair iteration: regenerate tree2 from sc + prune(FORCE), build, harvest new unknowns
set -u
R=/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo
cd $R
H=sprint/simplify/m10/harness
rm -rf .scratch/m10/tree2/lean/OAI
cp -a .scratch/m10/sc/lean/OAI .scratch/m10/tree2/lean/
python3 $H/apply_prune.py --tree .scratch/m10/tree2 | grep -E '!!|TOTAL'
python3 $H/linecount.py --base $H/BASELINE.json --root .scratch/m10/tree2 2>&1 | tail -2
python3 $H/hbuild.py --root .scratch/m10/tree2 --env $R/scripts/env4341.sh -j2 --timeout 700 > .scratch/m10/b.log 2>&1
echo "build rc=$?"
grep -c '^OK' .scratch/m10/b.log
grep -o 'Unknown identifier `[^`]*`' .scratch/m10/b.log | sed 's/Unknown identifier `//;s/`//' | sort -u > .scratch/m10/new_unknown.txt
echo "--- new unknowns:"; wc -l < .scratch/m10/new_unknown.txt
cat .scratch/m10/new_unknown.txt | tr '\n' ' '; echo
grep -E '^(FAIL)' .scratch/m10/b.log | wc -l
