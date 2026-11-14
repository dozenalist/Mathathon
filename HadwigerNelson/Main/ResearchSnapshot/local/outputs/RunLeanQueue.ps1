# Serial, workspace-scoped Lean checks. Does not install or change toolchains.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$queueRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\work\lean-queue'))
$queuePath = Join-Path $queueRoot 'queue.json'
$lockStream = $null
try {
    try {
        $lockStream = [IO.File]::Open((Join-Path $queueRoot 'queue.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
    } catch {
        throw ('Cannot acquire the Lean queue lock; no job started. {0}' -f $_.Exception.Message)
    }
    $queue = Get-Content -LiteralPath $queuePath -Raw | ConvertFrom-Json -AsHashtable
    if ($queue.maxParallel -ne 1) { throw 'Only serial execution is supported.' }
    if (@($queue.jobs | Where-Object { $_.status -eq 'running' }).Count) {
        throw 'A previous job is marked running. Reconcile its process/log before retrying.'
    }
    foreach ($job in $queue.jobs) {
        if ($job.status -ne 'queued') { continue }
        if ($job.dependsOn) {
            $dependency = @($queue.jobs | Where-Object { $_.id -eq $job.dependsOn })
            if ($dependency.Count -ne 1 -or $dependency[0].status -ne 'passed') {
                $job.status = 'blocked_dependency'
                $job.error = 'Required preceding module did not pass; no process started.'
                $queue | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $queuePath -Encoding utf8
                continue
            }
        }
        if ($job.id -notmatch '^[a-z0-9][a-z0-9-]*$') { throw 'Invalid job id.' }
        $sourcePath = [IO.Path]::GetFullPath((Join-Path $queueRoot $job.source))
        $rootPrefix = $queueRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
        if (-not $sourcePath.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($sourcePath) -ne '.lean') {
            throw 'Lean source must be a .lean file inside the queue workspace.'
        }
        if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) { throw 'Queued source is missing.' }
        if (-not (Test-Path -LiteralPath $job.leanExe -PathType Leaf)) { throw 'Selected Lean executable is missing.' }
        $versionText = (& $job.leanExe --version | Out-String).Trim()
        if ($LASTEXITCODE -ne 0 -or $versionText -notmatch ([regex]::Escape($job.expectedVersion) + '(?:\D|$)')) {
            throw 'Installed Lean version does not match this job.'
        }
        if ($job.expectedCommit -and -not $versionText.Contains($job.expectedCommit)) { throw 'Lean commit does not match this job.' }
        if ($job.mathlibRoot -and $job.requiredMathlib) {
            $actualMathlib = (& git -C $job.mathlibRoot rev-parse HEAD | Out-String).Trim()
            if ($LASTEXITCODE -ne 0 -or $actualMathlib -ne $job.requiredMathlib) { throw 'Mathlib checkout does not match the queued revision.' }
            $job.actualMathlib = $actualMathlib
        }
        $job.sourceSha256 = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($job.expectedSourceSha256 -and $job.sourceSha256 -ne $job.expectedSourceSha256) { throw 'Source does not match the frozen job revision.' }
        $jobWorkingDirectory = $queueRoot
        if ($job.workingDirectory) {
            $jobWorkingDirectory = [IO.Path]::GetFullPath((Join-Path $queueRoot $job.workingDirectory))
            if (-not $jobWorkingDirectory.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase) -or -not (Test-Path -LiteralPath $jobWorkingDirectory -PathType Container)) { throw 'Working directory must exist inside the queue workspace.' }
        }
        $outputPath = Join-Path $queueRoot ($job.id + '.olean')
        if ($job.output) {
            $outputPath = [IO.Path]::GetFullPath((Join-Path $queueRoot $job.output))
            if (-not $outputPath.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($outputPath) -ne '.olean') { throw 'Compiled output must stay inside the queue workspace.' }
            [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($outputPath))
        }
        $job.actualVersion = $versionText
        $job.status = 'running'
        $job.startedUtc = [DateTime]::UtcNow.ToString('o')
        $queue | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $queuePath -Encoding utf8
        $procInfo = [Diagnostics.ProcessStartInfo]::new()
        $procInfo.FileName = $job.leanExe
        $procInfo.WorkingDirectory = $jobWorkingDirectory
        $procInfo.UseShellExecute = $false
        $procInfo.CreateNoWindow = $true
        $procInfo.RedirectStandardOutput = $true
        $procInfo.RedirectStandardError = $true
        $procInfo.Environment['LEAN_NUM_THREADS'] = '1'
        if ($job.leanPath) { $procInfo.Environment['LEAN_PATH'] = $job.leanPath }
        else { [void]$procInfo.Environment.Remove('LEAN_PATH') }
        $procInfo.ArgumentList.Add('-o')
        $procInfo.ArgumentList.Add($outputPath)
        $procInfo.ArgumentList.Add($sourcePath)
        $proc = [Diagnostics.Process]::new()
        $proc.StartInfo = $procInfo
        $started = $false
        try {
            [void]$proc.Start()
            $started = $true
            $job.processId = $proc.Id
            $queue | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $queuePath -Encoding utf8
            $stdoutTask = $proc.StandardOutput.ReadToEndAsync()
            $stderrTask = $proc.StandardError.ReadToEndAsync()
            $timeoutMs = [Math]::Clamp([int]$job.timeoutSeconds, 10, 900) * 1000
            if (-not $proc.WaitForExit($timeoutMs)) {
                $proc.Kill($true)
                $proc.WaitForExit()
                $job.status = 'timeout'
            } else {
                $job.status = if ($proc.ExitCode -eq 0) { 'passed' } else { 'failed' }
            }
            $job.exitCode = $proc.ExitCode
            $stdoutText = $stdoutTask.GetAwaiter().GetResult()
            $stderrText = $stderrTask.GetAwaiter().GetResult()
            $logText = "Version: $versionText`nSource SHA256: $($job.sourceSha256)`nStatus: $($job.status)`nExit code: $($job.exitCode)`n`nSTDOUT`n$stdoutText`nSTDERR`n$stderrText"
            $logText | Set-Content -LiteralPath (Join-Path $queueRoot ($job.id + '.log')) -Encoding utf8
        } catch {
            if ($started -and -not $proc.HasExited) { $proc.Kill($true); $proc.WaitForExit() }
            $job.status = 'runner_error'
            $job.error = $_.Exception.Message
        } finally {
            $proc.Dispose()
            $job.finishedUtc = [DateTime]::UtcNow.ToString('o')
            $queue | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $queuePath -Encoding utf8
        }
        Write-Output ("{0}: {1}" -f $job.id, $job.status)
    }
} finally {
    if ($null -ne $lockStream) { $lockStream.Dispose() }
}
