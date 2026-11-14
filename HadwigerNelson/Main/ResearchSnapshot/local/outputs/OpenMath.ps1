# Open Math OS Platform API helper for Windows PowerShell 5.1 and PowerShell 7.
# Dot-source this file with -Setup to enter, validate and encrypt your key:
# . 'C:\Users\jarom\Documents\Codex\2026-11-13\i\outputs\OpenMath.ps1' -Setup
# Later, dot-source without -Setup to reuse the saved key.
[CmdletBinding()]
param([switch]$Setup)

if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw 'This helper requires Windows for DPAPI-protected credential storage.'
}
$script:OpenMathKeyPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'work\openmath\platform-key.xml'

function Invoke-OpenMathPlatform {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][ValidatePattern('^[a-z][a-z_]*$')][string]$Operation,
        [hashtable]$Body = @{},
        [Security.SecureString]$Key
    )
    if ($Operation -in @('files_upload', 'files_download')) {
        throw 'Binary file operations use x-nucleus-arg and are not supported by this JSON helper.'
    }
    $ownsKey = $false
    if ($null -eq $Key) {
        if (-not (Test-Path -LiteralPath $script:OpenMathKeyPath)) {
            throw 'No saved platform key. Run Set-OpenMathPlatformKey first.'
        }
        try {
            $Key = Import-Clixml -LiteralPath $script:OpenMathKeyPath -ErrorAction Stop
            $ownsKey = $true
        } catch {
            throw 'Cannot decrypt the saved key. Run Set-OpenMathPlatformKey under your Windows account.'
        }
    }
    $plain = $null
    $headers = $null
    try {
        $plain = [Net.NetworkCredential]::new('', $Key).Password
        if ($plain -notmatch '^nuc_oc_\S+$') {
            throw 'Use a Platform API key starting with nuc_oc_, with no surrounding whitespace.'
        }
        $headers = @{ Authorization = 'Bearer ' + $plain }
        $json = ConvertTo-Json -InputObject $Body -Depth 50 -Compress
        try {
            Invoke-RestMethod -Uri ('https://os.openmathmodel.org/v1/' + $Operation) `
                -Method Post -Headers $headers -ContentType 'application/json; charset=utf-8' `
                -Body ([Text.Encoding]::UTF8.GetBytes($json)) -TimeoutSec 60 `
                -MaximumRedirection 0 -ErrorAction Stop -Verbose:$false -Debug:$false
        } catch {
            $status = 0
            if ($null -ne $_.Exception.Response) {
                $status = [int]$_.Exception.Response.StatusCode
            }
            $hint = switch ($status) {
                401 { 'Key rejected. Create a new Platform API key and run Set-OpenMathPlatformKey.' }
                403 { 'Your account lacks permission for this operation.' }
                409 { 'State conflict; the operation may require waking the team VM.' }
                429 { 'Rate or quota limit reached. Try later.' }
                0   { 'Connection failed or timed out. Check network access.' }
                default { 'Check the operation and fields against the API reference.' }
            }
            # Do not print raw request objects, headers, or server error bodies.
            throw ('Open Math OS request failed (HTTP {0}). {1}' -f $status, $hint)
        }
    } finally {
        if ($null -ne $headers) { $headers.Clear() }
        $plain = $null
        if ($ownsKey -and $null -ne $Key) { $Key.Dispose() }
    }
}

function Set-OpenMathPlatformKey {
    [CmdletBinding()]
    param()
    $secret = Read-Host 'Paste your Open Math OS PLATFORM key (input hidden)' -AsSecureString
    try {
        # Validate via a read-only operation before saving. No model call is made.
        $result = Invoke-OpenMathPlatform -Operation orgs -Key $secret
        $directory = Split-Path -Parent $script:OpenMathKeyPath
        $null = New-Item -ItemType Directory -Path $directory -Force -ErrorAction Stop
        # On Windows, Export-Clixml encrypts SecureString using user-scoped DPAPI.
        $secret | Export-Clixml -LiteralPath $script:OpenMathKeyPath -Force -ErrorAction Stop
        Write-Host ('Connected. Key encrypted locally. Teams on first page: {0}.' -f @($result.orgs).Count)
    } finally {
        if ($null -ne $secret) { $secret.Dispose() }
    }
}

function Test-OpenMathConnection {
    [CmdletBinding()]
    param()
    $result = Invoke-OpenMathPlatform -Operation orgs
    Write-Host ('Connected. Teams on first page: {0}.' -f @($result.orgs).Count)
}

if ($Setup) { Set-OpenMathPlatformKey }

