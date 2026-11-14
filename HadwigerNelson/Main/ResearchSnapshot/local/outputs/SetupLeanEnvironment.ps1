# Prepare an isolated, exactly pinned local environment. No global defaults change.
[CmdletBinding()]
param([switch]$Run, [switch]$Cache, [switch]$FullCache)
if ($FullCache) { $Cache = $true }
$ErrorActionPreference = 'Stop'
$envRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\work\lean-env'))
$queueRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\work\lean-queue'))
$statePath = Join-Path $envRoot 'setup-status.json'
if (-not $Run) {
    if (Test-Path -LiteralPath $statePath) {
        $previous = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
        if ($previous.state -in @('starting','running')) { throw 'Setup already marked active; inspect status/process before retrying.' }
    }
    @{ state='starting'; startedUtc=[DateTime]::UtcNow.ToString('o') } | ConvertTo-Json | Set-Content -LiteralPath $statePath -Encoding utf8
    $hostExe = (Get-Process -Id $PID).Path
    $childArgs = @('-NoProfile','-File',('"' + $PSCommandPath + '"'),'-Run')
    if ($Cache) { $childArgs += '-Cache' }
    if ($FullCache) { $childArgs += '-FullCache' }
    $child = Start-Process -FilePath $hostExe -ArgumentList $childArgs -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $envRoot 'launcher.out') -RedirectStandardError (Join-Path $envRoot 'launcher.err')
    Write-Output ('Started isolated Lean setup, process {0}. Status: work/lean-env/setup-status.json' -f $child.Id)
    return
}
$status = @{ state='running'; stage='starting'; processId=$PID; startedUtc=[DateTime]::UtcNow.ToString('o') }
$queueLock = $null
function Save-SetupStatus {
    $status.updatedUtc = [DateTime]::UtcNow.ToString('o')
    $status | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $statePath -Encoding utf8
}
function Invoke-SetupStep([string]$step, [string]$exe, [string[]]$arguments, [string]$workingDirectory, [int]$seconds=1200) {
    $status.stage=$step
    Save-SetupStatus
    $info=[Diagnostics.ProcessStartInfo]::new()
    $info.FileName=$exe
    $info.WorkingDirectory=$workingDirectory
    $info.UseShellExecute=$false
    $info.CreateNoWindow=$true
    $info.RedirectStandardOutput=$true
    $info.RedirectStandardError=$true
    foreach ($arg in $arguments) { $info.ArgumentList.Add($arg) }
    $process=[Diagnostics.Process]::new()
    $process.StartInfo=$info
    $started=$false
    try {
        [void]$process.Start()
        $started=$true
        $status.childProcessId=$process.Id
        Save-SetupStatus
        $outTask=$process.StandardOutput.ReadToEndAsync()
        $errTask=$process.StandardError.ReadToEndAsync()
        $stepClock = [Diagnostics.Stopwatch]::StartNew()
        while (-not $process.WaitForExit(1000)) {
            if ($stepClock.Elapsed.TotalSeconds -ge $seconds) { $process.Kill($true); $process.WaitForExit(); throw ('Setup step timed out: '+$step) }
            if ($step -like 'fetch-*-cache') {
                $freeBytes = ([IO.DriveInfo]::new([IO.Path]::GetPathRoot($workingDirectory))).AvailableFreeSpace
                if ($freeBytes -lt 3GB) { $process.Kill($true); $process.WaitForExit(); throw 'Cache preparation stopped to preserve at least 3 GB free disk space.' }
            }
        }
        $outText=$outTask.GetAwaiter().GetResult()
        $errText=$errTask.GetAwaiter().GetResult()
        ($outText + "`n" + $errText) | Set-Content -LiteralPath (Join-Path $envRoot ($step+'.log')) -Encoding utf8
        if ($process.ExitCode -ne 0) { throw ('Setup step {0} failed, exit {1}; inspect its log.' -f $step,$process.ExitCode) }
        return $outText.Trim()
    } finally {
        if ($started -and -not $process.HasExited) { $process.Kill($true); $process.WaitForExit() }
        $process.Dispose()
        $status.Remove('childProcessId')
    }
}
try {
    $queueLock=[IO.File]::Open((Join-Path $queueRoot 'queue.lock'),'OpenOrCreate','ReadWrite','None')
    $queue=Get-Content -LiteralPath (Join-Path $queueRoot 'queue.json') -Raw | ConvertFrom-Json
    if (@($queue.jobs | Where-Object { $_.status -eq 'running' }).Count) { throw 'A proof job is marked running; reconcile it before setup.' }
    $expected=Get-Content -LiteralPath (Join-Path $envRoot 'expected-manifest.json') -Raw | ConvertFrom-Json -AsHashtable
    $git=(Get-Command git.exe -ErrorAction Stop).Source
    $elan='C:\Users\jarom\.elan\bin\elan.exe'
    if (-not (Test-Path -LiteralPath $elan -PathType Leaf)) { throw 'Existing elan executable not found.' }
    # These environment changes affect this process and its children only.
    $env:ELAN_HOME=Join-Path $envRoot 'elan'
    $env:MATHLIB_CACHE_DIR=Join-Path $envRoot 'cache'
    $env:MATHLIB_NO_CACHE_ON_UPDATE='1'
    $env:LEAN_NUM_THREADS='1'
    if (-not $Cache) { $null=Invoke-SetupStep 'install-toolchain' $elan @('toolchain','install','leanprover/lean4:v4.34.1') $envRoot }
    $nativeBin=Join-Path $env:ELAN_HOME 'toolchains\leanprover--lean4---v4.34.1\bin'
    $leanExe=Join-Path $nativeBin 'lean.exe'
    $version=Invoke-SetupStep 'verify-toolchain' $leanExe @('--version') $envRoot 60
    if ($version -notmatch '4\.34\.1' -or $version -notmatch '5045d0056413266e57c625dcd7c365b10e377c52') { throw 'Downloaded toolchain version/commit does not match the remote pin.' }
    $status.leanVersion=$version
    $status.leanExe=$leanExe
    $repo=Join-Path $envRoot 'mathlib4'
    if (-not (Test-Path -LiteralPath $repo)) {
        $null=Invoke-SetupStep 'clone-mathlib' $git @('clone','--filter=blob:none','--no-checkout','--quiet','https://github.com/leanprover-community/mathlib4.git',$repo) $envRoot
    }
    if (-not (Test-Path -LiteralPath (Join-Path $repo '.git'))) { throw 'Expected an isolated git checkout; refusing to overwrite an existing directory.' }
    $remote=Invoke-SetupStep 'verify-remote' $git @('-C',$repo,'remote','get-url','origin') $envRoot 60
    if ($remote -ne 'https://github.com/leanprover-community/mathlib4.git') { throw 'Unexpected Mathlib source remote.' }
    if (-not $Cache) { $null=Invoke-SetupStep 'checkout-pin' $git @('-c','core.longpaths=true','-C',$repo,'checkout','--detach',$expected.mathlib_commit) $envRoot }
    $head=Invoke-SetupStep 'verify-mathlib' $git @('-C',$repo,'rev-parse','HEAD') $envRoot 60
    if ($head -ne $expected.mathlib_commit) { throw 'Mathlib revision mismatch.' }
    $toolchain=(Get-Content -LiteralPath (Join-Path $repo 'lean-toolchain') -Raw).Trim()
    if ($toolchain -ne $expected.lean_toolchain_file) { throw 'Mathlib toolchain mismatch.' }
    $actual=Get-Content -LiteralPath (Join-Path $repo 'lake-manifest.json') -Raw | ConvertFrom-Json -AsHashtable
    foreach ($name in $expected.pinned_dependency_revs.Keys) {
        $package=@($actual.packages | Where-Object { $_.name -ceq $name })
        if ($package.Count -ne 1 -or $package[0].rev -ne $expected.pinned_dependency_revs[$name]) { throw ('Dependency pin mismatch: '+$name) }
    }
    $status.mathlibCommit=$head
    $status.mathlibRoot=$repo
    $status.state='sources_ready_cache_pending'
    $status.stage='ready_for_cache'
    $status.note='Pinned Lean and Mathlib source/manifest verified. No candidate proof or full Mathlib build has run. Fetch matching cached artifacts as the next serial setup step.'
    if ($Cache) {
        $env:PATH = $nativeBin + [IO.Path]::PathSeparator + $env:PATH
        $env:ELAN_TOOLCHAIN = 'leanprover/lean4:v4.34.1'
        $cacheRoots = @('Mathlib.Topology.Order.IntermediateValue','Mathlib.Analysis.Normed.Group.Real','Mathlib.Analysis.Normed.Group.Continuity','Mathlib.Analysis.Normed.Group.Uniform','Mathlib.Tactic.Push','Mathlib.Tactic.Linarith','Mathlib.Tactic.Ring','Mathlib.Data.ZMod.Basic','Mathlib.Data.Finset.Image','Mathlib.Data.Fintype.Basic')
        if ($FullCache) {
            $freeBytes = ([IO.DriveInfo]::new([IO.Path]::GetPathRoot($repo))).AvailableFreeSpace
            if ($freeBytes -lt 12GB) { throw 'Full Mathlib cache needs at least 12 GB free before starting; minimal cache remains usable.' }
            $cacheRoots = @('Mathlib')
            $status.freeBytesBeforeFullCache = $freeBytes
        }
        $status.cacheRoots = $cacheRoots
        $status.state='running'
        $lakeExe=Join-Path $nativeBin 'lake.exe'
        $cacheStep = if ($FullCache) { 'fetch-full-cache' } else { 'fetch-minimal-cache' }
        $null=Invoke-SetupStep $cacheStep $lakeExe (@('exe','cache','get') + $cacheRoots) $repo 1200
        $actual=Get-Content -LiteralPath (Join-Path $repo 'lake-manifest.json') -Raw | ConvertFrom-Json -AsHashtable
        foreach ($name in $expected.pinned_dependency_revs.Keys) {
            $package=@($actual.packages | Where-Object { $_.name -ceq $name })
            if ($package.Count -ne 1 -or $package[0].rev -ne $expected.pinned_dependency_revs[$name]) { throw ('Dependency pin changed during cache preparation: '+$name) }
        }
        foreach ($mod in $cacheRoots) {
            $relativeModule=$mod.Replace('.', [IO.Path]::DirectorySeparatorChar) + '.olean'
            if (-not (Test-Path -LiteralPath (Join-Path $repo ('.lake\build\lib\lean\'+$relativeModule)))) { throw ('Required cached root is missing: '+$mod) }
        }
        $leanPaths=@((Join-Path $repo '.lake\build\lib\lean'))
        foreach ($packageDir in (Get-ChildItem -LiteralPath (Join-Path $repo '.lake\packages') -Directory)) {
            $packageLib=Join-Path $packageDir.FullName '.lake\build\lib\lean'
            if (Test-Path -LiteralPath $packageLib -PathType Container) { $leanPaths += $packageLib }
        }
        $status.leanPath=$leanPaths -join [IO.Path]::PathSeparator
        $status.state='ready'
        $status.stage='minimal_cache_ready'
        $status.note='Pinned minimal Mathlib cache is ready for an explicitly narrowed-import check. The umbrella import Mathlib is NOT cached or verified by this setup.'
        if ($FullCache) {
            $status.stage='full_mathlib_cache_ready'
            $status.note='Pinned umbrella Mathlib cache is ready. Project sources still require separate serial builds and statement/axiom verification.'
        }
    }
    Save-SetupStatus
} catch {
    $status.state='failed'
    $status.error=$_.Exception.Message
    Save-SetupStatus
    throw
} finally {
    if ($null -ne $queueLock) { $queueLock.Dispose() }
}
