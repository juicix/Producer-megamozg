param(
  [string]$CodexSkillsPath = "$env:USERPROFILE\.codex\skills",
  [switch]$PackageForClaude
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$skillSource = $repoRoot

if (-not (Test-Path $skillSource)) {
  throw "Skill source not found: $skillSource"
}

New-Item -ItemType Directory -Path $CodexSkillsPath -Force | Out-Null
$target = Join-Path $CodexSkillsPath 'producer-megamozg'
New-Item -ItemType Directory -Path $target -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $skillSource 'SKILL.md') -Destination $target -Force
Copy-Item -LiteralPath (Join-Path $skillSource 'agents'),(Join-Path $skillSource 'assets'),(Join-Path $skillSource 'references') -Destination $target -Recurse -Force
Write-Host "Codex skill installed to $target"

if ($PackageForClaude) {
  $zipPath = Join-Path $repoRoot 'producer-megamozg-claude-skill.zip'
  if (Test-Path $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
  Compress-Archive -Path (Join-Path $skillSource 'SKILL.md'),(Join-Path $skillSource 'agents'),(Join-Path $skillSource 'assets'),(Join-Path $skillSource 'references') -DestinationPath $zipPath -Force
  Write-Host "Claude upload package created: $zipPath"
}
