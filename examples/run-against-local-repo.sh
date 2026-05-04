#!/usr/bin/env bash
set -euo pipefail

TARGET_REPO="${1:?Usage: examples/run-against-local-repo.sh /path/to/repo}"

PYTHONPATH=src python3 -m repo_onboarding all \
  --repo "$TARGET_REPO" \
  --out ./reports/"$(basename "$TARGET_REPO")"
