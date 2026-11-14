#Requires -Version 5.1
[CmdletBinding()]
param([string]$Watcher)

$ErrorActionPreference = 'Stop'
if (!$Watcher) { $Watcher = Join-Path (Split-Path $PSScriptRoot -Parent) 'Watch-Sair.ps1' }
$Watcher = (Resolve-Path -LiteralPath $Watcher).Path
$parseErrors = $null
$null = [Management.Automation.Language.Parser]::ParseFile($Watcher, [ref]$null, [ref]$parseErrors)
if ($parseErrors) { throw ($parseErrors | Out-String) }

$temporaryRoot = [IO.Path]::GetTempPath()
$testRoot = Join-Path $temporaryRoot ('sair-watcher-test-' + [Guid]::NewGuid().ToString('N'))
$null = New-Item -ItemType Directory -Path $testRoot
$jobs = @()
$heldLocks = @()

function Assert-Condition {
    param([bool]$Condition, [string]$Message)
    if (!$Condition) { throw $Message }
}

# Each job has its own PowerShell process and receives the same mixed event feed.
# Both HTTP and Codex are mocked, so this suite sends no research prompts or wakes.
$worker = {
    param($WatcherPath, $RunDirectory, $ThreadId, $SessionId, $Mode, $SharedKeyFile)
    $ErrorActionPreference = 'Stop'
    $null = New-Item -ItemType Directory -Path $RunDirectory -Force
    $fixture = @{
        stage = -1
        mirroredReads = 0
        sends = 0
        creates = 0
        wakes = @()
        reports = @()
        transientErrors = 0
    }
    $stateFile = Join-Path $RunDirectory 'state.json'
    $stopFile = Join-Path $RunDirectory 'STOP'
    $expectedWakes = if ($Mode -in @('Resume', 'SendExisting')) { 1 } else { 2 }
    $env:SAIR_PLATFORM_API_KEY = 'nuc_oc_mock_for_tests'

    if ($Mode -eq 'Resume') {
        @{
            codex_thread = $ThreadId
            team_name = 'Test Team'
            project_name = 'Test Project'
            target = @{team='team-test';project='project-test';session=$SessionId}
            last_queued_sequence = 6
            last_completion_event = 100
        } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $stateFile -Encoding UTF8
    }

    function codex {
        $fixture.wakes += ,$args
        $global:LASTEXITCODE = 0
        $current = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
        if ($current.last_report) {
            $fixture.reports += Get-Content -LiteralPath $current.last_report -Raw | ConvertFrom-Json
        }
        if ($fixture.wakes.Count -eq $expectedWakes) { Set-Content -LiteralPath $stopFile -Value 'Finished test' }
    }

    function Start-Sleep {
        param($Seconds)
        if ($Mode -eq 'StopDuringRetry') { Set-Content -LiteralPath $stopFile -Value 'Stop during outage' }
    }

    function Throw-GatewayError {
        $exception = New-Object System.Exception 'Mock gateway failure'
        $exception | Add-Member -NotePropertyName Response -NotePropertyValue ([pscustomobject]@{StatusCode=502})
        $errorRecord = New-Object Management.Automation.ErrorRecord($exception, 'Mock502', 'ConnectionError', $null)
        $errorRecord.ErrorDetails = New-Object Management.Automation.ErrorDetails('error code: 502')
        throw $errorRecord
    }

    function Invoke-RestMethod {
        param($Method, $Uri, $Headers, $ContentType, $Body, $TimeoutSec, $MaximumRedirection, [switch]$UseBasicParsing)
        if ($Headers.Authorization -ne 'Bearer nuc_oc_mock_for_tests') { throw 'Wrong mock credential.' }
        $request = $Body | ConvertFrom-Json
        if ($Uri.EndsWith('/orgs') -and $Mode -in @('TransientRead', 'StopDuringRetry') -and $fixture.transientErrors -lt 6) {
            if ($fixture.transientErrors -gt 0) {
                $retryState = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
                if ($retryState.status -ne 'retrying') { throw 'Transient retry state was not saved.' }
            }
            $fixture.transientErrors++
            Throw-GatewayError
        }
        switch ($Uri.Split('/')[-1]) {
            'orgs' { @{orgs=@(@{name='Test Team';id='team-test'})} }
            'org_projects' { @{projects=@(@{display_name='Test Project';name='project-test';state='active'})} }
            'project_sessions' { @{sessions=@(@{session=$SessionId;title='Test coordinator'})} }
            'chat_create' {
                $fixture.creates++
                @{project='project-test';session=$SessionId}
            }
            'chat_say' {
                $fixture.sends++
                if ($Mode -eq 'SendFailure') { Throw-GatewayError }
                if ($fixture.stage -ne 0) { throw 'The completion cursor was not captured before sending.' }
                if ($request.project -cne 'project-test' -or $request.session -cne $SessionId) { throw 'Wrong send target.' }
                if ($request.text -ne 'Bounded mock research' -or $request.model -ne 'mock-model' -or $request.reasoning_effort -ne 'high') { throw 'Incorrect prompt/model arguments.' }
                if ($request.PSObject.Properties.Name -contains 'after') { throw 'Pagination mutated the send target.' }
                @{message_id='mock-message'}
            }
            'chat_changes' {
                $fixture.stage++
                switch ($fixture.stage) {
                    0 { @{cursor='baseline';reset=$false;completions=@()} }
                    1 { @{cursor='streaming';reset=$false;chats=@(@('project-test',$SessionId));completions=@()} }
                    2 {
                        @{
                            cursor='unrelated';reset=$false
                            completions=@(
                                @('other-project',$SessionId,10),
                                @('project-test','another-session',20),
                                @('PROJECT-TEST',$SessionId,30),
                                @('project-test',$SessionId.ToUpperInvariant(),40)
                            )
                        }
                    }
                    3 { @{cursor='first';reset=$false;completions=@(@('project-test','alpha',100),@('project-test','beta',100))} }
                    4 { @{cursor='duplicate';reset=$false;completions=@(@('project-test','alpha',100),@('project-test','beta',100))} }
                    5 { @{cursor='reset';reset=$true;completions=@()} }
                    default { throw 'Unexpected extra completion poll.' }
                }
            }
            'session_history' {
                if ($request.project -cne 'project-test' -or $request.session -cne $SessionId) { throw 'Fetched an unrelated transcript.' }
                if ($null -eq $request.after) {
                    @{records=@(@{seq=0;kind='user';text='Fixture'});next=0}
                } else {
                    if ($request.after -ne 0) { throw 'Incorrect pagination cursor.' }
                    $completedRecords = @()
                    if ($fixture.stage -ge 3) { $fixture.mirroredReads++ }
                    if ($Mode -in @('Resume', 'SendExisting') -or ($fixture.stage -ge 3 -and $fixture.mirroredReads -ge 3)) {
                        $completedRecords += @{seq=5;kind='assistant';text='First result'}
                        $completedRecords += @{seq=6;kind='turn_complete';at_ms=100}
                    }
                    if ($fixture.stage -ge 5 -or ($Mode -eq 'SendExisting' -and $fixture.stage -ge 3)) {
                        $completedRecords += @{seq=12;kind='assistant';text='Second result'}
                        $completedRecords += @{seq=14;kind='turn_complete';at_ms=200}
                    }
                    @{records=$completedRecords}
                }
            }
            default { throw 'Unexpected mock API operation.' }
        }
    }

    $parameters = @{
        CodexThreadId=$ThreadId
        Team='Test Team'
        Project='Test Project'
        OutputDirectory=$RunDirectory
        Continuous=$true
        TimeoutHours=1
    }
    if ($SharedKeyFile) {
        Remove-Item Env:SAIR_PLATFORM_API_KEY
        $parameters.ApiKeyFile = $SharedKeyFile
    }
    if ($Mode -ne 'New') { $parameters.Session = $SessionId }
    if ($Mode -in @('New', 'SendExisting', 'SendFailure')) {
        $parameters.Prompt = 'Bounded mock research'
        $parameters.Model = 'mock-model'
        $parameters.ReasoningEffort = 'high'
    }
    $caughtError = $null
    $bindingError = $false
    try {
        if ($Mode -eq 'Positional') { & $WatcherPath @parameters 'unexpected-input' 6>$null }
        else { & $WatcherPath @parameters 6>$null }
    } catch {
        $caughtError = $_.Exception.Message
        $bindingError = $_.Exception -is [Management.Automation.ParameterBindingException]
    }

    if ($Mode -eq 'Positional') {
        if (!$bindingError -or $fixture.wakes.Count -ne 0 -or $fixture.sends -ne 0 -or $fixture.creates -ne 0) {
            throw 'Unexpected positional input was not rejected before side effects.'
        }
        [pscustomobject]@{Case=$Mode;Passed=$true}
        return
    }

    if ($Mode -eq 'SendFailure') {
        if ($caughtError -ne 'SAIR chat_say returned HTTP 502.' -or $fixture.sends -ne 1 -or $fixture.creates -ne 0) {
            throw 'An uncertain send was retried or its non-JSON HTTP error was lost.'
        }
        [pscustomobject]@{Case=$Mode;Passed=$true}
        return
    }
    if ($Mode -eq 'StopDuringRetry') {
        $stoppedState = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
        if ($caughtError -or $stoppedState.status -ne 'stopped' -or $fixture.transientErrors -ne 1 -or $fixture.wakes.Count -ne 0) {
            throw 'Stopping during an outage failed or caused an unwanted callback.'
        }
        [pscustomobject]@{Case=$Mode;Passed=$true}
        return
    }
    if ($Mode -eq 'TransientRead' -and $fixture.transientErrors -ne 6) { throw 'Extended outage recovery was not exercised.' }

    if ($Mode -eq 'Locked') {
        if ($caughtError -notlike 'Another watcher already owns*' -or $fixture.wakes.Count -ne 0 -or $fixture.sends -ne 0) {
            throw 'A duplicate watcher was not rejected before sending or waking.'
        }
        [pscustomobject]@{Case=$Mode;Passed=$true}
        return
    }
    if ($caughtError) { throw $caughtError }
    if ($env:SAIR_PLATFORM_API_KEY) { throw 'The key remained in the child environment.' }
    if ($fixture.wakes.Count -ne $expectedWakes) { throw 'Incorrect wake count.' }
    foreach ($wake in $fixture.wakes) {
        if ($wake[0] -ne 'queue' -or $wake[2] -ne $ThreadId -or $wake[3] -ne '--resume') { throw 'Callback went to the wrong supervisor.' }
    }
    foreach ($report in $fixture.reports) {
        if ($report.target.team -cne 'team-test' -or $report.target.project -cne 'project-test' -or
            $report.target.session -cne $SessionId -or $report.codex_thread -ne $ThreadId) { throw 'Report target mismatch.' }
        if (@($report.records).Count -lt 3) { throw 'Incomplete transcript pagination.' }
    }
    $state = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
    if ($state.last_queued_sequence -ne 14 -or $state.status -ne 'stopped') { throw 'Incorrect persisted completion or stop state.' }
    $expectedSends = if ($Mode -in @('New', 'SendExisting')) { 1 } else { 0 }
    $expectedCreates = if ($Mode -eq 'New') { 1 } else { 0 }
    if ($fixture.sends -ne $expectedSends -or $fixture.creates -ne $expectedCreates) { throw 'Unexpected chat creation or prompt.' }
    [pscustomobject]@{Case=$Mode;Session=$SessionId;Supervisor=$ThreadId;Wakes=$fixture.wakes.Count;Passed=$true}
}

function Hold-TestLock {
    param([string]$Identity)
    $hash = [Security.Cryptography.SHA256]::Create()
    try { $digest = [BitConverter]::ToString($hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($Identity))).Replace('-', '') }
    finally { $hash.Dispose() }
    $mutex = New-Object System.Threading.Mutex($false, "Local\Mathathon.WatchSair.$digest")
    if (!$mutex.WaitOne(0)) { throw 'Test lock is unexpectedly occupied.' }
    return $mutex
}

try {
    $threadA = [Guid]::NewGuid().ToString()
    $threadB = [Guid]::NewGuid().ToString()
    $sharedKeyFile = Join-Path $testRoot 'mock-key.clixml'
    ConvertTo-SecureString 'nuc_oc_mock_for_tests' -AsPlainText -Force | Export-Clixml -LiteralPath $sharedKeyFile
    $jobs += Start-Job -ScriptBlock $worker -ArgumentList $Watcher,(Join-Path $testRoot 'alpha'),$threadA,'alpha','Attach',$sharedKeyFile
    $jobs += Start-Job -ScriptBlock $worker -ArgumentList $Watcher,(Join-Path $testRoot 'beta'),$threadB,'beta','Attach',$sharedKeyFile
    $finished = @($jobs | Wait-Job -Timeout 45)
    Assert-Condition ($finished.Count -eq 2) 'Concurrent watcher tests timed out.'
    $results = @($jobs | Receive-Job -ErrorAction Stop)
    Assert-Condition (@($results | Where-Object Passed).Count -eq 2) 'Concurrent watcher isolation failed.'
    $results | Format-Table -AutoSize

    foreach ($mode in @('New', 'SendExisting', 'Resume', 'Positional', 'TransientRead', 'StopDuringRetry', 'SendFailure')) {
        & $worker $Watcher (Join-Path $testRoot $mode) $threadA 'alpha' $mode | Format-Table -AutoSize
    }

    $heldLocks += Hold-TestLock ('chat|team-test|project-test|alpha|' + $threadA)
    $duplicateJob = Start-Job -ScriptBlock $worker -ArgumentList $Watcher,(Join-Path $testRoot 'duplicate'),$threadA,'alpha','Locked'
    $jobs += $duplicateJob
    $null = $duplicateJob | Wait-Job -Timeout 30
    $duplicateResult = @($duplicateJob | Receive-Job -ErrorAction Stop)
    Assert-Condition ($duplicateResult.Count -eq 1 -and $duplicateResult[0].Passed) 'Duplicate chat watcher lock failed.'

    $collisionDirectory = Join-Path $testRoot 'state-collision'
    $collisionState = [IO.Path]::GetFullPath((Join-Path $collisionDirectory 'state.json'))
    $heldLocks += Hold-TestLock ('file|' + $collisionState.ToLowerInvariant())
    $collisionJob = Start-Job -ScriptBlock $worker -ArgumentList $Watcher,$collisionDirectory,$threadB,'beta','Locked'
    $jobs += $collisionJob
    $null = $collisionJob | Wait-Job -Timeout 30
    $collisionResult = @($collisionJob | Receive-Job -ErrorAction Stop)
    Assert-Condition ($collisionResult.Count -eq 1 -and $collisionResult[0].Passed) 'Shared state-file lock failed.'
    Assert-Condition (!(Test-Path -LiteralPath $collisionState)) 'An unowned state file was overwritten.'

    Write-Output 'PASS: concurrent supervisors sharing a protected key, exact chat/project filtering, streaming suppression, duplicate events, delayed history, reset recovery, pagination, restart deduplication, initial and existing-chat sends, positional argument rejection, process locks, and stop isolation.'
} finally {
    foreach ($job in $jobs) {
        if ($job.State -eq 'Running') { $job | Stop-Job }
        $job | Remove-Job -Force
    }
    foreach ($mutex in $heldLocks) { $mutex.ReleaseMutex(); $mutex.Dispose() }
    $resolvedTestRoot = (Resolve-Path -LiteralPath $testRoot).Path
    $allowedPrefix = [IO.Path]::GetFullPath($temporaryRoot).TrimEnd('\') + '\sair-watcher-test-'
    if (!$resolvedTestRoot.StartsWith($allowedPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Refusing cleanup outside the test temporary directory.'
    }
    Remove-Item -LiteralPath $resolvedTestRoot -Recurse -Force
}
