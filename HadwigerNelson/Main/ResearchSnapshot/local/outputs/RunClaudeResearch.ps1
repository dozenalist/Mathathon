# One bounded, tool-free research request through the user's Claude subscription.
# No credentials are copied, printed, or supplied by this runner.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$claudeRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\work\claude-supervisor'))
$claudeExe = 'C:\Users\jarom\AppData\Local\Microsoft\WinGet\Packages\Anthropic.ClaudeCode_Microsoft.Winget.Source_8wekyb3d8bbwe\claude.exe'
$claudeLock = [IO.File]::Open((Join-Path $claudeRoot 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $jobPath = Join-Path $claudeRoot 'job.json'
    $job = Get-Content -LiteralPath $jobPath -Raw | ConvertFrom-Json -AsHashtable
    if ($job.id -notmatch '^claude-[a-z0-9-]+$') { throw 'Invalid research job id.' }
    if ($job.status -ne 'queued') { throw 'Only a newly queued job may run; reconcile prior jobs first.' }
    $jobDir = [IO.Path]::GetFullPath((Join-Path $claudeRoot $job.id))
    if (-not $jobDir.StartsWith($claudeRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid job directory.' }
    $promptPath = Join-Path $jobDir 'prompt.txt'
    $promptText = [IO.File]::ReadAllText($promptPath)
    if ($promptText.Length -gt 250000) { throw 'Research packet exceeds the bounded input size.' }
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $claudeExe
    $psi.WorkingDirectory = $jobDir
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.StandardInputEncoding = [Text.UTF8Encoding]::new($false)
    $psi.StandardOutputEncoding = [Text.UTF8Encoding]::new($false)
    $psi.StandardErrorEncoding = [Text.UTF8Encoding]::new($false)
    # Use the authenticated first-party subscription, with no API/provider override.
    foreach ($name in @('ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_BASE_URL','CLAUDE_CODE_USE_BEDROCK','CLAUDE_CODE_USE_VERTEX','CLAUDE_CODE_USE_FOUNDRY')) {
        [void]$psi.Environment.Remove($name)
    }
    $effort = if ($job.effort -in @('high','max')) { $job.effort } else { 'high' }
    $timeoutSeconds = if ($job.timeoutSeconds) { [Math]::Clamp([int]$job.timeoutSeconds, 30, 900) } else { 900 }
    foreach ($arg in @('--print','--model','opus','--effort',$effort,'--output-format','stream-json','--verbose','--include-partial-messages','--no-session-persistence','--safe-mode','--restricted','--strict-mcp-config','--permission-mode','dontAsk','--tools','')) {
        $psi.ArgumentList.Add($arg)
    }
    $proc = [Diagnostics.Process]::new()
    $proc.StartInfo = $psi
    try {
        [void]$proc.Start()
        $job.status = 'running'
        $job.startedUtc = [DateTime]::UtcNow.ToString('o')
        $job.processId = $proc.Id
        $job.modelAlias = 'opus'
        $job.reasoningEffort = $effort
        $job.toolsEnabled = $false
        $job.authRoute = 'existing claude.ai subscription login'
        $job | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jobPath -Encoding utf8
        $streamPath = Join-Path $jobDir 'events.jsonl'
        [IO.File]::WriteAllText($streamPath, '')
        $outTask = $proc.StandardOutput.ReadLineAsync()
        $errTask = $proc.StandardError.ReadToEndAsync()
        $watch = [Diagnostics.Stopwatch]::StartNew()
        $writeTask = $proc.StandardInput.WriteAsync($promptText)
        $inputClosed = $false
        $outputClosed = $false
        $lastSave = 0
        $lastResult = $null
        while ($true) {
            if (-not $inputClosed -and $writeTask.IsCompleted) {
                [void]$writeTask.GetAwaiter().GetResult()
                $proc.StandardInput.Close()
                $inputClosed = $true
            }
            while (-not $outputClosed -and $outTask.IsCompleted) {
                $line = $outTask.GetAwaiter().GetResult()
                if ($null -eq $line) { $outputClosed = $true; break }
                [IO.File]::AppendAllText($streamPath, $line + "`n")
                try {
                    $event = $line | ConvertFrom-Json -AsHashtable
                    $job.lastEventType = $event.type
                    $job.lastEventUtc = [DateTime]::UtcNow.ToString('o')
                    if ($event.type -eq 'system' -and $event.model) { $job.resolvedModel = $event.model }
                    if ($event.type -eq 'result') { $lastResult = $event }
                } catch { }
                $outTask = $proc.StandardOutput.ReadLineAsync()
            }
            if ($proc.HasExited -and $outputClosed) { break }
            $proc.Refresh()
            if ($watch.Elapsed.TotalSeconds -gt $timeoutSeconds -or $proc.WorkingSet64 -gt 4GB -or (Get-Item -LiteralPath $streamPath).Length -gt 16MB) {
                $job.status = 'bounded_stop'
                $job.stopReason = if ($watch.Elapsed.TotalSeconds -gt $timeoutSeconds) { 'Configured timeout' } else { 'Memory or output cap' }
                $proc.Kill($true)
                $proc.WaitForExit()
                break
            }
            if ($watch.Elapsed.TotalSeconds - $lastSave -ge 10) {
                $job.inputDelivered = $inputClosed
                $job.processWorkingSetMiB = [Math]::Round($proc.WorkingSet64 / 1MB,1)
                $job.elapsedSeconds = [Math]::Round($watch.Elapsed.TotalSeconds,1)
                $job | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath ($jobPath + '.tmp') -Encoding utf8
                Move-Item -LiteralPath ($jobPath + '.tmp') -Destination $jobPath -Force
                $lastSave = $watch.Elapsed.TotalSeconds
            }
            [Threading.Thread]::Sleep(200)
        }
        $stderr = $errTask.GetAwaiter().GetResult()
        [IO.File]::WriteAllText((Join-Path $jobDir 'stderr.txt'), $stderr)
        $job.exitCode = $proc.ExitCode
        if ($job.status -eq 'running') { $job.status = if ($proc.ExitCode -eq 0) { 'completed' } else { 'failed' } }
        if ($proc.ExitCode -eq 0) {
            if ($null -eq $lastResult) { throw 'No completed Claude result event.' }
            $result = $lastResult
            [IO.File]::WriteAllText((Join-Path $jobDir 'response.json'), ($result | ConvertTo-Json -Depth 40))
            if ($result.is_error) { $job.status = 'model_error' }
            if ($result.result) { [IO.File]::WriteAllText((Join-Path $jobDir 'REPORT.txt'), [string]$result.result) }
            $job.actualModels = @($result.modelUsage.Keys)
            $job.usage = $result.usage
            $job.numTurns = $result.num_turns
        }
    } catch {
        if ($job.status -eq 'running' -and -not $proc.HasExited) { $proc.Kill($true); $proc.WaitForExit() }
        $job.status = 'runner_error'
        $job.errorCategory = $_.Exception.GetType().Name
    } finally {
        $job.finishedUtc = [DateTime]::UtcNow.ToString('o')
        $job | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jobPath -Encoding utf8
        Copy-Item -LiteralPath $jobPath -Destination (Join-Path $jobDir 'job.json') -Force
        $proc.Dispose()
    }
    Write-Output ('Claude research {0}: {1}. Output saved in its workspace job directory.' -f $job.id,$job.status)
} finally { $claudeLock.Dispose() }
