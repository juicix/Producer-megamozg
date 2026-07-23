param(
  [string]$CodexSkillsPath = "$env:USERPROFILE\.codex\skills",
  [switch]$PackageForClaude
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$skillSource = Join-Path $repoRoot 'skills\producer-megamozg'

if (-not (Test-Path $skillSource)) {
  throw "Skill source not found: $skillSource"
}

New-Item -ItemType Directory -Path $CodexSkillsPath -Force | Out-Null
$target = Join-Path $CodexSkillsPath 'producer-megamozg'
Copy-Item -LiteralPath $skillSource -Destination $target -Recurse -Force
Write-Host "Codex skill installed to $target"

if ($PackageForClaude) {
  $zipPath = Join-Path $repoRoot 'producer-megamozg-claude-skill.zip'
  if (Test-Path $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
  Compress-Archive -Path (Join-Path $skillSource '*') -DestinationPath $zipPath -Force
  Write-Host "Claude upload package created: $zipPath"
}
