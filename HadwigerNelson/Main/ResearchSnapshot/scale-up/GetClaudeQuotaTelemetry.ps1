# Read only rate-limit metadata; never print research text, reasoning, or credentials.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$claudeQuotaRoot = 'C:\Users\jarom\Documents\Codex\2026-11-13\i\work\claude-supervisor'
$job = Get-Content -LiteralPath (Join-Path $claudeQuotaRoot 'job.json') -Raw | ConvertFrom-Json
if ($job.id -notmatch '^claude-[a-z0-9-]+$') { throw 'Invalid Claude job identifier.' }
$eventPath = Join-Path $claudeQuotaRoot ($job.id + '\events.jsonl')
$rateInfo = $null
$count = 0
$eventTimestamp = $null
if (Test-Path -LiteralPath $eventPath) {
    $stream = $null
    $reader = $null
    try {
        # The research runner appends concurrently; do not deny its write access.
        $stream = [IO.File]::Open($eventPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::ReadWrite -bor [IO.FileShare]::Delete))
        $reader = [IO.StreamReader]::new($stream, [Text.Encoding]::UTF8, $true)
        while ($null -ne ($line = $reader.ReadLine())) {
            if ($line -notmatch '"type"\s*:\s*"rate_limit_event"') { continue }
            try { $event = $line | ConvertFrom-Json } catch { continue }
            if ($event.type -ne 'rate_limit_event') { continue }
            $rateInfo = $event.rate_limit_info
            $count++
            $eventTimestamp = if ($event.timestamp) { $event.timestamp } else { $null }
        }
    } finally {
        if ($null -ne $reader) { $reader.Dispose() }
        elseif ($null -ne $stream) { $stream.Dispose() }
    }
}
$windows = @()
if ($null -ne $rateInfo.unifiedWindows) {
    $windows = @($rateInfo.unifiedWindows.PSObject.Properties | ForEach-Object {
        $usedPercent = $null
        $remainingPercent = $null
        if ($null -ne $_.Value.utilization) {
            $usedPercent = 100 * [double]$_.Value.utilization
            $remainingPercent = [Math]::Clamp([double](100 - $usedPercent), [double]0, [double]100)
        }
        [ordered]@{
            window = $_.Name
            usedPercent = $usedPercent
            remainingPercent = $remainingPercent
            resetsAtUnix = $_.Value.resetsAt
            status = $_.Value.status
        }
    })
}
[ordered]@{
    readAtUtc = [DateTimeOffset]::UtcNow.ToString('o')
    provider = 'Claude'
    source = 'Existing Claude research stream rate_limit_event only'
    jobId = $job.id
    jobStatus = $job.status
    model = $job.resolvedModel
    eventCount = $count
    eventTimestamp = $eventTimestamp
    eventTimeLowerBoundUtc = $job.startedUtc
    eventTimeUpperBoundUtc = if ($job.finishedUtc) { $job.finishedUtc } else { [DateTimeOffset]::UtcNow.ToString('o') }
    freshnessRule = 'When exact event time is absent, use job start as conservative freshness bound. Repeated reads/file modification are not new provider observations.'
    status = $rateInfo.status
    isUsingOverage = $rateInfo.isUsingOverage
    windows = $windows
} | ConvertTo-Json -Depth 6
