# Claude Code 하네스 초기화 TUI 실행 스크립트
param(
    [string]$TargetDir = "."
)

$ErrorActionPreference = "Stop"

# 의존성 확인 및 설치
Write-Host "의존성 확인 중..." -ForegroundColor Cyan

$requirementsFile = Join-Path $PSScriptRoot "requirements.txt"

try {
    python -c "import textual" 2>$null
} catch {
    Write-Host "textual 설치 중..." -ForegroundColor Yellow
    pip install -r $requirementsFile
}

# TUI 실행
$scriptPath = Join-Path $PSScriptRoot "init-harness.py"
$resolvedTarget = Resolve-Path $TargetDir

Write-Host "하네스 초기화 TUI 시작: $resolvedTarget" -ForegroundColor Green
python $scriptPath $resolvedTarget
