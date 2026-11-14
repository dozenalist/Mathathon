# Scoped Open Math OS research supervisor transport. Requires PowerShell 7.
# Reads work/openmath-supervisor/request.json and writes response.json.
# Uses the explicitly authorized coordinator roster; never prints credentials.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'OpenMath.ps1')
$root = Join-Path (Split-Path -Parent $PSScriptRoot) 'work\openmath-supervisor'
$null = New-Item -ItemType Directory -Path $root -Force
$lock = [IO.File]::Open((Join-Path $root 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $statePath = Join-Path $root 'transport-state.json'
    $requestPath = Join-Path $root 'request.json'
    $responsePath = Join-Path $root 'response.json'
    $team = 'o-67dc4eac-a86a-439c-9459-ef86c31aeaa7'
    $project = 'p-a4e2849861784c708dd751c46b0f4f64'
    $policy = Get-Content -LiteralPath (Join-Path $root 'runtime-policy.json') -Raw | ConvertFrom-Json -AsHashtable
    $deadline = [DateTimeOffset]::Parse($policy.deadlineUtc)
    if ($policy.maxCoordinatorChats -ne 8 -or @($policy.activeSessions).Count -gt 8) { throw 'Invalid authorized coordinator cap.' }
    $state = @{ chats = @{}; done = @{}; pending = @{} }
    if (Test-Path $statePath) {
        $state = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json -AsHashtable
    }
    function Save-State {
        $state | ConvertTo-Json -Depth 80 | Set-Content -LiteralPath ($statePath + '.tmp') -Encoding utf8
        Move-Item -LiteralPath ($statePath + '.tmp') -Destination $statePath -Force
    }
    $request = Get-Content -LiteralPath $requestPath -Raw | ConvertFrom-Json -AsHashtable
    $out = [Collections.Generic.List[object]]::new()
    foreach ($item in $request.requests) {
        $id = [string]$item.id
        $op = [string]$item.operation
        if (-not $id -or $op -notin @('orgs','org_projects','project_sessions','chat_reads','session_history','files_list','files_download','model_catalog','org_model_usage','chat_create','chat_say','chat_stop','wake')) {
            throw 'Missing request id or unsupported operation.'
        }
        $write = $op -in @('chat_create','chat_say','chat_stop','wake')
        if ($write -and $state.done.ContainsKey($id)) {
            $out.Add(@{id=$id;result=$state.done[$id];replayed=$true})
            continue
        }
        if ($write -and $state.pending.ContainsKey($id)) {
            $out.Add(@{id=$id;error='Ambiguous prior write. Reconcile remote state; do not blindly resend.'})
            continue
        }
        $body = @{}
        if ($item.body) { foreach ($k in $item.body.Keys) { $body[$k] = $item.body[$k] } }
        $body.Remove('team'); $body.Remove('project')
        if ($op -notin @('orgs','model_catalog')) { $body.team = $team }
        if ($op -notin @('orgs','model_catalog','org_projects','org_model_usage','wake')) { $body.project = $project }
        if ($op -eq 'chat_create') {
            if ($body.title -notin @($policy.allowedNewTitles)) { throw 'Chat title is not explicitly authorized for this scale-up.' }
            if ($state.chats.ContainsKey([string]$body.title)) { throw 'Chat title already exists; reconcile before creating another.' }
            $createdScaleChats = @($policy.allowedNewTitles | Where-Object { $state.chats.ContainsKey([string]$_) }).Count
            $existingNonScaleChats = @($policy.activeSessions | Where-Object { $_ -notin @($policy.allowedNewTitles | ForEach-Object { $state.chats[[string]$_] }) }).Count
            if ($existingNonScaleChats + $createdScaleChats -ge $policy.maxCoordinatorChats) { throw 'Eight authorized coordinator chats already exist.' }
        }
        if ($op -eq 'chat_stop') { throw 'Do not interrupt existing work; let workers finish naturally.' }
        if ($op -eq 'chat_say' -and $body.session -notin @($policy.activeSessions)) {
            throw 'This chat is outside the authorized continuing roster: read findings but do not message it.'
        }
        if ($op -in @('chat_say','chat_stop') -and $body.session -notin @($state.chats.Values)) {
            throw 'Only supervisor-owned chats may receive messages or stops.'
        }
        if ($op -in @('chat_create','chat_say','wake') -and [DateTimeOffset]::UtcNow -ge $deadline) {
            $out.Add(@{id=$id;error='Research window ended; new work disabled.'}); continue
        }
        if ($op -eq 'chat_say') {
            $body.model = $policy.model
            if (-not $body.reasoning_effort) { $body.reasoning_effort = $policy.reasoningEffort }
            if ($body.reasoning_effort -ne 'max') { throw 'Use the supported max coordinator effort; verify actual Ultramath through swarm tool records, not the unsupported API effort string.' }
        }
        if ($write) { $state.pending[$id] = @{operation=$op;at=[DateTimeOffset]::UtcNow.ToString('o')}; Save-State }
        try {
            if ($op -eq 'files_download') {
                if ($body.path -match '(^/|(^|/)\.\.(/|$))') { throw 'Use a project-relative path.' }
                $secret = Import-Clixml -LiteralPath $script:OpenMathKeyPath
                $headers = $null
                try {
                    $headers = @{
                        Authorization = 'Bearer ' + [Net.NetworkCredential]::new('', $secret).Password
                        'x-nucleus-arg' = (ConvertTo-Json -InputObject $body -Compress)
                    }
                    $r = Invoke-WebRequest -Uri 'https://os.openmathmodel.org/v1/files_download' -Method Post -Headers $headers -TimeoutSec 60 -MaximumRedirection 0 -Verbose:$false -Debug:$false
                    $content = $r.Content
                    if ($content -is [byte[]]) { $content = [Text.Encoding]::UTF8.GetString($content) }
                    $result = @{path=$body.path;text=[string]$content}
                } finally {
                    if ($null -ne $headers) { $headers.Clear() }
                    if ($null -ne $secret) { $secret.Dispose() }
                }
            } elseif ($op -eq 'session_history') {
                $pageBudget = 1
                if ($body.ContainsKey('page_budget')) { $pageBudget = [Math]::Clamp([int]$body.page_budget, 1, 25); $body.Remove('page_budget') }
                $kept = [Collections.Generic.List[object]]::new()
                $swarmCalls = @{}
                $pages = 0; $rawCount = 0; $lastSeq = $body.after; $lastKind = $null; $model = $null
                do {
                    $page = Invoke-OpenMathPlatform -Operation $op -Body $body
                    $pages++; $rawCount += @($page.records).Count
                    foreach ($record in $page.records) {
                        $lastSeq = $record.seq; $lastKind = $record.kind
                        if ($record.kind -eq 'model_call') { $model = $record.served_by }
                        if ($record.kind -in @('user','turn_complete','error','turn_failed','cancelled') -or ($record.kind -eq 'assistant' -and $record.text)) { $kept.Add($record) }
                        elseif ($record.kind -eq 'model_call') {
                            $kept.Add(@{seq=$record.seq;kind=$record.kind;served_by=$record.served_by;reasoning_effort=$record.reasoning_effort;reasoning_mode=$record.reasoning_mode;at_ms=$record.at_ms})
                        } elseif ($record.kind -eq 'tool_call' -and $record.name -match 'ultramath|swarm') {
                            $swarmCalls[[string]$record.call_id] = $true
                            $kept.Add($record)
                        } elseif ($record.kind -eq 'tool_result' -and $swarmCalls.ContainsKey([string]$record.call_id)) { $kept.Add($record) }
                        elseif ($record.kind -match '^ultramath_|^swarm_') { $kept.Add($record) }
                    }
                    if ($null -eq $page.next -or $pages -ge $pageBudget) { break }
                    $body.after = $page.next
                } while ($true)
                $result = @{records=@($kept.ToArray());next=$page.next;last_seq=$lastSeq;last_kind=$lastKind;model=$model;pages=$pages;raw_count=$rawCount}
            } else {
                $result = Invoke-OpenMathPlatform -Operation $op -Body $body
                if ($op -eq 'model_catalog') {
                    $result = @{models=$result.models;swarm_models=$result.swarm_models}
                }
            }
            if ($write) {
                if ($op -eq 'chat_create') { $state.chats[$body.title] = $result.session }
                $state.done[$id] = $result
                $state.pending.Remove($id)
                Save-State
            }
            $out.Add(@{id=$id;result=$result})
        } catch {
            # Pending writes intentionally stay pending until reconciled after any failure.
            $safeStatus = 0
            if ($null -ne $_.Exception.Response) { $safeStatus = [int]$_.Exception.Response.StatusCode }
            elseif ($_.Exception.Message -match '^Open Math OS request failed \(HTTP (\d+)\)\.') { $safeStatus = [int]$Matches[1] }
            $safeCategory = switch ($safeStatus) { 401 {'authentication'} 403 {'permission'} 409 {'state_conflict'} 429 {'rate_or_quota'} 502 {'upstream_unavailable'} 503 {'unavailable'} 504 {'deadline'} 0 {'local_or_connection'} default {'http_failure'} }
            $out.Add(@{id=$id;http_status=$safeStatus;category=$safeCategory;error='Request failed. For writes reconcile before retrying; credential/request details suppressed.'})
        }
        # Incremental results survive interruption without resending completed writes.
        @{at=[DateTimeOffset]::UtcNow.ToString('o');results=@($out.ToArray());chats=$state.chats} |
            ConvertTo-Json -Depth 80 | Set-Content -LiteralPath $responsePath -Encoding utf8
    }
    Write-Output ('Processed {0} requests. Results saved to work/openmath-supervisor/response.json. Managed chats: {1}.' -f $out.Count,$state.chats.Count)
} finally { $lock.Dispose() }

