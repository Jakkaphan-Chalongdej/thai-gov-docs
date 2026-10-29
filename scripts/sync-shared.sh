#!/usr/bin/env bash
# Copies shared/ (scripts, fonts, brands) into every skill so each skill folder works on its own: a plugin
# install or a claude.ai zip carries only that folder. Edit shared/, never the copies.
#   scripts/sync-shared.sh          copy
#   scripts/sync-shared.sh --check  exit 1 if a copy differs from shared/
set -euo pipefail
cd "$(dirname "$0")/.."
status=0
for skill in plugins/*/skills/*/; do
  for part in scripts fonts brands; do
    if [ "${1:-}" = "--check" ]; then
      diff -rq -x __pycache__ -x .DS_Store "shared/$part" "$skill$part" >/dev/null 2>&1 || { echo "out of date: $skill$part"; status=1; }
    else
      rm -rf "$skill$part"
      cp -R "shared/$part" "$skill$part"
      find "$skill$part" \( -name __pycache__ -o -name .DS_Store \) -prune -exec rm -rf {} +
    fi
  done
done
exit $status
