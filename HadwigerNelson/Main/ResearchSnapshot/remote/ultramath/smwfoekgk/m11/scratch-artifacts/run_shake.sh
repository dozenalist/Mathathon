#!/bin/bash
source ./env4341.sh
run_one() { f="$1"; b=$(basename "$f"); lean "$f" > ".scratch/shake_out/$b.out" 2>&1; echo "done $b"; }
export -f run_one
ls .scratch/shk/*.lean | xargs -P 2 -I{} bash -c 'source ./env4341.sh; lean "{}" > ".scratch/shake_out/$(basename {}).out" 2>&1; echo done $(basename {})'
