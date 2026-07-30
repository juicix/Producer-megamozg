param(
    [string]$PluginRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$utf8Strict = [System.Text.UTF8Encoding]::new($false, $true)

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

$manifestPath = Join-Path $PluginRoot '.claude-plugin\plugin.json'
Assert-True (Test-Path -LiteralPath $manifestPath -PathType Leaf) 'Missing .claude-plugin/plugin.json'
$manifest = Get-Content -LiteralPath $manifestPath -Encoding utf8 -Raw | ConvertFrom-Json
Assert-True ($manifest.name -eq 'employer-megamozg') 'Wrong plugin name in manifest'
Assert-True ($manifest.version -match '^\d+\.\d+\.\d+$') 'Version must use semver'

$skillRoot = Join-Path $PluginRoot 'skills'
$skills = @(Get-ChildItem -LiteralPath $skillRoot -Directory)
Assert-True ($skills.Count -eq 7) "Expected 7 skills, found $($skills.Count)"

foreach ($skill in $skills) {
    $skillFile = Join-Path $skill.FullName 'SKILL.md'
    Assert-True (Test-Path -LiteralPath $skillFile -PathType Leaf) "Missing SKILL.md: $($skill.Name)"
    $bytes = [System.IO.File]::ReadAllBytes($skillFile)
    $text = $utf8Strict.GetString($bytes)
    Assert-True ($text.StartsWith("---`n") -or $text.StartsWith("---`r`n")) "Missing YAML frontmatter: $($skill.Name)"
    Assert-True ($text -match '(?m)^name:\s*.+$') "Missing name: $($skill.Name)"
    Assert-True ($text -match '(?m)^description:\s*.+$') "Missing description: $($skill.Name)"
    Assert-True ($text -notmatch '(?i)\bTODO\b') "TODO remains: $($skill.Name)"
}

$transcriptRoot = Join-Path $skillRoot 'producer-megamozg\references\transcripts'
$transcripts = @(Get-ChildItem -LiteralPath $transcriptRoot -File | Where-Object Name -ne '00-index.md')
Assert-True ($transcripts.Count -eq 13) "Expected 13 transcripts, found $($transcripts.Count)"

$projectTemplateRoot = Join-Path -Path $PluginRoot -ChildPath "assets\project-template"
$projectFiles = @(Get-ChildItem -LiteralPath $projectTemplateRoot -File)
Assert-True ($projectFiles.Count -eq 13) "Expected 13 Project files, found $($projectFiles.Count)"

Write-Output "OK: plugin=$($manifest.name) version=$($manifest.version) skills=$($skills.Count) transcripts=$($transcripts.Count) project_files=$($projectFiles.Count)"
