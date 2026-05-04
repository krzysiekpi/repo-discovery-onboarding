Do NOT run python -m agents.*

# /discovery

Generate a repository discovery report for a local target repo.

## Usage

```text
/discovery /absolute/path/to/repo
```

Optional:

```text
/discovery /absolute/path/to/repo --out ./reports/custom-name
```

## Step 0 - Resolve Paths

Use this Bash block to resolve paths and run the local CLI.

```bash
set -euo pipefail

COMMAND_REPO_ROOT="$(pwd)"
TARGET_REPO="$(printf '%s\n' "$ARGUMENTS" | awk '{print $1}')"
CUSTOM_OUT="$(printf '%s\n' "$ARGUMENTS" | sed -n 's/.*--out[[:space:]]\+\([^[:space:]]\+\).*/\1/p')"

if [ -z "$TARGET_REPO" ]; then
  echo "Usage: /discovery /absolute/path/to/repo [--out ./reports/name]"
  exit 2
fi

if [ ! -d "$TARGET_REPO" ]; then
  echo "Target repo does not exist: $TARGET_REPO"
  exit 2
fi

TARGET_NAME="$(basename "$TARGET_REPO")"
if [ -n "$CUSTOM_OUT" ]; then
  OUTPUT_DIR="$CUSTOM_OUT"
else
  OUTPUT_DIR="$COMMAND_REPO_ROOT/reports/$TARGET_NAME"
fi

printf 'COMMAND_REPO_ROOT=%s\nTARGET_REPO=%s\nOUTPUT_DIR=%s\n' "$COMMAND_REPO_ROOT" "$TARGET_REPO" "$OUTPUT_DIR"

PYTHONPATH="$COMMAND_REPO_ROOT/src" python3 -m repo_onboarding discovery \
  --repo "$TARGET_REPO" \
  --out "$OUTPUT_DIR"

printf 'DISCOVERY_REPORT=%s\n' "$OUTPUT_DIR/discovery.md"
```

## Step 1 - Return Result

Read the generated report path:

```text
reports/{repo-name}/discovery.md
```

Final response must include:

- path to `discovery.md`
- 3-5 bullet summary from the generated report
- any risks listed in "Risks and Open Questions"
