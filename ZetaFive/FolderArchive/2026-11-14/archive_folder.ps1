param(
    [string]$SourceRoot = $PSScriptRoot,
    [string]$Destination = (Join-Path $PSScriptRoot 'tmp/github-folder-archive/ZetaFive/FolderArchive/2026-11-14')
)

$ErrorActionPreference = 'Stop'
$archiveSource = [IO.Path]::GetFullPath($SourceRoot)
$archiveDestination = [IO.Path]::GetFullPath($Destination)
if ($archiveSource -eq $archiveDestination) { throw 'Source and destination must differ.' }
if (Test-Path -LiteralPath $archiveDestination) { throw 'Choose a new, empty snapshot destination.' }
New-Item -ItemType Directory -Path $archiveDestination -Force | Out-Null

# Enumerate only research roots; never descend into temporary repository copies.
$archiveFiles = @(
    Get-ChildItem -LiteralPath $archiveSource -Force -File
    Get-ChildItem -LiteralPath $archiveSource -Force -Directory |
        Where-Object { $_.Name -notin @('.git', 'tmp', '__pycache__', '.codex', '.agents', '.aws') } |
        ForEach-Object { Get-ChildItem -LiteralPath $_.FullName -Recurse -Force -File }
)
$archiveFiles = @($archiveFiles | Where-Object {
    $relative = [IO.Path]::GetRelativePath($archiveSource, $_.FullName).Replace('\', '/')
    $relative -notmatch '(^|/)(\.git|__pycache__)/|^zeta9_draft/tools/' -and
    $_.Extension -notin @('.pyc', '.pyo')
})
$extraResearchFiles = @(
    'tmp/full-argument-authoring/assemble_backbone.py',
    'tmp/full-argument-authoring/build_source_ledger.py',
    'tmp/lai_section_checks/check_arithmetic.py',
    'tmp/lai_section_checks/results.txt',
    'tmp/exposition-audit/check_lai_gamma_exact.cjs',
    'tmp/exposition-audit/check_lai_gamma_exact_results.json',
    'tmp/exposition-audit/local_phrase_comparison.json',
    'tmp/exposition-audit/manifest.json',
    'tmp/parallel-revision/chat_review.json'
)
foreach ($relative in $extraResearchFiles) {
    $archiveFiles += Get-Item -LiteralPath (Join-Path $archiveSource $relative)
}

$archiveEntries = foreach ($file in ($archiveFiles | Sort-Object FullName -Unique)) {
    $relative = [IO.Path]::GetRelativePath($archiveSource, $file.FullName).Replace('\', '/')
    $target = Join-Path $archiveDestination $relative
    New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $target
    $sourceHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    $copyHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sourceHash -ne $copyHash) { throw "Copy mismatch: $relative" }
    [ordered]@{ path = $relative; bytes = $file.Length; sha256 = $copyHash }
}

# Preserve exact source bytes even on checkouts with automatic line-ending conversion.
[IO.File]::WriteAllText((Join-Path $archiveDestination '.gitattributes'), "* -text`n")
$archiveManifest = [ordered]@{
    format_version = 1
    snapshot_date = '2026-11-14'
    timezone = 'America/Los_Angeles'
    created_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
    source_folder = 'Zeta 5'
    file_count = $archiveEntries.Count
    total_bytes = ($archiveEntries | ForEach-Object { $_.bytes } | Measure-Object -Sum).Sum
    scope = 'Research files and visible project chat messages; original folder-relative paths retained.'
    exclusions = @(
        'Git metadata and nested temporary repository checkouts',
        'Python bytecode and __pycache__',
        'zeta9_draft/tools: downloaded TeX runtime and cache',
        'Temporary render copies and duplicate consolidation workspaces',
        'SAIR operational run state, local credentials, raw tool/chat payloads',
        'Other tmp files except the nine explicitly listed research scripts, results, and provenance records'
    )
    generated_archive_files = @('.gitattributes', 'archive_manifest.json', 'README.md')
    files = @($archiveEntries)
}
$archiveManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $archiveDestination 'archive_manifest.json') -Encoding utf8NoBOM
"Archived $($archiveEntries.Count) source files; $($archiveManifest.total_bytes) bytes. Every copied SHA-256 verified."
