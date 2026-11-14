# Read-only quota snapshot. Does not use or modify the research supervisor queue.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
. 'C:\Users\jarom\Documents\Codex\2026-11-13\i\outputs\OpenMath.ps1'
try {
    $usage = Invoke-OpenMathPlatform -Operation 'org_model_usage' -Body @{ team = 'o-67dc4eac-a86a-439c-9459-ef86c31aeaa7' }
    $windows = @($usage.windows | ForEach-Object {
        $remaining = $null
        if ($null -ne $_.limit_usd -and [double]$_.limit_usd -gt 0 -and $null -ne $_.spent_usd) {
            $remaining = [Math]::Clamp([double](100 * (1 - [double]$_.spent_usd / [double]$_.limit_usd)), [double]0, [double]100)
        }
        [ordered]@{
            window = $_.window
            limitUsd = $_.limit_usd
            spentUsd = $_.spent_usd
            remainingPercent = $remaining
            resetsAt = $_.resets_at
        }
    })
    [ordered]@{
        observedUtc = [DateTimeOffset]::UtcNow.ToString('o')
        provider = 'Open Math OS'
        scope = 'Team model-usage accounting; not an isolated chat cost or proof of UI limit semantics'
        windows = $windows
    } | ConvertTo-Json -Depth 6
} catch {
    # The reviewed helper suppresses raw request, server-body and credential data.
    [ordered]@{
        observedUtc = [DateTimeOffset]::UtcNow.ToString('o')
        provider = 'Open Math OS'
        available = $false
        error = 'Could not retrieve a fresh quota snapshot; do not interpret missing data as zero usage.'
        errorCategory = $_.Exception.GetType().Name
    } | ConvertTo-Json -Depth 3
    exit 1
}
