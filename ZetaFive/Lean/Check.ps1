param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$targets = @(
    'ZetaFive.Lean.Common.MomentFunctional',
    'ZetaFive.Lean.Common.Criterion',
    'ZetaFive.Lean.Common.Normalization',
    'ZetaFive.Lean.Common.SquareNodes',
    'ZetaFive.Lean.Common.AffineDeterminant',
    'ZetaFive.Lean.Common.PartialFractions',
    'ZetaFive.Lean.Common.Gram',
    'ZetaFive.Lean.Common.Andreief',
    'ZetaFive.Lean.Common.GammaIntegral',
    'ZetaFive.Lean.Common.ExponentialBounds',
    'ZetaFive.Lean.Common.Arithmetic.Val',
    'ZetaFive.Lean.Common.Arithmetic.IntPoly',
    'ZetaFive.Lean.Common.Arithmetic.Bernoulli',
    'ZetaFive.Lean.Common.Arithmetic.NaturalValuation',
    'ZetaFive.Lean.Family.Parameters',
    'ZetaFive.Lean.Family.Moments',
    'ZetaFive.Lean.Family.Specializations',
    'ZetaFive.Lean.Family.Construction',
    'ZetaFive.Lean.Family.Degree',
    'ZetaFive.Lean.Family.Weight',
    'ZetaFive.Lean.Family.WeightDerivative',
    'ZetaFive.Lean.Family.WeightBound',
    'ZetaFive.Lean.Family.PolynomialMoments',
    'ZetaFive.Lean.Family.MomentValuation',
    'ZetaFive.Lean.Family.PoleValuation',
    'ZetaFive.Lean.Family.Positivity',
    'ZetaFive.Lean.Family.DetIntegral',
    'ZetaFive.Lean.Family.AnalyticEstimates',
    'ZetaFive.Lean.Main',
    'ZetaFive'
)

Push-Location -LiteralPath $repoRoot
try {
    # Building in dependency order limits memory use on a desktop machine.
    foreach ($target in $targets) {
        & lake build $target
        if ($LASTEXITCODE -ne 0) { throw "Lean build failed: $target" }
    }
    & lake env lean ZetaFive/Lean/Audit.lean
    if ($LASTEXITCODE -ne 0) { throw 'Lean axiom audit failed.' }
} finally {
    Pop-Location
}
