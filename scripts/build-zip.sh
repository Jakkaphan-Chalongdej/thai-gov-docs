#!/usr/bin/env bash
# Builds dist/<skill>.zip for every skill, for claude.ai (Settings → Capabilities → Skills) or ~/.claude/skills.
set -euo pipefail
cd "$(dirname "$0")/.."
scripts/sync-shared.sh
mkdir -p dist
for skill in plugins/*/skills/*/; do
  name=$(basename "$skill")
  rm -f "dist/$name.zip"
  (cd "$(dirname "$skill")" && zip -qr "../../../dist/$name.zip" "$name" -x '*.DS_Store' "$name/.venv/*" "$name/.tools/*" '*/__pycache__/*')
  echo "dist/$name.zip"
done
