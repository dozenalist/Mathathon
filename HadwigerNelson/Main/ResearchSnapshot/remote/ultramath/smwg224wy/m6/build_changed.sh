#!/bin/bash
# Compile the changed/new modules of the diagnostic tree in topological order.
# Unchanged modules are taken from the already-built staged tree (statements are
# untouched: only declarations outside the headline closure were removed).
set -uo pipefail
cd "$(dirname "$0")"
REPO=../../..
source "$REPO/scripts/env4341.sh"
STAGE="$REPO/sprint/simplify/stage/lean/build/lib"
cd tree/lean
export LEAN_PATH="$PWD/build/lib:$STAGE:$LEAN_PATH"
mkdir -p build/lib
CHANGED="OAI/Analysis/PlaneSpectrum/Basic
OAI/Analysis/PlaneSpectrum/RSBase
OAI/Analysis/PlaneSpectrum/RSMeasure
OAI/Analysis/PlaneSpectrum/SmallArcs
OAI/Analysis/PlaneSpectrum/PhaseEncoding
OAI/Analysis/PlaneSpectrum/PhaseCollision
OAI/MeasureTheory/CompactFactors/ConditionalSelection
OAI/Analysis/PlaneSpectrum/ConditionalSpectrum
OAI/MeasureTheory/CompactFactors/Centers
OAI/MeasureTheory/CompactFactors/RelativeCenters
OAI/MeasureTheory/CompactFactors/Approximation
OAI/MeasureTheory/CompactFactors/ConditionalLimits
OAI/MeasureTheory/CompactFactors/Kernels
OAI/MeasureTheory/CompactFactors/Functions
OAI/MeasureTheory/CompactFactors/Factors
OAI/MeasureTheory/CompactFactors/Stationary
OAI/Analysis/PlaneSpectrum/TheoremA
OAI/Analysis/PlaneSpectrum/Ergodicity"
fail=0
for m in $CHANGED; do
  mkdir -p "build/lib/$(dirname "$m")"
  start=$(date +%s)
  if timeout 600 lean -o "build/lib/$m.olean" "$m.lean" > "build/lib/$(basename "$m").log" 2>&1; then
    echo "OK    $m  $(( $(date +%s) - start ))s"
  else
    echo "FAIL  $m  $(( $(date +%s) - start ))s"
    sed -n '1,25p' "build/lib/$(basename "$m").log"
    fail=1
  fi
done
exit $fail
