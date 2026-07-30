param(
    [string]$PluginRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputDirectory = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

& (Join-Path $PSScriptRoot 'validate-package.ps1') -PluginRoot $PluginRoot

$manifest = Get-Content -LiteralPath (Join-Path $PluginRoot '.claude-plugin\plugin.json') -Encoding utf8 -Raw | ConvertFrom-Json
$pluginZip = Join-Path $OutputDirectory "employer-megamozg-plugin-v$($manifest.version).zip"
$projectZip = Join-Path $OutputDirectory "employer-megamozg-project-kit-v$($manifest.version).zip"

function New-ZipFromEntries {
    param(
        [string]$ZipPath,
        [array]$Entries
    )
    $stream = [System.IO.File]::Open($ZipPath, [System.IO.FileMode]::Create)
    try {
        $archive = [System.IO.Compression.ZipArchive]::new($stream, [System.IO.Compression.ZipArchiveMode]::Create, $false)
        try {
            foreach ($item in $Entries) {
                $entry = $archive.CreateEntry($item.EntryName.Replace('\', '/'), [System.IO.Compression.CompressionLevel]::Optimal)
                $entryStream = $entry.Open()
                try {
                    $source = [System.IO.File]::OpenRead($item.Source)
                    try { $source.CopyTo($entryStream) } finally { $source.Dispose() }
                } finally { $entryStream.Dispose() }
            }
        } finally { $archive.Dispose() }
    } finally { $stream.Dispose() }
}

$pluginEntries = foreach ($file in Get-ChildItem -LiteralPath $PluginRoot -File -Recurse -Force) {
    $relative = $file.FullName.Substring($PluginRoot.Length).TrimStart('\')
    if ($relative -notmatch '(^|\\)agents\\' -and $relative -notmatch '\.zip$') {
        [pscustomobject]@{ Source = $file.FullName; EntryName = $relative }
    }
}
New-ZipFromEntries -ZipPath $pluginZip -Entries @($pluginEntries)

$projectRoot = Join-Path $PluginRoot 'assets\project-template'
$projectEntries = foreach ($file in Get-ChildItem -LiteralPath $projectRoot -File) {
    [pscustomobject]@{ Source = $file.FullName; EntryName = $file.Name }
}
$projectEntries += [pscustomobject]@{
    Source = (Join-Path $PluginRoot 'assets\PROJECT_INSTRUCTIONS.md')
    EntryName = 'PROJECT_INSTRUCTIONS.md'
}
New-ZipFromEntries -ZipPath $projectZip -Entries @($projectEntries)

Write-Output $pluginZip
Write-Output $projectZip
