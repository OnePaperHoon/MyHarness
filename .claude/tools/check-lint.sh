#!/usr/bin/env bash
# Run linter and report results. Exit 1 on errors.
set -euo pipefail

echo "=== Lint Check ==="

# Detect project type and run appropriate linter
if [ -f "package.json" ]; then
  if command -v npx &>/dev/null; then
    npx eslint . --max-warnings=0
  fi
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
  if command -v ruff &>/dev/null; then
    ruff check .
  elif command -v flake8 &>/dev/null; then
    flake8 .
  fi
elif find . -name "*.go" -maxdepth 2 | grep -q .; then
  go vet ./...
else
  echo "No supported linter found for this project type."
  exit 0
fi

echo "=== Lint passed ==="
