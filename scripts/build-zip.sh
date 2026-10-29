#!/usr/bin/env bash
# Builds dist/srs-sds.zip from the plugin's skill, for claude.ai (Settings → Capabilities → Skills) or ~/.claude/skills.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/srs-sds.zip
(cd plugins/srs-sds/skills && zip -qr ../../../dist/srs-sds.zip srs-sds -x '*.DS_Store' 'srs-sds/.venv/*' 'srs-sds/.tools/*' '*/__pycache__/*')
echo dist/srs-sds.zip
