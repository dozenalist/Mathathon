#!/bin/bash
# Rebuild the diagnostic tree from the pristine copy:
#   staged tree  -  362 declarations (5820 lines) no longer needed once
#   `ergodic_wild_fourier` is proved from `TerminalObligation`
#   + m5's Theorem A as real OAI modules (RSBase / RSMeasure / TheoremA)
#   + one diagnostic axiom `terminalObligation_diagnostic`.
set -euo pipefail
cd "$(dirname "$0")"
M=../../smwfoekgk/m5/work
T=tree/lean/OAI/Analysis/PlaneSpectrum
rm -rf tree
cp -r tree-pristine tree
python3 ../../../sprint/simplify/m10/harness/apply_prune.py --tree tree --prune PRUNE8.json > apply.log
cp "$M/A.lean" "$T/RSBase.lean"
cp "$M/B.lean" "$T/RSMeasure.lean"
sed -i 's|^import A$|import OAI.Analysis.PlaneSpectrum.RSBase|' "$T/RSMeasure.lean"
{ printf 'import OAI.Analysis.PlaneSpectrum.RSBase\nimport OAI.Analysis.PlaneSpectrum.RSMeasure\nimport OAI.Analysis.PlaneSpectrum.RadialEnergy\nimport OAI.Analysis.PlaneSpectrum.DifferenceLaw\nimport OAI.MeasureTheory.CompactFactors.DifferenceInvariant\nimport OAI.Analysis.PlaneSpectrum.SpectralMeasure\n'
  tail -n +3 "$M/C.lean"; } > "$T/TheoremA.lean"
python3 patch_ergodicity.py
python3 fix_omit.py
echo "tree rebuilt: $(find tree -name '*.lean' | wc -l) modules, $(find tree -name '*.lean' -exec cat {} + | wc -l) lines"
